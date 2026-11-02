from qin_persia_build_support import *
types={}
for root in [G,C]:
 for p in (root/'common/pop_types').glob('*.txt'):
  for n in parse(read(p)).children:types[n.key]=n
poptypes=sorted(types)
sv='''
nesnd_qe1_pop_sol_divisor = { value = standard_of_living subtract = 15 max = 0 min = 15 divide = 15 multiply = 9 add = 1 }
nesnd_qe1_pop_sol_impact = { value = define:NPops|DEFAULT_SOL_CHANGE_IMPACT_FACTOR if = { limit = { is_pop_type = peasants } value = 0.01 } divide = nesnd_qe1_pop_sol_divisor }
'''
fx='nesnd_qe1_measure_sol_bonus = {\n if = { limit = { nesnd_qe1_country = yes OR = { has_modifier = nesnd_qe1_angovernment has_modifier = nesnd_qe1_stalled } }\n set_variable = nesnd_qe1_sol_bonus_tracking\n every_scope_state = { set_variable = nesnd_qe1_sol_tracked\n'
for pt in poptypes:
 sv+=f'''nesnd_qe1_sol_{pt}_n = {{ value = 0 every_scope_pop = {{ limit = {{ is_pop_type = {pt} }} add = total_size }} }}
nesnd_qe1_sol_{pt}_s = {{ value = 0 every_scope_pop = {{ limit = {{ is_pop_type = {pt} }} add = {{ value = total_size multiply = standard_of_living }} }} }}
nesnd_qe1_sol_{pt}_f = {{ value = 0 every_scope_pop = {{ limit = {{ is_pop_type = {pt} }} add = {{ value = total_size multiply = nesnd_qe1_pop_sol_impact }} }} }}
'''
 prev='nesnd_qe1_sol_previous_'+pt
 fx+=f'''
 set_variable = {{ name = nesnd_qe1_sol_n value = nesnd_qe1_sol_{pt}_n }}
 if = {{ limit = {{ var:nesnd_qe1_sol_n > 0 }}
  set_variable = {{ name = nesnd_qe1_sol_s value = {{ value = nesnd_qe1_sol_{pt}_s divide = var:nesnd_qe1_sol_n }} }}
  set_variable = {{ name = nesnd_qe1_sol_f value = {{ value = nesnd_qe1_sol_{pt}_f divide = var:nesnd_qe1_sol_n }} }}
  if = {{ limit = {{ has_variable = {prev} }}
   if = {{ limit = {{ owner = {{ has_modifier = nesnd_qe1_angovernment }} var:nesnd_qe1_sol_s > var:{prev} }}
    add_loyalists_in_state = {{ pop_type = pop_type:{pt} value = {{ value = var:nesnd_qe1_sol_s subtract = var:{prev} multiply = var:nesnd_qe1_sol_f multiply = 0.15 max = 0 min = 0.05 }} }}
   }}
   if = {{ limit = {{ owner = {{ has_modifier = nesnd_qe1_stalled }} var:nesnd_qe1_sol_s < var:{prev} }}
    add_radicals_in_state = {{ pop_type = pop_type:{pt} value = {{ value = var:{prev} subtract = var:nesnd_qe1_sol_s multiply = var:nesnd_qe1_sol_f multiply = 0.10 max = 0 min = 0.05 }} }}
   }}
  }}
  set_variable = {{ name = {prev} value = var:nesnd_qe1_sol_s }}
 }} else = {{ remove_variable = {prev} }}
'''
fx+='''
 remove_variable = nesnd_qe1_sol_n remove_variable = nesnd_qe1_sol_s remove_variable = nesnd_qe1_sol_f
 }
 } else_if = { limit = { has_variable = nesnd_qe1_sol_bonus_tracking }
  every_scope_state = { nesnd_qe1_clear_sol_state = yes }
  remove_variable = nesnd_qe1_sol_bonus_tracking
 }
}
nesnd_qe1_clear_sol_state = {
'''+''.join(f'remove_variable = nesnd_qe1_sol_previous_{pt}\n' for pt in poptypes)+'''
 remove_variable = nesnd_qe1_sol_tracked
}
nesnd_qe1_start_sol_observation = {
 every_scope_state = { nesnd_qe1_clear_sol_state = yes }
 nesnd_qe1_measure_sol_bonus = yes
}
'''
put('common/script_values/nesnd_qe1_sol_bonus.txt',sv);put('common/scripted_effects/nesnd_qe1_sol_bonus.txt',fx)
# Establish the first sample at grant time, then only pay monthly net changes.
p=C/'common/scripted_effects/nesnd_qe1_agendas.txt';s=read(p).replace('add_modifier = { name = nesnd_qe1_angovernment years = 10 }','add_modifier = { name = nesnd_qe1_angovernment years = 10 }\n nesnd_qe1_start_sol_observation = yes').replace('add_modifier = { name = nesnd_qe1_stalled years = 10 }','add_modifier = { name = nesnd_qe1_stalled years = 10 }\n nesnd_qe1_start_sol_observation = yes');write(p,s)

