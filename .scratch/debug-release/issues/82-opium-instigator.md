# 82 鸦片之战的宣战对象与烟瘾提示

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者内审通过，2026-11-10，游戏 1.15.0，Git main 0dfb25c；原始记录未附）
Evidence: [工作台静态核查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-09-opium-instigator/静态核查.md>)

## 现象与期望

更正反写的胜败提示，把强制禁烟诉求限于实际向本国推广鸦片的国家，并核实烟瘾下限和失败修正期限。

## 原因

原来只保存经历标，未记录生产国。胜败判定读脚本条，两语提示却写反端点。

## 改了什么

推广时在收件国保存发件国，博弈和战争目标共用资格检查；收件时显示发件国。中英文校正两端和卖单门槛。

## 怎么复测

A 对 B 推广，另设有园的 C。B 结案后应只能向仍有园的 A 提出此诉求，追加目标亦同。按游戏外算例，卖单低于 400、经济干预、其余项为零时，烟瘾 25 个月归零。

## 遗留问题

旧档已发生事件且没有来源记录时无法追溯。失败国家修正当前没有自动到期。未启动游戏。

## Comments

2026-11-10：作者内审通过。正文中“未启动游戏”“待复测”等为交付时的状态。
