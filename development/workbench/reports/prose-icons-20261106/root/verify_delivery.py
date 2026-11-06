"""Check the reported source defects against native 1.15 structures, without running the game."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse, basekey
M=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
R=M.parents[1]/'nesnd-workbench/reports/prose-icons-20261106'
GIT=M.parents[1]/'nesnd-workbench/projects/nesnd-repository'
root=M if '--main' in sys.argv else R/'reviewed'
def read(rel):
    p=root/rel
    return parse((p if p.exists() else M/rel).read_text(encoding='utf-8-sig'))
def shape(n):
    return (n.key,n.op,n.value,tuple(shape(c) for c in n.children or []))
checks=[]
def check(name,ok):
    checks.append(dict(check=name,passed=bool(ok)))
    assert ok,name

# The noisy native text is reached by this sole source call. The Boolean subtree is identical.
old=parse((R/'root/south-holdouts-before.txt').read_text('utf-8-sig')).get('nesnd_south_defender_in_campaign_war')
new=read('common/scripted_triggers/nesnd_south_holdouts.txt').get('nesnd_south_defender_in_campaign_war')
wrapper=new.get('custom_tooltip')
check('War.GetName-producing native trigger has a context-free player tooltip',wrapper is not None and wrapper.scalar('text')=='nesnd_south_defender_in_campaign_war_tt')
check('Jingnan membership Boolean and PREV scope unchanged',tuple(shape(n) for n in old.children)==tuple(shape(n) for n in wrapper.children if n.key!='text'))
check('Native no-negotiated-peace setting retained',read('common/diplomatic_plays/ce_diplomatic_plays.txt').get('dp_usm_civil_war').scalar('allow_negotiated_peace')=='no')

agenda=read('common/journal_entries/nesnd_civic_routes.txt')
parent=agenda.get('nesnd_c2_hus_transport'); hub=agenda.get('nesnd_c2_hus_agenda')
choices={n.value for n in parent.all('scripted_button') if n.value!='nesnd_c2_hus_transport_retarget'}
check('Road choices have only their transport parent as owner',len(choices)==3 and not choices & {n.value for n in hub.all('scripted_button')})
children=read('common/journal_entries/nesnd_hus_road_projects.txt')
for je in children.children:
    a=je.get('is_shown_when_inactive');b=je.get('possible')
    check(je.key+' uses matching native inactive+activation predicates',a is not None and b is not None and tuple(shape(n) for n in a.children)==tuple(shape(n) for n in b.children))
    check(je.key+' follows actual transport parent',any(n.key=='has_journal_entry' and n.value=='nesnd_c2_hus_transport' for n in b.walk()))
    check(je.key+' has real progress bar and outcome',je.scalar('scripted_progress_bar') is not None and bool(je.all('outcome')))
helper=read('common/scripted_effects/nesnd_hus_road_projects.txt').get('nesnd_hus_road_attach_selected')
check('No duplicate explicit child add competing with activation',not any(n.key=='add_journal_entry' for n in helper.walk()))
small=read('common/journal_entries/nesnd_small_states.txt').get('nesnd_small_dispute_journal')
check('Dispute has response action and named time bar',small.scalar('scripted_button')=='nesnd_small_review_dispute' and small.scalar('scripted_progress_bar')=='nesnd_small_dispute_time_bar')
laws={n.value for n in small.walk() if n.key in ['has_law','has_law_or_variant']}
check('Dispute presents real law alternatives',{'law_type:law_slavery_banned','law_type:law_worker_protections','law_type:law_universal_suffrage','law_type:law_commercialized_agriculture','law_type:law_hindu_caste_not_enforced'}<=laws)
check('Dispute outcomes cannot pay duplicate rewards',all(o.get('effect') is None for o in small.all('outcome')))
review=read('common/scripted_effects/nesnd_small_dispute_display.txt').get('nesnd_small_dispute_review')
check('Reopening response does not restart its clock',not any(n.key in ['set_variable','change_variable','remove_variable'] for n in review.walk()))
check('Reopening supplies both event identity scopes',{n.scalar('name') for n in review.walk() if n.key=='save_scope_value_as'}=={'small_episode_serial','small_episode_regime'})

# Native outcome records, not a simulated state machine. Six explicitly parent-bound exceptions.
exceptions={'nesnd_cne_confidence_journal','nesnd_cne_land_journal','nesnd_cne_urban_journal','nesnd_cne_camps_journal','nesnd_qe1_economy_journal','nesnd_qe1_army_journal'}
paths={p.name:p for p in (M/'common/journal_entries').glob('*.txt')}
paths.update({p.name:p for p in (root/'common/journal_entries').glob('*.txt')})
definitions={}
for path in sorted(paths.values(),key=lambda p:p.name):
    for n in parse(path.read_text('utf-8-sig')).children:
        if n.key: definitions[basekey(n.key)]=n
missing=[];active=0
for key,je in definitions.items():
    possible=je.get('possible')
    if possible is not None and possible.scalar('always')=='no':continue
    active+=1
    visible=[o for o in je.all('outcome') if not(o.get('flags') and 'hidden' in o.get('flags').values())]
    if not visible and key not in exceptions:missing.append(key)
    for o in visible:
        check(key+' visible outcome contains native fields',all(o.scalar(k) for k in ['header','effect_header','conclusion_desc']))
check('Every automatically enabled standalone JE has visible outcome',not missing)

pattern=re.compile(r'^\s*([^\s:#]+):\d*\s*"(.*)"\s*$',re.M)
signature=lambda s: (sorted(re.findall(r'\[[^\]]*\]',s)),sorted(re.findall(r'\$[^$]+\$',s)))
prose_report=[]
manifest=json.loads((R/'root/delivery-manifest.json').read_text('utf-8'))
for row in manifest:
    p=root/row['file']
    if p.suffix=='.txt':parse(p.read_text('utf-8-sig'));continue
    if p.suffix!='.yml':continue
    raw=p.read_bytes();text=raw.decode('utf-8-sig');pairs=pattern.findall(text)
    check(row['file']+' BOM/header and one valid entry per line',raw.startswith(b'\xef\xbb\xbf') and text.startswith('l_') and all(pattern.fullmatch(line) or not line.strip() or line.lstrip().startswith(('#','l_')) for line in text.splitlines()))
    check(row['file']+' keys unique',len(pairs)==len(dict(pairs)))
    if p.name not in ['nesnd_civic_characters_l_simp_chinese.yml','nesnd_small_states_l_simp_chinese.yml','nesnd_phi_finance_l_simp_chinese.yml','nesnd_native_americas_l_simp_chinese.yml']:continue
    before=dict(pattern.findall((M/row['file'] if root!=M else R/'root/premerge'/row['file']).read_text('utf-8-sig')))
    check(p.name+' exact key set and order unchanged',list(before)==[k for k,v in pairs])
    for k,v in pairs:
        check(k+' dynamic functions and aliases preserved',signature(before[k])==signature(v))
    prose_report.append({'file':row['file'],'keys':len(pairs),'changed':sum(before[k]!=v for k,v in pairs)})

# Package parser catches structural editing accidents; not an assertion about engine behavior.
parsed=0
for folder in ['common','events','gui']:
    files={p.relative_to(M).as_posix():p for p in (M/folder).rglob('*') if p.suffix in ['.txt','.gui']}
    files.update({p.relative_to(root).as_posix():p for p in (root/folder).rglob('*') if p.suffix in ['.txt','.gui']})
    for p in files.values():parse(p.read_text('utf-8-sig'));parsed+=1
result={'status':'STATIC_PASS','engine_run':False,'source_root':str(root),'checks':len(checks),'source_files_parsed':parsed,'automatically_enabled_journals':active,'missing_standalone_outcomes':missing,'parent_bound_exceptions':sorted(exceptions),'prose':prose_report,'detail':checks}
(R/'root'/('validation-main.json' if root==M else 'validation-candidate.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='detail'},ensure_ascii=False))
