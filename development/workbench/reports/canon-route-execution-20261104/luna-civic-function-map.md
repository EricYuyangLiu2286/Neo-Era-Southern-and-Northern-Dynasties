# C2 公民路线函数导航（只读）

日期：2026-11-04。范围：候选 `exports/canon-route-execution-20261104-a`（C）、主 MOD（M，只读）、游戏本体（G，只读）、C2 两份合同。未开游戏；未修改脚本；未做验证。本报告只供后续计划/实现定位，绝不是完成或游戏内验证声明。

## 委派与来源状态

- 任务：C2 意大利/HUS/USM路线及18人物的候选函数、调用链、原生接口行号和缺口定位。
- 实际配置：`gpt-6-luna / high`。委派证据：父任务明确要求只读探索，并引用 NESND 技能规定的 Luna/High 职责；不是从代理名称推断。
- 按指定路径读取 NESND 技能、`docs/agents/engineering-skills.md`、C2 合同及 native contract。技能目录的 `catalog.py status` 实际返回 `1.13.11 / build 24799966 / CURRENT / changed_count=0`。WORK 根目录下 `scripts/catalog.py` 不存在；改用技能自身脚本运行成功。
- 没有复查 PPET/原始计划正文，也没有重做 native contract 已记录的引擎研究。原生行号引用沿用已读合同所记路径/行号，再对相关脚本片段作只读定位；版本/当前本体 SHA 见下方。

## 候选公民路线：当前是什么、断在哪里

公民脚本组：

|职责|候选路径及定位|
|---|---|
|JE 定义|`common/journal_entries/nesnd_civic_routes.txt:1–97`：意大利 foundations/concord/common_budget；HUS transport/frontier/citizenship/oil；USM schools/industry/distribution。每组有 `possible`/完成条件，但范围内没有 `add_journal_entry` 启动调用。|
|资格/阶段条件|`common/scripted_triggers/nesnd_civic_routes.txt:1–34`：国家资格、项目门槛、油业和边疆条件。`nesnd_hus_civic_country` 只有 HUS 存活条件，不排除 `nesnd_hus_native_successor`；面向原 HUS 的阶序/登记 trigger 才有 successor 边界。实现时要把两种语义分清。|
|按钮|`common/scripted_buttons/nesnd_civic_routes.txt:1–235`：17 个候选 policy 按钮；每个做一次性 flag + 120 月 modifier。第一批 12 个在行 1–163，USM学校按钮行 165–195，USM分配按钮行 197–235。候选按钮定义存在，不代表玩家文本/JE入口已接通。|
|共用效果|`common/scripted_effects/nesnd_civic_routes.txt:1–6` 的 `nesnd_civic_policy`：只在传入的 eligibility 与 choice flag 允许时挂限时修正并写 flag。|
|数值修正|`common/static_modifiers/nesnd_civic_routes.txt:1–19`：对应上述政策的 120 月效果；未证明这些数值适合当前量纲，也未运行。|

发现的断接：

1. 对 C 做 `add_journal_entry` / `type = nesnd_italy_*|nesnd_hus_*|nesnd_usm_*` 调用搜索，除 USM 西部置省 JE 外，没有发现任何 civic JE 的调用者。**因此这批路线从何时进入日志尚未接线**；单有 `is_shown_when_inactive`/`possible` 不是本候选可见的启动链。
2. C 的 localization 树里找不到 `nesnd_italy_public_works_button`、`nesnd_hus_chartered_contractors_button`、`nesnd_usm_practical_schools_button` 或 `nesnd_civic_policy_once_tt` 等已定义键。应对 17 按钮的 name/desc、JE标题/正文/条件提示及按钮提示逐键做中英闭包。
3. `nesnd_italy_concord` 同时引用 `nesnd_canon_italy_fra`（JE行 12）和 `nesnd_italy_local_concord`（行 18）。前者并非 `nesnd_civic_routes.txt` 内定义的按钮；查清其定义/作用域/启动方和既有有效 localization，再决定保留哪条既有接口。不能误计成新增的 17 policy buttons。
4. 18 个提案 template ID 在 `integration-native-contract.md:97–114`，在 C 脚本/模板/本地化中未找到；C 的三国历史人物初始化文件也只初始化既有人物。当前候选没有人物定义、全局活人/流亡池复用、seen/dead 或死亡/退休调用闭包。报告只定位缺口，不替 Astra 规划生成逻辑。
5. USM civic trigger（`common/scripted_triggers/nesnd_civic_routes.txt:3–8`）限定 USM 活着、`usm_civilwar_occured` 或 `nesnd_south_settled` 之一、停战且主内战 JE 已结束；它没读取 `tag_WUU_var`、西部置省 opened/succeeded/failed，也没有礼法分支。合同要求三个战后入口和旧结局读取，目前从 civic 链看尚未实现。

