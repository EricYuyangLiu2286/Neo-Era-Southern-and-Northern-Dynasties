# 西秦政治日志：本机原生接口研究

2026-11-02；只读研究。`catalog.py status`：Victoria 3 **1.13.11 / build 24799966**，CURRENT，changed_count=0。未打开游戏；以下为源码/API证据及明确标注的实现建议，**不是引擎验收**。只新建本报告，没有修改 MOD、GAME、技能或存档。

路径缩写：

- GAME = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`
- MOD = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`
- DOC = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031`

## 需要先解决的三处接口事实

1. **−50～50可以直接存入原生进度条，无需偏移。** GAME `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt:3–12` 的 `je_ryukyu_rivalry_score_bar` 为 start=0/min=−40/max=40；`00_ip4_carlist_wars_progress_bars.txt:3–12` 为 −10～10。负数不是仅在本地化展示的假象。
2. **比例代表制有本地化，没有可用的原生法律定义。** GAME `localization/simp_chinese/laws_l_simp_chinese.yml:430–431` 和 `localization/english/laws_l_english.yml:609–610` 有 `law_proportional_representation`；对 GAME 所有 `.txt/.gui/.md` 及 MOD `common` 搜索此标识，无定义或执行引用。不能直接 `activate_law = law_type:law_proportional_representation`；`law_proportional_taxation` 是比例税制，不能代替。若实现，必须真正新增法律，并明确其机制。
3. **专制与技官制同组，不能作为两条同时生效的法律。** GAME `common/laws/00_distribution_of_power.txt:5–6,240–241` 均为 `lawgroup_distribution_of_power`。`law_corporate_state` 则是治理原则（`00_governance_principles.txt:919–920`），所以“合作主义国家＋专制”的跨组组合成立。“皇权＋技官”要用君主制＋原生技官制，或有明确行为的自定义法律变体，不能按顺序激活专制和技官制后声称两者并存。

## 统治者、初始化和逐王偏好

完整原生调用点为 GAME `common/on_actions/00_code_on_actions.txt:3146–3184`：`on_ruler_selected` 的 root 为 **新统治者 character**，`scope:previous` 为原统治者。实际 effect 直接进入 `root.owner` 国家并设置变量（3150–3152）。在这个 on_action 内不可把 root 当 country；国家检查/加 JE 放 `owner` 中，人物偏好/一次标记放人物上。DOC `on_actions.log:1145–1147` 的泛化 `Expected Scope: none` 与原生注释/实际调用形状不一致，本研究依据实际代码的 character→owner 链，保留实测边界。

GAME `00_code_on_actions.txt:1–13`：`on_game_started` 和 `on_game_started_after_lobby` 无 root；后者只在每个 campaign 首次从大厅入局时触发。因而首王初始化不应只依赖未知的 history/ruler_selected 执行顺序，也不能把 after_lobby 当通用读档恢复事件。

MOD `common/history/characters/QE1 - Western Qin Empire.txt:1–10` 明确生成 `QE1_chen_wuxing`、`QE1_chen_chuguo`；`common/character_templates/zz_historical_leaders_ce_asia.txt:1259–1291` 明确前者 ruler、后者 heir。**首王可由 `has_template = QE1_chen_wuxing` 固定经济偏好**，无需靠“第一次触发回调”推测谁是首王。继任者只在本人未有偏好标记时执行 `random_list = { 60 = { ... } 40 = { ... } }`；DOC `effects.log:28893` 定义 random_list 为只选一项的加权随机效果。人物持久标记避免读档、重复回调、废黜复辟重新抽签；国家可以缓存当前王偏好供条公式使用。

建议初始化闭包：父 JE `immediate` 调统一的“确保状态存在”效果；首王分支固定经济，其他王分支一次60/40；`on_ruler_selected` 在 QE1/有效父JE/未终局守卫下更新缓存；父JE周脉冲对比当前 ruler 对象作为恢复/漏回调保障。初始化标记和 running 分开；不因恢复补子JE而把余额、偏好或计时归零。该组合是源码支持的设计建议，尚未实际触发测试。

## 原生进度条完整链条

- 定义：GAME `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt:3–12`。
- 挂载：GAME `common/journal_entries/01_ryukyu_rivalry.txt:1–6` 同时挂两个 `scripted_progress_bar`；一个 JE 可以有主平衡/其他独立条。
- 判定：同 JE `:96–102` 比较 `scope:journal_entry = { "scripted_bar_progress(je_ryukyu_rivalry_score_bar)" >= 40 }`；`:183–191` 对 −40。这里的数值是**绝对条值**。
- 写入：DOC `effects.log:36789–36792`：`set_bar_progress = { name = key value = N }`，scope 必须 journal_entry，示例本身使用 −5。DOC `triggers.log:14102–14107` 同样把 scripted_bar_progress 限于 journal_entry。
- UI：GAME `gui/journal_entry.gui:262,283,305,343,416,505,594` 绑定 `JournalEntry.GetCurrentBarProgress(ScriptedProgressBar.Self)`；`GetCurrentBarValue` 用于绝对读数，可参 GAME `localization/english/agitators_1_l_english.yml:65–69`。不要把百分比进度函数当−50～50的读数。
- 顺序：GAME `common/scripted_progress_bars/scripted_progress_bars.md:8–21` 定义 min/max/start，并说明 weekly/monthly/yearly bar 更新先于同周期 JE pulse。原生明细用 `add = { desc = key value = ... }`。不要 bar 自动累积后再把增量加入读取值一次。

候选可以 `start_value = 0 min_value = -50 max_value = 50 double_sided_gold = yes`；double_sided_gold 是同 md 已列样式。琉球/卡洛斯的专用样式包含各自美术，不应为了负值照搬。国家变量如需用于跨JE/按钮/保存，只设一个权威来源并统一绝对同步。按钮预览中对 JE 对象和国家变量分别分支守卫；`visible/possible` 不保证 effect preview 已初始化。

**“端点持续超过4周”的计时注意：** GAME `common/journal_entries/00_meiji_restoration.txt:79–107` 有条件满足计数+1、否则重置为0的原生连续计时。可在父JE周脉冲建立正、负两计数，离开端点立即清零，切边也清零。严格时间语义下“五次观察”只相隔四周：若第一次观察就设1，`>4` 会在28天时成立。若必须严格大于28天，可首次到端点置0，以后每完整周+1，`>4` 为35天；或记录端点进入期限并在期限后复查。对正文中“超过四周”的解释应与此实现一致。不要让超时与端点结算各发一次奖励；所有出口共用一个提交标记与清理效果。

## 父子JE、晚启动、超时和失效

GAME `common/journal_entries/journal_entries.md:1–57` 说明普通country-context JE root是所属国，`scope:journal_entry` 是JE，`scope:target` 是 add_journal_entry 的目标。`is_shown_when_inactive` 和 `possible` 在显式 add 时均被忽略；`immediate` 仍执行。因此子JE可保持不自动显示，**由父JE显式 add**，而不是只写一个默认无法激活的 possible。DOC `effects.log:250–253` 给出 `add_journal_entry = { type = key target = scope }`；其 Supported Scopes:none 是泛化标注，原生 country 调用证据见下。

完整父子实例：GAME `common/journal_entries/00_sick_man.txt:1–34` 为有超时/终局的主JE；`:95–164` 子JE在完成时更新国家主进度（111–115）、必要时 `add_journal_entry = { type = je_sick_man_egypt }`（152–154），并用父结算变量失效（159–164）。推荐本任务用**实际 `has_journal_entry = 父JE` ＋终局标记**约束孩子，避免永久历史flag撑住孤儿子JE；补齐子JE用 `NOT has_journal_entry`，保留已存在进度。

晚启动原生实例：GAME `common/laws/00_distribution_of_power.txt:247–258` 在技官法启用时显式加入 `je_technocracy`；GAME `common/journal_entries/05_technocracy.txt:6–23` 也有科技/法律触发的自动入口及 immediate，说明 JE 不限新开局。`:66–70` 废除技官制使其失败。本任务采用已授权的后续政治节点激活三派JE，不能无条件将新日志放开局历史。

GAME `journal_entries.md` 在 timeout 段明确单位是天；GAME `common/journal_entries/00_art_jes.txt:45` 实际使用 `timeout = 3650`。这可做10年名义期限；它是3650天，并非逐日期跨闰年的“第10个周年”。主JE超时由 `on_timeout` 收尾（完整例为 `00_sick_man.txt:23–34`），所有 complete/fail/timeout/invalid 均清临时修正、子JE运行许可、计时及 pending请求。

DOC `event_targets.log:1304–1307`：`num_states` 输入country、输出value，含当前该国拥有的states，不是 state_region 数或只算已整合州。故父项目 `num_states < 4`；三派后期项目 `num_states < 5`。后者另以 `has_law_or_variant = law_type:law_universal_suffrage` 或 `law_council_republic` 失效。若采用 census parent 的自定义比例代表法律，不应被 universal_suffrage 条件误伤。

## 数值修正：单位、scope与实际例子

| 需求 | 已核接口与语义 | 源码闭环 |
|---|---|---|
| 特定IG吸引力 | 国家修正内 `interest_group_ig_intelligentsia_pop_attraction_mult` 等；0.1是+10%吸引力，非+10影响力点 | GAME `events/iberia_events/philippines_events.txt:661–664` country add_modifier → `common/static_modifiers/00_ip4_03_modifiers.txt:66–70`；DOC `modifiers.log:7337–7338,7373–7374` |
| 特定IG政治力量 | 国家修正内 `interest_group_ig_armed_forces_pol_str_mult = 0.25` 等 | 同 events `:473–478` → 同 static_modifiers `:24–27`；DOC `modifiers.log:7333–7334,7369–7370,7381–7382` |
| 已进入单个IG的修正 | `ig:ig_x = { add_modifier = ... }` 中定义用通用 `interest_group_pol_str_mult`、`interest_group_pop_attraction_mult`；不要把角色loyalty当作集团政治力量 | DOC `modifiers.log:1199–1210` mask=interest_group；GAME `common/static_modifiers/00_ep2_05_modifiers.txt:11–14` 同时给吸引−25%/力量−10% |
| 立法速度 | `country_law_enactment_speed_mult`，0.5=+50%速度；不是+50成功率，也不能宣称精确减半周期 | GAME `events/japan_events/ep2_meiji_restoration.txt:625–626` 给JE加 `modifier_meiji_interregnum` → `common/static_modifiers/00_ep2_04_modifiers.txt:7–13`；DOC `modifiers.log:719–722` |
| SoL变动的忠诚/激进产生 | **只有合并接口** `state_radicals_and_loyalists_from_sol_change_mult`；正值同时放大两个方向。当前导出没有只放大SoL忠诚、同时只压低SoL激进的独立接口 | GAME `common/journal_entries/07_tenpo_crisis.txt:9–10` modifiers_while_active → `common/static_modifiers/00_ep2_02_modifiers.txt:1–7`；`common/modifier_type_definitions/00_modifier_types.txt:2335–2342` percent=yes；DOC `modifiers.log:1875–1878` mask=state |
| 固定合法性 | `country_legitimacy_base_add = N` 是基础合法性加点，不是 `country_legitimacy_govt_total_clout_add` | DOC `modifiers.log:739–742`；GAME `common/static_modifiers/00_code_static_modifiers.txt:315,324,336,346` 真实+10/+5/−10/−20 |
| 军需商品成本 | `country_military_goods_cost_mult`；负值降低成本，0.1=+10%成本；不生成枪械/大炮实物，不提高市场供给 | GAME `common/interest_group_traits/00_armed_forces_traits.txt:20–26,38–44`；`common/modifier_type_definitions/00_modifier_types.txt:526–533` percent=yes/color=bad；DOC `modifiers.log:851` |
| 攻防 | `unit_offense_mult`, `unit_defense_mult`；陆军限定可用 `unit_army_offense_mult`, `unit_army_defense_mult` | GAME `common/interest_group_traits/00_armed_forces_traits.txt:1–8` 国家集团特质+10%攻防；`common/static_modifiers/00_code_static_modifiers.txt:453–454` 陆军限定+15%；DOC `modifiers.log:2019,2035,2043,2091` |

**政治力量不等于clout的固定点数。** GAME `localization/english/concepts_l_english.yml:854,1445` 定义clout为某IG占全国总政治力量的份额。若只给一组+25%政治力量，原clout为20%、没有其他变动时，新份额的简化算式为 `20×1.25/(80+20×1.25)=23.81%`，不是45%。派系进度可以读取/由IG clout推进，但不得把这个修正本地化为“影响力增加25个百分点”。IG底层吸引规则还取决于职业/识字/领袖人气，例如 GAME `common/interest_groups/00_intelligentsia.txt:399–446`。

如果用户想分别控制SoL激进/忠诚，两种独立 `country_radicals_from_legitimacy_mult` / `country_loyalists_from_legitimacy_mult` 虽然存在（DOC `modifiers.log:823–826,943–946`），却针对合法性来源，不能冒充SoL。应使用合并的真实SoL效果并准确说明，或另做有明确定义的事件系统；不得编造旧版modifiers。

## 法律与科技条件

| 法律 | 法律组 | 科技 | 重要前置或副作用 |
|---|---|---|---|
| `law_autocracy` | distribution_of_power | 无unlocking_technologies | 禁止 parliamentary_republic；on_activate消除政党并清投票强度修正；GAME `00_distribution_of_power.txt:5–50` |
| `law_technocracy` | distribution_of_power | `central_archives` | 启用时选举官僚→任命官僚，移除政党、清投票修正、加入原生技官JE；同文件`:240–289` |
| `law_corporate_state` | governance_principles | `corporatism` | 调 `transition_off_of_monarchy_effects`；独立特许公司不可普通enact；GAME `00_governance_principles.txt:919–975` |
| `law_presidential_republic` | governance_principles | `democracy` | 同公司限制；调退君主制效果；同文件`:334–394` |
| `law_census_voting` | distribution_of_power | `democracy` | 禁止chiefdom/command_economy；识字与财产资格投票；启用有electoral_confidence/caciquismo/政党钩子；GAME `00_distribution_of_power.txt:886–958` |
| `law_universal_suffrage` | distribution_of_power | `egalitarianism` | 禁止chiefdom/command_economy；同文件`:1017–1038` |
| `law_council_republic` | governance_principles | `socialism` | 同独立公司限制；退出君主制；GAME `00_governance_principles.txt:789–807,842` |
| `law_proportional_representation` | 当前不存在 | 当前不存在 | 只有loc，不存在可沿用的原生科技/前置 |

科技数据库闭环：GAME `common/technology/technologies/30_society.txt:100–119` democracy(era1，前置rationalism)；`:377–393` egalitarianism(era2，前置democracy)；`:537–552` central_archives(era2，前置centralization)；`:1022` socialism(era3)；`:1073` corporatism(era3)。按钮应直接列 `has_technology_researched`，实际effect再检查相同门槛；`activate_law` 是country→law_type立即启用效果（DOC `effects.log:12–15`），不能假定普通立法流程会替按钮检查所有科技条件。

退君主制不是单一名义切换：GAME `common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2647–2676` 调整王室土地和法律、将宪政主义IG换共和意识形态，并加 `je_abolish_monarchy`。实现“和平改法”可以不人为创建战争，但不能承诺原生IG/运动反应完全消失，也不应随意删除原生法律on_activate闭包。

## 法律变体：继承范围与两种候选

原生变体的可靠接口：`parent = law_key`。GAME `common/laws/00_bureaucracy.txt:54–89` 的crownland_diets及 `02_welfare.txt:29–55` 的chiefs_distribute_aid均注释 **Inherits ideological stances from parent**；它们显式定义group、icon、modifier和必要效果。GAME `00_governance_principles.txt:290–332` 的colonial_administration是monarchy parent，依然显式提供独立modifier、can_enact和空on_activate。因此不能凭parent断言自动继承了母法数值、科技、可用条件、on_activate或引擎政府类型。

`has_law_or_variant` 则明确支持母法及变体：DOC `triggers.log:10471–10476`。原生distribution变体实例：GAME `00_distribution_of_power.txt:114–194` bakufu(parent autocracy)，`:196–238` neo_absolutism(parent autocracy)，均显式写其修正/启用钩子。

### A. 新增比例代表法

可新增独立定义（建议带NESND前缀）并 `parent = law_census_voting`，而不是不存在的`law_census_suffrage`。作用为distribution_of_power中的秦国专用、识字/财产资格下的比例代表制度，维持用户要求普选一旦通过则退出三派政治；若选universal parent，`has_law_or_variant universal_suffrage`会使刚进入的改革立刻失效。

这只是可行实现选择，不能宣称Victoria引擎因此增加了真实席位按比例分配算法。若要体现多党妥协，明确写更适合联合政府的合法性规模/意识形态惩罚数值；原生census现有 `country_legitimacy_govt_size_add = 1`、`country_legitimacy_ideological_incoherence_mult = 0.1` 可作量纲参考。投票参数必须显式写入，因为 GAME `common/scripted_triggers/00_scripted_triggers.txt:16–40` 的 `country_has_voting_franchise` 检查的是实际投票修正，不检查parent名字。

显式保留真正适用的census启动链：`initialize_electoral_confidence`（按其game_date/franchise条件），在新法律自己的 `random_law { limit { type = law_type:新法 } save_scope_as = relevant_voting_law }` 后调用 `handle_possible_absent_caciquismo_variables`、`scripted_effect_parties_emergence`、`inherit_caciquismo_effect`、`inherit_free_elections_effect`。来源 GAME `00_distribution_of_power.txt:927–944`；辅助函数 `common/scripted_effects/00_victoria_ip4_scripted_effects.txt:1808,1823,1878,2528`。不能留下random_law仍选原census，否则相关law scope可能为空。法国/日本/英国特殊剧情无需照搬。可在新法中显式加democracy（原census母法科技）；新增更晚的科技门槛属于设计，不是原版事实。

### B. 君主制变体“皇权技官制”＋专制

用 `group = lawgroup_governance_principles parent = law_monarchy` 的新法，与 `law_autocracy` 跨组配套，属于原生格式允许的候选。显式写 `central_archives` 解锁、君主法需要的合法性/authority基线及技官职业政治力量（参原技官 academics/engineers/officers各0.33）。避免同时把原生technocracy的整套国家修正加进来又保留autocracy，尤其clout legitimacy 120和authority会重复叠加；数字必须作为本MOD设计核算。

此变体**不等同于激活原生law_technocracy**：原生技官JE与某些精确法检查不会自动认它。若保留任命官僚含义，显式按 `00_distribution_of_power.txt:247–254` 转换；无需无意触发原生je_technocracy然后立即因精确法不符而失败。

必须处理君主身份的闭包：GAME `common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt:13–18` 的 `country_has_monarchy_law` **只精确列出monarchy/social_monarchy**，不是has_law_or_variant。新变体不会自动满足它；`:20–28` 的非君主helper也是精确列表。因此不要只检查自定义日志而忽略原生摄政（`common/government_types/01_regencies.txt:12,42,71,...`调用该helper）。MOD `common/government_types/00_ce_government_types.txt:1–67` 用has_law_or_variant monarchy，且明定transfer_of_power=hereditary及前后change_to_hereditary钩子，能为秦的既有汉文化君主政府提供识别路径，但尚不能替代完整继位/摄政验证。

较小而稳妥的实现是保留原生monarchy，选择原生technocracy，用按钮/日志叙事表达皇权主导；若产品要求必须同时保留专制法标识，则采用上述自定义治理变体，并把涉及新法的君主helper识别、政府类型与继承路径纳入实际改动/验收。不要用parent等于monarchy就自动证明“与原生君主完全同等”。

## 本任务最低验证边界

外部闭包检查至少涵盖：负值bar引用与端点计时；第一王固定、继任一次抽签、旧档已有王不反复重抽；父JE补齐子JE而不清零；每一出口清理和少于4/5州失效；按钮visible/possible/effect三层科技法条件一致；比例代表新法确有定义及投票参数、relevant_voting_law指向自身；皇权变体继承/摄政helper不漏；同一政治力量和SoL修正不伪装为其他量纲。真实新法激活、原生on_activate顺序、UI负数与hover、存读档、继位与端点周序都仍为ENGINE_NOT_RUN。

## 补充：SoL上升增效忠、下降增激进的分向采样实现

本节回应后续实施研究：**可以在不使用合并modifier、不改动实际财富的前提下，按采样到的SoL升降分别调用原生效忠／激进效果。** 它是有明确计算公式的脚本加成，不是引擎内部“来自SoL”的逐次精确乘区。前文“只有合并接口”仅指现成modifier；不表示脚本无法表达单向效果。

### 能读什么、能改什么

| 接口 | 精确scope与含义 | 来源 |
|---|---|---|
| `standard_of_living`、`wealth` | pop数值，不能在state直接当全国/全州平均值读取 | DOC `triggers.log:14307–14312,14800–14805` |
| `total_size` | pop全部人口；用于人口权重比仅用workforce更接近效果作用的人群分母 | DOC `triggers.log:14659–14664`；`workforce:14829–14834`、`dependents:9672–9677`也可分别读 |
| `pop_loyalist_fraction`、`pop_radical_fraction`、`pop_neutral_fraction` | pop当前三种比例，不能拆出“本月因为SoL增加的比例” | DOC `triggers.log:13574–13593`；其中loyalist英文说明误写Radicals，原生 `common/political_movements/04_country_specific_ideological_movements.txt:2522` 实际读取pop_loyalist_fraction，另见 `00_ideological_movements.txt:3116` |
| `loyalist_fraction`、`radical_fraction` | country/state的带筛选比例trigger，可筛pop_type/strata/culture/religion | DOC `triggers.log:12810–12815,13957–13962` |
| `add_loyalists`、`add_radicals` | country effect，value为每个匹配pop向该方向移动的人口比例；0.0045是0.45%，不是0.0045人 | DOC `effects.log:277–290,367–380` |
| `add_loyalists_in_state`、`add_radicals_in_state` | state effect，同样按匹配pop人口比例；支持可选pop_type/strata/culture/religion/interest_group，pop_type与strata不可同时指定 | DOC `effects.log:292–305,382–395`；GAME `events/assassination_events.txt:343–358` 为upper阶层10%效忠/5%激进实际例 |
| value内脚本运算 | 可用 `value = { add = N multiply = 脚本值 }`，不局限字面常数 | GAME `common/scripted_effects/00_chris_scripted_effects.txt:43–48`，以及 `events/iberia_events/ip4_coup_events.txt:537–544` |
| `add_pop_wealth` / `set_pop_wealth` | pop effect，`wealth_distribution`是真实财富，`update_loyalties`控制财富操作是否更新效忠；不是独立的loyalty setter | DOC `effects.log:341–345,37090–37094`；GAME `common/scripted_effects/00_starting_pop_wealth.txt:7–37` 实际set wealth且update_loyalties=no |

本次完整effects导出未找到pop直接加效忠／激进的effect；`update_loyalties`是上述wealth效果参数，未找到可独立调用的effect。不能将 `add_loyalists_in_state` 放pop scope，也不能创造 `add_pop_loyalists`。从pop跳state是合法的（DOC `event_targets.log:330–333`），但在每个pop循环内对整个state或整个同职业群体都调用一次，会重复作用于其他pop，必须先聚合再每个目标群体调用一次。原生on_actions及导出也未找到SoL/财富变化逐次回调。

不建议“加一点财富且update_loyalties=yes，再减回来且no”这类办法：它实际改动财富分布，会经过财富等级/需要/SoL修正及取整等环节；没有当前已启用的原生示例证明可无副作用地实现纯忠诚奖励。GAME `events/test_events.txt:166–186` 的财富测试只是注释，甚至含未导出的旧set_pop_happiness，不能当生产接口证据。

### 本机原生基线

GAME `common/defines/00_defines.txt:1382,1463–1466` 的NPops：默认 `DEFAULT_SOL_CHANGE_IMPACT_FACTOR = 0.03`；SoL15以上开始缩减，SoL30达到最大缩减，`SOL_CHANGE_IMPACT_FACTOR_REDUCTION_SCALE = 9` 意味着高端除以10。GAME `common/pop_types/peasants.txt:14` 用 `sol_change_impact = 0.01` 覆盖默认；本轮搜索全部原生pop_types仅此职业覆盖，MOD common未找到该参数或上述defines覆盖。

因此最基础的“+15%上升效忠”不是每升1点就给全国15%效忠，而是一般人口 `0.03 × 1 × 0.15 = 0.0045`（额外0.45%人口向效忠移动）；农民则为0.0015。若“+10%下降激进”，对应一般人口额外0.003、农民0.001。在SoL30以上相应额外影响约再除以10。100,000名非农人口由10升到11，估算额外效忠方向移动450人；同量农民150人。下降1点的10%激进加成分别约300、100人。实际最终人数还受已有忠诚状态、饱和、取整及引擎对effect的处理影响。

脚本可读取 `define:NPops|DEFAULT_SOL_CHANGE_IMPACT_FACTOR` 等数值defines；这一路径格式有 GAME `common/script_values/war_exhaustion_values.txt:57` 和 `cultural_community_values.txt:256` 的实际NPops使用。未找到暴露pop_type.sol_change_impact数值的event target，所以农民0.01分支应明确登记为已核源码值并列入版本检查，而不是虚构动态读取接口。

可选的高SoL缩减近似公式：`r(S) = 1 / (1 + 9 × clamp((S − 15)/15, 0, 1))`。**15/30/9和两端行为是源码事实；中间线性插值及采用月末S是建议近似，defines注释没有给完整C++算法。** 不应声称已复现引擎每一步。直接忽略缩减会在SoL30人口上把额外奖励放大到约10倍，不宜这样实现。

### 建议：州×职业的月度单向奖励

以每个州、每种pop_type为一个群体，把缓存放在state上，较逐pop永久缓存更容易应对人口合并、拆分、就业变更和迁徙。country/state→`every_scope_pop`已由DOC `effects.log:4762–4766`支持；原生`set_variable`支持对象变量及到期天数（`:37194–37202`），但本次未找到可靠的原生pop永久变量实例或变量如何随pop合并继承的契约，因此不把它当已验证前提。

群体k的实际算式（数学表达，不是可直接粘贴的Jomini）：

```text
N_k(t) = sum(total_size_i)
S_k(t) = sum(total_size_i × standard_of_living_i) / N_k(t)
F_k(t) = sum(total_size_i × f_type_i × r(SoL_i)) / N_k(t)
ΔS_k = S_k(t) − S_k(t−1)
extra_loyal_fraction_k = max(ΔS_k, 0) × F_k(t) × 0.15
extra_radical_fraction_k = max(−ΔS_k, 0) × F_k(t) × 0.10
```

对k只调用一次 `add_loyalists_in_state = { pop_type = 对应类型 value = 对应额外比例 }` 或radicals对应效果；两种奖励各受自己的限时国家buff/flag守卫。未授权该方向的效果为0，不能用合并modifier使另一方向跟着增长。若只做州平均，则用人口加权F避免把农民当普通3%，但同州不同职业升降相抵的误差更大。

这里0.15/0.10为当前任务指定的候选倍率，不是原生固定值。它们为**额外部分**，不能乘1.15/1.10再全部发一次，因为原生SoL机制已产生基础部分。若设计要求的是降低某方向而非额外增加，可使用带负value的对应state效果；原生 `events/balkans_events/montenegro_events.txt:297–299,313–315` 有 `add_radicals_in_state value=-1`，但这种补偿也会移除已有的其他来源激进者，仍不能伪称精确减少了SoL来源。

生命周期：buff授予时记录当时基线，不支付首样本；以后每次月脉冲只在buff仍有效、州仍属于原country、群体人口>0且缓存属于本次buff时支付，然后更新基线。新获得州/新增职业群体只建基线，避免把没有历史值当0造成巨额奖励。state_owner_change或buff结束清本轮缓存；重复授予同一buff不应追溯重付。若buff在月中到期，要先做最后一次结算再移除，或明确放弃末尾不足一月的差额；不能到期后继续付钱。所有缓存读取仍需真正分支守卫。

### 可量化的近似与未验证部分

- 每月取端点只能看到净变化。一个群体月内10→11→10，采样额外为0，逐次增强本应分别产生一次正、负加成。月度延迟最多约一个月；周度可把时间误差降到约一周，但不能消除月内往返或群体构成变化。
- 相同职业在一州内存在多个工作地点/文化/宗教pop，平均上升与下降会互相抵消；迁入高SoL人口或职业转换也会改变均值，即使留在原群体者没有变富。按州×职业改善但不消除这个问题。若细分到文化×宗教，目标和缓存复杂度增加，仍不获得单pop effect。
- state effect把比例分配给该职业当前所有pop，因此不保证只奖励真正变富的那批人。不得把循环中的每个pop都再次当整个职业群体支付。
- 原生缓冲规则存在：GAME `00_defines.txt:1401–1403` 对short/long/extra_long给出1837/1841/1846终点，`common/game_rules/00_game_rules.txt:77–94` 默认none。defines只说按时间缩放，未给完整缩放算法；启用缓冲的游戏中不能宣称本公式是当时原生结果精确增加15%/10%。同样，文化接纳等已有忠诚增长修正与effect饱和顺序仍需引擎核对。
- 低于预期SoL的持续激进（`00_defines.txt:1404,1406`）、歧视、饥饿、合法性等均不是“SoL变化”，本公式不将其当奖励基数。直接拿 `pop_radical_fraction(t)-旧值` 或总忠诚变化乘倍率会混入这些来源，不能这样替换。

建议交付说明使用“按州内各职业每月生活水平净变化，额外产生效忠／激进倾向，按原生基础系数计”的准确范围；不能只显示一个不存在的原生SoL单向modifier。以上接口及数学量纲已核，实际采样结果、性能、缓存存读档、上限和偏差均为ENGINE_NOT_RUN。

## 本次读取的关键原生文件指纹

均为SHA-256，用于后续判断报告是否仍对应当前源码。

| GAME相对路径 | SHA-256 |
|---|---|
| `common/on_actions/00_code_on_actions.txt` | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |
| `common/laws/00_governance_principles.txt` | `e676448ea64c17079677ddbf2cbfdbec0ffdefa465286f16c1e6107a14e7f4cf` |
| `common/laws/00_distribution_of_power.txt` | `014b5fcb89d4e4abb86c98c013364117a183daf569c9cb8d4ab0bb5ff833cd04` |
| `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt` | `1252cbb7eb15be91704ccdb99298ceb615927abfee6fb9ae3e2f893ac029d6cf` |
| `common/journal_entries/journal_entries.md` | `1032c0dac08d502d49380e05929912fa94ba3a3a6f2a6279b480d58ea7272323` |
| `common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt` | `4170ec272e2e4930d36534f9268a5e110e3223a8e94655f4c5a07dcb40e211c3` |
| `common/scripted_effects/00_victoria_ip4_scripted_effects.txt` | `f1c4691e8734d0872283abd184b538d25f4474e68f7b0790c75cf252e03fcc8e` |
| `common/modifier_type_definitions/00_modifier_types.txt` | `b07822b507cdf169cc7df5edd41214857a80d95ce6ba79de7d11e688a86a6dbe` |
