# 65 唐衣大食：民族矛盾、教派、起义与经济线

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: claimed
Assignee: Claude
Blocked by: none（第①至⑤批全部交付，待作者统一复测，再集中修错）
Validation: STATIC_PASS（第①至⑤批及天命说补充：括号/BOM/引用/本地化键与 vic3-tiger 1.19.0 前后对比；第①批作者实机复测发现 2 处问题已修，第②至⑤批未实机验证）
Evidence: [方案](../../per-ethnic/spec.md)；模拟、检查与 Tiger `nesnd-workbench/reports/2026-11-07-per-ethnic-plan/`；第①批改前备份 `nesnd-workbench/backups/pre-change-per-ethnic-batch1-20261107T134331Z`

## 1. 现象与期望

作者：唐衣大食没有伊朗人起义推翻政权的内容，也没有任何民族矛盾的暗示，不符合设定。要求唐人中心等级制、矛盾激化主日志（约 1865 年爆发）、两阶段教派日志（含两派代表人物界面）、伊朗人起义与上台后的事件链、与矛盾挂钩的经济线，并改造现有日志。先交方案，确认后分五批实现。

## 2. 原因

- 作者原作没有 PER 日志；现有五条 PER 日志均为代理所写（`common/journal_entries/nesnd_per_campaign.txt`、`nesnd_per_governance.txt`），只有向东/向西与施政拨款，其中两条是空壳。
- 设定有明文：“贤王阿兹丹……通过商贸和技术进步缓和民族矛盾”（北明ppet 第 22 张）。

## 3. 改了什么

第①批（等级制、矛盾主日志、四按钮、风味事件、方针接入、冻结）：
- 新增 `scripted_triggers/nesnd_per_tension.txt`：唐人政权、三层人口、伊朗诸州、与伊斯兰国家交战、冻结（少于 3 州）。
- 新增等级制：`social_hierarchies/nesnd_per_tang_hierarchy.txt`、`social_classes/nesnd_per_tang_classes.txt`（3 层 × 上中下）、`law_groups/` 与 `laws/nesnd_per_tang_order.txt`（严分、成文、宽和）、`modifier_type_definitions/nesnd_per_social_class_modifiers.txt`。
- `ideologies/` 五个覆盖文件及 `ce_legacy_social_democrat.txt`：在东洲四等制立场旁插入唐律三档立场（68 处，严分随四等制，宽和随原住民编户，成文取中值）。
- 新增日志「波斯之忧」：`journal_entries/`、`scripted_progress_bars/`（29 项来源）、`scripted_buttons/`（4 个）、`static_modifiers/`、`script_values/`、`scripted_effects/`、`events/nesnd_per_tension.txt`（6 个）、`on_actions/nesnd_per_tension.txt`（开局设置）。
- `scripted_effects/nesnd_qin_persia_lifecycle.txt`：维护脉冲挂上等级制与新日志。
- `journal_entries/nesnd_per_campaign.txt`：「近西帝国的未来」换原版图标；两个方针提示补写对矛盾的影响（中英 `nesnd_button_tooltips`）。
- 中英本地化 `nesnd_per_tension_l_*.yml` 各 169 键。

第①批复测后修正（2026-11-07 作者实测截图与 error.log）：
- 开局法律为「唐律严分」而非「唐律成文」：法律组启用时引擎自动给首条法律。成文改排首位，并在开局（及 1836.3.1 前）强制设为成文。
- 「唐律成文」无利益集团支持、立法成功率为 0：唐衣大食执政利益集团的意识形态（家长制、忠君、军国、尚武、卫道、虔信）原无唐律立场；在 `ideologies/00_ig_ideologies.txt` 补上（只影响启用此法律组的唐衣大食）。
- `scripted_buttons/nesnd_per_tension.txt:46`：圣陵按钮给未设的变量加数报错，改为先判断。
- 开局重复添加「波斯之忧」的警告：维护脉冲不再添加，日志由 possible 自行激活；开局钩子只做等级制与法律设置。

