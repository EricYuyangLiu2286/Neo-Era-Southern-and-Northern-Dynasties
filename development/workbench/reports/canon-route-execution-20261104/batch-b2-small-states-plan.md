# B2 — 印度土邦与南洋：实施计划

2026-11-04；状态 **PLAN_READY（修订2，待root批准新增尺度分支与C1交接）**。root已批准原计划的机制、数值、原生武装独立入口及kind6/7/8/9；修订1已核南洋地域并修正文案主体。本次依用户最新说明，将远南、缅甸、暹罗及其他满足实际规模的国家分为区域发展路径，替代仅给六个TAG产业等级下限4的处理。新分支与待批数值集中在§4.1–4.3、§5.1、§10.1和§15；其余已批协议与底层机制保留。本阶段只读源码、写本报告；未改玩法、未执行行为测试、未运行游戏。适用当前候选 `exports/canon-route-execution-20261104-a`，不是主 MOD。父级任务34／B2。实施须等 root 明确GO和 C1 共享外交文件交接，之后依次完成编辑→代码与中英文冻结→获准测试。B1 `STATIC_PASS` r3显示修复及其34文件闭包、帝国印度、天竺／远山门槛不在本批重设计范围。

## 1. 本批交付与受保护内容

交付一套可实际游玩的土邦／南洋发展链：经营生计→地方能力→政府自主谈判或底层改革冲突→真实独立后的市场、法律与防御安排。它使用实际就业建筑、财政、州市场接入、运动和条约。不会生成库存、股票、统一工业链任务、虚构政治运动或自动复国。

保留以下原行为及算术：MUG/BHT/DRA 学校／工业／社会／统一、六地区 IR 案件、TZ1/YU1 两司、B1 印度共同体与王朝值及按法组展开的进度行、所有既有团结政策。`nesnd_india_request_4/7` 只调整真实土邦分支；帝国分支和已经发送的旧印度请求继续原协议。现存印度对法援助和防御协议可继续使用，但新的 B2 请求必须同时尊重旧印度与 C1 的 pending/cooldown，不能双发绕过期限。

本轮不加具名章西女王／阿里模板。PPET 是条件式未来依据：1853–60 吴吞地引起第一次起义，1876–89 莫卧儿腐败与饥荒引起第二次起义；不能到年即复活人物或强制起义。底层事件优先使用现实存活、实际支持目标运动的人物；没有适格人物时用集体叙述，运动仍可发展。

## 2. 身份、地域与控制

`nesnd_small_state_country` 的真实定义由 B2 提供，关闭 C1 kind5 的已知外部依赖。名单只定义本轮入口，绝不代替运行态宗属或市场关系。

* 印度：调用既有 `nesnd_india_prince`，43项为 `ALW ASM AWA BAG BAS BER BHO BHV BHW BIK BUN COC COO DHA GAR GWA HYD IDA IND JAI JAS JEY JHN JOD JUN KHP KNO KOT KUT MEW MNP MYB NAG NAR NAW PAN PLP PTA PTN SAT SIN SUR TRA`。原触发器另允许 `nesnd_india_local_state`，并要求存活、集中政体、有印度人口州、非帝国。
* 南洋小邦24项：`ACE BAL BRU BLG LAN JMB SAK SRK YOG BNJ KTI TID PON SEL PRK SMB STG JOH MGD SUL LUA CMI CHP CAM`。
* 南洋区域中介6项：`PHI DEI YN1 BUR SIA DAI`。这组说明其地区角色，不再凭TAG给相同门槛乘大；真正阶段由§4.1的直接持地、人口和经济分布选择。用户明确YN1为澳大利亚＋新西兰的中等国家，BUR/SIA同属中等国家，其当前开局结构已据源码落实。DEI沿用南洋联省；YN1是远南，YU1是南非远山。
* 南洋入口另要求实际存活、集中政体、至少一个人口大于0且由本国拥有的适格州：通常为 `region_indochina/region_indonesia`；**YN1远南另允许本国实际拥有的 `region_oceania` 人口州**。这一Oceania分支只随YN1及其按本计划登记的真实B2后继身份，不向全体大洋洲国家开放。当前 C 的地域定义包含菲律宾与两半新几内亚；不套原版地域表。已登记YN1革命后继以复制的远南来源标记保留此资格，不能因临时新TAG又被本项排除。
* MUG/BHT/DRA／imperial_line、TZ1、YU1、IR1–IR6明确排除。无土的MYS不补入名单，不借IR4复国。
* 已登记国家的真实革命后继只能由 `on_revolution_start` 从原国复制 B2 lineage、已完成／已领奖标记及有限进度。战争期间标为 provisional，不开放重复发展奖励、协议或新对外战争。实际胜者通过 `on_civil_war_won` 转正；不会按任意新TAG猜测后继。和平改TAG保留本国变量；转为受保护帝国／两司即退出B2。

所有请求使用当时实际 `overlord`、`market.owner`；只直接宗主可批准自治／独立。间接宗主不能代签。市场权接收者必须是实际市场主人，且原生 grant_own_market 允许该主人给这个国家授权。开局关系文件中USM与SIA／DAI历史块有重叠，报告不裁定运行态赢家。

### 2.1 三十个南洋对象的开局地域逐项来源

本次实际读取C的`common/history/states/00_states.txt`所有有效`create_state`、三份对应POP文件及`common/strategic_regions/east_asia_strategic_regions.txt`，不把名单当领土证明。下表州名前省略`STATE_`；数字是states源码中有效country行，POP数字是对应`region_state:TAG`第一条有效`size`行。每个已列持有份额都至少有一条正数create_pop，**这是新局源码的有居民证据，不是读取存档得到的实时state_population**。分州只计各自owner-state。注释掉的JOH旧块不计。

战略区来源：C/east_asia_strategic_regions.txt:3–9为`region_indochina`（下表I）；:12–17为`region_indonesia`（D）；:68–72为`region_oceania`（O）。POP简称E=`11_east_asia.txt`、D=`12_indonesia.txt`、A=`13_australasia.txt`，均位于C/common/history/pops。

|TAG|实际开局持有州份额（states行）|战略区|逐份额有效POP来源|
|---|---|---|---|
|ACE|ACEH:4531|D|D:611|
|BAL|SUNDA_ISLANDS:4644|D|D:852|
|BRU|NORTH_BORNEO:4687|D|D:86|
|BLG|EAST_BORNEO:4621；NORTH_BORNEO:4695|D|D:303、138|
|LAN|WEST_BORNEO:4592|D|D:160|
|JMB|NORTH_SUMATRA:4513|D|D:550|
|SAK|NORTH_SUMATRA:4509；ACEH:4535|D|D:526、635|
|SRK|CENTRAL_JAVA:1641|D|D:470|
|YOG|CENTRAL_JAVA:1637|D|D:449|
|BNJ|EAST_BORNEO:4627|D|D:279|
|KTI|EAST_BORNEO:4633|D|D:323|
|TID|WESTERN_NEW_GUINEA:4551；MOLUCCAS:4563；CELEBES:4583|D|D:700、747、824|
|PON|WEST_BORNEO:4604|D|D:228|
|SEL|MALAYA:4679|I|D:21|
|PRK|MALAYA:4675|I|D:36|
|SMB|WEST_BORNEO:4600|D|D:204|
|STG|WEST_BORNEO:4608|D|D:252|
|JOH|没有有效create_state；states:4662是注释旧块|无|D:3起旧POP块也被注释；不声称开局存在|
|MGD|MINDANAO:4717|D|D:925|
|SUL|NORTH_BORNEO:4691；MINDANAO:4709；LUZON:4736|D|D:110、964、1026|
|LUA|LAOS:6771|I|E:1324|
|CMI|CHIANG_MAI:6798|I|E:1424|
|CHP|LAOS:6780|I|E:1367|
|CAM|CAMBODIA:1922|I|E:1116|
|PHI|WEST_MICRONESIA:1608；MINDANAO:4704；LUZON:4732；VISAYAS:4747|首项O，其余D|D:1101、902、989、1043|
|DEI|WEST_JAVA:1616；EAST_JAVA:1625；CENTRAL_JAVA:1633；TENASSERIM:4426；PEGU:4488；NORTH_SUMATRA:4505；SOUTH_SUMATRA:4522；ACEH:4539；MOLUCCAS:4559；CELEBES:4575；WEST_BORNEO:4596；EAST_BORNEO:4617；SUNDA_ISLANDS:4653；MALAYA:4670；ARAKAN:9386|TENASSERIM、PEGU、MALAYA、ARAKAN为I；其余D|D:370、397、424；E:1495、1717；D:493、576、659、717、781、179、343、876、66；E:1726|
|YN1|NEW_SOUTH_WALES:1392；VICTORIA:1401；QUEENSLAND:1427；SOUTH_AUSTRALIA:1436；WESTERN_AUSTRALIA:1473；NORTHERN_TERRITORY:1522；NORTH_ISLAND:1555；SOUTH_ISLAND:1583|全部O|A:6、27、60、77、108、152、172、200|
|BUR|KACHIN:4443；SHAN_STATES:4454；MANDALAY:4469；PEGU:4483|全部I|E:1561、1603、1651、1684|
|SIA|CAMBODIA:1918；TENASSERIM:4431；MALAYA:4666；BANGKOK:6738；LAOS:6775；NAKHON_RATCHASIMA:6807|全部I|E:1091、1526；D:51；E:1161、1348、1455|
|DAI|MEKONG:163；ANNAM:6762；LAOS:6784；SOUTH_CENTRAL_VIETNAM:9542|全部I|E:1265、1234、1392、2471|

