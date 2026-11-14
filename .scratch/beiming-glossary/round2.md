# 北明与大革命词条：第二轮交付

2026-11-12。依据作者答复 [author-decisions-20261112.md](author-decisions-20261112.md)（原文照录）。未启动游戏。验证等级 **STATIC_PASS**，游戏内显示未验证。

## 新增

| 文件 | 内容 |
|---|---|
| [common/glossary/nesnd_beiming_glossary.txt](../../common/glossary/nesnd_beiming_glossary.txt) | 15 条 `glossary_nesnd_* = {}` |
| [localization/simp_chinese/replace/nesnd_beiming_glossary_l_simp_chinese.yml](../../localization/simp_chinese/replace/nesnd_beiming_glossary_l_simp_chinese.yml) | 30 个键：每条一个标题、一个 `_desc` |
| [localization/english/replace/nesnd_beiming_glossary_l_english.yml](../../localization/english/replace/nesnd_beiming_glossary_l_english.yml) | 同上，英文 |

词条（括号内为键名后缀）：

- **北明组：** 北明 Northern Ming（beiming），北明战国世 Northern Ming Warring States（beiming_zhanguoshi），塞王之乱 Rebellion of the Frontier Princes（saiwang_rebellion），藩镇 Military Fiefs（fanzhen），中原大战 Central Plains Wars（central_plains_wars），联军体系 Coalition Order（coalition_order），灭明战争 Overthrow of the Ming（overthrow_of_ming）。
- **大革命组：** 中华大革命 Chinese Great Revolution（chinese_revolution），蓝田哗变 Lantian Mutiny（lantian_mutiny），长安起义 Chang’an Uprising（changan_uprising），西秦大革命 Western Qin Great Revolution（western_qin_revolution），鼓楼结社 Drum Tower Society（gulou_society），牧仲棠东征 Eastern Campaigns of Mu Zhongtang（eastern_campaigns），南征 Southern Campaign（southern_campaign），扬州条约 Treaty of Yangzhou（treaty_of_yangzhou）。

与第一轮相比：

- 新增“北明战国世”（A10）和“长安起义”两条。长安起义用来放你补充的起义经过，西秦大革命一条因此只写起义之后的元老执政与青年派夺权。
- 东征更名为牧仲棠东征（A5）。联军体系改用南军、北军和你给的全称（A6）。
- 所有“西安”都改成了长安。秦皇写作陈炯，被革命军绞死于长安王宫。第六次中原大战写作1800年开战，1810年仍在进行。
- 中华大革命一句按你的原话改写。蓝田哗变按你的原文压缩，原文全文保存在 author-decisions 文件里。
- 嵌套链接只从主条目指向子条目，或从后发生的事件指向先发生的事件，没有循环。

## 检查（全部通过）

- **BOM 与语言头：** 两种语言全部 .yml 都有 UTF-8 BOM 和正确的语言头。
- **重复键：** 两种语言各 0 个（不含 `replace/map/`）。
- **中英键名：** 30 个键完全一致，15 条定义都有标题与 `_desc`。
- **链接引用：** 所有 `[Glossary(...)]` 都指向已定义的词条，方括号成对。
- **字面不变：** 20 个改动文件去掉新链接后，与备份逐字节相同。
- **玩家文字：** 新词条中文无“；”，无“西安”。
- **pdx.py：** 解析 `nesnd_beiming_glossary.txt`，得 15 条。
- **audit.py：** 报告 `nesnd-workbench/reports/2026-11-12-beiming-glossary/audit.json`。2 处 parse 错误都是 `.scratch/steam-desc` 里的说明草稿，136 处重复州主或投资者属于地图历史，均与本次无关。audit.py 不检查本地化，本地化由上面几项检查。
- **备份：** `nesnd-workbench/backups/20261112-beiming-glossary/`（改动前的 localization 与 common/glossary）。

## 复测时看哪里

