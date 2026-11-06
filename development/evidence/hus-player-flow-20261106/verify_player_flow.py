"""Source regression for the reported UI/control-flow defects. No game execution.

The Boolean evaluator below supports only the country predicates used by the
five milestone outcomes. Unknown predicates raise, rather than silently pass.
Native 1.15 JE/outcome/button contracts are documented in task 44.
"""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse, basekey

R=Path(__file__).parent
M=R.parents[2]/'mod/Neo-Era Southern and Northern Dynasties'
B=R/'before'
rows=[]
def check(name, ok):
    rows.append({'check':name,'pass':bool(ok)})
def read(path, root=M): return parse((root/path).read_text('utf-8-sig'))
def shape(n): return (n.key,n.op,n.value,tuple(shape(c) for c in n.children or []))
def conjunction(nodes, variables, facts):
    result=True
    previous=False
    for n in nodes:
        if n.key=='text': continue
        if n.key=='trigger_if':
            previous=conjunction(n.get('limit').children,variables,facts)
            value=not previous or conjunction([c for c in n.children if c.key!='limit'],variables,facts)
        elif n.key=='trigger_else':
            value=previous or conjunction(n.children,variables,facts)
        else: value=predicate(n,variables,facts)
        result=result and value
    return result
def predicate(n, variables, facts):
    if n.key in ('hidden_trigger','custom_tooltip','AND'):
        return conjunction(n.children,variables,facts)
    if n.key=='OR':return any(predicate(c,variables,facts) for c in n.children)
    if n.key in ('NOT','NOR'):return not any(predicate(c,variables,facts) for c in n.children)
    if n.key=='has_variable':return n.value in variables
    if n.key=='always':return n.value=='yes'
    if n.key not in facts:raise ValueError('Unsupported predicate: '+str(n.key))
    left=facts[n.key]
    if n.value in ('yes','no'):return bool(left)==(n.value=='yes')
    right=float(n.value)
    return {'>=':left>=right,'>':left>right,'<':left<right,'<=':left<=right,'=':left==right}[n.op]

old=read('common/journal_entries/nesnd_small_states.txt',B)
new=read('common/journal_entries/nesnd_small_states.txt')
for stem, condition, regional, months in [
    ('economy','nesnd_small_compact_economy',False,12),
    ('governance','nesnd_small_compact_governance',False,12),
    ('regional_economy','nesnd_small_regional_economy',True,12),
    ('regional_governance','nesnd_small_regional_governance',True,12),
    ('order','nesnd_small_order_ready',True,24)]:
    name='nesnd_small_'+stem
    facts={'nesnd_small_state_country':True,condition:True,name+'_months':months}
    variables={name+'_done','nesnd_small_economy_done','nesnd_small_regional_economy_done'}
    if regional:variables.add('nesnd_small_regional')
    before=old.get(name+'_journal').all('outcome')
    after=new.get(name+'_journal').all('outcome')
    eval_out=lambda n,v=variables,f=facts:conjunction(n.get('trigger').children,v,f)
    check(stem+': original completed state also invalid (regression captured)',eval_out(before[0]) and eval_out(before[1]))
    check(stem+': completed succeeds without invalid',not eval_out(after[0]) and eval_out(after[1]))
    facts[condition]=False
    check(stem+': later condition loss does not erase recorded success',eval_out(after[1]))
    variables.discard(name+'_done');facts[name+'_months']=months-1
    check(stem+': premature completion forbidden',not eval_out(after[1]))
    facts['nesnd_small_state_country']=False
    check(stem+': genuine ineligibility closes unfinished JE',eval_out(after[0]) and not eval_out(after[1]))
    check(stem+': no second reward writer',all(o.get('effect') is None for o in after))

