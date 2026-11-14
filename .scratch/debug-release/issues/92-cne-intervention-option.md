# 92 「伪朝禅代」南下选项

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（1.15.1）
Evidence: [Toolkit 检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-cne-usurpation/option-checks/toolkit-checks.json>)

## 现象与期望

属国北朝可以选择准备南下并承担支出，参战效果却要求独立。作者要求保留灰色选项，用红字说明原因，并提示南朝可能没有内战。

## 原因

事件第三项的可选条件漏了征召脚本已有的独立要求。

## 改了什么

`events/nesnd_crisis_events.txt` 第三项增加独立条件，属国时显示禁选项，属国分支只提供悬停文字。中英 `nesnd_crisis_l_*.yml` 增加禁选原因和准备落空两条提示。

## 怎么复测

在事件弹出前分别以独立北朝和属国北朝读档。属国应能悬停第三项读到红字，但无法点选。独立国符合其他条件时可以选择，两种状态都应显示内战可能不发生的提示。

## 遗留问题

三文件 Toolkit 零诊断。已逐项比对改前改后独立国的征召、失序和支出效果。悬停实际排版待作者复测。
