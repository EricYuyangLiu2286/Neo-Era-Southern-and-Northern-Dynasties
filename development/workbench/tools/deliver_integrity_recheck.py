from integrity_context import *
import subprocess,zipfile
from datetime import datetime,timezone
repo=W/'projects/nesnd-repository'
parent='870639a35218625722be02113157a518ed8271bd'
before,after=man(B),man(C)
backup=W/'backups/candidate-integrity-recheck-final-20261102T091420Z/mod'
assert man(M)==before and man(backup)==after
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==parent
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
assert not set(before)-set(after)
assert json.loads(read(R/'contracts-final.json'))['status']=='PASS'
tiger=json.loads(read(R/'global-final/tiger_classification.json'));assert not tiger['new_vs_baseline']
fingerprint=json.loads(read(R/'global-final/fingerprint.json'))['candidate_manifest']
drift=[r for r in set(fingerprint)|set(after) if fingerprint.get(r)!=after.get(r)]
assert all(r.startswith('.scratch/') for r in drift),drift
changes=sorted(r for r in after if before.get(r)!=after[r])
for r in changes:
 q=repo/r
 if r in before:assert sha(q)==before[r],('Git conflict',r)
 else:assert not q.exists(),('Git add conflict',r)
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
for r in changes:cp(C/r,M/r);cp(C/r,repo/r)
assert man(M)==after
dump(R/'main-merge.json',{'parent_commit':parent,'main':str(M),'candidate':str(C),'before_backup':str(B),'candidate_backup':str(backup),'changed':[{'file':r,'before':before.get(r),'after':after[r]} for r in changes],'deletions':[],'conflicts':[],'verified_files':len(after),'post_validation_changes':drift,'engine_verified':False})
archive=W/'releases/nesnd-20261102-integrity-recheck.zip';assert not archive.exists();excluded=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for r in sorted(after):
  if r.startswith(('docs/','.scratch/','development/','tools/')) or r.endswith(('.md','.py','.pyc','.bak')):excluded.append(r);continue
  assert not any(k in r for k in ['nesnd_qa','nesnd_f2_qa','nesnd_batch_probe','nesnd_sequence_qa'])
  z.write(M/r,r)
with zipfile.ZipFile(archive) as z:
 for r in z.namelist():assert z.read(r)==(M/r).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'files':len(after)-len(excluded),'excluded':excluded,'QA_included':False,'tools_included':False})
plan=W/'plans/two-empires/20261102-qin-persia-implementation.md'
cp(plan,R/'plan-before/20261102-qin-persia-implementation.md')
write(plan,read(plan).rstrip()+'''\n\n## 完整性复查后修订（2026-11-02）

本节取代前文对应战争/新军规则。秦解体独立联盟共同羞辱秦，秦对各参战国分别吞并；新生国七条漏接入口已补。原版禁止重复羞辱同一目标，故不为每个盟友叠加；后加入者必须实际在战中或博弈中，才补秦的反向吞并。

建国只选择人口>0的实际州；无合格州不新建TAG，不造人口。新军转地后只准备一次，明确给线列步兵/火炮科技；已有军队不额外赠兵，全国与首都人口同时满足5万/10万/20万/40万时最多1/2/4/8营，低于5万为零。对应最大兵员不超过2%，不承诺实际满编。

文化复归先恢复异常残留批次，再做半数文化、整批宗教、整批目标文化转换。近期英文完成编辑复核。细节与未决引擎/历史资源问题见WORK/reports/integrity-recheck-20261102/release-notes.md及任务17；不开游戏。
''')
support={}
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if any(part.startswith('cwtools-negative-') for part in rel.parts[:-1]):continue
 if p.suffix not in {'.json','.md','.diff','.txt','.yml'}:continue
 if p.name in {'tiger_raw.json','tiger-after.json','baseline.json'} or 'protocol' in p.name:continue
 support['workbench/reports/'+R.name+'/'+rel.as_posix()]=p
for name in ['integrity_context.py','audit_integrity_contracts.py','repair_integrity_campaign.py','probe_cwtools_integrity.py','document_integrity_recheck.py','deliver_integrity_recheck.py']:
 support['workbench/tools/'+name]=W/'tools'/name
for rel in ['SKILL.md','references/active-work.md','references/validation.md','references/syntax-and-routing.md','references/content-development.md']:
 support['nesnd-skill/'+rel]=S/rel
support['nesnd-player-writing/references/author-samples.md']=S.parent/'nesnd-player-writing/references/author-samples.md'
support['workbench/plans/two-empires/'+plan.name]=plan
for rel,p in support.items():cp(p,repo/'development'/rel)
mf=repo/'development/snapshot-manifest.json';d=json.loads(read(mf));records={x['path']:x for x in d['files']}
for rel,p in support.items():records[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
d.update(files=[records[k] for k in sorted(records)],updated_utc=datetime.now(timezone.utc).isoformat(),refresh_scope='Integrity audit, actual CWTools cold-load and missing-definition control, narrow source fixes, Qin asymmetric goals/population/army guards, English editorial review; engine not run; inherited diagnostics retained.')
dump(mf,d)
print(json.dumps({'main_files':len(after),'changed_files':len(changes),'support_files':len(support),'package':str(archive),'engine_verified':False}))
