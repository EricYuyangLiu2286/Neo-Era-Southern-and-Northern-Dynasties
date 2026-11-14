# 北明与大革命概念：第一轮交付

2026-11-12。本轮只读、只起草，没有改动 MOD 的任何游戏文件，也没有启动游戏。证据与脚本在 `nesnd-workbench/reports/2026-11-12-beiming-glossary/`。

## 一、原版 1.15.1 的写法

下文 `GAME` 指 `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`（1.15.1 Ivan-Chai）。

**原版有两套可悬停的名词，历史事件和专名用的是“词汇表”（glossary），不是游戏概念。**

| | 游戏概念 concept | 词汇表 glossary |
|---|---|---|
| 定义 | `GAME/common/game_concepts/00_game_concepts.txt`（1953 行）、`01_additional_game_concepts.txt` | `GAME/common/glossary/00_glossary.txt`（19 条），格式说明 `GAME/common/glossary/glossary.md:1-3` |
| 键名 | `concept_<名>`，本地化 `concept_<名>`、`concept_<名>_desc` | 必须以 `glossary_` 开头，本地化 `<键>`、`<键>_desc`，可选 `<键>_short` |
| 字段 | `texture`、`is_loading_tip`、`shown_in_encyclopedia`（例 `00_game_concepts.txt:155-158`、`:1892-1894`） | `icon`、`shown_in_encyclopedia`，大多数条目为空 `{}`（`00_glossary.txt:1-41`，带图标的例子 `:27-29`） |
| 内容 | 游戏机制：政变、外交博弈、合法性 | 历史事件与名词：十二月党人起义、十一月起义、1830 年革命、第三次瓜分波兰、地方自治局 |
| 链接写法 | `[concept_coup]`，或 `[Concept('concept_commander_rank','concept_commander_rank_short')]`（`GAME/localization/english/concepts_l_english.yml:2817`） | `[glossary_revolutions_of_1830]`（`GAME/localization/english/ip5_02_l_english.yml:128`），或 `[Glossary('glossary_third_partition','$glossary_third_partition_short|q$')]`（`ip5_07_l_english.yml:3`、`:101`） |
| 只引用名称不生成链接 | `$concept_coup$`（`concepts_l_english.yml:2817`） | `$glossary_congress_of_vienna$`（`ip5_04_l_english.yml:530`） |

**嵌套。** 词汇表的说明里可以再放词汇表链接：`glossary_revolutions_of_1830_desc` 末尾链接到“会议波兰”条目（`GAME/localization/english/glossary_l_english.yml:51`，中文 `GAME/localization/simp_chinese/glossary_l_simp_chinese.yml:36`）。概念说明里大量嵌套 `[concept_…]`（`concepts_l_simp_chinese.yml:2196`）。

**写法。** 说明以 `#b;italic 名词#!` 开头，第一句下定义，再用一两段交代经过与后果，段间 `\n\n`（`glossary_l_simp_chinese.yml:21`、`:36`）。英文同理（`glossary_l_english.yml:29`、`:51`）。人名、国名、年份常加 `#b …#!`。

**长度。** 原版 19 条中文说明 18—201 字，英文 13—100 词。最长的是“1830年革命”（中文约 200 字、英文约 100 词）和“十二月党人起义”（中文约 140 字）。

**MOD 已有的先例。** `common/glossary/nesnd_forest_of_bayonets.txt:1` 定义了 `glossary_nesnd_settlement_of_1829`，正文用 `[Glossary('glossary_nesnd_settlement_of_1829','1829年的和议')]` 直接写显示文字（`localization/simp_chinese/replace/nesnd_forest_of_bayonets_l_simp_chinese.yml:2`、`:4-5`）。MOD 中没有其他自定义概念或词汇表，也没有任何关于北明或大革命的同类条目。

**建议：** 用词汇表实现，键名 `glossary_nesnd_*`，正文链接一律写 `[Glossary('键','原文名词')]`。显示文字取原句中的原词，这样插入链接不会改动任何字面文字。请确认（待决 A1）。

## 二、资料清单

| 代号 | 资料 | 用途 |
|---|---|---|
| PPT | `OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx`（SHA256 `b3306f4a…050ae`，与 canon 记录一致），抽取文本 `nesnd-workbench/research/20261031/北明ppet.txt`。引用写作“幻灯片:段落”，如 PPT 10:5 | 主干：北明分期（3、5、6）、灭明与南明（8、9）、关中大革命与东征（10）、南征与西秦（12、13）、陈东阳（15）、费西翼（16）、吴代明（17） |
| BM | `Desktop/Mod0/paratranz/decoded/celestial_empire/BM_start_events_l_english.yml`（内容为中文，4732 行，EU4 时代的北明事件与任务） | 塞王之乱、大营、直隶之乱、中原大战编号与年代、越国与闽国拓殖、吴越战争 |
| 列传 | `北明战国世/北明人物列传.docx`，抽取 `research/20261031/北明人物列传.txt`，按段落号 p 引用 | 牧仲棠、秦末帝、第五、六次中原大战、“秦国的灭亡与第一次中国革命”（p314–320） |
| 时间线 | `北明战国世/时间线 - 副本.docx` | 1441—1455 年燕、齐、唐、吴诸国，夺门之变（p5、p26） |
| canon | 技能 `nesnd-victoria3/lookup/canon/narrative-context.md`、`worldbook.json`（条目 chronology-variants、north-constraints）、`character-book.json`（牧仲棠、陈东阳、郑钦）、`north-south-institutions.md`（英文定译 Southern/Western Administration） | 年代异文的处理原则、人物立场、英文用名 |
| 原作 | Git tag `original-20261030` 的 `ce_cne_events`、`ce_usm_events`、`ce_country_flavor*` | 1810 西秦大革命、1819 称帝、1820—22 南征、1835 扬州条约；文风样本 |

PPT 与列传是作者早期设定，彼此有异文（见待决 B）。凡 MOD 原作已经采用的年份（1810、1819、1820—22、1835），草稿从原作。


## 三、概念树与草稿

链接只从主概念指向子概念，或从后发生的事件指向先发生的事件，两组之间唯一的共用条目是“中原大战”。草稿里 ⟦文字→键⟧ 表示一处嵌套链接，实装时写成 `[Glossary('glossary_nesnd_键','文字')]`。〔〕内是待决数字。

```
北明 ─┬─ 塞王之乱
      ├─ 藩镇 ───────────── (中原大战 → 藩镇)
      ├─ 中原大战 ◀──────┐ (两组共用)
      ├─ 联军体系 → 中原大战
      └─ 灭明战争 → 中原大战、联军体系
中华大革命 ─┬─ 中原大战（共用）
           ├─ 蓝田哗变 → 中原大战
           ├─ 西秦大革命 → 蓝田哗变
           ├─ 鼓楼结社 → 西秦大革命
           ├─ 东征
           ├─ 南征 → 东征
           └─ 扬州条约 → 南征
```

### `glossary_nesnd_beiming`：北明 / Northern Ming（北明组主概念）

中文：

> #b;italic 北明#!指1408年永乐帝在田猎中暴崩以后，直到〔1705〕年秦燕灭明的明朝。1433年宣德帝驾崩至灭明的两百余年，史称北明战国世。
>
> ⟦塞王之乱→saiwang_rebellion⟧后，宣德帝派驻各地的大营渐成⟦藩镇→fanzhen⟧，燕京朝廷的处境近于中唐以后的唐室。各镇逐步变为自行治国的诸侯，吴、秦、越、闽等国向南洋、中亚乃至新大陆殖民。几次⟦中原大战→central_plains_wars⟧后，天下进入燕、吴对垒的⟦联军体系→coalition_order⟧。⟦灭明战争→overthrow_of_ming⟧中秦燕联军攻入燕京，燕、秦称帝，南方诸侯另立南明，形成新的南北朝。

