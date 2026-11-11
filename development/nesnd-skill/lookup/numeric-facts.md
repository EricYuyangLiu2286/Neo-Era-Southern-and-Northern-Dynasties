# 数值量级与已核实例

> 何时读：给关系、影响力、修正、军需、script_value 上下限定数字前，查它属于哪一层、量级多大。不必读：方法与回路检查（读 references/numeric-scale-contract.md）。

## 本机1.13.11已核实例〔1.15.0 未复核〕

- 关系范围是−100至+100；总跨度200不等于上限200。change_relations 的 value=10 是直接10点；不要与关系进度转换混用。
- 国家影响力容量没有统一1000上限；国家等级基础约600–1100，另受制度、集团与修正影响。外交 leverage 的1000上限不是 influence 上限。
- country_influence_add 是生成侧加值，可受生成倍率影响；不能承诺它与直接增加usage完全等价。百分比修正、固定容量与货币库存分别处理。
- 本轮商使费用由−15改−100持续6个月、首次通商直接关系+25、完成奖励由+25改+100持续24个月。这是本项目平衡选择，不是原版接口强制值；首联与完成标记防止循环刷奖励。

具体源码、行号和期限追踪见 WORK/reports/ui-trade-feedback-20261102/research.md；未来版本先查原文件，不把这些实例当永恒常量。

## 本机陆军军需数量与舰船维持〔1.13.11；1.15.0 已核编制仍用 `ship_type:`，其余未复核〕

1.13.11 的有效 `combat_unit_types` 是19种战斗营，含陆战队；舰队使用独立 `ship_types`、ship-mask修正与 `SHIP_UPKEEP_*` 定义。实际原版 `events/brazil/paraguay.txt` 的 `paraguay.6` 在国家作用域施加 `unit_supply_consumption_mult`，改变战斗营维持所需商品数量；货币费用减免是另一种效果。不能把旧版本“unit也含舰船”的记忆搬到本版。

同一原版按钮里的军营片段只是tooltip预览，不证明building上的unit修正会传给军队。本轮Tiger指出此传递不成立，改用原版真实国家效果。每次迁移重查有效单位/舰船数据库和修正传递，来源见 WORK/reports/canon-route-execution-20261104/batch-b-repair-plan.md 及对应source-hashes；该证据不等于新候选已实机验收。

## 有界算术与单向生活变化（1.13.11，西秦实证）

script_value 的 `min` 是下限、`max` 是上限；以当前原版实例核验，再执行真实AST的边界算术，不凭自然语言误读。两者颠倒会把人口比例、力量和收益推到极端。
SoL带来的“额外15%效忠”是对对应新增量乘0.15，不是每月把全国15%人口变成效忠派。当前原生仅有双向合并修正；需要单向时先记录近似边界，再按原版define的基础量、农民折减及高SoL折减采样。月度净变化无法还原月内所有涨跌。来源及720样本见 WORK/reports/qin-persia-20261102/native-political-contracts.md、sol-approximation.json、arithmetic-cases.json。
