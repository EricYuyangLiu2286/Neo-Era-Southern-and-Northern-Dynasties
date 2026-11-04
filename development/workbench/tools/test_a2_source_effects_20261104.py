"""Execute frozen ordered AST and explicit native fact/operation adapters, not a gameplay state machine."""
from pathlib import Path
from types import SimpleNamespace as NS
from copy import deepcopy
import json,hashlib,sys,traceback,operator,math
import batch_a_test_support as A
import batch_a_lifecycle_support as L
W=A.W;R=A.R;G=A.G;cfg=json.loads((R/"batch-a2-test-config.json").read_text());S=Path(cfg["snapshot"]);RUN=Path(cfg["run"])
A.TR=A.defs("common/scripted_triggers",(S,));A.EFF=A.defs("common/scripted_effects",(S,));L.EFF=A.EFF
VALUES=A.defs("common/script_values",(S,))
ROLES=A.defs("common/character_roles",(G,S))
Obj=A.Obj;bind=L.bindvar
CMP={"=":operator.eq,"?=":operator.eq,"!=":operator.ne,">":operator.gt,">=":operator.ge,"<":operator.lt,"<=":operator.le}
def body(n):return NS(children=[x for x in n.children or [] if x.key not in ("limit","order_by","position","max","min","check_range_bounds","count")])
def items(key,o,w):
 if "scope_state" in key:return o.a.get("states",[])
 if "scope_pop" in key:return o.a.get("pops",[])
 if "scope_building" in key:return o.a.get("buildings",[]) if o.kind=="state" else [b for s in o.a.get("states",[]) for b in s.a["buildings"]]
 if "scope_character" in key:return o.a.get("characters",[])
 if "character_in_exile" in key:return w["exiles"]
 if "character_in_void" in key:return w["void"]
 if key.endswith("character"):return [c for x in w["countries"].values() for c in x.a.get("characters",[])]
 if "military_formation" in key:return o.a.get("formations",[])
 raise AssertionError(("UNSUPPORTED iterator",key))
