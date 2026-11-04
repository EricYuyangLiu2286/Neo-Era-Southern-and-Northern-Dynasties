# 印度土邦与南洋邦国：生存、市场与政治独立方案

2026-11-04。状态：只读源码研究与方案，尚未实施，未打开游戏。按 NESND 与 Matt Pocock research 技能完成；catalog.py status＝1.13.11 / build 24799966、CURRENT、changed_count=0。下文“建议”均不是当前代码行为；源码链可证明接口和设计形状，不能证明实机节奏。末尾来源账记录本轮读取文件的 SHA-256 和行号。

本方案让小国先解决能否生存和接入需求，再形成自己的税基、人才与政治组织。后期的独立可由旧王朝、地方贵族与商人联合争取，也可由受压迫群体推翻本国旧制度后争取。革命、国家独立、离开市场是三个不同结果；它们不互相自动代替。普通政治目标采用有关 IG 执政与合法性50；经济建设不自动加政治资格，全部路线禁止党派组合条件。

## 1. 当前对象与准确范围

当前 `nesnd_india_prince` 明列43 TAG，另接受 `nesnd_india_local_state` 标记；同时要求国家存活、非分散政体、在印度战略区有带人口的州，并排除帝国组。43 TAG 为：

`ALW ASM AWA BAG BAS BER BHO BHV BHW BIK BUN COC COO DHA GAR GWA HYD IDA IND JAI JAS JEY JHN JOD JUN KHP KNO KOT KUT MEW MNP MYB NAG NAR NAW PAN PLP PTA PTN SAT SIN SUR TRA`。[M01]

这不是“全部印度国家”的通用列表。`MUG/BHT/DRA`及带`nesnd_india_imperial_line`的国家走帝国路径；`MYS`虽然有国家定义和附属历史条件，但不在43项枚举中，本轮对主`00_states.txt`国家归属字段检索为0，不能当作开局活国。`IR1–IR6`分别对应西尔卡、库尔努尔、马德拉斯、迈索尔、特拉凡哥尔、古吉拉特的既有起义演员；它们不是六个开局土邦。`TZ1`是天竺宣慰司；`YU1`是远山宣慰司（南非），不是南洋；`YN1`远南才是南洋—远南网络中的既有国家。[M01/M03/M04/M05]

南洋方案的首轮明确名单如下。它是本轮设计范围，不声称所有国家已经有相同小国JE；所有新入口还须实际存活和持地检查。中文沿用有效MOD本地化。[M06/M07]

|分组|TAG与现有名称|本方案用途|
|---|---|---|
|岛屿与海峡邦国|ACE亚齐、BAL巴厘、BRU文莱、BLG布隆彦、LAN兰芳、JMB占碑、SAK锡亚克、SRK梭罗、YOG日惹、BNJ班贾尔、KTI库泰、TID蒂多雷、PON坤甸、SEL雪兰莪、PRK霹雳、SMB三发、STG新当、JOH柔佛|主小国生存组；兰芳采用既有共和国/地方商人政治，不硬套王朝独立|
|菲律宾网络|MGD马京达瑙、SUL苏禄；PHI菲律宾|前两国采用小邦路径；PHI是区域中介与可能的宗主，不按一州邦国调平|
|大陆东南亚|BUR缅甸、LUA琅勃拉邦、CMI清迈、CHP占巴塞、CAM柬埔寨、SIA暹罗、DAI大南|小邦与区域强国分别取尺度；不能要求缅甸和清迈建设同样等级|
|区域中介|DEI南洋联省、YN1远南|作为市场/外交对象及其自身自主路线；DEI不是“荷属东印度”，YN1不是YU1|

`ce_subject_relationships.txt`将大量上述国家设为USM附属：PHI/BUR/LUA/CMI/CHP/CAM/LAN/DAI/BRU/BLG/DEI为dominion，SIA为tributary，JMB/SAK/ACE/SRK/YOG/BAL/BNJ/KTI为puppet，TID/PON/SEL/PRK/SMB/STG为protectorate，YN1为dominion；PHI另拥有MGD/SUL puppet。[M06] 但`00_subject_relationships.txt`仍有DAI→CAM及SIA→CHP/CMI/LUA的旧关系块。[M08] **这是重叠历史声明，需要运行态确认，不以文件名排序推断最终宗主。** 所有协议和门槛使用实际`overlord`、市场所有者和直接/间接附属关系，不用开局TAG表代替。

