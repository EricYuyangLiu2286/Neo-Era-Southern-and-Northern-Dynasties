# Localization 重复 key 与 zz 脚本命名整理计划（只读）

范围：当前 M 所有 `localization/{english,simp_chinese}/replace/**/*.yml`，不限定 z 前缀；另盘点 27 个 z 前缀 `.txt` 文件。只读调查，未编辑 M、未改名、未删除、未测试。

基准：当前 M 与本地源仓库 main 内容一致性按逐文件 Git blob 核验；主代码交付为 `f05f0639d3cba02206fb357043a90deb32ba8c47`，工作台 main 当前为 `0bd4bdbd43adf0076165a8e338a92e70daefeb40`。任务34状态是 STATIC_PASS / ENGINE_NOT_RUN，不表述为游戏内验证。

## 重复总量

|语言|replace文件|key行|唯一key|重复key|不同文本冲突|相同文本重复|只在单文件重复|跨文件重复|重复值含CJK字符|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|english|76|7267|7143|119|44|75|3|116|17|
|simp_chinese|76|6641|6516|120|36|84|7|113|0|

重复统计覆盖 `ce_*.yml`、普通描述文件、`map/` 子目录和 z 文件；一个 key 同一文件内重复也计入。17 个重复英文 occurrence 含 CJK，集中在 `ce_states` 的 STATE_SICHUAN 和 `zz_nesnd_crisis[_rules]_l_english`。这些 EN occurrence 中不少整段是中文，见 JSON `english_duplicate_values_containing_cjk`；其他 English-locale 文本里另有中文专名，CJK 命中不一概等于翻译错误。精确 occurrence、行号、UTF-8 BOM、当前值、2026-10-30前变化前快照的同 key 值、key 引用以及 Git blob 证据都在 JSON。

## 唯一 key owner 提案

每个重复 key 两种语言分别指定一个主题文件。保持 `localization/<locale>/replace/`，map key 继续放在 `replace/map/`；所有最终 `.yml` 继续 UTF-8 BOM、同一 `l_english:` / `l_simp_chinese:` 头。move key 只保留一个定义；不对重复来源按文件名排序取值。

### `localization/english/replace/ce_cne_events_l_english.yml`
主题：`ce_cne_events`；分配 key 数：English 5，简中 0。
**english**
- `ce_cne_reform_legal_system` — 同值合并；来源：`ce_cne_events_l_english.yml:29`, `ce_usm_events_l_english.yml:128`。
- `ce_cne_reform_limited_market_access` — 值冲突需按证据选定；来源：`ce_cne_events_l_english.yml:25`, `ce_usm_events_l_english.yml:124`。
- `ce_cne_technology_advantage` — 同值合并；来源：`ce_cne_events_l_english.yml:28`, `ce_usm_events_l_english.yml:127`。
- `ce_cne_war_with_usm` — 值冲突需按证据选定；来源：`ce_cne_events_l_english.yml:27`, `ce_usm_events_l_english.yml:126`。
- `ce_cne_war_with_western_qin` — 值冲突需按证据选定；来源：`ce_cne_events_l_english.yml:26`, `ce_usm_events_l_english.yml:125`。

