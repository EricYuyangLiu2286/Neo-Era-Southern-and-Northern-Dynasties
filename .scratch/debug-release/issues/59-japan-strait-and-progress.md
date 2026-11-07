# 59 日本国政条面与海峡彼岸治理

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS，1.15.0 / 26453692，待作者实机复测
Evidence: [三版调查、内容树与复测](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-journals-20261107/调查与复测.md>)、[10 个游戏文件及校验结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-journals-20261107/validation.json>)

## 现象与期望

国政条的四行月变压住方针按钮。选择朝鲜总督后只剩改设议事会，归还领土是唯一可见成功。作者追加授权直接实施两条治理路线，本轮不开游戏。

## 原因

原版 journal_entry.gui:477、484 分别读取周期悬停与条面 desc。任务 52 把零值明细放入 desc。任务 56 前后朝鲜治理日志定义一致；“已达成和解＋两道无地”从 c1463da 就是交还结局。总督、议事会原先只维持修正。

## 改了什么

- 中英 nesnd_japan：国政条恢复一行，名称和数值共用四来源悬停。新增地方条件、阶段、按钮、结局及事件文字。
- journal_entries/nesnd_jp_korea 和 script_values/nesnd_jp_korea：月检单点计数、治理／和解／失地或朝鲜亡国结案。
- scripted_buttons、scripted_triggers、scripted_effects、static_modifiers 中的 nesnd_jp_korea：两地行政、教育目标，十二次月检后的核准、一次性三年州奖励与易主清理。
- events/nesnd_jp_coast：税册定本、学款公议。journal_entries/nesnd_jp_foreign：承接原遣使按钮，治理结案后仍可交涉。
- 日本基本治理继续影响全局重建运动的既有读数。未修改任何 nesnd_kr_restoration 文件。

## 怎么复测

国政先重启读观察者档看未选布局，1840年后切丰臣选方针，悬停在名称或数值，核四项、灰显与第三按钮。朝鲜用1836丰臣新局、选择前分档；总督查每州两级行政半数岗位，议事会查教育两级、当地一所大学半数岗位。官僚非负、所持两道各州由本国控制且动乱低于25%，连续十二次月检，再点结案按钮。

## 遗留问题

悬停命中区、月检次序、三年奖励与重建交接待作者实机验证。本次按所在地基本方针延续、全局运动接案设计，KOR复建但运动未结束时不重开本地里程碑。任务31新政内容另行跟踪。
