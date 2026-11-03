# 四国发展提案：参考MOD源码与法国、东洲专案

日期：2026-11-03。范围：只读研究和开发提案，未实施、未启动游戏、未认证参考MOD的运行行为。唯一产物为本报告；参考MOD、本机GAME、原稿与主MOD均未修改。

已按 NESND 与 Matt Pocock research 技能读取来源。catalog.py status 回报本机 **1.13.11 / build 24799966，CURRENT、changed_count=0**。这里只把可读源码列为机制证据；源码存在、静态通过、真正游戏内可达分别陈述。

## 1. 两个参考MOD实际是什么

|参考|本地事实|适合取用的层面|
|---|---|---|
|Realism Ai Historical Flavor Mod|WORKSHOP/2893069455，metadata 10.9、1.13.*。[R01](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/.metadata/metadata.json:2>)|国家建设总目标、部门日志、利润/就业条件、政治与建设相互影响、按实际国家与目标调整AI|
|More Unique Companies|WORKSHOP/3032185644；metadata中的version、supported_game_version为空，不能据此宣称适配1.13。[U01](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/.metadata/metadata.json:2>)|主营与扩展产业组合、地理/科技/建筑成立门槛、繁荣修正、公司资产与金融基础的成长日志|

这些是已安装源码的研究，不是建议同时加载两个大MOD，也不需要搬运其图片、商标、地图或整套脚本。MUC拥有许多现实公司名称；名称存在不意味着其创办年代、管理机构及效果适合NESND。下面建议只借结构，新名称和历史归属按本项目决定。

## 2. RAHF可借鉴的完整链与限制

|源码链|查到的事实|提案应怎样改写|
|---|---|---|
|法国总入口→子日志|`je_fra_empire`要求法国、君主制、波拿巴恢复标记或拿破仑三世实际在位；AI另要求1852.3.1之后。immediate调用`france_flavor.4`，该事件加入铁路、商业、学院、新巴黎、外交、法律、农业等子项。[R02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_fra.txt:324>) [R03](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/france_flavor.txt:133>)|NESND 1836已是连续存在的波拿巴帝国，不再等现实第二帝国成立；建设议程按当前政治分支进入，不复演1848–1852复辟。现有五条法国政治JE保留主导权。[M02](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_french_empire.txt:1>)|
|铁路/商业→巴黎总计数|法兰西岛铁路15级、就业>75%、盈利>0、道路法令；商业为当地食品/纺织/玻璃各15级并就业>75%、盈利>0。完成事件增加巴黎计数；铁路给永久州修正，商业给120个月修正。[R02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_fra.txt:324>) [R04](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/france_events.txt:2550>)|借“建成并经营起来”而非建筑数量打卡；法国交通目标应覆盖现实持有的工业与港口地区，巴黎文化/消费目标另列，不要求全部产业堆巴黎。奖励期限和规模重新校准。|
|通用工业总JE→多部门目标|总JE需要殖民、铁路、拿破仑战术科技，目标12；事件实际一次加入许多子日志，并不是严格按industry_1→2→3逐个解锁。[R05](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_tongyong_industrial_revolution.txt:2>) [R06](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/dsk_common.txt:2>)|借总目标汇总成绩；NESND可按开局建设、成熟工业、后期资本三阶段逐步展开。并非所有国家都要把殖民主义当现代化前置。|
|航运/重工业经营验收|允许市场产量或本国有效工厂的替代条件；如蒸汽船600产量或5级船厂、75%就业、合格PM；重工业允许多个中型厂或单个大厂。完成给5年衰减修正。[R05](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_tongyong_industrial_revolution.txt:2>) [R07](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/dsk_usa_modifiers.txt:2664>)|允许集中/分散布局，市场合作与本国产业分别计分。共同市场中的总供给不能冒充本国生产，不能强迫四国都工业自给。|
|清国洋务分部门|识字、特定改革人物意识形态或失败修正开启，军工/铁路/商业/学校/公司分项，和CHI、JAP、汉文化及特定败战绑定。[R08](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_chi_QNG.txt:96>)|可借国家能力的组合，不把CNE/USM写成晚清，不强制鸦片战争或甲午战争前置；既有土改、明吴危机和宗属秩序决定其改革成本。|
|AI地域估值|默认AI策略注入以游戏规则、年份、主文化、科技、目标州与宗属关系筛选州价值；例如荷兰/印尼、爪哇统一、英属印度。[R09](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/ai_strategies/dsk_default_strategy.txt:4>)|借“硬条件先排除，再按利益加权”；不复制英法美按现实国界扩张的目标，也不靠改文化诱导AI。|

**不照抄的明确部分：**法国铁路/商业/学院JE在1870之后对AI以invalid分支触发同一成功事件，属于该MOD的AI保护；它不是AI实际完成产业的证据。NESND应给AI可行的建设目标和外交偏好，仍按真实成果结算。[R02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_fra.txt:324>)

