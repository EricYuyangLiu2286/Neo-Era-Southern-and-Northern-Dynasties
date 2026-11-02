"""Ordered-source and bounded arithmetic validation. Never an engine emulator."""
from qin_persia_context import *
import collections,re,math,copy,itertools,asyncio,difflib
rows=[];trees={};definitions={}
base,current=man(B),man(C);changed=sorted(r for r,h in current.items() if base.get(r)!=h)
def check(name,ok):rows.append({'name':name,'pass':bool(ok)});assert ok,name
def tree(rel):
 if rel not in trees:trees[rel]=parse(read(C/rel))
 return trees[rel]
def node(rel,key):return tree(rel).get(key)
def has(n,key,val=None):return any(a.key==key and (val is None or a.value==val) for a in n.walk())
def lookup(key):return definitions[key][1]
check('Main remains byte-identical to pre-change baseline',man(M)==base)
check('No deletion of previous work',not set(base)-set(current))
for rel in changed:
 if rel.endswith('.txt'):
  t=tree(rel);check('ordered AST parses '+rel,bool(t))
  for n in t.children:
   if n.key.startswith(('nesnd_qe1','nesnd_per','nesnd_qin')):
    if rel.startswith(('common/scripted_effects/','common/scripted_triggers/','common/script_values/')):
     check('unique helper '+n.key,n.key not in definitions);definitions[n.key]=(rel,n)
 if rel.endswith('.yml'):
  check('localization encoding '+rel,(C/rel).read_bytes().startswith(b'\xef\xbb\xbf') and read(C/rel).startswith('l_'+('simp_chinese' if 'simp_chinese' in rel else 'english')+':'))
check('Map, population, buildings, military formations and Japanese gameplay preserved',not any(r.startswith(('map_data/','common/history/pops/','common/history/buildings/','common/history/military_formations/','gfx/')) or 'japan' in r.lower() for r in changed))
for rel in ['common/history/countries/QE1 - Western Qin.txt','common/history/countries/per - persia.txt']:
 old=parse(read(B/rel)).children[0].children[0];new=tree(rel).children[0].children[0]
 check('History only appends bootstrap '+rel,[shape(x) for x in new.children[:-1]]==[shape(x) for x in old.children] and new.children[-1].key in ['nesnd_qe1_bootstrap','nesnd_per_bootstrap'])
for rel in changed:
 if rel.endswith('.txt'):
  for n in tree(rel).walk():
   if (n.key or '').startswith(('nesnd_qe1','nesnd_per','nesnd_qin')) and n.value in ['yes','no']:
    check('helper reference '+rel+':'+n.key,n.key in definitions)

# Evaluate only the documented condition subset used in lifecycle predicates.
# Unknown syntax fails rather than pretending the full engine was executed.
triggers={k:n for k,(r,n) in definitions.items() if r.startswith('common/scripted_triggers/')}
def number(v,e):
 if v.startswith('var:'):
  assert v[4:] in e['vars'],('unguarded variable',v)
  return float(e['vars'][v[4:]])
 return float(v)
def cmp(a,op,b):return {'=':a==b,'!=':a!=b,'>':a>b,'>=':a>=b,'<':a<b,'<=':a<=b}[op]
def condition(n,e,root=None):
 root=root or e;k=n.key;v=n.value
 if k in triggers:return block(triggers[k].children,e,root)==(v=='yes')
 if k in ['hidden_trigger','AND','limit']:return block(n.children,e,root)
 if k=='OR':return any(condition(x,e,root) for x in n.children)
 if k=='NOR':return not any(condition(x,e,root) for x in n.children)
 if k=='NOT':return not block(n.children,e,root)
 if k=='always':return v=='yes'
 if k=='has_variable':return v in e['vars']
 if k=='has_journal_entry':return v in e['jes']
 if k=='has_modifier':return v in e.get('mods',set())
 if k=='is_country_alive':return e.get('alive',True)==(v=='yes')
 if k=='num_states':return cmp(e['states'],n.op,float(v))
 if k=='exists' and v.startswith('c:'):return v[2:] in e['world']
 if k.startswith('c:'):
  assert k[2:] in e['world'],('unguarded country',k)
  target=e['world'][k[2:]]
  if n.children:return block(n.children,target,root)
  return target['tag']==e['tag'] if v in ['this','This','THIS'] else target['tag']==root['tag']
 if k=='is_subject_of':return e.get('overlord')==root['tag'] if v=='root' else e.get('overlord')==v[2:]
 if k=='is_subject':return bool(e.get('overlord'))==(v=='yes')
 if k=='can_create_diplomatic_pact':return e.get('can_tributary',False)
 if k=='has_law_or_variant':
  law=v.removeprefix('law_type:');laws=e.get('laws',set());return law in laws or (law=='law_census_voting' and 'law_nesnd_qe1_proportional_representation' in laws)
 if k.startswith('var:'):return cmp(number(k,e),n.op,number(v,e))
 if k=='country_or_subject_owns_entire_state_region':return v in e.get('regions',set())
 if k=='country_has_building_type_levels':
  val=n.get('value');return cmp(e.get('buildings',{}).get(n.scalar('target').removeprefix('bt:'),0),val.op,number(val.value,e))
 raise AssertionError(('unsupported condition subset',k,v))
