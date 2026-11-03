from observer_logfix_context import *
import subprocess,zipfile,hashlib
repo=W/'projects/nesnd-repository'
parent='adfc31759b355d33e0f09269822911b367499b53'
bm,cm,mm=man(B),man(C),man(M)
changes={p:h for p,h in cm.items() if bm.get(p)!=h}
user={p:h for p,h in mm.items() if bm.get(p)!=h}
assert not bm.keys()-cm.keys(), 'Candidate deletion'
assert json.loads(read(R/'regression-candidate.json'))['status']=='PASS'
assert json.loads(read(R/'mcp-final.json'))['status']=='PASS'
assert json.loads(read(R/'graph-audit-comparison.json'))['status']=='PASS'
assert not json.loads(read(R/'tiger-added.json'))
tests=json.loads(read(R/'regression-candidate.json'))['source_files']
tiger=json.loads(read(R/'tiger-candidate-run.json'))['source_files']
for rel,h in json.loads(read(R/'patch-files.json')).items():
    assert cm[rel]==h==tests[rel]==tiger[rel],('Test SHA changed',rel)
candidate_backup=W/'backups/candidate-observer-logfix-20261103T110657Z/mod'
assert man(candidate_backup)==cm,'Candidate backup mismatch'
dump(R/'candidate-backup.json',{'path':str(candidate_backup),'verified_files':len(cm),'engine_verified':False})
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==parent
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
for rel,h in bm.items():assert (repo/rel).exists() and sha(repo/rel)==h,('Repo parent conflict',rel)
for rel,h in changes.items():assert mm.get(rel) in [bm.get(rel),h],('Main conflict',rel)
for rel in changes:
    p=M/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/rel,p)
for rel,h in user.items():assert sha(M/rel)==h
merged=man(M)
dump(R/'main-merge.json',{'parent':parent,'source':str(C),'changed':changes,'preserved_user_edits':user,'conflicts':[],'deletions':[],'main':merged,'engine_verified':False})
for rel,h in merged.items():
    if not (repo/rel).exists() or sha(repo/rel)!=h:
        p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(M/rel,p)
for rel in ['references/syntax-and-routing.md','references/active-work.md']:
    p=repo/'development/nesnd-skill'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,p)
for p in R.iterdir():
    if p.is_file() and p.suffix in ['.md','.json','.diff'] and not p.name.startswith(('tiger-baseline','tiger-candidate','audit-')) and p.stat().st_size<3000000:
        q=repo/'development/workbench/reports/observer-logfix-20261103'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for name in ['observer_logfix_context.py','fix_observer_log_errors.py','test_observer_log_errors.py','validate_observer_logfix.py','merge_observer_logfix.py']:
    p=repo/'development/workbench/tools'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/'tools'/name,p)
z=W/'releases/nesnd-20261103-observer-logfix.zip';assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for rel in merged:
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):continue
        assert not any(t in rel for t in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
        f.write(M/rel,rel)
with zipfile.ZipFile(z) as f:
    for rel in f.namelist():assert hashlib.sha256(f.read(rel)).hexdigest()==merged[rel]
dump(R/'package.json',{'path':str(z),'sha256':sha(z),'all_files_match_main':True,'QA_included':False})
shutil.copy2(R/'package.json',repo/'development/workbench/reports/observer-logfix-20261103/package.json')
subprocess.run(['git','add','--all'],cwd=repo,check=True)
q=subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,capture_output=True,text=True,encoding='utf8')
dump(R/'git-whitespace.json',{'status':q.returncode,'output':q.stdout+q.stderr});assert q.returncode==0,q.stdout
subprocess.run(['git','commit','-m','Fix observer-run scope and parsing errors without changing journal refresh'],cwd=repo,check=True)
print('Merged',len(changes),'files; main equals candidate',merged==cm)
