from native_extract import G,W,pdx,loc
import json,hashlib,re

manifest=json.loads((W/'native-india-manifest.json').read_text(encoding='utf-8'))
for rel in ['events/east_indies_je_events.txt','common/static_modifiers/00_ip2_03_modifiers.txt','common/static_modifiers/00_ip2_05_modifiers.txt']:
 p=G/rel;t,r=pdx.read(p)
 manifest['files'].append({'file':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':len(t.splitlines()),'objects':[{'id':n.key,'lines':loc(t,n)} for n in r.children if n.children is not None]})
inputs=json.loads((W/'native-india-inputs.json').read_text(encoding='utf-8'))
known={x['file'] for x in manifest['files']}
for src in inputs['sources']:
 if src['file'] not in known:
  p=G/src['file'];manifest['files'].append({**src,'lines':len(p.read_text(encoding='utf-8-sig').splitlines())})
manifest['files'].sort(key=lambda x:x['file'])
inventory=[]
for entry in manifest['files']:
 if not entry['file'].startswith('common/journal_entries/'):continue
 t,r=pdx.read(G/entry['file'])
 for n in r.children:
  if not n.children:continue
  calls=[]
  for c in n.walk():
   if c.key=='trigger_event': calls.append(c.scalar('id') if c.children else c.value)
  inventory.append({'id':n.key,'file':entry['file'],'lines':loc(t,n),'direct_dlc_gates':list(dict.fromkeys(c.value for c in n.walk() if c.key=='has_dlc_feature')),'buttons':[c.value for c in n.all('scripted_button')],'progress_bars':[c.value for c in n.all('scripted_progress_bar')],'event_calls':list(dict.fromkeys(calls)),'fields':{c.key:loc(t,c) for c in n.children if c.key in ['is_shown_when_inactive','possible','complete','fail','invalid','timeout','on_timeout','immediate','on_complete','on_fail']}})
summary={'version':'1.13.11','build':'24799966','date':'2026-11-02','status':'SOURCE_RESEARCH_ONLY_ENGINE_NOT_RUN','scope':'All selected India 04_ JE definitions and India event directory inventoried; selected core chains deeply traced. BIC explicit inputs scanned across full native history directories, excluding subjects and runtime-generated state.','journal_entries':inventory,'source_files':len(manifest['files']),'population_input_total':inputs['population_input_total'],'population_records':inputs['population_records'],'building_ownership_level_total':inputs['building_ownership_level_total'],'explicit_building_levels':inputs['explicit_building_levels'],'ownership_country_levels':inputs['ownership_country_levels'],'military_formation_unit_counts':{r['name']:sum(r['unit_counts'].values()) for r in inputs['military_formations'] if r['unit_counts']},'cautions':['Native BIC anti-colonial movement is gated to BIC subject without South Asian primary culture; cannot represent anti-Mughal nationalism unchanged.','Hindu religion database has no direct literacy penalty; caste hierarchy, caste law, education/qualifications and initial literacy are distinct.','je_reform_indies and je_ethical_policy belong to DEI, not BIC.','No verified native France-to-Mughal modernization or anti-Wu chain among covered JEs.','Scripted population/wealth/building inputs are not runtime GDP, SOL or national literacy.']}
(W/'native-india-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
# Keep an object inventory separate from the compact hash manifest.
(W/'native-india-object-index.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
compact={k:v for k,v in manifest.items() if k!='files'}
compact['files']=[{k:v for k,v in f.items() if k!='objects'} for f in manifest['files']]
compact['object_index']='native-india-object-index.json'
(W/'native-india-manifest.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2),encoding='utf-8')
issues=[]
for f in compact['files']:
 if hashlib.sha256((G/f['file']).read_bytes()).hexdigest()!=f['sha256']:issues.append(f['file'])
assert not issues,issues
for match in re.finditer(r'\[N\d+\]: <([^>]+)>',(W/'native-india.md').read_text(encoding='utf-8')):
 p=re.sub(r':\d+$','',match.group(1));assert __import__('pathlib').Path(p).exists(),p
print(json.dumps({'source_files':len(compact['files']),'journal_objects':len(inventory),'all_source_hashes_match':True,'all_reference_files_exist':True,'source_manifest_sha256':hashlib.sha256((W/'native-india-manifest.json').read_bytes()).hexdigest(),'report':str(W/'native-india.md')},ensure_ascii=False))
