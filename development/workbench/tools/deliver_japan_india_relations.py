from qin_persia_context import W, M, S, G, man, sha, read, dump
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess, shutil, re

R = W/'reports/japan-india-plan-revision-20261102'
B = W/'backups/pre-change-japan-india-plan-relations-20261102T165000Z/mod'
repo = W/'projects/nesnd-repository'
parent = 'd2a7f302322eef2bb868bb6c6e0625f55b2d55b5'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip() == parent
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
before, after = man(B), man(M)
changes = sorted(k for k in after if before.get(k) != after[k])
assert len(before) == 670 and len(after) == 671
assert not set(before)-set(after)
assert set(changes) == {'.scratch/debug-release/map.md','.scratch/japan-development/map.md','.scratch/india-development/map.md','.scratch/debug-release/issues/20-japan-india-relations-plan.md'}
for rel, digest in before.items():
    assert sha(repo/rel) == digest, rel

stable, expected = [], []
plans = [W/'plans/two-empires'/n for n in ['20261102-japan-development-design.md','20261102-india-development-design.md','20261102-japan-india-lifecycle.md']]
for f in R.glob('*sources.json'):
    sources = json.loads(read(f))['sources']
    entries = sources if isinstance(sources,list) else [dict(v,path=k) for k,v in sources.items()]
    for e in entries:
        p = Path(e['path'])
        current = sha(p)
        record = {'manifest':f.name,'path':str(p),'read_sha256':e['sha256'],'current_sha256':current}
        if current == e['sha256']:
            stable.append(record)
        else:
            assert p in plans, str(p)
            expected.append(record)
link_count = 0
for p in [*plans,*R.glob('*.md')]:
    for link in re.findall(r'\]\(<([^>]+)>\)',read(p)):
        if not re.match(r'^[A-Za-z]:[/\\]',link):
            continue
        target = Path(re.sub(r':\d+$','',link.split('#')[0]))
        assert target.exists(), (str(p),str(target))
        link_count += 1
dump(R/'source-and-scope-verification.json',{
    'baseline':parent,'backup':str(B),'game_version':'1.13.11','build':24799966,
    'unchanged_source_records':stable,'expected_revised_plan_records':expected,
    'root_sources':[{'path':str(p),'sha256':sha(p)} for p in [G/'common/journal_entries/journal_entries.md',M/'common/journal_entries/ce_cne_land_draft.txt',M/'common/journal_entries/nesnd_cne_programs.txt',M/'common/journal_entries/nesnd_japan.txt']],
    'main_files':len(after),'main_changes':[{'path':p,'before':before.get(p),'after':after[p]} for p in changes],
    'absolute_links_resolved':link_count,'gameplay_changed':False,'game_launched':False,
    'scenario_table':'24 design scenarios; not executed engine tests'})

def cp(a,b):
    b.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(a,b)
for rel in changes:
    if rel not in before:
        assert not (repo/rel).exists()
    cp(M/rel,repo/rel)
support = {}
for p in R.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.json','.py'} and '__pycache__' not in p.parts:
        support['workbench/'+p.relative_to(W).as_posix()] = p
for p in [*plans,W/'plans/two-empires/00-master-plan.md',W/'tools/document_japan_india_relations.py',Path(__file__)]:
    support['workbench/'+p.relative_to(W).as_posix()] = p
for name in ['active-work.md','narrative-context.md']:
    support['nesnd-skill/references/'+name] = S/'references'/name
manifest_path = repo/'development/snapshot-manifest.json'
manifest = json.loads(read(manifest_path))
records = {x['path']:x for x in manifest['files']}
for rel,p in support.items():
    cp(p,repo/'development'/rel)
    assert sha(repo/'development'/rel) == sha(p)
    records[rel] = {'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
manifest.update(files=[records[k] for k in sorted(records)],updated_utc=datetime.now(timezone.utc).isoformat(),
    refresh_scope='Japan revision 3, India revision 2, policy/source research and 24 planned lifecycle scenarios; documentation only.')
dump(manifest_path,manifest)
assert man(M) == after
print(json.dumps({'stable_source_records':len(stable),'expected_plan_changes':len(expected),'links':link_count,'support_files':len(support),'main_markdown_changes':changes,'gameplay_changed':False}))
