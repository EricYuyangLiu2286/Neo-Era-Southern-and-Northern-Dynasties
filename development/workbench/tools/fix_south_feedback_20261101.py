"""Apply the user's southern-crisis corrections in an isolated, backed-up candidate."""
from pathlib import Path
import sys,json,shutil,hashlib,textwrap
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties';B=W/'backups/pre-change-south-politics-feedback-20261101T175047Z/mod'
C=W/'exports/south-feedback-20261101-a';R=W/'reports/south-feedback-20261101'
S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
sys.path.insert(0,str(S/'scripts'));from pdx import parse
def man(root):return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
assert man(M)==man(B);assert not C.exists();shutil.copytree(M,C);R.mkdir(exist_ok=False)
shutil.copytree(S,R/'skill-before')
for name in ['error.log','debug.log']:
 p=W.parent/'logs'/name
 if p.exists():shutil.copy2(p,R/('before-'+name))
def read(rel):return (C/rel).read_text('utf-8-sig')
def write(rel,s):
 p=C/rel;old=p.read_bytes() if p.exists() else b'\xef\xbb\xbf';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in old else '\n').encode('utf-8'))
def node(s,path):
 n=parse(s)
 for k in path:n=n.get(k);assert n is not None,path
 return n
def edit(rel,path,fn):
 s=read(rel);n=node(s,path);out=s[:n.start]+fn(s[n.start:n.end],n)+s[n.end:];parse(out);write(rel,out)
def replace(rel,key,s):edit(rel,[key],lambda old,n:textwrap.dedent(s).strip())
def add(rel,path,body):edit(rel,path,lambda s,n:s[:s.rfind('}')]+body+'\n'+s[s.rfind('}'):])
def wrap_effect(rel,path,limit):
 edit(rel,path,lambda s,n:s[:s.index('{')+1]+'\n if = { limit = { '+limit+' }\n'+s[s.index('{')+1:s.rfind('}')]+'\n }\n}')

# One allegiance policy shared by initialization, AI, previews and negotiation.
t='common/scripted_triggers/nesnd_succession_board.txt'
write(t,read(t)+'''
nesnd_board_fixed_ming_allegiance = {
    c:HNA ?= this
    NOT = { has_global_variable = usm_civilwar_occured }
    NOT = { has_global_variable = nesnd_south_settled }
}
nesnd_board_can_choose_local_stance = {
    nesnd_board_can_choose = yes
    NOT = { c:USM ?= this }
    NOT = { has_variable = nesnd_ming_court }
}
''')
add(t,['nesnd_board_can_choose'],'    NOT = { nesnd_board_fixed_ming_allegiance = yes }')
e='common/scripted_effects/nesnd_succession_board.txt'
replace(e,'nesnd_board_initialize_country','''
nesnd_board_initialize_country = {
    set_variable = nesnd_board_registered
    if = { limit = { NOT = { has_variable = nesnd_south_stance } }
        set_variable = { name = nesnd_south_stance value = 0 }
    }
    nesnd_board_enforce_allegiance = yes
    nesnd_board_refresh_country = yes
}''')
write(e,read(e)+'''
# Refresh also repairs an earlier save's incompatible stance, once per real change.
nesnd_board_enforce_allegiance = {
    if = { limit = { nesnd_board_fixed_ming_allegiance = yes }
        if = { limit = { has_variable = nesnd_south_accord_active nesnd_south_accord_side_value = 2 }
            nesnd_south_withdraw_accord = yes
        }
        set_variable = { name = nesnd_south_stance value = 1 }
    }
    else_if = { limit = {
        OR = { c:USM ?= this has_variable = nesnd_ming_court }
        OR = { nesnd_board_stance_value = 3 nesnd_board_stance_value = 4 }
    }
        set_variable = { name = nesnd_south_stance value = 1 }
    }
}
''')
v='common/script_values/nesnd_succession_board.txt'
replace(v,'nesnd_board_stance_value','''
nesnd_board_stance_value = {
    if = { limit = { nesnd_board_fixed_ming_allegiance = yes } value = 1 }
    else_if = { limit = { has_variable = nesnd_south_stance } value = var:nesnd_south_stance }
    else = { value = 0 }
}''')
a='common/scripted_effects/nesnd_south_political_ai.txt'
edit(a,['nesnd_south_ai_initial_stance'],lambda s,n:s.replace('if = { limit = { c:USM ?= this }','if = { limit = { nesnd_board_fixed_ming_allegiance = yes } set_variable = { name = nesnd_south_stance value = 1 } }\n    else_if = { limit = { c:USM ?= this }',1))
wrap_effect(a,['nesnd_south_ai_review'],'NOT = { nesnd_board_fixed_ming_allegiance = yes }')
b='common/scripted_buttons/nesnd_succession_board.txt'
for stance in ['ming','wu','neutral','autonomy']:
 key='nesnd_board_choose_'+stance
 add(b,[key,'visible'],'    NOT = { nesnd_board_fixed_ming_allegiance = yes }')
 if stance in ['neutral','autonomy']:
  add(b,[key,'visible'],'    NOT = { c:USM ?= this }\n    NOT = { has_variable = nesnd_ming_court }')
  edit(b,[key,'possible'],lambda s,n:s.replace('nesnd_board_can_choose = yes','nesnd_board_can_choose_local_stance = yes'))
 limit=('nesnd_board_can_choose_local_stance' if stance in ['neutral','autonomy'] else 'nesnd_board_can_choose')+' = yes'
 wrap_effect(b,[key,'effect'],limit)