另一个阅读陷阱：`france_flavor.txt:95`有旧“ORPHAN_EVENT”注释，但当前`dsk_je_fra.txt:373`确实调用`france_flavor.4`；不能只看注释认定入口失效。[R02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_fra.txt:324>) [R03](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/france_flavor.txt:133>)

## 3. MUC：公司成长可用机制

|例子|真实脚本条件/产业|适配价值与边界|
|---|---|---|
|Fraissinet航运|主营船厂/港口，扩展木材/纸；在普罗旺斯有3级港口或船厂；繁荣给迁移吸引与贸易优势；AI计划5级船厂。定义的preferred HQ却是法国低地，和成立州不同。[U02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_France.txt:583>)|可供法国地中海—印度航线参考；HQ、港口、经营范围在NESND重新保持一致。|
|江南制造局|官僚所有类别；枪械/工具/船厂，扩展弹药；苏州整合州3级工具厂；繁荣给陆军防御；AI目标5级工具厂。[U03](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_China.txt:1250>)|适合“工艺—军需—舰船”的纵向产业链。但不把实际洋务江南制造局直接当南明/吴朝的既有组织。|
|招商轮船|官僚类别；贸易中心/港口，扩展船厂/小麦/水稻；苏州3级港口与螺旋桨护卫舰技术；繁荣给供给舰施工、铸币与港口吞吐。[U03](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_China.txt:1250>)|可借官办与民办航运的分工；本项目已有福海行，优先围绕它的商权与实际资产，而非再造同功能招商局。|
|大北方铁路|铁路主营，扩展引擎/钢；可见/成立地区允许大西洋岸、大平原、太平洋岸；5级铁路、钢车厢、股份公司技术。AI仍只对明尼苏达设目标。[U04](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_USA.txt:4028>)|可供东洲内陆运输参考；玩家地理范围与AI目标必须对齐，不能把HUS引去一个不在其统治内的现实美国总部。|
|Levi / Dunsmuir|前者加州纺织与棉丝扩展、硫化科技；后者不列颠哥伦比亚煤矿与钢铁/铁路/港口扩展、水管锅炉和铁路科技。[U04](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_USA.txt:4028>) [U05](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_Canada.txt:2085>)|西岸劳作服饰、煤矿—铁路是行业范式；不把现实品牌和移民生平直接提前安给东洲。部分繁荣奖励还降低期望生活水平或改变歧视相关参数，不能按“公司收益”原样搬。|
|法国银行|需banks_enabled规则、15级金融区、全国没有另一家所列银行；主营纸/火炮/金，扩展钢/弹药/铁路/纺织；繁荣影响投资池贡献、私人建设份额、政府分红等并加公司槽。[U02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_France.txt:583>) [U10](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/scripted_triggers/00_unique_companies_scripted_triggers.txt:1>) [U11](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/game_rules/00_unique_companies_game_rules.txt:1>)|“银行连接资本与产业”可以借；这里不是独立银行建筑或真实股票市场模拟，也不是一组免费财政增益。银行规则、触发器、公司类别和奖励范围是完整依赖，不能只抄公司块。|
|US Steel整合日志|成熟钢企需繁荣、产声望品、持有至少50级；存在另一相关钢企；纽约50级金融区；摩根公司50级或全国500级金融区；电弧、共同基金、社团主义科技。随后累计繁荣月份达36再结算。[U07](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/journal_entries/more_unique_companies_journal_us_steel_corp.txt:1>) [U09](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/script_values/more_unique_companies_event_values.txt:5>)|可借“产业集中到一定规模后出现兼并/反垄断政治”；这是累计36个繁荣月，并非连续36月，计时不会因不繁荣自动归零。|

US Steel实际整合事件移除旧公司并添加新公司，还按钢厂等级逐项`remove_building/create_building`重建归属。源码不能证明这一做法保存工作岗位、PM、外国权益与全部等级的正确结果，NESND不采用这种拆建合并。需要另查当前引擎安全的所有权操作，并做范围明确的引擎试验。[U08](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/events/more_unique_companies_events_us_steel_corp.txt:3>)

### 本机原生机制对照

GAME的DMC已采用主营、扩展、声望品、科技/建筑成立门槛、繁荣修正、`ai_will_do`及`ai_construction_targets`，MUC并非全新公司系统。[G01](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/company_types/00_companies_france.txt:144>)

本机GAME声望衣物链：公司潜在可产且繁荣→锁定公司→每月繁荣并具前三产量时累计→36月后给该公司解锁标记→DMC的`prestige_goods_trigger`读标记，商品定义在prestige_goods数据库；公司消失/解散另有重绑定和补JE的效果。适合NESND公司成长框架，但不能拿“给公司buff”冒充新增生产行为。[G01](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/company_types/00_companies_france.txt:144>) [G02](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_prestige_goods.txt:1>) [G03](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_scripted_effects.txt:1156>) [G04](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/event_values.txt:243>) [G05](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/prestige_goods/00_prestige_goods.txt:510>)

