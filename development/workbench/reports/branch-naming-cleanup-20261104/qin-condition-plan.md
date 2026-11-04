# 西秦条件展示审查方案

状态：PLAN_ONLY。实际配置 gpt-6.1-sol / medium。仅读源码；未修改MOD、未测试候选、未开游戏。目录索引核验 1.13.11 / build 24799966，CURRENT，changed_count=0。

## 根因与边界

截图直接来自 `common/journal_entries/nesnd_qe1_agendas.txt:20`：complete虽已补TT，fail仍裸露num_states、agenda_started、agenda_clock，NOR胜利递归展开edge/wait/balance。所有七个JE均已纳入：agenda/economy/army/court/unity/uprising/recovery；挂载5个议程按钮、7个朝议按钮、2个共享团结按钮，以及6个进度条。仅修展示，不改逻辑、数值、周期、AI资格、生命周期与visible/possible分工。

## 当前原版完整链条

- `GAME/common/journal_entries/00_meiji_restoration.txt:68,79-107,123-155`：初始化restoration_timer_var→月度条件计时/重置→complete中单项TT包计时，其他法律/内战条件仍原生→on_complete事件与永久标记。秦可借其“变量计时单项TT”，但秦是29日到期标记，不能照搬按月变量数值。
- 原生计时文案 `GAME/localization/english/ep2_04_l_english.yml:44`，与JE的at_least_six_months_tt调用相连；原生标题同文件18-21行。
- `GAME/common/journal_entries/00_meiji_restoration.txt:640-719`：JE挂载按钮、完整complete/fail/timeout及hidden_trigger内部完成记账；不能借其hidden块隐藏秦玩家真实期限。
- `GAME/common/scripted_buttons/07_japan_buttons.txt:378-419`：visible/possible/selected→独立建院flag与使用次数TT→effect加次数/调用事件；`GAME/localization/english/ep2_02_l_english.yml:170-171`定义两个独立条件。秦用相同单项包装，不总包军政门槛。
- `GAME/common/scripted_buttons/00_balkan_wars_buttons.txt:100-119`：关系/国家等级等原生条件与hidden内部接纳/防重复标记分离。
- 数据库声明 `GAME/common/journal_entries/journal_entries.md`、`GAME/common/scripted_buttons/scripted_buttons.md`；界面消费 `GAME/gui/journal_entry.gui:179,188-189,215-235,742,832,875-876`，分别timeout/status/button/reason/complete/fail。未发现invalid被同一窗口固定直接渲染的证明，仍审查其闭包以免失效详情或嵌套引用泄漏。
- 实际资源图标引用 `gfx/interface/icons/invention_icons/egalitarianism.dds`沿用；原生UI不需要新增GUI或资源。这里只证明当前源链，未证明候选实机显示。

## 原稿对读

作者备份 `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\pre-update-20261030T233944Z\mod\localization\simp_chinese\replace\ce_french_empire_journals_l_simp_chinese.yml`；SHA-256 `352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844`。

|作者原文|候选类型|决定|
|---|---|---|
|第2行“统治者成年且非摄政”|“尚未奖掖其他派系。”|采用对象/状态直述，不写变量名。|
|第6行“稳定度进度条 >= 950”|“势力平衡点达到−50。”|保留可判定数值，改用自然中文；不把门槛写成剧情。|
|第7行“王朝稳定度 <= 50”|“羌种暴动达到100。”|保留指标与阈值；实际是完成坏结果，不擅改为失败。|

以上条件候选为编辑提案，未接入游戏。作者第29行含“国家拥有…变量”是已存在反例，受本轮明确要求约束，不沿袭。秦现有叙事与状态后续稿来源不能冒称原作者。

## 逐项候选与结构

### A01 · common/journal_entries/nesnd_qe1_agendas.txt:20

原逻辑：`num_states >= 4`

中文候选：拥有至少4个地区。

英文候选：Owns at least 4 states.

结构：本机num_states比较显示缺键；复用/迁移nesnd_sweep_four_states为秦议题所有键。仅包装这一项，不全球伪造num_states_greater_or_equal。complete/possible/inactive/invalid对应反向均覆盖。

### A02 · common/journal_entries/nesnd_qe1_agendas.txt:20

原逻辑：`has_variable=agenda_started AND NOT has_variable=agenda_clock`

中文候选：朝议的十年期限已届满。

英文候选：The ten-year deadline for the court debate has expired.

结构：started是纯存在性守卫，hidden_trigger；NOT clock放单项TT。clock由start_agenda_clock一次设置years=10；不改原生timeout=3650，两条出口原样保留。

