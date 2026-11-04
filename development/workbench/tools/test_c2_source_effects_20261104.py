"""Frozen source execution; native facts are explicit fixtures, never an engine pass."""
from c2_source_adapter_20261104 import *
class CP(Pred):
 def expr(self,n,o,root,prev):
  k,v=n.key,n.value
  if k=="any_country":return any([self.block(n,q,root,o) for q in self.w["countries"].values()])
  if k in ("nesnd_italy_country","nesnd_hus_civic_country","nesnd_usm_civic_country","nesnd_c2_project_theatre_peace","nesnd_c2_political_authority"):
   # External eligibility/theatre/government facts only. Project source is executed unchanged.
   return o.a.get(k,True)==(v!="no")
  if k in ("occupancy","weekly_profit","market_access","government_legitimacy","net_fixed_income","gdp"):
   return CMP[n.op](self.number(k,o,root,prev),self.number(v,o,root,prev))
  if k=="in_default":return o.a.get(k,False)==(v=="yes")
  if k=="is_ai":return o.a.get(k,False)==(v=="yes")
  if k=="institution_investment_level":return o.a.get("school_level",0)>=self.number(n.scalar("value"),o,root,prev)
  if k in VALUES:return CMP[n.op](self.calc(VALUES[k],o,root,prev),self.number(v,o,root,prev))
  return super().expr(n,o,root,prev)
class CR(Runner):
 def __init__(self,w,preview=False):super().__init__(w,preview=preview);self.pred=CP(w)
 def effect(self,n,o,root,prev):
  if n.key=="custom_description":
   target=self.pred.scope(n.scalar("subject"),o,root,prev);assert target is not None
   self.trace.append(("description",n.scalar("text"),target.name));return
  return super().effect(n,o,root,prev)
results=[]
def test(name,fn):
 try:results.append({"name":name,"status":"SOURCE_AST_PASS","detail":fn()})
 except Exception as e:results.append({"name":name,"status":"RED_OR_ADAPTER_UNSUPPORTED","error":str(e),"traceback":traceback.format_exc()})
def setup():
 w=world();c=country(w,"LOM");c.a.update(in_default=False,net_fixed_income=10000,gdp=1000000,school_level=1);s=state(w,c,"Milan");pop(s,"residents",100000,"han");s.a.update(market_access=0.8,state_region=Obj("state_region","lombardy",geographic={"geographic_region_italy_old"}));return w,c,s,CR(w)
def bld(s,key,level,occ=.75,profit=1):
 b=Obj("building",key,vars=set(),variable_values={},owner=s.a["owner"],state=s,level=level,occupancy=occ,weekly_profit=profit);s.a["buildings"].append(b);return b
def formula():
 w,c,s,r=setup();rows=[]
 for family in ["italy_foundations","italy_common_budget","hus_transport","hus_frontier","hus_citizenship","hus_oil","usm_constitution","usm_schools","usm_industry","usm_distribution"]:
  for e in range(101):
   bind(c,"nesnd_c2_"+family+"_baseline",e);a=r.pred.calc(VALUES["nesnd_c2_"+family+"_delta"],c,c);assert a==max(2,min(8,math.ceil(.2*e)));rows.append([family,e,a])
 quotes=[]
 for gdp in [0,1,249999,250000,1000000,24999999,25000000,999999999]:
  c.a["gdp"]=gdp;v=r.pred.calc(VALUES["nesnd_c2_weekly_quote"],c,c);assert v==min(2500,max(25,round(gdp*.0001)));quotes.append([gdp,v])
 return {"delta_combinations":len(rows),"quotes":quotes}
def project():
 w,c,s,r=setup();key="nesnd_c2_italy_foundations";bind(c,key+"_public_works_target",s)
 r.call(key+"_public_works_start",c)
 assert c.a["variable_values"][key+"_baseline"]==0
 assert c.a["variable_values"][key+"_quote"]==100
 assert c.a["variable_values"][key+"_target"] is s
 assert key+"_active" in c.a["vars"]
 b=bld(s,"building_tooling_workshop",2)
 months=[]
 for i in range(3):
  r.call(key+"_monthly",c);months.append(c.a["variable_values"][key+"_months"])
 assert months==[1,2,3] and key+"_done" in c.a["vars"]
 before=len(w["events"]);r.call(key+"_monthly",c);r.call(key+"_settle",c);assert len(w["events"])==before==1
 return {"months":months,"reward_events":before,"E0":c.a["variable_values"][key+"_baseline"],"quote":100}
