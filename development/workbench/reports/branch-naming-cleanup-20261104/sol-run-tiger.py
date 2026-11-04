from pathlib import Path
import subprocess,json,hashlib,concurrent.futures,collections
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/branch-naming-cleanup-20261104';G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3');C=W/'exports/maintenance-current';B=W/'backups/pre-change-maintenance-pre-cleanup-20261104T213001Z/mod';exe=W/'tools/tiger-1.19.0/vic3-tiger.exe'
config=R/'sol-tiger-repair1.conf'; config.write_text('languages = { check = "english" check = "simp_chinese" }\nfilter = { show_vanilla = no show_loaded_mods = yes }\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,root):
 cmd=[str(exe),'--game',str(G),'--config',str(config),'--json',str(root)]
 q=subprocess.run(cmd,capture_output=True,timeout=240)
 (R/f'sol-tiger-{label}.json').write_bytes(q.stdout);(R/f'sol-tiger-{label}.stderr.txt').write_bytes(q.stderr)
 return {'label':label,'command':cmd,'exit_code':q.returncode,'raw_sha256':sha(R/f'sol-tiger-{label}.json'),'stderr_sha256':sha(R/f'sol-tiger-{label}.stderr.txt')}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:commands=list(pool.map(lambda x:run(*x),[('B',B),('C',C)]))
report={'commands':commands,'tool_sha256':sha(exe),'configuration_sha256':sha(config),'baseline_root':str(B),'candidate_root':str(C),'candidate_manifest_sha256':sha(R/'candidate-freeze.json')}
for label in ('B','C'):
 d=json.loads((R/f'sol-tiger-{label}.json').read_text(encoding='utf-8-sig'));report[label]={'count':len(d),'severity':dict(collections.Counter(x.get('severity') for x in d))}
(R/'sol-tiger-execution.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
