from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,r"C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts")
from pdx import parse
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104"
m=json.loads((R/"batch-b2-freeze.json").read_text(encoding="utf-8"))
F=Path(m["owned_freeze"]);B=W/"backups/b2-preimplementation-20261104";I=Path(m["dependency_base"])
def shape(n):return (n.key,n.op,n.value,tuple(shape(c) for c in n.children or []))
def nodes(p):return parse(p.read_text(encoding="utf-8-sig")).children
def bykey(ns,k):return next(n for n in ns if n.key==k)
out={"purpose":"Frozen interface/source diff only; no gameplay matrix or engine execution","files":{}}
for rel,base in [
("common/scripted_triggers/nesnd_canon_diplomacy.txt",B),
("common/scripted_effects/nesnd_canon_diplomacy.txt",B),
("common/scripted_triggers/nesnd_india_diplomacy.txt",I),
("common/scripted_buttons/nesnd_india_diplomacy.txt",B)]:
 old=nodes(base/rel);new=nodes(F/rel)
 unchanged=[];changed=[]
 for n in old:
  current=bykey(new,n.key)
  (unchanged if shape(n)==shape(current) else changed).append(n.key)
 out["files"][rel]={"baseline":str(base/rel),"unchanged_definitions":unchanged,"changed_definitions":changed}
 if rel.endswith("scripted_effects/nesnd_canon_diplomacy.txt"):
  for key in ("nesnd_canon_accept_request","nesnd_canon_refuse_request"):
   a=bykey(old,key);b=bykey(new,key)
   out[key+"_original_body_retained"]=tuple(shape(x) for x in a.children)==tuple(shape(x) for x in b.children[1:])
  a=bykey(old,"nesnd_canon_clear_request");b=bykey(new,"nesnd_canon_clear_request")
  out["clear_request_original_fields_retained"]=tuple(shape(x) for x in a.children)==tuple(shape(x) for x in b.children[:len(a.children)])
 if rel.endswith("scripted_triggers/nesnd_canon_diplomacy.txt"):
  a=bykey(old,"nesnd_canon_request_eligible").get("trigger_if")
  b=bykey(new,"nesnd_canon_request_eligible").get("trigger_if")
  oldbranches=[n for n in a.children if n.key in ("trigger_if","trigger_else_if")]
  newbranches=[n for n in b.children if n.key in ("trigger_if","trigger_else_if")][1:]
  out["shared_original_kind_branch_shapes"]=[]
  for index,(oa,nb) in enumerate(zip(oldbranches,newbranches)):
   out["shared_original_kind_branch_shapes"].append({"index":index,"same":shape(oa)==shape(nb)})
  out["kind2_subbranch_preserved"]=shape(oldbranches[1].get("trigger_if"))==shape(newbranches[1].get("trigger_if"))
  a=bykey(old,"nesnd_canon_treaty_result").get("trigger_if").get("scope:canon_sender")
  b=bykey(new,"nesnd_canon_treaty_result").get("trigger_if").get("scope:canon_sender")
  out["original_treaty_result_branches_retained"]=all(shape(x)==shape(y) for x,y in zip(a.children[:-1],b.children[:len(a.children)-1]))
 if rel.endswith("scripted_triggers/nesnd_india_diplomacy.txt"):
  a=bykey(old,"nesnd_india_can_send");b=bykey(new,"nesnd_india_can_send")
  out["india_can_send_original_fields_retained"]=tuple(shape(x) for x in a.children)==tuple(shape(x) for x in b.children if x.key!="trigger_if")
 if rel.endswith("scripted_buttons/nesnd_india_diplomacy.txt"):
  for key in ("nesnd_india_request_4","nesnd_india_request_7"):
   a=bykey(old,key);b=bykey(new,key)
   out[key]={"unchanged_metadata":all(shape(a.get(k))==shape(b.get(k)) for k in ("name","desc","visible","ai_chance")),"original_possible_in_else":tuple(shape(x) for x in a.get("possible").children)==tuple(shape(x) for x in b.get("possible").get("trigger_else").children),"original_effect_in_else":shape(a.get("effect").get("hidden_effect").get("if"))==shape(b.get("effect").get("hidden_effect").get("else").get("if"))}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out["shared_event_unchanged"]=sha(B/"events/nesnd_canon_diplomacy.txt")==sha(Path(m["test_snapshot"])/"events/nesnd_canon_diplomacy.txt")
out["protected_data_unchanged"]={}
for rel in ("common/history/states/00_states.txt","common/history/pops/10_india.txt","common/history/pops/11_east_asia.txt","common/history/pops/12_indonesia.txt","common/history/pops/13_australasia.txt"):
 out["protected_data_unchanged"][rel]=sha(I/rel)==sha(Path(m["candidate"])/rel)
(R/"batch-b2-interface-diff.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(out,indent=2,ensure_ascii=False))
