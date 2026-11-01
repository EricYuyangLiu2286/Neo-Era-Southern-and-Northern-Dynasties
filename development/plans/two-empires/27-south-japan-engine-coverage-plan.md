# 27 — 南朝、日本与朱氏分支实机支持

2026-10-31；依据 map-reference-closure-A（run165620 实载）和其仅UI子版 usm-journal-ui-A。当前自然USM至1836.6.4、首次契约无刷屏是已覆盖小项，不重算为内战或日本完成。

旧 QA routes 三项会写吴胜/settled或虚构反吴资格，不能继续作为真实胜负测试入口。备份活动QA源后隐藏这三个旧选项，保留名字以识别旧报告；不改变冻结run。增加只读当前国家谓词探针和仅在真实 `nesnd_rebel_can_offer_settlement` 为真时请求真实 .10 的入口。后者不写 waiting/opposition/winner，必须由实际JE/战局建立前置。

依赖：真实JE/国家/人物/战争/领土 → 当前scripted_triggers → QA静态debug_log PASS/FAIL → 原生存档/UI核验。无动态ROOT日志、无假胜利旗、无直接annex，不能通过脚本自证战斗结果。

自然与夹具分开：`flavorUSM.4` 是既有实际事件入口，会进行真实禅让及邀请，但跳过压力/寿命；如使用必须留原自然档。日本方案应由真实吴朝结束南方危机后到达准备按钮，或明确独立组件档，不能用置吴胜flag称已满足战后条件。现阶段优先完整实际链，不添加新的假阶段夹具。

短步骤另见 evidence/south-japan-current-engine-sequence.md。CUA本轮因工具报告physical Escape停止，用户此前明确否认按键；不得继续CUA，不推断用户暂停整个项目。下次先重连读屏再决定下一操作。
