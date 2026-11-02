from qin_persia_build_support import *
mapping=json.loads(read(R/'native-identity-map.json'));part=mapping['exclusive_breakup_partition_proposal']
core=['STATE_ILI','STATE_DZUNGARIA','STATE_JETISY'];part['QE1']=core
for tag in list(part):
 if tag!='QE1':part[tag]=[r for r in part[tag] if r not in core]
assert len([r for regs in part.values() for r in regs])==len(set(r for regs in part.values() for r in regs))==36
put('common/country_definitions/nesnd_qe1_rebels.txt','''
QRC = { color = { 156 105 49 } country_type = recognized tier = kingdom cultures = { ce_xiyu ce_xibei } capital = STATE_UZBEKIA }
QFR = { color = { 94 128 96 } country_type = recognized tier = kingdom cultures = { ce_xiyu ce_xibei } capital = STATE_TIANSHAN }
''')
for k,z in [('QRC','秦国讨逆军'),('QRC_ADJ','讨逆军'),('QFR','西部诸省联邦'),('QFR_ADJ','西部联邦'),('nesnd_qe1_rebel_army','讨逆军'),('nesnd_qe1_frontier_army','边地新军'),('nesnd_qe1_commander_first','兆毅'),('nesnd_qe1_commander_last','梁'),('dp_nesnd_qe1_civil','秦国权争'),('dp_nesnd_qe1_frontier','西域反秦战争')]:loc(k,z)
put('common/diplomatic_plays/nesnd_qe1_conflicts.txt','''
dp_nesnd_qe1_civil = { war_goal = annex_country mirror_war_goal = yes texture = "gfx/interface/icons/war_goals/annex_country.dds" possible = { always = no } }
dp_nesnd_qe1_frontier = { war_goal = annex_country mirror_war_goal = yes texture = "gfx/interface/icons/war_goals/annex_country.dds" possible = { always = no } }
''')
tr='''
nesnd_qe1_core_region = { OR = { '''+' '.join('state_region = s:'+x for x in core)+''' } }
nesnd_qe1_civil_danger = {
 nesnd_qe1_agenda_live = yes num_states >= 5
 NOT = { has_variable = nesnd_qe1_civil_raised }
 NOT = { exists = c:QRC }
 trigger_if = { limit = { has_variable = nesnd_qe1_balance }
  OR = {
   AND = { var:nesnd_qe1_balance <= -35 ig:ig_armed_forces = { clout >= 0.25 approval <= -5 } }
   AND = { var:nesnd_qe1_balance >= 35 ig:ig_intelligentsia = { clout >= 0.2 approval <= -5 } }
  }
 }
 trigger_else = { always = no }
}
nesnd_qe1_has_frontier_play = {
 trigger_if = { limit = { exists = c:QE1 } any_diplomatic_play = { initiator = root target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_frontier } }
 trigger_else = { always = no }
}
'''
put('common/scripted_triggers/nesnd_qe1_fracture.txt',tr)
clean=' '.join('remove_modifier = '+x for x in ['nesnd_qe1_law_push','nesnd_qe1_economy_push','nesnd_qe1_angovernment','nesnd_qe1_military_government','nesnd_qe1_stalled','nesnd_qe1_patronage_crown','nesnd_qe1_patronage_literati','nesnd_qe1_patronage_army','nesnd_qe1_recovered_military','nesnd_qe1_recovered_civil'])
effects='''
nesnd_qe1_check_civil_conflict = {
 if = { limit = { nesnd_qe1_civil_danger = yes any_scope_state = { is_capital = no } }
  set_variable = nesnd_qe1_civil_raised
  ordered_scope_state = { limit = { is_capital = no } order_by = state_population position = 0 check_range_bounds = no save_scope_as = nesnd_qe1_rebel_seed }
  if = { limit = { exists = scope:nesnd_qe1_rebel_seed }
   create_country = { tag = QRC origin = root state = scope:nesnd_qe1_rebel_seed on_created = {
    set_variable = nesnd_qe1_civil_challenger
    activate_law = law_type:law_presidential_republic
    activate_law = law_type:law_oligarchy
    set_ruling_interest_groups = { ig_armed_forces ig_landowners }
    nesnd_qe1_setup_civil_challenger = yes
   } }
   if = { limit = { exists = c:QRC }
    trigger_event = { id = nesnd_qe1_fracture.1 popup = yes }
    c:QRC = { trigger_event = { id = nesnd_qe1_fracture.90 days = 1 popup = no } }
   }
  }
 }
}
nesnd_qe1_setup_civil_challenger = {
 '''+clean+'''
 save_scope_as = nesnd_qe1_new_challenger
 create_military_formation = { name = nesnd_qe1_rebel_army type = army hq_region = scope:nesnd_qe1_new_challenger.capital.region
  combat_unit = { type = unit_type:combat_unit_type_line_infantry state_region = scope:nesnd_qe1_new_challenger.capital.state_region count = 16 }
  combat_unit = { type = unit_type:combat_unit_type_cannon_artillery state_region = scope:nesnd_qe1_new_challenger.capital.state_region count = 4 }
 }
 create_character = { first_name = nesnd_qe1_commander_first last_name = nesnd_qe1_commander_last is_general = yes interest_group = ig_armed_forces ideology = ideology_jingoist }
}
nesnd_qe1_start_civil_war = {
 if = { limit = { c:QRC ?= this exists = c:QE1 has_variable = nesnd_qe1_civil_challenger NOT = { has_variable = nesnd_qe1_civil_war_started } }
  if = { limit = { NOT = { has_war_with = c:QE1 } }
   end_truce = c:QE1
   create_diplomatic_play = { type = dp_nesnd_qe1_civil target_country = c:QE1 war = yes annex_as_civil_war = no }
  }
  if = { limit = { OR = { has_war_with = c:QE1 any_diplomatic_play = { initiator = root target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_civil } } } set_variable = nesnd_qe1_civil_war_started }
 }
}
nesnd_qe1_prepare_frontier_army = {
 '''+clean+'''
 save_scope_as = nesnd_qe1_new_frontier
 create_military_formation = { name = nesnd_qe1_frontier_army type = army hq_region = scope:nesnd_qe1_new_frontier.capital.region
  combat_unit = { type = unit_type:combat_unit_type_line_infantry state_region = scope:nesnd_qe1_new_frontier.capital.state_region count = 6 }
  combat_unit = { type = unit_type:combat_unit_type_cannon_artillery state_region = scope:nesnd_qe1_new_frontier.capital.state_region count = 2 }
 }
}
nesnd_qe1_start_frontier_war = {
 if = { limit = { has_variable = nesnd_qe1_breakaway_attacker exists = c:QE1 NOT = { has_variable = nesnd_qe1_frontier_war_started } }
  if = { limit = { is_subject = no NOT = { has_war_with = c:QE1 } }
   end_truce = c:QE1
   create_diplomatic_play = { type = dp_nesnd_qe1_frontier target_country = c:QE1 war = yes annex_as_civil_war = no }
  }
  if = { limit = { OR = { has_war_with = c:QE1 nesnd_qe1_has_frontier_play = yes } } set_variable = nesnd_qe1_frontier_war_started }
 }
}
'''
cultures={'XIN':'uighur','UZB':'uzbek','BUK':'uzbek','KHI':'uzbek','TRC':'turkmen','KYR':'kirgiz','TJI':'tajik','KAZ':'kazak','AFG':'pashtun','KAL':'baluchi','PER':'persian','TIB':'tibetan','KAS':'kashmiri','MGL':'mongol','TUV':'tuvan','QFR':'ce_xiyu'}
attackers={'XIN','UZB','BUK','KHI','TRC','KYR','TJI','KAZ','QFR'}
for tag,regions in part.items():
 if tag=='QE1' or not regions:continue
 conditions='OR = { '+' '.join('state_region = s:'+r for r in regions)+' }'
 effects+=f'''nesnd_qe1_release_{tag.lower()} = {{
 if = {{ limit = {{ any_scope_state = {{ {conditions} }} }}
  if = {{ limit = {{ NOT = {{ exists = c:{tag} }} }}
   random_scope_state = {{ limit = {{ {conditions} }} save_scope_as = nesnd_qe1_secession_seed }}
   create_country = {{ tag = {tag} origin = root state = scope:nesnd_qe1_secession_seed on_created = {{
    set_variable = nesnd_qe1_newly_restored
    add_primary_culture = cu:{cultures[tag]}
    remove_primary_culture = cu:ce_xiyu remove_primary_culture = cu:ce_xibei remove_primary_culture = cu:ce_laoqin
    nesnd_qe1_prepare_frontier_army = yes
   }} }}
  }}
  if = {{ limit = {{ exists = c:{tag} }}
   c:{tag} = {{ if = {{ limit = {{ is_subject_of = root }} make_independent = yes }} }}
   every_scope_state = {{ limit = {{ {conditions} }} set_state_owner = c:{tag} }}
   '''+(f'c:{tag} = {{ if = {{ limit = {{ is_subject = no }} set_variable = nesnd_qe1_breakaway_attacker trigger_event = {{ id = nesnd_qe1_fracture.91 days = 2 popup = no }} }} }}' if tag in attackers else '')+'''
  }
 }
}
'''
# Anything conquered after the baseline goes to a separate federation, not a guessed
# vanilla owner and not an arbitrary existing neighbour. Core provinces stay Qin.
effects+='''nesnd_qe1_release_other_provinces = {
 if = { limit = { any_scope_state = { NOT = { nesnd_qe1_core_region = yes } } }
  if = { limit = { NOT = { exists = c:QFR } }
   random_scope_state = { limit = { NOT = { nesnd_qe1_core_region = yes } } save_scope_as = nesnd_qe1_secession_seed }
   create_country = { tag = QFR origin = root state = scope:nesnd_qe1_secession_seed on_created = { nesnd_qe1_prepare_frontier_army = yes } }
  }
  if = { limit = { exists = c:QFR }
   c:QFR = { if = { limit = { is_subject_of = root } } make_independent = yes }
   every_scope_state = { limit = { NOT = { nesnd_qe1_core_region = yes } } set_state_owner = c:QFR }
   c:QFR = { if = { limit = { is_subject = no } set_variable = nesnd_qe1_breakaway_attacker trigger_event = { id = nesnd_qe1_fracture.91 days = 2 popup = no } } }
  }
 }
}
nesnd_qe1_breakup = {
 if = { limit = { nesnd_qe1_country = yes NOT = { has_variable = nesnd_qe1_dissolved } }
  set_variable = nesnd_qe1_dissolved
  nesnd_qe1_close_agenda = yes nesnd_qe1_archive_court = yes
'''
for tag in part:
 if tag!='QE1' and part[tag]:effects+='nesnd_qe1_release_'+tag.lower()+' = yes\n'