### A03 · common/scripted_triggers/nesnd_qe1_campaign.txt:18

原逻辑：`balance exists AND econ_edge AND NOT econ_wait AND balance<=-50`

中文候选：势力平衡点达到−50。 / 安国派在这一端连续维持29天。

英文候选：The balance of power has reached −50. / The reformers have held this endpoint for 29 consecutive days.

结构：complete的OR内安国分支分为两项TT：阈值和持续时间；balance存在性hidden。持续时间TT内部保持edge AND NOT wait，不得只NOT wait。现有“四周”改精确29天，仅改文案。

### A04 · common/scripted_triggers/nesnd_qe1_campaign.txt:19

原逻辑：`balance exists AND army_edge AND NOT army_wait AND balance>=50`

中文候选：势力平衡点达到＋50。 / 统治派在这一端连续维持29天。

英文候选：The balance of power has reached +50. / The military faction has held this endpoint for 29 consecutive days.

结构：与A03对称；保留AND/OR。fail中的NOR保留两种胜利各自的否定，可每种胜利单独一项TT，文案分别为安国派尚未在−50连续维持29天／统治派尚未在＋50连续维持29天；不可把整段fail包成一个笼统失败TT。

### A05 · common/scripted_triggers/nesnd_qe1_campaign.txt:2

原逻辑：`country AND num_states>=4 AND NOT agenda_done`

中文候选：朝议尚未结束。

英文候选：The court debate has not ended.

结构：NOT done是已结束语义，单项TT；identity内部exists c:QE1检查hidden，国家身份/存续用原生可读条件或专属identity单项TT。live在展示时保留has_journal_entry的原生名字。

### A06 · common/scripted_triggers/nesnd_qe1_campaign.txt:20

原逻辑：`country AND num_states>=5 AND NOT court_archived AND NOR(universal_suffrage,council_republic)`

中文候选：拥有至少5个地区。 / 伊犁的朝议尚未结束。

英文候选：Owns at least 5 states. / The court politics of Ili have not ended.

结构：数量单项TT；归档单项TT；两条法律用原生NOR显示；invalid严格用原有NOT eligible，或等价OR反向逐项，不能把法律条件hidden。

### A07 · common/scripted_triggers/nesnd_qe1_campaign.txt:21

原逻辑：`country AND NOT dissolved`

中文候选：西秦尚未解体。

英文候选：Western Qin has not dissolved.

结构：dissolved是世界状态，单项TT；非纯记账不能全hidden。用于unity JE和uprising live/complete/invalid。

### A08 · common/scripted_triggers/nesnd_qe1_campaign.txt:22

原逻辑：`country AND NOT recovery_done`

中文候选：恢复故土尚未完成或结束。

英文候选：The recovery of the homeland has not concluded.

结构：done也可能由on_invalid写入；不可只称已经获得奖励。TT用concluded或“结束”；on_complete reward_pending保持隐藏执行。

### A09 · common/scripted_triggers/nesnd_qe1_campaign.txt:31-37

原逻辑：`court_eligible AND court_opened / recovery_eligible AND recovery_opened`

中文候选：朝议已告一段落。 / 朝议已告一段落，或已恢复河西、甘肃、西安、陕北中的任一整片地区。

英文候选：The opening court debate has concluded. / The court debate has concluded, or Qin or a subject controls all of Hexi, Gansu, Xi’an or Shaanbei.

结构：opened为持久解锁，旧档可由已经活动JE补登记；只给opened单项TT“伊犁的朝议已开启／恢复故土已开启”，正文或目标提示另解释首次解锁来源。不可用实时条件取代持久opened导致已解锁内容回锁。上列两句是首次规则解释，不冒充opened的即时真值。

### A10 · common/journal_entries/nesnd_qe1_identity.txt:32-43

原逻辑：`unity_live AND uprising_awakened; completion guarded uprising>=100`

中文候选：地方反抗已经兴起。 / 羌种暴动达到100。

英文候选：Local resistance has emerged. / The uprising has reached 100.

结构：awakened单项TT；uprising>=100单项TT，has_variable guard hidden且trigger_else仍false；unity_live展开可读的identity/dissolved/JE名。该complete为坏结果，不改为fail。

### A11 · common/scripted_triggers/nesnd_qe1_campaign.txt:23-28

原逻辑：`country_or_subject_owns_entire_state_region=HEXI,GANSU,XIAN,SHAANBEI`

中文候选：本国或属国控制河西、甘肃、西安、陕北的完整地区（逐项显示）。

英文候选：Qin or a subject controls the whole of Hexi, Gansu, Xi’an and Shaanbei (separate conditions).

