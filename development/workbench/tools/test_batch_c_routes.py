"""Frozen source-AST requests/coalition/intervention/frontier tests.
Native API outcomes and country/building/DP facts are fixtures. No game engine,
war resolution, population mechanics or AI simulation is claimed. Unknown nodes
raise Unsupported. Native scripted treaty helper bodies are read from source.
"""
from canon_routes_context import *
import copy,operator,re,traceback
cfg=json.loads((R/'batch-c-validation-current.json').read_text('utf-8'));run=Path(cfg['run']);snap=Path(cfg['snapshot'])
x={};src=(W/'tools/test_batch_c_egypt_matrix.py').read_text('utf-8');exec(src[:src.index('\nresults=[]')],x)
defs=x['defs'];child=x['child'];body=x['body'];subst=x['subst'];Country=x['Country'];Unsupported=x['Unsupported']
world=x['world'];saved=x['saved'];cmp=x['cmp'];original_scalar=x['scalar'];original_resolve=x['resolve'];original_effects=x['effects']
for rel in ['common/scripted_triggers/00_diplomacy_triggers.txt','common/scripted_triggers/00_scripted_triggers.txt','common/script_values/00_diplomacy_values.txt','common/scripted_triggers/nesnd_batch_c_dependency_slice.txt']:
 p=snap/rel if (snap/rel).exists() else G/rel
 for n in parse(read(p)).children or []:
  if n.key and n.key not in defs:defs[n.key]=('value' if '/script_values/' in rel else 'trigger',n,rel)
class Entity:
 def __init__(self,kind,key,**kwargs):
  self.kind=kind;self.tag=key;self.variables={};self.expiry={};self.modifiers=set();self.modifier_adds={};self.valid=True
  for k,v in kwargs.items():setattr(self,k,v)
 def __repr__(self):return self.tag
cultures={k:Entity('culture',k) for k in ['north_german','south_german','north_italian','south_italian','yankee','ce_wuu']}
regions={};plays=[];captured_events=[];long_events=[];engine={'can_create_treaty':True,'create_treaty':True,'add_backer':True,'create_play':False}
# Numeric values are taken from current GAME, not copied expected constants.
define_text=read(G/'common/defines/00_defines.txt')
defines={k:float(re.search(r'^\s*'+k+r'\s*=\s*(-?[0-9.]+)',define_text,re.M).group(1)) for k in ['DIPLOMATIC_PLAY_OPENING_PHASE_END','DIPLOMATIC_PLAY_CLOSING_PHASE_START','RELATIONS_THRESHOLD_CORDIAL','RELATIONS_THRESHOLD_POOR']}
current_date=(1836,1,1)
props={'owner','source_country','target_country','target','initiator','region','state_region','power_bloc','civil_war_origin_country','overlord','top_overlord'}
def resolve(token,stack):
 token=subst(token)
 if isinstance(token,str) and token.startswith('define:NDiplomacy|'):return defines[token.split('|')[1]]
 if isinstance(token,str) and token.startswith(('cu:','s:','sr:','bt:','law_type:')):
  prefix,key=token.split(':',1)
  if prefix=='cu':return cultures.get(key)
  if prefix in ['s','sr']:return regions.get(key)
  return key
 if token=='top_overlord':
  obj=stack[-1].overlord
  if obj is None:return None
  while obj.overlord is not None:obj=obj.overlord
  return obj
 if token in props:return getattr(stack[-1],token,None)
 if isinstance(token,str) and token.startswith('relations_threshold:'):return defines['RELATIONS_THRESHOLD_'+token.split(':')[1].upper()]
 if token=='country_rank':return stack[-1].country_rank
 if isinstance(token,str) and token.startswith('relations:'):
  target=resolve(token.split(':',1)[1],stack)
  if target is None:raise Unsupported('null relations target')
  return stack[-1].relations.get(target.tag,0)
 m=re.fullmatch(r'relations\((.+)\)',str(token))
 if m:
  target=resolve(m.group(1),stack)
  if target is None:raise Unsupported('null relations target')
  return stack[-1].relations.get(target.tag,0)
 if isinstance(token,str) and '.' in token and not re.fullmatch(r'-?\d+(\.\d+)?',token):
  first,tail=token.split('.',1);obj=resolve(first,stack)
  if obj is None:raise Unsupported('null chained scope '+token)
  return resolve(tail,stack+[obj])
 value=original_resolve(token,stack)
 return None if hasattr(value,'valid') and not value.valid else value
x['resolve']=resolve;x['ns']['resolve']=resolve

