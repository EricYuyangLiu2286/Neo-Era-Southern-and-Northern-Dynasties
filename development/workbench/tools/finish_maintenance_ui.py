from maintenance_20261102_context import *
import re

# Native triggers remain visible; runtime bookkeeping and AI caution are hidden.
p=C/'common/scripted_triggers/nesnd_cne_reform.txt';s=read(p)
s=s.replace('    bureaucracy >= 0\n    NOT = { has_modifier = declared_bankruptcy }\n    gold_reserves >= nesnd_reform_investment_cost','    trigger_if = { limit = { is_ai = yes } bureaucracy >= 0 NOT = { has_modifier = declared_bankruptcy } }\n    gold_reserves >= nesnd_reform_investment_cost')
n=parse(s).get('nesnd_reform_can_relieve');part=s[n.start:n.end].replace('NOT = { has_modifier = declared_bankruptcy }','trigger_if = { limit = { is_ai = yes } NOT = { has_modifier = declared_bankruptcy } }');s=s[:n.start]+part+s[n.end:];write(p,s)
p=C/'common/scripted_buttons/nesnd_crisis_buttons.txt';s=read(p)
for key,body in [('nesnd_land_survey','gold_reserves >= nesnd_reform_investment_cost\n hidden_trigger = { nesnd_reform_can_invest = yes NOT = { has_variable = nesnd_cne_funding_pending } }'),('nesnd_land_military','gold_reserves >= nesnd_reform_review_cost\n institution_investment_level = { institution = institution_social_security value >= 1 }\n hidden_trigger = { nesnd_reform_can_relieve = yes NOT = { has_variable = nesnd_cne_funding_pending } }')]:
 n=parse(s).get(key).get('possible');s=s[:n.start]+'possible = { '+body+' }'+s[n.end:]
write(p,s)
# Explain only derived aggregates with a custom tooltip. Native laws, institutions,
# literacy, monarchy and state count retain their native individual rows.
p=C/'common/journal_entries/ce_cne_land_draft.txt';s=read(p);parent=parse(s).get('ce_cne_land_reform');n=parent.get('complete')
body='''complete = {
 num_states >= 4
 country_has_monarchy_law = yes
 hidden_trigger = { NOT = { nesnd_cne_reform_failed = yes } nesnd_reform_active = yes has_variable = nesnd_reform_v2 var:nesnd_reform_samples >= 3 var:nesnd_reform_workforce > 0 }
 nesnd_reform_land_rights = yes
 institution_investment_level = { institution = institution_schools value >= 2 }
 literacy_rate >= 0.48
 bureaucracy >= 0
 is_at_war = no
 NOT = { has_modifier = declared_bankruptcy }
 custom_tooltip = { text = nesnd_cne_employment_condition nesnd_reform_employment_ready = yes }
 custom_tooltip = { text = nesnd_cne_livelihood_condition var:nesnd_reform_starving <= 0.08 var:nesnd_reform_sol >= 11 var:nesnd_reform_access >= 0.85 var:nesnd_reform_neglected_regions < 1 }
 custom_tooltip = { text = nesnd_cne_completion_condition var:cne_landreform_completion_tracker >= 100 }
 custom_tooltip = { text = nesnd_cne_stability_condition var:nesnd_reform_good_months >= 12 }
 custom_tooltip = { text = nesnd_cne_disorder_condition var:cne_landreform_failure_tracker < 50 }
}'''
s=s[:n.start]+body+s[n.end:];n=parse(s).get('ce_cne_land_reform').get('fail')
body='''fail = { OR = {
 NOT = { country_has_monarchy_law = yes }
 custom_tooltip = { text = nesnd_cne_confidence_gone nesnd_cne_confidence_exhausted = yes }
 custom_tooltip = { text = nesnd_cne_coup_failure nesnd_cne_coup_has_succeeded = yes }
 custom_tooltip = { text = nesnd_cne_civil_failure nesnd_cne_native_civil_war = yes }
 custom_tooltip = { text = nesnd_cne_crisis_failure nesnd_reform_extreme_crisis = yes }
} }'''
s=s[:n.start]+body+s[n.end:];write(p,s)
loc={
'nesnd_cne_employment_condition':('无业劳动力不超过6%；若社保达到二级、生活水平达到12，则可放宽至12%。','Unemployment is at most 6%, or 12% with level 2 Social Security and a standard of living of 12.'),
'nesnd_cne_livelihood_condition':('欠食劳动力不超过8%，生活水平至少11，市场接入至少85%，各地没有持续的严重民生危机。','Starvation is at most 8%, standard of living at least 11 and market access at least 85%, with no persistent severe local hardship.'),
'nesnd_cne_completion_condition':('改革进度达到100。','Reform progress has reached 100.'),
'nesnd_cne_stability_condition':('民生与制度条件已连续巩固十二个月。','Living conditions and institutions have remained secure for twelve consecutive months.'),
'nesnd_cne_disorder_condition':('地方失序低于50。','Local disorder is below 50.'),
'nesnd_cne_confidence_gone':('帝国人民的信心已经耗尽。','The people\'s confidence is exhausted.'),
'nesnd_cne_coup_failure':('政变已经成功。','A coup has succeeded.'),
'nesnd_cne_civil_failure':('革命或分离内战已经爆发。','A revolution or secession war has begun.'),
'nesnd_cne_crisis_failure':('民生困境已持续一年，地方失序达到90、动乱超过40%、合法性低于25，且帝国陷入战争或破产惩罚。','Hardship has persisted for a year, disorder has reached 90, turmoil exceeds 40%, legitimacy is below 25, and the empire is at war or under bankruptcy penalties.'),
}
for i,lang in enumerate(['simp_chinese','english']):
 p=C/f'localization/{lang}/replace/zzzzzzz_nesnd_cne_clear_conditions_l_{lang}.yml';s=read(p)
 s=s.replace('举兵者的旗帜已经倒下，地方仍在等待朝廷履行承诺。','战事的震荡尚未平息。')
 for k,v in loc.items():s+=f' {k}:0 "{v[i]}"\n'
 write(p,s)

