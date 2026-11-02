from integrity_context import *
import re

def replace_def(rel,key,body):
 p=C/rel;s=read(p);n=parse(s).get(key);assert n is not None
 write(p,s[:n.start]+body.strip()+s[n.end:])

# Correct actual character scope paths; these effects keep the same faction and character.
evidence=json.loads(read(R/'tiger-source-review.json'))
for rel in sorted({x['relative_path'].replace('\\','/') for x in evidence['character_ig_scope_errors']}):
 p=C/rel;s=read(p);edits=[]
 for n in parse(s).walk():
  if n.key=='set_interest_group' and (n.value or '').startswith('ig:'):
   edits.append((n.vstart,n.vend,'owner.'+n.value))
 for start,end,new in reversed(edits):s=s[:start]+new+s[end:]
 assert len(edits)==sum(x['relative_path'].replace('\\','/')==rel for x in evidence['character_ig_scope_errors'])
 write(p,s)

p=C/'common/scripted_triggers/00_ai_triggers.txt';s=read(p)
assert s.count('imposed_law ?= scope:law.type')==1;s=s.replace('imposed_law ?= scope:law.type','imposed_law ?= scope:law')
for i,law in enumerate(['isolationism','freedom_of_conscience','total_separation'],1):
 old=f'scope:law = scope:donghak_desired_law_{i}';assert s.count(old)==1
 s=s.replace(old,f'scope:law = {{ type = law_type:law_{law} }}')
write(p,s)

p=C/'events/ce_fra_unrest_events.txt';s=read(p);event=parse(s).get('fra_unrest.10');blocks=event.all('cancellation_trigger');assert len(blocks)==2
new='''cancellation_trigger = {
		trigger_if = {
			limit = { exists = scope:partisan_character exists = scope:relevant_interest_group }
			OR = {
				NOT = { has_journal_entry = je_ce_unstable_imperium }
				scope:partisan_character = { is_character_alive = no }
			}
		}
		trigger_else = { always = yes }
	}'''
for n in reversed(blocks):s=s[:n.start]+(new if n==blocks[0] else '')+s[n.end:]
write(p,s)

# Conversion recovers a prior orphan batch before marking a new half.
p=C/'common/scripted_effects/nesnd_qe1_identity.txt';s=read(p)
s=s.replace('nesnd_qe1_convert_selected_cohort = {\n','nesnd_qe1_convert_selected_cohort = {\n\tnesnd_qe1_clear_orphan_cohort = yes\n',1);write(p,s)

rel='common/scripted_effects/nesnd_qe1_fracture.txt';p=C/rel;s=read(p);edits=[]
for fn in parse(s).children:
 if not (fn.key.startswith('nesnd_qe1_release_') or fn.key=='nesnd_qe1_check_civil_conflict'):continue
 for n in fn.walk():
  if n.key in ['random_scope_state','ordered_scope_state'] and any(x.key=='save_scope_as' for x in n.children or []):
   t=s[n.start:n.end];limit=n.get('limit');offset=limit.vstart-n.start
   # Offset points to the opening brace of a block.
   t=t[:offset+1]+' state_population > 0 '+t[offset+1:]
   if n.key=='random_scope_state':
    t=t.replace('random_scope_state','ordered_scope_state',1)
    pos=t.rfind('save_scope_as');t=t[:pos]+'order_by = state_population position = 0 check_range_bounds = no '+t[pos:]
   edits.append((n.start,n.end,'clear_saved_scope = '+n.scalar('save_scope_as')+'\n\t\t\t'+t))
  if n.key=='create_country':
   raw=s[n.start:n.end];seed=n.scalar('state')
   if fn.key.startswith('nesnd_qe1_release_'):
    raw=raw.replace('nesnd_qe1_prepare_frontier_army = yes','nesnd_qe1_register_new_frontier = yes')
   edits.append((n.start,n.end,'if = { limit = { exists = '+seed+' }\n\t\t\t\t'+raw+'\n\t\t\t}'))
for start,end,new in sorted(edits,reverse=True):s=s[:start]+new+s[end:]
# Do not consume the one-time civil flag when every noncapital state is empty.
s=s.replace('nesnd_qe1_civil_danger = yes any_scope_state = { is_capital = no }','nesnd_qe1_civil_danger = yes any_scope_state = { is_capital = no state_population > 0 }',1)
write(p,s)
replace_def('common/diplomatic_plays/nesnd_qe1_conflicts.txt','dp_nesnd_qe1_frontier','''dp_nesnd_qe1_frontier = {
	war_goal = humiliation
	texture = "gfx/interface/icons/war_goals/humiliation.dds"
	possible = { always = no }
}''')

