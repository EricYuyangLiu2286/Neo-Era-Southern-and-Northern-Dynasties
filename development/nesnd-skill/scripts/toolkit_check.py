"""Run the installed Paradox Modding Toolkit language server over stdio on chosen files (read-only).

python scripts/toolkit_check.py --out <report dir> <MOD-relative file> ...
  --mod     mod root (default: main MOD)
  --server  path to the Toolkit's dist/server.js (default: newest jdeffner.px-toolkit-* in ~/.vscode/extensions)

An unsaved buffer with one extra '}' is sent first as a negative control; the run fails if the
server does not report it. Files on disk are never changed. Writes toolkit-checks.json and
toolkit-protocol.json in --out. Status PASS means no diagnostics; it is not engine validation.
Generalised from the per-report toolkit.py copies of 2026-11-06/07.
"""
import argparse, json, os, queue, subprocess, threading, time
from pathlib import Path
from catalog import MOD, GAME

def newest_server():
    ext = Path.home() / '.vscode' / 'extensions'
    found = sorted(ext.glob('jdeffner.px-toolkit-*/dist/server.js'),
                   key=lambda p: [int(x) if x.isdigit() else x for x in p.parts[-3].split('-')[-1].split('.')])
    if not found: raise FileNotFoundError('Paradox Modding Toolkit not found under ' + str(ext))
    return found[-1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+'); ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--mod', type=Path, default=MOD); ap.add_argument('--server', type=Path)
    a = ap.parse_args()
    R, O = a.mod.resolve(), a.out.resolve(); O.mkdir(parents=True, exist_ok=True)
    server = a.server or newest_server()
    files = [f.replace('\\', '/') for f in a.files]
    for f in files:
        if not (R / f).is_file(): raise FileNotFoundError(R / f)
    config = {'gameId': 'vic3', 'gamePath': str(GAME).replace('\\', '/'), 'modPath': str(R), 'tigerRunOn': 'manual',
              'diagnostics': {'vanilla': False, 'ignore': [], 'ignorePatterns': []}}
    q, messages, diagnostics = queue.Queue(), [], {}
    err = (O / 'toolkit-stderr.log').open('wb')
    p = subprocess.Popen(['node', str(server), '--stdio'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err,
                         cwd=R, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    def reader():
        while True:
            headers = {}
            while True:
                line = p.stdout.readline()
                if not line: return
                if line == b'\r\n': break
                k, v = line.decode().split(':', 1); headers[k.lower()] = v.strip()
            q.put(json.loads(p.stdout.read(int(headers['content-length']))))
    threading.Thread(target=reader, daemon=True).start()
    def send(m):
        data = json.dumps({'jsonrpc': '2.0', **m}).encode()
        p.stdin.write(f'Content-Length: {len(data)}\r\n\r\n'.encode() + data); p.stdin.flush()
    def get(timeout=1):
        try: m = q.get(timeout=timeout)
        except queue.Empty: return None
        messages.append(m)
        if m.get('method') == 'workspace/configuration':
            vals = []
            for item in m['params']['items']:
                section = item.get('section', 'px'); v = config
                if section not in ('px', ''):
                    for k in section.removeprefix('px.').split('.'): v = v.get(k, {}) if isinstance(v, dict) else None
                vals.append(v)
            send({'id': m['id'], 'result': vals})
        elif 'id' in m and 'method' in m: send({'id': m['id'], 'result': None})
        if m.get('method') == 'textDocument/publishDiagnostics':
            diagnostics[m['params']['uri']] = m['params']['diagnostics']
        return m
    def wait_for(cond, seconds):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            m = get()
            if cond(m): return True
        return False
    try:
        send({'id': 1, 'method': 'initialize', 'params': {'processId': os.getpid(), 'rootUri': R.as_uri(),
              'workspaceFolders': [{'uri': R.as_uri(), 'name': 'NESND'}],
              'capabilities': {'workspace': {'configuration': True}, 'textDocument': {'publishDiagnostics': {}}}}})
        assert wait_for(lambda m: m and m.get('id') == 1 and 'result' in m, 45), 'Toolkit initialize timed out'
        send({'method': 'initialized', 'params': {}})
        send({'method': 'workspace/didChangeConfiguration', 'params': {'settings': {'px': config}}})
        for f in files:
            path = R / f
            send({'method': 'textDocument/didOpen', 'params': {'textDocument': {
                'uri': path.as_uri(), 'languageId': 'paradox-loc' if f.endswith('.yml') else 'paradox',
                'version': 1, 'text': path.read_text('utf-8')}}})
        wanted = {(R / f).as_uri() for f in files}
        wait_for(lambda m: wanted.issubset(diagnostics), 45)
        control = (R / files[0]).as_uri(); original = (R / files[0]).read_text('utf-8')
        diagnostics.pop(control, None)
        send({'method': 'textDocument/didChange', 'params': {'textDocument': {'uri': control, 'version': 2},
              'contentChanges': [{'text': original + '\n}\n'}]}})
        wait_for(lambda m: control in diagnostics, 10)
        negative = diagnostics.get(control, [])
        assert any(x.get('code') == 'stray-close' for x in negative), ('Negative control not detected', negative)
        diagnostics.pop(control, None)
        send({'method': 'textDocument/didChange', 'params': {'textDocument': {'uri': control, 'version': 3},
              'contentChanges': [{'text': original}]}})
        wait_for(lambda m: control in diagnostics, 10)
        missing = sorted(wanted - set(diagnostics))
        result = {'server': str(server), 'engine_verified': False, 'config': config, 'missing_diagnostics': missing,
                  'unsaved_negative_control': negative,
                  'diagnostics': {u: diagnostics[u] for u in sorted(wanted) if u in diagnostics}}
        result['status'] = 'PASS' if not missing and not any(result['diagnostics'].values()) else 'REVIEW'
        (O / 'toolkit-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), 'utf-8')
        print(json.dumps({'status': result['status'], 'files': len(files),
                          'diagnostics': sum(map(len, result['diagnostics'].values())), 'missing': missing}, ensure_ascii=False))
    finally:
        (O / 'toolkit-protocol.json').write_text(json.dumps(messages, ensure_ascii=False, indent=2), 'utf-8')
        p.terminate(); p.wait(timeout=10); err.close()

if __name__ == '__main__':
    main()
