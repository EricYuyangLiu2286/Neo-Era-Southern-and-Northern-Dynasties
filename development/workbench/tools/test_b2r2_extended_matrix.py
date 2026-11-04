from canon_routes_context import *
import copy,traceback,itertools
src=(W/'tools/b2r2_b2_minimal_source_cases.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
old_scalar=scalar;old_effects=x['effects'];facts.update({'population','size','political_strength','liberty_desire'})
def scalar(n,stack):
 k=subst(n.key);v=subst(n.value);cur=stack[-1]
 if k.startswith('relations:'):return cmp[n.op](resolve(k,stack),x['number'](v,stack))
 if k in ['prev','root']:
  obj=resolve(k,stack)
  if n.children is not None:
   if obj is None:raise Unsupported('missing native scope '+k)
   return x['triggers'](n.children,stack+[obj])
  return cmp[n.op](obj,resolve(v,stack))
 if '.' in k and n.children is None and not k.startswith('relations('):
  left=resolve(k,stack);right=resolve(v,stack)
  if left is None and n.op!='?=':raise Unsupported('unguarded chained scalar '+k)
  return cmp[n.op](left,right)
 if k in facts:return cmp[n.op](getattr(cur,k),x['number'](v,stack))
 if k.startswith('ig:'):
  target=resolve(k,stack)
  if target is None:raise Unsupported('missing IG '+k)
  return x['triggers'](n.children,stack+[target])
 if k=='in_default':return cur.in_default==(v=='yes')
 if k=='is_in_government':return cur.in_government==(v=='yes')
 if k=='institution_investment_level':
  test=child(n,'value');return cmp[test.op](cur.institutions.get(subst(child(n,'institution').value),0),x['number'](test.value,stack))
 if k=='pop_type_percent_country':
  test=child(n,'percent');return cmp[test.op](cur.pop_percent.get(subst(child(n,'pop_type').value),0),x['number'](test.value,stack))
 if k=='is_pop_type':return cur.pop_type==v
 if k=='is_strata':return cur.strata==v
 if k=='has_government_type':return cur.government_type==v
 if k=='economic_dependence':
  target=resolve(child(n,'target').value,stack);test=child(n,'value');return cmp[test.op](cur.dependence[target.tag],x['number'](test.value,stack))
 if k=='is_adjacent_to_country':return resolve(v,stack) in cur.adjacent
 return old_scalar(n,stack)
x['scalar']=scalar;x['ns']['scalar']=scalar

def effects(nodes,stack,path):
 for n in nodes or []:
  k=subst(n.key);cur=stack[-1]
  if k=='if':
   # Process whole ordered chain together, not sibling nodes separately.
   return effect_sequence(nodes,stack,path)
  effect_sequence([n],stack,path)
def effect_sequence(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);cur=stack[-1]
  if k=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:effect_sequence(body(chosen),stack,path)
  elif k in ['ordered_scope_state','every_scope_state','every_scope_pop','every_scope_building','random_political_movement','random_supporting_character']:
   items=list(cur.states if 'scope_state' in k else cur.pops if k=='every_scope_pop' else cur.buildings if k=='every_scope_building' else cur.movements if k=='random_political_movement' else cur.supporters)
   limit=child(n,'limit');items=[z for z in items if x['triggers'](limit.children if limit else [],stack+[z])]
   if k=='ordered_scope_state':
    order=child(n,'order_by');items.sort(key=lambda z:x['number'](order.value,stack+[z]),reverse=True);pos=int(child(n,'position').value) if child(n,'position') else 0;items=items[pos:pos+1]
   elif k.startswith('random_'):items=items[:1]
   for z in items:effect_sequence([c for c in body(n) if c.key not in ["order_by","position","check_range_bounds","max"]],stack+[z],path)
  elif k=='change_variable':
   name=subst(child(n,'name').value);add=child(n,'add');cur.variables[name]=cur.variables.get(name,0)+x['number'](add.children if add.children else add.value,stack)
  elif k.startswith('ig:'):
   target=resolve(k,stack)
   if target is None:raise Unsupported('missing actual IG '+k)
   effect_sequence(n.children,stack+[target],path)
  elif k in ['add_radicals','add_loyalists']:
   native_effects.append((cur.tag,k,shape(n)))
  else:old_effects([n],stack,path)
x['effects']=effect_sequence
native_effects=[]
def country_fixture(tag='ACE',strategic='region_indonesia',pop=100000):
 a,land=fixture()
 if tag!='ACE':
  world.pop('ACE');a.tag=tag;world[tag]=a
 a.in_default=False;a.institutions={'institution_schools':1,'institution_police':1};a.pop_percent={};a.government_type='gov_monarchy';a.dependence={};a.adjacent=set();a.liberty_desire=80
 for c in world.values():
  c.in_default=False;c.institutions=getattr(c,'institutions',{});c.igs=getattr(c,'igs',{});c.movements=getattr(c,'movements',[]);c.has_revolution=False
 for key in ['ig_landowners','ig_industrialists','ig_intelligentsia','ig_armed_forces','ig_rural_folk','ig_trade_unions']:a.igs[key]=Entity('interest_group',key,in_government=(key=='ig_landowners'),owner=a)
 land.region=region(strategic);land.state_population=pop;land.pops=[]
 return a,land

def identity_matrix():
 indian=sorted({n.key[2:] for n in defs['nesnd_india_prince'][1].walk() if n.key and n.key.startswith('c:')});southern=sorted({n.key[2:] for n in defs['nesnd_small_southern_identity'][1].walk() if n.key and n.key.startswith('c:')}|{'BUR','SIA'})
 out=[]
 for tags,good in [(indian,'region_north_india'),(southern,'region_indonesia')]:
  for tag in tags:
   a,s=country_fixture(tag,good);assert trig('nesnd_small_state_country',a);s.region=region('region_western_europe');assert not trig('nesnd_small_state_country',a);s.region=region(good);s.owner=world['FRA'];assert not trig('nesnd_small_state_country',a);out.append({'tag':tag,'good_region':good,'foreign_region_rejected':True,'foreign_owner_rejected':True})
 for tag in ['MUG','BHT','DRA','TZ1','YU1','IR1','IR2','IR3','IR4','IR5','IR6']:
  a,s=country_fixture(tag);a.variables['nesnd_small_southern_line']=True;assert not trig('nesnd_small_state_country',a)
 a,s=country_fixture('ACE');a.variables['nesnd_small_southern_line']=True;world.pop('ACE');a.tag='ZZZ';world['ZZZ']=a;assert trig('nesnd_small_state_country',a);a.variables['nesnd_india_imperial_line']=True;assert not trig('nesnd_small_state_country',a)
 return {'countries':len(out),'indian':len(indian),'southern':len(southern),'rows':out}

def zero_and_regions():
 a,s=country_fixture();s.state_population=0
 for v in ['nesnd_small_population','nesnd_small_job_coverage','nesnd_small_transport','nesnd_small_candidate_one_share','nesnd_small_candidate_two_share','nesnd_small_group_one_share','nesnd_small_group_two_share','nesnd_small_group_one_transport','nesnd_small_group_two_transport']:
  assert val(v,a)==0,(v,val(v,a))
 rows=[]
 cases=[('YN1','region_oceania',['STATE_NEW_SOUTH_WALES','STATE_NORTH_ISLAND']),('BUR','region_indochina',['STATE_MANDALAY','STATE_PEGU']),('SIA','region_indochina',['STATE_BANGKOK','STATE_NAKHON_RATCHASIMA']),('HYD','region_south_india',['STATE_HYDERABAD','STATE_MADRAS'])]
 for tag,reg,states in cases:
  a,s=country_fixture(tag,reg,1200000);s.state_region=region(states[0]);b=state(a,states[1]);b.region=s.region;b.state_population=800000;b.market_access=.8;b.state_unemployment_rate=0;b.pops=[]
  eff('nesnd_small_refresh_candidates',a);valid=trig('nesnd_small_candidate_valid',a);rows.append({'tag':tag,'valid':valid,'group_one':val('nesnd_small_candidate_one_pop',a),'group_two':val('nesnd_small_candidate_two_pop',a),'scale':val('nesnd_small_scale',a)})
  assert valid,(tag,rows[-1]);eff('nesnd_small_initialize',a);assert trig('nesnd_small_targets_valid',a);b.owner=world['FRA'];assert not trig('nesnd_small_targets_valid',a)
 return {'zero_denominators':'all9 zero','geographic_cases':rows}

if __name__=='__main__':
 results=[]
 for name,fn in [('73_country_actual_identity_territory',identity_matrix),('zero_and_special_region_registration',zero_and_regions)]:
  try:results.append({'name':name,'status':'PASS','detail':fn()})
  except Exception as exc:
   results.append({'name':name,'status':'FAIL_OR_ADAPTER_UNRESOLVED','error':repr(exc),'traceback':traceback.format_exc()});break
 dump(run/'b2r2-extended-source-matrix.json',{'checks':results,'engine_verified':False,'boundary':'Frozen ordered AST, actual primitives/state facts injected. Unknown syntax is explicit tool limitation, not automatically MOD bug.'});print(json.dumps(results,ensure_ascii=False,indent=2))


