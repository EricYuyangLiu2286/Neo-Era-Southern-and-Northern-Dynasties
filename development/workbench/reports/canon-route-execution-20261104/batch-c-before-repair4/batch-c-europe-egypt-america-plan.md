# C批计划：埃及、普奥、美洲竞争与共用外交

2026-11-04。状态：PLAN_ONLY，待root批准；此阶段只读源码与写计划，未改候选、未运行测试、未开游戏。执行对象为WORK/exports/canon-route-execution-20261104-a；固定父b94582ecec7b0b6dd5620a184658190157fc1729，独立备份pre-change-canon-route-execution-20261104T080559Z/mod。主MOD、本体、工坊、冻结备份只读。本机仍为1.13.11/build24799966。

依据最新steer-implementation-ledger.md、计划63、integration-native-contract.md及egypt-native-contract.md。旧Standards报告是发现时快照，不冒充当前候选仍有那些已修缺陷。此次先计划，再逐任务实现、逐任务外部检查；最后由root协调跨批次复审和合入。

## 1. 文件所有权与边界

C批独占现有文件：

- common/journal_entries/nesnd_egypt_independence.txt；common/{scripted_triggers,scripted_effects,script_values,scripted_progress_bars,scripted_buttons,on_actions,static_modifiers}/nesnd_egypt_independence.txt；events/nesnd_egypt_independence.txt；common/history/treaties/nesnd_egypt_1825.txt；common/treaty_articles/zzzz_nesnd_egypt_guarantee.txt。
- common/{journal_entries,scripted_triggers,scripted_effects,scripted_buttons,static_modifiers}/nesnd_europe_america.txt。
- common/{scripted_triggers,scripted_effects,script_values,on_actions}/nesnd_canon_diplomacy.txt；events/nesnd_canon_diplomacy.txt；common/scripted_buttons/nesnd_canon_requests.txt。
- events/nesnd_regional_development.txt及common/scripted_effects/nesnd_regional_development.txt：仅退役旧七国排队事件/领奖入口，不删除已获修正。

拟新增：common/on_actions/nesnd_europe_america.txt，events/nesnd_europe_america.txt，必要的common/script_values/nesnd_europe_america.txt，common/static_modifiers/nesnd_canon_diplomacy.txt，以及两语言独立replace文件zzzzzzzzzzzz_nesnd_batch_c_l_<language>.yml。EGY如采用下面的专用保护国方案，新增common/subject_types/nesnd_egypt_subject_types.txt与common/diplomatic_actions/nesnd_egypt_protectorate.txt；不改全局标准subject类型。旧埃及终局事件如需封闭，新增同路径events/veiled_protectorate_events.txt，仅停目标事件。

现有history/diplomacy/00_subject_relationships.txt与history/treaties/00_historical_treaties.txt只复核EGY差异；如修复，仅编辑EGY段。static_modifiers/nesnd_europe_america.txt中kind3/5使用的意大利、小国条目保留；共用请求接口`nesnd_canon_send_request={TAG=... KIND=...}`、kind1–5、serial字段和外部按钮键保留。后续批次可调用新安全helper，但不会被迫改接口。

不编辑TUR扩张/团结度、现有日本、HUS法条/NKH/MEX/Andes、意大利/HUS/USM人物与后续议程、印度南洋玩法。旧regional文件中的TUR事件只有退役壳处置，属于此次统一退役授权，不触碰B批TUR新路线。

## 2. 已见代码缺口

