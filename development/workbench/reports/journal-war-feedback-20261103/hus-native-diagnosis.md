# HUS“消灭君主制”原生日志：只读诊断

日期：2026-11-03。版本：Victoria 3 **1.13.11 / Steam build 24799966**。本次再次运行 NESND `catalog.py status`，返回 `CURRENT / changed_count=0`。

状态：`SOURCE_DIAGNOSIS / ENGINE_NOT_RUN`。本子任务只读源码、写本报告；未改玩法、未启动游戏、未读新的用户存档。用户截图所述条件与当前原版日志相符，但没有截图所属存档的完整政体史、JE实例创建日期或运行日志，故不能把“已找到可疑源码入口”说成“已复现该存档的触发过程”。

方法：按 NESND 技能、`docs/agents/engineering-skills.md` 与 Matt diagnosing-bugs 的双层反馈执行。用户明确只读且不启动游戏，本轮不构造虚假的 Python 游戏替身；源码证据用于区分入口，真实 red/green 留给以后的一次定向存档验证。未完成引擎复现的边界是本报告结论的一部分。

## 结论与建议

这是原版 **`je_abolish_monarchy`**，不是 MOD 自制同名JE。原版用途确实包括**已经成为共和国以后，持续削弱君主派、巩固共和**；所以“当前是总统共和”本身不能证明日志错误。其完成事件正叫“最后的君主派”，描述维持共和多年后的结果。[S1][S2]

HUS则有独立的设计依据：当前MOD的国家定义称“华夏东洲共和国”，开局明确激活总统共和；原稿风味文本把其起源追溯到1644年起义，并描述共和主义者长期倚重它。若用户确认这局没有后来复辟—再共和，则将其当作刚废除君主制的新共和国不符合本MOD设定。[M1][M2]

**最直接的可达问题链已找到：**HUS历史调用 `effect_starting_politics_liberal`，其中激活总统共和，随后历史又显式激活一次总统共和；原版总统共和 `on_activate` 无条件调用 `transition_off_of_monarchy_effects`，该effect的“加入消灭君主制JE”分支只检查没有该JE、没有 `monarchy_stamped_out_var`，不核前政体、是否曾为君主制、是否处于历史初始化。[M1][S3][S4] 这是**MOD开局法律配置接入原版过宽改制入口**的源码风险，不是MOD自建JE。初始化期间回调的实际时序尚无本局证据，不能把它写成已确定发生的运行事实。

**异名global不是本条JE的直接重复添加来源。**原版是 `common/history/global/00_global.txt`，MOD是 `common/history/global/ce_global.txt`；MOD元数据未声明替换该历史目录，它们是不同相对路径，不能认为后者替掉前者。但本次对两文件完整搜索 `je_abolish_monarchy`、`abolishing_monarchy_var`、`transition_off_of_monarchy_effects`、两个消灭君主制完成标记，均无命中。两个文件也没有给HUS设置“曾是君主国”的标记。原版global第20–26行只是给君主制+专制国家设置 `king_in_parliament_possible`，不是本JE入口。[S5][M3]

可以在MOD用 **`REPLACE:je_abolish_monarchy`** 作限定HUS的修复，保留其他国家原有流程。显式 `add_journal_entry` 会忽略 `possible` 和 `is_shown_when_inactive`，所以**只加隐藏/不可用条件不能阻止本问题，更不能清掉旧档活跃JE**。必须包含HUS限定的 `invalid`，并保护计数与完成副作用；具体最小方案见后文。[S6][M4]

## 可证伪假设与本轮核查结果

