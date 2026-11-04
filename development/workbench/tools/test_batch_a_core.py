from batch_a_test_support import *

report=json.loads((R/'batch-a-validation.json').read_text(encoding='utf-8'))
report['core_cases']=[];report['coverage']={};report['status']='RUNNING'
def save():
    (R/'batch-a-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    table='\n'.join(f'| {x["name"]} | {x["status"]} | {x.get("detail", "")} |' for x in report['cases']+report['core_cases'])
    md=f'''# Batch A frozen validation

Status: **{report['status']}**. Engine verification: **NOT_RUN**. Gameplay files were not edited during tests. A-01's original failure remains in `batch-a-validation-red-a01/`; the repaired owner gate passes.

Snapshot: `{T.as_posix()}`. Scope is the 24 owned files and recorded dependencies; no whole-C fixed SHA is claimed. All test inputs come from this snapshot and the fingerprinted GAME inputs in [batch-a-test-snapshot.json](batch-a-test-snapshot.json).

| Case | Result | Evidence |
|---|---|---|
{table}

Coverage details: `{json.dumps(report['coverage'],ensure_ascii=False)}`.

'''
    if report.get('new_finding'):
        f=report['new_finding']
        md+=f'''## {f['id']}: {f['title']}

{f['explanation']}

Observed strict-AST error: `{f['error']}`. This follows actual ordered helper calls. Normal effect execution is tested separately; no engine preview was launched. The preview fixture resolves explicit arguments without pretending preceding set_variable/set_global_variable effects initialized the preview environment, as required by the project's recorded engine failures.

Testing stopped at this material finding. Remaining full lifecycle/old-window/source-loss/reentrancy, UI datatype assertions, MCP and Tiger checks are NOT_RUN. No repair was applied in the test phase.
'''
    (R/'batch-a-validation.md').write_text(md,encoding='utf-8')
def case(name,fn):
    try:
        detail=fn();report['core_cases'].append({'name':name,'status':'PASS','detail':detail or ''});save()
    except Exception as exc:
        report['core_cases'].append({'name':name,'status':'FAIL','detail':repr(exc)});report['status']='FAIL_STOPPED'
        report['new_finding']={'id':'A-02','title':name,'error':repr(exc),'explanation':'See exact case and frozen source; coordinator repair phase required.'}
        if name=='fresh_button_preview_without_global_epoch_never_reads_uninitialized_values':
            p=T/'common/scripted_effects/nesnd_hus_registration.txt';s=read(p);node=EFF['nesnd_hus_allocate_registration_epoch'];line=s.count('\n',0,node.start)+1
            report['new_finding'].update(title='First-choice preview reads a global serial that only preceding effects initialize',file='common/scripted_effects/nesnd_hus_registration.txt',line=line,
                explanation=f'''The first HUS choice enters `nesnd_hus_choose_registration` and then `nesnd_hus_allocate_registration_epoch` (starts at L{line}). That helper writes a missing global serial and later reads `global_var:nesnd_hus_registration_serial` into the local epoch; further statements read the newly written local epoch. A first-open preview has neither value, and hidden_effect does not establish those variables for its later expressions. The normal execution positive control allocates epoch 1 with a one-year global wait and rejects a second click; the preview-only read fails. This is the same write-before-read preview pattern already prohibited by the project validation contract. A repair must make each preview-visible numeric expression independently readable via guarded values/fallbacks, while preserving real execution's serial allocation and immutable deadline. Moving the same expressions into another hidden block is insufficient.''')
        save();print(json.dumps({'status':report['status'],'finding':report['new_finding'],'report':str(R/'batch-a-validation.md')},ensure_ascii=False));raise SystemExit(1)

def parse_owned():
    count=0
    for row in META['owned_and_candidate_dependencies']:
        if row['role']=='owned' and row['path'].endswith('.txt'):
            parse(read(T/row['path']));count+=1
    return f'{count} owned script files parsed with ordered duplicate-preserving AST'
case('owned_ordered_AST_parses',parse_owned)

CL=tree('common/social_classes/nesnd_hus_social_classes.txt').children
def class_matrix():
    require(len(CL)==12,('class_count',len(CL)))
    default=parse(read(G/'common/social_classes/00_default.txt'))
    native_jobs={job:n.scalar('strata') for n in default.children for job in n.get('allowed_professions').values()}
    w,o=world();ev=E(w);hier=tree('common/social_hierarchies/nesnd_hus_social_hierarchy.txt').children[0].get('pop_criteria')
    combinations=0;applicable=set();witnesses={n.key:0 for n in CL}
    for culture in CULTURES.values():
        for job,strata in native_jobs.items():
            pop=Obj('pop',culture.name+':'+job,culture=culture)
            applies=ev.block(hier,pop,o)
            matched=[n for n in CL if job in n.get('allowed_professions').values() and ev.block(n.get('pop_criteria'),pop,o)]
            require(len(matched)==int(applies),('ambiguous_or_uncovered',culture.name,job,applies,[n.key for n in matched]))
            if matched:
                require(matched[0].scalar('strata')==strata,('economic_stratum_changed',culture.name,job));applicable.add(culture.name);witnesses[matched[0].key]+=1
            combinations+=1
    require('heritage_han' in CULTURES['manchu'].a['traits'],'global Manchu heritage changed')
    require(ev.block(TR['nesnd_hus_manchu_class_culture'],CULTURES['manchu'],o),'Manchu not classified first')
    require(not ev.block(TR['nesnd_hus_han_class_culture'],CULTURES['manchu'],o),'Manchu also Han class')
    report['coverage']['classes']={'effective_cultures':len(CULTURES),'native_professions':len(native_jobs),'combinations':combinations,'applicable_cultures':len(applicable),'class_witnesses':witnesses}
    return f'{combinations} culture × native profession combinations, each exactly one class or default; original economic strata preserved'
case('effective_cultures_disjoint_12_classes_native_profession_coverage',class_matrix)

def bounds():
    new=tree('common/laws/nesnd_hus_social_hierarchy.txt').children
    types=tree('common/modifier_type_definitions/nesnd_hus_social_class_modifiers.txt')
    group=tree('common/law_groups/nesnd_hus_social_hierarchy.txt').children[0]
    require(group.scalar('linked_social_hierarchy')=='nesnd_hus_social_hierarchy','wrong hierarchy group link')
    require(group.scalar('affected_by_regime_change')=='no','regime change may replace registration')
    require(len(new)==3 and len(types.children)==24,'wrong law/type count')
    matrix={}
    for n in new:
        require(n.get('parent') is None,'new law incorrectly inherits citizenship')
        require(n.scalar('group')=='lawgroup_nesnd_hus_social_hierarchy','new law wrong group')
        for guard in ('can_enact','can_impose','ai_will_do'):require(n.get(guard).scalar('always')=='no',('ordinary entry open',n.key,guard))
        fields=n.get('modifier').children;require(len(fields)==24,('incomplete bounds',n.key,len(fields)))
        expected={'han':(80,100),'manchu':(60,79),'native':(40,59),'white':(20,39)}
        if n.key.endswith('manchu_registration'):expected['manchu']=(80,100)
        if n.key.endswith('native_registration'):expected['native']=(80,100)
        for culture,(lo,hi) in expected.items():
            for strata in ('upper','middle','lower'):
                prefix=f'country_nesnd_hus_{culture}_{strata}_acceptance_'
                require(n.get('modifier').scalar(prefix+'min_add')==str(lo),('wrong floor',n.key,culture,strata))
                require(n.get('modifier').scalar(prefix+'max_add')==str(hi),('wrong ceiling',n.key,culture,strata))
                require(types.get(prefix+'min_add') is not None and types.get(prefix+'max_add') is not None,'missing modifier metadata')
        matrix[n.key]=expected
        require(n.get('acceptance_modifier') is None,'new law duplicates acceptance-tier citizenship treatments')
    report['coverage']['bounds']=matrix
    return 'Three laws × 24 exact bounds; unchanged classes keep identical bounds; no duplicate citizenship treatment blocks'
case('independent_group_three_laws_all_bounds_and_treatments',bounds)

def ideology_preservation():
    manifest=json.loads((R/'batch-a-native-ideology-edit-manifest.json').read_text(encoding='utf-8'));total=0
    for row in manifest:
        rel=row['path'];before=R/'batch-a-before'/rel;before=before if before.exists() else G/rel
        old=parse(read(before));new=parse(read(T/rel));changes={x['ideology'] for x in row['insertions']}
        cleaned=deepcopy(new)
        for n in cleaned.children:
            if n.key in changes:
                blocks=n.all('lawgroup_nesnd_hus_social_hierarchy');require(len(blocks)==1,('missing/duplicate attitude',n.key))
                n.children=[x for x in n.children if x.key!='lawgroup_nesnd_hus_social_hierarchy'];total+=1
        require(shape(old)==shape(cleaned),('non-attitude source changed',rel))
    effective=defs('common/ideologies');source=json.loads((R/'batch-a-effective-ideology-sources.json').read_text(encoding='utf-8'))
    for row in source['mapped_keys']:
        n=effective[row['key']].get('lawgroup_nesnd_hus_social_hierarchy')
        require(n is not None,('later source overwrote attitude',row['key']))
        require(n.scalar('law_nesnd_hus_four_tier_system')==row['initial'],('wrong initial attitude',row['key']))
        for law in ('manchu_registration','native_registration'):require(n.scalar('law_nesnd_hus_'+law)==row['registries'],('wrong registry attitude',row['key']))
    require(total==68,('wrong insertion count',total));report['coverage']['ideologies']=total
    return 'All 68 effective attitude mappings and ordered-AST equality after removing only added group blocks'
case('effective_68_ideology_mappings_preserve_all_original_AST_fields',ideology_preservation)

def guard_matrix():
    replacements=tree('common/laws/zzzz_nesnd_hus_citizenship_lock.txt').children;require(len(replacements)==6,'six ordinary laws required')
    checked=0
    for n in replacements:
        guard=n.get('can_impose').get('scope:target_country');require(guard is not None,('wrong impose scope',n.key))
        for root_locked in (False,True):
            for target_locked in (False,True):
                actor=country('FRA',root_locked);target=country('HUS',target_locked)
                w={'countries':{'FRA':actor,'HUS':target},'saved':{'target_country':target},'regions':{},'globals':{}}
                got=E(w).expr(guard,actor,actor,None)
                require(got==not_target(target_locked),('impose checks wrong country',n.key,root_locked,target_locked,got));checked+=1
        require(any(x.key=='nesnd_hus_citizenship_unlocked' for x in n.get('can_enact').walk()),('missing enact lock',n.key))
    report['coverage']['ordinary_law_target_matrix']=checked
    return f'{checked} root/target combinations; lock applies only to target country and six ordinary citizenship laws'
def not_target(value):return not value
case('six_ordinary_laws_target_scope_root_target_four_way_matrix',guard_matrix)

def history_guard():
    h=tree('common/history/countries/HUS.txt').get('COUNTRIES').get('c:HUS')
    commands=h.children
    start=next(i for i,n in enumerate(commands) if n.key=='set_variable' and n.value=='nesnd_hus_hierarchy_mutating')
    end=next(i for i,n in enumerate(commands) if n.key=='remove_variable' and n.value=='nesnd_hus_hierarchy_mutating')
    init=next(i for i,n in enumerate(commands) if n.key=='nesnd_hus_initialize_hierarchy')
    active=[i for i,n in enumerate(commands) if n.key in ('activate_law','effect_starting_politics_liberal')]
    require(all(start<i<end<init for i in active),'history can freeze an intermediate law')
    require(any(n.value=='law_type:law_cultural_exclusion' for n in commands),'original citizenship not restored')
    return 'All starting politics/activate_law commands lie inside mutation guard; initialization follows its removal'
case('history_politics_is_guarded_before_hierarchy_initialization',history_guard)

def actual_choice():
    w,o=world();tr=ChoiceTrace(w,True)
    tr.call('nesnd_hus_choose_registration',o,{'CHOICE':'1'})
    require(w['globals']['nesnd_hus_registration_serial']==1,'first epoch not one')
    require(o.a['variable_values']['nesnd_hus_registration_epoch']==1,'local epoch mismatch')
    require(w['globals']['nesnd_hus_registration_record_epoch']==1,'record epoch mismatch')
    require(w['globals']['nesnd_hus_registration_wait']==1,'timer not tied to epoch')
    require(w['expiries'][('global','nesnd_hus_registration_wait')]=={'years':'1'},'global lifetime not one native year')
    require(w['events']==[{'id':'nesnd_hus_registration.10','months':'12'}],'wrong delayed event')
    tr.call('nesnd_hus_choose_registration',o,{'CHOICE':'2'})
    require(w['globals']['nesnd_hus_registration_serial']==1 and o.a['variable_values']['nesnd_hus_registration_choice']==1,'second click replaced route/timer')
    report['coverage']['choice_trace']=tr.trace
    return 'Real helper AST allocates one epoch and a one-year global timer; second click cannot change either'
case('actual_first_choice_then_duplicate_click_preserves_epoch_and_deadline',actual_choice)

def preview():
    w,o=world();tr=ChoiceTrace(w,False)
    buttons=tree('common/scripted_buttons/nesnd_hus_registration.txt')
    tr.block(buttons.get('nesnd_hus_register_manchu').get('effect'),o,o)
    require(not w['globals'] and 'nesnd_hus_registration_choice' not in o.a['vars'],'preview mutated the world')
    return 'Fresh preview evaluates without relying on simulated earlier writes'
case('fresh_button_preview_without_global_epoch_never_reads_uninitialized_values',preview)

def preview_existing_serial():
    w,o=world();w['globals']['nesnd_hus_registration_serial']=9
    tr=ChoiceTrace(w,False)
    tr.block(tree('common/scripted_buttons/nesnd_hus_registration.txt').get('nesnd_hus_register_native').get('effect'),o,o)
    require(w['globals']=={'nesnd_hus_registration_serial':9} and not o.a['variable_values'],'preview changed serial or initialized local state')
    return 'Existing serial / missing local epoch also previews safely without mutation'
case('existing_global_serial_missing_local_epoch_preview',preview_existing_serial)

def mutation_removes_guard():
    key='nesnd_hus_allocate_registration_epoch';original=EFF[key];mutant=deepcopy(original)
    changed=[]
    for n in mutant.children:
        if n.key=='if' and n.get('limit') and n.get('limit').get('has_global_variable') is not None:
            changed.extend(q for q in n.children if q.key!='limit')
        else:changed.append(n)
    mutant.children=changed;EFF[key]=mutant
    try:
        w,o=world();tr=ChoiceTrace(w,False)
        try:tr.call('nesnd_hus_choose_registration',o,{'CHOICE':'1'})
        except AssertionError as exc:
            require('global_var:nesnd_hus_registration_serial' in repr(exc),('wrong mutation signal',repr(exc)))
            return 'Removing the new explicit serial branch in memory reproduces the exact missing-global preview read'
        raise AssertionError('Regression mutant was not detected')
    finally:EFF[key]=original
case('A02_guard_removal_adversarial_mutation_is_detected',mutation_removes_guard)

report['status']='CORE_PASS_REMAINING_PENDING';save()
print(json.dumps({'status':report['status'],'core_cases':report['core_cases']},ensure_ascii=False))