|对象|当前候选|本批处理|
|---|---|---|
|EGY两JE|第二JE只有status，第一JE已有六赞助＋none＋独立性条|第一JE完整保留六赞助按钮、none按钮和独立性bar的唯一挂载；第二JE改为真实教育与工场能力目标，完成给一次适度限时收益|
|EGY历史保证|visible放宽SIH后possible仍有泛用rank分支|原生分支补is_subject=no；历史例外仅六国→独立EGY、1845之前；其余原生字段保序不变|
|EGY计时/结算|已有持久30年钟、对象标记撤约、zero fail/invalid|补全初始化旧档和精确终态互斥；原生保护国失败保留pending，绝不当赞助国消失|
|外交请求|45日锁、6月冷却、事件duration=20月；kind1/4创建后无条件成功；旧式relations:scope参数|事件期限改为1月、次日送达、45日锁；先核真正条约才成功；修正原生relations函数；显式保护scope与回执身份|
|PRU|日志可续NGF/GER，请求仍只认PRU；3个alliance受multilateral_alliances限制|统一身份入口；外交资格按当前条约原生技术/关系；给早期实际防御协约路线，完整联盟后续仍可选|
|AUS|has_escalated未经证实；只看目标意大利及发起国名单|改原生is_war、escalation与领土/统一goal；复现原生参战侧规则，明确绑定双方、DP及结果|
|USA|全北美一次宣称、end_truce、羞辱主诉求、开博弈立即done|一次一个保存的争议州；不强行撕停战；实际return_state博弈；只有该州真实转移才有领土成果，白和/失败可重试|
|旧regional|JE已REPLACE关闭，排队成功事件仍有奖|取消旧队列/旧打开窗口，effect二次锁定不发奖，已领奖不撤销|

## 3. 按任务实施与检查顺序

### C1：共用请求，先完成后供各国接入

发送者country是唯一pending所有者。实际发出前清临时canon_sender/partner，分层exists→alive→不同国家→非交战→kind资格。保存双方、kind、单调递增serial；45日pending、6月冷却。事件保存值必须与当前发送者的serial/kind/partner均一致。迟答、失去对象、国家形成/换宗主、政体变化、外交关系下降或路线关闭时重新判断；不能用仅存活代替当前资格。国家形成允许PRU起源连续NGF/GER，其他新对象不冒领身份。

使用现有原生can_create_treaty完整结构（is_draft、binding_period均已查到支持），与执行create_treaty同方向同内容。接受联盟/防御条约后查真实条约article；投资接受后查实际source=申请国、target=投资国，并保存有效条约对象。若创建被拒绝，只结束本nonce并通知未缔约，不写成功、不发奖励。拒绝/过期只清当前匹配请求；新的请求不被旧事件清理。关系+25只在首次实际缔约发放，不能撤约重签刷关系。

kind1继续表示德国alliance；增加kind11表示德国defensive_pact（kind6/7/8保留给B2后续自主/市场请求），使用独立可读按钮，绝不静默把同盟请求变成另一条约。kind2仅欧洲投资对象FRA/GBR/PRU及连续NGF/GER；kind3、kind5保留既有接口与效果，纳入scope/nonce/生命周期保护，不在C批改变其设计。kind4为AUS对当前独立意大利邦国的防御条约。接收AI权重按当前关系及真实外交利益；已在相反阵营/不兼容宗属/不能创建原生条约时直接不可接受。

投资修正只依实际生效投资约维持；对象灭亡、开战、条约退出/替换丧失对应权利立即或最迟月度清理。多份不同欧洲投资条约不叠加同一经济修正；不可把投资权写成外国已经落厂。kind3的政治担保和kind5的财政支持仍由后续对应路线说明，不借此宣称所有外部玩法已完成。

kind3/5接口冻结合同：kind3由后续意大利议程提供真实发送者资格，接收方固定FRA；只表示限时法国政治信用/担保，绝不冒称已建立同盟或投资条约，不改变统一支持/国家归属。成功须实际写入发送者的担保期限与对应修正；法国改制、关系/宗属变化的担保存续规则留给该路线在C1冻结后扩展。kind5由B2提供真实`nesnd_small_state_country`及国家/市场资格；请求方向为小国host→投资国，成功必须有实际foreign_investment_rights，不能只写修正当投资成立。C1不新增always=yes/no占位trigger来把未实现依赖涂绿；冻结报告列出外部未完成接口，由B2/后续意大利批次接入后再做完整引用检查。双方都由同一serial/partner/kind/clock保护，拒绝/取消不清别人请求。C1编辑期B2不改共用文件，冻结后再交接扩展。

C1检查：发送/回复/拒绝/到期/旧nonce迟答；双方亡国、PRU形成国、接收者换宗主、双方政体和关系改变；创建失败无成功标记；同一条约重复接受；article双向、互惠/有向格式；按钮预览scope为空；AI事件参数与scripted_button数值字段分开核。

