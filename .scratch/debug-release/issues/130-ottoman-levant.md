Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-27，奥斯曼 B10 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；模拟 `_agy_checks/levant_sim.py` 与 `_agy_checks/levant_sim_result.txt`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`、`_agy_checks/tree_diff.md`、`_agy_checks/grep6.txt` 与 `_agy_checks/je_defs_check.txt`

# 130 奥斯曼 B10：黎凡特（`nesnd_ottoman_levant`）

## 1. 现象与期望

开局埃及（`c:EGY`）持有阿达纳分州（`STATE_ADANA`，奥斯曼仅留 3 省）、阿勒颇（`STATE_ALEPPO`）、叙利亚（`STATE_SYRIA`）及黎巴嫩、巴勒斯坦、外约旦、西奈。埃及在「独立的代价」中可能长期独立、担保落空、成为第三国保护国（法兰西、大不列颠、大明联邦、蜀王藩、西秦等）或成为奥斯曼保护国；唐衣大食助秦西向亦会争夺叙利亚与阿勒颇。既有「重整东方秩序」结局又把五区写死为直辖，导致埃及成为奥斯曼保护国后反而死锁。

本批（B10）照 B9「两河」的范式，新增奥斯曼两线共用对外日志 `nesnd_ottoman_levant`（「黎凡特」）：对手不写死国名，按三目标地区持州数与最上层宗主动态选出并记入 `global_var:nesnd_levant_foe`（`c:EGY` 仅作 R11 a 类 +10 历史加权）；开启时动态快照整区在手且与非奥斯曼目标州接壤的州地区；设 4 枚按钮（鼓动、定下方略、提议承认现状、寻求外援）、6 则事件（`.26`–`.31`，含埃及一侧独立后的「埃及北上」年度事件 `.31`）、7 项按隐藏失效优先及 R10/R12/R13 排序的结局；同步在 `nesnd_north_helper_candidate` 排除黎凡特对手，并将「重整东方秩序」的「东方秩序」结局触发条件改为奥斯曼及其附属持有五地区（`nesnd_ottoman_eastern_order_held`）。中英新增本地化键全部以 `TODO_CLAUDE` 占位，由主会话填写玩家文字。

## 2. 改了什么

- **新建黎凡特日志、触发器、脚本值、效果、按钮、修正与自定义本地化**：
  - `common/scripted_triggers/nesnd_ottoman_levant.txt`：目标三区与更宽六区判断、持地判断（`any_subject_or_below`）、对手候选与有效性、入口补加、快照失守、交战/博弈、局面已变、宣称与直接持有国、提议有效守卫（`.27`/`.29`）、求援帮手候选、`nesnd_egypt_north_eligible` 与 `nesnd_ottoman_eastern_order_held`。
  - `common/script_values/nesnd_ottoman_levant.txt`：对手计分（每州 +20、`c:EGY` +10）、直接持州计数、求援帮手计分（与土关系值 + 与对手互为宿敌 +50）。
  - `common/scripted_effects/nesnd_ottoman_levant.txt`：选对手、动态接壤快照、统一入口 `nesnd_ottoman_levant_start`、R13 失自主月数维护、失地加宣称、承认现状弃三区宣称、派发求援事件 `.29`、统一清理、埃及北上年度 20% 掷骰及埃及宣称奥斯曼接壤地区效果。
  - `common/journal_entries/nesnd_ottoman_levant.txt`：新建「黎凡特」日志（无 `possible`/`is_shown_when_inactive`，240 月自定义期限，7 结局依次为隐藏失效、边境失守、失去自主、收复、承认现状、局面已变、搁置，三档 `status_desc`）。
  - `common/scripted_buttons/nesnd_ottoman_levant.txt`：新建「鼓动」（36 月冷却，更宽六区外手州加 `small_radicals`，与对手关系 −15，发 `.26`）、「定下方略」（限一次，需宣称，三目标区设 `conquer` 秘密目标，60 月军需/征兵修正）、「提议承认现状」（60 月冷却，发 `.27`）、「寻求外援」（36 月冷却，向最高分近东帮手发 `.29`）四枚按钮。
  - `common/static_modifiers/nesnd_ottoman_levant.txt`：新建 9 项静态修正（4 项结局永久修正、方略准备、持有国驻防、外援威望、埃及北上、经营尼罗河）。
  - `common/customizable_localization/nesnd_ottoman_levant.txt`：新建 `nesnd_ottoman_levant_foe_name`，从 `global_var:nesnd_levant_foe` 动态取对手名并带兜底键。
- **既有文件衔接**：
  - `common/on_actions/nesnd_ottoman_recovery.txt`：`on_monthly_pulse_country` 新增 `nesnd_ottoman_levant_fallback`；新增 `on_yearly_pulse_country` 挂 `nesnd_egypt_north_yearly`。
  - `events/nesnd_ottoman_recovery.txt`：`.5`/`.6` 四选项补加调用 `nesnd_ottoman_levant_start`；文末新增 `.26`（持有国告急）、`.27`（提议承认现状，含列强 5 年投资权条约）、`.28`（承认现状回音）、`.29`（外援请求）、`.30`（外援回音）、`.31`（埃及北上）。
  - `common/scripted_triggers/nesnd_north.txt`：`nesnd_north_helper_candidate` 仅加一行 `NOT = { global_var:nesnd_levant_foe ?= this }`。
  - `common/journal_entries/nesnd_ottoman_recovery.txt`：「东方秩序」结局 `trigger` 改为 `nesnd_ottoman_eastern_order_held` 并包具名提示 `nesnd_ottoman_recovery_eastern_order_tt`。
  - `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`：同步追加 97 对新键，值均为 `TODO_CLAUDE`。

## 3. 怎么复测

1. 坦志麦特成功（`.5`）与失败（`.6`）各测一局：核对选项执行后开启「黎凡特」日志，开局独立埃及得 70 分当选对手，快照记下安卡拉、迪亚巴克尔、代尔祖尔三区；旧存档推进一个月核对 `nesnd_ottoman_levant_fallback` 补开。
2. 逐项验证 7 项结局与判序：换标签走隐藏失效；快照三区失州走边境失守（即便同月收复三目标区亦坏先判）；失自主满 12 月走失去自主并 24 月冷却；三目标区全归奥斯曼或附属（含埃及成奥斯曼保护国）走收复、热情 +20、近东冷淡列强关系 −10；承认现状走完成；对手成附属或失地且未交战走局面已变并 24 月后按新对手重开；240 月届满战时不截断。
3. 测四枚按钮与事件 `.26`–`.30`：鼓动加更宽六区激进派并发 `.26`；定下方略设秘密目标并给 60 月修正；承认现状在对手为列强且满足条约条件时另签 5 年投资权条约；寻求外援选最高分近东帮手发 `.29` 并在 `.30` 按传递作用域分流。
4. 测埃及北上（`.31`）：独立埃及完成「独立的代价」且停战解除后年度 20% 触发一次，选北上获接壤奥斯曼地区宣称与 `conquer` 秘密目标，后续夺州即触发奥斯曼「边境失守」。
5. 测「重整东方秩序」的「东方秩序」结局在埃及或两河为奥斯曼附属时亦可正常达成。

## 4. 遗留问题

- 本批 97 对中英新键均以 `TODO_CLAUDE` 占位，且旧键 `nesnd_ottoman_recovery_eastern_order_conclusion` 的文字需由主会话同步改为涵盖附属持有。
- 结局变量 `nesnd_ottoman_levant_outcome` 目前只写不读，留给 B11 读取。
- 汉志与圣城、唐衣哈里发（B11）、北非（B12）、埃及原日志与原版埃及危机事件按任务规定不在本批范围。
