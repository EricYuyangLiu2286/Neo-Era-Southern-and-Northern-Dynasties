# Batch A2：美洲原住民复国、迁徙与汗国实施计划

状态：READY_FOR_TEST / 编辑冻结。日期：2026-11-04。实施者：`/root/sol_a2_implementation`，实际模型配置 gpt-6.1-sol / medium；依据 root 显式分派，复用既有探索与获批架构。32 owned / 27 changed，详见 batch-a2-implementation.md 与 batch-a2-owned-files-sha256.json；尚无STATIC_PASS或游戏验收。

本计划的原探索阶段只读当前候选、本机1.13.11 / build24799966、作者PPET与既有合同。后续已按root GO完成A2候选代码与中英文，并冻结所有权副本；未运行行为测试、Tiger、MCP或游戏。A1的STATIC_PASS继续只适用于原冻结闭包；A2有限接口的局部diff已归档，独立回归仍待分派。

目录约定：W=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`；C=`W/exports/canon-route-execution-20261104-a`；R=`W/reports/canon-route-execution-20261104`；G=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`。主 MOD、G、作者材料均只读；本计划获 GO 后只在 C 实施。来源编号及 SHA 见文末和同目录 `batch-a2-source-manifest.json`。

## 1. 本批交付边界与必须修正的骨架

交付两套相连而不混同的内容：墨西哥／秘鲁的原住民旧王朝政治复兴；HUS 登记分支引出的满蒙迁徙或大平原汗国。拥有全部自身中英文、人物、条件、结果、失效和旧窗口处理，不把缺文案或未接回调留给 root。

已读的当前草稿不是验证结果。其中必须修正：

1. NAH/TWT 使用同一总统共和准备函数；而且调用 A1 的 `nesnd_native_primary_cultures_only` 已因其 NKH／native_successor 限定而实际不适用于两国。
2. 复国只切一州、固定 24 营、没有具体统治者和军政代表；NPU 存在即使 SPU 永远没有入口。
3. `enemy_occupation >= 0.8` 将任何第三国占领算成复国军功；对手消失也被直接当胜利；一场没有建立成功的 DP 可能被普通旗标伪装为完成。
4. 战败后才找亡国来源，或 HUS 缺席时永远 pending；没有人物的真正角色清理／流亡。
5. NKH 建国选择和半数迁徙缺完整提交边界；固定 40 营及大量工业可能重复／超规模；两战收尾只看没有在交战。
6. 原住民登记后的满蒙外迁保留逐源 pop 的70/30随机目的地；修正必须两个目的国同时存在才会结束的问题，补单目的地与双缺席终态。
7. Turtle Island 三个原版按钮效果没有拦截；仅隐藏 JE 不能拦住旧窗口。

不重新执行 `prepare_canon_data.py`，不改 `common/history/pops`、历史州归属、province 或任何历史 owner-state 人口总量。下列人口数字只是当前候选源文件的只读加总，不是旧档人口或实机观测。相关来源：[P01–P04、C01–C05]。

## 2. 作者历史与政体选择

直接提取作者原 PPTX 的 slide 18、19、22 到 `batch-a2-ppet-primary.json`。PPTX SHA 为 `b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`，不拿文本缓存 SHA 冒充原件。[P01]

|政体|作者原文事实|本批选择的可玩解释|
|---|---|---|
|NAH 阿兹特克|slide18 ¶8：1524 年夸乌特莫克逃往吴地，被北明封宋王；¶18：1712 年宋王后裔复蒙特祖玛王朝、向吴称臣；¶23：1811–1815 HUS 支持墨西哥第一共和国|现存 MEX 共和国与流散王族／本土共同体竞争合法性。复统是蒙特祖玛王族主持的原住民王国，保留议会与地方共同体，不能把已死的夸乌特莫克重新生成。吴国保护作为延续史与外交态度；不凭历史朝贡自动给当代 CNE 属国、兵力或同意吞并的权限。|
|TWT 印加|slide19 ¶12：1534 曼科印卡在吴军帮助下逐皮萨罗；¶17：1653 库亚喀印卡重建第三帝国；¶18：1653–1865 上层信儒；¶19：1811 尤潘基·阿马鲁一世即位、谋求近代化|NPU/SPU/PEU 的现存地图不被开局重写。政治路线争取恢复第三帝国的宫廷与地方盟约；统治者与文官可信 `old_confucianism`，不转换民众宗教。1836–1839 战争、1839 死亡和1865改朝换代是作者未来线，不能无条件强制重演。|
|NKH 大平原汗国|slide18 ¶21：HUS 曾援助原住民和美洲蒙古；¶22：1805–1809 大平原汗国起义遭 HUS/USA 镇压|新的原住民汗号和草原结盟有本地历史来源。新汗是本批虚构的活人，不复活旧汗；主流文化最终只含原住民，满蒙历史参与不等于再次得到 HUS 登记特权。|

新增 NAH/TWT 身份函数必须单独限定 `tag + 本批案件标记 + 原住民文化`，不放宽 A1 法律辅助函数。NAH：`law_monarchy`、`law_census_voting`、`law_freedom_of_conscience`、`law_elected_bureaucrats`、`law_professional_army`、`law_slavery_banned`、`law_racial_segregation`、`law_interventionism`、`law_mercantilism`；主流固定本案四文化 `nahua mixtec zapotec tarascan`，不得把 Mexican／south_andean 当原住民。TWT：君主制、`law_oligarchy`、信仰自由、`law_appointed_bureaucrats`、职业军、禁奴、种族隔离、干预主义、重商主义；主流 `quechua aimara`（已核当前文化键为 aimara），国家信仰选 `old_confucianism`，明确这是对“儒学宫廷”的本批政策解释，非原文称所有人口儒教。两国均用 default hierarchy。其余已有法律不批量套用 CNE 或 HUS 政治模板。窄替换NAH/TWT国家定义时保留原版颜色、首都与其它字段，仅将NAH的tier设kingdom、TWT设empire，并在TWT主流加aimara；不改开局owner-state人口。[G01、G02、G03、C06]

## 3. 入口、压力和三条政治行动

MEX 入口只属于活的 MEX。安第斯入口属于活的 PEU、NPU、SPU，且确实拥有 `geographic_region_peru` 内人口；三者各有本地压力，不再让 NPU 永久遮掉 SPU。BOL、IQU、ECU 的份额不自动卷入割地；IQU 的 Huachaca 可作为已有统治者的外交背景，不能被偷走当新国国王。

每一地区族系只允许一个活动复国国家／案件。MEX 与 Andes 各有独立全局 epoch 与终态；每个本地政府保留自己的压力和回应。第一份实际成立的 NAH/TWT 或和平复统才占用地区案件；单纯点击、达到压力或创建失败不写“已解决”。另一个秘鲁政府在 TWT 出现后进入“承认／谈判／拒绝并备战”阶段，不能再生成第二个 TWT。后续加入须该政府自己的明确选择；拒绝不会凭关系高被吞并。

