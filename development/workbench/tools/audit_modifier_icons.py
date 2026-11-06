from __future__ import annotations
import argparse, collections, difflib, hashlib, json, re, struct, sys
import tempfile
from pathlib import Path

GAME = Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
MOD = Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
WORKSHOP = Path(r'D:/Program Files (x86)/Steam/steamapps/workshop/content/529340')
WORK = Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
OUT = WORK / 'reports/prose-icons-20261106/icons'
sys.path.insert(0, r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse, basekey, unquote

ICON_DIR = 'gfx/interface/icons/timed_modifier_icons/'


def line_at(text: str, offset: int) -> int:
    return text.count('\n', 0, offset) + 1


def iter_files(root: Path, folder: str, suffix: str = '*.txt'):
    d = root / folder
    if d.exists():
        yield from sorted(d.rglob(suffix))


def is_dds(path: Path) -> bool:
    try:
        b = path.read_bytes()[:128]
    except OSError:
        return False
    return len(b) == 128 and b[:4] == b'DDS ' and struct.unpack_from('<I', b, 4)[0] == 124


def resource(value: str | None, roots=None):
    if value is None or not value.strip():
        return {'state': 'omitted', 'roots': [], 'is_dds': None}
    raw = unquote(value).replace('\\', '/')
    if raw.startswith('/') or re.match(r'^[A-Za-z]:', raw) or '..' in Path(raw).parts:
        return {'state': 'unknown_external', 'roots': [], 'is_dds': None}
    if not raw.startswith('gfx/'):
        return {'state': 'unknown_external', 'roots': [], 'is_dds': None}
    # Ordered loose-file precedence: the first root containing the exact file wins.
    # A corrupt MOD copy shadows a valid GAME file with the same resource path.
    hits = []
    for label, root in (roots or [('mod', MOD), ('game', GAME)]):
        f = root / Path(raw)
        if f.is_file():
            hit={'root': label, 'path': str(f), 'is_dds': is_dds(f)}
            if hit['is_dds']:
                return {'state': 'resolved', 'roots': [hit], 'is_dds': True}
            return {'state': 'invalid_dds', 'roots': [hit], 'is_dds': False}
    # Workshop-only files are noted as external dependencies, never treated as resolved
    # without an explicit enabled-dependency/load-order contract.
    if roots is None and WORKSHOP.exists():
        for external in sorted(p for p in WORKSHOP.iterdir() if p.is_dir()):
            f=external/Path(raw)
            if f.is_file():
                return {'state':'unknown_external','roots':[{'root':f'workshop:{external.name}','path':str(f),'is_dds':is_dds(f)}], 'is_dds':is_dds(f)}
    return {'state': 'explicit_missing', 'roots': [], 'is_dds': None}


def top_modifier_defs():
    rows=[]
    for f in iter_files(MOD, 'common/static_modifiers'):
        text=f.read_text(encoding='utf-8-sig')
        tree=parse(text)
        for node in tree.children or []:
            if node.key is None or node.children is None:
                continue
            key=basekey(node.key)
            if not key:
                continue
            icons=[n for n in (node.children or []) if n.key=='icon']
            icon_values=[n.value for n in icons]
            icon=icon_values[0] if icon_values else None
            # A definition is effectful if it contains any field other than icon metadata.
            effectful=any(n.key not in {'icon','comment'} for n in node.children or [])
            rows.append({'key':key,'raw_key':node.key,'file':str(f.relative_to(MOD)).replace('\\','/'),
                         'line':line_at(text,node.start),'node':node,'text':text,
                         'icon_nodes':icons,'icon':icon,'effectful':effectful,
                         'duplicate_icon':len(icons)>1})
    return rows


def collect_je_modifier_refs(tree,text,rel):
    found=[]
    for je in tree.children or []:
        if je.children is None: continue
        for field in je.children:
            if field.key=='modifiers_while_active' and field.children is not None:
                for entry in field.children:
                    name=entry.value if entry.key is None else (entry.value if entry.key=='modifier' else None)
                    if name: found.append((basekey(unquote(name)),rel,line_at(text,entry.start),'modifiers_while_active'))
            elif field.key=='scaling_modifiers_while_active' and field.children is not None:
                for entry in field.children:
                    if entry.key=='modifier' and entry.value:
                        found.append((basekey(unquote(entry.value)),rel,line_at(text,entry.start),'scaling_modifiers_while_active'))
    return found


def applied_modifier_refs():
    refs=collections.defaultdict(list)
    dynamic=[]
    scan_folders=['common','events','history','on_actions','decisions']
    seen=set()
    for folder in scan_folders:
        for f in iter_files(MOD,folder):
            if f in seen: continue
            seen.add(f)
            try:
                text=f.read_text(encoding='utf-8-sig')
                tree=parse(text)
            except (UnicodeError,ValueError):
                continue
            rel=str(f.relative_to(MOD)).replace('\\','/')
            for n in tree.walk():
                if n.key != 'add_modifier': continue
                name=None
                if n.children is not None:
                    nn=[x for x in n.children if x.key=='name' and x.value is not None]
                    if nn: name=nn[0].value.strip('"')
                elif n.value is not None:
                    name=n.value.strip('"')
                if name and not any(x in name for x in ('$','var:','scope:')):
                    refs[basekey(name)].append({'file':rel,'line':line_at(text,n.start),'consumer':'add_modifier'})
                elif name:
                    dynamic.append({'file':rel,'line':line_at(text,n.start),'consumer':'add_modifier','value':name})
            # Native JE contracts: bare static modifiers in modifiers_while_active,
            # and `modifier = KEY` in scaling_modifiers_while_active.
            if rel.startswith('common/journal_entries/'):
                for name,path,line,consumer in collect_je_modifier_refs(tree,text,rel):
                    refs[name].append({'file':path,'line':line,'consumer':consumer})
    return refs,dynamic


EFFECT_POLICY = {
    # exact modifier type -> (native icon family, numeric polarity that is beneficial)
    'country_expenses_add': ('coins', -1), 'country_government_wages_mult': ('coins', -1),
    'country_military_goods_cost_mult': ('coins', -1), 'country_military_wages_mult': ('coins', -1),
    'country_authority_add': ('statue', 1), 'country_authority_mult': ('statue', 1),
    'country_bureaucracy_mult': ('documents', 1), 'country_influence_add': ('statue', 1),
    'country_law_enactment_speed_mult': ('documents', 1), 'country_legitimacy_base_add': ('statue', 1),
    'country_prestige_add': ('statue', 1), 'country_prestige_mult': ('statue', 1),
    'country_tech_research_speed_mult': ('lightbulb', 1), 'country_tech_spread_mult': ('lightbulb', 1),
    'character_popularity_add': ('statue', 1),
    'state_construction_mult': ('gear', 1), 'state_education_access_add': ('lightbulb', 1),
    'state_infrastructure_mult': ('gear', 1), 'state_pop_qualifications_mult': ('lightbulb', 1),
    'state_tax_capacity_mult': ('coins', 1), 'state_tax_collection_mult': ('coins', 1),
    'state_turmoil_effects_mult': ('fire', -1),
    'unit_army_defense_mult': ('rifle', 1), 'unit_army_offense_mult': ('rifle', 1),
    'unit_defense_mult': ('rifle', 1), 'unit_offense_mult': ('rifle', 1),
    'unit_supply_consumption_mult': ('rifle', -1),
    'state_pop_support_movement_labor_mult': ('flag', 1),
    'state_pop_support_movement_land_reform_mult': ('flag', 1),
    'state_pop_support_movement_liberal_mult': ('flag', 1),
    'state_pop_support_movement_radical_mult': ('flag', 1),
    'interest_group_approval_add': ('flag', 1),
}
for _ig in ('armed_forces','devout','industrialists','intelligentsia','landowners','petty_bourgeoisie','rural_folk','trade_unions'):
    for _effect in ('approval_add','pol_str_mult','pop_attraction_mult'):
        EFFECT_POLICY[f'interest_group_ig_{_ig}_{_effect}']=('flag',1)
for _building in ('arms_industry','cotton_plantation','fishing_wharf','food_industry','furniture_manufactory','glassworks','iron_mine','opium_plantation','rice_farm','shipyard','silk_plantation','steel_mill','tea_plantation','textile_mill','tooling_workshop','urban_center'):
    EFFECT_POLICY[f'building_{_building}_throughput_add']=('gear',1)
EFFECT_POLICY['building_group_bg_manufacturing_throughput_add']=('gear',1)

ICON_SUFFIX={'coins':'coins','statue':'statue','documents':'documents','lightbulb':'lightbulb','gear':'gear','fire':'fire','rifle':'rifle','flag':'flag'}

# Ambiguous cultural/subject/identity mechanics stay keyed and reviewable.
KEY_ICON_DECISIONS = {
    # These choices are keyed because their compound effects have no one-dimensional polarity.
    'nesnd_c2_hus_frontier_pasture_passage_local': {'icon':'modifier_gear_positive.dds','reason':'Road-route infrastructure is the project’s defining state effect; construction trade-off remains in the tooltip.'},
    'nesnd_c2_hus_frontier_land_compensation_local': {'icon':'modifier_gear_positive.dds','reason':'Compensated road access is the project’s defining state effect; construction trade-off remains in the tooltip.'},
    'nesnd_hna_academy': {'icon':'modifier_lightbulb_positive.dds','reason':'Academy education access is the defining effect; payroll cost is not used as icon polarity.'},
    'nesnd_hna_supply': {'icon':'modifier_rifle_positive.dds','reason':'Military supply/support and defense are the defining effect; wages are not used as icon polarity.'},
    'nesnd_hna_veterans': {'icon':'modifier_fire_positive.dds','reason':'Veteran settlement reduces turmoil effects; payroll is a secondary fiscal side effect.'},
    'nesnd_wu_clemency': {'icon':'modifier_statue_positive.dds','reason':'Clemency is a political settlement choice; authority loss and lower turmoil are mixed outcomes.'},
    'nesnd_japan_reorganization': {'icon':'modifier_documents_positive.dds','reason':'Reorganization’s education and bureaucracy effects define the administrative program; wages are a secondary cost.'},
    'nesnd_india_french_teachers': {'icon':'modifier_lightbulb_positive.dds','reason':'French teachers’ education and qualification support define the route; liberty desire is left out of polarity.'},
    'nesnd_india_french_engineers': {'icon':'modifier_gear_positive.dds','reason':'French engineers’ workshop, steel and construction effects define the route; liberty desire is left out of polarity.'},
    'nesnd_india_french_officers': {'icon':'modifier_rifle_positive.dds','reason':'French officers’ offense and defense effects define the route; liberty desire is left out of polarity.'},
    'nesnd_jp_korea_governor': {'icon':'modifier_flag_positive.dds','reason':'Governor administration is the effect domain; higher tax capacity and harsher turmoil effects have mixed direction.'},
    'nesnd_jp_korea_councils': {'icon':'modifier_flag_positive.dds','reason':'Korean councils are the effect domain; tax capacity, schooling and turmoil effects are deliberately mixed.'},
    'nesnd_ottoman_common_allegiance': {'icon':'modifier_flag_positive.dds','reason':'Common allegiance is a cultural/political identity effect; assimilation direction is not treated as universal benefit.'},
    'nesnd_qe1_recovered_civil': {'icon':'modifier_documents_positive.dds','reason':'Civil recovery’s bureaucracy and public administration define the package; assimilation and conversion are not treated as polarity.'},
    'nesnd_small_specialised_market': {'icon':'modifier_gear_positive.dds','reason':'Specialised local market capacity and qualifications define the effect; authority expenditure is secondary.'},
    'nesnd_usm_ming_resistance': {'icon':'modifier_flag_positive.dds','reason':'Resistance is a political sovereignty effect; slower incorporation and added administration costs are intentional.'},
    'nesnd_small_own_market': {'icon':'modifier_coins_positive.dds','reason':'The 12-month own-market marker appears as a timed modifier despite having no numeric effects; coins-positive is the existing native market/trade resource motif.'},
}

def semantic_icon(key: str, children, name_lookup):
    if key in KEY_ICON_DECISIONS:
        choice=KEY_ICON_DECISIONS[key]
        return {'icon':ICON_DIR+choice['icon'],'policy':'keyed','reason':choice['reason']}
    fields=[(n.key,unquote(n.value) if n.value is not None else None) for n in children or [] if n.key and n.key!='icon']
    if not fields: return None
    policies=[]
    for field,value in fields:
        policy=EFFECT_POLICY.get(field)
        if policy is None: return {'manual':True,'policy':'unmapped_effect','reason':f'No explicit polarity contract for {field}'}
        family,beneficial_sign=policy
        outcome=0
        if beneficial_sign:
            try: number=float(value)
            except (TypeError,ValueError): return {'manual':True,'policy':'nonnumeric_effect','reason':f'Cannot classify {field}={value!r}'}
            outcome=1 if number*beneficial_sign>0 else (-1 if number*beneficial_sign<0 else 0)
        policies.append({'field':field,'family':family,'outcome':outcome,'value':value})
    # Political modifiers use the flag motif. Signed-only changes get matching polarity;
    # mixed-sign IG effects follow the native positive-flag convention.
    families=[x['family'] for x in policies]
    if 'flag' in families:
        fam='flag'
        flag_outcomes={x['outcome'] for x in policies if x['family']=='flag' and x['outcome']}
        if flag_outcomes=={-1,1}: outcome=1
        elif flag_outcomes=={-1}: outcome=-1
        else: outcome=1
    else:
        outcomes={x['outcome'] for x in policies if x['outcome']}
        if len(outcomes)>1:
            return {'manual':True,'policy':'conflicting_effect_polarity','reason':'Effects point in both positive and negative directions','effects':policies}
        outcome=next(iter(outcomes),0)
        # Cost icon is the clearer motif when a modifier is primarily a recurring expense.
        fam='coins' if 'coins' in families else families[0]
    sign='positive' if outcome>=0 else 'negative'
    icon=ICON_DIR+f"modifier_{ICON_SUFFIX[fam]}_{sign}.dds"
    return {'icon':icon,'policy':'effect_type_polarity','reason':f'{fam} family; polarity derived from explicit effect contracts','effects':policies}


def summarize():
    defs=top_modifier_defs()
    refs,dynamic=applied_modifier_refs()
    counts=collections.Counter()
    records=[]
    bykey=collections.defaultdict(list)
    for d in defs: bykey[d['key']].append(d)
    for d in defs:
        info=resource(d['icon'])
        dref=refs.get(d['key'],[])
        category=info['state']
        if category=='omitted' and dref and d['effectful']: category='iconless_applied_effectful'
        elif category=='omitted' and dref: category='iconless_applied_empty'
        elif category=='omitted' and d['effectful']: category='iconless_unreferenced_effectful'
        elif category=='omitted': category='iconless_unreferenced_empty'
        elif category=='resolved': category='resolved'
        elif category=='explicit_missing': category='explicit_missing'
        elif category=='invalid_dds': category='invalid_dds'
        elif category=='unknown_external': category='unknown_external'
        counts[category]+=1
        rec={'key':d['key'],'raw_key':d['raw_key'],'file':d['file'],'line':d['line'],'icon':d['icon'],
             'resource':info,'effectful':d['effectful'],'applied_references':dref,'classification':category,
             'duplicate_icon_fields':d['duplicate_icon']}
        records.append(rec)
    for empty_class in ('explicit_missing','invalid_dds','unknown_external'):
        counts.setdefault(empty_class,0)
    return defs,refs,dynamic,records,counts


def make_candidate(defs,refs,records):
    rec_by=( {(r['key'],r['file'],r['line']):r for r in records} )
    edits=collections.defaultdict(list)
    decision=[]
    for d in defs:
        r=rec_by[(d['key'],d['file'],d['line'])]
        needs=(r['classification'] in {'explicit_missing','invalid_dds','iconless_applied_effectful'} or
               (r['classification']=='iconless_applied_empty' and d['key'] in KEY_ICON_DECISIONS))
        if not needs: continue
        choice=semantic_icon(d['key'],d['node'].children,refs)
        if choice is None or choice.get('manual'):
            decision.append({'key':d['key'],'file':d['file'],'line':d['line'],'status':'manual_icon_semantics_required','current':d['icon'],
                             'policy':choice.get('policy') if choice else 'empty_definition','reason':choice.get('reason') if choice else 'No effect fields'})
            continue
        icon=choice['icon']
        if d['duplicate_icon']:
            decision.append({'key':d['key'],'file':d['file'],'line':d['line'],'status':'manual_duplicate_icon_conflict','candidate':icon,
                             'policy':choice['policy'],'reason':choice['reason']})
            continue
        if d['icon_nodes']:
            n=d['icon_nodes'][0]
            # Replace only scalar payload, preserving whether native source quotes values.
            raw_old=d['text'][n.vstart:n.vend]
            quote='"' if raw_old.startswith('"') else ''
            newval=quote+icon+quote
            edits[d['file']].append((n.vstart,n.vend,newval))
            status='replace_broken_icon'
        else:
            # Insert immediately in the definition's opening brace. Existing effects are unchanged.
            pos=d['node'].vstart
            if d['text'][pos:pos+1] != '{':
                decision.append({'key':d['key'],'file':d['file'],'line':d['line'],'status':'manual_unexpected_block_shape','candidate':icon})
                continue
            edits[d['file']].append((pos+1,pos+1,'\n\ticon = '+icon))
            status='add_icon'
        decision.append({'key':d['key'],'file':d['file'],'line':d['line'],'status':status,'candidate':icon,'baseline_classification':r['classification'],
                         'candidate_resource':resource(icon),'policy':choice['policy'],'reason':choice['reason'],'effects':choice.get('effects',[])})
    out=OUT/'candidate'
    out.mkdir(parents=True,exist_ok=True)
    for child in list(out.iterdir()):
        if child.is_file(): child.unlink()
        elif child.is_dir():
            import shutil; shutil.rmtree(child)
    patches=[]
    manifest=[]
    for rel,es in sorted(edits.items()):
        src=MOD/rel
        source_bytes=src.read_bytes()
        has_bom=source_bytes.startswith(b'\xef\xbb\xbf')
        newline='\r\n' if b'\r\n' in source_bytes else '\n'
        # Match pdx.read's universal-newline offsets; restore the original EOL on output.
        old=src.read_text(encoding='utf-8-sig')
        new=old
        for a,b,value in sorted(es,reverse=True): new=new[:a]+value+new[b:]
        diff=''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='a/'+rel,tofile='b/'+rel))
        patch_path=out/'patches'/Path(rel).with_suffix('.patch')
        patch_path.parent.mkdir(parents=True,exist_ok=True)
        patch_path.write_text(diff,encoding='utf-8')
        full_path=out/'files'/Path(rel)
        full_path.parent.mkdir(parents=True,exist_ok=True)
        preserved_eol=new.replace('\n',newline)
        full_path.write_bytes((b'\xef\xbb\xbf' if has_bom else b'')+preserved_eol.encode('utf-8'))
        before_sha=hashlib.sha256(source_bytes).hexdigest()
        after_sha=hashlib.sha256(full_path.read_bytes()).hexdigest()
        patch_rows=[d for d in decision if d.get('file')==rel and d['status'] in {'add_icon','replace_broken_icon'}]
        manifest.append({'file':rel,'before_sha256':before_sha,'candidate_sha256':after_sha,
                         'keys':[{'key':d['key'],'source_line':d['line'],'icon':d['candidate']} for d in patch_rows]})
        patches.append(diff)
    (out/'all-icons.patch').write_text(''.join(patches),encoding='utf-8')
    (out/'decisions.json').write_text(json.dumps(decision,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps({'files':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
    return decision


def validate_candidate(decisions):
    """Rebuild candidate source in memory, parse it, and resolve every added icon to real DDS."""
    edits=collections.defaultdict(list)
    applied=0
    for d in decisions:
        if d['status'] not in {'add_icon','replace_broken_icon'}: continue
        path=MOD/d['file']
        text=path.read_text(encoding='utf-8-sig')
        tree=parse(text)
        matches=[n for n in tree.children or [] if n.key and basekey(n.key)==d['key']]
        if not matches: raise AssertionError(f"candidate key vanished: {d['file']}:{d['key']}")
        # Decisions have an original source line; preserve repeated keys by selecting that line.
        node=next((n for n in matches if line_at(text,n.start)==d['line']),matches[0])
        icons=[n for n in node.children or [] if n.key=='icon']
        if d['status']=='add_icon':
            edits[d['file']].append((node.vstart+1,node.vstart+1,'\n\ticon = '+d['candidate']))
        else:
            if not icons: raise AssertionError(f"expected broken icon field missing: {d['key']}")
            raw_old=text[icons[0].vstart:icons[0].vend]
            quote='"' if raw_old.startswith('"') else ''
            edits[d['file']].append((icons[0].vstart,icons[0].vend,quote+d['candidate']+quote))
    final_by_file={}
    for rel,es in edits.items():
        original=(MOD/rel).read_text(encoding='utf-8-sig')
        revised=original
        for a,b,value in sorted(es,reverse=True): revised=revised[:a]+value+revised[b:]
        parse(revised)
        full_candidate=OUT/'candidate/files'/Path(rel)
        if full_candidate.read_text(encoding='utf-8-sig')!=revised:
            raise AssertionError(f'full candidate file does not match reconstructed patch: {rel}')
        parse(full_candidate.read_text(encoding='utf-8-sig'))
        final_by_file[rel]=revised
    for d in decisions:
        if d['status'] not in {'add_icon','replace_broken_icon'}: continue
        text=final_by_file[d['file']]
        tree=parse(text)
        matches=[n for n in tree.children or [] if n.key and basekey(n.key)==d['key']]
        node=next((n for n in matches if any(c.key=='icon' and unquote(c.value)==d['candidate'] for c in n.children or [])),None)
        if node is None: raise AssertionError(f"candidate definition not reparsed: {d['key']}")
        icons=[n for n in node.children or [] if n.key=='icon']
        if not icons: raise AssertionError(f"candidate icon absent after parse: {d['key']}")
        icon=unquote(icons[0].value)
        check=resource(icon)
        if check['state']!='resolved': raise AssertionError(f"candidate DDS did not resolve: {d['key']} => {icon} {check}")
        applied+=1
    return {'candidate_source_files_reparsed':len(final_by_file),'candidate_icon_properties':applied,
            'all_candidate_paths_resolve_exact_dds':True}


def audit_candidate_ig_polarity(defs,decisions):
    by_id={(d['key'],d['file'],d['line']):d for d in defs}
    checked=0; pure_negative=[]; pure_negative_correct=[]; mixed_positive=[]; non_flag_family=[]
    for choice in decisions:
        icon=choice.get('candidate','')
        definition=by_id.get((choice['key'],choice['file'],choice['line']))
        if definition is None: continue
        values=[]
        for effect in definition['node'].children or []:
            if not effect.key or not effect.key.startswith('interest_group_') or not effect.value: continue
            try: values.append(float(unquote(effect.value)))
            except ValueError: pass
        if not values: continue
        checked+=1
        if not icon.endswith(('modifier_flag_positive.dds','modifier_flag_negative.dds')):
            non_flag_family.append(choice['key'])
        all_negative=all(v<0 for v in values)
        has_both=any(v<0 for v in values) and any(v>0 for v in values)
        if all_negative and icon.endswith('modifier_flag_positive.dds'):
            pure_negative.append(choice['key'])
        if all_negative and icon.endswith('modifier_flag_negative.dds'):
            pure_negative_correct.append(choice['key'])
        if has_both and icon.endswith('modifier_flag_positive.dds'):
            mixed_positive.append(choice['key'])
    if pure_negative:
        raise AssertionError(f'all-negative IG modifier(s) must not use positive flag: {sorted(pure_negative)}')
    if non_flag_family:
        raise AssertionError(f'IG effects must use a flag-family icon unless keyed semantic review is added: {sorted(non_flag_family)}')
    return {'flag_candidates_with_ig_effects_checked':checked,
            'all_negative_ig_assigned_positive_flag':pure_negative,
            'all_negative_ig_assigned_negative_flag':pure_negative_correct,
            'ig_candidates_with_non_flag_icon':non_flag_family,
            'mixed_sign_ig_assigned_native_positive_flag':mixed_positive}


def markdown(records,counts,final_counts,decisions,source='main MOD'):
    bad=[r for r in records if r['classification'] not in {'resolved','iconless_unreferenced_or_empty'}]
    lines=['# Modifier icon audit','',f'Source: {source}. This is a static source/resource audit; no game launch or visual engine validation.','',
           '## Counts before candidate','', '| Classification | Definitions |','|---|---:|']
    for k,n in sorted(counts.items()): lines.append(f'| `{k}` | {n} |')
    lines+=['','## Candidate final counts','', '| Classification | Definitions |','|---|---:|']
    for k,n in sorted(final_counts.items()): lines.append(f'| `{k}` | {n} |')
    lines+=['',f'Total definitions scanned: **{len(records)}**.','',
            '## Findings','', '| Key | Source | Line | Class | Icon/resource | Applied references |','|---|---|---:|---|---|---|']
    for r in bad:
        resource_text=r['icon'] or '(no explicit icon)'
        hits='; '.join(f"{x['file']}:{x['line']}" for x in r['applied_references'][:4]) or '—'
        lines.append(f"| `{r['key']}` | `{r['file']}` | {r['line']} | `{r['classification']}` | `{resource_text}` | {hits} |")
    lines+=['','## Candidate decisions','',f'Candidate edits prepared: **{sum(d["status"] in {"add_icon","replace_broken_icon"} for d in decisions)}**; require manual icon choice: **{sum(d["status"].startswith("manual_") for d in decisions)}**.','',
            'The candidate patches add/replace only `icon` properties and reuse GAME DDS files. Each candidate path was resolved exactly and its DDS magic validated. Apply semantics of duplicate static modifier definitions still require review before merge; this output is a unified source diff rather than a standalone override file.','',
            'Polarity is mapped by effect type, not by assuming any negative numeric value is harmful. Cost reductions use positive coins; lower turmoil effects use positive fire while higher turmoil effects use negative fire; construction, education and military effects use their explicit per-type direction. Ambiguous combined modifiers use keyed choices in `KEY_ICON_DECISIONS` with rationale stored per key. Political/mixed IG modifiers use the flag motif without claiming either direction is universally beneficial. GAME has no neutral timed-modifier icon family. Mixed-sign IG modifiers follow native precedent: `modifier_army_bases` at GAME `common/static_modifiers/02_event_modifiers.txt:1244` combines IG approval gains and losses while using `modifier_flag_positive.dds`.','',
            '### Candidate icon decisions','', '| Key | Definition | Line | Candidate icon | Resolved file |','|---|---|---:|---|---|']
    for d in decisions:
        if d['status'] not in {'add_icon','replace_broken_icon'}: continue
        hits='; '.join(x['path'] for x in d.get('candidate_resource',{}).get('roots',[])) or '—'
        lines.append(f"| `{d['key']}` | `{d['file']}` | {d['line']} | `{d['candidate']}` | `{hits}` |")
    lines.append('')
    return '\n'.join(lines)


def current_hus_iconless_keys(records,source_file,baseline_keys):
    return {r['key'] for r in records if r['file']==source_file and r['key'] in baseline_keys and r['classification']=='iconless_applied_effectful'}


def run_regression():
    # Real source regression: parser must preserve duplicate top-level names, ignore comment-only icon,
    # retain quoted brace/hash value and keep the pre-change HUS sample immutable.
    fixture='''dup = { effect = 1 }\ndup = { effect = 2 }\n# icon = gfx/fake.dds\nquoted = { note = "brace } # in string" effect = 1 }\n'''
    tree=parse(fixture)
    assert len([n for n in tree.children if n.key=='dup'])==2
    assert all(not any(c.key=='icon' for c in n.children or []) for n in tree.children if n.key=='dup')
    q=next(n for n in tree.children if n.key=='quoted')
    assert q.get('note').value=='"brace } # in string"'
    je_text='sample_je = { modifiers_while_active = { live_modifier } scaling_modifiers_while_active = { modifier = scaled_modifier value = { value = 0.5 } } }'
    je_refs=collect_je_modifier_refs(parse(je_text),je_text,'common/journal_entries/fixture.txt')
    assert {(x[0],x[3]) for x in je_refs}=={('live_modifier','modifiers_while_active'),('scaled_modifier','scaling_modifiers_while_active')}
    defs,refs,dynamic,records,counts=summarize()
    before=json.loads((OUT/'fixtures/hus-iconless-before.json').read_text(encoding='utf-8'))
    before_keys={x['key'] for x in before['definitions']}
    assert len(before_keys)==before['expected_iconless_applied_effectful_count_before']==26
    current_hus={r['key'] for r in records if r['file']==before['source_file'] and r['key'] in before_keys}
    assert current_hus==before_keys, f'HUS baseline definitions absent from current scan: {sorted(before_keys-current_hus)}'
    assert all(key in refs for key in before_keys), 'HUS baseline definitions should retain actual modifier consumers'
    current_hus_iconless=current_hus_iconless_keys(records,before['source_file'],before_keys)
    # Regression contract: after candidate application, the frozen before-list still
    # validates while current missing count is allowed to reach zero.
    postapply_records=[{'file':before['source_file'],'key':key,'classification':'resolved'} for key in before_keys]
    assert not current_hus_iconless_keys(postapply_records,before['source_file'],before_keys)
    # Real-bug detector: exact absent GAME path is a missing explicit resource; fake DDS magic is rejected.
    bad=MOD/'gfx/interface/icons/test-only-icon-absent.dds'
    assert resource('gfx/interface/icons/test-only-icon-absent.dds')['state']=='explicit_missing'
    assert is_dds(GAME/'gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds')
    cost_reduction=semantic_icon('sample_military_recovery',[type('N',(),{'key':'country_military_goods_cost_mult','value':'-0.2'})()],{})
    turmoil_reduction=semantic_icon('sample_veterans',[type('N',(),{'key':'state_turmoil_effects_mult','value':'-0.1'})()],{})
    turmoil_increase=semantic_icon('sample_unrest',[type('N',(),{'key':'state_turmoil_effects_mult','value':'0.1'})()],{})
    ig_negative=semantic_icon('sample_ig_loss',[type('N',(),{'key':'interest_group_ig_armed_forces_approval_add','value':'-2'})()],{})
    ig_attraction_negative=semantic_icon('sample_ig_attraction_loss',[type('N',(),{'key':'interest_group_ig_devout_pop_attraction_mult','value':'-0.1'})()],{})
    ig_mixed=semantic_icon('sample_ig_tradeoff',[type('N',(),{'key':'interest_group_ig_armed_forces_approval_add','value':'2'})(),type('N',(),{'key':'interest_group_ig_landowners_approval_add','value':'-2'})()],{})
    assert cost_reduction['icon'].endswith('modifier_coins_positive.dds')
    assert turmoil_reduction['icon'].endswith('modifier_fire_positive.dds')
    assert turmoil_increase['icon'].endswith('modifier_fire_negative.dds')
    assert ig_negative['icon'].endswith('modifier_flag_negative.dds')
    assert ig_attraction_negative['icon'].endswith('modifier_flag_negative.dds')
    assert ig_mixed['icon'].endswith('modifier_flag_positive.dds')
    with tempfile.NamedTemporaryFile(suffix='.dds') as fake:
        fake.write(b'not a DDS file'+b'\0'*124); fake.flush()
        assert not is_dds(Path(fake.name)), 'DDS filename alone must not validate'
    return {'fixture_duplicates_preserved':True,'comments_ignored':True,'quoted_brace_hash_preserved':True,'journal_active_and_scaling_modifier_contracts_parsed':True,
            'missing_realistic_fixture_detected':True,'native_dds_magic_validated':True,'fake_dds_magic_rejected':True,
            'military_cost_reduction_uses_positive_icon':True,'turmoil_reduction_uses_positive_icon':True,'turmoil_increase_uses_negative_icon':True,
            'pure_negative_ig_approval_uses_negative_icon':True,'pure_negative_ig_attraction_uses_negative_icon':True,'mixed_sign_ig_uses_native_positive_flag':True,
            'hus_before_snapshot_entries':len(before_keys),'hus_current_iconless_active_count':len(current_hus_iconless),
            'hus_current_iconless_active_keys':sorted(current_hus_iconless),'hus_postapply_zero_count_is_allowed':True}


def run_shadow_regression():
    native=GAME/'gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds'
    assert is_dds(native)
    with tempfile.TemporaryDirectory() as td:
        modroot=Path(td)/'mod'; gameroot=Path(td)/'game'
        rel=Path('gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds')
        bad=modroot/rel; good=gameroot/rel
        bad.parent.mkdir(parents=True); good.parent.mkdir(parents=True)
        bad.write_bytes(b'bad override'+b'\0'*124)
        good.write_bytes(native.read_bytes())
        resolution=resource(rel.as_posix(), [('mod',modroot),('game',gameroot)])
        assert resolution['state']=='invalid_dds' and resolution['roots'][0]['root']=='mod',resolution
    return {'invalid_mod_shadow_does_not_fall_through_to_game':True}


def apply_candidate_guarded():
    manifest=json.loads((OUT/'candidate/manifest.json').read_text(encoding='utf-8'))
    return apply_manifest_guarded(manifest['files'],MOD,OUT/'candidate/files')


def apply_manifest_guarded(rows, mod_root, candidate_files_root):
    writes=[]
    # Preflight every file and candidate hash before touching any main-MOD file.
    for row in rows:
        rel=Path(row['file'])
        target=(mod_root/rel).resolve(); modroot=mod_root.resolve()
        if modroot not in target.parents: raise ValueError(f'candidate path escapes MOD: {rel}')
        candidate=(candidate_files_root/rel).resolve()
        if candidate_files_root.resolve() not in candidate.parents: raise ValueError(f'candidate source path escapes: {rel}')
        if hashlib.sha256(target.read_bytes()).hexdigest()!=row['before_sha256']:
            raise RuntimeError(f'guard mismatch; MOD changed since candidate: {rel}')
        payload=candidate.read_bytes()
        if hashlib.sha256(payload).hexdigest()!=row['candidate_sha256']:
            raise RuntimeError(f'candidate copy hash mismatch: {rel}')
        writes.append((target,payload))
    for target,payload in writes: target.write_bytes(payload)
    return len(writes)


def run_apply_guard_regression():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'mod'; files=Path(td)/'candidate/files'; rel='common/static_modifiers/sample.txt'
        target=root/rel; candidate=files/rel
        target.parent.mkdir(parents=True); candidate.parent.mkdir(parents=True)
        target.write_bytes(b'old') ; candidate.write_bytes(b'new')
        row={'file':rel,'before_sha256':hashlib.sha256(b'old').hexdigest(),'candidate_sha256':hashlib.sha256(b'new').hexdigest()}
        assert apply_manifest_guarded([row],root,files)==1 and target.read_bytes()==b'new'
        row['before_sha256']=hashlib.sha256(b'old').hexdigest()
        try: apply_manifest_guarded([row],root,files)
        except RuntimeError: pass
        else: raise AssertionError('hash mismatch must refuse candidate write')
        assert target.read_bytes()==b'new'
    return {'guarded_apply_success_and_stale_hash_refusal':True}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--no-candidate',action='store_true')
    ap.add_argument('--check',action='store_true',help='exit nonzero when current MOD has explicit bad paths or active nonempty icon omissions')
    ap.add_argument('--apply-candidate',action='store_true',help='apply every candidate file only after all source/candidate SHA-256 guards pass')
    args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    if args.apply_candidate:
        print(json.dumps({'applied_files':apply_candidate_guarded(),'mod':str(MOD)},ensure_ascii=False))
        return 0
    regression=run_regression()
    shadow=run_shadow_regression()
    apply_guard=run_apply_guard_regression()
    defs,refs,dynamic,records,counts=summarize()
    decisions=[] if args.no_candidate else make_candidate(defs,refs,records)
    final_check={} if args.no_candidate else validate_candidate(decisions)
    ig_polarity={} if args.no_candidate else audit_candidate_ig_polarity(defs,decisions)
    final_counts=counts.copy()
    if not args.no_candidate:
        final_counts['resolved']+=final_check['candidate_icon_properties']
        for decision in decisions:
            if decision['status'] not in {'add_icon','replace_broken_icon'}: continue
            final_counts[decision['baseline_classification']]-=1
    source_errors=sum(counts[k] for k in ('explicit_missing','invalid_dds','unknown_external','iconless_applied_effectful','iconless_applied_empty'))
    (OUT/'audit.json').write_text(json.dumps({'game':str(GAME),'mod':str(MOD),'version':json.loads((GAME.parent/'launcher/launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],'before_counts':counts,'candidate_final_counts':final_counts,'candidate_validation':final_check,'candidate_ig_polarity':ig_polarity,'records':records,'dynamic_modifier_references':dynamic,'parser_regression':regression,'resource_shadow_regression':shadow,'guarded_apply_regression':apply_guard,'check_errors':source_errors},ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'audit.md').write_text(markdown(records,counts,final_counts,decisions),encoding='utf-8')
    (OUT/'parser-regression.json').write_text(json.dumps({'parser':regression,'resource_shadow':shadow,'guarded_apply':apply_guard},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'records':len(records),'before_counts':counts,'candidate_final_counts':final_counts,'candidate_validation':final_check,'candidate_ig_polarity':ig_polarity,'candidate_decisions':collections.Counter(d['status'] for d in decisions),'regression':regression,'resource_shadow':shadow,'guarded_apply':apply_guard,'dynamic_references':len(dynamic),'check_errors':source_errors,'out':str(OUT)},ensure_ascii=False,default=dict))
    return 1 if args.check and source_errors else 0

if __name__=='__main__': sys.exit(main())
