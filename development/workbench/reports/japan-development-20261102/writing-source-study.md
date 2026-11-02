# 日本发展文本：作者原文取样与双语编辑草稿

日期：2026-11-02。范围：原作者文本取样、设定边界、名称与日志正文草稿。仅写本报告；未改游戏、未开游戏。

状态：**SOURCE_STUDY / EDITORIAL_DRAFT / ENGINE_NOT_RUN**。本报告没有收到最终脚本键契约，以下编号是编辑编号，不是游戏键。草稿尚未核对新增脚本、动态作用域、最终覆盖层或全部触发条件，不能称作“全部文本通过”或直接整批落库。原文来源核验已完成；文案提案与技术接入验收分开。

已阅读 nesnd-player-writing、nesnd-victoria3 的 narrative-context、numeric-scale-contract、author-prose-profile，以及日本方案全篇（含第九、十节）、日本三份研究。catalog.py status：Victoria 3 1.13.11 / build 24799966 / CURRENT / changed_count 0，仅证明来源版本。

## 1. 作者来源与可复核指纹

下列 A1–A4 均从独立备份逐字读取，并用 `git show f18b6c4:相对路径` 逐字比较。完整基准提交为 `f18b6c45525351f5bf1a86ab29cccff9fee49500`；四文件完全相同。行号是备份当前的一基行号。当前主 MOD 的 `nesnd_japan_l_*.yml` 只用于核现行国名，不冒充作者原稿。

| ID | 文件 | SHA-256 | 与基准逐字一致 |
| --- | --- | --- | --- |
| A1 | [ce_usm_events_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml>) | `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f` | 是 |
| A2 | [ce_cne_events_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml>) | `3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a` | 是 |
| A3 | [ce_french_empire_journals_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml>) | `352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844` | 是 |
| A4 | [flavorJAP_ce.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/events/flavorJAP_ce.txt>) | `0150edb24e6ae546d3baa31cdb29c9e9011b021c6f96093c2a3e3f2b0654d18d` | 是 |

## 2. 实际作者样本

样本保留原字，包括原稿的笔误与动态引用。它们证明文体与字段用途；有错误的拼写、接口或年代不应作为新的写法继承。A1 的 `flavorJAP_ce.1.d` 将人物意识形态当作将军称谓，是源码/本地化契约问题，不能据此仿写。A4:15、100、312分别把`.t/.d/.f/.1`用于标题、叙述、风味与选项；A4:121、333的日期和人物条件说明继承事件依赖特定人物，不能把秀明的愿望写成所有国家永久事实。

### A1:149 — `ce_usm_cw_japanese_interest`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:149>)

> ce_usm_cw_japanese_interest: "第二次靖难战争：和族独立运动"

### A1:150 — `ce_usm_cw_japanese_interest_reason`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:150>)

> ce_usm_cw_japanese_interest_reason: "丰臣幕府在距今约两百年前依靠大明吴王的支持平定了战国之世，又在朝鲜的争夺中联合后者击败了燕京明廷和故齐藩支持的朝鲜。"

### A1:256 — `usm_civilwar.14.d`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:256>)

> usm_civilwar.14.d: "我们为南明赴汤蹈火，其中一各原因就是我们曾经被承诺了他们所占日本领土的归还。现在我们已经答打赢了这场大战，是时候让明朝人履行契约了。"

### A1:258 — `usm_civilwar.14.1`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:258>)

> usm_civilwar.14.1: "就是这样，发出去！"

### A1:302 — `usm_civilwar.23.d`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:302>)

> usm_civilwar.23.d: "郑家和日本的统治者都是老相识了。说实话，他们虽然已经是中国之天下人。但按照唐土历史的惯例，天下人更进一步也并非是前无古人，反倒显得郑家隐忍太久了。然而，郑吴的人中就是对自己的实力过于自信。阴影中，反对郑家势力的人们正在集结。这将是百年未有的时机，如果明国（吴国）内战爆发，日本作为明廷诸外藩中最大的一个，必须迅速做好维护我们利益，乃至神州秩序的准备。"

### A1:305 — `usm_civilwar.23.2`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:305>)

> usm_civilwar.23.2: "如果战争爆发，我们应当积极支持那些反对吴朝的力量。"

### A1:332 — `flavorJAP_ce.1.d`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:332>)

> flavorJAP_ce.1.d: "自南吴军队协助先太阁丰臣秀吉夺取日本政权后，我们的地位便久处明廷之下，渐渐成为其臣妾。最终不仅失去了九州岛，海关贸易的权力一并为杭州西府所设置的“东洋领事府”所控制。然而，风水自古是轮流转的。在南明联邦崩溃的洪流中，当代幕府将军[SCOPE.sCharacter('japanese_ruler').GetIdeology.GetName]攥紧了时代的脉络，赢得了来之不易的独立。"