|行动|可见、点击和最终 effect 同一政治门槛|实际效果与退出|
|---|---|---|
|承认旧王朝与地方盟约|合法性 ≥50；`ig_rural_folk` 在政府；当前案件可处理、没有本案热战；目标 TAG 尚不存在，或已有同案合法原住民王朝|不存在目标时当前政府 `change_tag`，随后核实际 TAG 才设和平完成、配置相应君主和原住民主流。已有同案 TWT 时向实际 TWT 发一次带 epoch 的合并邀请，接收者 90 日内同意才合并；两侧重新检查身份、独立性、战事、存活与 nonce。拒绝／超时保留两国，关闭本次请求，12 月后可再议。|
|地方议会与地权谈判|合法性 ≥50；农村或知识分子在政府；无同案战争、无现有谈判修正|36 月 `authority -100`、农村好感 +2，压力立即 -15，期间月度压力额外 -2；只扣本次一次，可自然到期再用。谈判不是复国成功，也不会发军队或改 TAG。|
|镇压复统组织|合法性 ≥50；武装力量在政府；现有正规营数 ≥本案起兵目标数的 1.5 倍，最低 8 营；无当前同案战争|用当前本国原住民 pop 的 40% 一次迁徙契约，余下原住民 `add_radicals` 0.15；处理本案活的政治人物；关闭本地主动复国入口。墨西哥案件可终止；安第斯只终止本政府，不能替另一秘鲁政府表态。|

AI 权重：承认基础 30，原住民份额≥50% +30、激进派份额>25% +30；谈判 50；镇压 15，军力≥目标两倍 +20，民族至上／种族国家 +20。不检查具体党派拼盘。国家死亡、无本地州或 TAG 变为无关国：日志 invalid 并有条件清本案修正；不自动生成一个亡国替身。

压力以 0–100 为量纲：初始 25；每月基础 +1；激进人口份额>15% +1；SoL<10 +1；谈判期间 -2（因此平稳政府可缓慢降压）。达到 100 后尝试本案起兵；没有合法领土／有内战／目标 TAG 被无关存活国家占用时显示具体等待原因，不反复生成奖励或国家。争取承认、谈判、整军、改革和压制都各有可见结果。所有 JE 默认钉选。[C01、G04、G05]

## 4. 起兵土地与人口：明确保留“小国一州”的理由

实施补充裁定：政治镇压的准备营数是保守估计，大国使用min(当前全国人口50%,两座合格核心州最高人口合计)，小安第斯使用最高单个合格州；取对应军力档×1.5且最低8。按钮不承诺它与下一次随机割地的实际军力完全一致。实际初建军队严格按已经转入新国的真实人口档计算。

当前只读人口源：MEX 6,699,263／原住民 3,684,595（55%）；NPU 866,600／563,192；SPU 681,108／520,204；HUS 25,589,642／5,117,928；USA 15,833,769／180,078。NPU+SPU 原住民共 70%，但不能把各国都写成 70%。[P04]

|案例|割地方案|限制|
|---|---|---|
|MEX、或拥有 ≥5 个有人的秘鲁州的较大 PEU|选两座实际相邻、当前全部 state 对象属于案件政府的核心州|每州人口≥100,000、原住民份额≥35%，本王朝核心文化合计份额≥25%（NAH四文化／TWT两文化）；合计≥400,000；合计不超过原政府人口50%；留下至少两座有人的 state、剩余人口≥200,000。没有满足组合则等待，不偷第三国份额。|
|只有2–4个人口州的NPU/SPU/PEU|选一座人口≥200,000、Quechua＋Aimara份额≥40%的核心州|保留至少一座人口州、原国剩余人口≥150,000。NPU 的 Cajamarca 306,500（原住民95%）和 SPU 的 Arequipa 277,400（81.8%）是当前可能的规模，不把薄弱的 Pastaza/Tarapaca 剩余人口当足够国力。|
|只剩一座人口州、无合格州或已有目标 TAG|不开出新国|保留和平政治路径或现有 TWT 的承认请求；不会制造空国，也不强切第三方 province。|

本地原住民份额值使用 `every_scope_pop` 对 `total_size` 求和，文化经有效 discrimination trait group 分类，再除以严格 >0 的 `state_population`，夹在0–1；按整个 pop（含家属）计算，不拿 workforce 作总人口。原版 script values 明确支持所有迭代列表；`total_size` 为 pop、`state_population` 为 state。[G06、G07]

`create_country` 直接给完整已选 state 列表，使用 `on_created` 记录实际新国家、案件、来源与资本；不先转一州再漏转剩余。落地前再次验证来源／归属／数量／人口，当前 effect 内为一次事务；成功后才记录已建国和本案 TAG。只转当前国家的 state 对象，不对整个 `state_region` 的 IQU/ECU/USA/HUS 份额操作。原国家仍有存活领土；双方各有本国首都。首都选新国人口最大的已转州。

## 5. 具体人物、角色与不复活约定

|角色|来源与人设|实际作用|
|---|---|---|
|NAH 王族代表：伊特斯科亚特·蒙特祖玛 / Itzcoatl Moctezuma|本批虚构19世纪后裔，建议生于1788；Nahua、Catholic、王党思想；不能称作者已给定姓名、出生年|承认事件中的王族签署人；君主制成立时成为 ruler；不同时强置所有 IG 领袖。初次可生成窗口1836–1860；此后若未见，由本土制度产生普通新君主，不重造历史名人。|
|NAH 共同体代表：Benito Juárez|原版 `mex_juarez_character_template`，Zapotec，1806.3.21，现代化思想、知识分子；真实模板不等于已在1836存在|只复用实际存活、未担任外国统治者的人物，能担任谈判／地方议会代表；不自动生成第二个Juárez，不把他改成蒙特祖玛王族或亲王。不存在时使用本国活的原住民政治人物；不以他为必需钥匙。|
|TWT 王朝代表：尤潘基·阿马鲁一世 / Yupanqui Amaru I|作者1811即位；本批模板补充出生1778仅为可执行年龄选择，Quechua、old_confucianism、reformer。若1836–1850初次入场且从未见／死才可生成|恢复印卡宫廷，保留现代化议题；不会预定1839死亡。已死亡或窗口过后，制度仍可复兴，由实际活人／新一代普通君主承继，绝不重生阿马鲁一世。|
|TWT 军事代表：鲁米·基斯佩 / Rumi Quispe|本批虚构，Quechua、Catholic，1803生，jingoist_leader，armed_forces；地方军人|战争成立时作为将领分配给本案陆军；不是既有 IQU 君主 Huachaca 的替身。|
|NKH 新汗：塔坦卡·帖木儿 / Tatanka Temur|本批虚构，Siouan、Animist，1805生；以草原盟约／汗号体现1805–1809前史，jingoist_leader|君主与将领可兼任（沿当前骨架），有实际军队分配；人物死亡后正常继承，不由月度维护补刷。|

姓名、文化、宗教、IG、思想与角色分开。模板思想使用当前实际 `character_ideology = yes` 键。Huachaca 是原版 IQU 的 Quechua 在位君主，Alvarez/Gamarra 的 culture=primary 并非可靠原住民证明，不能按现实姓名或“秘鲁人”分类。[G08–G10]

每一具名模板采用永久 global seen/dead + 活体搜索（本国、其他国家、exile pool、void）的契约；首次创建之前先写 seen，角色死亡 on_action 记 dead。已见但没有活体意味着不再创建，不能将“查不到”当未出生。异国在位 ruler 不转移；非 ruler 的当事人须实际与本案国家／文化／政治角色相关。王朝制度可以失去该人后继续运转；不创建与之前同名同生年的“继任者”。

失败人物处理最多三位，优先本案代表，再本国原住民 IG leader／agitator／general；仅活人、非外国 ruler。先解除将领分配、替换为 agitator 角色，再进入流亡池；使用原版 `exile_character_with_role_cleanup` 链。HUS接收条件取实际 `invite_exile`：人物接纳≥`acceptance_status_3`、`can_agitate = c:HUS`、HUS的`empty_agitator_slots >= 1`、未实行closed_borders，以及原版devout／state_religion宗教约束。HUS还必须实际存活；只有全部满足才 `transfer_character = c:HUS` 并调用 `free_from_exile_effect`。未满足条件留全球流亡池并给明确反馈；不把 `exile_character=yes` 谎称已经抵达HUS。败国 ruler 可在吞并前解除 ruler 角色后成为流亡者；不给他保留已灭国的军职。[G11、G12]

