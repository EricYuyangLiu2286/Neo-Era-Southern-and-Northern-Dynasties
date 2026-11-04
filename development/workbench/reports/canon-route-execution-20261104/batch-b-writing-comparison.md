# Batch B writing comparison

Implementation editorial record; no engine/UI test. Immutable author sample root: WORK/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace.

Samples: ce_french_empire_journals_l_simp_chinese.yml:236–237 (action title and political stance), :247–248 (indicator title and current/max readout), SHA352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844; ce_cne_events_l_simp_chinese.yml:15 (historical actors/interests) and :69 (social consequences), SHA3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a.

## Editorial decisions

- The author’s “保卫王朝” uses a concrete political action, with its reason in desc. Policy buttons retain the user’s action names; costs, durations and discrete monthly effects are separated into native previews and concise tooltips.
- Qin’s original land-reform writing names the social groups whose interests change. Material subsidy names marginalized recipients and established groups bearing resentment; it does not claim a scripted SoL increase, new buildings or votes.
- The exact sensitivity interface is unavailable. Player text states that 0.1% of each primary culture’s population moves toward radicalism monthly, at most12 applications. It never calls this sensitivity. The plan’s +6/year estimate is conditional on12 pulses; final player text promises only the monthly rate and real12-month term.
- Law rows use actual lawgroup names in both languages. The old mixed “laws”/unrest wording is removed from active rows without changing the existing legal coefficients.
- TUR reason concerns expansion and relations among the empire’s peoples. It does not narrate tests, callback ordering, patch history or a forced future breakup. Status is current and conditional.
- Military supply source correction: Paraguay’s building-scoped fragment is show_as_tooltip; the actual event applies its modifier to the country. The effect accepts building scope and the unit modifier’s quantity semantics are documented, but runtime propagation from a TUR barracks to its units remains unverified. Player text states the intended scripted reward; delivery must retain ENGINE_NOT_RUN.

## Per-key candidate and final editorial result

All entries below are the final hand-authored candidates after these decisions. PASS means editorial contract pass, not engine validation. Claim names use the existing state-region localization token rather than inventing/retranslating geography. Native modifier previews supply their actual numeric effects.

