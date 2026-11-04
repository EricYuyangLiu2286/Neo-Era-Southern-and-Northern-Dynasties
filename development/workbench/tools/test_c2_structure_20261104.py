from pathlib import Path
import sys,json,re,hashlib,collections
sys.path.insert(0,r"C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts")
from pdx import parse,basekey
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104";cfg=json.loads((R/"batch-c2-test-config.json").read_text());S=Path(cfg["snapshot"]);P=Path(cfg["baseline_snapshot"]);RUN=Path(cfg["run"]);G=Path(r"D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game")
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:p.read_text(encoding="utf-8-sig")
def shape(n):return (n.key,n.op,n.value,tuple(shape(x) for x in n.children or []))
def defs(p):return {basekey(n.key):n for n in parse(read(p)).children}
freeze=json.loads((R/"batch-c2-freeze.json").read_text());out={"owned":[],"top_level_builtin_errors":[],"native_diff":{}}
for rel,h in freeze["owned_files"].items():
 q=S/rel;data=q.read_bytes();row={"path":rel,"sha256":sha(q),"match":sha(q)==h,"BOM":data.startswith(b"\xef\xbb\xbf")}
 if rel.endswith(".txt"):
  ast=parse(read(q));row["definitions"]=len(ast.children)
  if rel.startswith("common/scripted_effects/"):
   for n in ast.children:
    if n.key in ("if","else_if","else","set_variable","remove_variable"):out["top_level_builtin_errors"].append({"file":rel,"key":n.key,"position":n.start,"line":read(q).count("\n",0,n.start)+1,"shape":shape(n)})
 out["owned"].append(row)
for rel,allow in [("events/agitators_events/garibaldi_events.txt",["garibaldi_events.1","garibaldi_events.2","garibaldi_events.3"]),("events/italian_unification.txt",["italian_unification.4","italian_unification.7","italian_unification.8","italian_unification.10"])]:
 a=defs(G/rel);b=defs(S/rel);changed=[k for k in a if shape(a[k])!=shape(b.get(k))] if all(k in b for k in a) else ["MISSING"]
 out["native_diff"][rel]={"changed":changed,"allowed":allow,"extra_changed":[k for k in changed if k not in allow],"keys_identical":a.keys()==b.keys()}
# originalce_global preservation (product baseline before C2)
a=parse(read(P/"common/history/global/ce_global.txt"));b=parse(read(S/"common/history/global/ce_global.txt"))
out["ce_global_shape_change"]={"before_children":len(a.children),"after_children":len(b.children)}
loc={};effective={}
for lang in ("english","simp_chinese"):
 vals={};dups=[];headers=[];effective[lang]={}
 for rel in freeze["owned_files"]:
  if rel.startswith("localization/"+lang+"/"):
   text=read(S/rel);pairs=re.findall(r'^\s+([\w.]+):\d*\s+"(.*)"\s*$',text,re.M);headers.append({"file":rel,"header":text.splitlines()[0]})
   for k,v in pairs:
    if k in vals:dups.append(k)
    vals[k]=v
 for root in (G/"localization"/lang,S/"localization"/lang):
  for p in sorted(root.rglob("*.yml")):
   for k,v in re.findall(r'^\s*([\w.]+):\d*\s+"(.*)"\s*$',p.read_text(encoding="utf-8-sig",errors="replace"),re.M):effective[lang][k]={"value":v,"source":str(p)}
 loc[lang]={"count":len(vals),"values":vals,"duplicates":dups,"headers":headers,"effective_overrides":[{"key":k,**effective[lang][k]} for k,v in vals.items() if effective[lang].get(k,{}).get("value")!=v]}
loc["paired"]=loc["english"]["values"].keys()==loc["simp_chinese"]["values"].keys()
missing=[]
for rel in cfg["owned_files"]:
 if rel.endswith(".txt"):
  for n in parse(read(S/rel)).walk():
   if n.key in ("title","desc","text","custom_tooltip") and n.value and n.value.startswith("nesnd_") and not all(n.value in effective[l] for l in effective):missing.append({"file":rel,"field":n.key,"value":n.value})
loc["missing_explicit"]=missing;out["localization"]=loc
# C1 interface AST preservation by definition
out["C1_interface"]={}
for key,x in freeze["dependencies"].items():
 if key.startswith("C1:"):
  rel=key.split(":",1)[1];a=defs(Path(x["frozen_copy"]));b=defs(S/rel)
  out["C1_interface"][rel]={"changed_old_definitions":[k for k in a if k not in b or shape(a[k])!=shape(b[k])],"added":[k for k in b if k not in a]}
a=json.loads((RUN/"tiger-baseline-raw.json").read_text(encoding="utf-8-sig"));b=json.loads((RUN/"tiger-current-raw.json").read_text(encoding="utf-8-sig"))
def sig(d):return(d["key"],d["message"],tuple((x["path"].replace("\\","/"),(x.get("line") or "").strip()) for x in d.get("locations",[])))
am={sig(d):d for d in a};bm={sig(d):d for d in b}
(RUN/"tiger-delta.json").write_text(json.dumps({"baseline":len(a),"current":len(b),"added":[bm[k] for k in bm.keys()-am.keys()],"removed":[am[k] for k in am.keys()-bm.keys()]},indent=2,ensure_ascii=True))
(RUN/"structure-contract.json").write_text(json.dumps(out,indent=2,ensure_ascii=True))
sources=[{"path":str(S/rel),"sha256":sha(S/rel)} for rel in cfg["owned_files"]]
sources += [{"path":x["source"],"sha256":x["sha256"]} for x in freeze["dependencies"].values()]
(RUN/"evidence-source-sha.json").write_text(json.dumps(sources,indent=2,ensure_ascii=True))
print(json.dumps({"owned_match":all(x["match"] for x in out["owned"]),"loc":[loc[l]["count"] for l in ("english","simp_chinese")],"paired":loc["paired"],"loc_overrides":[len(loc[l]["effective_overrides"]) for l in ("english","simp_chinese")],"missing_loc":missing,"top_if":len(out["top_level_builtin_errors"]),"native_diff":out["native_diff"],"C1_interface":out["C1_interface"]},ensure_ascii=True))

