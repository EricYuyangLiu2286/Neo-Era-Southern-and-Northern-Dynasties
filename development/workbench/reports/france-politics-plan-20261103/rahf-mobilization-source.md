# RAHF 日本政治动员源码研究：征韩论、人口支持与人物传播

日期：2026-11-03。状态：`SOURCE_RESEARCH / ENGINE_NOT_RUN`。本报告只读 RAHF 与本体源码，不启动游戏，不修改 MOD；不把工坊代码存在视为当前引擎有效性证明。已按 NESND 技能及工程适配使用 Matt research 的原始来源方法。当前 `catalog.py status` 返回 **1.13.11 / Steam build 24799966 / CURRENT / changed_count=0**。RAHF 本机 metadata 为 **10.9，supported_game_version 1.13.***。

## 核心结论

RAHF 的日本路线确有一套跨长期日志、地方社会事件与人物事件的政治传播结构。**征韩论是这条结构中的阶段转折**：其标记开启中日竞争，竞争胜利与帝国国策又接入后期军国化；尊攘事件直接改地方运动吸引，帝国日志定期改变人物思想，后期法律又影响扶植/打压效率。这个整体观察成立，不能只检查征韩论当次弹窗就否定它。[R1][R2][R4][R12–R15]

若细分接口，`open_japan.12` 本身的选项只在接收国写入 `battle_of_east_sun_var`，然后通知所有玩家国家。画面展示三名 IG 领袖，文案描写意见分歧，但该事件没有三个机械选项、人物改意识形态、政治运动创建或人口支持变更。三位人物在此节点是展示 scope，实际人群变化由前后其他节点承担。[R1]

真正值得法国借鉴的是它周边的分层结构：**现实条件→剧情进度；地方事件→人口运动吸引与激进派；人物事件→角色意识形态；IG/法律→后续剧情条件**。这些层可互相影响，却不是一个可以互换使用的“支持度”。尤其 `ig_radicalized` 实际是 IG 认可度 −3、政治力量 −15%，本地化为“失势”，并非政治运动 radicalism +3。[R2][R3]

对法国的建议是保留这套分层表达，同时以当前 GAME 原生政治运动承载人口支持和激进化；剧情条只记录王朝竞争、执政合法性或危机阶段。不能把征韩论的国家布尔标记换个名字后宣称“全国思想传播”。

## 1. 从士族冲突到征韩论：实际入口与退出

| 节点 | 条件、调度、scope 与结果 |
|---|---|
| `je_jap_xinan_war`，士族矛盾 | JAP 专属显示；`japan_emperor_restored` 后可启动。country scope 在 immediate 排入 `sino_event.38/.36/.114/.35`，延迟分别为 30/60/90/360 天。附着 `jap_xinan_war_bar`。[R2:1402–1437] |
| 士族矛盾成功 | 同时具有 `modifier_feidaoling`、`hu_ji_fa_modifier`、`modifier_fei_fan_zhi_xian` → `.104`。超时 3650 天也走 `.104`。失败条件是 bar ≥195 → `.103`。两出口不是同一政治立场。[R2:1459–1500] |
| `sino_event.104`，武士效忠 | 军队 IG 获 `ig_gaining_support`；国家获十年衰减修正；日本文化 soldiers 的 `add_loyalists value=0.25`；30 天后 `.12`。[R4:6972–7020] |
| `sino_event.103`，西南战争 | 以 JAP 的九州 owner-state 建 SMF；找现存/流亡西乡或新建模板，交给 SMF 当 ruler、IG leader、general；JAP 日本文化 soldiers `add_radicals=0.1`；创建真实 annex war，并添加 `je_annex_smf`。这段走脚本战争，不是凭人口支持自动爆发的原生革命。[R4:6855–6962] |
| `je_annex_smf` | SMF 不存在且和平→胜利收益，30 天后 `.12`；SMF 存在、双方停战、SMF 独立且 AI 且无战争/博弈→失败：地主入阁、365 天 forced_regime_change、`.254`，7 天后 `.12`。[R2:2266–2347] |
| `open_japan.12` | country event；trigger 只检查 KOR 存在，`duration=3`（月）；无本地 cooldown、无一次标记守卫、无 cancellation_trigger。保存知识分子/乡村民众/军队 IG 的当前 leader；唯一选项置国家标记并通知玩家。[R1:986–1048] |
| 后续 `je_japan_china_win` | 君主制、`japan_emperor_restored`、民族主义科技、非独裁，再满足 KOR 已不存在 / 全局拼作 `battel_of_east_sun_var` / `KJU_unite` / 国家 `battle_of_east_sun_var` 中一项。初始化 `china_japan_var=0` 并发 `.96`。达成朝鲜诸州、北海道、台湾与 goal 才成功；中国胜利修正可失败；中日不战全局标记可 invalid；三出口均清 `china_japan_var`。[R2:1806–1934] |

