"""Build read-only engine probes and collect actual logs. Never launches or controls UI.
The overlay executes in Victoria 3 after real lobby entry and on monthly pulses.
Missing or buffered logs are NOT_OBSERVED/INCOMPLETE, never evidence of success. Engine output is distinct from
Python fixture coverage and static checks. No official scripted_tests output is used.
"""
from pathlib import Path
import argparse,json,re,hashlib,sys
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
TOKEN='NESND_BATCH_V1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def treehash(p):return {f.relative_to(p).as_posix():sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
def output_path(p):
 p=p.resolve()
 if not p.is_relative_to(W.resolve()):raise ValueError('Output must stay under workbench')
 return p
EVENT='''# QA only. Read-only: no world variables, flags, characters, laws or economics changed.
namespace = nesnd_batch_probe
nesnd_batch_probe.1 = {
 type = country_event
 hidden = yes
 immediate = {
  debug_log = "NESND_BATCH_V1 BEGIN USM"
  if = {
   limit = { has_journal_entry = ce_usm_conflicts_within }
   if = {
    limit = { has_variable = usm_conflicts_within_tracker has_variable = nesnd_compact_progress }
    debug_log = "NESND_BATCH_V1 RESULT usm_init PASS"
    if = {
     limit = { var:usm_conflicts_within_tracker >= 0 var:usm_conflicts_within_tracker <= 100 }
     debug_log = "NESND_BATCH_V1 RESULT usm_pressure_range PASS"
    }
    else = { debug_log = "NESND_BATCH_V1 RESULT usm_pressure_range FAIL" }
   }
   else = {
    debug_log = "NESND_BATCH_V1 RESULT usm_init FAIL"
    debug_log = "NESND_BATCH_V1 RESULT usm_pressure_range SKIP"
   }
  }
  else = {
   debug_log = "NESND_BATCH_V1 RESULT usm_init SKIP"
   debug_log = "NESND_BATCH_V1 RESULT usm_pressure_range SKIP"
  }
  debug_log = "NESND_BATCH_V1 END USM"
 }
}
'''
HOOK='''# QA only. The native engine supplies actual world state and advancing dates.
on_game_started_after_lobby = { on_actions = { nesnd_batch_probe_after_lobby } }
nesnd_batch_probe_after_lobby = {
 effect = { c:USM ?= { trigger_event = { id = nesnd_batch_probe.1 days = 1 } } }
}
on_monthly_pulse_country = { on_actions = { nesnd_batch_probe_monthly } }
nesnd_batch_probe_monthly = {
 effect = { if = { limit = { c:USM ?= this } trigger_event = { id = nesnd_batch_probe.1 days = 1 } } }
}
'''
CASES=['usm_init','usm_pressure_range']
def build(candidate,dest):
 candidate=candidate.resolve();dest=output_path(dest)
 if dest.exists():raise ValueError('Choose a new overlay directory; existing evidence is immutable')
 effects=candidate/'common/scripted_effects/nesnd_south_initialization.txt'
 txt=effects.read_text('utf-8-sig')
 # Probe fields must correspond to this version; never silently certify a renamed system.
 for name in ['usm_conflicts_within_tracker','nesnd_compact_progress']:
  if name not in txt:raise ValueError('Candidate field mismatch: '+name)
 for text in [EVENT,HOOK]:parse(text)
 for rel,text in [('events/nesnd_batch_probe.txt',EVENT),('common/on_actions/nesnd_batch_probe.txt',HOOK)]:
  p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,'utf-8-sig')
 p=dest/'.metadata/metadata.json';p.parent.mkdir(parents=True);p.write_text(json.dumps({'name':'NESND Read-only Monthly Probe','id':'nesnd_readonly_probe','version':'1','supported_game_version':'1.13.11'},indent=2),'utf-8')
 report={'status':'generated_not_run','candidate':str(candidate),'candidate_manifest':treehash(candidate),'overlay':str(dest),'cases':CASES,'overlay_manifest':treehash(dest),'requires':'Mount after candidate and QA, enter real game then unpause. Reuses natural engine month pulses. Does not advance time itself.','coverage_exclusions':['UI hover/render','event options','war outcomes','economic balance','AI decisions','harbor navigation'],'expected_channel':'logs/debug.log after native game execution','official_scripted_tests_used':False}
 (dest/'PROBE-MANIFEST.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');return {'status':report['status'],'overlay':str(dest),'cases':CASES}
