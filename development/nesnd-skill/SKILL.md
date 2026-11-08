---
name: nesnd-victoria3
description: 为 Neo-Era Southern and Northern Dynasties（NESND）维多利亚3 MOD 设计、编写、修复和迁移脚本与内容：日志/事件/按钮/进度条体系、地图与人口、版本迁移、游戏外验证。玩家看到的文字另用 nesnd-player-writing。
---

# NESND 维多利亚3开发

本技能给任何接手的代理（Codex、Claude 或其他）使用。它只放可复用的做法；项目进度不写在这里。

## 1. 开工前

- **项目现状**：主 MOD 的 `docs/agents/STATUS.md`。这是唯一的“当前”入口；任务细节在 `.scratch/debug-release/issues/`，旧交接在 `docs/agents/history/`。
- **路径**：见 [paths.md](references/paths.md)。只有主 MOD、本技能、`nesnd-player-writing` 和工作台可写。

## 2. 硬边界（作者明确要求，不可变通）

- 游戏本体和所有创意工坊目录只读。工坊 MOD 只用于查兼容接口（例如 EACR 服装资源的引用名）；**不学习、不仿写、不复制其他作者的内容设计和代码**。不复制 EACR 的任何素材。
- **启动游戏须有用户在当次任务中的明确要求。**“修复”“测试”“继续”或过去的许可都不算。要求“观察者五速并保存”时，做完这三步就停止，不监看、不轮询日志、不重开。
- 静态检查通过不等于游戏内验证；交付时分开写。
- 版本迁移保留架空领土、人口、文化与制度意图，不照搬原版新国界，不删掉不再受支持的设计（改写为新接口）。
- 每次游戏版本更新或开始适配新版前，先提醒作者一句：「请先按[修改的原版文件清单](references/vanilla-overrides.md)复查新版原版文件是否有改动。」
- 不改既有译名和名词；作者的改稿优先于任何代理稿。

## 3. 默认工作方式

1. **只做被要求的事。** 发现相关问题就列出来问，不顺手扩展成新系统、新事件、新修正或救档分支。
2. **兜底用最小原生守卫：** `?=`、`exists`、`limit`、一个 `hidden invalid_outcome`、`can_revolution_inherit`、`transferable`。只有作者要求、或真实对局出过错的情形，才新增事件、修正或状态变量。
3. **逻辑写在用它的地方。** 只用一次的条件和效果写在日志、按钮或事件里，让人在一个文件看懂。scripted trigger/effect/value 只在两处以上复用、或需要参数（如原版 `je_tsarpoints_add_partial = { PROGRESS_BAR = … }`）时提取。
4. **先选内容形状，再写代码。** 见 [content-design.md](references/content-design.md)。日志、按钮、进度条、事件要排成一棵树，每个节点有主人、有可见反馈、有结局。
5. **引擎行为不确定时**，查 GAME 同类实例和用户文档目录 `docs/*.log`（当前版本的 script_docs 导出）。仍无法确定，就写最简单的实现并在交付说明里标出，不为每种可能各搭一层保护。
6. **失败是玩法。** 作者接受战败、失国、短缺和破产；判断的是事件顺序和胜负条件是否按设计发生，不替玩家保证成功。修复以修正版的新开局为验收基准，旧存档只用来定位问题，不写救档。
7. **停止条件：** 要求的行为写完、本地化齐全、外部检查跑过、交付说明写清哪些未实机验证。然后停。

## 4. 按任务找资料

| 任务 | 读 |
|---|---|
| 新内容，或改造日志链、事件、按钮、进度条 | [content-design.md](references/content-design.md)（必读），再查 GAME 同类 |
| 玩家文字（事件、日志、按钮、进度条、提示、修正名） | `nesnd-player-writing` 技能 |
| 语法、作用域、按钮预览与延迟回复的引用安全 | [syntax-and-routing.md](references/syntax-and-routing.md)、[recipes.md](references/recipes.md) |
| 1.15 日志 outcome、各界面字段、进度条条面与悬停 | [journal-text-contract.md](references/journal-text-contract.md)（查阅用） |
| 政治目标、IG 执政、合法性、党派 | [political-design-and-difficulty.md](references/political-design-and-difficulty.md) |
| 数值、成本、奖励节奏 | [numeric-scale-contract.md](references/numeric-scale-contract.md) |
| 经济压力、市场、自给经济 | [economic-agency-and-crises.md](references/economic-agency-and-crises.md)、[subsistence-transition.md](references/subsistence-transition.md)、[native-treaty-aid.md](references/native-treaty-aid.md) |
| 地图、拆州、人口分配 | [map-economy-design.md](references/map-economy-design.md) |
| 梳理系统结构（日志链、事件链） | [content-tree.md](references/content-tree.md) |
| 修 bug（作者报告、error.log、存档） | [debugging-and-updates.md](references/debugging-and-updates.md) |
| 游戏更新后 | [debugging-and-updates.md](references/debugging-and-updates.md)，再按 [migration.md](references/migration.md) 迁移 |
| 世界观、南北朝制度、人物 | [narrative-context.md](references/narrative-context.md)、[north-south-institutions.md](references/north-south-institutions.md)、`worldbook.json`、`character-book.json` |
| 多国路线、历史人物挪用、小国 | [regional-history-and-survival.md](references/regional-history-and-survival.md)、[faction-model.md](references/faction-model.md) |
| 服装与 UI 兼容、日志人物像的绑定与崩溃排查 | [compatibility.md](references/compatibility.md) |
| 检查、日志、备份、交付 | [verification.md](references/verification.md) |

参考文件中标为 1.13.11 的条目是旧版本证据，使用前对照当前 GAME。

## 5. 向谁学

- **引擎写法**：GAME 本体（当前 1.15.0，见 STATUS.md）。原版是最可靠的范例，但也会出错。
- **作者的设计与文风**：Git tag `original-20261030`（提交 `f18b6c4`）中的 `ce_*` 文件，是未经 AI 改动的原作。当前主 MOD 的 `ce_*` 已被代理改过，不能直接当作者样本。
- **`nesnd_*` 文件**：代理写的现有实现，不是范本。

- **退役文字素材**：[unused_localisations](../nesnd-player-writing/resources/unused_localisations/README.md) 保留未使用本地化，可供 desc、story、information 类文本写作参考；按来源区分作者、AI和原版，采用时由玩家写作技能核对现行设定。

## 6. 交付

交付说明写四件事：改了哪些文件；跑了哪些外部检查；哪些行为未经实机验证；遗留问题。然后按 STATUS.md 末尾的规则更新它。

## 7. 维护本技能

见 [skill-maintenance.md](references/skill-maintenance.md)。改动技能后，同步到仓库 `development/nesnd-skill/`。
