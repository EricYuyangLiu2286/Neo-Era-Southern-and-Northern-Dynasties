# JIM／林汉涵迁移与原版日本链：实施依据

2026-11-02。父任务指定基线 c4bbc19；本报告只读当前主 MOD 与本机原版，未编辑玩法、未运行游戏。`catalog.py status` 返回 CURRENT，Victoria 3 1.13.11 / build 24799966、changed_count 0。源 SHA 清单见同目录 `lin-native-source-sha.json`。下文 M=主 MOD，G=当前 GAME，E=WORK/references/engine-docs-1.13.11-20261031。建议变量、效果名均为拟议接口，不冒称已存在。

权威规格：WORK/plans/two-empires/20261102-japan-development-design.md 第九节修订2、第十节修订3及 20261102-japan-india-lifecycle.md。目标是 JIM=天皇／林摄政、JIM主流 japanese+ce_wuu、保留既有人物与领土、旧JAP实际林统治存档有合法交接。新旧双方所有持久成果不可用重播分封初始化来补齐。

## 1. 已有调用链与应改的位置

|文件与位置|实际行为|最小改动位置|
|---|---|---|
|M/common/character_templates/zz_historical_leaders_ce_asia.txt:939–962；M/common/history/characters/USM - UnitedStatesOfMing.txt:35|唯一 `USM_lin_hanhan`：USM现存军官，闽文化，林/汉涵；不是新建模板|迁移同一实例，不改文化／宗教／姓名／模板，不重新create|
|M/common/scripted_triggers/nesnd_japan_lin_regency.txt:1–81|候选必须USM、非ruler非heir；realm_ready检查三国属USM，受任国JAP君主制；pending也硬绑JAP|新任命的 recipient 改为JIM；旧JAP ruler不能走这个候选入口，另建迁移路径|
|M/common/scripted_effects/nesnd_japan_lin_regency.txt:8–88|USM持久pending保存精确officer/country/previous_ruler→转国→设ruler→记录country/regent/previous_ruler|目标改JIM；成为ruler前保存JIM当前天皇和其真实继承人；完成后设置天皇身份和后续交接|
|同文件:94–119；M/common/on_actions/nesnd_japan_lin_regency.txt:1–14|先maintain再appoint；recipient失效只撤标题，不换统治者，并删除previous_ruler；appointment-once保留|旧档捕获／迁移必须放在这些清理之前；不能先全局替换JAP导致清理吃掉证据|
|M/common/government_types/00_nesnd_japan_lin_regency.txt:4–10|hereditary，actual ruler显示摄政王；未使用原版regency modifier|保持一个actual ruler，改为JIM身份谓词；加准确的天皇/继承人称号或UI说明，不把engine heir误称林之子|
|M/common/country_definitions/nesnd_japan.txt:2|JIM cultures只有japanese|加入ce_wuu、保留japanese|
|M/common/scripted_effects/nesnd_japan.txt:154–222|创建JIM，origin JAP，激活monarchy/autocracy；移现存天皇或创建匿名Yamato后备，设其ruler，再写emperor_var|新国on_created显式add_primary_culture=cu:ce_wuu。保留当前天皇精确对象。不能只依赖definition覆盖origin继承|
|同文件:378–387、450–453|JAP残余激活autocracy、删emperor_var；完成三国后USM调用Lin任命|注意前述激活autocracy可调用原版law_bakufu退出效果；在首个法改之前建立分封保护。最终commit后接新的JIM初始化／任命|
|M/common/scripted_effects/nesnd_japan_recovery.txt:52–85、174、218–264|恢复JAP时身份重置只保留japanese；从USM移回既有Yamato候选→调用同一个partition|当前init_identity仅调用于JAP；若今后供JIM复用，文化剔除必须保留japanese+ce_wuu。当前最小补丁是在JIM on_created和旧档刷新加ce_wuu，不让JAP也变江南|

新分封链入口：M/events/nesnd_japan_events.txt:13、M/common/war_goal_types/nesnd_japan.txt:14；吞并恢复入口最终到M/common/scripted_effects/nesnd_japan_recovery.txt:264。两者共用 `nesnd_partition_japan`，无需复制建国链。不得改变京都／关东敌占崩溃、第三国州保护或既有领土分配。

## 2. 已证明的原生角色接口

E/effects.log 64–67、36452–36455、36683–36686、36816–36819、36910–36914、37318–37322：

```text
# character scope, target country
scope:lin = { transfer_character = scope:jim }
# character scope, rules character's present owner
scope:lin = { set_character_as_ruler = yes }
# country scope, target character
scope:jim = { set_heir = scope:emperor }
# character scope, database role is supported
scope:emperor = { add_character_role = character_role_emperor_of_japan }
```

