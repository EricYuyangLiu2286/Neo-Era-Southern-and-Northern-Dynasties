# 维护本技能

## 什么可以写进技能

- 作者明确提出的长期要求。
- 同一种错误出现两次以上、且有共同原因时，总结成一条规则，附一个正例和一个反例。
- 已在 GAME 源码或游戏中证实的接口事实，注明游戏版本。

单次事故、任务进度、运行编号、测试数量写进仓库 `.scratch/debug-release/issues/` 或 `docs/agents/STATUS.md`，不写进技能。

## 篇幅

- `SKILL.md` 不超过约 6 KB；单个参考文件尽量不超过约 10 KB。
- 加一条就检查能否删一条或合并一条。规则冲突时保留较新的作者要求，删掉旧的。
- 与版本有关的事实写明版本号（如“1.15.0”）。游戏更新后，先核对这些条目，过时的改写或删除。

## 同步

- 技能本体：`C:/Users/Eric Liu/.codex/skills/nesnd-victoria3` 与 `nesnd-player-writing`。
- 仓库副本：`development/nesnd-skill/` 与 `development/nesnd-player-writing/`。每次修改技能后整体复制到仓库副本并提交，以保留历史。
- 旧版技能（2026-11-06 重写前）在仓库提交 `2643273` 的 `development/` 中。
