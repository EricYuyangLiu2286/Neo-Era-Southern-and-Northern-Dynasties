from sweep_context import *
from test_commission_gate_behavior import Evaluator as Base,Obj,SimpleNamespace
from test_commission_effect_boundaries import EffectTrace as BaseTrace
from copy import deepcopy
import re,itertools

class E(Base):
 def __init__(self,w):
  super().__init__(C,w);self.values={n.key:n for p in (C/'common/script_values').glob('*.txt') for n in parse(read(p)).children}
 def scope(self,k,o,root,prev):
  if k.startswith('je:'):
   if k[3:] not in o.a.get('journals',set()):return None
   return self.w.setdefault('jes',{}).setdefault((o.name,k[3:]),Obj('journal',k[3:],owner=o))
  return super().scope(k,o,root,prev)
 def expr(self,n,o,root,prev):
  k,v=n.key,n.value
  if k=='has_global_variable':return v in self.w.get('globals',set())
  if k=='nesnd_per_claim_obstructor':return o.a.get('obstructs',False)==(v=='yes') # existing diplomacy predicate is an explicit boundary fixture
  if k=='is_adjacent_to_state':return self.scope(v,o,root,prev).name in o.a.get('adjacent',set())
  if k=='has_claim_by':return self.scope(v,o,root,prev).name in o.a['state_region'].a.get('claims',set())
  if k=='game_date':return self.cmp(self.w['date'],n.op,v)
  if k in ['army_size','army_power_projection','gdp_ranking','government_legitimacy','literacy_rate'] or k.startswith('relations('):return self.cmp(o.a.get(k,0),n.op,self.number(v,o,root,prev))
  if k=='country_rank':return self.cmp(o.a.get(k,1),n.op,{'rank_value:major_power':5,'rank_value:unrecognized_major_power':3}.get(v,float(v) if v.isdigit() else -100))
  if k in ['nesnd_per_civil_ready','nesnd_per_economy_ready']:return o.a.get(k,False)==(v=='yes') # construction fixture, separately preserved original predicate
  if k=='is_incorporated':return o.a.get('incorporated',False)==(v=='yes')
  if k=='owns_entire_state_region':
   states=self.w['regions'][v].a.get('states',[]);return bool(states) and all(s.a['owner'] is o for s in states)
  if k.startswith('var:'):return self.cmp(self.scope(k,o,root,prev),n.op,self.number(v,o,root,prev))
  return super().expr(n,o,root,prev)
 def number(self,t,o,root,prev):
  if t.startswith('nesnd_qe1_sol_') and t.endswith(('_n','_s','_f')):return o.a['cohort'][t[-1]]
  return super().number(t,o,root,prev)
 def value_block(self,n,o,root,prev,current=0):
  chain=None
  for x in n.children or []:
   if x.key=='limit':continue
   if x.key=='if':
    chain=self.block(x.get('limit'),o,root,prev)
    if chain:current=self.value_block(x,o,root,prev,current)
   elif x.key in ['else','else_if']:
    assert chain is not None
    if not chain:
     yes=x.key=='else' or self.block(x.get('limit'),o,root,prev)
     if yes:current=self.value_block(x,o,root,prev,current)
     chain=yes
   elif x.key=='every_country':
    for q in self.w['countries'].values():
     if self.block(x.get('limit'),q,root,o):current=self.value_block(x,q,root,o,current)
   else:
    chain=None;val=self.value_block(x,o,root,prev) if x.children else self.number(x.value,o,root,prev)
    if x.key=='value':current=val
    elif x.key=='add':current+=val
    elif x.key=='subtract':current-=val
    elif x.key=='multiply':current*=val
    elif x.key=='divide':current/=val
    elif x.key=='min':current=max(current,val)
    elif x.key=='max':current=min(current,val)
    else:raise AssertionError(('unknown arithmetic',x.key))
  return current

