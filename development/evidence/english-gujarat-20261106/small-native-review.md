# Small states and Native Americas English synchronization

## Plan recorded before editing

Scope: only `localization/english/replace/nesnd_small_states_l_english.yml` and `localization/english/replace/nesnd_native_americas_l_english.yml`. The current Chinese counterparts are the semantic authority. Preserve keys, BOM, dynamic expressions, concepts, numbers, and Task44 regional UI additions. No gameplay, Chinese, Git or engine changes.

1. Read current bilingual files and the actual events, journal entries, buttons, effects and regional customizable-localization routes.
2. Recover the social and political causes omitted by old English summaries. Give choices a speaker's voice. Keep operation tooltips concise and factual.
3. Check region-specific events against their non-generic homeland guards, keep the new Australia/New Zealand/Burma/Siam scope routing intact, and preserve distinct khanate outcome branches.
4. Record every key as retained or rewritten, show representative old-English / current-Chinese / final-English comparisons, and check encoding, entry identity and dynamic tokens. Root performs final review and broader validation.

Source model metadata: awaiting parent confirmation; do not infer runtime model from task name. Delegation evidence: parent task `/root/astra_english_small_native` assigned these two files explicitly.

Author samples: `f18b6c4` CNE and Poland Chinese replace files. CNE `ce_cne_land_reform_reason` explains who loses land, who receives it and why the state resumes reform; `flavorCNE.1.1` is a political assertion by the option's speaker. Poland `je_ce_the_polish_problem_reason` develops a national grievance through concrete territorial limitations; `ce_support_polish_problem_btn_desc` states a commitment directly. These support explicit interests, causal narrative and decisive options, rather than bureaucratic summaries.

Current native baseline: catalog status CURRENT, Victoria 3 1.15.0 / build 26453692. Native counterpart chain inspected: GAME `common/journal_entries/00_canada_australia.txt:3,110` -> `common/scripted_buttons/06_canada_australia_buttons.txt:1` -> `common/customizable_localization/victoria_ip4_custom_loc.txt:1` -> `localization/english/content_1_l_english.yml:781-784` and `ip4_misc_01_l_english.yml:635-639`. Applicable precedent: political narrative in JE reasons, action/eligibility separation, and country-context dynamic description. No new engine interface is introduced.

MOD chains read: `events/nesnd_small_states.txt`, `common/journal_entries/nesnd_small_states.txt`, `common/customizable_localization/nesnd_small_regions.txt`, `common/scripted_effects/nesnd_small_states.txt`; `events/nesnd_american_restoration.txt`, `events/nesnd_native_khanate.txt`, `common/scripted_buttons/nesnd_american_restoration.txt` and related actual effect definitions. Region-specific .2/.6 prose is guarded by homeland selection and valid targets; generic reselection uses generic prose. Native .2 success distinguishes two, one and zero humiliation outcomes. Requests, delays and unsuccessful exits must not claim unimplemented treaty revocation or victories.

The independent pre-change backup is `WORK/backups/pre-change-english-gujarat-20261106T212037Z/mod`. Validation remains external/static; the game is not launched.

