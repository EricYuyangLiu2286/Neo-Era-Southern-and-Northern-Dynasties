from pathlib import Path
import hashlib,json,shutil,subprocess,zipfile
from datetime import datetime,timezone
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';C=W/'exports/south-war-collapse-20261101-a';B=W/'backups/pre-change-south-plan-map-20261101T213214Z/mod';G=W/'projects/nesnd-repository';R=W/'reports/south-war-collapse-20261101';S=Path(r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def man(p):return {f.relative_to(p).as_posix():sha(f) for f in p.rglob('*') if f.is_file()}
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
before=man(B);assert man(M)==before,'Main changed since independent pre-change backup'
assert subprocess.check_output(['git','status','--porcelain'],cwd=G).strip()==b''
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=G).decode().strip()=='862319174ba2ff6eca0e324e4c3ad625fe7d1f29'
assert subprocess.check_output(['git','branch','--show-current'],cwd=G).strip()==b'main'
assert json.loads((R/'green.json').read_text('utf-8'))['validation']=='STATIC_PASS'
assert not json.loads((R/'tiger-delta.json').read_text('utf-8'))['added']
assert json.loads((R/'mcp-queries.json').read_text('utf-8'))['status']=='PASS'
after=man(C);changes=[r for r in after if before.get(r)!=after[r]];assert not set(before)-set(after)
for rel in changes:
 if rel in before:assert (G/rel).exists() and sha(G/rel)==before[rel],('Git conflict',rel)
 else:assert not (G/rel).exists(),('Git add conflict',rel)
for rel in changes:cp(C/rel,M/rel);cp(C/rel,G/rel)
assert man(M)==after
dump(R/'main-merge.json',{'source':str(C),'target':str(M),'changes':[dict(file=r,before=before.get(r),after=after[r]) for r in changes],'deletions':[],'conflicts':[],'main_equals_candidate':True,'game_launched':False})
archive=W/'releases/nesnd-20261101-war-collapse.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(after):
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):excluded.append(rel);continue
  assert not any(x in rel for x in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa']);z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
 for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'excluded':excluded,'QA_included':False})
# Selected project-owned sources and evidence only; keep vanilla files, binaries and runtime archives out.
support={}
for rel in ['references/active-work.md','references/log-first-delivery.md','references/syntax-and-routing.md']:
 support['nesnd-skill/'+rel]=S/rel
for p in R.iterdir():
 if p.is_file() and p.suffix in {'.md','.json','.diff'} and p.name!='tiger-raw.json':support['workbench/reports/south-war-collapse-20261101/'+p.name]=p
for name in ['calibration-v2.json','membership-inventory.json','map-candidate-superseded.json','gansu-lake-audit.json']:
 support['workbench/reports/south-allegiance-plan-20261101/'+name]=W/'reports/south-allegiance-plan-20261101'/name
for name in ['check_south_war_20261101.py','validate_south_war_20261101.py','calibrate_south_allegiance_v2_20261101.py','deliver_south_war_20261101.py']:
 support['workbench/tools/'+name]=W/'tools'/name
p=W/'plans/two-empires/20261101-southern-allegiances-envoys-plan.md';support['workbench/plans/two-empires/'+p.name]=p
for rel,p in support.items():cp(p,G/'development'/rel)
manifest=G/'development/snapshot-manifest.json';data=json.loads(manifest.read_text('utf-8-sig'));existing={x['path']:x for x in data['files']}
for rel,p in support.items():existing[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
data['files']=[existing[k] for k in sorted(existing)];data['updated_utc']=datetime.now(timezone.utc).isoformat();dump(manifest,data)
print(json.dumps({'main_changed_files':len(changes),'candidate_equals_main':True,'release':str(archive),'support_files':len(support),'game_launched':False}))
