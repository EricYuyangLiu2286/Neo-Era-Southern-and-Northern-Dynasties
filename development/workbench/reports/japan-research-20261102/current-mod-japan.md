# 当前主 MOD 日本源码研究（2026-11-02）

状态：SOURCE_AUDIT / ENGINE_NOT_RUN。本轮仅研究，未改主 MOD、未启动游戏、未把历史数量推演为 GDP、财政余额、市场价格或生活水平。目录严格使用当前主 MOD + 当前 GAME 同路径覆盖；保序解析器保留重复 create_pop、create_building、option。GAME catalog status：1.13.11 / Steam 24799966 / CURRENT / changed_count=0。配套仓库只读核得 HEAD `a7b445ba515d0e4842fb36ba3e6094d54e046012`；主 MOD 本身无 Git 元数据，以下文件 SHA 才是实际研究对象指纹。

数据与方法：[current-mod-japan-data.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102/current-mod-japan-data.json>)；[可复跑的保序审计脚本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102/audit_current_mod.py>)。JSON 含每个人口块、每个建筑块及 PM、州归属、人物历史、原版继承军队、事件入边和逐文件 SHA-256。

## 1. 现有内容的边界

当前日本不是空白国家。它已有：丰臣开局与世系、独立后解锁开国按钮、1840/1846 两次政治继承分歧、明吴参战与九州回报、战败吞并后恢复三国、东征外交博弈、林汉涵摄政、独立与九核心地区统一日志。未查到 MOD 专门的“军国化／幕府改革／民主化”三套长期路线，也未查到“统一但不含九州”的独立终局判定或日本对朝鲜三选一内政线；这些是设计接入空间，不能写成已有实现。

原版日本玩法仍由继承文件提供，须结合原版研究报告；本报告只说明实际 MOD 覆盖与联接，不能把原版现成终局原封不动套到丰臣、扶国和和国。主 MOD 明确禁用了原版琉球竞争 JE：possible、inactive/lobby 和 should_be_involved 都有 `always = no`。[common/journal_entries/CE_01_ryukyu_rivalry.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/CE_01_ryukyu_rivalry.txt:12>)

## 2. 开局国家、制度与疆域

JAP 是 recognized / empire，唯一主文化 japanese，首都 STATE_KANSAI；JTK 扶国和 JIM 和国均为 recognized / kingdom、主文化 japanese，定义首都分别关东和京都，开局没有历史领土。JAP 是 USM 的 tributary；剩余 KOR 是 CNE 的 tributary。[common/country_definitions/ce_countries.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:62>)；[common/country_definitions/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/nesnd_japan.txt:1>)；[common/history/diplomacy/ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:15>)；[common/history/diplomacy/ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:162>)

JAP 的完整州为东北、关东、东海、北陆信越、关西、京都、中国、四国；北海道为 JAP 3 province / EZO 21 province；九州为 JAP 2 province / USM 10 province。JAP 两个朝鲜州 BUSAN、YANGHO 均为未整合领土；剩余 KOR 持首尔、沙里院、平壤。萨哈林属 SHA，琉球属 RYU，不能把它们默认算作日本国土。来源：[common/history/states/00_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:6814>)（朝鲜）、[common/history/states/00_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:6869>)（萨哈林至日本诸州）。

开局法律包括君主制、幕府、传统主义、农奴制、世袭官僚、民族至上、锁国、地方警察、无学校、土地税、审查、闭关、intermediate_edo_system、warrior_caste；军队和地主入阁，警察机构1。科技使用 tier_3 起始效果，并再次列城市规划、中央集权、执法。DLC ep2 开启时添加 je_sakoku，对本州拥有州加5破坏并启动720天、强度5暴雨；天保危机 JE/事件与琉球竞争会员标记在本历史文件被注释。[common/history/countries/jap - japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/jap - japan.txt:2>)

财富与识字使用 low / middling 初始化效果；这不是全国精确均值。原版效果按职业与阶层分配，不能把 middling 起始基值0.35写成日本实测识字率35%。[common/history/population/jap - japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/population/jap - japan.txt:1>)；[common/scripted_effects/00_starting_pop_wealth.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_wealth.txt:120>)；[common/scripted_effects/00_starting_pop_literacy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:121>)。

