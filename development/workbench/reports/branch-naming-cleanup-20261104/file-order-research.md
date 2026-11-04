# `zz…` 文件命名与加载顺序调查（只读）

范围：M 内文件 basename 以至少两个 `z` 开始；读取当前 GAME、所有 WORKSHOP basename、M 文本引用和工作台工具证据。没有改 M、删目录、启动游戏或测试改动。
共 121 个文件；本地化 94，脚本 27，其他 0。

## 结论与风险

- 这些 `zz…` 文件不能统一当作临时产物：其中有语言 `replace` 本地化、多个 `common` 数据库脚本、历史/军事初始化文件。未发现能只凭文件名认定可删的依据。 当前 121 个文件名/注释也未出现 `tmp`、`temporary`、`scratch`、`WIP` 等临时标记；文本搜索的 `test` 命中是普通玩家叙述。`common/history/military_formations/zz_ce_transferred_garrisons.txt` 目前仅有空 `MILITARY_FORMATIONS = {}` 容器，属于唯一明显无内容文件，但它的空壳本身不足以证明可删。
- 检查了 GAME 和 WORKSHOP 中 basename/相对路径；完整命中清单在 JSON。跨 mod 是否获胜取决于 mod load order，同名命中本身不证明当前胜者。
- 本次以同目录原版数据完成 `REPLACE` 目标核对：23 个带指令的脚本覆盖原版数据库对象；`common/journal_entries/zzzz_nesnd_retire_regional.txt` 的 7 个 `nesnd_rg_*` 在 GAME 同目录不存在，均是本 MOD 自定义 ID，`je_veiled_protectorate` 则对应 GAME `common/journal_entries/00_veiled_protectorate.txt:1`。每个目标的原版/MOD 定义路径和行号已加入 JSON。该脚本仍然是内容层 replace 命令，文件名前缀保留并不能替代其覆盖定义。
- `zz` 本地化的 GAME 同键碰撞数和跨 z 文件重复数已按 key/source/前缀计入 JSON：English 47 duplicate keys、24 vanilla overlaps；简中 47 duplicate keys、25 vanilla overlaps。
- 当前 GAME 没有找到 localization loader README 或对重复 localization key 胜出的官方说明；`localization/languages.yml` 仅说明语言。静态文件名顺序不能证明引擎 key 优先级，故本报告不猜“最后文件赢”。重复键清单按 `english`、`simp_chinese` 的 replace 子树列出。
- `.txt/.gui` 内出现的 `REPLACE:`、`REPLACE_OR_CREATE:`、`INJECT:` 行见 JSON。文件改名不改内容级命令；是否改变数据库定义顺序需按具体数据库文档与原版同类文件确定，不能拿 localization 规则套用。
- M 内按完整文件名的文本引用扫描命中见 JSON；未命中只表示文本扫描未找到，不覆盖动态路径/外部 launcher manifest/二进制引用。

## 可复用的本地化比较工具

- `WORK/tools/test_fpr1_localization_complete.py`、`test_final_preview_localization_complete.py`、`test_c2_repair3_localization_complete.py`：读取 GAME 与候选本地化并汇总 key；代码使用 sorted 文件和 dict 覆写，不能据此判定引擎重复 key 的实际胜出顺序。可复用作 key 存在性比较，需先增强为冲突/来源追踪器。
- `WORK/tools/test_fpr1_locale_pairs_native.py`：语言配对完整度检查，可复用检测英文/简中 key 对齐。
- `WORK/tools/localization_style_review.py`：作者文本的风格对比工具，不是 loader/重复 key 比较器。

## 改名建议

