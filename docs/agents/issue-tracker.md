# Issue tracker: Local Markdown

本项目继续使用本地 Markdown 管理任务。GitHub 用于源码与版本保存。目前不自动创建 GitHub Issues、PR 请求队列或外部评论。

## 位置与权威记录

- 每项工作一个目录：`.scratch/<effort>/`。入口为 `map.md`。
- 新规格为 `spec.md`。已有 WORK 规格与计划只建立链接，保留原编号及正文。
- 实施任务分别存放在 `issues/<NN>-<slug>.md`，从 `01` 编号。
- 当前工作入口：[DEBUG 收口与交付](../../.scratch/debug-release/map.md)。
- 已有整体范围和批次要求分别由 [原始范围账](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/12-scope-ledger.md>) 与 [集中修复计划](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)承载。当前进度、差异和新证据从执行索引到具体任务追踪，不复制另一套详细计划。
- 工具、备份、报告、原生日志和存档放 WORK。任务中记录绝对路径、版本/候选 SHA 和覆盖范围。

## 实施任务

顶部字段：

- `Record: implementation`。
- `Category: bug|enhancement`，只选一个。
- `Status:` 使用 [五种分诊状态](triage-labels.md)，只选一个。
- `Execution: open|claimed|blocked|completed|rejected`。认领时先写 `Assignee:`，阻塞时写原因，完成/拒绝时记录结果。
- `Blocked by: NN, NN` 引用本目录任务。`none` 表示无前置。前置完成才解除执行依赖。
- `Validation: NOT_RUN|STATIC_PASS|ENGINE_PARTIAL|ENGINE_PASS|NOT_APPLICABLE`，附 `Evidence:` 链接。

`completed` 仅表示该任务声明的交付与检查完成，不能外推整个 MOD。文档任务可用 `NOT_APPLICABLE` 标明无游戏行为。游戏任务的 `ENGINE_PASS` 必须绑定实际场景、候选 SHA、游戏/依赖版本与原始证据。部分通过用 `ENGINE_PARTIAL` 并列未覆盖项。`ready-for-agent` 只说明可实施。
讨论追加到 `## Comments`，最终交付记入 `## Result`。仅由规划分析产生的 bug 线索，先记未核验，不伪称已复现。

技能要求“发布到任务跟踪器”时按上述位置建文件。要求“获取任务”时按路径或当前 effort 编号读取。使用 triage 技能时保留其 AI 分诊标注及类别/状态要求。

## 篇幅

任务文件是给作者读的，控制在一页以内（约 60 行），顶部字段之后固定五段：

1. 现象与期望（作者原话）
2. 原因（几句话，指到 文件:行）
3. 改了什么（每个文件一句）
4. 怎么复测
5. 遗留问题

日志副本、SHA、解析与检查细节放 WORK/reports/<任务>/，任务文件里只给链接。

## Wayfinding operations

默认 wayfinder 图用于决策。经用户明确授权执行的图可在 Notes 中声明该例外。执行索引中的 implementation 任务与 decision 任务依 `Record` 分开判断。

- 地图：`.scratch/<effort>/map.md`，包含 Destination、Notes、Decisions-so-far、Not yet specified、Out of scope。图只存索引与结论摘要。
- 决策子任务：`issues/NN-<slug>.md`，顶部 `Record: decision`、`Type: research|prototype|grilling|task`。正文 `## Question`。
- 决策状态为 `Status: open|claimed|resolved|closed-out-of-scope`。不使用五种 triage 状态，也不附 implementation 类别。
- 初始 `open` 且 `Assignee: none`。领取前写 `claimed` 和实际代理/人工身份。释放领取恢复 open 并说明原因。
- `Blocked by:` 所列决策全部 resolved 后，从 open、无阻塞、无人认领的子任务按编号选择。
- 解决时追加 `## Answer`、状态改 resolved，并向地图 Decisions-so-far 追加摘要及链接。resolved 表示问题得到回答，不证明实施或游戏验收。
- 移出范围时写 closed-out-of-scope 及原因，将链接放地图 Out of scope。不删除已有记录。
