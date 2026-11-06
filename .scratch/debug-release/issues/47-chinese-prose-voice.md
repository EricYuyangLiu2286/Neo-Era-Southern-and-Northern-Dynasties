Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Blocked by: none
Assignee: root
Validation: STATIC_PASS（逐键比对动态代码、数字、颜色；BOM、语言头、键集合、无重复键）。未启动游戏。
Evidence: development/evidence/chinese-prose-voice-20261106/

# 47 中文代理文本去平衡腔（2026-11-06）

第一步统计见下文；用户确认后的第二步结果见文末 `## Comments` 与 `## Result`。

## 范围与来源

- 作者原作：Git 标签 `original-20261030`，提交 `f18b6c45525351f5bf1a86ab29cccff9fee49500`（即写作技能所称 `f18b6c4`），`localization/simp_chinese/` 下 25 个文件、3,425 键。
- 原版中文：本云端环境没有游戏安装。改用公开的原版文件镜像 `tjysdsg/Victoria-3-files@0e8b625`（2025-06-23）中的 `game/localization/simp_chinese`，129 个文件、76,937 键。版本早于当前 1.15，只用来计词频，不作文风参照，也不进仓库。
- 当前文本：工作树 `localization/simp_chinese/` 共 89 个文件、7,345 键，没有重复键。
- 判定代理文本：同一键在标签中不存在，或内容不同。仅标点不同（7 键）算作者原文。
- 统计只算“叙事条目”：去掉 `[...]`、`$...$`、`#x ...#!` 等代码后至少 12 个汉字。代理一侧再排除名称、进度条读数和机制提示，避免模板重复冲高计数。
- 作者原作的叙事条目只有 436 条、29,885 字，样本偏小。每万字频率仅供发现异常，不作配额。
- 写作技能要求 GPT-6 Astra 等指定模型分工。本环境没有这些模型，第一步统计和下方改稿样例由本会话代理完成，没有子代理参与。`C:/` 路径下的技能原件无法访问，改读仓库内副本 `development/nesnd-player-writing/` 与 `development/nesnd-skill/references/author-prose-profile.md`。
- `docs/agents/STATUS.md` 在仓库中不存在，第二步交付时需要用户指明位置或同意新建。

## 不改的键（保护清单）

|类别|键数|依据|
|---|---:|---|
|与原作逐字相同|3,341|标签比对|
|与原作仅差标点|7|标签比对；属作者文本|
|作者改稿，当前仍是作者版|49|`development/workbench/reports/canon-prose-20261102/author-revision-original.txt`（作者 11-02 改稿）、提交 `be56496`（作者本机改稿）、PHI 审查“作者改稿整段保留”的 `nesnd_american_restoration.2.d`、含作者指定措辞的 `nesnd_khanate_suppression_failed_tt` 与 `nesnd_ui_khanate_campaign_ended_tt`|
|作者改稿后又被代理改动|34|同上来源；当前值与作者改稿不同。默认不改，见待确认 3|
|印度文件|216|任务45记录作者本机主 MOD 有未上传的改稿，本仓库看不到差异。默认整份不改，见待确认 1|
|`nesnd_qin_persia_l_simp_chinese.yml`|18|`journal-war-feedback-20261103/main-merge.json` 记为 `preserved_preexisting_author_files`，归属不明。见待确认 2|
|名称类（国名、州名、人名、地名、外交博弈名）|—|不改名词与既定译名|
|机制提示、进度条读数|—|只有带开发口吻的 23 条列入|

## 1. 代理文本高频而作者原作与原版少见的词与句式（前 30）

语料（去掉动态代码后的汉字数）：代理叙事 57,487 字 / 1,104 条；作者原作 29,885 字 / 436 条；原版 435,451 字 / 11,416 条。每格为“出现次数（每万字）”。按“代理频率 ÷ 较高一方频率 × √代理次数”排序；“已经”“处置/处理”在原版里本来常见，换成用户点名的“补述代价”和“既……也”。