这条链未看到把 `.12` 的三个展示人物标为征韩论支持者的代码；也未看到因其死亡取消或逆转征韩论的代码。`battle_of_east_sun_var` 没有持续期限，不是百分比，更不是 POP 意识。入口大体由一次日志结算限制，但 `.12` 自身不抵抗重复调度；法国实现应有显式 campaign/阶段锁，而不是依赖“按历史大概只来一次”。

士族条 `jap_xinan_war_bar` 初始0、范围0–200，逐月按以下条件求和：全局 `fall_of_the_samurai_global_var` 且无 `samurai_officers` +1；AI或军队IG有 `revoked_sword_rights` +1；AI或自由贸易 +1；AI或非边缘地主认可<−8 +1；AI或非边缘军队认可<−8 +2；全国average_sol≥15 −2。这里SoL与IG情绪改变的是**剧情压力点/月**，并不直接写POP支持。首项源码有 `else` 后接 `else_if` 的异常结构，报告只记录字段意图，不把它认证为可运行公式。[R10:3598–3721]

全目录检索国家标记与近似拼写全局标记后，读写者完整如下（不能把两个拼写视为同一个变量）：

| 符号 | 全部直接读写者 | 含义 |
|---|---|---|
| 国家 `battle_of_east_sun_var` | `.12` 写；`historical_small_adjustment.txt` 的 `weixin` JE在443行检查、448行保底写；`.44` 在3039行读；`je_japan_china_win` 在1836行读 | 日本进入对外竞争的阶段状态；未找到remove/数值累计读写。 |
| 全局 `battel_of_east_sun_var` | `.96` immediate在6431行写；`.44`在3043行读；`je_japan_china_win`在1834行读 | 跨国启动中日竞争的全局状态，不是全国人口支持。 |

`weixin` 另一路专供 AI：显示条件含 `ra_buff_on`、JAP独立且无战争/博弈、1870.2.1–1910.1.1、已复辟；immediate给予500万金库、日本文化人口效忠化0.22、舰队、宗教IG变更，若未置征韩标记则补置。这说明AI与玩家会以不同路径进入同一后期阶段；不是每个AI日本都经历过征韩弹窗。[R12:348–454]

完整下游连接为：`battle_of_east_sun_var` → `je_japan_china_win` → `.96` → 添加 `je_chaoxian_jap / je_japan_china_tao / je_japan_china_tea`；`.96`也写全局标记，使中国`.44`开启其对应竞争日志。`.44`的直接日本条件还包括非独裁、与接收国关系低于amicable、复辟、独立，或由全局标记绕过；有国家 `battel_of_east_sun_china_var` 一次锁与1000年cooldown。[R4:3010–3076、6388–6474]

`.96`的十五年 `inheritance_kamikaze_modifiers_1` **实际增加教育机会0.1、科技扩散10%、威望25**，没有直接新增军国运动支持；教育可能通过识字影响后续政治参与，是可解释的间接通道，实际时间响应未实测。源文件长注释列了更多收益，报告以有效字段为准。[R13:3–8][G9]

竞争成功 `.99` 给 `japan_win3` 十年并置 `invade_china_now_var`；并行帝国日志的 `jap_be_empire_button` 耗50帝国进度，加 `je_great_japan`，该日志成功/AI放宽出口发 `.29`，置 `great_japan_var`、日本文化效忠化0.1，并施行帝国宪法（AI另施报刊等法律）。随后 `inheritance_kamikaze_1` 按钮要求君主制、`great_japan_var`、政治鼓动/军事统计、朝鲜诸州/北海道/台湾；玩家还需 `invade_china_now_var`，AI可绕过此项。按钮置一次 `invade_china_var`，发 `kamikaze.1`并添加 `je_japan_invade_china`，接入本报告第5节长期军国化条。[R4:1436–1498、6544–6612][R14:1–62、1410–1445]