第②批（三教消长、唐人同心）：
- 新增 `scripted_triggers/`、`script_values/`、`scripted_progress_bars/`、`scripted_effects/`、`scripted_buttons/`、`static_modifiers/`、`journal_entries/nesnd_per_faith.txt`，`character_templates/nesnd_per_faith_templates.txt`（10 位代表人物），`events/nesnd_per_faith.txt`（2 个团结度事件），`gui/journal_entry_widgets/nesnd_per_faith.gui`（三位代表人物肖像）。
- 「三教消长」：三条影响力份额条、改宗条、三个立国教按钮（20 年冷却，代价按影响力排名），开局国教定为逊尼；代表人物死亡或离国时按链条接续，链尽则生成同宗教的继任者。
- 「唐人同心」：唐人团结度（开局 60），高于 75 时诸族渐化为西域汉羌、西域汉羌渐入老秦；低于 40 时某州西域汉羌离散入伊朗诸族；伊朗系统治者时方向相反。
- 「波斯之忧」新增两行：国教（什叶 −0.06、逊尼 +0.02、佛教 +0.06）、唐人离心（团结度低于 60）；国教为什叶时与伊斯兰国家交战的矛盾减半。
- 中英本地化 `nesnd_per_faith_l_*.yml`。
- 作者复测：改宗进度条的说明写在条的 desc 里，会印在进度条上溢出。条上只留读数，说明移到「三教消长」的第二条状态行（同西秦团结度日志的两段 status_desc 写法）。
- 作者复测（第二轮）：①状态行写了“「国教不得人心」按2倍计”这类规则，违背 journal-text-contract“状态行写处境、不复述机制”。三条日志的状态行全部改为处境描述，倍数与阈值交给国家修正和进度条明细；改宗说明行改为改宗发生时的通知事件 `nesnd_per_faith.1`。开局即计算一次三教排名，修掉首月误显示“排在最后”（排名变量未算出时落入默认分支）。②三位代表人物穿明式朝服：EACR 给主体文化含华夏文化国家的全部政治人物套朝服。新增 `gfx/portraits/portrait_modifiers/nesnd_per_faith_clothes.txt`（仿本 MOD `EACR_hairstyles.txt` 的 INJECT 写法），对带 `nesnd_per_faith_rep` 变量的代表人物给原版素材：什叶、逊尼为阿拉伯式长袍加头巾，佛门为僧袍、不戴冠；权重 10 亿，约 97% 以上胜出（加权随机，非绝对）。
- 作者要求（第三轮）：佛门应居第二，逊尼、佛门影响力太小。乘数改为什叶 0.45、逊尼 0.7、佛门 4.5（`script_values/nesnd_per_faith.txt`），开局约 46/29/25，至 1900 年约 51/29/21（`nesnd-workbench/reports/2026-11-07-per-ethnic-plan/faith_mult.py`）。
- 「重启远西战争」加完成结局：拥有全部 18 个可宣称地区的整个地区即完成，设永久变量 `nesnd_per_west_realized`；资格条件排除已完成，防止维护脉冲把日志加回。作者选定方案一「唐衣哈里发国」：完成时触发事件 `nesnd_per.8`「三衣归一」；国号由作者 `ce_dynamic_country_names.txt` 的 REPLACE:PER 块中新增一条（优先级 100，高于「波斯将军府」75；条件为已完成且唐人执政）；新纹章 `coat_of_arms/nesnd_per_coa.txt` 的 `PER_tang_caliphate`（黑白绿横三色加金色秦鸟），在 `flag_definitions/00_flag_definitions.txt` 的 PER 块中以优先级 100 使用（低于法西斯旗 1500）。已按作者第四轮要求改为随执政文化 × 国教换名：唐人（逊尼「唐衣哈里发国」、什叶「唐衣伊玛目国」、其他「西唐」），波斯（「波斯哈里发国」「伊朗沙阿国」「伊朗帝国」），阿拉伯（「大食哈里发国」「大食伊玛目国」「阿拉伯帝国」）；旗帜按文化三面（黑白绿底，中央金秦鸟、狮与太阳、新月）；通知事件正文按文化与国教分四种。判定见 `scripted_triggers/nesnd_per_tension.txt` 的 `nesnd_per_west_ruler_*`。
- 作者第四轮：三教影响力改为“宗教乘数 + 唐人文化加成”：什叶 0.8、逊尼 0.7、佛门 0.6，唐人文化人口每人另加 4；开局约 70/14/16，至 1900 年约 75/11/15（`faith_culture.py`）。同一次人口遍历内计算。