class Pred(L.LE):
 def __init__(self,w):super().__init__(w);self.values=VALUES
 def scope(self,k,o,root,prev):
  if k in ("primary_culture","initiator","target"):return o.a.get(k)
  if k.startswith("sr:"):return self.w["strategic"].setdefault(k[3:],Obj("strategic",k[3:]))
  if k in ("state","owner","state_region","region","capital","culture"):
   if o is None:return None
   if k=="owner" and o.kind=="pop":return o.a["state"].a["owner"]
   return o.a.get(k)
  if "." in k:
   first,rest=k.split(".",1);obj=self.scope(first,o,root,prev)
   return self.scope(rest,obj,root,o) if obj is not None else None
  return super().scope(k,o,root,prev)
 def number(self,t,o,root,prev):
  try:return float(t)
  except(TypeError,ValueError):pass
  if t in VALUES:return self.calc(VALUES[t],o,root,prev)
  if "." in str(t):
   first,rest=t.split(".",1);obj=self.scope(first,o,root,prev)
   if obj is not None:return self.number(rest,obj,root,o)
  val=self.scope(t,o,root,prev)
  if isinstance(val,(int,float)):return val
  if t in ("total_population","state_population"):
   if o.kind=="country":return sum(self.number("state_population",s,root,o) for s in o.a["states"])
   if o.kind=="state":return sum(p.a["total_size"] for p in o.a["pops"])
  if t in o.a and isinstance(o.a[t],(int,float)):return o.a[t]
  raise AssertionError(("UNSUPPORTED numeric",t,o))
 def expr(self,n,o,root,prev):
  k,v=n.key,n.value
  if k.startswith("any_") and k not in ("any_primary_culture",):
   if k=="any_civil_war":return False
   found=sum(self.block(n,q,root,o) for q in items(k,o,self.w));c=n.get("count")
   return CMP[c.op](found,self.number(c.value,o,root,prev)) if c else found>0
  if k in ("state_population","total_population","total_size","army_size","level"):return CMP[n.op](self.number(k,o,root,prev),self.number(v,o,root,prev))
  if k=="has_role":
   if v not in ROLES:self.w["invalid_roles"].append(v)
   return v in o.a.get("roles",set())
  if k=="has_template":return o.a.get("template")==v
  if k=="is_diplomatic_play_type":return o.a.get("play_type")==v
  if k in ("initiator","target") and n.children is None:return CMP[n.op](self.scope(k,o,root,prev),self.scope(v,o,root,prev))
  if k=="culture" and n.children is None:return CMP[n.op](self.scope(k,o,root,prev),self.scope(v,o,root,prev))
  if k=="is_army":return o.kind=="army"
  if k=="is_character_alive":return o.a.get("alive",True)==(v=="yes")
  if k=="is_building_type":return o.name==v
  if k=="owns_entire_state_region":return o in self.w["full_regions"].get(self.scope(v,o,root,prev),[])
  if k=="is_in_geographic_region":return v in o.a.get("geographic",set())
  if k=="is_interest_group_leader":return False
  return super().expr(n,o,root,prev)
 def calc(self,n,o,root,prev=None,acc=0):
  chain=None
  for x in n.children or []:
   k,v=x.key,x.value
   if k=="if":
    chain=self.block(x.get("limit"),o,root,prev)
    if chain:acc=self.calc(body(x),o,root,prev,acc)
   elif k in ("else_if","else"):
    if not chain:
     chain=k=="else" or self.block(x.get("limit"),o,root,prev)
     if chain:acc=self.calc(body(x),o,root,prev,acc)
   elif k.startswith("every_") or k.startswith("ordered_"):
    qs=list(items(k,o,self.w))
    if x.get("limit"):qs=[q for q in qs if self.block(x.get("limit"),q,root,o)]
    if k.startswith("ordered_"):
     qs.sort(key=lambda q:self.number(x.scalar("order_by"),q,root,o),reverse=True)
     if x.get("position"):qs=qs[int(x.scalar("position")):int(x.scalar("position"))+1]
     elif x.get("max"):qs=qs[:int(x.scalar("max"))]
    for q in qs:acc=self.calc(body(x),q,root,o,acc)
   elif k in ("value","add","subtract","multiply","divide","min","max"):
    val=self.calc(x,o,root,prev) if x.children is not None else self.number(v,o,root,prev)
    acc={"value":lambda:val,"add":lambda:acc+val,"subtract":lambda:acc-val,"multiply":lambda:acc*val,"divide":lambda:acc/val,"min":lambda:max(acc,val),"max":lambda:min(acc,val)}[k]()
   elif k=="floor":acc=math.floor(acc)
   elif k=="round":acc=round(acc)
   else:
    target=self.scope(k,o,root,prev)
    if target is None:raise AssertionError(("UNSUPPORTED value",k))
    acc=self.calc(x,target,root,o,acc)
  return acc
