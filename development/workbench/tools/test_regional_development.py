from regional_context import *
from test_commission_gate_behavior import Evaluator as Base,Obj,SimpleNamespace
from test_commission_effect_boundaries import EffectTrace as OldTrace
from copy import deepcopy
import re,itertools
TAGS=['PRU','AUS','TUR','EGY','MEX','USA','PEU']
J=parse(read(C/'common/journal_entries/nesnd_regional_development.txt'))
EV=parse(read(C/'events/nesnd_regional_development.txt'))
TR=parse(read(C/'common/scripted_triggers/nesnd_regional_development.txt'))
EF=parse(read(C/'common/scripted_effects/nesnd_regional_development.txt'))

def expand(node,args):
 n=deepcopy(node)
 for x in n.walk():
  for k,v in args.items():
   if x.key:x.key=x.key.replace('$'+k+'$',v)
   if x.value:x.value=x.value.replace('$'+k+'$',v)
 return n

class E(Base):
 def __init__(self,w):self.w=w;self.db={n.key:n for n in TR.children};self.reads=[];self.values={}
 def expr(self,n,o,root,prev):
  if n.key in self.db and n.children is not None:return self.block(expand(self.db[n.key],{x.key:x.value for x in n.children}),o,root,prev)
  if n.key in ['occupancy','literacy_rate','government_legitimacy','bureaucracy']:return self.cmp(o.a.get(n.key,0),n.op,float(n.value))
  if n.key=='game_date':return self.cmp(tuple(map(int,self.w['date'].split('.'))),n.op,tuple(map(int,n.value.split('.'))))
  if n.key.strip('"').startswith('scripted_bar_progress('):return self.cmp(o.a['progress'],n.op,float(n.value))
  return super().expr(n,o,root,prev)

class Trace(OldTrace):
 def __init__(self,w):self.w=w;self.pred=E(w);self.db={n.key:n for n in EF.children};self.trace=[]
 def effect(self,n,o,root,prev):
  if n.key in self.db:
   args={x.key:x.value for x in n.children or []};self.block(expand(self.db[n.key],args),o,root,prev);return
  if n.key=='hidden_effect':self.block(n,o,root,prev);return
  if n.key=='show_as_tooltip' or n.key in ['name','default_option','trigger','ai_chance']:return
  if n.key=='trigger_event':self.trace.append(('event',n.scalar('id')));return
  if n.key=='add_modifier':self.trace.append(('reward',n.scalar('name'),n.scalar('months')));o.a.setdefault('modifiers',set()).add(n.scalar('name'));return
  return super().effect(n,o,root,prev)

def world(tag):
 w={'countries':{},'regions':{},'saved':{},'date':'1845.1.1'}
 for t in TAGS+['GER','NGF','FRA']:
  w['countries'][t]=Obj('country',t,states=[],buildings=[],vars=set(),tech={'railways'},laws={'law_professional_army','law_slavery_banned','law_public_schools'},journals=set(),modifiers=set(),is_country_alive=True,is_at_war=False)
 for n in TR.walk():
  if n.value and n.value.startswith('s:'):w['regions'][n.value[2:]]=Obj('region',n.value[2:],states=[])
 a=w['countries'][tag];a.a['vars']|={'hungarian_acceptance_var','sick_man_complete'}
 def st(region,buildings):
  r=w['regions'].setdefault(region,Obj('region',region,states=[]));s=Obj('state',region,owner=a,state_region=r,buildings=[]);r.a['states'].append(s);a.a['states'].append(s)
  for typ,level in buildings:
   b=Obj('building','building_'+typ,owner=a,state=s,level=level,occupancy=.75);s.a['buildings'].append(b);a.a['buildings'].append(b)
 data={
 'PRU':[('STATE_BRANDENBURG',[('railway',1),('tooling_workshop',3)]),('STATE_LOWER_SILESIA',[('railway',1)])],
 'AUS':[('STATE_AUSTRIA',[('government_administration',3)]),('STATE_BOHEMIA',[('university',2)])],
 'TUR':[('STATE_EASTERN_THRACE',[('government_administration',3)]),('STATE_OTHER',[('port',3)])],
 'EGY':[('STATE_LOWER_EGYPT',[('port',2),('textile_mill',3)]),('STATE_MIDDLE_EGYPT',[])],
 'MEX':[('STATE_MEXICO',[('government_administration',2),('tooling_workshop',2)]),('STATE_VERACRUZ',[('port',1)])],
 'USA':[('STATE_VIRGINIA',[('university',2)]),('STATE_GEORGIA',[('railway',2)])],
 'PEU':[('STATE_LIMA',[('port',2),('iron_mine',3)]),('STATE_AREQUIPA',[('railway',1)])]}
 for name,bs in data[tag]:st(name,bs)
 je=Obj('journal','nesnd_rg_'+tag.lower(),owner=a,progress=12);w['saved']['journal_entry']=je
 return w,a,je

