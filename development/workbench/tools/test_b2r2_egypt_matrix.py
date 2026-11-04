"""Source-AST Egypt lifecycle matrix with explicit native API outcomes.
Scope: script control flow, timers, writes and callbacks. No Victoria engine is simulated.
Unknown syntax raises Unsupported. All paths use the fixed snapshot definitions.
"""
from canon_routes_context import *
import operator,traceback,copy
cfg=json.loads((R/'batch-b2-repair2-test-config.json').read_text('utf-8'));run=Path(cfg['run']);snap=Path(cfg['snapshot'])
ns={};src=(W/'tools/test_b2r2_preview.py').read_text('utf-8');exec(src[:src.index('\ntry:\n parsed=0')],ns)
for rel in cfg['owned_files']:
 if not rel.endswith('.txt'):continue
 text=read(snap/rel);ns['texts'][rel]=text
 kind='trigger' if '/scripted_triggers/' in rel else 'effect' if '/scripted_effects/' in rel else 'value' if '/script_values/' in rel else 'event' if rel.startswith('events/') else 'journal' if '/journal_entries/' in rel else 'button' if '/scripted_buttons/' in rel else None
 if kind:
  for n in parse(text).children or []:
   if n.key:ns['defs'][n.key]=(kind,n,rel)
defs=ns['defs'];child=ns['child'];body=ns['body'];clean=ns['clean'];Country=ns['Country'];Unsupported=ns['Unsupported']
world=ns['world'];saved=ns['saved'];params={};now=0;schedule=[];notifications=[];mutations=[];pacts=[];pact_outcome='success'
base_resolve=ns['resolve'];base_scalar=ns['scalar'];cmp={'=':operator.eq,'?=':operator.eq,'!=':operator.ne,'>':operator.gt,'<':operator.lt,'>=':operator.ge,'<=':operator.le}
def subst(s):
 s=clean(s)
 if not isinstance(s,str):return s
 for k,v in params.items():s=s.replace('$'+k+'$',str(v))
 return s

def resolve(s,stack):
 s=subst(s)
 if s=='yes':return True
 if s=='no':return False
 try:return float(s)
 except (ValueError,TypeError):pass
 return base_resolve(s,stack)
ns['resolve']=resolve

def invoke(kind,name,stack,args=None):
 global params
 if name not in defs or defs[name][0]!=kind:raise Unsupported(kind+' function '+name)
 previous=params
 new=dict(params)
 for n in args or []:
  if n.children is not None:raise Unsupported('structured parameter '+str(n.key))
  new[n.key]=subst(n.value)
 params=new
 try:
  node=defs[name][1]
  if kind=='trigger':return triggers(node.children,stack)
  if kind=='effect':return effects(node.children,stack,defs[name][2])
  if kind=='value':return calculate(node.children,stack)
 finally:params=previous

def scalar(n,stack):
 k=subst(n.key);v=subst(n.value);cur=stack[-1]
 if k in defs:
  if defs[k][0]=='trigger':return invoke('trigger',k,stack,n.children)
  if defs[k][0]=='value':return cmp[n.op](invoke('value',k,stack),number(v,stack))
 if k=='game_date':return cmp[n.op]((1836,1,1),tuple(map(int,v.split('.'))))
 if k=='is_country_type':return cur.country_type==v
 if k=='has_journal_entry':return v in cur.journals
 if k=='any_country':
  nodes=[x for x in n.children or [] if x.key not in ['count','percent']]
  vals=[triggers(nodes,stack+[c]) for c in list(world.values())]
  counter=child(n,'count')
  return cmp[counter.op](sum(vals),number(counter.value,stack)) if counter else any(vals)
 if k.startswith(('var:','scope:')) and n.children is None:
  return cmp[n.op](resolve(k,stack),resolve(v,stack))
 if k!=n.key or v!=clean(n.value):
  n=copy.copy(n);n.key=k;n.value=v
 return base_scalar(n,stack)