因此：YN1原入口会全部漏掉，本次专属Oceania分支修正它；BUR已有I人口州，不增加虚构的`region_burma`；PHI仍由三个菲律宾人口州进入，其WEST_MICRONESIA在本国人口／财政／产业统计中仍按§4的全部直接持有口径计算。PHI若日后丢失全部I/D本土、仅余密克罗尼西亚，按失去地区根基退出本链；不会因这张历史表给它永久菲律宾资格。JOH保留为日后真实存活持地才可进入的候选，不能为凑30国补地、补POP或自动复国。

地域资格应在common trigger统一定义，由主JE入口、维护、失地invalid、旧档初始化和革命后继共用；禁止只修possible却让月维护立即移除YN1。新增后续用例明确覆盖YN1八州、其革命后继、BUR四州、PHI两区份额、JOH注释无地及YU1非南洋。

## 3. 原生完整链与适用边界

|机制|已读链条／适用|
|---|---|
|有用产业|G `common/journal_entries/00_player_objectives_economic_dominance.txt:8–24` 实际目标检查盈利、occupancy>0.75、不补贴并读取building.level；`00_opium.txt:27–34`同类。G `00_building_groups.txt`、building类型归属及D occupancy/weekly_profit/level确认对象是本国真实建筑；外国市场总产量不计本国产业。|
|财政／运输|D net_fixed_income、state_unemployment_rate、market_access、state_population；B1当前已冻结的 `country_expenses_add` 正值＋multiplier是每周费用。费用不误写为一次性金库扣款；人口占比不是全国劳动力失业率。|
|投资|C1 kind5→实际双边事件→create_treaty foreign_investment_rights→实际条款方向检查→一次限时small_capital。G `treaty_articles/07_foreign_investment_rights.txt`及条约docs证明它只是投资许可；新增正文不保证外国实际建厂／持股。经营目标仍检查国内已建、已就业、盈利建筑。|
|自有市场|G `42_subjects_request_market_control.txt:14–101` 审批请求、自由渴望25及pact市场owner；`36_subjects_grant_own_market.txt:1–53` 主人授予，pact `market_owner=second_country`、强制12月、宗属／集团维持条件。**实际事件** `the_grand_collapse_events.txt:113–135` 在原市场主人country执行create_diplomatic_pact grant_own_market。D can_create_diplomatic_pact与has_diplomatic_pact核合法性和关系。调用create不假设自动执行外交动作accept_effect。|
|共同市场|G join_power_bloc条款→集团身份／principle_market_unification_2/3→power_bloc_customs_union_bool。B2观察真实market.owner；不提供不存在的customs_union条约，也不借防御约改变市场。|
|自治|G `38_subjects_increase_autonomy.txt:107–209` 实际请求／接受increase_autonomy／拒绝催化剂；G subject_types的autonomy_level和higher alternatives；D country increase_autonomy。本批回复后比较实际subject type／等级，不能仅设同意flag。|
|独立|D make_independent；旧印度协议实际执行。G dp_independence:202–231→war_goal independence:27–31（实际宗主）→原生强制执行；G `british_raj_events.txt:276–280`实际create_diplomatic_play实例。B2和平批准可make_independent；战争路径沿用原生外交界面与AI决策，记录真实战争／独立结果，**本批不增加忽略原生资格的强制开战按钮**。拒绝自治可按原生动作创建denied催化剂，允许原生博弈入口判断。|
|可靠外援|G `03_support_independence.txt:1–33` 有方向，自动支持dp_independence／dp_increase_autonomy等。只计算生效且source→本国的真实support_independence，不把投资权、友好或防御约当作进攻独立援军。|
|防御|C1条约创建／结果验证＋G `01_defensive_pact.txt`。kind9已由root明确预留；双方均真实独立且can_create_treaty。既有联盟／防御约也可满足后续目标，不发第二份重复条约。|
|运动|G `political_movements.md` 区分creation_trigger、实际pop_support_weight与仅UI的pop_support_factors；00_ideological_movements中land_reform/labor/liberal/radical的技术／法律限定。G `agitators_election_events.txt:3544–3549`实际country modifier→`agitators_5_modifiers.txt:380–385`原生land_reform支持权重；`two_spains_events.txt:128–155`实际country modifier→00_ip4_04_modifiers:115–128的liberal/radical/labor权重。B2使用这些真实权重接口，只对已存在且满足原生类型的运动选项开放。|
|人群与人物|D add_radicals_in_state只在state、add_radicals只在country；value=.01为该POP向激进移动1%，不是敏感度。D any_supporting_character作用于movement；character_popularity_add只作用于character。选现存真实支持者，活着且在本国才应用／显示，不造领袖、不设所有人同一思想。|
|革命|G on_actions:5154–5180 ROOT原国/target起义国；5513–5518 revolution_end；5743–5762 civil_war_won在其后。原生运动自己决定革命、国家和法律结果。B2仅移交自身记录、按实际结果结算；不能国内革命胜利就make_independent。|

本计划的精确源码SHA账在末尾。来源能证明原生形状和执行调用，不代表本批已经通过引擎验证。原生pact的市场重算时序、原生运动支持的动态幅度、革命回调次序仍列为未实机验证。

## 4. 数值、分母与规模

每国月度只计算一次，JE的bar与结算引用同一script_value。只数直接拥有的实际州、人口、建筑；省区拆分不把其他owner-state加入。所有比例分母先判正，否则为0，不能因max(1)给无人口国家资格。

* `P`＝本国全部直接州人口。基础规模 `S=1`（P<100万），2（100–499万），4（500–999万），8（≥1000万）。**删除六个区域中介的`S=max(S,4)`身份加值**。S只服务于紧凑国家的最低有效产业等级及共同自卫量纲，不再代表区域国家完整目标。紧凑国家行政目标 `A=max(1,S/2)`，仅有1/2/4整数；区域国家读取地区分布目标（§4.2）。人口变化月度更新要求；已完成阶段不因规模增长撤销。
* `J=合格就业州人口/P`；合格州为state_unemployment_rate≤0.10。界面准确写“失业率不高于10%的州内人口占比”，绝不称“全国失业率”。不要求每个州达标。
* `T=market_access≥0.80的本国州人口/P`。它检查真实市场接入；不等于港口等级或独立市场。纯内陆国家可以靠陆路达标。
* `L=Σ合格生产建筑level`。须不属subsistence、不属government/army、occupancy≥0.75、weekly_profit>0、is_subsidized=no。合格集合由有效建筑定义的父group闭包生成：manufacturing/agriculture/plantations/mining/logging/fishing（包括其真实子类）；不得靠一层group名推断父类匹配行为。每建筑只计一次；外国所有但在本国雇工的建筑可计就业，仍不冒称本国持股。
* 自有市场路线的`L`还须building_has_goods_shortage=no；这一条件针对达标产业的投入，不要求全市场所有商品完全无短缺。
* `R_army=本国army_size/max(实际直接宗主army_size,1)`；`R_gdp=本国gdp/max(实际直接宗主gdp,1)`。宗主不存在则这些值为0并走独立事实分支。它们是谈判能力指标，文案不称战力／胜率。
* `economic_dependence(target=实际宗主或市场主人)`仅月度／请求时查询，按<0.8、0.8–1.2、>1.2影响AI倾向，不当作80%或单独硬锁。
* 每周公共投入报价 `C=clamp(round(GDP×0.0002),10,2000)`，开始时冻结，持续12月不可中途撤销／叠加。GDP10万→£20/周，100万→£200，1000万→£2000；约52周分别£1040/10400/104000，属于一年GDP约1.04%的年度费用，上限后占比递减。新开项目要求net_fixed_income≥C且非违约；不额外要求可支付一年费用的金库。AI另留缓冲2C。

这是明确的候选平衡参数，不是既有观察者实测。静态验收能核算量纲和边界；不能据此宣称73国的开局经济已平衡。

### 4.1 紧凑国家与区域国家：按实际结构分路

新增分支不另造一套外交货币或产业资源。常驻JE仍一个，经济与能力两个阶段各自使用互斥的紧凑／区域变体，读取同一套真实建筑、POP、市场和财政。区域变体的目标是把分散的生产、公共服务与对外关系组成能够长期运作的国家经济，不以“再多建几级同样工厂”代表中等国家成长。

**首次分类：**至少3个本国直接拥有、各有实际人口的state，且P≥200万，并可按§4.2选出两个实际人口地区及支点，进入区域profile；其余进入紧凑profile。只数owner-state，不数属国州、地图州面积或名义宣称。此阈值为本次待批设计值；YN1/BUR/SIA按当前开局直接州及源码人口规模满足，不靠永久TAG特权。PHI/DEI/DAI和较大印度土邦也按同一事实分类。一个仅剩一州的旧帝国／区域名号不会继续强求跨国土目标。

**后续变动：**月度检测；P≥200万且至少3个人口州持续6月才从紧凑转区域，P<150万或人口州≤2持续6月才转紧凑恢复，阈值之间保持既有profile，避免人口小幅变化造成反复切换。当前实际目标州失去时立刻停止相应区域累计，不能等6月继续白赚。profile更换不重发阶段奖励、不清真实资产和既有政治结果；当前阶段计数保存各自进度，恢复该profile时续算。已完成紧凑能力的成长国家需实际补齐区域能力事实才能使用区域终局，不能仅复制done；这次补齐不再发基础完成奖。经济衰落者仍可通过紧凑恢复过程重建，不会被要求夺回旧国土才能游玩。

