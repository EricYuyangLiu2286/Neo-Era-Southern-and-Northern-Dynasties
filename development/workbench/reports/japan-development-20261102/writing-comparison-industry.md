# 日本产业与团结：实际契约逐键编辑对照

2026-11-02。只写报告与文本JSON；未改候选或主MOD，未开游戏。对象为 `WORK/exports/japan-development-20261102-a`，报告内SHA固定本次读入版本。

结论：本表全部键已逐条完成中英编辑对照，判定仅为 **编辑通过，待装配**。它不表示候选有效覆盖层已装入这些文字，不表示显示/引擎验收通过。JSON为 `{key:{zh,en}}`，无脚本改动；江南高团结键是根任务已同意接入的额外条件分支。

## 原作者样本与来源

A1–A3的原始路径、25条完整样本与SHA，见[作者来源研究](writing-source-study.md)。已逐字匹配原始提交 `f18b6c45525351f5bf1a86ab29cccff9fee49500`，未用当前AI新增文本充当作者样本。

|类别|原作者原句/字段|本轮用法|
|---|---|---|
|标题|A1:331“挣脱巨龙”、336“炎夏”|短标题点出实物、政治局面或生活，不以内部阶段编号命名。|
|经济正文|A2:69“随着旧宗族和土地不再能锁住农民……从郊野涌入城市。”|生产、人口流动和生活形成因果；产业理由不写建设检查流程。|
|经济日志|A2:34“战争和社会革命……地方经济的野蛮生长……内贸失调。”|具体经济关系解释持续问题，不在正文列完成条件。|
|政治正文|A2:20“武勋贵族集团……新派士绅……愿意对社会下层让利以自保。”|团结从地方力量与生活利益解释，不把社会变动写成无主语的数值运算。|
|政治立场|A3:237“革命君主制和拿破仑的宪政……”|作者允许明确立场；不要求每段插一个匿名反对者或反复提醒代价。|
|修正|A2:74“投资狂热”|简明状态名；实际效果由引擎列出，名字不冒称未实现的贸易/出口。|
|规则/进度|A3:249使用`JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)`|精确的数值留在原生bar/必要提示，与故事分字段。|

N1为前报告原版英文`content_1_l_english.yml:686`。N5:467是当前本体fascism_progress_bar_desc，读数使用`[JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|1]/100`；本轮只保留当前值/总值。N6:128为`GetCulture('yankee').GetName`现行本体示例，支持高团结提示使用固定文化数据库对象，避免无效人物/国家scope。中文japanese目前由本体显示为“大和”，所以采用`GetCulture`，不擅改为未定义译名。

## 当前源码指纹

|ID|文件|SHA-256|
|---|---|---|
|C-JE|[nesnd_jp_industry.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_jp_industry.txt>)|`76475ab54da367f9fd07e4767dee049b5699539061e3934a548ab4a63f2a14ce`|
|C-COH|[nesnd_jp_cohesion.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_jp_cohesion.txt>)|`25875a499fdc309cee97f4a52c8ca3d2bde8b998ec6714934e68e88a700aebfc`|
|C-EFF|[nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_effects/nesnd_jp_development.txt>)|`8ab3a273c45dc0a6b34506ad27800b0d58ce12caa6314bace435aa45395bd416`|
|C-VAL|[nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/script_values/nesnd_jp_development.txt>)|`c16d4e119a4159b5e0b95405062a20c141ddea5380e9875f8d7746cf7d45781e`|
|C-BAR|[nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_progress_bars/nesnd_jp_development.txt>)|`3be517ca466ca2e9bed8ca82db5dbcea235eca1997c55551f276642c7d22fc1e`|
|C-MOD|[nesnd_jp_industry.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/static_modifiers/nesnd_jp_industry.txt>)|`4011d679679eaff718da8ce9a06b7a34f1a1c37547f01f1ff06bd36196a8684c`|
|C-MOD2|[nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/static_modifiers/nesnd_jp_development.txt>)|`aae2be57dfb92473418bf3f4aec7b4936c5f93d2da43d209052dbc04f86c6f00`|
|C-TRIG|[nesnd_jp_industry.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_industry.txt>)|`f9a77c913591fff3ab0db90d060e8a58db637b8e26a201477e1eeef27e0476e4`|
|C-TRIG2|[nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_development.txt>)|`6ce0673f4f8b07d63fb2558838119df8b2e743299b32e435ed06665f03aaba9b`|
|C-IND-EFF|[nesnd_jp_industry.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_effects/nesnd_jp_industry.txt>)|`ebfe9d23455989086830832eff9c7cc629d664c5c4f541eaa46e2b5d8e03cfc7`|
|C-IND-VAL|[nesnd_jp_industry.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/script_values/nesnd_jp_industry.txt>)|`e1fea205c982fc65ce84ebd9d81b6dcec8c413168d71bfbaf1482fbc0a383270`|
|N5|[content_104_l_english.yml](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/content_104_l_english.yml>)|`b1773ec14d7efbff8eac19d5f961ebb784d6f1f1fe697f3a8e038968e5d46038`|
|N6|[acw_text_l_english.yml](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/acw_text_l_english.yml>)|`f367e2117d2fe88f6abdb132795f6bc664bd8d4c57a1cc720dbafbbdc8a0ccc8`|

