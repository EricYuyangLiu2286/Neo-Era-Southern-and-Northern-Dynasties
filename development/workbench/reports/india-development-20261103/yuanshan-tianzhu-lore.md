# 远山、天竺宣慰司：原始设定复读与实施边界

日期：2026-11-03。研究性质：只读原作者 PPT/DOCX、旧 HOI4 工程及当前 MOD；未修改来源、未修改玩法、未开游戏。父任务授权的当轮设计是南明／USM 可通过决议和日志设立“远山”“天竺宣慰司”；本报告把这个最新命名与原稿确证分开。`catalog.py status`：Victoria 3 1.13.11 / Steam build 24799966，CURRENT，0 changed。

本轮重新从原始 OOXML 提取《北明ppet》481条、《海军人物》103条、《北明人物列传》456条，按真实 slide / paragraph 定位；没有以旧 AI 方案替代原文。旧研究只作寻址。PPT 三张内嵌图片也已检查，均为影视插图，不是地图。检索到的命名冲突是实际来源差异，不是游戏验证结果。

## 可以直接采用的结论

1. **远山在本轮适用的近现代殖民资料中指南非，HOI4 实际州定位是纳塔尔。** 不是印度的一块领土，也不是远南／澳洲。旧 HOI4 的 `STATE_719: "远山"` 对应 `719-Natal.txt`；其所有者为昆仑行都司 KL1，KL1 首都也是719。革命国策又直写“远山（南非）”。[H01 L721；H02 L2–3、13–14；H03 L11515–11546；H04 L562；H07 L1，来源表在文末]
2. **旧资料存在另一个“远山＝加利福尼亚”的早期异文。** 《北明人物列传》p330在公子祁航海传说中把加利福尼亚称“远山”，并有“美洲大陆最东侧”的原文地理表述。不可删掉这个异文，也不能据此把近现代南非证据移到加州。当前最新“设立远山”若采用近现代南非路线，是有两类独立来源支持的实施选择，仍应保留异文记录。[BIO p330；NAV p119；H01–H04]
3. **“天竺行都司／吴属天竺”有直接原稿证据；“天竺宣慰司”是本轮作者最新要求的名称。** 本轮复读的 PPT、两份 DOCX、旧 HOI4 文本没有找到完整“天竺宣慰司”词组。HOI4 的“西洋宣慰司”是 XY1 的民主政体名称，不能误当成 TZ1 的同名证据。执行最新要求可命名天竺宣慰司，无须把旧文献伪引成这个名称。[NAV p99、110；H12 L322–324、335–353；H13 L34]
4. **两地行政可以属于同一 USM 海外治理入口，但地理与任务必须分开。** 天竺是印度及相关印度洋岛屿的殖民行政；远山在南非。原文没有给“远山统治天竺”、两司彼此宗属、共同首都或同一统治者的关系。[H05 L13–14；H06 L123–153、180–186、210–216]
5. **不能把1936人物、疆界和军备倒灌到1836。** 王世珍是旧 TZ1 1936殖民军阀首领；山梨半造是旧 KL1 1936首领。PPT把大吴建立南非昆仑行都司置于1855—1861战争之后；海军人物均是后期角色。它们证明制度延续、势力和称谓，不能证明1836两司已存在或这些人物可任初任官员。[H07 L112–122；H08 L1–9、109–117；H09–H11；PPT24 p21]

证据等级：`author_explicit`＝本轮父任务传达的作者明确方向；`text_attested`＝原始文献／作者源码可直接证明；`unresolved_variant`＝异文；`inference`＝受来源约束的解释；`gameplay_proposal`＝本轮可行玩法建议，尚非唯一正史或已实现机制。后文不把一种批准可选未来升级为所有游戏必须发生的历史。

## 地域、首府、人物和文化

