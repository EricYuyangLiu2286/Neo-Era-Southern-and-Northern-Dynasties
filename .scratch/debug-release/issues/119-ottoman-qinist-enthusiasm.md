Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-24，「源目录写法整理」会话调度的奥斯曼 B1）
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-ottoman-b1-20261124T154956Z/`；报告 `nesnd-workbench/reports/2026-11-24-ottoman-qinist/`（交付记录.md、法律组合.md、sim/、checks/、顶层设计/）

# 119 奥斯曼：秦制主义者领袖事件与扩张热情重算

## 1. 现象与期望

奥斯曼中后期线第 1 批（提示词 `nesnd-workbench/reports/2026-11-24-ottoman-qinist/B1-提示词-奥斯曼秦制与热情.txt`）：查清坦志麦特进行中、成功后、失败后的法律组合；秦式军改期间每月 5% 让小市民、地主、军队之一的领袖改持秦制主义者；重算三种情况下的扩张热情，加入法律与秦制主义者领袖人气两项；6472d99 的「推行秦式军改 −3」让 AI 十年只能买 0.4 个宣称，要解决。

## 2. 原因

新内容。热情条 `common/scripted_progress_bars/nesnd_ottoman_recovery.txt` 原有五项；秦制主义者意识形态 `common/ideologies/ce_leader_ideologies.txt:1` 的三处触发器只认西秦、汉裔波斯与西秦内战国，且集团领袖不含地主；AI 军改按钮权重 20、战时 +60，十年约 114 个月在军改。

## 3. 改了什么

- `common/script_values/nesnd_ottoman_recovery.txt`：坦志麦特一项改为 2 / 1.25 / 0（成功、进行中、失败），新增秦式军改代价（−1.5 / −2 / −2.5）、秦制主义者人气（人气和 ÷50，夹在 −1 与 2）、七个法组各一项（合拍 +0.25、背离 −0.25）。
- `common/scripted_progress_bars/nesnd_ottoman_recovery.txt`：加八行（秦制主义者一行、法组七行），「推行秦式军改」改读按情况分档的脚本值。
- `common/scripted_buttons/nesnd_ottoman_recovery.txt`：AI 军改权重 1，战时 +40（只动 AI）。
- `common/journal_entries/nesnd_ottoman_recovery.txt`：加回 `on_monthly_pulse`，只放事件掷骰（95 = 0、5 = 事件）。
- `events/nesnd_ottoman_recovery.txt`：新事件 `nesnd_ottoman_recovery.2`「从军法到国制」。变量 `nesnd_qinist_allowed` 同时设在领袖和所在集团上（集团领袖触发器的根可能是人物，也可能是集团）。
- `common/scripted_triggers/nesnd_ottoman_recovery.txt`：`nesnd_ottoman_qinist_candidate`（集团作用域）、`nesnd_qinist_origin_country`（国家作用域，抄自意识形态原有的国别条件）。
- `common/ideologies/ce_leader_ideologies.txt`：三处触发器各加一条读人物变量 `nesnd_qinist_allowed` 的 OR 分支，原有条件不动；另两处的原有分支加「本国是原来那几国」，防止奥斯曼有了一个带变量的领袖后，其他集团自然刷出秦制主义者。
- 本地化 `nesnd_ottoman_l_*.yml`（replace）：中英各 12 键。

## 4. 怎么复测

奥斯曼开局，控制台加日志后按「推行秦式军改」，过几个月等事件弹出，看领袖意识形态与热情条明细的秦制主义者、法组七行。坦志麦特成功、失败两档分别看「坦志麦特的进程与成果」与「推行秦式军改」两行的数值。

## 5. 遗留问题

- 宣称按钮 visible 要求热情 ≥25（`nesnd_ottoman_claim_target`），本批不动。
- 原有 `non_interest_group_leader_trigger` 在人物作用域调用集团类型判断（`ideology_bonapartist_valid_trigger`），是原作写法，未改。
- 设置意识形态后引擎是否会因触发器失效把领袖改回，未实机核实。
