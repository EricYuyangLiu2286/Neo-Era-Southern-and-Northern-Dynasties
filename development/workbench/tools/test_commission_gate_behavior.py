from commission_context import *
from copy import deepcopy
from types import SimpleNamespace
# A strict subset evaluator reads the REAL ordered trigger AST. It does not execute the engine.
class Obj:
 def __init__(self,kind,name,**attrs):self.kind,self.name,self.a=kind,name,attrs
 def __repr__(self):return self.kind+':'+self.name
class Evaluator:
 def __init__(self,rootdir,world):
  self.w=world;self.db={};self.reads=[];self.values={n.key:n for n in parse(read(rootdir/'common/script_values/nesnd_india_diplomacy.txt')).children}
  for p in (rootdir/'common/scripted_triggers').glob('*.txt'):
   for n in parse(read(p)).children:self.db[n.key]=n
 def scope(self,key,o,root,prev):
  if key in ['this','root','prev']:return {'this':o,'root':root,'prev':prev}[key]
  if key.startswith('scope:'):return self.w.get('saved',{}).get(key[6:])
  if key.startswith('c:'):return self.w['countries'].get(key[2:])
  if key.startswith('sr:'):return self.w.setdefault('strategic',{}).get(key[3:])
  if key.startswith('var:'):return o.a.get('variable_values',{}).get(key[4:])
  if key.startswith('s:'):
   reg,*tail=key[2:].split('.region_state:');r=self.w['regions'].get(reg)
   return next((x for x in r.a['states'] if x.a['owner'].name==tail[0]),None) if r and tail else r
  if key in ['owner','overlord','state_region','controller','region','ruler']:return o.a.get(key)
  return None
 def cmp(self,a,op,b):
  return {'=':lambda:a==b,'?=':lambda:a is not None and a==b,'!=':lambda:a!=b,'>':lambda:a>b,'>=':lambda:a>=b,'<':lambda:a<b,'<=':lambda:a<=b}[op]()
 def block(self,n,o,root,prev=None):
  out=[];chain=None
  for x in n.children or []:
   if x.key in ['count','percent','text','subject','object']:continue
   if x.key=='trigger_if':
    chain=self.block(x.get('limit'),o,root,prev)
    out.append(self.body_except_limit(x,o,root,prev) if chain else True)
   elif x.key=='trigger_else':
    if chain is None:raise AssertionError('orphan else')
    if not chain:out.append(self.block(x,o,root,prev))
    chain=None
   else:chain=None;out.append(self.expr(x,o,root,prev))
  return all(out)
 def body_except_limit(self,n,o,root,prev):return self.block(SimpleNamespace(children=[x for x in n.children if x.key!='limit']),o,root,prev)
 def expr(self,n,o,root,prev):
  k,v=n.key,n.value
  if k=='AND':return self.block(n,o,root,prev)
  if k=='OR':return any([self.expr(x,o,root,prev) for x in n.children])
  if k in ['NOT','NOR','NAND']:
   vals=[self.expr(x,o,root,prev) for x in n.children]
   return not (all(vals) if k in ['NOT','NAND'] else any(vals))
  if k in ['custom_tooltip','hidden_trigger']:return self.block(n,o,root,prev)
  if k in self.values:return self.cmp(self.number(k,o,root,prev),n.op,self.number(v,o,root,prev))
  if k in self.db:return self.block(self.db[k],o,root,prev)==(v=='yes')
  if k=='always':return v=='yes'
  if k=='exists':return self.scope(v,o,root,prev) is not None
  if k=='has_variable':return v in o.a.get('vars',set())
  if k=='has_modifier':return v in o.a.get('modifiers',set())
  if k=='has_journal_entry':return v in o.a.get('journals',set())
  if k=='is_subject_of':
   target=self.scope(v,o,root,prev)
   assert target is not None,('missing subject target',v)
   parent=o.a.get('overlord');seen=set()
   while parent is not None and parent.name not in seen:
    if parent is target:return True
    seen.add(parent.name);parent=parent.a.get('overlord')
   return False
  if k in ['has_law','has_law_or_variant']:return v.removeprefix('law_type:') in o.a.get('laws',set())
  if k=='country_has_monarchy_law':return bool(o.a.get('laws',set()) & {'law_monarchy','law_social_monarchy'})
  if k=='has_war_with':
   target=self.scope(v,o,root,prev);assert target is not None,('missing war target',v)
   return target.name in o.a.get('wars',set())
  if k=='is_direct_subject_of':
   target=self.scope(v,o,root,prev);assert target is not None
   return o.a.get('overlord') is target
  if k=='can_increase_autonomy':return bool(o.a.get('can_increase_autonomy',False))==(v=='yes')
  if k=='gold_reserves':return self.cmp(o.a.get('gold_reserves',0),n.op,self.number(v,o,root,prev))
  if k=='has_technology_researched':return v in o.a.get('tech',set())
  if k in ['any_scope_state','any_state_region','any_country','any_scope_building']:
   if k=='any_scope_state':items=o.a['states']
   elif k=='any_state_region':items=list(self.w['regions'].values())
   elif k=='any_country':items=list(self.w['countries'].values())
   else:items=o.a.get('buildings',[])
   found=sum(self.block(n,q,root,o) for q in items);count=n.get('count')
   return self.cmp(found,count.op,float(count.value)) if count else found>0
  if k in ['in_default','is_country_alive','is_subject','is_at_war','is_active_in_diplomatic_play','is_diplomatic_play_committed_participant','is_diplomatic_play_initiator','is_diplomatic_play_target','is_largest_state_in_region']:
   a=(o.a.get('overlord') is not None) if k=='is_subject' else o.a.get(k,False)
   return a==(v=='yes')
  if k=='is_building_type':return o.name==v
  if k=='is_country_type':return o.a.get('country_type','recognized')==v
  if k in ['level','state_population','num_states']:return self.cmp(o.a.get(k,len(o.a.get('states',[])) if k=='num_states' else 0),n.op,float(v))
  # Links/comparisons fail loudly for missing required scopes; no implicit default masks errors.
  link=self.scope(k,o,root,prev)
  if n.children is not None:
   if link is None:
    if n.op=='?=':return True
    raise AssertionError(('unguarded scope',k,o.name))
   return self.block(n,link,root,o)
  if k in ['this','root','prev','owner','overlord','state_region','controller','region','ruler'] or k.startswith(('c:','s:','scope:','var:')):
   target=self.scope(v,o,root,prev)
   if target is None and n.op!='?=':raise AssertionError(('missing RHS',v,k,o.name))
   return self.cmp(link,n.op,target)
  raise AssertionError(('unsupported real AST',k,n.op,v))
 def number(self,t,o,root,prev):
  try:return float(t)
  except (TypeError,ValueError):pass
  if t in self.values:return self.value_block(self.values[t],o,root,prev)
  if '.' in t:
   first,rest=t.split('.',1);target=self.scope(first,o,root,prev)
   assert target is not None,('missing numeric scope',first)
   return self.number(rest,target,root,o)
  val=self.scope(t,o,root,prev)
  if isinstance(val,(int,float)):return val
  if t in o.a and isinstance(o.a[t],(int,float)):return o.a[t]
  raise AssertionError(('unknown numeric value',t,o.name))
 def value_block(self,n,o,root,prev,current=0):
  chain=None
  for x in n.children or []:
   if x.key=='if':
    chain=self.block(x.get('limit'),o,root,prev)
    if chain:current=self.value_block(SimpleNamespace(children=[a for a in x.children if a.key!='limit']),o,root,prev,current)
   elif x.key in ['else','else_if']:
    assert chain is not None
    if not chain:
     yes=True if x.key=='else' else self.block(x.get('limit'),o,root,prev)
     if yes:current=self.value_block(SimpleNamespace(children=[a for a in x.children if a.key!='limit']),o,root,prev,current)
     chain=yes
   else:
    chain=None
    val=self.number(x.value,o,root,prev)
    if x.key=='value':current=val
    elif x.key=='add':current+=val
    elif x.key=='multiply':current*=val
    elif x.key=='min':current=max(current,val)
    elif x.key=='max':current=min(current,val)
    else:raise AssertionError(('unimplemented arithmetic',x.key))
  return current
 def test(self,key,actor='USM',global_root=False):return self.block(self.db[key],self.w['countries'][actor],None if global_root else self.w['countries'][actor])

