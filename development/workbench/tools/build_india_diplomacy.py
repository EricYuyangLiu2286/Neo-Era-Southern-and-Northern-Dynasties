from india_context import *
values=''
for k in ['serial','kind','quote']:
 values+=f'nesnd_india_request_{k} = {{ value = 0 if = {{ limit = {{ has_variable = nesnd_india_request_{k} }} value = var:nesnd_india_request_{k} }} }}\n'
values+='''nesnd_india_incoming_kind = { value = 0 if = { limit = { exists = scope:india_sender } value = scope:india_sender.nesnd_india_request_kind } }
nesnd_india_grant = { value = net_fixed_income multiply = 4 min = 25000 max = 125000 }
nesnd_india_regime = {
 value = 0
 if = { limit = { has_law = law_type:law_council_republic } value = 6 }
 else_if = { limit = { has_law = law_type:law_theocracy } value = 7 }
 else_if = { limit = { OR = { has_law = law_type:law_presidential_republic has_law = law_type:law_parliamentary_republic } } value = 4 }
 else_if = { limit = { country_has_monarchy_law = yes }
  value = 5
  if = { limit = { exists = ruler }
   if = { limit = { ruler = { has_variable = house_bonaparte } } value = 1 }
   else_if = { limit = { ruler = { has_variable = house_orleans } } value = 2 }
   else_if = { limit = { ruler = { OR = { has_variable = house_bourbon has_variable = house_bourbon_leader has_variable = legitimist_leader } } } value = 3 }
  }
 }
}
'''
put('common/script_values/nesnd_india_diplomacy.txt',values)
triggers='''nesnd_india_diplomacy_live = { OR = { nesnd_india_empire = yes nesnd_india_prince = yes } }
nesnd_india_can_send = {
 nesnd_india_diplomacy_live = yes is_at_war = no is_active_in_diplomatic_play = no
 NOT = { has_variable = nesnd_india_request_clock } NOT = { has_variable = nesnd_india_request_cooldown }
 NOT = { has_variable = nesnd_external_pending } NOT = { has_variable = nesnd_external_cooldown }
}
nesnd_india_french_contact = {
 nesnd_india_can_send = yes
 NOT = { has_variable = nesnd_india_aid_lock } NOT = { has_variable = nesnd_external_aid_committed }
 trigger_if = { limit = { exists = c:FRA }
  NOT = { c:FRA = this } NOT = { has_war_with = c:FRA }
  c:FRA = { is_country_alive = yes is_at_war = no }
  OR = { is_subject = no is_subject_of = c:FRA }
 } trigger_else = { always = no }
}
nesnd_india_autonomy_available = {
 nesnd_india_can_send = yes
 trigger_if = { limit = { is_subject = yes exists = overlord }
  overlord = { is_country_alive = yes }
  NOT = { has_war_with = overlord }
 } trigger_else = { always = no }
}
nesnd_india_union_target = {
 nesnd_india_prince = yes is_subject = no is_at_war = no is_active_in_diplomatic_play = no
 NOT = { has_variable = nesnd_india_incoming_union_clock }
 NOT = { this = root } relations:root >= 25
 root = { is_subject = no }
}
nesnd_india_reply_valid = {
 trigger_if = { limit = {
  exists = scope:india_sender exists = scope:india_partner exists = scope:india_serial
  exists = scope:india_sender_patron exists = scope:india_partner_patron
  exists = scope:india_sender_regime exists = scope:india_partner_regime
 }
  this = scope:india_partner is_country_alive = yes is_at_war = no
  nesnd_india_regime = scope:india_partner_regime
  trigger_if = { limit = { is_subject = yes } overlord = scope:india_partner_patron } trigger_else = { this = scope:india_partner_patron }
  scope:india_sender = {
   nesnd_india_diplomacy_live = yes is_at_war = no
   has_variable = nesnd_india_request_clock
   nesnd_india_request_serial = scope:india_serial nesnd_india_regime = scope:india_sender_regime
   trigger_if = { limit = { exists = var:nesnd_india_request_partner } var:nesnd_india_request_partner = scope:india_partner } trigger_else = { always = no }
   NOT = { has_war_with = scope:india_partner }
   trigger_if = { limit = { is_subject = yes } overlord = scope:india_sender_patron } trigger_else = { this = scope:india_sender_patron }
   trigger_if = { limit = { nesnd_india_request_kind <= 3 }
    c:FRA = scope:india_partner NOT = { has_variable = nesnd_india_aid_lock } NOT = { has_variable = nesnd_external_aid_committed }
    OR = { is_subject = no is_subject_of = scope:india_partner }
   }
   trigger_if = { limit = { OR = { nesnd_india_request_kind = 4 nesnd_india_request_kind = 7 } } is_direct_subject_of = scope:india_partner }
   trigger_if = { limit = { nesnd_india_request_kind = 4 } can_increase_autonomy = yes }
   trigger_if = { limit = { nesnd_india_request_kind = 5 } is_subject = no scope:india_partner = { is_subject = no } }
   trigger_if = { limit = { nesnd_india_request_kind = 6 }
    nesnd_india_empire = yes is_subject = no has_variable = nesnd_india_reform_done nesnd_india_community >= 60
    scope:india_partner = { nesnd_india_prince = yes is_subject = no is_active_in_diplomatic_play = no
     trigger_if = { limit = { exists = var:nesnd_india_incoming_union_sender } var:nesnd_india_incoming_union_sender = scope:india_sender has_variable = nesnd_india_incoming_union_clock } trigger_else = { always = no }
    }
   }
  }
 } trigger_else = { always = no }
}
nesnd_india_defence_treaty_possible = {
 trigger_if = { limit = { exists = scope:india_sender exists = scope:india_partner }
 can_create_treaty = {
  first_country = scope:india_sender second_country = scope:india_partner is_draft = no
  binding_period = { years = 3 }
  articles_to_create = { { article = defensive_pact } }
 }
 } trigger_else = { always = no }
}
nesnd_india_reply_can_accept = {
 nesnd_india_reply_valid = yes
 trigger_if = { limit = { exists = scope:india_sender }
  trigger_if = { limit = { nesnd_india_incoming_kind <= 3 } gold_reserves >= scope:india_sender.nesnd_india_request_quote in_default = no NOT = { has_modifier = declared_bankruptcy } }
  trigger_if = { limit = { nesnd_india_incoming_kind = 5 } nesnd_india_defence_treaty_possible = yes }
  trigger_if = { limit = { nesnd_india_incoming_kind = 6 } scope:india_sender = { gold_reserves >= nesnd_india_request_quote } }
 } trigger_else = { always = no }
}
'''
put('common/scripted_triggers/nesnd_india_diplomacy.txt',triggers)
effects='''nesnd_india_clear_request = {
 if = { limit = { exists = var:nesnd_india_request_partner }
  save_scope_as = india_request_cleanup_owner
  var:nesnd_india_request_partner = {
   if = { limit = { exists = var:nesnd_india_incoming_union_sender }
    if = { limit = { var:nesnd_india_incoming_union_sender = scope:india_request_cleanup_owner } remove_variable = nesnd_india_incoming_union_sender remove_variable = nesnd_india_incoming_union_clock }
   }
  }
 }
 remove_variable = nesnd_india_request_clock remove_variable = nesnd_india_request_partner
 remove_variable = nesnd_india_request_kind remove_variable = nesnd_india_request_quote
}
nesnd_india_send_request = {
 if = { limit = { nesnd_india_can_send = yes exists = scope:india_partner }
  if = { limit = { scope:india_partner = { is_country_alive = yes } NOT = { this = scope:india_partner } NOT = { has_war_with = scope:india_partner } }
   save_scope_as = india_sender
   save_scope_value_as = { name = india_sender_regime value = nesnd_india_regime }
   if = { limit = { is_subject = yes } overlord = { save_scope_as = india_sender_patron } } else = { save_scope_as = india_sender_patron }
   scope:india_partner = {
    save_scope_value_as = { name = india_partner_regime value = nesnd_india_regime }
    if = { limit = { is_subject = yes } overlord = { save_scope_as = india_partner_patron } } else = { save_scope_as = india_partner_patron }
   }
   set_variable = { name = nesnd_india_request_serial value = { value = nesnd_india_request_serial add = 1 } }
   save_scope_value_as = { name = india_serial value = nesnd_india_request_serial }
   set_variable = { name = nesnd_india_request_kind value = $KIND$ }
   set_variable = { name = nesnd_india_request_partner value = scope:india_partner }
   set_variable = { name = nesnd_india_request_quote value = nesnd_india_grant }
   set_variable = { name = nesnd_india_request_clock days = 45 }
   set_variable = { name = nesnd_india_request_cooldown months = 6 }
   if = { limit = { nesnd_india_request_kind = 6 } scope:india_partner = { set_variable = { name = nesnd_india_incoming_union_sender value = scope:india_sender } set_variable = { name = nesnd_india_incoming_union_clock days = 45 } } }
   scope:india_partner = { trigger_event = { id = nesnd_india_diplomacy.1 days = 1 popup = yes } }
  }
 }
}
nesnd_india_refuse_request = {
 if = { limit = { nesnd_india_reply_valid = yes }
  scope:india_sender = {
   if = { limit = { OR = { nesnd_india_request_kind = 4 nesnd_india_request_kind = 7 } } add_liberty_desire = 10 }
   trigger_event = { id = nesnd_india_diplomacy.3 popup = yes }
   nesnd_india_clear_request = yes
  }
 }
}
nesnd_india_accept_request = {
 if = { limit = { nesnd_india_reply_can_accept = yes }
  if = { limit = { nesnd_india_incoming_kind <= 3 }
   add_treasury = { value = scope:india_sender.nesnd_india_request_quote multiply = -1 }
   scope:india_sender = {
    add_treasury = nesnd_india_request_quote
    add_modifier = { name = nesnd_india_french_advisers months = 48 }
    set_variable = { name = nesnd_india_aid_lock months = 48 }
    set_variable = { name = nesnd_india_adviser_partner value = scope:india_partner }
    if = { limit = { is_subject = yes } set_variable = { name = nesnd_india_adviser_patron value = overlord } } else = { set_variable = { name = nesnd_india_adviser_patron value = this } }
    if = { limit = { nesnd_india_request_kind = 1 } add_modifier = { name = nesnd_india_french_teachers months = 48 } }
    else_if = { limit = { nesnd_india_request_kind = 2 } add_modifier = { name = nesnd_india_french_engineers months = 48 } }
    else = { add_modifier = { name = nesnd_india_french_officers months = 48 } }
   }
  }
  else_if = { limit = { nesnd_india_incoming_kind = 4 } scope:india_sender = { increase_autonomy = yes add_liberty_desire = -20 } }
  else_if = { limit = { nesnd_india_incoming_kind = 7 } scope:india_sender = { make_independent = yes create_bidirectional_truce = { country = scope:india_partner months = 60 } } }
  else_if = { limit = { nesnd_india_incoming_kind = 5 }
   create_treaty = { first_country = scope:india_sender second_country = scope:india_partner is_draft = no binding_period = { years = 3 } articles_to_create = { { article = defensive_pact } } }
  }
  if = { limit = { nesnd_india_incoming_kind = 6 }
   scope:india_sender = {
    add_treasury = { value = nesnd_india_request_quote multiply = -1 }
    add_modifier = { name = nesnd_india_princely_pensions months = 120 }
    nesnd_india_inherit_partner = yes
    nesnd_india_clear_request = yes
    annex = scope:india_partner
    nesnd_india_refresh = yes
   }
  }
  else = { scope:india_sender = { change_relations = { country = scope:india_partner value = 25 } trigger_event = { id = nesnd_india_diplomacy.2 popup = yes } nesnd_india_clear_request = yes } }
 }
}
nesnd_india_remove_advisers = {
 remove_modifier = nesnd_india_french_advisers remove_modifier = nesnd_india_french_teachers remove_modifier = nesnd_india_french_engineers remove_modifier = nesnd_india_french_officers
 remove_variable = nesnd_india_adviser_partner remove_variable = nesnd_india_adviser_patron
}
nesnd_india_diplomacy_maintenance = {
 if = { limit = { has_variable = nesnd_india_request_partner NOT = { has_variable = nesnd_india_request_clock } } nesnd_india_clear_request = yes }
 if = { limit = { has_variable = nesnd_india_incoming_union_sender NOT = { has_variable = nesnd_india_incoming_union_clock } } remove_variable = nesnd_india_incoming_union_sender }
 if = { limit = { has_variable = nesnd_india_adviser_partner }
  if = { limit = { exists = var:nesnd_india_adviser_partner exists = var:nesnd_india_adviser_patron }
   if = { limit = { OR = {
    NOT = { has_modifier = nesnd_india_french_advisers }
    has_war_with = var:nesnd_india_adviser_partner
    AND = { is_subject = yes NOT = { overlord = var:nesnd_india_adviser_patron } }
    AND = { is_subject = no NOT = { this = var:nesnd_india_adviser_patron } }
   } } nesnd_india_remove_advisers = yes }
  } else = { nesnd_india_remove_advisers = yes }
 }
}
nesnd_india_inherit_partner = {
'''
for done in ['schools','industry','reform','caste','unified']:
 effects+=f' if = {{ limit = {{ scope:india_partner = {{ has_variable = nesnd_india_{done}_done }} }} set_variable = nesnd_india_{done}_done }}\n'
