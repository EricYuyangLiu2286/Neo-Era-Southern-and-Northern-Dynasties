from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_extended_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
reads=[]
def dry(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);cur=stack[-1]
  if k=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:dry(body(chosen),stack,path)
  elif k in defs and defs[k][0]=='effect':x['invoke']('effect',k,stack,n.children)
  elif k in ['hidden_effect','show_as_tooltip']:dry(n.children,stack,path)
  elif k.startswith('je:'):
   key=k[3:]
   if key not in stack[0].journals:raise Unsupported('fixture missing actual JE '+key)
   dry(n.children,stack+[Entity('journal',key,owner=stack[0])],path)
  elif k=='set_bar_progress':
   valnode=child(n,'value');reads.append({'path':path,'value':valnode.value,'saved_scope_present':'small_display_country' in saved});x['number'](valnode.value,stack)
  elif k.startswith(('c:','scope:','var:')) or k in props:
   obj=resolve(k,stack)
   if obj is None:
    if n.op=='?=':continue
    raise Unsupported('unguarded preview scope '+k)
   dry(n.children,stack+[obj],path)
  elif k in ['set_variable','change_variable','remove_variable','save_scope_as','save_scope_value_as','clear_saved_scope','add_modifier','remove_modifier','trigger_event','custom_tooltip']:pass
  else:raise Unsupported('unsupported preview primitive '+k)
x['effects']=dry
# A real active economy JE, on an already-initialized country; initialization is not the failure.
a,s=country_fixture();a.variables['nesnd_small_lineage']=True;a.journals={'nesnd_small_economy_journal'};saved.clear();before=copy.copy(a.variables)
je=defs['nesnd_small_economy_journal'][1]
try:
 dry(child(je,'immediate').children,[a],defs['nesnd_small_economy_journal'][2]);result={'status':'PASS'}
except Exception as e:
 result={'status':'SOURCE_PREVIEW_REFERENCE_FAILURE','error':repr(e),'traceback':traceback.format_exc(),'actual_je_immediate':shape(child(je,'immediate')),'native_facts':{'tag':'ACE','active_journal':'nesnd_small_economy_journal','already_initialized':True},'reads':reads,'writes_skipped':a.variables==before and not saved,'boundary':'Actual frozen JE immediate -> sync_bars ordered AST; native current JE instance is injected; effect save/write operations skipped by established preview contract. No game UI claim.'}
dump(run/'b2r2-display-preview-red.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))