English:

> #b;italic Northern Ming#! is the Ming dynasty from the Yongle Emperor's sudden death on a hunt in 1408 until Qin and Yan overthrew it in 〔1705〕. The years after the Xuande Emperor's death in 1433 are called the Northern Ming Warring States.
>
> After the ⟦Rebellion of the Frontier Princes→saiwang_rebellion⟧, the Xuande Emperor's garrisons hardened into ⟦military fiefs→fanzhen⟧, leaving the Yanjing court much like the later Tang court. The fiefs became self-governing states, and Wu, Qin, Yue and Min colonised the Southern Seas, Central Asia and the New World. The ⟦Central Plains Wars→central_plains_wars⟧ produced the ⟦Coalition Order→coalition_order⟧ of Yan against Wu. In the ⟦Overthrow of the Ming→overthrow_of_ming⟧, Qin and Yan took Yanjing and proclaimed themselves emperors, while the southern princes founded the Southern Ming.

出处：PPT 3:5、3:7（1408 起点、燕明时期）；PPT 6:2（北明战国世 1433—1705）；PPT 5:11–12；PPT 6:7–8（拓殖）；PPT 6:10–11、8:2–8；BM 509.d（中唐，标注“构思中”）

### `glossary_nesnd_saiwang_rebellion`：塞王之乱 / Rebellion of the Frontier Princes

中文：

> #b;italic 塞王之乱#!是北明开端的宗室内战。永乐帝朱棣在靖难成功后暴崩，宁王朱权、晋王朱济熺、齐王朱榑等洪武诸子乘机起兵，与燕京的洪熙帝分庭抗礼。关中二王中立，周王不愿附逆，逃往广东。战事持续三年有余，双方议和相持。
>
> 宣德帝即位后灭晋平宁。1433年，他亲征突袭关中的蜀王朱椿，病逝于洛阳。此后朱姓藩王一蹶不振，异姓诸侯取而代之。

English:

> The #b;italic Rebellion of the Frontier Princes#! opened the Northern Ming. When the Yongle Emperor died suddenly after his usurpation, the Princes of Ning, Jin and Qi and other sons of the Hongwu Emperor rose against the Hongxi Emperor in Yanjing. The two princes in Guanzhong stayed neutral, and the Prince of Zhou fled to Guangdong rather than join the rebels. After more than three years both sides made peace.
>
> The Xuande Emperor later destroyed Jin and subdued Ning. In 1433 he died at Luoyang while marching against the Prince of Shu, who had seized Guanzhong. The Zhu princes never recovered, and lords of other surnames took their place.

出处：PPT 5:3–12；BM desc_BM_shuwang_legacy（第 1993 行，“塞王之乱的最后一抹余晖”“异姓藩镇诸侯”）；BM 609.d（宁、晋起兵）

### `glossary_nesnd_fanzhen`：藩镇 / Military Fiefs

中文：

> #b;italic 藩镇#!是北明割据势力的通称。1425年起，宣德帝猜忌南京留守使郑和，命他再下西洋，分其南京留守之权，又将河北塞兵分驻全国各地，称为“大营”，权归兵部。
>
> 宣德帝死后，正统朝政被武功勋贵把持，各地大营的将领割据城池，开府摄政。北明天子仍维持着朝廷，却无力恢复永乐、宣德时的统一，处境近于中唐、唐末的唐室。

English:

> #b;italic Military fiefs#! is the common name for the regional powers of the Northern Ming. From 1425 the Xuande Emperor, wary of the Nanjing Protector Zheng He, sent him back to the Western Seas and stationed the frontier troops of Hebei across the realm as 'Grand Garrisons' under the Ministry of War.
>
> After his death, military nobles dominated the court, and garrison commanders seized their cities and opened their own administrations. The emperors kept their court but could never restore the unity of the Yongle and Xuande reigns, much like the later Tang emperors.

出处：PPT 5:11–12；BM NC_legacy_of_yanjing_desc（第 1257 行，“割据城池，开府摄政”）；BM_flavor.112.d（第 1460 行）；BM 509.d（中唐、唐末，构思中）

### `glossary_nesnd_central_plains_wars`：中原大战 / Central Plains Wars

中文：

> #b;italic 中原大战#!是北明⟦藩镇→fanzhen⟧诸侯争夺中原的六次大战。第一次（1500—1503）后，诸侯订立凤阳盟誓，中原安定近一个世纪。第二次（1549—1553）后，燕京朝廷再也无法约束诸侯。第三次（1611—1619）打破了凤阳盟誓的秩序。第四次（〔1706—1713〕）中，秦燕联军灭亡北明。
>
> 第五次（1788—1792）与第六次（〔1800—1807〕）中原大战耗尽了各国的人口与粮食。各国户口骤减，从东宁到羌城，民变四起。

English:

> The #b;italic Central Plains Wars#! were six great wars in which the Northern Ming ⟦military fiefs→fanzhen⟧ fought for the Central Plains. After the first (1500–1503), the princes swore the Fengyang Covenant, which kept the Central Plains at peace for nearly a century. After the second (1549–1553), Yanjing could no longer restrain the princes. The third (1611–1619) broke the covenant's order, and in the fourth (〔1706–1713〕) Qin and Yan destroyed the Northern Ming.
>
> The fifth (1788–1792) and sixth (〔1800–1807〕) wars exhausted the people and grain of every state. Registered households fell sharply, and revolts broke out from Dongning to Qiangcheng.

出处：BM 第 737 行（第一次与凤阳盟誓）；PPT 6:5（第二次后燕京体系崩溃）；BM 第 737、4189 行（第三次）；PPT 8:2、BM 508.d（第四次）；列传 p312（第五、六次年份）；列传 p316–317（户口骤减、东宁到羌城）

### `glossary_nesnd_coalition_order`：联军体系 / Coalition Order

中文：

> #b;italic 联军体系#!是北明最后一个世纪的格局（1611—〔1705〕）。宣德年间，郑和以南京留守使镇守江南，郑氏此后世袭吴国公。1443年，天津侯徐祁烨在夺门之变中挟持天子，受封燕国公，又以太师身份掌握京营一部。
>
> 第三次⟦中原大战→central_plains_wars⟧后，秦、燕、吴三国胜出，南京的吴国与天津的燕国南北对垒，各自拉拢关中的秦国，并与楚、蜀、齐等国合纵连横，结成联军。越国在吴越战争（1669—1675）中失去殖民地水师，向南京投降，闽国也向吴国让利求存。

English:

> The #b;italic Coalition Order#! shaped the last Northern Ming century (1611–〔1705〕). Zheng He had held Jiangnan as Nanjing Protector, and his house inherited the title Duke of Wu. In 1443 Xu Qiye, Marquis of Tianjin, seized the emperor in the Gate Coup, became Duke of Yan and commanded part of the capital army as Grand Preceptor.
>
> After the third ⟦Central Plains War→central_plains_wars⟧, Wu at Nanjing and Yan at Tianjin faced each other. Each courted Qin in Guanzhong and built coalitions with Chu, Shu, Qi and other states. Yue lost its colonial fleet in the Wu–Yue War (1669–1675) and surrendered to Nanjing, and Min survived by ceding interests to Wu.

