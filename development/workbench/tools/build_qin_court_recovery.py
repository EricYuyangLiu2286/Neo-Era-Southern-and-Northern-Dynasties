from qin_persia_build_support import *
import re
tr='''
nesnd_qe1_court_live = { nesnd_qe1_court_eligible = yes has_journal_entry = nesnd_qe1_court_journal }
nesnd_qe1_no_patronage = { NOR = { has_variable = nesnd_qe1_patron_crown has_variable = nesnd_qe1_patron_literati has_variable = nesnd_qe1_patron_army } }
'''
for side in ['crown','literati','army']:
 for label,threshold in [('strong',40),('peak',60)]:
  tr+=f'nesnd_qe1_{side}_{label} = {{ trigger_if = {{ limit = {{ has_variable = nesnd_qe1_power_{side} }} var:nesnd_qe1_power_{side} >= {threshold} }} trigger_else = {{ always = no }} }}\n'
put('common/scripted_triggers/nesnd_qe1_court.txt',tr)
sv='''
nesnd_qe1_crown_raw = {
 value = 15
 if = { limit = { has_law_or_variant = law_type:law_monarchy } add = 25 }
 if = { limit = { has_law_or_variant = law_type:law_autocracy } add = 25 }
 if = { limit = { has_law_or_variant = law_type:law_technocracy } add = 15 }
 if = { limit = { has_law_or_variant = law_type:law_appointed_bureaucrats } add = 10 }
 if = { limit = { bureaucracy >= 0 government_legitimacy >= 75 } add = 20 }
 if = { limit = { OR = { has_variable = nesnd_qe1_patron_literati has_variable = nesnd_qe1_patron_army } } subtract = 10 }
 min = 5
}
nesnd_qe1_literati_raw = {
 value = 15
 add = { value = ig:ig_intelligentsia.clout add = ig:ig_industrialists.clout multiply = 100 }
 if = { limit = { has_law_or_variant = law_type:law_elected_bureaucrats } add = 20 }
 if = { limit = { has_law_or_variant = law_type:law_census_voting } add = 20 }
 if = { limit = { has_law_or_variant = law_type:law_wealth_voting } add = 15 }
 if = { limit = { has_law_or_variant = law_type:law_presidential_republic } add = 20 }
 if = { limit = { institution_investment_level = { institution = institution_schools value >= 3 } } add = 20 }
 if = { limit = { bureaucracy < 0 } add = { value = nesnd_qe1_significant_cultures multiply = 2 max = 20 } }
 if = { limit = { OR = { has_variable = nesnd_qe1_patron_crown has_variable = nesnd_qe1_patron_army } } subtract = 10 }
 min = 5
}
nesnd_qe1_army_raw = {
 value = 15
 add = { value = army_size divide = 4 max = 60 }
 add = { value = ig:ig_armed_forces.clout multiply = 60 }
 if = { limit = { has_law_or_variant = law_type:law_professional_army } add = 10 }
 if = { limit = { has_law_or_variant = law_type:law_militarized_police } add = 15 }
 if = { limit = { has_variable = nesnd_qe1_military_winner } add = 15 }
 if = { limit = { is_at_war = yes } add = 10 }
 if = { limit = { OR = { has_variable = nesnd_qe1_patron_crown has_variable = nesnd_qe1_patron_literati } } subtract = 10 }
 min = 5
}
'''
put('common/script_values/nesnd_qe1_court.txt',sv)
effects='''
nesnd_qe1_compute_court = {
 if = { limit = { nesnd_qe1_court_live = yes }
  set_variable = { name = nesnd_qe1_power_total value = { value = nesnd_qe1_crown_raw add = nesnd_qe1_literati_raw add = nesnd_qe1_army_raw } }
  set_variable = { name = nesnd_qe1_power_crown value = { value = nesnd_qe1_crown_raw divide = var:nesnd_qe1_power_total multiply = 100 } }
  set_variable = { name = nesnd_qe1_power_literati value = { value = nesnd_qe1_literati_raw divide = var:nesnd_qe1_power_total multiply = 100 } }
  set_variable = { name = nesnd_qe1_power_army value = { value = nesnd_qe1_army_raw divide = var:nesnd_qe1_power_total multiply = 100 } }
  nesnd_qe1_prune_patronage = yes
  je:nesnd_qe1_court_journal = {
   set_bar_progress = { name = nesnd_qe1_crown_bar value = root.var:nesnd_qe1_power_crown }
   set_bar_progress = { name = nesnd_qe1_literati_bar value = root.var:nesnd_qe1_power_literati }
   set_bar_progress = { name = nesnd_qe1_army_bar value = root.var:nesnd_qe1_power_army }
  }
 }
}
nesnd_qe1_clear_patronage = {
 remove_variable = nesnd_qe1_patron_crown remove_variable = nesnd_qe1_patron_literati remove_variable = nesnd_qe1_patron_army
 remove_modifier = nesnd_qe1_patronage_crown remove_modifier = nesnd_qe1_patronage_literati remove_modifier = nesnd_qe1_patronage_army
}
nesnd_qe1_prune_patronage = {
'''
for side in ['crown','literati','army']:
 effects+=f'''if = {{ limit = {{ has_variable = nesnd_qe1_patron_{side} has_variable = nesnd_qe1_power_{side} }}
 if = {{ limit = {{ var:nesnd_qe1_power_{side} < 35 }} remove_variable = nesnd_qe1_patron_{side} remove_modifier = nesnd_qe1_patronage_{side} }}
}}\n'''
effects+='''}
nesnd_qe1_archive_court = { set_variable = nesnd_qe1_court_archived nesnd_qe1_clear_patronage = yes }
'''
put('common/scripted_effects/nesnd_qe1_court.txt',effects)
names={'crown':'皇权','literati':'地方士人','army':'军队'}
bars=''
for side in names:
 loc('nesnd_qe1_power_'+side,names[side]);bars+=bar('nesnd_qe1_'+side+'_bar','nesnd_qe1_power_'+side,0,100,0)
