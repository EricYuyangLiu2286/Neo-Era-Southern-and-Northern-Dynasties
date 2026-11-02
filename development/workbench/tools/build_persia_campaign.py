from qin_persia_build_support import *
claims=json.loads(read(R/'claimsets.json'))['recommended']
groups={
 'levant':('aid_west_levant_and_southern_anatolia','黎凡特','west'),
 'egypt':('aid_west_egypt','尼罗河流域','west'),
 'arabia':('aid_west_arabia','阿拉伯','west'),
 'central_asia':('covert_east_native_khorasan_chorasmia_transoxiana','中亚','east'),
 'india':('covert_east_northwestern_india','印度河流域','east')}
tr='''
nesnd_per_country = { c:PER ?= this is_country_alive = yes }
nesnd_per_future_eligible = { nesnd_per_country = yes NOT = { has_variable = nesnd_per_future_done } }
nesnd_per_future_live = { nesnd_per_future_eligible = yes has_journal_entry = nesnd_per_future_journal }
nesnd_per_route_unset = { NOR = { has_variable = nesnd_per_route_aid has_variable = nesnd_per_route_covert } }
nesnd_per_aid_live = { nesnd_per_future_live = yes has_variable = nesnd_per_route_aid }
nesnd_per_west_eligible = { nesnd_per_country = yes has_variable = nesnd_per_future_done has_variable = nesnd_per_route_aid }
nesnd_per_east_eligible = { nesnd_per_country = yes has_variable = nesnd_per_future_done has_variable = nesnd_per_route_covert }
nesnd_per_civil_ready = {
 has_law_or_variant = law_type:law_appointed_bureaucrats
 institution_investment_level = { institution = institution_schools value >= 2 }
 country_has_building_type_levels = { target = bt:building_university value >= 3 }
}
nesnd_per_economy_ready = {
 country_has_building_type_levels = { target = bt:building_cotton_plantation value >= 10 }
 country_has_building_type_levels = { target = bt:building_textile_mills value >= 10 }
 country_has_building_type_levels = { target = bt:building_railway value >= 5 }
}
nesnd_per_claim_obstructor = {
 trigger_if = { limit = { exists = scope:nesnd_per_claim_state exists = scope:nesnd_per_claim_region exists = scope:nesnd_per_potential_obstructor }
  NOT = { this = root }
  relations:root <= relations_threshold:neutral
  NOR = { has_truce_with = root is_diplomatic_play_ally_of = root root = { is_subject_of = prev } any_scope_treaty = { binds = root any_scope_article = { OR = { has_type = alliance has_type = defensive_pact } } } }
  OR = {
   has_interest_marker_in_region = scope:nesnd_per_claim_state.region
   scope:nesnd_per_claim_region = { any_scope_state = { owner = { OR = { this = scope:nesnd_per_potential_obstructor is_subject_of = scope:nesnd_per_potential_obstructor } } } }
  }
 }
 trigger_else = { always = no }
}
'''
for key,(source,name,direction) in groups.items():
 regs=[x['state_region'] for x in claims[source]]
 tr+=f'nesnd_per_claim_{key}_state = {{ NOT = {{ owner = root }} NOT = {{ has_claim_by = root }} OR = {{ '+ ' '.join('state_region = s:'+r for r in regs)+' } }\n'
