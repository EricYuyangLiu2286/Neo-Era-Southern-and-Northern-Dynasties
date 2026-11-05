# 四项日志与南明停战修复

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（引擎待用户测试）
Evidence: [journal-war-feedback-20261103](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/journal-war-feedback-20261103/spec.md>)

## Result

东洋−1是相对基线错误。德里学校已在1851存档中活跃，修子条显示/暂停及市场国家引用。HUS开局废君源于原生政体初始化，定点限制入口与清退旧JE。南朝争端独立于单轮war，行在占领后先迁逃再吞并。本土参战国和平时每轮一次选择再战、求北朝保护、归吴。AI及例外详见spec与runtime-findings。两轴复审、定向回归、AST故障注入、MCP、Tiger差分与数据图保护结果见同目录final-validation.json。

未更改地图、人口、国家历史和已验证日本三分。未开游戏。候选独立备份及合入与远端结果分别见candidate-backup.json、main-merge.json、git-delivery.json。旧HUS短暂君主历史无法可靠倒推。旧war领袖不做未经证实的引擎替换。