`kamikaze.1`还把日本文化加 `coprosperity_circle`，朝鲜文化移除 `tradition_sinosphere`并加前者；这是**culture数据库特质层面的全局变更**，不是单个POP选择意识形态。法国政治路线不应因群众宣传而复制这种文化身份改写。该事件另改AI战略、关系、竞争与满洲宣称；外交阶段与思想传播需分别建模。[R15:1–78]

朝鲜事务 `je_chaoxian_jap` 的 monthly pool 是 `200=0，50=.106，50=.107，50=.108`；`.108` 是江华条约推进而非征韩论人口传播。其条件为 navy_size≥1、KOR 存在、无 `cooldown_1_year`；事件 cooldown=3600 月，名为“一年”的变量实际保存 **2 年**，另保存 `korean_things_var` 200 月。选择触发 KOR `.147`。权重 50 不是“每月50%”；各事件 trigger/cooldown 会改变合格池。[R2:1069–1126][R4:7228–7284]

## 2. 尊王攘夷：政治条件如何变成叙事推进

`je_jap_shougun` 按月抽事件；`open_japan.3` 需尚未复辟、无 `je_respect_king`，且 year>1853 或已非孤立主义，cooldown 500 年。它给军队 IG 移除 `ideology_bakufu`、加入 `ideology_anti_shogunate`，加五年愤怒修正，并置两年 `respect_king_var`。`je_respect_king` 的显示入口还接受强迫开市修正。[R1:201–274][R2:3–113]

`japan_sonnou_joui_bar` 为 **0–500 的剧情点数**，初始0，逐月求和：[R5:1–142]

| 因子 | 每月点数 |
|---|---:|
| AI，或地主被迫开市修正，或国家强迫开市变量 | +1.5 |
| 自由贸易且 AI 或持有与美/英/法/俄绑定的投资权条约 | +1.5 |
| 军队 IG 认可度 × −0.5 | 限于 −1 至 +5 |
| AI，或地主不在政府/不再强大 | +1 |
| AI，或任一内战进度 >0.5 | +1 |
| AI，或任一国内州 turmoil>0.3 | +1 |

该条不是自动统计支持该运动的人口。它读取 IG 情绪、动乱和战争，再投影成剧情速度。AI 在多个条件直接满足，不能把其节奏用于估算玩家体验。第二项源文件 `else` 的嵌套不规整，属于待验证源码形状，不能原样复制后视为有效。

JE 按月池 `200=0`，`.109/.110/.111` 各10，`open_japan.4–.8` 各15；有 `je_meiji_restoration` 且条≥490→`.112` 戊辰战争；3650天超时→`.113` 倒幕路线；复辟标记使其 invalid。活动期 `no_shougun_modifier` 将反对派认可度−1、意识形态不协调合法性惩罚×1.25、合法性来源激进派×1.5、该来源效忠派×0.75、地主力量×0.9。这些是真实政治环境修正，但也不是“尊王派人数”。[R2:147–214][R3:3888–3895]

## 3. 人口政治层：哪些是真的，哪些只是名字

| 入口/对象 | 源码结果及量纲 | 当前适用边界 |
|---|---|---|
| `open_japan.5` 樱田门外之变 | bar≥200、地主认可度<0且非边缘；一次近似200年cooldown。事件给关东/东北/九州的 state 加 `sonno_sentiment_boiling` 3650天；其 `state_pop_support_movement_liberal_mult=0.15` 是自由派运动支持吸引乘数+15%，另有 capitalist 力量字段。[R1:359–437][R3:3897–3901] | **实际人口运动接口**，不是新增15个百分点支持，也不是15%人口立即改宗。事件使用 `every_state`，没有明确 owner=root 的 limit；法国必须选择本国 owner-state，不能将所有该地区国家的州作为默认目标。 |
| `open_japan.7` 天狗党 | bar≥350；知识分子 IG 五年支持修正；关东 `sonno_sentiment_suppressed` 1095天，其自由派支持乘数−15%。[R1:521–584][R3:3911–3915] | 真正改变吸引方向；不会删除思想或立刻清零运动。 |
| `open_japan.6` 生野之变 | bar≥300，地主负认可且非边缘；镇压选项 bar+10，九州 soldiers `add_radicals=0.05`；另选项给当地五年 `satsuma_military`。[R1:439–518] | **作用域缺陷**：RAHF 在 state 内使用 country-only `add_radicals`。当前引擎对应州接口是 `add_radicals_in_state`；这段意图可学，代码不能照搬。[G1:367–395] |
| `open_japan.8` 禁门之变 | bar≥450；bar+10，地主认可/力量+3/+15%，知识分子−3/−15%；关西劳工+0.1、长州士兵+0.15激进派的写法。[R1:587–667] | 保存的是 `s:STATE_*` 即 state_region，却直接施加 state/country 效果；当前 API 作用域不匹配。不能宣称该人口效果已生效。 |
| `satsuma_military` | `state_radicals_from_political_movements_mult=1`，政治运动来源激进派增量+100%；另移民吸引−100%、建筑吞吐−30%、税收浪费+0.3。[R3:3903–3909] | 源码注释误说“生活水平所影响的激进派”；实际键明确是政治运动来源，不是直接把所有士兵变成激进派。 |
| `.103` / `.104` | country scope，筛 Japanese+soldiers，分别激进化0.1 / 效忠化0.25。[R4:6942–6946、7009–7013] | 与当前 country 接口同层；量纲是选定 POP 向激进/效忠方向移动的比例，不是运动 radicalism、支持率或全国份额。[G1:367–395] |

