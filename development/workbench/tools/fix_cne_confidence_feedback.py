from feedback_context import *
rel='common/script_values/nesnd_cne_confidence.txt';s=read(C/rel);tree=parse(s);edits=[]
for key,old,new in [('base','-50','-25'),('land','-10','-5'),('urban','-10','-5'),('estates','-10','-5'),('war','-50','-25'),('radicals','-40','-20')]:
    n=tree.get('nesnd_cne_conf_'+key);body=s[n.start:n.end];assert body.count(old)==1
    edits.append((n.start,n.end,body.replace(old,new)))
for a,b,t in sorted(edits,reverse=True):s=s[:a]+t+s[b:]
write(C/rel,s)
rel='common/scripted_effects/nesnd_cne_confidence.txt';s=read(C/rel)
assert s.count('name = nesnd_cne_confidence add = -500')==1
s=s.replace('name = nesnd_cne_confidence add = -500','name = nesnd_cne_confidence add = -250')
s+='''
nesnd_cne_take_respite = {
    if = {
        limit = { nesnd_cne_respite_ready = yes }
        set_variable = nesnd_cne_respite_used
        set_variable = { name = nesnd_cne_respite_active months = 6 }
        nesnd_cne_stop_all_programs = yes
        change_variable = { name = nesnd_cne_confidence add = 100 }
        clamp_variable = { name = nesnd_cne_confidence min = 0 max = 1000 }
        nesnd_cne_confidence_sync = yes
        nesnd_refresh_land_display = yes
    }
}
''';write(C/rel,s)
rel='common/scripted_triggers/nesnd_cne_confidence.txt';s=read(C/rel)
s+='''
nesnd_cne_reforms_in_progress = {
    OR = { has_variable = nesnd_cne_land_program has_variable = nesnd_cne_urban_program nesnd_cne_active_camp_count > 0 }
}
nesnd_cne_respite_confidence_ready = {
    trigger_if = { limit = { has_variable = nesnd_cne_confidence } var:nesnd_cne_confidence <= 900 }
    trigger_else = { always = no }
}
nesnd_cne_respite_confidence_urgent = {
    trigger_if = { limit = { has_variable = nesnd_cne_confidence } var:nesnd_cne_confidence <= 600 }
    trigger_else = { always = no }
}
nesnd_cne_respite_ready = {
    nesnd_cne_programs_live = yes
    nesnd_cne_reforms_in_progress = yes
    nesnd_cne_respite_confidence_ready = yes
    NOT = { has_variable = nesnd_cne_respite_used }
    NOT = { has_variable = nesnd_cne_respite_active }
}
''';write(C/rel,s)
rel='common/scripted_triggers/nesnd_cne_programs.txt';s=read(C/rel);n=parse(s).get('nesnd_cne_program_can_start')
old=s[n.start:n.end];new=old.replace('nesnd_cne_programs_live = yes','nesnd_cne_programs_live = yes\n NOT = { has_variable = nesnd_cne_respite_active }');assert new!=old
write(C/rel,s[:n.start]+new+s[n.end:])

# Keep actual execution checks, but do not expose internal lifecycle variables in effect previews.
rel='common/scripted_buttons/nesnd_cne_programs.txt';s=read(C/rel);keys=[n.key for n in parse(s).children if n.key.endswith(('_start_button','_stop_button'))];assert len(keys)==48
rows=[]
for key in keys:
    s=read(C/rel);n=parse(s).get(key);e=n.get('effect');tips=[x.value for x in e.walk() if x.key=='custom_tooltip' and x.value];assert len(tips)==1,(key,tips)
    rows.append(wrap_button(rel,key,tips[0]))
    s=read(C/rel);n=parse(s).get(key);p=n.get('possible');body=s[p.vstart+1:p.vend-1]
    if key.endswith('_stop_button'):new='possible = { hidden_trigger = {'+body+'} }'
    else:new='possible = {'+body+'\n custom_tooltip = { text = nesnd_cne_respite_over_tt NOT = { has_variable = nesnd_cne_respite_active } }\n}'
    write(C/rel,s[:p.start]+new+s[p.end:])

