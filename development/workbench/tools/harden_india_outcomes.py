from india_context import *
append('common/scripted_triggers/nesnd_india_uprising.txt','''nesnd_india_revolt_won = {
 has_variable = nesnd_india_revolt_negotiation_ended
 NOT = { has_variable = nesnd_india_revolt_failed }
 is_subject = no
 trigger_if = { limit = { exists = var:nesnd_india_revolt_origin }
  any_scope_state = { state_region = prev.var:nesnd_india_revolt_origin }
 } trigger_else = { always = no }
}
''')
p=C/'common/journal_entries/nesnd_india_uprising.txt';s=read(p);n=parse(s).get('nesnd_india_revolt_war');comp=n.get('complete');s=s[:comp.start]+'complete = { custom_tooltip = { text = nesnd_india_revolt_resolved_tt nesnd_india_revolt_won = yes } }'+s[comp.end:];n=parse(s).get('nesnd_india_revolt_war').get('fail');s=s[:n.start]+'fail = { has_variable = nesnd_india_revolt_resolved NOT = { nesnd_india_revolt_won = yes } }'+s[n.end:];write(p,s)
# The republican outcome closes the dynasty-specific JE but retains the national community.
p=C/'common/journal_entries/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_society');part=s[n.start:n.end].replace('scripted_progress_bar = nesnd_india_dynasty_bar','').replace('nesnd_india_dynasty_tick = yes','').replace('nesnd_india_sync_dynasty = yes','');write(p,s[:n.start]+part+s[n.end:])
append('common/journal_entries/nesnd_india_core.txt','''nesnd_india_dynasty_journal = {
 icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content can_revolution_inherit = no
 is_shown_when_inactive = { nesnd_india_society_live = yes country_has_monarchy_law = yes }
 possible = { nesnd_india_society_live = yes country_has_monarchy_law = yes }
 immediate = { nesnd_india_initialize = yes nesnd_india_sync_dynasty = yes }
 scripted_progress_bar = nesnd_india_dynasty_bar
 invalid = { OR = { NOT = { nesnd_india_society_live = yes } NOT = { country_has_monarchy_law = yes } } }
 on_monthly_pulse = { effect = { if = { limit = { nesnd_india_society_live = yes country_has_monarchy_law = yes } nesnd_india_dynasty_tick = yes } } }
 weight = 600
}
''')
p=C/'common/scripted_effects/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_sync_dynasty');part=s[n.start:n.end].replace('nesnd_india_society','nesnd_india_dynasty_journal');s=s[:n.start]+part+s[n.end:];n=parse(s).get('nesnd_india_refresh');s=s[:n.vend-1]+' if = { limit = { nesnd_india_society_live = yes country_has_monarchy_law = yes NOT = { has_journal_entry = nesnd_india_dynasty_journal } } add_journal_entry = { type = nesnd_india_dynasty_journal } }\n'+s[n.vend-1:];write(p,s)
p=C/'common/scripted_buttons/nesnd_india_reform.txt';s=read(p);n=parse(s).get('nesnd_india_dynastic_constitution').get('visible');s=s[:n.vend-1]+' country_has_monarchy_law = yes '+s[n.vend-1:];write(p,s)
p=C/'common/scripted_progress_bars/nesnd_india_core.txt';s=read(p);n=parse(s).get('nesnd_india_dynasty_bar');part=s[n.start:n.end].replace('nesnd_india_society_live = yes','nesnd_india_society_live = yes country_has_monarchy_law = yes');write(p,s[:n.start]+part+s[n.end:])
loc({'nesnd_india_dynasty_journal':('王朝的民望','The Dynasty’s Standing'),'nesnd_india_dynasty_journal_reason':('皇室的旧名望仍有分量，但人们也会用眼前的政绩评判君主。各省的信仰能否得到尊重，朝廷能否作出自己的决定，都将影响他们是否愿意拥戴这个王朝。','The dynasty’s old prestige still carries weight, but its subjects also judge their sovereign by the conduct of government. Respect for the provinces’ faiths and the court’s ability to make its own decisions will shape their loyalty.')})
# Generic local republican flags do not carry the Ming imperial emblem.
p=C/'common/coat_of_arms/coat_of_arms/nesnd_india_uprising.txt';s=read(p)
for n in sorted([n for n in parse(s).walk() if n.key=='colored_emblem'],key=lambda n:n.start,reverse=True):s=s[:n.start]+s[n.end:]
write(p,s)
# Distinguish the two administrative stories instead of duplicate prose.
for lang in ['simp_chinese','english']:
 p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzzz_nesnd_india_l_{lang}.yml';s=read(p)
 rows={'nesnd_tianzhu_governance_reason':('天竺的商人熟悉海路，乡村却有另一套秩序。宣慰使既要维持港口与驻军，也要让学校和税务进入内地；当地王公与村社不会仅因南京的任命就放弃自己的利益。','Tianzhu’s merchants know the sea routes, while its villages follow a different order. The commissioner must maintain the ports and garrisons while extending schools and revenue services inland. Local princes and communities will not surrender their interests merely because Nanjing has appointed an official.'),'nesnd_yuanshan_governance_reason':('远山的港口已经成为南朝航路上的据点，腹地的治理却刚刚开始。道路、税务与学校必须随着驻军一同建立，否则沿海的旗帜仍无法代表整个宣慰司。','Yuanshan’s ports have become stations on the Southern Court’s sea routes, but administration inland is only beginning. Roads, revenue services and schools must follow the garrisons if the commission is to become more than a flag on the coast.'),'nesnd_india_revolt_resolved_tt':('本次争端已经结束，仍独立保有起义地区。','The dispute has ended, and we retain the territory of the rising as an independent state.')}
 for k,pair in rows.items():v=pair[0 if lang=='simp_chinese' else 1];s=re.sub(r'(?m)^(\s*'+k+r':\d*\s+)".*"$',lambda m:m[1]+'"'+v+'"',s)
 write(p,s)
print('Final outcome and dynasty lifecycle closure applied')
