from batch_a_lifecycle_support import *

REPORT=json.loads((R/'batch-a-validation.json').read_text(encoding='utf-8'))
REPORT['lifecycle_cases']=[]
REPORT['native_fixture_boundaries']=[
    'activate_law stores the chosen active law and injects before/after callbacks; it does not simulate native political acceptance or enlistment',
    'calendar years/months and timed-variable expiry are deterministic fixtures, not observed engine scheduling',
    'revolution/tag object transitions are explicit fixtures; source loss is injected',
    'native American territorial unification prerequisite is injected; population/military/war behavior is not simulated in this A legal test',
]
REPORT['status']='RUNNING_LIFECYCLE'
def save():
    (R/'batch-a-validation.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
    rows=REPORT['cases']+REPORT['core_cases']+REPORT['lifecycle_cases']
    table='\n'.join(f'| {x["name"]} | {x["status"]} | {x.get("detail", "")} |' for x in rows)
    text=f'''# Batch A frozen validation

Status: **{REPORT['status']}**. Engine verification: **NOT_RUN**. No gameplay files changed during tests. A-01 and A-02 original failures are preserved in their red archives. Both repaired gates and the guard-removal mutation control pass.

Snapshot: `{T.as_posix()}`. This binds the 24 owned files and recorded candidate/native prerequisites, not the concurrently edited whole candidate. See [snapshot/dependency hashes](batch-a-test-snapshot.json).

The interpreter executes the actual ordered source AST. Unknown nodes fail loudly. Native API results, callback timing, object transitions and expiry are explicit injected boundaries, not recreated engine behavior. In particular, these results do not certify real law callback order, class modifier application, exact calendar expiry order, AI play or GUI layout.

| Case | Result | Evidence |
|---|---|---|
{table}

Core coverage: `{json.dumps(REPORT['coverage'],ensure_ascii=False)}`.

'''
    if REPORT.get('lifecycle_finding'):
        text+='## First failing lifecycle case\n\n'+json.dumps(REPORT['lifecycle_finding'],ensure_ascii=False,indent=2)+'\n\nTesting stopped. Remaining lifecycle, UI, MCP and Tiger work is NOT_RUN; no test-phase gameplay repair has been made.\n'
    else:text+='\nUI datatype/narrow-diff assertions, actual MCP queries and A-scoped Tiger are still pending.\n'
    (R/'batch-a-validation.md').write_text(text,encoding='utf-8')
def ck(name,fn):
    try:
        detail=fn();REPORT['lifecycle_cases'].append({'name':name,'status':'PASS','detail':detail or ''});save()
    except Exception as exc:
        REPORT['lifecycle_cases'].append({'name':name,'status':'FAIL','detail':repr(exc)});REPORT['status']='FAIL_STOPPED'
        REPORT['lifecycle_finding']={'id':'A-03','case':name,'error':repr(exc),'engine_verified':False}
        save();print(json.dumps({'status':REPORT['status'],'finding':REPORT['lifecycle_finding']},ensure_ascii=False));raise SystemExit(1)

INITIAL='law_nesnd_hus_four_tier_system';MM='law_nesnd_hus_manchu_registration';NATIVE='law_nesnd_hus_native_registration';GROUP='lawgroup_nesnd_hus_social_hierarchy'
def expected(r,o,law=INITIAL,frozen='law_cultural_exclusion'):
    require(active_law(o,GROUP)==law,('wrong_hierarchy_law',o.name,active_law(o,GROUP),law))
    require(active_law(o,'lawgroup_citizenship')==frozen,('wrong_frozen_citizenship',o.name))
    require(o.a['hierarchy']=='nesnd_hus_social_hierarchy','missing hierarchy')
    require('nesnd_hus_hierarchy_active' in o.a['vars'],'inactive hierarchy')
    require('nesnd_hus_hierarchy_mutating' not in o.a['vars'],'mutation guard leaked')
    require(not r.pred.block(TR['nesnd_hus_citizenship_unlocked'],o,o),'citizenship lock bypassed')

def initialization():
    for timing in ('before','after'):
        w,o=life_world();r=initialized(w,o,callback_timing=timing);expected(r,o)
        require(readvar(o,'nesnd_hus_hierarchy_version')==2,'schema missing')
        require(readvar(o,'custom_social_hierarchy').kind=='law','CMF got law_type rather than law')
        r.call('nesnd_hus_initialize_hierarchy',o);r.call('nesnd_hus_reconcile_hierarchy',o);expected(r,o)
        require(active_law(o,'lawgroup_governance_principles')=='law_presidential_republic','unrelated governance changed')
    return 'Initialization and repeated reconciliation retain current governance and actual law CMF object under both injected callback timings'
ck('new_history_like_initialization_and_law_callback_reentrancy',initialization)

def old_ordinary():
    w,o=life_world(citizenship='law_multicultural');r=initialized(w,o);expected(r,o,frozen='law_multicultural')
    r.call('nesnd_hus_initialize_hierarchy',o);expected(r,o,frozen='law_multicultural')
    return 'Existing ordinary citizenship is saved once and preserved'
ck('old_save_existing_ordinary_citizenship_is_not_rolled_back',old_ordinary)

def old_completed():
    for old,new,route in [('law_nesnd_hus_registry_manchu',MM,1),('law_nesnd_hus_registry_native',NATIVE,2)]:
        w,o=life_world(citizenship=old);r=initialized(w,o);expected(r,o,new)
        require(readvar(o,'nesnd_hus_registration_choice')==route and 'nesnd_hus_registration_done' in o.a['vars'],'legacy law did not preserve outcome')
        require(w['globals']['nesnd_hus_registration_record_state']==3,'completed legacy record not terminal')
        r.call('nesnd_hus_registration_settle',o)
        require('nesnd_hus_manchu_exodus_pending' not in o.a['vars'],'migration reissued exodus')
    return 'Both legacy registered laws migrate directly; completion does not reissue aftermath'
ck('legacy_completed_laws_preserve_choice_and_no_reissued_outcome',old_completed)

def legacy_pending():
    w,o=life_world(citizenship='law_nesnd_hus_hierarchy');r=Life(w)
    bindvar(o,'nesnd_hus_registration_choice',1)
    r.effect(parse('set_variable = { name = nesnd_hus_registration_wait days = 90 }').children[0],o,o,None)
    deadline=w['timers'][0]['due'];r.call('nesnd_hus_initialize_hierarchy',o)
    require(w['globals']['nesnd_hus_registration_record_state']==5,'legacy timer not in custody')
    require('nesnd_hus_registration_wait' not in w['globals'],'legacy created a fresh global year')
    r.advance(deadline-timedelta(days=1));r.call('nesnd_hus_registration_settle',o);expected(r,o)
    require('nesnd_hus_registration_done' not in o.a['vars'],'old wait completed early')
    r.advance(deadline);r.call('nesnd_hus_registration_settle',o);expected(r,o,MM)
    require(w['globals']['nesnd_hus_registration_record_state']==3,'legacy wait failed to settle at original due date')
    return 'Original 90-day remaining wait is retained; no extra year and no early settlement'
ck('legacy_pending_keeps_original_remaining_wait',legacy_pending)

def global_timer():
    for route,law in ((1,MM),(2,NATIVE)):
        w,o=life_world();r=initialized(w,o);choose(r,o,route)
        deadline=next(x['due'] for x in w['timers'] if x['obj'] is None and x['name']=='nesnd_hus_registration_wait')
        for _ in range(3):r.call('nesnd_hus_reconcile_hierarchy',o);r.call('nesnd_hus_registration_settle',o)
        require(next(x['due'] for x in w['timers'] if x['obj'] is None)==deadline,'reconcile refreshed global timer')
        r.advance(deadline-timedelta(days=1));r.call('nesnd_hus_registration_settle',o);expected(r,o)
        r.advance(deadline);r.call('nesnd_hus_registration_settle',o);expected(r,o,law)
        epoch=readvar(o,'nesnd_hus_registration_epoch');count=len(w['native_trace']);r.call('nesnd_hus_registration_settle',o)
        require(epoch==readvar(o,'nesnd_hus_registration_epoch') and len(w['native_trace'])==count,'duplicate settlement reapplied effects')
    return 'Both routes settle only after fixed global expiry and remain idempotent'
ck('new_global_year_before_at_after_deadline_and_duplicate_settle',global_timer)

def activation_failure():
    w,o=life_world();r=initialized(w,o);choose(r,o,2);r.advance(date(1837,1,15));r.fail_activate=NATIVE
    r.call('nesnd_hus_registration_settle',o)
    require('nesnd_hus_registration_done' not in o.a['vars'] and 'nesnd_hus_manchu_exodus_pending' not in o.a['vars'],'failed native activation committed success')
    require(w['globals']['nesnd_hus_registration_record_state']==2,'failure consumed settlement')
    r.fail_activate=None;r.call('nesnd_hus_registration_settle',o);expected(r,o,NATIVE)
    return 'Injected native activation failure leaves ready state and no committed outcome; retry succeeds'
ck('native_law_activation_failure_does_not_commit_done',activation_failure)

def queued_windows():
    w,o=life_world();r=initialized(w,o);choose(r,o);event=w['events'][0]
    r.advance(date(1837,1,14));r.event(event)
    require('nesnd_hus_registration_done' not in o.a['vars'],'early event bypassed global clock')
    require(len(w['events'])==2 and w['events'][1]['due']==date(1837,1,15),'missing bounded next-day retry')
    r.event(w['events'][1]);require(len(w['events'])==2,'retry generated infinite retries')
    stale=dict(event);stale['saved']=dict(event['saved']);stale['saved']['nesnd_hus_delayed_epoch']=0
    r.advance(date(1837,1,15));r.event(stale);require('nesnd_hus_registration_done' not in o.a['vars'],'old epoch settled current choice')
    r.event(event);expected(r,o,MM);r.event(event);require(w['globals']['nesnd_hus_registration_record_state']==3,'repeated event changed terminal record')
    return 'Early same-date window waits, retry is bounded, stale epoch rejects, repeated event stays terminal'
ck('old_window_old_epoch_bounded_retry_and_repeat_event',queued_windows)

def direct_law_changes():
    for timing in ('before','after'):
        w,o=life_world();r=initialized(w,o,callback_timing=timing);choose(r,o)
        r.effect(parse('activate_law = law_type:law_multicultural').children[0],o,o,None)
        r.call('nesnd_hus_reconcile_hierarchy',o);expected(r,o)
        r.effect(parse('activate_law = law_type:law_nesnd_hus_native_registration').children[0],o,o,None)
        r.call('nesnd_hus_reconcile_hierarchy',o);expected(r,o)
        o.a['hierarchy']='default_social_hierarchy';r.call('nesnd_hus_reconcile_hierarchy',o);expected(r,o)
        require(readvar(o,'nesnd_hus_registration_choice')==1,'external law changed choice')
    return 'External ordinary/custom law or hierarchy changes cannot bypass pending route; monthly reconciliation covers injected pre-activation callback'
ck('direct_activate_and_external_hierarchy_changes_preserve_frozen_choice',direct_law_changes)

def pending_revolutions():
    for formed_first in (True,False):
        for source_gone in (False,True):
            w,o=life_world();r=initialized(w,o);choose(r,o);deadline=next(x['due'] for x in w['timers'] if x['obj'] is None)
            rebel=fake_revolution(r,o);require('nesnd_hus_hierarchy_retired' not in rebel.a['vars'],'temporary revolution retired')
            require(readvar(rebel,'nesnd_hus_registration_epoch')==1 and 'nesnd_hus_registration_wait' not in rebel.a['vars'],'revolution copied/refreshed local timer')
            if source_gone:bindvar(rebel,'nesnd_hus_revolution_source',None)
            winner=win_revolution(r,o,rebel,formed_first);expected(r,winner)
            require('nesnd_hus_hierarchy_retired' not in winner.a['vars'],'retired flag bypassed restored freeze')
            require(next(x['due'] for x in w['timers'] if x['obj'] is None)==deadline,'revolution reset deadline')
            r.advance(deadline);r.call('nesnd_hus_registration_settle',winner);expected(r,winner,MM)
    return 'Both formed/won orders and lost-source variants retain choice/epoch and the original global deadline'
ck('ordinary_revolution_pending_formed_won_orders_and_source_gone',pending_revolutions)

def completed_revolutions():
    for route,law in ((1,MM),(2,NATIVE)):
        for completed_before_start in (True,False):
            w,o=life_world();r=initialized(w,o);choose(r,o,route)
            if completed_before_start:r.advance(date(1837,1,15));r.call('nesnd_hus_registration_settle',o)
            rebel=fake_revolution(r,o)
            if not completed_before_start:r.advance(date(1837,1,15));r.call('nesnd_hus_registration_settle',o)
            if route==2:
                # Native population movement is outside A; its already-committed outcome is an explicit fixture.
                bindvar(o,'nesnd_hus_manchu_exodus_done');o.a['vars'].discard('nesnd_hus_manchu_exodus_pending');o.a['variable_values'].pop('nesnd_hus_manchu_exodus_pending',None)
                w['globals']['nesnd_hus_registration_exodus_epoch']=1
            winner=win_revolution(r,o,rebel);expected(r,winner,law)
            require('nesnd_hus_registration_done' in winner.a['vars'],'completed route lost in revolution')
            if route==2:require('nesnd_hus_manchu_exodus_done' in winner.a['vars'] and 'nesnd_hus_manchu_exodus_pending' not in winner.a['vars'],'revolution reissued completed emigration')
    return 'Both completed routes survive; original-government completion during war is refreshed from its source snapshot'
ck('revolution_after_done_or_original_completion_during_war',completed_revolutions)

def legacy_source_loss():
    w,o=life_world(citizenship='law_nesnd_hus_hierarchy');r=Life(w);bindvar(o,'nesnd_hus_registration_choice',1)
    r.effect(parse('set_variable = { name = nesnd_hus_registration_wait days = 90 }').children[0],o,o,None);r.call('nesnd_hus_initialize_hierarchy',o)
    rebel=fake_revolution(r,o);bindvar(rebel,'nesnd_hus_revolution_source',None);bindvar(rebel,'nesnd_hus_registration_clock_source',None)
    winner=win_revolution(r,o,rebel);r.call('nesnd_hus_registration_settle',winner)
    require('nesnd_hus_migration_conflict' in winner.a['vars'] and 'nesnd_hus_registration_done' not in winner.a['vars'],'missing legacy expiry was treated as completed')
    require(not r.pred.block(TR['nesnd_hus_citizenship_unlocked'],winner,winner),'damaged legacy state unlocked rights')
    return 'Unknown legacy remaining time enters explicit conflict and retains freeze'
ck('legacy_source_object_loss_does_not_fake_elapsed_time',legacy_source_loss)

def permanent_retag():
    w,o=life_world();r=initialized(w,o);choose(r,o)
    r.effect(parse('change_tag = XXX').children[0],o,o,None)
    require('nesnd_hus_hierarchy_retired' in o.a['vars'] and active_law(o,GROUP) is None,'normal retag did not retire')
    require(w['globals']['nesnd_hus_registration_record_state']==4 and 'nesnd_hus_registration_wait' not in w['globals'],'permanent exit did not cancel its own record')
    r.effect(parse('change_tag = HUS').children[0],o,o,None)
    require(active_law(o,GROUP) is None and r.pred.block(TR['nesnd_hus_citizenship_unlocked'],o,o),'arbitrary return resurrected the hierarchy')
    return 'Non-revolutionary retag permanently retires; bare later HUS tag does not revive the system'
ck('normal_retag_permanent_exit_and_late_return',permanent_retag)

def successor_and_primary():
    w,o=life_world('NKH');r=Life(w)
    bindvar(o,'nesnd_hus_native_successor');bindvar(o,'nesnd_hus_revolution_continuation');bindvar(o,'nesnd_hus_hierarchy_version',2);bindvar(o,'nesnd_hus_frozen_citizenship_type',LAW_TYPES['law_cultural_exclusion'])
    o.a['primary']=[CULTURES['han'],CULTURES['manchu'],CULTURES['french']];o.a['cultures']=[CULTURES['cherokee']]
    r.call('nesnd_hus_reconcile_hierarchy',o)
    require(o.a['hierarchy']=='default_social_hierarchy' and active_law(o,GROUP) is None,'NKH inherited HUS hierarchy')
    require({c.name for c in o.a['primary']}=={'siouan','cherokee'},('primary cleanup missed absent-pop primary',o.a['primary']))
    require(active_law(o,'lawgroup_citizenship')=='law_racial_segregation','successor initial citizenship missing')
    r.effect(parse('activate_law = law_type:law_multicultural').children[0],o,o,None);r.call('nesnd_hus_reconcile_hierarchy',o)
    require(active_law(o,'lawgroup_citizenship')=='law_multicultural','native successor was permanently frozen')
    # The legal succession function itself retains default hierarchy and native primaries.
    o.a['nesnd_native_americas_unified']=True;r.call('nesnd_khanate_form_native_hus',o)
    require(o.name=='HUS' and 'nesnd_hus_native_successor' in o.a['vars'],'native formation identity missing')
    require(o.a['hierarchy']=='default_social_hierarchy' and active_law(o,GROUP) is None,'native HUS reentered hierarchy')
    require(active_law(o,'lawgroup_citizenship')=='law_racial_segregation','native HUS law package missing')
    require(r.pred.block(TR['nesnd_hus_citizenship_unlocked'],o,o),'native HUS rights remained locked')
    return 'Native successor wins over revolution receipt; all non-native primaries removed, fallback retained, default hierarchy and editable citizenship'
ck('NKH_native_successor_priority_primary_fallback_and_native_HUS',successor_and_primary)

def foreign_cmf_cleanup():
    w,o=life_world();r=initialized(w,o);foreign=Obj('law','external_law',owner=o,type=LAW_TYPES['law_multicultural']);bindvar(o,'custom_social_hierarchy',foreign)
    o.a['modifiers']={'nesnd_hus_acceptance_hierarchy','nesnd_hus_acceptance_manchu','nesnd_hus_acceptance_native'}
    r.call('nesnd_hus_clear_hierarchy',o);r.call('nesnd_hus_reconcile_hierarchy',o)
    require(readvar(o,'custom_social_hierarchy') is foreign,'clear removed another module CMF value')
    require(not o.a['modifiers'] and active_law(o,GROUP) is None,'cleanup left modifiers/laws')
    require('nesnd_hus_hierarchy_mutating' not in o.a['vars'],'clear guard leaked')
    return 'Permanent clear removes all three legacy modifiers and own hierarchy while retaining foreign CMF law reference'
ck('clear_all_retains_foreign_CMF_and_has_no_reentrant_revival',foreign_cmf_cleanup)

REPORT['status']='LIFECYCLE_PASS_UI_TOOLS_PENDING';save()
print(json.dumps({'status':REPORT['status'],'lifecycle_cases':REPORT['lifecycle_cases']},ensure_ascii=False))
