from journal_war_context import *
from pdx import replace_spans
import re

def edit(rel,key,fn):
    p=C/rel;s=read(p);n=parse(s).get(key);assert n,key
    write(p,s[:n.start]+fn(s[n.start:n.end])+s[n.end:])

# Native JE goal_add_value is relative to the metric on entry; use absolute counters.
for je,bar,score,maximum,flag in [
 ('nesnd_wu_eastern_question','nesnd_eastern_readiness_bar','nesnd_japan_preparation_score',3,'nesnd_eastern_absolute_v2'),
 ('nesnd_japan_reunification','nesnd_japan_unification_bar','nesnd_japan_unity_score',7,'nesnd_unification_absolute_v2')]:
    def fix(s):
        s=s.replace('progressbar = yes','scripted_progress_bar = '+bar)
        s=re.sub(r'    current_value = \{ value = \w+ \}\n    goal_add_value = \{ value = \d+ \}\n','',s)
        if je=='nesnd_wu_eastern_question':
            s=s.replace('immediate = { set_variable = nesnd_japan_dossier_entered }','immediate = { set_variable = nesnd_japan_dossier_entered set_variable = '+flag+' }')
            s=s.replace('complete = { has_global_variable = nesnd_japan_dossier_closed }','complete = { custom_tooltip = { text = nesnd_eastern_question_resolved_tt has_global_variable = nesnd_japan_dossier_closed } }')
            s=s.replace('invalid = { NOT = { has_variable = tag_WUU_var } }','invalid = { OR = { NOT = { has_variable = tag_WUU_var } NOT = { has_variable = '+flag+' } } }')
            s=s.replace('on_invalid = { set_global_variable = nesnd_japan_dossier_closed }','on_invalid = { if = { limit = { NOT = { has_variable = tag_WUU_var } } set_global_variable = nesnd_japan_dossier_closed } else = { remove_variable = nesnd_japan_dossier_entered } }')
        else:
            s=s.replace('immediate = { set_variable = nesnd_japan_unity_entered }','immediate = { set_variable = nesnd_japan_unity_entered set_variable = '+flag+' }')
            s=s.replace('invalid = { NOT = { nesnd_jp_country = yes } }','invalid = { OR = { NOT = { nesnd_jp_country = yes } NOT = { has_variable = '+flag+' } } }')
        return s
    edit('common/journal_entries/nesnd_japan.txt',je,fix)
    bp=C/'common/scripted_progress_bars/nesnd_japan_absolute_counters.txt'
    old=read(bp) if bp.exists() else ''
    write(bp,old+f'''{bar} = {{
    name = {bar}_name desc = {bar}_name
    min_value = 0 max_value = {maximum} start_value = 0 default_green = yes
    weekly_progress = {{ add = {{ desc = {bar}_change value = owner.{bar}_delta }} }}
}}
''')
    sv=C/'common/script_values/nesnd_japan_absolute_counters.txt'
    old=read(sv) if sv.exists() else ''
    write(sv,old+f'''{bar}_delta = {{
    value = 0
    if = {{ limit = {{ has_journal_entry = {je} }}
        value = {score}
        subtract = "je:{je}.scripted_bar_progress({bar})"
    }}
}}
''')
# These predicates are also called through a JE-owned script value; use the actual caller.
p=C/'common/scripted_triggers/nesnd_japan.txt';s=read(p)
assert s.count('<= root.army_power_projection')==1 and s.count('<= root.naval_power_projection')==1
write(p,s.replace('<= root.army_power_projection','<= prev.army_power_projection').replace('<= root.naval_power_projection','<= prev.naval_power_projection'))

# A chosen programme may pause; it must not lose its journal object on switching focus.
for kind in ['schools','industry']:
    rel='common/journal_entries/nesnd_india_core.txt'
    def fix(s):
        s=s.replace('is_shown_when_inactive = { nesnd_india_'+kind+'_available = yes } possible = { nesnd_india_'+kind+'_available = yes }','is_shown_when_inactive = { nesnd_india_'+kind+'_visible = yes } possible = { nesnd_india_'+kind+'_visible = yes }')
        s=s.replace('invalid = { NOT = { nesnd_india_'+kind+'_available = yes } }','invalid = { NOT = { nesnd_india_'+kind+'_visible = yes } }')
        s=s.replace('    weight = 700','    should_be_pinned_by_default_uninvolved_or_context = yes\n    status_desc = { first_valid = { triggered_desc = { trigger = { nesnd_india_'+kind+'_available = yes } desc = nesnd_india_'+kind+'_working } desc = nesnd_india_'+kind+'_paused } }\n    weight = 700')
        return s
    edit(rel,'nesnd_india_'+kind,fix)
    p=C/'common/scripted_triggers/nesnd_india_core.txt'
    write(p,read(p)+f'\nnesnd_india_{kind}_visible = {{ nesnd_india_reform_live = yes NOT = {{ has_variable = nesnd_india_{kind}_done }} OR = {{ nesnd_india_priority_value = 1 nesnd_india_priority_value = 2 }} }}\n')
