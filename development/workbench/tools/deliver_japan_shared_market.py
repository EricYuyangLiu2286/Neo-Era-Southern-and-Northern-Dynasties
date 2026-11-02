from japan_dev_context import *
import datetime,zipfile

repo=W/'projects/nesnd-repository'
parent='38cf3ea6bacdd5bcc43f3041a39bcde6d96982d9'
pre=W/'backups/pre-change-japan-shared-market-20261102T234554Z/mod'
backup=W/'backups/candidate-japan-shared-market-final-20261102T234557Z/mod'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==parent
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo).strip()==b'main'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
before,after=man(pre),man(C)
assert man(M)==before,'Main changed after independent pre-change backup.'
assert man(backup)==after,'Candidate differs from final independent backup.'
for rel,digest in before.items():assert sha(repo/rel)==digest,('Main/Git mismatch',rel)
validated=json.loads(read(R/'external-final-checks.json'))
assert validated['status']=='STATIC_PASS'
assert json.loads(read(R/'mcp-final-queries.json'))['status']=='PASS'
assert not json.loads(read(R/'tiger-final-delta.json'))['added']
for rel,digest in validated['files'].items():
    if not rel.endswith('.md'):assert after.get(rel)==digest,('Game file changed since validation',rel)
assert not (before.keys()-after.keys()),'Unexpected deletion.'
changes=[p for p in sorted(after) if before.get(p)!=after[p]]
def cp(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
for rel in changes:cp(C/rel,M/rel)
assert man(M)==after
for rel in changes:cp(M/rel,repo/rel)
dump(R/'main-merge.json',{'candidate':str(C),'main':str(M),'parent_commit':parent,'prechange':str(pre),'candidate_backup':str(backup),'changes':[{'file':p,'before':before.get(p),'after':after[p]} for p in changes],'conflicts':[],'deletions':[],'main_equals_candidate':True,'game_launched':False})
dump(R/'delivery-final-manifest.json',{'files':after,'engine_verified':False,'post_review_changes':'Task/handoff documentation only; gameplay SHA matches 866-check snapshot.'})
package=W/'exports/nesnd-japan-shared-market-20261102.zip'
included=[]
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(after):
        if rel.split('/')[0] not in {'.metadata','common','events','gfx','gui','localization','map_data'}:continue
        if Path(rel).suffix.lower() in {'.md','.py','.bak','.log'}:continue
        assert 'procurement' not in rel and '/qa' not in rel and 'qa-overlay' not in rel,rel
        z.write(M/rel,rel);included.append(rel)
dump(R/'package.json',{'path':str(package),'sha256':sha(package),'files':included,'count':len(included),'qa_tools_included':False,'engine_verified':False})

support={}
excluded={'plan-before-market-correction.md','procurement-exit-fix.json','procurement-exit-text.json','wu-procurement-budget-benchmark.json','wu-procurement-contract.json','assembled-localization.json','final-gap-text.json','final-gap-text-applied.json'}
# Top-level reports only. Never recursively copy the withdrawn full candidate.
for p in R.iterdir():
    if p.is_file() and p.name not in excluded and p.suffix in {'.md','.json','.py','.txt'}:
        support['workbench/'+p.relative_to(W).as_posix()]=p
for name in ['japan_dev_context.py','validate_japan_delivery.py','probe_japan_delivery.py','run_japan_tiger.py','fix_japan_market_model.py','fix_existing_shared_market.py','withdraw_japan_procurement.py','finalize_japan_market_review.py','prepare_japan_delivery_records.py','deliver_japan_shared_market.py']:
    p=W/'tools'/name;support['workbench/'+p.relative_to(W).as_posix()]=p
p=W/'plans/two-empires/20261102-japan-development-design.md';support['workbench/'+p.relative_to(W).as_posix()]=p
for p in [S/'references/economic-agency-and-crises.md',S/'references/numeric-scale-contract.md',S/'references/active-work.md']:
    support['nesnd-skill/'+p.relative_to(S).as_posix()]=p
mp=repo/'development/snapshot-manifest.json';manifest=json.loads(read(mp));records={x['path']:x for x in manifest['files']}
for rel,p in support.items():
    cp(p,repo/'development'/rel)
    records[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
manifest.update(files=[records[k] for k in sorted(records)],updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),refresh_scope='Japanese journals and shared-market correction; withdrawn procurement draft excluded; engine launch still pending.')
dump(mp,manifest)
assert man(M)==after
print(json.dumps({'main_changes':len(changes),'main_files':len(after),'support_files':len(support),'package_files':len(included),'game_launched':False}))
