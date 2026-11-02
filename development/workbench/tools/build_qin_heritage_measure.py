from qin_persia_context import *
defs={}
for root in [G,B]:
 for p in (root/'common/cultures').glob('*.txt'):
  for n in parse(read(p)).children:defs[n.key.split(':')[-1]]=n
heritages=sorted({n.scalar('heritage') for n in defs.values() if n.scalar('heritage')})
parts=[]
for h in heritages:
 parts.append(f'''nesnd_qe1_share_{h} = {{
 value = 0
 every_scope_culture = {{ limit = {{ has_discrimination_trait = {h} }} root = {{ add = "culture_percent_country(prev)" }} }}
}}''')
parts.append('nesnd_qe1_foreign_heritages = { value = 0\n'+''.join(f'if = {{ limit = {{ NOT = {{ any_primary_culture = {{ has_discrimination_trait = {h} }} }} nesnd_qe1_share_{h} >= 0.01 }} add = 1 }}\n' for h in heritages)+'}\n')
put('common/script_values/nesnd_qe1_heritages.txt','\n'.join(parts))
p=C/'common/script_values/nesnd_qe1_identity.txt';s=read(p);n=parse(s).get('nesnd_qe1_unity_diversity');s=s[:n.start]+'nesnd_qe1_unity_diversity = { value = nesnd_qe1_foreign_heritages multiply = -0.05 }'+s[n.end:];write(p,s)
dump(R/'heritage-contract.json',{'grouping':'actual culture heritage; current primary-culture heritage groups exempt','minimum_combined_population_share':.01,'monthly_cost_per_foreign_group':-.05,'known_heritages':heritages,'politics_culture_count':'significant culture count remains separate for local administrative power','game_launched':False})
print('Explicit shared-heritage grouping generated:',len(heritages))
