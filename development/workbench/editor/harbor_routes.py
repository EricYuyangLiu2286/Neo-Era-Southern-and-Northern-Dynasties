"""Bounded new-port sea-node authoring during isolated scenario export.
Land routes and moved existing ports still require separate transport review.
"""
from pathlib import Path
import sys,math,heapq,copy
import numpy as np
from PIL import Image
from model import Project,read as pdx_read,GAME,WORK
sys.path.insert(0,str(WORK/'tools'))
from inspect_splnet import read
from spline_candidate import encode,rec,val
REL=Path('gfx/map/spline_network/spline_network.splnet')
def astar(start,end,allowed):
 ys,xs=np.where(allowed);x0,x1=int(xs.min()),int(xs.max())+1;y0,y1=int(ys.min()),int(ys.max())+1
 mask=allowed[y0:y1,x0:x1];h,w=mask.shape
 sx,sy=start[0]-x0,start[1]-y0;ex,ey=end[0]-x0,end[1]-y0
 assert mask[sy,sx] and mask[ey,ex]
 first=sy*w+sx;last=ey*w+ex;cost={first:0};prev={};q=[(math.hypot(ex-sx,ey-sy),0,first)]
 while q:
  _,c,i=heapq.heappop(q)
  if cost[i]!=c:continue
  if i==last:break
  y,x=divmod(i,w)
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
   xx,yy=x+dx,y+dy
   if not(0<=xx<w and 0<=yy<h and mask[yy,xx]):continue
   if dx and dy and not(mask[y,xx] and mask[yy,x]):continue
   nc=c+math.hypot(dx,dy);j=yy*w+xx
   if nc<cost.get(j,float('inf')):
    cost[j]=nc;prev[j]=i;heapq.heappush(q,(nc+math.hypot(ex-xx,ey-yy),nc,j))
 else:raise ValueError('No sea-only path in declared naval exit')
 path=[last]
 while path[-1]!=first:path.append(prev[path[-1]])
 return [(i%w+x0,i//w+y0) for i in path[::-1]]

def ensure_new_port_routes(stage,affected):
    stage=Path(stage).resolve()
    if not stage.is_relative_to((WORK/'projects').resolve()):
        raise ValueError('Port routes may only be authored in isolated export staging.')
    p=Project(stage);affected=set(affected)
    source=stage/REL if (stage/REL).exists() else GAME/REL
    raw,t=read(source)
    if encode(t)!=raw:raise ValueError('Unsupported spline binary; native editor required.')
    old=copy.deepcopy(t)
    A={r[2]['value']:[v['value'] for v in r[5]] for r in t[8]}
    SS={r[2]['value']:[v['value'] for v in r[5]] for r in t[11]}
    C={r[2]['value']:[v['value'] for v in r[5]] for r in t[14]}
    todo=[]
    for region in sorted(affected):
        if region not in p.regions:continue
        n=p.regions[region][1]
        if n.get('port') and (1<<23)+int(n.scalar('id'))*100 not in A:todo.append(region)
    if not todo:return {'new_ports':[],'changed':False,'engine_verified':False}
    locrel=Path('gfx/map/map_object_data/generated_map_object_locators_port.txt')
    _,loc=pdx_read(stage/locrel if (stage/locrel).exists() else GAME/locrel)
    L={int(q.scalar('id')):q for q in loc.children[0].get('instances').children}
    raster=stage/'map_data/provinces.png'
    if not raster.exists():raster=GAME/'map_data/provinces.png'
    img=np.asarray(Image.open(raster).convert('RGB'),dtype=np.uint32)
    pix=(img[:,:,0]<<16)|(img[:,:,1]<<8)|img[:,:,2]
    height=pix.shape[0];nr={int(n.scalar('id')):r for r,(_,n) in p.regions.items()}
    nextpoint=max(a&0xfffffff for a in A if a>>28==1)+1
    nextstrip=max(s>>8 for s in SS)+1;routes=[]
    for region in todo:
        n=p.regions[region][1];sid=int(n.scalar('id'));sea=int(n.scalar('naval_exit_id'))
        port=sid*100+3;harbor=(1<<23)+sid*100;sea_anchor=(1<<23)+sea*100
        if sid not in L or sea_anchor not in A:raise ValueError(region+': choose a valid port location and existing sea region.')
        pos=[float(q) for q in L[sid].get('position').values()];land=[pos[0],pos[2]]
        x,y=int(land[0]),height-1-int(land[1])
        if f'X{pix[y,x]:06X}'!=n.scalar('port').upper():raise ValueError(region+': port marker is outside its declared province.')
        if port in A and math.dist(A[port],land)>.02:
            raise ValueError(region+': existing land port anchor moved; rebuild its land routes before export.')
        allowed=np.isin(pix,[int(v[1:],16) for v in p.regions[nr[sea]][1].get('provinces').values()])
        adj=[(x+dx,y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=x+dx<pix.shape[1] and 0<=y+dy<height and allowed[y+dy,x+dx]]
        if not adj:raise ValueError(region+': port marker must touch the selected sea region; choose a coastal province and update its marker.')
        tx,tz=A[sea_anchor];end=(int(tx),height-1-int(tz));start=min(adj,key=lambda pt:math.dist(pt,end))
        xy=astar(start,end,allowed);hpos=[start[0]+.5,height-1-start[1]+.5]
        if port not in A:
            t[8].append(rec(20,port,76,[val(13,v) for v in land]));A[port]=land
        t[8].append(rec(20,harbor,76,[val(13,v) for v in hpos]));A[harbor]=hpos
        ids=[harbor]
        for xx,yy in xy[1:-1]:
            aid=(1<<28)+nextpoint;nextpoint+=1;pp=[xx+.5,height-1-yy+.5]
            assert aid not in A
            t[8].append(rec(20,aid,76,[val(13,v) for v in pp]));A[aid]=pp;ids.append(aid)
        ids.append(sea_anchor);strip=(nextstrip<<8)+3;nextstrip+=1
        lo,hi=sorted([harbor,sea_anchor]);connection=(hi<<35)+(lo<<6)+3
        assert strip not in SS and connection not in C
        t[11].append(rec(668,strip,0x5f7,[val(20,v) for v in ids]));SS[strip]=ids
        t[14].append(rec(668,connection,0x5f5,[val(668,strip)]));C[connection]=[strip]
        routes.append({'region':region,'port':port,'harbor':harbor,'sea_anchor':sea_anchor,'strip':strip,'connection':connection,'pixels':xy})
    for i,num in enumerate([len(A),len(SS),len(C)]):t[5][i]['value']=num
    for i in [8,11,14]:assert t[i][:len(old[i])]==old[i]
    assert len(A)==len(t[8]) and len(SS)==len(t[11]) and len(C)==len(t[14])
    result=encode(t);target=stage/REL;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(result)
    check,tt=read(target);assert check==result and encode(tt)==result
    return {'new_ports':routes,'changed':True,'old_records_preserved':True,'engine_verified':False,'land_routes_review_required':True}
