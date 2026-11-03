from india_context import *
from datetime import datetime,timezone
# Correct the research adaptation snippet, retaining a dated explanation of the actual native key check.
p=R/'commission-execution-contract.md';s=read(p).replace('set_capital=s:STATE_MADRAS','set_capital=STATE_MADRAS').replace('set_capital = s:STATE_MADRAS','set_capital = STATE_MADRAS').replace('set_capital = s:STATE_ZULULAND','set_capital = STATE_ZULULAND');s+='\n## 实施核对纠正\n\n原版events/meiji_restoration.txt:82与agitators_events/algeria_events.txt:939使用裸state-region数据库键：set_capital = STATE_KANTO / STATE_ALGIERS。本报告早期适配片段误加s:，已改；state创建仍是owner-state scope。奥兰治自由邦当前数据库键为STATE_VRYSTAAT，不是STATE_ORANJE。候选已修并通过Tiger检查。\n';write(p,s)
source=json.loads(read(R/'writing-source.json'));source['native_english_sources']={}
for rel in ['localization/english/ip2_misc_01_l_english.yml','localization/english/ip2_mughal_l_english.yml']:
 p=G/rel;source['native_english_sources'][rel]={'sha256':sha(p),'samples':[(i+1,l) for i,l in enumerate(read(p).splitlines()) if any(k in l for k in ['je_federation_of_india_reason:','je_mughal_hindustan_reason:'])]}
