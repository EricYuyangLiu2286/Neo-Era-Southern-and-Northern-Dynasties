Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-26，奥斯曼 F2 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt` 与 `_agy_checks/tree_diff.md`；模拟 `_agy_checks/rtw_sim.py` 与 `_agy_checks/rtw_sim_result.txt`

# 126 奥斯曼 F2：北方战争通用化（克里米亚战争与俄土战争）

## 1. 现象与期望

已合并的克里米亚战争（成功线，B4）与未合并的俄土战争草稿（失败线，B7）原先均写死对手 `c:RUS`、帮手写死英／法／西秦，战果只认土俄两国直接对阵，且超时会在战中截断进行中的战争、俄土超时对峙误将俄国判负、俄国一侧无超时兜底（L-15、L-17–L-21）。

本批（F2）按全局重想规则 R2、R10、R11、R12、R13 将两条线改造为同一套通用写法：北方对手与外援帮手按当时局面动态评分挑选；战果按参战双方名单与目标州归属只读结果判定（坏结局先判）；新增与潜在北方对手结盟时的「海峡的代价」事件（`.20`）、「失去自主」与「局面已变」结局；用带期限变量替代引擎 `timeout` 以避免战中截断；为对手侧补足「搁置」结局与超时兜底；事件 `.19` 改用 F1 的 `nesnd_ottoman_conquer_goal_on_holders` 去写死；日志标题按当前北方对手动态切换。

## 2. 改了什么

- **共用北方战争框架**（新建 `common/scripted_triggers/nesnd_north.txt`、`common/scripted_effects/nesnd_north.txt`、`common/script_values/nesnd_north.txt`、`common/customizable_localization/nesnd_north.txt`）：
  - 统一声明北方目标 6 州与南方目标 6 州常量触发器；实现北方对手候选判定与评分（`c:RUS` 历史加权 +100）、帮手候选判定与评分（`c:GBR`/`c:FRA` 历史加权 +15）、有效对手检查与月度重选（`nesnd_north_foe_refresh`）。
  - 实现共享开战快照（`nesnd_north_snapshot` 写 `nesnd_north_tur_regions` 与 `nesnd_north_foe_regions`）、战时双方参战名单月度维护（`nesnd_north_war_roster_update`）、统一战果信号钩子（`nesnd_north_handle_wargoal_enforced`、`nesnd_north_handle_won_war`）、统一胜负／平局／局面已变判定（`nesnd_north_tur_lost` / `_won` / `_drawn` / `_situation_changed`）与统一清理效果（`nesnd_north_cleanup`）。
  - 通过自定义本地化 `nesnd_crimea_title`、`nesnd_rtw_title` 实现对手为俄国时显示「克里米亚战争」「俄土战争」、否则显示「北方战争」「北方的威胁」。
- **成功线「克里米亚／北方战争」返工**（`common/journal_entries/nesnd_crimea.txt`、`common/scripted_triggers/nesnd_crimea.txt`、`common/scripted_effects/nesnd_crimea.txt`、`common/on_actions/nesnd_crimea.txt`、`events/nesnd_crimea.txt`、`common/scripted_buttons/nesnd_ottoman_islam_leader.txt`、`common/journal_entries/nesnd_ottoman_islam_leader.txt`、`common/journal_entries/nesnd_ottoman_charter.txt`）：
  - 全部 `c:RUS` 改读 `global_var:nesnd_north_foe`；`nesnd_ottoman_has_major_ally` 改为任一 great power；`nesnd_ottoman_challenge_russia` 补对手有效与战时 AI 权重乘 0。
  - 删除 `nesnd_crimea_invite_fra`、`nesnd_crimea_invite_qe1`、`nesnd_crimea.2` 与写死的 `nesnd_crimea_fra`／`nesnd_crimea_qe1`，合并为通用帮手日志 `nesnd_crimea_helper`（仅在帮手答应出兵时授予）。
  - `nesnd_crimea_tur` 改为 7 结局统一判序（败 → 失去自主 → 胜 → 无果 → 局面已变 → 120 月期限变量超时 → 隐藏失效），`nesnd_crimea_rus` 隐藏失效改读 `global_var:nesnd_north_foe` 并加 4400 天兜底超时。
- **失败线「俄土／北方的威胁」与通用求援返工**（`common/journal_entries/nesnd_rtw.txt`、`common/scripted_buttons/nesnd_rtw.txt`、`common/scripted_triggers/nesnd_rtw.txt`、`common/scripted_effects/nesnd_rtw.txt`、`common/static_modifiers/nesnd_rtw.txt`、`common/on_actions/nesnd_rtw.txt`、`events/nesnd_rtw.txt`、`events/nesnd_ottoman_qe1.txt`）：
  - 新建通用「寻求外援」按钮 `nesnd_north_seek_help`（两条线共用、12 月冷却 `nesnd_north_help_cd`、最多两次、选中西秦且克里米亚战前阶段改发 `nesnd_ottoman_qe1.3`，其余发通用 `nesnd_rtw.1–.3`）；删 `nesnd_rtw_ask_gbr`。
  - `nesnd_rtw_ask_qe1` 补全西秦独立、不在内战及 `c:PER` 为西秦附属且正与奥斯曼交战时不可用的前提；`events/nesnd_ottoman_qe1.txt` `.2–.4` 对俄判断改读 `global_var:nesnd_north_foe`。
  - `nesnd_rtw_tur` 改为与克里米亚同序的 7 结局（白和算守住、180 月期限变量超时写 `flag:standoff` 而不判对手失败）；`nesnd_rtw_rus` 新增无惩罚「搁置」结局（永久修正 `nesnd_rtw_rus_shelved_mod`、`flag:shelved`）与 6210 天兜底超时。
- **月脉与事件**（`common/on_actions/nesnd_ottoman_recovery.txt`、`events/nesnd_ottoman_recovery.txt`）：
  - 月度列表新增 `nesnd_north_foe_refresh`、`nesnd_ottoman_straits_check`、`nesnd_north_war_roster_monthly`，删 `nesnd_rtw_white_peace_check`。
  - `.14`、`.15` 改读 `global_var:nesnd_north_foe`；`.19` 两个选项改调 `nesnd_ottoman_conquer_goal_on_holders`（两河三州与巴尔干有宣称失地）；新增 `.20`「海峡的代价」。
- **本地化**（`localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`）：
  - 同步删去旧按钮／旧日志／`.2` 的废弃键，改写所有把俄／法／英当作固定对手或帮手的文本，新增通用求援、海峡的代价、局面已变、失去自主、搁置与动态标题键。

## 3. 怎么复测

1. 正常开局下确认 `nesnd_ottoman_islam_leader` 或失败线进入俄土前置时 `global_var:nesnd_north_foe` 选中 `c:RUS`，日志标题显示「克里米亚战争」／「俄土战争」；若俄国沦为附属或与土结盟且另有合格列强，确认重选新对手并切换标题为「北方战争」／「北方的威胁」。
2. 让奥斯曼与俄国结盟且无其他候选，确认触发 `.20`「海峡的代价」并验证两选项关系效果；破盟后确认下月重选重新生效。
3. 在克里米亚与俄土两条线测试「寻求外援」按钮（最多两次、12 月冷却、战前／博弈可用、开战后禁用），验证通用事件 `nesnd_rtw.1–.3`、`nesnd_crimea_helper` 授予与 `nesnd_ottoman_qe1.3` 分流，以及「向西秦求援」在西秦内战或波斯作为西秦附属与土交战时灰显。
4. 测试战时盟友代为执行战争目标、同时失地与得地（坏的先判）、白和（克里米亚无果／俄土守住）、战中对手被吞并或博弈中变附属（走「局面已变」且 24 月后可重开）、第 179 月开战跨过 180 月期限不截断、连续 12 月失去自主且未开战、奥斯曼改标签时对手侧安全结束。

## 4. 遗留问题

- 鲁米利亚、东方诸省与事件 `.18` 中的 `c:RUS` 依规则第 27 条留待 F3 处理；「资助西秦诸部」按钮留待 B13；`.12`、`.13` 不在本批修改范围内。
- 只写不读的变量 `nesnd_ottoman_straits`、`nesnd_ottoman_revenge`、`nesnd_rtw_rus_outcome` 预留给后续批次或存档留档。
