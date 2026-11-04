from sweep_context import *
import re
inventory=json.loads(read(R/'analogue-inventory.json'))
# Approved homogeneous metadata change: only named MOD historical journals from the reviewed inventory.
for rel in sorted({x['file'] for x in inventory['missing_pins']}):
 p=C/rel;s=read(p);keys={x['key'] for x in inventory['missing_pins'] if x['file']==rel}
 for n in sorted([x for x in parse(s).children if x.key in keys],key=lambda x:x.end,reverse=True):
  assert n.scalar('group')=='je_group_historical_content' and not n.get('should_be_pinned_by_default_uninvolved_or_context')
  s=s[:n.end-1]+'    should_be_pinned_by_default_uninvolved_or_context = yes\n'+s[n.end-1:]
 write(p,s)
# Same cooldown fact, exactly three known funding actions. Execution conditions remain unmodified.
p=C/'common/scripted_buttons/nesnd_jp_politics.txt';s=read(p)
for n in sorted([n for n in parse(s).children if n.key in ['nesnd_jp_inspect_court','nesnd_jp_inspect_military','nesnd_jp_inspect_representative']],key=lambda n:n.start,reverse=True):
 q=n.get('possible').get('NOT');assert q.scalar('has_variable')=='nesnd_jp_reform_effort_cooldown'
 s=s[:q.start]+'custom_tooltip = { text = nesnd_sweep_reform_ready '+s[q.start:q.end]+' }'+s[q.end:]
write(p,s)
dump(R/'bulk-changes.json',{'pins':inventory['missing_pins'],'cooldown_buttons':3,'purpose':'Repeated identical UI metadata only; gameplay written directly with patches.'})
print('Pinned',len(inventory['missing_pins']),'story journals; three explicit cooldown labels.')