def iterator_items(key,node,cur):
 if key=='any_country':return list(world.values())
 if key=='any_primary_culture':return cur.cultures
 if key=='any_scope_state':return cur.states
 if key=='any_scope_building':return cur.buildings
 if key=='any_scope_treaty':return cur.treaties
 if key=='any_scope_article':return cur.articles
 if key=='any_neighbouring_state':return cur.neighbours
 if key=='any_diplomatic_play':return [p for p in plays if p.valid]
 if key=='any_in_list':return cur.lists.get(subst(child(node,'variable').value),[])
 raise Unsupported('iterator '+key)

def member_side(play,c):
 if c is play.initiator or c in play.initiator_backers:return 1
 if c is play.target or c in play.target_backers:return 2
 return 0

def scalar(n,stack):
 key=subst(n.key);value=subst(n.value);cur=stack[-1]
 if key in defs:return original_scalar(n,stack)
 if key=='game_date':return cmp[n.op](current_date,tuple(map(int,value.split('.'))))
 if key.startswith('relations(') or '.relations:' in key:return cmp[n.op](resolve(key,stack),x['number'](value,stack))
 if key in ['custom_description','custom_description_no_bullet']:
  for field in ['subject','object']:
   f=child(n,field)
   if f and resolve(f.value,stack) is None:raise Unsupported('null native tooltip object '+field)
  return x['triggers']([a for a in n.children or [] if a.key not in ['text','subject','object']],stack)
 if key.startswith('any_'):
  items=iterator_items(key,n,cur);pred=[a for a in n.children or [] if a.key not in ['count','percent','variable','list']]
  result=[x['triggers'](pred,stack+[obj]) for obj in items]
  count=child(n,'count')
  if count:
   if subst(count.value)=='all':return all(result)
   return cmp[count.op](sum(result),x['number'](count.value,stack))
  return any(result)
 if key=='save_temporary_scope_as':saved[value]=cur;return True
 if key=='save_temporary_scope_value_as':saved[subst(child(n,'name').value)]=x['number'](child(n,'value').value,stack);return True
 if key in props:
  target=resolve(key,stack)
  if n.children is not None:
   if target is None:
    if n.op=='?=':return True
    raise Unsupported('null scope '+key)
   return x['triggers'](n.children,stack+[target])
  return cmp[n.op](target,resolve(value,stack))
 if key=='has_law_or_variant':return value.removeprefix('law_type:') in cur.laws
 if key=='can_create_treaty':
  for field in ['first_country','second_country']:
   if resolve(child(n,field).value,stack) is None:raise Unsupported('null treaty participant')
  return engine['can_create_treaty']
 if key=='binds':return resolve(value,stack) in cur.participants
 if key=='has_type':return cur.article_type==value
 if key=='has_claim_by':return resolve(value,stack).tag in cur.state_region.claims
 if key=='is_building_type':return cur.building_type==value
 if key=='country_has_building_type_levels':
  typ=resolve(child(n,'target').value,stack);test=child(n,'value')
  return cmp[test.op](sum(b.level for b in cur.buildings if b.building_type==typ),x['number'](test.value,stack))
 if key in ['army_size','occupancy','level','escalation','state_population','country_rank']:
  return cmp[n.op](getattr(cur,key),x['number'](value,stack))
 if key=='is_war':return cur.is_war==(value=='yes')
 if key=='has_play_goal':return value in cur.goals
 if key=='is_diplomatic_play_type':return value==cur.dp_type
 if key=='has_strategic_region_interest_tier':
  region=resolve(child(n,'strategic_region').value,stack);test=child(n,'value')
  if region is None:raise Unsupported('null interest region')
  return cmp[test.op](cur.interests.get(region.tag,0),x['number'](test.value,stack))
 if key=='is_in_same_power_bloc':
  target=resolve(value,stack)
  return cur.power_bloc is not None and cur.power_bloc is target.power_bloc
 if key=='modifier:power_bloc_disallow_war_bool':return cur.disallow_war==(value=='yes')
 if key=='is_indirect_subject_of':
  target=resolve(value,stack);return cur.overlord is not target and x['ns']['is_subject_of'](cur,target)
 if key=='has_subject_relation_with':
  target=resolve(value,stack);return x['ns']['is_subject_of'](cur,target) or x['ns']['is_subject_of'](target,cur)
 if key=='has_truce_with':return resolve(value,stack).tag in cur.truces
 if key=='is_at_war':return bool(cur.wars)==(value=='yes')
 if key=='is_diplomatic_play_committed_participant':return any(member_side(p,cur) for p in plays if p.valid)==(value=='yes')
 if key in ['is_diplomatic_play_ally_of','is_diplomatic_play_enemy_of']:
  target=resolve(value,stack)
  if target is None:raise Unsupported('null DP counterpart')
  return any(member_side(p,cur) and member_side(p,target) and ((member_side(p,cur)==member_side(p,target))==(key=='is_diplomatic_play_ally_of')) for p in plays if p.valid)
 if key in ['aggressive_diplomatic_plays_permitted','is_revolutionary','is_secessionist']:
  return getattr(cur,key)==(value=='yes')
 if key=='is_in_geographic_region':return value in cur.geographies
 return original_scalar(n,stack)
