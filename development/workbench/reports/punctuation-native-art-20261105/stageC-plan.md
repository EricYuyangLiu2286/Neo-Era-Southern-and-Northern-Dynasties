# Task37 StageC — 日本国民团结：结构与文本提案

状态：只读提案，等待主代理逐条审定；尚未修改 MOD，也未进行游戏验证。草案代理实际配置为 `gpt-6-astra / high`。父任务的本轮委派是配置与授权依据。使用 NESND 与 nesnd-player-writing 技能，数值为源码推算，最终架构、数值判断及合入由主代理决定。

## 1. 修改边界

建议只改六个现有文件：

1. `common/scripted_effects/nesnd_jp_development.txt`：在现有月度更新后的 `<25` 分支调用一个新的低团结文化变化 helper；保留当前修正增删和 `>75` helper。
2. `common/script_values/nesnd_jp_development.txt`：新增七个日本专用 AI 数值。
3. `common/scripted_buttons/nesnd_unity_policies.txt`：仅在两个 `ai_chance` 内分出日本分支，非日本原条件及权重逐字保留。
4. `common/journal_entries/nesnd_jp_cohesion.txt`：在现有低团结状态之前插入江南政策低团结状态。
5–6. 现有中英文 `localization/*/replace/nesnd_japan_l_*.yml`：改写 `nesnd_jp_cohesion_doubt`，新增 `nesnd_jp_cohesion_doubt_jiangnan`，共两对文本。

不需要新玩家资格、额外进度条、新文化、主流文化、宗教、迁移或人口损失效果。`possible`、`selected`、按钮实际效果与12个月防重入标记保持现状。

## 2. 已读完整来源链

- MOD `common/scripted_triggers/nesnd_jp_development.txt`：`nesnd_jp_country` 包含存活的 JAP/JTK/JIM；`nesnd_jp_cohesion_live` 只再要求对应 JE，没有统一日本后的退出门槛。`nesnd_jp_jiangnan_policy` 是 JIM 加持久变量，未检查林汉涵存活。
- MOD `common/scripted_effects/nesnd_jp_development.txt:1–49`：初始化 JIM 时已有 japanese/ce_wuu 主流文化及江南政策标记。月更先更新生活水平变化、战争月数，再加 delta、限制到0–100，随后判定 `<25` 和 `>75`。新增效果应遵循更新后的数值。
- 同文件52–83：高团结效果每月70/30随机表，30分支选择合格州，对非目标文化 Pops 按现有比例换文化，至多相当于该州总人口10%。江南政策目标 ce_wuu，其余 japanese。整段保留。
- MOD `common/journal_entries/nesnd_jp_cohesion.txt`：国家有效性、月度 caller、状态 first_valid 与共享按钮；无需另造 on_action 或重复月更。
- MOD `common/script_values/nesnd_jp_development.txt`：当前值、七项月度来源、统计就绪守卫。两项支援各贡献0.5，已计入 delta。
- MOD `common/scripted_{buttons,triggers,effects}/nesnd_unity_policies.txt` 与 `common/script_values/nesnd_unity_policies.txt`：按钮资格只检查既有活动状态；12个月期限/修正防重入；经济费用按周；物质支援逐月使各主流文化0.1%人口趋于激进，最多12次。
- MOD 静态修正中的政治支援：合法性基础−10。经济支援费用 multiplier 使用 weekly_cost。
- MOD `common/scripted_effects/nesnd_jp_imperial_court.txt:15–25`：建立林摄政时设置的政策标记；现有初始化也维持该政策，因此本轮应沿用政策 trigger，而非重新检查人物生死。
- MOD `localization/simp_chinese/replace/ce_cultures_l_simp_chinese.yml:11–22`：han=华北、ce_wuu=江南、ce_zhonghua=华夏。目标绝不能误用 ce_zhonghua。
- GAME `common/cultures/00_cultures.txt:9818,23821` 的 heritage_japanese 仅 japanese、ryukyuan。MOD `common/cultures/CE_cultures.txt:110–113,1752–1756` 分别替换 japanese 与 ryukyuan，后者实际 heritage_han。全 MOD cultures 搜索仅 japanese 仍有 heritage_japanese。因此“日本传承文化且排除琉球”的实际候选集只有 japanese，使用字面量 cu:japanese 与集合选择等价；不伪造 random_culture。
- 引擎文档 `WORK/references/engine-docs-1.13.11-20261031/effects.log:646`：pop scope 的 `change_pop_culture = { target = cu:... value = 0.25 }` 是该 Pop 的指定比例。`effects.log:30852` 支持 state 内 random_scope_pop。`triggers.log:12236` 的 is_primary_culture_of 在 culture scope 接收 country target。
- GAME `events/cultural_homeland_events.txt:24–55`：国家事件内先判断州内文化、再 random_scope_state，culture 上使用 is_primary_culture_of=ROOT。GAME `events/brazil/culture_south_america.txt:660–671`：在受限 Pop 上执行 change_pop_culture，明确分母是 Pop。原版没有被本轮发现的“完全相同一行”组合；这里是以受支持 scope 接口组合，不能称整段已经原版实证。
- `triggers.log:11083,13206,13213,13964` 分别支持 in_default、net_fixed_income、net_total_income、radical_population_fraction。不存在本轮要求语义中的字面 `net_income` API。主代理已批准日本使用 net_total_income，非日本原 net_fixed_income 不变。
- 本机 numeric-scale-contract 指明 scripted_button.ai_chance 使用 script-value 的 value/if/limit/add 形状，不能混入事件选项的 base/modifier。

