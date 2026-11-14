# 已核实的接口事实

> 何时读：用到下列接口、修相关报错，或版本迁移逐条复核时。不必读：一般设计与写作。

每条标出版本状态：〔1.15.0 已核〕表示 2026-11-11 在本机 1.15.0 GAME 或 script_docs 导出中找到同样写法；〔1.13.11，1.15.0 未复核〕表示仍是旧版本证据，用前先查当前 GAME。行号会随版本变化，以对象名为准。

## 外交、战争与条约

〔1.15.0 已核：`GAME/common/diplomatic_catalysts/01_event_catalysts.txt:24、30` 仍用 `"relations(scope:target_country)"`〕

关系数值的保存scope参数用`"relations(scope:target_country)" >= relations_threshold:cordial`，精确实例在GAME `events/diplomatic_events.txt:49`、`common/diplomatic_catalysts/01_event_catalysts.txt:24`。简单`relations:root`不能机械拼成`relations:scope:xxx`；后者在2026-10-31 run143454真实引擎报Unknown trigger type三次，而Tiger未报。须用当前实际参数语法并再冷启动。

〔1.15.0 已核：`00_carlist_war.txt:9` 仍用 `annex_as_civil_war = yes`；1.15 的 `effects.log` 另列 `## annex_as_civil_war`（581 行），`create_diplomatic_play` 说明仍写旧名（959 行）〕

2026-10-31 CNE改革复核：本机导出的 `effects.log` 在 `create_diplomatic_play` 说明中写 `handle_annexation_as_civil_war`，实际 `GAME/common/history/diplomatic_plays/00_carlist_war.txt:9`、`common/on_actions/00_code_on_actions.txt:5220` 使用 `annex_as_civil_war = yes`；Tiger也将前者指出为文档错名。新脚本以实际源码后者为候选，并单独真实触发博弈验证，不能把文档列出视为引擎已经接受。

〔部分核：1.15.0 `on_enemy_capitulated_notification` 在 `00_code_on_actions.txt:2297`，原文行号已变；其余 1.13.11，未复核〕

- `on_wargoal_enforced`的root是执行要求的国家，`scope:target`是被执行者；它不覆盖没有针对性要求的支援国败退。补查原生`on_enemy_capitulated_notification`：00_code_on_actions.txt:4217→messages/00_messages.txt:70→interfaces_l_english.yml:9318–9319显示root国家、scope:target敌国。只记录目标明确的败退，不能用recently_lost_war推断输给谁。该链证实对象语义；AI/零要求分发顺序仍需实测，勿把源码推断写成引擎通过。

〔1.13.11，1.15.0 未复核〕

政变成功检测读实际效果：1.13.11中je_ip4_coup.on_complete先弹事件，ip4_coup_victory_effect的government分支才给国家modifier_government_recently_couped；modifier_successful_coup加在IG。不要把JE进度达标、show_as_tooltip或政变开始当作已成功。新改革登记既有政变修正基线，避免旧档误触；成功/失败共用实际结果谓词，防同帧双结算。

条约预检与创建的商品字段（`good` / `goods`）见[原生条约、供给和援助](native-treaty-aid.md)，1.15.0 已核。

## 按钮、事件与 AI 权重

〔1.15.0 已核：`07_meiji_buttons.txt:87、211、295` 仍为 script value 形状；`00_colonial_administration_buttons.txt:40` 现为 `value = 100`（旧文写 0）〕

`common/scripted_buttons/scripted_buttons.md` 仍示范 `ai_chance = { base = ... }`，但当前 `07_meiji_buttons.txt:87`、`:211`、`:295` 使用 script-value 形状 `ai_chance = { value = 10 if = { limit = { ... } add = 5 } }`，新按钮依据后者。事件 option 的 `ai_chance` 仍是 `base`/`modifier` 形状，两者不能互相移植。事件 modifier 的 trigger 里出现动态 add，不证明外层 AI 权重接受动态值。2026-10-31 Tiger 检出按钮的 base 写法为 unknown token。来源：GAME/common/scripted_buttons/00_scripted_buttons.txt、当前 events 语料，任务34 A2/B2。改写时要保持概率，就读取改前改后两份 AST，枚举相关条件组合核对等价，不默改权重。真实按钮执行另行验收。

〔1.13.11，1.15.0 未复核（事件 option 的 `modifier` 计数需重做）〕

本机1.13.11原版events根目录实际149个ai_chance.modifier全部使用add，其中146个显式trigger块（如events/1848.txt:45起）。本项目新事件用 `ai_chance = { base = 50 modifier = { add = 50 trigger = { 条件 } } }`；把权重按实际国家条件逐支计算，不把按钮script_value的`if/limit/value`语法与事件modifier混为一类。不要依据别的P社游戏假定factor行为；当前未单独证明factor不支持，选择已证实原版用法并实测。亲善/敌对条件互斥时，50的×2/×0意图可分别写+50/−50。