## 从未接入草稿到实际键的返工

- 原草稿I-W1“京都的居民与大阪的商民……”及标题“两京的生计”返工：当前入口是JIM身份，没有同时持有两城的条件。改为“城市的生计”；既有事实不再假定永远持有两城。
- 原草稿I-W2“京都是朝廷所在……”及“朝廷与商都”返工：JIM政治后续可改变且当前产业入口不要求君主制。改为“商都的成长”，具体写学校、纸张和城市。
- 原草稿I-S2“织工却仍受制于狭小的作坊”返工：已有纺织厂并不排除阶段出现。改写为现有贸易与工场扩张的机会。
- 原草稿I-S4的“丰臣政府”改为“政府”，避免JAP改政体后仍假称丰臣在位。
- 原草稿I-F3道路、学校、官府并列收紧为城市和学校的关系，避免让玩家误认额外必做目标。
- 食品修正内部键含exports、数个产业修正含trade，实际没有出口/贸易协定效果；中文与英文均以实际产业状态命名。
- 高团结正文不塞概率；仅高值状态显示一次必要机制。根任务已同意高团结先判江南政策，然后落到大和默认分支。

## 全键对照与逐条决定

下列每行同时检查用词、断句、造句、冗余、视角与脚本契约；状态与效果不预告未发生事件。所有英文均为完整英文，动态表达和数字与中文一致。