# Flatten only presentation wrappers and the two old single-use requirements.
def requirements(nodes, expand):
    out=[]
    for n in nodes:
        if n.key in ('text',):continue
        if n.key in ('hidden_trigger','custom_tooltip'):out.extend(requirements(n.children,expand))
        elif n.key in expand:out.extend(requirements(expand[n.key].children,expand))
        elif n.children is not None:out.append((n.key,n.op,tuple(requirements(n.children,expand))))
        else:out.append((n.key,n.op,n.value))
    return out
before=read('common/scripted_triggers/nesnd_small_states.txt',B)
after=read('common/scripted_triggers/nesnd_small_states.txt')
expanded={k:before.get(k) for k in ('nesnd_small_safe','nesnd_small_regional_industry')}
check('Flattened regional economy keeps original scope/order/numeric requirements',
      requirements(before.get('nesnd_small_regional_economy').children,expanded)==requirements(after.get('nesnd_small_regional_economy').children,{}))
check('No unused regional_industry trampoline',after.get('nesnd_small_regional_industry') is None)
oldvalues=read('common/script_values/nesnd_small_states.txt',B)
newvalues=read('common/script_values/nesnd_small_states.txt')
for k in ('nesnd_small_group_one_transport','nesnd_small_group_two_transport','nesnd_small_group_one_pop','nesnd_small_group_two_pop'):
    check(k+': actual population aggregation unchanged',shape(oldvalues.get(k))==shape(newvalues.get(k)))
labels=read('common/customizable_localization/nesnd_small_regions.txt')
check('Siam name follows recorded group membership, not changing population ordering',any(n.key=='nesnd_small_group_two' for n in labels.walk()) and not any(n.key=='nesnd_small_sia_interior_pop' for n in labels.walk()))
actions=read('common/scripted_triggers/nesnd_small_actions.txt')
button=read('common/scripted_buttons/nesnd_small_states.txt').get('nesnd_small_retarget_button')
for tag, block in [('visibility',button.get('visible')),('execution gate',actions.get('nesnd_small_can_retarget'))]:
    n=next(n for n in block.walk() if n.key=='nesnd_small_populated_states')
    check('Retarget '+tag+' hides/refuses 4 and permits 5',not predicate(n,set(),{'nesnd_small_populated_states':4}) and predicate(n,set(),{'nesnd_small_populated_states':5}))
    check('Retarget '+tag+' requires actual change',any(n.key=='nesnd_small_retarget_changes_groups' for n in block.walk()))
check('Retarget real effect rechecks same eligibility',any(n.key=='nesnd_small_can_retarget' for n in read('common/scripted_effects/nesnd_small_states.txt').get('nesnd_small_retarget').get('if').get('limit').walk()))

# Evaluate the actual membership-difference predicate on populated country states.
# group labels here stand for already validated owner+epoch registrations.
def retarget_test(nodes, states, anchor, current=None):
    def term(n):
        if n.key=='OR':return any(term(c) for c in n.children)
        if n.key=='NOT':return not any(term(c) for c in n.children)
        if n.key=='always':return n.value=='yes'
        if n.key=='exists':return anchor is not None
        if n.key=='any_scope_state':return any(retarget_test(n.children,states,anchor,s) for s in states)
        if n.key=='var:nesnd_small_anchor_one':return retarget_test(n.children,states,anchor,anchor)
        if n.key=='owner':return current['owned']
        if n.key=='this':return current is anchor
        if n.key in ('nesnd_small_group_one','nesnd_small_group_two'):
            return current['group']==(1 if n.key.endswith('one') else 2)
        if n.key=='state_population':return current['pop']>(anchor['pop'] if n.value.startswith('prev.') else float(n.value))
        raise ValueError('Unknown retarget predicate '+str(n.key))
    branch=False;result=True
    for n in nodes:
        if n.key=='trigger_if':
            branch=retarget_test(n.get('limit').children,states,anchor,current)
            value=not branch or retarget_test([c for c in n.children if c.key!='limit'],states,anchor,current)
        elif n.key=='trigger_else':value=branch or retarget_test(n.children,states,anchor,current)
        else:value=term(n)
        result=result and value
    return result