这些是本机当前GAME文件的完整可查链；未在本轮重新做运行试验。新JE还需覆盖公司解散/国有化/总部转属、国家更名或继承、失去目标州、退出共同市场、战争和既有存档。

## 4. 四国公司与发展差异——明确为提案

|国家|已有锚点|建议发展链|政治代价与可选方向|
|---|---|---|---|
|FRA|干预主义、保护主义、公共学校；已有DMC、Cockerill。[M01](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/fra - france.txt:1>)|煤铁—钢铁—铁路与机械→港口与商船→消费品/玻璃/奢侈品、金融和技术输出。以现有公司成长为主，新航运公司为可选。|皇家保证金与私人融资各有代价；资本越集中，越要处理乡村、城市工人、议会预算权与皇帝恩庇网络；海外投资与印度援助共享财政和舰队约束。|
|CNE|已有远北粮农总行定义：牧场/水稻/食品，扩展硫/化工、官僚类别。这里只确认定义，不宣称开局已成立。[M05](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/company_types/ce_companies_china.txt:53>) [M06](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_companies_l_simp_chinese.yml:2>)|土地改革成果→余粮进入城市市场→食品、化肥、工具与交通→更有财力的工业和军需。|皇产/官产整理、农户产权和商人承办分工；不要另起一套洋务进度覆盖已经存在的土改/信心成本。|
|USM|已有福海行且开局加入：纺织/船厂/木材，扩展棉，跨域经营。[M05](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/company_types/ce_companies_china.txt:53>) [M06](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_companies_l_simp_chinese.yml:2>)；开局公司由父任务另核|商船与港口—纺织及原料—保险/金融式政策—区域投资；明吴结算后围绕实际帝国/朝贡网络重订商权与财政责任。|维持商帮协商、强化国家海军/官营军需、扩大地区议事权均可；共同市场自然供需，不重新引入库存/预付款/履约模块。|
|HUS|东青行已在开局加入；主营糖/木/工具/铁，扩展棉/船；拥有铁路、机械工具、中央银行、公司特许等科技。[M03](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:1>) [M05](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/company_types/ce_companies_china.txt:53>) [M06](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_companies_l_simp_chinese.yml:2>)|东青行的木—铁—工具→沿海航运和内陆铁路→食品/纺织与成熟资本市场→实际勘探和技术具备后发展石油。|殖垦土地与原住民条约、债务奴役与自由劳工、东青行集中与竞争性商号；繁荣可以推动共和改革，也能巩固士绅和公司寡头。|

所有量化门槛先取四国当前人口、州规模、资产和财政基线再定；本报告不把RAHF的15级三厂、MUC的50/500级金融目标当通用平衡值。殖民/投资须保留真实条约与市场权限，外国公司资产不因政治路线选择自动消失。

## 5. FRA专案：在已有政治树上增加经济与外交后继

2026-11-03更新：具体实施方向以[法国政治与地区方案](../france-politics-plan-20261103/france-development-plan.md)为准。常规政治任务是相关IG执政＋合法性50，不设党派组合门槛。原参考公司与人物资料保留。

事实锚：开局风味已写路易推动工业与报刊、同时把帝权置于人民主权之上；PPT的1848自由帝国、1850–66铁路、1862–72经济萧条是作者的一条未来线，不是每局必须按年发生。当前已存在波拿巴稳定、镇压共和、共和运动、奥尔良与波旁分支，不应再造平行王朝争夺系统。[M02](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_french_empire.txt:1>) [M08](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:2>) [C02](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:324>)

