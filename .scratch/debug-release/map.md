# DEBUG 收口、版本保存与交付

Record: execution-map
Updated: 2026-11-01

## Destination

依用户已批准的四阶段顺序整理工程入口、建立 F2、完成受影响范围的实际验收，保留最初版本和各阶段成果到私有 GitHub，最后提交可审查的主 MOD 合并清单。

## Notes

- 本轮已获准整理文档/技能、建立独立 F2、修复已确认缺陷、集中实机验收及保存 GitHub 历史。**最终合入主 MOD 仍须用户批准具体清单。**
- 当前为明确授权的执行图；下列子任务是 implementation，不是默认 wayfinder 决策票。
- 领域与工程职责见 [工程适配](../../docs/agents/engineering-skills.md)；任务字段见 [任务约定](../../docs/agents/issue-tracker.md)。
- 详细设计继续使用 [原始范围账](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/12-scope-ledger.md>)和 [批次计划40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)。其中旧进度描述以精确候选及本轮结果为准，不删除原账。
- 主 MOD 已备份为 `pre-change-github-f2-entry-20261101T002814Z`。F1 冻结为 `batch-debug-20261031-f1`；本轮 F2 目标为 `batch-debug-20261101-f2`，实际生成/冻结结果在对应任务记录。

## Tasks

| 任务 | 前置 |
| --- | --- |
| [整理工程入口与交接](issues/01-engineering-docs.md) | 无 |
| [保存原始版本与当前源码](issues/02-github-history.md) | 无 |
| [F2 最小修复与分类复核](issues/03-f2-minimal-debug.md) | 整理工程入口 |
| [集中实机验收](issues/04-engine-validation.md) | F2 候选闭包 |
| [准备交付与主 MOD 合并清单](issues/05-delivery-merge-review.md) | 实机验收、远端保存 |

## Decisions-so-far

- [工程适配](../../docs/agents/engineering-skills.md)：NESND 维护领域约束与验收，Matt 提供工程方法；本地任务跟踪继续保留。
- [F1 合并记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/batch-debug-20261031-f1-merge.json>)：日本 A1（含 Lin）、海域、功能本地化及字面 scope 修复已在 F1，旧“待合入本批”描述不再指当前候选。
- [日本设计与保护条件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/japan-annex-recovery-batch-review.md>)：允许 JAP 被吞并；恢复三政权、人物与第三国保护仍须实测。

## Not yet specified

- 真实吞并后的玩家失国/续玩行为及必要的最小修复，以原生结果决定。
- 实机出现的新差异，只在已授权 DEBUG 范围内补任务与依赖。

## Out of scope

新增剧情、扩大拆州、经济调数和原始范围账中的新设计未因此恢复。已有内容和验收欠账保留；本轮不改本体/工坊文件，也不搬运 EAC 素材。

## Resume evidence

[F1 最终统一报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/f1-global-20261101-final/report.md>)：12 PASS、2 FAIL、3 NOT_RUN，未绑定 F1 引擎运行。旧 PHI/陈案/海域实测仅适用于其原版本与场景。
[完整旧交接存档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/engineering-entry-20261101T002933Z/references/active-work.md>)保留此前运行记录；当前进程/窗口必须重新枚举。