## 2. 当前可复用内容与缺口

印度土邦已有常驻`nesnd_india_princes`，按钮用于自治、独立、向FRA/MUG/USM寻求防御；对法援助有单独JE。协议已保存双方、请求序号、双方宗主、政体、45日期限和6月冷却；回复重验对象及原承诺。自治增加、和平独立、原生防御条约、印度统一吞并已有执行入口。统一复制的是既有成果标记，不可把它当作已经转移全部资源或已经避免全部重复奖励。[M02/M09/M10/M11]

缺口是土邦自己的经济与社会过程：帝国改革目前有大学5/纸厂8、煤铁工具15、钢5、军工10、铁路10、40营等大国尺度；这些不应直接成为微型邦国自主路线的前置。原有工业目标已经允许市场供给替代部分本土煤铁工具钢生产，可复用“自己建设或借市场”的原则。[M01] 不把现有门槛全局削弱；新建小国尺度的独立分支。

当前六地区起义由印度帝国赞助，要求改革完成、民族主义，附属帝国另需60营与合法性50；地方至少30万人且实际殖民所有者控制，动荡≥0.15或平均生活水平<10。准备、暂停、恢复、发动、建国、外交博弈、结算各有阶段，州区保存案件与唯一演员。[M03/M12/M13] 这不是“土邦国内底层革命”现成实现，也不是无条件每到1853就爆发的大起义；新的底层路线不能重复借同一地区另造第二个IR演员。

天竺/远山两司已有后置行政转置：天竺需12大陆目标区、3土邦或3土邦地域、2莫卧儿核心区，并有港口、行政和科技；远山需4目标区等。小国路线应读取两司造成的真实宗主/领土变化，保留本地人物、建设和国家承诺，不能为使两司成立而自动剥夺小国的一切发展成果。[M04]

## 3. 阶段、行动与结果

年份只作观察窗口：前期约1836—1850、中期约1850—1870、后期至1936；实际按国家能力与危机发生，不按年份替玩家完成。

|阶段|玩家直接行动|印度重点|南洋重点|成功与失败|
|---|---|---|---|---|
|前期：保住生计与国库|调整PM和税负；建设一种有需求的行业；改善交通；利用现有市场或争取市场控制；必要时寻求防御|粮棉/地方工艺/矿产各择其有资源者；小邦不要预建整套军工|港口与海运、木材/种植/地方加工；内陆邦以邻国运输为主|收益来自真实岗位、税基和商品可得性；暂时亏损/战争暂停累计，不删已有资产、不立刻宣判整条路线失败|
|前中期：两条市场路线|A 借邻国/宗主市场，以专业产业换取工具、纸与军需；B 取得自己市场后以贸易和有限替代产业分散风险|可在MUG、FRA、USM实际网络中协商，受现有宗属与条约限制|区域中介DEI/PHI及邻国可合作；不允许邦国任意把自己转入第三国市场|A快、初始成本低但依赖高；B更自主但短期价格/财政风险大。独立市场不等于必须自产全部商品|
|中期：地方能力|学校/行政/军官训练依本国规模择项；保护有效运输；让改革利益进入职业与地方组织|村社、种姓与地主关系；保留既有宗教/社会等级设定|港口商人、种植劳动者、乡村与宫廷的利益冲突|形成可持续财政与人才；逾期不发虚假完成奖励。无改革仍可生存，但后期妥协成本更高|
|中后期A：旧政权自主|现任王朝/地方精英通过合法性50、地方支持、外交和军备争取自治或独立|可保王朝，选择与印度统一者结盟、议价加入或保持独立|王朝、兰芳的地方共和精英、商人议会分别表达诉求|宗主同意才和平兑现；拒绝形成冷却/自由渴望与外交机会。武装独立按真实博弈，战败/吞并可失国|
|中后期B：底层激进变革|村社、工人、士兵与受歧视群体在生计/镇压冲突中形成运动；玩家可让步、联合、镇压或承受革命|土地、徭役/债务、平等服役与村社代表权；和既有第二次大起义背景相接|种植劳动、港口工会、村社土地与地方宗教/文化平等|本国政体革命与对外独立分开结算。革命成功仍可能是属国；独立成功也可能保留旧国内制度|
|后期：独立后的秩序|重订市场、防御与宪制；处理新税负、原外国权益、统一要求|和平加入更大印度政体不是自动死亡失败；但主权让渡需玩家明确选择|区域邦联/协定合作只在实际关系支持时成立，不强行建“现代民族国家”|留下真实法律、产业、人口和外交后果；失败路线允许仍存活者重新组织，绝不每次失败重刷同一历史人物|

