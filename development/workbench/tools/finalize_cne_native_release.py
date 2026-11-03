from cne_native_context import *
import subprocess,zipfile,hashlib
repo=W/'projects/nesnd-repository'
backup=W/'backups/candidate-cne-time-native-ban-final-20261103T134027Z/mod'
cm,mm,bm=man(C),man(M),man(B)
assert man(backup)==cm
merge=json.loads(read(R/'main-merge.json'))
assert mm==merge['main'],'Main changed since staged merge'
for rel,h in mm.items():assert sha(repo/rel)==h
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==PARENT
tests=json.loads(read(R/'regression-candidate.json'));tr=json.loads(read(R/'tiger-candidate-run.json'));patch=json.loads(read(R/'patch-files.json'))
assert tests['status']=='PASS' and not json.loads(read(R/'tiger-added.json'))
for rel,h in patch.items():assert cm[rel]==h==tests['source_files'][rel]==tr['source_files'][rel]
for q in json.loads(read(R/'mcp-final.json'))['queries']:assert sha(C/q['query']['file_path'])==q['sha256']
for rel,h in cm.items():
    if mm.get(rel)!=h:
        assert rel in patch,'Unexpected post-merge change'
        shutil.copy2(C/rel,M/rel);shutil.copy2(C/rel,repo/rel)
assert man(M)==cm
merge['main']=cm;merge['changed']={r:h for r,h in cm.items() if bm.get(r)!=h};dump(R/'main-merge.json',merge)
dump(R/'candidate-backup.json',{'path':str(backup),'verified_files':len(cm),'engine_verified':False})
p=R/'review.md';s=read(p).replace('清理新复制原版文件的行尾空白','清理新复制原版文件的行尾及空格接Tab缩进');write(p,s)
z=W/'releases/nesnd-20261103-cne-time-native-ban-final.zip';assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for rel in cm:
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):continue
        assert not any(t in rel for t in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
        f.write(M/rel,rel)
with zipfile.ZipFile(z) as f:
    for rel in f.namelist():assert hashlib.sha256(f.read(rel)).hexdigest()==cm[rel]
dump(R/'package.json',{'path':str(z),'sha256':sha(z),'all_files_match_main':True,'QA_included':False})
for p in R.iterdir():
    if p.is_file() and p.suffix in ['.md','.json','.diff'] and p.name not in ['tiger-control.json','tiger-candidate.json'] and p.stat().st_size<3000000:
        q=repo/'development/workbench/reports/cne-time-native-ban-20261103'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for name in ['build_cne_time_native_ban.py','test_cne_time_native_ban.py','format_cne_native_release.py','finalize_cne_native_release.py']:
    shutil.copy2(W/'tools'/name,repo/'development/workbench/tools'/name)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
q=subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,capture_output=True,text=True,encoding='utf8')
dump(R/'git-whitespace.json',{'status':q.returncode,'output':q.stdout+q.stderr});assert q.returncode==0,q.stdout
shutil.copy2(R/'git-whitespace.json',repo/'development/workbench/reports/cne-time-native-ban-20261103/git-whitespace.json')
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Escalate prolonged CNE reform costs and disable isolated native error chains'],cwd=repo,check=True)
print('Verified 801 main/candidate/backup files; final package excludes development tools')