| 假设 | 预测 | 当前证据/边界 |
| --- | --- | --- |
| 1. HUS开局激活共和法时走原版通用改制effect | 主MOD没有自制同名JE；历史到原版法律存在完整调用链，effect不核旧政体 | 源码证据成立；初始化是否执行这次回调及存档创建日期未证实。为首要入口嫌疑。 |
| 2. 原版global与MOD异名global重复直接添加该JE | 两文件至少存在同一个add JE或调用添加effect的语句 | 完整检索无命中，排除这对文件“直接重复添加本JE”的说法。不能据此排除全项目其他历史重复问题。 |
| 3. 玩家/AI在本局曾真实恢复君主制后又共和，或经历反君主革命 | 存档/日志可找到该次法律变更或反君主革命；原生调用者有相应入口 | 原版存在这些正常入口；没有当前存档历史，不能排除。但不得以此推翻作者对HUS长期共和的既定设计。 |
| 4. MOD改了原版JE内容或直接将本JE加入HUS | MOD JE、事件、历史、on_action或scripted_effect有该ID调用/覆盖 | 本次完整搜索这些目录没有相关命中；当前MOD未覆盖原JE、通用改制effect或原版政体法律同路径文件。 |
| 5. “总统共和”只改显示，实际法律还是君主制 | 历史只变government name而未激活共和法 | 源码反证：HUS第69–70行确实使用原生`activate_law=law_presidential_republic`；截图条件也与原版共和巩固逻辑吻合。当前存档法律仍以实际存档为准。 |

## 原版完整链条

### JE定义、计数、退出与奖励

[GAME/common/journal_entries/00_abolish_monarchy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_abolish_monarchy.txt:2>)：

- ID `je_abolish_monarchy`；图标 `gfx/interface/icons/event_icons/event_portrait.dds`；组 `je_group_internal_affairs`，是country-context普通内政JE，不是contextless全球日志。文件没有`possible`或`is_shown_when_inactive`入口，靠调用者显式添加。
- `on_monthly_pulse` 第7–34行：不是君主制、没有进度≥0.75的革命、没有强势且对君主法态度高于neutral的IG，才把 `abolishing_monarchy_var` 加1。`country_has_monarchy_law`实际包含`law_monarchy`和`law_social_monarchy`，吻合截图。[S7]
- 第95–103行：`current_value=root.var:abolishing_monarchy_var`，目标增量60，显示进度条。**脚本只在合格月加1，没有else归零**；源码表达的是60个满足条件的月，不能擅自承诺必须连续60个月或不满足就清零。
- `complete` 第36–56行：目标完成且上述当下条件仍成立。
- `immediate` 第58–62行只保存可存在地主IG为`landowners_ig`；计数初始化为0由调用者负责。
- `invalid` 第84–93行：既没有正在制定总统/议会/委员会共和，也没有这三类现行法及其variant才失效。**现有总统共和当然不会触发该原生失效条件**，所以误加入HUS以后不会仅因“早已共和”自动消失。
- `on_complete` 第64–74行：设 `stamped_out_monarchy_var`，触发`1848.2`；若仍有中国军阀JE，还会调用`chi_add_1_fragile_unity`并设`china_warlord_abolished_monarchy`。

完成事件 [GAME/events/1848.txt:115–180](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/1848.txt:115>) 不是纯通知：

- `.2.a` 第143–169行移除地主多种家长主义意识形态（包括`ideology_scholar_paternalistic`），加`ideology_republican_paternalistic`，设 **`monarchy_stamped_out_var`**，并把所有君主主义IG领袖改为温和派。
- `.2.b` 第171–179行给地主`monarchist_nostalgia`临时修正，保留君主派可能。
- **两个名字不同的flag是不同用途，不要“修错字”合并：**`stamped_out_monarchy_var`由JE完成设置，原版成就读取；`monarchy_stamped_out_var`由`.2.a`选择设置，控制通用effect不再加JE，以及君主派意识形态/运动资格。
- 因此用`set_variable=monarchy_stamped_out_var`给HUS挡入口，会额外改变人物和政治运动资格，不能作为无副作用清理替代。

### 全部已定位的显式添加入口

