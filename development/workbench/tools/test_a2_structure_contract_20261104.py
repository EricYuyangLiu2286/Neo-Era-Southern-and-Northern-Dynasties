from pathlib import Path
import sys,json,re,hashlib,collections
sys.path.insert(0,r"C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts")
from pdx import parse,basekey
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104";cfg=json.loads((R/"batch-a2-test-config.json").read_text());S=Path(cfg["snapshot"]);P=Path(cfg["baseline_snapshot"]);F=Path(cfg["frozen_owned"]);RUN=Path(cfg["run"]);G=Path(r"D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game")
m=json.loads((R/"batch-a2-owned-files-sha256.json").read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return p.read_text(encoding="utf-8-sig")
def shape(n):return None if n is None else (n.key,n.op,n.value,tuple(shape(x) for x in n.children or []))
def defs(p):return {basekey(n.key):n for n in parse(read(p)).children}
out={"status":"STRUCTURE_AND_SOURCE_DIFF_ONLY","behavior_pass_claimed":False,"owned":[],"parsed":0,"baseline_identity":[],"a1_preservation":{}}
for x in m["files"]:
 rel=x["path"];a=sha(F/rel);b=sha(S/rel);out["owned"].append({"path":rel,"sha256":a,"freeze_and_snapshot_match":a==b==x["sha256"]})
 if rel.endswith(".txt"):parse(read(S/rel));out["parsed"]+=1
 if x["baseline_sha256"] is not None:out["baseline_identity"].append({"path":rel,"match":sha(P/rel)==x["baseline_sha256"]})
for rel,h in cfg["a1_sha"].items():
 if rel not in cfg["owned_files"]:out["a1_preservation"][rel]=sha(S/rel)==h
rel="common/scripted_effects/nesnd_hus_registration.txt";old=defs(P/rel);new=defs(S/rel)
out["a1_hus_effects_changed_definitions"]=[k for k,v in old.items() if shape(v)!=shape(new.get(k))]
rel="events/nesnd_hus_registration.txt";old=defs(P/rel);new=defs(S/rel)
out["a1_event10_preserved"]=shape(old["nesnd_hus_registration.10"])==shape(new["nesnd_hus_registration.10"])
rel="common/scripted_effects/nesnd_native_khanate.txt";old=defs(P/rel);new=defs(S/rel)
out["a1_native_primary_helper_preserved"]=shape(old["nesnd_native_primary_cultures_only"])==shape(new["nesnd_native_primary_cultures_only"])
laws=[x.value for x in new["nesnd_khanate_successor_laws"].walk() if x.key=="activate_law"]
out["successor_ordinary_laws"]={"count":len(laws),"unique":len(set(laws)),"no_hus_special_registration_law":not any("nesnd_hus" in x for x in laws)}
orig=defs(G/"common/scripted_buttons/turtle_island_buttons.txt");now=defs(S/"common/scripted_buttons/zzzz_nesnd_turtle_island.txt");tis={}
for key,a in orig.items():
 b=now[key]
 ef=b.get("effect").get("if")
 tis[key]={"name_desc_preserved":all(shape(a.get(k))==shape(b.get(k)) for k in ("name","desc")),"visible_original_children_retained":tuple(shape(x) for x in a.get("visible").children)==tuple(shape(x) for x in b.get("visible").children[2:]),"possible_original_children_retained":tuple(shape(x) for x in a.get("possible").children)==tuple(shape(x) for x in b.get("possible").children[2:]),"effect_original_body_retained":tuple(shape(x) for x in a.get("effect").children)==tuple(shape(x) for x in ef.children if x.key!="limit")}
out["turtle_island_native_ast"]=tis
out["cherokee_7_stubs_unchanged"]=sha(P/"events/native_resettlement.txt")==sha(S/"events/native_resettlement.txt")
loc={}
for lang in ("english","simp_chinese"):
 p=S/f"localization/{lang}/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_{lang}.yml";data=p.read_bytes();text=data.decode("utf-8-sig");pairs=re.findall(r'^\s+([\w.]+):\d*\s+"(.*)"\s*$',text,re.M)
 loc[lang]={"BOM":data.startswith(b"\xef\xbb\xbf"),"header":text.splitlines()[0],"count":len(pairs),"duplicates":[k for k,v in collections.Counter(k for k,v in pairs).items() if v>1],"values":dict(pairs)}
loc["paired_keys"]=set(loc["english"]["values"])==set(loc["simp_chinese"]["values"])
effective={lang:{} for lang in ("english","simp_chinese")}
for lang in effective:
 for root in (G/"localization"/lang,S/"localization"/lang):
  for p in sorted(root.rglob("*.yml")):
   for k,v in re.findall(r'^\s*([\w.]+):\d*\s+"(.*)"\s*$',p.read_text(encoding="utf-8-sig",errors="replace"),re.M):effective[lang][k]=str(p)
missing=[]
for rel in cfg["owned_files"]:
 if not rel.endswith(".txt"):continue
 for n in parse(read(S/rel)).walk():
  if n.key in ("title","desc","text","custom_tooltip") and n.value and n.value.startswith("nesnd_"):
   if not all(n.value in effective[l] for l in effective):missing.append({"file":rel,"key":n.value})
loc["unresolved_explicit_refs"]=missing
out["localization"]=loc
a=json.loads((RUN/"tiger-baseline-owned.json").read_text());b=json.loads((RUN/"tiger-current-owned.json").read_text())
def sig(d):return(d["key"],d["message"],tuple((x["path"].replace("\\","/"),(x.get("line") or "").strip()) for x in d.get("locations",[])))
am={sig(d):d for d in a["owned_diagnostics"]};bm={sig(d):d for d in b["owned_diagnostics"]}
delta={"current_counts":b["counts"],"baseline_counts":a["counts"],"added":[bm[k] for k in bm.keys()-am.keys()],"removed":[am[k] for k in am.keys()-bm.keys()],"classifications":{"has_role unprefixed specific IDs":"CONFIRMED_DEFECT plus actual AST commander red/control and native source actual instance","date country triggers":"CONFIRMED_UNKNOWN_NATIVE_TRIGGER; engine registry provides game_date, native events use game_date; date only history syntax is not this trigger","control_half_target_country_states":"TOOL_ENUM_LAG: actual GAME 00_annex_country.txt:19 uses exact same value","dynamic combat_unit count":"UNPROVEN_BLOCKING: Tiger expects integer; engine docs only literal example, no current native variable-count instance found. Native interface timing/acceptance remains NOT_RUN.","dynamic set_capital scope":"UNPROVEN: native docs say state region but Tiger treats static DB key; no current native dynamic instance located. Do not claim capital relocation tested.","ai_chance modifier":"UNRESOLVED: current scripted_buttons.md has old base/modifier example, whereas submitted value+modifier lacks that trigger wrapper and Tiger warns. Needs source-backed homogeneous shape, not global ignore.","strict scopes":"REQUIRES_GUARDED_REFERENCE_REPAIR_OR_NATIVE_PROOF; no aggregate ignore","encoding":"RETAINED_STYLE_WARNING with changed path grouping; localization BOM independently checked"}}
(RUN/"structure-contract.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");(RUN/"tiger-delta.json").write_text(json.dumps(delta,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
sources=[]
for p in [F/x["path"] for x in m["files"]]+[G/"common/character_roles/00_auto_assigned_roles.txt",G/"common/scripted_effects/00_victoria_ep2_scripted_effects.txt",G/"common/character_roles/character_roles.md",G/"common/commander_orders/orders.md",G/"common/scripted_buttons/scripted_buttons.md",G/"common/war_goal_types/00_annex_country.txt",W/"references/engine-docs-1.13.11-20261031/effects.log",W/"references/engine-docs-1.13.11-20261031/triggers.log"]:
 sources.append({"path":str(p),"sha256":sha(p)})
(RUN/"evidence-source-sha.json").write_text(json.dumps(sources,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps({"owned":len(out["owned"]),"parsed":out["parsed"],"owned_match":all(x["freeze_and_snapshot_match"] for x in out["owned"]),"baseline_match":all(x["match"] for x in out["baseline_identity"]),"a1_other_preserved":all(out["a1_preservation"].values()),"a1_effects_changed":out["a1_hus_effects_changed_definitions"],"a1_event10":out["a1_event10_preserved"],"a1_native_helper":out["a1_native_primary_helper_preserved"],"ordinary_laws":out["successor_ordinary_laws"],"loc_counts":[loc[l]["count"] for l in ("english","simp_chinese")],"paired":loc["paired_keys"],"unresolved":missing,"tiger_added":len(delta["added"]),"tiger_removed":len(delta["removed"])}))
