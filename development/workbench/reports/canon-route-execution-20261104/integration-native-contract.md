# 地区路线实施契约：原设定、实际对象与1.13.11原生接口

2026-11-04。本报告为当前实现批次的只读来源映射，**不是MOD实现，也不是引擎验收**。未打开游戏，未改主MOD。用户已要求把先前升级方案真正实施；本契约供执行代理直接落脚本，不能以保存本文件代替该工作。

读取NESND与工程适配、既有两份升级方案后，运行catalog.py status：**1.13.11 / Steam build 24799966 / CURRENT / changed_count=0**。PPET原件SHA256本轮复核为`b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`，与逐页缓存来源相同。本报告用PPET原页号，不把其唯一未来线强制为当前存档事实。

根路径：M=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`；G=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`；W=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。正文简写为源码定位；末节给出可点击原始文件。

## 1. 必须立即改正的接口与设定判断

1. **坦志麦特的`sick_man_complete`不是成功标记。** G/events/sick_man_events.txt:93和:196分别在成功、失败事件中设置它。G/common/journal_entries/00_sick_man.txt:10–20只在原生目标完成时调用`.2`，当前值是`:79`的`var:sick_man_var`，目标加值4；原生超时调用`.3`。当前M/common/scripted_triggers/nesnd_regional_development.txt:16只查complete，因此会放失败者入新链。最低安全成功资格应为complete且保留的`sick_man_var >= 4`，或在明确原生成功hook写永久专属成功标记。`failed_tanzimat`会20年过期，单靠它排除失败不够；`failed_sick_man_main`受DLC分支控制，也不能作唯一证明。本轮对G全部.txt检索sick_man_var，写入仅初始事件及原生子日志增量，未见删除；实施时仍核MOD是否覆盖这些写入者。
2. **莱茵邦联TAG是FRM。** M/common/dynamic_country_names/ce_dynamic_country_names.txt:750以现实对法关系显示北莱茵邦联/莱茵联合省。不能用RHI/RHN，也不能把统一前所有德意志邦国都当独立盟友。
3. **外交结盟是条约，不是旧alliance pact。** G/common/treaty_articles/00_alliance.txt定义`alliance`；G/events/soi_events/00_ep1_caucasus_events.txt:774–790给出`create_treaty`、`is_draft=no`、5年约束及互惠alliance条款实例。新内容先`can_create_treaty`，接受后执行，再验证真实条约才计成果。
4. **参战接口是DP scope的`add_initiator_backers`/`add_target_backers`。** 原版意大利事件先找真实RSM博弈、保存scope，再给玩家加入目标方：G/events/italian_unification.txt:644–674。不存在已核实的`join_diplomatic_play`。外交承诺必须绑定明确博弈与阵营，不按“有战争”随意参战。
5. **军用品消耗量与花费不同。** `country_military_goods_cost_mult`明确是货币成本（G/localization/english/modifiers_l_english.yml:72–73）。本次要数量，使用`unit_supply_consumption_mult=-0.20`；实际国家作用域实例是G/events/brazil/paraguay.txt:509–516→G/common/static_modifiers/brazil_2_modifiers.txt:314–317。其按钮预览却把修正放在兵营，不能把预览scope误认实际执行scope。引擎说明是维护军事单位所需商品，未查到army专属supply键；不擅称它已证明严格排除所有海军补给。
6. **人物可以是真实非领袖politician。** G/common/character_templates/country_arg.txt:146–172使用`role=character_role_politician`；无需`ig_leader=yes`。G/common/character_roles/00_auto_assigned_roles.txt:188规定政客角色、5–10年career、人物池；因此18名候选都能成为实有人物而不挤掉佩佩、郭庆达或现任南朝领袖。女性公共人物优先合法agitator或具名事件身份，政治任职另查当前资格；创建agitator前检查本国empty_agitator_slots >= 1（引擎triggers.log:9720），无槽时保留具名叙事，议程照常。

## 2. PPET给出的冲突，和本轮应该实现的行为

