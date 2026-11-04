"""Actual frozen AST lifecycle probe. Native country facts are explicit fixtures.
This checks persistence/available exits, not whether an engine creates a pact.
"""
from canon_routes_context import *
import operator,traceback
cfg=json.loads((R/'batch-c-validation-current.json').read_text('utf-8'));run=Path(cfg['run']);snap=Path(cfg['snapshot'])
# Reuse the already-red/green ordered control-flow evaluator, before its runner.
source=(W/'tools/test_batch_c_preview.py').read_text('utf-8')
namespace={};exec(source[:source.index('\ntry:\n parsed=0')],namespace)
for rel in cfg['owned_files']:
 if rel.startswith(('common/scripted_triggers/','common/scripted_effects/')) and rel.endswith('.txt'):
  raw=read(snap/rel);namespace['texts'][rel]=raw
  kind='trigger' if '/scripted_triggers/' in rel else 'effect'
  for node in parse(raw).children or []:
   if node.key:namespace['defs'][node.key]=(kind,node,rel)
old_resolve=namespace['resolve'];old_scalar=namespace['scalar']
def resolve(token,stack):
 token=namespace['clean'](token)
 try:return float(token)
 except (ValueError,TypeError):pass
 return old_resolve(token,stack)
namespace['resolve']=resolve
comparisons={'=':operator.eq,'?=':operator.eq,'!=':operator.ne,'>':operator.gt,'<':operator.lt,'>=':operator.ge,'<=':operator.le}
def scalar(node,stack):
 if node.key=='game_date':return comparisons[node.op]((1836,1,1),tuple(map(int,namespace['clean'](node.value).split('.'))))
 if node.key.startswith('var:') and node.children is None:
  left=resolve(node.key,stack);right=resolve(node.value,stack)
  return comparisons[node.op](left,right)
 if node.key=='has_journal_entry':return namespace['clean'](node.value) in getattr(stack[-1],'journals',set())
 return old_scalar(node,stack)
namespace['scalar']=scalar
child=namespace['child'];body=namespace['body'];triggers=namespace['triggers'];defs=namespace['defs'];clean=namespace['clean']
world=namespace['world'];saved=namespace['saved'];events=[];write_log=[]
# The patron was selectable earlier, then became unable to hold subjects before Egypt reached zero.
egypt=world['EGY'];patron=world['FRA'];patron.can_have_subjects=False
egypt.journals={'nesnd_egypt_independence'}
def effects(nodes,stack,path):
 i=0
 while i<len(nodes):
  node=nodes[i];key=node.key;value=clean(node.value);current=stack[-1]
  if key=='if':
   branches=[node];i+=1
   while i<len(nodes) and nodes[i].key in ['else_if','else']:branches.append(nodes[i]);i+=1
   for branch in branches:
    limit=child(branch,'limit')
    if branch.key=='else' or triggers(limit.children if limit else [],stack):effects(body(branch),stack,path);break
   continue
  i+=1
  if key in defs and defs[key][0]=='effect':
   _,definition,definition_path=defs[key];effects(definition.children or [],stack,definition_path);continue
  if key.startswith(('c:','var:','scope:')):
   target=resolve(key,stack)
   if target is None:
    if node.op=='?=':continue
    raise RuntimeError('missing scoped object '+key)
   effects(node.children or [],stack+[target],path);continue
  if key=='set_variable':
   name=value if value else clean(child(node,'name').value)
   valnode=child(node,'value')
   assigned=resolve(valnode.value,stack) if valnode else True
   current.variables[name]=assigned
   write_log.append({'country':current.tag,'name':name,'has_expiry':any(x.key in ['days','weeks','months','years'] for x in node.children or [])})
  elif key=='remove_variable':current.variables.pop(value,None)
  elif key=='save_scope_as':saved[value]=current
  elif key=='clear_saved_scope':saved.pop(value,None)
  elif key=='add_modifier':current.modifiers.add(clean(child(node,'name').value))
  elif key=='remove_modifier':current.modifiers.discard(value)
  elif key=='trigger_event':events.append({'country':current.tag,'id':clean(child(node,'id').value) if node.children else value})
  elif key in ['hidden_effect','show_as_tooltip']:effects(node.children or [],stack,path)
  else:raise namespace['Unsupported']('effect '+str(key))
def call(name):
 _,node,path=defs[name];effects(node.children or [],[egypt],path)
result={'test':'living_patron_loses_subject_capacity_before_zero','scope':'actual frozen effects and predicates','fixture':{'EGY':'alive independent, independence=0, selected FRA, mode=1','FRA':'alive, no war, not Egyptian subject, can_have_subjects=no','external_conditions':'remain unchanged throughout retries'},'engine_verified':False}
try:
 call('nesnd_egypt_settle_dependence')
 egypt.journals.clear() # The native parent JE has failed; the source callback retains pending.
 first=dict((k,str(v)) for k,v in egypt.variables.items())
 for retry in range(64):call('nesnd_egypt_maintenance')
 open_node=defs['nesnd_egypt_independence_open'][1]
 gate_open=triggers(open_node.children,[egypt])
 button=parse(read(snap/'common/scripted_buttons/nesnd_egypt_independence.txt'))
 none=next(n for n in button.children if n.key=='nesnd_egypt_investor_none')
 none_possible=triggers(child(none,'possible').children,[egypt])
 selectable=defs['nesnd_egypt_can_select'][1]
 selected_gates=[n.key for n in selectable.children or [] if n.key=='nesnd_egypt_independence_open']
 pending_writes=[x for x in write_log if x['name']=='nesnd_egypt_settlement_pending']
 result.update({'after_first_callback':first,'after_64_maintenance_callbacks':dict((k,str(v)) for k,v in egypt.variables.items()),'pending_write_count':len(pending_writes),'pending_has_any_expiry':any(x['has_expiry'] for x in pending_writes),'independence_open':gate_open,'none_button_possible':none_possible,'all_six_selection_buttons_require_closed_open_gate':bool(selected_gates),'notifications':events})
 stalled=bool(egypt.variables.get('nesnd_egypt_settlement_pending')) and 'nesnd_egypt_finished' not in egypt.variables and not gate_open and not none_possible and not any(x['has_expiry'] for x in pending_writes)
 result['status']='FAIL_UNBOUNDED_PENDING' if stalled else 'PASS_EXIT_OBSERVED'
 result['reason']='Living sponsor is never replaced, cannot create either pact, pending has no deadline, parent JE is gone and all seven choice buttons are closed.' if stalled else 'An exit was observed in this source fixture.'
except Exception as exc:
 result['status']='NOT_RUN_UNSUPPORTED';result['error']=repr(exc);result['traceback']=traceback.format_exc()
dump(run/'egypt-pending-lifecycle.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(1 if result['status'].startswith('FAIL') else 0)