|#|词或句式|代理|作者原作|原版|代理命中键数|代理例键|
|---:|---|---:|---:|---:|---:|---|
|1|经营（“继续经营共同市场”“依旧例经营”以外）|83（14.4）|1（0.3）|8（0.2）|76|`nesnd_external_end_desc`、`nesnd_tenasserim_recovery_reason`、`nesnd_ten_build_button_desc`|
|2|也须／仍须／还须／须先|64（11.1）|0（0.0）|10（0.2）|62|`nesnd_external_sha_desc`、`nesnd_external_bur_desc`、`nesnd_external_gbr_desc`|
|3|本国（泛称自指）|126（21.9）|2（0.7）|13（0.3）|114|`nesnd_external_qe1_desc`、`nesnd_external_bur_desc`、`nesnd_external_gbr_desc`|
|4|安排|92（16.0）|1（0.3）|25（0.6）|90|`nesnd_external_mug_desc`、`nesnd_ten_status_jobs`、`nesnd_ten_tenant_button_desc`|
|5|原有／现有／既有|97（16.9）|2（0.7）|27（0.6）|96|`nesnd_external_bur_desc`、`nesnd_external_policy_reason`、`nesnd_external_cancel_request_desc`|
|6|地方（泛称；不含“地方失序”“地方官”“地方自治”）|307（53.4）|12（4.0）|126（2.9）|250|`nesnd_tenasserim_recovery_reason`、`nesnd_ten_abolish_button_desc`、`nesnd_ten_dismiss_button_desc`|
|7|往来|45（7.8）|1（0.3）|4（0.1）|44|`nesnd_external_fra_desc`、`nesnd_external_qe1_desc`、`nesnd_external_sha_desc`|
|8|承担|69（12.0）|0（0.0）|29（0.7）|67|`nesnd_external_hus_desc`、`nesnd_external_end_desc`、`nesnd_jp_nation_reason`|
|9|争取|68（11.8）|0（0.0）|32（0.7）|67|`nesnd_external_gbr_desc`、`nesnd_external_rus_desc`、`nesnd_ten_compromise_button_desc`|
|10|朝廷（泛称主语）|112（19.5）|5（1.7）|4（0.1）|100|`nesnd_external_bur_desc`、`nesnd_external_rus_desc`、`nesnd_japan_war_collapse_reason`|
|11|共同（“共同市场”以外）|105（18.3）|2（0.7）|67（1.5）|94|`nesnd_per_civil_journal_reason`、`nesnd_per.1.d`、`nesnd_japan.5.d`|
|12|仍（仍在／仍然／仍须）|197（34.3）|12（4.0）|152（3.5）|182|`nesnd_external_fra_desc`、`nesnd_external_mug_desc`、`nesnd_external_gbr_desc`|
|13|答复|25（4.3）|0（0.0）|9（0.2）|24|`nesnd_external_status_await_partner`、`nesnd_wu_eastern_question_status_offer`、`nesnd_japan.1.d`|
|14|由谁／听谁／归谁（设问罗列）|24（4.2）|0（0.0）|3（0.1）|22|`nesnd_jp_politics_reason`、`nesnd_jp_nation_reason`、`nesnd_jp_korea_reason`|
|15|生计|23（4.0）|0（0.0）|4（0.1）|21|`nesnd_ten_status_sampling`、`nesnd_ten_tenant_button_desc`、`nesnd_ten_reopen_desc`|
|16|两国／双方（对称叙述）|76（13.2）|3（1.0）|68（1.6）|68|`nesnd_external_money_desc`、`nesnd_external_end_no_partner_desc`、`nesnd_external_status_signed_partner`|
|17|须决定／须判断／须衡量／须考虑（把问题抛给玩家）|27（4.7）|1（0.3）|16（0.4）|27|`nesnd_external_hus_desc`、`nesnd_external_fra_desc`、`nesnd_external_qe1_desc`|
|18|若……则／便|25（4.3）|1（0.3）|1（0.0）|25|`nesnd_supply_status_stable`、`flavorCNE.6.d`、`nesnd_jp_consumer_goods_reason`|
|19|事务|47（8.2）|2（0.7）|49（1.1）|45|`nesnd_supply_status_jobs`、`flavorCNE.7.d`、`nesnd_japan.4.d`|
|20|也有人／有人主张（各方并陈）|14（2.4）|0（0.0）|6（0.1）|13|`nesnd_external_sha_desc`、`nesnd_south_holdout_campaign_reason`、`kazakhstan_events.1.f`|
|21|维持|83（14.4）|4（1.3）|130（3.0）|79|`nesnd_external_sha_desc`、`nesnd_supply_preparations_reason`、`nesnd_supply_status_jobs`|
|22|有了（“……有了新的……”）|44（7.7）|3（1.0）|56（1.3）|39|`nesnd_tenasserim.2.d`、`nesnd_jp_cash_crops_reason`、`nesnd_jp_development.1.d`|
|23|政府（泛称主语）|239（41.6）|16（5.4）|750（17.2）|217|`nesnd_external_hus_desc`、`nesnd_external_fra_desc`、`nesnd_external_sha_desc`|
|24|各自|19（3.3）|0（0.0）|17（0.4）|18|`nesnd_external_end_no_partner_desc`、`nesnd_supply.2.d`、`nesnd_jp_cohesion_reason`|
|25|等候／等待……决定或答复（段尾交给统治者）|12（2.1）|0（0.0）|1（0.0）|12|`nesnd_external_status_await_partner`、`nesnd_wu_eastern_question_status_offer`、`nesnd_japan.1.d`|
|26|却（转折）|125（21.7）|22（7.4）|110（2.5）|121|`nesnd_external_hus_desc`、`nesnd_ten_train_button_desc`、`nesnd_ten_compromise_button_desc`|
|27|如今|74（12.9）|12（4.0）|43（1.0）|73|`nesnd_external_hus_desc`、`nesnd_external_gbr_desc`、`nesnd_external_end_no_partner_desc`|
|28|关系着／关系到（段尾总括）|10（1.7）|0（0.0）|0（0.0）|10|`nesnd_jp_politics_reason`、`nesnd_jp_islands_reason`、`nesnd_jp_foreign_reason`|
|29|“，……也须／也要／也将……”补述（每说一个好处就补一个代价）|84（14.6）|17（5.7）|143（3.3）|84|`nesnd_tenasserim.2.d`、`nesnd_japan_war_collapse_status`、`nesnd_xiangyang_camp_journal_reason`|
|30|既……也／又|22（3.8）|2（0.7）|43（1.0）|22|`nesnd_xiangyang_camp_journal_reason`、`nesnd_supply_preparations_reason`、`nesnd_ottoman_recovery_reason`|

用户点名的已知例子，当前计数：

|句式|代理|作者原作|原版|代理例键|
|---|---:|---:|---:|---|
|然而……（并）不能／无法|1（0.2）|0（0.0）|4（0.1）|`nesnd_cne_land_journal_reason`|
|不是……而是|0（0.0）|3（1.0）|28（0.6）|—|
|在……之间|9（1.6）|4（1.3）|57（1.3）|`nesnd_supply.1.d`、`nesnd_ottoman_recovery_reason`、`nesnd_c2_usm_industry_reason`|
|相关|11（1.9）|6（2.0）|63（1.4）|`nesnd_jp_cohesion_reason`、`nesnd_c2_usm_constitution_practical_franchise_desc`、`nesnd_small_dispute_organised`|
|推进|4（0.7）|3（1.0）|74（1.7）|`nesnd_ten_status_working_hungry`、`nesnd_c2_usm_west_open`、`ai_strategy_nesnd_cne_land_and_schools_desc`|
|此项／本项／本次|4（0.7）|0（0.0）|6（0.1）|叙事字段内；机制提示另有 23 条开发口吻|

“然而……不能”“不是……而是”前几轮已基本清除，“相关”“推进”已回到作者水平。剩下的问题集中在三处：

1. **泛称主语**：地方、本国、政府、朝廷、双方。作者原文写的是具体的人和机构，如“川边乡校的讲习台到南京礼部的议会殿”“巡捕的警棍和判官的惊堂木”。
2. **抽象动词名词**：安排、承担、往来、争取、经营、维持、事务，常常一句里出现两三个。
3. **收尾套路**：段尾把问题交还玩家（“政府须决定与谁往来，又愿意为外交主张付出多少”）、“能否……关系着……”总括、好处后补一个义务（“……也须……”）、并列各方立场（“支持用兵的人称许……，受到搜捕的原住民却……”）。这些正是作者语体档案已经否定的“为平衡口气凭空加反对者”和“见一项成功就补一句失败可能”。

