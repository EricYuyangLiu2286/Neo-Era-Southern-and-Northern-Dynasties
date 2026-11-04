from test_commission_gate_behavior import Evaluator as Base,Obj,SimpleNamespace
from journal_war_context import *
import copy,itertools,re

class Eval(Base):
    def __init__(self,w):
        super().__init__(C,w)
        self.values={n.key:n for p in (C/'common/script_values').glob('*.txt') for n in parse(read(p)).children}
    def scope(self,k,o,root,prev):
        if k=='capital':return o.a.get('capital')
        if k.startswith('global_var:'):return self.w.get('global_values',{}).get(k[11:])
        return super().scope(k,o,root,prev)
    def expr(self,n,o,root,prev):
        k,v=n.key,n.value
        if k=='has_global_variable':return v in self.w.get('globals',set())
        if k in ['army_size','army_power_projection','enemy_occupation'] or k.startswith('relations('):
            val=o.a.get(k,0);return self.cmp(val,n.op,self.number(v,o,root,prev))
        if k in ['nesnd_india_empire','nesnd_ming_authorized_dynast','nesnd_japan_fiscal_ready','nesnd_japan_army_ready','nesnd_japan_navy_ready']:
            return o.a.get(k,False)==(v=='yes') # explicit native/history fixture boundaries
        if k in ['is_character_alive','is_in_exile_pool','is_heir_of_own_country','has_game_started']:
            return o.a.get(k,False)==(v=='yes')
        if k=='any_scope_character':return any([self.block(n,q,root,o) for q in o.a.get('characters',[])])
        if k=='any_diplomatic_play':return any([self.block(n,q,root,o) for q in self.w.get('plays',[])])
        if k=='owns_entire_state_region':return v in o.a.get('owned_regions',set())
        if k=='country_has_local_shortage':raise AssertionError('Engine shortage not simulated')
        return super().expr(n,o,root,prev)

def world():
    w={'countries':{},'globals':{'usm_civilwar_occured'},'global_values':{},'saved':{},'regions':{},'plays':[]}
    for tag in ['USM','HNA','SIH','GNG','CNE','HUS','MUG','FRA']:
        o=Obj('country',tag,vars=set(),variable_values={},is_country_alive=True,num_states=5,army_size=20,army_power_projection=100,characters=[])
        w['countries'][tag]=o;o.a['capital']=Obj('state','capital_'+tag,owner=o,controller=o)
    w['countries']['USM'].a['vars'].add('tag_WUU_var')
    h=w['countries']['HNA'];h.a['vars']|={'nesnd_restoration_side','usm_opposition_country','nesnd_holdout_enrolled_round'};h.a['variable_values']['nesnd_holdout_enrolled_round']=1
    return w
rows=[]
def test(name,fn):
    try:fn();rows.append({'name':name,'pass':True})
    except Exception as e:rows.append({'name':name,'pass':False,'detail':repr(e)})
def check(w,key,want,actor='HNA'):
    actual=Eval(w).test(key,actor);assert actual==want,(key,actual,want)
test('first_peace_offers_choice',lambda:check(world(),'nesnd_holdout_offer_due',True))
for flag in ['nesnd_holdout_resolved','nesnd_capital_surrender_pending','nesnd_south_defeat_confirmed','nesnd_holdout_choice_pending','nesnd_holdout_north_awaited','nesnd_holdout_resistance_pending']:
    def case(flag=flag):
        w=world();w['countries']['HNA'].a['vars'].add(flag);check(w,'nesnd_holdout_offer_due',False)
    test('offer_blocked_'+flag,case)
for state in ['is_at_war','is_diplomatic_play_committed_participant','is_diplomatic_play_target']:
    def case(state=state):
        w=world();w['countries']['HNA'].a[state]=True;check(w,'nesnd_holdout_offer_due',False)
    test('offer_waits_for_'+state,case)
for answered,enrolled,want in [(0,1,True),(1,1,False),(1,2,True),(2,2,False)]:
    def case(a=answered,e=enrolled,want=want):
        w=world();h=w['countries']['HNA'];h.a['vars'].add('nesnd_holdout_answered_round');h.a['variable_values'].update(nesnd_holdout_answered_round=a,nesnd_holdout_enrolled_round=e);check(w,'nesnd_holdout_offer_due',want)
    test(f'round_{answered}_{enrolled}',case)
def missing_wu():
    w=world();del w['countries']['USM'];check(w,'nesnd_holdout_offer_due',False)
