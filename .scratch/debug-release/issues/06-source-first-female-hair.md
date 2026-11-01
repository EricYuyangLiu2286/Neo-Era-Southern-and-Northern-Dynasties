# 原版参考步骤与中国女性发型

Record: implementation
Category: bug
Status: ready-for-agent
Execution: completed
Assignee: root
Blocked by: none
Validation: ENGINE_PASS
Evidence: [A同人物原生对照与B编码收口](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/female-hair-20261101-b-review.md>)；[A原生绑定](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/female-hair-20261101-a-native.json>)；[B精确manifest](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/female-hair-20261101-b-build.json>)

## Scope

原版调用链记录进入核心步骤；发型按 GAME/EACR gene→modifier→accessory→mesh 实际链定位。独立候选通过静态检查后，使用同一原生牧沐子人物实机前后对照；不复制工坊素材。

## Comments

2026-11-01用户明确授权并要求休息期间不要提问。

## Result

已追到完整链：旧兼容声明把EAC_hairstyles从持久DNA移为special gene，但依赖modifier仍用replace，同时清空原版hairstyles。独立A只将两处special槽调用改为add，原版持久发型仍replace；所有性别类别、模板顺序、文化/宗教/西化/僧侣判定保持，无工坊素材复制，无人物身份修改。

主控实机同档对照通过：run20261101T012826Z的sequence A中，牧沐子原生ID3124无头发；run20261101T013305Z的female-hair A中，完整女性发型和花饰恢复，脸、衣服、年龄、文化宗教与身份保持，乡村民众群像女发也恢复。两局均1836-01-01暂停；实际加载存档SHA一致。GAME1.13.11/build24799966，EACR1.0.4先加载。A SHA为`8794f72ab8dd92a34bbe39e48d39f6f6f2bbf5e1e95a9e1efed5c2ac4f05e156`。

日志增量仅一条新增modifier缺UTF-8 BOM。A保持原样以供复现；新B `WORK/exports/female-hair-20261101-b`仅前置该文件BOM三字节，其余532文件不变，完整有序AST相同；B SHA为`2579d29090c8ee4356fc8172d3b977e2810e566087cbe2fd2714b0658efa1e77`。A与B均有独立checkpoint备份及manifest。

已完成本票范围：原版完整链条已成为AGENTS/SKILL核心实现步骤；A同档复现与修复对照实际通过，BOM版本随后在综合A（553文件、SHA 1f0c4f79024eb674d60b2d2cbc2b82e2e7fea56673a55caeb78eb2d421d4650d）的真实全新局中重新打开牧沐子完整肖像通过，冷加载未新增BOM告警。run20261101T014437Z的[原生绑定记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Jan1-new-baseline/mu-muzi-newgame.json>)和[截图](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Jan1-new-baseline/mu-muzi-newgame.jpg>)为最终窄范围证据。

本票completed/ENGINE_PASS仅覆盖该已复现女性秃发缺陷及上述样本；全肖像、全部帽饰、单MOD回退和整体验收均未由此认证。后续受影响的走时/重载回归归入任务04，主MOD玩法仍未合入。
