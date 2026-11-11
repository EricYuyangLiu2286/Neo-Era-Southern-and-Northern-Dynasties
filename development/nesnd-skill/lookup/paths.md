# 绝对路径和读写范围

> 何时读：第一次接手、找某个目录或文件该去哪里、确认某处能不能写。不必读：已知路径时。

| 代号 | 路径 | 用途与权限 |
|---|---|---|
| MOD | `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties` | 唯一主 MOD；授权修改，修改前独立备份 |
| GAME | `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game` | 当前引擎自带脚本/注释/GUI/地图，只读 |
| INSTALL | `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3` | `launcher/launcher-settings.json` 查版本，`binaries/victoria3.exe` 启动验证；不得改本体文件 |
| WORK | `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench` | 本任务新建的工具、基线、编辑器工程、验证报告、独立备份；允许写 |
| USERDATA | `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3` | 游戏日志/存档/加载配置；验证前保存旧日志与配置，运行后恢复用户加载组合；不得覆盖既有存档 |
| WORKSHOP | `D:\Program Files (x86)\Steam\steamapps\workshop\content\529340` | 参考 MOD 和依赖，全部只读 |

## 会话需要连接哪些目录

通过文件桥（每次会话选择文件夹）工作时，连接这三个即可覆盖上表全部常用位置：

1. `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3`：包含 MOD（`mod\Neo-Era…`，可写）、WORK（`nesnd-workbench`，可写）、`logs`、`docs`（script_docs 导出）、`save games`（只读）。
2. `C:\Users\Eric Liu\.codex\skills`：`nesnd-victoria3` 与 `nesnd-player-writing`（可写）。
3. `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3`：GAME，只读。

只在做服装/UI 兼容时再连接 WORKSHOP。OneDrive 和桌面上的旧项目、设定、翻译资料很少需要，用到时再连接。

若会话装有 Desktop Commander 等本机终端工具，它不受上述连接限制，可直接访问这些路径；只读规则仍按上表执行。

## 参考来源，不是可修改的第二工作区

创意工坊 MOD 只用于查兼容接口（资源名、GUI 注入点、触发器名）。不学习、不仿写、不复制其他作者的内容设计与代码；设计与写法以 GAME 本体和作者原作为准。

- `WORKSHOP/3704408897`：East Asian Clothes: Redux 1.0.4。查 `common/scripted_triggers/EACR_scripted_triggers.txt`、`00_EACR_mod_compat_trigger.txt`、`zz_EACR_mod_compat_trigger.txt`；再查 `gfx/portraits/portrait_modifiers/EACR_clothes.txt`、`EACR_headgear.txt` 和 `common/genes`。服装规则→gene template→accessory→asset/mesh/texture 是完整链条。
- `WORKSHOP/3385002128`：Community Mod Framework 1.65.0，目标 1.13。UI 注入、共享组件、`data_binding`、`gui`、`input_profile`。先与 GAME 同路径文件比对，不把整套 GUI 移植进本 MOD。
- `WORKSHOP/3278156786`：Expanded Building Grid，目标 1.13。重点 `gui/states_panel_buildings.gui` 与 `gui/expanded_building_grid.gui`，对照 GAME 的州建筑页面。它解决布局，不是历史建筑初始化。
- `D:\Users\Eric Liu\OneDrive\Documents\Modings\CelestialDynastyOfMan(Old Abandoned Project)`：旧废弃项目。含 `history/`、`interface/`、`map/` 和 `descriptor.mod`；仅查设计、名字与旧关系，**不可将这里的语法视为 Victoria 3 API**。
- `D:\Users\Eric Liu\OneDrive\文档\文案-EMP2286\Modings\北明战国世`：世界观和人物资料；`北明人物列传.docx`、`时间线 - 副本.docx`、人物与时间线文档。只读，写人物另用专门列传技能。
- `D:\Users\Eric Liu\Desktop\paratranz`：已有翻译/名称、不同游戏工程混杂；优先按对象名检索，不批量导入，不重译已定术语。
- `D:\Users\Eric Liu\OneDrive\文档\文案-EMP2286\计划文件（相关项目）`：`1830北明.drawio/png`、政治架构、战争时间线与路线图；用于理解历史意图，只读。

## 当前 MOD 内该去哪里

