# 76 商路筹备按钮条件提示

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [条件等价与中英文检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-supply-button-tooltips/static.json>) · [Toolkit](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-supply-button-tooltips/toolkit-checks.json>)

## 现象与期望
「货源与生计」界面的遣使按钮反复显示「国家没有相关变量」。每项可用条件应能让玩家知道要等什么或先办理哪件事。

## 原因
六个遣使按钮公开了待复请求、现有联络伙伴和派使间隔三个变量，并显示了只限制 AI 的选项。自行往来、条约和结案按钮也直接或经共用条件展开内部判断。

## 改了什么
- common/scripted_buttons/nesnd_supply_buttons.txt 与 common/scripted_triggers/nesnd_supply_triggers.txt：六个遣使目的地共用三个具名条件，AI 专用分支与劳动力统计初始化归入隐藏条件。自行往来、条约联络、条约提议间隔、商贸安排以及连续十二周的要求各按实际含义显示。国家、和平、影响力与条约许可仍由原生条件展示。
- 简中、英文 nesnd_supply 本地化各新增八键。两份日志共用十三个按钮；去掉显示包装并展开派使条件后，与修改前的脚本逻辑一致。

## 怎么复测
悬停「遣使蜀王藩」，分别查看商使待复、现有联络伙伴及距上次派使六个月三行。派使后查看各行勾叉；已有伙伴时查看「商议互惠贸易条约」，并检查「由商人自行往来」和结案按钮。

## 遗留问题
未启动游戏。中文与英文实际悬停排版、条件勾叉待作者复测。