|国家/对象|原始作者依据|本轮可执行的核心冲突；不强迫原稿未来|
|---|---|---|
|PRU、FRM与FRA|PPET24 p14、27–28：俾斯麦先作莱茵外交官，后入普鲁士；普奥战争与莱茵战争使普鲁士逼近法国，法国经济危机削弱干预；25 p18：法国镇压法兰克福公社与统一派|普鲁士争取实际德意志诸邦的反法协作，法国/FRM既有宗属是阻力；由现实条约、脱离宗属、对法博弈和统一结果兑现，不用铁路两站代替外交路线。不强制1866战争或俾斯麦跳槽|
|AUS与意大利|PPET23 p11、16：法国扶植共和国及奥地利败于法国；26 p5、9、13–14：后世大陆秩序、反法联盟及威尼托以东保护国|奥地利对意大利统一有可参与的干涉窗口：保护小邦/维持多国秩序，或与实际统一者议价承认；法国支持LOM并非天然反统一。奥地利国内民族问题继续由原生链负责|
|TUR、QE1、PER|PPET21 p19–23、22 p22、24、28：秦扩张与唐衣大食；奥斯曼为伊斯兰联军领袖，第四近西战争遏止秦俄；24 p18后来又有秦土法合作|按用户最新设定：原生坦志麦特成功后，出现0–100扩张热情、逐州花费制造宣称与12月仿秦军改。秦式军改是可借鉴制度，不等于永远反秦；军队政治势力和财政效率有真实交换|
|EGY|PPET26 p13–18仅对1918以后埃及、哈希姆与列强争夺叙利亚/巴勒斯坦给出详细未来|现有埃及王朝、自主和亚洲领土是当前冲突；不能按未来结局在1836生成哈希姆王朝。独立EGY的实际亚洲州是TUR潜在宣称对象；依附关系必须实时读|
|LOM/ITA|PPET23 p11：1802法国支持意大利共和国；p13意大利执政与法国皇帝互通；M已有佩佩总统、军队领袖与将军|法国支持的共和整合是主路线之一。国内财政/学校与统一协议同时有内容；小邦、教宗、南方能谈地方税款和制度。亲法与支持统一分别判定|
|HUS|PPET18 p12–19：奴隶独立起源，坞堡主/士绅/八旗军头共和；p20–24东进、油业、对美战争、对原住民与蒙古牧民的先扶植后镇压；p25–28对吴民族运动与后世战争|东青行—债权—公民资格，东进与牧地通道，跨洋市场与资本，对吴民族运动立场，油业及大陆外交。共和拥有债务奴隶制度是现存矛盾；不套美国开国、不按1919自动并入USA|
|MEX|PPET18 p18、23：阿兹特克王朝复国与HUS扶植墨西哥共和国；22 p32–34：美洲列强互动|依据现时共和国/王朝、HUS与USM关系塑造内政和边疆外交。PPET对1836墨西哥内部具体制度细节较少，不能把现实Santa Anna史线装成作者既有设定|
|USA|PPET18 p21–24及24 p24：与东洲/牧民的北美战争；林肯废奴战争中FRA/HUS反而支持奴隶主叛军|废奴、联邦重建及外部干涉三者相接；根据实际奴隶法与真实内战判定，不能先认定废奴成功，再只给大学/铁路奖励|
|PEU印加|PPET19 p18–34：儒教上层、尤潘基改革、拉普拉塔战争、外国银行矿业资本、共和与公社、复辟|矿业收入与地方社会、外资与皇室/共和派、沿海交通与真实战争。PEU不是波斯PER。主00_states无PEU：当前开局NPU/SPU与后期形成PEU须分别观察，不凭名称假设存活|
|USM及明廷继承国|PPET27 p7–20，叠加用户最新制度说明（后者优先）|明存、吴代、长期停战三入口；礼议院与考试资格、沿海实业与内陆学额、军费和省际分配。现有西部置省1850期限与失败后果保留；学政不是布政使，不新增上院|
|印度/南洋|PPET24 p19：吴吞地引章西起义；25 p4、12、14：莫卧儿饥荒与村社阿里、列强镇压及印度势力分割|小国经济生存→实际市场选择→地方组织→旧政权自主或底层改革/革命→独立后重订关系。国内革命、对外独立、离开市场分别结算；不能所有国家共用一次建筑打卡|

PPET文本原文定位见[逐页缓存](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:174>)。日期均为作者某条未来线，不是强制排程。

## 3. 现存演员与地域清单

### 德意志与意大利

德意志候选建议用存活、持地、主文化north_german/south_german及现实独立/宗属资格筛选，原生G/common/journal_entries/00_german_unification.txt:8–30已有文化资格。显式重要对象：PRU、FRM、SAX、BAV、HAN、WUR、BAD、HES、HEK、NAS、WLD、LIP、AUS；小邦是否独立不由这张表保证。FRM的附属历史为WUR/HEK/HES/NAS/WLD/LIP/BAD（WUR重复声明不要把两条当两个盟友），FRA另有SAX贡属。对FRM附属先支持自主/同一具体对法博弈，不绕过原生外交权限强塞alliance。

M/common/history/states/00_states.txt当前直接持有：FRM＝WESTPHALIA、RHINELAND部分、NORTH_RHINE、RUHR、HESSE部分；PRU＝POMERANIA、POSEN、ANHALT、WEST_PRUSSIA、EAST_PRUSSIA、RHINELAND部分、LOWER_SILESIA、UPPER_SILESIA、BRANDENBURG、BRUNSWICK部分。州区内部可多人所有，宣称和“完全控制”分别判定。

意大利主演员LOM、SAR、SIC、PAP、PAR、MOD、TUS及原生形成的ITA；外部FRA、AUS。M外交：FRA保护LOM与SAR；LOM傀儡PAR/MOD/TUS。LOM现持LOMBARDY、PIEDMONT、VENETIA、ROMAGNA。意大利统一依旧走原生country_formation，成功后凭国家连续身份和实际领土保留阶段，不写“LOM不存在=统一失败”。

### TUR候选宣称地域

直接复用M/common/strategic_regions/west_south_asia_strategic_regions.txt，以下前缀均为STATE_：