`set_character_as_heir` 不在当前引擎文档；实际接口是country-scope `set_heir`。`replace_character_roles`能保序替换角色，但不要在Lin身上remove_all，军官/IG角色应保留。

最直接同类实例：G/events/iberia_events/regency_events.txt:104–120：

```text
ruler ?= { save_scope_as = monarch_scope }
# option, same country scope
scope:ig_candidate_1.leader = { set_character_as_ruler = yes }
set_heir = scope:monarch_scope
```

因此“现君主→保存精确scope→另一人设ruler→原君主set_heir”是有原版实例的流程，不需要虚构regent effect。原版该option另调用的 `add_regency_modifier` 和 `designate_character_as_regent`不适合照搬：G/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:298–306将摄政设为immortal；G/events/iberia_events/regency_events.txt:441–468在heir成年时还政。成年天皇会立即满足原生还政路径。G/common/scripted_triggers/00_ip4_victoria_scripted_triggers.txt:1–16的has_gov_regency只查这些modifier，不查政府名；故维持现有自定义office显示不自动触发其还政链。

独立天皇身份有现成数据库：G/common/character_roles/02_unique_roles.txt:1–13的 `character_role_emperor_of_japan` 是type=other、priority=50、天皇名称和ruler图标；G/common/character_templates/country_jap.txt:28–49给仁孝该role、`house_yamato`和special emperor trait。这证明天皇可以在不是actual ruler时存在。JIM新国将天皇设为ruler时没有JAP专有新君主hook，不能假定role已自动正确移除或恢复；新模块显式维护。

建议最小模型：Lin唯一actual ruler；当前天皇保留同一人物实例，写JIM独立的精确 `nesnd_japan_emperor`（拟名），并兼容 `emperor_var`；授予native emperor role，使用country `set_heir`把他作为Lin退出后的合法承接者。这和原版摄政的engine表示一致；用JIM自定义male_heir/female_heir显示“天皇”，并记录原JIM.heir为帝室后继，避免把成年天皇表现成林的子嗣。角色显示组合仍需用户实机核验，源码证明不等于UI验收。

## 3. 新任命与旧档迁移的提交顺序

### 新分封／Lin仍在USM

1. JIM存在且为君主制，已有当前天皇必须alive、owner=JIM、非流亡；保存JIM ruler/原heir精确scope。先保存持久pending，再转Lin。
2. 使用原有USM候选资格找到同一USM_lin_hanhan；只从USM移至当前已捕获的JIM。确认transfer后owner=该JIM，才set_character_as_ruler。
3. 确认Lin actual ruler后，为原天皇恢复/保留emperor role、set_heir，写帝室后继精确引用、JIM制度身份及江南目标。JIM同时add_primary_culture japanese/ce_wuu，非人物文化改变。
4. 最后写commission完成、v2迁移完成和准确recipient，再清pending。不可预先清旧completed锁再重入，会重复发奖或换君主。

### 旧存档：Lin已经JAP actual ruler

必须从存量变量捕获，不允许把USM非ruler条件放宽到任意外国owner。首先在旧维护前读取USM `nesnd_japan_lin_commissioned_officer` / `nesnd_japan_lin_regency_country`及JAP `nesnd_japan_lin_regent`、`nesnd_japan_lin_previous_ruler`。验证它们指向同一个alive、owner=实际JAP、template=USM_lin_hanhan的当前统治者。旧证据缺失时，只有JAP actual ruler本身的template+旧任命标记足以识别，不能any_character全世界搜索抢回。

准备阶段全部完成后才改人物：

