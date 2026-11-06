# 作者样本

全部取自 Git tag `original-20261030`（提交 `f18b6c4`），即 AI 参与前的作者原作。读全文：`git show original-20261030:localization/simp_chinese/replace/<文件>`。

文件：
- `ce_french_empire_journals_l_simp_chinese.yml`（法兰西帝国链：日志、按钮、进度条、事件）
- `ce_cne_events_l_simp_chinese.yml`（沐帝国 / 地权革命）
- `ce_usm_events_l_simp_chinese.yml`（明 / 吴）
- 英文同名文件在 `localization/english/replace/`

## 日志正文：历史来路 + 立场 + 一个问题

> **je_ce_unstable_imperium_reason**：自1832年拿破仑三世登基以来，好大喜功又思想活跃的第三代波拿巴皇帝在法国内部同时推动多项改革，并在这个过程中激进地对各类“重大工业部门”挥洒税款。似乎只要向工业经济注入足够多的资源，就能让整个法国乃至欧洲自动变成他承诺的“和平且伟大之地”。事实真能如此吗？就算法国真的那么伟大，这个法国中又有没有拿破仑们的位置呢？

> **ce_cne_land_draft_failing_reason**：掌握权力的中华帝国统治集团是以牧氏家族为核心的武勋贵族集团，以及围绕着他们成长起来的一批新派士绅。他们对摧毁了华北秦燕帝国的西秦大革命记忆犹新，因此在一定程度上愿意对社会下层让利以自保。然而，随着时间的推移与势力内部的斗争，理智和恐惧会同时衰退。

“好大喜功”“挥洒税款”是叙述者的判断。作者也用“然而”，但用在真正的转折处（统治集团从让利走向反对），不是为平衡口气。

## 事件正文：具体的人和利益

> **flavorCNE.4.d**：地权革命是经济上的革新，同样也是一项冷酷的政治运动。它要将一整个旧社会窃夺数千年的利益，转移到诞生不过数十年的新贵手中。这一过程不仅仅是金钱赎买就能结束的，必然存在法律机关的追捕、诓骗、来回的争夺、执行者的背叛，甚至是残酷的暴力手段。

> **flavorCNE.3.d**（节选）：随着旧宗族和土地不再能锁住农民，无数稚嫩、满是灰土却充满朝气的脸孔源源不断地从郊野涌入城市。他们憧憬新的生活。

手段逐项列出（追捕、诓骗、背叛、暴力），利益写清从谁转给谁。

## 标题、引文、选项

| 键 | 原文 | 注 |
|---|---|---|
| fra_unrest.4.t | 异梦同床 | 成语点题 |
| flavorCNE.4.t | “万民书” | 点出文书 |
| fra_unrest.13.f | “小小拿破仑，治国靠佞臣。岛夷非正主，依旧让民权！” | 街头口号作引文 |
| flavorCNE.4.f | 天杀尤无奈，地卷不能逃。岁末小积蓄，官人何忍收？ | 民谣 |
| fra_unrest.12.f | ……“传统，”他们说。另外成千上万的人发誓要焚烧尸体。“霍乱，”他们说。 | 讽刺的对照 |
| flavorCNE.4.1 / .2 | 胡言乱语，正不必忧心。 / 风头正盛，需暂避锋芒。 | 两种态度，各一句 |
| fra_unrest.16.1 | 有人要被畏罪自杀了。 | 黑色幽默 |
| fra_unrest.13.2 | 他们骂小拿破仑跟我[…统治者姓名…]有什么关系？ | 统治者本人开口 |

## 按钮、进度条、修正

| 键 | 原文 |
|---|---|
| ce_french_support_dynasty_button_desc | 波拿巴的道路是[ROOT.GetCountry.GetAdjective]民族团结和繁荣的唯一办法。 |
| ce_french_freeze_republican_movement_with_institution_2_desc | 面包和马戏永远不过时。 |
| ce_french_republican_hit_economy_desc | 正义的事业总不缺支持者。 |
| ce_french_stability_increase_50_tt | 稳定度变化：#g +50#! |
| ce_republican_power_20 | 共和呼声进度达到#g 20%#!进度 |
| push_land_reform_forward_15 | #BOLD 地权革命#![concept_journal_entry]的进度#bold 增长15点#! |
| FRA_ce_french_internal_victory | 拿破仑繁荣 |
| ce_lose_the_monarchist_way | 君主主义下水道 |

## 英文（作者原作）

| 键 | 原文 |
|---|---|
| fra_unrest.4.t | Strange Bedfellows |
| fra_unrest.16.1 | Someone is about to 'commit suicide' to escape punishment. |
| ce_french_freeze_republican_movement_with_institution_2_desc | Bread and circuses never go out of style. |
| flavorCNE.4.1 | Nonsense - no need to worry. |
| FRA_ce_french_internal_victory | Napoleonic Prosperity |

## 对照：代理稿（2026-11 当前文件）

> **nesnd_cne_land_journal_reason**：……新法准许土地流转，也让经营农业的商人有了扩张的机会。然而，一纸买卖契约并不能使失去田地的人立即找到新的营生。田庄改作、雇工与迁居带来的争执，将伴随这场变革走进乡村。

> **nesnd_journal_closures_parent_cne**：此项事务随“地权革命”一同结束。

前一句语法通顺，但每个好处都配一个代价，没有叙述者的判断，也没有具体的人；后一句是开发者对日志生命周期的说明，不该出现在游戏里。
