from pathlib import Path
import json,hashlib,sys,re,collections
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');import pdx
G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102')
d=json.loads((W/'native-inventory.json').read_text(encoding='utf8'));sources={v['path']:v for v in d['sources']}
def add(rel,group,ids=None):
 p=G/rel;t,r=pdx.read(p);sources[str(p)]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 for n in r.children:
  if n.children is not None and (ids is None or n.key in ids):d[group].append({'path':rel,'line':t.count('\n',0,n.start)+1,'end_line':t.count('\n',0,n.end)+1,'id':n.key,'source':t[n.start:n.end]})
for rel in ['events/soi_events/00_ep1_korea_events.txt','events/agitators_events/coup_events.txt','events/iberia_events/ip4_coup_events.txt']:add(rel,'events')
add('common/institutions/00_institutions.txt','support_definitions',['institution_police','institution_colonial_affairs','institution_schools'])
for rel in ['common/interest_groups/00_landowners.txt','common/interest_groups/00_armed_forces.txt','common/interest_groups/00_intelligentsia.txt']:add(rel,'support_definitions')
text='\n'.join(r['source'] for cat in ['journal_entries','events','buttons','support_definitions'] for r in d[cat])
tokens=set(re.findall(r'[A-Za-z_][A-Za-z0-9_.]*',text))
for folder in ['common/political_movements','common/ideologies','common/static_modifiers','common/scripted_progress_bars','common/character_roles','common/character_traits']:
 for p in (G/folder).glob('*.txt'):
  t,r=pdx.read(p);hit=[n.key for n in r.children if n.key in tokens]
  if hit:add(p.relative_to(G).as_posix(),'support_definitions',hit)
byid=collections.defaultdict(list)
for group in ['journal_entries','events','buttons','support_definitions']:
 for r in d[group]:byid[r['id']].append(r)
edges=[]
for group in ['journal_entries','events','buttons','support_definitions']:
 for row in d[group]:
  t,r=pdx.read(G/row['path']);n=next(v for v in r.children if v.key==row['id'])
  for v in n.walk():
   target=kind=None
   if v.key=='trigger_event':target=v.scalar('id');kind='event'
   elif v.key=='add_journal_entry':target=v.scalar('type');kind='add_je'
   elif v.key=='scripted_button':target=pdx.unquote(v.value);kind='button'
   elif v.key=='scripted_progress_bar':target=pdx.unquote(v.value);kind='progress_bar'
   elif v.key in byid and v.key!=row['id']:target=v.key;kind='script_call'
   elif v.value and v.value in byid and '.' in v.value:target=v.value;kind='event_pool'
   if target:edges.append({'caller':row['id'],'kind':kind,'target':target,'path':row['path'],'line':t.count('\n',0,v.start)+1,'target_locations':[{k:q[k] for k in ['path','line','end_line']} for q in byid.get(target,[])]})
d['direct_reference_edges']=edges;d['sources']=sorted(sources.values(),key=lambda v:v['path'])
(W/'native-inventory.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('support defs',len(d['support_definitions']),'sources',len(d['sources']),'events',len(d['events']),'edges',len(edges))
