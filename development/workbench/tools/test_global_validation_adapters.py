"""Local regressions for actual nullable Tiger records and narrowly bound history evidence."""
from pathlib import Path
import hashlib,json,sys
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');E=W/'plans/two-empires/evidence'
sys.path.insert(0,str(W/'tools'))
from global_validation_runner import tiger_lines,tiger_origin,norm_tiger
from classify_history_findings import classify
raw=W/'validation/runs/e1-global-20261031-b/tiger_raw.json'
data=json.loads(raw.read_text('utf-8-sig'))
nulls=[d for d in data if any(x.get('line') is None or x.get('from') is None for x in (d.get('locations') or []))]
assert nulls,'Must exercise the actual DEP0/global nullable-location failure, not only a fabricated easy case.'
for d in data:
    assert isinstance(tiger_lines(d),str) and isinstance(tiger_origin(d),str) and isinstance(norm_tiger(d),str)
for d in [{'locations':[{'line':None,'from':None}]},{'locations':None},{}]:
    assert tiger_origin(d)=='unknown' and tiger_lines(d)==''
issues=json.loads((W/'validation/runs/e1-global-20261031-a/history_production_parser.json').read_text('utf8'))['issues']
positive=classify(W/'exports/debug-naval-20261031-e1',issues)
assert not positive['unreviewed_hard'] and not positive['unreviewed_semantics']
assert positive['counts']['REVIEWED_SAME_OWNER_OVERWRITE_NOT_ADDITIVE']==4
assert positive['counts']['REVIEWED_NATIVE_ORDERED_OVERWRITE']==38
assert positive['counts']['REVIEWED_AUTHOR_ORDERED_OVERWRITE_NONBLOCKING']==94
negative=classify(W/'validation/nonexistent-candidate-evidence-negative',issues)
assert len(negative['unreviewed_semantics'])==136 and not negative['unreviewed_hard']
report={'actual_tiger_raw':str(raw),'actual_tiger_raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
        'actual_records_processed':len(data),'actual_nullable_location_records':len(nulls),
        'nullable_records_pass':True,'empty_locations_pass':True,
        'history_current_exact_source_counts':positive['counts'],
        'different_candidate_evidence_rejected_count':len(negative['unreviewed_semantics']),
        'no_candidate_or_history_modified':True,'engine_verified':False,
        'limits':'Tests adapter handling and evidence binding only; does not execute Victoria3 or determine new territorial design.'}
(E/'global-validation-adapter-regression.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
