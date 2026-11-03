from cne_native_context import *
from pdx import replace_spans
import re

rel='common/script_values/nesnd_cne_confidence.txt';s=read(C/rel)
needle='add = nesnd_cne_conf_base add = nesnd_cne_conf_land'
assert s.count(needle)==1
s=s.replace(needle,'add = nesnd_cne_conf_base add = nesnd_cne_conf_delay add = nesnd_cne_conf_land')
s+='''
# Each completed five-year period adds 25 to the annual confidence cost.
# The existing monthly age counter keeps its value in old active saves and during respite.
nesnd_cne_conf_delay = {
    value = 0
    if = {
        limit = { nesnd_cne_programs_live = yes }
        if = {
            limit = { has_variable = nesnd_land_months }
            add = {
                value = var:nesnd_land_months
                min = 0
                divide = 60
                floor = yes
                multiply = -25
            }
        }
    }
}
'''
write(C/rel,s)
rel='common/scripted_progress_bars/nesnd_cne_confidence.txt';s=read(C/rel)
needle='add = { desc = nesnd_cne_conf_base_desc value = nesnd_cne_conf_base }'
assert s.count(needle)==1
write(C/rel,s.replace(needle,needle+'\n  add = { desc = nesnd_cne_conf_delay_desc value = nesnd_cne_conf_delay }'))

# Preserve all other native definitions and namespace declarations in order.
sources={}
for rel,ids in EVENTS.items():
    assert not (B/rel).exists(),('Review pre-existing override',rel)
    source=G/rel;s=read(source);tree=parse(s);edits=[];sources[rel]=sha(source)
    for key in ids:
        n=tree.get(key);assert n and n.scalar('type')=='country_event'
        stub=f'''{key} = {{
    type = country_event
    hidden = yes
    trigger = {{ always = no }}
    cancellation_trigger = {{ always = yes }}
    immediate = {{ }}
}}'''
        edits.append((n.start,n.end,stub))
    p=C/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,p)
    write(p,replace_spans(s,edits))

write(C/'common/scripted_buttons/zzzz_nesnd_native_error_bans.txt','''# Disable the native agitator request; CE Poland keeps its own buttons/events.
REPLACE:christ_of_nations_button = {
    name = christ_of_nations_button
    desc = christ_of_nations_button_desc
    visible = { always = no }
    possible = { always = no }
    cooldown = { days = normal_modifier_time }
    ai_chance = { value = 0 }
    effect = { }
}
''')
write(C/'common/journal_entries/zzzz_nesnd_native_error_bans.txt','''# No split, territory transfer, or new ZAN creation; existing countries are untouched.
REPLACE:je_splitting_oman = {
    icon = "gfx/interface/icons/event_icons/event_portrait.dds"
    group = je_group_historical_content
    is_shown_in_lobby = { always = no }
    is_shown_when_inactive = { always = no }
    possible = { always = no }
    complete = { always = no }
    fail = { always = no }
    invalid = { always = yes }
}
''')

# Only the two malformed reparations weights are disabled, not the ideology.
rel='common/ideologies/01_character_ideologies.txt';source=G/rel
assert not (B/rel).exists();s=read(source);n=parse(s).get('ideology_integralist');edits=[]
for key in ['interest_group_leader_weight','non_interest_group_leader_weight']:
    nodes=[x for x in n.get(key).all('if') if x.get('limit') and x.get('limit').get('any_diplomatically_relevant_country')]
    assert len(nodes)==1,(key,len(nodes))
    lim=nodes[0].get('limit');edits.append((lim.start,lim.end,'limit = { always = no }'))
p=C/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,p);write(p,replace_spans(s,edits));sources[rel]=sha(source)

# Three conditions actually logged an intensity evaluation without random context.
rel='common/naval_battle_conditions/00_naval_battle_conditions.txt';source=G/rel
assert not (B/rel).exists();s=read(source);tree=parse(s);edits=[]
for key in ['naval_condition_cyclone','naval_condition_rough_waters','naval_condition_tropical_storm']:
    n=tree.get(key);assert n
    stub=f'''{key} = {{
    icon = {n.get('icon').value}
    possible = {{ always = no }}
    weight = {{ value = 0 }}
    period = {{ value = 0 }}
    intensity = {{ value = 0 }}
}}'''
    edits.append((n.start,n.end,stub))
p=C/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,p);write(p,replace_spans(s,edits));sources[rel]=sha(source)

for lang in ['simp_chinese','english']:
    values={'nesnd_cne_conf_delay_desc':'改革久拖未成' if lang=='simp_chinese' else 'Reform left unfinished'}
    if lang=='simp_chinese':
        values.update({
            'BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER':'进攻方：$BATTLE_SHIPS_BREAKDOWN_HEADER$',
            'BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER':'防御方：$BATTLE_SHIPS_BREAKDOWN_HEADER$',
            'BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER_START_OF_BATTLE':"[ConcatIfNeitherEmpty( NAVAL_BATTLE.GetAttackerNumWantedShipsDesc, '\\n' )]战斗开始时有$BATTLE_SHIPS_BREAKDOWN_HEADER$进攻",
            'BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER_START_OF_BATTLE':"[ConcatIfNeitherEmpty( NAVAL_BATTLE.GetDefenderNumWantedShipsDesc, '\\n' )]战斗开始时有$BATTLE_SHIPS_BREAKDOWN_HEADER$防御"})
    else:
        values.update({'BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER':'Attacking: $BATTLE_SHIPS_BREAKDOWN_HEADER$','BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER':'Defending: $BATTLE_SHIPS_BREAKDOWN_HEADER$'})
    write(C/f'localization/{lang}/replace/zzzzzzzzzzzzzzz_nesnd_native_errors_l_{lang}.yml','l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in values.items()))
for rel in sources:
    clean=re.sub(r'[\t ]+(?=\n|$)','',read(C/rel))
    clean=re.sub(r'(?m)^[ \t]+',lambda m:re.sub(r' +\t','\t',m.group()),clean)
    write(C/rel,clean)
dump(R/'native-source-hashes.json',sources)
baseline=man(B)
dump(R/'patch-files.json',{r:h for r,h in man(C).items() if baseline.get(r)!=h})
print('Built CNE confidence escalation and native error bans')
