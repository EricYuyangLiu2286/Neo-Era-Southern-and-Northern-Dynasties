from batch_a_test_support import *
REPORT=json.loads((R/'batch-a-validation.json').read_text(encoding='utf-8'));REPORT['static_closure_cases']=[]
def save():
    (R/'batch-a-validation.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
    with (R/'batch-a-validation.md').open('a',encoding='utf-8') as f:
        f.write('\n## UI and source closure\n\n')
        for row in REPORT['static_closure_cases']:f.write(f'- {row["status"]}: {row["name"]} — {row.get("detail", "")}\n')
def ck(name,fn):
    try:REPORT['static_closure_cases'].append({'name':name,'status':'PASS','detail':fn() or ''})
    except Exception as exc:
        REPORT['static_closure_cases'].append({'name':name,'status':'FAIL','detail':repr(exc)});REPORT['status']='FAIL_STOPPED';save();print(json.dumps(REPORT['static_closure_cases'][-1],ensure_ascii=False));raise SystemExit(1)

def only_header():
    native=parse(read(G/'gui/culture_panel.gui'));candidate=parse(read(T/'gui/culture_panel.gui'))
    marker='lawgroup_nesnd_hus_social_hierarchy';found=[]
    def visit(n):
        kept=[]
        for x in n.children or []:
            if x.key=='acceptance_group_with_law_status' and marker in (x.scalar('visible') or ''):found.append(x)
            else:visit(x);kept.append(x)
        if n.children is not None:n.children=kept
    visit(candidate)
    require(len(found)==1,'exactly one native-style HUS header required')
    require(shape(native)==shape(candidate),'GUI changed outside the single added header')
    header=found[0]
    require(header.scalar('datacontext')=='[AccessPlayer.GetSocialHierarchy]','header has wrong context type')
    law_items=[n for n in header.walk() if n.key=='law_item_small']
    require(len(law_items)==1 and law_items[0].scalar('datacontext')=="[AccessPlayer.AccessActiveLawFromGroup('lawgroup_nesnd_hus_social_hierarchy')]",'law item is not native active-law context')
    effect=EFF['nesnd_hus_sync_cmf_law']
    require(effect.get('active_law:lawgroup_nesnd_hus_social_hierarchy') is not None,'CMF source not law scope')
    value=next(n for n in effect.walk() if n.key=='set_variable' and n.scalar('name')=='custom_social_hierarchy').scalar('value')
    require(value=='scope:nesnd_hus_display_law' and not value.endswith('.type'),'CMF law_type confusion')
    return 'Ordered GUI AST identical after removing one added native-style header; native data contexts and CMF law object agree'
ck('native_GUI_narrow_AST_and_law_datatypes',only_header)

def loc_closure():
    databases={}
    for language in ('simp_chinese','english'):
        p=T/f'localization/{language}/replace/zzzz_nesnd_hus_social_hierarchy_l_{language}.yml'
        require(p.read_bytes().startswith(b'\xef\xbb\xbf'),'localization BOM missing')
        s=read(p);require(s.splitlines()[0]=='l_'+language+':','wrong language header')
        pairs=re.findall(r'^\s+([^ #][^:]*):(?:\d+)?\s+"((?:\\.|[^"\\])*)"\s*$',s,re.M)
        require(len(pairs)==len(s.splitlines())-1,('unparsed localization row',language))
        db=dict(pairs);require(len(db)==len(pairs),'duplicate local key')
        if language=='english':require(not re.search('[\u4e00-\u9fff]',s),'Chinese fallback in English file')
        databases[language]=db
    require(set(databases['english'])==set(databases['simp_chinese']),'translation key mismatch')
    keys=set(databases['english']);required=set()
    for n in tree('common/laws/nesnd_hus_social_hierarchy.txt').children:required|={n.key,n.key+'_desc'}
    for n in tree('common/social_classes/nesnd_hus_social_classes.txt').children:required|={n.key,n.key+'_desc'}
    for n in tree('common/modifier_type_definitions/nesnd_hus_social_class_modifiers.txt').children:required|={n.key,n.key+'_desc'}
    for rel in ['common/scripted_buttons/nesnd_hus_registration.txt','common/journal_entries/nesnd_hus_registration.txt','common/scripted_triggers/nesnd_hus_registration.txt','events/nesnd_hus_registration.txt']:
        source=tree(rel)
        for n in source.walk():
            # Internal variable/save_scope_value_as.name is not a localization reference.
            if n.key in ('desc','title','text','custom_tooltip') and n.value and n.value.startswith('nesnd_hus_'):required.add(n.value)
            if n.key=='option' and n.scalar('name'):required.add(n.scalar('name'))
        if '/scripted_buttons/' in rel:
            required.update(n.scalar('name') for n in source.children if n.scalar('name'))
    require(required<=keys,('missing HUS text',sorted(required-keys)))
    external={'HUS','CNE','lawgroup_citizenship','concept_pops'}
    for lang,db in databases.items():
        for key,value in db.items():
            refs=set(re.findall(r'\$([A-Za-z0-9_]+)\$',value))
            require(refs <= keys|external,('unresolved alias',lang,key,refs-keys-external))
    return f'{len(keys)} paired keys, BOM/header/quote parsing, no English Chinese fallback, required legal/UI text and aliases closed'
ck('Chinese_English_effective_text_and_references',loc_closure)

def ordinary_preservation():
    native={basekey(n.key):n for n in parse(read(G/'common/laws/00_citizenship.txt')).children if n.key}
    for changed in tree('common/laws/zzzz_nesnd_hus_citizenship_lock.txt').children:
        key=basekey(changed.key);old=native[key];n=deepcopy(changed);n.key=key
        enact=n.get('can_enact');enact.children=[x for x in enact.children if x.key!='nesnd_hus_citizenship_unlocked']
        if not enact.children and old.get('can_enact') is None:n.children.remove(enact)
        impose=n.get('can_impose')
        impose.children=[x for x in impose.children if not (x.key=='scope:target_country' and len(x.children or [])==1 and x.children[0].key=='nesnd_hus_citizenship_unlocked')]
        require(shape(old)==shape(n),('ordinary citizenship changed outside two guards',key))
    return 'All six native citizenship law ordered ASTs are preserved except the two explicit freeze guards'
ck('six_ordinary_citizenship_native_AST_preservation',ordinary_preservation)

def legal_only_shared():
    rel='common/scripted_effects/nesnd_native_khanate.txt'
    old=parse(read(R/'batch-a-before'/rel));new=tree(rel)
    allowed={'nesnd_khanate_prepare','nesnd_native_primary_cultures_only','nesnd_khanate_form_native_hus'}
    old.children=[n for n in old.children if n.key not in allowed];new.children=[n for n in new.children if n.key not in allowed]
    require(shape(old)==shape(new),'NKH non-legal functions changed')
    rel='common/country_definitions/ce_countries.txt';old=parse(read(R/'batch-a-before'/rel));new=tree(rel)
    target=new.get('HUS');target.children=[x for x in target.children if x.key!='social_hierarchy']
    require(shape(old)==shape(new),'non-HUS country definition or original HUS fields changed')
    return 'NKH non-legal functions and all original country-definition fields remain ordered-AST identical'
ck('shared_Khanate_functions_and_country_definition_boundaries',legal_only_shared)

REPORT['status']='AST_AND_UI_STATIC_PASS_TOOLS_PENDING';save()
print(json.dumps({'status':REPORT['status'],'static_closure_cases':REPORT['static_closure_cases']},ensure_ascii=False))
