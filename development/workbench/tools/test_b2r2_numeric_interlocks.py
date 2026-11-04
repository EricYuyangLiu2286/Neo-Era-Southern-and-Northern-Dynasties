from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
rows=[]
try:
 a,s=country_fixture();a.catalysts=[]
 for pop,tier in [(0,1),(999999,1),(1000000,2),(4999999,2),(5000000,4),(9999999,4),(10000000,8)]:s.state_population=pop;assert val('nesnd_small_scale',a)==tier
 s.state_population=100000;a.gdp=100000;a.net_fixed_income=100;eff('nesnd_small_start_public',a);assert a.variables['nesnd_small_frozen_quote']==20 and a.modifier_adds['nesnd_small_public_investment']==1
 a.gdp=100000000;eff('nesnd_small_start_public',a);assert a.variables['nesnd_small_frozen_quote']==20 and a.modifier_adds['nesnd_small_public_investment']==1
 a.modifiers.remove('nesnd_small_public_investment');a.modifiers.remove('nesnd_small_public_services');a.net_fixed_income=3000;eff('nesnd_small_start_public',a);assert a.variables['nesnd_small_frozen_quote']==2000
 rows.append({'scale':'all7 thresholds','public_quote':'20 frozen despite GDP growth; next actual period2000 clamp; no duplicate same-period charge'})
 # Population-weighted access/occupation, not unweighted mean of states.
 a,s=country_fixture(pop=600000);b=state(a,'STATE_SECOND');b.region=s.region;b.state_population=400000;b.market_access=.79;b.state_unemployment_rate=.2;s.market_access=.8;s.state_unemployment_rate=.1
 assert val('nesnd_small_transport',a)==.6 and val('nesnd_small_job_coverage',a)==.6;b.market_access=.8;b.state_unemployment_rate=.1;assert val('nesnd_small_transport',a)==1 and val('nesnd_small_job_coverage',a)==1
 rows.append({'population_weight':'600k valid +400k invalid =>.6; exact access .8 and unemployed .1 included'})
 # Old India pending/cooldowns gate B2; B2 pending/verification gates only real B2 India, not empire route.
 for flag in ['nesnd_canon_request_clock','nesnd_canon_request_cooldown','nesnd_small_market_verification','nesnd_small_market_verifying']:
  a,s=country_fixture('HYD','region_south_india');assert trig('nesnd_india_can_send',a);a.variables[flag]=True;assert not trig('nesnd_india_can_send',a)
 for flag in ['nesnd_india_request_clock','nesnd_india_request_cooldown','nesnd_external_pending','nesnd_external_cooldown']:
  a,s=country_fixture('HYD','region_south_india');a.variables['nesnd_small_governance_done']=True;assert trig('nesnd_small_diplomacy_ready',a);a.variables[flag]=True;assert not trig('nesnd_small_diplomacy_ready',a)
 a,s=country_fixture('MUG','region_north_india');a.variables['nesnd_canon_request_clock']=True;assert not trig('nesnd_small_state_country',a) and trig('nesnd_india_can_send',a)
 rows.append({'mutual_India_interlock':'8 lock facts gate both sides; MUG original empire branch not gated by B2 canon lock'})
 # Investment permit and bonus do not manufacture productive industries or alter real market ownership.
 a,s=country_fixture();a.relations['FRA']=30;f=world['FRA'];f.relations['ACE']=30;before=len(a.buildings);owner=a.market.owner;eff('nesnd_canon_send_request',a,'TAG = FRA KIND = 5');e=next(e for e in captured_events if e['event']=='nesnd_canon_diplomacy.1');saved.clear();saved.update(e['scopes']);eff('nesnd_canon_accept_request',f)
 assert a.variables['nesnd_canon_investor'] is f and 'nesnd_small_state_capital' in a.modifiers and len(a.buildings)==before and a.market.owner is owner and val('nesnd_small_production',a)==0
 rows.append({'kind5':'actual permit+investor+capital bonus; no industry or market facts created'})
 report={'status':'PASS_SCALE_BUDGET_WEIGHTS_INDIA_AND_INVESTMENT_CONTRACTS','cases':rows,'boundary':'Actual fixed source AST and explicit state/building/market/law facts; no economy/AI simulation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-numeric-interlock-contracts.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
