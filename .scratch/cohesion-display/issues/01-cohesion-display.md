# 01　文化团结度日志：显示下次转化，写技能范例

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude (Opus 5.5)
Blocked by: none
Validation: STATIC_PASS
Evidence: [清点与方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-cohesion-journals/round1.md>)；同目录 `verify.py`／`verify.json`、`tiger/tiger-delta.json`、`audit.json`、`content_tree_vars.txt`；备份 `WORK/backups/pre-change-cohesion-display-20261112T233440Z`；Git 分支 `feat/cohesion-journal-preview` 提交 `d30cc0d`（基于 origin/main `d8fabf8`，只含本任务改动）

## 1. 现象与期望

作者：让玩家在日志上看到每次文化转化的时间、位置、规模和方向；写法总结进技能。不改转化规则和数值，规则 bug 列出来问。作者选 A（只加显示），同意处理 B1–B3，时间写“下次月结”（周计数耗性能，否决）。

## 2. 原因

三个日志：日本「国民团结」、西秦「帝国的稳定」、唐衣大食「唐人同心」。日本、西秦已预选州，但不显示人数与方向，西秦的目标文化到事件时才抽。唐衣大食完全不预选。日本转化里还有 `culture = scope:`／`prev.var:` 比较，与任务 38 刷 1 万条报错的写法相同（B1）。

## 3. 改了什么

- 日本：`scripted_effects/nesnd_jp_development.txt` 执行改为按目标文化分支、直接写 `cu:` 键（B1）；`scripted_triggers/nesnd_jp_development.txt` 有效性条件同样改写；`script_values/nesnd_jp_development.txt` 加 `nesnd_jp_next_size`；`journal_entries/nesnd_jp_cohesion.txt` 第二段状态行分 6 种情况。
- 西秦：`scripted_effects/nesnd_qe1_identity.txt` 预选时抽定文化与宗教并存变量，月结把它们交给事件（B3）；`events/nesnd_qe1_identity.txt` 用预选结果，旧档缺项时当场抽；`script_values/nesnd_qe1_identity.txt` 加 `nesnd_qe1_next_size`；日志状态行 7 种情况。
- 唐衣大食：`scripted_effects/nesnd_per_faith.txt` 低档改为上月末掷 15% 并存州与伊朗文化，下月执行（B2），高档照旧；`scripted_triggers/nesnd_per_faith.txt` 加 `nesnd_per_unity_plan_valid`；`script_values/nesnd_per_faith.txt` 加 4 个人数值；`events/nesnd_per_faith.txt` 事件 1 用预选文化；日志加第二段状态行 9 种情况，冻结或关闭时清预告。
- `on_actions/nesnd_unity_policies.txt` 兜底清理加唐衣大食。
- 本地化：`nesnd_japan_l_*`、`nesnd_qin_politics_l_*`、`nesnd_per_faith_l_*` 中英各改／增 6、7、9 键。
- 统一结束（2026-11-13，作者选身份证件）：`scripted_triggers/nesnd_unity_policies.txt` 加三个条件；三个日志各加“研究身份证件”“采用委员会共和国或法团国家”两个蓝色结局，写永久标记 `nesnd_cohesion_fixed`；`possible`、未激活显示、日本与西秦的补加入口排除已结束的国家；`nesnd_journal_closures_l_*` 中英各加 2 条结语。
- 补贴随日志停止（2026-11-14，作者要求）：`scripted_effects/nesnd_unity_policies.txt` 加 `nesnd_unity_stop_subsidies`，日本、西秦的全部结局调用，撤销补贴修正与期限变量。补贴按周计入开支，没有预付款，撤销即不再支出。奥斯曼、印度日志仍在用同一按钮时不撤。两个补贴按钮加一行提示，中英各 1 键。
- 技能：新增 `references/cohesion-journal.md`，SKILL.md §5 加一行，journal-state.md、journal-display.md 各一句指向，已同步 `development/nesnd-skill/`。

## 4. 怎么复测

可读档。日本状态行立即可见；西秦读档前已抽定的州显示“届时按当地原有人口抽定”，最多一个月；唐衣大食要过一次月结才有预选。看日志第二段“下次月结：州、约 N 人、A → B”，推进到月结后对照该州人口文化、西秦和唐衣大食的事件。

结束条件：先在日本或西秦点一项团结补贴，再用 `conclude_journal_entry nesnd_jp_cohesion 0`（科技结局；`1` 为政体结局，西秦为 `nesnd_qe1_unity_journal`）。看结语是否对应、补贴修正与开支是否消失、西秦「羌种暴动」是否随之结束，此后日志不再出现。自然研究到身份证件时应自动结束。

## 5. 遗留问题

- `GetReligion` 在 `Var()` 上的显示、`ScriptValue(...)|D` 的格式未实机看过。
- 唐衣大食低档事件比原先晚一个月出现。高档不受影响。
- 顺带发现：`journal_entries/nesnd_acw_slavery_question.txt:379` 也有 `culture = scope:` 比较，不在本任务范围。