“意识”应落实为：人口所属运动及其 attraction、pop radical/loyalist fraction、IG membership/政治力量、literacy、实际运动 activism。检索这条日本链未发现独立的 POP `consciousness` 变量或征韩论 movement 数据库条目。`political_movement_pop_support/` 的条目只是 UI 因子列表；原版文档明说 `pop_support_factors` 本身没有玩法作用，真正计算在 movement 的 `pop_support_weight`。[G2:63–81]

## 4. 人物思想传播、退场与死亡

`je_jap_empire` 按月池包含 `.31`（开明保皇）、`.32`（军国主义）、`.33`（大正浪漫），各权重15，另有100空事件及其他事件；不能当作各15%概率。[R2:633–648]

`.32` 为 country event，duration3月、cooldown120月，trigger空。immediate 从本国 `random_scope_character` 抽一人：尚非 `ideology_meiji`、politician、age>18、不忙、非历史人物、非本国 ruler、所在 IG 非边缘。选择A直接 `set_ideology=ideology_meiji`；B添加 `modifier_devout_in_scandal`。这是**单人改派**，不是每期把其 POP 支持者全部改派。`.31`类似；`.33`还要求 ruler 模板为大正，接受后同时给工业家 IG 添加 `ideology_dazheng_jituan`。[R4:1574–1749]

`ideology_meiji` 是 `character_ideology=yes` 的真实人物意识形态，拥有法律偏好。自然生成条件要求日本为主流文化、`meiji_var`、君主制；可用于工业家、小市民、知识分子、军队、工会、地主六类IG。非领袖排除 agitator。领袖基础weight100，meiji标记+20，再君主制×2，拥有台湾另+75；这是**相对生成权重**，不是确定比例。事件直接 set 的路径与自然生成权重是不同入口。[R6:2–129][R7:21–29]

当前 GAME `movement_fascist.character_ideologies` 和 `character_support_trigger` 接纳 fascist/integralist/corporatist（后者还接 ethno_nationalist），**没有 `ideology_meiji`**。RAHF 在这条日本链也没有接上一个独立军国主义运动定义。所以 `.32` 转军国主义足以影响人物/IG法律态度及自定义bar，不能未经另证宣称它会自动领导原生法西斯运动。[G3:3648–3730]

人物生命周期有几处必须改进的地方：

- `.31/.32` trigger 不先要求至少一个合格候选，immediate 可能抽不到 `gaixi`；选项没有存在、存活、仍在本国、仍满足资格的复核，也没有取消条件。法国不应照搬。人物死于弹窗期间、流亡、转国、成为统治者，都应失效/重新选择而非操作旧scope。
- `.12` 只拿当时 IG leader 展示；后来的领袖死亡不会回退国家征韩论flag。图像对象与制度状态必须分开。
- 西乡模板 `agitator_saigo_takamori` 实际 IG=地主、ideology_mitogaku，commander_usage 为1854.1.1–1877.9.24、chance99，并检查全局 `dsk_saigo_takamori_happen`；名字含 agitator 不代表创建后自动拥有 agitator role。[R8:5130–5165]
- 倒幕完成、`.103`、`.113`、`.254` 都有“找各国现存→找流亡池→否则创建模板”路径；部分新建路径设 career_length 50年×1–1.5随机范围。没有在这些选人limit写 `is_alive`，也没有将人物死亡设为该政治运动的专门退出条件。若政治象征死亡，应保留组织支持但移除该人的声望贡献，再由继承/新领袖事件接续，而不是自动重建同一历史人。[R2:296–348][R4:6878–6931、7574–7628][R9:23390–23477]
- 樱田门事件“领袖遇害”在该 `.5` 选项实际只加 `ig_power_challenged`；未出现 `kill_character`。史事文字并不能替代人物生命周期代码。[R1:393–437]

