"""Read-only naval-exit migration audit using real province edges and direct sea strips.

Uses the project's ordered PDX reader and existing binary spline reader.  It does
not change any game file and does not substitute for native route validation.
"""
from pathlib import Path
from collections import defaultdict, Counter
import sys, json, hashlib, argparse
import numpy as np
from PIL import Image

W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
sys.path.insert(0,str(W/'tools'))
from pdx import read, effective_files
from inspect_splnet import read as read_spline
from spline_candidate import encode

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def effective(c,rel): return c/rel if (c/rel).is_file() else G/rel
def definitions(roots):
    out={}; duplicates=[]
    for p in effective_files(roots,'map_data/state_regions'):
        text,tree=read(p)
        for n in tree.children:
            if n.children is None: continue
            if n.key in out: duplicates.append(n.key)
            out[n.key]={'path':str(p),'line':text[:n.start].count('\n')+1,
                       'id':int(n.scalar('id')),'exit':int(n.scalar('naval_exit_id')) if n.get('naval_exit_id') else None,
                       'port':n.scalar('port'),'provinces':[p.upper() for p in n.get('provinces').values()]}
    return out,duplicates
def audit(candidate):
    d,duplicate_keys=definitions([G,candidate]); base,_=definitions([G])
    _,dm=read(effective(candidate,Path('map_data/default.map')))
    seas={int(x[1:],16) for x in dm.get('sea_starts').values()}
    ids=defaultdict(list); sea_by_color=defaultdict(list)
    for key,row in d.items():
        ids[row['id']].append(key)
        row['is_sea']=all(int(c[1:],16) in seas for c in row['provinces'])
        if row['is_sea']:
            for c in row['provinces']: sea_by_color[int(c[1:],16)].append(key)
    imagepath=effective(candidate,Path('map_data/provinces.png'))
    rgb=np.asarray(Image.open(imagepath),dtype=np.uint32)
    pixels=(rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2];del rgb
    h,w=pixels.shape
    # Full shared-pixel edges, including world-map horizontal wrap. Corner-only
    # contact is deliberately not counted as a usable coastal edge.
    pairs=set()
    for a,b in [(pixels[:,:-1],pixels[:,1:]),(pixels[:-1,:],pixels[1:,:]),(pixels[:,-1:],pixels[:,:1])]:
        mask=a!=b; aa=a[mask].astype(np.uint64);bb=b[mask].astype(np.uint64)
        packed=(np.minimum(aa,bb)<<24)|np.maximum(aa,bb)
        pairs.update(int(x) for x in np.unique(packed))
    adjacent=defaultdict(set)
    for x in pairs:
        a=x>>24;b=x&0xFFFFFF;adjacent[a].add(b);adjacent[b].add(a)
    splinepath=effective(candidate,Path('gfx/map/spline_network/spline_network.splnet'))
    raw,t=read_spline(splinepath)
    if encode(t)!=raw: raise ValueError('Spline roundtrip failed; refusing to infer structure')
    tables=[{r[2]['value']:[v['value'] for v in r[5]] for r in t[i]} for i in [8,11,14]]
    anchors,strips,connections=tables
    assigned={x for a in connections.values() for x in a}
    sea_anchors={(1<<23)+row['id']*100:key for key,row in d.items() if row['is_sea']}
    locpath=effective(candidate,Path('gfx/map/map_object_data/generated_map_object_locators_port.txt'))
    _,lt=read(locpath)
    locs={int(n.scalar('id')):[float(x) for x in n.get('position').values()] for n in lt.children[0].get('instances').children}
    def at(x,z):
        xx=int(x)%w; yy=h-1-int(z)
        return f'X{int(pixels[yy,xx]):06X}' if 0<=yy<h else None
    rows=[]
    for key,row in d.items():
        if row['port'] is None and row['exit'] is None: continue
        sid=row['id'];harbor=(1<<23)+sid*100;port=row['port'].upper() if row['port'] else None
        neighbor_colors=sorted(adjacent.get(int(port[1:],16),set())&seas) if port else []
        neighbor_regions=sorted({r for color in neighbor_colors for r in sea_by_color[color]})
        region_sea_colors=set().union(*(adjacent.get(int(c[1:],16),set())&seas for c in row['provinces']))
        region_sea_regions=sorted({r for color in region_sea_colors for r in sea_by_color[color]})
        direct=[]
        for strip,aa in strips.items():
            if strip not in assigned or strip&255!=3 or len(aa)<2 or harbor not in [aa[0],aa[-1]]:continue
            other=aa[-1] if aa[0]==harbor else aa[0]
            direct.append({'strip':strip,'other_anchor':other,'sea_region':sea_anchors.get(other)})
        direct_regions=sorted({x['sea_region'] for x in direct if x['sea_region']})
        target=ids.get(row['exit'],[]) if row['exit'] is not None else []
        issue=[]
        if not port: issue.append('exit_without_port')
        elif port not in row['provinces']: issue.append('port_outside_declared_region')
        if len(target)!=1: issue.append('missing_exit_id' if not target else 'duplicate_exit_id')
        elif not d[target[0]]['is_sea']: issue.append('exit_is_not_sea')
        elif port and target[0] not in neighbor_regions: issue.append('exit_not_adjacent_to_port_province')
        if len(target)==1 and d[target[0]]['is_sea'] and target[0] not in region_sea_regions:issue.append('exit_not_adjacent_to_any_region_province')
        if port and not neighbor_regions:issue.append('port_province_has_no_sea_edge')
        if port and target and target[0] not in direct_regions:issue.append('exit_not_direct_harbor_sea_strip')
        b=base.get(key,{});common=set(neighbor_regions)&set(direct_regions)
        recommendation=None
        # Do not rewrite current vanilla's own declaration/visual discrepancies
        # merely to satisfy a stricter convention that the engine has not proven.
        # Existing-key migration uses current vanilla + the preserved real coast;
        # a conflicting visual strip is an explicit review exception.
        if port and b.get('port','').upper()==port and b.get('exit') is not None and b['exit']!=row['exit']:
            proposed_keys=ids.get(b['exit'],[])
            if len(proposed_keys)==1 and proposed_keys[0] in region_sea_regions:
                proposed=proposed_keys[0]
                recommendation={'action':'set_exit','value':b['exit'],'sea_region':proposed,
                                'vanilla_same_key_same_port_and_exit':True,
                                'port_province_adjacent':proposed in neighbor_regions,
                                'direct_visual_sea_matches':proposed in direct_regions,
                                'requires_visual_exception_review':proposed not in direct_regions}
        elif port and not b and len(common)==1:
            proposed=next(iter(common));newid=d[proposed]['id']
            if row['exit']!=newid:
                recommendation={'action':'set_exit','value':newid,'sea_region':proposed,
                                'vanilla_same_key_same_port_and_exit':False,'requires_custom_region_review':True}
        if not port and b and b.get('port') is None and b.get('exit') is None:
            recommendation={'action':'remove_orphan_exit','value':None,'reason':'candidate has no port; current same-key vanilla has neither port nor exit'}
        lp=locs.get(sid);ha=anchors.get(harbor);pa=anchors.get(sid*100+3)
        rows.append({'region':key,**row,'target_regions':target,'adjacent_sea_colors':[f'X{x:06X}' for x in neighbor_colors],
                     'adjacent_sea_regions':neighbor_regions,'harbor':harbor,'harbor_anchor':ha,
                     'whole_region_adjacent_sea_regions':region_sea_regions,
                     'harbor_pixel':at(*ha) if ha else None,'port_anchor':pa,'port_anchor_pixel':at(*pa) if pa else None,
                     'port_locator':lp,'port_locator_pixel':at(lp[0],lp[2]) if lp else None,
                     'direct_sea_strips':direct,'direct_sea_regions':direct_regions,
                     'vanilla_exit':b.get('exit'),'vanilla_port':b.get('port'),
                     'issues':issue,'recommendation':recommendation})
    return {'candidate':str(candidate),'engine_verified':False,
            'sources':{str(p):sha(p) for p in [imagepath,splinepath,locpath,effective(candidate,Path('map_data/default.map'))]},
            'effective_region_count':len(d),'duplicate_keys':duplicate_keys,'duplicate_ids':{k:v for k,v in ids.items() if len(v)>1},
            'table_duplicate_keys':{name:len(t[pos])-len(tab) for name,pos,tab in zip(['anchors','strips','connections'],[8,11,14],tables)},
            'counts':{'ports_or_exits':len(rows),'issues':dict(Counter(i for r in rows for i in r['issues'])),
                      'recommended_changes':sum(r['recommendation'] is not None for r in rows)},
            'rows':rows,'limits':['Shared pixel edge and direct assigned type-3 strip are static migration evidence, not engine naval reachability.',
                    'Existing native exceptions and unambiguous reference migrations are separated; no country border, population, building or terrain is changed.',
                    'Global sea network reachability alone is deliberately not accepted as correct geographic exit.']}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);x=ap.parse_args()
    if not x.out.resolve().is_relative_to(W.resolve()):raise ValueError('Output outside WORK')
    result=audit(x.candidate.resolve());x.out.parent.mkdir(parents=True,exist_ok=True);x.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps({'out':str(x.out),'counts':result['counts'],'duplicate_ids':result['duplicate_ids'],
                     'review_exceptions':[r['region'] for r in result['rows'] if r['recommendation'] and r['recommendation'].get('requires_visual_exception_review')]},ensure_ascii=False))
