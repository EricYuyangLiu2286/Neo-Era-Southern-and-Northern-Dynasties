"""Extract real Japan/Lin/player/sea native state, never infer a game pass.

Reuses the established ordered save readers. Output is evidence, not simulation.
"""
from pathlib import Path
from decimal import Decimal
import argparse, collections, hashlib, json, re, sys
sys.dont_write_bytecode = True
from save_market_network import sections, records, scalar
from audit_politics_phi_native import node, variables, nested, dead_ids
from pdx import parse

WORK = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
TAGS={'USM','JAP','JTK','JIM','YN1','PHI','CNE'}
REGIONS={'STATE_KANTO','STATE_KYOTO','STATE_KANSAI','STATE_CHUGOKU','STATE_TOHOKU','STATE_TOKAI','STATE_HOKUSHINETSU','STATE_HOKKAIDO','STATE_KYUSHU','STATE_SHIKOKU','STATE_HAWAII','STATE_RYUKYU_ISLANDS'}

def ordered(n):
    if n is None:return None
    if n.children is None:return n.value
    return [{'key':c.key,'op':c.op,'value':ordered(c)} for c in n.children]

def extract(source):
    s0=source.stat();raw=source.read_bytes();s1=source.stat()
    assert (s0.st_size,s0.st_mtime_ns)==(s1.st_size,s1.st_mtime_ns),'Save is still changing'
    assert raw.startswith(b'SAV0100'),'Only verified uncompressed native text format is supported'
    text=raw.decode('utf-8-sig');sec=sections(text)
    cb=records(sec['country_manager']);tags={i:scalar(b,'definition') for i,b in cb.items()}
    country_dead=dead_ids(sec['country_manager']);countries=[]
    for ident,body in cb.items():
        if tags[ident] not in TAGS:continue
        n=node(body);v=variables(n.get('variables'))
        countries.append({'id':ident,'tag':tags[ident],'raw_dead':n.scalar('dead'),'death_date':country_dead.get(ident),
            'capital':n.scalar('capital'),'market':n.scalar('market'),'market_capital':n.scalar('market_capital'),
            'primary_cultures':ordered(n.get('primary_cultures')),'religion':n.scalar('religion'),
            'ruler':n.scalar('ruler'),'heir':n.scalar('heir'),
            'variables':{k:v for k,v in v.items() if k.startswith(('nesnd_japan','nesnd_lin','tag_WUU','usm_opposition','nesnd_restoration','nesnd_south','nesnd_ming'))}})
    char_records=records(sec['character_manager']);char_dead=dead_ids(sec['character_manager']);people=[]
    for ident,body in char_records.items():
        template=scalar(body,'template');v=variables(nested(body,'variables'))
        if template!='USM_lin_hanhan' and not any(k in v for k in ['house_toyotomi','house_tokugawa','house_yamato']):continue
        n=node(body)
        people.append({'id':ident,'template':template,'owner_id':n.scalar('country'),'owner_tag':tags.get(n.scalar('country')),
            'first_name':n.scalar('first_name'),'last_name':n.scalar('last_name'),'raw_dead':n.scalar('dead'),
            'death_date':char_dead.get(ident) or n.scalar('death_date'),'roles':n.get('character_roles').values() if n.get('character_roles') else [],
            'flags':n.get('flags').values() if n.get('flags') else [],'variables':v})
    players=[{'id':i,'country_id':scalar(b,'country'),'country_tag':tags.get(scalar(b,'country'))}
             for i,b in records(sec['player_manager']).items()]
    region_tags={i:scalar(b,'template') for i,b in records(sec['state_region_manager']).items()}
    state_bodies=records(sec['states']);states={};state_dead=dead_ids(sec['states'])
    for ident,body in state_bodies.items():
        region=scalar(body,'region');region_name=region if region and region.startswith('STATE_') else region_tags.get(region)
        tag=tags.get(scalar(body,'country'));v=variables(nested(body,'variables'))
        if region_name not in REGIONS and tag not in {'JAP','JTK','JIM'} and 'nesnd_japan_before_annex' not in v:continue
        states[ident]={'id':ident,'region_native_field':region,'region':region_name,'country_id':scalar(body,'country'),
           'country_tag':tag,'controller_id':scalar(body,'controller'),'controller_tag':tags.get(scalar(body,'controller')),
           'raw_dead':scalar(body,'dead'),'death_date':state_dead.get(ident),'population':0,'building_levels':{},
           'infrastructure':scalar(body,'infrastructure'),'infrastructure_usage':scalar(body,'infrastructure_usage'),
           'native_market_access_cache':scalar(body,'market_access'),'variables':{k:v for k,v in v.items() if k.startswith('nesnd_japan')}}
    for ident,body in records(sec['pops']).items():
        state=states.get(scalar(body,'location'))
        if state is not None:state['population']+=int(scalar(body,'workforce','0'))+int(scalar(body,'dependents','0'))
    bdead=dead_ids(sec['building_manager'])
    for ident,body in records(sec['building_manager']).items():
        state=states.get(scalar(body,'state'))
        if state is None or ident in bdead or scalar(body,'dead','no')=='yes':continue
        kind=scalar(body,'building');levels=Decimal(scalar(body,'levels','0'))
        state['building_levels'][kind]=str(Decimal(state['building_levels'].get(kind,'0'))+levels)
    pacts=[]
    for ident,body in records(sec['pacts']).items():
        n=node(body);targets=n.get('targets')
        if not targets:continue
        first,second=targets.scalar('first'),targets.scalar('second')
        if tags.get(first) in {'JAP','JTK','JIM'} or tags.get(second) in {'JAP','JTK','JIM'}:
            pacts.append({'id':ident,'action':n.scalar('action'),'first_id':first,'first_tag':tags.get(first),'second_id':second,'second_tag':tags.get(second),'raw':ordered(n)})
    globalvars=variables(parse(sec['variables']).get('variables'))
    date=re.search(r'^date=(\S+)',text,re.M)
    return {'source':str(source),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'date':date[1] if date else None,
       'engine_verified':False,'evidence_kind':'real native save extraction only; scenario outcome needs run/UI/entry proof',
       'countries':countries,'people':people,'players':players,'japan_related_states':states,'japan_related_pacts':pacts,
       'global_variables':{k:v for k,v in globalvars.items() if k.startswith(('nesnd_japan','nesnd_south','usm_civilwar'))},
       'all_character_ids':sorted(char_records,key=int),
       'limits':['Only actual serialized fields are reported.','Native market_access is an opaque cached count, not a displayed percentage.','Country/tag re-creation may change IDs; players must be verified against player_manager and UI.','Dead-object registry is checked alongside raw fields.','Population may change with natural time; compare dates before making conservation assertions.','Province-level boundaries, full laws/ownership/military and fleet arrivals need separate inspection.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--save',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--before',type=Path)
    a=p.parse_args();out=a.out.resolve()
    if not out.is_relative_to(WORK.resolve()) or out.exists():raise ValueError('Use a new evidence path under WORK')
    report=extract(a.save)
    if a.before:
        before=json.loads(a.before.read_text(encoding='utf-8-sig'))
        report['comparison']={'before_report':str(a.before),'before_save_sha256':before['sha256'],
          'same_date':before['date']==report['date'],'players_before':before['players'],'players_after':report['players'],
          'new_character_ids':sorted(set(report['all_character_ids'])-set(before['all_character_ids']),key=int),
          'missing_character_ids':sorted(set(before['all_character_ids'])-set(report['all_character_ids']),key=int),
          'lin_before':[x for x in before['people'] if x['template']=='USM_lin_hanhan'],
          'lin_after':[x for x in report['people'] if x['template']=='USM_lin_hanhan']}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'out':str(out),'date':report['date'],'players':report['players'],'selected_people':len(report['people']),'selected_states':len(report['japan_related_states']),'engine_verified':False},ensure_ascii=False))

if __name__=='__main__':main()