put('common/scripted_progress_bars/nesnd_qe1_court.txt',bars)
loc('nesnd_qe1_court_status','皇族、地方士人与军府正在争夺帝国的中枢。')
J=je('nesnd_qe1_court_journal','nesnd_qe1_court_eligible = yes','伊犁的朝议','皇帝凭借旧日征服的威望任命官员，地方士人依靠学堂、商号和官署主持日常政务，军队则掌握了帝国赖以扩张的武力。三者的合作使朝廷得以运转，他们也都希望把其他两方变成自己的助力。',extra='''
 immediate = { nesnd_qe1_initialize = yes nesnd_qe1_compute_court = yes }
 scripted_progress_bar = nesnd_qe1_crown_bar
 scripted_progress_bar = nesnd_qe1_literati_bar
 scripted_progress_bar = nesnd_qe1_army_bar
 scripted_button = nesnd_qe1_patron_crown_button
 scripted_button = nesnd_qe1_patron_literati_button
 scripted_button = nesnd_qe1_patron_army_button
 scripted_button = nesnd_qe1_patron_cancel_button
 scripted_button = nesnd_qe1_coup_crown_button
 scripted_button = nesnd_qe1_coup_literati_button
 scripted_button = nesnd_qe1_coup_army_button
 invalid = { NOT = { nesnd_qe1_court_eligible = yes } }
 on_invalid = { nesnd_qe1_archive_court = yes }
 on_weekly_pulse = { effect = { nesnd_qe1_compute_court = yes } }
 status_desc = nesnd_qe1_court_status
''')
put('common/journal_entries/nesnd_qe1_court.txt',J)
buttons=''
patron={'crown':('奖掖奉宸官僚','让依靠皇室任命的军士与官员掌握更多职位。'), 'literati':('奖掖地方士人','让学堂、商号与文官的意见更多地进入朝廷。'), 'army':('奖掖军府','让军队及支持军府的市民取得更多的政治声望。')}
for side in names:
 buttons+=button('nesnd_qe1_patron_'+side+'_button',*patron[side],f'nesnd_qe1_court_live = yes nesnd_qe1_{side}_strong = yes', 'hidden_trigger = { nesnd_qe1_no_patronage = yes }',f'set_variable = nesnd_qe1_patron_{side} add_modifier = {{ name = nesnd_qe1_patronage_{side} months = -1 }} nesnd_qe1_compute_court = yes',ai='value = 5')
