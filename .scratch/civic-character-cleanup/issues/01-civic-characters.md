# 01 公民路线人物事件

Record: implementation  
Category: bug  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付、文件清单、复测命令](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-character-audit/implementation/交付与复测.md>)

## 现象与期望

「债契与求学」点名沈季川，选项可能只有一句表态。作者确认按 15 组删除、2 组合并、1 组改造实施，由作者复测。

## 原因

旧链把姓名写入正文，人物能否生成与开场是两个条件。用全国集团好感和 90 天后的单选回访承载了 18 个人物。

## 改了什么

撤去 17 个拟名人物与 35 个旧事件。承包归道路合同，识字归废奴后的地方选择。保留段敬川作为川中政治家，由南朝任用或由独立西府决定两国书院交流。脚本与双语清单见上方交付。

## 怎么复测

用 1.15.1 新开局。东洲看特许承包与废奴事件。1840 年后在有四川大学的一方看段敬川，分别测试南朝任用及独立西府交流。控制台命令和三类收益见交付表。

## 遗留问题

未实机验证。全库审计与修改前相比没有新增项。旧档已生成的人物及排队事件不作迁移。
