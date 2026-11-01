"""Apply narrowly fingerprinted native evidence to audit.py's history findings.
No history edits, no rebasing, no summing overwritten ownership entries.
"""
from pathlib import Path
from collections import Counter
import hashlib,json
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');E=W/'plans/two-empires/evidence'

def classify(candidate,findings):
    candidate=Path(candidate).resolve();cache={}
    def sha(p):
        p=Path(p)
        if p not in cache:cache[p]=hashlib.sha256(p.read_bytes()).hexdigest()
        return cache[p]
    def evidence(name):
        path=E/name
        if not path.exists():return None,{'path':str(path),'valid':False,'reason':'No native review'}
        r=json.loads(path.read_text('utf8'));old=Path(r.get('candidate',r.get('mod',''))).resolve();errors=[]
        for raw,expected in r.get('source_sha256',{}).items():
            p=Path(raw)
            target=candidate/p.relative_to(old) if p.is_relative_to(old) else p
            if not target.is_file() or sha(target)!=expected:errors.append(str(target))
        save=Path(r['save'])
        if not save.is_file() or sha(save)!=r['save_sha256']:errors.append('native save drifted')
        return r,{'path':str(path),'sha256':sha(path),'valid':not errors,'mismatches':errors,
                  'boundary':'Reuse only initial-history semantics, not a claim that this new candidate already ran'}
    owners,om=evidence('province-overlap-e1-classification.json')
    investors,im=evidence('four-history-investors-e1-native-review.json')
    approved=Counter();design=Counter();design_notes=[]
    if owners and om['valid']:
        assert owners['summary']['all_native_counts_match_ordered_model'] and owners['summary']['numeric_owner_collisions']==0 and owners['summary']['rle_vs_direct_mismatches']==0
        for row in owners['rows']:
            target=design if row['classification'] in ['mod_explicit_territory_intent_conflict_requires_design','author_ordered_overlap_nonblocking_review'] else approved
            for item in row['source']['overlaps']:target[(row['region'],item['later'],item['province'].upper())]+=1
            if target is design:design_notes.append({'region':row['region'],'classification':'author_ordered_overlap_nonblocking_review',
                'native_counts_match':row['ordered_model_country_counts_match_native'],'source':row['source']['source'],'source_line':row['source']['line']})
    investor_keys=set()
    if investors and im['valid']:
        for row in investors['results']:
            if row['classification']=='inherited_same_block_overwrite_confirmed_native' and row['source_same_as_current_GAME'] and row['source_same_as_author'] and row['source_same_as_frozen_E1']:
                investor_keys.add((row['region'],row['tag'],row['building']))
    rows=[];hard=[];unreviewed_semantics=[]
    for item in findings:
        group='UNREVIEWED_HARD';proof=None
        if item['kind']=='duplicate_province_owner':
            key=(item['region'],item['tag'],item['province'].upper())
            if approved[key]>0:approved[key]-=1;group='REVIEWED_NATIVE_ORDERED_OVERWRITE';proof=om
            elif design[key]>0:design[key]-=1;group='REVIEWED_AUTHOR_ORDERED_OVERWRITE_NONBLOCKING';proof=om
        elif item['kind']=='duplicate_building_investor' and (item['region'],item['tag'],item['building']) in investor_keys:
            group='REVIEWED_SAME_OWNER_OVERWRITE_NOT_ADDITIVE';proof=im
        row={'classification':group,'finding':item,'evidence':proof};rows.append(row)
        if group=='UNREVIEWED_HARD':
            if item['kind'] in ['duplicate_province_owner','duplicate_building_investor']:
                row['classification']='UNREVIEWED_ORDERED_HISTORY_SEMANTICS';unreviewed_semantics.append(row)
            else:hard.append(row)
    return {'classified_findings':rows,'counts':dict(Counter(r['classification'] for r in rows)),
            'unreviewed_hard':hard,'unreviewed_semantics':unreviewed_semantics,'author_design_notes':design_notes,
            'evidence_checks':{'owners':om,'investors':im},'engine_verified':False,
            'limits':['Reviewed ordered overwrites are not duplicated runtime land. Four author-specific outcomes are preserved and nonblocking; lack of further lore research is not a newly invented release condition.',
                      'Four duplicate investors resolve to actual 3/2/1/1 levels, total7; summing15 would add8 phantom levels.',
                      'A changed source witness or native file rejects reuse and leaves the finding unreviewed.']}