## 5. 后期军国化条：条件反馈，不是人口占比

`je_japan_invade_china` 使用 `je_japan_fascist_bar`，初始700、范围0–2000、按月推进。[R10:3040–3198]

| 月度因子 | 点数 |
|---|---:|
| 基础准军事暴力 | +0.5；秘密警察/禁止异议/RAHF诽谤法之一则×1.8=+0.9 |
| 政府领袖意识形态 | 默认+0.1；执政IG有meiji/fascist/ethno-nationalist领袖→×20=+2；否则有communist/vanguardist/anarchist领袖→×−20=−2 |
| 公民权法律 | 默认+0.1；ethnostate/national_supremacy→+1.5；racial_segregation/cultural_exclusion/multicultural→−2 |
| 军队 IG 在政府且认可>12 | +2 |
| 恶名 | infamy×0.02，上限+2 |
| 任意州有暴力镇压 decree | +0.5（源码写 `any_state`，并非明确本国scope） |
| 本国或属国控制南满/北满/盛京全地区 | +5 |
| 裁军修正 | 默认−0.1；有 `modifier_caijun_button`→−1.5 |

该源码同时存在极右与社会主义执政IG时按首个if取极右分支，不是两项抵消。条≥1500后可抽 `.42`：一次近似500年cooldown，条+200、全国laborers激进化0.2、保守IG修正；流放特定左翼人物并给殉道者效果；有 cruel/bandit/grifter/pillager trait 的本国人物直接改 meiji。条≥2000且有强大IG由meiji/fascist领导（AI可绕过领袖要求）且CHI独立，才发 `.39`；CHI不存在则invalid。[R2:679–782][R4:2846–2924]

后期报刊/压制确实接到原生运动机制：`.29`给AI施行的 `law_IJ_newspaper` 包含 `country_bolster_attraction_factor=0.3`、`country_suppression_attraction_factor=-0.5`、知识分子力量−5%；`law_IJ_defamation`则有扶植0.8/打压−0.8、禁止邀请鼓动者、知识分子力量−25%、因立法反对产生的运动激进化倍率−10%。这些是国家制度改变运动吸引/人物入口的通道；不是单纯背景文案，也不是由征韩flag直接循环给人口加分。[R16:1113–1177] 当前GAME同类运动的`pop_support_weight`确实读取bolster/suppression attraction factor，Bonapartist实例见[G10:785–820]。

有用的是**执政联盟、社会压制和对外扩张共同反馈**；不宜照搬的是把人物负面trait、外战、法律强行合成单一必然极右道路，更不能照搬日本历史阶段到法国。

## 6. 当前 GAME 可用的原生链与量纲

本机原版有一个更适合法国自由化/压制设计的完整实例：`je_devorismo.on_monthly_pulse` → `devorismo.3` → 找最激进的自由/社会主义政治运动 → 加运动修正。[G4][G5][G6]

事件要求知识分子和工会人物各至少一个、执政IG支持审查、至少一个自由/社会主义运动；duration期间原版临时设两个展示人物immortal，after恢复（这是实例，不建议把普遍免死当必要方案）。压制选项给目标运动 `political_movement_pop_attraction_mult=-0.10` 与 `political_movement_radicalism_add=0.10`，同时全国 academics `add_radicals=large_radicals=0.1`；容忍选项给同类运动 attraction+0.10，同时使支持审查的执政IG认可−3。修正 `normal_modifier_time=1825` 天。这里清楚地允许**支持面缩小但残余支持者更激进**，而非一个刻度同时表示支持和愤怒。[G5:282–416][G6:146–159][G7:4、40]

当前原版接口/数据含义：

