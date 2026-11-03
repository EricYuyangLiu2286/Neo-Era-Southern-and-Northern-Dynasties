from feedback_context import *
p=C/'common/scripted_effects/nesnd_ming_generation.txt';s=read(p);s=s.replace('owner = { nesnd_ming_refresh_royal_identity = yes }','owner = { if = { limit = { exists = ruler } ruler = { nesnd_ming_identify_lineage = yes } } }');write(p,s)
p=C/'common/on_actions/nesnd_ming_generation.txt';write(p,'''on_heir_born = { on_actions = { nesnd_ming_dynastic_heir_birth } }
nesnd_ming_dynastic_heir_birth = {
    trigger = {
        exists = owner
        owner = {
            exists = ruler
            ruler = { OR = {
                has_variable = nesnd_ming_ning_line
                has_variable = nesnd_ming_huai_line
                has_template = USM_zhu_kuobing
                has_template = USM_zhu_zuoyu
                has_template = USM_zhu_zhongying
                has_template = USM_zhu_jingyin
            } }
        }
    }
    effect = { nesnd_ming_name_new_dynastic_heir = yes }
}
''')
p=C/'common/scripted_effects/nesnd_south_restoration.txt';s=read(p);a=s.index('nesnd_postwar_gng_restore_ming =');head,body=s[:a],s[a:];body=body.replace('nesnd_postwar_ruling_dynast = yes','nesnd_postwar_ruling_dynast = yes ruler = { has_variable = nesnd_ming_huai_line }').replace('nesnd_ming_authorized_dynast = yes','nesnd_ming_authorized_dynast = yes has_variable = nesnd_ming_huai_line');write(p,head+body)
p=W/'tools/probe_persia_journal_ui.py';s=read(p).replace("'country_has_building_type_levels','bt:building_textile_mill'","'country_has_building_type_levels.1','bt:building_textile_mill'");write(p,s)
print('Targeted birth and Huai-line guards applied')