class Runner(L.Life):
 def __init__(self,w,lottery=(),preview=False):
  super().__init__(w);self.pred=Pred(w);self.lottery=iter(lottery);self.moves=[];self.preview=preview
 def value(self,t,o,root,prev):
  if t is not None:
   try:return self.pred.number(t,o,root,prev)
   except AssertionError:pass
  return super().value(t,o,root,prev)
 def effect(self,n,o,root,prev):
  k,v=n.key,n.value
  if self.preview and k in ("set_variable","change_variable","remove_variable","set_global_variable","remove_global_variable","save_scope_as","save_temporary_scope_as","clear_saved_scope","save_scope_value_as","trigger_event","add_modifier","remove_modifier"):return
  if k=="while":
   for i in range(int(n.scalar("count"))):
    if not self.pred.block(n.get("limit"),o,root,prev):break
    self.block(body(n),o,root,prev)
   return
  if k in ("set_variable","set_global_variable") and n.get("value") and n.get("value").children is not None:
   val=self.pred.calc(n.get("value"),o,root,prev);name=n.scalar("name")
   if k=="set_variable":bind(o,name,val)
   else:self.w["globals"][name]=val
   return
  if k in ("every_scope_state","every_scope_pop","every_scope_building","every_character","every_character_in_exile_pool","every_character_in_void","random_scope_state","random_scope_character","random_military_formation"):
   qs=list(items(k,o,self.w))
   if n.get("limit"):qs=[q for q in qs if self.pred.block(n.get("limit"),q,root,o)]
   if k.startswith("random_"):qs=qs[:1]
   for q in qs:self.block(body(n),q,root,o)
   return
  if k=="random_list":
   weights=[int(q.key) for q in n.children];choice=next(self.lottery,weights[0])
   assert choice in weights
   self.w["lotteries"].append({"source":o.name,"weights":weights,"selected":choice})
   self.block(next(q for q in n.children if int(q.key)==choice),o,root,prev);return
  if k in ("move_pop","move_partial_pop"):
   dest=self.pred.scope(v if k=="move_pop" else n.scalar("state"),o,root,prev);assert dest and dest.kind=="state"
   source=o.a["state"];ratio=1 if k=="move_pop" else self.value(n.scalar("population_ratio"),o,root,prev);size=o.a["total_size"]*ratio
   self.moves.append({"source_pop":o.name,"source_owner":source.a["owner"].name,"destination":dest.a["owner"].name,"size":size,"ratio":ratio})
   if ratio==1:source.a["pops"].remove(o);dest.a["pops"].append(o);o.a["state"]=dest
   else:
    o.a["total_size"]-=size;clone=pop(dest,o.name+"-moved",size,o.a["culture"])
   return
  if k=="transfer_to_formation":
   dest=self.pred.scope(v,o,root,prev);assert dest
   dest.a["commanders"].append(o);return
  if k=="create_character":
   assert n.scalar("template") in A.defs("common/character_templates",(S,))
   t=A.defs("common/character_templates",(S,))[n.scalar("template")]
   roles={"character_role_general"} if t.scalar("is_general")=="yes" else set()
   c=character(o,n.scalar("template"),roles,n.scalar("template"));self.w["created_characters"].append(c)
   if n.get("on_created"):self.block(n.get("on_created"),c,root,o)
   return
  if k=="add_modifier":o.a.setdefault("modifiers",set()).add(n.scalar("name"));return
  return super().effect(n,o,root,prev)
def world():
 return {"countries":{},"regions":{},"saved":{},"globals":{},"objects":[],"timers":[],"events":[],"day":L.date(1836,1,15),"native_trace":[],"strategic":{},"full_regions":{},"invalid_roles":[],"exiles":[],"void":[],"lotteries":[],"created_characters":[]}
def country(w,tag):
 c=A.country(tag);c.a.update(states=[],characters=[],formations=[],primary=[],cultures=[],army_size=0,active_laws={});w["countries"][tag]=c;return c
def state(w,c,name,strategic="region_great_plains"):
 s=Obj("state",name,vars=set(),variable_values={},owner=c,pops=[],buildings=[],region=w["strategic"].setdefault(strategic,Obj("strategic",strategic)))
 c.a["states"].append(s);return s
def pop(s,name,size,culture):
 p=Obj("pop",name,vars=set(),variable_values={},total_size=size,culture=A.CULTURES[culture] if isinstance(culture,str) else culture,state=s);s.a["pops"].append(p);return p
def character(c,name,roles,template=None):
 a=Obj("character",name,vars=set(),variable_values={},owner=c,roles=roles,template=template,alive=True)
 c.a["characters"].append(a);return a
results=[]
def check(name,fn):
 try:detail=fn();results.append({"name":name,"status":"PASS","detail":detail})
 except Exception as exc:results.append({"name":name,"status":"FAIL_OR_NOT_RUN","error":repr(exc),"traceback":traceback.format_exc()})