**新成立与革命国家：**没有本批lineage的新国家按实际直接州和人口分类，完成期仍需真实达标月，不从母国GDP或旧名继承成就。已登记革命后继按§11转移其真实记录，战时provisional不领奖；胜后按实际持地重算profile与区域目标。旧存档首次进入也按当时事实，不倒填“过去已经完成十二月”。

**宗属不是规模：**YN1的殖民扩张法／共和政体、DEI的殖民行政、BUR的王朝和SIA的贡属，分别影响政治措辞、条约资格与自主选择，不把殖民国家自动降为微型经济，也不把共和国自动当独立国家。属国可以经营本地和区域经济、争取自治或市场权；只有独立者才发起kind9，普通投资许可遵守C1最终“投资人必须实际独立”的规则。

### 4.2 区域经济的地区与产业口径

区域profile从直接拥有的州选择两个**地区支点**；它们必须位于两个不同的地区组，每组至少有本国P的10%，两个组合计至少50%。这些百分比是人口权重，不是地图面积。各组选一块实际owner-state作操作与可见目标，支点州各有不少于本国P的5%人口；选择后保存具体州，不能预览一个、执行另一个。省区拆分只计本国份额。地区组及来源如下：

|对象|地区组与真实经济构成|本轮应让玩家经营的差异|
|---|---|---|
|YN1|澳洲组：NEW_SOUTH_WALES、VICTORIA、QUEENSLAND、SOUTH_AUSTRALIA、WESTERN_AUSTRALIA、NORTHERN_TERRITORY；新西兰组：NORTH_ISLAND、SOUTH_ISLAND。C/13_australasia开局已声明新南威尔士纸4／食品5，昆士兰工具3，南澳纺织5；两组都有港口。新南威尔士船厂与若干林场、种植股份有USM所有权，必须保留。|从既有加工、种植、矿产及海运出发，使新西兰渔林与澳洲加工／人口中心保持有效连接；不用“建第一家作坊”叙述。两组支点都需实际有就业的港口并market_access达标；没有要求自己生产全部船舶或独立开市场。|
|BUR|上游／内地组：MANDALAY、KACHIN、SHAN_STATES；下游组：PEGU。当前ARAKAN属于DEI，TENASSERIM由DEI/SIA分持，不能当BUR工程目标。C/11_east_asia在曼德勒有行政2、茶／稻／牧，Pegu有稻／渔／烟，Kachin有稻牧，Shan有鸦片。|联系曼德勒与Pegu的生产、行政与物资流通；可发展初级专业化，也可新增加工。下游不是“尚无出海口必须征服阿拉干”的锁；真实market_access和财政比固定港口等级更重要。|
|SIA|中部组：BANGKOK；内陆组：NAKHON_RATCHASIMA、LAOS；外围组：本国份额的CAMBODIA、TENASSERIM、MALAYA。优先中部＋实际人口最多的另一组。C/11_east_asia有曼谷行政2和兵营20，呵叻兵营15，老挝／柬埔寨各5；粮食、渔业及种植分布数州。原生国家史开局isolationism和debt_slavery。|把曼谷财政／军事集中与内陆生产和公共服务连接；现有军队的维持是负担，不再写“凑两营即可自立”。锁国未改时不承诺跨市场贸易或外国已经投资；原生允许的宗属共同市场与国内生产仍可用。|
|其他区域profile|第一组为本国人口最大州；第二组为入项时其他直接持有人口州，支点为其中人口最大的一州。两组各≥10%P，第二支点≥5%P；第二组成员以入项时实际owner-state登记。本国95%以上人口集中一州等不满足分布结构的情形继续走紧凑profile，不因拥有若干空旷小州强求区域路线。|不为PHI/DEI/DAI或大印度土邦另写无限分支；人口中心之外的其他地区必须有真实经营和公共服务；不借属国人口填分母。|

通用分组不依赖未核引擎“经济区域”数据库；两个支点和当前本国owner-state的地区标记由现有state迭代、scope与变量记录。每个标记带本轮country与项目期次，统计始终再次限定当前owner为本国；不能把转给第三国的州留在本国分母。只有最高人口州和其余州两组，不建立复杂的逐级聚类或连续地图连通算法。若一国虽P和州数达标，却无法选出第二个有足够人口的支点，保持紧凑profile并显示人口集中事实；不生成永久无目标的区域JE。

每个地区组分别统计：该组直接人口、market_access≥.80的人口比例、经营合格生产等级、至少一处实际有就业的行政／大学。不拿全国一座大学代表所有地区。生产分为农业／种植、矿业、林渔、加工四类；同一个building只计一类，加工包括已核manufacturing子类。区域经济可以走两种等价结果：①两个地区合计有两类合格产业，各类至少2级，且每个地区至少有1级真实经营产业；②两个地区各有至少2级不同type的同类专业生产，并通过真实市场取得其投入。后一项允许农牧、种植或渔林专业国，不要求每个国家建齐加工和军工。两路都必须occupancy≥.75、盈利、非补贴；自有市场路线对这些达标产业另查无投入品短缺。

地区组选择在首次进入本阶段时冻结，不能在每月把落后州换掉缩小分母。旧目标失地时暂停，并提供一次无奖励的“重订地区目标”行动，按当前实际持地重新选择、区域阶段计数归零；24月才可再重订。不能为完成目标自动征服第三国。目标变更不会清已有投资或返还已付公共支出。

### 4.3 实际源码、能力界线与轻量实现

本次读取的是C的建筑原始声明，不把等级当实时就业／利润。建筑入口行：YN1的C/13_australasia:2、198、296、446、523、580、607、690；BUR的C/11_east_asia:5641、5671、5688、5742；SIA的C/11_east_asia:5071、5142、5449、5557、5611及C/12_indonesia:2。本国建筑中的外国股份照旧，不国有化、不改历史数据。

原生多州目标证据：G/common/journal_entries/02_coffee_and_milk.txt:16–31在两个非首都州检查真实农业并区分实际市场owner；06_economic_regeneration.txt:444–465用多州的真实工业group等级和公司条件；00_major_railroads.txt:19–70对明确地区目标检查实际铁路并落完成事件。这些证明多州经营与选定地区目标的形状，不把巴西50/125种植等级、西班牙四工业州或西伯利亚铁路清单直接移植进本批。

只增加region-profile triggers/values、两个阶段JE变体及一条终局分支；继续用同一月维护、奖励幂等和外交协议。不新增国家TAG、文化、法组、产业系统、资产转移或强制战争。人口／产业构成是分类和行动依据，具体利润、财政、接入仍运行时读，不能捏造一组开局达标结论。

## 5. JE和实际行动

所有JE默认钉选。一个常驻处境JE＋按需出现的4类阶段JE；不让玩家每日点按钮领取发展数值。

|JE／阶段|完整目标与推进|行动／收益／退出|
|---|---|---|
|邦国的生计（常驻）|真实合格country；显示实际宗主、市场主人、人口尺度、就业与财政，阶段状态；不因政体改变消失|显示当前可用投资／自治／市场／防御入口；本国灭亡、失去全部本区人口州、转为帝国／两司时invalid且清临时项目；没有奖励。|
|活下去（12个达标月）|P>0，J≥.60，T≥.60，L≥S，net_fixed_income≥0，非违约，非内战。每月全部满足+1，否则+0，12封顶|已有产业允许直接计入，旧档不强迫重建。完成一次country state_tax_capacity_mult+.10、state_pop_qualifications_mult+.10，36月；不送现金／建筑。进度暂停保留，永久done和rewarded防重领。|
|地方的根基（12个达标月）|生计完成；bureaucracy≥0；本国行政等级≥A；学校机构≥1 **或** literacy≥.20且本国大学≥1；T≥.60；net_fixed_income≥0；非违约／内战|可签12月“培养地方人才”：每周C，资格+.15，税容+.10（同源不重复叠加）。它提供真实服务帮助，不直接增加阶段计数。完成一次技术传播+.10，60月并开放政府自主谈判。所有建筑、科技、机构仍由玩家／原生经济实际获得。|
|国内争议（见§7）|至少6个月持续的真实困顿／法律冲突且现存适格运动；12月组织期／24月改革承诺有独立时钟|支持、承诺改革、镇压是互斥有限行动；真实运动和相关POP改变；失败有有限后果与24月重开冷却。完成不要求先独立，也不让革命者先达到合法性50。|
|自主后的秩序（24个达标月，120月上限）|真实is_subject=no；地方能力已完成；T≥.60、财政≥0、非违约／内战；法律项、市场项、防御项全部为实际状态|24月目标达成：一次bureaucracy+.10、资格+.10，60月；done/rewarded永久。120月仍未达标：失效通知，12月冷却后可重开，保留已有产业和法律，阶段计数归零；已领奖永不重领。再附属立即停止本阶段并保留经济成果；重新独立可重新结算未领奖目标。|

生计／能力是常驻建设目标，没有假装有限“谈判进行中”的永久锁；未完成时明确显示当前实际阻碍。战争或短期赤字只是停止达标月，已完成的基础阶段不倒退。失败不删除真实建筑／人口。

### 5.1 区域profile对应的完整阶段

上表紧凑国家的前两阶段在区域profile下由以下两条互斥变体替代，不能同时出现并累计两次。成功奖励的数值、期限和唯一标记与原基础阶段相同；区别在玩家必须完成的国家建设过程。终局采用§10.1的区域分支。

