# 意大利侦查与分阶段开发方案

2026-11-03。范围：只读研究、方案；主 MOD、原版、参考 MOD、原稿、存档均未修改，未启动游戏。本研究分支的新增产物为本文。已读项目 AGENTS、工程适配、领域入口、执行索引、NESND 目录/设定/系统设计路由及 Matt Pocock research 技能。`catalog.py status`：GAME **1.13.11 / build 24799966，CURRENT，changed_count=0**。下文明确区分 `current_script`、原稿记载、既有存档观察和 `gameplay_proposal`；所有新角色、分支和开发文件均属提案。本文是内部规划，标题不作为玩家本地化发布，后续落库另走作者原文取样与玩家文本审查。

## 设计环境

2026-11-03用户补充：通常不考虑DLC缺失。方案默认当前完整DLC环境，不建立缺DLC的替代人物、简化公司或旁路剧情，也不将缺DLC用例列为交付阻断。资料表中的DLC条件仍保留为源码事实；这不授权批量删除原生has_dlc条件，亦不豁免当前环境的引用、触发和退出检查。

## 一、结论：主体应是既存的北方共和国及法国体系

**NESND 的意大利已有共和国，统一问题首先是法国保护体系内的自主权、附属邦整合和南北政治妥协。** PPET slide 23 §11明确：1802年法国支持建立意大利共和国；§13的1804年叙事已有“意大利执政”。这与现实1815后由撒丁王国收复奥属伦巴第的起点不同。原稿未给本轮所需的完整统一宪制、经济路线或统一日期；“统一进程不可避免”可作为时代意识，不应转成所有局1861年必然吞并。[P]

当前 LOM：总统共和、财富投票、民选官僚、干预主义、重商主义、信仰自由、宗教学校、集会权、国民民兵、自耕农所有制；军队和知识分子在政府。它控制伦巴第、皮埃蒙特、威尼西亚、罗马涅，受法国保护，又支配帕尔马、摩德纳和托斯卡纳。此处“共和国”已经存在，真正未完成的是其自主权、公民范围和半岛秩序。[M1][M2][M3][G1]

**名称需要单列核对。** 作者定义的 `ce_north_italy` 是“北意大利共和国”，但当前动态名还要求完整拥有南蒂罗尔；该州开局属于奥地利。不能把该动态名当作1836已显示的事实，也不应为了显示名字直接夺走南蒂罗尔。建议将“共和国称号”和“阿尔卑斯边界要求”解耦，是否改名属于独立小项。[M4][M1]

## 二、1836有效脚本基线

`.bak`不计有效定义。意大利国家数据库沿用 GAME 的 `00_countries.txt`；MOD的 `LOM.txt`新增国家/人物历史，其他国家仍读取原版对应历史文件。人口是 `create_pop.size`合计，不是本轮新局运行后人口；建筑级数由保序解析重复 `create_building` 和所有权等级求和，未推断实际就业、利润或财政。[M1][M2][M5][M6][G2][G3]

