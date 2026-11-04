"""Strict, ordered source-AST tests. Native APIs are recorded boundary operations,
not a Jomini/runtime simulation. Stop at the first source failure for repair phase.
"""
from canon_routes_context import *
from test_commission_gate_behavior import Evaluator as Base, Obj, SimpleNamespace
from test_commission_effect_boundaries import EffectTrace as BaseTrace
from pdx import effective_files, basekey, unquote
from copy import deepcopy
from datetime import date, timedelta
import calendar, itertools, math, traceback

META=json.loads(read(R/'batch-b-test-snapshot.json')); T=Path(META['snapshot'])
RESULT=R/'batch-b-ast-results.json'
def definitions(folder,roots=(G,T)):
    out={}
    for p in effective_files(roots,folder):
        for n in parse(read(p)).children:
            if n.key:out[basekey(n.key)]=n
    return out

TR=definitions('common/scripted_triggers',(T,))
VAL=definitions('common/script_values',(T,))
EFF=definitions('common/scripted_effects',(T,))
MODS=definitions('common/static_modifiers')
LAWS=definitions('common/laws')
CULT=definitions('common/cultures')
TRAITS=definitions('common/discrimination_traits')
CULTURES={}
for k,n in CULT.items():
    traits={n.scalar('heritage'),n.scalar('language')}-{None}
    for field in ['traditions','traits']:
        if n.get(field):traits.update(n.get(field).values())
    groups={TRAITS[t].scalar('trait_group') for t in traits if t in TRAITS}-{None}
    CULTURES[k]=Obj('culture',k,traits=traits,groups=groups)

def var(o,k,v=1):o.a['vars'].add(k);o.a['variable_values'][k]=v
def country(tag,**extra):
    d=dict(is_country_alive=True,is_at_war=False,has_game_started=True,vars=set(),variable_values={},
           modifiers=set(),modifier_data={},expiries={},journals=set(),states=[],cultures=[],shares={},
           primary=[],laws=set(),tech=set(),institutions={},claims=set(),gdp=10000000,net_fixed_income=5000,
           total_population=1000000,average_sol=10,government_legitimacy=50,bureaucracy=0,
           literacy_rate=.1,country_turmoil=0,radical_population_fraction=0,army_size=50,infamy=0)
    d.update(extra);return Obj('country',tag,**d)
def world(tag='TUR'):
    o=country(tag);return {'countries':{tag:o},'regions':{},'cultures':CULTURES,'saved':{},'day':date(1836,1,15)},o
def shares(o,values):
    o.a['shares']=values;o.a['cultures']=[CULTURES[k] for k in values]
    o.a['total_population']=1000000 if sum(values.values()) else 0
def add_months(d,n):
    y,m=divmod(d.year*12+d.month-1+n,12);m+=1
    return date(y,m,min(d.day,calendar.monthrange(y,m)[1]))

