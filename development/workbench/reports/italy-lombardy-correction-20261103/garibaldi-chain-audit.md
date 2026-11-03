# 加里波第原版链条与伦巴第适配审计

2026-11-03；研究/计划，未改游戏、未改意大利主计划、未启动游戏，未全量解析存档。版本沿本轮 `catalog.py status`：**1.13.11 / Steam build 24799966，CURRENT**。当前完整 DLC 环境为设计前提，不另做缺 DLC 旁路。用户所说“加里波利”按 **Giuseppe Garibaldi／加里波第**核查；不混入马志尼、波兰内容或现实人物百科。

## 结论与证据边界

**建议保留加里波第本人和稳定模板ID，优先适配历史起点、迁移条件及独立的统一事件。** 原版加里波第是可被招揽、授予军职、流放和跨国迁移的历史角色；`italian_unification` 的直接改政、兼并和撒丁优待并不要求他存在。删人物或把所有 `votp_garibaldi` 视频换掉，均不能解决后者。[G1][G3][G4]

`author_explicit`：法国主导的伦巴第共和国已经存在；佩佩是亲法意大利民族主义者。此确认不等于作者已经指定加里波第也亲法、反法或支持佩佩。加里波第保留自身激进共和主义、群众动员与军事志愿者的候选作用；与佩佩合作或冲突要有具体利益与事件原因，不能把他写成佩佩复制品，也不能把民族主义自动等同反法。伦巴第合作整合、友好独立和条件性决裂应分开。身份基线另见 [source-check.md][M0]。

下文 `current_script` 为文件所写；适配方案为 `gameplay_proposal`。重复生成、死亡后再出现、旧档里当前在哪里等没有本轮运行证据，不能写成已复现问题。

## 一、当前有效来源与覆盖

- **人物定义**：GAME `common/character_templates/garibaldi_template.txt:1—20`；`historical=yes`，出生 `1807.7.4`，北意大利文化、天主教、工会IG、`is_agitator=yes`、`ideology_radical`，家乡 `STATE_PROVENCE`，DNA `dna_giuseppe_garibaldi`，勇敢与基础进攻规划者。`on_created` 设置全局 `garibaldi_is_alive_global_var`。[G1]
- **生成并非国家人物历史**：GAME 人物历史中未检到 Garibaldi 调用；现有模板的创建调用在 `garibaldi_events.1:174—183`。MOD 人物历史亦未创建加里波第；LOM 现有角色调用是佩佩与马志尼，两者不能替代此链。[G3][M0]
- **MOD没有替换此链**：核对 GAME 同相对路径，MOD 无加里波第模板、专属事件、`italian_unification.txt`、原版两份 on_actions、人物互动、原版意大利JE、按钮、形成数据库、加里波第修正、希腊 `bavarocracy.txt`、相关衣帽文件；全 MOD 有效 `.txt/.yml` 检索也未见这些加里波第ID的另名定义。MOD 的 `ce_code_on_actions.txt:30—34` 是追加自己的月脉冲，另有多份自有挂钩；没有查见排除加里波第原版链的指令。[M2]
- **开局调用存在两份源码**：GAME `common/history/global/00_global.txt:970—975` 与 MOD `common/history/global/ce_global.txt:710—715` 都在 `c:PNI ?=` 内以 `days=6` 排 `garibaldi_events.1`。MOD 当前只有 `ce_global.txt`，没有同路径 `00_global.txt` 覆盖；异名历史文件不能视为替换。两份排程是明确源码事实；引擎是否去重、届时是否重复执行 immediate、是否造成角色或名望重复，均待核。[G2][M1]
- **原版南美环境**：`common/history/diplomatic_plays/00_south_american_wars.txt:1—18` 建 BRZ 对 PNI 的 `ragamuffin_war`，`war=yes`；MOD 无同路径覆盖。PNI 在 MOD 州历史仍有归属（`00_states.txt:2540`）。本轮不把南美战史写成作者已确认的加里波第新生平。[G17]

## 二、人物生命周期：调用者 → 条件 → 执行 → 收尾

