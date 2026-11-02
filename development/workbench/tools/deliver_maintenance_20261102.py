from maintenance_20261102_context import *
import subprocess,zipfile
from datetime import datetime,timezone
repo=W/'projects/nesnd-repository';before=man(B);after=man(C);parent='044de73e0e0fb516a4b8f36384d0d815a86802f7'
assert man(M)==before,'Main changed after backup; three-way merge required'
assert subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()==b''
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==parent
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo).strip()==b'main'
assert json.loads(read(R/'checks.json'))['status']=='STATIC_PASS'
assert not json.loads(read(R/'tiger-delta.json'))['added']
assert json.loads(read(R/'mcp-queries.json'))['status']=='PASS'
assert not set(before)-set(after)
changes=sorted(r for r in after if before.get(r)!=after[r])
for rel in changes:
 q=repo/rel
 if rel in before:assert q.exists() and sha(q)==before[rel],('Git conflict',rel)
 else:assert not q.exists(),('Git add conflict',rel)
# Validate only the intended country/treaty definitions changed in historical data.
def shape(n):return n.key,n.op,n.value,tuple(shape(a) for a in n.children or [])
for rel in ['common/history/diplomacy/ce_subject_relationships.txt','common/history/treaties/ce_historical_treaties.txt']:
 a,b=parse(read(B/rel)),parse(read(C/rel));different=[]
 for x,y in zip(a.children[0].children,b.children[0].children):
  if shape(x)!=shape(y):different.append({'old':x.key,'new':y.key})
 assert len(a.children[0].children)==len(b.children[0].children)
 assert len(different)==1,(rel,different)
 dump(R/('history-preservation-'+Path(rel).stem+'.json'),{'only_changed_parent':different,'other_AST_identical':True})
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
for rel in changes:cp(C/rel,M/rel);cp(C/rel,repo/rel)
assert man(M)==after
dump(R/'main-merge.json',{'candidate':str(C),'main':str(M),'parent_commit':parent,'changed':[{'file':r,'before':before.get(r),'after':after[r]} for r in changes],'deletions':[],'conflicts':[],'main_files_equal_candidate':len(after),'engine_verified':False,'game_launched':False})
archive=W/'releases/nesnd-20261102-ui-poland-tributary.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(after):
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
  assert not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
  z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
 for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'excluded':excluded,'QA_included':False})
support={}
for rel in ['SKILL.md','references/active-work.md','references/narrative-context.md','references/journal-text-contract.md','references/numeric-scale-contract.md']:support['nesnd-skill/'+rel]=S/rel
for q in (S.parent/'nesnd-player-writing').rglob('*'):
 if q.is_file():support['nesnd-player-writing/'+q.relative_to(S.parent/'nesnd-player-writing').as_posix()]=q
for directory in [R,W/'reports/rules-poland-qin-20261102',W/'reports/ui-trade-feedback-20261102']:
 for q in directory.iterdir():
  if q.is_file() and q.suffix in {'.md','.json','.diff'} and q.name not in {'tiger-raw.json','tiger-final.json','baseline.json','preexisting-main-japan-events.diff'}:support['workbench/reports/'+directory.name+'/'+q.name]=q
for name in ['maintenance_20261102_context.py','patch_cne_ui_20261102.py','patch_poland_20261102.py','patch_trade_persia_and_review_20261102.py','final_maintenance_guards.py','finish_maintenance_ui.py','close_trade_reply_window.py','update_maintenance_skills.py','document_maintenance_20261102.py','format_maintenance_changed.py','validate_maintenance_20261102.py','deliver_maintenance_20261102.py','audit_qin_cultures_20261102.py']:
 support['workbench/tools/'+name]=W/'tools'/name
support['workbench/plans/two-empires/20261102-western-qin-design.md']=W/'plans/two-empires/20261102-western-qin-design.md'
for rel,q in support.items():cp(q,repo/'development'/rel)
mf=repo/'development/snapshot-manifest.json';data=json.loads(read(mf));records={x['path']:x for x in data['files']}
for rel,q in support.items():records[rel]={'path':rel,'source':str(q),'sha256':sha(q),'bytes':q.stat().st_size}
data['files']=[records[k] for k in sorted(records)];data['updated_utc']=datetime.now(timezone.utc).isoformat();data['refresh_scope']='Native CNE conditions, Poland lifecycle fixes, supply scale/window, Persia tributary, original-rule audit, independent writing skill, Qin culture/story/structure plan; engine not run.';dump(mf,data)
print(json.dumps({'main_changed_files':len(changes),'main_verified_files':len(after),'package':str(archive),'support_files':len(support),'game_launched':False}))