ns['scalar']=scalar;triggers=ns['triggers']

def number(token,stack):
 if isinstance(token,list):return calculate(token,stack)
 t=subst(token)
 if t in defs and defs[t][0]=='value':return invoke('value',t,stack)
 if t=='gdp_ownership_ratio(prev)':return stack[-1].ownership.get(stack[-2].tag,0)
 value=resolve(t,stack)
 if not isinstance(value,(int,float)):raise Unsupported('not a number '+str(t))
 return value

def selected_branches(nodes,i,stack,prefix):
 branches=[nodes[i]];i+=1
 others=['else_if','else'] if prefix=='if' else ['trigger_else_if','trigger_else']
 while i<len(nodes) and nodes[i].key in others:branches.append(nodes[i]);i+=1
 for n in branches:
  limit=child(n,'limit')
  if n.key==others[-1] or triggers(limit.children if limit else [],stack):return n,i
 return None,i

def calculate(nodes,stack,acc=0):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=n.key
  if k=='if':
   selected,i=selected_branches(nodes,i-1,stack,'if')
   if selected:acc=calculate(body(selected),stack,acc)
  elif k in ['value','add','subtract','multiply','divide','min','max']:
   operand=calculate(n.children,stack) if n.children is not None else number(n.value,stack)
   if k=='value':acc=operand
   elif k=='add':acc+=operand
   elif k=='subtract':acc-=operand
   elif k=='multiply':acc*=operand
   elif k=='divide':acc/=operand
   elif k=='min':acc=max(acc,operand)
   elif k=='max':acc=min(acc,operand)
  elif k=='every_country':
   limit=child(n,'limit')
   for c in list(world.values()):
    if triggers(limit.children if limit else [],stack+[c]):acc=calculate(body(n),stack+[c],acc)
  elif k=='prev':
   if len(stack)<2:raise Unsupported('missing prev in script value')
   acc=calculate(n.children,stack+[stack[-2]],acc)
  else:raise Unsupported('script value '+str(k))
 return acc

def effects(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);v=subst(n.value);cur=stack[-1]
  if k=='if':
   chosen,i=selected_branches(nodes,i-1,stack,'if')
   if chosen:effects(body(chosen),stack,path)
   continue
  if k in defs and defs[k][0]=='effect':invoke('effect',k,stack,n.children);continue
  if k.startswith(('c:','var:','scope:')):
   target=resolve(k,stack)
   if target is None:
    if n.op=='?=':continue
    raise RuntimeError('null effect scope '+k)
   effects(n.children or [],stack+[target],path);continue
  if k in ['hidden_effect','show_as_tooltip']:
   # show_as_tooltip is non-executing; only hidden_effect contains real writes.
   if k=='hidden_effect':effects(n.children or [],stack,path)
  elif k=='set_variable':
   name=v if v else subst(child(n,'name').value);val=child(n,'value')
   assigned=number(val.children if val.children else val.value,stack) if val and (val.children or not str(subst(val.value)).startswith(('c:','scope:','var:'))) else resolve(val.value,stack) if val else True
   cur.variables[name]=assigned;cur.expiry.pop(name,None)
   days=child(n,'days')
   if days:cur.expiry[name]=now+number(days.value,stack)
   mutations.append((now,cur.tag,'set_variable',name,cur.expiry.get(name)))
  elif k=='remove_variable':cur.variables.pop(v,None);cur.expiry.pop(v,None)
  elif k=='save_scope_as':saved[v]=cur
  elif k=='clear_saved_scope':saved.pop(v,None)
  elif k=='random_country':
   limit=child(n,'limit');eligible=[c for c in world.values() if triggers(limit.children if limit else [],stack+[c])]
   if eligible:effects(body(n),stack+[eligible[0]],path)
  elif k=='add_modifier':
   name=subst(child(n,'name').value);cur.modifiers.add(name);cur.modifier_adds[name]=cur.modifier_adds.get(name,0)+1
  elif k=='remove_modifier':cur.modifiers.discard(v)
  elif k=='trigger_event':
   event=subst(child(n,'id').value) if n.children else v;days=child(n,'days')
   due=now+(number(days.value,stack) if days else 0)
   if event in defs and defs[event][0]=='event' and child(defs[event][1],'hidden'):
    schedule.append((due,event,cur))
   else:notifications.append((cur.tag,event))
  elif k=='create_diplomatic_pact':
   target=resolve(child(n,'country').value,stack);action=subst(child(n,'type').value)
   if target is None:raise RuntimeError('missing pact target')
   pacts.append((now,cur.tag,target.tag,action))
   if pact_outcome=='success' or (pact_outcome=='custom_only' and action=='nesnd_egypt_protectorate'):
    target.overlord=cur;target.subject_type='subject_type_'+action
  elif k in ['custom_tooltip']:pass
  else:raise Unsupported('effect '+str(k))