## 6. 真正战争目标与结算，不再读取泛占领率

复国双方需要争夺政治国家，因此继续用双向吞并诉求，但采用本批专用自定义战争目标 `wg_nesnd_restoration_settlement`：`kind = custom`、`target_type = country`、`contestion_type = control_half_target_country_states`、`annexes_entire_country` 和原版吞并冲突验证设置；只允许本案互为敌方的 holder/target 和确切 DP。禁止其它玩家从外交菜单随意添加此目标，禁止附加无关目标。它的 `on_enforced` 才是结果授权，绝不按第三方占领或对手不见直接吞并。

这是原生已记录接口，不是模拟胜利：G `war_goal_types.md` 明确 custom 无预置效果、只运行 on_enforced，并明确 ROOT=holder，`scope:target_country`、`scope:diplomatic_play` 等；实际 `restore_union` 采用 custom 并在 on_enforced 改法、建宗属。原版 annex_country 有对应冲突／占领要求。自定义回调可以在明确吞并之前处理 still-alive target，避免依赖引擎先吞并后留下亡国 scope 的顺序。[G13–G15]

顺序固定：检查案件 epoch、双方和确切 DP → 写 resolving 防重入 → 若胜者是镇压政府，败方 NAH/TWT 在仍存在时执行一次40%迁徙和人物流亡 → 胜者 `annex = scope:target_country` → 只在目标已不存活、胜者实际得到土地后标实际胜果／完成。若吞并未成功，记录 settlement_failed、保留可诊断原因，不付胜利奖励，也不循环再搬40%。原住民胜利不把政府的非原住民人口强制迁出；新国完成相应君主／身份检查。

`create_diplomatic_play` 使用本机 docs 记录的目标 country scope + `initiator`、`type`、`war=yes`、`handle_annexation_as_civil_war=no` 形式，或者经原版 Sepoy 调用证明的 initiator + target_country 形式；实施时只锁定一种，按实际解析/MCP闭包核对，不保留未经证明的 `annex_as_civil_war` 参数。创建之后必须找回 **同 type、initiator、target、案件 epoch 的实际 DP** 且具双方目标，才置 dispatched。[G07、G16]

`on_war_end` 的原版源码标 ROOT=DP、scope:actor=initiator、scope:target=target；它只负责核查已有结果、标无战争目标执行的停战，不假设 actor 就是 winner。和平无吞并：两国存活，记“分治停战”，不称王朝统一胜利；拒绝再战保留实体。退让有目标执行则走同 on_enforced；创建失败不算战争，12月内每月最多重试一次，届期关闭为“军事决裂未成”，保留实际国家和和平外交，不无限 pending。原父国遭第三国吞并、叛军遭第三国吞并、普通转TAG：记录 interrupted/displaced，取消未执行的奖励和战争；不复活任一方。[G17]

## 7. 大规模迁徙：失败来源仍活时一次结算

政治镇压：当前案件政府所有现存原住民 pop 各迁40%；战争镇压：败方原住民政体现存原住民 pop 各迁40%，分母为战败结算时仍在败方境内的人口。不是“原国开局人口40%”，也不把已被第三方夺去的人群算入；不会 kill/create 冒充迁徙。MEX 当前政治镇压量约1,473,838人；NPU约225,277，SPU约208,082。战败量按实际被割出的领土与战争后的活人口变化。[P04、G07]

目的地是实际存活的 HUS、有人的实际 owned state，源国与目的国不同；从HUS人口州中分散选目的地，每个原源 pop 只一次 `population_ratio=0.4`，不是四次10%。州临时迁入吸引 +25%、60月（最多一份，不每个pop叠一份），实际搬迁即时发生，修正只表达后续网络。原生 move_partial_pop 会令迁入者失业，某些 slave／不可失业职业会转默认 pop type；文案不承诺职业、就业或生活水平保持。[G07、G18]

若 HUS 不存在／没有有效人口州：**立即结算“无可接纳目的地”**，人口留在当前合法所在国，人物可留全球流亡池；清 pending、记 failed_destination、给源国结果文案，不创建HUS、不等到永远，也不擅自把本应赴HUS的原住民改送CNE。若源国先被无关方吞并而错过受控结算：终止人口迁徙，不遍历吞并者所有原住民；仅对已存活于流亡池的本案人物允许适格HUS接纳。明确这属于来源已失效的终态，不假称迁徙完成。

每地区 epoch 的 `refugee_state` 为未开始／执行中／已迁／目的地缺失／来源失效，不仅一个布尔值。标记先防重入、实际成功／失败再终结；新旧窗口重复点击不得重复迁移。国家 retag 同对象维持 receipt；同 TAG 后来复国不继承重新领款机会。旧草稿已有 `refugees_sent` 则承认已执行，不能重搬；旧 pending 经当前来源／目的地重新核对后仅处理一次或明确关闭。

## 8. 原住民登记后的满蒙外迁

只有 A1 真实完成 native route 且 epoch 正确的 original HUS 调用；不改 A1 的12月时钟、选择、冻结法律、革命继承、global wait 和 legal prepared 边界。将 `nesnd_hus_manchu_exodus` 的内部迁徙 body 改成：

1. 对每一个原 HUS 满蒙 pop（A1 `nesnd_hus_manchu_culture` 分类）先选择非HUS、存活、有人的CNE与USA西部目的state；每源pop最多一个CNE州和一个USA州，防止巨量堆入一州。
2. 两者均有：每个源pop执行一次 `random_list`，70权重 `move_pop` 到CNE，30权重 `move_pop` 到USA西部。此为逐社区目的地概率，不拆人数，不保证全国人口精确70:30。
3. 只有一个目的地有效：全部送往该有效目的国，文案明确“原定分流目的地缺席，转赴另一处”；不伪称仍70:30。USA西部只按已核战略区域和USA实际所有权，不使用WES。
4. 两者都缺席：一次 terminal_no_destination，人口留原居地，清pending，写本epoch已处理；不能永久等待。该终态不改 native route，也绝不转入汗国／战争路线。
5. done、result、global exodus_epoch 与一次通知一起收尾。已有 done 或 global 同epoch收据的旧存档保持已处理，不再搬人。A1实际原legal完成/退休/革命守卫不变。

当前源计划人口的满蒙总数7,676,893仅供规模背景；各目的国实际人数取决于不同大小社区的独立抽签，不承诺精确份额。[P03、G07、C02]

## 9. 满蒙登记＋永久美国内战信号：四州建国

触发接口沿用 A1：合法 completed Manchu route + 原版永久 global `american_civil_war`，两者先后顺序任意。只有此分支写 campaign started；native route 绝不写该标志。原HUS消亡而汗国未成立：终止该原HUS的发动资格，不从墓地继续执行。汗国已成立后，独立的NKH/全局维护负责后续，不能依赖HUS仍活。[P03、C02]

候选 state：owner当前是USA、`sr:region_great_plains`、人口>0；不是任意整个state_region。USA必须至少有5座人口state，建国后仍有实际人口领土。当前USA大平原涉及Louisiana294,684、Arkansas92,620、Missouri367,508、Iowa43,992及Minnesota16,000、SouthDakota12,000、Nebraska21,000的美国份额。LA–AR–MO–IA是当前完整四州链示例；实际选择不硬编码这四个。[P04、G19]

