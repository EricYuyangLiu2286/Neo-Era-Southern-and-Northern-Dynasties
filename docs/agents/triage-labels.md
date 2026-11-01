# Triage Labels

| 技能角色 | 本地 Status | 含义 |
| --- | --- | --- |
| needs-triage | needs-triage | 等待维护者评估 |
| needs-info | needs-info | 等待补充信息 |
| ready-for-agent | ready-for-agent | 规格完整，可交给代理实施 |
| ready-for-human | ready-for-human | 需要人工判断或操作 |
| wontfix | wontfix | 不予实施 |

每个已分诊的 implementation 任务携带一个 `Category: bug|enhancement` 和一个上表状态。实施认领/完成用 `Execution`，证据等级用 `Validation`，具体约定见 [任务跟踪](issue-tracker.md)。

五状态只描述分诊，不代替实施完成或引擎验收。wayfinder 决策记录使用自己的 open/claimed/resolved 状态，不套用本表。