- 当前没有证据支持任何不带前置条件的“安全改名”：对于同语言 `replace` 树内重复 key 的文件，须先查清引擎实际优先级；即使 key 唯一，也先核对原版同 key、同名文件和显式引用。
- 条件式候选：唯一 key、没有原版/工坊 basename/相对路径冲突、没有 M 引用、脚本没有顺序敏感的 duplicate ID 或 REPLACE/INJECT 目标关系，并有该目录加载文档支持“filename 不承载顺序”的文件，可改为描述用途的 basename；语言目录、`replace` 层级、所有 ID/key 和相对优先级必须保留。
- 必须保留/显式复核：所有重复 localization key 文件之间引擎验证后的优先关系；所有 REPLACE/INJECT 指向同一数据库对象的源文件关系；所有与 GAME/WORKSHOP 同 basename 或同 path 的资源；`history` 类覆盖目录语义。不可机械删除 z，也不可把 z 数量改成相同值。


## 静态无重复 key 的本地化改名候选

以下文件在同语言 M 全部 `localization/*/replace` 与 GAME 本地化里没有内部重复或跨文件重复 key；因此从静态 key 冲突角度看，改为描述性文件名不会改变重复 key 竞争。前提是保留语言目录、`replace` 路径和 `.yml` 后缀。此结论不声称已验证引擎对重命名文件的发现规则，发布前仍应做一次定向引擎核验。其他 zz localization 文件至少有一个重复 key 或同名 GAME key，改名须查明实际优先级并维持它。

### English

- `localization/english/replace/zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_english.yml`
- `localization/english/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_english.yml`
- `localization/english/replace/zzzzzzzzzzzzz_nesnd_small_states_l_english.yml`
- `localization/english/replace/zzzzzzzzzzzz_nesnd_batch_c_l_english.yml`
- `localization/english/replace/zzzzzzzzzzzz_nesnd_canon_l_english.yml`
- `localization/english/replace/zzzzzzzzz_nesnd_south_feedback_l_english.yml`
- `localization/english/replace/zzzzzzzz_nesnd_annex_recovery_l_english.yml`
- `localization/english/replace/zzzzzzzz_nesnd_poland_integrity_l_english.yml`
- `localization/english/replace/zzzzzzzz_nesnd_vanilla_concept_compat_l_english.yml`
- `localization/english/replace/zzzzzzz_nesnd_cne_clear_conditions_l_english.yml`
- `localization/english/replace/zzzzzz_nesnd_cne_confidence_l_english.yml`
- `localization/english/replace/zzzzzz_nesnd_cne_programs_l_english.yml`
- `localization/english/replace/zzzzzz_nesnd_concept_clarity_l_english.yml`
- `localization/english/replace/zzzzzz_nesnd_jp_final_l_english.yml`
- `localization/english/replace/zzzzz_nesnd_random_given_names_l_english.yml`
- `localization/english/replace/zzzz_nesnd_cne_ai_agenda_l_english.yml`
- `localization/english/replace/zzzz_nesnd_cne_feedback_l_english.yml`
- `localization/english/replace/zzzz_nesnd_subsistence_modifier_labels_l_english.yml`
- `localization/english/replace/zzzz_nesnd_usm_local_authority_l_english.yml`
- `localization/english/replace/zz_nesnd_engine_compat_l_english.yml`
- `localization/english/replace/zz_nesnd_south_dayuan_l_english.yml`

### 简体中文

- `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzz_nesnd_per_usm_mechanics_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzzzzzzz_nesnd_small_states_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_batch_c_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_canon_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzzz_nesnd_south_feedback_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzz_nesnd_annex_recovery_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzzz_nesnd_vanilla_concept_compat_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzzz_nesnd_cne_clear_conditions_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzz_nesnd_cne_confidence_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzz_nesnd_cne_programs_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzz_nesnd_concept_clarity_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzzz_nesnd_jp_final_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzzz_nesnd_random_given_names_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzz_nesnd_cne_ai_agenda_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzz_nesnd_cne_feedback_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzz_nesnd_subsistence_modifier_labels_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zzzz_nesnd_usm_local_authority_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zz_nesnd_engine_compat_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zz_nesnd_existing_modifier_labels_l_simp_chinese.yml`
- `localization/simp_chinese/replace/zz_nesnd_south_dayuan_l_simp_chinese.yml`

