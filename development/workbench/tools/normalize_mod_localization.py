"""Apply reviewed unique localization ownership and descriptive script filenames."""
from pathlib import Path
import collections, hashlib, json, re, sys
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
C=W/'exports/maintenance-current'; R=W/'reports/branch-naming-cleanup-20261104'
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
def read(p):return p.read_text(encoding='utf-8-sig')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'\xef\xbb\xbf'+s.replace('\r\n','\n').replace('\n','\r\n').encode())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def remove_file(p):
    assert p.resolve().is_relative_to(C.resolve()) and p.is_file()
    p.unlink()
plan=json.loads(read(R/'localization-duplicate-consolidation-plan.json'))
approved=json.loads(read(R/'root-approved-localization.json'))
edits={(x['lang'],x['key']):x['new'] for x in approved}
assert len(edits)==len(approved)
line_rx=re.compile(r'^\s*(?P<key>[^\s:#]+)\s*:\s*(?P<version>\d*)\s*"(?P<value>(?:\\.|[^"\\])*)"\s*(?:#.*)?$')
rows=collections.defaultdict(list);file_lines={};old_hashes={}
for lang in ('english','simp_chinese'):
    for p in sorted((C/'localization'/lang).rglob('*.yml')):
        rel=p.relative_to(C).as_posix();lines=read(p).splitlines();file_lines[rel]=lines;old_hashes[rel]=digest(p)
        for n,line in enumerate(lines):
            m=line_rx.match(line)
            if m: rows[(lang,m['key'])].append({'path':rel,'index':n,'value':m['value'],'line':line})

special_zero={'ce_cne_land_draft_failing','ce_cne_land_draft_failing_reason','ce_cne_reform_limited_market_access','ce_cne_war_with_usm','ce_cne_war_with_western_qin','NOT_TRIGGER_MARKET_ACCESS_LESS_THAN'}
choices={}
for row in plan['keys']:
    k=(row['locale'],row['key']);actual=rows[k]
    # This is the root-reviewed index list, not an inference about engine load order.
    index=0 if row['key'] in special_zero or row['occurrence_value_count']==1 else 1
    selected=row['occurrences'][index]
    assert any(x['path']==selected['path'] and x['value']==selected['value'] for x in actual),k
    choices[k]=next(x for x in actual if x['path']==selected['path'] and x['value']==selected['value'])

def topic_for(key,old):
    stem=re.sub(r'^z+_','',Path(old).stem)
    stem=re.sub(r'_l_(english|simp_chinese)$','',stem)
    if key.startswith(('STATE_','HUB_NAME_','region_')):return 'map/nesnd_geography'
    if key.startswith(('nesnd_qe1','nesnd_qin','nesnd_sweep_qin','nesnd_sweep_four_states','nesnd_sweep_economic_victory','nesnd_sweep_military_victory')):return 'nesnd_qin_politics'
    if key.startswith(('nesnd_per','nesnd_persian')):return 'nesnd_persia'
    if key.startswith(('nesnd_cne','nesnd_land','ce_cne','cne_')):return 'nesnd_cne_land_reform'
    if key.startswith(('nesnd_chen','nesnd_protect_chen')):return 'nesnd_chen_security'
    if key.startswith(('nesnd_jp','nesnd_japan','gov_nesnd_japan')):return 'nesnd_japan'
    if key.startswith(('nesnd_small_','nesnd_small.')):return 'nesnd_small_states'
    if key.startswith(('nesnd_egypt','dp_nesnd_egypt','subject_type_nesnd_egypt')):return 'nesnd_egypt'
    if key.startswith(('nesnd_prussian','nesnd_austrian','nesnd_usa_','nesnd_europe_america')):return 'nesnd_europe_america'
    if key.startswith('nesnd_ottoman'):return 'nesnd_ottoman'
    if key.startswith('nesnd_canon'):return 'nesnd_diplomatic_negotiations'
    if key.startswith('nesnd_unity'):return 'nesnd_unity_policies'
    if key.startswith(('nesnd_india','nesnd_prince','nesnd_tianzhu','nesnd_yuanshan')):return 'nesnd_india'
    if key.startswith(('nesnd_native','nesnd_khanate','nesnd_american_restoration','nesnd_restoration','nesnd_hus_registration.','wg_nesnd_','war_goal_wg_nesnd_')):return 'nesnd_native_americas'
    if key.startswith(('nesnd_board','nesnd_south','nesnd_ming','nesnd_court','nesnd_federal')):return 'nesnd_south_politics'
    fallback={'nesnd_batch_c':'nesnd_diplomatic_negotiations','nesnd_a2_native_americas':'nesnd_native_americas','nesnd_qin_persia':'nesnd_qin_persia','nesnd_bug_sweep':'nesnd_journal_tooltips','nesnd_feedback':'nesnd_button_tooltips','nesnd_native_errors':'nesnd_native_compatibility','nesnd_canon':'nesnd_country_routes','nesnd_regional':'nesnd_regional_development'}
    return fallback.get(stem,stem)

