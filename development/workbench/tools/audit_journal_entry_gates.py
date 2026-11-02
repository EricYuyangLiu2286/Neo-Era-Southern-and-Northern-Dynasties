from qin_persia_context import *
from collections import defaultdict
helpers={};journals={};adds=defaultdict(list)
for p in (C/'common/scripted_triggers').glob('*.txt'):
 for n in parse(read(p)).children:helpers[n.key.removeprefix('REPLACE:')]=n
for p in (C/'common/journal_entries').glob('*.txt'):
 for n in parse(read(p)).children:
  if n.children:journals[n.key.removeprefix('REPLACE:')]=(p,n)
roots=[C/'events',C/'common/scripted_effects',C/'common/on_actions',C/'common/journal_entries',C/'common/scripted_buttons',C/'common/decisions',C/'common/history/countries']
for directory in roots:
 for p in directory.rglob('*.txt'):
  for n in parse(read(p)).walk():
   if n.key=='add_journal_entry':adds[n.scalar('type')].append({'file':p.relative_to(C).as_posix(),'line':read(p).count('\n',0,n.start)+1})
def refs(n,neg=False,seen=None):
 seen=set() if seen is None else seen;out=[]
 if n is None:return out
 if n.key=='has_journal_entry':out.append({'JE':n.value,'negated':neg})
 if n.key in helpers and n.key not in seen:out+=refs(helpers[n.key],neg,seen|{n.key})
 for c in n.children or []:out+=refs(c,not neg if n.key in ['NOT','NOR'] else neg,seen)
 return out
out=[];suspects=[]
for k,(p,n) in journals.items():
 dep=refs(n.get('possible'))+refs(n.get('is_shown_when_inactive'))
 self_positive=[x for x in dep if x['JE']==k and not x['negated']]
 disabled=any(a.key=='always' and a.value=='no' for field in ['possible','is_shown_when_inactive'] for a in (n.get(field).children if n.get(field) else []))
 rec={'JE':k,'file':p.relative_to(C).as_posix(),'positive_self_gate':bool(self_positive),'creation_dependencies':dep,'explicit_adds':adds[k],'directly_disabled':disabled,'terminal_fields':[f for f in ['complete','fail','invalid','timeout'] if n.get(f)],'terminal_callbacks':[f for f in ['on_complete','on_fail','on_invalid','on_timeout'] if n.get(f)]}
 out.append(rec)
 if self_positive:suspects.append(rec)
dump(R/'all-journal-entry-gates.json',{'status':'SOURCE_AUDIT','journals':out,'positive_self_gate_candidates':suspects,'count':len(out),'boundary':'dependency references are not a general boolean proof; disabled placeholders retained, no engine execution','game_launched':False})
print('Audited',len(out),'MOD journals; positive self-gate candidates:',[x['JE'] for x in suspects]);print('Previously disabled:',[x['JE'] for x in out if x['directly_disabled']])
