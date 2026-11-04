from sweep_context import *
# Homogeneous binding across the existing, explicitly enumerated border-state buttons.
p=C/'common/scripted_buttons/nesnd_per_border_claims.txt';s=read(p);nodes=parse(s).children;records=[]
for n in sorted(nodes,key=lambda n:n.start,reverse=True):
 if not n.key or not n.key.startswith('nesnd_per_claim_'):continue
 assert any(x.key=='nesnd_per_attempt_claim' for x in n.walk())
 e=n.get('effect');q=n.get('possible');assert q and e
 s=s[:e.vstart+1]+'\n        custom_tooltip = nesnd_per_claim_spend_25_tt'+s[e.vstart+1:]
 s=s[:q.vstart+1]+'\n        custom_tooltip = { text = nesnd_per_claim_cost_25_tt nesnd_per_claim_points >= 25 }'+s[q.vstart+1:]
 records.append(n.key)
write(p,s)
assert len(records)==37
# The 12 requests all use the same send-request fee, 45-day clock and six-month cooldown.
previews=[]
for rel in ['common/scripted_buttons/nesnd_jp_foreign.txt','common/scripted_buttons/nesnd_jp_korea.txt']:
 p=C/rel;s=read(p)
 selected=[n for n in parse(s).children if n.key and any(x.key=='nesnd_jp_send_request' for x in n.walk())]
 for n in sorted(selected,key=lambda n:n.start,reverse=True):
  e=n.get('effect');assert e and not e.get('show_as_tooltip')
  body=s[e.vstart+1:e.vend-1]
  wrapper='''effect = {
        custom_tooltip = nesnd_sweep_jp_request_terms
        show_as_tooltip = { add_treasury = { value = nesnd_jp_negotiation_cost multiply = -1 } }
        hidden_effect = {'''+body+''' }
    }'''
  s=s[:e.start]+wrapper+s[e.end:];previews.append(n.key)
 write(p,s)
assert len(previews)==12
dump(R/'resource-button-bindings.json',{'claims':records,'request_previews':previews,'semantics':'Original request execution preserved under hidden_effect; explicit fee preview uses same source expression.'})
print('Bound',len(records),'state claims; repaired',len(previews),'request previews.')