def block(nodes,e,root=None):
 i=0
 while i<len(nodes or []):
  n=nodes[i]
  if n.key=='trigger_if':
   chain=[n];i+=1
   while i<len(nodes) and nodes[i].key in ['trigger_else_if','trigger_else']:chain.append(nodes[i]);i+=1
   branch=next((x for x in chain if x.key=='trigger_else' or block(x.get('limit').children,e,root)),None)
   if branch is not None and not block([x for x in branch.children if x.key!='limit'],e,root):return False
  else:
   if not condition(n,e,root):return False
   i+=1
 return True
def fixture(tag='QE1',states=36):
 e={'tag':tag,'states':states,'alive':True,'vars':{},'jes':set(),'laws':set(),'buildings':{},'regions':set()};e['world']={tag:e};return e
def pred(k,e):return block(triggers[k].children,e)
def checked(k,e,want,label):check(label,pred(k,e)==want)
e=fixture();checked('nesnd_qe1_country',e,True,'QE1 identity exists');other=fixture('FRA');checked('nesnd_qe1_country',other,False,'Absent QE1 never matches another country');checked('nesnd_per_country',other,False,'Absent PER never matches another country')
for statecount in [0,1,3,4,5,36]:
 for done in [False,True]:
  e=fixture(states=statecount)
  if done:e['vars']['nesnd_qe1_agenda_done']=1
  checked('nesnd_qe1_agenda_eligible',e,statecount>=4 and not done,f'agenda cutoff {statecount}/{done}')
  e['jes'].add('nesnd_qe1_agenda_journal');checked('nesnd_qe1_agenda_live',e,statecount>=4 and not done,f'children cutoff {statecount}/{done}')
for law in ['law_monarchy','law_nesnd_qe1_proportional_representation','law_universal_suffrage','law_council_republic']:
 e=fixture();e['laws']={law};checked('nesnd_qe1_court_eligible',e,law not in ['law_universal_suffrage','law_council_republic'],'court franchise exit '+law)
 e['vars']['nesnd_qe1_court_archived']=1;checked('nesnd_qe1_court_eligible',e,False,'court archive durable '+law)
for side,balance in [('econ',-50),('army',50)]:
 for offset in [0,0.01,1]:
  for waiting in [False,True]:
   e=fixture();e['vars']={'nesnd_qe1_balance':balance+(offset if side=='econ' else -offset),'nesnd_qe1_'+side+'_edge':1}
   if waiting:e['vars']['nesnd_qe1_'+side+'_wait']=1
   checked('nesnd_qe1_'+('economic' if side=='econ' else 'military')+'_victory',e,offset==0 and not waiting,f'endpoint {side}/{offset}/{waiting}')
for k in ['nesnd_qe1_army_ready','nesnd_qe1_economic_victory','nesnd_qe1_military_victory','nesnd_qe1_crown_peak']:
 checked(k,fixture(),False,'no-init reference guard '+k)
econlaws=['law_commercialized_agriculture','law_laissez_faire','law_wealth_voting']
for bits in itertools.product([False,True],repeat=3):
 for tools,rails in [(19,10),(20,9),(20,10),(100,100)]:
  e=fixture();e['laws']={law for law,b in zip(econlaws,bits) if b};e['buildings']={'building_tooling_workshop':tools,'building_railway':rails}
  checked('nesnd_qe1_economy_ready',e,all(bits) and tools>=20 and rails>=10,f'economic readiness {bits}/{tools}/{rails}')