| 对象 | 原始资料中可确认的内容 | 年代／不能推出的内容 |
| --- | --- | --- |
| 远山（地域） | HOI4 719＝Natal，纳塔尔；CPC罢工决议明确作用州719。更广义的革命宣传使用“远山（南非）”。 | 1936地域用法；719不能机械等同V3整个南非战略区，也不能把其国家所有者KL1的全部非洲领土都叫远山。H01–H04。 |
| 昆仑行都司 KL1 | 首都719远山；1936领有德兰士瓦、纳塔尔、开普、安哥拉、西南非、贝专纳、莫桑比克、罗得西亚、坦噶尼喀、卢旺达、布隆迪、马拉维、赞比亚共13个HOI4州。 | 这是1936行政跨度，不是1836释放清单，更非取得一座港口后免费获得全非洲的依据。H07 L1、HSTATE_*，逐州行号见证据JSON。 |
| 天竺殖民地 TZ1 | 首都423（原文件注释Madurai，文件名Tamil）；1936直接所有州为281、422、423、424、425、426、427、429。分别为溜山（马尔代夫，原州有MLD核心）、锡兰、泰米尔／马杜赖、安得拉／马德拉斯、卡纳塔克／迈索尔、奥里萨、海得拉巴、孟买。 | HOI4州名、边界不能直接转换V3州。426有MUG核心而非TZ1核心，说明所有权与政治归属声索未完全合一。H08 L1；H01 L283、424–431；HSTATE_281/422/423/424/425/426/427/429。 |
| 1936官员 | TZ1调用王世珍；KL1调用山梨半造；二者人物意识形态均为殖民军阀 `zhiminjunfa`，国家政治为军阀主义、禁止选举。 | 来源没有给出1836初任宣慰使、完整继承名单、任期或任免办法。不得用现实同名者生平补足架空1836官职。H07–H11。 |
| 当地军政 | “天竺大名军”由当地土王军队整编；另有正规天竺军与“联合水师天竺驻屯舰队”。 | 说明本地军事合作与帝国舰队共存；作者兵种注释“非常不可靠”不应变成全体印度人的族群特征。1936编制不能作为1836免费部队。H14 L1–3、28–31；H15 L7。 |
| 文化／宗教 | 核心原稿没有两司1836主文化清单、当地人口比例或国家宗教定案。NAV p70有1886出生于南天竺的移民家庭，p129–131有广东出身军校生驻天竺经历。 | 移民和官员存在不能推出当地已有大量吴／闽人口，不能删除原有印度、非洲文化或让所有居民改宗。HOI4人名及头像也不能充当人口证据。 |

旧 HOI4 TZ1 的民主、非同盟与共产主义变体分别采用马拉塔共和国、马拉塔联邦、马拉塔人民共和国。这证明原作者曾给该殖民政权设置独立后的地方身份，但不是“所有南印度人都属马拉塔文化”，也不是一条已经完备的1836联邦建国流程。[H12 L342–350]

## 对USM、莫卧儿与法国的关系和时间线

| 原始定位 | 原文事实 | 本轮用途 |
| --- | --- | --- |
| BIO p571、574 | 1711—1715吴—莫卧儿战争；郑寰晚年继续扩张德干、马拉塔；吴、闽地主商人在殖民地经营经济作物，但吴国库贫困。 | 殖民地的财富、地方精英收益与中央财政并不相等。可支持地方治理与供给议程，不能把设司写成凭空发财。 |
| PPT23 p6–8 | 1730年代吴吞孟加拉、法国渗莫卧儿；1750年代饥荒与殖民疏于管理；1770年代法英南明瓜分殖民地。 | 1836以前有殖民与法国商业渗透背景。当前V3孟加拉归MUG，旧年代叙述不能直接覆盖当前国界。 |
| PPT23 p17、19 | 1810法明共同封锁英国，1819英国与法国关系正常化。 | 不能写成法国从开局起与南明永恒敌对；法国援MUG的倾向须受当前关系与政策制约。 |
| PPT24 p19–23 | 1853—1860章西女王反抗大吴侵吞；1854吴代明后法国拒绝承认法明旧约；1855—1861吴征服南非，法国放弃支持德瓦士兰独立，成立昆仑行都司；1861吴法恢复正常外交。 | 印度并吞、改朝、南非战争、外交重建是相关但分立的变化。其年份是作者未来线，可提供条件型后续目标，不应强迫玩家在固定年份侵吞或失去一切现有条约。 |
| PPT25 p4、12、14 | 吴法英帮助MUG镇压第二次印度起义；随后法吴为分配利益冲突；1893以孟买所在马哈拉施特拉地区划分印度势力范围。 | MUG王朝、印度民众、吴、法国各有利益。1893孟买界线不能冒充1836行政边界。 |
| NAV p25、62、119 | 一战期间法—莫联合舰队对吴作战；另有吴袭法属远山（法属南非）的计划。 | 法莫合作和南非海路竞争的后期旁证。与PPT1850年代南非征服之间存在疆界／时代空白，不能自造一条完整法吴属权更替。 |
| H13 L34 | MUG长期为法国霸权附庸，王朝以外援镇压；大战末换英德支持得到独立和王朝延续，仍困于资本债务／倾销并受南方天竺威胁。 | 可用于半殖民地与外援代价；独立转向是1936回顾，不能放入1836既成事实。原文“和属”是旧名异文。 |
| H06 | TZ1、KL1同属吴的朝贡体系；不同DLC设殖民地、傀儡或帝国属国。 | 最稳固的是各自对吴从属，不能把HOI4自治枚举当V3法律；无两者互为宗主的证据。 |