**锁国是关键已有约束。** MOD 的 REPLACE:law_sakoku 可见性是日本主文化且拥有任一九州州块（与原版“最大州块”不同），保留只能在九州贸易、贸易容量−75%、科技传播−20%、禁主动外交博弈等修正。开局 JAP 确有九州小块和贸易中心，所以“丧失多数九州”不等于“开局绝无贸易入口”。未来若设计完全无九州的统一国或三国独立，需明确开国／贸易制度变化及实际法继承；仅改变日志标题不会自动解除既有贸易限制。当前分封只显式换 monarchy/autocracy，没有显式贸易法转换。[common/laws/ce_trade_policy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/laws/ce_trade_policy.txt:6>)；[common/scripted_effects/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan.txt:98>)；[common/scripted_effects/nesnd_japan_recovery.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_recovery.txt:52>)

## 3. 开局人口、产业与军队（静态历史账）

JAP 合计 **35,594,072 人**，其中 BUSAN+YANGHO **8,669,114 人**。其主文化仅 japanese，但人口文化组成是 japanese 26,793,854，korean 8,149,114，han 334,802，ce_wuu 226,200，manchu 90,000，ainu 102。上述是人物数，不是劳动力数。

| 实际所有者／地区 | 人口 | 脚本建筑等级合计 |
|---|---:|---:|
| JAP / STATE_BUSAN | 3,850,627 | 18 |
| JAP / STATE_CHUGOKU | 3,228,128 | 56 |
| JAP / STATE_HOKKAIDO | 34,006 | 2 |
| JAP / STATE_HOKUSHINETSU | 4,138,700 | 13 |
| JAP / STATE_KANSAI | 4,073,380 | 75 |
| JAP / STATE_KANTO | 5,223,276 | 42 |
| JAP / STATE_KYOTO | 1,437,948 | 14 |
| JAP / STATE_KYUSHU | 340,334 | 9 |
| JAP / STATE_SHIKOKU | 1,763,836 | 22 |
| JAP / STATE_TOHOKU | 2,492,432 | 41 |
| JAP / STATE_TOKAI | 4,192,918 | 19 |
| JAP / STATE_YANGHO | 4,818,487 | 16 |
| USM / STATE_KYUSHU | 4,835,880 | 53 |
| KOR / STATE_PYONGYANG | 4,112,828 | 20 |
| KOR / STATE_SARIWON | 1,820,102 | 27 |
| KOR / STATE_SEOUL | 2,918,978 | 40 |
| EZO / STATE_HOKKAIDO | 36,331 | 0 |
| RYU / STATE_RYUKYU_ISLANDS | 409,181 | 8 |
| SHA / STATE_SAKHALIN | 48,806 | 4 |

人口来源为 [common/history/pops/11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/pops/11_east_asia.txt:1769>)，建筑为 [common/history/buildings/11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/buildings/11_east_asia.txt:5881>)；逐块行号见 JSON。建筑等级用 explicit `level`（如存在），否则加总 add_ownership 中所有 `levels`，不合并重复块；例如东北三组铁矿5+5+4全部计入。表中的0表示没有显式 create_building，不能解释为没有自给建筑或游戏运行后不存在自动生成建筑。

JAP 合计327级显式建筑：兵营75、政府行政30、建设4、港口9、海防3、贸易中心4；工业有枪械4、造船4、纺织8、食品10、玻璃15、纸5、家具2；矿业有铁20、煤10、铅1、金1；伐木21，农林渔牧种植其余见 JSON。**没有显式 tools/steel/explosives/chemical/railway/university 建筑块；不能据此声称运行时市场必定断供。**

PM 已有差异：建设含 wooden 与 iron_frame；铁矿含 picks_and_shovels 与 atmospheric_engine，煤矿采用 atmospheric_engine；伐木含 simple_forestry 与 saw_mills；渔业含 simple_fishing 与 fishing_trawlers；枪械为 muskets，造船为 basic_shipbuilding，纺织 traditional_looms，兵营 pm_no_organization。行政 PM 同时存在 hereditary、professional、religious，必须按州原样保留审阅，不能根据国家世袭官僚法擅自统一。明确工业转型切口是投入品、资格、行政/税容、港口与贸易制度，而非凭脚本造 GDP。

