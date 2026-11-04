from pathlib import Path
import json,hashlib,datetime
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/canon-route-execution-20261104';T=W/'tools';f=json.loads((R/'batch-b2-repair2-freeze.json').read_text(encoding='utf-8'));im=json.loads((R/'integration-snapshot-current.json').read_text(encoding='utf-8'));print('manifest_keys',list(f))
snap=Path(f['snapshot']);expected=dict(im['source_files']);expected.update(f['owned_files']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();bad=[p for p,h in expected.items() if sha(snap/p)!=h];assert not bad,bad
run=R/('batch-b2-repair2-validation-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'));run.mkdir();cfg=json.loads((R/'batch-b2-repair1-test-config.json').read_text(encoding='utf-8'));cfg.update(run=str(run),snapshot=str(snap),owned_freeze=f['owned_freeze']);cfg['owned_files']={p:expected[p] for p in cfg['owned_files']};(R/'batch-b2-repair2-test-config.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
for p in list(T.glob('test_b2r1_*.py'))+list(T.glob('b2r1_*.py')):
 s=p.read_text(encoding='utf-8-sig').replace('b2r1_','b2r2_').replace('batch-b2-repair1-test-config.json','batch-b2-repair2-test-config.json').replace("R/'batch-b2-repair1-freeze.json'","R/'batch-b2-repair2-freeze.json'")
 # AI compares to original pre-repair score, not to immediately preceding repair1.
 if p.name=='test_b2r1_ai_exhaustive.py':s=s.replace("original=Path(json.loads((R/'batch-b2-repair2-freeze.json').read_text())['parent_freeze'])","original=Path(json.loads((R/'batch-b2-repair1-freeze.json').read_text())['parent_freeze'])")
 (T/p.name.replace('b2r1_','b2r2_')).write_text(s,encoding='utf-8')
(run/'integrity-start.json').write_text(json.dumps({'files':len(expected),'full_sha_match':True,'owned36_match':True,'expected':expected},indent=2),encoding='utf-8');print(json.dumps({'snapshot':str(snap),'run':str(run),'verified':len(expected)}))