effects+=''' scope:india_partner = { nesnd_india_clear_request = yes nesnd_india_remove_advisers = yes }
}
'''
put('common/scripted_effects/nesnd_india_diplomacy.txt',effects)
mods='''nesnd_india_french_advisers = { country_government_wages_mult = 0.05 }
nesnd_india_french_teachers = { state_education_access_add = 0.05 state_pop_qualifications_mult = 0.15 }
nesnd_india_french_engineers = { building_tooling_workshop_throughput_add = 0.1 building_steel_mill_throughput_add = 0.1 state_construction_mult = 0.1 }
nesnd_india_french_officers = { unit_offense_mult = 0.1 unit_defense_mult = 0.1 }
nesnd_india_princely_pensions = { country_government_wages_mult = 0.05 }
''';put('common/static_modifiers/nesnd_india_diplomacy.txt',mods)
texts={
'nesnd_india_foreign':('借法自强','Strength Through French Assistance'),
'nesnd_india_foreign_reason':('法国人并非为印度的独立而来。然而，借来的知识仍可以成为自己的力量。朝廷可以请来教师、工程师或军官；他们是否动身，要看巴黎愿意为这段关系付出多少。','France has not come to secure India’s independence. Yet borrowed knowledge can become a strength of our own. Teachers, engineers and officers may be invited; whether they come depends on what Paris is prepared to invest in the relationship.'),
'nesnd_india_foreign_status':('援助与自主之间，需要自己的打算。','Foreign assistance calls for a policy of our own.'),
'nesnd_india_diplomatic_desc':('向对方正式提出请求，由其政府作答。','Submit a formal request for the other government to consider.'),
'nesnd_india_request_tt':('请求将交给对方决定。六个月后可再次交涉；法国援助获准后四年内不可再次领取。','The other government will decide. Another approach may be made in six months; accepted French assistance cannot be claimed again for four years.'),
'nesnd_india_union_request_tt':('向一国提出并入印度的条件。对方可拒绝；同意后支付安置费，并承担十年的王公年金开支。','Offer one state terms for joining India. It may refuse. Acceptance requires a settlement payment and ten years of princely pensions.'),
'nesnd_india_french_advisers':('法国顾问团','French Advisers'),
'nesnd_india_french_teachers':('法国教师','French Teachers'),
'nesnd_india_french_engineers':('法国工程师','French Engineers'),
'nesnd_india_french_officers':('法国教官','French Officers'),
'nesnd_india_princely_pensions':('王公年金','Princely Pensions'),
'nesnd_india_diplomacy.1.t':('印度使团','An Indian Delegation'),
'nesnd_india_diplomacy.1.d':('[SCOPE.sCountry(\'india_sender\').GetName]的使者已带来正式请求。双方的交往并不意味着无条件的支持；我们有权决定愿意承担怎样的责任。','An envoy from [SCOPE.sCountry(\'india_sender\').GetName] has brought a formal proposal. Our existing relations do not commit us to unconditional support. We must decide what responsibility we are prepared to accept.'),
'nesnd_india_diplomacy.1.a':('接受这些条件。','Accept these terms.'),
'nesnd_india_diplomacy.1.b':('我们不能答应。','We cannot agree.'),
'nesnd_india_diplomacy.2.t':('使者归来','The Envoy Returns'),
'nesnd_india_diplomacy.2.d':('[SCOPE.sCountry(\'india_partner\').GetName]接受了我们的请求。约定已交付执行，接下来仍要靠本国将它变为成果。','[SCOPE.sCountry(\'india_partner\').GetName] has accepted our request. The agreement is now in effect; making good use of it falls to us.'),
'nesnd_india_diplomacy.3.t':('未获应允','The Request Declined'),
'nesnd_india_diplomacy.3.d':('[SCOPE.sCountry(\'india_partner\').GetName]拒绝了使团提出的条件。我们仍须寻找自己的出路。','[SCOPE.sCountry(\'india_partner\').GetName] has declined the delegation’s terms. We must seek another way forward.'),
'nesnd_india_diplomacy_ack':('知道了。','Understood.'),
'nesnd_india_reply_aid_tt':('提供一笔拨款及四年的专业援助。受援国承担顾问费用；双方交战或受援国改投其他宗主后，顾问撤离。','Provide a grant and four years of specialist assistance. The recipient pays the advisers’ expenses. The mission withdraws if the countries go to war or the recipient changes its overlord.'),
'nesnd_india_reply_autonomy_tt':('提高对方一级自治权。','Increase the recipient’s autonomy by one level.'),
'nesnd_india_reply_independence_tt':('承认对方独立，缔结五年停战。','Recognise independence and establish a five-year truce.'),
'nesnd_india_reply_union_tt':('本国并入对方，原有土地与人民成为统一国家的一部分。','Our state will join the other country, bringing its lands and people into the union.'),
'nesnd_india_reply_defence_tt':('缔结防御条约，约束期三年。','Conclude a defensive pact with a three-year binding period.'),
}
labels={1:('延请法国教师','Invite French Teachers'),2:('延请法国工程师','Invite French Engineers'),3:('延请法国教官','Invite French Officers'),4:('商议自治','Negotiate Autonomy'),7:('请求独立','Request Independence'),6:('邀请土邦加入','Invite a Princely State')}
buttons=[]
for kind,pair in labels.items():
 key='nesnd_india_request_'+str(kind);texts[key]=pair
 if kind<=3:ready='nesnd_india_french_contact = yes';selection='c:FRA = { save_scope_as = india_partner }'
 elif kind in [4,7]:ready='nesnd_india_autonomy_available = yes'+(' can_increase_autonomy = yes' if kind==4 else '');selection='overlord = { save_scope_as = india_partner }'
 else:ready='nesnd_india_can_send = yes nesnd_india_empire = yes is_subject = no has_variable = nesnd_india_reform_done nesnd_india_community >= 60 any_country = { nesnd_india_union_target = yes }';selection='ordered_country = { limit = { nesnd_india_union_target = yes } order_by = total_population position = 0 check_range_bounds = no save_scope_as = india_partner }'
 visible='nesnd_india_diplomacy_live = yes'
 if kind in [4,7]:visible+=' is_subject = yes'
 if kind==6:visible+=' nesnd_india_empire = yes has_variable = nesnd_india_reform_done'
 tip='nesnd_india_union_request_tt' if kind==6 else 'nesnd_india_request_tt'
 buttons.append(f'''{key} = {{ name = {key} desc = nesnd_india_diplomatic_desc visible = {{ {visible} }} possible = {{ {ready} }} ai_chance = {{ value = {'2' if kind==7 else '5'} }} effect = {{ custom_tooltip = {tip} hidden_effect = {{ if = {{ limit = {{ {ready} }} clear_saved_scope = india_partner {selection} nesnd_india_send_request = {{ KIND = {kind} }} }} }} }} }}''')
