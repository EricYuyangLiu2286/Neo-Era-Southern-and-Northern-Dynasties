# Americas: acceptance and indigenous revival source investigation

Date: 2026-11-04. Read-only investigation of GAME/MOD/canon; report artifacts only. Catalog status CURRENT: Victoria 3 1.13.11, Steam build 24799966, changed_count=0. No game started. This document proves available source syntax and existing data, **not engine behavior of a new implementation**.

## Actionable conclusions

1. Use `country_<culture>_cultural_acceptance_add` in a named country modifier, or `add_culture_acceptance_modifier = { culture = cu:ainu multiplier = 15 days = ... }` in country scope. Japan provides both actual forms. The generic engine effect selects the culture-specific static modifier; its multiplier is an acceptance-point amount through the native base +1 modifier. Named MOD modifiers are easier to remove when a law changes. Do not use descriptive text as the effect.
2. HUS currently has primary cultures `ce_liaodong ce_wuu hakka manchu`; citizenship `law_cultural_exclusion`; religion law `law_total_separation`. Manchu is globally overridden to `heritage_han / language_mandarin / tradition_sinosphere`. Author's new Manchu second tier therefore requires removing only HUS's Manchu primary status and applying a HUS-specific distinction. Changing global Manchu heritage would alter all countries and is unnecessary.
3. `NAH` and `TWT` are real dormant native country keys. NAH is Nahua/Mixtec/Zapotec/Tarascan, capital Mexico; TWT is Quechua, capital Lima. There is no need to invent AZT or INC. Both release definitions already exist in MOD with `use_culture_states=yes` and `ai_will_do={always=no}`. Ordinary release eligibility does not itself implement a scripted uprising.
4. **PEU does not exist at initial history.** Actual Peru populations/states belong to `NPU` (North Peru), `SPU` (South Peru), and associated `BOL` territory. New content limited to `c:PEU` will be absent at 1836. Bind to actual regional owners with safe existence checks, and transfer/initialize the persistent route when PEU later exists. A deliberate map consolidation would be a separate decision involving ownership/buildings/military; no such edit is made here.
5. Preserve every affected state-region population total while changing cultural shares. This guarantees world population conservation and stays within the fixed ±25% envelope for unchanged regions. California is split into California/North Dayuan/South Dayuan: do not read zero original totals for the two new names as unlimited population room.
6. Current ACW is a native political-movement civil war listener, not a scripted create_country example. For fixed NAH/TWT uprising creation, use Sepoy country creation + a MOD diplomatic-play definition with reciprocal annexation semantics; do not directly use `dp_revolution`, whose possible trigger requires an actual revolutionary country and its `civil_war_origin_country`.

## HUS acceptance implementation bounds

Original acceptance statuses are 0–19 violent hostility, 20–39 cultural erasure, 40–59 open prejudice, 60–79 second-rate citizen, 80–100 full acceptance. The user's ordinal 'first / second / third / fourth class' can thus map to native statuses 80+, 60–79, 40–59, 20–39, respectively. This is a design mapping, not a new engine status.

Current cultural exclusion uses primary culture 100; otherwise highest matching heritage contribution (60 exact / 50 group / 10 none), highest language contribution (50 exact / 25 group / 10 none), shared tradition 25 or none 0. Total separation adds 15 for every religion. Manchu after merely removing primary is therefore still 60+50+25+15=150 before cap: a small -20 modifier cannot implement second class. Mongol uses `heritage_mongolian`, `language_mongolian`, no traditions, and is in the north-Asian heritage group, unlike Han's east-Asian group. Indigenous cultures use `heritage_group_indigenous_american`; European/Latin-American-settler heritage group is European. MEX culture `mexican` and PEU culture `south_andean` both use `heritage_latin_american_settler`, so they belong on the settler side rather than being mistaken for Indigenous merely because they were born in America.

Recommended implementation shape: a HUS-only citizenship variant with `parent = law_cultural_exclusion` (native law-parent mechanism inherits ideological stance), a scoped visibility rule, explicit full modifiers/acceptance modifiers, and exact HUS culture bonuses. This avoids trying to cancel several inherited trait components differently for each culture. Example design arithmetic, pending review: primary 100; every nonprimary heritage match category 20, all language/tradition contributions 0; religion +15 => base35. Add named HUS-only culture bonuses: Han heritage except Manchu +55 =>90, Manchu/Mongol +35 =>70, Indigenous-American +15 =>50, European -5 =>30. These are suggested balance values, not sourced historical proportions. Every relevant culture key needs a defined modifier type (MOD already has ce_* declarations); static named modifiers can enumerate actual cultures, or generic effect can iterate cultures with tested trait predicates. Additions must occur once, not monthly stack; law exit/reform removes them. Keep an explicit policy for Japanese/Korean/African/other cultures rather than accidentally labeling every non-Chinese population white. Future religious-law changes and new community acceptance deltas can move actual pop acceptance away from these base targets; display measured `country_average_culture_pop_acceptance` and distinguish current actual acceptance from intended legal status.

Austria proves real measurement: Hungarian average >=80 for 60 monthly checks; federal integration actually `add_primary_culture`, while disqualification `remove_primary_culture`. Do not add Manchu as a primary culture to simulate second-class citizenship. New communities can start with -30% acceptance delta and recover 0.25/month; mass migration requires prospective acceptance >=30. These mechanics make 'exiles allowed' different from promising instant mass immigration.

## Identity and narrative facts

PPET slide18 states Cuauhtemoc fled into Wu territory and received a Song princely title; Aztec descendants restored in1712 and paid tribute to Wu. HUS supported the Mexican republic in1811–15. PPET slide19 has Wu naval intervention against Pizarro in1534, the third Inca empire restored in1653 accepting Northern Ming investiture, upper elite adopting Confucianism in1653–1865, and war with La Plata in1836–39. The newest author's request controls the revised playable native-revival outcome; the PPET imperial continuity should inform the surviving dynastic/cultural base rather than be presented as a real-world extinct civilization.

The biography cache corroborates Wu conquest of Mexico in1590, creation of Dayuan/Jinlin/Taiyuan colonial offices, and Han/Manchu/Mongol independence participants in1620. It does not supply precise1836 census percentages. No HOI4 syntax is used; the old project's country-file filename search did not provide a stronger relevant canonical source than PPET/biography, so importing it is unnecessary.

## Population baseline and bounded rebalance proposal

Effective sources combine GAME then MOD by file replacement. MEX population is 6,699,263. Mexican culture 3,846,334 (57.41%); all Indigenous groups 2,746,808 (41.00%); Afro-Caribeno106,121 (1.58%). Indigenous core NAH cultures: Nahua1,243,589; Tarascan333,081; Mixtec39,996; Zapotec317,719 =1,934,385 (28.87%). Other natives include Mayan460,968, Oodham335,455, Apache16,000. NAH core should not swallow Mayan culture identity automatically.

The current distribution already supports regional native majorities in Mexico proper, Oaxaca, Guerrero and Zacatecas. A bounded candidate can convert 20–30% of each *existing Mexican-culture row* in Mexico/Bajio/Guerrero/Oaxaca/Zacatecas to that state's existing native cultures, preserving the existing native mix and using integer largest-remainder allocation. This is a proposed author-informed design choice, not a canon census. Leave northern Oodham/Apache and Mayan Yucatan distinct, and keep every existing religion/pop-type/slave field when splitting. Do not convert whole populations to a monoculture or delete settlers.

NPU866,600: Quechua402,700, Amazonian68,000, South-Andean351,800, Afro44,100 (54.31% indigenous). SPU681,108: Quechua389,304, Aimara118,900, Amazonian12,000, South-Andean152,904, Afro8,000 (76.38% indigenous). Combined NPU+SPU1,547,708 with Indigenous990,904 (64.02%). BOL1,394,398 has at least Quechua491,500+Aimara454,200, plus Amazonian/Guarani. This is already a strong native demographic base. For the strongest PPET-continuity correction, rebalance only Lima's South-Andean248,000 versus Quechua212,000/Amazonian16,000: e.g. move49,600 (=20% of settler row) to existing Quechua while keeping Lima504,100 unchanged; this yields277,600 indigenous/504,100=55.07%. No global increase is needed. Do not conflate Quechua with Aimara or Amazonian identities. The exact candidate target requires the parent's implementation judgment.

Full region/country/culture values, total-region denominators, source paths, and fixed original baselines are saved next to this report in `americas-population-baseline.json`. Read the fixed geographic mapping for split California through population_envelope_audit, not simple name matches.

## Uprising, victory, suppression, refuge chain

Owner country owns the JE. Select a native homeland state actually owned by that country; save owner, state and target-tag identities before creation. At launch recheck owner alive, minimum held states after cession, peace/diplomatic-play/truce conditions, native pop presence, and target tag not already alive. Use actual state intersection (`s:STATE_...region_state:OWNER`), not a bare region pretending to be state. `create_country` supports tag, origin, repeated state/province, and on_created in the new country scope. With origin set, explicitly reset primary cultures to the selected NAH/TWT definition and set native political laws/religion/leader as required; do not assume origin inheritance yields native identity.

A dedicated uprising DP can borrow `war_goal=annex_country`, `mirror_war_goal=yes`, `allow_negotiated_peace=no`, no extra demands, no starting infamy from native `dp_revolution`; its possible rules must be rewritten for fixed native tags. Or explicitly add the defender's annex demand using verified current fields. Fixed TAG country creation + a war is not identical to the engine's dynamically created political revolution. Record the distinction honestly in code/docs. War winner annexation yields whole-country replacement; secession only yields independence. Choose which outcome the design actually wants.

Native source/current docs mismatch: engine effects docs still describe scoped-target + initiator + country fields, but current Sepoy scripts and current MOD India use scoped-initiator `target_country` plus goal `target_country`. Prefer current working source shape and source-linked existing MOD pattern; do not silently 'fix' it to doc prose. Original GAME has no occurrence of `handle_annexation_as_civil_war` in current script corpus, so that flag remains engine-doc-supported but unproven here. Native ACW captures existing CSA/FSA after movement civil war and transfers tagged Confederate characters; it does not create countries or reciprocal goals in the JE.

Suppression must capture the same native leader before country death so refuge does not resurrect a random replacement. `exile_character=yes` sends a character to the global exile pool and does NOT target HUS. Actual hosted refuge uses `replace_character_roles = { add={ agitator } remove_all=yes }` then `transfer_character = c:HUS`, following Duleep Singh→GBR. Check HUS alive and eligible, character alive and not an unrelated ruler/heir, clear military/political roles correctly, then transfer. If HUS no longer exists choose a defined no-host/exile fallback. Existing creation source is a guide, not proof this new post-annexation timing survives destruction; requires targeted engine test or safe pre-annexation callback. Pop refugee movement is a separate mechanism (`move_pop` moves the entire selected pop; generic mass migration is not a guaranteed exact headcount). The user asked suppressed leaders to flee; do not silently move all native populations.

## USA anti-HUS investment / claims / war route

