# 语法、作用域与目录

## Victoria 3 专属约束

```text
namespace = ce_example
ce_example.1 = {
    type = country_event
    title = ce_example.1.t
    desc = ce_example.1.d
    duration = 3
    trigger = { c:USM ?= this }
    option = { name = ce_example.1.a }
    option = { name = ce_example.1.b }
}
```

这是格式骨架，不是已验证的完整可发布事件。`#` 注释、`{}` 分块、`=` 赋值/匹配、`yes/no` 布尔；列表通常没有逗号。多次同名块是序列。带引号的值需处理转义，`rgb { ... }` / `hsv { ... }` 为带类型的数据。`@NAME` 是脚本常量，`$PARAM$` 是脚本替换参数，不是 Python/JS 字符串插值。`@[ ... ]` 等表达式不能用简单的空白切分重写。

`?=` 是可空作用域比较/跳转（读相同用法的原版代码以确定上下文），不是普通赋值。`c:USM` 是 country；`s:STATE_GUANGDONG` 是 state_region；`s:STATE_GUANGDONG.region_state:USM` 才是该地区中 USM 的 state；`cu:han` 是 culture；`rel:confucian` 是 religion；`law_type:law_monarchy` 是 law type。`root`、`this`、`prev` 与 `scope:saved_name` 不互换。

效果的 `if = { limit = { ... } ... } / else_if / else` 与条件里的 `trigger_if / trigger_else_if / trigger_else` 不同。script value 的 `value/add/multiply/min/max` 又是一种上下文。GUI 使用 Jomini widget/datacontext 及 `[Get...()]` 绑定，不能把效果写进 GUI 属性。

作用域是 API 的组成部分。写每个效果前记录“输入 scope→返回/跳转 scope→副作用”。事件可以是 country_event、character_event 等，不能从其他 Paradox 游戏推断 root。

## 引用安全：按钮、延迟回复与预览

适用当前 1.13.11 / build 24799966。供给按钮原生日志已经证明缺失 scope/变量会在预览中报错；外部援助与进度条的同形修复见 [按钮修复记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/button-guards-20261101/release-notes.md>)。本轮源码/Tiger/MCP检查不是新的引擎验收。

1. **对象先分支，再使用。** `exists`、`has_variable` 与读取并列，以及普通 AND/OR，不构成短路保证。对象变量用 `exists = var:...` 检查可解析对象；数值用 `has_variable` 检查已赋值。保护实际读取的完整链，例如 `s:STATE_TENASSERIM.region_state:DEI`，不是只检查 state_region。`has_war_with`、`has_truce_with`、`relations(...)`、条约国家参数的右侧对象也属于读取。
2. **谓词缺对象明确返回 false。** `trigger_if` 的 limit 只做安全存在性判断，进入分支后再访问对象；配 `trigger_else = { always = no }`。多层依赖按层嵌套。检查 overlord 时按 `is_subject` 分支；独立国走 this，不让另一并列 AND 求值空 overlord。`?=` 适合允许跳过的副作用，不能单靠它证明“有效目标”条件成立。
3. **预览与执行分开。** `visible`/`possible`/选项 `trigger` 不保护 effect 的预览；`hidden_effect` 也不建立安全边界。effect 内重新检查实际前置条件。预览不能假定前面的 `set_variable` 或 `save_scope_as` 已执行：进度条读取临时 scope 前加存在性分支；读取数值再核变量。缺值无明确默认语义时跳过刷新，不能给对象塞零。只有“未累计周数=0”等有定义的数值才用安全 script_value。
进度条的数值函数也须独立处理未初始化上下文，不能把JE的possible、is_shown_when_inactive或immediate当作读取保护。2026-11-03真实QE1日志和存档显示：其他国家持有未激活JE，数值函数仍触发缺变量报错。用script_value的has_variable分支返回无变化值；状态文字/完成条件用trigger_if并明确缺值false。不要为消除错误向所有国家写入西秦变量，也不要重置已有进度。回归证据：WORK/reports/qe1-variable-20261103/diagnosis.md。

4. **延迟回复核整个生命周期。** 沿按钮→请求标记/对象→延迟事件→选项/AI权重→取消/过期清理检查。接收国、发起国、pending、target、双方 sponsor 均可能失效。过期事件用安全的 cancellation_trigger 收尾；接受执行重新检查资格，拒绝清理只操作仍指向本事件接收国的请求。保留冷却与窗口设计，不能未经可达性核对就断言旧事件会覆盖新请求。
5. **可用条件和实际选择同一集合。** `any_*` 的候选条件应与 `random_*`/`ordered_*` 的 limit 一致，特别是 alive、owner、已有 modifier 等排除项。检查实际执行对象，不以按钮亮起替代结果验证。

