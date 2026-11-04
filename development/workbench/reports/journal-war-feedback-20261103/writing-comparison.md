# 玩家文本逐项对读

作者原文：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\pre-update-20261030T233944Z\mod\localization\simp_chinese\replace\ce_usm_events_l_simp_chinese.yml；SHA256 c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f。候选中文及英文分别核过主语、断句、重复、世界设定与效果对应；这不是游戏显示验收。

作者在 usm_civilwar.9.d 先叙战争消耗、再说脆弱和平，允许长句与明确政治判断；.11.d 从战后处境导出抉择；两条选项直接表态。新文沿用这条因果线，不另造国家宪法/议会，不把停战称作政治争端已解决。外交使节可以用所属国家指代；本轮没有颁诏动作，不强塞君主称号。

返工记录：归降提示原稿“若明帝尚在行在”遗漏寄居其它国家的情况，现改“若明帝仍在本国”。英文同步改为 still sheltered here。其余正文不把代码轮次、重试、变量或后台队列写给玩家。

短标签/统计取原生JE界面职责：显示名称与当前数值；不模仿事件叙事语气。两条印度完成条件各对应一个实际成果，不能合并成一个叉。

原样本 usm_civilwar.9.d，第228行：

> usm_civilwar.9.d: "这场震惊了世界的闹剧最终没有任何赢家。在长期的战争消磨中，南朝东西双方都耗尽了自己的战争潜力和工业底蕴。或许在不久的将来，这样脆弱的和平将会被打破，而更加伟大和血腥的时代将会到来。但至少现在的我们获得了喘息之机......"

原样本 usm_civilwar.11.d，第240行：

> usm_civilwar.11.d: "战争已然结束，胜果为他人所夺。我们和新朝的关系尴尬了起来。自北明以来，中原各省行诸侯政治不是什么新闻。但今日战胜之国若是转变枪口对准我们，我们难道就有信息抗拒”王师“吗？"

原样本 usm_civilwar.11.1，第242行：

> usm_civilwar.11.1: "我们应该维持自己的独立。"

原样本 usm_civilwar.11.2，第243行：

> usm_civilwar.11.2: "拥抱新政权。"