另有两类成批模板：
- 修正名“……的地方安排”有 24 个（`nesnd_civic_routes`，如“维持经学资格的地方安排”“商人融资的地方安排”）。
- 外交事务 `nesnd_external_*` 十余条按钮说明同一骨架：“局势→某方有利益→政府须决定与谁往来、愿意付出多少资金与军械”。

## 2. 按文件统计受影响的键数

“叙事字段”指事件正文、选项、日志正文与状态、按钮说明、修正名与说明、通知、标题等，不含名称、进度条与机制提示。“命中”指含前 30 项中任一项。

|文件|键数|作者原文（含仅标点差异）|作者改稿（保护）|作者改稿后又被改|代理写或改|其中叙事字段|叙事字段命中前30项|机制提示带开发口吻|待确认文件的文本键|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|`replace/nesnd_india_l_simp_chinese.yml`|216|0|0|0|0|0|0|0|180|
|`replace/nesnd_civic_routes_l_simp_chinese.yml`|328|0|0|0|328|220|144|2|0|
|`replace/nesnd_japan_l_simp_chinese.yml`|256|0|1|0|255|199|94|0|0|
|`replace/nesnd_civic_characters_l_simp_chinese.yml`|201|0|0|0|201|165|76|0|0|
|`replace/nesnd_small_states_l_simp_chinese.yml`|216|0|0|0|216|137|72|8|0|
|`replace/nesnd_native_americas_l_simp_chinese.yml`|194|0|3|0|191|131|62|0|0|
|`replace/nesnd_south_politics_l_simp_chinese.yml`|237|0|1|3|233|104|50|1|0|
|`replace/nesnd_qin_politics_l_simp_chinese.yml`|179|0|0|0|179|130|42|0|0|
|`replace/nesnd_regional_native_restoration_l_simp_chinese.yml`|98|0|0|0|98|67|38|0|0|
|`replace/nesnd_regional_development_l_simp_chinese.yml`|61|0|0|0|61|58|28|0|0|
|`nesnd_external_l_simp_chinese.yml`|100|0|0|0|100|43|27|0|0|
|`replace/nesnd_persia_l_simp_chinese.yml`|174|0|0|0|174|75|27|0|0|
|`replace/nesnd_russian_frontiers_l_simp_chinese.yml`|37|0|0|0|37|34|25|0|0|
|`replace/nesnd_cne_land_reform_l_simp_chinese.yml`|294|0|4|8|282|168|25|2|0|
|`replace/nesnd_crisis_l_simp_chinese.yml`|82|0|39|17|26|42|24|0|0|
|`nesnd_supply_l_simp_chinese.yml`|63|0|0|0|63|36|23|2|0|
|`replace/nesnd_europe_america_l_simp_chinese.yml`|75|0|0|0|75|59|22|0|0|
|`replace/nesnd_phi_finance_l_simp_chinese.yml`|80|0|0|0|80|56|22|2|0|
|`replace/nesnd_egypt_l_simp_chinese.yml`|71|0|0|3|68|50|21|0|0|
|`nesnd_tenasserim_l_simp_chinese.yml`|44|0|0|0|44|28|19|2|0|
|`replace/nesnd_small_display_additions_l_simp_chinese.yml`|30|0|0|0|30|18|16|0|0|
|`replace/nesnd_journal_closures_l_simp_chinese.yml`|44|0|0|0|44|20|15|0|0|
|`replace/nesnd_hus_social_hierarchy_l_simp_chinese.yml`|117|0|0|0|117|68|14|0|0|
|`replace/ce_usm_events_l_simp_chinese.yml`|286|249|0|0|37|30|13|0|0|
|`replace/nesnd_diplomatic_negotiations_l_simp_chinese.yml`|75|0|1|0|74|25|11|1|0|
|`replace/nesnd_chen_security_l_simp_chinese.yml`|37|0|0|2|35|26|11|2|0|
|`replace/nesnd_ottoman_l_simp_chinese.yml`|120|0|0|0|120|39|9|0|0|
|`replace/nesnd_italian_undertaking_l_simp_chinese.yml`|15|0|0|0|15|9|8|1|0|
|`replace/nesnd_qin_persia_l_simp_chinese.yml`|18|0|0|0|0|0|0|0|8|
|`replace/nesnd_journal_tooltips_l_simp_chinese.yml`|13|0|0|0|13|12|7|0|0|
|`replace/nesnd_hus_road_projects_l_simp_chinese.yml`|35|0|0|0|35|17|7|0|0|
|`nesnd_war_collapse_l_simp_chinese.yml`|10|0|0|0|10|8|4|0|0|
|`replace/ce_cne_events_l_simp_chinese.yml`|125|119|0|1|5|4|4|0|0|
|`replace/nesnd_map_refinement_l_simp_chinese.yml`|8|0|0|0|8|4|4|0|0|
|`replace/nesnd_south_feedback_l_simp_chinese.yml`|4|0|0|0|4|4|3|0|0|
|`replace/nesnd_per_usm_mechanics_l_simp_chinese.yml`|10|0|0|0|10|8|3|0|0|
|`replace/nesnd_button_tooltips_l_simp_chinese.yml`|35|0|0|0|35|11|3|0|0|
|`replace/nesnd_usa_manifest_destiny_l_simp_chinese.yml`|4|0|0|0|4|4|2|0|0|
|`replace/nesnd_unity_policies_l_simp_chinese.yml`|18|0|0|0|18|7|2|0|0|
|`replace/ce_french_empire_journals_l_simp_chinese.yml`|254|240|0|0|14|11|2|0|0|
|`replace/nesnd_diaspora_l_simp_chinese.yml`|26|0|0|0|26|14|1|0|0|
|`replace/nesnd_court_followup_l_simp_chinese.yml`|4|0|0|0|4|2|1|0|0|
|`replace/nesnd_cne_reform_l_simp_chinese.yml`|5|0|0|0|5|5|1|0|0|
|`replace/nesnd_country_routes_l_simp_chinese.yml`|1|0|0|0|1|1|1|0|0|
|其余 29 个含代理键的文件（地名、名称、兼容键等，无命中）|2,608|2,303|0|0|305|41|0|0|0|
|**合计（全部 89 个文件）**|7,345|3,348|49|34|3,680|2,190|983|23|188|