常驻主JE展示国家当前处境；建设/谈判/政治冲突分别是后置子JE。前期常驻目标无需定期点“领发展点数”；经营状态自然累计。按钮只服务于有代价且不同利益的行动：择市场政策、指定谈判对象、提出宪制/土地妥协、暂停危险请求。完成奖是一次限时奖励或制度结果，维持条件的收益自动续期，避免重复点击维护。

## 4. 门槛采用相对条件，但保留真实硬约束

下列为**候选数值示例**，不是平衡结论，也不是新引擎符号。

|议程|不可替代硬条件|可变条件/示例|避免的错误|
|自主财政|国家存活、有本土人口与收入；无当前违约；费用能支付|成本取本国数周净固定收入并设小邦可承担的下限/上限；现有法援4周收入、£25k–125k只能作量纲实例，不直接套小国|所有国家固定£20k；负收入生成负费用；只看金库而忽略持续支出|
|有用的本土产业|有真实建筑/岗位；目标商品并非仅仅不存在需求|目标厂就业≥75%并有盈利可作经营验收；需求按本地/市场规模判；无资源国家可用进口或同市场供给|要求每邦煤铁钢枪纸大学铁路全齐；把市场总产量算成本国贡献|
|和平自治/市场权|实际直接宗主或市场主人存在；原生动作/条约允许；对象未变更；无重复请求|参考原生`economic_dependence`，用0.8/1.0/1.2三档增加谈判倾向或准备速度；这些不是“依赖占比80%/100%/120%”|把经济依赖误当0–1百分比；把低依赖设成任何外交都不可绕过的硬锁|
|旧政权独立|政治行动需要相关IG执政＋合法性≥50；外交对象和战争合法；实际已独立才能完成|候选军事比率B＝本国army_size/max(实际宗主army_size,1)。B≥0.20、B≥0.40分档提高议价；盟友支持、宗主多线战争可替代部分实力要求；舰队/运输仍看真实情况|“必须60营才能独立”压死所有小邦；营数比率冒充完整战力或胜率；宗主亡国后继续除以旧值|
|底层政治传播|存在适格运动/人口/角色与真实不满；需当前技术/法律允许相应运动|多源传播：城镇职业、识字、学校/出版渠道、生活下降、压迫与外部示范分别影响；采用有限期地区支持/激进化修正|强迫底层运动先掌政府或合法性50；把“思想进步”国家flag当真实人口变化|
|自建市场稳定|市场已经实际归己；交通/港口条件有效|连续若干月重点投入品无严重短缺、价格与预算可承受；压力期允许贸易、改PM、减军费等调整|宣布独立市场瞬间送足商品；自动保价；伪造库存采购系统|

经济依赖在引擎文档标注为昂贵查询；适合谈判预览和月度/季度阶段计算，不给几十个邦国每周对所有列强做全排列扫描。[E01/G01/G02] 营数比率是可解释但粗略的源码候选：此轮未核出可安全直接套用的“综合相对国力”单一接口，不发明`relative_military_power`。更精细战力、盟友可投入兵力与远征运输需分别核查。

临时合法性49只暂停需要政府授权的行动，50/51可继续；党籍变化不改变资格。政体被革命改变时旧“王朝自主”子JE失效，已有经济成果保留，转入相应新政府后继。不得将王朝路线的合法性门槛抄给底层革命发动条件。

## 5. 1.13.11实际市场路径

本机`treaty_articles`没有`customs_union`条款。已查到以下完整链：

