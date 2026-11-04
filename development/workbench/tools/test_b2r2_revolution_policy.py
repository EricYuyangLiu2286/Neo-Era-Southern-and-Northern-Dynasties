from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
rows=[]
try:
 a,s,f,scopes=request_fixture(9);a.variables.update(nesnd_small_lineage=True,nesnd_small_southern_line=True,nesnd_small_economy_done=True,nesnd_small_economy_rewarded=True,nesnd_small_governance_done=True,nesnd_small_governance_rewarded=True,nesnd_small_order_done=True,nesnd_small_order_rewarded=True,nesnd_small_economy_months=8,nesnd_small_governance_months=5,nesnd_small_episode_active=True,nesnd_small_episode_clock=True,nesnd_small_episode_issue=3);a.modifiers.add('nesnd_small_organise_representation')
 rebel=new_country('REV');rebel.country_type='recognized';rebel.in_default=False;rebel.has_revolution=True;rebel.techs=set();rebel.igs={k:Entity('interest_group',k,owner=rebel,in_government=False) for k in a.igs};rebel.movements=[];rebel.pact_facts=[];rebel.gdp=100000;rebel.net_fixed_income=100;rebel.bureaucracy=0;rebel.government_legitimacy=50;rebel.literacy_rate=.3;rebel.market=Entity('market','rebel-market',owner=rebel);rebel.institutions={};rebel.pop_percent={};rebel.adjacent=set();rebel.catalysts=[]
 land=state(rebel,'STATE_REBEL');land.region=region('region_indonesia');land.state_population=700000;land.market_access=1;land.state_unemployment_rate=0;land.average_sol=12;land.turmoil=0;land.pops=[];saved['target']=rebel
 rel='common/on_actions/nesnd_small_states.txt';tree=parse(read(snap/rel));start=next(n for n in tree.children if n.key=='nesnd_small_revolution_start');assert x['triggers'](child(start,'trigger').children,[a]);x['effects'](child(start,'effect').children,[a],rel)
 assert 'nesnd_small_episode_active' not in a.variables and 'nesnd_canon_request_clock' not in a.variables and 'nesnd_small_organise_representation' not in a.modifiers
 assert rebel.variables['nesnd_small_economy_months']==8 and rebel.variables['nesnd_small_governance_months']==5 and rebel.variables.get('nesnd_small_provisional') and rebel.variables.get('nesnd_small_southern_line')
 for key in ['economy','governance','order']:assert rebel.variables['nesnd_small_'+key+'_rewarded']
 assert not trig('nesnd_small_safe',rebel)
 won=next(n for n in tree.children if n.key=='nesnd_small_civil_war_won');rebel.has_revolution=False;x['effects'](child(won,'effect').children,[rebel],rel);assert 'nesnd_small_provisional' not in rebel.variables and rebel.variables.get('nesnd_small_domestic_settlement')
 eff('nesnd_small_economy_reward',rebel);eff('nesnd_small_governance_reward',rebel);assert not rebel.modifiers
 rows.append({'actual_revolution_start':'closes source episode/request; copies permanent receipts and8/5 counters to real target object','provisional':'safe disabled until actual won callback','won':'clears provisional, refreshes targets; copied rewards suppress duplicate modifiers'})
 # Policy mismatch only withdraws the temporary specialization, leaving the actual new market unchanged.
 a,s=country_fixture();a.market=Entity('market','foreign-market',owner=world['FRA']);eff('nesnd_small_specialise',a);assert 'nesnd_small_specialised_market' in a.modifiers;a.market=Entity('market','own-market',owner=a);eff('nesnd_small_monthly',a);assert 'nesnd_small_specialised_market' not in a.modifiers and 'nesnd_small_policy_market' not in a.variables and a.market.owner is a
 rows.append({'specialisation_ended':'new market fact preserved, temporary bonus and snapshot cleaned'})
 report={'status':'PASS_ACTUAL_REVOLUTION_CALLBACK_AND_TEMP_POLICY_CLOSURE','cases':rows,'boundary':'Actual frozen on_action/helper AST with explicitly injected native original/revolutionary country and victory callback. No engine revolution inheritance/JE spawning behavior claim.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-revolution-policy-closure.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