put('common/scripted_triggers/nesnd_per_campaign.txt',tr)
put('common/script_values/nesnd_per_campaign.txt','''
nesnd_per_future_delta = { value = 0 if = { limit = { NOT = { nesnd_per_route_unset = yes } } value = 2 } }
''')
loc('nesnd_per_future_progress','近西帝国的前途','The Near-Western Empire’s Future');loc('nesnd_per_future_delta_desc','朝廷的部署','Preparations of the court')
put('common/scripted_progress_bars/nesnd_per_campaign.txt',bar('nesnd_per_future_bar','nesnd_per_future_progress',0,100,0,[('nesnd_per_future_delta_desc','nesnd_per_future_delta')]))
for k,z in [('choice','朝廷尚未决定与伊犁的关系。'),('aid','使者正在往来，朝廷准备借秦国的力量经营西方。'),('covert','朝廷的使者正在中亚联络不满伊犁的地方势力。')]:loc('nesnd_per_future_status_'+k,z)
J=je('nesnd_per_future_journal','nesnd_per_future_eligible = yes','近西帝国的未来','唐衣大食的君臣熟悉秦国的军府，也熟悉波斯的商旅与地方家族。近西战争留下了土地和声望，却没有替后人决定帝国的方向：朝廷可以借伊犁的力量向西经营，也可以在西秦的地方纷争中寻找独立扩张的机会。',extra='''
 immediate = { nesnd_per_initialize = yes nesnd_per_future_sync = yes }
 scripted_progress_bar = nesnd_per_future_bar
 scripted_button = nesnd_per_seek_aid_button
 scripted_button = nesnd_per_subvert_button
 complete = { trigger_if = { limit = { has_variable = nesnd_per_future_progress } var:nesnd_per_future_progress >= 100 } trigger_else = { always = no } }
 on_complete = { nesnd_per_settle_future = yes }
 invalid = { NOT = { nesnd_per_future_eligible = yes } }
 on_monthly_pulse = { effect = { nesnd_per_future_monthly = yes } }
 status_desc = { first_valid = {
  triggered_desc = { trigger = { has_variable = nesnd_per_route_aid } desc = nesnd_per_future_status_aid }
  triggered_desc = { trigger = { has_variable = nesnd_per_route_covert } desc = nesnd_per_future_status_covert }
  desc = nesnd_per_future_status_choice
 } }
''')
J+=je('nesnd_per_civil_journal','nesnd_per_country = yes','唐衣之下','军府带来的官制与本地的书院、宗教学校和家族并存。朝廷要使不同出身的官员共同办事，就需要可靠的任官制度，也需要能够训练新人的学堂。',extra='''
 scripted_button = nesnd_per_civil_commit_button
 invalid = { NOT = { nesnd_per_country = yes } }
 on_invalid = { remove_modifier = nesnd_per_civil_order }
 on_monthly_pulse = { effect = { if = { limit = { nesnd_per_civil_ready = yes } add_modifier = { name = nesnd_per_civil_order months = 2 } } else = { remove_modifier = nesnd_per_civil_order } } }
''')
J+=je('nesnd_per_economy_journal','nesnd_per_country = yes','波斯的市镇','棉田、织工与往来商旅维持着波斯的繁荣。朝廷希望用铁路联结产地与市镇，使近西战争得到的土地不仅供养军队，也能养活新的工场。',extra='''
 scripted_button = nesnd_per_economy_commit_button
 invalid = { NOT = { nesnd_per_country = yes } }
 on_invalid = { remove_modifier = nesnd_per_industry_order }
 on_monthly_pulse = { effect = { if = { limit = { nesnd_per_economy_ready = yes } add_modifier = { name = nesnd_per_industry_order months = 2 } } else = { remove_modifier = nesnd_per_industry_order } } }
''')
for direction,name,desc in [('west','重启远西战争','朝廷已把目光投向两河以西。来自秦国的军事传统与波斯的财力将服务于新的扩张，而奥斯曼、埃及及阿拉伯的诸国也会寻找自己的强国援手。'),('east','近西战争重启','伊犁的权威正在受到挑战。朝廷准备沿中亚与印度的道路追求自己的利益，昔日宗主的边疆如今也进入了军府的地图。')]:
 buttons='\n'.join('scripted_button = nesnd_per_claim_'+k+'_button' for k,(_,_,d) in groups.items() if d==direction)
 J+=je('nesnd_per_'+direction+'_journal',f'nesnd_per_{direction}_eligible = yes',name,desc,extra=buttons+f'\ninvalid = {{ NOT = {{ nesnd_per_{direction}_eligible = yes }} }}')
put('common/journal_entries/nesnd_per_campaign.txt',J)
buttons=button('nesnd_per_seek_aid_button','遣使伊犁','请求秦国帮助朝廷整顿官署与军政，为向西扩张准备力量。','nesnd_per_future_live = yes nesnd_per_route_unset = yes','always = yes','set_variable = nesnd_per_route_aid nesnd_per_future_sync = yes')
buttons+=button('nesnd_per_subvert_button','联络西秦诸部','结交不满伊犁的地方领袖，准备摆脱宗主并经营东方。','nesnd_per_future_live = yes nesnd_per_route_unset = yes','always = yes','set_variable = nesnd_per_route_covert nesnd_per_future_sync = yes')
for key,title,desc,ready,modifier in [('civil','整顿官署','任用受过训练的官员，把书院与官署的培养连在一起。','nesnd_per_civil_ready','nesnd_per_civil_order'),('economy','奖掖工商业','支持已有的棉田、织造与铁路，使商路和工场相互接续。','nesnd_per_economy_ready','nesnd_per_industry_order')]:
 buttons+=button(f'nesnd_per_{key}_commit_button',title,desc,'nesnd_per_country = yes',ready+' = yes',f'add_modifier = {{ name = {modifier} months = 2 }}')