### `localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml`
主题：`ce_cne_events`；分配 key 数：English 0，简中 6。
**simp_chinese**
- `NOT_TRIGGER_MARKET_ACCESS_LESS_THAN` — 值冲突需按证据选定；建议：root_choose_single_same_file_value；来源：`ce_cne_events_l_simp_chinese.yml:23`, `ce_cne_events_l_simp_chinese.yml:25`。
- `ce_cne_reform_legal_system` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:31`, `ce_usm_events_l_simp_chinese.yml:128`。
- `ce_cne_reform_limited_market_access` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:27`, `ce_usm_events_l_simp_chinese.yml:124`。
- `ce_cne_technology_advantage` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:30`, `ce_usm_events_l_simp_chinese.yml:127`。
- `ce_cne_war_with_usm` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:29`, `ce_usm_events_l_simp_chinese.yml:126`。
- `ce_cne_war_with_western_qin` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:28`, `ce_usm_events_l_simp_chinese.yml:125`。

### `localization/english/replace/ce_countries_l_english.yml`
主题：`ce_countries`；分配 key 数：English 2，简中 0。
**english**
- `GNG` — 值冲突需按证据选定；来源：`ce_00_countries_l_english.yml:1009`, `ce_countries_l_english.yml:31`。
- `GNG_ADJ` — 值冲突需按证据选定；来源：`ce_00_countries_l_english.yml:1010`, `ce_countries_l_english.yml:32`。

### `localization/english/replace/ce_country_flavor_l_english.yml`
主题：`ce_country_flavor`；分配 key 数：English 2，简中 0。
**english**
- `ig_qin_aristocrats` — 值冲突需按证据选定；来源：`ce_country_flavor_l_english.yml:3`, `ce_scripted_names_l_english.yml:3`。
- `party_ce_french_liberal_party` — 值冲突需按证据选定；来源：`ce_country_flavor_l_english.yml:19`, `ce_scripted_names_l_english.yml:10`。

### `localization/simp_chinese/replace/ce_country_flavor_l_simp_chinese.yml`
主题：`ce_country_flavor`；分配 key 数：English 0，简中 2。
**simp_chinese**
- `ig_qin_aristocrats` — 同值合并；来源：`ce_country_flavor_l_simp_chinese.yml:3`, `ce_scripted_names_l_simp_chinese.yml:3`。
- `party_ce_french_liberal_party` — 值冲突需按证据选定；来源：`ce_country_flavor_l_simp_chinese.yml:23`, `ce_scripted_names_l_simp_chinese.yml:10`。

### `localization/english/replace/map/ce_states_l_english.yml`
主题：`map/ce_states`；分配 key 数：English 1，简中 0。
**english**
- `STATE_SICHUAN` — 值冲突需按证据选定；建议：keep English “Chengdu” from per-USM mechanics in map/ce_states owner; current ce_states value is Chinese text；来源：`ce_states_l_english.yml:473`, `zzzzzzzzzzzzzzzzzz_nesnd_per_usm_mechanics_l_english.yml:2`。

### `localization/english/replace/nesnd_chen_security_l_english.yml`
主题：`nesnd_chen_security`；分配 key 数：English 3，简中 0。
**english**
- `nesnd_protect_chen_button` — 同值合并；来源：`zz_nesnd_crisis_l_english.yml:68`, `zzzzzz_nesnd_chen_security_l_english.yml:2`。
- `nesnd_protect_chen_button_desc` — 同值合并；来源：`zz_nesnd_crisis_l_english.yml:69`, `zzzzzz_nesnd_chen_security_l_english.yml:3`。
- `nesnd_protect_chen_button_requirements` — 值冲突需按证据选定；建议：keep Chen-security English value; do not alter condition meaning pending separate review；来源：`zz_nesnd_crisis_rules_l_english.yml:15`, `zzzzzz_nesnd_chen_security_l_english.yml:4`。

### `localization/simp_chinese/replace/nesnd_chen_security_l_simp_chinese.yml`
主题：`nesnd_chen_security`；分配 key 数：English 0，简中 3。
**simp_chinese**
- `nesnd_protect_chen_button` — 同值合并；来源：`zz_nesnd_crisis_l_simp_chinese.yml:67`, `zzzzzz_nesnd_chen_security_l_simp_chinese.yml:2`。
- `nesnd_protect_chen_button_desc` — 同值合并；来源：`zz_nesnd_crisis_l_simp_chinese.yml:68`, `zzzzzz_nesnd_chen_security_l_simp_chinese.yml:3`。
- `nesnd_protect_chen_button_requirements` — 值冲突需按证据选定；建议：preserve_existing_CPS_text_pending_separate_review；来源：`zz_nesnd_crisis_rules_l_simp_chinese.yml:15`, `zzzzzz_nesnd_chen_security_l_simp_chinese.yml:4`。

### `localization/english/replace/nesnd_cne_land_reform_l_english.yml`
主题：`nesnd_cne_land_reform`；分配 key 数：English 20，简中 0。
**english**
- `ce_cne_land_draft_failing` — 值冲突需按证据选定；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_english.yml:18`, `zz_nesnd_crisis_l_english.yml:4`。
- `ce_cne_land_draft_failing_reason` — 值冲突需按证据选定；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_english.yml:19`, `zz_nesnd_crisis_l_english.yml:5`。
- `ce_cne_land_reform` — 同值合并；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_english.yml:13`, `zz_nesnd_crisis_l_english.yml:2`。
- `ce_cne_land_reform_reason` — 同值合并；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_english.yml:15`, `zz_nesnd_crisis_l_english.yml:3`。
- `cne_landreform_completion_tracker_add_1` — 值冲突需按证据选定；建议：prefer_number-matching-CNE-reform-value；来源：`ce_cne_events_l_english.yml:100`, `zzzz_nesnd_cne_reform_l_english.yml:27`。
- `cne_landreform_completion_tracker_add_2` — 值冲突需按证据选定；建议：prefer_number-matching-CNE-reform-value；来源：`ce_cne_events_l_english.yml:99`, `zzzz_nesnd_cne_reform_l_english.yml:26`。
- `nesnd_land_completion_bar` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:140`, `zzzz_nesnd_cne_reform_l_english.yml:2`。
- `nesnd_land_completion_bar_desc` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:141`, `zzzz_nesnd_cne_reform_l_english.yml:3`。
- `nesnd_land_disorder_bar` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:142`, `zzzz_nesnd_cne_reform_l_english.yml:4`。
- `nesnd_land_disorder_bar_desc` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:143`, `zzzz_nesnd_cne_reform_l_english.yml:5`, `zzzzzz_nesnd_cne_politics_l_english.yml:2`。
- `nesnd_land_military` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:10`, `zzzz_nesnd_cne_reform_l_english.yml:17`。
- `nesnd_land_military_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:11`, `zzzz_nesnd_cne_reform_l_english.yml:18`。
- `nesnd_land_review` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:8`, `zzzz_nesnd_cne_reform_l_english.yml:14`。
- `nesnd_land_review_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:9`, `zzzz_nesnd_cne_reform_l_english.yml:15`。
- `nesnd_land_review_outcome_tt` — 值冲突需按证据选定；建议：keep CNE-reform English value; crisis_rules English occurrence contains Chinese；来源：`zz_nesnd_crisis_rules_l_english.yml:4`, `zzzz_nesnd_cne_reform_l_english.yml:16`。
- `nesnd_land_status_admin` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:136`, `zzzz_nesnd_cne_reform_l_english.yml:9`。
- `nesnd_land_status_normal` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:139`, `zzzz_nesnd_cne_reform_l_english.yml:11`。
- `nesnd_land_status_war` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:137`, `zzzz_nesnd_cne_reform_l_english.yml:10`。
- `nesnd_land_survey` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:6`, `zzzz_nesnd_cne_reform_l_english.yml:12`。
- `nesnd_land_survey_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_english.yml:7`, `zzzz_nesnd_cne_reform_l_english.yml:13`。

### `localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`
主题：`nesnd_cne_land_reform`；分配 key 数：English 0，简中 20。
**simp_chinese**
- `ce_cne_land_draft_failing` — 值冲突需按证据选定；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_simp_chinese.yml:18`, `zz_nesnd_crisis_l_simp_chinese.yml:4`。
- `ce_cne_land_draft_failing_reason` — 值冲突需按证据选定；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_simp_chinese.yml:19`, `zz_nesnd_crisis_l_simp_chinese.yml:5`。
- `ce_cne_land_reform` — 同值合并；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_simp_chinese.yml:13`, `zz_nesnd_crisis_l_simp_chinese.yml:2`。
- `ce_cne_land_reform_reason` — 同值合并；建议：merge one selected text into the CNE land-reform owner; exact duplicate text can be retained, differing source values need review；来源：`ce_cne_events_l_simp_chinese.yml:15`, `zz_nesnd_crisis_l_simp_chinese.yml:3`。
- `cne_landreform_completion_tracker_add_1` — 值冲突需按证据选定；建议：prefer_number-matching-CNE-reform-value；来源：`ce_cne_events_l_simp_chinese.yml:107`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:27`。
- `cne_landreform_completion_tracker_add_2` — 值冲突需按证据选定；建议：prefer_number-matching-CNE-reform-value；来源：`ce_cne_events_l_simp_chinese.yml:106`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:26`。
- `nesnd_land_completion_bar` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:139`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:2`。
- `nesnd_land_completion_bar_desc` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:140`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:3`。
- `nesnd_land_disorder_bar` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:141`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:4`。
- `nesnd_land_disorder_bar_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:142`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:5`, `zzzzzz_nesnd_cne_politics_l_simp_chinese.yml:2`。
- `nesnd_land_military` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:10`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:17`。
- `nesnd_land_military_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:11`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:18`。
- `nesnd_land_review` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:8`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:14`。
- `nesnd_land_review_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:9`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:15`。
- `nesnd_land_review_outcome_tt` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_rules_l_simp_chinese.yml:4`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:16`。
- `nesnd_land_status_admin` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:135`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:9`。
- `nesnd_land_status_normal` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:138`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:11`。
- `nesnd_land_status_war` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:136`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:10`。
- `nesnd_land_survey` — 值冲突需按证据选定；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:6`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:12`。
- `nesnd_land_survey_desc` — 同值合并；建议：use_CNE_land_reform_reviewed_candidate；来源：`zz_nesnd_crisis_l_simp_chinese.yml:7`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:13`。