Use actual investment rights, not a throughput modifier labeled investment. `foreign_investment_rights` treaty article is directed: original GBR/POR treaty has source_country=POR, target_country=GBR, granting British rights in Portugal. Therefore USA investing in a native country uses source_country=native host, target_country=USA. Rights are access; they do not create construction or foreign-owned buildings by themselves. Subsequent native construction can be validated through ownership/building facts. Add national-budget support separately with an explicit duration/cost if requested.

Claims use state-region `add_claim = c:USA`, supported by engine docs. Limit them to the contested region list and actual HUS ownership, save the list, and require real completion (USA ownership or an agreed political outcome) rather than claiming that a claim already won territory. War uses a dedicated DP or native return-state type with the selected target_state and current source-format target_country; HUS absent/ownership changed/truce/subject and third-party intervention must have defined exits. USA support to native movements should improve relations/real investment capability or war backing, without erasing the native player's independent choices.

## Verification needed by implementation

Static: exact legal/culture keys, full referenced modifier declarations/localization, state ownership intersection, unchanged world and region totals, no duplicated primary/native definitions, bounded per-law modifiers, safe missing objects, one-time launch/settlement/refuge locks. Engine: actual HUS pop acceptance for a Han nonprimary, Manchu, Mongol, Indigenous and European culture; law reform cleanup; new-country culture and units; both reciprocal war outcomes; leader alive in HUS after suppression. None of these new engine scenarios were run in this investigation.

## Source excerpts and fingerprints

Every excerpt below was read from the local file shown. Paths are absolute; line numbers are 1-based. Hashes bind the whole source file, not the excerpt. Cached extracted canon contains original slide or Word paragraph anchors in each line. The generated docs are cited from current USERDATA/docs, with a matching1.13.11 reference copy available.

### HUS identity

[ce_countries.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt:38) — lines 38–46; SHA-256 `7056d622fb21e0d3a72f0af4f73a9a5e23a87f769870b23c5df9043f8fbfb6f5`

```text
38: HUS = {
39: 	color = { 5 49 117 }
40: 	
41: 	country_type = recognized
42: 	tier = empire
43: 	
44: 	cultures = { ce_liaodong ce_wuu hakka manchu } 
45: 	capital = STATE_CALIFORNIA
46: }
```

### HUS laws

[HUS.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/HUS.txt:72) — lines 72–91; SHA-256 `cb1485aa1ec06d0706806a9dbbdb6ab458ea78cbf796ac506a2482c6ecb33608`

```text
72: 		activate_law = law_type:law_census_voting
73: 		activate_law = law_type:law_per_capita_based_taxation
74: 		activate_law = law_type:law_elected_bureaucrats
75: 		activate_law = law_type:law_private_schools
76: 		activate_law = law_type:law_tenant_farmers
77: 		activate_law = law_type:law_laissez_faire
78: 		activate_law = law_type:law_mercantilism	
79: 		activate_law = law_type:law_cultural_exclusion
80: 		activate_law = law_type:law_professional_army
81: 		activate_law = law_type:law_no_migration_controls
82: 		activate_law = law_type:law_censorship
83: 		activate_law = law_type:law_debt_slavery
84: 		activate_law = law_type:law_no_womens_rights
85: 		activate_law = law_type:law_frontier_colonization
86: 
87: 		# COOP
88: 		add_company = company_type:company_ce_daqing_coop
89: 		company:company_ce_daqing_coop = {
90: 			set_company_establishment_date = 1721.12.12
91: 			set_company_state_region = s:STATE_WASHINGTON
```

### Manchu override

[CE_cultures.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/cultures/CE_cultures.txt:292) — lines 292–298; SHA-256 `deab0fd04a418e17f063665669610d3930d1af007a513d38da6b86247fe400b0`

```text
292: REPLACE:manchu={
293: 	color = rgb{ 233 207 84 }
294: 	religion = mahayana
295: 	heritage = heritage_han
296: 	language = language_mandarin
297: 	traditions = { tradition_sinosphere }
298: 	obsessions = {
```

### Mexico definition

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2149) — lines 2149–2160; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
2149: MEX = {
2150: 	color = { 56 143 53 }
2151: 
2152: 	country_type = recognized
2153: 
2154: 	#173  242  175
2155: 
2156: 	tier = kingdom
2157: 
2158: 	cultures = { mexican }
2159: 	capital = STATE_MEXICO
2160: 	is_named_from_capital = yes
```

### Peru definition

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2381) — lines 2381–2390; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
2381: PEU = {
2382: 	color = { 124  140  162 }
2383: 
2384: 	country_type = recognized
2385: 
2386: 	tier = kingdom
2387: 
2388: 	cultures = { south_andean }
2389: 	capital = STATE_LIMA
2390: }
```

### Nahua definition

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2786) — lines 2786–2795; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
2786: NAH = {
2787: 	color = hsv360{ 130 100 52 }
2788: 
2789: 	country_type = unrecognized
2790: 
2791: 	tier = principality
2792: 
2793: 	cultures = { nahua mixtec zapotec tarascan }
2794: 	capital = STATE_MEXICO
2795: }
```

### Inca definition

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:3109) — lines 3109–3119; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
3109: TWT = { # Tawantinsuyu
3110: 	color = { 125 92 110 }
3111: 
3112: 	country_type = unrecognized
3113: 
3114: 	tier = kingdom
3115: 
3116: 	cultures = { quechua }
3117: 
3118: 	capital = STATE_LIMA
3119: }
```

### Release NAH

[00_releasable_countries.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_creation/00_releasable_countries.txt:743) — lines 743–746; SHA-256 `269b5bd06f7c46698da446fdcbe2df2869217660c57074988458554e27229bce`

```text
743: NAH = {
744: 	use_culture_states = yes
745: 	ai_will_do = { always = no }
746: }
```

### Release TWT

[00_releasable_countries.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_creation/00_releasable_countries.txt:888) — lines 888–892; SHA-256 `269b5bd06f7c46698da446fdcbe2df2869217660c57074988458554e27229bce`

```text
888: TWT = {
889: 	use_culture_states = yes
890: 
891: 	ai_will_do = { always = no }
892: }
```