军队继承 GAME 未被同路径覆盖的 `06_military_formations_asia.txt`：Edo_Guard_Army 26、Kinai_Guard_Army 20、Kyushu_Guard_Army 12，共 **58 个显式 irregular_infantry 单位**，均在东北亚 HQ。JAP 的75级兵营与58个显式编制是两类数据；这里不把差额判为故障，也不把兵营等级当作实测作战兵力。有效 JAP 历史块中没有显式海军编队，海防/港口不等于舰队；游戏自动补全与战时兵力须引擎观察。[common/history/military_formations/06_military_formations_asia.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/military_formations/06_military_formations_asia.txt:547>)

## 4. 现有日志、事件与终局调用图

| 入口 | 当前条件／作用 | 终局与边界 |
|---|---|---|
| `flavorUSM.400 → usm_civilwar.23` | JAP一次答复，添加 `ce_usm_cw_japanese_interest`；三选项设置支持中央、反吴、中立；AI基础权重45/30/25 | 是参战承诺层，不是后述政治面板四立场的同一组概率 |
| `ce_usm_cw_japanese_interest` | 等南朝settled；反对派胜者须完成改号/结算 | JAP反吴而吴胜：记败北并排队崩溃；支持中央且中央胜，或反吴且反对派胜：转交USM所持九州并独立；其他保留局势；非崩溃支进入crisis.41 |
| `nesnd_crisis.41` | 战后军政选项 | a：10年政府工资+5%、教育获取+3百分点、行政力+5%；b：5年authority+10%、军队支持+3、知识分子−5；没有建立三条长期改革路线 |
| `nesnd_japan_war_collapse` | 全局JE，吴与日本交战时激活；相关交战国可见 | 京都、关东两个JAP州块都被与JAP交战的敌国控制，或吴已确认败北事实，可启动吞并恢复；partitioned才完成 |
| `nesnd_wu_eastern_question` | 吴身份USM+南朝settled+JAP活着，未封卷 | 准备值财政/行政、陆军/合法性、海军/维护三项；送条件或维持旧约；仅一次 dossier |
| `nesnd_japan.1 → .2` | 日本接受分封 / 拒绝 / 请求保留统一；吴决定开战或认可现状 | 同意直接分封；开战使用dp_nesnd_eastern_intervention→wg_nesnd_japan_reorganization；日本有humiliation反要求；分封目标执行才改领土 |
| `nesnd_japan_reunification` | JAP/JTK/JIM，南朝settled，一次入场 | 独立且完整持有9核心地区；统一变量+10年行政力+5%、动乱影响−10%，.5通知；JTK/JIM改显示名“日本” |

调用源码：[events/flavorUSM_ce.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/flavorUSM_ce.txt:677>)；[events/usm_civilwar_events.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:2511>)；[common/journal_entries/ce_usm_the_last_days_of_ming.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:492>)；[events/nesnd_crisis_events.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_crisis_events.txt:222>)；[common/static_modifiers/nesnd_crisis_modifiers.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/nesnd_crisis_modifiers.txt:1>)；[common/journal_entries/nesnd_war_collapse.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_war_collapse.txt:1>)；[common/scripted_triggers/nesnd_war_collapse.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_war_collapse.txt:24>)；[common/journal_entries/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_japan.txt:1>)；[events/nesnd_japan_events.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_japan_events.txt:1>)；[common/war_goal_types/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/war_goal_types/nesnd_japan.txt:1>)；[common/diplomatic_plays/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/diplomatic_plays/nesnd_japan.txt:1>)；[common/static_modifiers/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/nesnd_japan.txt:1>)；[common/dynamic_country_names/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/nesnd_japan.txt:1>)。

东征不以1847年强制触发，当前按钮要求吴非负bureaucracy与net_total_income、合法性≥50、陆军投射不低于日本、海军投射不低于日本且非零、军舰维护满足≥0.9；双方不在战争/已投入博弈、无相互停战。直接分封前还要求丰臣君主统治、JTK/JIM未存在、日本为独立或吴属国，且日本完整持有关东、京都、关西、中国四地区。当前完整统一需要九州和四国；北海道、朝鲜、琉球都不在9州完成条件。[common/scripted_triggers/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_japan.txt:2>)；[common/scripted_buttons/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_japan.txt:1>)；[common/script_values/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_japan.txt:7>)。

