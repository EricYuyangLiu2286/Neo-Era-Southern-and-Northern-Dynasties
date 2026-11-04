# 明吴战争结束、行在迁逃与残存国结算：源码核查

2026-11-03；GAME 1.13.11 / build 24799966。只读，未修改脚本、未启动游戏。`SOURCE_RESEARCH / ENGINE_NOT_RUN`。本报告补充[此前外交接口报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/journal-war-feedback-20261103/south-postwar-native.md>)，重点核TAG、主战国消失和一次结算范围；没有本局新存档，因此不能把主战国亡国时引擎如何收束战事当作本轮已复现事实。

## 可直接用于修复的结论

1. **当前“大明行在”不是MNG或ZHI。**它是HNA或SIH持有`nesnd_ming_court`后的动态国名。截图具体是哪一国仍须实际TAG/存档；源码只能确定现有两个承载者。
2. SIH在没有已选行在接收国时，是内战主战目标的首选。蜀亡后若引擎结束这场战争，现有“无带标记博弈＋没有反对国与USM交战”条件会触发`.9`，立即设置全局`nesnd_south_settled`。这会将**原战争结束**扩大成**所有政治后继结束**。
3. 未找到原生“切换/继承既有战争主战国”的脚本effect，不得编造。可靠修复方向是保存实际参战者、确认该国确已与USM停战，再按国家一次结算；新战争是新实例和新锁。
4. `.5`目前先随机kill/exile人物、再吞并。行在皇帝必须在随机处理前保存同一人物并转移/流亡，不能以生成一个同名皇帝替代。
5. 本土残存流程应限定**本轮实际参战、仍存活、仍拥明的本土国家**。仅`usm_opposition_country`过宽，会包含JAP与海外成员；JAP/JTK/JIM有独立恢复链，不接本土求附CNE三选一。

## 真实TAG与硬编码遗漏

| 位置 | 当前行为 | 修复闭包要求 |
| --- | --- | --- |
| [dynamic_country_names/zz_nesnd_ming_court.txt:1、43](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/zz_nesnd_ming_court.txt:1>) | 仅`REPLACE:HNA`与`REPLACE:SIH`；第31/84行用`nesnd_ming_court_country`，条件为行在flag、非interregnum | 扩展到GNG或其他新承载国时，动态名也必须覆盖对应TAG，否则flag/人物已迁走而地图仍显示旧国名。不能只改host候选。 |
| [本地化:19](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/zzzzzzz_nesnd_ming_court_l_simp_chinese.yml:19>) | `nesnd_ming_court_country="大明行在"` | 这是显示名，不是country key。 |
| [flag_definitions:10915](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/flag_definitions/00_flag_definitions.txt:10915>)、country_creation第2721行 | `MNG`注释为Minas Gerais | 巴西米纳斯吉拉斯，与明朝无关。不得为了猜TAG去吞并/迁人到MNG。 |
| [ce_countries.txt:88](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:88>) | `REPLACE:ZHI`为Zhili，首都直隶 | ZHI不是目前的明朝行在承载者。`events/warlord_china_events.txt:120`另有ZHI引用，是另一条链。 |
| [nesnd_ming_host_candidate:1–7](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_ming_court.txt:1>) | alive、非玩家、有州、自控首都，TAG只HNA/SIH；允许stance0/1，排共和/吴 | 这是初始迁廷候选；新“陷城后随机仍拥明国”应单独核实际拥明，不无声继承“非玩家”和“中立也可”的旧限制。 |
| [nesnd_ming_find_rebel_host:22–32](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_court.txt:22>) | 有已选receiver先用，否则HNA、再SIH；保存国家对象变量 | 不是随机；新迁逃不能复用后声称“任一存活拥明国”。 |
| [nesnd_ming_royal_refuge_host:1–8](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_court_followup.txt:1>) | TAG仍硬限HNA/SIH，独立、stance1、反对国、非共和、自控首都 | 新通用host需统一any/random候选谓词，排origin/USM/已经降吴者。 |
| [nesnd_ming_refresh_royal_identity:20–31](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_generation.txt:20>) | 人物/流亡/void都会扫描；国家保存原人物引用只直接查USM/HNA/SIH | 若新增GNG等承载者，人物身份扫描仍可工作，但国家引用读写/清理、行在君主引用也要泛化，不能遗留在旧HNA/SIH上。 |