effects+='''
  nesnd_qe1_release_other_provinces = yes
  if = { limit = { exists = c:QE1 }
   c:QE1 = { if = { limit = { exists = s:STATE_ILI.region_state:QE1 } set_capital = STATE_ILI } trigger_event = { id = nesnd_qe1_fracture.2 popup = yes } }
  }
 }
}
'''
# Correct the compact conditional before writing; no unconditional release of foreign subjects.
effects=effects.replace('if = { limit = { is_subject_of = root } } make_independent = yes','if = { limit = { is_subject_of = root } make_independent = yes }')
put('common/scripted_effects/nesnd_qe1_fracture.txt',effects)
loc('nesnd_qe1_fracture.1.a','向朝廷效忠的军队，听候调遣。');loc('nesnd_qe1_fracture.2.a','帝国只剩下最后的疆土。')
ev='namespace = nesnd_qe1_fracture\n'
ev+=event('nesnd_qe1_fracture.1','朝议之外','被排除在朝议之外的官员与军人已经集结成军。他们自称讨逆，宣告伊犁已被一派私党控制，要求以武力重新决定帝国的政务。朝廷内部的争执终于走出了官署。','option = { name = nesnd_qe1_fracture.1.a default_option = yes }')
ev+=event('nesnd_qe1_fracture.2','西部帝国的崩解','地方官署已经改换旗帜。布哈拉、花剌子模与草原的旧名重新进入军令和税册，各地不再承认伊犁对人丁、土地与征赋的支配。朝廷保住的疆土之外，昔日帝国正在变成彼此争夺的新国家。','option = { name = nesnd_qe1_fracture.2.a default_option = yes }')
ev+='''nesnd_qe1_fracture.90 = { type = country_event hidden = yes trigger = { c:QRC ?= this exists = c:QE1 } immediate = { nesnd_qe1_start_civil_war = yes } }
nesnd_qe1_fracture.91 = { type = country_event hidden = yes trigger = { has_variable = nesnd_qe1_breakaway_attacker exists = c:QE1 } immediate = { nesnd_qe1_start_frontier_war = yes } }
'''
put('events/nesnd_qe1_fracture.txt',ev)
dump(R/'breakup-partition.json',{'initial_regions':part,'later_conquests':'QFR except explicit core','core':core,'new_country_army':8,'civil_challenger_army':20,'navy_created':0,'attackers':sorted(attackers),'if_core_lost_to_third_party':'do not steal; Qin may be eliminated','game_launched':False})
flush_loc();print('Civil conflict and once-only territorial breakup generated.')
