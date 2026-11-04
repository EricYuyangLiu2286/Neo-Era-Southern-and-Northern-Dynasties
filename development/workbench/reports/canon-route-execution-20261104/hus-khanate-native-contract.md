# HUS khanate and registration-law native contract

2026-11-04. Read-only research. Current game1.13.11/build24799966. No MOD edit, no game launch. This supplements `americas-acceptance-native.md` and supersedes its generic warning that only entire-pop movement was available: **the exact native effect is `move_partial_pop`**. Initial quick search missed the name; the complete effects index and actual Japan/ACW/Red Scare callers resolve it.

## 1. Exact migration API and invariants

`move_partial_pop` is a pop-scope engine effect with `state = <owned state scope>` and either `population_ratio = 0.5` or `population = <number/script value>`. `move_pop` moves the entire scoped pop. `create_mass_migration` only starts a culture migration to the scoped state from an origin country; it has no headcount/ratio and is unsuitable for an exact50% or70:30 scripted exodus.

Japan's Hokkaido event scopes the source state, iterates every Japanese pop, and applies `population_ratio = 0.015` into the destination state. Red Scare explicitly moves10% of a saved pop. ACW supplies a script-value population bound. Therefore a source-country loop can filter `culture = { has_discrimination_trait_group = heritage_group_indigenous_american }` and migrate50% of every matching pop to a valid Khanate-owned destination. This is population movement, not kill/create reconstruction. Keep culture, religion, wealth and literacy untouched by script; do not create replacement pops or use kill_population. The documented side effect is unemployment, and pop type may change when that type cannot be unemployed or when a slave moves to a state that disallows slavery. Existing populations may merge; exact original pop IDs and individual wealth buckets are not promised. Engine verification must compare same-tick national/world totals and culture/religion aggregates, and inspect weighted wealth/literacy rather than interpreting changed group IDs as loss.

For a70/30 split of ALL HUS Manchu/Mongol population: on each ORIGINAL HUS pop, first `move_partial_pop = { state = <CNE destination> population_ratio = 0.7 }`, then move the surviving original remainder using `move_pop = <USA-west destination>`. **Do not then use ratio0.3 on the remainder**, which would send9% of original and leave21%. The complementary second whole-pop move handles engine rounding without deleting people. Require both valid, separately owned destinations before the first move. The source and both destinations must be different countries. If destination selections fail, do not partially execute the exodus; retain a pending state and retry.

For50% into a four-state Khanate, choose the destination state for each source pop once and move ratio0.5 once. A random distribution among four states preserves50% total but can be uneven; use population/capacity-aware weights if desired. Four successive0.125 moves send only41.38% of original, not50%; if a single original pop must be evenly divided among four, sequential remainder ratios must be0.125,1/7,1/6,0.2 (sending12.5% of original four times) while leaving50%. Simpler one-destination-per-pop avoids repeated rounding and is native-shaped.

Snapshot source membership AFTER the four Khanate states are established, then migrate from remaining HUS and USA owners. Native pops already inside the new four states remain there and are not re-migrated. If the intended denominator is pre-cession USA population instead, that is a different census contract and must explicitly count native residents already transferred with territory; do not mix both meanings. No immigrants can be selected again by the HUS/USA loops because destination owner differs. Keep one-time flags per route and source country, so save/reload or month pulses do not repeatedly halve population.

Failed MEX/Andean native revival can reuse the same partial-pop effect for the requested large migration to HUS, with a separately chosen bounded percentage. The user did not give this branch a numeric share; record the parent's balance choice. Capture source states and validate HUS destination before resolving defeated-country destruction; if defeat ends the country, iterate the former territory's CURRENT owner/state intersection. Do not query a dead tag's pop list or silently resurrect leaders/pops. A hosted leader transfer remains a separate character effect.

## 2. HUS starting30% Manchu/Mongol +20% Indigenous

Frozen read-only baseline from `americas-population-baseline.json`: total25,589,642; Manchu3,320,000 +Mongol1,978,500 =5,298,500 (20.7056%); Indigenous-American cultures2,648,509 (10.3499%). Rounded requested totals are7,676,893 Manchu/Mongol,5,117,928 Indigenous,12,794,821 other, sum exactly25,589,642. Required additions are+2,378,393 to Manchu/Mongol and+2,469,419 to Indigenous, offset by-4,847,812 from other cultures. These are demographic reclassification in initial history, not runtime population creation.

Maintain each state-region total, religion/pop-type fields and existing cultural distributions where feasible; allocate integer residuals globally with largest remainder. Preserve meaningful concentrations (northern Manchu, plains Mongol, local Indigenous cultures), rather than converting every region to identical30/20/50. A hard per-state30/20 would erase existing geography and is not required by the national percentages. Exclude Manchu from the Han-first acceptance branch even though current global Manchu heritage is Han. Opening population percentages apply to new games; existing saves require a separately authorized migration/rebalance and must not silently rewrite all live pops.

## 3. Real citizenship-law lock and12-month registration

The actual native per-law field is `can_enact = { ... }`, shown in `law_no_police`; AI weight zero or a hidden description does not block human enactment. Native global modifiers `country_cannot_start_law_enactment_bool` and `country_cannot_enact_laws_bool` lock ALL law groups and are unsuitable when only HUS citizenship/tier laws should be fixed.

For the HUS tier laws themselves, use `can_enact = { always = no }` and invoke `activate_law = law_type:<chosen registered law>` only from the completed registration route. But this alone does NOT prevent enacting a different citizenship law. The effective vanilla citizenship set is exactly six keys in00_citizenship.txt: `law_subjecthood`, `law_ethnostate`, `law_national_supremacy`, `law_racial_segregation`, `law_cultural_exclusion`, `law_multicultural`. Each destination needs a preserved/native full definition with an additional `can_enact` condition rejecting the original-HUS tier-lock variable (plus any new MOD variants). Do not attach the condition to all countries indiscriminately; use a dedicated original-regime marker rather than tag HUS alone, because the eventual native successor also becomes HUS and must not inherit Han/Manchu privileges. Preserve preexisting can_enact conditions conjunctively and keep exact REPLACE semantics used by current MOD law overrides. Also audit `can_impose` if foreign imposed law must be blocked; ordinary can_enact is not proof that a treaty/imposition cannot change it.

