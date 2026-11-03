from cne_native_context import W,M,S,read,write,sha,man,dump
from pathlib import Path
import re,json,shutil,subprocess

R=W/'reports/france-politics-plan-20261103';repo=W/'projects/nesnd-repository'
b=json.loads(read(R/'baseline.json'));backup=Path(b['backup'])
before=b['main_files'];after=man(M)
changed={r:h for r,h in after.items() if before.get(r)!=h}
allowed={'.scratch/debug-release/map.md','.scratch/debug-release/issues/29-france-political-planning.md'}
assert set(changed)==allowed and not before.keys()-after.keys()
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==b['parent']
for rel,h in before.items():assert sha(repo/rel)==h,('Repo parent conflict',rel)
for rel in ['SKILL.md','references/active-work.md']:
    old=backup/('SKILL.md' if rel=='SKILL.md' else 'active-work.md')
    assert sha(repo/'development/nesnd-skill'/rel)==sha(old)
for name in ['canon-and-routes.md','reference-mods.md']:
    previous=repo/'development/workbench/reports/observer-finish-20261103'/name
    if previous.exists():assert sha(previous)==sha(backup/name)

plan=read(R/'france-development-plan.md')
assert 'government_legitimacy >= 50' in plan
assert '不要求指定党派组合、成员数、同党关系或特定组阁排列' in plan
assert 'devorismo.3' in plan and 'agitators_2.6' not in plan
assert '尚未改' not in plan or '计划' in plan
skill=read(S/'references/political-design-and-difficulty.md')
assert '相关IG执政＋合法性至少50' in skill
assert '不得检测指定党派成员组合' in skill and '高于50' in skill
assert 'references/political-design-and-difficulty.md' in read(S/'SKILL.md')
assert '常规执政设计以至少25' not in read(R/'party-legitimacy-source.md')

# Unrelated countries and previously proposed characters remain untouched.
old=read(backup/'canon-and-routes.md');new=read(W/'reports/observer-finish-20261103/canon-and-routes.md')
assert old.split('### FRA：兑现波拿巴繁荣，再决定帝国的政治形状')[0]==new.split('### FRA：繁荣、宫廷与外省、共和分配')[0]
assert old[old.index('### HUS：共和国的公民与大陆的土地'):]==new[new.index('### HUS：共和国的公民与大陆的土地'):]
old=read(backup/'reference-mods.md');new=read(W/'reports/observer-finish-20261103/reference-mods.md')
assert old.split('## 5. FRA专案')[0]==new.split('## 5. FRA专案')[0]
assert old[old.index('**拟新增虚构角色，尚非正史：**',old.index('## 5. FRA专案')):]==new[new.index('**拟新增虚构角色，尚非正史：**',new.index('## 5. FRA专案')):]

links=[]
for p in [R/'france-development-plan.md',R/'party-legitimacy-source.md',R/'rahf-mobilization-source.md',S/'references/political-design-and-difficulty.md']:
    for raw in re.findall(r'<([CD]:/[^>]+)>',read(p)):
        path=re.sub(r':\d+$','',raw).split('#')[0]
        assert Path(path).exists(),('Missing source link',str(p),raw)
        links.append(raw)
    for raw in re.findall(r'\]\(([^<][^)]*\.md(?:#[^)]*)?)\)',read(p)):
        if raw.startswith(('http','C:','D:')):continue
        assert (p.parent/raw.split('#')[0]).exists(),('Missing relative link',str(p),raw)
dump(R/'validation.json',{'status':'DOCUMENT_REVIEW_PASS','gameplay_changed':False,'game_launched':False,'engine_validation':'NOT_APPLICABLE: research and design only','main_document_changes':changed,'valid_local_source_links':len(links),'unrelated_country_plans_preserved':True,'political_gate':'relevant IG in government + legitimacy >= 50; no party composition conditions','backup':str(backup),'plan_sha256':sha(R/'france-development-plan.md'),'skill_sha256':sha(S/'references/political-design-and-difficulty.md')})

for rel in changed:
    dst=repo/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(M/rel,dst)
for rel in ['SKILL.md','references/active-work.md','references/political-design-and-difficulty.md']:
    dst=repo/'development/nesnd-skill'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,dst)
for name in ['canon-and-routes.md','reference-mods.md']:
    dst=repo/'development/workbench/reports/observer-finish-20261103'/name;dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(W/'reports/observer-finish-20261103'/name,dst)
for name in ['france-development-plan.md','party-legitimacy-source.md','rahf-mobilization-source.md','validation.json']:
    dst=repo/'development/workbench/reports/france-politics-plan-20261103'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/name,dst)
for name in ['record_france_political_plan.py','save_france_political_plan.py']:
    shutil.copy2(W/'tools'/name,repo/'development/workbench/tools'/name)
subprocess.run(['git','add','--all'],cwd=repo,check=True)
subprocess.run(['git','-c','core.whitespace=blank-at-eol,space-before-tab,cr-at-eol,-blank-at-eof','diff','--cached','--check'],cwd=repo,check=True)
subprocess.run(['git','commit','-m','Plan French political development with accessible government goals'],cwd=repo,check=True)
print('Political constraints, local links and unchanged gameplay verified; research saved')
