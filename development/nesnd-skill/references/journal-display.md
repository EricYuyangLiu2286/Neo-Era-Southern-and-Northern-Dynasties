# 玩家看到的条件、提示与结局

> 何时读：写或修日志的可用/完成条件、按钮预览、custom_tooltip、状态行、进度条明细与结局面板。不必读：只改措辞（读玩家写作技能）；查字段名与 GUI 位置（读 lookup/journal-ui.md）。

## 1. 原生条件优先与状态节制（2026-11-02）

- 先读作者原始日志/按钮的 trigger，再查当前 GAME 同类条目。能直接呈现的法律、科技、机构、建筑、国库等条件直接写在 possible/complete，独立条件各占原生勾叉。不要把多项真实门槛塞入一个 custom_tooltip；换行不能替代独立真假状态。
- 全国等级用 country_has_building_type_levels = { target = bt:building_iron_mine value >= 25 }（GAME/common/scripted_buttons/07_japan_buttons.txt）；州分布另用 any_scope_state 的 count 与 state_has_building_type_levels。五州各有五级城镇中心不等于每州须同时达到全国工业总量。
- custom_tooltip 只用于原生显示无法说明的自定义统计/对象选择，以及未自动呈现的必要效果；写最短的可判断条件。原生 effect 已显示关系变化，就不再加一行相同数字。内部存在性、schema、重复执行保护用 hidden_trigger，但不能隐藏真实玩家资格或费用。GAME/common/scripted_buttons/00_balkan_wars_buttons.txt 有原生隐藏示例。
- AI 谨慎阈值与玩家资格分别维护。用户指定仅供 AI 的政力、破产、失序限制，放 is_ai 分支/AI选择权重，不能悄悄变成玩家硬门槛。玩家仍须支付实际费用；该规则不自动删除完成条件或进度公式里的同名指标。
- status_desc 用 first_valid/triggered_desc 呈现当前阶段；没有新增信息时留空。未发生的起义不在开场预告。状态不复述按钮已列的门槛；按钮 desc 不复述原生效果。统计面板只保留读数。
- 检查同国同时激活的全部 JE 挂载。两个名称不同、调用同一操作的按钮依然可能重复；删除冗余挂载不删除其他日志或 AI 使用的 effect。

本轮来源与前后对照：WORK/reports/ui-trade-feedback-20261102/research.md、WORK/reports/ui-poland-tributary-20261102。源码检查不能证明实际UI布局。

### 公开条件逐层展开

- 从玩家入口`possible/complete/fail`递归展开scripted trigger后审查。身份枚举、初始化和防重复记录用`hidden_trigger`；影响玩家决定的前置、等待、正在进行的选择，各用一句具名条件；法律、建筑、合法性等仍用原生条件。不要把`visible`或状态分支内的变量误计为屏幕上的裸变量。`any_*`中的国家身份比较会产生scope-dependent描述警告，对实际候选集合做简短提示，不展示“他们是本国”的枚举。

## 2. 按钮预览与周期占比：2026-11-03实际反馈

禁止滥用custom_tooltip不等于删除变量效果提示。按钮可见/可用条件不保证effect预览受同样条件约束；执行内的if在预览时可能展开内部缺值，或已设置标记使效果消失。把真实守卫留在hidden_effect，外层用简短custom_tooltip说明不可原生呈现的变量、路线与一次性期限，配show_as_tooltip显示真实modifier/law/treasury；不得重复同一收益。验证实际执行AST及提示两面。

国家变量完成条件没有本地化时，只包装对应单项条件，勿用全局伪造country_var_*翻译或把无关门槛合成一个勾叉。建筑用bt引用时核对实际定义键，别名不保证可作scope：本轮error.log证明building_textile_mills失败，而building_textile_mill正确。先查同类JE/events/decisions完整链条，再决定用全国累计还是单座建筑；两者不能为显示漂亮而互换。

占比条每周重算不是每月固定增量。原生weekly_progress应解释新目标减旧值，并纳入同周期扶持撤销，再由既有单一写入者绝对同步；只读预览不得改变持久变量。依据：原生00_ip4_victoria_progress_bars与本轮QE1三权来源/80组边界报告。

证据：WORK/reports/persia-journal-ui-20261103/release-notes.md、sources.json、button-feedback-other-review.md、qe1-court-progress-research.md。未做引擎验收。

## 3. 法律影响按法组呈现

进度条增减包含法律时，先按实际 `lawgroup` 拆分贡献值，并用该法组的既有本地化名作行名。一行内部用 `if/else_if/else` 表达不同现行法律即可；不同法组分别显示，便于玩家从负数找到可调整的法律。社会动荡、机构等级、经济和战争另列，避免混进“法律”行。内部总和函数可以保留，但实际结算和UI不得把分项与总和重复计入。

依据：2026-11-04作者纠正；西秦旧 `nesnd_qe1_unity_laws` 混合公民权、宗教与军队法组，印度共同认同又把社会动荡与公民权混在一起。当前来源与实施要求见 WORK/reports/canon-route-execution-20261104/unity-inventory-and-native-contract.md、batch-b-unity-plan.md；最终是否通过以该批验证报告为准。

## 4. 1.15 可见结局与自动激活（2026-11-06）

用户要求独立剧情日志有可见的关闭条件。按当前 `GAME/common/journal_entries/journal_entries.md:135–194`，`outcome` 的 `hidden invalid_outcome` 不显示在结局面板。结构合法不等于玩家能知道如何结束。查每个实际启用的日志：常驻政策可直接显示原有终止条件，不另造满条胜利、奖励或一套存在性分支；真正依附父日志的条目注明父日志，并核实际存续依赖。暂时无目标而允许恢复的隐藏失效，才与长期退出分开。

同文档25–49说明自动激活需要 `is_shown_when_inactive` 与 `possible`，显式 `add_journal_entry` 则绕过两者。互斥子日志优先用“父日志有效＋方案已选”控制两项自动条件，单一入口。不能一边永远隐藏潜在条目，一边用每周重复add当作激活已证明的证据。若日志报告already has而UI不见，先查实际激活条件及实例状态。

触发器能判真，不代表其原生自动描述有正确数据上下文。本轮 `is_on_defending_side` 可执行，但经国家条件展开时原版 `TRIGGER_IS_ON_DEFENDING_SIDE` 读取 `War.GetName` 而没有War上下文。保留原布尔子树，以一句具名custom_tooltip包装这一判定；不改战争创建、阵营或和平规则，也不伪造全局原版翻译。

工具与证据：WORK/reports/prose-icons-20261106/root/verify_delivery.py、outcomes/audit_native_outcomes.py、原始error-before.log。检查真实原缺陷和原版字段，主MOD后的检查不得要求旧缺陷仍存在。STATIC_PASS不代表游戏内显示已验证。