class Trace(BaseTrace):
 def __init__(self,w):super().__init__(w,C);self.pred=E(w)
 def effect(self,n,o,root,prev):
  k,v=n.key,n.value
  if k=='save_scope_as':self.w.setdefault('saved',{})[v]=o;return
  if k=='clear_saved_scope':self.w.setdefault('saved',{}).pop(v,None);return
  if k=='add_claim':o.a.setdefault('claims',set()).add(self.pred.scope(v,o,root,prev).name);self.trace.append(('claim',o.name));return
  if k=='set_variable':
   name=v or n.scalar('name');o.a.setdefault('vars',set()).add(name)
   q=n.get('value')
   if q:o.a.setdefault('variable_values',{})[name]=self.pred.value_block(q,o,root,prev) if q.children else self.pred.number(q.value,o,root,prev)
   return
  if k=='change_variable':
   name=n.scalar('name');assert name in o.a['vars'],('uninitialized variable',name)
   o.a['variable_values'][name]+=self.pred.number(n.scalar('add'),o,root,prev);return
  if k=='clamp_variable':
   name=n.scalar('name');o.a['variable_values'][name]=min(float(n.scalar('max')),max(float(n.scalar('min')),o.a['variable_values'][name]));return
  if k=='add_modifier':o.a.setdefault('modifiers',set()).add(n.scalar('name'));self.trace.append(('modifier',o.name,n.scalar('name'),n.scalar('months')));return
  if k=='set_bar_progress':o.a['bar']=self.pred.number(n.scalar('value'),o,root,prev);return
  if k=='set_state_type':o.a['incorporated']=v=='incorporated';self.trace.append(('incorporate',o.name));return
  if k=='every_scope_state':
   for st in o.a['states'][:]:
    if n.get('limit') is None or self.pred.block(n.get('limit'),st,root,o):self.block(SimpleNamespace(children=[q for q in n.children if q.key!='limit']),st,root,o)
   return
  if k=='every_country':
   for country in self.w['countries'].values():
    if self.pred.block(n.get('limit'),country,root,o):self.block(SimpleNamespace(children=[q for q in n.children if q.key!='limit']),country,root,o)
   return
  if k=='add_radicals':self.trace.append(('radicals',o.name,n.scalar('culture'),float(n.scalar('value'))));return
  if k=='add_radicals_in_state':self.trace.append(('radicals_state',o.name,n.scalar('pop_type'),self.pred.value_block(n.get('value'),o,root,prev)));return
  if k=='trigger_event':self.trace.append(('event',o.name,n.scalar('id')));return
  if k=='hidden_effect':self.block(n,o,root,prev);return
  if k in ['show_as_tooltip','custom_tooltip']:return
  if k in self.db and n.children:
   body=deepcopy(self.db[k]);args={q.key:q.value for q in n.children}
   for q in body.walk():
    for key,value in args.items():
     if q.key:q.key=q.key.replace('$'+key+'$',value)
     if q.value:q.value=q.value.replace('$'+key+'$',value)
   self.block(body,o,root,prev);return
  return super().effect(n,o,root,prev)

def world(date='1849.12.31'):
 w={'countries':{},'regions':{},'saved':{},'globals':{'usm_civilwar_occured'},'date':date}
 for tag in ['PER','QE1','FRA','USM','SIH']:
  w['countries'][tag]=Obj('country',tag,vars=set(),variable_values={},states=[],is_country_alive=True,army_size=50,army_power_projection=100,gdp_ranking=20,country_rank=5,journals=set(),modifiers=set())
 u=w['countries']['USM'];u.a['vars'].add('tag_WUU_var')
 # All named state regions exist, as in the actual game; only fixture owner-states are created below.
 for p in (C/'common/scripted_triggers').glob('*.txt'):
  for n in parse(read(p)).walk():
   for token in [n.key,n.value]:
    if token and token.startswith('s:'):w['regions'].setdefault(token[2:].split('.')[0],Obj('region',token[2:].split('.')[0],states=[]))
 return w
