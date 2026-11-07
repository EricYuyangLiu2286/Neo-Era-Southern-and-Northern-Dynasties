# NESND 玩家文本返工 · 2026-11-07

以提交 `9d6959a` 及上轮 121 条记录为清单。复核了四组中英文文件。写入前，8 份主 MOD 文件逐字节与该提交一致。已确认的 10 条样稿均按原样定稿。

**实际修改 90 条，涉及 7 份文件；复核保留 31 条，其中含已删除的 16 个中英文条目。** 恢复审核前原文 6 条，局部修订 35 条，重写 49 条。

| 文件 | 复核条数 | 实际修改 | 复核保留 |
|---|---:|---:|---:|
| `localization/english/replace/nesnd_france_court_l_english.yml` | 3 | 3 | 0 |
| `localization/english/replace/nesnd_india_l_english.yml` | 6 | 2 | 4 |
| `localization/english/replace/nesnd_japan_l_english.yml` | 9 | 1 | 8 |
| `localization/english/replace/nesnd_journal_closures_l_english.yml` | 2 | 0 | 2 |
| `localization/simp_chinese/replace/nesnd_france_court_l_simp_chinese.yml` | 7 | 6 | 1 |
| `localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml` | 31 | 27 | 4 |
| `localization/simp_chinese/replace/nesnd_japan_l_simp_chinese.yml` | 48 | 41 | 7 |
| `localization/simp_chinese/replace/nesnd_journal_closures_l_simp_chinese.yml` | 15 | 10 | 5 |

问题类型和严重程度沿用首轮诊断。表中三版分别为审核前原文、上轮提交的文本、本次写入或保留的文本。波斯专档及共用文件中的波斯条目由外审负责。

## nesnd_france_court_l_english.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_court_royal_reason` | 技术错误／中 | `The Paris delegation has brought plans for a new quay. A provincial manufacturer waits three days in the corridor before a minister asks about freight. He lays two invoices on the desk. One gives the cost of landing a boatload of coal in Paris, the other the cost of getting it to his factory gate. The new king has yet to put his signature on a single drawing. Both men want the first.` | `The Paris delegation has brought plans for a new quay. A provincial manufacturer waits three days in the corridor before a minister asks about freight. He lays two invoices on the desk. One gives the cost of landing a boatload of coal in Paris, the other the cost of getting it to his factory gate. The court has yet to approve a single drawing. Both delegations want theirs signed first.` | `The Paris delegation has brought plans for a new quay. A provincial manufacturer waits three days in the corridor before a minister asks about freight. He lays two invoices on the desk. One gives the cost of landing a boatload of coal in Paris, the other the cost of getting it to his factory gate. The court must decide which project has the stronger claim on public funds.` | 局部修订 | 保留既有运煤比较和三天等候，仅将上轮改过的签字结尾改为宫廷面对的拨款决定，兼容摄政。 |
| `nesnd_court_activation` | 技术错误／中 | `The imperial succession has been settled and a Bourbon or Orléans monarch holds the French throne.` | `The imperial succession is settled. A Bourbon or Orléans holds the French throne, or is the heir during a regency.` | `The imperial succession is settled. Either the reigning monarch or, during a regency, the heir belongs to the House of Bourbon or the House of Orléans.` | 局部修订 | 明确在位君主与摄政储君两种家族判定。 |
| `nesnd_france_court.1.marked` | 技术错误／中 | `The auditor adds up both columns twice. The towns favored by the ministry have grown and now account for a larger share of the country’s urban centers. When the minister gives the table to the press, he asks the compositor to print the totals exactly as they stand.\n\nFrance gains #g 10#! Prestige for #v 24#! months.` | `The auditor adds up both columns twice. The towns favored by the ministry have grown and now account for a larger share of the urban centers in metropolitan states whose borders remained unchanged. When the minister gives the table to the press, he asks the compositor to print the totals exactly as they stand.\n\nFrance gains #g 10#! Prestige for #v 24#! months.` | `The auditor adds up both columns twice. The towns that received funding have grown. Across metropolitan states whose borders have remained unchanged since the allocation, the funded towns now account for a larger share of urban development. When the minister gives the table to the press, he asks the compositor to print the totals exactly as they stand.\n\nFrance gains #g 10#! Prestige for #v 24#! months.` | 局部修订 | 只调整上轮技术修复所在句。分别交代受资助地的增长、分母及比较起点。 |

## nesnd_india_l_english.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_india_reform_status` | 技术错误／低 | `The government is establishing schools and workshops.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。日志显式使用三路状态文本，覆盖旧默认状态。 |
| `nesnd_india_reform_finished_tt` | 技术错误／低 | `Complete Schools and Administration and Workshops and Armies.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。两项改革的完成提示各有专键，旧合并提示无调用。 |
| `nesnd_india_uprising_reason` | 技术错误／中 | `The Southern Court relies on ports, garrisons and local allies to sustain its rule. Its opponents also need organisation, money and friends. Delhi can assist them without treating their lands as its reward.` | `The Southern Court relies on ports, garrisons and local allies to sustain its rule. Its opponents also need organisation, money and friends. Our government can assist them without treating their lands as its reward.` | `The Southern Court relies on ports, garrisons and local allies to sustain its rule. Its opponents also need organisation, money and friends. Financial support from our government confers no right to govern the territory claimed by the insurgents.` | 局部修订 | 保留可变赞助方，只改上轮涉及的末句，区分资助与管辖权。 |
| `nesnd_india_contact_desc` | 技术错误／中 | `Support local opponents of colonial rule as they prepare to rise.` | `Local organizers need messengers they can trust and backers willing to pay.` | `Local preparations for the uprising depend on financial support from our government.` | 重写 | 联络、暂停、恢复与举事共用此键。写明本国与当地组织的资助关系，四种状态下均成立。 |
| `nesnd_india_preparation_tt` | 技术错误／低 | `Preparation in this region has reached 100.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。六地各用自己的举事条件，筹备值由脚本直接判断。 |
| `nesnd_india_usm_ready_status` | 技术错误／中 | `The Tianzhu Commission can now be established.` | `Enough mainland regions are under direct rule to meet the territorial requirement.` | `Enough mainland regions are under direct rule to meet the territorial requirement.` | 保留上轮稿 | 状态只报告领土条件，英语已准确区分领土达标和可以设司。 |

## nesnd_japan_l_english.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_japan_send_terms_requirements` | 技术错误／中 | `Wu and Japan are at peace, with no truce between them, and neither is committed to a diplomatic play. Japan is independent or a Wu subject, is ruled by a Toyotomi, Tokugawa or Yamato monarch, and fully owns Kyoto, Kanto, Kansai and Chugoku. Fu and Wa have yet to be established.` | `Wu and Japan are at peace, with no truce between them, and neither is committed to a diplomatic play. Japan is independent or a Wu subject, is ruled by a Toyotomi, Tokugawa or Yamato monarch, and fully owns Kyoto, Kanto, Kansai and Chugoku. Fu and Wa have yet to be established. Japanese holdings in Honshu, Hokkaido, Kyushu and Shikoku must be controlled by Japan or Wu.` | `Wu and Japan are at peace, with no truce between them, and neither is committed to a diplomatic play. Japan is independent or a Wu subject, is ruled by a Toyotomi, Tokugawa or Yamato monarch, and fully owns Kyoto, Kanto, Kansai and Chugoku. Fu and Wa have yet to be established. Japanese holdings in Honshu, Hokkaido, Kyushu and Shikoku must be controlled by Japan or Wu.` | 保留上轮稿 | 条件提示完整列出第三国占领限制，沿用上轮技术修复。 |
| `nesnd_japan.1.d` | 技术错误／中 | `The envoys from Nanjing propose to divide the realm. Kyoto and Osaka would recognize the Emperor, the Tokugawa would rule from Edo, and the Toyotomi would govern western Kansai and Chugoku. Wu would administer Kyushu and Shikoku directly. The levies and revenues of the eastern domains would henceforth answer to several governments. The retainers have laid their accounts of troops and provisions before [ROOT.GetCountry.GetRuler.GetFullName], who must decide how to answer.` | `The envoys from Nanjing propose to divide the realm. Kyoto and Osaka would recognize the Emperor, the Tokugawa would rule from Edo, and the Toyotomi would govern western Kansai and Chugoku. Wu would administer Kyushu and Shikoku directly. The levies and revenues of the eastern domains would henceforth answer to several governments. The retainers have laid their accounts of troops and provisions before the assembled council and await an answer.` | `The envoys from Nanjing propose to divide the realm. Kyoto and Osaka would recognize the Emperor, the Tokugawa would rule from Edo, and the Toyotomi would govern western Kansai and Chugoku. Wu would administer Kyushu and Shikoku directly. The levies and revenues of the eastern domains would henceforth answer to several governments. The retainers have submitted estimates of the troops and provisions available to the council.` | 局部修订 | 沿用上轮去除不安全君主回调的修复，明确提交的是可用兵力与军粮的估计。 |
| `nesnd_japan.2.d` | 技术错误／中 | `Japan’s envoys have declined the proposed settlement. An expedition would require Nanjing to provide funds and ships to install the three houses in their domains. The court may also withdraw its demands and leave Japan under a single government. The decision rests with [ROOT.GetCountry.GetRuler.GetFullName].` | `Japan’s envoys have declined the proposed settlement. An expedition would require Nanjing to provide funds and ships to install the three houses in their domains. The court may also withdraw its demands and leave Japan under a single government. The decision rests with the court in Nanjing.` | `Japan’s envoys have declined the proposed settlement. An expedition would require Nanjing to provide funds and ships to install the three houses in their domains. The court may also withdraw its demands and leave Japan under a single government. The decision rests with the court in Nanjing.` | 保留上轮稿 | 末句由南京朝廷作出决定，不依赖君主姓名，表述简洁。 |
| `nesnd_jp_mercantile_ports_desc` | 技术错误／低 | `Allow merchants to trade overseas, using tariffs to support state revenue and domestic commerce.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_protected_ports_desc` | 技术错误／低 | `Open the sea routes to obtain the materials our factories need, while using tariffs to support domestic producers in the wider market.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_political_opposition_desc` | 技术错误／低 | `War and Radicalism` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。进度条改用战争、激进情绪两条独立明细，旧合并键无调用。 |
| `nesnd_jp_development.2.t` | 技术错误／中 | `Reform Takes ` | `Reform Takes Root` | `Reform Takes Root` | 保留上轮稿 | 保留完整事件标题。 |
| `nesnd_jp_mercantile_ports_junior_desc` | 技术错误／低 | `Replace seclusion with mercantilism and permit overseas commerce. The common market’s tariffs remain under the control of its leading country.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_protected_ports_junior_desc` | 技术错误／低 | `Adopt protectionist trade laws and open our ports. The common market’s tariffs remain under the control of its leading country.` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |

## nesnd_journal_closures_l_english.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_journal_closures_parent_cne` | 技术错误／中 | `This undertaking ends with “$ce_cne_land_reform$”.` | `While $ce_cne_land_reform$ is in effect.` | `While $ce_cne_land_reform$ is in effect.` | 保留上轮稿 | 按开启条件描述适用期间，保留父日志键。 |
| `nesnd_journal_closures_parent_qin` | 技术错误／中 | `This court agenda ends with “$nesnd_qe1_agenda_journal$”.` | `While $nesnd_qe1_agenda_journal$ is in session.` | `While $nesnd_qe1_agenda_journal$ is in session.` | 保留上轮稿 | 按开启条件描述朝议期间，保留父日志键。 |

## nesnd_france_court_l_simp_chinese.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_court_royal_reason` | 技术错误／中 | `巴黎市政厅送来了新码头的图样。外省来的商会代表也带着图样，在走廊上等了三天，终于等到大臣问起运费。他把两张账单并排摆好：一船煤运到巴黎是多少钱，运到自家厂门口又是多少钱。新国王刚刚登基，两拨人都盼着他在自己的图纸上签第一个字。` | `巴黎市政厅送来了新码头的图样。外省来的商会代表也带着图样，在走廊上等了三天，终于等到大臣问起运费。他把两张账单并排摆好：一船煤运到巴黎是多少钱，运到自家厂门口又是多少钱。宫里还没批下头一项工程，两拨人都想把自己的图纸放在上面。` | `巴黎市政厅已呈交新码头的图样。外省商会的代表等了三天，才有机会向大臣陈述本地厂主的困难。他列出一船煤运抵巴黎和运抵本省工厂的两笔费用，请宫廷在议定工程拨款时考虑外省工业的运输负担。` | 重写 | 保留码头、三天和煤运账目，以两方争取拨款的理由收束。宫廷议款也适用于摄政。 |
| `nesnd_court_activation` | 技术错误／中 | `法国帝国主线已经结束，波旁或奥尔良君主已就位。` | `帝位继承已定，法国由波旁或奥尔良家族执政；摄政期间以储君的家族为准。` | `帝位继承已定，法国由波旁或奥尔良家族执政；摄政期间以储君的家族为准。` | 保留上轮稿 | 开启条件已区分执政与摄政时的家族判定。 |
| `nesnd_france_court.1.marked` | 技术错误／中 | `审计员把两栏数字分别加了两遍。拨款所及的城镇确已扩张，它们在全国账上所占的份额也见了涨。公共工程部长把这张表交给报馆时，特地嘱咐排字工照原样印出末尾的合计。\n\n法国获得 #g 10#! 威望，持续 #v 24#! 个月。` | `部长把审计员的表送去排印，特地用铅笔圈出末栏。只算本期拨款后疆界未动的本土州，领过拨款的城镇所占的份额也涨了。他要报馆把这栏也印出来。\n\n评议结算　法国威望 #g 10#! 点，为期 #v 24#! 个月。` | `审计员复核了本期拨款前后的两份账册。在疆界未变的法国本土各州中，获拨款地区的城镇规模有所增长，所占份额也有提高。公共工程部长将这份核算结果交给报馆刊布。\n\n法国获得 #g 10#! 威望，持续 #v 24#! 个月。` | 重写 | 保留本土可比范围和双重达标的区别，去掉关于铅笔圈画与排印的重复描写。 |
| `nesnd_france_court.1.growth` | 机械性／低 | `各地寄回的册页已经订成一卷。审计员在合计数下划了一道线：当年领了工程的地方，如今确实多出了都市街区。这句话足够让部长在议事厅把五年前的许诺再念一遍。\n\n法国获得 #g 5#! 威望，持续 #v 24#! 个月。` | `部长在议事厅念了五年前的许诺，随即翻到审计员作记号的那一页。领过拨款的地方，新添的街区已经逐处登了册。\n\n评议结算　法国威望 #g 5#! 点，为期 #v 24#! 个月。` | `各地呈报的账册显示，本期获得工程拨款的地区已有新的都市街区。公共工程部长在议事厅宣读了审计结果，说明五年前议定的工程已有成效。\n\n法国获得 #g 5#! 威望，持续 #v 24#! 个月。` | 重写 | 普通档仅确认都市增长；延用原文的议事厅与五年期限，结算另起一段。 |
| `nesnd_france_court.1.paris` | 机械性／低 | `核算地区：巴黎。$nesnd_court_figures$` | `巴黎工务呈报。$nesnd_court_figures$` | `核算地区：巴黎。$nesnd_court_figures$` | 恢复原文 | 核算地区是账目口径，原抬头短而确切。 |
| `nesnd_france_court.1.provinces` | 机械性／低 | `核算地区：外省。$nesnd_court_figures$` | `外省工务合报。$nesnd_court_figures$` | `核算地区：外省。$nesnd_court_figures$` | 恢复原文 | 与巴黎核算抬头对称，外省是统计范围。 |
| `nesnd_court_figures` | 机械性／低 | `都市等级从 #v [SCOPE.GetValue('nesnd_court_before')\|0]#! 至 #v [SCOPE.GetValue('nesnd_court_after')\|0]#!，在疆界可比的本土州中所占份额从 #v [SCOPE.GetValue('nesnd_court_share_before')\|2]%#! 至 #v [SCOPE.GetValue('nesnd_court_share_after')\|2]%#!。` | `本土各州，疆界有变者另册。所报城镇原计 #v [SCOPE.GetValue('nesnd_court_before')\|0]#! 级，今计 #v [SCOPE.GetValue('nesnd_court_after')\|0]#! 级。占同册各州都市总数，原为 #v [SCOPE.GetValue('nesnd_court_share_before')\|2]%#!，今为 #v [SCOPE.GetValue('nesnd_court_share_after')\|2]%#!。` | `在本期疆界未变的本土州中，核算地区的都市等级期初为 #v [SCOPE.GetValue('nesnd_court_before')\|0]#! 级，期末为 #v [SCOPE.GetValue('nesnd_court_after')\|0]#! 级，占上述各州都市总等级的份额由 #v [SCOPE.GetValue('nesnd_court_share_before')\|2]%#! 变为 #v [SCOPE.GetValue('nesnd_court_share_after')\|2]%#!。` | 局部修订 | 交代可比范围与等级分母，期初期末的表述也适用于持平或下降。 |