class E(Base):
    def __init__(self,w):self.w=w;self.db=TR;self.values=VAL;self.reads=[]
    def scope(self,k,o,root,prev):
        if k.startswith('cu:'):return self.w['cultures'].get(k[3:])
        if k.startswith('ig:'):return o.a.get('igs',{}).get(k[3:])
        if k.startswith('je:'):
            return Obj('journal',k[3:],owner=o) if k[3:] in o.a['journals'] else None
        return super().scope(k,o,root,prev)
    def expr(self,n,o,root,prev):
        k,v=n.key,n.value
        if k=='has_discrimination_trait':return v in o.a['traits']
        if k=='has_discrimination_trait_group':return v in o.a['groups']
        if k=='has_game_started':return o.a.get(k,False)==(v=='yes')
        if k in ['government_legitimacy','bureaucracy','total_population','gdp','net_fixed_income','literacy_rate','country_turmoil','average_sol','army_size','infamy','radical_population_fraction']:
            return self.cmp(o.a[k],n.op,self.number(v,o,root,prev))
        if k in ['has_claim','owns_entire_state_region']:
            assert o.kind=='country',('wrong country claim/ownership scope',k,o)
            region=self.scope(v,o,root,prev);assert region is not None and region.kind=='region',('missing region',k,v)
            if k=='has_claim':return region.name in o.a['claims']
            return bool(region.a['states']) and all(x.a['owner'] is o for x in region.a['states'])
        if k=='has_claim_by':
            assert o.kind=='state',('state-only has_claim_by used in wrong scope',o)
            target=self.scope(v,o,root,prev);assert target is not None and target.kind=='country'
            return o.a['state_region'].name in target.a['claims']
        if k=='institution_investment_level':
            value=n.get('value');return self.cmp(o.a['institutions'].get(n.scalar('institution'),0),value.op,float(value.value))
        if k in ['has_law','has_law_or_variant']:
            wanted=v.removeprefix('law_type:')
            for actual in o.a['laws']:
                seen=set()
                while actual:
                    if actual==wanted:return True
                    if k=='has_law' or actual in seen:break
                    seen.add(actual);actual=LAWS.get(actual,SimpleNamespace(scalar=lambda x:None)).scalar('parent')
            return False
        if k.startswith('var:'):
            a=self.scope(k,o,root,prev)
            if a is None:raise AssertionError(('unguarded variable read',k,o.name))
            return self.cmp(a,n.op,self.number(v,o,root,prev))
        return super().expr(n,o,root,prev)
    def number(self,t,o,root,prev):
        t=unquote(t)
        if t in self.values and self.values[t].children is None:
            return self.number(self.values[t].value,o,root,prev)
        if t.startswith('culture_percent_country('):
            assert o.kind=='country',('wrong population-share scope',o)
            assert o.a['total_population']>0,('unguarded zero-population native share read',o.name)
            target=self.scope(t[len('culture_percent_country('):-1],o,root,prev)
            assert target is not None and target.kind=='culture',('missing culture scope',t)
            self.reads.append((o.name,'culture_percent_country',target.name))
            return o.a['shares'].get(target.name,0)
        return super().number(t,o,root,prev)
    def value_block(self,n,o,root,prev,current=0):
        chain=None
        for x in n.children or []:
            k=x.key
            if k=='limit':continue
            if k=='if':
                chain=self.block(x.get('limit'),o,root,prev)
                if chain:current=self.value_block(x,o,root,prev,current)
            elif k in ['else','else_if']:
                assert chain is not None
                if not chain:
                    yes=k=='else' or self.block(x.get('limit'),o,root,prev)
                    if yes:current=self.value_block(x,o,root,prev,current)
                    chain=yes
            elif k=='every_scope_culture':
                chain=None
                for q in o.a['cultures']:
                    if x.get('limit') is None or self.block(x.get('limit'),q,root,o):current=self.value_block(x,q,root,o,current)
            elif k in ['prev','owner','root']:
                chain=None;target=self.scope(k,o,root,prev)
                assert target is not None,('empty arithmetic scope',k)
                current=self.value_block(x,target,root,o,current)
            elif k=='round':current=math.floor(current+.5);chain=None
            else:
                chain=None;v=self.value_block(x,o,root,prev) if x.children is not None else self.number(x.value,o,root,prev)
                if k=='value':current=v
                elif k=='add':current+=v
                elif k=='subtract':current-=v
                elif k=='multiply':current*=v
                elif k=='divide':current/=v
                elif k=='min':current=max(current,v)
                elif k=='max':current=min(current,v)
                else:raise AssertionError(('unsupported arithmetic',k))
        return current

