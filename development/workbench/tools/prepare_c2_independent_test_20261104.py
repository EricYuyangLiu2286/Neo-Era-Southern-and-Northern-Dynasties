from pathlib import Path
import json,shutil,hashlib,datetime
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((R/"batch-c2-freeze.json").read_text()); a=json.loads((R/"batch-a2-owned-files-sha256.json").read_text())
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
run=W/"validation/runs"/("batch-c2-"+stamp);run.mkdir(parents=True)
base=W/"validation/snapshots/batch-b2-repair1-20261104T164006Z/mod"
p=W/"validation/snapshots"/("batch-c2-baseline-"+stamp)/"mod";s=W/"validation/snapshots"/("batch-c2-"+stamp)/"mod"
shutil.copytree(base,p)
af=W/"backups/batch-a2-frozen-owned-20261104"
for x in a["files"]:
 q=af/x["path"];assert sha(q)==x["sha256"]; t=p/x["path"];t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(q,t)
deps=[]
for k,x in f["dependencies"].items():
 q=Path(x.get("frozen_copy",x["source"]));assert sha(q)==x["sha256"],k
 if k.startswith("MOD:"):
  rel=k.split(":",1)[1];t=p/rel;deps.append({"key":k,"captured":x["sha256"],"assembled":sha(t) if t.exists() else None,"match":t.exists() and sha(t)==x["sha256"]})
shutil.copytree(p,s)
for rel,h in f["owned_files"].items():
 q=Path(f["owned_freeze"])/rel;assert sha(q)==h;t=s/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(q,t)
cfg={"run":str(run),"snapshot":str(s),"baseline_snapshot":str(p),"frozen_owned":f["owned_freeze"],"owned_files":list(f["owned_files"]),"dependency_capture_comparison":deps,"assembled_files":len(list(s.rglob("*.*"))),"source_freeze":str(R/"batch-c2-freeze.json"),"A2":"original immutable freeze; no changing candidate read","base":str(base)}
(R/"batch-c2-test-config.json").write_text(json.dumps(cfg,indent=2)+"\n")
(run/"snapshot-sha.json").write_text(json.dumps({str(q.relative_to(s)).replace("\\\\","/"):sha(q) for q in s.rglob("*") if q.is_file()},indent=2)+"\n")
for stem in ("tiger","mcp"):
 text=(W/"tools"/("test_a2_"+stem+"_20261104.py")).read_text()
 text=text.replace("batch-a2-test-config.json","batch-c2-test-config.json").replace("mcp-a2.json","mcp-c2.json")
 if stem=="mcp":
  start=text.index('   for path,symbol in [');end=text.index('   for name,args in calls:')
  text=text[:start]+'''   for path,symbol in [
    ("common/scripted_effects/nesnd_civic_routes.txt","nesnd_c2_monthly"),
    ("common/scripted_effects/nesnd_civic_characters.txt","nesnd_c2_characters_monthly"),
    ("common/scripted_triggers/nesnd_civic_routes.txt","nesnd_c2_italy_country"),
    ("common/journal_entries/nesnd_civic_routes.txt","je_nesnd_italy_foundations"),
    ("common/script_values/nesnd_civic_routes.txt","nesnd_c2_weekly_quote")]:calls.append(("get_structure",{"file_path":path,"symbol":symbol}))
'''+text[end:]
 (W/"tools"/("test_c2_"+stem+"_20261104.py")).write_text(text)
print(json.dumps({"config":cfg,"dependency_mismatches":[x for x in deps if not x["match"]]},indent=2))

