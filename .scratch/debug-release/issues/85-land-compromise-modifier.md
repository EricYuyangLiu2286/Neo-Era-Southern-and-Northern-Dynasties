# 85 暂缓田籍清理的数值

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [Tiger 原始输出](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-10-land-compromise/tiger.json>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/2026-11-10-land-compromise>)

## 现象与期望

作者：土地改革结束时有一个很小的减益（−5% 之类），改成威望 −10%、行政力 −5%、政治运动吸引力 +15%，持续十年。

## 原因

该减益是 `nesnd_land_compromise`“暂缓田籍清理”（`common/static_modifiers/nesnd_crisis_modifiers.txt:6-7`），原为税收 −5%、权威 −5%。冻结（`nesnd_crisis_effects.txt:81-82`）与崩溃分裂（`:153-154`）时施加 120 个月，请愿事件选 b 时施加 60 个月（`nesnd_land_choices.txt:15-16`）。

## 改了什么

- `common/static_modifiers/nesnd_crisis_modifiers.txt`：改为 `country_prestige_mult = -0.10`、`country_authority_mult = -0.05`、`political_movement_pop_attraction_mult = 0.15`。代理初稿写的是行政力 −5%，作者随后亲自改为权威 −5%，以作者版本为准（任务 86 整理该文件时一度误回写为行政力，已恢复）。结束时的期限原本就是 120 个月（十年），未改。没有文字写死旧数值，界面直接读修正。

## 怎么复测

新开局后在改革中按“议止地权革命”选结束，看国家修正“暂缓田籍清理”的三项数值和 10 年期限。

## 遗留问题

- 请愿事件 `nesnd_crisis.30` 的选项 b 在改革进行中也施加此修正，期限 60 个月，现在同样是新数值。未改期限。
- 该修正原本就没有 `_desc` 说明文字，未补。

## Comments

2026-11-10：作者测试完毕。正文中“未启动游戏”“待复测”等为交付时的状态。