| 接口 | scope / 单位 / 限制 |
|---|---|
| `add_radicals` | country；按选定POP比例向激进化移动，可筛职业/阶层（互斥）、IG成员、文化、宗教。[G1] |
| `add_radicals_in_state` | state；同上；不是 `state_region`。[G1] |
| `create_political_movement={ movement_type=... }` | country；可选culture/religion；创建运动不等于强制人口加入。[G1:996] |
| `set_ideology` | character→ideology；直接改角色，不改全体人口。[G1:36947] |
| `state_pop_support_movement_liberal_mult` | 原生定义 percent=yes；可通过本国state上的限时修正做地方差别。[G8:169–175] |
| `political_movement_pop_attraction_mult` | 运动scope上调整吸引倍率；与实际支持比例不同。[G5][G6] |
| `political_movement_radicalism_add` | 运动激进化/activism加值，以0–1比例单位表达；0.10不是+10人口支持百分点。[G6][G9] |
| `pop_support_weight` | pop scope，与其他合格运动比较的吸引权重；UI的`pop_support_factors`不参与计算。[G2] |

原生反馈的当前常量在 `00_defines.txt`：[G9]

- 每次POP更新每个运动最多改变0.1份额（另有最低10人）；这是**每次更新上限**，不能擅自解读为每周10%。运动吸引×0.01形成支持份额上限。
- 创建默认需 calculated support≥0.025；维持默认actual support≥0.01；新建12个月不因低支持解散；创建失败365天内不重试同一个运动。
- 总运动support由人口34%、军事33%、财富33%加权，不能当作纯人口比例。
- 运动radicalism每周向目标移动0.01；≥0.5后每月将支持者0.005–0.025比例向激进化移动。支持者的激进/效忠又以+1.0/−0.75系数反馈到目标。
- 运动对IG施压影响人物意识形态生成；100%压力给对应权重+1000。另有已存在人物的prominence和role权重影响下一位IG领袖。故角色死亡后不是所有组织支持归零。
- agitator 的运动吸引按识字与同IG成员比例加权（权重各0.75），基础15并受popularity×0.15影响；这是可用的人物→群众通道，区别于直接给政治家set_ideology。[G9:1864–1867]

当前法国已有 `movement_bonapartist / movement_orleanist / movement_legitimist`，以及对应 `state_pop_support_movement_*_add/mult` 定义。Bonapartist 创建限制FRA或其内战来源，受王党消灭/其他王朝定于一尊变量阻断，disband也检查这些条件；角色支持、人口职业权重、识字倍率、原生革命门槛各自独立。军官+25、士兵+15、农民+10是**吸引权重项**，不是这些阶层支持百分比；底数还要叠5及识字×(literacy+0.1)。[G10:675–937][G8:387–434]

## 7. 三种可移植的法国结构（设计建议，未实施）

| 法国路线 | 可学的结构 | 原生承载、分支与退出 |
|---|---|---|
| 波拿巴：声望、军队与群众授权 | 学 RAHF“人物事件+现实条件反馈”，让外交成败、军人待遇、地方巡行/公开讲话影响不同对象；将战争目标换为法国世界线的争议，不采用征韩时间表。 | 原生 `movement_bonapartist` 承载群众；prominence/popularity与IG clout承载精英；国家剧情条只记录复辟/总统权力/帝制合法化阶段。胜利不自动让全部人口支持帝制，失败也可出现拥护者更激进。领导人死亡移除个人贡献并走继承/组织接班；不复活历史模板。 |
| 王党：巴黎与外省 | 学地方 `sonno_sentiment_boiling/suppressed` 的有限期地域修正，按**当前法国所有的state**分别描绘巴黎议会/报刊、外省教会/地方名望网络。 | 使用 legitimist/orleanist 两类原生运动支持，而非全国一个王党数字。各州按实际职业/识字/经济结构参与吸引；巴黎事件不能自动改所有外省。剧情条统计王朝协调或宪章争议，政策可短期压低吸引却激怒当地支持者；失去州、政体转换、和解、条款终止时清本案修正。地理差异是候选设计，实施前仍须读NESND法国人口与作者设定。 |
| 共和国：自由化与社会压制 | 学原版 devorismo 完整链及RAHF地方冲突事件：开放报刊/集会、社团合法化、救济、镇压分别影响吸引、activism、职业激进派与执政IG认可。 | 自由派/激进派/劳工等原生运动并存；“准许组织”可扩大支持面并缓和目标radicalism，“关社团”可削弱吸引却提高残余activism。不要用共和布尔flag代表人民已经共和化，也不要必然滑向帝制。选项触发前保证运动/人物存在，执行时重验；运动自然消散后换成无对象安全退出，剧情结束保留人口真实政治后果。 |