## SIH绑定与“剧情提前结束”的调用链

[nesnd_open_southern_war:181–285](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:181>)先看`nesnd_ming_receiver`，再按SIH→HNA→GNG→PHI→DEI→YN1→JAP选`nesnd_opposition_leader`，给它`usm_opposition_country_leader_var`，以它作为`create_diplomatic_play.target_country`。第312–325行把其他独立反对国加入target backers。这解释了SIH经常是这场战争的主战目标。

该选择当前只看`has_variable=usm_opposition_country`等既有状态；新增/重开局入口须核alive与对象存在，不可仅凭历史TAG或旧变量。`usm_civilwar_occured`全局阻止原函数再次开战，不能清掉它来重跑整套第一次开战与政治邀请。

[主战争JE:345–360](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:345>)现在的镇压完成是“没有存活且非己属的反对国”，**并未直接写SIH灭国便胜利**；但fail检查无标记外交博弈且没有反对国与USM交战，然后调用`.9`。拥明/革命JE第408–425、468–485同形。

[usm_civilwar.9:1305–1318](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1305>)只要没有总胜利/败退事务阻塞且本国未seen，就设置`usm_civilwar_status_quo`和全局`nesnd_south_settled`。后者令旧反对国JE invalid；它不创造和约/停战。

[当前战后资格:37–58](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_settlement.txt:37>)要求USM是叛军改tag后的总胜利者（`usm_rebel_winner_of_the_civil_war`＋`nesnd_rebel_settlement_seen`），所以原吴-USM仍在的停战常不能进入`.11`。这是清楚的后继缺口。

**本次没有证实的部分：**SIH被吞并那一刻引擎是否一定终止整场战争、是否某些条件下有自然主战继承。当前原生脚本与effects文档未提供可用于承诺“把主战国改为HNA”的接口。不要以`add_target_backers`、`join_war`冒充更换主战；它们仅添加参与者。

## 原版结束回调与实际参战记录

- [00_code_on_actions.txt:6988–7015](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:6988>)：`on_war_end` root是**外交博弈**，`scope:actor`是发起国，`scope:target`是目标国；原版target使用`?=`可空。不能在该root直接调用country trigger。
- [同文件:4173–4184](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:4173>)：`on_peace_agreement_signed_war_leader`和`...war_participant`是country root。可作为排队检查入口，但通知回调本身不应直接无守卫改变所有国家。
- 引擎[effects.log:9648–9652](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:9648>)提供war scope的`every_war_participant`；**`every_participant`是diplomatic_pact scope的两方，不是战争参与者迭代器**。
- 当前日本恢复已在[nesnd_japan_recovery on_actions:34–46](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_japan_recovery.txt:34>)挂`on_war_end`，进入明确`c:USM`执行，不依赖已消亡目标。新南明处理应追加独立回调而不是覆盖现有日本恢复。

建议在战事仍有效时把“实际与USM交战”的事实及本轮序号记到国家：身份至少满足本土成员＋拥明立场，且`has_war_with=c:USM`为真。单纯受邀、口头拥明、拥有`usm_opposition_country`不足以成为战后待结算者。结束后依赖持久国家记录，而不是已经消失的SIH/战争对象。

## 残存国范围与序列

现有分类在[nesnd_south_politics.txt:90–123](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_politics.txt:90>)：本土HNA/SIH/GNG；保护海外PHI/DEI/YN1；日本JAP/JTK/JIM。它比广义政治成员或反对国flag更适合本土残存流程。