- 捕获准确JAP、JIM、Lin、JAP合法承接者、JIM当前天皇、JIM原heir，保存本次migration身份和阶段。不清旧引用。
- JAP合法承接优先恢复该次误任命保存的、仍alive且owner=JAP的丰臣前任；否则使用当前合法丰臣heir；否则本国既有且合法的house_toyotomi朝廷成员。除非明确设计了新朝廷fallback，不凭日期create既已死过的具名丰臣人物。无安全接任人则记录待定而不移走ruler。幼年合法heir会进入原生幼主摄政，需单列测试；不宣称用成年随机官员替他也是“合法继承”。
- 先对精确JAP承接者set_character_as_ruler；验证JAP ruler已经不再是Lin，Lin仍归JAP且不再ruler/heir。然后标记“JAP交接已完成”。这一阶段后重复执行不得再次恢复前任。
- 原JIM current ruler应优先确认为house_yamato或精确现有emperor_var；若当前JIM已共和、别朝实际执政、天皇已外流/死亡或人物合法移到第三国，停止自动转移，不覆盖当前政治结果。
- 把同一Lin从JAP转至捕获JIM；验证owner，再设为ruler；同新任命保存天皇为native role+heir、原帝室heir另存。
- 只有所有后置条件成立才将USM recipient/officer和JIM regent/appointed/active更新为新对象，清JAP旧office变量。清JAP旧office时旧 `nesnd_japan_lin_clear_recipient`会删除同一个Lin的commissioned标记：要么先清JAP再写JIM最终commissioned，要么写专用迁移清理，不可调用后把新标记删掉。
- 旧USM completed标记保留；另加版本完成标记。部分迁移重试只接受记录中人物在记录中的JAP或JIM，绝不接受第三国owner。若JAP交接已完成而后续无效，保留已合法接任结果并结束/暂停该案，不能强行把Lin再放回去覆盖新君主。

补丁触点：在同一个 `nesnd_japan_lin_monthly.effect`里把migration置于maintain/try_appoint之前，以实际代码顺序保证；不能依赖两个独立月度on_action的文件排序。recipient清理也必须排除正在迁移的记录。after-lobby可同入口初始化，但月度是旧档补漏，不重置有值记录。

## 4. 摄政退出与帝室连续性

country层制度身份和ce_wuu政策独立于Lin个人、USM的tag_WUU和当前宗主；任命资格仍可要求原三国结算，office存续不能继续用“属USM且不交战”的旧判断。独立、改宗主或USM灭亡只结束宗主的委任/合作，不自动抹掉JIM的天皇—摄政制度和已经转换的人口。

Lin正常死亡：若原天皇alive、仍owner=JIM且是合法heir，原生hereditary继承有既定接任对象；新 `on_new_ruler` country-owner刷新精确emperor_var并撤摄政标题。强制还政/辞职则明确set_character_as_ruler=原天皇后再收尾。若Lin被政变/共和替换，尊重实际法律/君主，不在月度把天皇强塞回去。死亡/外流天皇不复活。

天皇先死亡时：JIM现存原帝室后继（提前保存的原JIM.heir）是首选，验证alive/owner/JIM/house_yamato；改为emperor role与Lin的heir。若无明确后继，选本国既有合格帝室成员或进入明定宫廷交接，不在月度反复create。若决定生成匿名后备君主，可参考已有partition fallback，必须一次锁且不是复活具名模板。原生继位链不能直接调用于JIM，见下节。

新增native `on_character_death` / `on_new_ruler`只追加专用on_action，root=character；先验证owner，再在owner country执行JIM刷新。原版 `_on_actions.md`和00_code_on_actions.txt:2604、2889证明scope；事件发起中必须保存精确国家，不能把character root当country。月度维护用于纠正缺标记，不承担重复换人的“保险”。

## 5. 原版JAP硬绑、全局改革冲突与准确接缝

