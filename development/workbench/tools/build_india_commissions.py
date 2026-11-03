from india_context import *
configs=[('tianzhu','TZ1','MADRAS','CIRCARS KURNOOL MADRAS MYSORE TRAVANCORE GUJARAT CEYLON INDIAN_OCEAN_TERRITORY'.split(),'天竺','Tianzhu','purple'),('yuanshan','YU1','ZULULAND','CAPE_COLONY EASTERN_CAPE NORTHERN_CAPE ZULULAND ORANJE TRANSVAAL'.split(),'远山','Yuanshan','orange')]
texts={};defs=[];names=[];flags=[];coa=[];triggers=[];effects=[];buttons=[];jes=[];decisions=[]
# Conditional technology inheritance only on actual creation, no invented copy-tech interface.
techs={}
for rootdir in [G,C]:
 for p in (rootdir/'common/technology/technologies').glob('*.txt'):
  for n in parse(read(p)).children:techs[n.key]=n
tech='nesnd_commission_inherit_technology = {\n'+''.join(f' if = {{ limit = {{ c:USM = {{ has_technology_researched = {t} }} NOT = {{ has_technology_researched = {t} }} }} add_technology_researched = {t} }}\n' for t in techs)+'}\n'
effects.append(tech)
for slug,tag,capital,states,cn,en,color in configs:
 defs.append(f'''{tag} = {{ color = {{ {'118 93 154' if tag=='TZ1' else '135 104 69'} }} country_type = colonial tier = principality cultures = {{ ce_wuu min }} religion = confucian capital = STATE_{capital} {'social_hierarchy = british_indian_caste_system' if tag=='TZ1' else ''} }}''')
 names.append(f'''{tag} = {{ dynamic_country_name = {{ name = nesnd_{slug}_commission_name adjective = {tag}_ADJ is_main_tag_only = yes priority = 100 trigger = {{ trigger_if = {{ limit = {{ exists = scope:actor exists = c:USM }} scope:actor = {{ is_subject_of = c:USM }} }} trigger_else = {{ always = no }} }} }} }}''')
 flags.append(f'{tag} = {{ flag_definition = {{ coa = {tag} subject_canton = {tag} allow_overlord_canton = yes priority = 1 }} }}')
 coa.append(f'{tag} = {{ pattern = "pattern_solid.tga" color1 = "{color}" color2 = "yellow" colored_emblem = {{ texture = "ce_ming.dds" color1 = "yellow" instance = {{ position = {{ 0.5 0.5 }} scale = {{ 0.65 0.65 }} }} }} }}')
 owned='OR = { '+' '.join('state_region = s:STATE_'+st for st in states)+' }'
 triggers.append(f'''nesnd_{slug}_region = {{ {owned} }}
nesnd_{slug}_commission_available = {{ c:USM ?= this NOT = {{ has_variable = nesnd_{slug}_commission_established }} NOT = {{ exists = c:{tag} }} }}
nesnd_{slug}_commission_ready = {{
 nesnd_{slug}_commission_available = yes is_subject = no is_at_war = no is_active_in_diplomatic_play = no
 has_technology_researched = democracy
 NOT = {{ has_variable = nesnd_{slug}_commission_cooldown }}
 exists = s:STATE_{capital}.region_state:USM
 s:STATE_{capital}.region_state:USM ?= {{ state_population > 0 any_scope_building = {{ is_building_type = building_port level >= 1 }} }}
 any_scope_state = {{ count >= 2 nesnd_{slug}_region = yes is_largest_state_in_region = yes state_population > 0 }}
 any_scope_state = {{ nesnd_{slug}_region = yes any_scope_building = {{ is_building_type = building_government_administration level >= 1 }} }}
}}
nesnd_{slug}_governance_live = {{ c:{tag} ?= this is_country_alive = yes any_scope_state = {{ nesnd_{slug}_region = yes }} NOT = {{ has_variable = nesnd_commission_governance_done }} }}
''')
 hierarchy='set_social_hierarchy = british_indian_caste_system activate_law = law_type:law_hindu_caste_not_enforced' if tag=='TZ1' else 'set_social_hierarchy = default_social_hierarchy'
 effects.append(f'''nesnd_establish_{slug}_commission = {{
 if = {{ limit = {{ nesnd_{slug}_commission_ready = yes }}
  set_variable = {{ name = nesnd_{slug}_commission_cooldown months = 12 }}
  create_country = {{ tag = {tag} origin = c:USM state = s:STATE_{capital}.region_state:USM on_created = {{
   set_country_type = colonial {hierarchy} set_variable = nesnd_commission_created
   nesnd_commission_inherit_technology = yes copy_laws = c:USM
   activate_law = law_type:law_presidential_republic activate_law = law_type:law_autocracy {hierarchy}
   set_capital = s:STATE_{capital}
  }} }}
  if = {{ limit = {{ exists = c:{tag} }}
   create_diplomatic_pact = {{ country = c:{tag} type = puppet }}
   if = {{ limit = {{ c:{tag} = {{ is_subject_of = c:USM }} }}
'''+''.join(f'    if = {{ limit = {{ exists = s:STATE_{st}.region_state:USM }} s:STATE_{st}.region_state:USM = {{ set_state_owner = c:{tag} }} }}\n' for st in states if st!=capital)+f'''
    set_variable = nesnd_{slug}_commission_established
    c:{tag} = {{ if = {{ limit = {{ NOT = {{ has_journal_entry = nesnd_{slug}_governance }} }} add_journal_entry = {{ type = nesnd_{slug}_governance }} }} }}
   }}
   else = {{
    # Creation succeeded but the actual subject relationship failed. Only its seed may return.
    if = {{ limit = {{ exists = s:STATE_{capital}.region_state:{tag} c:{tag} = {{ num_states = 1 has_variable = nesnd_commission_created }} }}
     s:STATE_{capital}.region_state:{tag} = {{ set_state_owner = c:USM }}
    }}
   }}
  }}
 }}
}}
''')
 buttons.append(f'''nesnd_establish_{slug}_button = {{ name = nesnd_establish_{slug} desc = nesnd_establish_{slug}_desc
 visible = {{ nesnd_{slug}_commission_available = yes }} possible = {{ nesnd_{slug}_commission_ready = yes }}
 ai_chance = {{ value = 5 }}
 effect = {{ custom_tooltip = nesnd_establish_{slug}_tt hidden_effect = {{ nesnd_establish_{slug}_commission = yes }} }}
}}''')
 decisions.append(f'''nesnd_establish_{slug} = {{ is_shown = {{ nesnd_{slug}_commission_available = yes }} possible = {{ nesnd_{slug}_commission_ready = yes }} when_taken = {{ custom_tooltip = nesnd_establish_{slug}_tt hidden_effect = {{ nesnd_establish_{slug}_commission = yes }} }} ai_chance = {{ value = 5 }} }}''')
 jes.append(f'''nesnd_{slug}_commission = {{ icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content
 is_shown_when_inactive = {{ nesnd_{slug}_commission_available = yes any_scope_state = {{ nesnd_{slug}_region = yes }} }}
 possible = {{ nesnd_{slug}_commission_available = yes any_scope_state = {{ nesnd_{slug}_region = yes }} }}
 scripted_button = nesnd_establish_{slug}_button
 complete = {{ has_variable = nesnd_{slug}_commission_established }}
 invalid = {{ OR = {{ NOT = {{ c:USM ?= this }} NOT = {{ any_scope_state = {{ nesnd_{slug}_region = yes }} }} }} }}
 weight = 500
}}
nesnd_{slug}_governance = {{ icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = {{ nesnd_{slug}_governance_live = yes }} possible = {{ nesnd_{slug}_governance_live = yes }}
 complete = {{ hidden_trigger = {{ nesnd_{slug}_governance_live = yes }}
 institution_investment_level = {{ institution = institution_schools value >= 1 }} literacy_rate >= 0.2
 country_has_building_type_levels = {{ target = bt:building_port value >= 3 }}
 country_has_building_type_levels = {{ target = bt:building_government_administration value >= 5 }}
 bureaucracy >= 0
 }}
 on_complete = {{ if = {{ limit = {{ nesnd_{slug}_governance_live = yes }} set_variable = nesnd_commission_governance_done add_modifier = {{ name = nesnd_commission_governance_reward months = 120 }} }} }}
 invalid = {{ NOT = {{ nesnd_{slug}_governance_live = yes }} }}
 weight = 650
}}
''')
 texts.update({tag:(cn,en),tag+'_ADJ':(cn,en),'nesnd_'+slug+'_commission_name':(cn+'宣慰司',en+' Pacification Commission'),'nesnd_establish_'+slug:('设立'+cn+'宣慰司','Establish the '+en+' Commission'),'nesnd_establish_'+slug+'_desc':('将'+cn+'的领地交由中央委任的宣慰使治理。','Place our '+en+' possessions under a commissioner appointed by the central government.'),'nesnd_establish_'+slug+'_tt':('将本国在'+('印度' if tag=='TZ1' else '南非')+'指定地区的实有领土划归'+cn+'宣慰司，建立[concept_puppet]关系。其他国家及其领土不变。','Transfer our possessions in the designated '+('Indian' if tag=='TZ1' else 'South African')+' states to the '+en+' Commission as a [concept_puppet].'),'nesnd_'+slug+'_commission':('筹建'+cn+'宣慰司','A Commission for '+en),'nesnd_'+slug+'_commission_reason':(('印度的领地与南京相隔万里。驻军和商人需要一个能在当地作出决定的官署，朝廷也需要一个能为这些决定负责的人。','Our Indian possessions lie far from Nanjing. The garrisons and merchants need an authority able to act locally, and the court needs someone it can hold responsible.') if tag=='TZ1' else ('远山的港口面向两洋，也是南朝船队进入非洲腹地的起点。只有真正取得并经营这片土地，朝廷才能在那里设立自己的宣慰司。','Yuanshan’s ports face two oceans and offer our fleets a foothold in southern Africa. A commission can be established only after we have secured and developed possessions there.')),'nesnd_'+slug+'_governance':(cn+'的庶务','Governing '+en),'nesnd_'+slug+'_governance_reason':('任命到达之后，学校、港口与税务仍需逐一办妥。宣慰使必须使地方的收入能够支持治理，而不能只依赖南京的命令。','An appointment does not provide schools, ports or a working revenue service. The commissioner must establish an administration that can support itself rather than rely on orders from Nanjing.')})