### `localization/english/replace/nesnd_india_l_english.yml`
主题：`nesnd_india`；分配 key 数：English 1，简中 0。
**english**
- `nesnd_india_community_unrest` — 值冲突需按证据选定；建议：root_choose_semantic_scope；来源：`zzzzzzzzzzzzzz_nesnd_india_l_english.yml:22`, `zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_english.yml:20`。

### `localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml`
主题：`nesnd_india`；分配 key 数：English 0，简中 1。
**simp_chinese**
- `nesnd_india_community_unrest` — 值冲突需按证据选定；建议：root_choose_semantic_scope；来源：`zzzzzzzzzzzzzz_nesnd_india_l_simp_chinese.yml:22`, `zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml:20`。

### `localization/english/replace/nesnd_japan_l_english.yml`
主题：`nesnd_japan`；分配 key 数：English 5，简中 0。
**english**
- `gov_nesnd_japan_lin_regency` — 同值合并；来源：`nesnd_japan_lin_regency_l_english.yml:2`, `zzzzzz_nesnd_jp_development_l_english.yml:178`。
- `gov_nesnd_japan_lin_regency_desc` — 值冲突需按证据选定；建议：use_reviewed_Lin_regency_text；来源：`nesnd_japan_lin_regency_l_english.yml:3`, `zzzzzz_nesnd_jp_development_l_english.yml:179`。
- `nesnd_japan_reunification_goal` — 值冲突需按证据选定；建议：use_reviewed_Japan_text；来源：`nesnd_japan_l_english.yml:27`, `zzzzzz_nesnd_jp_development_l_english.yml:114`。
- `nesnd_japan_reunification_reason` — 值冲突需按证据选定；建议：use_reviewed_Japan_text；来源：`nesnd_japan_l_english.yml:25`, `zzzzzz_nesnd_jp_development_l_english.yml:112`。
- `nesnd_japan_reunification_status` — 值冲突需按证据选定；建议：use_reviewed_Japan_text；来源：`nesnd_japan_l_english.yml:26`, `zzzzzz_nesnd_jp_development_l_english.yml:113`。

### `localization/simp_chinese/replace/nesnd_japan_l_simp_chinese.yml`
主题：`nesnd_japan`；分配 key 数：English 0，简中 5。
**simp_chinese**
- `gov_nesnd_japan_lin_regency` — 同值合并；来源：`nesnd_japan_lin_regency_l_simp_chinese.yml:2`, `zzzzzz_nesnd_jp_development_l_simp_chinese.yml:178`。
- `gov_nesnd_japan_lin_regency_desc` — 值冲突需按证据选定；建议：use_reviewed_Lin_regency_text；来源：`nesnd_japan_lin_regency_l_simp_chinese.yml:3`, `zzzzzz_nesnd_jp_development_l_simp_chinese.yml:179`。
- `nesnd_japan_reunification_goal` — 值冲突需按证据选定；建议：use_reviewed_Japan_text；来源：`nesnd_japan_l_simp_chinese.yml:27`, `zzzzzz_nesnd_jp_development_l_simp_chinese.yml:114`。
- `nesnd_japan_reunification_reason` — 值冲突需按证据选定；建议：use_reviewed_Japan_text；来源：`nesnd_japan_l_simp_chinese.yml:25`, `zzzzzz_nesnd_jp_development_l_simp_chinese.yml:112`。
- `nesnd_japan_reunification_status` — 值冲突需按证据选定；建议：use_reviewed_Japan_text；来源：`nesnd_japan_l_simp_chinese.yml:26`, `zzzzzz_nesnd_jp_development_l_simp_chinese.yml:113`。

### `localization/english/replace/nesnd_native_americas_l_english.yml`
主题：`nesnd_native_americas`；分配 key 数：English 5，简中 0。
**english**
- `nesnd_hus_registration.1.a` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_english.yml:38`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml:101`。
- `nesnd_hus_registration.1.d` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_english.yml:37`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml:100`。
- `nesnd_hus_registration.1.t` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_english.yml:36`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml:99`。
- `nesnd_hus_registration.2.a` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_english.yml:41`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml:103`。
- `nesnd_hus_registration.2.t` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_english.yml:39`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml:102`。

### `localization/simp_chinese/replace/nesnd_native_americas_l_simp_chinese.yml`
主题：`nesnd_native_americas`；分配 key 数：English 0，简中 5。
**simp_chinese**
- `nesnd_hus_registration.1.a` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml:38`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml:101`。
- `nesnd_hus_registration.1.d` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml:37`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml:100`。
- `nesnd_hus_registration.1.t` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml:36`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml:99`。
- `nesnd_hus_registration.2.a` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml:41`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml:103`。
- `nesnd_hus_registration.2.t` — 值冲突需按证据选定；建议：use_A2_text_for_shared_event_keys；来源：`zzzz_nesnd_hus_social_hierarchy_l_simp_chinese.yml:39`, `zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml:102`。

### `localization/english/replace/nesnd_qin_persia_l_english.yml`
主题：`nesnd_qin_persia`；分配 key 数：English 1，简中 0。
**english**
- `nesnd_qe1_balance_bar_desc` — 锁定原审定文案；不改 QE1；建议：locked_keep_Qin_Persia_reviewed_value；来源：`zzzzzzz_nesnd_qin_persia_l_english.yml:6`, `zzzzzzzzzzzzzzzzzz_nesnd_bug_sweep_l_english.yml:9`。

### `localization/simp_chinese/replace/nesnd_qin_persia_l_simp_chinese.yml`
主题：`nesnd_qin_persia`；分配 key 数：English 0，简中 1。
**simp_chinese**
- `nesnd_qe1_balance_bar_desc` — 锁定原审定文案；不改 QE1；建议：locked_keep_Qin_Persia_reviewed_value；来源：`zzzzzzz_nesnd_qin_persia_l_simp_chinese.yml:6`, `zzzzzzzzzzzzzzzzzz_nesnd_bug_sweep_l_simp_chinese.yml:9`。

### `localization/english/replace/nesnd_shared_feedback_l_english.yml`
主题：`nesnd_shared_feedback`；分配 key 数：English 1，简中 0。
**english**
- `nesnd_feedback_per_maintenance_tt` — 值冲突需按证据选定；建议：prefer_complete_lifecycle_wording；来源：`zzzzzzzzzzzzz_nesnd_feedback_l_english.yml:14`, `zzzzzzzzzzzzzzzzzz_nesnd_bug_sweep_l_english.yml:17`。