groups=actions.get('nesnd_small_retarget_changes_groups').children
states=[{'pop':p,'group':1 if i==0 else 2,'owned':True} for i,p in enumerate([5000000,2000000,1500000,1000000,400000])]
check('Changing only the second representative does not reset work',not retarget_test(groups,states,states[0]))
states[1]['group']=1
check('Splitting a multi-state first group is a genuine change',retarget_test(groups,states,states[0]))
states[1]['group']=2;states[-1]['group']=None
check('New populated state outside registered groups enables retarget',retarget_test(groups,states,states[0]))
states[-1]['group']=2;states[1]['pop']=6000000
check('A genuinely new largest state enables retarget',retarget_test(groups,states,states[0]))

routes=read('common/journal_entries/nesnd_civic_routes.txt')
hub=routes.get('nesnd_c2_hus_agenda')
check('One registration hub with both choices',{n.value for n in hub.all('scripted_button')}=={'nesnd_hus_register_manchu','nesnd_hus_register_native'})
check('Registration hub has actionable state and settlement',hub.get('status_desc') is not None and any(n.key=='nesnd_hus_registration_settle' for n in hub.walk()))
retired=read('common/journal_entries/nesnd_hus_registration.txt').get('nesnd_hus_registration')
check('Duplicate registration JE retired',retired.get('possible').scalar('always')=='no')
reg=read('common/scripted_effects/nesnd_hus_registration.txt')
for helper,eid in [('nesnd_hus_choose_registration','nesnd_hus_registration.20'),('nesnd_hus_registration_settle','nesnd_hus_registration.21')]:
    check(eid+': one guarded notification call',len([n for n in reg.get(helper).walk() if n.key=='trigger_event' and n.scalar('id')==eid])==1)
    event=read('events/nesnd_hus_registration.txt').get(eid)
    check(eid+': notification never changes law or clock',not any(n.key in ('activate_law','set_variable','change_variable','set_global_variable') for n in event.walk()))
check('Existing registration yearly timer preserved',any(n.key=='set_global_variable' and n.scalar('name')=='nesnd_hus_registration_wait' and n.scalar('years')=='1' for n in reg.get('nesnd_hus_choose_registration').walk()))

old_operating=parse((R/'sol-operating-before.txt').read_text('utf-8-sig'))
new_operating=read('common/scripted_triggers/nesnd_civic_routes.txt')
for route in ('frontier','citizenship','oil'):
    key='nesnd_c2_hus_'+route+'_operating'
    before_body=old_operating.get(key).get('trigger_if')
    old_choices=before_body.all('OR')
    after_body=new_operating.get(key).get('trigger_if')
    branches=[n for n in after_body.children if n.key in ('trigger_if','trigger_else_if')]
    for i,branch in enumerate(branches):
        # Original two ORs each use the identical exclusive choice discriminator.
        building=old_choices[0].children[i]
        political=old_choices[1].children[i]
        check(route+str(i+1)+': same exclusive choice',shape(building.children[0])==shape(political.children[0])==shape(branch.get('limit').children[0]))
        check(route+str(i+1)+': exact building and IG requirements retained',
              [shape(n) for n in building.children[1:]+political.children[1:]]==[shape(n) for n in branch.children if n.key!='limit'])
for name in ('frontier','citizenship','oil'):
    je=routes.get('nesnd_c2_hus_'+name)
    for key in ('possible','is_shown_when_inactive'):
        check(name+': available before choosing, '+key,not any(n.key=='has_variable' and n.value.endswith('_active') for n in je.get(key).walk()))
    check(name+': usable choices, status, bar, outcomes',bool(je.all('scripted_button')) and je.get('status_desc') is not None and je.scalar('scripted_progress_bar') and len(je.all('outcome'))>=2)

