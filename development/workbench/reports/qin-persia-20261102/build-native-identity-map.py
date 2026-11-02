"""Read native population pairs, align geography by provinces; never area-scale people."""
from pathlib import Path
import sys, json, collections, hashlib, re, math
sys.path.insert(0, 'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse, basekey
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
R=W/'reports/qin-persia-20261102'
fingerprints={}
def read(p):
    fingerprints[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    return p.read_text('utf-8-sig')
def files(rel,mod=False):
    result={str(p.relative_to(G/rel)):p for p in (G/rel).rglob('*.txt')}
    if mod:result.update({str(p.relative_to(M/rel)):p for p in (M/rel).rglob('*.txt')})
    return [result[k] for k in sorted(result)]
def db(rel,mod=False):
    result={}
    for p in files(rel,mod):
        text=read(p)
        for n in parse(text).children:
            result[basekey(n.key)]=(n,str(p),text[:n.start].count('\n')+1,text)
    return result
def ownership(mod=False):
    result=[]
    for p in files('common/history/states',mod):
        text=read(p);states=parse(text).get('STATES')
        if states:
            for s in states.children:
                for n in s.all('create_state'):
                    result.append({'region':s.key[2:],'owner':n.scalar('country').split(':')[-1],
                        'provinces':set(n.get('owned_provinces').values()) if n.get('owned_provinces') else set(),
                        'source':str(p),'line':text[:n.start].count('\n')+1})
    return result
cult=db('common/cultures');effective_cult=db('common/cultures',True)
poprows=[]
for p in files('common/history/pops'):
    text=read(p);pops=parse(text).get('POPS')
    if not pops:continue
    for region in pops.children:
        for state in region.children or []:
            if not state.key.startswith('region_state:'):continue
            for n in state.all('create_pop'):
                c=n.scalar('culture');cn,cp,cl,ct=cult[c]
                religion=n.scalar('religion') or cn.scalar('religion')
                poprows.append({'region':region.key[2:],'owner':state.key.split(':')[-1],
                    'culture':c,'religion':religion,'religion_explicit':n.scalar('religion') is not None,
                    'religion_default_source':None if n.scalar('religion') else {'file':cp,'line':ct[:cn.get('religion').start].count('\n')+1},
                    'size':int(n.scalar('size','0')),'source':str(p),'line':text[:n.start].count('\n')+1})
assert all(x['religion'] for x in poprows)
native_by_state=collections.defaultdict(list)
for x in poprows:native_by_state[x['region'],x['owner']].append(x)
native_owners=ownership();qe1=[x for x in ownership(True) if x['owner']=='QE1']
previous=json.loads((W/'reports/rules-poland-qin-20261102/qin-culture-inventory.json').read_text('utf-8'))
names={k:v['name'] for k,v in previous['states'].items()}
allmap=[]
for current in sorted(qe1,key=lambda x:x['region']):
    references=[];pairs=collections.Counter();sources=[]
    for original in native_owners:
        overlap=current['provinces'] & original['provinces']
        if not overlap:continue
        full=overlap==original['provinces']
        ref={'native_region':original['region'],'native_owner':original['owner'],
            'matched_provinces':len(overlap),'native_substate_provinces':len(original['provinces']),
            'full_native_substate':full,'native_ownership_source':original['source'],'native_ownership_line':original['line']}
        references.append(ref)
        for row in native_by_state[original['region'],original['owner']]:
            pairs[row['culture'],row['religion']]+=row['size'];sources.append(row)
    pairrows=[]
    for (c,rel),n in pairs.most_common():
        cn=cult[c][0];en=effective_cult[c][0]
        ntrad=cn.get('traditions').values() if cn.get('traditions') else []
        etrad=en.get('traditions').values() if en.get('traditions') else []
        pairrows.append({'culture':c,'religion':rel,'native_reference_population':n,
            'native_sinosphere':'tradition_sinosphere' in ntrad,'effective_sinosphere':'tradition_sinosphere' in etrad})
    eligible=[x for x in pairrows if not x['effective_sinosphere']]
    total=sum(x['native_reference_population'] for x in eligible)
    divisor=math.gcd(*(x['native_reference_population'] for x in eligible)) if eligible else 1
    for x in eligible:
        x['weight']=x['native_reference_population']//divisor
        x['weight_fraction']=x['native_reference_population']/total if total else 0
    currentstats=previous['states'].get(current['region'],{})
    allmap.append({'region':current['region'],'current_name':names.get(current['region'],current['region']),
        'current_ce_xiyu_starting_size':currentstats.get('cultures',{}).get('ce_xiyu',0),
        'current_ownership_source':current['source'],'current_ownership_line':current['line'],
        'native_references':references,
        'coverage_note':'All intersected native substates covered in full; reference counts have exact footprint' if all(r['full_native_substate'] for r in references) else 'At least one native substate only partly intersected. Whole-substate pairs are geographic background; weights are a design prior, NOT local headcounts or area-scaled allocation.',
        'pairs':pairrows,'eligible_non_sinosphere_pairs':eligible,'source_pop_rows':sources})
countries=db('common/country_definitions',True);creation=db('common/country_creation',True)
tags=['BUK','UZB','KHI','KOK','TRC','TRM','KAZ','KYR','TJI','XIN','AFG','TIB','MGL','TUV','KAS','KAL','PER','QE1']
countryrows=[]
for tag in tags:
    if tag not in countries:countryrows.append({'tag':tag,'exists_definition':False});continue
    n,p,line,t=countries[tag]
    cr=creation.get(tag)
    countryrows.append({'tag':tag,'exists_definition':True,'type':n.scalar('country_type'),'capital':n.scalar('capital'),
        'cultures':n.get('cultures').values() if n.get('cultures') else [],'definition_source':p,'definition_line':line,
        'releasable_states':cr[0].get('states').values() if cr and cr[0].get('states') else None,
        'releasable_provinces':cr[0].get('provinces').values() if cr and cr[0].get('provinces') else None,
        'country_creation_source':cr[1] if cr else None,'country_creation_line':cr[2] if cr else None,
        'currently_owns_state':any(x['owner']==tag for x in ownership(True))})
partition={
    'QE1':['STATE_ILI'],
    'XIN':['STATE_DZUNGARIA','STATE_JETISY','STATE_TIANSHAN','STATE_WESTERN_TIANSHAN'],
    'UZB':['STATE_FERGANA'],'BUK':['STATE_UZBEKIA'],'KHI':['STATE_KHIVA'],
    'TRC':['STATE_TURKMENIA','STATE_MERZ'],'KYR':['STATE_KIRGHIZIA'],'TJI':['STATE_TAJIKISTAN'],
    'KAZ':['STATE_AKTOBE','STATE_CHELYABINSK','STATE_URALSK','STATE_SAMARA','STATE_SEMIRECHE','STATE_SYRDARYA'],
    'AFG':['STATE_BALKH','STATE_CENTRAL_HIGHLANDS','STATE_HERAT','STATE_KABUL','STATE_KANDAHAR','STATE_PASHTUNISTAN','STATE_QUETTA'],
    'KAL':['STATE_BALUCHISTAN','STATE_NORTHERN_BALUCHISTAN'],'PER':['STATE_SISTAN'],
    'TIB':['STATE_LHASA','STATE_NGARI','STATE_QINGHAI','STATE_EASTERN_HIMALAYAS'],
    'KAS':['STATE_KASHMIR'],'MGL':['STATE_ALTAI','STATE_ULIASTAI'],'TUV':['STATE_TUVA']}
flat=[x for states in partition.values() for x in states]
assert len(flat)==len(set(flat))==36 and set(flat)=={x['region'] for x in qe1}
out={'game_version':'1.13.11','build':'24799966','basis':'native history pairs + province overlap; native religion omitted => native culture religion default',
    'game_launched':False,'mapping_is_gameplay_proposal':True,'warning':'Weights sample a native regional identity pair. They are not proof of genealogy of current ce_xiyu pops.',
    'states':allmap,'native_country_candidates':countryrows,
    'exclusive_breakup_partition_proposal':partition,
    'partition_note':'Design proposal only, not native borders or genealogical fact. Transfer only QE1-owned states; retain STATE_ILI; existing KAL/PER/MGL are recipients, not newly spawned tags. Do not alter third-party provinces or automatically change subject relations.',
    'sha256':fingerprints}
(R/'native-identity-map.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('states',len(allmap),'pairs',sum(len(x['pairs']) for x in allmap),'countries',len(countryrows))
for x in allmap:
    top=x['eligible_non_sinosphere_pairs'][:3]
    print(x['region'],x['current_name'],'; '.join(f"{p['culture']}+{p['religion']} {p['weight_fraction']:.1%}" for p in top),'PARTIAL' if any(not y['full_native_substate'] for y in x['native_references']) else 'FULL')
for x in countryrows:print(x['tag'],x.get('capital'),x.get('releasable_states'),x.get('currently_owns_state'))