def world_from_history():
 data=json.loads(read(R/'native-starting-regions.json'));w={'countries':{},'regions':{}}
 def country(t):
  if t not in w['countries']:w['countries'][t]=Obj('country',t,states=[],vars=set(),tech={'democracy'},is_country_alive=True,is_at_war=False,is_active_in_diplomatic_play=False)
  return w['countries'][t]
 # Use real ownership/province counts; economic positive fixtures deliberately isolate unlock logic.
 rows=data['rows'][:]
 states=parse(read(B/'common/history/states/00_states.txt')).get('STATES')
 for name in ['STATE_CAPE_COLONY','STATE_EASTERN_CAPE','STATE_NORTHERN_CAPE','STATE_ZULULAND','STATE_VRYSTAAT','STATE_TRANSVAAL','STATE_CEYLON','STATE_INDIAN_OCEAN_TERRITORY']:
  r=states.get('s:'+name);rs=[]
  for n in r.all('create_state'):rs.append({'tag':n.scalar('country')[2:],'provinces':len(n.get('owned_provinces').children)})
  rows.append({'region':name,'states':rs})
 for row in rows:
  r=Obj('state_region',row['region'],states=[]);w['regions'][r.name]=r
  # Sole-owner states certainly qualify as largest. Split-state largest is a test fixture flag, not a claim about engine criteria.
  for d in row['states']:
   c=country(d['tag']);st=Obj('state',r.name+':'+c.name,owner=c,controller=c,state_region=r,state_population=100000,num_provinces=d['provinces'],is_largest_state_in_region=len(row['states'])==1,buildings=[Obj('building','building_port',level=1),Obj('building','building_government_administration',level=1)])
   r.a['states'].append(st);c.a['states'].append(st)
 country('TRA').a['overlord']=country('USM');country('MUG').a['overlord']=country('FRA')
 return w

