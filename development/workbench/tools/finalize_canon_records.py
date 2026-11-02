from canon_prose_context import *
import collections,datetime

def signature(n):
    return (n['severity'],n['key'],n['message'],tuple((v.get('from'),v.get('path'),(v.get('line') or '').strip()) for v in n['locations']))
a=json.loads(read(W/'reports/japan-development-20261102/tiger-baseline.json'))
b=json.loads(read(R/'tiger-candidate.json'))
ac=collections.Counter(map(signature,a));bc=collections.Counter(map(signature,b));added=[];removed=[]
for n in b:
    k=signature(n)
    if ac[k]:ac[k]-=1
    else:added.append(n)
for n in a:
    k=signature(n)
    if bc[k]:bc[k]-=1
    else:removed.append(n)
assert not added,(len(added),added[:3])
dump(R/'tiger-delta.json',{'baseline':len(a),'candidate':len(b),'added':added,'removed':removed,'engine_verified':False,'note':'Inherited diagnostics remain; zero added is not a clean whole-mod audit.'})

write(R/'review-aggregate.md','''# 两轴复核

## Standards
首轮1项P2：英文易代压力提示遗漏1837/1838首辅案与1839保底推进。已补齐全部中英文覆盖，并明确需首辅案已有结果。复核者独立确认修复，剩余0项。详细原报告及修复SHA见standards-review.md、standards-resolution-verification.json。

## Spec
0项可执行问题。已核附件79键、有效覆盖、明吴实际终局、CNE地方范围和终止效果、波斯关系分支。详见spec-review.md。

两轴是源码和编辑判断，均未执行游戏。日本新增玩法不属于本次主MOD文案交付范围。两处按钮desc缩进调整前后AST一致；最终文件SHA以delivery清单为准。
''')

notes='''# 制度设定与中英文案修订

本批为任务22。日本新增玩法仍在独立候选，未混入本批主MOD交付。

## 变更

- 审核CNE、南朝明吴、西秦/波斯、既有日本、吕宋、丹那沙林、地图说明等当前AI文本；657个既有或新增键修订，包含中文、英文和同键覆盖层。作者成熟原文保留，作者本轮附件原样另存。
- 记录六部、元老院、咨议局、礼议院、南西府、省制与学政；统一实际权限和称谓。国家礼法、军阀联盟和对外条约分别表达。明20→22、吴21→23为实际和平结果；旧事件10、旧HNA三按钮保持停用，不将改稿当成新玩法。
- CNE清丈事件保存具体改革州并提供安全后备描述；极端军事失控按全国危机描述。妥协事件在选择前是草案，“停止地权革命”明确为永久结束。
- 遣使按钮按拥明/拥吴显示不同政治目标，使用原版Cuba按钮已有的triggered_desc结构；既有条件和结算数值保留。
- 英文文件中的中文占位和作者中文改稿重新翻译；消除开发说明、角色动作与实际effect不符等问题。波斯在秦已不存在、交战或另属第三国时不再收到秦援助；朝贡结果按实际关系显示。
- skills保存作者本轮制度纠正和逐项对读要求，明确逗号/主语/范围/有效覆盖层/实际效果审查。

## 检查与边界

182项外部检查通过；6次实际MCP源码查询通过；Tiger基线553、候选553，新增诊断0。原有553项含继承缺项和工具能力差异，未宣称全MOD零错误。两轴审查：Spec0项，Standards1项已修并独立确认。

未启动游戏。文化、人口、地图、建筑、原有事件数值未改。CNE选项effect逐项AST核对保持；新增只是地点选择与呈现。波斯源头守卫是本次发现并修复的有限逻辑问题。

## 仍未完成

1. 日本候选：三国产业/团结/政治/外交及Lin迁JIM已写入，仍需最终生命周期检查、整批外部测试和交付。最新文案同步进候选，但不能凭本批182项测试认证日本新代码。
2. 日本交付后的一次游戏启动、切国→观察者→五速运行仍未执行。用户授权继续保留，须先完成前述测试。
3. 印度与土邦、法国关系方案尚未实施；南朝概率profile、一次选边、密使、文化首都权重等旧计划仍在.scratch/south-allegiance，未以本次礼法重写冒充实现。

作者原稿、主MOD用户编辑、日本候选及skills的修改前副本见pre-canon-prose-20261102T213403Z。最终主MOD差分部署与Git记录分别在main-merge.json、git-delivery.json；存在记录才代表已完成相应保存。
'''
write(R/'release-notes.md',notes)
write(R/'mcp-query-notes.md','''# MCP查询边界

实际服务器get_structure在key_path只有一段时返回块概要；两段及以上才展开。布尔yes回传True。重复option路径不能据单一路径输出推断完整多选项；本批完整选项使用保序pdx解析器核对。

初次探测的断言失败是查询深度/布尔表达与重复键路径选择问题，未证明游戏脚本失败。最终六次查询及原始返回保存于mcp-source-queries.json。工具查询不会运行游戏。
''')

