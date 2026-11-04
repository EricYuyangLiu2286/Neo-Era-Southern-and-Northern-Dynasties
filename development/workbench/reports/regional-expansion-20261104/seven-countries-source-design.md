# 七国短日志：当前源码、原稿与保守实现建议

2026-11-04；只读研究。GAME 1.13.11 / Steam build 24799966，catalog.py status=CURRENT、changed_count=0。没有启动游戏、没有修改MOD。本文新日志与数字全部是gameplay_proposal；PPET未来为text_attested，不是所有存档的必然历史。先读NESND技能、工程适配、domain、恢复map、research、journal-system-design、numeric-scale-contract、political-design-and-difficulty。报告路径按工程适配放WORK。

M = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties
G = D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game
W = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench
P = W/research/20261031/北明ppet.txt，原件 D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx

## 最关键事实

1. 秘鲁TAG是 **PEU**（G/common/country_definitions/00_countries.txt:2381），PER为波斯，不能混用。当前MOD开局没有PEU州，仍由NPU、SPU和BOL分持秘鲁/玻利维亚地区；M/history/states/00_states.txt:2363以后。PPET所写1836印加第三帝国没有落实为当前开局国家，不能只写一条PEU事件就声称补齐了印加帝国。
2. 1866.1.15终档中PEU已存在、5州、总统民主，故PEU形成后日志既能保守接续原版形成链，又能覆盖这份存档；不必先篡改开局国界。若未来要实现完整印加帝国，应另立地图/历史/法律/人物迁移任务。
3. EGY是TUR的protectorate，并获grant_own_market；不是1836完全独立国。M/common/history/diplomacy/00_subject_relationships.txt:243–277。自身工业日志可以允许属国参与，外交选择须重查宗主。
4. AUS开局有HUN/TRS/CRO王冠领，不直接持有全部匈牙利。M同文件:92–113；保留原版匈牙利问题完整链。
5. 美国西岸属于架空东洲体系，不能把现实美墨战争后的美国大陆领土当事实。M/common/journal_entries/00_major_railroads.txt:74–119已要求加利福尼亚和NORTH_DAYUAN，不能拿原版横贯铁路当美国必做经济教程。

## 当前国家基线

国家定义未被活动MOD文件覆盖；`00_countries.txt.bak`不加载，不能当有效定义。

| 国家 | 文化/首都 | 当前开局关键法律和关系 | 既有内容与处理 |
|---|---|---|---|
| PRU | north_german / BRANDENBURG；G country_definitions/00_countries.txt:58 | M history/countries/pru - prussia.txt:12–26 君主/专制、民族至上、任命官僚、职业军队、公共学校、干预/重商；学校2；HOH傀儡 | 德意志统一、石勒苏益格继续原生；MOD波兰已设置参与标记，不重复重开旧波兰问题 |
| AUS | south_german / AUSTRIA；G同文件:93 | M history/countries/aus - austria.txt:13–30 君主/专制、王冠议会、庄园制、臣民、公共学校、秘密警察、干预/重商 | 历史:63主动添加je_matter_of_hungary，保留；新地方建设放它结算后 |
| TUR | turkish / EASTERN_THRACE；G同文件:1106 | G history/countries/tur - ottoman empire.txt:16–23 君主/专制、米利特、臣民、传统主义、奴隶贸易；EGY宗主 | 历史:29触发sick_man.1，保留坦志麦特/埃及危机；新内容等坦志麦特结算 |
| EGY | misri / LOWER_EGYPT；G country_definitions/01_africa.txt:26 | G history/countries/egy - egypt.txt:10–17 君主/专制、有经者、臣民、农业主义、职业军队、奴隶贸易；TUR保护国、有独立市场 | 保留危机与宗属；独立不是建设入口硬门槛 |
| MEX | mexican / MEXICO；G country_definitions/00_countries.txt:2149 | G history/countries/mex - mexico.txt:7–16 总统共和/寡头、文化排斥、农业主义、无学校/无警察；地主/军队执政 | initialise_caciquismo_effect与考迪罗原链继续；另加小型行政/教育建设 |
| USA | yankee+dixie / DISTRICT_OF_COLUMBIA；G同文件:109 | G history/countries/usa - usa.txt:14–26 公共学校、遗留奴隶制、种族隔离、自耕农、保护/干预、国民民兵；自由政治初始化 | 历史:71–73加入Texas/ACW/Seminole；废奴/内战/重建保留，不再写一套固定1861内战 |
| PEU | south_andean / LIMA；G同文件:2381 | 开局不存在；NPU/SPU继承原版历史，总统共和/寡头、国教、种族隔离、干预/重商、遗留奴隶制 | 保留秘玻国际日志及NPU/SPU→PEU变tag；形成后补山海交通，不假称当前是印加帝国 |