另有 16 个文件与原作逐字相同或仅差标点，未单列，计入合计。逐键分类见 `development/evidence/chinese-prose-voice-20261106/step1-key-classification.json`，完整表见同目录 `tables.md`。

第二步实际要逐条重写的，是命中前 30 项的 983 条叙事键，加 23 条开发口吻提示。其余 1,207 条叙事键也要连读，但多数是短标题和短状态，预计改动不多。

## 3. 十条代表键改稿（未落库，仅供确认方向）

每条均已对照脚本：效果、条件、数字与动态代码不变（这十条原文都没有动态代码）。

### 日志正文

**作者同字段原文** `ce_usm_conflicts_within_reason`：
> 明朝朱姓，还是吴国郑氏？这对于中国南朝有能力参预政治的国人来说，是一个每分每秒都要自问的难题。从川边乡校的讲习台到南京礼部的议会殿。争论、札子、散文、报道，各式各样体裁的文字都在对人们呼喊。却是问多于答，争大于论。

**1. `nesnd_suppress_native_khanate_reason`**（`common/journal_entries/nesnd_native_khanate.txt:49`；吞并汗国则成功，汗国战事结束而未吞并则失败）

- 现稿：大平原的割地与人口迁移，已经改变了北美的力量分布。汗国凭原住民共同体的支持建立政府，试图把迁民、土地与地方武装联成新的国家。我们若任其立足，原有的领土主张便将越来越难维持。\n\n政府准备以吞并结束汗国的统治，新汗则希望迫使干涉者屈服，为草原盟约赢得威望。双方争夺的，既是这片国土，也是今后谁有权安排原住民的生活。
- 改稿：大平原割让之后，迁徙的部族涌进了草原。汗国借原住民共同体的支持立起政府，要把迁民、土地和各地武装拧成一个国家。任它扎下根来，我们对这片土地的主张便一年比一年站不住。\n\n我们要吞并汗国。新汗则想逼退干涉者，借一场胜利让草原盟约在各部之间立威。
- 问题：“已经改变了力量分布”是空泛总括；“政府”换成说话的“我们”；删去“既是……也是……”的收尾。那句收尾提出的“谁替原住民做主”，前文“立起政府”已经说到。

**2. `nesnd_jp_establish_toyotomi_reason`**（`common/journal_entries/nesnd_jp_establishment.txt:1`，c:JAP 即丰臣）

- 现稿：分封使丰臣旧臣失去了支配整个日本的地位，留在西部的军队与家臣却仍须供养。各地收入从哪里征收，谁来办理地方政务，都不能只靠旧日的威望维持。政府须在现有辖地建立可靠的行政机关，使城下町成为办事、征税与雇工的中心。
- 改稿：分封之后，丰臣家再也号令不了全日本。留在西国的军队和家臣却一个不少，都等着领禄米。年贡从哪里收，村町派谁去管，单凭旧日的威名已经办不成。丰臣政权须在现有领地上设起靠得住的奉行所，让城下町成为收税、办事和招工的地方。
- 问题：“仍须供养”“由谁征收”“政府须”三个套路连用；改成具体的禄米、年贡、奉行所，主语落到丰臣家。

### 事件正文

**作者同字段原文** `flavorCNE.4.d`：
> 地权革命是经济上的革新，同样也是一项冷酷的政治运动。它要将一整个旧社会窃夺数千年的利益，转移到诞生不过数十年的新贵手中。这一过程不仅仅是金钱赎买就能结束的，必然存在法律机关的追捕、诓骗、来回的争夺、执行者的背叛，甚至是残酷的暴力手段。……

**3. `nesnd_ming_court.3.d`**（`events/nesnd_ming_court.txt:5`，玩家转入行在国家后触发；唯一选项另有转移提示）

- 现稿：随驾臣僚已经抵达行在，地方政府正在安置朝廷。原有军队仍须征饷调兵，布政司仍须治理各地，如今又要供给天子的行朝。拥明的主张由此有了可以奉事的中央，也使接驾之地首先承担了同南府决裂的代价。\n\n各省与海外诸邦还在遣使往来。曾经在礼议院与内阁争执的名分，如今已须由彼此的军力担保。
- 改稿：随驾的臣僚到了行在，地方官忙着安顿朝廷。这里的营伍照旧要征饷调兵，布政司照旧要治理州县，如今又多出一座行朝要养。拥明的人总算有了可以奉事的天子；接驾的地方，也头一个同南府撕破了脸。\n\n各省与海外诸邦的使者还在路上。当年在礼议院与内阁里争的名分，往后要拿兵马来定。
- 问题：一段里有“仍须”两次、“如今”两次，还有“有了……也使……承担了……代价”的好处加代价对举。

**4. `nesnd_american_restoration.12.d`**（`events/nesnd_american_restoration.txt:82`，合并请求被拒）

- 现稿：印卡宫廷拒绝了合并的请求。王朝的共同传统可以使双方相互接近，却不足以让现有的统治者接受同一国家的安排。\n\n政府须继续处理本国的土地与地方政治，不能把这些责任都寄于宫廷的答复。经过等待期，双方仍可重新商谈。
- 改稿：印卡宫廷回绝了合并。两家同奉一个王朝的传统，彼此可以论亲，却谁也不肯让出自己的君位和朝堂。\n\n村社的土地和地方上的纷争，还得我们自己料理，指望不上宫廷的答复。等待期满后，可以再遣使商谈。
- 问题：“可以使……却不足以……”的平衡句；“政府须继续处理……不能寄于……”是替玩家下结论。

### 选项

**作者同字段原文**：`flavorCNE.4.1`“胡言乱语，正不必忧心。”；`flavorCNE.5.2`“彼等有何能耐？翻天了不成？”

**5. `nesnd_supply.1.b`**（拒绝商人联络，默认选项）
- 现稿：本国事务尚多，暂不接洽。
- 改稿：自家的事还没理清，顾不上替商人牵线。

