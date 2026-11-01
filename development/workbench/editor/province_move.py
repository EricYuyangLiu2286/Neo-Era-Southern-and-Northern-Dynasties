"""Existing-region province transactions, deliberately refusing unresolved scope semantics."""
import copy,json,sys
from collections import defaultdict
from pathlib import Path
from fractions import Fraction

def scaled(count,ratio):
    value=Fraction(str(ratio))
    return count*value.numerator//value.denominator

def origins(project):
    from model import WORK
    sys.path.insert(0,str(WORK/'tools'))
    from population_envelope_audit import extract,FROZEN_GAME,ORIGINAL,ORIGINAL_MANIFEST_SHA
    baseline=extract([FROZEN_GAME,ORIGINAL])
    parent={p:r for r,ps in baseline['regions'].items() for p in ps}
    recorded=project.mod/'EDITOR-GEOGRAPHIC-POPULATION.json'
    ledger=json.loads(recorded.read_text(encoding='utf-8-sig')) if recorded.exists() else {}
    for region in project.pops:
        rows=project.state_rows('pops',region)
        parents={parent.get(p.upper()) for p in project.regions[region][1].get('provinces').values()}
        records=ledger.get('regions',{}).get(region)
        for index,(tag,pop) in enumerate(rows):
            if hasattr(pop,'original_region'):continue
            if records is not None:
                item=records[index]
                actual={'country':tag,'culture':pop.scalar('culture','<unspecified>'),'religion':pop.scalar('religion','<culture_default>'),'population':int(pop.scalar('size'))}
                if {k:v for k,v in item.items() if k!='original_region'}!=actual:raise ValueError('Population geographic record differs from source history.')
                pop.original_region=item['original_region']
            elif len(parents)==1 and None not in parents:pop.original_region=next(iter(parents))
            else:raise ValueError('This source region needs explicit population geography records: '+region)
    return parent,ORIGINAL_MANIFEST_SHA

def population_ledger(project):
    _,manifest=origins(project)
    return {'fixed_manifest_sha256':manifest,'method':'Every actual history pop row retains its original geographic parent through movement. Fixed parent totals are never reset.','regions':{
        region:[{'original_region':pop.original_region,'country':tag,'culture':pop.scalar('culture','<unspecified>'),'religion':pop.scalar('religion','<culture_default>'),'population':int(pop.scalar('size'))} for tag,pop in project.state_rows('pops',region)]
        for region in project.pops}}

def merge_buildings(items,choices):
    from model import clone,block,emit,setlist,levels
    merged={}
    for item in items:
        kind=item.scalar('building')
        if kind in choices:setlist(item,'activate_production_methods',choices[kind])
        if kind not in merged:merged[kind]=item;continue
        target=merged[kind]
        if item.get('level') or target.get('level'):raise ValueError('Unique building merge needs separate location design: '+kind)
        def signature(b):return emit(block('create_building',[clone(n) for n in b.children if n.key not in {'add_ownership'}]))
        if signature(item)!=signature(target):raise ValueError('Building history/production settings conflict for '+kind+'; choose an existing full production-method set.')
        for own in item.all('add_ownership'):target.children.append(clone(own))
    return list(merged.values())

