from canon_routes_context import *
import math,copy,traceback
src=(W/'tools/test_b2r2_routes.py').read_text();exec(src[:src.rindex('\ntry:\n check(')],globals())
# Fill actual source definitions; no rewritten B2 predicates are inserted.
for folder,kind in [('common/scripted_triggers','trigger'),('common/script_values','value')]:
 for p in sorted((snap/folder).glob('*.txt')):
  for n in parse(read(p)).children or []:
   key=n.key.removeprefix('REPLACE:') if n.key else None
   if key and key not in defs:defs[key]=(kind,n,p.relative_to(snap).as_posix())
props.add('market')
building_aliases=json.loads((run/'b2-effective-building-aliases.json').read_text('utf-8'))
base_resolve=resolve;base_scalar=scalar;base_iterator=iterator_items
facts={'gdp','net_fixed_income','state_population','state_unemployment_rate','market_access','level','occupancy','weekly_profit','government_legitimacy','literacy_rate','bureaucracy','army_size','liberty_desire','average_sol','turmoil'}
def resolve(token,stack):
 t=subst(token)
 if t in facts:return getattr(stack[-1],t)
 if t.startswith('ig:'):return stack[-1].igs.get(t[3:])
 return base_resolve(token,stack)
x['resolve']=resolve;x['ns']['resolve']=resolve

def iterator_items(key,node,cur):
 if key=='any_political_movement':return cur.movements
 if key=='any_interest_group':return list(cur.igs.values())
 if key=='any_scope_pop':return getattr(cur,'pops',[])
 return base_iterator(key,node,cur)
def scalar(n,stack):
 k=subst(n.key);v=subst(n.value);cur=stack[-1]
 if k=='is_building_type':return building_aliases.get(cur.building_type,cur.building_type)==building_aliases.get(v,v)
 if k=='market.owner':
  target=resolve(k,stack)
  if n.children is not None:
   if target is None:raise Unsupported('unguarded market.owner scope')
   return x['triggers'](n.children,stack+[target])
  return cmp[n.op](target,resolve(v,stack))
 if k in ['has_law','has_law_or_variant']:return v.removeprefix('law_type:') in cur.laws
 if k=='has_technology_researched':return v in cur.techs
 if k in ['has_revolution','is_subsidized','building_has_goods_shortage','is_active_in_diplomatic_play']:
  attr={'building_has_goods_shortage':'shortage'}.get(k,k);return bool(getattr(cur,attr,False))==(v=='yes')
 if k=='is_political_movement_type':return cur.movement_type==v
 if k=='has_diplomatic_pact':
  who=resolve(child(n,'who').value,stack);typ=subst(child(n,'type').value);initiator=child(n,'is_initiator');direction=subst(initiator.value)=='yes' if initiator else None
  return any(other is who and kind==typ and (direction is None or first==direction) for kind,other,first in cur.pact_facts)
 return base_scalar(n,stack)
x['scalar']=scalar;x['ns']['scalar']=scalar

def calculate(nodes,stack,acc=0):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key)
  if k=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:acc=calculate(body(chosen),stack,acc)
  elif k in ['value','add','subtract','multiply','divide','min','max']:
   v=calculate(n.children,stack) if n.children is not None else x['number'](n.value,stack)
   if k=='value':acc=v
   elif k=='add':acc+=v
   elif k=='subtract':acc-=v
   elif k=='multiply':acc*=v
   elif k=='divide':acc/=v
   elif k=='min':acc=max(acc,v)
   elif k=='max':acc=min(acc,v)
  elif k in ['round','ceiling','floor']:
   if subst(n.value)!='yes':raise Unsupported('unexpected rounding')
   acc=math.ceil(acc) if k=='ceiling' else math.floor(acc) if k=='floor' else math.floor(acc+0.5)
  elif k.startswith('every_'):
   key='any_'+k[6:];items=list(world.values()) if k=='every_country' else iterator_items(key,n,stack[-1]);limit=child(n,'limit')
   for obj in items:
    if x['triggers'](limit.children if limit else [],stack+[obj]):acc=calculate(body(n),stack+[obj],acc)
  elif k in props or k in ['prev','root'] or k.startswith(('var:','scope:','c:')):
   obj=resolve(k,stack)
   if obj is None:
    if n.op=='?=':continue
    raise Unsupported('null numeric scope '+k)
   acc=calculate(n.children,stack+[obj],acc)
  else:raise Unsupported('numeric node '+str(k))
 return acc
x['calculate']=calculate

def fixture():
 reset();a=new_country('ACE');a.techs={'democracy'};a.movements=[];a.igs={};a.pact_facts=[];a.has_revolution=False;a.gdp=100000;a.net_fixed_income=100;a.bureaucracy=0;a.government_legitimacy=50;a.literacy_rate=.3
 a.laws={'law_oligarchy'};a.market=Entity('market','ace-market',owner=a)
 reg=region('STATE_ACEH');land=state(a,'STATE_ACEH',reg);land.region=region('region_indonesia');land.state_population=100000;land.market_access=1;land.state_unemployment_rate=0;land.average_sol=12;land.turmoil=0;land.pops=[]
 for c in world.values():
  if not hasattr(c,'techs'):c.techs=set();c.movements=[];c.igs={};c.pact_facts=[];c.has_revolution=False
 return a,land