def reset(capable=False,selected=True):
 global now,pact_outcome
 now=0;pact_outcome='success';world.clear();saved.clear();params.clear();schedule.clear();notifications.clear();mutations.clear();pacts.clear()
 for tag in ['EGY','FRA','USM','GBR']:
  c=Country(tag);c.country_type='recognized';c.journals=set();c.expiry={};c.modifier_adds={};c.ownership={};world[tag]=c
 e=world['EGY'];e.journals={'nesnd_egypt_independence'}
 e.variables={'nesnd_egypt_started':True,'nesnd_egypt_independence':0,'nesnd_egypt_generation':True,'nesnd_egypt_sponsor_mode':1 if selected else 0}
 if selected:e.variables['nesnd_egypt_investor']=world['FRA']
 world['FRA'].can_have_subjects=capable
 return e

def call(name,country='EGY',args=None):return invoke('effect',name,[world[country]],args)
def predicate(name,country='EGY',args=None):return invoke('trigger',name,[world[country]],args)
def deliver(event,actor):
 n=defs[event][1];trigger=child(n,'trigger')
 if trigger is None or triggers(trigger.children,[actor]):
  immediate=child(n,'immediate')
  if immediate:effects(immediate.children,[actor],defs[event][2])
def expire():
 for c in world.values():
  for key,deadline in list(c.expiry.items()):
   if deadline<=now:c.expiry.pop(key,None);c.variables.pop(key,None)
def advance(day,expire_first=True):
 global now
 while True:
  ready=sorted([x for x in schedule if x[0]<=day],key=lambda x:x[0])
  if not ready:break
  due,event,actor=ready[0];schedule.remove((due,event,actor));now=due
  if expire_first:expire()
  deliver(event,actor)
  if not expire_first:expire()
 now=day;expire()
def params_node(text):return parse(text).children
results=[]

def check(name,fn):
 try:
  detail=copy.deepcopy(fn());results.append({'name':name,'status':'PASS','detail':detail})
 except AssertionError:
  results.append({'name':name,'status':'FAIL','traceback':traceback.format_exc()});raise

def immediate(outcome='success',blocked=None):
 global pact_outcome
 e=reset(True);pact_outcome=outcome;world['FRA'].blocked_types=set(blocked or [])
 call('nesnd_egypt_settle_dependence')
 assert e.variables.get('nesnd_egypt_finished') and not schedule
 if outcome=='failure':assert e.variables.get('nesnd_egypt_guarantees_unworkable') and e.modifier_adds['nesnd_egypt_unsecured_independence']==1
 else:
  assert e.variables.get('nesnd_egypt_protected') and e.variables['nesnd_egypt_final_patron'] is world['FRA']
  assert 'nesnd_egypt_investor' not in e.variables and predicate('nesnd_egypt_protected_fact')
  assert not predicate('nesnd_egypt_investor_cooperating')
 before=(len(pacts),len(notifications),dict(e.modifier_adds))
 for _ in range(64):call('nesnd_egypt_maintenance');call('nesnd_egypt_settle_dependence')
 assert before==(len(pacts),len(notifications),dict(e.modifier_adds))
 assert len(pacts)==(2 if outcome in ['failure','custom_only'] and not blocked else 1)
 assert not any('settlement_' in m[3] or m[3] in ['nesnd_egypt_standard_attempted','nesnd_egypt_pending_explained'] for m in mutations)
 return {'pacts':pacts,'notifications':notifications,'penalties':e.modifier_adds,'immediate':True}

