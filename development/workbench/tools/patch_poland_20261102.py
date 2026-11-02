from maintenance_20261102_context import *
import re
bs='common/scripted_buttons/ce_poland_scripted_buttons.txt';ev='events/ce_poland_events.txt';je='common/journal_entries/ce_europe_poland_issude.txt';oa='common/on_actions/ce_code_on_actions.txt'
def replace_child(rel,key,child,body):
 p=C/rel;s=read(p);n=parse(s).get(key);a=n.get(child)
 if a:s=s[:a.start]+body+s[a.end:]
 else:s=s[:n.end-1]+'\n'+body+'\n'+s[n.end-1:]
 write(p,s)
regions=['WEST_GALICIA','UPPER_SILESIA','EAST_GALICIA','POSEN','KAUNAS','BREST','VOLHYNIA','WEST_PRUSSIA','GREATER_POLAND','LESSER_POLAND']
triggers='''nesnd_poland_active = {
 exists = c:KRA
 NOT = { has_global_variable = ce_poland_problem_end }
}
# Country scope; no reference to an absent private journal is evaluated.
nesnd_poland_can_issue_ultimatum = {
 nesnd_poland_active = yes
 is_at_war = no
 NOT = { has_variable = nesnd_polish_pending_state }
 trigger_if = { limit = { has_journal_entry = je_ce_polish_war_preparation }
  je:je_ce_polish_war_preparation = { "scripted_bar_progress(ce_polish_reconquest_war_prep_bar)" >= 100 }
 }
 trigger_else_if = { limit = { has_journal_entry = je_ce_polish_territory_claim }
  je:je_ce_polish_territory_claim = { "scripted_bar_progress(ce_polish_territory_claim_bar)" >= 100 }
 }
 trigger_else = { always = no }
}
# State scope. Shared by availability, selection and reply-time validation.
nesnd_poland_ultimatum_state = {
 trigger_if = { limit = { exists = c:KRA exists = owner }
  NOT = { owner = c:KRA }
  state_region = { has_claim_by = c:KRA }
  owner = {
   NOR = {
    has_subject_relation_with = c:KRA
    is_in_same_power_bloc = c:KRA
    any_scope_treaty = { binds = c:KRA any_scope_article = { has_type = alliance } }
    any_scope_treaty = { binds = c:KRA any_scope_article = { has_type = defensive_pact } }
    any_scope_treaty = { binds = c:KRA any_scope_article = { has_type = guarantee_independence } }
   }
  }
 }
 trigger_else = { always = no }
}
nesnd_poland_ultimatum_valid = {
 trigger_if = { limit = { exists = c:KRA exists = scope:target_diplo_play_state exists = scope:ce_from_country }
  nesnd_poland_active = yes
  is_at_war = no
  c:KRA = { is_subject = no is_diplomatic_play_committed_participant = no }
  scope:ce_from_country = { is_country_alive = yes var:nesnd_polish_pending_state ?= scope:target_diplo_play_state }
  scope:target_diplo_play_state = { owner = root nesnd_poland_ultimatum_state = yes }
 }
 trigger_else = { always = no }
}
nesnd_poland_join_invitation_valid = {
 trigger_if = { limit = { exists = scope:ce_poland_return_land_dp exists = c:KRA }
  nesnd_poland_active = yes
  has_variable = ce_pro_polish_variable
  is_diplomatic_play_committed_participant = no
  NOT = { has_war_with = c:KRA }
  scope:ce_poland_return_land_dp = { is_war = no initiator = c:KRA NOT = { target = root } NOT = { any_scope_play_involved = { this = root } } }
 }
 trigger_else = { always = no }
}
nesnd_poland_existing_successor = {
 OR = {
  # A living POL occupies the tag even before it reaches three incorporated states.
  exists = c:POL
  c:PLC ?= { is_subject = no num_incorporated_states >= 3 }
 }
}
'''
write(C/'common/scripted_triggers/nesnd_poland_repairs.txt',triggers)
effects='''nesnd_poland_pay_ultimatum = {
 if = { limit = { has_journal_entry = je_ce_polish_war_preparation }
  je:je_ce_polish_war_preparation = { add_progress = { name = ce_polish_reconquest_war_prep_bar value = -50 } }
 } else_if = { limit = { has_journal_entry = je_ce_polish_territory_claim }
  je:je_ce_polish_territory_claim = { add_progress = { name = ce_polish_territory_claim_bar value = -50 } }
 }
}
nesnd_poland_clear_request = {
 if = { limit = { exists = scope:ce_from_country exists = scope:target_diplo_play_state }
  scope:ce_from_country = { if = { limit = { var:nesnd_polish_pending_state ?= scope:target_diplo_play_state } remove_variable = nesnd_polish_pending_state } }
 }
}
nesnd_poland_snapshot_stance = {
 if = { limit = { NOT = { has_variable = nesnd_polish_result_resolved } }
  if = { limit = { has_variable = ce_pro_polish_variable } set_variable = nesnd_polish_result_pro remove_variable = nesnd_polish_result_anti }
  else_if = { limit = { has_variable = ce_anti_polish_variable } set_variable = nesnd_polish_result_anti remove_variable = nesnd_polish_result_pro }
 }
}
nesnd_poland_enrol_country = {
 if = { limit = { NOT = { has_variable = nesnd_polish_stance_invited } NOT = { has_global_variable = ce_poland_problem_end } }
  set_variable = nesnd_polish_stance_invited
  if = { limit = { NOR = { has_variable = ce_pro_polish_variable has_variable = ce_anti_polish_variable } }
   trigger_event = { id = ce_poland_events.97 popup = yes }
  }
 }
}
# Called by the contextless JE; scope:journal_entry belongs to this active instance.
nesnd_poland_refresh_participants = {
 if = { limit = { NOT = { has_global_variable = ce_poland_problem_end } exists = scope:journal_entry }
  every_country = { limit = { OR = { has_variable = ce_participated_in_polish_problem any_scope_state = { OR = {
'''+''.join(' state_region = s:STATE_'+r+'\n' for r in regions)+''' } } } NOT = { is_involved_in_journal_entry = je_ce_the_polish_problem } }
   set_variable = ce_participated_in_polish_problem
   scope:journal_entry = { add_involved_country = prev }
   nesnd_poland_enrol_country = yes
  }
 }
}
'''
write(C/'common/scripted_effects/nesnd_poland_repairs.txt',effects)
# Rebuild only the ten mounted ultimatum buttons; retain names and exact AI weights.
p=C/bs;s=read(p);buttons=[n for n in parse(s).children if n.key.startswith('ce_polish_dp_state_')]
assert len(buttons)==10
for n in buttons[::-1]:
 old=s[n.start:n.end];matches=re.findall(r's:(STATE_[A-Z_]+)',old);reg=matches[0];ai=n.get('ai_chance');aitext=s[ai.start:ai.end]
 body=f'''{n.key} = {{
 name = {n.scalar('name')}
 desc = {n.scalar('desc')}
 visible = {{ nesnd_poland_active = yes OR = {{ has_journal_entry = je_ce_polish_war_preparation has_journal_entry = je_ce_polish_territory_claim }} }}
 possible = {{
  nesnd_poland_can_issue_ultimatum = yes
  s:{reg} = {{ any_scope_state = {{ nesnd_poland_ultimatum_state = yes NOT = {{ owner = root }} }} }}
 }}
 {aitext}
 effect = {{
  if = {{ limit = {{ nesnd_poland_can_issue_ultimatum = yes }}
   clear_saved_scope = target_diplo_play_state
   save_scope_as = ce_from_country
   s:{reg} = {{ random_scope_state = {{ limit = {{ nesnd_poland_ultimatum_state = yes NOT = {{ owner = root }} }} save_scope_as = target_diplo_play_state }} }}
   if = {{ limit = {{ exists = scope:target_diplo_play_state }}
    nesnd_poland_pay_ultimatum = yes
    set_variable = {{ name = nesnd_polish_pending_state value = scope:target_diplo_play_state months = 4 }}
    scope:target_diplo_play_state.owner = {{ trigger_event = {{ id = ce_poland_events.2 popup = yes }} }}
   }}
  }}
 }}
}}''';s=s[:n.start]+body+s[n.end:]
write(p,s)
# Correct worldwide state selectors and explicit aid sender.
p=C/bs;s=read(p)
for key in ['ce_anti_polish_radicals_kra_btn','ce_anti_polish_radicals_pro_btn']:
 n=parse(s).get(key);body=s[n.start:n.end].replace('random_state =','random_scope_state =');s=s[:n.start]+body+s[n.end:]