for folder,body in [('country_definitions',defs),('dynamic_country_names',names),('flag_definitions',flags),('coat_of_arms/coat_of_arms',coa),('scripted_triggers',triggers),('scripted_effects',effects),('scripted_buttons',buttons),('journal_entries',jes),('decisions',decisions)]:put('common/'+folder+'/nesnd_commissions.txt','\n'.join(body))
put('common/static_modifiers/nesnd_commissions.txt','nesnd_commission_governance_reward = { country_bureaucracy_mult = 0.1 state_education_access_add = 0.05 state_tax_capacity_mult = 0.1 }')
texts['nesnd_commission_governance_reward']=('地方行政渐备','An Established Administration');loc(texts)
# Refresh simply reaches applicable entries; all completed flags persist.
p=C/'common/scripted_effects/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_refresh');tail=''
for slug,tag,cap,states,cn,en,col in configs:
 tail+=f' if = {{ limit = {{ nesnd_{slug}_commission_available = yes any_scope_state = {{ nesnd_{slug}_region = yes }} NOT = {{ has_journal_entry = nesnd_{slug}_commission }} }} add_journal_entry = {{ type = nesnd_{slug}_commission }} }}\n'
 tail+=f' if = {{ limit = {{ nesnd_{slug}_governance_live = yes NOT = {{ has_journal_entry = nesnd_{slug}_governance }} }} add_journal_entry = {{ type = nesnd_{slug}_governance }} }}\n'
s=s[:n.vend-1]+tail+s[n.vend-1:];write(p,s)
p=C/'common/on_actions/nesnd_india_core.txt';s=read(p).replace('nesnd_india_country = yes c:USM ?= this','nesnd_india_country = yes c:USM ?= this c:YU1 ?= this c:TZ1 ?= this');write(p,s)
p=C/'common/scripted_triggers/nesnd_india_core.txt';write(p,read(p).replace('law_type:law_caste_not_enforced','law_type:law_hindu_caste_not_enforced'))
dump(R/'commissions-implementation.json',{'tags':['TZ1','YU1'],'techs_conditionally_inherited':len(techs),'create_armies':False,'create_pops':False,'third_country_states_affected':False,'engine_verified':False})
print('Two commission routes written, conditional technology count',len(techs))