三结构共用的实施合同：campaign ID与一次提交锁；角色保存身份、owner、alive独立检查；pending事件取消与旧档恢复；政治路线结束清剧情modifier但不无依据重置POP；国家灭亡/分裂/附庸、人物死亡、失去目标州、运动消失均有出口。每月/每周条的量纲明确，限时修正设同名不可刷叠与冷却。初版只给已验证类型与scope，不设计“直接增加全国共和意识20”这类没有接口的效果。

## 8. 可复查来源索引

以下均为本机原始源码；行号绑定本报告读取时内容，升级后重查。RAHF日本链调用调度来自JE pulse/完成事件，未查到单独征韩论 on_action 传播回调。没有打开游戏，也没有声明人口效果实际运行通过。

- **R1**：[RAHF open_japan_events.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/open_japan_events.txt:986>)，完整读 `.3–.8`、`.12`。
- **R2**：[RAHF dsk_je_jap.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/dsk_je_jap.txt:98>)，尊王、帝国、士族、征韩后续及退出。
- **R3**：[RAHF dsk_usa_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/dsk_usa_modifiers.txt:3888>)，3888–3927。
- **R4**：[RAHF sino_events.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/sino_events.txt:1625>)，人物传播、士族与军事政变。
- **R5**：[RAHF jiawu_war_progress_bars.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/scripted_progress_bars/jiawu_war_progress_bars.txt:1>)。
- **R6**：[RAHF dsk_ideologies_leaders.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/ideologies/dsk_ideologies_leaders.txt:2>)。
- **R7**：[RAHF dsk_ideology_triggers.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/scripted_triggers/dsk_ideology_triggers.txt:21>)。
- **R8**：[RAHF 西乡模板](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/character_templates/replace_historical_leaders_europe.txt:5130>)。
- **R9**：[RAHF clever_dsk_events.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/clever_dsk_events.txt:23390>)。
- **R10**：[RAHF dsk_progress_bars.txt](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/scripted_progress_bars/dsk_progress_bars.txt:3040>)，法西斯条3040–3198；士族条3598–3721。
- **R11**：[RAHF 征韩与人物本地化](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/localization/simp_chinese/DSK main events/DSK_sino_events_l_simp_chinese.yml:1369>)；“失势”等修正本地化见同目录 `DSK_CHI_and_JAP_l_simp_chinese.yml:694–697`。
- **R12**：[RAHF AI维新保底](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/journal_entries/historical_small_adjustment.txt:348>)。
- **R13**：[RAHF 神风修正实际字段](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/static_modifiers/inheritance_kamikaze_mod.txt:3>)。
- **R14**：[RAHF 国策按钮入口](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/scripted_buttons/dsk_jap_scripted_buttons.txt:1>)。
- **R15**：[RAHF kamikaze.1](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/events/inheritance_kamikaze_eve.txt:1>)。
- **R16**：[RAHF 报刊与诽谤法律](<D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455/common/laws/kamikaze_laws.txt:1113>)。
- **G1**：[1.13.11 effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:367>)。
- **G2**：[GAME political_movements.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md:1>)。
- **G3**：[GAME ideological movements](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt:3648>)；法西斯人口权重含职业、SoL、失业、识字、接受度、激进派比例：3750–4096。
- **G4**：[GAME 葡萄牙JE调度](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/06_portugal_politics.txt:1>)。
- **G5**：[GAME devorismo.3](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/ip4_portuguese_political_events.txt:268>)。
- **G6**：[GAME 政治运动修正](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip4_04_modifiers.txt:146>)。
- **G7**：[GAME event_values](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/event_values.txt:4>)。
- **G8**：[GAME movement modifier types](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/08_movement_modifier_types.txt:169>)。
- **G9**：[GAME defines](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt:75>)；agitator参数1864–1867。
- **G10**：[GAME 法国政治运动](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/04_country_specific_ideological_movements.txt:675>)。
- **G11**：[GAME 殉道流亡效果](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_scripted_effects.txt:2031>)，角色修正/短期流亡池保护→exile→角色清理；2031–2111。