## 逐文件摘要
### `common/character_templates/zz_CE_country_bel.txt`
- script；前缀 z=2；784 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L5 REPLACE:BEL_John_Cockerill = {
- 注释：Belgium character template file ### / Executives / John Cockerill
### `common/character_templates/zz_ce_FRA.txt`
- script；前缀 z=2；2837 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L5 REPLACE:FRA_francois-rene_de_chateaubriand = {；L23 REPLACE:fra_napoleon_iii_character_template = {；L69 REPLACE:FRA_louis_philippe = {；L97 REPLACE:FRA_ferdinand_philippe = {
- 注释：Netherlands character template file ### / Netherlands - NET / dna = dna_francois_rene_de_chateaubriand
### `common/character_templates/zz_ce_historical_commanders_asia.txt`
- script；前缀 z=2；3161 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:afg_general_mohammed = {；L27 REPLACE:chi_admiral_ding_ruchang = {；L55 REPLACE:chi_admiral_sa_chenbing = {；L82 REPLACE:chi_general_yuan_shikai = {
- 注释：Afghanistan - AFG / China - CHI / guaranteed to spawn if possible
### `common/character_templates/zz_ce_italian.txt`
- script；前缀 z=2；337 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 注释：
### `common/character_templates/zz_ce_JAP.txt`
- script；前缀 z=2；16321 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L195 REPLACE:JAP_ienari_tokugawa = {；L233 REPLACE:JAP_ieyoshi_tokugawa = {；L270 REPLACE:JAP_iesada_tokugawa = {；L311 REPLACE:JAP_iemochi_tokugawa = {
- 注释：dna = dna_shogun_tokugawa_ienari / add_trait = sickly / add_trait = sickly
### `common/character_templates/zz_ce_missing_character.txt`
- script；前缀 z=2；548 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 注释：Wu (Ii) Naosuke: existing civil-war event requires a Ming commander. / DNA and birth date: vanilla JAP_ii_naosuke; no Japanese daimyo on_created effects.
### `common/character_templates/zz_ce_NET.txt`
- script；前缀 z=2；407 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L5 REPLACE:NET_willem_i_van_oranje_nassau = {
- 注释：Netherlands character template file ### / Netherlands - NET
### `common/character_templates/zz_historical_leaders_ce_asia.txt`
- script；前缀 z=2；27122 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1204 REPLACE:per_mohammad_shah_qajar_template = {；L1219 REPLACE:per_nasir_al_din_qajar_template = {
- 注释：CNE / 牧驰悯 / role = politician # Remove this line
### `common/company_types/zz_nesnd_fujian_company_location.txt`
- script；前缀 z=2；1569 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:company_foochow_arsenal = {
- 注释：Current GAME Foochow company; exact original rewards/requirements retained.
### `common/country_definitions/zzzz_nesnd_native_restoration.txt`
- script；前缀 z=4；299 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:NAH = {；L5 REPLACE:TWT = {
### `common/dynamic_country_names/zz_nesnd_ming_court.txt`
- script；前缀 z=2；2398 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:HNA = { #；L43 REPLACE:SIH = { #
### `common/government_types/zzzz_nesnd_native_khanate.txt`
- script；前缀 z=4；879 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:gov_khanate = {
### `common/history/ai/zz_nesnd_hus_initial_goal.txt`
- script；前缀 z=2；356 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 注释：HUS emerged from repeated wars against Wu's overseas empire. / Set its initial strategic desire in new-game history only. / Later diplomatic catalysts remain free to change this goal.
### `common/history/military_formations/zz_ce_transferred_garrisons.txt`
- script；前缀 z=2；31 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
### `common/journal_entries/zz_nesnd_jp_native_journals.txt`
- script；前缀 z=2；2555 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:je_meiji_restoration = {；L10 REPLACE:je_meiji_imperial_marriage = {；L19 REPLACE:je_meiji_main = {；L28 REPLACE:je_meiji_economy = {
### `common/journal_entries/zzzz_nesnd_hus_native_monarchy.txt`
- script；前缀 z=4；2241 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:je_abolish_monarchy = {
- 注释：triggered by on_law_enactment_started
### `common/journal_entries/zzzz_nesnd_india_native.txt`
- script；前缀 z=4；4460 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:je_uneasy_raj = {；L8 REPLACE:je_sepoy_mutiny = {；L13 REPLACE:je_mughal_hindustan = {；L18 REPLACE:je_consolidate_colonial_rule = {
### `common/journal_entries/zzzz_nesnd_native_error_bans.txt`
- script；前缀 z=4；431 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:je_splitting_oman = {
- 注释：No split, territory transfer, or new ZAN creation; existing countries are untouched.
### `common/journal_entries/zzzz_nesnd_retire_regional.txt`
- script；前缀 z=4；1442 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:nesnd_rg_pru = { group = je_group_historical_content is_shown_when_inactive = { always = no } possible = { always = no } invalid = { always = yes } }；L3 REPLACE:nesnd_rg_aus = { group = je_group_historical_content is_shown_when_inactive = { always = no } possible = { always = no } invalid = { always = yes } }；L4 REPLACE:nesnd_rg_tur = { group = je_group_historical_content is_shown_when_inactive = { always = no } possible = { always = no } invalid = { always = yes } }；L5 REPLACE:nesnd_rg_egy = { group = je_group_historical_content is_shown_when_inactive = { always = no } possible = { always = no } invalid = { always = yes } }
- 注释：Superseded by the author's PPET campaign instructions. Earned old rewards are not revoked. / The new Egyptian independence outcome owns its government transition.
### `common/journal_entries/zzzz_nesnd_turtle_island.txt`
- script；前缀 z=4；2198 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:je_unite_the_nations = {
### `common/laws/zzzz_nesnd_cne_ai_agenda.txt`
- script；前缀 z=4；4227 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:law_peasant_proprietorship = { # Homesteading for old world countries；L117 REPLACE:law_restricted_child_labor = {
- 注释：Only the two current native law symbols are overridden; all native behavior is preserved. / building_minimum_incorporated_subsistence_employment_add = 0.25 / AI should really try to get out of Serfdom under the right circumstances
### `common/laws/zzzz_nesnd_hus_citizenship_lock.txt`
- script；前缀 z=4；24315 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L5 REPLACE:law_subjecthood = {；L124 REPLACE:law_ethnostate = {；L251 REPLACE:law_national_supremacy = {；L374 REPLACE:law_racial_segregation = {
- 注释：group = this is the law_group a law belongs to / icon = graphical icon shown in-game / modifier = {} modifier on country for having adopted this law
### `common/scripted_buttons/zzzz_nesnd_native_error_bans.txt`
- script；前缀 z=4；353 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L2 REPLACE:christ_of_nations_button = {
- 注释：Disable the native agitator request; CE Poland keeps its own buttons/events.
### `common/scripted_buttons/zzzz_nesnd_turtle_island.txt`
- script；前缀 z=4；4764 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:je_unite_the_nations_proclaim_turtle_island_button = {；L30 REPLACE:je_unite_the_nations_organize_the_tribes_button = {；L94 REPLACE:je_unite_the_nations_offer_confederation_button = {
### `common/scripted_effects/zz_nesnd_jp_native_guards.txt`
- script；前缀 z=2；4932 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:country_restore_japanese_emperor = {；L81 REPLACE:character_appoint_new_shogun_when_no_heir = {
### `common/scripted_effects/zzzz_nesnd_hus_monarchy_entry.txt`
- script；前缀 z=4；737 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:transition_off_of_monarchy_effects = {
### `common/treaty_articles/zzzz_nesnd_egypt_guarantee.txt`
- script；前缀 z=4；7481 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 加载指令：L1 REPLACE:guarantee_independence = {
- 注释：We are doing this to be able to reuse loc across treaties and diplomatic actions / Special anti-Opium Wars cheese - block any alliance/defensive pact/guarantee deals before the JE fires
### `localization/english/replace/zz_nesnd_crisis_l_english.yml`
- localization；前缀 z=2；34130 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：161。
- 注释：nesnd_federal_compact_button_alt_desc:0 "在新政完全实现已不可阻挡的今天，南明政局已在杭州南府最高掌控之下——这是好的！以我们的权势为基础，易代改姓时机已然成熟。就像过去的“大礼议”改变了北明中期的国家格局，我们应当从速召集额外的大礼议会（南明国家议会）和内阁会议。重新议定任官、
### `localization/english/replace/zz_nesnd_crisis_rules_l_english.yml`
- localization；前缀 z=2；2468 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：21。
### `localization/english/replace/zz_nesnd_engine_compat_l_english.yml`
- localization；前缀 z=2；57 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：1。
### `localization/english/replace/zz_nesnd_geography_l_english.yml`
- localization；前缀 z=2；1803 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：29。
### `localization/english/replace/zz_nesnd_hainan_l_english.yml`
- localization；前缀 z=2；309 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：7。
### `localization/english/replace/zz_nesnd_map_refinement_l_english.yml`
- localization；前缀 z=2；2453 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：41。
### `localization/english/replace/zz_nesnd_national_map_l_english.yml`
- localization；前缀 z=2；3583 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：55。
### `localization/english/replace/zz_nesnd_south_central_vietnam_l_english.yml`
- localization；前缀 z=2；568 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：8。
- 注释：Geographical working labels; no new political or historical title is implied.
### `localization/english/replace/zz_nesnd_south_dayuan_l_english.yml`
- localization；前缀 z=2；341 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：6。
### `localization/english/replace/zzzz_nesnd_cne_ai_agenda_l_english.yml`
- localization；前缀 z=4；302 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：2。
### `localization/english/replace/zzzz_nesnd_cne_feedback_l_english.yml`
- localization；前缀 z=4；1787 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：21。
### `localization/english/replace/zzzz_nesnd_cne_reform_l_english.yml`
- localization；前缀 z=4；6170 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：26。
### `localization/english/replace/zzzz_nesnd_hus_social_hierarchy_l_english.yml`
- localization；前缀 z=4；15492 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：112。
### `localization/english/replace/zzzz_nesnd_subsistence_modifier_labels_l_english.yml`
- localization；前缀 z=4；1064 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：8。
### `localization/english/replace/zzzz_nesnd_usm_local_authority_l_english.yml`
- localization；前缀 z=4；68 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：1。
### `localization/english/replace/zzzzz_nesnd_random_given_names_l_english.yml`
- localization；前缀 z=5；830 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：25。
### `localization/english/replace/zzzzz_nesnd_south_journal_ui_l_english.yml`
- localization；前缀 z=5；3370 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：12。
### `localization/english/replace/zzzzzz_nesnd_chen_security_l_english.yml`
- localization；前缀 z=6；8879 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：35。
### `localization/english/replace/zzzzzz_nesnd_cne_confidence_l_english.yml`
- localization；前缀 z=6；6411 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：51。
### `localization/english/replace/zzzzzz_nesnd_cne_politics_l_english.yml`
- localization；前缀 z=6；185 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：2。
### `localization/english/replace/zzzzzz_nesnd_cne_programs_l_english.yml`
- localization；前缀 z=6；25291 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：180。
### `localization/english/replace/zzzzzz_nesnd_concept_clarity_l_english.yml`
- localization；前缀 z=6；1164 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：3。
### `localization/english/replace/zzzzzz_nesnd_jp_development_l_english.yml`
- localization；前缀 z=6；25555 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：184。
### `localization/english/replace/zzzzzz_nesnd_jp_final_l_english.yml`
- localization；前缀 z=6；2165 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：12。
### `localization/english/replace/zzzzzz_nesnd_succession_board_l_english.yml`
- localization；前缀 z=6；5686 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：37。
### `localization/english/replace/zzzzzzz_nesnd_cne_clear_conditions_l_english.yml`
- localization；前缀 z=7；1644 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：16。
### `localization/english/replace/zzzzzzz_nesnd_ming_court_l_english.yml`
- localization；前缀 z=7；5256 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：32。
### `localization/english/replace/zzzzzzz_nesnd_qin_persia_l_english.yml`
- localization；前缀 z=7；21897 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：206。
### `localization/english/replace/zzzzzzzz_nesnd_annex_recovery_l_english.yml`
- localization；前缀 z=8；380 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：5。
### `localization/english/replace/zzzzzzzz_nesnd_poland_integrity_l_english.yml`
- localization；前缀 z=8；538 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：7。
### `localization/english/replace/zzzzzzzz_nesnd_south_politics_l_english.yml`
- localization；前缀 z=8；13315 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：53。
### `localization/english/replace/zzzzzzzz_nesnd_vanilla_concept_compat_l_english.yml`
- localization；前缀 z=8；164 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：1。
- 注释：Compatibility alias for the vanilla great_game_complete_tt spelling; retain the native concept label.
### `localization/english/replace/zzzzzzzzz_nesnd_south_feedback_l_english.yml`
- localization；前缀 z=9；950 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：5。
### `localization/english/replace/zzzzzzzzz_nesnd_south_peace_gates_l_english.yml`
- localization；前缀 z=9；1253 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：4。
### `localization/english/replace/zzzzzzzzzz_nesnd_court_followup_l_english.yml`
- localization；前缀 z=10；5864 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：28。
### `localization/english/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml`
- localization；前缀 z=12；18290 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：141。
### `localization/english/replace/zzzzzzzzzzzz_nesnd_batch_c_l_english.yml`
- localization；前缀 z=12；25432 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：216。
### `localization/english/replace/zzzzzzzzzzzz_nesnd_canon_l_english.yml`
- localization；前缀 z=12；3117 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：10。
### `localization/english/replace/zzzzzzzzzzzzz_nesnd_feedback_l_english.yml`
- localization；前缀 z=13；18160 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：183。
### `localization/english/replace/zzzzzzzzzzzzz_nesnd_small_states_l_english.yml`
- localization；前缀 z=13；24299 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：189。
### `localization/english/replace/zzzzzzzzzzzzzz_nesnd_india_l_english.yml`
- localization；前缀 z=14；19225 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：202。
### `localization/english/replace/zzzzzzzzzzzzzzz_nesnd_native_errors_l_english.yml`
- localization；前缀 z=15；242 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：3。
### `localization/english/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_english.yml`
- localization；前缀 z=16；4088 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：39。
### `localization/english/replace/zzzzzzzzzzzzzzzzzz_nesnd_bug_sweep_l_english.yml`
- localization；前缀 z=18；2356 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：18。
### `localization/english/replace/zzzzzzzzzzzzzzzzzz_nesnd_per_usm_mechanics_l_english.yml`
- localization；前缀 z=18；4521 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：46。
### `localization/english/replace/zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_english.yml`
- localization；前缀 z=19；7644 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：61。
### `localization/english/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_english.yml`
- localization；前缀 z=20；10724 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：139。
### `localization/simp_chinese/replace/zz_nesnd_crisis_l_simp_chinese.yml`
- localization；前缀 z=2；27399 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：161。
### `localization/simp_chinese/replace/zz_nesnd_crisis_rules_l_simp_chinese.yml`
- localization；前缀 z=2；2217 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：21。
### `localization/simp_chinese/replace/zz_nesnd_engine_compat_l_simp_chinese.yml`
- localization；前缀 z=2；62 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：1。
### `localization/simp_chinese/replace/zz_nesnd_existing_modifier_labels_l_simp_chinese.yml`
- localization；前缀 z=2；135 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：2。
### `localization/simp_chinese/replace/zz_nesnd_geography_l_simp_chinese.yml`
- localization；前缀 z=2；1541 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：29。
### `localization/simp_chinese/replace/zz_nesnd_hainan_l_simp_chinese.yml`
- localization；前缀 z=2；309 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：7。
### `localization/simp_chinese/replace/zz_nesnd_map_refinement_l_simp_chinese.yml`
- localization；前缀 z=2；2311 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：41。
### `localization/simp_chinese/replace/zz_nesnd_national_map_l_simp_chinese.yml`
- localization；前缀 z=2；3078 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：55。
### `localization/simp_chinese/replace/zz_nesnd_south_central_vietnam_l_simp_chinese.yml`
- localization；前缀 z=2；540 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：8。
- 注释：Geographical working labels; no new political or historical title is implied.
### `localization/simp_chinese/replace/zz_nesnd_south_dayuan_l_simp_chinese.yml`
- localization；前缀 z=2；408 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：6。
- 注释：South Dayuan and new hub labels are 2026-10-31 working design names, not author-attested lore.
### `localization/simp_chinese/replace/zzzz_nesnd_cne_ai_agenda_l_simp_chinese.yml`
- localization；前缀 z=4；264 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：2。
### `localization/simp_chinese/replace/zzzz_nesnd_cne_feedback_l_simp_chinese.yml`
- localization；前缀 z=4；1803 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：21。
### `localization/simp_chinese/replace/zzzz_nesnd_cne_reform_l_simp_chinese.yml`
- localization；前缀 z=4；5193 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：26。
### `localization/simp_chinese/replace/zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml`
- localization；前缀 z=4；13787 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：112。
### `localization/simp_chinese/replace/zzzz_nesnd_subsistence_modifier_labels_l_simp_chinese.yml`
- localization；前缀 z=4；1017 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：8。
### `localization/simp_chinese/replace/zzzz_nesnd_usm_local_authority_l_simp_chinese.yml`
- localization；前缀 z=4；73 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：1。
### `localization/simp_chinese/replace/zzzzz_nesnd_random_given_names_l_simp_chinese.yml`
- localization；前缀 z=5；815 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：25。
### `localization/simp_chinese/replace/zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml`
- localization；前缀 z=5；2947 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：12。
### `localization/simp_chinese/replace/zzzzzz_nesnd_chen_security_l_simp_chinese.yml`
- localization；前缀 z=6；8034 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：35。
### `localization/simp_chinese/replace/zzzzzz_nesnd_cne_confidence_l_simp_chinese.yml`
- localization；前缀 z=6；5782 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：51。
### `localization/simp_chinese/replace/zzzzzz_nesnd_cne_politics_l_simp_chinese.yml`
- localization；前缀 z=6；187 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：2。
### `localization/simp_chinese/replace/zzzzzz_nesnd_cne_programs_l_simp_chinese.yml`
- localization；前缀 z=6；21722 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：180。
### `localization/simp_chinese/replace/zzzzzz_nesnd_concept_clarity_l_simp_chinese.yml`
- localization；前缀 z=6；1004 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：3。
### `localization/simp_chinese/replace/zzzzzz_nesnd_jp_development_l_simp_chinese.yml`
- localization；前缀 z=6；22423 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：184。
### `localization/simp_chinese/replace/zzzzzz_nesnd_jp_final_l_simp_chinese.yml`
- localization；前缀 z=6；1813 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：12。
### `localization/simp_chinese/replace/zzzzzz_nesnd_succession_board_l_simp_chinese.yml`
- localization；前缀 z=6；4778 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：37。
### `localization/simp_chinese/replace/zzzzzzz_nesnd_cne_clear_conditions_l_simp_chinese.yml`
- localization；前缀 z=7；1370 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：16。
### `localization/simp_chinese/replace/zzzzzzz_nesnd_ming_court_l_simp_chinese.yml`
- localization；前缀 z=7；4321 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：32。
### `localization/simp_chinese/replace/zzzzzzz_nesnd_qin_persia_l_simp_chinese.yml`
- localization；前缀 z=7；18414 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：206。
### `localization/simp_chinese/replace/zzzzzzzz_nesnd_annex_recovery_l_simp_chinese.yml`
- localization；前缀 z=8；385 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：5。
### `localization/simp_chinese/replace/zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml`
- localization；前缀 z=8；10832 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：53。
### `localization/simp_chinese/replace/zzzzzzzz_nesnd_vanilla_concept_compat_l_simp_chinese.yml`
- localization；前缀 z=8；169 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：1。
- 注释：Compatibility alias for the vanilla great_game_complete_tt spelling; retain the native concept label.
### `localization/simp_chinese/replace/zzzzzzzzz_nesnd_south_feedback_l_simp_chinese.yml`
- localization；前缀 z=9；865 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：5。
### `localization/simp_chinese/replace/zzzzzzzzz_nesnd_south_peace_gates_l_simp_chinese.yml`
- localization；前缀 z=9；1128 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：4。
### `localization/simp_chinese/replace/zzzzzzzzzz_nesnd_court_followup_l_simp_chinese.yml`
- localization；前缀 z=10；4978 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：28。
### `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml`
- localization；前缀 z=12；15952 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：141。
### `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_batch_c_l_simp_chinese.yml`
- localization；前缀 z=12；22161 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：216。
### `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_canon_l_simp_chinese.yml`
- localization；前缀 z=12；2519 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：10。
### `localization/simp_chinese/replace/zzzzzzzzzzzzz_nesnd_feedback_l_simp_chinese.yml`
- localization；前缀 z=13；16969 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：183。
### `localization/simp_chinese/replace/zzzzzzzzzzzzz_nesnd_small_states_l_simp_chinese.yml`
- localization；前缀 z=13；21948 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：189。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzz_nesnd_india_l_simp_chinese.yml`
- localization；前缀 z=14；17441 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：202。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzzz_nesnd_native_errors_l_simp_chinese.yml`
- localization；前缀 z=15；625 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：5。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzzzz_nesnd_journal_feedback_l_simp_chinese.yml`
- localization；前缀 z=16；3681 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：39。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzz_nesnd_bug_sweep_l_simp_chinese.yml`
- localization；前缀 z=18；2037 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：18。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzz_nesnd_per_usm_mechanics_l_simp_chinese.yml`
- localization；前缀 z=18；3941 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：45。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_simp_chinese.yml`
- localization；前缀 z=19；6865 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：61。
### `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml`
- localization；前缀 z=20；9933 B；GAME 同相对路径=否；同 basename GAME=0、WORKSHOP=0。
- 本地化条目数：139。

## 来源和限制

- 依 `M/AGENTS.md`、NESND `SKILL.md` 与 `docs/agents/engineering-skills.md` 路由：GAME/WORKSHOP 只读，报告归 WORK；并检查技能指向的 `references/paths.md`。
- `catalog.py status` 执行没有返回 stdout/stderr，本报告不据此声称版本状态。
- WORK 上述比较工具只作为代码检查结果，不把静态结果称为引擎优先级或游戏验证。
- 精确路径、哈希、basename 命中、文本引用和脚本指令详见旁边 JSON；重复 key 完整集合见 `english-duplicate-keys.json` 和 `simp_chinese-duplicate-keys.json`。
