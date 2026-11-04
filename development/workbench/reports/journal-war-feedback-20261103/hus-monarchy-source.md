# HUS原生“消灭君主制”：本批源码核对与最小修复建议

2026-11-03；本机Victoria 3 **1.13.11 / Steam build 24799966**；`catalog.py status`再次返回`CURRENT / changed_count=0`。依据NESND、项目工程适配及research流程，只读当前GAME/MOD和引擎文档，未修改游戏文件、未启动游戏。状态：`SOURCE_RESEARCH / ENGINE_NOT_RUN`。

本报告复核此前[完整诊断](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/journal-war-feedback-20261103/hus-native-diagnosis.md>)，新增了原版法律用`has_game_started`隔离历史初始化的实际实例。四项关键源文件SHA与此前一致。截图没有附带本局法律历史、JE创建日期或新存档，不能把源码入口推断说成已复现截图那一局。

## 结论

- ID是原版 **`je_abolish_monarchy`**。原版本来就让已经共和的国家继续消除君主派影响，因此“总统共和＋该JE”不自动构成错误。
- 它**不是**“任何共和国家只要有君主主义IG就自动出现”的普适JE：定义没有自动显示/possible入口，主要由废君改制、反君主革命和特定事件显式添加。君主IG影响的是进度是否能增加，不是自动创建条件。
- 当前MOD没有直接添加/覆盖这个JE，也没有替换通用`transition_off_of_monarchy_effects`。HUS历史却会激活总统共和；原版总统共和`on_activate`无条件调用该通用effect，而effect末尾只查无JE、无`monarchy_stamped_out_var`，不核前政体或历史初始化。**最有力的源码原因是MOD开局共和国配置遇到了原版过宽的改制入口。**该初始化回调在用户存档中的实际发生时点仍未实测。
- 原版`00_global.txt`和MOD异名`ce_global.txt`均没有此JE或通用改制effect调用；不是这两个global重复直接添加造成的。不要为本问题停用全部global。
- 最小范围应只修HUS，并保留将来真实复辟后再废君的资格。用自有“正式运行后真实采用过君主制”标记＋HUS限定JE `REPLACE`；不要全局排除共和国，不要伪造奖励flag。

## JE本身的实际逻辑

完整定义：[GAME/common/journal_entries/00_abolish_monarchy.txt:2](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_abolish_monarchy.txt:2>)。

| 字段 | 本机代码 | 含义 |
| --- | --- | --- |
| `group`，第5行 | `je_group_internal_affairs` | 普通country-context内政JE，不是contextless全球JE。 |
| `on_monthly_pulse`，第7–34行 | 非君主、无进度≥0.75的革命、无强势且`law_stance(law_monarchy)>neutral`的IG时，`abolishing_monarchy_var += 1` | 截图条件对应这里。**75%恰好被挡；要求小于75%，不是允许≤75%。** |
| `complete`，第36–56行 | `is_goal_complete=yes`并再次检查同样政治条件 | 当前是共和国是完成的必要条件之一，不是应自动失效的理由。 |
| `immediate`，第58–62行 | 保存地主IG为`landowners_ig` | 不负责计数初始化；各显式调用者初始化为0。 |
| `on_complete`，第64–74行 | 设置`stamped_out_monarchy_var`；触发`1848.2`；中国军阀JE另有联动 | 有实际奖励/状态变更，错误清退不能走此路径。 |
| `invalid`，第84–93行 | 不正在制定且不拥有总统/议会/委员会共和及相应variant | HUS已有总统共和，因此现行invalid不会将其清掉。 |
| `current_value` / `goal_add_value`，第95–103行 | 读取国家计数；目标60；progressbar=yes | 月度不合条件时没有清零else，因此源码为累计60个合格月，不能擅自宣称连续五年断一次全归零。 |

`country_has_monarchy_law`的定义明确包含普通君主制和社会君主制：[00_ep2_victoria_scripted_triggers.txt:13–18](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt:13>)。中文标题、五年要求、完成事件“最后的君主派”及维持共和多年的描述位于[content_1_l_simp_chinese.yml:1206–1214](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/content_1_l_simp_chinese.yml:1206>)，与该解释相符。

## 所有已定位的原版添加入口

| 入口 | 原版条件和副作用 | 对HUS的判断 |
| --- | --- | --- |
| `on_law_enactment_started` | [00_code_on_actions:4440–4488](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:4440>)，root为国家；当前普通君主制，正在制定公司国/总统/议会/委员会共和；计数0再add JE | 真实从君主法开始改制的正常入口，应保留。 |
| `on_civil_war_won` | [同文件:5743–5769](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5743>)，有`anti_monarchist_revolution`且当前非普通君主制→计数0、add，随后移除革命标记 | 反君主革命正常入口；不应因国家当前共和而取消。 |
| `transition_off_of_monarchy_effects` | [00_victoria_ep2_scripted_effects:2647–2677](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2647>)，先处理王室地产/幕府法律/宪政主义IG；末尾无JE且无`monarchy_stamped_out_var`就设0并加入 | **末尾没有曾君主、旧法、game_date或has_game_started守卫，是HUS开局失配重点。** |
| `pedro.8` | [pedro_brazil_events.txt:649–653](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/brazil/pedro_brazil_events.txt:649>)，巴西废君结算显式初始化并add JE | 未见MOD把它接到HUS，保留巴西链。 |

