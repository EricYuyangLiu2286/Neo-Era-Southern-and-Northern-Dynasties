# 绝对路径和读写范围

| 代号 | 路径 | 用途与权限 |
|---|---|---|
| MOD | `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties` | 唯一主 MOD；授权修改，修改前独立备份 |
| GAME | `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game` | 当前引擎自带脚本/注释/GUI/地图，只读 |
| INSTALL | `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3` | `launcher/launcher-settings.json` 查版本，`binaries/victoria3.exe` 启动验证；不得改本体文件 |
| WORK | `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench` | 本任务新建的工具、基线、编辑器工程、验证报告、独立备份；允许写 |
| USERDATA | `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3` | 游戏日志/存档/加载配置；验证前保存旧日志与配置，运行后恢复用户加载组合；不得覆盖既有存档 |
| WORKSHOP | `D:\Program Files (x86)\Steam\steamapps\workshop\content\529340` | 参考 MOD 和依赖，全部只读 |

## 参考来源，不是可修改的第二工作区

- `WORKSHOP/3704408897`：East Asian Clothes: Redux 1.0.4。查 `common/scripted_triggers/EACR_scripted_triggers.txt`、`00_EACR_mod_compat_trigger.txt`、`zz_EACR_mod_compat_trigger.txt`；再查 `gfx/portraits/portrait_modifiers/EACR_clothes.txt`、`EACR_headgear.txt` 和 `common/genes`。服装规则→gene template→accessory→asset/mesh/texture 是完整链条。
- `WORKSHOP/3385002128`：Community Mod Framework 1.65.0，目标 1.13。UI 注入、共享组件、`data_binding`、`gui`、`input_profile`。先与 GAME 同路径文件比对，不把整套 GUI 移植进本 MOD。
- `WORKSHOP/3278156786`：Expanded Building Grid，目标 1.13。重点 `gui/states_panel_buildings.gui` 与 `gui/expanded_building_grid.gui`，对照 GAME 的州建筑页面。它解决布局，不是历史建筑初始化。
- `WORKSHOP/3464386853`：大洋国—汉洲联省共和国，目标 1.13。地图、日志、事件链实例；`docs/skills/vic3-modding/scripts` 的检查器只作代码参考，其结论不等同引擎验收，不执行会写回该 MOD 的脚本。
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