精确开局州清单、逐州起始行号在`seven-countries-evidence.json`的opening_territory。清单指一个state_region中存在该国的create_state，不意味着完整地区归属。PRU有BRANDENBURG、上下西里西亚、东西普鲁士、波美拉尼亚、波森等；AUS有奥地利、波希米亚、摩拉维亚、蒂罗尔/施蒂利亚等；EGY还占叙利亚、黎巴嫩、巴勒斯坦等；MEX保有墨西哥核心但不含加利福尼亚。地图可能分州，完成条件应查owner-state，避免整州条件误锁。

## PPET依据与冲突处理

P原件SHA256=b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae，本次重新计算相同。

- PRU：P24§14/27/28（文本357、370–371行），俾斯麦1851–61为莱茵联邦大使，1864才成为普鲁士顾问、1866宰相；普奥战争和莱茵战争才建立霸权。新日志可做产业和外交准备，不能1836硬塞宰相俾斯麦，也不能强制现实统一德国。
- AUS：P24§12（355行），1848–50镇压匈牙利后让步。适合原版匈牙利问题之后的行政/地方教育议程；日期只是原稿未来，不强制所有存档按年爆发。
- TUR/EGY：P21§12、P22§24/28（267、303、307行）有奥斯曼征服埃及、东方贸易条约和伊斯兰领袖背景；P26§13–18（411–416）是1918–22帝国解体及埃及王朝战争，不应当1836入口。保守新内容用商路、行政和尼罗河产业，不提前写末期哈希姆取代。
- MEX：P18§18/23（181、186）阿兹特克复国及1811–15东洲扶助第一共和国；新日志可处理共和国地方行政、学校与北邻关系，不能再讲现实西班牙殖民解放或必须割让加利福尼亚。
- USA：P18§22/24（185、187）大原汗国剿灭与第三次北美战争；P24§24（367）1861–69废奴战争且法国/东洲支持南方。这是可选未来，保留原生奴隶制冲突；不会强行废奴、生成战争或1919吞并美国。
- PEU：P19§17–29（207–221）印加第三帝国、1811改革、1836–39对拉普拉塔失败、1850年代流亡士绅、矿业证券危机、1864–65共和革命。与当前NPU/SPU/BOL开局冲突。短日志只能借安第斯矿业、山海联系与地方财政的主题，明确称当前秘鲁，不用尚未实现的尤潘基皇帝/儒教上层叙事。

## 每国一个短JE＋结算选择事件

以下均是建议，不是已上线功能；数值为源码估算，未宣称平衡实测。各JE自动识别真实建筑/法律；不新增购买库存/军需履约，不自动activate_law，不要求党派排列。最终两项奖励互斥、限时5年、一次领取；百分比用0.05表示5%，不是5。选项设置done后发奖，重复事件无收益。

