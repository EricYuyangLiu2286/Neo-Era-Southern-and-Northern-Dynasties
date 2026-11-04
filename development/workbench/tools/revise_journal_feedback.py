from journal_war_context import *
import re

def edit(rel,fn):
    p=C/rel;write(p,fn(read(p)))

# The parameter is supplied by each known caller: country-root JE/effect, or JE-root bar.
edit('common/scripted_triggers/nesnd_india_core.txt',lambda s:s.replace('prev.prev.owner','$COUNTRY$'))
for rel in ['common/journal_entries/nesnd_india_core.txt','common/scripted_effects/nesnd_india_core.txt']:
    edit(rel,lambda s:s.replace('nesnd_india_industry_ready = yes','nesnd_india_industry_ready = { COUNTRY = root }'))
edit('common/scripted_progress_bars/nesnd_india_core.txt',lambda s:s.replace('nesnd_india_industry_ready = yes','nesnd_india_industry_ready = { COUNTRY = root.owner }'))

# Original transition effect retained byte-for-byte except for one eligibility condition.
p=G/'common/scripted_effects/00_victoria_ep2_scripted_effects.txt';s=read(p);n=parse(s).get('transition_off_of_monarchy_effects')
t=s[n.start:n.end];needle='\t\t\tNOR = {\n\t\t\t\thas_journal_entry = je_abolish_monarchy'
assert needle in t
t=t.replace(needle,'\t\t\tnesnd_native_abolish_monarchy_eligible = yes\n'+needle,1)
write(C/'common/scripted_effects/zzzz_nesnd_hus_monarchy_entry.txt','REPLACE:'+t+'\n')

for je,bar,score in [('nesnd_wu_eastern_question','nesnd_eastern_readiness_bar','nesnd_japan_preparation_score'),('nesnd_japan_reunification','nesnd_japan_unification_bar','nesnd_japan_unity_score')]:
    p=C/'common/journal_entries/nesnd_japan.txt';s=read(p);n=parse(s).get(je).get('immediate')
    block=s[n.start:n.end];assert 'set_bar_progress' not in block
    block=block[:-1]+f' scope:journal_entry ?= {{ set_bar_progress = {{ name = {bar} value = owner.{score} }} }} }}'
    write(p,s[:n.start]+block+s[n.end:])

# Each event AI modifier has an explicit trigger, as in vanilla balkan_wars_events.
p=C/'events/nesnd_south_holdouts.txt';s=read(p)
mods=[n for n in parse(s).walk() if n.key=='modifier' and n.get('factor')]
for n in sorted(mods,key=lambda x:x.start,reverse=True):
    f=n.get('factor');conditions=[q for q in n.children if q.key!='factor'];assert not n.get('trigger')
    body=' '.join(s[q.start:q.end] for q in conditions)
    body=body.replace('relations:scope:nesnd_holdout_sender','"relations(scope:nesnd_holdout_sender)"')
    body=body.replace('relations:c:CNE','"relations(c:CNE)"').replace('relations:c:USM','"relations(c:USM)"')
    for target in ['scope:nesnd_holdout_sender','c:CNE','c:USM']:
        if target in body:
            body=f'trigger_if = {{ limit = {{ exists = {target} }} {body} }} trigger_else = {{ always = no }}'
    s=s[:n.start]+f'modifier = {{ factor = {f.value} trigger = {{ {body} }} }}'+s[n.end:]
write(p,s)

for rel in ['common/on_actions/nesnd_hus_monarchy_history.txt','common/on_actions/nesnd_south_holdouts.txt']:
    edit(rel,lambda s:re.sub(r'^\} \}$','    }\n}',s,flags=re.M))
print('Review corrections: entry, initialization, trigger parameters and AI wrappers.')
