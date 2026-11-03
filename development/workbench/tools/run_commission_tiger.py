from commission_context import *
import subprocess
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
with (R/'tiger-current.json').open('wb') as o,(R/'tiger-current.stderr.txt').open('wb') as e:p=subprocess.run(cmd,stdout=o,stderr=e)
a=json.loads(read(R/'tiger-current.json'));b=json.loads(read(W/'reports/india-development-20261103/tiger-current.json'))
def sig(x):return x['severity'],x['key'],x['message'],tuple((z.get('path'),(z.get('line') or '').strip()) for z in x['locations'])
old={sig(x) for x in b};added=[x for x in a if sig(x) not in old];dump(R/'tiger-added.json',added)
print('New diagnostics',len(added))
for x in added:print(x['severity'],x['key'],x['message'],[(z.get('path'),z.get('linenr')) for z in x['locations']])
