# 西秦身份转换与崩解：当前原版接口和地区配对

日期：2026-11-02。只读研究；未改 MOD、技能，未开游戏。NESND source-first 与 Matt research 的原始来源方法；本代理已经是父任务委派的研究子任务，按明确指令没有继续派生代理。

GAME=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`；MAIN=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`；WORK=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`；DOC=`WORK/references/engine-docs-1.13.11-20261031`。以下相对路径显式给出所属根。核验基线为本机 1.13.11 / Steam build 24799966；此前本会话 catalog status 为 CURRENT、0 变化。所有结论是源码与文档支持，`ENGINE_NOT_RUN`。

可机读配对和国家资料：[native-identity-map.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/qin-persia-20261102/native-identity-map.json>)；可重跑提取：[build-native-identity-map.py](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/qin-persia-20261102/build-native-identity-map.py>)。输出 **36 个当前 QE1 地区、174 个原版文化—宗教配对、18 个国家候选**，保存逐 create_pop 来源行、默认宗教来源、地理交集、输入 SHA。不是运行存档人口。

## 1. 用户边界与实现顺序

文化统一初值 **70** 是独立玩法指标，不能拿现行三主文化人口占比65.46%替换，也不能每次进入日志或读档再设70。大于75时的转换只改文化为 ce_xiyu，宗教保持原值；小于50时每月20%概率选择有资格的本国州，把该州50%的 ce_xiyu 转为一个按原版地理权重抽取的文化—宗教配对；小于25时启用动荡条，100时崩解、保留伊犁核心并产生新战争。

严格边界是 `>75`、`<50`、`<25`，75/50/25本身不落入相应严格区间。低于25同时满足低于50；是否同时允许身份复归和动荡累计应按用户所述双机制处理，不应误写成互斥 else_if 导致一条失效。每月先锁定本轮统一值再评估分支，避免一次转换改变指标后当月又走反向转换。

概率的原生接口是 `random = { chance = 20 ... }`，其 chance 为0–100；DOC `effects.log:26796`–`:26803`。概率20和人口比例0.5的单位不同。`random_events` 中的20权重不能自动解释为20%概率。

## 2. 人口接口、scope 与比例

|目的|当前接口与 scope|直接来源|
|---|---|---|
|改变一部分 pop 的文化|pop scope：`change_pop_culture = { target = cu:... value = 0.5 }`|DOC `effects.log:646`–`:649`；GAME `events/brazil/culture_south_america.txt:382`–`:391` 在首都逐 pop 转0.75；`common/diplomatic_actions/53_subjects_change_culture.txt:139`–`:149` 选择官僚 pop 转0.05|
|改变一部分 pop 的宗教|pop scope：`change_pop_religion = { target = rel:... value = 0.5 }`|DOC `effects.log:651`–`:654`；GAME `events/japan_events/japan_religion_events.txt:139`–`:147`、`:161`–`:169`；`common/script_values/event_values.txt:302` 给转换比例0.20|
|当前国家/州的人口集合|`every_scope_pop` / `random_scope_pop`，country/state/culture/IG 输入，返回 pop|DOC `effects.log:4762`–`:4766`、`:30852`–`:30856`|
|当前国家的州集合|`random_scope_state`，在国家输入下返回其州|DOC `effects.log:30870`–`:30874`；`random_state` 是全球，不用于此处|
|中华文化圈判断|pop → `culture` → `has_discrimination_trait = tradition_sinosphere`|DOC `event_targets.log:1790`–`:1793`；`triggers.log:10277`–`:10281`；GAME `common/scripted_triggers/00_clothes_triggers.txt:1237`、`:1254` 使用同 trait|
|保存与取回事件上下文|`save_scope_as` 沿未中断事件链；`save_temporary_scope_as` 仅当前 effect|DOC `effects.log:36744`–`:36757`；保存不保证对象分裂/合并后仍指向预想的人口部分|
|州/人口国家归属|pop `.state`、pop/state `.owner`|DOC `event_targets.log:330`–`:333`、`:451`–`:454`|

高统一转换的直接原生做法是对当前本国的非中华文化圈 pop 调用**仅文化转换**。不调用 `change_pop_religion`、`convert_population` 或 `set_state_religion`。ce_xiyu 数据库的 `religion = mahayana` 是默认定义，不能据此假设修改文化的 effect 会自动把现存 pop 的宗教也改成大乘；该 effect 的正式契约只说改文化。宗教保持不变仍需在实际候选人口快照中核验。

### 两次50%不等于同一半人口

不能写成在同一个保存的原 pop 上先 `change_pop_culture value=0.5`，再 `change_pop_religion value=0.5` 并声称“同一半人完成配对转换”。文档未承诺第一个 effect 之后原 scope 指向原剩余部分、转换后的部分还是合并目标；也未提供转换后人口的返回 scope。即使原 scope 保留，第二次0.5仍可能以剩余人口为分母。全 GAME 检索到的文化、宗教转换实例都是各自单维转换，没有找到能证明两次部分转换配对的原生实例。

同理，把原 pop 保存进列表后改完文化再遍历列表改宗教，并没有解决“保存对象是谁”的问题。人口的迁移、职业变化与合并也不适合作永久谱系指针。`move_partial_pop` 虽能分一部分人，但文档明确会成为失业人口且可能换 pop_type（DOC `effects.log:9829`–`:9838`），不适合为身份机制临时迁移人口。

## 3. 同一批人口配对：三阶段临时文化方案

父任务已接受采用如下组合。它由现有原生 primitive 组成，**不是查到了完整原版同形流程，也不是引擎已验证**。

1. 选中当前属于 QE1、存在 ce_xiyu、且有原版配对表的一个 state。保存该**州**和本次目标 culture/religion；不要跨月保存 pop。使用相同资格谓词检查可选与实际选择。
2. 在该州对所有 ce_xiyu pop 执行 `change_pop_culture`，target为唯一临时文化、value=0.5。此阶段仅将待转换的半数人口隔离出来，原来的另一半 ce_xiyu 与其宗教不动。
3. **重新枚举**该州所有临时文化 pop，对它们 `change_pop_religion target=抽中的宗教 value=1`。
4. **再次重新枚举**临时文化 pop，对它们 `change_pop_culture target=抽中的文化 value=1`。不再读取第一阶段的原 pop scope。

上述三次身份变更在一个同步 effect/事件 immediate 中完成，中间不弹选项、不安排延迟事件、不转属州、不创建国家。以临时文化作为集合标记，即使某一步分裂/合并了 pop，下一步重新枚举仍按实际文化找到待处理集合；两个后续变更为全量，避免二次减半。

临时文化应使用独立项目键，按 MAIN `common/cultures/CE_cultures.txt:1314` 起的 ce_xiyu **当前真实 schema**复制必要字段（color、religion、heritage、language、traditions、name_format及所需名称/ethnicities/graphics）。不要假造 `hidden=yes` 等未查证字段，也不要只写旧版 `traits`。它不出现在初始人口、国家主文化、homeland或人物转换中；正常执行结束人口数应为0。临时文化只是本次事务集合，不是家谱或祖先来源登记。

必要后置条件：选中州总人口不变；原 ce_xiyu 减少约半数（允许引擎按各 pop 舍入）；目标文化—宗教配对增加相同人数；未选中州及原目标文化的其他宗教人口不变；临时文化人口为0。原生转换是否保留就业、财富、识字与资格以及百分比舍入，需用同一场景记录前后值，不能靠 Python 模拟宣称通过。

保守残留清理：若发现上次遗留临时文化，先处理残留再开始新事务；有完整有效的本次目标记录时可完成原定最后阶段，否则只将临时文化回到 ce_xiyu，**保留当下宗教**，避免猜测原宗教或转入错误国家文化。后者不能保证恢复 phase2之前的宗教，报告须保留这一故障恢复边界。清理日志与变量由开发证据保存，不向玩家展示实现细节。

## 4. 原版地域文化—宗教权重

JSON `states[].pairs` 保存全部原版配对；`eligible_non_sinosphere_pairs` 为排除当前有效 `tradition_sinosphere` 文化后的候选。`weight` 是原版配对人数除以公约数的整数权重，保留原始比例；`weight_fraction` 只便于阅读。抽取的是**一个完整 culture+religion pair**，不是先抽文化再独立抽宗教。原版 create_pop 明示宗教优先；省略时采用 GAME 文化定义的 religion 默认，并记录来源。

来源链：当前 MAIN `history/states` 的 QE1 owned_provinces → 同省份ID的 GAME create_state → 对应 GAME `history/pops` 的 region_state → create_pop文化/显式宗教 → GAME文化默认宗教。原版例子：乌兹别克/塔吉克/维吾尔默认sunni（`00_cultures.txt:6829`、`:7002`、`:7064`），哈扎拉默认shiite（`:7237`），藏默认gelugpa（`:7637`）。显式宗教可能覆盖文化默认，不能丢掉。

|当前地区组|主要候选（前三项，仅示例；小群体保留在JSON）|
|---|---|
|西都 STATE_UZBEKIA|uzbek+sunni 67.6%；persian+shiite 9.8%；tajik+sunni 8.1%|
|拔汗那 STATE_FERGANA|uzbek+sunni 64.5%；kirgiz+sunni 24.0%；tajik+sunni 10.0%|
|内花州 STATE_KHIVA|uzbek+sunni 44.9%；persian+shiite 24.5%；turkmen+sunni 22.3%|
|外花州 STATE_TURKMENIA|turkmen+sunni 80.5%；persian+shiite 19.5%|
|木鹿 STATE_MERZ|turkmen+sunni 90.2%；persian+shiite 9.0%；uzbek+sunni 0.8%|
|葱岭 STATE_TAJIKISTAN|tajik+sunni 70.3%；uzbek+sunni 23.7%；kirgiz+sunni 4.6%|
|黠戛斯 STATE_KIRGHIZIA|kirgiz+sunni 44.5%；uzbek+sunni 36.8%；kazak+sunni 6.7%|
|西益 STATE_JETISY|kazak+sunni 37.9%；uighur+sunni 32.2%；kirgiz+sunni 29.9%|
|准噶尔 STATE_DZUNGARIA、伊犁 STATE_ILI|原版母地区背景：uighur+sunni 51.5%；mongol+gelugpa 27.7%；kazak+sunni 20.8%|
|大沙海盆地 STATE_TIANSHAN、西天山 STATE_WESTERN_TIANSHAN|原版母地区背景：uighur+sunni 92.4%；kirgiz+sunni 4.3%；tajik+sunni 2.4%|
|赫拉特 STATE_HERAT|persian+shiite 55.9%；pashtun+sunni 22.5%；tajik+sunni 11.3%|
|白勒黑 STATE_BALKH|tajik+sunni 40.1%；uzbek+sunni 24.6%；turkmen+sunni 10.9%|
|西佛山 STATE_CENTRAL_HIGHLANDS|hazara+shiite 68.9%；tajik+sunni 23.9%；pashtun+sunni 4.8%|
|喀布里斯坦 STATE_KABUL|pashtun+sunni 58.9%；tajik+sunni 28.2%；hazara+shiite 5.7%|
|健驮逻 STATE_KANDAHAR|pashtun+sunni 82.3%；tajik+sunni 8.1%；hazara+shiite 3.5%|
|克什米尔 STATE_KASHMIR|kashmiri+sunni 56.4%；tibetan+gelugpa 21.1%；kashmiri+hindu 14.8%|
|青海 STATE_QINGHAI|tibetan+gelugpa 66.1%；mongol+gelugpa 21.3%；kazak+animist 8.1%|
|萨马拉 STATE_SAMARA|russian+orthodox 50.0%；kazak+sunni 24.7%；bashkir+sunni 18.2%|
|阿尔泰 STATE_ALTAI|mongol+animist 74.0%；russian+orthodox 15.0%；tatar+sunni 11.0%|

**地理边界：**伊犁仍是 STATE_ILI；改名西益的是 STATE_JETISY，不能混淆。新拆伊犁/准噶尔、天山两州，以及当前QE1只覆盖部分原版substate的东喜马拉雅、普什图尼斯坦，标记 `full_native_substate=false`；整组原版人口作为地区背景权重，不是精确划进该现州的人数。没有按面积/省份数拆分人口。其他满覆盖组的原版人数可准确描述其覆盖范围，但仍不是当前 ce_xiyu 的个人祖先。

事件资格不应依赖“当前州里是否还有目标文化”。即使现州已全为ce_xiyu，只要该州有有效历史映射，仍可复归；目标用数据库culture/religion，不要求该州预先有同类pop。未在36州映射的新征服州不能套用“所有未识别地区都uzbek+sunni”的兜底，应扩展地理表或暂不纳入这类事件。

## 5. 崩解建国、军队与战争的完整原版链条

### 一条最接近的原生起义链

GAME `common/journal_entries/03_russia.txt:792`–`:828` 的失败条件调用 `kazakhstan_events.1` → `events/soi_events/00_ep1_kazakh_events.txt:26`–`:68` 选取现所有国的具体州、变tag或 `create_country` → `:71`–`:102` 设置人物/法律/IG并创建军队 → 选项 `:125`–`:150` 转移更多限定地区 → `:219`–`:277` 创建外交博弈、双方战争目标。国家定义 `common/country_definitions/00_countries.txt:1267` 给KAZ文化/首都；兵种 `common/combat_unit_types/00_land_combat_unit_types.txt:10`、`:674` 有实际 irregular infantry/hussars（max_manpower=1000）；外交类型 `common/diplomatic_plays/00_diplomatic_plays.txt:129` 与 `common/war_goal_types/21_return_state.txt:24`、`:34`–`:36` 定义state目标、所有权与宣称验证。

另一个真正崩解链：GAME `common/on_actions/00_code_on_actions.txt:475`–`:482` 月度 → `events/bic_breakup.txt:45` 的 `collapse_india_effect` → `common/scripted_effects/00_victoria_scripted_effects.txt:4456`起。`:4458`–`:4474` 先检查实际领土和目标tag不存在，再创建具体国家；`:4493`–`:4502` 将来源国仍拥有的后续州交给新国；`:4725`、`:4740` 有已存活受领国转属分支。DEI崩解同样先按当前归属分配，`events/dei_breakup.txt:106`附近再显式使属国独立。不能裸调用这些地区专用helper给QE1使用。

### 可采用的原生步骤

- `create_country = { tag = BUK origin = root state = scope:seed_state on_created = { ... } }`：DOC `effects.log:878`–`:889`；state/province字段可重复，on_created中scope是新国。必须先证明seed属于QE1、非伊犁，且目标tag不存活。不要把可能不存在的多州字段直接塞进同一创建块。
- 如果目标tag已经存在，只向其转移**当前仍归QE1**的分配州；不得重复造tag、重置其领导人或复制一次军队。新建和既存目标共用后续分配，但初始化只跑新建分支。
- 使用 `on_created` 保存新国，再从已确认存在的国家读取capital/region；处理每个后续州时重新判断该具体 `region_state:QE1` 存在及归属。全部现有第三国部分不动，人口、建筑和产权随真实state归属走；不能只改地图标记。
- `origin`继承哪些政治与经济属性的文档不完整。需要时明确设置新国的主文化、官方宗教、法律与首都；`set_state_religion` **是country scope的官方宗教**（DOC `effects.log:37150`–`:37155`，GAME `events/bic_breakup.txt:78`），不是转换州内所有pop。不要把国家初始化当人口全体改宗。
- 原生 `create_military_formation` 输入country（DOC `effects.log:959`–`:983`）：`type=army`、`hq_region=新国.capital.region`、每个 `combat_unit` 带 `type=unit_type:...`、`state_region=新国.capital.state_region`、`count`。KAZ原版创建5步兵+5骑兵；它只证明此写法存在，不能直接作为每个西秦继承国合理兵力，更不能把count当立即满员人头。已有转属军营、军队、科技、人力、军备需检查，避免按州循环刷多个模板军。
- `create_diplomatic_play` 的当前原版真实用法在发起国scope内给 `target_country`，并按类型给target_state/war_goal；生成文档该项示例陈旧，不能反过来否定当前GAME实例。直接开战字段 `war=yes` 有原生历史链：`common/history/diplomatic_plays/00_texan_war_of_independence.txt:8`、`00_fezzan_revolt.txt:6`；动态事件里使用该字段仍需实机确认。
- 新国家之间的战争应在所有领土转属、身份和军队初始化完成后再排队启动，重新检查双方alive、独立/关系、无既有同场战争或同一pending、目标州归属与宣称。一个共享结算锁保证动荡条100只触发一次；不要让每个子JE或每个创建国重复执行全境崩解。

本体仅给各机制的支持证据，未证明“多国同日创建、同步军队转属、多个直接战争”这个组合已经可运行。本轮可做源码/MCP关系检查；真实军事编制、外交博弈合法性和开战时序仍是必要的定向引擎项目。

## 6. 可用tag、领土重叠与保留伊犁

JSON `native_country_candidates` 给当前有效定义、首都、文化、释放表、源码行和开局存活情况。重点：

|实体|tag|当前定义/释放表的主要领土|
|---|---|---|
|布哈拉|BUK|首都/释放州 STATE_UZBEKIA；GAME定义 `00_countries.txt:1199`|
|乌兹别克|UZB|首都FERGANA；释放范围UZBEKIA/FERGANA/KHIVA，GAME `:4131`，释放表`:2655`|
|希瓦|KHI|首都KHIVA；释放KHIVA/TURKMENIA，GAME `:1245`|
|浩罕|KOK|首都FERGANA、主文化kirgiz；释放表KIRGHIZIA/TAJIKISTAN，GAME `:1256`|
|土库曼|TRC|recognized，首都TURKMENIA，释放TURKMENIA/MERZ，GAME `:2881`|
|土库曼游牧实体|TRM|decentralized，首都TURKMENIA，GAME `:4480`；不等同TRC|
|哈萨克|KAZ|首都SEMIRECHE，释放表是provinces而不是单一states；GAME `:1267`|
|吉尔吉斯|KYR|KIRGHIZIA，GAME `:4142`|
|塔吉克|TJI|TAJIKISTAN，GAME `:4120`|
|西域|XIN|主文化uighur；当前MOD释放表包括DZUNGARIA、ILI、TIANSHAN、WESTERN_TIANSHAN、JETISY；GAME定义`:1966`|

不要用猜测的TKM/TJK/KIR/UYG等tag；TRK实际是非洲Turkana（GAME `country_definitions/01_africa.txt:697`）。同样不能先按UZB的完整释放表释放，再按BUK/KHI完整表释放：三者领土重叠，后执行者会遇到空scope或夺走前者土地。**XIN现有释放表包含伊犁**，直接release会违反本轮保留核心的要求。

JSON另给 `exclusive_breakup_partition_proposal`：一套互不重叠、覆盖当前36州的**玩法设计候选**，不是原版边界或历史必然结局。它通过集合检查：36州各出现一次，QE1仅保留STATE_ILI。父任务可据用户范围调整；若“伊犁核心”应包含邻州，必须显式改保留集合，而不是混用原版伊犁译名。

|目标|候选分配（仅转QE1当前份额）|
|---|---|
|QE1|伊犁 STATE_ILI|
|XIN|准噶尔、西益、大沙海盆地、西天山|
|BUK / UZB / KHI|分别西都 / 拔汗那 / 内花州|
|TRC / KYR / TJI|分别外花州+木鹿 / 黠戛斯 / 葱岭|
|KAZ|老白山、车里雅宾斯克、西海沿岸、萨马拉、七河、药杀水|
|AFG|白勒黑、西佛山、赫拉特、喀布里斯坦、健驮逻、普什图尼斯坦、堡山|
|KAL / PER|分别俾路支斯坦+北俾路支斯坦 / 锡斯坦；两者开局已存活，走受领分支|
|TIB / KAS|分别拉萨、阿里、青海、东喜马拉雅 / 克什米尔|
|MGL / TUV|分别阿尔泰+乌里雅苏台 / 图瓦；MGL已存活|

新战争可用相邻竞争者与重叠原生主张作为候选，但战争目标须显式选定。例如BUK与UZB是不同国家，不能给双方自动相互吞并且无缓冲；是否全都直接开战、是否包括残秦、波斯/卡拉特是否脱离属国关系，是结果设计，不由接口研究替代。当前36州独占表只解决“谁拿哪片QE1领土”，不擅自更改第三国或现存臣属关系。

## 7. 军事压力、战争与恶名读取

|需要读的量|可用表达式、含义与来源|
|---|---|
|常备营规模|country `army_size`：营数，不含当前征召；DOC `event_targets.log:888`–`:893`|
|含已征召营规模|country `army_size_including_raised_conscripts`：营数，含已征召、排除未征召；DOC `:902`–`:907`，GAME `common/script_values/ip4_je_values.txt:547`实际使用|
|兵力估计|country `army_power_projection`：力量投射值，不是士兵人数；DOC `triggers.log:8757`–`:8762`|
|士兵职业人口占比|country `pop_type_percent_country = { pop_type = soldiers percent > 0.01 }`；DOC `triggers.log:13595`–`:13605`；分母人口，不要写成营数比例|
|实际士兵劳动人口|country → every_scope_pop，limit `is_pop_type=soldiers`，累计 `workforce`；DOC `triggers.log:12203`、`:14829`。若要包括军官，另加 officers，不要把它们混为一个type|
|士兵家庭总人口|同集合累计 `total_size`；它与workforce区分，DOC `triggers.log:14659`；dependents有独立读取`:9672`|
|部队实有人力|new_combat_unit `manpower`；DOC `event_targets.log:184`–`:187`。需先在合法formation/army内迭代unit，不把国家直接当unit|
|是否在战争中|country `is_at_war=yes/no`，DOC `triggers.log:11260`；具体对手 `has_war_with=scope:country` `:10988`，先检查对手存在|
|恶名|country `infamy`数字读取，DOC `event_targets.log:1037`–`:1040`；原版比较 `common/script_values/decision_values.txt:6`、`:13`、`:20` 使用infamy_threshold|
|军费压力|country `military_expenses` / `military_expenses_share`，DOC `event_targets.log:1105`–`:1113`；后者是总支出份额，不是GDP份额|

`army_size_including_conscripts` 的生成文档与 `_including_raised_conscripts` 描述相近（DOC `:895`–`:905`），不能凭名字自行断言前者必含所有未征召潜力。衡量当前征召压力优先选文档明确排除未征召的后者。1000×营数只能估算满编上限；原版兵种max_manpower=1000并不证明所有营满员。

## 8. 后续检查边界

外部可确定：实际地区候选集合与目标执行一致；所有culture/religion/tag有数据库定义；三阶段scope不借用旧pop；无其他玩家/人物文化变更；创建新国与既存受领国互斥；独占分配表不夺第三国且保留伊犁；一次性结算与待处理事件清理；进度条件严格边界；初值仅缺失时设置。结构与引用测试须绑定候选SHA。

引擎仍需确定：百分比舍入与转换后就业/宗教保存、临时文化零残留；创建国的实际继承与人口/建筑/军营转属；同日多国形成后军队归属及补兵；直接开战字段的动态路径与合法战目标；旧档初始化与终局后的引用安全。不要把本报告或映射JSON当作这些行为已经发生。