effects='''
nesnd_qe1_bootstrap = {
 if = { limit = { nesnd_qe1_country = yes NOT = { has_variable = nesnd_qe1_bootstrap_busy } }
  set_variable = nesnd_qe1_bootstrap_busy
  nesnd_qe1_initialize = yes
  if = { limit = { exists = ruler } ruler = { nesnd_qe1_assign_ruler = yes } }
  if = { limit = { has_variable = nesnd_qe1_agenda_started NOT = { has_variable = nesnd_qe1_agenda_clock } NOT = { has_variable = nesnd_qe1_agenda_done } }
   nesnd_qe1_agenda_timeout = yes
  }
  if = { limit = { num_states < 4 NOT = { has_variable = nesnd_qe1_agenda_done } } nesnd_qe1_close_agenda = yes }
  if = { limit = { nesnd_qe1_agenda_eligible = yes }
   if = { limit = { NOT = { has_variable = nesnd_qe1_agenda_started } }
    set_variable = nesnd_qe1_agenda_started set_variable = { name = nesnd_qe1_agenda_clock years = 10 }
   }
   if = { limit = { NOT = { has_journal_entry = nesnd_qe1_agenda_journal } } add_journal_entry = { type = nesnd_qe1_agenda_journal } }
   nesnd_qe1_ensure_agenda_children = yes
  }
  if = { limit = { nesnd_qe1_unity_eligible = yes NOT = { has_journal_entry = nesnd_qe1_unity_journal } } add_journal_entry = { type = nesnd_qe1_unity_journal } }
  if = { limit = { nesnd_qe1_unity_live = yes has_variable = nesnd_qe1_uprising_awakened NOT = { has_journal_entry = nesnd_qe1_uprising_journal } } add_journal_entry = { type = nesnd_qe1_uprising_journal } }
  if = { limit = { nesnd_qe1_court_eligible = yes NOT = { has_journal_entry = nesnd_qe1_court_journal } } add_journal_entry = { type = nesnd_qe1_court_journal } }
  if = { limit = { NOT = { nesnd_qe1_court_eligible = yes } NOT = { has_variable = nesnd_qe1_court_archived } } nesnd_qe1_archive_court = yes }
  if = { limit = { nesnd_qe1_recovery_eligible = yes NOT = { has_journal_entry = nesnd_qe1_recovery_journal } } add_journal_entry = { type = nesnd_qe1_recovery_journal } }
  remove_variable = nesnd_qe1_bootstrap_busy
 }
}
nesnd_per_bootstrap = {
 if = { limit = { nesnd_per_country = yes NOT = { has_variable = nesnd_per_bootstrap_busy } }
  set_variable = nesnd_per_bootstrap_busy
  nesnd_per_initialize = yes
  if = { limit = { nesnd_per_future_eligible = yes NOT = { has_journal_entry = nesnd_per_future_journal } } add_journal_entry = { type = nesnd_per_future_journal } }
  if = { limit = { NOT = { has_journal_entry = nesnd_per_civil_journal } } add_journal_entry = { type = nesnd_per_civil_journal } }
  if = { limit = { NOT = { has_journal_entry = nesnd_per_economy_journal } } add_journal_entry = { type = nesnd_per_economy_journal } }
  nesnd_per_ensure_frontier = yes
  remove_variable = nesnd_per_bootstrap_busy
 }
}
'''
put('common/scripted_effects/nesnd_qin_persia_lifecycle.txt',effects)
put('common/on_actions/nesnd_qin_persia.txt','''
on_monthly_pulse_country = { on_actions = { nesnd_qin_persia_monthly_maintenance } }
nesnd_qin_persia_monthly_maintenance = {
 trigger = { OR = { c:QE1 ?= this c:PER ?= this has_variable = nesnd_qe1_civil_challenger has_variable = nesnd_qe1_breakaway_attacker } }
 effect = {
  if = { limit = { nesnd_qe1_country = yes } nesnd_qe1_bootstrap = yes nesnd_qe1_measure_sol_bonus = yes every_scope_state = { nesnd_qe1_clear_orphan_cohort = yes } }
  if = { limit = { nesnd_per_country = yes } nesnd_per_bootstrap = yes }
  if = { limit = { c:QRC ?= this has_variable = nesnd_qe1_civil_challenger } nesnd_qe1_start_civil_war = yes }
  if = { limit = { has_variable = nesnd_qe1_breakaway_attacker } nesnd_qe1_start_frontier_war = yes }
 }
}
on_ruler_selected = { on_actions = { nesnd_qe1_new_ruler } }
nesnd_qe1_new_ruler = { trigger = { exists = owner owner = { nesnd_qe1_country = yes } } effect = { nesnd_qe1_assign_ruler = yes } }
on_state_owner_change = { on_actions = { nesnd_qe1_state_changed } }
nesnd_qe1_state_changed = {
 effect = {
  if = { limit = { has_variable = nesnd_qe1_sol_tracked } nesnd_qe1_clear_sol_state = yes }
  nesnd_qe1_clear_orphan_cohort = yes
  if = { limit = { owner = { nesnd_qe1_unity_live = yes } } owner = { set_variable = { name = nesnd_qe1_new_land_prestige months = 12 } } }
 }
}
on_wargoal_enforced = { on_actions = { nesnd_qe1_border_victory } }
nesnd_qe1_border_victory = {
 trigger = { nesnd_qe1_unity_live = yes NOT = { has_variable = nesnd_qe1_victory_cooldown } }
 effect = { set_variable = { name = nesnd_qe1_victory_cooldown years = 1 } set_variable = { name = nesnd_qe1_victory_prestige months = 24 } }
}
''')
# Starting histories enter through a nonrecursive orchestrator; each JE immediate
# invokes only the idempotent initializer, not its own addition.
for rel,tag in [('common/history/countries/QE1 - Western Qin.txt','qe1'),('common/history/countries/per - persia.txt','per')]:
 p=C/rel;s=read(p).replace('nesnd_'+tag+'_initialize = yes','nesnd_'+tag+'_bootstrap = yes');write(p,s)