for key in ['ce_pro_polish_give_money_btn','ce_pro_polish_influence_btn']:
 n=parse(s).get(key).get('effect');s=s[:n.vstart+1]+'\n save_scope_as = ce_strong_power\n'+s[n.vstart+1:]
write(p,s)
# Source-side turncoat correction, without changing any non-Polish callback.
p=C/oa;s=read(p);n=parse(s).get('on_ce_poland_war_change_side').get('effect').all('if')[1];t=n.get('scope:target');s=s[:t.start]+s[t.start:t.end].replace('scope:target','scope:initiator',1)+s[t.end:]
# Preserve last declared side before the legacy monthly terminal cleanup removes flags.
n=parse(s).get('ce_monthly_pulse_country').get('effect');s=s[:n.vstart+1]+'\n nesnd_poland_snapshot_stance = yes\n'+s[n.vstart+1:];write(p,s)
# A nonnegative claim count is the tested quantity; avoid object-existence for numeric globals.
p=C/'common/scripted_progress_bars/ce_poland_progress_bars.txt';s=read(p);s=s.replace('global_var:ce_polish_claim_state_count_inverse >= 3','global_var:ce_polish_claim_state_count >= 3');s=re.sub(r'exists = global_var:([A-Za-z_]+)',r'has_global_variable = \1',s);write(p,s)
replace_child(ev,'ce_poland_events.4','option','''option = {
 name = ce_poland_events.4.a
 if = { limit = { has_journal_entry = je_ce_polish_war_preparation }
  je:je_ce_polish_war_preparation = {
   if = { limit = { "scripted_bar_progress(ce_polish_reconquest_war_prep_bar)" >= 10 } add_progress = { name = ce_polish_reconquest_war_prep_bar value = -10 } }
   else = { set_bar_progress = { name = ce_polish_reconquest_war_prep_bar value = 0 } }
  }
 }
 if = { limit = { has_journal_entry = je_ce_polish_reconquest }
  je:je_ce_polish_reconquest = {
   if = { limit = { "scripted_bar_progress(ce_polish_reconquest_energy_bar)" >= 10 } add_progress = { name = ce_polish_reconquest_energy_bar value = -10 } }
   else = { set_bar_progress = { name = ce_polish_reconquest_energy_bar value = 0 } }
  }
 }
}''')
# Matching candidate play, not a global play-independent property of countries.
p=C/ev;s=read(p);n=parse(s).get('ce_poland_events.2');a=next(x for x in n.walk() if x.key=='random_diplomatic_play');li=a.get('limit');s=s[:li.start]+'''limit = { initiator = c:KRA target = root is_diplomatic_play_type = dp_return_state is_war = no }'''+s[li.end:]
n=parse(s).get('ce_poland_events.2');d=next(x for x in n.walk() if x.key=='create_diplomatic_play');body=s[d.start:d.end]
body=body.replace('target_country = root','target_country = root\n target_state = scope:target_diplo_play_state',1)
# Native dp_return_state already makes its initial return-state demand.
dn=parse(body).get('create_diplomatic_play');extra=next(x for x in dn.all('add_war_goal') if x.scalar('type')=='return_state');body=body[:extra.start]+body[extra.end:];s=s[:d.start]+body+s[d.end:]
n=parse(s).get('ce_poland_events.2');invite=next(x for x in n.walk() if x.key=='every_country');li=invite.get('limit');s=s[:li.start]+'''limit = { has_variable = ce_pro_polish_variable NOT = { c:KRA ?= this } NOT = { this = root } exists = scope:ce_poland_return_land_dp }'''+s[li.end:];write(p,s)
for num,predicate in [('2','nesnd_poland_ultimatum_valid'),('7','nesnd_poland_join_invitation_valid')]:
 replace_child(ev,'ce_poland_events.'+num,'trigger',f'trigger = {{ {predicate} = yes }}')
 replace_child(ev,'ce_poland_events.'+num,'cancellation_trigger',f'cancellation_trigger = {{ NOT = {{ {predicate} = yes }} }}')
 p=C/ev;s=read(p);event=parse(s).get('ce_poland_events.'+num)
 for opt in event.all('option')[::-1]:
  metadata={'name','ai_chance','default_option','trigger'};parts=[];actions=[]
  for child in opt.children:
   (parts if child.key in metadata else actions).append(s[child.start:child.end])
  body='option = {\n'+'\n'.join(parts)+f'\n if = {{ limit = {{ {predicate} = yes }}\n'+'\n'.join(actions)+'\n }\n}'
  s=s[:opt.start]+body+s[opt.end:]
 write(p,s)
