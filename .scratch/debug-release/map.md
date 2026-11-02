# 恢复开发、DEBUG、版本保存与交付

Record: execution-map
Updated: 2026-11-01

## Destination

依用户已批准的四阶段顺序整理工程入口、建立 F2、完成受影响范围的实际验收，保留最初版本和各阶段成果到私有 GitHub，最后提交可审查的主 MOD 合并清单。

## Notes

- 用户已进一步授权：先完成原版参考流程、中国女性发型、指定地图细化及 DEBUG 延续，再做完整改革、明吴多结局、编辑器；海外市场退出降低优先级。用户休息期间明确不提问，合理实现选择由代理处理。独立候选、备份、验证和 Git 保存持续执行；2026-11-01最新授权已改为：修复已知BUG、完成必要检查及备份后直接整合主MOD与主Git分支。
- 当前为明确授权的执行图；下列子任务是 implementation，不是默认 wayfinder 决策票。
- 领域与工程职责见 [工程适配](../../docs/agents/engineering-skills.md)；任务字段见 [任务约定](../../docs/agents/issue-tracker.md)。
- 详细设计继续使用 [原始范围账](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/12-scope-ledger.md>)和 [批次计划40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)。其中旧进度描述以精确候选及本轮结果为准，不删除原账。
- 主 MOD 已备份为 `pre-change-github-f2-entry-20261101T002814Z`。F1 冻结为 `batch-debug-20261031-f1`；本轮 F2 目标为 `batch-debug-20261101-f2`，实际生成/冻结结果在对应任务记录。
- 2026-11-01最新范围优先：接受玩家失国/GAME OVER（包括日本），不要求自动保控续玩。F2别名版及sequence A保留为父链；当前运行resumed-integrated-20261101-a（553文件，SHA 1f0c4f79024eb674d60b2d2cbc2b82e2e7fea56673a55caeb78eb2d421d4650d）。玩家确认和日本旧终局两个独立候选仍UNSELECTED，不集成。

## Tasks

| 任务 | 前置 |
| --- | --- |
| [整理工程入口与交接](issues/01-engineering-docs.md) | 无 |
| [保存原始版本与当前源码](issues/02-github-history.md) | 无 |
| [F2 最小修复与分类复核](issues/03-f2-minimal-debug.md) | 整理工程入口 |
| [集中实机验收](issues/04-engine-validation.md) | F2 候选闭包 |
| [准备交付与主 MOD 合并清单](issues/05-delivery-merge-review.md) | 实机验收、远端保存 |
| [原版参考步骤与女性发型](issues/06-source-first-female-hair.md) | 无 |
| [六地区地图细化](issues/07-map-refinement.md) | 无 |
| [原始欠账继续实施](issues/08-original-backlog.md) | 本批 03、04、06、07完成 |

## Decisions-so-far

- [工程适配](../../docs/agents/engineering-skills.md)：NESND 维护领域约束与验收，Matt 提供工程方法；本地任务跟踪继续保留。
- [F1 合并记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/batch-debug-20261031-f1-merge.json>)：日本 A1（含 Lin）、海域、功能本地化及字面 scope 修复已在 F1，旧“待合入本批”描述不再指当前候选。
- [日本设计与保护条件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/japan-annex-recovery-batch-review.md>)：允许 JAP 被吞并；恢复三政权、人物与第三国保护仍须实测。
- [本轮真实运行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/runtime-003815-root-observations.md>)：原生JAP退让后GAME OVER已观察；手动“作为观察者继续”后自然恢复三国。这是可接受失败结果及世界机制证据，不改写为自动续玩。
- 先核实际事件顺序：吞并→恢复三个日本政权；林汉涵后续统辖三个日本属国（可任其中一国摄政）；陈东阳刺杀→内战进度跃升→战争。具体条件和成功/失败证据沿实际源码查证，不自动补救或新造剧情。

## Current checkpoint

- 06原版参考/女性发型：completed / ENGINE_PASS，仅认证A同档牧沐子及女群像复现修复、BOM版综合新局牧沐子复核。主MOD玩法未合入。
- 03、04、07均claimed / ENGINE_PARTIAL：综合新局12受改州和初始化已核，真实退让后三国恢复、Lin摄政显示及原生Mar12重载持久已观察；完整人物/关系审计、陈链、实际市场/航行与其余分支仍待。
- 原始版、主MOD起点、F1/F2和6条新candidate分支已远端保存；[Git报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/git-resumed-candidates-20261101T014406Z/report.json>)的archive核对均逐字一致，综合提交5edbdf6。主分支只保存文档/support更新，不切换游戏部署。
- 最新实际运行与所有偏差见[恢复记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/resumed-runtime-20261101-root-observations.md>)；新局基线和[BOM肖像记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Jan1-new-baseline/mu-muzi-newgame.json>)、[Lin重载记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Mar12-native-Lin-regency/reload-observation.json>)分别限定证明范围。综合global仍为13 PASS、1 FAIL、3 NOT_RUN，不能标整体验收。

## Not yet specified

- 上述三条既定事件链的顺序、守卫、完成结果和可达性仍需源码/引擎证据，尤其Lin后续统辖与陈案推动内战。
- 实机出现的新差异按已授权闭包修复；原始欠账的未定实现从原有计划与原版源码查证。用户已接受失败、稀缺与破产，经济验收只判断开局功能、难度及真正脚本缺陷。

