# 02 没有买卖双方时进度停滞，AI 多数年份暂停

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS（1.15.1，pdx.py 解析与 Toolkit 零诊断）
Evidence: [1878 自动存档与日志](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-error-flood/save-button/>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-triangle-trade-stall-20261112T205703Z>)

## 现象与期望
作者 1878 年看到北洋三角贸易各国似乎都“暂停交易”，成交单一直失败。期望：没有一组买方与卖方时进度条停滞，不做无用运算。

## 原因（存档 1878-07-01）
- 北洋参与国 9 个：USA、BUR、PHI、SHA、JIM、DEI、USM、QE1、HUS。设了模式的只有 PHI（卖出）。CAM 卖出、AST 买入，但都不是参与国。没有参与国在买，所以每一单都找不到买方。
- AI 不点按钮。`scripted_effects/nesnd_triangle_trade.txt:24–59` 每年按 `nesnd_triangle_ai_buy/sell`（`script_values/nesnd_triangle_trade.txt:5–57`）的百分比掷一次，掷不中就停在暂停。参与国现行奴隶制：PHI 奴隶贸易（40），USA、QE1 遗留奴隶制（10），其余为债务奴隶制（15）。再加减地主、知识分子与废奴派元首，多数国家每年只有 0–35% 的机会选边。
- 原来进度条不看订单，没有订单也照常累加，满 100 时记为“没有可用的成交单”。

## 改了什么
- common/scripted_progress_bars/nesnd_triangle_trade.txt：两条进度条的 `monthly_progress` 增加 `exists = global_var:nesnd_<KEY>_trade_dest`，没有订单时不累加，停在原值。
- common/scripted_effects/nesnd_triangle_trade.txt：`nesnd_triangle_pick_order` 只在参与国里同时有买方与卖方时才列出人口、抽取订单，否则直接跳过。
- localization/{simp_chinese,english}/replace/nesnd_triangle_trade_l_*.yml:18：`nesnd_triangle_trade_no_order_status` 改为“下一单：目前没有可以成交的买卖，市场活动暂停。”（作者改定措辞）

## 怎么复测
重启游戏后读 1878 年自动存档。北洋进度条应停在当前值（如 65），日志写“市场活动暂停”。把登莱设为买入后，若菲律宾仍在卖出且有合适的目标州，下个月应排出订单，进度恢复累加。

## 遗留问题
- 2026-11-12 作者决定：`script_values/nesnd_triangle_trade.txt` 的 `nesnd_triangle_ai_interest` 基础值由 0 改为 40，废奴派元首的 -40 正好抵消。备份 `backups/pre-change-triangle-ai-interest-20261112T210215Z`。
- 2026-11-12 作者澄清：三单各有一条进度条，各自计时、各自结算，不是共用一条。已按此重做，备份 `backups/pre-change-triangle-three-bars-20261112T212130Z`：
  - 进度条：每个日志 3 条 `nesnd_<KEY>_trade_bar_1..3`（界面名甲、乙、丙号货船）。只在该槽位有订单时累加。每月速度 = 运输效率（排单时随机 3 / 5 / 7 / 9 / 10）+ 卖方奴隶制法律 + 买方奴隶制法律（奴隶贸易 +3，债务奴隶制 +2，遗留奴隶制 +1，殖民地奴隶制 0，`script_values` 的 `nesnd_triangle_law_speed`）。法律加成每月按现行法律重算。原来的“各港船主 +1、参与国奴隶贸易或殖民地奴隶制 +1、商业海军 +3”三行已删除，月结里统计这些的全局变量也一并删除。
  - 结算：周脉冲里哪一条满 100 就只结算哪一单，清零那一条，然后为空着的槽位排单。月脉冲也为空槽位排单。同一对买卖国可以占多单，同一个 pop 只能进一单（抽取时排除其他两个槽位的 pop）。
  - 日志状态：“在途货物：”后逐行列出在途各单，不再写“第 X 单”。上一单的结果恢复为单笔：“上一单已成交：X 人运抵目的地，成为奴隶。Y 人死于途中。”及两种失败说明。
  - 旧存档里的订单和进度条用的是旧名，读档后会被忽略，下个月重新排单。
