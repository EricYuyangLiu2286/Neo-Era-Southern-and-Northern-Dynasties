from feedback_context import *
pools={
 'ning':[
 [('阔梁','Kuoliang'),('阔槐','Kuohuai'),('阔棠','Kuotang'),('阔槿','Kuojin')],
 [('作烨','Zuoye'),('作灿','Zuocan'),('作煦','Zuoxu'),('作煐','Zuoying')],
 [('哲坤','Zhekun'),('哲塘','Zhetang'),('哲均','Zhejun'),('哲基','Zheji')],
 [('向钦','Xiangqin'),('向铉','Xiangxuan'),('向铎','Xiangduo'),('向铭','Xiangming')],
 [('亲治','Qinzhi'),('亲浩','Qinhao'),('亲清','Qinqing'),('亲澄','Qincheng')],
 [('衷梁','Zhongliang'),('衷槐','Zhonghuai'),('衷棠','Zhongtang'),('衷槿','Zhongjin')]],
 'huai':[
 [('仲檄','Zhongxi'),('仲梁','Zhongliang'),('仲槐','Zhonghuai'),('仲檀','Zhongtan')],
 [('简煜','Jianyu'),('简焜','Jiankun'),('简烺','Jianlang'),('简炅','Jianjiong')],
 [('靖坤','Jingkun'),('靖塘','Jingtang'),('靖均','Jingjun'),('靖垣','Jingyuan')],
 [('迪钊','Dizhao'),('迪锋','Difeng'),('迪锐','Dirui'),('迪钧','Dijun')],
 [('先流','Xianliu'),('先浩','Xianhao'),('先清','Xianqing'),('先澄','Xiancheng')],
 [('猷梁','Youliang'),('猷棱','Youleng'),('猷松','Yousong'),('猷桐','Youtong')]]}
texts={f'nesnd_ming_{line}_{en.lower()}':(cn,en) for line,gens in pools.items() for names in gens for cn,en in names}
trigger='''nesnd_ming_recruitable_royal = {
    is_character_alive = yes
    nesnd_ming_authorized_dynast = yes
    trigger_if = {
        limit = { exists = owner }
        OR = { owner = root NOR = { is_ruler_of_own_country = yes is_heir_of_own_country = yes } }
    }
}
nesnd_ming_recruitable_huai = { nesnd_ming_recruitable_royal = yes has_variable = nesnd_ming_huai_line }
'''
write(C/'common/scripted_triggers/nesnd_ming_generation.txt',trigger)
eff='''# Character scope: recognize historical identities without renaming existing people.
nesnd_ming_identify_lineage = {
    if = { limit = { OR = { has_template = USM_zhu_kuobing has_variable = this_is_zhukuobin_var } }
        set_variable = nesnd_ming_dynastic_verified set_variable = nesnd_ming_ning_line
        if = { limit = { NOT = { has_variable = nesnd_ming_generation } } set_variable = { name = nesnd_ming_generation value = 0 } }
    }
    if = { limit = { OR = { has_template = USM_zhu_zuoyu has_variable = this_is_zhuzuoyu_var } }
        set_variable = nesnd_ming_dynastic_verified set_variable = nesnd_ming_ning_line
        if = { limit = { NOT = { has_variable = nesnd_ming_generation } } set_variable = { name = nesnd_ming_generation value = 1 } }
    }
    if = { limit = { has_template = USM_zhu_zhongying }
        set_variable = nesnd_ming_dynastic_verified set_variable = nesnd_ming_huai_line
        if = { limit = { NOT = { has_variable = nesnd_ming_generation } } set_variable = { name = nesnd_ming_generation value = 0 } }
    }
    if = { limit = { has_template = USM_zhu_jingyin }
        set_variable = nesnd_ming_dynastic_verified set_variable = nesnd_ming_huai_line
        if = { limit = { NOT = { has_variable = nesnd_ming_generation } } set_variable = { name = nesnd_ming_generation value = 2 } }
    }
}
nesnd_ming_refresh_royal_identity = {
    every_character = { limit = { is_character_alive = yes } nesnd_ming_identify_lineage = yes }
    every_character_in_exile_pool = { limit = { is_character_alive = yes } nesnd_ming_identify_lineage = yes }
    every_character_in_void = { limit = { is_character_alive = yes } nesnd_ming_identify_lineage = yes }
    c:USM ?= { nesnd_mark_original_ming_refs = yes }
    c:HNA ?= { nesnd_mark_original_ming_refs = yes }
    c:SIH ?= { nesnd_mark_original_ming_refs = yes }
    if = { limit = { NOT = { any_character = { is_character_alive = yes has_variable = nesnd_original_ming_emperor } } }
        every_character = { limit = { is_character_alive = yes has_template = USM_zhu_kuobing NOT = { has_variable = nesnd_original_ming_heir } } set_variable = nesnd_original_ming_emperor }
    }
    if = { limit = { NOT = { any_character = { is_character_alive = yes has_variable = nesnd_original_ming_heir } } }
        every_character = { limit = { is_character_alive = yes has_template = USM_zhu_zuoyu NOT = { has_variable = nesnd_original_ming_emperor } } set_variable = nesnd_original_ming_heir }
    }
}
# The new character is a living guest until the accepted restoration option enthrones them.
nesnd_ming_create_dynast = {
    create_character = {
        first_name = $NAME$
        last_name = Zhu
        female = no
        noble = yes
        historical = no
        age = 21
        culture = $CULTURE$
        interest_group = ig_landowners
        ideology = ideology_traditionalist
        on_created = {
            set_variable = nesnd_ming_dynastic_verified
            set_variable = nesnd_ming_generated_dynast
            set_variable = $LINE_FLAG$
            set_variable = { name = nesnd_ming_generation value = $GENERATION$ }
            set_variable = $NAME$
            add_character_role = character_role_nesnd_ming_refuge
            save_scope_as = nesnd_ming_generated_candidate
            set_global_variable = { name = $HIGHWATER$ value = $GENERATION$ }
        }
    }
}
'''
selectors={
 'ning': [('has_variable = nesnd_original_ming_emperor','nesnd_ming_recruitable_royal'),('has_variable = nesnd_original_ming_heir','nesnd_ming_recruitable_royal'),('has_variable = nesnd_ming_ning_line','nesnd_ming_recruitable_royal'),('','nesnd_ming_recruitable_royal')],
 'huai': [('', 'nesnd_ming_recruitable_huai')]}