## 三国现存实际链与入口

### 意大利 / LOM

- 当前 LOM 人物落点是 M `common/history/characters/LOM.txt:1–10`：开局创建 `ITA_GUGLIELMO_PEPE` 和原版 `agitator_giuseppe_mazzini`。佩佩模板在 M `common/character_templates/zz_ce_italian.txt:3–21`（总统、IG领袖、军队领袖、将军）。不要用新模板再造这两人；加里波第也不能无条件生成。
- 候选 `nesnd_italy_country` 依赖 `nesnd_canon_italian_country`，并要求存活且拥有旧意大利地理区州（`common/scripted_triggers/nesnd_civic_routes.txt:1`）。目前完整统一接口仍是原生 `country_formation`；C2 的已研究事实为意大利实际 actor LOM/SAR/SIC/PAP/PAR/MOD/TUS 与形成的 ITA，保留原版 formation 才能覆盖统一后连续身份（integration contract §3、§4）。
- 原生局部统一/参战实现：G `events/italian_unification.txt:644–674` 先定位真实 RSM diplomatic play、保存 DP scope，再 `add_target_backers = { root }`（原合同注明范围 644–674）。如果路线要拉玩家加入，必须复用真实 DP 与阵营；不存在泛化 `join_diplomatic_play` 的已证据。
- 原生 Garibaldi 流亡/迁移接口：G `events/agitators_events/garibaldi_events.txt:185–198` 对真实人物、事件条件和 cooldown 作检查，再 `transfer_character = root`。死亡边界在 G `common/on_actions/00_code_on_actions.txt:2702–2707` 的 Garibaldi alive global 清理；人物全局查找与流亡池应使用合同给的 engine docs `triggers.log:100,106`。适用于借用其生命周期形状，不等于可以按路线强行生成。
- C 路线 currently 有开局经营条件（tooling、铁路/港口、学校：`nesnd_civic_routes.txt:9–14`）、法国按钮/协商与预算 JEs（JE文件 `1–31`），却未接入启动调用。法国同意按钮不能取代 PAR/MOD/TUS/PAP/SIC 逐邦真实对象协商，也不能因此吞并有主权玩家国家。形成 ITA 后的预算/地方制度后继目前只有变量提示，没有本地触发/owner 与失败/多国结局闭包。

### HUS