如果将来新增真正大陆行在TAG，单靠这个固定三TAG集合又会漏掉它；应明确“本土成员或本轮登记的合法行在承载国”，但仍排除日本独立链与海外殖民地，不能将任何持行在flag的任意国自动当大陆受降对象。

建议状态序列（这是MOD状态设计，不是伪造原生接口）：

`本轮已实际参战 → 与USM不再交战且无相关外交博弈/败退事务 → 本国一次选择pending → 抵抗 / 请求CNE / 降吴 → 结果confirmed`。

- 保存“本轮序号、参与序号、已派发序号、已解决序号/请求身份”；同轮多次和平/投降/周度回调只排一次。
- `pending`在派发时设定；请求CNE期间保持。拒绝/失效/超时发**明确后继**并清请求，不能每月重新弹初始三选一。
- 选择抵抗是该次选择已完成，不等于立即无视休战开战；后继JE/按钮等待新战资格。新战争另有创建与结束锁，保留上一轮已答标记，不能通过全局清空`usm_civilwar_occured`或初始邀请锁回放老剧情。
- 存活、无`has_war_with=USM`、无相关play和无待执行吞并应分别检查；初始六个月`nesnd_war_opening_grace`只属第一轮开战缓冲，不应让后续和平永远等待。
- `nesnd_south_settled`不能继续同时表示“第一次战争已停”与“所有拥明势力全灭”。最终胜利取全体仍存有效抵抗者集合；停战只进入后继阶段。

## 陷城吞并与同一皇帝保全

[nesnd_south_capital_defeat:2–22](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_war_collapse.txt:2>)对非JAP反对国，已确认败退或与USM交战且敌占>80%/USM或其属国控制首都即触发。用户现在指定“行在首都遭USM占领”，行在专门分支应严格使用该事实，不以蜀亡、友军控制或任意敌占替代。

[usm_civilwar.5:927–1094](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:927>)：pending→after重验→成年角色随机流亡/杀死→USM `annex_as_civil_war=root`。**当前没有皇帝先迁出的特别分支。**[nesnd_ming_general_refuge:104–146](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_royal_refuge.txt:104>)又要求root=USM、tag_WUU、未settled等，只适合最初易代时的出逃，不能原样复用到HNA/SIH行在败退。

新的陷城事务应先保存当前在位皇帝或合法`nesnd_ming_court_monarch`，验证alive/owner/宗室身份，再random_country选择同一候选谓词下仍存活拥明者。先transfer并确认owner，再令新国持行在状态；无候选才流亡；最后吞并旧行在。旧随机人物处分排除该同一皇帝；若人物已移出，不再解引用旧国家owner去重新找人。

**existing lookup必须保留：**

- [nesnd_ming_prepare_accession:2–19](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_court.txt:2>)保存`nesnd_ming_claimant_ref`与`nesnd_ming_heir_ref`；后继还有`nesnd_ming_court_monarch`、refuge claimant/heir对象。
- [nesnd_ming_find_ning_dynast:59–125](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_generation.txt:59>)按原帝、原储、宁系等查本国/全体人物、流亡池、void；不是一看到国家灭亡就create_character。
- [nesnd_transfer_restoration_claimant:95–123](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_restoration.txt:95>)对void释放、流亡人物转移并清旧host引用，保持同一人物；[recruitable谓词:1–9](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_ming_generation.txt:1>)不夺走外国在位统治者/继承人。

陷城保全应以**当前实际皇帝**为先；只有引用确实失效才使用既有查找链。不能用“原始皇帝模板”覆盖仍活着的后继君主，不能因人物已在exile/void就判死亡，更不能通过新建同名人物绕开缺scope。

## 续战与CNE接受的原版参考

