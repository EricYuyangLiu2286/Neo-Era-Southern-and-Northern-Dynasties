from india_context import *
rows=[('CIRCARS','IR1','telegu','西尔卡斯','Circars'),('KURNOOL','IR2','telegu','库尔努尔','Kurnool'),('MADRAS','IR3','tamil','马德拉斯','Madras'),('MYSORE','IR4','kannada','迈索尔','Mysore'),('TRAVANCORE','IR5','malayalam','特拉凡哥尔','Travancore'),('GUJARAT','IR6','gujarati','古吉拉特','Gujarat')]
# Names represent newly organised inhabitants of the transferred colonial segment; existing princes retain their states.
texts={
'nesnd_india_uprising':('南方的烽火','Fire in the South'),
'nesnd_india_uprising_reason':('南朝的统治依靠港口、驻军和愿意合作的地方势力。反对者同样需要组织、经费与盟友。德里可以帮助他们行动，却不能因此把他们的土地视作自己的奖赏。','The Southern Court relies on ports, garrisons and local allies to sustain its rule. Its opponents also need organisation, money and friends. Delhi can assist them without treating their lands as its reward.'),
'nesnd_india_uprising_status':('地方的行动尚待时机。','Local resistance awaits its opportunity.'),
'nesnd_india_contact_desc':('资助当地的反殖民组织，为公开举事作准备。','Support local opponents of colonial rule as they prepare to rise.'),
'nesnd_india_contact_tt':('支付£5,000联络费用。筹备每月推进5，政府工资增加2%；每次只能支持一处。暂停后不再支付维护费，筹备每月减少2。','Pay £5,000 to establish contact. Preparation gains 5 each month at a 2% government wage cost. Only one region may be sponsored at a time. Pausing ends this cost and loses 2 preparation each month.'),
'nesnd_india_pause_tt':('暂停联络并撤去维护开支；当地组织每月损失2筹备。','Suspend contact and its maintenance cost. Local preparation falls by 2 each month.'),
'nesnd_india_resume_tt':('恢复联络与维护开支；不再支付首次联络费。','Resume contact and maintenance without paying the initial fee again.'),
'nesnd_india_launch_tt':('支付£20,000支持举事。当地将成立自己的国家，殖民统治者要求收复本州，起义者以羞辱对方为反诉求。独立的赞助国加入起义一方；资助不会自动使当地并入本国。','Pay £20,000 to support the rising. A local state is formed. Its former ruler demands the return of this state; the insurgents demand humiliation. An independent sponsor joins the insurgents. Sponsorship does not grant ownership of their land.'),
'nesnd_india_preparation_tt':('本地区的筹备已达100。','Preparation in this region has reached 100.'),
'nesnd_india_contact_cost':('南方联络经费','Southern Organisation Fund'),
'nesnd_india_revolt_war':('保卫地方自主','Defending Local Independence'),
'nesnd_india_revolt_war_reason':('旧统治者要求收回这片土地。独立的命运将由这场交涉与战争决定；外国资助不应成为另一个国家吞并我们的借口。','Our former ruler demands this land back. Negotiation and war will decide its independence. Foreign assistance must not become another country’s excuse to annex us.'),
'nesnd_india_revolt_resolved_tt':('本次起义的外交博弈与战争已经结束。','This rising’s diplomatic play and war have ended.'),
'nesnd_india_revolt_survived':('守住自主','Independence Preserved'),
'nesnd_india_suppression_desc':('以额外的警务开支打击地方秘密组织。','Devote additional policing resources to disrupting local organisations.'),
'nesnd_india_suppression_tt':('支付£10,000，使当地筹备减少25；六个月内不能再次采取同一行动。','Pay £10,000 to reduce local preparation by 25. This action cannot be repeated for six months.'),
'nesnd_india_revolt.1.t':('南方举事','A Rising in the South'),
'nesnd_india_revolt.1.d':("[SCOPE.sState('india_case_state').GetName]的反对者已经公开举事。他们占据地方官署，宣布不再服从旧统治者。现在，是否承认这场分离已成为两国之间的争端。","Opponents of colonial rule in [SCOPE.sState('india_case_state').GetName] have seized the local administration and declared their independence. Recognition of their breakaway government is now a dispute between states."),
'nesnd_india_revolt_ack':('局势已变。','The situation has changed.'),
}
triggers='''nesnd_india_colonial_owner = { OR = { c:USM ?= this AND = { c:TZ1 ?= this exists = c:USM is_subject_of = c:USM } } }
nesnd_india_uprising_strength = { nesnd_india_empire = yes has_variable = nesnd_india_reform_done has_technology_researched = nationalism OR = { is_subject = no AND = { army_size >= 60 government_legitimacy >= 50 } } }
nesnd_india_contact_safe = { nesnd_india_uprising_strength = yes is_at_war = no is_active_in_diplomatic_play = no NOT = { has_variable = nesnd_india_contact_region } }
nesnd_india_colonial_state = {
 state_population >= 300000 owner = { nesnd_india_colonial_owner = yes is_at_war = no is_active_in_diplomatic_play = no }
 controller = owner
}
'''
effects='''nesnd_india_contact_release_sponsor = {
 if = { limit = { exists = var:nesnd_india_case_sponsor }
  save_scope_as = india_cleanup_region
  var:nesnd_india_case_sponsor = {
   if = { limit = { exists = var:nesnd_india_contact_region }
    if = { limit = { var:nesnd_india_contact_region = scope:india_cleanup_region } remove_variable = nesnd_india_contact_region remove_modifier = nesnd_india_contact_cost }
   }
  }
 }
}
nesnd_india_close_case = {
 nesnd_india_contact_release_sponsor = yes
 remove_variable = nesnd_india_case_sponsor remove_variable = nesnd_india_case_owner remove_variable = nesnd_india_case_state
 remove_variable = nesnd_india_case_stage remove_variable = nesnd_india_case_progress remove_variable = nesnd_india_case_play remove_variable = nesnd_india_case_retries
 set_variable = { name = nesnd_india_case_cooldown months = 36 }
}
'''
buttons=[];defs=[];plays=[];cases=[];globalsteps='';coa=[];flags=[]
for region,tag,culture,cn,en in rows:
 slug=region.lower();r='s:STATE_'+region;dp='dp_nesnd_india_'+slug
 # Proven culture symbols are validated against effective data in final checker.
 defs.append(f'{tag} = {{ color = {{ 120 80 55 }} country_type = unrecognized tier = principality cultures = {{ {culture} }} religion = hindu capital = STATE_{region} social_hierarchy = british_indian_caste_system }}')
 coa.append(f'{tag} = {{ pattern = "pattern_solid.tga" color1 = "orange" color2 = "green" colored_emblem = {{ texture = "ce_ming.dds" color1 = "green" instance = {{ position = {{ 0.5 0.5 }} scale = {{ 0.4 0.4 }} }} }} }}')
 flags.append(f'{tag} = {{ flag_definition = {{ coa = {tag} priority = 1 }} }}')
 texts[tag]=(cn+'共和国',en+' Republic');texts[tag+'_ADJ']=(cn,en);texts[dp]=(cn+'起义',en+' Rising')
 triggers+=f'''nesnd_india_{slug}_target = {{
 NOT = {{ exists = c:{tag} }}
 {r} = {{ NOT = {{ has_variable = nesnd_india_case_stage }} NOT = {{ has_variable = nesnd_india_case_cooldown }} any_scope_state = {{ nesnd_india_colonial_state = yes }} }}
}}
nesnd_india_{slug}_our_case = {{
 {r} = {{ trigger_if = {{ limit = {{ exists = var:nesnd_india_case_sponsor has_variable = nesnd_india_case_stage }} var:nesnd_india_case_sponsor = root var:nesnd_india_case_stage <= 3 }} trigger_else = {{ always = no }} }}
}}
nesnd_india_{slug}_launch_ready = {{
 nesnd_india_uprising_strength = yes nesnd_india_{slug}_our_case = yes is_at_war = no is_active_in_diplomatic_play = no gold_reserves >= 20000
 NOT = {{ exists = c:{tag} }}
 {r} = {{
  trigger_if = {{ limit = {{ has_variable = nesnd_india_case_progress exists = var:nesnd_india_case_state exists = var:nesnd_india_case_owner }}
   var:nesnd_india_case_progress >= 100
   var:nesnd_india_case_state = {{ nesnd_india_colonial_state = yes owner = prev.var:nesnd_india_case_owner }}
   var:nesnd_india_case_owner = {{ NOT = {{ has_war_with = root }} NOT = {{ has_truce_with = root }} }}
  }} trigger_else = {{ always = no }}
 }}
}}
'''
 effects+=f'''nesnd_india_{slug}_start = {{
 if = {{ limit = {{ nesnd_india_contact_safe = yes nesnd_india_{slug}_target = yes gold_reserves >= 5000 }}
  add_treasury = -5000
  set_variable = {{ name = nesnd_india_contact_region value = {r} }}
  add_modifier = {{ name = nesnd_india_contact_cost }}
  save_scope_as = india_sponsor
  {r} = {{
   set_variable = {{ name = nesnd_india_case_sponsor value = scope:india_sponsor }}
   set_variable = {{ name = nesnd_india_case_progress value = 0 }}
   set_variable = {{ name = nesnd_india_case_stage value = 1 }}
   ordered_scope_state = {{ limit = {{ nesnd_india_colonial_state = yes }} order_by = state_population position = 0 check_range_bounds = no save_scope_as = india_case_state owner = {{ save_scope_as = india_case_owner }} }}
   set_variable = {{ name = nesnd_india_case_state value = scope:india_case_state }} set_variable = {{ name = nesnd_india_case_owner value = scope:india_case_owner }}
  }}
 }}
}}
nesnd_india_{slug}_create_play = {{
 if = {{ limit = {{ exists = var:nesnd_india_case_owner exists = c:{tag} exists = s:STATE_{region}.region_state:{tag} }}
  save_scope_as = india_case_region var:nesnd_india_case_owner = {{ save_scope_as = india_case_owner }}
  c:{tag} = {{ save_scope_as = india_case_local }}
  add_claim = scope:india_case_owner
  scope:india_case_owner = {{
   if = {{ limit = {{ is_at_war = no is_active_in_diplomatic_play = no NOT = {{ has_war_with = scope:india_case_local }} NOT = {{ has_truce_with = scope:india_case_local }} }}
    create_diplomatic_play = {{ name = {dp} type = {dp} target_country = scope:india_case_local target_state = s:STATE_{region}.region_state:{tag} escalation = 80
     add_war_goal = {{ holder = scope:india_case_local type = humiliation target_country = scope:india_case_owner primary_demand = yes }}
    }}
    clear_saved_scope = india_case_created_play
    random_diplomatic_play = {{ limit = {{ is_diplomatic_play_type = {dp} initiator = scope:india_case_owner target = scope:india_case_local }} save_scope_as = india_case_created_play }}
    if = {{ limit = {{ exists = scope:india_case_created_play }}
     scope:india_case_region = {{ set_variable = {{ name = nesnd_india_case_play value = scope:india_case_created_play }} set_variable = {{ name = nesnd_india_case_stage value = 5 }} }}
     scope:india_case_created_play = {{
      set_variable = {{ name = nesnd_india_revolt_region value = scope:india_case_region }}
      if = {{ limit = {{ scope:india_case_region = {{ exists = var:nesnd_india_case_sponsor }} }}
       scope:india_case_region.var:nesnd_india_case_sponsor = {{ if = {{ limit = {{ is_country_alive = yes is_subject = no is_at_war = no NOT = {{ this = scope:india_case_owner }} }} save_scope_as = india_case_backer }} }}
       if = {{ limit = {{ exists = scope:india_case_backer }} add_target_backers = {{ scope:india_case_backer }} }}
      }}
     }}
    }}
   }}
  }}
 }}
}}
nesnd_india_{slug}_launch = {{
 if = {{ limit = {{ nesnd_india_{slug}_launch_ready = yes }}
  save_scope_as = india_sponsor clear_saved_scope = india_case_backer
  {r} = {{
   var:nesnd_india_case_state = {{ save_scope_as = india_case_state }} var:nesnd_india_case_owner = {{ save_scope_as = india_case_owner }}
   set_variable = {{ name = nesnd_india_case_stage value = 4 }} set_variable = {{ name = nesnd_india_case_retries value = 0 }}
   save_scope_value_as = {{ name = india_recruit_count value = {{ value = 2 if = {{ limit = {{ scope:india_case_state = {{ state_population >= 1000000 }} }} value = 4 }} if = {{ limit = {{ scope:india_case_state = {{ state_population >= 3000000 }} }} value = 6 }} if = {{ limit = {{ scope:india_case_state = {{ state_population >= 6000000 }} }} value = 8 }} }} }}
   scope:india_case_owner = {{ create_country = {{ tag = {tag} origin = scope:india_case_owner state = scope:india_case_state on_created = {{
    set_variable = nesnd_india_local_state set_variable = nesnd_india_revolt_actor set_variable = {{ name = nesnd_india_revolt_origin value = {r} }}
    activate_law = law_type:law_presidential_republic activate_law = law_type:law_oligarchy set_social_hierarchy = british_indian_caste_system activate_law = law_type:law_hindu_caste_not_enforced
    if = {{ limit = {{ NOT = {{ has_technology_researched = democracy }} }} add_technology_researched = democracy }}
   }} }} }}
   if = {{ limit = {{ exists = c:{tag} }}
    scope:india_sponsor = {{ add_treasury = -20000 remove_modifier = nesnd_india_contact_cost }}
    c:{tag} = {{
     add_treasury = 20000
     if = {{ limit = {{ army_size < 1 NOT = {{ has_variable = nesnd_india_initial_recruitment }} }}
      set_variable = nesnd_india_initial_recruitment
      create_military_formation = {{ type = army hq_region = sr:region_{'north_india' if region=='GUJARAT' else 'south_india'} combat_unit = {{ type = unit_type:combat_unit_type_irregular_infantry state_region = s:STATE_{region} count = scope:india_recruit_count }} }}
     }}
     if = {{ limit = {{ NOT = {{ has_journal_entry = nesnd_india_revolt_war }} }} add_journal_entry = {{ type = nesnd_india_revolt_war }} }}
     trigger_event = {{ id = nesnd_india_revolt.1 popup = yes }}
    }}
    nesnd_india_{slug}_create_play = yes
   }} else = {{ nesnd_india_close_case = yes }}
  }}
 }}
}}
nesnd_india_{slug}_maintain = {{
 if = {{ limit = {{ has_variable = nesnd_india_case_stage }}
  if = {{ limit = {{ var:nesnd_india_case_stage <= 3 }}
   if = {{ limit = {{ exists = var:nesnd_india_case_sponsor exists = var:nesnd_india_case_owner exists = var:nesnd_india_case_state }}
    save_scope_as = india_case_region
    if = {{ limit = {{ var:nesnd_india_case_state = {{ owner = scope:india_case_region.var:nesnd_india_case_owner }} var:nesnd_india_case_owner = {{ nesnd_india_colonial_owner = yes }} var:nesnd_india_case_sponsor = {{ nesnd_india_uprising_strength = yes }} }}
     if = {{ limit = {{ var:nesnd_india_case_stage = 1 }}
      if = {{ limit = {{ var:nesnd_india_case_sponsor = {{ in_default = no NOT = {{ has_modifier = declared_bankruptcy }} is_at_war = no }} }} change_variable = {{ name = nesnd_india_case_progress add = 5 }} }}
      else = {{ set_variable = {{ name = nesnd_india_case_stage value = 2 }} var:nesnd_india_case_sponsor = {{ remove_modifier = nesnd_india_contact_cost }} }}
     }}
     else_if = {{ limit = {{ var:nesnd_india_case_stage = 2 }} change_variable = {{ name = nesnd_india_case_progress add = -2 }} }}
     clamp_variable = {{ name = nesnd_india_case_progress min = 0 max = 100 }}
     if = {{ limit = {{ var:nesnd_india_case_progress >= 100 }} set_variable = {{ name = nesnd_india_case_stage value = 3 }} var:nesnd_india_case_sponsor = {{ remove_modifier = nesnd_india_contact_cost }} }}
    }} else = {{ nesnd_india_close_case = yes }}
   }} else = {{ nesnd_india_close_case = yes }}
  }}
  else_if = {{ limit = {{ var:nesnd_india_case_stage = 4 }}
   change_variable = {{ name = nesnd_india_case_retries add = 1 }}
   if = {{ limit = {{ var:nesnd_india_case_retries <= 2 }} nesnd_india_{slug}_create_play = yes }}
   else = {{
    if = {{ limit = {{ exists = var:nesnd_india_case_owner exists = c:{tag} exists = s:STATE_{region}.region_state:{tag} }}
     if = {{ limit = {{ c:{tag} = {{ num_states = 1 has_variable = nesnd_india_revolt_actor is_at_war = no is_active_in_diplomatic_play = no }} }}
      var:nesnd_india_case_owner = {{ save_scope_as = india_case_original_owner }}
      s:STATE_{region}.region_state:{tag} = {{ set_state_owner = scope:india_case_original_owner }}
     }}
    }}
    c:{tag} ?= {{ set_variable = nesnd_india_revolt_resolved }}
    nesnd_india_close_case = yes
   }}
  }}
  else = {{
   if = {{ limit = {{ exists = var:nesnd_india_case_play }}
    if = {{ limit = {{ var:nesnd_india_case_play = {{ is_war = yes }} }} set_variable = {{ name = nesnd_india_case_stage value = 6 }} }}
   }} else = {{
    c:{tag} ?= {{ set_variable = nesnd_india_revolt_resolved }}
    nesnd_india_close_case = yes
   }}
  }}
 }}
}}
'''
 # Local-state contacts deliberately only foreign USM/TZ1 owner-state; no conquest of preexisting princes.
 for action in ['contact','pause','resume','launch']:
  key='nesnd_india_'+slug+'_'+action;texts[key]=({'contact':'联络','pause':'暂停','resume':'恢复联络：','launch':'支持举事：'}[action]+cn,{'contact':'Contact ','pause':'Suspend ','resume':'Resume Contact: ','launch':'Support the Rising: '}[action]+en)
  vis=f'nesnd_india_uprising_strength = yes '+(f'nesnd_india_{slug}_target = yes' if action=='contact' else f'nesnd_india_{slug}_our_case = yes')
  if action in ['pause','resume']:vis+=f' {r} = {{ var:nesnd_india_case_stage = {1 if action=="pause" else 2} }}'
  if action=='launch':vis+=f' {r} = {{ var:nesnd_india_case_stage = 3 }}'
  poss=f'nesnd_india_contact_safe = yes gold_reserves >= 5000' if action=='contact' else ('gold_reserves >= 20000 custom_tooltip = { text = nesnd_india_preparation_tt '+r+' = { var:nesnd_india_case_progress >= 100 } }' if action=='launch' else 'always = yes')
  if action in ['contact','launch']:execute=f'nesnd_india_{slug}_{"start" if action=="contact" else "launch"} = yes'
  else:execute=f'if = {{ limit = {{ {vis} }} {r} = {{ set_variable = {{ name = nesnd_india_case_stage value = {2 if action=="pause" else 1} }} }} '+('remove_modifier = nesnd_india_contact_cost' if action=='pause' else 'add_modifier = { name = nesnd_india_contact_cost }')+' }'
  buttons.append(f'''{key} = {{ name = {key} desc = nesnd_india_contact_desc visible = {{ {vis} }} possible = {{ {poss} }} ai_chance = {{ value = {'0' if action=='pause' else '5'} }} effect = {{ custom_tooltip = nesnd_india_{action}_tt hidden_effect = {{ {execute} }} }} }}''')
 key='nesnd_india_'+slug+'_suppress';texts[key]=('侦缉'+cn+'秘密组织','Disrupt Organisations in '+en)
 owning=f'{r} = {{ trigger_if = {{ limit = {{ exists = var:nesnd_india_case_owner has_variable = nesnd_india_case_stage }} var:nesnd_india_case_owner = root var:nesnd_india_case_stage <= 3 }} trigger_else = {{ always = no }} }}'
 buttons.append(f'''{key} = {{ name = {key} desc = nesnd_india_suppression_desc visible = {{ {owning} }} possible = {{ gold_reserves >= 10000 NOT = {{ has_variable = nesnd_india_suppression_cooldown }} }} ai_chance = {{ value = 15 }} effect = {{ custom_tooltip = nesnd_india_suppression_tt hidden_effect = {{ if = {{ limit = {{ {owning} gold_reserves >= 10000 NOT = {{ has_variable = nesnd_india_suppression_cooldown }} }} add_treasury = -10000 set_variable = {{ name = nesnd_india_suppression_cooldown months = 6 }} {r} = {{ change_variable = {{ name = nesnd_india_case_progress add = -25 }} clamp_variable = {{ name = nesnd_india_case_progress min = 0 max = 100 }} if = {{ limit = {{ var:nesnd_india_case_stage = 3 }} set_variable = {{ name = nesnd_india_case_stage value = 2 }} }} }} }} }} }} }}''')
 plays.append(f'''{dp} = {{ war_goal = return_state requires_interest_marker = no allow_negotiated_peace = yes mirror_war_goal = no initiator_can_add_war_goals = no target_can_add_war_goals = no add_infamy_for_starting_initiator_wargoals = no texture = "gfx/interface/icons/war_goals/return_state.dds" selectable_in_lens = {{ always = no }} possible = {{ }} ai_acceptance_max = 75 on_weekly_pulse = {{ }} on_war_begins = {{ }} on_war_end = {{ }} }}''')
 globalsteps+=f' {r} = {{ nesnd_india_{slug}_maintain = yes }}\n'