The direct `activate_law` engine effect and native history bypass the ordinary legislative process. This is the correct switch API; do not fake a passed law with a variable. Its behavior with newly added can_enact=false is source-backed but should still be one targeted runtime check if any engine validation is allowed later.

Registration lifecycle: choice stores permanent branch (Manchu/Mongol default AI, or native), then a persistent registration-started marker plus a12-month expiring wait variable. On monthly pulse, when started AND wait absent AND not-completed, activate chosen law, record completed before migration/war dispatch, clear temporary state. This avoids event duration confusion and makes reload persistent. Choice buttons cannot replace the choice while pending, and AI chooses Manchu/Mongol deterministically (other weight0) unless the user later changes it. Watch for12-month logic evaluating on a missing uninitialized variable; use has_variable guards. Scripted law activation is an actual mechanism; normal political law enactment stays locked.

## 4. ACW permanent prerequisite, before OR after choice

Native `acw_je_events.1` sets global variable `american_civil_war=yes` without a duration. A full current GAME search found one setter and no remove_global_variable/removal. Thus `has_global_variable = american_civil_war` is an existing permanent 'ever happened' flag. Native JE sets it after detecting slavery-movement civil war; no need to require USA currently at war or CSA alive. A HUS monthly dispatcher checks: branch=Manchu/Mongol, registration completed, global ACW flag exists, Khanate not launched/pending. This fires regardless of whether ACW occurred before or after registration. If route creation must wait for four eligible connected USA states, keep pending; do not forget the prior ACW condition. Never use a timed current-war flag as the only historical record.

## 5. Country identity,4-state connected founding and geography

No country named 'Western America' exists in the relevant definitions. `WES` is Westphalia (North German, capital STATE_WESTPHALIA), `CAL` is California (Yankee/Mexican, capital within HUS), and FSA is the Free States ACW participant. Interpret 'western America' here as **western USA-owned states** and use `c:USA` plus an explicit region list/predicate. Do not send migrants to WES or invent a tag silently.

Dormant `TIS` is an existing pan-Indigenous empire: cultures Cherokee/Iroquoian/Siouan, capital Oklahoma, unrecognized. It is not present in initial MOD state ownership. It is a possible reusable Khanate identity, but original Turtle Island JE automatically offers national unification and change_tag=TIS to native North American states; using TIS requires branch-scoped suppression/compatibility of `je_unite_the_nations` and its three buttons so it cannot shortcut this custom route. A dedicated MOD tag avoids that collision but is not an existing unused tag. Do not reuse active COM/SEQ/LKT/IRC and overwrite their existing populations or politics.

Native neighboring-state APIs are `any_neighbouring_state`, `random_neighbouring_state`, `ordered_neighbouring_state` (British spelling). Supported input includes state/state_region/country/strategic_region; output is state. Actual trade-state code compares neighbor `this` to a saved target state. `is_adjacent_to_state` is country→state and is not the pairwise state trigger.

Current `region_great_plains` includes15 regions, but USA does NOT own most western ones. USA whole states: Louisiana, Arkansas, Missouri, Iowa. USA partial states: Minnesota, South Dakota, Nebraska. HUS owns Colorado/Wyoming/Montana/New Mexico, most North Dakota, Kansas; Oklahoma belongs SEQ/COM, Texas TEX/MEX/COM. Therefore select four **USA-owned state intersections**, optionally requiring owns_entire_state_region if the user means whole state regions. A bare state_region transfer could seize unrelated HUS/native/Texan/Mexican pieces and violates the request. Only whole-USA initial candidates are the adjacent Louisiana–Arkansas–Missouri–Iowa chain, so random variation at1836 requires allowing USA portions or waiting for expansion. After ACW the ownership may differ: query live state owners, not initial assumptions.

Safe selection algorithm: select a qualifying seed; keep a temporary chosen-state list; each subsequent candidate must be USA-owned, eligible central/plain geography, not already chosen, and have any_neighbouring_state in the chosen list. This yields a connected set. Select all four before any territory change, and verify cardinality4 plus continued owner membership. A random seed can strand a selection before four; abandon only temporary scopes and retry, not create a smaller Khanate. Pre-enumerating valid connected quartets from the current map plus runtime owner tests gives bounded guaranteed selection and avoids mutation-before-completion. Creation transfers chosen states, then refreshes the new country's state scopes, sets capital/HQ to one actual selected state, and initializes laws/cultures/leader. Never leave the original TIS capital Oklahoma as an assumption when Oklahoma was not selected.

Native `geographic_region_north_america` in this MOD covers Canada/Atlantic/Pacific/Great Plains only; most Mexico/Central America is in region_central_america. If 'all North America claims' includes Mexico, include that explicitly. `geographic_region_americas` already contains North+Central+South and is the correct starting set for 'unify the Americas'; excluding Central America is an implementation error. Decide whether overseas island regions such as Caribbean islands count from the actual chosen region list, and make the decision condition display that same list.

## 6. Army, industry and two hostile powers

`create_military_formation` supports type=army, hq_region, supply_hub, combat_unit={ type=unit_type:... state_region=s:... count=N }. `create_building` is state-scope and supports level, PMs, reserves and ownership. New-country state transfer brings existing local infrastructure/buildings/population; do not clone them a second time. Count current barracks and units, add only deficits, initialize recruitment/manpower from available native troops, add an actual commander, and supply government/market/goods capacity. Four states and millions of arriving unemployed people need real administrative/food/industrial capacity; a throughput modifier alone is not an industry base. No arbitrary unbounded units or instant max-tech army is justified by the interface.

For each opposing country, the user requested annexation against the Khanate, while the Khanate demands humiliation. **Do not use mirror_war_goal=yes**, which would give reciprocal annexation. `annex_country` validates conflicting war goals and annexation; putting both USA's and HUS's annex demands for the SAME Khanate in one diplomatic play is a conflict/ambiguous outcome. A faithful candidate is two independent rapid wars: USA→Khanate annex / Khanate→USA humiliation, and HUS→Khanate annex / Khanate→HUS humiliation. Native source-backed current MOD shape is scoped initiator + target_country + war=yes, with explicit defender add_war_goal using holder=Khanate and target_country=opponent. Guard each launch independently for alive owner, no already-created direct play/war and one-time dispatch; avoid repeating or treating one failed launch as both complete. Simultaneous two-war creation and capitulation cross-cleanup remain an engine test requirement; an annex winner destroys the Khanate, so the other war's pending callbacks must exit cleanly. Do not override current USA civil-war sides or pull an already opposed HUS/USA into the same side merely for convenience.