def stale_episode():
 a,land=fixture();m=Entity('movement','liberal',movement_type='movement_liberal');a.movements=[m]
 a.variables.update(nesnd_small_episode_active=True,nesnd_small_episode_serial=1,nesnd_small_episode_issue=3)
 saved.update(small_episode_serial=1,small_episode_regime=val('nesnd_canon_regime',a));a.variables['nesnd_small_episode_regime']=saved['small_episode_regime']
 assert 'nesnd_small_episode_clock' not in a.variables
 active=trig('nesnd_small_episode_valid',a);event=defs['nesnd_small_states.10'][1];organise=next(o for o in event.children if o.key=='option' and child(o,'name').value=='nesnd_small_states.10.organise')
 return {'clock_present':False,'actual_episode_valid':active,'actual_organise_option_available':x['triggers'](child(organise,'trigger').children,[a]),'actual_cancellation':x['triggers'](child(event,'cancellation_trigger').children,[a]),'expected_valid':False,'source_duration_months':child(event,'duration').value}

def stale_market():
 a,land=fixture();f=world['FRA'];a.pact_facts=[('grant_own_market',f,False)]
 a.variables.update(nesnd_small_market_verifying=True,nesnd_small_verification_partner=f,nesnd_small_verification_regime=val('nesnd_canon_regime',a),nesnd_small_verification_partner_regime=val('nesnd_canon_regime',f))
 assert 'nesnd_small_market_verification' not in a.variables
 valid=trig('nesnd_small_market_verification_valid',a);eff('nesnd_small_market_verify',a)
 return {'clock_present':False,'actual_contract_valid':valid,'actual_current_market_owner':'ACE','actual_notifications':list(x['notifications']),'expected_notification':'nesnd_canon_diplomacy.3'}

def kind5():
 a,land=fixture();f=world['FRA'];a.relations['FRA']=30;f.relations['ACE']=30
 eff('nesnd_canon_send_request',a,'TAG = FRA KIND = 5');event=next(e for e in captured_events if e['event']=='nesnd_canon_diplomacy.1');saved.clear();saved.update(event['scopes'])
 assert trig('nesnd_canon_reply_valid',f) and trig('nesnd_canon_request_eligible',f)
 eff('nesnd_canon_accept_request',f)
 return {'actual_small_country':trig('nesnd_small_state_country',a),'investor':a.variables.get('nesnd_canon_investor').tag,'actual_modifiers':list(a.modifiers),'notifications':list(x['notifications']),'dependency_stub_used':False}

def imperial_marker():
 a,land=fixture();a.variables['nesnd_india_imperial_line']=True
 return {'tag':'ACE','actual_region':'region_indonesia','imperial_line':True,'actual_india_empire_helper':trig('nesnd_india_empire',a),'actual_small_country':trig('nesnd_small_state_country',a),'expected_small_country':False}

def late_promise_branch():
 a,land=fixture();a.variables.update(nesnd_small_episode_active=True,nesnd_small_episode_serial=1,nesnd_small_episode_issue=3,nesnd_small_episode_choice=2,nesnd_small_promise=5,nesnd_small_episode_regime=val('nesnd_canon_regime',a));a.laws={'law_wealth_voting'}
 node=defs['nesnd_small_episode_monthly'][1];outer=child(node,'if');chosen,index=x['selected_branches'](body(outer),0,[a],'if')
 return {'clock_present':False,'target_law_now_enacted':trig('nesnd_small_promised_law',a),'selected_branch':chosen.key,'first_selected_effect':body(chosen)[0].key,'first_effect_value':body(chosen)[0].value,'expected':'expired promise must not use success branch','boundary':'actual ordered branch predicate only, not full loyalty effect execution'}

if __name__=='__main__':
 results=[]
 for name,fn in [('expired_episode_still_actionable',stale_episode),('expired_30_day_market_verification_reports_success',stale_market),('C1_kind5_actual_B2_closure',kind5),('imperial_line_outside_India_not_excluded',imperial_marker),('promise_law_after_expiry_selects_success',late_promise_branch)]:
  try:results.append({'name':name,'result':copy.deepcopy(fn())})
  except Exception as exc:results.append({'name':name,'status':'NOT_RUN','error':repr(exc),'traceback':traceback.format_exc()})
 dump(run/'b2-minimal-source-red-cases.json',{'cases':results,'boundary':'Actual frozen ordered AST; native country/building/movement/pact facts explicitly injected. No general B2 behavioral matrix or engine simulation.','snapshot':str(snap),'engine_run':False});print(json.dumps(results,ensure_ascii=False,indent=2))