| 环节与ID | 当前源码行为 | 伦巴第适配判断 |
| --- | --- | --- |
| 月度入口 | `on_monthly_pulse_country` 在 `00_code_on_actions.txt:1556—1559` 延迟4天调用 `garibaldi_monthly_events`；`00_on_actions_monthly.txt:21—28` 给 `chance_to_happen=30`，`.1/.2/.3/.4` 权重30/30/2/1。不是每月四件事都发生。[G5][G6] | 保留入口。需改个别事件时不要复制整个国家月脉冲。 |
| `.1` 来投：一般限制 | `garibaldi_events.1:25—43` 要VOTP、年份≤1862、所在国没有 `rejected_garibaldi`、没有带 `garibaldi_var` 的国内角色；还要全局存活标志不存在，或流亡池已有带该变量的人。[G3] | 有角色身份保护，仍应让每条新入口共用同一身份，不另造 `nesnd_garibaldi` 副本。1862是来投事件上限，不是强制死亡日期。 |
| `.1` 来投：战争选择 | 第44—161行三类：①有特定选举/无政府法律的国家抵御专制/寡头/一党制敌国，或对应民主倾向革命/分离；②意大利文化传承国对非意大利且持意大利本土州者开战、意大利分离战，或被非意大利国家攻击；③PNI在≤1839年与BRZ交战。②不要求共和制，也没有“必须反法”条件。[G3] | LOM可在符合条件的真实战争中获得他；法国保护关系本身不触发反法战争。若新增合作援军入口，要读取实际交战方、盟友与宗主，而非把法国预定为敌人。 |
| `.1` 创建/移国 | 第165—198行：全球 `any_character` 不存在带 `garibaldi_var` 者才创建模板并写角色变量、冷却与 `garibaldi_scope`；否则从流亡池选择原角色，`transfer_character=root`，保留身份。第200—210行每次进入 immediate 增加全局 `garibaldi_fame_var`，不是按胜仗计分。[G3][D1][D2] | 重用原角色。避免重复排程、预览或拒绝导致额外名望累加；后续若改奖励，不能误把原版名望当战功统计。 |
| `.1` 接受/拒绝 | 第249—257行在保存角色不存在/死亡时取消。接受第261—424行加 `general` 角色，按全局名望给1—5档修正、概率升级进攻规划特质，发布到达通知。拒绝第426—484行设置本国无期限 `rejected_garibaldi`，部分IG扣支持，角色流亡并清理职责。[G3][G10] | 保留国家取舍，不强迫佩佩接纳任何军事动员者。拒绝状态应由真实行动产生，不能因“亲法”开局自动写入。 |
| `.2` 告别/转战 | 第619—691行：①非ITA、非意大利传承国家已和平且人物冷却结束；或②全球出现另一意大利传承国家与非意大利国家的合格战争、对方未拒绝他。②不限当前雇主参战；引擎文档明确 `any_diplomatic_play` 为全球迭代。第705—816行存人物、旧雇主、意大利与外国参战方scope；第819—945行移除志愿军人物/兵营修正、流亡清职责，再给新意大利国家触发 `.1`；第947—959行发布离境通知。[G3][D2] | 意大利雇主不会仅因和平被①赶走，但可能被②重新选择。法国主导体系下，不能假定原版迁移会保留现有协作；若设计将法援/军事承诺纳入路线，应在触发、选目标、执行三处共同核约束。 |
| 普通邀请与授职 | `invite_exile:997—1088` 要流亡池、空鼓动者槽、接纳度、宗教与开放边境等条件、`can_agitate`；执行移到邀请国，增加鼓动者职业期限60—90个月；对 `garibaldi_var` 写冷却。`grant_command_to_agitator:218—238` 再按成年男性、有陆军HQ等条件加将军身份；邀请本身不加将军。[G7] | 这是 `.1` 之外的合法迁入路径，必须覆盖。可保留通用机制；不能认为每个带变量的人都已是将军。 |
| `.3` 意大利志愿军 | 第983—1004行要人物变量、当地意大利传承人口、所在国作为战争发起/目标、未有 `italian_legion_var`。第1008行立即写一次性标志；第1009—1014行选角色却额外要求 `general`。第1079—1084行取消只检查国内是否仍有变量角色。选项第1087—1111行给人物作战或兵营吞吐修正。[G3][G10] | **明确源码前置不一致**：普通邀请迁入而未授职是候选到达路径；`garibaldi_scope`可能无法保存，但取消条件仍通过。是否实际可达与UI/执行后果未核。最小处理应统一将军资格并在即时和选项重验scope；不是删事件或免费授军职。 |
| `.4` 农民动员 | 第1137—1156行要变量角色、整合州农民、真实战争、非边缘乡村民众；允许其言论会提高乡村民众力量并增加农民激进派，制止则80%流亡并写拒绝变量（第1199—1227行）。[G3][G10] | 可保留战争动员与国内土地/公民利益冲突。文案不能仅凭支持法国便把现政府称为外国压迫者。 |
| 通用退出与死亡 | `exile_character_with_role_cleanup:720—728` 流亡、解除军队编组、清所有角色后仅留agitator；`clean_up_exile_character_roles:731—738` 做后两项。通用流放互动有法律/职位/忙碌等限制；`retire_commander:1240—1258` 常规路径先移除将领/海军将领，再按可剔除条件退休。`on_character_death:2702—2707` 以模板识别并移除存活全局标志。[G8][G7][G5] | 保留生命周期。原版并无本链永久死亡墓碑变量；死亡/退休后能否在≤1862年再次进入创建分支不能仅据此断言，需一次最小验证。旧档不清存活标志、不重置出生日期、不复活。 |