## 7. Native successor HUS and cleanup

When the Khanate owns the intended complete Americas set, expose a decision using current holdings. `change_tag = HUS` is real; original native Turtle Island button uses the same API. Require HUS tag availability: conquering all Americas does not logically prove HUS dead if it acquired overseas territory. Do not delete an extant foreign HUS just to free its tag. Set a persistent native-successor marker before/after tag transition, add desired Indigenous primary cultures first, then remove every non-Indigenous primary, activate `law_racial_segregation`, remove all Han/Manchu/Mongol tier modifiers and pending timers, and unlock/close the old registration route. All HUS bootstrap/monthly/migration logic must exclude the native-successor marker so it does not reapply original-regime buffs on the next monthly tick or after load. Do not change the cultures of resident Han/Manchu/Mongol pops; removing primary status is the specified policy outcome.

Native-choice branch has NO Khanate/war dispatch. After completed registration, execute Manchu/Mongol70:30 exodus once, mark completion, and prevent later ACW from launching the other branch. If the correct branch or target country fails, maintain the unresolved branch state rather than silently defaulting to the war route.

## 8. Disable Cherokee entrance without unrelated damage

Complete native chain: monthly-country on_action includes `native_resettlement.1`; its option adds `je_indian_removal`; the JE rolls events.2/.3/.4 and completion fires.5/.6. Replace the JE using the already-proven MOD `REPLACE:je_*` disabling shape (possible=no, no lobby/inactive visibility, invalid=yes; no side effects). Disable the actual entrance event too so USA does not receive a dead-end prompt. Current project evidence from task28 explicitly says JE/buttons support REPLACE but events were handled by same-path file override retaining unrelated definitions. Therefore use a same-path `events/native_resettlement.txt` copy and disable .1's trigger, preserving other definitions; **do not assume `REPLACE:native_resettlement.1` is supported**. Existing live JE invalidation and already queued/pending .2–.4 must be reviewed for old-save migration; JE disable alone is not proof old delayed events cannot run. No need to remove SEQ or Cherokee culture/populations.

## Required external checks and remaining engine limits

Check sums/cultural targets at initial history; every migration ratio and source/target state; no kill/create replacement; one-time and cross-branch locks; laws visibly/actually selected and ordinary enactment gate; actual4 live USA-owned connected states; no initial TIS/other-tag collision; both war goal pairs; existing TIS/oldHUS cleanup; all-Americas list includes Central America; Cherokee entrance+JE closed. Engine verification still needed for same-tick ratio rounding/wealth merger behavior, disabled ordinary enactment versus script activation, creation armies, two simultaneous wars, tag transition and save/load persistence. This report makes no ENGINE_PASS claim.

## Source excerpts and SHA-256