|主体|1836地图/宗属|人口与政治基础|路线意义|
|---|---|---|---|
|LOM|伦巴第、皮埃蒙特、威尼西亚、罗马涅；FRA protectorate；PAR/MOD/TUS为其puppet|约750.22万人；主文化north_italian；首都定义伦巴第，tier仍principality；共和国。自定义统治者Guglielmo Pepe，53岁、北意大利文化、军队IG、沙文主义领袖、将军；另创建马志尼|自然的北方统一倡议者，但法国不会自动放弃宗主权；低tier和称号条件需要与设计核对，不能仅据版图认为它已经是ITA|
|SAR|仅撒丁岛；FRA protectorate；皮埃蒙特已属LOM，萨伏伊及普罗旺斯属FRA|约52.41万人；原版主文化north_italian、岛上人口south_italian，国家首都定义仍STATE_PIEDMONT；君主制/专制、国家至上，卡洛·阿尔贝托|岛屿王朝与矿业/海运路线；复国或王朝统一可作为条件性竞争线，不能默认领跑。首都与主文化/人口差异应先核新局实际行为与作者意图|
|PAP|拉齐奥、翁布里亚；无本轮查见的宗属pact；法国大陆体系成员|约179.05万人；神权、寡头政治、国教、传统主义、土地税、宗教学校与慈善医院；原版格里高利模板|教会与城市财权、学校和罗马地位；可以谈判、维持独立，也可参与天主教邦联|
|SIC|坎帕尼亚、阿布鲁佐、卡拉布里亚、普利亚、西西里；无本轮查见的宗属pact|约703.27万人；south_italian；原版反动政治起点，传统主义、土地税、大庄园制，费迪南多模板；有奥地利独立保证与双向贸易条款|规模接近北方，具有独立现代化和竞争统一基础，不能只是等待北方吞并的落后尾声|
|PAR/MOD/TUS|分别占艾米利亚一部、一部及托斯卡纳；LOM傀儡|约47.20/64.84/163.24万人；沿用君主与反动政治基线。统治者模板为玛丽亚·路易莎、弗朗切斯科四世、利奥波德|附属君主与共和宗主之间的宪制矛盾；地方法院、税收、债务、学校与军队条款决定整合|
|LUC|艾米利亚另一部分；未在当前有效宗属历史中找到其附属pact|约10.84万人；原版卡洛·卢多维科君主、反动政治|商业小国和地方自治谈判；不能因同州就随PAR/MOD自动吞并|
|AUS/FRA边区|南蒂罗尔、伊斯特里亚为AUS；萨伏伊、普罗旺斯、科西嘉为FRA|伊斯特里亚现有人口含斯洛文尼亚、克罗地亚、北意大利、南德意志和匈牙利文化；不能称单一民族空地|边界和文化权利是后续外交问题，不是形成ITA必须清空的地图障碍|

表中依据：[M1]州归属；[M3]宗属；[M7]法国大陆体系；[M8]奥西条约；[M5]人口；[M2][G1][G2][G3]法律、国家定义与人物。当前法国集团在历史中同时列入AUS和PAP，故“法国援意大利反奥”也是重订既有秩序的抉择，不是无成本默认盟约。[M7]

LOM没有独立人口财富/识字历史文件，原版人口模板与其当前替代定位应在实现前核查；本轮不据文件缺失宣称运行异常。LOM创建马志尼，而原版SAR在相应DLC下也创建并放逐马志尼，是需要定向核对的角色唯一性问题；没有本轮新局双人证据，不列为已确认BUG。[M2][G3]

### 地区经济：先利用已存在的差异

|地区|当前历史资产（例）|可发展的玩法方向（提案）|
|---|---|---|
|伦巴第|纺织5、枪械5、火炮2、建设3、行政3|军工订单与民用转产；共和国军队、工厂主与纳税人的争论|
|皮埃蒙特|工具2、船厂2、纺织2、大学1、纸1、食品1、建设1、行政5；煤28/铁45资源容量|开煤铁、工具—钢—机械—铁路，港口连接法国市场；原料可进口，不强制全自给|
|威尼西亚|纺织8、丝5、玻璃5、纸5、港口2；煤44容量|纺织/玻璃与印刷贸易，熟练工、女性纺织劳工、城市商人与乡村蚕农的分配问题|
|罗马涅/艾米利亚|前者纺织1、麦5、牧2；后者多国分割、农业为主，MOD大学1、LUC纺织/贸易/港口各1|连接共和中心与附属邦，粮食、教育和跨境通道；需要实际协定，不以“共享国家认同”替代宗属法权|
|托斯卡纳|铁4、丝2、纺织2、玻璃1、大学1、港口2；铁60/硫40容量|矿山—工具—港口与学院；地方财产权和债务安排使和平加盟有实际内容|
|撒丁岛|铁3、木5、船厂1、港口1；煤20/铁21/硫20容量|矿业和海运，外部资本换工程与自主权；保留可经营的岛屿国家路线|
|坎帕尼亚/南方大陆|坎帕尼亚工具3、枪2、纺织3、丝2、麦10、港口3、建设2；卡拉布里亚铁2及煤16/铁24容量|那不勒斯的行政、军工、食品与南方矿业；土地制度、财政和就业决定现代化速度|
|西西里|硫5、麦5、港口2，硫资源容量100|硫矿—肥料/炸药—港口，承包商、土地所有者与矿工利益冲突；保留进口设备和外资路线|
|教宗国|拉齐奥行政4、纸2、港口1、梵蒂冈1，翁布里亚农业/林渔|教育、出版、行政和农业改善，教会财政与世俗市政的权限交换|

