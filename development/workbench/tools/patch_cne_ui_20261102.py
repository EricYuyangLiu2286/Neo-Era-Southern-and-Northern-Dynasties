from maintenance_20261102_context import *
import re
tr='common/scripted_triggers/nesnd_cne_programs.txt'
replace_def(tr,'nesnd_cne_program_can_start','''nesnd_cne_program_can_start = {
 nesnd_cne_programs_live = yes
 trigger_if = { limit = { is_ai = yes } nesnd_cne_ai_program_safe = yes }
}''')
p=C/tr;write(p,read(p)+'''nesnd_cne_ai_program_safe = {
 trigger_if = { limit = { has_variable = cne_landreform_failure_tracker }
  bureaucracy >= 0
  NOT = { has_modifier = declared_bankruptcy }
  var:cne_landreform_failure_tracker < 65
 }
 trigger_else = { always = no }
}
nesnd_cne_urban_centres_ready = {
 any_scope_state = { count >= 5 state_has_building_type_levels = { target = bt:building_urban_center value >= 5 } }
}
nesnd_cne_urban_welfare_technology = {
 OR = { has_technology_researched = democracy has_technology_researched = labor_movement has_technology_researched = human_rights }
}
nesnd_cne_urban_welfare_law = {
 OR = { has_law_or_variant = law_type:law_poor_laws has_law_or_variant = law_type:law_wage_subsidies has_law_or_variant = law_type:law_old_age_pension }
}
''')
buildings=[('building_iron_mine',25),('building_coal_mine',40),('building_steel_mill',10),('building_tooling_workshop',30),('building_motor_industry',6),('building_logging_camp',60),('building_shipyard',12)]
replace_def(tr,'nesnd_cne_urban_foundation','''nesnd_cne_urban_foundation = {
 nesnd_cne_urban_centres_ready = yes
'''+''.join(f' country_has_building_type_levels = {{ target = bt:{k} value >= {v} }}\n' for k,v in buildings)+''' nesnd_cne_urban_welfare_technology = yes
 nesnd_cne_urban_welfare_law = yes
 institution_investment_level = { institution = institution_social_security value >= 1 }
}''')
replace_def(tr,'nesnd_cne_land_foundation','''nesnd_cne_land_foundation = {
 has_technology_researched = intensive_agriculture
 custom_tooltip = { text = nesnd_cne_arable_share_tt nesnd_cne_agricultural_share >= 0.06 }
}''')
# Native country building totals replace the seven traversal wrappers; same scope/threshold.
p=C/'common/script_values/nesnd_cne_programs.txt';s=read(p)
for key in ['iron','coal','steel','tools','engines','timber','ships']:
 n=parse(s).get('nesnd_cne_'+key+'_levels');assert n;s=s[:n.start]+s[n.end:]
write(p,s)
btn='common/scripted_buttons/nesnd_cne_programs.txt';p=C/btn;s=read(p)
for kind in ['land','urban']:
 n=parse(s).get('nesnd_cne_'+kind+'_start_button');q=n.get('possible')
 body=f'''possible = {{
 nesnd_cne_{kind}_foundation = yes
 hidden_trigger = {{ nesnd_cne_program_can_start = yes }}
}}''';s=s[:q.start]+body+s[q.end:]
# All estate identity/AI checks remain executable, but internal flags are not player prose.
for n in list(parse(s).children)[::-1]:
 if n.key.startswith('nesnd_cne_camp_') and n.key.endswith('_start_button'):
  q=n.get('possible');ready=n.key.removesuffix('_start_button')+'_ready';s=s[:q.start]+f'possible = {{ hidden_trigger = {{ {ready} = yes }} }}'+s[q.end:]
write(p,s)
for kind in ['land','urban']:
 rel='common/journal_entries/nesnd_cne_programs.txt';p=C/rel;s=read(p);n=parse(s).get('nesnd_cne_'+kind+'_journal');q=n.get('status_desc')
 st=f'''status_desc = {{ first_valid = {{
 triggered_desc = {{ trigger = {{ has_variable = nesnd_cne_{kind}_program }} desc = nesnd_cne_{kind}_running }}
 desc = nesnd_cne_quiet_status
}} }}''';write(p,s[:q.start]+st+s[q.end:])
rel='common/journal_entries/nesnd_cne_confidence.txt';p=C/rel;s=read(p);n=parse(s).get('nesnd_cne_confidence_journal').get('status_desc')
st='''status_desc = { first_valid = {
 triggered_desc = { trigger = { c:NRP ?= { has_war_with = root } } desc = nesnd_cne_confidence_rebellion }
 triggered_desc = { trigger = { has_variable = nesnd_cne_republican_rose } desc = nesnd_cne_confidence_aftermath }
 triggered_desc = { trigger = { has_variable = nesnd_cne_confidence var:nesnd_cne_confidence < 750 } desc = nesnd_cne_confidence_waning }
 desc = nesnd_cne_confidence_status
} }''';write(p,s[:n.start]+st+s[n.end:])
# Remove duplicate mounting, not the shared button definition or the AI call.
p=C/'common/journal_entries/ce_usm_the_last_days_of_ming.txt';s=read(p);assert s.count('scripted_button = nesnd_federal_compact_button')==1;s=s.replace('scripted_button = nesnd_federal_compact_button','');write(p,s)
strings={
'simp_chinese':{'nesnd_cne_arable_share_tt':'本国中华本土及东北诸州：农业用地至少占可耕地的#v 6%#!。','nesnd_cne_quiet_status':'','nesnd_cne_land_running':'土地商品化正在推行。','nesnd_cne_urban_running':'国家城市化正在推行。','nesnd_cne_confidence_status':'各省仍相信朝廷能完成大革命未竟之业。','nesnd_cne_confidence_waning':'地方请愿日多，朝廷的许诺正在失去分量。','nesnd_cne_confidence_rebellion':'共和军已经举兵，旧日同道正在兵戎相见。','nesnd_cne_confidence_aftermath':'举兵者的旗帜已经倒下，地方仍在等待朝廷履行承诺。'},
'english':{'nesnd_cne_arable_share_tt':'In our Chinese heartland and northeastern states, developed farmland occupies at least #v 6%#! of arable land.','nesnd_cne_quiet_status':'','nesnd_cne_land_running':'Land commercialisation is underway.','nesnd_cne_urban_running':'National urbanisation is underway.','nesnd_cne_confidence_status':'The provinces still trust the court to fulfil the unfinished promise of the Great Revolution.','nesnd_cne_confidence_waning':'Petitions multiply, and the court’s promises carry less weight.','nesnd_cne_confidence_rebellion':'Republican armies have risen. Former comrades face one another in battle.','nesnd_cne_confidence_aftermath':'The rebels’ banners have fallen. The provinces still await fulfilment of the court’s promises.'}}
for lang,keys in strings.items():
 for p in (C/f'localization/{lang}').rglob('*.yml'):
  s=read(p);out=s
  for k,v in keys.items():out=re.sub(rf'^ {re.escape(k)}:.*$',lambda m:f' {k}:0 "{v}"',out,flags=re.M)
  if s!=out:write(p,out)
 # New keys in one dedicated file, excluding preexisting status key.
 write(C/f'localization/{lang}/replace/zzzzzzz_nesnd_cne_clear_conditions_l_{lang}.yml','l_'+lang+':\n'+''.join(f' {k}:0 "{v}"\n' for k,v in keys.items() if k!='nesnd_cne_confidence_status'))
print('Native independent requirements, AI-only safety gates, conditional status and one USM envoy entry written')