〔1.13.11（2026-11-03 观察者日志），1.15.0 未复核〕

角色当前IG由 `owner.ig:...` 取得；`ig:`只支持country/political_movement，不能直接从character调用。人物转国后应指向转国后的owner。比较法律对象时两端均用law；只有明确比较law_type才取`.type`。JE在immediate保存的事件链scope不自动成为全局AI法案评估scope；固定法案目标可直接比较当前law的type。
事件先声明 `type = country_event` 等类型，再声明 `cancellation_trigger`；当前引擎按读取顺序解析取消条件，反序会报 invalid event type（20261103观察者日志）。同一事件的cancellation_trigger只定义一次，按完整OR语义合并所有取消理由；缺对象先分支判定，再检查人物存活。避免将原本可重复的option/modifier与本应单一的条件字段混为一类。全局on_action调用country效果时不要把全局root当当前country，需在country入口明确保存行动者。
以上修正以1.13.11 event_targets/effects及原版调用链查证，26处人物IG、Donghak三scope、法国取消条件的定位见 WORK/reports/integrity-recheck-20261102/tiger-source-review.json。

## 加载期要求与说明的数据上下文

〔1.15.1 已核：2026-11-12 本机 error.log 与 GAME 源码〕

- `variable_list_size`：script_docs 写 `{ name = X target >= Y }`，引擎读不进 `target`（`Failed to read 'target' for 'variable_list_size'`），条件结果不可靠。另一个已启用 MOD 写 `value <= 15`，本 MOD 已改为 `value = …`，是否生效以下次 error.log 为准。
- `.type` 能从建筑、法律等多种对象取类型（`docs/event_targets.log` 的 `### type`）。写成 `currently_enacting_law.type = { is_same_law_group_as = … }` 时，引擎按 building_type 解析，报 `Inconsistent trigger scopes (building_type vs. law_type)`。把 `.type` 放到被比较的一边：`law_type:law_tenant_farmers = { is_same_law_group_as = root.currently_enacting_law.type }`（GAME `00_tutorial.txt:871`）。
- 事件正文没有 Date 上下文，`[Date.GetString]` 报 `No context supplied … 'Date'`。原版只在代码提供日期的冷却提示里用它，事件正文用 `[TimeKeeper.GetCurrentDate.GetString]`（GAME `ip2_misc_01_l_english.yml:497` 等）。
- 新增文化必须同时定义 6 个静态修正，否则加载报 `Missing expected culture static modifier`：`<文化>_standard_of_living_modifier_positive/negative`（`state_<文化>_standard_of_living_add = 1`）、`<文化>_cultural_acceptance_modifier_*`（`country_<文化>_cultural_acceptance_add`）、`<文化>_fervor_target_modifier_*`（`country_fervor_target_<文化>_add`）。格式照 GAME `07_culture_standard_of_living.txt`、`10_culture_cultural_acceptance_modifiers.txt`，不配本地化。本 MOD 例：`common/static_modifiers/nesnd_regional_communities.txt`。
- 社会阶层和等级制的 `pop_criteria` 里解析不了 `cu:` 链接（`this = cu:manchu` 报 `Invalid right side during comparison 'cu'`，一次读档 1,600 多条）。按人口的文化键判断用 `has_pop_culture = manchu`，原版说明 `common/social_classes/readme.md` 的写法是 `has_pop_religion = catholic`。每个受等级制管辖的人口必须恰好落入一个阶层，判断失败可能崩溃或损坏存档（同一 readme）。
- 脚本与本地化缺 UTF-8 BOM 时，加载报 `should be in utf8-bom encoding`（仍会读取）。原版纹章文件 BOM 混用，引擎不报。
- 可见结局缺 `color`、`possible = { always = no }` 挡住 `add_journal_entry`：见 [journal-display.md §4](../references/journal-display.md)。

## 人物、IG 与文化

〔1.15.0 已核：`ig_clout`、`ig_approval` 在 triggers.log:8546–8553；`building_barrack` 在 `05_military.txt:3`〕

IG判定用当前script_docs的 `ig_clout` / `ig_approval`；不能将scope列表中的简名误当trigger。文化数据使用 `heritage` / `language` / `traditions`，特质查询用 `has_discrimination_trait`。营房标准键是 `building_barrack`，历史复数别名需确认解析后再统计。

〔部分核：1.15.0 triggers.log 仍分列 `has_role`、`has_role_of_type`（8204–8211）；其余 1.13.11〕