test('missing_wu_has_no_unguarded_read',missing_wu)
def request():
    w=world();h=w['countries']['HNA'];h.a['vars']|={'nesnd_holdout_north_awaited','nesnd_holdout_north_clock'}
    w['saved'].update(nesnd_holdout_sender=h,nesnd_holdout_request_round=1);return w
test('north_valid',lambda:check(request(),'nesnd_holdout_north_can_accept',True,'CNE'))
for saved in ['nesnd_holdout_sender','nesnd_holdout_request_round']:
    def case(saved=saved):
        w=request();del w['saved'][saved];check(w,'nesnd_holdout_north_request_valid',False,'CNE')
    test('north_missing_'+saved,case)
for variant in ['stale_round','timeout','sender_subject','sender_war','recipient_subject','recipient_war','recipient_bankrupt']:
    def case(variant=variant):
        w=request();h=w['countries']['HNA'];c=w['countries']['CNE']
        if variant=='stale_round':w['saved']['nesnd_holdout_request_round']=0
        if variant=='timeout':h.a['vars'].remove('nesnd_holdout_north_clock')
        if variant=='sender_subject':h.a['overlord']=c
        if variant=='sender_war':h.a['is_at_war']=True
        if variant=='recipient_subject':c.a['overlord']=w['countries']['FRA']
        if variant=='recipient_war':c.a['is_at_war']=True
        if variant=='recipient_bankrupt':c.a['modifiers']={'declared_bankruptcy'}
        check(w,'nesnd_holdout_north_can_accept',False,'CNE')
    test('north_'+variant,case)
for tag,army,default,want in [('HNA',10,False,True),('GNG',10,False,True),('SIH',40,False,False),('HNA',9,False,False),('HNA',20,True,False)]:
    def case(tag=tag,army=army,default=default,want=want):
        w=world();w['countries'][tag].a.update(army_size=army,in_default=default);check(w,'nesnd_holdout_ai_unyielding',want,tag)
    test(f'ai_unyielding_{tag}_{army}_{default}',case)
for tag,law,seen,want in [('HUS',False,False,False),('HUS',True,False,True),('HUS',False,True,True),('FRA',False,False,True)]:
    def case(tag=tag,law=law,seen=seen,want=want):
        w=world();o=w['countries'][tag]
        if law:o.a['laws']={'law_monarchy'}
        if seen:o.a['vars'].add('nesnd_hus_monarchy_seen')
        check(w,'nesnd_native_abolish_monarchy_eligible',want,tag)
    test(f'monarchy_{tag}_{law}_{seen}',case)
for priority in [None,0,1,2]:
    for kind in ['schools','industry']:
        def case(priority=priority,kind=kind):
            w=world();o=w['countries']['MUG'];o.a['nesnd_india_empire']=True
            if priority is not None:o.a['vars'].add('nesnd_india_priority');o.a['variable_values']['nesnd_india_priority']=priority
            check(w,'nesnd_india_'+kind+'_visible',priority in [1,2],'MUG')
            check(w,'nesnd_india_'+kind+'_available',priority==(1 if kind=='schools' else 2),'MUG')
            o.a['vars'].add('nesnd_india_reform_done');check(w,'nesnd_india_'+kind+'_visible',False,'MUG')
        test(f'india_priority_{priority}_{kind}',case)

# Exhaust actual score AST; delta arithmetic is read from its source, not copied into a mock score function.
def japan():
    w=world();o=w['countries']['USM'];ev=Eval(w)
    for bits in itertools.product([False,True],repeat=3):
        for key,b in zip(['fiscal','army','navy'],bits):o.a['nesnd_japan_'+key+'_ready']=b
        score=ev.number('nesnd_japan_preparation_score',o,o,None);assert score==sum(bits)
        for prior in range(4):
            n=ev.values['nesnd_eastern_readiness_bar_delta'].get('if')
            assert n.scalar('value')=='nesnd_japan_preparation_score' and n.scalar('subtract')=='je:nesnd_wu_eastern_question.scripted_bar_progress(nesnd_eastern_readiness_bar)'
            assert prior+(score-prior)==score and 0<=score<=3
    source=ev.values['nesnd_japan_unity_score'];states=[q.get('limit').scalar('owns_entire_state_region') for q in source.all('if')]
    assert len(states)==len(set(states))==7
    for bits in itertools.product([False,True],repeat=7):
        o.a['owned_regions']={s for s,b in zip(states,bits) if b};assert ev.number('nesnd_japan_unity_score',o,o,None)==sum(bits)
