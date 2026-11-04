from pathlib import Path
import json,hashlib,datetime,re
R=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/branch-naming-cleanup-20261104');load=lambda n:json.loads((R/n).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=load('sol-independent-results.json');layer=load('sol-layered-database-review.json');tiger=load('sol-tiger-execution.json');delta=load('sol-tiger-delta.json');mcp=load('sol-mcp-repair1.json');f=load('candidate-freeze.json');freeze_sha=sha(R/'candidate-freeze.json');C=Path(f['root']);assert f['revision']=='root-repair2'
assert v['root_gate']['status']=='STATIC_PASS' and layer['gate']['status']=='STATIC_PASS' and delta['status']=='STATIC_REGRESSION_PASS'
assert all(x['candidate_manifest_sha256']==freeze_sha for x in [tiger,delta,mcp]);assert layer['source_manifest_sha256']==freeze_sha
assert v['freeze']['pass'] and len(f['files'])==1002 and all(sha(C/p)==h for p,h in f['files'].items())
assert not layer['B_errors'] and not layer['C_errors'];assert {x['id'] for x in layer['semantic_differences']}=={'nesnd_small_monthly','nesnd_small_episode_monthly'}
assert mcp['status']=='PROTOCOL_PASS' and len(mcp['calls'])==8
assert not any('Error' in c.get('text','') or 'not found' in c.get('text','').lower() for x in mcp['calls'] for c in x['response'].get('content',[]))
# Account for all explicitly authorized text repair overrides.
repair=load('root-repair1.json');rx=re.compile(r'^\s*([^\s:#]+)\s*:\s*\d*\s*"((?:\\.|[^"\\])*)"\s*(?:#.*)?$');rows={}
for p in (C/'localization').rglob('*.yml'):
 lang=p.relative_to(C/'localization').parts[0]
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  m=rx.match(line)
  if m:rows[(lang,m[1])]=m[2]