角色类型与角色数据库ID也不能互换：本机原生`add_character_role = general`使用类型，而`has_role = character_role_general`查询具体角色；`has_role_of_type`另有其职责。查实际执行脚本与数据库，不以README中的简称示例推断查询接受别名。来源：GAME/common/scripted_effects/00_victoria_ep2_scripted_effects.txt及common/character_roles/00_auto_assigned_roles.txt；本轮错误筛选使真实将领未被分配到新军队，见WORK/reports/canon-route-execution-20261104的A2验证。建筑、人物、法律等引用须按所用字段解析到有效定义，不仅检查文本外形。
跨 `create_country.on_created` 回调不假定外层root或saved scope自动可用：对固定国家先exists再进入c:TAG；遍历内确需回到调用country时按实际scope栈用prev，不能把全局history或after-lobby的none root当country。原版链条、错误名纠正与最终检查见 WORK/reports/qin-persia-20261102/native-political-contracts.md、source-name-corrections.json。

〔1.15.0 已核：`ideology_jingoist_leader` 在 `common/ideologies/01_character_ideologies.txt`〕

- `create_character.ideology` 查询角色意识形态数据库的 `character_ideology = yes`，不能使用同名近似的IG意识形态；例如角色使用 `ideology_jingoist_leader`。

〔MOD 事实，2026-11-05〕

“马 马”已由原生角色字段证明是随机名池组合，不是作者模板。随机名字修订改`common/cultures/CE_cultures.txt`对应名池和独立`nesnd_given_*`键，不全局重译Ma；混合文化保留其其他片段，固定历史人物和旧存档已保存的名字不自动变化。单字名或名姓同字并非语言上必错，是否回避是本项目命名设计。完整溯源与候选见WORK/plans/two-empires/32-names-and-test-harness.md。

### 独特 DNA 人物〔1.13.11，1.15.0 未复核〕

链条：`common/dna_data/ce_*.txt` 中唯一 DNA key → `common/character_templates/ce_*.txt` 中 `dna = ce_person_dna` → `common/history/characters/...` 的 `create_character = { template = ce_person }`，或已证实的事件生成调用。

先读 GAME `character_templates/00_default_template.txt`、`country_afg.txt`，配对 `dna_data/dna_data.md` 和实际 DNA 定义。独特外貌应从当前肖像编辑器导出的 `dna` 字符串或 `portrait_info.genes` 保存，逐项核查当前 `common/genes`，不能编造 DNA 字符串。脸部 DNA 与服装规则分离；创建后在游戏人物页检查姓名、年龄、角色、外貌、服装和读档后保持一致。

## 日志与国家对象〔1.13.11，1.15.0 未复核〕

- 固定TAG建国的state是owner-state；set_capital使用裸数据库键STATE_*，不是s:前缀。combat_unit.count需要整数常量，动态人口分档用独立if/else_if选择常量。不要把继承certain values理解为已证明军队/技术全部继承；原版条件授予技术可单项核对，transfer_to_formation仅用于人物。

- 原版global通过add_contextless_journal_entry显式加入的JE，禁用壳必须保留contextless组；仅改possible=no不能封住显式添加。

- 停用contextless日志仍在最终覆盖中明确 `should_be_involved = { always = no }`；保留关闭条件。优先检查最后生效定义，早期文件有字段不代表最终覆盖仍有。

## 军事单位

〔部分核：1.15.0 `00_military_formations_europe.txt` 等仍用 `ship_type:`〕

海军历史编制在 `create_military_formation` 内使用 `ship`（`ship_type:`），陆军使用 `combat_unit`。统计兵力不能只遍历 combat_unit 而把海军漏报为零；预设单位数不等于实际招募完成数、舰艇维护能力或可投送兵力。

## 改革指标的作用域〔1.13.11，1.15.0 未复核〕

改革指标的scope须明确：`standard_of_living`、`workforce`、`is_in_mild_starvation`、`is_in_severe_starvation`在pop；`state_unemployment_rate`、`state_population`在state；机构、金库、全国收入在country。月度script_value可用`every_scope_state`→`every_scope_pop`聚合，但劳动力加权家庭SoL、州人口加权失业率都是有说明的指标，不能冒充全国UI统计。实现例子与未测边界见 `WORK/plans/two-empires/evidence/cne-reform-engine-matrix.md`；当前只静态核验，需由真实缓存/存档和UI对照补上engine状态。

## 政治

〔1.13.11，1.15.0 未复核〕

当前原生字段为`valid_for_country`、`available_for_interest_group`、`join_weight`。自由党与保守党源码注明国家有效性只在开局求值；动态路线放运行期资格/评分，不承诺`update_party_support`能重跑开局资格。刷新前后党派scope与领袖可能变化，延迟事件须重查对象。改变政治路线不等于必须改党派定义。