def state(w,name,owner='USM',inc=False):
 o=w['countries'][owner];r=w['regions'].setdefault(name,Obj('region',name,states=[]));s=Obj('state',name+':'+owner,owner=o,controller=o,state_region=r,incorporated=inc,vars=set(),variable_values={});r.a['states'].append(s);o.a['states'].append(s);return s
rows=[]
def ck(name,f):
 try:f();rows.append({'name':name,'pass':True})
 except Exception as e:rows.append({'name':name,'pass':False,'detail':repr(e)})
def require(x):assert x

for qe,fra,relationship,want in [(True,True,30,2),(True,True,-30,.5),(False,True,0,1),(False,False,0,1)]:
 def case(qe=qe,fra=fra,relationship=relationship,want=want):
  w=world();p=w['countries']['PER'];p.a['relations(c:QE1)']=relationship
  if not qe:del w['countries']['QE1']
  if not fra:del w['countries']['FRA']
  require(E(w).number('nesnd_per_governance_delta',p,p,None)==want)
  require(E(w).number('nesnd_per_claim_reference',p,p,None)==(.5 if qe or fra else 0))
 ck(f'currency_missing_countries_{qe}_{fra}_{relationship}',case)

buttons=parse(read(C/'common/scripted_buttons/nesnd_per_resources.txt'))
for kind,cost in [('civil',20),('industry',40),('education',20),('legislation',20)]:
 for points in [0,cost-1,cost,cost+20]:
  def case(kind=kind,cost=cost,points=points):
   w=world();p=w['countries']['PER'];p.a['journals'].add('nesnd_per_governance');p.a['currently_enacting_law']=Obj('law','law')
   t=Trace(w);t.call('nesnd_per_resources_initialize',p);p.a['variable_values']['nesnd_per_governance_points']=points
   # currently_enacting_law is a real link supplied by the fixture; extend only this link.
   old=t.pred.scope;t.pred.scope=lambda k,o,r,pr:o.a.get(k) if k=='currently_enacting_law' else old(k,o,r,pr)
   effect=buttons.get('nesnd_per_'+kind+'_grant_button').get('effect');t.block(effect,p,p)
   expected=points-cost if points>=cost else points;require(p.a['variable_values']['nesnd_per_governance_points']==expected)
   t.block(effect,p,p);require(p.a['variable_values']['nesnd_per_governance_points']==expected)
   require(('nesnd_per_'+kind+'_grant' in p.a['modifiers'])==(points>=cost))
  ck(f'purchase_{kind}_{points}_no_repeat',case)

def clamp():
 w=world();p=w['countries']['PER'];p.a['journals'].add('nesnd_per_governance');t=Trace(w);t.call('nesnd_per_resources_initialize',p)
 p.a['variable_values']['nesnd_per_governance_points']=99.5;t.call('nesnd_per_governance_monthly',p);require(p.a['variable_values']['nesnd_per_governance_points']==100)
 p.a.update(is_at_war=True,in_default=True);p.a['relations(c:QE1)']=-50;p.a['variable_values']['nesnd_per_governance_points']=0;t.call('nesnd_per_governance_monthly',p);require(p.a['variable_values']['nesnd_per_governance_points']==0)
ck('governance_clamps_both_endpoints',clamp)
def sources_match():
 values=parse(read(C/'common/script_values/nesnd_per_resources.txt'));bars=parse(read(C/'common/scripted_progress_bars/nesnd_per_resources.txt'))
 for prefix,bar in [('nesnd_per_governance','nesnd_per_governance_bar'),('nesnd_per_claim','nesnd_per_claim_resource_bar')]:
  formula=[x.value for x in values.get(prefix+'_delta').children]
  shown=[x.scalar('value').removeprefix('owner.') for x in bars.get(bar).get('monthly_progress').all('add')]
  require(formula==shown)