rows=[]
def ck(name,f):
 try:f();rows.append({'name':name,'pass':True})
 except Exception as e:rows.append({'name':name,'pass':False,'error':repr(e)})
def require(b):assert b
for i,tag in enumerate(TAGS,1):
 slug=tag.lower();journal=J.get('nesnd_rg_'+slug);ready='nesnd_rg_'+slug+'_ready';entry='nesnd_rg_'+slug+'_entry'
 def base(tag=tag,entry=entry,ready=ready,journal=journal):
  w,a,je=world(tag);e=E(w);require(e.test(entry,tag));require(e.test(ready,tag));require(e.block(journal.get('complete'),a,a));je.a['progress']=11;require(not e.block(journal.get('complete'),a,a))
 ck(tag+'_entry_ready_and_11_vs_12_months',base)
 for occupancy in [.74,.75]:
  def case(tag=tag,ready=ready,occupancy=occupancy):
   w,a,je=world(tag)
   for b in a.a['buildings']:b.a['occupancy']=occupancy
   require(E(w).test(ready,tag)==(occupancy>=.75))
  ck(tag+'_occupancy_'+str(occupancy),case)
 def shortages(tag=tag,ready=ready):
  w,a,je=world(tag);a.a['is_at_war']=True;require(not E(w).test(ready,tag));a.a['is_at_war']=False
  for b in a.a['buildings']:b.a['level']=0
  require(not E(w).test(ready,tag))
 ck(tag+'_war_or_empty_buildings_pause',shortages)
 def ownership(tag=tag,ready=ready):
  w,a,je=world(tag);a.a['states']=[];a.a['buildings']=[];require(not E(w).test(ready,tag))
 ck(tag+'_foreign_buildings_do_not_count',ownership)
 def terminal(tag=tag,journal=journal):
  for hook in ['on_fail','on_timeout','on_invalid']:
   w,a,je=world(tag);t=Trace(w);t.block(journal.get(hook),a,a);t.block(journal.get(hook),a,a)
   require('nesnd_rg_closed' in a.a['vars']);require(not E(w).test('nesnd_rg_open',tag));require(len([x for x in t.trace if x[0]=='event'])<2)
 ck(tag+'_all_terminal_paths_once',terminal)
 for optidx in [0,1]:
  def reward(tag=tag,journal=journal,i=i,optidx=optidx):
   w,a,je=world(tag);t=Trace(w);t.block(journal.get('on_complete'),a,a);t.block(journal.get('on_complete'),a,a)
   require(len([x for x in t.trace if x[0]=='event'])==1)
   opt=EV.get('nesnd_regional.'+str(i)).all('option')[optidx];require(t.pred.block(opt.get('trigger'),a,a))
   t.block(opt,a,a);t.block(opt,a,a);require(len([x for x in t.trace if x[0]=='reward'])==1)
   require(not t.pred.block(EV.get('nesnd_regional.'+str(i)).all('option')[1-optidx].get('trigger'),a,a))
   require('nesnd_rg_pending' not in a.a['vars'])
  ck(tag+'_choice_'+str(optidx)+'_single_reward',reward)
 def late(tag=tag,journal=journal,i=i):
  w,a,je=world(tag);t=Trace(w);t.block(journal.get('on_complete'),a,a);a.a['num_states']=1
  ev=EV.get('nesnd_regional.'+str(i));require(not t.pred.block(ev.all('option')[0].get('trigger'),a,a));require(t.pred.block(ev.all('option')[2].get('trigger'),a,a));t.block(ev.all('option')[2],a,a)
  require(not any(x[0]=='reward' for x in t.trace));require('nesnd_rg_pending' not in a.a['vars'])
 ck(tag+'_late_collapse_has_explicit_no_reward_exit',late)

def phases():
 for tag in ['PRU','AUS','EGY','MEX','USA']:
  w,a,je=world(tag);w['date']='1836.1.1';require(not E(w).test('nesnd_rg_'+tag.lower()+'_entry',tag))
 for tag,var in [('AUS','hungarian_acceptance_var'),('TUR','sick_man_complete')]:
  w,a,je=world(tag);a.a['vars'].discard(var);require(not E(w).test('nesnd_rg_'+tag.lower()+'_entry',tag))
 w,a,je=world('USA');a.a['laws'].discard('law_slavery_banned');require(not E(w).test('nesnd_rg_usa_entry','USA'))
 w,a,je=world('AUS');a.a['journals'].add('je_matter_of_hungary');require(not E(w).test('nesnd_rg_aus_entry','AUS'))