class Trace(BaseTrace):
    def __init__(self,w):self.w=w;self.pred=E(w);self.db=EFF;self.trace=[];self.events=[]
    def expiry(self,n):
        d=self.w['day']
        if n.get('months'):return add_months(d,int(n.scalar('months')))
        if n.get('years'):return add_months(d,12*int(n.scalar('years')))
        if n.get('days'):return d+timedelta(days=int(n.scalar('days')))
        return None
    def effect(self,n,o,root,prev):
        k,v=n.key,n.value
        if k=='save_scope_as':self.w['saved'][v]=o;return
        if k=='clear_saved_scope':self.w['saved'].pop(v,None);return
        if k=='set_variable':
            name=v or n.scalar('name');q=n.get('value')
            value=(self.pred.value_block(q,o,root,prev) if q.children is not None else self.pred.number(q.value,o,root,prev)) if q else 1
            var(o,name,value);expires=self.expiry(n)
            if expires:o.a['expiries'][name]=expires
            else:o.a['expiries'].pop(name,None)
            return
        if k=='change_variable':
            name=n.scalar('name');assert name in o.a['vars'],('change absent var',name)
            for sign,key in [(1,'add'),(-1,'subtract')]:
                if n.get(key):o.a['variable_values'][name]+=sign*self.pred.number(n.scalar(key),o,root,prev)
            return
        if k=='clamp_variable':
            name=n.scalar('name');o.a['variable_values'][name]=min(float(n.scalar('max')),max(float(n.scalar('min')),o.a['variable_values'][name]));return
        if k=='remove_variable':
            o.a['vars'].discard(v);o.a['variable_values'].pop(v,None);o.a['expiries'].pop(v,None);return
        if k=='add_modifier':
            name=n.scalar('name');assert name in MODS,('unknown modifier',name)
            mult=self.pred.number(n.scalar('multiplier','1'),o,root,prev)
            o.a['modifiers'].add(name);o.a['modifier_data'][name]={'multiplier':mult,'expires':self.expiry(n)}
            self.trace.append(('modifier',o.name,name,mult));return
        if k=='remove_modifier':
            # Native absent-removal behavior is not invented by this interpreter.
            o.a['modifiers'].discard(v);o.a['modifier_data'].pop(v,None);self.trace.append(('remove_modifier',o.name,v));return
        if k in ['every_scope_state','every_scope_building','every_primary_culture']:
            field={'every_scope_state':'states','every_scope_building':'buildings','every_primary_culture':'primary'}[k]
            for q in list(o.a.get(field,[])):
                if n.get('limit') is None or self.pred.block(n.get('limit'),q,root,o):self.block(SimpleNamespace(children=[x for x in n.children if x.key!='limit']),q,root,o)
            return
        if k=='add_radicals':
            q=self.pred.scope(n.scalar('culture'),o,root,prev);assert o.kind=='country' and q is not None and q.kind=='culture'
            self.trace.append(('radicals',o.name,q.name,self.pred.number(n.scalar('value'),o,root,prev)));return
        if k=='add_claim':
            assert o.kind=='region',('wrong add_claim scope',o)
            target=self.pred.scope(v,o,root,prev);assert target is not None and target.kind=='country'
            target.a['claims'].add(o.name);self.trace.append(('claim',target.name,o.name));return
        if k=='trigger_event':self.events.append((o,n.scalar('id'),self.expiry(n)));return
        if k=='set_bar_progress':o.a['bar']=self.pred.number(n.scalar('value'),o,root,prev);return
        if k=='hidden_effect':self.block(n,o,root,prev);return
        if k in ['show_as_tooltip','custom_tooltip']:return
        if k in self.db and n.children is not None:
            body=deepcopy(self.db[k]);args={q.key:q.value for q in n.children}
            for q in body.walk():
                for name,value in args.items():
                    if q.key:q.key=q.key.replace('$'+name+'$',value)
                    if q.value:q.value=q.value.replace('$'+name+'$',value)
            self.block(body,o,root,prev);return
        return super().effect(n,o,root,prev)
    def advance(self,d):
        self.w['day']=d
        for o in self.w['countries'].values():
            for k,end in list(o.a['expiries'].items()):
                if end<=d:o.a['vars'].discard(k);o.a['variable_values'].pop(k,None);del o.a['expiries'][k]
            for k,info in list(o.a['modifier_data'].items()):
                if info['expires'] and info['expires']<=d:o.a['modifiers'].discard(k);del o.a['modifier_data'][k]
    def modifier_total(self,o,key):
        return sum(float(n.value)*o.a['modifier_data'][m]['multiplier'] for m in o.a['modifiers'] for n in MODS[m].all(key))

rows=[]
def check(name,fn):
    try:
        detail=fn();rows.append({'name':name,'pass':True,'detail':detail})
    except Exception as e:
        rows.append({'name':name,'pass':False,'error':repr(e),'traceback':traceback.format_exc()})
        dump(RESULT,{'status':'FAIL_STOP','snapshot':str(T),'cases':rows,'engine_verified':False})
        print('FAIL_STOP',name,repr(e));raise SystemExit(1)
def equal(a,b):assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b)
def predicate(e,key,o):return e.block(e.db[key],o,o)
def readvalue(e,key,o):return e.number(key,o,o,None)
def enable(w,o):
    if o.name=='QE1':o.a['journals'].add('nesnd_qe1_unity_journal')
    elif o.name in ['JAP','JTK','JIM']:
        o.a['journals'].add('nesnd_jp_cohesion');var(o,'nesnd_jp_statistics_ready')
    elif o.name in ['MUG','BHT','DRA','XIM']:
        var(o,'nesnd_india_reform_done');var(o,'nesnd_india_imperial_line');o.a['tech'].add('nationalism');o.a['journals'].add('nesnd_india_society')
        reg=Obj('strategic','region_north_india');w['strategic']={'region_north_india':reg,'region_south_india':Obj('strategic','region_south_india')}
        o.a['states']=[Obj('state','INDIA',owner=o,region=reg,state_population=100000)]
    elif o.name=='TUR':o.a['num_states']=36;o.a['journals'].add('nesnd_ottoman_unity');var(o,'nesnd_ottoman_unity_opened')