**政治面板与和平交涉是另一个真实存在的层。** 已登记且立场为0的日本成员AI，初始面板立场权重为保明30、拥吴10、中立15、自主45；每3月可审查，既有立场一般不会重新掷同一随机表，吴欠债或明宗主失去合适君主等会改中立。JAP/JTK/JIM均属日本政治成员；新计划数字不能覆盖这里的当前读数。[common/scripted_effects/nesnd_south_political_ai.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_political_ai.txt:61>)；[common/scripted_effects/nesnd_south_political_ai.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_political_ai.txt:124>)；[common/scripted_triggers/nesnd_south_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_politics.txt:117>)。

当前和平吴约并不是“归还九州”：`nesnd_south_accords.1.c`接受吴方约定，写入`nesnd_south_accepts_japan_concession`，有效协定36个月、立场冷却6个月。吴和平结算调用`nesnd_south_japan_consented_cession`，把签约日本国实际持有的九州、四国州块交吴。可割让条件要求有效吴约、和平、同意；需要有非割让州留存并保护本国非敌占控制，必要时迁政治/市场首都。这个“战时胜利索还九州”与“战前拥吴和平割让九州/四国”方向相反，后续路线设计必须明确区分，而非把两者揉为一个九州按钮。[events/nesnd_south_accords.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_south_accords.txt:156>)；[common/scripted_effects/nesnd_south_accords.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_accords.txt:20>)；[common/scripted_triggers/nesnd_south_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_politics.txt:306>)；[common/scripted_effects/nesnd_south_peace.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_peace.txt:327>)；[common/scripted_effects/nesnd_south_peace.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_peace.txt:440>)。

## 5. 三国实际分配、人物与经济接缝

直接分封和战败恢复共用`nesnd_partition_japan`。JTK得到原JAP的关东、东北、东海、北陆信越、北海道州块；JIM得京都，以及关西的`xB03EF0`大阪province；JAP留中国、关西余部和原有朝鲜领地，改首都中国地区并标记丰臣残余；日本所持九州和四国给USM。EZO、RYU及其他第三国所有权不被所选州块匹配，恢复分支另要求controller=owner。三国成为吴保护国（JAP若原有吴属国关系则保留既有关系，独立时设保护国）。[common/scripted_effects/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan.txt:77>)；[common/scripted_effects/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan.txt:228>)。

战败路径先把JAP存活人物转USM并吞并，登记前日本州块；隔1天恢复事件在安全上下文检查锚点，再以USM为origin恢复JAP，转回匹配州块（排除九州、四国），调用同一分封。身份重置移除明吴继承变量，把主文化收束为japanese，激活monarchy/autocracy。缺锚点、第三国控制等保留pending/blocked供月脉冲重试。这里允许原JAP玩家失国；没有“自动续玩救援”承诺。[common/scripted_effects/nesnd_war_collapse.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_war_collapse.txt:2>)；[common/scripted_effects/nesnd_japan_recovery.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_recovery.txt:1>)；[common/scripted_triggers/nesnd_japan_recovery.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_japan_recovery.txt:1>)；[common/on_actions/nesnd_japan_recovery.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_japan_recovery.txt:1>)。

下表只把**开局历史**按现有分封的整州规则重新分组，表示静态产业依赖，绝不是战争后实测账；大阪province切分由引擎处理，不能用面积把州级人口建筑编造为精确值。

| 政权 | 可确认的开局整州部分 | 经济结构与缺口（只针对显式历史块） |
|---|---|---|
| JTK扶国 | 关东+东北+东海+北陆信越+JAP北海道：16,081,332人、117级建筑 | 行政9、兵营35、枪械2、铁15、伐木10、港口1；无显式建设/纸/煤/造船块。人口与铁木大区，但原造船、纸和煤链大多分给其他政权，宜独立设港航、财政行政、投入品接入目标 |
| JIM和国 | 京都固定1,437,948人、14级建筑，再加大阪实际部分 | 京都行政4、玻璃1、家具1、食品1、茶2、丝1、木1、牧2、稻1；京都本身无显式港口、建设、兵营、枪械和煤。大阪商港与工业的真实转移量决定预算/就业，不能把和国写成天然富裕或注定破产 |
| JAP丰臣残余／桑国 | 中国+关西+BUSAN+YANGHO合计15,970,622人、165级建筑，再减大阪实际部分 | 整州上限中有全部4建设、全部5纸、全部10煤、全部4造船、枪械2；没有显式铁矿。韩国领土占8,669,114人，民族与行政整合不能附带略过；林摄政会改变统治者但不自动移除这些治理问题 |
| USM直辖 | 原USM九州+日本九州+四国共6,940,050人、84级建筑 | 含海军行政5、港口4、海防3、兵营20、造船3、铁5；这是九州/四国合计，不能把海军行政5错误算成三日本国共有舰队 |