出处：PPT 6:6（联军体系 1611—1705）；PPT 5:9（郑和南京留守使）；列传 p327（郑氏世袭吴国公）；时间线 p5、p26 与 PPT 10:22（1443 夺门之变、燕国公）；BM_flavor.112.d（太师徐祁烨掌京营一部）；BM CEBM_WUU 条（吴越战争 1669—1675）；BM 闽国条（让利求存）

### `glossary_nesnd_overthrow_of_ming`：灭明战争 / Overthrow of the Ming

中文：

> #b;italic 灭明战争#!是第四次⟦中原大战→central_plains_wars⟧中秦燕联军攻灭燕京明廷的战争（〔年份待定〕）。燕国直隶诸军与秦国安北幕府的龙骑军合围北京，齐、吴、楚、蜀、淮、宁六国对秦燕联军宣战。⟦联军体系→coalition_order⟧随之终结。
>
> 北明灭亡后，燕、秦两国君主称帝。南方诸侯在楚国公与淮王带领下，于南京签署《联邦平贼诏书》，由诸侯与士绅推举朱明宗室为帝，建立南明，又称大明联邦。联邦各国偏安之心远大于光复燕京之志，此后与燕、秦维持了数十年的和平。

English:

> The #b;italic Overthrow of the Ming#! was the campaign of the fourth ⟦Central Plains War→central_plains_wars⟧ in which Qin and Yan destroyed the Ming court at Yanjing (〔date pending〕). Yan's metropolitan armies and Qin's Anbei dragoons besieged Beijing, while Qi, Wu, Chu, Shu, Huai and Ning declared war on them. The ⟦Coalition Order→coalition_order⟧ ended with it.
>
> The rulers of Yan and Qin then took the imperial title. At Nanjing the southern princes, led by the Duke of Chu and the Prince of Huai, signed the Edict of Federation against the Usurpers and elected a Zhu prince emperor of the Southern Ming, or Great Ming Federation. Its members preferred security to reconquest and kept the peace with Yan and Qin for decades.

出处：BM 第 2770 行（合围北京、六国宣战）；PPT 8:2、8:4、8:8；PPT 6:11（推举朱明宗室）

### `glossary_nesnd_chinese_revolution`：中华大革命 / Chinese Great Revolution（大革命组主概念）

中文：

> #b;italic 中华大革命#!是19世纪初推翻北方秦、燕两朝的革命。第五、第六次⟦中原大战→central_plains_wars⟧后，各国户口锐减，民变四起。1810年⟦蓝田哗变→lantian_mutiny⟧后，秦国爆发⟦西秦大革命→western_qin_revolution⟧，牧仲棠、吴省等青年军官和士人抓捕秦王，建立共和国。
>
> 1815年，牧仲棠在⟦东征→eastern_campaigns⟧途中回师关中，借⟦鼓楼结社→gulou_society⟧推翻共和政府，杀死吴省。陈东阳等共和派南逃，为吴国主郑钦收纳。1819年，牧仲棠灭燕，在开封宣布废除共和政府，登基称帝，建立中华帝国。次年的⟦南征→southern_campaign⟧受阻于襄阳，南北两朝最终以⟦扬州条约→treaty_of_yangzhou⟧划江而治。

English:

> The #b;italic Chinese Great Revolution#! overthrew the northern dynasties of Qin and Yan in the early nineteenth century. The fifth and sixth ⟦Central Plains Wars→central_plains_wars⟧ had emptied the registers and spread revolt. After the ⟦Lantian Mutiny→lantian_mutiny⟧ of 1810, the ⟦Western Qin Great Revolution→western_qin_revolution⟧ broke out, and officers and scholars led by Mu Zhongtang and Wu Sheng arrested the King of Qin and founded a republic.
>
> In 1815 Mu turned back from the ⟦Eastern Campaigns→eastern_campaigns⟧, overthrew the republican government through the ⟦Drum Tower Society→gulou_society⟧ and had Wu Sheng killed. Chen Dongyang and other republicans fled south to the protection of Zheng Qin of Wu. In 1819 Mu destroyed Yan, abolished the republic at Kaifeng and crowned himself emperor. His ⟦Southern Campaign→southern_campaign⟧ stalled at Xiangyang, and the ⟦Treaty of Yangzhou→treaty_of_yangzhou⟧ finally divided north and south along the Yangtze.

出处：PPT 3:5、10:5（“中华大革命”）；列传 p316–317；PPT 10:5–22、12:4、12:6；MOD flavorCNE.1.d（1819 清理土地后代共和）；MOD flavorCNE.15.d（1835 扬州条约）

### `glossary_nesnd_lantian_mutiny`：蓝田哗变 / Lantian Mutiny

中文：

> #b;italic 蓝田哗变#!是西秦大革命的导火索。秦国的军事地主集团在⟦中原大战→central_plains_wars⟧中穷兵黩武，蓝田等地接连发生贪墨军饷、拖欠军资的案件。1810年，西安青年军官的请愿发展为革命运动。

English:

> The #b;italic Lantian Mutiny#! set off the Western Qin Great Revolution. Qin's military landholding elite had drained the country in the ⟦Central Plains Wars→central_plains_wars⟧, and Lantian and other places saw one case after another of embezzled and unpaid army funds. In 1810 a petition by young officers in Xi'an grew into a revolutionary movement.

出处：PPT 10:5；BM 第 2027、2588 行（同文）。“哗变”一词与具体经过素材未载

### `glossary_nesnd_western_qin_revolution`：西秦大革命 / Western Qin Great Revolution

中文：

> #b;italic 西秦大革命#!是1810年在秦国爆发的共和革命。⟦蓝田哗变→lantian_mutiny⟧后，西安的青年军官推举牧仲棠与士人吴省为领袖，炮轰秦王城，抓捕秦末帝。1812年“东方共和国”成立，几经更名，定为“大汉共和邦”。
>
> 1814年，陈东阳发表《论东方的革命》与《共和宪法》，阐明“万族共和”的主张。1815年3月，以牧仲棠、吴省、陈东阳、邓明舆“共和四子”为首的青年派夺取政权，陈东阳任国家元首周公，吴省任召公。

English:

> The #b;italic Western Qin Great Revolution#! broke out in Qin in 1810. After the ⟦Lantian Mutiny→lantian_mutiny⟧, young officers in Xi'an chose Mu Zhongtang and the scholar Wu Sheng as leaders, shelled the royal palace and arrested the last King of Qin. The Eastern Republic was proclaimed in 1812 and, after several changes of name, became the Great Han Commonwealth.
>
> In 1814 Chen Dongyang published 'On the Eastern Revolution' and the 'Republican Constitution', setting out the ideal of a commonwealth of all peoples. In March 1815 the Young Faction of the 'Four Republicans', Mu, Wu, Chen and Deng Mingyu, took power, with Chen as head of state, the Duke of Zhou, and Wu as Duke of Shao.

出处：PPT 10:5–9；MOD ce_cne_land_reform_reason（1810 西秦大革命，作者原作）

### `glossary_nesnd_gulou_society`：鼓楼结社 / Drum Tower Society

中文：

> #b;italic 鼓楼结社#!是1815年7月推翻⟦西秦大革命→western_qin_revolution⟧青年派政府的密谋集团。青年派推行的土地改革逐渐失控，牧仲棠从前线突然回到关中，在军队与国人的拥戴下，与邓明舆等人秘密结社，发动政变。他们以破坏革命、施行暴政为名，捕杀昔日同窗、革命领袖吴省。陈东阳劝阻无果，逃往南明。
>
> 次年，共和邦更名为“中华联邦”，以“混一寰宇，再兴国族”取代“万族共和，国人革命”为最终目标。邓明舆也举家南逃。