## nesnd_india_l_simp_chinese.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_india_reform_reason` | AI 八股／低 | `莫卧儿的旧帝国曾靠君主的声望维系各省，如今的统治者却必须面对新的问题。法国商人与教官带来了财富和新式兵器，也带来了新的债主。国家需要自己的学校和工场，让地方的赋税变成能够保卫它的力量。` | `莫卧儿君主从前凭一道谕令就能向各省征调兵马。如今军中添一批新枪，先得同法国商人议价，再由法国教官教人操练。各省送来的税银，有多少能留下来办自己的学堂和工场？` | `莫卧儿的旧帝国曾靠君主的声望维系各省。法国商人与教官带来了资本和新式兵器，法国债主也由此在印度取得了影响。德里希望以各省赋税兴办自己的学校和工场，逐步培养本国的教员与军械工匠。` | 局部修订 | 保留原文中王朝声望、外来资本与债权的关系，以本国教育和工业写出改革方向。 |
| `nesnd_india_reform_status` | 技术错误／低 | `政府正在筹办学校与工场。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。日志显式使用三路状态文本，覆盖旧默认状态。 |
| `nesnd_india_schools_reason` | AI 八股／低 | `帝国需要能看懂账簿的官员，也需要能教会下一代读书的人。德里的一所学院无法代替各省的学校。纸张、教师与稳定的经费，必须一同送到地方。` | `德里的学院每年送得出多少识字的办事员？各省的税册堆在官署里，等着有人来核。地方要开学堂，先生的薪水和学生用的纸都得有着落。` | `德里的学院足以培养一批官员，却难以独力承担各省的学务。地方官署需要通晓账目的书吏，各省学校也须延聘教师。维持校舍、购置纸张和支付薪俸，都有赖于常年的地方经费。` | 重写 | 按官署和学校各自的人力需要展开，保留经常性经费的实质。 |
| `nesnd_india_princes_reason` | AI 八股／低 | `德里、南京与巴黎都向印度诸邦递出了自己的条件。王公们所要保住的不只是祖传的宫殿，还有土地、税收和决定本国命运的权力。合作可以带来援助，却不一定带来自主。` | `德里、南京和巴黎的使节都肯帮王公守住宫门。至于门外的田租归谁，军队听谁号令，几封国书开出的价可大不相同。` | `德里、南京与巴黎都向印度诸邦提出了合作条件。王公们愿意接受外援，也要保全世袭领地和征税的权力。对各邦而言，一份盟约的轻重，取决于缔约之后有多少政务仍可由本国裁决。` | 局部修订 | 延用三方交涉及王公利益，删去虚构的守门许诺。 |
| `nesnd_india_princes_status` | AI 八股／低 | `本国的主权与地方利益仍待守护。` | `王公们还在同各方议价。` | `各邦正在权衡德里、南京与巴黎提出的条件。` | 重写 | 状态说明交涉对象，避免将主权交涉写成讨价。 |
| `nesnd_india_unified_reason` | AI 八股／低 | `统一使许多边界从地图上消失，却没有消除各省的差别。新的国家必须把税收、教育与公共事务维持下去，让共同的法律在宫廷以外也具有意义。` | `从前隔着邦界打官司，走到界碑就得另投一道状。如今两边奉同一部法令，收税的旧账还各有各的算法。各省百姓要看这新政府怎样断头一桩案。` | `印度统一以后，旧邦界已失去政治意义，各省沿用的税制与办学成规仍有差异。共同的法律要在全国施行，新政府须使地方官署有能力征收赋税，维持学校和各项公共事务。` | 局部修订 | 恢复原稿的税收、教育与施政问题，删去虚构的首宗诉讼。 |
| `nesnd_india_priority_desc` | 机械性／低 | `将政府的人力与经费集中到这项事业上。` | `国库里这笔钱，学堂要用，工场也要用。总得有一家先领。` | `学务与实业均需国库拨款，政府须确定两项事业的先后次序。` | 重写 | 两枚按钮共用此句。明确由政府分配经费，两种选择均适用。 |
| `nesnd_india_settlement_desc` | 机械性／低 | `将各省共同的政治要求确立为国家的制度。` | `各省肯同奉一部宪章，就得在议席上听得见自己的声音。` | `各省要求推举代表，参与国家立法。` | 重写 | 两项政治方案都引入选举。写明代表权的内容，同时兼容君主与共和两种政体。 |
| `nesnd_india_reform_finished_tt` | 技术错误／低 | `完成学校与官署、工场与军队。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。两项改革的完成提示各有专键，旧合并提示无调用。 |
| `nesnd_tianzhu_governance_reason` | AI 八股／低 | `天竺的商人熟悉海路，乡村却有另一套秩序。宣慰使既要维持港口与驻军，也要让学校和税务进入内地。当地王公与村社不会仅因南京的任命就放弃自己的利益。` | `天竺港里的商人知道哪一季来船，也知道关税该交给谁。往内地走，收租有王公，断事有村社。宣慰使若要在那里办学收税，光给他们看南京发的印信可不够。` | `天竺的商人熟悉海上贸易，内地的田赋与地方事务则多由王公和村社经手。宣慰使受命治理港口、供养驻军，若要将学务和税政推及乡村，还须取得地方的合作。` | 重写 | 重心回到南京任命与地方既有权力的关系，避免假定见印即从。 |
| `nesnd_establish_yuanshan_desc` | 机械性／低 | `将远山的领地交由中央委任的宣慰使治理。` | `远山的驻军等得到海船，等不得每件事都送南京批。` | `远山距南京遥远，朝廷拟任命宣慰使，就地统辖当地军政。` | 重写 | 保留中央任命宣慰使这一授权关系，并说明就地治理的缘由。 |
| `nesnd_india_foreign_reason` | AI 八股／低 | `法国希望以贸易、投资与军事援助维持在印度的影响，[ROOT.GetCountry.GetName]的政府则需要教师、工程师和军官。借助法国的知识与技术，可以培养本国人才，也会使国家继续依赖巴黎的支持。` | `法国愿意把教师、工程师和教官送到[ROOT.GetCountry.GetName]来。当地要有人懂得开矿练兵，巴黎也有自己的盘算。等学生们能接先生的班时，聘书上那些条件还作不作数？` | `[ROOT.GetCountry.GetName]的政府希望延聘法国教师、工程师与教官，为本国学校、工场和军队培养人才。巴黎愿意提供援助，也希望借此巩固法国在印度的商业与军事影响。` | 局部修订 | 保留动态国名和三类顾问，仅写双方利益，不预设聘书条款。 |
| `nesnd_india_foreign_status` | AI 八股／低 | `援助与自主之间，需要自己的打算。` | `使团可与法国商议延聘教师、工程师和教官。` | `使团可与法国商议延聘教师、工程师和教官。` | 保留上轮稿 | 状态行已列出可商议延聘的三类人员。 |
| `nesnd_india_diplomatic_desc` | 机械性／低 | `向对方正式提出请求，由其政府作答。` | `把条件写进国书，请使者带一句准话回来。` | `向对方正式提出请求，由其政府作答。` | 恢复原文 | 外交事项共用此句；原文能准确说明由对方答复，省去使者传话的虚构。 |
| `nesnd_india_diplomacy.1.d` | AI 八股／低 | `[SCOPE.sCountry('india_sender').GetName]的使团已经抵达，带来了有关两国关系的请求。使者正在等待答复。` | `[SCOPE.sCountry('india_sender').GetName]的使者递上国书，在客馆候信。` | `[SCOPE.sCountry('india_sender').GetName]的使团已呈交国书，等候我国政府答复。` | 重写 | 通用来文仅交代使团所处的交涉阶段。 |
| `nesnd_india_diplomacy.2.d` | AI 八股／低 | `[SCOPE.sCountry('india_partner').GetName]接受了我们的请求。约定已交付执行，接下来仍要靠本国将它变为成果。` | `使者把[SCOPE.sCountry('india_partner').GetName]签过的文书带回来了。两边议定的事，如今可以照办。` | `[SCOPE.sCountry('india_partner').GetName]已接受我国提出的条件。` | 重写 | 接受答复已经完整，删去签署文书的细节。 |
| `nesnd_india_diplomacy.3.d` | AI 八股／低 | `[SCOPE.sCountry('india_partner').GetName]拒绝了使团提出的条件。我们仍须寻找自己的出路。` | `[SCOPE.sCountry('india_partner').GetName]退回了国书。使团照原路返程，没能带回一纸约定。` | `[SCOPE.sCountry('india_partner').GetName]拒绝了使团提出的条件。` | 局部修订 | 保留原文第一句，删去泛论出路和返程场景。 |
| `nesnd_india_diplomacy.1.d1` | AI 八股／低 | `[SCOPE.sCountry('india_sender').GetName]请求法国派遣教师，并拨款支持初期办学。使者希望以此培养本国人才，法国也将借顾问团扩大在当地教育中的影响。` | `[SCOPE.sCountry('india_sender').GetName]的使者想从法国请几位教师，连办学的钱也想在巴黎筹。他说，学堂可以在本国开，头一批先生得劳法国人费心。` | `[SCOPE.sCountry('india_sender').GetName]请求法国派遣教师，并拨款支持当地学校的开办。` | 局部修订 | 保留援助的两项内容，删去代使者编写的陈词。 |
| `nesnd_india_diplomacy.1.d2` | AI 八股／低 | `[SCOPE.sCountry('india_sender').GetName]请求法国派遣矿业与工业工程师，并拨款协助开办产业。使者希望取得新的生产技术，法国企业也将从这段合作中寻找商机。` | `[SCOPE.sCountry('india_sender').GetName]缺的是会勘矿、会办厂的人。使团来法国延请工程师，也来谈开办的本钱。做机器买卖的商人已经打听起这桩生意。` | `[SCOPE.sCountry('india_sender').GetName]拟扩充本国矿业与工业，请法国派遣工程师，并资助有关工场的建设。` | 重写 | 说明援助用途，保留技术人员与经费两项请求。 |
| `nesnd_india_diplomacy.1.d3` | AI 八股／低 | `[SCOPE.sCountry('india_sender').GetName]请求法国派遣军事教官，并拨款协助整训军队。受援国希望改善训练与装备，法国则有机会影响这支军队今后的组织。` | `[SCOPE.sCountry('india_sender').GetName]想用法国的办法练兵，托使者来请教官。操典可以随身带去，枪械却要花钱，来文末尾便是请法国拨款的数目。` | `[SCOPE.sCountry('india_sender').GetName]请求法国派遣军事教官，并拨款协助整训军队。` | 局部修订 | 保留原文首句。来文没有列明军购金额。 |
| `nesnd_india_diplomacy.1.d4` | AI 八股／低 | `[SCOPE.sCountry('india_sender').GetName]的使者要求扩大自治权，让当地政府自行处理更多事务。我们必须决定是否放宽现有的宗主权。` | `[SCOPE.sCountry('india_sender').GetName]的使者来争一件事。凡地方自己办得了的事务，往后别再叫他们把文书送到宗主这里来回跑。` | `[SCOPE.sCountry('india_sender').GetName]的使者要求扩大自治权，让当地政府自行处理更多事务。` | 局部修订 | 采用审核前原文首句，使自治与完全独立有所区别。 |
| `nesnd_india_diplomacy.1.d6` | 机械性／低 | `[SCOPE.sCountry('india_sender').GetName]邀请本国并入统一的印度，并提出以年金保障原有王公。接受这一安排，就意味着结束本国的单独统治，将土地与人民交由对方政府管辖。` | `[SCOPE.sCountry('india_sender').GetName]送来了合邦的约书。王公名下的年金写得明白，往后本地的税簿要送到对方政府，约书上也写得明白。` | `[SCOPE.sCountry('india_sender').GetName]邀请本国并入统一的印度，并提出以年金保障原有王公。接受这一安排，就意味着结束本国的单独统治，将土地与人民交由对方政府管辖。` | 恢复原文 | 依作者意见恢复原文。年金是给予王公的条件，第二句交代本国让渡的管辖权。 |
| `nesnd_india_diplomacy.1.d7` | 机械性／低 | `[SCOPE.sCountry('india_sender').GetName]请求我们承认其独立，由当地政府自行决定内外事务。接受请求将结束现有的宗属关系。` | `[SCOPE.sCountry('india_sender').GetName]的来使请求独立。这回他求见宗主，为的是往后两国再通国书时，谁也不必向谁称臣。` | `[SCOPE.sCountry('india_sender').GetName]的来使请求结束两国宗藩关系，真正行使国家主权。` | 重写 | 采用作者定稿。宗藩关系与国家主权已经说明独立请求的内容。 |
| `nesnd_india_uprising_reason` | 技术错误／中 | `南朝的统治依靠港口、驻军和愿意合作的地方势力。反对者同样需要组织、经费与盟友。德里可以帮助他们行动，却不能因此把他们的土地视作自己的奖赏。` | `南朝的驻军把守海港，收税却少不了当地人帮忙。反对它的人也在各处找钱、找门路。他们托人捎来的话很明白：肯出钱的可以做朋友，别来做主人。` | `南朝依靠港口、驻军和当地盟友维持统治。反对南朝的地方组织若要公开举事，需要外来的经费和支持。本国可以资助他们争取独立，举事地区的归属仍应由当地人决定。` | 重写 | 保留多种赞助政权共用的本国视角，交代援助与领土权利。 |
| `nesnd_india_contact_desc` | 技术错误／中 | `资助当地的反殖民组织，为公开举事作准备。` | `南方的密信要有人送，愿意出面举事的人也得知道，身后还有谁肯出钱。` | `地方组织筹备起义，有赖于本国的经费支持。` | 重写 | 与已确认英文对应。说明资助关系，亦适用于暂停或恢复联络。 |
| `nesnd_india_preparation_tt` | 技术错误／低 | `本地区的筹备已达100。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。六地各用自己的举事条件，筹备值由脚本直接判断。 |
| `nesnd_india_revolt_war_reason` | 机械性／低 | `旧统治者要求收回这片土地。独立的命运将由这场交涉与战争决定。外国资助不应成为另一个国家吞并我们的借口。` | `旧统治者已来索地，举事的人守着刚接过手的官署。我们向外人借钱时，可曾答应连官署的钥匙也一并交给债主？` | `旧统治者要求收回起义地区，新政府则要求承认独立。我们曾接受外国资助，但援助并未赋予资助国管辖这片土地的权利。` | 重写 | 保留旧统治者、起义政府和资助国三方的关系。原文没有贷款约定，删去债主与钥匙的比喻。 |
| `nesnd_india_suppression_desc` | 机械性／低 | `以额外的警务开支打击地方秘密组织。` | `巡警要打听出谁在替举事的人递信，手里总得有几个钱。` | `以额外的警务开支打击地方秘密组织。` | 恢复原文 | 现有开支用于警务侦缉，原文简洁，免去臆造的线人情节。 |
| `nesnd_india_revolt.1.d` | AI 八股／低 | `[SCOPE.sState('india_case_state').GetName]的反对者已经公开举事。他们占据地方官署，宣布不再服从旧统治者。现在，是否承认这场分离已成为两国之间的争端。` | `[SCOPE.sState('india_case_state').GetName]的反对者占了官署，宣布独立。旧官吏要他们交还印信，门内传出一句话：这地方的公文，今后由我们来签。` | `[SCOPE.sState('india_case_state').GetName]的起义者已经占领地方官署，宣布独立。原统治者仍要求收回该地。` | 局部修订 | 恢复占领官署和宣布独立两件事，直接交代争端。 |
| `nesnd_india_revolt_ack` | AI 八股／低 | `局势已变。` | `把举事的消息传开。` | `通报举事经过。` | 重写 | 以简短公事用语回应通知，去掉口头吩咐。 |
| `nesnd_india_usm_ready_status` | 技术错误／中 | `已可设立天竺宣慰司。` | `直辖的天竺地区已够设司。` | `本国在天竺直辖的地区数已符合设司要求。` | 局部修订 | 明确达标的只是领土条件，保留上轮修复。 |

## nesnd_japan_l_simp_chinese.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_japan_send_terms_requirements` | 技术错误／中 | `吴、日两国均处于和平，未投入外交博弈，且彼此没有停战协定。日本须由丰臣、德川或大和家君主统治，独立或隶属吴朝，完整拥有京都、关东、关西和中国地区。扶国与和国尚未建立。` | `吴、日两国均处于和平，未投入外交博弈，且彼此没有停战协定。日本须由丰臣、德川或大和家君主统治，独立或隶属吴朝，完整拥有京都、关东、关西和中国地区。扶国与和国尚未建立。本州、北海道、九州和四国的日本领地须由日本或吴朝控制。` | `吴、日两国均处于和平，未投入外交博弈，且彼此没有停战协定。日本须由丰臣、德川或大和家君主统治，独立或隶属吴朝，完整拥有京都、关东、关西和中国地区。扶国与和国尚未建立。本州、北海道、九州和四国的日本领地须由日本或吴朝控制。` | 保留上轮稿 | 保留日本领地控制权与三家政权的条件说明。 |
| `nesnd_japan_partition_tt` | 技术错误／中 | `#bold 日本的领土安排#!\n九州与四国的日本领地转交吴朝。德川据江户和北方诸领建立扶国，和国奉天皇统治京都与大阪。丰臣治关西余部、中国地区及原有朝鲜领地。扶、和成为吴朝保护国，丰臣原属国关系保留，原本独立时成为保护国。三家各自宣称由另两家完整控制的分封首府地区。#v EZO、琉球及其他外国领土不受转移。#!` | `#bold 日本的领土安排#!\n九州与四国的日本领地转交吴朝。德川据江户和北方诸领建立扶国，和国奉天皇统治京都与大阪。丰臣治关西余部、中国地区及原有朝鲜领地。扶、和成为吴朝保护国，丰臣原属国关系保留，原本独立时成为保护国。三家各自宣称由另两家完整控制的分封首府地区。#v $EZO$、琉球及其他外国领土不受转移。#!` | `#bold 日本的领土安排#!\n九州与四国的日本领地转交吴朝。德川据江户和北方诸领建立扶国，和国奉天皇统治京都与大阪。丰臣治关西余部、中国地区及原有朝鲜领地。扶、和成为吴朝保护国，丰臣原属国关系保留，原本独立时成为保护国。三家各自宣称由另两家完整控制的分封首府地区。#v $EZO$、琉球及其他外国领土不受转移。#!` | 保留上轮稿 | 保留可解析的虾夷国名引用和原结算条件。 |
| `nesnd_japan_reunification_reason` | 机械性／低 | `海峡两岸的盟约曾替丰臣打开平定诸侯的道路，也让唐土朝廷得以介入日本的继承、封地和征战。城下町的税赋汇往各家府库，军队与商人各认其主。[ROOT.GetCountry.GetName]要重建统一的政府，就须使本州归于一统，并取得自主决定内外政务的地位。` | `海峡两岸的旧盟替丰臣家开过路，也给了唐土朝廷插手封地的由头。如今本州的税各归各家，兵也各听各家号令。[ROOT.GetCountry.GetName]纵能号召诸侯，若连自家的国书都得请外人用印，天下又凭什么归心？` | `丰臣氏曾借唐土朝廷之力平定诸侯。此后，日本诸家的继承、封地与征战，屡有海外势力介入。如今本州的赋税仍分入各家府库，军队各有其主。[ROOT.GetCountry.GetName]要重建统一政权，既须掌握诸藩的兵赋，也须取得独立处理外交的权力。` | 重写 | 恢复原有的海东盟约、兵赋与自主三层内容，取消国书反问。 |
| `nesnd_japan.1.d` | 技术错误／中 | `南京使节带来了分封之议。京都与大阪奉天皇名位，德川以江户为府，丰臣领关西余部与中国地区，九州和四国则归吴朝直辖。海东诸藩的兵力与赋税将从此分属数家。家臣已呈上各地兵力与军粮，等候[ROOT.GetCountry.GetRuler.GetFullName]决定如何答复。` | `南京使节带来了分封之议。京都与大阪奉天皇名位，德川以江户为府，丰臣领关西余部与中国地区，九州和四国则归吴朝直辖。海东诸藩的兵力与赋税将从此分属数家。家臣已呈上各地兵力与军粮，等候裁决。` | `南京使节带来了分封之议。京都与大阪奉天皇名位，德川以江户为府，丰臣领关西余部与中国地区，九州和四国则归吴朝直辖。海东诸藩的兵力与赋税将从此分属数家。家臣已呈报各领可供调遣的兵力与军粮，以备议决。` | 局部修订 | 沿用安全的通用称谓，改清呈报的是各地可用军力。 |
| `nesnd_japan.2.d` | 技术错误／中 | `日本使者未肯接受分封方案。南京若决意东征，就须筹措军饷、调集舰船，扶持三家接管海东诸藩。朝廷也可以撤回要求，让日本保有统一的政府。如何答复，已交由[ROOT.GetCountry.GetRuler.GetFullName]裁定。` | `日本使者未肯接受分封方案。南京若决意东征，就须筹措军饷、调集舰船，扶持三家接管海东诸藩。朝廷也可以撤回要求，让日本保有统一的政府。如何答复，已交由南京朝议裁定。` | `日本使者未肯接受分封方案。南京若决意东征，就须筹措军饷、调集舰船，扶持三家接管海东诸藩。朝廷也可以撤回要求，让日本保有统一的政府。南京朝廷须就此作出答复。` | 局部修订 | 保留南京朝廷为决策者，去除拗口的双重裁决表述。 |
| `nesnd_jp_mining_reason` | AI 八股／低 | `征税和征兵曾是武士的本分，开矿、办厂却要仰仗商人。北方的矿藏给江户带来了新的财源，也带来了旧军府不熟悉的合作者。那些不佩刀的人正在积累财富，并开始要求政府保护他们的生意。` | `江户的武士下乡，从前为的是点丁收税。如今矿口塌了，要找商人垫木料钱。佩刀的人头一次得听听柜台后面那位开些什么条件。` | `征税与征兵向由武士经办，北方铁矿的开采却有赖于商人出资。江户有望从矿业取得新的税源。承担矿场开办费用的商人，也开始要求军府保障他们的经营权。` | 重写 | 以矿业资本、税源与经营权交代武士与商人之间的新关系。 |
| `nesnd_jp_metal_cities_reason` | AI 八股／低 | `城下町原本围着城郭与武士宅邸生长，如今来此谋生的人却越来越多。工人、学徒和小店主住进新街区，他们的孩子也要在这里读书。旧日替领主办事的城镇，正在长成有自己诉求的社会。` | `城下町的街巷原是顺着武士宅子的围墙修的。如今墙外又住满了工人和学徒，等他们的孩子也到了上学的年纪，哪一家肯腾出房子来做学堂？` | `城下町原本围绕城郭与武士宅邸而建。工场兴起以后，工匠、学徒和小商户逐渐在城郊定居。新街区的子弟也需要入学，地方官署须开始为这些迁入的家庭筹办学务。` | 局部修订 | 保留城镇社会的变化与学务需要，省去无依据的借屋设学。 |
| `nesnd_jp_cash_crops_reason` | AI 八股／低 | `海港把远方的价钱带到了乡间。棉田、桑园和茶山有了新的买主，土地所有者与商人都想从中分得更多。农民日复一日的劳作，也开始受到这些遥远市场的支配。` | `收茶的人带着港口的价钱上山时，桑园的主人也会问一句，今年的生丝卖得怎样。农家到秋后才知道，一片叶子在海那边值多少钱，竟能抵掉自家几个月的辛苦。` | `海港的收购商深入乡间，棉花、生丝与茶叶的价格也随海外行情涨落。地主和商人由此扩大销路，种棉、养蚕与栽茶的农家，则越来越依赖收获时的市价。` | 局部修订 | 把农业商业化写成生产者所得与港口行情的关系。 |
| `nesnd_jp_textiles_reason` | AI 八股／低 | `收购生丝与棉花的商人开始把织工集中起来。熟悉的手艺进入了更大的工场，雇工按时领钱，也须服从工头的规矩。对于离开田地的人，这是新的指望。对于商人，这则是把乡村生产握得更紧的办法。` | `商人把生丝和棉花运进工场，来领料的织工也在那里坐下了。从前赶织到半夜，天亮还能歇一晌。如今按日领工钱，连什么时候停梭子，都得听工头的。` | `过去，农户随农时安排纺织，将成布售予商人。如今，经营生丝与棉花的商人开始设立工场，集中雇用织工。离开田地的织工有了按日计付的工资，商人也由收购成品转而直接管理原料供应和工时。` | 重写 | 保留原文中雇佣与生产组织的变化，删去虚构的夜织场景。 |
| `nesnd_jp_consumer_goods_reason` | AI 八股／低 | `食品、家具和日用器皿的生意，正在从少数富户扩展到更多家庭。经营这些工场的人开始关心普通人的收入：顾客若只能勉强糊口，工场便难以扩大销路，产品的价格与收益也会受到压制。` | `做桌椅的木匠过去只等得起大户的生意。如今街上租屋过日子的人多了，谁家不缺一张桌？可米铺若拿走了工钱的最后一文，再好的桌子也只能搁在店里。` | `食品、家具和日用器皿的销路，已经从少数富户扩展到寻常人家。对经营工场的商人而言，米价与工资由此有了新的分量。普通家庭在衣食之外能有多少余款，直接决定着这些工场的生意。` | 局部修订 | 恢复多种日用品与家庭购买力之间的因果关系。 |
| `nesnd_jp_living_standards_reason` | AI 八股／低 | `已经进入工场的人开始盘算房租、米价和孩子读书的钱。他们为城市带来了劳力与税收，也要求从繁荣中得到自己的份额。政府许诺的新生活，终究要落到这些日常开支上。` | `月钱发下来，先扣房租，再留出买米的钱。城里人想送孩子读书，摊开手心一数，剩下的钱可够付先生的束脩？` | `工场的工资养活了越来越多的城市家庭，房租和米价也在消耗他们的收入。对希望子女入学的工人而言，衡量生活是否改善，还要看缴清房租、购足口粮之后，是否仍能负担学费。` | 重写 | 保留房租、粮价和子女教育，以实际购买力解释生活水平。 |
| `nesnd_jp_food_cities_reason` | AI 八股／低 | `粮商带来了买卖，工匠和学徒也跟着留下。新街区需要学校，官府与书商需要纸张。许多过去由乡里宗族包办的事情，开始交到城镇的机构手中。` | `粮船靠岸的地方先有了脚店，又有工匠带着学徒来住。要是住下来的人想送孩子念书，从前村里凑钱延师的那套办法，在码头上该找谁出面？` | `粮食贸易使沿岸集镇日渐繁盛，工匠与学徒也在此定居。过去乡里可以合资延聘教师，如今城中学童渐多，办学须有经常的款项。官署和书商所需的纸张，也为当地工场增添了销路。` | 重写 | 保留商贸、人口聚居、学校和造纸的联系。 |
| `nesnd_jp_cohesion_reason` | AI 八股／低 | `幕府治下的诸藩、乡间的宗族和城下町的商人，曾各自维持着一方秩序。学校与官府把远近的地方联结起来，繁荣的工商业又使更多人的生活休戚相关。百姓能否过得安定，国家能否在战争中保护他们，都在改变人们对共同前途的信心。` | `各藩的孩子渐渐读起同样的书，各地的官吏也认得同一道印信。可到了歉收要开仓、开战要出兵的时候，百姓究竟信本地的老爷，还是信那张盖印的告示？` | `幕府治下，诸藩、宗族与城镇商人各自维持着地方秩序。学校的普及和各地贸易的增长，使百姓的生计逐渐越出藩界。政府能否维持民生，在战时保全疆土，也将影响国民对共同政权的信任。` | 重写 | 恢复多个社会主体与战争、民生的关联，去掉老爷与印信的口语设问。 |
| `nesnd_jp_new_army_reason` | AI 八股／低 | `旧日军队依靠世袭武士与地方关系维持，征募和训练也随各家而异。国家需要有组织的兵员、受过训练的军官和能够听从统一调度的部队。无论以常备军还是国民军承担防务，都应使军事服务于共同的国事。` | `各家的武士认自家的旗号，连点名操练也各有规矩。倘若明日几支人马要合守一个港口，谁带来的枪药，谁听谁的号令？兵册上的这些空白，靠报一个祖传的姓氏填不上。` | `各藩依靠世袭武士维持军队，征募、训练与军需各行其制。无论采用常备军还是国民军，本国要使各地兵力听从统一指挥，首先须确立共同的编制和征募制度。` | 局部修订 | 保留两种建军方案；说明军制整顿涉及的具体权力。 |
| `nesnd_jp_open_diplomacy_reason` | AI 八股／低 | `过去的朝贡和海禁把外交、通商交织在宗主的安排之中。我们需要以本国的名义派遣商船、开放港口，同其他国家商谈彼此的利益。持续的自主将使这些往来有一个可以信赖的政府作为依托。` | `商船过去要借宗主的名义出海。到了异国港口，哪怕是本国货主同当地税吏争一笔税，也得托别人捎话。我们要派自己的使节，让他们认得船尾的旗。` | `过去，宗主借朝贡与海禁掌握了日本对外通商的条件。如今本国有意开放港口，准许商人经营海外贸易。政府须能自行派遣使节，就商船入港和货物待遇与各国交涉。` | 重写 | 保留开港尚属目标的时态，并写明自主对外交涉的用途。 |
| `nesnd_jp_choose_court_desc` | AI 八股／低 | `王朝的号召力可以把旧臣与改制者召到一处。保留君主，任用新官员，让议政与实业为国家带来新的力量。` | `请君主为新法用印。旧臣肯来听宣，商人也想知道往后该照哪条法令纳税。` | `以君主的名义推行新法，使旧臣与主张改制的官员共事于朝。` | 重写 | 君主路线由王权维系新旧官员的合作。 |
| `nesnd_jp_choose_military_desc` | AI 八股／低 | `军队需要统一的指挥，国家也需要能够贯彻到底的政令。支持军官们整顿兵制与军需，把地方的人力和财力用于共同的防务。` | `各藩的兵册既要合在一起，军官就要问，临阵时究竟由谁发令？` | `军官主张将各藩的征募、训练与军需交由军府统辖。` | 局部修订 | 说明军方所要求的权力，免设临阵发令的场景。 |
| `nesnd_jp_choose_representative_desc` | AI 八股／低 | `国事关乎所有纳税、服役和谋生的人。让更多代表参与议政，使官员必须面对公开的讨论，也使国民能够以选票影响政府。` | `税要百姓缴，兵要百姓出，议事时总该给出钱出力的人留个位子。` | `纳税与服役的义务遍及各地，国民理应有权推举代表，参与议政。` | 重写 | 按代议派的政治主张表述，删除席位比喻。 |
| `nesnd_jp_abandon_reform_desc` | 机械性／低 | `撤回当前改革方针，结束政府为新政进行的动员。改革进度归零，#v 24#! 个月内不能重新提出改革。已有法律和建设保留。` | `请把新政的议案收起来。各处已行的法照旧，已开的工照做。这一搁就是 #v 24#! 个月，再要重提，还得从头召集肯出力的人。` | `政府拟搁置现行新政，已颁行的法律和已开办的工程照旧。新政一经搁置，此前的推行进展和连续落实的月数均从零起算。#v 24#! 个月后方可重提改革。` | 重写 | 保留现有法律与工程；明确既有进度及连续月份立即归零，重提须待二十四个月。 |
| `nesnd_jp_mercantile_ports_desc` | 技术错误／低 | `准许商人经营海外买卖，以关税维护国家的收入和本国商业的地位。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_protected_ports_desc` | 技术错误／低 | `开放海路，让工场取得所需的原料，再以关税扶持本国生产者在新市场中的地位。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_political_opposition_desc` | 技术错误／低 | `战争与激进情绪` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。进度条改用战争、激进情绪两条独立明细，旧合并键无调用。 |
| `nesnd_jp_development.2.d` | AI 八股／低 | `新的任官办法已经推行，国家的法令也改变了权力在各阶层间的分配。旧日凭借门第把持地方的人，如今必须面对由政府确定的职位和权限。参与改制的官员、军人和商人，则在新的秩序中寻找自己的位置。这场改革已经进入日常统治，成为处理国事的准则。` | `地方官署换了任命书。旧日凭家名就能坐上的位子，如今得拿出新法上的凭据。有人读罢文书接过印信，也有人读到末行，才明白自己该把印信交出去。` | `新的任官制度已在各地施行。旧日由门第决定的官职，如今须按法令授任，各级官员的职权也有了明文规定。改制之议由此成为地方官署日常奉行的制度。` | 重写 | 恢复任官制度落地的结局，删去虚构的印信交接。 |
| `nesnd_jp_seek_autonomy_desc` | 剧透／低 | `请求宗主放宽对本国的约束，将现有宗属关系提升一个自治等级。\n\n若获同意，双方将有 #v 5#! 年停战期。` | `地方的公文来回渡海，急事也耽误成了旧事。请准我们在本地裁处，使者愿以 #v 5#! 年休兵作保。` | `本国拟请宗主扩大地方政府自行处理内政的权限，并提议双方缔结为期 #v 5#! 年的停战协定。` | 重写 | 写明自治和停战是拟议条款，尚待宗主答复。 |
| `nesnd_jp_seek_independence_desc` | 剧透／低 | `要求宗主解除藩属关系，让本国自行处理内外事务。\n\n若获同意，双方将有 #v 5#! 年停战期。` | `请宗主收回藩属名分。使者带去的国书里另有一条，两国愿约 #v 5#! 年休兵，各守疆界。` | `本国要求宗主承认独立，愿与宗主缔结 #v 5#! 年停战协定。` | 重写 | 保留独立与停战这两项实质请求。 |
| `nesnd_jp_seek_reform_permission_desc` | 机械性／低 | `请宗主认可本国的制度改革，让我们能够自行筹划官员任用、军政与议政的安排。` | `新法即使只在本国施行，宗主若不首肯，谁肯第一个在文书上署名？` | `请宗主认可本国的制度改革，让我们能够自行筹划官员任用、军政与议政的安排。` | 恢复原文 | 原文准确说明须经宗主认可的改制事项，未预告答复。 |
| `nesnd_jp_seek_overlord_capital_desc` | 剧透／低 | `请求宗主拨款兴办工场、培养熟练工匠，使本国的生产能够成长。\n\n获准后，#v 3#! 年内不能再次获得这项资助。` | `工场要置机器，熟手还得从学徒带起。请宗主拨一笔开办款，往后 #v 3#! 年，我们不为同一桩事再登门。` | `请求宗主拨款兴办工场、训练工匠。自获款之日起，本国 #v 3#! 年内不再申请同类资助。` | 局部修订 | 承接已确认的资助口径，保留三年从获款起算。 |
| `nesnd_jp_seek_capital_cne_desc` | 剧透／低 | `以工商业合作为纽带，向北朝争取建设资金，吸引其参与日本的发展。\n\n获准后，#v 3#! 年内不能再次获得这项资助。` | `这份工场用款的账请北朝过目。钱若拨得下来，#v 3#! 年之内，本国自理后续用度。` | `本国拟邀请北朝资助工场建设。若此次拨款获准，今后 #v 3#! 年内不再申请同类资助。` | 重写 | 指明受邀出资者，避免将援助期限误写为此后所有用度均须自理。 |
| `nesnd_jp_seek_capital_hus_desc` | 剧透／低 | `以通商和工业发展为由，向东洲争取一笔用于工场建设的资金。\n\n获准后，#v 3#! 年内不能再次获得这项资助。` | `东洲做海外买卖的人多，懂得工场开张时最费本钱。使者只为开办来筹一笔款，#v 3#! 年以内不来续请。` | `本国拟向东洲申请工场建设经费，以扩充两国的工业品贸易，获款后 #v 3#! 年内不再申请同类资助。` | 重写 | 保留通商理由、工场建设用途与受援间隔。 |
| `nesnd_jp_seek_capital_usm_desc` | 剧透／低 | `[SCOPE.sCountry('nesnd_label_usm').GetName]与日本的商业联系由来已久。我们可以循着这些关系寻求资助，为本国工场筹集资本、培养工匠。\n\n获准后，#v 3#! 年内不能再次获得这项资助。` | `同[SCOPE.sCountry('nesnd_label_usm').GetName]来往的海商熟悉日本工场的底细，请他们带使者去谈开办费。往后 #v 3#! 年，不能指望再开这个口。` | `[SCOPE.sCountry('nesnd_label_usm').GetName]与日本素有通商往来。本国拟请其出资兴办工场、培养工匠，并承诺自获款之日起 #v 3#! 年内不再申请同类资助。` | 重写 | 交代资金用途，并把三年期限准确系于获款之日。 |
| `nesnd_jp_independence_play_desc` | 机械性／低 | `向宗主提出独立的最后通牒，发起独立[concept_diplomatic_play]，准备以战争迫使其接受。` | `使节带去的是最后一封国书。独立的要求若谈不拢，这场[concept_diplomatic_play]就得由军队接手。` | `向宗主发出要求承认本国独立的最后通牒。在这场[concept_diplomatic_play]中，本国将保留诉诸武力的权利。` | 重写 | 保留博弈链接，以最后通牒说明战争可能性。 |
| `nesnd_jp_union_jap_desc` | 剧透／低 | `向[SCOPE.sCountry('nesnd_label_jap').GetName]提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。` | `请[SCOPE.sCountry('nesnd_label_jap').GetName]共议归统。天下的政令该从何处发出，使者得让对方听完这一席话。` | `向[SCOPE.sCountry('nesnd_label_jap').GetName]提出合邦，请其接受本国政府的统一管辖。` | 重写 | 三枚按钮的条款相同，仅受邀国有别。保留动态国名，明示合邦的权力归属。 |
| `nesnd_jp_union_jtk_desc` | 剧透／低 | `向[SCOPE.sCountry('nesnd_label_jtk').GetName]提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。` | `使者带着合邦的国书去见[SCOPE.sCountry('nesnd_label_jtk').GetName]。两家的兵册各管各的日子，还要过多久？` | `向[SCOPE.sCountry('nesnd_label_jtk').GetName]提出合邦，请其接受本国政府的统一管辖。` | 重写 | 三枚按钮的条款相同，仅受邀国有别。保留动态国名，明示合邦的权力归属。 |
| `nesnd_jp_union_jim_desc` | 剧透／低 | `向[SCOPE.sCountry('nesnd_label_jim').GetName]提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。` | `请向[SCOPE.sCountry('nesnd_label_jim').GetName]陈明归统的条件。肯不肯共奉一道政令，还得听对方亲口答复。` | `向[SCOPE.sCountry('nesnd_label_jim').GetName]提出合邦，请其接受本国政府的统一管辖。` | 重写 | 三枚按钮的条款相同，仅受邀国有别。保留动态国名，明示合邦的权力归属。 |
| `nesnd_jp_korean_envoy_desc` | 剧透／低 | `向朝鲜提出归还属地。朝鲜有宗主时由宗主答复。议定后，本国将交还在庆尚道和全罗道所持的州块，并撤销对两地的宣称。` | `庆尚道、全罗道的属地，我们愿意交回朝鲜，两地的宣称也可以一并谈。朝鲜若有宗主，这封国书就得送到宗主手里。` | `本国拟将庆尚道和全罗道的属地归还朝鲜，并撤销对两地的宣称。朝鲜若有宗主，此议须由宗主答复。` | 局部修订 | 属地归还和撤销宣称均属议案；保留有权答复的一方。 |
| `nesnd_jp_foreign.1.d1` | AI 八股／低 | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]希望扩大自行处理国事的权力，要求我们放宽现有宗属关系的约束。使者认为，更大的自主可以让地方政府及时应对国内事务，同时保留两国之间的联系。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者带来一摞须请宗主批复的公文。地方的事等到文书往返才肯办，误了事又算谁的？使者请我们把其中一部分留给当地裁处。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]请求扩大自治权，将部分须经宗主核准的内政事务交由本国政府裁决。` | 重写 | 直接说明来使请求移交的权限，保留宗藩关系。 |
| `nesnd_jp_foreign.1.d2` | AI 八股／低 | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者要求结束藩属关系。他们希望从此自行决定外交、军队与通商事务，并以独立国家的身份同我们往来。这份答复将决定我们是否愿意交出原有的宗主权。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者请求独立。他想要的，是下回再来递交国书时，可以用本国的名义同我们平起平坐。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者要求解除宗藩关系，由本国政府独立行使外交、军事与通商权。` | 重写 | 按来文列明主权事项，删去对下次出使的设想。 |
| `nesnd_jp_foreign.1.d4` | AI 八股／低 | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]正为工场建设寻求一笔资金。使者希望我们拨款，帮助他们扩建生产、培养熟练工匠，以日益兴盛的工商业加深双方的往来。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]递来开办工场的用款单。机器、匠师和学徒的费用都列在纸上，使者唯独拿不出足够的本钱，想请我们拨款。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]请求我国拨款，协助扩建当地工场并培养熟练工匠。` | 局部修订 | 来文只陈明拨款请求和用途，省去未经证实的费用清单。 |
| `nesnd_jp_foreign.1.d7` | AI 八股／低 | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]希望得到我们的许可，同其他日本属国商议归并。他们打算由本国政府主持统一，并承诺只有受邀国家同意才结束其单独统治。我们需要决定是否允许这项合邦计划在现有宗属体系内进行。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者要一封准许合邦的文书。他明白宗主可以点头，却不能替另一位藩主落款。只要我们准他出使，他愿自己去讨那个签押。` | `[SCOPE.sCountry('jp_sender').GetNameNoFormatting]请求宗主授权其与其他日本属国商议合邦。各国是否加入，仍须分别取得其政府的同意。` | 重写 | 区分宗主的交涉许可与受邀国对合邦的批准。 |
| `nesnd_jp_foreign.2.d` | AI 八股／低 | `使者带回了[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的答复。对方已经接受我们的提议，双方将依照商定的安排处理此事。` | `使者回国时，行囊里多了一封[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的复书。末页已经用印，所请照准。` | `[SCOPE.sCountry('jp_partner').GetNameNoFormatting]已复函接受我方提议。` | 重写 | 保留动态答复方，删去行囊、用印与重复的准许。 |
| `nesnd_jp_development.2.d_representative` | AI 八股／低 | `取得选举权的人开始用选票选择代表，报纸也能公开议论政府的行为。官员须面对新的任用办法，而议场内外的争论已经越出旧日少数家族的范围。\n\n新学堂还在把更多人带进这个世界。下一代读书人将怎样运用这些权利，要由他们自己决定。` | `头一批代表入席时，报馆也派了人来。昔日几家人关起门就能定下来的事，如今上午在议场里说了什么，下午选他们来的人就能读到。` | `取得选举权的国民已经开始推举代表，报刊也能公开评论政府的施政。过去限于少数家族之间的政治争议，如今可以提交议会审议。随着新式学校日渐普及，能够阅读法案、参与公共讨论的人也在增多。` | 局部修订 | 兼顾选举、新闻与教育，删除特定报馆当日刊报的虚构情节。 |
| `nesnd_jp_establish_edo_reason` | AI 八股／低 | `江户如今统辖着大片北方领地。驻军可以守住要道，却不能替地方筹办一切政务。军府需要任用办事人员，将税收与支出纳入共同的安排。各地城下町也须容纳商人、工匠与离乡谋生的人。只有这些地方能够支撑日常统治，江户才有余力谋求更大的权利。` | `江户派兵能守住北方的要道，可领粮的军士到了城下，常要跑好几个衙门才找得到经手的人。各地府库究竟收进多少，又从哪一本账里付饷，军府自己先得弄清楚。` | `江户如今统辖大片北方领地。守备各处要道所需的军饷，须由各地征收的赋税维持。军府若要按期供饷，便须任用地方官员，查明各领的岁入与支出，并在城下町建立常设官署。` | 重写 | 用北方守备与财赋说明江户的建制需要。 |
| `nesnd_jp_establish_kyoto_reason` | AI 八股／低 | `京都的公卿与大阪的商人各有自己的交游和利益。朝廷的名位不能直接变成军饷，商人的财富也不会自行成为公用。办理财赋的官员须将现有辖地的收入与政务组织起来，使城市能够供养这个新立的政府。` | `京都的公卿替新朝排好了朝班，大阪的商人却还等着有人来议军饷。朝廷向谁借，拿哪一处的税来还，光抬出天皇的名位还不足以叫人在欠据上署名。` | `京都公卿奉天皇主持朝政，大阪商人掌握着新朝赖以维持的商业财源。两地同属一个政权，驻军与官署的开支也须在同一财政制度下筹措。朝廷眼下需要的是熟悉大阪商情、能与商人议定征税办法的官员。` | 重写 | 以京都政治名位和大阪商业财源交代同一政府的财政问题。 |
| `nesnd_jp_establish_toyotomi_reason` | AI 八股／低 | `分封使丰臣旧臣失去了支配整个日本的地位，留在西部的军队与家臣却仍须供养。各地收入从哪里征收，谁来办理地方政务，都不能只靠旧日的威望维持。政府须在现有辖地建立可靠的行政机关，使城下町成为办事、征税与雇工的中心。` | `丰臣的旧臣还拿着平定天下时的俸单，府库能支用的却只剩西部诸领的收入。城下町的商户若把同一笔税交给了两位家臣，明日还肯认谁的收据？` | `分封之后，丰臣氏向诸藩征调兵赋的旧权已随领土一并缩减，西部诸领仍要供养军队与家臣。厘定各领的税额，任用负责征收的地方官员，是丰臣旧臣眼下必须议定的政务。` | 局部修订 | 保留分封后的财力与既有军政开支，不假定发生重复征税。 |
| `nesnd_jp_mercantile_ports_junior_desc` | 技术错误／低 | `以重商主义取代闭关，准许本国商人经营海外买卖。共同市场的关税仍由市场主导国制定。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_protected_ports_junior_desc` | 技术错误／低 | `改定保护主义贸易法，放开本国口岸。共同市场的关税仍由市场主导国制定。` | 〔键已删除〕 | 〔键已删除〕 | 保留上轮稿 | 沿用已核实的删键结果。开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_jp_foreign.2.d1` | 机械性／低 | `宗主已同意放宽对本国的约束，原有的宗属关系升为更自主的等级。双方议定休兵五年，政府可以据此着手处理此前受制的事务。` | `宗主在来书上准我们多办几件原要请示的国事。使节还带回了一份休战文书，约定双方五年不动兵。` | `宗主已同意扩大本国政府的自治权限。双方同时订立停战协定，期限为五年。` | 局部修订 | 自治权与五年停战均属已达成协议。 |
| `nesnd_jp_foreign.2.d4` | 机械性／低 | `[SCOPE.sCountry('jp_partner').GetNameNoFormatting]同意拨给建设资金。工场扩建与工匠训练有了新的助力。政府须善用这笔资助，三年内不能再获同类拨款。` | `[SCOPE.sCountry('jp_partner').GetNameNoFormatting]答应了这笔拨款。工场可以订机器，也可以招学徒了。使者临行时记得最牢的一句，是对方叮嘱三年之内别再来筹同一笔钱。` | `[SCOPE.sCountry('jp_partner').GetNameNoFormatting]已同意拨付工场建设经费，并资助本国训练工匠。此次拨款获准后，本国三年内不得再申请同类援助。` | 重写 | 保留资金用途和三年条件，以正式答复取代临行叮嘱。 |

## nesnd_journal_closures_l_simp_chinese.yml

| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |
|---|---|---|---|---|---|---|
| `nesnd_journal_closures_parent_cne` | 技术错误／中 | `此项事务随“$ce_cne_land_reform$”一同结束。` | `「$ce_cne_land_reform$」施行期间。` | `「$ce_cne_land_reform$」施行期间。` | 保留上轮稿 | 开启栏准确指明父日志施行期间。 |
| `nesnd_journal_closures_parent_qin` | 技术错误／中 | `此项朝议随“$nesnd_qe1_agenda_journal$”一同结束。` | `「$nesnd_qe1_agenda_journal$」议政期间。` | `「$nesnd_qe1_agenda_journal$」议政期间。` | 保留上轮稿 | 开启栏准确指明朝议期间。 |
| `nesnd_journal_closures_restoration_conclusion` | AI 八股／低 | `本国原有的原住民复国交涉已经结束。` | `本国不再以原先的身份参与复国谈判。` | `本国已退出原有的原住民复国交涉。` | 局部修订 | 指明停止的是原有交涉，也适用于转入武装对抗的情况。 |
| `nesnd_journal_closures_america_conclusion` | AI 八股／低 | `围绕$HUS$的大陆扩张议程已经结束。` | `针对$HUS$的扩张计划就此撤下。` | `本国针对$HUS$的大陆扩张计划已经终止。` | 局部修订 | 保留动态国名，将「撤下」改为计划的正式结案措辞。 |
| `nesnd_journal_closures_india_society_conclusion` | AI 八股／低 | `原有的印度共同认同议程已经结束。` | `各省共同议定印度政体的商谈就此中断。` | `各省共同议定印度政体的商谈就此中断。` | 保留上轮稿 | 说明停止的是各省议定政体的商谈。 |
| `nesnd_journal_closures_india_princes_conclusion` | AI 八股／低 | `原有印度邦国的对外交涉安排已经结束。` | `王公们不能再循旧例遣使了。` | `本国以印度邦国身份开展的对外交涉已经终止。` | 重写 | 邦国身份或领地条件已变，结案不延伸为一切派使活动终止。 |
| `nesnd_journal_closures_india_dynasty_conclusion` | AI 八股／低 | `本国围绕王朝维系政治效忠的议程已经结束。` | `再也无人以这个王朝的名义召集各省。` | `争取各省拥戴印度王朝的政治活动已经中止。` | 重写 | 无论政体还是认同建设发生变化，都只终止这一项政治活动。 |
| `nesnd_journal_closures_india_france_conclusion` | AI 八股／低 | `原有的对法交涉及法国顾问安排已经结束。` | `同法国的交涉中止，顾问团撤离。` | `同法国的交涉中止，顾问团撤离。` | 保留上轮稿 | 结案的两个实际后果为中止交涉及撤离顾问，均已交代。 |
| `nesnd_journal_closures_india_uprising_conclusion` | AI 八股／低 | `原有的起义联络议程已经结束。` | `通往南方举事者的联络断了。` | `本国与南方起义组织的联络已经中断。` | 局部修订 | 以政府与地方组织为行动主体。 |
| `nesnd_journal_closures_japan_cohesion_conclusion` | AI 八股／低 | `原有日本政权主持的国民团结议程已经结束。` | `诸藩与百姓的向背，已由另一个政权面对。` | `原政府维系日本诸地共同认同的政策已经终止。` | 重写 | 国家身份失效不等于必然出现继任政府。 |
| `nesnd_journal_closures_japan_foreign_conclusion` | AI 八股／低 | `原有日本政权的使节交涉已经结束。` | `旧政府派出的使节收回了国书。` | `原日本政权派出的使团已结束交涉。` | 局部修订 | 只陈述外交交涉终止，删去虚构的收回国书。 |
| `nesnd_journal_closures_ottoman_recovery_conclusion` | AI 八股／低 | `奥斯曼复兴政策所维系的军政安排已经结束。` | `奥斯曼旧政府留下的整军办法到此为止。` | `奥斯曼政府的军政复兴计划已告终止。` | 局部修订 | 明确为军政复兴计划，避免把范围缩为整军。 |
| `nesnd_journal_closures_ottoman_unity_conclusion` | AI 八股／低 | `奥斯曼国家原有的团结政策已经结束。` | `维系奥斯曼各地的旧政就此废止。` | `维系奥斯曼各地共同认同的政策已经终止。` | 局部修订 | 明确终止政策的对象，去除笼统的「旧政」。 |
| `nesnd_journal_closures_qin_court_conclusion` | AI 八股／低 | `皇族、士人与军队之间原有的朝议安排已经结束。` | `皇族、士人与军方不再共议国事。` | `皇族、士人与军方不再共议国事。` | 保留上轮稿 | 保留上轮稿。结案行已写明三方停止的政治活动。 |
| `nesnd_journal_closures_qin_unity_conclusion` | AI 八股／低 | `维系西秦诸地共同认同的旧有安排已经结束。` | `朝廷已无力再把西秦诸地统在一起。` | `西秦朝廷已停止维系各地共同认同的政策。` | 重写 | 结案涉及共同认同政策，不能由此断言朝廷已失去一切统治能力。 |

## 上轮英文需同步清单

原报告所列 83 键完整保留，供后续翻译使用。本次英文返工仅涉及上轮实际改过的句子。

- `nesnd_france_court.1.growth`
- `nesnd_france_court.1.paris`
- `nesnd_france_court.1.provinces`
- `nesnd_court_figures`
- `nesnd_india_reform_reason`
- `nesnd_india_schools_reason`
- `nesnd_india_princes_reason`
- `nesnd_india_princes_status`
- `nesnd_india_unified_reason`
- `nesnd_india_priority_desc`
- `nesnd_india_settlement_desc`
- `nesnd_tianzhu_governance_reason`
- `nesnd_establish_yuanshan_desc`
- `nesnd_india_foreign_reason`
- `nesnd_india_foreign_status`
- `nesnd_india_diplomatic_desc`
- `nesnd_india_diplomacy.1.d`
- `nesnd_india_diplomacy.2.d`
- `nesnd_india_diplomacy.3.d`
- `nesnd_india_diplomacy.1.d1`
- `nesnd_india_diplomacy.1.d2`
- `nesnd_india_diplomacy.1.d3`
- `nesnd_india_diplomacy.1.d4`
- `nesnd_india_diplomacy.1.d6`
- `nesnd_india_diplomacy.1.d7`
- `nesnd_india_revolt_war_reason`
- `nesnd_india_suppression_desc`
- `nesnd_india_revolt.1.d`
- `nesnd_india_revolt_ack`
- `nesnd_japan_reunification_reason`
- `nesnd_jp_mining_reason`
- `nesnd_jp_metal_cities_reason`
- `nesnd_jp_cash_crops_reason`
- `nesnd_jp_textiles_reason`
- `nesnd_jp_consumer_goods_reason`
- `nesnd_jp_living_standards_reason`
- `nesnd_jp_food_cities_reason`
- `nesnd_jp_cohesion_reason`
- `nesnd_jp_new_army_reason`
- `nesnd_jp_open_diplomacy_reason`
- `nesnd_jp_choose_court_desc`
- `nesnd_jp_choose_military_desc`
- `nesnd_jp_choose_representative_desc`
- `nesnd_jp_abandon_reform_desc`
- `nesnd_jp_development.2.d`
- `nesnd_jp_seek_autonomy_desc`
- `nesnd_jp_seek_independence_desc`
- `nesnd_jp_seek_reform_permission_desc`
- `nesnd_jp_seek_overlord_capital_desc`
- `nesnd_jp_seek_capital_cne_desc`
- `nesnd_jp_seek_capital_hus_desc`
- `nesnd_jp_seek_capital_usm_desc`
- `nesnd_jp_independence_play_desc`
- `nesnd_jp_union_jap_desc`
- `nesnd_jp_union_jtk_desc`
- `nesnd_jp_union_jim_desc`
- `nesnd_jp_korean_envoy_desc`
- `nesnd_jp_foreign.1.d1`
- `nesnd_jp_foreign.1.d2`
- `nesnd_jp_foreign.1.d4`
- `nesnd_jp_foreign.1.d7`
- `nesnd_jp_foreign.2.d`
- `nesnd_jp_development.2.d_representative`
- `nesnd_jp_establish_edo_reason`
- `nesnd_jp_establish_kyoto_reason`
- `nesnd_jp_establish_toyotomi_reason`
- `nesnd_jp_foreign.2.d1`
- `nesnd_jp_foreign.2.d4`
- `nesnd_journal_closures_restoration_conclusion`
- `nesnd_journal_closures_america_conclusion`
- `nesnd_journal_closures_india_society_conclusion`
- `nesnd_journal_closures_india_princes_conclusion`
- `nesnd_journal_closures_india_dynasty_conclusion`
- `nesnd_journal_closures_india_france_conclusion`
- `nesnd_journal_closures_india_uprising_conclusion`
- `nesnd_journal_closures_japan_cohesion_conclusion`
- `nesnd_journal_closures_japan_foreign_conclusion`
- `nesnd_journal_closures_ottoman_recovery_conclusion`
- `nesnd_journal_closures_ottoman_unity_conclusion`
- `nesnd_journal_closures_qin_court_conclusion`
- `nesnd_journal_closures_qin_unity_conclusion`
- `nesnd_france_court.1.marked`
- `nesnd_india_uprising_reason`

另记法国王党正文 `nesnd_court_royal_reason`。审核前英文称外省厂主亲自到场，确认的中文稿采用商会代表陈情。该英文人物叙述位于上轮未改过的句子，本轮仅修订上轮触及的结尾，人物称谓留待翻译同步。

## 游戏外检查与实机抽查

以审核基线逐字节重放改动，核对键集合、UTF-8 BOM、语言头、引号、动态函数、嵌套引用、数字与颜色，以及 10 条批准稿和 16 条已删记录。未启动游戏。

- 印度「诸邦之间」及「借法自强」：对照自治、独立、合邦来文，核对王公年金和土地、人民的管辖权。
- 印度「南方的烽火」：依次悬停联络、暂停、恢复与举事，共用描述应适用于四种操作。
- 日本「东洋交涉」：比较自治、独立、合邦和对外求援；停战与拨款期限在提案和答复中的时态应有区别。
- 日本「机杼声中」：阅读工场雇佣与农户织造的叙述；对照同组「富足的生活」中的房租、米价和教育费用。
- 法国「宫廷与外省」：核对王党或摄政期间的工程理由，再看五年评议对疆界可比州的统计与两档威望奖励。

在本目录运行 `python rework.py report` 可由同目录的 `records.json` 重新生成报告。