- C 的公民路线：JE `common/journal_entries/nesnd_civic_routes.txt:32–68`；门槛/资格在 `common/scripted_triggers/nesnd_civic_routes.txt:2,15–20,33–34`。transport 当前要求铁路 30、工具厂 20、食品厂 15 和有占用铁路；油业门槛为 pumpjacks + 实际油井 5 级且占用 50%；这些仅是候选门槛，不是历史证据或已验收值。
- HUS 既存登记链已连接：JE `common/journal_entries/nesnd_hus_registration.txt:1–17`；on_actions 月脉冲维护和革命/法令入口 `common/on_actions/nesnd_hus_registration.txt:1–32`；结算函数 `common/scripted_effects/nesnd_hus_registration.txt:228–253,376–390`；两法选择及 epoch/时钟守卫 `common/scripted_triggers/nesnd_hus_registration.txt:2–65`。该链真实地区分满蒙路线(1)与 native route(2)，不能由 civic JE重设选择。满蒙+原生美国内战永久信号门槛在同 trigger 文件 `78–80`：要求 HUS原国家、登记法正确、manchu route、`american_civil_war` 且汗国未创建。此函数序列/任意先后顺序是 A2 已有边界，C2 不应改写。
- 阶序值在 `common/laws/nesnd_hus_social_hierarchy.txt:1–112`：四级身份 acceptance 范围分别落在 HUS 拥有的 Han、Manchu、native、white culture 条件；普通 four-tier 与满蒙登记法、原住民登记法分别为不同法律。`common/scripted_effects/nesnd_hus_registration.txt:2–30` 清除/停用冲突旧新法并刷新 tier，`8–36` 的 tier refresh 路径；`common/social_classes/nesnd_hus_social_classes.txt:1–61` 按upper/middle/lower class与culture分类；`common/static_modifiers/nesnd_hus_culture_tiers.txt` 提供接受度效果。阶序制度链已存在于候选，公民JE不应“解锁普通公民法”或重置登记法。
- successor 边界（关键）：`common/scripted_triggers/nesnd_hus_registration.txt:2–5` 的 `nesnd_hus_original_country` 明确排除 `nesnd_hus_native_successor` 与 retired；`27–30` 的 citizenship unlock、`63–65` 的革命快照也排除/锁住 native successor。Native successor 标记在 `common/scripted_effects/nesnd_native_khanate.txt:135–136`。反之，公民路线的 `nesnd_hus_civic_country` 仅 `c:HUS ?= this` + alive，因此仍会匹配存活的 HUS successor。应视为**需 Astra 决定的调用边界缺口**：查明大汗国沿用公民 JE 是否在意图内，且绝不能借此改变登记路线。
- 现有 USM 西部州结果为只读输入：C `common/scripted_effects/nesnd_usm_western_provinces.txt:15–45` 管理 success/failure/opened/finished 与既有 West outcome，周调用在 `common/on_actions/nesnd_usm_western_provinces.txt:1–6`。HUS路线不要再次赋予/清零这些变量。

### USM

- 现有战后事件调用在 C `events/flavorUSM_ce.txt:441–507,553–697`：`tag_WUU_var` 与 `nesnd_south_settled` 参与迟答/收复结果，`flavorUSM.1` 设 tag_WUU、创建既有模板人物并开始明吴内战，另外有 `ce_usm_civilwar_journal`。全局停战/结算状态写入见 C `events/usm_civilwar_events.txt:20–23,1276`。M on_action 入口为 `common/on_actions/ce_code_on_actions.txt:30–40,109–116`（新局月度事件、USM本国与危机守卫）。这些现有入口应作为明存/吴代/停战分类源。
- 西部置省入口及旧结局结果不可重做：C `common/on_actions/nesnd_usm_western_provinces.txt:1–8` 接周脉冲、强制战争目标与 capitulation 回调；`common/scripted_effects/nesnd_usm_western_provinces.txt:15–45` 负责 opened/finished/succeeded/failed、一次迁入和恢复州处理。公民JE应读取实际变量与实际 owner-state，避免触发第二轮迁移或改 1850 结算。
- 当前公民触发器 `nesnd_usm_civic_country` 只用两个全局“战争发生/南朝结算”之一 + peace + 原内战 JE 已结束；不会据此区分三入口、未同步礼法、也不会读取旧 western 结果。就当前查到的范围，不存在 civic route 的 `add_journal_entry` 启动链。
- 后续礼法、六部/礼议院、布政司、学政分责应先读取作者现有机制来源；当前 civic 文件中只有学校、产业 readiness 与 distribution buttons，没有礼法政策/资格状态函数。虚构“席位数”接口风险已由 integration contract §4 明确排除。

## 18人物映射（提案对照索引）

唯一权威提案行在 `integration-native-contract.md:97–114`。表中均为计划模板，不是候选已存在人物：