|区域阶段|实际过程、达标月与行动|暂停／完成／后继|
|---|---|---|
|地区生产与市场|十二个达标月。全国J≥.60；两个登记地区组分别有≥75%本组人口处在market_access≥.80的州；全国T≥.75；两组满足§4.2的两类产业或不同type专业生产结果；非违约、净固定收入≥0、非内战。YN1另要求两组各至少一座occupancy≥.50的本国港口，验证澳洲—新西兰海运基础；BUR/SIA可用真实陆路市场接入，不加港口强制。|短期短缺、亏损、封锁只停达标月。实际市场owner变化保留产业事实，但清旧市场合作政策并重新累计该阶段；它不宣布独立市场成功。完成共享生计done/rewarded，不再要求“活下去”从零做一遍；转入地区治理。|
|地区治理|十二个达标月。bureaucracy≥0；两个登记地区组各至少一座level≥1且occupancy≥.50的实际政府行政；教育为学校机构≥1，或literacy≥.20且两组各有一座occupancy≥.50的大学；全国T≥.75、净固定收入≥0、非违约／内战。可用原12月C报价的培养地方人才项目，玩家仍须实际扩建／招工，项目不凭空给官署或大学。|行政不再仅查全国等级或首都；学校机构本身覆盖全国，故不要求每区都重复建大学。完成共享地方能力done/rewarded，开放原自治、独立、市场权的实际谈判；也开放保留高自主宗属的地区协作终局。|

“地区生产与市场”指国内不同地区能参与实际供需，不称新market已成立；**共享大市场、获准自有市场、失去宗主市场后重新贸易是三种事实**。原生能提供工具／军需的共同市场与进口都可满足需要；不增加固定交货、采购库存或一定要自产全部投入的要求。现有市场专业化政策沿用已批准12月期限、资格+.10与权威−25；区域profile选择它也不能抹掉两组产业和接入目标。仿照原生大国多州经营的检查形状，采用本国规模与地理目标，不照抄大国建筑数。

新成立国家如果已经继承真实经营资产，可以从现状开始积累十二月；这不等于继承母国已领奖标记。衰落国家恢复紧凑profile后仅处理尚未完成的基础成果；重新成长需要现有地区治理达标才进入区域终局，不能切换profile再领相同税容／资格奖励。完成计数、领奖标记、当前profile分开存，国内政治episode仍是共用的一条，不因两个经济变体开两次运动。

## 6. 两种经济策略与投资许可

“依托现有市场”与“筹办自有市场”是相互排斥的12月政策意向，改变投入与目标显示，不改变市场owner。任期结束可重新选择；已实际自有市场者可直接选择后者。未选择时也能经营并完成通用生计目标。

* **现有市场专业化**：12月country state_pop_qualifications_mult+.10；代价是country_authority_add−25，表示把部分地方经营交给商人／行会。仅在实际market.owner≠本国时生效；市场主人变化时移除旧政策并通知，不能永久保留免费收益。专业化目标按§4 L，不指定每邦必须种某一种作物，不强制生产不存在的资源。
* **筹办自有市场**：不自动脱离市场，提供kind8请求；取得自有市场后才开启12月公共投入C、税容+.10／资格+.15（与“培养地方人才”为同一费用项目，不能双开叠加）。完成生计时L要求无投入品短缺，允许进口或改PM，不要求煤铁钢枪全自产。审批失败不会收取尚未开始的建制费用。
* **外国投资**：沿用C1 kind5最终交接接口和允许候选；**出资国家必须实际独立**，不能因它在原FRA/GBR/USM/MUG/HUS名单内就放行现为属国的投资人。C1正按用户最新“独立投资人＋事件取消”要求重规划，本批不复制其旧版发送／取消语义。存活、关系、资格及真实许可方向照最终C1；投资效果名称／文字写“获准投资／资本与技术渠道”，不写已交付固定厂、就业、股票或保证投资额。协议失效／取消仍由C1清理，仅移除条件性帮助，不拆外国真实产业。原计划一次60月奖励如被C1最终修订，以交接合约为准，并刷新B2来源和显示，不擅自回退共享文件。

## 7. 底层路线：真实运动、承诺、镇压和革命

压力按当前人口／法律判定，连续满足6个月开启一个episode，不修改帝国印度起义门槛。贫困指标为平均SoL<10或turmoil≥.15的州人口占P≥.20；违约也构成压力。法律冲突只按各分组显示，绝无总称“法律影响”行。

|争议|同时需要的实际运动／法律／人口|承诺的实际法组结果|
|---|---|---|
|土地与债役|existing movement_land_reform；原生enclosure与土地／peasants>25%条件由原生创建和本批重验；serfdom/tenant_farmers或debt_slavery存在；实际peasants/laborers非空|分别列“土地制度”“奴隶制”。土地由serfdom/tenant_farmers转为peasant_proprietorship／其homesteading变体、commercialized_agriculture或collectivized_agriculture；债役承诺要求slavery_banned。选择时只承诺一项。|
|劳动处境|existing movement_labor，labor_movement技术；poor_laws无关，不以社会救济冒充劳动权利；no_workers_rights且真实laborers非空|“劳动权利”：regulatory_bodies或worker_protections。|
|种姓／公民代表|印度种姓等级实际实施＋existing liberal/radical movement及原生技术；或受排斥政治权利与实际liberal/radical movement|“种姓制度”：hindu_caste_not_enforced／affirmative_action；或“权力分配”：已承诺wealth_voting/census_voting/universal_suffrage之一。不会更改B1法组公式，也不触碰HUS法律。|

不满足运动前置时只显示现实困顿与可用经济行动，不创建政治运动、不凭空派发现代主义／共产主义，也不给经济发展flag赋予实际运动支持的假含义。

三个选择：

1. **允许地方组织**：12月目标运动对应的state_pop_support_movement_*_mult+.15（country修正，原生已执行同形）。代价authority−25；只一次对本案相关POP add_radicals=.01。它放大原生支持权重，不把15%人口强行变成成员，也不保证革命。选择实际支持运动的存活本国人物，若存在则popularity+10、12月；变量保存并逐次判活，死亡／流亡不重造。期满收束，无限循环radical脉冲不存在。
2. **承诺法律改革**：按上表存一个具体law-group目标和24月期限；相关IG认可+2、24月，给实际改法的政治窗口。选择不自动activate_law；玩家通过原生立法。完成以实际法结果核对，一次相关POP add_loyalists=.01；反对获益转移者（地权／债役：aristocrats，劳动：capitalists）的add_radicals=.005。超时仍未改法：相关POP add_radicals=.01，撤掉临时认可，24月冷却，事件明确承诺落空。新政体不能继承旧政府尚未完成的承诺锁。
3. **镇压组织**：需实际政府、合法性≥50、domestic policing institution≥1；不把这一门槛套给运动本身。12月目标运动支持权重−.15，authority−50；相关POP一次add_radicals=.02。已有革命出现时只按原生civil_war运行；不凭一个按钮杀人／把全国人口改成革命者。期满清理并24月冷却。

同一时刻每国一个episode／一种争议；新episode优先取当前实际影响人口最多的合格争议，固定平局顺序土地→劳动→种姓／代表制。事件延迟1日，选项提交时重验国家、episode serial、政体、运动和相关法仍存在；不依赖显示时旧scope。运动消失提前结束组织收益；改革已合法通过仍可成功；失去议题或政体变更撤销未履行的旧承诺而不惩罚新政府。旧事件不能清掉新serial。

原生革命开始后，经济发展暂停；本国既有运动、参与IG和原生AI决定是否革命。B2不额外创建IR国家、第二场内战或自动复国。革命胜者接真实土地／法律／宗属，并记录“国内政局已定”；若仍是属国，外部自主目标继续。没有“革命完成＝独立”捷径。

## 8. 政府自主：政治与相对能力

旧政府可保留王朝，也可以是兰芳式地方共和政府。相关IG实际执政＋government_legitimacy≥50：landowners、industrialists、intelligentsia、armed_forces至少一项；不得检查党派组合。地方能力完成、财政非负、非违约、没有内战／当前外交博弈是请求条件。

|kind|发起硬条件|接收者与实际结果|
|---|---|---|
|6 自治|真实直接属国；can_increase_autonomy=yes；liberty_desire≥75；相对军队≥.20 **或** 相对GDP≥.20 **或** 合格支持独立条款；关系≥0；遵守原生company需civilizing_mission／personal_union需nationalism与催化剂冷却|实际直接宗主；重验后increase_autonomy。保存有效subject-type对应数值，回复后必须实际自主等级提高或实际独立。未知非本机subject type不猜级别、不发这种请求。原生批准的自由渴望−30、双边60月停战及相关催化剂使用显式effects，不假设动作隐式执行。|
|7 和平独立|真实直接属国；liberty_desire≥75；相对军队≥.40 **或** 相对GDP≥.40 **或** 合格支持独立条款；关系≥−20；相同政治／能力条件|实际直接宗主；make_independent后核is_subject=no并60月停战。若变为第三国属国，视为本次未兑现而不是独立成功。|
|8 自有市场|本国当前不拥有市场；实际market.owner存活；同实际市场；作为直接属国须liberty_desire≥25，独立集团成员按原生规则；接收方can_create_diplomatic_pact grant_own_market通过；地方能力完成，相关IG执政＋合法性50；关系≥0|实际市场主人。接收方执行create_diplomatic_pact target=requester type=grant_own_market。核本国market.owner=self；若pact已在但市场暂未重算，最多30日pending verification，无奖励，deadline到未实现即失败。|
|9 防御协定|双方真实独立、存活、和平、无互战/博弈；关系≥20；原生can_create_treaty defensive_pact通过|玩家选的实际候选；成功以双边生效defensive_pact条款判定。无额外现金／军队奖。|

