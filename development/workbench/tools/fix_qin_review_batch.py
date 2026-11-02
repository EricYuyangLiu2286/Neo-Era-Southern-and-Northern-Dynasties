from qin_persia_build_support import *
import re
# Native script-value min is a floor, max a ceiling. These are not function names.
p=C/'common/script_values/nesnd_qe1_sol_bonus.txt';s=read(p).replace('max = 0 min = 15','min = 0 max = 15');write(p,s)
p=C/'common/scripted_effects/nesnd_qe1_sol_bonus.txt';s=read(p).replace('max = 0 min = 0.05','min = 0 max = 0.05');write(p,s)
p=C/'common/script_values/nesnd_qe1_identity.txt';s=read(p).replace('subtract = 3 max = 0 multiply = -0.025','subtract = 3 min = 0 multiply = -0.025');write(p,s)
p=C/'common/scripted_effects/nesnd_qe1_court.txt';write(p,read(p).replace('< 35','< 40'))
# A repeated six-month aid cannot refresh itself before its own term ends.
p=C/'common/scripted_effects/nesnd_per_campaign.txt';s=read(p)
for i,mod in [(1,'law'),(2,'building'),(3,'legitimacy')]:s=s.replace(f'10 = {{ trigger_event = {{ id = nesnd_per.{i}',f'10 = {{ trigger = {{ NOT = {{ has_modifier = nesnd_per_aid_{mod} }} }} trigger_event = {{ id = nesnd_per.{i}')
write(p,s)
# A direct law enactment must honour compatibility, not just technology.
p=C/'common/scripted_buttons/nesnd_qe1_court.txt';s=read(p)
n=parse(s).get('nesnd_qe1_coup_literati_button')
for name in ['possible','effect']:
 n=parse(s).get('nesnd_qe1_coup_literati_button');parent=n.get(name) if name=='possible' else n.get('effect').get('if').get('limit');s=s[:parent.end-1]+' NOT = { has_law_or_variant = law_type:law_command_economy } '+s[parent.end-1:]
s=s.replace('activate_law = law_type:law_autocracy activate_law = law_type:law_corporate_state','activate_law = law_type:law_corporate_state activate_law = law_type:law_autocracy');write(p,s)
# Complete the actual present-day Korean/Japanese state definitions, not guessed old names.
add=['STATE_SEOUL','STATE_BUSAN','STATE_SARIWON','STATE_PYONGYANG','STATE_TOKAI','STATE_HOKUSHINETSU','STATE_KYOTO']
p=C/'common/scripted_effects/nesnd_qe1_recovery.txt';s=read(p);n=parse(s).get('nesnd_qe1_recovery_claims');extra=''.join(f's:{r} = {{ add_claim = root }}\n' for r in add if 's:'+r+' ' not in s);write(p,s[:n.end-1]+extra+s[n.end-1:])
q=json.loads(read(R/'recovery-claim-regions.json'));q['regions']=sorted(set(q['regions']+add));dump(R/'recovery-claim-regions.json',q)
# Source-required modifier type chain for the temporary cohort.
p=C/'common/modifier_type_definitions/ce_culture_modifier_types.txt';s=read(p);defs=[]
for n in parse(s).children:
 if 'ce_xiyu' in n.key:
  k=n.key.replace('ce_xiyu','nesnd_qe1_conversion_cohort');defs.append(s[n.start:n.end].replace('ce_xiyu','nesnd_qe1_conversion_cohort'));loc('modifier_'+k,'西域汉羌的'+('生活水平' if 'standard_of_living' in k else '文化接纳' if 'acceptance' in k else '文化热情'));loc('modifier_'+k+'_desc','对西域汉羌人口的影响。')
assert len(defs)==3
put('common/modifier_type_definitions/nesnd_qe1_cohort.txt','\n'.join(defs))
for key in list(LOC):
 if key.startswith('nesnd_qe1_conversion_cohort_') and 'modifier_' in key:
  loc(key,'西域汉羌的'+('生活水平' if 'standard_of_living' in key else '文化接纳' if 'acceptance' in key else '文化热情'))