| 国家 | 后置入口 | 玩家真实行动与完成条件 | 完成事件选择和有限奖励 |
|---|---|---|---|
| PRU | 1840起＋railways已研究；PRU或由PRU进入的NGF/GER持久身份 | 实有BRANDENBURG和一处西里西亚州；两州各有在岗铁路，国内工具工坊等级至少3且occupancy≥0.75；职业军队/国民民兵任一 | 交通优先：本国合格铁路州铁路吞吐+5%；工坊优先：本国合格州工具吞吐+5%。不给军备库存；不要求吞并莱茵 |
| AUS | 1840起＋原生匈牙利问题已结算；保留失败也可发展 | 至少3个自有州；波希米亚或摩拉维亚有在岗大学，奥地利本部有在岗行政；已实施任一种学校法；若需要政治协议，相关IG入阁＋合法性50即可 | 地方学校优先：短期教育/大学支持（键另核）；中央行政优先：固定+25政力5年。学校路线可直接用有限大学吞吐，避免虚构文化转化 |
| TUR | sick_man_complete持久标记（成功或失败都能进入）＋非战争期 | EASTERN_THRACE及一个自有安纳托利亚州；行政/港口各达到有限等级且occupancy≥0.75；经济法已离开traditionalism | 港路优先：现有港口州港口吞吐+5%；官署优先：+25政力5年。不给外交附庸权或自动转属 |
| EGY | 1840起＋保有LOWER_EGYPT及另一尼罗河州，不要求独立 | 下埃及在岗港口≥2、全国纺织≥3且occupancy≥0.75、学校法离开no_schools；仍可在TUR保护下完成 | 棉纺出口：合格自有纺织州吞吐+5%；地方行政：+25政力5年。若有对TUR关系变化，存在性/宗属必须当场重查 |
| MEX | 1838起，保有至少3州 | MEXICO行政≥2、VERACRUZ港口≥1，工具≥2，occupancy≥0.75；任意学校法，和平 | 地方建设：合格州工具吞吐+5%；联邦行政：+25政力5年。避免“选中央路线即自动寡头/独裁” |
| USA | 废奴已完成＋不在je_acw_war，至少1840；和平废奴也能进 | slavery_banned仍有效；至少两个自有南方州有在岗铁路或大学；教育存在。不能要求真实历史全部南方州/西海岸 | 公民教育：合格州大学吞吐小幅限时；交通复建：铁路吞吐+5%。原版重建/平等日志仍负责政治权利，不再次发文化主流或强制改公民法 |
| PEU | PEU形成且秘玻危机已结束；也可仅has_technology_researched=railways后进入 | LIMA和至少一个自有安第斯州；港口≥1、铁路≥1、矿井≥3且occupancy≥0.75；不要求王朝或儒教 | 矿业通路：合格州铁矿吞吐+5%；省政学校：行政或大学支持。只对当前自有州发奖，不对整个安第斯地区及别国加成 |

为维持短链，完成前不发任何长期buff，失败时无退款和补偿；无需running变量、定时抽钱或人为进度条。目标建筑的就业状态变差只暂时未完成，不清掉建设。上述等级需由实现者对现有历史建筑再定稿：它们是门槛候选，不是已证明七国合理难度。

## 原版完整机制链，可直接借结构

### 真实建设 → JE完成 → 国家选择事件 → 限时州修正

完整已读链：

1. G/common/journal_entries/00_art_jes.txt:1–46 `je_romanticism`：is_shown_when_inactive→possible研究/州建筑条件→complete中country下`any_scope_building`，`is_building_type`、`occupancy >= 0.9`、`level >= 2`；on_complete触发`society_tech_events.302`并set_variable；fail/timeout。证明全国建筑查询不必先绕州。
2. G/events/tech_events/society_tech_events.txt:1、192–255：namespace声明；type=country_event；immediate找满足条件的自有州/建筑保存scope；option/default_option；对州add_modifier并给days。事件在国家scope触发，不从scope:journal_entry中错误调用国家effect。
3. G/common/static_modifiers/02_event_modifiers.txt:1755–1758：romantic_building_modifier使用`building_art_academy_throughput_add = 0.2`；这说明吞吐量键可在州修正适用。新方案建议0.05，不复制原版0.2。
4. G/common/buildings/06_urban_center.txt:32–71：building_art_academy解锁romanticism，引用pmg_base_building_art_academy；G/common/production_method_groups/06_urban_center.txt:38；G/common/production_methods/06_urban_center.txt:252–261 pm_traditional_art实际paper投入/fine_art产出。
5. G/localization/english/content_104_l_english.yml:422–430完成JE/event文本闭包；G/common/journal_entry_groups/00_journal_entries.txt:126定义technology组；图标均来自实际文件中已存在路径。

