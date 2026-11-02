from qin_persia_context import *
import collections,subprocess
phase=sys.argv[1] if len(sys.argv)>1 else 'final'
if '--run' in sys.argv:
 cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(C)]
 p=subprocess.run(cmd,capture_output=True);(R/f'tiger-{phase}.json').write_bytes(p.stdout);(R/f'tiger-{phase}-stderr.txt').write_bytes(p.stderr)
a=json.loads(read(R/f'tiger-{phase}.json'));old=json.loads(read(W/'reports/ui-poland-tributary-20261102/tiger-final.json'))
def key(x):return (x['severity'],x['key'],x['message'],tuple((n.get('from'),n.get('path'),(n.get('line') or '').strip()) for n in x['locations']))
base=collections.Counter(map(key,old));added=[]
for x in a:
 k=key(x)
 if base[k]:base[k]-=1
 else:added.append(x)
dump(R/f'tiger-added-{phase}.json',added)
dump(R/'tiger-delta.json',{'phase':phase,'counts':dict(collections.Counter(x['severity'] for x in a)),'added_count':len(added),'added':added,'game_launched':False})
print('NEW',collections.Counter(x['key'] for x in added))
for x in added:
 if x['key'] not in ['brace-placement','localization']:
  print(x['severity'],x['key'],x['message'],[(n.get('path'),n.get('linenr'),n.get('line')) for n in x['locations']])