第②批补充：天命说可替换佛门（spec 第十三节；改前备份 `nesnd-workbench/backups/pre-change-per-mandate-20261107T171845Z`）：
- 开局事件 `nesnd_per_faith.2`「西来的学说」：守佛门或迎天命说，写永久变量 `nesnd_per_third_chosen`（及 `nesnd_per_third_mandate`），不可再改；AI 九成守佛门、一成迎天命说。由 `nesnd_per_tang_setup` 在 1836.3.1 前触发一次；中途接手或到 1836.6.1 仍未作答的按佛门。
- 两版「三教消长」按变量二选一：原佛门版 `nesnd_per_faith_journal`，新增天命说版 `nesnd_per_faith_mandate_journal`（天命说份额条、传道条、立天命说为国教、设讲堂，肖像界面 `gui/journal_entry_widgets/nesnd_per_faith_mandate.gui`）。共用计算：第三教影响力另存 `nesnd_per_inf_third_v` 供排名，国教代价改为 `nesnd_per_faith_rank_penalty`，原改宗改为 `nesnd_per_faith_convert_to`（四教信众都算在内）。
- 天命说影响力 `nesnd_per_inf_mandate`：信众同佛门算法（0.6，唐人另加 4）；与西秦有往来时未定路线 +3、朝贡伊犁 +4，向东断交或与西秦交战为 0；讲堂每座 +0.6（最多 6 座，花费 GDP 1.5%，2 年冷却，断交时每年荒废一座）；国教 +6；代表人物 ×1.1。
- 传道条：唐人团结度 ≥ 60 且与西秦有往来时每月 +0.25，朝贡伊犁 +0.15，讲堂每座 +0.1，立为国教 +3；受阻的缘由以 0 值行列在明细里。满 100 时在唐人信众最多的州（唐人佛门 ×2）把唐人佛门、什叶、逊尼改 25%；立为国教后同州非唐人什叶、逊尼另改 30%。团结度高于 75 时入老秦者随之改奉天命说。
- 佛门信众保留，不进份额条，是传道最先改信的对象。
- 联动：「波斯之忧」国教一行加天命说 +0.10；「唐人同心」国教一行加天命说 +0.06；远西完成国号落入「西唐」。
- 代表人物：自创西秦经师韩守正（1781）、赵敬之（1803）、王明德（1826），老秦文化，链尽生成老秦继任者；服装不另设，用本 MOD EACR 的明式朝服。
- 模拟（`mandate_sim.py`、`mandate_final_results.txt`）：开局约 3%；放任（朝贡伊犁、不建讲堂）至 1900 年约 8%；积极建讲堂约 1865 年超过逊尼；1860 年立为国教约 1895 年前后居首，1870 年立则在 1900 年后。断交时为 0。
- 静态检查 `static_check_mandate.py` 通过；Tiger（`tiger-after-mandate.json`）对本任务文件只多出 Tiger 1.19 不认识的 1.15 字段。曾用两段 status_desc，Tiger 报重复且无先例，已改为传道条明细行。

第③批（伊朗人起义、改朝换代或分裂、波斯人统治阶段；作者 2026-11-07 指示：不做改前备份，各批连做，最后统一修错）：
- 「波斯之忧」满 100 → 起义结局（outcome）→ 事件 `nesnd_per_rising.1`「伊朗人起义」：
  - 迎一位沙阿（广义伊朗人 ≥ 50% 时可选；AI 在 ≥ 55% 且合法性 < 40 时选）：`nesnd_per_shah_takeover`。立恺加王子（在国内则立，否则新建波斯贵人），唐人继承人换为波斯继承人；唐人文化退出主体文化、补波斯；国教什叶；等级制回默认；「新朝初立」5 年（合法性 −20），武勋门阀不满、乌理玛满意；讲堂与天命说代表人物作废，矛盾条清零。
  - 平叛：`nesnd_per_split`。广义伊朗人过半的非首都州另立 IRN「伊朗」（种子州取人口最多者；没有则取任一非首都伊朗州；再没有则改为迎立沙阿）。广义伊朗人 ≥ 60% 或十年内两次用过激化按钮（`nesnd_per_provoke_mark`，唐人实边、整肃清议各记一笔）→ 内战（伊朗发起 `dp_nesnd_per_civil`，双方互以吞并为目标）；否则独立战争（PER 发起 `dp_nesnd_per_reconquest`）。伊朗开局：君主制、专制、乌理玛与地主执政，波斯君主，「举国同仇」5 年，12 步兵 3 炮兵与一位将领。平叛后十年内「波斯之忧」不重开。
  - 投向起义一方（仅玩家）：同平叛，`play_as` 伊朗。
