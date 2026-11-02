from qin_persia_build_support import *
mapping=json.loads(read(R/'native-identity-map.json'))
eligible=[x for x in mapping['states'] if x['eligible_non_sinosphere_pairs']]
tr='''
nesnd_qe1_unity_live = { nesnd_qe1_unity_eligible = yes has_journal_entry = nesnd_qe1_unity_journal }
nesnd_qe1_decay_state = { owner = c:QE1 any_scope_pop = { culture = cu:ce_xiyu } OR = {
'''+''.join(f'state_region = s:{x["region"]}\n' for x in eligible)+''' } }
nesnd_qe1_persian_subversion = {
 trigger_if = { limit = { exists = c:PER }
  c:PER = { has_journal_entry = nesnd_per_future_journal has_variable = nesnd_per_route_covert NOT = { has_variable = nesnd_per_future_done } }
 }
 trigger_else = { always = no }
}
'''
put('common/scripted_triggers/nesnd_qe1_identity.txt',tr)
values='''
nesnd_qe1_population = { value = 0 every_scope_state = { add = state_population } }
nesnd_qe1_sol_sum = { value = 0 every_scope_state = { every_scope_pop = { add = { value = total_size multiply = standard_of_living } } } }
nesnd_qe1_average_sol = { value = 0 if = { limit = { nesnd_qe1_population > 0 } value = nesnd_qe1_sol_sum divide = nesnd_qe1_population } }
nesnd_qe1_soldier_population = { value = 0 every_scope_state = { every_scope_pop = { limit = { is_pop_type = soldiers } add = total_size } } }
nesnd_qe1_soldier_radicals_sum = { value = 0 every_scope_state = { every_scope_pop = { limit = { is_pop_type = soldiers } add = { value = total_size multiply = pop_radical_fraction } } } }
nesnd_qe1_soldier_radicals = { value = 0 if = { limit = { nesnd_qe1_soldier_population > 0 } value = nesnd_qe1_soldier_radicals_sum divide = nesnd_qe1_soldier_population } }
nesnd_qe1_significant_cultures = { value = 0 every_scope_culture = { limit = { root = { "culture_percent_country(prev)" >= 0.01 } } add = 1 } }
nesnd_qe1_unity_order = { value = 0.15 }
nesnd_qe1_unity_population = { value = primary_cultures_percent_country subtract = 0.65 multiply = 0.8 }
nesnd_qe1_unity_diversity = { value = nesnd_qe1_significant_cultures subtract = 3 max = 0 multiply = -0.025 }
nesnd_qe1_unity_livelihood = { value = 0 if = { limit = { has_variable = nesnd_qe1_sol_change } if = { limit = { var:nesnd_qe1_sol_change >= 0.05 } add = 0.4 } if = { limit = { var:nesnd_qe1_sol_change <= -0.05 } add = -0.6 } } if = { limit = { has_modifier = declared_bankruptcy } add = -1.5 } }
nesnd_qe1_unity_institutions = {
 value = 0
 if = { limit = { bureaucracy >= 0 } add = 0.1 } else = { add = -0.4 }
 if = { limit = { institution_investment_level = { institution = institution_schools value >= 1 } } add = 0.05 }
 if = { limit = { institution_investment_level = { institution = institution_schools value >= 2 } } add = 0.05 }
 if = { limit = { institution_investment_level = { institution = institution_schools value >= 3 } } add = 0.05 }
 if = { limit = { institution_investment_level = { institution = institution_schools value >= 4 } } add = 0.05 }
 if = { limit = { institution_investment_level = { institution = institution_police value >= 2 } } add = 0.05 }
 if = { limit = { institution_investment_level = { institution = institution_health_system value >= 2 } } add = 0.05 }
}
nesnd_qe1_unity_laws = {
 value = 0
 if = { limit = { has_law_or_variant = law_type:law_multicultural } add = 0.15 }
 if = { limit = { has_law_or_variant = law_type:law_national_supremacy } add = -0.25 }
 if = { limit = { has_law_or_variant = law_type:law_racial_segregation } add = -0.1 }
 if = { limit = { has_law_or_variant = law_type:law_freedom_of_conscience } add = 0.05 }
 if = { limit = { has_law_or_variant = law_type:law_total_separation } add = 0.1 }
 if = { limit = { has_law_or_variant = law_type:law_mass_conscription is_at_war = yes } add = -0.2 }
}
nesnd_qe1_unity_war = { value = 0 if = { limit = { is_at_war = yes } add = -0.2 if = { limit = { var:nesnd_qe1_war_months >= 12 } add = -0.3 } if = { limit = { var:nesnd_qe1_war_months >= 24 } add = -0.3 } } }
nesnd_qe1_unity_infamy = { value = 0 if = { limit = { infamy >= 25 } add = -0.15 } if = { limit = { infamy >= 50 } add = -0.25 } if = { limit = { infamy >= 100 } add = -0.5 } }
nesnd_qe1_unity_soldiers = { value = 0 if = { limit = { pop_type_percent_country = { pop_type = soldiers percent > 0.03 } } add = -0.15 } if = { limit = { nesnd_qe1_soldier_radicals >= 0.25 } add = -0.3 } if = { limit = { ig:ig_armed_forces = { approval >= 5 } } add = 0.1 } }
nesnd_qe1_unity_victory = { value = 0 if = { limit = { has_variable = nesnd_qe1_victory_prestige } add = 0.15 } if = { limit = { has_variable = nesnd_qe1_new_land_prestige } add = 0.1 } }
nesnd_qe1_unity_persia = { value = 0 if = { limit = { nesnd_qe1_persian_subversion = yes } value = -1 } }
nesnd_qe1_unity_delta = { value = nesnd_qe1_unity_order add = nesnd_qe1_unity_population add = nesnd_qe1_unity_diversity add = nesnd_qe1_unity_livelihood add = nesnd_qe1_unity_institutions add = nesnd_qe1_unity_laws add = nesnd_qe1_unity_war add = nesnd_qe1_unity_infamy add = nesnd_qe1_unity_soldiers add = nesnd_qe1_unity_victory add = nesnd_qe1_unity_persia }
nesnd_qe1_uprising_low_unity = { value = 0 if = { limit = { var:nesnd_qe1_unity < 25 } value = 2 } else = { value = -1 } }
nesnd_qe1_uprising_war = { value = 0 if = { limit = { var:nesnd_qe1_unity < 25 is_at_war = yes } value = 1 } }
nesnd_qe1_uprising_deprivation = { value = 0 if = { limit = { var:nesnd_qe1_unity < 25 OR = { has_modifier = declared_bankruptcy radical_population_fraction > 0.25 } } value = 1 } }
nesnd_qe1_uprising_delta = { value = nesnd_qe1_uprising_low_unity add = nesnd_qe1_uprising_war add = nesnd_qe1_uprising_deprivation }
'''
put('common/script_values/nesnd_qe1_identity.txt',values)
parts=[]
for suffix,label in [('order','朝廷秩序'),('population','主流人口'),('diversity','地方文化'),('livelihood','生计的变化'),('institutions','行政与机构'),('laws','帝国的法令'),('war','经年战事'),('infamy','征伐之名'),('soldiers','营伍的人心'),('victory','边功与新地'),('persia','波斯文化秘密运动')]:
 loc('nesnd_qe1_unity_'+suffix+'_desc',label);parts.append(('nesnd_qe1_unity_'+suffix+'_desc','nesnd_qe1_unity_'+suffix))