**选择算法（随机且可证明有限，不用预制假邻接）：** 清本轮临时选择／排除标记 → 最多15次尝试（该战略区15个region；USA每region最多一个state）；随机选未排除的合格USA州为种子；重复三次从“未选合格USA州且 any_neighbouring_state 是本轮已选州”中随机加一州。任何≥4州的连通分量从任一种子逐次扩张都能填满4，不存在草稿所担心的“随机先走错支路”死路；少于4的分量扩到尽头后，将整个已探索分量标排除、清选择，换下一种子。已满4就停止后续尝试。使用原生 `while count`／列表与 `any_neighbouring_state`，后者作用域是state，不能拿 country 的 `is_adjacent_to_state` 充当state对state关系。[G06、G07]

提交前再核4个唯一state、全USA、有实际人口、连通、USA仍剩人口州；必要先把USA首都移到其最大剩余州。`create_country` 一次列四个state，on_created确认NKH四州和本国首都后才置created。迁移第三方部分、先造空国、失败后遗留选中标记均禁止。无四州连通解时继续待命并展示原因，月度重试；这是明确无领土解的等待，不是已经成立后的无限pending。

## 10. 建国后两国各迁半数与军工预算

顺序固定：USA四个state转给NKH → 确认NKH四州、人口、首都 → USA余下境内原住民pop各迁50% → 原HUS仍存活时其境内原住民pop各迁50% → 下一日重新读当前人口，做一次军政准备。四州已经在NKH的人口不再从USA算第二次。每源国各有独立永久receipt；缺HUS记source_absent并关闭其迁徙，不能拖死USA一侧；NKH缺失则终止，不复活。每个源pop随机选一个实际NKH州，单次0.5，不能向四州分别搬0.125。迁入州的每次owner和活体检查先于effect。迁出失业／职业变化沿原生说明。[G07]

以当前LA–AR–MO–IA示例：四州798,804、已有原住民50,136；USA余下原住民129,942，迁64,971；HUS迁2,558,964；建国后约3,422,739人口。实际动态建国不使用该常数。其它合法四州和战争损失使结果变化。

|对象|一次军力目标（非无条件额外赠送）|设施上限与科技|
|---|---|---|
|NAH/TWT初建|按本国实际总人口：<300k=2营，300–599k=4，600–899k=8，900–1199k=12，1.2–1.799m=16，≥1.8m=24；只补现有正规营不足；至少75%线列步兵、其余炮兵，2营档全步兵|兵营容量仅补至目标，优先分散到本国有人州；首都军工1／工具1／行政1；人口≥600k再给炮厂1和食品1，≥1.2m行政总2；已有够用不增。不得原样给一座277k州24营、数十工厂。|
|NKH|人口<800k=8；800k–1.599m=16；1.6–2.399m=24；2.4–3.199m=32；≥3.2m=40营；只补不足，80%线列／20%炮兵|四州兵营尽量均分，单州新补不超过10级；军工总2、炮厂总1、工具总2、食品总2、行政总4、造纸总1、建设总4为可补上限。资本州不一次塞入40营及所有产业；已有建筑算入上限。|

设施是可用产能、实际雇佣由原生经济决定，不承诺自给或满员。无海军、无凭空金币。军队单位使用 `combat_unit_type_line_infantry` 与 `combat_unit_type_cannon_artillery`；相关 `line_infantry`、`artillery` 及必要前置均为era1。新国保留origin已继承技术，最低补齐这条era1军事链与所建基础工厂所需技术，不无条件给全部era2、general_staff、percussion_cap。新建formation必须有实际unit和同国commander；只在本案initial preparation一次补兵，不能每月把战损补满。后续正常经济与征募由玩家承担。[G20、G21]

## 11. USA、HUS各一场真实快速战争与终态

两条案件分开：USA→NKH吞并、NKH→USA羞辱；HUS→NKH吞并、NKH→HUS羞辱。每条独立nonce、attempts、DP scope、dispatched、outcome；禁止一次 has_war flag 代替两场。使用当前专用 `dp_nesnd_khanate_suppression`、`mirror_war_goal=no`，创建 `war=yes`，省略漫长升级期；“快速”指直接进入真实战争，不强迫一方在固定天数投降。[G07、C03]

吞并使用本批 `kind=custom` 的专用目标、精确案件valid、在on_enforced中实际annex后才记NKH败亡；羞辱使用本批窄定制的 `kind=humiliation` 目标，保留原生羞辱效果，on_enforced只记录对应该国的真实胜果。两种类型都仅用于本案，避免改全游戏原版war_goal。若root要求显示原生名字，loc可显示“吞并汗国／羞辱”，但语义与原版相同。[G13–G15]

创建前守卫：双方存活、NKH确实是本案四州国家、不是同一对象、没有本案DP、没有互为敌方的现有未结战争。若同pair已有战争，先等其结束，不将该战争伪装成本案；12月最多12次尝试，期限后明确“未能发动干涉”并关闭该条。若处于原生革命／分裂／属国限制使实际DP未创建，同样走有限重试；不在写成功flag之后才发现没开战。

双方同盟／防御约只移除 **本案pair** 的该类 pact 和本案pair停战，避免目的互斥；不解除任何第三方的联盟。NKH作为新建国须真实独立；若创建时继承source宗属，使用有原生文档的 `make_independent=yes` 解除NKH本身继承关系，不能使USA/HUS或其第三方臣属全独立。USA/HUS为第三国属国、正内战或受条约限制时不强改其整个外交体系；实际create失败按上段有限终态。玩家得到原因，不能称两场均胜。[G07]

双方退让走on_enforced；双方都活的白和平为stalemate；一国亡于第三方为opponent_gone，不授羞辱胜利；NKH被任一国实际吞并则整个汗国链failed，关闭另一条待发案件；两场先后结束、只一场已结束都保持独立。存活JE的完成要求“NKH存活 + 两条均终态”，正文列明胜利／停战／未成战争／对手消失，不将所有终态统称击败两共和国。胜利修正仅在对应羞辱goal实际执行时授予，最多一次。

## 12. 北美宣称、全美洲决议和完整HUS法制

北美宣称按有效G+C的 `geographic_region_north_america` 加 `sr:region_central_america`（后者包括加勒比诸岛）及`STATE_GREENLAND`逐实际state_region加claim；不能把country iterator当州列表。全美洲决议用有效 `geographic_region_americas` 全部陆地地区并明确纳入 `STATE_GREENLAND`，冰岛不纳入：原版把格陵兰归斯堪的纳维亚战略区，故“全美洲”的地理完整性需要这个显式补项。当前C的pacific_coast还包含作者`STATE_NORTH_DAYUAN`和`STATE_SOUTH_DAYUAN`，必须随有效战略区域包含，不能只拿原版州列表漏掉它们。无人口／未殖民地区也必须实际完整拥有，不能只数当前owned states；外国split-state使条件失败。[G19、G22、C07]

visible只本案NKH；possible与effect同样检查：每一目标state_region完整归ROOT、当前没有活的旧HUS、无正在进行的本案战争或事务。不能通过同名／flag冒充HUS已经亡国。effect先写 `nesnd_hus_native_successor` 和A1 `nesnd_hus_native_legal_prepared`，change_tag=HUS，核实际TAG，再调用 A1 clear、default hierarchy、mutating guard和18条作者HUS开局明确法／原版liberal间接法（下表）。人口、财富、军队不重建。[C02、C03、G23]

|法组|准确目标|
|---|---|
|governance / power / religion|presidential_republic / census_voting / total_separation|
|bureaucracy / army / education|elected_bureaucrats / professional_army / private_schools|
|tax / economy / trade / land|per_capita_based_taxation / laissez_faire / mercantilism / tenant_farmers|
|citizenship / migration / slavery|racial_segregation / no_migration_controls / debt_slavery|
|speech / women / colonization|censorship / no_womens_rights / frontier_colonization|
|labour / labour associations|no_workers_rights / anti_strike_laws|