- 波斯人统治阶段（作者定：按统治者文化，`nesnd_per_persian_stage`：主体文化不含唐人、君主属伊朗传承、首都在伊朗诸州）：
  - 「沙阿的新朝」：遣返东归（送往西秦）、流放远方、改籍留任（改波斯文化与什叶）每次至多三人，共用 3 个月冷却，可交替使用；优容旧贵一次了结并开「旧唐人心」。西秦不在时遣返不可用。无唐人人物或已优容即完成。
  - 「旧唐人心」：条开局 20，来源为旧贵怀念、唐人尚众、与西秦交战、团结度低（旧唐人重新抬头）或高（唐人渐化）、北伐雪耻；满 100 → `nesnd_per_rising.10`「旧唐密谋」（严办：西域汉羌 20% 激进，条降到 40；让步：合法性 −5 五年，条降到 50）；按钮「抚慰旧贵」（GDP 1%，2 年冷却，−15）；20 年后完成。
  - 「沙阿的道路」二选一：北伐雪耻（宣称西秦与本国接壤、人口最多的一州并发起外交博弈 `dp_nesnd_per_north`，5 年冷却可再发；夺得即完成：「北伐雪耻」10 年、波斯人忠诚 +10%、西秦团结度十年 −0.5）；西进两河（宣称胡齐斯坦、法尔斯、拉里斯坦、巴士拉、巴格达、摩苏尔中别国的州；乌理玛不满，除非国教什叶且对手有逊尼国家；六地全得即完成：「两河与海湾」10 年）。
  - 「三教消长」改朝换代后在同一 PER 继续（`nesnd_per_faith_regime`）；天命说的西秦往来、传道、讲堂与代表人物只在唐人执政时有。伊朗（IRN）不开这条日志。
- 西秦团结度新增一行「波斯北伐」（`nesnd_qe1_unity_persia_north`：与北伐中的波斯交战 −0.5；雪耻后十年 −0.5）。
- 国名与旗帜：IRN 按政体八种名称（大伊朗、伊朗人民共和国、伊朗国、伊朗伊玛目国、伊朗伊斯兰共和国、崇高伊朗国、伊朗沙阿国、伊朗共和国；默认「伊朗」），旗帜沿用原版波斯各政体旗。唐衣大食新旗 `PER_tang`（竖分：白底黑秦鸟、绿底金狮与太阳、中缝金线），唐人执政时优先级 50（远西变身 100、法西斯 1500 仍优先）。
- 新文件：`scripted_triggers/`、`script_values/`、`scripted_effects/`、`static_modifiers/`、`diplomatic_plays/nesnd_per_rising.txt`，`events/nesnd_per_rising.txt`，`journal_entries/`、`scripted_progress_bars/`、`scripted_buttons/nesnd_per_shah.txt`，`country_definitions/`、`dynamic_country_names/`、`flag_definitions/nesnd_per_irn.txt`，中英 `nesnd_per_rising_l_*.yml`（124 键）。改动：`nesnd_per_tension` 日志与按钮、`nesnd_per_faith` 触发器/日志/按钮/效果、`nesnd_qe1_identity` 条与脚本值、`coat_of_arms/nesnd_per_coa.txt`、`flag_definitions/00_flag_definitions.txt` 的 PER 块。
- 静态检查 `static_check_b3.py` 通过；Tiger（`tiger-after-b3.json`）对本任务文件只多出 Tiger 1.19 不认识的 1.15 字段（`outcome`、`activation_description`、`progress_condition`）。