`.1/.2` 的取消条件主要检查角色存在/生死，并未完整重验当初战事、所有权和承诺。`.2`触发层的拒绝过滤亦未在后续全部随机目标筛选中重复。新增路线必须修完整的候选筛选与延迟执行闭包，不能只加一条最外层法国条件。[G3]

## 三、与人物无关的意大利统一链

| 入口与实际效果 | 需要适配的原因；最小方向 |
| --- | --- |
| `je_risorgimento`：意大利区域/主文化条件；民族主义科技、非帝国/霸权；进入时`.10`，每周`.4`，每月按180:20抽无事/`.2`；形成ITA且有月度进度标记完成，失去所有意大利本土失败。两按钮绑定于此。[G9:18—130] | 统一底座可保留，经济发展不必等民族主义科技。不要把启用JE写成伦巴第第一次成为共和国或第一次有民族认同。 |
| `italian_unification.10:824—1001`：赞成统一基础40，SAR+50、SIC−35；反对基础15，SAR−50、SIC+50，另有政体/IG权重。`jingoist_leader`在支持统一的IG反馈中获益，并非反法标志。[G4] | 重新评估SAR/SIC固定优待/抑制，让实际政权、联盟、国力和法国关系参与。亲法与赞成统一可同时成立；不能以LOM永久赞成替换SAR永久领跑。 |
| `.2:75—169`：唯一ITA候选、邻接意大利小国、友好、目标AI、赞成统一、无拒绝冷却；目标须独立/本国属国/同关税同盟；接受给10外交事件值并`annex_with_incorporation`，拒绝加关系与目标冷却。[G4] | 可留和平整合结构；它不引用加里波第，也不会自动取得法国同意。LOM→PAR/MOD/TUS和FRA→LOM两层关系仍须单独协调，避免另造一套平行免费吞并。 |
| `.4:220—378`：首都激进人口≥10%、意大利民族运动革命、另有独立意大利文化国等条件；立即改支持统一。择独立意大利领袖；少于2州转`.5`，≥2州第一次流放现统治者、改议会共和+普查选举（世袭官僚才改任命官僚）、3个月选举；以后再发可转`.5`。`.5:409—455`默认AI吞并，玩家可`play_as`接收国，另一项改傀儡；`.6`为兄弟共和国外交回应。[G4] | **已经是总统共和国的LOM也可满足这一分支，佩佩被流放并非“从君主制第一次建共和”。** 这是条件性革命后果，不能保证免除，也不能不分现政体照叙事宣告推翻异族旧制。最小改当前制度/实际革命诉求的分支与文案，保留真实失败、改政或失国的可能。 |
| 意大利民族运动自身 `movement_italian_national:931—1005`：非ITA等国家、意大利文化热情门槛，支持若干领袖意识形态；形成ITA后解散并可转多数文化运动。[G18] | 这是运动及制度争议，不要求加里波第或佩佩在场。统一后内容应随运动和法律转换，不固定某人不死。 |
| `on_secession_start:5547—5570`→`.7`→`.8`：源注释称奥地利/圣马可，实际只要求RSM不存在、意大利主文化分离国、母国非意大利主文化、意大利有复兴JE；不限AUS。`.7:546—576`随机选意大利区域分离国、改总统共和/寡头、改TAG为RSM并加升级度；`.8`给各JE国家选择支持、损害对母国关系、撤相关同盟/防御条约，亦有移除protectorate逻辑。[G5][G4] | **法国也可能成为该一般谓词的母国**；并不证明本轮已有法属叛乱。LOM已有伦巴第/威尼西亚，不能通用套“奥属伦巴第—威尼西亚五日”。改触发对象与保存真实分离国scope，按法国/奥地利及现有关系分别议价；避免随机选错同时发生的分离国。 |
| `je_risorgimento_austrian_radicals_button:450—598` 与国内鼓动按钮`:600—714` | 两者属国时隐藏，当前LOM开局不能直接按它们。前者名字含austrian，实际可选持意大利本土的非意大利文化国；possible检查南欧及`relations<=20`，执行`random_country`未重复这两个限制。若独立后的LOM仍亲法而有另一敌对国满足possible，目标可能另选法国——是源码筛选不一致风险，未运行复现。最小调整应让显示/资格/执行选同一合格目标。国内按钮同样需核外交关系筛选闭包。[G11] |
| ITA形成与收尾 | `country_formation/00_major_formables.txt:54—101`提供70%文化州、最多3候选、排名/科技等资格；不要求加里波第。真正`on_country_formed:4055—4059`触发`.1`，给予意大利声明及威望/统治者IG奖励；JE的`on_complete:110—113`包在`show_as_tooltip`里，不能仅因看到两个事件引用就认定双重执行。`give_claims_on_italy`仅加声明，不是分地。[G12][G5][G4][G13] |

