from qin_persia_build_support import *
import re
# Current engine trigger names, checked against docs and native ip4_je_values.
for p in C.rglob('nesnd_qe1_*.txt'):
 s=read(p);s=re.sub(r'\bclout\b','ig_clout',s);s=re.sub(r'\bapproval\b','ig_approval',s)
 s=s.replace('has_cultural_trait','has_discrimination_trait').replace('STATE_ORENBURG','STATE_UFA')
 s=re.sub(r'OR\s*=\s*\{\s*(state_region\s*=\s*s:STATE_\w+)\s*\}',r'\1',s)
 write(p,s)
for rel,key,tag in [('common/scripted_triggers/nesnd_qe1_campaign.txt','nesnd_qe1_country','QE1'),('common/scripted_triggers/nesnd_per_campaign.txt','nesnd_per_country','PER')]:
 p=C/rel;s=read(p);n=parse(s).get(key)
 body=f'{key} = {{ trigger_if = {{ limit = {{ exists = c:{tag} }} c:{tag} = this is_country_alive = yes }} trigger_else = {{ always = no }} }}'
 write(p,s[:n.start]+body+s[n.end:])
p=C/'common/on_actions/nesnd_qin_persia.txt';s=read(p).replace('c:QE1 ?= this c:PER ?= this','nesnd_qe1_country = yes nesnd_per_country = yes').replace('c:QRC ?= this has_variable','exists = c:QRC c:QRC ?= this has_variable');write(p,s)
p=C/'common/scripted_effects/nesnd_per_campaign.txt';s=read(p)
for tag in ['FRA','MUG','USM','RUS','QE1']:s=s.replace('this = c:'+tag,'AND = { exists = c:'+tag+' c:'+tag+' ?= this }')
write(p,s)
# Barracks target and endpoint comparisons are never evaluated before init.
p=C/'common/scripted_triggers/nesnd_qe1_campaign.txt';s=read(p)
for key,var in [('nesnd_qe1_army_ready','nesnd_qe1_barracks_goal'),('nesnd_qe1_economic_victory','nesnd_qe1_balance'),('nesnd_qe1_military_victory','nesnd_qe1_balance')]:
 n=parse(s).get(key);inner=s[n.vstart+1:n.end-1];replacement=f'{key} = {{ trigger_if = {{ limit = {{ has_variable = {var} }} {inner} }} trigger_else = {{ always = no }} }}';s=s[:n.start]+replacement+s[n.end:]
write(p,s)
# Permanent patronage is explicitly removed by the state machine; no negative month duration.
p=C/'common/scripted_buttons/nesnd_qe1_court.txt';s=read(p).replace(' months = -1','')
for side,laws in {'army':['law_autocracy','law_corporate_state'],'literati':['law_presidential_republic','law_nesnd_qe1_proportional_representation'],'crown':['law_monarchy','law_technocracy']}.items():
 n=parse(s).get('nesnd_qe1_coup_'+side+'_button');vis=n.get('visible');guard=' NOT = { '+ ' '.join('has_law_or_variant = law_type:'+law for law in laws)+' } '
 # All of the desired law set already being active should hide the action.
 guard=' NOT = { AND = { '+ ' '.join('has_law_or_variant = law_type:'+law for law in laws)+' } } '
 s=s[:vis.end-1]+guard+s[vis.end-1:]
write(p,s)
# A newly defined culture requires its six engine-expected modifier shells.
registry={}
for p in (C/'common/static_modifiers').glob('*.txt'):
 s=read(p)
 for n in parse(s).children:
  if n.key.startswith('ce_xiyu_') and any(x in n.key for x in ['standard_of_living_modifier','cultural_acceptance_modifier','fervor_target_modifier']):registry[n.key]=s[n.start:n.end]
assert len(registry)==6,registry.keys()
parts=[]
for k,s in registry.items():
 nk=k.replace('ce_xiyu','nesnd_qe1_conversion_cohort');parts.append(s.replace('ce_xiyu','nesnd_qe1_conversion_cohort'));loc(nk,'$'+k+'$')
put('common/static_modifiers/nesnd_qe1_cohort.txt','\n'.join(parts))
for key,desc in [('dp_nesnd_qe1_civil','双方以武力争夺秦国的统治。'),('dp_nesnd_qe1_frontier','边地诸国向伊犁发动战争。')]:
 loc(key+'_desc',desc);loc(key+'_tooltip',desc)
flush_loc()
dump(R/'source-name-corrections.json',{'ig_numeric':'ig_clout / ig_approval; triggers.log11039/11046 and GAME ip4_je_values.txt28','culture_trait':'has_discrimination_trait; triggers.log10277','north_target':'STATE_UFA (STATE_ORENBURG has no definition)','cohort_modifier_shells':sorted(registry),'optional_identity':'exists branch before country comparison','game_launched':False})
print('Actual engine symbols, culture resource chain and optional-country guards repaired.')