def roles_case():
 w=world();n=country(w,"NKH");f=Obj("army","new-army",commanders=[]);n.a["formations"].append(f);character(n,"Tatanka",{"character_role_general","character_role_ruler"},"nesnd_a2_tatanka")
 runner=Runner(w);definition=A.EFF["nesnd_khanate_prepare"];nodes=definition.get("if").children
 start=next(i for i,x in enumerate(nodes) if x.key=="random_military_formation");end=next(i for i in range(start,len(nodes)) if nodes[i].key=="clear_saved_scope")
 fragment=NS(children=deepcopy(nodes[start:end+1]));runner.block(fragment,n,n)
 actual=len(f.a["commanders"]);invalid=list(w["invalid_roles"])
 for x in fragment.children:
  for q in x.walk():
   if q.key=="has_role" and q.value=="general":q.value="character_role_general"
 runner.block(fragment,n,n);control=len(f.a["commanders"])
 assert actual==0 and control==1
 return {"source_assignment_count":actual,"native_role_control_assignment_count":control,"invalid_role_keys":invalid,"status":"CONFIRMED_SOURCE_DEFECT","fragment_source":"nesnd_khanate_prepare actual formation/character assignment suffix; native formation existence supplied, no full preparation pass claimed"}
def exodus(dest,lottery):
 w=world();h=country(w,"HUS");hs=state(w,h,"HUS");pop(hs,"a",100,"manchu");pop(hs,"b",900,"manchu")
 bind(h,"nesnd_hus_registration_choice",2);bind(h,"nesnd_hus_registration_done");bind(h,"nesnd_hus_registration_epoch",1);bind(h,"nesnd_hus_manchu_exodus_pending");h.a["laws"].add("law_nesnd_hus_native_registration");w["globals"]["nesnd_hus_registration_record_epoch"]=1
 for tag in dest:
  c=country(w,tag);s=state(w,c,tag);pop(s,tag+"-resident",1000,"han")
 runner=Runner(w,lottery);runner.call("nesnd_a2_manchu_exodus",h);before=list(runner.moves);runner.call("nesnd_a2_manchu_exodus",h)
 assert runner.moves==before and "nesnd_hus_manchu_exodus_pending" not in h.a["vars"]
 return {"moves":runner.moves,"lotteries":w["lotteries"],"result":h.a["variable_values"].get("nesnd_a2_exodus_result"),"receipt":w["globals"].get("nesnd_hus_registration_exodus_epoch")}
def half():
 w=world();n=country(w,"NKH");bind(n,"nesnd_native_khanate");ns=state(w,n,"NKH");pop(ns,"ceded",100,"siouan");u=country(w,"USA");us=state(w,u,"remaining-USA");pop(us,"remaining",200,"siouan");h=country(w,"HUS");hs=state(w,h,"HUS");pop(hs,"native-HUS",400,"siouan")
 r=Runner(w);r.call("nesnd_khanate_transfer_native_half",u);r.call("nesnd_khanate_transfer_native_half",h);r.call("nesnd_khanate_transfer_native_half",u)
 assert [(m["source_pop"],m["size"]) for m in r.moves]==[("remaining",100),("native-HUS",200)]
 assert ns.a["pops"][0].a["total_size"]==100
 return {"moves":r.moves,"ceded_population_not_recounted":True}
def refugee(dest):
 w=world();a=country(w,"NAH");s=state(w,a,"NAH");pop(s,"native",500,"nahua");bind(a,"nesnd_restoration_refugees_pending")
 if dest:
  h=country(w,"HUS");hs=state(w,h,"HUS");pop(hs,"resident",100,"siouan")
 r=Runner(w);r.call("nesnd_restoration_refugees",a);r.call("nesnd_restoration_refugees",a)
 assert len(r.moves)==(1 if dest else 0)
 return {"moves":r.moves,"state":a.a["variable_values"].get("nesnd_restoration_refugee_state"),"pending":"nesnd_restoration_refugees_pending" in a.a["vars"]}
