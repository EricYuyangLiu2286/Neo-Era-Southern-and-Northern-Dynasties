# 查办帮会的州级政治代价

父版本：已冻结 `cne-event-feedback-20261031-a`；独立候选 `cne-local-modifier-20261031-b`。修改前完整备份，主 MOD、D、UI A、活动 run 均不改。

## 已核对的作者意图和真实错误

pre-update 作者 `.8.1`“必须维护劳工利益”：本州工业家 +0.05、地主 +0.1 激进派，查办帮会修正 36 月，改革进度 +2。该修正含州税容 +15%、人口行政成本 +10%、`country_loyalists_from_legitimacy_mult=-0.1`。`.8.2` 顺从帮会给当地税收浪费 +15%，进度 +3。D 又分别加入失序 −4/+7。

因此收益是税收与整顿秩序；代价是受影响雇主/地主的反抗、行政开支和持续政治摩擦。原 country 修正挂在州上没有国家流向，UI 能显示一行文字并不能证明它生效。该错不在 `CNE_local_industrial_broom`；原先报告误名已勘误。

## 最小替代与取舍

只把无效国家项改为 `state_loyalists_from_political_movements_mult=-0.1`，36 月不变；此项减少本州因满足政治运动诉求而获得的忠诚派。它实现持续地方政治摩擦，适用于土改与立法环境，并使用真实州 pop 系统。

保留所有原有税容、行政成本、当地工业家/地主即时激进派和进度/失序，避免再叠一轮任意激进派。没有变成国家范围的合法性惩罚，其他州不会受这次地方行动的额外惩罚。负号和量级沿用作者，但不宣称不同生成机制数值等价；36 月内没有满足政治运动的立法，就不会凭空生成忠诚派损失。

替代方案不采用：把整个修正移到 country 会把本州税容/行政开支扩成全国，并扩大地方冲突范围；额外一次性全州激进派会重复现有定向反弹；任意增加地方所有人的政治力量会同时放大劳工和地主，改变权力设计。

## 当前来源

- 引擎 `references/engine-docs-1.13.11-20261031/modifiers.log:823–826`：旧项 Mask country，改变高合法性产生的忠诚派。
- 同文件 1783–1786：新项 Mask state，改变满足政治运动后的忠诚派。
- `GAME/common/static_modifiers/agitators_4_revolution_modifiers.txt:17–21`：`modifier_dual_power_state` 的同一州项为 −0.5；存在真实负值用法。
- `GAME/common/static_modifiers/02_event_modifiers.txt:1158–1160` 与 `GAME/events/urbanization_events.txt:34–40`：同项按 state event 挂在当地州。
- 作者 pre-update `events/flavorCNE_ce.txt` .8 与 `common/static_modifiers/ce_event_modifiers.txt:69–75`。

## 验证

ordered AST 仅一个 modifier key 改变，数字 −0.1 原样；其余所有脚本、作者本地化与 UI A 全部 SHA 不变。Tiger 定位到该 modifier 的 scope warning 应消失；不能把 0 error 当游戏验收。

实机在新版本 .8.1 悬停确认只有税容、人口行政成本和州政治运动忠诚派，旧“来自高合法性”行消失；选择后确认作用州、36 月、即时定向激进派、progress +2/disorder −4。读取本州 pop/修正以确认生效；若要验证长期生成，必须走实际满足政治运动的法律完成并与未受该修正州对照，不能用静态 tooltip 宣称已核出生成量。其他国家/省份的合法性指标不应新增此项。