通用effect的法律调用者：[00_governance_principles.txt:374–384](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt:374>)为总统共和；同文件521–531为议会共和，842为委员会共和，940为公司国。它并不先确认“从君主制转来”。

本轮搜索MOD的`common`、`events`：只有意识形态/政治运动读取`monarchy_stamped_out_var`，没有`je_abolish_monarchy`、`abolishing_monarchy_var`、`transition_off_of_monarchy_effects`的调用或覆盖。没有原JE、原政体法律、原通用effect的同路径替代。原版入口仍有效。

## HUS与global核对

- [MOD/common/history/countries/HUS.txt:69–85](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:69>)先`effect_starting_politics_liberal=yes`，再显式activate总统共和及其他法。原版自由预设[00_political_setup.txt:3–18](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_political_setup.txt:3>)第一项已经是总统共和。删第二次activate只能去冗余，不能消掉第一个入口；也不能断言两次activate会产生两份JE，因为通用effect已有has_journal_entry去重。
- [MOD国家定义:37–45](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:37>)明确华夏东洲共和国；[原稿风味:12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:12>)记1644起义与长期共和背景。作者要求HUS开局长期共和有项目依据，不应套原版新生共和国历史。
- HUS历史47–54行给士绅`ideology_scholar_paternalistic`；原版[00_ig_ideologies_flavored.txt:40–50](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies_flavored.txt:40>)使其强烈支持君主制。如果此IG在用户局中强势且实际合成态度支持君主制，原生JE会停滞。这解释“为什么可能长期不完成”，不证明“为什么自动加入”，也不授权本次改士绅意识形态。
- 原版global [00_global.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/global/00_global.txt:1>)与MOD [ce_global.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/global/ce_global.txt:1>)路径不同；当前元数据没有该目录的replace_path。两者完整搜索无本JE/计数/通用effect/完成flag。原版global第20–26行的`king_in_parliament_possible`仅给君主制＋专制国家，不是“所有共和国加入消灭君主制”。

## 哪些原版标记可以区分真实废君

| 符号 | 实际意义 | 能否作为HUS曾为君主国的通用证据 |
| --- | --- | --- |
| `anti_monarchist_revolution` | [on_revolution_start:5183–5192](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5183>)记录普通君主国面对非君主革命；胜利后消费 | **只证明特定革命路径的临时状态**。正常立法/脚本改制不一定有，旧档胜利后已删除。 |
| `abolishing_monarchy_var` | 所有添加入口给0，JE合格月加1 | 不能。过宽初始化入口也给它，拿它当真实转型证明形成循环论证。 |
| `stamped_out_monarchy_var` | JE完成标记，原版成就使用 | 不能证明“需要开始JE”；它是结果，强行设置会伪造完成状态。 |
| `monarchy_stamped_out_var` | `1848.2.a`选项标记；抑制以后JE加入并改变君主派人物/运动生成资格 | 不能当无副作用屏蔽开关。另一个完成选项不设置它，不能与上一个变量混同。 |
| `king_in_parliament_possible` | 开局普通君主制＋专制国家的特定内容资格 | 不是所有君主制/实际废君的账本，不能拿来全局分类。 |
| `has_been_monarchy`及近似名称 | 本机GAME/common、MOD/common、引擎trigger中未找到可用定义 | 不能虚构。没有现成的可靠通用“曾是君主国”谓词。 |
| `has_game_started` | 当前游戏是否开始；引擎triggers.log:10326–10330支持 | **可用于排除历史初始化，但不是政体历史记录。**原生法律已有实际用例，见下文。 |

完成事件[1848.txt:143–169](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/1848.txt:143>)会把地主家长主义换成共和家长主义，设置`monarchy_stamped_out_var`，并改变君主主义IG领袖。因此清除误入日志必须走失效，不能“让它完成一次”。

**本次新增的直接原版参考：**[GAME/common/laws/01_trade_policy.txt:339–349](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_trade_policy.txt:339>)在`on_activate`先检查`has_game_started=yes`，再联动activate封闭边境。证明本版本原生会对法律副作用使用这一运行期守卫。它优于简单`game_date>1836.1.1`，后者会误排开局当天玩家真实操作。

## 最小修复方案：HUS限定，保留真复辟后再废君

推荐采用**一个HUS自有资格标记、一个JE定点REPLACE，以及通用入口末尾的HUS守卫**。不对所有历史共和国作推断，也不扩改其他国家。

