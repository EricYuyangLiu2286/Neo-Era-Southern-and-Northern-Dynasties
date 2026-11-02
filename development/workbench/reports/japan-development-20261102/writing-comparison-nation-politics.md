# 日本国家发展与政治路线：逐键编辑对照

2026-11-02。对象：`WORK/exports/japan-development-20261102-a`。只写本JSON及报告，未改候选、未开游戏。

所有表中结论均为 **编辑通过，待装配**。已读实际JE、按钮、trigger/effect、值、bar、modifier和两事件；尚不代表最终覆盖层或引擎显示验收。原作者样本全文、基准提交匹配与SHA见[作者来源研究](writing-source-study.md)，没有用当前代理新增文案训练风格。

## 原文与本轮写法

|类别|原作者同类原句|本轮编辑选择|
|---|---|---|
|日本前史与独立|A1:150“丰臣幕府……依靠大明吴王的支持平定了战国之世”；332的九州、海关与东洋领事府关系|政治与国家建设以具体统治关系开篇；不把开国等同首次得到国际承认。|
|日本改革|A1:337“他梦想一个新的、强大的幕府政权已久，藩臣们也多尊重这一愿景。”；339–340“我们必须向明国学习。”“我们必须现代化！”|人物愿望和国家行动鲜明，不把三国固定为丰臣家同一条未来；选项表达态度。|
|政治按钮|A3:237“革命君主制和拿破仑的宪政……”；240“要么革命，要么帝制。”|三个按钮各有支持者和政治诉求；不以中性实现流程或相同风险总结替代。|
|政治事件|A2:79“将……利益，转移到……新贵手中。”|新政结算写实际官职、法令与权力分配，不无条件宣告三种互斥路线全部实现。|
|经济成果|A2:69从法案写到迁入城市的农民和日常生活|独立结算把军队、工商业、港口与自主权联系起来，不写“完成三个子日志”。|
|修正/读数|A2:74“投资狂热”；A3:249原生当前值/总值|修正名简明，数值交原生效果；bar沿用原生JournalEntry/ScriptedProgressBar.Self上下文。|

A1=`ce_usm_events_l_simp_chinese.yml`；A2=`ce_cne_events_l_simp_chinese.yml`；A3=`ce_french_empire_journals_l_simp_chinese.yml`，均为原始备份并逐字匹配f18b6c4。N1/N2/N5为来源研究及产业对照报告已核当前原版英文JE、锁国、进度条示例。D为本轮日本计划，不冒充既有剧情。

## 实际契约与返工

- “幕府的前途／再造幕府”原是丰臣专用草稿；当前政治总JE和court路线可给JAP/JTK/JIM，court仅需君主制。总标题改“国政之争”，君主路线改“君主与新政”。丰臣前史保留为历史，不假称当前统治者仍是丰臣。
- 军方路线入口没有战胜条件，删除“战场上的胜利使军官们……”既成事实。改成军官对指挥、征募和国家权力的要求。
- 选择路线扣实际费用、12个月不能改换、改换会归零。费用由原生效果展示；后两项在按钮说明中保留，因为它们会直接改变玩家决定。
- 资助按钮实际付费获得6个月立法推进和地主-1；不写成“检查改革条件”或即时加进度。根任务计划补“目标未达才可使用”的守卫，文字不依赖该守卫而假称按钮直接推进总进度。
- 放弃/失去君主资格导致停止、清临时成本、归零并24个月不能重开。放弃按钮必须说明失去进度，不写“保留已积累进度”。实际法律建筑没有逆转。
- 国家发展在再次附属时仍保留，reason采用独立建设目标而不无条件声称当前主权完整；subject/independent状态按实际条件显示。
- 两完成事件没有强加未来战争、三国合并或夺回九州。政治事件共享的具体事实是任官制度改变，三路线均有实际法律依据。
- 既有统一reason/status/goal仍写九地区；本批附三键的必要改写。保留原题“天下之归/One Realm”及原生progress读数，避免无端重译；九州与四国改为独立后续争端。

## 源码指纹

C-JE-P/N指政治/国家JE；C-EFF-P/N指对应effect；C-VAL-P/N指值；C-MOD-P/N指modifier；C-UNITY指既有统一JE及已读core谓词。

