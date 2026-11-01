"""Local historical-map editor. Ordered source trees; candidate exports only."""
from __future__ import annotations
import sys, copy, json, hashlib, shutil, re, uuid
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
sys.path.insert(0, r'C:\Users\Eric Liu\.codex\skills\nesnd-victoria3\scripts')
from pdx import Node, read, emit, effective_files, basekey, replace_spans, parse
from catalog import GAME, MOD, WORK, version

def scalar(k,v): return Node(k,str(v),start=-1)
def block(k,children): return Node(k,children=children,start=-1)
def values(k,items): return block(k,[scalar(None,x) for x in items])
def setval(n,k,v):
    q=n.get(k)
    if q:q.value=str(v)
    else:n.children.append(scalar(k,v))
def setlist(n,k,items):
    q=n.get(k)
    if q:q.children=[scalar(None,v) for v in items]
    else:n.children.append(values(k,items))
def clone(n):
    q=copy.deepcopy(n)
    for c in q.walk(): c.start=-1
    return q
def tree_manifest(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def integer(value, minimum=0):
    if isinstance(value,bool) or not re.fullmatch(r'[0-9]+',str(value)):
        raise ValueError('Use an integer, not a fraction or expression.')
    value=int(value)
    if value<minimum:raise ValueError(f'Value must be at least {minimum}.')
    return value

def levels(b):
    owned=sum(int(float(q.value)) for q in b.walk() if q.key=='levels')
    return owned or int(float(b.scalar('level','0')))

class Document:
    def __init__(self,path,rel):
        self.path=path;self.rel=rel;self.text,self.tree=read(path)
        self.original={id(n):copy.copy(n) for n in self.tree.walk()}
        for n in self.tree.walk():
            if n.children is not None:self.original[id(n)].children=list(n.children)
        self.sha=hashlib.sha256(path.read_bytes()).hexdigest()
    def render_node(self,n):
        o=self.original.get(id(n))
        if o is None:return emit(n)
        edits=[]
        if n.key!=o.key:
            edits.append((o.start,o.start+len(o.key),n.key))
        if n.children is None:
            if n.value!=o.value:edits.append((o.vstart,o.vend,n.value))
        elif o.children is not None:
            oldids={id(c) for c in o.children};newids={id(c) for c in n.children}
            for c in o.children:
                if id(c) not in newids:edits.append((c.start,c.end,''))
                else:
                    rendered=self.render_node(c)
                    if rendered!=self.text[c.start:c.end]:edits.append((c.start,c.end,rendered))
            added=[c for c in n.children if id(c) not in oldids]
            if added:
                at=o.end-1 if n is not self.tree else o.end
                edits.append((at,at,'\n'+'\n'.join(emit(c,1 if n is not self.tree else 0) for c in added)+'\n'))
        return replace_spans(self.text[o.start:o.end],[(a-o.start,b-o.start,v) for a,b,v in edits])
    def render(self):return self.render_node(self.tree)

class Project:
    def __init__(self,mod=MOD):
        self.mod=Path(mod).resolve()
        if self.mod!=MOD.resolve() and not self.mod.is_relative_to(WORK.resolve()):raise ValueError('Only the main MOD or a WORK copy can be an editor source; game/workshop/reference folders are read-only references, not export templates.')
        if not self.mod.is_dir() or not ((self.mod/'.metadata/metadata.json').exists() or (self.mod/'descriptor.mod').exists()):
            raise ValueError('Choose an actual MOD root with metadata or descriptor.mod.')
        self.source_manifest=tree_manifest(self.mod)
        self.version=version();self.docs={};self.actions=[];self.notes=[];self.population_reasons={}
        previous=self.mod/'EDITOR-REVIEW.json'
        if previous.exists():self.population_reasons=json.loads(previous.read_text(encoding='utf-8-sig')).get('population_reasons',{})
        self.regions={};self.states=defaultdict(list);self.pops=defaultdict(list);self.buildings=defaultdict(list);self.strategic={};self.country_defs={}
        self.cultures=set();self.religions=set();self.traits=set();self.building_types=set()
        folders=['map_data/state_regions','common/history/states','common/history/pops','common/history/buildings','common/history/military_formations','common/history/countries','common/history/trade','common/strategic_regions','common/country_definitions']
        for folder in folders:
            for p in effective_files([GAME,self.mod],folder):
                root=self.mod if p.is_relative_to(self.mod) else GAME;rel=p.relative_to(root).as_posix();d=Document(p,rel);self.docs[rel]=d
                if folder=='map_data/state_regions':
                    for n in d.tree.children:self.regions[basekey(n.key)]=(d,n)
                elif folder=='common/country_definitions':
                    for n in d.tree.children:self.country_defs[basekey(n.key)]=(d,n)
                elif folder=='common/strategic_regions':
                    for n in d.tree.children:
                        if n.get('states'):
                            for r in n.get('states').values():self.strategic[r]=(d,n)
                elif folder in ['common/history/states','common/history/pops','common/history/buildings']:
                    target={'common/history/states':self.states,'common/history/pops':self.pops,'common/history/buildings':self.buildings}[folder]
                    for w in d.tree.children:
                        for n in w.children or []:target[n.key.removeprefix('s:')].append((d,w,n))
        for folder,target in [('common/cultures',self.cultures),('common/religions',self.religions),('common/state_traits',self.traits),('common/buildings',self.building_types)]:
            for p in effective_files([GAME,self.mod],folder):
                _,n=read(p);target.update(basekey(c.key) for c in n.children)
        self.production_methods=set();self.pmg_methods={};self.building_pmgs={}
        for p in effective_files([GAME,self.mod],'common/production_methods'):
            _,n=read(p);self.production_methods.update(basekey(c.key) for c in n.children)
        for p in effective_files([GAME,self.mod],'common/production_method_groups'):
            _,n=read(p)
            for c in n.children:
                if c.get('production_methods'):self.pmg_methods[basekey(c.key)]=set(c.get('production_methods').values())
        for p in effective_files([GAME,self.mod],'common/buildings'):
            _,n=read(p)
            for c in n.children:
                if c.get('production_method_groups'):self.building_pmgs[basekey(c.key)]=c.get('production_method_groups').values()
        self.reindex()
        if (self.mod/'EDITOR-GEOGRAPHIC-POPULATION.json').exists():
            from province_move import origins
            origins(self)
    def reindex(self):
        self.province_region={};self.owners=defaultdict(dict)
        for r,(_,n) in self.regions.items():
            for p in n.get('provinces').values() if n.get('provinces') else []:self.province_region[p.upper()]=r
        for r,records in self.states.items():
            for _,_,n in records:
                for cs in n.all('create_state'):
                    tag=cs.scalar('country').removeprefix('c:');q=cs.get('owned_provinces')
                    ps=q.values() if q else self.regions[r][1].get('provinces').values()
                    self.owners[r].setdefault(tag,set()).update(p.upper() for p in ps)
    def state_rows(self,kind,region):
        return [(st.key.split(':')[1],b) for _,_,n in getattr(self,kind).get(region,[]) for st in n.children or [] if st.key and st.key.startswith('region_state:') for b in st.children or [] if b.key==('create_pop' if kind=='pops' else 'create_building')]
    def totals(self):
        return {'population':sum(int(b.scalar('size','0')) for r in self.pops for _,b in self.state_rows('pops',r)), 'building_levels':sum(levels(b) for r in self.buildings for _,b in self.state_rows('buildings',r))}
    def summary(self,r):
        n=self.regions[r][1]
        return {'region':r,'id':n.scalar('id'),'owners':list(self.owners[r]),'provinces':len(n.get('provinces').values()),'population':sum(int(b.scalar('size','0')) for _,b in self.state_rows('pops',r)),'buildings':sum(levels(b) for _,b in self.state_rows('buildings',r)),'traits':n.get('traits').values() if n.get('traits') else [],'arable_land':int(n.scalar('arable_land','0'))}
    def transfer_conflicts(self,region):
        bytype=defaultdict(set)
        for _,b in self.state_rows('buildings',region):
            pm=b.get('activate_production_methods')
            bytype[b.scalar('building')].add(tuple(sorted(pm.values() if pm else [])))
        return {k:[list(v) for v in sorted(vals)] for k,vals in bytype.items() if len(vals)>1}

    def transfer_state_types(self,region):
        return sorted({cs.scalar('state_type','__SOURCE_DEFAULT__') for _,_,n in self.states[region] for cs in n.all('create_state')})

    def transfer(self,region,newtag,production_method_choices=None,state_type=None):
        if newtag not in self.country_defs:raise ValueError('Unknown country tag: '+newtag)
        if not self.owners[region]:raise ValueError('Region has no existing state to transfer.')
        oldtags=set(self.owners[region]);before=self.totals()
        production_method_choices=production_method_choices or {}
        state_types=self.transfer_state_types(region)
        if len(state_types)>1 and state_type not in state_types:
            raise ValueError('Merged state histories have different incorporation types; explicitly choose one source setting: '+str(state_types))
        if state_type is not None and state_type not in state_types:raise ValueError('Choose an existing source state_type setting.')
        bykind=defaultdict(list)
        for _,b in self.state_rows('buildings',region):bykind[b.scalar('building')].append(b)
        for kind,items in bykind.items():
            if len(items)<2:continue
            if any(b.get('level') for b in items):raise ValueError('Cannot merge multiple unique buildings of type '+kind)
            signatures={emit(block('create_building',[clone(x) for x in b.children if x.key not in {'add_ownership','activate_production_methods'}])) for b in items}
            if len(signatures)>1:raise ValueError(kind+': different non-ownership history settings need an explicit merge; no changes applied.')
        conflicts=self.transfer_conflicts(region)
        for kind,choices in conflicts.items():
            if sorted(production_method_choices.get(kind,[])) not in choices:
                raise ValueError(f'{kind}: merged states use different production methods; choose one existing full PM set explicitly: {choices}')
        # A whole-country annexation needs explicit political history redesign.
        for tag in oldtags-{newtag}:
            if not any(tag in owners for r,owners in self.owners.items() if r!=region):raise ValueError(f'{tag} would lose its last state. Resolve its country/subject/event history explicitly before exporting this annexation.')
        # Local government assets follow the state. Explicit foreign government
        # shares and investors in other regions remain foreign property.
        for tag,b in self.state_rows('buildings',region):
            for add in b.all('add_ownership'):
                for own in add.children or []:
                    if own.key=='country' and own.scalar('country','').removeprefix('c:')==tag:
                        setval(own,'country','"c:'+newtag+'"')
        first=None
        for _,_,n in self.states[region]:
            for cs in list(n.all('create_state')):
                if first is None:first=cs;setval(cs,'country','c:'+newtag);setlist(cs,'owned_provinces',self.regions[region][1].get('provinces').values())
                else:n.children.remove(cs)
        if state_type is not None:
            if state_type=='__SOURCE_DEFAULT__':first.children=[x for x in first.children if x.key!='state_type']
            else:setval(first,'state_type',state_type)
        for kind in ['pops','buildings']:
            for _,_,n in getattr(self,kind)[region]:
                for st in n.children or []:
                    if st.key and st.key.startswith('region_state:'):st.key='region_state:'+newtag
        for records in self.buildings.values():
            for _,_,n in records:
                for own in n.walk():
                    if own.scalar('region')==region and own.scalar('country','').removeprefix('c:') in oldtags:setval(own,'country','"c:'+newtag+'"')
        # Combine duplicate history wrappers and buildings when several owners
        # become one state. Keep all pop groups and ownership shares.
        for kind in ['pops','buildings']:
            records=getattr(self,kind)[region]
            if not records:continue
            target=records[0][2]
            contents=[]
            for _,_,n in records:
                for st in list(n.children or []):
                    if st.key and st.key.startswith('region_state:'):
                        contents.extend(st.children or []);n.children.remove(st)
            if kind=='buildings':
                merged={}
                for b in contents:
                    if b.key!='create_building':continue
                    key=b.scalar('building')
                    if key in production_method_choices:setlist(b,'activate_production_methods',production_method_choices[key])
                    if key not in merged:merged[key]=b;continue
                    dest=merged[key]
                    for add in b.all('add_ownership'):dest.children.append(clone(add))
                    if b.get('level'):
                        setval(dest,'level',int(dest.scalar('level','0'))+int(b.scalar('level')))
                contents=[b for b in contents if b.key!='create_building']+list(merged.values())
                for b in contents:
                    if b.key!='create_building':continue
                    owners={}
                    for add in b.all('add_ownership'):
                        for own in add.children or []:
                            ident=clone(own);setval(ident,'levels',0);key=emit(ident)
                            if key in owners:setval(owners[key],'levels',int(owners[key].scalar('levels','0'))+int(own.scalar('levels','0')))
                            else:owners[key]=own
                    if owners:
                        b.children=[x for x in b.children if x.key!='add_ownership']
                        b.children.append(block('add_ownership',list(owners.values())))
            target.children.append(block('region_state:'+newtag,contents))
        self.reindex();self._military_transfer(region,oldtags,newtag)
        for tag in oldtags-{newtag}:
            d,c=self.country_defs[tag]
            if c.scalar('capital')==region:
                choices=[r for r,tags in self.owners.items() if tag in tags]
                target=max(choices,key=lambda r:sum(int(b.scalar('size','0')) for t,b in self.state_rows('pops',r) if t==tag))
                setval(c,'capital',target);self.notes.append(f'{tag} capital moved to {target}, the largest remaining population.')
        for d in self.docs.values():
            if '/history/countries/' in d.rel:
                for w in d.tree.children:
                    for c in w.children or []:
                        if c.key and c.key.removeprefix('c:') in oldtags-{newtag}:
                            for q in c.all('set_market_capital'):
                                if q.value==region:q.value=self.country_defs[c.key[2:]][1].scalar('capital')
        self.actions.append({'op':'transfer','region':region,'from':sorted(oldtags),'to':newtag,'production_method_choices':production_method_choices,'state_type':state_type or state_types[0]})
        assert self.totals()==before,'Conservation failure'
    def _military_transfer(self,r,oldtags,newtag):
        buckets=defaultdict(list)
        for d in list(self.docs.values()):
            if '/military_formations/' not in d.rel:continue
            for w in d.tree.children:
                for c in w.children or []:
                    if not c.key or c.key.removeprefix('c:') not in oldtags-{newtag}:continue
                    for f in c.all('create_military_formation'):
                        for u in list(f.all('combat_unit')+f.all('ship')):
                            if u.scalar('state_region')=='s:'+r:f.children.remove(u);buckets[f.scalar('type')].append(clone(u))
        if buckets:
            d=next(d for d in self.docs.values() if '/military_formations/' in d.rel)
            for typ,units in buckets.items():d.tree.children[0].children.append(block('c:'+newtag,[block('create_military_formation',[scalar('type',typ),scalar('hq_region','sr:'+self.strategic[r][1].key),*units])]))
        self.notes.append('Country-level treaties, claims and event allegiance stay with their original country; territory-dependent references are listed in export review.')
    def move_provinces(self,source,target,selected,population_ratio=.5,building_ratio=.5,arable_amount=0,resource_ratio=.5,reason='',production_method_choices=None,traits=None):
        from province_move import move
        return move(self,source,target,selected,population_ratio,building_ratio,arable_amount,resource_ratio,reason,production_method_choices,traits)
    def geography_ledger(self):
        if any(hasattr(pop,'original_region') for r in self.pops for _,pop in self.state_rows('pops',r)):
            from province_move import population_ledger
            return population_ledger(self)
        return None
    def split(self,source,new,selected,ratio=0.5,unique_buildings=None):
        from province_move import divide_building_ownership
        known={getattr(pop,'original_region',None) for _,pop in self.state_rows('pops',source)}-{None}
        if len(known)>1:raise ValueError('This region contains multiple original geographic populations. Split requires explicit per-origin allocations; the one-ratio operation does not guess them.')

        if not re.fullmatch(r'STATE_[A-Z0-9_]+',new) or new in self.regions:raise ValueError('Use a new unique STATE_UPPERCASE_KEY.')
        if source not in self.strategic:raise ValueError('Source region has no strategic region; resolve it before splitting.')
        d,n=self.regions[source];allps={p.upper() for p in n.get('provinces').values()};selected={p.upper() for p in selected}
        if not selected or not selected<allps:raise ValueError('Select a nonempty proper subset of provinces from this region.')
        if not 0<ratio<1:raise ValueError('Split ratio must be between 0 and 1.')
        fractions={tag:(1 if ps<=selected else ratio if ps&selected else 0) for tag,ps in self.owners[source].items()}
        unique_buildings=unique_buildings or {}
        # Monuments use top-level `level`, not investor `levels`. They cannot
        # be halved or discarded; require an explicit location decision BEFORE
        # mutating the project. UI must surface this review to the user.
        for tag,b in self.state_rows('buildings',source):
            if b.get('level') and not b.get('add_ownership') and 0<fractions.get(tag,0)<1:
                if unique_buildings.get(b.scalar('building')) not in {'source','new'}:
                    raise ValueError('Choose source/new location for unique building '+b.scalar('building'))
        before=self.totals();q=clone(n);q.key=new;setval(q,'id',max(int(v.scalar('id','0')) for _,v in self.regions.values())+1)
        color_tokens=lambda items:['"x'+v[1:].upper()+'"' for v in sorted(items)]
        setlist(q,'provinces',color_tokens(selected));setlist(n,'provinces',color_tokens(allps-selected))
        for k in ['arable_land']:
            if n.get(k):v=int(n.scalar(k));nv=int(v*ratio);setval(q,k,nv);setval(n,k,v-nv)
        for key in ['capped_resources']:
            if n.get(key):
                for a,b in zip(n.get(key).children,q.get(key).children):v=int(a.value);b.value=str(int(v*ratio));a.value=str(v-int(v*ratio))
        for a,b in zip(n.all('resource'),q.all('resource')):
            for k in ['amount','undiscovered_amount','discovered_amount','depleted_amount']:
                if a.get(k):v=int(a.scalar(k));nv=int(v*ratio);setval(b,k,nv);setval(a,k,v-nv)
        for node,ps in [(n,allps-selected),(q,selected)]:
            for key in ['impassable','prime_land']:
                if node.get(key):setlist(node,key,[v for v in node.get(key).values() if v.upper() in ps])
            for hub in ['city','farm','mine','wood','center_province']:
                if node.get(hub) and node.scalar(hub).upper() not in ps:
                    node.children=[c for c in node.children if c.key!=hub]
            if node.get('port') and node.scalar('port').upper() not in ps:
                node.children=[c for c in node.children if c.key not in ['port','naval_exit_id']]
        d.tree.children.append(q);self.regions[new]=(d,q)
        sd,sr=self.strategic[source];sr.get('states').children.append(scalar(None,new));self.strategic[new]=(sd,sr)
        for d,w,n in list(self.states[source]):
            nn=clone(n);nn.key='s:'+new
            for orig,target in [(n,allps-selected),(nn,selected)]:
                for cs in list(orig.all('create_state')):
                    tag=cs.scalar('country').removeprefix('c:');ps=self.owners[source][tag]&target
                    if ps:setlist(cs,'owned_provinces',color_tokens(ps))
                    else:orig.children.remove(cs)
            w.children.append(nn);self.states[new].append((d,w,nn))
        for kind in ['pops','buildings']:
            for d,w,n in list(getattr(self,kind)[source]):
                nn=clone(n);nn.key='s:'+new
                for oldst,newst in zip(list(n.children),list(nn.children)):
                    if not oldst.key or not oldst.key.startswith('region_state:'):continue
                    tag=oldst.key.split(':')[1];f=fractions.get(tag,0)
                    if f==0:nn.children.remove(newst);continue
                    if f==1:n.children.remove(oldst)
                    for a,b in zip(list(oldst.children),list(newst.children)):
                        if kind=='pops':
                            v=int(a.scalar('size','0'));nv=int(v*f);setval(b,'size',nv)
                            if f<1:setval(a,'size',v-nv)
                        else:
                            if a.get('level') and not a.get('add_ownership'):
                                v=int(a.scalar('level'));side='new' if f==1 else unique_buildings[a.scalar('building')]
                                setval(a,'level',v if side=='source' else 0);setval(b,'level',v if side=='new' else 0)
                            divide_building_ownership(a,b,f)
                            for own in b.walk():
                                if own.scalar('region')==source and own.scalar('country')=='c:'+tag:setval(own,'region','"'+new+'"')
                    if kind=='pops':
                        newst.children=[b for b in newst.children if b.key!='create_pop' or int(b.scalar('size','0'))>0]
                        oldst.children=[b for b in oldst.children if b.key!='create_pop' or int(b.scalar('size','0'))>0]
                    else:
                        newst.children=[b for b in newst.children if b.key!='create_building' or levels(b)>0]
                        oldst.children=[b for b in oldst.children if b.key!='create_building' or levels(b)>0]
                w.children.append(nn);getattr(self,kind)[new].append((d,w,nn))
        for d in self.docs.values():
            if '/military_formations/' not in d.rel:continue
            for w in d.tree.children:
                for c in w.children or []:
                    f=fractions.get(c.key.removeprefix('c:') if c.key else '',0)
                    for form in c.all('create_military_formation'):
                        for u in list(form.all('combat_unit')+form.all('ship')):
                            if u.scalar('state_region')!='s:'+source:continue
                            v=int(u.scalar('count'));nv=int(v*f);nu=clone(u);setval(nu,'state_region','s:'+new);setval(nu,'count',nv)
                            if nv:form.children.append(nu)
                            if v==nv:form.children.remove(u)
                            else:setval(u,'count',v-nv)
        self.reindex()
        # An investor whose entire local state moved cannot keep referencing
        # the now nonexistent old country/state intersection, even abroad.
        for records in self.buildings.values():
            for _,_,node in records:
                for own in node.walk():
                    if own.scalar('region')==source and fractions.get(own.scalar('country','').removeprefix('c:'),0)==1:
                        setval(own,'region','"'+new+'"')
        self.actions.append({'op':'split','source':source,'new':new,'provinces':sorted(selected),'ratio':ratio,'unique_buildings':unique_buildings})
        self.notes.append(f'{new}: original terrain raster retained. Review hub locations, coastline/port exit, loc names and external event references before game test.')
        assert self.totals()==before,(before,self.totals())
    def set_hubs(self,region,values_by_kind):
        """Explicit province choice plus matching visual locator, never lexical-first placement."""
        from PIL import Image
        import numpy as np
        n=self.regions[region][1];ps={v.upper() for v in n.get('provinces').values()}
        unknown=set(values_by_kind)-{'city','farm','mine','wood','port','naval_exit_id'}
        if unknown:raise ValueError('Unknown hub fields: '+','.join(unknown))
        for key,value in values_by_kind.items():
            if value and key!='naval_exit_id' and value.upper() not in ps:raise ValueError(f'{region}: {key} outside selected provinces')
        mapfile=self.mod/'map_data/provinces.png'
        if not mapfile.exists():mapfile=GAME/'map_data/provinces.png'
        arr=np.asarray(Image.open(mapfile).convert('RGB'));height=arr.shape[0]
        for kind,value in values_by_kind.items():
            if not value:continue
            setval(n,kind,value)
            if kind=='naval_exit_id':continue
            rel=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt'
            if rel not in self.docs:
                path=self.mod/rel if (self.mod/rel).exists() else GAME/rel
                self.docs[rel]=Document(path,rel)
            d=self.docs[rel];instances=d.tree.children[0].get('instances');rid=n.scalar('id')
            matches=[v for v in instances.children if v.scalar('id')==rid]
            if len(matches)>1:raise ValueError('Duplicate locator instance '+rid)
            rgb=tuple(bytes.fromhex(value.lstrip('xX')));yy,xx=np.where((arr==rgb).all(axis=2))
            if not len(xx):raise ValueError('Province color missing from actual map: '+value)
            if kind=='port':
                sea_id=str(values_by_kind.get('naval_exit_id') or n.scalar('naval_exit_id',''))
                sea_node=next((q for _,q in self.regions.values() if q.scalar('id')==sea_id),None)
                if sea_node is None:raise ValueError('Select the sea region before placing a port.')
                sea_colors=[tuple(bytes.fromhex(v.lstrip('xX'))) for v in sea_node.get('provinces').values()]
                sea_mask=np.zeros(arr.shape[:2],dtype=bool)
                for color in sea_colors:sea_mask|=(arr==color).all(axis=2)
                adjacent=np.zeros(sea_mask.shape,dtype=bool)
                adjacent[1:]|=sea_mask[:-1];adjacent[:-1]|=sea_mask[1:];adjacent[:,1:]|=sea_mask[:,:-1];adjacent[:,:-1]|=sea_mask[:,1:]
                coastal=adjacent[yy,xx]
                if not coastal.any():raise ValueError('Selected port province does not touch the selected sea region.')
                yy=yy[coastal];xx=xx[coastal]
            near=int(np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2));px=int(xx[near]);py=int(yy[near])
            if matches:
                inst=matches[0];pos=inst.get('position').values();ox=int(float(pos[0]));oy=height-1-int(float(pos[2]))
                # Preserve authored precise positions when they still occupy the selected hub.
                if 0<=oy<height and 0<=ox<arr.shape[1] and tuple(arr[oy,ox])==rgb and (kind!='port' or adjacent[oy,ox]):continue
            else:
                inst=block(None,[scalar('id',rid),values('position',['0','0','0']),values('rotation',['0','0','0','1']),values('scale',['1','1','1'])]);instances.children.append(inst)
            setlist(inst,'position',[f'{px}.500000','0.000000',f'{height-1-py}.500000'])
        self.actions.append({'op':'hubs','region':region,'values':values_by_kind,'locator_status':'pixel checked; game visual verification required'})
    def traits_set(self,region,names):
        unknown=set(names)-self.traits
        if unknown:raise ValueError('Unknown traits: '+','.join(unknown))
        setlist(self.regions[region][1],'traits',names);self.actions.append({'op':'traits','region':region,'traits':names})
    def arable_set(self,region,amount,reason):
        amount=integer(amount)
        if not str(reason).strip():raise ValueError('Record the geographic/design reason for changing arable land.')
        node=self.regions[region][1];old=int(node.scalar('arable_land','0'))
        setval(node,'arable_land',amount)
        self.actions.append({'op':'arable_land','region':region,'before':old,'after':amount,'reason':str(reason).strip()})

    def edit_pop(self,region,index,data,reason):
        tag,pop=self.state_rows('pops',region)[index]
        if set(data)-{'culture','religion','size'}:raise ValueError('Unexpected population fields.')
        if data['culture'] not in self.cultures or (data.get('religion') and data['religion'] not in self.religions):
            raise ValueError('Unknown culture or religion.')
        size=integer(data['size'],1)
        if not str(reason).strip():raise ValueError('Record the population/design reason; transfer and pure split do not need population edits.')
        before={k:pop.scalar(k,'') for k in ['culture','religion','size']}
        setval(pop,'culture',data['culture']);setval(pop,'size',size)
        if data.get('religion'):setval(pop,'religion',data['religion'])
        else:pop.children=[n for n in pop.children if n.key!='religion']
        self.actions.append({'op':'edit_pop','region':region,'owner':tag,'index':index,'before':before,'values':data,'reason':str(reason).strip()})

    def add_pop(self,region,data,reason):
        if set(data)-{'owner','culture','religion','size','original_region'}:raise ValueError('Unexpected population fields.')
        if data['owner'] not in self.owners[region] or data['culture'] not in self.cultures or (data.get('religion') and data['religion'] not in self.religions):
            raise ValueError('Unknown local owner, culture or religion.')
        size=integer(data['size'],1)
        if not str(reason).strip():raise ValueError('Record why this population change is appropriate.')
        known={getattr(pop,'original_region',None) for _,pop in self.state_rows('pops',region)}-{None}
        origin=data.get('original_region')
        if len(known)>1 and origin not in known:raise ValueError('Choose the original geographic area for the new population.')
        if origin and known and origin not in known:raise ValueError('Unknown original geographic population area.')
        n=self._history_region('pops',region)
        fields=[scalar('culture',data['culture']),scalar('size',size)]
        if data.get('religion'):fields.insert(1,scalar('religion',data['religion']))
        newpop=block('create_pop',fields)
        if origin or known:newpop.original_region=origin or next(iter(known))
        n.children.append(block('region_state:'+data['owner'],[newpop]))
        self.actions.append({'op':'add_pop','region':region,'values':data,'reason':str(reason).strip()})

    def _history_region(self,kind,region):
        records=getattr(self,kind)[region]
        if records:return records[0][2]
        d=next(d for d in self.docs.values() if d.rel.startswith('common/history/'+kind+'/'))
        wrapper=d.tree.children[0];node=block('s:'+region,[]);wrapper.children.append(node)
        records.append((d,wrapper,node));return node

    def validate_pms(self,building,names):
        if building not in self.building_types:raise ValueError('Unknown building type.')
        if not isinstance(names,list) or any(not isinstance(n,str) for n in names):raise ValueError('Production methods must be a list of source IDs.')
        unknown=set(names)-self.production_methods
        if unknown:raise ValueError('Unknown production methods: '+', '.join(sorted(unknown)))
        groups=[self.pmg_methods.get(g,set()) for g in self.building_pmgs.get(building,[])]
        allowed=set().union(*groups) if groups else set()
        if set(names)-allowed:raise ValueError('Production method does not belong to this building: '+', '.join(sorted(set(names)-allowed)))
        if any(len(set(names)&g)>1 for g in groups):raise ValueError('Choose only one production method per group.')

    def building_pm_set(self,region,index,names):
        _,b=self.state_rows('buildings',region)[index];self.validate_pms(b.scalar('building'),names)
        setlist(b,'activate_production_methods',names)
        self.actions.append({'op':'building_pms','region':region,'index':index,'production_methods':names})

    def add_building(self,region,data):
        if set(data)-{'owner','building','levels','production_methods'}:raise ValueError('Unexpected building fields.')
        if data['owner'] not in self.owners[region]:raise ValueError('Building owner must own part of this region.')
        amount=integer(data['levels'],1);self.validate_pms(data['building'],data['production_methods'])
        node=self._history_region('buildings',region)
        if any(t==data['owner'] and b.scalar('building')==data['building'] for t,b in self.state_rows('buildings',region)):
            raise ValueError('This building already exists for that owner; edit its level/PM instead of adding a duplicate.')
        b=block('create_building',[scalar('building','"'+data['building']+'"'),
            block('add_ownership',[block('country',[scalar('country','"c:'+data['owner']+'"'),scalar('levels',amount)])]),
            values('activate_production_methods',data['production_methods'])])
        node.children.append(block('region_state:'+data['owner'],[b]))
        self.actions.append({'op':'add_building','region':region,'values':data})

    def building_levels_set(self,region,index,value):
        value=integer(value,1);_,b=self.state_rows('buildings',region)[index];old=levels(b)
        qs=[q for q in b.walk() if q.key=='levels']
        if not qs:
            if not b.get('level'):raise ValueError('Building has no supported ownership or top-level level.')
            if value!=1:raise ValueError('Unique/monument history must stay at one level; relocation requires separate potential/locator review.')
            setval(b,'level',value)
        else:
            remaining=value
            for q in qs[:-1]:
                n=int(value*int(q.value)/old);remaining-=n;q.value=str(n)
            qs[-1].value=str(remaining)
        self.actions.append({'op':'building_levels','region':region,'index':index,'before':old,'levels':value})

    def project_data(self):
        return {'version':self.version,'source':str(self.mod),'source_manifest':self.source_manifest,
                'actions':self.actions,'notes':self.notes,'population_reasons':self.population_reasons,'geographic_population':self.geography_ledger(),
                'files':{rel:d.render() for rel,d in self.docs.items() if d.render()!=d.text}}

    def save_project(self,path):
        path=Path(path).resolve()
        if not path.is_relative_to((WORK/'projects').resolve()) or path.is_relative_to(self.mod):raise ValueError('Save project JSON inside WORK/projects and outside the source MOD tree.')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(self.project_data(),ensure_ascii=False,indent=2),encoding='utf-8')

    @classmethod
    def load_project(cls,path):
        data=json.loads(Path(path).read_text(encoding='utf-8-sig'));source=Path(data['source']).resolve()
        if data['version']!=version():raise ValueError('Saved project targets a different installed game version.')
        if not data.get('source_manifest') or tree_manifest(source)!=data['source_manifest']:
            raise ValueError('Project source changed or has no saved fingerprint. Reopen the exact source or migrate explicitly.')
        prepared=[]
        for rel,text in data['files'].items():
            relpath=Path(rel)
            if relpath.is_absolute() or '..' in relpath.parts:raise ValueError('Unsafe project path.')
            parse(text);prepared.append((rel,text))
        dest=WORK/'projects'/('editor-load-'+uuid.uuid4().hex)
        shutil.copytree(source,dest)
        for rel,text in prepared:
            target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8-sig')
        if data.get('geographic_population'):(dest/'EDITOR-GEOGRAPHIC-POPULATION.json').write_text(json.dumps(data['geographic_population'],ensure_ascii=False,indent=2),encoding='utf-8')
        project=cls(dest);project.actions=data['actions'];project.notes=data['notes'];project.population_reasons=data.get('population_reasons',{});project.notes.append('Restored from project '+str(Path(path).resolve())+' with original source '+str(source))
        return project

    def dependency_review(self):
        affected={a[k] for a in self.actions for k in ['region','source','new','target'] if k in a and str(a[k]).startswith('STATE_')}
        if not affected:return []
        hits=[];pattern=re.compile(r'\b('+'|'.join(re.escape(x) for x in sorted(affected))+r')\b')
        for folder in ['common','events']:
            for path in effective_files([GAME,self.mod],folder):
                if not path.name.endswith('.txt'):continue
                root=self.mod if path.is_relative_to(self.mod) else GAME
                rel=path.relative_to(root).as_posix()
                if rel in self.docs:continue
                for number,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
                    if pattern.search(line) and not line.lstrip().startswith('#'):
                        hits.append({'path':str(path),'line':number,'text':line.strip()[:280],'status':'semantic review required; not automatically rewritten'})
        return hits

    def validate(self):
        issues=[];seen={}
        for r,(_,n) in self.regions.items():
            ps={p.upper() for p in n.get('provinces').values()}
            for p in ps:
                if p in seen:issues.append(f'{p} occurs in {seen[p]} and {r}')
                seen[p]=r
            for k in ['city','farm','mine','wood','port']:
                if n.get(k) and n.scalar(k).upper() not in ps:issues.append(f'{r}: {k} outside region')
            if n.get('arable_land'):
                try:integer(n.scalar('arable_land'))
                except ValueError:issues.append(f'{r}: invalid arable_land')
                for k in ['city','farm','mine','wood']:
                    if not n.get(k):issues.append(f'{r}: choose {k} hub and matching locator before export')
        for action in self.actions:
            if action['op']!='split':continue
            r=action['new'];n=self.regions[r][1]
            for k in ['city','farm','mine','wood']+(['port'] if n.get('port') else []):
                rel=f'gfx/map/map_object_data/generated_map_object_locators_{k}.txt'
                d=self.docs.get(rel)
                if d is None:
                    path=self.mod/rel
                    if path.exists():
                        d=Document(path,rel);self.docs[rel]=d
                if d is None or not any(v.scalar('id')==n.scalar('id') for v in d.tree.children[0].get('instances').children):issues.append(f'{r}: missing {k} visual locator')
        for r in self.pops:
            for t,b in self.state_rows('pops',r):
                if t not in self.owners[r]:issues.append(f'{r}: orphan pop owner {t}')
                if b.scalar('culture') not in self.cultures:issues.append(f'{r}: unknown culture {b.scalar("culture")}')
                if b.scalar('religion') and b.scalar('religion') not in self.religions:issues.append(f'{r}: unknown religion')
                if int(b.scalar('size','0'))<0:issues.append(f'{r}: negative pop')
        for r in self.buildings:
            for t,b in self.state_rows('buildings',r):
                if t not in self.owners[r]:issues.append(f'{r}: orphan building owner {t}')
                if b.scalar('building') not in self.building_types:issues.append(f'{r}: unknown building')
        affected={a.get('region') for a in self.actions if a['op'] in {'split','hubs','move_provinces'}}
        affected.update(a.get('source') for a in self.actions if a['op']=='split')
        affected.update(a.get('new') for a in self.actions if a['op']=='split')
        affected.update(a[k] for a in self.actions if a['op']=='move_provinces' for k in ['source','target'])
        for r in affected-{None}:
            if any(b.scalar('building')=='building_port' and levels(b)>0 for _,b in self.state_rows('buildings',r)):
                node=self.regions[r][1]
                if not node.get('port') or not node.get('naval_exit_id'):issues.append(f'{r}: port buildings need an explicitly valid port hub and naval_exit_id after the split.')
        return issues
    def export(self,dest):
        dest=Path(dest).resolve()
        if dest.parent!=(WORK/'exports').resolve() or dest.exists():raise ValueError('Export must be a NEW direct child directory of workbench/exports; never nest inside an existing candidate.')
        if version()!=self.version:raise ValueError('Installed game version changed; refresh source catalog and reopen project.')
        if tree_manifest(self.mod)!=self.source_manifest:raise ValueError('Source MOD changed while the project was open; reopen or restore its exact source.')
        for d in self.docs.values():
            if hashlib.sha256(d.path.read_bytes()).hexdigest()!=d.sha:raise ValueError('Source changed while editor was open: '+str(d.path))
        issues=self.validate()
        if issues:raise ValueError('\n'.join(issues[:25]))
        stage=(WORK/'projects'/('editor-export-staging-'+uuid.uuid4().hex)).resolve()
        if not stage.is_relative_to(WORK.resolve()):raise ValueError('Unsafe staging path.')
        shutil.copytree(self.mod,stage);changed=[]
        for rel,d in self.docs.items():
            rendered=d.render()
            if rendered!=d.text:
                parse(rendered);p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(rendered,'utf-8-sig');changed.append(rel)
        port_regions=set()
        for action in self.actions:
            if action['op'] in {'split','hubs','move_provinces'}:
                port_regions.update(action[k] for k in ['region','source','new','target'] if k in action)
        from harbor_routes import ensure_new_port_routes
        harbor_review=ensure_new_port_routes(stage,port_regions) if port_regions else {'new_ports':[],'changed':False,'engine_verified':False}
        if harbor_review['changed']:changed.append('gfx/map/spline_network/spline_network.splnet')
        sys.path.insert(0,str(WORK/'tools'))
        from population_envelope_audit import audit
        ledger=self.geography_ledger()
        if ledger:(stage/'EDITOR-GEOGRAPHIC-POPULATION.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
        preview=audit(stage)
        reasons=dict(self.population_reasons)
        for action in self.actions:
            if action['op'] in {'edit_pop','add_pop'}:
                parents=preview.get('candidate_to_original_regions',{}).get(action['region'],[])
                for parent in parents:
                    if action.get('reason'):reasons[parent]=reasons.get(parent,'')+'; '+action['reason']
        population=audit(stage,reasons)
        failures=[r['original_region']+': '+r['status'] for r in population['rows'] if r['status']!='within_envelope']
        failures+=['missing reason: '+r for r in population['missing_change_reasons']]
        if population['unresolved_mapping']:failures.append('New geography crosses original parents or has unknown provinces.')
        if failures:
            (stage/'EDITOR-REJECTED-POPULATION.json').write_text(json.dumps(population,ensure_ascii=False,indent=2),encoding='utf8')
            raise ValueError('Population export rejected; no export directory was created. '+ '; '.join(failures[:12])+'\nEvidence: '+str(stage/'EDITOR-REJECTED-POPULATION.json'))
        metadata=stage/'.metadata/metadata.json'
        if metadata.exists():
            m=json.loads(metadata.read_text('utf-8-sig'));m['name']='NESND scenario '+dest.name;m['id']='nesnd-editor-'+dest.name;metadata.write_text(json.dumps(m,ensure_ascii=False,indent=2),'utf-8')
        newregions=[a['new'] for a in self.actions if a['op']=='split']
        if newregions:
            for lang in ['english','simp_chinese']:
                p=stage/f'localization/{lang}/nesnd_editor_l_{lang}.yml';p.parent.mkdir(parents=True,exist_ok=True)
                previous=p.read_text(encoding='utf-8-sig') if p.exists() else 'l_'+lang+':\n'
                existing=set(re.findall(r'^\s*([^\s:#]+):\d*\s+"',previous,re.M))
                additions=''.join(f' {r}:0 "{r.removeprefix("STATE_").replace("_"," ").title()}"\n' for r in dict.fromkeys(newregions) if r not in existing)
                if additions:p.write_text(previous+('' if previous.endswith('\n') else '\n')+additions,'utf-8-sig')
        transport_changed=any(a['op'] in {'split','hubs','move_provinces'} for a in self.actions)
        dependencies=self.dependency_review()
        population['candidate']=str(dest)
        for row in population['candidate_effective_sources']:
            path=Path(row['file'])
            if path.is_relative_to(stage):row['file']=str(dest/path.relative_to(stage))
        for row in population['rows']:
            for child in row['child_allocations_since_fixed_split']:
                child['candidate_population_sources']=[str(dest/Path(x).relative_to(stage)) if Path(x).is_relative_to(stage) else x for x in child['candidate_population_sources']]
        backup=WORK/'backups'/('candidate-editor-'+uuid.uuid4().hex)
        review={'candidate_backup':str(backup),'game':self.version,'source':str(self.mod),'source_manifest':self.source_manifest,'export':str(dest),'totals':self.totals(),'actions':self.actions,'notes':self.notes,'changed_files':changed,
                'validation':'Source fingerprints, population envelope and script/reference checks passed. Engine, transport and political semantics are NOT verified.',
                'population_reasons':reasons,'population_audit':'EDITOR-POPULATION-AUDIT.json','dependency_review':dependencies,
                'transport_review_required':transport_changed,'harbor_routes':harbor_review,'engine_verified':False,
                'transport_status':'NOT VERIFIED: review spline anchors, internal routes and passable neighbouring states in the native map editor.' if transport_changed else 'No geometry actions recorded; engine verification still required.'}
        (stage/'EDITOR-POPULATION-AUDIT.json').write_text(json.dumps(population,ensure_ascii=False,indent=2),encoding='utf8')
        (stage/'EDITOR-REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),'utf-8')
        # Every delivered candidate has a separate verified copy; it remains
        # a candidate until real engine evidence exists, never an accepted build.
        candidate_manifest=tree_manifest(stage)
        shutil.copytree(stage,backup/'mod')
        if tree_manifest(backup/'mod')!=candidate_manifest:raise ValueError('Candidate backup verification failed; staging retained.')
        (backup/'manifest.json').write_text(json.dumps({'source':str(dest),'backup':str(backup/'mod'),'status':'candidate',
            'label':'editor-export','version':self.version,'sha256':candidate_manifest,'verified_files':len(candidate_manifest),
            'engine_verified':False},ensure_ascii=False,indent=2),encoding='utf8')
        # Same-volume rename publishes only a fully checked candidate. Existing
        # exports and all original sources are untouched, so rollback is opening
        # the previous project/export, not overwriting a successful version.
        if not stage.is_relative_to(WORK.resolve()) or not dest.is_relative_to((WORK/'exports').resolve()):raise ValueError('Unsafe publish path.')
        stage.rename(dest)
        return review