1. **记录真实君主状态。**新标记例`nesnd_hus_monarchy_observed_in_campaign`（这是拟新增MOD变量，不是原生API）。通过附加`on_law_activated`回调，在`has_game_started=yes`时进入该law的`owner`，只对HUS且实际`country_has_monarchy_law=yes`设置。原版[00_code_on_actions:5020–5033](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:5020>)明确root是law、owner才是国家；正常立法与脚本直接activate都走此回调，此时`currently_enacting_law`为空。
2. **旧档当下君主与正常立法补证。**迁移/自然检查仅在当前HUS实际君主时补标记；还可以在`on_law_enactment_started`的country root，现行君主法、正在制定共和法时即时补证，使从旧君主档继续改革也能保留资格。不能因为“存在JE”或“当前共和”就补成真实废君。
3. **入口局部守卫。**`REPLACE:transition_off_of_monarchy_effects`完整保留原前半王室地产/法律/IG处理，仅把末尾初始化计数＋add JE限定为“非HUS，或HUS已有真实君主标记”。不要把整个effect改空。这样HUS开局共和不会重新触发，后续真复辟再共和可以正常加入。
4. **活跃JE局部REPLACE。**保留完整原生定义，在`invalid`中以OR加入“HUS且无真实转型资格”。同一HUS资格守卫同时保护`on_monthly_pulse`、`complete`及`on_complete`，避免失效/完成检查先后尚未实测时仍误发1848.2。非HUS逻辑逐项保持。
5. **失效清理。**`on_invalid`只对这次被排除HUS清掉专属计数`abolishing_monarchy_var`，不设置两种完成flag，不改地主/领袖/法律/激进派。`current_value`在计数不存在时安全返回0，避免失效清理后UI/同帧再次求值。
6. **保留真正已发生转型的旧档边界。**若旧存档当前已共和、过去曾复辟又废君，且新标记尚未存在，原生现存变量不足以可靠反推；不能声称自动识别百分之百准确。当前用户明确HUS为开局长期共和国，可按该事实清理其错误实例。以后遇到有真实复辟证据的旧档，应按实际证据迁移资格，不以无标记证明它从未君主。

若主任务决定只交付一个JE REPLACE、暂不覆盖effect，仍能让错误HUS实例静默失效，但共和法每次重新激活仍可能尝试添加/重置计数；这一局部方案只治存量可见症状，入口并未关闭。直接永久`c:HUS`禁用虽更短，会错误屏蔽HUS未来真复辟后的玩法，不建议。

项目已有JE `REPLACE`先例：[zzzz_nesnd_native_error_bans.txt:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/zzzz_nesnd_native_error_bans.txt:2>)；scripted_effect先例：[ce_japan_gov_effects.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/ce_japan_gov_effects.txt:1>)。REPLACE是整个对象替换，不能仅写invalid后假设自动合并其他字段。on_action扩展按官方[_on_actions.md:115–128](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/_on_actions.md:115>)追加`on_actions={独立回调}`，不要重复定义原有effect块。

## 旧active JE退出与验收边界

官方[journal_entries.md:13–14、33–34](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:13>)说明显式`add_journal_entry`会忽略inactive/possible条件。第148–158行说明`invalid`使JE静默消失并执行on_invalid；第422–424行说明possible变false默认不会退活跃JE。因此只隐藏/possible=no不够，invalid才是对应旧实例清退入口。

建议外部闭包与以后一次定向游戏观察分别验证：

- HUS长期共和且JE进度0/59/60：失效，不增长、不完成、不弹1848.2、不设奖励flag；角色/IG不变。
- HUS开局法律激活：不误记录真实君主；`has_game_started`守卫作用于运行期。
- HUS真实普通/社会君主→共和，含脚本直接activate：记录资格并保留原生巩固过程；开局当天真实操作不被日期硬切排除。
- 非HUS君主正常立法、反君主革命、巴西专属事件：原逻辑和奖励不变。
- 已排队/已打开1848.2事件独立于JE；本截图只提供活跃JE证据，不全局禁事件或倒退已生效奖励。若确有该实例，再做限定HUS的取消处理。
- 旧档重载后invalid何时求值、同tick完成/失效顺序、人物/变量是否保持，需要真实存档观察；源码检查不认证这些已通过。

## 本次复核指纹

| 来源 | SHA-256 |
| --- | --- |
| GAME `common/journal_entries/00_abolish_monarchy.txt` | `1d8ac88eea45b13e035e5a1c15567f48a06de069fe386305b2e4bbc639ddd138` |
| GAME `common/scripted_effects/00_victoria_ep2_scripted_effects.txt` | `5eb6dca67e7647b4d09dbeb1c22e0ab2b68cee66c04a7476375c581f074191dc` |
| GAME `common/laws/00_governance_principles.txt` | `e676448ea64c17079677ddbf2cbfdbec0ffdefa465286f16c1e6107a14e7f4cf` |
| MOD `common/history/countries/HUS.txt` | `cb1485aa1ec06d0706806a9dbbdb6ab458ea78cbf796ac506a2482c6ecb33608` |

本报告未实施建议。法案on_activate的运行期守卫有当前原生实例；HUS新标记与迁移仍须由具体实现及闭包检查验证。