## Out of scope

旧 DEBUG ONLY 限制已被最新明确任务取代。维持原始设定、数据和已验证机制；本体/工坊仍只读，EAC 素材不搬运。自动救援、保证市场永久无稀缺和保证玩家不败均不是目标。

`f2-player-continuation-20261101-a`（SHA `5b8e98246e52f4d8cb160257e18aa9a4f4e8896e8be7473d618ea0ee9632fd5e`）及 `f2-japan-legacy-20261101-a`（SHA `0332f0dcc72f290b7873f2ae61d222c8f215e5e4f428d56db6a97d7e69213018`）保留为未选用备选及历史工作。各自静态通过不表示接受或将要合并；玩家主动离开后的selection锁中断边界仍仅是备选局限。旧“玩家续玩FAIL”不再约束当前交付。

## Resume evidence

[F1 最终统一报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/f1-global-20261101-final/report.md>)：12 PASS、2 FAIL、3 NOT_RUN，未绑定 F1 引擎运行。旧 PHI/陈案/海域实测仅适用于其原版本与场景。
[完整旧交接存档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/engineering-entry-20261101T002933Z/references/active-work.md>)保留此前运行记录；当前进程/窗口必须重新枚举。

旧回合 CUA在Lin夹具操作期间返回“physical Escape”停止信号，故当时停止 UI，Lin 未通过。2026-11-01用户明确 resume 并说明进程关闭，本轮重新枚举进程/窗口后恢复隔离运行；旧窗口与 exec ID 均失效。范围修订前文档保存在[归档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/accepted-failure-20261101T010339Z/manifest.json>)。

## 最新纠正：日志优先收口

进港已正常，停止反复开局/读档/截图。优先修supply按钮预览缺失scope及其他error.log根因，运行外部静态/MCP检查；正式包不含QA覆盖层。已知问题修复与必要检查后直接备份合入。完整规则见技能log-first-delivery.md。原始功能欠账保留，未完成候选不混入本次BUG修复正式包。

## 已整合：日志修复正式包

主MOD已按最新授权备份合入，零文件删除/零冲突，metadata和当前文档保留。供给按钮缺失对象及17处其他清理保护已修；源码23→0，Tiger零新增，MCP4查询通过。正式包无QA覆盖层。详细范围、未新跑引擎及后续功能欠账见WORK/reports/logfix-release-20261101/release-notes.md。此节取代上方旧“主MOD未合入/等待审批”状态；旧阶段记录保留。

## 最新交付：按钮引用保护

[09 按钮修复与用户测试](issues/09-button-reference-guards.md)：完成源码修复和主项目交付，STATIC_PASS，用户自行实机测试；不打开游戏。12个玩法脚本文件修改，53项检查通过，Tiger零新增，MCP四查询通过。该节为当前入口；上方历史进度保留。引用规则集中在技能syntax-and-routing.md。

## Editor rounding 已完成

[10 编辑器舍入修复](issues/10-editor-rounding.md)：正式工具已部署，真实接口外部测试通过；现有12州148建筑组分配正确，主MOD玩法数据未改。未开游戏。

## 最新：南朝反馈修正

[11 南朝立场、文案与危机节奏](issues/11-south-feedback.md)已交付主MOD：HNA战前固定拥明、朝廷无中立/自主、参与国默认钉选、“脆弱的贸易”与日志文风重写。1837下半年起首辅案、1838初保底进入分支、1839初未解决危机推进；陈各结局即时同步两处bar，intro不再清零。STATIC_PASS，未开游戏；完整限制与证据见对应交付记录。

## 最新：战争结算恢复与新政治计划

[12 首都投降与日本崩溃](issues/12-war-collapse.md)完成源码修复和外部检查，主MOD交付；甘肃不改，旧伊犁改西益，襄阳大营提供小幅军事支持。未开游戏。详细范围与静态边界见任务12；前面游戏验收记录只代表各自旧候选。

最新概率与密使要求取代旧HNA/SIH固定明设计，但政治重构尚未实施：[南朝立场与遣使任务图](../south-allegiance/map.md)。当前HNA固定明仍是旧代码行为，不能把计划数字当成已上线配置。

## 最新：中华帝国土改子日志

[13 地权改革子日志](issues/13-cne-subjournals.md)已实施并完成外部核验：土地商品化、国家城市化、22州营产清理，具名拨款确认与政变失败联动。旧进度保留，主日志所有终局统一清理。259项源码检查、Tiger零新增、5项MCP源码查询、两轴复查；ENGINE_NOT_RUN，用户自行测试。南朝新政治计划仍未实施，保留原任务图。


## 最新：信心、原生进度明细与州归属（2026-11-02）

[14 日志入口与帝国人民的信心](issues/14-cne-confidence.md)：修复三个子日志的running自锁并补齐第四个信心日志；1000信心年度消耗/执政恢复/破产，500一次共和起义，0/废君主/原生内战失败；原生明细、少于4州失效及22州失去归属时的按钮/修正清理已完成。STATIC_PASS，未开游戏；详细交付与限制见任务14。任务13的“实现完成”不代表当时子日志曾实机通过，本次以用户反馈补修。