loc('nesnd_qe1_unity','文化团结度','Cultural Cohesion');loc('nesnd_qe1_uprising','羌种暴动','Frontier Uprising')
bars=bar('nesnd_qe1_unity_bar','nesnd_qe1_unity',0,100,70,parts)
loc('nesnd_qe1_uprising_low_unity_desc','地方的离心与复归');loc('nesnd_qe1_uprising_war_desc','战事未息');loc('nesnd_qe1_uprising_deprivation_desc','破产与激愤')
bars+=bar('nesnd_qe1_uprising_bar','nesnd_qe1_uprising',0,100,0,[(f'nesnd_qe1_uprising_{x}_desc',f'nesnd_qe1_uprising_{x}') for x in ['low_unity','war','deprivation']],False)
put('common/scripted_progress_bars/nesnd_qe1_identity.txt',bars)
loc('nesnd_qe1_unity_hope','田野、市镇与营伍仍把自身的前途寄托在帝国之中。')
loc('nesnd_qe1_unity_doubt','地方正在重新讲述自己的来历，朝廷的号令越来越难抵达。')
loc('nesnd_qe1_unity_crisis','旧日族名已成为结社与举兵的旗帜。')
J=je('nesnd_qe1_unity_journal','nesnd_qe1_unity_eligible = yes','帝国的稳定','商路、村社与军屯把许多不同来历的人联结在陈秦皇帝的治下。西域汉羌既是帝国扩张的产物，也为这个国家提供了兵员与税源。人们在繁荣中接受共同的身份，也会在征役与贫困中重新寻找旧日的族名、信仰和乡里。',extra='''
 immediate = { nesnd_qe1_initialize = yes nesnd_qe1_unity_sync = yes }
 scripted_progress_bar = nesnd_qe1_unity_bar
 invalid = { NOT = { nesnd_qe1_unity_eligible = yes } }
 on_monthly_pulse = { effect = { nesnd_qe1_unity_monthly = yes } }
 status_desc = { first_valid = {
 triggered_desc = { trigger = { var:nesnd_qe1_unity < 25 } desc = nesnd_qe1_unity_crisis }
 triggered_desc = { trigger = { var:nesnd_qe1_unity < 50 } desc = nesnd_qe1_unity_doubt }
 desc = nesnd_qe1_unity_hope } }
''')
J+=je('nesnd_qe1_uprising_journal','nesnd_qe1_unity_live = yes has_variable = nesnd_qe1_uprising_awakened','羌种暴动','边地的社团已不再满足于请愿。他们募集粮饷，联系旧贵族与宗教领袖，以本地人的名义向帝国征税的官署和征兵的军府发出挑战。伊犁仍有机会恢复人心，但拖延将使各地的反抗连成一片。',extra='''
 scripted_progress_bar = nesnd_qe1_uprising_bar
 immediate = { nesnd_qe1_unity_sync = yes }
 complete = { nesnd_qe1_unity_live = yes var:nesnd_qe1_uprising >= 100 }
 on_complete = { nesnd_qe1_breakup = yes }
 invalid = { NOT = { nesnd_qe1_unity_live = yes } }
 on_monthly_pulse = { effect = { if = { limit = { nesnd_qe1_unity_live = yes } change_variable = { name = nesnd_qe1_uprising add = nesnd_qe1_uprising_delta } clamp_variable = { name = nesnd_qe1_uprising min = 0 max = 100 } nesnd_qe1_unity_sync = yes } } }
''')
put('common/journal_entries/nesnd_qe1_identity.txt',J)
effects='''
nesnd_qe1_unity_sync = {
 if = { limit = { has_journal_entry = nesnd_qe1_unity_journal } je:nesnd_qe1_unity_journal = { set_bar_progress = { name = nesnd_qe1_unity_bar value = root.var:nesnd_qe1_unity } } }
 if = { limit = { has_journal_entry = nesnd_qe1_uprising_journal } je:nesnd_qe1_uprising_journal = { set_bar_progress = { name = nesnd_qe1_uprising_bar value = root.var:nesnd_qe1_uprising } } }
}
nesnd_qe1_unity_monthly = {
 if = { limit = { nesnd_qe1_unity_live = yes }
  set_variable = { name = nesnd_qe1_sol_current value = nesnd_qe1_average_sol }
  set_variable = { name = nesnd_qe1_sol_change value = 0 }
  if = { limit = { has_variable = nesnd_qe1_sol_previous } set_variable = { name = nesnd_qe1_sol_change value = { value = var:nesnd_qe1_sol_current subtract = var:nesnd_qe1_sol_previous } } }
  set_variable = { name = nesnd_qe1_sol_previous value = var:nesnd_qe1_sol_current }
  if = { limit = { is_at_war = yes } change_variable = { name = nesnd_qe1_war_months add = 1 } } else = { set_variable = { name = nesnd_qe1_war_months value = 0 } }
  change_variable = { name = nesnd_qe1_unity add = nesnd_qe1_unity_delta }
  clamp_variable = { name = nesnd_qe1_unity min = 0 max = 100 }
  if = { limit = { var:nesnd_qe1_unity > 75 }
   every_scope_state = { every_scope_pop = { limit = { NOT = { culture = { has_cultural_trait = tradition_sinosphere } } NOT = { culture = cu:nesnd_qe1_conversion_cohort } } change_pop_culture = { target = cu:ce_xiyu value = 0.005 } } }
  }
  if = { limit = { var:nesnd_qe1_unity < 50 any_scope_state = { nesnd_qe1_decay_state = yes } }
   random_list = {
    80 = { }
    20 = { random_scope_state = { limit = { nesnd_qe1_decay_state = yes } save_scope_as = nesnd_qe1_declining_state } trigger_event = { id = nesnd_qe1_identity.1 popup = yes } }
   }
  }
  if = { limit = { var:nesnd_qe1_unity < 25 }
   set_variable = nesnd_qe1_uprising_awakened
   if = { limit = { NOT = { has_journal_entry = nesnd_qe1_uprising_journal } } add_journal_entry = { type = nesnd_qe1_uprising_journal } }
  }
  nesnd_qe1_unity_sync = yes
 }
}
# State scope. Fresh loops after each split ensure culture and religion affect the same half.
nesnd_qe1_convert_selected_cohort = {
 every_scope_pop = { limit = { culture = cu:ce_xiyu } change_pop_culture = { target = cu:nesnd_qe1_conversion_cohort value = 0.5 } }
 every_scope_pop = { limit = { culture = cu:nesnd_qe1_conversion_cohort } change_pop_religion = { target = scope:nesnd_qe1_return_religion value = 1 } }
 every_scope_pop = { limit = { culture = cu:nesnd_qe1_conversion_cohort } change_pop_culture = { target = scope:nesnd_qe1_return_culture value = 1 } }
}
nesnd_qe1_clear_orphan_cohort = { every_scope_pop = { limit = { culture = cu:nesnd_qe1_conversion_cohort } change_pop_culture = { target = cu:ce_xiyu value = 1 } } }
nesnd_qe1_select_old_identity = {
'''
for i,row in enumerate(eligible):
 effects+=('if' if i==0 else 'else_if')+f' = {{ limit = {{ state_region = s:{row["region"]} }} random_list = {{\n'
 for pair in row['eligible_non_sinosphere_pairs']:
  effects+=f'{pair["weight"]} = {{ cu:{pair["culture"]} = {{ save_scope_as = nesnd_qe1_return_culture }} rel:{pair["religion"]} = {{ save_scope_as = nesnd_qe1_return_religion }} }}\n'
 effects+='} }\n'
