from pathlib import Path
import sys,json,hashlib,collections
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read,effective_files,basekey
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
O=Path(__file__).parent
hashes={}
def src(p,t,n=None):
    k=p.as_posix(); hashes[k]=hashlib.sha256(p.read_bytes()).hexdigest()
    return {'path':k,'line':t.count('\n',0,n.start)+1 if n else 1,'end_line':t.count('\n',0,n.end)+1 if n else len(t.splitlines())}
def hist(folder):
    for p in effective_files([G,M],'common/history/'+folder):
        t,r=read(p)
        for g in r.children:
            for n in g.children or []: yield p,t,n
def defs(folder):
    out={}
    for p in effective_files([G,M],'common/'+folder):
        t,r=read(p)
        for n in r.children:
            out[basekey(n.key)]=(p,t,n)
    return out
cultures=defs('cultures'); countries=defs('country_definitions')
t,r=read(M/'common/history/pops/10_india.txt')
india={n.key[2:] for g in r.children for n in g.children}
allstates=list(hist('states'))
india.update(n.key[2:] for p,t,n in allstates if any(c.scalar('country')=='c:MUG' for c in n.all('create_state')))
states=[]
for p,t,n in allstates:
    if n.key[2:] not in india: continue
    for c in n.all('create_state'):
        states.append({'region':n.key[2:],'tag':c.scalar('country').removeprefix('c:'),'type':c.scalar('state_type','incorporated_default'),'provinces':c.get('owned_provinces').values(),'homelands':[x.value for x in n.all('add_homeland')],'claims':[x.value for x in n.all('add_claim')],'source':src(p,t,c)})
owners={(s['region'],s['tag']) for s in states}; tags={x[1] for x in owners}
pops=[]; buildings=[]; formations=[]; history={}; definitions=[]; resources=[]
for p,t,n in hist('pops'):
    if n.key[2:] not in india: continue
    for rs in n.children or []:
        for c in rs.all('create_pop'):
            culture=c.scalar('culture'); cp,ct,cn=cultures[culture]
            religion=c.scalar('religion',cn.scalar('religion'))
            pops.append({'region':n.key[2:],'tag':rs.key.removeprefix('region_state:'),'culture':culture,'religion':religion,'explicit_religion':c.scalar('religion'),'size':int(c.scalar('size','0')),'pop_type':c.scalar('pop_type'),'has_owner':(n.key[2:],rs.key.removeprefix('region_state:')) in owners,'source':src(p,t,c),'culture_source':src(cp,ct,cn)})
for p,t,n in hist('buildings'):
    if n.key[2:] not in india: continue
    for rs in n.children or []:
        for c in rs.all('create_building'):
            own=[int(x.value) for o in c.all('add_ownership') for x in o.walk() if x.key=='levels']
            buildings.append({'region':n.key[2:],'tag':rs.key.removeprefix('region_state:'),'type':c.scalar('building'),'levels':int(c.scalar('level')) if c.scalar('level') else sum(own),'pms':c.get('activate_production_methods').values() if c.get('activate_production_methods') else [],'has_owner':(n.key[2:],rs.key.removeprefix('region_state:')) in owners,'source':src(p,t,c)})
for tag in sorted(tags):
    if tag in countries:
        p,t,n=countries[tag]; definitions.append({'tag':tag,'source':src(p,t,n),'script':t[n.start:n.end]})
for folder in ['countries','characters','population','military_formations','diplomacy','treaties','power_blocs']:
    history[folder]=[]
    for p,t,n in hist(folder):
        if (n.key or '').removeprefix('c:') in tags or (folder in {'diplomacy','treaties','power_blocs'} and any(x.value in {'c:MUG','c:TRA','c:MYS'} for x in n.walk())):
            history[folder].append({'tag':n.key,'source':src(p,t,n),'script':t[n.start:n.end]})
for p in effective_files([G,M],'map_data/state_regions'):
    t,r=read(p)
    for n in r.children:
        if n.key in india:
            resources.append({'region':n.key,'source':src(p,t,n),'arable_land':n.scalar('arable_land'),'arable_resources':n.get('arable_resources').values() if n.get('arable_resources') else [],'capped_resources':{c.key:c.value for c in n.get('capped_resources').children} if n.get('capped_resources') else {},'resource_blocks':[t[c.start:c.end] for c in n.all('resource')],'traits':n.get('traits').values() if n.get('traits') else []})
def aggregate(rows,keys,val):
    agg=collections.Counter()
    for row in rows:
        if row['has_owner']: agg[tuple(row.get(k) for k in keys)]+=row[val]
    return [{**dict(zip(keys,k)),val:v} for k,v in sorted(agg.items(),key=lambda kv:str(kv[0]))]
result={'method':'Ordered pdx parser preserving repeated blocks. Effective files merge GAME then MOD by case-insensitive relative path. This audits static scripts, not engine outcomes. Missing pop religion resolved from effective culture default. Totals exclude orphan region_state without effective state owner. Building level is explicit level else sum(add_ownership levels). Country definition key resolution is source-index heuristic; absence of duplicate MUG verified separately.','version':'1.13.11','build':'24799966','baseline_git':'717c901','regions':sorted(india),'states':states,'pops':pops,'buildings':buildings,'resources':resources,'definitions':definitions,'history':history,'population_by_owner':aggregate(pops,['tag'],'size'),'population_by_state':aggregate(pops,['tag','region'],'size'),'population_by_culture':aggregate(pops,['tag','culture'],'size'),'population_by_religion':aggregate(pops,['tag','religion'],'size'),'population_by_pop_type':aggregate(pops,['tag','pop_type'],'size'),'buildings_by_type':aggregate(buildings,['tag','type'],'levels'),'source_sha256':hashes}
for folder in ['common/journal_entries','common/scripted_buttons','common/scripted_triggers','common/scripted_effects','common/on_actions','events','localization/simp_chinese/replace']:
    for p in (M/folder).rglob('*'):
        if p.suffix in {'.txt','.yml'} and any(s in p.read_text(encoding='utf-8-sig') for s in ['MUG','mug','莫卧儿','印度','迈索尔']): src(p,p.read_text(encoding='utf-8-sig'))
(O/'current-mod-india-data.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['population_by_owner','population_by_state','population_by_culture','population_by_religion','buildings_by_type']},ensure_ascii=False,indent=2))
print('ORPHAN POPS',[(x['region'],x['tag'],x['size']) for x in pops if not x['has_owner']])