test('japan_all_8_readiness_and_128_unity_combinations',japan)

def unchanged_native_effect():
    old=parse(read(G/'common/scripted_effects/00_victoria_ep2_scripted_effects.txt')).get('transition_off_of_monarchy_effects')
    new=parse(read(C/'common/scripted_effects/zzzz_nesnd_hus_monarchy_entry.txt')).get('REPLACE:transition_off_of_monarchy_effects');new.key=old.key
    found=0
    for n in new.walk():
        if n.children:
            for q in n.children[:]:
                if q.key=='nesnd_native_abolish_monarchy_eligible':n.children.remove(q);found+=1
    assert found==1 and shape(old)==shape(new)
test('hus_native_effect_only_entry_guard_changed',unchanged_native_effect)

def contracts():
    effects=parse(read(C/'common/scripted_effects/nesnd_south_holdouts.txt'))
    surrender=effects.get('nesnd_holdout_surrender_to_wu')
    tokens=[x.key for x in surrender.walk()]
    assert tokens.index('annex_as_civil_war')<tokens.index('nesnd_holdout_mark_answer')
    assert any(x.key=='is_country_alive' and x.value=='no' for x in surrender.walk())
    escape=effects.get('nesnd_ming_escape_fallen_court');text=read(C/'common/scripted_effects/nesnd_south_holdouts.txt')[escape.start:escape.end]
    assert text.index('save_scope_as = nesnd_fleeing_heir')<text.index('nesnd_ming_relocate_royal = yes')
    old=parse(read(C/'events/usm_civilwar_events.txt')).get('usm_civilwar.5').get('after')
    tokens=[x.key for x in old.walk()];assert tokens.index('nesnd_ming_escape_fallen_court')<tokens.index('kill_character')
    je=parse(read(C/'common/journal_entries/ce_usm_the_last_days_of_ming.txt')).get('ce_usm_suppress_rebellion');assert je.get('complete').scalar('nesnd_south_wu_total_victory')=='yes'
    deadlock=parse(read(C/'common/scripted_triggers/nesnd_court_followup.txt')).get('nesnd_south_deadlock_context');assert any(x.key=='nesnd_south_unresolved_holdouts' for x in deadlock.walk())
test('royal_retry_order_and_all_settlement_entry_guards',contracts)

# Negative control: removing the actual answered-round comparison re-offers the same choice.
def negative():
    w=world();h=w['countries']['HNA'];h.a['vars'].add('nesnd_holdout_answered_round');h.a['variable_values']['nesnd_holdout_answered_round']=1
    ev=Eval(w);assert not ev.test('nesnd_holdout_offer_due','HNA')
    n=ev.db['nesnd_holdout_offer_due'];n.children=[q for q in n.children if q.key!='nesnd_holdout_answered_value'];assert ev.test('nesnd_holdout_offer_due','HNA')
test('negative_control_detects_repeated_offer',negative)

# Actual effect AST with deliberately failing native transfer/exile/annex APIs.
# This proves scripted branch handling, not how the game performs these operations.
from test_commission_effect_boundaries import EffectTrace as BaseTrace
class Trace(BaseTrace):
    def __init__(self,w,transfer_ok=True,exile_ok=True,annex_ok=True):
        super().__init__(w,C);self.pred=Eval(w);self.transfer_ok=transfer_ok;self.exile_ok=exile_ok;self.annex_ok=annex_ok
    def effect(self,n,o,root,prev):
        k,v=n.key,n.value
        if k=='save_scope_as':self.w['saved'][v]=o;return
        if k=='clear_saved_scope':self.w['saved'].pop(v,None);return
        if k=='set_variable':
            name=v or n.scalar('name');o.a.setdefault('vars',set()).add(name)
            if n.get('value'):
                value=n.scalar('value');obj=self.pred.scope(value,o,root,prev)
                o.a.setdefault('variable_values',{})[name]=obj if obj is not None else self.pred.number(value,o,root,prev)
            return
        if k in ['random_country','random_scope_character','every_scope_character']:
            items=list(self.w['countries'].values()) if k=='random_country' else list(o.a.get('characters',[]))
            items=[a for a in items if self.pred.block(n.get('limit'),a,root,o)]
            if k.startswith('random'):items=items[:1]
            for item in items:self.block(SimpleNamespace(children=[q for q in n.children if q.key!='limit']),item,root,o)
            return
        if k=='transfer_character':
            target=self.pred.scope(v,o,root,prev);assert target is not None
            self.trace.append(('transfer',o.name,target.name,self.transfer_ok))
            if self.transfer_ok:
                old=o.a.get('owner')
                if old is not None:
                    old.a['characters'].remove(o)
                    if old.a.get('ruler') is o:
                        # A successor can cease to be an heir immediately: source must have saved the old heir.
                        old.a.pop('ruler');heirs=[q for q in old.a['characters'] if q.a.get('is_heir_of_own_country')]
                        if heirs:old.a['ruler']=heirs[0];heirs[0].a['is_heir_of_own_country']=False
                o.a['owner']=target;target.a['characters'].append(o)
            return
        if k=='nesnd_ming_give_guest_role':o.a['guest']=True;return
        if k=='exile_character_with_role_cleanup':
            self.trace.append(('exile',o.name,self.exile_ok))
            if self.exile_ok:o.a['is_in_exile_pool']=True
            return
        if k=='annex_as_civil_war':
            target=self.pred.scope(v,o,root,prev);self.trace.append(('annex',target.name,self.annex_ok))
            if self.annex_ok:target.a['is_country_alive']=False
            return
        return super().effect(n,o,root,prev)