### C2：EGY六国协定与三十年独立

保留1825六约历史和1845精确撤约；每份新局历史创建先分支查双方存在。after-lobby一次登记当时六个定向投资＋保证的真实条约对象，1845后只退出这些对象，不撤玩家后来重签的新约。旧档：已登记不重扫；未登记且1845前仅允许明确匹配历史旧约，不能借补迁移误标普通新约。1845后未登记的旧档不猜测条约身份、不删除未知对象。

**第一JE（nesnd_egypt_independence）完整保留六投资国按钮FRA/USM/SIH/GBR/QE1/TUR、none按钮及独立性bar，全部在同一JE、唯一挂载，绝不把按钮搬去第二JE。** 第一JE显示真正当前对象、产业利益、公共建设/教育科研效益与退出代价，且唯一写国家独立性和bar；初始化一次=100，30历年期限一次；每月−1仅在实际活赞助存在时扣，外资压力以所有外国实际GDP所有权总和计算。现有平衡公式保留为−2×max(0,foreign_share−0.25)，并在来源和玩家原生明细明确25%缓冲；0/25/50/100%对应额外0/0/−0.5/−1.5/月。这是平衡选值，不是原生规定。

主动none保留mode=0，不自动再选。mode=1且对象灭亡先清旧修正，再从六个存活可交互对象选择，全部不存在则保持无对象。切换不重置独立性或期限。已在EGY属国树或与EGY交战者不能成为新承诺对象；现有赞助随后陷入这些状态时暂停/清利益并保留明确政治选择，不能暗中当作亡国重抽。

0且活赞助：先尝试标准protectorate，核真实overlord/type；rank/type限制导致正常存活赞助无法建立时，拟用埃及专用autonomy=2保护国类型与隐藏action，沿契约10.5实现，只放宽本路线rank/type。真正循环宗属或赞助自身不能持属国时仍保留pending及原对象，月度重试，不释放赞助、不改其原宗主、不发假的保护国事件。0且没有活赞助：invalid一次、合法性−15/60月。30年期满且独立性>0且非终态：一次120月成功修正。0与期满同日零独立性优先，不双结算。终态清赞助利益，未完成的能力子JE同步关闭；不刷新已获成功奖，也不撤销此前已完成的本地能力奖励。

**第二JE的具体目标与尺度（替换原nesnd_egypt_investment_accounts信息壳）：** 它展示王朝能否把资本、既有军工与地方劳动力转化为可持续的技术教育和工场能力；玩家用原生建设、生产方式、教育和就业经营推进，不添加领取/空转按钮。它与主JE同期开启，无投资国、没有投资权、foreign_share=0也完全可达。三项分别显示原生勾叉：

1. 本国至少一座大学level≥2、occupancy≥0.75。
2. 本国至少一座工具工场level≥3、occupancy≥0.75。
3. 本国至少一座实际主业工厂level≥5、occupancy≥0.75；可选纺织、兵工、钢铁、民用造船或食品厂，按原生OR分别显示种类。这些是经济能力替代路线，不绑当前赞助国。

三项同时成立即自动完成，不强加额外时钟/点击。一次奖励`nesnd_egypt_local_capability`持续60个月：`state_education_access_add=0.02`（受教育机会+2百分点）和`building_group_bg_manufacturing_throughput_add=0.05`（制造业吞吐+5%）。不恢复独立性、不暂停外资压力、不发免费工厂、不要求任何最低外国所有权、不把投资权限当成已建工厂。完成标记先于奖励；JE重加/重载/改赞助不续期。未完成时临时就业不足只阻止完成；主JE结束或国家身份失效才关闭。

开局源码基线（不是运行态就业证据）：有效history合并GAME与候选同路径覆盖后，EGY现有大学0、工具工场0、纺织4（下埃及3＋叙利亚1）、兵工2、造纸3。因此低成本路线为新建大学2、工具3、将一座纺织从3扩至5，同时真实招足人；不是开局自动领奖，也不要求外资落厂。此目标比原生教育坦志麦特的单座大学5级且就业>90%更温和。2%/5%且五年显著低于赞助公共15%建造与三十年终局20%制造十年奖励；属于本批平衡选值，未实测经济难度。

