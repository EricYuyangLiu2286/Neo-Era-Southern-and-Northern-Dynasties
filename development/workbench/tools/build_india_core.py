from india_context import *
# Pin current native files used by this first implementation batch.
sources=['common/history/countries/mug - mughals.txt','common/history/characters/mug - hindustan.txt','common/history/military_formations/05_military_formations_india.txt','common/scripted_effects/00_political_setup.txt','common/journal_entries/journal_entries.md','common/scripted_progress_bars/scripted_progress_bars.md','common/journal_entries/04_indian_federation.txt','common/journal_entries/00_sick_man.txt']
dump(R/'core-sources.json',{'version':'1.13.11','build':'24799966','files':{x:sha(G/x) for x in sources if (G/x).exists()},'differences':'Author MUG history owns initialization; no British national-chain or population replacement.'})
put('common/history/countries/mug - mughals.txt','# Native MUG history superseded by author mug - mongul.txt. Keep one initial legal/technology source.\nCOUNTRIES = { }')
put('common/history/characters/mug - hindustan.txt','''# Author Bahadur/Mirza remain sole ruler and heir. Retain unrelated native IG leaders.
CHARACTERS = { c:MUG ?= {
 create_character = { template = mug_raja_sohan_lal }
 create_character = { template = mug_hamid_ali_khan }
} }''')
p=C/'common/history/countries/mug - mongul.txt';s=read(p);n=parse(s).get('COUNTRIES').get('c:MUG');edits=[x for x in n.children if x.key in ['add_company','company:company_east_india_company']]
for x in sorted(edits,key=lambda x:x.start,reverse=True):s=s[:x.start]+s[x.end:]
write(p,s)
# Additional 37 battalions, alongside native Delhi3; no navy or runtime old-save reinforcements.
put('common/history/military_formations/nesnd_mughal_armies.txt','''MILITARY_FORMATIONS = { c:MUG ?= {
 create_military_formation = { type = army hq_region = sr:region_north_india name = nesnd_india_imperial_army
  combat_unit = { type = unit_type:combat_unit_type_irregular_infantry state_region = s:STATE_DELHI count = 12 }
  combat_unit = { type = unit_type:combat_unit_type_irregular_infantry state_region = s:STATE_AGRA count = 10 }
  combat_unit = { type = unit_type:combat_unit_type_irregular_infantry state_region = s:STATE_BIHAR count = 8 }
  combat_unit = { type = unit_type:combat_unit_type_hussars state_region = s:STATE_WEST_BENGAL count = 7 }
 }
} }''')
# Disable British national narratives narrowly. Specific contextless entry cannot execute country effects.
disabled=['je_uneasy_raj','je_sepoy_mutiny','je_mughal_hindustan','je_consolidate_colonial_rule','je_imperialism_of_promise','je_british_dictate_plantations','je_british_dictate_military','je_british_dictate_law','je_british_dictate_universities','je_india_home_rule','je_india_nationalism_britain','je_india_nationalism','je_india_non_cooperation_movement','je_communal_divides','je_dravidian_movement','je_federation_of_india','je_victoria_terminus','je_princely_states']
put('common/journal_entries/zzzz_nesnd_india_native.txt','\n'.join(f'''REPLACE:{x} = {{
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds"
 group = je_group_historical_content
 is_shown_when_inactive = {{ always = no }} possible = {{ always = no }} invalid = {{ always = yes }}
}}''' for x in disabled))
princes='ALW ASM AWA BAG BAS BER BHO BHV BHW BIK BUN COC COO DHA GAR GWA HYD IDA IND JAI JAS JEY JHN JOD JUN KHP KNO KOT KUT MEW MNP MYB NAG NAR NAW PAN PLP PTA PTN SAT SIN SUR TRA'.split()
regions='CIRCARS KURNOOL MADRAS MYSORE TRAVANCORE GUJARAT CEYLON INDIAN_OCEAN_TERRITORY'.split()
put('common/scripted_triggers/nesnd_india_core.txt','''nesnd_india_state = { OR = { region = sr:region_north_india region = sr:region_south_india } }
nesnd_india_country = { is_country_alive = yes NOT = { is_country_type = decentralized } any_scope_state = { nesnd_india_state = yes state_population > 0 } }
nesnd_india_empire = { nesnd_india_country = yes OR = { c:MUG ?= this c:BHT ?= this c:DRA ?= this has_variable = nesnd_india_imperial_line } }
nesnd_india_prince = { nesnd_india_country = yes NOT = { nesnd_india_empire = yes } OR = { '''+' '.join('c:'+x+' ?= this' for x in princes)+''' has_variable = nesnd_india_local_state } }
nesnd_india_reform_live = { nesnd_india_empire = yes NOT = { has_variable = nesnd_india_reform_done } }
nesnd_india_reform_safe = { bureaucracy >= 0 in_default = no NOT = { has_modifier = declared_bankruptcy } }
nesnd_india_schools_ready = {
 has_technology_researched = academia
 institution_investment_level = { institution = institution_schools value >= 2 }
 country_has_building_type_levels = { target = bt:building_university value >= 5 }
 country_has_building_type_levels = { target = bt:building_paper_mill value >= 8 }
 any_scope_building = { is_building_type = building_university level >= 3 occupancy >= 0.75 }
 literacy_rate >= 0.2
}
nesnd_india_industry_ready = {
 country_has_building_type_levels = { target = bt:building_coal_mine value >= 15 }
 country_has_building_type_levels = { target = bt:building_iron_mine value >= 15 }
 country_has_building_type_levels = { target = bt:building_tooling_workshop value >= 15 }
 country_has_building_type_levels = { target = bt:building_steel_mill value >= 5 }
 country_has_building_type_levels = { target = bt:building_arms_industry value >= 10 }
 country_has_building_type_levels = { target = bt:building_railway value >= 10 }
 any_scope_building = { is_building_type = building_arms_industry occupancy >= 0.75 weekly_profit > 0 }
 army_size >= 40
}
nesnd_india_society_live = { nesnd_india_empire = yes has_variable = nesnd_india_reform_done has_technology_researched = nationalism }
nesnd_india_caste_live = { nesnd_india_society_live = yes has_technology_researched = human_rights NOT = { has_variable = nesnd_india_caste_done } }
nesnd_india_caste_ready = {
 has_law = law_type:law_slavery_banned
 OR = { has_law = law_type:law_caste_not_enforced has_law = law_type:law_affirmative_action }
 OR = { has_law = law_type:law_freedom_of_conscience has_law = law_type:law_total_separation }
 institution_investment_level = { institution = institution_schools value >= 3 }
 literacy_rate >= 0.35
}
nesnd_india_usm_region = { OR = { '''+' '.join('state_region = s:STATE_'+x for x in regions)+''' } }
nesnd_india_usm_live = { c:USM ?= this any_scope_state = { nesnd_india_usm_region = yes state_population > 0 } }
''')
texts={
'nesnd_india_imperial_army':('印度帝国军','Army of Hindustan'),
'nesnd_india_reform':('德里的朝廷','The Court at Delhi'),
'nesnd_india_reform_reason':('德里仍是帝国的心脏，但君主的声望已经不足以维系这片土地。法国商人与教官带来了财富和新式兵器，也带来了新的债主。朝廷必须建立自己的学校和工场，让地方的赋税变成能够保卫国家的力量。','Delhi remains the heart of the empire, but royal prestige alone can no longer hold it together. French merchants and officers have brought wealth and new weapons, along with new creditors. Schools and workshops must turn the revenues of the provinces into the means to defend them.'),
'nesnd_india_reform_status':('朝廷正在筹办学校与工场。','The court is establishing schools and workshops.'),
'nesnd_india_schools':('学校与官署','Schools and Administration'),
'nesnd_india_schools_reason':('帝国需要能看懂账簿的官员，也需要能教会下一代读书的人。德里的一所学院无法代替各省的学校；纸张、教师与稳定的经费，必须一同送到地方。','The empire needs officials who can read its accounts and teachers who can educate the next generation. One college in Delhi cannot serve every province. Paper, teachers and regular funding must reach the districts together.'),
'nesnd_india_industry':('工场与军队','Workshops and Armies'),
'nesnd_india_industry_reason':('孟加拉的织物远销海外，帝国军队却仍仰赖旧式武备。矿井、工具厂和铁路将把这些分散的财富联系起来。朝廷的军工不必包办所有买卖，但不能只在名册上存在。','Bengali cloth reaches distant markets, yet the imperial army still relies on ageing equipment. Mines, toolworks and railways can bring these scattered resources together. The arsenals need not supply every purchase, but they must produce more than figures in a ledger.'),
'nesnd_india_school_service':('各省学务','Provincial Education'),
'nesnd_india_industrial_service':('帝国工场','Imperial Workshops'),
'nesnd_india_society':('王朝与印度','The Dynasty and India'),
'nesnd_india_society_reason':('同在帝国治下，不代表人们已经把彼此看作同胞。各省有自己的语言、信仰和旧日王公。随着学校与城市的发展，他们开始讨论谁有权代表印度。德里的君主可以参与这场变化，也可能被它抛在身后。','Living under one crown does not make its subjects a nation. The provinces have their own languages, faiths and princes. As schools and cities grow, their inhabitants are asking who can speak for India. The sovereign at Delhi may lead this change—or be left behind.'),
'nesnd_india_society_status':('各省正在寻找共同的政治归属。','The provinces are seeking a common political home.'),
'nesnd_india_dynasty_bar':('王朝接受度','Support for the Dynasty'),
'nesnd_india_community_bar':('印度共同体','An Indian Nation'),
'nesnd_india_dynasty_legitimacy':('朝廷的合法性','Legitimacy of the court'),
'nesnd_india_dynasty_religion':('宗教待遇','Religious policy'),
'nesnd_india_dynasty_dependence':('对法国的依赖','Dependence on France'),
'nesnd_india_community_education':('学校与识字','Schools and literacy'),
'nesnd_india_community_representation':('政治参与','Political representation'),
'nesnd_india_community_unrest':('失序与歧视','Unrest and discrimination'),
'nesnd_india_caste':('身份与公职','Birth and Public Office'),
'nesnd_india_caste_reason':('学校的大门已经打开，旧有身份仍决定着人们能够走多远。让军官与官员凭才干任职，需要改变成文法律，也需要把教育送到原先被排斥的家庭。','Schools have opened their doors, but inherited status still determines how far their pupils may rise. Appointing officers and officials by ability requires both new laws and education for families once excluded from it.'),
'nesnd_india_equal_service':('公职开放','Open Public Service'),
'nesnd_india_princes':('诸邦之间','Among the Princes'),
'nesnd_india_princes_reason':('德里、南京与巴黎都向印度诸邦递出了自己的条件。王公们所要保住的不只是祖传的宫殿，还有土地、税收和决定本国命运的权力。合作可以带来援助，却不一定带来自主。','Delhi, Nanjing and Paris each have terms to offer the Indian princes. Their rulers seek to preserve more than ancestral palaces: land, revenue and the right to decide their own future are at stake. Cooperation may bring assistance without securing independence.'),
'nesnd_india_princes_status':('本国的主权与地方利益仍待守护。','Our sovereignty and local interests must be defended.'),
'nesnd_india_usm':('天竺的土地','The Lands of Tianzhu'),
'nesnd_india_usm_reason':('南朝在印度的领地隔海相望，商人、驻军与地方王公各有利益。南京可以派遣官员直接治理，也可以把这些土地交给另设的宣慰司。无论采用何种制度，当地人的生计都不会因为一道任命而自行改善。','The Southern Court’s Indian possessions lie across the ocean, where merchants, garrisons and local princes pursue different interests. Nanjing may govern them directly or place them under a separate commission. Neither arrangement can improve local livelihoods by decree alone.'),
'nesnd_india_usm_status':('海路把天竺与南朝的市场联系起来。','Sea routes connect Tianzhu to the Southern Court’s market.'),
'nesnd_india_unified':('印度的新秩序','A New Order in India'),
'nesnd_india_unified_reason':('统一使许多边界从地图上消失，却没有消除各省的差别。新的国家必须把税收、教育与公共事务维持下去，让共同的法律在宫廷以外也具有意义。','Unification has erased borders without erasing differences between the provinces. The new state must sustain taxation, education and public services if its common laws are to mean anything beyond the court.'),
'nesnd_india_unified_reward':('共同的国家','A Common State'),
'nesnd_india_choose_schools':('先办学务','Prioritise Education'),
'nesnd_india_choose_industry':('先兴实业','Prioritise Industry'),
'nesnd_india_priority_desc':('将朝廷的人力与经费集中到这项事业上。','Concentrate the court’s staff and funding on this undertaking.'),
'nesnd_india_priority_tt':('将此事列为当前改革重点；另一项工作暂停，已取得的成果保留。','Make this our reform priority. The other programme pauses without losing its gains.'),
'nesnd_india_program_months':('持续达标月份','Months of Sustained Progress'),
'nesnd_india_ready_month':('建设与制度条件达标','Construction and institutions meet the requirements'),
'nesnd_india_dynastic_constitution':('共戴皇室','A Crown for India'),
'nesnd_india_republican_settlement':('印度属于国民','India Belongs to Its People'),
'nesnd_india_settlement_desc':('将各省共同的政治要求确立为国家的制度。','Give the provinces’ shared political demands a place in the constitution.'),
'nesnd_india_community_ready_tt':('印度共同体达到75。','An Indian Nation has reached 75.'),
'nesnd_india_dynasty_ready_tt':('王朝接受度达到60。','Support for the Dynasty has reached 60.'),
'nesnd_india_national_settlement':('印度的政治和解','An Indian Settlement'),
}
put('common/static_modifiers/nesnd_india_reform.txt','''nesnd_india_school_service = { state_education_access_add = 0.05 country_bureaucracy_mult = 0.1 }
nesnd_india_industrial_service = { building_tooling_workshop_throughput_add = 0.15 building_arms_industry_throughput_add = 0.15 }
nesnd_india_equal_service = { state_education_access_add = 0.05 interest_group_ig_intelligentsia_pop_attraction_mult = 0.15 }
nesnd_india_national_settlement = { country_legitimacy_base_add = 10 country_bureaucracy_mult = 0.1 }
nesnd_india_unified_reward = { country_bureaucracy_mult = 0.15 state_education_access_add = 0.05 country_prestige_mult = 0.1 }
''')
put('common/script_values/nesnd_india_core.txt','''nesnd_india_dynasty = { value = 0 if = { limit = { has_variable = nesnd_india_dynasty } value = var:nesnd_india_dynasty } }
nesnd_india_community = { value = 0 if = { limit = { has_variable = nesnd_india_community } value = var:nesnd_india_community } }
nesnd_india_dynasty_legitimacy = { value = 0 if = { limit = { country_has_monarchy_law = yes government_legitimacy >= 60 } add = 0.5 } else_if = { limit = { government_legitimacy < 25 } add = -0.5 } }
nesnd_india_dynasty_religion = { value = -0.25 if = { limit = { OR = { has_law = law_type:law_freedom_of_conscience has_law = law_type:law_total_separation } } value = 0.25 } }
nesnd_india_dynasty_dependence = { value = 0 if = { limit = { has_modifier = nesnd_india_french_advisers } add = -0.25 } }
nesnd_india_community_education = { value = 0 if = { limit = { literacy_rate >= 0.25 institution_investment_level = { institution = institution_schools value >= 2 } } add = 0.5 } }
nesnd_india_community_representation = { value = 0 if = { limit = { NOR = { has_law = law_type:law_autocracy has_law = law_type:law_oligarchy } } add = 0.5 } }
nesnd_india_community_unrest = { value = 0 if = { limit = { country_turmoil > 0.25 } add = -0.5 } if = { limit = { has_law = law_type:law_ethnostate } add = -0.5 } }
nesnd_india_dynasty_delta = { value = 0 add = nesnd_india_dynasty_legitimacy add = nesnd_india_dynasty_religion add = nesnd_india_dynasty_dependence }
nesnd_india_community_delta = { value = 0 add = nesnd_india_community_education add = nesnd_india_community_representation add = nesnd_india_community_unrest }
''')
triggers='';effects='';jes='';bars='';buttons=''
for kind,mod in [('schools','school_service'),('industry','industrial_service')]:
 done='nesnd_india_'+kind+'_done';var='nesnd_india_'+kind+'_months';prio=1 if kind=='schools' else 2
 triggers+=f'''nesnd_india_{kind}_available = {{ nesnd_india_reform_live = yes NOT = {{ has_variable = {done} }} trigger_if = {{ limit = {{ has_variable = nesnd_india_priority }} var:nesnd_india_priority = {prio} }} trigger_else = {{ always = no }} }}
'''
 effects+=f'''nesnd_india_{kind}_tick = {{
 if = {{ limit = {{ nesnd_india_{kind}_available = yes }}
  if = {{ limit = {{ NOT = {{ has_variable = {var} }} }} set_variable = {{ name = {var} value = 0 }} }}
  if = {{ limit = {{ nesnd_india_{kind}_ready = yes }} change_variable = {{ name = {var} add = 1 }} }}
  clamp_variable = {{ name = {var} min = 0 max = 12 }}
  journal_entry:nesnd_india_{kind} ?= {{ set_bar_progress = {{ bar = nesnd_india_{kind}_bar value = root.var:{var} }} }}
 }}
}}
'''
 jes+=f'''nesnd_india_{kind} = {{
 icon = "gfx/interface/icons/invention_icons/mechanical_tools.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = {{ nesnd_india_{kind}_available = yes }} possible = {{ nesnd_india_{kind}_available = yes }}
 immediate = {{ if = {{ limit = {{ NOT = {{ has_variable = {var} }} }} set_variable = {{ name = {var} value = 0 }} }} }}
 scripted_progress_bar = nesnd_india_{kind}_bar
 complete = {{ hidden_trigger = {{ nesnd_india_{kind}_available = yes }} nesnd_india_{kind}_ready = yes custom_tooltip = {{ text = nesnd_india_twelve_months_tt has_variable = {var} var:{var} >= 12 }} }}
 on_complete = {{ if = {{ limit = {{ nesnd_india_{kind}_available = yes }} set_variable = {done} add_modifier = {{ name = nesnd_india_{mod} months = 120 }} }} }}
 invalid = {{ NOT = {{ nesnd_india_{kind}_available = yes }} }}
 on_monthly_pulse = {{ effect = {{ nesnd_india_{kind}_tick = yes }} }}
 weight = 700
}}
'''
 bars+=f'''nesnd_india_{kind}_bar = {{ name = nesnd_india_program_months max_value = 12 start_value = 0
 monthly_progress = {{ add = {{ desc = nesnd_india_ready_month value = {{ value = 0 if = {{ limit = {{ owner = {{ nesnd_india_{kind}_available = yes nesnd_india_{kind}_ready = yes }} }} add = 1 }} }} }} }}
}}
'''
 buttons+=f'''nesnd_india_choose_{kind} = {{ name = nesnd_india_choose_{kind} desc = nesnd_india_priority_desc
 visible = {{ nesnd_india_reform_live = yes NOT = {{ has_variable = {done} }} NOT = {{ AND = {{ has_variable = nesnd_india_priority var:nesnd_india_priority = {prio} }} }} }}
 possible = {{ has_technology_researched = academia }}
 ai_chance = {{ value = 20 if = {{ limit = {{ NOT = {{ nesnd_india_reform_safe = yes }} }} value = 0 }} }}
 effect = {{ custom_tooltip = nesnd_india_priority_tt hidden_effect = {{ if = {{ limit = {{ nesnd_india_reform_live = yes NOT = {{ has_variable = {done} }} }} set_variable = {{ name = nesnd_india_priority value = {prio} }} nesnd_india_refresh = yes }} }} }}
}}
'''
texts['nesnd_india_twelve_months_tt']=('上述条件已累计维持十二个月。','These conditions have been met for a total of twelve months.')
append('common/scripted_triggers/nesnd_india_core.txt',triggers)
# Single monthly owner for society variables; bar is an explanatory mirror.
for kind,parts in [('dynasty',['legitimacy','religion','dependence']),('community',['education','representation','unrest'])]:
 bars+=f'nesnd_india_{kind}_bar = {{ name = nesnd_india_{kind}_bar max_value = 100 start_value = 50 monthly_progress = {{\n'
 for part in parts:bars+=f' add = {{ desc = nesnd_india_{kind}_{part} value = {{ value = 0 if = {{ limit = {{ owner = {{ nesnd_india_society_live = yes }} }} value = owner.nesnd_india_{kind}_{part} }} }} }}\n'
 bars+='} }\n'
 effects+=f'''nesnd_india_{kind}_tick = {{ change_variable = {{ name = nesnd_india_{kind} add = nesnd_india_{kind}_delta }} clamp_variable = {{ name = nesnd_india_{kind} min = 0 max = 100 }} journal_entry:nesnd_india_society ?= {{ set_bar_progress = {{ bar = nesnd_india_{kind}_bar value = root.nesnd_india_{kind} }} }} }}\n'''