第④批（经济线「大食的矿冶」）：
- 三个阶段日志依次开启，各限 20 年（期满无奖励，下一阶段照常开启）：
  - 一「矿产与木材」：开局；采矿建筑组 20 级、伐木场 15 级 →「矿冶初兴」10 年（采矿、伐木吞吐 +10%）。
  - 二「煤与钢」：第一阶段结束且研究炼钢、铁路；煤矿 20、铁矿 30、钢铁厂 10、铁路 20 →「伊斯法罕钢铁带」10 年。
  - 三「石油与汽车」：第二阶段结束且研究抽油机、内燃机；油井 30、汽车工业 10 →「海湾油田」10 年（石油开采、汽车吞吐与威望），并弹「大食的矿冶」告成事件。
  - 「波斯之忧」≥ 70 时完成只领减半版。
- 利权（唐人执政时每阶段选一次，阶段结束作废）：唐人专营（本阶段建造 +10%，矛盾每月 +0.05）或波斯商贾入股（矛盾 −0.05，武勋门阀不满 3 年）。
- 油田特许权（第三阶段，任何政权，二选一，10 年）：许给外国资本（立得 GDP 10%，石油开采吞吐 +15%，威望 −10，唐人执政时矛盾 +0.05）或自办（吞吐 −5%，矛盾 −0.03）。
- 「波斯之忧」≥ 60 时伊朗诸州有矿工罢工（`nesnd_per_mines.1`）与铁路、油井遭破坏（`.2`）：弹压（本州 10% 激进，矛盾 +0.04 三年）或安抚（花 GDP 1%，矛盾 −0.04 三年）。「波斯之忧」新增四行：矿工罢工、铁路与油井遭破坏、经济利权、油田特许权。
- 政权：唐人执政或波斯人统治阶段（`nesnd_per_mines_regime`）。改朝换代后同一 PER 接着走；分裂出的伊朗从第一阶段起按建筑判定，已建成的即刻完成。迎沙阿时唐人时代的利权作废。
- 「波斯人统治阶段」收紧为首都在伊朗高原（波斯、马赞德兰、卢尔、库尔德故土，`nesnd_per_plateau_state`）：开局的卡拉特、莫克兰（首都俾路支斯坦、君主俾路支人）原会被算进去，拿到「沙阿的道路」与经济线。
- 新文件：`scripted_triggers/`、`static_modifiers/`、`scripted_effects/`、`journal_entries/`、`scripted_buttons/nesnd_per_mines.txt`，`events/nesnd_per_mines.txt`，中英 `nesnd_per_mines_l_*.yml`（64 键）。改动：`scripted_progress_bars/nesnd_per_tension.txt`（四行）、`scripted_effects/nesnd_per_rising.txt`、`scripted_triggers/nesnd_per_rising.txt`。
- 静态检查 `static_check_b4.py` 通过；Tiger（`tiger-after-b4.json`）对全部 `nesnd_per_*` 文件除 1.15 新字段外无告警。曾用 `building_oil_rig_throughput_add`，Tiger 报不存在（1.15 只列为“潜在”修正），改用 `building_group_bg_oil_extraction_throughput_add`。
- 与方案的出入：方案写“主日志 30 年时限”，但第三阶段要内燃机（约 1880 年后），30 年内做不到；改为三个阶段日志各限 20 年、不设总日志。“使用汽车生产”的生产方式条件未做，只看汽车工业等级。

第⑤批（现有日志清理）：
- 删除「唐衣大食的经略」（施政余力条与四个拨款按钮，「扶植工商」已由经济线的利权取代）：删 `journal_entries/nesnd_per_governance.txt`、`scripted_buttons/nesnd_per_resources.txt`、`static_modifiers/nesnd_per_resources.txt`；`scripted_effects/`、`scripted_progress_bars/`、`script_values/nesnd_per_resources.txt` 只留宣称点；维护脉冲 `nesnd_qin_persia_lifecycle.txt` 不再挂它。
- 删除空壳「唐衣之下」「波斯的市镇」（`nesnd_per_civil_journal`、`nesnd_per_economy_journal`）及其按钮、修正（`nesnd_per_civil_order`、`nesnd_per_industry_order`）、触发器（`nesnd_per_civil_ready`、`nesnd_per_economy_ready`）。
- 中英 `nesnd_persia_l_*.yml` 各删 45 键（含早先合并方案留下、从未使用的五个地区宣称按钮名），`nesnd_journal_closures_l_*.yml` 各删 2 键。
- 宣称接入「波斯之忧」：37 个逐州按钮共用的 `nesnd_per_attempt_claim` 在宣称成功时调用 `nesnd_per_claim_tension`，向西一次 +2、向东一次 −1；按钮不合并（作者定）。「波斯之忧」新增一行「向外宣称」。
- 「近西帝国的未来」「重启远西战争」「近西战争重启」的说明补写与民族矛盾的关系（中英）。
- 李霄业注释不动（作者定）。
- 静态检查与 Tiger（`tiger-after-b5.json`）：PER 各文件除 1.15 新字段外无告警；删去的日志相关告警随之消失。