def captured(w,n,owner='USM',population=100000):
 r=w['regions'][n];c=w['countries'][owner]
 for old in r.a['states']:old.a['owner'].a['states'].remove(old)
 st=Obj('state',n+':'+owner,owner=c,controller=c,state_region=r,state_population=population,is_largest_state_in_region=True,buildings=[Obj('building','building_port',level=1),Obj('building','building_government_administration',level=1)])
 r.a['states']=[st];c.a['states'].append(st)
 return st

def eligible_world():
 w=world_from_history();u=w['countries']['USM'];u.a['tech'].add('civilizing_mission')
 names=['STATE_MADRAS','STATE_CIRCARS','STATE_KURNOOL','STATE_MYSORE','STATE_TRAVANCORE','STATE_GUJARAT','STATE_DELHI','STATE_AGRA','STATE_BIHAR','STATE_BOMBAY','STATE_SINDH','STATE_CENTRAL_PROVINCES']
 for n in names:captured(w,n)
 return w

def run(rootdir):
 cases=[]
 def check(name,w,key,expected):
  got=Evaluator(rootdir,w).test(key);cases.append({'name':name,'actual':got,'expected':expected,'pass':got==expected})
 w=world_from_history();check('Historical ownership with qualifying construction cannot found Tianzhu at era1',w,'nesnd_tianzhu_commission_ready',False)
 w['countries']['USM'].a['tech'].add('civilizing_mission');check('Technology alone without Indian expansion remains insufficient',w,'nesnd_tianzhu_commission_ready',False)
 w=eligible_world();check('Conquest route is reachable',w,'nesnd_tianzhu_commission_ready',True)
 return cases
if __name__=='__main__':
 import sys
 rootdir=B if '--baseline' in sys.argv else C
 cases=run(rootdir);dump(R/('gate-red.json' if rootdir==B else 'gate-green.json'),{'cases':cases,'scope':'Strict evaluation of actual ordered trigger AST with explicit world fixtures; not Jomini engine','history_input_sha':sha(B/'common/history/states/00_states.txt')})
 print(('FAIL' if any(not x['pass'] for x in cases) else 'PASS'),[(x['name'],x['actual']) for x in cases]);sys.exit(any(not x['pass'] for x in cases))