资产依据[M6]；资源容量依据[G4]。本轮地图资源定义沿用原版南欧文件，不能用现实“意大利无煤”删掉游戏已有煤矿容量。容量不等于已经开采；LOM的初始工业并不等于已经有与之匹配的煤铁/运输。北方工业、南方农业各自内部都不单一，不能给全部北方州同一工厂包或把南方仅当粮库。

## 三、1866既有观察者局：目前的内容缺口

读取既有最终存档1866.1.15，以此前 `fra_hus_extract.py`的序列化section/record切片方法筛选意大利TAG，未构建213MB整档AST、未再开局。原档SHA256为`84aeb299f56656c3c9ce2373299ef5ba98a78a3bf01bdc9a1b39f38c49ee67e4`。[SAVE]

- **没有存活主TAG ITA**。存活LOM约1269.98万人，拥有北方四州及艾米利亚的一部分；PAR/MOD不在筛选出的存活主TAG中。只据终档，不能反推吞并发生日或全部原因。
- LOM的`je_risorgimento`确为`active=yes`，加入日1844.4.19；变量是`risorgimento_anti_unifying_stance`。其统治者为Luca Guglianetti，出生1829.10.27，liberal领袖意识形态。这是本局生成角色记录，不把他冒认成作者新增正史人物。
- SAR约171.06万、SIC约831.60万、PAP约229.62万、TUS约286.02万、LUC约11.91万。各自原生复兴JE活跃；SAR/TUS为赞成统一立场，LOM/SIC/PAP/LUC反对统一。
- 当前pact记录表明LOM/SAR/TUS均为FRA的`puppet`；这只是1866状态，不把存档pact保留的开始日期误当每次降自治的发生日期。
- LOM已建工具28、纺织17、钢9、铁路2；相应staffing约27.14、16.57、5.94、2，为已招募等级当量，不是工人数。这说明共和国可发生工业增长，同时统一仍停留在原生JE；单局不能证明新方案平衡，也不能将“未统一”本身定为BUG。

**规划含义：**法国依附、政府反统一、增长中的工商业与民族运动应能构成完整可玩路线。不能为修补叙事空白把本局强制改成统一，也不能用统一进度条覆盖其实际外交约束。

## 四、原版完整链与适配点

|链条环节|本机1.13.11实际源码|NESND适配判断|
|---|---|---|
|国家与形成数据库|ITA有north/south_italian两主文化；重大形成、文化本土州70%门槛、最多3候选；候选排名至少minor，意大利区域所有国家研究民族主义；AUS/KUK/HRE排除。[G2][G5]|不预设SAR。LOM/SIC等按现实规模、外交地位及支持竞逐；数据库候选资格与引擎宗属限制分别核，不宣称保护国无条件可形成|
|复兴JE入口|意大利主文化、意大利区域、民族主义、非帝国/霸权；开局事件`.10`选择赞成或反对统一；周触发`.4`，月随机`.2`。[G6]|保留基本入口与统一立场。新增经济内容可在民族主义之前进入；自主权谈判不是为了激活不存在的民族文化|
|统一立场/AI|`.10`赞成基础40，SAR+50，SIC−35；反对会受神权/传统主义/地主加权，SAR有减权。[G7:796]|当前明显继承现实TAG倾向，1866反统一LOM不自动是错误。以后只做本项目有依据的权重适配，让执政联盟、法国关系与实力参与，不换成LOM永远统一|
|和平兼并|`.2`要求唯一候选、邻接、友好、目标minor及以下、目标AI、赞成统一且无拒绝冷却；目标独立、为本国属国或同关税同盟；执行`annex_with_incorporation`。[G7:57]|不另造绕开外交的一键吞并。PAR/MOD/TUS须真实归属与协定，LUC/教宗国/两西西里不能被当作免费附件|
|激进派与人物|`.4`要求首都激进比例至少10%、意大利民族运动内战等真实条件，可能政变或被其他统一国吸收；民族运动由当前文化热情与政治条件产生。[G7:186][G8]|保留失败与革命，不让虚构人物凭姓名强制改政体；角色可表达利益，运动与实际法律承担政治结果|
|鼓动民族主义按钮|外国持有意大利本土州、关系等条件，按钮显示要求非属国；名称虽然带austrian，筛选并非只AUS。[G9:450]|法国持有科西嘉/萨伏伊等且保护意大利，也可能成为民族主义对象；不得照抄“所有问题都在奥地利”|
|战争与结算|`dp_unify_italy`使用`unification`战目标且需民族主义；战目标kind有引擎预置执行，`on_enforced`为空。`on_country_formed`对ITA触发`.1`，后者给意大利旧地理区声明及修正。[G10][G11][G12][G7:1][G13]|扩展应观察原生建国结果再接整合，避免第二套自动吞并或双重奖励；边界声明与实际承认/占领分开|
|资源/显示|JE调用waving_flag图标，事件引用`votp_garibaldi`视频，本地化在`content_1_l_simp_chinese.yml`；公司图标/声望商品另在对应数据库。[G6][G7][G14][G15]|按本机完整DLC环境设计并复用已核资源；不搬参考MOD素材。原版视频的历史人物意象也需与共和国叙事区分|