作者复测（2026-11-07，第⑤批后）：
- 文字：作者指出分号滥用、“的话／口子／底子／塌了”式口语八股、文学性不足。按 `nesnd-player-writing` 与作者样本重写任务65全部中文故事文字（136 键：日志说明、事件正文、引文、选项、按钮说明、状态行、结局），规则提示中的分号改为句号或逗号。选项改为人物表态，引文出处各不相同；意思有变的同步重写英文（`gen_prose_rewrite.py`）。作者亲改的两处（矿冶第一阶段说明、矿冶告成正文中的国名引用）保留。
- 代表人物宗教错误：原版教士集团 `ig_devout` 的 `on_character_ig_membership` 会把入会者改信国教，开局国教逊尼，四派代表人物因此全成了逊尼（天命说的韩守正也是），服装随之错用阿拉伯长袍。当时以生成后立即改回本派及每周复核暂作修复。
- 教士集团改名：三教并立时 PER 的 `ig_devout` 改称「三教宗师」（`ig_nesnd_per_clergy`，每月在三教计算时设定），不再随国教叫「什叶派乌理玛」；「波斯之忧」中该行与西进提示随之改称。
- 服装：佛门住持在宗教改对后即穿原版僧袍、不戴冠；天命说经师改用原版中式文人长衫（`chinese_outfits_agitator`）、不戴冠，不再依赖另行加载的 EACR 朝服（原注释误把 EACR 当作本 MOD 内容，已改）。

四派代表改入知识分子（2026-11-07）：

- `common/character_templates/nesnd_per_faith_templates.txt` 的 13 个具名模板，以及 `common/scripted_effects/nesnd_per_faith.txt` 四个 `nesnd_per_rep_fill_*` 的通用继任者，均指定 `ig_intelligentsia`。四派生成后仍立即执行 `change_character_religion`。原版知识分子的入会效果为空。
- 保留显式指定的 `ideology_traditionalist`。原版随机分配传统主义的集团条件未列知识分子，具名模板 `RUS_fyodor_dostoevsky` 和 `RUS_vladimir_solovyov` 则直接指定知识分子与传统主义（GAME `common/character_templates/country_rus.txt`）。
- `common/journal_entries/nesnd_per_faith.txt` 的 `nesnd_per_faith_journal`、`nesnd_per_faith_mandate_journal` 各在 `on_yearly_pulse` 对本路线三席调用 `nesnd_per_rep_keep_faith`。复用 `nesnd_per_rep_valid` 排除已故或离国人物，旧档现任代表若属其他集团，就在人物作用域执行 `set_interest_group = owner.ig:ig_intelligentsia`，再按席位校正宗教。两版日志仍每周调用 `nesnd_per_rep_fill_all` 补缺。
- 游戏外验证：定向解析通过，覆盖 13 个模板、4 个通用继任者、生成后设定宗教、两版周／年脉冲和迁移守卫。`static_check_b4.py` 的 BOM、括号与脚本引用检查通过。中英各有 6 个本地化误报，其中 4 个是带点事件描述键被截短后的前缀，另 2 个是国家变量 `nesnd_per_inf_total_v`、`nesnd_per_tang_share_v`。`run_tiger.py after` 与上次的 `tiger-after.json` 均为 2767 条，按主位置、诊断键、级别和消息计数无增减。三份脚本仅有日志原有的 1.15 字段告警。报告位于工作台 `reports/2026-11-07-per-ethnic-plan/`。待作者实机复测。

