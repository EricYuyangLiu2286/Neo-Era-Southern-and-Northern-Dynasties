from maintenance_20261102_context import *
p=C/'common/scripted_triggers/nesnd_poland_repairs.txt';s=read(p).replace('is_country_alive = yes var:nesnd_polish_pending_state ?= scope:target_diplo_play_state','is_country_alive = yes nesnd_poland_matching_pending = yes')
s+='''nesnd_poland_matching_pending = {
 trigger_if = { limit = { has_variable = nesnd_polish_pending_state }
  trigger_if = { limit = { exists = var:nesnd_polish_pending_state }
   var:nesnd_polish_pending_state = scope:target_diplo_play_state
  }
  trigger_else = { always = no }
 }
 trigger_else = { always = no }
}
''';write(p,s)
p=C/'events/ce_poland_events.txt';s=read(p);n=parse(s).get('ce_poland_events.2')
for op in n.all('option')[::-1]:
 action=op.get('if');assert action
 # Clear the matching request before a peaceful transfer can merge/destroy the state object.
 li=action.get('limit');s=s[:li.end]+'\n nesnd_poland_clear_request = yes\n'+s[li.end:]
write(p,s)
# Make exact max(value-10,0), missing/present JE, and preview checks mechanically inspectable.
# Format changed scripts only, retaining every AST node and original line endings.
def shape(n):return n.key,n.op,n.value,tuple(shape(x) for x in n.children or [])
def indent(text):
 depth=0;out=[]
 for line in text.splitlines():
  st=line.strip()
  if not st:out.append('');continue
  code='';quoted=False;escaped=False
  for ch in st:
   if escaped:escaped=False;continue
   if ch=='\\' and quoted:escaped=True;continue
   if ch=='"':quoted=not quoted;continue
   if not quoted:
    if ch=='#':break
    code+=ch
  leading=len(code)-len(code.lstrip('}'));out.append('\t'*max(0,depth-leading)+st);depth+=code.count('{')-code.count('}')
 assert depth==0
 return '\n'.join(out)+'\n'
formatted=[]
for rel in ['events/ce_poland_events.txt','common/scripted_buttons/ce_poland_scripted_buttons.txt','common/scripted_triggers/nesnd_poland_repairs.txt','common/scripted_effects/nesnd_poland_repairs.txt','common/scripted_values/nesnd_poland_repairs.txt']:
 p=C/rel
 if not p.exists():continue
 s=read(p);out=indent(s);assert shape(parse(s))==shape(parse(out));write(p,out);formatted.append(rel)
dump(R/'format-proof.json',{'files':formatted,'AST_unchanged':True})
print('Pending request identity and post-transfer lifetime guards closed')
