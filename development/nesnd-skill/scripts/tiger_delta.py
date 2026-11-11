"""Run vic3-tiger on a pre-change backup and on the current MOD; list new reports in changed files.

python scripts/tiger_delta.py --before <WORK/backups/pre-change-.../mod> --out <report dir>
  --after   mod to check (default: main MOD)
  --config  tiger config (default: written to --out: english + simp_chinese, EACR loaded as dependency)
  --tiger   vic3-tiger.exe (default: WORK/tools/tiger-1.19.0/vic3-tiger.exe)
Writes tiger-before.json, tiger-after.json, tiger-delta.json. Tiger rules can lag behind the game;
check each new report against current GAME before acting.
Generalised from the per-report run_tiger.py and delta.py scripts (2026-11-07).
"""
import argparse, hashlib, json, subprocess
from collections import Counter
from pathlib import Path
from catalog import MOD, WORK, GAME, WORKSHOP

CONF = ('languages = { check = "english" check = "simp_chinese" }\n'
        'filter = { show_vanilla = no show_loaded_mods = no }\n'
        'load_mod = { label = "DEP0" mod = "%s" }\n') % str(WORKSHOP / '3704408897').replace('\\', '/')


def digests(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}


def run(tiger, conf, mod, out):
    with out.open('wb') as o, out.with_suffix('.stderr.txt').open('wb') as e:
        code = subprocess.run([str(tiger), '--game', str(GAME.parent), '--config', str(conf), '--json', str(mod)],
                              stdout=o, stderr=e).returncode
    return json.loads(out.read_text('utf-8') or '[]'), code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--before', type=Path, required=True)
    ap.add_argument('--after', type=Path, default=MOD)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--config', type=Path)
    ap.add_argument('--tiger', type=Path, default=WORK / 'tools/tiger-1.19.0/vic3-tiger.exe')
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    conf = a.config or a.out / 'tiger.conf'
    if not a.config:
        conf.write_text(CONF, 'utf-8')
    b, c = digests(a.before), digests(a.after)
    changed = {k for k in set(b) | set(c) if b.get(k) != c.get(k)}
    before, cb = run(a.tiger, conf, a.before, a.out / 'tiger-before.json')
    after, ca = run(a.tiger, conf, a.after, a.out / 'tiger-after.json')

    def key(it):
        return (it['severity'], it['key'], it['message'],
                tuple((z.get('path', '').replace('\\', '/'), (z.get('line') or '').strip()) for z in it['locations']))
    old = {key(x) for x in before}
    new = [x for x in after if key(x) not in old
           and any(z.get('path', '').replace('\\', '/') in changed for z in x['locations'])]
    (a.out / 'tiger-delta.json').write_text(json.dumps(new, ensure_ascii=False, indent=2), 'utf-8')
    print(json.dumps({'changed_files': len(changed), 'before': len(before), 'after': len(after),
                      'new_in_changed': len(new), 'by_key': Counter(x['key'] for x in new).most_common(10),
                      'exit': [cb, ca]}, ensure_ascii=False))
    for x in new[:40]:
        z = x['locations'][0]
        print(x['severity'], x['key'], z.get('path'), z.get('linenr'), x['message'][:160])


if __name__ == '__main__':
    main()