### `localization/simp_chinese/replace/nesnd_shared_feedback_l_simp_chinese.yml`
主题：`nesnd_shared_feedback`；分配 key 数：English 0，简中 1。
**simp_chinese**
- `nesnd_feedback_per_maintenance_tt` — 值冲突需按证据选定；建议：prefer_complete_lifecycle_wording；来源：`zzzzzzzzzzzzz_nesnd_feedback_l_simp_chinese.yml:14`, `zzzzzzzzzzzzzzzzzz_nesnd_bug_sweep_l_simp_chinese.yml:17`。

### `localization/english/replace/nesnd_shared_localization_l_english.yml`
主题：`nesnd_shared_localization`；分配 key 数：English 56，简中 0。
**english**
- `CIR` — 同值合并；来源：`ce_00_countries_l_english.yml:1087`, `ce_countries_l_english.yml:149`。
- `CIR_ADJ` — 同值合并；来源：`ce_00_countries_l_english.yml:1088`, `ce_countries_l_english.yml:150`。
- `Qiufu` — 同值合并；来源：`ce_names_l_english.yml:94`, `ce_names_l_english.yml:97`。
- `RULER_TITLE_NESND_JAPAN_REGENT` — 同值合并；来源：`nesnd_japan_lin_regency_l_english.yml:4`, `zzzzzz_nesnd_jp_development_l_english.yml:180`。
- `Zhang` — 同值合并；来源：`ce_names_l_english.yml:83`, `ce_names_l_english.yml:117`。
- `ce_Li` — 同值合并；来源：`ce_names_l_english.yml:36`, `ce_names_l_english.yml:104`。
- `ce_usm_conflicts_within_reason` — 同值合并；来源：`ce_usm_events_l_english.yml:118`, `zz_nesnd_crisis_l_english.yml:101`。
- `ce_usm_cw_japanese_interest_reason` — 同值合并；来源：`ce_usm_events_l_english.yml:149`, `zz_nesnd_crisis_l_english.yml:135`。
- `dyn_c_chechnya_imamate` — 同值合并；来源：`ce_00_countries_l_english.yml:1583`, `ce_countries_l_english.yml:140`。
- `dyn_c_chechnya_imamate_adj` — 同值合并；来源：`ce_00_countries_l_english.yml:1584`, `ce_countries_l_english.yml:141`。
- `flavorCNE.3.d` — 同值合并；来源：`ce_cne_events_l_english.yml:61`, `zz_nesnd_crisis_l_english.yml:98`。
- `flavorCNE.3.f` — 同值合并；来源：`ce_cne_events_l_english.yml:62`, `zz_nesnd_crisis_l_english.yml:163`。
- `flavorCNE.6.d` — 同值合并；来源：`ce_cne_events_l_english.yml:87`, `zz_nesnd_crisis_l_english.yml:95`, `zzzz_nesnd_cne_reform_l_english.yml:23`。
- `flavorCNE.7.d` — 同值合并；来源：`ce_cne_events_l_english.yml:93`, `zz_nesnd_crisis_l_english.yml:96`, `zzzz_nesnd_cne_reform_l_english.yml:24`。
- `flavorCNE.8.d` — 同值合并；来源：`ce_cne_events_l_english.yml:108`, `zz_nesnd_crisis_l_english.yml:97`, `zzzz_nesnd_cne_reform_l_english.yml:25`。
- `flavorUSM.4.1` — 同值合并；来源：`ce_usm_events_l_english.yml:32`, `zz_nesnd_crisis_l_english.yml:102`。
- `flavorUSM.4.d` — 同值合并；来源：`ce_usm_events_l_english.yml:30`, `zz_nesnd_crisis_l_english.yml:104`。
- `flavorUSM.4.f` — 同值合并；来源：`ce_usm_events_l_english.yml:31`, `zz_nesnd_crisis_l_english.yml:152`。
- `flavorUSM.4.t` — 同值合并；来源：`ce_usm_events_l_english.yml:29`, `zz_nesnd_crisis_l_english.yml:103`。
- `flavorUSM.6.d` — 同值合并；来源：`ce_usm_events_l_english.yml:80`, `zz_nesnd_crisis_l_english.yml:106`。
- `flavorUSM.6.t` — 同值合并；来源：`ce_usm_events_l_english.yml:79`, `zz_nesnd_crisis_l_english.yml:105`。
- `ig_ce_mongol_landowners` — 同值合并；来源：`ce_country_flavor_l_english.yml:4`, `ce_scripted_names_l_english.yml:4`。
- `ig_ce_mongol_warboss` — 同值合并；来源：`ce_country_flavor_l_english.yml:5`, `ce_scripted_names_l_english.yml:5`。
- `ig_soldier_officials` — 同值合并；来源：`ce_country_flavor_l_english.yml:2`, `ce_scripted_names_l_english.yml:2`。
- `nesnd_crisis.30.c` — 同值合并；来源：`zz_nesnd_crisis_l_english.yml:16`, `zzzz_nesnd_cne_reform_l_english.yml:22`。
- `nesnd_crisis.33.d` — 同值合并；来源：`zz_nesnd_crisis_l_english.yml:22`, `zzzz_nesnd_cne_reform_l_english.yml:21`。
- `party_ce_imperial_con_party` — 同值合并；来源：`ce_country_flavor_l_english.yml:18`, `ce_scripted_names_l_english.yml:9`。
- `party_ce_imperial_ft_party` — 同值合并；来源：`ce_country_flavor_l_english.yml:17`, `ce_scripted_names_l_english.yml:8`。
- `usm_civilwar.1.1` — 同值合并；来源：`ce_usm_events_l_english.yml:170`, `zz_nesnd_crisis_l_english.yml:108`。
- `usm_civilwar.1.2` — 同值合并；来源：`ce_usm_events_l_english.yml:171`, `zz_nesnd_crisis_l_english.yml:109`。
- `usm_civilwar.1.3` — 同值合并；来源：`ce_usm_events_l_english.yml:172`, `zz_nesnd_crisis_l_english.yml:110`。
- `usm_civilwar.1.d` — 同值合并；来源：`ce_usm_events_l_english.yml:168`, `zz_nesnd_crisis_l_english.yml:107`。
- `usm_civilwar.10.1` — 同值合并；来源：`ce_usm_events_l_english.yml:233`, `zz_nesnd_crisis_l_english.yml:121`。
- `usm_civilwar.10.2` — 同值合并；来源：`ce_usm_events_l_english.yml:234`, `zz_nesnd_crisis_l_english.yml:122`。
- `usm_civilwar.10.3` — 同值合并；来源：`ce_usm_events_l_english.yml:235`, `zz_nesnd_crisis_l_english.yml:123`。
- `usm_civilwar.10.d` — 同值合并；来源：`ce_usm_events_l_english.yml:231`, `zz_nesnd_crisis_l_english.yml:125`。
- `usm_civilwar.10.t` — 同值合并；来源：`ce_usm_events_l_english.yml:230`, `zz_nesnd_crisis_l_english.yml:124`。
- `usm_civilwar.12.d` — 同值合并；来源：`ce_usm_events_l_english.yml:244`, `zz_nesnd_crisis_l_english.yml:127`。
- `usm_civilwar.12.t` — 同值合并；来源：`ce_usm_events_l_english.yml:243`, `zz_nesnd_crisis_l_english.yml:126`。
- `usm_civilwar.13.d` — 同值合并；来源：`ce_usm_events_l_english.yml:249`, `zz_nesnd_crisis_l_english.yml:129`。
- `usm_civilwar.13.t` — 同值合并；来源：`ce_usm_events_l_english.yml:248`, `zz_nesnd_crisis_l_english.yml:128`。
- `usm_civilwar.2.1` — 同值合并；来源：`ce_usm_events_l_english.yml:182`, `zz_nesnd_crisis_l_english.yml:111`。
- `usm_civilwar.2.2` — 同值合并；来源：`ce_usm_events_l_english.yml:183`, `zz_nesnd_crisis_l_english.yml:112`。
- `usm_civilwar.2.3` — 同值合并；来源：`ce_usm_events_l_english.yml:184`, `zz_nesnd_crisis_l_english.yml:113`。
- `usm_civilwar.2.4` — 同值合并；来源：`ce_usm_events_l_english.yml:185`, `zz_nesnd_crisis_l_english.yml:114`。
- `usm_civilwar.2.5` — 同值合并；来源：`ce_usm_events_l_english.yml:186`, `zz_nesnd_crisis_l_english.yml:115`。
- `usm_civilwar.2.d` — 同值合并；来源：`ce_usm_events_l_english.yml:178`, `zz_nesnd_crisis_l_english.yml:117`。
- `usm_civilwar.2.t` — 同值合并；来源：`ce_usm_events_l_english.yml:177`, `zz_nesnd_crisis_l_english.yml:116`。
- `usm_civilwar.23.1` — 同值合并；来源：`ce_usm_events_l_english.yml:302`, `zz_nesnd_crisis_l_english.yml:130`。
- `usm_civilwar.23.2` — 同值合并；来源：`ce_usm_events_l_english.yml:303`, `zz_nesnd_crisis_l_english.yml:131`。
- `usm_civilwar.23.3` — 同值合并；来源：`ce_usm_events_l_english.yml:304`, `zz_nesnd_crisis_l_english.yml:132`。
- `usm_civilwar.23.d` — 同值合并；来源：`ce_usm_events_l_english.yml:300`, `zz_nesnd_crisis_l_english.yml:134`。
- `usm_civilwar.23.t` — 同值合并；来源：`ce_usm_events_l_english.yml:299`, `zz_nesnd_crisis_l_english.yml:133`。
- `usm_civilwar.3.1` — 同值合并；来源：`ce_usm_events_l_english.yml:195`, `zz_nesnd_crisis_l_english.yml:118`。
- `usm_civilwar.3.d` — 同值合并；来源：`ce_usm_events_l_english.yml:192`, `zz_nesnd_crisis_l_english.yml:120`。
- `usm_civilwar.3.t` — 同值合并；来源：`ce_usm_events_l_english.yml:191`, `zz_nesnd_crisis_l_english.yml:119`。