两版「三教消长」在故事正文下方增设中英规则框（`custom_widget_container_5`）。两版均说明改宗满条的选州与 5% 改信效果，以及每月影响力的计分与份额。天命说版另列传道的选州门槛、25%／30% 改信效果和天命说专属加成。已核对界面挂载、本地化引用和数值。Tiger 1.19 对两版各新增一条重复 `widget` 警告；原版 1.15 的 `je_meiji_restoration` 同样使用两个独立的 `widget`。

2026-11-07 19:48，开局事件「西来的学说」（`nesnd_per_faith.2`）弹出时，崩溃包最后一行记录引擎在 `gui/eventwindow.gui` 找不到 `nesnd_event_window_per_faith_teaching`。该名字仅在独立 GUI 文件里定义。事件现指定原版 `event_window`，移除空壳别名。按引擎实际路径检查，改前缺失、改后可解析；独立 DDS 插图与两个选项已核对。证据在工作台 `reports/2026-11-07-per-faith-crash-194808/`。待作者实机确认。

2026-11-07 19:54，日志开启效果反复报告代表人物继任序号未设置。四派 13 个候选分支现共用 `nesnd_per_rep_index_at_most`：序号存在才比较，未设置视为 0。已对照原脚本核过全部候选人的门槛、年份和继任序号写入，Tiger 对信仰文件无新增诊断。两版中文规则框改为按句换行，数字紧连单位，仅分组标题加粗。两版展开后的文本以 20 像素宋体估测，最长行均为 450 像素。证据见工作台 `reports/2026-11-07-per-faith-rep-index/`。

## 4. 怎么复测

第①批需新开局，用 PER（唐衣大食），1836.1.1：
1. 日志「波斯之忧」开局即有，条为 20；悬停列出全部来源（不满足的为空框）。
2. 法律「权力结构」中有「唐律分等」，开局为「唐律成文」；人口面板中波斯人归「伊朗人上/中/下层」，阿拉伯、阿塞拜疆人归「诸族」。
3. 国家修正中有「唐衣之治」（开局约 67%）。
4. 一个月后条约 +0.3；控制台 `event nesnd_per_tension.1` 至 `.6` 可直接看事件。
5. 四个按钮的代价、冷却与余波行；选「遣使伊犁」或「联络西秦诸部」后，「朝贡伊犁」或「脱离伊犁」一行生效。

第②批（同一新开局即可）：
6. 「三教消长」开局：国教为逊尼；什叶、逊尼、佛门三位代表人物肖像；三条份额约 78% / 20% / 2%；改宗条每月约 +1.6；状态行为“只排第二”，国家修正中有「国教不得人心」。
7. 立国教按钮的代价提示随排名变化；改立后 20 年冷却。
8. 「唐人同心」开局 60；控制台 `event nesnd_per_unity.1`、`.2` 可直接看两个事件（需先有满足条件的州，否则事件不触发）。

天命说（新开局，PER）：
9. 开局弹出「西来的学说」。选“唐人自有佛门”：同上第 6 条。
10. 另开一局选“请西秦经师来讲学”：「三教消长」换成天命说版，第三条为天命说影响力（约 3%），多出传道条、「以天命说为国教」「设讲堂」；第三位代表人物韩守正穿中式文人长衫。
11. 传道条悬停：明细列出各项来源，受阻时有“与伊犁断了往来”“唐人离心”“与西秦交战”的 0 值行。满 100 后弹改宗通知，呼罗珊或马赞德兰的唐人佛门部分改奉天命说。
12. 立天命说为国教后，「波斯之忧」国教一行为 +0.10，「唐人同心」国教一行为 +0.06。

第③批（可读档用控制台；唐人执政时旗帜应为竖分新旗）：
13. 把「波斯之忧」推满（控制台改变量或连用激化按钮）后，日志完成并弹「伊朗人起义」。广义伊朗人不足一半时没有“迎一位沙阿”。
14. 迎沙阿：君主换成恺加王子，国名回「波斯」，旗帜换回波斯旗，国教什叶；「沙阿的新朝」「沙阿的道路」出现，「三教消长」仍在（天命说一栏空）。
15. 平叛：伊朗诸州成为「伊朗」并立即开战（内战或收复战）；“投向起义一方”后改操控伊朗。
16. 「沙阿的新朝」四个按钮各试一次；优容后「旧唐人心」出现。
17. 北伐：西秦团结度多出「波斯北伐」一行。