### A1:334 — `flavorJAP_ce.1.1`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:334>)

> flavorJAP_ce.1.1: "我们不必再遵守锁国令了！"

### A1:337 — `flavorJAP_ce.2.d`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:337>)

> flavorJAP_ce.2.d: "盛夏的酷热使年迈的[SCOPE.sCharacter('japanese_shogun').GetPrimaryRoleTitle][SCOPE.sCharacter('japanese_shogun').GetFullName]健康状况急剧恶化，最终于本月早些时候薨逝。他的继承人，锐意改革的[SCOPE.sCharacter('japanese_heir').GetFullName]如今执掌日本。他梦想一个新的、强大的幕府政权已久，藩臣们也多尊重这一愿景。"

### A1:339 — `flavorJAP_ce.2.1`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:339>)

> flavorJAP_ce.2.1: "我们必须向明国学习。"

### A1:340 — `flavorJAP_ce.2.2`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:340>)

> flavorJAP_ce.2.2: "我们必须现代化！"

### A1:344 — `flavorJAP_ce.3.f`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:344>)

> flavorJAP_ce.3.f: "将军的床被移到窗前。仆人们本指望从海上吹来的凉风，配合上手中的扇子，能稍微减轻暑气。床尾摆着一只打开的冰匣，他的额头上覆着湿布。\n\n今天没有风。燥热的空气在落日下翻涌。闷热而无情，笼罩一切。他已看不清下方海浪的形状。"

### A1:345 — `flavorJAP_ce.3.1`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:345>)

> flavorJAP_ce.3.1: "“兄终弟及，如明故事，吾弟当为尧舜...”"

### A1:346 — `flavorJAP_ce.3.2`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:346>)

> flavorJAP_ce.3.2: "改革失败了！谁会听将死之人的命令？"

### A2:15 — `ce_cne_land_reform_reason`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:15>)

> ce_cne_land_reform_reason: "这一运动发源自1810年的西秦大革命。被本时代人视为农业发达而宗族根深蒂固的东方诸国内萌发的一种近代经济上的变革运动。其特点大致可以是用赎买或强制剥夺的手段，将超额聚敛的土地从其旧时代的所有者手中剥夺，平均到部分农民手中。以此打破古代宗族对农村人口的束缚和垄断。中华帝国统治集团在掌权过程中一度中止这一变革。但在1820年的牧仲棠南征前后，为了经济振兴、解放生产和发动底层农民、士兵，牧仲棠及其亲信重新开启了这一运动。"

### A2:34 — `ce_cne_reform_limited_market_access_reason`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:34>)

> ce_cne_reform_limited_market_access_reason: "在过去的动荡岁月中，战争和社会革命带来的特殊繁荣时期导致了地方经济的野蛮生长。由此引发了国内市场的一系列动荡与内贸失调。是时候扭转这一局面了。"

### A2:69 — `flavorCNE.3.d`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:69>)

> flavorCNE.3.d: "我们完善的土地法案、雇工法案、民法家庭相关条文已被推行至帝国的每一个角落，建起来一个崭新的经济秩序。在这一秩序中，我们解放了被血亲家族束缚了数千年的人们。高高的田垄回归了它自然资源的本来面目。\n\n随着旧宗族和土地不再能锁住农民，无数稚嫩、满是灰土却充满朝气的脸孔源源不断地从郊野涌入城市。他们憧憬新的生活。一种用人类的智慧和科学力量构建的生活。许多血缘的余孽用各种各样的地方团体伪装自己，试图重新夺回对这些人的控制。但巡捕的警棍和判官的惊堂木终会粉碎他们的野心。\n\n我们又一次将开国帝牧仲棠的理想照进现实。我们证明了这个帝国是为了华夏民族之利益而构建。为此，它将保护哪怕最细小无助者自由选择自己命运的权力——他们如今在城市中追求幸福，给帝国带来新的繁荣。"

### A2:74 — `CNE_post_landdraft_modifier`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:74>)

> CNE_post_landdraft_modifier: "投资狂热"

### A2:79 — `flavorCNE.4.d`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:79>)