ck('periodic_tooltip_components_equal_actual_arithmetic',sources_match)
def claim_tick():
 w=world();p=w['countries']['PER'];p.a['vars']|={'nesnd_per_future_done','nesnd_per_route_aid','nesnd_per_route_covert'};p.a['journals'].add('nesnd_per_west_journal')
 t=Trace(w);t.call('nesnd_per_resources_initialize',p);require(not t.pred.test('nesnd_per_east_eligible','PER'))
 p.a['variable_values']['nesnd_per_claim_points']=99;t.call('nesnd_per_claim_monthly',p)
 require(p.a['variable_values']['nesnd_per_claim_points']==100 and w['jes'][('PER','nesnd_per_west_journal')].a['bar']==100)
ck('claim_bar_cap_sync_and_exclusive_route',claim_tick)

def geography():
 w=world();ordinary=state(w,'STATE_HUNAN');exceptions=[state(w,x) for x in ['STATE_SICHUAN','STATE_XIANGYANG','STATE_GUILIN']];island=state(w,'STATE_FORMOSA');foreign=state(w,'STATE_KYOTO')
 w['countries']['USM'].a['vars'].add('nesnd_usm_western_migrated')
 t=Trace(w);t.call('nesnd_usm_integrate_recovered_mainland',w['countries']['USM'])
 require(ordinary.a['incorporated']);require(not any(x.a['incorporated'] for x in exceptions+[island,foreign]));require('nesnd_usm_western_provinces' in w['countries']['USM'].a['journals'])
ck('mainland_only_preserves_three_exceptions_and_foreign_states',geography)

for bits in itertools.product([False,True],repeat=3):
 def case(bits=bits):
  w=world()
  for name,inc in zip(['STATE_SICHUAN','STATE_XIANGYANG','STATE_GUILIN'],bits):state(w,name,inc=inc)
  require(E(w).test('nesnd_usm_western_integrated','USM')==all(bits))
 ck('three_province_incorporation_'+str(bits),case)
def split():
 w=world()
 for name in ['STATE_SICHUAN','STATE_XIANGYANG','STATE_GUILIN']:state(w,name,inc=True)
 state(w,'STATE_SICHUAN','SIH',True);require(not E(w).test('nesnd_usm_western_integrated','USM'))
ck('foreign_fragment_prevents_completion',split)

for date,penalty in [('1849.12.31',False),('1850.1.1',True),('1851.1.1',True)]:
 def case(date=date,penalty=penalty):
  w=world(date);u=w['countries']['USM'];u.a['vars'].add('nesnd_usm_western_opened');t=Trace(w);t.call('nesnd_usm_western_fail',u);t.call('nesnd_usm_western_fail',u)
  rad=[x for x in t.trace if x[0]=='radicals'];require(len(rad)==(4 if penalty else 0))
  if penalty:require({x[2] for x in rad}=={'cu:ce_chu','cu:ce_xinan','cu:hakka','cu:yue'} and all(x[3]==.25 for x in rad));require('nesnd_usm_western_finished' in u.a['vars'])
 ck('deadline_and_single_culture_penalty_'+date,case)

def sol():
 w=world();u=w['countries']['USM'];st=state(w,'STATE_HUNAN');st.a['cohort']={'n':100,'s':1000,'f':5};t=Trace(w)
 call=parse('nesnd_usm_western_sample_cohort = { TYPE = laborers N = nesnd_qe1_sol_laborers_n S = nesnd_qe1_sol_laborers_s F = nesnd_qe1_sol_laborers_f PREVIOUS = nesnd_west_sol_laborers }').children[0]
 t.effect(call,st,u,u);require(not t.trace)
 st.a['cohort']['s']=900;t.effect(call,st,u,u);require(abs(t.trace[-1][3]-.005)<1e-9)
 st.a['cohort']['s']=1100;before=len(t.trace);t.effect(call,st,u,u);require(len(t.trace)==before)
 t.call('nesnd_usm_western_clear_observation',u);require('nesnd_west_sol_laborers' not in st.a['vars'])
ck('sol_first_sample_then_decline_only_and_cleanup',sol)

