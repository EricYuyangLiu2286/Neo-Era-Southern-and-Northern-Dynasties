from india_context import *
# Safe numeric accessors; pre-init previews get zero, never read missing variables.
vars=['nesnd_india_priority','nesnd_india_schools_months','nesnd_india_industry_months','nesnd_india_case_stage','nesnd_india_case_progress','nesnd_india_case_retries']
for p in list((C/'common').rglob('nesnd_india*.txt')):
 if p.parent.name=='script_values':continue
 s=read(p)
 for v in vars:s=s.replace('var:'+v,v+'_value')
 write(p,s)
append('common/script_values/nesnd_india_core.txt','\n'.join(f'{v}_value = {{ value = 0 if = {{ limit = {{ has_variable = {v} }} value = var:{v} }} }}' for v in vars))
# Contextless native is explicitly added by global history.
p=C/'common/journal_entries/zzzz_nesnd_india_native.txt';s=read(p);n=parse(s).get('je_uneasy_raj');part=s[n.start:n.end].replace('je_group_historical_content','je_group_global_international_situations');write(p,s[:n.start]+part+s[n.end:])
# Alias originally incorrectly documented in source research, now verified against game.
p=C/'common/scripted_triggers/nesnd_india_uprising.txt';s=read(p);n=parse(s).get('nesnd_india_colonial_owner');replacement='''nesnd_india_colonial_owner = {
 OR = { c:USM ?= this AND = { c:TZ1 ?= this trigger_if = { limit = { exists = c:USM } is_subject_of = c:USM } trigger_else = { always = no } } }
}''';write(p,s[:n.start]+replacement+s[n.end:])
# Industry may use the functioning common market for inputs; real domestic arsenals/railways remain goals.
p=C/'common/scripted_triggers/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_industry_ready');part=s[n.start:n.end]
for building,amount,good in [('coal_mine',15,'coal'),('iron_mine',15,'iron'),('tooling_workshop',15,'tools'),('steel_mill',5,'steel')]:
 old=f'country_has_building_type_levels = {{ target = bt:building_{building} value >= {amount} }}'
 new=f'''OR = {{ {old} trigger_if = {{ limit = {{ exists = capital }} capital.market = {{ mg:{good} = {{ market_goods_pricier <= 0.25 NOT = {{ country_has_local_shortage = root }} }} }} }} trigger_else = {{ always = no }} }}'''
 assert old in part;part=part.replace(old,new)
s=s[:n.start]+part+s[n.end:]
s=s.replace('OR = { has_law = law_type:law_hindu_caste_not_enforced has_law = law_type:law_affirmative_action }','OR = { has_social_hierarchy = default_social_hierarchy has_law = law_type:law_hindu_caste_not_enforced has_law = law_type:law_affirmative_action }');write(p,s)
# Adviser maintenance uses actual branching before optional overlord lookup.
p=C/'common/scripted_effects/nesnd_india_diplomacy.txt';s=read(p);s=s.replace('AND = { is_subject = yes NOT = { overlord = var:nesnd_india_adviser_patron } }','AND = { trigger_if = { limit = { is_subject = yes } NOT = { overlord = var:nesnd_india_adviser_patron } } trigger_else = { always = no } }');write(p,s)
p=C/'common/scripted_triggers/nesnd_india_diplomacy.txt';s=read(p).replace('c:FRA = scope:india_partner NOT =','trigger_if = { limit = { exists = c:FRA } c:FRA = scope:india_partner } trigger_else = { always = no } NOT =');write(p,s)
p=C/'events/nesnd_india_diplomacy.txt';s=read(p);s=s.replace('scope:india_sender = { country_has_monarchy_law = yes }','trigger_if = { limit = { exists = scope:india_sender } scope:india_sender = { country_has_monarchy_law = yes } } trigger_else = { always = no }').replace('relations:scope:india_sender >= 50','trigger_if = { limit = { exists = scope:india_sender } relations:scope:india_sender >= 50 } trigger_else = { always = no }');write(p,s)
# Recruitment count is a literal integer in the native formation schema.
p=C/'common/scripted_effects/nesnd_india_uprising.txt';s=read(p)
for n in sorted([n for n in parse(s).walk() if n.key=='create_military_formation'],key=lambda n:n.start,reverse=True):
 old=s[n.start:n.end];repl='if = { limit = { exists = scope:india_recruit_count }\n'
 for i,num in enumerate([2,4,6,8]):repl+=('if' if i==0 else 'else_if')+f' = {{ limit = {{ scope:india_recruit_count = {num} }} '+old.replace('count = scope:india_recruit_count','count = '+str(num))+' }\n'
 repl+='}';s=s[:n.start]+repl+s[n.end:]