English:

> The #b;italic Drum Tower Society#! overthrew the Young Faction government of the ⟦Western Qin Great Revolution→western_qin_revolution⟧ in July 1815. As the Young Faction's land reform slipped out of control, Mu Zhongtang returned suddenly from the front. Backed by the army and the citizens, he and Deng Mingyu formed a secret society and staged a coup. Accusing Wu Sheng, their schoolmate and fellow leader, of wrecking the revolution through tyranny, they seized and killed him. Chen Dongyang could not stop them and fled to the Southern Ming.
>
> The next year the Commonwealth became the Chinese Federation, and 'Unite the world, revive the nation' replaced 'A commonwealth of all peoples' as its aim. Deng Mingyu then fled south with his family.

出处：PPT 10:9、10:15–17

### `glossary_nesnd_eastern_campaigns`：东征 / Eastern Campaigns

中文：

> #b;italic 东征#!是牧仲棠率共和邦军队对燕国与南明联军的战争（1815—1819）。1815年，他先在洞庭湖、后在徐州击败明燕联军，南明宗室别支朱班博因保全所部声名大振。1818年第二次东征，南明淮王中流弹而死，旧西府军几乎覆没。
>
> 1819年正月，牧仲棠在德州、束鹿击溃燕军，斩燕帝徐柬，进入北京，延续379年的徐燕政权灭亡。燕国宗室、辽东总督徐鼎元逃往辽阳，自称监国，建立东燕。

English:

> The #b;italic Eastern Campaigns#! were Mu Zhongtang's wars for the Commonwealth against Yan and the Southern Ming (1815–1819). In 1815 he beat the Ming–Yan allies at Dongting Lake and Xuzhou, where Zhu Banbo, of a cadet branch of the Ming house, made his name by saving his army. In the second campaign of 1818 the Ming Prince of Huai fell to a stray bullet and the old Western Administration army was nearly wiped out.
>
> In early 1819 Mu routed the Yan army at Dezhou and Shulu, beheaded the Yan emperor Xu Jian and entered Beijing, ending 379 years of Xu rule. Xu Dingyuan, Governor-General of Liaodong, escaped to Liaoyang, proclaimed himself regent and founded Eastern Yan.

出处：PPT 10:12、10:14、10:18、10:22、12:8；“东燕”取 MOD 现用名（PPT 作“辽（北）燕”）

### `glossary_nesnd_southern_campaign`：南征 / Southern Campaign

中文：

> #b;italic 南征#!是⟦东征→eastern_campaigns⟧灭燕之后，中华帝国皇帝牧仲棠统一南北的战役（1820—1822）。他依《南征札记》分兵三路：偏师屯汉中牵制巴蜀，奇兵自徐州、蚌埠南下江淮，他亲率正兵围攻襄阳。朱班博坚守襄阳，萧虎力在剑阁挡住费西翼。
>
> 徐州会战中，郑（德川）家齐统率的南府军坐视西府军覆没。苏宏乘势渡江，却在南京城下被吴国主郑钦击溃。1821年秋，逃亡鄯州的陈秦政权举兵东进，牧仲棠回师兰州破之，秦军残部退守伊犁，号称西秦。南征以失败告终。

English:

> The #b;italic Southern Campaign#! was Mu Zhongtang's attempt to unite north and south after the ⟦Eastern Campaigns→eastern_campaigns⟧ (1820–1822). Following the 'Notes on the Southern Campaign', he split his army in three: one force held Hanzhong against Sichuan, a raiding force struck from Xuzhou into the Huai region, and the emperor besieged Xiangyang. Zhu Banbo held Xiangyang, and Xiao Huli stopped Fei Xiyi at Jiange.
>
> At Xuzhou the Southern Administration army under Zheng (Tokugawa) Jiaqi let the Western Administration army perish. Su Hong crossed the Yangtze but was routed beneath Nanjing by Zheng Qin. In the autumn of 1821 the Qin court in refuge at Shanzhou marched east. Mu broke it at Lanzhou, and its remnants withdrew to Ili as Western Qin. The campaign ended in failure.

出处：PPT 12:10–20、13:4–10；MOD flavorCNE.1.d（1820—22 南征失败，作者原作）；MOD 现文“郑（德川）家齐”写法

### `glossary_nesnd_treaty_of_yangzhou`：扬州条约 / Treaty of Yangzhou

中文：

> #b;italic 扬州条约#!是中华帝国与南明在〔1835〕年签订的条约。⟦南征→southern_campaign⟧失败后，两国以此结束敌对，划江而治。

English:

> The #b;italic Treaty of Yangzhou#! was concluded between the Empire of China and the Southern Ming in 〔1835〕. Following the failed ⟦Southern Campaign→southern_campaign⟧, it ended hostilities and divided the land between the two courts along the Yangtze.

出处：MOD flavorCNE.15.d（1835，作者原作）；PPT 3:5（1839）。条款除“划江而治”外素材未载


## 四、待决清单

### A. 命名与体例（请定）

1. **用词汇表（glossary）还是游戏概念（concept）。** 建议词汇表，理由见第一节。若用概念，键名改为 `concept_nesnd_*`，内容不变。
2. **大革命主概念的名称。** 素材有三种：“中华大革命”（PPT 3:5、10:5；MOD `flavorCNE.15.d` 作者原作）、“关中大革命”（PPT 10 标题）、“西秦大革命”（PPT 15:8、16:6；MOD 作者原作多处）。草稿以“中华大革命 / Chinese Great Revolution”为总称，“西秦大革命”为 1810—1815 年秦国境内的子事件。
3. **“蓝田哗变”素材未载此名。** PPT 10:5 只写“蓝田等地爆发的贪墨军饷、拖欠军资案件。青年军官的请愿发展成革命运动”。草稿沿用任务中的名称，经过、日期和人物都按素材只写到这一步。是否定名“蓝田哗变”，请定。
4. **“鼓楼结社”** 是 PPT 10:15 的原词，指政变组织。是否改叫“鼓楼政变”（素材未载）。
5. **“东征”与 MOD 中其他“东征”同名。** 现有 16 处“东征”全部指吴伐日本（`nesnd_japan`）、西秦东顾（`nesnd_qin_politics`）或哥萨克东进，不插链接。词条名是否改为“牧仲棠东征”之类以免混淆。
6. **任务中的全称素材只部分可考。** 已载：南京留守司、南京留守使郑和（PPT 5:9；BM 第 199、901 行）、吴国公、燕国公、太师徐祁烨（BM_flavor.112.d）、“开府摄政”（BM 第 1257 行）。未载：“辅国”“五军太师府”“南军”“北军”。“五军都督府”在素材中是南明时期郑氏在杭州另立的机构（PPT 9:8，MOD `ce_usm_ruling_of_nanfu_modifier`），不属于北明的燕吴对垒。草稿只用已载部分，并以 PPT 原词“联军体系”命名这一格局。是否采用全称，请定。
7. **东燕的叫法。** PPT 12:8 作“辽（北）燕”，MOD 现文作“东燕”（`nesnd_sha_restore_yan`、`nesnd_sha_republic`）。草稿用东燕。
8. **英文词条名待定：** Military Fiefs（藩镇）、Rebellion of the Frontier Princes（塞王之乱）、Coalition Order（联军体系）、Overthrow of the Ming（灭明战争）、Drum Tower Society（鼓楼结社）、Eastern Campaigns（东征）、Lantian Mutiny（蓝田哗变）。沿用原作的有 Northern Ming、Chinese Great Revolution、Western Qin Great Revolution、Southern Campaign（原作小写 southern campaign）、Treaty of Yangzhou。
9. **“北明”的范围。** 草稿定为 1408 年永乐帝死后到秦燕灭明，并说明 1433—灭明为“北明战国世”（PPT 6:2）。MOD 还用“北明世界”“北明中国”泛指这个架空世界（`flavorCNE.15.d`、`flavorCNE.12.d`、`tooltip_is_modern_china_state`）。这些位置是否链接，草稿默认链接，`tooltip_is_modern_china_state` 是条件提示，默认不链接。
10. **“北明战国世 / 北明战国”作时代名时**（`ce_unification_chinese_culture_desc`、`usm_civilwar.4.d5`）是否把整个词链接到“北明”。默认作专名一部分跳过。
11. **“中唐—五代”的比喻**只见于 BM_events.509.d，该条开头注明“具体设定现在还在构思中”。BM 第 243、1302、1560 行另有“唐末五代”“五代骄兵”的说法。草稿只写“近于中唐以后的唐室”。
12. 任务说“南吴”，素材称吴国、吴国公、郑吴。草稿写“吴”。