- 近东：HUDAVENDIGAR AYDIN KONYA ANKARA ADANA KASTAMONU CYPRUS DIYARBAKIR TRABZON EAST_AEGEAN_ISLANDS ERZURUM KARS TRANSJORDAN PALESTINE LEBANON SYRIA ALEPPO DEIR_EZ_ZOR BAGHDAD BASRA MOSUL。
- 阿拉伯：OMAN ABU_DHABI YEMEN HEDJAZ HAIL NEJD。
- 大波斯：BALUCHISTAN GREATER_CAUCASUS ARMENIA AZERBAIJAN ELIZAVETPOL KHORASAN ISFAHAN MAZANDARAN IRAKAJEMI LARISTAN FARS SISTAN KHUZESTAN TABRIZ URMIA PERSIAN_KURDISTAN LURISTAN KANDAHAR KABUL PASHTUNISTAN NORTHERN_BALUCHISTAN CENTRAL_HIGHLANDS QUETTA BALKH HERAT KERMAN SEMNAN。
- 中亚：UZBEKIA KHIVA TAJIKISTAN KIRGHIZIA TURKMENIA SEMIRECHE AKMOLINSK AKTOBE SYRDARYA FERGANA MERZ DZUNGARIA TIANSHAN URALSK JETISY ILI WESTERN_TIANSHAN。
- 独立EGY实际亚洲州：实时检查owner=EGY、EGY.is_subject=no、亚洲范围；当前历史包括ADANA、ALEPPO、SYRIA、LEBANON、PALESTINE、TRANSJORDAN和**SINAI**。SINAI在地理亚洲口径有边界风险，按用户“埃及亚洲州”的明确含义单列，别漏掉；CRETE与埃及本土不属此分支。

目标必须尚未完全归TUR/其被排除的自己阵营、无TUR宣称、仍有适格外国owner-state；显示和执行用同一个具体州。EGY若仍为附属，不能从通用近东路径绕过“独立EGY”限制。每州分别扣热情，绝不能一个按钮买整个战略区；没有目标不扣款。新增拆州已列入，不能用旧原版名单漏掉ILI/JETISY/WESTERN_TIANSHAN。

### HUS与南朝

HUS当前有21州区份额：ALASKA WASHINGTON OREGON IDAHO COLORADO WYOMING MONTANA NORTH_DAKOTA NEBRASKA KANSAS YUKON_TERRITORY BRITISH_COLUMBIA NEVADA ARIZONA NEW_MEXICO CALIFORNIA SONORA UTAH BAJA_CALIFORNIA SOUTH_DAYUAN NORTH_DAYUAN。大平原并非“尚无东洲人”的空白区。蒙古POP在M/common/history/pops/05_north_america.txt:165、296、347等实际存在；巴彦图可用现有`mongol`文化，家园/活动州从当前实际持有、当地POP筛选，不能让他代表全部原住民。

HUS主文化实际为ce_liaodong、ce_wuu、hakka、manchu（M/common/country_definitions/ce_countries.txt:35）。USM主文化ce_wuu/min。西秦是QE1，唐衣大食是PER。南朝事件入口在实际USM或持有`nesnd_ming_court`的存活继承国；不能仅看动态国名。

### 印度与南洋

印度直接复用`nesnd_india_prince`的43TAG：ALW ASM AWA BAG BAS BER BHO BHV BHW BIK BUN COC COO DHA GAR GWA HYD IDA IND JAI JAS JEY JHN JOD JUN KHP KNO KOT KUT MEW MNP MYB NAG NAR NAW PAN PLP PTA PTN SAT SIN SUR TRA；另接`nesnd_india_local_state`，仍要原trigger要求的存活、持有有POP印度州、非分散国家。MUG/BHT/DRA为帝国，不混入小国尺度。IR1–IR6为既有地区起义演员，不能用作小国国内革命的通用新tag。MYS无开局持地证据，IR4不等于开局MYS。

南洋主小国：ACE BAL BRU BLG LAN JMB SAK SRK YOG BNJ KTI TID PON SEL PRK SMB STG JOH MGD SUL LUA CMI CHP CAM；区域中介/较大国：PHI DEI YN1 BUR SIA DAI。YN1是远南，YU1是南非远山。对所有国家读当前overlord/market.owner；M的ce_subject_relationships和00_subject_relationships对CAM/CHP/CMI/LUA有重叠历史，不能按文件先后推断运行态。

## 4. 可直接落库的最小完整链条

下列“最小”是每条都拥有实际冲突、玩家行动和后果的完整闭包，不是少造几个JE。建议每国主议程常驻、最多两条阶段子JE活跃；经济成就自然确认，不让玩家重复点领取进度。