### `localization/simp_chinese/replace/nesnd_shared_localization_l_simp_chinese.yml`
主题：`nesnd_shared_localization`；分配 key 数：English 0，简中 59。
**simp_chinese**
- `CIR` — 同值合并；来源：`ce_00_countries_l_simp_chinese.yml:1039`, `ce_countries_l_simp_chinese.yml:151`。
- `CIR_ADJ` — 同值合并；来源：`ce_00_countries_l_simp_chinese.yml:1040`, `ce_countries_l_simp_chinese.yml:152`。
- `Qiufu` — 同值合并；来源：`ce_names_l_simp_chinese.yml:92`, `ce_names_l_simp_chinese.yml:95`。
- `RULER_TITLE_NESND_JAPAN_REGENT` — 同值合并；来源：`nesnd_japan_lin_regency_l_simp_chinese.yml:4`, `zzzzzz_nesnd_jp_development_l_simp_chinese.yml:180`。
- `Zhang` — 同值合并；来源：`ce_names_l_simp_chinese.yml:81`, `ce_names_l_simp_chinese.yml:115`。
- `ce_Li` — 同值合并；来源：`ce_names_l_simp_chinese.yml:36`, `ce_names_l_simp_chinese.yml:102`。
- `ce_fra_character_popularity` — 同值合并；来源：`ce_french_empire_journals_l_simp_chinese.yml:12`, `ce_french_empire_journals_l_simp_chinese.yml:74`。
- `ce_usm_conflicts_within_reason` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:118`, `zz_nesnd_crisis_l_simp_chinese.yml:100`。
- `ce_usm_cw_japanese_interest_reason` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:150`, `zz_nesnd_crisis_l_simp_chinese.yml:134`。
- `dyn_c_chechnya_imamate` — 同值合并；来源：`ce_00_countries_l_simp_chinese.yml:1175`, `ce_countries_l_simp_chinese.yml:142`。
- `dyn_c_chechnya_imamate_adj` — 同值合并；来源：`ce_00_countries_l_simp_chinese.yml:1176`, `ce_countries_l_simp_chinese.yml:143`。
- `dyn_c_dutch_east_india` — 同值合并；来源：`ce_00_countries_l_simp_chinese.yml:1165`, `ce_00_countries_l_simp_chinese.yml:1190`。
- `dyn_c_dutch_east_india_adj` — 同值合并；来源：`ce_00_countries_l_simp_chinese.yml:1166`, `ce_00_countries_l_simp_chinese.yml:1191`。
- `flavorCNE.3.d` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:68`, `zz_nesnd_crisis_l_simp_chinese.yml:97`。
- `flavorCNE.3.f` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:69`, `zz_nesnd_crisis_l_simp_chinese.yml:162`。
- `flavorCNE.6.d` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:94`, `zz_nesnd_crisis_l_simp_chinese.yml:94`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:23`。
- `flavorCNE.7.d` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:100`, `zz_nesnd_crisis_l_simp_chinese.yml:95`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:24`。
- `flavorCNE.8.d` — 同值合并；来源：`ce_cne_events_l_simp_chinese.yml:115`, `zz_nesnd_crisis_l_simp_chinese.yml:96`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:25`。
- `flavorUSM.4.1` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:32`, `zz_nesnd_crisis_l_simp_chinese.yml:101`。
- `flavorUSM.4.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:30`, `zz_nesnd_crisis_l_simp_chinese.yml:103`。
- `flavorUSM.4.f` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:31`, `zz_nesnd_crisis_l_simp_chinese.yml:151`。
- `flavorUSM.4.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:29`, `zz_nesnd_crisis_l_simp_chinese.yml:102`。
- `flavorUSM.6.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:80`, `zz_nesnd_crisis_l_simp_chinese.yml:105`。
- `flavorUSM.6.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:79`, `zz_nesnd_crisis_l_simp_chinese.yml:104`。
- `ig_ce_mongol_landowners` — 同值合并；来源：`ce_country_flavor_l_simp_chinese.yml:4`, `ce_scripted_names_l_simp_chinese.yml:4`。
- `ig_ce_mongol_warboss` — 同值合并；来源：`ce_country_flavor_l_simp_chinese.yml:5`, `ce_scripted_names_l_simp_chinese.yml:5`。
- `ig_soldier_officials` — 同值合并；来源：`ce_country_flavor_l_simp_chinese.yml:2`, `ce_scripted_names_l_simp_chinese.yml:2`。
- `nesnd_crisis.30.c` — 同值合并；来源：`zz_nesnd_crisis_l_simp_chinese.yml:16`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:22`。
- `nesnd_crisis.33.d` — 同值合并；来源：`zz_nesnd_crisis_l_simp_chinese.yml:22`, `zzzz_nesnd_cne_reform_l_simp_chinese.yml:21`。
- `party_ce_imperial_con_party` — 同值合并；来源：`ce_country_flavor_l_simp_chinese.yml:22`, `ce_scripted_names_l_simp_chinese.yml:9`。
- `party_ce_imperial_ft_party` — 同值合并；来源：`ce_country_flavor_l_simp_chinese.yml:21`, `ce_scripted_names_l_simp_chinese.yml:8`。
- `usm_civilwar.1.1` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:171`, `zz_nesnd_crisis_l_simp_chinese.yml:107`。
- `usm_civilwar.1.2` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:172`, `zz_nesnd_crisis_l_simp_chinese.yml:108`。
- `usm_civilwar.1.3` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:173`, `zz_nesnd_crisis_l_simp_chinese.yml:109`。
- `usm_civilwar.1.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:169`, `zz_nesnd_crisis_l_simp_chinese.yml:106`。
- `usm_civilwar.10.1` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:235`, `zz_nesnd_crisis_l_simp_chinese.yml:120`。
- `usm_civilwar.10.2` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:236`, `zz_nesnd_crisis_l_simp_chinese.yml:121`。
- `usm_civilwar.10.3` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:237`, `zz_nesnd_crisis_l_simp_chinese.yml:122`。
- `usm_civilwar.10.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:233`, `zz_nesnd_crisis_l_simp_chinese.yml:124`。
- `usm_civilwar.10.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:232`, `zz_nesnd_crisis_l_simp_chinese.yml:123`。
- `usm_civilwar.12.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:246`, `zz_nesnd_crisis_l_simp_chinese.yml:126`。
- `usm_civilwar.12.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:245`, `zz_nesnd_crisis_l_simp_chinese.yml:125`。
- `usm_civilwar.13.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:251`, `zz_nesnd_crisis_l_simp_chinese.yml:128`。
- `usm_civilwar.13.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:250`, `zz_nesnd_crisis_l_simp_chinese.yml:127`。
- `usm_civilwar.2.1` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:184`, `zz_nesnd_crisis_l_simp_chinese.yml:110`。
- `usm_civilwar.2.2` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:185`, `zz_nesnd_crisis_l_simp_chinese.yml:111`。
- `usm_civilwar.2.3` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:186`, `zz_nesnd_crisis_l_simp_chinese.yml:112`。
- `usm_civilwar.2.4` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:187`, `zz_nesnd_crisis_l_simp_chinese.yml:113`。
- `usm_civilwar.2.5` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:188`, `zz_nesnd_crisis_l_simp_chinese.yml:114`。
- `usm_civilwar.2.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:179`, `zz_nesnd_crisis_l_simp_chinese.yml:116`。
- `usm_civilwar.2.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:178`, `zz_nesnd_crisis_l_simp_chinese.yml:115`。
- `usm_civilwar.23.1` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:304`, `zz_nesnd_crisis_l_simp_chinese.yml:129`。
- `usm_civilwar.23.2` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:305`, `zz_nesnd_crisis_l_simp_chinese.yml:130`。
- `usm_civilwar.23.3` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:306`, `zz_nesnd_crisis_l_simp_chinese.yml:131`。
- `usm_civilwar.23.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:302`, `zz_nesnd_crisis_l_simp_chinese.yml:133`。
- `usm_civilwar.23.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:301`, `zz_nesnd_crisis_l_simp_chinese.yml:132`。
- `usm_civilwar.3.1` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:197`, `zz_nesnd_crisis_l_simp_chinese.yml:117`。
- `usm_civilwar.3.d` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:194`, `zz_nesnd_crisis_l_simp_chinese.yml:119`。
- `usm_civilwar.3.t` — 同值合并；来源：`ce_usm_events_l_simp_chinese.yml:193`, `zz_nesnd_crisis_l_simp_chinese.yml:118`。