write(C/'common/scripted_buttons/nesnd_cne_respite.txt','''nesnd_cne_respite_button = {
    name = nesnd_cne_respite_button
    desc = nesnd_cne_respite_button_desc
    visible = {
        nesnd_cne_programs_live = yes
        nesnd_cne_reforms_in_progress = yes
        nesnd_cne_respite_confidence_ready = yes
        NOT = { has_variable = nesnd_cne_respite_used }
    }
    possible = {
        hidden_trigger = { nesnd_cne_programs_live = yes }
        custom_tooltip = { text = nesnd_cne_respite_unused_tt NOT = { has_variable = nesnd_cne_respite_used } }
        custom_tooltip = { text = nesnd_cne_respite_over_tt NOT = { has_variable = nesnd_cne_respite_active } }
        custom_tooltip = { text = nesnd_cne_respite_programs_tt nesnd_cne_reforms_in_progress = yes }
        custom_tooltip = { text = nesnd_cne_respite_confidence_tt nesnd_cne_respite_confidence_ready = yes }
    }
    ai_chance = { value = 0 if = { limit = { nesnd_cne_respite_confidence_urgent = yes } value = 15 } }
    effect = {
        custom_tooltip = nesnd_cne_respite_effect_tt
        hidden_effect = { nesnd_cne_take_respite = yes }
    }
}
''')
rel='common/journal_entries/nesnd_cne_confidence.txt';s=read(C/rel)
assert s.count('scripted_progress_bar = nesnd_cne_confidence_bar')==1
s=s.replace('scripted_progress_bar = nesnd_cne_confidence_bar','scripted_progress_bar = nesnd_cne_confidence_bar\n\tscripted_button = nesnd_cne_respite_button')
s=s.replace('status_desc = { first_valid = {','status_desc = { first_valid = {\n            triggered_desc = { trigger = { has_variable = nesnd_cne_respite_active } desc = nesnd_cne_confidence_respite_status }')
write(C/rel,s)
texts={
 'nesnd_cne_respite_button':('暂缓诸项改革','Pause the Reforms'),
 'nesnd_cne_respite_button_desc':('朝廷暂缓土地商品化、国家城市化与各省营产改制，给地方留下安顿生计、平息争端的时日。','The court will suspend land, urban and military-estate reforms, giving the provinces time to restore livelihoods and settle disputes.'),
 'nesnd_cne_respite_unused_tt':('本轮地权革命尚未实行过全面暂缓。','We have not yet called a general pause during this land revolution.'),
 'nesnd_cne_respite_over_tt':('未处于改革暂缓期。','No general reform pause is in effect.'),
 'nesnd_cne_respite_programs_tt':('至少一项改革正在推行。','At least one reform is underway.'),
 'nesnd_cne_respite_confidence_tt':('人民的信心不高于#v 900#!。','Public confidence is no higher than #v 900#!.'),
 'nesnd_cne_respite_effect_tt':('暂停土地商品化、国家城市化与各省营产整顿，并撤回对应的临时修正。#v 6个月#!内不能重启这些改革；人民的信心#p +100#!。本轮地权革命只能实行一次。','Pause land commercialisation, urbanisation and all military-estate reforms, removing their temporary modifiers. These reforms cannot be restarted for #v 6 months#!. Public confidence #p +100#!. This is available once during the land revolution.'),
 'nesnd_cne_confidence_respite_status':('各省的改革暂缓推行。','Reforms in the provinces have been temporarily suspended.'),
}
append_texts(texts)
changed_locs=[]
for lang in ['simp_chinese','english']:
    p=C/'localization'/lang/'replace'/f'zzzzzz_nesnd_cne_programs_l_{lang}.yml';lines=read(p).splitlines()
    for i,line in enumerate(lines):
        if any(re.match(r'\s*'+key+':',line) for key in ['nesnd_cne_land_start_tt','nesnd_cne_urban_start_tt','nesnd_cne_camp_start_tt']):
            assert line.count('#n 10#!')==1;lines[i]=line.replace('#n 10#!','#n 5#!');changed_locs.append((lang,line.split(':')[0].strip()))
    write(p,'\n'.join(lines)+'\n')
p=C/'localization/simp_chinese/replace/zz_nesnd_crisis_rules_l_simp_chinese.yml';s=read(p);assert s.count('地权革命正在进行，尚未结案。')==1
write(p,s.replace('地权革命正在进行，尚未结案。','地权革命仍在进行。'))
dump(R/'cne-confidence-applied.json',{'losses_halved':True,'governing_IG_recovery_unchanged':10,'bankruptcy_loss':250,'respite_recovery':100,'respite_months':6,'respite_once':True,'progress_thresholds_unchanged':[1000,500,0],'buttons':rows,'texts':texts,'updated_start_texts':changed_locs,'game_launched':False})
print('Confidence losses halved; bounded respite added; 48 button previews fixed; historical progress preserved.')