def royals(host=True,guest=False):
    w=world();h=w['countries']['HNA'];king=Obj('character','original_emperor',owner=h,is_character_alive=True,nesnd_ming_authorized_dynast=True,vars={'nesnd_ming_claimant'})
    heir=Obj('character','original_heir',owner=h,is_character_alive=True,nesnd_ming_authorized_dynast=True,is_heir_of_own_country=True,vars=set())
    h.a['characters']=[king,heir];h.a['ruler']=king;h.a['vars'].add('nesnd_ming_court')
    if guest:
        h.a['vars'].remove('nesnd_ming_court');h.a['variable_values'].update(nesnd_ming_claimant_ref=king,nesnd_ming_heir_ref=heir)
        h.a['vars']|={'nesnd_ming_claimant_ref','nesnd_ming_heir_ref'}
        h.a['ruler']=Obj('character','host_ruler',owner=h,is_character_alive=True,nesnd_ming_authorized_dynast=True,vars=set());h.a['characters'].append(h.a['ruler'])
    if host:w['countries']['GNG'].a['vars'].add('nesnd_restoration_side')
    return w,h,king,heir
for guest in [False,True]:
    def case(guest=guest):
        w,h,king,heir=royals(guest=guest);t=Trace(w);t.call('nesnd_holdout_surrender_to_wu',h)
        assert king.a['owner'] is w['countries']['GNG'] and heir.a['owner'] is w['countries']['GNG']
        assert not h.a['is_country_alive'] and 'nesnd_holdout_resolved' in h.a['vars']
        assert [x[0] for x in t.trace].index('transfer')<[x[0] for x in t.trace].index('annex')
    test('surrender_protects_'+('guest' if guest else 'court')+'_emperor_and_heir',case)
for host,move,exile,annex,dead in [(False,True,True,True,True),(True,False,True,True,True),(True,False,False,True,False),(True,True,True,False,False)]:
    def case(host=host,move=move,exile=exile,annex=annex,dead=dead):
        w,h,king,heir=royals(host);t=Trace(w,move,exile,annex);t.call('nesnd_holdout_surrender_to_wu',h)
        assert h.a['is_country_alive']!=dead
        if not dead:
            assert 'nesnd_holdout_answered_round' not in h.a['vars'] and 'nesnd_holdout_resolved' not in h.a['vars']
            check(w,'nesnd_holdout_offer_due',True)
        if not host or not move:
            assert king.a.get('is_in_exile_pool',False)==exile
            assert 'nesnd_ming_court' not in w['countries']['GNG'].a['vars']
    test(f'flight_faults_host{host}_move{move}_exile{exile}_annex{annex}',case)
dump(R/'boundary-tests.json',{'status':'PASS' if all(q['pass'] for q in rows) else 'FAIL','cases':rows,'scope':'Actual trigger/value AST subset. Native ownership, wars, character transfer and timing require engine testing. Unknown expressions fail; fixtures explicitly named.','source_files':man(C),'engine_verified':False})
print('PASS',sum(q['pass'] for q in rows),'FAIL',sum(not q['pass'] for q in rows))
for q in rows:
    if not q['pass']:print(q)
sys.exit(any(not q['pass'] for q in rows))
