from pathlib import Path
import sys,json,hashlib,collections
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read,effective_files
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
O=Path(__file__).parent
pop=collections.Counter(); buildings=collections.Counter(); sources={}; military=[]
for folder in ['pops','buildings','military_formations']:
    for p in effective_files([G,M],'common/history/'+folder):
        t,r=read(p)
        for group in r.children:
            for state in group.children or []:
                if folder=='military_formations':
                    if state.key=='c:MUG': military.append({'path':p.as_posix(),'line':t.count('\n',0,state.start)+1,'script':t[state.start:state.end]})
                    continue
                for rs in state.children or []:
                    if rs.key!='region_state:MUG': continue
                    sources[p.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
                    for n in rs.all('create_pop'): pop[state.key]+=int(n.scalar('size','0'))
                    for n in rs.all('create_building'):
                        lvl=n.scalar('level')
                        count=int(lvl) if lvl else sum(int(x.value) for a in n.all('add_ownership') for x in a.walk() if x.key=='levels')
                        buildings[n.scalar('building')]+=count
result={'method':'Global GAME+MOD effective history scan, not restricted to India file or preset geography','MUG_total':sum(pop.values()),'MUG_population_regions':dict(pop),'MUG_building_types':dict(buildings),'building_barrack':buildings['building_barrack'],'building_barracks':buildings['building_barracks'],'military':military,'sources_sha256':sources}
(O/'root-plan-source-check-data.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
