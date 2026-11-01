# F2 最小修复与分类复核

Record: implementation
Category: bug
Status: ready-for-agent
Execution: claimed
Assignee: root/f2_gate_review
Blocked by: 01
Validation: NOT_RUN
Evidence: pending

## Scope

从不可变 F1 建立独立 `WORK/exports/batch-debug-20261101-f2`，处理已确认的最小缺陷并复核过期诊断。细节依据 [计划40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)、[F1报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/f1-global-20261101-final/report.md>)和 [源码分类](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/tiger-e1-eac-exact-source-review.md>)。

## Acceptance

- 原版 `concept_geogregions` 缺引用只通过 MOD 独立兼容入口处理，本体只读。
- Tiger 原版枚举/target_region、波兰缩进和原版 AI 空块逐项依据分类，不修改经济或外交数值清报错。
- 26处人物 ig 调用保持“兼容性待证”，没有原生证据前不批量改写。
- 更新具体语义审查的来源 SHA 与结论，不用重设基线自动清除旧 FAIL。
- 保留地图、历史人口、所有权、既有设计与新工程配置；差分和检查绑定最终候选。
- 运行统一检查，完整记录 PASS/FAIL/NOT_RUN；进入引擎前明确冻结版本及场景矩阵。

## Result

F2已从冻结F1精确复制514文件，并保存pre-change-f2-closure-entry-20261101T002934Z。内容检查已复现原版concept_geogregions缺键，最小兼容别名后hard_errors由1降为0；分类、玩家续玩调用链与最终统一检查仍在进行。此结果不等于引擎通过。

## Comments

F1 中 Japan A1、Lin、字面 scope 修复已合入；旧计划的“待实现/待合并”不代表当前候选仍缺这些代码。玩家续玩及日本部分旧失败/退出路径仍待闭合。