### Generic acceptance engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:139) — lines 139–141; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
139: ## add_culture_acceptance_modifier
140: Apply a cultural acceptance modifier in the scoped country for the given culture. Other than the required culture argument, this effect has the same syntax as add_modifier.
141: **Supported Scopes**: country  
```

### Japan acceptance caller

[ep2_hokkaido_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ep2_hokkaido_events.txt:410) — lines 410–438; SHA-256 `017027ee155f7b864004740da5ab6e6d223151826fc198c401285c3475199b32`

```text
410: 
411: 	option = {
412: 		name = hokkaido_events.2.c
413: 		scope:hokkaido_state_scope = {
414: 			add_radicals_in_state = {
415: 				value = large_radicals
416: 				culture = cu:japanese
417: 			}
418: 			add_loyalists_in_state = {
419: 				value = large_radicals
420: 				culture = cu:ainu
421: 			}
422: 			add_modifier = {
423: 				name = modifier_restricted_settlements
424: 				days = very_long_modifier_time
425: 			}
426: 		}
427: 		add_culture_acceptance_modifier = {
428: 			culture = cu:ainu
429: 			days = very_long_modifier_time
430: 			multiplier = 15
431: 		}
432: 		custom_tooltip = {
433: 			text = the_ainu_will_appreciate_this_tt
434: 			change_variable = {
435: 				name = ainu_friendship_var
436: 				add = 1
437: 			}
438: 		}
```

### Japan fixed modifier

[00_ep2_02_modifiers.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ep2_02_modifiers.txt:148) — lines 148–152; SHA-256 `151e77e1d57c7bd5b239674f7d5b13dfe4189f8d9b1dc0a7c4fba5067f37be47`

```text
148: modifier_ainu_heritage_aknowleged = {
149: 	icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
150: 	country_ainu_cultural_acceptance_add = 10
151: 	state_assimilation_mult = -0.2
152: }
```

### Acceptance tiers

[00_acceptance_statuses.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/acceptance_statuses/00_acceptance_statuses.txt:1) — lines 1–54; SHA-256 `a4edb8eb0b7d78d34d0fbd320312856cd0e41b60e9c1d3713fe767fed7425409`

```text
1: violent_hostility = {
2: 	threshold = 0
3: 	base_migration_desire = 100
4: 	war_exhaustion_impact_own_side = 0
5: 	war_exhaustion_impact_other_side = 0
6: 	color = { 180 75 80 }
7: 	small_icon = "gfx/interface/icons/acceptance_icons/acceptance_number1.dds"
8: 	large_icon = "gfx/interface/icons/acceptance_icons/acceptance_tier1.dds"
9: 	background = "gfx/interface/icons/acceptance_icons/bg_illu_acceptance_t1.dds"
10: }
11: 
12: cultural_erasure = {
13: 	threshold = 20
14: 	base_migration_desire = 100
15: 	war_exhaustion_impact_own_side = 0
16: 	war_exhaustion_impact_other_side = 0
17: 	color = { 175 100 75 }
18: 	small_icon = "gfx/interface/icons/acceptance_icons/acceptance_number2.dds"
19: 	large_icon = "gfx/interface/icons/acceptance_icons/acceptance_tier2.dds"
20: 	background = "gfx/interface/icons/acceptance_icons/bg_illu_acceptance_t2.dds"
21: }
22: 
23: open_prejudice = {
24: 	threshold = 40
25: 	base_migration_desire = 50
26: 	war_exhaustion_impact_own_side = 0.5
27: 	war_exhaustion_impact_other_side = 0
28: 	color = { 155 130 100 }
29: 	small_icon = "gfx/interface/icons/acceptance_icons/acceptance_number3.dds"
30: 	large_icon = "gfx/interface/icons/acceptance_icons/acceptance_tier3.dds"
31: 	background = "gfx/interface/icons/acceptance_icons/bg_illu_acceptance_t3.dds"
32: }
33: 
34: second_rate_citizen = {
35: 	threshold = 60
36: 	base_migration_desire = 20
37: 	war_exhaustion_impact_own_side = 1.5
38: 	war_exhaustion_impact_other_side = 0.5
39: 	color = { 130 155 90 }
40: 	small_icon = "gfx/interface/icons/acceptance_icons/acceptance_number4.dds"
41: 	large_icon = "gfx/interface/icons/acceptance_icons/acceptance_tier4.dds"
42: 	background = "gfx/interface/icons/acceptance_icons/bg_illu_acceptance_t4.dds"
43: }
44: 
45: full_acceptance = {
46: 	threshold = 80
47: 	base_migration_desire = 0
48: 	war_exhaustion_impact_own_side = 3
49: 	war_exhaustion_impact_other_side = 3
50: 	color = { 90 150 150 }
51: 	small_icon = "gfx/interface/icons/acceptance_icons/acceptance_number5.dds"
52: 	large_icon = "gfx/interface/icons/acceptance_icons/acceptance_tier5.dds"
53: 	background = "gfx/interface/icons/acceptance_icons/bg_illu_acceptance_t5.dds"
54: }
```

### Citizenship calculation

[00_citizenship.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_citizenship.txt:528) — lines 528–599; SHA-256 `c006054323511c81b40502810c4ed8f6a806ebde02bf0a3023538e756ec9bb10`

```text
528: 	modifier = {
529: 		country_authority_add = 50
530: 		country_support_separatism_resistance_mult = 0.25
531: 		country_support_separatism_strength_mult = -0.25
532: 
533: 		#If primary culture, only apply this value
534: 		country_acceptance_primary_culture_add = 100
535: 
536: 		#Heritage
537: 		#From this block, we only apply the highest value a Pop qualifies for
538: 		country_acceptance_shared_heritage_trait_add = 60
539: 		country_acceptance_shared_heritage_trait_group_add = 50
540: 		country_acceptance_no_shared_heritage_trait_add = 10
541: 
542: 		#Language
543: 		#From this block, we only apply the highest value a Pop qualifies for
544: 		country_acceptance_shared_language_trait_add = 50
545: 		country_acceptance_shared_language_trait_group_add = 25
546: 		country_acceptance_no_shared_language_trait_add = 10
547: 
548: 		#Tradition
549: 		#From this block, we only apply the highest value a Pop qualifies for
550: 		country_acceptance_shared_tradition_trait_add = 25
551: 		country_acceptance_no_shared_tradition_trait_add = 0
552: 
553: 		#Fervor
554: 		country_primary_culture_fervor_from_laws_add = 5
555: 	}
556: 
557: 	acceptance_modifier = {
558: 		country_allow_assimilation_cultural_erasure_bool = yes
559: 		country_allow_assimilation_open_prejudice_bool = yes
560: 		country_allow_assimilation_second_rate_citizen_bool = yes
561: 		country_allow_assimilation_full_acceptance_bool = yes
562: 
563: 		country_assimilation_cultural_erasure_mult = 0.05
564: 		country_assimilation_open_prejudice_mult = 0.15
565: 
566: 		country_allow_voting_violent_hostility_bool = no
567: 		country_voting_power_cultural_erasure_mult = -0.25
568: 		country_allow_voting_cultural_erasure_bool = yes
569: 		country_allow_voting_open_prejudice_bool = yes
570: 		country_allow_voting_second_rate_citizen_bool = yes
571: 		country_allow_voting_full_acceptance_bool = yes
572: 
573: 		country_political_strength_violent_hostility_mult = -0.3
574: 		country_political_strength_cultural_erasure_mult = -0.2
575: 		country_political_strength_open_prejudice_mult = -0.1
576: 		country_political_strength_second_rate_citizen_mult = 0.1
577: 		country_political_strength_full_acceptance_mult = 0.1
578: 
579: 		country_wage_violent_hostility_mult = -0.3
580: 		country_wage_cultural_erasure_mult = -0.2
581: 		country_wage_open_prejudice_mult = -0.1
582: 		country_wage_full_acceptance_mult = 0.05
583: 
584: 		country_qualification_growth_violent_hostility_mult = -0.5
585: 		country_qualification_growth_cultural_erasure_mult = -0.3
586: 		country_qualification_growth_open_prejudice_mult = -0.1
587: 
588: 		country_disallow_military_work_violent_hostility_bool = no
589: 		country_disallow_military_work_cultural_erasure_bool = no
590:  		country_disallow_military_work_open_prejudice_bool = no
591: 		country_disallow_military_work_second_rate_citizen_bool = no
592: 		country_disallow_military_work_full_acceptance_bool = no
593: 
594: 		country_disallow_government_work_violent_hostility_bool = yes
595: 		country_disallow_government_work_cultural_erasure_bool = no
596: 		country_disallow_government_work_open_prejudice_bool = no
597: 		country_disallow_government_work_second_rate_citizen_bool = no
598: 		country_disallow_government_work_full_acceptance_bool = no
599: 	}
```

### Religion contribution

[00_church_and_state.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_church_and_state.txt:483) — lines 483–487; SHA-256 `ad4e366533b268a86f29813c13aeae6f7472d94de84c35bfe51ce960fd8bb015`

```text
483: 	modifier = {
484: 		country_acceptance_state_religion_add = 15
485: 		country_acceptance_shared_religious_trait_add = 15
486: 		country_acceptance_shared_religious_trait_group_add = 15
487: 		country_acceptance_no_shared_religious_trait_add = 15
```

### Law parent example

[00_church_and_state.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_church_and_state.txt:243) — lines 243–247; SHA-256 `ad4e366533b268a86f29813c13aeae6f7472d94de84c35bfe51ce960fd8bb015`

```text
243: law_people_of_the_book = { # Other Muslim states
244: 	group = lawgroup_church_and_state
245: 	parent = law_state_religion # Inherits ideological stances from parent
246: 
247: 	icon = "gfx/interface/icons/law_icons/people_of_the_book.dds"
```

### Acceptance bounds

[00_defines.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt:1488) — lines 1488–1507; SHA-256 `e47db10931a2149c80aadab0b8de8f3fa000fdbb82a2f878fee893aa4434dd39`

```text
1488: 	# Acceptance #
1489: 	MIN_ACCEPTANCE_VALUE = 0													# It is both the minimum acceptance value a pop can have as well as the explicit threshold scripted for the first acceptance status [any signed 32 bit value]
1490: 	MAX_ACCEPTANCE_VALUE = 100													# It is both the maximum acceptance value a pop can have as well as the (implied) upper bound of the last acceptance status [> MIN_ACCEPTANCE_VALUE]
1491: 	ACCEPTANCE_FROM_HOMELAND_COMMUNITY = 0										# The amount of acceptance a pop gets from living in their homeland, applied statically on their Cultural Community
1492: 	ACCEPTANCE_FROM_NOT_HOMELAND_COMMUNITY = 0									# The amount of acceptance a pop gets from not living in their homeland, applied statically on their Cultural Community
1493: 	MIN_REQUIRED_ACCEPTANCE_FOR_MIGRATION = 30		 							# If a pop would have less than this much acceptance in a target state, they won't mass migrate there
1494: 	EXPECTED_ACCEPTANCE_INCREASE_TO_MIGRATE = 10                                # A pop will look to increase their acceptance by this much when mass migrating, but might accept less if mass migration attraction difference is high enough
1495: 	MAX_ACCEPTANCE_RATIO_MULT_MIGRATION = 5										# A difference in acceptance between source and target in mass migrations will result in at most this much increased migration
1496: 
1497: 	BUCKET_MIGRATION_EXPIRATION_YEARS = 5									    # How long a migration bucket will be kept before it is removed
1498: 	BUCKET_MIGRATION_THRESHOLD = 1000											# How many pops need to be in a bucket before it is executes migration
1499: 	BUCKET_MIGRATION_MIN_LEFTOVER_THRESHOLD = 1000								# Minimum number of pops that can stay without being moved over to another state when a bucket migration is executed
1500: 	MIGRATION_PULL_CULTURE_VACANCIES_MODIFIER = 0.25							# Modifies migration pull for pop if there is vacancies available for the pop culture
1501: 	MIGRATION_PULL_CULTURE_NO_VACANCIES_MODIFIER = -0.5							# Modifies migration pull for pop if there is no vacancies available for the pop culture
1502: 
1503: 	# Cultural Communities #
1504: 	CULTURAL_COMMUNITY_LINGER_TIME_WEEKS = 3									# When the last pop of a given culture leaves a state, the corresponding cultural community will be removed after this long
1505: 	CULTURAL_COMMUNITY_MAX_PER_MONTH_CHANCE = 0.04
1506: 	CULTURAL_COMMUNITY_ACCEPTANCE_DELTA_ON_SPAWN = -0.3							# The percentage of the maximum cultural acceptance that should be added as a delta to the cultural community when it first appears
1507: 	CULTURAL_COMMUNITY_ACCEPTANCE_DELTA_DECAY_PER_MONTH = 0.25					# The amount of acceptance delta that will decay each month
```

### Austria measured acceptance

[05_austria_journal_entries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_austria_journal_entries.txt:26) — lines 26–74; SHA-256 `abc3af4f08ee235a250a2dca949cc4bf1b0e835b62c2380813ccf19b8614b369`

```text
26: 		OR = {
27: 			custom_tooltip = {
28: 				text = je_matter_of_hungary_completion_autonomy_tt
29: 				has_variable = established_austria_hungary_var
30: 			}
31: 			custom_tooltip = {
32: 				text = hungarian_above_80_acceptance_for_a_while_tt
33: 				has_variable = hungarian_acceptance_var
34: 				var:hungarian_acceptance_var >= 60 # This 60 has nothing to do with the acceptance value itself
35: 			}
36: 			AND = {
37: 				NOT = {
38: 					exists = c:HUN
39: 				}
40: 				custom_tooltip = {
41: 					text = hungarian_movements_pacified_tt
42: 					any_political_movement = {
43: 						is_political_movement_type = movement_cultural_minority
44: 						culture ?= cu:hungarian
45: 						political_movement_radicalism < define:NPolitics|RADICALISM_AGITATING_THRESHOLD
46: 					}
47: 				}
48: 				any_scope_state = {
49: 					state_region = {
50: 						is_homeland = cu:hungarian
51: 					}
52: 					count >= 8
53: 					is_incorporated = yes
54: 					turmoil < 0.05
55: 				}
56: 			}
57: 		}
58: 	}
59: 
60: 	on_monthly_pulse = {
61: 		effect = {
62: 			if = {
63: 				limit = {
64: 					country_average_culture_pop_acceptance = {
65: 						culture = cu:hungarian
66: 						value >= 80
67: 					}
68: 				}
69: 				change_variable = { name = hungarian_acceptance_var add = 1 }
70: 			}
71: 			else = {
72: 				set_variable = { name = hungarian_acceptance_var value = 0 }
73: 			}
74: 		}
```

### Austria integration

[00_victoria_ip3_scripted_effects.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip3_scripted_effects.txt:113) — lines 113–165; SHA-256 `50ebf064dc069c7f157b0bb9b46cc96902c8121d6f4dc5a0f21583c1625f4c3d`

```text
113: danubian_federation_integrate_culture = {
114: 	$CULTURE$ = { # Saves relevant culture, for localisation purposes
115: 		save_scope_as = relevant_culture_scope
116: 	}
117: 	if = {
118: 		limit = {
119: 			NOT = { country_has_primary_culture = $CULTURE$ }
120: 		}
121: 		if = {
122: 			limit = {
123: 				NOT = {
124: 					is_target_in_variable_list = { name = aus_integrated_cultures target = $CULTURE$ }
125: 				}
126: 			}
127: 			add_to_variable_list = { name = aus_integrated_cultures target = $CULTURE$ }
128: 			change_variable = { name = count_integrated_cultures add = 1 }
129: 
130: 			every_subject_or_below = {
131: 				limit = {
132: 					OR = {
133: 						is_subject_type = subject_type_personal_union
134: 						is_subject_type = subject_type_crown_land
135: 						is_subject_type = subject_type_puppet
136: 					}
137: 					country_has_primary_culture = $CULTURE$
138: 				}
139: 				post_notification = danubian_federation_culture_integrated
140: 			}
141: 		}
142: 		if = { # Note - should never happen, but just in case it does.
143: 			limit = {
144: 				is_target_in_variable_list = { name = aus_disqualified_cultures target = $CULTURE$ }
145: 			}
146: 			remove_list_variable = { name = aus_disqualified_cultures target = $CULTURE$ }
147: 			change_variable = { name = count_disqualified_cultures subtract = 1 }
148: 		}
149: 		custom_tooltip = {
150: 			text = successful_integration_tt
151: 			add_primary_culture = $CULTURE$
152: 		}
153: 	}
154: }
155: 
156: danubian_federation_disqualify_culture = {
157: 	$CULTURE$ = { # Saves relevant culture, for localisation purposes
158: 		save_scope_as = relevant_culture_scope
159: 	}
160: 
161: 	if = { # Removes primary culture, in the case that it's already integrated
162: 		limit = {
163: 			country_has_primary_culture = $CULTURE$
164: 		}
165: 		remove_primary_culture = $CULTURE$
```

### Native trait classification

[acw_wild_west_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/american_civil_war/acw_wild_west_events.txt:115) — lines 115–145; SHA-256 `5b137b73e884c1a735dda36bdf7b89203a585eb4ec4683519f214a49cf2c1695`

```text
115: 	duration = 3
116: 
117: 	cooldown = { days = short_modifier_time }
118: 
119: 	trigger = {
120: 		any_scope_state = {
121: 			is_incorporated = no
122: 			has_building = building_railway
123: 			any_scope_pop = { culture = { has_discrimination_trait_group = heritage_group_indigenous_american } }
124: 			NOT = {
125: 				has_modifier = iron_horse_raids
126: 			}
127: 		}
128: 	}
129: 
130: 	immediate = {
131: 		random_scope_state = {
132: 			limit = {
133: 				is_incorporated = no
134: 				has_building = building_railway
135: 				any_scope_pop = {
136: 					culture = { has_discrimination_trait_group = heritage_group_indigenous_american }
137: 				}
138: 			}
139: 			random_scope_pop = {
140: 				limit = {
141: 					culture = { has_discrimination_trait_group = heritage_group_indigenous_american }
142: 				}
143: 				culture = {	save_scope_as = native_people_infringed }
144: 			}
145: 			save_scope_as = raided_railroad
```

### Culture traits

[00_cultural_heritages.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/discrimination_traits/00_cultural_heritages.txt:328) — lines 328–356; SHA-256 `06d6638c64c1185a3e8a01102958bfaa5ef57a9c657bf82528cd89f4ec622443`

```text
328: heritage_manchu = {
329: 	type = heritage
330: 	trait_group = heritage_group_north_asian
331: }
332: 
333: heritage_melanesian = {
334: 	type = heritage
335: 	trait_group = heritage_group_indigenous_oceanic
336: }
337: 
338: heritage_mesoamerican = {
339: 	type = heritage
340: 	trait_group = heritage_group_indigenous_american
341: }
342: 
343: heritage_miao = {
344: 	type = heritage
345: 	trait_group = heritage_group_east_asian
346: }
347: 
348: heritage_micronesian = {
349: 	type = heritage
350: 	trait_group = heritage_group_indigenous_oceanic
351: }
352: 
353: heritage_mongolian = {
354: 	type = heritage
355: 	trait_group = heritage_group_north_asian
356: }
```

### Actual native DP caller

[00_sepoy_mutiny_scripted_effects.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:461) — lines 461–495; SHA-256 `be32f69bde816f2216d18a29ae1aebca1859f22ea25cf9504b25cf62ff519534`

```text
461: 	# Mughal uprising
462: 	# Mughal independence war diplomatic play
463: 	if = {
464: 		limit = {
465: 			exists = c:MUG
466: 			NOT = {
467: 				any_diplomatic_play = {
468: 					target = { c:MUG ?= this }
469: 					initiator = { c:BIC ?= this }
470: 					is_diplomatic_play_type = dp_secession
471: 				}
472: 			}
473: 		}
474: 		create_diplomatic_play = {
475: 			name = sepoy_mutiny
476: 			type = dp_sepoy_mutiny
477: 			escalation = 80
478: 			target_country = c:MUG
479: 		}
480: 		# Add Britain
481: 		random_diplomatic_play = {
482: 			limit = {
483: 				is_diplomatic_play_type = dp_sepoy_mutiny
484: 				target = {
485: 					c:MUG ?= this
486: 				}
487: 			}
488: 			if = {
489: 				limit = {
490: 					initiator = {
491: 						is_subject = yes
492: 					}
493: 				}
494: 				add_initiator_backers = { initiator.top_overlord }
495: 			}
```

### Country creation

[00_sepoy_mutiny_scripted_effects.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:33) — lines 33–51; SHA-256 `be32f69bde816f2216d18a29ae1aebca1859f22ea25cf9504b25cf62ff519534`

```text
33: 	else_if = {
34: 		limit = {
35: 			NOT = { exists = c:MUG }
36: 			exists = s:STATE_DELHI.region_state:BIC
37: 			p:xE0EFA0.state.owner = root
38: 		}
39: 		create_country = {
40: 			origin = root
41: 			tag = MUG
42: 			province = p:xE0EFA0
43: 			on_created = {
44: 				set_variable = sepoy_mutiny_revolter_var
45: 				sepoy_mutiny_apply_laws_effect = yes
46: 				add_modifier = {
47: 					name = war_for_independence
48: 					days = normal_modifier_time
49: 				}
50: 				s:STATE_DELHI.region_state:BIC ?= { set_state_owner = c:MUG }
51: 			}
```

### DP engine documentation

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:909) — lines 909–922; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
909: ## create_diplomatic_play
910: Create a diplomatic play with the scoped object as target  
911: create_diplomatic_play = {  
912: 	name = loc_key  
913: 	escalation = integer between 0 and 100  
914: 	war = bool  
915: 	initiator = country scope/tag  
916: 	type = diplomatic play type  
917: 	handle_annexation_as_civil_war = yes/no  
918: 	add_initiator_backers = { list of country scopes/tags }  
919: 	add_target_backers = { list of country scopes/tags }  
920: 	add_war_goal = { holder = country scope/tag, type = x, state = <state target>, country = <country target,> region = <region target>  }  
921: }
922: **Supported Scopes**: country  
```

### Country engine documentation

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:878) — lines 878–890; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
878: ## create_country
879: Creates a new country  
880: create_country = {  
881: 	tag = TAG			# optional, if not specified origin's tag will be used  
882: 	origin = country	# optional, newly created country will inherit certain values from the origin country  
883: 	                    # at least one of tag or origin must be supplied  
884: 	state = state		# can be repeated; at least one state or province must be supplied  
885: 	province = province	# can be repeated; at least one state or province must be supplied  
886: 						# both states and provinces can be supplied at the same time  
887: 	on_created = effect	# optional effect that will be run with the newly created country in scope  
888: }
889: **Supported Scopes**: none  
890: 
```

### Revolution DP restrictions

[00_diplomatic_plays.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:521) — lines 521–543; SHA-256 `4f4c61ad1198cc1b862e6399fb08cff7813be815d8c3644b08e3d43a708c00a9`

```text
521: dp_revolution = {
522: 	requires_interest_marker = no
523: 	enable_switch_sides = yes
524: 	allow_negotiated_peace = no
525: 	mirror_war_goal = yes
526: 	initiator_can_add_war_goals = no
527: 	target_can_add_war_goals = no
528: 	add_infamy_for_starting_initiator_wargoals = no
529: 
530: 	war_goal = annex_country
531: 
532: 	texture = "gfx/interface/icons/war_goals/annex_country.dds"
533: 
534: 	selectable_in_lens = {
535: 		always = no
536: 	}
537: 
538: 	possible = {
539: 		scope:initiator = {
540: 			is_revolutionary = yes
541: 		}
542: 		scope:initiator.civil_war_origin_country = scope:target_country
543: 	}
```

### Sepoy DP

[00_diplomatic_plays.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:1368) — lines 1368–1391; SHA-256 `4f4c61ad1198cc1b862e6399fb08cff7813be815d8c3644b08e3d43a708c00a9`

```text
1368: dp_sepoy_mutiny = {
1369: 	war_goal = annex_country
1370: 
1371: 	allow_negotiated_peace = no
1372: 	add_infamy_for_starting_initiator_wargoals = no
1373: 
1374: 	texture = "gfx/interface/icons/war_goals/annex_country.dds"
1375: 
1376: 	selectable_in_lens = {
1377: 		always = no
1378: 	}
1379: 
1380: 	possible = {}
1381: 
1382: 	ai_acceptance_max = 75
1383: 
1384: 	on_weekly_pulse = {}
1385: 
1386: 	on_war_begins = {}
1387: 
1388: 	on_war_end = {
1389: 
1390: 	}
1391: }
```

### ACW lifecycle

[00_acw_entries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_acw_entries.txt:26) — lines 26–44; SHA-256 `f164d68b6422676c1ed410f75532a05b18b091a77dea628bc9b62ab1d859e3fa`

```text
26: 	fail = {
27: 		OR = {
28: 			has_civil_war_from_movement_type = movement_type:movement_pro_slavery
29: 			has_civil_war_from_movement_type = movement_type:movement_anti_slavery
30: 		}
31: 	}
32: 
33: 	on_fail = {
34: 		if = {
35: 			limit = {
36: 				has_civil_war_from_movement_type = movement_type:movement_pro_slavery
37: 			}
38: 			set_variable = csa_will_spawn_var
39: 		}
40: 		custom_tooltip = {
41: 			text = acw_will_happen_tt
42: 			trigger_event = { id = acw_je_events.1 }
43: 		}
44: 	}
```

### ACW character move

[acw_je_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/american_civil_war/acw_je_events.txt:117) — lines 117–139; SHA-256 `aa76f4b83dbf2b51d6a59a478f02d79306e4ac77380ecdb19edb51636bfbe90a`

```text
117: 		if = {
118: 			limit = { exists = c:CSA }
119: 			add_journal_entry = {
120: 				type = je_acw_war
121: 				target = c:CSA
122: 			}
123: 			remove_modifier = missouri_compromise
124: 			c:CSA ?= {
125: 				set_variable = acw_slave_nation_var
126: 			}
127: 
128: 			# historical Confederates move to CSA
129: 			every_scope_character = {
130: 				limit = {
131: 					has_variable = historical_csa
132: 					NOR = {
133: 						is_ruler_of_own_country = yes
134: 						is_heir_of_own_country = yes
135: 					}
136: 				}
137: 				transfer_character = c:CSA
138: 			}
139: 		}
```

### Ruler exile host

[sikh_empire.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/sikh_empire.txt:747) — lines 747–771; SHA-256 `d9fcbe766e674662cebf3ee5b0c31498c470adf3f4c6aa848435e3e3a03be65f`

```text
747: 		else_if = { # For sending Duleep Singh to GBR if he happens to be at least 18
748: 			limit = {
749: 				ruler = {
750: 					is_adult = yes
751: 					has_template = pan_duleep_singh
752: 				}
753: 				top_overlord = {
754: 					c:GBR ?= this
755: 				}
756: 			}
757: 			ruler = {
758: 				replace_character_roles = { add = { agitator } remove_all = yes }
759: 				custom_tooltip = {
760: 					text = duleep_goes_to_gbr_tt
761: 					transfer_character = c:GBR
762: 				}
763: 				change_character_religion = rel:protestant
764: 			}
765: 		} # For exiling any other ruler if Sikh Empire becomes a subject
766: 		else = {
767: 			ruler = {
768: 				exile_character_with_role_cleanup = yes
769: 			}
770: 			create_character = {
771: 				ruler = yes
```

### Character transfer engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:37318) — lines 37318–37322; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
37318: ## transfer_character
37319: Transfers current scope character to target country  
37320: transfer_character = country
37321: **Supported Scopes**: character  
37322: **Supported Targets**: country  
```

### Exile engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:9659) — lines 9659–9662; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
9659: ## exile_character
9660: Exile a character to the exile pool  
9661: exile_character = yes
9662: **Supported Scopes**: character  
```

### Investment treaty caller

[00_historical_treaties.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/treaties/00_historical_treaties.txt:60) — lines 60–82; SHA-256 `a1c7e519ef1b07e2491f473ce0f94e6abae718fe725d68bcd8644d2432602f4e`

```text
60: 		create_treaty = {
61: 			name = treaty_name_quadruple_alliance
62: 			first_country = c:GBR
63: 			second_country = c:POR
64: 
65: 			is_draft = no
66: 			entered_into_force_on = 1834.4.22
67: 			binding_period = { years = 10 } # 8 years
68: 
69: 			articles_to_create = {
70: 				{ # Anglo-Portuguese Alliance
71: 					article = defensive_pact
72: 				}
73: 				{ # British Military Assistance to Portugal
74: 					article = military_assistance
75: 					source_country = c:GBR
76: 					target_country = c:POR
77: 				}
78: 				{ # British Economic interests in Portugal
79: 					article = foreign_investment_rights
80: 					source_country = c:POR
81: 					target_country = c:GBR
82: 				}
```

### Investment article

[07_foreign_investment_rights.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/07_foreign_investment_rights.txt:1) — lines 1–39; SHA-256 `d1e4b58b2bdd5bf931e02b65ed89d4c8ef952611eef6558852af8360fdc20bf1`

```text
1: foreign_investment_rights = {
2: 	kind = directed
3: 	cost = 25
4: 
5: 	relations_progress_per_day = 0.5
6: 	relations_improvement_max = 50
7: 
8: 	max_target_involvement = 2000
9: 	target_involvement_applies_to = source_country
10: 
11: 	icon = "gfx/interface/icons/diplomatic_treaties_articles_icons/foreign_investment_agreement_treaties.dds"
12: 
13: 	flags = {
14: 		is_investment_rights
15: 		can_be_enforced
16: 		can_be_renegotiated
17: 		giftable
18: 		friendly
19: 		ai_consider_threaten_naval_hostilities
20: 	}
21: 
22: 	maintenance_paid_by = target_country
23: 	usage_limit = once_per_side
24: 
25: 	unlocked_by_technologies = {
26: 		stock_exchange
27: 	}
28: 
29: 	source_modifier = {
30: 		country_treaty_leverage_generation_add = 300
31: 	}
32: 
33: 	visible = {
34: 		OR = {
35: 			has_dlc_feature = foreign_investment
36: 			has_dlc_feature = mp1_treaties
37: 		}
38: 		is_revolutionary = no
39: 	}
```

### Claim engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:74) — lines 74–78; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
74: ## add_claim
75: Adds scoped state region as a claim for target country  
76: add_claim = scope/country
77: **Supported Scopes**: state_region  
78: **Supported Targets**: country  
```

### Mexico population

[05_north_america.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/pops/05_north_america.txt:2088) — lines 2088–2290; SHA-256 `8f6dc57394211cf493c37e3b7bca141e11aef606053632d704bde2f8ed905884`

```text
2088: 	s:STATE_VERACRUZ = { # 242658 in 1830, 259463 in 1840
2089: 		region_state:MEX = {
2090: 			create_pop = {
2091: 				culture = mexican
2092: 				size = 251061
2093: 			}
2094: 		}
2095: 	}
2096: 	s:STATE_DURANGO = { # est. total of 156999. 153810 in 1830, 160187 in 1840
2097: 		region_state:MEX = {
2098: 			create_pop = {
2099: 				culture = mexican
2100: 				size = 136199
2101: 			}
2102: 			create_pop = {
2103: 				culture = oodham
2104: 				size = 20000
2105: 			}
2106: 			create_pop = {
2107: 				culture = afro_caribeno
2108: 				size = 800
2109: 			}
2110: 		}
2111: 	}
2112: 	s:STATE_SINALOA = { # est. total of 134941. 122285 in 1830, 147596 in 1840
2113: 		region_state:MEX = {
2114: 			create_pop = {
2115: 				culture = mexican
2116: 				size = 113841
2117: 			}
2118: 			create_pop = {
2119: 				culture = oodham
2120: 				size = 20000
2121: 			}
2122: 			create_pop = {
2123: 				culture = afro_caribeno
2124: 				size = 1100
2125: 			}
2126: 		}
2127: 	}
2128: 	# San Luis Potosi:	302390 in 1830, 326559 in 1840, so averaging out to 314475
2129: 	# Guanajuato:		442916 in 1830, 591401 in 1840, so averaging out to 517159
2130: 	# Queretaro:		114437 in 1830, 122962 in 1840, so averaging out to 118699
2131: 	# working total number of 950333
2132: 	s:STATE_BAJIO = {
2133: 		region_state:MEX = {
2134: 			create_pop = {
2135: 				culture = mexican
2136: 				size = 594909
2137: 			}
2138: 			create_pop = {
2139: 				culture = nahua
2140: 				size = 266461
2141: 			}
2142: 			create_pop = {
2143: 				culture = tarascan
2144: 				size = 85162
2145: 			}
2146: 			create_pop = {
2147: 				culture = afro_caribeno
2148: 				size = 3801
2149: 			}
2150: 		}
2151: 	}
2152: 	# Yucatan proper: 	417947 in 1830, 420726 in 1840, so averaging out to 419337
2153: 	# Campeche:			64053 in 1830, 72707 in 1840, so averaging out to 68380
2154: 	# Tabasco:			58518 in 1830, 63919 in 1840, so averaging out to 61219
2155: 	# working total number of 548936
2156: 	s:STATE_YUCATAN = {
2157: 		region_state:MEX = {
2158: 			create_pop = {
2159: 				culture = mexican
2160: 				size = 226764
2161: 			}
2162: 			create_pop = {
2163: 				culture = mayan
2164: 				size = 388804
2165: 			}
2166: 			create_pop = {
2167: 				culture = afro_caribeno
2168: 				size = 1400
2169: 			}
2170: 		}
2171: 	}
2172: 	# Mexico state (incl. Hidalgo): 1050153 in 1830, 1145759 in 1840, so averaging out to 1097956
2173: 	# Puebla: 610950 in 1830, 661524 in 1840, so averaging out to 636237
2174: 	# Tlaxcala: 72271 in 1830, 81524 in 1840, so averaging out to 76897
2175: 	# working total number of 1811090
2176: 	s:STATE_MEXICO = {
2177: 		region_state:MEX = {
2178: 			create_pop = {
2179: 				culture = mexican
2180: 				size = 763486
2181: 			}
2182: 			create_pop = {
2183: 				culture = mixtec
2184: 				religion = catholic
2185: 				size = 39996
2186: 			}
2187: 			create_pop = {
2188: 				culture = nahua
2189: 				size = 689604
2190: 			}
2191: 			create_pop = {
2192: 				culture = zapotec
2193: 				size = 264004
2194: 			}
2195: 			create_pop = {
2196: 				culture = afro_caribeno
2197: 				size = 54000
2198: 			}
2199: 		}
2200: 	}
2201: 
2202: 	# total of 231319. This number was revealed to me in a dream.
2203: 	# jk. Couldn't find estimates for Guerrero in 1830 or 1840, but they could be found for 1870 onwards, so some math trickery was done. Neighboring Oaxaca's estimated 1835 population is 74.7% of its 1870 population, and 50.61% of its 1900 population, so those percentages were applied to Guerrero's 1870 and 1900 population figures, and the two results were averaged together into the above.
2204: 	s:STATE_GUERRERO = {
2205: 		region_state:MEX = {
2206: 			create_pop = {
2207: 				culture = mexican
2208: 				size = 114874
2209: 			}
2210: 			create_pop = {
2211: 				culture = zapotec
2212: 				size = 13183
2213: 			}
2214: 			create_pop = {
2215: 				culture = tarascan
2216: 				size = 60846
2217: 			}
2218: 			create_pop = {
2219: 				culture = nahua
2220: 				size = 27381
2221: 			}
2222: 			create_pop = {
2223: 				culture = afro_caribeno
2224: 				size = 15036
2225: 			}
2226: 		}
2227: 	}
2228: 	s:STATE_OAXACA = { # approx 479674. 457504 in 1830, 501844 in 1840.
2229: 		region_state:MEX = {
2230: 			create_pop = {
2231: 				culture = mexican
2232: 				size = 143903
2233: 			}
2234: 			create_pop = {
2235: 				culture = zapotec
2236: 				size = 40532
2237: 			}
2238: 			create_pop = {
2239: 				culture = tarascan
2240: 				size = 187073
2241: 			}
2242: 			create_pop = {
2243: 				culture = nahua
2244: 				size = 84182
2245: 			}
2246: 			create_pop = {
2247: 				culture = afro_caribeno
2248: 				size = 23984
2249: 			}
2250: 		}
2251: 	}
2252: 	# Jalisco: 656881 in 1830, 691397 in 1840, so averaging out to 674139
2253: 	# Michoacan: 435281 in 1830, 497537 in 1840, so averaging out to 466409
2254: 	# Colima: 45838 in 1830, 53389 in 1840, so averaging out to 49614
2255: 	# working total of 1190162
2256: 	# 1.5858
2257: 	s:STATE_JALISCO = {
2258: 		region_state:MEX = {
2259: 			create_pop = {
2260: 				culture = mexican
2261: 				size = 1011710
2262: 			}
2263: 			create_pop = {
2264: 				culture = oodham
2265: 				religion = catholic
2266: 				size = 152078
2267: 			}
2268: 			create_pop = {
2269: 				culture = oodham
2270: 				size = 26373
2271: 			}
2272: 		}
2273: 	}
2274: 	# Zacatecas: 222918 in 1830, 274380 in 1840, so averaging out to 248649
2275: 	# Aguascalientes: 57125 in 1830, 72193, so averaging out to 64659
2276: 	# working total of 313308
2277: 	s:STATE_ZACATECAS = {
2278: 		region_state:MEX = {
2279: 			create_pop = {
2280: 				culture = mexican
2281: 				size = 137347
2282: 			}
2283: 			create_pop = {
2284: 				culture = nahua
2285: 				size = 175961
2286: 			}
2287: 		}
2288: 	}
2289: 	# 121424 in 1830, 138595 in 1840
2290: 	# working total of 130010
```

### Andes population

[07_south_america.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/pops/07_south_america.txt:374) — lines 374–478; SHA-256 `f6a8f324ec4948913a817a2b0e9ea686405963935a93bdd405bdbb5d9dc572fe`

```text
374: 	s:STATE_CAJAMARCA = {
375: 		region_state:NPU = {
376: 			create_pop = {
377: 				culture = south_andean
378: 				size = 91804
379: 			}
380: 			create_pop = {
381: 				culture = afro_caribeno
382: 				size = 12000
383: 			}
384: 			create_pop = {
385: 				pop_type = slaves
386: 				culture = afro_caribeno
387: 				size = 4000
388: 			}
389: 			create_pop = {
390: 				culture = amazonian
391: 				size = 12000
392: 			}
393: 			create_pop = {
394: 				culture = quechua
395: 				size = 186696
396: 			}
397: 		}
398: 	}
399: 	s:STATE_LIMA = {
400: 		region_state:NPU = {
401: 			create_pop = {
402: 				culture = south_andean
403: 				size = 248000
404: 			}
405: 			create_pop = {
406: 				culture = quechua
407: 				size = 212000
408: 			}
409: 			create_pop = {
410: 				culture = afro_caribeno
411: 				size = 21900
412: 			}
413: 			create_pop = {
414: 				pop_type = slaves
415: 				culture = afro_caribeno
416: 				size = 6200
417: 			}
418: 			create_pop = {
419: 				culture = amazonian
420: 				size = 16000
421: 			}
422: 		}
423: 	}
424: 	s:STATE_ICA = {
425: 		region_state:SPU = {
426: 			create_pop = {
427: 				culture = south_andean
428: 				size = 92904
429: 			}
430: 			create_pop = {
431: 				culture = afro_caribeno
432: 				size = 3350
433: 			}
434: 			create_pop = {
435: 				pop_type = slaves
436: 				culture = afro_caribeno
437: 				size = 650
438: 			}
439: 			create_pop = {
440: 				culture = quechua
441: 				size = 242804
442: 			}
443: 			create_pop = {
444: 				culture = amazonian
445: 				size = 12000
446: 			}
447: 		}
448: 		region_state:IQU = {
449: 			create_pop = {
450: 				culture = quechua
451: 				size = 55000
452: 			}
453: 		}
454: 	}
455: 	s:STATE_AREQUIPA = {
456: 		region_state:SPU = {
457: 			create_pop = {
458: 				culture = south_andean
459: 				size = 48000
460: 			}
461: 			create_pop = {
462: 				culture = aimara
463: 				size = 80400
464: 			}
465: 			create_pop = {
466: 				culture = quechua
467: 				size = 146500
468: 			}
469: 			create_pop = {
470: 				culture = afro_caribeno
471: 				size = 2000
472: 			}
473: 			create_pop = {
474: 				pop_type = slaves
475: 				culture = afro_caribeno
476: 				size = 500
477: 			}
478: 		}
```

### Andes actual state owners

[00_states.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:2363) — lines 2363–2413; SHA-256 `a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`

```text
2363: 	s:STATE_PASTAZA = {
2364: 		create_state = {
2365: 			country = c:NPU
2366: 			owned_provinces = { x6B0A5B x3C0D20 xF479D2 xD61646 x737C7E x51F069 xA54AD4 xB16F01 x411597 x3E32E2 xF73F96 xF86ADF x3799DE xA5ACFD x8C41E2 x096D46 x6D7047 x4F0E85 x299588 xFD33D9 xB47529 xD0BAEC }
2367: 		}
2368: 		create_state = {
2369: 			country = c:ECU
2370: 			owned_provinces = { x804050 x439628 x6675F2 x0EA863 x9110AC x8A1A0D x2521E8 x01CA2C xEB5ADD xD18F33 xD21383 xA29A00 x9FEB80 x7AC512 x8080D0 x63ED6E x6B096B x8FE675 x60DC96 x3DBF3C x598DEB x248E5D xFB499C xE043D2 xE85DC6 x667AE7 xE05359 xB7C18D xFD054C xDF9283 x917883 x7FE0D2 xC5B9B8 xD37CBF x877BF7 x9B0B43 x27EF71 x38C3BD x9EAA88 x8CD643 xA28606 x97F39F xC778AE x0080D0 x272E8C xDCA8CF xCF5C7B xF2735E x6DCE38 x7E3539 xD0D212 }
2371: 		}
2372: 		add_homeland = cu:amazonian
2373: 	}
2374: 	s:STATE_CAJAMARCA = {
2375: 		create_state = {
2376: 			country = c:NPU
2377: 			owned_provinces = { x5ED420 xA33231 xE8C4B9 x49AE7D xA6A663 x069581 x53C9A1 xDC3D44 x6EDBA1 x215FF5 xD57EEE x54BF7F xC000D0 x1D15F7 xD12A1F xE709F8 x4CD5E4 x2A7F60 x3EA1E4 x4080D0 x08FB24 xF91A3D x66279A x2E0608 x5C955D xC8294A x8170A2 x769175 xB26C25 x1FAA35 x8D62E6 x2ACF46 xAD65A3 xEF024D }
2378: 		}
2379: 
2380: 		add_homeland = cu:south_andean
2381: 		add_homeland = cu:quechua
2382: 	}
2383: 	s:STATE_LIMA = {
2384: 		create_state = {
2385: 			country = c:NPU
2386: 			owned_provinces = { x03B9CB x05FB9B x0B1EE1 x131D6D x187234 x20C0B0 x25CF2A x26F77F x2AFF79 x2B7493 x3060D7 x32863F x3528D6 x4411B8 x48284E x539023 x59E553 x5E4494 x60C030 x631487 x64989F x690D59 x6BEF27 x6EB212 x786D2C x7C29E5 x7C6BF6 x88CDF0 x91B0BF x928ED8 x96560E x9866F2 x99E70D x9BBC5E x9E0F14 xA03573 xA06991 xA0C0B0 xA146DE xA3F17B xA4735B xC0A53C xC2FE32 xC64601 xC9CBD8 xCBB91A xCD4EF2 xCF5BB8 xD3F539 xD7B13A xDEA3E2 xE69BC9 xF19D07 xF2A18E xF3F25C xF405A2 }
2387: 		}
2388: 
2389: 		add_homeland = cu:south_andean
2390: 		add_homeland = cu:quechua
2391: 	}
2392: 	s:STATE_ICA = {
2393: 		create_state = {
2394: 			country = c:SPU
2395: 			owned_provinces = { x08AC16 x08BBBC x0AF425 x186AEE x199608 x1CA561 x1F2F47 x38EE47 x3B8AB8 x3F9FD5 x40E12A x43494D x44B4A5 x6040B0 x6780B3 x728391 x7B9FBE x7DD2F8 x807F09 x817BB5 x82F15A x83E894 x98E058 xA4CA0B xA4DAF3 xB0BAC0 xB15AC4 xB2AB53 xB3DC65 xBDFBD1 xC6E532 xD464CF xD54205 xDF4030 xE5E702 xE7EB9B xF0A4FE xF211E2  xF3A702  xFF8828 }
2396: 		}
2397: 		create_state = {
2398: 			country = c:IQU
2399: 			owned_provinces = { xF333CF x7991EE xA101CC x32FF31 x52BF37 xDF00B0 x3C568C xCAB5E1 x4061BE xA7C0A9 x0D8A39 x5F849A x003582 x68D883 x08623F xDFC030 xFB1969 }
2400: 		}
2401: 
2402: 		add_homeland = cu:south_andean
2403: 		add_homeland = cu:quechua
2404: 	}
2405: 	s:STATE_AREQUIPA = {
2406: 		create_state = {
2407: 			country = c:SPU
2408: 			owned_provinces = { x007035 x2E3791 x3BC37F x451783 x67EC55 x72698B x79A3B0 x7C1054 x89775D x8EC087 x923040 x96798E x96AB5D xB077B0 xBB02B0 xBED190 xC16B62 xC72B01 xD619E0 xD66487 xDF23D0 xDFC0B0 xE326BA xF6869A }
2409: 		}
2410: 
2411: 		add_homeland = cu:south_andean
2412: 		add_homeland = cu:quechua
2413: 		add_homeland = cu:aimara
```

### PPET America chronology

[北明ppet.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:171) — lines 171–226; SHA-256 `227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`

```text
171: [slide 18 p8] 1524，阿兹特克覆灭，西班牙帝国逐渐形成，末代阿兹特克领袖夸乌特莫克逃亡吴国领地，吴国奏请北明朝廷加封夸乌特莫克“宋王”；
172: [slide 18 p9] 1590年代，吴将公子术攻灭西班牙墨西哥总督府，结束了欧洲殖民者在中美洲的霸权；
173: [slide 18 p10] 1620，五月花号抵达美洲；
174: [slide 18 p11] 东洲第一共和国（1620-1918）
175: [slide 18 p12] 约1620-28，女真奴隶努尔哈赤、皑雪地主孙承宗发起第一次东洲独立战争，吴首辅左光斗平灭之；
176: [slide 18 p13] 1621，努尔哈赤改革皑雪女真、蒙古奴隶的部族制度，建立以义军军官为核心的八旗制度；
177: [slide 18 p14] 1628-44，爱新觉罗·喝竿（别名黄台吉）、毛文龙等人继续领导义军，终于在1644年赢得独立战争的胜利，；
178: [slide 18 p15] 1645，东洲正式确立以皑雪坞堡主、士绅、八旗军头为领袖的共和政治，议员称“国公”，元首称“大执政”，国号“大夏”；
179: [slide 18 p16] 1647-1690，皑雪军进攻吴属长岸，史称第三次东洲独立战争，霖、洛、樊、攸四州并入大夏；
180: [slide 18 p17] 1701-1712，紧随着“银票危机”和吴王宣布朝廷破产，吴属长岸、大原爆发起义，史称第四次东洲独立战争；
181: [slide 18 p18] 1712，长岸、大原、阳州（墨西哥西北部高原与下加利福尼亚）并入大夏国，改国号为“华夏东洲共和国”，宋王（阿兹特克君主）后裔复国，建立阿兹特克-蒙特苏马王朝，向吴国朝贡；
182: [slide 18 p19] 1713，迁都长岸新郑城，改名金邑，又称作“金都”；
183: [slide 18 p20] 1720-1890，东洲东进运动，西海岸的石油开发使东洲资本迅速膨胀；
184: [slide 18 p21] 1763-1792，第一次北美洲战争，华夏东洲扶持印第安部落和美洲蒙古大宁部、东科尔沁部对抗英国殖民者和后来成立的美利坚合众国；
185: [slide 18 p22] 1805-1809，第二次北美洲战争与游牧民大起义，东洲、中部殷人联盟对抗美利坚合众国，起义后由印第安、蒙古牧民组成的大原可汗国被东洲、美国联合剿灭；
186: [slide 18 p23] 1811-1815，东洲介入墨西哥革命，扶持墨西哥第一共和国；
187: [slide 18 p24] 1861-1867，由于东洲介入美国南北战争（1861-64），第三次北美洲战争爆发，又称“北美石油战争”，双方最终绝定以中部的奥马哈为“永久边界”，签订“奥马哈条约”；
188: [slide 18 p25] 1890-1912，东洲资本家资助大吴的民族解放运动；
189: [slide 18 p26] 1913-1918，东洲于1913年宣布介入辛亥革命和亚洲民族解放战争，向大吴宣战；并在1915年宣布响应法国号召对反法同盟宣战；
190: [slide 18 p27] 1917-18年，法国战败，西南国民政府与大吴停战，1918年7月，大吴主力舰队炮击东洲金邑城，东洲元帅府宣布战败；
191: [slide 18 p28] 1919年元月，随着杭州条约签署，东洲与美利坚合众国正式合并为华夏美利坚合众国，华夏东洲第一共和国灭亡；
192: [slide 18 p30] 总背景介绍与设计思路
193: [slide 19 p1] 总背景介绍与设计思路
194: [slide 19 p2] 南美洲初步设定——
195: [slide 19 p3] 前现代历史
196: [slide 19 p4] ~1.1万年前，印加人抵达安第斯山脉；
197: [slide 19 p5] 约十三世纪，安第斯山脉之间的城邦繁荣起来；
198: [slide 19 p6] 印加帝国（古代-1936）
199: [slide 19 p7] 1430年代，库斯科国崛起，一统安第斯山脉，建立“四方之地”，史称印加第一帝国；
200: [slide 19 p8] 1490年代，天花与鼠疫等流行病抵达南美洲，第一帝国陷入第一次内战
201: [slide 19 p9] 幸存的印加人通过印加古文明的公社制度组织动员，从多次瘟疫中幸存下来；
202: [slide 19 p10] 1523-1527，福建航海家林驹容的船队越过阿兹特克抵达南美，发现印加人；
203: [slide 19 p11] 1526-1533，西班牙冒险家皮萨罗攻入库斯科，劫持印加皇帝，希望能藉此控制分裂的印加人；
204: [slide 19 p12] 1534，大明（吴国）东洋水师抵达印加，印加北方（明人称谓）都指挥使、藩王曼科·印卡利用吴国与西班牙在中美洲的矛盾驱逐皮萨罗，以北方为基业建立印加第二帝国；
205: [slide 19 p13] 1536-1602，印加第二帝国时期，印加人与中国、西班牙、葡萄牙人进行贸易，进口铁器和牲畜，技术和社会制度有了长足的进步，但社会矛盾也因此加剧；
206: [slide 19 p14] 1550-1600年代，基督教从巴西、哥伦比亚的欧洲殖民地传来，在印加社会中新崛起的自耕农阶层中广泛传播；
207: [slide 19 p15] 1602，北方基督教农民起义攻占首都基多，击败印加官军，印加第二帝国陷入分裂；
208: [slide 19 p16] 1602-1653，第二次内战时期；
209: [slide 19 p17] 1653，印加军阀库亚喀·印卡统一全国，建立印加第三帝国，定都库斯科，接受北明册封；
210: [slide 19 p18] 1653-1865，印加第三帝国时期，帝国上层接纳儒教；
211: [slide 19 p19] 1811，尤潘基·阿马鲁一世登基，开始在国内进行一系列近代化改革；
212: [slide 19 p20] 1808-1833，南美洲独立运动；
213: [slide 19 p21] 1817-1818，在明、法、英、美等国的怂恿下，尤潘基·阿马鲁伺机入侵西属哥伦比亚，但被玻利瓦尔率领的起义军击败，尽管立场不同，但佩德罗一世统治下的巴西也出兵支援了玻利瓦尔以遏制印加人；
214: [slide 19 p22] 1817，起义领袖何塞·德·圣马丁率领拉普拉塔军发动“瀚海远征”，翻过安第斯山脉占领西属智利，智利殖民者战败后因为惧怕印卡人南下而选择并入拉普拉塔；
215: [slide 19 p23] 1830-1833，印卡-哥伦比亚战争，玻利维尔去世后，大哥伦比亚陷入内斗，尤潘基·阿马鲁再次入侵哥伦比亚，巴西由于皇帝新丧未能介入，大哥伦比亚最终战败，被迫退守委内瑞拉；
216: [slide 19 p24] 1836-1839，第一次印卡-拉普拉塔战争，印加战败，尤潘基·阿马鲁一世去世；
217: [slide 19 p25] 1850年代，大吴代明而立，清洗保明派，大量前朝士绅流亡美洲；
218: [slide 19 p26] 1852-1855，拉普拉塔内战爆发，第二次印卡-拉普拉塔战争，拉普拉塔割让所属智利地区；
219: [slide 19 p27] 1860-1863，大吴极东银行矿业证券危机爆发，印加皇室作为主要客户陷入动荡，拉普拉塔趁势发动第三次印卡-拉普拉塔战争，夺回智利海岸线；
220: [slide 19 p28] 1864-1865，印加爆发共和派起义并攻占首都库斯科，第三帝国灭亡；
221: [slide 19 p29] 1865-1892，印加共和国时期，共和党与激进党轮流执政，改革报禁和历史研究，共产主义在印加传播；
222: [slide 19 p30] 1870，印加社会民主工人党成立，领袖利马·阿图罗发表《印卡公社与我们的历史》，将印加古代的公社制度与印加未来的社会主义制度联系起来；
223: [slide 19 p31] 1874-1883，第四次印卡-拉普拉塔战争，又称“硝石战争”，印加战胜，强迫智利从拉普拉塔独立；
224: [slide 19 p32] 1892，共和国银行改革案遭遇失败，在大吴帝国的干涉下，印加第三帝国皇室复辟，史称印加第四帝国；
225: [slide 19 p33] 1893，北方首府基多爆发工人起义，建立“基多公社”，起义持续五个月后失败；
226: [slide 19 p34] 1892-1936，印加第四帝国时期，经济持续由传统的矿业、农业支撑，境内资本大多由大吴、英国、美国和东洲资本家支配，最近统一的华美资本家开始了更大规模的投资；
```

### PPET European chronology

[北明ppet.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:311) — lines 311–313; SHA-256 `227a043951fa72e927915a52c03a60957baf29668d4e4e18414e69e28c822c37`

```text
311: [slide 22 p32] 1756-1763，七年战争，阿兹特克-蒙特苏马王朝（中方称为“大商”）站在英国-普鲁士一方加入战争，战后扩张至密西西比河流域，而华夏东洲则渗入了法国的魁北克殖民地；
312: [slide 22 p33] 1764，仍是学者的托马斯·杰斐逊造访东洲；
313: [slide 22 p34] 1775-1783，美国独立战争，在法国的怂恿下，阿兹特克帝国支持美国独立；
```

### Biography colonization

[北明人物列传.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明人物列传.txt:275) — lines 275–296; SHA-256 `43381417ce9343438a86f0c37f1e1f73a3f51ed3bffa8a911d77fdf1aaf04256`

```text
275: [word/document.xml p456] 1590年，在公子术的指挥下，吴国东洋水师及其陆军友军、雇佣军、女真兵袭击并攻陷了佛朗机人在金林的最后一处据点——墨西哥。结束了佛朗机人对新大陆持续近70余年的殖民霸权，并以吴国的殖民霸权取而代之。同年，吴国长岸总督府的首府——江子港（今旧金山）及其周围直接管辖的田地与农村突破了六万人口，并被改名为“祁州”，以继续纪念公子祁为吴国和中华文明做出的贡献。
276: [word/document.xml p457] 1592年，公子术参与了由北洋水师都督叶世班与丰臣氏联军发动的壬辰朝鲜战争。虽然朝鲜一方已经大量引进了来自中原的先进火器，同时大量任用来自齐国、唐国、晋国的中原旅朝军官，又有其中原盟友齐国、闽国的直接干预，甚至包括北明皇帝本人的支持，这次战争仍以朝鲜割让汉城以南所有领土、迁都平壤、臣事吴、日为结局。在这场战争中的重要战役——鸣梁海战与露梁海战中，吴国两洋水师、日本水师虽然遭受了当地朝鲜水师与齐国水师的夹击，最终仍全歼敌军，获得了完全的胜利。
277: [word/document.xml p458] 此后，公子术继续指挥在极东洲的殖民事务，并且将金林、皑雪发掘的大量金银运回吴国，一度大大好转了吴国为了维持内外霸权而恶化的经济。
278: [word/document.xml p459] 1599年，公子术因心脏病逝于皑雪史氏港（科迪亚克岛南部）。
279: [word/document.xml p460] 陈泷（字康范）（1539-1592）：“英宗遗臣”、吴国东洋总领事府代领事、南洋舰队总司长，北明时期著名水师将领。从他的人生中来看，陈泷无疑是一个天才。他以闽国政治逃犯的身份来到吴国。并在郑象的集权改革中，作为前者坚定的支持者而称道，但他所作的并不仅限于此。在郑象调配的资金支持下，与公子术在日本、极东的成就相似，陈泷与越国盟友合作，对内封锁宿敌闽国沿海，进一步压缩对方的战略空间，对外控扼南海，让原本只是偏师的南洋舰队成为足以压服该地区传统强国的越国与大越南国。
280: [word/document.xml p461] 1576年，陈泷在郑象的默许下自作主张，与盟友越国反目，不仅将越国威震海内的“正、中、后”三大舰队全歼，还将南洋舰队开至广州城下，正对越国海关口岸连续齐射空炮三响。此后，由于再无与吴国抗衡的海上力量，越国虽然在南洋的群岛上遍布堡垒、关口，也无能与之作战，只得称臣议和，就连位于马六甲海峡的重要基地——“李氏岛”也被夺取，修筑港城“郑家坡”。
281: [word/document.xml p462] 除了军事与外务上成绩斐然之外，陈泷在政治上也极受国君郑象信任。在郑象晚年的宫廷倾轧中，陈泷十分可靠地置身事外，并最终作为“立庶派”的首脑正确地推举了下任国君。使得吴国得以避免诸子争权的内乱。但也正因为他的这项举动，郑象诸公子的余党在失势后铤而走险，在一次水师操演中将陈泷刺杀。
282: [word/document.xml p464] 米安稷（字明津）（1540-1601）：吴国首辅（1582-1591）、英公遗臣（见后文）。黄正茗之后，郑象独断之欲更炽，奏疏、战事“不批于宫，便议于营” （指吴国水陆两军枢密院，将军枢密院【陆官府】、水军枢密院【官船营】），“几无文臣之事，六部如一文书阁，诸侍郎唯垂手润色、抬头领命而已”。因此，吴国官场一片风声鹤唳，“几无任事之臣，亦无任事之需”。有抱负、有野心的士人无不避吴国而去。就连号称“新儒诸院文章魁首”的东林书院，也落了个门可罗雀的下场。在此期间，“装点门面”的首辅，便是米氏。不过或许也正因如此，米安稷虽在政治上无赫赫之功，却同前辈黄九星一样是当时的书法名家。在郑象去世后，米氏作为“文臣首脑”即时在政治上支持“立庶”，使得吴国日益膨胀的权力能够正常交接。
283: [word/document.xml p466] 郑钟声（1548-1602）：吴王，第六代吴国君，吴英公郑象庶出子，1591年秋即位。其母为郑象众嫔妃中一人，因为失宠后被迫害而逃出宫内，被其外镇南洋的叔父庇护，郑钟声因此长于吕宋，直到被推举为储君前一直藏身吴国在吕宋的一处军镇中。
284: [word/document.xml p467] 在郑象晚年，愈加风声鹤唳的政治气氛带来了血腥的后宫倾轧。郑象的大公子在一次出海巡航后死于可疑的“伤寒”。其余几位有能力继位的公子也因为各种各样的原因，不是事败身死，就是因为太过残忍而被郑象君臣忌惮。因此郑象在弥留之际也未能立储，只得以遗诏的形式将这个任务传给几位名望隆重的文臣武将。
285: [word/document.xml p468] 这些文臣武将，便在历史上被称为“英宗遗臣”。更具体一些，指的是郑象晚年处于权力中心的一大批人。
286: [word/document.xml p469] 而在郑象逝世后，吴国宫廷内以外戚范氏、遗臣之一公子术为首的“公子派”要求从众公子中选拔一人，遗臣中的大将陈泷、首辅米明津等人却竭力反对之，并推举一直藏身军中的郑钟声继位,是为“立庶派”。双方的争执史称“吴国公庶之争”。最终，在濒临内战时，公子派的首脑公子术选择忠于水师与郑象遗诏，倒向陈泷。郑钟声于是登得大宝。
287: [word/document.xml p470] 在他执政期间，郑钟声不仅贯彻了郑象的集权改革，还同东林书院学政（校长）顾东行联盟，重新恢复了一些文臣的权力。这主要是因为新兴起的“法治”与“国人”概念改变了东方的内政结构，驱使着郑钟声设立了主要司职税法、商法及其他法律修订的“中堂内阁”。依靠这一法律机构，郑钟声与吴国政府得以对吴国的经济进行细节调控，并依靠国家影响力垄断华南贸易。在郑钟声朝极盛时，华南贸易几乎一体，所有商贩都要在金陵设置鸽驿传书以便第一时间了解吴国的关税变化。
288: [word/document.xml p471] 政治条例的法律化、标准化，使得吴国政府建立起极大的威信。在此之前，诸侯之间虽然早有私铸钱币泛滥，但直到吴国建立起稳固而不可动摇的税法体制，北明皇室才在“礼议会”（吴国主导）的胁迫下，被迫交出正式的“铸币权”，并“令”吴国称王以示“天子威仪唯王是亲”。
289: [word/document.xml p472] 然而，郑钟声晚年，吴国的政坛出现新一轮动荡。以对海外殖民地、日本大阪幕府的态度为导火索，主导水师的“海事派”与主导政治的“商派”、“东林派”士大夫开始党争倾轧。使得原本稳固的吴国法律体系发生动摇。不仅直接影响了吴国财政，也离间了原本开始朝向吴国的华南诸侯。尤其是此前被迫支持吴国霸业的越国和闽国。
290: [word/document.xml p474] 顾东行（字远国）（1550-1612）：东林书院学政、吴国太学大祭酒、吴国中堂首辅（1592-1608），人称“东林先生”。作为郑象晚年异军突起的政治强人，顾东行起初并非吴英公（郑象）近臣，而是作为反对吴国集权的清流派新人，在东林书院讲学。有他青年时期云游四海的经历为辅，顾东行在经学、道学、新儒物理学等方面一时无两，他的大课也常常人满为患，与在郑象统治后期不断衰弱的东林格格不入。因此，顾氏竟在黄九星去世后被推举为东林书院私学学政。意识到自己所行的政治之弊端的吴英公也在后来破格提拔顾东行，将其从一白身提拔为太学祭酒，欲稍稍挽回士大夫之心。结果顾东行在祭酒位置上展现出了超越职权的能力，不但在三四年之间复兴了吴国太学，还拉拢了缪昌期、陈幼学等贤士能臣进入吴廷，于是郑象在弥留之际遗诏顾氏为新朝辅政大臣之一。顾氏因此得以参与“庶长之争”，并以其“公子派”遗臣的身份竭力抗争。
291: [word/document.xml p475] 而在郑钟声即位后，原本属于公子派的顾东行原本以为自己要被罢官或流放，已经提前将行李准备好，再应诏前去面见新君，却得知自己因为“立庶派”之首陈泷、米明津的保荐得以留任。不过，顾东行却没有因此满意，反而在得知现任首辅米氏即将告老时求首辅之位，并自比魏征。因为顾东行所言条理清晰、逻辑俨然，郑钟声遂应其所请。后来，顾东行才得知，英公遗诏上早有任其为首辅的条陈。
292: [word/document.xml p476] 在任首辅期间，顾东行用“众人天下”的学说规劝和辅佐郑钟声，并开启了法律的规范化，禁止从前过分依赖人情故事、政治规则的刑律，并建立了著名的“中堂内阁”。在他执政期间，任人不遗、任事不废，使得法规、政策都能有始有终，从没有治政偏废或中途修改的。史家则说，顾东行执政时，吴国首辅开始制订、管理法律，虽然对政治评论、言官问事都制定了审查规则，但也用法规制止集权因为政治斗争肆意钳制言论，结束了御史言官时不时能“风闻奏事”的时代。在税法上，顾东行学习了前燕国相张居正的改革，在吴国削减土地和人头税，增设收入税、商税和货税，正式开始区分国内商品和外贸输入品，设立并控制“关税”，同时废除了许多苛捐杂税，并开始推行银本位的纸币。不过相较于张氏，顾氏的税法更宽松，但涉及的商品很多，调整也很频繁。这是吴国发达的海贸促进了商品经济和大宗货物交易的结果。
293: [word/document.xml p478] 黎笋（字昌奇）（1559-1632）：吴国中堂首辅、著名经济学家、金融先驱。黎氏生于金陵，父亲是旅居吴国的交趾客商，但很早就去世了。童年时他受过一定的私塾教育，恰逢“报刊”的出现和活字轧墨印刷普及，黎笋便成为了世界上第一批报童之一。
294: [word/document.xml p479] 然而，他的志向却不在文字出版，而在权力和金钱。因此他借助自己能够率先读到报刊的便利，学习知识、寻找消息。终于在20岁时成为了一个山西商行在华南的向导，很快他便晋升为这个商行的管事，继而踏上了陶朱公的道路。
295: [word/document.xml p480] 此后数十年间，黎笋表现出了自己对信息超乎常人的敏锐和理解力。此时恰逢吴英宗（郑象）缔造的繁荣扩张时代。黎笋接触并参与了许多这一时期吴国民间对日本、朝鲜、广东、交趾及其他内外地区的商业扩张。在这一过程中，他逐渐从单纯的商人，成长为一个心机缜密、关系遍布的“斡旋家”。或者说，民间的“纵横家”。
296: [word/document.xml p481] 在野时的黎笋依靠其影响力，大力推动和支持吴国的海外扩张。他与同时期越国的张化臣一起被认为是东方殖民历史上的不朽传奇。在他的支持和引导下，吴国在北极东洲（北美）建立了庞大的大原（加利福尼亚与大平原）行都司、金林行都司与苔原（秘鲁）行都司。为吴国未来的寰球殖民帝国的开端。
```

### Biography independence

[北明人物列传.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明人物列传.txt:312) — lines 312–314; SHA-256 `43381417ce9343438a86f0c37f1e1f73a3f51ed3bffa8a911d77fdf1aaf04256`

```text
312: [word/document.xml p500] 与此同时，1620年，由于吴国财政的一系列问题，著名的“极东洲革命”爆发。当地女真奴隶首领努尔哈赤、汉人士绅孙承宗等汉、女真、蒙三民族士绅、头领四十八人签署发布了《东洲独立檄文》。细数吴王、燕明等中原封建君主七大罪状，并宣告了世界上第一个近代共和国家的建立。吴国旋即开始对革命军进行清剿，一度几乎将起义扑灭。但最终还是在郑摧死后的1644年，由于内部急转直下的政治局势承认了东洲独立。
313: [word/document.xml p501] 虽然如此，郑摧时代的吴国并不是一个衰弱的国家。在海外的温和政策导致吴国军人频繁在北明境内挑动冲突。先后进军并控制了宁、梁、闽等国政。吴国首辅左光斗在东林党的支持下，于这些邦国恢复国相制度，架空本地王公，试图建立一个以金陵为中心、地跨东南半壁的集权帝国。
314: [word/document.xml p502] 同时，他在后宫的一些履历也使他“子孙满堂”，直接导致了他于1644年因巡游墨西哥而罹患热病去世后，吴国宫廷爆发了第二次“公庶之争”。
```

### Population envelope method

[population_envelope_audit.py](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/population_envelope_audit.py:1) — lines 1–17; SHA-256 `721c2f7d1856c313dd51a56c078d5bcce6e45cf7847be00f490e9bc25dd02586`

```text
1: """Read-only population envelope audit against the ORIGINAL mod, never the last candidate.
2: 
3: The fixed reference combines pre-update-20261030T233944Z with the frozen vanilla
4: 1.13.11 / 24799966 source snapshot. Current vanilla is a separate comparison.
5: New regions are mapped by province membership to their original parent region.
6: Cross-parent regions require an explicit per-history-pop geographic ledger;
7: missing provinces and a zero-to-positive baseline still require review.
8: The tool never silently chooses the largest overlap.
9: """
10: from pathlib import Path
11: from collections import Counter, defaultdict
12: from datetime import datetime, timezone
13: import argparse
14: import hashlib
15: import json
16: import sys
17: 
```

### Custom culture modifier declarations

[ce_culture_modifier_types.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/modifier_type_definitions/ce_culture_modifier_types.txt:1) — lines 1–30; SHA-256 `f793165a2a331f71d76ab6bc71826387ceab1294442893f9f5b29a7e10e2c47a`

```text
1: state_ce_zhonghua_standard_of_living_add = {
2: 	decimals = 1
3: 	color = good
4: 	game_data = {
5: 		ai_value = 0
6: 	}
7: }
8: 
9: country_ce_zhonghua_cultural_acceptance_add = {
10: 	decimals = 1
11: 	color = good
12: 	game_data = {
13: 		ai_value = 0
14: 	}
15: }
16: 
17: state_ce_liaodong_standard_of_living_add = {
18: 	decimals = 1
19: 	color = good
20: 	game_data = {
21: 		ai_value = 0
22: 	}
23: }
24: 
25: country_ce_liaodong_cultural_acceptance_add = {
26: 	decimals = 1
27: 	color = good
28: 	game_data = {
29: 		ai_value = 0
30: 	}
```
