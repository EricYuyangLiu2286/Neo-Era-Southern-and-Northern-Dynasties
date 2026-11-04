from sweep_context import *
import zipfile,hashlib
repo=W/'projects/nesnd-repository';branch='fix/journal-mechanics-20261104'
backup=W/'backups/candidate-journal-bug-sweep-final-20261104T031126Z/mod'
bm,cm,mm=man(B),man(C),man(M)
assert man(backup)==cm
assert mm==bm,'Main changed since freeze; review before merge'
patch=json.loads(read(R/'patch-files.json'))
assert patch=={p:h for p,h in cm.items() if bm.get(p)!=h}
final=json.loads(read(R/'final-validation.json'));assert final['status']=='STATIC_PASS' and final['source_files']==cm
assert not bm.keys()-cm.keys()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==PARENT
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()=='main'
for p,h in bm.items():assert sha(repo/p)==h,('Repository baseline differs',p)
subprocess.run(['git','switch','-c',branch],cwd=repo,check=True)
for rel in patch:
 p=M/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/rel,p)
assert man(M)==cm
dump(R/'main-merge.json',{'parent':PARENT,'branch':branch,'candidate':str(C),'changed':patch,'preserved_user_edits':'All baseline files verified; no concurrent edits found','deletions':[],'conflicts':[],'main':cm,'engine_verified':False})
dump(R/'candidate-backup.json',{'path':str(backup),'verified_files':len(cm),'all_files_match_main':True,'engine_verified':False})
for rel,h in cm.items():
 p=repo/rel
 if not p.exists() or sha(p)!=h:p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(M/rel,p)
for rel in ['references/journal-system-design.md','references/active-work.md']:
 p=repo/'development/nesnd-skill'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,p)
plan='plans/two-empires/61-continuity-and-journal-rework-20261104.md'
shutil.copy2(W/plan,repo/'development/workbench'/plan)
z=W/'releases/nesnd-20261104-journal-mechanics.zip';assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for rel in cm:
  if rel.startswith(('docs/','.scratch/','development/','tools/')) or rel.endswith(('.md','.bak','.py','.pyc')):continue
  assert not any(q in rel for q in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa']),rel
  f.write(M/rel,rel)
with zipfile.ZipFile(z) as f:
 for rel in f.namelist():assert hashlib.sha256(f.read(rel)).hexdigest()==cm[rel]
dump(R/'package.json',{'path':str(z),'sha256':sha(z),'all_files_match_main':True,'QA_included':False})
for p in R.iterdir():
 if p.is_file() and p.suffix in ['.md','.json','.diff'] and p.name not in ['tiger-baseline.json','tiger-candidate.json','graph-audit.json'] and p.stat().st_size<3000000:
  q=repo/'development/workbench/reports/journal-bug-sweep-20261104'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for name in ['sweep_context.py','test_journal_sweep.py','verify_journal_sweep.py','test_per_usm_mechanics.py','sweep_mcp.py','sweep_bulk_checks.py','connect_resource_buttons.py','finalize_sweep_format.py','record_sweep_writing.py','freeze_journal_sweep.py','deliver_journal_sweep.py']:
 p=repo/'development/workbench/tools'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/'tools'/name,p)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
q=subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,capture_output=True,text=True,encoding='utf8')
dump(R/'git-whitespace.json',{'status':q.returncode,'output':q.stdout+q.stderr});assert q.returncode==0,q.stdout
shutil.copy2(R/'git-whitespace.json',repo/'development/workbench/reports/journal-bug-sweep-20261104/git-whitespace.json')
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Fix journal feedback and add Persian resources and Wu western incorporation'],cwd=repo,check=True)
assert man(M)==cm
print('Main merged, candidate backed up, source commit created; files changed:',len(patch))
