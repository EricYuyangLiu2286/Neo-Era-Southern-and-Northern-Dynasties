"""Ordered source execution of initialization guards only, not a game emulator.
Replays the exact v3/no-running/active-parent state that old cleanup can produce.
Unknown triggers/effects fail loudly; no invented default truth values.
"""
from cne_confidence_context import *
root=Path(sys.argv[1]);p=root/'common/scripted_effects/nesnd_cne_programs.txt'
n=parse(read(p)).get('nesnd_cne_programs_init')
flags={'nesnd_cne_programs_v3'}
def cond(n):
 def atom(a):
  if a.key=='has_variable':return a.value in flags
  if a.key=='NOT':return not cond(a)
  if a.key=='OR':return any(atom(x) for x in a.children)
  if a.key in ('AND','limit'):return cond(a)
  if a.key=='nesnd_reform_active':return a.value=='yes'
  if a.key=='has_journal_entry':return a.value=='ce_cne_land_reform'
  if a.key=='has_modifier':return False
  raise AssertionError(('unsupported trigger',a.key))
 return all(atom(a) for a in n.children or [])
def run(n):
 for a in n.children or []:
  if a.key=='if':
   if cond(a.get('limit')):run(a)
  elif a.key=='limit':pass
  elif a.key=='set_variable':flags.add(a.value or a.scalar('name'))
  elif a.key in ('nesnd_cne_confidence_init','nesnd_cne_ensure_children'):pass # separately checked; no effect on running repair
  else:raise AssertionError(('unsupported effect',a.key))
run(n)
out={'source':str(p),'case':'already initialized; running cleared; parent active; no terminal flag','running_restored':'nesnd_cne_programs_running' in flags,'scope':'source guard replay only; not engine/UI execution'}
print(json.dumps(out,ensure_ascii=False));dump(R/('activation-green.json' if out['running_restored'] else 'activation-red.json'),out)
sys.exit(0 if out['running_restored'] else 1)
