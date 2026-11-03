from feedback_context import *
triggers='''nesnd_rebel_unclaimed_total_victory = {
    is_country_alive = yes
    is_subject = no
    has_global_variable = usm_civilwar_occured
    has_variable = usm_opposition_country
    NOT = { has_variable = nesnd_rebel_settlement_seen }
    NOT = { exists = c:USM }
    owns_entire_state_region = STATE_NANJING
}
# Character scope; a living foreign sovereign or designated heir is not seized.
nesnd_postwar_original_royal_available = {
    is_character_alive = yes
    trigger_if = {
        limit = { exists = owner }
        OR = {
            owner = root
            NOR = { is_ruler_of_own_country = yes is_heir_of_own_country = yes }
        }
    }
}
nesnd_postwar_has_original_royal = {
    any_character = {
        OR = { has_variable = nesnd_original_ming_emperor has_variable = nesnd_original_ming_heir }
        nesnd_postwar_original_royal_available = yes
    }
}
nesnd_postwar_gng_has_local_dynast = {
    OR = {
        ruler ?= { is_character_alive = yes nesnd_ming_authorized_dynast = yes }
        any_scope_character = { is_character_alive = yes is_heir_of_own_country = yes nesnd_ming_authorized_dynast = yes }
    }
}
nesnd_postwar_special_victor = { OR = { c:SIH ?= this c:HNA ?= this c:GNG ?= this } }
'''
write(C/'common/scripted_triggers/nesnd_south_restoration.txt',triggers)
effect='''# Reads exact royal references; never infers a claimant from a surname.
nesnd_mark_original_ming_refs = {
'''
for role,refs in [('emperor',['nesnd_ming_claimant_ref','nesnd_ming_refuge_claimant']),('heir',['nesnd_ming_heir_ref','nesnd_ming_refuge_heir'])]:
    for ref in refs:
        effect+=f'''    if = {{
        limit = {{ NOT = {{ any_character = {{ is_character_alive = yes has_variable = nesnd_original_ming_{role} }} }} }}
        if = {{
            limit = {{ exists = var:{ref} }}
            var:{ref} = {{
                if = {{
                    limit = {{ is_character_alive = yes nesnd_ming_authorized_dynast = yes }}
                    set_variable = nesnd_original_ming_{role}
                    set_global_variable = nesnd_ming_original_identity_recorded
                }}
            }}
        }}
    }}
'''
effect+='''}
nesnd_import_original_ming_identity = {
    if = { limit = { NOT = { has_global_variable = nesnd_ming_original_identity_recorded } } c:USM ?= { nesnd_mark_original_ming_refs = yes } }
    if = { limit = { NOT = { has_global_variable = nesnd_ming_original_identity_recorded } } c:HNA ?= { nesnd_mark_original_ming_refs = yes } }
    if = { limit = { NOT = { has_global_variable = nesnd_ming_original_identity_recorded } } c:SIH ?= { nesnd_mark_original_ming_refs = yes } }
}
nesnd_record_original_ming_identity = {
    if = {
        limit = { exists = var:nesnd_ming_claimant_ref }
        if = {
            limit = { var:nesnd_ming_claimant_ref = { is_character_alive = yes nesnd_ming_authorized_dynast = yes } }
            every_character = {
                limit = { OR = { has_variable = nesnd_original_ming_emperor has_variable = nesnd_original_ming_heir } }
                remove_variable = nesnd_original_ming_emperor
                remove_variable = nesnd_original_ming_heir
            }
            nesnd_mark_original_ming_refs = yes
        }
    }
}
nesnd_ming_preserve_unhosted_royals = {
    if = {
        limit = { c:USM ?= this has_variable = tag_WUU_var }
        every_scope_character = {
            limit = { is_character_alive = yes is_ruler_of_own_country = no OR = { has_variable = nesnd_original_ming_emperor has_variable = nesnd_original_ming_heir } }
            exile_character_with_role_cleanup = yes
        }
    }
}
nesnd_select_original_ming_royal = {
    clear_saved_scope = nesnd_postwar_original_royal
    if = {
        limit = { any_character = { has_variable = nesnd_original_ming_emperor nesnd_postwar_original_royal_available = yes } }
        random_character = { limit = { has_variable = nesnd_original_ming_emperor nesnd_postwar_original_royal_available = yes } save_scope_as = nesnd_postwar_original_royal }
    }
    else_if = {
        limit = { any_character = { has_variable = nesnd_original_ming_heir nesnd_postwar_original_royal_available = yes } }
        random_character = { limit = { has_variable = nesnd_original_ming_heir nesnd_postwar_original_royal_available = yes } save_scope_as = nesnd_postwar_original_royal }
    }
}
# Character scope, with an explicit saved winner. Native exile/void recruitment keeps the same person.
nesnd_postwar_transfer_royal = {
    if = {
        limit = { exists = scope:nesnd_postwar_winner is_character_alive = yes }
        save_scope_as = nesnd_postwar_moved_royal
        clear_saved_scope = nesnd_postwar_previous_host
        owner ?= { save_scope_as = nesnd_postwar_previous_host }
        if = { limit = { is_in_void = yes } free_character_from_void = yes }
        if = { limit = { NOT = { owner ?= scope:nesnd_postwar_winner } } transfer_character = scope:nesnd_postwar_winner }
        if = {
            limit = { owner ?= scope:nesnd_postwar_winner }
            if = { limit = { has_modifier = in_exile_modifier } remove_modifier = in_exile_modifier }
            if = { limit = { has_role = character_role_nesnd_ming_refuge } remove_character_role = character_role_nesnd_ming_refuge }
            if = {
                limit = { exists = scope:nesnd_postwar_previous_host }
                scope:nesnd_postwar_previous_host = {
                    if = { limit = { exists = var:nesnd_ming_refuge_claimant } if = { limit = { var:nesnd_ming_refuge_claimant = scope:nesnd_postwar_moved_royal } remove_variable = nesnd_ming_refuge_claimant } }
                    if = { limit = { exists = var:nesnd_ming_refuge_heir } if = { limit = { var:nesnd_ming_refuge_heir = scope:nesnd_postwar_moved_royal } remove_variable = nesnd_ming_refuge_heir } }
                    if = { limit = { NOT = { exists = var:nesnd_ming_refuge_claimant } NOT = { exists = var:nesnd_ming_refuge_heir } } remove_variable = nesnd_ming_refuge_received }
                }
            }
        }
    }
}
nesnd_postwar_clear_constitution = {
    remove_variable = tag_WUU_var
    remove_variable = nesnd_postwar_great_han
    remove_variable = nesnd_ming_interregnum
    remove_variable = nesnd_ming_court
    remove_variable = nesnd_ming_court_monarch
    remove_variable = ce_usm_restoration_of_ming_var
    remove_variable = ce_usm_republican_revolution_tag
    remove_variable = usm_dominion_of_ming_var
}
nesnd_postwar_restore_original_ming = {
    if = {
        limit = { nesnd_rebel_can_commit_settlement = yes OR = { c:SIH ?= this c:HNA ?= this } }
        save_scope_as = nesnd_postwar_winner
        nesnd_import_original_ming_identity = yes
        nesnd_select_original_ming_royal = yes
        if = {
            limit = { exists = scope:nesnd_postwar_original_royal }
            if = {
                limit = { scope:nesnd_postwar_original_royal = { nesnd_postwar_original_royal_available = yes } }
                if = { limit = { exists = ruler } set_variable = { name = nesnd_ming_local_ruler_ref value = ruler } }
                activate_law = law_type:law_monarchy
                scope:nesnd_postwar_original_royal = {
                    nesnd_postwar_transfer_royal = yes
                    if = { limit = { owner ?= scope:nesnd_postwar_winner is_character_alive = yes } set_character_as_ruler = yes }
                }
                if = {
                    limit = { ruler ?= scope:nesnd_postwar_original_royal }
                    nesnd_postwar_clear_constitution = yes
                    set_variable = ce_usm_restoration_of_ming_var
                    set_variable = nesnd_restoration_side
                    nesnd_ming_preserve_local_patron = yes
                    clear_saved_scope = nesnd_postwar_original_heir
                    if = {
                        limit = { any_character = { has_variable = nesnd_original_ming_heir nesnd_postwar_original_royal_available = yes is_ruler_of_own_country = no } }
                        random_character = { limit = { has_variable = nesnd_original_ming_heir nesnd_postwar_original_royal_available = yes is_ruler_of_own_country = no } save_scope_as = nesnd_postwar_original_heir nesnd_postwar_transfer_royal = yes }
                    }
                    if = { limit = { exists = scope:nesnd_postwar_original_heir } if = { limit = { scope:nesnd_postwar_original_heir = { owner ?= scope:nesnd_postwar_winner is_character_alive = yes } } set_heir = scope:nesnd_postwar_original_heir } }
                    add_modifier = { name = USM_not_wuu_post_war_modifier months = 120 }
                    nesnd_commit_rebel_settlement = yes
                }
            }
        }
    }
}
nesnd_postwar_sih_great_han = {
    if = {
        limit = { c:SIH ?= this nesnd_rebel_can_commit_settlement = yes exists = ruler }
        ruler = { save_scope_as = nesnd_postwar_local_sovereign }
        activate_law = law_type:law_monarchy
        if = { limit = { exists = scope:nesnd_postwar_local_sovereign } scope:nesnd_postwar_local_sovereign = { if = { limit = { is_character_alive = yes owner = root } set_character_as_ruler = yes } } }
        nesnd_postwar_clear_constitution = yes
        set_variable = nesnd_postwar_great_han
        nesnd_commit_rebel_settlement = yes
    }
}
nesnd_postwar_hna_republic = {
    if = {
        limit = { c:HNA ?= this nesnd_rebel_can_commit_settlement = yes }
        nesnd_postwar_clear_constitution = yes
        set_variable = ce_usm_republican_revolution_tag
        activate_law = law_type:law_presidential_republic
        add_modifier = { name = nesnd_hna_republic_gentry_opposition months = 120 }
        nesnd_commit_rebel_settlement = yes
    }
}
nesnd_postwar_gng_restore_ming = {
    if = {
        limit = { c:GNG ?= this nesnd_rebel_can_commit_settlement = yes nesnd_postwar_gng_has_local_dynast = yes }
        clear_saved_scope = nesnd_postwar_local_sovereign
        if = { limit = { ruler ?= { is_character_alive = yes nesnd_ming_authorized_dynast = yes } } ruler = { save_scope_as = nesnd_postwar_local_sovereign } }
        else_if = { limit = { any_scope_character = { is_character_alive = yes is_heir_of_own_country = yes nesnd_ming_authorized_dynast = yes } } random_scope_character = { limit = { is_character_alive = yes is_heir_of_own_country = yes nesnd_ming_authorized_dynast = yes } save_scope_as = nesnd_postwar_local_sovereign } }
        if = {
            limit = { exists = scope:nesnd_postwar_local_sovereign }
            activate_law = law_type:law_monarchy
            scope:nesnd_postwar_local_sovereign = { if = { limit = { is_character_alive = yes owner = root } set_character_as_ruler = yes } }
            if = {
                limit = { ruler ?= scope:nesnd_postwar_local_sovereign }
                nesnd_postwar_clear_constitution = yes
                set_variable = ce_usm_restoration_of_ming_var
                set_variable = nesnd_restoration_side
                add_modifier = { name = USM_not_wuu_post_war_modifier months = 120 }
                nesnd_commit_rebel_settlement = yes
            }
        }
    }
}
'''
write(C/'common/scripted_effects/nesnd_south_restoration.txt',effect)
write(C/'common/static_modifiers/nesnd_south_restoration.txt','''nesnd_hna_republic_gentry_opposition = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_negative.dds
    country_authority_mult = -0.20
    country_legitimacy_base_add = -10
    interest_group_ig_landowners_approval_add = -5
    interest_group_ig_intelligentsia_pop_attraction_mult = 0.25
    interest_group_ig_intelligentsia_pol_str_mult = 0.25
    interest_group_ig_petty_bourgeoisie_pop_attraction_mult = 0.25
    interest_group_ig_petty_bourgeoisie_pol_str_mult = 0.25
}
''')
print('Exact original-royal metadata, recall and three country-specific settlement effects prepared.')
