from observer_logfix_context import *
import re
from pdx import replace_spans,emit

changes={}
def save(rel,before,after):
    if before!=after:
        write(C/rel,after);changes[rel]=sha(C/rel)

# The engine parses cancellation_trigger using the already-declared event type.
rel='events/nesnd_external_events.txt';s=read(C/rel);edits=[]
for event in parse(s).children:
    typ=event.get('type');cancel=event.get('cancellation_trigger')
    if typ and cancel and cancel.start<typ.start:
        edits.extend([(typ.start,typ.end,''),(cancel.start,cancel.start,'type = country_event\n\t')])
save(rel,s,replace_spans(s,edits))

# Quoted argument form is used by the current native diplomatic catalysts.
for rel in ['events/nesnd_india_diplomacy.txt','events/nesnd_jp_foreign.txt']:
    s=read(C/rel)
    save(rel,s,re.sub(r'relations:(scope:[A-Za-z0-9_]+)',r'"relations(\1)"',s))

rel='common/scripted_effects/nesnd_qe1_fracture.txt';s=read(C/rel)
assert s.count('ideology = ideology_jingoist }')==1
save(rel,s,s.replace('ideology = ideology_jingoist }','ideology = ideology_jingoist_leader }'))

# Saved characters may survive in exile/void while their owner no longer resolves.
# Missing owner means false only for an ownership comparison; do not erase people.
for rel in ['common/scripted_effects/nesnd_ming_royal_refuge.txt','common/scripted_effects/nesnd_ming_court.txt','common/scripted_effects/nesnd_ming_generation.txt']:
    before=read(C/rel);s=before;edits=[]
    for n in parse(s).walk():
        if n.key=='owner' and n.children is None and n.op=='=':
            original=s[n.start:n.end]
            edits.append((n.start,n.end,'trigger_if = { limit = { exists = owner } '+original+' } trigger_else = { always = no }'))
    s=replace_spans(s,edits)
    # An exists sibling is not a short-circuit guard. Nest the actual character read.
    edits=[]
    for parent in parse(s).walk():
        if parent.key!='limit':continue
        for exists in parent.all('exists'):
            if not (exists.value or '').startswith(('var:','scope:')):continue
            obj=parent.get(exists.value)
            if obj is None or obj.children is None:continue
            if not any(x.key=='owner' and x.children is None for x in obj.walk()):continue
            edits.extend([(exists.start,exists.end,''),(obj.start,obj.end,'trigger_if = { limit = { exists = '+exists.value+' } '+s[obj.start:obj.end]+' } trigger_else = { always = no }')])
    s=replace_spans(s,edits)
    save(rel,before,s)

rel='common/journal_entries/zzzz_nesnd_india_native.txt';s=read(C/rel)
needle='group = je_group_global_international_situations'
assert s.count(needle)==1
save(rel,s,s.replace(needle,needle+'\n    should_be_involved = { always = no }\n    should_show_when_not_involved = { always = no }'))

# Original railway vehicle tags can outlive a valid market during state changes.
rel='gfx/map/spline_network/military_route_graphics/02_railroad_vehicles.txt'
s=read(G/rel);edits=[]
for tag in parse(s).get('military_train_01').get('tags').children:
    market=tag.get('trigger').get('market');body=s[market.start:market.end]
    edits.append((market.start,market.end,'trigger_if = {\n\t\t\t\t\tlimit = { exists = market }\n\t\t\t\t\t'+body.replace('\n','\n\t')+'\n\t\t\t\t}\n\t\t\t\ttrigger_else = { always = no }'))
assert len(edits)==2
save(rel,s,replace_spans(s,edits))

# Format only the amended condition blocks; preserve ordered AST and other text.
for rel in changes:
    s=read(C/rel);edits=[]
    if '/nesnd_ming_' in rel:
        for n in parse(s).walk():
            if n.key=='limit' and any(x.key=='owner' and x.children is None for x in n.walk()):
                indent=re.match(r'[ \t]*',s[s.rfind('\n',0,n.start)+1:]).group()
                edits.append((n.start,n.end,emit(n).replace('\t','    ').replace('\n','\n'+indent)))
        s=replace_spans(s,edits)
    write(C/rel,re.sub(r'(?m)^[ \t]+$', '',s))
changes={rel:sha(C/rel) for rel in changes}
dump(R/'patch-files.json',changes)
print('Patched',len(changes),'files')
