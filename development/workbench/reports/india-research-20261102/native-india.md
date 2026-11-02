# 原版印度机制研究：1.13.11 / build 24799966

研究日期：2026-11-02。只读本机 GAME；未修改主 MOD、本体或技能，未开游戏。`catalog.py status` 为 CURRENT，changed_count=0。本报告是**源码研究与设计参考**，不是引擎验收，也不是 NESND 印度的既定世界观。

配套：`native-india-manifest.json` 记录81个源文件 SHA-256；`native-india-object-index.json` 保存对象行号；`native-india-inputs.json` 保存逐人口块、逐建筑所有权块和军队输入；`native-india-summary.json` 保存精简结论及23个 JE 索引（包括明确排除为BIC内容的2个DEI日志）。解析器是 NESND `pdx.py`，保留重复项和顺序。

## 首要结论

1. 原版可借鉴的是“治理压力—改革—政治动员—主权安排—统一后整合”的条件链，而不是将英属印度改名为莫卧儿。BIC 开局的公司政权、英国主体文化、殖民行政、攫取经济和宗主关系，是原版大量条件的前提。[N1][N2]
2. 日志并非开局全部开启：公司治理与功利主义较早；铁路要求技术与跨南北印度据点；泛民族主义及自治要求 `pan-nationalism` 和现实政治运动；反种姓要求 `human_rights`；联邦整合在自治或独立后。[N3][N4][N8][N9][N10][N11]
3. 1.13 的种姓是独立社会等级、职业归属、法律及接纳度系统。印度教数据库本身只有宗教传承、颜色、图标和肉类禁忌；“印度教使识字率低”不是该宗教条目的原生效果。[N14][N15][N16]
4. 印度民族主义、印度教民族主义、穆斯林民族主义、反种姓运动和莫卧儿王朝复兴是不同对象。原版泛印度运动必须发生在非南亚主体文化的 BIC 属国；原版 MUG 的主体文化则是 hindustani。原版代码不能证明 NESND 的莫卧儿天然是“外族王朝”。[N2][N10][N12][N18]
5. 可借鉴的工业化目标有跨区域铁路、三地大学、军力与种植业扩张、税制与公共教育改革、降低对宗主经济依赖，以及统一后的土邦财政安排。不是一个“完成工业化”按钮。[N3][N4][N5][N9][N11]
6. 本次覆盖的原版印度 JE 中没有“法国帮助莫卧儿现代化、统一印度后抗吴”的既成链。这部分须据 NESND 人物、外交、领土与年代另行设计；原版提供外交应答、外部施压、建造目标及统一结算的机制实例。法国在 BIC 历史建筑中的一等级所有权也不是援助剧情证据。

## 覆盖口径

已枚举 `common/journal_entries/04_*.txt` 全部对象、`00_east_indies.txt` 及 `events/india_events/*.txt` 全部事件，另含 `british_raj_events.txt`、`bic_breakup.txt`；这些文件的对象清单是完整的。核心段落逐项阅读了调用者、JE 门槛、按钮/进度条、主要效果与终局。**并未宣称印度所有随机事件的每个选项、所有模型资源或全游戏通用工业 JE 已逐一闭包审查。** 锡克、土邦、杂项、监狱及人物创建池在清单中；下文只对直接影响当前方案的链做深入说明。

`ip2_content` 在源码注释中对应 Pivot of Empire。铁路、功利主义、自治、民族主义、不合作、反种姓、联邦、饥荒与维多利亚车站均有 DLC 门槛。兵变全局入口、殖民巩固及宗教分歧 JE 不能一概标成同一 DLC 限制：需保留各自实际入口判断。[N3][N4][N6][N8][N9][N10][N11][N12][N13]

## 按阶段的原版链条