结构：保持4个原生territorial trigger，不自定义合并勾叉。恢复故土领取/结束标记只在执行hidden。

### B01 · common/scripted_buttons/nesnd_qe1_agendas.txt:1,11,36

原逻辑：`NOT law_push_cooldown / economy_push_cooldown / military_budget_cooldown`

中文候选：过去六个月未曾责令议法。 / 过去六个月未曾裁军兴业。 / 过去六个月未曾拨给军府预备金。

英文候选：Has not ordered a legislative push in the past 6 months. / Has not backed the reform agenda in the past 6 months. / Has not allocated military reserves in the past 6 months.

结构：三键各自possible的hidden冷却改为对应单项TT；effect内部原守卫保留hidden。保留AI财力等限定在AI，不新增玩家国库门槛。

### B02 · common/scripted_buttons/nesnd_qe1_agendas.txt:24,30

原逻辑：`NOT army_petition_cooldown / NOT economy_petition_cooldown`

中文候选：过去十二个月未曾呈报边功。 / 过去十二个月未曾呈报新政。

英文候选：Has not reported frontier victories in the past 12 months. / Has not presented the reforms in the past 12 months.

结构：分别单项TT，与ready原生法律/建筑/疆土条件分开。

### B03 · common/scripted_triggers/nesnd_qe1_campaign.txt:4-10

原逻辑：`commercialized_agriculture; laissez_faire; wealth_voting; tools>=20; railway>=10`

中文候选：三项法律；全国工具工场至少20级；全国铁路至少10级。

英文候选：Three laws; at least 20 levels of tooling workshops nationally; at least 10 levels of railways nationally.

结构：全部保留原生trigger逐项勾叉，不重译法律名字、不用TT包全部经济资格。

### B04 · common/scripted_triggers/nesnd_qe1_campaign.txt:11-17

原逻辑：`goal exists AND snapshot_done; barracks>=goal; OR Punjab/Sindh/Gujarat; PER subject; OR Astrakhan/Ufa/Tobolsk`

中文候选：兵营总等级比朝议开始时增加至少25级。 / 波斯是本国属国。

英文候选：Total barracks levels are at least 25 above the opening baseline. / Persia is our subject.

结构：snapshot/goal存在性hidden；兵营原生country_has_building_type_levels动态goal优先保留，若实际UI仍泄漏var则仅该条TT包装固定规则25。不能写死107，goal由实际baseline+25。两个疆土OR原生保留。PER存在性hidden，subject条件原生显示；PER缺失分支单项TT“波斯仍须是本国属国”且always=no，不能无意允许PER不存在。

### B05 · common/scripted_buttons/nesnd_qe1_court.txt:1,7,13

原逻辑：`no_patronage = NOR(patron_crown,patron_literati,patron_army)`

中文候选：尚未奖掖其他派系。

英文候选：No faction is currently receiving patronage.

结构：真实互斥资格改为单项TT，不继续纯hidden；三方奖掖按钮visible保持40%门槛，不变更为possible。

### B06 · common/scripted_triggers/nesnd_qe1_court.txt:3-8

原逻辑：`power_* exists AND >=40 / >=60`

中文候选：皇权／地方士人／军府的势力比重达到40%（奖掖）或60%（接掌中枢）。

英文候选：The Crown / literati / army controls at least 40% (patronage) or 60% (taking power).

结构：visible条件不自动展开，状态说明可以用短句解释当前存在的行动；若在可用条件引用，则每方每阈值单项TT，guard hidden。不要为解释而移动visible到possible，避免改变按钮集合。

### B07 · common/scripted_buttons/nesnd_qe1_court.txt:24,30,36

原逻辑：`NOT peaceful_coup_cooldown`

中文候选：过去五年未曾发动此类政变。

英文候选：No such change of government has taken place in the past 5 years.

结构：三按钮共用同一条件TT，对应共享锁；技术与指令经济禁令保留原生勾叉；不能只在effect承诺五年后可用却隐藏禁用原因。

### B08 · common/scripted_buttons/nesnd_qe1_court.txt:19

原逻辑：`NOT no_patronage; possible always=yes`

中文候选：撤回当前奖掖。

英文候选：Withdraw current patronage.

结构：visible只筛选当前是否存在奖掖，effect已有语义TT；没有额外条件无需新TT。

### B09 · common/scripted_buttons/nesnd_unity_policies.txt:6-8,29-31

原逻辑：`policy_live hidden AND NOT material_active/political_active TT`

中文候选：现行补贴期已结束，且没有同类补贴生效。

