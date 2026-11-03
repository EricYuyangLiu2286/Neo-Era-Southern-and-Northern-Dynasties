from cne_native_context import *
from copy import deepcopy
import math,re
root=Path(sys.argv[1]) if len(sys.argv)>1 else C
rows=[]
def ck(name,fn):
    try:fn();rows.append({'name':name,'pass':True})
    except (AssertionError,ValueError,KeyError,AttributeError) as e:rows.append({'name':name,'pass':False,'detail':str(e)})
def req(v,msg='mismatch'):assert v,msg
def actual(rel):return root/rel if (root/rel).exists() else G/rel
def tree(rel):return parse(read(actual(rel)))
def unchanged(a,b):return shape(a)==shape(b)

def evaluate_age(months,live=True):
    n=tree('common/script_values/nesnd_cne_confidence.txt').get('nesnd_cne_conf_delay');assert n is not None,'missing five-year escalation'
    def cond(n):
        vals=[]
        for x in n.children:
            if x.key=='nesnd_cne_programs_live':vals.append(live==(x.value=='yes'))
            elif x.key=='has_variable':req(x.value=='nesnd_land_months');vals.append(months is not None)
            else:raise AssertionError('unsupported condition '+str(x.key))
        return all(vals)
    def val(n,start=0):
        out=start
        for x in n.children or []:
            if x.key=='limit':continue
            if x.key=='if':
                if cond(x.get('limit')):out=val(x,out)
                continue
            if x.children is not None:v=val(x)
            elif x.value=='yes':v=True
            elif x.value=='var:nesnd_land_months':
                assert months is not None,'unguarded age read';v=months
            else:v=float(x.value)
            if x.key=='value':out=v
            elif x.key=='add':out+=v
            elif x.key=='min':out=max(out,v)
            elif x.key=='divide':out/=v
            elif x.key=='multiply':out*=v
            elif x.key=='floor':req(v is True);out=math.floor(out)
            else:raise AssertionError('unsupported arithmetic '+str(x.key))
        return out
    return val(n)
for months,want in [(None,0),(-1,0),(0,0),(59,0),(60,-25),(61,-25),(119,-25),(120,-50),(179,-50),(180,-75),(240,-100),(600,-250)]:
    ck('elapsed_months_'+str(months),lambda m=months,w=want:req(evaluate_age(m)==w))
ck('settled_reform_no_decay',lambda:req(evaluate_age(600,False)==0))
def same_existing_confidence():
    rel='common/script_values/nesnd_cne_confidence.txt';base=parse(read(B/rel));new=tree(rel)
    for n in base.children:
        q=deepcopy(new.get(n.key));assert q
        if n.key=='nesnd_cne_confidence_annual_change':
            req(sum(x.key=='add' and x.value=='nesnd_cne_conf_delay' for x in q.children)==1)
            q.children=[x for x in q.children if not(x.key=='add' and x.value=='nesnd_cne_conf_delay')]
        req(unchanged(q,n),n.key)
    rel='common/scripted_progress_bars/nesnd_cne_confidence.txt';base=parse(read(B/rel));new=tree(rel)
    adds=new.get('nesnd_cne_confidence_bar').get('yearly_progress').children
    req(sum(x.scalar('value')=='nesnd_cne_conf_delay' for x in adds)==1)
    adds[:]=[x for x in adds if x.scalar('value')!='nesnd_cne_conf_delay']
    req(unchanged(base,new),'bar existing contributions changed')
    for rel in ['common/scripted_effects/nesnd_cne_confidence.txt','common/scripted_effects/nesnd_crisis_effects.txt','common/journal_entries/ce_cne_land_draft.txt','common/scripted_triggers/nesnd_cne_confidence.txt']:
        req(sha(root/rel)==sha(B/rel),'Existing lifecycle changed '+rel)
ck('same_other_costs_recovery_failure_and_sync',same_existing_confidence)

for rel,ids in EVENTS.items():
    def case(rel=rel,ids=ids):
        old=parse(read(G/rel));new=tree(rel)
        req([n.key for n in old.children]==[n.key for n in new.children],'top-level identifiers/namespaces changed')
        for a,b in zip(old.children,new.children):
            if a.key not in ids:req(unchanged(a,b),'Unrelated event '+str(a.key));continue
            req(b.scalar('type')=='country_event' and b.scalar('hidden')=='yes')
            req(b.get('trigger').scalar('always')=='no')
            req(b.get('cancellation_trigger').scalar('always')=='yes')
            req(b.get('type').start<b.get('cancellation_trigger').start)
            req(b.get('immediate').children==[] and not b.all('option'),'effects survive forced call')
    ck('inert_events_'+rel,case)