## Completed editorial review and static checks
Configured delegation: **gpt-6-astra / high**, confirmed by parent from requested spawn metadata. This records configured delegation, not an independently introspected backend identity. No further agents were spawned.
Reviewed all **410** entries. Rewrote **148** entries (small states 95/216; Native Americas 53/194), retained **262** entries after comparison. Root final review remains separate.
Targeted external checks passed: both BOM/header and CRLF conventions; identical key order/count; exact bilingual key sets; no added duplicate keys; exact per-entry dynamic-expression, localization-reference, formatting-tag and numeric-token preservation; no CJK in English; unchanged line counts; Task44 regional UI keys retained byte-for-byte; pre-change English sources exactly match the independent backup. These checks are **STATIC_PASS / ENGINE_NOT_RUN**. They do not certify layout or runtime behaviour.
The full before/after payload is `small-native-changes.json`. `rewrite-small-native.py` preserves the first candidate construction, and `polish-small-native.py` records the second editorial pass: awkward legacy law tooltips were rewritten, native law names checked in GAME/localization/english/laws_l_english.yml:642-702,760-762,991-1001, and the ambiguous title “People to Govern” became “Hands for Local Government”.
No permanent skill change was needed. Existing rules on social causation, action/eligibility separation and outcome-specific prose covered the findings.
## Discrepancies resolved and boundaries
- Old small-state reasons and completion events omitted most of the Chinese social argument: production supports household livelihoods, taxation supports services, and public learning changes political expectations. The new English restores those connections.
- Old generic success prose claimed foreign agreements supplied autonomy. Current script can qualify through other defence arrangements; the translation now follows the Chinese claim of market connections and defensive capacity. Regional .2/.6 versions remain attached only to valid original homeland groups.
- Autonomy/independence/defence tooltips contained “native”, “verifies the outcome”, “actually independent” and “counts only” implementation wording. They now describe the actual proposal and result. Market-request failure after thirty days remains explicit and does not imply treaty cancellation.
- The old regional-target tooltip omitted the homeland-versus-national population denominator. The English now includes it, without altering the 100,000 and 5% thresholds. All newly introduced Task44 UI values and functions remain unchanged.
- Exodus text retained the seventy/thirty probability for each community and all four destinations/result branches, but dropped the tutorial about why population totals do not form an exact ratio. The Chinese instead supplies social consequences, which are restored. Actual source: common/scripted_effects/nesnd_a2_manchu_exodus.txt:14-38.
- Restoration termination and its notification now describe a struggle interrupted by political/territorial changes and our failure to annex the rival. They do not claim that neither side could annex anyone, nor recast the exit as peaceful settlement.
- The refugee option restores the Chinese Earth Mother invocation instead of the old administrative “Let them settle here.” It is translated as an option, not attributed to an external historical quotation.
- The khanate treaty event retains withdrawal of treaties containing alliance/defensive-pact articles, loss of other articles in those same treaties, and penalties on the withdrawing state. The third-party exclusion sentence belonged to implementation commentary and is absent from the current Chinese. Actual source: common/scripted_effects/nesnd_native_khanate.txt:157-178.
- Existing fallback keys nesnd_hus_registration.2.d and nesnd_native_khanate.2.d were retained as keys; the first is already synchronized, while the second was rewritten but is not the active first_valid outcome branch. The three active .2.both/.one/.none texts are individually synchronized. No unused fallback is counted as proof that an active display was repaired.
- No new gameplay discrepancy was identified within the inspected translation contracts. Source assertions and engine execution remain distinct; root should perform final wording and repository-wide reference checks.
## Representative bilingual comparisons
### `nesnd_small_livelihood_journal_reason` (English line 64)
**Old English:** Farmers, artisans and merchants bear the costs of rent, taxation and changing markets. Greater autonomy requires income from local production and people trained to staff schools and public offices. Foreign investment can bring money and expertise, and support from an overlord can ease the burden, but the country must still sustain itself through local work and enterprise.
**Current Chinese:** 小国的自主，往往要从普通人的生计里寻找根据。农户付得起税，雇工找得到活计，商人能够把货物运到有买主的地方，政府才有供养行政、教育与防务的财源。若生产者终日困于地租、债务和失业，再多宏大的国事也只能向他们索取。\n\n外国资本可以带来资金与技术，宗主的支持也能分担一些负担。本国若要在这些关系中取得更多说话的余地，就须使地方产业能够经营，使民众有机会学会新的本领。国计的根基，正在这些看似细小的生活之中。
**Final English:** A small country's freedom of action often rests on the livelihoods of ordinary people. Farmers must be able to pay their taxes, labourers to find work, and merchants to carry goods to willing buyers before the government can afford administration, education and defence. When producers are overwhelmed by rent, debt and unemployment, every grand undertaking makes another demand on people who can scarcely bear it.\n\nForeign capital can bring money and knowledge, and an overlord's support may ease some burdens. To have a stronger voice in these relationships, the country needs viable local industries and opportunities for its people to learn new skills. The means to conduct affairs of state begin in these seemingly modest concerns.
**Disposition:** Editorial pass. Restore actors, livelihoods, political interests and causal development omitted by old English summary.
### `nesnd_small_states.2.far_south` (English line 57)
**Old English:** Australia's population and processing centres now maintain effective links with local production in New Zealand. Working ports carry goods to market. These industries support the Far South's growth and provide revenue for local services.
**Current Chinese:** 澳洲与新西兰之间的海面，正在成为两地生产者共同的商路。港口雇得起工人，地方产业也有了通向市场的出路，远南的经营因而不再只系于一处产地。\n\n农户与雇工的生计渐有根基，政府也能从这些经营中取得收入。接下来要维持的学校与地方事务，终究还要靠往来两地的货物和生产它们的人供养。
**Final English:** The sea between Australia and New Zealand has become a common trading route for their producers. Ports can hire workers and local industries have found outlets for their goods, giving the Far South more than a single centre of production on which to depend.\n\nFarmers and labourers have firmer livelihoods, and the government can draw revenue from their work. The schools and local services it hopes to maintain will depend on the goods crossing these waters, and on the people who produce them.
**Disposition:** Editorial pass. Restore actors, livelihoods, political interests and causal development omitted by old English summary.
### `nesnd_small_states.6.burma` (English line 61)
**Old English:** Production and public services have gained a stable footing in the upper country and the lower reaches around $STATE_PEGU$. Markets and transport linking the two have increased public revenue, while schools train new personnel. Burma can use these strengths to seek better terms abroad.
**Current Chinese:** 上游与$STATE_PEGU$下游的生产、交通和公共事务已有了较为稳定的根基。政府能够取得收入，地方也有人从事行政与教育，上下游的联系因而超出了货物的往来。\n\n缅甸可以凭这些积累安排自己的国事。对外关系仍须审慎经营，但面对外部要求时，本国已有更多可以依靠的财源与人才。
**Final English:** Production, transport and public services have gained a more secure footing in the upper country and the lower reaches around $STATE_PEGU$. The government has revenue, and local people can undertake administration and teaching. Relations between the two regions now extend well beyond the exchange of goods.\n\nBurma can draw on these resources to conduct its own affairs. Foreign relations will still require care, but the country has more wealth and trained people on which to rely when faced with demands from abroad.
**Disposition:** Editorial pass. Restore actors, livelihoods, political interests and causal development omitted by old English summary.
### `nesnd_small_states.10.labor` (English line 169)
**Old English:** Hardship among labourers has strengthened the labour movement. Wages, hours and protection at work have become matters of dispute. The government's approach to organisation and law will affect the balance between workers and employers.
**Current Chinese:** 雇工的生活日渐困顿，劳动运动因而取得了地方支持。工人要求讨论工资、工时与工作中的保障，希望不再独自同雇主争执。对雇主而言，这些要求会改变经营的成本，也会改变他们支配劳动的余地。\n\n政府须决定怎样对待这些组织。容许工人发声、承诺立法，或派警察压制，都将影响劳资双方今后凭什么争取自己的利益。
**Final English:** Growing hardship among labourers has brought local support to the labour movement. Workers want a voice in wages, hours and protection at work, hoping to avoid facing their employers alone. Employers see demands that will alter their costs and their authority over labour.\n\nThe government must decide how to treat these organisations. Allowing workers to speak, promising legislation or sending in the police will shape the means by which both sides can defend their interests.
**Disposition:** Editorial pass. Restore actors, livelihoods, political interests and causal development omitted by old English summary.
### `nesnd_small_states.10.promise_labor` (English line 177)
**Old English:** Promise protection at work.
**Current Chinese:** 劳动者应当得到法律保障。
**Final English:** Working people deserve the protection of the law.
**Disposition:** Editorial pass. Restore the choice as a concrete political stance or action.
### `nesnd_small_request_autonomy_tt` (English line 111)
**Old English:** Ask the actual direct overlord. Approval applies the native autonomy increase, verifies the outcome, reduces liberty desire and establishes a truce.
**Current Chinese:** 向直接宗主请求提高自治权。批准后提高自治权，减少自由渴望，并与宗主订立停战。
**Final English:** Ask our direct overlord for greater autonomy. Approval increases autonomy, reduces Liberty Desire and establishes a truce with the overlord.
**Disposition:** Editorial pass. Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording.
### `nesnd_small_defence_fra_desc` (English line 119)
**Old English:** Mutual defence requires two independent countries and an effective treaty.
**Current Chinese:** 商谈防御条约，约定共同应对外来进攻。
**Final English:** Negotiate a defensive treaty, agreeing to stand together against attacks from abroad.
**Disposition:** Editorial pass. Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery.
### `nesnd_small_regional_targets_tt` (English line 29)
**Old English:** Both selected regions retain at least 100,000 people and 5% of the relevant population; their directly owned centres each retain 5%
**Current Chinese:** 两个地区各有至少10万人，且人口各达到计算范围的5%。两地支点仍属本国，人口也各达5%。本土地理目标按本土人口计算，其他地区目标按全国人口计算。
**Final English:** Each region has at least 100,000 people and 5% of the relevant population. Both regional centres remain under our control and each has at least 5%. Homeland targets use the homeland population; other regional targets use the national population.
**Disposition:** Editorial pass. Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording.
### `nesnd_small_working_status` (English line 83)
**Old English:** Conditions are met this month; observation can continue.
**Current Chinese:** 本月各项条件满足，达标月数增加。
**Final English:** All conditions are met this month, adding to the total of qualifying months.
**Disposition:** Editorial pass. Describe present political or progress state directly.
### `nesnd_small_learning` (English line 197)
**Old English:** Local Exchange of Knowledge
**Current Chinese:** 地方学识的传播
**Final English:** The Spread of Local Learning
**Disposition:** Editorial pass. Align established display wording with current Chinese and actual field purpose.
### `nesnd_american_restoration_reason` (English line 14)
**Old English:** The heirs of Moctezuma and the Andean court claim different inheritances. Both confront a question the republics have left unresolved: can Indigenous communities control their land and local government? Dynastic supporters appeal to old compacts, while rural communities resist dispossession. Recognition, negotiation, and repression offer sharply different futures.
**Current Chinese:** 蒙特祖玛王族与安第斯宫廷的复兴，得到了一批原住民村社的支持。共和国曾许诺自由，新的统治者却照样侵夺公地、征取税款。对于仍在田间劳作的人而言，首都换了一面旗帜，并没有减轻他们肩上的负担。\n\n旧王朝的拥护者正凭这种不满重新活动。他们以保护公地和地方权利为条件，争取村社的人口与武装。乡村也希望借君主的威望，摆脱新贵对自己的侵夺。政府如今须决定，是承认王朝的权利，通过地方议会与地权改革分化它的支持者，还是派军队去压下这些复统的呼声。
**Final English:** The restoration of the house of Moctezuma and the Andean court has won support among Indigenous villages. The republics promised liberty, yet their new rulers still encroach on common land and exact taxes. For those who work the fields, a change of flag in the capital has done little to lighten their burden.\n\nSupporters of the old dynasties are turning this resentment to their advantage. They promise to protect common land and local rights in return for the villages' people and arms. Rural communities, in turn, hope to use a monarch's prestige to resist the depredations of the new elite. The government must decide whether to recognise the dynasty, draw away its supporters through local councils and land reform, or send the army to silence the calls for restoration.
**Disposition:** Editorial pass. Restore actors, livelihoods, political interests and causal development omitted by old English summary.
### `nesnd_american_restoration.2.a` (English line 52)
**Old English:** Let them settle here.
**Current Chinese:** 望大地母神恩泽，维护大地沃土于阳光中...
**Final English:** May the Earth Mother bless us, and keep the soil fertile beneath the sun...
**Disposition:** Editorial pass. Restore the choice as a concrete political stance or action.
### `nesnd_american_restoration.6.d` (English line 63)
**Old English:** This struggle has not brought unification. The government must reconsider its relations with local powers in light of the present borders.
**Current Chinese:** 国土与政权的变动打断了复统之争。原先与本国争夺统治权的对手已无法继续参战，我们却也没有接管它的全部国土。\n\n局势已经改变，政府须重新判断周围的敌友。此前未能解决的地方问题，只得在新的疆界之内继续处置。
**Final English:** Changes in territory and government have interrupted the restoration struggle. Our former rival can no longer continue the fight, yet we have not taken possession of all its lands.\n\nThe government must reassess its friends and enemies in these altered circumstances. Unresolved local questions will have to be addressed within the new borders.
**Disposition:** Editorial pass. State interruption/non-annexation without inventing victory, peace agreement or completed intervention war.
### `nesnd_a2_exodus_both_desc` (English line 112)
**Old English:** Manchu and Mongol communities have left for [SCOPE.sCountry('nesnd_a2_cne_country').GetName] or the west of [SCOPE.sCountry('nesnd_a2_usa_country').GetName]. Each community has a seventy percent chance of choosing the former and thirty percent the latter. Community sizes differ, so the actual population is not divided in an exact seventy-to-thirty ratio.
**Current Chinese:** 登记完成以后，仍被留在二等户籍中的满蒙社区开始离开共和国。有人投向[SCOPE.sCountry('nesnd_a2_cne_country').GetName]，有人前往[SCOPE.sCountry('nesnd_a2_usa_country').GetName]西部，把亲族与旧日联系一同带往新的土地。\n\n各社区有七成概率迁往前者、三成概率迁往后者。人们带走的不只是人口与家当，也带走了在这里取得平等身份的期待。
**Final English:** With registration complete, Manchu and Mongol communities left in the second tier have begun to leave the republic. Some have gone to [SCOPE.sCountry('nesnd_a2_cne_country').GetName], others to the west of [SCOPE.sCountry('nesnd_a2_usa_country').GetName], carrying their families and old ties to new lands.\n\nEach community has a seventy percent chance of choosing the former destination and thirty percent of choosing the latter. Along with their people and possessions, the republic is losing the hopes they once held of an equal place within it.
**Disposition:** Editorial pass. Restore registration grievance, family migration and branch-specific consequences; remove implementation commentary.
### `nesnd_native_khanate.2.none` (English line 131)
**Old English:** Both interventions have ended. Though it has forced neither opponent to accept humiliation, the khanate has preserved its government. Its communities must share the burdens of taxation and defence to sustain the new state.
**Current Chinese:** 两国的干涉都已结束。汗国没有迫使对手接受羞辱，却保住了自己的政府，草原上的共同体也得以继续经营新家园。\n\n新汗仍须依靠地方首领与迁民的支持。怎样负担税收与防务，怎样维护各地的权利，将决定这份为求生存而结成的盟约能够维持多久。
**Final English:** Both interventions have ended. The khanate forced neither opponent to accept humiliation, but it has preserved its government. The communities of the Plains can continue to build their new homes.\n\nThe new khan still depends on local leaders and settlers for support. How taxes and defence are shared, and how local rights are protected, will determine how long this compact for survival can endure.
**Disposition:** Editorial pass. Preserve distinct intervention outcome and restore peacetime interests of khan and communities.
### `nesnd_native_khanate.4.d` (English line 148)
**Old English:** [SCOPE.sCountry('nesnd_khanate_opponent').GetName] has withdrawn from treaties with the khanate containing an alliance or defensive pact, clearing the way for intervention. Any trade or other provisions in the same treaties end with them. The withdrawing country bears the diplomatic cost of breaking its word. Neither country's treaties with third powers are included.
**Current Chinese:** [SCOPE.sCountry('nesnd_khanate_opponent').GetName]已经退出同汗国之间载有联盟或防御协定的条约，为干涉清除障碍。曾经用来保证彼此安全的承诺，如今让位于吞并与领土的要求。\n\n退出的条约若还载有贸易或其他约定，那些安排也一同终止，毁约的代价由退出国承担。汗国原先可以依靠的这段关系，已经随着战争的准备破裂。
**Final English:** [SCOPE.sCountry('nesnd_khanate_opponent').GetName] has withdrawn from treaties with the khanate containing an alliance or defensive pact, clearing the way for intervention. Promises once intended to secure both countries have given way to demands for annexation and territory.\n\nAny trade or other provisions within those treaties end with them, and the withdrawing country bears the cost of breaking its word. A relationship on which the khanate could once rely has broken under the preparations for war.
**Disposition:** Editorial pass. Restore treaty breakdown narrative; retain same-treaty trade losses and withdrawal cost, remove developer exclusion note.
### `notification_nesnd_restoration_dispute_ended_notice_desc` (English line 186)
**Old English:** The restoration dispute involving [SCOPE.sCountry('nesnd_restoration_notice_actor').GetName] has ended without either side annexing the other.
**Current Chinese:** 国土与政权的变动打断了[SCOPE.sCountry('nesnd_restoration_notice_actor').GetName]卷入的复统争夺，本国未通过吞并对手完成统一。
**Final English:** Changes in territory and government have interrupted the restoration struggle involving [SCOPE.sCountry('nesnd_restoration_notice_actor').GetName]. Our country has not unified the land by annexing its opponent.
**Disposition:** Editorial pass. State interruption/non-annexation without inventing victory, peace agreement or completed intervention war.
## Full entry dispositions
### nesnd_small_states
| Line | Key | Disposition | Reason |
|---:|---|---|---|
| 2 | `nesnd_small_state_capital` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 3 | `state_pop_support_movement_land_reform_mult_desc` | Retained — editorial pass | Existing English conveys the current Chinese meaning; no stale narrative omitted. |
| 4 | `nesnd_small_order_available_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 5 | `nesnd_small_retarget_ready_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 6 | `nesnd_small_regional_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 7 | `nesnd_small_regional_access_status` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 8 | `nesnd_small_region_australia` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 9 | `nesnd_small_region_new_zealand` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 10 | `nesnd_small_region_upper_burma` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 11 | `nesnd_small_region_lower_burma` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 12 | `nesnd_small_region_siam_interior` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 13 | `nesnd_small_region_siam_outer` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 14 | `nesnd_small_region_anchor` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 15 | `nesnd_small_region_other_states` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 16 | `nesnd_small_region_unselected` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 17 | `nesnd_small_employment_coverage_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 18 | `nesnd_small_national_access_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 19 | `nesnd_small_first_access_tt` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 20 | `nesnd_small_second_access_tt` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 21 | `nesnd_small_first_industry_tt` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 22 | `nesnd_small_second_industry_tt` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 23 | `nesnd_small_two_industries_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 24 | `nesnd_small_first_port_tt` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 25 | `nesnd_small_second_port_tt` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 26 | `nesnd_small_retarget_size_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 27 | `nesnd_small_retarget_change_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 28 | `nesnd_small_no_regional_crisis_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 29 | `nesnd_small_regional_targets_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 30 | `nesnd_small_governance_completed_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 31 | `nesnd_small_specialisation_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 32 | `nesnd_small_population` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 33 | `nesnd_small_populated_states` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 34 | `nesnd_small_scale` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 35 | `nesnd_small_admin_target` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 36 | `nesnd_small_army_target` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 37 | `nesnd_small_job_coverage` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 38 | `nesnd_small_transport` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 39 | `nesnd_small_production` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 40 | `nesnd_small_clean_production` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 41 | `nesnd_small_administration` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 42 | `nesnd_small_barracks` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 43 | `nesnd_small_industry_classes` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 44 | `nesnd_small_region_one_production` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 45 | `nesnd_small_region_two_production` | Retained — editorial pass | Task44 region identity / population coverage contract retained verbatim. |
| 46 | `nesnd_small_group_one_transport` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 47 | `nesnd_small_group_two_transport` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 48 | `nesnd_small_weekly_quote` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 49 | `nesnd_small_army_ratio` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 50 | `nesnd_small_gdp_ratio` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 51 | `nesnd_small_pressure_coverage` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 52 | `nesnd_small_generic_anchor_min` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 53 | `nesnd_small_native_one_pop` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 54 | `nesnd_small_native_two_pop` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 55 | `nesnd_small_native_one_share` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 56 | `nesnd_small_native_two_share` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 57 | `nesnd_small_states.2.far_south` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 58 | `nesnd_small_states.2.burma` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 59 | `nesnd_small_states.2.siam` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 60 | `nesnd_small_states.6.far_south` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 61 | `nesnd_small_states.6.burma` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 62 | `nesnd_small_states.6.siam` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 63 | `nesnd_small_livelihood_journal` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 64 | `nesnd_small_livelihood_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 65 | `nesnd_small_subject_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 66 | `nesnd_small_independent_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 67 | `nesnd_small_targets_lost` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 68 | `nesnd_small_economy_journal` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 69 | `nesnd_small_economy_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 70 | `nesnd_small_economy_months_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 71 | `nesnd_small_governance_journal` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 72 | `nesnd_small_governance_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 73 | `nesnd_small_governance_months_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 74 | `nesnd_small_regional_economy_journal` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 75 | `nesnd_small_regional_economy_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 76 | `nesnd_small_regional_economy_months_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 77 | `nesnd_small_regional_governance_journal` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 78 | `nesnd_small_regional_governance_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 79 | `nesnd_small_regional_governance_months_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 80 | `nesnd_small_order_journal` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 81 | `nesnd_small_order_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 82 | `nesnd_small_order_months_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 83 | `nesnd_small_working_status` | Rewritten — editorial pass | Describe present political or progress state directly. |
| 84 | `nesnd_small_paused_status` | Rewritten — editorial pass | Describe present political or progress state directly. |
| 85 | `nesnd_small_dispute_journal` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 86 | `nesnd_small_dispute_journal_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 87 | `nesnd_small_dispute_status` | Rewritten — editorial pass | Describe present political or progress state directly. |
| 88 | `nesnd_small_observation_months` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 89 | `nesnd_small_bar_desc` | Retained — editorial pass | Existing English conveys the current Chinese meaning; no stale narrative omitted. |
| 90 | `nesnd_small_qualified_month` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 91 | `nesnd_small_public` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 92 | `nesnd_small_public_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 93 | `nesnd_small_public_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 94 | `nesnd_small_specialise_button` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 95 | `nesnd_small_specialise_button_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 96 | `nesnd_small_specialise_button_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 97 | `nesnd_small_own_market_button` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 98 | `nesnd_small_own_market_button_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 99 | `nesnd_small_own_market_button_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 100 | `nesnd_small_retarget_button` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 101 | `nesnd_small_retarget_button_desc` | Retained — editorial pass | Existing English conveys the current Chinese meaning; no stale narrative omitted. |
| 102 | `nesnd_small_retarget_button_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 103 | `nesnd_small_restore_geography_button` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 104 | `nesnd_small_restore_geography_button_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 105 | `nesnd_small_restore_geography_button_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 106 | `nesnd_small_order_button` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 107 | `nesnd_small_order_button_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 108 | `nesnd_small_order_button_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 109 | `nesnd_small_request_autonomy` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 110 | `nesnd_small_request_autonomy_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 111 | `nesnd_small_request_autonomy_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 112 | `nesnd_small_request_independence` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 113 | `nesnd_small_request_independence_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 114 | `nesnd_small_request_independence_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 115 | `nesnd_small_request_market` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 116 | `nesnd_small_request_market_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 117 | `nesnd_small_request_market_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 118 | `nesnd_small_defence_fra` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 119 | `nesnd_small_defence_fra_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 120 | `nesnd_small_defence_fra_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 121 | `nesnd_small_defence_gbr` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 122 | `nesnd_small_defence_gbr_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 123 | `nesnd_small_defence_gbr_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 124 | `nesnd_small_defence_usm` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 125 | `nesnd_small_defence_usm_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 126 | `nesnd_small_defence_usm_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 127 | `nesnd_small_defence_mug` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 128 | `nesnd_small_defence_mug_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 129 | `nesnd_small_defence_mug_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 130 | `nesnd_small_defence_phi` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 131 | `nesnd_small_defence_phi_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 132 | `nesnd_small_defence_phi_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 133 | `nesnd_small_defence_dei` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 134 | `nesnd_small_defence_dei_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 135 | `nesnd_small_defence_dei_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 136 | `nesnd_small_defence_yn1` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 137 | `nesnd_small_defence_yn1_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 138 | `nesnd_small_defence_yn1_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 139 | `nesnd_small_defence_bur` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 140 | `nesnd_small_defence_bur_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 141 | `nesnd_small_defence_bur_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 142 | `nesnd_small_defence_sia` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 143 | `nesnd_small_defence_sia_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 144 | `nesnd_small_defence_sia_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 145 | `nesnd_small_defence_dai` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 146 | `nesnd_small_defence_dai_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 147 | `nesnd_small_defence_dai_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 148 | `nesnd_small_defence_neighbour` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 149 | `nesnd_small_defence_neighbour_desc` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 150 | `nesnd_small_defence_neighbour_tt` | Rewritten — editorial pass | Describe the defence proposal and reciprocal commitment instead of repeating eligibility or verification machinery. |
| 151 | `nesnd_small_request_defence_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 152 | `nesnd_small_states.continue` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 153 | `nesnd_small_states.2.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 154 | `nesnd_small_states.2.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 155 | `nesnd_small_states.3.t` | Rewritten — editorial pass | Title now conveys the actual scene or outcome. |
| 156 | `nesnd_small_states.3.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 157 | `nesnd_small_states.4.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 158 | `nesnd_small_states.4.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 159 | `nesnd_small_states.5.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 160 | `nesnd_small_states.5.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 161 | `nesnd_small_states.6.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 162 | `nesnd_small_states.6.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 163 | `nesnd_small_states.11.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 164 | `nesnd_small_states.11.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 165 | `nesnd_small_states.12.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 166 | `nesnd_small_states.12.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 167 | `nesnd_small_states.10.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 168 | `nesnd_small_states.10.land` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 169 | `nesnd_small_states.10.labor` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 170 | `nesnd_small_states.10.representation` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 171 | `nesnd_small_states.10.organise` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 172 | `nesnd_small_states.10.organise_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 173 | `nesnd_small_states.10.promise_land` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 174 | `nesnd_small_states.10.promise_land_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 175 | `nesnd_small_states.10.promise_debt` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 176 | `nesnd_small_states.10.promise_debt_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 177 | `nesnd_small_states.10.promise_labor` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 178 | `nesnd_small_states.10.promise_labor_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 179 | `nesnd_small_states.10.promise_caste` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 180 | `nesnd_small_states.10.promise_caste_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 181 | `nesnd_small_states.10.promise_representation` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 182 | `nesnd_small_states.10.promise_representation_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 183 | `nesnd_small_states.10.suppress` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 184 | `nesnd_small_states.10.suppress_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 185 | `nesnd_small_states.20.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 186 | `nesnd_small_states.20.autonomy` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 187 | `nesnd_small_states.20.independence` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 188 | `nesnd_small_states.20.market` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 189 | `nesnd_small_states.20.defence` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 190 | `nesnd_small_accept_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 191 | `nesnd_small_refuse_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 192 | `nesnd_small_states.21.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 193 | `nesnd_small_states.21.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 194 | `nesnd_small_states.21.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 195 | `nesnd_small_states.21.b` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 196 | `nesnd_small_livelihood` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 197 | `nesnd_small_learning` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 198 | `nesnd_small_order` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 199 | `nesnd_small_public_investment` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 200 | `nesnd_small_public_services` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 201 | `nesnd_small_specialised_market` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 202 | `nesnd_small_own_market` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 203 | `nesnd_small_local_spokesperson` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 204 | `nesnd_small_reform_approval` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 205 | `nesnd_small_organise_land` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 206 | `nesnd_small_organise_labor` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 207 | `nesnd_small_organise_representation` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 208 | `nesnd_small_suppress_land` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 209 | `nesnd_small_suppress_labor` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 210 | `nesnd_small_suppress_representation` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 211 | `nesnd_final_small_own_public_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 212 | `nesnd_final_small_public_existing_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 213 | `nesnd_small_economy_bar_readout` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 214 | `nesnd_small_governance_bar_readout` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 215 | `nesnd_small_regional_economy_bar_readout` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 216 | `nesnd_small_regional_governance_bar_readout` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 217 | `nesnd_small_order_bar_readout` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
### nesnd_native_americas
| Line | Key | Disposition | Reason |
|---:|---|---|---|
| 2 | `nesnd_hus_registration.1.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 3 | `nesnd_hus_registration.1.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 4 | `nesnd_hus_registration.1.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 5 | `nesnd_hus_registration.2.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 6 | `nesnd_hus_registration.2.d` | Retained — editorial pass | Existing English conveys the current Chinese meaning; no stale narrative omitted. |
| 7 | `nesnd_hus_registration.2.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 8 | `war_goal_wg_nesnd_usm_annex_type_name` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 9 | `war_goal_wg_nesnd_usm_annex_type_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 10 | `war_goal_wg_nesnd_usm_annex` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 11 | `war_goal_wg_nesnd_usm_annex_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 12 | `war_goal_wg_nesnd_usm_annex_sway_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 13 | `nesnd_american_restoration` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 14 | `nesnd_american_restoration_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 15 | `nesnd_native_recognize` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 16 | `nesnd_native_recognize_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 17 | `nesnd_native_recognize_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 18 | `nesnd_native_negotiate` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 19 | `nesnd_native_negotiate_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 20 | `nesnd_native_negotiate_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 21 | `nesnd_native_suppress` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 22 | `nesnd_native_suppress_desc` | Retained — editorial pass | Existing English conveys the current Chinese meaning; no stale narrative omitted. |
| 23 | `nesnd_native_suppress_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 24 | `nesnd_native_local_councils` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 25 | `nesnd_native_restored_rule` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 26 | `nesnd_native_exiles` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 27 | `nesnd_restoration_pressure_bar` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 28 | `nesnd_restoration_pressure_bar_desc` | Retained — editorial pass | Existing English conveys the current Chinese meaning; no stale narrative omitted. |
| 29 | `nesnd_restoration_pressure_base` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 30 | `nesnd_restoration_pressure_radicals` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 31 | `nesnd_restoration_pressure_poverty` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 32 | `nesnd_restoration_pressure_repression` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 33 | `nesnd_restoration_existing_court_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 34 | `nesnd_restoration_waiting_land_status` | Rewritten — editorial pass | Describe present political or progress state directly. |
| 35 | `nesnd_restoration_politics_status` | Rewritten — editorial pass | Describe present political or progress state directly. |
| 36 | `nesnd_native_restoration_war` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 37 | `nesnd_native_restoration_war_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 38 | `nesnd_restoration_war_status` | Rewritten — editorial pass | Describe present political or progress state directly. |
| 39 | `nesnd_restoration_war_against` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 40 | `nesnd_restoration_war_mustering` | Rewritten — editorial pass | Align established display wording with current Chinese and actual field purpose. |
| 41 | `nesnd_restoration_war` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 42 | `dp_nesnd_native_restoration` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 43 | `dp_nesnd_native_restoration_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 44 | `dp_nesnd_native_restoration_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 45 | `wg_nesnd_restoration_settlement` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 46 | `wg_nesnd_restoration_settlement_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 47 | `nesnd_american_restoration.1.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 48 | `nesnd_american_restoration.1.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 49 | `nesnd_american_restoration.1.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 50 | `nesnd_american_restoration.2.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 51 | `nesnd_american_restoration.2.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 52 | `nesnd_american_restoration.2.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 53 | `nesnd_american_restoration.3.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 54 | `nesnd_american_restoration.3.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 55 | `nesnd_american_restoration.3.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 56 | `nesnd_american_restoration.4.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 57 | `nesnd_american_restoration.4.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 58 | `nesnd_american_restoration.4.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 59 | `nesnd_american_restoration.5.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 60 | `nesnd_american_restoration.5.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 61 | `nesnd_american_restoration.5.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 62 | `nesnd_american_restoration.6.t` | Rewritten — editorial pass | State interruption/non-annexation without inventing victory, peace agreement or completed intervention war. |
| 63 | `nesnd_american_restoration.6.d` | Rewritten — editorial pass | State interruption/non-annexation without inventing victory, peace agreement or completed intervention war. |
| 64 | `nesnd_american_restoration.6.a` | Rewritten — editorial pass | State interruption/non-annexation without inventing victory, peace agreement or completed intervention war. |
| 65 | `nesnd_american_restoration.10.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 66 | `nesnd_american_restoration.10.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 67 | `nesnd_american_restoration.10.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 68 | `nesnd_american_restoration.10.b` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 69 | `nesnd_a2_itzcoatl_first` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 70 | `nesnd_a2_moctezuma_last` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 71 | `nesnd_a2_amaru_first` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 72 | `nesnd_a2_amaru_last` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 73 | `nesnd_a2_rumi_first` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 74 | `nesnd_a2_quispe_last` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 75 | `nesnd_a2_tatanka_first` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 76 | `nesnd_a2_temur_last` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 77 | `nesnd_khanate_emergence` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 78 | `nesnd_khanate_emergence_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 79 | `nesnd_khanate_waiting_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 80 | `nesnd_khanate_established_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 81 | `nesnd_khanate_survival` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 82 | `nesnd_khanate_survival_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 83 | `nesnd_khanate_usa_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 84 | `nesnd_khanate_hus_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 85 | `nesnd_khanate_survival_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 86 | `nesnd_khanate_legacy_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 87 | `nesnd_khanate_survived_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 88 | `nesnd_suppress_native_khanate` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 89 | `nesnd_suppress_native_khanate_reason` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 90 | `nesnd_khanate_intervention_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 91 | `nesnd_khanate_destroyed_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 92 | `nesnd_khanate_suppression_failed_tt` | Rewritten — editorial pass | State interruption/non-annexation without inventing victory, peace agreement or completed intervention war. |
| 93 | `nesnd_khanate_war` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 94 | `dp_nesnd_khanate_suppression` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 95 | `dp_nesnd_khanate_suppression_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 96 | `dp_nesnd_khanate_suppression_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 97 | `NKH` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 98 | `NKH_ADJ` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 99 | `wg_nesnd_khanate_annex` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 100 | `wg_nesnd_khanate_annex_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 101 | `wg_nesnd_khanate_humiliation` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 102 | `wg_nesnd_khanate_humiliation_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 103 | `nesnd_khanate_army` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 104 | `nesnd_native_american_republic` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 105 | `nesnd_native_american_republic_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 106 | `nesnd_native_khanate.2.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 107 | `nesnd_native_khanate.2.d` | Rewritten — editorial pass | Preserve distinct intervention outcome and restore peacetime interests of khan and communities. |
| 108 | `nesnd_native_khanate.2.a` | Rewritten — editorial pass | Restore the choice as a concrete political stance or action. |
| 109 | `nesnd_native_khanate.3.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 110 | `nesnd_native_khanate.3.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 111 | `nesnd_native_khanate.3.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 112 | `nesnd_a2_exodus_both_desc` | Rewritten — editorial pass | Restore registration grievance, family migration and branch-specific consequences; remove implementation commentary. |
| 113 | `nesnd_a2_exodus_cne_desc` | Rewritten — editorial pass | Restore registration grievance, family migration and branch-specific consequences; remove implementation commentary. |
| 114 | `nesnd_a2_exodus_usa_desc` | Rewritten — editorial pass | Restore registration grievance, family migration and branch-specific consequences; remove implementation commentary. |
| 115 | `nesnd_a2_exodus_none_desc` | Rewritten — editorial pass | Restore registration grievance, family migration and branch-specific consequences; remove implementation commentary. |
| 116 | `nesnd_american_restoration.11.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 117 | `nesnd_american_restoration.11.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 118 | `nesnd_american_restoration.11.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 119 | `nesnd_american_restoration.12.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 120 | `nesnd_american_restoration.12.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 121 | `nesnd_american_restoration.12.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 122 | `nesnd_restore_native_hus` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 123 | `nesnd_restore_native_hus_desc` | Rewritten — editorial pass | Describe current action and its purpose in idiomatic English. |
| 124 | `nesnd_native_americas_unified_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 125 | `nesnd_native_hus_restored_tt` | Rewritten — editorial pass | Natural actionable English; retain all numerical terms and actual effects, remove engine-verification wording. |
| 126 | `nesnd_american_restoration.13.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 127 | `nesnd_american_restoration.13.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 128 | `nesnd_american_restoration.13.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 129 | `nesnd_native_khanate.2.both` | Rewritten — editorial pass | Preserve distinct intervention outcome and restore peacetime interests of khan and communities. |
| 130 | `nesnd_native_khanate.2.one` | Rewritten — editorial pass | Preserve distinct intervention outcome and restore peacetime interests of khan and communities. |
| 131 | `nesnd_native_khanate.2.none` | Rewritten — editorial pass | Preserve distinct intervention outcome and restore peacetime interests of khan and communities. |
| 132 | `war_goal_wg_nesnd_restoration_settlement_type_name` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 133 | `war_goal_wg_nesnd_restoration_settlement_type_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 134 | `war_goal_wg_nesnd_restoration_settlement` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 135 | `war_goal_wg_nesnd_restoration_settlement_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 136 | `war_goal_wg_nesnd_restoration_settlement_sway_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 137 | `war_goal_wg_nesnd_khanate_annex_type_name` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 138 | `war_goal_wg_nesnd_khanate_annex_type_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 139 | `war_goal_wg_nesnd_khanate_annex` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 140 | `war_goal_wg_nesnd_khanate_annex_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 141 | `war_goal_wg_nesnd_khanate_annex_sway_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 142 | `war_goal_wg_nesnd_khanate_humiliation_type_name` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 143 | `war_goal_wg_nesnd_khanate_humiliation_type_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 144 | `war_goal_wg_nesnd_khanate_humiliation` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 145 | `war_goal_wg_nesnd_khanate_humiliation_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 146 | `war_goal_wg_nesnd_khanate_humiliation_sway_desc` | Retained — editorial pass | War-goal name/effect or native alias already matches current Chinese. |
| 147 | `nesnd_native_khanate.4.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 148 | `nesnd_native_khanate.4.d` | Rewritten — editorial pass | Restore treaty breakdown narrative; retain same-treaty trade losses and withdrawal cost, remove developer exclusion note. |
| 149 | `nesnd_native_khanate.4.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 150 | `nesnd_final_native_restored_existing_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 152 | `nesnd_ui_restoration_no_dispute_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 153 | `nesnd_ui_restoration_native_population_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 154 | `nesnd_ui_restoration_no_invitation_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 155 | `nesnd_ui_restoration_wait_over_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 156 | `nesnd_ui_khanate_campaign_ended_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 157 | `nesnd_ui_khanate_not_annexed_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 158 | `nesnd_native_repression` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 159 | `nesnd_restoration_repression_pressure_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 160 | `nesnd_restoration_mobilizing_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 161 | `nesnd_restoration_mobilization_remaining` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 162 | `nesnd_restoration_mobilization_paused_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 163 | `nesnd_restoration_mobilization_ready_status` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 164 | `nesnd_american_restoration.14.t` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 165 | `nesnd_american_restoration.14.d` | Rewritten — editorial pass | Restore actors, livelihoods, political interests and causal development omitted by old English summary. |
| 166 | `nesnd_american_restoration.14.a` | Retained — editorial pass | Established name, option, UI label or readout already matches current Chinese. |
| 167 | `notification_nesnd_restoration_repression_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 168 | `notification_nesnd_restoration_repression_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 169 | `notification_nesnd_restoration_repression_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 170 | `notification_nesnd_restoration_mobilization_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 171 | `notification_nesnd_restoration_mobilization_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 172 | `notification_nesnd_restoration_mobilization_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 173 | `notification_nesnd_restoration_country_created_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 174 | `notification_nesnd_restoration_country_created_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 175 | `notification_nesnd_restoration_country_created_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 176 | `notification_nesnd_restoration_war_started_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 177 | `notification_nesnd_restoration_war_started_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 178 | `notification_nesnd_restoration_war_started_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 179 | `notification_nesnd_restoration_dispatch_failed_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 180 | `notification_nesnd_restoration_dispatch_failed_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 181 | `notification_nesnd_restoration_dispatch_failed_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 182 | `notification_nesnd_restoration_opponent_lost_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 183 | `notification_nesnd_restoration_opponent_lost_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 184 | `notification_nesnd_restoration_opponent_lost_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 185 | `notification_nesnd_restoration_dispute_ended_notice_name` | Rewritten — editorial pass | State interruption/non-annexation without inventing victory, peace agreement or completed intervention war. |
| 186 | `notification_nesnd_restoration_dispute_ended_notice_desc` | Rewritten — editorial pass | State interruption/non-annexation without inventing victory, peace agreement or completed intervention war. |
| 187 | `notification_nesnd_restoration_dispute_ended_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 188 | `notification_nesnd_restoration_settlement_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 189 | `notification_nesnd_restoration_settlement_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 190 | `notification_nesnd_restoration_settlement_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 191 | `notification_nesnd_restoration_reopened_notice_name` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 192 | `notification_nesnd_restoration_reopened_notice_desc` | Retained — editorial pass | Notification already describes the actual current branch without added claims. |
| 193 | `notification_nesnd_restoration_reopened_notice_tooltip` | Retained — editorial pass | Existing alias/format contract remains accurate. |
| 194 | `nesnd_restoration_war_victory_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 195 | `nesnd_restoration_war_terminal_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |
| 196 | `nesnd_restoration_war_not_victorious_tt` | Retained — editorial pass | Condition, cost, duration or branch already matches Chinese and actual script. |