|文件|SHA-256|
|---|---|
|[common/journal_entries/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_jp_politics.txt>)|`d19197834ff84eeeb493c0c77bbc4ab240c91a342f15eb6f0824059b08959755`|
|[common/journal_entries/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_jp_nation.txt>)|`08e4f4118799ed5c430828badbaed328069b0e874a0e1082921a432f0436075e`|
|[common/scripted_buttons/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_buttons/nesnd_jp_politics.txt>)|`30b240562394aa308631ca7e791cd302784bba279e8568eb2a0f9917b0cfe2b0`|
|[common/scripted_buttons/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_buttons/nesnd_jp_nation.txt>)|`383558300571a147c628e226e372cbe0218b255b6908481e651e3d14039dc0ad`|
|[common/scripted_effects/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_effects/nesnd_jp_politics.txt>)|`09da821e82b6e7e08ac8886bf8a6bee18dd2e3b11c178363f42e53dbb1b61c39`|
|[common/scripted_effects/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_effects/nesnd_jp_nation.txt>)|`68225c5521611ec8d435708afcc73f3cfdd9fac23095336ed33dab63ff7b798d`|
|[common/scripted_triggers/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_politics.txt>)|`a4ef0e35cd1acec845526f0ba60f30417dd61c2b6b5ce9c8cebe6ee3d2052167`|
|[common/scripted_triggers/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_nation.txt>)|`4dcb99e309bf5754c358cdb9538a2fb9ac8430a4fa199b0a1871eb9896a394a1`|
|[common/script_values/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/script_values/nesnd_jp_politics.txt>)|`3a1ac8206715f0c5a64c948fc87dbc8eb348e1cca405c355d415ff657eda15a4`|
|[common/script_values/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/script_values/nesnd_jp_nation.txt>)|`c691872eb85e1c18c0953bcef33eb466e6243690c8011035aacf4f6858e30fc9`|
|[common/scripted_progress_bars/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_progress_bars/nesnd_jp_politics.txt>)|`9d8045500fd7dd6b29ff6ba4da2ca6f2e122b0f4b85bb7c044f440e69def8726`|
|[common/scripted_progress_bars/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_progress_bars/nesnd_jp_nation.txt>)|`ac4c15d39c6a89b2cabb063c651de3e552bc9fad063a0d86e957a81c47fd734f`|
|[common/static_modifiers/nesnd_jp_politics.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/static_modifiers/nesnd_jp_politics.txt>)|`59f3ddfb9bcb3bf227ce99d4a2f4452a94cdb7e0eca7a47032862713cb765681`|
|[common/static_modifiers/nesnd_jp_nation.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/static_modifiers/nesnd_jp_nation.txt>)|`ecf1d6710c28337519153b0c9f33bd056af520fbce06c499bcccb2b1bd54338e`|
|[events/nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/events/nesnd_jp_development.txt>)|`a424934268f2b7886f29551b6673494a957e47dd3dc071db000d30d2ef41b43a`|
|[common/journal_entries/nesnd_japan.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_japan.txt>)|`ae16684e9ae84784d2ceac5ce280971dd57a3359810705ec3a0319fe2239f36f`|
|[common/scripted_triggers/nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_development.txt>)|`6ce0673f4f8b07d63fb2558838119df8b2e743299b32e435ed06665f03aaba9b`|
|[common/script_values/nesnd_jp_development.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/script_values/nesnd_jp_development.txt>)|`d57d70128f63b14983730ffd51462b12c96c2a669b8951b91fb2c31d5d742fa3`|

## 全键中英对照

每项均检查用词、断句、造句、冗余、玩家视角与真实脚本。英文表达重新组织句子，保留同一事实、动态引用与必要数值，不沿用中文回退。