适用差异：新链不保存可能在事件停留期间丢失的州scope，优先选项执行时每次遍历当前owner自有州并重新检查建筑/归属；若使用scope必须`exists`与owner守卫。原版事件本身没有覆盖所有迟答边界，不能直接照搬漏洞。

另一个完整同类：G/common/journal_entries/00_major_railroads.txt:1–71→G/events/major_railways.txt:1–121→G/common/static_modifiers/content_1_modifiers.txt:932–945。country JE完成触发country_event；国家事件中every_scope_state过滤地区和建筑，再赋州修正，两个option分流矿业或铁路。该原版奖励是+25%与移民吸引2，并不意味着NESND短链应照抄力度。

### 生命周期原生入口

- G/common/journal_entries/05_austria_journal_entries.txt:396–424：on_fail国家事件/失败变量，invalid法律不再符合，on_invalid设置结束变量。证明on_invalid有效，不能只写fail而遗漏合法变制。
- 同文件:1–148：je_matter_of_hungary完整入口、monthly acceptance、complete、on_complete、fail、on_fail；M history/countries/aus - austria.txt:63提供真实调用者。原版国家和JE修正scope不同，`modifiers_while_active`的清理要按原型区分。
- G/common/history/countries/tur - ottoman empire.txt:29→G/events/sick_man_events.txt:4–69→G/common/journal_entries/00_sick_man.txt:1开始，主JE结算触发sick_man.2/.3；两事件分别93、196行set_variable=sick_man_complete。新后续用此持久标记，不用“没有JE”冒充完成。
- G/common/journal_entries/02_peru_bolivia.txt:1开始为contextless国际日志，country自己的has_journal_entry不能冒充involved判定；G/events/brazil/peru_bolivia.txt:267–299存在NPU/SPU合并与change_tag=PEU。不要把全球JE整份复制为country JE。
- G/common/history/countries/usa - usa.txt:71–73→G/common/journal_entries/00_acw_entries.txt:1/90/133/172/305分别倒计时、战争、重建、重新整合、平等。后续只做建设，不替原版重复结算政治成果。
- 德意志链G/common/journal_entries/00_german_unification.txt:111–197（文化热情→候选→german_unification.5）、199北德、258南德、320统一。它与本MOD莱茵联邦现实不完全相同，但本次不重写统一系统；后续精调应独立范围核对形成国/外交，不靠新工业JE强制吞并。

## 推荐生命周期契约

- 未激活：身份、日期/科技/前置结算全部满足才possible；内部tag树隐藏，真实条件用原生勾叉。新局与旧档均靠自动possible识别，不依赖on_game_start只跑一次。
- 激活：没有临时buff则无需running锁。若要running，possible不得NOT running（会自锁），失效清理与成功结算一致。
- 暂停：战争、就业不足、预算低、临时执政/合法性不足只阻止完成，不自动失败。建筑/法律恢复即继续。
- 失败/失效：关键全部领土丢失、国家身份变成不相容国家、永久改变前置路线才invalid；on_invalid移除本轮临时变量/国家修正，是否可重开明确选一种。建议无奖励未完项目可在资格恢复后重开，已done永久不可重领。
- PRU→NGF/GER必须继续同一国家持久标记；不可让独立成立的奥地利GER无条件继承普鲁士工程。新JE是否transferable不要凭想象：原版sick_man子JE:178有transferable=no，但它指日志转移语义，不能代替tag资格。
- NPU/SPU→PEU：如仅PEU后置日志则无迁移问题；若以后做先导，变tag后保持同一country变量，吞并另一秘鲁国家不得重复结算。
- 国家被吞并：无国家时无法触发新奖励；不要给原owner州修正留下无期限效果。限时已获得奖励是历史结果，可自然到期；未完成项目不自动恢复国家或送钱。
- 改宗主：经济日志允许继续；外交事件选项重查当前宗主/对手，不持久缓存TUR作为必有对象。
- 事件迟答：每个选项重查done和最低资格；地点失去时只发仍适用的国家奖励或明确无效，不对别国州奖励。设一个默认选项处理AI/到期；事件必须有稳定desc，不引用执行后才建立的scope。
- 抽查边界：0/门槛-1/门槛建筑；occupancy0.74/0.75；1/2/3州；前置未结算/成功/失败；tag改变；国家死亡；重复事件/存读档；同等IG和合法性下党派改变不影响资格。

