Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-24，奥斯曼 B4 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 基线索引 `_agy_base/v3tree/index`；调研 `_agy_checks/调研.md`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`；模拟 `_agy_checks/crimea_sim.py` 与 `_agy_checks/crimea_sim_result.txt`

# 122 奥斯曼：伊斯兰领袖与克里米亚战争

## 1. 现象与期望

坦志麦特成功后的第二块路线内容（外交）：落地奥斯曼「伊斯兰领袖」日志（`nesnd_ottoman_islam_leader`）、四方全局「克里米亚战争」日志（`nesnd_crimea_tur`/`rus`/`fra`/`qe1`）以及俄国、法国、西秦一侧的互动事件与按钮，严格遵守 R2（战争与运动由引擎推进）与西秦旧文件只读约束。

## 2. 改了什么

- **新日志 `nesnd_ottoman_islam_leader`**（`common/journal_entries/nesnd_ottoman_islam_leader.txt`）：
  - 入口同 `nesnd_ottoman_charter`：事件 `nesnd_ottoman_recovery.5` 两选项加入 + `common/on_actions/nesnd_ottoman_recovery.txt` 新增 `nesnd_ottoman_islam_leader_fallback`；`immediate` 设 60 个月倒计时变量并补设对俄 `antagonize` 秘密目标。
  - 结局：完成（克里米亚胜，或已得「东方秩序」且日志满 60 个月）给永久修正 `nesnd_ottoman_islam_leader`、宣称中亚 17 州与高加索 5 州，发事件 `.12`「哈里发还是列强」（永久修正 `nesnd_ottoman_caliphate` 或 `nesnd_ottoman_concert` + 英法大升关系 + 高关系方防御同盟）；失败（俄胜且不完整持有巴格达）清零扩张热情、永久修正 `nesnd_ottoman_crimean_humiliation`、发事件 `.13` 转回「重整东方秩序」；300 个月超时给 `nesnd_ottoman_leader_unclaimed`。结局均写 `event_outcome_desc` 与 `nesnd_ottoman_islam_leader_outcome`。
  - 按钮（`common/scripted_buttons/nesnd_ottoman_islam_leader.txt`）：「资助诸部」「与西秦结约抗俄」（共用 24 个月冷却）与「向俄国开战」。
- **全局克里米亚战争**（`common/journal_entries/nesnd_crimea.txt`、`common/scripted_effects/nesnd_crimea.txt`、`common/scripted_triggers/nesnd_crimea.txt`、`common/on_actions/nesnd_crimea.txt`、`common/static_modifiers/nesnd_crimea.txt`）：
  - 两条启动路径：TUR 按钮发起 `dp_return_state` 博弈并调 `nesnd_crimea_start`；RUS 年度检查（`on_yearly_pulse_country`）玩家走 `nesnd_crimea.1`，AI 按年份与对土关系档分枝掷骰发起。
  - 参战按钮「请法国参战」「请西秦参战」分别触发 `nesnd_crimea.2`、`nesnd_ottoman_qe1.3`，接受方按发起/守方调 `add_initiator_backers`/`add_target_backers` 加入。
  - 胜负由 `on_wargoal_enforced`、`on_won_war`、`on_capitulation` 记录并在停战后结算，写全局变量 `nesnd_crimea_result`（`flag:ottoman`/`russia`/`none`）；俄胜时若 `nesnd_ottoman_charter` 在进行则给宪政派 60 个月加分（`nesnd_ottoman_charter_bonus`）；法/秦按参战与否 × 胜负给永久修正或关系变化。
- **西秦一侧**（新文件 `events/nesnd_ottoman_qe1.txt`，未改西秦任何旧文件）：`.1`「奥斯曼资助诸部」（抗议设 `antagonize` 或花钱加 `nesnd_qe1_frontier_bolstered` 抵消推力，记 120 月 `nesnd_qe1_tribes_funded_by_tur`）、`.2`「奥斯曼邀约抗俄」（签 5 年防御同盟或拒绝）、`.3`「奥斯曼请兵抗俄」。
- **本地化**：中英同增 147 键于 `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml` 与 `localization/english/replace/nesnd_ottoman_l_english.yml`。

## 3. 怎么复测

控制台 `tag TUR`，坦志麦特成功后触发 `nesnd_ottoman_recovery.5` 确认 `nesnd_ottoman_islam_leader` 开启；测试三个按钮（资助诸部、结约抗俄、向俄国开战）与克里米亚战争中「请法国参战」「请西秦参战」；用 `event nesnd_ottoman_recovery.12`–`.15`、`nesnd_crimea.1`–`.4`、`nesnd_ottoman_qe1.1`–`.3` 检查弹窗文案、作用域替换与选项提示。

## 4. 遗留问题

- `nesnd_ottoman_islam_leader_outcome` 预留给后续批次读取（当前只写不读，同 B3 的 `nesnd_ottoman_charter_outcome`）。
- 原版 `gov_caliphate` 写死 `c:SOK`，按总纲第八节代定 2 退路以永久修正 `nesnd_ottoman_caliphate` 代替，未复制原版 `01_monarchies.txt`。
- 「两河」节点与「1845 之后的埃及」节点按计划留给 B9。