外援可替代相对指标时，来源国必须存活、非己宗属、不是当前宗主，真实支持条款source→本国，至少army_size≥max(本国army_size,1)且财政非违约／没有内战。真实条款不保证能够登陆或必胜；仅作为有意义的谈判资格。

**战争入口**：保留原生自治／独立外交行动与AI。B2拒绝自治明确执行原生denied催化剂，并说明原生博弈仍受关系、宗属和停战条件限制。不加入未经验证的can_start_diplomatic_play接口，也不强制`war=yes`。现存独立博弈／战争使和平请求关闭；其结算以实际主权事实判断，战败吞并为有效失败，不救援。若用户另要求强制剧情开战，须另提交完整战争链计划，不暗中拓展此批。

## 9. 共享外交事务与AI

root已预留kind6/7/8/9。C1 kinds1/2/3/4/5/11及埃及事务遵守其**最新正式交接**语义；当前用户新增的独立投资人和事件取消重规划由C1负责，本批不写这些共享文件。扩展分支放在明确的B2kind判断内，不把C1共有relations≥20错误套在独立请求上。C1冻结并由root交接后才取得shared文件所有权；旧read-time SHA不是授权回退基点。

新增动态接收者B2 send-helper：保存requester／receiver、serial、kind、双方政府类型、实际直接宗主（或无宗主）、市场主人、原subject type/autonomy、请求时版本。共用C1请求变量和nonce，不建第二套可并发canon时钟。固定国家投资按钮仍用原C1 helper。B2只在本批kind范围增加额外snapshot字段。

发送→45日clock、6月cooldown→1日到接收者事件→接受／拒绝都再次检查nonce、活国、政体和本案控制关系→执行一次→验证实际结果→仅本serial清理。接受结果未达成发“未生效”而不发成功奖。kind8仅在真实pact存在时允许30日验后期；月度maintenance也有deadline兜底。失去目标、改宗主、市场易主、政体更替、被吞并均立即使旧提议作废；下次可在冷却后按新关系请求。不会调用不存在的国家或旧state引用。

目标选择：自治/独立唯一实际宗主；市场唯一实际market.owner；防御候选为FRA/GBR/USM/MUG/PHI/DEI/YN1/BUR/SIA/DAI中适格国家，以及一个实际相邻的小邦候选。可用单个选择事件逐页列出具名存活对象；邻邦按钮取最高关系、平局GDP最高的适格相邻对象并在按钮前置显示名称，玩家确认后才发送；所有候选同一can_create_treaty检验，无空候选随机scope。不存在“法国代替所有小邦同意”。

AI发起数值是按钮月度执行权重而非宣称精确概率：公共投入8（netfixed≥2C、bureaucracy≥0、非危机）；专业化10；自治3（另要求LD≥85、army或GDP≥.25或可靠支持）；独立1（LD≥90、army或GDP≥.50或可靠支持）；市场2（T≥.75、L≥S、地方能力、netfixed≥2C）；防御2（实际独立且尚无防御）。玩家门槛按§8，不显示AI额外条件。

接收者AI接受权重与拒绝权重100并列计算：自治基础25、独立8、市场45、防御30；关系≥50加20；接收者违约或对外战争加15；申请者army比≥.40加20（独立≥.60加20）；GDP比≥.40加10；可靠support_independence加20（仅6/7）；economic_dependence<.8加15、>1.2减20（仅6/7/8）；clamp 1–95。玩家接收者始终自己选择。仅“接收者战争”是AI倾向，实际双方互战／当前敌对关系仍取消和平请求。每个数值只影响其定义的kind，避免旧C1外交与帝国印度受波及。

底层AI：承诺40（已有该法正在立法或目标支持IG执政时+30）；组织30（movement_popular_support≥.10时+20）；镇压20（合法资格、相关保守IG执政时+20）；失去合法选项不能选出空效果。国家存亡仍由原生系统决定。

## 10. 独立后的三项安排

每项以当前真实状态检查，24月达标累计期间不得只靠历史flag。

* **法律**：至少一项合法政府基础已经实际存在：官僚体制为appointed/elected_bureaucrats；或权力分配为wealth_voting/census_voting/universal_suffrage；或本批已完成的实际土地／劳动／种姓改革仍生效。君主制可以保留，不强制共和；既有合格法律可计，不虚构“新宪法已颁布”。原生法律因文化/政体被禁用时按当前真实alternative显示。
* **市场**：本国实际market.owner=self且L≥S无投入短缺；或真实与另一个存活国家共享市场、T≥.60且该市场关系并未过期。加入集团但未共享市场不算第二条，防御约不算。默认不强推脱离大市场。
* **防御**：实际独立盟约／防御条款与一个存活伙伴；或自主防御达到 `army_size≥2S`、至少S级实际军营、至少一座有就业且无投入品短缺的军营。可以靠同市场或进口供军，绝不要求每邦自造枪炮。后者不宣称战斗力足以打败列强，只是有限自卫准备的建设目标。

已完成后的真实法律和产业保留，限时奖励正常到期；后续失约／市场解散由常驻JE显示并停止尚未完成的累计。新宗主导致独立阶段退出，不能继续领取独立奖励。

### 10.1 区域国家的主权选择与地区关系

区域profile不会把“摆脱宗主”当唯一终局。地区治理完成后，通过一个有明确后果的选择进入下列任一目标，均为24个真实达标月、120月上限，并共用§5的终局奖励和永久rewarded。尚未领奖时可随真实身份改变转入相容分支，不能两路分别领奖。

* **独立后的地区秩序：**is_subject=no，保留§10真实法律、市场和自卫／防御条约条件；区域两组仍有有效产业和公共服务，全国T≥.75。另需至少一个存活的地区伙伴：本国邻接国家，或本批30国中的实际海洋／东南亚伙伴，双方关系≥20且未互为博弈敌人，并有真实共同市场、双方生效贸易／投资许可或防御／联盟条款之一。直接宗主已不存在，不能用旧宗主scope填此关系。已有关系可以计，不强制为JE重复发请求。
* **保留宗属、经营地区：**玩家明确选择维持当前高自主关系，仍为实际直接属国，且原生subject type的autonomy_level=2（本机九型映射已有来源，不能对未知type猜值）；真实宗主存活、双方无战争／敌对博弈，本国继续具有法律项、全国T≥.75及两个地区的产业和公共服务。地区伙伴条件同上，但宗主本身不能充当唯一地区伙伴；同属一宗主的邻邦可通过真实共同市场与关系构成合作。这一路只结算“地区治理与合作”，绝不写独立、make_independent、免费减贡赋或解除原生外交约束。低自主傀儡／殖民地可先走原kind6请求争取自治；被拒不妨碍经济成长，仍可用原生外交追求其他结果。

远南可以在保留南朝关系、既有外国股份和共同市场的情况下经营澳洲—新西兰，再与菲律宾／南洋的实际伙伴合作；缅甸与暹罗可以经营本国上下游／内陆，处理邻邦关系而不立即与世界级宗主决战。若玩家选独立，原kind7的真实宗主批准、相对能力或可靠外援、原生战争规则仍成立；中等国家的实际组织能力体现在跨地区建设和自卫负担，不凭一个“中等国家”flag让宗主必然同意。

地区伙伴只是现存关系的检查，不新增泛用“地区联盟”数据库。kind9仅独立国可请求；属国的投资／贸易／共同市场关系一律遵守原生资格和C1独立投资人规则，不能靠本段绕过。自己的直接属国若被用作地区伙伴，必须双方真实仍存活且共享市场、关系≥20，同时其人口／产业不计本国两个地区目标；不把附属人口当本国财政实力。玩家可保留王朝、共和或现有殖民行政，政治动作仍只要求相关IG实际执政与合法性50，没有党派组合要求。

区域profile若采用自主防御而非条约分支，还需两个登记地区组各至少一座occupancy≥.50且无投入品短缺的军营；全国army_size≥2S的基础下限仍保留。它检查军队能否在本国不同地区维持，不能只在首都堆低等级军营。财政条件读取全体现役军队的实际预算后果，不要求暹罗把开局45营维持到永久，也不凭“已有45营”略过补给／财政。选择缩减军队仍是原生可行政策，文案不把建设门槛说成击败列强的战力保证。

## 11. 地区案件、两司与继承

* 新B2外交／episode发起前，查本国实际owned-state的state_region是否有`nesnd_india_case_stage`1–3或实际IR演员／相关外交博弈。只暂停新的本批谈判和组织，不篡改原案件进度，不把整个印度无关州都锁死；已有原生运动仍由引擎运行。
* 本批不创建战争，因此不会额外在IR地区造第二个IR国家。原生内战开始则冻结经营累计并取消旧政府未执行提议；不强行结束正在进行的原生革命。
* TZ1设立／宗主转置：保留邦国实际产业和B2永久经济done；作废旧宗主请求，读取新直接宗主；被实际吞并者退出。YU1不得误当南洋入口。
* 印度和平统一：旧帝国union协议保持。B2奖励为原邦国country修正，不向统一者重新发；对方吞并后没有“被吞并但继续给补助”的尾调。若已有原协议显式继承印度标记，不另把B2done混入帝国门槛。
* 改TAG：同一country保留标记；革命新country受控移交。新释放的43名单国家可按当前实际经济重新进入，属于新的政治实体；不凭地图曾属于它而自动create_country。已灭国对象不保留需要调用的saved_scope。