原生[虾夷:ep2_ezo_republic.txt:79–100](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ep2_ezo_republic.txt:79>)先独立、移出旧博弈backers，再另建`create_diplomatic_play`（target_country、escalation60、dp_annex_war）并给对方明确目标。它证明可以创建新的后继博弈，**不是继承主战身份**。普通`dp_annex_war`另有目标国等级/关系/宗属限制，不能保证对任意剩余国家可用；本MOD已有专属dp/war_goal可审查复用，不能不验返回状态就标“已再战”。

休战检查`has_truce_with`与结束休战`end_truce`有原生实例：[哈萨克:00_ep1_kazakh_events.txt:26–41](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/soi_events/00_ep1_kazakh_events.txt:26>)。默认建议等自然休战结束；若明确设计撕约，才对指定双方end_truce。未找到`skipcountdown`、`set_liberty_desire`、`make_subject`；当前接口详情见此前报告，不重复发明。

归附的实际接口是宗主scope `create_diplomatic_pact={country=申请者 type=...}`。原生[巴尔干请求保护:277–291](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/balkan_wars_events.txt:277>)由TUR创建对root的protectorate；[西藏远征:2000–2019](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/tibetan_expedition.txt:2000>)按等级/承认状态选择tributary或vassal。`tributary`是实际属国类型，定义[24_subject_tributary.txt:1–43](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/24_subject_tributary.txt:1>)包含20%收入转移、subject_type_tributary与解除后60月休战；不能把“庇护”一词当作无宗属副作用的剧情flag。

CNE接受前重新核双方alive、申请者独立、CNE可作宗主、双方和平、无已承诺外交博弈、关系与本次pending身份仍满足。真正create pact后确认`is_subject_of=CNE`才标成功；不能在发请求时加CNE为backer，也不能强制让它加入已结束或尚未结束的吴战。拒绝→申请国明确继续抵抗或另行降吴；失效/超时采用同一明确保底，不留pending。

## AI分歧：沿用动机，不偷搬旧战前概率

[既有南朝计划:61](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261101-southern-allegiances-envoys-plan.md:61>)：SIH重半独立经济利益、维护明廷、渐进改革；HNA支持陈东阳、迅速立宪、反郑氏背叛与旧士绅/奴役；[80–82行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261101-southern-allegiances-envoys-plan.md:80>)旧战前方案SIH求QE1、HNA求CNE且拒绝回拥明。旧地图方案给GNG较强拥明基础，当前胜利后[GNG复辟分支:198](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_restoration.txt:198>)有淮系宗室逻辑。

因此本轮战后可让HNA相对偏向求CNE及立宪式继续抵抗、SIH偏保留自主与明统、GNG偏延续拥明/宗室；战争损害、实力、关系再调整权重。**用户本次明确要求投北朝由CNE接受/拒绝，优先于旧SIH求QE1或旧“接受后共同开战”的计划。**旧90/5/5、20/80是战前设计，不能直接说它们就是本轮战后概率，更不能随机覆盖玩家选择。

## 定向验证要求

1. SIH灭亡但HNA/GNG仍存且本轮真实参战：政治后继继续；未参战中立国、JAP、海外国家不被错误纳入。
2. 行在首都陷落：同一皇帝先迁合法随机host，无host进入流亡池，旧行在确实吞并；多回调只执行一次。
3. 仍有其他吴战/外交博弈/吞并pending时，不提前全局终结；主战对象已不存在时回调不读空target。
4. 每个登记国本轮只派发一次选择；CNE接受/拒绝/迟答时改属/灭国/开战/过期都有后继。
5. 新战争采用新实例锁并在结束时独立清理；旧邀请、原始人物身份、已有已答结算不被全局重置。
6. 此次只认源码闭包。自然主战亡国处理、皇帝迁逃—吞并实际顺序、旧档回调与附属关系创建结果仍需定向引擎验证，不能由静态研究替代。

引用自检：33条本地文件链接均存在，带行号的引用均在文件范围内；只认证来源可定位。
