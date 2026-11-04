from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_extended_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
base_scalar2=scalar;base_effects2=x['effects'];base_iter2=iterator_items
native={'autonomy':'subject_type_protectorate','independence':True,'market':'pending'};ops=[]
def iterator_items(key,node,cur):
 if key=='any_diplomatic_catalyst':return cur.catalysts
 return base_iter2(key,node,cur)
def scalar(n,stack):
 k=subst(n.key);v=subst(n.value);cur=stack[-1]
 if k=='can_increase_autonomy':return cur.can_increase==(v=='yes')
 if k=='can_create_diplomatic_pact':return cur.can_pact
 if k=='is_diplomatic_catalyst_type':return cur.catalyst_type==v
 return base_scalar2(n,stack)
x['scalar']=scalar;x['ns']['scalar']=scalar

def effect_sequence2(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);cur=stack[-1]
  if k=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:effect_sequence2(body(chosen),stack,path)
  elif k=='set_variable' and child(n,'value') is not None and child(n,'value').children is None and subst(child(n,'value').value) in ['overlord','market.owner']:
   cur.variables[subst(child(n,'name').value)]=resolve(child(n,'value').value,stack)
  elif k=='increase_autonomy':
   ops.append((cur.tag,k,native['autonomy']))
   if native['autonomy']=='independent':cur.overlord=None;cur.subject_type=None
   elif native['autonomy'] is not None:cur.subject_type=native['autonomy']
  elif k=='make_independent':
   ops.append((cur.tag,k,native['independence']))
   if native['independence']:cur.overlord=None;cur.subject_type=None
  elif k=='add_liberty_desire':cur.liberty_desire+=x['number'](n.value,stack)
  elif k=='create_bidirectional_truce':
   other=resolve(child(n,'country').value,stack);ops.append((cur.tag,k,other.tag));cur.truces.add(other.tag);other.truces.add(cur.tag)
  elif k=='create_diplomatic_catalyst':
   other=resolve(child(n,'target').value,stack);cur.catalysts.append(Entity('catalyst',str(len(cur.catalysts)),catalyst_type=subst(child(n,'type').value),target=other))
  elif k=='create_diplomatic_pact' and child(n,'type').value=='grant_own_market':
   other=resolve(child(n,'country').value,stack);ops.append((cur.tag,k,'grant_own_market',native['market']))
   if native['market']!='failure':
    cur.pact_facts.append(('grant_own_market',other,True));other.pact_facts.append(('grant_own_market',cur,False))
    if native['market']=='immediate':other.market=Entity('market','actual-own-market',owner=other)
  else:base_effects2([n],stack,path)
x['effects']=effect_sequence2

def request_fixture(kind=6,subject_type='subject_type_puppet'):
 a,s=country_fixture();f=world['FRA'];a.variables['nesnd_small_governance_done']=True;a.army_size=20;a.gdp=100000;a.liberty_desire=80;a.dependence={'FRA':1};a.relations['FRA']=30;f.relations['ACE']=30;f.army_size=40;f.gdp=100000;f.in_default=False
 for c in world.values():c.gdp=getattr(c,'gdp',100000);c.catalysts=[];c.can_increase=True;c.can_pact=True;c.adjacent=set();c.pact_facts=getattr(c,'pact_facts',[])
 if kind in [6,7]:a.overlord=f;a.subject_type=subject_type
 if kind in [6,7,8]:a.market=Entity('market','foreign-market',owner=f)
 if kind==9:a.overlord=None;a.subject_type=None
 native.update(autonomy='subject_type_protectorate',independence=True,market='pending');ops.clear();saved['small_receiver']=f
 eff('nesnd_small_send_request',a,'KIND = '+str(kind));assert 'nesnd_canon_request_clock' in a.variables,(kind,'send failed')
 captured=next(e for e in captured_events if e['event']=='nesnd_small_states.20');saved.clear();saved.update(captured['scopes']);assert trig('nesnd_canon_reply_valid',f) and trig('nesnd_canon_request_eligible',f)
 return a,s,f,copy.copy(saved)

def cases():
 rows=[]
 for kind in [6,7,8,9]:
  for outcome in ['success','no_native_change']:
   a,s,f,scopes=request_fixture(kind)
   if outcome=='no_native_change':native.update(autonomy=None,independence=False,market='failure');engine['create_treaty']=False
   elif kind==8:native['market']='immediate'
   eff('nesnd_small_accept_request',f)
   notice=x['notifications'][-1][1];expected='nesnd_canon_diplomacy.2' if outcome=='success' else 'nesnd_canon_diplomacy.3';assert notice==expected,(kind,outcome,notice)
   assert 'nesnd_canon_request_clock' not in a.variables
   rows.append({'kind':kind,'native_outcome':outcome,'notice':notice,'actual_overlord':a.overlord.tag if a.overlord else None,'actual_subject_type':a.subject_type,'actual_market_owner':a.market.owner.tag,'ops':copy.deepcopy(ops)})
 # A low-grade to different low-grade native transition must not claim the high-autonomy result.
 a,s,f,scopes=request_fixture(6);native['autonomy']='subject_type_vassal';eff('nesnd_small_accept_request',f);assert x['notifications'][-1][1]=='nesnd_canon_diplomacy.3';rows.append({'kind6_low_to_low':'failure confirmed by actual grade helper'})
 # A still-high unchanged level is not a new concession; captured prior level2.
 a,s,f,scopes=request_fixture(6,'subject_type_protectorate');assert a.variables['nesnd_small_request_autonomy']==2;native['autonomy']=None;eff('nesnd_small_accept_request',f);assert x['notifications'][-1][1]=='nesnd_canon_diplomacy.3';rows.append({'kind6_prior_high_no_change':'failure'})
 return rows

if __name__=='__main__':
 try:r={'status':'PASS_NATIVE_POSTCONDITION_FIXTURE_MATRIX','cases':cases(),'boundary':'Actual frozen send/reply/accept/result AST, native effect outcome explicitly supplied as primitive country/treaty/market facts. No derivation or claim of engine autonomy/treaty behavior.'}
 except Exception as e:r={'status':'FAIL_OR_ADAPTER_UNRESOLVED','error':repr(e),'traceback':traceback.format_exc()}
 dump(run/'b2r2-kind6-9-postconditions.json',r);print(json.dumps(r,ensure_ascii=False,indent=2))