**6. `nesnd_american_restoration.3.a`**（镇压复统派后的唯一选项，无效果）
- 现稿：军队已经出面，乡村却未必服从。
- 改稿：再有聚众的，照此办理。
- 问题：原选项替玩家预告后果，又补了一句代价。选项应是下令镇压的一方在说话。

### 按钮说明

**作者同字段原文**：`ce_french_republican_hit_economy_desc`“正义的事业总不缺支持者。”；`ce_french_support_dynasty_button_desc`“波拿巴的道路是[ROOT.GetCountry.GetAdjective]民族团结和繁荣的唯一办法。……”

**7. `nesnd_small_request_autonomy_desc`**（`common/scripted_buttons/nesnd_small_states.txt:45`；效果与条件由 `_tt` 和原生勾叉显示，不在说明里重复）
- 现稿：以地方已经具备的经济与行政能力为据，要求宗主允许本国自行处理更多事务。
- 改稿：我们自己收得上税，也有人手办理政务。宗主该把更多国事交还给我们了。
- 说明：这是小国通用按钮（缅甸、远南等），不用“衙门”“朝廷”等中国称谓。

**8. `nesnd_south_retry_confrontation_desc`**（`common/scripted_buttons/nesnd_south_accords.txt:51`；效果 `nesnd_open_southern_war` 发起 `dp_usm_civil_war` 外交博弈）
- 现稿：前次交涉未成，反对新朝的地方仍据地拥兵。再次提出交涉，要求他们就朝廷的统治权作出答复。
- 改稿：上回的交涉不了了之，不服新朝的地方至今拥兵自守。再向他们摊牌：认不认朝廷，给个准话。

### 修正名

**作者同字段原文**：`CNE_land_draft_debuff`“军功集团把握地权”；`ce_french_suppress_increase_police_spending`“特别警务补贴”；`CNE_post_landdraft_modifier`“投资狂热”。

**9. `nesnd_c2_usm_constitution_classical_franchise_local`**（州修正，`state_tax_capacity_mult = 0.10`，24个月；仅南朝礼法路线“维持经学资格”）
- 现稿：维持经学资格的地方安排
- 改稿：经学士人理财

**10. `nesnd_c2_local_administration`**（州修正，`state_tax_capacity_mult = 0.10`；公民路线通用，非中国国家也会用）
- 现稿：地方财政安排
- 改稿：税务协理
- 说明：同文件还有 24 个“……的地方安排”，第二步逐个按实际效果命名，避免换成另一套统一后缀。

## 待确认（第二步开始前）

1. **印度文件**：作者本机主 MOD 的 `nesnd_india_l_simp_chinese.yml` 有未上传改稿，本仓库看不到差异。请上传该文件，或说明哪些键可以改。没有回复则整份不改。
2. **`nesnd_qin_persia_l_simp_chinese.yml`**（8 条文本键）：记录写它是“合并前已存在的作者文件”，但内容与原作标签不同。它算作者文本还是代理文本？
3. **作者改稿后又被代理改动的 34 键**：默认不改。如需处理，建议按作者改稿还原后只修与脚本矛盾的句子。键名：`ce_cne_land_reform_reason`、`nesnd_federal_compact`、`nesnd_federal_compact_button`、`nesnd_federal_compact_button_desc`、`nesnd_egypt_investment_accounts_reason`、`nesnd_egypt_choose_cost`、`nesnd_egypt_none_effect`、`nesnd_crisis.30.b`、`nesnd_crisis.30.c`、`nesnd_crisis.30.d`、`nesnd_crisis.33.d`、`nesnd_crisis.31.d`、`nesnd_crisis.32.a`、`nesnd_crisis.32.d`、`nesnd_hna_veterans`、`nesnd_huguang_preparations_reason`、`nesnd_hna_academy_button_desc`、`nesnd_hna_supply_button_desc`、`nesnd_hna_veterans_button_desc`、`nesnd_crisis.10.d`、`nesnd_crisis.11.a`、`nesnd_crisis.11.d`、`nesnd_crisis.20.c`、`nesnd_crisis.20.d`、`nesnd_protect_chen_button`、`nesnd_protect_chen_button_desc`、`nesnd_land_survey`、`nesnd_land_survey_desc`、`nesnd_land_review`、`nesnd_land_review_desc`、`nesnd_land_military`、`nesnd_land_military_desc`、`nesnd_land_suspend`、`nesnd_land_suspend_desc`。其中 `ce_cne_land_reform_reason` 是作者原文后被追加了一句“要巩固地权革命的成果，政府可以推行……”，只可能改追加句。
4. **南朝内战事件 `usm_civilwar.*`（约 30 键）**：作者原作的选项有鲜明立场（“吴贼！狗贼！奸贼！恶贼！逆贼！”“新朝的乌纱帽好看吗？”“或许我们的时代还未到来……”）。11-02 的设定修订（提交 `1cb7b0c`）把它们改成了“维持中立，不作军事承诺。”这类平稳句；`canon-prose-20261102/usm-audit.md` 中对应条目的理由多为“统一本轮设定与名称”或“修复英文槽中的中文回退”，没有说明为什么要去掉原句的口气。按判定规则它们属于代理文本。建议：保留设定修订带来的事实变动（例如不再称“第二次靖难战争”），按作者原句的口气重写；能直接沿用的原句尽量沿用。
5. **标题和按钮名**：建议只在有开发口吻或成批模板时才改（如“……的地方安排”），其余短标题不动，以免改动既定名称。
6. **STATUS.md**：仓库中没有 `docs/agents/STATUS.md`。第二步交付时更新到哪里？

## 工具与复现

`development/evidence/chinese-prose-voice-20261106/tools/`：`corpus.py` 建三份语料，`report.py` 应用保护清单并统计，`render.py` 出表。原版语料不入库，复现时需另取原版中文本地化，传入 `corpus.py` 的第二个参数。工具只做统计和定位，不改写文本。

## Comments

2026-11-06 用户对“待确认”的答复：