> flavorCNE.4.d: "地权革命是经济上的革新，同样也是一项冷酷的政治运动。它要将一整个旧社会窃夺数千年的利益，转移到诞生不过数十年的新贵手中。这一过程不仅仅是金钱赎买就能结束的，必然存在法律机关的追捕、诓骗、来回的争夺、执行者的背叛，甚至是残酷的暴力手段。\n\n这样的过程不仅仅会激怒那些地方乡绅，也会吓到仍处懵懂中的社会中层成员。后者由此就容易被前者纠集，化为前者的马前卒、排头兵了。"

### A2:81 — `flavorCNE.4.1`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:81>)

> flavorCNE.4.1: "胡言乱语，正不必忧心。"

### A3:236 — `ce_french_support_dynasty_button`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:236>)

> ce_french_support_dynasty_button: "保卫王朝"

### A3:237 — `ce_french_support_dynasty_button_desc`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:237>)

> ce_french_support_dynasty_button_desc: "波拿巴的道路是[ROOT.GetCountry.GetAdjective]民族团结和繁荣的唯一办法。革命君主制和拿破仑的宪政是同时实现稳定与公正的唯一出路。"

### A3:240 — `ce_french_against_dynasty_button_desc`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:240>)

> ce_french_against_dynasty_button_desc: "要么革命，要么帝制。任何折中都是在麻痹[ROOT.GetCountry.GetAdjective]公民。我们是勇于自立、长于自守的民族，绝不需要威胁我们生活的独治凌驾我上！"

### A3:245 — `je_ce_orleans_dynasty_support_reason`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:245>)

> je_ce_orleans_dynasty_support_reason: "拿破仑的后裔及其武勋支持者有种天然的蛮横，这种蛮横使其不足以为稳定繁荣的宪政所凭。而当今之寰球乃宪政主义和理性之世界，已非武夫政权所能称霸。更遑论使法兰西领袖西方世界在东西对抗中拔得头筹。"

### A3:248 — `ce_french_empire_oreleans_progress_bar_desc`

[原文件](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:248>)

> ce_french_empire_oreleans_progress_bar_desc: "#v [JournalEntry.GetCurrentBarProgress(ScriptedProgressBar.Self)|%1]#!（[JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0]/200）"

## 3. 从样本观察到的句法，与本轮采用的编辑选择

| 可观察事实 | 原文证据 | 本轮选择；不外推为作者禁令 |
| --- | --- | --- |
| 日本历史以援助、征服、领土及通商权的变化解释当下政治。 | A1:150、332、302。 | 主权、海港与朝鲜正文先说谁拥有何种利益；不以抽象“国家发展路线”开篇。 |
| 日本事件的“我们”带着幕府的利益，外交事件可带讽刺和傲慢。 | A1:256、258、302、304。 | 选项是当事人的决定；后果交给效果显示，不写“承受相应代价”。 |
| 正文与风味可以采用不同距离：继承正文说明人物政治愿景，病榻风味描写酷暑、冰匣、海风。 | A1:337、344。 | 只在具体事件需要场景时写场景；日志不必每次经过呈文、印信、账册。 |
| 改革理由可以长篇解释历史、阶层和生产关系。 | A2:15、69、79。 | 产业写原料、工厂、城市劳动力和生活，政治写谁扩大决策权；不强行统一为三句短文。 |
| 作者的现代政治经济词与历史叙述并存。 | A2:15的“近代经济”“解放生产”，A3:237的“革命君主制”“宪政”。 | 沿用现代化、宪政、民权、生产、商人、职业军队等具体词，不为显古雅改成泛泛“振纲纪”。 |
| 政治按钮可以正面支持某一制度，无需中立地列出所有利弊。 | A3:237、240；A2:81。 | 三路线各有自己的政治主张；不在每段追加匿名反对者或同样的财政警告。 |
| 准确读数与政治叙述分属不同字段。 | A3:249进度百分比与当前值/总值；A2:15正文另有goal。 | 条件用原生勾叉，变化用进度来源；正文不重复每月公式。 |
| 原稿也有否定对举和重复句式，并非所有原句都要照抄。 | A3:243“他不属于……”；A1:338含“此非……”。 | 按本轮用户要求避免新写套式“X不是Y而是Z”；不把原稿中普通“不是”一律删掉。 |

本轮不设字数硬配额，不据词频证明作者身份。下方草稿的历史事实来自明确方案或已核原稿，新增主张属于玩法提案，未伪装成作者既定结局。

## 4. 英文依据、专名和事实边界

英文先读当前原版同类JE，取其自然表达和字段分工，不移植德川幕府、天皇复位、未获承认等原版前提。原版工业正文以竞争与外国压力解释工业化，军制正文解释武士集团的形成和现状；锁国正文从贸易口岸制度谈开放；财阀正文写资本集中如何转化为政治力量。来源如下。