## 1866.1.15既有观察者终档

读取W/reports/observer-finish-20261103/finish.json指定原始终档，仅解析，不启动游戏。
SHA256=84aeb299f56656c3c9ce2373299ef5ba98a78a3bf01bdc9a1b39f38c49ee67e4，213403518 bytes；该局loaded_commit=adfc31759b355d33e0f09269822911b367499b53。它不含本轮新实现，不能当其引擎验证。

| TAG | 终档政府/州数 | active日志或法律的有效观察 |
|---|---|---|
| PRU | gov_absolute_kingdom / 9 | je_north_german_unification、石勒苏益格仍active；君主/专制、职业军队、公共学校 |
| AUS | gov_dual_monarchy / 13 | 匈牙利问题不在active集；君主/专制、crownland_diets、公共学校。政府名不等于自由宪政 |
| TUR | gov_sultanate / 29 | sick_man_main及经济/教育/军队/官僚子JE active；农业主义、私人学校、奴隶贸易 |
| EGY | gov_khedive / 11 | 农业主义、no_schools、奴隶贸易；不能假称已现代化 |
| MEX | gov_presidential_democracy / 13 | je_caudillo active；资格选举、宗教学校、农业主义 |
| USA | gov_presidential_democracy / 37 | law_legacy_slavery active、je_acw_countdown active；PPET废奴战争没有成为此局1866既成事实 |
| PEU | gov_presidential_democracy / 5 | 财富投票、宗教学校、遗留奴隶制；je_caudillo与南美国家认同active，非印加皇帝政体 |

原始选取字段在seven-countries-evidence.json（包括所有序列化候选laws/JE）；**必须过滤active=yes**，不能把候选序列化项说成同时激活。opening_territory来自当前MOD，1866数据来自旧运行，两者版本不同。extract_seven_countries.py复用既有只读serializer分段方法，保留同名重复记录，未修改save。

## 交付边界

本报告完成了来源、身份、原稿、原生完整链和小型可实现建议。未完成：各国建筑门槛量化经济平衡、玩家正式文案、脚本实现、静态验证及引擎验证。正式文本须另按nesnd-player-writing作者取样流程写；不要把本文内部术语放进游戏。Real AI不需要复制剧情或模块，本次优先已有原生完整链，未将其当作来源。

## 源文件指纹

完整绝对路径与大小见seven-countries-source-manifest.json。以下为本次读取源码SHA256；报告引用行号以这些指纹为准。