| 调用者 | 源码守卫/副作用 | HUS相关性 |
| --- | --- | --- |
| `on_law_enactment_started` | [00_code_on_actions:4442、4473–4488](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:4473>)：当前`has_law=law_monarchy`且正在制定公司国/总统共和/议会共和/委员会共和；计数0再add JE | 真正从君主制改制的正常入口，不能因为当前已共和就全局停掉。该入口与JE invalid对公司国的名单差异是原生相邻问题，本次不扩修。 |
| `on_civil_war_won` | [同文件:5743–5769](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5743>)：有`anti_monarchist_revolution`且当前非`law_monarchy`，计数0再add，随后移除革命标记 | 标记来源为`on_revolution_start`第5156、5183–5192行，检查当时君主制与革命目标非君主制。真实内战转型应保留。 |
| `transition_off_of_monarchy_effects` | [00_victoria_ep2_scripted_effects:2647–2677](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2647>)：先王室地产处理、幕府法律处理、宪政主义IG转共和主义；随后无JE/无`monarchy_stamped_out_var`就设0并add | **没有前政体/曾为君主制/日期守卫。**HUS历史直接activate总统共和可连接到此入口。不能为禁止JE而删掉整个effect，其他合法副作用须保留。 |
| 巴西`pedro.8`相关结算 | [pedro_brazil_events:649–653](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/brazil/pedro_brazil_events.txt:649>)：政变/废君结算显式计数0、add JE | 巴西专属链，未发现MOD把该事件接到HUS；保留。 |

总统共和`on_activate`见 [00_governance_principles:374–384](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt:374>)；议会共和第521–531、委员会共和第842、公司国第940也调用同一通用effect。这里所谓“on_activate”是法律数据库中的effect，不要与`on_actions`里同名概念混为scope相同的接口。

另有原生`on_law_activated`回调：[00_code_on_actions:5020–5033](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5020>)明确 **root=law、owner=国家**，法律经正常制定或脚本直接activate都会执行；此时`currently_enacting_law`为空。这给未来记录“真实采用君主制”的自有标记提供接口，但不能在law root直接写国家条件。它的注释不单独证明本局历史加载期间实际先后次序。

### “曾为君主国”与历史初始化

本次搜索当前GAME/common、MOD/common及本机引擎triggers目录，没有找到 `has_been_monarchy`、`has_been_a_monarchy`、`has_ever_been_monarchy`、`has_had_law`等可据此使用的原生历史谓词或现成国家变量。不能凭旧版本印象为当前补一个不存在的接口。

本JE不核“曾是君主国”，已知通用添加effect也不核。旧存档即使碰巧保留某个旧版本同名变量，在没有当前读者的情况下也不能证明它是本条JE的来源或正确清理守卫。

## HUS当前源码与长期停滞的额外原因

- [MOD国家定义:37–45](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:37>)称“华夏东洲共和国”，HUS为recognized、首都加州；[原稿风味:12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:12>)提供1644起义与共和主义者背景。它不是原版法国那种刚废君主的默认历史。
- [MOD HUS历史:69–85](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:69>)调用自由开局政治，然后明确总统共和、资格选举等。原版自由开局政治 [00_political_setup:3–18](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_political_setup.txt:3>)自身第一项就是总统共和。两次相同activate是冗余，**不能断言会创建两个JE**：通用effect已查`has_journal_entry`，第二次是否执行on_activate也未实测。
- 本次MOD目录没有`00_abolish_monarchy.txt`、`00_governance_principles.txt`、`00_political_setup.txt`、`00_code_on_actions.txt`的同路径覆盖，也没有`je_abolish_monarchy`/通用effect的同名REPLACE；相关调用仍来自上述原生链。
- HUS历史第34–37行给军方共和主义；第47–54行给地主/士绅`ideology_scholar_paternalistic`、农业主义和自由主义，且在阁。原版 [00_ig_ideologies_flavored:40–50](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:40>)的士绅家长主义**强烈支持君主制**、对总统/议会共和中立。如果该IG在存档中强势且实际合成态度支持君主制，便会挡住本JE的月度计数。这是“为何不结束”的源码解释候选，不是“为何被加入”的入口证据，也不是授权改变HUS士绅设计。
- 角色 [HUS_Guo_qingda:1092–1105](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_historical_leaders_ce_asia.txt:1092>)是统治者与实业家领袖、激进主义；没有本JE调用。`nesnd_crisis.21`只是外援政策入口，未改HUS政体。

## 最小MOD修复合同

### 优先：单条JE的HUS限定兼容修复

在独立前缀文件用 `REPLACE:je_abolish_monarchy = { 完整原生定义加局部守卫 }`。本项目已使用该数据库的REPLACE（如`REPLACE:je_splitting_oman`、印度原生日志）；这是整个对象的替换，不能只写一个新的`invalid`块便假定其余字段自动保留。[M4]

