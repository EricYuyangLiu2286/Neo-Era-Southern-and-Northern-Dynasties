from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_extended_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
def regional_threshold_retarget():
 a,s=country_fixture(pop=1200000);s.state_region=region('STATE_ACEH');b=state(a,'STATE_OTHER');b.region=s.region;b.state_population=799999;b.market_access=1;b.state_unemployment_rate=0;b.pops=[];b.average_sol=12;b.turmoil=0
 eff('nesnd_small_initialize',a);assert 'nesnd_small_regional' not in a.variables
 for _ in range(6):eff('nesnd_small_monthly',a)
 assert 'nesnd_small_regional' not in a.variables
 b.state_population=800000
 for _ in range(5):eff('nesnd_small_monthly',a)
 assert 'nesnd_small_regional' not in a.variables
 eff('nesnd_small_monthly',a);assert a.variables.get('nesnd_small_regional') and trig('nesnd_small_targets_valid',a)
 initial_epoch=a.variables['nesnd_small_epoch'];s.state_population=900000;b.state_population=600000
 for _ in range(6):eff('nesnd_small_monthly',a)
 assert a.variables.get('nesnd_small_regional')
 b.state_population=599999
 for _ in range(5):eff('nesnd_small_monthly',a)
 assert a.variables.get('nesnd_small_regional')
 eff('nesnd_small_monthly',a);assert 'nesnd_small_regional' not in a.variables
 # Actual loss of anchor ownership invalidates; remaining two eligible own states can be re-registered.
 a.variables['nesnd_small_regional']=True;b.owner=world['FRA'];assert not trig('nesnd_small_targets_valid',a)
 c=state(a,'STATE_THIRD');c.region=s.region;c.state_population=900000;c.market_access=1;c.state_unemployment_rate=0;c.pops=[];c.average_sol=12;c.turmoil=0
 assert trig('nesnd_small_can_retarget',a);eff('nesnd_small_retarget',a)
 assert a.variables['nesnd_small_epoch']==initial_epoch+1 and trig('nesnd_small_targets_valid',a)
 assert 'nesnd_small_retarget_cooldown' in a.variables and b.variables['nesnd_small_region_epoch']==initial_epoch
 return {'upgrade':'2m needs6 months; below no upgrade','decline':'exact1.5m retained; below requires6 months','owner_loss':'invalidates old target; own new targets epoch+1; foreign state old mark not reused','retarget_cooldown':True}

def political_mutual_exclusion():
 rows=[]
 for choice in ['organise','promise','suppress']:
  a,s=country_fixture();m=Entity('movement','liberal',movement_type='movement_liberal',owner=a,supporters=[]);a.movements=[m]
  p=Entity('pop','workers',pop_type='laborers',strata='lower',population=50000,size=50000,political_strength=100);s.pops=[p];a.laws={'law_oligarchy'}
  a.variables.update(nesnd_small_episode_active=True,nesnd_small_episode_clock=True,nesnd_small_episode_serial=1,nesnd_small_episode_issue=3,nesnd_small_episode_regime=val('nesnd_canon_regime',a));saved.update(small_episode_serial=1,small_episode_regime=val('nesnd_canon_regime',a))
  assert trig('nesnd_small_episode_valid',a)
  if choice=='organise':eff('nesnd_small_support_episode',a)
  elif choice=='promise':eff('nesnd_small_promise_episode',a,'LAW = 5')
  else:eff('nesnd_small_suppress_episode',a)
  picked=a.variables.get('nesnd_small_episode_choice');assert picked=={'organise':1,'promise':2,'suppress':3}[choice]
  assert not trig('nesnd_small_episode_valid',a)
  before=copy.copy(a.variables);eff('nesnd_small_support_episode',a);eff('nesnd_small_promise_episode',a,'LAW = 5');eff('nesnd_small_suppress_episode',a);assert a.variables==before
  a.has_revolution=True;eff('nesnd_small_episode_monthly',a);assert 'nesnd_small_episode_active' not in a.variables and not any(x.startswith(('nesnd_small_organise_','nesnd_small_suppress_')) for x in a.modifiers)
  rows.append({'chosen':choice,'mutually_exclusive':True,'revolution_closes':True})
 return rows
results=[]
for name,fn in [('population_hysteresis_and_owned_retarget',regional_threshold_retarget),('three_real_movement_choices_revolution_cleanup',political_mutual_exclusion)]:
 try:results.append({'name':name,'status':'PASS','detail':fn()})
 except Exception as e:results.append({'name':name,'status':'FAIL_OR_ADAPTER_UNRESOLVED','error':repr(e),'traceback':traceback.format_exc()});break
dump(run/'b2r2-threshold-politics-matrix.json',{'checks':results,'boundary':'Actual source AST and native movement/pop/state facts; no game simulation.'});print(json.dumps(results,ensure_ascii=False,indent=2))