buttons+=button('nesnd_qe1_patron_cancel_button','撤回奖掖','朝廷停止对这一方的特别扶持。','nesnd_qe1_court_live = yes NOT = { nesnd_qe1_no_patronage = yes }','always = yes','nesnd_qe1_clear_patronage = yes nesnd_qe1_compute_court = yes')
coups={
 'army':('军府接掌中枢','以军队与职业团体重组国家，专制的权力将由法团机关行使。','corporatism','activate_law = law_type:law_autocracy activate_law = law_type:law_corporate_state'),
 'literati':('改立共和','废除皇位，由民选总统与实行比例代表的议会主持国政。','democracy','activate_law = law_type:law_presidential_republic activate_law = law_type:law_nesnd_qe1_proportional_representation'),
 'crown':('重整皇权','保留皇位，把官署交给受过专业训练的技术官僚，以此重建君主的统治。','central_archives','activate_law = law_type:law_monarchy activate_law = law_type:law_technocracy'),
}
for side,(name,desc,tech,fx) in coups.items():
 buttons+=button('nesnd_qe1_coup_'+side+'_button',name,desc,f'nesnd_qe1_court_live = yes nesnd_qe1_{side}_peak = yes has_technology_researched = {tech}',f'has_technology_researched = {tech} hidden_trigger = {{ NOT = {{ has_variable = nesnd_qe1_peaceful_coup_cooldown }} }}',f'{fx} set_variable = {{ name = nesnd_qe1_peaceful_coup_cooldown years = 5 }} nesnd_qe1_clear_patronage = yes nesnd_qe1_compute_court = yes',ai='value = 1')
put('common/scripted_buttons/nesnd_qe1_court.txt',buttons)
put('common/static_modifiers/nesnd_qe1_court.txt','''
nesnd_qe1_patronage_crown = { interest_group_ig_landowners_pop_attraction_mult = 0.05 interest_group_ig_devout_pop_attraction_mult = 0.05 interest_group_ig_intelligentsia_pop_attraction_mult = -0.025 interest_group_ig_armed_forces_pop_attraction_mult = -0.025 }
nesnd_qe1_patronage_literati = { interest_group_ig_intelligentsia_pop_attraction_mult = 0.05 interest_group_ig_industrialists_pop_attraction_mult = 0.05 interest_group_ig_landowners_pop_attraction_mult = -0.025 interest_group_ig_armed_forces_pop_attraction_mult = -0.025 }
nesnd_qe1_patronage_army = { interest_group_ig_armed_forces_pop_attraction_mult = 0.05 interest_group_ig_petty_bourgeoisie_pop_attraction_mult = 0.05 interest_group_ig_landowners_pop_attraction_mult = -0.025 interest_group_ig_intelligentsia_pop_attraction_mult = -0.025 }
''')
for side in names:loc('nesnd_qe1_patronage_'+side,'奖掖'+names[side])
put('common/laws/nesnd_qe1_laws.txt','''
law_nesnd_qe1_proportional_representation = {
 parent = law_census_voting
 group = lawgroup_distribution_of_power
 icon = "gfx/interface/icons/law_icons/census_voting.dds"
 progressiveness = 60
 unlocking_technologies = { democracy }
 disallowing_laws = { law_chiefdom law_command_economy }
 modifier = {
  country_legitimacy_govt_total_votes_add = 85 country_legitimacy_govt_total_clout_add = 55
  country_legitimacy_govt_size_add = 2 country_legitimacy_ideological_incoherence_mult = -0.1
  country_voting_power_wealth_threshold_add = 10 country_voting_power_from_literacy_add = 50
  country_authority_add = 25 country_electoral_confidence_impact_mult = -0.1
 }
 can_enact = { c:QE1 ?= this }
 on_activate = {
  if = { limit = { game_date > 1836.1.1 country_has_voting_franchise = yes } initialize_electoral_confidence = yes }
  random_law = { limit = { type = law_type:law_nesnd_qe1_proportional_representation } save_scope_as = relevant_voting_law }
  handle_possible_absent_caciquismo_variables = yes
  scripted_effect_parties_emergence = yes
  inherit_caciquismo_effect = yes inherit_free_elections_effect = yes
 }
}
''')
loc('law_nesnd_qe1_proportional_representation','比例代表制','Proportional Representation');loc('law_nesnd_qe1_proportional_representation_desc','拥有财产与读写能力的选民选出代表，各政治团体依其支持组成议会与政府。','Literate property-owning voters elect representatives; political groups form a parliament and government according to their support.')

