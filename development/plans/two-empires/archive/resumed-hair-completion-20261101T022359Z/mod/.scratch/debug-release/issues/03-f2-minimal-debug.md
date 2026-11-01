# F2 最小修复与分类复核

Record: implementation
Category: bug
Status: ready-for-agent
Execution: claimed
Assignee: root
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
- 按最新用户范围核吞并→三日本政权、Lin后续统辖（可任一国摄政）、陈案刺杀→内战进度跃升→战争的真实调用顺序、完成条件与可达性。接受的失国/GAME OVER不作为缺陷，不自动插入救援或新剧情。

## Result

F2已从冻结F1精确复制514文件，并保存pre-change-f2-closure-entry-20261101T002934Z。最小兼容别名使内容hard_errors由1降为0；同步工程文档后的526文件版SHA为416ac54f8fb9f4c4ab1c86266519b517724f9f78a9a396e4579342774fb9353f。其[统一报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/f2-global-20261101-before-player-fix/report.md>)为13 PASS、2 FAIL、2 NOT_RUN；报告保留历史结果，旧玩家续玩阻断须依最新授权重新分类，不改写旧证据。尚未全体验收。

按用户顺序调试要求，后续编辑候选为 `WORK/exports/f2-sequence-debug-20261101-a`，精确父为上述526文件版；修改前独立备份 `pre-change-f2-sequence-entry-20261101T010656Z`。陈案已获得的进度可能被后加入JE的零初始化覆盖，现仅增加“变量不存在”守卫，保留全部原数值/郑钦门槛；[源级反例与修复](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/chen-pressure-initialization-sequence-static.json>)通过，native仍NOT_RUN。Lin摄政实际链路正在同一独立候选中补齐；统一检查和实机结果以后续精确指纹记录为准。

## Comments

F1 中 Japan A1、Lin、字面 scope 修复已合入；旧计划的“待实现/待合并”不代表当前候选仍缺这些代码。用户已接受玩家GAME OVER，玩家确认和日本旧终局独立候选均未选用，不因存在旧断开事件就接回叙事。当前继续F2别名版的真实机制顺序审计。