write(S/'references/active-work.md','''# 当前交接：作者制度纠正与中英文案

Updated: 2026-11-02。当前入口为主MOD任务22（.scratch/debug-release/issues/22-canon-prose.md），证据WORK/reports/canon-prose-20261102/。作者最新制度权威见north-south-institutions.md；写作按nesnd-player-writing执行。

本批修订657键及相应有效呈现，原稿独立保留；外部182检查/MCP6/Tiger零新增，两轴问题已收口。是否完成主MOD/Git保存看本报告目录main-merge.json/git-delivery.json。游戏未启动，不能标ENGINE_PASS。

日本任务21继续：候选WORK/exports/japan-development-20261102-a，父c4bbc194ddafcb2bb62f2bb89746c95f0b7b7f49。三国产业、团结、政治、外交、朝鲜与Lin迁JIM已写入；最终生命周期、全量测试、主MOD部署及观察者运行未完成。当前文案已同步候选；依赖新机制的文案仅在该候选。不要重跑旧build脚本覆盖后续修补。断点详见本轮work-state-and-request.md与WORK/reports/japan-development-20261102/。

用户允许全部更新与测试完成后开游戏，切入任意国家再观察者，五速运行留待用户；启动/崩溃则读错误报告定向修复。此授权未执行，不得跳过测试。旧不开游戏要求在此受限授权内被取代。

印度/土邦/法国与南朝概率/密使待办保持各自map，仍为方案。最初游戏数据和既有崩溃链保持；不得把文案交付等同这些新玩法完成。
''')

for root in (E,C):
    rel='.scratch/debug-release/issues/22-canon-prose.md'
    if root==C:shutil.copy2(E/rel,C/rel)
    p=root/rel;s=read(p).replace('Execution: claimed','Execution: completed').replace('Validation: NOT_RUN','Validation: STATIC_PASS')
    s+='\n## Result\n\n源码与文案交付完成；182项外部检查、MCP6、Tiger零新增，两轴问题已收口。主MOD/Git保存以WORK/reports/canon-prose-20261102/main-merge.json和git-delivery.json为凭。日本新玩法未合入，游戏未启动；边界和待办见release-notes.md。\n'
    write(p,s)
    if root==C:shutil.copy2(E/'.scratch/debug-release/issues/21-japan-implementation.md',C/'.scratch/debug-release/issues/21-japan-implementation.md')
    p=root/'.scratch/debug-release/map.md';s=read(p)
    s+='\n## 当前：日本候选与作者制度纠正（2026-11-02）\n\n[21 日本实施](issues/21-japan-implementation.md)已写入独立候选，尚未最终测试/合入；[22 制度与中英文案](issues/22-canon-prose.md)已完成外部检查与文案复核。作者最新设定已记录并修改657键，保留旧记录。实际交付和未完成项见WORK/reports/canon-prose-20261102/release-notes.md；未启动游戏。\n'
    write(p,s)
    p=root/'.scratch/japan-development/map.md';s=read(p)
    s+='\n## 最新实施断点（2026-11-02，取代上文尚未实施状态）\n\n[任务21](../debug-release/issues/21-japan-implementation.md)已写入WORK/exports/japan-development-20261102-a，尚待最终生命周期检查、整批外部验证和合入。[任务22](../debug-release/issues/22-canon-prose.md)的作者设定及文案修订同步进入候选。上方研究历史保留；不开游戏限制已受用户最新的一次完成后观察者运行授权取代，当前尚未运行。\n'
    write(p,s)

print('Records finalized; runtime unverified and Japan/India/South remaining work explicit.')
