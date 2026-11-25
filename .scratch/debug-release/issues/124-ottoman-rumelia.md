Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-25，奥斯曼 B6 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 基线索引 `_agy_base/v3tree/index`；调研 `_agy_checks/调研.md`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`；模拟 `_agy_checks/rumelia_sim.py` 与 `_agy_checks/rumelia_sim_result.txt`

# 124 奥斯曼：鲁米利亚与东方诸省

## 1. 现象与期望

坦志麦特失败后「苏丹的帝国」路线的第一块内政内容（B6）：落地奥斯曼「鲁米利亚」（`nesnd_ottoman_rumelia`，接原版大东方危机 `je_great_eastern_crisis`）与「东方诸省」（`nesnd_ottoman_eastern_provinces`，面向埃尔祖鲁姆／迪亚巴克尔／卡尔斯三州与库尔德／亚美尼亚文化少数运动）两份日志、各自三个行动按钮，以及俄国一侧的回应事件「保护基督徒」（`nesnd_ottoman_recovery.18`）。严格遵循 R2，只作用于接纳度、激进派、热忱、恶名、关系、宣称与集团好感等原版输入，不直接修改原版危机进度条。

## 2. 改了什么

- **入口与触发器**（`common/on_actions/nesnd_ottoman_recovery.txt`、`common/scripted_triggers/nesnd_ottoman_rumelia.txt`、`common/script_values/nesnd_ottoman_rumelia.txt`）：
  - 在 `on_monthly_pulse_country` 追加 `nesnd_ottoman_rumelia_fallback` 与 `nesnd_ottoman_eastern_provinces_fallback`，分别按 `flag:sultanic` 失败线条件补加两份日志；两日志均无 `possible` 与 `is_shown_when_inactive`。
  - 新增脚本值 `nesnd_ottoman_east_force_count` 汇总东方诸省「镇压」与「部落骑兵」计数。
- **日志「鲁米利亚」与三按钮**（`common/journal_entries/nesnd_ottoman_rumelia.txt`、`common/scripted_buttons/nesnd_ottoman_rumelia.txt`、`common/scripted_effects/nesnd_ottoman_rumelia.txt`、`common/static_modifiers/nesnd_ottoman_rumelia.txt`）：
  - 开启时在 TUR 持有的每个巴尔干州（`region = sr:region_balkans`）设州变量 `nesnd_ottoman_rumelia_held`。
  - 三按钮共用 24 月冷却 `nesnd_ottoman_rumelia_cd`：「宪章」（各巴尔干州最大非主要文化 60 月接纳度 +10，宗教与地主集团 60 月好感 −2）、「自治」（按动荡最高选出非首都巴尔干州，经 `create_dynamic_country` 释放为新国并建 `protectorate`/`tributary` 附属，合法性 −10 持续 60 月）、「镇压」（有文化少数运动的巴尔干州加小量激进、最大非主要文化热忱目标 +5 持续 60 月、与俄关系 −15；第三次镇压触发俄国 `.18`，限一次）。
  - 结局均带 `event_outcome_desc`：大东方危机以 `eastern_crisis_controlled` 结束得永久修正与 `flag:held`；以 `eastern_crisis_not_controlled` 结束或 300 个月超时对失去的原持巴尔干州加宣称、永久合法性 −5、设 `flag:lost`；所有结局及隐藏 invalid 均清理 `nesnd_ottoman_rumelia_held`。
- **日志「东方诸省」与三按钮**（`common/journal_entries/nesnd_ottoman_rumelia.txt`、`common/scripted_buttons/nesnd_ottoman_eastern_provinces.txt`）：
  - 入口要求失败线、持有东方三州（`STATE_ERZURUM`、`STATE_DIYARBAKIR`、`STATE_KARS`）至少一州且存在库尔德或亚美尼亚文化少数运动。
  - 三按钮共用独立 24 月冷却 `nesnd_ottoman_east_cd`：「部落骑兵」（60 月军事修正、三州亚美尼亚人口激进增加）、「宪章」（亚美尼亚文化 60 月接纳度 +15、俄国关系 +15、宗教集团好感 −2）、「镇压」（三州激进增加、恶名 +5、俄英关系各 −15；第三次镇压触发俄国 `.18`，限一次）。
  - 四结局加隐藏 invalid：宪章 ≥ 3 得亚美尼亚永久接纳度与 `nesnd_ottoman_armenian_millet`、改善俄国关系、`flag:charter`；镇压加骑兵 ≥ 3 且三州已无库尔德／亚美尼亚文化少数运动得永久 `nesnd_ottoman_tribal_cavalry`、`flag:crushed`；尽失三州得永久合法性 −5、`flag:lost`；240 个月超时得永久 `nesnd_ottoman_eastern_unrest`、`flag:unresolved`。
- **俄国事件「保护基督徒」**（`events/nesnd_ottoman_recovery.txt` 追加 `.18`）：
  - 仅对 `c:RUS` 触发，按 `nesnd_ottoman_rus_protect_source`（`flag:rumelia`/`flag:eastern`）分支正文；选项 a 优先按 `dp_return_state`（配目标州与防御方 `humiliation`）对 TUR 发起外交博弈（无法开博弈时退回关系 −40 与 `antagonize` 秘密目标），AI 权重 70（战时降为 10）；选项 b 外交抗议（关系 −20、60 月威望 +10），AI 权重 30。
- **本地化**：中英同增 68 键于 `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml` 与 `localization/english/replace/nesnd_ottoman_l_english.yml`。

## 3. 怎么复测

1. 控制台 `tag TUR`，令坦志麦特超时失败并走「苏丹的帝国」路线（`nesnd_ottoman_route = flag:sultanic`）且原版 `je_great_eastern_crisis` 进行中，下月确认 `nesnd_ottoman_rumelia` 开启并标记当前巴尔干州；逐一测试「宪章」「自治」「镇压」按钮冷却、动态附属创建及第三次镇压后俄国收到 `nesnd_ottoman_recovery.18`（巴尔干分支）。
2. 在大东方危机已结束的存档上确认 `nesnd_ottoman_rumelia` 不开启；确认危机以 `eastern_crisis_controlled` 或 `eastern_crisis_not_controlled` 结束时分别走遏制或失控（含失地宣称）结局并清理州变量。
3. 当东方三州存在库尔德或亚美尼亚文化少数运动时，确认下月开启 `nesnd_ottoman_eastern_provinces`；测试三按钮与宪章／镇压完成／失守／超时四种结局及第三次镇压触发俄国 `.18`（东方分支）；另切 `tag RUS` 测 `event nesnd_ottoman_recovery.18` 两个选项的博弈发起与抗议修正。

## 4. 遗留问题

- 无阻塞项；`nesnd_ottoman_rumelia_outcome` 与 `nesnd_ottoman_east_outcome` 在 `xcheck_diff` 与 `tree_diff` 中呈只写不读，预留给后续 B7（「1878 年战争」「向东报复」）读取。