|阶段/方向（提案）|玩家实际要做什么|收益、代价和失败后继|
|---|---|---|
|开局共同议程：帝国的繁荣|接现有稳定JE，分别处理工业通道、公共教育、军需、城乡生活；选择政府保证与民间经营的比例，建设必须有就业和真实需求。|扩产、资格与税基改善；财政支出、城市激进化、传统乡村利益受损。停滞保留已建资产，给调整政策的后继。|
|自由帝国／议会妥协|允许君主仍在位，推进代表权、公开预算、法定劳动和社会保障的可选组合；经济建设成果换取谈判空间。|政治稳定与人才增长；皇帝、军官、教会、地主和资本家对不同改革分别反应。改革失败回到现有政治危机，不能只用一个“支持自由”按钮一键民主化。|
|奥尔良后继：宫廷与外省|取得政权后选择巴黎集中发展或外省城市成长，用巴黎都市份额显示倾向；金融、服务、工业与地方学校围绕选择展开。|巴黎人口基建或外省迁移吸引/施工效率；保留财政、就业、公司集中和劳动争议。铁路不再是统一的路线终点。|
|波旁后继：宫廷与外省|复用同一空间选择，按农村、教会、军人购田者及在位人物的利益发展不同政治反馈；既可经营外省也可强化巴黎。|公共工程、农业加工与教育；纳税、学校控制、地方特权和城市代表权仍有冲突。不把王朝名称固定为某个按钮。|
|共和繁荣与分配|现实共和制度成立后，延续资产并推动政治经济自由化；比较企业繁荣与民众生活，回应真实政治运动。|可走社会改革，也可形成军队与寡头的合作、压制社会主义运动乃至右转；不是预定结局，不复制俄罗斯人物和时间线。|
|外交共同后继：大陆秩序与海外承诺|印度、南明/吴、秦、东洲分别处理贸易、军援、实际投送与承诺；法国可在维护旧约、支持新伙伴、承认新政权之间取舍。|兑现援助消耗财政和舰队；违约与妥协影响威望和伙伴关系。PPT的法吴条约断裂及后来恢复可作条件式事件题材。|

**拟新增虚构角色，尚非正史：**

|人物|1836身份与利益|实际可承载事件|
|---|---|---|
|埃蒂安·瓦尔库尔（Étienne Valcour，1791年生）|勃艮第工程师转铁路承包人；工业家，拥护可预期的法制与帝国担保，但反对无限军事征用。|铁路特许、国家保证金、兼并报价、债务重组；能支持自由帝国或奥尔良实业政府，也可能在共和政府下继续经营。|
|吕西安·德洛姆（Lucien Delorme，1796年生）|巴黎律师兼地方报刊撰稿人；知识分子，支持扩大代表权和公开预算，对用“人民主权”掩饰皇帝特权持批判态度。|建设征地、报刊限制、工业劳动争端及议会妥协；可由温和反对派转共和激进派，取决于政府实际处置。|

人物不顶替路易、郭庆达式核心既有人物，也不预设部长空位。若未来实现，应通过人物/IG与事件范围表达职能；不编造引擎没有的“经济部长”任命机制。

## 6. HUS专案：商业共和国中的公民与疆土

事实锚：HUS四个主文化为ce_liaodong、ce_wuu、hakka、manchu，已受承认。现行总统共和/财产门槛选举、自由放任、重商、文化排斥、债务奴隶、审查、私人学校共同存在。郭庆达模板写士绅出身、远洋见闻、科名官僚履历、与亚洲共和派往来及扬州协定外交声望；他不是一个无历史关系的美国式总统替身。[M03](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:1>) [M04](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:38>) [M07](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_historical_leaders_ce_asia.txt:1092>)

PPT18写1645由坞堡主、士绅、八旗军头主导共和，议员称国公，元首称大执政；当前角色注释又使用“周公/总统”等称谓，提案暂用“国家元首/现政府”，不自行把异称裁成一套新官制。它曾援助殷人、蒙古盟友，也与美国共同镇压大原可汗国；东洲共和的自由理念和扩张利益有真实张力。[C01](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:164>) [M07](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_historical_leaders_ce_asia.txt:1092>)

|阶段/方向（提案）|可玩议题|成果与约束|
|---|---|---|
|开局共同议程：让东洲相连|东青行及其他公司供给木材、铁和工具；铁路与港口连接实际人口和产业；允许贸易和进口解决缺项。|降低分散市场与交通成本、吸收移民；需就业、投入品和预算。不能靠修路按钮凭空生成移民。|
|通洋共和国|经营太平洋港口、商船、大学/技术交流，和日本、吴/明、秦、法国按利益建立贸易/投资/有限顾问联系。|产业与知识网络；承担跨洋投送成本和商业依赖。支持共和派不自动变成所有君主国的敌人。|
|大陆工商共和国|以东青行和拟“金邑通运公司”为产业载体，扩展内陆铁路与矿产；旧堡主、军户、土地权和地方税收进入议会争论。|大市场、移民与钢铁/机械产业；资产集中、地方自治和前线驻军费用相互牵制。石油后置到真实资源与科技条件。|
|公民共和国|争论债务奴役、选举资格、文化排斥与劳动结社；从真实法律、政治运动及人口待遇推进，先改善教育/资格和就业。|扩大公民基础与劳动力流动；既得债权人、堡主、种植园和商行的反对。不能把四主文化之外群体自动视作同化材料。|
|边疆条约／大陆霸权|和当地殷人、蒙古政权有协议、互市、保障和共同防御；也允许扩张派选择强制兼并，明确战争和治理代价。|前者保留自主邻邦与商路，后者增加领土及治理/外交负担；不把现实Manifest Destiny或1919华夏美利坚合并硬套为必走终局。|
|寡头共和的稳定化|玩家可保留财产权门槛与商号特许，换取信贷/交通扩展；持续处理债务、腐败及受排除者诉求。|有可经营的保守商业路线；不能永久用繁荣修正压掉公民权问题，严重失败由现有政治机制引向改组/革命。|