def choices():
 rows=[]
 for tag in ['FRA','USM','SIH','GBR','QE1','TUR']:
  for state in ['absent','dead','subject','independent']:
   e=reset(True);e.variables['nesnd_egypt_independence']=50
   world.pop(tag,None)
   if state!='absent':
    c=Country(tag);c.country_type='recognized';world[tag]=c
    if state=='dead':c.alive=False
    if state=='subject':c.overlord=world['EGY'] if tag=='USM' else world['USM']
   got=predicate('nesnd_egypt_can_select',args=params_node('TAG = '+tag));assert got==(state=='independent')
   call('nesnd_egypt_select_investor',args=params_node('TAG = '+tag))
   rows.append([tag,state,got])
 return rows

def none():
 e=reset(True);e.variables['nesnd_egypt_independence']=50;call('nesnd_egypt_choose_none')
 for _ in range(8):call('nesnd_egypt_maintenance')
 assert e.variables['nesnd_egypt_sponsor_mode']==0 and 'nesnd_egypt_investor' not in e.variables
 assert e.variables['nesnd_egypt_independence']==50 and e.variables['nesnd_egypt_generation'] is True
 e.variables['nesnd_egypt_independence']=0;call('nesnd_egypt_settle_dependence')
 assert not pacts and e.modifier_adds['nesnd_egypt_unsecured_independence']==1
 return {'penalties':e.modifier_adds}

def replacement(state):
 e=reset(True);e.variables['nesnd_egypt_independence']=50
 if state=='dead':world['FRA'].alive=False
 else:world['FRA'].overlord=world['GBR']
 call('nesnd_egypt_replace_lost_investor');assert e.variables['nesnd_egypt_investor'] is world['USM']
 assert not e.modifier_adds and e.variables['nesnd_egypt_independence']==50 and e.variables['nesnd_egypt_generation'] is True
 return {'replacement':'USM','state':state}

def unavailable():
 e=reset(True)
 for c in world.values():
  if c is not e:c.can_have_subjects=False
 call('nesnd_egypt_settle_dependence');assert e.variables.get('nesnd_egypt_guarantees_failed') and e.variables.get('nesnd_egypt_finished')
 assert not pacts and e.modifier_adds['nesnd_egypt_unsecured_independence']==1
 return {'penalties':e.modifier_adds}

legacy=['nesnd_egypt_settlement_pending','nesnd_egypt_settlement_started','nesnd_egypt_settlement_deadline','nesnd_egypt_settlement_grace','nesnd_egypt_standard_attempted','nesnd_egypt_pending_explained']
def migration(mode,invalid_first=False):
 e=reset(True)
 for k in legacy:e.variables[k]=True
 if mode=='protected':e.overlord=world['FRA'];e.subject_type='subject_type_protectorate'
 if mode=='external':e.overlord=world['GBR'];e.subject_type='subject_type_protectorate'
 if mode=='finished':e.variables['nesnd_egypt_finished']=True
 if invalid_first:effects(child(defs['nesnd_egypt_independence'][1],'on_invalid').children,[e],defs['nesnd_egypt_independence'][2])
 else:call('nesnd_egypt_maintenance')
 assert not any(k in e.variables for k in legacy)
 assert e.variables.get('nesnd_egypt_finished')
 if mode in ['protected','independent']:assert e.variables.get('nesnd_egypt_protected') and e.variables['nesnd_egypt_final_patron'] is world['FRA']
 if mode=='external':assert e.variables.get('nesnd_egypt_external_subjugation') and e.overlord is world['GBR'] and not e.modifier_adds
 if mode=='finished':assert not pacts and not e.modifier_adds and not notifications
 return {'mode':mode,'invalid_first':invalid_first,'notifications':notifications}