当前V3的实际关系是USM对TRA有傀儡条约，MYS关系只有该国存在时才创建；FRA对MUG为朝贡。[M02 L136–147、185–196] 作者原始MUG背景明确提出倚法、转向东方或自力更生的开放选择，当前该条与2026-10-30作者备份逐字一致。因此新天竺行政不应把“所有印度国家已默认效忠USM／MUG／法国”写入旁白。[M07 L30＝B01 L30]

## 1836当前源码与旧未来地图的交界

当前USM在印度直接所有的候选地区为下表。表中“地区”表示state_region；实施只能转移其中**当下实际属USM的owner-state**，不能把分享该地区的他国部分一并给新司。

| 地区 | 当前州历史定位 |
| --- | --- |
| 锡兰 `STATE_CEYLON` | M01 L1647–1666 |
| 印度洋领地 `STATE_INDIAN_OCEAN_TERRITORY` | M01 L3327–3340 |
| 西尔卡斯 `STATE_CIRCARS` | M01 L4123–4134 |
| 迈索尔 `STATE_MYSORE` | M01 L4174–4186 |
| 特拉凡哥尔地区 `STATE_TRAVANCORE` | M01 L4187–4202；不等于吞并独立TAG TRA |
| 马德拉斯 `STATE_MADRAS` | M01 L4203–4225 |
| 古吉拉特 `STATE_GUJARAT` | M01 L4254–4300 |
| 库尔努尔 `STATE_KURNOOL` | M01 L9331–9346 |

当前南非六个相应大区（开普、东开普、北开普、祖鲁兰、奥兰治、德兰士瓦）没有USM所有块。祖鲁兰归ZUL/BST，德兰士瓦由MTB/TRN/PDI/SWZ/VND分治；不可因PPT后世征服直接改1836开局。[M01 L3445–3517、5957–6036]

当前USM定义主文化是 `ce_wuu min`，首都南京。[M03 L1–11] 这只证明宗主的主文化；不证明新天竺／远山必有同样主文化。当前MOD已有“海外宣慰司”政府类型，条件包括殖民国家、USM属国、傀儡或自治领、总统共和、无选举权及汉文化特征；这是既有实现约束，不是原稿对新司文化／制度的定案。若沿用它，必须在实施时核对条件和新国家实际政治配置，不能为凑显示而悄悄改当地文化。[M04 L69–98；M05 L2–4]

## 有边界的实施建议（全部为gameplay_proposal）

### 天竺宣慰司

