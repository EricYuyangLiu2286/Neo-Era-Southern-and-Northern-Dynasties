"""Merge reviewed maintenance into main, preserving exact checked gameplay bytes."""
from pathlib import Path
import json,hashlib,shutil,subprocess,zipfile
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';C=W/'exports/maintenance-current';R=W/'reports/branch-naming-cleanup-20261104';REPO=W/'projects/nesnd-repository';S=Path(r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return p.read_text(encoding='utf-8-sig')
def man(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
def dump(name,value):(R/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO,text=True,encoding='utf-8').strip()
base=json.loads(read(R/'baseline-manifest.json'));current=man(M);cm=man(C);frozen=json.loads(read(R/'candidate-freeze.json'))['files']
assert current==base,'Concurrent main edit requires a three-way merge'
assert git('rev-parse','HEAD')==json.loads(read(R/'local-author-baseline.json'))['commit']
assert git('branch','--show-current')=='main' and not git('status','--porcelain')
doc_delta={p for p in set(cm)|set(frozen) if cm.get(p)!=frozen.get(p)}
assert all(p.startswith(('docs/','.scratch/')) for p in doc_delta),doc_delta
check=json.loads(read(R/'sol-independent-results.json'));layer=json.loads(read(R/'sol-layered-database-review.json'))
assert check['root_gate']['status']=='STATIC_PASS' and layer['gate']['status']=='STATIC_PASS'
assert not json.loads(read(R/'sol-tiger-delta.json'))['added']
assert check['source_hashes']['candidate_manifest_sha256']==sha(R/'candidate-freeze.json')
for rel,h in base.items():assert sha(REPO/rel)==h,rel
changed={p:h for p,h in cm.items() if base.get(p)!=h};deleted=sorted(base.keys()-cm.keys())
for root in (M,REPO):
    for rel in deleted:
        p=(root/rel).resolve();assert p.is_relative_to(root.resolve()) and sha(p)==base[rel];p.unlink()
    for rel,h in changed.items():
        p=(root/rel).resolve();assert p.is_relative_to(root.resolve());p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/rel,p);assert sha(p)==h
assert man(M)==cm
dump('main-merge.json',{'status':'DEPLOYED_STATIC_PASS','engine_verified':False,'main_source':cm,'changed':changed,'deleted_old_paths':deleted,'documentation_only_delta':sorted(doc_delta),'baseline_commit':git('rev-parse','HEAD'),'checked_freeze_sha':sha(R/'candidate-freeze.json')})
package=W/'releases/nesnd-maintenance-20261104.zip';assert not package.exists()
with zipfile.ZipFile(package,'x',zipfile.ZIP_DEFLATED) as z:
    for rel in cm:
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.py','.bak','.pyc')):continue
        assert not any(x in rel for x in ('nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa')),rel
        z.write(M/rel,rel)
with zipfile.ZipFile(package) as z:
    for rel in z.namelist():assert hashlib.sha256(z.read(rel)).hexdigest()==cm[rel]
dump('package.json',{'path':str(package),'sha256':sha(package),'files':len(z.namelist()),'QA_included':False,'engine_verified':False})
for source,target in [(S,REPO/'development/nesnd-skill'),(S.parent/'nesnd-player-writing',REPO/'development/nesnd-player-writing')]:
    for p in source.rglob('*'):
        if p.is_file() and p.suffix in ('.md','.yaml','.py'):
            dest=target/p.relative_to(source);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
for p in R.rglob('*'):
    if p.is_file() and p.suffix in ('.md','.json','.py','.patch') and p.stat().st_size<3_000_000:
        target=REPO/'development/workbench/reports'/R.name/p.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ('cleanup_obsolete_workspace.ps1','approve_maintenance_text.py','normalize_mod_localization.py','repair_maintenance_review.py','deliver_maintenance.py'):
    shutil.copy2(W/'tools'/name,REPO/'development/workbench/tools'/name)
subprocess.run(['git','add','--all'],cwd=REPO,check=True)
dump('precommit.json',{'source_files':len(cm),'changed':len(changed),'old_paths_removed':len(deleted),'package':str(package),'engine_verified':False})
print(json.dumps({'deployed':True,'source_files':len(cm),'changed':len(changed),'old_paths_removed':len(deleted),'commit_pending':True}))