### Partial population movement engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:9829) — lines 9829–9847; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
9829: ## move_partial_pop
9830: Moves the scoped pop to the specified state (they become unemployed)  
9831: move_partial_pop = { state = s:STATE_TUSCANY.region_state:TUS }  
9832: move_partial_pop = { state = s:STATE_TUSCANY.region_state:TUS population = 1000 }  
9833:  move_partial_pop = { state = s:STATE_TUSCANY.region_state:TUS population_ratio = 0.2 }  
9834:   
9835: NOTE: VERY IMPORTANT! This effect _may_ change the pop type of the moved pop. This will happen under the following conditions:  
9836: 1. if the current pop type cannot be unemployed, the new pop type will be the default one  
9837: 2.if the current pop type is a slave type and the target state does not allow slavery, the new pop type will be the default one
9838: **Supported Scopes**: pop  
9839: 
9840: ## move_pop
9841: Moves the scoped pop in its entirety to the specified state (they become unemployed)  
9842: move_pop = s:STATE_TUSCANY.region_state:TUS  
9843: NOTE: VERY IMPORTANT! This effect _may_ change the pop type of the moved pop. This will happen under the following conditions:  
9844: 1. if the current pop type cannot be unemployed, the new pop type will be the default one  
9845: 2.if the current pop type is a slave type and the target state does not allow slavery, the new pop type will be the default one
9846: **Supported Scopes**: pop  
9847: **Supported Targets**: state  
```

### Partial migration native ratio

[red_scare_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/red_scare_events.txt:1276) — lines 1276–1302; SHA-256 `e5388c4f147bd936dc5ff4836fcc8802bf81b7d70e7793fc79484d8fc76dc15b`

```text
1276: 			random_scope_pop = {
1277: 				limit = {
1278: 					pop_has_primary_culture = no
1279: 					pop_acceptance < acceptance_status_4
1280: 					NOR = {
1281: 						is_pop_type = slaves
1282: 						is_pop_type = peasants
1283: 					}
1284: 					AND = { # ensures that only 100 to 1000 total pops of scope:deported_pop are moved in red_scare.14.a
1285: 						total_size <= 10000
1286: 						total_size >= 1000
1287: 					}
1288: 				}
1289: 				save_scope_as = deported_pop
1290: 			}
1291: 			save_scope_as = deportation_state
1292: 		}
1293: 	}
1294: 
1295: 	option = {
1296: 		name = red_scare.14.a
1297: 		default_option = yes
1298: 		scope:deported_pop = {
1299: 			move_partial_pop = { # moves 10% of scope:deported_pop
1300: 			 	state = scope:deportation_target
1301: 			 	population_ratio = 0.1
1302: 			}
```

### Japan migration all matching pops

[ep2_hokkaido_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ep2_hokkaido_events.txt:344) — lines 344–364; SHA-256 `017027ee155f7b864004740da5ab6e6d223151826fc198c401285c3475199b32`

```text
344: 	option = {
345: 		name = hokkaido_events.2.a
346: 		default_option = yes
347: 		scope:hokkaido_state_scope = {
348: 			add_modifier = {
349: 				name = modifier_tondenhei_settlements
350: 				days = very_long_modifier_time
351: 			}
352: 		}
353: 		scope:capital_scope = {
354: 			custom_tooltip = {
355: 				text = hokkaido_events.2.tt_1
356: 				every_scope_pop = {
357: 					limit = {
358: 						culture = cu:japanese
359: 					}
360: 					move_partial_pop = {
361: 						state = scope:hokkaido_state_scope
362: 						population_ratio = 0.015
363: 					}
364: 				}
```

### ACW bounded population move

[acw_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/american_civil_war/acw_events.txt:504) — lines 504–540; SHA-256 `9f225b44f4f61a1bca9d202777337666129e09ac84faf24185b8b28c7667481e`

```text
504: 		scope:bleeding_kansas = {
505: 			ordered_neighbouring_state = {
506: 				limit = {
507: 					owner = ROOT
508: 					is_slave_state = yes
509: 				}
510: 				order_by = state_population
511: 				position = 0
512: 				check_range_bounds = no
513: 				ordered_scope_pop = {
514: 					limit = {
515: 						is_pop_type = slaves
516: 					}
517: 					save_temporary_scope_as = relevant_pop
518: 					order_by = total_size
519: 					position = 0
520: 					check_range_bounds = no
521: 					move_partial_pop = {
522: 						state = scope:bleeding_kansas
523: 						population = {
524: 							# move in at most 5% of the target state's population, max 5000, or the max size of the pop, whichever is smaller
525: 							add = scope:bleeding_kansas.state_population
526: 							multiply = 0.05
527: 							if = {
528: 								limit = {
529: 									scope:relevant_pop.total_size >= 5000
530: 								}
531: 								max = 5000
532: 							}
533: 							else = {
534: 								max = scope:relevant_pop.total_size
535: 							}
536: 						}
537: 					}
538: 				}
539: 			}
540: 		}
```

### Mass migration engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:951) — lines 951–957; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
951: ## create_mass_migration
952: Initiates mass migration of a specific culture from a origin country to a scoped state  
953: create_mass_migration = {  
954: 	origin = c:GBR  
955: 	culture = cu:english  
956: }
957: **Supported Scopes**: state  
```

### Law activation engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:12) — lines 12–15; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
12: ## activate_law
13: Activates a law for a country
14: **Supported Scopes**: country  
15: **Supported Targets**: law_type  
```

### Native per-law enactment gate

[01_policing.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_policing.txt:1) — lines 1–18; SHA-256 `8d6938f1eb556f412ba5353056cd43797f4eea3fb7ea8d6ef6e7e9eeb4a80be3`

```text
1: law_no_police = {
2: 	group = lawgroup_policing
3: 
4: 	icon = "gfx/interface/icons/law_icons/no_police.dds"
5: 
6: 	progressiveness = 0
7: 
8: 	can_enact = {
9: 		custom_tooltip = {
10: 			modifier:country_disallow_law_no_police_bool = no
11: 			text = disallow_law_no_police_tt
12: 		}
13: 	}
14: 
15: 	# AI shouldn't try to abolish institutions
16: 	ai_will_do = {
17: 		always = no
18: 	}
```

### Native country-wide start prohibition

[00_code_static_modifiers.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_code_static_modifiers.txt:999) — lines 999–1007; SHA-256 `0f42a271058ca8932c8b87641328473f1bc6a7961b7f4bf40663d5aba43faf1d`

```text
999: foreign_legislative_interference = {
1000: 	icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds
1001: 	country_cannot_start_law_enactment_bool = yes
1002: }
1003: 
1004: foreign_legislative_interference_enactment = {
1005: 	icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds
1006: 	country_cannot_cancel_law_enactment_bool = yes
1007: }
```

### Native country-wide enactment prohibition

[montenegrin_modifiers.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/montenegrin_modifiers.txt:89) — lines 89–93; SHA-256 `c6be2f66f380f3b6644da88ea797dd9e9239b03f064bfa2647298f72fe793910`

```text
89: modifier_mon_no_passing_laws = {
90: 	icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
91: 	country_cannot_enact_laws_bool = yes
92: 	state_radicals_from_political_movements_mult = 2
93: }
```

### Citizenship law types

[00_citizenship.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_citizenship.txt:1) — lines 1–32; SHA-256 `c006054323511c81b40502810c4ed8f6a806ebde02bf0a3023538e756ec9bb10`

```text
1: # group = this is the law_group a law belongs to
2: # icon = graphical icon shown in-game
3: # modifier = {} modifier on country for having adopted this law
4: 
5: law_subjecthood = {
6: 	group = lawgroup_citizenship
7: 
8: 	icon = "gfx/interface/icons/law_icons/imperial_subjecthood.dds"
9: 
10: 	progressiveness = -25
11: 
12: 	on_enact = {
13: 		recalculate_pop_ig_support = yes
14: 		if = {
15: 			limit = {
16: 				is_subject = yes
17: 			}
18: 			custom_tooltip = subjecthood_fervor_no_effects_ld_tt
19: 		}
20: 	}
21: 
22: 	can_impose = {
23: 		OR = {
24: 			AND = {
25: 				is_in_same_power_bloc = scope:target_country
26: 				AND = {
27: 					modifier:country_can_impose_same_lawgroup_citizenship_in_power_bloc_bool = yes
28: 					has_law = scope:law
29: 				}
30: 			}
31: 			can_impose_law_default = yes
32: 		}
```

### Neighbor iterator engine

[triggers.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/triggers.log:2023) — lines 2023–2028; SHA-256 `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`

```text
2023: ## any_neighbouring_state
2024: Iterate through all states neighbouring a state region  
2025: any_neighbouring_state = { <count=num/all> / <percent=fixed_point> <triggers> }
2026: Reads nothing for all scopes.
2027: **Supported Scopes**: country, state, state_region, strategic_region  
2028: **Supported Targets**: state  
```

### Random neighbor engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:28982) — lines 28982–28986; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
28982: ## random_neighbouring_state
28983: Iterate through all states neighbouring a state region  
28984: random_neighbouring_state = { limit = { <triggers> } (optional) weight = { mtth } <effects> }
28985: **Supported Scopes**: country, state, state_region, strategic_region  
28986: **Supported Targets**: state  
```

### Actual neighbor scope example

[04_trade_states.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/04_trade_states.txt:48) — lines 48–79; SHA-256 `b78b42306f55be2138c05b6b4bcc069550392b62db3387a36a09d1bcb779a7e9`

```text
48: 			}
49: 
50: 			custom_tooltip = {
51: 				text = DIPLO_ACTION_TRADE_STATES_NOT_SAME_REGION
52: 				NOT = {
53: 					scope:first_state.state_region = scope:second_state.state_region
54: 				}
55: 			}
56: 
57: 			custom_tooltip = {
58: 				text = DIPLO_ACTION_TRADE_STATES_WOULD_BREAK_CONNECTION
59: 				scope:actor = {
60: 					any_scope_state = {
61: 						NOT = { this = scope:first_state }
62: 						OR = {
63: 							any_neighbouring_state = { this = scope:second_state }
64: 							AND = {
65: 								is_coastal = yes
66: 								scope:second_state = { is_coastal = yes }
67: 							}
68: 						}
69: 					}
70: 				}
71: 				scope:target_country = {
72: 					any_scope_state = {
73: 						NOT = { this = scope:second_state }
74: 						OR = {
75: 							any_neighbouring_state = { this = scope:first_state }
76: 							AND = {
77: 								is_coastal = yes
78: 								scope:first_state = { is_coastal = yes }
79: 							}
```

### Dormant native empire TIS

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4379) — lines 4379–4388; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
4379: TIS = {
4380: 	color = { 190 133 82 }
4381: 
4382: 	country_type = unrecognized
4383: 
4384: 	tier = empire
4385: 
4386: 	cultures = { cherokee iroquoian siouan }
4387: 	capital = STATE_OKLAHOMA
4388: }
```

### Wrong WES tag

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:69) — lines 69–79; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
69: WES = {
70: 	color = { 5 85 5 }
71: 
72: 	country_type = recognized
73: 
74: 	tier = principality
75: 
76: 	cultures = { north_german }
77: 	capital = STATE_WESTPHALIA
78: 	is_named_from_capital = yes
79: }
```

### CAL tag

[00_countries.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2001) — lines 2001–2010; SHA-256 `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

```text
2001: CAL = {
2002: 	color = { 144  181  106 }
2003: 
2004: 	country_type = recognized
2005: 
2006: 	tier = principality
2007: 
2008: 	cultures = { yankee mexican }
2009: 	capital = STATE_CALIFORNIA
2010: }
```

### Turtle Island auto journal conflict

[00_turtle_island.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_turtle_island.txt:1) — lines 1–50; SHA-256 `716e4283aa690e7c250e4fa6f756d24ddd31e60e36e24c8f018139c21cd53a26`

```text
1: je_unite_the_nations = {
2: 	icon = "gfx/interface/icons/event_icons/waving_flag.dds"
3: 
4: 	group = je_group_foreign_affairs
5: 
6: 	scripted_button = je_unite_the_nations_proclaim_turtle_island_button
7:     scripted_button = je_unite_the_nations_organize_the_tribes_button
8:     scripted_button = je_unite_the_nations_offer_confederation_button
9: 
10:     is_shown_in_lobby = {
11: 		NOT = { is_country_type = decentralized }
12: 		is_in_geographic_region = geographic_region_north_america
13: 		any_primary_culture = {
14: 			has_discrimination_trait_group = heritage_group_indigenous_american
15: 		}
16: 		OR = {
17: 			NOT = {
18: 				exists = c:TIS
19: 			}
20: 			AND = {
21: 				exists = c:TIS
22: 				c:TIS = this
23: 			}
24: 		}
25: 	}
26: 
27: 	is_shown_when_inactive = {
28: 		NOT = { is_country_type = decentralized }
29: 		is_in_geographic_region = geographic_region_north_america
30: 		any_primary_culture = {
31: 			has_discrimination_trait_group = heritage_group_indigenous_american
32: 		}
33: 		OR = {
34: 			NOT = {
35: 				exists = c:TIS
36: 			}
37: 			AND = {
38: 				exists = c:TIS
39: 				c:TIS = this
40: 			}
41: 		}
42: 	}
43: 
44: 	possible = {
45: 		is_subject = no
46: 	}
47: 
48: 	complete = {
49: 		custom_tooltip = {
50: 			text = je_unite_the_nations_complete_tt
```

### Turtle Island tag action

[turtle_island_buttons.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/turtle_island_buttons.txt:1) — lines 1–22; SHA-256 `8c5b48719a0e34efb88e6bb7a0c0f428f09fbf2e529a0599902f14a4c66682b8`

```text
1: je_unite_the_nations_proclaim_turtle_island_button = {
2: 	name = "je_unite_the_nations_proclaim_turtle_island_button"
3: 	desc = "je_unite_the_nations_proclaim_turtle_island_button_desc"
4: 
5: 	visible = {
6: 		NOT = {
7: 			exists = c:TIS
8: 		}
9: 	}
10: 
11: 	possible = {
12: 		has_technology_researched = nationalism
13: 		any_decentralized_country = {
14: 			is_in_geographic_region = geographic_region_north_america
15: 			is_adjacent_to_country = root
16: 		}
17: 	}
18: 
19: 	effect = {
20: 		change_tag = TIS
21: 	}
22: }
```

### Actual HUS/USA geography

[north_america_strategic_regions.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/strategic_regions/north_america_strategic_regions.txt:1) — lines 1–36; SHA-256 `6e03d9f31e4bf4415117b1ce73285d5c0f0e094f70d699a0a1cb0ba0b4cecf4c`

```text
1: # Strategic Regions in North America
2: 
3: region_canada = {
4: 	capital_province = x8C4FC7
5: 	map_color = { 0.21 0.81 0.82 }
6: 	states = { STATE_NORTHWEST_TERRITORIES STATE_NUNAVUT STATE_ONTARIO STATE_QUEBEC STATE_NEWFOUNDLAND STATE_MANITOBA STATE_ALBERTA STATE_SASKATCHEWAN }
7: }
8: 
9: region_pacific_coast = {
10: 	capital_province = xBD0F03
11: 	map_color = { 0.471 0.824 0.196 }
12: 	states = { STATE_CALIFORNIA STATE_WASHINGTON STATE_OREGON STATE_IDAHO STATE_NEVADA STATE_UTAH STATE_ARIZONA STATE_ALASKA STATE_YUKON_TERRITORY STATE_BRITISH_COLUMBIA 
13: 	STATE_SOUTH_DAYUAN
14: 
15: 	STATE_NORTH_DAYUAN
16: }
17: }
18: 
19: region_great_plains = {
20: 	capital_province = x9A9935
21: 	map_color = { 0.5 1 0.5 }
22: 	states = { STATE_MONTANA STATE_WYOMING STATE_COLORADO STATE_NORTH_DAKOTA STATE_SOUTH_DAKOTA STATE_NEBRASKA STATE_KANSAS STATE_NEW_MEXICO STATE_LOUISIANA STATE_ARKANSAS STATE_TEXAS STATE_OKLAHOMA STATE_MISSOURI STATE_IOWA STATE_MINNESOTA}
23: }
24: 
25: region_atlantic_coast = {
26: 	capital_province = x6B3BE8
27: 	map_color = { 0 0.8 0.4 }
28: 	states = { STATE_WISCONSIN STATE_MICHIGAN STATE_INDIANA STATE_ILLINOIS STATE_WEST_VIRGINIA STATE_OHIO STATE_KENTUCKY STATE_TENNESSEE STATE_MASSACHUSETTS STATE_MAINE STATE_CONNECTICUT STATE_RHODE_ISLAND STATE_VERMONT STATE_NEW_HAMPSHIRE STATE_NEW_BRUNSWICK STATE_BERMUDA STATE_PENNSYLVANIA STATE_NEW_YORK STATE_NEW_JERSEY STATE_MISSISSIPPI STATE_ALABAMA STATE_FLORIDA STATE_GEORGIA STATE_SOUTH_CAROLINA STATE_NORTH_CAROLINA STATE_VIRGINIA STATE_DISTRICT_OF_COLUMBIA STATE_MARYLAND STATE_DELAWARE}
29: }
30: 
31: region_central_america = {
32: 	graphical_culture = "latin"
33: 	capital_province = x10EFC0
34: 	map_color = { 1 0.25 0.25 }
35: 	states = { STATE_BAJA_CALIFORNIA STATE_HONDURAS STATE_NICARAGUA STATE_COSTA_RICA STATE_PANAMA STATE_SAN_SALVADOR STATE_YUCATAN STATE_CHIAPAS STATE_GUATEMALA STATE_JALISCO STATE_ZACATECAS STATE_GUERRERO STATE_MEXICO STATE_CHIHUAHUA STATE_DURANGO STATE_RIO_GRANDE STATE_SONORA STATE_VERACRUZ STATE_SINALOA STATE_BAJIO STATE_OAXACA STATE_WESTERN_CUBA STATE_JAMAICA STATE_HAITI STATE_SANTO_DOMINGO STATE_WEST_INDIES STATE_BAHAMAS STATE_PUERTO_RICO STATE_EASTERN_CUBA STATE_CENTRAL_CUBA}
36: }
```

### Continental geography

[02_geographic_regions_america.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/geographic_regions/02_geographic_regions_america.txt:1) — lines 1–41; SHA-256 `d8282bf1ee3fbaa80f9c57ef943f30b487d2a5f45b2978a393a7d3024a8b8216`

```text
1: geographic_region_north_america = {
2: 	short_key = "north_america"
3: 
4: 	strategic_regions = {
5: 		sr:region_canada
6: 		sr:region_atlantic_coast
7: 		sr:region_pacific_coast
8: 		sr:region_great_plains
9: 	}
10: }
11: 
12: geographic_region_south_america = {
13: 	short_key = "south_america"
14: 
15: 	strategic_regions = {
16: 		sr:region_brazil
17: 		sr:region_la_plata
18: 		sr:region_andes
19: 		sr:region_gran_colombia
20: 	}
21: }
22: 
23: geographic_region_americas = {
24: 	short_key = "americas"
25: 
26: 	strategic_regions = {
27: 		sr:region_canada
28: 		sr:region_atlantic_coast
29: 		sr:region_pacific_coast
30: 		sr:region_great_plains
31: 
32: 		#geographic_region_central_america
33: 		sr:region_central_america
34: 
35: 		#geographic_region_south_america
36: 		sr:region_brazil
37: 		sr:region_la_plata
38: 		sr:region_andes
39: 		sr:region_gran_colombia
40: 	}
41: }
```

### ACW persistent global marker

[acw_je_events.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/american_civil_war/acw_je_events.txt:111) — lines 111–115; SHA-256 `aa76f4b83dbf2b51d6a59a478f02d79306e4ac77380ecdb19edb51636bfbe90a`

```text
111: 		}
112: 		set_global_variable = {
113: 			name = american_civil_war
114: 			value = yes
115: 		}
```

### Native ACW listener

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

### Cherokee monthly caller

[00_code_on_actions.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:474) — lines 474–483; SHA-256 `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb`

```text
474: # Root = Country
475: on_monthly_pulse_country = {
476: 	events = {
477: 		communism.8 # Red Army
478: 		opium_wars.1
479: 		native_resettlement.1
480: 		bic_breakup.1
481: 		dreyfus.1
482: 		dei_breakup.1
483: 		alk_breakup.1
```

### Cherokee event entrance

[native_resettlement.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/native_resettlement.txt:1) — lines 1–61; SHA-256 `f57064e02b72d926a27855e79a60d96734adc4537fc310898cdec0b95830322c`

```text
1: namespace = native_resettlement
2: 
3: # Worcester v. Georgia
4: # Jackson defies the Supreme Court
5: native_resettlement.1 = {
6: 	type = country_event
7: 
8: 	icon = "gfx/interface/icons/event_icons/event_scales.dds"
9: 	event_image = {
10: 		video = "europenorthamerica_native_american"
11: 	}
12: 
13: 	on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
14: 
15: 	placement = s:STATE_GEORGIA.region_state:USA
16: 
17: 	title = native_resettlement.1.t
18: 	desc = native_resettlement.1.d
19: 	flavor = native_resettlement.1.f
20: 
21: 	duration = 3
22: 
23: 	trigger = {
24: 		exists = c:USA
25: 		exists = c:SEQ
26: 		c:USA = ROOT
27: 		NOT = { has_variable = indian_removal_var }
28: 		c:SEQ ?= { is_subject_of = c:USA }
29: 		owns_entire_state_region = STATE_GEORGIA
30: 		ruler = {
31: 			has_trait = bigoted
32: 		}
33: 	}
34: 
35: 	immediate = {
36: 		set_variable = indian_removal_var
37: 		ruler = {
38: 			save_scope_as = indian_removal_president
39: 		}
40: 		c:SEQ ?= {
41: 			save_scope_as = indian_territory_scope
42: 		}
43: 		cu:cherokee = {
44: 			save_scope_as = cherokee_culture
45: 		}
46: 	}
47: 
48: 	option = {
49: 		name = native_resettlement.1.a
50: 		default_option = yes
51: 		add_journal_entry = {
52: 			type = je_indian_removal
53: 		}
54: 	}
55: 
56: 	cancellation_trigger = {
57: 		NOT = {
58: 			exists = c:SEQ
59: 		}
60: 	}
61: }
```

### Cherokee JE lifecycle

[00_indian_removal.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_indian_removal.txt:1) — lines 1–74; SHA-256 `9a849a3b3e5a64709a9e5cd09a1e13174c6a88cb2c95eb5b907f7142c1b53cb0`

```text
1: je_indian_removal = {
2: 	icon = "gfx/interface/icons/event_icons/event_skull.dds"
3: 
4: 	group = je_group_usa_manifest_destiny
5: 
6: 	is_shown_in_lobby = {
7: 		c:USA = THIS
8: 	}
9: 
10: 	on_monthly_pulse = {
11: 		random_events = {
12: 			20 = 0
13: 			2 = native_resettlement.2 # john ross. Fires once because very specific.
14: 			2 = native_resettlement.3 # Preparing for resettlement, repeats.
15: 			1 = native_resettlement.4 # Trail of Tears, requires native_resettlement.3 to have fired at least once.
16: 		}
17: 	}
18: 
19: 	complete = {
20: 		OR = {
21: 			has_law_or_variant = law_type:law_no_colonial_affairs
22: 			country_average_culture_pop_acceptance = { culture = cu:cherokee value >= acceptance_status_4 }
23: 			custom_tooltip = {
24: 				text = indian_removal_fail_tt
25: 				NOT = {
26: 					any_scope_state = {
27: 						any_scope_pop = {
28: 							culture = cu:cherokee
29: 						}
30: 					}
31: 				}
32: 			}
33: 		}
34: 	}
35: 
36: 	on_complete = {
37: 		custom_tooltip = {
38: 			text = indian_removal_end
39: 			if = {
40: 				limit = {
41: 					NOT = {
42: 						any_scope_pop = {
43: 							culture = cu:cherokee
44: 						}
45: 					}
46: 				}
47: 				trigger_event = { id = native_resettlement.5 }
48: 			}
49: 			else = {
50: 				trigger_event = { id = native_resettlement.6 }
51: 			}
52: 		}
53: 	}
54: 
55: 	invalid = {
56: 		OR = {
57: 			NOT = { owns_entire_state_region = STATE_GEORGIA }
58: 			NOT = {
59: 				AND = {
60: 					exists = c:SEQ
61: 					exists = c:USA
62: 					c:SEQ ?= { is_subject_of = c:USA }
63: 				}
64: 			}
65: 		}
66: 	}
67: 
68: 	weight = 200
69: 
70: 		
71: 	should_be_pinned_by_default_uninvolved_or_context = yes
72: 
73: 	transferable = no
74: }
```

### Existing proven JE disable shape

[zzzz_nesnd_native_error_bans.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/zzzz_nesnd_native_error_bans.txt:1) — lines 1–12; SHA-256 `75af4203078eeb29b76c01e12bdfbbc13aedd70e035228915bfc4aed9efad793`

```text
1: # No split, territory transfer, or new ZAN creation; existing countries are untouched.
2: REPLACE:je_splitting_oman = {
3:     icon = "gfx/interface/icons/event_icons/event_portrait.dds"
4:     group = je_group_historical_content
5:     is_shown_in_lobby = { always = no }
6:     is_shown_when_inactive = { always = no }
7:     possible = { always = no }
8:     complete = { always = no }
9:     fail = { always = no }
10:     invalid = { always = yes }
11: }
```

### Event override directory rule evidence

[release-notes.md](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/cne-time-native-ban-20261103/release-notes.md:11) — lines 11–18; SHA-256 `433e75db51fa565d1c1c98ca3ab1e48a9c8eafd3ab1553edbdfeac25c85b6d28`

```text
11: ## 原版故障
12: 
13: 关闭原生波兰请求按钮/.1/.2、阿曼分裂JE/zanzibar.1、movement_events.6及coup_aftermath_events.1；保留本MOD波兰、其它同文件事件、既有国家/领土。整合主义仅关闭两个错scope赔款权重。海况cyclone/rough_waters/tropical_storm禁用并去掉随机求值，三类海况不再产生其原有效果；其它海况及核心海战逻辑保持。海战本地化仅修不存在/不可求值的方法调用。重复add JE不处理。
14: 
15: JE和按钮使用已证REPLACE。事件等采用同路径覆盖并保留非目标定义；没有假定所有数据库均支持REPLACE。整文件覆盖绑定当前1.13.11/build24799966，升级必须对照来源SHA。无定位的command_values未知国家、引擎断言和外部资源冲突仍未解决，不能宣称整MOD零错误。
16: 
17: ## 检查与设计
18: 
```

### Military creation engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:959) — lines 959–990; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
959: ## create_military_formation
960: Creates a military formation  
961: create_military_formation = {  
962: 	# Optional name  
963: 	name = "name"  
964: 	# type defaults to army  
965: 	type = army/fleet  
966: 	hq_region = sr:region_russia  
967: 	# Optional, overrides the automatic supply hub selection  
968: 	supply_hub = s:STATE_MOSCOW  
969: 	# Add as many combat_unit specifications as necessary  
970: 	combat_unit = {  
971: 		type = unit_type:combat_unit_type_irregular_infantry  
972: 		# service_type defaults to regular and conscript is not applicable for fleets  
973: 		service_type = regular/conscript  
974: 		state_region = s:STATE_MOSCOW  
975: 		count = 5  
976: 	}  
977: 	# mobilization_options are not applicable for fleets  
978: 	mobilization_options = {  
979: 		mobilization_option:mobilization_option_basic_supplies  
980: 		mobilization_option:mobilization_option_truck_transport  
981: 	}  
982: }
983: **Supported Scopes**: country  
984: 
985: ## create_political_lobby
986: Creates a new political lobby  
987: create_political_lobby = {  
988: 	type = lobby_pro_country  
989: 	arget = <country scope>  
990: 	add_interest_group = <ig scope 1>  
```

### Building creation engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:817) — lines 817–839; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
817: ## create_building
818: Creates a building in the scoped state. Supported values are:  
819: 	building = <building>  
820: 	activate_production_methods = { <production_methods> }  
821: 	subsidized = yes/no  
822: 	reserves = [0..1] (percentage of cash reserves the building should be created with)  
823: 	add_ownership = { (mutually exclusive with level)  
824: 		country = { (give ownership levels to a specific country)  
825: 			country = s:GBR (country script target)  
826: 			levels = 5  
827: 		}  
828: 		country = { (give ownership levels to a specific building)  
829: 			type = building_financial_district (building type that will get ownership levels, should be self or other ownership type)  
830: 			region = STATE_SINAI (region where owning building is placed)  
831: 			country = s:GBR (country script target for a region)  
832: 			levels = 3  
833: 		}  
834: 	}  
835: 	level = arable_land/integer(mutually exclusive with add_ownership)  
836:   
837: If level is "arable_land", the building will be of the necessary level to exhaust all available arable land in the state.  
838: If level is an integer, the building will be of that level  
839:   
```

### Existing immediate war shape

[nesnd_cne_republic.txt](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_cne_republic.txt:85) — lines 85–105; SHA-256 `1ab1708f907dbe4ea22b967e7583b11bcf26074edc1058833eaef46d601d4dd4`

```text
85: nesnd_cne_start_republic_war = {
86:     if = {
87:         limit = {
88:             c:CNE ?= this
89:             nesnd_cne_republic_target_available = yes
90:             NOT = { nesnd_cne_republic_has_play = yes }
91:         }
92:         end_truce = c:NRP
93:         create_diplomatic_play = {
94:             name = nesnd_cne_republic_war
95:             type = dp_nesnd_cne_republic
96:             target_country = c:NRP
97:             war = yes
98:             annex_as_civil_war = no
99:         }
100:         if = {
101:             limit = { nesnd_cne_republic_has_play = yes }
102:             c:NRP = { set_variable = nesnd_cne_republic_war_created }
103:         }
104:     }
105:     # Also observes an already-existing direct war, without recreating it.
```

### Annex war-goal conflict validation

[00_annex_country.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/00_annex_country.txt:1) — lines 1–25; SHA-256 `f6ced621bac6a29b35d771f1a322219d9520565046af402790bd4ffdf22195e2`

```text
1: annex_country = {
2: 	icon = "gfx/interface/icons/war_goals/annex_country.dds"
3: 
4: 	kind = annex_country
5: 
6: 	settings = {
7: 		require_target_be_part_of_war
8: 		can_add_for_other_country
9: 		annexes_entire_country
10: 		skip_build_list
11: 
12: 		# Validation
13: 		validate_conflicts_war_goals_all
14: 		validate_conflicts_annex_country
15: 	}
16: 
17: 	execution_priority = 80
18: 
19: 	contestion_type = control_half_target_country_states
20: 
21: 	target_type = country
22: 
23: 	possible = {
24: 		# trigger to determine if a goal with its target data is listed when selecting a war goal in the diplo play panel
25: 		# scopes: root = holder, creator_country, diplomatic_play, target_country, target_state, stakeholder, target_region, article_options
```

### Humiliation war goal

[08_humiliation.txt](D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/08_humiliation.txt:1) — lines 1–25; SHA-256 `1dfd74884beb5211093bc474c08fd72bac303ec7f110bfe55143076afa0e0088`

```text
1: humiliation = {
2: 	icon = "gfx/interface/icons/war_goals/humiliation.dds"
3: 
4: 	kind = humiliation
5: 
6: 	settings = {
7: 		require_target_be_part_of_war
8: 
9: 		# Validation
10: 		validate_conflicts_war_goals_all
11: 	}
12: 
13: 	execution_priority = 18
14: 
15: 	contestion_type = control_any_target_country_state
16: 
17: 	target_type = country
18: 
19: 	possible = {
20: 		# trigger to determine if a goal with its target data is listed when selecting a war goal in the diplo play panel
21: 		# scopes: root = holder, creator_country, diplomatic_play, target_country, target_state, stakeholder, target_region, article_options
22: 	}
23: 
24: 	valid = {
25: 		# trigger in addition to some basic validation code-side
```

### Claim effect

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:74) — lines 74–78; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
74: ## add_claim
75: Adds scoped state region as a claim for target country  
76: add_claim = scope/country
77: **Supported Scopes**: state_region  
78: **Supported Targets**: country  
```

### Tag change engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:682) — lines 682–685; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
682: ## change_tag
683: Change the tag for the scoped country  
684: c:GBR = { change_tag = FRA }
685: **Supported Scopes**: country  
```

### Primary culture add

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:347) — lines 347–351; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
347: ## add_primary_culture
348: Adds a culture to the primary cultures of a country  
349: add_primary_culture = X  
350: Where X is a culture scope
351: **Supported Scopes**: country  
```

### Primary culture remove

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:36610) — lines 36610–36614; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
36610: ## remove_primary_culture
36611: Removes a culture from the primary cultures of a country  
36612: remove_primary_culture = X  
36613: Where X is a culture scope
36614: **Supported Scopes**: country  
```

### Variable expiration engine

[effects.log](D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:37194) — lines 37194–37214; SHA-256 `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

```text
37194: ## set_variable
37195: Sets a variable  
37196: set_variable = { name = X value = Y days = Z }  
37197: Where X is the name of the variable used to then access it  
37198: Where Y is any event target, bool, value, script value or flag (flag:W)  
37199: An optional days where Z is the number of days or script value  
37200: This variable will be accessible with <type_>var:X. With type being in a scope object or in a top scope  
37201: Can also be used as set_variable = X (equivalent to set_variable = { name = X value = yes })
37202: **Supported Scopes**: none  
37203: 
37204: ## set_war
37205: Set a diplomatic play to be a war  
37206: set_war = bool
37207: **Supported Scopes**: diplomatic_play  
37208: 
37209: ## show_as_tooltip
37210: Enclosed effects are only shown in tooltips (but are not actually executed)  
37211: show_as_tooltip = { <more effects> }
37212: **Supported Scopes**: none  
37213: 
37214: ## sort_global_variable_list
```