1. **百科词汇表页**应列出 15 条新词条。这是确认文件生效最快的办法。
2. **地权革命日志**（`ce_cne_land_reform_reason`）：悬停“西秦大革命”，再在其说明里悬停“长安起义”，然后是“蓝田哗变”，最后是“中原大战”，可以检验三层嵌套。
3. **中华帝国事件 flavorCNE.1.d（推动地权革命）**：一段里同时有中华大革命、北明、南征三个链接。中华大革命的说明链接了 7 个子条目。
4. **flavorCNE.15.d（《北明战国世》出版）**：书名、北明、中华大革命、扬州条约四个链接。“北明世界”按你的要求没有链接。
5. **明朝开局事件 flavorUSM.1.d、flavorUSM.4.d**：北明、藩镇、北明战国世。悬停北明，再进入联军体系，可以看南北军全称的显示。
6. **共和派日志**（`nesnd_cne_confidence_journal_reason`、`nesnd_cne_republic_journal_reason`）和**南朝和解日志**（`nesnd_south_reconciliation_reason`）。
7. **英文界面**同样看上述位置。另请留意 “Chang’an Uprising” 链接里的弯引号是否正常显示。

## 补充答复后的修改（2026-11-12）

- 苏阿宏即苏宏，蓝田哗变词条写作“苏阿宏（苏宏）”，英文写作 “Su Ahong (Su Hong)”。
- 北明亡于1707年。北明词条写为“直到1707年秦燕灭明”，联军体系的年代改为1611—1707，灭明战争仍为1706—1707。
- 说明长度保持现状。另一会话改动的文件与本任务不重叠。
- 重新生成两份词条本地化文件后复查，BOM、重复键、中英键名和引用全部通过。
- 第一轮第八节的其他文本问题仍只记录，未改。

## 改动文件与链接数

| 文件 | 插入链接 |
|---|---|
| [ce_cne_events_l_simp_chinese.yml](../../localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml) | 15 |
| [ce_usm_events_l_simp_chinese.yml](../../localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml) | 14 |
| [ce_cne_events_l_english.yml](../../localization/english/replace/ce_cne_events_l_english.yml) | 13 |
| [ce_usm_events_l_english.yml](../../localization/english/replace/ce_usm_events_l_english.yml) | 13 |
| [nesnd_cne_land_reform_l_simp_chinese.yml](../../localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml) | 7 |
| [nesnd_cne_land_reform_l_english.yml](../../localization/english/replace/nesnd_cne_land_reform_l_english.yml) | 6 |
| [nesnd_south_politics_l_english.yml](../../localization/english/replace/nesnd_south_politics_l_english.yml) | 4 |
| [nesnd_south_politics_l_simp_chinese.yml](../../localization/simp_chinese/replace/nesnd_south_politics_l_simp_chinese.yml) | 4 |
| [ce_country_flavor_text_l_english.yml](../../localization/english/replace/ce_country_flavor_text_l_english.yml) | 3 |
| [ce_country_flavor_text_l_simp_chinese.yml](../../localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml) | 3 |
| [ce_events_1_l_english.yml](../../localization/english/replace/ce_events_1_l_english.yml) | 2 |
| [ce_events_1_l_simp_chinese.yml](../../localization/simp_chinese/replace/ce_events_1_l_simp_chinese.yml) | 2 |
| [ce_country_flavor_l_english.yml](../../localization/english/replace/ce_country_flavor_l_english.yml) | 1 |
| [nesnd_crisis_l_english.yml](../../localization/english/replace/nesnd_crisis_l_english.yml) | 1 |
| [nesnd_per_faith_l_english.yml](../../localization/english/replace/nesnd_per_faith_l_english.yml) | 1 |
| [nesnd_sha_restore_yan_l_english.yml](../../localization/english/replace/nesnd_sha_restore_yan_l_english.yml) | 1 |
| [ce_country_flavor_l_simp_chinese.yml](../../localization/simp_chinese/replace/ce_country_flavor_l_simp_chinese.yml) | 1 |
| [nesnd_crisis_l_simp_chinese.yml](../../localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml) | 1 |
| [nesnd_per_faith_l_simp_chinese.yml](../../localization/simp_chinese/replace/nesnd_per_faith_l_simp_chinese.yml) | 1 |
| [nesnd_sha_restore_yan_l_simp_chinese.yml](../../localization/simp_chinese/replace/nesnd_sha_restore_yan_l_simp_chinese.yml) | 1 |
| 合计（20 个文件） | 94 |