## 四、人物身份、画面和文本依赖

- **身份识别**：事件通常用角色 `garibaldi_var`；死亡清理与希腊支线用 `has_template=garibaldi_character_template`。同时北意大利通用姓氏池含 `Garibaldi`（`common/cultures/00_cultures.txt:2345`），所以同名不等于第二个历史人物。核唯一性要查模板、标记、所属国/流亡池和存活状态，不能按显示姓名删人。[G1][G3][G5][G14]
- **还有合法用途**：`bavarocracy_events.2.i` 在希腊国家内已有该模板角色时可选（`events/balkans_events/bavarocracy.txt:515—543`），清退相关原王室/南德意志人物并将其设为统治者；这不是意大利统一链，也不创建第二个加里波第。本轮不因意大利适配连带删除该支线。[G15]
- **视频不是角色调用**：`italian_unification.1`和`.10`只引用 `votp_garibaldi`；别的革命/流放事件甚至葡萄牙殖民事件也用该视频。`gfx/media_aliases/media_aliases.txt:424—429`解析到 `gfx/event_pictures/votp_garibaldi.bk2`，实际资源在 `dlc/dlc004_voice_of_the_people/gfx/event_pictures/`。调整伦巴第显示时可只换相关事件的media alias引用，不删除全局资源。[G4][G16]
- **头像/红衫军**：模板用 `common/dna_data/00_giuseppe_garibaldi.txt`；`gfx/portraits/portrait_modifiers/01_clothes.txt:7261—7289`、`01_headgear.txt:4285—4315`会根据国内人物标记/模板及ITA候选条件影响军人群像服装。重命名模板或删变量会波及这些可保留效果；本轮未改素材，也未验证实际渲染。[G1][G19]
- **需要适配的现行文案**：`content_1_l_simp_chinese.yml:1089`直接采用拿破仑战争结束后外国占领叙事；`:1108`将结果称为新建共和国；`:1113—1121`写伦巴第—威尼西亚、四角防线/威尼斯；`:1158`为建国引文，注释归加里波第。它们不能无条件代表当前LOM。人物 `.1—4`文案在 `agitators_2_l_simp_chinese.yml:436—458`；通知在 `agitators_1_l_simp_chinese.yml:456—461`，还依赖保存的人物与新旧国家scope。[L1][L2][L3]

## 五、最小替换/重置计划（尚未实施）

1. **保持身份，先收口初始化。** 保留 `garibaldi_character_template`、DNA与人物标记；围绕两份PNI六天排程核实际加载与执行，再消除本MOD的重复调度。若新世界线决定改变早期去向，只改明确的调度/资格，不给LOM免费复制一个人物，不全局重置原版历史文件。
2. **先修安全闭包，再写新政治分支。** `.3`统一将军资格、保存scope及选项重验；`.1/.2`统一候选战争、接纳国和拒绝标记过滤，验证战事结束/人物死亡/被流放后延迟事件的退出。保留普通邀请和军职授予入口，不假定所有来投都经过`.1`。
3. **统一链独立适配。** 按现有伦巴第共和国、亲法整合优先的起点修`.10`AI权重；`.4—6`区分既有共和国与君主国的真实革命诉求；`.7—8`使用真实分离国与宗主，处理法国体系内援助、边界与条约；两按钮使用同一目标资格。保留`.2`及原生ITA形成框架，检查法国与附属邦条款，避免双轨吞并。
4. **仅改确有旧史前提的文本和图像入口。** 改JE起点、奥属伦巴第式通用描述及新建共和国表述；加里波第自身可保留名字、跨国志愿者身份与利益冲突。若要写正式玩家文本，另按 `nesnd-player-writing`采样原文，不在这份报告提前发布候选文案。
5. **旧档保留人的历史。** 迁入、死亡、退休、担任他国统治者和拒绝记录分别识别；不重开开局礼物，不删除同姓随机人物，不重置统一/反统一立场或所有外交条约。只有确证重复模板实例才拟定定向修复；目前没有此证据。