supply=read('common/journal_entries/nesnd_supply_journals.txt').get('nesnd_supply_hus_preparations')
check('Trade ready status precedes still-preparing status',supply.get('status_desc').get('first_valid').children[0].scalar('desc')=='nesnd_supply_hus_ready_shared_status')
buttons=read('common/scripted_buttons/nesnd_supply_buttons.txt')
for name in ('shared','autonomous'):
    b=buttons.get('nesnd_supply_finish_'+name)
    check(name+': manual review preserved',b.scalar('autocomplete')!='yes')
    check(name+': visible effect feedback',b.get('effect').scalar('custom_tooltip')=='nesnd_supply_hus_review_effect_tt')
    for weeks in (11,12):
        result=conjunction(b.get('possible').children,set(),{'nesnd_supply_all_ready':True,'nesnd_supply_weeks_value':weeks})
        check(name+': week '+str(weeks),result==(weeks==12))
    check(name+': actual completion written',any(n.key=='set_variable' and n.value=='nesnd_supply_done' for n in b.get('effect').walk()))

egypt=read('common/journal_entries/nesnd_egypt_independence.txt').get('nesnd_egypt_independence')
check('All seven investor choices retained',len(egypt.all('scripted_button'))==7)
check('Egypt explains hidden choices before ordinary status','cooldown' in egypt.get('status_desc').get('first_valid').children[0].scalar('desc'))
e=read('common/scripted_effects/nesnd_egypt_independence.txt')
check('Egypt cooldown is 12 months, not persistent flag',all(n.scalar('months')=='12' for n in e.walk() if n.key=='set_variable' and n.scalar('name')=='nesnd_egypt_choice_cooldown'))

pattern=re.compile(r'^\s*([^\s:#]+):\d*\s*"(.*)"\s*$',re.M)
loc={}
for lang in ('simp_chinese','english'):
    merged={}
    for p in (M/'localization'/lang).rglob('*.yml'):
        merged.update(pattern.findall(p.read_text('utf-8-sig')))
    loc[lang]=merged
changed=[]
for folder in ('common','events','localization'):
    for p in (M/folder).rglob('*'):
        if p.suffix not in ('.txt','.yml'):continue
        rel=p.relative_to(M);old=B/rel
        if old.exists() and old.read_bytes()==p.read_bytes():continue
        changed.append(str(rel).replace('\\','/'))
        if p.suffix=='.txt':
            tree=parse(p.read_text('utf-8-sig'))
            for n in tree.walk():
                if n.key in ('text','desc','conclusion_desc','localization_key') and n.value and n.value.startswith('nesnd_'):
                    check(str(rel)+': '+n.value+' exists in both languages',all(n.value in loc[l] for l in loc))
        else:
            text=p.read_text('utf-8-sig');pairs=pattern.findall(text)
            check(str(rel)+': BOM',p.read_bytes().startswith(b'\xef\xbb\xbf'))
            check(str(rel)+': unique keys',len(pairs)==len(dict(pairs)))
            check(str(rel)+': complete line syntax',all(pattern.fullmatch(line) or not line.strip() or line.lstrip().startswith(('#','l_')) for line in text.splitlines()))
            for k,v in pairs:
                for ref in re.findall(r'\$([^$]+)\$',v):
                    if ref.startswith('nesnd_'):check(k+': referenced key '+ref,ref in loc['english'] and ref in loc['simp_chinese'])
                check(k+': balanced function brackets',v.count('[')==v.count(']'))
check('Parent hub no longer presents population coverage as progress',all('group_one_transport' not in loc[l]['nesnd_small_regional_status'] for l in loc))
check('Regional goal names both groups explicitly',all("GetCustom('nesnd_small_region_one_name')" in loc[l]['nesnd_small_regional_access_status'] for l in loc))
result={'evidence':'STATIC_ONLY','checks':len(rows),'failed':[r for r in rows if not r['pass']],'changed':changed,'rows':rows}
(R/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ('evidence','checks','failed','changed')},ensure_ascii=False,indent=2))
sys.exit(bool(result['failed']))