按词条：

| 词条 | 中文 | 英文 |
|---|---|---|
| 北明（`glossary_nesnd_beiming`） | 12 | 10 |
| 北明战国世（`glossary_nesnd_beiming_zhanguoshi`） | 5 | 4 |
| 塞王之乱（`glossary_nesnd_saiwang_rebellion`） | 0 | 0 |
| 藩镇（`glossary_nesnd_fanzhen`） | 9 | 9 |
| 中原大战（`glossary_nesnd_central_plains_wars`） | 0 | 0 |
| 联军体系（`glossary_nesnd_coalition_order`） | 0 | 0 |
| 灭明战争（`glossary_nesnd_overthrow_of_ming`） | 0 | 0 |
| 中华大革命（`glossary_nesnd_chinese_revolution`） | 8 | 7 |
| 蓝田哗变（`glossary_nesnd_lantian_mutiny`） | 0 | 0 |
| 长安起义（`glossary_nesnd_changan_uprising`） | 0 | 0 |
| 西秦大革命（`glossary_nesnd_western_qin_revolution`） | 8 | 8 |
| 鼓楼结社（`glossary_nesnd_gulou_society`） | 0 | 0 |
| 牧仲棠东征（`glossary_nesnd_eastern_campaigns`） | 0 | 0 |
| 南征（`glossary_nesnd_southern_campaign`） | 6 | 6 |
| 扬州条约（`glossary_nesnd_treaty_of_yangzhou`） | 1 | 1 |

## 跳过的位置

