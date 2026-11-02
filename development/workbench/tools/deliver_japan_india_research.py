from qin_persia_context import W, M, S, man, sha, read, dump
from pathlib import Path
import subprocess, shutil, json
from datetime import datetime, timezone

repo = W / 'projects/nesnd-repository'
R = W / 'reports/india-research-20261102'
J = W / 'reports/japan-research-20261102'
B = W / 'backups/pre-change-japan-india-research-20261102T161938Z/mod'
parent = '717c901195aa683a68a88409e1b6acb464e64f06'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode().strip() == parent
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo).strip()
before, after = man(B), man(M)
assert len(before) == 668 and len(after) == 670
assert not set(before) - set(after)
changes = sorted(rel for rel in after if before.get(rel) != after[rel])
assert set(changes) == {
    '.scratch/debug-release/map.md', '.scratch/japan-development/map.md',
    '.scratch/india-development/map.md', '.scratch/debug-release/issues/19-japan-india-research.md'
}
for rel in before:
    assert sha(repo / rel) == before[rel], rel

def cp(a, b):
    b.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(a, b)

for rel in changes:
    if rel not in before:
        assert not (repo / rel).exists(), rel
    cp(M / rel, repo / rel)

dump(R / 'docs-delivery.json', {
    'parent_commit': parent, 'main': str(M), 'prechange_backup': str(B),
    'files': len(after), 'main_changes': [
        {'path': rel, 'before': before.get(rel), 'after': after[rel]} for rel in changes
    ], 'deletions': [], 'gameplay_changed': False, 'game_launched': False,
    'scope': 'Research and unimplemented proposals only; no new gameplay package.'
})
support = {}
for root in [R, J / 'revision-2']:
    for p in root.rglob('*'):
        if p.is_file() and p.suffix in {'.md', '.json', '.txt', '.py'} and '__pycache__' not in p.parts:
            support['workbench/' + p.relative_to(W).as_posix()] = p
for name in ['current-mod-japan.md', 'japan-canon.md']:
    support['workbench/reports/' + J.name + '/' + name] = J / name
for name in ['document_japan_revision2.py', 'save_japan_india_research.py', 'deliver_japan_india_research.py']:
    support['workbench/tools/' + name] = W / 'tools' / name
for name in ['20261102-japan-development-design.md', '20261102-india-development-design.md', '00-master-plan.md']:
    support['workbench/plans/two-empires/' + name] = W / 'plans/two-empires' / name
for rel in ['references/active-work.md', 'references/narrative-context.md']:
    support['nesnd-skill/' + rel] = S / rel
for rel, source in support.items():
    cp(source, repo / 'development' / rel)
    assert sha(source) == sha(repo / 'development' / rel)
f = repo / 'development/snapshot-manifest.json'
d = json.loads(read(f))
records = {item['path']: item for item in d['files']}
for rel, p in support.items():
    records[rel] = {'path': rel, 'source': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
d.update(files=[records[k] for k in sorted(records)], updated_utc=datetime.now(timezone.utc).isoformat(),
         refresh_scope='Japan revision 2 and India native/MOD/canon research; proposals only, no gameplay change or game launch.')
dump(f, d)
assert man(M) == after
print(json.dumps({'main_task_markdown': len(changes), 'main_files': len(after),
                  'archived_support_files': len(support), 'gameplay_changed': False}))