|链|开启与过程|结算及后继|实际接口|
|---|---|---|---|
|PRU 德意志反法协作|PRU/其连续形成国拥有相关实力与外交资格；选一个实际德国对象，向其提出明确联盟、支持自主或对法协作；被法国/FRM控制者有拒绝/独立约束|联盟真实成立记盟友；被支持国真正独立记自主成果；对法博弈加入成功记本轮参战。任一项不是泛用“外交点”；失盟暂停合作、保留历史，不重复发首盟奖|alliance/defensive_pact条约、现有请求nonce与45/90日期限框架、真实DP backer；G德国统一结果继续有效|
|AUS 意大利干涉|一个实际意大利统一/兼并争端出现；法国已承诺对象与自身利益可见；奥地利可保护受威胁小邦、介入真实博弈，或有代价承认统一|保存本次target和DP；依据战后实际独立/归属结算，白和不等于奥方胜利。失败留下意大利影响力/军费政治后果，冷却后遇新争端可再来|DP双方守卫、条约保护；不创建与现有博弈重复的战争，不在别人已经消失的DP加人|
|TUR 扩张热情|仅原生坦志麦特成功；0–100资源，单一月度写入。军方强势/战争准备等具名增长来源，12月仿秦军改降低增长；逐州选有效目标花费宣称|声明实际添加后才扣热情；不强送战争/州。改tag/亡国/不再适格清临时军改，永久宣称按原生保留；0不能消费、100截顶，反复点同一州不能扣费或获奖|state_region.add_claim=root；unit_supply_consumption_mult、army offense/defense、armed_forces attraction/pol_str；变量值与原生bar同源|
|LOM/意大利 I-A→I-B|开局共和国和各邦地区产业/学校议程；工程的融资对象不同，法国关系可支持但不自动否定发展；选择真实协商邦国，明确税款/军队/学校保障|完成实际项目后开协商；协商同意不直接吞并，落现实条约/统一支持并由原生统一入口推进。法国改制重验个人担保和现实条约，不抹厂房|原生ITA形成与italian_unification事件；项目实际building occupancy/profit；PAP/SIC有自己的协商结果|
|意大利 I-C统一/多国秩序|统一形成后处理新辖地区代表/财政/军制；未统一但多邦协定真实成立也可达稳定多国终局|学校/地方税款/劳动争议继续，人物死亡不关JE。强制集权能引地方反对，有地方保障的统一也有预算代价|实际owner-state，州/IG限时修正，法律观察；严禁凭统一flag吞所有意大利国家|
|HUS H-A通洋/大陆工商|东青行与现有railways科技已存在；实业发展从现有岗位/运输及真实公司进入。通洋关注港口/进口/亚洲联系，大陆关注铁路/土地/内陆产业|完成一个实有经营成果后进入公民/边疆，保留另一经济方向后续可转。共同市场、投资与对吴态度分开记|company_ce_daqing_coop；实际market.owner，原生集团退出/市场权。科技railways不能再作“尚未发明”的门槛|
|HUS H-B边疆与债务劳工|实际受影响本国州或真实邻国；保牧地通道、补偿开发、强制驻军有不同代价。债务奴隶法存在才叫废债务奴役|协定实际关系成立或本国州受约束才记完成；废奴后改谈文化/资格/结社，不能持续宣称仍在废奴。强制路线能战败和失地|实际债务奴隶法与原生立法，地方有限期修正/IG反馈；不把人物签名当整国吞并授权|
|HUS H-C→H-D|铁路/机械就业形成后出现公开投资、公民资格；pumpjacks+实际油井+就业运输后才进入油业|特许扩张、地方保留收益、监督和改革具有不同政治承担；对美墨/对吴干涉从实际战争与关系进入；油业失败保留学校港口|公司实际条件；原生外交/投资，不创建采购库存；不按1861/1919自动战争与并国|
|USM U-A战后礼法|无活跃同一明吴对抗，读取明存/吴代/长期停战三个事实；只算本国实辖；吴代读取已存在西部置省进行/成功/失败|礼法方案分别落考试资格叙事身份和现行法律，不假造议院席位数据库；西府独立时以外交交流处理|`tag_WUU_var`、`nesnd_ming_court`、global usm_civilwar_status_quo/nesnd_south_settled；政治授权相关IG执政+合法性50|
|USM U-B双线|书院/实学/地方学额与工场/船业/内河运输可并行。段敬川先教习，资格改革后才称学政；罗映棠教育活动不越过妇女任官法|学校和产业以实际建筑/制度为主要收益；日本同市场时可协作，离开只去掉关系依赖修正|共享市场现货与就业；现行西部置省结果仅读取，不能重罚0.25或改1850期限|
|USM U-C分配|沿海资本、实际工业就业、跨省工程进入商业集中/省际均衡/学政改革|真实预算让利、IG和地方后果；失利可再谈与缓解，但不清历史失败。人物退出留下组织，学校不随死亡消失|一次限时政策修正、真实法律/投资；不要新增“南府自治=各省自治”概念|
|小国 S1生存→S2市场|全名单按港口/内陆、行业资源/岗位和现实市场选profile；连续3月经营/财政可维持开后继；可依市场供给，不要求军工全套|借现市场与取得自己市场两路都可达；独立市场分支必须观察market.owner真正变成本国|原生request_market_control/grant_own_market；有条件集团加入、跨市场贸易权各自独立|
|小国 S3地方能力→S4政治|尺度合适的行政/学校/军官能力进入旧精英自主或底层议题。旧精英政治动作合法性50；底层运动不能要求先入政府|自治请求/独立事实和国内法律/革命事实分别结算；革命胜利仍可能属国，独立后仍可能寡头|既有nesnd_india_diplomacy请求协议、原生movement与革命；不复用IR案件造第二次同地起义|
|小国 S5独立后秩序|实际独立后的新税负、投资与安全关系；可选择留市场、贸易伙伴、区域防御或明确同意加入统一国家|条约落实才发一次有限收益；失败、易主、统一保留实际资产，国家灭亡允许GAME OVER，不自动救援|现实overlord、treaty、market；真实吞并后仅迁移可继承经济结果，政治主权奖励不复制|