当前MOD没有查见专属意大利JE/事件体系；已有是开局历史、动态国名、全局成就标记和继承的原版统一机制。`CE_major_formables.txt`只覆盖中国，不能认为它已经改过ITA的70%门槛。原生链可以保留为统一底座，新增内容应填经济、宪制、宗主权和统一后果。[M9]

## 五、两个参考MOD具体取用与排除

**RAHF：借部门建设与政治回报，不借历史结果强送。** 通用工业总JE由民族国家技术组合开启，事件`dsk_common.1`一次加入多个子JE；重工业子项允许市场产量或集中/分散工厂达到就业条件，完成后触发汇总事件并给5年衰减修正。这可改成意大利各地区“建成并经营起来”的组合目标，并给小国缩放条件；不能照搬15级钢厂、电力或殖民主义为1836前置。[R1][R2]

RAHF的意大利专用`sar_become_ita_now`在1861–62窗口、指定游戏规则下替AI撒丁升高关系、吞并诸邦，并处理向法国让地；`plom1/2`围绕1859–60萨奥战争和伦巴第转移安排。NESND的伦巴第/威尼西亚已属LOM，萨伏伊/普罗旺斯已属FRA，SAR本身又受保护，直接复制会毁掉真实起点。借用“外交承诺—参战—战后议价”的结构，日期和归属都改为真实条件，且允许拒绝或败战。[R3]

**MUC：借公司主营/扩展/地理门槛，并把公司政治化。**

|参考公司|实际结构|本项目候选用途|
|---|---|---|
|Ansaldo、Ilva|皮埃蒙特的军工/工具/钢，扩展电力或煤；前者铁路技术、某相应建筑5级，后者弧焊和钢5级。[U1:4][U1:83] 原版已提供同形链。[G15]|共和国军工承包、军民技术与钢铁后续；不把晚期钢铁企业1836免费赠送|
|Mantero Seta|伦巴第丝/纺织，扩展棉，5级建筑门槛与Como丝商品；相关DLC条件。[U1:480]|伦巴第/威尼西亚蚕丝—纺织、贸易与劳动关系；总部按实际经营中心核，不因名称就给土地|
|英西西里硫公司|西西里硫矿主营、港口扩展，整合州硫5级，不能对英战争，DLC条件；繁荣修正涉及军需、农业。[U1:401]|矿权、外资和南方财政可用结构；英国并非本世界必然投资者。法国、国内或其他资本应按实际条约/资金进入|
|意大利银行|ITA/由ITA形成、banks_enabled，拉齐奥金融区15、投资银行科技、无另一银行；主营纸/金/枪，扩展火炮/汽车/钢/煤。[U1:1747]|统一后财政与信贷争论；这不是独立银行建筑或完整货币模拟。不能把全国金融安排硬绑罗马或给一串免费修正|

原版公司本就有主营/扩展、声望商品、科技与成立门槛、AI建设目标。优先发展已存在公司机制，新增虚构公司最多先做一两个承担确实不同利益的组织；新名称与创业史应由NESND决定。参考源码的存在不认证其运行兼容，不建议把两个大MOD叠加载入，不搬图片/商标/地图，也不复制拆建工厂式公司兼并。[G15][U1]

## 六、分阶段路线（全部为玩法提案）