def source_closure():
    actual=man(T);assert actual==META['manifest'],'immutable snapshot changed'
    keys={}
    for p in list(META['frozen_files'])+list(META['dependency_files']):
        if p.endswith('.txt'):
            tree=parse(read(T/p))
            for n in tree.walk():
                if n.key in ['has_discrimination_trait','has_discrimination_trait_group']:
                    source=TRAITS if n.key=='has_discrimination_trait' else definitions('common/discrimination_trait_groups')
                    assert n.value in source,('unknown native cultural enum',p,n.value)
            keys[p]=len(tree.children)
    for lang in ['simp_chinese','english']:
        p=T/f'localization/{lang}/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_{lang}.yml'
        assert p.read_bytes().startswith(b'\xef\xbb\xbf')
        assert read(p).splitlines()[0]=='l_'+lang+':'
    return {'parsed_script_files':len(keys),'culture_count':len(CULTURES),'snapshot_files':len(actual)}
check('frozen source parse, real culture enums and localization encoding',source_closure)

def law_regression():
    oldq=parse(read(B/'common/script_values/nesnd_qe1_identity.txt')).get('nesnd_qe1_unity_laws')
    oldi=parse(read(B/'common/script_values/nesnd_india_core.txt')).get('nesnd_india_community_unrest')
    w,o=world('QE1');e=E(w);cases=0
    groups=['lawgroup_citizenship','lawgroup_church_and_state','lawgroup_army_model']
    options=[[None]+[k for k,n in LAWS.items() if n.scalar('group')==g] for g in groups]
    for laws in itertools.product(*options):
        o.a['laws']={x for x in laws if x}
        for atwar in [False,True]:
            o.a['is_at_war']=atwar
            old=e.value_block(oldq,o,o,None)
            new=sum(readvalue(e,k,o) for k in ['nesnd_qe1_unity_citizenship','nesnd_qe1_unity_church_state','nesnd_qe1_unity_army_model'])
            equal(old,new);equal(new,readvalue(e,'nesnd_qe1_unity_laws',o));cases+=1
    for laws,unrest in itertools.product(options[0],[0,.25,.250001,1]):
        o.a['laws']={laws} if laws else set();o.a['country_turmoil']=unrest
        equal(e.value_block(oldi,o,o,None),readvalue(e,'nesnd_india_community_unrest',o)+readvalue(e,'nesnd_india_community_citizenship',o));cases+=1
    return {'effective_law_combinations':cases,'laws_from_game_and_snapshot':len(LAWS)}
check('actual law AST regression across every effective group law/variant',law_regression)

def culture_partition():
    w,o=world();e=E(w);groups=['nesnd_ottoman_culture_arab','nesnd_ottoman_culture_han','nesnd_ottoman_culture_african','nesnd_ottoman_culture_slavic'];counts=[0]*6
    for k,c in CULTURES.items():
        hits=[predicate(e,g,c) for g in groups]
        assert sum(hits)<=1,(k,hits)
        expected=0 if k=='turkish' else 1 if c.a['traits']&{'heritage_arab','heritage_berber','heritage_afro_arab'} else 2 if 'heritage_han' in c.a['traits'] else 3 if 'heritage_group_african' in c.a['groups'] else 4 if c.a['traits']&{'heritage_east_slavic','heritage_south_slavic','heritage_west_slavic'} else 5
        actual=0 if k=='turkish' else (hits.index(True)+1 if any(hits) else 5)
        assert actual==expected,(k,actual,expected);counts[actual]+=1
    for k in ['haratin','sudanese']:assert predicate(e,groups[0],CULTURES[k]) and not predicate(e,groups[2],CULTURES[k])
    return {'all_effective_cultures':len(CULTURES),'counts_Turkish_Arab_Han_African_Slavic_Other':counts}
check('actual cultural trait/group classification and Afro-Arab priority',culture_partition)

def culture_values():
    w,o=world();t=Trace(w);e=t.pred
    samples=[({},0),({'turkish':1},0),({'misri':1},-1.2),({'sudanese':1},-1.2),({'han':1},-.9),({'yoruba':1},-.6),({'russian':1},-.35),({'greek':1},-.15),({'turkish':.5,'misri':.2,'han':.1,'yoruba':.1,'russian':.05,'greek':.05},-.415)]
    parts=['arab','han','african','slavic','other']
    for pop,want in samples:
        shares(o,pop);t.call('nesnd_ottoman_unity_measure_cultures',o)
        total=sum(readvalue(e,'nesnd_ottoman_unity_'+k,o) for k in parts);equal(total,want)
        equal(sum(readvalue(e,'nesnd_ottoman_'+k+'_share',o) for k in ['turkish']+parts),0 if not pop else 1)
    return {'samples':len(samples),'native_country_culture_share_reads':len(e.reads)}
check('real share-sampling and weighted value AST: zero, single and mixed populations',culture_values)