1. **属国取得自己的市场**：`request_market_control`要求目标是本国当前市场主人；独立成员或满足直接附属及自由渴望≥25条件；存在催化剂冷却；接受/拒绝各有关系和自由渴望结果。其pact设置`market_owner = first_country`，强制持续12月并核宗属/集团成员关系。`grant_own_market`由宗主/集团领袖授予，pact设置`market_owner = second_country`。[G01/G02] 这是现成玩家外交入口，新增JE可引导玩家使用并观察市场owner；不能仅因原生pact存在就宣称脚本强行create pact也会执行同样审批、accept_effect和合法性。
2. **通过集团进入共同市场**：`join_power_bloc`条款核独立、非集团领袖、相对威望/等级、目标集团领袖和leverage等；生效时执行`join_power_bloc`。只有目标集团实际具备`identity_trade_league`或`principle_market_unification_2/3`提供的`power_bloc_customs_union_bool`等市场效果，才可据此谈共同市场。[G03/G04/G05] 加入任意集团并不自动加入一个共同市场；现为他国属国也不能绕过条款要求直接签入。
3. **跨市场贸易**：原生no_tariffs、trade_privilege、transit_rights、foreign_investment_rights是各自权利；它们不能在文案中冒充转移市场所有权。先允许现成贸易与产业需求自然汇合，不新增采购数量、仓储、预付款、履约或保底供给。[G06]

因此前期“借邻国市场”有两种合法体验：已经同市场时做专业化；不在同市场时先贸易，满足宗属/集团与条约条件后才真正改市场。独立邦国不能靠一个忽略关税同盟资格的剧情按钮自由换市场。政治易主、集团解散、独立市场pact结束后，月度JE按实际market.owner重新评价，保存旧采购承诺没有意义。

## 6. RAHF日本：真正可借的传播结构与不能借的部分

已核metadata：WORKSHOP/2893069455，Realism Ai Historical Flavor Mod 10.9，支持声明1.13.*；这只是安装源码声明，未加载运行。[R01]

**链A：外部冲击→阶段→地方支持与IG反应。** `je_jap_shougun`月事件调用`open_japan.1/.2/.3`；开国/尊攘事件改变法律、外部权利、幕府相关修正、IG意识形态并设置`respect_king_var`。`je_respect_king`据标记或强制开市修正开启，月度调用安政大狱、樱田门、生野、天狗党、禁门等。樱田门对部分州加`sonno_sentiment_boiling`，实际定义为自由派运动POP支持乘数+0.15等；不是瞬间把15%人口变成运动成员。后续`satsuma_military`含`state_radicals_from_political_movements_mult = 1`，原注释却写生活水平，实际键应优先于注释。`ig_radicalized`实际只含IG认可度−3和政治力量−0.15，不等于直接提高原生运动激进度。[R02/R03/R04]

**链B：阶段→人物改思想→法律态度。** 日本帝国JE的月事件调用`sino_event.31/.32/.33`，分别选择成年、非历史、非统治者、不忙碌且所属IG非边缘的politician，保存`gaixi`，再`set_ideology`为开明保皇/明治/大正；第三事件还向工业家IG添加意识形态。这证实了按角色和处境传播思想的结构，不能说它已经把全国人口或某个运动统一改思想。其空trigger/候选可能为空和迟到对象重查不能照抄。[R02/R05]

**链C：既有人物复用。** 倒幕JE完成先全球查西乡模板、再查流亡池、最后才创建，并赋予领袖/将军角色；模板采用水户学意识形态并有1854—1877指挥官出场窗口。[R02/R06] 可以借“一人一身份、先现存再流亡再创建”的模式，不能把西乡、现实明治复辟、黑船年份和JAP现实政治直接搬成南洋/印度剧情。

**完整的人物→运动→社会变革，需要原版机制补齐。** 原生政治运动定义区分`character_support_trigger/weight`、`pop_support_trigger/weight`、`character_ideologies`（运动可向受压IG领袖赋予的思想）、革命/分离及激进化因素；这些方向不是同一件事。`pop_support_factors`仅供UI展示，原生文档明确不产生玩法效果。`movement_radical`本身需平等主义技术和相应非共和等法律环境，并有本国/地区特别排除；角色须满足激进/虚无/共和等资格。[G07/G08] 新人物改成激进派仍需有合格运动，POP实际支持也须规则允许。方案不造“意识觉醒值”等同于V2 consciousness的假接口；如需要自定义传播进度，它只能是剧情组织程度，必须另接真实运动/人口/人物效果。

RAHF还出现state内`add_radicals`、state_region上直接`add_radicals`/modifier等疑点；本机引擎文档分开country的`add_radicals`与state的`add_radicals_in_state`，州区应定位实际本国owner-state再执行。[R03/E02] 不复制有疑点的scope写法或未核资源。思想传播可借结构，既有人物、图像、DNA、地方文化与史实节点不搬运。

## 7. 人物出场建议（提案，未造新人物名）