## 12. 文案、UI与写作对读

使用 `nesnd-player-writing`。已读独立作者基线 `backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/`：ce_cne_events 的地权革命正文／完成／反对事件（15/69/79/81）；ce_french_empire_journals 的政治按钮237、进度248；ce_country_flavor_text 的MUG30；ce_government 的宣慰司3；ce_00_countries 的LAN409、MUG510、DEI989。原文强调利益、生产和政治冲突，不能把本批改写成办证、盖章、核册；沿用莫卧儿、兰芳、南洋联省、远南。

|类别|作者特征／候选方向|草拟示例（编辑提案，未接游戏）|
|---|---|---|
|生计JE：共享市场|原地权正文以实际生产、利益分配与制度为因果；本批先由market.owner≠self且有效market owner选择该段|“本国属于[实际市场主人]主持的市场。商人希望借此扩大销路，农户和雇工关心的则是收成与工资能否维持生活。地方产业能得到多少原料、把货物运到哪里，仍受交通和市场供需限制；经营所得如何分配，又牵涉国内的税负、地租和用工规矩。”具名市场对象必须在显示时存在；只写真实市场归属，不在市场接入低下时假称运输已经畅通。|
|生计JE：自有市场|市场主人确为本国时使用；对居民、企业与政府分别叙述|“本国政府掌管着市场，原料、工具和军需仍须由生产或进口取得。征税和养军所需的收入来自居民的劳动；农庄、作坊和矿场能否经营下去，也决定了政府能维持多少学校和军队。外国商人若获准投资，还须谈清他们能取得什么权利。”该段不预告已经取得投资或已有特定外国厂。|
|政府自主：现为属国|作者MUG正文把外援与自主利益并列；本段只在有效直接宗主存在时出现，以政府为主体，不把30国全写成王朝|“本国与[实际宗主]的宗属关系仍在延续。政府准备争取更大的自主权，军队和财政却未必足以承担独立的代价。地方商人与有产者愿意为此支持政府到什么程度，又会要求哪些权利，这些分歧已经不能回避。”实际君主政体才可在专属分支提宫廷；共和国称共和国政府，其他政体保持本国政府。不把保护国、傀儡、贡属的税务和驻军权限一概写成相同。|
|自主后的秩序：独立|实际is_subject=no后才出现；不假定它刚由战争独立，也不假称已经脱离共同市场|“外交和国防由本国政府决定。共同市场可以继续提供销路与原料，独立市场也需要贸易伙伴；与邻国缔约能分担防御的开支，却不能代替本国的军队。曾支持政府争取自主的人，如今也在要求自己的意见进入法律。”最后一句仅用于本批实际完成自主过程的国家；开局已独立者改为“围绕税赋、土地和用工的分歧，也必须在国内得到处理。”|
|底层事件：土地|作者flavorCNE.4列具体利益转移与阻力；仅实际土地案，不能凭debt_slavery一项混称佃户案|“地方的佃户和农民要求改变土地分配。支持这项运动的人已开始联络村社，地主则担心失去租金和支配土地的权力。政府须作出选择：允许他们公开组织，推动土地改革，或动用警察阻止集会。”仅实际movement_land_reform及对应土地条件调用；债役、劳动、种姓和代表制各有独立正文，不从本段替换名词。|
|选项|作者flavorCNE.4.1有立场；本批动作与实际effects对应|“让他们公开组织。”／“这项改革必须交到议事桌上。”／“派警察解散集会。”精确期限、支持权重、激进化和权威成本由tooltip显示。|
|按钮／状态|作者政治按钮表明阵营，进度desc只读数；本批需显示真实对象|“向[实际宗主]请求自治”；待批／拒绝／已独立／市场尚未分离分开，绝不写已成功而effects未确认。|

实施须产出完整中英文专用文件，按键对读报告记录“作者样本→初稿→effects→最终CN/EN→通过/返工”。英文不以中文占位。所有JE、事件t/d/f/选项、按钮、status、bar、cost、失败原因、modifier、外交kind动态loc都有归属，不留root补写。预估约130–180对有效键，最终以实际引用闭包为准。

原生bar分别显示“就业”“财政”“市场接入”“有效产业”“行政”“学校”和具体法组名；月度达标+1只有一条真实delta，不能把多个勾叉各算+1。法组条目绝不合并为“法律影响”。原生条件优先，custom tooltip仅用于人口权重／规模L之类原生无法自然表达的统计。正文不写“serial、运行态、同源、验后、闭包、继承补漏”等开发说明。

### 12.1 本次返工记录与实际政体依据

本次按nesnd-player-writing再次回读不可变作者样本`ce_cne_land_reform_reason`、`flavorCNE.3.d`、`flavorCNE.4.d`与`MUG_FLAVOR_TEXT`。作者正文具体交代生产关系、利益转移、外援和政治主体；据此修订的规则是：**先选择当前国家实际的市场与政体分支，再叙述受到影响的居民、产业和政府；不以一条抽象商路故事给所有国家安排相同政治主体。**这条是本次计划编辑规则，尚未写入永久技能。

|原候选／问题|原文对照与事实依据|修订决定／判定|
|---|---|---|
|“王公的岁入……同一张商路网”|作者地权正文明确区别土地所有者、农民、城市雇工和统治集团；G有效`lan - lanfang.txt:10`为总统共和，C/YN1.txt:42也是总统共和，不能统称王公|返工为共享市场／自有市场两段；政府与居民、产业分别承担动作。编辑提案通过，未接游戏。|
|“船舶带来……宫廷……宗主”被用作所有南洋独立叙述|BUR四州可走陆路；C/DEI country史是殖民行政＋寡头，LAN/YN1共和国；原作者MUG说明只为莫卧儿特定王朝作判断，不是通用模板|返工为实际属国／独立两个分支，通用主语“本国政府”；只有实际君主条件下才出现宫廷。编辑提案通过，未接游戏。|
|土地事件同时写佃户与债户|原作者flavorCNE.4逐一写明利益承担者；B2承诺实际只选一个法组，土地和债役是不同条件|本段限定土地案，债役另稿；禁止只因任一法律满足就在正文宣称两项都存在。编辑提案通过，实际落库仍须逐键核effect。|

LAN的国家史不在C内同路径，因此依法继承当前GAME同名文件；这属于已核有效加载来源，不是用旧候选或存档回退缺少的B2函数。后续所有本批helper都在C正式定义，缺失则停止并报告，不建立stub或从COLD候选复制兜底。动态政体判断使用实时法律，不能永远按开局共和国写LAN/YN1。

## 13. 文件所有权与编辑边界

新增专用文件（均C下，root批准后）：

* `common/scripted_triggers/nesnd_small_states.txt`
* `common/scripted_effects/nesnd_small_states.txt`
* `common/script_values/nesnd_small_states.txt`
* `common/journal_entries/nesnd_small_states.txt`
* `common/scripted_buttons/nesnd_small_states.txt`
* `common/scripted_progress_bars/nesnd_small_states.txt`
* `common/static_modifiers/nesnd_small_states.txt`
* `common/on_actions/nesnd_small_states.txt`
* `events/nesnd_small_states.txt`
* `localization/simp_chinese/nesnd_small_states_l_simp_chinese.yml`
* `localization/english/nesnd_small_states_l_english.yml`

窄改existing：`common/scripted_buttons/nesnd_india_diplomacy.txt`仅request4/7真实prince分支的possible/effect/AI；`common/journal_entries/nesnd_india_core.txt`仅旧prince JE加`NOT small_initialized`的失效迁移，避免双常驻窗口。旧JE不移除所有国家条件、不碰society或B1政策。新的常驻JE保留旧prince法援／防御入口。原印度send/reply脚本不改，旧请求靠原maintenance终结。

C1交接后扩展：`common/scripted_triggers/nesnd_canon_diplomacy.txt`、`common/scripted_effects/nesnd_canon_diplomacy.txt`、`events/nesnd_canon_diplomacy.txt`，必要dynamic loc按现有实际注册文件增加6/7/8/9。优先让新kind调用B2 helper，减少共享函数改面。C1既有kind5按钮无需改名。任何共享本地化文件在交接manifest列明再窄改；不在C1修复／测试期间写入。

不修改history、population、地图、laws、political_movements数据库、character_templates、G／其他MOD／main。**禁止再运行prepare_canon_data.py**。通用on_actions采用独立文件且核叠加注册，不覆盖原生code_on_actions。无需新贴图，引用已存在的native event_trade/newspaper/law图标。

## 14. 冻结与后续测试计划（本阶段不执行）

编辑期间完成全部代码、中文、英文和写作对照后一次冻结B2 modified+dependencies（含B1 protected与C1交接SHA），记录每文件SHA／源合同／内容差异。停止编辑后由root授权测试。依次：实际ordered-AST边界与旧行为回归→实际MCP语法／对象／scope查询→基线对比Tiger→完整引用、loc和资源检查。不得把mutating整C叫冻结SHA。发现实际玩法错误先停测试，窄修复→refreeze→重测。

必测矩阵：