# Military actors have an action before border objectives have all been completed.
p=C/'common/script_values/nesnd_qe1_agendas.txt';write(p,read(p)+'''\nnesnd_qe1_military_budget = { value = total_income min = 10000 }
nesnd_qe1_military_budget_debit = { value = nesnd_qe1_military_budget multiply = -1 }
''')
p=C/'common/static_modifiers/nesnd_qe1_agendas.txt';write(p,read(p)+'\nnesnd_qe1_military_preparations = { country_military_goods_cost_mult = -0.1 interest_group_ig_armed_forces_approval_add = 1 }\n');loc('nesnd_qe1_military_preparations','军府预备金')
p=C/'common/scripted_buttons/nesnd_qe1_agendas.txt';write(p,read(p)+button('nesnd_qe1_military_budget_button','拨给军府预备金','以一周收入支持军府筹备军需，至少支出一万。军府将据此争取更多的朝议席位。','nesnd_qe1_agenda_live = yes','hidden_trigger = { NOT = { has_variable = nesnd_qe1_military_budget_cooldown } }','set_variable = { name = nesnd_qe1_military_budget_cooldown months = 6 } add_treasury = nesnd_qe1_military_budget_debit add_modifier = { name = nesnd_qe1_military_preparations months = 6 } change_variable = { name = nesnd_qe1_balance add = 10 } nesnd_qe1_watch_endpoints = yes nesnd_qe1_agenda_sync = yes',ai='value = 0 if = { limit = { has_variable = nesnd_qe1_ruler_military gold_reserves >= nesnd_qe1_military_budget in_default = no } add = 8 }'))
p=C/'common/journal_entries/nesnd_qe1_agendas.txt';write(p,read(p).replace('scripted_button = nesnd_qe1_army_petition_button','scripted_button = nesnd_qe1_military_budget_button\n scripted_button = nesnd_qe1_army_petition_button'))
# Use native add_progress to expose the actual balance change; the persistent variable
# still changes once, followed by absolute sync, so the bar cannot double charge.
p=C/'common/scripted_buttons/nesnd_qe1_agendas.txt';s=read(p)
for k in ['nesnd_qe1_economy_push_button','nesnd_qe1_army_petition_button','nesnd_qe1_economy_petition_button','nesnd_qe1_military_budget_button']:
 n=parse(s).get(k);a=next(x for x in n.walk() if x.key=='change_variable' and x.scalar('name')=='nesnd_qe1_balance');v=a.scalar('add');s=s[:a.end]+f'\n je:nesnd_qe1_agenda_journal = {{ add_progress = {{ name = nesnd_qe1_balance_bar value = {v} }} }}'+s[a.end:]
write(p,s)
p=C/'common/scripted_effects/nesnd_qe1_agendas.txt';s=read(p).replace('remove_modifier = nesnd_qe1_law_push remove_modifier = nesnd_qe1_economy_push','remove_modifier = nesnd_qe1_law_push remove_modifier = nesnd_qe1_economy_push remove_modifier = nesnd_qe1_military_preparations');write(p,s)
# Log-first rule: removing an absent modifier is not a harmless cleanup assumption.
wrapped=[]
for p in (C/'common/scripted_effects').glob('nesnd_q*.txt'):
 s=read(p);leaves=[n for n in parse(s).walk() if n.key=='remove_modifier' and n.value]
 for n in reversed(leaves):s=s[:n.start]+f'if = {{ limit = {{ has_modifier = {n.value} }} remove_modifier = {n.value} }}'+s[n.end:]
 if leaves:write(p,s);wrapped.append({'file':p.relative_to(C).as_posix(),'guarded_removals':len(leaves)})
for p in list((C/'common/scripted_effects').glob('nesnd_per*.txt'))+list((C/'common/journal_entries').glob('nesnd_per*.txt')):
 s=read(p);leaves=[n for n in parse(s).walk() if n.key=='remove_modifier' and n.value]
 for n in reversed(leaves):s=s[:n.start]+f'if = {{ limit = {{ has_modifier = {n.value} }} remove_modifier = {n.value} }}'+s[n.end:]
 if leaves:write(p,s);wrapped.append({'file':p.relative_to(C).as_posix(),'guarded_removals':len(leaves)})
dump(R/'review-fixes.json',{'bounded_values_corrected':True,'aid_same_type_cooldown':'current six-month modifier excludes repeat selection','patronage_remove_below':40,'added_recovery_regions':add,'guarded_modifier_removals':wrapped,'military_action':'one-week income floor10000,6months,-10%goods,1approval,10balance','game_launched':False})
flush_loc();print('Both review axes: bounds, cleanup, claims, aid cooldown, law compatibility and military action addressed.')