effects+='''
 if = { limit = { exists = scope:nesnd_qe1_return_culture exists = scope:nesnd_qe1_return_religion }
  nesnd_qe1_convert_selected_cohort = yes
 }
}
'''
put('common/scripted_effects/nesnd_qe1_identity.txt',effects)
# Clone only the author's own culture definition for an invisible transient cohort;
# no initial population, no new names/assets, and never retained as a political identity.
p=C/'common/cultures/CE_cultures.txt';s=read(p);n=parse(s).get('ce_xiyu');assert n;cohort=s[n.start:n.end];cohort=cohort.replace('ce_xiyu','nesnd_qe1_conversion_cohort',1)
put('common/cultures/nesnd_qe1_cohort.txt',cohort);loc('nesnd_qe1_conversion_cohort','西域汉羌','Western Han-Qiang')
loc('nesnd_qe1_identity.1.a','地方已不再相信旧日的许诺。')
ev=event('nesnd_qe1_identity.1','认同的衰退','[SCOPE.sState(\'nesnd_qe1_declining_state\').GetName]的村社与军屯正在重述自己的来历。旧时的族名、经文与乡里关系重新成为人们彼此信任的凭据。帝国仍能向他们征税，却越来越难使他们承认这份共同的身份。','option = { name = nesnd_qe1_identity.1.a default_option = yes }',trigger='nesnd_qe1_unity_live = yes var:nesnd_qe1_unity < 50 exists = scope:nesnd_qe1_declining_state scope:nesnd_qe1_declining_state ?= { nesnd_qe1_decay_state = yes }',immediate='if = { limit = { exists = scope:nesnd_qe1_declining_state } scope:nesnd_qe1_declining_state = { if = { limit = { nesnd_qe1_decay_state = yes } nesnd_qe1_select_old_identity = yes } } }',placement='scope:nesnd_qe1_declining_state')
put('events/nesnd_qe1_identity.txt','namespace = nesnd_qe1_identity\n'+ev)
dump(R/'identity-implementation-mapping.json',{'regions':[x['region'] for x in eligible],'pairs':sum(len(x['eligible_non_sinosphere_pairs']) for x in eligible),'cohort_fraction':.5,'assimilation_per_month':.005,'religion_preserved_on_assimilation':True,'game_launched':False})
flush_loc();print('Cohesion, conditional uprising JE and paired identity conversion generated.')
