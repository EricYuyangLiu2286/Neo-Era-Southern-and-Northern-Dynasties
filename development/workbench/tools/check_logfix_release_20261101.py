"""Fast source-pattern regression and final Tiger delta; never launches the game."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,collections
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
R=W/'reports/logfix-release-20261101';P=W/'exports/resumed-integrated-20261101-a';C=W/'exports/release-logfix-20261101-a'
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse,emit
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(root):
 problems=[]
 # Check the exact malformed-preview patterns from the captured native log.
 e=parse((root/'common/scripted_effects/nesnd_supply_effects.txt').read_text('utf-8-sig'))
 n=e.get('nesnd_supply_save_pending_sponsor');first=n.children[0]
 if not(first.key=='if' and first.get('limit') and first.get('limit').scalar('exists')=='var:nesnd_supply_pending'):problems.append('pending effect dereferences its value before an existence branch')
 t=parse((root/'common/scripted_triggers/nesnd_supply_triggers.txt').read_text('utf-8-sig'));n=t.get('nesnd_supply_partner_valid')
 first=n.children[0];last=n.children[-1]
 if not(first.key=='trigger_if' and first.get('limit') and all(v in [x.value for x in first.get('limit').all('exists')] for v in ('var:nesnd_supply_partner','var:nesnd_supply_sponsor','var:nesnd_supply_partner_sponsor')) and last.key=='trigger_else' and last.scalar('always')=='no'):problems.append('partner validity dereferences missing objects instead of returning false')
 for sub in ('common/scripted_buttons','common/scripted_effects','events','common/journal_entries','common/decisions'):
  for f in (root/sub).rglob('*.txt'):
   s=f.read_text('utf-8-sig');tree=parse(s)
   def walk(n,anc):
    if n.key=='remove_modifier' and n.value:
     if not any(a.key=='if' and a.get('limit') and any(x.key=='has_modifier' and x.value==n.value for x in a.get('limit').walk()) for a in anc):problems.append(str(f.relative_to(root))+': unguarded removal '+n.value)
    for x in n.children or []:walk(x,anc+[n])
   walk(tree,[])
 # Engine syntax requires quoted function-style comparison keys.
 for f in (root/'events').glob('nesnd_supply*.txt'):
  for no,line in enumerate(f.read_text('utf-8-sig').splitlines(),1):
   if re.match(r'\s*relations\(',line):problems.append(f'{f.name}:{no}: unquoted function key')
 return problems
before=check(P);after=check(C);assert before and not after,(before,after)
config=W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'
exe=W/'tools/tiger-1.19.0/vic3-tiger.exe'
cmd=[str(exe),'--game','D:/Program Files (x86)/Steam/steamapps/common/Victoria 3','--config',str(config),'--json',str(C)]
q=subprocess.run(cmd,capture_output=True);(R/'tiger-final-raw.json').write_bytes(q.stdout);(R/'tiger-final-stderr.txt').write_bytes(q.stderr)
raw=json.loads(q.stdout.decode('utf-8-sig'));base=json.loads((W/'validation/runs/release-logfix-20261101-a/tiger_baseline_raw.json').read_text('utf-8-sig'))
def norm(d):return json.dumps({'severity':d.get('severity'),'key':d.get('key'),'message':d.get('message'),'locations':[(x.get('from'),x.get('path'),(x.get('line') or '').strip()) for x in d.get('locations',[])]},ensure_ascii=False,sort_keys=True)
added=[json.loads(k) for k,n in (collections.Counter(map(norm,raw))-collections.Counter(map(norm,base))).items() for _ in range(n)]
new_errors=[x for x in added if x['severity']=='error']
changed=[f.relative_to(C).as_posix() for f in C.rglob('*') if f.is_file() and (not(P/f.relative_to(C)).exists() or sha(f)!=sha(P/f.relative_to(C)))]
for rel in changed:
 if rel.endswith('.txt'):parse((C/rel).read_text('utf-8-sig'))
qa=[]
for root in (C/'gui',C/'events',C/'common/on_actions',C/'tools'):
 if root.exists():
  for f in root.rglob('*'):
   if f.is_file() and (re.search(r'qa|probe|fixture',f.name,re.I) or b'ExecuteConsoleCommand' in f.read_bytes()):qa.append(str(f.relative_to(C)))
report={'source_regression':{'before_failures':before,'after_failures':after,'status':'PASS','boundary':'Checks real source patterns from captured native failures; does not execute the engine'},'tiger_new_errors':new_errors,'tiger_added_diagnostics':added,'tiger_counts':dict(collections.Counter(x.get('severity') for x in raw)),'changed_files':changed,'production_QA_leaks':qa,'command':cmd,'engine_rerun':False}
(R/'final-source-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k in ('tiger_counts','tiger_new_errors','production_QA_leaks')}));print('source regression',len(before),'->',len(after),'new diagnostics',len(added))
raise SystemExit(1 if after or new_errors or qa else 0)