## 5. 十八名人物的实际模板与进入角色

以下ID/文化/职能是实施用提案映射，名字、职业、出生年及窗口来自已要求实施的升级计划，不冒充PPET既有人物。生日只确定年：为引擎固定birth_date需要统一采用1月1日作技术占位并在来源账注明，不在玩家文案假装准确生日。**不使用固定age=30**；有出生日期才能避免旧档刷年轻人。每个阶段最多新进入一名实际政治候选；剧情组织可以先有文本。`role=character_role_politician`不等于IG领袖；明确军事岗位的Sereni才用general。表中geo为出生/活动定位，不是无条件跨国抢人许可。

|唯一template建议|姓名/出生|文化、home_region建议|实际初始角色与IG/思想|进入条件与主要议题|
|---|---|---|---|---|
|nesnd_ita_valdieri|乔万尼·瓦尔迪耶里，1798|north_italian；PIEDMONT|politician，industrialists；ideology_market_liberal|1836–1855；实际工具/军工就业+融资争议；预算担保，具体毁约才反法|
|nesnd_ita_bellandi|特蕾莎·贝兰迪，1807|north_italian；ROMAGNA|female agitator，intelligentsia；ideology_radical（共和且公民资格运动需适格）|1840–1862；教育/出版和资格议题，女校及报馆；镇压可流亡|
|nesnd_ita_rusciani|马泰奥·鲁夏尼，1794|south_italian；CAMPANIA|politician，petty_bourgeoisie；ideology_moderate|1836–1855；SIC或实际持有南方的国家，土地/矿权/地方财权；不能从LOM无条件召南方代表|
|nesnd_ita_sereni|卢卡·塞雷尼，1819|north_italian；LOMBARDY|politician，armed_forces；ideology_republican_leader；确有军职才add general|1844–1874；战争军费或军制整合/工程学校；欠饷与统一指挥|
|nesnd_ita_vitali|保罗·维塔利，1811|south_italian；LAZIO|politician，devout；ideology_moderate|1840–1865；PAP教育财政或取得教宗旧地后的学校安排；不得升教宗|
|nesnd_ita_martelli|罗莎·马尔泰利，1833|south_italian；SICILY|female agitator，trade_unions；ideology_social_democrat，需社会主义/劳动运动资格|1858–1888；真实矿业就业与劳动问题；不预造1836工会领袖|
|nesnd_hus_tong|佟世衡，1790|manchu；WASHINGTON|politician，industrialists；ideology_market_liberal/传统债权立场|1836–1852；东青行/铁路承包；公司不存在改投资者叙事，不写虚假董事|
|nesnd_hus_shen|沈季川，1798|ce_wuu；SOUTH_DAYUAN|politician或有适格运动时agitator，intelligentsia；ideology_abolitionist|1836–1860；债务劳工与资格冲突；废奴后个人议题转公民资格，不重复要求废奴|
|nesnd_hus_bayant|巴彦图，1806|mongol；活动州由当前蒙古POP与建设筛选，候选NORTH_DAYUAN/MONTANA|politician，rural_folk；ideology_moderate|1840–1866；实际牧地通道被工程影响；不是全体殷人/蒙古唯一代表|
|nesnd_hus_lin|林素岚，1816|hakka；CALIFORNIA|female agitator/事件公共人物，intelligentsia；ideology_abolitionist|1842–1872；纺织移民与识字/债务劳动议题；任官另重验法律|
|nesnd_hus_lu|陆景铎，1824|ce_wuu；CALIFORNIA|politician，intelligentsia；ideology_moderate|1849–1879；铁路工具/机械就业、公开投资争议；固定知识分子，不因工程师自动赋大股东|
|nesnd_hus_guan|关廷宪，1840|manchu；WASHINGTON|politician，petty_bourgeoisie；ideology_moderate|1865–1895；真实油业矿权与预算；技术未到等待，不能按日期生成油井|
|nesnd_usm_ji|季文衡，1796|ce_wuu；ZHEJIANG|politician，industrialists；ideology_moderate|危机结算后至1858；现辖浙江或真实沿海利益；既有考试合格身份=事件变量，不是新增上院角色|
|nesnd_usm_duan|段敬川，1800|ce_sichuan；SICHUAN|politician，intelligentsia；ideology_moderate|1840–1862；本国控制巴蜀或与独立西府交流；先教习，合格事件后学政；全球只有一人|
|nesnd_usm_xu|许廷璋，1788|ce_wuu；JIANGSU（M/map_data/state_regions/11_east_asia.txt:772已核）|politician，landowners；ideology_traditionalist|1836–1850礼法资格议题；反任意征敛与反过快扩资格并存|
|nesnd_usm_luo|罗映棠，1814|min；FUJIAN|female agitator/事件公共人物，petty_bourgeoisie；ideology_moderate|1840–1870；纺织船业劳动教育；当前无妇女权利不直接任学政或领袖|
|nesnd_usm_han|韩士铎，1822|ce_chu；XIANGYANG|politician或适格agitator，trade_unions；ideology_moderate→明确劳动议题后社会思想|1848–1878；真实内陆工业/技能学校；边缘工会不强造政府势力|
|nesnd_usm_jiang|蒋绍衡，1834|ce_wuu；ZHEJIANG|politician，intelligentsia；ideology_moderate|1860–1890；资本集中/跨省工程与预算；不附会皇族或自动掌六部|

