from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_routes.py').read_text();exec(src[:src.rindex('\ntry:\n check(')],globals())
results=[];reads=[]
def dry(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);cur=stack[-1]
  if k=='if':
   branch,i=x['selected_branches'](nodes,i-1,stack,'if')
   if branch:dry(body(branch),stack,path)
  elif k in defs and defs[k][0]=='effect':x['invoke']('effect',k,stack,n.children)
  elif k in ['hidden_effect','show_as_tooltip']:dry(n.children,stack,path)
  elif k.startswith(('c:','var:','scope:')):
   obj=resolve(k,stack)
   if obj is None:
    if n.op=='?=':continue
    raise RuntimeError('preview missing effect scope '+k)
   dry(n.children,stack+[obj],path)
  elif k in ['create_diplomatic_pact','create_treaty']:
   for field in ['country'] if k=='create_diplomatic_pact' else ['first_country','second_country']:
    obj=resolve(child(n,field).value,stack);reads.append((k,field,str(obj)));assert obj is not None
  elif k=='random_country':
   for obj in world.values():
    if x['triggers'](child(n,'limit').children,stack+[obj]):dry(body(n),stack+[obj],path)
  elif k in ['set_variable','change_variable','remove_variable','clamp_variable','save_scope_as','save_scope_value_as','clear_saved_scope','add_modifier','remove_modifier','trigger_event','custom_tooltip','change_relations']:pass
  else:raise Unsupported('dry effect '+k)
x['effects']=dry
try:
 for selected in ['valid','missing','subject','dead','final']:
  reset();e=world['EGY'];f=world['FRA'];e.variables={'nesnd_egypt_started':True,'nesnd_egypt_independence':0,'nesnd_egypt_sponsor_mode':1}
  if selected!='missing':e.variables['nesnd_egypt_investor']=f
  if selected=='subject':f.overlord=world['GBR']
  if selected=='dead':f.alive=False
  if selected=='final':e.variables.update(nesnd_egypt_finished=True,nesnd_egypt_final_patron=f);e.overlord=f;e.subject_type='subject_type_protectorate'
  before=copy.copy(e.variables);saved.clear();eff('nesnd_egypt_settle_dependence',e);assert e.variables==before and not saved
  results.append({'name':'egypt_settle_preview_'+selected,'status':'PASS'})
 for tag in ['FRA','USM','SIH','GBR','QE1','TUR']:
  reset();e=world['EGY'];e.variables={'nesnd_egypt_started':True,'nesnd_egypt_independence':50,'nesnd_egypt_sponsor_mode':1};saved.clear();eff('nesnd_egypt_select_investor',e,'TAG = '+tag);assert not saved and 'nesnd_egypt_investor' not in e.variables
  results.append({'name':'select_preview_no_writes_'+tag,'status':'PASS'})
 for tag in ['FRA','ABSENT']:
  reset();a=world['USA'];saved.clear();eff('nesnd_canon_send_request',a,'TAG = '+tag+' KIND = 2');assert not saved and not a.variables
  results.append({'name':'send_preview_no_saved_scopes_'+tag,'status':'PASS'})
 status='PASS_PREVIEW_SOURCE_CLOSURE'
except Exception as exc:status='NOT_RUN_OR_FAIL';results.append({'error':repr(exc),'traceback':traceback.format_exc()})
report={'status':status,'checks':results,'native_target_reads':reads,'boundary':'Actual source AST; all effect saves/writes skipped in preview, hidden_effect traversed; native primitives are fixtures. Not engine/UI validation.'}
dump(run/'preview-repair4-closure.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
