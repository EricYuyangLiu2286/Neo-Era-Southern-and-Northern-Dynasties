# 1.15.0 引擎导出查询

本机游戏为 1.15.0，Steam build 26453692。六份 docs 日志最后写入时间均为 2026-11-05 17:05:04 UTC。查询工具直接读取用户资料目录的 docs 和 logs/data_types，按原始条目名保留全部匹配、来源绝对路径和从 1 开始的行号。每个源文件的 SHA-256、字节数、记录计数见同目录 engine-dump-inventory.json。

## 使用

从主 MOD 目录运行以下 PowerShell 命令。脚本移到其他位置、或要查隔离运行副本时，用 --root 指定有 docs/ 与 logs/data_types/ 的资料根目录。--kind 只读取该种查询需要的文件。查询默认区分大小写、匹配完整名称，--prefix 可查名字前缀，--json 便于其他程序读取。退出码 0 表示找到记录，1 表示没有匹配，2 表示输入或文件错误。

```powershell
$lookup = '../../nesnd-workbench/tools/vic3_dump_lookup.py'
python -B $lookup set_hub_names --kind effect --scope state
python -B $lookup has_law_or_variant --kind trigger --scope country
python -B $lookup owner --kind target --scope state
python -B $lookup context --kind saved-target
python -B $lookup on_monthly_pulse --kind on-action
python -B $lookup great_game_victory_caucasus --kind custom-loc
python -B $lookup building_angkor_wat_throughput_add --kind modifier
python -B $lookup Country.GetName --kind datatype --prefix
python -B $lookup TopScope.sCountry --kind datatype --arity 1 --json
python -B $lookup --inventory
python -B '../../nesnd-workbench/tools/test_vic3_dump_lookup.py'
```

## 索引实际读取的内容