拟新公司只是候选，不替换东青行：**金邑通运公司**以铁路为主营、钢/引擎为后期扩展；**长岸轮船公所**以船厂/港口联系为主题，须先核公司是否实际可持有每种目标建筑及现行私有化规则，不能从MUC的建筑列表推定一切建筑都能按同样方式买卖。

**拟新增虚构角色，尚非正史：**

|人物|1836身份与利益|实际可承载事件|
|---|---|---|
|佟世衡（1790年生）|皑雪军户后裔、东青行董事；工业家，主张扩大铁路与内陆市场，也希望保留土地契券和债权强制力。|公司特许、铁路穿越地方土地、外国投资与兼并；可支持郭庆达对外妥协，但在债务奴役改革上与其分裂。|
|沈季川（1798年生）|大原港口商人家庭出身的律师、报刊组织者；知识分子，支持自由劳工与扩大公民资格，认为共和权利不能只属于创国家族。|债务劳工案件、移民资格、地方议会和边疆协约；改革成功可进入政府合作，遭镇压后成为激进反对者。|

以上只是角色职能提案，出生地、文化与亲缘关系尚待作者确认，不写成已经存在的北明人物。人物应在自然死亡、失势、迁移或政府更替时由同一利益集团的继任者承接议题，而非因单一人物不在就锁死国策。

## 7. 后续实现的最小边界

1. 复用法国已有政治主线、CNE土改、USM明吴结算及HUS开局公司；经济议程用国家当前状态与真实成果开启。
2. 产业建设、国家经营政策、公司繁荣、公司所有权是四件不同的事；公司商标和奖励不能代替生产、就业和投资。
3. AI先核财政、战争、领土、条约、科技和对象存在，再选可负担方案；同一建设成果对玩家/AI采用同一结算定义。
4. 目标州失去、公司解散、国家继承、政体变化及共同市场变化允许暂停、转轨或失效；清理不会删除真实工厂和无关外国投资。
5. 本提案未定每国统一数值，不做全局平衡替换，不承诺任何参考MOD兼容性；下一步先把用户选中的分支写成范围明确的设计，再核当前API与实际资产闭包。

## 8. 来源定位与指纹

源文件为最终依据；行号为2026-11-03本地版本。PPT缓存JSON中SHA与只读原件重新计算一致：`b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`。原件：`D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx`。

