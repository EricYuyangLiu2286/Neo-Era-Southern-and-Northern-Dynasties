# 本项目开发入口

开始工作前读取 `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/SKILL.md`，按其中的目录路由查证当前游戏源码与实际实例。写功能或修复前，完成该技能“实现前先查原版完整链条”步骤并记录来源。

只有本目录是主 MOD。维多利亚3本体、所有创意工坊 MOD、旧项目与文案/翻译资料均只读。
工具、独立备份、原版基线、地图编辑工程与测试证据放在 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。

不得以“通过静态检查”宣称“游戏内已验证”。版本迁移应保持架空领土、人口、文化与制度意图，不能直接复制原版的新国界或删除不再受支持的设计。

## Agent skills

使用工程技能进行诊断、规划、实现、审查或版本交付前，先读 `docs/agents/engineering-skills.md`。恢复本轮工作时读 `.scratch/debug-release/map.md`。

### Issue tracker

创建、读取或更新任务时，使用本地 Markdown；先读 `docs/agents/issue-tracker.md`。

### Triage labels

分诊任务时，使用五种默认状态名称；先读 `docs/agents/triage-labels.md`。

### Domain docs

探索项目时，按单一领域文档布局读取术语和设计决策；先读 `docs/agents/domain.md`。

当前验证顺序按 [日志优先交付](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/log-first-delivery.md>)：修复日志根因、外部工具/MCP优先，已验证行为不重复开局或读档；正式包排除QA工具。