t='common/scripted_triggers/nesnd_south_politics.txt'
add(t,['nesnd_south_can_receive_accord'],'''    trigger_if = { limit = { nesnd_board_fixed_ming_allegiance = yes }
        trigger_if = { limit = { exists = c:USM } c:USM = { nesnd_board_stance_value = 1 } }
        trigger_else = { always = no }
    }''')
add(t,['nesnd_south_accord_reply_valid'],'''    trigger_if = { limit = { nesnd_board_fixed_ming_allegiance = yes }
        nesnd_south_pending_side_value = 1
    }''')
e='events/usm_civilwar_events.txt'
s=read(e);event=node(s,['usm_civilwar.1']);option=next(n for n in event.all('option') if n.scalar('name')=='usm_civilwar.1.3')
pos=option.end-1;s=s[:pos]+'\n trigger = { NOT = { c:HNA ?= this } }\n'+s[pos:];write(e,s)
# The loyalist answer remains the only valid HNA answer, including timeout/default handling.
# For other countries retain the original acceptance default through a mutually exclusive duplicate.
s=read(e);event=node(s,['usm_civilwar.1']);loyal=event.all('option')[0];text=s[loyal.start:loyal.end]
hna=text[:text.rfind('}')]+ '\n trigger = { c:HNA ?= this }\n default_option = yes\n'+text[text.rfind('}'):]
other=text[:text.rfind('}')]+ '\n trigger = { NOT = { c:HNA ?= this } }\n'+text[text.rfind('}'):]
s=s[:loyal.start]+hna+'\n'+other+s[loyal.end:];write(e,s)
j='common/journal_entries/nesnd_succession_board.txt'
add(j,['nesnd_south_succession_board'],'    should_be_pinned_by_default_involved = yes')

