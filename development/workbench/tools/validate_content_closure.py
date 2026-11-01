"""Read-only literal content dependency closure, not a Jomini interpreter.

Preserves ordered PDX nodes and all symbol/localization providers. Dynamic data,
ambiguous overrides and engine-only resources are explicit review findings.
"""
from pathlib import Path
from collections import defaultdict,Counter,deque
import sys,re,json,hashlib,argparse
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read,effective_files,basekey,unquote
DB={'event':'events','journal':'common/journal_entries','button':'common/scripted_buttons',
    'bar':'common/scripted_progress_bars','modifier':'common/static_modifiers',
    'media':'gfx/media_aliases','effect':'common/scripted_effects','trigger':'common/scripted_triggers',
    'value':'common/script_values','concept':'common/game_concepts',
    'culture':'common/cultures','religion':'common/religions'}
IDENT=re.compile(r'^[A-Za-z_][A-Za-z0-9_.-]*$')
EVENT_ID=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z0-9_]+$')
# Paradox's one-line localization is not strict YAML: current vanilla contains
# internal unescaped quote marks (e.g. ep2_meiji.1.d, alaska.1.f). Preserve the
# whole text between its first and final delimiter instead of dropping the key.
LOC=re.compile(r'^\s*([A-Za-z0-9_.-]+):\s*(?:\d+\s*)?"(.*)"\s*(?:#.*)?$',re.M)
DOLLAR=re.compile(r'\$([A-Za-z0-9_.-]+)(?:\|[^$]*)?\$')