def eligibility():
    result=[]
    for tag in ['QE1','JAP','JTK','JIM','MUG','BHT','DRA','XIM','TUR','FRA','ALW']:
        w,o=world(tag);enable(w,o);got=predicate(E(w),'nesnd_unity_policy_live',o);assert got==(tag not in ['FRA','ALW']),(tag,got);result.append((tag,got))
        o.a['journals'].clear();assert not predicate(E(w),'nesnd_unity_policy_live',o),(tag,'no journal')
    w,o=world('FRA');o.a['num_states']=100
    assert not predicate(E(w),'nesnd_ottoman_unity_available',o)
    for tag in ['TUR','FRA']:
        w,o=world(tag);o.a['is_country_alive']=False;o.a['num_states']=100
        assert not predicate(E(w),'nesnd_ottoman_unity_available',o)
    return result
check('owner/regime, imperial successor, unrelated and dead/absent journal eligibility',eligibility)

def entry_resume():
    w,o=world();t=Trace(w);shares(o,{'turkish':1})
    for n in [27,35]:o.a['num_states']=n;assert not predicate(t.pred,'nesnd_ottoman_unity_available',o)
    o.a['subject_state_count']=100;assert not predicate(t.pred,'nesnd_ottoman_unity_available',o)
    o.a['num_states']=36;t.call('nesnd_ottoman_unity_bootstrap',o);equal(o.a['variable_values']['nesnd_ottoman_unity'],70)
    var(o,'nesnd_ottoman_unity',17)
    o.a['num_states']=26;t.call('nesnd_ottoman_unity_bootstrap',o);assert not predicate(t.pred,'nesnd_ottoman_unity_live',o);equal(o.a['variable_values']['nesnd_ottoman_unity'],17)
    o.a['journals'].discard('nesnd_ottoman_unity')
    o.a['num_states']=27;t.call('nesnd_ottoman_unity_bootstrap',o);assert predicate(t.pred,'nesnd_ottoman_unity_live',o);equal(o.a['variable_values']['nesnd_ottoman_unity'],17)
    return {'entry':36,'resume':27,'retained_stock':17,'subjects_counted':False}
check('TUR direct 27/35/36 state entry, subject exclusion, loss and resume',entry_resume)

def policy_cost_and_pulses():
    w,o=world('JIM');enable(w,o);t=Trace(w);o.a['primary']=[CULTURES['japanese'],CULTURES['ce_wuu']]
    o.a['gold_reserves']=0;o.a['net_fixed_income']=-5000
    t.call('nesnd_unity_start_material',o)
    equal(t.modifier_total(o,'country_expenses_add'),2500);equal(t.modifier_total(o,'state_assimilation_mult'),.1)
    quote=o.a['variable_values']['nesnd_unity_material_quote'];o.a['gdp']=100000000;t.call('nesnd_unity_start_material',o)
    equal(o.a['variable_values']['nesnd_unity_material_quote'],quote);equal(t.modifier_total(o,'country_expenses_add'),2500)
    t.call('nesnd_unity_start_political',o);equal(t.modifier_total(o,'country_legitimacy_base_add'),-10);equal(t.modifier_total(o,'state_assimilation_mult'),.2)
    equal(readvalue(t.pred,'nesnd_jp_cohesion_material',o)+readvalue(t.pred,'nesnd_jp_cohesion_political',o),1)
    # Lose the JE: country cost persists, shared growth ceases.
    o.a['journals'].clear();equal(readvalue(t.pred,'nesnd_unity_material_growth',o),0);equal(t.modifier_total(o,'country_expenses_add'),2500)
    for i in range(12):
        t.advance(add_months(date(1836,1,15),i));t.call('nesnd_unity_material_monthly_cost',o);t.call('nesnd_unity_material_monthly_cost',o)
    radicals=[r for r in t.trace if r[0]=='radicals'];assert len(radicals)==24,radicals
    assert {r[2] for r in radicals}=={'japanese','ce_wuu'}
    assert all(r[3]==.001 for r in radicals)
    equal(o.a['variable_values']['nesnd_unity_material_pulses'],12)
    # Inject an extra same-contract callback before expiry; no extra political cost.
    t.advance(date(1837,1,1));t.call('nesnd_unity_material_monthly_cost',o);assert len([r for r in t.trace if r[0]=='radicals'])==24
    t.advance(date(1837,1,15));enable(w,o);assert predicate(t.pred,'nesnd_unity_material_available',o)
    t.call('nesnd_unity_start_material',o);equal(t.modifier_total(o,'country_expenses_add'),25000);equal(o.a['variable_values']['nesnd_unity_material_pulses'],0)
    return {'primary_cultures':2,'monthly_applications':12,'targeted_radical_operations':24,'initial_weekly_expense':2500,'renewal_weekly_expense':25000,'both_assimilation':.2}
