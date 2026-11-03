# 2026-11-03 原版故障链停用合同（只读研究）

状态：SOURCE_RESEARCH；未改主 MOD，未开游戏。`catalog.py status` 返回 CURRENT，1.13.11 / Steam build 24799966，changed_count=0。对象是 `observer-finish-20261103/logs/error.log` 的原版脚本错误；其他 MOD、重复 add_journal_entry 与无源码定位的引擎断言均不扩入禁用范围。

路径缩写：

- GAME = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`
- MOD = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`
- WORK = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`
- DOC = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs`

## 可直接实施的最窄集合

| 故障 | 边界 | 建议停用 | 保留 |
|---|---|---|---|
| 波兰缺 target | JE → button → .1 → .2 | `christ_of_nations_button`，`poland_events.1`、`.2` | 原版波兰 `.3`–`.7`、所有 `ce_poland_*` 与 MOD 波兰外交/战争链 |
| 桑给巴尔无州建国 | 历史 add JE → JE complete → event | `je_splitting_oman`、`zanzibar.1` | `je_lion_of_the_zanj`、`zanzibar.2`–`.6`、既有 ZAN 及领土 |
| 群众集会缺 relevant_state | 半年随机池 → event | 仅 `movement_events.6` | 其余 14 个运动事件和运动系统 |
| 政变余波缺邻接州 | 半年随机池 → event | 仅 `coup_aftermath_events.1` | 政变成功效果、CNE 政变失败联动、其余余波 `.2`–`.4` |
| 整合主义 character 错 scope | ideology weight 分支 | 两个“赔款 +25”分支 | ideology ID、法律态度、生成资格及其余权重 |
| 海况 randomization | 三个海况 intensity | 仅 cyclone、rough_waters、tropical_storm 三条已报错海况惰性化 | 海战、舰船、其余 4 条海况 |
| 海战 UI 调用 | 4 个本地化键 | 移除两个非法 PP 计算表达式；中文另将 UnitsDesc 更正为 ShipsDesc | 舰队/战斗系统、其他文本 |

这张表以逐项日志、实际调用者和源码为依据，详见下面的引用。没有证据支持整套禁用波兰、运动、政变、意识形态或海战。

## 覆盖与壳的合同

1. **JE / scripted_buttons**：项目已有 `REPLACE:` 实例可沿用。JE 例为 [MOD zzzz_nesnd_india_native.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/zzzz_nesnd_india_native.txt:1>)；按钮例为 [MOD ce_replace_buttons.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/ce_replace_buttons.txt:1>)。
2. **events**：本项目的实际停用先例采用**与 GAME 相同相对路径的文件覆盖、裸事件 ID**，并非 `REPLACE:event.id`。见 [MOD 日本壳:4](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/japan_events/ep2_meiji_restoration.txt:4>)。本轮全 MOD events 搜索没有 `REPLACE:` 实例；本机官方文档也未找到其支持声明。不要把其他数据库的模式外推到事件。安全实现是按原相对路径保留整文件，仅用下列壳替换目标 ID；逐项验证其他顶层块逐字或保序 token 相同。
3. **ideologies / naval_battle_conditions**：本轮没有找到主 MOD 已有 `REPLACE:` 使用证据，不能把“语法看起来相同”记作已证支持。若根代理已有当前数据库加载证据，可按它选 REPLACE；否则采用同路径完整文件覆盖、只改本报告指定块。此处只给安全回退，不宣称该数据库不支持 REPLACE。
4. 不能以事件 `trigger = { always = no }` 单独证明明确 `trigger_event` 调用必被拦截。本机 [effects.log:37336](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:37336>) 只声明触发事件，没有承诺重验 event trigger；官方 [on_actions 文档:58](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/_on_actions.md:58>) 明确说明池中事件检查触发条件。**本轮未证明明确调用究竟是否绕过 trigger，因此不作确定断言**；入口禁用 + 删除实际 effects 的壳，使结果不依赖这个未决语义。

事件统一形状（先 `type`，后 `cancellation_trigger`；不留 title/desc/placement/scope/option/AI/原 immediate）：

```text
namespace = poland_events
poland_events.1 = {
    type = country_event
    hidden = yes
    trigger = { always = no }
    cancellation_trigger = { always = yes }
    immediate = { }
}
```

这与现有日本壳一致，适用于五个目标 country_event。对已经入队/打开的旧事件，`cancellation_trigger` 提供清退意图，空 effects 避免后续触发副作用；旧档实际取消时机仍是 ENGINE_NOT_RUN。不能仅保留原效果并加 hidden=yes。

