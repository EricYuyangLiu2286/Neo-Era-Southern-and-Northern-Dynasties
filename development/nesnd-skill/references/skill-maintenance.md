# 维护本技能

> 何时读：要改本技能或 `nesnd-player-writing` 时。不必读：普通开发任务。

## 什么可以写进技能

- 作者明确提出的长期要求。
- 同一种错误出现两次以上、且有共同原因时，总结成一条规则，附一个正例和一个反例。
- 已在 GAME 源码或游戏中证实的接口事实，注明游戏版本。

单次事故、任务进度、运行编号、测试数量写进仓库 `.scratch/debug-release/issues/` 或 `docs/agents/STATUS.md`，不写进技能。

## 结构

- `SKILL.md` 只做入口：硬规则、通用做法与“任务 → 必读 → 可选”路由表。路由表的任务类型与主 MOD `docs/agents/prompt-kit.md` 一致（修复 / 新内容 / 文字 / 迁移 / 工具 / 分析）。
- `references/` 放做法（怎么设计、调试、交付）；`lookup/` 放查表（接口事实、数值量级、设定、清单）。做法文件里只留支撑规则所需的一两句事实，成段的接口事实放 `lookup/`。
- 每个参考文件在标题下写一行“何时读 / 不必读”。
- 同一条规则只在一个地方写全，其他地方用一句话指向它。“静态检查不等于实机验证”只写在 SKILL.md 硬规则与 verification.md §3。
- 版本事实在 `lookup/engine-facts.md`、`lookup/numeric-facts.md` 标注〔1.15.0 已核〕或〔1.13.11，1.15.0 未复核〕。复核一条就改一条标记。
- 主 MOD 的 `docs/agents/prompt-kit.md` 引用 `references/` 下的 debugging-and-updates.md、content-design.md、migration.md、verification.md；改名时同步修改它。

## 整理与防丢失

大改结构前用 `scripts/backup.py --paths` 备份两个技能目录；改完跑 `python scripts/skill_loss_check.py --old <备份>/skills`。它把旧文件逐段（段落、列表项、表格行）与新内容比对，列出找不到去向的条目；每条要么补回，要么在 [MIGRATION.md](../MIGRATION.md) 的“删除或改写”表里写明理由。

## 篇幅

- `SKILL.md` 不超过约 8 KB（2026-11-11 加入路由表后由约 6 KB 放宽）；单个参考文件尽量不超过约 10 KB。
- 加一条就检查能否删一条或合并一条。规则冲突时保留较新的作者要求，删掉旧的。
- 与版本有关的事实写明版本号（如“1.15.0”）。游戏更新后，先核对这些条目，过时的改写或删除。

## 同步

- 技能本体：`C:/Users/Eric Liu/.codex/skills/nesnd-victoria3` 与 `nesnd-player-writing`。
- 仓库副本：`development/nesnd-skill/` 与 `development/nesnd-player-writing/`。每次修改技能后整体复制到仓库副本并提交，以保留历史。
- 旧版技能（2026-11-06 重写前）在仓库提交 `2643273` 的 `development/` 中。
