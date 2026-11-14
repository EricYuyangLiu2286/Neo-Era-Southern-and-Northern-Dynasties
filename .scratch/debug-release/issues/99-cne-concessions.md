Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-14）
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-cne-concessions-20261114T121946Z/`；报告 `nesnd-workbench/reports/2026-11-14-cne-concessions/`（report.md 含修正核对表与 AI 概率表，verify.py，tiger/，toolkit/，near_summary.txt）

# 99 地权革命：战争胜利、再次击败共和主义者、做出让步

## 1. 现象与期望

作者要求三项：任意战争胜利信心 +50，可多次。击败信心低于 500 时出现的共和军后触发事件「再次击败共和主义者」：进度 +25，地方失序 −20（作者追加），信心 +50，并获得「迅速而果决的清洗」5 年。信心日志加按钮「做出让步」，按宠臣集团给 10 年修正，冷却 6 个月。改革完成时若有让步修正，奖励换成减半的「不完全的改革」与「元老政治」，各 30 年。

## 2. 原因

新内容。此前信心没有战争胜利一项（`scripted_progress_bars/nesnd_cne_confidence.txt` 全部来源）。共和军每局只出现一次（`nesnd_cne_republican_rose` 从不清除），击败有两条互斥路径：镇压目标被执行（`war_goal_types/nesnd_cne_republic.txt:62`），或停战后共和军日志失败结局吞并（`scripted_effects/nesnd_cne_republic.txt:147`）。宠臣日志接口：`nesnd_palace_journal`、`nesnd_power_holder_ig`、`nesnd_power_balance`（0–100，高为宠臣一方）。

## 3. 改了什么

- `common/on_actions/nesnd_cne_confidence.txt`：`on_wargoal_enforced` 中 root 为执行者且是 CNE 时，非共和军战争信心 +50（同一次和约只计一次）。共和军战争转入平叛事件。
- `common/scripted_effects/nesnd_cne_confidence.txt`：新增 `nesnd_cne_republicans_defeated`、`nesnd_cne_concession_balance`、`nesnd_cne_concession_modifier`。
- `common/scripted_effects/nesnd_cne_republic.txt`：停战路径改调 `nesnd_cne_republicans_defeated`，不再弹 `.4`。
- `events/nesnd_cne_confidence.txt`：新增 `.7`「再次击败共和主义者」，删去 `.4`「共和军归降」。
- `common/scripted_buttons/nesnd_cne_concession.txt`（新）、`common/journal_entries/nesnd_cne_confidence.txt`：按钮「做出让步」，原生 `cooldown = { months = 6 }`。
- `common/scripted_triggers/nesnd_cne_confidence.txt`：`nesnd_cne_has_concession`。
- 2026-11-14 玩家反馈按钮“过一阵就没了”（实为换宠臣后要等宠臣日志的周更新才认定）。作者定：地权革命进行期间按钮始终显示，宠臣条件不满足时变灰，逐项列出“宫廷力量进行中”“宫中有宠臣”“宠臣属于三集团之一（显示当前所属）”。按钮说明补写了周更新的延迟。同日追加：信心已满 1000 时按钮变灰，写明“信心未满”（开局信心为满值，+150 会被截掉）。按钮说明与条件提示改用函数显示本国三个集团的名称（`GetInterestGroupOfType`）、当前宠臣及其集团、权力平衡的名称与宠臣一方（新文件 `customizable_localization/nesnd_cne_concession.txt` 兜底无宠臣的情形）。
- `common/static_modifiers/nesnd_cne_concessions.txt`（新）：7 个修正。
- `common/scripted_effects/nesnd_crisis_effects.txt`、`events/flavorCNE_ce.txt`：完成时记 `nesnd_cne_reform_conceded`，flavorCNE.3 与「及时确权」按它分支。
- 中英 `nesnd_cne_land_reform_l_*.yml`：21 键，名词解释加三项一次性变化。`.4` 的 8 键退役，归档至 `nesnd-player-writing/resources/unused_localisations/2026-11-14-cne-concessions/`。
- `common/war_goal_types/nesnd_cne_republic.txt` 与中英 `nesnd_cne_confidence_l_*.yml`：作者 2026-11-14 定，去掉镇压目标原有的进度 +15、失败条 −20 及其说明。两条击败路径都只由 `.7` 结算：进度 +25，地方失序 −20（后者作者同日追加）。
- 宠臣日志的文件未改。

## 4. 怎么复测

读档即可（按钮挂在已有日志类型上，on_action 与修正都是新定义）。1.15.1 控制台没有 `effect`，信心无法直接设值，见报告 §5。

1. 平叛：`event nesnd_cne_confidence.7` 看文字、进度、信心与修正。完整路径要等信心降到 500 以下出共和军，再打赢（目标被执行）或停战（帝国未被羞辱），两条都应弹 `.7` 一次。
2. 战争胜利：与他国开战并在和约中执行本国至少一个目标，信心条 +50。一次和约多个目标只加一次。
3. 让步：在人物界面任命地主、军队、实业家集团的宠臣各一次，等一周（宠臣日志每周认定宠臣集团），点「做出让步」。不合格集团的宠臣或没有宠臣时，按钮应为灰色并列出原因与当前所属集团。合格时看平衡 +25、信心 +150、对应修正 10 年、按钮显示“冷却至某日”。同类再点重新计时。
4. 完成替换：让步修正生效期间完成改革，看 flavorCNE.3 选项悬停是「不完全的改革」「元老政治」各 30 年。速成条件满足时另有「不完全的改革：及时确权」。

## 5. 遗留问题

- 全部未实机验证：`scope:actor` 是否等于 root、`on_wargoal_enforced` 在吞并共和军的同一结算中能否读到博弈类型、原生冷却的 AI 行为、AI 评估按钮的频率。
- 原完成奖励「投资狂热」写作 `months = long_modifier_time`（3650，即约 304 年），作者原作如此，未改。
- flavorCNE.3 正文仍是全胜的叙述，让步完成时只换了修正。
