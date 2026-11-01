"""Preserve the current work and record the user's log-first delivery policy."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
P=W/'exports/resumed-integrated-20261101-a'
C=W/'exports/release-logfix-20261101-a'
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
B=W/'backups'/('pre-logfix-release-'+stamp)
def manifest(p):return {f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file()}
def write(p,s):p.write_text(s,encoding='utf-8')
assert not C.exists(), 'Do not overwrite a candidate'
B.mkdir(parents=True)
for name,src in [('main-mod',M),('skill',S),('candidate-parent',P)]:
    before=manifest(src);shutil.copytree(src,B/name);assert manifest(B/name)==before
    write(B/(name+'-manifest.json'),json.dumps(before,ensure_ascii=False,indent=2))
shutil.copytree(P,C);assert manifest(C)==manifest(P)
policy='''# 日志优先的增量交付

2026-11-01用户明确纠正验证成本。本页为当前验证顺序；旧运行报告保留证据价值，其逐步截图/多次重载流程不再是每次开发的必做清单。

1. 写功能前读当前原版同类完整链条，记下路径、版本和适用差异。复用已证实的写法，保序解析重复键。
2. 先归档当前 error.log/debug.log 与实际候选指纹，按错误内容和最早项目调用位置去重。先修项目脚本错误及每帧刷屏根因；截图计数不是根因列表。
3. 批量检查按钮、选项、effect、trigger、script_value、初始化和清理闭包。按钮不可用也可能预览 effect；预览不承诺前面的 set_variable 已执行。hidden_effect 只影响展示。
4. typed 对象用可选 scope 或明确条件分支保护；普通 AND/OR 和并列 has_variable 不作为短路保证。缺失对象的有效性谓词返回 false；缺失数值只在有定义的展示语义下使用安全 script_value。移除修正先在同一 scope 判断 has_modifier。
5. 优先运行现成有序 parser、引用/资源/地图全链、Tiger及实际 stdio MCP。增加与已捕获错误模式对应的小检查，不建另一个游戏模拟器。MCP查询不冒充引擎执行。
6. 地图集合、ownership、人口/建筑/资源守恒、hub/locator/海域/交通链检查通过且已有相同写法实测后，复用结论。进港、死亡、分裂或任命已成功一次即关闭该项；只有存档格式、加载/迁移逻辑变更或真实复发证据才重载复测。读档本身不重置这些已完成行为。
7. 仅无法由日志和外部工具回答的新增引擎语义做一次定向实测。复现按钮错误用新增日志是否再次出现判断；视觉错误才截图。检查通过即推进交付，不重复开局/进港/截图收集同一事实。
8. 正式包只包含玩法和必要资源。QA浮层、控制台按钮、测试事件/on_action、夹具、验证程序、原版/工坊素材和测试存档留在WORK独立debug目录，或由明确DEBUG开关控制；正式profile不加载QA。不要删除独立备份和历史证据。
9. 保留通过机制、主MOD新增配置和数据，备份后作逐文件三方整合。用户已授权本轮修复后直接整合主MOD及主Git分支；不再重复申请此前合并审批。报告已修问题、实际检查范围及仍存在的具体限制，不承诺证明所有未来玩法绝无BUG。

## 本轮已证写法与边界

- EACR女性special_genes配件用add保留基础发型；两条旧replace导致秃发。仅独立兼容脚本引用EAC资源，脚本UTF-8 BOM，禁止搬运第三方资产。
- 地图拆州沿现有province、完整联动history/states/pops/buildings/resources/战略区/州引用/hubs/locators/海路。已完成闽江、高凉、北大原实际入港；复用原生证据，无需重复重载舰队。
- 陈死亡压力在event immediate结算；JE初始化只在变量不存在时置零。已实证0→25→确认intro仍25→周显示25。
- Lin任命以实际owner和country.ruler确认，pending捕获原对象后转属；完成flag不代替实际对象。已实证吞并→三国恢复→同一Lin任摄政王。
- 原生events/JE数据库保留dead墓碑，静态对象存在/active字段不独立证明仍活跃。预算、bar等缓存与真实变量分开解释。

详细源依据和实测记录保留WORK/plans/two-empires/evidence与reports/runtime/20261101T014437Z；只对受改闭包重查。
'''
write(S/'references/log-first-delivery.md',policy)
p=S/'SKILL.md';s=p.read_text('utf-8-sig')
old='8. 验证遵循 [工具与游戏验证](references/validation.md) 和 [日志判读](references/error-log.md)。修改后必须在实际游戏中走时间及触发相关事件，覆盖可达选项、成功/失败/中断路径、必要组合和读档；静态检查不替代此门槛。未覆盖项逐项列明，不声称证明了所有随机未来。'
new='8. 验证先按 [日志优先的增量交付](references/log-first-delivery.md)：先修error.log根因，集中外部工具/MCP检查，复用已经成功的行为证据；只有未决引擎语义做一次定向验证。避免重复开局、读档和进港截图。层次与能力边界见 [工具与游戏验证](references/validation.md)。'
assert old in s;s=s.replace(old,new);write(p,s)
for name in ['validation.md','incremental-editing.md','active-work.md']:
    p=S/'references'/name;s=p.read_text('utf-8-sig');pos=s.find('\n')+1
    s=s[:pos]+'\n当前优先：[日志优先的增量交付](log-first-delivery.md)。2026-11-01用户已取消重复进港/读档/截图验收，要求修日志错误、外部检查优先、正式包排除QA，并授权修复后直接整合。以下历史流程仅按受改范围选用。\n'+s[pos:];write(p,s)
p=M/'AGENTS.md';s=p.read_text('utf-8-sig');s+='\n当前验证顺序按 [日志优先交付](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/log-first-delivery.md>)：修复日志根因、外部工具/MCP优先，已验证行为不重复开局或读档；正式包排除QA工具。\n';write(p,s)
p=M/'docs/agents/engineering-skills.md';s=p.read_text('utf-8-sig');s+='\n2026-11-01最新授权：按 [日志优先交付](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/log-first-delivery.md>)收口按钮报错，复用既有实测，正式包排除QA。已知问题修复并完成必要检查、独立备份后直接合入主MOD与主Git分支；此授权取代本轮此前的最终合并再次审批。\n';write(p,s)
p=M/'.scratch/debug-release/map.md';s=p.read_text('utf-8-sig');s=s.replace('此前主 MOD 最终合并清单审批保留，当前不发起问题。','2026-11-01最新授权已改为：修复已知BUG、完成必要检查及备份后直接整合主MOD与主Git分支。')
s+='\n## 最新纠正：日志优先收口\n\n进港已正常，停止反复开局/读档/截图。优先修supply按钮预览缺失scope及其他error.log根因，运行外部静态/MCP检查；正式包不含QA覆盖层。已知问题修复与必要检查后直接备份合入。完整规则见技能log-first-delivery.md。原始功能欠账保留，未完成候选不混入本次BUG修复正式包。\n';write(p,s)
R=W/'reports/logfix-release-20261101';R.mkdir(exist_ok=True)
logs=W/'runtime/profiles/20261101T014437Z/logs'
for n in ['error.log','debug.log']:
    if (logs/n).exists():shutil.copy2(logs/n,R/('input-'+stamp+'-'+n))
write(R/'preparation.json',json.dumps({'backup':str(B),'candidate':str(C),'parent':str(P),'parent_manifest':manifest(P),'policy':'log-first, no repeated harbor/reload QA, release excludes debug overlay','main_merge_authorized':True},ensure_ascii=False,indent=2))
print(json.dumps({'backup':str(B),'candidate':str(C),'policy_written':str(S/'references/log-first-delivery.md')},ensure_ascii=False))