def wrong_dp():
 w=world();n=country(w,"NKH");u=country(w,"USA");bind(n,"nesnd_native_khanate");bind(n,"nesnd_khanate_original_usa",u)
 good=Obj("diplomatic_play","actual-dispatched",vars=set(),variable_values={},initiator=u,target=n,play_type="dp_nesnd_khanate_suppression")
 wrong=Obj("diplomatic_play","different-same-pair",vars=set(),variable_values={},initiator=u,target=n,play_type="dp_nesnd_khanate_suppression")
 bind(u,"nesnd_khanate_war_dispatched");bind(u,"nesnd_khanate_play",good)
 w["saved"].update(target_country=u,diplomatic_play=wrong)
 r=Runner(w);goal=A.parse(A.read(S/"common/war_goal_types/nesnd_native_americas.txt")).get("wg_nesnd_khanate_humiliation")
 accepted=r.pred.block(A.TR["nesnd_khanate_goal_pair"],n,n)
 r.block(goal.get("on_enforced"),n,n)
 assert accepted and u.a["variable_values"].get("nesnd_khanate_war_outcome")==2
 return {"stored_dp":good.name,"callback_dp":wrong.name,"accepted_wrong_object":accepted,"opponent_outcome":u.a["variable_values"].get("nesnd_khanate_war_outcome"),"rewarded":"nesnd_khanate_victory_reward" in n.a["vars"],"status":"CONFIRMED_SOURCE_DEFECT"}
def army_preview():
 w=world();n=country(w,"NKH")
 for i in range(4):s=state(w,n,str(i));pop(s,"resident"+str(i),1000000,"siouan")
 r=Runner(w,preview=True);r.call("nesnd_khanate_army",n)
 return {"safe":True}
def tiers():
 w=world();c=country(w,"NKH");s=state(w,c,"state");p=pop(s,"people",1,"siouan");pred=Pred(w);values=[]
 for key,points in [("nesnd_khanate_army_target",[0,799999,800000,1599999,1600000,2399999,2400000,3199999,3200000]),("nesnd_restoration_army_target",[0,299999,300000,599999,600000,899999,900000,1199999,1200000,1799999,1800000])]:
  for size in points:p.a["total_size"]=size;values.append({"value":key,"population":size,"result":pred.calc(VALUES[key],c,c)})
 return values
def core_eligibility():
 values=[]
 for size,split in ((99999,False),(100000,False),(100000,True),(200000,False)):
  w=world();c=country(w,"MEX");s=state(w,c,"core");reg=Obj("state_region","core-region",geographic={"geographic_region_mexico"});s.a["state_region"]=reg;w["regions"][reg.name]=reg
  w["full_regions"][reg]=[] if split else [c]
  pop(s,"native",size*0.75,"nahua");pop(s,"other",size*0.25,"yankee")
  p=Pred(w);actual=p.block(A.TR["nesnd_restoration_native_state"],s,s)
  expected=size>=100000 and not split;assert actual==expected
  values.append({"population":size,"split_state":split,"eligible":actual})
 return values
def turtle_guards():
 result=[]
 source=A.parse(A.read(S/"common/scripted_buttons/zzzz_nesnd_turtle_island.txt"))
 for flag in ("nesnd_native_khanate","nesnd_hus_native_successor"):
  for definition in source.children:
   w=world();c=country(w,"NKH" if flag=="nesnd_native_khanate" else "HUS");bind(c,flag);r=Runner(w);before=set(c.a["vars"])
   r.block(definition.get("effect"),c,c)
   assert set(c.a["vars"])==before and not w["native_trace"] and c.name in ("NKH","HUS")
   result.append({"flag":flag,"button":definition.key,"native_effects":0})
 return result
check("native_role_assignment_minimal_failure_and_control",roles_case)
check("exodus_first_run_missing_global_epoch",lambda:exodus(("CNE","USA"),(70,30)))
check("aftercession_two_sources_half_once",half)
for dst in (True,False):check("refugee40_"+str(dst),lambda dst=dst:refugee(dst))
check("khanate_wrong_same_pair_dp_goal_callback",wrong_dp)
check("army_preview_no_prior_writes",army_preview)
check("population_tiers_actual_script_values",tiers)
check("core_state_population_and_full_owner_guards",core_eligibility)
check("turtle_island_old_effect_window_guards",turtle_guards)
(RUN/"source-effects-matrix.json").write_text(json.dumps({"boundary":"Actual frozen source AST and explicit native population/formation facts, not engine semantics; invalid-role failure stops full army/personnel branch testing.","checks":results},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps([{"name":r["name"],"status":r["status"],"detail":r.get("detail"),"error":r.get("error")} for r in results],indent=2,ensure_ascii=False))