|编号与文件|覆盖内容|SHA-256|
|---|---|---|
|[R01](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/.metadata/metadata.json:2>)|RAHF 本地 metadata，版本10.9，支持1.13.*|`70df3daa373aae9c9ccf915b1b2b6f339e9264747c39eb6322cff2b219a06526`|
|[U01](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/.metadata/metadata.json:2>)|MUC 本地 metadata，版本和支持版本字段为空|`3764dd5ce9620870ebc87042a04c6c89dff891bfdbb7850c806bf11c0c086616`|
|[R02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_fra.txt:324>)|法国帝国入口324–380；铁路543–595；商业597–668；巴黎670–739；学院741–792|`b1ca2a97851fdd3d9b025f7bef74e04dc1c57c53a8875e0ad4660747655cbf38`|
|[R03](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/france_flavor.txt:133>)|france_flavor.4：152–174加入法国建设子日志|`1898e0529c5bfea2c2dbad271bfece7b3cb9a9c67237c07176b2a08f901ffac5`|
|[R04](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/france_events.txt:2550>)|dsk_france.11/12：2550–2631，建设完成奖励与巴黎总计数|`2c49852f2508e6da119bd0f9adaf2c5b4fb8de14d321efa01ab7d9269e77032c`|
|[R05](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_tongyong_industrial_revolution.txt:2>)|通用工业总日志2–133；航运730–790；重工业793–893|`5b3b04d7c90a9a9e3100ff333b5fe537872822feff407b1bcb94f23e4df85cab`|
|[R06](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/dsk_common.txt:2>)|通用工业事件23–64同时加入多项部门日志|`e176995a43280f4baa0c3b813c37fb7418068e70147bdf60e6d824408740428c`|
|[R07](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/dsk_usa_modifiers.txt:2664>)|行业修正2664–2676|`b564ea3dfcfa7a880bf2f4ede9768a14db79ebb7079effb953088954b990fe4c`|
|[R08](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_chi_QNG.txt:96>)|洋务总日志96–244、铁路246、商业307、军工427、学校577、公司661|`fc38d75563270b2c1b2d8d22d727e30da01d7fc1be0d3cf3657669f08e0e9ea5`|
|[R09](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/ai_strategies/dsk_default_strategy.txt:4>)|INJECT默认AI：按游戏规则、文化、技术、年份、目标区域调州价值|`6e8cf8e5661363071e2f0756a5590c582eadad90cd4c2b71f11479f452b2cb1a`|
|[U02](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_France.txt:583>)|Fraissinet 583–654；法国银行1701–1787；其余法国公司见索引|`cdaf8a07b9707e0cb339a5364d424358afdb2c8664fe6264c1da9bcea3d02163`|
|[U03](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_China.txt:1250>)|江南制造局1250–1319；招商轮船1322–1396；其余中国公司见索引|`384f6e76ef8e5a2f8e28584f9dc5180840536be13ed05a769e09209e860c25b8`|
|[U04](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_USA.txt:4028>)|大北方铁路4028–4115；Levi 1138–1210；其余美国公司见索引|`0608a1f65c4cd674fde54684df8d8d7f9c27bcc7ba5d553d0e8784f206aa6716`|
|[U05](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_Canada.txt:2085>)|Dunsmuir 2085–2150；加拿大公司见索引|`382ed0c6d08af0ae5c770e918e97ba4e387508f74349a268ad9dcbc5beab13ec`|
|[U06](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/company_types/00_flavoured_companies_Mexico.txt:155>)|墨西哥铁路155；Peñoles299；墨西哥银行372|`9ba678d86252a17da7dd592b29bb98f633abb3a9bfd373a5bf2499db95e24ded`|
|[U07](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/journal_entries/more_unique_companies_journal_us_steel_corp.txt:1>)|US Steel整合日志：成立26–77；计月114–124；完成127–138|`abec13aba784b1dedd1072a0feec5cf3bda65244af235b3962bc3236c4714eec`|
|[U08](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/events/more_unique_companies_events_us_steel_corp.txt:3>)|整合事件：移除/新增公司81–127；按建筑等级逐项拆建129起|`8235dc1e5c5725670ada861e52eefa2c69bd61bdfe431312e23e7eb427408aba`|
|[U09](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/script_values/more_unique_companies_event_values.txt:5>)|普通并购JE目标36个月|`661c6c46cabd7b6b848f70d137cf8f63ee6dc7aa3e85af4586d4290f3011c74c`|
|[U10](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/scripted_triggers/00_unique_companies_scripted_triggers.txt:1>)|unique_companies_has_bank共用触发器|`f2aeb8da9df3d8fbab0317f8c9940e80998cf9e9d23bf672d162e48b1c26a643`|
|[U11](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3032185644/common/game_rules/00_unique_companies_game_rules.txt:1>)|银行开关游戏规则|`969ab9c574698f7e105b4ab763a9d01bc3a268f95617500deb10a4f0deb01941`|
|[G01](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/company_types/00_companies_france.txt:144>)|本机GAME DMC：主营、扩展、声望商品门槛、成立条件、繁荣、AI目标|`f4078c4ccd97956e681ece7df5b2a43c07943cbb35cd54baac7812ef8f202b2a`|
|[G02](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_prestige_goods.txt:1>)|本机GAME声望衣物完整JE，36月繁荣/前三生产名次链|`28d78a15b585a27b3978570b22b978ede32ecf31d5b9112f7dae194a320649fd`|
|[G03](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_scripted_effects.txt:1156>)|公司消失重绑定与解散后重加声望JE，1156–1230|`278e5988ba786184ee12e1d806a6c72608e7b45df53fb7e4c4e61a6953f8d1c0`|
|[G04](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/event_values.txt:243>)|prestige_good_journal_entry_months=36|`2bde5cecb435cf0e41ed83987e7acd72adb41578ebc39df5970f176a39469581`|
|[G05](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/prestige_goods/00_prestige_goods.txt:510>)|声望衣物数据库定义|`25b126a94b0a18fdd0e84ad38a87beacd90fadff92905df36a3a23d7b341e23b`|
|[M01](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/fra - france.txt:1>)|法国开局法律16–34；DMC82–86；Cockerill97–101；不稳帝国JE137|`c3e3f99d78fbfb01217841fd1e69043780f68143609a60add096c9ccada7c85b`|
|[M02](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_french_empire.txt:1>)|已有波拿巴稳定/镇压共和/共和运动/奥尔良/波旁五组JE，1、201、338、431、732|`e8a32123bdcafd92ae366d3cb53bf03c2b9308ce95f8ed5aea8624382eb62ff6`|
|[M03](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:1>)|东洲科技8–25；政治法律69–85；公司88–92|`cb1485aa1ec06d0706806a9dbbdb6ab458ea78cbf796ac506a2482c6ecb33608`|
|[M04](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:38>)|HUS已受承认、帝国级、四主文化和加州首都|`7056d622fb21e0d3a72f0af4f73a9a5e23a87f769870b23c5df9043f8fbfb6f5`|
|[M05](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/company_types/ce_companies_china.txt:53>)|福海行53、远北粮农总行165、东青行290；公司定义和AI建设目标|`5475c1fdcc8da9052d280f9c4ba5680fa3ae407f859e1e6761b43cf67f13f7d9`|
|[M06](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_companies_l_simp_chinese.yml:2>)|三家公司有效中文名，不能按内部ID猜译|`4399a53e4a860b4f9ddf81bec3d25aa06d998290ab36af117c8d1a9482b146da`|
|[M07](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_historical_leaders_ce_asia.txt:1092>)|郭庆达模板注释与政治身份：1092–1111|`d740dc245ef314bfa2889687fc23db366b7945c0427f376573d547daf2d595ad`|
|[M08](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:2>)|FRA开局风味2，HUS开局风味12|`a63e35b23b57f2149038acb939b9f6c65fdeceee7fe63829384d941ea5de5071`|
|[M09](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/characters/fra - france.txt:3>)|路易/拿破仑三世模板为统治者，杰罗姆为另一个模板|`daafaa8a3f745be362c36142dbca9cd7d93cf73e90d060fc5bfe3f5ba13f1dd9`|
|[C01](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:164>)|PPT18原文缓存：东洲起源/扩张/共和制度164–191|`227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`|
|[C02](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:324>)|PPT23–24原文缓存：法国帝国与未来线324–375|`227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`|

