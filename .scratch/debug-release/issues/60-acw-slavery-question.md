# 60 美国「奴隶制存废之争论」不推进；新日志与东洲联动

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [计划](../../acw-slavery/spec.md)；[模拟、检查与 Tiger](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-acw-plan/>)；改前备份 `nesnd-workbench/backups/pre-change-acw-slavery-question-20261107T031512Z`

## 1. 现象与期望

作者：测试局里美国「奴隶制之存废」一直没有进展，最晚看到 1873 年；废奴、拥奴运动始终不激进化。期望：换成 MOD 自己的日志，南北战争通常 1860–1862 年爆发，可推迟但不晚于 1872 年，可和解或因条件改变失效；东洲以逃亡、宣称与美国对称联动。

## 2. 原因

- 原版日志的进度只在禁奴后才增加（GAME `00_acw_entries.txt:58-68`），战争靠引擎的运动内战（同文件 `:30-56`）。MOD 未改坏相关代码，但西部与墨西哥北部归东洲，美墨割地、威尔莫特附文等推动力基本消失（推断）。最新存档约 1868 年，确无内战。
- 连带：汗国成立要求 `american_civil_war`（`scripted_triggers/nesnd_hus_registration.txt:111-114`），战争不来汗国也不来。

## 3. 改了什么

- `common/journal_entries/nesnd_acw_slavery_question.txt`（新）：`REPLACE:je_acw_countdown`（保留键名与原版运动挂钩）；分裂危机条、三个结局（和解／内战沿用原版／失效）、分离危机阶段与每周内战推进；东洲日志「西岸的砝码」及逃亡批次。
- `common/scripted_progress_bars/…`（新）：分裂危机（28 项来源）、对美宣称、下一批逃亡者。每项来源写成带 desc 的内联 `progress_condition`（v3 模拟系数），1.15 日志面板逐项列出，条件不满足时显示空框；与任务 52 的修法一致。
- `common/script_values/…`（新）：只保留多处复用的值（两运动激进度、赎买与资助费用、批次规模）。
- `common/scripted_triggers/…`、`common/scripted_effects/…`（新）：共用条件；清理与推动分离。
- `common/scripted_buttons/…`（新）：美国 3 个（国会妥协案、追捕逃亡者、赎买奴隶主），东洲 5 个。
- `events/nesnd_acw_slavery_question.txt`（新）：废奴派入主、MOD 版西部领土但书、分离危机；逃奴与杖击的隐藏转发。
- `common/static_modifiers/…`（新）：不得人心的妥协、赎买金、东进凯旋。
- `common/scripted_triggers/nesnd_europe_america.txt`：东洲开放西境时，美国边疆主张不受冷却限制（一行）。
- 中英本地化：新文件各 118 键；`nesnd_usa_claim_cooldown_tt` 改为同时说明此例外。

## 4. 怎么复测

新开局（1836）。看美国日志条与悬停明细；1850、1855、1860 年各记一次条值与两运动激进度。控制台把条设满（或等到满条）后，看几个月内爆发内战、CSA/FSA 疆域是否正确、原版战争日志是否接上。东洲侧：开放西境后每六个月一批，看奴隶到达后是否为自由劳工、汗国（满蒙路线）是否在内战后出现。

## 5. 遗留问题

- 2026-11-07 复核：原先进度条各项指向命名脚本值，按 1.15 文档这类来源只计数不列出（任务 52 曾因此悬停为空），另用一段自定义悬停表补显示，公式两处并存。现改为内联 `progress_condition`，删去 33 个只供进度条用的命名值和自定义悬停键 `nesnd_acw_crisis_bar_tt`；条说明改为纯读数，东洲宣称条同样处理（原悬停指向按钮条件文字）。静态检查无缺失引用，中英各 117 键；Tiger 在这些文件上只剩 1.19 不认识的 1.15 字段（`progress_condition`，任务 52 的日本条同样被报），见 `tiger-summary-inline.json`。
- 未实机：条件成立但数值为 0 的来源（如参议院恰好平衡）是否仍列出。

- 未实机：满条后几个月内宣战；`nesnd_acw_rad_anti > nesnd_acw_rad_pro` 两个脚本值直接比较（Tiger 未报错）；进度条明细与零值显示。
- 与计划的差异：开放／关闭西境做成两个按钮（24 个月冷却），不另设确认事件；逃亡不发逐批通知；汗国不需改代码（现有转移已含逃来的原住民）。
- 东洲到达者财富设为 10 只保证到达时不被债务奴隶制奴役。
- 分支：仅改主 MOD，未同步 Git 工作副本。