- **所有者与入口**：USM持有实际印度领地时出现设司议程；明、吴两种身份按当前合法政权显示相应宗主称谓。行政重组是一个可选决策，不要求先把所有土邦吞并，也不把占有全部印度作为开局门槛。
- **土地契约**：初次成立只接收选定范围中USM实际拥有的部分；既有第三国、MUG、TRA、外国资本所有权继续各按自身法律／条约处理。USM以后取得其他印度领地可另行划拨，不能用1936清单预先赠地。
- **首府**：原稿的1936首府证据是南方泰米尔／马杜赖。新司首府可在实际取得、人口和行政条件合适的南印度州选择；马德拉斯是当前地图上的合理候选，属于推断，不称为原稿指定1836首府。若只剩锡兰等有限领地，则条件化选择现实可用首府或推迟建司。
- **官员与族群**：不生成王世珍或晚出生海军将领；用经原版链条核验的当代任命方式／时代合适的角色。殖民统治者主文化、种姓体系与国教必须独立定案；保留真实印度人口、宗教、建筑和当地所有权。可保留中央委派与本地精英合作的制度差异，不用同化来掩盖歧视。
- **持续日志**：以行政、教育、基础产业、地方接受度、海军与驻军负担为主；中枢只在建司、重大自治议价、外援介入或起义暴露时接收事件。与MUG的“策动南方”按实际新所有者接续，不能USM一设司就让已建立的地区案件消失或永久找不到对象。
- **宗属与战争**：新司对USM有真实从属关系；TRA是否转归新司不得默许，应保留USM直辖宗属或另开真实谈判。MUG/法国援助、既有战争和条约均按各自实际对象迁移或退出；建司不自动给予MUG主权，也不强制法国对USM开战。

### 远山

- **入口分立**：放入USM海外治理／南非方向，与天竺议程并列。开局无地时可以展示征服／经营的长期目标；不可无条件生成有地属国。
- **地域锚点**：以纳塔尔—祖鲁兰沿海为最强词源锚点。HOI4 Natal与V3 Zululand不是同一地图单元；实际映射须另核province和港口。扩展到其他南非州只接收USM实有部分。是否再扩为“昆仑行都司”是新后续设计，不能把1936的13州免费视为远山成立范围。
- **政治身份**：“远山”在原稿中首先是地域／首府名，未找到独立国家定义。作者本轮要求将其成立为实体，可以执行；将它称为“远山宣慰司”“远山行都司”或直接“远山”须作为本轮新名称记录，不能伪称旧HOI4已有同名TAG。
- **法国和本地诸国**：PPT允许法国保护南非国家并在败局中放弃，支持有条件的外交对抗与妥协。不可把所有本地国家写成法国傀儡，或让建司按钮直接吞并未参战第三国。当前土地何时合法取得、停战是否允许、法国是否还愿干预分别核验。
- **成长与退出**：成立后关注港口、交通、地方治理、移民与财政；不创造大批吴／闽人口。因失地、独立、改宗主或USM灭亡而改变身份时，清临时行政支出并保留真实人口产业成果；后续重新设司不得重复刷初始补助和军队。

上述是行为契约而非已证明的V3脚本接口。父任务仍须按NESND要求读当前原版调用者→effect/trigger→数据库→资源的完整链条，确认国家释放、州转移、军队、人物、条约和生命周期。这里不提供未经验证的effect拼法，不认证引擎行为。

## 双语术语与作者文体边界

| 中文 | 建议英文 | 依据与状态 |
| --- | --- | --- |
| 天竺 | Tianzhu | 保留世界内专名；首次确需说明地理时可释作Indian possessions，不用British India。新工作译名。 |
| 天竺宣慰司 | Tianzhu Pacification Commission | 本轮作者指定中文；英文沿现有Luzon／Nanyang Pacification Commission，不另造Governor-Generalship。M05–M06。 |
| 宣慰使 | Pacification Commissioner | 当前已定译名，M05 L4。 |
| 天竺行都司 | Tianzhu Regional Military Commission | 旧名的工作译法，用于研究／旧史回忆；不能自动替换用户最新“宣慰司”。未发现旧工程的可靠正式英文。 |
| 远山 | Yuanshan | 保留专名；研究注释写Yuanshan (Natal / South Africa)。不直译Distant Mountains，不混Far South。 |
| 昆仑行都司 | Kunlun Regional Military Commission | 后期旧实体，工作译名；旧tag注释写Yamato Africa District，是早期“和”残留，不宜直接当现版本英文。 |
| 远南 | Yuannan | 与远山分开；旧资料对应大洋洲，此报告不为其改名。 |
| 莫卧儿／印度 | Mughal Empire / India | 王朝与国家政治共同体分开；当前已有词保留。 |
| 马拉塔 | Maratha | 旧TZ1独立变体可用；不把此身份覆盖全体南印度文化。 |