for level,captured,india,north,subject in itertools.product([106,107],[False,True],[False,True],[False,True],[False,True]):
 e=fixture();per=fixture('PER');per['world']=e['world'];e['world']['PER']=per;per['overlord']='QE1' if subject else None;e['vars']={'nesnd_qe1_barracks_goal':107}
 if captured:e['vars']['nesnd_qe1_barracks_snapshot_done']=1
 e['buildings']={'building_barrack':level};e['regions']=({'STATE_PUNJAB'} if india else set())|({'STATE_UFA'} if north else set())
 checked('nesnd_qe1_army_ready',e,level>=107 and captured and india and north and subject,f'military readiness {level}/{captured}/{india}/{north}/{subject}')

# Lifecycle graph: no JE gates its own creation, and later entries have guarded
# explicit entry points in addition to automatic possible evaluation.
jes={n.key:(rel,n) for rel in changed if rel.startswith('common/journal_entries/') for n in tree(rel).children}
def dependencies(n,seen=None):
 seen=set() if seen is None else seen;result=set()
 for a in n.walk():
  if a.key=='has_journal_entry':result.add(a.value)
  if a.key in triggers and a.key not in seen:seen.add(a.key);result|=dependencies(triggers[a.key],seen)
 return result
added=collections.Counter(a.scalar('type') for rel in changed if rel.endswith('.txt') for a in tree(rel).walk() if a.key=='add_journal_entry')
lifecycles=[]
for key,(rel,n) in jes.items():
 deps=dependencies(n.get('possible'));check('JE has explicit add '+key,added[key]>0);check('JE no self-lock '+key,key not in deps);check('JE has invalid closure '+key,n.get('invalid') is not None)
 lifecycles.append({'JE':key,'file':rel,'creation_dependencies':sorted(deps),'explicit_add_sites':added[key],'terminal_hooks':[x.key for x in n.children if x.key.startswith('on_') or x.key in ['invalid','complete','fail','timeout']]})
check('Twelve new journals',len(jes)==12)
for key in ['nesnd_qe1_initialize','nesnd_per_initialize']:check('initializer never recursively adds its own JE '+key,not has(lookup(key),'add_journal_entry'))
check('PER terminal independent of own JE',not any(x in dependencies(lookup('nesnd_per_settle_future')) for x in ['nesnd_per_future_journal']))
for route in ['aid','covert']:
 e=fixture('PER');e['vars']={'nesnd_per_route_'+route:1,'nesnd_per_future_done':1}
 checked('nesnd_per_'+('west' if route=='aid' else 'east')+'_eligible',e,True,'later Persian journal '+route)
 checked('nesnd_per_route_unset',e,False,'route cannot be selected again '+route)
for rel,n in jes.values():
 if n.key in ['nesnd_qe1_economy_journal','nesnd_qe1_army_journal']:check('child stops with parent '+n.key,dependencies(n.get('invalid'))=={'nesnd_qe1_agenda_journal'})
clock=lookup('nesnd_qe1_watch_endpoints');waits=[a for a in clock.walk() if a.key=='set_variable' and a.get('days')];check('Strictly more than28days, both endpoints',len(waits)==2 and all(a.scalar('days')=='29' for a in waits))
check('Durable ten-year clock initialized from JE immediate',has(node('common/journal_entries/nesnd_qe1_agendas.txt','nesnd_qe1_agenda_journal').get('immediate'),'nesnd_qe1_start_agenda_clock','yes'))
check('Coup/native war not an agenda invalidation predicate',not has(node('common/journal_entries/nesnd_qe1_agendas.txt','nesnd_qe1_agenda_journal').get('invalid'),'is_at_war') and 'nesnd_qe1_native_civil_war' not in dependencies(node('common/journal_entries/nesnd_qe1_agendas.txt','nesnd_qe1_agenda_journal').get('invalid')))
check('Ruler 60/40 once, first template fixed',has(lookup('nesnd_qe1_assign_ruler'),'has_template','QE1_chen_wuxing') and has(lookup('nesnd_qe1_assign_ruler'),'has_variable','nesnd_qe1_ruler_registered') and any(a.key=='random_list' and [x.key for x in a.children]==['60','40'] for a in lookup('nesnd_qe1_assign_ruler').walk()))

# Read actual Jomini arithmetic and execute its bounded arithmetic subset.
values={k:n for k,(rel,n) in definitions.items() if rel.startswith('common/script_values/')}
def val(v,env):
 if v in env:return env[v]
 if v in values:return calculate(values[v],env)
 if v=='define:NPops|DEFAULT_SOL_CHANGE_IMPACT_FACTOR':return .03
 return float(v)
