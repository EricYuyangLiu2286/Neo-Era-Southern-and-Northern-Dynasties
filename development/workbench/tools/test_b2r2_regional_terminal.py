from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_extended_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
def regional_fixture(subject=True):
 a,s=country_fixture(pop=1200000);s.state_region=region('STATE_ACEH');b=state(a,'STATE_REGION_TWO');b.region=s.region;b.state_population=800000;b.market_access=1;b.state_unemployment_rate=0;b.pops=[];b.average_sol=12;b.turmoil=0
 for c in world.values():c.adjacent=set();c.market=getattr(c,'market',None)
 a.laws={'law_appointed_bureaucrats'};a.techs=set();a.army_size=4
 if subject:a.overlord=world['FRA'];a.subject_type='subject_type_protectorate';a.market=Entity('market','french-market',owner=world['FRA'])
 for land,prod in [(s,'building_rice_farm'),(b,'building_tooling_workshop')]:
  for typ,level in [(prod,2),('building_government_administration',1),('building_university',1),('building_barrack',1)]:
   z=building(a,typ,level);z.weekly_profit=10;z.is_subsidized=False;z.shortage=False;land.buildings.append(z)
 friend=world['BAV'];friend.market=a.market;friend.adjacent={a};a.adjacent={friend};friend.relations['ACE']=30
 eff('nesnd_small_initialize',a);assert a.variables.get('nesnd_small_regional') and trig('nesnd_small_targets_valid',a)
 return a,s,b
rows=[]
try:
 for subject in [True,False]:
  a,s,b=regional_fixture(subject)
  assert trig('nesnd_small_regional_economy',a)
  for _ in range(12):eff('nesnd_small_monthly',a)
  assert a.variables.get('nesnd_small_regional_economy_done') and a.modifier_adds['nesnd_small_livelihood']==1
  assert trig('nesnd_small_regional_governance',a)
  for _ in range(12):eff('nesnd_small_monthly',a)
  assert a.variables.get('nesnd_small_regional_governance_done') and a.modifier_adds['nesnd_small_learning']==1
  eff('nesnd_small_choose_order',a);assert a.variables.get('nesnd_small_order_active') and bool(a.variables.get('nesnd_small_order_subject'))==subject
  assert trig('nesnd_small_order_ready',a)
  for _ in range(24):eff('nesnd_small_monthly',a)
  assert a.variables.get('nesnd_small_order_rewarded') and a.modifier_adds['nesnd_small_order']==1
  eff('nesnd_small_choose_order',a);assert 'nesnd_small_order_active' not in a.variables
  rows.append({'subject':subject,'economy12':True,'governance12':True,'order24':True,'repeat_receipt':True,'native_barrack_alias_retained':True})
 report={'status':'PASS_REGIONAL_12_12_AND_HIGH_AUTONOMY_INDEPENDENT_TERMINALS','cases':rows,'boundary':'Actual frozen monthly AST; explicit existing state/building/market/adjacent partner facts. No economy or native market simulation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-regional-terminal-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