表内完整ideology键均已核M/common/ideologies/01_character_ideologies.txt：moderate:9、traditionalist:126、republican_leader:852、radical:1176、abolitionist:2197、social_democrat:3274、market_liberal:5999。人物共和主义用ideology_republican_leader，不能误用IG层ideology_republican。无需新建18套意识形态。文化、region字段指“人物身份”，不改变POP或国家主文化。没有实际人物槽时不要给固定IG领袖；角色池与组织叙事足够承载国家行动。

### 一次生成、流亡、退休与死亡的闭包

G引擎triggers.log:100明确`any_character`为**全球**人物迭代，不需要每国遍历；同文件:106有流亡池，:112有void。最低创建算法：

1. 先检查全球`any_character={ has_template=... is_character_alive=yes }`并保存符合归属的人；流亡池另查。本人在外国时只进入访问/正式邀请，不抢转；流亡邀请成功才`transfer_character=root`，原生实例见G/events/agitators_events/garibaldi_events.txt:185–198。
2. 若全球永久`nesnd_seen_<id>`存在，且未找到活人，不再创建。同一模板on_created立即写永久seen并设置人物身份变量；这是终身防重建锁，不在死亡时删。先确认create成功/on_created再写，别在create之前锁死。
3. 新模板只保留一个生成通道：本批故事create负责，先不同时加自然`agitator_usage`/leader_usage；这样不会自然生成和剧情生成抢跑。未来要加自然池，也必须共用seen资格。
4. 在on_character_death追加独立hook，匹配模板后写`nesnd_dead_<id>`、清个人担保/请求，不删除seen。G/common/on_actions/00_code_on_actions.txt:2604为root=Character，:2704加里波第清alive、:2715 Espartero写dead可作实例；本批用后者的永久终态思想。
5. politican角色默认career5–10年。自然退休可能落void或无role；seen仍阻止复活。月度只在需要本人事件时重查alive/owner/role，不保存长期悬空character scope。特定退隐可`remove_character_role`并写retired；组织议题不随个人结束。角色可活着但无公共职权，不能一概“死亡”。
6. 人物归国、国家形成和政体变化复用同一对象；角色死亡不让建设自动成功、不把职位自动给虚构儿子。文案提供组织版兜底，延迟事件显示和option执行都重验。

已有Pepe/Mazzini/Garibaldi不计18人。G自然Douglass模板存在；若实现历史访客先全球复用/事件访问，不另造HUS模板。G模板1817.2.14与研究史料1818的差异保留，不借机改游戏出生日期。最小本批可以先完成18名虚构池，历史访问者另按既有方案择优接，不靠强刷名人填内容。

## 6. 市场、投资、IG与运动：完整数据库链