def zero30():
 table=[];j=defs['nesnd_egypt_independence'][1]
 for order in [('on_complete','on_fail'),('on_fail','on_complete')]:
  e=reset(True);e.variables.pop('nesnd_egypt_generation')
  assert not triggers(child(j,'complete').children,[e]) and triggers(child(j,'fail').children,[e])
  for k in order:effects(child(j,k).children,[e],defs['nesnd_egypt_independence'][2])
  assert e.variables.get('nesnd_egypt_protected') and not e.variables.get('nesnd_egypt_independence_secured')
  assert len(notifications)==1 and not e.modifier_adds
  table.append(order)
 return table

def pressure():
 e=reset(True);out=[]
 for ratio,expect in [(0,0),(.25,0),(.5,-.5),(1,-1.5)]:
  e.variables['nesnd_egypt_foreign_gdp']=ratio
  a=invoke('value','nesnd_egypt_foreign_drain',[e]);b=invoke('value','nesnd_egypt_monthly_delta',[e]);assert a==expect and b==expect-1
  world['FRA'].overlord=world['USM'];assert invoke('value','nesnd_egypt_monthly_delta',[e])==expect;world['FRA'].overlord=None
  out.append([ratio,a,b])
 return out

def retired():
 e=reset(True)
 for id in ['nesnd_egypt.90','nesnd_egypt.91']:
  n=defs[id][1];assert child(n,'type');assert not triggers(child(n,'trigger').children,[e]);assert triggers(child(n,'cancellation_trigger').children,[e]);assert not child(n,'immediate') and not child(n,'after')
  before=dict(e.variables);deliver(id,e);assert e.variables==before
 n=defs['nesnd_egypt_protection_negotiations'][1]
 assert not triggers(child(n,'possible').children,[e]) and triggers(child(n,'invalid').children,[e])
 assert not any(c.key.startswith('on_') or c.key=='scripted_button' for c in n.children)
 return {'events':['.90','.91'],'retired_JE':True}

try:
 check('six_country_exists_alive_independent_selection',choices)
 check('standard_immediate_actual_postcondition_final_patron',immediate)
 check('standard_failure_custom_success',lambda:immediate('custom_only'))
 check('only_custom_type_eligible',lambda:immediate('success',['subject_type_protectorate']))
 check('both_native_creates_fail_immediate_once',lambda:immediate('failure'))
 check('explicit_none_no_random_draw_and_zero_once',none)
 check('dead_patron_replace_no_progress_reset',lambda:replacement('dead'))
 check('subject_patron_replace_no_progress_reset',lambda:replacement('subject'))
 check('all_patrons_incapable_zero_once',unavailable)
 for m in ['protected','external','independent','finished']:check('old_pending_'+m,lambda m=m:migration(m))
 check('invalid_before_weekly_protection_migration',lambda:migration('protected',True))
 check('zero_and_30_years_both_callback_orders',zero30)
 check('unchanged_pressure_and_subject_patron_no_drain',pressure)
 check('old_90_2_day_events_and_JE_inert',retired)
 status='PASS_SOURCE_MATRIX'
except AssertionError:status='FAIL_STOPPED'
except Exception as exc:status='NOT_RUN_UNSUPPORTED';results.append({'name':'adapter','status':'NOT_RUN','error':repr(exc),'traceback':traceback.format_exc()})
report={'status':status,'checks':results,'boundary':'Frozen ordered source AST control flow; native country facts and native create outcomes are fixtures; no engine validation.','snapshot':str(snap),'engine_verified':False}
dump(run/'egypt-repair4-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(status=='FAIL_STOPPED')
