from maintenance_20261102_context import *
p=C/'common/scripted_buttons/nesnd_supply_buttons.txt';s=read(p);hits=[]
for n in parse(s).walk():
 if n.key=='set_variable' and n.scalar('name')=='nesnd_supply_trade_pending':
  d=n.get('days');assert d and d.value=='30';hits.append((d.start,d.end))
assert len(hits)==1
for a,b in reversed(hits):s=s[:a]+'months = 4'+s[b:]
write(p,s)
p=C/'events/nesnd_supply_events.txt';s=read(p)
for ev,predicate in [('nesnd_supply.1','nesnd_supply_request_valid'),('nesnd_supply.2','nesnd_supply_trade_request_valid')]:
 n=parse(s).get(ev);assert n.get('cancellation_trigger') is None;t=n.get('trigger');s=s[:t.end]+f'\n cancellation_trigger = {{ NOT = {{ {predicate} = yes }} }}'+s[t.end:]
write(p,s)
print('Both contact and treaty replies retain identities for4months and cancel when invalid.')
