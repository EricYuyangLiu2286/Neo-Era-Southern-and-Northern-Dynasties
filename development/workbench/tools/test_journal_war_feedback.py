from journal_war_context import *
root=Path(sys.argv[1]) if len(sys.argv)>1 else C
rows=[]
def check(name,fn):
    try:fn();rows.append({'name':name,'pass':True})
    except Exception as e:rows.append({'name':name,'pass':False,'detail':str(e)})
def req(x,msg='assertion failed'):
    if not x:raise AssertionError(msg)
def node(rel,key):return parse(read(root/rel)).get(key)
def bars():
    for key in ['nesnd_wu_eastern_question','nesnd_japan_reunification']:
        n=node('common/journal_entries/nesnd_japan.txt',key)
        req(n.get('goal_add_value') is None,'Relative goal captures starting score and can display negative progress')
        req(n.get('scripted_progress_bar') is not None)
check('absolute_japan_readiness_not_relative_growth',bars)
def children():
    for k in ['schools','industry']:
        n=node('common/journal_entries/nesnd_india_core.txt','nesnd_india_'+k)
        req(n.scalar('should_be_pinned_by_default_uninvolved_or_context')=='yes')
        req(n.get('invalid').get('NOT').get('nesnd_india_'+k+'_visible') is not None,'Switching priority must not delete the other journal')
check('delhi_children_stay_visible_when_paused',children)
def parent():
    n=node('common/journal_entries/nesnd_india_core.txt','nesnd_india_reform')
    req(len(n.get('complete').all('custom_tooltip'))==2,'Two independent completed programmes need separate checks')
check('delhi_parent_two_distinct_results',parent)
def market():
    n=node('common/scripted_triggers/nesnd_india_core.txt','nesnd_india_industry_ready')
    for x in n.walk():
        if x.key=='country_has_local_shortage':req(x.value!='root','JE bar root is not a country')
check('delhi_shortage_owner_not_outer_root',market)
def court():
    n=node('common/scripted_triggers/nesnd_war_collapse.txt','nesnd_south_capital_defeat')
    req(any(x.key=='nesnd_ming_court' or x.value=='nesnd_ming_court' for x in n.walk()),'Ming court must remain a defeat target even with legacy missing opposition flag')
    n=node('common/scripted_effects/nesnd_war_collapse.txt','nesnd_check_war_collapses')
    req(any(x.key=='nesnd_south_court_collapse' for x in n.walk()),'Court annexation must not wait for a three-month event option')
check('ming_court_defeat_has_immediate_transaction',court)
def peace():
    n=node('events/usm_civilwar_events.txt','usm_civilwar.9')
    req(not any(x.key=='set_global_variable' and x.value=='nesnd_south_settled' for x in n.walk()),'A ceasefire with surviving opponents is not final settlement')
check('south_ceasefire_not_total_settlement',peace)
phase='baseline' if root==B else 'candidate'
dump(R/f'regression-{phase}.json',{'checks':rows,'status':'PASS' if all(r['pass'] for r in rows) else 'FAIL','engine_verified':False,'source_files':man(root)})
print(phase,'PASS',sum(r['pass'] for r in rows),'FAIL',sum(not r['pass'] for r in rows))
for r in rows:
    if not r['pass']:print(r['name'],r['detail'])
sys.exit(not all(r['pass'] for r in rows))
