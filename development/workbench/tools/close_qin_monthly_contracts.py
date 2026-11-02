from qin_persia_build_support import *
# The unity JE is the sole country-state writer for both cohesion and uprising.
# Every displayed bar resets to that authority in its own pulse. Either JE order
# therefore ends at the same value, without cross-JE double accounting.
p=C/'common/scripted_effects/nesnd_qe1_identity.txt';s=read(p);n=parse(s).get('nesnd_qe1_unity_monthly');body=s[n.start:n.end]
anchor='  nesnd_qe1_unity_sync = yes\n'
assert body.count(anchor)==1
body=body.replace(anchor,'''  if = { limit = { has_variable = nesnd_qe1_uprising_awakened }
   change_variable = { name = nesnd_qe1_uprising add = nesnd_qe1_uprising_delta }
   clamp_variable = { name = nesnd_qe1_uprising min = 0 max = 100 }
  }
'''+anchor)
s=s[:n.start]+body+s[n.end:]
s=s.replace('save_scope_as = nesnd_qe1_declining_state } trigger_event','save_scope_as = nesnd_qe1_declining_state state_region = { save_scope_as = nesnd_qe1_declining_region } } trigger_event')
write(p,s)
p=C/'common/journal_entries/nesnd_qe1_identity.txt';s=read(p);n=parse(s).get('nesnd_qe1_uprising_journal').get('on_monthly_pulse');s=s[:n.start]+'on_monthly_pulse = { effect = { nesnd_qe1_unity_sync = yes } }'+s[n.end:];write(p,s)
key='nesnd_qe1_identity.1.d';LOC[key]=[t.replace("SCOPE.sState('nesnd_qe1_declining_state')","SCOPE.sStateRegion('nesnd_qe1_declining_region')") for t in LOC[key]]
p=C/'events/nesnd_qe1_identity.txt';s=read(p).replace('exists = scope:nesnd_qe1_declining_state scope:', 'exists = scope:nesnd_qe1_declining_state exists = scope:nesnd_qe1_declining_region scope:');write(p,s)
# Recompute power after removing a now-ineligible sponsor; displayed shares must
# not retain the removed concession until next week.
p=C/'common/scripted_effects/nesnd_qe1_court.txt';s=read(p);n=parse(s).get('nesnd_qe1_compute_court');ifn=n.get('if');assign=[a for a in ifn.children if a.key=='set_variable'];calc='\n'.join(s[a.start:a.end] for a in assign)
for a in reversed(assign):s=s[:a.start]+s[a.end:]
n=parse(s).get('nesnd_qe1_compute_court').get('if');li=n.get('limit');s=s[:li.end]+'\n nesnd_qe1_calculate_power_values = yes\n'+s[li.end:]
s=s.replace('nesnd_qe1_prune_patronage = yes','nesnd_qe1_prune_patronage = yes\n if = { limit = { has_variable = nesnd_qe1_power_recalculate } remove_variable = nesnd_qe1_power_recalculate nesnd_qe1_calculate_power_values = yes }',1)
n=parse(s).get('nesnd_qe1_prune_patronage');body=s[n.start:n.end]
for side in ['crown','literati','army']:body=body.replace('remove_variable = nesnd_qe1_patron_'+side,'set_variable = nesnd_qe1_power_recalculate remove_variable = nesnd_qe1_patron_'+side)
s=s[:n.start]+body+s[n.end:];s+='\nnesnd_qe1_calculate_power_values = {\n'+calc+'\n}\n';write(p,s)
loc('nesnd_qe1_balance_bar_desc',"[JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|1]（安国派 −50／统治派 +50）","[JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|1] (Economic −50 / Military +50)")
loc('nesnd_qe1_sol_loyalty_tt','生活改善带来的效忠倾向额外增加#p 15%#!，持续#v 十年#!。','Improving living standards bring 15% additional loyalist momentum for ten years.')
loc('nesnd_qe1_sol_radical_tt','生活下降带来的激进倾向额外增加#n 10%#!，持续#v 十年#!。','Declining living standards bring 10% additional radical momentum for ten years.')
p=C/'events/nesnd_qe1_agendas.txt';s=read(p)
for ev,tip in [('nesnd_qe1.1','nesnd_qe1_sol_loyalty_tt'),('nesnd_qe1.3','nesnd_qe1_sol_radical_tt')]:
 n=parse(s).get(ev).get('option');s=s[:n.end-1]+' custom_tooltip = '+tip+' '+s[n.end-1:]
write(p,s)
p=C/'common/static_modifiers/nesnd_qe1_agendas.txt';s=read(p).replace('nesnd_qe1_stalled = { }','nesnd_qe1_stalled = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_flag_negative.dds" }');write(p,s)
flush_loc();print('Cross-JE display ordering, post-prune power display and persistent region localization closed.')
