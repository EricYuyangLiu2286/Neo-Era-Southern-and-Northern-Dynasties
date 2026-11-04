from journal_war_context import *

flight='''# Character scope, called only with a saved fallen country. Confirm relocation before annexation.
nesnd_ming_relocate_royal = {
    if = { limit = { exists = scope:nesnd_court_flight_host }
        transfer_character = scope:nesnd_court_flight_host
    }
    if = { limit = {
            trigger_if = { limit = { exists = scope:nesnd_court_flight_host exists = owner }
                owner = scope:nesnd_court_flight_host
            } trigger_else = { always = no }
        }
        nesnd_ming_give_guest_role = yes
    }
    else = { exile_character_with_role_cleanup = yes }
    if = { limit = {
            is_in_exile_pool = no
            trigger_if = { limit = { exists = owner } owner = scope:nesnd_court_fallen }
            trigger_else = { always = no }
        }
        scope:nesnd_court_fallen = { set_variable = nesnd_ming_flight_blocked }
    }
}
# Country scope. A guest emperor is protected too, without making his host a new court.
nesnd_ming_escape_fallen_court = {
    save_scope_as = nesnd_court_fallen
    clear_saved_scope = nesnd_fleeing_emperor
    clear_saved_scope = nesnd_fleeing_heir
    clear_saved_scope = nesnd_court_flight_host
    remove_variable = nesnd_ming_flight_blocked
    if = { limit = {
            trigger_if = { limit = { exists = var:nesnd_ming_court_monarch }
                var:nesnd_ming_court_monarch = { nesnd_ming_local_royal_for_flight = yes }
            } trigger_else = { always = no }
        }
        var:nesnd_ming_court_monarch = { save_scope_as = nesnd_fleeing_emperor }
    }
    else_if = { limit = {
            trigger_if = { limit = { exists = var:nesnd_ming_claimant_ref }
                var:nesnd_ming_claimant_ref = { nesnd_ming_local_royal_for_flight = yes has_variable = nesnd_ming_claimant }
            } trigger_else = { always = no }
        }
        var:nesnd_ming_claimant_ref = { save_scope_as = nesnd_fleeing_emperor }
    }
    else_if = { limit = {
            has_variable = nesnd_ming_court
            trigger_if = { limit = { exists = ruler } ruler = { nesnd_ming_local_royal_for_flight = yes } }
            trigger_else = { always = no }
        }
        ruler = { save_scope_as = nesnd_fleeing_emperor }
    }
    else_if = { limit = { any_scope_character = { nesnd_ming_local_royal_for_flight = yes has_variable = nesnd_ming_claimant } }
        random_scope_character = { limit = { nesnd_ming_local_royal_for_flight = yes has_variable = nesnd_ming_claimant } save_scope_as = nesnd_fleeing_emperor }
    }
    if = { limit = { exists = scope:nesnd_fleeing_emperor }
        # Snapshot the heir before moving the ruler, which can cause an immediate succession.
        if = { limit = {
                trigger_if = { limit = { exists = var:nesnd_ming_heir_ref }
                    var:nesnd_ming_heir_ref = { nesnd_ming_local_royal_for_flight = yes }
                } trigger_else = { always = no }
            }
            var:nesnd_ming_heir_ref = { save_scope_as = nesnd_fleeing_heir }
        }
        else_if = { limit = { has_variable = nesnd_ming_court any_scope_character = { nesnd_ming_local_royal_for_flight = yes is_heir_of_own_country = yes } }
            random_scope_character = { limit = { nesnd_ming_local_royal_for_flight = yes is_heir_of_own_country = yes } save_scope_as = nesnd_fleeing_heir }
        }
        if = { limit = { any_country = { nesnd_ming_flight_host = yes } }
            random_country = { limit = { nesnd_ming_flight_host = yes } save_scope_as = nesnd_court_flight_host }
        }
        scope:nesnd_fleeing_emperor = { set_variable = nesnd_ming_claimant nesnd_ming_relocate_royal = yes }
        scope:nesnd_fleeing_heir ?= { nesnd_ming_relocate_royal = yes }
        if = { limit = {
                trigger_if = { limit = { exists = scope:nesnd_court_flight_host }
                    scope:nesnd_fleeing_emperor = {
                        trigger_if = { limit = { exists = owner } owner = scope:nesnd_court_flight_host }
                        trigger_else = { always = no }
                    }
                } trigger_else = { always = no }
            }
            scope:nesnd_court_flight_host = {
                set_variable = { name = nesnd_ming_claimant_ref value = scope:nesnd_fleeing_emperor }
                set_variable = nesnd_ming_royals_retained
                if = { limit = { exists = scope:nesnd_fleeing_heir }
                    if = { limit = {
                            scope:nesnd_fleeing_heir = {
                                trigger_if = { limit = { exists = owner } owner = scope:nesnd_court_flight_host }
                                trigger_else = { always = no }
                            }
                        }
                        set_variable = { name = nesnd_ming_heir_ref value = scope:nesnd_fleeing_heir }
                    }
                }
                if = { limit = { OR = { c:HNA ?= this c:SIH ?= this } }
                    set_variable = nesnd_ming_court
                    set_variable = { name = nesnd_ming_court_monarch value = scope:nesnd_fleeing_emperor }
                }
            }
        }
    }
    if = { limit = { NOT = { has_variable = nesnd_ming_flight_blocked } }
        remove_variable = nesnd_ming_court
        remove_variable = nesnd_ming_court_monarch
    }
}
'''
p=C/'common/scripted_effects/nesnd_south_holdouts.txt';s=read(p);n=parse(s).get('nesnd_ming_escape_fallen_court');s=flight+s[n.end:]
# Both immediate court collapse and voluntary surrender are gated on safe royal disposition.
for name in ['nesnd_south_court_collapse','nesnd_holdout_surrender_to_wu']:
    n=parse(s).get(name).get('if');children=n.children;ix=next(i for i,x in enumerate(children) if x.key=='nesnd_ming_escape_fallen_court')
    start=children[ix+1].start;end=children[-1].end
    body=s[start:end]
    s=s[:start]+'if = { limit = { NOT = { has_variable = nesnd_ming_flight_blocked } }\n        '+body+'\n        }'+s[end:]
