from sweep_context import *
import hashlib
bm,cm,mm=man(B),man(C),man(M)
patch={p:h for p,h in cm.items() if bm.get(p)!=h}
assert not bm.keys()-cm.keys()
game={p:h for p,h in patch.items() if p.startswith(('common/','events/','localization/','gui/'))}
assert len(game)==46
checks={}
for file,want in [('regression-candidate.json',6),('boundary-checks.json',45),('mechanism-tests.json',46)]:
 d=json.loads(read(R/file));assert d['pass'];assert len(d['checks'])==want
 for p,h in patch.items():assert d['source_files'][p]==h,(file,p)
 checks[file]=want
tr=json.loads(read(R/'tiger-candidate-run.json'))
for p,h in patch.items():assert tr['source_files'][p]==h,('tiger source changed',p)
assert not json.loads(read(R/'tiger-added.json'))
mcp=json.loads(read(R/'mcp-final.json'));assert mcp['pass'] and len(mcp['queries'])==7
for q in mcp['queries']:assert sha(C/q['query']['file_path'])==q['sha256']
sp=json.loads(read(R/'spec-review-final-hashes.json'));assert sp['remaining_spec_findings']==0
assert {r['path']:r['sha256'] for r in sp['files']}==game
st=json.loads(read(R/'standards-reviewed-hashes.json'));assert st['sha256']==game
textrows=json.loads(read(R/'writing-keys.json'));assert len(textrows)==127
for row in textrows:assert sha(C/row['path'])==row['sha256']
for p in game:
 if p.endswith('.yml'):assert (C/p).read_bytes().startswith(b'\xef\xbb\xbf')
assert all(mm.get(p) in [bm.get(p),h] for p,h in patch.items()),'Main changed conflicting files; preserve and review'
assert not bm.keys()-mm.keys()
repo=W/'projects/nesnd-repository'
preexisting={p:{'baseline':h,'repository':sha(repo/p) if (repo/p).exists() else None} for p,h in bm.items() if not (repo/p).exists() or sha(repo/p)!=h}
dump(R/'preexisting-main-differences.json',preexisting)
dump(R/'patch-files.json',patch)
fingerprint=hashlib.sha256(json.dumps(cm,sort_keys=True,separators=(',',':')).encode()).hexdigest()
dump(R/'final-validation.json',{'status':'STATIC_PASS','candidate':str(C),'baseline':str(B),'parent':PARENT,'game_version':'1.13.11','build':'24799966','mod_sha256':fingerprint,'gameplay_changed_files':46,'checks':checks,'mcp_queries':7,'tiger_added':0,'changed_text_keys':127,'reviews_remaining':{'spec':0,'standards':0},'preserved_history':True,'engine_verified':False,'runs':[],'source_files':cm,'limits':['Native event/annex callback order and rendered UI not engine-tested','SoL additional radicals is a monthly 15-occupation approximation','Inherited global diagnostics are retained; repeated add JE intentionally ignored']})
print('Frozen:',len(patch),'changed files;',len(cm),'total; pre-existing main/repo differences:',len(preexisting))
print('Main concurrent changes:',[p for p,h in mm.items() if bm.get(p)!=h])