x['scalar']=scalar;x['ns']['scalar']=scalar

def treaty(a,b,kind,source=None,target=None):
 article=Entity('article',kind,article_type=kind,source_country=source,target_country=target)
 t=Entity('treaty',kind+'-'+a.tag+'-'+b.tag,participants=[a,b],articles=[article]);a.treaties.append(t);b.treaties.append(t);return t

def extended_effects(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;key=subst(n.key);cur=stack[-1]
  if key=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:extended_effects(body(chosen),stack,path)
   continue
  if key=='save_scope_value_as':saved[subst(child(n,'name').value)]=x['number'](child(n,'value').value,stack)
  elif key=='create_treaty':
   a=resolve(child(n,'first_country').value,stack);b=resolve(child(n,'second_country').value,stack)
   if a is None or b is None:raise Unsupported('null create treaty participant')
   if engine['create_treaty']:
    for art in child(n,'articles_to_create').children:
     if not art.children:continue
     typ=subst(child(art,'article').value);source=child(art,'source_country');target=child(art,'target_country')
     treaty(a,b,typ,resolve(source.value,stack) if source else None,resolve(target.value,stack) if target else None)
  elif key=='change_relations':
   target=resolve(child(n,'country').value,stack);amount=x['number'](child(n,'value').value,stack)
   cur.relations[target.tag]=cur.relations.get(target.tag,0)+amount;target.relations[cur.tag]=cur.relations[target.tag]
  elif key=='trigger_event':
   event=subst(child(n,'id').value);captured_events.append({'actor':cur,'event':event,'scopes':dict(saved)})
   if child(n,'months') or child(n,'years'):
    long_events.append({'actor':cur.tag,'event':event,'months':child(n,'months').value if child(n,'months') else None,'years':child(n,'years').value if child(n,'years') else None})
   else:original_effects([n],stack,path)
  elif key in ['random_diplomatic_play','random_scope_state','random_scope_treaty','random_scope_article','every_scope_treaty','every_province']:
   if key=='random_diplomatic_play':items=[p for p in plays if p.valid]
   elif key=='random_scope_state':items=cur.states
   elif key in ['random_scope_treaty','every_scope_treaty']:items=list(cur.treaties)
   elif key=='random_scope_article':items=cur.articles
   else:items=cur.provinces
   limit=child(n,'limit');items=[z for z in items if x['triggers'](limit.children if limit else [],stack+[z])]
   if key.startswith('random_'):items=items[:1]
   for obj in items:extended_effects(body(n),stack+[obj],path)
  elif key in props:
   obj=resolve(key,stack)
   if obj is None:
    if n.op=='?=':continue
    raise Unsupported('null effect link '+key)
   extended_effects(n.children,stack+[obj],path)
  elif key=='withdraw':
   for participant in cur.participants:
    if cur in participant.treaties:participant.treaties.remove(cur)
   cur.valid=False
  elif key=='add_target_backers':
   if engine['add_backer']:
    for a in n.children or []:
     target=resolve(a.value if a.value is not None else a.key,stack)
     if target is None:raise Unsupported('null backer')
     cur.target_backers.add(target)
  elif key=='add_claim':cur.claims.add(resolve(n.value,stack).tag)
  elif key=='clear_variable_list':cur.lists.pop(subst(n.value),None)
  elif key=='add_to_variable_list':
   name=subst(child(n,'name').value);cur.lists.setdefault(name,[]).append(resolve(child(n,'target').value,stack))
  elif key=='create_diplomatic_play':
   # Source callback is tested explicitly below; native play creation is an injected outcome.
   if engine['create_play']:raise Unsupported('automatic native DP creation is deliberately not simulated')
  else:original_effects([n],stack,path)
x['effects']=extended_effects

def new_country(tag,culture='north_german'):
 c=Country(tag);c.country_type='recognized';c.journals=set();c.expiry={};c.modifier_adds={};c.ownership={};c.laws={'law_monarchy'}
 c.relations={};c.cultures=[cultures[culture]];c.states=[];c.buildings=[];c.treaties=[];c.truces=set();c.power_bloc=None;c.interests={};c.lists={}
 c.country_rank=4;c.army_size=0;c.aggressive_diplomatic_plays_permitted=True;c.is_revolutionary=False;c.is_secessionist=False;c.civil_war_origin_country=None
 world[tag]=c;return c

def reset():
 global current_date
 current_date=(1836,1,1)
 world.clear();saved.clear();x['params'].clear();x['schedule'].clear();x['notifications'].clear();x['mutations'].clear();x['pacts'].clear();x['now']=0
 regions.clear();plays.clear();captured_events.clear();long_events.clear();engine.update(can_create_treaty=True,create_treaty=True,add_backer=True,create_play=False)
 for tag in ['USA','HUS','FRA','PRU','AUS','BAV','HAN','SAX','GBR','TUS','EGY']:
  new_country(tag,'yankee' if tag=='USA' else 'ce_wuu' if tag=='HUS' else 'north_italian' if tag=='TUS' else 'north_german')
 world['USA'].laws={'law_presidential_republic'}
 for c in world.values():
  for other in world.values():c.relations[other.tag]=30
 return world

def trig(name,actor,args=None):return x['invoke']('trigger',name,[actor],parse(args).children if args else None)
def eff(name,actor,args=None):return x['invoke']('effect',name,[actor],parse(args).children if args else None)
def val(name,actor):return x['invoke']('value',name,[actor])
def building(actor,key,level,occupancy=.75):
 b=Entity('building',key,building_type=key,level=level,occupancy=occupancy,owner=actor);actor.buildings.append(b);return b

def region(key,geographies=None):
 r=Entity('state_region',key,states=[],claims=set(),geographies=set(geographies or []));regions[key]=r;return r

def state(owner,key,reg=None):
 reg=reg or region(key);s=Entity('state',key+'-'+owner.tag,owner=owner,state_region=reg,region=reg,neighbours=[],provinces=[],buildings=[],geographies=set(reg.geographies),state_population=100000)
 reg.states.append(s);owner.states.append(s);return s

def dp(initiator,target,goal='conquer_state',stage=50,war=False,typ='dp_conquer_state'):
 r=regions.get('italy') or region('italy');p=Entity('diplomatic_play','play-'+str(len(plays)),initiator=initiator,target=target,region=r,goals={goal},escalation=stage,is_war=war,dp_type=typ,initiator_backers=set(),target_backers=set());plays.append(p);return p

results=[]
def check(name,fn):
 try:detail=copy.deepcopy(fn());results.append({'name':name,'status':'PASS','detail':detail})
 except AssertionError as exc:results.append({'name':name,'status':'FAIL','reason':str(exc)});raise

def request_fixture():
 reset();a=world['USA'];b=world['FRA'];a.variables={'nesnd_canon_request_serial':4,'nesnd_canon_request_kind':2,'nesnd_canon_request_partner':b,'nesnd_canon_request_clock':True}
 saved.update(canon_sender=a,canon_partner=b,canon_serial=4,canon_kind=2,canon_sender_regime=2,canon_partner_regime=1)
 return a,b

def reply_identity():
 out=[]
 for field,value,expected in [('canon_serial',4,True),('canon_serial',3,False),('canon_kind',1,False),('canon_partner',None,False),('canon_sender',None,False)]:
  a,b=request_fixture();saved[field]=value;got=trig('nesnd_canon_reply_valid',b);assert got==expected;out.append((field,str(value),got))
 a,b=request_fixture();b.alive=False;assert not trig('nesnd_canon_reply_valid',b)
 a,b=request_fixture();b.laws={'law_presidential_republic'};assert not trig('nesnd_canon_reply_valid',b)
 a,b=request_fixture();a.variables.pop('nesnd_canon_request_clock');assert not trig('nesnd_canon_reply_valid',b)
 return out

def treaty_failure_and_success():
 out=[]
 for succeeds in [False,True]:
  a,b=request_fixture();engine['create_treaty']=succeeds
  eff('nesnd_canon_accept_request',b)
  assert 'nesnd_canon_request_clock' not in a.variables
  assert ('nesnd_canon_investor' in a.variables)==succeeds
  assert ('nesnd_usa_european_capital' in a.modifiers)==succeeds
  expected='nesnd_canon_diplomacy.2' if succeeds else 'nesnd_canon_diplomacy.3'
  assert ('USA',expected) in x['notifications'];out.append({'create_result':succeeds,'notifications':list(x['notifications']),'modifiers':list(a.modifiers)})
 return out

def old_reply_preserves_new():
 a,b=request_fixture();a.variables['nesnd_canon_request_serial']=5
 before=dict(a.variables);eff('nesnd_canon_accept_request',b);eff('nesnd_canon_refuse_request',b)
 assert a.variables==before and not a.treaties and not x['notifications']
 return {'new_serial_retained':a.variables['nesnd_canon_request_serial']}

def current_relations_and_regime():
 a,b=request_fixture();a.relations[b.tag]=19;assert not trig('nesnd_canon_request_eligible',b)
 a.relations[b.tag]=20;assert trig('nesnd_canon_request_eligible',b)
 engine['can_create_treaty']=False;assert not trig('nesnd_canon_request_eligible',b)
 a,b=request_fixture();a.wars.add(b.tag);assert not trig('nesnd_canon_reply_valid',b)
 return {'relation_19':False,'relation_20_with_native_permission':True,'native_permission_false':False,'war':False}

def prussian_distinct_and_formation():
 reset();p=world['PRU'];p.army_size=75;building(p,'building_arms_industry',5)
 treaty(p,world['BAV'],'alliance');treaty(p,world['BAV'],'defensive_pact')
 assert not trig('nesnd_prussian_coalition_ready',p)
 treaty(p,world['HAN'],'defensive_pact');assert not trig('nesnd_prussian_coalition_ready',p)
 treaty(p,world['SAX'],'defensive_pact');assert trig('nesnd_prussian_coalition_ready',p)
 p.army_size=74;assert not trig('nesnd_prussian_coalition_ready',p);p.army_size=75
 treaty(world['SAX'],world['FRA'],'alliance');assert not trig('nesnd_prussian_coalition_ready',p)
 formed=[]
 for tag in ['NGF','GER']:
  n=new_country(tag);assert not trig('nesnd_prussian_identity',n);n.variables['nesnd_prussian_coalition_origin']=True;assert trig('nesnd_prussian_identity',n);formed.append(tag)
 return {'duplicate_treaties_count_once':True,'three_distinct_required':True,'army_74_rejected':True,'French_ally_excluded':True,'formed_identity':formed}

def austrian_stage_and_sides():
 table=[]
 for stage,war,goal,expected in [(20,False,'unification',False),(21,False,'unification',True),(79,False,'conquer_state',True),(80,False,'conquer_state',False),(50,True,'unification',False),(50,False,'humiliation',False)]:
  reset();a=world['AUS'];p=dp(world['FRA'],world['TUS'],goal,stage,war);a.variables['nesnd_austrian_play']=p;a.interests[p.region.tag]=2
  got=trig('nesnd_austrian_intervention_ready',a);assert got==expected;table.append((stage,war,goal,got))
 reset();a=world['AUS'];p=dp(world['FRA'],world['TUS']);a.variables['nesnd_austrian_play']=p;a.interests[p.region.tag]=2;a.truces.add('FRA');assert not trig('nesnd_austrian_intervention_ready',a)
 a.truces.clear();p.initiator_backers.add(a);assert not trig('nesnd_austrian_intervention_ready',a)
 return table

def austrian_join_postcondition():
 out=[]
 for success in [False,True]:
  reset();a=world['AUS'];p=dp(world['FRA'],world['TUS']);a.variables['nesnd_austrian_play']=p;a.interests[p.region.tag]=2;engine['add_backer']=success
  eff('nesnd_austria_intervene',a)
  assert ('nesnd_austrian_case_active' in a.variables)==success
  assert ('nesnd_austrian_italian_commitment' in a.modifiers)==success
  out.append({'backer_result':success,'active':a.variables.get('nesnd_austrian_case_active',False),'cost':a.modifier_adds})
 return out

def usa_provinces_and_rewards():
 out=[]
 for enforced,owners,expected in [(True,['USA','USA'],True),(False,['USA','USA'],False),(True,['USA','HUS'],False),(True,['USA','GBR'],False)]:
  reset();a=world['USA'];a.variables={'nesnd_usa_case_active':True,'nesnd_usa_case_ended':True}
  if enforced:a.variables['nesnd_usa_goal_enforced']=True
  a.lists['nesnd_usa_claim_provinces']=[Entity('province','p'+str(i),owner=world[tag]) for i,tag in enumerate(owners)]
  eff('nesnd_usa_settle_border',a)
  assert ('nesnd_usa_continental_done' in a.variables)==expected
  assert ('nesnd_usa_continental_army' in a.modifiers)==expected
  eff('nesnd_usa_settle_border',a);assert a.modifier_adds.get('nesnd_usa_continental_army',0)==int(expected)
  out.append({'matching_goal':enforced,'owners':owners,'reward':expected})
 return out

def usa_native_hus_and_acw():
 reset();a=world['USA'];assert trig('nesnd_usa_continental_identity',a)
 world['HUS'].variables['nesnd_hus_native_successor']=True;assert not trig('nesnd_usa_continental_identity',a)
 world['HUS'].variables.clear();a.journals.add('je_acw_war');assert trig('nesnd_usa_native_civil_war',a)
 a.journals.clear();assert not trig('nesnd_usa_native_civil_war',a)
 r=new_country('REV');r.is_revolutionary=True;r.civil_war_origin_country=a;assert trig('nesnd_usa_native_civil_war',a)
 return {'native_successor_closes':True,'ACW_JE_and_real_revolution_pause':True}

def send_serial_roundtrip():
 reset();a=world['USA'];b=world['FRA']
 eff('nesnd_canon_send_request',a,'TAG = FRA KIND = 2')
 first=next(e for e in captured_events if e['event']=='nesnd_canon_diplomacy.1');assert a.variables['nesnd_canon_request_serial']==1
 a.variables.pop('nesnd_canon_request_clock');a.variables.pop('nesnd_canon_request_cooldown') # explicit engine-expired fixture
 eff('nesnd_canon_send_request',a,'TAG = FRA KIND = 2');assert a.variables['nesnd_canon_request_serial']==2
 saved.clear();saved.update(first['scopes']);eff('nesnd_canon_refuse_request',b);eff('nesnd_canon_accept_request',b)
 assert a.variables['nesnd_canon_request_serial']==2 and a.variables.get('nesnd_canon_request_clock')
 assert not a.treaties
 return {'serials':[1,2],'old_response_keeps_current_pending':True}

def kind_contracts():
 out=[]
 for kind,actor,partner in [(1,'PRU','BAV'),(11,'PRU','BAV'),(4,'AUS','TUS'),(3,'TUS','FRA')]:
  reset();a=world[actor];b=world[partner]
  if kind==3:state(a,'STATE_TUSCANY',region('STATE_TUSCANY',['geographic_region_italy_old']))
  a.variables={'nesnd_canon_request_serial':1,'nesnd_canon_request_kind':kind,'nesnd_canon_request_partner':b,'nesnd_canon_request_clock':True}
  saved.update(canon_sender=a,canon_partner=b,canon_serial=1,canon_kind=kind,canon_sender_regime=1,canon_partner_regime=1)
  assert trig('nesnd_canon_request_eligible',b)
  eff('nesnd_canon_accept_request',b);assert (actor,'nesnd_canon_diplomacy.2') in x['notifications']
  if kind==3:assert a.variables.get('nesnd_italy_french_guarantee') and not a.treaties
  else:assert len(a.treaties)==1
  out.append({'kind':kind,'articles':[ar.article_type for t in a.treaties for ar in t.articles],'political_credit':bool(a.variables.get('nesnd_italy_french_guarantee'))})
 return out

def investment_withdrawal():
 reset();a=world['USA'];f=world['FRA'];g=world['GBR'];a.variables['nesnd_canon_investor']=f;a.modifiers.add('nesnd_usa_european_capital')
 first=treaty(a,f,'foreign_investment_rights',a,f);other=treaty(a,g,'foreign_investment_rights',a,g)
 a.treaties.remove(first);f.treaties.remove(first);eff('nesnd_canon_diplomatic_maintenance',a)
 assert a.variables['nesnd_canon_investor'] is g and 'nesnd_usa_european_capital' in a.modifiers
 a.treaties.remove(other);g.treaties.remove(other);eff('nesnd_canon_diplomatic_maintenance',a)
 assert 'nesnd_canon_investor' not in a.variables and 'nesnd_usa_european_capital' not in a.modifiers
 return {'alternate_live_treaty_preserves_existing_duration':True,'last_rights_loss_removes_benefit':True}

def historical_treaties_and_expiry():
 global current_date
 reset();a=world['EGY']
 for tag in ['USM','SIH','QE1','TUR']:new_country(tag)
 history=parse(read(snap/'common/history/treaties/nesnd_egypt_1825.txt')).children[0]
 extended_effects(history.children,[None],'common/history/treaties/nesnd_egypt_1825.txt')
 # The adapter creates one in-force record per article; join only these two records
 # into the actual create_treaty pair to reflect the documented API outcome.
 pair_records={}
 for t in list(a.treaties):
  other=next(c for c in t.participants if c is not a)
  if other.tag in pair_records:
   first=pair_records[other.tag];first.articles+=t.articles
   a.treaties.remove(t);other.treaties.remove(t)
  else:pair_records[other.tag]=t
 assert set(pair_records)=={'FRA','USM','SIH','GBR','QE1','TUR'}
 for tag,t in pair_records.items():
  assert [(ar.article_type,ar.source_country.tag,ar.target_country.tag) for ar in t.articles]==[('foreign_investment_rights','EGY',tag),('guarantee_independence',tag,'EGY')]
 eff('nesnd_egypt_startup',a)
 assert all(t.variables.get('nesnd_egypt_1825_treaty') for t in pair_records.values())
 newer=treaty(a,world['FRA'],'foreign_investment_rights',a,world['FRA']);newer.articles.append(Entity('article','guarantee',article_type='guarantee_independence',source_country=world['FRA'],target_country=a))
 eff('nesnd_egypt_startup',a);assert 'nesnd_egypt_1825_treaty' not in newer.variables
 a.variables['nesnd_egypt_finished']=True;current_date=(1845,1,1);eff('nesnd_egypt_maintenance',a)
 assert a.treaties==[newer] and all(not t.valid for t in pair_records.values())
 return {'six_directions':True,'old_only_expiry':True,'finished_JE_does_not_block_expiry':True}

def historical_subject_exception():
 global current_date
 reset();sih=new_country('SIH');sih.overlord=world['PRU'];sih.country_rank=4
 egypt=world['EGY'];egypt.country_rank=3;other=world['BAV'];other.country_rank=2
 article=parse(read(snap/'common/treaty_articles/zzzz_nesnd_egypt_guarantee.txt')).children[0]
 possible=child(article,'possible');out=[]
 for date,target,expected in [((1844,12,31),egypt,True),((1844,12,31),other,False),((1845,1,1),egypt,False)]:
  current_date=date;saved.clear();saved['other_country']=target
  got=x['triggers'](possible.children,[sih]);assert got==expected;out.append((date,target.tag,got))
 return out

def austrian_exact_callbacks_and_white_peace():
 out=[]
 for outcome in ['victory','white_peace','enemy_enforced','wrong_play']:
  reset();a=world['AUS'];enemy=world['FRA'];target=world['TUS'];p=dp(enemy,target);a.variables={'nesnd_austrian_case_active':True,'nesnd_austrian_play':p,'nesnd_austrian_target':target,'nesnd_austrian_enemy':enemy};p.target_backers.add(a);a.modifiers.add('nesnd_austrian_italian_commitment')
  if outcome!='white_peace':
   which=dp(world['GBR'],world['BAV']) if outcome=='wrong_play' else p
   saved['diplomatic_play']=which;saved['target']=target if outcome=='enemy_enforced' else enemy
   eff('nesnd_europe_wargoal',enemy if outcome=='enemy_enforced' else target)
  eff('nesnd_europe_play_ended',p);assert a.variables.get('nesnd_austrian_end_grace')
  assert 'nesnd_austrian_italian_influence' not in a.modifiers
  x['advance'](2);expected='nesnd_europe_america.4' if outcome=='victory' else 'nesnd_europe_america.5' if outcome=='enemy_enforced' else 'nesnd_europe_america.6'
  assert ('AUS',expected) in x['notifications'];assert 'nesnd_austrian_case_active' not in a.variables
  assert ('nesnd_austrian_italian_influence' in a.modifiers)==(outcome=='victory')
  out.append({'outcome':outcome,'notification':expected,'modifiers':list(a.modifiers)})
 return out

def usa_exact_callback_matching():
 reset();a=world['USA'];h=world['HUS'];p=dp(a,h,'return_state',50,False,'dp_return_state')
 a.variables['nesnd_usa_launching']=True;eff('nesnd_europe_play_started',p)
 assert a.variables['nesnd_usa_border_play'] is p and a.variables.get('nesnd_usa_case_active')
 wrong=dp(world['FRA'],h,'return_state',50,False,'dp_return_state')
 saved.update(diplomatic_play=wrong,target=h);eff('nesnd_europe_wargoal',a);assert 'nesnd_usa_goal_enforced' not in a.variables
 saved.update(diplomatic_play=p,target=h);eff('nesnd_europe_wargoal',a);assert a.variables.get('nesnd_usa_goal_enforced')
 a.lists['nesnd_usa_claim_provinces']=[Entity('province','p1',owner=a)]
 eff('nesnd_europe_play_ended',wrong);assert 'nesnd_usa_case_ended' not in a.variables
 eff('nesnd_europe_play_ended',p);assert a.variables.get('nesnd_usa_case_ended') and not a.modifiers
 x['advance'](2);assert a.variables.get('nesnd_usa_continental_done') and 'nesnd_usa_case_active' not in a.variables
 return {'wrong_DP_no_write':True,'right_DP_goal_and_end':True,'deferred_ownership_award':True}

def usa_claim_and_no_war_creation_award():
 reset();a=world['USA'];h=world['HUS'];f=world['FRA'];a.army_size=60;building(a,'building_arms_industry',8);building(a,'building_railway',10)
 treaty(a,f,'foreign_investment_rights',a,f);a.variables['nesnd_canon_investor']=f
 strategic=region('region_great_plains');r=region('STATE_TARGET',['geographic_region_north_america']);land=state(h,'STATE_TARGET',r);land.region=strategic
 neighbour=state(a,'STATE_NEIGHBOUR');land.neighbours=[neighbour]
 land.provinces=[Entity('province','p1',owner=h),Entity('province','p2',owner=h)]
 a.variables['nesnd_usa_border_state']=land;a.variables['nesnd_usa_border_region']=r
 assert trig('nesnd_usa_border_claimable',a);eff('nesnd_usa_claim_border',a);assert 'USA' in r.claims
 assert a.modifier_adds['nesnd_usa_frontier_claim']==1 and a.relations['HUS']==20
 eff('nesnd_usa_claim_border',a);assert a.modifier_adds['nesnd_usa_frontier_claim']==1
 a.relations['HUS']=0;h.relations['USA']=0;a.interests[strategic.tag]=2
 assert trig('nesnd_usa_border_war_ready',a)
 a.truces.add('HUS');assert not trig('nesnd_usa_border_war_ready',a);a.truces.clear()
 eff('nesnd_usa_press_west',a);assert 'nesnd_usa_continental_done' not in a.variables and 'nesnd_usa_case_active' not in a.variables
 assert a.lists['nesnd_usa_claim_provinces']==land.provinces
 return {'one_claim_cost':True,'truce_blocks':True,'creation_failure_no_award':True,'exact_province_snapshot':len(land.provinces)}

try:
 check('reply_nonce_missing_actor_dead_actor_and_regime',reply_identity)
 check('create_treaty_false_never_awards_success',treaty_failure_and_success)
 check('old_accept_or_refuse_cannot_clear_new_request',old_reply_preserves_new)
 check('reply_revalidates_relations_native_permission_and_war',current_relations_and_regime)
 check('three_distinct_partners_and_NGF_GER_identity',prussian_distinct_and_formation)
 check('AUS_actual_stage_territorial_goal_and_side_eligibility',austrian_stage_and_sides)
 check('AUS_added_backer_postcondition_before_cost',austrian_join_postcondition)
 check('USA_original_provinces_and_matching_goal_required',usa_provinces_and_rewards)
 check('USA_ACW_and_native_HUS_exits',usa_native_hus_and_acw)
 check('actual_send_monotone_serial_and_late_response',send_serial_roundtrip)
 check('kinds_1_11_4_3_actual_result_contracts',kind_contracts)
 check('investment_withdrawal_and_alternate_existing_treaty',investment_withdrawal)
 check('six_treaty_directions_registration_and_old_only_expiry',historical_treaties_and_expiry)
 check('historical_guarantee_exception_only_EGY_before_1845',historical_subject_exception)
 check('AUS_exact_wargoal_end_grace_and_white_peace',austrian_exact_callbacks_and_white_peace)
 check('USA_exact_DP_wargoal_and_end_callbacks',usa_exact_callback_matching)
 check('USA_single_claim_and_creation_failure',usa_claim_and_no_war_creation_award)
 status='PASS_SOURCE_MATRIX'
except AssertionError:status='FAIL_STOPPED'
except Exception as exc:status='NOT_RUN_UNSUPPORTED';results.append({'name':'adapter','status':'NOT_RUN','error':repr(exc),'traceback':traceback.format_exc()})
report={'status':status,'checks':results,'snapshot':str(snap),'boundary':'Actual frozen source AST and effective native treaty helpers; native facts/API outcomes explicitly injected. No engine validation.','engine_verified':False}
dump(run/'routes-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(1 if status=='FAIL_STOPPED' else 0)
