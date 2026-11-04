from batch_a_lifecycle_support import *
REPORT=json.loads((R/'batch-a-validation.json').read_text(encoding='utf-8'));REPORT['additional_boundaries']=[]
def case(name,fn):
    try:REPORT['additional_boundaries'].append({'name':name,'status':'PASS','detail':fn()})
    except Exception as exc:
        REPORT['additional_boundaries'].append({'name':name,'status':'FAIL','detail':repr(exc)});REPORT['status']='FAIL_STOPPED'
        (R/'batch-a-validation.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(REPORT['additional_boundaries'][-1],ensure_ascii=False));raise SystemExit(1)
GROUP='lawgroup_nesnd_hus_social_hierarchy'
def contaminate(o):
    bindvar(o,'nesnd_hus_hierarchy_version',2);bindvar(o,'nesnd_hus_hierarchy_active');bindvar(o,'nesnd_hus_frozen_citizenship_type',LAW_TYPES['law_cultural_exclusion'])
    o.a['hierarchy']='nesnd_hus_social_hierarchy';key='law_nesnd_hus_four_tier_system';o.a['active_laws'][GROUP]=Obj('law',key,owner=o,type=LAW_TYPES[key]);o.a['laws'].add(key)

def prepare_prefix():
    w,o=life_world('NKH');contaminate(o)
    class NativeResearchBoundary(Life):
        def effect(self,n,o,root,prev):
            if n.key=='add_era_researched':self.w['native_trace'].append(('native_research_boundary',n.value));return
            return super().effect(n,o,root,prev)
    r=NativeResearchBoundary(w);block=EFF['nesnd_khanate_prepare'].get('if')
    require(r.pred.block(block.get('limit'),o,o),'native preparation gate unexpectedly closed')
    prefix=[]
    for n in block.children:
        if n.key=='limit':continue
        prefix.append(n)
        if n.key=='remove_variable' and n.value=='nesnd_hus_hierarchy_mutating':break
    r.block(SimpleNamespace(children=prefix),o,o)
    require(o.a['hierarchy']=='default_social_hierarchy' and active_law(o,GROUP) is None,'NKH legal preparation retained HUS hierarchy')
    require(active_law(o,'lawgroup_citizenship')=='law_racial_segregation','NKH preparation missing citizenship')
    require('nesnd_hus_hierarchy_mutating' not in o.a['vars'],'NKH legal prefix guard leaked')
    require('nesnd_hus_native_legal_prepared' in o.a['vars'],'NKH preparation not recorded')
    return 'Executed actual gated legal prefix through native research boundary and law package; later construction/military code intentionally outside A test'
case('NKH_prepare_actual_legal_prefix_default_hierarchy',prepare_prefix)

def released_copy():
    w,o=life_world();r=initialized(w,o);choose(r,o)
    target=lawful_country(w,'REL');contaminate(target)
    for key in ('nesnd_hus_registration_choice','nesnd_hus_registration_epoch'):bindvar(target,key,readvar(o,key))
    bindvar(target,'nesnd_hus_revolution_continuation');bindvar(target,'nesnd_hus_revolution_source',o)
    due=next(x['due'] for x in w['timers'] if x['obj'] is None)
    r.on('nesnd_hus_hierarchy_independent_target',o,target)
    require(active_law(target,GROUP) is None and target.a['hierarchy']=='default_social_hierarchy','release inherited hierarchy')
    require('nesnd_hus_revolution_continuation' not in target.a['vars'],'release retained false revolutionary credential')
    require(w['globals']['nesnd_hus_registration_record_state']==1 and next(x['due'] for x in w['timers'] if x['obj'] is None)==due,'release cleanup cancelled original registration')
    return 'Released/secession target loses inherited credentials and hierarchy without changing original HUS global timer'
case('released_target_cannot_cancel_original_HUS_clock',released_copy)

def completed_source_gone():
    w,o=life_world();r=initialized(w,o);choose(r,o,2);rebel=fake_revolution(r,o)
    r.advance(date(1837,1,15));r.call('nesnd_hus_registration_settle',o)
    w['globals']['nesnd_hus_registration_exodus_epoch']=readvar(o,'nesnd_hus_registration_epoch')
    bindvar(rebel,'nesnd_hus_revolution_source',None)
    winner=win_revolution(r,o,rebel)
    require(active_law(winner,GROUP)=='law_nesnd_hus_native_registration','global terminal record failed to restore completed route')
    require('nesnd_hus_manchu_exodus_done' in winner.a['vars'] and 'nesnd_hus_manchu_exodus_pending' not in winner.a['vars'],'source loss reissued emigration')
    return 'Global done/emigration epoch restores completed Indigenous route after source payload disappears'
case('global_completed_epoch_survives_reclaimed_original_source',completed_source_gone)

def damaged_legacy():
    w,o=life_world();bindvar(o,'nesnd_hus_registration_done');r=initialized(w,o)
    require('nesnd_hus_migration_conflict' in o.a['vars'],'missing-route completed legacy was guessed')
    require('nesnd_hus_registration_choice' not in o.a['vars'],'damaged legacy got invented choice')
    require(not r.pred.block(TR['nesnd_hus_citizenship_unlocked'],o,o),'damaged legacy silently unlocked')
    choose(r,o,2);require(not w['globals'],'damaged legacy started a new registration')
    return 'Completed legacy with no route evidence remains frozen/conflicted and cannot reselect'
case('damaged_legacy_done_without_choice_cannot_reselect',damaged_legacy)

def only_citizenship():
    w,o=life_world();r=initialized(w,o)
    r.effect(parse('activate_law = law_type:law_monarchy').children[0],o,o,None)
    require(active_law(o,'lawgroup_governance_principles')=='law_monarchy','HUS freeze spilled into governance group')
    require(active_law(o,'lawgroup_citizenship')=='law_cultural_exclusion','citizenship freeze lost')
    return 'A direct governance-principles change remains; reconciliation only restores citizenship and hierarchy'
case('HUS_freeze_does_not_lock_other_law_groups',only_citizenship)

REPORT['status']='AST_UI_MCP_PASS_TIGER_CLASSIFICATION_PENDING'
(R/'batch-a-validation.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':REPORT['status'],'additional_boundaries':REPORT['additional_boundaries']},ensure_ascii=False))