条件骨架（country scope；对象有效时才比较）：

```text
trigger_if = {
    limit = { exists = var:partner }
    var:partner = { is_country_alive = yes }
    NOT = { has_war_with = var:partner }
}
trigger_else = { always = no }
```

查原版链条时可定位 GAME `events/commander_events.txt` 的 saved scope、cancellation_trigger 与 option；`common/scripted_triggers/00_scripted_triggers.txt` 的 trigger_if。原版也存在并列 exists 写法，不能据此覆盖本项目已有的真实失败证据。以修复后的外部援助条件和供给 display 为项目安全实例。

接口字段按各自文档核对，不能凭相似名字统一：本机生成的 `triggers.log:8955` 将 can_create_treaty 输入写为 `good`，`effects.log:1056` 将 create_treaty 输入写为 `goods`；实际条约类型 `common/treaty_articles/13_goods_transfer.txt` 与 `common/history/treaties/00_historical_treaties.txt` 使用 goods。此差异保留，升级时重新查证。

修改闭包后检查引用缺失、取消/过期、对象转属与预览四类边界；外部检查须绑定文件 SHA。现有回归工具为 `WORK/tools/check_button_guards_20261101.py`，覆盖真实源码结构及数据不变性，不模拟 Jomini。原生日志复发时扩展相应断言。读取 MCP 嵌套结构用精确 key_path（例如 `cancellation_trigger.NOT`），`[block]` 只表示未展开。

局部重写保留原 token 的引号、重复键和注释；尤其 `"relations(scope:...)"` 不能由宽松 parser 的 emitter 丢掉引号。格式化只限受改定义，以保序 AST 等价及独立 Tiger 复核。新脚本采用 UTF-8 BOM；原文件保留编码/换行。

## 必读文档与当前实现配对

以下均相对 GAME，读文档后必须再读右列真实实现；文档里的省略号不是可用语法。

| 任务 | 官方文档 | 当前代码交叉检查 |
|---|---|---|
| 地区 | `map_data/state_regions/state_regions.md` | `11_east_asia.txt` 与 `common/history/states/00_states.txt` |
| 社会阶层 | `common/social_classes/readme.md`、`common/social_hierarchies/readme.md` | `social_classes/00_default.txt`、`01_edo_system.txt`、`social_hierarchies/*.txt` |
| 法律 | `common/laws/readme.md` | `laws/00_distribution_of_power.txt` 等、`ideologies/*`、`ai_strategies/*` |
| IG 吸引 | 无独立完整规范则查代码 | `common/interest_groups/00_landowners.txt` 中实际吸引字段及相关 `pop_types`、`scripted_modifiers`；不要假设旧职业 strata 仍有效 |
| 日志 | `common/journal_entries/journal_entries.md` | `common/journal_entries/00_opium.txt`、带 `scripted_progress_bar` 的 JE |
| 进度条 | `common/scripted_progress_bars/scripted_progress_bars.md` | `00_je_progress_bars.txt`、使用该键的 JE/事件/按钮 |
| 按钮 | `common/scripted_buttons/scripted_buttons.md` | `common/scripted_buttons/*.txt` 和引用者 |
| 角色 | `common/dna_data/dna_data.md`、`common/genes/genes.md` | `character_templates/00_default_template.txt`、`country_afg.txt`、相应 `dna_data` 和 `history/characters` |
| 建筑/生产 | `common/buildings/buildings.md`、`production_methods/production_methods.md`、`production_method_groups/production_method_groups.md` | `common/history/buildings/11_east_asia.txt`、对应建筑和 PM 定义 |
| 军事编制 | `common/history/military_formations/military_formations.md` | 同目录实际编制；1.13 舰船系统不能继续照搬旧 naval base/flotilla 模型 |
| 事件调度 | `common/on_actions/_on_actions.md` | `common/on_actions/00_code_on_actions.txt`、原版事件 |
| UI | `common/scripted_guis/scripted_guis.md`、`gui/scripted_widgets/scripted_widgets.md` | GAME GUI + CMF + Expanded Building Grid |
| 真引擎测试 | `tools/scripted_tests/scripted_tests.md` | 引擎控制台 `help`、当前生成日志；测试文件不能代替在游戏实际运行 |