| 阶段/对象 | 实际入口与玩家目标 | 结果与退出 | 对 NESND 的借鉴边界 |
| --- | --- | --- | --- |
| `je_consolidate_colonial_rule` | BIC 国家历史直接加入；印度边疆列表中本国/属国/宗主体系控制至少80%；分离进度<0.3的月份累计120，完成时最高分离进度<0.5 | `east_indies.1`，置 `consolidated_colonial_rule`；脱离英国、英国不存在或转殖民地失败；公司崩溃变量使其失效 | 可借鉴领土覆盖与累计稳定月份；英国边疆扩张目标不搬进 MOD。[N1][N3] |
| `je_imperialism_of_promise` | BIC 特许公司且英国主体文化；有功利主义统治者/煽动者/IG领袖/重要政治家；Mill可满足。公共学校、义务小学、废奴、改女性法律、比例/累进税、行政充足、SoL≥10 | 30年（10950日）；成功 `utilitarian.1`，失败 `.2`，超时 `.3`；兵变/分离危机/崩溃可使失败；成功更改工业家马尔萨斯主义为密尔功利主义并给修正 | 适合学校—税制—官僚互相制约的改革链；不是本土君主改革的现成叙事。[N4] |
| `je_uneasy_raj` | `history/global/00_global.txt:3` 加入 contextless JE，围绕 BIC 的孟加拉、孟买、马德拉斯三条稳定度 | 完成需殖民巩固、SoL≥10、激进人口≤10%；失败累计危机月达100或相关入口退出，启动兵变；成功保留公司并开放后续结束公司统治决议 | 三地区压力条、政治/财政/宗教/土邦条件是可复用结构，三总统区身份是殖民前提。[N6] |
| `je_sepoy_mutiny` | 上一 JE 失败→`sepoy_mutiny_events.3`→即时准备、土邦立场、`sepoy_mutiny_run_all_effects`；可选转入已生成反叛方 | 清除相应起义国、无战争、无分离后，英国宗主情形触发 `raj.1`；失败触发 `.2` 并展开多国解体结算 | 保留“危机强度决定参战方与代价”的设计；本轮不复制其大规模领土结算。[N6][N7] |
| 英国的四种命令 JE | 年度池发种植园/军力/大学事件，强迫法律另由法律施压回调；同一时间排除其他命令，接受后加入子JE | 5年（1825日）；种植园目标原基数+25%、夹10–50级；军力投射+25%；三地各3级大学；指定法律生效。成功改善关系/亲宗主派安抚，超时或拒绝有代价 | 外援合同可借鉴“先有外交事件，再有明确建设义务”，必须替换宗主命令含义。[N5] |
| `je_india_railway` | 玩家在印度、有铁路科技且南北印度均有州 | 四条指定地区铁路均具建筑即可，无须完成时都由玩家拥有；完成置全局一次性变量并发 `india_railway.5`；失去所有印度州失效 | 铁路走廊适合中期统一市场任务，需重建 NESND 地区列表。[N8] |
| `je_india_home_rule` | BIC属国、泛民族主义、存在泛印度运动、无南亚主体文化、且不是特许公司 | 要自治领/保护国地位、选举权、民选官僚、至少一个南亚文化平均接纳≥60。失败：分离爆发、运动激进≥0.65、革命进度≥0.75；独立/宗主失效使 JE 退出 | 用于主权谈判与国内制度条件；不能在独立莫卧儿开局直接挂原条目。[N9] |
| `je_india_nationalism` | BIC属国、泛民族主义，泛印度运动激进≥0.65，且无南亚主体文化 | 完成是运动消失/支持≤5%且激进≤10%，或独立；革命触发宗主抉择。撤出后有区域解体、转入革命方、孟加拉自由邦等不同结算 | 原版“压制民族主义成功”和印度独立的价值立场不同；需按 NESND 玩家阵营改叙述与成功含义。[N10] |
| `je_india_non_cooperation_movement` | 上述身份条件，运动造成阻挠，经济依赖>2.5，有合格贸易商品 | 10年；依赖<2，且同市场本国生产份额>50%，异市场则对宗主市场进口依赖<25%。激进降≤10%/运动消失或升至内战阈值失败；独立失效 | 这是产业替代与经济自主的实际玩法目标，阈值依原版尺度；MOD开局不能无测量照抄。[N11] |
| `je_communal_divides` | BIC、民族主义可见、至少5州同时有印/穆群体；泛民族主义后，印/穆民族主义之一身份支持≥5%、激进≥50% | 降低运动压力或选联邦方案；失去东孟加拉、旁遮普、信德、克什米尔且和平则失败。联邦按钮会生成 BGL/IDS属国并转移西北诸州，增加印度教激进、穆斯林忠诚 | 宗教共同体冲突≠普通全国激进人口；联邦是实际分权/领土与忠诚交换。[N12] |
| `je_dravidian_movement` | BIC、种姓等级体系、无人权平等法；到 `human_rights` 才激活 | 农民IG在政府或强大，且种姓不执行/平权行动则成功；独立/自治条件下，农民边缘化且执行/法典化种姓则失败；社会等级改变则失效 | 反种姓不宜开局作为第六七条无条件任务；能与教育和职业资格改革形成后段。[N13] |
| `je_federation_of_india` | BHT或自治后的BIC，有所属土邦；独立或已获自治 | 年度邀请按钮，友好关系+低独立倾向；土邦接受则吞并并累加王公年金负担；世界不再有土邦完成；恶名≥100或委员会共和国失败 | 统一后任务而非开局总目标；财政补偿、关系和领主利益提供和平整合成本。[N17] |
| `je_mughal_hindustan` | MUG国家历史在ip2开启时加入，保存BIC与MUG | 独立且和平即成功，失君主制/内战失败；`mughal.7`提供多文化整合（加4文化、最多3邻国）或君主威望/行政路线（最多2邻国） | 这更接近王朝复兴可借鉴样式，但原版MUG是英国控制下的德里王朝；NESND范围与合法性必须重建。[N18] |
| 饥荒、维多利亚车站 | 饥荒在北或南≥4州/全印度≥15州实际饥荒才启；车站需英国文化、孟买和钢结构建筑科技 | 饥荒解除相应范围、清理修正并设冷却；车站建筑存在，允许奇观效果时就业≥50%才成功 | 危机按实际可观测状态触发；车站是英国专属纪念建筑，不能冒充通用工业阶段。[N19] |