for tag in ['FRA','MUG','USM']:
 key='nesnd_india_defence_'+tag.lower();texts[key]=('与$'+tag+'$商议互保','Seek a Defensive Pact with $'+tag+'$')
 ready=f'nesnd_india_can_send = yes is_subject = no exists = c:{tag} NOT = {{ c:{tag} ?= this }} c:{tag} ?= {{ is_subject = no is_at_war = no }}'
 buttons.append(f'''{key} = {{ name = {key} desc = nesnd_india_diplomatic_desc visible = {{ nesnd_india_prince = yes is_subject = no exists = c:{tag} }} possible = {{ {ready} }} ai_chance = {{ value = 2 }} effect = {{ custom_tooltip = nesnd_india_request_tt hidden_effect = {{ if = {{ limit = {{ {ready} }} c:{tag} = {{ save_scope_as = india_partner }} nesnd_india_send_request = {{ KIND = 5 }} }} }} }} }}''')
put('common/scripted_buttons/nesnd_india_diplomacy.txt','\n'.join(buttons))
put('common/journal_entries/nesnd_india_diplomacy.txt','''nesnd_india_foreign = { icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_diplomacy_live = yes exists = c:FRA } possible = { nesnd_india_diplomacy_live = yes exists = c:FRA }
 scripted_button = nesnd_india_request_1 scripted_button = nesnd_india_request_2 scripted_button = nesnd_india_request_3
 invalid = { OR = { NOT = { nesnd_india_diplomacy_live = yes } NOT = { exists = c:FRA } } }
 on_invalid = { nesnd_india_clear_request = yes }
 status_desc = { desc = nesnd_india_foreign_status } weight = 400
}''')
# Original event template: same snapshot checks on display, reply, AI and execution.
ev='''namespace = nesnd_india_diplomacy
nesnd_india_diplomacy.1 = {
 type = country_event title = nesnd_india_diplomacy.1.t
 desc = { first_valid = {
'''
for k in [1,2,3,4,5,6,7]:
 ev+=f' triggered_desc = {{ trigger = {{ nesnd_india_incoming_kind = {k} }} desc = nesnd_india_diplomacy.1.d{k} }}\n'
 evdesc={1:('教师','teachers'),2:('矿业和工业的工程师','mining and industrial engineers'),3:('军队教官','military instructors')}
 if k<=3:cn,en=evdesc[k];texts[f'nesnd_india_diplomacy.1.d{k}']=(f"[SCOPE.sCountry('india_sender').GetName]希望我们派遣{cn}，并帮助支付初期的费用。这个国家需要新知识，法国也有自己的利益；接受请求意味着投入真实的经费与人员。",f"[SCOPE.sCountry('india_sender').GetName] asks us to send {en} and help cover the initial costs. The country needs new expertise, while France has interests of its own. Acceptance will require a real commitment of money and personnel.")
 else:
  cnen={4:('提高自治权','greater autonomy'),5:('共同防御的条约','a defensive pact'),6:('以年金保障原有王公，并入共同的印度国家','union within an Indian state, with pensions for the ruling princes'),7:('承认独立','recognition of independence')};cn,en=cnen[k];texts[f'nesnd_india_diplomacy.1.d{k}']=(f"[SCOPE.sCountry('india_sender').GetName]的使者提出了{cn}的要求。这将改变两国今后的关系，我们可以接受，也可以保留现状。",f"The delegation from [SCOPE.sCountry('india_sender').GetName] proposes {en}. This would change our relationship. We may accept or retain the present arrangement.")
