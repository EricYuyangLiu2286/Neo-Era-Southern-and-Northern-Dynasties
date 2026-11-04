from pathlib import Path
import sys,json,hashlib,collections
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse,basekey
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/branch-naming-cleanup-20261104';G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');C=W/'exports/maintenance-current';B=W/'backups/pre-change-maintenance-pre-cleanup-20261104T213001Z/mod'
normal=json.loads((R/'normalization-implementation.json').read_text(encoding='utf-8'));folders=sorted({str(Path(x['old']).parent).replace('\\','/') for x in normal['script_renames']}|{'common/scripted_effects','common/scripted_triggers','common/scripted_buttons','common/journal_entries'})
cache={}
def tree(p):
 if p not in cache:cache[p]=parse(p.read_text(encoding='utf-8-sig'))
 return cache[p]
def canon(n):
 if n.children is None:return (n.op,n.value,n.prefix)
 return (n.op,tuple((x.key,canon(x)) for x in n.children),n.prefix)
def effective(mod):
 result={};errors=[];parsed=0
 for folder in folders:
  files={p.relative_to(G/folder).as_posix():p for p in (G/folder).rglob('*.txt')}
  files.update({p.relative_to(mod/folder).as_posix():p for p in (mod/folder).rglob('*.txt')})
  for rel,p in sorted(files.items()):
   try:t=tree(p);parsed+=1
   except Exception as e:errors.append({'path':str(p),'parse_error':str(e)});continue
   for n in t.children or []:
    k=(folder,basekey(n.key))
    if not n.key or n.key.startswith('@'):continue
    if n.key.startswith('REPLACE:') and k not in result:errors.append({'path':str(p),'id':k[1],'reason':'REPLACE before definition'})
    # Injections need explicit ordered merging; none in changed prefixes must be silently replaced.
    if n.key.startswith(('INJECT:','TRY_INJECT:')):errors.append({'path':str(p),'id':k[1],'reason':'INJECT semantics require separate review'});continue
    result[k]=(n,p)
 return result,errors,parsed
b,be,bp=effective(B);c,ce,cp=effective(C)
changes=[]
for k in sorted(set(b)|set(c)):
 a=b.get(k);d=c.get(k)
 if a is None or d is None or canon(a[0])!=canon(d[0]):changes.append({'database':k[0],'id':k[1],'B':str(a[1]) if a else None,'C':str(d[1]) if d else None})
report={'source_manifest_sha256':hashlib.sha256((R/'candidate-freeze.json').read_bytes()).hexdigest(),'folders':folders,'parsed_files':{'B':bp,'C':cp},'B_errors':be,'C_errors':ce,'effective_differences':changes}
(R/'sol-layered-database-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
# Display wrappers affect visibility, not the enclosed predicate. Preserve effect ordering.
def semantic(n,commutative=False):
 if n.children is None:return (n.key,n.op,n.value,n.prefix)
 kids=[]
 for x in n.children:
  if x.key in ('hidden_trigger','custom_tooltip'):
   kids.extend(semantic(y,commutative) for y in x.children or [] if not (x.key=='custom_tooltip' and y.key in ('text','subject')))
  else:kids.append(semantic(x,commutative))
 if commutative:kids.sort(key=repr)
 return (n.key,n.op,tuple(kids),n.prefix)
semanticdiff=[]
for k in sorted(set(b)|set(c)):
 a=b.get(k);d=c.get(k)
 if a is None or d is None or semantic(a[0],k[0]=='common/scripted_triggers')[1:]!=semantic(d[0],k[0]=='common/scripted_triggers')[1:]:semanticdiff.append({'database':k[0],'id':k[1]})
allowed={'nesnd_small_monthly','nesnd_small_episode_monthly'}
report['semantic_differences']=semanticdiff
report['gate']={'status':'FAIL' if ce or any(x['id'] not in allowed for x in semanticdiff) else 'STATIC_PASS','engine_verified':False,'boundary':'GAME+MOD file-order simulation and ordered parse; native engine loading not executed. Only trigger database conjuncts sorted. Effects and all other databases retain original ordered AST.'}
(R/'sol-layered-database-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report['gate']));sys.exit(1 if report['gate']['status']=='FAIL' else 0)
