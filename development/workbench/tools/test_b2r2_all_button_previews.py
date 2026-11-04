from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
reads=[]
mutators={'set_variable','change_variable','remove_variable','save_scope_as','save_scope_value_as','clear_saved_scope','add_modifier','remove_modifier','trigger_event','custom_tooltip','change_relations','add_to_variable_list','remove_from_variable_list','increase_autonomy','make_independent','add_liberty_desire','create_bidirectional_truce','create_diplomatic_catalyst','add_radicals','add_loyalists'}
def dry(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);cur=stack[-1]
  if k=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:dry(body(chosen),stack,path)
  elif k in defs and defs[k][0]=='effect':x['invoke']('effect',k,stack,n.children)
  elif k in ['hidden_effect','show_as_tooltip']:dry(n.children,stack,path)
  elif k.startswith(('c:','var:','scope:','ig:')) or k in props or k=='market.owner':
   obj=resolve(k,stack)
   if obj is None:
    if n.op=='?=':continue
    raise Unsupported('missing preview target '+k)
   dry(n.children,stack+[obj],path)
  elif k in ['random_country','ordered_country','random_scope_state','ordered_scope_state','every_scope_state','random_political_movement','random_supporting_character']:
   items=list(world.values()) if 'country' in k else cur.states if 'scope_state' in k else cur.movements if 'political_movement' in k else cur.supporters
   lim=child(n,'limit');items=[z for z in items if x['triggers'](lim.children if lim else [],stack+[z])]
   # Traverse all eligible branches; skip ordering metadata and effect writes.
   for z in items:dry([c for c in body(n) if c.key not in ['order_by','position','check_range_bounds','max']],stack+[z],path)
  elif k.startswith('je:'):
   key=k[3:]
   if key not in stack[0].journals:raise Unsupported('no actual JE '+key)
   dry(n.children,stack+[Entity('journal',key,owner=stack[0])],path)
  elif k=='set_bar_progress':x['number'](child(n,'value').value,stack)
  elif k in ['create_treaty','create_diplomatic_pact']:
   for field in ['country'] if k=='create_diplomatic_pact' else ['first_country','second_country']:
    obj=resolve(child(n,field).value,stack);assert obj is not None;reads.append((k,field,str(obj)))
  elif k in mutators:
   if k=='add_modifier' and child(n,'multiplier') is not None:x['number'](child(n,'multiplier').value,stack)
  else:raise Unsupported('unknown preview effect '+k)
x['effects']=dry
rows=[]
try:
 rel='common/scripted_buttons/nesnd_small_states.txt';buttons=parse(read(snap/rel)).children
 for mode in ['independent','low_subject','high_subject','lost_country']:
  # Use a successful real request setup, then native expiry clears request/cooldown for button review.
  x['effects']=effect_sequence2
  a,s,f,scopes=request_fixture(6 if mode in ['low_subject','high_subject'] else 9)
  for key in list(a.variables):
   if key.startswith('nesnd_canon_request_') or key.startswith('nesnd_small_request_'):a.variables.pop(key)
  if mode=='high_subject':a.subject_type='subject_type_protectorate'
  if mode=='lost_country':s.region=region('region_western_europe')
  a.market=Entity('market','foreign-market',owner=f)
  x['effects']=dry
  for button in buttons:
   saved.clear();before=copy.copy(a.variables);visible=x['triggers'](child(button,'visible').children,[a]);possible=x['triggers'](child(button,'possible').children,[a]);dry(child(button,'effect').children,[a],rel);assert a.variables==before
   rows.append({'mode':mode,'button':button.key,'visible':visible,'possible':possible,'preview_no_country_writes':True})
 report={'status':'PASS_ALL_SMALL_BUTTON_EFFECT_PREVIEWS','cases':rows,'native_target_reads':reads,'boundary':'Actual source conditions and entire hidden-effect closures, all effect save/writes skipped; ephemeral trigger saved scopes follow native trigger contract. No UI rendering or gameplay click claim.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-all-small-button-previews.json',report);print(json.dumps({'status':report['status'],'completed':len(rows),'error':report.get('error'),'traceback':report.get('traceback')},ensure_ascii=False,indent=2))