### `localization/english/replace/nesnd_south_journal_ui_l_english.yml`
主题：`nesnd_south_journal_ui`；分配 key 数：English 8，简中 0。
**english**
- `nesnd_south_compact_bar_desc` — 同值合并；来源：`zz_nesnd_crisis_l_english.yml:151`, `zzzzz_nesnd_south_journal_ui_l_english.yml:9`。
- `nesnd_south_compact_detail_tt` — 同值合并；来源：`zzzzz_nesnd_south_journal_ui_l_english.yml:11`, `zzzzzz_nesnd_succession_board_l_english.yml:34`, `zzzzzzzz_nesnd_south_politics_l_english.yml:52`。
- `nesnd_south_politics_summary` — 同值合并；来源：`zzzzzzzz_nesnd_south_politics_l_english.yml:8`, `zzzzzzzzz_nesnd_south_peace_gates_l_english.yml:5`。
- `nesnd_south_pressure_bar_desc` — 值冲突需按证据选定；建议：keep South journal UI English value; crisis English occurrence contains Chinese；来源：`zz_nesnd_crisis_l_english.yml:149`, `zzzzz_nesnd_south_journal_ui_l_english.yml:8`。
- `nesnd_south_pressure_detail_tt` — 同值合并；来源：`zzzzz_nesnd_south_journal_ui_l_english.yml:10`, `zzzzzzzzzz_nesnd_court_followup_l_english.yml:27`。
- `nesnd_south_rules` — 值冲突需按证据选定；建议：keep South journal UI English value; crisis English occurrence contains Chinese；来源：`zz_nesnd_crisis_l_english.yml:147`, `zzzzz_nesnd_south_journal_ui_l_english.yml:12`。
- `nesnd_south_status_succession` — 同值合并；来源：`zz_nesnd_crisis_l_english.yml:146`, `zzzzz_nesnd_south_journal_ui_l_english.yml:13`。
- `nesnd_south_succession_board_reason` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_english.yml:4`, `zzzzzzz_nesnd_ming_court_l_english.yml:22`。

### `localization/simp_chinese/replace/nesnd_south_journal_ui_l_simp_chinese.yml`
主题：`nesnd_south_journal_ui`；分配 key 数：English 0，简中 8。
**simp_chinese**
- `nesnd_south_compact_bar_desc` — 同值合并；来源：`zz_nesnd_crisis_l_simp_chinese.yml:150`, `zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml:9`。
- `nesnd_south_compact_detail_tt` — 同值合并；来源：`zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml:11`, `zzzzzz_nesnd_succession_board_l_simp_chinese.yml:34`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:52`。
- `nesnd_south_politics_summary` — 同值合并；来源：`zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:8`, `zzzzzzzzz_nesnd_south_peace_gates_l_simp_chinese.yml:5`。
- `nesnd_south_pressure_bar_desc` — 值冲突需按证据选定；建议：prefer_reviewed_UI_value_check_English；来源：`zz_nesnd_crisis_l_simp_chinese.yml:148`, `zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml:8`。
- `nesnd_south_pressure_detail_tt` — 同值合并；来源：`zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml:10`, `zzzzzzzzzz_nesnd_court_followup_l_simp_chinese.yml:27`。
- `nesnd_south_rules` — 值冲突需按证据选定；建议：prefer_reviewed_UI_value_check_English；来源：`zz_nesnd_crisis_l_simp_chinese.yml:146`, `zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml:12`。
- `nesnd_south_status_succession` — 同值合并；来源：`zz_nesnd_crisis_l_simp_chinese.yml:145`, `zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml:13`。
- `nesnd_south_succession_board_reason` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:4`, `zzzzzzz_nesnd_ming_court_l_simp_chinese.yml:22`。

### `localization/english/replace/nesnd_succession_board_l_english.yml`
主题：`nesnd_succession_board`；分配 key 数：English 9，简中 0。
**english**
- `nesnd_board_compact_bar_desc` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_english.yml:31`, `zzzzzzzz_nesnd_south_politics_l_english.yml:7`。
- `nesnd_board_compact_bar_name` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_english.yml:29`, `zzzzzzzz_nesnd_south_politics_l_english.yml:6`。
- `nesnd_board_country_metrics` — 值冲突需按证据选定；建议：preserve_complete_metric_payload_if_current；来源：`zzzzzz_nesnd_succession_board_l_english.yml:7`, `zzzzzzzz_nesnd_south_politics_l_english.yml:53`。
- `nesnd_board_ming_bar_desc` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_english.yml:27`, `zzzzzzzz_nesnd_south_politics_l_english.yml:4`。
- `nesnd_board_ming_bar_name` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_english.yml:25`, `zzzzzzzz_nesnd_south_politics_l_english.yml:2`。
- `nesnd_board_stance_effect_tt` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_english.yml:16`, `zzzzzzzz_nesnd_south_politics_l_english.yml:17`。
- `nesnd_board_wu_bar_desc` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_english.yml:28`, `zzzzzzzz_nesnd_south_politics_l_english.yml:5`。
- `nesnd_board_wu_bar_name` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_english.yml:26`, `zzzzzzzz_nesnd_south_politics_l_english.yml:3`。
- `nesnd_federal_compact_button_outcome_tt` — 值冲突需按证据选定；建议：keep succession-board English value; crisis-rules English occurrence contains Chinese；来源：`zz_nesnd_crisis_rules_l_english.yml:14`, `zzzzzz_nesnd_succession_board_l_english.yml:33`。