1. 印度文件：作者不清楚本机有哪些改稿，直接改。
2. `nesnd_qin_persia_l_simp_chinese.yml`：都是变量名，不必改。本轮未动。
3. 南朝内战事件：按作者原句的口气重写，能沿用的原句尽量沿用。
4. 标题和按钮名：可以改。
5. STATUS.md：在仓库合适位置新建。已建于 `docs/agents/STATUS.md`。

“作者改稿后又被代理改动的 34 键”用户未作答复，按默认不改。

## Result

### 做法

- 逐文件读完范围内全部键（2,972 个，含标题、按钮名和印度文件），只改需要改的。每条手写，不做词语替换。工具只用于导出、按键写回和校验（`tools/locedit.py`）。
- 事实以脚本为准：改写前核对事件选项的使用方、按钮效果（如 `nesnd_open_southern_war` 发起 `dp_usm_civil_war`）、修正效果（`_politics` 为利益集团好感、`_local` 为州修正）。
- 每个文件改完连读，又统一回看一遍新出现的高频词（撑、还得、就此、自己……），换掉了 16 处重复。
- 上一轮审查记为“保留作者口吻”的键（PHI 驻屯日志正文、1.d、2.d 及其全部选项；原住民文件的若干选项）不改。过程中误改的 `nesnd_hus_registration.2.a`、`nesnd_american_restoration.12.a` 已恢复原样，最终无差异。
- 南朝内战：恢复了与现行设定不冲突的作者原句（1.1、1.2、1.3、2.2–2.5、3.t、3.1、10.t、10.1、10.2、23.1、23.3）。1.d、2.d、3.d、10.d、23.d、`flavorUSM.6.d`、`ce_usm_cw_japanese_interest_reason` 以作者原段为底，删去与分支冲突的固定事实（陈东阳遇刺、朱阔彬与天演帝的具体经过、日期代码），补回现行剧情事实。
- 波兰两条日志正文 `je_ce_polish_reconquest_reason`、`je_ce_polish_war_preparation_reason`：代理在作者原句后补了尾巴，已恢复作者原句。

### 改了多少键（按文件）

|文件|改动键数|
|---|---:|
|`replace/nesnd_civic_routes_l_simp_chinese.yml`|121|
|`replace/nesnd_japan_l_simp_chinese.yml`|48|
|`replace/nesnd_small_states_l_simp_chinese.yml`|34|
|`replace/ce_usm_events_l_simp_chinese.yml`|26|
|`replace/nesnd_south_politics_l_simp_chinese.yml`|25|
|`replace/nesnd_native_americas_l_simp_chinese.yml`|22|
|`replace/nesnd_journal_closures_l_simp_chinese.yml`|19|
|`nesnd_external_l_simp_chinese.yml`|18|
|`replace/nesnd_india_l_simp_chinese.yml`|12|
|`replace/nesnd_civic_characters_l_simp_chinese.yml`|11|
|`replace/nesnd_regional_development_l_simp_chinese.yml`|11|
|`replace/nesnd_regional_native_restoration_l_simp_chinese.yml`|9|
|`replace/nesnd_persia_l_simp_chinese.yml`|8|
|`replace/nesnd_diplomatic_negotiations_l_simp_chinese.yml`|7|
|`replace/nesnd_europe_america_l_simp_chinese.yml`|7|
|`replace/nesnd_phi_finance_l_simp_chinese.yml`|7|
|`replace/nesnd_small_display_additions_l_simp_chinese.yml`|7|
|`nesnd_supply_l_simp_chinese.yml`|6|
|`replace/nesnd_hus_social_hierarchy_l_simp_chinese.yml`|6|
|`replace/nesnd_egypt_l_simp_chinese.yml`|5|
|`replace/nesnd_qin_politics_l_simp_chinese.yml`|5|
|`replace/nesnd_cne_land_reform_l_simp_chinese.yml`|4|
|`replace/nesnd_crisis_l_simp_chinese.yml`|3|
|`replace/nesnd_ottoman_l_simp_chinese.yml`|3|
|`nesnd_tenasserim_l_simp_chinese.yml`|2|
|`replace/ce_cne_events_l_simp_chinese.yml`|2|
|`replace/ce_poland_l_simp_chinese.yml`|2|
|`replace/nesnd_russian_frontiers_l_simp_chinese.yml`|2|
|`replace/nesnd_unity_policies_l_simp_chinese.yml`|2|
|`replace/nesnd_usa_manifest_destiny_l_simp_chinese.yml`|2|
|`replace/nesnd_chen_security_l_simp_chinese.yml`|1|
|`replace/nesnd_cne_ai_agenda_l_simp_chinese.yml`|1|
|`replace/nesnd_per_usm_mechanics_l_simp_chinese.yml`|1|
|**合计（33 个文件）**|439|

前 30 项高频词与句式，在同一批叙事键上的改前／改后次数：

|词或句式|改前|改后|
|---|---:|---:|
|经营（共同市场/旧例以外）|91|53|
|也须／仍须／还须／须先|67|28|
|本国（泛称自指）|137|87|
|安排|144|69|
|原有／现有／既有|98|61|
|地方（泛称）|391|285|
|往来|50|31|
|承担|76|34|
|争取|72|45|
|朝廷（泛称主语）|119|100|
|共同（共同的/共同市场以外）|117|88|
|仍（仍在/仍然/仍须）|207|144|
|答复|33|26|
|由谁／听谁／归谁（设问罗列）|25|25|
|生计|25|20|
|两国／双方（对称叙述）|77|58|
|须决定／须判断／须衡量／须考虑（把问题抛给玩家）|27|6|
|若……则／便|25|14|
|事务|50|22|
|也有人／有人主张（各方并陈）|14|13|
|维持|91|48|
|有了（……有了新的……）|45|47|
|政府（泛称主语）|250|177|
|各自|21|14|
|等候／等待……决定或答复|16|12|
|却（转折）|126|115|
|如今|74|76|
|关系着／关系到|10|4|
|“，……也须/也要/也将……”补述|85|69|
|既……也／又|22|13|
|**合计**|2585|1784|

剩余次数多在状态行、机制条件，以及作者口吻文件（人物事件、PHI、内战原句），这些未强行改。

### 20 条改前／改后对照

