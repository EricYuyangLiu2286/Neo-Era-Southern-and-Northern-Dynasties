from pathlib import Path
import json,collections,hashlib
R=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/branch-naming-cleanup-20261104');load=lambda n:json.loads((R/n).read_text(encoding='utf-8-sig'));B=load('sol-tiger-B.json');C=load('sol-tiger-C.json')
rename={x['old'].replace('/','\\'):(x.get('new') or x['old']).replace('/','\\') for x in load('normalization-implementation.json')['script_renames']}
def key(x):
 d={k:v for k,v in x.items() if k!='locations'}
 d['locations']=[{k:(rename.get(v,v) if k=='path' else v) for k,v in y.items() if k not in ('fullpath','linenr','column','length','line')} for y in x['locations']]
 return json.dumps(d,sort_keys=True)
b=collections.Counter(key(x) for x in B);c=collections.Counter(key(x) for x in C)
added=[json.loads(k) for k,n in (c-b).items() for _ in range(n)];removed=[json.loads(k) for k,n in (b-c).items() for _ in range(n)]
report={'candidate_manifest_sha256':hashlib.sha256((R/'candidate-freeze.json').read_bytes()).hexdigest(),'added':added,'removed':removed,'status':'STATIC_REGRESSION_PASS' if not added else 'FAIL','normalization':'only documented renamed paths and diagnostic positions; semantic diagnostic message/key/severity preserved'}
(R/'sol-tiger-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
