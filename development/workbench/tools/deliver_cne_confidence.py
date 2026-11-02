from cne_confidence_context import *
import subprocess,zipfile
from datetime import datetime,timezone
repo=W/'projects/nesnd-repository';before=manifest(B);after=manifest(C)
assert manifest(M)==before,'Main changed after backup: perform a three-way merge.'
assert subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()==b''
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()=='bbe7ebe0fec2067da13022a74aef49ed4dcc4be6'
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo).strip()==b'main'
assert json.loads(read(R/'checks.json'))['status']=='STATIC_PASS'
assert json.loads(read(R/'legacy-green.json'))['validation']=='STATIC_PASS'
assert not json.loads(read(R/'tiger-delta.json'))['added']
assert json.loads(read(R/'mcp-queries.json'))['status']=='PASS'
assert not set(before)-set(after)
changes=[r for r in after if before.get(r)!=after[r]]
for rel in changes:
 q=repo/rel
 if rel in before:assert q.exists() and sha(q)==before[rel],('Git conflict',rel)
 else:assert not q.exists(),('Git add conflict',rel)
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
for rel in changes:cp(C/rel,M/rel);cp(C/rel,repo/rel)
assert manifest(M)==after
dump(R/'main-merge.json',{'candidate':str(C),'main':str(M),'parent_commit':'bbe7ebe0fec2067da13022a74aef49ed4dcc4be6','changed':[{'file':r,'before':before.get(r),'after':after[r]} for r in changes],'deletions':[],'conflicts':[],'main_files_equal_candidate':len(after),'engine_verified':False,'game_launched':False})
archive=W/'releases/nesnd-20261102-cne-confidence.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(after):
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
  assert not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
  z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
 for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'excluded':excluded,'QA_included':False})
support={}
for rel in ['SKILL.md','references/active-work.md','references/journal-text-contract.md','references/author-prose-profile.md']:support['nesnd-skill/'+rel]=S/rel
for q in R.iterdir():
 if q.is_file() and q.suffix in {'.md','.json','.diff'} and q.name not in ['tiger-raw.json','baseline.json']:support['workbench/reports/cne-confidence-20261101/'+q.name]=q
for name in ['cne_confidence_context.py','check_cne_activation.py','check_cne_confidence_legacy.py','validate_cne_confidence.py','deliver_cne_confidence.py']:support['workbench/tools/'+name]=W/'tools'/name
support['workbench/plans/two-empires/20261101-cne-confidence.md']=W/'plans/two-empires/20261101-cne-confidence.md'
for rel,q in support.items():cp(q,repo/'development'/rel)
mf=repo/'development/snapshot-manifest.json';data=json.loads(read(mf));records={x['path']:x for x in data['files']}
for rel,q in support.items():records[rel]={'path':rel,'source':str(q),'sha256':sha(q),'bytes':q.stat().st_size}
data['files']=[records[k] for k in sorted(records)];data['updated_utc']=datetime.now(timezone.utc).isoformat();data['refresh_scope']='CNE confidence, child-JE activation, native progress breakdowns, republican campaign, estate ownership teardown and player-facing prose; external source validation only.';dump(mf,data)
print(json.dumps({'main_changed_files':len(changes),'main_verified_files':len(after),'package':str(archive),'game_launched':False}))