|人物类型|适格出场与岗位|如何影响路线|退出|
|---|---|---|---|
|土邦财政/军务改革者|国家存在、改革压力与合适职业/IG存在；优先现有适格人物，不直接替换王公|支持有限学校、税制或军备；进入政府需要玩家实际组阁，人物出现不等于自动立法|死亡/流亡后由制度成果继续，不重复刷同名人|
|港口商人/地方议事代表|港口与实际贸易行业形成就业；兰芳/南洋联省沿用各自制度|偏好市场协作、投资与有限自治，但可能反对劳动/土地改革|市场易主更换外交目标；保留人物和真实财产，不立即变成反殖民者|
|村社/种植劳动组织者|受压群体真实存在，土地/生活/劳动冲突持续，适格运动或前置技术可达|从有限权利要求发展到革命，支持条件依本国法律与压迫，不因姓氏/宗教自动激进|运动消散则临时传播修正结束；流亡可在有容纳条件的真实国家继续，不能永生|
|旧王朝独立派|实际君主政体和地方政治支持；主张自治而非必然反动|能与底层暂时结盟对外，胜利后再次面对国内分配|革命废君后王朝路线结束，仍在位或存活人物另按既有角色处理|
|章西女王/村社阿里|PPT明确第一次大起义因吴吞地、第二次因莫卧儿统治与饥荒；实际角色模板、年代、生死、州属仍要另核|作为具名历史/设定路线的后置入口，避免一套“所有起义都是同一人”|此轮不承诺当前游戏已有模板；不得因日期到了强制生成或复活|

PPT第24页的1853—1860、25页的1876—1889及1889—1893是作者一条未来线，为条件式冲突提供依据；不能宣称观察者局在这些年份真的发生相应事件。[C01] 有关新人物的名字、籍贯和对白还须作者文本采样，写玩家文本时另用nesnd-player-writing。

## 8. 生命周期与唯一结算

|边界|建议处理|
|---|---|
|开局/旧档进入|显式add入口和自动possible共用准备；初始化不覆盖已存在进度、已完成标记和实际市场。分别验证JE先激活、月脉冲先发生|
|条件暂失|经营、财政、合法性或运输暂时不足只暂停对应收益；保留已建产业、已完成阶段与有限累计。运行说明清楚指出当前阻碍|
|宗主亡国|存活邦国先清对旧宗主的请求/回复锁，再读实际独立或新宗主；独立事实是新阶段，不能向亡国宗主索要批准，也不免费重复领取“独立奖励”|
|宗主易主/改tag|同一存活国家改名/改tag按实际对象保留国内建设；对象或政体承诺变更则旧请求作废，新关系重新谈。USM→吴的同对象政治变化不默认丢失地方产业|
|小国亡国|本国JE停止。不要由已死TAG自己的周脉冲重建；若获授权设计复国，只能由存活控制者/外部已证回调发起，并核真实原地区，不能夺第三国土地|
|统一/自愿加入|先完成真实吞并或关系改变，再迁移允许继承的成果并登记完成；经济发展成果按实际资产保留，政治自主奖励不迁移复制。明确主体丧失主权而非自动让玩家转国|
|革命/分离|国家自主与政体革命分别记终态；本国原生革命不共享IR1–IR6地区演员；已有地区案件活跃时禁止为同一领土另发同一类起义。先检查原生内战/博弈，再决定剧情只提供压力还是创建特定战争|
|两司成立/失去地区|当前地方案件核owner/control与历史对象。成立宣慰司并不重置同区案件；失地主线暂停或结束，已转移州的修正由新owner-state规则处理|
|协议拒绝/超时/迟答|共享请求序号与双方身份检查，清双方锁、保留明确冷却；对象无效不先写“接受完成”再落空；新请求不能被旧事件清理|
|胜利/退让/白和/战争消失|同一共享结算入口只处理登记的博弈/案件；检查实际独立、持有原地区、目标关系，再奖励。原生退让与战争结束两个入口不能双奖|
|人物死亡/流亡/换IG|事件预览不用执行中才建立的scope；实际执行重验存活、归属、角色、仍适格；无候选安全结束，必要时另找新适格者，不复制人|

每个进度条定义单位、上下限和唯一写入者。政治传播进度不得同时作为财政库存和独立军力。所有写入、初始化、按钮消费、显示明细、终态共用数值来源；同一资源只允许当前路线的周期回调增长，覆盖旧JE尚未失效而新JE已激活的重叠。按钮显示/possible和执行守卫各自完整；冷却、待回复、对象消失有稳定可读提示；效果预览与实际成本同源。