replace_child(ev,'ce_poland_events.2','after','after = { nesnd_poland_clear_request = yes }')
# Native result and faction cleanup may fire before a player answers a popup.
# Snapshot the current allegiance at every terminal boundary. Keep it until .10/.11 executes.
p=C/je;s=read(p)
for n in parse(s).children[::-1]:
 for callback in [a for a in n.children if a.key in ['on_complete','on_fail','on_invalid','on_complete_all_involved','on_fail_all_involved','on_invalid_all_involved']][::-1]:
  s=s[:callback.vstart+1]+'\n nesnd_poland_snapshot_stance = yes\n'+s[callback.vstart+1:]
write(p,s)
replace_child(je,'je_ce_the_polish_problem','immediate_all_involved','immediate_all_involved = { nesnd_poland_enrol_country = yes }')
replace_child(je,'je_ce_the_polish_problem','on_become_involved_after_activation','on_become_involved_after_activation = { nesnd_poland_enrol_country = yes }')
replace_child(je,'je_ce_the_polish_problem','on_monthly_pulse','on_monthly_pulse = { effect = { nesnd_poland_refresh_participants = yes c:KRA ?= { trigger_event = { id = ce_poland_events.98 } } } }')
p=C/je;s=read(p);n=parse(s).get('je_ce_the_polish_problem').get('invalid');block=next(a for a in n.walk() if a.key=='custom_tooltip' and a.scalar('text')=='ce_je_poland_1_invalid_tt_1');s=s[:block.start]+'nesnd_poland_existing_successor = yes'+s[block.end:];write(p,s)
# Terminal events resolve once at creation; their sole options acknowledge results.
p=C/ev;s=read(p)
for num in ['10','11']:
 n=parse(s).get('ce_poland_events.'+num);im=n.get('immediate');op=n.get('option')
 before='\n'.join(s[x.start:x.end] for x in im.children) if im else ''
 actions='\n'.join(s[x.start:x.end] for x in op.children if x.key!='name')
 payload=(before+'\n'+actions).replace('has_variable = ce_pro_polish_variable','has_variable = nesnd_polish_result_pro').replace('has_variable = ce_anti_polish_variable','has_variable = nesnd_polish_result_anti')
 if num=='10':
  payload=payload.replace('exists = c:KRA c:KRA ?= this','c:KRA ?= this NOT = { exists = c:POL }')
  payload=payload.replace('add_claim = c:POL','add_claim = root')
 # Existing release tags are handled by a dedicated guarded helper below.
 if num=='11':
  tree=parse('x = {'+payload+'}').get('x');kra=next(x for x in tree.all('if') if x.get('limit') and any(y.key=='c:KRA' for y in x.get('limit').walk()));release_if=next(x for x in kra.all('if') if x.get('limit') and any(y.key=='owns_entire_state_region' for y in x.get('limit').walk()))
  tail=tree.children; # replace only this original release tree, preserve rewards/penalties
  # offsets include the x={ prefix, which is 5 characters.
  siblings=kra.children;idx=siblings.index(release_if);last=siblings[idx+1] if idx+1<len(siblings) and siblings[idx+1].key=='else' else release_if
  payload=payload[:release_if.start-5]+'nesnd_poland_failure_secessions = yes'+payload[last.end-5:]
 newim='immediate = {\n nesnd_poland_snapshot_stance = yes\n if = { limit = { NOT = { has_variable = nesnd_polish_result_resolved } }\n set_variable = nesnd_polish_result_resolved\n'+payload+'\n clear_variable_list = ce_list_state_effective\n }\n}'
 newop=f'option = {{ name = {op.scalar("name")} default_option = yes }}'
 replacements=[(im.start,im.end,newim),(op.start,op.end,newop)]
 for a,b,t in sorted(replacements,reverse=True):s=s[:a]+t+s[b:]
