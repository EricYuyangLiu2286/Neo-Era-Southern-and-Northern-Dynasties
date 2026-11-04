from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_regional_terminal.py').read_text();exec(src[:src.index('rows=[]')],globals())
try:
 a,s,b=regional_fixture(False);eff('nesnd_small_economy_reward',a);eff('nesnd_small_governance_reward',a);a.variables.update(nesnd_small_regional_economy_done=True,nesnd_small_regional_governance_done=True,nesnd_small_regional_economy_months=12,nesnd_small_regional_governance_months=12,nesnd_small_order_months=17);epoch=a.variables['nesnd_small_epoch'];mods=copy.copy(a.modifier_adds)
 assert trig('nesnd_small_can_retarget',a);eff('nesnd_small_retarget',a)
 assert a.variables['nesnd_small_epoch']==epoch+1 and a.variables['nesnd_small_economy_rewarded'] and a.variables['nesnd_small_governance_rewarded'] and a.variables['nesnd_small_economy_done'] and a.variables['nesnd_small_governance_done']
 assert not any(k in a.variables for k in ['nesnd_small_regional_economy_done','nesnd_small_regional_governance_done','nesnd_small_regional_economy_months','nesnd_small_regional_governance_months','nesnd_small_order_months'])
 eff('nesnd_small_economy_reward',a);eff('nesnd_small_governance_reward',a);assert a.modifier_adds==mods
 report={'status':'PASS_RETARGET_REQUIRES_NEW_REGION_PROGRESS_WITH_PERMANENT_ONE_TIME_REWARDS','detail':{'new_epoch':epoch+1,'all3_observation_counters_and2_regional_done_cleared':True,'national_achievement_and_reward_receipts_kept':True,'no_second_modifier_add':True},'boundary':'Actual retarget and reward helper AST; the separate12+12 matrix covers monthly accumulation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-retarget-permanent-rewards.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