### B. 素材互相矛盾（请定，草稿中以〔〕标出或从原作）

| # | 事项 | 说法一 | 说法二 | 草稿 |
|---|---|---|---|---|
| 1 | 永乐帝之死 | 1408 年田猎暴崩（PPT 3:5；BM 第 1133 行；MOD `flavorCNE.15.d`） | 永乐三年（1405）会猎后暴毙（BM_events.16.d、8.d） | 1408 |
| 2 | 北明灭亡 | 1705 年秦燕攻入燕京（PPT 6:2、6:10；BM 第 3207、3234 行） | 灭明战争 1712—1713（PPT 8:2）；1706—1707（BM_events.508.d） | 〔1705〕，灭明战争年份〔待定〕 |
| 3 | 第四次中原大战 | 1706—1713（PPT 8:2；BM 508.d） | 1706—1712（列传 p96） | 〔1706—1713〕 |
| 4 | 第六次中原大战 | 1800—1807（列传 p102、p312；BM 第 2395、3881 行） | “1810年第六次中原大战时”（BM 第 2588 行） | 〔1800—1807〕，蓝田一条不写次数 |
| 5 | 革命爆发 | 1810（PPT 10:5；BM 第 2027 行；MOD 原作 `ce_cne_land_reform_reason`） | 1805（PPT 15:8、16:6）；1805—1808，长安起义 1806（列传 p319） | 1810 |
| 6 | 牧仲棠称帝 | 1819 年 2 月 1 日于开封（PPT 12:4；MOD 原作 `flavorCNE.1.d`） | 1810 年于开封（列传 p102） | 1819 |
| 7 | 扬州条约 | 1835（MOD 原作 `flavorCNE.15.d`） | 1839（PPT 3:5；BM 第 1133 行） | 〔1835〕 |
| 8 | 南征结束 | 1822（MOD 原作 `flavorCNE.1.d`“1820-22年”；`nesnd_sha_restore_yan_reason`） | PPT 写到 1821 年 10 月兰州之战，未写结束年 | 1820—1822 |
| 9 | 吴省 | 吴省（PPT 10:2、10:5、10:8、10:16） | 吴三省（列传 p644、p654） | 吴省 |
| 10 | 燕国公之名 | 徐祁烨（BM、时间线） | 徐祈烨（PPT 5:8、6:14、10:22） | 徐祁烨（MOD 现文也作“祁”） |
| 11 | 秦末帝 | 1810 年被革命军抓捕（PPT 10:5） | 陈炯 1759—1809，死于革命前（列传 p312） | 抓捕，不写名 |
| 12 | 大汉共和邦周公 | 1815 年 3 月陈东阳任周公（PPT 10:8） | “自1818年牧仲棠任大汉共和邦周公（总统）”（MOD 原作 `flavorCNE.11.d`，属共和分支事件） | 陈东阳 |
| 13 | 首义之城 | 西安（PPT 10:5） | 长安（BM 第 2588 行；列传“长安起义”；MOD `SHA_FLAVOR_TEXT`“西秦长安大革命”） | 西安。同一城市，只是称呼不同 |

### C. 素材未载

1. 蓝田哗变的日期、人物、经过（见 A3）。
2. 陈秦宗室何时、如何西逃鄯州。PPT 13:4 只写“临时逃亡鄯州的陈秦政权”。
3. 扬州条约除“划江而治”外的条款与签约人。
4. 郑钦收纳共和派的具体安排。素材只有 PPT 10:20：郑钦不顾各藩反对，大举收纳南逃共和党人，推陈东阳为首辅。草稿只写到这一步。
5. “南军”“北军”称号（见 A6）。


## 五、扫描统计

扫描范围：`localization/simp_chinese` 与 `localization/english` 下全部 .yml（含 `replace/`、`replace/map/`）。脚本 `nesnd-workbench/tools/beiming_glossary_scan.py`，原始结果 `reports/2026-11-12-beiming-glossary/scan.json`。

| 子概念 | 语言 | 可插链接 | 同键非首次 | 专名一部分 | 其他所指 | 已在链接/代码内 |
|---|---|---|---|---|---|---|
| beiming | 中 | 15 | 4 | 5 | 0 | 0 |
| beiming | 英 | 13 | 0 | 6 | 0 | 0 |
| fanzhen | 中 | 9 | 1 | 0 | 0 | 0 |
| fanzhen | 英 | 9 | 1 | 0 | 0 | 0 |
| chinese_revolution | 中 | 8 | 0 | 0 | 7 | 0 |
| chinese_revolution | 英 | 5 | 0 | 0 | 5 | 0 |
| western_qin_revolution | 中 | 8 | 0 | 0 | 0 | 0 |
| western_qin_revolution | 英 | 8 | 0 | 0 | 0 | 0 |
| eastern_campaigns | 中 | 15 | 1 | 0 | 0 | 0 |
| southern_campaign | 中 | 7 | 1 | 0 | 1 | 0 |
| southern_campaign | 英 | 5 | 1 | 0 | 0 | 0 |
| treaty_of_yangzhou | 中 | 1 | 0 | 0 | 0 | 0 |
| treaty_of_yangzhou | 英 | 1 | 0 | 0 | 0 | 0 |

按第四节的默认做法，扣除条件提示 `tooltip_is_modern_china_state`（中英各 1）、`usm_civilwar.4.d5` 的“北明战国”（中 1）和人物引语 `nesnd_crisis.20.f`（中 1），再加上英文换了说法但仍可链接的 3 处，第二轮预计插入**中文 45 处、英文 43 处，共 88 处**，涉及 20 个文件。


塞王之乱、联军体系、灭明战争、蓝田哗变、鼓楼结社在现有文本中出现 0 次（中原大战中文 0 次，英文“Central Plains”4 处均指地理）。它们只作为嵌套子概念存在。

可插链接的分布（按文件，未计“东征”，其 16 处见第七节）：