1. 精确43／24／6名单；活国、中央／分散、无人口、split-state、实际owned/controller、帝国／两司／IR排除；南洋变宗主不依赖TAG表。新增YN1八个Oceania州及其真实革命后继、BUR四个I州、PHI的菲律宾/Oceania混合持地、JOH无有效开局州、YU1不属于南洋；入口、维护和失地invalid采用同一地域资格。新增区域profile的P=150/200万、人口州2/3、六个月转换、地区10%/支点5%边界；人口集中、失去支点、一次重订、改TAG／革命后继不重复领奖。
2. P=0、99.9/100/499/500/999/1000万人，区域中介下限；S/A/L按全部有效building-group祖先；不重计建筑；外国市场产量为0贡献；occupancy=.749/.75、profit=0/正、补贴、短缺。
3. J/T人口加权、就业率边界.10/.1001，market_access .799/.80；财政−1/0、违约、内战；12个月及多JE同月不多脉冲；状态丢失暂停、已完成不重领。
4. 费用GDP零／低／中／上限；每周量纲、冻结报价、12月不取消／不叠加／不额外金库门槛；旧任期结束不清新任期。
5. 两条策略都不直接改market.owner；kind5只有真实投资许可，仍需实际建筑；市场授权接收者为actual owner。grant pact前后方向、12月forced期限、30日验后成功／失败、主人死亡／第三方接管。
6. 自治type9项全部实际level映射，can_increase边界；军队/GDP分母0；比率.199/.20/.399/.40；LD74/75；合法性49/50；相关IG执政／党籍无关。支持独立条款方向、失效、弱国／宗属／战争不能冒充援军。
7. 双协议pending/cooldown；所有6/7/8/9 stale serial、regime、actualoverlord／marketowner变更、死国、空对象、拒绝、超时、接受后实际失败；old event不能清new request。
8. oldIndia empire按钮与send/reply保持AST一致，prince单独新路由；旧印度inflight能终结。C1kind1/2/3/4/5/11与埃及、B1所有算术／lawrows／政策逐项差分无回退。
9. 运动实际type／tech／laws／nonemptyPOP全组合；无适格movement无modernfaction；UI pop_support_factors不被当effect；12月支持权重与一次.01/.02真实POP移动；24月承诺成功／失败／改政体；无空character无复活。
10. 原生革命前／中／胜负、原国与target映射、奖励和移交唯一；国内胜者仍属国不算独立；不创建第二IR案件；两司成立／印度统一／fullannex／失地／改TAG清理；后继只取得实际应有记录。
11. 独立整合法律/市场/防御的全部真实分支，其他集团无customs_union不能假通过；期限120月、24个达标月、失败重开、再附属；旧存档initialized缺失但done存在不能重领。
12. 全部active loc键、动态country/character安全引用、原生预览与实际effect量纲、双语内容／法组名称／AI专属条件不泄漏；资源存在，UTF8 BOM。
13. 区域两地区分别统计产业／接入／行政，不能用全国一项代替；两类产业与同类不同type专业化都可达；YN1两个地区实际港口、BUR/SIA无港仍可陆路达标；区域自卫两地区军营与真实财政。保留高自主宗属终局不触发独立效果，独立后再完成不双奖；地区伙伴只有真实生效关系，kind5投资人必须独立，C1取消／超时按正式交接回归。该项仅列未来用例，本阶段不执行。

测试报告只能按实际结果给`STATIC_PASS/ENGINE_NOT_RUN`。本任务禁止游戏启动；本批不会声称市场重算、运动人口支持或革命继承已经实机通过。

## 15. 已批准项与实施关口

root已批准原计划数值、阶段和“武装独立沿原生外交入口、不增加强制开战按钮”的范围，kind6/7/8/9均已预留；修订1的地域／文案改正保留。用户最新明确中等国家定位后，本次提出以下**新增待批准决定**，不把它们伪称此前已批数值：

1. 删除六TAG的S下限4；改用P≥200万、至少3人口州和两实际人口地区选择区域profile，150万／2州与6月滞后处理衰落、成长。
2. 两个地区组各至少10%P、操作支点≥5%P；指定三国实际地区组，其他国采用最大人口州＋其余直接州。12月地区经营与12月地区治理取代紧凑两阶段，市场接入人口占比提高至各组／全国75%，两类产业或同类不同type专业化均可达；行政分布和YN1实际双区港口成为目标。奖励、公共投入C及其期限不加码。
3. 增加一次目标重订及24月冷却；失地立即停累计，改profile不重领，已完成紧凑能力者只补实际区域能力，不再拿基础奖。
4. 区域终局增加“维持真实autonomy_level=2宗属＋实际地区合作”的可选出口；与独立终局共用24/120月和唯一奖励。区域自卫要求两组实际军营，地区伙伴只认真实市场／条约与关系，不强制造新联盟或战争。

C1 shared正依最新独立投资人／事件取消指令重规划；其正式交接之前不写共享文件、不使用旧读时SHA回退。后续代理先对本修订作计划整合／审查，再由root明确GO，才实施所列阶段、请求、政治事件和中英文；完成编辑冻结后再由root授权测试。最高目标仍是最终实施、核验并入主MOD，这份计划不是交付终点。

**本代理本轮状态：PLAN_READY / STOPPED。**按最新模型分工指令保存计划后停止，不进入玩法或测试。当前代理沿继承配置运行，配置未公开，不能给出可核验的模型名；后续显式模型分工由root安排，不将计划作者身份伪记为某一模型。

## 16. 源文件指纹

以下为只读计划取证时SHA，不是待交付candidate冻结。C1仍可能修改其拥有文件，实施开始必须记录其正式交接SHA并基于交接版本窄改。源码行号见§3；其余来源以所列完整文件及已引用前置研究为入口。

版本目录核验：catalog.py status＝CURRENT，1.13.11/build24799966，changed_count=0。以下70个文件只读取证（含地域／政体与中等国家分支修订新增来源）；不存在新玩法冻结或执行测试。