上述整州数均从第3节JSON相加；并不修改人口、不保证三国自给，也没有按三等份拆疆域。三国状态下应逐国观察实际市场/通商法、税容、行政薪酬、军费、资格、营房单位接收和大阪人口产业转移，且只对未验证行为做后续定向验收。

人物开局调用：秀治君主、秀明继承人、仁孝天皇（存`emperor_var`），德川家齐及诸大名、IG人物；Hotta模板在历史中有两个create_character调用，研究保留重复，不据重复文本直接宣称引擎产生错误。模板世系包含秀治→秀明→秀和→平胜／平胜alt→秀卿→秀照，另有德川和天皇继承分支、丰臣纪州大名和釜山德川支系。[common/history/characters/jap - japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/characters/jap - japan.txt:1>)；[common/character_templates/zz_ce_JAP.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_ce_JAP.txt:1>)；[common/scripted_effects/ce_japan_gov_effects.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/ce_japan_gov_effects.txt:355>)；[localization/simp_chinese/replace/ce_names_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_names_l_simp_chinese.yml:46>)。

1840事件以秀治在位为条件，转秀明并改地主意识形态：默认儒家+殖民主义，独立国家可选宪政+殖民主义，基础AI权重1:10。1846事件以秀明在位为条件：默认秀和继位（权重9），或保守派平胜alt（权重1，临近革命+20、地方/首都激进增加权重）；后者回填日本等级/家长制意识形态。它们是有条件的既有继承选项，不等于已经完成“民主路线”或“军国路线”。[events/flavorJAP_ce.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/flavorJAP_ce.txt:100>)；[events/flavorJAP_ce.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/flavorJAP_ce.txt:312>)。

林汉涵当前模板是`USM_lin_hanhan`，first_name Hanhan / last_name ce_Lin。实际任命模块要求三国同属吴、JAP为日本主文化君主国且不与吴交战；取仍在USM的合格同一人物，**固定移入JAP并设ruler**，使用窄政府类型显示摄政。它不是把林同一人物同时设为三国君主。委任失效会撤该模块标记，注释和代码明确不擅自换王；一次任命标记保留。旧设定PPT“李汉涵”是资料异名，由总研究的设定来源另行记录，当前游戏名称以林汉涵为准。[common/character_templates/zz_historical_leaders_ce_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_historical_leaders_ce_asia.txt:939>)；[common/scripted_effects/nesnd_japan_lin_regency.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_lin_regency.txt:8>)；[common/scripted_triggers/nesnd_japan_lin_regency.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_japan_lin_regency.txt:13>)；[common/government_types/00_nesnd_japan_lin_regency.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/government_types/00_nesnd_japan_lin_regency.txt:1>)。

## 6. 三种疆域情境与后续路线的可用接入点

| 研究情境 | 已有实现 | 尚需规格化的长期内容／边界 |
|---|---|---|
| 统一且含九州 | 赢既有参战结算可收回USM九州并独立；九核心统一JE可完成 | 统一后的政体、工业与朝鲜治理仍缺专门长线；统一奖励只有10年行政/动乱修正 |
| 统一但不含九州 | 拒绝分封而吴认可旧约能保留现有国家；可有外部战争/和平外交产生此地图 | 当前统一JE仍要求完整九州，无法将此认定为同一完成终局；须区分“多数九州仍属吴而日本留港口”和“日本完全无九州”；完全无九州需处理锁国贸易入口 |
| 三国并立 | 实际JAP/JTK/JIM创建、分州、人物、吴关系、Lin任命已有 | 三国各自独立外交／解约、互相统一行动、各国可改革到何种政体、原版JAP硬绑机制/global变量隔离、军队/市场/新政府继承需要设计与定向验证 |

