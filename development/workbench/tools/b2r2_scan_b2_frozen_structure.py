from canon_routes_context import *
import hashlib,re,collections,json
cfg=json.loads((R/'batch-b2-repair2-test-config.json').read_text());run=Path(cfg['run']);snap=Path(cfg['snapshot']);f=json.loads((R/'batch-b2-repair2-freeze.json').read_text());owned=f['owned_files'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parsed={};allnodes={}
for rel,h in owned.items():
 p=snap/rel
 if sha(p)!=h:raise RuntimeError('SHA mismatch '+rel)
 if p.suffix=='.txt':parsed[rel]=parse(read(p));allnodes[rel]=list(parsed[rel].walk())
# Effective current database definitions, respecting same-path mod replacement and REPLACE prefixes.
dbs={}
for folder in ['buildings','laws','production_methods','political_movements','subject_types','static_modifiers','diplomatic_actions','technology/technologies']:
 paths={p.relative_to(G/f'common/{folder}').as_posix():p for p in (G/f'common/{folder}').rglob('*.txt')} if (G/f'common/{folder}').exists() else {}
 if (snap/f'common/{folder}').exists():paths.update({p.relative_to(snap/f'common/{folder}').as_posix():p for p in (snap/f'common/{folder}').rglob('*.txt')})
 defs={}
 for p in sorted(paths.values()):
  for n in parse(read(p)).children or []:
   if n.key:
    canonical=n.key.removeprefix('REPLACE:').removeprefix('REPLACE_OR_CREATE:');defs[canonical]=str(p)
    aliases=n.get('aliases')
    if aliases:
     for alias in aliases.values():defs[alias]=str(p)+'#alias_of:'+canonical
 dbs[folder]=defs
dump(run/'b2-effective-building-aliases.json',{k:v.split('#alias_of:')[1] for k,v in dbs['buildings'].items() if '#alias_of:' in v})
checks={'is_building_type':'buildings','has_law':'laws','has_law_or_variant':'laws','is_political_movement_type':'political_movements','is_subject_type':'subject_types','has_modifier':'static_modifiers','remove_modifier':'static_modifiers','has_technology_researched':'technology/technologies'}
missing=[]
for rel,nodes in allnodes.items():
 s=read(snap/rel)
 for n in nodes:
  if n.key in checks and n.children is None:
   token=n.value.strip('"').removeprefix('law_type:');db=checks[n.key]
   if '$' not in token and token not in dbs[db]:missing.append({'file':rel,'line':s.count('\n',0,n.start)+1,'field':n.key,'token':token,'database':db})
# UI decomposition preserves the ordered possible AST, separate from visible and hidden execution.
ui=[]
for rel,tree in parsed.items():
 if '/scripted_buttons/' not in rel:continue
 for n in tree.children or []:
  poss=n.get('possible');vis=n.get('visible');eff=n.get('effect')
  ui.append({'button':n.key,'file':rel,'line':read(snap/rel).count('\n',0,n.start)+1,'visible':shape(vis) if vis else None,'possible':shape(poss) if poss else None,'effect':shape(eff) if eff else None,'boundary':'source decomposition only; no UI hover or gameplay click verified'})
langs={};formats=[]
for lang in ['english','simp_chinese']:
 rel=f'localization/{lang}/replace/zzzzzzzzzzzzz_nesnd_small_states_l_{lang}.yml';p=snap/rel;s=read(p);entries=re.findall(r'^\s*([\w.]+):\d*\s+"(.*)"\s*$',s,re.M);keys=[k for k,v in entries];langs[lang]=dict(entries);formats.append({'lang':lang,'BOM':p.read_bytes().startswith(b'\xef\xbb\xbf'),'header':s.splitlines()[0],'keys':len(keys),'duplicates':[k for k,n in collections.Counter(keys).items() if n>1]})
# All actual explicit localization references resolve in current GAME + snapshot; record literal native modifier desc gaps separately.
resolved={lang:set() for lang in langs}
for lang in langs:
 for root in [G/'localization'/lang,snap/'localization'/lang]:
  if root.exists():
   for p in root.rglob('*.yml'):resolved[lang].update(re.findall(r'^\s*([\w.]+):\d*\s+"',read(p),re.M))
locmissing=[]
for rel,nodes in allnodes.items():
 for n in nodes:
  if n.key in ['title','desc','text','custom_tooltip'] and n.children is None and n.value and re.fullmatch(r'nesnd_[\w.]+',n.value):
   for lang,keys in resolved.items():
    if n.value not in keys:locmissing.append({'key':n.value,'file':rel,'lang':lang})
# Dynamic AI base source evidence: current native events use constant/simple bases in the inspected corpus.
base_values=collections.Counter();examples=[]
for p in (G/'events').rglob('*.txt'):
 for n in parse(read(p)).walk():
  if n.key=='ai_chance':
   base=n.get('base')
   if base and base.children is None:
    base_values[base.value]+=1
    if not re.fullmatch(r'-?\d+(\.\d+)?',base.value or ''):examples.append({'file':str(p),'base':base.value})
result={'snapshot':str(snap),'owned_files':len(owned),'parsed_txt':len(parsed),'owned_sha_match':True,'literal_database_references_missing':missing,'localization':{'formats':formats,'paired_keys_equal':set(langs['english'])==set(langs['simp_chinese']),'explicit_missing':locmissing},'UI_buttons':len(ui),'native_AI_base_non_numeric_examples':examples,'native_AI_base_total':sum(base_values.values()),'boundary':'ordered parser/resources/effective localization and source shape only; not engine validation'}
dump(run/'b2-structural-scan.json',result);dump(run/'b2-ui-source-decomposition.json',ui);print(json.dumps(result,ensure_ascii=False,indent=2))