# Pull progress arithmetic out of global cleanup: the sponsor JE is its single monthly writer.
start=s.index('     if = { limit = { nesnd_india_case_stage_value = 1 }')
end=s.index('    } else = { nesnd_india_close_case = yes }',start)
block=s[start:end]
assert s.count(block)==6
s=s.replace(block,'     # The sponsoring JE advances preparation; this global pulse only checks ownership and lifecycle.\n')
# Recruitment source snapshot and dirty-territory guard for exact rollback.
s=s.replace('set_variable = nesnd_india_revolt_actor set_variable =','set_variable = nesnd_india_revolt_actor set_variable =')
s=s.replace('nesnd_india_case_stage value = 4 } set_variable', 'nesnd_india_case_stage value = 4 } set_variable')
s=s.replace('save_scope_value_as = { name = india_recruit_count','set_variable = { name = nesnd_india_case_original_provinces value = scope:india_case_state.num_provinces }\n   save_scope_value_as = { name = india_recruit_count')
# On creation before any subsequent transfers, store exact source province count on the newborn country.
s=s.replace('set_variable = nesnd_india_local_state set_variable = nesnd_india_revolt_actor','set_variable = nesnd_india_local_state set_variable = nesnd_india_revolt_actor remove_variable = nesnd_india_revolt_territory_changed')
s=s.replace('num_states = 1 has_variable = nesnd_india_revolt_actor is_at_war = no is_active_in_diplomatic_play = no','num_states = 1 has_variable = nesnd_india_revolt_actor NOT = { has_variable = nesnd_india_revolt_territory_changed } is_at_war = no is_active_in_diplomatic_play = no')
# Guard original numeric count used after creation (case region owns snapshot).
for region,tag in [('CIRCARS','IR1'),('KURNOOL','IR2'),('MADRAS','IR3'),('MYSORE','IR4'),('TRAVANCORE','IR5'),('GUJARAT','IR6')]:
 old=f'if = {{ limit = {{ c:{tag} = {{ num_states = 1'
 new=f'if = {{ limit = {{ has_variable = nesnd_india_case_original_provinces s:STATE_{region}.region_state:{tag} = {{ num_provinces = prev.var:nesnd_india_case_original_provinces }} c:{tag} = {{ num_states = 1'
 s=s.replace(old,new)
write(p,s)
# Guard each newly saved scope before using its RHS. All repeated case implementations are handled structurally.
def wrap_tail(rel,fn,needle,conditions):
 p=C/rel;s=read(p);n=parse(s).get(fn);body=s[n.start:n.end];at=body.index(needle)
 # needle lies inside a scope block; find smallest enclosing block and wrap from there to its closing brace.
 absat=n.start+at
 parents=[x for x in n.walk() if x.children is not None and x.vstart<absat<x.vend]
 parent=min(parents,key=lambda x:x.vend-x.vstart)
 tail=s[absat:parent.vend-1]
 replacement='if = { limit = { '+conditions+' }\n'+tail+'\n}\n'
 write(p,s[:absat]+replacement+s[parent.vend-1:])
