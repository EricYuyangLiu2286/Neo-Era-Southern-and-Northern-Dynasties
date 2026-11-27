Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-27，奥斯曼 B8 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；模拟 `_agy_checks/autocracy_sim.py` 与 `_agy_checks/autocracy_sim_result.txt`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt` 与 `_agy_checks/tree_diff.md`

# 128 奥斯曼 B8：失败线·社会「专制的主导权」

## 1. 现象与期望

坦志麦特失败后的奥斯曼失败线（`nesnd_ottoman_route = flag:sultanic`）此前仅有内政（鲁米利亚、东方诸省）与外交（俄土战争 / 北方威胁），缺少社会与专制主导权一块；同时成功线「宪章与军营」中的秦式国家结局效果尚未抽成共用脚本效果。

本批（B8）照成功线 `nesnd_ottoman_charter` 的两套议程结构，新增失败线社会日志 `nesnd_ottoman_autocracy`（「专制的主导权」），呈现苏丹的泛伊斯兰一方与秦制军人一方争夺专制主导权、以及地方显贵在僵局中坐大的过程；补上三项共用 24 个月冷却的按钮、两则月度随机事件（谢赫伊斯兰的教令、普鲁士与西秦两国教官）、R13 首都沦陷修正维护，并把秦式国家结局效果抽成 `nesnd_ottoman_found_qin_state` 供两线共用。

## 2. 改了什么

- **新日志、触发器、脚本值、按钮、修正与共用效果**：
  - `common/journal_entries/nesnd_ottoman_autocracy.txt`：新建「专制的主导权」日志（240 个月期限，3 枚按钮，`on_monthly_pulse` 维护 `nesnd_ottoman_capital_fallen` 并掷骰 `.21`/`.22`，苏丹胜 / 军人胜 / 超时地方显贵坐大 / 隐藏失效四结局，不设 `event_outcome_desc` 由效果栏原生显示；苏丹胜撤换秦制领袖前先清利益集团与人物上的 `nesnd_qinist_allowed`；三档状态描述）。
  - `common/scripted_triggers/nesnd_ottoman_autocracy.txt`：新建 `p1`–`p8`、`m1`–`m8`（其中 `p6` 与 `m5` 同属土地改革法组互斥，其余 `p4`/`p5`/`m4`/`m6` 独立）、军人议程达标、平分裁决（R10）、月度补加，以及 `.22` 使用的 `nesnd_ottoman_prussian_mission_valid`、`nesnd_ottoman_qin_instructors_available` 触发器。
  - `common/script_values/nesnd_ottoman_autocracy.txt`：新建双方现算分数与差值脚本值。
  - `common/scripted_effects/nesnd_ottoman_autocracy.txt`：抽出共用效果 `nesnd_ottoman_found_qin_state`（开头判 `NOT = { has_modifier = nesnd_ottoman_qin_state }`）与首都沦陷清理效果 `nesnd_ottoman_autocracy_clear_capital_fallen`。
  - `common/scripted_buttons/nesnd_ottoman_autocracy.txt`：新建「任用乌理玛」「任用军人」「整肃报刊」三枚按钮，共用 24 个月冷却 `nesnd_ottoman_autocracy_cd`。
  - `common/static_modifiers/nesnd_ottoman_autocracy.txt`：新建结局、按钮、事件与首都沦陷所需的 12 项修正（其中 `nesnd_ottoman_sultan_supreme` 给合法性 +10 与威望 +5，避免与宗教集团好感修正叠加）。
- **既有文件衔接**：
  - `common/journal_entries/nesnd_ottoman_charter.txt`：秦制结局改为调用 `nesnd_ottoman_found_qin_state`，行为不变。
  - `common/on_actions/nesnd_ottoman_recovery.txt`：`on_monthly_pulse_country` 新增 `nesnd_ottoman_autocracy_fallback` 动作与注释，兼顾补加日志及日志不在位时兜底清理 `nesnd_ottoman_capital_fallen`。
  - `events/nesnd_ottoman_recovery.txt`：事件 `.6` 两选项各补开日志一行；文末新增 `.21`「谢赫伊斯兰的教令」与 `.22`「两国教官」（R11 b 类：普鲁士与西秦，按普鲁士使团与西秦可聘与否分三种局面；改聘秦人教官给 120 个月 `nesnd_ottoman_barracks_bonus`，普鲁士不在时提供本国教官选项 c）。
- **中英本地化**：
  - `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`：同步新增 50 对中英键。

## 3. 怎么复测

1. 在坦志麦特失败后触发事件 `.6`，分别选「苏丹亲政」与「依靠军营」，核对日志「专制的主导权」直接开启、倾向项对应亮起；对已过 `.6` 的旧存档推进一个月，核对月度补加正常开出日志且不重复开启。
2. 逐项验证 `p1`–`p8` 与 `m1`–`m8` 计分、4 项法律门槛以及同月双达标时的高分胜与平分按 `.6` 倾向裁决；测试苏丹胜（清 `nesnd_qinist_allowed` 后撤换秦制领袖且新领袖不再是秦制主义者、效果栏原生显示且 `nesnd_ottoman_sultan_supreme` 给威望而非叠加宗教好感）、军人胜（共用秦式国家效果加宗教集团永久降好感）、超时（地方显贵坐大）三结局。
3. 测试三枚按钮的 24 个月共用冷却与效果；测试 `.21`（60 个月冷却、颁行得 60 个月加分）与 `.22`（仅发一次；核对普鲁士使团与西秦均在、仅普鲁士在、仅西秦在三种局面的正文与选项 a/b/c 显示，以及选项 b 给 120 个月加分；两者皆不在时不触发）。
4. 在日志开启期间失去东色雷斯，核对次月加上「都城失守」修正，收回后次月摘除，日志任意结局关闭时一并摘除；若异常情况下日志已不在位仍残留该修正，次月由 `nesnd_ottoman_autocracy_fallback` 兜底摘除。
5. 在成功线「宪章与军营」触发秦制结局，核对抽取 `nesnd_ottoman_found_qin_state` 后行为与改前完全一致。

## 4. 遗留问题

- 结局变量 `nesnd_ottoman_autocracy_outcome`（`flag:sultan` / `flag:barracks` / `flag:notables`）留待后续批次（如哈里发与远期路线）读取。
- 「伊斯兰的启蒙与解放神学」节点、哈里发名义、两河与埃及联动按任务规定留待后续批次。