ev+=''' desc = nesnd_india_diplomacy.1.d } }
 duration = 1 trigger = { nesnd_india_reply_valid = yes } cancellation_trigger = { NOT = { nesnd_india_reply_valid = yes } }
 option = { name = nesnd_india_diplomacy.1.a show_as_unavailable = { always = yes } trigger = { nesnd_india_reply_can_accept = yes }
 ai_chance = { base = 30
  modifier = { trigger = { nesnd_india_reply_valid = yes nesnd_india_regime = 1 nesnd_india_incoming_kind = 3 } add = 40 }
  modifier = { trigger = { nesnd_india_reply_valid = yes nesnd_india_regime = 2 nesnd_india_incoming_kind = 2 } add = 40 }
  modifier = { trigger = { nesnd_india_reply_valid = yes nesnd_india_regime = 3 nesnd_india_incoming_kind = 1 scope:india_sender = { country_has_monarchy_law = yes } } add = 30 }
  modifier = { trigger = { nesnd_india_reply_valid = yes OR = { nesnd_india_regime = 4 nesnd_india_regime = 6 } nesnd_india_incoming_kind = 1 } add = 40 }
  modifier = { trigger = { nesnd_india_reply_valid = yes relations:scope:india_sender >= 50 } add = 25 }
  modifier = { trigger = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind = 6 } factor = 0.25 }
  modifier = { trigger = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind = 7 } factor = 0.25 }
 }
 if = { limit = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind <= 3 } custom_tooltip = nesnd_india_reply_aid_tt show_as_tooltip = { add_treasury = { value = scope:india_sender.nesnd_india_request_quote multiply = -1 } } }
 if = { limit = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind = 4 } custom_tooltip = nesnd_india_reply_autonomy_tt }
 if = { limit = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind = 5 } custom_tooltip = nesnd_india_reply_defence_tt }
 if = { limit = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind = 6 } custom_tooltip = nesnd_india_reply_union_tt }
 if = { limit = { nesnd_india_reply_valid = yes nesnd_india_incoming_kind = 7 } custom_tooltip = nesnd_india_reply_independence_tt }
 hidden_effect = { nesnd_india_accept_request = yes }
 }
 option = { name = nesnd_india_diplomacy.1.b default_option = yes ai_chance = { base = 70 } hidden_effect = { nesnd_india_refuse_request = yes } }
}
'''
for k in [2,3]:ev+=f'''nesnd_india_diplomacy.{k} = {{ type = country_event title = nesnd_india_diplomacy.{k}.t desc = nesnd_india_diplomacy.{k}.d trigger = {{ exists = scope:india_partner }} cancellation_trigger = {{ NOT = {{ exists = scope:india_partner }} }} option = {{ name = nesnd_india_diplomacy_ack default_option = yes }} }}\n'''
put('events/nesnd_india_diplomacy.txt',ev);loc(texts)
p=C/'common/scripted_effects/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_refresh');s=s[:n.vend-1]+''' nesnd_india_diplomacy_maintenance = yes
 if = { limit = { nesnd_india_diplomacy_live = yes exists = c:FRA NOT = { has_journal_entry = nesnd_india_foreign } } add_journal_entry = { type = nesnd_india_foreign } }
'''+s[n.vend-1:];write(p,s)
p=C/'common/journal_entries/nesnd_india_core.txt';s=read(p)
for key in ['nesnd_india_reform','nesnd_india_princes','nesnd_india_society']:
 n=parse(s).get(key);insert=' scripted_button = nesnd_india_request_4 scripted_button = nesnd_india_request_7\n'
 if key=='nesnd_india_princes':insert+=' scripted_button = nesnd_india_defence_fra scripted_button = nesnd_india_defence_mug scripted_button = nesnd_india_defence_usm\n'
 if key=='nesnd_india_society':insert+=' scripted_button = nesnd_india_request_6\n'
 s=s[:n.vend-1]+insert+s[n.vend-1:]
write(p,s)
# Mutual exclusion with the old aid channel. Preserve all existing actual treaties.
p=C/'common/scripted_triggers/nesnd_external_triggers.txt';s=read(p)
for key in ['nesnd_external_can_request_aid','nesnd_external_can_request_money','nesnd_external_can_request_arms']:
 n=parse(s).get(key)
 if n:s=s[:n.vstart+1]+'\n NOT = { has_variable = nesnd_india_request_clock } NOT = { has_variable = nesnd_india_aid_lock }\n'+s[n.vstart+1:]
write(p,s)
dump(R/'diplomacy-implementation.json',{'request_kinds':7,'snapshots':['serial','both_regimes','both_patrons','partner'],'reply_days':45,'event_duration_months':1,'cooldown_months':6,'aid_lock_months':48,'grant_weeks_fixed_income':4,'grant_bounds':[25000,125000],'game_launched':False})
print('India diplomacy implemented; source and lifecycle tests pending')
