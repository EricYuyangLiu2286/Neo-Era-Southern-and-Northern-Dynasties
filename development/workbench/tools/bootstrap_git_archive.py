"""Import exact immutable MOD snapshots into Git without writing to source trees."""
from pathlib import Path
import hashlib
import json
import subprocess

WORK = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
REPO = WORK / 'projects/nesnd-repository'
SPECS = [
    ('pre-update-20261030T233944Z', 'archive/original-20261030', 'original-20261030', 'Archive original MOD snapshot from 2026-10-30 before development'),
    ('candidate-mattpocock-setup-20261101T001645Z', 'main', 'main-snapshot-20261101', 'Preserve current main MOD and engineering setup; not full engine acceptance'),
    ('candidate-batch-debug-f1-20261101T000328Z', 'candidate/f1', 'f1-frozen-20261101', 'Archive frozen F1 debug candidate; engine acceptance pending'),
]

def git(*args, source=None):
    cmd = ['git', '--git-dir', str(REPO / '.git'), '--work-tree', str(source or REPO), *args]
    r = subprocess.run(cmd, capture_output=True, check=True)
    return r.stdout.decode('utf-8', 'replace').strip()

def verify_snapshot(name):
    backup = WORK / 'backups' / name
    source = backup / 'mod'
    expected = json.loads((backup / 'manifest.json').read_text(encoding='utf-8-sig'))['sha256']
    actual = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in source.rglob('*') if p.is_file()}
    assert actual == expected, f'Snapshot drift: {name}'
    for p in source.rglob('*'):
        if p.is_file():
            assert p.stat().st_size < 100 * 1024 * 1024, f'Oversize GitHub file: {p}'
            assert p.name.lower() not in {'.env', 'id_rsa', 'id_ed25519'}, f'Credential-like file: {p}'
            assert p.suffix.lower() not in {'.pem', '.pfx', '.key'}, f'Credential-like file: {p}'
    return source, actual

def main():
    snapshots = [(spec, *verify_snapshot(spec[0])) for spec in SPECS]
    if REPO.exists():
        assert {p.name for p in REPO.iterdir()} == {'.git'}, f'Existing working files preserved: {REPO}'
        result = subprocess.run(['git', '-C', str(REPO), 'rev-parse', '--verify', 'HEAD'], capture_output=True)
        assert result.returncode != 0, 'Existing committed repository preserved'
    else:
        REPO.mkdir(parents=True)
        subprocess.run(['git', 'init', '--initial-branch=archive/original-20261030', str(REPO)], check=True, capture_output=True)
    git('config', 'core.autocrlf', 'false')
    git('config', 'core.safecrlf', 'false')
    git('config', 'core.quotePath', 'false')
    if 'origin' not in git('remote').splitlines():
        git('remote', 'add', 'origin', 'https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties.git')
    assert git('remote', 'get-url', 'origin') == 'https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties.git'
    records = []
    previous = None
    for (name, branch, tag, message), source, hashes in snapshots:
        if previous:
            git('branch', branch, previous)
        git('symbolic-ref', 'HEAD', 'refs/heads/' + branch)
        git('read-tree', '--empty')
        git('add', '--force', '--all', '--', '.', source=source)
        staged_paths = [p for p in git('ls-files', '-z', source=source).split('\0') if p]
        assert set(staged_paths) == set(hashes), f'Staging mismatch: {name}'
        git('commit', '-m', message, source=source)
        commit = git('rev-parse', 'HEAD')
        git('tag', '-a', tag, '-m', f'{message}\nSource snapshot: {name}\nFiles: {len(hashes)}\nThis tag preserves a snapshot; it does not certify gameplay.')
        records.append({'snapshot': name, 'branch': branch, 'tag': tag, 'commit': commit, 'files': len(hashes), 'source': str(source), 'engine_acceptance': False})
        previous = commit
    git('symbolic-ref', 'HEAD', 'refs/heads/main')
    git('read-tree', 'main')
    git('checkout-index', '--all')
    assert git('status', '--porcelain') == '', 'Unexpected initial worktree changes'
    report = {'repository': str(REPO), 'remote': 'https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties', 'pushed': False, 'snapshots': records}
    out = WORK / 'reports/git-bootstrap-20261101.json'
    with out.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