write(p,s)
# Victory declaration is transactional: recount now, set once before the notification.
p=C/bs;s=read(p);n=parse(s).get('ce_polish_announce_victory_btn');name=n.key
old=s[n.start:n.end];old=old.replace('effect = {','effect = {\n if = { limit = { nesnd_poland_can_declare_victory = yes }\n set_variable = ce_polish_victory_declared',1);old=old[:-1]+'}\n}'
s=s[:n.start]+old+s[n.end:];write(p,s)
replace_child(bs,name,'possible','possible = { nesnd_poland_can_declare_victory = yes }')
replace_child(ev,'ce_poland_events.3','option','option = { name = ce_poland_events.3.a default_option = yes }')
# Guard the existing-tag secession cases; retain the original failure design and demands.
p=C/'common/scripted_effects/nesnd_poland_repairs.txt';s=read(p)+'''nesnd_poland_failure_secessions = {
 if = { limit = { c:KRA ?= this }
  if = { limit = { owns_entire_state_region = STATE_KAUNAS }
   s:STATE_KAUNAS = { add_homeland = cu:lithuanian add_claim = root }
   if = { limit = { NOT = { exists = c:LIT } }
    create_country = { tag = LIT origin = root state = s:STATE_KAUNAS.region_state:KRA on_created = { set_capital = STATE_KAUNAS } }
   } else = { s:STATE_KAUNAS.region_state:KRA = { set_state_owner = c:LIT } }
   if = { limit = { exists = c:LIT }
    if = { limit = { NOT = { has_war_with = c:LIT } c:LIT = { is_subject = no } is_diplomatic_play_committed_participant = no }
     create_diplomatic_play = { target_country = c:LIT type = dp_annex_war war = yes add_war_goal = { holder = c:LIT type = make_protectorate target_country = root } }
    }
   }
  } else = { every_scope_state = { add_radicals_in_state = { value = 0.05 } } }
  if = { limit = { owns_entire_state_region = STATE_BREST }
   s:STATE_BREST = { add_homeland = cu:byelorussian }
   if = { limit = { NOT = { exists = c:BYE } } create_country = { tag = BYE origin = root state = s:STATE_BREST.region_state:KRA } }
   else = { s:STATE_BREST.region_state:KRA = { set_state_owner = c:BYE } }
  } else = { every_scope_state = { add_radicals_in_state = { value = 0.05 } } }
 }
}
''';write(p,s)
count='nesnd_poland_live_control_count = { value = 0\n'+''.join(f' if = {{ limit = {{ owns_entire_state_region = STATE_{reg} }} add = 1 }}\n' for reg in regions)+'}\n'
write(C/'common/script_values/nesnd_poland_repairs.txt',count)
p=C/'common/scripted_triggers/nesnd_poland_repairs.txt';write(p,read(p)+'''nesnd_poland_can_declare_victory = {
 c:KRA ?= this
 nesnd_poland_active = yes
 NOT = { exists = c:POL }
 NOT = { has_variable = ce_polish_victory_declared }
 nesnd_poland_live_control_count >= 5
}
''')
print('Poland target, resource, faction, terminal, dynamic membership and delayed-request closures patched')
