from canon_routes_context import *
import re,collections,hashlib
cfg=json.loads((R/'batch-c-repair4-test-config.json').read_text());run=Path(cfg['run']);snap=Path(cfg['snapshot']);f=json.loads((R/'batch-c-repair4-freeze.json').read_text());oldrun=Path(cfg['previous_run'])
actual={rel:sha(snap/rel) for rel in f['files']};assert actual==f['files'];assert all(sha(Path(f['owned_freeze'])/rel)==h for rel,h in actual.items())
deps={rel:sha(snap/rel) for rel in f['read_only_dependency_sha256']};assert deps==f['read_only_dependency_sha256']
manifest={str(p.relative_to(snap)).replace('\\','/'):sha(p) for p in snap.rglob('*') if p.is_file()};dump(run/'snapshot.json',{'cfg':cfg,'owned_sha':actual,'dependencies':deps,'full_snapshot_sha':manifest,'source':'previous frozen dependency snapshot + exact repair4 owned and hash-verified read-only dependencies; no live full C used'})
loc={};formats=[]
for lang in ['english','simp_chinese']:
 p=snap/f'localization/{lang}/replace/zzzzzzzzzzzz_nesnd_batch_c_l_{lang}.yml';raw=p.read_bytes();s=raw.decode('utf-8-sig');assert raw.startswith(b'\xef\xbb\xbf');assert s.splitlines()[0]=='l_'+lang+':'
 entries=re.findall(r'^\s+([\w.]+):\d*\s+"(.*)"\s*$',s,re.M);keys=[k for k,v in entries];assert len(keys)==len(set(keys));loc[lang]=dict(entries);formats.append({'language':lang,'count':len(keys),'BOM':True,'header':True})
assert set(loc['english'])==set(loc['simp_chinese'])
for lang,items in loc.items():
 for k,v in items.items():
  assert not re.search(r'90|九十|2.day|两日|deadline|期限前另择',v,re.I),(lang,k)
# Explicit old compatibility JE keys are intentionally absent; report rather than fabricate titles.
refs=[];known=set(loc['english']);missing=[]
for rel in actual:
 if not rel.endswith('.txt'):continue
 s=read(snap/rel)
 for m in re.finditer(r'\b(title|text|name|custom_tooltip|desc)\s*=\s*(nesnd_[\w.]+)',s):
  key=m.group(2)
  if key not in known and m.group(1) in ['title','text','custom_tooltip','desc']:missing.append({'key':key,'file':rel,'line':s.count('\n',0,m.start())+1})
# Current B2-related text can be outside C; missing references are listed with effective resolution below.
resolved={lang:{} for lang in loc}
for lang in loc:
 for root in [G/'localization'/lang,snap/'localization'/lang]:
  if not root.exists():continue
  for p in sorted(root.rglob('*.yml')):
   for k,v in re.findall(r'^\s*([\w.]+):\d*\s+"(.*)"\s*$',read(p),re.M):resolved[lang][k]=str(p)
unresolved=[m for m in missing if not all(m['key'] in resolved[l] for l in resolved)]
dump(run/'localization-repair4.json',{'status':'PASS_PAIRED_C_LOCALIZATION' if not unresolved else 'FAIL','formats':formats,'keys':sorted(known),'unresolved_explicit_refs':unresolved,'retired_compatibility_JE_missing_implicit_keys':['nesnd_egypt_protection_negotiations','nesnd_egypt_protection_negotiations_reason'],'boundary':'key coverage/format and removed-term checks only; prose approval remains implementation writing comparison'})
old=json.loads((oldrun/'tiger-c-owned.json').read_text());new=json.loads((run/'tiger-c-owned.json').read_text())
def sig(d):return (d['key'],d['message'],tuple((l['path'].replace('\\','/'),l['line'].strip()) for l in d['locations']))
a={sig(d):d for d in old['owned_diagnostics']};b={sig(d):d for d in new['owned_diagnostics']}
dump(run/'tiger-repair4-delta.json',{'against':str(oldrun/'tiger-c-owned.json'),'added':[b[k] for k in b.keys()-a.keys()],'removed':[a[k] for k in a.keys()-b.keys()],'counts':new['owned_counts'],'classification':{'unknown-field:nesnd_small_state_country':'EXPECTED_UNIMPLEMENTED B2 dependency, no placeholder inserted','strict-scopes:ai_opium_dealer_no_alliance_trigger':'INHERITED; exact article/helper AST and native control evidence retained from repair2; both relevant source SHA unchanged','missing-localization:retired_JE':'NEW_WARNING; inactive compatibility shell possible/show=false, invalid=true, no effects/buttons; not hidden as inherited'}})
print({'snapshot_files':len(manifest),'loc_pairs':len(known),'unresolved':unresolved,'tiger_added':len(b.keys()-a.keys())})
