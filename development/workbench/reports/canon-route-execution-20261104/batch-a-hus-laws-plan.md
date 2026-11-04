# Batch A：HUS 独立社会阶序法律实施计划

状态：PLAN_APPROVED / AWAITING_GO。根代理已批准架构及7.5普通革命延续方向，本版补齐其全局时钟契约；仍需明确GO才实施。本文件没有授权执行测试；本阶段仅查原版与候选源码、制定方案、保存计划。未改玩法、未开游戏、未运行测试。

2026-11-04 接手修订：批次A所有权已由 `/root/hus_law_native_audit` 移交 `/root/unity_native_inventory`。原代理未实施玩法。根代理已认可独立法组、三法、12类、仅冻结citizenship、68项意识形态增补及原生GUI架构；本次只补齐7.5普通革命延续及其相邻状态契约，仍等待明确GO。

日期：2026-11-04。候选 C = `WORK/exports/canon-route-execution-20261104-a`；WORK = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`；GAME = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`。当前原版 1.13.11 / build 24799966，来源指纹及完整链审计见 [hus-law-native-audit.md](hus-law-native-audit.md)。最新范围账见 [steer-implementation-ledger.md](steer-implementation-ledger.md)。本计划以新纠正取代审计报告中“是否采用真正阶序仍可选择”的旧讨论。

## 1. 已确定的交付行为与范围

用户要求采用江户制度同类结构：**独立法组、真正社会阶序、三个新法律**。新法不再属于 citizenship，不通过父法律名称模拟阶序。

- 汉人一等、满蒙二等、美洲原住民三等、白人四等，是实际接纳档的上下限，不只是开局加值。满洲即使全球仍有 `heritage_han`，在本制度中也归满蒙。
- 新局原有 HUS `law_cultural_exclusion` 恢复并冻结；独立阶序法组控制等级。两个登记结果成立后，公民法仍冻结，直到整套HUS阶序退出。
- 根代理已确认“公民权/民权冻结”范围仅为 `lawgroup_citizenship`，不冻结自由言论、妇女权利、劳动、奴隶制或其他 human_rights 法组。
- 两个日志选择保留：满蒙登记、原住民登记；AI只选满蒙。等满12个月后以脚本激活对应新阶序法。选中人群提高至第一接纳档，其他三类的法定接纳边界不变。
- 原住民路线的满蒙外迁、满蒙路线的汗国后续继续使用原有路由变量；本批只修法律接口与其生命周期，不重写人口迁移比例或战争逻辑。
- NKH及其建立的原住民HUS均使用 default hierarchy、原住民主流文化、racial_segregation；原住民HUS不会因重新取得HUS tag再次进入旧等级制度。
- 已完成的初始人口调整（满蒙30%、原住民20%）、州内人口守恒、HUS原三主体文化、全球满洲文化、其他国家历史都保持。本批不编辑人口history。

## 2. 原版完整来源链与实现选择

| 机制 | 当前原始来源 | 本批采用方式 |
|---|---|---|
| 特殊阶序法组 | GAME `common/law_groups/00_laws.txt:38-50` | 新建group，category=power_structure、ideological_opinion_impact=0.5、linked_social_hierarchy指向本阶序 |
| 国家开局阶序 | GAME `common/country_definitions/00_countries.txt:201-210`；`common/history/countries/jap - japan.txt:14-27` | HUS country_definition增加阶序；history激活基础公民法及初始阶序法 |
| 适用人口 | GAME `common/social_hierarchies/00_social_hierarchies.txt:17-24` 与同目录readme | 仅四类适用，其他文化回默认职业阶层 |
| 阶层/经济strata | GAME `common/social_classes/00_default.txt:1-38`；`01_edo_system.txt:1-68`；readme | 四类文化×三种经济strata，12个互斥social classes，保留职业所属strata |
| 接纳上下限 | GAME `common/laws/00_caste_hegemony.txt:188-210,241-261` | 法律modifier直接对12个class设min/max；不再依赖逐文化国家修正 |
| 完整公民待遇 | GAME `common/laws/00_citizenship.txt:486-609` | 保留真实文化排斥全部效果；阶序法只改变接纳边界，避免补写不完整的acceptance_modifier |
| 施加法律作用域 | GAME `common/laws/00_governance_principles.txt:310-315`；`common/scripted_rules/00_scripted_rules.txt:145-150`；`common/scripted_triggers/00_scripted_triggers.txt:1806-1822` | 普通法can_impose在scope:target_country检查冻结；自定义三法can_impose=no |
| 直接激活及终态回调 | GAME `common/on_actions/00_code_on_actions.txt:5020-5033,5108-5119` | on_law_activated的root为law，进入owner后校正；事务flag防重入 |
| 保存并恢复原法律 | GAME `common/scripted_effects/00_victoria_ip3_scripted_effects.txt:1-35`；`events/peoples_springtime.txt:794-810` | 保存active law.type到国家变量，恢复时activate_law=var；用于保留旧档已选公民法 |
| 12个月定时 | 引擎 `effects.log:37336-37341`；`36749-36752` | delay months=12；用保存的事件链数值携带epoch；同一国家状态/epoch再次核验 |
| 清除阶序 | GAME `events/india_events/set_hierarchy_events.txt:48-53,65-70`；引擎effects `set_social_hierarchy` | 显式恢复default，不只删modifier |
| 政治面板法组列表 | GAME `gui/politics_panel_constitution.gui:76-110` | `AccessActivePowerStructureLaws`枚举实际活跃法；无需硬编码另改政治面板 |
| 社会面板阶序标题/法律按钮 | GAME `gui/culture_panel.gui:182-244` | 在候选新增本体同路径文件，仅插入HUS法组分支，保留原版其他块 |
| 可选CMF标题接口 | WORKSHOP `3385002128/gui/com_gui_society_panel.gui:184-221` | 同步`custom_social_hierarchy`为本国law对象，复用CMF通用入口；不复制CMF文件/素材、不将CMF设为必需 |

没有找到可用的局部GUI注入接口能够在本体society面板已有fixed_top内部增加这一法组标题。候选当前只有两个journal_entry_widgets，没有culture_panel或politics_panel覆盖。因此本批原生GUI采用本体同路径窄差异覆盖，并记录源SHA；这是明确的更新依赖。政治面板本身按category取数，无需复制。

## 3. 数据库、符号与三个新法律

独立定义：

```text
lawgroup_nesnd_hus_social_hierarchy = {
    law_group_category = power_structure
    ideological_opinion_impact = 0.5
    affected_by_regime_change = no
    linked_social_hierarchy = nesnd_hus_social_hierarchy
    enable = { nesnd_hus_original_country = yes }
    change_allowed_trigger = { always = no }
}
```

`enable`保护其他国家，linked hierarchy决定本国特殊制度显示，change_allowed_trigger表达该组由登记剧情转换。三法各自仍显式can_enact=no、can_impose=no、ai_will_do=no，以免用一个守卫代替全部入口。脚本activate_law按原生接口绕过正常立法流程；这是用户已授权的12个月选择机制。

三项新law keys：