### 阶段A：既存国家先能兑现自己的承诺

默认1836—1845观察窗，而非硬日期。北方共和国的议题是军需、城市工作、商业资本和附属邦税款；两西西里是农业产权、矿权、军队和港口；教宗国是学校、市政与教会财政；撒丁是矿业、港口及王朝生存。每国保留一个总议程，最多两项当前可操作项目，不开局铺满后期日志。

共和国可选公共建设与军工转产、商人融资与贸易扩张、地方合资与附属邦议价。玩家以真实建设、就业、财政承受和物流改善推进；获得国家能力，也面临征税、工人组织、债务和法国对特许权的要求。行政与学校投入提供后期资格，不用一个科技完成按钮直接宣告全社会现代化。[M2][M6][R1]

### 阶段B：法国保护关系、附属邦关系与统一领导权

科技、国内民族运动、财政/军事实力和真实外交地位达到相应条件后推进。统一是政治选择，不是惟一成功结局。

1. **法国体系内协商整合。** LOM争取更高自治，以继续对法协作、有限军事义务或投资保护换取合并自己附属邦的许可。邦国谈地方税收、法院、军队、学校与债务；法国可支持足以稳定半岛的伙伴，也可保护PAP及平衡SIC。正式归属依原生条约/附属/统一系统；“联邦”如果只以若干修正和政治承诺近似表现，必须明确这种机制边界，不能声称引擎已有联邦议会。失败可留下松散合作与继续改革的共和国。
2. **自主的共和统一。** 民族主义者挑战法国宗主权，先通过外交或战争取得现实行动空间，再争取诸邦支持。可以同法国谈判友好独立，也可在法国内乱/对外受挫时联合他国；不要求法国一定革命。扩大公民资格、承担战争税和债务、处理保守教会与地主反对，使共和国不是只改国名。失败可能停战、降自治、分裂或亡国，不强制保人。
3. **南方主导的君主统一。** SIC以现有大人口、军需、矿业和港口改革形成竞争力，争取中部保守王公、教会与一部分商人。它可走有代表权的君主妥协，也可中央集权；北方资本和共和团体有具体反对条件。奥地利保证能增加谈判筹码，但奥地利也处于法国体系，支援须考虑关系和自身危机。SAR保留更难的复国/王朝路线，实际取得大陆支持后才竞争，不享标签加成保证成功。
4. **教宗主持的邦联或长期多国秩序。** PAP可主张共同防御和贸易，同时保留成员政权；它需要世俗行政和财政让步，不能仅以宗教相同取得统治。LOM、SIC可参与或拒绝；自由城市和小国有存续出口。若维持多国，仍能完成跨境交通、工业、教育和贸易目标，不把未形成ITA等同失败。

原生`.10`统一/反统一立场应统一管理，避免本项目界面选择共和统一而原生变量仍在反对。AI倾向按执政联盟、政体、自治、真实领土/国力和关系权重，而非1859/1861自动送地；不把法属意大利每个国家每月强制改成统一派。[G7][G9][R3]

### 阶段C：统一之后才出现的国家建设

形成ITA或达到明确区域整合终态后，继承原有工程和财产，开放三组议题：

- **统一财政与军队。** 合并后真实新领土的债务负担、税制与军制差异才纳入处理；中央接债换行政整合、地方留税换自治、限期过渡各有代价。现有存档无法安全逐项转移历史债务时，先以明确预算支出与政治承诺近似，不编造货币/海关API或重复扣旧债。
- **南北投资与公民资格。** 北方工具、丝织、玻璃与南方硫、食品、港口形成互补，同时防止工业与税款只流向一处。土地改革、教育、征兵和基础设施有地区受益者/失利者；南方拥有自己的工业城市，不能“一次同化”解决。意大利两主文化之外的法语、科西嘉、南德意志、斯洛文尼亚、克罗地亚和犹太群体按实际领土与法律进入议题。
- **罗马与阿尔卑斯边界。** 罗马可以是谈判结果、宗教特别安排、既有首都保持或战争后果；不把迁都列为所有公司的成立条件。南蒂罗尔/伊斯特里亚可选择承认边界、贸易与文化权利协议、诉诸领土要求。统一后的外交不必自动变成征服殖民地，也不按1919原稿未来线强制分裂。

