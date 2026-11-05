"""Captured-error source contracts. Does not simulate Jomini or certify engine behavior."""
from pathlib import Path
import sys, json, hashlib
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
R=Path(__file__).parent
def load(p): return parse(p.read_text('utf-8-sig'))
def walk(n):
    yield n
    for c in n.children or []: yield from walk(c)
rows=[]
def check(name, pred):
    try: assert pred(); rows.append({'name':name,'pass':True})
    except Exception as e: rows.append({'name':name,'pass':False,'detail':str(e)})
E=load(M/'common/scripted_effects/nesnd_egypt_independence.txt')
A=load(M/'common/scripted_effects/nesnd_american_restoration.txt')
T=load(M/'common/scripted_triggers/nesnd_american_restoration.txt')
N=load(M/'common/scripted_effects/nesnd_regional_native_restoration.txt')
L=load(M/'events/agitators_events/agitators_law_events.txt').get('agitators_law_events.9')
check('No variable access directly on Egypt treaty iterator', lambda: not any(
    c.key in ('set_variable','has_variable','remove_variable')
    for n in walk(E) if n.key=='every_scope_treaty' for c in walk(n)
))
check('Historical expiry before/after 1845 guarded and available on old save', lambda:
    E.get('nesnd_egypt_expire_historical_treaties').get('if').get('limit').get('game_date').value=='1845.1.1'
    and E.get('nesnd_egypt_startup').get('c:EGY').get('nesnd_egypt_expire_historical_treaties') is not None)
check('New later treaties excluded by historical-only selection', lambda:
    E.get('nesnd_egypt_expire_historical_treaty').get('if').get('every_scope_treaty').get('limit').get('is_historical_treaty').value=='yes')
check('Creation initialization called in caller context after create_country', lambda:
    not any(n.key=='on_created' for n in walk(A.get('nesnd_restoration_revolt')))
    and any(n.key=='c:$TAG$' for n in walk(A.get('nesnd_restoration_revolt'))))
check('Dispatch does not clear caller-owned host', lambda:
    not any(n.key=='clear_saved_scope' and n.value=='nesnd_restoration_host' for n in walk(A.get('nesnd_restoration_dispatch'))))
check('Relocation uses explicit guarded selected-state predicate', lambda:
    any(n.key=='nesnd_restoration_state_selected' for n in walk(A.get('nesnd_restoration_relocate_host_capital')))
    and T.get('nesnd_restoration_state_selected') is not None)
check('Regional creation uses caller context too', lambda:
    not any(n.key=='on_created' for n in walk(N.get('nesnd_regional_native_create_tag')))
    and any(n.key=='c:$TAG$' for n in walk(N.get('nesnd_regional_native_create_tag'))))
check('Agitator event9 both option scopes optional and eligibility matches selector', lambda:
    all(o.get('scope:supporting_ig').op=='?=' and o.get('scope:opposing_movement').op=='?=' for o in L.all('option'))
    and L.get('trigger').get('trigger_if').get('any_interest_group') is not None)

# Evaluate ONLY the actual guarded state-comparison AST. Missing RHS raises.
# This is a source-semantic counterexample check, never an engine substitute.
def selected_block(n,state,scopes):
    results=[];branch=None
    for c in n.children or []:
        if c.key=='trigger_if':
            branch=selected_block(c.get('limit'),state,scopes)
            results.append(all(selected_expr(x,state,scopes) for x in c.children if x.key!='limit') if branch else True)
        elif c.key=='trigger_else':
            results.append(selected_block(c,state,scopes) if not branch else True)
        else: results.append(selected_expr(c,state,scopes))
    return all(results)
def selected_expr(n,state,scopes):
    if n.key=='exists': return n.value in scopes
    if n.key=='always': return n.value=='yes'
    if n.key=='this':
        if n.value not in scopes: raise AssertionError('Invalid right side during comparison '+n.value)
        return state==scopes[n.value]
    if n.key=='OR': return any([selected_block(x,state,scopes) for x in n.children])
    if n.key=='AND': return selected_block(n,state,scopes)
    raise AssertionError('Unsupported selected-state AST '+str(n.key))
def selected_matrix():
    t=T.get('nesnd_restoration_state_selected'); cases=0
    for seed in (False,True):
        for second in (False,True):
            scopes={}
            if seed: scopes['scope:nesnd_restoration_seed']='s1'
            if second: scopes['scope:nesnd_restoration_second']='s2'
            for state in ('s1','s2','other'):
                assert selected_block(t,state,scopes)==(state in scopes.values())
                cases+=1
    return cases==12
check('12 selected-state cases include absent seed and optional second',selected_matrix)

# Evaluate the actual historical treaty selection and date nodes, including
# direction-sensitive article predicates. No variables accepted on treaties.
def treaty_filter(n,t,patron):
    out=[]
    for c in n.children or []:
        if c.key=='is_historical_treaty': out.append(t['historical']==(c.value=='yes'))
        elif c.key=='binds': out.append(patron in t['binds'])
        elif c.key=='any_scope_article':
            d=c.get('nesnd_canon_directed_article')
            assert d is not None
            source=d.scalar('SOURCE').replace('$TAG$',patron.removeprefix('c:'))
            target=d.scalar('TARGET').replace('$TAG$',patron.removeprefix('c:'))
            out.append((d.scalar('TYPE'),source,target) in t['articles'])
        else: raise AssertionError('Unsupported treaty filter '+str(c.key))
    return all(out)
def treaty_matrix():
    limit=E.get('nesnd_egypt_expire_historical_treaty').get('if').get('every_scope_treaty').get('limit')
    gate=E.get('nesnd_egypt_expire_historical_treaties').get('if').get('limit').get('game_date')
    assert gate.op=='>='
    patrons=[x.scalar('TAG') for x in E.get('nesnd_egypt_expire_historical_treaties').get('if').all('nesnd_egypt_expire_historical_treaty')]
    assert patrons==['FRA','USM','SIH','GBR','QE1','TUR']
    cases=0
    for p in patrons:
        p='c:'+p
        good=[('foreign_investment_rights','c:EGY',p),('guarantee_independence',p,'c:EGY')]
        for historical in (False,True):
            for variant in ('match','reversed','missing_guarantee','wrong_patron'):
                a=good if variant in ('match','wrong_patron') else [(kind,target,source) for kind,source,target in good] if variant=='reversed' else good[:1]
                t={'historical':historical,'binds':['c:EGY',p] if variant!='wrong_patron' else ['c:EGY','c:RUS'],'articles':a}
                for date in ('1836.1.1','1844.12.31','1845.1.1','1891.1.1'):
                    actual=tuple(map(int,date.split('.')))>=tuple(map(int,gate.value.split('.'))) and treaty_filter(limit,t,p)
                    assert actual==(historical and variant=='match' and date in ('1845.1.1','1891.1.1'))
                    cases+=1
    return cases==192
check('192 treaty date/identity/direction cases protect later treaties',treaty_matrix)
result={'status':'STATIC_PASS' if all(r['pass'] for r in rows) else 'STATIC_FAIL','checks':rows,'engine_run':False}
print(json.dumps(result,ensure_ascii=False,indent=2))
if len(sys.argv)>1: (R/sys.argv[1]).write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
sys.exit(0 if result['status']=='STATIC_PASS' else 1)