目标谓词应表达“这是HUS已确认不适用的旧共和巩固任务”，而不是“所有共和国”或“所有非君主国”。最窄的本次兼容选择是HUS限定失效；它会取消HUS将来真实废君主后的同一原生JE，必须在交付中明确这个边界。**更保守、建议采用的版本**是加一个本MOD自有的“本局HUS真实君主制度已观察”标记：

1. 对作者确认长期共和的HUS，不凭当前共和国状态反造其历史；新局不设该标记。
2. 后续HUS实际采用君主制或社会君主制时，通过`on_law_activated`的`owner`记录该标记；月度只作迁移/补漏，不能作为唯一记录入口（可能漏掉同月内脚本改制）。若游戏初始化也出现临时默认法律，必须限制“正式开局完成后”的记录入口并做一次定向验证，避免把初始化默认君主制误当真历史。
3. JE中“非HUS或有该真实转型标记”允许原生玩法；HUS且无标记走清退。与本次问题有关的旧档按作者确认的长期共和处理；若以后取得存档证据确曾复辟，就为该局保留转型资格，不把所有旧HUS档都概括成从未君主制。
4. 在`invalid`把该HUS清退条件与原生invalid作`OR`。同一HUS守卫也覆盖`on_monthly_pulse`计数、`complete`及`on_complete`副作用，避免invalid与complete同次评估先后尚未确认时发出奖励。非HUS分支原逻辑不变。
5. `on_invalid`对本次受影响HUS最多清理只供该JE使用的`abolishing_monarchy_var`，不设置任何完成奖励flag、不触发1848.2、不改IG/法律/人气/激进派。`current_value`也应对缺计数安全返回0，避免清理后同帧/UI继续求值报错。

如果本轮只需立即消除这条误入的HUS日志，**不要为此覆盖整个法律数据库、所有共和国家或全部on_actions**。为了精确保留将来真实HUS转型，新增记录标记比全世界“曾为君主”迁移要窄；它仍是一项需要验证事件顺序的实现选择，本报告未实施。

### 如需同时修入口

可以在MOD侧局部替换 `transition_off_of_monarchy_effects`，完整保留原effect前半的王室土地、法律和意识形态处理，只给末尾“设0+add JE”分支加上相同HUS资格守卫。项目`common/scripted_effects/ce_japan_gov_effects.txt`已有此数据库`REPLACE:`用例。该修改防止未来HUS共和法重新激活时反复加入错误JE，但**它本身不会移除已经活跃的旧JE**，仍需上面的invalid清退。

不要仅把 `effect_starting_politics_liberal` 改成别的预设；那会改变HUS大量法律。删去历史中第70行冗余activate只能去重一个调用位置，不能阻断第69行预设的同一入口。不要添加`monarchy_stamped_out_var`伪装已完成；不要直接执行1848.2“领一次奖励再结束”。

如添加on_action记录，不可在已有`on_law_activated`上另写第二个effect块。原版 [_on_actions.md:115–128](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/_on_actions.md:115>)明确允许附加`on_actions={本MOD回调}`，由独立回调承载effect。

## 旧档清退的能力与副作用边界

官方 [journal_entries.md:148–158](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:148>)声明`invalid`使条目静默消失并执行`on_invalid`。第13–14、33–34行同时声明显式添加绕过inactive/possible；第422–424行说明possible变false不默认把活跃JE退回inactive。因此上述invalid是正确的数据库层旧档退出接口，不能以“隐藏了”宣称“清退了”。

本机effects文档没有检到可直接使用的`remove_journal_entry`效果，不能臆造。用已有JE的`invalid`路径最符合当前官方接口。

**尚未执行的实际验证：**加载旧档后何时重新求invalid、是否在下一更新tick消失、不会同tick先complete、是否已有1848.2事件排队/打开。这些不能用静态检查认证。若1848.2已在队列，其状态独立于JE；本次用户仅报告活跃JE，没有证据授权回滚已完成奖励或全局禁事件，先保护JE未来副作用，遇到已有事件实例另作限定HUS的取消处理。

