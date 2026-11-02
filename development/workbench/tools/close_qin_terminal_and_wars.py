from qin_persia_build_support import *
# Terminal callbacks may run after the engine marks/removes their JE. Completion
# effects validate persistent facts, not the continued presence of that same JE.
p=C/'common/scripted_effects/nesnd_per_campaign.txt';s=read(p).replace('limit = { nesnd_per_future_live = yes NOT = { has_variable = nesnd_per_future_done } }','limit = { nesnd_per_future_eligible = yes has_variable = nesnd_per_future_progress }\n if = { limit = { var:nesnd_per_future_progress >= 100 }')
# Close the added guarded numeric branch inside only this terminal effect.
n=parse(s+'\n}').get('nesnd_per_settle_future') if False else None
# The inserted brace is closed just before the next definition; original block
# structure consists of effect -> if, now effect -> if -> if.
marker='\nnesnd_per_attempt_claim = {';idx=s.index(marker);s=s[:idx]+'\n}\n'+s[idx:];parse(s);write(p,s)

p=C/'common/scripted_effects/nesnd_qe1_fracture.txt';s=read(p)
s=s.replace('set_variable = nesnd_qe1_civil_challenger','set_variable = nesnd_qe1_civil_challenger set_variable = { name = nesnd_qe1_war_launch_window days = 90 }')
s=s.replace('set_variable = nesnd_qe1_breakaway_attacker','set_variable = nesnd_qe1_breakaway_attacker set_variable = { name = nesnd_qe1_war_launch_window days = 90 }')
n=parse(s).get('nesnd_qe1_start_civil_war');body=s[n.start:n.end]
body=body.replace('has_variable = nesnd_qe1_civil_challenger NOT', 'has_variable = nesnd_qe1_civil_challenger has_variable = nesnd_qe1_war_launch_window NOT')
body=body.replace('limit = { NOT = { has_war_with = c:QE1 } }','limit = { is_subject = no is_diplomatic_play_committed_participant = no c:QE1 = { is_subject = no } NOT = { has_war_with = c:QE1 } }')
s=s[:n.start]+body+s[n.end:]
n=parse(s).get('nesnd_qe1_start_frontier_war')
body='''nesnd_qe1_start_frontier_war = {
 if = { limit = { has_variable = nesnd_qe1_breakaway_attacker has_variable = nesnd_qe1_war_launch_window exists = c:QE1 NOT = { has_variable = nesnd_qe1_frontier_war_started } }
  clear_saved_scope = nesnd_qe1_frontier_play
  random_diplomatic_play = {
   limit = { target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_frontier initiator = { has_variable = nesnd_qe1_breakaway_attacker } }
   save_scope_as = nesnd_qe1_frontier_play
  }
  if = { limit = { exists = scope:nesnd_qe1_frontier_play }
   if = { limit = { is_subject = no NOT = { has_war_with = scope:nesnd_qe1_frontier_play.initiator } }
    scope:nesnd_qe1_frontier_play = {
     if = { limit = { is_war = yes exists = war }
      war = { if = { limit = { NOT = { is_war_participant = root } } join_war = { target = root side = scope:nesnd_qe1_frontier_play.initiator } } }
     } else_if = { limit = { is_war = no NOT = { any_scope_play_involved = { this = root } } } add_initiator_backers = { root } }
    }
   }
  } else = {
   if = { limit = { is_subject = no is_diplomatic_play_committed_participant = no c:QE1 = { is_subject = no } NOT = { has_war_with = c:QE1 } }
    end_truce = c:QE1
    create_diplomatic_play = { type = dp_nesnd_qe1_frontier target_country = c:QE1 war = yes annex_as_civil_war = no }
   }
  }
  if = { limit = { OR = { has_war_with = c:QE1 nesnd_qe1_has_frontier_play = yes } } set_variable = nesnd_qe1_frontier_war_started }
 }
}'''
s=s[:n.start]+body+s[n.end:];write(p,s)
dump(R/'terminal-war-contract.json',{'PER_terminal':'no dependency on its own active JE; persistent100/done guard','breakaway_war':'one shared frontier war; later countries join same side via native join_war','launch_window_days':90,'sources':['GAME/common/diplomatic_actions/44_enforce_military_access.txt:24-30','engine event_targets.log:109 (DP to war)','GAME/events/soi_events/00_ep1_kazakh_events.txt:303-310'],'countergoal':'native mirrored annexation against coalition leader, not automatic annexation of all backers','game_launched':False})
print('Terminal self-lock removed; breakaway coalition shares a real front and bounded launch window.')