def audit(candidate,dependencies=None,languages=None):
    candidate=Path(candidate).resolve();dependencies=[Path(p).resolve() for p in dependencies or []]
    languages=list(languages or ['simp_chinese','english']);roots=[G,*dependencies,candidate]
    hard=[];review=[];edges=[];accessed={};cache={};defs={k:defaultdict(list) for k in [*DB,'entity','texture','mesh']};loc={l:defaultdict(list) for l in languages}
    emitted=set();queue=deque();seen=set();loc_queue=deque();loc_seen=set();asset_seen=set();asset_counts=Counter()
    modifier_names=[];literal_modifier_calls=set();native_template_shapes=defaultdict(list)
    template_re=re.compile(r'^(.+)_(fervor_target|standard_of_living|cultural_acceptance)_modifier_(positive|negative)$')
    def template_shape(key,node):
        m=template_re.fullmatch(key or '')
        if not m:return None
        identity=m[1]
        # Ordered full scalar body must match a current GAME template after only
        # its culture/religion token is abstracted. No arbitrary name exemption.
        if any(q.children is not None for q in node.children or []):return None
        return (m[2],m[3],tuple(((q.key or '').replace(identity,'<identity>'),q.op,q.value) for q in node.children or []))
    def finding(level,kind,path=None,line=None,**kw):
        origin='candidate' if path and Path(path).is_relative_to(candidate) else ('game' if path and Path(path).is_relative_to(G) else 'dependency_or_unspecified')
        row={'kind':kind,'origin':origin,**({'path':str(path)} if path else {}),**({'line':line} if line else {}),**kw};key=json.dumps(row,sort_keys=True,ensure_ascii=False)
        if key not in emitted:(hard if level=='hard' else review).append(row);emitted.add(key)
    def load(p):
        p=Path(p)
        if p in cache:return cache[p]
        raw=p.read_bytes();accessed[str(p)]=hashlib.sha256(raw).hexdigest()
        try:
            text,tree=read(p);cache[p]=(text,tree);return text,tree
        except (ValueError,UnicodeError) as e:
            finding('hard' if p.is_relative_to(candidate) else 'review','parse_unavailable',p,detail=str(e));cache[p]=(None,None);return None,None
    def place(p,n):
        text=cache[p][0];return {'path':str(p),'line':text.count('\n',0,n.start)+1 if text else None}
    def adddef(kind,key,p,n):
        if key:defs[kind][key].append((p,n))
    for kind,folder in DB.items():
        for p in effective_files(roots,folder):
            _,tree=load(p)
            if tree:
                for n in tree.children:
                    if n.key and n.children is not None:adddef(kind,basekey(n.key),p,n)
    for key,entries in defs['modifier'].items():
        for p,n in entries:
            if p.is_relative_to(G):
                sig=template_shape(key,n)
                if sig:native_template_shapes[sig].append({'path':str(p),'example_key':key})
    # Actual asset syntax: repeated entity/spriteType blocks use name, not their
    # block key, as identity. Keep each provider rather than dict-overwriting.
    for pattern in ['*.asset','*.gfx']:
        for p in effective_files(roots,'gfx',pattern):
            _,tree=load(p)
            if tree:
                for n in tree.walk():
                    if n.key=='entity' and n.children is not None:adddef('entity',n.scalar('name'),p,n)
                    elif n.key=='pdxmesh' and n.children is not None:adddef('mesh',n.scalar('name'),p,n)
                    elif n.key in ['spriteType','texture'] and n.children is not None:adddef('texture',n.scalar('name'),p,n)
    for lang in languages:
        for p in effective_files(roots,'localization/'+lang,'*.yml'):
            raw=p.read_bytes();accessed[str(p)]=hashlib.sha256(raw).hexdigest()
            try:text=raw.decode('utf-8-sig')
            except UnicodeError as e:finding('review','localization_decode',p,language=lang,detail=str(e));continue
            for m in LOC.finditer(text):loc[lang][m[1]].append((p,text.count('\n',0,m.start())+1,m[2]))
    # DLC asset locations are optional fallback sources; physical installation is
    # not DLC ownership/activation. Never certify entitlement from this lookup.
    dlc_roots=[p for p in (G/'dlc').iterdir() if p.is_dir()] if (G/'dlc').is_dir() else []
    def providers(kind,key):return [{'path':str(p),'line':place(p,n)['line'],'source_key':n.key} for p,n in defs[kind].get(key,[])]
    def ref(kind,value,p,n,context):
        info=place(p,n);value=unquote(value)
        if value is None:return
        if not IDENT.fullmatch(value) or value.startswith(('scope:','var:')):
            finding('review','dynamic_reference_not_run',**info,reference_type=kind,value=value,context=context,status='NOT_RUN');return
        entries=defs[kind].get(value,[]);edges.append({**info,'kind':kind,'target':value,'context':context,'provider_count':len(entries)})
        if kind=='modifier':literal_modifier_calls.add(value)
        if not entries:finding('hard','unresolved_literal_reference',**info,reference_type=kind,value=value,context=context);return
        if len(entries)>1:finding('review','multiple_symbol_providers',**info,reference_type=kind,value=value,providers=providers(kind,value),status='REVIEW')
        for pp,nn in entries:queue.append((pp,nn,kind,value))
    def locref(key,p,n,context):
        key=unquote(key);info=place(p,n)
        if not key:return
        if not IDENT.fullmatch(key):
            finding('review','dynamic_or_literal_text_not_resolved',**info,value=key,context=context,status='NOT_RUN');return
        for lang in languages:
            entries=loc[lang].get(key,[]);edges.append({**info,'kind':'localization','target':key,'language':lang,'context':context,'provider_count':len(entries)})
            if not entries:finding('hard','missing_localization_key',**info,key=key,language=lang,context=context)
            for pp,line,value in entries:loc_queue.append((lang,key,pp,line,value))
            if len(entries)>1 and len({x[2] for x in entries})>1:finding('review','conflicting_localization_providers',**info,key=key,language=lang,providers=[{'path':str(a),'line':b} for a,b,_ in entries],status='REVIEW')
    def asset(value,p,n,optional=False):
        value=unquote(value);info=place(p,n)
        if value in asset_seen:return
        asset_seen.add(value)
        if not value or any(x in value for x in ['$','[',']']):finding('review','dynamic_asset_not_run',**info,value=value,status='NOT_RUN');return
        found=next((r/value for r in reversed(roots) if (r/value).is_file()),None)
        dlc=next((r/value for r in dlc_roots if (r/value).is_file()),None) if not found else None
        edges.append({**info,'kind':'asset','target':value,'resolved_path':str(found or dlc) if found or dlc else None,'optional_fallback_primary':optional})
        if found:asset_counts['filesystem_present']+=1
        elif dlc:
            asset_counts['dlc_present_entitlement_unknown']+=1;finding('review','dlc_asset_activation_not_run',**info,value=value,physical_path=str(dlc),status='NOT_RUN')
        elif optional:finding('review','optional_primary_asset_missing',**info,value=value,detail='Media alias has a fallback; fallback is checked separately.')
        else:asset_counts['missing']+=1;finding('hard','missing_direct_asset',**info,value=value)
    # Every candidate content script is a seed, including hidden/orphaned events.
    # This is intentionally not a runtime reachability filter.
    for folder in ['common','events','gfx','gui']:
        for p in (candidate/folder).rglob('*') if (candidate/folder).exists() else []:
            if p.suffix.lower() not in ['.txt','.asset','.gfx','.gui']:continue
            _,tree=load(p)
            if tree:
                kind=next((k for k,v in DB.items() if p.is_relative_to(candidate/v)), 'script')
                for n in tree.children:queue.append((p,n,kind,basekey(n.key)))
    def scan(p,top,kind,key):
        # Exact UI fields, not every generic name/description in history.
        if kind=='journal':
            locref(key,p,top,'journal implicit title');locref(key+'_reason',p,top,'journal implicit reason')
        if kind=='modifier':modifier_names.append((key,p,top))
        def walk(n,parent=None):
            k=n.key;v=unquote(n.value) if n.value is not None else None
            if k=='trigger_event':ref('event',v if v is not None else n.scalar('id'),p,n,'trigger_event')
            elif k in ['events','random_events'] and n.children is not None:
                for q in n.walk():
                    vv=unquote(q.value)
                    if vv and EVENT_ID.fullmatch(vv):ref('event',vv,p,q,k)
                    elif vv and any(c in vv for c in ['$','[',':']):finding('review','dynamic_event_table_not_run',**place(p,q),value=vv,status='NOT_RUN')
            elif k=='add_journal_entry':ref('journal',v if v is not None else n.scalar('type'),p,n,k)
            elif k in ['has_journal_entry','remove_journal_entry'] and v:ref('journal',v,p,n,k)
            elif k=='scripted_button' and v:ref('button',v,p,n,k)
            elif k=='scripted_progress_bar' and v:ref('bar',v,p,n,k)
            elif k in ['add_modifier','remove_modifier','has_modifier']:
                ref('modifier',v if v is not None else n.scalar('name'),p,n,k)
            elif k=='video' and v and not v.startswith(('gfx/','dlc/')):ref('media',v,p,n,k)
            elif k=='texture' and v and not v.startswith(('gfx/','dlc/')):
                if parent and parent.key in ['colored_emblem','textured_emblem']:
                    asset('gfx/coat_of_arms/'+('colored_emblems' if parent.key=='colored_emblem' else 'textured_emblems')+'/'+v,p,n)
                elif v in defs['texture']:ref('texture',v,p,n,k)
                else:finding('review','texture_symbol_or_relative_path_not_run',**place(p,n),value=v,parent=parent.key if parent else None,status='NOT_RUN')
            elif k=='pattern' and v and 'coat_of_arms' in p.parts and not v.startswith('gfx/'):
                asset('gfx/coat_of_arms/patterns/'+v,p,n)
            elif k=='entity' and v:ref('entity',v,p,n,k)
            elif k=='pdxmesh' and v:ref('mesh',v,p,n,k)
            elif kind=='media' and k=='fallback' and v:ref('media',v,p,n,'media fallback')
            if v and v.startswith(('gfx/','dlc/','fonts/')):
                asset(v,p,n,optional=(kind=='media' and top.get('fallback') is not None and k in ['video','texture']))
            if v and v.startswith('event:/'):
                finding('review','audio_event_engine_bank_not_run',**place(p,n),value=v,status='NOT_RUN')
            isloc=(k in ['custom_tooltip','custom_tooltip_no_bullet'] and v is not None) or (k=='text' and parent and parent.key in ['custom_tooltip','custom_tooltip_no_bullet','modifier_tooltip'])
            if kind in ['event','journal','button','bar']:
                isloc=isloc or (k in ['title','desc','description','second_desc','status_desc','reason','custom_effect_description'] and v is not None)
                isloc=isloc or (k=='name' and v is not None and (n in (top.children or []) or (parent and parent.key=='option')))
            if isloc:locref(v,p,n,k)
            # Resolve known scripted helpers through the same provider graph.
            if k:
                for typ in ['effect','trigger','value']:
                    if k in defs[typ]:ref(typ,k,p,n,'scripted helper call')
            if v and v in defs['value']:ref('value',v,p,n,'script value literal use')
            for child in n.children or []:walk(child,n)
        walk(top)
    while queue:
        p,n,kind,key=queue.popleft();identity=(str(p),n.start,n.end,kind)
        if identity in seen:continue
        seen.add(identity);scan(p,n,kind,key)
    for key,p,n in modifier_names:
        sig=template_shape(key,n)
        match=template_re.fullmatch(key or '')
        defined_identity=bool(match and (match[1] in defs['culture'] or (match[2]=='standard_of_living' and match[1] in defs['religion'])))
        if sig in native_template_shapes and defined_identity and key not in literal_modifier_calls:
            finding('review','native_modifier_template_display_not_run',**place(p,n),key=key,status='NOT_RUN',
                    defined_identity=match[1],native_template_example=native_template_shapes[sig][0],
                    detail='Full ordered body matches a current GAME culture/religion template; no literal add/remove/has_modifier call found. Public display name is not inferred from this internal template key.')
        else:locref(key,p,n,'modifier display name')
    # Expands every reachable provider, preserving duplicates and cycles.
    while loc_queue:
        lang,key,p,line,value=loc_queue.popleft();identity=(lang,key,str(p),line)
        if identity in loc_seen:continue
        loc_seen.add(identity)
        for target in DOLLAR.findall(value):
            entries=loc[lang].get(target,[]);edges.append({'path':str(p),'line':line,'kind':'localization_expansion','target':target,'from_key':key,'language':lang,'provider_count':len(entries)})
            if not entries:
                finding('review' if target.upper()==target else 'hard','unresolved_dollar_expansion',p,line,key=key,target=target,language=lang,detail='Uppercase may be a runtime supplied localization argument; no provider found.',status='NOT_RUN' if target.upper()==target else 'FAIL')
            for pp,ll,vv in entries:loc_queue.append((lang,target,pp,ll,vv))
        for target in re.findall(r'\[(concept_[A-Za-z0-9_]+)\]',value):
            if target not in defs['concept'] and target not in loc[lang]:finding('hard','unresolved_concept',p,line,key=key,target=target,language=lang)
        if re.search(r'\[[^\]]*(?:Get|SCOPE|Scope|ROOT|root|var:)[^\]]*\]',value):finding('review','dynamic_localization_scope_not_run',p,line,key=key,language=lang,status='NOT_RUN')
    for lang in languages:
        graph=defaultdict(set)
        for e in edges:
            if e['kind']=='localization_expansion' and e['language']==lang and e['provider_count']:graph[e['from_key']].add(e['target'])
        visited=set();active=[];active_set=set()
        def cycle(k):
            if k in active_set:
                finding('review','localization_expansion_cycle',language=lang,cycle=active[active.index(k):]+[k],detail='All providers traversed; override winner must be resolved before classifying as a runtime failure.');return
            if k in visited:return
            visited.add(k);active.append(k);active_set.add(k)
            for target in sorted(graph.get(k,())):cycle(target)
            active.pop();active_set.remove(k)
        for k in sorted(graph):cycle(k)
    return {'candidate':str(candidate),'roots':[str(r) for r in roots],'languages':languages,'status':'FAIL' if hard else ('REVIEW' if review else 'PASS'),'engine_verified':False,
            'hard_errors':hard,'review_findings':review,'counts':{'hard_errors':len(hard),'review_findings':len(review),'traversed_definitions':len(seen),'reachable_localization_providers':len(loc_seen),'edges':len(edges),'source_files_read':len(accessed),'definitions':{k:len(v) for k,v in defs.items()},'assets':dict(asset_counts),'hard_by_kind':dict(Counter(x['kind'] for x in hard))},
            'edges':edges,'accessed_source_sha':accessed,
            'limits':['Literal reference closure only; no effect execution, scope validity, AI behavior, economic balance or UI rendering proved.',
                      'Same relative file overlays use existing effective_files; repeated nodes and distinct symbol providers remain visible. REPLACE/INJECT cross-file behavior is reviewed, not guessed.',
                      'Only the listed schema fields are interpreted; unknown dynamic scope/resource expressions are NOT_RUN, not inferred from names.',
                      'Audio bank events, dynamic localization arguments and DLC entitlement require engine checks. Filesystem media existence does not prove decode/render validity.',
                      'Full dependency source definitions are indexed; candidate scripts seed traversal. Multiple providers may include inactive overridden branches and are explicitly reviewed.',
                      'Asset bytes are not decoded or hashed merely to check presence; accessed_source_sha covers source text actually read.',
                      'Event and JE graph edges are routing evidence, not semantic reachability. Localized uppercase $TOKENS$ can be runtime parameters.']}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--dependency',action='append',type=Path,default=[]);p.add_argument('--language',action='append');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if not a.out.resolve().is_relative_to(W.resolve()):raise ValueError('Output must be in WORK')
    r=audit(a.candidate,a.dependency,a.language);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf-8');print(json.dumps({'status':r['status'],'counts':r['counts'],'out':str(a.out)},ensure_ascii=False));raise SystemExit(1 if r['hard_errors'] else 0)