本报告只写研究与行为契约，没有提交玩家正文，因此没有声称“文案对读通过”。后续文案应遵循独立 `nesnd-player-writing`：作者原始MUG条体现的是衰落压力、外国干涉与开放路线，不是“先点击三个改革按钮”的开发说明。此次核对M07/B01逐字一致，可供印度日志语体取样；新设司正文还须读取原始海外同类JE/事件并逐项并排审稿。

## 原始来源和可复核证据

定位中 `PPTn pm`＝原始演示第n张、XML段落m；`NAV/BIO pm`＝DOCX `word/document.xml` 含空段计数第m段。文件行号按原始UTF-8文本。以下来源均已本轮重新读取并记录SHA-256；完整55来源指纹、原始段落及逐行摘录见 [primary evidence](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-development-20261103/yuanshan-tianzhu-primary-evidence.json>)，紧凑可读版见 [primary excerpts](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-development-20261103/yuanshan-tianzhu-primary-excerpts.txt>)。

| 编号 | 文件 |
| --- | --- |
| PPT | [北明ppet.pptx](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx>)，SHA `b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae` |
| NAV | [海军人物.docx](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/海军人物.docx>) |
| BIO | [北明人物列传.docx](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明人物列传.docx>) |
| H01 | [HOI4 地名](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/localisation/replace/CEM_state_names_l_english.yml:721>) |
| H02 | [HOI4 纳塔尔](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/history/states/719-Natal.txt:1>) |
| H03 | [HOI4 远山罢工决议](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/common/decisions/CPC_decisions.txt:11515>) |
| H04 | [HOI4 海外抗战原文](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/localisation/replace/CPC_focus_l_english.yml:562>) |
| H05 | [HOI4 国家注册](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/common/country_tags/CEM_countries.txt:10>) |
| H06 | [HOI4 吴属关系](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/history/countries/DMF - Dahelianbang.txt:123>) |
| H07 | [HOI4 昆仑历史](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/history/countries/KL1 - KunLunDistrict.txt:1>) |
| H08 | [HOI4 天竺历史](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/history/countries/TZ1 - TianZhuColonies.txt:1>) |
| H09/H10 | [昆仑人物](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/common/characters/KL1.txt:3>)、[天竺人物](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/common/characters/TZ1.txt:3>) |
| H11 | [HOI4 人物名](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/localisation/replace/CEM_characters_l_english.yml:9>) |
| H12 | [HOI4 国名变体](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/localisation/replace/CEM_countries_l_english.yml:319>) |
| H13 | [HOI4 MUG背景](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/localisation/replace/DMF_bookmark_l_english.yml:34>) |
| H14/H15 | [天竺陆军](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/history/units/TZ1_1936_land.txt:1>)、[驻屯舰队](<D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)/history/units/TZ1_1936_naval_mtg.txt:7>) |
| HSTATE_* | 旧HOI4 `history/states/`，逐个绝对路径与行号见primary evidence的HSTATE记录；没有依赖州名猜所有权。 |
| M01 | [当前州历史](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:1647>)；印度摘录另列MSTATE记录 |
| M02 | [当前宗属](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:136>) |
| M03 | [USM定义](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:2>) |
| M04 | [现有宣慰司政府](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/government_types/00_ce_government_types.txt:69>) |
| M05/M06 | [政府英文](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/english/replace/ce_government_l_english.yml:2>)、[既有国名英文](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/english/replace/ce_countries_l_english.yml:99>) |
| M07/B01 | [MUG现行原文](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:30>)、[作者备份同条](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:30>) |

本轮技能复核：已读取NESND、player-writing、工程适配、目录路由、叙事入口、制度纠正与research技能。没有来源支持的新永久写作规则；未修改技能。所有待定事项已给出不吞第三国、不倒灌未来、保留实际人口及可选路线的实施边界，无需将研究不确定性转成阻止已授权开发的额外审批。
