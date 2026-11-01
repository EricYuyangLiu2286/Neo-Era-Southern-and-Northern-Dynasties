"""Read-only global naval-reference and explicit-region transport gate; not engine reachability."""
from pathlib import Path
import argparse,sys,json,hashlib
from collections import defaultdict,deque
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
sys.path.insert(0,str(W/'editor'));sys.path.insert(0,str(W/'tools'))
from model import Project,GAME,read as pdx_read
from inspect_splnet import read
from spline_candidate import encode

def naval_reference_gate(p,candidate):
    """Catch deleted/reused-as-land IDs globally, even when testing a small edited region set.

    Existing sea IDs can still point to the wrong ocean. Pixel/harbor adjacency is
    a separate required gate, not inferred from globally connected sea graphs.
    """
    rel=Path('map_data/default.map')
    f=candidate/rel if (candidate/rel).exists() else GAME/rel
    _,tree=pdx_read(f)
    starts=tree.get('sea_starts')
    if starts is None:raise ValueError('Effective default.map has no sea_starts; cannot classify naval exits.')
    sea_colors={v.upper() for v in starts.values()}
    ids=defaultdict(list)
    for key,(_,node) in p.regions.items():
        ids[node.scalar('id','')].append((key,node))
    rows=[];errors=[]
    for key,(_,node) in p.regions.items():
        value=node.scalar('naval_exit_id')
        if value is None:continue
        targets=ids.get(value,[])
        issue=None
        if not targets:issue='missing effective state_region ID'
        elif len(targets)!=1:issue='ambiguous duplicate effective state_region ID'
        else:
            ps=targets[0][1].get('provinces')
            colors={v.upper() for v in ps.values()} if ps else set()
            if not colors or not colors.issubset(sea_colors):issue='target is not wholly sea_starts water'
        row={'region':key,'naval_exit_id':value,'target_regions':[x[0] for x in targets],'issue':issue}
        rows.append(row)
        if issue:errors.append(f'{key}: naval_exit_id {value}: {issue}')
    return {'default_map':str(f),'default_map_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),
            'scope':'all effective regions with naval_exit_id, not only changed regions',
            'reference_count':len(rows),'rows':rows,'errors':errors,
            'limits':['A valid sea ID may still be geographically wrong; use the global province/port/harbor audit.',
                      'Sea graph reachability does not establish correct direct coastal exit.']}

def check(candidate,regions):
    p=Project(candidate);rel=Path('gfx/map/spline_network/spline_network.splnet');f=candidate/rel if (candidate/rel).exists() else GAME/rel
    raw,t=read(f);refs=naval_reference_gate(p,candidate);errors=list(refs['errors'])
    if encode(t)!=raw:errors.append('binary roundtrip differs: unsupported format')
    tables=[]
    for pos,label in [(8,'anchors'),(11,'strips'),(14,'connections')]:
        seq=t[pos];table={r[2]['value']:[v['value'] for v in r[5]] for r in seq};tables.append(table)
        if len(seq)!=len(table):errors.append('duplicate '+label+' keys')
    A,S,C=tables
    if any(v not in A for vals in S.values() for v in vals):errors.append('strip references missing anchor')
    if any(v not in S for vals in C.values() for v in vals):errors.append('connection references missing strip')
    assigned={q for vals in C.values() for q in vals};g=defaultdict(set);sea=defaultdict(set)
    for key,vals in S.items():
        if key not in assigned or len(vals)<2:continue
        target=sea if (key&255)==3 else g
        target[vals[0]].add(vals[-1]);target[vals[-1]].add(vals[0])
    def reaches(graph,a,b):
        if a not in graph:return False
        seen={a};q=deque([a])
        while q:
            v=q.popleft()
            if v==b:return True
            for z in graph[v]-seen:seen.add(z);q.append(z)
        return False
    L={}
    for h in ['city','farm','mine','wood','port']:
        rel=Path(f'gfx/map/map_object_data/generated_map_object_locators_{h}.txt');loc=candidate/rel if (candidate/rel).exists() else GAME/rel
        _,tree=pdx_read(loc);seq=tree.children[0].get('instances').children
        L[h]={int(n.scalar('id')):n for n in seq}
        if len(seq)!=len(L[h]):errors.append(h+' duplicate locator IDs')
    rows=[]
    for r in regions:
        if r not in p.regions:errors.append(r+': absent state_region');continue
        n=p.regions[r][1];sid=int(n.scalar('id'));ps={v.upper() for v in n.get('provinces').values()};row={'region':r,'id':sid,'checks':{}}
        for h,kind in [('city',0),('farm',1),('mine',2),('wood',4)]+([('port',3)] if n.get('port') else []):
            aid=sid*100+kind
            good=n.get(h) is not None and n.scalar(h).upper() in ps and sid in L[h] and aid in A
            row['checks'][h+'_declaration_locator_anchor']=good
            if not good:errors.append(r+': missing/outside '+h+' declaration, locator or anchor')
            reachable=reaches(g,sid*100,aid)
            row['checks'][h+'_land_connection']=reachable
            if not reachable:errors.append(r+': '+h+' has no strip/connection path to city')
        if n.get('port'):
            harbor=(1<<23)+sid*100;sea_id=int(n.scalar('naval_exit_id','0'));exit_anchor=(1<<23)+sea_id*100
            good=harbor in A and exit_anchor in A and reaches(sea,harbor,exit_anchor)
            row['checks']['harbor_and_declared_exit_searoute']=good
            row['harbor']=harbor;row['sea_anchor']=exit_anchor
            if not good:errors.append(r+': missing harbor or connected sea route to declared exit')
        rows.append(row)
    return {'candidate':str(candidate),'version':p.version,'spline':str(f),'spline_sha256':hashlib.sha256(raw).hexdigest(),'counts':{'anchors':len(A),'strips':len(S),'connections':len(C)},'global_naval_references':refs,'regions':rows,'errors':errors,'static_pass':not errors,'engine_verified':False,'limits':['No geography/hub pixel or full strip terrain sampling here; use candidate geometry audit.','A valid sea ID and a path across the global sea graph do not prove the correct coastal exit.','Graph reachability is not engine NavMesh, military arrival, trade, combat or save/load proof.','Implicit port-to-harbor link is inferred from currently verified node convention; actual engine must instantiate it.','Inherited network exceptions are not rewritten.']}
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--candidate',type=Path,required=True);a.add_argument('--regions',nargs='+',required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args()
    out=x.out.resolve()
    if not out.is_relative_to(W.resolve()):raise ValueError('Reports must remain inside WORK')
    result=check(x.candidate.resolve(),x.regions);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps({'report':str(out),'static_pass':result['static_pass'],'errors':result['errors']},ensure_ascii=False));return 0 if result['static_pass'] else 2
if __name__=='__main__':raise SystemExit(main())
