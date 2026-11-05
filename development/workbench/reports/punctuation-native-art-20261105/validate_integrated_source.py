"""Verify the actual installed mod against reviewed inputs and run Tiger on that directory."""
from pathlib import Path
import collections, hashlib, json, subprocess, sys
R = Path(__file__).resolve().parent
W = R.parents[1]
M = W.parent / 'mod/Neo-Era Southern and Northern Dynasties'
folders = ('common', 'events', 'localization', 'gfx', 'gui', 'map_data', '.metadata')
load = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
expected = dict(load(R/'independent-stageC/inputs.json')['baseline_manifest'])
changed = {}
for manifest, before, after in [
 ('stageB-script-freeze.json','parent_sha256','sha256'),
 ('stageB-player-text-applied.json','before_sha256','after_sha256'),
 ('stageC-implementation-manifest.json','before_sha256','after_sha256')
]:
 for row in load(R/manifest)['files']:
  key = row['file']
  assert key not in changed, ('unreviewed overlapping edits', key)
  assert expected.get(key) == row.get(before), ('baseline mismatch',key,expected.get(key),row.get(before))
  expected[key] = row[after]
  changed[key] = manifest
live = {p.relative_to(M).as_posix():sha(p) for folder in folders for p in (M/folder).rglob('*') if p.is_file()}
assert live == expected, ('live input differs', {key for key in live.keys()|expected.keys() if live.get(key)!=expected.get(key)})
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
parsed = 0
for folder in ['common','events']:
 for p in (M/folder).rglob('*.txt'):
  parse(p.read_text(encoding='utf-8-sig')); parsed += 1
regression = subprocess.run([sys.executable,'-X','utf8',str(W/'reports/runtime-followup-20261104/check_runtime_contracts.py'),str(M)], capture_output=True,check=True)
assert not json.loads(regression.stdout)['failures']
tiger = W/'tools/tiger-1.19.0/vic3-tiger.exe'
args = [str(tiger),'--game','D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(R/'independent-stageC/tiger-full.conf'),'--json',str(M)]
raw = subprocess.run(args,capture_output=True,check=True,timeout=240)
(R/'integrated-tiger.json').write_bytes(raw.stdout)
rows = json.loads(raw.stdout); previous = load(R/'independent-stageC/tiger-full-B.json')
def signature(d):
 return (d['key'],d['severity'],d['message'],tuple((x.get('path'),x.get('tag')) for x in d.get('locations',[])))
diff=collections.Counter(signature(x) for x in rows)-collections.Counter(signature(x) for x in previous)
out={'source_sha256':hashlib.sha256(json.dumps(live,sort_keys=True).encode()).hexdigest(),'game_files':len(live),'parsed_script_files':parsed,'overlay_paths':len(changed),'runtime_contract_errors':0,'tiger_baseline':len(previous),'tiger_final':len(rows),'tiger_final_errors':sum(x['severity']=='error' for x in rows),'added_diagnostics':list(diff.elements()),'engine_run':False}
(R/'integrated-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
assert not diff, 'new Tiger diagnostics'
