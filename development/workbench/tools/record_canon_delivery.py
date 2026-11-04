"""Record completed deployment; edit documentation only, preserving prior records."""
from canon_routes_context import C, M, R, W, S, man, sha, read, write, dump
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

repo = W / 'projects/nesnd-repository'
code_commit = 'f05f0639d3cba02206fb357043a90deb32ba8c47'
branch = 'feature/canon-routes-20261104T203047Z'
git = lambda *args: subprocess.check_output(['git', *args], cwd=repo, text=True, encoding='utf-8').strip()
assert git('rev-parse', 'HEAD') == code_commit
assert not git('status', '--porcelain')
remote = git('ls-remote', 'origin', 'refs/heads/main', 'refs/heads/' + branch)
assert all(line.startswith(code_commit + '\t') for line in remote.splitlines())
assert len(remote.splitlines()) == 2
validated = json.loads(read(R / 'final-validation.json'))
assert man(C) == man(M) == validated['source_files']
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
archive = R / 'archive' / ('pre-delivery-records-' + stamp)
issue_rel = '.scratch/debug-release/issues/34-canon-route-execution.md'
map_rel = '.scratch/debug-release/map.md'
plan = W / 'plans/two-empires/63-canon-route-execution.md'
targets = {
    'issue34.md': C / issue_rel,
    'map.md': C / map_rel,
    'work-state.md': R / 'work-state.md',
    'steer-implementation-ledger.md': R / 'steer-implementation-ledger.md',
    'agent-execution-plan.md': R / 'agent-execution-plan.md',
    'plan63.md': plan,
    'active-work.md': S / 'references/active-work.md',
}
archived = {}
for name, source in targets.items():
    target = archive / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    assert sha(source) == sha(target)
    archived[name] = {'source': str(source), 'sha256': sha(target)}