|路线|template ID（contract 行）|身份/进入主题速记|
|---|---|---|
|意大利|`nesnd_ita_valdieri` (97)|瓦尔迪耶里；融资/工业| 
|意大利|`nesnd_ita_bellandi` (98)|贝兰迪；教育/出版、合资格 agitator| 
|意大利|`nesnd_ita_rusciani` (99)|鲁夏尼；南方土地/地方财权，按实际 owner 引入| 
|意大利|`nesnd_ita_sereni` (100)|塞雷尼；确有军职才给 general| 
|意大利|`nesnd_ita_vitali` (101)|维塔利；PAP 教育财政，不升任教宗| 
|意大利|`nesnd_ita_martelli` (102)|马尔泰利；晚期真实劳动运动| 
|HUS|`nesnd_hus_tong` (103)|佟世衡；东青行/承包，不假造 CEO| 
|HUS|`nesnd_hus_shen` (104)|沈季川；债务劳工/资格，废奴后转议题| 
|HUS|`nesnd_hus_bayant` (105)|巴彦图；受影响牧地与实际 POP| 
|HUS|`nesnd_hus_lin` (106)|林素岚；识字/债务劳动，任官需法律适格| 
|HUS|`nesnd_hus_lu` (107)|陆景铎；工业就业/公开投资| 
|HUS|`nesnd_hus_guan` (108)|关廷宪；真实油业/矿权条件后期进入| 
|USM|`nesnd_usm_ji` (109)|季文衡；战后沿海资格/利益| 
|USM|`nesnd_usm_duan` (110)|段敬川；教习→资格后学政，全球单例| 
|USM|`nesnd_usm_xu` (111)|许廷璋；礼法资格和征敛| 
|USM|`nesnd_usm_luo` (112)|罗映棠；教育/劳动，任官受法律限制| 
|USM|`nesnd_usm_han` (113)|韩士铎；技能教育/真实劳动议题| 
|USM|`nesnd_usm_jiang` (114)|蒋绍衡；后期预算/跨省工程| 

合同 §5（`integration-native-contract.md:119–129`）是创建/生命周期边界：全局人物先查、流亡池单独查、活人优先复用、seen 永久、dead/retired 不复生；政治人物使用 `role=character_role_politician`，不是全部做 IG leader；女性/未达运动资格人物用具名事件身份，agitator槽位和法律适格需实查。原生 Douglass template 与 Garibaldi/Mazzini/Pepe均为现成人物参考，不能为填人数复制模板。当前候选没有这些模板/生命周期闭包。

## 后续规划者仍需核实

- 计划正文与原作者资料原文到具体行为的逐条映射；本报告未读取 PPET/DOCX 或 regional plan 正文以免复做已完成研究。
- `nesnd_canon_italian_country`、`nesnd_canon_italy_fra`、`nesnd_italy_local_concord` 的确切定义来源/玩家范围/真实外交后果；确认现成调用者后再接入。
- 每个 civic JE 的唯一启动入口、JE完成与子JE生命周期、旧档已记录状态及政治最终结果；尤其统一后 ITA 连续性、HUS native successor政策、USM礼法三入口。
- C2 18人何时进入、哪个国家/州/人物池角色、活动/死亡与流亡后事件；先查全局人物而非模板生成。
- localization 缺键的完整有效覆盖层（replace/base、双语和 BOM）；当前只做候选树键查询，未做全 MOD 有效键覆盖审计。
- 引擎支持与真实效果、数值量纲、按钮 tooltip scope、存档触发；均未验证。

## 关键来源及 SHA-256

SHA 来自本轮读取时的确切文件；候选 SHA 只标识 C，不暗示已冻结或已验收。