## 附录：MUC相关公司源码索引

下列是公司定义ID，`TRY_REPLACE:`项为该MOD对原有公司的替换尝试；不是本报告建议全盘移植的清单。法国/中国/美国/加拿大/墨西哥的文件在来源表U02–U06。

### France（36个定义）

`TRY_REPLACE:company_societe_mokta_el_hadid`（4）；`TRY_REPLACE:company_schneider_creusot`（71）；`TRY_REPLACE:company_dmc`（146）；`TRY_REPLACE:company_cgv`（224）；`TRY_REPLACE:company_saint_etienne`（294）；`TRY_REPLACE:company_fcm`（368）；`TRY_REPLACE:company_mines_anzin`（437）；`TRY_REPLACE:company_maison_worth`（505）；`company_CompagnieFraissinet`（583）；`company_HermesFreres`（656）；`company_SocieteJF`（731）；`company_LouisVuitton`（811）；`company_Peugeot`（883）；`company_Bonduelle`（956）；`company_EJB`（1031）；`company_ThomsonCSF`（1106）；`company_Montagut`（1180）；`company_NavalGroup`（1255）；`company_SaintGobain`（1327）；`company_Baccarat`（1398）；`company_Vinci`（1470）；`company_Pernord_Ricard`（1549）；`company_Bouasse_Lebel`（1624）；`company_bank_of_france`（1701）；`company_Bank_Credit_Lyonnais`（1789）；`company_Renault`（1880）；`company_Panhard`（1953）；`company_Duveen_Brothers`（2026）；`company_Bugatti`（2122）；`company_Citroen`（2197）；`company_Michelin`（2270）；`company_Hauts_fourneaux`（2344）；`company_French_Petrol`（2423）；`company_lalique`（2504）；`company_maison_jansen`（2583）；`company_Oberkampf`（2661）。

### China（40个定义）

`TRY_REPLACE:company_kaiping_mining`（4）；`TRY_REPLACE:company_hanyang_arsenal`（88）；`TRY_REPLACE:company_foochow_arsenal`（171）；`TRY_REPLACE:company_jingdezhen`（250）；`TRY_REPLACE:company_jiangnan_weaving_bureaus`（324）；`TRY_REPLACE:company_ong_lung_sheng_tea_company`（428）；`company_Bianyifang`（505）；`company_Changan`（581）；`company_Arnhold`（654）；`company_Chongqing`（730）；`company_Dalian`（799）；`company_DuoYunXuan`（870）；`company_Li`（946）；`company_Xie_Zhi`（1024）；`company_Jian_Hsin`（1095）；`company_ITA`（1169）；`company_Jiangnan_Arsenal`（1250）；`company_CMSNC`（1322）；`company_Jardine`（1399）；`company_Honkong_Electric`（1474）；`company_Commercial_Press`（1550）；`company_Ta_Kung_Pao`（1627）；`company_ShenBao`（1702）；`company_Zhonghua`（1777）；`company_Rong_Bao_Zhai`（1853）；`company_Churin`（1931）；`company_LeeKumKee`（2008）；`company_ASWatson`（2080）；`company_Tsingtao`（2155）；`company_TongRenTang`（2237）；`company_Yanchang`（2309）；`company_Bank_HSBC`（2380）；`company_Tangshan_LRSW`（2497）；`company_Bank_IBC`（2571）；`company_Bank_BOCOM`（2666）；`company_Da_Qing_Bank`（2760）；`company_Ma_Yu_Ching`（2854）；`company_Rui_Fu_Xiang`（2937）；`company_Harbin_Brewery`（3010）；`company_canton_factories`（3096）。

