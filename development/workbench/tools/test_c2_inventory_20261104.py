from test_c2_structure_20261104 import *
index=json.loads((R/"batch-c2-person-implementation-index.json").read_text(encoding="utf-8"))
templates=defs(S/"common/character_templates/nesnd_civic_characters.txt");events=defs(S/"events/nesnd_civic_characters.txt");roles=defs(G/"common/character_roles/00_auto_assigned_roles.txt")
rows=[]
for person in index:
 n=templates[person["id"]];birth=n.scalar("birth_date");year=int(birth.split(".")[0]);role=n.scalar("role")
 rows.append({"id":person["id"],"birth":birth,"birth_contract_match":birth==person["birth_date"],"opening_age":person["window"][0]-year,"role":role,"native_role":role is None or role in roles,"intro_exists":person["intro_event"] in events,"follow_exists":person["follow_event"] in events,"is_general":n.scalar("is_general"),"female":n.scalar("female"),"is_agitator":n.scalar("is_agitator")})
checks=[]
for lang in ("english","simp_chinese"):
 for filename in ("nesnd_civic_characters","nesnd_civic_routes"):
  p=S/f"localization/{lang}/replace/{filename}_l_{lang}.yml";pairs=re.findall(r'^\s+([\w.]+):\d*\s+"(.*)"\s*$',read(p),re.M)
  for k,v in pairs:checks.append({"language":lang,"key":k,"value":v,"effective":out["localization"][lang]["values"][k]==v,"source":str(p),"empty":not bool(v),"replacement_character":"\ufffd" in v})
audit={"persons":rows,"character_count":len(rows),"effective_C2_text_pairs":len(checks)//2,"text_rows":checks,"BOM":[x for x in out["owned"] if not x["BOM"]],"engine_run":False}
(RUN/"person-and-effective-text-audit.json").write_text(json.dumps(audit,ensure_ascii=True,indent=2),encoding="utf-8")
# Scoped write inventory and pinned-interface identities.
mut=[]
for rel in cfg["owned_files"]:
 if not rel.startswith(("common/scripted_effects/","events/","common/on_actions/")) or not rel.endswith(".txt"):continue
 for n in parse(read(S/rel)).walk():
  if n.key in ("activate_law","start_enactment","move_pop","move_partial_pop","annex","transfer_state","set_capital","create_diplomatic_play"):mut.append({"path":rel,"effect":n.key,"value":n.value})
identity={}
a1=json.loads((R/"batch-a-validation.json").read_text(encoding="utf-8"))
for x in a1.get("final_owned_file_identity",[]):
 rel=x["path"]
 if rel not in cfg["owned_files"] and rel not in {x["path"] for x in json.loads((R/"batch-a2-owned-files-sha256.json").read_text())["files"]}:identity[rel]=sha(S/rel)==x["expected_sha256"]
a2=json.loads((R/"batch-a2-owned-files-sha256.json").read_text())
a2identity={x["path"]:sha(S/x["path"])==x["sha256"] for x in a2["files"] if x["path"] not in cfg["owned_files"]}
b1identity={x["path"]:sha(S/x["path"])==x["sha256"] for x in cfg["B1_exact_owned"] if x["path"] not in cfg["owned_files"]}
out2={"A1_non_A2_pinned":identity,"A2_original_all32":a2identity,"B1_all34":b1identity,"C2_native_mutation_inventory":mut,"C2_captured_mod_dependencies_all_match":all(x["match"] for x in cfg["dependency_capture_comparison"])}
(RUN/"interface-inventory.json").write_text(json.dumps(out2,ensure_ascii=True,indent=2),encoding="utf-8")
print(json.dumps({"persons":len(rows),"birth_contracts":all(x["birth_contract_match"] for x in rows),"minimum_opening_age":min(x["opening_age"] for x in rows),"roles_valid":all(x["native_role"] for x in rows),"events":all(x["intro_exists"] and x["follow_exists"] for x in rows),"text_pairs":len(checks)//2,"BOM_missing":len(audit["BOM"]),"pinned_A1":all(identity.values()),"pinned_A2":all(a2identity.values()),"pinned_B1":all(b1identity.values()),"native_mutations":mut},ensure_ascii=True))