按钮壳保留原 name/desc、cooldown（`days = normal_modifier_time`）即可，设 `visible={always=no}`、`possible={always=no}`，清空 effect；必要时 `ai_chance={value=0}` 采用[当前原版按钮实例:40](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_colonial_administration_buttons.txt:40>)；旧Markdown的base写法与当前实例不符。不要只把 visible 改成 no 而继续保留事件副作用。

JE 壳保留 icon 与 `group = je_group_historical_content`，设 `is_shown_in_lobby/is_shown_when_inactive/possible/complete/fail = { always = no }`、`invalid = { always = yes }`，不留 immediate/on_complete/on_fail/on_invalid 的副作用。`je_splitting_oman` 是 country-context，不要套用印度 contextless 组。官方 [JE 文档:13](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:13>)、[33](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:33>) 明确 `add_journal_entry` 会忽略 inactive/possible，故 invalid 与清空效果是必需边界。

## 波兰：完整链与清理

- 日志 [1537](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/logs/error.log:1537>)、2134、2289：`.1` 原生第148行读未设置的 `polish_agitation_target_1_scope`；随后 `.2` 第290行在 none 上 random_scope_state。
- [GAME 00_poland.txt:13](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_poland.txt:13>) 把 `christ_of_nations_button` 接入 `je_christ_of_nations`。JE 完成另触发 `.4`，所以禁整个 JE 会误伤统一链。
- [按钮:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_christ_of_europe_buttons.txt:1>) 没有要求存在合格非波兰母文化持地国；第18行明确调用 `.1`，第26行给本 JE `support_separatism_nationalist_propaganda`。入口必须清空 effect，避免事件被取消而仍拿到增益。
- [.1:29](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/poland_events.txt:29>) 随机选非波兰母文化、拥有波兰 homeland 的国家；没有候选时第1个 scope 根本不生成。第45/74/106行在目标国家设置永久选取标记。第148/177/206/235行依次明确调用 `.2`，并支付 funding_polish_radicals 修正。`.2` 在第290行选州；第303–412行增加激进派、临时 `christ_of_nations_target`、关系惩罚，部分选项还有破坏度。`.2` 后没有再调用 `.3`，`.3` 是独立统一事件。
- 精确文件范围：`.1` 4–258、`.2` 261–414；保留417行起 `.3`–`.7`。原有 `funding_polish_radicals`、州标记都具有限时期限；停止新调用不会需要补发或回滚。目标选择标记只有被禁 `.1` 再读取，已有永久标记会变成无效残留；本轮不要增加全局清扫去触碰与任务无关国家。资源定义 [content_3_modifiers.txt:507](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/content_3_modifiers.txt:507>)、[12_diplomatic_modifiers.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/12_diplomatic_modifiers.txt:1>) 保留。

## 桑给巴尔：历史显式 JE 不能靠 possible=no 拦住

- 日志 [2383](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/logs/error.log:2383>)：第32行 create_country 无州；第88行 set_state_owner 没有合法 ZAN。
- 原版 [oma - oman.txt:35](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/oma - oman.txt:35>) 显式加入 JE。该历史文件在主 MOD 没有同相对路径替代，因此它仍是来源之一。
- [00_zanzibar.txt:10](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_zanzibar.txt:10>) 检查苏丹已经更替及仍为君主制；第21行 on_complete → 28行 `.1`。这不是直接 `on_ruler_death` 回调，而是 JE 完成条件。
- [.1:32](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/zanzibar_events.txt:32>) 固定拿 `s:STATE_ZANZIBAR.region_state:OMA` 创建 ZAN，不验证该 owner-state 存在。之后存君主/首都 scopes，选项转让其他非洲领地、附属国，玩家分支 `play_as=c:ZAN`，最后可能 add `je_lion_of_the_zanj`。所以不能只删除报错第88行或只保护新事件入口。
- `.1` 4–303 改惰性壳，保留305行起 `.2`–`.6`；`je_splitting_oman` 用上述 REPLACE 壳终止未来完成。无需删除历史文件，也不新建 ZAN 或搬州补“缺失”条件。
- JE 没有自建变量/修正需要清理。失效后 ZAN 常规释放资格不再被此 JE 阻塞，这是现有 [country_creation:3031](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_creation/00_releasable_countries.txt:3031>) 的自然结果，应写入变化说明；不要为了保留阻塞再造永久假 JE。

## 运动与政变：只禁各一个事件

