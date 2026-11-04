from pathlib import Path
import subprocess,json,collections
W=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench");R=W/"reports/canon-route-execution-20261104";cfg=json.loads((R/"batch-a2-test-config.json").read_text())
run=Path(cfg["run"]);owned=set(cfg["owned_files"])
for label,key in (("baseline","baseline_snapshot"),("current","snapshot")):
 command=[str(W/"tools/tiger-1.19.0/vic3-tiger.exe"),"--game",r"D:/Program Files (x86)/Steam/steamapps/common/Victoria 3","--config",str(W/"validation/runs/release-logfix-20261101-a/tiger-load-order.conf"),"--json",cfg[key]]
 with (run/f"tiger-{label}-raw.json").open("wb") as out,(run/f"tiger-{label}-stderr.txt").open("wb") as err:result=subprocess.run(command,stdout=out,stderr=err)
 raw=json.loads((run/f"tiger-{label}-raw.json").read_text(encoding="utf-8-sig"))
 diagnostics=[d for d in raw if any(l.get("path","").replace("\\","/") in owned for l in d.get("locations",[]))]
 (run/f"tiger-{label}-owned.json").write_text(json.dumps({"command":command,"returncode":result.returncode,"total":len(raw),"owned_diagnostics":diagnostics,"counts":dict(collections.Counter(d["key"] for d in diagnostics))},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(label,len(raw),dict(collections.Counter(d["key"] for d in diagnostics)),flush=True)