第④批（新开局，PER）：
18. 开局有「大食的矿冶：矿产与木材」，两个利权按钮；选后「波斯之忧」多出「经济利权」一行，状态行写明谁在经营。
19. 控制台推高矛盾到 60 以上后，控制台 `event nesnd_per_mines.1`、`.2` 可直接看罢工与破坏事件。
20. 建满第一阶段的建筑后日志完成，得「矿冶初兴」；研究炼钢与铁路后第二阶段出现。

第⑤批：
21. 日志里不再有「唐衣大食的经略」；「重启远西战争」宣称一州后，「波斯之忧」下月多出「向外宣称」+2（向东为 −1）。

四派代表人物（两条路线分别复测）：

22. 读取已有「三教消长」现任代表的旧档，记下三人姓名。在读档后一年内、下一次年度脉冲过后，悬停日志中的三幅肖像。仍在任者应是原来的人，集团均为知识分子，宗教依次为什叶、逊尼，以及所选路线的大乘佛教或天命说。佛门住持应穿僧袍，天命说经师应穿中式文人长衫。
23. 新开局选定第三教后即可悬停核对三人所属集团和宗教。若有人去世或离国，下一次每周脉冲应补上继任者，继任者出现时即属知识分子并信本派。

24. 分别打开佛门版和天命说版「三教消长」，向下滚过故事正文。两版都应显示「改宗进度」「三教影响力」的说明，天命说版还应显示「传道进度」及讲堂、西秦往来的影响力加成。

25. 用唐衣大食重走触发「西来的学说」的开局。确认弹窗显示传道插图、可选佛门或天命说，选择后能打开对应的「三教消长」日志。

26. 选择第三教、展开「三教消长」，核对三位代表和故事下方的规则框。数字、百分号与单位应连读。经过周脉冲后查看本次时段的 error.log，核对不再新增继任序号（`nesnd_per_rep_*_idx`）未设置或无效比较的报错。

## 5. 遗留问题

- 第①批作者已确认：日志、进度条明细、按钮、法律面板与阶层修正显示正常。
- 第②批未实机：代表人物生成与肖像、份额条写入、改宗批次、立国教代价、团结度转换与事件。佛教三位住持为自创名（法照、圆通、智澄），待作者改定。
- 天命说补充未实机：开局事件、两版日志切换、传道、讲堂。三位西秦经师为自创名（韩守正、赵敬之、王明德），待作者改定。目标“1890 年有望居首”在模拟中略迟：1860 年立国教约 1895 年居首。
- 伊朗人上台后天命说代表人物与讲堂作废：第③批已做。
- 「伊朗系统治者时方向相反」按字面实现（高团结：西域汉羌入伊朗诸族；低团结：某州伊朗人转为西域汉羌），迎沙阿后触发，请确认语义。
- 第③批未实机：起义事件、改朝换代（换君主、去唐人主体文化）、建国与开战、四种处置、北伐博弈、新旗显示（竖分旗的纹样位置未见过实图）。遣返用 `transfer_character` 到西秦；内战与收复战用自定义外交博弈，仿本 MOD 西秦内战写法。
- 第③批的取舍：「唐人人口降为二层」未做（改朝后等级制回默认，已无层级）；西进不限穆斯林国家，凡持有六个石油地区的别国都被宣称；PER 若已拥有全部六地，西进不可选。
- 第三档改为「唐律宽和」（原版种姓第三档的写法：保留等级制、放宽封顶），不切回默认等级制。
- 方案曾称引擎自动生成阶层接受度修正，有误：须在 `modifier_type_definitions` 声明（东洲与原版均如此），已补。

- 作者已答复全部问题（spec 第十二节）：三教影响力取口径甲（保留人口，什叶开局领先）；李霄业注释为作者授意的正确设定，不恢复；国教开局定逊尼，在第②批实现。
- 后续批次：② 信仰日志（三教影响力、转化条、代表人物继任链）与西域汉羌团结度；③ 起义、改朝换代或分裂、伊朗国名与旗帜、波斯阶段日志；④ 经济线；⑤ 现有日志清理。