## Source and output fingerprints
| Source | SHA-256 |
|---|---|
| `MOD/localization/simp_chinese/replace/nesnd_small_states_l_simp_chinese.yml` | `f6447d46d1b92b3835afb39632ad6c1e528b7b285578fe554c326dd5846ddefb` |
| `MOD/localization/simp_chinese/replace/nesnd_native_americas_l_simp_chinese.yml` | `5ea527456d54a8bbae81275fa2e216fb89db218cad550a62757af4e4b4dc3f89` |
| `MOD/localization/english/replace/nesnd_small_states_l_english.yml` | `21097fbc25530921cce098fa24c0c2206d1f9685a552bfc201c6b49f11a62ffe` |
| `MOD/localization/english/replace/nesnd_native_americas_l_english.yml` | `f11b41803d28ecac39eb883bd20c4b06655c6a01299cb0f4a9b2f192f9b0bb0a` |
| `MOD/events/nesnd_small_states.txt` | `abaf3eead7dd7deab0412f44cc2805d4604c9d892c5b23a8d4830eae743c1197` |
| `MOD/events/nesnd_american_restoration.txt` | `8316975e43a599b222440b5acc1bb356dc006f5c8c6183e55a8b14cc79f589e3` |
| `MOD/events/nesnd_native_khanate.txt` | `d80833c8eae19cc719bc2f42c98ac3b128239e9b1ad58c52a705ad1fac625426` |
| `MOD/events/nesnd_hus_registration.txt` | `00fff46e9205b4883f38a2635888c6a3811d132c61645aa78f98b3c57e2c7d7d` |
| `MOD/common/journal_entries/nesnd_small_states.txt` | `d6daadd9ab6d495e123fc90830321febe5a25bf4e082139d1b1efaac1a188f67` |
| `MOD/common/customizable_localization/nesnd_small_regions.txt` | `3ec7977aa36c727ac91b915e2d0610e8140f22baea697b2b2ab18c15860c4600` |
| `MOD/common/scripted_buttons/nesnd_american_restoration.txt` | `da157c43331edb2e9316d6e474847a37d2665391de3ae9e7c5b767374ec92211` |
| `MOD/common/scripted_effects/nesnd_american_restoration.txt` | `bfc923d0d0285fb1956b43da3bf0e61c6e81c49734a46928849cc64124927a95` |
| `MOD/common/scripted_effects/nesnd_native_khanate.txt` | `5a0630407f7ca908cf7e3482e8bcd24cab70c330bb4e13a6a8cd044ce620b440` |
| `MOD/common/scripted_effects/nesnd_a2_manchu_exodus.txt` | `a3a8b0c592529a1b60690a7c72b90bb517839e43f727a6592f95648047a8be52` |
| `MOD/common/scripted_effects/nesnd_small_states.txt` | `39a1bffc3dc28fa32e853b182b17c4d2d3ab2e20574372d421a4f1fb14b48e35` |
| `GAME/common/journal_entries/00_canada_australia.txt` | `d0e4ec54a9cf60afb25f1d5e711719a90c47ae146a03b2d97f8829e13fd9bc11` |
| `GAME/common/scripted_buttons/06_canada_australia_buttons.txt` | `40811d1d0f60a96d8bbbef78b993f90ca55ff0ef4d16f4cd51c176758859dc00` |
| `GAME/common/customizable_localization/victoria_ip4_custom_loc.txt` | `851cdf8f67c089cf91465e852df3d0336331e94d955073ae41fac40e0bbbeb4f` |
| `GAME/events/canada_australia_events.txt` | `5fe9b423a546f5d3c50bbcb005f858dbd2528e0719151ebb77c931d1d983092b` |
| `GAME/common/static_modifiers/content_1_modifiers.txt` | `398dcee1be15a500e1c53822810ac10fa287777f14c9a25b110b1d5878b6c387` |
| `GAME/localization/english/content_1_l_english.yml` | `144c05d3a56ba1b7d1ec9b6393b9cedd5074421fd55dc6d950e359df67b2760a` |
| `GAME/localization/english/ip4_misc_01_l_english.yml` | `a833429fe921eb576e98566188e79367a31ac9884410cc8fc206b15a3f833725` |
| `GAME/localization/english/laws_l_english.yml` | `0b75cb8a71c98276758866bf1a8706e8e195b21860bdea3ebb2a56d7ea568d43` |
| Pre-change English `nesnd_small_states` (backup confirmed) | `78e4cbf0fe52fd80ccab1c82175b189d240c4a063d88e3bb7d3add4231de5fdb` |
| Pre-change English `nesnd_native_americas` (backup confirmed) | `f8cc861e2ff991376cc168bcc5042d75390281ebcef359fe63d898cc8701b05e` |
| `f18b6c4:localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml` | `3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a` |
| `f18b6c4:localization/simp_chinese/replace/ce_poland_l_simp_chinese.yml` | `20731ac53ebbe66c85d65ac5a9eb1e52a00f69feb6bcf13b490f13f5bcc17f6d` |

Native chain completion: event caller/recipient scopes and annexation read in GAME/events/canada_australia_events.txt:4-75; timed modifier definition/icon read in GAME/common/static_modifiers/content_1_modifiers.txt:213-216. The existing event video and icon paths were inspected as references; no resources were copied or changed.
