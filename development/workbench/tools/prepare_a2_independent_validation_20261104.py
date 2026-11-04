from pathlib import Path
import json,shutil,hashlib,datetime,sys
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104"
f=json.loads((R/"batch-a2-owned-files-sha256.json").read_text(encoding="utf-8"))
F=Path(f["frozen_owned"]);B=W/"validation/snapshots/batch-c-repair4-20261104T150000Z/mod"
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
run=R/("batch-a2-validation-"+stamp);run.mkdir()
S=W/("validation/snapshots/batch-a2-"+stamp)/"mod";shutil.copytree(B,S)
P=W/("validation/snapshots/batch-a2-baseline-"+stamp)/"mod";shutil.copytree(B,P)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
av=json.loads((R/"batch-a-validation.json").read_text(encoding="utf-8"));ab=Path(av["snapshot"])
for x in av["final_owned_file_identity"]:
 rel=x["path"];assert sha(ab/rel)==x["expected_sha256"],rel
 for root in (S,P):
  dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ab/rel,dst)
owned=[x["path"] for x in f["files"]]
for x in f["files"]:
 rel=x["path"];assert sha(F/rel)==x["sha256"],rel
 dst=S/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(F/rel,dst)
 prior=W/"backups/batch-a2-pre-change-20261104"/rel
 if prior.exists():
  dst=P/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(prior,dst)
 elif x["baseline_sha256"] is None and (P/rel).exists():(P/rel).unlink()
cfg={"run":str(run),"snapshot":str(S),"baseline_snapshot":str(P),"frozen_owned":str(F),"dependency_base":str(B),"a1_dependency_base":str(ab),"a1_sha":{x["path"]:x["expected_sha256"] for x in av["final_owned_file_identity"]},"owned_files":owned,"expected_unimplemented_dependency":[],"source":"C1 repair4 fixed full dependency snapshot plus exact validated 24-file A1 overlay plus exact hash-checked A2 owned; live C unused"}
(R/"batch-a2-test-config.json").write_text(json.dumps(cfg,indent=2)+"\n",encoding="utf-8")
(run/"snapshot.json").write_text(json.dumps({"config":cfg,"owned":{rel:sha(S/rel) for rel in owned},"all_files":{p.relative_to(S).as_posix():sha(p) for p in sorted(S.rglob("*")) if p.is_file()}},indent=2)+"\n",encoding="utf-8")
print(json.dumps(cfg))
