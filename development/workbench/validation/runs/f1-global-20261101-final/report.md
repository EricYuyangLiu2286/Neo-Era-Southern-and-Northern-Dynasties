# NESND 全局验证报告

候选：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\batch-debug-20261031-f1`
指纹：`3b379906c62a4611513bcf9110ecce429a84c22b48562b920b86f2307f3ebcdb`
游戏：1.13.11 / 24799966
本地编排已完成；总体状态 **FAIL**。未宣称全游戏已验收。

|检查|层次|状态|实际执行|用时秒|证据|
|---|---|---|---|---:|---|
|frozen_toolchain|PROVENANCE|PASS|COMPLETED|0.016|[frozen_toolchain.json](frozen_toolchain.json)|
|source_version|STATIC|PASS|COMPLETED|1.328|[source_version.json](source_version.json)|
|history_production_parser|STATIC|PASS|COMPLETED|2.704|[history_production_parser.json](history_production_parser.json)|
|history_intent_review|SOURCE_REVIEW|PASS|COMPLETED|0.0|[history_intent_review.json](history_intent_review.json)|
|global_production_resources|STATIC|PASS|COMPLETED|0.281|[global_production_resources.json](global_production_resources.json)|
|fixed_population_envelope|STATIC|PASS|COMPLETED|1.704|[fixed_population_envelope.json](fixed_population_envelope.json)|
|dependency_impact_graph|STATIC|PASS|COMPLETED|13.156|[dependency_impact_graph.json](dependency_impact_graph.json)|
|content_localization_resources|STATIC|FAIL|COMPLETED|16.797|[content_localization_resources.json](content_localization_resources.json)|
|global_naval_geometry|STATIC|PASS|COMPLETED|5.766|[global_naval_geometry.json](global_naval_geometry.json)|
|global_transport_regression|STATIC|PASS|COMPLETED|6.64|[global_transport_regression.json](global_transport_regression.json)|
|tiger_classification|STATIC|FAIL|COMPLETED|3.985|[tiger_classification.json](tiger_classification.json)|
|known_semantic_review|SOURCE_REVIEW|NOT_RUN|COMPLETED|0.0|[known_semantic_review.json](known_semantic_review.json)|
|mcp_actual_query|MCP|PASS|COMPLETED|2.797|[mcp_actual_query.json](mcp_actual_query.json)|
|native_batch_probe_evidence|ENGINE_EVIDENCE|NOT_RUN|COMPLETED|0.0|[native_batch_probe_evidence.json](native_batch_probe_evidence.json)|
|runtime_candidate_binding|PROVENANCE|NOT_RUN|COMPLETED|0.0|[runtime_candidate_binding.json](runtime_candidate_binding.json)|
|input_integrity_after|PROVENANCE|PASS|COMPLETED|0.453|[input_integrity_after.json](input_integrity_after.json)|
|tool_integrity_after|PROVENANCE|PASS|COMPLETED|0.0|[tool_integrity_after.json](tool_integrity_after.json)|

## 尚需处理

FAIL：content_localization_resources, tiger_classification
NOT_RUN：known_semantic_review, native_batch_probe_evidence

未知/继承告警不因基线相同自动豁免；已知源码反证与视觉例外各有证据。静态范围、真实MCP协议和原生运行证据分别保存。
下一阶段先修报告中的源码/闭包错误，重跑本入口；之后才在精确冻结候选上实际进入国家、走时并执行所需分支，再收集绑定原生探针。
运行时scope、预览求值、AI、就业/价格、战争胜负、舰队到达及所有故事组合均不能由本检查器模拟认证。