| ID | 当前原版来源与位置 | SHA-256 |
| --- | --- | --- |
| N1 | [content_1_l_english.yml:672](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/content_1_l_english.yml:672>) | `02241456487324b318f9c269a725b57027c5baaff2b36597e77412cf21fd9a84` |
| N2 | [ep2_sakoku_l_english.yml:2](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/ep2_sakoku_l_english.yml:2>) | `198f32422659b61d9b3848d12f922ba642f4d1078c72d880c1c9a6dba267fa58` |
| N3 | [ep2_04_l_english.yml:760](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/ep2_04_l_english.yml:760>) | `a2ba8f5db1b375fdb235046a103cc3a98b50524a5f5ff02f822e216e834a33af` |
| N4 | [ep2_03_l_english.yml:55](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/ep2_03_l_english.yml:55>) | `cffe0b00902f33dc151173190780c652bba2ca97e077c5780a5cb41222a7f2f0` |

N1:686短例：“Japan must modernize its industry to compete with nations that seek to control and exploit us.”这句话有政治目的且直述行动；本轮英文不逐字翻译中文的修辞，也不使用 preparation snapshot、monthly calculations 等开发词。

| 中文对象 | 当前英文 | 现行定位 |
| --- | --- | --- |
| 桑国 | Sang | `localization/english/replace/nesnd_japan_l_english.yml:6` |
| 扶国 | Fu；形容词 Tokugawa | 同文件:2–3 |
| 和国 | Wa；形容词 Imperial Japanese | 同文件:4–5 |
| 日本／丰臣幕府 | Japan / Toyotomi Shogunate | `ce_00_countries_l_english.yml:359`；`ce_countries_l_english.yml:81` |
| 江南文化 | Jiangnan | `ce_cultures_l_english.yml:23` |
| 南明USM | United Federation of Ming；政权改变后须实际动态国名 | `ce_countries_l_english.yml:34` |
| 中华CNE | Great Han Commonwealth；须实际动态国名 | `ce_countries_l_english.yml:59` |
| 东洲HUS | Civic Republic of Dongzhou | `ce_countries_l_english.yml:108` |
| 朝鲜 | Korea | `ce_00_countries_l_english.yml:401` |

将“中华帝国”一律译为 Mu Empire 会误用现行专名；把所有USM一律写Wu也会提前宣布吴代明。草稿避免无条件写某位摄政仍活着；“林摄政政权”的江南文化方针是制度身份，按方案第九、十节不随林去世或改宗主自动撤销。

本轮事实源为 [日本方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md>)。读入SHA-256：`50bc776788ccb7059620088465a8a39a7db1e61d1b2bed600b525912e46eed9f`。第九节规定三国产业次序、JIM不开放轻纺—SOL链、独立即进国家发展、团结与文化目标；第十节要求实际宗主和政治承诺分开、外交采购有具体合同、自治/统一与朝鲜治理分别收尾。本文不新增历史人口、工厂、国界、奖励或概率。

## 5. 双语名称与日志正文草稿

以下均为 **待接入草稿**；不是已通过的有效游戏文本。每项的“边界”留在报告，不能复制进玩家正文。句中的“我们”对应该日志所属国家。JAP/JTK/JIM默认链专名版本仅适用于该国；其他国家补充开放同链时，应使用同事实的通用版本或动态触发段，不能给桑国显示“扶国”。

### I-F1 · 扶国／矿业第一步

**山中的铁矿 / Iron in the Hills**

中文：德川氏据有的北方领地蕴藏着铁矿，山林又为冶炼和造船供应木材。军府若要装备新的军队，首先要让矿石运出山谷，使矿山与城下町的工场做成长期的生意。

English: The Tokugawa domains in the north hold iron deposits, while their forests provide timber for furnaces and shipyards. To equip a modern army, Fu must bring the ore down from the hills and establish lasting trade between its mines and town workshops.

编辑依据与边界：方案九.2；A2:34、69。不称扶国煤铁皆丰富，不把采矿奖励写成矿山吞吐；具体奖励另核。

### I-F2 · 扶国／军工船业第二步

**兵工与船坞 / Arsenals and Shipyards**

中文：军队需要枪炮，沿海交通和海防需要船只。矿山所产的铁只有送进兵工厂和船坞，才能成为军府可以依靠的力量；稳定的采购也将使工匠和商人敢于扩建工场。

English: Armies need weapons, while coastal trade and defence depend on ships. Iron from the mines must reach the arsenals and shipyards before it can strengthen the government. Steady orders will give craftsmen and merchants reason to expand their works.