## 后续验收：只测这条闭包

| 场景 | 本地可检查 | 引擎应观察 |
| --- | --- | --- |
| HUS既有长期共和活跃JE，进度0/59/60 | HUS拒绝谓词同时保护计数、complete、on_complete；invalid为真；计数缺值安全 | 日志静默消失；不弹1848.2；不设置两种完成flag；IG/领袖不变。 |
| HUS重新激活同一种共和法/总统转议会 | 通用入口局部守卫与JE守卫一致；不重置其他国家计数 | 错误JE不再出现/不反复闪现；不修改现行制度。 |
| HUS将来真君主→共和 | on_law_activated进入owner，正式开局后才记真实君主；原生完成链保留 | 标记及时记录，随后原生60月巩固可用；同月脚本变法不漏记。 |
| 非HUS君主改革、反君主革命、巴西专属结算 | 新旧保序AST比较：除HUS条件以外原入口、计数、奖励等价 | 原生JE照常加入/推进/结束；法国和中国关联不被禁用。 |
| 旧档已曾复辟但缺新标记 | 不能靠当前法推断过去；检查存档历史再定兼容值 | 确认真实转型被保留，不能强制当长期共和清退。 |
| UI/存读档/无计数变量 | `current_value`缺值分支返回0；清理只作用HUS | 不报变量/作用域错误；未完成奖励不误发；读档不复活错误任务。 |

源码检查能确认的结论仅为“入口与守卫按定义闭合”，不能写成“已经修好截图那一局”。本轮不重复启动观察者长局，也不扩大到其他原版JE。

## 来源补充与指纹

- **S1** JE完整定义：`GAME/common/journal_entries/00_abolish_monarchy.txt:2–109`，见前述链接。
- **S2** 原版中文标题/意图：[content_1_l_simp_chinese.yml:1206–1214](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/content_1_l_simp_chinese.yml:1206>)。
- **S3** 原版自由预设、政体法律调用，见“完整链条”和“HUS当前源码”。
- **S4** 通用改制effect：`GAME/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2647–2677`。
- **S5** 原版global：[00_global.txt:1–26](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/global/00_global.txt:1>)；本次完整文件关键词搜索无本JE调用。
- **S6** 官方JE触发/失效规范：[journal_entries.md:13](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:13>)、33–34、148–158、422–424。
- **S7** [country_has_monarchy_law](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt:13>)包含普通君主制和社会君主制。
- **M1/M2** HUS国家定义、国家历史、原稿风味与人物模板，见前述各本地链接。
- **M3** MOD异名global：[ce_global.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/global/ce_global.txt:1>)；[元数据](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.metadata/metadata.json:1>)未声明目录替换。
- **M4** 已有JE REPLACE：[zzzz_nesnd_native_error_bans.txt:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/zzzz_nesnd_native_error_bans.txt:2>)；scripted_effect REPLACE：[ce_japan_gov_effects.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/ce_japan_gov_effects.txt:1>)。先例表明项目可按该数据库做定点覆盖；本报告未对新候选执行引擎加载验证。

本次读取时SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| GAME `common/journal_entries/00_abolish_monarchy.txt` | `1d8ac88eea45b13e035e5a1c15567f48a06de069fe386305b2e4bbc639ddd138` |
| GAME `common/scripted_effects/00_victoria_ep2_scripted_effects.txt` | `5eb6dca67e7647b4d09dbeb1c22e0ab2b68cee66c04a7476375c581f074191dc` |
| GAME `common/laws/00_governance_principles.txt` | `e676448ea64c17079677ddbf2cbfdbec0ffdefa465286f16c1e6107a14e7f4cf` |
| MOD `common/history/countries/HUS.txt` | `cb1485aa1ec06d0706806a9dbbdb6ab458ea78cbf796ac506a2482c6ecb33608` |

引用检查：24条本地来源链接均存在，所引用起始行在文件范围内；这只证明来源可定位，不是引擎验证。当前研究没有创建新技能规则，没有改写HUS制度、士绅意识形态或原版文件。此报告供主任务准备具体修复候选与限定验收。