# At request send all self references are root; saved aliases are checked before dependent recipient writes.
wrap_tail('common/scripted_effects/nesnd_india_diplomacy.txt','nesnd_india_send_request','scope:india_partner = {\n    save_scope_value_as','exists = scope:india_sender exists = scope:india_partner exists = scope:india_sender_patron exists = scope:india_sender_regime')
# Event scope serial/patrons carry real values only after explicit saves.
wrap_tail('common/scripted_effects/nesnd_india_diplomacy.txt','nesnd_india_send_request','set_variable = { name = nesnd_india_request_kind','exists = scope:india_serial exists = scope:india_partner_patron exists = scope:india_partner_regime')
for region in ['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT']:
 slug=region.lower();rel='common/scripted_effects/nesnd_india_uprising.txt'
 wrap_tail(rel,'nesnd_india_'+slug+'_start','s:STATE_'+region+' = {','exists = scope:india_sponsor')
 wrap_tail(rel,'nesnd_india_'+slug+'_start','set_variable = { name = nesnd_india_case_state','exists = scope:india_case_state exists = scope:india_case_owner')
 wrap_tail(rel,'nesnd_india_'+slug+'_create_play','add_claim = scope:india_case_owner','exists = scope:india_case_region exists = scope:india_case_owner exists = scope:india_case_local')
 wrap_tail(rel,'nesnd_india_'+slug+'_launch','s:STATE_'+region+' = {','exists = scope:india_sponsor')
 wrap_tail(rel,'nesnd_india_'+slug+'_launch','set_variable = { name = nesnd_india_case_stage value = 4','exists = scope:india_case_state exists = scope:india_case_owner')
# Use single writable progression, alongside safe read-only UI components.
append('common/scripted_triggers/nesnd_india_uprising.txt','''nesnd_india_case_unrest = { OR = { turmoil >= 0.15 average_sol < 10 } }
nesnd_india_case_can_advance = {
 trigger_if = { limit = { exists = var:nesnd_india_case_state exists = var:nesnd_india_case_sponsor }
  nesnd_india_case_stage_value = 1
  var:nesnd_india_case_state = { nesnd_india_case_unrest = yes state_population >= 300000 }
  var:nesnd_india_case_sponsor = { in_default = no NOT = { has_modifier = declared_bankruptcy } is_at_war = no }
 } trigger_else = { always = no }
}
''')
append('common/script_values/nesnd_india_core.txt','''nesnd_india_contact_progress = { value = 0 if = { limit = { exists = var:nesnd_india_contact_region } value = var:nesnd_india_contact_region.nesnd_india_case_progress_value } }
nesnd_india_case_organisation = { value = 0 if = { limit = { nesnd_india_case_can_advance = yes } add = 1 } }
nesnd_india_case_unrest_growth = { value = 0 if = { limit = { nesnd_india_case_can_advance = yes } if = { limit = { var:nesnd_india_case_state = { turmoil >= 0.25 } } add = 2 } } }
nesnd_india_case_transport = { value = 0 if = { limit = { nesnd_india_case_can_advance = yes } if = { limit = { var:nesnd_india_case_state = { market_access >= 0.5 } } add = 1 } } }
nesnd_india_case_foreign_training = { value = 0 if = { limit = { nesnd_india_case_can_advance = yes } if = { limit = { var:nesnd_india_case_sponsor = { has_modifier = nesnd_india_french_officers } } add = 1 } } }
nesnd_india_case_decay = { value = 0 if = { limit = { nesnd_india_case_stage_value = 2 } add = -2 } }
nesnd_india_case_monthly = { value = 0 add = nesnd_india_case_organisation add = nesnd_india_case_unrest_growth add = nesnd_india_case_transport add = nesnd_india_case_foreign_training add = nesnd_india_case_decay }
''')
bar='nesnd_india_contact_bar = { name = nesnd_india_contact_bar desc = nesnd_india_contact_bar default_green = yes start_value = 0 min_value = 0 max_value = 100 monthly_progress = {\n'
for part in ['organisation','unrest_growth','transport','foreign_training','decay']:
 bar+=f' add = {{ desc = nesnd_india_case_{part} value = {{ value = 0 if = {{ limit = {{ owner = {{ exists = var:nesnd_india_contact_region }} }} value = owner.var:nesnd_india_contact_region.nesnd_india_case_{part} }} }} }}\n'
