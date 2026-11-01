"""Thin ordered-AST closure supplement for global PM groups and map resources.
The existing audit.py checks history PM assignment. This checks references even
for buildings/PMs not selected in initial history. No production simulation.
"""
from pathlib import Path
import hashlib,sys
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read,effective_files,basekey
from catalog import GAME

def audit(candidate):
    roots=[GAME,Path(candidate)];sources={};registries={};providers={};errors=[];review=[]
    for folder in ['buildings','production_method_groups','production_methods','state_traits']:
        registry={};origin={}
        for path in effective_files(roots,'common/'+folder):
            text,tree=read(path);sources[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
            for n in tree.children:
                if not n.key or n.children is None:continue
                key=basekey(n.key);origin.setdefault(key,[]).append({'path':str(path),'line':text.count('\n',0,n.start)+1,'operator':n.key})
                registry[key]=n
        registries[folder]=registry;providers[folder]=origin
    for key,n in registries['buildings'].items():
        gs=n.get('production_method_groups')
        for group in gs.values() if gs else []:
            if group not in registries['production_method_groups']:
                errors.append({'kind':'unknown_building_pm_group','building':key,'group':group,'source':providers['buildings'][key]})
    for key,n in registries['production_method_groups'].items():
        ps=n.get('production_methods')
        for pm in ps.values() if ps else []:
            if pm not in registries['production_methods']:
                errors.append({'kind':'unknown_group_pm','group':key,'pm':pm,'source':providers['production_method_groups'][key]})
    for path in effective_files(roots,'map_data/state_regions'):
        text,tree=read(path);sources[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for region in tree.children:
            if not region.key or region.children is None:continue
            location={'path':str(path),'line':text.count('\n',0,region.start)+1,'region':basekey(region.key)}
            traits=region.get('traits')
            for trait in traits.values() if traits else []:
                if trait not in registries['state_traits']:errors.append({'kind':'unknown_region_trait','trait':trait,**location})
            arable=region.get('arable_resources')
            building_refs=[('arable_resources',x) for x in arable.values()] if arable else []
            capped=region.get('capped_resources')
            if capped:building_refs.extend(('capped_resources',x.key) for x in capped.children if x.key)
            for block in region.all('resource'):
                if block.scalar('type'):building_refs.append(('resource.type',block.scalar('type')))
            for kind,building in building_refs:
                if building not in registries['buildings']:errors.append({'kind':'unknown_region_resource_building','field':kind,'building':building,**location})
    for folder,items in providers.items():
        for key,ps in items.items():
            # Keep all provider provenance. Replacement syntax and file mounting
            # differ by database; warn rather than claim this adapter models it.
            if len(ps)>1:review.append({'kind':'multiple_definition_providers','folder':folder,'key':key,'providers':ps})
    return {'hard_errors':errors,'review_findings':review,'counts':{k:len(v) for k,v in registries.items()},
            'accessed_source_sha256':sources,'engine_verified':False,
            'limits':['All providers retained; effective file override plus top-level basekey resolution is a conservative lookup, not a complete engine override interpreter.',
                      'Does not simulate staffing, qualifications, input/output prices, throughput, arable capacity or AI construction.']}