## 9. 证据边界与实施顺序

观察者收尾记录只证明冻结adfc317运行至1866.1.15、终档213403518字节与日志保存，主目录后修未加载；现有纪事主要针对CNE/USM/FRA/HUS。本轮未新增逐年小邦存档取样，也没有提取它们每年的财政/市场/动荡。因此不能声称“某土邦每年发展失败”或“南洋1866已普遍独立”；本方案依据源码结构和设定，不以虚构实测调平。[O01]

建议实施顺序：①先做43土邦与上述南洋名单的运行态国家/市场基线，读存档即可，不先开局；②做常驻生存JE和市场两分支，复用原生外交，先明确每个国家当前关系；③补旧政权自主路线与既有请求协议；④再接底层运动、人物及革命生命周期；⑤接统一/两司/宗主易主；⑥冻结候选后集中检查、仅对未证引擎语义安排定向测试。该顺序是未来实现计划，本轮未执行。

最低外部用例：合法性49/50/51；依赖0.8/1/1.2；宗主营数0；无港/内陆、市场owner缺失与同市场/不同市场；无合格人物；运动不存在/自然消散；协议超时+旧事件迟答；市场变更后同一月；旧JE新JE重叠；完成入口重复；六地区已有IR演员；起义生成失败；国家死亡/统一后重复回调。数值候选需要真实档基线与后续定向实测；不能把AST通过数等同玩法完成。

引擎待证：重叠附属历史的最终运行关系；市场pact变更与集团自动关系刷新时点；原生革命的身份/成果继承；国家死亡时JE及回调顺序；真实条约拒绝/改主与迟答；各国实际经济依赖值、适合阈值及经营持续月数。所有未证项保留，当前交付仅为方案。

## 10. 可反馈给技能的新知识

1. 1.13.11市场转换按实际拥有行为的数据库分路：属国市场权外交pact、集团identity/principle的关税同盟、join_power_bloc条约；不能把“贸易权利”或任意条约当作转市场。`join_power_bloc`不是`customs_union`同义词。
2. `economic_dependence`是country对目标country的有向指标，原生以1为分界且文档标注昂贵；不是比例库存，不宜所有国家每周遍历。具体0.8/1.2为本轮方案候选，不进入永久规则。
3. 政治运动`pop_support_factors`是UI清单，无实际玩法作用；真正变化来自pop_support_weight等。`character_ideologies`方向是运动向受压IG领袖施加思想，不是角色加入运动名单。
4. 参考MOD的修正名称/注释不足以证明行为：RAHF `ig_radicalized`实际改认可度/政治力量；`satsuma_military`实际键是运动导致激进化，并非注释中的SoL；country/state/state_region必须独立核scope。
5. 名单中“有国家定义”“开局有领土”“剧情生成TAG”“当前入口枚举”是四层：MYS与IR4、YN1与YU1、DEI当前名称尤其容易误判。历史重叠关系要读取运行态，不能以设定表覆盖真实overlord。

## 原始来源账

以下为本轮读取的原始路径、定位行和文件SHA-256。正文来源代号映射见下表；长文件列出与本结论相关起点，不宣称整文件所有分支均已审计。

