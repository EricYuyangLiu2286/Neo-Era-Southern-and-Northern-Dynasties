Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [工作台审核报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/text-audit-20261107/report.md>)

# 上轮审核后的本地化

## 现象与期望

逐份审核任务 68 后改过的 nesnd_ 文件，直接修技术错误、中文八股、描述剧透和机械性。波斯由外部代理复核。

## 原因

部分旧提示已被新脚本取代。日本外交按钮在发函前就宣布结果；印度与法国少数提示给出的适用条件比脚本更窄或更宽。

## 改了什么

法国宫廷、印度、日本、共用日志结案四对中英文文件合计 121 处。脚本与逐键记录均在报告同目录。波斯专档与共用文件中的波斯键由外审接手。

## 怎么复测

先看「东洋交涉」「国政之争」「天竺的土地」「宫廷与外省」。具体触发场景与预期见报告末节。

## 遗留问题

报告列出三个需脚本处理的界面问题、三个未确认使用方式的战争目标键，以及英文待同步键。本轮未启动游戏。