三种政治后继可以并存竞争：商业/议会共和国、强行政的共和或君主国家、扩大劳动权利与地方参与的社会改革。它们应由现实法律与运动决定，不设置一键“开启民主/社会主义”按钮。原稿20世纪极端民族主义与1919东部领土公投只是后世世界线资料，不在1836强制生成墨索里尼或预写结局。[P:142][P:412]

## 七、三名虚构人物候选

以下姓名为本轮新创作，检索当前人物、事件和本地化未见同名；不声称穷尽作者所有手稿，不移植现实同名者经历，也不替换Pepe、马志尼等既有人物。人物死亡/流亡/失势时由组织或合格继任者承接议程，不能复活或永久锁死路线。

|人物|1836身份、筹码|冲突与可变立场|
|---|---|---|
|乔万尼·瓦尔迪耶里 Giovanni Valdieri，1798生，38岁，北意大利文化|皮埃蒙特工程承包人与军需商的合伙人，熟悉共和国军工和法国资本；工业家候选|愿用法国融资换铁路与工具厂，同时要求预算和产权稳定；支持协商统一，军方无限征用或法国过度干预会使他倒向自主派。若工人要求全面没收，其改革联盟会分裂|
|特蕾莎·贝兰迪 Teresa Bellandi，1807生，29岁，北意大利文化|罗马涅印刷家庭出身的编辑、女校筹办人；经报馆、工匠互助组织和教师联系动员|主张共和国兑现公民与教育承诺，反对只让有产男性分享“统一”；可先为知识分子支持的公共人物，后期实际工业与结社环境足够时联结工人。不能在法律未准入时直接塞进国家统治职位；镇压、流亡或温和改革都有后继|
|马泰奥·鲁夏尼 Matteo Rusciani，1794生，42岁，南意大利文化|那不勒斯律师，代理小地主、租户与硫矿承包纠纷，能协调港口商人和地方议事者|支持南方国家现代化、有限土地改革与有条件君主宪制，反对北方无条件接管税款；若SIC压制改革，可转而支持带地方保障的共和统一。不会因南方出身天然反工业或排外|

这些角色承担工程融资、公民资格、土地与区域保障三类利益。可以拥有矛盾与妥协，不为每条路线另造一位无所不能的领袖；对白和本地化在获实施范围后另做作者语体对读。

## 八、最小实施边界与生命周期

建议先做三个闭环再决定后期规模，勿一次改完整意大利史：

1. **A：基线与经济。** 定向核LOM名称/tier、SAR首都/文化、马志尼唯一性；保留作者版图。新增一个区域发展总JE、最多两项经济子JE、少量利益冲突事件。国家定义/地图改动仅在确认具体不一致后单列，不混进风味扩展。
2. **B：自主与协商。** 共用一个状态机管理阶段、倡议国、当前合作对象和一次性结算；只处理存在且实际有关系的国家。法国现有王朝/共和路线决定其授权意愿；共享已有法国外交状态，不再造第二套法国内政。对LOM—FRA及LOM—PAR/MOD/TUS两层关系分别议价。
3. **C：统一后整合。** 观察原生ITA形成/国家继承再接后续；不拆建工厂，不清外国产权，不免费授予全部主张州。不要求所有未来系统在第一批交付。

**拟文件闭包：**`common/journal_entries/nesnd_italy.txt`（议程/阶段）、`events/nesnd_italy.txt`（协商/利益冲突）、`common/scripted_triggers/nesnd_italy.txt`与`common/scripted_effects/nesnd_italy.txt`（资格/单一幂等结算）、需要时`common/scripted_buttons/nesnd_italy.txt`、`common/static_modifiers/nesnd_italy.txt`、`common/character_templates/nesnd_italy.txt`、中英replace本地化各一份。公司仅在确有独特用途时增加`common/company_types/nesnd_italy.txt`。优先原生进度条，不用叙事塞循环增减细节。

原生意大利事件/按钮若需要更改，应先查当前数据库支持的窄覆盖方式再操作；不能假定所有数据库都支持同一`REPLACE`/`INJECT`。`on_country_formed`依赖用窄范围扩展，禁止复制整个原版on_actions。尽量保留原生统一战目标、和平兼并及现有声明机制，不另写平行战争系统。