write(p,s)

p=C/'common/scripted_triggers/nesnd_south_holdouts.txt';s=read(p);n=parse(s).get('nesnd_ming_flight_host')
s=s[:n.start]+'''nesnd_ming_local_royal_for_flight = {
    is_character_alive = yes nesnd_ming_authorized_dynast = yes
    trigger_if = { limit = { exists = owner exists = scope:nesnd_court_fallen }
        owner = scope:nesnd_court_fallen
    } trigger_else = { always = no }
}
nesnd_ming_flight_host = {
    trigger_if = { limit = { exists = scope:nesnd_court_fallen exists = capital exists = c:USM }
        is_country_alive = yes num_states > 0
        NOT = { this = scope:nesnd_court_fallen }
        NOT = { c:USM ?= this }
        NOT = { is_subject_of = c:USM }
        OR = { has_variable = nesnd_restoration_side nesnd_board_stance_value = 1 }
        capital = { controller = prev }
    } trigger_else = { always = no }
}
'''+s[n.end:];write(p,s)

# Legacy punishment first rescues an emperor sheltering outside a named court.
p=C/'events/usm_civilwar_events.txt';s=read(p);n=parse(s).get('usm_civilwar.5').get('after').get('if')
lim=n.get('limit');body=s[lim.end:n.end-1]
replacement=s[n.start:lim.end]+'\n            nesnd_ming_escape_fallen_court = yes\n            if = { limit = { NOT = { has_variable = nesnd_ming_flight_blocked } }'+body+'\n            }\n        }'
s=s[:n.start]+replacement+s[n.end:];write(p,s)

# Capture capital defeat at the battle callback before the following peace can clear occupation.
p=C/'common/on_actions/nesnd_war_collapse.txt';s=read(p)
s=s.replace('c:USM = { nesnd_queue_war_collapse_check = yes }','''c:USM = {
                    every_country = { limit = { has_variable = nesnd_ming_court nesnd_south_capital_defeat = yes }
                        set_variable = nesnd_south_defeat_confirmed
                    }
                    nesnd_queue_war_collapse_check = yes
                }''',1)
s=s.replace('has_variable = usm_opposition_country }','OR = { has_variable = usm_opposition_country has_variable = nesnd_ming_court } }',1)
write(p,s)
print('Royal chain: snapshot heir, confirm owner, exile fallback, block unsafe annex, protect guest on repeated defeat.')