for key,(_,label,direction) in groups.items():
 buttons+=button(f'nesnd_per_claim_{key}_button','申明'+label+'旧权','朝廷将向尚未承认我方权利的地区发出照会；相关强国可能出面阻挠。',f'has_journal_entry = nesnd_per_{direction}_journal',f'hidden_trigger = {{ NOT = {{ has_variable = nesnd_per_claim_cooldown }} }} any_state = {{ nesnd_per_claim_{key}_state = yes }}',f'''
 clear_saved_scope = nesnd_per_claim_state clear_saved_scope = nesnd_per_claim_region
 random_state = {{ limit = {{ nesnd_per_claim_{key}_state = yes }} save_scope_as = nesnd_per_claim_state state_region = {{ save_scope_as = nesnd_per_claim_region }} }}
 if = {{ limit = {{ exists = scope:nesnd_per_claim_state exists = scope:nesnd_per_claim_region }} nesnd_per_attempt_claim = yes }}
''',ai='value = 10 if = { limit = { OR = { is_at_war = yes in_default = yes government_legitimacy < 25 } } multiply = 0 }')
put('common/scripted_buttons/nesnd_per_campaign.txt',buttons)
put('common/static_modifiers/nesnd_per_campaign.txt','''
nesnd_per_aid_law = { country_law_enactment_speed_mult = 0.1 }
nesnd_per_aid_building = { state_construction_mult = 0.05 }
nesnd_per_aid_legitimacy = { country_legitimacy_base_add = 5 }
nesnd_per_claim_cost = { country_legitimacy_base_add = -5 }
nesnd_per_civil_order = { country_legitimacy_base_add = 3 }
nesnd_per_industry_order = { building_group_bg_manufacturing_throughput_add = 0.05 }
''')
for k,z in [('aid_law','伊犁的议法官'),('aid_building','援建工匠'),('aid_legitimacy','秦使的认可'),('claim_cost','边地交涉'),('civil_order','官署渐整'),('industry_order','市镇渐兴')]:loc('nesnd_per_'+k,z)
effects='''
nesnd_per_initialize = {
 if = { limit = { nesnd_per_country = yes NOT = { has_variable = nesnd_per_campaign_v1 } }
  set_variable = nesnd_per_campaign_v1 set_variable = { name = nesnd_per_future_progress value = 0 }
 }
}
nesnd_per_future_sync = { if = { limit = { has_journal_entry = nesnd_per_future_journal } je:nesnd_per_future_journal = { set_bar_progress = { name = nesnd_per_future_bar value = root.var:nesnd_per_future_progress } } } }
nesnd_per_future_monthly = {
 if = { limit = { nesnd_per_future_live = yes }
  if = { limit = { is_ai = yes nesnd_per_route_unset = yes } random_list = { 75 = { set_variable = nesnd_per_route_aid } 25 = { set_variable = nesnd_per_route_covert } } }
  change_variable = { name = nesnd_per_future_progress add = nesnd_per_future_delta }
  clamp_variable = { name = nesnd_per_future_progress min = 0 max = 100 }
  if = { limit = { nesnd_per_aid_live = yes var:nesnd_per_future_progress < 100 }
   random_list = { 70 = { } 10 = { trigger_event = { id = nesnd_per.1 popup = yes } } 10 = { trigger_event = { id = nesnd_per.2 popup = yes } } 10 = { trigger_event = { id = nesnd_per.3 popup = yes } } }
  }
  nesnd_per_future_sync = yes
 }
}
nesnd_per_ensure_frontier = {
 if = { limit = { nesnd_per_west_eligible = yes NOT = { has_journal_entry = nesnd_per_west_journal } } add_journal_entry = { type = nesnd_per_west_journal } }
 if = { limit = { nesnd_per_east_eligible = yes NOT = { has_journal_entry = nesnd_per_east_journal } } add_journal_entry = { type = nesnd_per_east_journal } }
}
nesnd_per_settle_future = {
 if = { limit = { nesnd_per_future_live = yes NOT = { has_variable = nesnd_per_future_done } }
  set_variable = nesnd_per_future_done
  if = { limit = { has_variable = nesnd_per_route_aid }
   if = { limit = { exists = c:QE1 }
    if = { limit = { is_subject_of = c:QE1 } change_subject_type = subject_type_tributary }
    else_if = { limit = { is_subject = no c:QE1 = { can_create_diplomatic_pact = { target = root type = tributary } } } c:QE1 = { create_diplomatic_pact = { country = root type = tributary } } }
    else = { set_variable = nesnd_per_aid_relation_unavailable }
   } else = { set_variable = nesnd_per_aid_relation_unavailable }
   trigger_event = { id = nesnd_per.4 popup = yes }
  } else = {
   if = { limit = { exists = c:QE1 } if = { limit = { is_subject_of = c:QE1 } make_independent = yes } }
   trigger_event = { id = nesnd_per.5 popup = yes }
  }
  nesnd_per_ensure_frontier = yes
 }
}
nesnd_per_attempt_claim = {
 if = { limit = { nesnd_per_country = yes NOT = { has_variable = nesnd_per_claim_cooldown } exists = scope:nesnd_per_claim_state exists = scope:nesnd_per_claim_region }
  set_variable = { name = nesnd_per_claim_cooldown months = 1 }
  add_modifier = { name = nesnd_per_claim_cost months = 1 }
  clear_saved_scope = nesnd_per_obstructor
  every_country = {
   limit = { OR = { this = c:FRA this = c:MUG this = c:USM this = c:RUS this = c:QE1 country_rank >= rank_value:major_power country_rank = rank_value:unrecognized_major_power } }
   if = { limit = { NOT = { exists = scope:nesnd_per_obstructor } }
    save_scope_as = nesnd_per_potential_obstructor
    if = { limit = { nesnd_per_claim_obstructor = yes } save_scope_as = nesnd_per_obstructor }
   }
  }
  if = { limit = { exists = scope:nesnd_per_obstructor } trigger_event = { id = nesnd_per.7 popup = yes } }
  else = { scope:nesnd_per_claim_region = { add_claim = root } trigger_event = { id = nesnd_per.6 popup = yes } }
 }
}
'''
put('common/scripted_effects/nesnd_per_campaign.txt',effects)
ev='namespace = nesnd_per\n'
aid_events=[(1,'伊犁的议法官','秦国派来的官员带来了军府之外的另一种经验。他们与本地书吏共同整理法令，希望使官员、商人和田主不必再为同一件事奔走于几套不同的规矩之间。','aid_law'),(2,'援建工匠','随使团而来的工匠已经进入当地工场。他们传授测量、营造与机器维修的方法，也需要本地工人与商人把这些知识变成能够长期经营的产业。','aid_building'),(3,'秦使入朝','秦国使者在朝会上确认了对本朝的支持。与伊犁保持联系的军官和商人因此安下心来，朝廷也得以暂时压低反对者的声势。','aid_legitimacy')]
for i,title,desc,mod in aid_events:
 loc(f'nesnd_per.{i}.a','接纳这些援助。');ev+=event(f'nesnd_per.{i}',title,desc,f'option = {{ name = nesnd_per.{i}.a default_option = yes }}',trigger='nesnd_per_aid_live = yes',immediate=f'if = {{ limit = {{ nesnd_per_aid_live = yes }} add_modifier = {{ name = nesnd_per_{mod} months = 6 }} }}')
