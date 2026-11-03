from observer_logfix_context import *
import subprocess,zipfile,hashlib,difflib
repo=W/'projects/nesnd-repository'
bm,cm,mm=man(B),man(C),man(M)
assert cm==mm
backup=W/'backups/candidate-observer-logfix-final-20261103T111141Z/mod'
assert man(backup)==cm
for rel,h in mm.items():assert sha(repo/rel)==h
parent='adfc31759b355d33e0f09269822911b367499b53'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==parent
patch=json.loads(read(R/'patch-files.json'));tests=json.loads(read(R/'regression-candidate.json'));tr=json.loads(read(R/'tiger-candidate-run.json'))
for rel,h in patch.items():assert cm[rel]==h==tests['source_files'][rel]==tr['source_files'][rel]
assert tests['status']=='PASS' and not json.loads(read(R/'tiger-added.json'))
merge=json.loads(read(R/'main-merge.json'));merge['main']=mm;merge['changed']={r:h for r,h in cm.items() if bm.get(r)!=h};dump(R/'main-merge.json',merge)
dump(R/'candidate-backup.json',{'path':str(backup),'verified_files':len(cm),'engine_verified':False})
diff=''
for rel in patch:
    old=B/rel if (B/rel).exists() else G/rel
    diff+=''.join(difflib.unified_diff(read(old).splitlines(True),read(C/rel).splitlines(True),fromfile=str(old),tofile=str(C/rel)))
(R/'gameplay.diff').write_text(diff,encoding='utf-8')
dump(R/'final-validation.json',{'status':'STATIC_PASS','targeted_checks':len(tests['checks']),'mcp_queries':4,'tiger_added':0,'graph_identical':True,'standards_findings':0,'spec_findings':0,'code_files':patch,'engine_verified':False,'runtime_snapshot_unchanged':man(W/'exports/observer-20261103T100813Z/mod')==bm})
z=W/'releases/nesnd-20261103-observer-logfix-final.zip';assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for rel in mm:
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):continue
        assert not any(t in rel for t in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
        f.write(M/rel,rel)
with zipfile.ZipFile(z) as f:
    for rel in f.namelist():assert hashlib.sha256(f.read(rel)).hexdigest()==mm[rel]
dump(R/'package.json',{'path':str(z),'sha256':sha(z),'all_files_match_main':True,'QA_included':False})
for p in R.iterdir():
    if p.is_file() and p.suffix in ['.md','.json','.diff'] and not p.name.startswith(('tiger-baseline','tiger-candidate','audit-')) and p.stat().st_size<3000000:
        q=repo/'development/workbench/reports/observer-logfix-20261103'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for name in ['observer_logfix_context.py','fix_observer_log_errors.py','test_observer_log_errors.py','validate_observer_logfix.py','merge_observer_logfix.py','finalize_observer_logfix.py']:
    shutil.copy2(W/'tools'/name,repo/'development/workbench/tools'/name)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
q=subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,capture_output=True,text=True,encoding='utf8')
assert q.returncode==0,q.stdout
dump(R/'git-whitespace.json',{'status':0,'output':q.stdout+q.stderr});shutil.copy2(R/'git-whitespace.json',repo/'development/workbench/reports/observer-logfix-20261103/git-whitespace.json')
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Fix observer-run scope and parsing errors without changing journal refresh'],cwd=repo,check=True)
print('Main, candidate, backup and release verified')