### `localization/simp_chinese/replace/nesnd_succession_board_l_simp_chinese.yml`
主题：`nesnd_succession_board`；分配 key 数：English 0，简中 9。
**simp_chinese**
- `nesnd_board_compact_bar_desc` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:31`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:7`。
- `nesnd_board_compact_bar_name` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:29`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:6`。
- `nesnd_board_country_metrics` — 值冲突需按证据选定；建议：preserve_complete_metric_payload_if_current；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:7`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:53`。
- `nesnd_board_ming_bar_desc` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:27`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:4`。
- `nesnd_board_ming_bar_name` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:25`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:2`。
- `nesnd_board_stance_effect_tt` — 同值合并；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:16`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:17`。
- `nesnd_board_wu_bar_desc` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:28`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:5`。
- `nesnd_board_wu_bar_name` — 值冲突需按证据选定；建议：prefer_board-specific_value；来源：`zzzzzz_nesnd_succession_board_l_simp_chinese.yml:26`, `zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:3`。
- `nesnd_federal_compact_button_outcome_tt` — 值冲突需按证据选定；来源：`zz_nesnd_crisis_rules_l_simp_chinese.yml:14`, `zzzzzz_nesnd_succession_board_l_simp_chinese.yml:33`。

## 有可核实文字依据的取值建议

