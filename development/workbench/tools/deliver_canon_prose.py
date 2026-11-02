from canon_prose_context import *
import datetime,zipfile
repo=W/'projects/nesnd-repository'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==PARENT
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo).strip()==b'main'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
assert man(M)==man(U),'Main changed during review: reconcile before copying.'
base,after=man(U),man(E)
for rel,digest in man(B).items():assert sha(repo/rel)==digest,('Git source changed',rel)
assert json.loads(read(R/'external-validation.json'))['status']=='PASS'
assert json.loads(read(R/'mcp-source-queries.json'))['status']=='PASS'
assert not json.loads(read(R/'tiger-delta.json'))['added']
backup=W/'backups/candidate-canon-prose-final-20261102T221434Z/mod'
assert man(backup)==after
changes=[p for p in sorted(base.keys()|after.keys()) if base.get(p)!=after.get(p)]
assert not (base.keys()-after.keys())
def cp(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
for rel in changes:cp(E/rel,M/rel)
assert man(M)==after
for rel,digest in after.items():
    if not (repo/rel).exists() or sha(repo/rel)!=digest:cp(M/rel,repo/rel)
dump(R/'main-merge.json',{'candidate':str(E),'main':str(M),'parent_commit':PARENT,'prechange':str(U),'candidate_backup':str(backup),'changes':[{'file':p,'before':base.get(p),'after':after[p]} for p in changes],'conflicts':[],'deletions':[],'main_equals_candidate':True,'game_launched':False})
dump(R/'delivery-final-manifest.json',{'files':after,'post_review_changes':'Two AST-identical desc indent fixes; bilingual pressure tooltip P2 independently verified; task/handoff documents.','japan_candidate_excluded':str(C),'engine_verified':False})

package=W/'exports/nesnd-canon-prose-20261102.zip'
included=[]
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(after):
        p=M/rel
        if rel.split('/')[0] not in {'.metadata','common','events','gfx','gui','localization','map_data'}:continue
        if p.suffix.lower() in {'.md','.py','.bak','.log'}:continue
        assert not re.search(r'(^|/)(?:qa|debug|tools|__pycache__)(/|$)',rel,re.I),rel
        z.write(p,rel);included.append(rel)
dump(R/'package.json',{'path':str(package),'sha256':sha(package),'files':included,'count':len(included),'qa_tools_included':False,'engine_verified':False})

support={}
for p in R.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.json','.py','.txt'} and '__pycache__' not in p.parts:
        support['workbench/'+p.relative_to(W).as_posix()]=p
for name in ['canon_prose_context.py','refine_canon_event_context.py','apply_canon_editorial.py','fix_canon_review.py','finalize_canon_records.py','validate_canon_prose.py','run_canon_tiger.py','probe_canon_context.py','deliver_canon_prose.py']:
    p=W/'tools'/name;support['workbench/'+p.relative_to(W).as_posix()]=p
for p in [S/'references/north-south-institutions.md',S/'references/narrative-context.md',S/'references/active-work.md']:
    support['nesnd-skill/'+p.relative_to(S).as_posix()]=p
p=S.parent/'nesnd-player-writing/SKILL.md';support['nesnd-player-writing/SKILL.md']=p
manifest_path=repo/'development/snapshot-manifest.json';manifest=json.loads(read(manifest_path));records={x['path']:x for x in manifest['files']}
for rel,p in support.items():
    cp(p,repo/'development'/rel)
    records[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
manifest.update(files=[records[k] for k in sorted(records)],updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),refresh_scope='Author constitutional canon and bilingual prose audit; Japan gameplay remains in an independent unfinished candidate.')
dump(manifest_path,manifest)
assert man(M)==after
print(json.dumps({'main_changes':len(changes),'main_files':len(after),'support_files':len(support),'package':str(package),'game_launched':False}))
