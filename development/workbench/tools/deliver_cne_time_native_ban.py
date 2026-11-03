from cne_native_context import *
import subprocess,zipfile,hashlib

repo=W/'projects/nesnd-repository'
backup=W/'backups/candidate-cne-time-native-ban-20261103T133514Z/mod'
bm,cm,mm=man(B),man(C),man(M)
assert not bm.keys()-cm.keys(),'Candidate deleted baseline files'
assert man(backup)==cm,'Candidate backup mismatch'
changes={p:h for p,h in cm.items() if bm.get(p)!=h}
user={p:h for p,h in mm.items() if bm.get(p)!=h}
assert len(changes)==14
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==PARENT
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()=='fix/cne-time-native-ban-20261103'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
for rel,h in bm.items():assert sha(repo/rel)==h,('Repo parent conflict',rel)
for rel,h in changes.items():assert mm.get(rel) in [bm.get(rel),h],('Main conflict',rel)
tests=json.loads(read(R/'regression-candidate.json'));tr=json.loads(read(R/'tiger-candidate-run.json'))
assert tests['status']=='PASS' and not json.loads(read(R/'tiger-added.json'))
assert json.loads(read(R/'mcp-final.json'))['status']=='PASS'
assert json.loads(read(R/'graph-audit-comparison.json'))['status']=='PASS'
patch=json.loads(read(R/'patch-files.json'))
for rel,h in patch.items():assert cm[rel]==h==tests['source_files'][rel]==tr['source_files'][rel]
for rel,h in json.loads(read(R/'native-source-hashes.json')).items():assert sha(G/rel)==h,('Native source changed',rel)
for q in json.loads(read(R/'mcp-final.json'))['queries']:assert sha(C/q['query']['file_path'])==q['sha256']
for rel in changes:
    p=M/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/rel,p)
for rel,h in user.items():assert sha(M/rel)==h,('User edit not preserved',rel)
merged=man(M)
dump(R/'main-merge.json',{'parent':PARENT,'source':str(C),'changed':changes,'preserved_user_edits':user,'conflicts':[],'deletions':[],'main':merged,'engine_verified':False})
dump(R/'candidate-backup.json',{'path':str(backup),'verified_files':len(cm),'engine_verified':False})
for rel,h in merged.items():
    if not (repo/rel).exists() or sha(repo/rel)!=h:
        p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(M/rel,p)
for rel in ['references/syntax-and-routing.md','references/active-work.md','references/system-design-and-plans.md']:
    p=repo/'development/nesnd-skill'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,p)
z=W/'releases/nesnd-20261103-cne-time-native-ban.zip';assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for rel in merged:
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):continue
        assert not any(t in rel for t in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
        f.write(M/rel,rel)
with zipfile.ZipFile(z) as f:
    for rel in f.namelist():assert hashlib.sha256(f.read(rel)).hexdigest()==merged[rel]
dump(R/'package.json',{'path':str(z),'sha256':sha(z),'all_files_match_main':True,'QA_included':False})
for p in R.iterdir():
    if p.is_file() and p.suffix in ['.md','.json','.diff'] and p.name not in ['tiger-control.json','tiger-candidate.json'] and p.stat().st_size<3000000:
        q=repo/'development/workbench/reports/cne-time-native-ban-20261103'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for name in ['cne_native_context.py','build_cne_time_native_ban.py','test_cne_time_native_ban.py','validate_cne_native_tools.py','finish_cne_native_documents.py','prepare_cne_native_release.py','deliver_cne_time_native_ban.py']:
    p=repo/'development/workbench/tools'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/'tools'/name,p)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
q=subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,capture_output=True,text=True,encoding='utf8')
dump(R/'git-whitespace.json',{'status':q.returncode,'output':q.stdout+q.stderr});assert q.returncode==0,q.stdout
shutil.copy2(R/'git-whitespace.json',repo/'development/workbench/reports/cne-time-native-ban-20261103/git-whitespace.json')
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Escalate prolonged CNE reform costs and disable isolated native error chains'],cwd=repo,check=True)
print('Merged',len(changes),'files; main equals candidate:',merged==cm)
