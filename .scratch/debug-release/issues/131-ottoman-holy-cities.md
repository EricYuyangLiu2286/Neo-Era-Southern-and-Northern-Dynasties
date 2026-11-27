Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-27，奥斯曼 B11 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；模拟 `_agy_checks/holy_sim.py` 与 `_agy_checks/holy_sim_result.txt`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`、`_agy_checks/tree_diff.md`、`_agy_checks/grep6.txt` 与 `_agy_checks/je_defs_check.txt`

# 131 奥斯曼 B11：圣城与两个哈里发（`nesnd_ottoman_holy_cities`）

## 1. 现象与期望

既有奥斯曼成功线日志「伊斯兰领袖」完成后直接发事件 `nesnd_ottoman_recovery.12`，选项 a 不看汉志（`STATE_HEDJAZ`）归属就直接给予永久修正 `nesnd_ottoman_caliphate`；失败线「专制的主导权」苏丹胜出仅设 `nesnd_ottoman_autocracy_outcome = flag:sultan`，尚未承接哈里发名义；唐衣大食完成「重启远西战争」后改称「唐衣哈里发国」（`nesnd_per_west_realized` + 逊尼国教），与奥斯曼之间尚无「两个哈里发」交互。

本批（B11）照 B10「黎凡特」的范式，新增对外日志 `nesnd_ottoman_holy_cities`（「圣城」）：奥斯曼取得哈里发名义须圣城在己方或其附属手中；成功线 `.12` 选项 a 在圣城不在手时转设 `nesnd_ottoman_caliph_claimed` 并开启本日志，失败线苏丹胜出由月度补加接起（圣城已在手时开出后下一次判定即走「圣城归附」获 `nesnd_ottoman_caliphate`）。对手不写死国名，按汉志持州数与最上层宗主动态选出并存 `global_var:nesnd_holy_foe`，另一位哈里发不写死 `c:PER`，凭 `nesnd_per_west_realized` 与逊尼国教识别并在对手计分中额外 +30。设 2 枚按钮（定下方略、提议归附）、4 则事件（`.32`–`.35`）、6 项按隐藏失效优先及 R10/R12/R13 排序的结局；同步在 `nesnd_north_helper_candidate` 与 `nesnd_ottoman_levant_helper_candidate` 各加一行排除 `global_var:nesnd_holy_foe`。中英新增本地化键全部以 `TODO_CLAUDE` 占位，由主会话填写玩家文字。

## 2. 改了什么

- **新建圣城日志、触发器、脚本值、效果、按钮、修正与自定义本地化**：
  - `common/scripted_triggers/nesnd_ottoman_holy_cities.txt`：圣城归属判断、不写国家标签的 `nesnd_rival_caliph`（排除奥斯曼自身与多级附属，对齐 PER 三个哈里发动态国名的执政文化条件与逊尼国教）与另一位哈里发持圣城判断、对手持地/候选/有效性、入口就绪与月度补加、交战/博弈/局面已变、收保护国机制前提与收件国筛选（`recognized/unrecognized`、`<= minor_power`、非博弈对立）、`.32`/`.35` 守卫、两个哈里发触发（不依赖日志此刻开启）与 `.35` 自身持圣城判断。
  - `common/script_values/nesnd_ottoman_holy_cities.txt`：对手计分（汉志每州 +20、满足 `nesnd_rival_caliph` +30）与汉志直接持州计数。
  - `common/scripted_effects/nesnd_ottoman_holy_cities.txt`：选对手、统一入口 `nesnd_ottoman_holy_start`、R13 失自主月数维护、派发归附提议 `.32`、派发两个哈里发事件 `.34`、统一清理 `nesnd_ottoman_holy_cleanup`。
  - `common/journal_entries/nesnd_ottoman_holy_cities.txt`：新建「圣城」日志（无 `possible`/`is_shown_when_inactive`，240 月自定义期限，6 结局依次为：1 隐藏失效、2 失去自主、3 圣城归附、4 局面已变、5 圣城归于另一位哈里发〔期限届满且无战无博弈时全汉志在另一位哈里发手，失败头〕、6 圣城未归〔期限届满且无战无博弈时与结局 5 互斥，超时头〕，四档 `status_desc`）。
  - `common/scripted_buttons/nesnd_ottoman_holy_cities.txt`：新建「定下方略」（限一次，需汉志宣称，设 `conquer` 秘密目标，60 月军需/征兵修正）与「提议归附」（60 月冷却，向独立弱小汉志持有国发 `.32` 请其成保护国）。
  - `common/static_modifiers/nesnd_ottoman_holy_cities.txt`：新建 6 项静态修正（圣城归于另一位哈里发、虔诚派震怒、圣城未归、方略准备、虔诚派振奋、虔诚派疑虑）。
  - `common/customizable_localization/nesnd_ottoman_holy_cities.txt`：新建 `nesnd_ottoman_holy_foe_name`，从 `global_var:nesnd_holy_foe` 动态取对手名并带兜底键。
- **既有文件衔接**：
  - `common/on_actions/nesnd_ottoman_recovery.txt`：`on_monthly_pulse_country` 新增 `nesnd_ottoman_holy_fallback`（同时负责圣城日志补加与两个哈里发 `.34` 派发）。
  - `events/nesnd_ottoman_recovery.txt`：仅改 `.12` 选项 a 分圣城在手/不在手两条分支；文末新增 `.32`（提议归附）、`.33`（归附回音）、`.34`（两个哈里发·奥斯曼侧）、`.35`（两个哈里发·另一位哈里发侧）。
  - `common/scripted_triggers/nesnd_north.txt`、`common/scripted_triggers/nesnd_ottoman_levant.txt`：各仅加一行 `NOT = { global_var:nesnd_holy_foe ?= this }`。
  - `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`：同步追加 67 对新键，值均为 `TODO_CLAUDE`。

## 3. 怎么复测

1. 成功线完成「伊斯兰领袖」后在 `.12` 选 a：汉志仍在埃及朝贡下时核对不加 `nesnd_ottoman_caliphate`、设 `nesnd_ottoman_caliph_claimed` 并开启「圣城」日志（对手埃及）；汉志已属奥斯曼时核对直接得修正不开日志；选 b 时核对本批内容完全不出现。
2. 失败线「专制的主导权」苏丹胜出后推进一月，核对 `nesnd_ottoman_holy_fallback` 开启「圣城」日志；军营胜出不开。
3. 汉志独立为小国时测「提议归附」按钮、事件 `.32`/`.33`：接受后成为奥斯曼保护国并在下一次日志判定走「圣城归附」获 `nesnd_ottoman_caliphate` 与热情 +20；开局汉志为埃及朝贡国或被列强吞并时按钮不可用。
4. 触发唐衣大食完成远西战争（保持逊尼国教与唐/波斯/阿拉伯执政文化之一且非奥斯曼附属）后推进一月，核对 `.34` 触发一次（无论日志是否正开，只要已有 `nesnd_ottoman_caliphate`、`nesnd_ottoman_caliph_claimed` 或 `flag:sultan` 之一）、选 a 后另一位哈里发收 `.35`；另一位哈里发握有汉志全境时「圣城」以它为对手（+30 分）照常进行，状态句走第三段，240 个月期限届满且无战无博弈时才走失败结局 5「圣城归于另一位哈里发」（此前夺回汉志走结局 3「圣城归附」）。
5. 核对隐藏失效（换标签）、失去自主（12 月 + 24 月冷却）、局面已变（对手成附属或结盟 + 24 月冷却）、圣城未归（240 月且未战未博弈）及清理效果。

## 4. 遗留问题

- 本批 67 对中英新键均以 `TODO_CLAUDE` 占位；旧键 `nesnd_ottoman_islam_leader_win_event_tt` 是否随 `.12` 选项 a 改写由主会话决定。
- 结局变量 `nesnd_ottoman_holy_outcome` 当前只写不读，留给后续批次读取。
- 「圣城归附」结束后圣城再度易手的情形按第 15 条本批不处理。
