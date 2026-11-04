from pathlib import Path
import json,shutil,subprocess,collections,hashlib
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/canon-route-execution-20261104';cfg=json.loads((R/'batch-b2-repair2-test-config.json').read_text(encoding='utf-8'));run=Path(cfg['run']);snap=Path(cfg['snapshot']);f=json.loads((R/'batch-b2-repair2-freeze.json').read_text(encoding='utf-8'));base=W/'validation/snapshots/batch-b2-repair2-tiger-baseline-20261104T173621Z/mod';assert not base.exists();shutil.copytree(snap,base);pre=W/'backups/b2-preimplementation-20261104';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();restored=[];removed=[]
for rel in f['owned_files']:
 p=base/rel;assert p.resolve().is_relative_to(base.resolve())
 if (pre/rel).exists():shutil.copy2(pre/rel,p);restored.append({'path':rel,'sha256':sha(p)})
 else:p.unlink();removed.append(rel)
(run/'tiger-baseline-construction.json').write_text(json.dumps({'snapshot':str(base),'unchanged_full_dependency_base':str(snap),'restored4_pre_B2':restored,'removed32_B2_new_files':removed},indent=2),encoding='utf-8')
command=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(base)]
with (run/'tiger-baseline-raw.json').open('wb') as out,(run/'tiger-baseline-stderr.txt').open('wb') as err:r=subprocess.run(command,stdout=out,stderr=err)
(run/'tiger-baseline-run.json').write_text(json.dumps({'command':command,'returncode':r.returncode},indent=2),encoding='utf-8');print(json.dumps({'baseline':str(base),'restored':len(restored),'removed':len(removed),'returncode':r.returncode}))
