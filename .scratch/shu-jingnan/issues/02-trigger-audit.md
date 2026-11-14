# 02 蜀国事件链、触发条件与大汉国旗

Record: decision
Type: research
Status: resolved
Assignee: Codex
Blocked by: none

## Question

用 v3tree 核查蜀国的事件链与触发完整性，判断“明旗汉国号”是否需要配新旗。

## Answer

六个新增事件均有实际调用。大汉称帝共用 USM 和同一大汉变量，国名读取它，旗规缺对应分支；刘、魏两线可共用一旗。游戏脚本与素材未改动。

核实了成都迎立朱氏后政变或投降的朝廷身份冲突、蜀胜复明后仍可能重复重建、吴方维持现状漏授统一资格，以及战败与执政选择的先后条件不一致。投降还会交出开局五州之外取得的领土。

[逐项报告与复测场景](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-shu-trigger-audit/audit.md>) · [v3tree 内容树](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-shu-trigger-audit/cases/shu/map.html>)。游戏版本 1.15.1 / 26591675，限游戏外核查。
