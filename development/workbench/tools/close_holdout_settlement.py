from journal_war_context import *

p=C/'common/scripted_triggers/nesnd_south_holdouts.txt';s=read(p)
s+='''
nesnd_south_unresolved_holdouts = {
    any_country = { nesnd_south_mainland_holdout = yes is_subject = no NOT = { has_variable = nesnd_holdout_resolved } }
}
nesnd_south_campaign_resolved = {
    nesnd_south_campaign_peace = yes
    NOT = { nesnd_south_unresolved_holdouts = yes }
}
nesnd_south_wu_total_victory = {
    c:USM ?= this has_global_variable = usm_civilwar_occured
    nesnd_south_campaign_resolved = yes
    NOT = { any_country = { is_country_alive = yes has_variable = usm_opposition_country NOT = { is_subject_of = root } } }
}
'''
write(p,s)
p=C/'common/scripted_effects/nesnd_south_holdouts.txt';s=read(p);n=parse(s).get('nesnd_holdout_surrender_to_wu');block=s[n.start:n.end]
block=block.replace('        nesnd_holdout_mark_answer = yes\n','',1)
block=block.replace('set_variable = nesnd_holdout_resolved\n','',1)
needle='c:USM = { annex_as_civil_war = scope:nesnd_court_fallen }';assert needle in block
block=block.replace(needle,needle+'''\n        if = { limit = { is_country_alive = no }
            set_variable = nesnd_holdout_resolved
            nesnd_holdout_mark_answer = yes
        }''')
s=s[:n.start]+block+s[n.end:];write(p,s)

p=C/'common/scripted_triggers/nesnd_court_followup.txt';s=read(p);n=parse(s).get('nesnd_south_deadlock_context')
s=s[:n.end-1]+'''    NOT = { AND = { has_global_variable = usm_civilwar_occured nesnd_south_unresolved_holdouts = yes } }
'''+s[n.end-1:];write(p,s)

p=C/'common/journal_entries/ce_usm_the_last_days_of_ming.txt';s=read(p);n=parse(s).get('ce_usm_suppress_rebellion').get('complete')
s=s[:n.start]+'''complete = {
        nesnd_south_wu_total_victory = yes
        NOT = { has_global_variable = nesnd_south_settled }
    }'''+s[n.end:];write(p,s)

p=C/'events/usm_civilwar_events.txt';s=read(p)
for key in ['after','immediate']:
    n=parse(s).get('usm_civilwar.8').get(key);body=s[n.vstart+1:n.vend-1]
    s=s[:n.start]+key+' = { if = { limit = { nesnd_south_wu_total_victory = yes }'+body+' } }'+s[n.end:]
n=parse(s).get('usm_civilwar.8').get('trigger')
s=s[:n.start]+'''trigger = { nesnd_south_wu_total_victory = yes }
    cancellation_trigger = { NOT = { nesnd_south_wu_total_victory = yes } }'''+s[n.end:]
write(p,s)

# Successor occupation state may be unavailable during destruction: guard the capital dereference.
p=C/'common/scripted_triggers/nesnd_war_collapse.txt';s=read(p);s=s.replace('is_country_alive = yes exists = capital','is_country_alive = yes',1)
s=s.replace('''capital = { controller = c:USM }
                    capital = { controller = { is_subject_of = c:USM } }''','''AND = {
                        trigger_if = { limit = { exists = capital }
                            capital = { OR = { controller = c:USM controller = { is_subject_of = c:USM } } }
                        } trigger_else = { always = no }
                    }''',1);write(p,s)
print('Settlement callbacks unified; failed surrender remains eligible for another offer.')
