from cne_native_context import W,M,S,read,write,sha,man,dump
from pathlib import Path
import re,json,shutil,subprocess
R=W/'reports/italy-lombardy-correction-20261103';repo=W/'projects/nesnd-repository'
plan=W/'reports/cne-time-native-ban-20261103/italy-research-plan.md'
b=json.loads(read(R/'baseline.json'));backup=Path(b['backup']);before=b['main_files'];after=man(M)
changed={rel:h for rel,h in after.items() if before.get(rel)!=h}
allowed={'.scratch/debug-release/issues/28-cne-time-native-ban.md','.scratch/debug-release/map.md'}
assert set(changed)==allowed and before.keys()==after.keys()
old=read(backup/'italy-research-plan.md');s=read(plan)
def span(text,a,z):return text[text.index(a):text.index(z)]
for a,z in [('### 地区经济','## 三、'),('## 五、','## 六、'),('### 阶段C：','## 七、')]:assert span(old,a,z)==span(s,a,z)
assert all(x in s for x in ['法国主导的“伦巴第共和国”','ITA_GUGLIELMO_PEPE','加里波第及原生统一剧情：局部适配计划','尚未改代码','亲法与民族主义是作者确认'])
assert '建议将“共和国称号”和“阿尔卑斯边界要求”解耦' not in s
assert '民族主义者挑战法国宗主权，先通过外交或战争取得现实行动空间' not in s
links=[]
for p in [plan,R/'source-check.md',R/'garibaldi-chain-audit.md']:
    for raw in re.findall(r'<([CD]:/[^>]+)>',read(p)):
        path=re.sub(r':\d+$','',raw).split('#')[0]
        assert Path(path).exists(),('Missing source link',str(p),raw)
        links.append(raw)
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
assert sha(repo/'development/workbench/reports/cne-time-native-ban-20261103/italy-research-plan.md')==sha(backup/'italy-research-plan.md')
assert sha(repo/'development/nesnd-skill/references/active-work.md')==sha(backup/'active-work.md')
for rel,h in before.items():assert sha(repo/rel)==h,('Repo changed',rel)
dump(R/'validation.json',{'status':'DOCUMENT_REVIEW_PASS','gameplay_changed':False,'game_launched':False,'engine_validation':'NOT_APPLICABLE: plan only','main_document_changes':changed,'preserved_sections':['地区经济','参考MOD具体取用与排除','统一后的国家建设'],'valid_local_source_links':len(links),'plan_sha256':sha(plan),'source_check_sha256':sha(R/'source-check.md'),'garibaldi_audit_sha256':sha(R/'garibaldi-chain-audit.md'),'backup':str(backup)})
for rel in changed:shutil.copy2(M/rel,repo/rel)
shutil.copy2(plan,repo/'development/workbench/reports/cne-time-native-ban-20261103/italy-research-plan.md')
shutil.copy2(S/'references/active-work.md',repo/'development/nesnd-skill/references/active-work.md')
for name in ['source-check.md','garibaldi-chain-audit.md','revision-scope.json','validation.json','lombardy-plan.diff']:
    p=repo/'development/workbench/reports/italy-lombardy-correction-20261103'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/name,p)
for name in ['revise_lombardy_plan.py','finish_lombardy_plan.py','save_lombardy_plan_revision.py']:
    shutil.copy2(W/'tools'/name,repo/'development/workbench/tools'/name)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check','--','.',':(exclude)development/workbench/reports/**'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Correct Lombardy planning premise and audit Garibaldi event adaptation'],cwd=repo,check=True)
print('Documentation reviewed; game files unchanged; source links checked:',len(links))