# Only the short agenda and court have the user-specified territory cutoffs.
p=C/'common/scripted_triggers/nesnd_qe1_campaign.txt';s=read(p)
s=s.replace('NOT = { has_variable = nesnd_qe1_dissolved } num_states >= 4','NOT = { has_variable = nesnd_qe1_dissolved }')
s=s.replace('nesnd_qe1_country = yes num_states >= 4 NOT = { has_variable = nesnd_qe1_recovery_done }','nesnd_qe1_country = yes NOT = { has_variable = nesnd_qe1_recovery_done }')
write(p,s)
# An absent king in a republic cannot continue influencing the balance.
p=C/'common/scripted_effects/nesnd_qe1_agendas.txt';s=read(p);n=parse(s).get('nesnd_qe1_assign_ruler');outer=n.get('if');li=outer.get('limit');body=s[li.end:outer.end-1]
replacement='\nif = { limit = { owner = { country_has_monarchy_law = yes } }\n'+body+'\n} else = { owner = { remove_variable = nesnd_qe1_ruler_economic remove_variable = nesnd_qe1_ruler_military } }\n'
s=s[:li.end]+replacement+s[outer.end-1:];write(p,s)
# Expose timeout through the durable clock as well as the native JE timer.
p=C/'common/journal_entries/nesnd_qe1_agendas.txt';s=read(p).replace('timeout = 3650','fail = { has_variable = nesnd_qe1_agenda_started NOT = { has_variable = nesnd_qe1_agenda_clock } }\n on_fail = { nesnd_qe1_agenda_timeout = yes }\n timeout = 3650');write(p,s)
dump(R/'sol-approximation.json',{'population_types':poptypes,'cohort':'state x profession','native_base':.03,'peasants_base':.01,'high_sol_scale':[15,30,9],'extra_loyal_multiplier':.15,'extra_radical_multiplier':.10,'monthly_fraction_cap':.05,'directional':True,'exact_engine_replica':False,'sources':'native-political-contracts.md','game_launched':False})
flush_loc();print('Explicit startup/recovery lifecycle, ruler hooks and directional SoL sampling generated.')
