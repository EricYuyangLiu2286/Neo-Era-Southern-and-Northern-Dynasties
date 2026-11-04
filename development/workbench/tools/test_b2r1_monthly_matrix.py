from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r1_extended_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
def productive_fixture():
 a,s=country_fixture();a.laws={'law_appointed_bureaucrats'};a.techs=set();a.army_size=2;s.market_access=1;s.state_unemployment_rate=0
 for typ,level in [('building_rice_farm',1),('building_government_administration',1),('building_barrack',1)]:
  b=building(a,typ,level);b.weekly_profit=10;b.is_subsidized=False;b.shortage=False;s.buildings.append(b)
 return a,s

def cumulative_and_terminal():
 a,s=productive_fixture()
 for i in range(6):eff('nesnd_small_monthly',a)
 assert a.variables['nesnd_small_economy_months']==6
 s.state_unemployment_rate=.2;eff('nesnd_small_monthly',a);assert a.variables['nesnd_small_economy_months']==6;s.state_unemployment_rate=0
 for i in range(6):eff('nesnd_small_monthly',a)
 assert 'nesnd_small_economy_done' in a.variables and a.modifier_adds['nesnd_small_livelihood']==1
 for i in range(12):eff('nesnd_small_monthly',a)
 assert 'nesnd_small_governance_done' in a.variables and a.modifier_adds['nesnd_small_learning']==1
 eff('nesnd_small_choose_order',a);assert 'nesnd_small_order_active' in a.variables
 for i in range(24):eff('nesnd_small_monthly',a)
 assert a.variables.get('nesnd_small_order_rewarded') and a.modifier_adds['nesnd_small_order']==1
 eff('nesnd_small_choose_order',a);eff('nesnd_small_monthly',a);assert 'nesnd_small_order_active' not in a.variables
 for _ in range(2):eff('nesnd_small_economy_reward',a);eff('nesnd_small_governance_reward',a)
 assert a.modifier_adds['nesnd_small_livelihood']==1 and a.modifier_adds['nesnd_small_learning']==1
 return {'economy':'6 good +1 bad +6 good cumulative12','governance':'next12 ticks','order':'24 independent ticks','permanent_reward_receipts':True,'modifiers_added_once':dict(a.modifier_adds)}

def terminal_switch_and_cleanup():
 rows=[]
 for original_subject,new_subject in [(False,True),(True,False)]:
  a,s=productive_fixture();a.variables.update(nesnd_small_governance_done=True,nesnd_small_order_active=True,nesnd_small_order_deadline=True,nesnd_small_order_months=9)
  if original_subject:a.variables.update(nesnd_small_order_subject=True,nesnd_small_regional=True)
  a.overlord=world['FRA'] if new_subject else None;a.subject_type='subject_type_protectorate' if new_subject else None
  eff('nesnd_small_monthly',a);assert 'nesnd_small_order_active' not in a.variables and 'nesnd_small_order_months' not in a.variables
  rows.append({'original_subject':original_subject,'new_subject':new_subject,'cancelled':True})
 a,s=productive_fixture();a.variables.update(nesnd_small_order_active=True,nesnd_small_order_months=23)
 eff('nesnd_small_monthly',a);assert 'nesnd_small_order_active' not in a.variables and 'nesnd_small_order_cooldown' in a.variables
 # Cleanup on losing all eligible territory, native market and building facts are preserved.
 a,s=productive_fixture();a.modifiers.update(['nesnd_small_specialised_market','nesnd_small_own_market','nesnd_small_public_investment','nesnd_small_public_services','nesnd_small_organise_representation']);a.variables.update(nesnd_small_market_verifying=True,nesnd_small_market_verification=True,nesnd_small_verification_partner=world['FRA']);s.region=region('region_western_europe');owner_before=a.market.owner;buildings_before=len(a.buildings)
 eff('nesnd_small_monthly',a)
 assert not a.modifiers and 'nesnd_small_market_verifying' not in a.variables and a.market.owner is owner_before and len(a.buildings)==buildings_before
 return {'switches':rows,'deadline_expired_before24':'closed +12m cooldown','ineligible_country_cleanup':'all four policy modifiers and active episode removed; native facts preserved'}

results=[]
for name,fn in [('cumulative_rewards_and_independent_terminal',cumulative_and_terminal),('terminal_subject_switch_deadline_cleanup',terminal_switch_and_cleanup)]:
 try:results.append({'name':name,'status':'PASS','detail':fn()})
 except Exception as e:results.append({'name':name,'status':'FAIL_OR_ADAPTER_UNRESOLVED','error':repr(e),'traceback':traceback.format_exc()});break
dump(run/'b2r1-monthly-source-matrix.json',{'checks':results,'boundary':'Actual frozen monthly/helper AST; native state/economy facts injected, calls represent callback ticks; no engine time or production simulation.'});print(json.dumps(results,ensure_ascii=False,indent=2))
