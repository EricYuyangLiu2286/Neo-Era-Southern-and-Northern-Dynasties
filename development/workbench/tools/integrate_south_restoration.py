from feedback_context import *
# Use a real existence branch for the optional local ruler.
rel='common/scripted_triggers/nesnd_south_restoration.txt';s=read(C/rel)
s=s.replace('ruler ?= { is_character_alive = yes nesnd_ming_authorized_dynast = yes }','nesnd_postwar_ruling_dynast = yes')
s+='''
nesnd_postwar_ruling_dynast = {
    trigger_if = { limit = { exists = ruler } ruler = { is_character_alive = yes nesnd_ming_authorized_dynast = yes } }
    trigger_else = { always = no }
}
''';write(C/rel,s)
rel='common/scripted_effects/nesnd_south_restoration.txt';s=read(C/rel)
s=s.replace('limit = { ruler ?= { is_character_alive = yes nesnd_ming_authorized_dynast = yes } }','limit = { nesnd_postwar_ruling_dynast = yes }')
s=s.replace('has_variable = nesnd_original_ming_heir nesnd_postwar_original_royal_available = yes is_ruler_of_own_country = no','has_variable = nesnd_original_ming_heir nesnd_postwar_original_royal_available = yes NOT = { this = scope:nesnd_postwar_original_royal }')
write(C/rel,s)

rel='common/scripted_triggers/nesnd_south_settlement.txt';s=read(C/rel)
needle='''    OR = {
        NOT = { has_global_variable = nesnd_south_settled }'''
assert s.count(needle)==1;s=s.replace(needle,'''    OR = {
        nesnd_rebel_unclaimed_total_victory = yes
        NOT = { has_global_variable = nesnd_south_settled }''')
# Split the live-USM case before any right-hand country lookup.
old='''        AND = {
            c:USM ?= { is_country_alive = yes enemy_occupation > 0.6 capital = { controller = root } }
            has_war_with = c:USM
            s:STATE_NANJING = { any_scope_state = { owner = c:USM controller = root } }
        }'''
new='''        trigger_if = {
            limit = { exists = c:USM }
            c:USM = { is_country_alive = yes enemy_occupation > 0.6 capital = { controller = root } }
            has_war_with = c:USM
            s:STATE_NANJING = { any_scope_state = { owner = c:USM controller = root } }
        }
        trigger_else = { always = no }'''
assert old in s;s=s.replace(old,new)
n=parse(s).get('nesnd_rebel_can_offer_settlement');part=s[n.start:n.end];part=part[:-1]+'''    trigger_if = { limit = { c:GNG ?= this } nesnd_postwar_gng_has_local_dynast = yes }
}''';s=s[:n.start]+part+s[n.end:];write(C/rel,s)

rel='common/scripted_effects/nesnd_south_settlement.txt';s=read(C/rel)
s=s.replace('    set_variable = nesnd_rebel_settlement_seen','    set_variable = nesnd_postwar_constitution_decided\n    set_variable = nesnd_rebel_settlement_seen',1)
n=parse(s).get('nesnd_south_settlement_retry');part=s[n.start:n.end]
old='''    if = { limit = { has_variable = nesnd_rebel_settlement_waiting is_country_alive = yes }'''
new='''    if = {
        limit = { nesnd_rebel_unclaimed_total_victory = yes }
        set_variable = nesnd_rebel_settlement_waiting
        if = { limit = { nesnd_rebel_can_offer_settlement = yes } trigger_event = { id = usm_civilwar.10 popup = yes } }
    }
    else_if = { limit = { has_variable = nesnd_rebel_settlement_waiting is_country_alive = yes }'''
assert old in part;part=part.replace(old,new,1)
# The old status-quo retry also needs to avoid comparing a vanished USM as RHS.
old='''            NOT = { any_country = { is_country_alive = yes has_variable = usm_opposition_country has_war_with = c:USM } }'''
new='''            trigger_if = { limit = { exists = c:USM } NOT = { any_country = { is_country_alive = yes has_variable = usm_opposition_country has_war_with = c:USM } } }'''
assert old in part;part=part.replace(old,new)
s=s[:n.start]+part+s[n.end:];write(C/rel,s)

# Record the exact deposed court before the existing transfer, then preserve unhosted survivors.
for rel,key,call in [('common/scripted_effects/nesnd_ming_court.txt','nesnd_ming_prepare_accession','nesnd_record_original_ming_identity'),('common/scripted_effects/nesnd_ming_royal_refuge.txt','nesnd_ming_resolve_court_migration','nesnd_ming_preserve_unhosted_royals')]:
    s=read(C/rel);n=parse(s).get(key);part=s[n.start:n.end]
    part=part[:-1]+'    '+call+' = yes\n}'
    write(C/rel,s[:n.start]+part+s[n.end:])