拟改动边界应是对应事件ID、必要的历史调度行、JE/按钮/立场适配及本地化；采用哪个数据库窄覆盖方法要在实施前核其真实支持，不能假定 `REPLACE:` 对所有文件生效，也不要整包覆盖原版 on_actions。非本次相关的通用招募、希腊、南美系统保留。

## 六、未证点与必要验证

- **本轮未核角色在1866终档的存在、死活或所属国**，也不从终档反推其全生涯。本报告以源码与引擎文档确认作用域。
- 两份PNI排程的运行去重、`trigger_event`延迟触发时对事件trigger/cooldown的处理、死亡/退休之后的`any_character`枚举行为，均不能由现有文档独立决定。引擎文档只说明触发事件/延迟语法与全局枚举，未承诺这些细节。[D1][D2]
- `.3`已证前置不一致；是否能经普通邀请→战争→未授军职达到、是否产生空scope错误，仍需定向验证。`.2`延迟间换雇主/战事消失、`.7`并发分离、按钮误选亲法国也列为未证可达性。
- 如实施：先做定义唯一性、引用与目标/角色/日期/关系闭包检查；再对未证语义安排一次集中小场景：PNI开局调度；一次正常来投与拒绝；一次手动邀请但无军职的`.3`；人物死亡/流亡与延迟退出；亲法LOM的合作战争和独立后目标筛选；既有共和LOM发生民族运动革命；ITA形成后交接与存读档。复用已有通过证据，不为文案纠正重开游戏，不用STATIC_PASS冒充ENGINE_PASS。

## 来源索引

`[G编号:行号]`表示该文件中的具体行号，表中区间为阅读范围。以下都是本机当前源文件或已导出的1.13.11引擎文档。

[M0]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/italy-lombardy-correction-20261103/source-check.md>
[M1]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/global/ce_global.txt:710>
[M2]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/ce_code_on_actions.txt:30>
[G1]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/garibaldi_template.txt:1>
[G2]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/global/00_global.txt:970>
[G3]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/garibaldi_events.txt:4>
[G4]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt:1>
[G5]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:1556>
[G6]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_on_actions_monthly.txt:21>
[G7]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_interactions/00_character_interactions.txt:997>
[G8]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_scripted_effects.txt:720>
[G9]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_italian_unification.txt:1>
[G10]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/agitators_2_modifiers.txt:361>
[G11]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_scripted_buttons.txt:450>
[G12]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_formation/00_major_formables.txt:54>
[G13]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_unification_effects.txt:1>
[G14]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/cultures/00_cultures.txt:2345>
[G15]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/bavarocracy.txt:515>
[G16]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gfx/media_aliases/media_aliases.txt:424>
[G17]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/diplomatic_plays/00_south_american_wars.txt:1>
[G18]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/03_pan_national_movements.txt:931>
[G19]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gfx/portraits/portrait_modifiers/01_clothes.txt:7261>
[L1]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/content_1_l_simp_chinese.yml:1079>
[L2]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/agitators_2_l_simp_chinese.yml:436>
[L3]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/simp_chinese/agitators_1_l_simp_chinese.yml:456>
[D1]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37318>
[D2]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:100>

| 关键文件 | SHA256 |
| --- | --- |
| G1 模板 | `12d8cbda7353b8f96e253465f079aa8bf8ad200e658382e2e0f551873119215d` |
| G3 人物事件 | `f421a5f191a0cde1d57a2d214701618f1f969a062196bd6c2897e5f38bfa1216` |
| G4 统一事件 | `3564046713083efe19a97fe04a3d83a6e875a627794652ce726c727c602b296e` |
| G5 引擎挂钩 | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |
| G2 原版全局历史 | `03c33f822172aee0f469c84286064d536e60af7df4b92526a74bd258505caf46` |
| M1 MOD全局历史 | `7ad25a08d41ba3c540d115f666f300734cac2993024a1ef2b3947afd92021040` |

技能复核：沿用作者确认、人物身份与机制分层；本任务只新增该研究备忘，无技能或游戏修改，无ENGINE_PASS声明。