| law key | 状态 | icon（引用本体） | progressiveness | Han | MM | Native | White |
|---|---|---|---:|---|---|---|---|
| `law_nesnd_hus_four_tier_system` | 初始 | social_hierarchy_enforced.dds | -75 | 80–100 | 60–79 | 40–59 | 20–39 |
| `law_nesnd_hus_manchu_registration` | 满蒙登记完成 | social_hierarchy_codified.dds | -25 | 80–100 | 80–100 | 40–59 | 20–39 |
| `law_nesnd_hus_native_registration` | 原住民登记完成 | social_hierarchy_codified.dds | -25 | 80–100 | 60–79 | 80–100 | 20–39 |

上述接纳值单位为0–100点；阈值来自当前acceptance_statuses：full80、second60、open40、erasure20。progressiveness采用原生严格/编定阶序的-75/-25，只是本批政治类别设计，不声称它自动决定IG立场。

三法无parent，避免跨法组继承假设。每法modifier含12个class的min/max共24项；min80、max100等数值直接按原版class上下限字段配置。新法不另加authority、工资、投票或同化修正，也不加江户的跨职业资质禁令。基础公民法已提供完整待遇，阶序法唯一新职责是固定文化层级边界，避免双算或未选择群体随登记被额外减税/加薪。

每法on_activate只清理三项旧culture tier modifier并重算pop IG支持；不靠该回调中的has_law猜测新法是否已落地。on_deactivate同样清旧修正；本法modifier由引擎随退出移除。切换三法时不在on_deactivate重置hierarchy，否则会中途禁用新法组。完整退出由单独clear_all事务负责。

旧三个citizenship-law keys不直接挪组，避免已存在存档把旧组活动法索引指向新组的不确定性。保留为**隐藏、不可颁布、不可施加的读档兼容定义**，不会成为第四、第五、第六个可选阶序法；完成一次迁移后它们不再活跃。现有`nesnd_hus_registration.txt`承担这三个legacy definitions，新三法另写`nesnd_hus_social_hierarchy.txt`。原有legacy modifiers暂保留定义用于精确清理存档，任何新路径都不再添加它们。

## 4. 文化分类与12个class

文化作用域谓词（固定优先级写成互斥条件，不依赖解析顺序）：

1. MM：`this = cu:manchu` 或 `has_discrimination_trait = heritage_mongolian`。
2. Han：`heritage_han`且不满足MM。
3. Native：`heritage_group_indigenous_american`且不满足前两组。
4. White：`heritage_group_european`且不满足前三组。
5. 其余文化不适用本hierarchy，使用default hierarchy及被冻结公民法的常规接纳；不擅自添加“第五等”制度。

上述trait与group均已在当前GAME实际数据库找到；候选`CE_cultures.txt:292-299`的manchu仍是heritage_han，严禁为分类方便改成其他heritage。按本MOD有效文化定义归类，包括已汉化的自定义文化，而不依据现实百科再分一次民族。

每一类创建下列三个class，keys用`nesnd_hus_<han|manchu|native|white>_<upper|middle|lower>`：

| strata | allowed_professions（原版完整列表） |
|---|---|
| upper | aristocrats, capitalists |
| middle | academics, bureaucrats, clergymen, engineers, farmers, officers, shopkeepers |
| lower | clerks, laborers, machinists, peasants, slaves, soldiers |

每个class = 对应文化谓词 AND 对应职业集合。hierarchy.pop_criteria = 四类文化谓词的OR。四文化类别互斥、15个职业分组互斥，因此不依赖catch-all顺序。每类文化在upper/middle/lower都有一个class，不把所有汉人直接当作经济上层，也不把白人资本家降成劳动者。原生职业待遇、资产、pop数量和文化不变。

为24个min/max字段建立本项目modifier_type_definitions，格式沿用GAME `09_social_class_modifier_types.txt`的`decimals=0/color=good/percent=no/game_data.tags={cultural_acceptance}`。新增字段名采用已证`country_<class_key>_acceptance_min_add/max_add`动态命名模式，并在实施后的引擎文档/解析器能力检查中区分类型标签缺项与真正未识别接口。

## 5. 完整待遇矩阵与不变项

新局基础公民法恢复原作者history中的文化排斥（修改前独立备份HUS.txt:79）。它本身继续提供authority+50、所有文化接纳组成、分离主义与热忱条款。特殊阶序在最终接纳边界上钳制，因此宗教政策/州级delta不会再把MM降到白人以下。

下表是当前原生文化排斥对五接纳档的实际待遇；新法不重复声明或篡改它。数字为本法modifier贡献，不是所有其他系统叠加后的总值。

| 项目 | violent 0–19 | erasure 20–39 | open 40–59 | second 60–79 | full 80–100 |
|---|---:|---:|---:|---:|---:|
| 投票许可 | 否 | 是 | 是 | 是 | 是 |
| 投票权力额外倍率 | 0 | -25% | 0 | 0 | 0 |
| 政治力量倍率 | -30% | -20% | -10% | +10% | +10% |
| 工资倍率 | -30% | -20% | -10% | 0 | +5% |
| 资质增长倍率 | -50% | -30% | -10% | 0 | 0 |
| 同化许可 | 不额外允许 | 是 | 是 | 是 | 是 |
| 同化额外倍率 | 0 | +5% | +15% | 0 | 0 |
| 军职禁止 | 否 | 否 | 否 | 否 | 否 |
| 官职禁止 | 是 | 否 | 否 | 否 | 否 |

由此满蒙登记提高MM工资/接纳状态、解除其接纳上限；原住民登记改善原住民工资、政力、资质和接纳状态；白人等未选择人群不因换登记法被额外改变待遇。不得继续保留旧草稿自定的erasure禁军职与初始/登记不一致的政治力量罚值。

旧档若进入迁移前已由玩家颁布另一项普通公民法，保存并冻结当时实际law type，不回滚玩家已做的普通改革；它的原生待遇与此新局矩阵可以不同，但四类接纳档边界仍固定。交付文档明确这个旧档保护规则。

## 6. 意识形态、统治者与政治支持

独立法组需要自己的立场，不能继续依赖parent=cultural_exclusion。本批不修改人物历史意识形态、不给郭庆达换人设、不额外给IG塞互相抵消的临时ideology。

采用确定、可重建的原版映射：

- 有`lawgroup_edo_social_system`的有效ideology：初始法复制`law_strict_edo_system`立场；两个登记法均复制`law_lax_edo_system`立场。
- 没有Edo映射但有citizenship映射：初始法取`law_national_supremacy`立场；两个登记法取`law_cultural_exclusion`立场。
- 上述具体源law没有显式态度时用neutral；既无Edo又无citizenship组的意识形态不追加新政治判断，保持原生中立/无态度。
- 两个登记法政治态度相同；哪类人获登记由玩家选择和AI按钮100/0决定，不用IG名字猜其文化亲疏。

当前有效源码读得68项需要添加映射。涉及5个文件：`00_ig_ideologies.txt`、`00_ig_ideologies_event.txt`、`00_ig_ideologies_flavored.txt`、`01_character_ideologies.txt`、`03_ig_ideologies_movement.txt`。其中candidate已有`01_character_ideologies.txt`，从该有效文件增补，保留之前原版故障停用等改动；其他4个按GAME同路径复制并只在对应对象新增一个新法组块。未查证ideology数据库的局部INJECT语义，所以本批不赌INJECT、不覆盖整对象并丢掉原权重。