|类别|文件|SHA-256|
|---|---|---|
|C candidate read-time|[nesnd_india_core.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_india_core.txt>)|`0622fab14d4db5208359b7d182fd76633926c28daa316487ac7f4fb718226548`|
|C candidate read-time|[nesnd_india_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_india_diplomacy.txt>)|`4552ac3a8ae1dc6468ed00efc19b12a417e79c83ebd0b0919cca6d2a04d96e1b`|
|C candidate read-time|[nesnd_india_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_india_diplomacy.txt>)|`8021ffc24d62850d79cdcbf0f155bf81ef88c3a7c651de610635a756c10326e9`|
|C candidate read-time|[nesnd_india_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_india_diplomacy.txt>)|`4af1617e360ded6b76f430f7eba59c1b79432c99fbb842efcf97b9cd86f80e39`|
|C candidate read-time|[nesnd_india_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/events/nesnd_india_diplomacy.txt>)|`31c9f3769fc5e2e969c31c6f56ba168e35b886cde600dd196c407bb9a9ed4f77`|
|C candidate read-time|[nesnd_india_core.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_india_core.txt>)|`c6901de919fffe76f73479acb2621b56aab630722f58be7963cd1b08d5f298c7`|
|C candidate read-time|[nesnd_india_uprising.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_india_uprising.txt>)|`812f719631b498b825a0b12e86eacb54b70209ff84c7e78a48f0f8e806583d82`|
|C candidate read-time|[nesnd_canon_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_canon_diplomacy.txt>)|`03e0bc00c96836c96d2410d2739427ea1ed63e917b69fbb796e84526aac444e6`|
|C candidate read-time|[nesnd_canon_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_canon_diplomacy.txt>)|`91e79671b76e2f0467c60606590e529fc3435fed7eb9385d2fa8417f7cdced32`|
|C candidate read-time|[nesnd_canon_requests.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_canon_requests.txt>)|`4f8947e3d1fa23d11a4bd6bb8eb5189dbc6d4c9185b4edeb724dce39d260a9ed`|
|C candidate read-time|[nesnd_unity_policies.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_unity_policies.txt>)|`156bf63af00bbb1270000ceab3c87f4260f715504e4e9136719c75dedecd5aee`|
|C candidate read-time|[nesnd_unity_policies.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/static_modifiers/nesnd_unity_policies.txt>)|`f481f4d46421ab5807a9a50117dc775e2e844aeb792e9db45a19f28e55cbc9f3`|
|C candidate read-time|[east_asia_strategic_regions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/strategic_regions/east_asia_strategic_regions.txt>)|`4aeb8c1ac1b4c5af3262035f885b78d1dca86af3fbcb18129e57df75be21670b`|
|C candidate read-time|[ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/diplomacy/ce_subject_relationships.txt>)|`78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7`|
|C candidate read-time|[00_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/diplomacy/00_subject_relationships.txt>)|`179816a2002336a2fa6a45c6bdec264fa683729a9e220b66dff3906e82fb089a`|
|G 1.13.11 build24799966|[00_player_objectives_economic_dominance.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_player_objectives_economic_dominance.txt>)|`7fb15aab732c9ce9f93c4f3a86265de98aaef64b1d9fdb4a4dd8174ec8e12599`|
|G 1.13.11 build24799966|[00_opium.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_opium.txt>)|`7aa000f4e516ced02003ac08307406f191e4651b7e1ca608087f4a3a555d5e4e`|
|G 1.13.11 build24799966|[00_building_groups.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/building_groups/00_building_groups.txt>)|`3d6e088d4fa5429653382738bd37b9a1beadce9a7c3f03bd537620267d02d37d`|
|G 1.13.11 build24799966|[42_subjects_request_market_control.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/42_subjects_request_market_control.txt>)|`88c081fb87846a98b78345fbda4e62e878184a08f161512a5c09baaab45699d1`|
|G 1.13.11 build24799966|[36_subjects_grant_own_market.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/36_subjects_grant_own_market.txt>)|`ad712dcfe896c0255eedf87ab979859c3e0702c56b8fc57370b7d61c71a076b3`|
|G 1.13.11 build24799966|[the_grand_collapse_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/the_grand_collapse_events.txt>)|`f03774a0931676331f55ac45a8316a9d8a4e00d53ec70596e6b7fcfc43316e78`|
|G 1.13.11 build24799966|[38_subjects_increase_autonomy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/38_subjects_increase_autonomy.txt>)|`c7e43033ad2684f579ea72f80f180bd08553d4064942fe892e11ec2842172d56`|
|G 1.13.11 build24799966|[00_subject_types.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/subject_types/00_subject_types.txt>)|`97a488157dfb2f340cca06aba30bfef42a36ea0a48dce6e591c8891628a6b91d`|
|G 1.13.11 build24799966|[00_diplomatic_plays.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt>)|`4f4c61ad1198cc1b862e6399fb08cff7813be815d8c3644b08e3d43a708c00a9`|
|G 1.13.11 build24799966|[00_scripted_triggers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt>)|`66432c31661d560146707744da29475cae92bbb6cbe432a1f0409133c92a3178`|
|G 1.13.11 build24799966|[10_independence.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/10_independence.txt>)|`4ef3498504a15eae8264f2839ef980202104c633e6c30a3e6e7d92d7c4d15eae`|
|G 1.13.11 build24799966|[british_raj_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/british_raj_events.txt>)|`9e3918a3a19bc34401d5af419b8a25fbf15ffa61c6169efddfd310a6fcb7db7c`|
|G 1.13.11 build24799966|[01_defensive_pact.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/01_defensive_pact.txt>)|`92c8eeafabaf8f1d10627d84531dd84d93c4c54e941596929c2202f2905fddb2`|
|G 1.13.11 build24799966|[03_support_independence.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/03_support_independence.txt>)|`37b2b31fe0d6266c2001ec5d966fd57dfd8452d9a85d51b7a89294d1d8377c29`|
|G 1.13.11 build24799966|[07_foreign_investment_rights.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/07_foreign_investment_rights.txt>)|`d1e4b58b2bdd5bf931e02b65ed89d4c8ef952611eef6558852af8360fdc20bf1`|
|G 1.13.11 build24799966|[09_join_power_bloc.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/09_join_power_bloc.txt>)|`9178a5b409a33634b557420b8730b01bf4f73991b23ad868602dc3aa22d63223`|
|G 1.13.11 build24799966|[political_movements.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md>)|`4842b165656f0741cc0baad97b2d82836f9097f64ce5b43ca4559c9d733e22c6`|
|G 1.13.11 build24799966|[00_ideological_movements.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt>)|`834a1b97f09c65b9b64eafdaffe4ee68965aaac262066140793a482eefd23a6b`|
|G 1.13.11 build24799966|[agitators_election_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/agitators_election_events.txt>)|`f4781ed233e88abc3e56371a9ce827b54ffd945d4872bb126c0917815e54c19c`|
|G 1.13.11 build24799966|[agitators_5_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/agitators_5_modifiers.txt>)|`118c439c6fd26bea041de27e10014da78c07592c9c0a49cb953a8dd17250af0f`|
|G 1.13.11 build24799966|[two_spains_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/two_spains_events.txt>)|`f8c6931d1e44fc6e7bc49c13e172d13b263fd2e742cc53d64012cfe3ea75ce46`|
|G 1.13.11 build24799966|[00_ip4_04_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip4_04_modifiers.txt>)|`a514e1fa61aa2178182506c90eb138f4bea53ad341fc20f9dbc1b6dbc5a7bf5c`|
|G 1.13.11 build24799966|[00_code_on_actions.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>)|`ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb`|
|G 1.13.11 build24799966|[01_land_reform.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_land_reform.txt>)|`2a6c33fb5c9c44c5876dfb066fc34379b48f382fafa322f483d6d4df02f57a9b`|
|G 1.13.11 build24799966|[02_labor_rights.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/02_labor_rights.txt>)|`78c4f45f9f3e0a5b3ecdaf03a8ea6ede6ade46eb1de64ae31621e4ecdfe8c371`|
|G 1.13.11 build24799966|[00_caste_hegemony.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_caste_hegemony.txt>)|`0c31a075766c3fc3db997e23b9aa61d737fe0c4c1086a5c8f501a2d03eecbae8`|
|G 1.13.11 build24799966|[00_distribution_of_power.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_distribution_of_power.txt>)|`014b5fcb89d4e4abb86c98c013364117a183daf569c9cb8d4ab0bb5ff833cd04`|
|D engine docs|[triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log>)|`ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`|
|D engine docs|[effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>)|`24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`|
|D engine docs|[event_targets.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log>)|`cc12b15da310d0d8ef10a9209107b4d2298a882fa6ee038c202650e3c9bd7c71`|
|D engine docs|[modifiers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/modifiers.log>)|`1d8ea1f6fb6bc0e2677d4591d45e21ef8f94ba4931074aa871583d61a63ceeff`|
|A immutable author backup|[ce_cne_events_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml>)|`3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a`|
|A immutable author backup|[ce_french_empire_journals_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml>)|`352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844`|
|A immutable author backup|[ce_country_flavor_text_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml>)|`a63e35b23b57f2149038acb939b9f6c65fdeceee7fe63829384d941ea5de5071`|
|A immutable author backup|[ce_government_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_government_l_simp_chinese.yml>)|`1fd33e98daf7a2febf3959d431ca88010eff3f1081cb655b276e66d0a113c865`|
|A immutable author backup|[ce_00_countries_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_00_countries_l_simp_chinese.yml>)|`9475fd3a1943de06f95c608e3ff36a2bd5161c786cb767152a36e71496c0e24d`|
|Spec/reference|[small-state-survival-plan.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/regional-expansion-20261104/small-state-survival-plan.md>)|`4b9817df3e79fddd7f90081805baf9e71a721739debf8f4723dd0247648ca3fa`|
|Spec/reference|[remaining-batch-contracts.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/remaining-batch-contracts.md>)|`f5b3a68f93a3b0212f323138441c8f4ca51dbb64ad4c77d078aea481836a07f9`|
|Spec/reference|[integration-native-contract.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/integration-native-contract.md>)|`25a415aa889550f084dc7addf474be7308b4cec2abea989477bf55c1eb64e2c7`|
|Spec/reference|[北明ppet.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt>)|`227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`|

### 本次修订新增来源

|类别|文件|SHA-256|
|---|---|---|
|C candidate plan revision 1|[00_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/states/00_states.txt>)|`a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`|
|C candidate plan revision 1|[11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/pops/11_east_asia.txt>)|`85b9ef1a805b3b033fb31009b55d270c8d83736749c6255f8d1f4ab45711fd6b`|
|C candidate plan revision 1|[12_indonesia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/pops/12_indonesia.txt>)|`4edfc72f48cf30abe74518dd1af81bc0e4d1683518825f005fbafedde1323a29`|
|C candidate plan revision 1|[13_australasia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/pops/13_australasia.txt>)|`8b12ed15ffdd378d7d0e337753453eadaa13a1d88f8f3aeeaf1aae9436309d5e`|
|C candidate plan revision 1|[YN1.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/countries/YN1.txt>)|`bfc0212a795e20232d436c1aec5acbe12c1a30921cc87ac93a5e0a9ed3ae3758`|
|C candidate plan revision 1|[dei - dutch east indies company.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/countries/dei - dutch east indies company.txt>)|`2516822c3e217c816274c746fe95281fa9198061b64eacb3d7d350bd4de650a2`|
|G effective inherited source 1.13.11|[lan - lanfang.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/lan - lanfang.txt>)|`ff2ea9e08a7ec802d12d5d6bb5f6314f009d1790e736ff81d08bbfc16370aedc`|

### 修订2新增中等国家来源

|类别|文件|SHA-256|
|---|---|---|
|C candidate plan revision 2|[11_east_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/buildings/11_east_asia.txt>)|`4879dbe1af1d432616d3954b7154b79ae28169cbfe715e68fd1dfa583a9c5238`|
|C candidate plan revision 2|[12_indonesia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/buildings/12_indonesia.txt>)|`31a1cef508511d7ac902bcc383ad156096ade6daedfc83fd1401e3f4cb643ce8`|
|C candidate plan revision 2|[13_australasia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/buildings/13_australasia.txt>)|`d0adc4c5ac40bbcb76887f8718fd061c10bf682fad01b12aabe7dc6c30342e4a`|
|G effective inherited source 1.13.11|[sia - siam.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/sia - siam.txt>)|`43d31e138a2faa57079c5797b5badac1e91842c0db4d6310f79c65a9cd433cae`|
|G effective inherited source 1.13.11|[bur - burma.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/bur - burma.txt>)|`af47cc71f73c24c7e3e24f3860924fa2e7b1ca9a7a13615974fc7c568bbe6bb3`|
|G regional plan primary example|[02_coffee_and_milk.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/02_coffee_and_milk.txt>)|`1370648361ab0b65020b93ff20f6da62b134378dc1d57ec187642f5c9403fc59`|
|G regional plan primary example|[06_economic_regeneration.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/06_economic_regeneration.txt>)|`7bcacb34f6ad1e6f19a7177476b61306f97babeb6ea67b972c7ad2b8c1fdd087`|
|G regional plan primary example|[00_major_railroads.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_major_railroads.txt>)|`14592b73831f8899cd089604fc4f3d1961b858e06cce09cefcb9dc5c3e2c8c9f`|