rel='events/usm_civilwar_events.txt';s=read(C/rel)
n=parse(s).get('usm_civilwar.9');part=s[n.start:n.end];t=parse(part).children[0].get('trigger');part=part[:t.vstart+1]+'\n        NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } }'+part[t.vstart+1:]
imm=parse(part).children[0].get('immediate');body=part[imm.vstart+1:imm.vend-1]
wrapped='immediate = { if = { limit = { NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } } }'+body+'} }'
part=part[:imm.start]+wrapped+part[imm.end:];s=s[:n.start]+part+s[n.end:]
n=parse(s).get('usm_civilwar.10');part=s[n.start:n.end]
for key in ['title','desc']:
    field=parse(part).children[0].get(key)
    val=key+' = { first_valid = {\n'
    for tag in ['SIH','HNA','GNG']:
        val+='        triggered_desc = { trigger = { c:'+tag+' ?= this } desc = nesnd_postwar_'+tag.lower()+'_'+key+' }\n'
    val+='        desc = usm_civilwar.10.'+('t' if key=='title' else 'd')+'\n    } }'
    part=part[:field.start]+val+part[field.end:]
part=part.replace('set_variable = nesnd_rebel_settlement_pending','''set_variable = { name = nesnd_rebel_settlement_pending months = 4 }
        if = { limit = { c:SIH ?= this } set_variable = nesnd_postwar_origin_sih }
        if = { limit = { c:HNA ?= this } set_variable = nesnd_postwar_origin_hna }
        if = { limit = { c:GNG ?= this } set_variable = nesnd_postwar_origin_gng }
        if = { limit = { OR = { c:SIH ?= this c:HNA ?= this } } nesnd_import_original_ming_identity = yes }''',1)
# Keep the original generic choices only for other winners, both preview and execution.
options=parse(part).children[0].all('option');edits=[]
for o in options:
    body=part[o.start:o.end];on=parse(body).children[0];trigger=on.get('trigger')
    if trigger:body=body[:trigger.vstart+1]+' NOT = { nesnd_postwar_special_victor = yes } '+body[trigger.vstart+1:]
    else:body=body[:body.index('{')+1]+'\n        trigger = { NOT = { nesnd_postwar_special_victor = yes } }'+body[body.index('{')+1:]
    body=body.replace('nesnd_rebel_can_commit_settlement = yes','nesnd_rebel_can_commit_settlement = yes\n                NOT = { nesnd_postwar_special_victor = yes }')
    edits.append((o.start,o.end,body))