每项原有字段、注释、顺序、重复条目和其他法组态度原样保留。实施后结构比较必须证明差异仅为新增`lawgroup_nesnd_hus_social_hierarchy`块。新法组只对original HUS开启，因此给上述原生意识形态加新组态度不改变其他国家现有法组的立场或人物生成规则。

HUS关键政治结果：

| 来源ideology | 初始法 | 两登记法 | 涉及对象 |
|---|---|---|---|
| ideology_scholar_paternalistic | strongly_approve | strongly_disapprove | HUS地主的既有学者家长制 |
| ideology_confucian | strongly_approve | strongly_disapprove | HUS士人/儒家devout配置 |
| ideology_liberal | disapprove | approve | HUS地主另有的liberal、自由派IG/人物 |
| ideology_radical | strongly_disapprove | approve | 郭庆达既有统治者/工业家领袖意识形态 |
| ideology_meritocratic | strongly_disapprove | approve | 绩效主义立场 |
| ideology_egalitarian | strongly_disapprove | strongly_approve | 平等主义立场 |
| ideology_reactionary | strongly_approve | neutral | 小市民既有反动主义 |

这提供原生政治支持/反对显示及当前法律带来的政治态度，但登记流程本身仍是用户要求的脚本12个月改法，不再额外要求政府支持、合法性或统治者同意。普通立法入口不会因某个IG赞成而绕过剧情步骤。

完整68项映射附在文末；数值映射是本批设计选择，原始立场来自当前原版/有效MOD记录，不称为原版已有HUS政治设计。

## 7. 状态机、锁与回调事务

持久状态：

| 符号 | 类型/职责 |
|---|---|
| `nesnd_hus_hierarchy_version` | 数值2，区分迁移版本；只首次设置 |
| `nesnd_hus_hierarchy_active` | 布尔，整个初始/两登记制度存续期都为真 |
| `nesnd_hus_frozen_citizenship_type` | law_type对象，恢复被冻结的实际公民法 |
| `nesnd_hus_registration_choice` | 既有1=MM、2=Native，不改含义 |
| `nesnd_hus_registration_wait` | 既有12个月限时变量，旧档剩余期限不重置 |
| `nesnd_hus_registration_done` | 既有完成记录，只在新法确认激活后提交 |
| `nesnd_hus_registration_epoch` | 递增数值，延迟结算身份；保存到事件链scope value |
| `nesnd_hus_hierarchy_mutating` | 同步事务的短期重入保护；事务结束移除 |
| `nesnd_hus_native_successor` | 既有永久排除标记，优先于全部初始化与修复 |
| `nesnd_hus_hierarchy_retired` | 制度因任意非革命改成其他tag/正式退出而终止；不用于可证HUS普通革命的临时tag |
| `nesnd_hus_revolution_continuation` | 由HUS的on_revolution_start或可证civil_war_origin_country建立的延续凭据；不是“复制过任何HUS变量”的同义词 |
| `nesnd_hus_revolution_source` | country对象，指向本次制度快照与原登记时钟的来源；读取前检查exists，不以is_country_alive替代对象存在性 |
| `nesnd_hus_revolution_suspended` | 临时革命tag已停用阶序显示但保留制度快照；与永久retired分开 |
| `nesnd_hus_registration_clock_source` | 仅旧档pending无全局时钟时的原wait来源；新v2选择使用下述全局时钟，不依赖已亡国家对象 |
| `global_var:nesnd_hus_registration_serial` | 单调递增的HUS选择编号；同一轮普通革命沿用原编号，永不因换tag重置 |
| `global_var:nesnd_hus_registration_record_epoch` | 已正式登记的当前选择编号；有此记录才能将全局wait消失解释为到期 |
| `global_var:nesnd_hus_registration_wait` | 值为选择编号的全局一年限时变量；只在原HUS第一次选择时设置，革命不复制、不重设 |
| `global_var:nesnd_hus_registration_record_state` | 1=原生全局计时中，2=可结算，3=已结算，4=永久终止，5=legacy原时钟托管；避免全局wait缺失代表多种含义 |

### 7.1 新局初始化

HUS country_definition声明hierarchy；country history在原有政治初始化后调用单一`nesnd_hus_initialize_hierarchy`。事务内：先排除successor→开启mutating→激活原作者文化排斥→保存其law.type→set_social_hierarchy→激活初始新法→设version/active→清三个legacy tier modifiers→同步CMF law变量→退出事务→重算pop IG支持。新局不触碰已经完成的人口调整。

history之外，on_game_started_after_lobby仅调用同一幂等初始化/修复入口，避免重复加变量或重置选择。它不被当成每次读档都会触发的on_load：原版注明它只在每场campaign首次从大厅进入时触发。

### 7.2 选择与12个月结算

按钮effect再次检查original HUS、制度active、未完成、未选择；只写一次choice。从全局serial分配新epoch，国家与全局record_epoch写同一编号，record_state=1；创建本国12个月wait供UI兼容，同时创建值为epoch的全局一年wait作为真正结算时钟。`save_scope_value_as`保存当前epoch，触发隐藏结算事件`nesnd_hus_registration.10`延迟12个月。AI仅满蒙按钮ai_chance=100，原住民=0。全局串行编号/计时只由唯一原HUS选择入口写入；革命目标无第二选择入口，普通国家与native_successor不能覆盖此记录。

隐藏事件重验：国家存在且original；version/active有效；scope中epoch存在且等于国家当前epoch及全局record_epoch；choice合法；未done；record_state不是已结算/终止。v2 settle以已正式登记的全局wait到期为准，国家本地wait缺失不能提早结算；到期后先将state置2，确认新法激活后才置3。若同一日期事件先于全局限时变量消失，延迟1天重试一次；月维护作为事件未随革命转移及旧档无新队列的兜底。不得在迁移时重排完整12个月，从而延长旧档已有等待；legacy托管见7.5.3。

结算顺序：开启mutating→按choice激活正确阶序法→验证`has_law`成立→设置done、移除wait→仅Native路线设置exodus_pending（且exodus_done时不重设）→清legacy modifiers→同步界面→退出mutating。激活失败不写done，留下幂等重试。两个登记法的权利锁仍然有效。

JE完成条件同时要求done与正确新法；invalid只针对亡国、非original/继承者或制度正式退出，不因一次外部尝试改法就删掉wait/留下choice。两个按钮既有visible条件与effect内部条件保持一致；玩家点击等待中不可重复选择。

### 7.3 普通立法与外国施加

`nesnd_hus_citizenship_unlocked`改为：本国没有active标记、没有本hierarchy、也没有三项新法时才解锁；另有successor清理在前保证正常退出。三项任一新法均保持冻结，不再只检测初始法。

六项普通公民法的can_enact继续AND本谓词；can_impose修为`scope:target_country = { nesnd_hus_citizenship_unlocked = yes }`，之后保留原版同集团/默认施加OR。其他国家同一法律的全部modifiers、技术/法律前置、AI权重与on_enact原样保留。三项旧法兼容壳及三项新法均明确禁止普通立法/施加。

### 7.4 直接activate、政体更迭与外部改法

`on_law_activated`挂本模块回调，root=law，进入owner。已在mutating事务则立即跳过；否则只处理本模块active/层级/法律污染的国家。

