from pathlib import Path
import sys, collections, copy, json
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read, effective_files
W=Path(__file__).parents[2]; M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'; B=W/'backups/pre-change-english-gujarat-20261106T212037Z/mod'; G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
def ast(n): return (n.key,n.op,n.value,n.prefix,tuple(ast(c) for c in n.children or []))
def load(base,rel): return read(base/rel)[1].children[0]
tags={'USM','BER','NAW'}; minor={'KUT','DHA','IDA','PLP','JUN','BHV'}
out={}; trees={}
for kind,file in [('states','00_states.txt'),('pops','10_india.txt'),('buildings','10_india.txt')]:
 rel=f'common/history/{kind}/{file}'; old=load(B,rel); new=load(M,rel); a=old.get('s:STATE_GUJARAT'); b=new.get('s:STATE_GUJARAT'); trees[kind]=(a,b)
 assert [ast(n) for n in old.children if n.key!='s:STATE_GUJARAT']==[ast(n) for n in new.children if n.key!='s:STATE_GUJARAT']
 if kind=='states':
  def states(n): return {x.scalar('country')[2:]:x for x in n.all('create_state')}
  aa,bb=states(a),states(b)
  for t in minor: assert ast(aa[t])==ast(bb[t])
  expected=collections.Counter(p for t in tags for p in aa[t].get('owned_provinces').values()); actual=collections.Counter(bb['FRA'].get('owned_provinces').values()); assert expected==actual and len(actual)==22 and set(actual.values())=={1}
  assert set(bb)==minor|{'FRA'} and bb['FRA'].scalar('state_type')=='unincorporated'
  assert [ast(n) for n in a.children if n.key!='create_state']==[ast(n) for n in b.children if n.key!='create_state']
  assert 'x31D0E0' in actual
  out['provinces']=22
 else:
  for t in minor:
   x,y=a.get('region_state:'+t),b.get('region_state:'+t)
   assert (ast(x) if x else None)==(ast(y) if y else None)
  assert not any(b.get('region_state:'+t) for t in tags)
  orig=[n for s in a.children if s.key in {'region_state:'+t for t in tags} for n in s.children]; dest=b.get('region_state:FRA').children
  if kind=='pops':
   assert [ast(n) for n in orig]==[ast(n) for n in dest]
   assert all(n.scalar('culture') for n in dest)
   out['pops']={'blocks':len(dest),'size':sum(int(n.scalar('size')) for n in dest),'omitted_religion':collections.Counter(n.scalar('culture') for n in dest if not n.scalar('religion'))}
  else:
   def weighted(rows,normalize):
    c=collections.Counter()
    for n in rows:
     n=copy.deepcopy(n); levels=[x for x in n.walk() if x.key=='levels']; assert len(levels)==1
     lev=int(levels[0].value); levels[0].value='LEVEL'
     if normalize:
      for x in n.walk():
       if x.key=='country' and x.value and x.value.strip('"') in {'c:USM','c:BER','c:NAW'}: x.value='"c:FRA"'
     c[ast(n)]+=lev
    return c
   aa,bb=weighted(orig,True),weighted(dest,False)
   for key in aa:
    expected=aa[key]+(3 if key[4][0][2].strip('"')=='building_naval_administration' else 0)
    assert bb[key]==expected,(key,aa[key],bb[key])
   assert set(aa)==set(bb)
   types=[n.scalar('building') for n in dest]; assert len(types)==len(set(types))
   out['building_levels']={'before':sum(aa.values()),'after':sum(bb.values()),'types':types}
states=load(M,'common/history/states/00_states.txt')
owners={n.scalar('country')[2:] for s in states.children for n in s.all('create_state')}
assert not owners & {'BER','NAW','BIC'}
sr=read(G/'common/strategic_regions/west_south_asia_strategic_regions.txt')[1].get('region_north_india').get('states').values()
fra_north=[s.key for s in states.children if s.key and s.key[2:] in sr and any(n.scalar('country')=='c:FRA' for n in s.all('create_state'))]
assert fra_north==['s:STATE_GUJARAT']; out['FRA_north_india']=fra_north
# Report every effective startup BER/NAW reference with its actual ancestor scopes.
refs=[]
for p in effective_files([G,M],'common/history'):
 text,root=read(p)
 def walk(n,anc):
  if n.value and n.value.strip('"') in {'c:BER','c:NAW'} or n.key in {'c:BER','c:NAW'}:
   refs.append({'file':str(p),'line':text[:n.start].count('\n')+1,'key':n.key,'value':n.value,'op':n.op,'ancestors':anc})
  for ch in n.children or []: walk(ch,anc+[(n.key,n.op)])
 walk(root,[])
out['effective_startup_refs']=refs
ships=read(G/'common/ship_types/00_ship_types.txt')[1]
fleet=load(M,'common/history/military_formations/nesnd_french_gujarat_fleet.txt').get('c:FRA').get('create_military_formation')
assert fleet.scalar('type')=='fleet' and fleet.scalar('hq_region')=='sr:region_north_india'
crew=sum(int(n.scalar('count'))*int(ships.get(n.scalar('type').split(':')[1]).get('modifier').scalar('ship_crew_max_add')) for n in fleet.all('ship'))
assert crew==3600
out['crew']=crew
Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