进度条自身不保证结局。自治条从25开始、0–100，有本土IG参与政府、宗主政界、关系、独立倾向和饥荒等月度因子；最后完成仍靠政体/法律/接纳度。三总统区条从250开始、范围0–300，向225缓慢回归；军饷、税率、地方动乱/忠诚、土邦独立倾向、地主态度、宗教与军法均影响变化。任一区低于225的月份推动兵变计时。这是“数字说明可操作原因”的原生样例，不是纯等待条。[N6][N20]

终局效果的数据库闭包另核如下：殖民巩固事件可选对所有土邦关系+30，或给工业家修正；铁路完成给选中州迁入吸引力+50%、铁路吞吐+15%；功利主义完成有教育机会+0.10和IG政治力修正；不合作成功给运动吸引力+25%、相关人道主义/和平主义支持人物永久人气+25；联邦完成给威望+15%和忠诚者。王公年金不是免费整合：`modifier_privy_purse_payments` 是 `country_expenses_add = 1`，乘数由本国GDP及已吞并土邦数计算；终止付款须地主不在政府且联邦日志结束，并激化贵族。以上是原版数值，不是MOD拟采用数值。[N28][N29][N17]

## 种姓、印度教与识字：四层应分别设计

| 层次 | 当前原版实际内容 | 设计含义 |
| --- | --- | --- |
| 宗教 | hindu 为 dharmic heritage，taboo meat | 没有直接教育惩罚，不能写成印度教天然低识字。[N14] |
| 社会等级 | `british_indian_caste_system` 的 pop criteria 为印度教+南亚传承；MUG/BIC国家定义均指定此体系。五类职业映射：婆罗门=学者/官僚/教士；刹帝利=贵族/资本家/工程师/军官；吠舍=职员/农民/店主；首陀罗=劳工/技工/自耕农/士兵；达利特=奴隶 | 这是引擎对社会等级的抽象，尤其不能据此把现实达利特等同于奴隶；要确认MOD采用此抽象还是自定义制度。[N2][N15] |
| 法律 | 执行、法典化、不执行、平权行动四档；前两档给行政人口成本折扣及地主政治力，并限制同等级/跨等级资格增长和接纳上下限；不执行仍有部分接纳惩罚；平权行动需废奴，给低等级教育与文化接纳加成，也有满接纳激进化代价 | 可将行政成本、就业流动、教育受益与旧利益反对连在一起，而非只加固定识字。[N16] |
| 政治/身份 | devout对印度教/英国印度有不同意识形态与名称；独立效果会撤换殖民工业家思想、调整小市民及宗教IG；反种姓运动由农民IG及法律决定 | 王朝、印度教宗教领袖、穆斯林群体、本地地主、城市中产不应合并成单一“传统派”。[N21][N13] |