社会阶层注意：当前 `strata` 属于 social class，不是直接属于 pop type。一个 hierarchy 至少覆盖上下中三层；每种适用 pop 应明确唯一地匹配某个 class。readme 对 catch-all 顺序的描述与其“不依赖歧义顺序”的告诫并存，实施时用互斥条件，不能靠顺序碰运气。

法律注意：`ai_enact_weight_modifier` 只是 AI 立法选择权重，不保证有合法提案条件、政府/运动支持或可承受的革命风险。支持/反对从意识形态与现行法律比较等机制产生，不要拿 AI 权重冒充 IG 立场。

## 覆盖与编码

按目录分别验证同路径替换、数据库条目替换与追加。现代 `REPLACE:key` 可见于本 MOD 的文化和定义，但不能据此假设 history 文件有同等语义。重复国家/地区定义必须审查有效加载结果。不要用 `.bak` 作活动文件；备份在 WORK/backups 的独立目录。

文本保持原换行/BOM风格，局部修改保留注释；本地化键 ` key:0 "文本"` 不能把双引号/反斜杠错误转义。绝不全局格式化或以字典去重引擎脚本。


## 战争回调与一次全球日志（1.13.11）

- `on_wargoal_enforced`的root是执行要求的国家，`scope:target`是被执行者；它不覆盖没有针对性要求的支援国败退。补查原生`on_enemy_capitulated_notification`：00_code_on_actions.txt:4217→messages/00_messages.txt:70→interfaces_l_english.yml:9318–9319显示root国家、scope:target敌国。只记录目标明确的败退，不能用recently_lost_war推断输给谁。该链证实对象语义；AI/零要求分发顺序仍需实测，勿把源码推断写成引擎通过。
- 战斗结束的on_action先排队次日检查，待占领刷新；用日志周度检查补漏。实际执行重新核战争与controller，友军控制不算敌占。所有回调共用一次标记与同一个提交效果，不能按每个观察国各吞并一次。
- 同一日志供各国查看时，使用`context=none`的journal_entry_group、should_be_involved/should_show_when_not_involved，并按原版01_ryukyu_rivalry方式动态add/remove_involved_country。全局副作用放单次全局回调，个人通知才用all_involved。`scope:journal_entry`只在已附着的JE上下文访问；一次激活与一次提交分开记录，既有状态不随读档清零。
- 湖泊外观疑点先对照有效default.map.lakes、province_terrains和相邻state_region，区分原版分类与MOD误分配。本轮甘肃xBD5671与原版一致，按用户要求保留；不能只把它塞进州而忘了湖泊/地形层。


政变成功检测读实际效果：1.13.11中je_ip4_coup.on_complete先弹事件，ip4_coup_victory_effect的government分支才给国家modifier_government_recently_couped；modifier_successful_coup加在IG。不要把JE进度达标、show_as_tooltip或政变开始当作已成功。新改革登记既有政变修正基线，避免旧档误触；成功/失败共用实际结果谓词，防同帧双结算。

事件duration按本机NEvents.DEFAULT_MONTHS_VALID及原版实例理解为月，不能与变量days等同。异步请求的锁覆盖事件窗口；实际答复提前清理，父任务结束使请求失效。若不能证明锁与事件不会重叠，增加请求身份检查；不要仅凭同名pending变量认定旧回复属于新请求。

## 1.13.11 本机接口与创建回调

IG判定用当前script_docs的 `ig_clout` / `ig_approval`；不能将scope列表中的简名误当trigger。文化数据使用 `heritage` / `language` / `traditions`，特质查询用 `has_discrimination_trait`。营房标准键是 `building_barrack`，历史复数别名需确认解析后再统计。
跨 `create_country.on_created` 回调不假定外层root或saved scope自动可用：对固定国家先exists再进入c:TAG；遍历内确需回到调用country时按实际scope栈用prev，不能把全局history或after-lobby的none root当country。原版链条、错误名纠正与最终检查见 WORK/reports/qin-persia-20261102/native-political-contracts.md、source-name-corrections.json。

## 人物、日志局部scope及重复字段

