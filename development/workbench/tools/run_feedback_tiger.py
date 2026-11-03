from feedback_context import *
import subprocess
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
with (R/'tiger-final.json').open('wb') as out,(R/'tiger-final.stderr.txt').open('wb') as err:
 p=subprocess.run(cmd,stdout=out,stderr=err)
print('Tiger finished',p.returncode)
