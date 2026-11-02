from qin_persia_context import *
p=C/'common/scripted_effects/nesnd_qe1_identity.txt';s=read(p)
n=parse(s).get('nesnd_qe1_unity_monthly').get('if').get('limit');s=s[:n.end]+'\n nesnd_qe1_measure_heritages = yes\n'+s[n.end:]
s+='''
nesnd_qe1_measure_heritages = {
 if = { limit = { nesnd_qe1_country = yes } set_variable = { name = nesnd_qe1_heritage_count value = nesnd_qe1_foreign_heritages } }
}
''';write(p,s)
p=C/'common/script_values/nesnd_qe1_identity.txt';s=read(p);n=parse(s).get('nesnd_qe1_unity_diversity');s=s[:n.start]+'''nesnd_qe1_unity_diversity = { value = 0 if = { limit = { has_variable = nesnd_qe1_heritage_count } value = var:nesnd_qe1_heritage_count multiply = -0.05 } }'''+s[n.end:];write(p,s)
p=C/'common/scripted_effects/nesnd_qin_persia_lifecycle.txt';s=read(p).replace('nesnd_qe1_capture_barracks = yes','nesnd_qe1_capture_barracks = yes\n if = { limit = { OR = { has_variable = nesnd_qe1_runtime_ready game_date > 1836.1.1 } } nesnd_qe1_measure_heritages = yes }',1);write(p,s)
print('Heritage measurements cached at runtime bootstrap and unity monthly pulse.')
