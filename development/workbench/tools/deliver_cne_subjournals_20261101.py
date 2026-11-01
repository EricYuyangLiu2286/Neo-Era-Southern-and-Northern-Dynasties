from pathlib import Path
import hashlib,json,shutil,subprocess,zipfile
from datetime import datetime,timezone
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';C=W/'exports/cne-reform-subjournals-20261101-a';B=W/'backups/pre-change-cne-reform-subjournals-20261101T222906Z/mod';G=W/'projects/nesnd-repository';R=W/'reports/cne-reform-subjournals-20261101';S=Path(r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def man(p):return {f.relative_to(p).as_posix():sha(f) for f in p.rglob('*') if f.is_file()}
def dump(p,x):p.write_bytes(json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'))
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
before=man(B);assert man(M)==before,'Main changed after independent backup; merge rather than overwrite'
assert subprocess.check_output(['git','status','--porcelain'],cwd=G).strip()==b''
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=G).decode().strip()=='47adfc05be87acb2ed255fe57404dceecb9eacbe'
assert subprocess.check_output(['git','branch','--show-current'],cwd=G).strip()==b'main'
assert json.loads((R/'green.json').read_text('utf-8'))['validation']=='STATIC_PASS'
assert not json.loads((R/'tiger-delta.json').read_text('utf-8'))['added']
assert json.loads((R/'mcp-queries.json').read_text('utf-8'))['status']=='PASS'
assert all(json.loads((R/'preservation.json').read_text('utf-8'))['checks'].values())
after=man(C);changed=[r for r in after if before.get(r)!=after[r]];assert not set(before)-set(after)
for rel in changed:
 if rel in before:assert (G/rel).exists() and sha(G/rel)==before[rel],('Git conflict',rel)
 else:assert not (G/rel).exists(),('Git add conflict',rel)
for rel in changed:cp(C/rel,M/rel);cp(C/rel,G/rel)
assert man(M)==after
dump(R/'main-merge.json',{'source':str(C),'target':str(M),'changes':[dict(file=r,before=before.get(r),after=after[r]) for r in changed],'deletions':[],'conflicts':[],'main_equals_candidate':True,'game_launched':False})
archive=W/'releases/nesnd-20261101-cne-subjournals.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(after):
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
  assert not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa']);z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
 for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'excluded':excluded,'QA_included':False})
support={}
for rel in ['references/active-work.md','references/journal-text-contract.md','references/syntax-and-routing.md']:support['nesnd-skill/'+rel]=S/rel
for p in R.iterdir():
 if p.is_file() and p.suffix in {'.md','.json','.diff'} and p.name!='tiger-raw.json':support['workbench/reports/cne-reform-subjournals-20261101/'+p.name]=p
for name in ['check_cne_subjournals_20261101.py','validate_cne_subjournals_20261101.py','deliver_cne_subjournals_20261101.py']:support['workbench/tools/'+name]=W/'tools'/name
for name in ['00-master-plan.md','20261101-cne-land-subjournals.md']:support['workbench/plans/two-empires/'+name]=W/'plans/two-empires'/name
for rel,p in support.items():cp(p,G/'development'/rel)
mf=G/'development/snapshot-manifest.json';data=json.loads(mf.read_text('utf-8-sig'));records={x['path']:x for x in data['files']}
for rel,p in support.items():records[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
data['files']=[records[k] for k in sorted(records)];data['updated_utc']=datetime.now(timezone.utc).isoformat();data['refresh_scope']='CNE land-reform subjournals, state projects, target-confirmation events, coup failure lifecycle, source-only checks; no game launch.';dump(mf,data)
print(json.dumps({'changed_main_files':len(changed),'verified_main_files':len(after),'main_equals_candidate':True,'release':str(archive),'game_launched':False}))