def gates():
    f=root/'common/scripted_buttons/zzzz_nesnd_native_error_bans.txt'
    n=parse(read(f)).get('REPLACE:christ_of_nations_button') if f.exists() else parse(read(G/'common/scripted_buttons/00_christ_of_europe_buttons.txt')).get('christ_of_nations_button')
    req(n.get('visible').scalar('always')==n.get('possible').scalar('always')=='no');req(n.get('effect').children==[])
    req(n.get('ai_chance').scalar('value')=='0')
    n=tree('common/journal_entries/zzzz_nesnd_native_error_bans.txt').get('REPLACE:je_splitting_oman')
    req(n.scalar('group')=='je_group_historical_content')
    for key in ['possible','complete','fail','is_shown_in_lobby','is_shown_when_inactive']:req(n.get(key).scalar('always')=='no')
    req(n.get('invalid').scalar('always')=='yes');req(not any(x.key in ['on_complete','on_fail','on_invalid','immediate'] for x in n.children))
ck('native_entry_gates_disabled',gates)
def ideology():
    rel='common/ideologies/01_character_ideologies.txt';old=parse(read(G/rel));new=tree(rel);count=0
    req([x.key for x in old.children]==[x.key for x in new.children])
    for a,b in zip(old.children,new.children):
        if a.key!='ideology_integralist':req(unchanged(a,b),str(a.key));continue
        ac,bc=deepcopy(a),deepcopy(b)
        for key in ['interest_group_leader_weight','non_interest_group_leader_weight']:
            aa=ac.get(key).all('if');bb=bc.get(key).all('if');req(len(aa)==len(bb))
            for x,y in zip(aa,bb):
                lim=x.get('limit')
                if lim and lim.get('any_diplomatically_relevant_country'):
                    req(y.get('limit').scalar('always')=='no');y.children[y.children.index(y.get('limit'))]=deepcopy(lim);count+=1
        req(unchanged(ac,bc),'Ideology changes outside two banned limits')
    req(count==2)
ck('two_bad_ideology_weights_only',ideology)
def navy():
    rel='common/naval_battle_conditions/00_naval_battle_conditions.txt';old=parse(read(G/rel));new=tree(rel)
    req([x.key for x in old.children]==[x.key for x in new.children])
    for a,b in zip(old.children,new.children):
        if a.key not in ['naval_condition_cyclone','naval_condition_rough_waters','naval_condition_tropical_storm']:req(unchanged(a,b),str(a.key));continue
        req(b.get('possible').scalar('always')=='no')
        req(b.get('weight').scalar('value')==b.get('intensity').scalar('value')=='0')
        req(not any(x.key in ['fixed_range','range','modifier'] for x in b.walk()))
ck('only_logged_naval_conditions_disabled',navy)
def loc():
    for lang in ['simp_chinese','english']:
        p=root/f'localization/{lang}/replace/zzzzzzzzzzzzzzz_nesnd_native_errors_l_{lang}.yml'
        req(p.exists(),'missing loc '+lang);s=read(p);req(p.read_bytes().startswith(b'\xef\xbb\xbf') and s.startswith('l_'+lang+':'))
        req('CalcCurrentAttackerPowerProjection' not in s and 'CalcCurrentDefenderPowerProjection' not in s and 'NumWantedUnitsDesc' not in s)
        req('nesnd_cne_conf_delay_desc:' in s)
ck('effective_ui_bad_calls_removed_and_age_named',loc)
def data_preserved():
    allowed={'common/script_values/nesnd_cne_confidence.txt','common/scripted_progress_bars/nesnd_cne_confidence.txt','.scratch/debug-release/map.md'}
    for rel,h in man(B).items():
        if rel not in allowed:req(sha(root/rel)==h,'Baseline file changed '+rel)
ck('all_other_existing_files_preserved',data_preserved)
phase='baseline' if root==B else 'candidate'
dump(R/f'regression-{phase}.json',{'status':'PASS' if all(x['pass'] for x in rows) else 'FAIL','checks':rows,'engine_verified':False,'source_files':man(root)})
print(phase,'PASS',sum(x['pass'] for x in rows),'FAIL',sum(not x['pass'] for x in rows))
for row in rows:
    if not row['pass']:print(row['name'],row['detail'])
sys.exit(0 if all(x['pass'] for x in rows) else 1)