这些键均加 `law_` 前缀。另六普通法组需要显式确定，防止NKH继承来的法律漏留：merchant_navy、no_home_affairs、no_police、no_health_system、child_labor_allowed、no_social_security。它们是当前原版对应法组的基础法，本批将这六项作为**明确补全政策**，不冒称作者HUS历史文件逐条写过；合计24普通组，特殊印度／江户／HUS阶序组均应不激活。[G24]

最后只保留实际有效文化数据库中 `heritage_group_indigenous_american` 的主流文化；清除所有汉、满、蒙古及其它非原住民主流，先保证至少一种原住民主流再移除旧文化，避免无主流国。使用A1函数允许的 native_successor路径，不改变函数对其它国家的拒绝边界；清三法/旧法/专用修正/临时mutating，永久successor证明保留。不可把种族隔离永久锁死；之后按普通政治运作。A1所有独立阶序类／意识形态／旧档时钟不重写。

## 13. Turtle Island与Cherokee旧链

保留当前 `REPLACE:je_unite_the_nations` 对NKH/native_successor的隐藏、invalid处理；新增三个原版按钮的窄REPLACE：proclaim、organize、offer_confederation，在visible、possible、effect三层加同一排除，effect用真if守卫，旧已开的按钮也不能把汗国／原住民HUS改成TIS或产生扣款。其余原版国家行为逐AST原样保留。当前G与C的country_formation没有TIS实体条目，不能虚构“修了TIS形成决议”；真实TAG入口是这个按钮。[G25、C04]

Cherokee原版monthly随机池可继续投到同namespace的无害stub；当前 `events/native_resettlement.txt` 的 .1–.7 全部 `trigger=always no`、`cancellation_trigger=always yes`、选项无effects，覆盖排队和已开窗口。`REPLACE:je_indian_removal` 当前已不可出现并invalid；后续验证其原版所有complete/fail/monthly/on_action引用都指向这些stub，没有另一个驱逐效应残留。没有证据不扩张到全局on_action整文件替换。[G17、C05]

## 14. 旧档、旧窗口和生命周期矩阵

|边界|规定结果|
|---|---|
|预览中变量不存在／owner缺失|显式exists分支、optional scope；tooltip与写后读执行分开，不能因预览不执行write读未赋值变量。沿A1修复经验逐本批扫描。|
|已写draft globalresolved但没有实际NAH/TWT／成功结果|不授胜利；只在没有真实国家、没有迁徙receipt、没有活DP时迁为“旧案关闭／可重新政治讨论”，按case迁移一次，不盲目重开战争。|
|已有NAH/TWT但旧版president／缺主流身份|保留真实人口与领土，一次legacy adoption：事件说明并应用本案约定王朝身份；已有有效活ruler优先审查，不凭空复制名人。没有案件标志的普通原生NAH/TWT不被批量接管。|
|旧NKH已创建、0–3州、旧旗标说4州|不从他国自动补割州；终态/旧案待人工诊断，不重复50%迁徙，不追加“补偿”40营。报告实际不满足建国契约。|
|旧population_sent/created/prepared|承认receipt，仅补元数据，不能重发人口或军队。缺源国／目标已死明确关闭，不重复创建已亡NKH。|
|普通革命／继承／转国|A1合法路线继承仍由A1；A2按真实case owner同对象、epoch与明示origin继承记录判断，不能把任意同TAG新国当原主。普通转TAG退出本案政治身份；仍活人物可在新国存在，但不会强改回。|
|战争途中来源／目标／目的地消失|各条明确failed/interrupted/no_destination，清临时DP引用及selection，不用死scope继续move/annex。|
|两个相反旧窗口连续确认|第一次事务改变epoch/state，第二次effect再次验证相同门槛与nonce后无副作用；不能先迁移再检查按钮条件。|
|JE invalid与修正到期|所有remove_modifier先has_modifier；只清本案修正与临时scope，不清A1global12月时钟；UI显示终态/缺失原因。|

上述旧档兼容不调整历史人口，也不把一次预存档文件修改说成旧档人口已重配。涉及不明旧记录冲突宁可给明确终态／诊断，不在同一存档重演不可逆50%/40%人口转移。

## 15. 文件所有权和A1局部边界

本批拟独占编辑以下C文件；新增文件标“新”。同名不同目录分别计文件，最终清单按实际闭包冻结，不承诺人为固定数量。

|文件|修改范围|
|---|---|
|common/journal_entries/nesnd_american_restoration.txt|MEX/Andes本地压力、王朝/分治后继、终态与钉选|
|common/scripted_triggers/nesnd_american_restoration.txt|实际身份、政治门槛、核心州、case/DP精确条件|
|common/script_values/nesnd_american_restoration.txt|人口份额、压力、军力档与剩余人口预算|
|common/scripted_progress_bars/nesnd_american_restoration.txt|0–100压力细项|
|common/scripted_buttons/nesnd_american_restoration.txt|承认／谈判／镇压及对现有TWT的请求|
|common/scripted_effects/nesnd_american_restoration.txt|事务、政治身份、人物、迁徙、创建与结算|
|common/scripted_effects/nesnd_a2_common.txt（新）|本批兵营容量、旧实体与旧精确DP目标迁移辅助；不改A1外围维护|
|common/scripted_effects/nesnd_a2_manchu_exodus.txt（新）|A1 exodus body调用的70/30目的地抽签与缺席收尾|
|common/on_actions/nesnd_american_restoration.txt|狭窄周/月监视、战争结束和本案人物seen/dead|
|common/diplomatic_plays/nesnd_american_restoration.txt|本案双方战争目标、直接战争、精确回调|
|common/static_modifiers/nesnd_american_restoration.txt|限定期限与防重复的本案修正|
|events/nesnd_american_restoration.txt|完整双方事件、邀请90日、战果与HUS避难通知|
|common/character_templates/nesnd_native_americas.txt（新）|上述A2虚构/作者人物模板；不碰C2的18人|
|common/war_goal_types/nesnd_native_americas.txt（新）|复国结算、NKH吞并／羞辱三个专用目标|
|common/country_definitions/nesnd_native_khanate.txt|保持TAG定义有效，仅需要的身份默认值|
|common/country_definitions/zzzz_nesnd_native_restoration.txt（新）|NAH/TWT窄REPLACE：原色/首都保留，kingdom/empire及TWT的aimara；不改原版大文件|
|common/government_types/zzzz_nesnd_native_khanate.txt（新）|原版gov_khanate窄REPLACE，仅在现有TAG判定OR中增加本案NKH，保留继承/摄政/臣属守卫及两个原版回调；不让Siouan汗国因不在原版亚洲TAG列表而显示一般帝制|
|common/scripted_triggers/nesnd_native_khanate.txt|4州、actual DP、Americas、successor条件|
|common/scripted_effects/nesnd_native_khanate.txt|四州／迁徙／预算／两战／建HUS；A1法律边界见下|
|common/script_values/nesnd_native_khanate.txt（新）|军队/设施档、选区/迁徙人口预算|
|common/on_actions/nesnd_native_khanate.txt|NKH自身及两国独立监视，不只HUS/USA|
|common/diplomatic_plays/nesnd_native_khanate.txt|两条case的实际直接战争|
|common/journal_entries/nesnd_native_khanate.txt|等待4州、两条战况、实际存续结局|
|common/decisions/nesnd_native_khanate.txt|全美洲＋HUS真亡国＋事务重查|
|events/nesnd_native_khanate.txt（新）|汗国人物/建国/两国战争/终局通知|
|common/scripted_buttons/zzzz_nesnd_turtle_island.txt（新）|仅3按钮NKH/successor守卫，余nativeAST不变|
|common/journal_entries/zzzz_nesnd_turtle_island.txt|仅必要同一身份守卫；已满足则不改|
|events/native_resettlement.txt|旧窗口闭包读取；现stub若已足够则只冻结不改|
|localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml（新）|A2所有生效中文、name/desc/tooltip/war goal/actor/status|
|localization/english/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml（新）|对应完整英文|