编辑依据与边界：方案九.2、十.3；A1:150。对吴采购只能作为合同成立时的另段；此基本正文亦适合独立或敌对阶段。

### I-F3 · 扶国／城市第三步

**城下町的变迁 / Beyond the Castle Town**

中文：铁矿、兵工厂和船坞正在改变北方的城下町。前来谋生的工人需要住房和粮食，商人希望货物能够运往更远的市场。军府要使这些新兴城市成为长久的税源，就须让道路、学校和官府跟上它们的成长。

English: Mines, arsenals and shipyards are changing the castle towns of the north. Workers arriving in search of wages need homes and food; merchants seek markets farther afield. Roads, schools and public administration must grow with these towns if they are to sustain the state.

编辑依据与边界：方案九.2；A2:69。道路、学校是政治经济叙述，若实际阶段不做学校，删去学校而不制造假目标；数字单独显示。

### I-S1 · 桑国／原料第一步

**棉田、桑园与茶山 / Cotton, Silk and Tea**

中文：丰臣家留下的西部领地拥有棉田、桑园和茶山。乡间出产沿着商路进入城镇，也使农民的生活越来越受市价影响。扩大的市场需要更多原料，桑国的工商业可以由此生长。

English: The western lands retained by the Toyotomi have cotton fields, mulberry groves and tea gardens. Their produce reaches the towns through established trading routes, tying rural livelihoods ever more closely to market prices. Growing demand offers Sang a foundation for further industry.

编辑依据与边界：方案九.2；A2:15、34。只列真实可种植品类，丢失适用州后须触发短段；不声称固定产量。

### I-S2 · 桑国／成衣第二步

**机杼声中 / The Sound of the Looms**

中文：棉花和生丝经商人之手运往各地，织工却仍受制于狭小的作坊。新的纺织厂将把这些原料留在本国加工，也给离开田地的人们提供另一种生计。

English: Merchants carry cotton and raw silk to distant markets, while weavers still work in small workshops. Larger textile mills would process more of this produce at home and offer a living to people leaving the fields.

编辑依据与边界：方案九.2；A2:69。入口若已是大型机器纺织业，须换“进一步扩建”版本；不能无条件宣布本国尚无厂。

### I-S3 · 桑国／消费品第三步

**百姓的买卖 / Goods for the People**

中文：城市中的工人和店主有了固定的收入，便会购买更好的食品、家具和日用器皿。工商业的兴盛需要这许多普通人参与其中，让家庭的开支养活更多工场，也让工场的工资回到市面。

English: Workers and shopkeepers with regular incomes can buy better food, furniture and household goods. Their spending sustains new workshops, whose wages in turn support the shops. A wider market for everyday goods will give industry roots throughout the country.

编辑依据与边界：方案九.2；A2:69。普通家庭消费是本段主旨，避免又列军费、外交或无关代价。

### I-S4 · 桑国／生活改善第四步

**富足的生活 / A Better Living**

中文：新工场已经吸引人们离开乡村，城市也因他们的劳动而兴旺。丰臣政府许诺的繁荣，应当见于百姓的衣食与居所；只有长久改善的生活，才能使人们愿意留在这新的经济秩序中。

English: New workshops have drawn people from the countryside, and their labour has helped the towns prosper. The prosperity promised by the government should be visible in their food, clothing and homes. Lasting improvements in daily life will secure their place in the new economy.

编辑依据与边界：方案九.2；A2:69。仅在前序工业完成后出现；SOL达标维持期必须据实际代码单列，不写永久生活水平奖励。

### I-W1 · 和国／粮食第一步

**两京的生计 / Feeding Kyoto and Osaka**

中文：京都的居民与大阪的商民依靠田间、海上和商船送来的粮食生活。和国的疆域狭小，稳定的收成、渔获和贸易将共同养活城里的人们，为新的工场留下成长的余地。

English: Kyoto and Osaka depend on food brought from the fields, the sea and merchant ships. Wa governs a small territory. Reliable harvests, fisheries and trade can feed its towns and allow new industries to grow.

编辑依据与边界：方案九.1–2；不能写全国自给、不能擅自增加大阪产量。失去京都或大阪时不得继续显示两京版本。

### I-W2 · 和国／城市第二步

**朝廷与商都 / Court and Commerce**

中文：京都是朝廷所在，大阪则聚集着往来商人和手工业者。和国要在这两座城市立足，就必须把商业所得用于道路、官府与民生，使朝廷的号令能够得到城镇社会的拥护。