- original HUS且active：若公民法不同于保存的frozen law.type，在事务中恢复；若阶序被外部替换或阶序法不符合choice/done状态，恢复本hierarchy与期望的新法。pending时期望初始法，done且choice1/2分别期望两个登记法。外部直接activate某登记法不能跳过12个月，也不能改换已完成路线。
- successor带了本模块的hierarchy/新法/旧modifier：优先调用永久清理事务。其余非original先查7.5的普通革命延续凭据；可证延续者只作可恢复暂停，不能调用会删wait/frozen-law的clear_hierarchy。其他非original才按永久退出清理，且不修改该国自己的其他法律。
- 月脉冲只扫描original HUS及携带本模块标记/本hierarchy/旧modifiers者，负责旧档迁移、set_social_hierarchy这种未产生law回调的外部修改与保存期修复，不每月遍历人口。
- 新lawgroup设affected_by_regime_change=no，避免正常政体更迭主动替换登记状态；即便直接脚本改动，最终守卫仍按持久状态修复。HUS政府更换、君主制/共和国改变不会自动解锁公民法。

正式清理入口先清active/设successor或终止语义，再deactivate新法，防止自己的on_law_activated把退出恢复回去。重入guard只覆盖本事务；不永久留下“修复中”标记。

### 7.5 释放国、革命国与改tag

**规则：普通HUS革命胜者恢复HUS时继续原阶序和公民法冻结；临时革命tag不能制造永久退出。** `native_successor`始终先于革命来源、HUS tag和所有初始化；NKH原住民HUS仍退出。任意HUS→其他国家的非革命改tag可以正式retire，释放国与分离主义国家不因有HUS来源就继承这套制度。

当前原始接口与scope：

| 接口 | 已读原版/引擎证据 | 用途和限制 |
|---|---|---|
| `civil_war_origin_country` | 引擎event_targets.log:959–962明确country→country；GAME events/iberia_events/independence.txt:30–36实际从起义国进入原国 | 仅在exists后核来源；必须同时证明普通革命，不将分离国一并当革命继承者 |
| `on_revolution_start` | GAME common/on_actions/00_code_on_actions.txt:5154–5156：ROOT=原国，scope:target=起义国；原版effect:5164–5167向target写变量 | 在来源尚可确定时记录本次延续身份和制度快照 |
| `on_country_formed` | 同文件:3886–3887：ROOT=国家 | 对已经是HUS的可证延续者执行恢复；不宣称所有change_tag必定触发此钩子 |
| `on_revolution_end` / `on_civil_war_won` | 同文件:5513–5515为原国/target；5743–5745说明country根且won在revolution_end之后 | end只检查双方，不猜谁赢；won只恢复当前已为HUS的胜者，否则保留凭据等待formed/月维护 |
| `on_country_released_*` / `on_secession_start` | 同文件:3645–3647、5521–5523 | 释放/分离目标走独立国家清理，不签发普通革命延续凭据 |

没有通用`on_country_created`或已证的“任意改tag回调”；不编造接口。形成/战争钩子与月维护汇入同一个幂等reconcile，NKH创建/继承另在本批可控调用点立即清理。

#### 7.5.1 革命开始：先记录来源，再处理临时制度

当on_revolution_start的ROOT是可证original HUS、不是native_successor且制度active时，先完成原国缺值迁移，再在scope:target存在且非native_successor时记录延续。目标若已有相同来源/epoch的快照则不覆盖；不能用后续外部改法更新被冻结公民法。全局等待记录完全不改；目标仅继承同一个epoch，不创建新一年计时。

明确保存version、制度状态、frozen citizenship law_type、choice、done、epoch，以及既有外迁/汗国防重历史记录。跨国引用均用保存的source/target对象，不在嵌套scope中假定ROOT变成目标；不调用copy_laws来复制本批以外的全部法律。`set_variable { value = <source>.var:<key> }`只能复制值，不证明复制定时变量剩余寿命。

若临时革命国需清除不属于其当前tag的阶序显示，使用单独`nesnd_hus_suspend_revolution_hierarchy`：设suspended、暂停active、只卸本阶序/三法/旧tier与本模块CMF显示；**保留version、choice、done、epoch、frozen-law、原wait和来源凭据，不设retired**。7.4的law回调与月维护必须识别这个暂停态，不能随后把它误交给永久clear_hierarchy。该临时对象不新增普通玩家登记入口、不接受第二次选择。

对先于本模块钩子运行而被旧清理误留retired的临时对象，仅当来源与本次on_revolution_start实际证据吻合时修复此中间标记。不能因一个无来源的has_variable就清除任意国家的正式退出记录。

#### 7.5.2 回归HUS：恢复优先于retired排除

reconcile的顺序固定为：①native_successor/NKH永久排除；②当前HUS且具有可证普通革命延续→恢复；③其他当前HUS的正常初始化/修复；④尚在普通革命临时tag的可恢复暂停；⑤任意非革命改tag、独立释放/分离或正式终止→永久清理。

第二分支必须放在`original_country`的NOT retired门槛之前，避免“先被门槛拒绝，永远到不了恢复”死锁。恢复事务先确认凭据来源并设置mutating，去除仅属于这条革命延续的suspended/retired，恢复active及原frozen-law，再按原choice/done恢复初始法或已完成登记法。恢复不运行history、不重新抽路线、不重发外迁/汗国奖励、不改变新政府的君主/共和法律；只恢复本阶序与已承诺冻结的citizenship。所有legal-state确认后才清暂停态并同步UI。

`on_country_formed`、`on_civil_war_won`和月维护均可多次调用这一个入口。钩子先后顺序不成为第二套结算规则：若胜出时尚非HUS则保留快照；若已经回HUS则直接恢复；保皇方取胜的原HUS只继续自己的既有状态。旧档中若没有新凭据，但仍有可核的`is_revolutionary`与`civil_war_origin_country`且源为受管理HUS，可在月维护补签；仅`was_formed_from=HUS`或普通复制变量不足以证明普通革命。

#### 7.5.3 pending时钟、迟到事件与不可证旧态

**确定的新v2时钟策略：HUS唯一选择epoch + 全局一年限时变量。** 原生`set_global_variable`接受定时寿命且为全局scope（effects.log:36891–36899）；GAME common/decisions/india_decisions.txt:42使用`years=10`，common/on_actions/00_on_actions_yearly.txt:569–572使用`years=5`。故本批使用已证形状`years=1`表达12个月，不依赖未证的expiry-copy接口；延迟事件仍沿用已证`months=12`。`global_var`访问见event_targets.log:589–592；has_global_variable与change_global_variable分别见triggers.log:10350–10353、effects.log:617起。

原选择入口的最小契约（省略执行守卫与choice赋值，但不省略持久存在记录）：

```text
if = { limit = { NOT = { has_global_variable = nesnd_hus_registration_serial } }
    set_global_variable = { name = nesnd_hus_registration_serial value = 0 }
}
change_global_variable = { name = nesnd_hus_registration_serial add = 1 }
set_variable = { name = nesnd_hus_registration_epoch value = global_var:nesnd_hus_registration_serial }
set_global_variable = { name = nesnd_hus_registration_record_epoch value = var:nesnd_hus_registration_epoch }
set_global_variable = { name = nesnd_hus_registration_record_state value = 1 }
set_global_variable = { name = nesnd_hus_registration_wait value = var:nesnd_hus_registration_epoch years = 1 }
```

