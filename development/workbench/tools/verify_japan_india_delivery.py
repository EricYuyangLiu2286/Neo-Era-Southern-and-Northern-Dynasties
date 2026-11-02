from qin_persia_context import W, M, man, sha, read, dump
import subprocess, json, hashlib, shutil
from datetime import datetime, timezone

repo = W / 'projects/nesnd-repository'
R = W / 'reports/india-research-20261102'
B = W / 'backups/pre-change-japan-india-research-20261102T161938Z/mod'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo).decode().strip()
head = git('rev-parse', 'HEAD')
assert head.startswith('cb2fc02')
assert git('ls-remote', 'origin', 'refs/heads/main').split()[0] == head
assert not git('status', '--porcelain')
main = man(M)
baseline = man(B)
changed = sorted(p for p in main if baseline.get(p) != main[p])
assert changed == sorted(json.loads(read(R / 'gameplay-unchanged.json'))['only_main_changes'])
assert not set(baseline) - set(main)
assert all(p.startswith('.scratch/') and p.endswith('.md') for p in changed)
manifest = json.loads(read(repo / 'development/snapshot-manifest.json'))
archive = {r['path']: r for r in manifest['files']}
paths = dict(main)
source_checks = 0
for rel in git('diff', '--name-only', '717c901', head).splitlines():
    if rel.startswith('development/'):
        paths[rel] = sha(repo / rel)
        item = archive.get(rel.removeprefix('development/'))
        if item:
            assert sha(__import__('pathlib').Path(item['source'])) == item['sha256'] == paths[rel], rel
            source_checks += 1
proc = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=repo,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for rel, digest in paths.items():
    proc.stdin.write((head + ':' + rel + '\n').encode())
    proc.stdin.flush()
    header = proc.stdout.readline().decode().split()
    assert len(header) == 3 and header[1] == 'blob', (rel, header)
    remaining = int(header[2])
    h = hashlib.sha256()
    while remaining:
        data = proc.stdout.read(min(remaining, 1048576))
        assert data
        h.update(data)
        remaining -= len(data)
    assert proc.stdout.read(1) == b'\n'
    assert h.hexdigest() == digest, rel
proc.stdin.close()
assert proc.wait() == 0
report = {
    'content_commit': head, 'remote_main_matches_content_commit': True,
    'verified_utc': datetime.now(timezone.utc).isoformat(),
    'main_files_verified_against_git_blobs': len(main),
    'archive_source_hash_checks': source_checks, 'git_blobs_verified': len(paths),
    'gameplay_changed': False, 'game_launched': False,
    'only_main_changes': changed, 'deletions': [],
    'delivery_note': 'This ledger is stored in the following documentation commit; it verifies the content commit, not its own future hash.'
}
dump(R / 'git-delivery.json', report)
for p in [R / 'git-delivery.json', W / 'tools/verify_japan_india_delivery.py']:
    rel = 'workbench/' + p.relative_to(W).as_posix()
    target = repo / 'development' / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, target)
    archive[rel] = {'path': rel, 'source': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
manifest.update(files=[archive[k] for k in sorted(archive)], updated_utc=datetime.now(timezone.utc).isoformat())
dump(repo / 'development/snapshot-manifest.json', manifest)
print(json.dumps(report, ensure_ascii=False))
