from pathlib import Path
import sys, json, hashlib, collections
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read, effective_files, basekey
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
OUT=Path(__file__).parent
JP={'STATE_HOKKAIDO','STATE_TOHOKU','STATE_KANTO','STATE_TOKAI','STATE_HOKUSHINETSU','STATE_KANSAI','STATE_KYOTO','STATE_KYUSHU','STATE_CHUGOKU','STATE_SHIKOKU','STATE_BUSAN','STATE_YANGHO','STATE_SEOUL','STATE_SARIWON','STATE_PYONGYANG','STATE_SAKHALIN','STATE_RYUKYU_ISLANDS'}
sources={}
def src(p,t,n=None):
    p=str(p).replace('\\','/')
    sources[p]=hashlib.sha256(Path(p).read_bytes()).hexdigest()
    return {'path':p,'line': t.count('\n',0,n.start)+1 if n else 1, 'end_line': t.count('\n',0,n.end)+1 if n else len(t.splitlines())}
def compact(n):
    return {'key':n.key,'value':n.value,'children':[compact(c) for c in n.children or []]} if n.children is not None else {'key':n.key,'value':n.value}
def hist(relative):
    for p in effective_files([G,M],relative):
        t,r=read(p)
        for group in r.children:
            for n in group.children or []: yield p,t,n
states=[]; pops=[]; buildings=[]; formations=[]; chars=[]
for p,t,n in hist('common/history/states'):
    if n.key and n.key.removeprefix('s:') in JP:
        for c in n.all('create_state'):
            states.append({'region':n.key[2:],'tag':c.scalar('country'),'type':c.scalar('state_type','incorporated_default'),'provinces':c.get('owned_provinces').values() if c.get('owned_provinces') else [],'homelands':[x.value for x in n.all('add_homeland')],'source':src(p,t,c)})
for p,t,n in hist('common/history/pops'):
    if n.key and n.key.removeprefix('s:') in JP:
        for rs in n.children or []:
            for c in rs.all('create_pop'):
                pops.append({'region':n.key[2:],'tag':rs.key.removeprefix('region_state:'),'culture':c.scalar('culture'),'religion':c.scalar('religion'),'size':int(c.scalar('size','0')),'source':src(p,t,c)})
for p,t,n in hist('common/history/buildings'):
    if n.key and n.key.removeprefix('s:') in JP:
        for rs in n.children or []:
            for c in rs.all('create_building'):
                own=[int(x.value) for o in c.all('add_ownership') for x in o.walk() if x.key=='levels']
                buildings.append({'region':n.key[2:],'tag':rs.key.removeprefix('region_state:'),'type':c.scalar('building'),'levels':int(c.scalar('level')) if c.scalar('level') else sum(own),'explicit_level':c.scalar('level'),'ownership_level_parts':own,'pms':c.get('activate_production_methods').values() if c.get('activate_production_methods') else [],'source':src(p,t,c)})
for p,t,n in hist('common/history/military_formations'):
    if n.key in {'c:JAP','c:JTK','c:JIM','c:KOR'}:
        formations.append({'tag':n.key,'source':src(p,t,n),'script':t[n.start:n.end]})
for p,t,n in hist('common/history/characters'):
    if n.key in {'c:JAP','c:JTK','c:JIM','c:KOR'}:
        chars.append({'tag':n.key,'source':src(p,t,n),'templates':[x.scalar('template') for x in n.walk() if x.key=='create_character'],'script':t[n.start:n.end]})
pop_sums=collections.defaultdict(int); culture_sums=collections.defaultdict(int); b_sums=collections.defaultdict(int)
for row in pops:
    pop_sums[(row['tag'],row['region'])]+=row['size']; culture_sums[(row['tag'],row['culture'])]+=row['size']
for row in buildings: b_sums[(row['tag'],row['type'])]+=row['levels']
symbols=[]
for folder in ['common/journal_entries','events','common/scripted_effects','common/scripted_triggers','common/on_actions','common/scripted_buttons','common/character_templates','common/dynamic_country_names','common/government_types','common/static_modifiers']:
    for p in effective_files([G,M],folder):
        if p.is_relative_to(M):
            t,r=read(p)
            for n in r.children:
                if n.key and ('jap' in n.key.lower() or 'ryukyu' in n.key.lower() or n.key=='ce_usm_cw_japanese_interest'):
                    symbols.append({'symbol':n.key,'source':src(p,t,n),'trigger':t[n.get('trigger').start:n.get('trigger').end] if n.get('trigger') else None,'possible':t[n.get('possible').start:n.get('possible').end] if n.get('possible') else None,'calls':[x.scalar('id') for x in n.walk() if x.key=='trigger_event']})
