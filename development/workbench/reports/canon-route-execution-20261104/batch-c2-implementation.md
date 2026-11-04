# C2 三国路线与十八人物实施 / READY_FOR_TEST

2026-11-04。实际显式配置 **gpt-6.1-sol / medium**，依据父委派NEW_TASK；角色由C1独立验收转任本批GO授权实现。未声称读取到单独的运行时模型元数据。架构、数值最终判断与合入仍归root。

**全部候选编辑已停止。状态仅READY_FOR_TEST / ENGINE_NOT_RUN。** 没有运行行为矩阵、Tiger、MCP或游戏，没有合入主MOD。源码parser只用于读取原生完整链和构造精确span补丁；没有把这类编辑操作记作验证PASS。

## 精确对象与阶段

候选：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\canon-route-execution-20261104-a`。最终owned冻结：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c2-owned-freeze-20261104T155623Z\mod`。28份owned文件及SHA在batch-c2-freeze.json与冻结目录freeze.json。冻结中没有QA事件、工具或测试档。

最终副本明确替代`batch-c2-owned-freeze-20261104T155044Z/mod`。首次副本发现收尾闭包尚需补充后降为IMPLEMENTATION_CHECKPOINT_SUPERSEDED，未测试、未覆盖、原样保留；最终副本使用新时间戳。两处收口分别是永久dead/retired阻止首次人物叙事，以及诸邦已接受协定失州/当前关系失效的结束和主动退出。已支付费用不退，承诺费用继续到原期满，旧nonce不能取消新请求。

## 完成的代码与玩家过程

- 三国各一常驻议程，10类工程/政治项目。常驻议程保留行动入口，开始后才进入对应施工JE；country月维护独占观察写入，JE不再各自重复结算。实际目标州在开始前保存，预览与执行读取同一对象，工程保存期初等级、选择、报价、观察月、成果和已领奖记录。失地/违约/相关战区/经营或政治资格不达标暂停或结束对应安排；玩家可在本期支出结束后重订，旧奖励不重发。
- 生产工程按目标owner-state实际合格组等级E0计算`ΔE=max(2,min(8,ceil(.2E0)))`，达到增量后75%就业、正利润和80%市场接入连续三月。学校/行政/交通采用实际设施、50%就业与对应学校机构条件，学校不要求利润。新项目冻结周报价`clamp(round(GDP*.0001),25,2500)`，十二月费用，最多两个有费用/进行中的工程；玩家非违约且净固定收入承担报价，AI再用两倍报价缓冲。费用是原生country_expenses_add乘冻结报价，没有一次扣金库或月费替代。
- 意大利保留法国主导LOM共和国、原生ITA形成和各邦主权。公共军需、商人融资、地方学校三类起点具有不同设施/政治承担；四种政治方向是立场，不自动改制或兼并。C2自有逐邦请求有90日回复、双方宗主与政体快照、单调serial、替代提案一次、接受/拒绝/取消/超时及十二月再议。接受后两国各付十二月费用、各有实际公共服务，双方连续三月履行才记一个独立伙伴；两个真实伙伴或实际ITA后进入预算整合。普通防御约与法国kind3信用不计为逐邦履约或军保/吞并许可。已接受协定可主动结束，失州及不再互为当前协议会结束本期，原费用不提前撤销。
- HUS复用A1原HUS边界，排除native_successor/retired；没有更换登记、阶序或普通公民法。通洋/大陆交通、蒙古牧道/补偿/驻军、债役后教育与公开账、实际油业的特许/地方收益/监督均有自己的目标与选择。债务奴役的实际原生废除另作观察事件；保守教育成果与真实改法事实分开。A2实际人口/领土变动会使目标重验，不创建第二场战争、不搬人口、不造油井。退出旧路线只撤C2临时帮助与人物背书。
- USM或实际明廷继承国读取明存/吴代/停战事实与西部四结果。相同明吴冲突优先暂停政治程序，矛盾身份标记暂缓政治终局；经济不因无关全国战争统一关闭。礼法三项先议资格、后实际观察，内阁六部/单院礼议院/布政司/学政分责明确；没有假造席位、上院或直接颁布普通游戏法律。学校与实业可并行，分配后继读取两个实际成果；旧西部失败0.25和1850期限完全未调用或修改。独立西府可留住同一个段敬川，教习交流由其真实接受/拒绝，不转国、不复造、不授予省级治理权；段只有经过本批实际资格流程且仍有公共角色，才出现学政资格通知。

## 十八人物与终身身份

18份唯一模板采用integration合同的文化、home_region、IG、思想和真实出生年；1月1日只是引擎生日技术占位。每人一件具名出现事件、一件后续/组织续行事件；男性使用真实非领袖politician角色，女性使用有法律、空槽、现有相应运动条件的agitator/公共组织者路径，不直接成为官员或IG领袖。塞雷尼默认讨论军费/工程，不免费授general。

