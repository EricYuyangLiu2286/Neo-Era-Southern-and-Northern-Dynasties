from qin_persia_build_support import *
import re
# Use the author's actual geographic groups, including Korea's custom split and
# the entire existing Northeast Asia strategic region.
p=C/'common/strategic_regions/east_asia_strategic_regions.txt';s=read(p);tree=parse(s)
regions=set()
for key in ['region_north_china','region_south_china','region_northeast_asia']:
 n=tree.get(key).get('states');regions.update(re.findall(r'\bSTATE_\w+',s[n.start:n.end]))
t=parse(read(C/'common/scripted_triggers/ce_scripted_triggers.txt')).get('is_modern_china_state')
regions.update(a.value[2:] for a in t.walk() if a.key=='state_region' and a.value and a.value.startswith('s:'))
regions-={'STATE_FORMOSA','STATE_HAINAN'}
put('common/scripted_effects/nesnd_qe1_recovery.txt','nesnd_qe1_recovery_claims = {\n'+''.join(f's:{r} = {{ add_claim = root }}\n' for r in sorted(regions))+'}\n')
dump(R/'recovery-claim-regions.json',{'regions':sorted(regions),'sources':['common/strategic_regions/east_asia_strategic_regions.txt:region_north_china/region_south_china/region_northeast_asia','common/scripted_triggers/ce_scripted_triggers.txt:is_modern_china_state'],'excluded_mainland_islands':['STATE_FORMOSA','STATE_HAINAN']})

p=C/'common/scripted_effects/nesnd_qe1_agendas.txt';s=read(p)
n=parse(s).get('nesnd_qe1_agenda_timeout');replacement='''nesnd_qe1_agenda_timeout = {
 if = { limit = { NOT = { has_variable = nesnd_qe1_agenda_done } }
  if = { limit = { num_states < 4 } nesnd_qe1_close_agenda = yes }
  else_if = { limit = { OR = { nesnd_qe1_economic_victory = yes nesnd_qe1_military_victory = yes } } nesnd_qe1_settle_agenda = yes }
  else = {
   nesnd_qe1_close_agenda = yes
   add_modifier = { name = nesnd_qe1_stalled years = 10 }
   nesnd_qe1_start_sol_observation = yes
   trigger_event = { id = nesnd_qe1.3 popup = yes }
  }
 }
}
''';s=s[:n.start]+replacement+s[n.end:]
s+='''
nesnd_qe1_start_agenda_clock = {
 if = { limit = { NOT = { has_variable = nesnd_qe1_agenda_started } NOT = { has_variable = nesnd_qe1_agenda_done } }
  set_variable = nesnd_qe1_agenda_started set_variable = { name = nesnd_qe1_agenda_clock years = 10 }
 }
}
''';write(p,s)
p=C/'common/journal_entries/nesnd_qe1_agendas.txt';s=read(p).replace('nesnd_qe1_initialize = yes nesnd_qe1_ensure_agenda_children','nesnd_qe1_initialize = yes nesnd_qe1_start_agenda_clock = yes nesnd_qe1_ensure_agenda_children')
s=s.replace('fail = { has_variable = nesnd_qe1_agenda_started NOT = { has_variable = nesnd_qe1_agenda_clock } }','fail = { num_states >= 4 has_variable = nesnd_qe1_agenda_started NOT = { has_variable = nesnd_qe1_agenda_clock } NOR = { nesnd_qe1_economic_victory = yes nesnd_qe1_military_victory = yes } }');write(p,s)

# The disaffected party, not always the army, forms the civil challenger.
p=C/'common/scripted_effects/nesnd_qe1_fracture.txt';s=read(p)
old='''activate_law = law_type:law_presidential_republic
    activate_law = law_type:law_oligarchy
    set_ruling_interest_groups = { ig_armed_forces ig_landowners }'''
new='''if = { limit = { root = { var:nesnd_qe1_balance <= -35 } }
     activate_law = law_type:law_monarchy activate_law = law_type:law_autocracy
     set_ruling_interest_groups = { ig_armed_forces ig_landowners }
     set_variable = nesnd_qe1_rebel_military
    } else = {
     activate_law = law_type:law_presidential_republic activate_law = law_type:law_wealth_voting
     set_ruling_interest_groups = { ig_intelligentsia ig_industrialists }
     set_variable = nesnd_qe1_rebel_economic
    }'''
assert old in s;s=s.replace(old,new)
write(p,s)
p=C/'common/scripted_triggers/nesnd_qe1_fracture.txt';s=read(p).replace('any_diplomatic_play = { initiator = root target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_frontier }','any_diplomatic_play = { target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_frontier OR = { initiator = root any_scope_play_involved = { this = root } } }');write(p,s)
loc('nesnd_qe1_military_budget_button_desc','筹备军需，支持军府扩充营伍。')
flush_loc();print('Author geography, terminal priority, durable first-entry clock and actual opposing civil faction finalized.')
