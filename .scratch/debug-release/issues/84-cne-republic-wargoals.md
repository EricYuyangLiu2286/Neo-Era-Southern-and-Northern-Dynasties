# 84 共和派起义的双方战争目标

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [Tiger 原始输出](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-09-cne-republic-wargoals/tiger.json>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/2026-11-09-cne-republic-wargoals>) · [起因核算](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-09-land-review/odds.md>)

## 现象与期望

作者要求：确认起义博弈的设置，不要轮空中华帝国的新战争目标（外部代理的代码曾出过此问题）。帝国对起义方的目标改为“镇压起义”：胜利吞并目标，若帝国仍有地权革命日志，改革进度 +15、失序 −20。起义军的目标为“羞辱（共和派起义）”：胜利时若帝国符合条件，获得十年修正，陆军攻防 −10%，因反对的法律而提高的政治运动活跃度 +15%。双语本地化。

## 原因

- 旧博弈 `dp_nesnd_cne_republic` 只写了 `war_goal = annex_country` 加 `mirror_war_goal = yes`，创建效果没有为任何一方写入战争目标（`common/scripted_effects/nesnd_cne_republic.txt:93-99` 旧版）。任务 79 中，作者实测同样依赖博弈类型的吴方主要要求为空。
- 共和国日志的失败结局在战争结束、NRP 尚存时触发，效果是帝国吞并 NRP（`common/journal_entries/nesnd_cne_republic.txt:19-33`）。起义方改用羞辱后，NRP 胜利也会存续，这条结局会把战胜的一方反过来吞并。

## 改了什么

- `common/war_goal_types/nesnd_cne_republic.txt`（新）：`wg_nesnd_cne_suppress_uprising` 为吞并类，`on_enforced` 在帝国、改革有效、有母日志、未进入终局裁决、两条变量都存在时，进度 +15、失序 −20，夹值后刷新条面。`wg_nesnd_cne_republican_humiliation` 为羞辱类，`on_enforced` 给 NRP 记 `nesnd_cne_republic_humbled_empire`，并在目标仍是存活的 CNE 时施加 120 个月修正。
- `common/diplomatic_plays/nesnd_cne_republic.txt`：主目标改为镇压起义，关闭镜像、换边和双方追加目标，不需要利益标记。
- `common/scripted_effects/nesnd_cne_republic.txt`：开战时为双方各写一项 `primary_demand = yes` 的主要要求。持有方写作 `c:CNE`、`c:NRP`，因为该效果也会从 NRP 的周脉冲调用。帝国吞并 NRP 的效果在 NRP 已羞辱帝国时不执行。
- `common/journal_entries/nesnd_cne_republic.txt`：羞辱帝国并停战后，共和国日志以隐藏失效结束，不再走“共和国战败”。
- `common/static_modifiers/nesnd_cne_reform.txt`：新增 `nesnd_cne_republican_humiliation`。
- 两语 `nesnd_cne_confidence_l_*.yml`：两项目标的名称、类型说明、实例名与说明，修正名与说明；博弈悬停改为双方的新要求。

## 怎么复测

1. 新开局，用控制台把帝国信心降到 500 以下，等共和起义开战。查看战争界面：帝国一方主要要求为“镇压[共和军]”，共和军一方为“羞辱[帝国]（共和派起义）”，两边都不为空，也没有重复。
2. 帝国胜：NRP 被吞并。地权革命仍在进行时，地权改革 +15、地方失序 −20，条面随即更新；改革已结束时没有变化。
3. 共和军胜：帝国受羞辱，并获得“共和派起义之辱” 120 个月。共和国日志隐藏结束，帝国没有吞并 NRP。
4. 共和军占领帝国八成州时，原有的共和国胜利结局（吞并帝国）仍照旧触发。

## 遗留问题

- 未启动游戏。博弈类型的 `war_goal` 与显式 `add_war_goal` 同为“镇压起义”，引擎可能合并、去重或显示两项，须实机确认；任务 79 的同类写法也尚未复测。
- Tiger 1.19.0 面向 1.13.5，对 `control_half_target_country_states`、`mirrored_wargoal` 与日志 `outcome` 的报错均为版本滞后。原版 1.15 的 `00_annex_country.txt`、`08_humiliation.txt` 使用相同写法。
- 已在进行中的共和战争不会重算目标，复测须用尚未起义的存档。
- NRP 羞辱帝国后作为独立共和国存续，后续没有专门内容。

## Comments

2026-11-10：作者测试完毕。正文中“未启动游戏”“待复测”等为交付时的状态。