def collect(log,dest,manifest,runfile=None):
 # Native rotation stores oldest at highest N; filenames, not mtimes, define order.
 family = log.is_dir() or re.fullmatch(r'debug(?:\.\d+)?\.log', log.name) is not None
 folder = log if log.is_dir() else log.parent
 if family:
  numbered=[]
  for file in folder.iterdir():
   m=re.fullmatch(r'debug\.(\d+)\.log',file.name)
   if file.is_file() and m:numbered.append((int(m[1]),file))
  files=[p for n,p in sorted(numbered,reverse=True)]
  if (folder/'debug.log').is_file():files.append(folder/'debug.log')
 else:files=[log]
 expected=json.loads(manifest.read_text('utf-8-sig'));required=set(expected['cases']);cycles=[];current=None;inputs=[];orphan_markers=[]
 for file in files:
  before=file.stat();raw=file.read_bytes();after=file.stat();text=raw.decode('utf-8-sig',errors='replace')
  inputs.append({'path':str(file),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'stable_during_read':before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns})
  for lineno,line in enumerate(text.splitlines(),1):
   pos={'file':str(file),'line':lineno}
   if TOKEN+' BEGIN USM' in line:
    if current:current['status']='INCOMPLETE';cycles.append(current)
    current={'start':pos,'results':[]}
   m=re.search(TOKEN+r' RESULT (\w+) (PASS|FAIL|SKIP)',line)
   if m:
    if current:current['results'].append({'case':m[1],'status':m[2],**pos})
    else:orphan_markers.append({'kind':'RESULT_WITHOUT_BEGIN','text':line,**pos})
   if TOKEN+' END USM' in line:
    if current:
     names=[r['case'] for r in current['results']];current['end']=pos
     current['status']='COMPLETE' if set(names)==required and len(names)==len(required) else 'INCOMPLETE'
     current['all_pass']=current['status']=='COMPLETE' and all(r['status']=='PASS' for r in current['results'])
     cycles.append(current);current=None
    else:orphan_markers.append({'kind':'END_WITHOUT_BEGIN','text':line,**pos})
 if current:current['status']='INCOMPLETE';cycles.append(current)
 seen={r['case'] for c in cycles if c['status']=='COMPLETE' for r in c['results']}
 anyfail=any(r['status']=='FAIL' for c in cycles for r in c['results']);passed={r['case'] for c in cycles if c['status']=='COMPLETE' for r in c['results'] if r['status']=='PASS'}
 fullpass=[i for i,c in enumerate(cycles) if c.get('all_pass')]
 status='FAIL' if anyfail else ('INCOMPLETE' if orphan_markers or any(c['status']!='COMPLETE' for c in cycles) else ('OBSERVED_PASS' if fullpass else ('SKIPPED_OR_PARTIAL' if cycles else 'NOT_OBSERVED_IN_AVAILABLE_LOGS')))
 binding={'verified':False,'reason':'No run.json supplied'}
 if runfile:
  run=json.loads(runfile.read_text('utf-8-sig')); candidate_ok=run.get('source_sha256')==expected['candidate_manifest']
  mounted=[Path(m['path']) for m in run.get('load',{}).get('enabledMods',[])]; probe_files={k:v for k,v in expected['overlay_manifest'].items() if k.endswith('.txt')}
  probe_ok=any(all((root/k).is_file() and sha(root/k)==v for k,v in probe_files.items()) for root in mounted)
  profile=Path(run['profile']).resolve(); log_ok=bool(files) and all(p.resolve().is_relative_to(profile/'logs') or p.resolve().is_relative_to(runfile.resolve().parent/'logs') for p in files)
  stable=all(x['stable_during_read'] for x in inputs)
  binding={'verified':candidate_ok and probe_ok and log_ok and stable,'candidate_match':candidate_ok,'mounted_probe_match':probe_ok,'log_path_match':log_ok,'stable_files':stable,'run':str(runfile),'run_sha256':sha(runfile)}
 report={'status':status,'engine_verified':binding['verified'] and status=='OBSERVED_PASS','binding':binding,'log_input':str(log),'rotation_family_included':family,'input_files_oldest_first':inputs,'manifest':str(manifest),'manifest_sha256':sha(manifest),'cycles':cycles,'orphan_markers':orphan_markers,'complete_all_pass_cycle_indices':fullpass,'required_cases':expected['cases'],'seen_cases':sorted(seen),'passed_cases':sorted(passed),'missing_cases':sorted(required-seen),'engine_evidence_boundary':'Only complete same-cycle emitted predicates, with engine_verified requiring run/candidate/mounted-probe/log binding. Missing markers never prove that the run did not execute: earlier rotations may be gone. No event-chain, UI or economy success inferred.'}
 output_path(dest).parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');return {k:report[k] for k in ['status','engine_verified','passed_cases','missing_cases']}
p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True);b=s.add_parser('build');b.add_argument('--candidate',type=Path,required=True);b.add_argument('--out',type=Path,required=True);c=s.add_parser('collect');c.add_argument('--log',type=Path,required=True);c.add_argument('--out',type=Path,required=True);c.add_argument('--manifest',type=Path,required=True);c.add_argument('--run',type=Path)
a=p.parse_args();print(json.dumps(build(a.candidate,a.out) if a.cmd=='build' else collect(a.log,a.out,a.manifest,a.run),ensure_ascii=False,indent=2))