textchecks=[{'lang':x['lang'],'key':x['key'],'matches':rows[(x['lang'],x['key'])]==x['new']} for x in repair['text_changes']];assert len(textchecks)==29 and all(x['matches'] for x in textchecks)
assert all(any((z['lang'],z['key'])==tuple(x) for z in repair['text_changes']) for x in v['approved_localization']['unexpected_value'])
(R/'sol-mcp-final.json').write_text(json.dumps(mcp,ensure_ascii=False,indent=2),encoding='utf-8')
meta={'reviewer':'gpt-6.1-sol','reasoning_effort':'medium','delegation':'Explicit independent review from /root; no candidate implementation authorship or edits.','revision':f['revision'],'candidate':str(C),'baseline':'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-maintenance-pre-cleanup-20261104T213001Z/mod','candidate_manifest_sha256':freeze_sha,'engine_verified':False,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
resolved=[{'id':'DYNAMIC_NAMES_OVERRIDE_REGRESSION','round':'initial','resolution':'Obsolete HNA/SIH REPLACE entries removed; final 00 owner matches original last patch.'},{'id':'TURTLE_REPLACE_BEFORE_DEFINITION','round':'repair1','resolution':'Renamed to turtle_island_nesnd_overrides.txt after native turtle_island_buttons.txt, identical payload; layered ordering errors0 and Tiger added diagnostics0.'},{'id':'QE1_ENCODING_REGRESSION','round':'repair1','resolution':'UTF-8 BOM restored.'}]
s={**meta,'status':'STATIC_PASS','findings':[],'resolved_findings':resolved,'history':['review-round1-history','review-repair1-history'],'checks':{'frozen_files':1002,'localization_unique_key_language_entries':14267,'locale_duplicates':0,'locale_lost_keys':0,'locale_BOM_header_syntax_issues':0,'condition_language_entries':64,'approved_language_entries':312,'root_repair_language_entries':29,'status_context_language_entries':18,'script_rename_plan_entries':27,'mod_owned_payload_merges':10,'layered_databases':len(layer['folders']),'layered_replacement_order_errors':0,'resources_byte_unchanged':True},'limitations':['STATIC_PASS applies to reviewed changes, not whole-MOD engine behavior.','13 inherited Tiger errors and other baseline diagnostics remain visible in raw reports; not waived or certified harmless.','268 native empty texture errors remain unresolved.','Sol validates script/text contracts; final player prose style requires Astra review.']}
val={**meta,'status':'STATIC_PASS','root_gate':v['root_gate'],'layered_gate':layer['gate'],'native_runtime_status':'NOT_RUN','strict_counter_regression':v['strict_counter_regression'],'counter_threshold_cases':v['counter_threshold_cases'],'counter_effect_preservation':v['counter_effect_preservation'],'trigger_equivalence':v['trigger_equivalence'],'text_contract':{'original_approved':312,'repair_overrides':textchecks,'condition_entries':64,'unique_entries':14267,'missing':[]},'tiger':{'execution':'sol-tiger-execution.json','delta':'sol-tiger-delta.json','B':tiger['B'],'C':tiger['C'],'added':delta['added'],'removed':delta['removed'],'status':'STATIC_REGRESSION_PASS','dependencies':'Current GAME only, identical B/C config, no workshop deps added to either run.'},'mcp':{'report':'sol-mcp-final.json','status':'PROTOCOL_PASS','actual_calls':8,'limitation':'Structure queries do not execute game behavior; repeated fields in MCP are not used for canonical validation.'},'native_log_records':v['native_log_records'],'unresolved':[{'type':'empty_texture','count':268,'status':'UNRESOLVED','reason':'Blank VFSOpen path lacks widget/resource provenance; unchanged gfx hashes do not prove rendering correct.'}],'test_boundaries':['Effects and all non-trigger databases remain ordered. Only scripted_trigger predicates permit conjunct ordering after display-wrapper removal; final layered semantic differences are exactly two intended guarded counter effects.','Eight increment sites execute real parsed adjacent guard/change source AST with strict missing/object types. Outer country/AI eligibility is preserved structurally, not interpreted as engine execution.','Reset case starts after deletion; original remove sites and lifecycle effects match baseline after removing only eight added guards.','No game launch, new save/reload, UI or error-zero claim.']}
for name,data in [('standards-review',s),('validation',val)]:
 (R/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'standards-review.md').write_text(f'''# Independent standards review — STATIC_PASS

Actual reviewer: gpt-6.1-sol / medium; independent of implementation, no candidate edits. Frozen revision root-repair2: 1002 files, manifest SHA256 `{freeze_sha}`. Initial and repair1 FAIL reports remain in review-round1-history and review-repair1-history.

No remaining change-specific standards findings. HNA/SIH final owner payloads are restored. Turtle Island overrides now follow native turtle_island_buttons.txt with identical payloads; the prior three replacement-order regressions are gone. Qin trigger BOM restored.

27 rename-plan entries and ten MOD-owned definition merges are accounted for. GAME+MOD same-path overlay followed by filename order across 13 affected databases yields zero ordering errors and no unintended final content changes. After display wrappers are removed, final semantic changes are exactly the two intended counter effects. Effect order is never sorted. Eight added guards removed from those files produce exact baseline ordered AST.

All 14,267 localization key×language entries have unique owners, UTF-8 BOM, matching headers and parseable entries; no lost keys or bracket/dollar imbalance. Original312 approved language entries plus29 explicitly documented repair overrides match the frozen candidate;64 condition entries and18 status-context entries are present. Final prose style approval belongs to Astra. All baseline gfx/map_data/gui/content_source bytes remain unchanged.

Actual Tiger B673→C672 diagnostics, errors13→13, warnings646→645; normalized added diagnostics0. Existing diagnostics remain visible and are not declared harmless. Actual MCP eight calls return expected nonempty structures. Both bind this manifest. No new engine run;268 blank-texture errors remain unresolved.

Reproducible tools and details: sol-independent-check.py, sol-layered-review.py, sol-run-tiger.py, sol-tiger-diff.py, sol-run-mcp.py, validation.json. Fingerprints: sol-final-sourcehashes.json.
''',encoding='utf-8')
(R/'validation.md').write_text(f'''# Independent validation — STATIC_PASS

Actual gpt-6.1-sol / medium. Frozen root-repair2 manifest SHA256 `{freeze_sha}`; 1002 files verified before seal. No game or candidate edits.

Executed against this revision: sol-independent-check.py exit0; sol-layered-review.py exit0; real Tiger B+C processes exit0 plus diagnostic diff; real stdio MCP initialization and eight calls. Current source catalog remains Victoria3 1.13.11/build24799966, unchanged.

- 725 candidate common/events files parse. GAME+MOD effective ordering across13 modified database directories parses B907/C906 files, zero replacement-order errors; HNA/SIH and all three Turtle Island final payloads equal baseline. Only the two guarded counter effects differ semantically after display-wrapper removal. Scripted trigger conjunctions alone permit reordering; effects and other databases retain order.
- Eight actual counter increment AST sites: baseline missing throws8/8, candidate first/existing/reset cases24/24 yield1/4/1, invalid object types throw8/8. Threshold6/12/24 neighboring cases preserve+1. Removing only added guards makes the entire two effect-file ASTs equal B, including reset/removal/lifecycle code. Outer country/AI gates are structurally preserved, not game-executed.
- 14,267 unique localization key×language entries: zero duplicates/loss/BOM/header/syntax/token-balance defects.312 approved language entries plus29 documented repair overrides match;64 condition entries and18 ROOT status entries checked.
- Actual Tiger B673→C672: error13 unchanged; warning646→645; added diagnostics0 after documented path normalization. One strict-scopes warning disappears but this does not certify a semantic fix. All inherited diagnostics remain in raw evidence. Current GAME only, same fresh config for B/C, no workshop deps added to either.
- Actual MCP eight calls initialize B/C and read small monthly, Qin economic victory, HNA. Correct nonempty structures, source-query PROTOCOL_PASS. No canonical repeated-key validation uses MCP dictionary output.
- Six original error logs retain original SHA.426 empty-variable records include pressure225, compact economy166, regional economy35. All belong to guarded sites.268 empty texture records remain UNRESOLVED because VFS path is blank. No error-zero claim.

Native status source chain personally read: GAME/common/journal_entries/journal_entries.md175–179;06_economic_regeneration.txt24–38;localization/english/ip4_spain_l_english.yml21. ROOT owning-country contract supports the narrow status repair; actual UI remains NOT_RUN. Small-state call/reset chain is preserved by ordered source AST.

Raw reports and exact source/tool/config hashes: sol-final-sourcehashes.json; sol-tiger-B.json/C.json; sol-tiger-delta.json; sol-layered-database-review.json; sol-mcp-final.json; sol-independent-results.json. Initial and repair1 FAIL evidence remains in separate history folders. STATIC_PASS is limited to reviewed source changes, not global engine validation.
''',encoding='utf-8')
evidence=['sol-seal-final.py','candidate-freeze.json','baseline-manifest.json','root-repair1.json','normalization-implementation.json','sol-independent-check.py','sol-independent-results.json','sol-layered-review.py','sol-layered-database-review.json','sol-run-tiger.py','sol-tiger-repair1.conf','sol-tiger-B.json','sol-tiger-C.json','sol-tiger-execution.json','sol-tiger-diff.py','sol-tiger-delta.json','sol-run-mcp.py','sol-mcp-final.json','standards-review.md','standards-review.json','validation.md','validation.json']
(R/'sol-final-sourcehashes.json').write_text(json.dumps({'revision':f['revision'],'candidate_manifest_sha256':freeze_sha,'evidence_sha256':{n:sha(R/n) for n in evidence}},indent=2),encoding='utf-8')
print(json.dumps({'status':'STATIC_PASS','manifest':freeze_sha,'sealed_reports':4,'source_hashes':len(evidence)}))