# Safe active goal: no permanently empty uprising JE, though territorial outcomes do not give an unearned reward.
triggers+='nesnd_india_uprising_available = { nesnd_india_uprising_strength = yes OR = { has_variable = nesnd_india_contact_region '+' '.join('nesnd_india_'+r.lower()+'_target = yes' for r,*_ in rows)+' } }\n'
for folder,body in [('country_definitions','\n'.join(defs)),('coat_of_arms/coat_of_arms','\n'.join(coa)),('flag_definitions','\n'.join(flags)),('diplomatic_plays','\n'.join(plays)),('scripted_triggers',triggers),('scripted_effects',effects),('scripted_buttons','\n'.join(buttons))]:put('common/'+folder+'/nesnd_india_uprising.txt',body)
put('common/on_actions/nesnd_india_uprising.txt','''on_monthly_pulse = { on_actions = { nesnd_india_global_cases } }
nesnd_india_global_cases = { effect = {
'''+globalsteps+'} }')
put('common/journal_entries/nesnd_india_uprising.txt','''nesnd_india_uprising = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_uprising_available = yes } possible = { nesnd_india_uprising_available = yes }
'''+''.join(' scripted_button = nesnd_india_'+r.lower()+'_'+a+'\n' for r,*_ in rows for a in ['contact','pause','resume','launch'])+'''
 invalid = { NOT = { nesnd_india_uprising_available = yes } }
 status_desc = { desc = nesnd_india_uprising_status } weight = 700
}
nesnd_india_revolt_war = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { has_variable = nesnd_india_revolt_actor NOT = { has_variable = nesnd_india_revolt_resolved } }
 possible = { has_variable = nesnd_india_revolt_actor NOT = { has_variable = nesnd_india_revolt_resolved } }
 complete = { custom_tooltip = { text = nesnd_india_revolt_resolved_tt has_variable = nesnd_india_revolt_resolved } num_states >= 1 }
 on_complete = { if = { limit = { NOT = { has_variable = nesnd_india_revolt_rewarded } } set_variable = nesnd_india_revolt_rewarded add_modifier = { name = nesnd_india_revolt_survived months = 60 } } }
 invalid = { NOT = { has_variable = nesnd_india_revolt_actor } }
 weight = 1000
}
''')
put('common/static_modifiers/nesnd_india_uprising.txt','nesnd_india_contact_cost = { country_government_wages_mult = 0.02 }\nnesnd_india_revolt_survived = { country_legitimacy_base_add = 10 country_prestige_mult = 0.1 }')
put('events/nesnd_india_revolt.txt','''namespace = nesnd_india_revolt
nesnd_india_revolt.1 = { type = country_event title = nesnd_india_revolt.1.t desc = nesnd_india_revolt.1.d trigger = { exists = scope:india_case_state } cancellation_trigger = { NOT = { exists = scope:india_case_state } } option = { name = nesnd_india_revolt_ack default_option = yes } }
''')
loc(texts)
p=C/'common/scripted_effects/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_refresh');s=s[:n.vend-1]+''' if = { limit = { nesnd_india_uprising_available = yes NOT = { has_journal_entry = nesnd_india_uprising } } add_journal_entry = { type = nesnd_india_uprising } }
'''+s[n.vend-1:];write(p,s)
p=C/'common/journal_entries/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_usm');s=s[:n.vend-1]+''.join(' scripted_button = nesnd_india_'+r.lower()+'_suppress\n' for r,*_ in rows)+s[n.vend-1:];write(p,s)
p=C/'common/journal_entries/nesnd_commissions.txt';s=read(p);n=parse(s).get('nesnd_tianzhu_governance');s=s[:n.vend-1]+''.join(' scripted_button = nesnd_india_'+r.lower()+'_suppress\n' for r,*_ in rows)+s[n.vend-1:];write(p,s)
dump(R/'uprising-implementation.json',{'regions':[r[0] for r in rows],'tags':[r[1] for r in rows],'existing_princes_untouched':True,'new_recruits':[2,4,6,8],'formation_only_if_zero_army':True,'sponsor_does_not_annex':True,'retry_limit':2,'rollback':'Only new one-state actor at peace with exact case state; otherwise diplomatic remainder.','game_launched':False})
print('Six regional uprising cases written; validation pending')