English: Kyoto houses the imperial court; Osaka brings together merchants and craftsmen. To establish itself in these cities, Wa must turn commercial wealth into roads, public administration and better living conditions, giving townspeople a stake in its government.

编辑依据与边界：方案六、九.2；政治目标是两城承载小国，不把林写成永生统治者；具体完成条件另核。

### I-W3 · 和国／食品加工第三步

**粮食入市 / Food for the Towns**

中文：城镇人口的增长扩大了对加工食品的需求。粮食与鱼获经过加工，可以运到更远的市场，供养更多脱离田地的劳动者。大阪的商路和京都周围的生产将为这门生意提供根基。

English: Growing towns need more processed food. Preserving grain and fish allows merchants to carry them farther and supports more workers away from the land. Osaka’s trading connections and production around Kyoto give this industry a firm foundation.

编辑依据与边界：方案九.2。罐头科技未启用前不硬写“罐头”；实际只要求食品厂时不承诺贸易路线已经建立。

### P0 · 完整丰臣日本／政治入口

**幕府的前途 / The Future of the Shogunate**

中文：丰臣幕府借助吴王的兵力平定日本，又靠诸藩的服从维持了两百年的统治。如今商人积累的财富、新学带来的议论与军队对新式武备的需要，都在改变将军治下的社会。丰臣家必须决定，怎样使幕府在这场变动中保住自己的权威。

English: Wu’s military support helped the Toyotomi unify Japan, and the obedience of the domains sustained their rule for two centuries. Merchant wealth, new learning and the army’s demand for modern weapons are now changing that society. The Toyotomi must decide how the shogunate will preserve its authority through these changes.

编辑依据与边界：方案三、四；A1:150、337。不宣布1840、1846事件已经发生，不预言改革人物死亡。

### P1 · 幕府改革路线

**再造幕府 / Renewing the Shogunate**

中文：将军的权威可以召集诸藩，也可以为新学和商业开路。改革派希望扩大议政，选任熟悉实务的官员，把各藩的财赋与兵力汇成可以调度的国家力量。丰臣家将在这一事业中重新取得统率日本的资格。

English: The shogun’s authority can bring the domains together and give new learning and commerce room to grow. Reformers seek wider deliberation, capable officials and a government able to coordinate provincial revenues and forces. Through these changes, the Toyotomi aim to renew their claim to lead Japan.

编辑依据与边界：方案四.1；A1:337–340。丰臣专属版本；若路线允许其他家族，需另写主语，不能全局替换皇帝称谓。

### P2 · 军事集权路线

**军府的新秩序 / The Military Ascendant**

中文：战场上的胜利使军官们相信，他们也能带领国家摆脱内争与屈从。职业军队、兵工厂和统一的征募制度将成为新政权的支柱。军府要把这份战功变成统治的依据，将各地的人力与财力集中到自己手中。

English: Victory has convinced the officers that they can also lead the country out of division and dependence. A professional army, arsenals and a common system of recruitment would become the pillars of their government. They now seek to turn military prestige into authority over the nation’s manpower and revenues.

编辑依据与边界：方案四.2；A2:20、79。首句仅用于有胜利/军功入口；若无战功条件，改“军官们主张以统一的指挥结束内争，摆脱对外屈从。”不能凭空宣布胜利。

### P3 · 民主化路线

**国人议政 / A Voice in Government**

中文：商人承担国家的税赋，军人保卫它的疆土，读书人也已开始讨论国政。宪政派希望使地方代表进入议会，让公共事务经由辩论与表决决定。学校、言论与选举的扩展，将使更多国人参与这个新政府。

English: Merchants finance the state, soldiers defend its territory, and scholars increasingly debate its government. Constitutionalists seek an assembly of local representatives to settle public affairs through debate and votes. Schools, freer expression and wider elections would bring more people into political life.

编辑依据与边界：方案四.3；A3:237、245。保留君主或共和国由实际分支决定；不预设普选、工会已存在或民主自动退出朝鲜。

### D0 · 独立后国家发展总日志

**自主之国 / A Nation of Our Own**

中文：对外事务、军队与通商如今由本国决定。各地的工商业可以供养新的军队，新的学校和官府也能使国家征得税赋、办得事务。我们要把独立带来的权力用在这些事业上，使邻国有理由与我们平等交往。

English: Foreign affairs, the army and trade are now in our own hands. Industry can sustain modern forces, while schools and effective administration give the state the means to raise revenue and govern. We must use our independence to build a country that our neighbours will deal with as an equal.

编辑依据与边界：方案九.3、十.5；A1:332；N1。只在真实独立时显示；不说从未获国际承认，不要求九州已归还，不在正文罗列子日志。