dump(R/'writing-source.json',source)
# Current task record links to immutable source audit; it is not a new gameplay test.
notes='''# 印度与两司实施交付

2026-11-03；父提交a1f2be2。独立候选india-development-20261103-a。STATIC_PASS，ENGINE_NOT_RUN；没有启动游戏或修改测试存档。实际合并、Git及独立备份以本目录JSON记录为准。

## 已落实的内容

1. 莫卧儿有效初始化统一：作者Bahadur/Mirza仍是唯一开局君主与继承人；保留原版两位无冲突IG领袖；删除不合用的英国公司调用。原始人口、州归属、建筑与外资数据不动。新开局37个新增营与原版3营合计40营；没有免费舰队，旧档不重复生成军队。
2. 德里的朝廷先开放学校/工业改革选择，单项达到实际建设、法律、机构和就业条件后累计12个月完成，切换不清进度。AI优先学校且避免反复切换；人类一年内只调整一次重点。原料允许由正常共同市场/进口满足；国内军工与铁路仍要建设。
3. 改革与民族主义之后开放印度共同体；王朝接受度单独的君主制日志，转共和后关闭，国家共同体保留。人权科技后开放身份与公职，既可以改种姓法律，也认可已经合法退出该社会层级的国家。BHT/DRA有统一后的行政、学校与铁路目标。
4. 43个有组织土邦共享自主议程，依实际宗属显示自治/独立请求；独立者可向FRA/MUG/USM商议真实防御条约。统一邀请只对独立、和平且愿意答复的实际国家；对方可以拒绝。并入支付安置费并承担十年年金工资开支，不自动吞并未答复的土邦。
5. 法国教师、工程师、军官三条援助。法国当前法律与在位王朝决定AI倾向，不是必定接受。实际拨款由法国国库扣除，受援方承担顾问工资；项目48个月，改宗主或交战撤顾问，既有条约不被无故删除。无库存采购、军需仓库或虚拟商品订单。
6. 六地区起义：西尔卡斯、库尔努尔、马德拉斯、迈索尔、特拉凡哥尔、古吉拉特。对象仅当时USM或其天竺属国实有的州片段。当地不满、人口、交通与教官影响筹备；暂停停费并缓慢衰减，暂时军力/合法性不足不清案。发难建立IR1–IR6地方共和国，只取得原殖民州片段，现有KNO/TRA等国家与土地保留。新募2/4/6/8营按人口分档，只在零现存军队时一次生成；不赠海军、不创建人口。
7. 起义采用有限收复州博弈：旧统治者return_state，地方共和国humiliation，允许和谈。独立赞助国明确加入防守方。每案保存真实DP，实际领土与独立结果决定成功；部分创建失败与普通失败没有胜利奖。全球只维护案件及限次重试，赞助者JE独占进度计分。失败返还仅限未经其他领土变更、原省份数量一致、单州、和平的新国；不回滚第三国所得。
8. 南明同时有决议与日志设立天竺、远山宣慰司。天竺以实际持有马德拉斯为首府锚点，划拨USM实有印度片段；远山以祖鲁兰/纳塔尔地区为锚点，需真实南非领地与建设。两司都不是1836白送疆土。殖民国家、傀儡、中央委任政府匹配既有宣慰司官制；种姓只设在天竺。原有筹备在USM→天竺转属后继续，天竺治理奖励完成后仍保留反制入口。

本轮新国家IR1–IR6是原殖民片段本地政治组织的实现选择，不将其虚构为原稿已有TAG，不强迫现有土邦接收领土。二司科技仅逐项确保宗主已经拥有且新司欠缺的技术；不假称存在copy_technology接口，不复制舰队或人口。

## 检查与证据

- 484项源码、引用、资产、有效本地化、初始化、代价、请求、六区同形与生命周期检查通过。
- 实际stdio MCP7项查询通过；Tiger相对父版零新增诊断。原有551项诊断仍分类保留，不以本轮检查宣称全MOD零BUG。
- Standards/Spec两轴审查找到并修复了空引用、预览、请求清理、暂时条件、返还保护、跨案援军、共和文字、进度条初值与按钮同步等问题；最终零未关闭发现。
- 197个中英文键逐项列在writing-lines.json，作者样本、原版英文与返工对读见writing-source.json、writing-comparison.md。条件和数字与实际代码对应。
- L01–L24检查矩阵见lifecycle-coverage.md；全部为源码/外部检查，没有引擎通过记录。

## 用户实测边界

新开局才能观察唯一历史人物与新增开局军队；旧档只补适用日志和缺失变量，不重刷军队。请优先留意实际JE首次出现与暂停重开、法国迟答/拒绝、筹备在建司后继承、具体战争退让/和谈，以及新国零军队时的原生募兵与兵营变化。动态军队继承、州合并回调顺序与建国后的实际经济无法由静态工具认证。

本轮没有强制解决稀缺、亏损或战败，没有改主MOD原有领土和人口。日本、已验证进港、编辑器等既有成果保留。更早南朝概率/密使等独立待办仍在其原任务图，本轮没有把它们冒称为完成。
'''
write(R/'release-notes.md',notes);write(R/'work-state.md',notes)
coverage='''# L01–L24覆盖：源码与外部检查，ENGINE_NOT_RUN

|范围|实际实现与检查|未证引擎边界|
|---|---|---|
|L01–L05阶段、重复与终局|晚期科技/改革done，缺值初始化；唯一JE计分；立即绝对同步；胜利/失败互斥，父项资格失效关闭|自然回调时点、UI首次显现、读档|
|L06–L09请求与对象|45天serial/双方patron/regime快照；一月事件/6月冷却；对象不存在分支失效；旧答复不操作新请求|实际事件取消与多人迟答|
|L10–L11、L18战争|每地区唯一类型/真实双方/登记DP；土地所有权与独立判胜；无重复制国|外交创建、退让、原生谈和、其他战争交织|
|L12–L16继承与领土|国家改号持久done；并国明确复制成果；USM→TZ1案件迁移；无人口不得创建；其他国家州不转|原生州分割/合并、国家形成接口时序|
|L17、L24法国政治|现行法律优先，实际君主家族其次，默认分支；快照过时作废|摄政与旧存档复杂人物状态|
|L19经济|真实市场价格/短缺备选，建设就业条件；费用不自动补偿；无仓库库存层|实际财政、就业、兵营/新募部队变化|
|L20人文政策|不转人口、不改已有名字；王朝JE在共和国关闭，国家共同体保留|新国原生人物生成|
|L21、L22玩家/AI|另一国真实接受/拒绝；priority一年、请求半年、资助四年冷却；无有效目标隐藏；弱势暂停保留|长期AI建设、政治和外交表现|
|L23非原子建国|分阶段登记、两次重试；失败无奖励；单州/原省份数量/未再易地/和平才可返还；其他情形明确余局失败|state_created/on_state_owner_change实际先后、空实体原生灭亡|

模板与数值测试不等于执行了游戏引擎。没有把Python状态模型输出称作真实游戏结果。
''';write(R/'lifecycle-coverage.md',coverage)
issue='''# 25 印度与天竺／远山宣慰司

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [详细交付与未证边界](<'''+(R/'release-notes.md').as_posix()+'''>)

## Result

按既有方案与新授权实施莫卧儿分阶段改革、种姓/共同体、法国合作、土邦自主/并入、六地区起义、统一后治理，以及南明天竺/远山决议与日志。484项外部检查、MCP7、Tiger零新增、两轴复查完成；未启动游戏。实际主MOD与Git结果以报告main-merge.json/git-delivery.json为准。原人口地图、作者日本改稿及之前修复保留。
'''
write(C/'.scratch/debug-release/issues/25-india-implementation.md',issue)
p=C/'.scratch/debug-release/map.md';write(p,read(p)+'\n## 最新：印度与两司实施（2026-11-03）\n\n[25 印度与宣慰司](issues/25-india-implementation.md)按用户授权实施；484检查/MCP7/Tiger零新增，双轴审查收口，未开游戏。新开局初始化与旧档迁移范围、实际合并结果见对应交付记录。\n')
p=C/'.scratch/india-development/map.md';write(p,read(p)+'\n## 实施记录：2026-11-03\n\n用户已明确授权开始实施及南明天竺/远山设司。既有研究与修订方案已落实到独立候选india-development-20261103-a，详见[任务25](../debug-release/issues/25-india-implementation.md)。前面的“仅计划”仅描述当时状态；484检查、MCP7与两轴复核为外部结果，不代表引擎验收。远山锚定南非，不挪到印度。\n')
# Skills: scoped new evidence, not a duplicated general checklist.
for rel in ['references/syntax-and-routing.md','references/journal-text-contract.md','references/active-work.md']:
 q=R/'skill-before'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,q)
