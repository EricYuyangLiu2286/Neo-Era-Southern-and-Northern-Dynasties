"""Experimental, bounded land-network repair in a NEW workbench export.

Preserves typed opaque Jomini identifiers; requires a byte-exact source roundtrip.
Existing records are retained. New routes use current province masks and heightmap.
This is a candidate generator, never an engine-certification tool.
"""
from pathlib import Path
from datetime import datetime, timezone
import sys, json, struct, hashlib, shutil, math, heapq
import numpy as np
from PIL import Image, ImageDraw
from inspect_splnet import read

W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
sys.path.insert(0,str(W/'editor'))
from model import Project, GAME, MOD
O=W/'research/20261031/map-design'
SOURCE=W/'map-projects/spline-authoring-20261031T035657Z/mod'
REL=Path('gfx/map/spline_network/spline_network.splnet')

def encode(tree):
    chunks=[]
    def item(x):
        if isinstance(x,list):
            chunks.append(struct.pack('<H',3))
            for v in x:item(v)
            chunks.append(struct.pack('<H',4))
        elif x=='=':chunks.append(struct.pack('<H',1))
        elif 'id' in x:chunks.append(struct.pack('<H',int(x['id'],16)))
        else:
            n=x['type'];v=x['value'];chunks.append(struct.pack('<H',n))
            if n in (15,23):
                b=v.encode('utf-8');chunks.append(struct.pack('<H',len(b))+b)
            else:chunks.append(struct.pack('<'+{12:'i',13:'f',14:'?',20:'I',359:'d',668:'Q',791:'q'}[n],v))
    for x in tree:item(x)
    return b''.join(chunks)

