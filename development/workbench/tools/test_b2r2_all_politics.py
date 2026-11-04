from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_extended_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
facts.add('total_size');base_polscalar=scalar;props.add('owner')
def scalar(n,stack):
 k=subst(n.key);v=subst(n.value);cur=stack[-1]
 if k=='strata':return cur.strata==v
 if k=='is_character_alive':return cur.alive==(v=='yes')
 if k=='is_in_exile_pool':return cur.in_exile==(v=='yes')
 return base_polscalar(n,stack)
x['scalar']=scalar;x['ns']['scalar']=scalar

def issue_fixture(issue=3):
 a,s=country_fixture();a.laws={'law_monarchy','law_oligarchy','law_tenant_farmers','law_no_workers_rights'};a.techs={'democracy','enclosure','labor_movement'};a.pop_percent={'peasants':.5};pop=Entity('pop','existing-workers',pop_type='laborers',strata='lower',total_size=50000);a.pops=[pop];s.pops=[pop]
 kind={1:'movement_land_reform',2:'movement_labor',3:'movement_liberal'}[issue];m=Entity('movement','actual-movement',movement_type=kind,owner=a,supporters=[]);a.movements=[m]
 eff('nesnd_small_begin_episode',a);assert a.variables.get('nesnd_small_episode_active') and a.variables['nesnd_small_episode_issue']==issue,(issue,a.variables)
 return a,s,m
rows=[]
try:
 for promise,issue,law in [(1,1,'law_peasant_proprietorship'),(2,1,'law_slavery_banned'),(3,2,'law_worker_protections'),(4,3,'law_hindu_caste_not_enforced'),(5,3,'law_wealth_voting')]:
  for clock_alive in [True,False]:
   a,s,m=issue_fixture(issue);eff('nesnd_small_promise_episode',a,'LAW = '+str(promise));assert a.variables['nesnd_small_promise']==promise
   if not clock_alive:a.variables.pop('nesnd_small_episode_clock')
   a.laws.add(law);eff('nesnd_small_episode_monthly',a)
   assert bool(a.variables.get('nesnd_small_reform_done'))==clock_alive,(promise,clock_alive,a.variables)
   assert ('nesnd_small_reform_law_'+str(promise) in a.variables)==clock_alive
   assert 'nesnd_small_episode_active' not in a.variables and not any('nesnd_small_reform_approval' in ig.modifiers for ig in a.igs.values())
   rows.append({'promise':promise,'issue':issue,'clock_alive':clock_alive,'reward':clock_alive,'closed':True})
 # Existing supporting native character appears materially and is cleaned up, no character creation used.
 a,s,m=issue_fixture(3);ch=Entity('character','actual-existing-spokesperson',owner=a,alive=True,in_exile=False);m.supporters=[ch];eff('nesnd_small_support_episode',a);assert a.variables['nesnd_small_episode_character'] is ch and 'nesnd_small_local_spokesperson' in ch.modifiers
 a.movements=[];eff('nesnd_small_episode_monthly',a);assert 'nesnd_small_episode_active' not in a.variables and 'nesnd_small_local_spokesperson' not in ch.modifiers
 rows.append({'existing_character':'selected and material modifier; movement absence closes and removes modifier, no creation'})
 # Old event has valid serial/regime but no original initial clock; no option becomes actionable.
 a,s,m=issue_fixture(3);a.variables.pop('nesnd_small_episode_clock');ev=defs['nesnd_small_states.10'][1];assert not trig('nesnd_small_episode_valid',a) and x['triggers'](child(ev,'cancellation_trigger').children,[a])
 rows.append({'initial_old_event_expired':'cancelled with unchanged serial/regime'})
 report={'status':'PASS_ALL_FIVE_PROMISES_AND_NATIVE_MOVEMENT_CHARACTER_CLOSURE','cases':rows,'boundary':'Actual begin/choice/monthly/cleanup AST, existing native movement/pop/character and law facts. No political movement propagation or engine character simulation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-all-politics-law-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