check('actual policy effects, native modifier values, low funds, duplicate pulses and renewal',policy_cost_and_pulses)

def tanzimat():
    w,o=world();e=E(w);rows=[]
    for complete,score,failed,want in [(False,None,False,1),(True,3,False,.75),(True,4,False,2),(True,4,True,.75),(True,None,False,.75),(False,4,False,1)]:
        o.a['vars'].clear();o.a['variable_values'].clear()
        if complete:var(o,'sick_man_complete')
        if score is not None:var(o,'sick_man_var',score)
        if failed:var(o,'failed_sick_man_main')
        equal(readvalue(e,'nesnd_ottoman_enthusiasm_base',o),want);rows.append((complete,score,failed,want))
    # Expired20-year native failure marker is deliberately absent; permanent failure remains decisive.
    var(o,'sick_man_complete');var(o,'sick_man_var',4);var(o,'failed_sick_man_main')
    equal(readvalue(e,'nesnd_ottoman_enthusiasm_base',o),.75)
    return rows
check('Tanzimat completion flag ambiguity and expired temporary failure',tanzimat)

def reform_cleanup():
    results=[]
    for mode in ['ongoing','success','failed']:
        w,o=world();t=Trace(w)
        if mode!='ongoing':var(o,'sick_man_complete');var(o,'sick_man_var',4 if mode=='success' else 3)
        st=Obj('state','OWN',owner=o,buildings=[]);o.a['states']=[st]
        for kind in ['building_barrack','building_conscription_center','building_naval_administration']:
            st.a['buildings'].append(Obj('building',kind,owner=o,modifiers=set(),modifier_data={},vars=set(),variable_values={},expiries={}))
        # Inject all old saved attachments; the new helper must remove them, not renew them.
        for bld in st.a['buildings']:
            for key in ['nesnd_ottoman_qin_supply','nesnd_ottoman_qin_supply_success','nesnd_ottoman_qin_supply_failed']:
                bld.a['modifiers'].add(key);bld.a['modifier_data'][key]={'multiplier':1,'expires':None}
        t.call('nesnd_ottoman_start_reform',o);assert len(t.events)==1
        t.call('nesnd_ottoman_start_reform',o);assert len(t.events)==1
        rate={'ongoing':-.2,'success':-.25,'failed':-.15}[mode]
        equal(t.modifier_total(o,'unit_supply_consumption_mult'),rate)
        for building in st.a['buildings']:
            assert not building.a['modifiers'],('legacy building attachment remained',building)
            equal(t.modifier_total(building,'unit_supply_consumption_mult'),0)
        # Invalidate/tag change removes all benefits, but keeps original term to block early renewal.
        t.call('nesnd_ottoman_clear_reform_benefits',o);assert not o.a['modifiers'];assert 'nesnd_ottoman_reform_pending' in o.a['vars']
        t.call('nesnd_ottoman_start_reform',o);assert len(t.events)==1
        t.advance(date(1837,1,15));t.call('nesnd_ottoman_finish_reform',o);assert 'nesnd_ottoman_reform_pending' not in o.a['vars']
        t.call('nesnd_ottoman_start_reform',o);assert len(t.events)==2
        retained=set(o.a['modifiers']);t.call('nesnd_ottoman_finish_reform',o);assert o.a['modifiers']==retained,'old callback cleared fresh term'
        results.append((mode,rate,'old-callback-blocked'))
    return results
check('all national battalion-supply tiers, legacy cleanup and stale renewal callback',reform_cleanup)

def war_and_callbacks():
    w,o=world();enable(w,o);t=Trace(w)
    for months,want in [(0,-.2),(11,-.2),(12,-.5),(23,-.5),(24,-.8)]:
        var(o,'nesnd_ottoman_war_months',months);o.a['is_at_war']=True;equal(readvalue(t.pred,'nesnd_ottoman_unity_war',o),want)
    o.a['is_at_war']=False;equal(readvalue(t.pred,'nesnd_ottoman_unity_war',o),0)
    action=parse(read(T/'common/on_actions/nesnd_ottoman_unity.txt')).get('nesnd_ottoman_unity_wargoal')
    for _ in range(3):
        if t.pred.block(action.get('trigger'),o,o):t.block(action.get('effect'),o,o)
    equal(readvalue(t.pred,'nesnd_ottoman_unity_victory',o),.15)
    assert o.a['expiries']['nesnd_ottoman_unity_victory']==date(1838,1,15)
    acquisition=parse(read(T/'common/on_actions/nesnd_ottoman_unity.txt')).get('nesnd_ottoman_unity_acquisition').get('effect')
    empty=Obj('state','EMPTY');t.block(acquisition,empty,empty)
    foreign=country('FRA');w['countries']['FRA']=foreign;st=Obj('state','FOREIGN',owner=foreign);t.block(acquisition,st,st);assert 'nesnd_ottoman_unity_expansion' not in foreign.a['vars']
    st=Obj('state','OWN',owner=o);shares(o,{'turkish':1});t.block(acquisition,st,st);deadline=o.a['expiries']['nesnd_ottoman_unity_expansion'];t.block(acquisition,st,st);assert o.a['expiries']['nesnd_ottoman_unity_expansion']==deadline
    return {'war_thresholds':5,'victory_does_not_stack':True,'empty_and_foreign_owner_safe':True,'duplicate_acquisition_shared_cooldown':True}