for line,tiers in selectors.items():
    eff+=f'\nnesnd_ming_find_{line}_dynast = {{\n    clear_saved_scope = nesnd_ming_available_dynast\n'
    # Global priority: original emperor before original heir before other existing dynasts.
    for flag,predicate in tiers:
        for anykind,randomkind in [('any_scope_character','random_scope_character'),('any_character','random_character'),('any_character_in_exile_pool','random_character_in_exile_pool'),('any_character_in_void','random_character_in_void')]:
            condition=(flag+' '+predicate+' = yes').strip()
            eff+=f'''    if = {{
        limit = {{ NOT = {{ exists = scope:nesnd_ming_available_dynast }} {anykind} = {{ {condition} }} }}
        {randomkind} = {{ limit = {{ {condition} }} save_scope_as = nesnd_ming_available_dynast }}
    }}
'''
    eff+='}\n'
    default=1 if line=='ning' else 2
    predicate='nesnd_ming_recruitable_royal' if line=='ning' else 'nesnd_ming_recruitable_huai'
    high=f'nesnd_ming_{line}_generation_highwater';culture='ce_wuu' if line=='ning' else 'ce_xinan'
    eff+=f'''\nnesnd_ming_generate_{line}_dynast = {{
    if = {{
        limit = {{
            nesnd_rebel_can_commit_settlement = yes
            NOT = {{ has_variable = nesnd_ming_generation_in_progress }}
            NOT = {{ has_global_variable = nesnd_ming_generation_cooldown }}
            NOR = {{ any_character = {{ {predicate} = yes }} any_character_in_exile_pool = {{ {predicate} = yes }} any_character_in_void = {{ {predicate} = yes }} }}
        }}
        clear_saved_scope = nesnd_ming_generated_candidate
        set_variable = {{ name = nesnd_ming_generation_in_progress days = 1 }}
        set_global_variable = {{ name = nesnd_ming_generation_cooldown days = 1 }}
        if = {{ limit = {{ NOT = {{ has_global_variable = {high} }} }} set_global_variable = {{ name = {high} value = {default} }} }}
        if = {{
            limit = {{ has_global_variable = {high} }}
            every_character = {{
                limit = {{ has_variable = nesnd_ming_{line}_line has_variable = nesnd_ming_generation }}
                if = {{ limit = {{ var:nesnd_ming_generation > global_var:{high} }} set_global_variable = {{ name = {high} value = var:nesnd_ming_generation }} }}
            }}
'''
    for gen in range(default+1,6):
        head='if' if gen==default+1 else 'else_if'
        comparator='< '+str(gen) if gen<5 else '>= '+str(gen-1)
        eff+=f'            {head} = {{ limit = {{ global_var:{high} {comparator} }}\n                random_list = {{\n'
        for cn,en in pools[line][gen]:
            name=f'nesnd_ming_{line}_{en.lower()}'
            eff+=f'                    1 = {{ nesnd_ming_create_dynast = {{ NAME = {name} CULTURE = cu:{culture} LINE_FLAG = nesnd_ming_{line}_line GENERATION = {gen} HIGHWATER = {high} }} }}\n'
        eff+='                }\n            }\n'
    eff+='''        }
        if = {
            limit = { exists = scope:nesnd_ming_generated_candidate }
            if = { limit = { scope:nesnd_ming_generated_candidate = { is_character_alive = yes owner = root } }
                scope:nesnd_ming_generated_candidate = { save_scope_as = nesnd_ming_available_dynast }
                remove_variable = nesnd_ming_generation_in_progress
            }
        }
    }
}
'''