dump(archive / 'manifest.json', archived)
archive_link = archive.as_posix()
report_link = R.as_posix()
common = f'''任务34已完成实现、外部检查、独立审查、备份和主MOD部署。游戏代码提交`{code_commit}`已快进合入本地main并推送私有远端；功能分支`{branch}`亦保存。远端两分支SHA已核。

验证为**STATIC_PASS / ENGINE_NOT_RUN**，游戏1.13.11/build24799966。本轮未开启游戏；实际UI、调度、自然AI经济、战争与存读档仍待实机。候选/主MOD/备份/提交的1015文件已核对；相对父b94582e有189变化（187游戏文件＋2任务文档），无删除/冲突。本次只补交接文档，不改已验证玩法字节。

证据入口：`final-validation.json`、`final-reviews-summary.md`、`release-notes.md`、`main-merge.json`、`git-delivery.json`、`deployment-byte-verification.json`；均在[{R.name}](<{report_link}>)。两轴和独立文案最终剩余确认问题0。Git空白检查的162条非功能诊断经显式复核保留，未冒写检查返回0。
'''
scope = '''|批次|交付内容|最终外部证据|
|---|---|---|
|A1|HUS独立社会阶序法组＋三法、公民权锁、文化/职业接纳、12月登记及退出|batch-a-validation.json|
|B1|西秦/日本/印度/土耳其团结政策、法组分行、TUR扩张后团结、坦志麦特分支奖励|batch-b-validation.json|
|C1|埃及六方条约/独立性即时结算；PRU/AUS/USA实际外交与扩张|batch-c-repair4-validation.json；B2闭合共享接口|
|A2|MEX/安第斯复国、流亡、HUS登记迁徙、原住民汗国、人口/军力/宣称/战争终局|batch-a2-repair3-validation.json|
|B2|印度/南洋小国与远南缅甸暹罗区域发展、市场、自主、运动及外交请求|batch-b2-repair2-validation.json|
|C2|意大利/HUS/USM十条建设分支、27选择、18虚构人物及原版意大利兼容|batch-c2-repair3-validation.json|
|最终显示/文案|效果预览、真实双边报价、旧报价反例、无重复奖励；作者原文对读和政体称谓修正|final-button-preview-repair1-validation.json；final-writing-independent-review-r2.json|
'''
backlog = '''## 未完成与后续边界

- 本轮自然引擎运行未做，由用户自行测试；不再重复已验证的进港/死亡/分裂截图。不用STATIC_PASS冒称游戏内零BUG。
- 历史人口、开局法律与1825投资条约主要在新开局生效。不要再次运行人口重配脚本叠改当前数据；旧档不自动重演全部初始化。
- 任务29的法国完整政治发展，任务31的法国古吉拉特/本地舰队与日本追加政治选择，任务08的编辑器等旧欠账继续保留在原任务。任务34中意大利/HUS/USM与小国路线已实际落库，不能再视为仅计划。
- 物质补贴主流文化代价为每月0.1%离散激进化近似；满蒙迁徙70/30是按源pop的目的地概率。具体实现差异与自然运行限制见release-notes，不隐去设计近似。
'''
models = '''## 模型与组织

两份自定义SKILL已强制：Luna/high探索、Sol/medium脚本审查、Astra/high计划草案；root保留架构、最终计划结构、数值正确性及最终整合。同任务按计划→编辑→冻结→测试分阶段。工具仅有gpt-6-astra，无gpt-6.1-astra；已披露替代，未使用Astra xhigh或以上。实际每个代理/阶段、失败spawn及旧未知继承配置见model-delegation-register.md，不能从代理名猜模型。
'''
write(R / 'work-state.md', '# 当前交付：任务34完成\n\n' + common + '\n' + scope + '\n' + backlog + '\n' + models + f'\n所有旧断点原字节保留于[交接档案](<{archive_link}/work-state.md>)，SHA见同目录manifest.json。后续恢复从本页进入，不按历史“当前仍未合入”重新执行人口迁徙或覆盖主MOD。\n')
write(R / 'steer-implementation-ledger.md', '# 任务34最终落实账\n\n' + common + '\n' + scope + '''
## 最新steer逐条落实

|用户纠正|实际结果|
|---|---|
|埃及投资人存在但不能收属|当前主投资人统一存在＋独立资格；原生事件取消条件与既有维护清理；零独立性即时结果，无90天待处置|
|远南/缅甸/暹罗不是微型国家|真实人口/直辖地区分类，分区域经营、公共服务、市场和自主；变化有持续期与迟滞，非一套建筑数量倍乘|
|不同法组分开列进度|各团结度法律影响按法组拆行，原同组if/else保留，显示法组名|
|HUS三法与公民权冻结|独立社会阶序法组、文化职业分层、三条法律；施加对象/普通立法/原住民终局全链验证|
|TUR改革失败不能封后续|扩张日志各结果可入；改革结果影响增长与奖励，直接州规模控制团结度开放|
|团结度两补贴|资金与主流文化代价/合法性−10两按钮，12月不可提前取消，月增团结与同化增益|
|严格模型分工|两SKILL写入强制条款；已知实际模型/effort逐代理记录；root裁定数值与整合|
|必须实现并入主MOD|六批玩法已部署、main与远端f05f063一致；非只交方案|
''' + '\n' + backlog + f'\n原始需求、逐轮失败与修复记录不删除，见[旧落实账](<{archive_link}/steer-implementation-ledger.md>)及各批报告。\n')
old_agent = read(R / 'agent-execution-plan.md')
write(R / 'agent-execution-plan.md', '# 最终阶段：全部批次已交付\n\n' + common + '\n' + models + '\n以下为当时的安排与阶段记录，当前结论以本页顶部和model-delegation-register为准。\n\n---\n\n' + old_agent)
issue = f'''# 34 作者意见落实、HUS阶序与团结度

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root（组织、裁定、整合）；显式配置代理（分批实现与交叉审查）
Blocked by: none
Validation: STATIC_PASS
Evidence: [最终外部验证](<{report_link}/final-validation.json>)

## Result

{common}
{scope}

{backlog}

{models}

Status保留ready-for-human表示用户后续实机测试；不表示等待再次批准已经完成的合入。旧任务全文和阶段失败记录已[独立归档](<{archive_link}/issue34.md>)。最新具体状态见[工作交接](<{report_link}/work-state.md>)。
'''
write(C / issue_rel, issue)
old_map = read(C / map_rel)
prefix = f'''最新交付（2026-11-04）：[任务34](issues/34-canon-route-execution.md)已完成六批国家路线、HUS法律/人口/原住民汗国、各团结度及全部最新steer，主MOD和Git main/远端代码为`f05f063`。STATIC_PASS，未开游戏；187游戏文件＋2任务文档变化，无删除。实际模型与未完成旧任务见任务34和WORK/reports/canon-route-execution-20261104/work-state.md。本页下面的旧“当前”段均是历史，不能回退本次交付。
'''
first, remainder = old_map.split('\n', 1)
write(C / map_rel, first + '\n\n' + prefix + '\n' + remainder)
for rel in (issue_rel, map_rel):
    for root in (M, repo):
        shutil.copy2(C / rel, root / rel)