所有后代仅保存相同epoch；不会重设全局wait。settle要求global record确实存在、国家epoch等于record_epoch、state为1或2、全局wait不存在；若wait仍在，即使继承者本地wait未继承也不能完成。state1首次确认全局计时结束才变2；新法成功激活后变3。state3及本国done阻止迟到/重复队列重发奖励；state4拒绝正式终止后的旧事件。任意其他国家清除自身污染时无权删除全局记录。只有持有匹配epoch的真正原HUS永久退出事务可将state置4；临时革命暂停与普通革命政权替换不终止全局时钟。

不假设延迟country_event会随革命自动转移：恢复HUS方月维护读全局记录兜底，同一日期到期顺序只影响最多下一次检查，不会重新等待12个月或立即错误完成。仍在临时tag时不提交登记、不触发外迁/汗国。已完成路线直接恢复对应新法和state3，不重新建wait。

**旧档pending兼容另列，不伪装成新的12月时钟。** 已有choice/wait但没有本批全局record时，分配一次身份编号并登记state5，保留原本地wait期限，保存clock_source；不创建新的全局一年wait。source仍存在且原wait确实消失后，原HUS或可证回归HUS将state5置2再结算。此前不得因全局wait本来就不存在而结算。革命时目标只继承托管记录和来源引用；原国不能为普通革命永久clear掉托管wait。source引用每次exists守卫，不能把is_country_alive=no当作对象不存在。

未找到读取/复制任意限时变量剩余天数的原生接口，不编造scope.days_left或remaining_variable_days。旧档若在迁移前已丢失原wait期限或革命后托管source对象消失，保留冻结和已知choice/version/status并记migration_conflict，禁止把“找不到wait”解释为等待已满；这一损坏legacy态单列。**新v2选择的全局时钟不依赖旧国家对象存续，已消除此生命周期依赖。** legacy已亡对象的变量到期及具体回调先后仍是未实测引擎边界，不能据静态源码宣称已认证。

#### 7.5.4 真正退出

非普通革命的HUS→其他tag、独立释放/分离国家和显式制度退出才调用永久clear_hierarchy并设retired。不重写这些国家新政体或无关普通法律。已确认的原住民继承者先设native_successor，故即使使用HUS tag或曾带革命凭据也不会复活等级制度；永久清理同步删除革命延续/暂停/时钟引用。

任意正式retired政权将来仅凭tag改回HUS仍不能自动恢复；只有本节证明的普通革命链或另一个明确授权的剧情恢复入口可以恢复。本节不添加后一种未请求剧情。

## 8. 旧档迁移规则

没有真实load回调证据，采用一次性country月维护；新添加JE的immediate也可调用相同入口，但不把其立即刷新时序当作已证。交付明确旧档最迟在第一次月维护完成迁移，不能承诺打开旧档暂停界面时已经迁完。

迁移读取顺序与动作：

| 旧档状态 | 迁移动作 |
|---|---|
| NKH或`nesnd_hus_native_successor` | 先清全部本模块阶序残留，不初始化；保持/设定racial_segregation，native-only主体文化 |
| 普通HUS革命胜者已回HUS，带可证来源及制度快照 | 在NOT retired筛选之前按7.5恢复；保留version/choice/done/frozen law及原等待，不能以临时retired解锁 |
| 普通HUS革命仍用临时tag | 暂停显示但保留快照及来源时钟，不调用永久clear、不重置12个月 |
| 普通HUS、无旧登记law/变量、无version | 保存当时普通公民law.type，安装初始阶序，冻结该law；不回滚已发生的玩家普通改革 |
| 旧初始citizenship law，无choice | 恢复文化排斥作为基础，安装新初始阶序；旧static modifiers清除 |
| 有合法choice且wait仍在 | 保存/还原基础公民法，安装新初始阶序；保留choice与wait原到期时间；不重新排12个月 |
| choice合法、wait已过、未done | 转入settle正常校验；仅一次提交完成 |
| 已有done+choice1/2 | 直接安装对应新登记法；保持done和后续剧情记录，不重新发外迁/汗国奖励 |
| done缺失但旧登记law明确某路线 | 从旧活动法恢复choice及done，再迁移到对应新法 |
| done存在但choice丢失 | 先由旧活动登记法恢复；再可用本国exodus_pending/done证明Native或本国khanate_campaign_started证明MM；不以一个全球汗国变量推断本国路线 |
| 多条来源矛盾或完成记录无任何可证路线 | 留`nesnd_hus_migration_conflict`，保留已知选择/活动法，不擅自重置完成状态或随机挑路线；外部回归把它报告为损坏legacy状态，不称支持此不一致档 |

v2已初始化国家每次只reconcile，不重复history、不重置wait、done、epoch、移民及战争一次性记录。冻结law变量只在首次迁移确定；外部强制改法不能把它更新成新值来绕过冻结。

## 9. clear_all、NKH与原住民HUS

`nesnd_hus_clear_hierarchy`是唯一**永久**退出事务；7.5的普通革命暂停不得调用它：

1. 开mutating；移除active并先设置调用方决定的永久successor/终止状态。
2. 若当前是本hierarchy，`set_social_hierarchy = default_social_hierarchy`；不删除其他mod已经装入的不同hierarchy。
3. 只对正在活跃的三项新阶序law执行deactivate；兼容三项legacy citizenship law则由调用方确定的普通公民法替代，不把国家留成无公民法。
4. 清三项legacy static modifiers、wait、待结算临时引用与本模块frozen law变量；递增epoch使旧延迟事件失效。
5. CMF变量仅在确实指向本模块law时删除，不清外部mod的变量值。清本模块临时saved scopes。
6. 保留done/choice、exodus_done、population_sent、khanate campaign等历史结果记录用于防重，不把清机制等同抹去故事历史。
   永久退出同时移除revolution_continuation/source/suspended和registration_clock_source；普通革命暂停保留这些及frozen-law/wait，不经过此步骤。
7. 退出mutating并recalculate_pop_ig_support。

`nesnd_khanate_prepare`与`nesnd_khanate_form_native_hus`立即显式设default hierarchy。后者必须先设native_successor再change_tag，然后clear_hierarchy，再激活原有successor法律清单中的racial_segregation，最后校准主体文化。只改这三个法律相关函数片段，不接管汗国四州/军队/战争函数。

native-only主体文化：先确保至少一项原住民主流（NKH初始siouan/cherokee保留，必要时以siouan兜底），增加境内原住民文化，再`every_primary_culture`删除所有不满足native谓词者；不再逐个补删汉/满蒙名单。其他国家不调用此effect。汗国/继承者不保留任何12个HUS class的接纳限制。

## 10. 界面与本地化

原生政治面板按power_structure枚举活动法；新group的本地化名与三个law名称/desc/图标是完整数据依赖。社会面板另需新增与Edo同形的标题块：

```text
visible = "[And(InformationPanel.IsTabSelected('classes'), GetPlayer.HasSpecialSocialHierarchyLawGroup('lawgroup_nesnd_hus_social_hierarchy'))]"
datacontext = "[AccessPlayer.GetSocialHierarchy]"
# group_name = SocialHierarchy.GetName
# law_item_small.datacontext = AccessPlayer.AccessActiveLawFromGroup('lawgroup_nesnd_hus_social_hierarchy')
```