军国化可接已有armed_forces／warrior_caste／枪械-造船-军需与林军政背景，但目前没有独立日本军国化进度日志。幕府改革应延续丰臣世系、1840宪政机会和大名行政问题，不能用原版德川倒幕替代丰臣作者线。民主化需要说明君主/天皇位置、代表权、职业军队与地主转型；现有1840意识形态改变不是民主法律自动颁行。三条政治方向宜与三种疆域交叉，而非把“统一/分裂”本身硬等同于某一政体结局。

朝鲜有明确的现实脚本基础：JAP控制BUSAN+YANGHO，KOR控制其余三州并朝贡CNE。当前统一JE明确不要求朝鲜，三分封实际把现存日本朝鲜领土留给JAP。今后“继续统治/重组属国/撤出或与KOR谈判”等均属新规格；需处理8.67M地区人口、8.15M韩国文化人口、煤10级与港口3级等真实得失，并给CNE/KOR响应。不能直接写成“统一日本自动吞并全朝鲜”。[common/history/states/00_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:6814>)；[common/history/pops/11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/pops/11_east_asia.txt:2077>)；[common/history/buildings/11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/buildings/11_east_asia.txt:7540>)；[common/history/diplomacy/ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:162>)。

与USM/Wu的连接已经很深：开局朝贡、九州直辖、支持/反对参战、和平割让、远征/分封、Lin摄政。与CNE的明确既有连接主要是KOR宗主及南朝反吴干涉上下文；未找到以日本为主体的专门中日谈判链。HUS已有南朝外部反应与供给系统，但未找到专门日本—HUS结盟、贸易或改革援助链；这是可接入的外交角色，不能凭背景叙述宣称现已结盟。[common/scripted_effects/nesnd_crisis_effects.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:344>)；[events/nesnd_external_events.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:1>)；[common/history/diplomacy/ce_truces.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_truces.txt:20>)。

## 7. 原作者保留、失去入口的旧分支与未选候选

本次用真正的最早独立备份`pre-update-20261030T233944Z/mod`逐字比对，而非将后来的计划当作原作。`events/flavorJAP_ce.txt` 当前与该备份**字节完全相同**（538行），因此上面三事件是应保留的既有作者内容。原`ce_JAP.txt`现为`zz_ce_JAP.txt`，以及`ce_japan_gov_effects.txt`已存在后续修订；原始与当前SHA均入JSON，不能声称全人物代码原样未动。[events/flavorJAP_ce.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/events/flavorJAP_ce.txt:1>)。

原作者的`ce_usm_cw_japanese_interest`在备份1104行起会调用`usm_civilwar.14`或`.17`，并设置`ce_japan_kyushu_winner`或通知`.19`；当前该JE492行起已改接新的settlement/collapse/crisis.41。有效GAME+MOD全引用保序扫描发现：`.14`、`.17`、`.19`**没有普通脚本入边**；`.15/.16`只由孤立的`.14`调用，`.18`只由孤立的`.17`调用。旧`ce_japan_kyushu_winner`与拼写`ce_japan_keyushu_status_quo`当前只有读/删，没有设置写点。它们仍是事件定义，可经旧存档队列或控制台出现，不能说文件不存在；也不能把它们作为新局正常终局。

旧`.14`是独立、接原版`je_meiji_restoration`和索回USM日本州；旧`.17`会向占领者列表索回9核心州、独立并加同一JE；旧`.16`含恢复东洋领事府的保护国博弈。它们的作者意图可参考，但旧无差别索地行为不是当前第三国保护分封/恢复的执行入口，不建议未经新规格直接重新接活。来源：[common/journal_entries/ce_usm_the_last_days_of_ming.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/journal_entries/ce_usm_the_last_days_of_ming.txt:1104>)；[common/journal_entries/ce_usm_the_last_days_of_ming.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:492>)；[events/usm_civilwar_events.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1661>)；[events/usm_civilwar_events.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1913>)；JSON `event_references`。