### C0 · 团结常驻／通用正文

**国民团结 / National Cohesion**

中文：安定的生活使人们愿意相信共同的国家，学校与官府则把远近的地方联结起来。战争的胜负、生活的盛衰，都在改变这份信任。政府若能使各地百姓分享繁荣，便能使他们更牢固地归属于同一个社会。

English: Stable livelihoods give people confidence in a common state, while schools and public administration connect its regions. The fortunes of war and changes in daily life continually reshape that confidence. Prosperity shared across the country can deepen the sense of belonging to one society.

编辑依据与边界：方案九.4、十.4。文化目标和概率属于效果说明，不把“归属”误称已授予平等公民权；无一次性通关奖励。

### O0 · 可用九州口岸／主动开国

**重开海门 / Opening the Ports**

中文：九州的少数口岸承载着日本与海外的买卖，商人和官府都受制于这狭窄的通道。更多港口一旦开放，工场便能取得远方的原料，船商也可以寻找新的销路。政府必须决定如何管理这片正在扩大的海上贸易。

English: A few ports in Kyushu carry Japan’s overseas trade, restricting merchants and officials to a narrow channel. Opening more ports would bring distant raw materials to the workshops and new markets to the shipping houses. The government must decide how this wider maritime trade will be governed.

编辑依据与边界：方案二、三；A1:332、334；N2。只适用于仍有九州口岸且贸易法律限制仍成立的国家。

### O1 · 完全失去九州贸易入口

**另辟海路 / New Ports of Trade**

中文：九州的贸易口岸已经离开我们的掌握，本国的船商仍被旧日禁令留在岸上。其他港口必须获得通商的许可，让货物重新往来于我们的城市和海外市场。

English: Kyushu’s trading ports are beyond our control, yet the old restrictions still keep our merchants ashore. Other ports must be opened to commerce so that goods can once again pass between our towns and overseas markets.

编辑依据与边界：方案二、九；A1:332。专用于锁国限制尚在且无九州口岸、有其他适用海港者；若已经开港不得显示“仍被禁令”。

### K0 · 拥有朝鲜州／治理入口

**海峡彼岸 / Across the Strait**

中文：丰臣与吴国的联军曾在朝鲜夺取大片土地，港口、矿山与驻军也把两岸的利益联在一起。如今这些地方的居民仍有自己的政治诉求。我们在半岛上的统治，将取决于政府怎样安排地方权力、经营利益与朝鲜人的生活。

English: The Toyotomi and Wu once conquered extensive lands in Korea. Ports, mines and garrisons have since bound interests on both sides of the strait. The people of these territories have political demands of their own. Our rule will depend on how we settle local authority, commercial interests and their place in government.

编辑依据与边界：方案五、十.5；A1:150。不称拥有整个半岛，不把KOR与CNE默认为恒在。

### K1 · 朝鲜／直接统治

**经营朝鲜 / Governing Korea**

中文：港口和矿山的收入使政府有理由维持半岛上的统治。要让驻军守得住、商路走得通，就须在当地建立足以办事的官府和学校，并处理居民对征税、土地与地方权力的要求。

English: Revenue from ports and mines gives the government a strong interest in retaining its Korean territories. Secure garrisons and dependable trade require effective local administration and schools, as well as answers to demands over taxation, land and local authority.

编辑依据与边界：方案五；A2:79；N4。利益是统治者的立场，不将反对居民写为天生落后；仅操作当前所有州。

### K2 · 朝鲜／自治安排

**朝鲜自治 / Korean Self-Government**

中文：朝鲜地方代表希望自行处理税赋与民政，商人则关心港口和投资能否继续经营。我们可以让当地政府承接这些事务，再以协议确定双方的权利，使半岛的秩序有当地人参与维持。

English: Korean representatives seek control over taxation and civil administration, while merchants want to preserve access to ports and investments. A local government could take charge of these affairs, with an agreement defining each side’s rights and giving Koreans a greater part in maintaining order.

编辑依据与边界：方案五。地方代表为本轮提案，不伪署作者原作人物；须有真实接收国家/政府与回应，不保证财政收入完全不变。

### K3 · 朝鲜／承认并退出

**与朝鲜议和 / A Settlement with Korea**

中文：继续驻守朝鲜需要兵力和财力，也使我们不断卷入半岛上的争端。若能同接管当地的政府谈妥边界、驻军撤离与商贸往来，我们便可结束直接统治，把两国的关系建立在新的协议之上。