|边界|必须实现的收尾|
|---|---|
|LOM变ITA或别国统一|按国家连续性转入整合阶段；国家失去或取得主体身份时重新判定，不能单靠硬编码c:LOM永久拥有内容；奖励只领一次|
|附属邦已吞并/独立/转宗主|读取现关系与领土；旧邀约失效并清理，无效scope不继续扣款或吞并；不夺第三方州|
|法国改政体、战败或与意大利交战|重新议价援助/承诺；原帝王专属保证失效，商业资产继续按真实产权存在；不自动所有条约清零|
|战争、占领、失州、失去共同市场|依目标性质暂停或结算失败；已建产业保留。进口变贵可构成合理压力，不自动全资源补给|
|破产/项目失败|停止未来补助和未兑现承诺，允许缩规模、换融资或转路线；不永久锁死国家发展|
|人物死亡/被放逐|以同利益组织或通用角色接议程，不越权复活；按当前完整DLC环境核角色入口及唯一性|
|旧档加入内容|检查已有国家、法律、工业、原生JE立场和已形成ITA；不重新发开局礼物、不复建亡国、不强行重置外交|
|事件预览与延迟回复|触发时和选项执行时都验证国家/角色/州与关系；预览不写持久变量；同一个结算effect跨入口幂等|

**验证计划（尚未执行）：**离线解析与引用/资源/作用域闭包、动态名与地图条件对照；然后仅对未证语义集中做LOM新局、SIC竞争、PAP拒绝、法国改政体、目标国消亡、LOM形成ITA、旧1866档接入及存读档场景。经济验收看真实就业/投入/预算/物流与可恢复选择，失败允许破产、失国和长期分裂；不以STATIC_PASS写ENGINE_PASS，不为同一已证行为重复开局。

## 九、来源与指纹

以下均为原始文件；行号用于定位主要入口。`[G7:796]`等表示该文件具体行号，文件哈希锁定本次阅读版本。原稿PPT已重新核SHA与缓存一致：`b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`，事实回到slide/paragraph，不把既有报告摘要当正史。

- **[P]** [原稿PPT提取（slide 23 §11）；原件见下列PPT链接](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:326>)
- **[M1]** [各州归属：另见1965、1981、1989、1997、8350、8466、8476、8534、8809、8817、8916、8934行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:200>)
- **[M2]** [LOM国家历史；人物见同目录上级characters/LOM.txt及character_templates/zz_ce_italian.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/LOM.txt:1>)
- **[M3]** [法国与北意大利两层宗属](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:185>)
- **[M4]** [SAR、LOM动态名；中文名见localization/simp_chinese/replace/ce_countries_l_simp_chinese.yml:8、25](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/ce_dynamic_country_names.txt:815>)
- **[M5]** [各地区人口群体，南蒂罗尔另见00_west_europe.txt:1292](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/pops/01_south_europe.txt:1>)
- **[M6]** [建筑与所有权，重点2、120、327、557、1196、1386、1461、1567、1731行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/buildings/01_south_europe.txt:1>)
- **[M7]** [法国大陆体系](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/power_blocs/ce_power_blocs.txt:46>)
- **[M8]** [奥地利保证两西西里与贸易条款](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/treaties/00_historical_treaties.txt:403>)
- **[M9]** [MOD重大形成仅中国覆盖；JE/events检索未见专属意大利链](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_formation/CE_major_formables.txt:1>)
- **[G1]** [自由/保守/反动政治模板，须按国家后续激活法律覆盖](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_political_setup.txt:3>)
- **[G2]** [ITA定义；LOM等在665—778行](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:213>)
- **[G3]** [各国原版history/countries、characters与population对应文件；SAR马志尼调用见characters/sar - sardinia-piedmont.txt:60](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/sic - two sicilies.txt:1>)
- **[G4]** [南欧地区与资源容量](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/map_data/state_regions/01_south_europe.txt:1>)
- **[G5]** [ITA形成候选与70%文化本土州门槛](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_formation/00_major_formables.txt:54>)
- **[G6]** [原生复兴JE](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_italian_unification.txt:1>)
- **[G7]** [建国、和平兼并、激进派与统一立场事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt:1>)
- **[G8]** [意大利民族运动](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/03_pan_national_movements.txt:931>)
- **[G9]** [复兴运动按钮，另600行国内鼓动](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_scripted_buttons.txt:450>)
- **[G10]** [统一外交博弈，领导权博弈1289行](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:1001>)
- **[G11]** [原生统一战目标kind及执行设置](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/27_unification.txt:1>)
- **[G12]** [on_country_formed，4059行ITA事件调用](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:3887>)
- **[G13]** [统一后的声明范围](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_unification_effects.txt:1>)
- **[G14]** [原生JE/事件/按钮文本](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/content_1_l_simp_chinese.yml:1079>)
- **[G15]** [原生意大利公司完整定义；声望商品在common/prestige_goods/00_prestige_goods.txt:291、318](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/company_types/00_companies_italy.txt:1>)
- **[R1]** [总JE及793行重工业子项](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_tongyong_industrial_revolution.txt:2>)
- **[R2]** [总入口添加子JE与完成汇总事件](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/dsk_common.txt:2>)
- **[R3]** [固定年份SAR统一链、838/1001行萨奥战争链](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/historical_sar_become_italia.txt:1>)
- **[U1]** [意大利公司范式；401/480/1747行硫、丝、银行](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_Italy.txt:1>)
- **[SAVE]** [既有终档；读取方法见reports/observer-finish-20261103/fra_hus_extract.py](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/runtime/profiles/20261103T100813Z/save games/观察者_1866_01_15.v3>)