put('common/scripted_progress_bars/nesnd_india_core.txt',bars)
jes+='''nesnd_india_reform = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_reform_live = yes } possible = { nesnd_india_reform_live = yes }
 scripted_button = nesnd_india_choose_schools scripted_button = nesnd_india_choose_industry
 complete = { hidden_trigger = { nesnd_india_reform_live = yes } custom_tooltip = { text = nesnd_india_reform_finished_tt has_variable = nesnd_india_schools_done has_variable = nesnd_india_industry_done } }
 on_complete = { if = { limit = { nesnd_india_reform_live = yes } set_variable = nesnd_india_reform_done remove_variable = nesnd_india_priority } }
 invalid = { NOT = { nesnd_india_reform_live = yes } }
 on_invalid = { remove_variable = nesnd_india_priority }
 status_desc = { desc = nesnd_india_reform_status }
 weight = 1000 should_be_pinned_by_default_uninvolved_or_context = yes
}
nesnd_india_society = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_society_live = yes } possible = { nesnd_india_society_live = yes }
 scripted_progress_bar = nesnd_india_dynasty_bar scripted_progress_bar = nesnd_india_community_bar
 scripted_button = nesnd_india_dynastic_constitution scripted_button = nesnd_india_republican_settlement
 invalid = { NOT = { nesnd_india_society_live = yes } }
 on_monthly_pulse = { effect = { if = { limit = { nesnd_india_society_live = yes } nesnd_india_dynasty_tick = yes nesnd_india_community_tick = yes } } }
 status_desc = { desc = nesnd_india_society_status }
 weight = 800
}
nesnd_india_caste = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_caste_live = yes } possible = { nesnd_india_caste_live = yes }
 complete = { hidden_trigger = { nesnd_india_caste_live = yes } nesnd_india_caste_ready = yes }
 on_complete = { if = { limit = { nesnd_india_caste_live = yes } set_variable = nesnd_india_caste_done add_modifier = { name = nesnd_india_equal_service months = 120 } } }
 invalid = { NOT = { nesnd_india_caste_live = yes } }
 weight = 700
}
nesnd_india_princes = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_prince = yes } possible = { nesnd_india_prince = yes }
 invalid = { NOT = { nesnd_india_prince = yes } }
 status_desc = { desc = nesnd_india_princes_status }
 weight = 450
}
nesnd_india_usm = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_usm_live = yes } possible = { nesnd_india_usm_live = yes }
 invalid = { NOT = { nesnd_india_usm_live = yes } }
 status_desc = { desc = nesnd_india_usm_status }
 weight = 600
}
nesnd_india_unified = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_empire = yes OR = { c:BHT ?= this c:DRA ?= this } NOT = { has_variable = nesnd_india_unified_done } }
 possible = { nesnd_india_empire = yes OR = { c:BHT ?= this c:DRA ?= this } NOT = { has_variable = nesnd_india_unified_done } }
 complete = { hidden_trigger = { nesnd_india_empire = yes NOT = { has_variable = nesnd_india_unified_done } }
 literacy_rate >= 0.4 institution_investment_level = { institution = institution_schools value >= 3 }
 bureaucracy >= 0 country_has_building_type_levels = { target = bt:building_railway value >= 30 }
 OR = { has_law = law_type:law_freedom_of_conscience has_law = law_type:law_total_separation }
 }
 on_complete = { if = { limit = { NOT = { has_variable = nesnd_india_unified_done } } set_variable = nesnd_india_unified_done add_modifier = { name = nesnd_india_unified_reward months = 120 } } }
 invalid = { OR = { NOT = { nesnd_india_empire = yes } has_variable = nesnd_india_unified_done } }
 weight = 800
}
'''
texts['nesnd_india_reform_finished_tt']=('完成学校与官署、工场与军队。','Complete Schools and Administration and Workshops and Armies.')
# Explicit constitutional choice, once, preserves religion/caste/populations.
for kind,law in [('dynastic_constitution','law_census_voting'),('republican_settlement','law_presidential_republic')]:
 extra='custom_tooltip = { text = nesnd_india_dynasty_ready_tt nesnd_india_dynasty >= 60 } country_has_monarchy_law = yes' if kind=='dynastic_constitution' else 'has_technology_researched = egalitarianism'
 realextra='nesnd_india_dynasty >= 60 country_has_monarchy_law = yes' if kind=='dynastic_constitution' else 'has_technology_researched = egalitarianism'
 lawextra='' if kind=='dynastic_constitution' else 'activate_law = law_type:law_census_voting'
 buttons+=f'''nesnd_india_{kind} = {{ name = nesnd_india_{kind} desc = nesnd_india_settlement_desc
 visible = {{ nesnd_india_society_live = yes NOT = {{ has_variable = nesnd_india_national_settlement }} }}
 possible = {{ custom_tooltip = {{ text = nesnd_india_community_ready_tt nesnd_india_community >= 75 }} {extra} }}
 ai_chance = {{ value = 10 }}
 effect = {{ if = {{ limit = {{ nesnd_india_society_live = yes NOT = {{ has_variable = nesnd_india_national_settlement }} nesnd_india_community >= 75 {realextra} }}
 set_variable = nesnd_india_national_settlement activate_law = law_type:{law} {lawextra}
 add_modifier = {{ name = nesnd_india_national_settlement months = 120 }}
 }} }}
}}
'''
put('common/scripted_buttons/nesnd_india_reform.txt',buttons)
put('common/journal_entries/nesnd_india_core.txt',jes)
effects+='''nesnd_india_initialize = {
 if = { limit = { nesnd_india_empire = yes }
  set_variable = nesnd_india_imperial_line
  if = { limit = { NOT = { has_variable = nesnd_india_dynasty } } set_variable = { name = nesnd_india_dynasty value = 50 } }
  if = { limit = { NOT = { has_variable = nesnd_india_community } } set_variable = { name = nesnd_india_community value = 25 } }
 }
}
nesnd_india_refresh = {
 nesnd_india_initialize = yes
'''
for name,trig in [('reform','nesnd_india_reform_live'),('schools','nesnd_india_schools_available'),('industry','nesnd_india_industry_available'),('society','nesnd_india_society_live'),('caste','nesnd_india_caste_live'),('princes','nesnd_india_prince'),('usm','nesnd_india_usm_live')]:effects+=f' if = {{ limit = {{ {trig} = yes NOT = {{ has_journal_entry = nesnd_india_{name} }} }} add_journal_entry = {{ type = nesnd_india_{name} }} }}\n'
effects+=''' if = { limit = { nesnd_india_empire = yes OR = { c:BHT ?= this c:DRA ?= this } NOT = { has_variable = nesnd_india_unified_done } NOT = { has_journal_entry = nesnd_india_unified } } add_journal_entry = { type = nesnd_india_unified } }
}
'''
put('common/scripted_effects/nesnd_india_core.txt',effects)
put('common/on_actions/nesnd_india_core.txt','''on_monthly_pulse_country = { on_actions = { nesnd_india_maintenance } }
on_country_formed = { on_actions = { nesnd_india_maintenance } }
on_game_started_after_lobby = { on_actions = { nesnd_india_startup } }
nesnd_india_maintenance = { trigger = { OR = { nesnd_india_country = yes c:USM ?= this } } effect = { nesnd_india_refresh = yes } }
nesnd_india_startup = { effect = { every_country = { limit = { OR = { nesnd_india_country = yes c:USM ?= this } } nesnd_india_refresh = yes } } }
''')
loc(texts)
dump(R/'core-implementation.json',{'additional_mug_battalions':37,'native_battalions':3,'total_declared':40,'history_population_unchanged':True,'journals':9,'disabled_native':disabled,'game_launched':False})
print('Core India scripts written; validation pending')