|对象|路径|SHA-256|
|---|---|---|
|C civic JE|`exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_civic_routes.txt`|`90D972E4DC9631AEDEE41468059B410F3C57E7D9126057C2130125D29AE8BA8E`|
|C civic effects|`exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_civic_routes.txt`|`B51BDD9B83FC4E4E26ABD316AFF1D5222B09828F1969898DD1F19C170F4763BD`|
|C civic triggers|`exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_civic_routes.txt`|`0516CA0C2A29DAF721634777C604E929F454587B049068EFA792405A9170F128`|
|C civic buttons|`exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_civic_routes.txt`|`FD1817700F16EC05029D6B94A96CA56F8F369E5D80EFACF3F1F5C900C9E36BFC`|
|C civic modifiers|`exports/canon-route-execution-20261104-a/common/static_modifiers/nesnd_civic_routes.txt`|`4F536A9EA5703788E65012827154F8E4B8A9D4E0278E82D19551255AE4D24207`|
|C HUS registration JE|`exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_hus_registration.txt`|`AAADCC5EE5FDFDC76857A548A04A29B2DF994B027C260BEAA72769749CE4844E`|
|C HUS registration effects|`exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_hus_registration.txt`|`677CEC937BD828A0DFBC17D269085CFBD331BBA926A66A1169C9F6D8B4F094B5`|
|C HUS registration triggers|`exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_hus_registration.txt`|`F6244AFA4ABAEED044B971F7C1DB32A7C0C08E9CBA41649285F658130BD29955`|
|C HUS hierarchy laws|`exports/canon-route-execution-20261104-a/common/laws/nesnd_hus_social_hierarchy.txt`|`075642A6D6FBE152D6152F1F751DABB9D4BE5462B6EBDD56B1EFF6078E9A9025`|
|C HUS hierarchy on_actions|`exports/canon-route-execution-20261104-a/common/on_actions/nesnd_hus_registration.txt`|`6CDA6FF84263D076A614CE0DE8102E18B33858FC71176AE781761302E9EE3ADE`|
|C native successor marking|`exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_native_khanate.txt`|`CD79A8FCB8071796193D856ABCD006424242418AC064FB7B6EDBD0BB94DECD15`|
|C USM western on_actions|`exports/canon-route-execution-20261104-a/common/on_actions/nesnd_usm_western_provinces.txt`|`1BCD99FD053E26E05ABE13B4D032D9AA8529CA5C604940F5B5D647CDC59BA48B`|
|C USM native event file|`exports/canon-route-execution-20261104-a/events/flavorUSM_ce.txt`|`1C75E75B015394B9AF4A75639D7DB0C943E4AAF81834DFC177B6BE2D3DBECD2C`|
|C USM civil-war events|`exports/canon-route-execution-20261104-a/events/usm_civilwar_events.txt`|`7A1458CB344D7AAF62204647522E6BD02D3E2E3482ADC7349714F1B426A801FE`|
|C USM western result effect|`exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_usm_western_provinces.txt`|`1DCB81D48E736D06088706A26848AF765B0941D1DC13F28FF43E3977C87B9824`|
|C LOM historical characters|`exports/canon-route-execution-20261104-a/common/history/characters/LOM.txt`|`65BD1D1C53933CA2171F008F6FBAA333CF594770E8628503682E6495119AD75F`|
|C HUS historical characters|`exports/canon-route-execution-20261104-a/common/history/characters/HUS.txt`|`8AA8FAEF8CC3204BA6EA79370B50143B3EFD9A14763156975258639F445E80E2`|
|C USM historical characters|`exports/canon-route-execution-20261104-a/common/history/characters/USM - UnitedStatesOfMing.txt`|`EBF6A3C4559B2A43CDC8CFC8225418F14B058063E995C5BC766770965EBF744F`|
|M Pepe template|`MOD/common/character_templates/zz_ce_italian.txt`|`DD4F8F72C3C9E747C77C9C1090AFA6C606ED740186D603EE39C0BC96F10EA2E7`|
|M USM entry on_actions|`MOD/common/on_actions/ce_code_on_actions.txt`|`DF60C03CC9EECE388A7EB8E030ECA2B14F8890E8A522F18AA28C57086B2B709B`|
|G Italian unification|`GAME/events/italian_unification.txt`|`3564046713083EFE19A97FE04A3D83A6E875A627794652CE726C727C602B296E`|
|G Garibaldi events|`GAME/events/agitators_events/garibaldi_events.txt`|`F421A5F191A0CDE1D57A2D214701618F1F969A062196BD6C2897E5F38BFA1216`|
|G event hooks|`GAME/common/on_actions/00_code_on_actions.txt`|`EC3E3E97140777B10D4D99F41C528EC1DC6F1499429E3E2F566B3819A36E63BB`|

`MOD`=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`; `GAME`=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`; `WORK`=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`.
