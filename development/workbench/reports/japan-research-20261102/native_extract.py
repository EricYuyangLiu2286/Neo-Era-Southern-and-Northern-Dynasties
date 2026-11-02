from pathlib import Path
import sys,json,hashlib,re,collections
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
import pdx
G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102')
cache={}
def rd(p):
 p=G/p
 if p not in cache: cache[p]=pdx.read(p)
 return cache[p]
def loc(p,t,n): return {'path':p,'line':t.count('\n',0,n.start)+1,'end_line':t.count('\n',0,n.end)+1}
def tree(n):return {'key':n.key,'op':n.op,'value':pdx.unquote(n.value),'children':[tree(c) for c in n.children] if n.children is not None else None}
def sub(p,root):
 t,r=rd(p);return t,r.get(root)
hist={}
for kind,root in [('pops','POPS'),('buildings','BUILDINGS')]:
 p=f'common/history/{kind}/11_east_asia.txt';t,r=sub(p,root)
 for st in r.children:
  for own in st.children or []:
   if own.key!='region_state:JAP':continue
   hist.setdefault(st.key[2:],{})[kind]=[]
   for x in own.children or []:
    if x.key not in ['create_pop','create_building']:continue
    row=loc(p,t,x)
    if kind=='pops':row.update({k:x.scalar(k) for k in ['culture','religion','size']})
    else:
     row.update(building=x.scalar('building'),level_explicit=x.scalar('level'),reserves=x.scalar('reserves'),pms=x.get('activate_production_methods').values() if x.get('activate_production_methods') else [],ownerships=[tree(o) for o in x.all('add_ownership')])
     row['ownership_levels']=sum(float(z.value) for o in x.all('add_ownership') for z in o.walk() if z.key=='levels')
    hist[st.key[2:]][kind].append(row)
p='map_data/state_regions/11_east_asia.txt';t,r=rd(p)
for st in r.children:
 if st.key not in hist:continue
 hist[st.key]['resources']={**loc(p,t,st),'arable_land':st.scalar('arable_land'),'arable_resources':st.get('arable_resources').values() if st.get('arable_resources') else [],'capped':[{c.key:c.value} for c in st.get('capped_resources').children] if st.get('capped_resources') else [],'discoverable':[tree(n) for n in st.all('resource')],'traits':st.get('traits').values() if st.get('traits') else []}
p='common/history/military_formations/06_military_formations_asia.txt';t,r=sub(p,'MILITARY_FORMATIONS');r=r.get('c:JAP');mil=[]
for x in r.all('create_military_formation'):
 mil.append({**loc(p,t,x),'name':x.scalar('name'),'type':x.scalar('type'),'hq':x.scalar('hq_region'),'units':[{**loc(p,t,z),'type':z.scalar('type'),'state':z.scalar('state_region'),'count':z.scalar('count')} for z in x.all('combat_unit')]})
jes=[];events=[];buttons=[]
for rel,store,pattern in [('common/journal_entries',jes,r'japan|meiji|sakoku|iwakura|zaibatsu|ryukyu|hokkaido|tenpo|korea_colonization'),('events',events,r'meiji_restoration|japan_events'),('common/scripted_buttons',buttons,r'japan|meiji|iwakura|tenpo|ryukyu')]:
 for p in (G/rel).rglob('*.txt'):
  if not re.search(pattern,p.as_posix(),re.I):continue
  path=p.relative_to(G).as_posix();t,r=rd(path)
  for n in r.children:
   if n.children is None:continue
   store.append({**loc(path,t,n),'id':n.key,'data':tree(n),'source':t[n.start:n.end]})
p='common/character_templates/country_jap.txt';t,r=rd(p);chars=[]
for n in r.children:
 if n.children is None:continue
 chars.append({**loc(p,t,n),'id':n.key,**{k:n.scalar(k) for k in ['first_name','last_name','birth_date','ig_leader','interest_group','ideology','role','ruler','heir','commander_rank','historical','culture','religion']},'traits':n.get('traits').values() if n.get('traits') else [],'source':t[n.start:n.end]})
data={'game_version':'1.13.11','steam_build':'24799966','economic_inputs':hist,'formations':mil,'journal_entries':jes,'events':events,'buttons':buttons,'character_templates':chars,'sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in cache]}
(W/'native-inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('states',len(hist),'JE',len(jes),'events',len(events),'buttons',len(buttons),'templates',len(chars))
for s,d in hist.items():
 print(s,'population',sum(int(x['size']) for x in d.get('pops',[])),'arable',d['resources']['arable_land'],'caps',d['resources']['capped'],'buildings',[(b['building'],b['ownership_levels']) for b in d.get('buildings',[])])
print('FORMATIONS',json.dumps(mil))
print('JES',[j['id'] for j in jes])
