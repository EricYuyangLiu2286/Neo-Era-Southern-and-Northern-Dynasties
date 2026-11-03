from feedback_context import *
report=read(R/'cne-confidence-research.md');section=report[report.index('## 六'):] if '## 六' in report else report[report.index('### 6.1'):]
blocks=re.findall(r'```text\n(.*?)```',section,re.S)
definitions={}
for block in blocks:
    for n in parse(block).children:
        if n.key:definitions[n.key]=block[n.start:n.end]
rel='common/scripted_effects/nesnd_cne_republic.txt';s=read(C/rel)
assert s.count('ideology = ideology_republican }')==1
s=s.replace('ideology = ideology_republican }','ideology = ideology_republican_leader }')
old=' add_journal_entry = { type = nesnd_cne_republic_journal }'
assert s.count(old)==1;s=s.replace(old,' if = { limit = { NOT = { has_journal_entry = nesnd_cne_republic_journal } } add_journal_entry = { type = nesnd_cne_republic_journal } }')
n=parse(s).get('nesnd_cne_spawn_republicans');part=s[n.start:n.end]
old='  if = { limit = { c:NRP ?= { has_variable = nesnd_cne_republican_challenger } }'
assert part.count(old)==1
part=part.replace(old,'  if = { limit = { exists = c:NRP }\n   if = { limit = { c:NRP = { has_variable = nesnd_cne_republican_challenger } }')
end='   trigger_event = { id = nesnd_cne_confidence.1 popup = yes }\n  }'
assert part.count(end)==1;part=part.replace(end,'   trigger_event = { id = nesnd_cne_confidence.1 popup = yes }\n   }\n  }')
s=s[:n.start]+part+s[n.end:];write(C/rel,s)
for key in ['nesnd_cne_start_republic_war','nesnd_cne_republic_watch','nesnd_cne_republic_defeat']:
    assert key in definitions,key
    replace_node(rel,key,definitions[key])
write(C/rel,read(C/rel)+'\n'+definitions['nesnd_cne_republic_note_actual_war']+'\n')
rel='common/journal_entries/nesnd_cne_republic.txt';s=read(C/rel);n=parse(s).get('nesnd_cne_republic_journal').get('fail')
assert 'fail' in definitions;write(C/rel,s[:n.start]+definitions['fail']+s[n.end:])
dump(R/'cne-republic-fix.json',{'definite_bugs':['invalid character ideology','duplicate explicit add_journal_entry','play_created used as proof of actual war','play_created preventing retry without a live play or war','nullable NRP check could pass without successful creation'],'preserved':['legacy rose flag','existing save history','1000/500/0 thresholds','regional split definitions','army size','mutual annexation goals'],'new_markers':['nesnd_cne_republic_war_confirmed','nesnd_cne_republic_settled'],'old_save_war_cause':'Actual NRP creation and 1841.5.18 reabsorption proven; whether real defeat or premature cleanup is not recoverable from this save.','engine_verified':False})
print('Republic creation, war observation, retry and settlement guards fixed; old uprising history preserved.')
