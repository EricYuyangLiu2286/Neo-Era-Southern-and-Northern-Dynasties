from canon_prose_context import *

for root in (E,C):
    replace_once(root,'events/nesnd_crisis_events.txt',
        'title = nesnd_crisis.30.t desc = nesnd_crisis.30.d',
        '''title = nesnd_crisis.30.t
    desc = {
        first_valid = {
            triggered_desc = {
                trigger = { exists = scope:nesnd_land_petition_state }
                desc = nesnd_crisis.30.local
            }
            desc = nesnd_crisis.30.d
        }
    }''')
    replace_once(root,'events/nesnd_crisis_events.txt',
        'immediate = { set_variable = nesnd_reform_petition_event_seen }',
        '''immediate = {
        set_variable = nesnd_reform_petition_event_seen
        clear_saved_scope = nesnd_land_petition_state
        ordered_scope_state = {
            limit = { nesnd_reform_region = yes }
            order_by = nesnd_reform_state_unemployment_rate
            position = 0
            check_range_bounds = no
            save_scope_as = nesnd_land_petition_state
        }
    }''')
    replace_definition(root,'common/scripted_triggers/nesnd_per_campaign.txt','nesnd_per_aid_live', '''nesnd_per_aid_live = {
    nesnd_per_future_live = yes
    has_variable = nesnd_per_route_aid
    trigger_if = {
        limit = { exists = c:QE1 }
        c:QE1 = { is_country_alive = yes }
        NOT = { has_war_with = c:QE1 }
        trigger_if = {
            limit = { is_subject = yes }
            overlord = { this = c:QE1 }
        }
    }
    trigger_else = { always = no }
}''')
    p=root/'events/nesnd_per_campaign.txt';s=read(p)
    assert s.count('trigger = { nesnd_per_aid_live = yes }')==3
    s=s.replace('trigger = { nesnd_per_aid_live = yes }','trigger = { nesnd_per_aid_live = yes }\n\tcancellation_trigger = { NOT = { nesnd_per_aid_live = yes } }')
    old='title = nesnd_per.4.t desc = nesnd_per.4.d'
    assert s.count(old)==1
    s=s.replace(old,'''title = nesnd_per.4.t
    desc = {
        first_valid = {
            triggered_desc = {
                trigger = {
                    trigger_if = {
                        limit = { exists = c:QE1 }
                        is_subject_of = c:QE1
                        is_subject_type = subject_type_tributary
                    }
                    trigger_else = { always = no }
                }
                desc = nesnd_per.4.d
            }
            desc = nesnd_per.4.d_unavailable
        }
    }''')
    write(p,s)
    for rel in ['events/nesnd_crisis_events.txt','common/scripted_triggers/nesnd_per_campaign.txt','events/nesnd_per_campaign.txt']:
        parse(read(root/rel))
dump(R/'event-context-patch.json',{'roots':[str(E),str(C)],'changes':['crisis30 selected owned reform state plus generic fallback','PER aid verifies surviving nonenemy source and direct overlord if a subject','PER receipt distinguishes actual tributary relation from unavailable relation'],'game_launched':False})
print('Event context patches applied to both isolated candidates; main unchanged.')