|原版／MOD链|确定的冲突|适合的窄接缝|
|---|---|---|
|G/common/laws/00_distribution_of_power.txt:156–169 `law_bakufu.on_deactivate` → G/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:1–76 `country_restore_japanese_emperor`|退出幕府法时退休现heir，强设现天皇ruler；找不到时生成新天皇。分封中的activate_law autocracy也可触发，尤其新国继承bakufu后再激活|在小型scripted_effect `country_restore_japanese_emperor`的MOD REPLACE内，按NESND政治身份/正在分封/正在迁移分流；其他国家保留原body。分封guard在任何law mutation前设置。不要只在事件末尾标记|
|G/common/laws/00_distribution_of_power.txt:134–150 → `country_generate_japanese_shogun`|幕府法重新激活会生成/换丰臣；M/common/scripted_effects/ce_japan_gov_effects.txt:1已有REPLACE，按年份可无条件create具名人物|在已有REPLACE入口添加managed身份/迁移守卫；不能用该effect恢复旧档JAP合法接任，因为会改变角色、IG、意识形态，可能复制／复活|
|G/common/on_actions/00_code_on_actions.txt:1069–1076|月度历史heir生成只JAP；M/common/scripted_effects/ce_japan_gov_effects.txt:355–594替换了generating effect，Yamato/Tokugawa/Toyotomi依ruler家族和country spawned旗标create|JIM/JTK用专用继承维护；有历史heir则按native can_generate_scripted_heirs不再造人。迁移后Lin不属Yamato，不能靠此函数维持帝室；也不直接重用有旧spawn标记漏洞的具名create分支|
|G/common/on_actions/00_code_on_actions.txt:2806–2840|JAP君主死亡→帝室继承；bakufu安全逻辑保证“全为Tokugawa”|小型 `character_appoint_new_shogun_when_no_heir` 的REPLACE最适合为Toyotomi身份分流；原body仅用于合适的德川情形。该body:2917–2927会把现非Tokugawa heir执行adopt_into_tokugawa，实际改姓/家族，不是仅标题|
|G/common/scripted_effects/00_victoria_royal_successions.txt:946–1095；G/events/japan_events/ep2_imperial_events.txt:71–96|帝室死亡原生链的无DLC分支写c:JAP.emperor_var；DLC事件非bakufu分支也写c:JAP，并仅找已经有的下一模板|不要给JIM直接调用此chain或japan_monarchy事件；追加JIM自己的owner-aware精确继承流程，按实际存在对象，不按年份复生|
|G/common/on_actions/00_code_on_actions.txt:3077–3118 → on_new_ruler_japan_effect；后者G/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:3083–3127|只JAP，Yamato写c:JAP.emperor_var；移除emperor role；Yamato持bakufu会立即改oligarchy|JIM用自身identity refresh，不能调用硬绑的effect；新JIM ruler属于Yamato时更新自己的emperor变量并清非执政角色，Lin ruler时保留宫廷天皇|
|M/events/usm_civilwar_events.txt:1704–1706、2189–2191、2385–2387|`.14.1/.17.1/.20.1`还在直接add原生je_meiji_restoration|更换成新的国内/独立阶段刷新入口，防旧外交选项重开原版维新；不改这些选项原有领土／独立结果|
|G/common/journal_entries/00_meiji_restoration.txt:26–42、71–75、156–175|bakufu退出/天皇复位、Meiji主JE及奖励与新政治日志重叠|新政策状态明确禁止原版同功能入口；已有活动JE须显式关闭/迁移成果，不能只改possible。原文件的on_invalid会设restoration_complete并删emperor_var，不能借它无区别完成JIM迁移|
|G/common/scripted_effects/00_sgui_effects.txt:2–76|UI/JE刷新先删emperor_var；无特质天皇时生成backup且非bakufu时强设ruler|不要让新JIM日志用原版Meiji widget/update；自用精确对象字段，并处理对象死亡。原版GUI依赖也必须一起替换|
|G/events/meiji_restoration.txt:75–122 → `country_clear_daimyo`；G/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2015–2022|设global japan_daimyo_abolished，遍历every_character清所有大名，影响三国、流亡者和MOD模板|为三国改革新增country-scoped效果，every_scope_character→character_clear_daimyo_status（原生低层清理2090起）并写本国完成标记；绝不调用global wrapper。防旧原版JE继续到达meiji.1|
|G/events/meiji_restoration.txt:345–377，G/common/interest_groups/00_armed_forces.txt:134–142|meiji.3写global fall_of_the_samurai_global_var；日文化国家IG初始化读此global|新军制完成只写country成果和本国IG；迁移已有global不能清零，因为其他国家原先真实改革已发生。新国IG身份应按本国阶段适配|
|M/events/flavorJAP_ce.txt:120–126、183–235、332–338、395–445|1840秀治→秀明、1846秀明→秀和/平胜既有作者剧情；option会set_ruler并kill旧君主|新主议程在各option实际结算后接刷新/记录；不提前按年份生成。trigger和option effect要重验政权身份/actor仍owner，不让延迟选项覆盖已迁移或已亡的君主|

此处“接缝”指实际函数/调用位置，不假定`INJECT:`在所有数据库支持覆盖嵌套条件。工程内已有scripted_effect `REPLACE:`实例，可对小函数受控包裹；若使用数据库注入，应另查加载语义，不能用两个同名invalid块指望OR。不要复制整个00_code_on_actions文件。

## 6. 必须覆盖的外部验证和未证边界

外部检查：新分封和恢复两入口均JIM双主流；旧Lin在USM／JAP ruler／JIM非ruler／JIM ruler四阶段；准确JAP接任人已死／流亡／第三国；JIM天皇为现ruler或已改制；Lin与天皇各自先死亡；双方独立／换宗主；每一步中断重读；旧office清理不删新commission；同一人物无第二create；原生bakufu退出不劫持交接；原版JE旧入口关闭且不重复奖励。

源码明确证明所有基础effects/roles和原版调用形状；没有本轮引擎证据证明完整迁移事务、country继承时角色列表/auto-heir生成先后、幼主callback顺序或天皇role+heir在UI的组合显示。保留ENGINE_NOT_RUN。本轮不得为这些未决点打开游戏；用户按冻结候选定向测试。