old=parse(read(p)).get('nesnd_qe1_prepare_frontier_army')
cleanup=read(p)[old.children[0].start:old.get('save_scope_as').start]
unit=lambda infantry,artillery: '''create_military_formation = {
					name = nesnd_qe1_frontier_army
					type = army
					hq_region = scope:nesnd_qe1_new_frontier.capital.region
					combat_unit = { type = unit_type:combat_unit_type_line_infantry state_region = scope:nesnd_qe1_new_frontier.capital.state_region count = %s }
%s				}'''%(infantry,('\t\t\t\t\tcombat_unit = { type = unit_type:combat_unit_type_cannon_artillery state_region = scope:nesnd_qe1_new_frontier.capital.state_region count = %s }\n'%artillery) if artillery else '')
body='''nesnd_qe1_prepare_frontier_army = {
	if = {
		limit = { has_variable = nesnd_qe1_newly_restored NOT = { has_variable = nesnd_qe1_frontier_force_prepared } }
		set_variable = nesnd_qe1_frontier_force_prepared
		add_technology_researched = line_infantry
		add_technology_researched = artillery
'''+cleanup+'''
		save_scope_as = nesnd_qe1_new_frontier
		if = {
			limit = { army_size = 0 exists = capital }
'''
for i,(population,infantry,artillery) in enumerate([(400000,6,2),(200000,3,1),(100000,2,0),(50000,1,0)]):
 body+='\t\t\t'+('if' if i==0 else 'else_if')+' = {\n\t\t\t\tlimit = { total_population >= '+str(population)+' capital = { state_population >= '+str(population)+' } }\n\t\t\t\t'+unit(infantry,artillery)+'\n\t\t\t}\n'
body+='\t\t}\n\t}\n}'
replace_def(rel,'nesnd_qe1_prepare_frontier_army',body)
write(p,read(p).rstrip()+'''

# Called only from a newborn country callback. Force sizing waits for land transfers.
nesnd_qe1_register_new_frontier = {
	set_variable = nesnd_qe1_newly_restored
	set_variable = nesnd_qe1_breakaway_attacker
	set_variable = { name = nesnd_qe1_war_launch_window days = 90 }
	trigger_event = { id = nesnd_qe1_fracture.91 days = 2 popup = no }
}
''')
replace_def(rel,'nesnd_qe1_start_frontier_war','''nesnd_qe1_start_frontier_war = {
	if = {
		limit = { has_variable = nesnd_qe1_breakaway_attacker has_variable = nesnd_qe1_war_launch_window exists = c:QE1 NOT = { has_variable = nesnd_qe1_frontier_war_started } }
		nesnd_qe1_prepare_frontier_army = yes
		save_scope_as = nesnd_qe1_frontier_actor
		clear_saved_scope = nesnd_qe1_frontier_play
		random_diplomatic_play = {
			limit = { target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_frontier initiator = { has_variable = nesnd_qe1_breakaway_attacker } }
			save_scope_as = nesnd_qe1_frontier_play
		}
		if = {
			limit = { exists = scope:nesnd_qe1_frontier_play }
			if = {
				limit = { is_subject = no NOT = { has_war_with = scope:nesnd_qe1_frontier_play.initiator } }
				scope:nesnd_qe1_frontier_play = {
					if = {
						limit = { is_war = yes exists = war }
						war = { if = { limit = { NOT = { is_war_participant = scope:nesnd_qe1_frontier_actor } } join_war = { target = scope:nesnd_qe1_frontier_actor side = scope:nesnd_qe1_frontier_play.initiator } } }
					}
					else_if = { limit = { is_war = no NOT = { any_scope_play_involved = { this = scope:nesnd_qe1_frontier_actor } } } add_initiator_backers = { scope:nesnd_qe1_frontier_actor } }
					if = {
						limit = {
							any_scope_play_involved = { this = scope:nesnd_qe1_frontier_actor }
							c:QE1 = { NOR = {
								play_participant_has_war_goal_of_type_against = { type = annex_country target = scope:nesnd_qe1_frontier_actor }
								war_participant_has_war_goal_of_type_against = { type = annex_country target = scope:nesnd_qe1_frontier_actor }
							} }
						}
						add_war_goal = { holder = c:QE1 target_country = scope:nesnd_qe1_frontier_actor type = annex_country }
					}
				}
			}
		}
		else = {
			if = {
				limit = { is_subject = no is_diplomatic_play_committed_participant = no c:QE1 = { is_subject = no } NOT = { has_war_with = c:QE1 } }
				end_truce = c:QE1
				create_diplomatic_play = {
					type = dp_nesnd_qe1_frontier target_country = c:QE1 war = yes annex_as_civil_war = no
					add_war_goal = { holder = c:QE1 target_country = scope:nesnd_qe1_frontier_actor type = annex_country }
				}
			}
		}
		if = {
			limit = { OR = {
				has_war_with = c:QE1
				any_diplomatic_play = { target = c:QE1 is_diplomatic_play_type = dp_nesnd_qe1_frontier any_scope_play_involved = { this = scope:nesnd_qe1_frontier_actor } }
			} }
			set_variable = nesnd_qe1_frontier_war_started
		}
	}
}''')
p=C/rel;s=read(p);s=s.replace('nesnd_qe1_setup_civil_challenger = {\n','nesnd_qe1_setup_civil_challenger = {\n\tadd_technology_researched = line_infantry\n\tadd_technology_researched = artillery\n',1);write(p,s)
print('Candidate repaired: source scope/cancellation chains, birth guards, bounded armies, asymmetric frontier goals and cohort preclear.')