ck('phase_gates_not_startup_or_absent_prerequisite',phases)
def prussian_origin():
 w,a,je=world('PRU');a.a['vars'].add('nesnd_rg_prussian_origin');w['countries']['GER']=a;del w['countries']['PRU'];require(E(w).test('nesnd_rg_pru_entry','GER'))
 a.a['vars'].clear();require(not E(w).test('nesnd_rg_pru_entry','GER'))
ck('same_country_unification_but_not_unrelated_germany',prussian_origin)
def low_states():
 for tag in TAGS:
  w,a,je=world(tag);a.a['num_states']=1;e=E(w);j=J.get('nesnd_rg_'+tag.lower());require(not e.block(j.get('complete'),a,a));require(e.block(j.get('fail'),a,a))
ck('collapse_and_completion_mutually_exclusive',low_states)
def mutation():
 w,a,je=world('PRU');t=Trace(w);t.block(J.get('nesnd_rg_pru').get('on_complete'),a,a)
 t.db['nesnd_rg_reward'].get('if').get('limit').children=[]
 opt=EV.get('nesnd_regional.1').all('option')[0];t.block(opt,a,a);t.block(opt,a,a)
 require(len([x for x in t.trace if x[0]=='reward'])==2)
ck('negative_control_removed_guard_detects_duplicate_reward',mutation)

# Lifecycle ordering regression: an already-completed duplicate JE must not destroy its event ticket.
def archive_after_success():
 w,a,je=world('PRU');t=Trace(w);j=J.get('nesnd_rg_pru');t.block(j.get('on_complete'),a,a);t.block(j.get('on_invalid'),a,a)
 require('nesnd_rg_pending' in a.a['vars'])
ck('invalid_duplicate_cannot_erase_completed_reward_ticket',archive_after_success)
def bar_cycles():
 bar=parse(read(C/'common/scripted_progress_bars/nesnd_regional_development.txt')).get('nesnd_rg_work')
 val=bar.get('monthly_progress').get('add').get('value')
 for tag in TAGS:
  w,a,je=world(tag);e=E(w);je.a['progress']=0
  for month in range(6):je.a['progress']+=e.value_block(val,je,je,None)
  require(je.a['progress']==6);a.a['is_at_war']=True
  for month in range(3):je.a['progress']+=e.value_block(val,je,je,None)
  require(je.a['progress']==6);a.a['is_at_war']=False
  for month in range(6):je.a['progress']+=e.value_block(val,je,je,None)
  require(je.a['progress']==12)
 require(not any(x.key in ['change_variable','set_bar_progress','add_progress'] for x in EF.walk()))
ck('native_monthly_arithmetic_7_countries_pause_resume_single_writer',bar_cycles)
def missing_tag():
 w,a,je=world('PRU');del w['countries']['PRU'];e=E(w)
 require(not e.block(TR.get('nesnd_rg_pru_identity'),a,a))
 t=Trace(w);a.a['vars']|={'nesnd_rg_closed','nesnd_rg_pending'};t.block(J.get('nesnd_rg_pru').get('on_invalid'),a,a)
 require('nesnd_rg_pending' not in a.a['vars'])
ck('identity_change_archives_ticket_without_untyped_country',missing_tag)
def display_matches_award():
 for i in range(1,8):
  for opt in EV.get('nesnd_regional.'+str(i)).all('option')[:2]:
   preview=opt.get('show_as_tooltip').get('add_modifier');call=opt.get('hidden_effect').get('nesnd_rg_reward')
   require(preview.scalar('name')==call.scalar('MODIFIER'));require(preview.scalar('months')==EF.get('nesnd_rg_reward').get('if').get('add_modifier').scalar('months'))
ck('all_14_choice_previews_match_execution_and_duration',display_matches_award)
phase=sys.argv[1] if len(sys.argv)>1 else 'candidate'
dump(R/('regional-behavior-'+phase+'.json'),{'pass':all(x['pass'] for x in rows),'checks':rows,'source_files':man(C),'engine_verified':False,'limit':'Real ordered script AST with explicit native API fixtures, no engine scheduling or rendered UI certification'})
print('PASS',sum(x['pass'] for x in rows),'FAIL',sum(not x['pass'] for x in rows))
for x in rows:
 if not x['pass']:print(x)
sys.exit(not all(x['pass'] for x in rows))
