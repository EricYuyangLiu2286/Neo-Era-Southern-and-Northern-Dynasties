# 79 东洋之议与吴日外交博弈

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [静态核验、开局人口模板算例及 11 个玩法文件指纹](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-08-eastern-question/static.json>) · [检查脚本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-08-eastern-question/verify.py>) · [Tiger 原始输出](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-08-eastern-question/tiger.txt>)

## 现象与期望

作者实测日志多出“远征条件 0/0”，外交博弈可招来列强，战争目标选择器缺字。要求吴日开战前仍可退让，日志须区分失败、失效和原有和平结案。

## 原因

- 原作标签 `original-20261030` 有丰臣幕府与靖难的背景，没有这套日志、博弈类型和战争目标。`ece3f9f` 把旧条的 `current_value / goal_add_value` 换为脚本条，留下中英 `nesnd_wu_eastern_question_progress`。原版 journal_entry.gui:761 按非空 GetProgressDesc 显示旧读数。没有游戏效果写入 0/0。
- 真条 `nesnd_eastern_readiness_bar` 开启时取财政、陆军、海军计分，每周用当前分与条值的差更新，范围 0 至 3。删除两个旧文本键没有移除计分、按钮条件或任何脚本写入者。
- 旧创建效果未设置激化值。原版印度起义以 80 起步，原版 defines 在 80 关闭正常加入和拉拢，100 开战。旧月度脉冲把日本消失及未分封的结案合并报作完成。战争目标原有实例名与悬停文案，缺少类型选择器的两键。

## 改了什么

- `common/journal_entries/nesnd_japan.txt` 分列吴国失败、日本降服、普通完成、失效及 3650 天超时。原有和平交涉及未分封的无胜负结局保留。
- `events/nesnd_japan_events.txt` 日方明确拒绝就脱离吴、当场发起博弈；日方提出反案才交吴选择。新增吴国 .6 与日本 .7 结案通知。
- `common/scripted_effects/nesnd_japan.txt` 创建博弈时设激化 80，固定日方羞辱的对象为 USM。失败一次性发奖并将符合条件的整组人口迁往吴都。
- `common/diplomatic_plays/nesnd_japan.txt` 关闭换边，记录该场战争结束。作者截图实测吴方主要要求为空、日方羞辱正常。现由创建效果逐项写入吴对日的“重组日本诸藩”和日对吴的“羞辱大吴”，两项均设 primary_demand = yes。
- `common/on_actions/nesnd_eastern_question.txt` 按专属博弈识别吴退让、吴战败及日对吴执行羞辱，日本在日志中重新臣属即判日方落败，在 JAP 作用域直接执行既有解体效果。分封所需领土暂不具备时，按月复核。
- `common/scripted_triggers/nesnd_japan.txt` 复用东征四岛十州范围，判定对手存续、目标执行资格和中华传承。
- `common/war_goal_types/nesnd_japan.txt` 阻止已经结案的东征在迟来的和约中再分封。`common/scripted_buttons/nesnd_japan.txt` 避免在对手已失效时抢先保留现状。
- `common/static_modifiers/nesnd_crisis_modifiers.txt` 日本威望和行政力各 +10%，每个国内利益集团支持度 +5，均持续 30 年。团结度另由失败效果一次 +25，上限 100。
- `localization/{simp_chinese,english}/replace/nesnd_japan_l_*.yml` 删除旧读数，补选择器类型名和描述、失败与失效说明、两国事件及修正名称。

## 怎么复测

1. 完整验收用新开局。重启后也可用尚未开启日志的旧档缩短流程；对已生成的博弈，创建参数不会重算。已结案和已经招入的援国没有迁移脚本。
2. 吴国完成南方事务后看日志，只显示一条远征条件。低于 2/3 时仍可送国书。日本选择拒绝后当场独立并进入倒计时；选择另议时，吴主动出兵仍查 2/3 及陆海投射。
3. 核两项主要要求、第三国加入／拉拢按钮和正式参战名单，属国自动支持已由作者确认。选择器用吴对 JAP 且允许添加目标的博弈检查类型名称、描述；已经挂上的主要要求可能不会再列为可选。
4. 分档测试吴退让、战败、接受羞辱、开启十年仍未解决。各看两国通知、国家修正、每个利益集团和团结条。开局朝贡关系可继续交涉。日本重新臣属应见日方落败、三家分封、原有结案事件及《天下之归》，且不应发吴国失败奖励。日本亡国或被吞并则失效。另查日本接受分封或吴选择维持现状的和平路径。
5. 失败结算前后比较 JAP 自有的本州、北海道、九州和四国十个州区的中华传承人口，以及吴都的接收量；排除朝鲜、库页岛和琉球。整组迁移按人数逼近一成。用开局建群模板算得 431,002 人中迁 42,802 人（9.93%），实机人口会进一步拆分。

## 遗留问题

- 按作者确认仅用原版 80 起步。作者截图已确认倒计时、日方主要要求和吴属国自动支持，修正后的吴方主要要求待重新创建博弈复测。本次没有启动游戏。Tiger 1.19.0 面向游戏 1.13.5，涉及上述文件的报项只剩原版 1.15 明载的 activation_description 与 outcome。
- 范围外的《天下之归》仍有读取旧分子、分母的“核心地区”本地化，可能出现同类显示问题，未改。
