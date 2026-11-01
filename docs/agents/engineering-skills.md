# 工程技能适配

在 NESND 使用 Matt Pocock 的诊断、规格、任务拆分、实现、审查或研究技能前读取本页。当前用户要求决定范围和授权；NESND 技能提供游戏领域约束，Matt 技能提供工程方法。

## 职责与资料入口

| 工作 | 入口与适配 |
| --- | --- |
| 当前游戏语法、scope、地图/历史/人物/制度、原设计保护 | [NESND 技能](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/SKILL.md>)；先核本机源码与版本 |
| 诊断与回归 | `diagnosing-bugs`；采用下述双层反馈，不把 Python 模型当游戏执行 |
| 规格、任务、领域术语 | 使用当前已安装的 `domain-modeling`，规格与拆分按本地任务约定实施；依 [任务约定](issue-tracker.md) 引用已有 WORK 计划 |
| 审查 | `code-review` 的 Standards 与 Spec 两轴；每项都绑定实际差异和依据 |
| 工具与解析器 | `tdd`、`codebase-design`；已有真实失败样本和可执行接口时应用 |
| 文档与技能 | `writing-for-agents`；可维护规则放项目文档或 NESND 技能，保留插件缓存原样 |
| 资料研究 | `research`；本机当前源码、引擎文档为首选原始来源，研究成果放 WORK |

WORK 为 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。工具、独立备份、基线、地图工程和测试证据遵循 [目录路由](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/paths.md>)，不因通用技能默认目录而搬进 MOD。
任务索引存项目 `.scratch/`，详细设计及已有证据保留原路径与编号。术语表和 ADR 依 [领域文档约定](domain.md) 按实际决策建立。

## 版本与审查对象

每次明确主 MOD、编辑候选、冻结运行副本、测试存档四个对象及指纹，遵循 [增量编辑](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/incremental-editing.md>)。
GitHub 源码保存目标为 [私有仓库](https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties)，本地源码仓库为 `WORK/projects/nesnd-repository`；GitHub Issues 尚未替代本地任务跟踪。Git命令在该工作副本执行；主MOD是独立加载目录，不把Git元数据混入MOD快照。

已有真实 Git 历史时使用明确提交/分支做审查基点；尚无 Git 历史的快照用共同父候选和逐文件 SHA 差异，报告为快照审查。不要伪造提交、工作树或 merge-base。
候选合并使用 [现有三方差分流程](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/incremental-editing.md>)，先核父版本。冻结 F1 早于工程配置，整包镜像会回退 AGENTS 和删除 `docs/agents/`；合入时保留目标目录已有文档和后续工作。
Git 保存、候选生成、实机验收和主 MOD 合入分别记录。用户要求先审合并清单时，最后一次批准针对具体候选、差异及验收结果；已授权阶段不反复请求同一许可。

## 双层反馈与完成标准

1. 本地反馈：保序解析、真实失败样本、引用/资源/人口/地图检查、Tiger 分类及实际 MCP 查询。工具回归可逐项 red/green。
2. 引擎反馈：冻结候选后集中走真实菜单、选择、自然时序、战争/航行和存读档；用原生日志及存档核结果。步骤见 [游戏验证](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/validation.md>)。

游戏不能秒级、无头或单命令复现时，保留最小真实场景与观察入口，先查当前源码及已存失败证据，再安排集中引擎运行。不得用替身模型满足通用技能的测试门槛。同一失败信号前后对应同一行为；UI预览和自然运行分列。
复用通过证据须核源 SHA、游戏版本、依赖、场景和受影响闭包；`STATIC_PASS`、`ENGINE_PARTIAL`、`ENGINE_PASS`含义见任务约定，进游戏或日志未新增均不独立等于验收。
采用 [备份与发布](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/backup-release.md>) 的 pre-change/candidate/checkpoint/accepted 状态；只有实际通过的覆盖范围才能写入验收记录。

## Jomini 审查边界

重复键、scope 链和跨数据库文件有引擎语义。代码气味只作问题线索，不据此合并 `create_pop`、`option`、`modifier` 等有效重复块，也不为套用 OO/API/schema/CI 术语改造游戏脚本。
审查分别回答：是否保留本项目硬约束；是否满足已批准设计和具体玩家行为。原版同形是来源证据，仍需区分工具差距、继承缺陷与未核验接口；不以全局忽略或改动经济权重清空告警。
当前开发范围、未完成项和实际授权以 [执行索引](../../.scratch/debug-release/map.md) 为准；旧设定与计划仍在其原有资料中。

失败结果按用户已确认的设计判定。2026-11-01用户明确接受包括日本在内的玩家失国/GAME OVER；它不再是当前发布缺陷，也不自动授权续玩救援、强制转国或新剧情。调试重点是事件顺序、条件下可达的既定目标，以及难度和玩家行动空间的实际证据；设计已明确时直接查证实施，减少重复设计追问。

2026-11-01最新授权：按 [日志优先交付](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/log-first-delivery.md>)收口按钮报错，复用既有实测，正式包排除QA。已知问题修复并完成必要检查、独立备份后直接合入主MOD与主Git分支；此授权取代本轮此前的最终合并再次审批。