|ID|Source and relevant lines|SHA-256|
|---|---|---|
|M01|nesnd_india_core.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt:1>) [L4](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt:4>) [L7](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt:7>) [L15](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt:15>)|`0622fab14d4db5208359b7d182fd76633926c28daa316487ac7f4fb718226548`|
|M02|nesnd_india_core.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_india_core.txt:1>) [L61](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_india_core.txt:61>)|`15d5f84faf514af67056797141f6aea867f10b80be35e37f18311d81bd1793d3`|
|M03|nesnd_india_uprising.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_uprising.txt:1>) [L4](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_uprising.txt:4>) [L117](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_uprising.txt:117>)|`812f719631b498b825a0b12e86eacb54b70209ff84c7e78a48f0f8e806583d82`|
|M04|nesnd_commissions.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commissions.txt:1>) [L3](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commissions.txt:3>) [L30](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commissions.txt:30>)|`de4dcb180455f8027bb36588bb96a0071ee303900ee52cc6740b027324dd6f83`|
|M04|nesnd_commission_expansion.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commission_expansion.txt:1>) [L17](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commission_expansion.txt:17>) [L30](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commission_expansion.txt:30>)|`6c0bde63e42d383a9c3d1de276e769e11c139c7c1274792ba9dede8419b6d1dd`|
|M05|nesnd_india_uprising.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/nesnd_india_uprising.txt:1>)|`46cf09a64853c217873f3270f329bffff79a63c48515d92e0089216e483fb4be`|
|M05|nesnd_commissions.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/nesnd_commissions.txt:1>)|`90ae174bc3ae3e52c02f109d6a690dbefe42a24a2a10103f926f8255d49b5e62`|
|M05|00_states.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:1>)|`a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`|
|M06|ce_subject_relationships.txt: [L27](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:27>) [L120](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:120>) [L175](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:175>)|`78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7`|
|M07|ce_00_countries_l_simp_chinese.yml: [L6](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_00_countries_l_simp_chinese.yml:6>) [L399](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_00_countries_l_simp_chinese.yml:399>) [L989](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_00_countries_l_simp_chinese.yml:989>) [L1001](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_00_countries_l_simp_chinese.yml:1001>)|`9475fd3a1943de06f95c608e3ff36a2bd5161c786cb767152a36e71496c0e24d`|
|M07|ce_countries_l_simp_chinese.yml: [L131](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_countries_l_simp_chinese.yml:131>)|`f1b759bf932dd6ca1cf7f572fee7781819151d615c3150839d75834de7d9fd15`|
|M08|00_subject_relationships.txt: [L223](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/00_subject_relationships.txt:223>) [L229](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/00_subject_relationships.txt:229>)|`618289bd6e7bd4e8fe5f3276249b6997f7a0c51cd2ab9f4f4f46289b9a02d59e`|
|M09|nesnd_india_diplomacy.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_diplomacy.txt:1>) [L35](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_diplomacy.txt:35>) [L71](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_diplomacy.txt:71>)|`4552ac3a8ae1dc6468ed00efc19b12a417e79c83ebd0b0919cca6d2a04d96e1b`|
|M10|nesnd_india_diplomacy.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:1>) [L20](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:20>) [L68](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:68>) [L73](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:73>) [L102](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:102>)|`8021ffc24d62850d79cdcbf0f155bf81ef88c3a7c651de610635a756c10326e9`|
|M11|nesnd_india_diplomacy.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_india_diplomacy.txt:1>) [L5](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_india_diplomacy.txt:5>)|`c8f0ef1043c908e940aa8624b0871786fbf12dfdbdce095284e70dc36323c8bd`|
|M12|nesnd_india_uprising.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_uprising.txt:1>) [L20](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_uprising.txt:20>) [L52](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_uprising.txt:52>) [L83](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_uprising.txt:83>) [L116](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_uprising.txt:116>)|`10c92917a3eef0c0f6a130359a031fee6b60dbf2715fc1584b4a55db341e05f8`|
|M13|nesnd_india_uprising.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_india_uprising.txt:1>) [L12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_india_uprising.txt:12>)|`280273a3342de3fed6562e6c2f56a9ca49ac338a592be5ef56980c6deba1ea40`|
|M13|nesnd_india_uprising.txt: [L1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_india_uprising.txt:1>) [L33](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_india_uprising.txt:33>)|`3d7d927ae0527a30b3f3d61a26bafa8538cad02e2884d4bdf0c155948d406106`|
|G01|42_subjects_request_market_control.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/42_subjects_request_market_control.txt:1>) [L14](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/42_subjects_request_market_control.txt:14>) [L48](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/42_subjects_request_market_control.txt:48>) [L81](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/42_subjects_request_market_control.txt:81>) [L166](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/42_subjects_request_market_control.txt:166>)|`88c081fb87846a98b78345fbda4e62e878184a08f161512a5c09baaab45699d1`|
|G02|36_subjects_grant_own_market.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/36_subjects_grant_own_market.txt:1>) [L18](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/36_subjects_grant_own_market.txt:18>) [L33](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/36_subjects_grant_own_market.txt:33>) [L67](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/36_subjects_grant_own_market.txt:67>)|`ad712dcfe896c0255eedf87ab979859c3e0702c56b8fc57370b7d61c71a076b3`|
|G03|09_join_power_bloc.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/09_join_power_bloc.txt:1>) [L22](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/09_join_power_bloc.txt:22>) [L55](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/09_join_power_bloc.txt:55>)|`9178a5b409a33634b557420b8730b01bf4f73991b23ad868602dc3aa22d63223`|
|G04|00_power_bloc_identities.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/power_bloc_identities/00_power_bloc_identities.txt:1>)|`3979e78c666d681a749a42bdf95e4eaf787b9709163cd6475b16d075476afe9b`|
|G05|00_power_bloc_principles.txt: [L179](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/power_bloc_principles/00_power_bloc_principles.txt:179>) [L199](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/power_bloc_principles/00_power_bloc_principles.txt:199>)|`98f9100cadcbb9d379ec356f8f73e168d3b3c332ed356882b8bd597144b66368`|
|G06|21_no_tariffs.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/21_no_tariffs.txt:1>)|`da75161d172cba02438fe6f48eb72acbfdb15b92ed60c15349d287325ce35de8`|
|G06|25_trade_privilege.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/25_trade_privilege.txt:1>)|`175370234bc4b186929b9ad24acfc7b0632dd954c026366fb5e9eda1b9068389`|
|G06|24_transit_rights.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/24_transit_rights.txt:1>)|`c5166e2c8d59337d7717ea103b36d8d8de5e00abe428bdbc67fc62bfb9c171dd`|
|G06|07_foreign_investment_rights.txt: [L1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/07_foreign_investment_rights.txt:1>)|`d1e4b58b2bdd5bf931e02b65ed89d4c8ef952611eef6558852af8360fdc20bf1`|
|G07|political_movements.md: [L8](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md:8>) [L48](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md:48>) [L78](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md:78>) [L94](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md:94>)|`4842b165656f0741cc0baad97b2d82836f9097f64ce5b43ca4559c9d733e22c6`|
|G08|00_ideological_movements.txt: [L4603](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt:4603>) [L5055](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt:5055>) [L5151](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt:5151>) [L5229](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt:5229>)|`834a1b97f09c65b9b64eafdaffe4ee68965aaac262066140793a482eefd23a6b`|
|R01|metadata.json: [L2](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/.metadata/metadata.json:2>) [L4](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/.metadata/metadata.json:4>)|`70df3daa373aae9c9ccf915b1b2b6f339e9264747c39eb6322cff2b219a06526`|
|R02|dsk_je_jap.txt: [L3](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:3>) [L69](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:69>) [L101](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:101>) [L154](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:154>) [L296](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:296>) [L632](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:632>)|`21b6d1e939a8713562ba3365ab5de6d68e5c5b7a55d6a1dbd5580cc9e61196ac`|
|R03|open_japan_events.txt: [L2](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:2>) [L195](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:195>) [L367](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:367>) [L432](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:432>) [L459](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:459>) [L497](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:497>) [L606](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:606>) [L652](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:652>)|`0dc7b4cbd2a576dabdcb7472a52441ad820f36a4d0cfbefba21da8ea5d54b455`|
|R04|dsk_usa_modifiers.txt: [L3897](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/dsk_usa_modifiers.txt:3897>) [L3903](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/dsk_usa_modifiers.txt:3903>) [L3917](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/dsk_usa_modifiers.txt:3917>)|`b564ea3dfcfa7a880bf2f4ede9768a14db79ebb7079effb953088954b990fe4c`|
|R05|sino_events.txt: [L1590](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/sino_events.txt:1590>) [L1617](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/sino_events.txt:1617>) [L1640](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/sino_events.txt:1640>) [L1668](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/sino_events.txt:1668>) [L1733](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/sino_events.txt:1733>)|`b7e986c567428e35a4a05cb109d1ce9b0902f66b9f295151a1d58b6201263798`|
|R06|replace_historical_leaders_europe.txt: [L5130](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/character_templates/replace_historical_leaders_europe.txt:5130>)|`3eb13c628814b8b57f78b43da03a4a18decf43ece60145ed34dff0ffd60660f5`|
|E01|triggers.log: [L9699](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:9699>)|`ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`|
|E02|effects.log: [L365](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:365>) [L380](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:380>) [L996](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:996>)|`24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`|
|O01|finish-and-bugs.md: [L3](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/finish-and-bugs.md:3>) [L19](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/observer-finish-20261103/finish-and-bugs.md:19>)|`002b066003474152ff14de57db822a5ce3e6015436b40b703af335c8080841a4`|
|C01|北明ppet.txt: [L362](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:362>) [L379](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:379>) [L387](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:387>) [L389](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:389>)|`227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`|
