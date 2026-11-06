# 本项目开发入口

1. 读技能 `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/SKILL.md`（仓库副本：`development/nesnd-skill/SKILL.md`）。写玩家文字时另读 `nesnd-player-writing`。
2. 读 `docs/agents/STATUS.md`：当前基线、未完成事项、各目录位置。
3. 写任务提示词的模板和“提示词会话”开场白见 `docs/agents/prompt-kit.md`。
4. 在 Codex 中开子代理前，读 `docs/agents/gpt_subagent_usage.md`：何时用、各类任务的模型与强度（上限 `gpt-6-astra` / high，不用 Luna）。

只有本目录是主 MOD。维多利亚3本体、所有创意工坊 MOD、旧项目与文案/翻译资料均只读。工坊 MOD 只用于查兼容接口，不学习、不复制其他作者的设计与代码。

**启动游戏须有用户在当次任务中的明确要求。**“修复”“测试”“继续”或过去的许可都不算。默认在游戏外验证。用户指定观察者五速并保存时，完成这三步就停止，不监看、不轮询日志、不自行重开。

工具、备份、原版基线、地图编辑工程与测试证据放在 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。

静态检查通过不等于游戏内验证。版本迁移保持架空领土、人口、文化与制度意图。

## 任务记录

- 任务用本地 Markdown：`.scratch/<工作>/issues/NN-*.md`，格式见 `docs/agents/issue-tracker.md`，状态名见 `docs/agents/triage-labels.md`。
- 使用 Matt Pocock 工程技能（诊断、规划、审查等）时，先读 `docs/agents/engineering-skills.md`；术语与设计决策布局见 `docs/agents/domain.md`。