| Key | Chinese final | English final | Source/category; decision |
|---|---|---|---|
| nesnd_unity_material_subsidy | 补贴落后人群 | Subsidize Disadvantaged Communities | author action/indicator samples; PASS |
| nesnd_unity_material_subsidy_desc | 向贫困、受歧视的群体提供补贴，使他们更愿意参与共同的社会生活。享有旧有地位的人群却会把这笔支出看作对自身利益的侵蚀。 | Provide assistance to poor and marginalized communities, encouraging their participation in a shared social life. Those who enjoy established privileges may resent the expense. | author action/indicator samples; PASS |
| nesnd_unity_political_subsidy | 补贴政治存在 | Support Political Representation | author action/indicator samples; PASS |
| nesnd_unity_political_subsidy_desc | 让长期处于政治边缘的人群在国家事务中获得更多关注。旧有的统治基础因此受到冲击，共同的国家认同也有了生长的余地。 | Give politically marginalized communities greater attention in national affairs. This unsettles the government’s established base of support while creating room for a shared national identity. | author action/indicator samples; PASS |
| nesnd_unity_material_available_tt | 此前的落后人群补贴已经到期 | The previous community subsidy has expired | effect contract; exact cost/target/term; PASS |
| nesnd_unity_political_available_tt | 此前的政治存在补贴已经到期 | The previous political representation subsidy has expired | effect contract; exact cost/target/term; PASS |
| nesnd_unity_material_monthly_tt | 每月团结度或共同认同#g +0.50#!；各主流文化中#r 0.1%#!的人口趋于激进，最多发生十二次。 | Each month, Cohesion or Common Identity gains #g 0.50#!. Move #r 0.1%#! of the population in each primary culture toward radicalism, for up to twelve monthly applications. | effect contract; exact cost/target/term; PASS |
| nesnd_unity_political_monthly_tt | 每月团结度或共同认同#g +0.50#!。 | Cohesion or Common Identity gains #g 0.50#! each month. | effect contract; exact cost/target/term; PASS |
| nesnd_unity_fixed_term_tt | 持续十二个月，期间不能撤销或再次启动同一措施。 | Lasts twelve months. This measure cannot be cancelled or renewed during that period. | effect contract; exact cost/target/term; PASS |
| nesnd_unity_material_expense | 落后人群补贴开支 | Community Subsidy Expenditure | author action/indicator samples; PASS |
| nesnd_unity_material_assistance | 落后人群补贴 | Community Assistance | author action/indicator samples; PASS |
| nesnd_unity_political_assistance | 政治存在补贴 | Political Representation Support | author action/indicator samples; PASS |
| nesnd_unity_material_growth_desc | 补贴落后人群 | Community Subsidies | author action/indicator samples; PASS |
| nesnd_unity_political_growth_desc | 补贴政治存在 | Political Representation Support | author action/indicator samples; PASS |
| nesnd_unity_lawgroup_citizenship | $lawgroup_citizenship$ | $lawgroup_citizenship$ | native lawgroup name + user correction; PASS |
| nesnd_unity_lawgroup_church_state | $lawgroup_church_and_state$ | $lawgroup_church_and_state$ | native lawgroup name + user correction; PASS |
| nesnd_unity_lawgroup_army_model | $lawgroup_army_model$ | $lawgroup_army_model$ | native lawgroup name + user correction; PASS |
| nesnd_unity_lawgroup_distribution_of_power | $lawgroup_distribution_of_power$ | $lawgroup_distribution_of_power$ | native lawgroup name + user correction; PASS |
| nesnd_india_community_unrest | 社会动荡 | Social Turmoil | author action/indicator samples; PASS |
| nesnd_ottoman_unity | 帝国诸民 | Peoples of the Empire | author action/indicator samples; PASS |
| nesnd_ottoman_unity_reason | 征服使苏丹能够支配更广阔的土地，也把信仰、语言和历史各异的人们置于同一朝廷之下。安纳托利亚的官员、巴尔干的地方势力和新近归附的各族，都要求国家保护他们的利益。\n\n学校、行政和安定的生活可以培育共同的归属，长期征战和排斥性的制度则会使地方社会离心。帝国必须在扩张之外，为这些臣民提供愿意留在一起的理由。 | Conquest places more land under the Sultan’s authority, bringing peoples of different faiths, languages and histories before the same court. Officials in Anatolia, provincial interests in the Balkans and newly incorporated communities all expect the state to protect their interests.\n\nSchools, effective administration and a secure livelihood can strengthen a sense of belonging. Prolonged war and exclusionary institutions pull provincial society apart. The empire must give its subjects reasons to remain together. | CNE historical/process sample; PASS |
| nesnd_ottoman_unity_bar | 国家团结度 | National Cohesion | author action/indicator samples; PASS |
| nesnd_ottoman_unity_bar_desc | #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100 | #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100 | author action/indicator samples; PASS |
| nesnd_ottoman_unity_fractured | 各地对朝廷的信任已经动摇，地方动荡正在加重统治的负担。 | Confidence in the court is faltering, and provincial turmoil is placing a heavier burden on government. | author action/indicator samples; PASS |
| nesnd_ottoman_unity_confident | 各地的共同归属正在巩固，不同群体更愿意融入帝国的社会生活。 | A shared sense of belonging is strengthening, encouraging communities to participate in the empire’s social life. | author action/indicator samples; PASS |
| nesnd_ottoman_unity_calm | 朝廷与地方仍在维持合作，各族对帝国的认同有待巩固。 | The court and the provinces continue to cooperate, though their shared allegiance still needs strengthening. | author action/indicator samples; PASS |
| nesnd_ottoman_unity_order_desc | 行政延续 | Administrative Continuity | author action/indicator samples; PASS |
| nesnd_ottoman_unity_arab_desc | 阿拉伯与北非诸族人口 | Arab and North African Communities | author action/indicator samples; PASS |
| nesnd_ottoman_unity_han_desc | 汉文化传承人口 | Communities of Han Heritage | author action/indicator samples; PASS |
| nesnd_ottoman_unity_african_desc | 其他非洲文化传承人口 | Other Communities of African Heritage | author action/indicator samples; PASS |
| nesnd_ottoman_unity_slavic_desc | 斯拉夫诸族人口 | Slavic Communities | author action/indicator samples; PASS |
| nesnd_ottoman_unity_other_desc | 其他非土耳其族人口 | Other Non-Turkish Communities | author action/indicator samples; PASS |
| nesnd_ottoman_unity_legitimacy_desc | 政府合法性 | Government Legitimacy | author action/indicator samples; PASS |
| nesnd_ottoman_unity_bureaucracy_desc | 行政能力 | Bureaucratic Capacity | author action/indicator samples; PASS |
| nesnd_ottoman_unity_schools_desc | 教育机构 | Education Institutions | author action/indicator samples; PASS |
| nesnd_ottoman_unity_livelihood_desc | 生活水平变化 | Changes in Living Standards | author action/indicator samples; PASS |
| nesnd_ottoman_unity_bankruptcy_desc | 破产后的惩罚 | Bankruptcy Penalties | author action/indicator samples; PASS |
| nesnd_ottoman_unity_war_desc | 战争持续 | Prolonged Warfare | author action/indicator samples; PASS |
| nesnd_ottoman_unity_victory_desc | 军事胜利 | Military Victory | author action/indicator samples; PASS |
| nesnd_ottoman_unity_expansion_desc | 领土扩张 | Territorial Expansion | author action/indicator samples; PASS |
| nesnd_ottoman_divided_provinces | 离心的行省 | Disaffected Provinces | author action/indicator samples; PASS |
| nesnd_ottoman_common_allegiance | 共同的归属 | Common Allegiance | author action/indicator samples; PASS |
| nesnd_ottoman_recovery | 重整东方秩序 | Restoring the Eastern Order | author action/indicator samples; PASS |
| nesnd_ottoman_recovery_reason | 坦志麦特的成果关系到奥斯曼国家的生存，也关系到苏丹能否重新向东方伸张权力。军官希望改进训练与补给，朝廷则要把军队的力量变成对亚洲土地的实际要求。秦国及其周边诸国的秩序，正是这场竞争所要改变的对象。\n\n改革带来的力量仍须由军备和政治支持维持。每一项新的领土要求，都需要消耗国内积聚起来的扩张热情。 | The outcome of the Tanzimat concerns both the survival of the Ottoman state and the Sultan’s ability to project power eastward. Officers seek better training and supply, while the court seeks to turn military strength into territorial demands in Asia. The order established by Qin and its neighboring states is at stake.\n\nThe strength gained through reform must be sustained by armaments and political support. Each new territorial demand draws upon the enthusiasm for expansion accumulated at home. | CNE historical/process sample; PASS |
| nesnd_ottoman_recovery_success_status | 坦志麦特已经成功。改革后的军队与朝廷可以更有力地推动东方扩张。 | The Tanzimat has succeeded. The reformed army and court can pursue eastern expansion with greater strength. | author action/indicator samples; PASS |
| nesnd_ottoman_recovery_failed_status | 坦志麦特已经失败。朝廷仍可推动扩张，但军改与动员的成效较弱。 | The Tanzimat has failed. The court can still pursue expansion, though military reform and mobilization yield weaker results. | author action/indicator samples; PASS |
| nesnd_ottoman_recovery_ongoing_status | 坦志麦特仍在进行，东方的竞争已经开始。 | The Tanzimat is still underway, while competition in the east has already begun. | author action/indicator samples; PASS |
| nesnd_ottoman_enthusiasm_bar | 扩张热情 | Enthusiasm for Expansion | author action/indicator samples; PASS |
| nesnd_ottoman_enthusiasm_bar_desc | #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100 | #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|1]#!/100 | author action/indicator samples; PASS |
| nesnd_ottoman_enthusiasm_base | 坦志麦特的进程与成果 | The Progress and Outcome of the Tanzimat | author action/indicator samples; PASS |
| nesnd_ottoman_enthusiasm_army | 陆军规模 | Army Strength | author action/indicator samples; PASS |
| nesnd_ottoman_enthusiasm_government | 军队执政支持 | Armed Forces in Government | author action/indicator samples; PASS |
| nesnd_ottoman_enthusiasm_reform | 军改投入 | Military Reform Effort | author action/indicator samples; PASS |
| nesnd_ottoman_reform_army | 推行秦式军改 | Adopt Qin Military Methods | author action/indicator samples; PASS |
| nesnd_ottoman_reform_army_desc | 吸收秦国组织军队和供给部队的经验，使军官在国家事务中承担更大责任。改革期间，朝廷需要收束扩张的呼声，把精力用于军队本身。 | Draw on Qin’s experience in organizing and supplying armies, giving officers a larger role in national affairs. During the reform, the court must devote some of its expansionist energy to the army itself. | author action/indicator samples; PASS |
| nesnd_ottoman_reform_not_active | 上一轮军改已经结束 | The previous military reform has ended | author action/indicator samples; PASS |
| nesnd_ottoman_qin_supply_tt | 十二个月内，军营与征兵中心所属单位的补给品消耗#g −20%#!。 | For twelve months, units raised by barracks and conscription centers consume #g 20%#! fewer supply goods. | effect contract; exact cost/target/term; PASS |
| nesnd_ottoman_qin_supply_success_tt | 十二个月内，军营与征兵中心所属单位的补给品消耗#g −25%#!。 | For twelve months, units raised by barracks and conscription centers consume #g 25%#! fewer supply goods. | effect contract; exact cost/target/term; PASS |
| nesnd_ottoman_qin_supply_failed_tt | 十二个月内，军营与征兵中心所属单位的补给品消耗#g −15%#!。 | For twelve months, units raised by barracks and conscription centers consume #g 15%#! fewer supply goods. | effect contract; exact cost/target/term; PASS |
| nesnd_ottoman_qin_reform | 秦式军改 | Qin Military Reform | author action/indicator samples; PASS |
| nesnd_ottoman_qin_reform_success | 改革后的秦式军制 | Qin Military Methods after the Tanzimat | author action/indicator samples; PASS |
| nesnd_ottoman_qin_reform_failed | 困境中的秦式军改 | Qin Military Reform amid Decline | author action/indicator samples; PASS |
| nesnd_ottoman_qin_supply | 改良陆军补给 | Improved Army Supply | author action/indicator samples; PASS |
| nesnd_ottoman_qin_supply_success | 完善陆军补给 | Reorganized Army Supply | author action/indicator samples; PASS |
| nesnd_ottoman_qin_supply_failed | 整顿陆军补给 | Army Supply Reforms | author action/indicator samples; PASS |
| nesnd_ottoman_claim_desc | 把军队和朝廷的扩张意愿化为正式领土要求，为日后的交涉和战争确立依据。 | Turn the ambitions of the army and court into a formal territorial claim, establishing a basis for future negotiations and war. | author action/indicator samples; PASS |
| nesnd_ottoman_claim_cost_tt | 扩张热情至少为#v 25#! | Enthusiasm for Expansion is at least #v 25#! | effect contract; exact cost/target/term; PASS |
| nesnd_ottoman_claim_spend_tt | 获得宣称后，消耗#v 25#!扩张热情。 | Spend #v 25#! Enthusiasm for Expansion when the claim is acquired. | effect contract; exact cost/target/term; PASS |
| nesnd_ottoman_claim_abu_dhabi | 宣称$STATE_ABU_DHABI$ | Claim $STATE_ABU_DHABI$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_adana | 宣称$STATE_ADANA$ | Claim $STATE_ADANA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_akmolinsk | 宣称$STATE_AKMOLINSK$ | Claim $STATE_AKMOLINSK$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_aktobe | 宣称$STATE_AKTOBE$ | Claim $STATE_AKTOBE$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_aleppo | 宣称$STATE_ALEPPO$ | Claim $STATE_ALEPPO$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_ankara | 宣称$STATE_ANKARA$ | Claim $STATE_ANKARA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_armenia | 宣称$STATE_ARMENIA$ | Claim $STATE_ARMENIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_aydin | 宣称$STATE_AYDIN$ | Claim $STATE_AYDIN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_azerbaijan | 宣称$STATE_AZERBAIJAN$ | Claim $STATE_AZERBAIJAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_baghdad | 宣称$STATE_BAGHDAD$ | Claim $STATE_BAGHDAD$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_balkh | 宣称$STATE_BALKH$ | Claim $STATE_BALKH$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_baluchistan | 宣称$STATE_BALUCHISTAN$ | Claim $STATE_BALUCHISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_basra | 宣称$STATE_BASRA$ | Claim $STATE_BASRA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_central_highlands | 宣称$STATE_CENTRAL_HIGHLANDS$ | Claim $STATE_CENTRAL_HIGHLANDS$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_cyprus | 宣称$STATE_CYPRUS$ | Claim $STATE_CYPRUS$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_deir_ez_zor | 宣称$STATE_DEIR_EZ_ZOR$ | Claim $STATE_DEIR_EZ_ZOR$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_diyarbakir | 宣称$STATE_DIYARBAKIR$ | Claim $STATE_DIYARBAKIR$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_dzungaria | 宣称$STATE_DZUNGARIA$ | Claim $STATE_DZUNGARIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_east_aegean_islands | 宣称$STATE_EAST_AEGEAN_ISLANDS$ | Claim $STATE_EAST_AEGEAN_ISLANDS$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_elizavetpol | 宣称$STATE_ELIZAVETPOL$ | Claim $STATE_ELIZAVETPOL$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_erzurum | 宣称$STATE_ERZURUM$ | Claim $STATE_ERZURUM$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_fars | 宣称$STATE_FARS$ | Claim $STATE_FARS$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_fergana | 宣称$STATE_FERGANA$ | Claim $STATE_FERGANA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_greater_caucasus | 宣称$STATE_GREATER_CAUCASUS$ | Claim $STATE_GREATER_CAUCASUS$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_hail | 宣称$STATE_HAIL$ | Claim $STATE_HAIL$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_hedjaz | 宣称$STATE_HEDJAZ$ | Claim $STATE_HEDJAZ$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_herat | 宣称$STATE_HERAT$ | Claim $STATE_HERAT$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_hudavendigar | 宣称$STATE_HUDAVENDIGAR$ | Claim $STATE_HUDAVENDIGAR$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_ili | 宣称$STATE_ILI$ | Claim $STATE_ILI$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_irakajemi | 宣称$STATE_IRAKAJEMI$ | Claim $STATE_IRAKAJEMI$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_isfahan | 宣称$STATE_ISFAHAN$ | Claim $STATE_ISFAHAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_jetisy | 宣称$STATE_JETISY$ | Claim $STATE_JETISY$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_kabul | 宣称$STATE_KABUL$ | Claim $STATE_KABUL$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_kandahar | 宣称$STATE_KANDAHAR$ | Claim $STATE_KANDAHAR$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_kars | 宣称$STATE_KARS$ | Claim $STATE_KARS$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_kastamonu | 宣称$STATE_KASTAMONU$ | Claim $STATE_KASTAMONU$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_kerman | 宣称$STATE_KERMAN$ | Claim $STATE_KERMAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_khiva | 宣称$STATE_KHIVA$ | Claim $STATE_KHIVA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_khorasan | 宣称$STATE_KHORASAN$ | Claim $STATE_KHORASAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_khuzestan | 宣称$STATE_KHUZESTAN$ | Claim $STATE_KHUZESTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_kirghizia | 宣称$STATE_KIRGHIZIA$ | Claim $STATE_KIRGHIZIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_konya | 宣称$STATE_KONYA$ | Claim $STATE_KONYA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_laristan | 宣称$STATE_LARISTAN$ | Claim $STATE_LARISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_lebanon | 宣称$STATE_LEBANON$ | Claim $STATE_LEBANON$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_luristan | 宣称$STATE_LURISTAN$ | Claim $STATE_LURISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_mazandaran | 宣称$STATE_MAZANDARAN$ | Claim $STATE_MAZANDARAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_merz | 宣称$STATE_MERZ$ | Claim $STATE_MERZ$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_mosul | 宣称$STATE_MOSUL$ | Claim $STATE_MOSUL$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_nejd | 宣称$STATE_NEJD$ | Claim $STATE_NEJD$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_northern_baluchistan | 宣称$STATE_NORTHERN_BALUCHISTAN$ | Claim $STATE_NORTHERN_BALUCHISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_oman | 宣称$STATE_OMAN$ | Claim $STATE_OMAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_palestine | 宣称$STATE_PALESTINE$ | Claim $STATE_PALESTINE$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_pashtunistan | 宣称$STATE_PASHTUNISTAN$ | Claim $STATE_PASHTUNISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_persian_kurdistan | 宣称$STATE_PERSIAN_KURDISTAN$ | Claim $STATE_PERSIAN_KURDISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_quetta | 宣称$STATE_QUETTA$ | Claim $STATE_QUETTA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_semireche | 宣称$STATE_SEMIRECHE$ | Claim $STATE_SEMIRECHE$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_semnan | 宣称$STATE_SEMNAN$ | Claim $STATE_SEMNAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_sinai | 宣称$STATE_SINAI$ | Claim $STATE_SINAI$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_sistan | 宣称$STATE_SISTAN$ | Claim $STATE_SISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_syrdarya | 宣称$STATE_SYRDARYA$ | Claim $STATE_SYRDARYA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_syria | 宣称$STATE_SYRIA$ | Claim $STATE_SYRIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_tabriz | 宣称$STATE_TABRIZ$ | Claim $STATE_TABRIZ$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_tajikistan | 宣称$STATE_TAJIKISTAN$ | Claim $STATE_TAJIKISTAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_tianshan | 宣称$STATE_TIANSHAN$ | Claim $STATE_TIANSHAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_trabzon | 宣称$STATE_TRABZON$ | Claim $STATE_TRABZON$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_transjordan | 宣称$STATE_TRANSJORDAN$ | Claim $STATE_TRANSJORDAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_turkmenia | 宣称$STATE_TURKMENIA$ | Claim $STATE_TURKMENIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_uralsk | 宣称$STATE_URALSK$ | Claim $STATE_URALSK$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_urmia | 宣称$STATE_URMIA$ | Claim $STATE_URMIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_uzbekia | 宣称$STATE_UZBEKIA$ | Claim $STATE_UZBEKIA$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_western_tianshan | 宣称$STATE_WESTERN_TIANSHAN$ | Claim $STATE_WESTERN_TIANSHAN$ | author action title + existing state name; PASS |
| nesnd_ottoman_claim_yemen | 宣称$STATE_YEMEN$ | Claim $STATE_YEMEN$ | author action title + existing state name; PASS |