|键/类别|作者或原生对照|本轮中文候选|本轮英文候选|决定与契约|
|---|---|---|---|---|
|`nesnd_jp_mining`<br>日志标题|A1:331、336；A2:34、69；N1:686|山中的铁矿|Iron in the Hills|编辑通过。保留矿冶主题；补实际煤矿与伐木目标。不称煤矿储量丰富，不将钢铁/工具奖励误写成矿业增产。|
|`nesnd_jp_mining_reason`<br>日志正文|A2:34、69；N1:686|北方的矿山与林场为德川氏提供了兴办工业的根基。铁矿、煤炭和木材沿着商路进入工场，才能变成更好的工具和新式武备。军府需要鼓励这门生意，使矿业能够长期供养正在成长的制造业。|The mines and forests of the north give the Tokugawa a foundation for industry. Iron, coal and timber must reach the workshops before they can become better tools and modern weapons. The government must encourage this trade so that the mines can sustain a growing manufacturing sector.|编辑通过。保留矿冶主题；补实际煤矿与伐木目标。不称煤矿储量丰富，不将钢铁/工具奖励误写成矿业增产。|
|`nesnd_jp_arsenals`<br>日志标题|A1:331、336；A1:150；A2:69|兵工与船坞|Arsenals and Shipyards|编辑通过。保留具体生产链。未要求与吴签合同，故不声称已向吴供货或吴必定采购。|
|`nesnd_jp_arsenals_reason`<br>日志正文|A1:150；A2:69|军队需要枪炮，沿海交通和海防需要船只。矿石经过钢厂冶炼，再由工具厂、兵工厂和船坞加工，才能成为国家可以依靠的力量。稳定的订单将使工匠和商人敢于扩建这些工场。|Armies need weapons, while coastal trade and defence depend on ships. Ore must pass through steelworks, tool workshops, arsenals and shipyards before it can strengthen the country. Steady orders will give craftsmen and merchants reason to expand their works.|编辑通过。保留具体生产链。未要求与吴签合同，故不声称已向吴供货或吴必定采购。|
|`nesnd_jp_metal_cities`<br>日志标题|A1:331、336；A2:69|城下町的变迁|Beyond the Castle Town|编辑通过。返工草稿的道路/官府并列清单，围绕实际城市与学校目标；不复述等级、州数。|
|`nesnd_jp_metal_cities_reason`<br>日志正文|A2:69|铁矿、兵工厂和船坞正在改变北方的城下町。前来谋生的工人需要住房和粮食，新的工场也需要懂得技术的人手。扩大的城市与普及的学校将培养这些人才，使地方的繁荣成为国家长久的力量。|Mines, arsenals and shipyards are changing the castle towns of the north. Workers arriving in search of wages need homes and food, while new factories need people with technical knowledge. Growing towns and wider schooling can provide these skills and give lasting strength to the country.|编辑通过。返工草稿的道路/官府并列清单，围绕实际城市与学校目标；不复述等级、州数。|
|`nesnd_jp_cash_crops`<br>日志标题|A1:331、336；A2:15、34、69|棉田、桑园与茶山|Cotton, Silk and Tea|编辑通过。移除桑国固定领土断言；列三类商业作物不宣称须全部达标，任二条件交原生勾叉。|
|`nesnd_jp_cash_crops_reason`<br>日志正文|A2:15、34、69|棉花、生丝与茶叶已经把乡间的生产同远方的市场联结起来。商人收购原料，农民则越来越关心作物能够卖出怎样的价钱。扩大的工商业将为这些出产寻找销路，也使土地上的劳动获得新的用途。|Cotton, raw silk and tea connect rural production with distant markets. Merchants buy the produce, while farmers pay closer attention to the prices their crops command. Growing commerce and industry can find new buyers and new uses for the work of the countryside.|编辑通过。移除桑国固定领土断言；列三类商业作物不宣称须全部达标，任二条件交原生勾叉。|
|`nesnd_jp_textiles`<br>日志标题|A1:331、336；A2:69|机杼声中|The Sound of the Looms|编辑通过。返工“仍受制于狭小作坊”的无条件现状；已有纺织厂仍适用，不预设没有机器。|
|`nesnd_jp_textiles_reason`<br>日志正文|A2:69|棉花和生丝经商人之手运往各地，纺织业也因此有了扩张的余地。更多原料可以留在本国加工，熟练的织工则能带着自己的手艺进入更大的工场。这门生意将给离开田地的人们提供另一种生计。|Merchants carry cotton and raw silk to markets near and far, creating room for the textile industry to expand. More of this produce can be processed at home, with skilled weavers bringing their craft into larger mills. The industry can offer another livelihood to people leaving the fields.|编辑通过。返工“仍受制于狭小作坊”的无条件现状；已有纺织厂仍适用，不预设没有机器。|
|`nesnd_jp_consumer_goods`<br>日志标题|A1:331、336；A2:69|百姓的买卖|Goods for the People|编辑通过。保留消费和就业因果，食品/家具/玻璃对应实际类别；不追加无关财政风险。|
|`nesnd_jp_consumer_goods_reason`<br>日志正文|A2:69|有了稳定的收入，工人和店主便会购买更好的食品、家具和日用器皿。工商业的兴盛需要这许多普通人参与其中，让家庭的开支养活更多工场，也让工场的工资回到市面。|With steady incomes, workers and shopkeepers can buy better food, furniture and household goods. Their spending sustains new workshops, whose wages in turn support the shops. A wider market for everyday goods will give industry roots throughout the country.|编辑通过。保留消费和就业因果，食品/家具/玻璃对应实际类别；不追加无关财政风险。|
|`nesnd_jp_living_standards`<br>日志标题|A1:331、336；A2:69|富足的生活|A Better Living|编辑通过。保留民生主题；删丰臣在位前提；12个月只写必要条件提示，未承诺奖励直接增加生活水平。|
|`nesnd_jp_living_standards_reason`<br>日志正文|A2:69|新工场已经吸引人们离开乡村，城市也因他们的劳动而兴旺。政府许诺的繁荣，应当见于百姓的衣食与居所。学校将为他们的子女打开新的道路，而长久改善的生活才能使这些家庭在城市中安顿下来。|New workshops have drawn people from the countryside, and their labour has helped the towns prosper. The prosperity promised by the government should be visible in their food, clothing and homes. Schools can open new paths for their children, while lasting improvements in daily life allow these families to settle in the towns.|编辑通过。保留民生主题；删丰臣在位前提；12个月只写必要条件提示，未承诺奖励直接增加生活水平。|
|`nesnd_jp_food_supply`<br>日志标题|A1:331、336；A2:34、69；D九.2|城市的生计|Feeding the Towns|编辑通过。返工“两京”固定地理断言：当前入口仅TAG JIM。认可生产或市场价格两路，不承诺全国自给或直接改变市场价格。|
|`nesnd_jp_food_supply_reason`<br>日志正文|A2:34、69；D九.2|城里的居民依靠田间、海上和商船送来的粮食生活。丰收与贸易可以共同充实市场，让人们买得起一日所需。稳定的供给也使工匠和工人能够留在城镇，为更多产业谋求生计。|Townspeople depend on food brought from the fields, the sea and merchant ships. Harvests and trade can together keep markets supplied and daily necessities within reach. Reliable food supplies also allow craftsmen and workers to remain in the towns and make their living in new industries.|编辑通过。返工“两京”固定地理断言：当前入口仅TAG JIM。认可生产或市场价格两路，不承诺全国自给或直接改变市场价格。|
|`nesnd_jp_food_cities`<br>日志标题|A1:331、336；A2:69|商都的成长|The Growth of the Towns|编辑通过。返工“朝廷与商都”：JIM共和制或丢京都仍可进入。加入纸张与学校的社会用途，对应真实纸厂和学校条件。|
|`nesnd_jp_food_cities_reason`<br>日志正文|A2:69|粮食供应安定之后，更多人能够在城镇中靠手艺和买卖生活。商人、学徒和工匠的子女需要学校，官府与书市则不断扩大对纸张的需求。这些城市将把地方的物产与人力聚集起来，成为工商发展的根基。|With reliable food supplies, more people can earn a living through crafts and trade. The children of merchants and craftsmen need schools, while public offices and booksellers create a growing demand for paper. These towns can bring local produce and labour together to support further industry.|编辑通过。返工“朝廷与商都”：JIM共和制或丢京都仍可进入。加入纸张与学校的社会用途，对应真实纸厂和学校条件。|
|`nesnd_jp_food_processing`<br>日志标题|A1:331、336；A2:69；D九.2|粮食入市|Food for the Towns|编辑通过。保留粮食加工和城市人口因果；技术目标是罐头，但正文用尚待发展的保存方法，不无条件宣布已出口或建成海外市场。|
|`nesnd_jp_food_processing_reason`<br>日志正文|A2:69；D九.2|城镇人口的增长扩大了对加工食品的需求。新的保存方法能够让粮食与鱼获运到更远的市场，供养更多脱离田地的劳动者。商人和工场将从这门生意中获得收入，城市也因此有了更稳固的经济基础。|Growing towns need more processed food. New preservation methods allow grain and fish to reach more distant markets and support more workers away from the land. Merchants and factories can profit from this trade, giving the towns a firmer economic foundation.|编辑通过。保留粮食加工和城市人口因果；技术目标是罐头，但正文用尚待发展的保存方法，不无条件宣布已出口或建成海外市场。|
|`nesnd_jp_living_year`<br>必要条件提示|A3:249；C-JE:135、143–145|已连续 #v 12#! 个月达到生活水平、学校和城市目标|The living standard, school and urban development goals have been met for #v 12#! consecutive months|编辑通过。实际按月ready检查，任何一月不合格归零；一次说明持续期，不重复其他条件数字。|
|`nesnd_jp_metal_foundries`<br>产业修正|A2:74 投资狂热；C-MOD|金属工业扩张|Metalworking Expansion|编辑通过。钢铁和工具吞吐各+10%，名称不误称矿业收益。|
|`nesnd_jp_arsenal_towns`<br>产业修正|A2:74 投资狂热；C-MOD|兵工与船业繁荣|Arsenals and Shipyards Flourish|编辑通过。枪械与造船吞吐各+15%，不承诺额外采购或舰队。|
|`nesnd_jp_industrial_cities`<br>产业修正|A2:74 投资狂热；C-MOD|工业城市兴盛|Flourishing Industrial Towns|编辑通过。行政力倍率与教育可及性，名称不暗加道路或铁路。|
|`nesnd_jp_cash_crop_trade`<br>产业修正|A2:74 投资狂热；C-MOD|经济作物兴盛|Cash Crop Expansion|编辑通过。棉丝茶吞吐；不把内部trade键译成未实现的贸易条约。|
|`nesnd_jp_textile_trade`<br>产业修正|A2:74 投资狂热；C-MOD|纺织业兴盛|Textile Expansion|编辑通过。仅纺织吞吐，不宣称提高关税或固定外销。|
|`nesnd_jp_consumer_trade`<br>产业修正|A2:74 投资狂热；C-MOD|日用工业兴盛|Flourishing Consumer Industries|编辑通过。食品、家具、玻璃吞吐，与阶段目标一致。|
|`nesnd_jp_towns_prosper`<br>产业修正|A2:74 投资狂热；C-MOD|富足的城镇|Prosperous Towns|编辑通过。奖教育可及性和威望，名称是已达生活目标的状态，不声称加SOL。|
|`nesnd_jp_rural_markets`<br>产业修正|A2:74 投资狂热；C-MOD|农渔业兴旺|Farming and Fishing Prosper|编辑通过。稻米和渔业吞吐，不误称直接降低粮价。|
|`nesnd_jp_growing_cities`<br>产业修正|A2:74 投资狂热；C-MOD|城市扩展|Growing Towns|编辑通过。城市中心吞吐与教育可及性，不声称自动增加城市等级。|
|`nesnd_jp_food_exports`<br>产业修正|A2:74 投资狂热；C-MOD|食品加工业兴盛|A Flourishing Food Industry|编辑通过。食品吞吐与行政力；删未实现的出口含义。|
|`nesnd_jp_cohesion`<br>常驻日志标题|A3:237；D九.4|国民团结|National Cohesion|编辑通过。沿用已定团结名称，不命名为文化转换任务。|
|`nesnd_jp_cohesion_reason`<br>常驻日志正文|A2:15、20、69；A3:237|幕府治下的诸藩、乡间的宗族和城下町的商人，曾各自维持着一方秩序。学校与官府把远近的地方联结起来，繁荣的工商业又使更多人的生活休戚相关。百姓能否过得安定，国家能否在战争中保护他们，都在改变人们对共同前途的信心。|The domains of the shogunate, rural clans and merchants of the castle towns once upheld their own local orders. Schools and public administration connect distant communities, while flourishing commerce ties more livelihoods together. Security at home and the country’s fortunes in war shape confidence in a shared future.|编辑通过。以地方利益、学校、行政、生活、战争解释共同信任；不塞文化公式，不宣告已统一或必然国家解体。|
|`nesnd_jp_cohesion_bar_name`<br>原生进度条名|A3:248；C-BAR:2|国民团结|National Cohesion|编辑通过。常驻状态名称，不写通关进度。|
|`nesnd_jp_cohesion_bar_desc`<br>原生进度条读数|A3:249；N5:467；C-BAR:4|#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100|#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100|编辑通过。采用原生JournalEntry/ScriptedProgressBar.Self上下文；只显示当前值/100，不重复百分比。|
|`nesnd_jp_cohesion_order_desc`<br>原生进度来源|A3:249；C-VAL|政府威信|Government Authority|编辑通过。合法性决定正负增减。 原生条显示实际数值，标签不重复公式。|
|`nesnd_jp_cohesion_living_desc`<br>原生进度来源|A3:249；C-VAL|民生与财政|Living Conditions and Public Finances|编辑通过。含生活水平、月度升降与破产，名称覆盖全部实际来源。 原生条显示实际数值，标签不重复公式。|
|`nesnd_jp_cohesion_learning_desc`<br>原生进度来源|A3:249；C-VAL|学校与行政|Schools and Administration|编辑通过。对应学校机构与行政力正负。 原生条显示实际数值，标签不重复公式。|
|`nesnd_jp_cohesion_conflict_desc`<br>原生进度来源|A3:249；C-VAL|内忧与外患|Unrest and Conflict|编辑通过。含激进化、战争、久战与外交羞辱。 原生条显示实际数值，标签不重复公式。|
|`nesnd_jp_cohesion_victory_desc`<br>原生进度来源|A3:249；C-VAL|战争胜负|Military Victories and Defeats|编辑通过。同时含胜利加分与败战减分，不单称胜利。 原生条显示实际数值，标签不重复公式。|
|`nesnd_jp_cohesion_doubt`<br>条件式状态|A2:20；C-COH:13；C-MOD2|民众对政府失去信任，地方分歧正在扩大。|Public trust in the government is faltering, and local divisions are deepening.|编辑通过。只陈述低团结与其社会压力，不预报未实现的起义、解体或自动三分。|
|`nesnd_jp_cohesion_calm`<br>条件式状态|A2:20；C-COH:15|各地仍能维持共同的秩序。|The regions continue to uphold a common political order.|编辑通过。中间区间的简短状态，不复述门槛或假称必然繁荣。|
|`nesnd_jp_cohesion_confident`<br>高团结状态与必要效果提示|C-EFF:39–68；C-VAL:3–8；N6:128|国民对共同前途的信心正在促进文化融合。<br>每月有 #v 30%#! 的概率，在一个合格的本国[concept_state]中，使至多相当于该州总人口 #v 10%#! 的人口同化为[GetCulture('japanese').GetName]文化；宗教不变。|Confidence in a shared future encourages cultural assimilation.<br>Each month, there is a #v 30%#! chance for people in one eligible owned [concept_state] to adopt [GetCulture('japanese').GetName] culture, up to #v 10%#! of that state's total population. Religion remains unchanged.|编辑通过。高团结才显示；本国每月一次抽取，一个本国州，总人口10%上限，准确目标文化；宗教仅此处一次说明。 默认分支仅用于未施行江南政策者。|
|`nesnd_jp_cohesion_confident_jiangnan`<br>高团结状态与必要效果提示|C-EFF:39–68；C-VAL:3–8；N6:128|国民对共同前途的信心正在促进文化融合。<br>每月有 #v 30%#! 的概率，在一个合格的本国[concept_state]中，使至多相当于该州总人口 #v 10%#! 的人口同化为[GetCulture('ce_wuu').GetName]文化；宗教不变。|Confidence in a shared future encourages cultural assimilation.<br>Each month, there is a #v 30%#! chance for people in one eligible owned [concept_state] to adopt [GetCulture('ce_wuu').GetName] culture, up to #v 10%#! of that state's total population. Religion remains unchanged.|编辑通过。高团结才显示；本国每月一次抽取，一个本国州，总人口10%上限，准确目标文化；宗教仅此处一次说明。 根任务已同意江南分支优先接入；当前文件尚需增加该status引用。|
|`nesnd_jp_divided_councils`<br>团结修正|A2:19、74；C-MOD2|人心离散|A Divided Society|编辑通过。合法性下降与动乱效果上升，不误称已发生内战。|