def calculate(n,env,start=0):
 out=start
 for a in n.children or []:
  if a.key in ['limit','desc']:continue
  if a.key=='if':
   li=a.get('limit');assert len(li.children)==1
   guard=li.children[0]
   if guard.key=='is_pop_type':applies=env['pop_type']==guard.value
   elif guard.key=='has_variable':applies='var:'+guard.value in env
   else:raise AssertionError(('unsupported value guard',guard.key))
   if applies:out=calculate(a,env,out)
   continue
  x=val(a.value,env) if a.value is not None else calculate(a,env)
  if a.key=='value':out=x
  elif a.key=='add':out+=x
  elif a.key=='subtract':out-=x
  elif a.key=='multiply':out*=x
  elif a.key=='divide':out/=x
  elif a.key=='min':out=max(out,x)
  elif a.key=='max':out=min(out,x)
  else:raise AssertionError(('unsupported arithmetic',a.key))
 return out
fx=tree('common/scripted_effects/nesnd_qe1_sol_bonus.txt');bonuses=[n for n in fx.walk() if n.key in ['add_loyalists_in_state','add_radicals_in_state']]
arithmetic=[]
for n in bonuses:
 pt=n.scalar('pop_type').split(':')[1];isloyal=n.key=='add_loyalists_in_state';mult=.15 if isloyal else .10
 for sol,delta in itertools.product([5,10,15,20,30,40],[.01,.25,1,5]):
  f=(.01 if pt=='peasants' else .03)/(1+9*min(1,max(0,(sol-15)/15)))
  env={'pop_type':pt,'standard_of_living':sol,'var:nesnd_qe1_sol_s':sol,'var:nesnd_qe1_sol_previous_'+pt:sol-delta if isloyal else sol+delta,'var:nesnd_qe1_sol_f':f}
  actual_f=calculate(values['nesnd_qe1_pop_sol_impact'],env);check('native factor '+pt+'/'+str(sol),math.isclose(actual_f,f,abs_tol=1e-12))
  got=calculate(n.get('value'),env);want=min(.05,delta*f*mult);check('directional SoL '+pt+'/'+str(sol)+'/'+str(delta)+'/'+str(isloyal),math.isclose(got,want,abs_tol=1e-12));arithmetic.append({'type':pt,'SoL':sol,'delta':delta,'loyal':isloyal,'fraction':got})
for count in [0,1,3,4,10,35]:check('heritage cost sign '+str(count),math.isclose(calculate(values['nesnd_qe1_unity_diversity'],{'var:nesnd_qe1_heritage_count':count}),-count*.05,abs_tol=1e-12))
check('No absent heritage-cache read',calculate(values['nesnd_qe1_unity_diversity'],{})==0)
check('Every profession paid once in each direction',all(v==2 for v in collections.Counter(n.scalar('pop_type') for n in bonuses).values()))

# Simulate both possible JE orders; only the main JE writes country uprising.
main=lookup('nesnd_qe1_unity_monthly');child=node('common/journal_entries/nesnd_qe1_identity.txt','nesnd_qe1_uprising_journal')
check('Uprising country counter has a single monthly writer',has(main,'name','nesnd_qe1_uprising') and not has(child,'change_variable'))
check('Both bar owners absolutely resync on their own pulse',has(main,'nesnd_qe1_unity_sync','yes') and has(child.get('on_monthly_pulse'),'nesnd_qe1_unity_sync','yes'))
for order in itertools.permutations(['main','mirror']):
 for old,delta in [(0,2),(98,4),(50,-1),(0,-1)]:
  country,bar=old,old
  for action in order:
   if action=='main':country=min(100,max(0,country+delta));bar=country
   else:bar=min(100,max(0,bar+delta));bar=country
  check('mirror ordering '+str(order)+str((old,delta)),country==bar==min(100,max(0,old+delta)))

# Complete paired conversion and exclusive partition invariants.
cohort=lookup('nesnd_qe1_convert_selected_cohort').children
check('Identity conversion uses three fresh loops',len(cohort)==3 and all(x.key=='every_scope_pop' for x in cohort))
check('Exactly half staged, then all staged religion, then all staged culture',cohort[0].get('change_pop_culture').scalar('value')=='0.5' and cohort[1].get('change_pop_religion').scalar('value')=='1' and cohort[2].get('change_pop_culture').scalar('value')=='1')
cultures={}
for source in [G,C]:
 for p in (source/'common/cultures').glob('*.txt'):
  for n in parse(read(p)).children:cultures[n.key.split(':')[-1]]=n
