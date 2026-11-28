Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-28，奥斯曼 B13 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；模拟 `_agy_checks/ca_sim.py` 与 `_agy_checks/ca_sim_result.txt`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`、`_agy_checks/tree_diff.md`、`_agy_checks/grep6.txt` 与 `_agy_checks/je_defs_check.txt`

# 133 奥斯曼 B13：中亚（`nesnd_ottoman_central_asia`）

## 1. 现象与期望

西秦（`c:QE1`）拥有日志 `nesnd_qe1_frontier_journal`（「边疆诸部」），含南线阿富汗条、北线草原条与土库曼/希瓦/浩罕连锁响应；奥斯曼既有按钮 `nesnd_ottoman_fund_tribes`（「资助诸部」）此前挂在成功线「伊斯兰领袖」上，不推动西秦的两条边疆条，且失败线没有该按钮；中亚诸国建国后奥斯曼线也没有任何承接内容。

本批（B13）照「北非」范式新建对外日志 `nesnd_ottoman_central_asia`（「中亚」），成功线与失败线均在路线既定且满足条件时开启：将「资助诸部」从「伊斯兰领袖」移入本日志、改独立 24 个月冷却并接入西秦两条边疆条（`+0.15/月`，可被 `nesnd_qe1_frontier_bolstered` 归零）；新增「提议庇护」（收中亚独立本地小国为保护国或未受认可时的朝贡国，并触发对手抗议事件 `.44`）与「提议共同防御」（向与对手为敌且接壤的独立国家提议 5 年共同防御条约）。日志允许无对手开启并在月度补选对手，在拥有至少两个中亚本地国家作附属时完成；不写死对手、本地国或共同防御对象（新写标签仅 `c:TUR` 及「资助诸部」中的 `c:QE1`）。中英新增 77 对本地化键均以 `TODO_CLAUDE` 占位，由主会话填写玩家文字。

## 2. 改了什么

- **新建中亚日志、触发器、脚本值、效果、按钮、修正与自定义本地化**：
  - `common/scripted_triggers/nesnd_ottoman_central_asia.txt`：18 州中亚地区触发器（排除波斯开局 16 州、两河 3 州及开局已有 `c:KAL`/`c:MAK` 首都的 `STATE_BALUCHISTAN`/`STATE_SISTAN`）、当地国家 `nesnd_ottoman_ca_native`（不看等级）与本地国家 `nesnd_ottoman_ca_local`（调 `native` + 低于主要政权）、外来大国/奥斯曼附属计数（`>= 2`）、对手持地/候选/有效性、入口就绪、交战/博弈/局面已变（无对手时不成立）、收附属前提（兼容 `recognized` 保护国与 `unrecognized` 朝贡国）、庇护目标与事件 `.40` 守卫、共同防御对象与无参条约前提及事件 `.42` 守卫。
  - `common/script_values/nesnd_ottoman_central_asia.txt`：对手计分（18 州自身与附属每州 +20）、庇护目标持州排序权重、共同防御对象计分（交战 +30、与土友善 +10、主要政权及以上 +20）。
  - `common/scripted_effects/nesnd_ottoman_central_asia.txt`：选对手（无候选不存变量）、统一入口 `nesnd_ottoman_ca_start`、R13 失自主月数维护、派发 `.40` 与 `.42`（均带同 `limit` 的 `any_country` 守卫）、统一清理 `nesnd_ottoman_ca_cleanup`（保留 `nesnd_ottoman_ca_had_client` 与 `nesnd_ottoman_ca_funded_once`）。
  - `common/journal_entries/nesnd_ottoman_central_asia.txt`：新建「中亚」日志（无 `possible`/`is_shown_when_inactive`，240 月期限，月度维护失自主月数、补选对手与记录曾有附属 `nesnd_ottoman_ca_had_client`；6 结局依次为：1 隐藏失效、2 失去自主、3 诸国覆灭〔须曾有附属、无任何 `native` 国家、奥斯曼在中亚 18 州无州且有大国候选〕、4 中亚的庇护者、5 局面已变、6 搁置；五档 `status_desc`）。
  - `common/scripted_buttons/nesnd_ottoman_central_asia.txt`：移入 `nesnd_ottoman_fund_tribes`（24 月独立冷却 `nesnd_ottoman_ca_fund_cd`、补西秦边疆日志开启与国库够付前提、记 `nesnd_ottoman_ca_funded_once`），新建 `nesnd_ottoman_ca_protect`（60 月冷却，发 `.40`）与 `nesnd_ottoman_ca_compact`（60 月冷却，发 `.42`）。
  - `common/static_modifiers/nesnd_ottoman_central_asia.txt`：新建 4 项静态修正（诸国覆灭 −10 威望、中亚的庇护者 +5 威望、搁置 −10 威望、对手不理会 60 月 −10 威望）。
  - `common/customizable_localization/nesnd_ottoman_central_asia.txt`：新建 `nesnd_ottoman_ca_foe_name`，从 `global_var:nesnd_ca_foe` 动态取对手名并带兜底键。
- **既有文件衔接**：
  - `common/on_actions/nesnd_ottoman_recovery.txt`：`on_monthly_pulse_country` 新增 `nesnd_ottoman_ca_fallback` 与上方注释。
  - `events/nesnd_ottoman_recovery.txt`：事件 `.5`、`.6` 四选项各加一段满足 `nesnd_ottoman_ca_start_ready` 时开日志；文末新增 `.40`（提议庇护·本地小国侧）、`.41`（庇护回音·奥斯曼侧）、`.42`（提议共同防御·邻国侧）、`.43`（共同防御回音·奥斯曼侧）、`.44`（对手抗议·对手侧；选项 a 秘密目标 `antagonize` 仅在 `is_player = no` 时设给 AI）。
  - `common/journal_entries/nesnd_ottoman_islam_leader.txt`：仅删 `scripted_button = nesnd_ottoman_fund_tribes` 一行。
  - `common/scripted_buttons/nesnd_ottoman_islam_leader.txt`：删 `nesnd_ottoman_fund_tribes` 定义及上方两行注释，并更新第 3 行冷却说明注释。
  - `common/scripted_progress_bars/nesnd_qe1_frontier.txt`：两条边疆条的 `monthly_progress` 各加一行 `nesnd_qe1_fr_src_foreign`。
  - `common/script_values/nesnd_qe1_frontier.txt`：文末新增 `nesnd_qe1_fr_foreign_term`（+0.15 / 0）与两条 `shown_foreign` 包装值。
  - `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`：同步追加 77 对新键，值均为 `TODO_CLAUDE`。

## 3. 怎么复测

1. 成功线触发 `.5`、失败线触发 `.6`：核对均开启「中亚」日志且开局选中 `c:QE1` 为对手、尚未立下 `nesnd_ottoman_ca_had_client`、「提议庇护」不可用、「资助诸部」可用（西秦开着「边疆诸部」且国库够付）。
2. 按「资助诸部」：核对西秦获得 36 月 `nesnd_ottoman_tribes_funded`、`.1` 选 a 时西秦两条边疆条显示「外国资助」`+0.15/月`，选 b 得 `nesnd_qe1_frontier_bolstered` 后该项立即归零；核对「伊斯兰领袖」仅剩两枚按钮且与 `nesnd_ottoman_ca_fund_cd` 互不干扰。
3. 西秦边疆分出两国独立后：核对仅有本地国而无附属时不立 `nesnd_ottoman_ca_had_client`；按「提议庇护」发送 `.40`（成功线收保护国、失败线未受认可时收朝贡国），对方接受后次月立 `nesnd_ottoman_ca_had_client`、触发奥斯曼 `.41` 与对手 `.44`（AI 抗议才设 `antagonize`，玩家抗议只减关系，或不理会得 60 月威望 −10）；收满两国完成「中亚的庇护者」。
4. 核对「提议共同防御」在存在与对手为敌且接壤的独立国家并满足条约前提时发送 `.42`，对方接受后经 `nesnd_crimea_sign_defensive_pact` 签 5 年共同防御并发 `.43`。
5. 核对无对手开启、对手失效走「局面已变」后 24 月重开且保留 `nesnd_ottoman_ca_had_client`、失自主 12 月走「失去自主」、有过附属后所有 `native` 被吞并且奥斯曼在 18 州无州时走「诸国覆灭」（附属升主要政权、奥斯曼吞并唯一附属或附属被别国夺走时均不误触）、240 月到期走「搁置」。

## 4. 遗留问题

- 本批 77 对中英新键均以 `TODO_CLAUDE` 占位，留待主会话填写玩家文字。
- 结局变量 `nesnd_ottoman_ca_outcome` 当前只写不读，留待后续批次读取。
- 72 宣称按钮与 20 边疆州的重叠冲突、`STATE_BALUCHISTAN`/`STATE_SISTAN` 排除决定以及 `nesnd_ottoman_qe1.4` 触发器缺口均已记入 `_agy_checks/调研.md` 与 `_agy_checks/交付说明.md`。