def resets():
 rows=[]
 for change in ["employment","profit","access","owner"]:
  w,c,s,r=setup();key="nesnd_c2_italy_foundations";bind(c,key+"_public_works_target",s);r.call(key+"_public_works_start",c);b=bld(s,"building_tooling_workshop",2);r.call(key+"_monthly",c);r.call(key+"_monthly",c)
  if change=="employment":b.a["occupancy"]=.74
  if change=="profit":b.a["weekly_profit"]=0
  if change=="access":s.a["market_access"]=.79
  if change=="owner":s.a["owner"]=country(w,"SAR")
  r.call(key+"_monthly",c);assert c.a["variable_values"][key+"_months"]==0;assert key+"_done" not in c.a["vars"];rows.append({"changed":change,"counter":0})
 return rows
def aggregation_counterexample():
 w,c,s,r=setup();key="nesnd_c2_italy_foundations";bind(c,key+"_public_works_target",s);r.call(key+"_public_works_start",c)
 bld(s,"building_tooling_workshop",1,.75,1);bld(s,"building_arms_industry",8,0,-100)
 accepted=r.pred.block(A.TR[key+"_operating"],c,c)
 assert accepted
 return {"observed_operating":accepted,"productive_levels":1,"empty_unprofitable_levels":8,"required_delta":2,"status":"SOURCE_CONTRACT_COUNTEREXAMPLE_REQUIRES_ROOT_NUMERIC_JUDGMENT"}
def preview():
 w,c,s,r=setup();buttons=A.parse(A.read(S/"common/scripted_buttons/nesnd_civic_routes.txt"));r=CR(w,preview=True);before=(set(c.a["vars"]),dict(c.a["variable_values"]))
 r.block(buttons.get("nesnd_c2_italy_foundations_public_works").get("effect"),c,c)
 assert (set(c.a["vars"]),dict(c.a["variable_values"]))==before
 return {"no_target_no_prior_writes":True,"trace":r.trace}
def hus_boundary():
 rows=[]
 for tag,flag,expected in [("HUS",None,True),("HUS","nesnd_hus_native_successor",False),("HUS","nesnd_hus_hierarchy_retired",False),("HUS","nesnd_hus_revolution_provisional",False),("NKH",None,False)]:
  w=world();c=country(w,tag)
  if flag:bind(c,flag)
  actual=Pred(w).block(A.TR["nesnd_hus_civic_country"],c,c);assert actual==expected;rows.append([tag,flag,actual])
 return rows
def western():
 rows=[]
 for kind,flags in [(0,[]),(1,["nesnd_usm_western_opened"]),(2,["nesnd_usm_western_succeeded"]),(3,["nesnd_usm_western_failed"])]:
  w,c,s,r=setup();w["countries"].pop("LOM");c.name="USM";w["countries"]["USM"]=c;bind(c,"tag_WUU_var")
  for flag in flags:bind(c,flag)
  laws=set(c.a["laws"]);popsize=s.a["pops"][0].a["total_size"]
  r.call("nesnd_c2_refresh_usm_outcome",c);r.call("nesnd_c2_refresh_usm_outcome",c)
  assert c.a["variable_values"]["nesnd_c2_western_outcome"]==kind
  assert c.a["laws"]==laws and s.a["pops"][0].a["total_size"]==popsize and not w["native_trace"]
  rows.append([kind,c.a["variable_values"]["nesnd_c2_usm_outcome"]])
 return rows
def budget():
 rows=[]
 for ai,income,slots,expected in [(False,99,0,False),(False,100,0,True),(True,199,0,False),(True,200,0,True),(False,10000,2,False)]:
  w,c,s,r=setup();c.a.update(is_ai=ai,net_fixed_income=income)
  for key in ["nesnd_c2_italy_foundations_active","nesnd_c2_hus_transport_active"][:slots]:bind(c,key)
  actual=r.pred.block(A.TR["nesnd_c2_can_budget"],c,c);assert actual==expected;rows.append([ai,income,slots,actual])
 return rows
test("all_project_delta_formulas_and_bounded_quote",formula)
test("actual_start_source_E0_same_target_three_months_once",project)
test("source_operating_employment_profit_access_owner_reset",resets)
test("manufacturing_mixed_productive_and_empty_buildings_counterexample",aggregation_counterexample)
test("actual_button_preview_without_prior_writes",preview)
test("actual_HUS_original_native_successor_retired_provisional_gates",hus_boundary)
test("USM_four_western_outcomes_read_only_repeat",western)
test("source_budget_player_AI_two_slot_thresholds",budget)
(RUN/"source-effects-c2.json").write_text(json.dumps({"boundary":"Actual unchanged frozen source AST executed with explicit native facts; no engine semantics certified. Affected character/Italian cancellation matrices stopped on top-level structural red examples.","checks":results},indent=2,ensure_ascii=False))
print(json.dumps(results,indent=2,ensure_ascii=False))