| 工作 | 先读 | 通常修改 |
|---|---|---|
| 明/吴开局与内战 | `common/history/countries/USM - UnitedStatesOfMing.txt`、`events/flavorUSM_ce.txt`、`events/usm_civilwar_events.txt` | 对应历史文件、`common/journal_entries/ce_usm_the_last_days_of_ming.txt`、`common/on_actions/ce_code_on_actions.txt` |
| 沐帝国 | `CNE - MuEmpire.txt`（国家/人物/人口）、`events/flavorCNE_ce.txt` | 同组文件与 `ce_cne_land_draft.txt` |
| 地图归属与地区 | `map_data/state_regions/*.txt`、`common/history/states/00_states.txt` | 对应区域定义 + `history/pops` + `history/buildings`；不可只改 states |
| 人口 | `common/history/pops/*`，`common/history/population/*` | 前者是群体数量/文化/宗教，后者是国家财富/识字初始化 |
| 公司/建筑 | `common/company_types/ce_companies_china.txt`、`history/buildings/*` | 公司条件与建筑所有权分别处理 |
| 国家文化政体 | `country_definitions/ce_countries.txt`、`cultures/CE_cultures.txt`、`religions/CE_religion.txt`、`government_types/00_ce_government_types.txt` | 保留自定义 tag、文化、宗教与制度设计 |
| 角色 | `character_templates/historical_leaders_ce_asia.txt`、`ce_historical_commanders_asia.txt`；`history/characters/*` | 模板定义与生成调用分别修改；固定 DNA 另建 `common/dna_data` |
| 法律/IG | `laws/ce_trade_policy.txt`、`ideologies/ce_ig_ideologies.txt`、`ce_leader_ideologies.txt`、国家历史 | 法律定义、意识形态态度、国家/角色的意识形态配置，勿混为同层 |
| 本地化 | `localization/simp_chinese/replace/`、`localization/english/replace/` | 两种语言保留相同键；地图名在 `replace/map/`，避免重复键 |

路径和文件列表由 `scripts/catalog.py refresh` 从实际磁盘生成到 WORK/reports/source-catalog.json；索引用于定位，源文件是最终内容依据。

## 向谁学

- **引擎写法**：GAME 本体（当前 1.15.0，见 STATUS.md）。原版是最可靠的范例，但也会出错。
- **作者的设计与文风**：Git tag `original-20261030`（提交 `f18b6c4`）中的 `ce_*` 文件，是未经 AI 改动的原作。当前主 MOD 的 `ce_*` 已被代理改过，不能直接当作者样本。
- **`nesnd_*` 文件**：代理写的现有实现，不是范本。

## 本机输出路径

工作产物、备份、日志和临时文件写到 WORK（D 盘），不写到 C 盘。两个代理应用自身的数据目录由 `WORK/tools/migrate-agent-data.ps1` 移到 D 盘，原位置留目录连接（junction），路径写法不变：

| C 盘原位置 | D 盘新位置 | 内容 |
|---|---|---|
| `C:\Users\Eric Liu\.codex` | `D:\Users\Eric Liu\Documents\ChatGPT\Codex\.codex` | Codex 会话、日志、sqlite、插件、技能（含本技能） |
| `C:\Users\Eric Liu\.cache\codex-runtimes` | `…\ChatGPT\Codex\.cache\codex-runtimes` | Codex 运行时与内置插件 |
| `C:\Users\Eric Liu\AppData\Local\OpenAI\Codex` | `…\ChatGPT\Codex\AppData-Local\OpenAI-Codex` | Codex 命令行程序 |
| `C:\Users\Eric Liu\.claude` | `D:\Users\Eric Liu\Documents\Claude\.claude` | Claude Code 会话记录、file-history、设置 |
| `C:\Users\Eric Liu\AppData\Local\Claude-Data` | `…\Documents\Claude\AppData-Local\Claude-Data` | Claude 桌面版数据与内置 Claude Code |

不迁移：`AppData\Local\Packages\*`（Windows 应用包目录，放连接会影响更新，只清其中缓存）；`C:\Users\Eric Liu\.claude.json`（单个文件）；系统临时目录 `AppData\Local\Temp\claude\…`（会话草稿，只放用完即弃的中间文件，要留的证据复制到 `WORK/reports/<日期>-<主题>/`）。

可设置的位置与保留期（改前以各自官方文档为准）：

- Codex：环境变量 `CODEX_HOME` 决定整个数据目录。`~/.codex/config.toml` 已写 `CODEX_HOME = 'C:\Users\Eric Liu\.codex'`，迁移后经连接指向 D 盘，不必改。
- Claude Code：环境变量 `CLAUDE_CONFIG_DIR` 指定配置与数据目录；`~/.claude/settings.json` 的 `cleanupPeriodDays` 控制本地会话记录保留天数。
- Claude 桌面版：没有用户可设置的数据目录，靠连接迁移。

技能本体的规范路径仍是 `C:\Users\Eric Liu\.codex\skills\…`；迁移后它是指向 D 盘的目录连接，引用不变。