|键/类别|同类原文依据|本轮中文|本轮英文|决定|
|---|---|---|---|---|
|`nesnd_jp_politics`<br>日志标题|A1:331、336；A1:150、302、337；A3:237、245|国政之争|The Question of Government|编辑通过。总JE适用于三国和不同现行政体，故以历史幕府开篇而不称当前统治者必为丰臣；新政治力量为本轮改制提案，不冒称原稿既定事件。|
|`nesnd_jp_politics_reason`<br>日志正文|A1:150、302、337；A3:237、245|丰臣氏平定日本以后，朝廷的名分、诸藩的兵马和大阪的商业共同支撑着幕府的统治。新的财源与知识正在改变旧有的权力关系，商人、军官和读书人都希望参与国家的决断。围绕官员任用、军队和法令的争论，已经关系到政府将由谁来掌握。|After the Toyotomi unified Japan, the authority of the court, the armies of the domains and the commerce of Osaka sustained the shogunate. New wealth and learning are changing these relationships. Merchants, officers and scholars seek a greater say in government, challenging the old arrangements for appointing officials, commanding troops and making laws.|编辑通过。总JE适用于三国和不同现行政体，故以历史幕府开篇而不称当前统治者必为丰臣；新政治力量为本轮改制提案，不冒称原稿既定事件。|
|`nesnd_jp_court_reform`<br>日志标题|A1:331、336；A1:337–340；A3:237|君主与新政|Reform under the Crown|编辑通过。删除“再造丰臣幕府”固定主语；monarchy、任命官僚、选举、学校和铁路均有实际目标。末句为路线追求，不承诺奖励直接创造效忠人口。|
|`nesnd_jp_court_reform_reason`<br>日志正文|A1:337–340；A3:237|君主的名义仍能召集旧臣，也能为新学和商业开路。拥护改制的人们希望由熟悉实务的官员治理地方，让议政的代表参与国事，再以学校与铁路联通远近。王朝将在这些改变中重新取得人们的信任。|The crown can still rally old loyalties and give learning and commerce room to grow. Reformers seek capable officials in the provinces and representatives who can take part in public affairs. Schools and railways would connect distant communities, allowing the dynasty to renew its hold on public confidence.|编辑通过。删除“再造丰臣幕府”固定主语；monarchy、任命官僚、选举、学校和铁路均有实际目标。末句为路线追求，不承诺奖励直接创造效忠人口。|
|`nesnd_jp_military_reform`<br>日志标题|A1:331、336；A2:20、79；N1:688|军府的新秩序|The Military Ascendant|编辑通过。选路线只要求军队影响力，无战胜条件，删原稿候选“战场上的胜利使……”；不假称已迫使军队入阁、不写二十世纪军国政体。|
|`nesnd_jp_military_reform_reason`<br>日志正文|A2:20、79；N1:688|军官们把军队视为国家最可靠的支柱。他们要求将征募、训练与军需交给统一的指挥，使地方的兵力能够供国家调度。兵工厂和工具厂将为这支军队提供装备，集中的政令则让军府有机会把自己的主张推行到各地。|The officers regard the army as the country’s most dependable institution. They seek common control over recruitment, training and supplies, bringing provincial forces under national direction. Arsenals and tool workshops would equip this army, while a concentrated government could carry the officers’ programme into the provinces.|编辑通过。选路线只要求军队影响力，无战胜条件，删原稿候选“战场上的胜利使……”；不假称已迫使军队入阁、不写二十世纪军国政体。|
|`nesnd_jp_representative_reform`<br>日志标题|A1:331、336；A3:240、245；A2:69|国人议政|A Voice in Government|编辑通过。对应选举、集会/言论、官僚、学校和识字；不强制共和国、不默认工会存在、不预告殖民退出。|
|`nesnd_jp_representative_reform_reason`<br>日志正文|A3:240、245；A2:69|读书人讨论国政，商人关心税赋，地方居民也希望有人替自己说话。代议派要把这些议论带进议会，以选举决定代表，以公开辩论约束执政者。教育的普及将使更多国人能够读懂法令、参与公共事务。|Scholars debate public affairs, merchants watch taxation, and local communities seek someone to speak for them. Advocates of representative government would bring these concerns into an elected assembly and subject those in power to open debate. Wider education can allow more people to understand the laws and take part in public life.|编辑通过。对应选举、集会/言论、官僚、学校和识字；不强制共和国、不默认工会存在、不预告殖民退出。|
|`nesnd_jp_nation`<br>日志标题|A1:331、336；A1:332–334；N1:673、686、690|自主之国|A Nation of Our Own|编辑通过。JE再次附属时仍保留，所以不无条件写“现在一切由本国决定”。不要求先统一、不假称首次获得国际承认。|
|`nesnd_jp_nation_reason`<br>日志正文|A1:332–334；N1:673、686、690|日本的诸政权长久在大陆王朝的庇护与干预下生存。自行决定国事，需要能够保卫疆土的军队、供养国家的工商业，也需要通向海外的港口与商路。我们要把这些力量掌握在自己手中，使独立有长久的根基。|Japan’s governments have long lived with protection and intervention from the mainland. To govern our own affairs, we need forces that can defend our territory, industry that can sustain the state, and ports connecting us with overseas markets. Bringing these strengths into our own hands will give independence lasting foundations.|编辑通过。JE再次附属时仍保留，所以不无条件写“现在一切由本国决定”。不要求先统一、不假称首次获得国际承认。|
|`nesnd_jp_new_army`<br>日志标题|A1:331、336；A1:337–340；N1:688|整顿国军|An Army for the Nation|编辑通过。兼容职业军队、大规模征兵、国民民兵三类完成法；不写所有非正规单位必须归零，比例条件留原生显示。|
|`nesnd_jp_new_army_reason`<br>日志正文|A1:337–340；N1:688|旧日军队依靠世袭武士与地方关系维持，征募和训练也随各家而异。国家需要有组织的兵员、受过训练的军官和能够听从统一调度的部队。无论以常备军还是国民军承担防务，都应使军事服务于共同的国事。|Hereditary warriors and local loyalties sustained the old armies, with recruitment and training varying between domains. The country needs organized manpower, trained officers and forces that answer to a common command. Whether defence rests on a standing army or a national militia, military service must support the affairs of the nation.|编辑通过。兼容职业军队、大规模征兵、国民民兵三类完成法；不写所有非正规单位必须归零，比例条件留原生显示。|
|`nesnd_jp_open_diplomacy`<br>日志标题|A1:331、336；A1:332–334；N1:690|与诸国往来|Dealing with the World|编辑通过。实际要求独立、开国、国际贸易科技、港口与12个月独立；派遣/谈判为政治目的，不声称脚本已经签成条约。|
|`nesnd_jp_open_diplomacy_reason`<br>日志正文|A1:332–334；N1:690|过去的朝贡和海禁把外交、通商交织在宗主的安排之中。我们需要以本国的名义派遣商船、开放港口，同其他国家商谈彼此的利益。持续的自主将使这些往来有一个可以信赖的政府作为依托。|Tributary ties and maritime restrictions once placed diplomacy and trade within an overlord’s arrangements. We need to open our ports, send out merchant ships and negotiate with other countries in our own name. Lasting sovereignty will give these exchanges a government they can rely upon.|编辑通过。实际要求独立、开国、国际贸易科技、港口与12个月独立；派遣/谈判为政治目的，不声称脚本已经签成条约。|
|`nesnd_jp_open_ports`<br>日志标题|A1:331、336；A1:332–334；N2:3|重开海门|Opening the Ports|编辑通过。泛述锁国制度，不声称当前仍有九州口岸，也不声称所有人已完全失去九州。两实际开港法交按钮选择。|
|`nesnd_jp_open_ports_reason`<br>日志正文|A1:332–334；N2:3|日本的海外买卖长久受制于少数口岸和严密的禁令。商人希望取得远方的原料，也希望把本国的出产运往更广阔的市场。政府必须决定如何开放这些海路，以及关税将在新的贸易中保护谁的利益。|Japan’s overseas trade has long been confined by a few designated ports and strict prohibitions. Merchants seek distant raw materials and wider markets for the country’s produce. The government must decide how to open these sea routes and whose interests its tariffs will serve.|编辑通过。泛述锁国制度，不声称当前仍有九州口岸，也不声称所有人已完全失去九州。两实际开港法交按钮选择。|
|`nesnd_jp_islands`<br>日志标题|A1:331、336；A1:256、272；D二、三|九州与四国|Kyushu and Shikoku|编辑通过。入口独立且七本州统一；只说未完全解决，不把两岛都写成完整失陷。和平接受边界仅放弃本国宣称，不许诺对方让步。|
|`nesnd_jp_islands_reason`<br>日志正文|A1:256、272；D二、三|本州已经归于一统，九州与四国的归属仍未完全解决。两岛的港口和海路关系着日本南部的贸易与防务。政府可以设法收回尚在他人掌握中的土地，也可以接受现有边界，放下这场领土争端。|Honshu has been reunited, but the question of Kyushu and Shikoku remains unsettled. Their ports and sea routes matter to trade and defence in southern Japan. The government may seek the remaining territories or accept the existing borders and relinquish its claims.|编辑通过。入口独立且七本州统一；只说未完全解决，不把两岛都写成完整失陷。和平接受边界仅放弃本国宣称，不许诺对方让步。|
|`nesnd_jp_choose_court`<br>按钮标题|A1:339–340；A3:237|以君主统合新政|Reform through the Crown|编辑通过。politics按钮选择court；两周收入数值由add_treasury自动显示，不再抄费用。12个月改线锁和归零是必要决策信息。|
|`nesnd_jp_choose_court_desc`<br>按钮说明|A1:339–340；A3:237|王朝的号召力可以把旧臣与改制者召到一处。保留君主，任用新官员，让议政与实业为国家带来新的力量。<br><br>选定后 #v 12#! 个月内不能改换方针。改换方针将清空已有改革进度。|The dynasty can bring loyal retainers and reformers together. Preserve the crown, appoint capable officials, and give representative deliberation and enterprise a place in the state.<br><br>The policy cannot be changed for #v 12#! months. Changing policy resets reform progress.|编辑通过。politics按钮选择court；两周收入数值由add_treasury自动显示，不再抄费用。12个月改线锁和归零是必要决策信息。|
|`nesnd_jp_choose_military`<br>按钮标题|A2:20、79|支持军府整顿|Back the Officers|编辑通过。不以胜利作未有入口条件；实为军方主导改制意图，非立即生成军事政府。必要改线信息同上。|
|`nesnd_jp_choose_military_desc`<br>按钮说明|A2:20、79|军队需要统一的指挥，国家也需要能够贯彻到底的政令。支持军官们整顿兵制与军需，把地方的人力和财力用于共同的防务。<br><br>选定后 #v 12#! 个月内不能改换方针。改换方针将清空已有改革进度。|The army needs a common command, and the state needs orders that can be carried through. Back the officers in reorganizing recruitment and supply, drawing provincial manpower and revenues into a common defence.<br><br>The policy cannot be changed for #v 12#! months. Changing policy resets reform progress.|编辑通过。不以胜利作未有入口条件；实为军方主导改制意图，非立即生成军事政府。必要改线信息同上。|
|`nesnd_jp_choose_representative`<br>按钮标题|A3:240、245|扩张代议政治|Expand Representation|编辑通过。以代议派立场写行动，未承诺立即普选/共和国。必要改线信息同上。|
|`nesnd_jp_choose_representative_desc`<br>按钮说明|A3:240、245|国事关乎所有纳税、服役和谋生的人。让更多代表参与议政，使官员必须面对公开的讨论，也使国民能够以选票影响政府。<br><br>选定后 #v 12#! 个月内不能改换方针。改换方针将清空已有改革进度。|Public affairs concern everyone who pays taxes, serves or earns a living. Bring more representatives into government, subject officials to public debate, and let voters influence the conduct of the state.<br><br>The policy cannot be changed for #v 12#! months. Changing policy resets reform progress.|编辑通过。以代议派立场写行动，未承诺立即普选/共和国。必要改线信息同上。|
|`nesnd_jp_advance_reform`<br>按钮标题|A3:237；A2:81|资助新政|Fund the Reformers|编辑通过。三个inspect按钮复用；实际只付费加6个月立法速度及地主不满，不写立即完成检查或直接增长改革条。|
|`nesnd_jp_advance_reform_desc`<br>按钮说明|A3:237；A2:81|拨款支持主张改制的人士，让他们的议论更快成为国家的法令。|Fund the advocates of reform so that their proposals can more quickly become law.|编辑通过。三个inspect按钮复用；实际只付费加6个月立法速度及地主不满，不写立即完成检查或直接增长改革条。|
|`nesnd_jp_abandon_reform`<br>按钮标题|A2:64–66|搁置新政|Shelve the Reforms|编辑通过。停止清理临时修正、route和进度并设24个月setback；必须说明进度丢失，不能写暂停后完整续进。|
|`nesnd_jp_abandon_reform_desc`<br>按钮说明|A2:64–66|撤回当前改革方针，结束政府为新政进行的动员。改革进度归零，#v 24#! 个月内不能重新提出改革；已有法律和建设保留。|Withdraw the current programme and end the government’s reform campaign. Reform progress is lost, and reforms cannot be proposed again for #v 24#! months. Existing laws and buildings remain.|编辑通过。停止清理临时修正、route和进度并设24个月setback；必须说明进度丢失，不能写暂停后完整续进。|
|`nesnd_jp_mercantile_ports`<br>按钮标题|A1:334；N2:3|重商开港|Open Ports under Mercantilism|编辑通过。实际激活重商主义；不假称自由贸易、免关税或建立特定贸易路线。|
|`nesnd_jp_mercantile_ports_desc`<br>按钮说明|A1:334；N2:3|准许商人经营海外买卖，以关税维护国家的收入和本国商业的地位。|Allow merchants to trade overseas, using tariffs to support state revenue and domestic commerce.|编辑通过。实际激活重商主义；不假称自由贸易、免关税或建立特定贸易路线。|
|`nesnd_jp_protected_ports`<br>按钮标题|A2:34、69；N2:3|以关税护业|Protect Industry with Tariffs|编辑通过。实际激活保护主义；科技、港口、现金与两年开港修正由原生显示，不重复数字。|
|`nesnd_jp_protected_ports_desc`<br>按钮说明|A2:34、69；N2:3|开放海路，让工场取得所需的原料，再以关税扶持本国生产者在新市场中的地位。|Open the sea routes to obtain the materials our factories need, while using tariffs to support domestic producers in the wider market.|编辑通过。实际激活保护主义；科技、港口、现金与两年开港修正由原生显示，不重复数字。|
|`nesnd_jp_islands_settlement`<br>按钮标题|A1:258、274|接受现有边界|Accept the Existing Borders|编辑通过。只是移除两州region宣称及关闭本议题，不写签约、返还或全面外交和解。|
|`nesnd_jp_islands_settlement_desc`<br>按钮说明|A1:258、274|放弃对九州与四国的领土要求，承认目前的疆界。|Relinquish our territorial claims to Kyushu and Shikoku and accept the current borders.|编辑通过。只是移除两州region宣称及关闭本议题，不写签约、返还或全面外交和解。|
|`nesnd_jp_court_policy`<br>条件式状态|A1:332；C-JE-P/C-JE-N|以君主名义推行宪政改革。|Constitutional reform proceeds under the crown.|编辑通过。选court，当前立场不宣告目标完成。|
|`nesnd_jp_military_policy`<br>条件式状态|A1:332；C-JE-P/C-JE-N|集中政令，整顿军制与军需。|Centralize authority and reorganize the army and its supplies.|编辑通过。选military；不必军队已经直接执政。|
|`nesnd_jp_representative_policy`<br>条件式状态|A1:332；C-JE-P/C-JE-N|扩大代议，保障公开议政。|Expand representation and protect public debate.|编辑通过。选representative；不宣称普选已经实行。|
|`nesnd_jp_unsettled_policy`<br>条件式状态|A1:332；C-JE-P/C-JE-N|政府尚未决定改革的方向。|The government has yet to choose a course for reform.|编辑通过。无路线时的准确短状态。|
|`nesnd_jp_nation_subject`<br>条件式状态|A1:332；C-JE-P/C-JE-N|国家重归藩属，对外事务受宗主约束。|The country is a subject again, with foreign affairs constrained by its overlord.|编辑通过。只有曾开启独立JE后再次附属时适用；不声称法律/产业全丢失。|
|`nesnd_jp_nation_independent`<br>条件式状态|A1:332；C-JE-P/C-JE-N|国家可以自主处理内外事务。|The country governs its own domestic and foreign affairs.|编辑通过。只据当前非subject说明主权，不预告战争胜利或建成所有目标。|
|`nesnd_jp_reform_settled`<br>必要条件提示|A3:249；C-JE-P/C-EFF-P|改革进度已满，且所选方针的制度目标已连续满足 #v 12#! 个月|Reform progress is full, and the chosen policy’s institutional goals have been met for #v 12#! consecutive months|编辑通过。合并实际progress>=100和good_months>=12；不将持续时间误称仅等待12个月即自动成功。|
|`nesnd_jp_nation_complete`<br>必要条件提示|A1:332；C-JE-N/C-EFF-N|产业、军制与外交建设均已完成，且国家已连续保持独立 #v 12#! 个月|Industrial, military and diplomatic development is complete, and the country has remained independent for #v 12#! consecutive months|编辑通过。score>=3与独立12个月；和平由独立原生条件显示，不再抄。|
|`nesnd_jp_political_bar_name`<br>进度条名|A3:248–249|新政推行|Reform Progress|编辑通过。国家改革的推进，而非某人物支持率。|
|`nesnd_jp_nation_bar_name`<br>进度条名|A3:248–249|国家建设|Nation Building|编辑通过。三类已完成成果的计数，不伪造月度推进率。|
|`nesnd_jp_political_bar_desc`<br>进度条读数|A3:249；N5:467|#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100|#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100|编辑通过。原生JournalEntry/ScriptedProgressBar.Self上下文，读数只出现一次。|
|`nesnd_jp_nation_bar_desc`<br>进度条读数|A3:249；N5:467|#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0]#!/3|#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0]#!/3|编辑通过。原生JournalEntry/ScriptedProgressBar.Self上下文，读数只出现一次。|
|`nesnd_jp_political_administration_desc`<br>原生进度来源|A3:249；C-VAL-P|行政与新学|Administration and Learning|编辑通过。开始改革且行政非负、识字达标才增益。 数值由原生bar显示。|
|`nesnd_jp_political_laws_desc`<br>原生进度来源|A3:249；C-VAL-P|制度确立|Institutional Reform|编辑通过。只有路线全部实际制度目标达成才增益，标题不误指仅一条法律。 数值由原生bar显示。|
|`nesnd_jp_political_opposition_desc`<br>原生进度来源|A3:249；C-VAL-P|战争与激进情绪|War and Radicalism|编辑通过。实际只由战争和高激进人口减分，避免泛称所有反对派。 数值由原生bar显示。|
|`nesnd_jp_court_debate`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|君主制改革|Reform of the Monarchy|编辑通过。立法速度、地主-2、知识分子+1，名字是政治运动非已完成制度。|
|`nesnd_jp_court_settlement`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|君主立宪|A Constitutional Settlement|编辑通过。任命官僚与选举等已达目标；奖励为行政/集团力量，不写额外法律激活。|
|`nesnd_jp_military_debate`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|军方推动改制|The Officers’ Reform Campaign|编辑通过。立法速度与军队/地主/知识分子态度；不称已全面军管。|
|`nesnd_jp_military_settlement`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|军制振兴|Military Renewal|编辑通过。军事商品成本与攻防，名字不擅自宣布战争胜利。|
|`nesnd_jp_representative_debate`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|代议改革运动|The Movement for Representation|编辑通过。集团支持与立法速度，属推进过程。|
|`nesnd_jp_representative_settlement`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|代议政治确立|Representative Government Established|编辑通过。合法性、教育和知识分子吸引力；不承诺取消君主。|
|`nesnd_jp_reform_effort`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|改革派的奔走|The Reformers’ Campaign|编辑通过。额外+15%立法速度、地主-1，未写成检查/验证修正。|
|`nesnd_jp_independent_state`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|独立国家的声望|The Standing of an Independent State|编辑通过。行政、威望与影响力；不称有新的承认等级。|
|`nesnd_jp_home_waters`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|九州与四国归统|Kyushu and Shikoku Reunited|编辑通过。军事成本与威望；具体两岛条件，避免假称所有现代日本领土归一。|
|`nesnd_jp_opening_dispute`<br>修正名称|A2:73–74；C-MOD-P/C-MOD-N|开港之议|The Debate over Opening|编辑通过。地主-2工业家+1；不声称已经发生叛乱。|
|`nesnd_jp_development.1.t`<br>完成事件标题|A1:331|独立的根基|The Foundations of Independence|编辑通过。国家建设完成的标题，未将国际承认再发一次。|
|`nesnd_jp_development.1.d`<br>完成事件正文|A1:332、334；A2:69|军队经过整顿，工商业有了新的根基，海外往来也逐渐摆脱旧日朝贡的束缚。这些变化使独立成为人们生活中可以感受到的事实：军人听从本国的号令，商船以本国的名义出海，政府能够自行处理国事。曾经必须送往宗主朝廷的决定，如今可以在国内作出。|The army has been reorganized, industry has gained firmer foundations, and overseas commerce has moved beyond the old tributary restrictions. Independence now has a place in daily life: soldiers answer to their own government, merchant ships sail in their country’s name, and public affairs are decided at home. Decisions once referred to an overlord can now be made here.|编辑通过。只反映已达军制/工业/外交成果；未声称完成全国统一、收回两岛或征服朝鲜。|
|`nesnd_jp_development.1.a`<br>事件选项|A1:334、339–340|国事当由国人自决。|We shall decide our own affairs.|编辑通过。纯确认选项，表态而非承诺额外效果。|
|`nesnd_jp_development.2.t`<br>完成事件标题|A2:68|新政立定|Reform Takes Root|编辑通过。进度满且目标稳定12个月后的既成结果。|
|`nesnd_jp_development.2.d`<br>完成事件正文|A2:69、79；A3:245|新的任官办法已经推行，国家的法令也改变了权力在各阶层间的分配。旧日凭借门第把持地方的人，如今必须面对由政府确定的职位和权限；参与改制的官员、军人和商人，则在新的秩序中寻找自己的位置。这场改革已经进入日常统治，成为处理国事的准则。|New arrangements for appointing officials are in place, and the laws have changed how power is distributed. Families accustomed to holding local office by birth must now contend with positions and powers defined by the state. Officials, soldiers and merchants who took part in reform are finding their places within these arrangements, which now guide the conduct of public affairs.|编辑通过。三路线均废世袭官僚，任命或选举官员；公共正文不声称三路线同时实现议会、军府和君主立宪，不捏造人物引语。|
|`nesnd_jp_development.2.a`<br>事件选项|A2:71、81|使新法行之久远。|Let these reforms endure.|编辑通过。确认已完成改革，不附虚假的后续选择或额外奖励。|
|`nesnd_japan_reunification_reason`<br>既有日志正文修订|A1:150、302；旧候选replace:25|海峡两岸的盟约曾替丰臣打开平定诸侯的道路，也让唐土朝廷得以介入日本的继承、封地和征战。城下町的税赋汇往各家府库，军队与商人各认其主。[ROOT.GetCountry.GetName]要重建统一的政府，就须使本州归于一统，并取得自主决定内外政务的地位。|Alliances across the strait once helped the Toyotomi conquer their rivals and allowed the mainland court to intervene in Japan’s successions, domains and wars. Taxes, armies and commerce now follow competing authorities. [ROOT.GetCountry.GetName] must reunite Honshu and secure the freedom to govern its own affairs.|编辑通过。最小修订既有正文，将三岛共同门槛改本州；现有候选原文不是作者样本。|
|`nesnd_japan_reunification_status`<br>既有状态修订|旧候选replace:26；C-UNITY|统一本州，确立自主的政府。|Unite Honshu under an independent government.|编辑通过。返工“七地区仍待统一”：国家可能已全有本州但尚附属，改为稳定的短目标；不复制完整地区清单。|
|`nesnd_japan_reunification_goal`<br>既有目标修订|旧候选replace:27；C-UNITY|独立并完整拥有本州七地区：关东、京都、关西、中国、东海、东北与北陆信越。|Be independent and fully own Honshu’s seven regions: Kanto, Kyoto, Kansai, Chugoku, Tokai, Tohoku and Hokushinetsu.|编辑通过。owns_entire_state_region是拥有不是战时控制；准确列七地区，不含两岛。|

## 本批边界

共 **68键**。其中新模块65键，加既有统一日志3键修订。条目不新增事件风味引文或不存在的按钮。实际支付为`nesnd_jp_negotiation_cost`，当前定义按两周`net_fixed_income`且限制5000–100000；自动费用不在reason重复。最终路线与国家奖励为一次、120个月；文字不承诺永久收益。两开港按钮实际分别激活重商主义/保护主义，原生科技、港口与现金条件保留；没有额外自由贸易或免费开港叙述。

本报告核定的是上述读入文件。根任务后续改触发、费用、法律或效果时，应据最终SHA重核受影响键，不能拿本稿替代最终覆盖审查。未运行引擎，未验收画面。