全球introduced/seen/dead/retired/closed/pending分别记录。故事只有一个create通道，on_created才写seen；先查询全球人物、流亡池和void，外国现有人物只作访问/原生邀请，不强夺。永久dead/retired/closed既阻首次调度也阻create，已seen却已无幸存对象的历史关闭，不刷新出生日期。每国31日出现锁保证同月不连续刷人；个人离开、退休、死亡会清背书，工程成果与组织议题不随个人一起消失。死亡使用独立on_character_death窄hook，未复制全局原生on_action文件。

18人逐个门槛/事件/角色/出生窗记录在batch-c2-person-implementation-index.json；不是只交名单或模板。

## 原生意大利窄兼容与来源

GAME 1.13.11/build24799966；本轮入口catalog为CURRENT、changed_count=0。实施前读integration-native-contract与Luna导航、旧专项Garibaldi审计，并定向回读原文件：

|链|原生实际来源与本批用途|
|---|---|
|政治资格与JE|common/journal_entries/00_liberalism.txt:54起：相关IG执政与合法性50；经济项目不复制组阁条件。|
|周费用/冻结报价|当前MOD nesnd_unity_policies scripted_values/effects的报价→multiplier→country_expenses_add；GAME crime_events.txt:160起原生add_modifier multiplier；script_values.md:33–40的min下限/max上限/round/ceiling。|
|目标实际等级|GAME script_values/je_values.txt:74–100的every_scope_building累加this.level；当前数据库building_barrack为单数，已据05_military.txt:3使用准确ID。|
|人物角色|character_templates/country_arg.txt:146–172→character_roles/00_auto_assigned_roles.txt:174–208；角色池politician不等于IG领袖。|
|流亡/死亡|garibaldi_events.txt:174–198；character_interactions/00_character_interactions.txt:997–1088；00_code_on_actions.txt:2604及2702–2716，根scope是Character。|
|形成与分离博弈|country_formation/00_major_formables.txt:54–101；italian_unification.txt:57–169、644–674；00_code_on_actions.txt:5530–5570传入真实scope:target。|
|真实取消|iberia_events/independence.txt:22–28；没有写on_cancel/cancel_effect。|

全部源SHA与只读依赖快照见batch-c2-implementation-source-hashes.json。源编辑细账见batch-c2-native-source-manifest.json。

获准修改的具体范围：C/common/history/global/ce_global.txt只删重复PNI六日排程；同路径garibaldi_events只动.1/.2/.3（终身身份、迁移重验与将军闭包）；同路径italian_unification只动.4的既有共和国识别、.7/.8同一真实分离对象/DP、.10删除SAR/SIC固定偏置；两原生按钮使用同一候选helper；je_risorgimento仅窄REPLACE保留原生机制并默认钉选，实际文本按LOM共和国起点更新。没有复制/替换整个00_code_on_actions、没有删除formation、没有改法国国内链或日本。

无关native AST采用保序span编辑保留，独立测试仍须比对实际冻结与GAME；本报告没有用“构造上保留”代替测试PASS。

## 文案与C1两键

不可变作者样本7条，逐键对读471个C2最终中英键；完整原句/路径/行号/SHA、最后文本及编辑结论在batch-c2-writing-comparison.md/json。双语覆盖事件、JE、按钮、人物名、修正、状态与兼容文本。全量对读是编辑判断，格式、最终加载覆盖与动态scope仍待独立测试。

C1只增加实际Tiger缺失的`nesnd_egypt_protection_negotiations`及`nesnd_egypt_protection_negotiations_reason`两键，每种语言各两条；准确键不是短名nesnd_egypt_negotiations。单独差分batch-c2-c1-retired-localization.diff；C1玩法与共享nesnd_canon_*均未编辑。

## 下一阶段边界

只测试最终owned冻结及其固定依赖；不要测试正在变化的全C。共享外交三项C2所需稳定依赖来自C1 repair4冻结，B2正在扩展的kind5/6/7/8/9文件不宣称已冻结或通过。本批不改kind3经济政治信用的语义。

最低独立用例仍按批准计划§12，重点加：两种形成/旧档恢复顺序、默认钉选/两个施工槽、连续三月中断、目标失地/分州和提供者stamp、周报价/费用期/重复点击、政治49/50/51与离阁、双边90日取消/同nonce/同伙伴新nonce/替代一次/失州/主动退出/十二月再议、18人各自窗口/外方/流亡/void/dead/retired/空槽/女性法律、独立西府同一个段与资格通知、原生完整未改AST。

尚未由本轮证明：原生人物role/女agitator动态can_agitate、void枚举和自然退休时序；当帧事件投递/取消与scope临时值；原生DP对象后帧存续和参与资格；UI预览、真实月度/财政缓存、AI与存读档。没有任何ENGINE_PASS或STATIC_PASS声明。所有数值是已批准尺度和实现的原生修正，最终正确性由root及后续外部边界测试裁定。

技能维护复核：没有新版本/永久接口规则需写入技能；未修改技能。工具、补丁历史、备份与证据都留在WORK，主MOD只读。