仅插入这个HUS专用header，其余culture/religion/acceptance tab保持原版。class列表已经用SocialHierarchy.GetLower/Middle/UpperStrataSocialClasses枚举，本批三列各4项，列高相同，不复制人为min_height_2垫片为4项猜高度。最终实际UI布局仍属引擎未验范围。

可选CMF：在on_law_activated后的owner scope取得`active_law:lawgroup_nesnd_hus_social_hierarchy`，保存这个law对象到custom_social_hierarchy；不保存law_type，因为CMF明确调用GetLaw.GetActiveGroupLaw。更新/清理与本法状态同步。原生同路径GUI保证无CMF时完整；若CMF自身覆盖society type则它有通用hook。不同GUI MOD加载顺序仍是兼容边界，不能声称本批静态检查证明所有组合都正确。

本地化单独两文件：`zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml`与`..._l_english.yml`，UTF-8 BOM。须有：group、hierarchy、3 law及desc、12 class、24 modifier label/desc（采用原生占位写法）、冻结原因提示、两按钮/选择/待完成/已完成状态、迁移冲突内部记录对应必要提示。旧law keys保留兼容名称但不让旧说明覆盖新有效显示。

名称初拟“东洲等级制度 / 四等户籍 / 满蒙编户 / 原住民编户”，不是已通过的玩家文案。实施阶段使用nesnd-player-writing技能，从作者原始replace样本取同类法律/政治日志句法，逐项对读后才落库；本计划不把尚未有脚本的文案视为已完成。已有确认名“华夏东洲共和国”继续沿用，不另译HUS国名。

## 11. 文件所有权与并行边界

下表均相对于C。本批获实施授权后才写入；根代理/其他代理不要同时编辑列出的文件或共享函数片段。

| 文件 | 动作/唯一职责 |
|---|---|
| `common/law_groups/nesnd_hus_social_hierarchy.txt` | 新建特殊法组 |
| `common/social_hierarchies/nesnd_hus_social_hierarchy.txt` | 新建适用人口hierarchy |
| `common/social_classes/nesnd_hus_social_classes.txt` | 新建12 classes |
| `common/modifier_type_definitions/nesnd_hus_social_class_modifiers.txt` | 新建24 min/max元数据 |
| `common/laws/nesnd_hus_social_hierarchy.txt` | 新建三个实际阶序laws |
| `common/laws/nesnd_hus_registration.txt` | 三旧law隐藏兼容定义 |
| `common/laws/zzzz_nesnd_hus_citizenship_lock.txt` | 六普通法冻结与target施加守卫 |
| `common/scripted_triggers/nesnd_hus_registration.txt` | 四类互斥谓词、状态、冻结、路线 |
| `common/scripted_effects/nesnd_hus_registration.txt` | 初始化/迁移/reconcile/clear/选择/结算；保留外迁逻辑只接新完成守卫 |
| `common/on_actions/nesnd_hus_registration.txt` | law owner回调、月维护、形成/胜出恢复、革命开始记源、释放/分离清理 |
| `common/journal_entries/nesnd_hus_registration.txt` | 新制度状态、完成/失效、旧JE禁用壳保持 |
| `common/scripted_buttons/nesnd_hus_registration.txt` | 两按钮显示/作用条件及AI100/0 |
| `events/nesnd_hus_registration.txt` | 新12月隐藏结算事件；现有两通知事件保持 |
| `common/country_definitions/ce_countries.txt` | **只改HUS块**增加hierarchy，不改其他国家 |
| `common/history/countries/HUS.txt` | 恢复原文化排斥、调用新初始化；其他历史不动 |
| `common/scripted_effects/nesnd_native_khanate.txt` | **仅prepare、native_primary_cultures_only、form_native_hus**中的法律/阶序/主体文化清理接口 |
| `common/ideologies/00_ig_ideologies.txt` | 从当前GAME复制，仅添加本group态度块 |
| `common/ideologies/00_ig_ideologies_event.txt` | 同上 |
| `common/ideologies/00_ig_ideologies_flavored.txt` | 同上 |
| `common/ideologies/01_character_ideologies.txt` | 以当前candidate有效文件为基，仅添加本group，保留已有禁用/修复 |
| `common/ideologies/03_ig_ideologies_movement.txt` | 从当前GAME复制，仅添加本group态度块 |
| `gui/culture_panel.gui` | 从当前GAME复制，仅插入HUS阶序header |
| `localization/simp_chinese/replace/zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml` | 新有效中文文案 |
| `localization/english/replace/zzzz_nesnd_hus_social_hierarchy_l_english.yml` | 新有效英文文案 |

现有`common/static_modifiers/nesnd_hus_culture_tiers.txt`仅保留旧存档定义供清理，不再添加其modifier，原则上不编辑。人口、军事/四州/战争/其他国家路线、团结度、主MOD和Git发布均不属本批实施所有权。

WORK文件：本计划、来源记录、实施后的native-clone-diff、writing-comparison和batch-a测试报告。生成重复class/态度字段的辅助工具如确有需要放WORK/tools，不混入候选正式包。本文源清单的生成仅是阅读/记录，不是运行测试。

## 12. 执行与验证顺序（尚未执行）

1. 根代理审阅本计划，确认24文件所有权及native_khanate三个函数的共享边界；记录本批候选pre-change指纹。
2. 一次性实现数据库→谓词/生命周期→历史/继承者→意识形态→GUI完整闭包，不只提交law骨架。
3. 完成中英玩家文本逐条作者对读；确保新有效键引用真实字段、范围与代价。
4. 报告IMPLEMENTED后转入本批独立测试阶段：不得在计划阶段以快速检查冒充已测试。
5. 外部测试与反例通过后交根代理做跨批整合/审查；本轮不启动游戏。交付只能写STATIC_PASS及精确未验引擎语义。

测试阶段必须覆盖以下断言与反例：

- 每个有效culture×15professions恰好匹配一个适用class或明确default；Manchu虽然heritage_han仍只MM；Mongol/Buryat/Kalmyk、各Han文化、欧洲/美洲类别的交集与空集。
- 三法律完整24上下限字段、全部class/group/modifier/icon/localization解析闭合；一般宗教/州delta可改变边界内的值，但不能越过规定档位；选中群体变full，未选群体边界逐字相等。
- 六普通法的非冻结内容与当前原版结构相同；can_impose中root与target的四种组合（普通→HUS、HUS→普通、HUS→HUS、普通→普通）；注册结果不解锁公民法。
- 独立新group只有3可用law；3legacy无法选择/施加；所有其他国家无新增活动group/阶序。
- 新局、未迁移旧档、pending旧档剩余时间、两已完成路线、旧法推断路线、矛盾legacy；不得重置wait或重复外迁/汗国触发。
- 12月到期前/当日/之后，事件epoch缺失/旧epoch/重复队列，done提交前激活失败，重复按钮，国家亡灭/改tag/复归，successor同tag排除。
- 普通革命在初始/pending/两完成路线四态开始，目标先被law回调/先被start处理两顺序；临时tag不得永久retire；胜者先formed或先won均恢复HUS公民法冻结；保皇方胜出不重置；source失活但对象仍在、source不存在分别走守卫/冲突；释放/分离和任意非革命改tag不冒充延续；native_successor即使有革命记录仍优先排除。
- 直接激活普通法/另一登记法/初始法，set_social_hierarchy外部更改，nested on_law_activated；mutating不泄露，expected state恢复，clear_all不会被回调反向复活。
- NKH/default→HUS successor/default；即使无pop的非原住民曾是primary也必须移除；至少保留一项native primary；racial_segregation落地；普通国家的primary清单保持。
- 68项意识形态新增块之外所有源字段结构不变；人物历史ideology不变；当前郭庆达与HUS地主/士人具名态度符合映射表，其他国家原组态度不变。
- 无CMF原生政治category数据入口与society header闭合；CMF值为law而非law_type，退出只清本模块的值；GUI复制文件与源差异只有新增block。
- legacy国家修正在任何退出/迁移完成后为零；任意初始/登记切换不会叠加旧modifier；global Manchu及人口文件指纹不变。