角色当前IG由 `owner.ig:...` 取得；`ig:`只支持country/political_movement，不能直接从character调用。人物转国后应指向转国后的owner。比较法律对象时两端均用law；只有明确比较law_type才取`.type`。JE在immediate保存的事件链scope不自动成为全局AI法案评估scope；固定法案目标可直接比较当前law的type。
事件先声明 `type = country_event` 等类型，再声明 `cancellation_trigger`；当前引擎按读取顺序解析取消条件，反序会报 invalid event type（20261103观察者日志）。同一事件的cancellation_trigger只定义一次，按完整OR语义合并所有取消理由；缺对象先分支判定，再检查人物存活。避免将原本可重复的option/modifier与本应单一的条件字段混为一类。全局on_action调用country效果时不要把全局root当当前country，需在country入口明确保存行动者。
以上修正以1.13.11 event_targets/effects及原版调用链查证，26处人物IG、Donghak三scope、法国取消条件的定位见 WORK/reports/integrity-recheck-20261102/tiger-source-review.json。

## 宗室延续与无所属角色

需要恢复人物时先查已保存身份，再查本国、every/any_character、流亡池及void，确认存活与owner；exile/void不得先无保护比较owner。移出外国在位ruler/heir须有明确剧情授权，不能将同姓当作身份。只有确定缺少可用活人且作者授权时，create_character创建新角色，不能重用旧历史template当复活。行辈/支系单独记录，淮系不能混宁系；已有姓名不回写，新出生只查自己的父系，不能为每个国家的出生扫描全球。on_created保存新角色后验证其owner，再立为君主；一次结算/创建锁避免重复刷人。当前原版法国、日本及巴西来源见WORK/reports/persia-journal-ui-20261103/ming-successor-generation.md。

## 印度实施的接口与案件隔离（1.13.11）

- 固定TAG建国的state是owner-state；set_capital使用裸数据库键STATE_*，不是s:前缀。combat_unit.count需要整数常量，动态人口分档用独立if/else_if选择常量。不要把继承certain values理解为已证明军队/技术全部继承；原版条件授予技术可单项核对，transfer_to_formation仅用于人物。
- 地区案件循环与重试每次先clear自己的临时backer/target scope。上次循环saved scope不会因下一次if不命中而自动消失。本轮已复现源码反例：第二案不合格赞助者会沿用第一案backer。
- set_state_owner转入现存国可能合并同地区州。返还整个region_state不是返还原来的province子集；回滚须保守证明未取得第三国地块。当前新建单州案同时保存原省份数并监听后续territory变化；不能以num_states=1单独证明安全。未知回调顺序保留引擎待验，不为清理而吞并整个现存国。
- 原版global通过add_contextless_journal_entry显式加入的JE，禁用壳必须保留contextless组；仅改possible=no不能封住显式添加。

来源与实际复查：WORK/reports/india-development-20261103/commission-execution-contract.md、uprising-execution-contract.md、india-standards-review.md。


## 20261103 原生日志补证

- saved scope 作为关系比较参数使用原生 `"relations(scope:target_country)"` 形式，并先分支确认目标存在；`relations:scope:...` 被1.13.11引擎拒绝。来源：GAME/common/diplomatic_catalysts/01_event_catalysts.txt:24、30。
- `create_character.ideology` 查询角色意识形态数据库的 `character_ideology = yes`，不能使用同名近似的IG意识形态；例如角色使用 `ideology_jingoist_leader`。
- 停用contextless日志仍在最终覆盖中明确 `should_be_involved = { always = no }`；保留关闭条件。优先检查最后生效定义，早期文件有字段不代表最终覆盖仍有。

角色存在、存活和owner有效性分别判断；适用于前述宗室/流亡池读取规则的实际失败证据为WORK/reports/observer-logfix-20261103。图形tag中的market链接同样在不存在时显式false；同路径兼容覆盖需随原版更新重查。修复源码与静态检查不升级为实机通过。

## 定点停用原版故障链

用户允许从本MOD侧停用已定位的原版故障内容，其他作者MOD只读。先从error.log定位ID和完整入口链，按数据库支持选择覆盖：本项目已证JE和scripted_button可用`REPLACE:ID`，关闭visible/possible等对应trigger；事件REPLACE支持未核实时沿用同路径覆盖，只把目标事件改为hidden惰性壳（trigger always=no、cancellation_trigger always=yes、空immediate），其余定义和namespace保序保留。只关闭UI入口不能替代清除旧队列和effect中的坏引用。

同路径覆盖须记录当前GAME版本/源SHA，并用保序AST比较所有非目标对象；升级时重新对照，避免冻结整文件后漏掉更新。局部坏权重只停该limit，勿关闭仍被本MOD引用的整个意识形态。scripted_button的ai_chance采用当前实例的`value=0`（00_colonial_administration_buttons.txt:40），旧Markdown的`base`不能直接当作有效语法。2026-11-03具体证据：WORK/reports/cne-time-native-ban-20261103/native-ban-contract.md。