技能维护复核：本报告发现的是只读参考MOD中的作用域/生命周期风险，现有NESND技能已经规定对应边界，本轮不修改技能。

同名/覆盖复核：在当前RAHF所有`.txt/.yml`中搜索，`.12`、`.32`、`je_respect_king`只找到各一个有效定义；未找到RAHF覆盖原生`movement_fascist`或自定义同名`add_radicals`效果来修正前述scope问题。中文`.12`标题在`DSK_sino_events_l_simp_chinese.yml:1369`，英文同键在`localization/english/open_japan_l_english.yml:1295`；中文`.108`及指南也称“征韩论”，但它们是江华条约事件与整条路线说明，不能按标题混成一个事件。此报告针对本机10.9，不代表其他工坊历史版本。


## 来源文件 SHA-256

用于区分工坊/本体更新，不包含运行认证。

| 来源 | SHA-256 |
|---|---|
| R1 | `0dc7b4cbd2a576dabdcb7472a52441ad820f36a4d0cfbefba21da8ea5d54b455` |
| R2 | `21b6d1e939a8713562ba3365ab5de6d68e5c5b7a55d6a1dbd5580cc9e61196ac` |
| R3 | `b564ea3dfcfa7a880bf2f4ede9768a14db79ebb7079effb953088954b990fe4c` |
| R4 | `b7e986c567428e35a4a05cb109d1ce9b0902f66b9f295151a1d58b6201263798` |
| R5 | `7321a15626803044a6b1b4d133f1014c8e6dd0a2214595b922d789e5b426cf7b` |
| R6 | `317d5fbef694da8f62d360106b6ca80e9ddc3f02188171f8909d8eb3be3a8509` |
| R7 | `c6bf84db2080ae21413097ca2a9b723e814178df76ce4f307ba2cc52e96ee18f` |
| R8 | `3eb13c628814b8b57f78b43da03a4a18decf43ece60145ed34dff0ffd60660f5` |
| R9 | `de09b7be3d38e2fa6972ec6dc9361959ad95b8576a5959f7408691e2756fbbcb` |
| R10 | `c4bf6a0d037a23ff549966404a177dbc69b7732160b58353c34a9fd0b8b952a1` |
| R11 | `81ea17d8cdf7eb5362b5a15d9393732ebeaa3a9fdec35717dae9077d85a62f7b` |
| R12 | `4375458853c69aa5a074390ae086e650e6c3af5f6e43ccb065d8a2bac7d66e8a` |
| R13 | `ad0d4f302759a43f137a4c7ee7a202848bcff7033f4d68093f5e3f9855678e12` |
| R14 | `9c6792af7e678c52b9cc743b96ca1ed16a6c9eff20143a48ed3023fb73913db7` |
| R15 | `39b7de2f90d7f0bc319c39de7622af009089aaab21910e24461d5a3f9ab02a0c` |
| R16 | `c59a61850fc6ddfd497d1bb6ee9d29ac885ed818c3b2a879d2dfe72920b70ca3` |
| G1 | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |
| G2 | `4842b165656f0741cc0baad97b2d82836f9097f64ce5b43ca4559c9d733e22c6` |
| G3 | `834a1b97f09c65b9b64eafdaffe4ee68965aaac262066140793a482eefd23a6b` |
| G4 | `c72620de8c07b2553ce0ea3421450cc91c03f4c2d992cd70d544ee3cd2206acb` |
| G5 | `9c54cca4c47d77eeb80cf68e44c175feac6b639e475e800bbc8cbb463fab549b` |
| G6 | `a514e1fa61aa2178182506c90eb138f4bea53ad341fc20f9dbc1b6dbc5a7bf5c` |
| G7 | `2bde5cecb435cf0e41ed83987e7acd72adb41578ebc39df5970f176a39469581` |
| G8 | `a1b9e3384835d48ff52f612bb186c855eeb4f7744b9eae172ce17c413cf1e11d` |
| G9 | `e47db10931a2149c80aadab0b8de8f3fa000fdbb82a2f878fee893aa4434dd39` |
| G10 | `503590cec446a8016e09f65b491e7d529af97fadd76ee98c32d85d7c9baaafc6` |
| G11 | `b173953ebbfc0edacdddedb8130c3df0f41282d10f8e7ceeaa054ab8ade0b42d` |