bar+='} }';append('common/scripted_progress_bars/nesnd_india_core.txt',bar)
append('common/scripted_effects/nesnd_india_uprising.txt','''nesnd_india_advance_contact = {
 if = { limit = { exists = var:nesnd_india_contact_region }
  var:nesnd_india_contact_region = {
   if = { limit = { has_variable = nesnd_india_case_stage has_variable = nesnd_india_case_progress nesnd_india_case_stage_value <= 3 }
    change_variable = { name = nesnd_india_case_progress add = nesnd_india_case_monthly }
    clamp_variable = { name = nesnd_india_case_progress min = 0 max = 100 }
    if = { limit = { nesnd_india_case_progress_value >= 100 } set_variable = { name = nesnd_india_case_stage value = 3 } var:nesnd_india_case_sponsor ?= { remove_modifier = nesnd_india_contact_cost } }
   }
  }
 }
 if = { limit = { has_journal_entry = nesnd_india_uprising } je:nesnd_india_uprising = { set_bar_progress = { name = nesnd_india_contact_bar value = root.nesnd_india_contact_progress } } }
}
nesnd_india_migrate_commission_case = {
 if = { limit = { has_variable = nesnd_india_case_stage exists = var:nesnd_india_case_owner exists = c:USM exists = c:TZ1 }
  if = { limit = { nesnd_india_case_stage_value <= 3 var:nesnd_india_case_owner = c:USM }
   clear_saved_scope = india_transferred_case_state
   random_scope_state = { limit = { owner = c:TZ1 } save_scope_as = india_transferred_case_state }
   if = { limit = { exists = scope:india_transferred_case_state }
    set_variable = { name = nesnd_india_case_state value = scope:india_transferred_case_state }
    set_variable = { name = nesnd_india_case_owner value = c:TZ1 }
   }
  }
 }
}
''')
p=C/'common/journal_entries/nesnd_india_uprising.txt';s=read(p);n=parse(s).get('nesnd_india_uprising');s=s[:n.vend-1]+''' scripted_progress_bar = nesnd_india_contact_bar
 on_monthly_pulse = { effect = { nesnd_india_advance_contact = yes } }
'''+s[n.vend-1:];write(p,s)
# Exact state dirty flag prevents same-region merger rollback. Conservative ambiguous changes stay as diplomatic outcomes.
append('common/on_actions/nesnd_india_uprising.txt','''on_state_owner_change = { on_actions = { nesnd_india_revolt_territory_changed } }
on_state_created = { on_actions = { nesnd_india_revolt_territory_changed } }
nesnd_india_revolt_territory_changed = { effect = {
 owner ?= { if = { limit = { has_variable = nesnd_india_revolt_actor } set_variable = nesnd_india_revolt_territory_changed } }
} }
''')
# Seed transfer + remaining USM states all complete before migrating stable-region preparation records.
p=C/'common/scripted_effects/nesnd_commissions.txt';s=read(p);needle='set_variable = nesnd_tianzhu_commission_established';assert needle in s
s=s.replace(needle,''.join(f's:STATE_{r} = {{ nesnd_india_migrate_commission_case = yes }}\n' for r in ['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT'])+needle);write(p,s)
# TZ1 retains its own persistent provincial journal after the finite governance award.
p=C/'common/scripted_triggers/nesnd_india_core.txt';s=read(p).replace('nesnd_india_usm_live = { c:USM ?= this','nesnd_india_usm_live = { OR = { c:USM ?= this AND = { c:TZ1 ?= this nesnd_india_colonial_owner = yes } }');write(p,s)
p=C/'common/scripted_buttons/nesnd_india_uprising.txt';s=read(p)
for n in sorted([x for x in parse(s).children if x.key.endswith('_launch')],key=lambda x:x.start,reverse=True):
 pos=n.get('possible');slug=n.key.removeprefix('nesnd_india_').removesuffix('_launch');s=s[:pos.start]+f'possible = {{ nesnd_india_{slug}_launch_ready = yes }}'+s[pos.end:]