工程入口列出的`f2-player-continuation-20261101-a`与`f2-japan-legacy-20261101-a`是未选用候选；不纳入本报告当前主MOD结论。旧实机曾观察吞并后恢复三国和Lin摄政，但对应旧候选、旧场景；本次只读源码未刷新整条路线的引擎认证。日本玩家失国已被用户接受，不自动转化为需要加救援剧情的BUG。[.scratch/debug-release/map.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/map.md:51>)；[docs/agents/engineering-skills.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/docs/agents/engineering-skills.md:31>)。

## 8. 后续方案应明确的最小设计问题

1. “不含九州统一”究竟保留日本九州小港还是全州失去；是否有独立完成判定、称号与对吴未决领土要求。
2. 三政权独立与统一是否依通用外交、局部交涉或专门JE推进；同一朝廷/幕府人物如何跨tag延续，林去世/失吴宗主后如何自然收尾。
3. 朝鲜的统治、自治、独立和KOR/CNE交涉分别消耗什么、何时能反悔、领土与煤/港口产业如何随所有权实际移交。
4. 所有政治路线如何与既有1840/1846丰臣继承、DLC锁国/幕府法律触发、原版大名global变量兼容，避免统一/分裂相互污染。
5. 三国经济目标分别围绕实际资源与行政/商路约束，不保证每国全自给；完整大阪分割、实际编队与市场、税容、工资、资格、投入品价格需后续存档/MCP事实，源码总量不能替代。

这些是具体扩展接缝，不是未经引擎验证的故障结论。日本现有机制保持；本报告未创建新规则、未改概率或法律、未调整人口产业。

## 9. 文件指纹

完整来源指纹见JSON `source_sha256`。以下为主要对象：

| 文件 | SHA-256 |
|---|---|
| [events/flavorJAP_ce.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/flavorJAP_ce.txt:1>) | `0150edb24e6ae546d3baa31cdb29c9e9011b021c6f96093c2a3e3f2b0654d18d` |
| [common/character_templates/zz_ce_JAP.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_ce_JAP.txt:1>) | `12be1c0dbe3f7d5828bd332bbb1df143a71c223adb8438645cf5b33d6472cd18` |
| [common/scripted_effects/ce_japan_gov_effects.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/ce_japan_gov_effects.txt:1>) | `de43bbf2475615a437795fd4cd7aa83d744857b8bbcd43b24b775771e93245f1` |
| [common/journal_entries/ce_usm_the_last_days_of_ming.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:1>) | `2d9cc7f5843e36a0d3c9a83175a42070e6766fdfc861d1141592d59ec8d86a0d` |
| [common/journal_entries/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_japan.txt:1>) | `424dece3a340197f5899728dd4f9513a6c54e62fdd5e403d70efe2f4c4066725` |
| [common/scripted_effects/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan.txt:1>) | `a37223a6f87ab9bf5eac53b525a1a4e9f0227e53517cdb0831702fefaa0f4f1e` |
| [common/scripted_effects/nesnd_japan_recovery.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_recovery.txt:1>) | `b1ff7114bd4866a0fd031568fe2148b9b9a1275539969e2888b43678ee1889f4` |
| [common/scripted_effects/nesnd_japan_lin_regency.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_lin_regency.txt:1>) | `137ddf6eb366bf07e2814eb3c3b7cc4bf53dd2f7adc78d79c23fda681f4f6570` |
| [common/history/states/00_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:1>) | `a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa` |
| [common/history/pops/11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/pops/11_east_asia.txt:1>) | `85b9ef1a805b3b033fb31009b55d270c8d83736749c6255f8d1f4ab45711fd6b` |
| [common/history/buildings/11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/buildings/11_east_asia.txt:1>) | `4879dbe1af1d432616d3954b7154b79ae28169cbfe715e68fd1dfa583a9c5238` |
| [common/laws/ce_trade_policy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/laws/ce_trade_policy.txt:1>) | `54585b30dc129f18ca827b0c15b9f86a29aace68b04f72a4ca5d1f9c50e82505` |

## 后续作者修订与现有实现的区别

用户随后明确天皇JIM就是林摄政政权；本文记录的JAP任命是717c901之前的真实实现，并非新方案。最新计划已列JIM目标、主流ce_wuu及整条任命/恢复/保存对象迁移；本轮研究未改玩法，不能只看计划便认为游戏已切换受任国。见同目录revision-2/revision-record.json。