|功能|已核原生链与执行语义|实现边界|
|---|---|---|
|自建市场|G/common/diplomatic_actions/42_subjects_request_market_control.txt→pact `market_owner=first_country`；36_subjects_grant_own_market.txt→`market_owner=second_country`|新增JE观察owner；剧情可引导原生外交。不能直接create pact就假称经过原生审批；liberty desire、现实直接宗属、冷却需保持|
|加入共同市场|09_join_power_bloc条约→join_power_bloc；00_power_bloc_identities中trade_league与market_unification原则提供customs union|没有customs_union treaty article；不是每个集团都共享市场。HUS离开贸易联盟的真实资格由原生UI/trigger决定，不仅删一个原则|
|跨市场合作|no_tariffs、trade_privilege、transit_rights、foreign_investment_rights各自条约|这些不是改变市场owner；小国不一键随意转入第三国市场|
|法国/海外投资|07_foreign_investment_rights：directed，source/target方向、stock_exchange、DLC、原生利益要求与重复检查；实际treaty flags给投资权|允许投资≠立刻落厂、就业或某商人持有公司；完成条件观察真实owned building/occupancy，建设本身由原生进行。不用免费create_building掩盖融资过程|
|本国预算/援助|已有M/nesnd_india_diplomacy真实报价`net_fixed_income*4`并25k–125k钳制，接受后add_treasury成对执行|小邦不能原封继承大国固定25k下限；每次报价冻结且收付同源。若无可靠财政基线，选确定限时财政修正并明确单位，别假称收入百分比|
|公司|M/ce_companies_china现有东青行/福海行→building_types/extension/possible/prosperity_modifier；G油公司以pumpjacks+实际油井等级为条件|公司身份、个人executive/magnate、国家投资权三层不同。佟是董事叙事不自动占原生CEO，若任职应另核company角色接口|
|政治门槛|G/common/journal_entries/00_liberalism.txt:54相关IG政府与合法性50→事件；经济子目标直接检查建筑就业|常规政治动作只相关IG执政+合法性50，不额外派系排列/同党/党魁/人数/长期65合法性；经济经营不绑50，底层运动不绑政府|
|运动|political_movements.md:48 character_support_trigger/weight；:78 pop_support_factors仅UI；:83 pop_support_weight真实支持；character_ideologies向受压IG领袖传播|不能只改UI列表声称支持增长；不能将人物set_ideology误称加入某运动。优先现有movement_anti_slavery/movement_liberal/movement_radical/movement_labor等实际定义，先满足creation_trigger与角色支持资格|
|地方效果|state内add_radicals_in_state；country内add_radicals可按文化/职业定向，原生modifier的state_movement等语义逐键核|不要在state_region直接用country效果；目标是实际owner-state，失地后不继续给外国州本国工程补贴|

## 7. TUR数值和按钮的精确闭包

已授权固定项：热情0–100；逐州宣称成本；秦式军改12月、降低热情增长、军用品数量−20%、军队IG吸引与政治力量各+0.15、攻击防御各+0.10。用户未指定每州成本与月基础增长，执行代理可取单独script_values，说明是平衡选值；所有入口引用同一值，禁止多个JE叠加增长。

修正推荐字段（都是本机实际存在键）：

```text
unit_supply_consumption_mult = -0.20
interest_group_ig_armed_forces_pop_attraction_mult = 0.15
interest_group_ig_armed_forces_pol_str_mult = 0.15
unit_army_offense_mult = 0.10
unit_army_defense_mult = 0.10
```

来源分别见第1节以及G/common/modifier_type_definitions/00_modifier_types.txt:1、825、3393、3410、3499；军队特化offense/defense有公司繁荣和国家static实例，因此避免额外提升海军。0.15是乘数15%，不是IG势力增加15个百分点；攻防是乘数10%。12月军改期间不允许叠加，再次开启必须等结束；停止增长不是清空热情。修改UI原生bar明细要展示基础增长与军改减速，不在描述重复公式。

逐州按钮可采用固定有限州列表配合“当前候选→下一目标→确认”或原生已核状态选择入口；本轮未发现通用`selected_state`按钮API，不发明动态下拉。若采用候选循环，预览显示当前真实州名；执行时重验该州、拥有者/EGY独立、已有claim与热情。只有`add_claim`实际成立后扣成本及登记。本国已有claim/全持有/目标消失不扣。不能一个random_state预览、另一个random_state执行。

## 8. 共用生命周期与必要外部用例

新增内容至少有：eligible→active→temporarily_paused→success/failed/invalid；success与奖励领取分开。国家依旧存在时失去短期财政/合法性/市场只暂停相应行动；不删工厂、永久资格、已做工作。被吞并国家取消个人担保与待答；国家形成同对象继承进度，真正新国家只能迁移明确允许的经济成果，不复制政治主权奖。

请求保存发送者、接收者、双方现实宗主/身份、议题、nonce、截止日。回复先重验，再实际执行；实际条约/参战/领土变化确认后结算。拒绝/过期/目标改变清同nonce锁，旧事件不得清新请求。玩家可拒绝，不以某人死/国家灭亡永久等待。战争结算只处理绑定DP，不能以后无关战争误发奖。

必要静态/模型用例：坦志麦特success/failure都带complete；四项成功阈值3/4；TUR热情0、cost−1、cost、100、重复claim、EGY独立→附属；法/奥已在相反DP、DP已结束；条约can_create拒绝/成功；同一人物本国/外国/流亡/void/死亡/自然退役；人物出生窗末年后旧档；USM明存/吴代/停战、置省进行/成功/失败；合法性49/50/51；小邦无港/内陆/零军力、宗主亡国/变更、市场变更、革命未改变独立；旧请求迟答、新JE旧JE重叠；同一成果第二次回调。

尚待引擎证实的部分：战争/国家灭亡回调顺序、角色退休和void的实际可见性、country供给消费修正对海军边界、集团市场自动刷新时点、具体存档财政/就业阈值。不得以AST或来源匹配写为ENGINE_PASS。本轮不启动游戏。

## 9. 可点击原始来源