| 文件 | 处数 | 子概念 |
|---|---|---|
| ce_cne_events_l_simp_chinese.yml | 15 | chinese_revolution×2、beiming×4、southern_campaign×4、western_qin_revolution×4、treaty_of_yangzhou×1 |
| ce_usm_events_l_simp_chinese.yml | 13 | beiming×6、fanzhen×5、western_qin_revolution×2 |
| ce_cne_events_l_english.yml | 12 | southern_campaign×3、western_qin_revolution×4、beiming×3、chinese_revolution×1、treaty_of_yangzhou×1 |
| ce_usm_events_l_english.yml | 12 | beiming×5、fanzhen×5、western_qin_revolution×2 |
| nesnd_cne_land_reform_l_simp_chinese.yml | 7 | chinese_revolution×6、beiming×1 |
| nesnd_cne_land_reform_l_english.yml | 5 | chinese_revolution×4、beiming×1 |
| nesnd_south_politics_l_simp_chinese.yml | 4 | fanzhen×3、beiming×1 |
| nesnd_south_politics_l_english.yml | 4 | fanzhen×3、beiming×1 |
| ce_country_flavor_text_l_simp_chinese.yml | 3 | beiming×2、western_qin_revolution×1 |
| ce_country_flavor_text_l_english.yml | 3 | beiming×2、western_qin_revolution×1 |
| nesnd_crisis_l_simp_chinese.yml | 2 | southern_campaign×2 |
| ce_country_flavor_l_simp_chinese.yml | 1 | western_qin_revolution×1 |
| ce_events_1_l_simp_chinese.yml | 1 | fanzhen×1 |
| nesnd_per_faith_l_simp_chinese.yml | 1 | beiming×1 |
| nesnd_sha_restore_yan_l_simp_chinese.yml | 1 | southern_campaign×1 |
| ce_country_flavor_l_english.yml | 1 | western_qin_revolution×1 |
| ce_events_1_l_english.yml | 1 | fanzhen×1 |
| nesnd_crisis_l_english.yml | 1 | southern_campaign×1 |
| nesnd_per_faith_l_english.yml | 1 | beiming×1 |
| nesnd_sha_restore_yan_l_english.yml | 1 | southern_campaign×1 |

## 六、链接插入样本（10 条）

每条列出该键内全部改动；只有被链接的名词变成 `[Glossary(...)]`，前后文字不动。前 8 条出自作者原作文件（`ce_*`），后 2 条出自代理文件。

**1. `ce_cne_land_reform_reason`**　[ce_cne_events_l_simp_chinese.yml:15](../../localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:15)

- 原：…这一运动发源自1810年的西秦大革命。被本时代人视为农业发达而宗族根深蒂固的东方诸国…
- 改：…这一运动发源自1810年的[Glossary('glossary_nesnd_western_qin_revolution','西秦大革命')]。被本时代人视为农业发达而宗族根深蒂固的东方诸国…

- 原：…权过程中一度中止这一变革。但在1820年的牧仲棠南征前后，为了经济振兴、解放生产和发动底层农民、士兵…
- 改：…权过程中一度中止这一变革。但在1820年的牧仲棠[Glossary('glossary_nesnd_southern_campaign','南征')]前后，为了经济振兴、解放生产和发动底层农民、士兵…

**2. `ce_cne_land_reform_reason`**　[ce_cne_events_l_english.yml:15](../../localization/english/replace/ce_cne_events_l_english.yml:15)

- 原：…movement began with the Western Qin Great Revolution of 1810. People of the …
- 改：…movement began with the [Glossary('glossary_nesnd_western_qin_revolution','Western Qin Great Revolution')] of 1810. People of the …

- 原：…. Around Mu Zhongtang’s southern campaign of 1820, however, he an…
- 改：…. Around Mu Zhongtang’s [Glossary('glossary_nesnd_southern_campaign','southern campaign')] of 1820, however, he an…

**3. `flavorCNE.1.d`**　[ce_cne_events_l_simp_chinese.yml:9](../../localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:9)