# Name only genuinely new non-historical heirs, from an explicitly identified parent line.
eff+='''
nesnd_ming_name_new_dynastic_heir = {
    if = {
        limit = { is_historical = no NOT = { has_variable = nesnd_ming_generation } exists = owner }
        owner = { nesnd_ming_refresh_royal_identity = yes }
        if = {
            limit = { owner = { exists = ruler } }
'''
for line,gens in pools.items():
    eff+=f'''            if = {{
                limit = {{ owner.ruler = {{ has_variable = nesnd_ming_{line}_line has_variable = nesnd_ming_generation }} }}
                set_variable = nesnd_ming_dynastic_verified
                set_variable = nesnd_ming_{line}_line
                if = {{
                    limit = {{ owner.ruler = {{ var:nesnd_ming_generation < 5 }} }}
                    set_variable = {{ name = nesnd_ming_generation value = {{ value = owner.ruler.var:nesnd_ming_generation add = 1 }} }}
'''
    for gen in range(1,6):
        eff+=f'                    if = {{ limit = {{ var:nesnd_ming_generation = {gen} }} random_list = {{\n'
        for cn,en in gens[gen]:eff+=f'                        1 = {{ set_first_name = nesnd_ming_{line}_{en.lower()} }}\n'
        eff+='                    } }\n'
    eff+='                }\n            }\n'
eff+='        }\n    }\n}\n'
write(C/'common/scripted_effects/nesnd_ming_generation.txt',eff)
write(C/'common/on_actions/nesnd_ming_generation.txt','''on_heir_born = { on_actions = { nesnd_ming_dynastic_heir_birth } }
nesnd_ming_dynastic_heir_birth = {
    trigger = { exists = owner }
    effect = { nesnd_ming_name_new_dynastic_heir = yes }
}
''')
append_texts(texts)
# Extend selection only at actual accepted settlement; preview never generates a person.
rel='common/scripted_effects/nesnd_south_restoration.txt';s=read(C/rel)
n=parse(s).get('nesnd_postwar_restore_original_ming');body=s[n.start:n.end]
old='''        nesnd_import_original_ming_identity = yes
        nesnd_select_original_ming_royal = yes'''
new='''        nesnd_ming_refresh_royal_identity = yes
        nesnd_ming_find_ning_dynast = yes
        if = { limit = { NOT = { exists = scope:nesnd_ming_available_dynast } } nesnd_ming_generate_ning_dynast = yes }
        clear_saved_scope = nesnd_postwar_original_royal
        if = { limit = { exists = scope:nesnd_ming_available_dynast } scope:nesnd_ming_available_dynast = { save_scope_as = nesnd_postwar_original_royal } }'''
assert old in body;body=body.replace(old,new)
# A generated or other verified living dynast is allowed by the same foreign-ruler guard.
body=body.replace('scope:nesnd_postwar_original_royal = { nesnd_postwar_original_royal_available = yes }','scope:nesnd_postwar_original_royal = { nesnd_ming_recruitable_royal = yes }')
s=s[:n.start]+body+s[n.end:];write(C/rel,s)

