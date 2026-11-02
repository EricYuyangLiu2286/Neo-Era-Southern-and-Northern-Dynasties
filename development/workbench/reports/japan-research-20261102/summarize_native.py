import json,collections
from pathlib import Path
x=json.loads(Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102/native-inventory.json').read_text(encoding='utf-8'))
b=collections.Counter();p=collections.Counter();g=collections.defaultdict(set);caps=collections.Counter()
for st,d in x['economic_inputs'].items():
 for r in d['pops']:p[(r['culture'],r['religion'])]+=int(r['size'])
 for r in d.get('buildings',[]):
  b[r['building']]+=r['ownership_levels'];g[r['building']].add(', '.join(r['pms']))
 if st not in ['STATE_HOKKAIDO','STATE_RYUKYU_ISLANDS']:
  for c in d['resources']['capped']:caps.update({k:int(v) for k,v in c.items()})
print('POP',p,'TOTAL',sum(p.values()))
print('BUILDING TOTAL',sum(b.values()),b)
print('CAPS WHOLE9',caps)
for k,v in g.items(): print(k,v)
