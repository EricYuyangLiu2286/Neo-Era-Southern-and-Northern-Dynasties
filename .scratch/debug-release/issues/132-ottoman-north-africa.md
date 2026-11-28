Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-27，奥斯曼 B12 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；模拟 `_agy_checks/na_sim.py` 与 `_agy_checks/na_sim_result.txt`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`、`_agy_checks/tree_diff.md`、`_agy_checks/grep6.txt` 与 `_agy_checks/je_defs_check.txt`

# 132 奥斯曼 B12：北非（`nesnd_ottoman_north_africa`）

## 1. 现象与期望

开局的黎波里塔尼亚（`c:TRI`）是奥斯曼傀儡、突尼斯（`c:TUN`）是奥斯曼保护国、君士坦丁（`c:CON`）与奥斯曼关系 +30；法兰西持有原版日志 `je_conquest_of_algeria` 争夺奥兰、阿尔及尔、君士坦丁三地；原版坦志麦特超时事件 `sick_man.3` 会放走奥斯曼的保护国与傀儡并把奥斯曼变为未受认可国家；原版 `algeria_events.8` 选项 b 可让阿尔及利亚成为奥斯曼傀儡或附庸。奥斯曼线此前没有任何北非内容。

本批（B12）照「圣城」「黎凡特」范式新建对外日志 `nesnd_ottoman_north_africa`（「北非」），成功线与失败线均在路线既定且满足条件时开启：奥斯曼须保住或收回属地地区（`STATE_TRIPOLI`、`STATE_TUNISIA`；`STATE_LIBYA` 开局 >80% 在分散部落手里不列入；经 `nesnd_ottoman_na_dependency_state` 排除分散部落及首都非属地地区的独立非大国如开局费赞）并了结阿尔及利亚问题（外来大国退出阿尔及利亚三地，或与之划界）。日志允许无对手开启并在月度脉冲中补选对手；不写死对手或属地国名（新写标签只有 `c:TUR`）。设 3 枚按钮（扶持抵抗、提议划界、重申宗主权）、4 则事件（`.36`–`.39`）、6 项按隐藏失效优先与 R10/R12/R13 排序的结局；并在北方战争与黎凡特帮手分数脚本值各加「划界伙伴加分、未划界对手减分」两段，同时不从帮手候选里排除北非对手。中英新增 73 对本地化键均以 `TODO_CLAUDE` 占位，由主会话填写玩家文字。

## 2. 改了什么

- **新建北非日志、触发器、脚本值、效果、按钮、修正与自定义本地化**：
  - `common/scripted_triggers/nesnd_ottoman_north_africa.txt`：属地地区与阿尔及利亚三地区州触发器、属地州筛选（`nesnd_ottoman_na_dependency_state`，排除分散部落及首都非属地地区的独立非大国如费赞）与属地归属/失守判断、外来大国与本地小国识别、对手持地/候选/有效性、入口就绪、交战/博弈/局面已变（无对手时不成立）、抵抗者筛选、划界（含不在博弈中对立）与重申宗主权事件守卫、收附属机制前提（兼容成功线 `recognized` 收保护国与 `sick_man.3` 后失败线 `unrecognized` 收朝贡国）。
  - `common/script_values/nesnd_ottoman_north_africa.txt`：对手计分（五地区自身与附属每州 +20）、阿尔及利亚三地区直接持州计数、属地重申宗主权目标持州计分。
  - `common/scripted_effects/nesnd_ottoman_north_africa.txt`：选对手（无候选不存变量）、统一入口 `nesnd_ottoman_na_start`、R13 失自主月数维护、放弃阿尔及利亚三地区宣称、派发重申宗主权事件 `.38`、统一清理 `nesnd_ottoman_na_cleanup`（清理效果本身保留 `nesnd_ottoman_na_demarcated` 与对方身上的 240 月 `nesnd_ottoman_na_partner`）。
  - `common/journal_entries/nesnd_ottoman_north_africa.txt`：新建「北非」日志（无 `possible`/`is_shown_when_inactive`，240 月期限，月度维护失自主月数与补选对手；6 结局依次为：1 隐藏失效、2 失去自主、3 属地尽失、4 北非的宗主权、5 局面已变〔单清 `nesnd_ottoman_na_demarcated`〕、6 搁置；五档 `status_desc`，其中已划界排在属地不全在手之前）。
  - `common/scripted_buttons/nesnd_ottoman_north_africa.txt`：新建「扶持抵抗」（36 月冷却，受助国得 60 月陆军防御 +5% 与关系 +20、对手关系 −20、记 `nesnd_ottoman_na_backed_once`；北方帮手候选 −10 减分仅在北方战争开着时生效）、「提议划界」（60 月冷却，发 `.36`）与「重申宗主权」（60 月冷却，发 `.38`）。
  - `common/static_modifiers/nesnd_ottoman_north_africa.txt`：新建 4 项静态修正（属地尽失 −10 威望、北非宗主权 +5 威望、搁置 −10 威望、扶持抵抗 60 月 +5% 陆军防御）。
  - `common/customizable_localization/nesnd_ottoman_north_africa.txt`：新建 `nesnd_ottoman_na_foe_name`，从 `global_var:nesnd_na_foe` 动态取对手名并带兜底键。
- **既有文件衔接**：
  - `common/on_actions/nesnd_ottoman_recovery.txt`：`on_monthly_pulse_country` 新增 `nesnd_ottoman_na_fallback` 与上方注释。
  - `events/nesnd_ottoman_recovery.txt`：事件 `.5`、`.6` 四个选项各加一行满足 `nesnd_ottoman_na_start_ready` 时开日志；文末新增 `.36`（提议划界·对手侧）、`.37`（划界回音·奥斯曼侧）、`.38`（重申宗主权·属地小国侧）、`.39`（重申宗主权回音·奥斯曼侧）。
  - `common/script_values/nesnd_north.txt`、`common/script_values/nesnd_ottoman_levant.txt`：在 `nesnd_north_helper_score`（±15）与 `nesnd_ottoman_levant_helper_score`（±25）各加「有 `nesnd_ottoman_na_partner` 加分」「是 `global_var:nesnd_na_foe` 且奥斯曼未划界减分」两段；帮手候选触发器未动。
  - `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`：同步追加 73 对新键，值均为 `TODO_CLAUDE`。

## 3. 怎么复测

1. 成功线触发 `.5`：核对开「北非」日志、选中法兰西为 `global_var:nesnd_na_foe`；测试「扶持抵抗」（受助国得 60 月防御修正与关系 +20，对手关系 −20，记 `nesnd_ottoman_na_backed_once`）与「提议划界」（`.36` 接受后弃宣称、关系 +30、奥斯曼设 `nesnd_ottoman_na_demarcated`、对手得 240 月 `nesnd_ottoman_na_partner`、奥斯曼收 `.37`）。
2. 失败线触发 `sick_man.3` 放走 `c:TRI` 与 `c:TUN` 并置奥斯曼为 `unrecognized`，次月 `.6` 开「北非」日志：核对「重申宗主权」立即可用，按持州优先发给 `c:TRI`（`.38` 接受后成为朝贡国；若奥斯曼恢复 `recognized` 则收为保护国），不走「属地尽失」。
3. 核对 `STATE_TRIPOLI` 内的独立 `c:FZN` 与分散部落 `c:ZWY`：二者均不满足 `nesnd_ottoman_na_dependency_state`，开局即满足 `nesnd_ottoman_na_suzerainty_held`，且大国吞并的黎波里与突尼斯的属地州时照常触发「属地尽失」；若 `c:FZN` 成为他国附属则计入属地州。
4. 核对无对手开日志时：不走「局面已变」、月度出现新候选自动补选、240 月后走「搁置」；核对对手失效走「局面已变」+ 清旧 `nesnd_ottoman_na_demarcated` + 24 月重开冷却、失自主 12 月走「失去自主」+ 24 月重开冷却。
5. 核对划界后法兰西在北方战争与黎凡特求援中的帮手分数加分（+15 / +25），未划界前作为北非对手减分（−15 / −25）且仍保留在帮手候选内。

## 4. 遗留问题

- 本批 73 对中英新键均以 `TODO_CLAUDE` 占位，留待主会话填写玩家文字。
- 结局变量 `nesnd_ottoman_na_outcome` 当前只写不读，留待后续批次读取。
- `sick_man.3` 把奥斯曼变为 `unrecognized` 后「重申宗主权」以朝贡国承接的做法已在 `_agy_checks/调研.md` 与 `_agy_checks/交付说明.md` 中说明。