for i,title,desc,opt in [(4,'西向之策','朝廷已经完成面向西方的部署。伊犁能否继续提供援助，仍取决于两国眼下的处境；波斯的军府与商人则已开始议论新的道路和土地。','向西经营。'),(5,'东方的机会','联络西秦地方势力的部署已经完成。朝廷准备以自身的名义经营中亚与印度，来自伊犁的号令将不再决定这条道路。','近西战争将有新的篇章。'),(6,'边地照会',"朝廷已正式申明对[SCOPE.sStateRegion('nesnd_per_claim_region').GetName]的权利。军府与商人可以据此准备下一步行动，土地的实际归属仍有待外交与战争决定。",'将照会交予各国。'),(7,'强国的反对',"关于[SCOPE.sStateRegion('nesnd_per_claim_region').GetName]的照会遭到强国阻挠。朝廷暂未取得所求的承认，必须先改变当地的外交处境。",'暂缓这次交涉。')]:
 loc(f'nesnd_per.{i}.a',opt);ev+=event(f'nesnd_per.{i}',title,desc,f'option = {{ name = nesnd_per.{i}.a default_option = yes }}',trigger='exists = scope:nesnd_per_claim_region' if i in [6,7] else '')
put('events/nesnd_per_campaign.txt',ev)
append_history('common/history/countries/per - persia.txt','nesnd_per_initialize')
flush_loc();print('Persian domestic journals, routes, aid events and bounded claim actions generated.')
