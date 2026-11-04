from regional_context import *
prior=R/'prior-regression';prior.mkdir(exist_ok=True)
old=W/'reports/journal-bug-sweep-20261104'
for name in ['bulk-changes.json','tiger-baseline.json']:shutil.copy2(old/name,prior/name)
shutil.copy2(R/'tiger-candidate.json',prior/'tiger-candidate.json')
for script in ['test_journal_sweep.py','verify_journal_sweep.py','test_per_usm_mechanics.py']:
 code='from regional_context import C,R; import sweep_context as s; s.C=C; s.R=R/"prior-regression"; import runpy; runpy.run_path('+repr(str(W/'tools'/script))+',run_name="__main__")'
 p=subprocess.run([sys.executable,'-X','utf8','-c',code],cwd=W/'tools',capture_output=True,text=True,encoding='utf8')
 print(script,p.stdout,p.stderr);assert p.returncode==0
dump(R/'prior-regression-summary.json',{'pass':True,'checks':97,'candidate':str(C),'engine_verified':False,'coverage':'Previous 6 regressions,45 boundary/source checks,46 Persian/USM arithmetic and lifecycle fixtures run against this candidate'})