实际引擎仍需未来授权场景核验：自定义class min/max动态modifier在该build的识别与最终接纳钳制、on_law_activated重入时序、12月事件队列与存读档、AI自然点击、法组与class GUI显示、强制改法真实菜单与结算。外部源码/模型不替代这些观察。

## 附录A：当前有效意识形态映射

| ideology | source mapping | initial | both registry laws | source file : line |
|---|---|---|---|---|
| `ideology_hierarchic` | EDO | strongly_approve | disapprove | [00_ig_ideologies.txt:189](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt:189>) |
| `ideology_isolationist` | CIT | neutral | neutral | [00_ig_ideologies.txt:368](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt:368>) |
| `ideology_meritocratic` | EDO | strongly_disapprove | approve | [00_ig_ideologies.txt:457](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt:457>) |
| `ideology_liberal` | CIT | disapprove | approve | [00_ig_ideologies.txt:569](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt:569>) |
| `ideology_egalitarian` | EDO | strongly_disapprove | strongly_approve | [00_ig_ideologies.txt:713](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt:713>) |
| `ideology_reactionary` | CIT | strongly_approve | neutral | [00_ig_ideologies.txt:803](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt:803>) |
| `ideology_liberal_modern` | CIT | disapprove | approve | [00_ig_ideologies_event.txt:64](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_event.txt:64>) |
| `ideology_scholar_paternalistic` | EDO | strongly_approve | strongly_disapprove | [00_ig_ideologies_flavored.txt:40](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:40>) |
| `ideology_confucian` | EDO | strongly_approve | strongly_disapprove | [00_ig_ideologies_flavored.txt:183](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:183>) |
| `ideology_bakufu` | EDO | strongly_approve | strongly_disapprove | [00_ig_ideologies_flavored.txt:217](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:217>) |
| `ideology_shinto_moralist` | EDO | approve | disapprove | [00_ig_ideologies_flavored.txt:256](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:256>) |
| `ideology_austrian_hegemony` | CIT | disapprove | neutral | [00_ig_ideologies_flavored.txt:333](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:333>) |
| `ideology_buddhist_moralist` | EDO | approve | disapprove | [00_ig_ideologies_flavored.txt:414](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:414>) |
| `ideology_sikh_militancy` | CIT | disapprove | approve | [00_ig_ideologies_flavored.txt:532](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:532>) |
| `ideology_heavenly_kingdom_theocratic` | CIT | approve | disapprove | [00_ig_ideologies_flavored.txt:602](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:602>) |
| `ideology_constitutionalist` | EDO | disapprove | approve | [00_ig_ideologies_flavored.txt:675](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:675>) |
| `ideology_sovereignist` | CIT | disapprove | neutral | [00_ig_ideologies_flavored.txt:796](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:796>) |
| `ideology_enclavist` | CIT | approve | disapprove | [00_ig_ideologies_flavored.txt:828](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:828>) |
| `ideology_ilustrado` | CIT | disapprove | approve | [00_ig_ideologies_flavored.txt:1332](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:1332>) |
| `ideology_liberal_praetorian` | CIT | approve | neutral | [00_ig_ideologies_flavored.txt:1374](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:1374>) |
| `ideology_conservative_praetorian` | CIT | approve | neutral | [00_ig_ideologies_flavored.txt:1409](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:1409>) |
| `ideology_rangaku` | EDO | disapprove | approve | [00_ig_ideologies_flavored.txt:1451](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:1451>) |
| `ideology_japan_hierarchic` | EDO | strongly_approve | disapprove | [00_ig_ideologies_flavored.txt:1568](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:1568>) |
| `ideology_japan_hierarchic_2` | EDO | strongly_approve | disapprove | [00_ig_ideologies_flavored.txt:1624](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:1624>) |
| `ideology_traditionalist` | EDO | strongly_approve | strongly_disapprove | [01_character_ideologies.txt:126](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:126>) |
| `ideology_traditionalist_minoritarian` | EDO | strongly_approve | strongly_disapprove | [01_character_ideologies.txt:332](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:332>) |
| `ideology_radical` | EDO | strongly_disapprove | approve | [01_character_ideologies.txt:1176](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:1176>) |
| `ideology_reformer` | EDO | disapprove | approve | [01_character_ideologies.txt:1692](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:1692>) |
| `ideology_social_democrat` | EDO | strongly_disapprove | approve | [01_character_ideologies.txt:3274](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:3274>) |
| `ideology_fascist` | CIT | approve | disapprove | [01_character_ideologies.txt:4572](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:4572>) |
| `ideology_anarchist` | CIT | strongly_disapprove | approve | [01_character_ideologies.txt:5115](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:5115>) |
| `ideology_ethno_nationalist` | CIT | approve | disapprove | [01_character_ideologies.txt:5538](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:5538>) |
| `ideology_humanitarian` | CIT | strongly_disapprove | neutral | [01_character_ideologies.txt:7288](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:7288>) |
| `ideology_jacksonian_democrat` | CIT | neutral | neutral | [01_character_ideologies.txt:7579](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:7579>) |
| `ideology_integralist` | CIT | disapprove | neutral | [01_character_ideologies.txt:8305](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:8305>) |
| `ideology_humanitarian_royalist` | CIT | strongly_disapprove | neutral | [01_character_ideologies.txt:9401](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:9401>) |
| `ideology_despotic_utopian` | CIT | strongly_disapprove | neutral | [01_character_ideologies.txt:9712](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:9712>) |
| `ideology_sovereignist_leader` | CIT | disapprove | neutral | [01_character_ideologies.txt:10116](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:10116>) |
| `ideology_modernizer_leader` | EDO | disapprove | approve | [01_character_ideologies.txt:10394](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:10394>) |
| `ideology_carlist` | CIT | neutral | neutral | [01_character_ideologies.txt:10577](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:10577>) |
| `ideology_carlist_2` | CIT | neutral | neutral | [01_character_ideologies.txt:10844](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:10844>) |
| `ideology_miguelist` | CIT | neutral | neutral | [01_character_ideologies.txt:11108](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:11108>) |
| `ideology_miguelist_2` | CIT | neutral | neutral | [01_character_ideologies.txt:11371](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:11371>) |
| `ideology_ilustrado_leader` | CIT | disapprove | approve | [01_character_ideologies.txt:11631](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:11631>) |
| `ideology_mitogaku` | EDO | disapprove | approve | [01_character_ideologies.txt:11725](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt:11725>) |
| `ideology_absolutist_movement` | CIT | neutral | neutral | [03_ig_ideologies_movement.txt:66](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:66>) |
| `ideology_anarchist_movement` | CIT | strongly_disapprove | approve | [03_ig_ideologies_movement.txt:303](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:303>) |
| `ideology_fascist_movement` | CIT | approve | disapprove | [03_ig_ideologies_movement.txt:433](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:433>) |
| `ideology_liberal_movement` | CIT | disapprove | approve | [03_ig_ideologies_movement.txt:532](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:532>) |
| `ideology_reactionary_movement` | CIT | strongly_approve | neutral | [03_ig_ideologies_movement.txt:738](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:738>) |
| `ideology_ethno_nationalist_movement` | CIT | approve | disapprove | [03_ig_ideologies_movement.txt:950](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:950>) |
| `ideology_liberal_republican_movement` | CIT | disapprove | approve | [03_ig_ideologies_movement.txt:969](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:969>) |
| `ideology_pluralist_movement_1` | CIT | approve | neutral | [03_ig_ideologies_movement.txt:1024](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1024>) |
| `ideology_pluralist_movement_2` | CIT | disapprove | neutral | [03_ig_ideologies_movement.txt:1037](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1037>) |
| `ideology_pluralist_movement_3` | CIT | strongly_disapprove | approve | [03_ig_ideologies_movement.txt:1050](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1050>) |
| `ideology_pluralist_movement_4` | CIT | strongly_disapprove | disapprove | [03_ig_ideologies_movement.txt:1063](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1063>) |
| `ideology_sovereignist_movement` | CIT | disapprove | neutral | [03_ig_ideologies_movement.txt:1076](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1076>) |
| `ideology_national_liberal_movement` | CIT | approve | disapprove | [03_ig_ideologies_movement.txt:1315](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1315>) |
| `ideology_integralist_movement` | CIT | disapprove | neutral | [03_ig_ideologies_movement.txt:1370](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1370>) |
| `ideology_carlist_movement` | CIT | neutral | neutral | [03_ig_ideologies_movement.txt:1428](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1428>) |
| `ideology_carlist_movement_2` | CIT | neutral | neutral | [03_ig_ideologies_movement.txt:1481](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1481>) |
| `ideology_miguelist_movement` | CIT | neutral | neutral | [03_ig_ideologies_movement.txt:1534](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1534>) |
| `ideology_miguelist_movement_2` | CIT | neutral | neutral | [03_ig_ideologies_movement.txt:1587](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1587>) |
| `ideology_slave_revolt_movement` | CIT | disapprove | neutral | [03_ig_ideologies_movement.txt:1640](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1640>) |
| `ideology_meiji_restorationist_movement_shojoi` | EDO | disapprove | approve | [03_ig_ideologies_movement.txt:1676](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1676>) |
| `ideology_meiji_restorationist_movement_daijoi` | EDO | disapprove | approve | [03_ig_ideologies_movement.txt:1725](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1725>) |
| `ideology_tokugawa_loyalist_movement` | EDO | approve | strongly_disapprove | [03_ig_ideologies_movement.txt:1780](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1780>) |
| `ideology_tokugawa_loyalist_movement_2` | EDO | approve | disapprove | [03_ig_ideologies_movement.txt:1832](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt:1832>) |