- [代码半年回调:1867](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:1867>) → 延迟17日的 `coup_aftermath_half_yearly_events` 与20日的 `movement_half_yearly_events`；对应 [半年池:45](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_on_actions_half_yearly.txt:45>)、[74](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_on_actions_half_yearly.txt:74>)。不需要覆盖 on_actions，事件 trigger=no 即可令它们失去候选资格；保留池和其他条目。
- 日志 [733](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/logs/error.log:733>) 对应 [movement_events.6:811](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/movement_events.txt:811>)。触发条件只要求合法运动/大众政治等，没有要求存在 incorporated 且无暴力镇压 decree 的州；immediate第873行才筛这个集合，可能无结果。取消条件第849行只检查 movement，不查 state；选项第895/915行均解引用 state。只替换811–925，保留其余14事件。无长链变量、request锁或延迟回复，既有短期修正自然结束，无需清扫运动。
- 日志 [2334](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/logs/error.log:2334>) 对应 [coup_aftermath_events.1:907](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/coup_events.txt:907>)。trigger第940行只保证有非首都州，immediate第959行却要求首都邻接且本国拥有的州；离散国土能通过前者而不满足后者。两选项985/1001行都不安全读取。只替换907–1022，保留所有 coup_pulse/coup其他定义和1024行起另外3余波。
- `coup_aftermath_var` 是政变成功效果 [00_victoria_ip4_scripted_effects.txt:663](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:663>) 创建的**一年共享标记**。其余3余波也读取并移除它（原文件1047/1068、1121/1180、1238/1274）。因此本壳不全局删除该标记、不改政变成功处理；其他余波仍可消费，未消费会自然到期。

## 整合主义：只关闭错误的加权代码

日志 [2354](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/logs/error.log:2354>)、2379 定位 `01_character_ideologies.txt:8675`，是 `ideology_integralist.non_interest_group_leader_weight` 内“war reparations +25”。[官方 trigger 文档:1879](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/triggers.log:1879>) 要求 country，日志证明此处为 character。相邻 [8672](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/01_character_ideologies.txt:8672>) 仍用旧 `has_diplomatic_pact ... type=war_reparations`。

同一 ideology 的 `interest_group_leader_weight` 在[8439](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/01_character_ideologies.txt:8439>) 同形错误：也从 owner-bearing scope 直接 any_diplomatically_relevant_country，只是改用了条约 article。父级其他分支均显式 owner。可把**这两处 if 的整个 limit 替换为 `{ always = no }`**，删除原 bad iterator（不并列保留），维持该分支 inert。更简单是删掉这两个加权块。不要 country_trigger=no 或 weight整体清零，主 MOD [法国运动:722](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/political_movements/ce_04_country_specific_ideological_movements.txt:722>) 仍引用该意识形态；法律态度8305–8369与其余权重属于有效既有玩法。

本项是“禁两条错误加权代码”，不是改变所有整合主义角色和法律。额外8442行是同定义同形源码缺陷，非本日志另一次已观察错误；交付应说明这个区别。

## 海军：可选极窄停用与独立 UI 问题

[日志496](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/logs/error.log:496>) 与550开始反复报告 intensity 的随机范围无随机上下文。精确归属：

- [naval_condition_rough_waters:178](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/naval_battle_conditions/00_naval_battle_conditions.txt:178>)：intensity 210–215，固定范围0.05–0.1。
- [naval_condition_tropical_storm:223](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/naval_battle_conditions/00_naval_battle_conditions.txt:223>)：intensity263–268，固定范围0.1–0.3。

若按本轮授权直接禁用，保留原 icon，`possible={always=no}`；weight、period、intensity 设为 `{ value=0 }`，删除可选的 max_hull_damage、max_crew_damage 和 modifier 块。官方 [naval_battle_conditions.md:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/naval_battle_conditions/naval_battle_conditions.md:1>) 证明这些字段及脚本数值格式，period=0 表示不造成周期伤害。移除 fixed_range 很重要：仅 possible=no 未证可阻止旧战斗/UI继续求其数值。同路径覆盖仅改这三个条目，强风/平静/雾/冰保持原内容。此举取消三类海况本身的影响，应在交付变更列明。

`naval_condition_cyclone`119在完整末次日志出现一次，已纳入；`naval_condition_ice`166也有同形fixed_range但本局未报错，保留。`command_values.txt:373` 的 `naval_battle_size` 另报 wrong type none；官方注释要求 country root并提供编队scope，此处是引擎海战取数接口，不能靠禁三海况承诺解决，更不能把整个 naval_battle_size 置零以消日志。

UI 是独立来源，不必禁战斗。 [GAME 中文 naval_battles:15](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/naval_battles_l_simp_chinese.yml:15>) 和[英文:17](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/naval_battles_l_english.yml:17>) 证明：