# Late stance choices must not revive a concluded global conflict.
p=C/'events/ce_poland_events.txt';s=read(p);n=parse(s).get('ce_poland_events.97');part=s[n.start:n.end];pn=parse(part).get(n.key)
for op in reversed(pn.all('option')):
 effect=[x for x in op.children if x.key not in {'name','trigger','ai_chance','default_option'}]
 if not effect:continue
 kept='\n'.join(part[x.start:x.end] for x in op.children if x.key in {'name','trigger','ai_chance','default_option'})
 payload='\n'.join(part[x.start:x.end] for x in effect)
 replacement='option = {\n'+kept+'\nif = { limit = { nesnd_poland_active = yes }\n'+payload+'\n}\n}'
 part=part[:op.start]+replacement+part[op.end:]
pn=parse(part).get(n.key);tr=pn.get('trigger');part=part[:tr.start]+part[tr.start:tr.end].replace('exists = c:KRA','nesnd_poland_active = yes',1)+'\ncancellation_trigger = { NOT = { nesnd_poland_active = yes } }'+part[tr.end:]
s=s[:n.start]+part+s[n.end:];write(p,s)
p=C/'common/scripted_effects/nesnd_poland_repairs.txt';s=read(p).replace('var:nesnd_polish_pending_state ?= scope:target_diplo_play_state','nesnd_poland_matching_pending = yes')
# Preserve the original single 10% radicalization when neither region remains.
n=parse(s).get('nesnd_poland_failure_secessions');outer=n.get('if');li=outer.get('limit');payload=s[li.end:outer.end-1]
wrapped='\nif = { limit = { OR = { owns_entire_state_region = STATE_KAUNAS owns_entire_state_region = STATE_BREST } }\n'+payload+'\n}\nelse = { every_scope_state = { add_radicals_in_state = { value = 0.10 } } }\n'
s=s[:li.end]+wrapped+s[outer.end-1:];write(p,s)
print('Native condition rows, AI-only funding caution, expired stance choices and original failure fallback updated.')