write(p,s)
# Launch needs a live local grievance as well as the accumulated organisation.
p=C/'common/scripted_triggers/nesnd_india_uprising.txt';s=read(p).replace('nesnd_india_colonial_state = yes owner = prev.var:nesnd_india_case_owner','nesnd_india_colonial_state = yes nesnd_india_case_unrest = yes owner = prev.var:nesnd_india_case_owner');write(p,s)
# Add missing native DP localization and source labels.
texts={'nesnd_india_contact_bar':('当地筹备','Local Preparation'),'nesnd_india_case_organisation':('秘密组织','Local organisation'),'nesnd_india_case_unrest_growth':('地方失序','Local turmoil'),'nesnd_india_case_transport':('交通与市场联系','Transport and market links'),'nesnd_india_case_foreign_training':('教官与训练','Officers and training'),'nesnd_india_case_decay':('联络中断','Suspended contact')}
for slug in ['circars','kurnool','madras','mysore','travancore','gujarat']:
 texts['dp_nesnd_india_'+slug+'_desc']=('要求收复本次起义占据的地区。','Demand the return of the state held by this rising.')
 texts['dp_nesnd_india_'+slug+'_tooltip']=('以收复本州为目标，允许谈判结束战争。','A play to recover this state, allowing a negotiated peace.')
loc(texts)
# Branch-neutral narration remains true after the player's own republican option and capital movement.
for lang in ['simp_chinese','english']:
 p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzzz_nesnd_india_l_{lang}.yml';s=read(p)
 replacements={
 'nesnd_india_contact_tt':('支付£5,000联络费用，政府工资增加2%。当地存在严重失序或生活水平低于10时，组织才能发展；交通、失序程度和法国教官影响筹备速度。暂停后不再支付维护费，筹备每月减少2。','Pay £5,000 and increase government wage costs by 2%. Organisation grows where turmoil is high or living standards are below 10. Transport, the extent of unrest and French officers affect its pace. Pausing ends maintenance and loses 2 preparation each month.'),
 'nesnd_india_society_reason':('生活在同一个国家里，不代表人们已经把彼此看作同胞。各省有自己的语言、信仰和旧日王公。随着学校与城市的发展，他们开始讨论谁有权代表印度。王朝、地方领袖和新兴的国民力量，都必须回答这个问题。','Living under one government does not make its subjects a nation. The provinces have their own languages, faiths and princes. As schools and cities grow, their inhabitants are asking who can speak for India. Dynasties, local leaders and the emerging national movement must each offer an answer.'),
 'nesnd_india_reform_reason':('莫卧儿的旧帝国曾靠君主的声望维系各省，如今的统治者却必须面对新的问题。法国商人与教官带来了财富和新式兵器，也带来了新的债主。国家需要自己的学校和工场，让地方的赋税变成能够保卫它的力量。','The old Mughal empire relied on the prestige of its sovereigns to bind the provinces together. Its rulers now face different demands. French merchants and officers have brought wealth and new weapons, along with new creditors. The state needs schools and workshops of its own to turn provincial revenues into the means to defend it.'),
 }
 for k,pair in replacements.items():v=pair[0 if lang=='simp_chinese' else 1];s=re.sub(r'(?m)^(\s*'+re.escape(k)+r':\d*\s+)".*"$',lambda m:m[1]+'"'+v+'"',s)
 write(p,s)
print('First review corrections applied; external checks follow')