源码 SHA 在 `stageC-plan-source-hashes.json`。所有 GAME 及参考资料只读。

## 3. 低团结文化效果

建议入口名 `nesnd_jp_low_cohesion_drift`。在现有 `<25` 分支内调用一次，调用位置在 cohesion 更新及 clamp 之后。JAP/JTK/JIM 无论是否统一，均走现有 live/statistics-ready 守卫。

1. 保存本次国家 owner scope，避免 JE ROOT 被误当成国家。人口的 `culture = { is_primary_culture_of = scope:... }` 必须相对当前国家判断。
2. 江南政策分支目标固定为 japanese。普通分支通过50/50 random_list 选择 han 或 ce_wuu。目标先确定，然后执行相同的“合格州→合格 Pop”选择，避免随机选中目标自身后白白浪费变化。
3. 合格 Pop 必须属于该国实际主流文化，且不是本次目标文化。州 limit 使用 any_scope_pop 同一谓词；随后 random_scope_pop 复用同一谓词。只选有合格 Pop 的 owned state，并只选一个 Pop。
4. 对所选 Pop 执行 change_pop_culture，value=0.25。没有合格 Pop 时无效果。不重抽另一个目标，保持普通分支目标50/50；正常日语主流文化下两个目标都适用。
5. 若实施者提取带 target 参数的 helper，须使用已核实的脚本参数语法；也可将三个固定目标分支写开。提案不要求引入任意文化随机 API。

抽样是州层级随机，再该州合格 Pop 随机，不是全国人口加权抽样。25%分母是被选中的一个 Pop。反向排除 japanese 后，当前 JIM 的有效候选是 ce_wuu 主流文化人口；以后若国家合法获得其他主流文化，仍按实际主流集合判断。

这里只换文化，保留该 Pop 的地点、宗教等既有属性；不调用 kill、move、宗教转换或 add_primary_culture。现有初始化的主流文化设置不在本轮修改范围。

## 4. AI 公式与量纲

C = 现有 cohesion value，库存范围0–100；D = 当前 cohesion_delta，单位点/月。F=C+12D 是按当前速度外推的12个月预测，不额外截断。

`N = min(40, 0.6×max(0,40−F) + 1.5×max(0,25−C))`

先置零的情况：C>=60，或 C>=32 且 D>=0。其余按上述公式。N 是按钮 AI 权重，不是每月实际点击概率，也不是对团结度直接加值。现有按钮 AI 调用频率不在本轮改变。

建议新增七个 script_value：

|名称|含义|
|---|---|
|nesnd_jp_cohesion_forecast_12m|C+12D|
|nesnd_jp_unity_ai_need|N；统一 live/statistics-ready 与提前置零守卫|
|nesnd_jp_unity_material_income_required|1.5×nesnd_unity_material_weekly_cost|
|nesnd_jp_unity_material_radical_factor|clamp(1−radical_population_fraction/0.30,0,1)|
|nesnd_jp_unity_political_legitimacy_factor|clamp((government_legitimacy−50)/25,0,1)|
|nesnd_jp_unity_material_ai_weight|全部物质支援 AI 守卫成立时 N×radical_factor，否则0|
|nesnd_jp_unity_political_ai_weight|全部政治支援 AI 守卫成立时 N×legitimacy_factor，否则0|

物质 AI 守卫：现有 available/live、statistics_ready、非 default、没有 declared_bankruptcy、net_total_income >= income_required、radical_population_fraction <0.30。政治 AI 守卫：现有 available/live、statistics_ready、government_legitimacy>=60。不得把物质财政守卫复制给政治支援，也不得加进玩家 possible。

当前 weekly_cost 为 `max(100, 100×round(GDP/400000))`，是按周货币支出，不是GDP百分比直接扣款。源码示例：GDP=400,000时费用100，4,000,000时1,000，20,000,000时5,000。收入门槛分别150、1,500、7,500，使用净总周收入同量纲比较。这里没有捏造当前存档的GDP或净收入。

