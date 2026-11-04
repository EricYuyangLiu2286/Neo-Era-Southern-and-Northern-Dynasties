from pathlib import Path
import sys,json,hashlib,collections,re,difflib
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench'); R=W/'reports/branch-naming-cleanup-20261104'; B=W/'backups/pre-change-maintenance-pre-cleanup-20261104T213001Z/mod'; C=W/'exports/maintenance-current'
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse,unquote,basekey
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return p.read_text(encoding='utf-8-sig')
def manifest(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
frozen=json.loads(read(R/'candidate-freeze.json'))['files']; actual=manifest(C)
results={}; results['freeze']={'pass':frozen==actual,'count':len(actual),'changed':[p for p in frozen if actual.get(p)!=frozen[p]],'added':sorted(actual.keys()-frozen.keys())}
normal=json.loads(read(R/'normalization-implementation.json'))
def canon(n,display=False):
    if n.children is None:return (n.key,n.op,n.value,n.prefix)
    kids=[]
    for x in n.children:
        if display and x.key in ('hidden_trigger','custom_tooltip'):
            for y in x.children or []:
                if x.key=='custom_tooltip' and y.key in ('text','subject'):continue
                z=canon(y,display);kids.append(z)
        else:kids.append(canon(x,display))
    return (n.key,n.op,tuple(kids),n.prefix)
def databases(root):
    out={}; files={}; errors=[]
    for folder in ('common','events'):
      for p in sorted((root/folder).rglob('*.txt')):
        rel=p.relative_to(root).as_posix()
        try:t=parse(read(p))
        except Exception as e:errors.append([rel,str(e)]);continue
        files[rel]=t
        for n in t.children or []:
          k=(str(p.parent.relative_to(root)).replace('\\','/'),basekey(n.key))
          if k[1] is not None:out[k]=(n,rel)
    return out,files,errors
bd,bf,be=databases(B); cd,cf,ce=databases(C)
changes=[]
for k in sorted(set(bd)|set(cd)):
    a=bd.get(k);b=cd.get(k)
    if a is None or b is None or canon(a[0],True)[1:]!=canon(b[0],True)[1:]:changes.append({'db':k[0],'id':k[1],'before':a[1] if a else None,'after':b[1] if b else None})
results['effective_script_semantic_diffs']=changes
results['parser']={'baseline_errors':be,'candidate_errors':ce,'candidate_parsed_files':len(cf)}
results['renames']=[]
for row in normal['script_renames']:
    old=row['old'];new=row.get('new')
    results['renames'].append({'old':old,'new':new,'payload_equal':sha(B/old)==sha(C/new) if new and row.get('payload_unchanged') else None,'removed_old':not (C/old).exists()})
results['merged_definition_equivalence']=[]
for row in normal['mod_owned_definition_merges']:
    key=(str(Path(row['source']).parent).replace('\\','/'),row['id'])
    # Explicitly select original REPLACE directive, not filename-precedence inference.
    old=next(n for n in bf[row['source']].children if n.key=='REPLACE:'+row['id'])
    new=next(n for n in cf[row['destination']].children if n.key==row['id'])
    results['merged_definition_equivalence'].append({**row,'equal':canon(old)[1:]==canon(new)[1:]})
line_rx=re.compile(r'^\s*([^\s:#]+)\s*:\s*\d*\s*"((?:\\.|[^"\\])*)"\s*(?:#.*)?$')
def loc(root):
    rows=collections.defaultdict(list);issues=[]
    for p in (root/'localization').rglob('*.yml'):
        lang=p.relative_to(root/'localization').parts[0];txt=read(p)
        if not p.read_bytes().startswith(b'\xef\xbb\xbf'):issues.append([str(p.relative_to(root)),'BOM'])
        if txt.splitlines()[0].strip()!='l_'+lang+':':issues.append([str(p.relative_to(root)),'header'])
        for i,line in enumerate(txt.splitlines()[1:],2):
          if not line.strip() or line.lstrip().startswith('#'):continue
          m=line_rx.match(line)
          if m:rows[(lang,m[1])].append((p.relative_to(root).as_posix(),i,m[2]))
          else:issues.append([str(p.relative_to(root)),i,'syntax',line])
    return rows,issues
bl,bi=loc(B);cl,ci=loc(C)
results['localization']={'issues':ci,'unique':len(cl),'duplicates':[{'lang':k[0],'key':k[1],'sources':v} for k,v in cl.items() if len(v)!=1],'lost_keys':[k for k in bl if k not in cl],'new_keys':[k for k in cl if k not in bl]}
required=json.loads(read(R/'required-loc-keys.json'))['keys'];results['required_condition_keys']={'count':len(required)*2,'missing':[(lang,row['key']) for row in required for lang in ('english','simp_chinese') if (lang,row['key']) not in cl]}
# Token balancing catches malformed escapes without presuming all [] syntax represents literals.
token_issues=[]
for (lang,key),rows in cl.items():
  value=rows[0][2]
  for op,close in [('[',']')]:
    depth=0
    for c in value:
      if c==op:depth+=1
      elif c==close:depth-=1
      if depth<0:break
    if depth:token_issues.append([lang,key,'unbalanced brackets'])
  if value.count('$')%2:token_issues.append([lang,key,'odd dollar delimiters'])
results['token_balance']=token_issues
# All display AST wrappers have localized text in each language.
missing=[];wraps=[]
for rel,t in cf.items():
  for n in t.walk():
    if n.key=='custom_tooltip' and n.get('text'):
      key=unquote(n.get('text').value or '')
      if key.startswith(('nesnd_qe1_condition_','nesnd_egypt_condition_')):
        wraps.append([rel,key]);missing.extend([rel,key,lang] for lang in ('english','simp_chinese') if (lang,key) not in cl)
results['condition_references']={'calls':wraps,'missing':missing}
# Keep exact source content hashes for all evidence and tools.
logs={}; lines=[]
for p in sorted((R/'runtime-error-capture').glob('error*.log')):
 s=read(p);logs[p.name]={'sha256':sha(p),'bytes':p.stat().st_size,'lines':len(s.splitlines()),'empty_texture':s.count('Could not find texture due to'),'JournalEntry':s.count('JournalEntry'),'change_variable':s.count('change_variable')}
 for line in s.splitlines():
  if 'JournalEntry' in line or 'change_variable' in line or 'Texture path is empty' in line:lines.append(p.name+': '+line)
results['native_logs']=logs
(R/'sol-raw-log-excerpts.txt').write_text('\n'.join(lines),encoding='utf-8')
(R/'sol-independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k not in ('condition_references','renames','native_logs')},ensure_ascii=False,indent=2))
# Additional strict counter regression using source AST siblings, no missing -> 0 fallback.
def structural(n,sort=False):
 z=canon(n,True)
 def rec(t):
  if not isinstance(t,tuple) or len(t)!=4:return t
  key,op,val,prefix=t
  if isinstance(val,tuple):val=tuple(rec(x) for x in val);val=tuple(sorted(val,key=repr)) if sort else val
  return (key,op,val,prefix)
 return rec(z)
results['trigger_equivalence'] = []
for row in changes:
 if row['db']=='common/scripted_triggers':
  k=(row['db'],row['id']);results['trigger_equivalence'].append({'id':k[1],'commutative_predicates_equal':structural(bd[k][0],True)==structural(cd[k][0],True)})
class Missing(Exception):pass
class InvalidType(Exception):pass
def effect(n,state):
 if n.key=='if':
  lim=n.get('limit');var=lim.get('NOT').scalar('has_variable')
  if var not in state:
   for x in n.children:
    if x.key!='limit':effect(x,state)
 elif n.key=='set_variable':state[n.scalar('name')]=float(n.scalar('value'))
 elif n.key=='change_variable':
  key=n.scalar('name')
  if key not in state:raise Missing(key)
  if not isinstance(state[key],(int,float)):raise InvalidType(key)
  state[key]+=float(n.scalar('add'))
 else:raise AssertionError(n.key)
countertests=[];guarded=[]
for rel in ['common/scripted_effects/nesnd_small_states.txt','common/scripted_effects/nesnd_small_politics.txt']:
 ct=cf[rel];bt=bf[rel]
 for parent in ct.walk():
  for index,n in enumerate(parent.children or []):
   if n.key!='change_variable' or not n.scalar('name','').startswith('nesnd_small_') or n.scalar('add')!='1':continue
   var=n.scalar('name');guard=parent.children[index-1]
   assert guard.key=='if' and guard.get('limit').get('NOT').scalar('has_variable')==var
   assert guard.get('set_variable').scalar('name')==var and guard.get('set_variable').scalar('value')=='0'
   cases=[]
   for label,state,expected in [('first',{},1),('existing',{var:3},4),('reset',{},1)]:
    effect(guard,state);effect(n,state);cases.append({'case':label,'value':state[var],'pass':state[var]==expected})
   old=next(x for x in bt.walk() if x.key=='change_variable' and x.scalar('name')==var)
   try:effect(old,{});red=False
   except Missing:red=True
   try:effect(guard,{var:'country:42'});effect(n,{var:'country:42'});typed=False
   except InvalidType:typed=True
   countertests.append({'source':rel,'variable':var,'baseline_missing_raises':red,'candidate_cases':cases,'invalid_type_raises':typed});guarded.append((rel,guard))
results['strict_counter_regression']=countertests
# Strip only the exact proven guards; remainder of effect AST must match B byte-independent.
for rel,guard in guarded:
 for parent in cf[rel].walk():
  if guard in (parent.children or []):parent.children.remove(guard);break
results['counter_effect_preservation']=[{'source':rel,'equal_after_removing_only_added_guard':canon(bf[rel])==canon(cf[rel])} for rel in sorted(set(x[0] for x in guarded))]
statuskeys=normal['status_context_repairs'];results['status_context']={'count':len(statuskeys),'pass':all('JournalEntry.GetCountry' not in cl[(x['lang'],x['key'])][0][2] and 'ROOT.GetCountry' in cl[(x['lang'],x['key'])][0][2] for x in statuskeys)}
approved=json.loads(read(R/'root-approved-localization.json'))
results['approved_localization']={'count':len(approved),'missing':[(x['lang'],x['key']) for x in approved if (x['lang'],x['key']) not in cl],'unexpected_value':[(x['lang'],x['key']) for x in approved if cl[(x['lang'],x['key'])][0][2] != x['new'].replace('JournalEntry.GetCountry','ROOT.GetCountry') and not any(a['lang']==x['lang'] and a['key']==x['key'] for a in statuskeys)]}
results['source_hashes']={'candidate_manifest_sha256':sha(R/'candidate-freeze.json'),'baseline_manifest_sha256':sha(R/'baseline-manifest.json'),'checker_sha256':sha(Path(__file__))}
(R/'sol-independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:results[k] for k in ('trigger_equivalence','strict_counter_regression','counter_effect_preservation','approved_localization','status_context','native_logs')},ensure_ascii=False,indent=2))
# Evidence enrichment: file-level boundaries, native log records, threshold tests.
bman=manifest(B); changed_files=sorted(p for p in set(actual)|set(bman) if actual.get(p)!=bman.get(p))
results['file_change_boundary']={'changed_paths':changed_files,'outside_script_locale':[p for p in changed_files if not p.startswith(('localization/','common/','events/'))]}
results['resources_unchanged']={'pass':all(actual.get(p)==h for p,h in bman.items() if p.startswith(('gfx/','map_data/','gui/','content_source/'))),'scope':'all baseline gfx/map_data/gui/content_source file bytes'}
records=[]
for p in sorted((R/'runtime-error-capture').glob('error*.log')):
 s=read(p); chunks=re.split(r'(?=^\[\d\d:\d\d:\d\d\])',s,flags=re.M)
 counts=collections.Counter()
 for chunk in chunks:
  if not chunk.strip():continue
  if 'JournalEntry' in chunk:counts['JournalEntry_context']+=1
  elif "Variable not of the 'value' scope type. Type: empty" in chunk:counts['change_variable_empty']+=1
  elif "Could not find texture due to 'VFSOpen Error:  not found'" in chunk:counts['empty_texture_unresolved']+=1
  else:counts['other']+=1
 records.append({'file':p.name,'records':dict(counts),'sha256':sha(p)})
results['native_log_records']=records
boundary=[]
for row in countertests:
 var=row['variable'];rel=row['source'];t=bf[rel];thresholds=[]
 for n in t.walk():
  if n.key==var and n.op=='>=' and n.value and n.value.isdigit():thresholds.append(int(n.value))
 for threshold in sorted(set(thresholds)):
  for initial in (threshold-2,threshold-1,threshold):
   n=next(x for x in t.walk() if x.key=='change_variable' and x.scalar('name')==var);state={var:initial};effect(n,state)
   boundary.append({'var':var,'threshold':threshold,'before':initial,'after':state[var],'at_or_above':state[var]>=threshold,'pass':state[var]==initial+1})
results['counter_threshold_cases']=boundary
(R/'sol-independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:results[k] for k in ('native_log_records','resources_unchanged')},ensure_ascii=False,indent=2))

# Root delivery gate: reports with semantic regressions must return nonzero.
allowed_diffs={'nesnd_small_episode_monthly','nesnd_small_monthly','nesnd_egypt_independence_open','nesnd_qe1_economic_victory','nesnd_qe1_military_victory'}
failures=[]
if not results['freeze']['pass']:failures.append('candidate changed after freeze')
if any(x['id'] not in allowed_diffs for x in changes):failures.append('unexpected effective script change')
if ce or results['localization']['issues'] or results['localization']['duplicates'] or results['localization']['lost_keys']:failures.append('source or localization integrity')
if token_issues or results['required_condition_keys']['missing'] or missing:failures.append('text/reference integrity')
if len(countertests)!=8 or any(not x['baseline_missing_raises'] or not x['invalid_type_raises'] or not all(t['pass'] for t in x['candidate_cases']) for x in countertests):failures.append('strict counter regression')
if not all(x['equal_after_removing_only_added_guard'] for x in results['counter_effect_preservation']):failures.append('counter payload change')
if not all(x['commutative_predicates_equal'] for x in results['trigger_equivalence']):failures.append('trigger predicate change')
if not results['status_context']['pass'] or not results['resources_unchanged']['pass']:failures.append('context or resource change')
results['root_gate']={'status':'FAIL' if failures else 'STATIC_PASS','failures':failures,'engine_verified':False}
(R/'sol-independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results['root_gate']))
sys.exit(1 if failures else 0)