p=C/'common/scripted_effects/nesnd_india_core.txt';s=read(p)
for k in ['schools','industry']:
    old=f'nesnd_india_{k}_available = yes NOT = {{ has_journal_entry = nesnd_india_{k} }}'
    assert s.count(old)==1;s=s.replace(old,f'nesnd_india_{k}_visible = yes NOT = {{ has_journal_entry = nesnd_india_{k} }}')
write(p,s)
def parent(s):
    s=s.replace('custom_tooltip = { text = nesnd_india_reform_finished_tt has_variable = nesnd_india_schools_done has_variable = nesnd_india_industry_done }','custom_tooltip = { text = nesnd_india_schools_completed_tt has_variable = nesnd_india_schools_done } custom_tooltip = { text = nesnd_india_industry_completed_tt has_variable = nesnd_india_industry_done }')
    s=s.replace('status_desc = { desc = nesnd_india_reform_status }','status_desc = { first_valid = { triggered_desc = { trigger = { nesnd_india_priority_value = 1 } desc = nesnd_india_reform_schools_status } triggered_desc = { trigger = { nesnd_india_priority_value = 2 } desc = nesnd_india_reform_industry_status } desc = nesnd_india_reform_waiting_status } }')
    return s
edit('common/journal_entries/nesnd_india_core.txt','nesnd_india_reform',parent)
p=C/'common/scripted_triggers/nesnd_india_core.txt';s=read(p)
for good in ['coal','iron','tools','steel']:
    old=f'capital.market = {{ mg:{good} = {{ market_goods_pricier <= 0.25 NOT = {{ country_has_local_shortage = root }} }} }}'
    new=f'capital = {{ trigger_if = {{ limit = {{ exists = market }} market = {{ mg:{good} = {{ market_goods_pricier <= 0.25 NOT = {{ country_has_local_shortage = prev.prev.owner }} }} }} }} trigger_else = {{ always = no }} }}'
    assert s.count(old)==1;s=s.replace(old,new)
write(p,s)

# Preserve vanilla abolishing-monarchy behaviour everywhere except a never-monarch HUS.
src=G/'common/journal_entries/00_abolish_monarchy.txt';s=read(src)
s=s.replace('je_abolish_monarchy = {','REPLACE:je_abolish_monarchy = {',1)
s=s.replace('complete = {\n','complete = {\n        nesnd_native_abolish_monarchy_eligible = yes\n',1)
s=s.replace('limit = {\n','limit = {\n                    nesnd_native_abolish_monarchy_eligible = yes\n',1)
n=parse(s).get('REPLACE:je_abolish_monarchy');inv=n.get('invalid');old=s[inv.start:inv.end]
body=old[old.index('{')+1:old.rindex('}')]
s=s[:inv.start]+'invalid = { OR = { NOT = { nesnd_native_abolish_monarchy_eligible = yes } '+body+' } }'+s[inv.end:]
write(C/'common/journal_entries/zzzz_nesnd_hus_native_monarchy.txt',s)
write(C/'common/scripted_triggers/nesnd_hus_monarchy_history.txt','''nesnd_native_abolish_monarchy_eligible = {
    OR = { NOT = { c:HUS ?= this } has_variable = nesnd_hus_monarchy_seen country_has_monarchy_law = yes }
}
''')
write(C/'common/on_actions/nesnd_hus_monarchy_history.txt','''# on_law_activated is law scope; enactment-start and monthly are country scope.
on_law_activated = { on_actions = { nesnd_hus_record_monarchy_law } }
nesnd_hus_record_monarchy_law = { effect = {
    owner ?= { if = { limit = { c:HUS ?= this has_game_started = yes country_has_monarchy_law = yes } set_variable = nesnd_hus_monarchy_seen } }
} }
on_law_enactment_started = { on_actions = { nesnd_hus_record_monarchy_country } }
on_monthly_pulse_country = { on_actions = { nesnd_hus_record_monarchy_country } }
nesnd_hus_record_monarchy_country = { effect = {
    if = { limit = { c:HUS ?= this has_game_started = yes country_has_monarchy_law = yes } set_variable = nesnd_hus_monarchy_seen }
} }
''')
dump(R/'simple-native-sources.json',{'abolish_monarchy':{'path':str(src),'sha256':sha(src)},'absolute_bar':'GAME/common/script_values/ip4_je_values.txt:17; journal_entries.md:392'})
print('Japan absolute counters, visible paused India programmes and HUS native eligibility written')