|键|最终中文|最终英文|对读与脚本核对|判定|
|---|---|---|---|---|
|nesnd_eastern_readiness_bar_name|远征条件|Preparations|短名称/来源标签与条目职责对应，不加入第二遍机制说明。|通过|
|nesnd_eastern_readiness_bar_desc|远征条件：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0] / 3#!|Preparations: #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0] / 3#!|原生GetCurrentBarValue调用，绝对计数与max=3/7一致；不再使用相对baseline。|通过|
|nesnd_eastern_readiness_bar_change|筹备情况变化|Preparations gained or lost|短名称/来源标签与条目职责对应，不加入第二遍机制说明。|通过|
|nesnd_japan_unification_bar_name|日本核心地区|Japanese Heartland|短名称/来源标签与条目职责对应，不加入第二遍机制说明。|通过|
|nesnd_japan_unification_bar_desc|核心地区：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0] / 7#!|Heartland regions: #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0] / 7#!|原生GetCurrentBarValue调用，绝对计数与max=3/7一致；不再使用相对baseline。|通过|
|nesnd_japan_unification_bar_change|领土变化|Territorial changes|短名称/来源标签与条目职责对应，不加入第二遍机制说明。|通过|
|nesnd_eastern_question_resolved_tt|东洋之议已有结果。|The eastern question has been resolved.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_india_schools_completed_tt|完成“学校与官署”。|Complete Schools and Administration.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_india_industry_completed_tt|完成“工场与军队”。|Complete Workshops and the Army.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_india_reform_schools_status|朝廷优先筹办学校与官署。|The court is giving priority to schools and administration.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_india_reform_industry_status|朝廷优先筹办工场与军队。|The court is giving priority to workshops and the army.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_india_reform_waiting_status|学校、官署与工场都需要经费。朝廷须先定轻重。|Schools, offices and workshops all need funding. The court must decide where to begin.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_india_schools_working|学务与官署扩建正在推进。|Work on schools and administration is under way.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_india_schools_paused|学务暂缓。|Work on schools is suspended.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_india_industry_working|工场与军队的整备正在推进。|Industrial and military preparations are under way.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_india_industry_paused|工场与军队的整备暂缓。|Industrial and military preparations are suspended.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_south_holdout_campaign|未息的南朝战事|An Unsettled Southern War|短名称/来源标签与条目职责对应，不加入第二遍机制说明。|通过|
|nesnd_south_holdout_campaign_reason|吴朝的号令尚未遍及南方。仍然拥明的诸国各有打算：有人准备再战，有人希望借北朝之力保存基业，也有人已在议论归降。停战之后，朝廷仍须面对这些未服的对手。|Wu’s authority does not yet extend across the south. The surviving Ming loyalists are divided: some prepare to fight again, others seek northern protection, and some consider submission. The court must still reckon with those who refuse its rule.|对照.9.d/.11.d：处境→行动；叙事主体明确，段内独立后果用句号。未新增机构或未来必然结局。|通过|
|nesnd_south_holdout_campaign_status|仍有拥明势力未归附。|Ming loyalists still hold out.|只报当前状态；不重复门槛。印度working与available、paused与visible对应。|通过|
|nesnd_south_holdouts_settled_tt|拥明诸国的归属已经确定，南朝战事已停。|The remaining Ming loyalists have settled their allegiance, and the southern fighting has ended.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_south_holdouts.1.t|停战之后|After the Armistice|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.1.d|本国已退出这场战争，但吴朝与拥明诸国的争执并未解决。败报与求和的消息相继传来，军中仍有人不肯放下兵器。如今，我们必须决定去向：再次举兵，向北朝寻求保护，或是承认吴朝的统治。|Our part in this war has ended, but the dispute between Wu and the Ming loyalists remains unresolved. Reports of defeat and appeals for peace arrive together; some officers still refuse to lay down their arms. We must decide whether to fight again, seek northern protection, or submit to Wu.|对照.9.d/.11.d：处境→行动；叙事主体明确，段内独立后果用句号。未新增机构或未来必然结局。|通过|
|nesnd_south_holdouts.resist|整军再战。|Prepare to fight again.|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.north|遣使北上，请求庇护。|Send envoys north to seek protection.|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.surrender|向吴朝归降。|Submit to Wu.|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts_resist_tt|着手再战，重新与大吴争夺南朝。|Prepare to renew the war against Wu.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_south_holdouts_north_tt|请求成为中华帝国的保护国。北朝将决定是否接纳；若未获保护，还须决定再战或归降。|Ask to become a protectorate of the Chinese Empire. If protection is refused, we must choose between renewed war and submission.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_south_holdouts_surrender_tt|本国将被大吴吞并。若明帝仍在本国，先安排其逃亡。|Our country will be annexed by Wu. A Ming emperor still sheltered here will be sent to safety first.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_south_holdouts.2.t|南方来使|Envoys from the South|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.2.d|[SCOPE.sCountry('nesnd_holdout_sender').GetName]的使者请求北朝保护。他们愿承认帝国的宗主地位，以求保住国土与军队。接受这份请求，便意味着帝国将在南朝纷争中承担新的责任。|Envoys from [SCOPE.sCountry('nesnd_holdout_sender').GetName] seek our protection. Their government offers to accept our suzerainty in return for preserving its territory and army. Accepting would give us a new responsibility in the southern dispute.|对照.9.d/.11.d：处境→行动；叙事主体明确，段内独立后果用句号。未新增机构或未来必然结局。|通过|
|nesnd_south_holdouts.accept|接受归附。|Accept their submission.|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.refuse|帝国无意承担此事。|We will not undertake this obligation.|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts_accept_tt|接纳来使所属国家为保护国。|Accept the requesting country as a protectorate.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_south_holdouts_refuse_tt|不提供保护，由来使所属国家另作决定。|Decline protection, leaving the requesting country to decide its next course.|对照.11.1/.11.2的明确表态；补原生不能表达的完成标记/等待/吞并或保护国后果，与实际分支对应。|通过|
|nesnd_south_holdouts.3.t|北朝未允|Without Northern Protection|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.3.d|北朝未能给予我们保护。使者的往返没有改变眼前的局势：要保住自己的国土，便须重新迎战吴军；要结束这场争夺，便只能向吴朝归降。|Northern protection has not materialised. The envoys’ journey has left us with the same choice: defend our country against Wu again, or end the struggle by submitting.|对照.9.d/.11.d：处境→行动；叙事主体明确，段内独立后果用句号。未新增机构或未来必然结局。|通过|
|nesnd_south_holdouts.4.t|北朝的保护|Northern Protection|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|
|nesnd_south_holdouts.4.d|使者带回了接受归附的答复。我们的国土与军队得以保留，北朝也成为本国的宗主。战后的生计与秩序，仍须由我们自己收拾。|The envoys have returned with acceptance. Our territory and army remain intact, and the northern empire is now our overlord. Restoring livelihoods and order after the war remains our task.|对照.9.d/.11.d：处境→行动；叙事主体明确，段内独立后果用句号。未新增机构或未来必然结局。|通过|
|nesnd_south_holdouts.4.a|先让百姓休息吧。|Let the people recover.|对照.11的短促选择；标题指当前事件，选项是行动，没有开发术语与无对应奖励。|通过|

共核39组中英文键。未改动原作者长篇事件文案；既有日本、印度正文与建筑门槛保持。英文按英语语序写，未逐逗号照译。新文没有把臣属市场误写成采购库存，没有将两院、礼法或地方行政改写为其它制度。