old_active = read(S / 'references/active-work.md')
marker = '# 历史交接：任务33'
assert marker in old_active
history = old_active[old_active.index(marker):]
write(S / 'references/active-work.md', '# 当前交付：任务34已合入（2026-11-04）\n\n' + common + '\n恢复优先读取WORK/reports/canon-route-execution-20261104/work-state.md、release-notes.md及项目任务34。六批均已实现并外部验证，不要从旧断点重做。两SKILL的强制模型分工已落库，实际配置见同报告model-delegation-register.md。\n\n' + backlog + f'\n修改前完整交接逐字归档于[{archive.name}](<{archive_link}/active-work.md>)，SHA见manifest.json。\n\n' + history)
old_plan = read(plan)
write(plan, '# 计划63交付结果（2026-11-04）\n\n' + common + '\n' + scope + '\n' + backlog + '\n---\n\n# 以下为原始计划与逐阶段设计；状态以顶部交付结果为准\n\n' + old_plan)
after = man(M)
delta = {rel: h for rel, h in after.items() if validated['source_files'].get(rel) != h}
assert set(delta) == {issue_rel, map_rel}
assert man(C) == after
dump(R / 'delivery-documentation-delta.json', {'source_code_commit':code_commit, 'documentation_only':delta, 'gameplay_files_unchanged':True, 'full_source_files':after, 'archive':str(archive), 'engine_verified':False})
dump(R / 'git-delivery.json', {'code_commit':code_commit, 'main_remote_verified':code_commit, 'feature_branch':branch, 'feature_remote_verified':code_commit, 'main_mod_deployed':True, 'status':'DELIVERED_STATIC_PASS', 'engine_verified':False, 'documentation_receipt_pending_commit':True, 'package':json.loads(read(R/'package.json')), 'document_only_delta':'delivery-documentation-delta.json'})
dump(R / 'skill-review-final-20261104.json', {'sources':{'nesnd-victoria3':sha(S/'SKILL.md'), 'nesnd-player-writing':sha(S.parent/'nesnd-player-writing/SKILL.md')}, 'changes':['Both modules strictly require explicit model/effort delegation and root architecture/numeric/integration responsibility','Active handoff replaced stale task34 instructions with archived originals and actual delivery','Current native examples, legal chain, population preservation, medium-country regions and display contracts retained'], 'new_gameplay_changes':False, 'limits':['No engine validation','6.1 Astra unavailable; actual gpt-6-astra/high disclosed','Earlier inherited models unknown'], 'evidence':'model-delegation-register.md; final-validation.json'})
for item in R.rglob('*'):
    if item.is_file() and item.suffix in {'.md','.json','.diff'} and item.stat().st_size <= 3_000_000:
        target = repo/'development/workbench/reports'/R.name/item.relative_to(R)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(item,target)
shutil.copy2(plan,repo/'development/workbench/plans/two-empires'/plan.name)
shutil.copy2(S/'references/active-work.md',repo/'development/nesnd-skill/references/active-work.md')
shutil.copy2(W/'tools/record_canon_delivery.py',repo/'development/workbench/tools/record_canon_delivery.py')
print(json.dumps({'recorded':True,'gameplay_files_unchanged':True,'document_delta':len(delta),'archive':str(archive),'source_commit':code_commit}))