**1. `nesnd_external_fra_desc`**（`nesnd_external_l_simp_chinese.yml`）
- 改前：南朝使者请求承认易代并延续旧约，印度方面则仍有南部海岸与殖民地的争执。法国商人、债权人与军官在两地都有利益。政府须决定与谁往来，又愿意为外交主张付出多少资金与军械。
- 改后：南朝使者请法国承认易代、延续旧约；印度那边，南部海岸与殖民地的争执还没有了结。两头都押着法国商人、债权人和军官的身家。

**2. `nesnd_c2_hus_frontier_reason`**（`replace/nesnd_civic_routes_l_simp_chinese.yml`）
- 改前：铁路和矿场向牧地伸展时，地图上的空白并非无人经过的土地。季节迁徙的牲畜要饮水，工程要用地，驻军要保障交通。牧民要求保留通道，开发者催促补偿征地，军方主张由驻军护持施工。每一种安排都将改变当地社会以后的生活基础。
- 改后：铁路和矿场伸进了牧地。地图上的空白，其实年年有畜群经过：牲畜要饮水，工程要用地，驻军要守路。牧民要求留出通道，开发者催着补偿征地，军方则主张派兵护持施工。

**3. `nesnd_c2_usm_constitution_classical_franchise_local`**（`replace/nesnd_civic_routes_l_simp_chinese.yml`）
- 改前：维持经学资格的地方安排
- 改后：经学士人理财

**4. `nesnd_c2_italy_foundations_public_works_politics`**（`replace/nesnd_civic_routes_l_simp_chinese.yml`）
- 改前：公共军需工程的支持与反对
- 改后：军方先拿到订单

**5. `nesnd_c2_hus_oil_oil_royalties_desc`**（`replace/nesnd_civic_routes_l_simp_chinese.yml`）
- 改前：支持油税留用于地方的主张，协助当地财政行政。
- 改后：油税留在当地，拿来修路办学。

**6. `nesnd_jp_establish_toyotomi_reason`**（`replace/nesnd_japan_l_simp_chinese.yml`）
- 改前：分封使丰臣旧臣失去了支配整个日本的地位，留在西部的军队与家臣却仍须供养。各地收入从哪里征收，谁来办理地方政务，都不能只靠旧日的威望维持。政府须在现有辖地建立可靠的行政机关，使城下町成为办事、征税与雇工的中心。
- 改后：分封之后，丰臣家再也号令不了全日本。留在西国的军队和家臣却一个不少，都等着领禄米。年贡从哪里收，村町派谁去管，单凭旧日的威名已经办不成。丰臣政权须在现有领地上设起靠得住的奉行所，让城下町成为收税、办事和招工的地方。

