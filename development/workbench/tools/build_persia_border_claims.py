from feedback_context import *
rel='common/scripted_triggers/nesnd_per_campaign.txt';s=read(C/rel);tree=parse(s);groups={}
for group in ['levant','egypt','arabia','central_asia','india']:
    n=tree.get('nesnd_per_claim_'+group+'_state')
    groups[group]=[x.value.removeprefix('s:') for x in n.get('OR').children]
    assert groups[group]
# State scope; root is the country pressing a scripted button. Native treaty pattern uses prev identically.
s+='''
nesnd_per_border_claim_state = {
    NOT = { owner = root }
    NOT = { has_claim_by = root }
    root = { is_adjacent_to_state = prev }
}
''';write(C/rel,s)
buttons=[];texts={
 'nesnd_per_border_claim_desc':('向邻州递交领土照会，为朝廷的扩张提出主张。','Send a territorial claim concerning the neighbouring state.'),
 'nesnd_per_claim_interval_tt':('距上次提出领土照会已满一个月。','At least one month has passed since our last territorial claim.'),
}
mapping={}
for group,states in groups.items():
    route='west' if group in ['levant','egypt','arabia'] else 'east'
    for region in states:
        slug=region.removeprefix('STATE_').lower();key='nesnd_per_claim_'+slug+'_button';mapping[key]={'region':region,'route':route}
        texts[key]=(f'宣称${region}$',f'Claim ${region}$')
        texts[key+'_effect_tt']=(f'尝试取得对${region}$的[concept_claim]；强权出面阻挠时，要求会被拒绝。一个月后可再次提出领土照会。',f'Seek a [concept_claim] on ${region}$. A Great Power may block the demand. Another territorial claim may be made after one month.')
        buttons.append(f'''{key} = {{
    name = {key}
    desc = nesnd_per_border_claim_desc
    visible = {{
        has_journal_entry = nesnd_per_{route}_journal
        s:{region} = {{ any_scope_state = {{ nesnd_per_border_claim_state = yes }} }}
    }}
    possible = {{
        custom_tooltip = {{ text = nesnd_per_claim_interval_tt NOT = {{ has_variable = nesnd_per_claim_cooldown }} }}
    }}
    ai_chance = {{ value = 10 if = {{ limit = {{ OR = {{ is_at_war = yes in_default = yes government_legitimacy < 25 }} }} value = 0 }} }}
    effect = {{
        custom_tooltip = {key}_effect_tt
        show_as_tooltip = {{ add_modifier = {{ name = nesnd_per_claim_cost months = 1 }} }}
        hidden_effect = {{
            if = {{
                limit = {{
                    nesnd_per_{route}_eligible = yes
                    has_journal_entry = nesnd_per_{route}_journal
                    NOT = {{ has_variable = nesnd_per_claim_cooldown }}
                    s:{region} = {{ any_scope_state = {{ nesnd_per_border_claim_state = yes }} }}
                }}
                clear_saved_scope = nesnd_per_claim_state
                clear_saved_scope = nesnd_per_claim_region
                s:{region} = {{
                    ordered_scope_state = {{
                        limit = {{ nesnd_per_border_claim_state = yes }}
                        order_by = state_population
                        position = 0
                        check_range_bounds = no
                        save_scope_as = nesnd_per_claim_state
                        state_region = {{ save_scope_as = nesnd_per_claim_region }}
                    }}
                }}
                if = {{
                    limit = {{ exists = scope:nesnd_per_claim_state exists = scope:nesnd_per_claim_region }}
                    nesnd_per_attempt_claim = yes
                }}
            }}
        }}
    }}
}}''')
write(C/'common/scripted_buttons/nesnd_per_border_claims.txt','\n\n'.join(buttons)+'\n')
rel='common/journal_entries/nesnd_per_campaign.txt';s=read(C/rel)
for route,oldgroups in [('west',['levant','egypt','arabia']),('east',['central_asia','india'])]:
    n=parse(s).get('nesnd_per_'+route+'_journal');fragment=s[n.start:n.end]
    oldlines=[f'\tscripted_button = nesnd_per_claim_{group}_button\n' for group in oldgroups]
    assert all(line in fragment for line in oldlines)
    block=''.join('\tscripted_button = '+key+'\n' for key,meta in mapping.items() if meta['route']==route)
    fragment=fragment.replace(oldlines[0],block)
    for line in oldlines[1:]:fragment=fragment.replace(line,'')
    s=s[:n.start]+fragment+s[n.end:]
write(C/rel,s)
rel='common/scripted_buttons/nesnd_per_campaign.txt';s=read(C/rel);tree=parse(s);old=[]
for group in groups:
    n=tree.get('nesnd_per_claim_'+group+'_button');old.append((n.start,n.end,s[n.start:n.end]))
write(R/'legacy-random-claims.txt','\n'.join(t for _,_,t in old))
for a,b,_ in sorted(old,reverse=True):s=s[:a]+s[b:]
write(C/rel,s)
append_texts(texts)
dump(R/'persia-border-claims.json',{'buttons':mapping,'count':len(buttons),'old_button_definitions_archived':True,'scope':'Every button targets one fixed state region; choose largest eligible foreign state segment only within that region; no random region selection.','border_api':'country.is_adjacent_to_state = state; checked both visible and actual execution','economic_cost_and_obstruction_unchanged':True,'game_launched':False})
print(len(buttons),'fixed-state, border-gated Persian claim buttons built.')