## Approved repair: country-level battalion supply

The initial building-target implementation failed the frozen Tiger flow check. Current1.13 sources define military units as battalions, including marine battalions; ships have their own types/materiel/upkeep. Actual paraguay.6 country execution is the accepted analogue.

| Changed/retired key | Final editorial decision |
|---|---|
| nesnd_ottoman_reform_army_desc (zh/en) | Add only the scope clarification that all battalions, including marines, benefit. PASS: no duplicate amount and no implementation vocabulary. |
| nesnd_ottoman_qin_supply_tt | Retired from caller and localization. The national modifier preview displays quantity once. |
| nesnd_ottoman_qin_supply_success_tt | Retired from caller and localization for the same reason. |
| nesnd_ottoman_qin_supply_failed_tt | Retired from caller and localization for the same reason. |
| Three national reform modifier names | Retained. Their native previews now include actual country-level unit_supply_consumption_mult amounts alongside the unchanged military effects. PASS. |
| Three legacy supply modifier names | Retained solely to resolve old saved references during cleanup; definitions are inert and no caller applies them. |

The rows in the original table document the first frozen draft; the three explicitly retired tooltip keys above are no longer effective content. Current effective paired localization has137 keys. Runtime army goods orders/unchanged ship upkeep remain untested.


## B-r3 state-count display repair

Root identified the previously observed untranslated `num_states_greater_or_equal` native UI key in the two TUR JE eligibility rows. Each real comparison now has its own short tooltip; no surrounding decision tree is hidden.

|Actual predicate|Chinese|English|Decision|
|---|---|---|---|
|num_states >= 27 (already opened)|直接拥有至少27个地区|Directly owns at least27 states|通过：实际直接实辖数量，保留27，不重复讲恢复规则。|
|num_states >= 36 (initial entry)|直接拥有至少36个地区|Directly owns at least36 states|通过：同一口径，保留36，不将属国地算入。|

Author/UI reference: original French bar desc keeps counts separate from narrative; current Qin agenda uses one custom tooltip per native count predicate. Only the two missing labels are introduced. This is an editorial/source check, not a rendered UI result.