- [现行意大利、HUS、USM升级方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/regional-expansion-20261104/italy-hus-usm-plan.md:1>)；[小国生存升级方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/regional-expansion-20261104/small-state-survival-plan.md:1>)。
- [坦志麦特成功/失败事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/sick_man_events.txt:70>)；[原生主日志](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_sick_man.txt:1>)；[当前错误入口](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_regional_development.txt:16>)。
- [原生联盟条款](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/00_alliance.txt:1>)；[实际建立联盟事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/soi_events/00_ep1_caucasus_events.txt:774>)；[意大利参战事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt:644>)。
- [原生军需消耗实际事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/brazil/paraguay.txt:509>)；[对应modifier](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/brazil_2_modifiers.txt:314>)；[本机modifier键定义](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/00_modifier_types.txt:3393>)。
- [原生非领袖政客模板](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_arg.txt:146>)；[角色生命周期](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_roles/00_auto_assigned_roles.txt:174>)；[角色数据库说明](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_roles/character_roles.md:1>)；[原生死亡hook](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:2604>)。
- [引擎人物全局查询](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:100>)；[引擎DP backer effect](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:226>)；[引擎人物转移](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37318>)。
- [实际战略区](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/strategic_regions/west_south_asia_strategic_regions.txt:1>)；[北美战略区](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/strategic_regions/north_america_strategic_regions.txt:9>)；[当前历史领土](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:202>)；[法/莱茵/意大利宗属](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:190>)。
- [LOM历史人物生成](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/characters/LOM.txt:1>)；[佩佩当前模板](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_ce_italian.txt:2>)；[HUS现行法律与公司](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:1>)。
- [小国原有资格](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt:1>)；[现有请求实际执行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:56>)；[真实投资条约](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/07_foreign_investment_rights.txt:1>)；[运动数据库方向](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md:48>)。
- [现行USM西部置省结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_usm_western_provinces.txt:20>)；[停战明廷身份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_ming_after_truce.txt:1>)。

实现代理应在最终差异定稿后记录新的源码行号与SHA，报告当前行号不是未来修改后的永久定位。技能维护复核：本轮新证据是坦志麦特双终态complete、政客role池与Paraguay实际消耗scope，建议在本批交付时纳入对应入口；本研究代理未修改技能或项目文件。

## 10. 本次关键来源指纹

仅绑定本次读取的源文件，不代表修改后的实现指纹。

|源码|SHA256|
|---|---|
|G/events/sick_man_events.txt|`d110d1fd83cd98e131d4c2769b606cc908f17844eff88ef65f51febf313a0c2b`|
|G/common/journal_entries/00_sick_man.txt|`e48405bfabb52f6ce757880e436c8d44c67111e246af3215fd3f96ec4f3477f9`|
|G/events/italian_unification.txt|`3564046713083efe19a97fe04a3d83a6e875a627794652ce726c727c602b296e`|
|G/common/treaty_articles/00_alliance.txt|`0db66b313c5b6d396d54b6abba265eaf031214f6930d50019a40b2200c59ff7c`|
|G/events/soi_events/00_ep1_caucasus_events.txt|`674474f2378e83c9430c50174c085272a220b640a4c4408c154e3820d34123f9`|
|G/events/brazil/paraguay.txt|`81391c93313c7f9fd6c35e98942fb865929a395d1b515fa7c41f86ed24439514`|
|G/common/static_modifiers/brazil_2_modifiers.txt|`5757585949f02bcfd37942c7839660cc2775ab1368f810bc895cfabe65c1f906`|
|G/common/modifier_type_definitions/00_modifier_types.txt|`b07822b507cdf169cc7df5edd41214857a80d95ce6ba79de7d11e688a86a6dbe`|
|G/common/character_templates/country_arg.txt|`12449bc62545fade294042eb92de82ea6cd76b86fb409e6e92e60cf4f6fe9780`|
|G/common/character_roles/00_auto_assigned_roles.txt|`7c53b49f0f79ac683811b3d5f5085197915f18de00864df8dc3873935ce49763`|
|G/common/on_actions/00_code_on_actions.txt|`ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb`|
|G/common/political_movements/00_ideological_movements.txt|`834a1b97f09c65b9b64eafdaffe4ee68965aaac262066140793a482eefd23a6b`|
|G/common/diplomatic_actions/42_subjects_request_market_control.txt|`88c081fb87846a98b78345fbda4e62e878184a08f161512a5c09baaab45699d1`|
|G/common/diplomatic_actions/36_subjects_grant_own_market.txt|`ad712dcfe896c0255eedf87ab979859c3e0702c56b8fc57370b7d61c71a076b3`|
|G/common/treaty_articles/09_join_power_bloc.txt|`9178a5b409a33634b557420b8730b01bf4f73991b23ad868602dc3aa22d63223`|
|M/common/strategic_regions/west_south_asia_strategic_regions.txt|`da8efdef8673e2a0e06ebf7990f453c434256ecde34901c1a70b37d0debe4a04`|
|M/common/history/diplomacy/ce_subject_relationships.txt|`78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7`|
|M/common/history/states/00_states.txt|`a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`|
|M/common/ideologies/01_character_ideologies.txt|`ea56543e49d9b25361f522d496b557413a8de62b2359a868aff3987f1a01128f`|
|M/common/scripted_triggers/nesnd_regional_development.txt|`d5ad989cea56569da5aab1cc25947b0d239667051a71692f3d5de9db5a8a48d6`|
