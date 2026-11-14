---
name: nesnd-victoria3
description: 为 Neo-Era Southern and Northern Dynasties（NESND）维多利亚3 MOD 设计、编写、修复和迁移脚本与内容：日志/事件/按钮/进度条体系、地图与人口、版本迁移、游戏外验证、开发工具。玩家看到的文字另用 nesnd-player-writing。
---

# NESND 维多利亚3开发

本技能给任何接手的代理（Codex、Claude 或其他）使用，只放可复用的做法；项目进度不写在这里。按第 4 节的路由表只读本次任务需要的文件。

## 1. 开工前

- **项目现状**：主 MOD 的 `docs/agents/STATUS.md`。这是唯一的“当前”入口；任务细节在 `.scratch/<工作>/issues/`，旧交接在 `docs/agents/history/`。
- **路径与读写范围**：[lookup/paths.md](lookup/paths.md)。只有主 MOD、本技能、`nesnd-player-writing` 和工作台可写。
- **向谁学**：GAME 本体与作者原作 tag `original-20261030`；`nesnd_*` 文件是代理稿，不是范本（[lookup/paths.md](lookup/paths.md#向谁学)）。

## 2. 硬规则（作者明确要求，不可变通）

- 游戏本体和所有创意工坊目录只读。工坊 MOD 只用于查兼容接口（例如 EACR 服装资源的引用名）；**不学习、不仿写、不复制其他作者的内容设计和代码**。不复制 EACR 的任何素材。
- **启动游戏须有用户在当次任务中的明确要求。**“修复”“测试”“继续”或过去的许可都不算。要求“观察者五速并保存”时，做完这三步就停止，不监看、不轮询日志、不重开。
- **静态检查通过不等于游戏内验证**；交付时分开写（`STATIC_PASS` / `ENGINE_VERIFIED`，见 [verification.md](references/verification.md) §3）。参考文件不再逐条重复这句。
- 修复以修正版的**新开局**为验收基准，旧存档只用来定位问题，不写救档（[debugging-and-updates.md](references/debugging-and-updates.md) §1）。
- 版本迁移保留架空领土、人口、文化与制度意图，不照搬原版新国界，不删掉不再受支持的设计（改写为新接口）。
- 版本更新时提醒作者并复查 **MOD 覆盖的原版文件和键**：按[同路径清单](lookup/vanilla-overrides.md)核对文件，再按[迁移步骤](references/migration.md)核对异文件同名键。
- 不改既有译名和名词；作者的改稿优先于任何代理稿。
- **工作产物、备份、日志、临时文件都写到 D 盘工作台**（`nesnd-workbench` 的 `backups/`、`reports/<日期>-<主题>/`、`tools/`），不写到 C 盘。会话草稿目录只放用完即弃的中间文件。可改的缓存与输出路径见 [lookup/paths.md](lookup/paths.md#本机输出路径)。

## 3. 通用做法

1. **只做被要求的事。** 发现相关问题就列出来问，不顺手扩展成新系统、新事件、新修正或救档分支。
2. **兜底用最小原生守卫：** `?=`、`exists`、`limit`、一个 `hidden invalid_outcome`、`can_revolution_inherit`、`transferable`。只有作者要求、或真实对局出过错的情形，才新增事件、修正或状态变量。对照表见 [content-design.md](references/content-design.md) §4。
3. **逻辑写在用它的地方。** 只用一次的条件和效果写在日志、按钮或事件里，让人在一个文件看懂。scripted trigger/effect/value 只在两处以上复用、或需要参数（如原版 `je_tsarpoints_add_partial = { PROGRESS_BAR = … }`）时提取。
4. **先选内容形状，再写代码。** 日志、按钮、进度条、事件排成一棵树，每个节点有主人、有可见反馈、有结局（[content-design.md](references/content-design.md)）。
5. **引擎行为不确定时**，查 GAME 同类实例和 script_docs 导出（[verification.md](references/verification.md) §1）。仍无法确定，就写最简单的实现并在交付说明里标出，不为每种可能各搭一层保护。
6. **失败是玩法。** 作者接受战败、失国、短缺和破产；判断的是事件顺序和胜负条件是否按设计发生，不替玩家保证成功。
7. **停止条件：** 要求的行为写完、本地化齐全、外部检查跑过、交付说明写清哪些未实机验证。然后停。

## 4. 路由表

任务类型与主 MOD `docs/agents/prompt-kit.md` 的模板一致。先读“必读”，再按主题从第 5 节挑。`references/` 是做法（怎么设计、调试、交付），`lookup/` 是查表（接口事实、数值量级、设定）。

| 任务 | 必读 | 可选 |
|---|---|---|
| 修复 | [debugging-and-updates.md](references/debugging-and-updates.md) §1、[verification.md](references/verification.md) | 引用/预览/延迟回复报错：[script-safety.md](references/script-safety.md)；日志与进度条：[journal-state.md](references/journal-state.md)、[journal-display.md](references/journal-display.md)；崩溃与人物像：[compatibility.md](references/compatibility.md)；接口事实：[engine-facts.md](lookup/engine-facts.md) |
| 新内容 | [content-design.md](references/content-design.md)、[verification.md](references/verification.md) | 第 5 节对应主题；玩家文字另用 `nesnd-player-writing` |
| 文字 | `nesnd-player-writing` 技能 | 字段在界面何处显示：[journal-ui.md](lookup/journal-ui.md)；设定：[canon/](lookup/canon/narrative-context.md)；动态引用的作用域：[script-safety.md](references/script-safety.md) |
| 迁移 | [debugging-and-updates.md](references/debugging-and-updates.md) §2、[migration.md](references/migration.md)、[verification.md](references/verification.md) | [vanilla-overrides.md](lookup/vanilla-overrides.md)、[engine-facts.md](lookup/engine-facts.md)（逐条核版本）、地图海域：[map-transport.md](references/map-transport.md) |
| 工具 | [tools.md](references/tools.md)、[verification.md](references/verification.md) §4 | [paths.md](lookup/paths.md)；改本技能：[skill-maintenance.md](references/skill-maintenance.md) |
| 分析 | [content-tree.md](references/content-tree.md)、[tools.md](references/tools.md) | [verification.md](references/verification.md) §1 防幻觉检查；概率与节奏：[numeric-scale-contract.md](references/numeric-scale-contract.md) |

## 5. 按主题查

| 主题 | 做法（references/） | 查表（lookup/） |
|---|---|---|
| 日志、事件、按钮、进度条 | journal-state、journal-display、script-safety | journal-ui、engine-syntax |
| 文化团结度日志（团结条 + 人口文化转化）：新建或修改时读 | [cohesion-journal](references/cohesion-journal.md) | — |
| 语法、作用域、覆盖原版 | script-safety | engine-syntax、engine-facts |
| 数值、成本、奖励节奏 | numeric-scale-contract | numeric-facts |
| 政治目标、IG、合法性、党派 | political-design-and-difficulty | engine-facts §政治 |
| 经济压力、市场、自给经济、援助 | economic-agency-and-crises、subsistence-transition | native-treaty-aid |
| 地图、拆州、人口分配、交通与港口 | map-economy-design、map-transport | map-data |
| 多国路线、历史人物、小国、势力 | regional-history-and-survival | — |
| 世界观、南北朝制度、人物 | — | canon/narrative-context、canon/north-south-institutions、canon/worldbook.json、canon/character-book.json |
| 服装与 UI 兼容、人物像崩溃 | compatibility | — |

标为 1.13.11 的条目是旧版本证据；[engine-facts.md](lookup/engine-facts.md) 与 [numeric-facts.md](lookup/numeric-facts.md) 逐条注明 1.15.0 是否已复核，用未复核的条目前先对照当前 GAME。

## 6. 交付与维护

- 交付说明的格式见 [verification.md](references/verification.md) §3；然后按 STATUS.md 末尾的规则更新它。
- 维护本技能见 [skill-maintenance.md](references/skill-maintenance.md)；2026-11-11 整理时各段的去向见 [MIGRATION.md](MIGRATION.md)。