**A1有条件局部编辑**：`common/scripted_effects/nesnd_hus_registration.txt` 只准 `nesnd_hus_manchu_exodus` 内body；如果需要外置A2helper，由该函数调用，签名和外围maintenance不变。`events/nesnd_hus_registration.txt` 只准迁徙／汗国通知的条件与A2文本接线。`common/journal_entries/nesnd_hus_registration.txt` 只对Cherokee inert覆盖核闭包，原则不改。NKH effect中的 `nesnd_native_primary_cultures_only`、clear/default/mutating/native_successor顺序与A1legal prepared语义保留；新增ordinary law补全须独立helper，不能混入A1classifier。

禁止编辑：A1 lawgroup/3laws/12classes/24bounds/68ideology/nativeGUI、公民法六个ordinary guard、历史HUS开局、globalepoch计时与革命来源证据；B unity及B2、C diplomatic/shared请求协议和C2公民路线/18人文件；所有history/pops。若确有必要越界，先给localized diff计划，不能借本批GO重构别人的模块。

## 16. 文案闭包与后续验证约定

写作遵循已读 `nesnd-player-writing`；实施前再取作者replace同类文本对照。新文本写本批专用双语文件，实际国家用有效country scope的GetName／旗帜，不把CNE固定为某政体；明确历史背景才可称吴国、北明。正文交代盟约、宫廷、地权、迁居与战争主张；内部epoch、fallback、invalid等不进入玩家文本。

每个真实分支必须有自身结果文本：和平复统、承认现有TWT并拒绝/同意/逾期、谈判到期、政治镇压、起兵待领土、战争胜/败/分治/第三方中断、HUS无法收留、人物留流亡池、满蒙70:30/单目的地/无目的地、NKH无连通解/两战独立状态/原HUS真亡国与终局。第一版写完对原稿逐类并排审阅，记录改写理由；不把“按钮有loc”当通过。

GO后阶段顺序：完整编辑闭包 → 停编辑 → `batch-a2-implementation.md`、独立所有权SHA、A1 localized diff、原版按钮窄diff、文案对照 → READY_FOR_TEST → root分派验证。测试阶段覆盖实际ordered AST及动态效果解释器、有效G+C覆盖、所有历史owner-state人口源SHA不变、24普通法与A1接口回归、4州所有候选/小连通分量/split-state/移首都/只剩4人口州、70:30舍入与目的地缺席、50%后割地分母、40%先吞并回调、sourcegone/反向旧窗口/死亡与流亡池/已有模板、两个独立DP与goal实际存在及全部终态、Cherokee旧7窗口/TIS3按钮效果守卫、当前MCP查询与限定闭包Tiger。

后续可能需要一次定向引擎证据的接口边界：自定义goal on_enforced内的事务顺序、`move_partial_pop`后原pop余数继续可寻址、country创建后人口缓存刷新、native DP立即战争与特殊外交关系拒绝。静态解释器/MCP/Tiger均不能把这些说成已实机验证；如果发现未知接口，停止对应实施或测试并报root，不以手写状态模型掩盖。人口迁徙是明确用户范围，只有实际不可证明的接口才需计划修订。

## 17. 审查时需要显式接受的政策选择

root已批准：两州大国／一州小安第斯、NAH议会君主／TWT寡头宫廷、old_confucianism仅国教、40%失败迁徙及缺HUS即时终结、逐源pop70/30概率目的地／单目的地全送／双缺席终态、12月有限干涉重试、全美洲补格陵兰、原住民HUS24普通法、自定义war goal先迁徙后吞并。代码实施与后续验证分阶段进行。

## 来源索引与SHA

下表由只读源采集追加；行号指当前源文件，SHA是文件内容指纹。候选全包仍有其他代理工作，**本报告不声称整个C固定SHA**。

<!-- SOURCE_CAPTURE_START -->

编号字母/数字后缀属于同一来源组；正文 `[G07]` 例如指 G07a–c。路径均为实际读到的文件。