check('sustained war, real callback root scopes, cooldowns and empty/non-owner references',war_and_callbacks)

def claim_cases():
    buttons=parse(read(T/'common/scripted_buttons/nesnd_ottoman_claims.txt')).children
    count=0
    for button in buttons:
        w,o=world();w['countries']['FRA']=foreign=country('FRA')
        region_key=next(n.value for n in button.walk() if n.key=='STATE')
        region=Obj('region',region_key,states=[]);w['regions'][region_key]=region
        state=Obj('state',region_key+':FRA',owner=foreign,state_region=region);region.a['states']=[state]
        t=Trace(w);var(o,'nesnd_ottoman_enthusiasm',25)
        assert t.pred.block(TR['nesnd_ottoman_claim_target'],region,o)
        t.block(button.get('effect'),o,o)
        assert region_key in o.a['claims'];equal(o.a['variable_values']['nesnd_ottoman_enthusiasm'],0)
        t.block(button.get('effect'),o,o);equal(o.a['variable_values']['nesnd_ottoman_enthusiasm'],0)
        assert not t.pred.block(TR['nesnd_ottoman_claim_target'],region,o)
        count+=1
    # Same predicate: own/foreign split, independent/subject Egypt, dead/missing TUR.
    w,o=world();region=Obj('region','STATE_ADANA',states=[]);w['regions'][region.name]=region
    egypt=country('EGY');w['countries']['EGY']=egypt;e=E(w)
    region.a['states']=[Obj('state','OWN',owner=o,state_region=region)]
    assert not e.block(TR['nesnd_ottoman_claim_target'],region,o)
    region.a['states'].append(Obj('state','EGY',owner=egypt,state_region=region))
    assert e.block(TR['nesnd_ottoman_claim_target'],region,o)
    egypt.a['overlord']=o;assert not e.block(TR['nesnd_ottoman_claim_target'],region,o)
    egypt.a.pop('overlord');o.a['is_country_alive']=False;assert not e.block(TR['nesnd_ottoman_claim_target'],region,o)
    del w['countries']['TUR'];assert not e.block(TR['nesnd_ottoman_claim_target'],region,o)
    return {'all_target_buttons':count,'cost_once':25,'boundary_cases':6}
check('all72 actual claim buttons, country/region scopes, one-time cost and Egypt boundaries',claim_cases)

def bar_sums():
    w,o=world();enable(w,o);t=Trace(w);shares(o,{'turkish':.5,'misri':.2,'han':.1,'yoruba':.1,'russian':.05,'greek':.05})
    t.call('nesnd_ottoman_unity_initialize',o);je=Obj('journal','nesnd_ottoman_unity',owner=o)
    bar=parse(read(T/'common/scripted_progress_bars/nesnd_ottoman_unity.txt')).get('nesnd_ottoman_unity_bar')
    count=0
    for war,months,legit,bankrupt,policy in itertools.product([False,True],[0,12,24],[24,25,49,50],[False,True],[False,True]):
        o.a['is_at_war']=war;o.a['government_legitimacy']=legit;var(o,'nesnd_ottoman_war_months',months)
        o.a['modifiers']={'declared_bankruptcy'} if bankrupt else set()
        if policy:o.a['modifiers'].update({'nesnd_unity_material_assistance','nesnd_unity_political_assistance'})
        value=sum(t.pred.value_block(n.get('value'),je,je,None) if n.get('value').children is not None else t.pred.number(n.scalar('value'),je,je,None) for n in bar.get('monthly_progress').all('add'))
        equal(value,readvalue(t.pred,'nesnd_ottoman_unity_delta',o));count+=1
    # Actual UI rows must name law groups, not the old combined field.
    qb=parse(read(T/'common/scripted_progress_bars/nesnd_qe1_identity.txt')).get('nesnd_qe1_unity_bar')
    labels=[x.scalar('desc') for x in qb.get('monthly_progress').all('add')]
    assert 'nesnd_qe1_unity_laws_desc' not in labels
    assert all('nesnd_unity_lawgroup_'+x in labels for x in ['citizenship','church_state','army_model'])
    return {'TUR_actual_delta_vs_bar_scenarios':count,'Qin_lawgroup_rows':3}
