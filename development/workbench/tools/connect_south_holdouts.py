from journal_war_context import *
from pdx import replace_spans

def edit(rel,key,fn):
    p=C/rel;s=read(p);n=parse(s).get(key);assert n,key
    write(p,s[:n.start]+fn(s[n.start:n.end])+s[n.end:])
rel='common/scripted_triggers/nesnd_war_collapse.txt'
def defeat(s):
    s=s.replace('has_variable = usm_opposition_country','OR = { has_variable = usm_opposition_country has_variable = nesnd_ming_court }',1)
    s=s.replace('is_country_alive = yes','is_country_alive = yes exists = capital',1)
    return s
edit(rel,'nesnd_south_capital_defeat',defeat)
edit('common/scripted_effects/nesnd_war_collapse.txt','nesnd_check_war_collapses',lambda s:s.replace('limit = { nesnd_south_capital_defeat = yes NOT = { has_variable = nesnd_capital_surrender_pending } }\n            trigger_event = { id = usm_civilwar.5 popup = yes }','limit = { nesnd_south_capital_defeat = yes }\n            if = { limit = { has_variable = nesnd_ming_court } nesnd_south_court_collapse = yes }\n            else_if = { limit = { NOT = { has_variable = nesnd_capital_surrender_pending } } trigger_event = { id = usm_civilwar.5 popup = yes } }'))
edit('events/usm_civilwar_events.txt','usm_civilwar.5',lambda s:s.replace('immediate = { set_variable = nesnd_capital_surrender_pending }','immediate = { if = { limit = { has_variable = nesnd_ming_court } nesnd_south_court_collapse = yes } else = { set_variable = nesnd_capital_surrender_pending } }'))
def ceasefire(s):
    s=s.replace('trigger = {\n        NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } }','trigger = {\n        nesnd_south_campaign_peace = yes\n        NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } }')
    s=s.replace('immediate = { if = { limit = { NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } } }','immediate = { if = { limit = { nesnd_south_campaign_peace = yes NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } } }')
    s=s.replace('            set_global_variable = nesnd_south_settled\n','')
    return s
edit('events/usm_civilwar_events.txt','usm_civilwar.9',ceasefire)
# Keep the campaign journals during an interval between wars; victory and actual final settlements still close them.
for key in ['ce_usm_suppress_rebellion','ce_usm_restoration_of_ming','ce_usm_acheive_revolution']:
    def ongoing(s):
        n=parse(s).get(key);edits=[(x.start,x.end,'') for x in n.children if x.key in ['fail','on_fail','timeout','on_timeout']]
        s=replace_spans(s,edits)
        if key=='ce_usm_suppress_rebellion':
            s=s[:s.rindex('}')]+'''    invalid = { OR = { NOT = { nesnd_south_wu_survives = yes } has_global_variable = nesnd_south_settled } }
'''+s[s.rindex('}'):]
        return s
    edit('common/journal_entries/ce_usm_the_last_days_of_ming.txt',key,ongoing)
# Use the diplomatic-play hook that actually exists, not an invented on_war_start.
p=C/'common/on_actions/nesnd_south_holdouts.txt';s=read(p);write(p,s[:s.index('# on_war_start')])
def war_start(s):
    n=parse(s).get('dp_usm_civil_war').get('on_war_begins');assert n
    return s[:n.start]+'''on_war_begins = {
        every_country = { limit = { nesnd_south_mainland_holdout = yes has_war_with = c:USM }
            set_variable = { name = nesnd_holdout_enrolled_round value = nesnd_south_round_value }
        }
    }'''+s[n.end:]
edit('common/diplomatic_plays/ce_diplomatic_plays.txt','dp_usm_civil_war',war_start)
p=C/'common/scripted_triggers/nesnd_south_holdouts.txt';s=read(p)
s=s.replace('    NOT = { c:USM ?= { has_variable = nesnd_war_opening_grace } }\n','',1)
write(p,s)
p=C/'common/scripted_effects/nesnd_south_holdouts.txt';s=read(p)
s=s.replace('var:nesnd_ming_court_monarch = { is_character_alive = yes owner = scope:nesnd_court_fallen nesnd_ming_authorized_dynast = yes }','var:nesnd_ming_court_monarch = { is_character_alive = yes nesnd_ming_authorized_dynast = yes trigger_if = { limit = { exists = owner } owner = scope:nesnd_court_fallen } trigger_else = { always = no } }')
old='''            set_global_variable = nesnd_south_settled
        }
    }
}'''
assert s.count(old)==1
s=s.replace(old,'''            if = { limit = { NOT = { has_global_variable = nesnd_south_settled } }
                if = { limit = { NOT = { any_country = { is_country_alive = yes has_variable = usm_opposition_country NOT = { is_subject_of = root } } } }
                    if = { limit = { NOT = { has_variable = usm_government_winner_civilwar } }
                        set_variable = usm_government_winner_civilwar
                        trigger_event = { id = usm_civilwar.8 popup = yes }
                    }
                }
                else = { set_global_variable = usm_civilwar_status_quo }
                set_global_variable = nesnd_south_settled
            }
        }
    }
}''')
write(p,s)
# A reopened southern campaign suspends an uncommitted eastern dossier without choosing its diplomatic outcome.
edit('common/journal_entries/nesnd_japan.txt','nesnd_wu_eastern_question',lambda s:s.replace('invalid = { OR = { NOT = { has_variable = tag_WUU_var }','invalid = { OR = { NOT = { has_global_variable = nesnd_south_settled } NOT = { has_variable = tag_WUU_var }'))
# Normalize only new script files to the project's required UTF-8 BOM.
bm=man(B)
for p in C.rglob('*.txt'):
    if p.relative_to(C).as_posix() not in bm:
        raw=p.read_bytes()
        if not raw.startswith(b'\xef\xbb\xbf'):p.write_bytes(b'\xef\xbb\xbf'+raw)
print('South campaign hooks, immediate court annexation and final-outcome guards connected')