| 源 | 条目数 | 可直接查证的字段 |
|---|---:|---|
| docs/triggers.log | 2044 | Markdown 二级标题、Supported Scopes、Supported Targets、Value Type、用法示例 |
| docs/effects.log | 3666 | 同上；多字段调用的示例保留在 body |
| docs/event_targets.log | 384＋160 | 384 条有标题的转换记录，各自导出 Input / Output Scopes 等字段；以下 160 条为 Event Targets Saved from Code 的名称清单 |
| docs/on_actions.log | 377 | 区块首行包括完整名称，From Code 和 Expected Scope 按字面保存。REPLACE:ryukyu_rivalry_coin_toss 也是本次实际导出名。Expected Scope: none 本身没有描述调用方另存的 named scopes |
| docs/custom_localization.log | 516 | 每个命名区块的 Scope、Random Valid 和候选 Entries；部分还有 Parent 和 Suffix，见 body |
| docs/modifiers.log | 7366 | Static、Dynamic、Potential dynamic 三组原样区分，Mask 表示修正类别。潜在组须结合实际数据库和国家/州/建筑的应用位置核对 |
| logs/data_types/*.txt | 19481 | common 335、gui 935、internalclausewitzgui 2891、script 483、uncategorized 14837。按完整 receiver.member 和从导出头提取的参数个数查，保留 Global promote / Promote / Function / Global function / Type 等分类以及原始 Return type |

--scope 针对脚本输入作用域，依次查 Supported Scopes、Input Scopes、Expected Scope、Scope。用 --kind target 查询 owner 并传入 state 可以看到返回 country。只有函数的调用方 scope 与该清单匹配时，这段链式访问才有来源支持。GUI receiver 查完整名字，修正的 Mask 单独查记录。--arity 表示显式参数个数，不包含 receiver。

格式注意：trigger/effect 导出里引擎生成的个别说明行含任意字节，UTF-8 无法解码。triggers 有 3821 个、effects 有 7335 个此类字节。例如 triggers.log:173 的 any_country_in_afghanistan、effects.log:1399 的 every_country_in_afghanistan 紧跟一行异常说明。读取器将这些字节显示为可辨认的 \xNN，继续保留其后合法的 scope/target 字段和原行号。在新旧 dump 间比较时看各文件 SHA。WORK/tools/cwtools-recheck-cache/vic3/script-docs/effects.log 本次实测 SHA 为 e536aca17918faf85ec516f1f553d3844690fe5a7d01e76cf6a53ffb18da1b3d，当前导出的 effects.log SHA 为 2929285fd483b0d8b6c78966dbde452c37ac795af3c57b408e3a09ef515927fe。NESND catalog.py 的源码索引读取 Clausewitz 赋值符号，导出的 Markdown/数据绑定头则由本工具直接解析。

## 国家名、参数与类型

1. data_types_script.txt:47、54 给出 ROOT 与 SCOPE 的入口。Scope.GetCountry 在该文件:810 返回 Country。data_types_uncategorized.txt:29201–29233 的 Country.GetName、GetNameDef、GetNameNoFlag、GetNameNoFormatting 以及 :26789 的 GetAdjective 均为 Country 实例方法、无显式参数、返回 CString。原版游戏 localization/english/content_104_l_english.yml:76 与 :123 使用 [ROOT.GetCountry.GetNameNoFlag]。这个链读取相关上下文的国家名；GetPlayer 则是独立的当前玩家入口。
2. TopScope.sCountry( Arg0 ) 在 data_types_script.txt:1636 导出的 Promote 返回 Country，同名 Function 在 :2374 返回 [unregistered]。索引保留两个条目。前一条能继续接 Country.GetName。原版 events/expedition_events/congo_river_expedition_events.txt:1118 保存 lost_expedition_country，localization/english/content_104_l_english.yml:1320 使用 [SCOPE.sCountry('lost_expedition_country').GetName]。源码展示这个参数为已保存的 scope 名，且在实际使用前由事件建立。
3. 五份 data_types 文件内，参数列表一般写作 Arg0、Arg1 等；少数宏写 Value、Condition、LocKey，并给出替换表达式，如 data_types_uncategorized.txt:12553–12554。参数名和参数数量、receiver、返回类型皆可直接读取；导出没有单列所有参数的声明类型。工具返回 arguments 和 arity，不补推测的类型。多参数方法应继续找原版实际调用与相同参数来源。孤立的 [unregistered] 条目不能用于类型推导。
4. 脚本命令的类型字段和GUI函数签名应分别读取。例：effects.log:12 的 activate_law 记有 Value Type common/laws、Supported Scopes country、Supported Targets law_type。effects.log:33546–33549 的 set_hub_names 则记输入 state，示例参数为 ukrainian。

## Kaunas 的调用来源

旧运行快照 script-review-first-snapshot/error.5.log:2133、2141、2149、2157、2165 记录的是五种 hub 的俄语后缀键。MOD 的 map_data/state_regions/15_russia.txt:90 为 STATE_KAUNAS，本体同文件:86 为 STATE_LITHUANIA。本体 common/scripted_effects/00_dynamic_state_names_europe.txt:187 按 STATE_LITHUANIA 路由；本次检查时 MOD 在同文件:187 按 STATE_KAUNAS 路由，并在 :190 调用 STATE_LITHUANIA_state_name_assign。该函数 :1768 与 :1785 分别用 set_hub_names = russian / polish。引擎依实际州地区名、hub 类别、后缀拼出查找键，规则来自上述 effects.log:33546。

原版简中 localization/simp_chinese/dynamic_state_and_hub_names_l_simp_chinese.yml:183–195、英文 localization/english/dynamic_state_and_hub_names_l_english.yml:219–232 已有对应 LITHUANIA 俄/波译名，可供补 KAUNAS 对应键时逐 hub 复用。俄文 city 的英文显示 Kovno、波兰文为 Kowno。也应比较此MOD开局五个hub布置，若已换聚落，则按实际聚落名处理。

## 已执行的检查

六项实际导出回归通过，覆盖国家名 getter、同名 Promote/Function、未经声明的参数类型、输入和输出 scope、无效 UTF‑8 后的字段、REPLACE 前缀、Potential modifier 组、独立的 saved-target 清单和缺档退出码。测试绑定 1.15.0 这次导出中的可核实样本，换游戏版本应复核预期差异。以上均为外部文件核查。
