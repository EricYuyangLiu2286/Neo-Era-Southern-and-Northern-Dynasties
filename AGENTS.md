# 本项目开发入口

> **开工前检查：每次开始任何工作之前，先做这一步。**
>
> 1. 运行 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-source/deploy.bat check`；或者直接读取 MOD 文件夹和源目录最外层的 `nesnd_deploy_version.txt`，以及源目录 `update_record.json` 的最后一条记录。
> 2. 三个版本号必须一致。
> 3. 不一致时，立即停止一切工作。查阅 `update_record.json`，判断是否有奇怪的误差（例如 MOD 文件夹被直接修改、部署中断、时间顺序异常），向用户发出警告，等用户指示后才能继续。不要自行运行 `deploy.bat force`，也不要手工改版本号或记录。
> 4. `check` 结束时会列出源目录里尚未提交到 Git 的文件，并标出哪些已经在 MOD 文件夹里。其中不属于本任务的，开始工作前先告诉用户有哪些文件；不代为提交，不回退。

## 源目录与 MOD 文件夹

- **源目录**：本文件所在的目录，`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-source`。保存 MOD 全部内容（运行文件、开发资料、.git）的唯一工作位置。所有修改都在这里进行。
- **MOD 文件夹**：文档下 mod 文件夹中本 MOD 的那个文件夹，即 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`。它是部署产物，只包含运行文件和部署版本号，每次部署都会被完全清空后重建，不得直接修改。
- 所有读写都在源目录进行；MOD 文件夹不得直接修改。
- 需要进游戏测试、读取 error.log 对应的部署版本，或者发布之前，先运行部署脚本（`deploy.bat`，用法见技能 `references/tools.md` §4）。
- 报告中提到路径时，写明是源目录还是 MOD 文件夹。

## 提交

部署只复制文件，不提交。2026-11-19 有一批改动部署了、也发布了，却一直没有提交，别的工作从 Git 取文件时就漏掉了它。

- 一项任务做完并部署以后，把本任务改动的文件提交到源目录的 Git，再交付。只提交本任务的文件，提交说明写清做了什么。
- 交付报告里写提交号。有文件没有提交的，写明是哪些、为什么。
- `deploy.bat deploy` 结束时会提醒还有哪些文件没有提交。这段提醒要原样转告用户，不得略去。
- 任务做到一半先部署测试是正常的，这时不必提交；做完再提交。

## 入口

1. 读共用技能 `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/SKILL.md`。技能有自己的 Git 仓库，就是这个文件夹；分工见其中的 `AGENTS.md`。
2. 按任务类型再读对应技能的 `SKILL.md`（都在 `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/skills/` 下），照它列的必读文件做：

   | 任务 | 技能 |
   |---|---|
   | 修复报错、崩溃、玩法缺陷 | `nesnd-fix` |
   | 新建或扩写内容 | `nesnd-new-content` |
   | 玩家文字 | `nesnd-player-writing` |
   | 游戏版本迁移 | `nesnd-migration` |
   | 工具、部署脚本、技能维护 | `nesnd-tools` |
   | 只分析、出报告 | `nesnd-analysis` |

3. 读 `docs/agents/STATUS.md`：当前基线、未完成事项、各目录位置。
4. 在 Codex 中开子代理前，读 `docs/agents/gpt_subagent_usage.md`：何时用、各类任务的模型与强度（上限 `gpt-6-astra` / high，不用 Luna）。

维多利亚3本体、所有创意工坊 MOD、旧项目与文案/翻译资料均只读。工坊 MOD 只用于查兼容接口，不学习、不复制其他作者的设计与代码。

**启动游戏须有用户在当次任务中的明确要求。**“修复”“测试”“继续”或过去的许可都不算。默认在游戏外验证。用户指定观察者五速并保存时，完成这三步就停止，不监看、不轮询日志、不自行重开。

工具、备份、原版基线、地图编辑工程与测试证据放在 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。

静态检查通过不等于游戏内验证。版本迁移保持架空领土、人口、文化与制度意图。

## 任务记录

- 任务用本地 Markdown：`.scratch/<工作>/issues/NN-*.md`，格式见 `docs/agents/issue-tracker.md`，状态名见 `docs/agents/triage-labels.md`。
- 使用 Matt Pocock 工程技能（诊断、规划、审查等）时，先读 `docs/agents/engineering-skills.md`；术语与设计决策布局见 `docs/agents/domain.md`。