J=je('nesnd_qe1_recovery_journal','nesnd_qe1_recovery_eligible = yes','恢复故土','河西的关隘与关中的田地仍在陈秦皇族的记忆之中。若帝国能够重新控制通往东方的道路，恢复军队与官署的力量，朝廷便有机会以故土为起点，再次争夺华夏的天下。',extra='''
 immediate = { nesnd_qe1_initialize = yes }
 complete = { nesnd_qe1_recovery_ready = yes }
 on_complete = { if = { limit = { NOT = { has_variable = nesnd_qe1_recovery_done } } set_variable = nesnd_qe1_recovery_done set_variable = nesnd_qe1_recovery_reward_pending trigger_event = { id = nesnd_qe1_recovery.1 popup = yes } } }
 invalid = { NOT = { nesnd_qe1_recovery_eligible = yes } }
 on_invalid = { set_variable = nesnd_qe1_recovery_done }
''')
put('common/journal_entries/nesnd_qe1_recovery.txt',J)
source=parse(read(C/'common/scripted_triggers/ce_scripted_triggers.txt')).get('is_modern_china_state')
regions={a.value[2:] for a in source.walk() if a.key=='state_region' and a.value and a.value.startswith('s:')}-{'STATE_FORMOSA','STATE_HAINAN'}
extra=['STATE_SHENGJING','STATE_OUTER_MANCHURIA','STATE_AMUR','STATE_YANGHO','STATE_YANGSEO','STATE_GWANBUK','STATE_KANTO','STATE_KANSAI','STATE_TOHOKU','STATE_CHUBU','STATE_CHUGOKU','STATE_KYUSHU','STATE_SHIKOKU','STATE_HOKKAIDO','STATE_SAKHALIN','STATE_URGA','STATE_ULIASTAI','STATE_TUVA']
defs=set()
for root in [G,C]:
 for p in (root/'map_data/state_regions').glob('*.txt'):defs.update(n.key for n in parse(read(p)).children)
regions|={s for s in extra if s in defs}
put('common/scripted_effects/nesnd_qe1_recovery.txt','nesnd_qe1_recovery_claims = {\n'+''.join(f's:{x} = {{ add_claim = root }}\n' for x in sorted(regions))+'}\n')
dump(R/'recovery-claim-regions.json',{'regions':sorted(regions),'northeast_asia_scope':'Manchuria, Korea, Japan, Mongolia/Tuva; explicit existing state regions','excluded_mainland_islands':['STATE_FORMOSA','STATE_HAINAN']})
put('common/static_modifiers/nesnd_qe1_recovery.txt','''
nesnd_qe1_recovered_military = { unit_army_offense_mult = 0.2 unit_army_defense_mult = 0.2 country_military_goods_cost_mult = -0.2 }
nesnd_qe1_recovered_civil = { country_bureaucracy_mult = 0.25 state_construction_mult = 0.15 state_tax_capacity_mult = 0.2 state_assimilation_mult = 0.5 state_conversion_mult = 0.5 }
''')
loc('nesnd_qe1_recovered_military','再造秦军');loc('nesnd_qe1_recovered_civil','故土新政')
loc('nesnd_qe1_recovery.1.a','以故土重整军伍。');loc('nesnd_qe1_recovery.1.b','先把新政推向各地。')
options=''
for letter,mod in [('a','military'),('b','civil')]:
 options+=f'''option = {{ name = nesnd_qe1_recovery.1.{letter} {'default_option = yes' if letter=='a' else ''} ai_chance = {{ base = 50 }} if = {{ limit = {{ has_variable = nesnd_qe1_recovery_reward_pending NOT = {{ has_variable = nesnd_qe1_recovery_rewarded }} }} set_variable = nesnd_qe1_recovery_rewarded remove_variable = nesnd_qe1_recovery_reward_pending nesnd_qe1_recovery_claims = yes add_modifier = {{ name = nesnd_qe1_recovered_{mod} years = 15 }} }} }}\n'''
put('events/nesnd_qe1_recovery.txt','namespace = nesnd_qe1_recovery\n'+event('nesnd_qe1_recovery.1','重返故土','秦军重新控制了河西与关中的道路。故土的归属已经改变，朝廷却仍须决定如何使用这次胜利：以新军继续向东，还是先把新的官署、产业与共同身份扎根于各省。',options,trigger='has_variable = nesnd_qe1_recovery_reward_pending NOT = { has_variable = nesnd_qe1_recovery_rewarded }'))
flush_loc();print('Three-power court, explicit voting law and recovery reward generated.')
