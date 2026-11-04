from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_regional_terminal.py').read_text();exec(src[:src.index('rows=[]')],globals())
rows=[]
try:
 for tag,reg,one,two in [('YN1','region_oceania','STATE_NEW_SOUTH_WALES','STATE_NORTH_ISLAND'),('BUR','region_indochina','STATE_MANDALAY','STATE_PEGU'),('SIA','region_indochina','STATE_BANGKOK','STATE_NAKHON_RATCHASIMA')]:
  a,s=country_fixture(tag,reg,1200000);s.state_region=region(one);b=state(a,two);b.region=s.region;b.state_population=800000;b.market_access=1;b.state_unemployment_rate=0;b.pops=[]
  overseas=state(a,'STATE_OVERSEAS');overseas.region=region('region_western_europe');overseas.state_population=10000000;overseas.market_access=1;overseas.state_unemployment_rate=0;overseas.pops=[]
  eff('nesnd_small_initialize',a);assert val('nesnd_small_candidate_denominator',a)==2000000 and val('nesnd_small_target_denominator',a)==2000000 and val('nesnd_small_group_one_share',a)==.6 and val('nesnd_small_group_two_share',a)==.4
  rows.append({'tag':tag,'own_overseas10m':'not in homeland denominator; actual groups .6/.4 remain','scale_including_all_owned_population':val('nesnd_small_scale',a)})
 a,s,b=regional_fixture(False)
 # Replace actual production facts with two single agro types; no rewritten class/specialization helper.
 a.buildings=[];s.buildings=[];b.buildings=[]
 for land in [s,b]:
  z=building(a,'building_rice_farm',2);z.weekly_profit=10;z.is_subsidized=False;z.shortage=False;land.buildings=[z]
 assert val('nesnd_small_industry_classes',a)==1 and not trig('nesnd_small_specialisation',a) and not trig('nesnd_small_regional_industry',a)
 b.buildings[0].building_type='building_wheat_farm';assert trig('nesnd_small_specialisation',a) and trig('nesnd_small_regional_industry',a)
 b.buildings[0].occupancy=.7499;assert not trig('nesnd_small_regional_industry',a);b.buildings[0].occupancy=.75;b.buildings[0].weekly_profit=0;assert not trig('nesnd_small_regional_industry',a);b.buildings[0].weekly_profit=.001;assert trig('nesnd_small_regional_industry',a)
 rows.append({'specialisation':'same rice2/rice2 fails; rice2/wheat2 succeeds; occupancy .7499 and profit0 reject; exact .75+positive accepts'})
 report={'status':'PASS_HOMELAND_DENOMINATORS_AND_REAL_SPECIALISATION','cases':rows,'boundary':'Actual frozen population/group/industry AST using explicit existing owned states/building facts.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-homeland-specialisation-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