英文候选：The current subsidy term has ended and no matching subsidy remains active.

结构：共享按钮已有单项available TT与12个月term，不另加秦专用覆盖。纳入有效键/引用审计，保留variable OR modifier防重复。修改共享键若有必要由unity议题所有者统一。

### C01 · common/journal_entries/nesnd_qe1_agendas.txt:28-31; nesnd_qe1_identity.txt:16-25

原逻辑：`balance<-10/>10; unity<25/<50 guarded`

中文候选：沿用当前安国／军府／争论三状态及团结度三状态。

英文候选：Retain the existing three agenda states and three cohesion states.

结构：status_desc内部trigger只选择已写desc，不直接显示变量条件。现有文案保留；本轮不把数值/计时说明塞进状态。若缺值保护有独立错误证据，另报逻辑BUG而不夹带改变。

### C02 · common/scripted_progress_bars/nesnd_qe1_agendas.txt; nesnd_qe1_identity.txt; nesnd_qe1_court.txt

原逻辑：`bar add/subtract desc; numeric values; nested if used for contribution selection`

中文候选：沿用已命名的进度来源、法组名与当前读数。

英文候选：Retain named progress sources, law-group labels and current values.

结构：进度明细显示desc与值，不将if/has_variable原样当条件树；本轮不改公式/周期/写入者。全量key闭包含3个权力条、团结、暴动、平衡条，防迁移丢引用。

## 文件与命名所有权

可编辑边界仅QE1三组trigger、四个JE文件及两组button脚本。是否采用共享helper由主Astra最终裁定。effects、values、bars以只读证明逻辑为主，不需要为展示改写；共享unity按钮当前已满足单项条件展示，不把其多国条件改成秦专用。

新候选键统一 `nesnd_qe1_condition_*`，归秦议题所有。可暂定非zz的 `localization/{simp_chinese,english}/replace/nesnd_qe1_conditions_l_<language>.yml`；若本轮统一归并到秦topic，则直接写topic所有文件，不新建平行覆盖。所有既存zz文件不在本子任务修改范围，父代理拥有去重/最终落点。`nesnd_sweep_four_states/economic_victory/military_victory`现由bug_sweep拥有，应迁秦topic或由topic复用并移除重定义；共享unity_*保留unity topic。

## 回归入口（仅计划，未执行）

- Compare original and candidate condition ASTs after stripping presentation wrappers; preserve trigger_if branches, default false, NOT/NOR grouping, timeout=3650 and years=10 separately.
- Enumerate complete/fail branch: missing balance; ±49/±50; edge missing/present; wait missing/present; clock active/expired; started missing/present; states=3/4. Do not run these before parent authorizes implementation/testing.
- Crown eligibility states=4/5, universal_suffrage/council_republic, archived, opened old-save flags.
- Barracks snapshot missing/pending/done; baseline+24/+25; PER missing/independent/subject; each territory OR; no hardcoded 107.
- Button cooldown active/expired at 6/12/60 months; existing patronage none/each; native legal/technology blockers each independently shown.
- Effective Chinese/English localization key uniqueness, references, BOM, dynamic scope safety, no raw country_var_ or num_states comparison placeholder in proposed displays.
- When game testing is allowed: one QE1 JE screen complete/fail/invalid and every scripted-button tooltip; verify both languages, old save timer and new initialized save. No repeated start/reload for already established behavior.

## 保留的不确定性

1. 29天由当前set_variable days=29证实；只可承诺原脚本计时/检查契约，实际周脉冲离开端点何时清除及到期何日被JE检查仍须引擎验证，不把静态“连续29天”视为已实测。
2. num_states在截图缺引擎本地化，因此该统计单项TT有必要；不得为了更多原生条件改成any_scope_state count而改变统计语义。
3. 原生动态goal兵营触发器显示是否能解析国家变量尚未实测；优先原生，若泄漏仅包该项，并将snapshot guard隐藏。
4. 游戏中inactive/invalid可见面板与NOT内部TT的否定排版需要一次定向显示验收。失败/完成不能仅以error.log无新增来认证。
5. 本轮仅报告与源码指纹在WORK，MOD没有由本代理写入。

补充原版下游核对：`GAME/events/meiji_restoration.txt:4-55` 的meiji.1保存皇帝上下文并加入je_meiji_main；`GAME/events/japan_events/ep2_hokkaido_events.txt:446-500` 的hokkaido_events.3保存州scope并在选项提供原生modifier。秦条件展示不引入它们的DLC/人物/视频资源。原生10份文件SHA见JSON。`scripted_buttons.md`的AI例子已过时，实际代码优先；本审查不改AI。