check('native bar rows equal actual stockdelta and actual lawgroup labels',bar_sums)

def quantity_preview():
    class Preview(Trace):
        def effect(self,n,o,root,prev):
            if n.key=='show_as_tooltip':self.block(n,o,root,prev);return
            if n.key=='hidden_effect':return
            if n.key=='custom_tooltip':self.trace.append(('tooltip',n.value));return
            return super().effect(n,o,root,prev)
    button=parse(read(T/'common/scripted_buttons/nesnd_ottoman_recovery.txt')).get('nesnd_ottoman_reform_army')
    result=[]
    for mode,rate in [('ongoing',-.2),('success',-.25),('failed',-.15)]:
        w,o=world();p=Preview(w)
        if mode!='ongoing':var(o,'sick_man_complete');var(o,'sick_man_var',4 if mode=='success' else 3)
        p.block(button.get('effect'),o,o)
        assert len(o.a['modifiers'])==1
        name=next(iter(o.a['modifiers']));assert len(MODS[name].all('unit_supply_consumption_mult'))==1
        equal(p.modifier_total(o,'unit_supply_consumption_mult'),rate)
        assert not any(row[0]=='tooltip' and 'supply' in str(row[1]) for row in p.trace)
        assert not MODS[name].all('country_military_goods_cost_mult') and not MODS[name].all('country_navy_goods_cost_mult')
        result.append((mode,rate,'one native amount'))
    return result
check('native reward preview displays quantity exactly once for all3 tiers',quantity_preview)

def negative_controls():
    caught=[]
    # Restore the exact first-freeze invalid predicate in memory, not in gameplay files.
    old_snapshot=W/'validation/runs/canon-b-unity-20261104/mod'
    old_claim=parse(read(old_snapshot/'common/scripted_triggers/nesnd_ottoman_recovery.txt')).get('nesnd_ottoman_claim_target')
    w,o=world();region=Obj('region','STATE_ADANA',states=[]);w['regions'][region.name]=region
    try:E(w).block(old_claim,region,o)
    except AssertionError as exc:
        assert 'state-only has_claim_by' in str(exc);caught.append('original state-only claim trigger rejected in state_region')
    else:raise AssertionError('negative control failed to reject original claim scope')
    # Remove the pulse cap from the real effect AST and require the behavioral case to catch it.
    key='nesnd_unity_material_monthly_cost';saved=EFF[key];mutant=deepcopy(saved)
    lim=mutant.get('if').get('limit');lim.children=[x for x in lim.children if x.key!='nesnd_unity_material_pulses']
    EFF[key]=mutant
    try:
        try:policy_cost_and_pulses()
        except AssertionError:caught.append('missing12-pulse cap detected')
        else:raise AssertionError('negative control failed to detect missing pulse cap')
    finally:EFF[key]=saved
    # Wrong expense sign must fail the actual modifier-derived cost assertion.
    key='nesnd_unity_material_expense';saved=MODS[key];mutant=deepcopy(saved);mutant.get('country_expenses_add').value='-1';MODS[key]=mutant
    try:
        try:policy_cost_and_pulses()
        except AssertionError:caught.append('negative expense sign detected')
        else:raise AssertionError('negative control failed to detect free-money sign')
    finally:MODS[key]=saved
    # Restore the exact rejected building-attachment helper, keeping the new inert shells.
    key='nesnd_ottoman_refresh_barracks';saved=EFF[key]
    EFF[key]=parse(read(old_snapshot/'common/scripted_effects/nesnd_ottoman_recovery.txt')).get(key)
    try:
        try:reform_cleanup()
        except AssertionError:caught.append('original building attachments detected by legacy-cleanup contract')
        else:raise AssertionError('negative control failed to detect old building attachment')
    finally:EFF[key]=saved
    return caught
check('negative controls reject original scope bug, missing pulse cap and wrong budget sign',negative_controls)

dump(RESULT,{'status':'PASS','snapshot':str(T),'cases':rows,'engine_verified':False,'limits':'Strict subset interpreter of actual ordered AST with explicit world fixtures; modifier propagation, native scheduling and UI are not simulated.'})
print('PASS',len(rows),'test groups; detailed real-AST cases in',RESULT)