p=S/'references/syntax-and-routing.md';write(p,read(p)+'''
## 印度实施的接口与案件隔离（1.13.11）

- 固定TAG建国的state是owner-state；set_capital使用裸数据库键STATE_*，不是s:前缀。combat_unit.count需要整数常量，动态人口分档用独立if/else_if选择常量。不要把继承certain values理解为已证明军队/技术全部继承；原版条件授予技术可单项核对，transfer_to_formation仅用于人物。
- 地区案件循环与重试每次先clear自己的临时backer/target scope。上次循环saved scope不会因下一次if不命中而自动消失。本轮已复现源码反例：第二案不合格赞助者会沿用第一案backer。
- set_state_owner转入现存国可能合并同地区州。返还整个region_state不是返还原来的province子集；回滚须保守证明未取得第三国地块。当前新建单州案同时保存原省份数并监听后续territory变化；不能以num_states=1单独证明安全。未知回调顺序保留引擎待验，不为清理而吞并整个现存国。
- 原版global通过add_contextless_journal_entry显式加入的JE，禁用壳必须保留contextless组；仅改possible=no不能封住显式添加。

来源与实际复查：WORK/reports/india-development-20261103/commission-execution-contract.md、uprising-execution-contract.md、india-standards-review.md。
''')
p=S/'references/journal-text-contract.md';write(p,read(p)+'''
## 阶段切换与数值同步：印度反例

保存变量并不会自动初始化新加JE的条。JE immediate、保留进度后重新进入、按钮改变与外国镇压改变都调用同一个只同步效果；计分仍只有该JE的周期回调。同步时保存当前country并保护存在性，不用可能是全球调用者的root读取国家变量。跨国/全局案件只负责生命周期，避免与国家JE重复推进。

暂时条件（战争、破产、军力或合法性）失去时按设计暂停、停维护费并保留案件；不要共用“新建资格”作为存续资格，导致自动清案与长冷却。建设奖JE完成之后仍需要的治理/防御按钮应挂在常驻入口。人口与领土成果不是按钮退出时的临时修正。

实际前后：WORK/reports/india-development-20261103/india-spec-review.md、india-spec-review-final.md及final-validation.json。未开游戏。
''')
p=S/'references/active-work.md';write(p,read(p)+'\n## 当前交付：印度与两司（2026-11-03）\n\n任务24已合入并推送a1f2be2；任务25印度新候选已完成484外部检查/MCP7/Tiger零新增及两轴复核，未开游戏。主MOD/Git结果看WORK/reports/india-development-20261103/main-merge.json与git-delivery.json。实施内容和未证边界见同目录release-notes.md。作者测试由作者启动；不得恢复旧观察者自动测试授权。\n')
print('Delivery records, lifecycle matrix, source corrections and skill notes saved')