result={'method':'Ordered pdx parser, repeated keys preserved; GAME then MOD same-relative-path overrides. Population is scripted persons, buildings counted by explicit level else sum(add_ownership levels); no SOL/GDP estimates or engine claims.', 'game_version':'1.13.11','game_build':'24799966','states':states,'pops':pops,'buildings':buildings,'formations':formations,'characters':chars,'population_by_state':[{'tag':k[0],'region':k[1],'population':v} for k,v in sorted(pop_sums.items())],'population_by_culture':[{'tag':k[0],'culture':k[1],'population':v} for k,v in sorted(culture_sums.items())],'buildings_by_type':[{'tag':k[0],'type':k[1],'levels':v} for k,v in sorted(b_sums.items())],'symbols':symbols,'source_sha256':sources}
event_ids={f'flavorJAP_ce.{i}' for i in [1,2,3]}|{f'nesnd_japan.{i}' for i in range(1,6)}|{'nesnd_japan_recovery.1','nesnd_crisis.41','usm_civilwar.23'}|{f'usm_civilwar.{i}' for i in range(14,20)}
references=[]
for folder in ['common','events']:
    for p in effective_files([G,M],folder):
        if not any(e in p.read_text(encoding='utf-8-sig') for e in event_ids): continue
        t,r=read(p)
        for top in r.children or []:
            for n in top.walk():
                if n.value in event_ids or (n.key in event_ids and n is top):
                    references.append({'event':n.value or n.key,'owner':top.key,'kind':'definition' if n is top and n.key in event_ids else 'reference','source':src(p,t,n)})
result['event_references']=references
extra=['common/country_definitions/ce_countries.txt','common/country_definitions/nesnd_japan.txt','common/history/countries/jap - japan.txt','common/history/population/jap - japan.txt','common/history/diplomacy/ce_subject_relationships.txt','common/history/diplomacy/ce_truces.txt','common/history/diplomacy/00_relations.txt','common/laws/ce_trade_policy.txt','common/scripted_effects/nesnd_south_political_ai.txt','common/scripted_effects/nesnd_south_accords.txt','common/scripted_effects/nesnd_south_peace.txt','common/scripted_effects/nesnd_crisis_effects.txt','common/scripted_triggers/nesnd_south_politics.txt','common/on_actions/nesnd_south_politics.txt','events/nesnd_south_accords.txt','events/flavorUSM_ce.txt','localization/simp_chinese/replace/nesnd_japan_l_simp_chinese.yml','localization/simp_chinese/replace/zz_nesnd_crisis_l_simp_chinese.yml','localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml','common/war_goal_types/nesnd_japan.txt','common/diplomatic_plays/nesnd_japan.txt','common/script_values/nesnd_japan.txt','common/static_modifiers/nesnd_japan.txt','.metadata/metadata.json']
for rel in extra:
    p=M/rel; src(p,p.read_text(encoding='utf-8-sig'))
B=M.parent.parent/'nesnd-workbench/backups/pre-update-20261030T233944Z/mod'
comparison=[]
for rel,newrel in [('events/flavorJAP_ce.txt','events/flavorJAP_ce.txt'),('common/character_templates/ce_JAP.txt','common/character_templates/zz_ce_JAP.txt'),('common/scripted_effects/ce_japan_gov_effects.txt','common/scripted_effects/ce_japan_gov_effects.txt'),('common/journal_entries/ce_usm_the_last_days_of_ming.txt','common/journal_entries/ce_usm_the_last_days_of_ming.txt'),('common/history/countries/jap - japan.txt','common/history/countries/jap - japan.txt')]:
    p=B/rel; q=M/newrel
    if p.exists():
        comparison.append({'original':src(p,p.read_text(encoding='utf-8-sig')),'current':src(q,q.read_text(encoding='utf-8-sig')),'byte_identical':p.read_bytes()==q.read_bytes()})
result['original_author_backup_comparison']=comparison
(OUT/'current-mod-japan-data.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['population_by_state','population_by_culture','buildings_by_type','formations']},ensure_ascii=False,indent=2))