原生检查链：GAME/common/journal_entries/00_liberalism.txt:131–135使用country→any_scope_building→university/level/occupancy；00_sick_man.txt:269–274大学5级及90%就业；00_opium.txt:29–33同时检查建筑类型、occupancy≥0.75及level。有效开局来源GAME/common/history/buildings/03_north_africa.txt:43/54/67为纸3、纺织3、兵工2，候选common/history/buildings/08_middle_east.txt:533叙利亚纺织1。收益键沿本批已核EGY modifier合同，不新增未知modifier。

第二JE专门用例纳入C2冻结后测试：0外资且无投资权仍可完成；只有投资权/空厂不满足；大学1/2、工具2/3、主业4/5及就业74.9%/75%；各种主业替代只算一次；国家失去对应州即不再满足；完成后父JE成功/失败不重复领奖；已完成旧档不重设60月期限。


C2检查：六签署方向/对照非EGY条款AST、SIHdominion例外；none重复点击、全部赞助亡国、0/30年同日、pending原对象失效、父子JE两个回调顺序（子JE只观察建筑，不写独立性）；1845旧约/新约、失去原JE后恢复不刷新30年；GDP函数方向和单位；专用类型/action双向引用与有限兼容扫描。保护国建立和条约实际冻结边界仅标SOURCE_VERIFIED/STATIC，仍不宣称实机通过。

### C3：普鲁士的德意志协作

持久origin在PRU第一次激活时设置，续国NGF/GER的JE、按钮、请求、AI与清理全部共用身份谓词；非PRU来源形成国不能借tag继承未做过的路线。德邦对象按存活、持地、真实德意志主文化和独立外交资格判断。FRA/FRM现有属国不绕过原生权限强塞同盟；他们脱离后才开放正常条约请求。每个对象显示条约门槛。

分两阶段：①独立德邦协作：保留现有军队75、军工5的准备门槛，3个不同德邦的实际alliance/defensive_pact合作可达成；alliance本身仍受原生multilateral_alliances/关系/利益条件约束。②既有协作后的莱茵竞争：保留常驻外交入口与实际合作读数，正式军事利益只在当前仍满足合作时维持，失盟暂停而不重发初次奖励。对FRA仍持有的ALSACE_LORRAINE只授予一次来源清楚的宣称，不自动宣战或转地。国家实际形成GER可作为统一终点；法国/莱茵原有支配退出、联盟瓦解与国家从属有分别的状态/有限后果，不能把俾斯麦的某条未来固定排程。

C3检查：PRU→NGF→GER任一阶段/请求中形成；3伙伴distinct统计（同国两类条约不能算2次）；无多边同盟科技时早期防御路线；法属SAX、FRM属国拒绝；失盟不重置历史但暂停增益；FRA失去阿尔萨斯时不误给其他国家领土、不重奖。

### C4：奥地利在意大利实际争端中选择

常驻JE继续观察当前意大利小邦及实际统一者。防御条约使用C1 kind4。可干预目标必须是真实DP，target为意大利国家，initiator为FRA或意大利统一参与者，并有unification/conquer_state/return_state/annex_country领土目标；单纯贸易或羞辱争端不冒充统一。

用原生`is_war=no`与escalation开放期（define开局21、关闭80，读取define，不硬写未证has_escalated）；保存精确DP、目标国、对手和最初相关领土。按钮可见展示保存对象；执行重新核对象、双方、阶段、当前资格。将GAME scripted_rules/can_join_side_in_diplomatic_play的实际条件改写为专用带参数trigger：战略利益或真实防御承诺、集团限制、宗属关系；另核AUS非该DP任一主方、没有已承诺相反阵营/对友方战争、无对敌方停战或不兼容盟约。不把scripted_rule回调名误当可调用trigger。

