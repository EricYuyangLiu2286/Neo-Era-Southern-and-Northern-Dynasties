from canon_routes_context import *
import subprocess,collections
cfg=json.loads((R/'batch-c-repair4-test-config.json').read_text('utf-8'));out=Path(cfg['run']);snapshot=Path(cfg['snapshot'])
config=W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'
command=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(config),'--json',str(snapshot)]
with (out/'tiger-raw.json').open('wb') as stdout,(out/'tiger-stderr.txt').open('wb') as stderr:
 p=subprocess.run(command,stdout=stdout,stderr=stderr)
raw=json.loads((out/'tiger-raw.json').read_text('utf-8-sig'));owned=set(cfg['owned_files'])
selected=[]
for d in raw:
 locs=d.get('locations',[])
 if any(str(x.get('path','')).replace('\\','/') in owned for x in locs):selected.append(d)
dump(out/'tiger-c-owned.json',{'command':command,'returncode':p.returncode,'total_diagnostics':len(raw),'owned_diagnostics':selected,'owned_counts':dict(collections.Counter(d.get('key') for d in selected)),'game_launched':False})
print('Tiger completed; owned diagnostic counts:',collections.Counter(d.get('key') for d in selected))
for d in selected:
 if d.get('key') not in ['brace-placement','localization']:
  print(d.get('severity'),d.get('key'),d.get('message'),[(x.get('path'),x.get('linenr'),x.get('line')) for x in d.get('locations',[])])