def val(n,x):return {'type':n,'value':x}
def ident(n):return {'id':hex(n)}
def rec(keytype,key,field,values):return [ident(11),'=',val(keytype,key),ident(field),'=',values]
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    b,t=read(SOURCE/REL)
    assert encode(t)==b,'Primitive/schema roundtrip differs: do not write.'
    assert [t[i]['id'] for i in (0,3,6,9,12)]==['0xee','0x45a','0x5f4','0x5f5','0x5f6']
    assert t[2]['value']==4
    anchors={r[2]['value']:tuple(v['value'] for v in r[5]) for r in t[8]}
    strips={r[2]['value']:[v['value'] for v in r[5]] for r in t[11]}
    connections={r[2]['value']:[v['value'] for v in r[5]] for r in t[14]}
    original_counts=[len(anchors),len(strips),len(connections)]
    assert [x['value'] for x in t[5]]==original_counts
    formula_bad=[]
    for k,ss in connections.items():
        for si in ss:
            aa,bb=sorted((strips[si][0],strips[si][-1]))
            if (bb<<35)+(aa<<6)+(si&255)!=k:formula_bad.append([k,si])
    # A few source connections have intermediate-point endpoints. Preserve them verbatim.
    assert len(formula_bad)==4,formula_bad
    p=Project(SOURCE);ob=json.loads((O/'transport-obligations.json').read_text('utf-8'))
    affected=set(ob)
    nr={int(n.scalar('id')):r for r,(_,n) in p.regions.items()}
    rid={r:int(n.scalar('id')) for r,(_,n) in p.regions.items()}
    hubids={r:[rid[r]*100+i for i in (0,1,2,4) if rid[r]*100+i in anchors] for r in p.regions}
    links={tuple(sorted((v[0],v[-1]))) for k,v in strips.items() if k&255 in (0,1,4,5,6)}
    rgb=np.asarray(Image.open(GAME/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    pixels=(rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2];del rgb
    height=np.asarray(Image.open(GAME/'map_data/heightmap.png').resize((8192,3616)),dtype=np.float32)
    height/=65535
    masks={}
    def mask(r):
        if r not in masks:
            n=p.regions[r][1];vs=set(n.get('provinces').values())
            if n.get('impassable'):vs-=set(n.get('impassable').values())
            masks[r]=np.isin(pixels,[int(v[1:],16) for v in vs])
        return masks[r]
    def pixel(a):
        x,z=anchors[a];return int(x),3615-int(z)
    def path(a,bb,rs):
        allowed=mask(rs[0]).copy()
        for r in rs[1:]:allowed|=mask(r)
        sx,sy=pixel(a);ex,ey=pixel(bb)
        assert allowed[sy,sx] and allowed[ey,ex],(a,bb,rs,'hub outside allowed mask')
        ys,xs=np.where(allowed);x0,x1=int(xs.min()),int(xs.max())+1;y0,y1=int(ys.min()),int(ys.max())+1
        m=allowed[y0:y1,x0:x1];h=height[y0:y1,x0:x1];hh,ww=m.shape
        sx-=x0;ex-=x0;sy-=y0;ey-=y0
        start=sy*ww+sx;goal=ey*ww+ex
        g={start:0.0};prev={};q=[(math.hypot(ex-sx,ey-sy),0,start)]
        while q:
            _,cost,i=heapq.heappop(q)
            if cost!=g[i]:continue
            if i==goal:break
            y,x=divmod(i,ww)
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)):
                xx=x+dx;yy=y+dy
                if not (0<=xx<ww and 0<=yy<hh and m[yy,xx]):continue
                if dx and dy and not (m[y,xx] and m[yy,x]):continue
                # Prefer low and gentle terrain. This is a routing heuristic, not historical roads.
                extra=math.hypot(dx,dy)*(1+float(h[yy,xx])*2)+abs(float(h[yy,xx]-h[y,x]))*80
                nc=cost+extra;j=yy*ww+xx
                if nc<g.get(j,float('inf')):
                    g[j]=nc;prev[j]=i;heapq.heappush(q,(nc+math.hypot(ex-xx,ey-yy),nc,j))
        else:raise ValueError(('No passable raster route',a,bb,rs))
        result=[goal]
        while result[-1]!=start:result.append(prev[result[-1]])
        result.reverse()
        xy=[(i%ww+x0,i//ww+y0) for i in result]
        # Every pixel retained: no straight simplification across sea or impassable provinces.
        return xy,g[goal]
    todo=[]
    # Connect every state's own hub components, without replacing existing good edges.
    for r in sorted(affected):
        parent={a:a for a in hubids[r]}
        def root(a):
            while parent[a]!=a:a=parent[a]
            return a
        for a,bb in links:
            if a in parent and bb in parent:parent[root(a)]=root(bb)
        while len({root(a) for a in parent})>1:
            candidates=sorted((math.dist(anchors[a],anchors[bb]),a,bb) for a in parent for bb in parent if a<bb and root(a)!=root(bb))
            _,a,bb=candidates[0];xy,cost=path(a,bb,[r]);todo.append((a,bb,[r],xy,cost));links.add((a,bb));parent[root(a)]=root(bb)
    for r in sorted(affected):
        for other in sorted(ob[r]['land_neighbors']):
            if any((nr.get(a//100)==r and nr.get(bb//100)==other) or (nr.get(a//100)==other and nr.get(bb//100)==r) for a,bb in links):continue
            candidates=sorted((math.dist(anchors[a],anchors[bb]),a,bb) for a in hubids[r] for bb in hubids[other])
            _,a,bb=candidates[0];a,bb=sorted((a,bb));xy,cost=path(a,bb,[r,other]);todo.append((a,bb,[r,other],xy,cost));links.add((a,bb))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    export=W/'exports'/('geography-routed-'+stamp)
    nextpoint=max(k&0xfffffff for k in anchors if k>>28==1)+1
    nextstrip=max(k>>8 for k in strips)+1
    newroutes=[]
    for a,bb,rs,xy,cost in todo:
        ids=[a]
        for x,y in xy[1:-1]:
            index=(1<<28)+nextpoint;nextpoint+=1
            pos=(x+.5,3615-y+.5)
            t[8].append(rec(20,index,76,[val(13,v) for v in pos]));anchors[index]=pos;ids.append(index)
        ids.append(bb)
        # Railroad route type matches the existing inland Chinese network; the engine selects display style.
        kind=1;si=(nextstrip<<8)+kind;nextstrip+=1
        t[11].append(rec(668,si,0x5f7,[val(20,v) for v in ids]));strips[si]=ids
        ck=(bb<<35)+(a<<6)+kind;assert ck not in connections
        t[14].append(rec(668,ck,0x5f5,[val(668,si)]));connections[ck]=[si]
        newroutes.append({'strip':si,'endpoints':[a,bb],'regions':rs,'pixels':xy,'terrain_cost':cost})
    for i,n in enumerate([len(anchors),len(strips),len(connections)]):t[5][i]['value']=n
    result=encode(t)
    shutil.copytree(SOURCE,export)
    (export/REL).write_bytes(result)
    # Sync the already backed-up, as-yet cold-unverified event preview fix from the main MOD.
    shutil.copy2(MOD/'events/flavorCNE_ce.txt',export/'events/flavorCNE_ce.txt')
    b2,t2=read(export/REL);assert b2==result and encode(t2)==result
    report={'candidate':str(export),'source':str(SOURCE),'source_sha256':sha(b),'result_sha256':sha(result),'byte_exact_source_roundtrip':True,'preserved_source_formula_exceptions':formula_bad,'counts_before':original_counts,'counts_after':[len(anchors),len(strips),len(connections)],'new_routes':newroutes,'engine_status':'NOT RUN','routing':'1 pixel A* on passable province masks; height/gradient penalty; no historical road claim'}
    (O/'spline-routed-candidate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
    # Diagnostic preview on actual elevation; plotting is not game media editing.
    points=[pt for x in newroutes for pt in x['pixels']];xs=[x for x,y in points];ys=[y for x,y in points]
    x0=max(0,min(xs)-20);y0=max(0,min(ys)-20);x1=max(xs)+21;y1=max(ys)+21
    img=Image.fromarray((height[y0:y1,x0:x1]*255).astype(np.uint8)).convert('RGB').resize(((x1-x0)*4,(y1-y0)*4))
    d=ImageDraw.Draw(img)
    for route in newroutes:
        line=[((x-x0)*4,(y-y0)*4) for x,y in route['pixels']];d.line(line,fill='#f6c846',width=2)
        for a in route['endpoints']:
            x,y=pixel(a);x=(x-x0)*4;y=(y-y0)*4;d.ellipse((x-4,y-4,x+4,y+4),fill='#ff5b5b');d.text((x+5,y),str(a),fill='white')
    img.save(O/'new-transport-routes.png')
    print(json.dumps({k:v for k,v in report.items() if k!='new_routes'},ensure_ascii=False,indent=2));print('Added routes:',len(newroutes))

if __name__=='__main__':main()