def legacy():
 w=world('1851.1.1');u=w['countries']['USM']
 for name in ['STATE_SICHUAN','STATE_XIANGYANG','STATE_GUILIN']:state(w,name,inc=True)
 require(not E(w).test('nesnd_usm_western_eligible','USM'))
 t=Trace(w);t.call('nesnd_usm_western_maintenance',u)
 require('nesnd_usm_western_succeeded' in u.a['vars'] and 'nesnd_usm_western_provinces' not in u.a['journals'])
 t.call('nesnd_usm_western_fail',u);require(not any(x[0]=='radicals' for x in t.trace))
ck('legacy_success_is_preserved_before_any_je_or_weekly_order',legacy)
for points,adjacent,blocked in [(0,True,False),(24,True,False),(25,True,False),(50,True,True),(25,False,False)]:
 def case(points=points,adjacent=adjacent,blocked=blocked):
  w=world();p=w['countries']['PER'];st=state(w,'STATE_SYRIA','SIH');p.a['adjacent']={st.name} if adjacent else set()
  w['saved']={'nesnd_per_claim_state':st,'nesnd_per_claim_region':st.a['state_region']};w['countries']['FRA'].a['obstructs']=blocked
  t=Trace(w);t.call('nesnd_per_resources_initialize',p);p.a['variable_values']['nesnd_per_claim_points']=points
  t.call('nesnd_per_attempt_claim',p)
  paid=points>=25 and adjacent;require(p.a['variable_values']['nesnd_per_claim_points']==points-(25 if paid else 0))
  require(('PER' in st.a['state_region'].a.get('claims',set()))==(paid and not blocked))
  t.call('nesnd_per_attempt_claim',p);require(p.a['variable_values']['nesnd_per_claim_points']==points-(25 if paid else 0))
 ck(f'claim_cost_{points}_adjacent{adjacent}_blocked{blocked}',case)

def no_unopened_failure():
 w=world('1851.1.1');t=Trace(w);t.call('nesnd_usm_western_fail',w['countries']['USM']);require(not t.trace)
ck('unopened_journal_cannot_apply_deadline_penalty',no_unopened_failure)

def annex_origin():
 w=world();q=w['countries']['SIH'];st=state(w,'STATE_KYOTO','SIH');t=Trace(w)
 t.call('nesnd_usm_mark_annex_origin',q);require('nesnd_usm_annex_had_mainland' not in q.a['vars'])
 state(w,'STATE_SICHUAN','SIH');t.call('nesnd_usm_mark_annex_origin',q);require('nesnd_usm_annex_had_mainland' in q.a['vars'])
 q.a['states']=[st];t.call('nesnd_usm_mark_annex_origin',q);require('nesnd_usm_annex_had_mainland' not in q.a['vars'])
ck('annex_origin_marks_mainland_but_not_overseas_or_stale_flag',annex_origin)

def callback_routes():
 w=world();p=w['countries']['PER'];p.a['vars']|={'nesnd_per_future_done','nesnd_per_route_aid','nesnd_per_route_covert'}
 p.a['journals']|={'nesnd_per_west_journal','nesnd_per_east_journal'};t=Trace(w);t.call('nesnd_per_resources_initialize',p)
 expected=t.pred.number('nesnd_per_claim_delta',p,p,None)
 js=parse(read(C/'common/journal_entries/nesnd_per_campaign.txt'))
 for name in ['nesnd_per_west_journal','nesnd_per_east_journal']:t.block(js.get(name).get('on_monthly_pulse').get('effect'),p,p,None)
 require(p.a['variable_values']['nesnd_per_claim_points']==expected)
ck('lingering_invalid_route_cannot_double_monthly_resource',callback_routes)

dump(R/'mechanism-tests.json',{'pass':all(x['pass'] for x in rows),'checks':rows,'source_files':man(C),'engine_verified':False,'scope':'Actual trigger/value/effect AST with explicit native operation mocks. Does not certify event ordering, real population changes, or engine UI.'})
print('PASS',sum(x['pass'] for x in rows),'FAIL',sum(not x['pass'] for x in rows))
for x in rows:
 if not x['pass']:print(x)
sys.exit(not all(x['pass'] for x in rows))