| 文件 | SHA256 |
|---|---|
| M/common/history/countries/pru - prussia.txt | 73e3fbaf13e3f2304f9ed1f77b8a1a6d6ba1a184117d8a2137429ad01e126929 |
| M/common/history/countries/aus - austria.txt | 7bd1b0aec76ed68befe4974916ae985bc277857981b089ed7390a014bb5eb15e |
| M/common/history/states/00_states.txt | a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa |
| M/common/history/diplomacy/00_subject_relationships.txt | 618289bd6e7bd4e8fe5f3276249b6997f7a0c51cd2ab9f4f4f46289b9a02d59e |
| M/common/journal_entries/00_major_railroads.txt | 543ed4d642ef697286d63ac4af1952af84f0f25957f60d425aa77d19cc0b806f |
| G/common/country_definitions/00_countries.txt | d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74 |
| G/common/country_definitions/01_africa.txt | dd89615390fc8051e818c1eb8aa8b96964be2257019c740eaa00dd2339d152cd |
| G/common/history/countries/tur - ottoman empire.txt | 93d02b1f8732205f8dce570639b220cf32df58a43741fc68d6604b4ded8ebf09 |
| G/common/history/countries/egy - egypt.txt | e5a22623deea26108296bb06b08343805c76b75b166d2404bf9fc2225d1b42af |
| G/common/history/countries/mex - mexico.txt | 8746ef2bd288d9a0123e597f5777d352447f2ff3c7ab47db7cba64f50cad6a6d |
| G/common/history/countries/usa - usa.txt | 64ee2fa609418dc56d40a8b052ede66af9cdbeba399639030692ad7b3242acae |
| G/common/history/countries/npu - north peru.txt | 3e2e69487c6f501b3f3fcf75eb16079679840e1d4ffde570a3543900f18371cc |
| G/common/history/countries/spu - south peru.txt | 86701e30bb22dc98a5b7108921b35b7db20ce76dc9724b5348607c61185de467 |
| G/common/journal_entries/00_art_jes.txt | cdad9a29326543d97f1a0d46c44e1fc3bd83252481503656b261af911df3f4d7 |
| G/events/tech_events/society_tech_events.txt | fdbc59b8dc76a95f41a71e0b42d817e58134b0915c133cad355f50171d248e0f |
| G/common/static_modifiers/02_event_modifiers.txt | 43fd43a9c772de4323582da2780c62eee87e8eb1f87a5fb845a643d064a8873d |
| G/common/buildings/06_urban_center.txt | 5bd858a79aca4a25e7f61956692fa9b56a5dc3f847971f63d7365db51623b25f |
| G/common/production_method_groups/06_urban_center.txt | 444618ae2ed2c71be1ebf8edd909926baa547f297d0c12515759fb6b606031e5 |
| G/common/production_methods/06_urban_center.txt | 1dc730c0a8a331c68c9035013d0d103e85208dac2d7536783fa236f63d1926a0 |
| G/localization/english/content_104_l_english.yml | b1773ec14d7efbff8eac19d5f961ebb784d6f1f1fe697f3a8e038968e5d46038 |
| G/common/journal_entry_groups/00_journal_entries.txt | ccee248be47bc1606e715f16503cca90aa2baa15a89ef978a5665c1eb8dee439 |
| G/common/journal_entries/00_major_railroads.txt | 14592b73831f8899cd089604fc4f3d1961b858e06cce09cefcb9dc5c3e2c8c9f |
| G/events/major_railways.txt | ae7b732918864fe77aae1ffb4d962cbf5a5a2ca5341d777aa3282c2041eb1af1 |
| G/common/static_modifiers/content_1_modifiers.txt | 52cb2cb977445444bfb55833ffc73d91c30a9d5f4c318f50f512e660468b2dce |
| G/common/journal_entries/05_austria_journal_entries.txt | abc3af4f08ee235a250a2dca949cc4bf1b0e835b62c2380813ccf19b8614b369 |
| G/common/journal_entries/00_sick_man.txt | e48405bfabb52f6ce757880e436c8d44c67111e246af3215fd3f96ec4f3477f9 |
| G/events/sick_man_events.txt | d110d1fd83cd98e131d4c2769b606cc908f17844eff88ef65f51febf313a0c2b |
| G/common/journal_entries/02_peru_bolivia.txt | 96095b62af0c7911aad5a3636c25fc933b58e92516803c9eaa08e948b922989f |
| G/events/brazil/peru_bolivia.txt | 019e3df6feba7e0c3a547da3c49e19a55f6a9bbe90b461d5fb8d7a6e85f5fae7 |
| G/common/journal_entries/00_acw_entries.txt | f164d68b6422676c1ed410f75532a05b18b091a77dea628bc9b62ab1d859e3fa |
| G/common/journal_entries/00_german_unification.txt | 38a42bbfae01cbc32d42b9076c904a4d0cb65c3c2959f7f7c3aca2271a7c66b8 |
