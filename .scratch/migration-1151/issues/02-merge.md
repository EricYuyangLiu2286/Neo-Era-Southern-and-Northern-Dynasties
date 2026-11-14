# 02 · 合入 Victoria 3 1.15.1 热修

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Assignee: Codex  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [逐项交付和检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-1151-migration/delivery.md>)

## 现象与期望

作者确认按复查清单合并，只处理原版覆盖导致的热修差异。

## 原因

1.15.1 的 21 个同路径源文件发生变化，另有异文件日志覆盖和五个已由原版补齐的简中键。

## 改了什么

P01–P12 共 24 个文件更新、1 个简中补丁撤下。逐项文件见交付表。同步了技能的两份副本及 STATUS 版本。补丁前指纹与备份留在工作台。

## 怎么复测

旧档副本可检查实际激活七法之一后的民族之春变量，以及继位和宠臣回调。新开局检查拆州铜矿、车里雅宾斯克和乌拉尔的开局人口、建筑与归属。

## 遗留问题

实机待作者复测。audit.py 的 138 条既存提示逐条相同。主 MOD 的 supported_game_version 已补齐为 1.15.1，并与本机游戏版本核对。