原版 `set_hierarchy_event.1/.2` 还有基于英国属国与印度教比例的社会等级切换尝试，由通用 on_action 调用；它们有自己的scope与条件。本报告不以原版存在即认证其适用于NESND，也不准备直接移植该自动切换。[N22]

人口初始化调用 `effect_starting_pop_literacy_baseline`：基础0.05；官僚/学者/教士/工程师+0.45；上层阶级+0.15；职员/店主+0.05；未整合州乘0.5。条件可以叠加，因此“全国5%”或“所有婆罗门50%”都不成立。财富低档基值10，上层+15、中层+7、劳工-2、自耕农-3，另调用奴隶财富处理。全国识字与SoL须由实际职业分配、州整合、初始化顺序和运行状态确定。[N23]

## 可核算的开局输入

从**所有原版 history/pops 与 history/buildings 文件**抽取 `region_state:BIC`，没有把 BIC 属国算进来。包括印度以外 BIC 所领缅甸部分。省略 religion 的人口依据相应 culture 定义补足；逐块证据、来源哈希和状态地区均在 `native-india-inputs.json`。未省略或覆盖重复 `create_pop` / `add_ownership`。

| 指标 | 原始输入 |
| --- | ---: |
| 人口块 / 所涉 state_region | 157 / 21 |
| 人口 size 总和 | 110,522,582 |
| 印度教 / 逊尼派 | 79,260,778 / 28,778,068 |
| 显式奴隶人口 | 2,760,923 |
| 未指定职业的人口 | 107,691,774（不能直接认作自耕农） |
| 建筑块 | 107 |
| 所有权等级总和 | 369，另有泰姬陵显式 level=1 |
| 本国/英国/法国的显式所有权等级 | 231 / 137 / 1 |
| 鸦片/染料/丝绸/烟草/棉花种植园 | 73 / 43 / 20 / 19 / 16 |
| 行政/纺织/港口/军工/铁矿/煤矿/建筑部门 | 47 / 30 / 17 / 11 / 5 / 2 / 3 |
| 孟买/马德拉斯/孟加拉军编制单位输入 | 39 / 69 / 100 |

以上是脚本初始化投入，**不等于**人口运行总量、就业、GDP、SoL、财政平衡或军队战力。显式建筑中没有大学/铁路，不代表没有铁路科技；BIC国家历史确实额外给 railways、mechanical_tools、atmospheric_engine、corporate_charters。军事编制单列，未把营队重复算进建筑所有权表。[N1][N24]

开局经济政治还包括 high 税率、鸦片和烟草消费税、鸦片低出口补贴与衣物高出口税；公司统治修正显著放大工业家/官僚政治力并压低贵族政治力，用元首合法性抵消基础合法性惩罚。孟买、马德拉斯与阿萨姆获 ryotwari 修正，当前效果是自给农业/牧业集体化额度，而不是一个通用提高产量buff。[N1][N25]

## 人物应按时代与政治角色进入

