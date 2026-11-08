# 80 第二次靖难：蜀军、继续战争、吴方失效与天朝帝国解体

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [静态检查脚本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-08-jingnan-continuation/verify.py>) · [结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-08-jingnan-continuation/static.json>) · [Tiger 原始输出](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-08-jingnan-continuation/tiger.json>) · 内容树：改前 `cases/jingnan2/`，改后 [map.html](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/content-tree/v3tree-output/cases/jingnan3/map.html>)、[report.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/content-tree/v3tree-output/cases/jingnan3/report.md>)

## 现象与期望

缅甸可经雨林从南面打蜀，打乱“先湖广、淮，最后蜀”；靖难战争可能留下未开战的拥明国，战争打不完。要求：蜀军子日志；吴方日志“继续战争”进度条；吴方失效条件；失效且吴仍在时“天朝帝国解体”，重建大明联邦。

## 原因

- “西军”不存在；湖广的同类是“襄阳大营”（`nesnd_war_collapse.txt:39`，防御+20%、军需−20%，随襄阳完整存续）。
- 占领即吞并：每周 `nesnd_check_war_collapses`→`nesnd_south_capital_defeat`（首都被占或敌占>80%）→`usm_civilwar.4`→`annex_as_civil_war`。禁止议和：`dp_usm_civil_war` 的 `allow_negotiated_peace = no`。
- 卡死点：残余战事只在对手和平时（不在战争、不在博弈）才发来函、才重开战争。对手若在和别国（如缅甸）打仗，就永远不进入下一轮，吴方日志无法结束。
- 残余战事的出口都能封口：降吴＝吞并；求北朝＝北朝接纳后成为其保护国（结案），拒绝则转抵抗；抵抗＝吴重开战争；“议定现状”只在已无未结对手时可用。

## 改了什么

- `common/static_modifiers/nesnd_shu_army.txt`（新）：蜀军，攻防各+20%、军需−20%。
- `common/journal_entries/nesnd_war_collapse.txt`：子日志 `nesnd_shu_army_journal`，蜀国持有任一靖难反吴日志（明方或共和方）时出现，日志结束即止。
- `common/scripted_progress_bars/nesnd_jingnan_continuation.txt`（新）：继续战争条，0–5 个月。
- `common/journal_entries/ce_usm_the_last_days_of_ming.txt`：吴方日志挂进度条；月脉冲归零或开战；新增首位的失败结局“天朝帝国解体”。
- `common/scripted_triggers/nesnd_south_holdouts.txt`：`nesnd_continue_war_candidate`；残余战事窗口在解体后关闭。
- `common/scripted_effects/nesnd_south_holdouts.txt`：`nesnd_continue_war_open`，与原重开战争并列。
- `common/scripted_triggers/nesnd_ming_court.txt`：`nesnd_ming_federation_loyalist`（拥明，不含共和派）。
- `events/nesnd_celestial_collapse.txt`（新）：.1 解体、.2 新闻、.3 大明联邦与天子、.4 玩家受邀、.5 复立君统。
- `common/dynamic_country_names/00_…`、`ce_…`：淮、南洋、远南、菲律宾加“大明行在／大明监国政府”国名。
- 中英本地化 `nesnd_celestial_collapse_l_*.yml`（新，32 键）。

## 怎么复测

新开局最可靠；继续战争和解体链也可读靖难进行中的存档（蜀军子日志在蜀国已有靖难日志时自动出现）。细节见交付说明（本次对话）。

## 遗留问题

- 停战不再阻止继续战争：到期时吴先用 `end_truce` 双向废止停战再开战（作者要求，2026-11-08）。
- 未实机：废止停战后能否立即开博弈、对正在打别的仗的国家发起博弈、吴同时处于别的战争时能否开新博弈。失败时进度条归零，5 个月后重试。
- 解体设置 `nesnd_south_settled`，会让吴（岛上）可能开启“东洋之议”等读取该标记的内容；未改。
- 内容树索引未把 `00_dynamic_country_names.txt` 中 GNG、DEI 新加的国名记为边（报告第 6 节 8 处），属工具漏抓。
- 改动前未做 `backup.py` 备份。

## Comments

- 2026-11-08 Claude：作者答复——蜀军取“攻防+20%、军需−20%”；战争用反吴、联邦用拥明；保留残余战事出口但须封口；天子即位，原君主任地主集团领袖，原地主领袖转为普通贵族政治家，不退休。
- 2026-11-08 Claude：按作者要求，停战期的反吴国计入进度条，开战前废止停战。
- 2026-11-08 Claude：作者截图显示继续战争条面整句溢出。条面改为“继续战争：X / 5 个月”，规则移到条面悬停 nesnd_continue_war_bar_rules_tt；周期条目改为“尚有反吴国家未参战”。原因：写作技能 SKILL.md 后来的重写把 542ea8e 中“进度条表面”一行并入“写明读数、门槛、期限”，现已恢复为独立一行（安装版与 development/ 一致；Git 工作副本仍是 542ea8e 版，未提交）。
