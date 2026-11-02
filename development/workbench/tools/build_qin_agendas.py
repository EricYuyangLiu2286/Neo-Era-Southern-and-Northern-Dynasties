from qin_persia_build_support import *

tr='''
nesnd_qe1_country = { c:QE1 ?= this is_country_alive = yes }
nesnd_qe1_agenda_eligible = { nesnd_qe1_country = yes num_states >= 4 NOT = { has_variable = nesnd_qe1_agenda_done } }
nesnd_qe1_agenda_live = { nesnd_qe1_agenda_eligible = yes has_journal_entry = nesnd_qe1_agenda_journal }
nesnd_qe1_economy_ready = {
 has_law_or_variant = law_type:law_commercialized_agriculture
 has_law_or_variant = law_type:law_laissez_faire
 has_law_or_variant = law_type:law_wealth_voting
 country_has_building_type_levels = { target = bt:building_tooling_workshop value >= 20 }
 country_has_building_type_levels = { target = bt:building_railway value >= 10 }
}
nesnd_qe1_army_ready = {
 country_has_building_type_levels = { target = bt:building_barracks value >= var:nesnd_qe1_barracks_goal }
 OR = { country_or_subject_owns_entire_state_region = STATE_PUNJAB country_or_subject_owns_entire_state_region = STATE_SINDH country_or_subject_owns_entire_state_region = STATE_GUJARAT }
 trigger_if = { limit = { exists = c:PER } c:PER = { is_subject_of = root } }
 trigger_else = { always = no }
 OR = { country_or_subject_owns_entire_state_region = STATE_ASTRAKHAN country_or_subject_owns_entire_state_region = STATE_ORENBURG country_or_subject_owns_entire_state_region = STATE_TOBOLSK }
}
nesnd_qe1_economic_victory = { has_variable = nesnd_qe1_econ_edge NOT = { has_variable = nesnd_qe1_econ_wait } var:nesnd_qe1_balance <= -50 }
nesnd_qe1_military_victory = { has_variable = nesnd_qe1_army_edge NOT = { has_variable = nesnd_qe1_army_wait } var:nesnd_qe1_balance >= 50 }
nesnd_qe1_court_eligible = { nesnd_qe1_country = yes num_states >= 5 NOT = { has_variable = nesnd_qe1_court_archived } NOR = { has_law_or_variant = law_type:law_universal_suffrage has_law_or_variant = law_type:law_council_republic } }
nesnd_qe1_unity_eligible = { nesnd_qe1_country = yes NOT = { has_variable = nesnd_qe1_dissolved } num_states >= 4 }
nesnd_qe1_recovery_eligible = { nesnd_qe1_country = yes num_states >= 4 NOT = { has_variable = nesnd_qe1_recovery_done } }
nesnd_qe1_recovery_ready = {
 country_or_subject_owns_entire_state_region = STATE_HEXI
 country_or_subject_owns_entire_state_region = STATE_GANSU
 country_or_subject_owns_entire_state_region = STATE_XIAN
 country_or_subject_owns_entire_state_region = STATE_SHAANBEI
}
'''
put('common/scripted_triggers/nesnd_qe1_campaign.txt',tr)

