# 94 南方残余势力条件的 country_c_equal 刷屏

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS（1.15.1，pdx.py 解析与 Toolkit 零诊断）
Evidence: [排查报告、日志与存档副本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-error-flood/report.md>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-error-flood-holdouts-20261112T190212Z>)

## 现象与期望
作者玩大吴到 1838 年，错误计数 289,626。窗口内 80% 是 `country_c_equal: Scope dependent values in localization inside an any trigger … at common/scripted_triggers/nesnd_south_holdouts.txt:108`。期望：该报错消失，判断结果不变。

## 原因
`nesnd_south_unresolved_holdouts` 的 `any_country` 含 11 处随被遍历国家而变的 `c:X ?= this`，界面每生成一次说明就报 241 × 11 = 2,651 条。刷屏在内战前（1838-01-27、02-26），内战开始后停止，与继承棋局日志在内战时结束一致。细节与排除依据见报告。

## 改了什么
- common/scripted_triggers/nesnd_south_holdouts.txt:107–111：用 `custom_tooltip = { text = nesnd_south_unresolved_holdouts_tt … }` 包住 `any_country`。
- localization/{simp_chinese,english}/replace/nesnd_journal_tooltips_l_*.yml:11：新键。
- localization/{simp_chinese,english}/replace/ce_usm_events_l_*.yml：各 7 处 `[Date.GetString|v]` 改为 `[TimeKeeper.GetCurrentDate.GetString|v]`（事件正文没有 Date 上下文）。

- common/scripted_buttons/nesnd_sha_restore_yan.txt:38：「招徕东北流民」按钮的 `any_country` 包上 `custom_tooltip`，新键 `nesnd_sha_yan_migrant_origin_tt`（nesnd_sha_restore_yan_l_*.yml:56）。悬停一次曾报 12,117 条。

## 怎么复测
新开局玩大吴到内战爆发，期间看继承棋局日志的按钮。error.log 搜 `nesnd_south_holdouts.txt:108` 应为 0，`usm_civilwar.2` 正文显示日期。

重启游戏后读 20:47 自动存档，悬停「招徕东北流民」，error.log 应无 `nesnd_sha_restore_yan.txt:38`。

## 遗留问题
- `nesnd_external_policy` 从未激活：`possible = { always = no }` 使开局生成的未激活实例挡住了 `add_journal_entry`。作者选方案一，已把 `nesnd_external_journal.txt:8–9` 改为以 `nesnd_external_following` 为激活条件，待读档复测。另有 35 个日志写法相同，未改。
- 本次运行较早的 error.log 已被轮转覆盖，刷屏最早从哪天开始无法确定。
- 「招徕东北流民」无法点击：存档中无船期冷却与破产，剩下“东北迁出国”和“本国接收州”两条依赖引擎原生判断，待重启后看提示确定。
- 同类写法静态扫描命中的其余位置未改，见报告。