|ID|来源（定位）|SHA-256|证据用途|
|---|---|---|---|
|P01|[北明ppet.pptx（slides18/19）](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx>)|`b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`|作者原件；slide18 ¶8/18/21–23，slide19 ¶12/17–19/24/28。PPT只读。|
|P02|[americas-acceptance-native.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/americas-acceptance-native.md:1>)|`0f374fc9b175b849e07b06088e5128642418e98383339556a8c9cdaefe5d3a3b`|旧原住民复国/人口研究；其中HUS公民法变体建议已被A1取代。|
|P03|[hus-khanate-native-contract.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/hus-khanate-native-contract.md:1>)|`63e6273183ebdf62652614b70ddc213da616990b34c217cc68367b287acb4b07`|70:30、50%、四州、两战、TIS/Cherokee原生接口；其无限等待建议被当前授权要求取代。|
|P04|[batch-a2-current-population-source-census.json:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/batch-a2-current-population-source-census.json:1>)|`069c92d7419a27ac914dcb9a3e04c04a30d9fa577001f7acb5b18097344f9ba2`|本次只读当前历史人口/文化源加总，非运行时或测试结果。|
|P05|[remaining-batch-contracts.md:5](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/remaining-batch-contracts.md:5>)|`f5b3a68f93a3b0212f323138441c8f4ca51dbb64ad4c77d078aea481836a07f9`|root分派的A2完整范围。|
|G01|[00_countries.txt:2786](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2786>)|`d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`|NAH:2786；TWT:3109；原色/主流/首都/tier。|
|G02|[00_cultures.txt:11155](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/cultures/00_cultures.txt:11155>)|`30c8a1085257fb130634d3e5cc187d2eef7717a07db5fa7b390846dd319e5baa`|zapotec11155/nahua11346/tarascan11444/quechua11537/aimara11734/siouan12784/mixtec13230。|
|G03|[01_character_ideologies.txt:1692](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/01_character_ideologies.txt:1692>)|`b54d0c294632be73ebc77edcb65d7f841803c6a19bacbb03e6331b0cd2ce39d3`|reformer1692/jingoist_leader2810/royalist3081均character_ideology=yes。|
|G04|[turtle_island_buttons.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/turtle_island_buttons.txt:1>)|`8c5b48719a0e34efb88e6bb7a0c0f428f09fbf2e529a0599902f14a4c66682b8`|真实country按钮visible/possible/effect与旧窗口副作用入口。|
|G05|[04_sepoy_mutiny.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sepoy_mutiny.txt:1>)|`8a213d7c395c6b2cc5f5e8d72d51cb55ab2c0dde62873c30cac07682141e490b`|原生JE→压力/事件→建国与战争caller链。|
|G06|[script_values.md:119](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/script_values.md:119>)|`66431f8e32c467a4b224b87a939189ee26c75ff1c6837f4966c6046cc67725a6`|script values支持所有list、加和与正常scope切换。|
|G07a|[effects.log:878](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:878>)|`24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`|create_country878/create_DP909/move_partial9830/move_pop9844/while37383；country/DP/character/pop/state scope合同。|
|G07b|[triggers.log:2023](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:2023>)|`ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`|any_neighbouring_state2023；culture_percent_state9558；state_population14458；total_size14659。|
|G07c|[event_targets.log:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:1>)|`cc12b15da310d0d8ef10a9209107b4d2298a882fa6ee038c202650e3c9bd7c71`|原生作用域链目标。|
|G08|[historical_leaders_americas.txt:20](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/historical_leaders_americas.txt:20>)|`44fd7167658d98d5afb8e2e172bafbf5ccddf6383bd2a1c92df4b4f189d057f6`|Juarez模板文化/出生/角色/思想。|
|G09a|[country_peu.txt:43](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_peu.txt:43>)|`d7d2c3e147c02dafca2d6ff86ad2a7c86ad2f54af0797241d8683618317316bb`|Huachaca是Quechua ruler/general；Orbegoso/Pierola/Gamarra非任意native替身。|
|G09b|[peu - peru.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/peu - peru.txt:1>)|`0d3482890585aa9cc1301e1dd7265f432166889267325a75d9ae5ebd27a1a27a`|NPU/SPU/IQU实际初始人物归属与Gamarra流亡。|
|G10a|[country_mex.txt:62](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_mex.txt:62>)|`3afe9957089ba056a2c3259f6fb9220ccb4fb7ffe04fa5118f8220674823a911`|Alvarez culture=primary，不能按姓名推定native。|
|G10b|[mex - mexico.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/mex - mexico.txt:1>)|`a07d0a2e8b495704a7be5cbaf205e62591418171f9b3af3d4501d1da11872cb1`|MEX实际已有角色；Juarez不是无条件初始角色。|
|G11|[00_scripted_effects.txt:720](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_scripted_effects.txt:720>)|`278e5988ba786184ee12e1d806a6c72608e7b45df53fb7e4c4e61a6953f8d1c0`|exile_character_with_role_cleanup：exile、unassign、replace roles。|
|G12a|[00_character_interactions.txt:997](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_interactions/00_character_interactions.txt:997>)|`0b563339c7f99f2f599924dba600a4f06b5c23c2cfb5b82434f9249066cea590`|invite_exile完整possible/effect；acceptance_status_3、slot、can_agitate、religion、closed_borders。|
|G12b|[exiles_events.txt:231](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/exiles_events.txt:231>)|`de27e06f386abf931d9a6f76c4abd2cba7ab550ecad94c9a87d3c87b1c828185`|实际transfer_character + free_from_exile_effect调用。|
|G13|[war_goal_types.md:47](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/war_goal_types.md:47>)|`9cb5fa6cd8bec160710433aa4b99a256db9a424a51f1a79998642489c5216c90`|on_enforced ROOT holder、target/play scopes；custom无预置效果；冲突验证由脚本配置。|
|G14|[29_restore_union.txt:152](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/29_restore_union.txt:152>)|`d35ce4855e1861177db618711d103985335d8c853af7249a2604f77df4c0fec0`|原生kind=custom实际on_enforced改法与建宗属。|
|G15a|[00_annex_country.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/00_annex_country.txt:1>)|`f6ced621bac6a29b35d771f1a322219d9520565046af402790bd4ffdf22195e2`|annexes_entire_country、conflict设置、control_half_target_country_states、target_typecountry。|
|G15b|[08_humiliation.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/08_humiliation.txt:1>)|`1dfd74884beb5211093bc474c08fd72bac303ec7f110bfe55143076afa0e0088`|kindhumiliation原生效果、contestion与on_enforced扩展。|
|G16a|[00_sepoy_mutiny_scripted_effects.txt:461](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:461>)|`be32f69bde816f2216d18a29ae1aebca1859f22ea25cf9504b25cf62ff519534`|原生create_DP以及以type/target/initiator重新定位真实DP后加goal。|
|G16b|[diplomatic_plays.md:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/diplomatic_plays.md:1>)|`0c534621315b5490404993cdf5932a2d29901d53d01b63af11bf7a7fea1ec336`|DP字段、mirror、allow_negotiated_peace、on_demand/war回调。|
|G17|[00_code_on_actions.txt:6991](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:6991>)|`ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb`|on_war_end ROOT DP、actorinitiator/targettarget；character_creation2566/death2604；Cherokee池479。|
|G18|[red_scare_events.txt:1276](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/red_scare_events.txt:1276>)|`e5388c4f147bd936dc5ff4836fcc8802bf81b7d70e7793fc79484d8fc76dc15b`|实际move_partial_pop国家→州→pop调用和population_ratio。|
|G19|[north_america_strategic_regions.txt:15](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/strategic_regions/north_america_strategic_regions.txt:15>)|`4ce977e0d1c341868b5105b322927e6967d217355126fd0e646bd11175dc4701`|原版大平原15州；central_america含加勒比。有效候选覆盖另见C07b。|
|G20|[00_land_combat_unit_types.txt:83](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/combat_unit_types/00_land_combat_unit_types.txt:83>)|`ad3ed3d68533cbe6ef05ce014cd88b920b58dc4a42b3e566077cdccee072d86c`|line_infantry与cannon_artillery真实unitkeys、1000 manpower与technology。|
|G21|[20_military.txt:84](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/20_military.txt:84>)|`1cf508f18a4dd98e4227e0f83aab220ca4af23ea2a88500302ed5ec278ea84eb`|artillery84/napoleonic118/line_infantry177的era1与前置。|
|G22a|[02_geographic_regions_america.txt:23](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/02_geographic_regions_america.txt:23>)|`595e7fe64b8224fe5d0f2e2838cc6e94ec7598d1f93f9bb5f248a4dba9c4b36d`|Americas包含North/Central/South；Peru六州。|
|G22b|[europe_strategic_regions.txt:80](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/strategic_regions/europe_strategic_regions.txt:80>)|`bbdc686f2f7ab6c7a88c38b1d9bc120c7358e6abc53796e546b861972e31e974`|Greenland在Scandinavia，计划显式补入Americas；Iceland不补。|
|G23|[00_political_setup.txt:3](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_political_setup.txt:3>)|`70c755848862abb553d5d5279d5f98a8a5e4d14b557aec484096eae316e7e9f4`|effect_starting_politics_liberal，HUS间接no_workers_rights/anti_strike_laws。|
|G24a|[00_navy_model.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_navy_model.txt:1>)|`406371ace46d307f866d27d7eaf1ced01362539788bed79abbb319d218f7d005`|六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。|
|G24b|[00_internal_security.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_internal_security.txt:1>)|`3e7b3fb954ee6d71e87f7e9a5878cadcb8acf9f4704b492c21d20552997caab2`|六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。|
|G24c|[01_policing.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_policing.txt:1>)|`8d6938f1eb556f412ba5353056cd43797f4eea3fb7ea8d6ef6e7e9eeb4a80be3`|六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。|
|G24d|[01_health_system.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_health_system.txt:1>)|`4d015438098f9eea1350bdeb4ffe308e86857c9245e24226ab2e643566e317ed`|六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。|
|G24e|[02_childrens_rights.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/02_childrens_rights.txt:1>)|`5c3659a8cfd083511b47ec0637c0ceb570a823029d9fc082f16ad854598d8818`|六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。|
|G24f|[02_welfare.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/02_welfare.txt:1>)|`42594f77b4566637631453c60749318f21e154e23d554be166ac68c7cac44784`|六个未由HUS历史显式设置的普通法组基础法；本批明确补全政策。|
|G25|[00_turtle_island.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_turtle_island.txt:1>)|`716e4283aa690e7c250e4fa6f756d24ddd31e60e36e24c8f018139c21cd53a26`|JE三按钮、原生形成/吞并链。|
|G26|[01_monarchies.txt:2350](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/government_types/01_monarchies.txt:2350>)|`23c1bf00d72f32d6233de36e721867743f7bb68ce3bb8db2c8b4a440e3698850`|gov_khanate真实TAG白名单、hereditary/摄政/宗属门槛与原生回调。|
|C01.1|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_american_restoration.txt:1>)|`5bc5d152eb3f3d7391727466c678a17f54b1b5dbc6728731ac7f44afc940f240`|当前未验证复国草稿；本计划重写范围。|
|C01.2|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_american_restoration.txt:1>)|`fd4dba348f290096d2cba9c3d1128697d043e798a85adcd57399feec61fa7524`|当前未验证复国草稿；本计划重写范围。|
|C01.3|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_american_restoration.txt:1>)|`d76b802d233ff4dcdc8df834f98cc4534157433103aa6b268171a58f809b53fd`|当前未验证复国草稿；本计划重写范围。|
|C01.4|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_progress_bars/nesnd_american_restoration.txt:1>)|`93150f0e97ee558db1a709fe1d82e06d2916d9767bc5dd0fc12c4489d4cf4ee2`|当前未验证复国草稿；本计划重写范围。|
|C01.5|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_american_restoration.txt:1>)|`4f714f879830ce4d503593f47e44fa30a57fc34f735c491cfcc030638dbb13b5`|当前未验证复国草稿；本计划重写范围。|
|C01.6|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_american_restoration.txt:1>)|`257692e5ea0c71473bec022126cffc4b13b0ffcbd57ed83351178d095ab1e6da`|当前未验证复国草稿；本计划重写范围。|
|C01.7|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/on_actions/nesnd_american_restoration.txt:1>)|`af16a1987b223ffe65b80f0306a51566bc5c757276e10e5e5f2008d37cf5388c`|当前未验证复国草稿；本计划重写范围。|
|C01.8|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/diplomatic_plays/nesnd_american_restoration.txt:1>)|`d9ab23a54e6e1ac031b52d3c67a9a01d7bd5f9ede537aa21b511da8d490e548a`|当前未验证复国草稿；本计划重写范围。|
|C01.9|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/static_modifiers/nesnd_american_restoration.txt:1>)|`54036140fb14379a602d1ddb4c5ff6231dcb3b88eebd83bbf071648fac75d4b4`|当前未验证复国草稿；本计划重写范围。|
|C01.10|[nesnd_american_restoration.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/events/nesnd_american_restoration.txt:1>)|`f14b3e23fe07d0995f64ecd13ced057357a17064887201e226cac72415157f5e`|当前复国事件骨架。|
|C02a|[nesnd_hus_registration.txt:355](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_hus_registration.txt:355>)|`677cec937bd828a0dfbc17d269085cfbd331bba926a66a1169c9f6d8b4f094b5`|A1冻结exodus/maintenance；仅迁徙body可局部改。|
|C02b|[nesnd_hus_registration.txt:68](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_hus_registration.txt:68>)|`f6244afa4abaeed044b971f7c1db32a7c0c08e9cba41649285f658130bd29955`|A1 native/MM分类及USA西部82–85；不编辑classifier。|
|C02c|[HUS.txt:84](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/countries/HUS.txt:84>)|`f5d82f8d4429b41b1e5dddaf554ec312c2e6201863396a921e8a9b92b640e6b9`|HUS开局明确法律＋liberal effect；本批只读。|
|C02d|[batch-a-owned-files-sha256.json:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104/batch-a-owned-files-sha256.json:1>)|`f4d08eea054d5d80528673860b9a7f5deb29c0900f0f9c6b599994afaf48318f`|A1原24文件指纹，A2局部改动必须独立diff与回归。|
|C03.1|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/country_definitions/nesnd_native_khanate.txt:1>)|`67318bccd394b9d4ea4c735eb7e6ac7756fc5784ca26a226406dc0a60fd9b4d4`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C03.2|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_native_khanate.txt:1>)|`cd79a8fcb8071796193d856abcd006424242418ac064fb7b6edbd0bb94decd15`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C03.3|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_native_khanate.txt:1>)|`e8d47b62f1d3da62dca7ee8c6eb0d107be507c1c2fbd7b388e5fccc260c0f332`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C03.4|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/on_actions/nesnd_native_khanate.txt:1>)|`6414ddcccbea216bb76eba9e7dcf714afecb0be1233ce33057553213426c1808`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C03.5|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/diplomatic_plays/nesnd_native_khanate.txt:1>)|`c7d2ca207b9d6d05c660335b489d38cd01f016152cef2c695ac93506c2905cd4`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C03.6|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_native_khanate.txt:1>)|`ebe7989d19ed7ea3c86819c3af418f2abb523be7c931054d4451035c22c9d05c`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C03.7|[nesnd_native_khanate.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/decisions/nesnd_native_khanate.txt:1>)|`f2df08e818a5b6873255e7c6b7307c9f2c4b1192a90c3361a068e941b14db6f4`|当前NKH草稿；其中A1法律辅助接口已冻结。|
|C04|[zzzz_nesnd_turtle_island.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/zzzz_nesnd_turtle_island.txt:1>)|`829b2252e483a7c6ea29aeb2670e557a44d3f58c0050c61633302327ee5e8cfd`|当前仅JE禁用；未覆盖3按钮effect。|
|C05a|[native_resettlement.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/events/native_resettlement.txt:1>)|`77a7790676f992a8fe93968864356e14434d987107069c4d91f11a2e09f6e0a3`|当前Cherokee七事件cancelled/inert旧窗口闭包。|
|C05b|[nesnd_hus_registration.txt:25](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_hus_registration.txt:25>)|`aaadcc5ee5fdfdc76857a548a04a29b2df994b027c260beaa72769749ce4844e`|je_indian_removal inert REPLACE；A1其它内容不动。|
|C06|[CE_religion.txt:8](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/religions/CE_religion.txt:8>)|`c3b9047fd53a424000b446eb12edcffea8b944adae7058af83ced1d6ab3594d0`|实际old_confucianism与kaimeng_confucianism定义。|
|C07a|[02_geographic_regions_america.txt:23](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/geographic_regions/02_geographic_regions_america.txt:23>)|`d8282bf1ee3fbaa80f9c57ef943f30b487d2a5f45b2978a393a7d3024a8b8216`|有效Americas geographic region覆盖。|
|C07b|[north_america_strategic_regions.txt:9](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/strategic_regions/north_america_strategic_regions.txt:9>)|`6e03d9f31e4bf4415117b1ce73285d5c0f0e094f70d699a0a1cb0ba0b4cecf4c`|有效Pacific含南北大原、大平原仍15region。|
|C07c|[05_north_america.txt:1660](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/map_data/state_regions/05_north_america.txt:1660>)|`89a2266ef80528abfffeb4a2a5aeb624e03a7de7a1d18d050fe1fda198b90483`|作者南北大原state_region，北美完整范围不可漏。|
|C08a|[05_north_america.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/pops/05_north_america.txt:1>)|`c813ff18df4e3010c6c5abbfe1d19b01f8508117ea2d7d0f18ee134b4ab13055`|已重配北美人口；只读冻结，不重跑人口工具。|
|C08b|[07_south_america.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/pops/07_south_america.txt:1>)|`7b0f372515fd50d93646650934349fea7a997cf3f73daa55d7f2e22ba895f502`|已重配南美人口；只读冻结。|
|C09|[ce_countries.txt:63](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/country_definitions/ce_countries.txt:63>)|`ce259abfdf584cad4b428a55014f7e09dd2ca7a24fc244446f9bd0a45c148781`|本候选国家定义数据库已有REPLACE实际用法。|