def divide_building_ownership(source,destination,fraction):
    """Floor each building total once, then apportion shares by largest remainder."""
    from model import levels
    pairs=[(a,b) for a,b in zip(source.walk(),destination.walk()) if a.key=='levels']
    total=sum(int(a.value) for a,b in pairs)
    wanted=scaled(total,fraction)
    shares=[wanted*int(a.value)//total for a,b in pairs] if total else []
    order=sorted(range(len(pairs)),key=lambda i:(-(wanted*int(pairs[i][0].value)%total),i)) if total else []
    for i in order[:wanted-sum(shares)]:shares[i]+=1
    for (a,b),share in zip(pairs,shares):
        a.value=str(int(a.value)-share);b.value=str(share)
    for node in [source,destination]:
        for add in list(node.all('add_ownership')):
            add.children=[own for own in add.children or [] if int(own.scalar('levels','0'))>0]
            if not add.children:node.children.remove(add)
    return wanted

def capacity_overages(project,region):
    from model import levels
    from collections import Counter
    node=project.regions[region][1]
    built=Counter()
    for tag,b in project.state_rows('buildings',region):built[b.scalar('building')]+=levels(b)
    agricultural=set(node.get('arable_resources').values() if node.get('arable_resources') else [])
    excess={'arable_land':max(0,sum(v for k,v in built.items() if k in agricultural)-int(node.scalar('arable_land','0')))}
    caps={c.key:int(c.value) for c in node.get('capped_resources').children} if node.get('capped_resources') else {}
    for resource in node.all('resource'):
        caps[resource.scalar('type')]=sum(int(resource.scalar(k,'0')) for k in ['amount','discovered_amount'])
    for kind,capacity in caps.items():excess[kind]=max(0,built[kind]-capacity)
    return excess

def move(project,source,target,selected,population_ratio,building_ratio,arable_amount,resource_ratio,reason,production_method_choices=None,traits=None):
    """Work on a deep copy; failed preflight or merge never changes the caller."""
    from model import clone,scalar,block,setval,setlist,levels,integer,emit
    if source==target or source not in project.regions or target not in project.regions:raise ValueError('Choose two different existing regions.')
    if not reason.strip():raise ValueError('Explain the geographic move.')
    for value in [population_ratio,building_ratio,resource_ratio]:
        if not 0<=value<=1:raise ValueError('Allocation ratios must lie between 0 and 1.')
    selected={p.upper() for p in selected}
    n=project.regions[source][1];tn=project.regions[target][1]
    allps={p.upper() for p in n.get('provinces').values()};targetps={p.upper() for p in tn.get('provinces').values()}
    if not selected or not selected<allps:raise ValueError('The source region must retain at least one province.')
    if n.get('arable_land') is None or tn.get('arable_land') is None:raise ValueError('Only inhabited land regions may be moved.')
    for hub in ['city','farm','mine','wood','port','center_province']:
        if n.scalar(hub,'').upper() in selected:raise ValueError('The selected land contains the source '+hub+' hub. Choose a retained hub location before moving it.')
    amount=integer(arable_amount)
    if amount>int(n.scalar('arable_land')):raise ValueError('Moved arable land exceeds the source.')
    if n.scalar('subsistence_building')!=tn.scalar('subsistence_building'):raise ValueError('Source/target subsistence building types differ; decide the agricultural design explicitly first.')
    memo={};p=copy.deepcopy(project,memo)
    # Document.original uses object identities as keys; preserve those keys in the cloned transaction.
    for doc in p.docs.values():doc.original={id(memo[key]):value for key,value in doc.original.items()}
    parents,_=origins(p)
    sourceparents={parents.get(x) for x in allps}
    if len(sourceparents)!=1 or None in sourceparents:raise ValueError('Moving out of an already mixed original region needs per-origin allocations; the single-ratio form does not guess these.')
    # All country intersections preserve their owner; complete intersections move in full.
    moved={tag:ps&selected for tag,ps in p.owners[source].items() if ps&selected}
    source_before={tag:set(ps) for tag,ps in p.owners[source].items()}
    target_before={tag:set(ps) for tag,ps in p.owners[target].items()}
    fractions={tag:(1 if ps<=selected else population_ratio) for tag,ps in source_before.items() if ps&selected}
    bfractions={tag:(1 if ps<=selected else building_ratio) for tag,ps in source_before.items() if ps&selected}
    for tag,b in p.state_rows('buildings',source):
        if tag in moved and b.get('level') and not b.get('add_ownership') and bfractions[tag]>0:
            raise ValueError('Move unique buildings separately after reviewing their potential and locator: '+b.scalar('building'))
    # Unknown state-level directives or incompatible incorporation must not disappear.
    for _,_,node in p.states[source]:
        if any(c.key not in {'create_state','add_homeland','add_claim'} for c in node.children or []):raise ValueError('Source state history has directives requiring manual semantic review.')
    signatures={}
    for region in [source,target]:
        for _,_,node in p.states[region]:
            for state in node.all('create_state'):
                tag=state.scalar('country').removeprefix('c:')
                signature=emit(block('create_state',[clone(c) for c in state.children if c.key not in {'owned_provinces'}]))
                if region==source and tag not in moved:continue
                if tag in signatures and signatures[tag]!=signature:raise ValueError('Country '+tag+' has incompatible state history/incorporation in the destination.')
                signatures[tag]=signature
    before=p.totals();n=p.regions[source][1];tn=p.regions[target][1]
    colors=lambda xs:['"x'+x[1:].upper()+'"' for x in sorted(xs)]
    setlist(n,'provinces',colors(allps-selected));setlist(tn,'provinces',colors(targetps|selected))
    setval(n,'arable_land',int(n.scalar('arable_land'))-amount);setval(tn,'arable_land',int(tn.scalar('arable_land'))+amount)
    for field in ['arable_resources']:
        setlist(tn,field,sorted(set(tn.get(field).values() if tn.get(field) else [])|set(n.get(field).values() if n.get(field) else [])))
    if n.get('capped_resources'):
        if not tn.get('capped_resources'):tn.children.append(block('capped_resources',[]))
        for resource in n.get('capped_resources').children:
            count=int(resource.value);movedcount=scaled(count,resource_ratio);resource.value=str(count-movedcount)
            setval(tn.get('capped_resources'),resource.key,int(tn.get('capped_resources').scalar(resource.key,'0'))+movedcount)
    for resource in n.all('resource'):
        name=resource.scalar('type')
        matches=[x for x in tn.all('resource') if x.scalar('type')==name]
        counts={'amount','undiscovered_amount','discovered_amount','depleted_amount'}
        def sig(r):return emit(block('resource',[clone(c) for c in r.children if c.key not in counts]))
        if len(matches)>1 or (matches and sig(matches[0])!=sig(resource)):raise ValueError('Incompatible discoverable resource definition: '+str(name))
        dest=matches[0] if matches else clone(resource)
        if not matches:
            for k in counts:
                if dest.get(k):setval(dest,k,0)
            tn.children.append(dest)
        for k in counts:
            if resource.get(k):
                value=int(resource.scalar(k));nv=scaled(value,resource_ratio);setval(resource,k,value-nv);setval(dest,k,int(dest.scalar(k,'0'))+nv)
    for field in ['impassable','prime_land']:
        old=set(x.upper() for x in n.get(field).values()) if n.get(field) else set()
        transfer=old&selected
        if n.get(field):setlist(n,field,colors(old-selected))
        if transfer:setlist(tn,field,colors(set(x.upper() for x in tn.get(field).values())|transfer) if tn.get(field) else colors(transfer))
    if traits is not None:
        unknown=set(traits)-p.traits
        if unknown:raise ValueError('Unknown state traits.')
        setlist(tn,'traits',traits)
    # Create/extend country intersections and copy only known regional ancestry directives.
    destroot=p._history_region('states',target)
    for _,_,node in p.states[source]:
        for directive in node.children or []:
            if directive.key in {'add_homeland','add_claim'} and not any(emit(x)==emit(directive) for _,_,dn in p.states[target] for x in dn.children or []):
                destroot.children.append(clone(directive))
        for state in list(node.all('create_state')):
            tag=state.scalar('country').removeprefix('c:')
            if tag not in moved:continue
            candidates=[cs for _,_,dn in p.states[target] for cs in dn.all('create_state') if cs.scalar('country')=='c:'+tag]
            if candidates:deststate=candidates[0]
            else:deststate=clone(state);destroot.children.append(deststate)
            setlist(deststate,'owned_provinces',colors(target_before.get(tag,set())|moved[tag]))
            remain=source_before[tag]-selected
            if remain:setlist(state,'owned_provinces',colors(remain))
            else:node.children.remove(state)
    for kind in ['pops','buildings']:
        destroot=p._history_region(kind,target)
        for _,_,node in p.__dict__[kind][source]:
            for state in list(node.children or []):
                if not state.key or not state.key.startswith('region_state:'):continue
                tag=state.key.split(':')[1]
                if tag not in moved:continue
                fraction=fractions[tag] if kind=='pops' else bfractions[tag]
                targets=[st for _,_,dn in p.__dict__[kind][target] for st in dn.children or [] if st.key==state.key]
                if targets:deststate=targets[0]
                else:deststate=block(state.key,[]);destroot.children.append(deststate)
                for item in list(state.children or []):
                    expected='create_pop' if kind=='pops' else 'create_building'
                    if item.key!=expected:raise ValueError('Unknown '+kind+' history directive requires review.')
                    dest=clone(item)
                    if kind=='pops':
                        count=int(item.scalar('size'));nv=scaled(count,fraction);setval(item,'size',count-nv);setval(dest,'size',nv)
                        if nv:deststate.children.append(dest)
                        if count==nv:state.children.remove(item)
                    else:
                        if item.get('level'):continue
                        divide_building_ownership(item,dest,fraction)
                        for own in dest.walk():
                            if own.scalar('region')==source and own.scalar('country')=='c:'+tag:setval(own,'region','"'+target+'"')
                        if levels(dest):deststate.children.append(dest)
                        if not levels(item):state.children.remove(item)
                if not state.children:node.children.remove(state)
    choices=production_method_choices or {}
    for kind,selected_pms in choices.items():
        available={tuple(sorted(b.get('activate_production_methods').values() if b.get('activate_production_methods') else [])) for region in [source,target] for tag,b in p.state_rows('buildings',region) if b.scalar('building')==kind}
        if tuple(sorted(selected_pms)) not in available:raise ValueError('Choose an existing complete production-method set for '+kind)
        p.validate_pms(kind,selected_pms)
    for _,_,node in p.buildings[target]:
        for state in node.children or []:
            if state.key and state.key.startswith('region_state:'):
                state.children=merge_buildings(state.children,choices)
    # Linked unit counts follow explicitly chosen building share; hq remains with formation.
    for d in p.docs.values():
        if '/military_formations/' not in d.rel:continue
        for wrapper in d.tree.children:
            for country in wrapper.children or []:
                tag=country.key.removeprefix('c:') if country.key else ''
                for formation in country.all('create_military_formation'):
                    for unit in list(formation.all('combat_unit')+formation.all('ship')):
                        if unit.scalar('state_region')!='s:'+source or tag not in moved:continue
                        count=int(unit.scalar('count'));nv=scaled(count,bfractions[tag]);newunit=clone(unit);setval(newunit,'count',nv);setval(newunit,'state_region','s:'+target)
                        if nv:formation.children.append(newunit)
                        if count==nv:formation.children.remove(unit)
                        else:setval(unit,'count',count-nv)
    p.reindex()
    for region in [source,target]:
        old=capacity_overages(project,region);new=capacity_overages(p,region)
        worsened={k:v for k,v in new.items() if v>old.get(k,0)}
        if worsened:raise ValueError('The allocation exceeds existing land/resource capacity in '+region+': '+str(worsened)+'. Adjust the resource/land or building allocation.')
    for tag in moved:
        if source_before[tag]<=selected:
            for records in p.buildings.values():
                for _,_,node in records:
                    for own in node.walk():
                        if own.scalar('region')==source and own.scalar('country')=='c:'+tag:setval(own,'region','"'+target+'"')
            if p.country_defs[tag][1].scalar('capital')==source:setval(p.country_defs[tag][1],'capital',target)
            for d in p.docs.values():
                if '/history/countries/' not in d.rel:continue
                for wrapper in d.tree.children:
                    for country in wrapper.children or []:
                        if country.key=='c:'+tag:
                            for cap in country.all('set_market_capital'):
                                if cap.value==source:cap.value=target
    assert p.totals()==before,(before,p.totals())
    p.actions.append({'op':'move_provinces','source':source,'target':target,'provinces':sorted(selected),'population_ratio':population_ratio,'building_ratio':building_ratio,'arable_amount':amount,'resource_ratio':resource_ratio,'reason':reason,'original_geography':'per-pop-row fixed parent retained','country_intersections':{tag:len(ps) for tag,ps in moved.items()}})
    p.notes.append('Province move retains owner intersections and source hubs; target traits are explicit. Review source/target political references, market geography, resource suitability and native transportation before game approval.')
    project.__dict__.clear();project.__dict__.update(p.__dict__)
