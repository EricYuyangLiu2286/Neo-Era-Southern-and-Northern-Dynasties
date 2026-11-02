from maintenance_20261102_context import *
P=S.parent/'nesnd-player-writing'
targets=['SKILL.md','references/active-work.md','references/narrative-context.md','references/journal-text-contract.md','references/author-prose-profile.md']
for rel in targets:
 dest=R/'skill-before'/rel
 if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,dest)
for rel in ['SKILL.md','references/author-samples.md']:
 dest=R/'skill-before'/'nesnd-player-writing'/rel
 if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,dest)
p=S/'SKILL.md';s=read(p).replace('5. 文本、事件、人物与图片先读','5. 撰写或修订玩家文本必须调用 [nesnd-player-writing](../nesnd-player-writing/SKILL.md)，完成作者原文取样、逐项对读和返工。文本、事件、人物与图片先读')
s=s.replace('9. 开局和危机先按','9. 新增或调整数值前必须读 [数值量纲与成本](references/numeric-scale-contract.md)，核实际上下限、基线、期限、叠加与重复领取。开局和危机先按')
write(p,s)
p=S/'references/narrative-context.md';s=read(p);s=s.replace('## 读取顺序','玩家文本的完整写作与审查流程由独立技能 [nesnd-player-writing](../../nesnd-player-writing/SKILL.md)维护；本页只负责设定与资料路由。涉及条件展示同时读 [日志契约](journal-text-contract.md)。\n\n## 读取顺序');write(p,s)
p=S/'references/journal-text-contract.md';s=read(p)+'''

## 原生条件优先与状态节制（2026-11-02）

- 先读作者原始日志/按钮的 trigger，再查当前 GAME 同类条目。能直接呈现的法律、科技、机构、建筑、国库等条件直接写在 possible/complete，独立条件各占原生勾叉。不要把多项真实门槛塞入一个 custom_tooltip；换行不能替代独立真假状态。
- 全国等级用 country_has_building_type_levels = { target = bt:building_iron_mine value >= 25 }（GAME/common/scripted_buttons/07_japan_buttons.txt）；州分布另用 any_scope_state 的 count 与 state_has_building_type_levels。五州各有五级城镇中心不等于每州须同时达到全国工业总量。
- custom_tooltip 只用于原生显示无法说明的自定义统计/对象选择，以及未自动呈现的必要效果；写最短的可判断条件。原生 effect 已显示关系变化，就不再加一行相同数字。内部存在性、schema、重复执行保护用 hidden_trigger，但不能隐藏真实玩家资格或费用。GAME/common/scripted_buttons/00_balkan_wars_buttons.txt 有原生隐藏示例。
- AI 谨慎阈值与玩家资格分别维护。用户指定仅供 AI 的政力、破产、失序限制，放 is_ai 分支/AI选择权重，不能悄悄变成玩家硬门槛。玩家仍须支付实际费用；该规则不自动删除完成条件或进度公式里的同名指标。
- status_desc 用 first_valid/triggered_desc 呈现当前阶段；没有新增信息时留空。未发生的起义不在开场预告。状态不复述按钮已列的门槛；按钮 desc 不复述原生效果。统计面板只保留读数。
- 检查同国同时激活的全部 JE 挂载。两个名称不同、调用同一操作的按钮依然可能重复；删除冗余挂载不删除其他日志或 AI 使用的 effect。

本轮来源与前后对照：WORK/reports/ui-trade-feedback-20261102/research.md、WORK/reports/ui-poland-tributary-20261102。源码检查不能证明实际UI布局。
''';write(p,s)
write(S/'references/numeric-scale-contract.md','''# 数值量纲与成本：改数值前必读

适用于事件、日志、按钮、修正、进度条、AI权重，以及设计提案中的候选公式。先核本机版本，再定数字；不能凭“+10看起来小”或“百分号看起来大”判定收益。

1. 写明数值属于哪一层：库存、每期流量、容量、比率、百分点、概率权重、进度；记录接口和scope。按当前 GAME 定义核上下限及转换规则，不混淆同名概念。
2. 记录开局和目标阶段的典型分母/基线，成本占比、持续时间、冷却与获取频率。没有实测时明确“源码估算”，不要捏造当前经济读数。
3. 从触发、门槛、扣款、收益、拒绝、超时、结束到重试走完整回路。更新门槛和文字；检查重复领取、叠加上限、提前退款、延迟请求期限和存档标记。
4. 用代表性极值与重复路径算结果：最小/最大基线、一次/多次、期满前后、拒绝/取消。静态算式通过不等于难度已实测。
5. 区分修复量纲错误与主动平衡调整，记录原值、新值、依据及适用档期。原生效果已展示的数字不要在自定义提示里再重复。

## 本机1.13.11已核实例

- 关系范围是−100至+100；总跨度200不等于上限200。change_relations 的 value=10 是直接10点；不要与关系进度转换混用。
- 国家影响力容量没有统一1000上限；国家等级基础约600–1100，另受制度、集团与修正影响。外交 leverage 的1000上限不是 influence 上限。
- country_influence_add 是生成侧加值，可受生成倍率影响；不能承诺它与直接增加usage完全等价。百分比修正、固定容量与货币库存分别处理。
- 本轮商使费用由−15改−100持续6个月、首次通商直接关系+25、完成奖励由+25改+100持续24个月。这是本项目平衡选择，不是原版接口强制值；首联与完成标记防止循环刷奖励。

具体源码、行号和期限追踪见 WORK/reports/ui-trade-feedback-20261102/research.md；未来版本先查原文件，不把这些实例当永恒常量。
''')
p=P/'SKILL.md';s=read(p)
s=s.replace('把原文、候选、问题、修改决定并排保存在 `WORK/reports/<本轮>/writing-comparison.md`。','把原文、候选、问题、修改决定并排保存在 `WORK/reports/<本轮>/writing-comparison.md`；用户指定其他报告名时沿用，不复制第二份审查记录。')
s=s.replace('- 同一事实只说一次。','- 条件优先用原生 trigger 逐项显示勾叉，能不用 custom_tooltip 就不用；自定义提示只补原生无法表达的统计或必要效果。状态按当前条件简短显示，不预告未发生的起义，也不抄按钮门槛。AI 专用安全条件不写成玩家资格。涉及数字时必须读 NESND 的 references/numeric-scale-contract.md。\n- 同一事实只说一次。')
s=s.replace('把新发现归纳为一条有证据的局部规则：','局部发现可以先留在本轮比较报告；只有可复用且有证据的纠正才进入永久技能。把新发现归纳为一条有证据的局部规则：')
s+='''

## 提案与落库分级

纯剧情提案可以通过作者风格与事实边界审查，不因尚无脚本而禁止起草；通过结论必须写“编辑提案通过，未接入游戏”。实际落库则必须再核脚本、动态引用、有效覆盖键和显示条件。二者都不能冒充引擎验收。

本轮实际试用、失败初稿、局部规则与重写记录：WORK/reports/rules-poland-qin-20261102/writing-skill-trial.md。规则更新来自用户反馈和这份实际试验，不以抽象清单代替对读。
''';write(p,s)
dump(R/'skill-updates.json',{'backups':str(R/'skill-before'),'updated':[str(S/r) for r in targets if r!='references/active-work.md']+[str(S/'references/numeric-scale-contract.md'),str(P/'SKILL.md')],'new_skill':str(P),'source':'user corrections and writing-skill-trial.md'})
print('Writing and numerical-scale requirements routed from core skill; before copies preserved.')
