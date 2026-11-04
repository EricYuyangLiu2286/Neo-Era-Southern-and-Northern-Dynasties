from journal_war_context import *
import subprocess,zipfile,hashlib
repo=W/'projects/nesnd-repository';branch='fix/journal-war-feedback-20261104'
backup=W/'backups/candidate-journal-war-feedback-final-20261104T001505Z/mod'
bm,cm,mm=man(B),man(C),man(M);assert man(backup)==cm
patch=json.loads(read(R/'patch-files.json'));assert {p:h for p,h in cm.items() if bm.get(p)!=h}==patch
assert not bm.keys()-cm.keys();assert json.loads(read(R/'final-validation.json'))['status']=='STATIC_PASS'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==PARENT
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()=='main'
existing=json.loads(read(R/'preexisting-main-differences.json'))['files']
assert existing==['localization/simp_chinese/replace/zzzzzzz_nesnd_qin_persia_l_simp_chinese.yml']
for rel,h in bm.items():
    if rel not in existing:assert sha(repo/rel)==h,('Repo baseline changed',rel)
    else:assert sha(M/rel)==h==cm[rel],('Pre-existing author text changed again',rel)
user={p:h for p,h in mm.items() if bm.get(p)!=h}
for rel,h in patch.items():assert mm.get(rel) in [bm.get(rel),h],('Main conflict',rel)
assert not bm.keys()-mm.keys(),'Main baseline deletion requires review'
for row in json.loads(read(R/'native-sources.json'))['sources']:assert sha(G/row['path'])==row['sha256']
for report in ['regression-candidate.json','boundary-tests.json','tiger-candidate-run.json']:
    data=json.loads(read(R/report))
    for p,h in patch.items():assert data['source_files'][p]==h
subprocess.run(['git','switch','-c',branch],cwd=repo,check=True)
for rel in patch:
    p=M/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/rel,p)
for rel,h in user.items():assert sha(M/rel)==h
merged=man(M)
dump(R/'main-merge.json',{'parent':PARENT,'branch':branch,'candidate':str(C),'changed':patch,'preserved_user_edits':user,'preserved_preexisting_author_files':existing,'deletions':[],'conflicts':[],'main':merged,'engine_verified':False})
dump(R/'candidate-backup.json',{'path':str(backup),'verified_files':len(cm),'engine_verified':False})
for rel,h in merged.items():
    p=repo/rel
    if not p.exists() or sha(p)!=h:p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(M/rel,p)
for rel in ['references/journal-text-contract.md','references/syntax-and-routing.md','references/active-work.md']:
    p=repo/'development/nesnd-skill'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,p)
z=W/'releases/nesnd-20261104-journal-war-feedback.zip';assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for rel in merged:
        if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):continue
        assert not any(q in rel for q in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
        f.write(M/rel,rel)
with zipfile.ZipFile(z) as f:
    for rel in f.namelist():assert hashlib.sha256(f.read(rel)).hexdigest()==merged[rel]
dump(R/'package.json',{'path':str(z),'sha256':sha(z),'all_files_match_main':True,'QA_included':False})
for p in R.iterdir():
    if p.is_file() and p.suffix in ['.md','.json','.diff'] and p.name not in ['tiger-baseline.json','tiger-candidate.json','graph-audit.json'] and p.stat().st_size<3000000:
        q=repo/'development/workbench/reports/journal-war-feedback-20261103'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
names=['journal_war_context.py','build_journal_feedback.py','connect_south_holdouts.py','write_journal_war_text.py','extract_journal_war_save.py','test_journal_war_feedback.py','validate_journal_war_tools.py','revise_journal_feedback.py','revise_ming_flight.py','close_holdout_settlement.py','test_holdout_boundaries.py','document_journal_war_feedback.py','freeze_journal_war_feedback.py','finalize_journal_war_feedback.py','deliver_journal_war_feedback.py']
for name in names:
    p=repo/'development/workbench/tools'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/'tools'/name,p)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
q=subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,capture_output=True,text=True,encoding='utf8')
dump(R/'git-whitespace.json',{'status':q.returncode,'output':q.stdout+q.stderr});assert q.returncode==0,q.stdout
shutil.copy2(R/'git-whitespace.json',repo/'development/workbench/reports/journal-war-feedback-20261103/git-whitespace.json')
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Fix journal progress, Delhi visibility and Ming loyalist war settlement'],cwd=repo,check=True)
assert man(M)==merged
print('Main and candidate match:',merged==cm,'Changed files:',len(patch),'Backup files:',len(cm))