[G3]对应国家与人物原文逐文件入口：[countries/sar - sardinia.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/sar - sardinia.txt:1>)；[countries/pap - papal states.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/pap - papal states.txt:1>)；[countries/sic - two sicilies.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/sic - two sicilies.txt:1>)；[countries/par - parma.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/par - parma.txt:1>)；[countries/mod - modena.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/mod - modena.txt:1>)；[countries/tus - tuscany.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/tus - tuscany.txt:1>)；[countries/luc - lucca.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/luc - lucca.txt:1>)；[characters/sar - sardinia-piedmont.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/sar - sardinia-piedmont.txt:1>)；[characters/pap - papacy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/pap - papacy.txt:1>)；[characters/sic - two sicilies.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/sic - two sicilies.txt:1>)；[characters/par - parma.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/par - parma.txt:1>)；[characters/mod - modena.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/mod - modena.txt:1>)；[characters/tus - tuscany.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/tus - tuscany.txt:1>)；[characters/luc - lucca.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/luc - lucca.txt:1>)。LOM人物原文：[历史调用](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/characters/LOM.txt:1>)、[Pepe模板](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_ce_italian.txt:3>)。

[P] [PPT原件](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx>)。

### 关键源SHA256

|源|SHA256|
|---|---|
|P|`227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`|
|M1|`a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`|
|M2|`f4ede35d5c0804cd4351eff9e99022839faa2daebb5530947aeef6deccdf5ad2`|
|M3|`78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7`|
|M4|`19fe37f408bd08f9ef24a850aed99270b3febf481de369120ca2c2872cc2518c`|
|M5|`723de5419df52f62762c038382edfc5f73cd2477f3dabe2bb0b95d8a41e4301c`|
|M6|`bffdaf03188a26e3bc786be4a7438b3cf79f6cac54ffbe9f57c8af19d23d582f`|
|M7|`daa0797c9726047dd3c2b116766ebc6618677902d605e8704bb65665ca671ccd`|
|M8|`fbb2d10c7e3840b50c2dab4fc2510a68439bcc6fdfcec98e0c6e7ab4d0d1d352`|
|G5|`df6c873820cd73267ee50becc31b9f8d9fbe754074198b021e5b767c6f914580`|
|G6|`9515ee785f32b69dd06883136c40d4e39f17376049685d29f992abd536238a52`|
|G7|`3564046713083efe19a97fe04a3d83a6e875a627794652ce726c727c602b296e`|
|R3|`65fc9d86f304d3f266e3dd1f2cb9cb0d20c4f63b053b100f64a9d38a2433decd`|
|U1|`62ac007b878e3bc4ee624b83456f92d371d2315af2e5d080db246b2df1125fa7`|

本报告未给任何新内容标记ENGINE_PASS；既有终档仅证明该局在所列时间的保存状态。下一步是作者取舍具体路线与实施范围后，按选定闭环补机制来源、数值量纲、AI与退出条件；不需要先改地图或重写整套意大利统一。