for a,b,body in sorted(edits,reverse=True):part=part[:a]+body+part[b:]
special='''
    cancellation_trigger = { NOT = { nesnd_rebel_victory_fact = yes } }
    option = {
        name = nesnd_postwar_restore_ming_option
        show_as_unavailable = yes
        trigger = { OR = { c:SIH ?= this c:HNA ?= this } nesnd_postwar_has_original_royal = yes }
        ai_chance = { base = 70 }
        custom_tooltip = nesnd_postwar_restore_ming_tt
        show_as_tooltip = { activate_law = law_type:law_monarchy add_modifier = { name = USM_not_wuu_post_war_modifier months = 120 } }
        hidden_effect = { nesnd_postwar_restore_original_ming = yes }
    }
    option = {
        name = nesnd_postwar_great_han_option
        default_option = yes
        trigger = { c:SIH ?= this exists = ruler }
        ai_chance = { base = 30 }
        custom_tooltip = nesnd_postwar_great_han_tt
        show_as_tooltip = { activate_law = law_type:law_monarchy }
        hidden_effect = { nesnd_postwar_sih_great_han = yes }
    }
    option = {
        name = nesnd_postwar_hna_republic_option
        default_option = yes
        trigger = { c:HNA ?= this }
        ai_chance = { base = 30 }
        custom_tooltip = nesnd_postwar_hna_republic_tt
        show_as_tooltip = { activate_law = law_type:law_presidential_republic add_modifier = { name = nesnd_hna_republic_gentry_opposition months = 120 } }
        hidden_effect = { nesnd_postwar_hna_republic = yes }
    }
    option = {
        name = nesnd_postwar_gng_option
        default_option = yes
        trigger = { c:GNG ?= this nesnd_postwar_gng_has_local_dynast = yes }
        ai_chance = { base = 100 }
        custom_tooltip = nesnd_postwar_gng_tt
        show_as_tooltip = { activate_law = law_type:law_monarchy add_modifier = { name = USM_not_wuu_post_war_modifier months = 120 } }
        hidden_effect = { nesnd_postwar_gng_restore_ming = yes }
    }
    option = {
        name = nesnd_postwar_wait_option
        default_option = yes
        trigger = { OR = { AND = { c:GNG ?= this NOT = { nesnd_postwar_gng_has_local_dynast = yes } } AND = { c:SIH ?= this NOT = { exists = ruler } NOT = { nesnd_postwar_has_original_royal = yes } } } }
        ai_chance = { base = 1 }
        custom_tooltip = nesnd_postwar_wait_tt
    }
'''
part=part[:-1]+special+'}\n';s=s[:n.start]+part+s[n.end:];write(C/rel,s)
rel='common/dynamic_country_names/ce_dynamic_country_names.txt';s=read(C/rel);n=parse(s).get('USM')
entry='''
    dynamic_country_name = {
        name = nesnd_great_han_name
        adjective = nesnd_great_han_adj
        priority = 1100
        is_main_tag_only = yes
        trigger = { scope:actor ?= { has_variable = nesnd_postwar_great_han } }
    }
'''
write(C/rel,s[:n.vstart+1]+entry+s[n.vstart+1:])
texts={
 'nesnd_great_han_name':('大汉','Great Han'),'nesnd_great_han_adj':('汉','Han'),
 'nesnd_postwar_sih_title':('蜀军入南京','The Army of Shu Enters Nanjing'),
 'nesnd_postwar_sih_desc':('南京已入我军之手，郑氏朝廷无力再维持南方的统治。蜀军起兵时以反吴为号，如今却必须决定天下由谁来统治。有人请求迎回朱氏天子，也有人劝蜀王承继汉统，自立新朝。','Nanjing is in our hands, and the Zheng court can no longer hold the south together. Shu rose against Wu; victory has now placed the succession before its ruler. Some urge the return of the Ming sovereign. Others would have the Prince of Shu establish a Han dynasty of his own.'),
 'nesnd_postwar_hna_title':('南京的国体之议','The Debate in Nanjing'),
 'nesnd_postwar_hna_desc':('襄阳将士以反吴复明为号南下，如今礼议院与各省都在等候新的国体。朱氏复位可以重续明统，共和派却不愿再把国家交给一家一姓。旧日士大夫对于共和政体的疑惧，也不会随着郑氏的失败一并消失。','The army of Xiangyang marched south under the banner of restoring Ming. The Assembly of Rites and the provinces now await a decision on the government. Restoring the Zhu would renew the dynasty’s authority, but republicans refuse to entrust the country to another ruling house. The gentry’s distrust of a republic has survived the fall of Zheng power.'),
 'nesnd_postwar_gng_title':('朱氏再掌明廷','The Zhu Restore Ming Rule'),
 'nesnd_postwar_gng_desc':('淮国宗室仍承朱氏皇统。南京既定，朝臣请淮王正皇帝位，重建明廷的号令。战争留下的分裂尚待弥合，礼议院与各省都将见证这个重新执掌天下的朝廷。','The ruling house of Huai bears the Zhu imperial lineage. With Nanjing secured, the court petitions its prince to take the imperial title and restore Ming authority. The divisions left by war remain, and the Assembly of Rites and the provinces will judge the restored court by what follows.'),
 'nesnd_postwar_restore_ming_option':('迎奉朱氏，重建明廷。','Recall the Zhu and restore the Ming court.'),
 'nesnd_postwar_restore_ming_tt':('迎回在世的原明朝天子；若天子已故，则奉其在世的合法继承人继位，恢复大明国号。','Recall the surviving deposed Ming emperor, or his surviving lawful heir if the emperor is dead, and restore the Ming name.'),
 'nesnd_postwar_great_han_option':('汉家再兴，当在今日。','Let the house of Han rise again.'),
 'nesnd_postwar_great_han_tt':('更改国号为大汉，由本国现任君主继续统治。','Adopt the name Great Han, retaining our current sovereign.'),
 'nesnd_postwar_hna_republic_option':('天下不是一家一姓的私产。','The country belongs to no ruling house.'),
 'nesnd_postwar_hna_republic_tt':('建立共和国。部分士大夫拒绝承认新政体，共和派则将扩大在知识分子与小市民中的影响。','Establish a republic. Sections of the gentry will resist its authority, while republican influence among the intelligentsia and urban middle classes grows.'),
 'nesnd_postwar_gng_option':('奉淮王为帝，复大明之号。','Raise the Prince of Huai to the Ming throne.'),
 'nesnd_postwar_gng_tt':('由淮国本支的在世朱氏君主继承帝位，恢复大明国号。','Restore the Ming name under Huai’s own surviving Zhu sovereign.'),
 'nesnd_postwar_wait_option':('继统之事，尚须再议。','The succession must be considered again.'),
 'nesnd_postwar_wait_tt':('目前没有合适的在世继统人选，暂不改变国体或君主。','No eligible living successor is available. Leave the constitution and ruler unchanged for now.'),
 'nesnd_hna_republic_gentry_opposition':('士绅对共和国的抵制','Gentry Resistance to the Republic'),
}
append_texts(texts)
dump(R/'south-restoration-applied.json',{'country_specific_outcomes':{'SIH':['restore exact Ming sovereign/heir','Great Han under current ruler'],'HNA':['restore exact Ming sovereign/heir','republic'],'GNG':['own local Zhu restoration']},'pending_months':4,'event_duration_months':3,'no_new_royal_characters':True,'no_resurrection':True,'existing_save_victor_recovery':'Absent USM + independent former rebel + entire Nanjing + not previously settled','texts':texts,'engine_verified':False})
print('Restoration integrated: existing victor recovery, exact royal preservation, Ming/Han/republic choices, four-month pending window.')
