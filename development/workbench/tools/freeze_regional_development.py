from regional_context import *
import hashlib
paths=[G/p for p in ['common/journal_entries/00_art_jes.txt','events/tech_events/society_tech_events.txt','common/static_modifiers/02_event_modifiers.txt','common/scripted_progress_bars/scripted_progress_bars.md','common/scripted_progress_bars/00_victoria_progress_bars.txt','common/journal_entries/journal_entries.md','common/scripted_effects/00_scripted_effects.txt','common/on_actions/00_code_on_actions.txt','common/journal_entries/05_austria_journal_entries.txt','map_data/state_regions/07_south_america.txt','map_data/state_regions/02_east_europe.txt']]
paths+=[D/'modifiers.log',D/'effects.log']
author=W/'backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace'
paths += [author/'ce_french_empire_journals_l_simp_chinese.yml',author/'ce_usm_events_l_simp_chinese.yml']
dump(R/'implementation-source-hashes.json',[{'path':str(p),'sha256':sha(p)} for p in paths])
bm,cm,mm=man(B),man(C),man(M)
patch={p:h for p,h in cm.items() if bm.get(p)!=h};game={p:h for p,h in patch.items() if p.startswith(('common/','events/','localization/'))}
assert len(game)==9 and not bm.keys()-cm.keys()
for fn,n in [('regional-behavior-candidate.json',71),('structural-checks.json',133)]:
 d=json.loads(read(R/fn));assert d['pass'] and len(d['checks'])==n
 assert all(d['source_files'].get(p)==h for p,h in game.items()),fn
assert json.loads(read(R/'prior-regression-summary.json'))['pass']
for fn in ['regression-candidate.json','boundary-checks.json','mechanism-tests.json']:
 d=json.loads(read(R/'prior-regression'/fn));assert d['pass']
 assert all(d['source_files'].get(p)==h for p,h in cm.items() if p.startswith(('common/','events/','localization/'))),fn
assert not json.loads(read(R/'tiger-added.json'))
d=json.loads(read(R/'tiger-candidate-run.json'));assert all(d['source_files'].get(p)==h for p,h in game.items())
mcp=json.loads(read(R/'mcp-final.json'));assert mcp['pass'] and len(mcp['queries'])==7
for q in mcp['queries']:assert sha(C/q['query']['file_path'])==q['sha256']
assert mm==bm,'Main concurrent changes require review'
for report in ['spec-review.md','standards-review.md']:
 s=read(R/report)
 for p,h in game.items():assert h in s,('Review fingerprint outdated',report,p)
for row in json.loads(read(R/'writing-keys.json')):assert sha(C/row['path'])==row['sha256']
dump(R/'patch-files.json',patch)
dump(R/'final-validation.json',{'status':'STATIC_PASS','candidate':str(C),'baseline':str(B),'parent':PARENT,'game_version':'1.13.11','build':'24799966','gameplay_changed_files':9,'new_ast_checks':71,'structure_checks':133,'prior_regressions':97,'mcp_queries':7,'tiger_added':0,'reviews_remaining':{'standards':0,'spec':0},'engine_verified':False,'source_files':cm,'mod_sha256':hashlib.sha256(json.dumps(cm,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'limits':['No game launched','AST fixtures do not certify engine scheduling, UI or AI balance','Three-country and small-state expanded plans not yet implemented in full']})
print('Frozen',len(patch),'changed files;',len(cm),'total; all gameplay evidence matches')
