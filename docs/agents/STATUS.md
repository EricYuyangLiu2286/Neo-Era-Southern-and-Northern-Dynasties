# NESND 当前状态

这是项目唯一的“当前”入口。只写现在的情况；历史放 `docs/agents/history/`。维护规则见文末。

更新于 2026-11-10。除法国后继内容外，全部任务记录已由作者结束：已交付的标 completed，未实施的（任务 08 原始欠账、南朝立场 01–07）标 rejected。

## 基线

- 游戏：Victoria 3 **1.15.0 Ivan-Chai / Steam build 26453692**。上一基线 1.13.11 / 24799966。
- Git main：2026-11-10 与主 MOD 逐文件同步，主 MOD 的新增、改动与删除均已提交。只在 Git 中的 `development/` 旧参考与 `README.md` 照旧保留。其余分支为历史记录，未合入的内容以主 MOD 为准。
- metadata 版本 0.2.0，声明支持 1.15.0（仅为包声明）。

## 位置

| 名称 | 路径 | 说明 |
|---|---|---|
| 主 MOD | `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties` | 游戏加载目录，唯一可写的游戏目录 |
| Git 工作副本 | `…/Victoria 3/nesnd-workbench/projects/nesnd-repository` | 与主 MOD 是两个目录，合并时逐文件比较 |
| 远端 | `github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties` | 代理用分支，作者合并 |
| 工作台 | `…/Victoria 3/nesnd-workbench` | 工具、备份、报告、原版基线 |
| 技能 | `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3`、`nesnd-player-writing` | 仓库副本在 `development/` |
| 任务账 | `.scratch/debug-release/issues/NN-*.md`，索引 `map.md` | 每项任务的细节与证据 |
| 作者原作 | Git tag `original-20261030`（`f18b6c4`） | 风格与设计的样本 |

## 未完成

法国后继内容还剩两批，沿用[任务 29 的法国方案](../../.scratch/debug-release/issues/29-france-political-planning.md)。

- 第二批：地方建设与人物、政治运动的联动。
- 第三批：共和国的繁荣分配与条件性右转。

法国后继首批[「宫廷与外省」](../../.scratch/debug-release/issues/70-france-court-and-provinces.md)和[法国印度领地与本地舰队](../../.scratch/debug-release/issues/46-english-gujarat.md)均已完成。

2026-11-10 更新（任务 82–87 与地权革命 01–02：鸦片两项、共和派战争目标、营产与军州、地权危机的数值与文件整理、西秦开局营产修正案）已由作者内审通过，Steam 改动说明见 `.scratch/steam-desc/steam_changenote_20261110_*.txt`。

## 已知差异

- 无。2026-11-10 同步后主 MOD 与 Git main 的游戏文件一致；此后在主 MOD 直接改动的文件，同步前先比较差异。

## 历史

- `history/development-summary-20261106.md`：开发过程、作者约束、代理自评。
- `history/retained-versions-20261106.md`：工作台中保留的备份与 Git 引用。
- `history/active-work-to-20261106.md`：2026-11-06 前的逐轮交接。
- `handoff-20261105.md`：任务 36–37 的交接。

## 维护规则

- 本文件只写现在。改动时覆盖旧内容，不在顶部追加新的“当前”段。全文控制在两屏以内。
- 作者确认完成后，从当前待办中移除该项。任务细节和当时的验证记录保存在各自的 issue 文件。
- 被替换的旧状态如仍有价值，另存为 `history/<主题>-<日期>.md`。
- 技能里不写项目状态。