实际add_target_backers后必须确认AUS在这一个DP目标方，才能记承诺及24月军费/防御修正；泛用is_diplomatic_play_committed_participant不算成功。保留这一DP直到结束，on_war_end/相关wargoal仅通知该案件核验。真正保存小邦独立及有匹配胜利证据→有限影响成果；小邦被并/目标领土失守→失败后果；白和→无胜利奖励并进入冷却。可以有代价承认当前统一者：明确关闭本次干预，不创造吞并/统一，不代意大利国家投票。拒绝干涉与自然未参战均不产生军费修正。

C4检查：DP21前/开放期/80后/已战争；不是领土争端；AUS本就是一方或另一场DP已承诺；FRA与AUS同侧/同盟/集团/停战；DP消失和target换tag；加入失败不扣成本；白和不记胜；之后无关战争不能结算旧案件。

### C5：美国的欧洲资本、边疆主张与真实领土争端

将现有总括任务拆成实际准备与边疆案件，保留主JE入口。欧洲投资是C1 kind2真正投资权；准备同时观察真实外资权利、军队60、军工8、铁路10及实际军工就业75%，不免费create_building或发不存在的资本。已取得的真实工厂不会在投资约退出时删除；临时融资修正停止。

争议州在HUS实际拥有的北美/中美owner-state中选，优先与USA本国接壤的州，保存具体state及region；不能从第三国份额拿地。提供刷新目标、向这一州提出主张、要求这一州归还三个不同动作。每次只add_claim一个region；没有有效目标/已有宣称不扣成本。拟主张成本为6月外交资源占用（influence−50）、对HUS关系−10、6月冷却，皆列为本批平衡选择。尚未接壤者可显示后置目标，不绕过可达地理限制。

战争入口复用原生dp_return_state、target_state=保存的HUS state，加入真实关系、停战、国家资格、战略利益/原生return_state规则及主目标合法性检查。删end_truce，不强制war=yes；允许原生退让/第三国介入。原生美国内战存在时暂停新增边疆攻势，保留投资/建设与旧案件；不因暂停清零成果。

创建后通过on_diplomatic_play_started绑定精确对象；仅见这场DP/战争才写started。完成只在所存HUS份额真实归USA且匹配本案回调后确认，发一次60月军事成果；如果HUS亡国且该州被第三国拿到则为失去目标，不假胜。白和/战败/撤诉分别反馈与冷却，保留已取得宣称；国家被吞并正常结束，不救援。不在开博弈时写continental_done。HUS有对应接收事件说明具体争议州；无需修改HUS国内法律或汗国链。

C5检查：无欧洲条约、只有权限没有外资厂、投资撤销；原生ACW前/中/后；HUS不存在、不是原HUS政权/已原住民后继、目标转第三国/分州合并；停战/同集团/关系过好；单州claim只一次，saved目标不在预览与执行间偷换；退让获地、战争获地、白和、战败、另一场战争获地，各有独立结果。原住民HUS后继沿实际身份停止原针对旧HUS统治集团的主线，不把tag相同当同一政治对象。

### C6：退役与玩家文本收口

七个旧regional成功事件及失败通知改hidden惰性壳，type先于cancellation_trigger，取消队列/旧窗，空immediate/option；旧reward helper增加退休闭包，防其他旧调用继续派发。只移除pending，不撤原来已经获得的60月修正，不删除国家发展数据。旧veiled_protectorate若存在排队终局同样定点封闭，保留无关原生事件。

本地化按nesnd-player-writing：从pre-update-20261030T233944Z原作者replace取同类正文/按钮/选项/进度样本，记录键、行、SHA；已经读取French政治按钮原句与bar样本。外交正文写当事国利益和具体承诺；存续/拒绝/等待/冷却各有独立可读反馈。稳定custom_tooltip只覆盖变量、路线和实际需说明的时限；原生law/relations/treasury/modifier用原生提示。英文真实英译。每个有效新键在batch-c-writing-comparison.md逐条通过/返工，发布前查后层覆盖与动态scope兜底。

C6检查：旧事件已打开/排队/显式trigger/既已领奖；七国所有旧奖不能重领；新旧JE同时在档不重结算；新键双语/BOM/概念/数值/占位符/动态对象；条约请求和战争按钮无空白效果预览。