## 附录B：本计划补充来源指纹

通用44项源码/引擎来源见前置审计报告；下表追加本计划实际新查的来源与将要作窄差异基线的文件。

| actual source | SHA-256 |
|---|---|
| [00_ig_ideologies.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt>) | `4c8bc020d2d1060795e5a615b850736b731a31193862399363ec2e1829639b05` |
| [00_ig_ideologies_event.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_event.txt>) | `9821d1dceb526c700eeb2a6351355bf2745004c747744bb8c855e1b1cd6e9f36` |
| [00_ig_ideologies_flavored.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt>) | `68b24613022a7d879337bd2a0c190c7c140b4c0ae2bd6db67770aaecdca87610` |
| [03_ig_ideologies_movement.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/03_ig_ideologies_movement.txt>) | `063a0a979aac9c4f3d721da16866ce242e7b786c8b0ae7de1f54b9c8a05b4a92` |
| [01_character_ideologies.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/ideologies/01_character_ideologies.txt>) | `ea56543e49d9b25361f522d496b557413a8de62b2359a868aff3987f1a01128f` |
| [00_cultural_heritages.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/discrimination_traits/00_cultural_heritages.txt>) | `06d6638c64c1185a3e8a01102958bfaa5ef57a9c657bf82528cd89f4ec622443` |
| [00_victoria_ip3_scripted_effects.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip3_scripted_effects.txt>) | `50ebf064dc069c7f157b0bb9b46cc96902c8121d6f4dc5a0f21583c1625f4c3d` |
| [peoples_springtime.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/peoples_springtime.txt>) | `455fae01670912ad67900745655e91cd926b0ecbd1ac05a30cea001c9cb5ea21` |
| [politics_panel_constitution.gui](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/politics_panel_constitution.gui>) | `2432432a4d9a63cc52f8dcd392767fa48495f123920e7e77f5f999a3e894b457` |
| [culture_panel.gui](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/culture_panel.gui>) | `17f02494fe2e797d75750493d368441a446128f891bb149947c759fd1959f295` |
| [com_gui_society_panel.gui](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3385002128/gui/com_gui_society_panel.gui>) | `bb567e3e92c47f9cbd49be401ebd3ea0711866feea83ed30841bbd1e9057100b` |
| [HUS.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-canon-route-execution-20261104T080559Z/mod/common/history/countries/HUS.txt>) | `cb1485aa1ec06d0706806a9dbbdb6ab458ea78cbf796ac506a2482c6ecb33608` |
| [HUS.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/countries/HUS.txt>) | `3c37f1c75bdf0b18f4adc877ad2b94103840302d227ef89cdbc47c181187c639` |
| [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/laws/nesnd_hus_registration.txt>) | `d1cea0a8f06d6815ecf3d0e42ceec53add6ee5347215b11c5a45e6510e235343` |
| [zzzz_nesnd_hus_citizenship_lock.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/laws/zzzz_nesnd_hus_citizenship_lock.txt>) | `f27fa12c8ee7ebe3a2a4e48b30e971278d8c31677172cfb5db3c27ba330d3f40` |
| [effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>) | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |

### 7.5 revision source fingerprints

Source-only read, no gameplay changes or tests.

| Source | SHA-256 |
|---|---|
| [00_code_on_actions.txt:L5154](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5154>) | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |
| [independence.txt:L30](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/independence.txt:30>) | `a1c098c8f1a00f6b112f6fcb2079b87bd209c6a771032218487f63b13ce2960a` |
| [india_decisions.txt:L42](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/decisions/india_decisions.txt:42>) | `310cfdd220e1f3e8673801cff342bd5fd12334fe2d4dbbfe821ea943316eaf0e` |
| [00_on_actions_yearly.txt:L569](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_on_actions_yearly.txt:569>) | `f520f18901e7136794d72e9647311ea5abb430e45ded311316138e1228c5ef1b` |
| [event_targets.log:L959](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:959>) | `cc12b15da310d0d8ef10a9209107b4d2298a882fa6ee038c202650e3c9bd7c71` |
| [effects.log:L36891](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:36891>) | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |
| [triggers.log:L10350](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:10350>) | `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e` |