## 完成边界与装配注意

本次共 **45个键**：10个产业JE标题与10个reason、10个产业修正、1个12个月条件提示；团结标题/reason、进度条名/读数、5项来源、4个条件状态、1个团结修正。没有新增未被请求的按钮、goal或触发器说明。

`nesnd_jp_cohesion_confident_jiangnan`必须先于默认高团结分支使用；两者互斥，宗教不变只会在当前高团结状态出现一次。根任务已明确采用两个分支。本报告不自行修改候选。

当前源码与计划尚有实现差别：工业入口仍按JTK/JAP/JIM固定分链，正文没有宣称补充链已经开放；朝廷与两京条件没有写入脚本，故本稿删去相应常驻断言。这些是实际适用边界，不用文案掩盖机制差别。

生活改善按每月`nesnd_jp_living_standards_ready`累计，未达归零；该提示准确说明12个连续月。其余建筑、学校、城市、产能与收益数字由原生条件和修正显示，没有重复抄入reason。

文化转换读入代码：每个国家月度一次`random_list`的30/70，成功才`random_scope_state`；转换比例快照为`min(1,0.1/(1-目标文化占比))`，对州内非目标pop应用，因而上限为州总人口10%。文本不把它说成非目标人口的10%、每州各抽30%或全国10%。仅见`change_pop_culture`，未见宗教变更。

装配后仍需根任务检查最终引用闭包、YAML转义、覆盖层和脚本SHA变化。未运行引擎，未检查游戏画面。
