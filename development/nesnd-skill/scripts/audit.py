"""Audit the effective GAME+MOD data graph, preserving repeated blocks."""
import argparse, json, re
from collections import defaultdict, Counter
from pathlib import Path
from catalog import GAME,MOD,WORK,version
from pdx import read,effective_files,basekey

def initial_building_levels(block):
    """Count history levels, correcting engine-proven repeated building owners.

    In one add_ownership block, the last entry for the same type/country/region
    identity wins (1.13.11 native-save regression: duplicate-history-audit.json).
    Separate add_ownership blocks and country/company owners retain the previous
    accounting behavior; those are not certified by the five building examples.
    """
    count=sum(int(float(n.value)) for n in block.walk() if n.key=='levels')
    for own in block.all('add_ownership'):
        last={}
        for owner in own.all('building'):
            identity=(owner.scalar('type'),owner.scalar('country'),owner.scalar('region'))
            if identity in last: count-=last[identity]
            last[identity]=int(float(owner.scalar('levels','0')))
    return count if count else int(float(block.scalar('level','0')))

def audit(mod=MOD):
    roots=[GAME,mod]; issues=[]; regions={}; states=defaultdict(dict); pops=defaultdict(int); buildings=defaultdict(int)
    def issue(kind,**detail): issues.append({'kind':kind,**detail})
    for p in mod.rglob('*.txt'):
        try: read(p)
        except (ValueError,UnicodeError) as e: issue('parse',file=str(p),detail=str(e))
    countries=set()
    for p in effective_files(roots,'common/country_definitions'):
        _,tree=read(p)
        countries.update(basekey(n.key) for n in tree.children if n.children is not None)
    # Validate the actual building -> PM group -> PM chain, not just spellings.
    definitions={}
    for folder in ['buildings','production_method_groups','production_methods']:
        entries={}
        for p in effective_files(roots,'common/'+folder):
            _,tree=read(p)
            for n in tree.children:
                if n.key and n.children is not None: entries[basekey(n.key)]=n
        definitions[folder]=entries
    allowed_pms={}
    for kind,n in definitions['buildings'].items():
        groups=n.get('production_method_groups');allowed=set()
        for g in groups.values() if groups else []:
            group=definitions['production_method_groups'].get(g)
            if group and group.get('production_methods'):allowed.update(group.get('production_methods').values())
        allowed_pms[kind]=allowed
    for p in mod.glob('common/history/population/*.txt'):
        _,tree=read(p);expected=re.match(r'([A-Z0-9]{3})(?:[ ._-]|$)',p.name,re.I)
        actual=[n.key[2:] for n in tree.walk() if n.key and re.fullmatch(r'c:[A-Z0-9]{3}',n.key)]
        if expected and actual and expected[1].upper() not in actual:
            issue('population_filename_scope_mismatch_review',file=str(p),expected_from_filename=expected[1].upper(),actual_scopes=actual)
    owners={}; ids={}
    for p in effective_files(roots,'map_data/state_regions'):
        _,tree=read(p)
        for n in tree.children:
            if n.children is None: continue
            key=basekey(n.key)
            if key in regions: issue('duplicate_region',region=key,file=str(p))
            provinces=n.get('provinces').values() if n.get('provinces') else []
            ps={s.upper() for s in provinces}
            regions[key]={'file':str(p),'node':n,'provinces':ps}
            ident=n.scalar('id')
            if ident in ids: issue('duplicate_region_id',region=key,other=ids[ident],id=ident)
            ids[ident]=key
            for prov in ps:
                if prov in owners: issue('duplicate_province_region',province=prov,region=key,other=owners[prov])
                owners[prov]=key
            for hub in ['city','farm','mine','wood','port','center_province']:
                val=n.scalar(hub)
                if val and val.upper() not in ps: issue('hub_outside_region',region=key,hub=hub,province=val)
    for p in effective_files(roots,'common/history/states'):
        _,tree=read(p)
        for wrapper in tree.children:
            if wrapper.key!='STATES': continue
            for n in wrapper.children:
                reg=n.key.removeprefix('s:')
                if reg not in regions: issue('unknown_history_region',file=str(p),region=reg);continue
                used=set()
                for cs in n.all('create_state'):
                    tag=cs.scalar('country','').removeprefix('c:')
                    if tag not in countries: issue('unknown_state_country',region=reg,tag=tag)
                    op=cs.get('owned_provinces')
                    ps={s.upper() for s in op.values()} if op else set(regions[reg]['provinces'])
                    for v in ps-regions[reg]['provinces']:issue('owned_province_outside_region',region=reg,tag=tag,province=v,actual_region=owners.get(v))
                    for v in ps & used: issue('duplicate_province_owner',region=reg,tag=tag,province=v)
                    if tag in states[reg]: issue('duplicate_country_state',region=reg,tag=tag)
                    states[reg][tag]=ps; used|=ps
                if n.all('create_state'):
                    for v in regions[reg]['provinces']-used: issue('unowned_province',region=reg,province=v)
    for kind in ['pops','buildings']:
        for p in effective_files(roots,f'common/history/{kind}'):
            _,tree=read(p)
            for wrapper in tree.children:
                for region in wrapper.children or []:
                    reg=region.key.removeprefix('s:')
                    for state in region.children or []:
                        if not state.key or not state.key.startswith('region_state:'):continue
                        tag=state.key.split(':',1)[1]
                        if tag not in states.get(reg,{}): issue('orphan_'+kind,region=reg,tag=tag,file=str(p))
                        for block in state.children or []:
                            if block.key=='create_pop':pops[(reg,tag)]+=int(float(block.scalar('size','0')))
                            elif block.key=='create_building':
                                kind=block.scalar('building');pms=block.get('activate_production_methods')
                                if kind not in definitions['buildings']:
                                    issue('unknown_building_type',file=str(p),region=reg,tag=tag,building=kind)
                                for pm in pms.values() if pms else []:
                                    if pm not in definitions['production_methods']:
                                        issue('unknown_production_method',file=str(p),region=reg,tag=tag,building=kind,pm=pm)
                                    elif pm not in allowed_pms.get(kind,set()):
                                        issue('production_method_wrong_building_group',file=str(p),region=reg,tag=tag,building=kind,pm=pm)
                                investors=set()
                                for own in block.all('add_ownership'):
                                    for owner in own.all('building'):
                                        identity=(owner.scalar('type'),owner.scalar('country'),owner.scalar('region'))
                                        if identity in investors: issue('duplicate_building_investor',file=str(p),region=reg,tag=tag,building=block.scalar('building'),investor=identity)
                                        investors.add(identity)
                                count=initial_building_levels(block)
                                buildings[(reg,tag)]+=count
                                for own in block.all('add_ownership'):
                                    for owner in own.children or []:
                                        oreg=owner.scalar('region'); otag=owner.scalar('country','').removeprefix('c:')
                                        if oreg and otag and otag not in states.get(oreg,{}):issue('orphan_building_owner',file=str(p),region=reg,tag=tag,owner_region=oreg,owner_tag=otag)
    strategic=defaultdict(list)
    for p in effective_files(roots,'common/strategic_regions'):
        _,tree=read(p)
        for n in tree.children:
            ss=n.get('states')
            if ss:
                for reg in ss.values():strategic[reg].append(n.key)
    for reg,data in regions.items():
        if data['node'].get('arable_land') and len(strategic.get(reg,[]))!=1: issue('strategic_region_membership',region=reg,groups=strategic.get(reg,[]))
    summary={'version':version(),'mod':str(mod),'regions':len(regions),'states':sum(map(len,states.values())),'total_population':sum(pops.values()),'building_levels':sum(buildings.values()),'issues':dict(Counter(x['kind'] for x in issues))}
    return {'summary':summary,'issues':issues,'population_by_state':{f'{r}:{t}':v for (r,t),v in pops.items()},'buildings_by_state':{f'{r}:{t}':v for (r,t),v in buildings.items()},'territory':{r:{t:sorted(ps) for t,ps in tags.items()} for r,tags in states.items()}}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mod',type=Path,default=MOD);ap.add_argument('--out',default='audit-current.json');args=ap.parse_args()
    report=audit(args.mod);dest=WORK/'reports'/args.out;dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8'); print(json.dumps(report['summary'],ensure_ascii=False)); print(dest)