- `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER_START_OF_BATTLE` / `...DEFENDER...`：中文调用 `Get*NumWantedUnitsDesc`，英文是 `Get*NumWantedShipsDesc`。本机 [data_types:56247](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/logs/data_types/data_types_uncategorized.txt:56247>) 有 ShipsDesc，日志明确无 UnitsDesc。中文仅改方法名，保留原句。
- `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER` / `...DEFENDER`：中英文都调用 `CalcCurrent*PowerProjection` 并残留 #todo PP。日志明确 non const promote 失败；生成文档虽列函数，却不能令该 loc 上下文可调用。最窄停用是两个键只显示 `$BATTLE_SHIPS_BREAKDOWN_HEADER$` 加进攻/防御（英文相同语义），删除 PP 计算片段。不发明替代 Get 方法。
- 本地化使用各语言 `replace/`，UTF-8 BOM；不是 `REPLACE:key` 脚本语法。若根代理实施新中文措辞，应按玩家文本技能取样；上述修改只需沿用原文中已有“进攻/防御”词。

## 外部检查与保留限制

- 保序解析比对：事件目标以外所有顶层块与 GAME / 修改前 MOD 等价；禁止用字典解析丢失 option/modifier 等重复项。
- 搜索有效定义：五事件惰性、入口按钮effect为空、JE没有任何后续触发；新文件不要出现 `REPLACE:event.id`，不要存在重复 event ID。
- 期望断言：目标事件不含原scope或实际副作用；完整命名空间保留；type在cancellation_trigger之前；未改 CE 波兰、日本、CNE 政变语义。
- 对 ideology 的验证应比较除两赔款if以外 token完全相等。海况只限3 ID；本地化只限4中文键及2英文键，且方法名能在本机 data_types里找到。
- 本机静态/Tiger/MCP可认证定义闭包，不认证旧档已取消、已经开的事件窗口消失或海况实例缓存更新。无需为本报告启动新局。
- 引擎旧事件已经执行的领土转移、破坏度、激进派不回滚；未证明的 trade-lane assertion / unknown invalid country / command_values none 留作残项，不借禁原版扩大破坏面。

## 来源指纹

以下为研究时 GAME 原始文件 SHA-256，可供根代理绑定候选。修改后原版文件应保持这些值。

- `events/poland_events.txt`: `3e43b72693e2391ebbefb050a595b3efef49fda2e8714c08685565129ff02c18`
- `events/zanzibar_events.txt`: `f9c415efcdd2bc702c51a1768764d33c5b922b5a994af6ac9fe2f6b1de6478b1`
- `events/movement_events.txt`: `7b0ed05dc72f9ad1c9e88569c72ab82a5131cdc17b109708176187a84592cbf7`
- `events/agitators_events/coup_events.txt`: `aee3d155d3c347ac5338468f5814cc5daafcbb9862e801d3287643587d525990`
- `common/scripted_buttons/00_christ_of_europe_buttons.txt`: `9c499857473e03498295a72e259cb71bdc3a655fdf8327e53c54e93544dc5d39`
- `common/journal_entries/00_zanzibar.txt`: `3f7a36bfccd130040abad23af17316e2c848c7d9a42bffe63f6ab9290e668bcd`
- `common/on_actions/00_on_actions_half_yearly.txt`: `404b1db6d1c589a4e958cb75bbc4b741df75ea20ee2a4f8764df334950998bdf`
- `common/ideologies/01_character_ideologies.txt`: `b54d0c294632be73ebc77edcb65d7f841803c6a19bacbb03e6331b0cd2ce39d3`
- `common/naval_battle_conditions/00_naval_battle_conditions.txt`: `d7a68c935c97cfc048ba877bfff2415d0524c62daf8a4ef34478edfdaa0a378a`
- `localization/english/naval_battles_l_english.yml`: `7644e8ffd6cb62962cd2a41971ef8dbd06adc1ddebf4c2c5d05c762b1257c275`
- `localization/simp_chinese/naval_battles_l_simp_chinese.yml`: `ac47ad2ee1692b298946856782ed5ad6d633ea9f0955c8a76d9b6f184cb065e9`


## 主控补证与实施口径

完整末次日志另有一次00_naval_battle_conditions.txt:119的intensity错误，AST定位为naval_condition_cyclone（fixed_range在120行）。因此最终停用3个实际报错海况：cyclone、rough_waters、tropical_storm；ice未在本局报错，保持。前述初查只列2个的记录已被此完整日志证据修正。按钮ai_chance采用当前原版00_colonial_administration_buttons.txt:40–41的value而非旧Markdown中的base，Tiger也检出了base错误；候选已修正。