## 4. 原生完整链条来源（本次读取；执行前必要时按改动回读）

|机制|调用者→数据库/引擎→执行与反馈|
|---|---|
|同盟请求|G/common/scripted_triggers/00_victoria_scripted_triggers.txt:330–365 can_create_treaty；G/events/soi_events/00_ep1_caucasus_events.txt:775–787 create_treaty；G/common/treaty_articles/00_alliance.txt:39–118关系、利益、多边同盟；01_defensive_pact.txt:38–110；D/triggers.log:8930–8964同形完整字段|
|投资权|G/common/history/treaties/00_historical_treaties.txt:242–289法埃实例；07_foreign_investment_rights.txt:33–118方向、原生可签/维持/重复检查；EGY契约第2–3节及10.3节|
|EGY保证例外|G/02_guarantee_independence.txt:36–139；EGY契约:375–384明确visible不能读other、possible补回独立、例外只EGY；历史绑定对象撤约与GDP求和见契约:98–144|
|EGY保护国|G/common/diplomatic_actions/31_power_bloc_force_become_subject.txt:41–65创建方向；C/common/subject_types/ce_subject_types.txt:124–183有效标准类型；D/triggers.log:9003–9008 can_have_as_subject；EGY契约:401–488专用type/action及不能循环的边界|
|真实DP参战|G/events/italian_unification.txt:643–674保存DP与add_target_backers；G/common/scripted_rules/00_scripted_rules.txt:81–143原生side资格；G/common/defines/00_defines.txt:1138–1140阶段；D/triggers.log:9786 escalation、10617 has_play_goal、12635 is_war|
|逐州战争|G/events/soi_events/00_ep1_kazakh_events.txt:269–277 scoped initiator、target_country、target_state、return_state；G/common/diplomatic_plays/00_diplomatic_plays.txt:129–153；G/common/war_goal_types/21_return_state.txt:24–38目标owner/claim合法性；G/common/scripted_triggers/00_scripted_triggers.txt:1753–1780实际外交关系阻挡|
|战争结算|G/common/on_actions/00_code_on_actions.txt:6230–6234 country root、target、diplomatic_play；:6988–6991 DP root、actor/target；:4216–4219敌国投降通知。只有绑定案件对象的回调可写本案结果；实际转地延后一天核、周度补漏|
|人物/设定|integration-native-contract.md:20–44 PPET冲突、FRM及意大利实际对象；本批不强造人物，不抢后续18人任务；PRU续国是既有同country对象连续身份|
|玩家文本|作者备份localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:237政治按钮、:248原生bar；后续逐类扩样再撰写，不将当前AI骨架当作者样本|

## 5. 完成条件与留存

每个C1–C6完成实现后停止编辑并保存该子任务文件SHA，再做该冻结内容的外部引用/边界检查；检查中发现问题先列修复任务、停止测试、修改后重新冻结复验，不边改边测旧快照。依agent-execution-plan.md由root安排关口；未授权的整批测试不提前执行。全部文件以保序parser审计重复块，脚本值的算式/边界从实际AST读取；对象语义以源实例/引擎文档核验，不能写简化模拟器冒充游戏运行。逐项报告新增SHA、实现差异、检查覆盖及仍属引擎的局限；最后对C批完整引用闭包做Tiger/MCP与Standards/Spec复审，修新发现后重新绑定最终指纹。

本轮不启动游戏。条约创建、生效/冻结、跨国scope保存、双JE自然时序、DP即时绑定和真实战后回调，只能保留待引擎证据；外部全部通过也只写STATIC_PASS。候选由root统一冻结备份、三方差异合入主MOD/Git并核远端；本代理不越过计划审批自行合并。


### 计划最终修订（root 2026-11-04）

EGY第一JE六投资国＋none＋独立性bar同页保留，是作者明确约束。第二JE采用上述大学/工具/主业就业能力与五年2%教育＋5%制造奖，不要求外国所有权。PRU防御协约路径、AUS原生参战资格、USA单一保存州及return_state方案已获root设计认可。当前仍PLAN_ONLY，待三批计划统一GO；此修订没有任何候选改动或测试运行。