开局 BIC人物历史创建 Robert Grant（工业家）、Haji Shariatullah（孟加拉逊尼农民IG）、Radhakanta Deb（孟加拉印度教虔诚者）、Dwarkanath Tagore（小市民）、Prasanna Tagore（地主）、Ramgopal Ghosh（知识分子，原版设atheist/reformer）。工会领袖使用孟加拉/泰卢固/马拉地文化随机生成。George Eden在英国生成；Mill仅在相应DLC条件下创建。军官人物由军队历史补入，不能只看国家人物文件就宣布人物全覆盖。[N26]

后期模板不是开局人物：例如 Dayananda Saraswati 的可用窗1865–1882、Narayan Lokhande 1874–1897、Jamshedji Tata 1868–1900、Nehru 1912–1936、Ambedkar 1917–1936。Gandhi、Tilak、Bipin Chandra Pal、Lajpat Rai又对泛印度运动支持权重有专门乘数。Periyar/Gandhi等部分模板靠事件创建，不能把所有模板一股脑放1836。[N27][N10]

可借鉴的不是照搬英国官员，而是“改革官僚—本地宗教保守派—地主—城市改革派—农民社会改革派—晚期群众民族运动”的人物职责分工。NESND可在适合的年代用本项目人物承担对应冲突，法国顾问也应有合同、技术领域、财政负担与国内反对者。

## 面向 NESND 的阶段建议（推论，不是原版设定）

1. **开局：王朝统治的基础。** 先处理合法性、地方领主、军队财政、宗教待遇和基础识字/官僚再生产，只给少数核心日志。是否启用原生种姓体系，先核对主MOD实际社会等级与法律，尤其穆斯林王朝治理印度教社会的作用边界。
2. **改革条件成立后：学校、税制与军工。** 用可负担的建筑/法律/行政/就业条件开子日志；法国帮助以谈判事件启动合约，法国提供何种具体技术、投资、顾问或军工支持须另查当前原生接口；不能把英国命令、GDP常量或一键研究全套技术冒充援助。
3. **社会动员阶段：印度共同体与王朝归属。** 民族主义科技、城市专业阶层增长、接纳度和可见政治运动提供新条件；“驱逐外族君主”“改造王朝为印度国家”“联邦妥协”应是可竞争路线，不预先规定民族主义必须反莫卧儿。
4. **取得足够领土与稳定后：统一印度。** 土邦同意、武力统一、文化承认与财政补偿应有不同条件及代价；统一不自动解决阶层和宗教问题。州列表要按NESND实际印度疆域重建，不照搬英国的四铁路走廊/分治边界。
5. **统一与现代化达到条件后：对吴战略。** 以具体工业/军工供应、军队质量、海陆通路、外交承诺与国内政治支持启动。原版印度链无吴，因此这是新设计，不能用原版对英独立结算来证明其完成。

## 不应直接复制的当前源码细节

原版也有需复核的疑点。例如自治进度条标作“pacifist”的正向分支同时要求且排除 `ideology_jingoist_leader`；宗教分歧完成条件第一组复用穆斯林支持条件；达罗毗荼日志的成功事件条件与社会等级检查有值得复核处。以上只作**源码结构疑点**，本轮不修原版、不声称已复现游戏缺陷。实施时使用清楚的scope、显式退出和真实观测条件，而不是整文件复制。[N20][N12][N13]

## 精确来源

以下链接以起始行定位，文字中的范围为读取范围；文件SHA见manifest。