- 原：…中华帝国的统治集团起源于那场距今不过二十年的大革命时代。他们目睹了北明藩阀世家在那场宏大的运动中碾…
- 改：…中华帝国的统治集团起源于那场距今不过二十年的[Glossary('glossary_nesnd_chinese_revolution','大革命')]时代。他们目睹了[Glossary('gloss…

- 原：…起源于那场距今不过二十年的大革命时代。他们目睹了北明藩阀世家在那场宏大的运动中碾为尘埃。在此之上，以…
- 改：…olution','大革命')]时代。他们目睹了[Glossary('glossary_nesnd_beiming','北明')]藩阀世家在那场宏大的运动中碾为尘埃。在此之上，以…

- 原：…为他们与军队的密切联络未遭处理。1820-22年南征的失败而导致的战债暴跌更将无数小民家庭推入深渊。…
- 改：…为他们与军队的密切联络未遭处理。1820-22年[Glossary('glossary_nesnd_southern_campaign','南征')]的失败而导致的战债暴跌更将无数小民家庭推入深渊。…

**4. `flavorCNE.15.d`**　[ce_cne_events_l_simp_chinese.yml:158](../../localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:158)

- 原：…《北明战国世》为北明世界中华大革命后，中华帝国太祖牧仲棠幼妹牧沐子中…
- 改：…《北明战国世》为[Glossary('glossary_nesnd_beiming','北明')]世界[Glossary('glossary_ne…

- 原：…《北明战国世》为北明世界中华大革命后，中华帝国太祖牧仲棠幼妹牧沐子中晚年所作小说，…
- 改：…_nesnd_beiming','北明')]世界[Glossary('glossary_nesnd_chinese_revolution','中华大革命')]后，中华帝国太祖牧仲棠幼妹牧沐子中晚年所作小说，…

- 原：…明永乐帝暴崩于田猎，直至1835年南北两朝签订《扬州条约》划江而治以来，中华大地四百余年的历史。由于本书…
- 改：…明永乐帝暴崩于田猎，直至1835年南北两朝签订《[Glossary('glossary_nesnd_treaty_of_yangzhou','扬州条约')]》划江而治以来，中华大地四百余年的历史。由于本书…

**5. `flavorCNE.15.d`**　[ce_cne_events_l_english.yml:152](../../localization/english/replace/ce_cne_events_l_english.yml:152)

- 原：…tang, written after the Chinese Great Revolution in the Northern Ming wo…
- 改：…tang, written after the [Glossary('glossary_nesnd_chinese_revolution','Chinese Great Revolution')] in the [Glossary('gloss…

- 原：…Great Revolution in the Northern Ming world. The work spans f…
- 改：…at Revolution')] in the [Glossary('glossary_nesnd_beiming','Northern Ming')] world. The work spans f…

- 原：…a 1408 hunt to the 1835 Treaty of Yangzhou and the north-south riv…
- 改：…a 1408 hunt to the 1835 [Glossary('glossary_nesnd_treaty_of_yangzhou','Treaty of Yangzhou')] and the north-south riv…

**6. `flavorUSM.1.d`**　[ce_usm_events_l_simp_chinese.yml:18](../../localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:18)

- 原：…地球上象征着东方世界的无限荣光。日月照临下前进的北明诸霸用比汉唐更加激进的尺度丈量自己和世界，永久地…
- 改：…地球上象征着东方世界的无限荣光。日月照临下前进的[Glossary('glossary_nesnd_beiming','北明')]诸霸用比汉唐更加激进的尺度丈量自己和世界，永久地…

- 原：…人类对于世界岛的势力划分。但对于经历了北明数百年藩镇政治的人们来说，朱姓的王朝给神州大地也带来了与它…
- 改：…人类对于世界岛的势力划分。但对于经历了北明数百年[Glossary('glossary_nesnd_fanzhen','藩镇')]政治的人们来说，朱姓的王朝给神州大地也带来了与它…

**7. `flavorUSM.1.d`**　[ce_usm_events_l_english.yml:18](../../localization/english/replace/ce_usm_events_l_english.yml:18)

- 原：…the hegemonic states of Northern Ming measured themselves and…
- 改：…the hegemonic states of [Glossary('glossary_nesnd_beiming','Northern Ming')] measured themselves and…

- 原：…es of Ming-era regional warlord politics, the royal house of Zhu…
- 改：…es of Ming-era regional [Glossary('glossary_nesnd_fanzhen','warlord politics')], the royal house of Zhu…

**8. `ig_xibei_literati_desc`**　[ce_country_flavor_l_simp_chinese.yml:18](../../localization/simp_chinese/replace/ce_country_flavor_l_simp_chinese.yml:18)

- 原：…西秦大革命后，北方的学士们不同于传统的文人士绅，而是在科学…
- 改：…[Glossary('glossary_nesnd_western_qin_revolution','西秦大革命')]后，北方的学士们不同于传统的文人士绅，而是在科学…

**9. `nesnd_south_reconciliation_reason`**　[nesnd_south_politics_l_simp_chinese.yml:137](../../localization/simp_chinese/replace/nesnd_south_politics_l_simp_chinese.yml:137)

- 原：…南朝诸省的军政关系经过陈东阳改制，已不同于北明旧日的藩镇。可是南府与西府之间的积怨，并不会随着…
- 改：…南朝诸省的军政关系经过陈东阳改制，已不同于[Glossary('glossary_nesnd_beiming','北明')]旧日的[Glossary('glossary_n…

- 原：…诸省的军政关系经过陈东阳改制，已不同于北明旧日的藩镇。可是南府与西府之间的积怨，并不会随着一场礼议自…
- 改：…nesnd_beiming','北明')]旧日的[Glossary('glossary_nesnd_fanzhen','藩镇')]。可是南府与西府之间的积怨，并不会随着一场礼议自…

**10. `nesnd_cne_confidence.1.d`**　[nesnd_cne_land_reform_l_simp_chinese.yml:70](../../localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml:70)

- 原：…氏朝廷。他们以“大汉共和军”为号，指斥帝国背弃了大革命的誓言。昔日支持地权革命的人群，正在分裂。…
- 改：…氏朝廷。他们以“大汉共和军”为号，指斥帝国背弃了[Glossary('glossary_nesnd_chinese_revolution','大革命')]的誓言。昔日支持地权革命的人群，正在分裂。…


## 七、不插链接的位置

| 理由 | 文件:行 | 键 | 上下文 |
|---|---|---|---|
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:9 | nesnd_wu_eastern_question_reason | 日本诸侯结下了绵延数代的利害。如今南朝大局已定，朝廷开始议论东征：将西军旧部调往海东，在丰臣之外扶植天皇与德川的政权，使三家 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:10 | nesnd_wu_eastern_question_status | 南京可先遣使议定分封。日本拒议，东征即起。若日本遣使另议，吴廷须在财政、陆军与海军三项中备妥至少 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:12 | nesnd_wu_eastern_question_status_war | 东征已进入[concept_diplomatic_play]或战 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:14 | nesnd_japan_send_terms_desc | 遣使赴日，提议由丰臣、德川与天皇三家各领其土。若日方拒绝，东征随即开始。 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:20 | dp_nesnd_eastern_intervention | 东征日本 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:33 | nesnd_japan.2.d | 日本使者未肯接受分封方案。南京若决意东征，就须筹措军饷、调集舰船，扶持三家接管海东诸藩。朝廷也可以撤 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:34 | nesnd_japan.2.a | 命舰队护送东征军。 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:39 | nesnd_japan.4.t | 东征罢议 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:40 | nesnd_japan.4.d | 东征所需的战局已经结束，分封日本的安排未能施行。舰队与驻军依现有 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:45 | nesnd_eastern_defeat_tt | 吴国在此次东征中退让、战败，或接受日本提出的羞辱要求。 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:46 | nesnd_eastern_defeat_conclusion | 吴廷未能迫使日本接受分封，东征之议至此作罢。 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_japan_l_simp_chinese.yml:65 | nesnd_japan.2.d_commander | _commander').GetFullName]已奉命筹划东征，旧西军的军官将随主帅出海，舰队、军饷和诸藩援军则须由南京调 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_qin_politics_l_simp_chinese.yml:11 | nesnd_qe1_agenda_journal_reason | 伊犁以后，陈秦皇族仍时常东顾玉门，军士和武勋门阀却已不敢轻言东征。帝国需要恢复生产和税收，军府也需要新的兵员与军饷。安国派主 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_qin_politics_l_simp_chinese.yml:15 | nesnd_qe1_army_journal_reason | 军府不愿再为一次仓促的东征耗尽兵力。他们要求先扩充营伍，稳住波斯，向印度与俄国的边地取 |
| 其他所指：吴伐日本、西秦东顾或哥萨克东进，不是牧仲棠东征 | nesnd_sha_far_north_l_simp_chinese.yml:3 | nesnd_sha_far_north_reason | 河弯泊得了船，哪一片草甸初夏就能放马。俄国移民起事、哥萨克人东征以来，那些地方已经换了主人。人却没有走尽。伊尔库茨克和上叶尼 |
| 其他所指 | ce_french_empire_journals_l_english.yml:38 | je_ce_subpress_republican_movement_reason | Since the outbreak of the Great Revolution, an idea of the inseparabilit |
| 其他所指 | ce_french_empire_journals_l_english.yml:41 | je_ce_republican_movement_reason | Since the outbreak of the Great Revolution, an idea of the inseparabilit |
| 其他所指 | ce_french_empire_journals_l_english.yml:44 | ce_french_revolution_base | Legacy of the Great Revolution |
| 其他所指 | ce_french_empire_journals_l_english.yml:144 | fra_unrest.13.d | After the outbreak of the Great Revolution, the [ROOT.GetCountry.GetAdje |
| 其他所指 | ce_french_empire_journals_l_english.yml:180 | fra_unrest.18.d | ns. After the outbreak of the Great Revolution, he fled to England for a tim |
| 其他所指 | ce_cne_events_l_simp_chinese.yml:149 | flavorCNE.14.f | 。自怜湖海三年隔，又作尘沙万里行。欲问后期何日是，寄书应见雁南征。 ——《示长安君》王安石 |
| 其他所指 | ce_country_flavor_text_l_simp_chinese.yml:4 | GBR_FLAVOR_TEXT | 声中，大不列颠步履阑珊地踏入了法国人的世纪。从新大陆的独立到大革命的恐怖，再到拿破仑的兴起，最后是法兰西-明人同盟的全球封锁。 |
| 其他所指 | ce_french_empire_journals_l_simp_chinese.yml:38 | je_ce_subpress_republican_movement_reason | 自从大革命爆发以来，一种民族和民权密不可分的思想就在法兰西民族中深深扎 |
| 其他所指 | ce_french_empire_journals_l_simp_chinese.yml:41 | je_ce_republican_movement_reason | 自从大革命爆发以来，一种民族和民权密不可分的思想就在法兰西民族中深深扎 |
| 其他所指 | ce_french_empire_journals_l_simp_chinese.yml:44 | ce_french_revolution_base | 大革命的遗产 |
| 其他所指 | ce_french_empire_journals_l_simp_chinese.yml:95 | fra_unrest.3.d | 再次试图）赋予有产公民们“尊严、义务和选举权”。从那时开始，大革命和拿破仑浪潮后的专权时代的那种“属于王朝和国家”法国人就消失 |
| 其他所指 | ce_french_empire_journals_l_simp_chinese.yml:144 | fra_unrest.13.d | 大革命爆发后，[ROOT.GetCountry.GetAdject |
| 其他所指 | ce_french_empire_journals_l_simp_chinese.yml:181 | fra_unrest.18.d | 路易 - 腓力是奥尔良公爵路易 - 腓力二世之子。大革命爆发后，他因故一度逃亡英国，在英国与拿破仑议和后又辗转旅居美 |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_english.yml:149 | bm_the_book | Chronicles of the Northern Ming Warring States |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_english.yml:151 | flavorCNE.15.t | lication of Chronicles of the Northern Ming Warring States |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_english.yml:152 | flavorCNE.15.d | Chronicles of the Northern Ming Warring States is a late-life |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_english.yml:153 | flavorCNE.15.f | ng verse of Chronicles of the Northern Ming Warring States |
| 专名一部分（书名或“北明战国世”） | ce_events_1_l_english.yml:16 | ce_unification_chinese_culture_desc | With the end of the Northern Ming Warring States age, people ha |
| 专名一部分（书名或“北明战国世”） | ce_usm_events_l_english.yml:200 | usm_civilwar.4.d5 | nce. In four hundred years of Northern Ming Warring States, a great state |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_simp_chinese.yml:155 | bm_the_book | 《北明战国事》 |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_simp_chinese.yml:157 | flavorCNE.15.t | 《北明战国世》出版 |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_simp_chinese.yml:158 | flavorCNE.15.d | 《北明战国世》为北明世界中华大革命后，中华帝国太祖牧仲棠幼妹牧沐子 |
| 专名一部分（书名或“北明战国世”） | ce_cne_events_l_simp_chinese.yml:159 | flavorCNE.15.f | ，霸主分国东风紧，逐鹿大将堆骸骨，襄阳梦华花落屏。 ——《北明战国事》开篇词 |
| 专名一部分（书名或“北明战国世”） | ce_events_1_l_simp_chinese.yml:16 | ce_unification_chinese_culture_desc | 随着北明战国世的终结，人们已经厌恶了诸候藩镇军阀之间无休止的争权夺利 |
| 同键非首次 | ce_usm_events_l_english.yml:33 | flavorUSM.4.d | fighting and the exactions of military governors and transport officials.  A |
| 同键非首次 | nesnd_crisis_l_english.yml:47 | nesnd_crisis.20.d | shed land reform would make a southern expedition more burdensome still. What c |
| 同键非首次 | ce_cne_events_l_simp_chinese.yml:158 | flavorCNE.15.d | 、各个人群中塑造人物。用类似近代历史小说的手法了从1408年北明永乐帝暴崩于田猎，直至1835年南北两朝签订《扬州条约》划江 |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:18 | flavorUSM.1.d | 己和世界，永久地改变了人类对于世界岛的势力划分。但对于经历了北明数百年藩镇政治的人们来说，朱姓的王朝给神州大地也带来了与它荣 |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:33 | flavorUSM.4.d | 年前的大宪战争中大获全胜的天津燕主及其国势还如烈火烹油。堪称北明战国末期的天下之雄。但郑氏的执拗战胜了朝臣的规劝和敌人的威胁 |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:33 | flavorUSM.4.d | 规劝和敌人的威胁。终于在同年六月成行。  这次觐见是一场北明从藩镇时期到诸侯时期近三百年来都未有人见过的盛大巡游。虽然吴 |
| 同键非首次 | ce_usm_events_l_simp_chinese.yml:33 | flavorUSM.4.d | 以及又用了近万名民夫运送的安南、高棉贡米。与之相对的，则是在藩镇节度使制度下被小规模械斗和转运使卡要下，四时常乱，在饥荒边缘 |
| 同键非首次 | nesnd_crisis_l_simp_chinese.yml:47 | nesnd_crisis.20.d | 世。国内政务仍须军队与财力维持，地权改革若尚未完成，更难兼顾南征。此时卷入南朝的混战，究竟能为帝国赢得什么？ |
| 同键非首次 | nesnd_japan_l_simp_chinese.yml:9 | nesnd_wu_eastern_question_reason | 其土，九州、四国则归吴朝直辖。远洋驻军与海上商路，都押在这次东征上。  交涉期间，日本若重新臣属于吴朝，吴廷即按分封之议 |

### 另需决定：中英文对应的写法不同

下列键中文有可链接的名词，英文对应句换了说法。默认做法写在右栏，请确认。这会使两种语言的链接数不相等。

| 键 | 中文 | 英文现文 | 默认 |
|---|---|---|---|
| flavorCNE.1.d | 大革命时代 / 北明藩阀世家 | “the great revolutionary era” / “the old military clans” | 英文把 great revolutionary era 链到中华大革命；military clans 不含“北明”，不链 |
| nesnd_cne_republic_journal_reason | 重建大革命尚未完成的共和国 | “complete the unfinished revolution” | 链 revolution |
| nesnd_cne_confidence.3.d | 大革命以来统一国家的主张 | “the revolutionary claim to national unity” | 形容词，不链 |
| ce_cne_war_with_usm_reason | 南征统一之大势 | “southern unification drive” | 链 southern unification drive |
| nesnd_crisis.20.f | 若朝廷复议南征（人物引语） | “another march south” | 引语中的“复议南征”指再次出兵，不是历史事件本身，中英文都不链 |
| usm_civilwar.4.d5 | 北明战国四百有余年 | “Northern Ming Warring States” | 同 A10 |

英文“Great Revolution”在 `ce_french_empire_journals` 5 处、中文“大革命”在法国日志 6 处和 `GBR_FLAVOR_TEXT` 1 处，都指法国大革命，已排除。`flavorCNE.14.f` 的“雁南征”是王安石诗句，已排除。

## 八、顺带发现的其他问题（未改）

1. `localization/english/replace/ce_cne_events_l_english.yml:9`（flavorCNE.1.d）：“Then, he the great led the founding of our great empire” 语法残缺。
2. `localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:158`（flavorCNE.15.d）：“用类似近代历史小说的手法了从1408年”多一“了”；“全书分为五大，十小卷”逗号位置。两处均是作者原作，沿自 PPT 3:5。
3. “诸候”应为“诸侯”：`ce_events_1_l_simp_chinese.yml:16`、`ce_cne_events_l_simp_chinese.yml:159`（后者是引用的书中开篇词）。
4. `localization/english/replace/ce_usm_events_l_english.yml:89`、`:115` 把南府译作 “Southern Office”，与制度定译 “Southern Administration” 不一致。
5. 南征的英文有 “southern campaign”（作者原作 3 处）与 “southern expedition”（`nesnd_crisis.20.d` 2 处）两种。
6. MOD 内部年代不一致：`flavorCNE.11.d` 写 1818 年牧仲棠任大汉共和邦周公，`flavorCNE.1.d` 写 1819 年帝国代共和而立（见 B12）。

## 第二轮要做的事（确认后）

- 新增 `common/glossary/nesnd_beiming_glossary.txt`（13 条，UTF-8 BOM）与 `localization/{simp_chinese,english}/replace/nesnd_beiming_glossary_l_*.yml`。
- 按第五节的可插链接逐键插入，每键每个子概念只链第一处，显示文字保持原词。
- 检查 BOM、重复键、中英键名一致，跑 pdx.py 与 audit.py，交付说明列出改动文件与跳过位置。