按钮路由建议：if nesnd_jp_country → value=对应日本weight；else → 原条件及add=25。即便日本统计尚未就绪，也不会回落至旧的“低于50便支援”分支。非日本两个旧分支完整保持。

### 公式边界与局限

- 两项活动支援已经进入 D；已有一项支援使趋势稳定时，第二项权重自然降低。各自的12个月 active guard仍绝对阻止同项重买。
- F使用当前速度，不模拟未来支援到期、战争终止或生活水平变化。因此是启发式，不是未来真实结果承诺；本轮不另造剩余月数预测。
- 政治支援合法性−10，若从60–69降至50–59，order会失去现有+0.15。因此它的即时净增幅可能是+0.35而非+0.5。原机制与门槛保持；60门槛使合法性至少留在50。游戏中的实际最终合法性仍须观察修正/上限效果。
- 这是带明确截断门槛的分段线性需求，不应称处处连续：32且趋势非负、60上限会产生跃变。其余需求不会把每个低于60的国家固定推到60。
- 不以文化转换收益作为 AI 目标，也不鼓励低于24。公式只按团结恶化风险、财政/激进派/合法性决定支援意愿。

## 5. 两条玩家文本契约与编辑对读

精确中英文字符串及显示条件在 `stageC-text-contract.json`。保留现有首句，随后交代一次月度变化及实际25%分母。只在低于25的相应状态显示，不增加常驻长篇说明。既有高团结两条文字不改。

原作者来源为 f18b6c4 的 `localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml`，样本、行号与SHA见 `stageC-author-samples.json`。第107行将概率与真实效果直接相连，第136行明确写数值的对象范围，第111行简述当前失效原因。由此采用“范围→所选对象→比例→结果”的规则句。当前 nesnd_japan 状态是延续参照，不冒称作者原始稿，也不把南明政治称谓迁入日本。

|条目|原文问题|候选决定|自审结论|
|---|---|---|---|
|doubt|只写信任下降，未呈现新增月度变化|保留原首句，明确一个州中的一个主流文化Pop、其中25%、han/ce_wuu机会各半|编辑提案通过；无ce_zhonghua、国家总人口或州总人口分母误写|
|doubt_jiangnan|无对应键|同首句，排除已为日本文化的Pop，25%转为日本文化|编辑提案通过；不把林存活写成条件，不造多个可随机的日本传承文化|

不把 AI 财政门槛写进玩家文案。初稿未使用“核验、结案、共享worker、本次行动”等实现术语。两条英文独立表达随机州与随机Pop，不将25%误译为州人口。

## 6. 实施后的检查清单（本阶段尚未执行）

算式样例已写 `stageC-arithmetic-proposal.json`，只是提案算术。关键预期：C60/D−3→N0；C32/D0→0；C31/D0→5.4；C40/D−1→7.2；C24/D0→11.1；C20/D−1→26.7；C10/D−2→40；C55/D−2→5.4。

- 月更新前24.8、D+0.3 →25.1，不转换；25.1、D−0.2→24.9，转换；恰为25不转换。低于25且有资格每月仅选一次州、一次Pop。
- JAP、JTK未统一/已统一同样工作。JIM政策存在而林已不在世仍走反向。无合格Pop安全不作变更。
- 普通分支大量固定种子采样分别检查han/ce_wuu目标频次，不能把单次随机结果当50/50错误。反向只有japanese目标。
- 验证总人口、位置、宗教、主流文化集合不因新helper改变；25%来自所选Pop，允许引擎舍入/分裂表现。
- 75恰值不触发旧高团结分支，75.1仍走原30%/州总人口10%逻辑。对旧helper做差异校验，不能只靠测试结果声称未改。
- 物质费用1000时净收入1499.99失败、1500通过；default或declared_bankruptcy使物质权重0。激进人口比例0/.15/.299/.30对应系数1/.5/.003333/0。
- 政治合法性59权重0、60系数.4、75及以上系数1。玩家在同样财政/激进派/合法性条件下仍保留现有按钮资格。
- 同项活动期限或任一现有相关修正仍在时权重0且按钮不可重复。活动加成必须进入预测；例如C35/D−.5需要6.6，已有一项将D抬到0后需要0。
- 对两个非日本旧AI分支做结构/条件等价检查，确认无新增条件或权重改动。

## 7. 并行附项：作者中文标点保护

`R37CNpunctguard.json` 独立检查两个基线各280键、313处精确替换。两份基线对应同一批313处作者修改，不能加成626。基线 SHA 全匹配，替换未进入 []函数/概念、#格式命令或$alias$，保护token及引号/方括号平衡未变。当前3键后来经授权改写，另列而未计作标点损坏。未改作者中文，也无必要修复提案。