# Monthly accrual and an explicit crisis window, with the case resolved before accession.
write('common/scripted_triggers/nesnd_south_timing.txt','''
nesnd_chen_case_concluded = {
    NOT = { has_variable = nesnd_chen_case_pending_death }
    OR = {
        has_variable = nesnd_assassination_resolved
        NOT = { nesnd_chen_present = yes }
    }
}
nesnd_south_accession_window_open = {
    OR = {
        NOT = { any_scope_character = { has_template = USM_zheng_qin is_character_alive = yes } }
        game_date >= 1839.1.1
    }
}
''')
write('common/scripted_effects/nesnd_south_timing.txt','''
# Production JE callbacks only. No game simulator or QA entry point.
nesnd_south_enforce_crisis_deadline = {
    if = { limit = {
        c:USM ?= this has_journal_entry = ce_usm_conflicts_within
        NOT = { has_variable = tag_WUU_var }
        NOT = { has_global_variable = nesnd_south_settled }
        game_date >= 1839.1.1 nesnd_chen_case_concluded = yes
    }
        nesnd_south_initialize = yes
        clamp_variable = { name = usm_conflicts_within_tracker min = 100 max = 100 }
    }
}
nesnd_south_crisis_month = {
    nesnd_south_initialize = yes
    change_variable = { name = usm_conflicts_within_tracker add = nesnd_south_base_monthly_pressure }
    clamp_variable = { name = usm_conflicts_within_tracker min = 0 max = 100 }
    if = { limit = { game_date >= 1838.1.1 nesnd_chen_case_possible = yes }
        trigger_event = { id = nesnd_chen.2 days = 0 }
    }
    nesnd_south_enforce_crisis_deadline = yes
    nesnd_refresh_south_display = yes
}
''')
t='common/scripted_triggers/nesnd_chen_security.txt'
replace(t,'nesnd_chen_case_possible','''
nesnd_chen_case_possible = {
    nesnd_chen_security_active = yes
    game_date >= 1837.7.1
    OR = { nesnd_south_pressure_value > 24 game_date >= 1838.1.1 }
}''')
v='common/script_values/nesnd_south_progress.txt'
write(v,read(v)+'''\nnesnd_south_base_monthly_pressure = {
    if = { limit = { has_modifier = nesnd_federal_compact } value = 2.5 }
    else = { value = 3 }
}
''')
edit(v,['nesnd_south_monthly_pressure_value'],lambda s,n:s.replace('if = { limit = { has_modifier = nesnd_federal_compact } add = 0.4 }\n  else = { add = 1 }','add = nesnd_south_base_monthly_pressure'))
j='common/journal_entries/ce_usm_the_last_days_of_ming.txt'
edit(j,['ce_usm_conflicts_within','on_monthly_pulse'],lambda s,n:'''on_monthly_pulse = {
    effect = { nesnd_south_crisis_month = yes }
    random_events = { 100 = 0 30 = nesnd_chen.2 }
}''')
s=read(j);complete=node(s,['ce_usm_conflicts_within','complete']);q=next(n for n in complete.all('custom_tooltip') if n.scalar('text')=='nesnd_south_qin_departed_tt')
s=s[:q.start]+'''custom_tooltip = {
    text = nesnd_south_qin_departed_tt
    nesnd_south_accession_window_open = yes
}
custom_tooltip = { text = nesnd_chen_case_concluded_tt nesnd_chen_case_concluded = yes }'''+s[q.end:];write(j,s)
edit(j,['ce_usm_conflicts_within','on_weekly_pulse'],lambda s,n:s.replace('nesnd_refresh_south_display = yes','nesnd_south_enforce_crisis_deadline = yes nesnd_refresh_south_display = yes'))
edit(j,['ce_usm_conflicts_within','status_desc'],lambda s,n:s.replace('any_scope_character = { has_template = USM_zheng_qin is_character_alive = yes }','game_date < 1839.1.1 any_scope_character = { has_template = USM_zheng_qin is_character_alive = yes }'))
add('common/scripted_buttons/nesnd_crisis_buttons.txt',['nesnd_early_accession','possible'],'    custom_tooltip = { text = nesnd_chen_case_concluded_tt nesnd_chen_case_concluded = yes }')
e='events/flavorUSM_ce.txt'
s=read(e);hidden=node(s,['flavorUSM.1','immediate','hidden_effect']);reset=next(n for n in hidden.all('set_variable') if n.scalar('name')=='usm_conflicts_within_tracker');s=s[:reset.start]+s[reset.end:];write(e,s)
# The existing death helper owns the +25 and clears its once-only flag. Do not add it twice.
e='common/scripted_effects/nesnd_chen_security.txt'
for key in ['nesnd_chen_after_death','nesnd_chen_case_wounded','nesnd_chen_case_escape']:
 add(e,[key],'    nesnd_refresh_south_display = yes')
e='common/scripted_effects/nesnd_presentation_effects.txt'
# Saved country guarded in the previous fix; je: also supports global entries (vanilla peoples_springtime.8).
add(e,['nesnd_refresh_south_display','if'],'''        je:nesnd_south_succession_board ?= {
            set_bar_progress = { name = nesnd_board_pressure_bar value = scope:nesnd_south_display_country.nesnd_south_pressure_value }
        }''')

# Localized status per country; move exact thresholds into the existing rules tooltip.
j='common/journal_entries/nesnd_supply_journals.txt'
for key in ['nesnd_supply_preparations','nesnd_supply_hus_preparations']:
 s=read(j);status=node(s,[key,'status_desc','first_valid']);generic=next(n for n in status.all('triggered_desc') if n.scalar('desc')=='nesnd_supply_status_jobs')
 entries='\n'.join('triggered_desc = { trigger = { c:'+tag+' ?= this NOT = { nesnd_supply_jobs_ready = yes } } desc = nesnd_supply_status_jobs_'+tag.lower()+' }' for tag in ['HNA','SIH','GNG','HUS'])+'\n'
 s=s[:generic.start]+entries+s[generic.start:];write(j,s)

# Format only modified PDX definitions, preserving quoted keys, duplicate entries and comments.
exec((W/'tools/format_button_guard_spans_20261101.py').read_text('utf-8'))
# Preserve the existing two-widget layout verbatim; only the involved-country pin is new.
rel='common/journal_entries/nesnd_succession_board.txt'
original=(B/rel).read_text('utf-8-sig');end=original.rfind('}')
write(rel,original[:end]+'    should_be_pinned_by_default_involved = yes\n'+original[end:])
dump={'base':str(B),'candidate':str(C),'before':man(B),'after':man(C),'game_launched':False}
(R/'logic-changes.json').write_text(json.dumps(dump,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'candidate':str(C),'logic_files':len([p for p,h in dump['after'].items() if dump['before'].get(p)!=h])},ensure_ascii=False))