### USA（74个定义）

`TRY_REPLACE:company_standard_oil`（4）；`TRY_REPLACE:company_united_fruit`（72）；`TRY_REPLACE:company_us_steel`（170）；`TRY_REPLACE:company_general_electric`（254）；`TRY_REPLACE:company_william_cramp`（340）；`TRY_REPLACE:company_ford_motor`（426）；`TRY_REPLACE:company_lee_wilson`（501）；`TRY_REPLACE:company_colt_firearms`（586）；`company_CocaCola`（661）；`company_JohnDeere`（743）；`company_JackDaniels`（823）；`company_Remington`（900）；`company_DuPont`（979）；`company_IPC`（1063）；`company_Levi`（1138）；`company_ASARCO`（1222）；`company_Tyson_foods`（1302）；`company_Ball`（1378）；`company_Coors`（1454）；`company_VFC`（1530）；`company_McIlhenny`（1613）；`company_3M`（1689）；`company_Leggett`（1764）；`company_Disney`（1842）；`company_Hasbro`（1919）；`company_Ziegler_company`（1996）；`company_Dow`（2075）；`company_Bechtel`（2152）；`company_TurnerConstruction`（2227）；`company_CooperCompany`（2302）；`company_ImperialSugar`（2378）；`company_KimberlyClark`（2453）；`company_HamiltonShirts`（2528）；`company_BuffaloForge`（2611）；`company_CarrierEng`（2685）；`company_SmithAndSons`（2762）；`company_Abbott`（2841）；`company_Boeing`（2915）；`company_Bank_JP_Morgan`（2986）；`company_Singer_MC`（3078）；`company_Lackawanna_IaCC`（3163）；`company_Heinz_Company`（3245）；`company_Westinghouse_conglomerate`（3321）；`company_Chase_Bank`（3413）；`company_americanbanknote`（3507）；`company_Bank_Goldman_Sachs`（3580）；`company_Bank_Wells_Fargo`（3672）；`company_Bank_American_Express`（3780）；`company_NationalBellTelephone`（3874）；`company_Bethlehem_Iron_Steel`（3945）；`company_GN_railway`（4028）；`company_general_motors`（4118）；`company_Cadillac_motor`（4194）；`company_Chevrolet_motor`（4271）；`company_Dodge_motor`（4353）；`company_Lincoln_motor`（4429）；`company_Western_Union`（4505）；`company_winchester_firearms`（4578）；`company_smith_wesson_firearms`（4658）；`company_Kellogg_Company`（4750）；`company_textile_schumacher`（4830）；`company_Pfaltzgraff`（4915）；`company_standard_fruit`（4990）；`company_American_Arabian_Oil`（5090）；`company_Vance_Lumber`（5169）；`company_Pittsburgh_Coal`（5241）；`company_hawaiian_bank`（5315）；`company_us_steel_corp`（5410）；`company_federal_steel`（5502）；`company_national_steel`（5585）；`company_american_tin`（5667）；`company_consolidated_lake_superior`（5745）；`company_american_wire`（5825）；`company_national_tube`（5907）。

### Canada（28个定义）

`TRY_REPLACE:company_hbc`（4）；`TRY_REPLACE:company_massey_harris`（85）；`company_BTCC`（168）；`company_Labatt`（241）；`company_GTR`（318）；`company_GrayDort`（387）；`company_Farr`（457）；`company_McLaughlin`（534）；`company_Royal_Bank_of_Canada`（605）；`company_LaMCoML`（714）；`company_Bank_of_Montreal`（784）；`company_Molson_Brewery`（873）；`company_John_Booth_lumber_mills`（947）；`company_William_Davies_Company`（1018）；`company_Montreal_RMC`（1100）；`company_Davie_Shipbuilding`（1177）；`company_Montmorency_CMC`（1247）；`company_Montreal_LHPC`（1322）；`company_DOSCO`（1395）；`company_Price_BaC`（1475）；`company_Redpath_Sugar`（1547）；`company_Seagram`（1618）；`company_Boswell_Brewery`（1693）；`company_Canadian_Vickers`（1770）；`company_Irving`（1843）；`company_ford_motor_canada`（1916）；`company_Bank_Desjardins`（1988）；`company_Dunsmuir`（2085）。

### Mexico（6个定义）

`TRY_REPLACE:company_fundidora_monterrey`（4）；`TRY_REPLACE:company_el_aguila`（83）；`company_MexicanRailway`（155）；`company_TequilaHerrandura`（226）；`company_Penoles`（299）；`company_Bank_of_Mexico`（372）。