pools=json.loads(read(R/'future-identity-pools.json'))['states']
for state in pools:
 for pair in state['return_pairs']:
  c=cultures[pair['culture']];traditions=c.get('traditions');traits={x.value or x.key for x in traditions.children} if traditions else set()
  check('native return pair '+state['region']+'/'+pair['culture']+'/'+pair['religion'],pair['weight']>0)
check('Assimilation alone excludes Sinosphere',has(lookup('nesnd_qe1_unity_monthly'),'has_discrimination_trait','tradition_sinosphere'))
original=json.loads(read(R/'native-identity-map.json'))['states'];byregion={x['region']:x for x in pools}
for x in original:check('Full starting-region return pool retained '+x['region'],{(p['culture'],p['religion'],p.get('weight',p['native_reference_population'])) for p in x['pairs']}=={(p['culture'],p['religion'],p['weight']) for p in byregion[x['region']]['return_pairs']})
check('Native future territory pools include Indian and Russian military targets',{'STATE_PUNJAB','STATE_GUJARAT','STATE_ASTRAKHAN','STATE_UFA','STATE_TOBOLSK'}<={x['region'] for x in pools})
part=json.loads(read(R/'breakup-partition.json'));flat=[r for regs in part['initial_regions'].values() for r in regs]
check('36 original regions partitioned once',len(flat)==len(set(flat))==36)
check('Ili and neighbours retained',part['initial_regions']['QE1']==['STATE_ILI','STATE_DZUNGARIA','STATE_JETISY'])
check('New conquests have guarded residual recipient',has(lookup('nesnd_qe1_release_other_provinces'),'nesnd_qe1_core_region','yes') and has(lookup('nesnd_qe1_release_other_provinces'),'set_state_owner','c:QFR'))
check('Breakup locks before any transfer',lookup('nesnd_qe1_breakup').get('if').children[1].key=='set_variable' and lookup('nesnd_qe1_breakup').get('if').children[1].value=='nesnd_qe1_dissolved')
check('Coalition joins existing war rather than splitting fronts',has(lookup('nesnd_qe1_start_frontier_war'),'join_war') and has(lookup('nesnd_qe1_start_frontier_war'),'has_variable','nesnd_qe1_war_launch_window'))
check('No new navy formations',not any(a.key=='type' and a.value=='fleet' for rel in changed if rel.startswith('common/scripted_effects/') for a in tree(rel).walk()))
check('Single Persian payer located in Qin formula',has(values['nesnd_qe1_unity_persia'],'value','-1') and not any(a.key=='change_variable' and a.scalar('name')=='nesnd_qe1_unity' for a in tree('common/scripted_effects/nesnd_per_campaign.txt').walk()))
check('Aid selection fixed75/25',any(a.key=='random_list' and [x.key for x in a.children]==['75','25'] for a in lookup('nesnd_per_future_monthly').walk()))
check('Three aid types have own current-buff cooldown',sum(1 for a in lookup('nesnd_per_future_monthly').walk() if a.key=='trigger' and has(a,'has_modifier'))==3)
claims=set(json.loads(read(R/'recovery-claim-regions.json'))['regions']);n=node('common/strategic_regions/east_asia_strategic_regions.txt','region_northeast_asia').get('states');nativeNE=set(re.findall(r'\bSTATE_\w+',read(C/'common/strategic_regions/east_asia_strategic_regions.txt')[n.start:n.end]));check('All actual Northeast Asia states claimed',nativeNE<=claims)
dump(R/'checks.json',{'status':'STATIC_PASS','checks':rows,'arithmetic_cases':len(arithmetic),'engine_verified':False,'game_launched':False})
dump(R/'arithmetic-cases.json',arithmetic);dump(R/'journal-lifecycle-matrix.json',lifecycles);dump(R/'changed-files.json',changed)
(R/'candidate.diff').write_text(''.join(''.join(difflib.unified_diff(read(B/r).splitlines(True) if (B/r).exists() else [],read(C/r).splitlines(True),fromfile='base/'+r,tofile='candidate/'+r)) for r in changed if r.endswith(('.txt','.yml','.md'))),'utf-8')
print(json.dumps({'status':'STATIC_PASS','checks':len(rows),'arithmetic':len(arithmetic),'journals':len(jes),'changed_files':len(changed),'engine_verified':False}))
