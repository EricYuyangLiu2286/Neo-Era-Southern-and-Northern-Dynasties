Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-24，奥斯曼 B5 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 基线索引 `_agy_base/v3tree/index`；调研 `_agy_checks/调研.md`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`；模拟 `_agy_checks/academy_sim.py` 与 `_agy_checks/academy_sim_result.txt`

# 123 奥斯曼：学院与报馆

## 1. 现象与期望

坦志麦特成功后的第三块路线内容（社会）：落地奥斯曼「学院与报馆」四环顺序里程碑日志（`nesnd_ottoman_academy_1`–`_4`）、环 1 人物事件「伊斯兰现代主义者」（纳米克·凯末尔，1860–1888）以及 1870 年后年度检查的「工会与工厂」社会左转事件，并接入「宪章与军营」日志计数与原版政治运动机制。

## 2. 改了什么

- **四环顺序日志 `nesnd_ottoman_academy_1`–`_4`**（`common/journal_entries/nesnd_ottoman_academy.txt`）：
  - 入口：在 `common/on_actions/nesnd_ottoman_recovery.txt` 的 `on_monthly_pulse_country` 追加 `nesnd_ottoman_academy_fallback`，条件经 `nesnd_ottoman_academy_fallback_due`（`common/scripted_triggers/nesnd_ottoman_academy.txt`）检查宪政路线、坦志麦特成功、原版教育子目标变量 `completed_sick_man_education_je`、日志不在且未关闭；四环均无 `possible` 与 `is_shown_when_inactive`。
  - 四环依次为：环 1 大学（等级 ≥ 10 且识字率 ≥ 40%）、环 2 公立学校（`law_public_schools`）、环 3 报馆与集会（`law_right_of_assembly` 或 `law_protected_speech`）、环 4 艺术学院（`building_art_academy` 等级 ≥ 1）。每环完成各给一个小永久修正与 60 个月 `nesnd_ottoman_academy_ulema_backlash`（推高 `movement_religious_majority` 支持度 +10%），全部非隐藏结局均写 `event_outcome_desc`。
  - 四环完成结局：永久修正 `nesnd_ottoman_enlightenment`、`ig:ig_intelligentsia` 升级 `ideology_liberal_modern`（已具备则追加 `ideology_egalitarian`）、宪章日志进行中宪政派 +1 项 60 个月、设 `nesnd_ottoman_academy_outcome = flag:complete` 与 `nesnd_ottoman_academy_closed`。
  - 300 个月共享超时（乌理玛胜，`nesnd_ottoman_academy_ulema_win`，`common/scripted_effects/nesnd_ottoman_academy.txt`）：环 1 `immediate` 设 300 个月 `nesnd_ottoman_academy_window` 并配 `timeout = 9125`，环 2–4 检定时变量失效触发；若非 `law_religious_schools` 且 `law_is_available` 则改行 `law_religious_schools`，给永久修正 `nesnd_ottoman_ulema_schools`，宪章日志进行中秦制派 +1 项 60 个月，设 `flag:ulema` 与关闭变量。
- **人物事件与劳工事件**（`events/nesnd_ottoman_recovery.txt` 追加 `.16`、`.17`；`common/on_actions/nesnd_ottoman_academy.txt`；`common/static_modifiers/nesnd_ottoman_academy.txt`）：
  - `.16`「伊斯兰现代主义者」：环 1 完成且 1860–1888 年间触发，`create_character` 建纳米克·凯末尔（知识分子派，`ideology_reformer`）；可选「收为政府顾问」（知识分子 60 月好感修正 + 加 `ideology_modernizer`）或「交乌理玛审判」（宗教集团 60 月好感修正 + 知识分子激进 + `exile_character_with_role_cleanup`），AI 权重在宪章日志秦制派领先时偏审判。
  - `.17`「工会与工厂」：`on_yearly_pulse_country` 检 TUR、日志进行中或已完成（`flag:complete`）、年份 ≥ 1870、`ig:ig_trade_unions` 非边缘且未触发，每年 20% 掷骰发一次；可选「容许工人结社」（工会好感 + 宪章日志宪政派 +1 项 60 月）或「取缔工人结社」（工会好感降 + 激进 + 60 月 `movement_labor` 支持度 +15%），AI 按言论/选举/专制法律加权。
- **本地化**：中英同增 47 键于 `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml` 与 `localization/english/replace/nesnd_ottoman_l_english.yml`。

## 3. 怎么复测

控制台 `tag TUR`，满足坦志麦特成功且已设 `completed_sick_man_education_je`、走宪政路线后，下月确认 `nesnd_ottoman_academy_1` 开启；逐环完成大学（10 级 + 40% 识字率）、公立学校、集会权/保护言论、艺术学院，确认 1860–1888 年间环 1 触发 `nesnd_ottoman_recovery.16` 且非该年代跳过事件照常开环 2；另用 `event nesnd_ottoman_recovery.16`、`.17` 核对人物生成、流亡、意识形态变化、劳工运动修正与中英文案。

## 4. 遗留问题

- 无；原版变量 `completed_sick_man_education_je` 在 `xcheck_diff` 报只读不写，确认由原版 `GAME common/journal_entries/00_sick_man.txt:355` 写入且清理效果不删。