- **HUS registration.1/.2 共享事件 key**：当前 old owner 是 `zzzz_nesnd_hus_social_hierarchy`，A2 新稿在 `zz...a2_native_americas`。建议按 A2 专题唯一归属 `nesnd_native_americas_l_<locale>.yml`。A2 逐键对读在 `reports/canon-route-execution-20261104/batch-a2-writing-comparison.md:122-126`，比 A1 旧表述具体并对应当前四州汗国/迁徙结算。JSON保留两份原值；不改脚本事件 key。
- **日本统一与摄政**：`nesnd_japan_reunification_reason/status/goal` 取已逐项对读的 2026-11-02 日本文案，owner 建议 `nesnd_japan_l_<locale>.yml`；具体证据 `reports/japan-development-20261102/writing-comparison-nation-politics.md:127-129`。`gov_nesnd_japan_lin_regency_desc` 取该日 Lin 摄政复审值，证据 `writing-comparison-foreign-korea.md:132`。历史重复值留在 VCS 中。
- **QE1 balance bar**：严格冻结现有 Qin/Persia 审稿值；只把重复 key 唯一归属至 `nesnd_qin_persia_l_<locale>.yml`。`reports/qin-persia-20261102/writing-items.json:39-41` 是取值来源；用户明确本轮不得改 QE1 文案。
- **CNE 地权主题**：重复 `nesnd_land_*` / `cne_landreform_completion_tracker_*` 建议统一归属 `nesnd_cne_land_reform_l_<locale>.yml`，按 `reports/canon-prose-20261102/cne-writing-comparison.md` 逐键 keep/revise 结论选用已审文本。CNE event failure title/reason 的 EN `zz_nesnd_crisis_l_english` 行含中文；不得把这份中文值保留为英文。该组在两语言当前值与 2026-10-30前版本均逐条附 JSON。
- **其余可定语言/专题的 EN 冲突**：`STATE_SICHUAN` 在 map owner 保留为 “Chengdu”（来自 per-USM 现有英文值；同键 map 简中为“成都”）；`nesnd_federal_compact_button_outcome_tt` 取 succession-board 英文；`nesnd_land_review_outcome_tt` 取 CNE-reform 英文；`nesnd_protect_chen_button_requirements` 取 Chen-security 英文但不改条件语义；`nesnd_south_pressure_bar_desc` / `nesnd_south_rules` 取 South journal UI 英文。它们在对应 `zz_nesnd_crisis[_rules]_l_english` 的重复值含中文，来源与字符串均逐项列于 JSON。
- **HUS registration** 是唯一已找到后来完整对读直接说明重复值取舍的事件文案。其他不同值冲突仍列所有来源和历史原值，由 root 最终选择；不能仅以 z 数多、文件更晚或列表顺序选值。
- `NOT_TRIGGER_MARKET_ACCESS_LESS_THAN` 在简中 `ce_cne_events` 同一文件出现两次：一个表达动态 `$NUM` / `$CURRENT_VALUE`，另一个写死 85%。需要结合调用/显示上下文决定保留哪一条，最后该文件内也只能有一个 key。
- `nesnd_board_*_bar_*` 和 `nesnd_board_country_metrics` 有不同值：专用 board source 对登记国支持率更明确；south-politics copy 的 `country_metrics` 多出 `nesnd_south_ready_loc`。先核当前 UI 是否包含该字段，再把选定完整字符串迁入唯一 board 文件。
- `nesnd_south_rules` / `nesnd_south_pressure_bar_desc`、India unrest、South maintenance feedback、Chen button guard 和 country/state labels 的 source value 在 JSON 中完整列出；没有逐条批准来源就不宣称已经定稿。Chen JE 新条件复核应独立返回后再处理其文字；本计划不碰该逻辑。

## 推荐按专题收拢的唯一 owner

|专题|唯一 owner 文件（英文/简中分别加 `_l_english.yml` / `_l_simp_chinese.yml`）|范围/备注|
|---|---|---|
|Qin/Persia|`nesnd_qin_persia`|现有 QE1 文案锁定；合并重复定义不改文字。|
|CNE land reform|`nesnd_cne_land_reform`|CE CNE failure JE、land progress/status、tracker tooltips；把冲突值按审稿证据选定。|
|Japan|`nesnd_japan`|统一目标、Lin 摄政说明和共用日方叙事；使用已审修订。|
|HUS native / A2|`nesnd_native_americas`|HUS event `.1/.2` 当前采用 A2 最终稿。|
|India|`nesnd_india`|印度社会动荡与团结政策同一 owner。|
|Southern succession|`nesnd_succession_board`|统绪/吴国 bar、board metrics、邦国契约按钮 outcome。|
|South journal UI|`nesnd_south_journal_ui`|南朝压力、规则 tooltip 与状态展示。|
|Chen security|`nesnd_chen_security`|保留已写条件文案；等待独立 JE 条件问题结论。|
|Shared modifier feedback|`nesnd_shared_feedback`|跨系统通用 modifier maintenance helper。|
|Legacy country/party names|`ce_countries`, `ce_country_flavor`, `ce_scripted_names`|GNG 名称与原版/既有主题名按代码消费者和用户原稿确定唯一源。|
|Map state names|`map/ce_states`|`STATE_SICHUAN` 保留 map locale 主文件。|

## 非本地化 `zz` 脚本改名计划

27个 z 脚本文件全部保留内容、定义、目标、语言以外的目录和对象 ID；新 basename 采用 `nesnd_<topic>_overrides.txt`。完整旧→新路径、每个 REPLACE target 和跨 M 定义行号列在 JSON 的 `script_rename_plan`。不删除空文件；当前 `zz_ce_transferred_garrisons.txt` 只有空 `MILITARY_FORMATIONS = {}`。

- 跨文件自定义 REPLACE 目标存在三组：`HNA` / `SIH` 在 `common/dynamic_country_names/00_dynamic_country_names.txt` 同目录定义；七个 `nesnd_rg_*` 在 `common/journal_entries/nesnd_regional_development.txt` 定义。为不依赖加载文件顺序，把每个 base definition 与紧随其后的现有 REPLACE 合并到同一 `.txt`，定义先、替换后；不改变内容。
- `je_veiled_protectorate` 是 GAME 原版对象，继续留在可读的 `nesnd_regional_development_overrides.txt`，但自定义目标应先在本 MOD 同一基础文件内归并后才列该 vanilla override。其余 REPLACE target 与 GAME 对象对应，不存在另一个 M 同目录定义。盘点文件里有 23 个 REPLACE 文件、0 个 INJECT。
- 本地/游戏目录文档没有给出可证明的跨文件 lexical load order，故计划只通过合并两组同 MOD 自定义目标避免该依赖。其他对象按当前数据库类别保存，所有 REPLACE 内容不变；不主张目录覆盖行为可由普通数据库推断。

## 步骤建议（仍待 root 决策）

1. root 确认 canonical owner 命名、争议 key 候选值与保留规则；QE1 文案锁定。
2. 建立 EN/简中专题目标文件，搬移选定原值，核对 BOM、语言头和 key-value 数量；原值、SHA 与用户原稿对照保存在 WORK report，Git 保留完整源码历史。
3. 逐文件删除重复定义，只保留唯一 owner；先不改任何脚本 key 或 gameplay。
4. 脚本文件按表改 informative basename；同 MOD 的 HNA/SIH 与 `nesnd_rg_*` 定义/REPLACE 各自放进同一文件顺序闭包。
5. 检查唯一 key、locale pair、引用闭包和 BOM；这只是静态检查，不能说明游戏内有效语言加载或最终行为。

## 限制

此交付是 PLAN；未动源码、未测试、未开游戏。除明确列出的审稿证据外，其余分歧不是我代替 root 作出最终文案裁决。确切值及前版源快照候选查看同目录 JSON；该快照不单独证明文本为直接用户原稿，作者来源须按项目原始文档/专项审稿确认。。