rel='common/scripted_effects/nesnd_south_restoration.txt';s=read(C/rel);n=parse(s).get('nesnd_postwar_gng_restore_ming');body=s[n.start:n.end]
body=body.replace('nesnd_rebel_can_commit_settlement = yes nesnd_postwar_gng_has_local_dynast = yes','nesnd_rebel_can_commit_settlement = yes')
body=body.replace('clear_saved_scope = nesnd_postwar_local_sovereign','save_scope_as = nesnd_postwar_winner\n        nesnd_ming_refresh_royal_identity = yes\n        clear_saved_scope = nesnd_postwar_local_sovereign',1)
anchor='''        if = {
            limit = { exists = scope:nesnd_postwar_local_sovereign }'''
insert='''        if = {
            limit = { NOT = { exists = scope:nesnd_postwar_local_sovereign } }
            nesnd_ming_find_huai_dynast = yes
            if = { limit = { NOT = { exists = scope:nesnd_ming_available_dynast } } nesnd_ming_generate_huai_dynast = yes }
            if = { limit = { exists = scope:nesnd_ming_available_dynast } scope:nesnd_ming_available_dynast = { nesnd_postwar_transfer_royal = yes save_scope_as = nesnd_postwar_local_sovereign } }
        }
'''
assert anchor in body;body=body.replace(anchor,insert+anchor,1);s=s[:n.start]+body+s[n.end:];write(C/rel,s)
# Creation is now a legitimate terminal fallback, so no pre-existing-person gate blocks its option.
rel='common/scripted_triggers/nesnd_south_settlement.txt';s=read(C/rel)
s=s.replace('trigger_if = { limit = { c:GNG ?= this } nesnd_postwar_gng_has_local_dynast = yes }','')
write(C/rel,s)
rel='events/usm_civilwar_events.txt';s=read(C/rel);n=parse(s).get('usm_civilwar.10');body=s[n.start:n.end]
body=body.replace('OR = { c:SIH ?= this c:HNA ?= this } nesnd_postwar_has_original_royal = yes','OR = { c:SIH ?= this c:HNA ?= this }')
body=body.replace('trigger = { c:GNG ?= this nesnd_postwar_gng_has_local_dynast = yes }','trigger = { c:GNG ?= this }')
# The extra defer is unnecessary for ordinary GNG fallback; keep only the exceptional unruled SIH case.
old='OR = { AND = { c:GNG ?= this NOT = { nesnd_postwar_gng_has_local_dynast = yes } } AND = { c:SIH ?= this NOT = { exists = ruler } NOT = { nesnd_postwar_has_original_royal = yes } } }'
body=body.replace(old,'c:SIH ?= this NOT = { exists = ruler } NOT = { nesnd_postwar_has_original_royal = yes }')
s=s[:n.start]+body+s[n.end:];write(C/rel,s)
for lang in ['simp_chinese','english']:
    p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzz_nesnd_feedback_l_{lang}.yml';s=read(p)
    replacement=('优先迎回原明朝天子或其合法继承人；若没有可迎奉的在世宗室，则按王系行辈推举新宗室继位，恢复大明国号。不强请别国在位君主或储君。' if lang=='simp_chinese' else 'Recall the deposed Ming emperor or his lawful heir first. If no eligible living royal can be found, establish a new dynast from the documented family line and restore the Ming name. Foreign sovereigns and heirs are not seized.')
    s=re.sub(r'(?m)^(\s*nesnd_postwar_restore_ming_tt:0 )".*"$',lambda m:m[1]+'"'+replacement+'"',s)
    replacement=('由淮王本支朱氏继承帝位；本宗无人可迎奉时，依淮王行辈推举新宗室，恢复大明国号。' if lang=='simp_chinese' else 'Restore Ming under Huai’s own Zhu line. If no eligible dynast of that branch survives, establish a new member following its documented generation names.')
    s=re.sub(r'(?m)^(\s*nesnd_postwar_gng_tt:0 )".*"$',lambda m:m[1]+'"'+replacement+'"',s)
    write(p,s)
dump(R/'ming-generation-applied.json',{'pools':pools,'creation':'Inline new21-year-old nonhistoricalcharacter; no historicaltemplate reuse; living guest until enthronement.','search_order':'original emperor -> originalheir -> Ningline -> other certified royals; each local/global/exile/void. GNG Huailine only.','missing_generation_defaults':{'ning':1,'huai':2},'documented_max_index':5,'newborn_naming':'Only new nonhistoricalheirs of marked parent; no inventedgeneration after documentedlast line.','existing_character_names_unchanged':True,'engine_verified':False})
print('Sourced royal generation fallback and exhaustive recruitment integrated; existing royals retain names and identities.')