| 理由 | 文件:行 | 键 | 上下文 |
|---|---|---|---|
| 事件标题 | ce_cne_events_l_english.yml:151 | flavorCNE.15.t | …Publication of Chronicles of the Northern Ming Warring States… |
| 事件标题 | ce_cne_events_l_simp_chinese.yml:157 | flavorCNE.15.t | …《北明战国世》出版… |
| 人物引语，“复议南征”指再次出兵 | nesnd_crisis_l_simp_chinese.yml:59 | nesnd_crisis.20.f | …“昔年渡江之兵，今尚有在营者。若朝廷复议南征，臣请先核粮饷。”… |
| 修正名称（专名） | ce_cne_events_l_english.yml:149 | bm_the_book | …Chronicles of the Northern Ming Warring States… |
| 修正名称（专名） | ce_cne_events_l_simp_chinese.yml:155 | bm_the_book | …《北明战国事》… |
| 同键非首次 | ce_usm_events_l_english.yml:33 | flavorUSM.4.d | …ing and the exactions of military governors and transport officials.… |
| 同键非首次 | nesnd_crisis_l_english.yml:47 | nesnd_crisis.20.d | …land reform would make a southern expedition more burdensome still. W… |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:18 | flavorUSM.1.d | …永久地改变了人类对于世界岛的势力划分。但对于经历了北明数百年藩镇政治的人们来说，朱姓的王朝给神州大地也带… |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:33 | flavorUSM.4.d | …的威胁。终于在同年六月成行。\n\n这次觐见是一场北明从藩镇时期到诸侯时期近三百年来都未有人见过的盛大巡… |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:33 | flavorUSM.4.d | …近万名民夫运送的安南、高棉贡米。与之相对的，则是在藩镇节度使制度下被小规模械斗和转运使卡要下，四时常乱，… |
| 同键非首次 | nesnd_crisis_l_simp_chinese.yml:47 | nesnd_crisis.20.d | …务仍须军队与财力维持，地权改革若尚未完成，更难兼顾南征。此时卷入南朝的混战，究竟能为帝国赢得什么？… |
| 指法国大革命 | ce_french_empire_journals_l_english.yml:38 | je_ce_subpress_republican_movement_reason | …ince the outbreak of the Great Revolution, an idea of the insepara… |
| 指法国大革命 | ce_french_empire_journals_l_english.yml:41 | je_ce_republican_movement_reason | …ince the outbreak of the Great Revolution, an idea of the insepara… |
| 指法国大革命 | ce_french_empire_journals_l_english.yml:44 | ce_french_revolution_base | …Legacy of the Great Revolution… |
| 指法国大革命 | ce_french_empire_journals_l_english.yml:144 | fra_unrest.13.d | …fter the outbreak of the Great Revolution, the [ROOT.GetCountry.Ge… |
| 指法国大革命 | ce_french_empire_journals_l_english.yml:180 | fra_unrest.18.d | …fter the outbreak of the Great Revolution, he fled to England for … |
| 指法国大革命 | ce_country_flavor_text_l_simp_chinese.yml:4 | GBR_FLAVOR_TEXT | …列颠步履阑珊地踏入了法国人的世纪。从新大陆的独立到大革命的恐怖，再到拿破仑的兴起，最后是法兰西-明人同盟的… |
| 指法国大革命 | ce_french_empire_journals_l_simp_chinese.yml:38 | je_ce_subpress_republican_movement_reason | …自从大革命爆发以来，一种民族和民权密不可分的思想就在法兰西民… |
| 指法国大革命 | ce_french_empire_journals_l_simp_chinese.yml:41 | je_ce_republican_movement_reason | …自从大革命爆发以来，一种民族和民权密不可分的思想就在法兰西民… |
| 指法国大革命 | ce_french_empire_journals_l_simp_chinese.yml:44 | ce_french_revolution_base | …大革命的遗产… |
| 指法国大革命 | ce_french_empire_journals_l_simp_chinese.yml:95 | fra_unrest.3.d | …赋予有产公民们“尊严、义务和选举权”。从那时开始，大革命和拿破仑浪潮后的专权时代的那种“属于王朝和国家”法… |
| 指法国大革命 | ce_french_empire_journals_l_simp_chinese.yml:144 | fra_unrest.13.d | …大革命爆发后，[ROOT.GetCountry.GetA… |
| 指法国大革命 | ce_french_empire_journals_l_simp_chinese.yml:181 | fra_unrest.18.d | …路易 - 腓力是奥尔良公爵路易 - 腓力二世之子。大革命爆发后，他因故一度逃亡英国，在英国与拿破仑议和后又… |
| 条件提示，且“北明中国”为泛称 | ce_cne_events_l_english.yml:67 | tooltip_is_modern_china_state | … an agrarian province in Northern Ming China… |
| 条件提示，且“北明中国”为泛称 | ce_cne_events_l_simp_chinese.yml:73 | tooltip_is_modern_china_state | …是北明中国的农业省份… |
| 泛称（北明中国、北明世界） | ce_cne_events_l_english.yml:130 | flavorCNE.12.d | …smen, and strategists in Northern Ming China, Mu built a nation… |
| 泛称（北明中国、北明世界） | ce_cne_events_l_english.yml:152 | flavorCNE.15.d | … Great Revolution in the Northern Ming world. The work spans fi… |
| 泛称（北明中国、北明世界） | ce_cne_events_l_simp_chinese.yml:136 | flavorCNE.12.d | …梁城郊梦华别宫。享年七十岁。是为华太祖高皇帝。作为北明中国历史上最成功的军事家、政治家、战略家之一，牧仲… |
| 泛称（北明中国、北明世界） | ce_cne_events_l_simp_chinese.yml:158 | flavorCNE.15.d | …《北明战国世》为北明世界中华大革命后，中华帝国太祖牧仲棠幼妹牧沐子中晚… |
| 王安石诗句 | ce_cne_events_l_simp_chinese.yml:149 | flavorCNE.14.f | …三年隔，又作尘沙万里行。欲问后期何日是，寄书应见雁南征。\n——《示长安君》王安石… |

另有第一轮列出的 16 处“东征”（吴伐日本、西秦东顾、哥萨克东进）不是牧仲棠东征，词条改名后已不匹配，未链接。