owners={};final={};selection=[]
for (lang,key),occ in rows.items():
    selected=choices.get((lang,key),occ[0]);old=selected['path'];value=edits.get((lang,key),selected['value'])
    if re.match(r'^z{2,}',Path(old).name):
        owner=f'localization/{lang}/replace/{topic_for(key,old)}_l_{lang}.yml'
    else:owner=old
    # Original author files keep the unique definition when the same key is copied elsewhere.
    if len(occ)>1:
        native=[x for x in occ if not re.match(r'^z{2,}',Path(x['path']).name)]
        if native:owner=next((x['path'] for x in native if x['path']==old),native[0]['path'])
    owners[(lang,key)]=owner;final[(lang,key)]=value
    if len(occ)>1:selection.append({'lang':lang,'key':key,'selected_source':old,'selected_value':selected['value'],'final_owner':owner,'final_value':value,'reason':'Root individually reviewed all multi-value conflicts; exact duplicates retained once.'})

for row in approved:
    k=(row['lang'],row['key'])
    if k not in rows:
        assert row['key'].startswith(('nesnd_qe1_condition_','nesnd_egypt_condition_')),k
        topic='nesnd_qin_politics' if row['key'].startswith('nesnd_qe1') else 'nesnd_egypt'
        owners[k]=f"localization/{row['lang']}/replace/{topic}_l_{row['lang']}.yml"
        final[k]=row['new']

# Native status_desc is localized with ROOT=owning country, not a JournalEntry GUI object.
status_keys={'nesnd_egypt_without_investor_status','nesnd_egypt_lost_investor_status','nesnd_egypt_with_investor_status','nesnd_austrian_dispute_status','nesnd_usa_border_selected_status','nesnd_small_independent_status','nesnd_small_subject_status','nesnd_small_regional_status','nesnd_south_reconciliation_status'}
status_changes=[]
for k,value in list(final.items()):
    if k[1] in status_keys:
        assert 'JournalEntry.GetCountry' in value,k
        final[k]=value.replace('JournalEntry.GetCountry','ROOT.GetCountry')
        status_changes.append({'lang':k[0],'key':k[1],'before':value,'after':final[k]})

emitted=set();outputs={}
for rel,lines in file_lines.items():
    if re.match(r'^z{2,}',Path(rel).name):continue
    lang=Path(rel).parts[1];out=[]
    for line in lines:
        m=line_rx.match(line)
        if not m:out.append(line);continue
        k=(lang,m['key'])
        if owners[k]==rel and k not in emitted:
            # Keep the original line (and its inline comment) if its value is unchanged.
            out.append(line if m['value']==final[k] else f' {m["key"]}:0 "{final[k]}"')
            emitted.add(k)
    outputs[rel]=out
for k,value in final.items():
    if k in emitted:continue
    rel=owners[k]
    if rel not in outputs:outputs[rel]=['l_'+k[0]+':']
    outputs[rel].append(f' {k[1]}:0 "{value}"');emitted.add(k)
assert emitted==set(final)
for rel,lines in outputs.items():
    p=C/rel;text='\n'.join(lines)+'\n'
    if not p.exists() or read(p)!=text:write(p,text)
removed_locales=[]
for rel in file_lines:
    if rel not in outputs:remove_file(C/rel);removed_locales.append(rel)

# REPLACE of a MOD-owned definition becomes an edit of that definition itself.
# Native-only targets retain their explicit REPLACE directive in a descriptive file.
script_changes=[];merges=[]
for item in plan['script_rename_plan']:
    old=C/item['current_path'];new=C/item['proposed_path'];text=read(old);tree=parse(text);cuts=[]
    for node in tree.children or []:
        if not (node.key or '').startswith('REPLACE:'):continue
        key=node.key.split(':',1)[1];matches=[]
        for p in old.parent.glob('*.txt'):
            if p==old or re.match(r'^z{2,}',p.name):continue
            for other in parse(read(p)).children or []:
                if other.key==key:matches.append((p,other))
        assert len(matches)<=1,(key,matches)
        if matches:
            p,other=matches[0];dest=read(p)
            replacement=key+' = '+text[node.vstart:node.end]
            write(p,dest[:other.start]+replacement+dest[other.end:])
            cuts.append((node.start,node.end));merges.append({'source':item['current_path'],'id':key,'destination':p.relative_to(C).as_posix()})
    for start,end in sorted(cuts,reverse=True):text=text[:start]+text[end:]
    if parse(text).children:
        assert not new.exists(),new
        if not cuts:new.write_bytes(old.read_bytes())
        else:write(new,text)
        script_changes.append({'old':item['current_path'],'new':item['proposed_path'],'payload_unchanged':not cuts})
    else:script_changes.append({'old':item['current_path'],'new':None,'merged_definitions':True})
    remove_file(old)

report={'localization_keys_before':len(rows),'localization_keys_after':len(final),'duplicate_key_groups_resolved':len(selection),'removed_long_prefix_locale_files':removed_locales,'key_ownership':{lang:{k:owners[(lang,k)] for l,k in final if l==lang} for lang in ('english','simp_chinese')},'duplicate_selection':selection,'status_context_repairs':status_changes,'script_renames':script_changes,'mod_owned_definition_merges':merges,'locale_source_hashes_before':old_hashes}
(R/'normalization-implementation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'final-localization-values.json').write_text(json.dumps({lang:{k:v for (l,k),v in final.items() if l==lang} for lang in ('english','simp_chinese')},ensure_ascii=False,indent=2),encoding='utf-8')
print({'unique_keys':len(final),'duplicates_resolved':len(selection),'old_z_locales_removed':len(removed_locales),'scripts_renamed':len(script_changes),'definitions_edited_in_place':len(merges),'status_context_repairs':len(status_changes)})