values='''
nesnd_qe1_barracks_total = { value = 0 every_scope_state = { every_scope_building = { limit = { is_building_type = building_barracks } add = level } } }
nesnd_qe1_agenda_economy_delta = { value = 0 if = { limit = { nesnd_qe1_economy_ready = yes } value = -1 } }
nesnd_qe1_agenda_army_delta = { value = 0 if = { limit = { nesnd_qe1_army_ready = yes } value = 2 } }
nesnd_qe1_agenda_ruler_delta = { value = 0 if = { limit = { has_variable = nesnd_qe1_ruler_economic } value = -0.25 } else_if = { limit = { has_variable = nesnd_qe1_ruler_military } value = 0.25 } }
nesnd_qe1_agenda_delta = { value = nesnd_qe1_agenda_economy_delta add = nesnd_qe1_agenda_army_delta add = nesnd_qe1_agenda_ruler_delta }
'''
put('common/script_values/nesnd_qe1_agendas.txt',values)
loc('nesnd_qe1_balance','势力平衡点','Balance of Power')
loc('nesnd_qe1_economy_delta','安国议程','Economic agenda');loc('nesnd_qe1_army_delta','军府议程','Military agenda');loc('nesnd_qe1_ruler_delta','秦王的倾向','The sovereign’s preference')
put('common/scripted_progress_bars/nesnd_qe1_agendas.txt',bar('nesnd_qe1_balance_bar','nesnd_qe1_balance',-50,50,0,[('nesnd_qe1_economy_delta','nesnd_qe1_agenda_economy_delta'),('nesnd_qe1_army_delta','nesnd_qe1_agenda_army_delta'),('nesnd_qe1_ruler_delta','nesnd_qe1_agenda_ruler_delta')]))
for k,z in [('econ','安国之策渐占上风。'),('army','军府正在争取朝廷的支持。'),('neutral','朝臣仍在争论帝国的出路。')]:loc('nesnd_qe1_agenda_status_'+k,z)
J=je('nesnd_qe1_agenda_journal','nesnd_qe1_agenda_eligible = yes','西部帝国的自救','秦军退守伊犁以后，陈秦皇族仍时常东顾玉门，军士和武勋门阀却已不敢轻言东征。帝国需要恢复生产和税收，军府也需要新的兵员与军饷。安国派主张先改旧法，使农工商各得其利；统治派则认为，没有强兵护持，朝廷的法令终究到不了地方。',extra='''
 immediate = { nesnd_qe1_initialize = yes nesnd_qe1_ensure_agenda_children = yes nesnd_qe1_agenda_sync = yes }
 scripted_progress_bar = nesnd_qe1_balance_bar
 complete = { num_states >= 4 OR = { nesnd_qe1_economic_victory = yes nesnd_qe1_military_victory = yes } }
 on_complete = { nesnd_qe1_settle_agenda = yes }
 timeout = 3650
 on_timeout = { nesnd_qe1_agenda_timeout = yes }
 invalid = { NOT = { nesnd_qe1_agenda_eligible = yes } }
 on_invalid = { nesnd_qe1_close_agenda = yes }
 on_monthly_pulse = { effect = { nesnd_qe1_agenda_monthly = yes } }
 on_weekly_pulse = { effect = { nesnd_qe1_watch_endpoints = yes nesnd_qe1_ensure_agenda_children = yes } }
 status_desc = { first_valid = {
  triggered_desc = { trigger = { var:nesnd_qe1_balance < -10 } desc = nesnd_qe1_agenda_status_econ }
  triggered_desc = { trigger = { var:nesnd_qe1_balance > 10 } desc = nesnd_qe1_agenda_status_army }
  desc = nesnd_qe1_agenda_status_neutral
 } }
''')
J+=je('nesnd_qe1_economy_journal','nesnd_qe1_agenda_live = yes','安国之策','安国派要求让田地自由买卖，让商人自行经营，并使有产之家进入朝议。他们相信，西部帝国只有先养民力，才能重新取得同东方争雄的财力。',extra='''
 scripted_button = nesnd_qe1_law_push_button
 scripted_button = nesnd_qe1_economy_push_button
 complete = { always = no }
 invalid = { NOT = { nesnd_qe1_agenda_live = yes } }
 status_desc = { first_valid = { triggered_desc = { trigger = { nesnd_qe1_economy_ready = yes } desc = nesnd_qe1_econ_ready_status } desc = nesnd_qe1_quiet_status } }
''')
J+=je('nesnd_qe1_army_journal','nesnd_qe1_agenda_live = yes','军府之议','军府不愿再为一次仓促的东征耗尽兵力。他们要求先扩充营伍，稳住波斯，向印度与俄国的边地取得新的土地和税源，然后再议玉门以东的天下。',extra='''
 scripted_button = nesnd_qe1_army_petition_button
 complete = { always = no }
 invalid = { NOT = { nesnd_qe1_agenda_live = yes } }
 status_desc = { first_valid = { triggered_desc = { trigger = { nesnd_qe1_army_ready = yes } desc = nesnd_qe1_army_ready_status } desc = nesnd_qe1_quiet_status } }
''')
loc('nesnd_qe1_quiet_status','');loc('nesnd_qe1_econ_ready_status','安国派的三项法案已成，新的工场与铁路正在支持他们的主张。');loc('nesnd_qe1_army_ready_status','新军已有规模，西部边疆的胜利使军府声望日隆。')
put('common/journal_entries/nesnd_qe1_agendas.txt',J)
loc('nesnd_qe1_agenda_gate_tt','此议案半年内不能再次提出。')
buttons=button('nesnd_qe1_law_push_button','责令议法','朝廷责成官员加紧议法，军府与军士的反对不得再使议程久拖不决。','nesnd_qe1_agenda_live = yes','hidden_trigger = { NOT = { has_variable = nesnd_qe1_law_push_cooldown } }', '''
 set_variable = { name = nesnd_qe1_law_push_cooldown months = 6 }
 add_modifier = { name = nesnd_qe1_law_push months = 6 }
''',ai='value = 0 if = { limit = { has_variable = nesnd_qe1_ruler_economic has_law_or_variant = law_type:law_tenant_farmers country_turmoil < 0.25 } add = 20 }')
buttons+=button('nesnd_qe1_economy_push_button','裁军兴业','削减军府的特权与乡村的旧规，把朝廷的力量投入安国之策。','nesnd_qe1_agenda_live = yes','hidden_trigger = { NOT = { has_variable = nesnd_qe1_economy_push_cooldown } }','''
 set_variable = { name = nesnd_qe1_economy_push_cooldown months = 6 }
 add_modifier = { name = nesnd_qe1_economy_push months = 6 }
 change_variable = { name = nesnd_qe1_balance add = -25 }
 nesnd_qe1_watch_endpoints = yes nesnd_qe1_agenda_sync = yes
''',ai='value = 0 if = { limit = { has_variable = nesnd_qe1_ruler_economic var:nesnd_qe1_balance > -40 country_turmoil < 0.25 ig:ig_armed_forces = { approval > -5 } } add = 8 }')
# Actionable native requirements also reveal exactly which military objective remains.
buttons+=button('nesnd_qe1_army_petition_button','呈报边功','军府将新营名册与边地战果送到伊犁，要求朝廷承认统治派的功劳。','nesnd_qe1_agenda_live = yes','nesnd_qe1_army_ready = yes hidden_trigger = { NOT = { has_variable = nesnd_qe1_army_petition_cooldown } }','set_variable = { name = nesnd_qe1_army_petition_cooldown months = 12 } change_variable = { name = nesnd_qe1_balance add = 10 } nesnd_qe1_watch_endpoints = yes nesnd_qe1_agenda_sync = yes',ai='value = 0 if = { limit = { has_variable = nesnd_qe1_ruler_military } add = 20 }')
# The economic programme gets a native-conditions presentation/action independent of
# the risky discretionary buttons. Its small once-yearly endorsement is symmetric.
buttons+=button('nesnd_qe1_economy_petition_button','呈报新政','工场、铁路与新法已见成效，安国派请求朝廷继续推行其议程。','nesnd_qe1_agenda_live = yes','nesnd_qe1_economy_ready = yes hidden_trigger = { NOT = { has_variable = nesnd_qe1_economy_petition_cooldown } }','set_variable = { name = nesnd_qe1_economy_petition_cooldown months = 12 } change_variable = { name = nesnd_qe1_balance add = -10 } nesnd_qe1_watch_endpoints = yes nesnd_qe1_agenda_sync = yes',ai='value = 0 if = { limit = { has_variable = nesnd_qe1_ruler_economic } add = 20 }')
put('common/scripted_buttons/nesnd_qe1_agendas.txt',buttons)
p=C/'common/journal_entries/nesnd_qe1_agendas.txt';write(p,read(p).replace('scripted_button = nesnd_qe1_law_push_button','scripted_button = nesnd_qe1_economy_petition_button\n scripted_button = nesnd_qe1_law_push_button'))
mods='''
nesnd_qe1_law_push = { country_law_enactment_speed_mult = 0.25 interest_group_ig_armed_forces_approval_add = -2 interest_group_ig_landowners_approval_add = -2 }
nesnd_qe1_economy_push = { interest_group_ig_armed_forces_approval_add = -2 interest_group_ig_rural_folk_approval_add = -2 }
nesnd_qe1_angovernment = {
 interest_group_ig_armed_forces_pop_attraction_mult = -0.25 interest_group_ig_petty_bourgeoisie_pop_attraction_mult = -0.25
 interest_group_ig_armed_forces_pol_str_mult = -0.15 interest_group_ig_petty_bourgeoisie_pol_str_mult = -0.15
 interest_group_ig_intelligentsia_pop_attraction_mult = 0.25 interest_group_ig_industrialists_pop_attraction_mult = 0.25
 interest_group_ig_intelligentsia_pol_str_mult = 0.15 interest_group_ig_industrialists_pol_str_mult = 0.15
}
nesnd_qe1_military_government = {
 interest_group_ig_armed_forces_pop_attraction_mult = 0.25 interest_group_ig_petty_bourgeoisie_pop_attraction_mult = 0.25
 interest_group_ig_armed_forces_pol_str_mult = 0.15 interest_group_ig_petty_bourgeoisie_pol_str_mult = 0.15
 interest_group_ig_intelligentsia_pop_attraction_mult = -0.25 interest_group_ig_industrialists_pop_attraction_mult = -0.25
 interest_group_ig_intelligentsia_pol_str_mult = -0.15 interest_group_ig_industrialists_pol_str_mult = -0.15 country_legitimacy_base_add = 10
}
nesnd_qe1_stalled = { }
'''
for k,z in [('law_push','责令议法'),('economy_push','裁军兴业'),('angovernment','安国派执政'),('military_government','统治派执政'),('stalled','久议不决')]:loc('nesnd_qe1_'+k,z)
loc('nesnd_qe1_angovernment_desc','工商业的新秩序使生活改善更易赢得人心。');loc('nesnd_qe1_stalled_desc','朝廷的争执拖延日久，生活困顿更易使人心转向激愤。')
put('common/static_modifiers/nesnd_qe1_agendas.txt',mods)
effects='''
nesnd_qe1_initialize = {
 if = { limit = { nesnd_qe1_country = yes }
  if = { limit = { NOT = { has_variable = nesnd_qe1_campaign_v1 } }
   set_variable = nesnd_qe1_campaign_v1
   set_variable = { name = nesnd_qe1_balance value = 0 }
   set_variable = { name = nesnd_qe1_barracks_goal value = { value = nesnd_qe1_barracks_total add = 25 } }
   set_variable = { name = nesnd_qe1_unity value = 70 }
   set_variable = { name = nesnd_qe1_uprising value = 0 }
   set_variable = { name = nesnd_qe1_war_months value = 0 }
   set_variable = nesnd_qe1_ruler_economic
   if = { limit = { exists = ruler } ruler = { nesnd_qe1_assign_ruler = yes } }
  }
 }
}
nesnd_qe1_assign_ruler = {
 if = { limit = { exists = owner owner = { nesnd_qe1_country = yes } }
  if = { limit = { NOT = { has_variable = nesnd_qe1_ruler_registered } }
   set_variable = nesnd_qe1_ruler_registered
   if = { limit = { has_template = QE1_chen_wuxing }
    set_variable = nesnd_qe1_person_economic
   } else = { random_list = { 60 = { set_variable = nesnd_qe1_person_economic } 40 = { set_variable = nesnd_qe1_person_military } } }
  }
  owner = {
   remove_variable = nesnd_qe1_ruler_economic remove_variable = nesnd_qe1_ruler_military
   if = { limit = { prev = { has_variable = nesnd_qe1_person_economic } } set_variable = nesnd_qe1_ruler_economic }
   else = { set_variable = nesnd_qe1_ruler_military }
  }
 }
}
nesnd_qe1_ensure_agenda_children = {
 if = { limit = { nesnd_qe1_agenda_live = yes }
  if = { limit = { NOT = { has_journal_entry = nesnd_qe1_economy_journal } } add_journal_entry = { type = nesnd_qe1_economy_journal } }
  if = { limit = { NOT = { has_journal_entry = nesnd_qe1_army_journal } } add_journal_entry = { type = nesnd_qe1_army_journal } }
 }
}
nesnd_qe1_agenda_sync = {
 clamp_variable = { name = nesnd_qe1_balance min = -50 max = 50 }
 if = { limit = { has_journal_entry = nesnd_qe1_agenda_journal } je:nesnd_qe1_agenda_journal = { set_bar_progress = { name = nesnd_qe1_balance_bar value = root.var:nesnd_qe1_balance } } }
}
nesnd_qe1_watch_endpoints = {
 if = { limit = { nesnd_qe1_agenda_live = yes }
  clamp_variable = { name = nesnd_qe1_balance min = -50 max = 50 }
  if = { limit = { var:nesnd_qe1_balance <= -50 }
   if = { limit = { NOT = { has_variable = nesnd_qe1_econ_edge } } set_variable = nesnd_qe1_econ_edge set_variable = { name = nesnd_qe1_econ_wait days = 29 } }
  } else = { remove_variable = nesnd_qe1_econ_edge remove_variable = nesnd_qe1_econ_wait }
  if = { limit = { var:nesnd_qe1_balance >= 50 }
   if = { limit = { NOT = { has_variable = nesnd_qe1_army_edge } } set_variable = nesnd_qe1_army_edge set_variable = { name = nesnd_qe1_army_wait days = 29 } }
  } else = { remove_variable = nesnd_qe1_army_edge remove_variable = nesnd_qe1_army_wait }
 }
}
nesnd_qe1_agenda_monthly = {
 if = { limit = { nesnd_qe1_agenda_live = yes }
  change_variable = { name = nesnd_qe1_balance add = nesnd_qe1_agenda_delta }
  nesnd_qe1_watch_endpoints = yes nesnd_qe1_agenda_sync = yes
  nesnd_qe1_check_civil_conflict = yes
 }
}
nesnd_qe1_close_agenda = {
 set_variable = nesnd_qe1_agenda_done
 remove_variable = nesnd_qe1_econ_edge remove_variable = nesnd_qe1_econ_wait
 remove_variable = nesnd_qe1_army_edge remove_variable = nesnd_qe1_army_wait
 remove_modifier = nesnd_qe1_law_push remove_modifier = nesnd_qe1_economy_push
}
nesnd_qe1_settle_agenda = {
 if = { limit = { NOT = { has_variable = nesnd_qe1_agenda_done } }
  if = { limit = { var:nesnd_qe1_balance <= -50 }
   add_modifier = { name = nesnd_qe1_angovernment years = 10 }
   set_variable = nesnd_qe1_economic_winner
   trigger_event = { id = nesnd_qe1.1 popup = yes }
  } else = {
   add_modifier = { name = nesnd_qe1_military_government years = 10 }
   set_variable = nesnd_qe1_military_winner
   trigger_event = { id = nesnd_qe1.2 popup = yes }
  }
  nesnd_qe1_close_agenda = yes
 }
}
nesnd_qe1_agenda_timeout = {
 if = { limit = { NOT = { has_variable = nesnd_qe1_agenda_done } }
  nesnd_qe1_close_agenda = yes
  add_modifier = { name = nesnd_qe1_stalled years = 10 }
  trigger_event = { id = nesnd_qe1.3 popup = yes }
 }
}
'''
put('common/scripted_effects/nesnd_qe1_agendas.txt',effects)
ev='namespace = nesnd_qe1\n'
for i,title,desc,opt in [(1,'安国之策','朝廷终于决定把恢复生产与改造旧法置于军府的要求之前。新任官员将凭借工场、学校和商人的支持施展其主张；军士与武勋门阀则退到了朝议的后列。','先养民力。'),(2,'军府得势','统治派取得了朝廷的信任。军令与征收将更紧密地连在一起，新的官员也更多出自营伍。伊犁的朝议暂时归于一致，代价则由被排除在权力之外的人承担。','整饬军政。'),(3,'十年空议','朝议延续了十年，田地、军饷与官职的争论仍没有结果。地方听过太多振兴帝国的许诺，越来越少的人相信下一道诏令能改变自己的处境。','朝廷失去了许多时间。')]:
 loc(f'nesnd_qe1.{i}.a',opt);ev+=event(f'nesnd_qe1.{i}',title,desc,f'option = {{ name = nesnd_qe1.{i}.a default_option = yes }}')
put('events/nesnd_qe1_agendas.txt',ev)
append_history('common/history/countries/QE1 - Western Qin.txt','nesnd_qe1_initialize')
flush_loc()
print('Qin agenda source generated; companion lifecycle/identity/court effects pending.')