[N1]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/bic - british east india company.txt:1> "1–83：科技、法律、税制、JE、修正"
[N2]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1278> "MUG1278–1289；BIC2529–2539；BHT3812–3821"
[N3]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_east_indies.txt:1> "1–104殖民巩固；106–187改革与伦理政策属于DEI"
[N4]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_imperialism_of_promise.txt:1> "1–151；终局events/india_events/utilitarian.txt:74–108、174–199"
[N5]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_british_dictates.txt:1> "1–423；年度调用on_actions/00_on_actions_yearly.txt:475–482；british_dictates.txt:715–806；法律回调00_code_on_actions.txt:7721"
[N6]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sepoy_mutiny.txt:1> "1–611；全局入口history/global/00_global.txt:3"
[N7]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/sepoy_mutiny_events.txt:1798> "1798–1936；scripted_effects/00_sepoy_mutiny_scripted_effects.txt；raj.1在events/british_raj_events.txt:4–161"
[N8]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_railway.txt:2> "2–175；终局events/india_events/india_railway.txt:430–522"
[N9]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_home_rule.txt:1> "1–251；成功换BHT及文化/宗教/IG处理在events/india_events/india_home_rule_events.txt:25–105"
[N10]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/03_pan_national_movements.txt:1> "1–394；JE见04_india_nationalism.txt:1–112；终局india_nationalism_events.txt:43–304；激进阈值script_values/india_values.txt末行"
[N11]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_non_cooperation.txt:1> "1–295；终局events/india_events/india_non_cooperation.txt:378–682"
[N12]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_communal_divides.txt:1> "1–202；联邦按钮scripted_buttons/04_india_buttons.txt:544–674；政治运动04_national_movements.txt:1、365"
[N13]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_dravidian_movement.txt:1> "1–102；终局caste_conflict.txt:160–246"
[N14]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/religions/religion.txt:89> "89–96"
[N15]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_hierarchies/00_social_hierarchies.txt:5> "5–15；职业分类social_classes/01_british_indian_caste_system.txt全文件"
[N16]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_caste_hegemony.txt:6> "6–181印度四法；law_groups/00_laws.txt:42链接等级"
[N17]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_indian_federation.txt:1> "1–144；按钮04_india_buttons.txt:676–786；接受/拒绝events/india_events/federation_of_india.txt:43–144；年金script_values/india_values.txt"
[N18]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_mughals.txt:1> "1–63；入口history/countries/mug - mughals.txt:21；mughal.7事件759–1202"
[N19]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_indian_famines.txt:1> "1–238；另04_victoria_terminus.txt:1–106"
[N20]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/00_victoria_progress_bars.txt:1020> "1020–1153；总统区00_sepoy_mutiny_progress_bars.txt:1–332、334–653、655–973"
[N21]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_scripted_effects.txt:4873> "4873–4979；devout定义interest_groups/00_devout.txt:406–423"
[N22]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/set_hierarchy_events.txt:4> "4–55；00_code_on_actions.txt:518–519"
[N23]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:292> "292–336；wealth_low在00_starting_pop_wealth.txt:120–154；调用history/population/bic - british east india company.txt:3–4"
[N24]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-research-20261102/native-india-inputs.json> "全GAME BIC人口/建筑扫描；逐块源路径、行号、SHA及军编制"
[N25]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/content_304_modifiers.txt:226> "226–256公司/王室统治；611–615 ryotwari"
[N26]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/bic - britishindia.txt:1> "全部创建入口；character_templates/country_bic.txt:5–167与军事历史100–328"
[N27]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_bic.txt:311> "311–714后期领袖；1015–1538群众政治人物；这是模板可用窗而非保证出生日期/加入日期"
[N28]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip2_03_modifiers.txt:2> "2–11功利主义；161–165铁路；298–327反种姓；不合作00_ip2_05_modifiers.txt:123–131；联邦content_304_modifiers.txt:688–700"
[N29]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/east_indies_je_events.txt:28> "28–49殖民巩固两选项；其他终局india_railway.txt:490–521、india_non_cooperation.txt:658–681、federation_of_india.txt:177–187"

## 仍需下一轮确认

- NESND现有印度全体国家、主体文化、宗教、种姓等级、法律、人物与实际殖民关系；本报告不替另一路MOD审计作判断。
- 新法国援助的具体调用链、提供方利益及终止条件；原版对英命令不能直接翻转为法国善意援助。
- 新统一范围、对吴战略目标、每条路线失败结果及人权/民族主义时代门槛。先规划，再按主MOD数据定量。
- 实机GDP、SoL、识字率、税收能力、军费、关键商品短缺和学校就业；本轮无游戏运行，不填伪造基线。