English: Holding territory in Korea requires troops and revenue and keeps us entangled in the peninsula’s disputes. An agreement with the government taking over could settle the border, the withdrawal of our garrisons and future trade, allowing direct rule to give way to a new relationship.

编辑依据与边界：方案五、十.5。只对真实持有地转移；接收方必须存在并接受，不保证和平/商业回报自动成立。

### K4 · 无须持有朝鲜州／具体外交议题

**半岛交涉 / Negotiations over Korea**

中文：朝鲜的港口、边界和外国驻军关系着海峡两岸的安危。对这些问题有实际权利的各方需要坐到谈判桌前，决定哪些承诺能够换来领土、安全或通商上的让步。

English: Korea’s ports, borders and foreign garrisons affect security on both sides of the strait. The parties with a stake in these questions must negotiate over the territory, security guarantees and commercial concessions they are prepared to exchange.

编辑依据与边界：方案十.5。通用入口必须有具体对象和议题；最终应按实际提案显示其中一段，不向玩家永久陈列全套虚构谈判。

## 6. 本轮试写、退稿与局部编辑规则

此表记录本报告内实际试写的失败句，并非声称它们曾经是作者原文或已经在游戏中显示。

| 原作者对照 | 本轮试写原句 | 判定与原因 | 修订决定 |
| --- | --- | --- | --- |
| A2:69 从人口离开田地写到城市生产、生活和繁荣。 | “完成农业核验后，桑国可以开启下一项成衣子日志，并持续检查消费条件。” | 返工。程序调用变成故事，主语是验证流程。 | I-S2改写为商人运原料、织工生产、离田者就业；阶段完成与接续只留脚本。 |
| A3:237 直接表明支持王朝与宪政的理由。 | “军府不仅要赢得战争，也必须承受军费与文官反对带来的代价。” | 返工。套式对举并把尚未确定的反对者塞入正文，沿用用户反感的代价总结。 | P2改写为军官把战功转为对征募与财政的控制；只有实际effect涉及的集团在必要提示说明。 |
| A1:332 将从属地位、九州及海关权联系起来。 | “独立不是改革的终点，而是国家发展真正的开始。” | 返工。重复定义“独立”却没有新事实。 | D0写实际外交、军队、贸易权与国家建设的用途。 |
| A1:344 的冰匣、湿布和海风服务于将军病死的事件。 | “官吏将两京粮册呈上案前，摄政批示逐户查核，待文书齐备再开工场。” | 返工。用同一官署小场景替代粮食、贸易和工业关系，并无对应政策。 | I-W1写京都大阪如何获得粮食，I-W3写加工食品如何供养城市。 |

局部规则：每段先确定具体的历史处境、行动者与可变化的关系；句子新增事实之后才考虑节奏。成本只在做选择时出现，不为每个建设目标统一添加“代价”；先查实际effect再指出承担者。本报告没有据单轮草稿修改永久技能。

## 7. 收到最终键契约后的逐条对读范围

待根任务给出：新增和改写的全部JE、事件、选项、按钮、状态、进度来源、modifier及自定义提示的有效键；对应入口、阶段、触发、真实效果、数值和动态scope。届时在根任务指定的比较报告内逐条记录“作者同类原句 → 实际候选 → 问题 → 修订 → 结论”，包含两种语言和所有最终replace覆盖层。

尤其要核：

- 矿业奖励作用金属制造，军工船业阶段的采购义务有真实对手与合同；失约/敌对/独立版本不继续写向吴交货。
- JIM无轻纺—SOL日志；京都/大阪失去时更新“和国两京”正文；粮食目标容许贸易，不暗添自给条件。
- P0不预告秀明、秀和或平胜的未发生结局；P1丰臣专名不能误给德川/天皇；P2若无近期胜利，使用已列替句。
- D0只在实际独立时使用“如今由本国决定”；重新附属应暂停或换段，不因为曾经独立就保持错误事实。
- 团结的常驻条不写通关奖励。文化提示按country选japanese或JIM的Jiangnan；每国每月一次30%抽取、成功最多单州总人口10%、不改宗教必须与实际脚本完全一致。未核脚本前不在草稿正文写效果承诺。
- 九州“少量口岸”和“完全失去”两版本分开，法律已开放时不再声称禁令仍阻港。
- 治理的有地条件与交涉的有对象条件分开；退出治理不自动取消仍真实存在的外交问题。
- 草稿不会创建引文。新对白若以后需要，标为本轮提案；现有历史引文只按原键与实际使用场合保留。

**当前结论：来源身份核验通过；文本为可继续编辑的提案草稿。未执行最终有效键审查，未称全量通过，未接入游戏，未运行引擎。**
