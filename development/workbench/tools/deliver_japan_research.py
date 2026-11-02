from qin_stage_context import *
import subprocess,zipfile
from datetime import datetime,timezone
repo=W/'projects/nesnd-repository';parent='a7b445ba515d0e4842fb36ba3e6094d54e046012'
before,after=man(B),man(C)
assert man(M)==before
assert man(W/'backups/candidate-qin-journal-stages-final-20261102T135757Z/mod')==after
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==parent
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
changes=sorted(r for r in after if before.get(r)!=after[r]);assert not set(before)-set(after)
assert len([r for r in changes if r.endswith('.txt')])==5
checks=json.loads(read(R/'qin-stage-checks.json'));assert checks['status']=='STATIC_PASS'
original_manifest=json.loads(read(R/'qin-stage-source-manifest.json'))['after']
for rel in checks['changed_scripts']:assert after[rel]==original_manifest[rel]
assert not json.loads(read(R/'qin-stage-tiger-delta.json'))['added']
assert json.loads(read(R/'qin-stage-mcp.json'))['status']=='PASS'
for rel in changes:
 if rel in before:assert sha(repo/rel)==before[rel],rel
 else:assert not (repo/rel).exists(),rel
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
for rel in changes:cp(C/rel,M/rel);cp(C/rel,repo/rel)
assert man(M)==after
dump(R/'main-merge.json',{'parent_commit':parent,'main':str(M),'candidate':str(C),'prechange_backup':str(B),'candidate_backup':str(W/'backups/candidate-qin-journal-stages-final-20261102T135757Z/mod'),'files':len(after),'changed':[{'file':r,'before':before.get(r),'after':after[r]} for r in changes],'deletions':[],'conflicts':[],'Japan_gameplay_changed':False,'engine_verified':False,'game_launched':False})
archive=W/'releases/nesnd-20261102-qin-journal-stages.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(after):
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.py','.pyc','.bak')):excluded.append(rel);continue
  assert not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
  z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
 for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'files':len(after)-len(excluded),'excluded':excluded,'QA_included':False})
support={}
for p in R.rglob('*'):
 if p.is_file() and p.suffix in {'.md','.json','.txt','.py','.png'} and p.name!='qin-stage-tiger.json':
  support['workbench/reports/'+R.name+'/'+p.relative_to(R).as_posix()]=p
for name in ['qin_stage_context.py','stage_qin_journals.py','validate_qin_stages.py','probe_qin_stages.py','document_japan_research.py','deliver_japan_research.py']:
 support['workbench/tools/'+name]=W/'tools'/name
for name in ['20261102-japan-development-design.md','07-japan.md','20261102-qin-persia-implementation.md','00-master-plan.md']:
 support['workbench/plans/two-empires/'+name]=W/'plans/two-empires'/name
for rel in ['SKILL.md','references/active-work.md','references/journal-text-contract.md','references/narrative-context.md']:
 support['nesnd-skill/'+rel]=S/rel
for rel,p in support.items():cp(p,repo/'development'/rel)
f=repo/'development/snapshot-manifest.json';d=json.loads(read(f));records={x['path']:x for x in d['files']}
for rel,p in support.items():records[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
d.update(files=[records[k] for k in sorted(records)],updated_utc=datetime.now(timezone.utc).isoformat(),refresh_scope='Japan native/MOD/canon research and unimplemented three-scenario proposal; five-script Qin later-journal gating with legacy-save preservation; engine not run.')
dump(f,d)
print(json.dumps({'main_files':len(after),'changed':len(changes),'gameplay_scripts':5,'support_files':len(support),'Japan_gameplay_changed':False,'package':str(archive)}))