**7. `nesnd_jp_foreign.1.d2`**（`replace/nesnd_japan_l_simp_chinese.yml`）
- 改前：[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者要求结束藩属关系。他们希望从此自行决定外交、军队与通商事务，并以独立国家的身份同我们往来。这份答复将决定我们是否愿意交出原有的宗主权。
- 改后：[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者要求结束藩属关系。从今往后，外交、军队和通商都由他们自己作主，同我们以独立国家相待。

**8. `nesnd_cne_land_journal_reason`**（`replace/nesnd_cne_land_reform_l_simp_chinese.yml`）
- 改前：军功爵与地方宗族积累的田产，使许多农户世代依附于旧主。新法准许土地流转，也让经营农业的商人有了扩张的机会。然而，一纸买卖契约并不能使失去田地的人立即找到新的营生。田庄改作、雇工与迁居带来的争执，将伴随这场变革走进乡村。
- 改后：军功爵与地方宗族积累的田产，让许多农户世代依附旧主。新法准许土地流转，经营农业的商人也有了扩张的机会。可一纸买卖契约，变不出失地农民的新营生。田庄改作、雇工与迁居引起的争执，会跟着这场变革一路走进乡村。

**9. `nesnd_ming_court.3.d`**（`replace/nesnd_south_politics_l_simp_chinese.yml`）
- 改前：随驾臣僚已经抵达行在，地方政府正在安置朝廷。原有军队仍须征饷调兵，布政司仍须治理各地，如今又要供给天子的行朝。拥明的主张由此有了可以奉事的中央，也使接驾之地首先承担了同南府决裂的代价。 / 各省与海外诸邦还在遣使往来。曾经在礼议院与内阁争执的名分，如今已须由彼此的军力担保。
- 改后：随驾的臣僚到了行在，地方官忙着安顿朝廷。这里的营伍照旧要征饷调兵，布政司照旧要治理州县，如今又多出一座行朝要养。拥明的人总算有了可以奉事的天子；接驾的地方，也头一个同南府撕破了脸。 / 各省与海外诸邦的使者还在路上。当年在礼议院与内阁里争的名分，往后要拿兵马来定。

**10. `nesnd_south_accords.1.overseas`**（`replace/nesnd_south_politics_l_simp_chinese.yml`）
- 改前：南府使者请[ROOT.GetCountry.GetName]承认郑氏的新名位，并表示本国的政府、辖地与现有宗属安排均可延续。南朝内部如何以礼法重定君权和省权，将由其礼议院与内阁办理。我国与它的通商、港务和军费往来，仍须依各项条约行事。 / 郑氏需要海内外的支持。我们也应在作答以前想清楚，这次易代将给本国留下怎样的位置。
- 改后：南府使者请[ROOT.GetCountry.GetName]承认郑氏的新名位，并表示本国的政府、辖地与现有宗属安排均可延续。南朝内部如何以礼法重定君权和省权，将由其礼议院与内阁办理。我国与它的通商、港务和军费往来，仍须依各项条约行事。 / 郑氏要的，是海内外的支持。

**11. `nesnd_small_states.2.siam`**（`replace/nesnd_small_states_l_simp_chinese.yml`）
- 改前：曼谷与地方的生产已有了较为稳定的市场联系。人口与财源集中的地方，需要别处的出产。地方经营者也需要销路，才能付出工钱、承担税款。 / 这样的联系给政府增加了收入，也带来了分配收入的要求。军队需要供养，地方还要办学与办理公共事务。生产者为国家创造了财源，也会期待国家能回应自己的生活。
- 改后：曼谷和外府的买卖做稳了。都城人多钱多，要外府的出产；外府的作坊和田庄有了销路，才付得起工钱、交得起税。 / 国库进了钱，伸手要钱的人也跟着来了：军队要饷，外府要学堂和公事的经费。替国家挣下这份财源的人，也等着国家替他们的日子出点力。

**12. `nesnd_small_request_autonomy_desc`**（`replace/nesnd_small_states_l_simp_chinese.yml`）
- 改前：以地方已经具备的经济与行政能力为据，要求宗主允许本国自行处理更多事务。
- 改后：我们自己收得上税，也有人手办理政务。宗主该把更多国事交还给我们了。

**13. `usm_civilwar.1.1`**（`replace/ce_usm_events_l_simp_chinese.yml`）
- 改前：奉明正朔，联络各省！
- 改后：吴贼！狗贼！奸贼！恶贼！逆贼！

**14. `usm_civilwar.10.3`**（`replace/ce_usm_events_l_simp_chinese.yml`）
- 改前：由国人议政，不再另立天子。
- 改后：当年没打赢，今天我们再来一遍！

**15. `nesnd_american_restoration.3.a`**（`replace/nesnd_native_americas_l_simp_chinese.yml`）
- 改前：军队已经出面，乡村却未必服从。
- 改后：再有聚众的，照此办理。

**16. `nesnd_american_restoration.12.d`**（`replace/nesnd_native_americas_l_simp_chinese.yml`）
- 改前：印卡宫廷拒绝了合并的请求。王朝的共同传统可以使双方相互接近，却不足以让现有的统治者接受同一国家的安排。 / 政府须继续处理本国的土地与地方政治，不能把这些责任都寄于宫廷的答复。经过等待期，双方仍可重新商谈。
- 改后：印卡宫廷回绝了合并。两家同奉一个王朝的传统，彼此可以论亲，却谁也不肯让出自己的君位和朝堂。 / 村社的土地和地方上的纷争，还得我们自己料理，指望不上宫廷的答复。等待期满后，可以再遣使商谈。

**17. `nesnd_india_princes_reason`**（`replace/nesnd_india_l_simp_chinese.yml`）
- 改前：德里、南京与巴黎都向印度诸邦递出了自己的条件。王公们所要保住的不只是祖传的宫殿，还有土地、税收和决定本国命运的权力。合作可以带来援助，却不一定带来自主。
- 改后：德里、南京和巴黎都给印度诸邦开出了条件。王公们要保的不只是祖传的宫殿，还有土地、税收和自己国家的命运。谁的援助都不白给。

**18. `nesnd_supply.1.b`**（`nesnd_supply_l_simp_chinese.yml`）
- 改前：本国事务尚多，暂不接洽。
- 改后：自家的事还没理清，顾不上替商人牵线。

**19. `nesnd_journal_closures_parent_cne`**（`replace/nesnd_journal_closures_l_simp_chinese.yml`）
- 改前：此项事务随“$ce_cne_land_reform$”一同结束。
- 改后：这件事随“$ce_cne_land_reform$”一并了结。

**20. `nesnd_egypt_independence_reason`**（`replace/nesnd_egypt_l_simp_chinese.yml`）
- 改前：1825年的协定承认埃及摆脱奥斯曼的统辖，六国以保证独立换取在尼罗河沿岸投资的权利。政府得到了喘息的机会，工场、学校和军队却也开始依赖外国的资金与技术。 / 选择投资伙伴，可以引进机器、教师和新的产业。外资占据的份额越大，埃及自主决策的余地就越小。未来三十年，政府必须在发展与独立之间作出取舍。
- 改后：1825年的协定承认埃及摆脱奥斯曼的统辖，六国以担保独立，换得在尼罗河沿岸投资的权利。朝廷得了喘息之机，工场、学校和军队却也开始仰仗外国的钱和技术。 / 有了投资伙伴，就有机器、教员和新产业进来。只是外资占得越多，埃及自己拿主意的余地就越少。这样的日子，要熬三十年。

### 校验

- 逐键比对：439 个改动键的 `[...]`、`$...$`、`#x ...#!`、`@...!`、阿拉伯数字、`\n` 全部与改前一致，问题 0（`final_check.json`）。
- 33 个改动文件均保留 UTF-8 BOM、`l_simp_chinese:` 语言头和原有换行符；各文件键集合不变；全目录 7,345 键无重复。
- 中文数字有变化的 6 键：`usm_civilwar.1.d`（数千年）、`usm_civilwar.10.t` 与 `12.d`（第二次靖难战争，现行战争名）、`usm_civilwar.23.d`（百年未有）都来自作者原句；`nesnd_qe1.3.a`“十年，就这么耗掉了”与事件标题“十年空议”和十年期限一致；`nesnd_rg_egy_reason` 的“四周”是方位词，不是数字。
- 未实机验证：游戏内的事件版式、按钮提示行宽和换行都没看过。

### 有疑问而未改的键

- 34 个“作者改稿后又被代理改动”的键（清单见上文“待确认 3”）。
- `usm_civilwar.10.3` 作者原句为“1812赢不了，今天我们再来一遍！”。因数字须与改前一致，本轮写作“当年没打赢，今天我们再来一遍！”。若要恢复原句（含 1812），请确认。
- `usm_civilwar.2.1` 作者原句提到季高、直弼、林汉涵等人，与现行设定是否相符无法确认，本轮改写为“传令各营，粮饷兵马即刻调齐！”。
- `nesnd_civic_characters_l_simp_chinese.yml`：任务43记录这份含用户改稿，但没有列出具体键。本轮只改了 11 条明显重复的收尾，选项一概未动。
- 营产整顿 `nesnd_cne_camp_*` 二十余州的按钮与修正、`nesnd_map_refinement` 与 `nesnd_national_map` 的水运说明：同一模板按州复用，文字具体，未改。
- `nesnd_crisis.30.local`：代理据作者改稿 `nesnd_crisis.30.d` 写的地方版，未改。
- 印度文件改了 12 键。若本机主 MOD 有未上传改稿，同步前请先比对这 12 键。

### 遗留

- 英文对应键未改，需另开任务按新中文重写。
- 主 MOD 同步须在本机完成（云端无法写入）。
