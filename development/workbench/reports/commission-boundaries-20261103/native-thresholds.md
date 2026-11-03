# 两司后置门槛：原版完整链条与开局分母

Date: 2026-11-03. Scope: source research only; no gameplay files changed, no game launched. Current local game is **1.13.11 / Steam build 24799966**; NESND catalog status returned CURRENT with zero changed fingerprints. This report follows the Matt Pocock research workflow, adapted by NESND engineering-skills.md to current local primary source and WORK output. All source files below were read; hashes bind this report to these versions. This is source evidence and design advice, **not ENGINE_PASS**.

## Findings that affect implementation

1. Native African colonial administrations unlock through `civilizing_mission` (era 3), not `democracy` (era 1). Their creation buttons require ≥2 **owned states that are the largest state in their region**, within the relevant strategic region. They do **not** count subject land for that threshold. The current commission gates copied the number 2 but used era-1 `democracy`, which USM already has through `add_era_researched = era_1`. Sources A1/A2/A4/M1/M6.
2. Native Confederation of the Rhine supplies the actual **owner is ROOT OR owner is ROOT's subject** model, threshold ≥4 and great-power rank in the JE. There is no technology prerequisite in this JE/button. Its `any_state_in_german_confederation` counts **state objects**, not distinct state regions. Its region membership comes from the geographic-region database. Sources R1/R2/R5.
3. Engine `is_subject_of` explicitly includes subject-of-subject. For the requested **direct princes**, test guarded `overlord = ROOT`; calling `is_subject_of = ROOT` alone direct is incorrect. Engine `any_state_region` supports `count`, and native Highveld uses `any_state_region → any_scope_state → owner`. Use that outer iterator for distinct-region counts. Sources C1/C3.
4. The effective main-MOD starting map has 23 mainland regions in north/south India after excluding Ceylon. USM owns pieces of 6; TRA's sole region overlaps USM's TRAVANCORE, so their union is **6**, not 7. MYS has no living initial state; its relationship is conditional. MUG owns pieces of **12** mainland regions. The current prince predicate matches **43 living countries** across **19 mainland regions**. Sources M3/M4/M5/M7 and the machine-readable counts beside this report.
5. Current six-region Yuanshan target matches native `geographic_region_south_africa`, not the nine-region southern-Africa strategic region. USM and its starting subjects control **zero** pieces of these six regions. Sources C6/M1/M4/M5; whole-file diplomacy review found no southern-African subject of USM.
6. Current Tianzhu transfer is bounded to six existing mainland regions plus Ceylon and Indian Ocean Territory; current Yuanshan transfer is six South African regions. Merely raising the gate will not expand the transfer or the gameplay coverage. The creator always seeds from a **USM-owned** Madras/Zululand state; a broad subject-land gate can therefore still fail the creator unless this seed rule is retained and shown, or redesigned. Sources M1/M2/M8.
7. `puppet` subject type has `can_have_subjects = no`; native `colony` has `can_have_subjects = yes`. Both current commissions are made puppets. Any plan to place princes under the commission must resolve this before transfer. Sources A6/A7/M2. This is a type-contract finding, not authority to change the authored political system.

## Native caller → trigger/value → effect → database chain

### African administration

`common/journal_entries/00_establish_colonial_administration.txt` exposes the four establish and four expand buttons. Inactive visibility requires non-African country context, not unrecognized, and an African interest; `possible` requires independent, not unrecognized, an owned sub-Saharan state, and `civilizing_mission` (A1).

`common/scripted_buttons/00_colonial_administration_buttons.txt` contains the whole creation effect inline: country-owned state threshold ≥2, `is_largest_state_in_region = yes`; no committed diplomatic-play participation or war; no recent-colony flag among subjects. It chooses an owned regional capital, favoring a migration decree, marks **all own states** in the strategic region, then calls `create_dynamic_country` with `origin=root`, colonial country type, principality tier, chosen culture and capital, and cession by the temporary state marker. It sets frontier-colonization/colonial-administration laws and the colonial-administration modifier; clears cession markers; creates a `colony` diplomatic pact; copies additional primary cultures; fires `colonial_administration_events.1` next day. Establish buttons have 90-day cooldown; the generated country's new flag lasts 3 months (A2). These are inline numeric constants, not a hidden scripted value.

`events/colonial_administration_events.txt` then chooses the new flagged subject and its capital/region. Option A can turn it into a chartered company, while other options select different institutions/relations; therefore “native colonial administration = always a puppet” is false (A3).

Database closure: `civilizing_mission` is era 3, requires `quinine` and `nationalism`, raises colonial-affairs investment maximum by 1 and reduces infamy against unrecognized countries by 0.25 (A4). `law_colonial_administration` is a governance-principles law for colonial/company countries (A5). `colony` maps to `subject_type_colony` (A6), which allows subjects (A7). The named modifier supplies incorporation-speed changes (A8). The JE uses the colonization invention DDS and the event uses the map icon/video specified in A1/A3. No new art is needed to reuse this UI pattern.

### Confederation of the Rhine

`common/journal_entries/01_natural_borders_of_france.txt`: visibility responds to regional subjects or own unincorporated German homeland land, excludes German-primary-culture countries; activation requires great-power rank and ≥4 regional states either owned directly or held by an eligible German subject, excluding personal unions and checking the **subject capital** lies in the confederation geography (R1).

`common/scripted_buttons/00_scripted_buttons.txt:718`: create button requires RHN absent and repeats ≥4 owned-or-eligible-subject states, with German homeland restriction; then directly fires `rhine_confederation.1` (R2). This region + owner OR subject model is native. No technology check exists in either gate, so attributing `pan-nationalism`/`civilizing_mission` to the Rhine gate would be wrong.

`events/agitators_events/natural_borders.txt:595`: event is gated to DLC004. Immediate selection prefers a player subject, else a ranked regional subject, changing its tag to RHN; absent eligible subjects, it selects an owned eligible unincorporated state by GDP and `create_country` with that state, then establishes a puppet. Options annex eligible subjects into RHN and cede own unincorporated German states; French natural-border exceptions apply in one route (R3). The `RHN` database is a recognized empire, north/south German primary cultures, capital Hesse (R4). The geographic database establishes the region used by generated iterator names (R5).

**Capital guard and transfer caveat:** native Rhine eligibility capital constraints characterize which **countries** count; they are not a definition of ownership of their every state. Native event selection is broader than the button's filtered count, and annexing entire countries also transfers their out-of-area land. Do not import that behavior into a bounded commission transfer just because native code exists.

## Correct counting semantics

The map hierarchy is province → state_region → owner-specific state → strategic_region. In a split region, USM and TRA can each have a state; a direct sum of country-state counts can double-count the same region. `is_largest_state_in_region` is documented only as “largest state in the state region”; the export does not state the area/population algorithm or tie behavior. This report does **not** identify province counts with engine-largest status.

Native-supported composition for an explicit distinct-region **presence** count, evaluated in the intended root country scope:

```text
any_state_region = {
    count >= 12
    # Explicit mainland region predicate: 23 named regions; exclude islands.
    any_scope_state = {
        state_population > 0
        OR = {
            owner = ROOT
            owner = { is_subject_of = ROOT }
        }
    }
}
```

The outer iterator deduplicates regions; inside, `is_largest_state_in_region = yes` can additionally require effective regional dominance like the African precedent. **Presence** counts a treaty-port-sized slice; **largest-state** excludes small enclaves but may reject an alliance's combined majority when neither individual allied state is largest. **Complete union control** instead requires every state owner in a region belongs to ROOT's subject hierarchy (`count = all`, or NOT any foreign owner), with a separate nonempty/populated-state check. Pick one and write its player-facing condition accurately. These three definitions are different design choices, not interchangeable syntax fixes. C1/C3/C5 prove the ingredients; this new combination still needs external and targeted engine validation.

For direct princes use a country iterator with the authored prince predicate, alive status and guarded immediate overlord identity. Example shape:

```text
any_country = {
    count >= 3
    nesnd_india_prince = yes
    is_subject = yes
    exists = overlord
    overlord = ROOT
}
```

For territorial control, native `is_subject_of` includes nested subjects, so ROOT + all subject tiers is available without recursively counting countries. A country may be a subject because its capital is in the target area while owning land elsewhere; only count states inside the explicit mainland/commission domain.

## Bounded, reachable proposed gates (new design, not native requirements)

| Gate | Starting effective source baseline | Suggested threshold | Rationale / bound |
|---|---:|---:|---|
| Tianzhu technology | democracy already known; civilizing_mission absent | civilizing_mission | era-3 native colonial-administration precedent; no fixed date claim |
| Tianzhu distinct mainland regions | presence union 6, dominant-state union at most 6 | ≥12 of 23 | at least 6 additional regions under presence rule; source-estimated mid/late expansion, not tested difficulty |
| Tianzhu princes | 1 living direct prince, TRA | ≥3 direct princes, with a conquest-equivalent fallback | at least 2 additional princes; 43 living starting choices; MYS must not count |
| Tianzhu Mughal expansion | 0 former MUG pieces controlled | ≥2 of the 12 MUG-origin mainland regions, using real original-MUG territory criteria | must not count a conquered neighboring prince in the same split region |
| Yuanshan technology | civilizing_mission absent | civilizing_mission | same era-3 unlock |
| Yuanshan distinct target regions | 0 of 6 | ≥4 of 6 | broad South African expansion; upper bound 6, no impossible ≥8/≥12 typo |

12/23, 3 princes, 2 MUG-origin regions, and 4/6 are balance recommendations; native code proves the interfaces and analogous workflow only. Native African ≥2 should not be called an authored late-expansion target automatically. No source-only threshold can guarantee a particular unlock year.

**Prince-annexation fallback:** use `(≥3 direct princes) OR (complete allied control of ≥3 initially princely mainland regions)`, while retaining ≥12 total regions and the Mughal requirement. The 19 initially princely regions are listed below; none is fully controlled by USM+TRA at start, so the fallback cannot satisfy itself from the colonial starting land. This permits a conquest path even after every prince has been annexed. It is intentionally more land-demanding than gathering three tiny princes. A more exact mixed score can count each original prince once if currently direct subject OR its entire original provincial footprint is now allied-owned, but that requires 43 bounded origin-footprint checks and careful no-double-counting; the attached origin-province JSON supports this implementation. Do not require living princes unconditionally: complete conquest otherwise makes formation impossible.

**Mughal-origin test:** an allowlist of the 12 regions plus ANY allied state is insufficient. AWADH has both AWA and MUG; HILL_PUNJAB has MUG/GAR/PAN/PTA; RAJPUTANA has a one-province MUG enclave plus many princes. Conquering a prince there must not count as conquest of MUG. Two viable definitions:

- Exact, recommended for faithful provenance: per region, require the original MUG provincial footprint all currently held by USM or qualifying subordinate owners, then sum qualifying regions. `p:xE0EFA0.state.owner = ROOT` is an actual native ownership path (C4); the same `owner={is_subject_of=ROOT}` logic applies. Use fixed 1836 source footprints, so the condition survives MUG disappearance or old-save loading. This proves acquisition of originally MUG land, not that the player personally fought MUG; requiring that separate historical event would need campaign markers and old-save rules.
- Simpler conservative alternative: ≥2 of those regions under **complete allied control**. This cannot falsely count non-Mughal enclaves, but demands taking every remaining prince's land too. Present it as a deliberately stricter alternative.

Keeping only provinces still tagged MUG creates a failure after total annexation. Conversely, testing `exists = c:MUG` as a formation prerequisite permanently locks out success after the empire is conquered. Neither is appropriate here.

**Small-enclave edge case:** original MUG footprints contain only 1 province in RAJPUTANA and 2 in HILL_PUNJAB. Acquiring those two alone could meet a footprint-based ≥2 gate, despite being little Mughal territory. The ≥12 total-region gate still forces broad expansion, but if the authored intent specifically requires imperial heartland conquest, restrict this subcondition to BIHAR, EAST_BENGAL, AGRA, BOMBAY, WEST_BENGAL and DELHI, six regions where the source province-list counts show MUG has a majority; or require complete allied region control. This majority-of-listed-provinces classification is a transparent design criterion, not a claim about the engine's largest-state algorithm. Do not quietly switch definitions without updating the displayed requirement.

## Starting territory table

Counts below are owner-specific `create_state` blocks and number of listed provinces, **not population, area, or a prediction of the engine's largest-state result**. Effective state history is a single MOD `common/history/states/00_states.txt` overriding the same base file; the base has no additional state-history file. Blank/commented-out create_state blocks are excluded by the ordered parser. Regions use the effective MOD strategic-region database. This table is new-game source initialization, not a running save snapshot.

| Region | Initial owners (province entries) | State-history region line |
|---|---|---:|
| STATE_GUJARAT | BER (8), KUT (7), DHA (2), IDA (5), NAW (6), PLP (1), USM (8), JUN (3), BHV (3) | 4254 |
| STATE_SINDH | SIN (32) | 4070 |
| STATE_CENTRAL_PROVINCES | HYD (9), NAG (25), BAS (10), MUG (21) | 4147 |
| STATE_AWADH | AWA (15), MUG (13) | 4397 |
| STATE_MALWA | IND (9), GWA (19), BHO (2) | 4301 |
| STATE_AGRA | MUG (34), GAR (3) | 9370 |
| STATE_BUNDELKHAND | BAG (9), BUN (4), SUR (7), JHN (4) | 9347 |
| STATE_BIHAR | MUG (39) | 4341 |
| STATE_EAST_BENGAL | MUG (30) | 121 |
| STATE_WEST_BENGAL | MUG (16), COO (1) | 4349 |
| STATE_ASSAM | MUG (9), ASM (6), NGA (11), MNP (5), TIP (3), KKI (4), MGH (5) | 4361 |
| STATE_ORISSA | MUG (6), MYB (6), PTN (8), NAR (3) | 4050 |
| STATE_PUNJAB | PAN (42), BHW (10) | 4135 |
| STATE_HILL_PUNJAB | MUG (2), GAR (5), PAN (14), PTA (4) | 9399 |
| STATE_DELHI | MUG (10), PTA (1) | 4410 |
| STATE_RAJPUTANA | BIK (13), JAS (9), MEW (8), JOD (22), JAI (10), MUG (1), ALW (4), KOT (3), GWA (1), IND (1) | 4078 |
| STATE_CIRCARS | USM (17), JEY (7) | 4123 |
| STATE_MYSORE | USM (16) | 4174 |
| STATE_TRAVANCORE | TRA (5), USM (3), COC (1) | 4187 |
| STATE_MADRAS | USM (26) | 4203 |
| STATE_HYDERABAD | HYD (45) | 4244 |
| STATE_KURNOOL | USM (12), KNO (2) | 9331 |
| STATE_BOMBAY | POR (1), MUG (25), SAT (10), KHP (3) | 4318 |
| STATE_CEYLON | USM (15) | 1647 |
| STATE_INDIAN_OCEAN_TERRITORY | FRA (1), USM (2) | 3327 |
| STATE_CAPE_COLONY | SAF (27), NAM (16) | 3464 |
| STATE_EASTERN_CAPE | SAF (21), XHO (17) | 3445 |
| STATE_NORTHERN_CAPE | SAF (40), TSW (18), WBL (8), SAN (18) | 3483 |
| STATE_ZULULAND | ZUL (22), BST (7) | 5957 |
| STATE_VRYSTAAT | ORA (17), PHL (7), BST (6) | 5975 |
| STATE_TRANSVAAL | MTB (28), TRN (11), PDI (11), SWZ (3), VND (14) | 6000 |

USM mainland set: STATE_GUJARAT, STATE_CIRCARS, STATE_MYSORE, STATE_TRAVANCORE, STATE_MADRAS, STATE_KURNOOL.

MUG original mainland set: STATE_CENTRAL_PROVINCES, STATE_AWADH, STATE_AGRA, STATE_BIHAR, STATE_EAST_BENGAL, STATE_WEST_BENGAL, STATE_ASSAM, STATE_ORISSA, STATE_HILL_PUNJAB, STATE_DELHI, STATE_RAJPUTANA, STATE_BOMBAY.

Initially princely mainland regions (19): STATE_GUJARAT, STATE_SINDH, STATE_CENTRAL_PROVINCES, STATE_AWADH, STATE_MALWA, STATE_AGRA, STATE_BUNDELKHAND, STATE_WEST_BENGAL, STATE_ASSAM, STATE_ORISSA, STATE_PUNJAB, STATE_HILL_PUNJAB, STATE_DELHI, STATE_RAJPUTANA, STATE_CIRCARS, STATE_TRAVANCORE, STATE_HYDERABAD, STATE_KURNOOL, STATE_BOMBAY.

Living prince tags under current authored predicate (43): ALW, ASM, AWA, BAG, BAS, BER, BHO, BHV, BHW, BIK, BUN, COC, COO, DHA, GAR, GWA, HYD, IDA, IND, JAI, JAS, JEY, JHN, JOD, JUN, KHP, KNO, KOT, KUT, MEW, MNP, MYB, NAG, NAR, NAW, PAN, PLP, PTA, PTN, SAT, SIN, SUR, TRA.

`STATE_CEYLON` and `STATE_INDIAN_OCEAN_TERRITORY` can remain in a transfer design if authorized, but cannot be silently included in a “mainland Indian regions” unlock denominator. Indian Ocean Territory is in east-Africa strategic geography in the base source, while the native broad `geographic_region_india` also includes frontier regions outside the MOD's two India strategic regions (C7). Use the explicit mainland scope when “23” is the documented maximum.

## Required follow-through for an implementation

- Keep one readiness predicate shared by decision, JE button and creation effect, so the effect rechecks exact current ownership/subject conditions. Current module already centralizes this part (M1/M2/M9/M10).
- Keep visibility/progression distinct from the final action gate: show the campaign JE as the player advances; do not hide the only explanation until every expansion requirement is met.
- Decide whether seed capital must be directly owned. If all-subject control should suffice, current fixed `region_state:USM` creators are inadequate. Do not steal an arbitrary independent owner's state when choosing a seed; use an allied eligible state, preserve its owners' out-of-area land, and confirm actual relationship success before additional transfers.
- Territorial gate scope, transfer scope, state-case migration scope, prince lifecycle scope, and governance JE scope must agree. The current six-mainland transfer would leave newly required Indian conquests outside Tianzhu (M2).
- Treat nested-subject territory and direct-prince count separately. Resolve puppet/colony `can_have_subjects` before any reparent operation.
- For bounded tests cover starting USM+TRA dedupe, split-region enclave ownership, all-subject territorial control, two former-MUG captures, no-MUG/no-princes after annexation, absent fixed seed, existing commission, war/play refusal, repeated click, and failure to create the intended subject relation. No claim of engine success follows from this report.

## Source ledger and verified excerpts

Each source label used above is expanded below with absolute path, SHA-256 and one-based line snippets. All paths outside WORK/MOD are read-only.

### A1: [00_establish_colonial_administration.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_establish_colonial_administration.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_establish_colonial_administration.txt`  
SHA-256: `a5a1fc6bd2c502a67b282aad0ac421ebc20d6c38e8888aad7794f6f6358b6509`

Lines 1–24:

```text
1: je_colonial_administration = {
2: 	icon = "gfx/interface/icons/invention_icons/colonization.dds"
3: 
4: 	group = je_group_foreign_affairs
5: 
6: 	is_shown_when_inactive = {
7: 		NOT = { is_country_type = unrecognized }
8: 		is_not_in_geographic_region = geographic_region_africa
9: 		OR = {
10: 			has_interest_marker_in_region = sr:region_west_africa
11: 			has_interest_marker_in_region = sr:region_east_africa
12: 			has_interest_marker_in_region = sr:region_southern_africa
13: 			has_interest_marker_in_region = sr:region_equatorial_africa
14: 		}
15: 	}
16: 
17: 	possible = {
18: 		NOT = { is_country_type = unrecognized }
19: 		is_subject = no
20: 		any_scope_state = {
21: 			is_in_geographic_region = geographic_region_subsaharan_africa
22: 		}
23: 		has_technology_researched = civilizing_mission
24: 	}
```

Lines 54–63:

```text
54: 	scripted_button = je_colonial_administration_button_senegal
55: 	scripted_button = je_colonial_administration_button_zanj
56: 	scripted_button = je_colonial_administration_button_southern_africa
57: 	scripted_button = je_colonial_administration_button_congo
58: 
59: 	# Expand Colonial Administration
60: 	scripted_button = je_colonial_administration_button_expand_senegal
61: 	scripted_button = je_colonial_administration_button_expand_zanj
62: 	scripted_button = je_colonial_administration_button_expand_southern_africa
63: 	scripted_button = je_colonial_administration_button_expand_congo
```

### A2: [00_colonial_administration_buttons.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_colonial_administration_buttons.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_colonial_administration_buttons.txt`  
SHA-256: `78008eb248bd06e77c38583357fdfcf122a64faa9e0ddfaa45456347ba067042`

Lines 1–38:

```text
1: je_colonial_administration_button_senegal = {
2: 	name = "je_colonial_administration_button_senegal"
3: 	desc = "je_colonial_administration_button_senegal_desc"
4: 
5: 	visible = {
6: 		is_not_in_geographic_region = geographic_region_africa
7: 		any_scope_state = {
8: 			region = sr:region_west_africa
9: 		}
10: 		NOT = {
11: 			any_subject_or_below = {
12: 				has_variable = senegal_subject_var
13: 			}
14: 		}
15: 	}
16: 
17: 	cooldown = { days = 90 }
18: 
19: 	possible = {
20: 		any_scope_state = {
21: 			region = sr:region_west_africa
22: 			is_largest_state_in_region = yes
23: 			count >= 2
24: 		}
25: 
26: 		#prevents splitting off during diplo play or war as it invalidates wargoals. is_at_war is there for clarity for players even though it's technically included in the former
27: 		is_diplomatic_play_committed_participant = no
28: 		is_at_war = no
29: 
30: 		custom_tooltip = {
31: 			text = colonial_administration_cooldown
32: 			NOT = {
33: 				any_subject_or_below = {
34: 					has_variable = newly_formed_colonial_nation_var
35: 				}
36: 			}
37: 		}
38: 	}
```

Lines 73–111:

```text
73: 		}
74: 		every_scope_state = {
75: 			limit = {
76: 				region = sr:region_west_africa
77: 			}
78: 			set_variable = state_to_cede
79: 		}
80: 		create_dynamic_country = {
81: 			origin = root
82: 			country_type = colonial
83: 			tier = principality
84: 			culture = scope:colony_culture_scope
85: 			capital = scope:newly_formed_colonial_nation_capital_scope
86: 			cede_state_trigger = {
87: 				has_variable = state_to_cede
88: 			}
89: 			on_created = {
90: 				set_variable = senegal_subject_var
91: 				set_variable = {
92: 					name = newly_formed_colonial_nation_var
93: 					months = 3
94: 				}
95: 				every_scope_state = {
96: 					remove_variable = state_to_cede
97: 				}
98: 				activate_law = law_type:law_frontier_colonization
99: 				activate_law = law_type:law_colonial_administration
100: 				add_modifier = {
101: 					name = colonial_administration
102: 				}
103: 			}
104: 		}
105: 		hidden_effect = {
106: 			create_diplomatic_pact = {
107: 				country = scope:newly_formed_colonial_nation_capital_scope.owner
108: 				type = colony
109: 			}
110: 			scope:overlord_country ?= {
111: 				every_primary_culture = { # ROOT's primary cultures
```

Lines 267–294:

```text
267: 		}
268: 		NOT = {
269: 			any_subject_or_below = {
270: 				has_variable = southern_africa_subject_var
271: 			}
272: 		}
273: 	}
274: 
275: 	cooldown = { days = 90 }
276: 
277: 	possible = {
278: 		any_scope_state = {
279: 			region = sr:region_southern_africa
280: 			is_largest_state_in_region = yes
281: 			count >= 2
282: 		}
283: 
284: 		#prevents splitting off during diplo play or war as it invalidates wargoals. is_at_war is there for clarity for players even though it's technically included in the former
285: 		is_diplomatic_play_committed_participant = no
286: 		is_at_war = no
287: 
288: 		custom_tooltip = {
289: 			text = colonial_administration_cooldown
290: 			NOT = {
291: 				any_subject_or_below = {
292: 					has_variable = newly_formed_colonial_nation_var
293: 				}
294: 			}
```

### A3: [colonial_administration_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/colonial_administration_events.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/colonial_administration_events.txt`  
SHA-256: `bf7ec34d0fb0093ad7b2283c54dd2bdc63c9e4a9e32763732731cab489a22691`

Lines 26–38:

```text
26: 	immediate = {
27: 		random_subject_or_below = {
28: 			limit = {
29: 				has_variable = newly_formed_colonial_nation_var
30: 			}
31: 			save_scope_as = newly_formed_colonial_nation_scope
32: 			capital = {
33: 				save_scope_as = newly_formed_colonial_nation_capital_scope
34: 				region = {
35: 					save_scope_as = newly_formed_colonial_nation_region_scope
36: 				}
37: 			}
38: 		}
```

Lines 47–67:

```text
47: 	option = {
48: 		name = colonial_administration_events.1.a
49: 		default_option = yes
50: 		create_diplomatic_pact = {
51: 			country = scope:newly_formed_colonial_nation_scope
52: 			type = chartered_company
53: 		}
54: 		custom_tooltip = {
55: 			text = colonial_administration_events.1_tt_1
56: 			scope:newly_formed_colonial_nation_scope = {
57: 				activate_law = law_type:law_colonial_administration
58: 				activate_law = law_type:law_oligarchy
59: 				activate_law = law_type:law_subjecthood
60: 				active_law:lawgroup_citizenship ?= { # Subjecthood
61: 					add_amendment = {
62: 						type = amendment_racialized_subjecthood
63: 						sponsor = PREV.ig:ig_armed_forces
64: 					}
65: 				}
66: 				activate_law = law_type:law_extraction_economy
67: 				activate_law = law_type:law_colonial_exploitation
```

### A4: [30_society.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt`  
SHA-256: `410b033c6ed95b5b417370a8778e5e056bc49d2cb95098854b0eb88d69f58cbb`

Lines 100–111:

```text
100: democracy = {
101: 	# Unlocks Right of Assembly - Freedom of Speech Law
102: 	# Unlocks Landed Voting, Wealth Voting, Census Voting - Distribution of Power Laws
103: 	# Unlocks Presidential Republic, Parliamentary Republic - Governance Principles Law
104: 	era = era_1
105: 	texture = "gfx/interface/icons/invention_icons/democracy.dds"
106: 	category = society
107: 
108: 	modifier = {
109: 		country_institution_social_security_max_investment_add = 2
110: 	}
111: 
```

Lines 691–708:

```text
691: nationalism = {
692: 	# Unlocks the Immigration Controls Law in Migration
693: 	# New leaders may spawn with the Ethno-Nationalist Ideology
694: 	era = era_2
695: 	texture = "gfx/interface/icons/invention_icons/nationalism.dds"
696: 	category = society
697: 
698: 	modifier = {
699: 		country_authority_mult = 0.1
700: 		country_voting_power_mult = 0.1
701: 	}
702: 
703: 	unlocking_technologies = {
704: 		mass_communication
705: 		international_relations
706: 	}
707: 
708: 	ai_weight = {
```

Lines 951–969:

```text
951: civilizing_mission = {
952: 	# Unlocks Panama Canal survey expedition decision
953: 	# Unlocks the Panama Canal
954: 
955: 	era = era_3
956: 	texture = "gfx/interface/icons/invention_icons/civilizing_mission.dds"
957: 	category = society
958: 
959: 	modifier = {
960: 		country_institution_colonial_affairs_max_investment_add = 1
961: 		country_infamy_generation_against_unrecognized_mult = -0.25
962: 	}
963: 
964: 	unlocking_technologies = {
965: 		quinine
966: 		nationalism
967: 	}
968: 
969: 	ai_weight = {
```

### A5: [00_governance_principles.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt`  
SHA-256: `e676448ea64c17079677ddbf2cbfdbec0ffdefa465286f16c1e6107a14e7f4cf`

Lines 290–321:

```text
290: law_colonial_administration = {
291: 	group = lawgroup_governance_principles
292: 	parent = law_monarchy
293: 
294: 	icon = "gfx/interface/icons/law_icons/colonial_administration.dds"
295: 
296: 	progressiveness = 0
297: 
298: 	disallowing_laws = {
299: 		law_anarchy
300: 	}
301: 
302: 	can_enact = {
303: 		country_is_colonial_or_company = yes
304: 	}
305: 
306: 	is_visible = {
307: 		country_is_colonial_or_company = yes
308: 	}
309: 
310: 	can_impose = {
311: 		scope:target_country ?= {
312: 			country_is_colonial_or_company = yes
313: 			is_subject_of = root
314: 		}
315: 	}
316: 
317: 	modifier = {
318: 		country_legitimacy_headofstate_add = 10
319: 		country_legitimacy_ideological_incoherence_mult = 0.2
320: 		country_bureaucrats_pol_str_mult = 1
321: 		country_officers_pol_str_mult = 1
```

### A6: [48_subject_colony.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/48_subject_colony.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/48_subject_colony.txt`  
SHA-256: `a73f8efc849a2813442fccb3adbf2960bcef933c1f15695be629daf7d3eb1aef`

Lines 1–25:

```text
1: colony = {
2: 	groups= {
3: 		general # for breaking only
4: 	}
5: 	show_in_lens = no
6: 
7: 	potential = { # Only created through diplomatic plays
8: 		always = no
9: 	}
10: 
11: 	pact = {
12: 		cost = 10
13: 		has_junior_participant = yes
14: 		maintenance_paid_by = first_country
15: 		income_transfer = 0.3
16: 		second_country_gets_income_transfer = no
17: 		income_transfer_based_on_second_country = yes
18: 
19: 		max_target_involvement = 8000
20: 		target_involvement_applies_to = source_country
21: 
22: 		relations_progress_per_day = 1
23: 		relations_improvement_max = 50
24: 
25: 		subject_type = subject_type_colony
```

### A7: [00_subject_types.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/subject_types/00_subject_types.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/subject_types/00_subject_types.txt`  
SHA-256: `97a488157dfb2f340cca06aba30bfef42a36ea0a48dce6e591c8891628a6b91d`

Lines 63–74:

```text
63: subject_type_puppet = {
64: 	allow_change_country_flag = yes
65: 	use_overlord_map_color = yes
66: 	use_overlord_ruler = no
67: 	annex_on_country_formation = yes
68: 	can_start_own_diplomatic_plays = no
69: 	breaks_if_subject_not_protected = yes
70: 	join_overlord_wars = yes
71: 	can_have_subjects = no
72: 	overlord_must_be_higher_rank = yes
73: 	overlord_must_be_same_country_type = no
74: 	use_for_release_country = yes
```

Lines 301–312:

```text
301: subject_type_colony = {
302: 	allow_change_country_flag = yes
303: 	use_overlord_map_color = yes
304: 	use_overlord_ruler = no
305: 	annex_on_country_formation = no
306: 	can_start_own_diplomatic_plays = no
307: 	breaks_if_subject_not_protected = yes
308: 	join_overlord_wars = yes
309: 	can_have_subjects = yes
310: 	overlord_must_be_higher_rank = yes
311: 	overlord_must_be_same_country_type = no
312: 	use_for_release_country = yes
```

### A8: [02_event_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/02_event_modifiers.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/02_event_modifiers.txt`  
SHA-256: `43fd43a9c772de4323582da2780c62eee87e8eb1f87a5fb845a643d064a8873d`

Lines 2004–2013:

```text
2004: colonial_administration = {
2005: 	icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
2006: 	state_non_contiguous_incorporation_speed_mult = -0.5
2007: 	state_contiguous_incorporation_speed_mult = 1.0
2008: }
2009: 
2010: usa_capital_relocated = {
2011: 	icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_negative.dds
2012: 	country_legitimacy_base_add = -15
2013: 	state_incorporation_speed_mult = -0.25
```

### R1: [01_natural_borders_of_france.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/01_natural_borders_of_france.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/01_natural_borders_of_france.txt`  
SHA-256: `7410283c9f4fb832576be6af56bc441015643add42a0a31714d559bdf9d35959`

Lines 80–149:

```text
80: je_confederation_of_the_rhine = {
81: 	icon = "gfx/interface/icons/event_icons/waving_flag.dds"
82: 
83: 	group = je_group_france_expansion
84: 
85: 	is_shown_when_inactive = {
86: 		OR = {
87: 			any_subject_or_below = {
88: 				capital = {
89: 					is_in_geographic_region = geographic_region_german_confederation
90: 				}
91: 			}
92: 			any_scope_state = {
93: 				state_region = {
94: 					OR = {
95: 						is_homeland = cu:south_german
96: 						is_homeland = cu:north_german
97: 					}
98: 				}
99: 				is_in_geographic_region = geographic_region_german_confederation
100: 				is_incorporated = no
101: 				NOT = {
102: 					ROOT = {
103: 						has_claim = prev.state_region
104: 					}
105: 				}
106: 			}
107: 		}
108: 		NOR = {
109: 			country_has_primary_culture = cu:north_german
110: 			country_has_primary_culture = cu:south_german
111: 		}
112: 	}
113: 
114: 	possible = {
115: 		country_rank >= rank_value:great_power
116: 		any_state_in_german_confederation = {
117: 			OR = {
118: 				owner = {
119: 					is_subject_of = ROOT
120: 					NOT = {
121: 						has_diplomatic_pact = {
122: 							who = ROOT
123: 							type = personal_union
124: 							is_initiator = no
125: 						}
126: 					}
127: 					capital = {
128: 						is_in_geographic_region = geographic_region_german_confederation
129: 					}
130: 					OR = {
131: 						country_has_primary_culture = cu:north_german
132: 						country_has_primary_culture = cu:south_german
133: 					}
134: 				}
135: 				owner = ROOT
136: 			}
137: 			count >= 4
138: 		}
139: 	}
140: 
141: 	immediate = {
142: 		save_scope_as = rhine_overlord
143: 		cu:north_german = {
144: 			save_scope_as = north_german_scope
145: 		}
146: 		cu:south_german = {
147: 			save_scope_as = south_german_scope
148: 		}
149: 	}
```

### R2: [00_scripted_buttons.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_scripted_buttons.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_scripted_buttons.txt`  
SHA-256: `4d85ac44950c38e09180c99e3fbe6c90b447bb7f57952577e771eab1277e2703`

Lines 718–769:

```text
718: je_confederation_of_the_rhine_confederate_button = {
719: 	name = "je_confederation_of_the_rhine_confederate_button"
720: 	desc = "je_confederation_of_the_rhine_confederate_button_desc"
721: 
722: 	visible = {
723: 		NOT = {
724: 			exists = c:RHN
725: 		}
726: 	}
727: 
728: 	possible = {
729: 		NOT = {
730: 			exists = c:RHN
731: 		}
732: 		any_state_in_german_confederation = {
733: 			state_region = {
734: 				OR = {
735: 					is_homeland = cu:south_german
736: 					is_homeland = cu:north_german
737: 				}
738: 			}
739: 			OR = {
740: 				owner = {
741: 					is_subject_of = ROOT
742: 					NOT = {
743: 						has_diplomatic_pact = {
744: 							who = ROOT
745: 							type = personal_union
746: 							is_initiator = no
747: 						}
748: 					}
749: 					capital = {
750: 						is_in_geographic_region = geographic_region_german_confederation
751: 					}
752: 					OR = {
753: 						country_has_primary_culture = cu:north_german
754: 						country_has_primary_culture = cu:south_german
755: 					}
756: 				}
757: 				owner = root
758: 			}
759: 			count >= 4
760: 		}
761: 	}
762: 
763: 	ai_chance = {
764: 		value = 50
765: 	}
766: 
767: 	effect = {
768: 		trigger_event = { id = rhine_confederation.1 }
769: 	}
```

### R3: [natural_borders.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/natural_borders.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/natural_borders.txt`  
SHA-256: `653273898c7f90e73be4a8ee613a8673987aeb71794362ad6f122eb945a6d960`

Lines 595–613:

```text
595: rhine_confederation.1 = {
596: 	type = country_event
597: 	placement = root
598: 	title = rhine_confederation.1.t
599: 	desc = rhine_confederation.1.d
600: 	flavor = rhine_confederation.1.f
601: 
602: 	duration = 3
603: 
604: 	dlc = dlc004
605: 
606: 	event_image = {
607: 		video = "unspecific_signed_contract"
608: 	}
609: 
610: 	on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
611: 
612: 	icon = "gfx/interface/icons/event_icons/waving_flag.dds"
613: 
```

Lines 708–755:

```text
708: 				limit = {
709: 					state_region = {
710: 						OR = {
711: 							is_homeland = cu:south_german
712: 							is_homeland = cu:north_german
713: 						}
714: 					}
715: 					OR = {
716: 						is_in_geographic_region = geographic_region_north_germany_old
717: 						is_in_geographic_region = geographic_region_south_germany_old
718: 						is_in_geographic_region = geographic_region_rhine_old
719: 					}
720: 					is_incorporated = no
721: 					trigger_if = {
722: 						limit = {
723: 							ROOT = {
724: 								country_has_primary_culture = cu:french
725: 							}
726: 						}
727: 						NOR = {
728: 							state_region = s:STATE_RHINELAND
729: 							state_region = s:STATE_NORTH_RHINE
730: 							state_region = s:STATE_WALLONIA
731: 							state_region = s:STATE_FLANDERS
732: 						}
733: 					}
734: 				}
735: 				order_by = gdp
736: 				position = 0
737: 				check_range_bounds = no
738: 				save_scope_as = rhine_state
739: 			}
740: 			create_country = {
741: 				tag = RHN
742: 				origin = ROOT
743: 				state = scope:rhine_state
744: 			}
745: 			ROOT = {
746: 				create_diplomatic_pact = {
747: 					country = c:RHN
748: 					type = puppet
749: 				}
750: 			}
751: 		}
752: 		c:RHN ?= {
753: 			save_scope_as = rhine_scope
754: 		}
755: 	}
```

Lines 814–849:

```text
814: 		name = rhine_confederation.1.b
815: 		default_option = yes
816: 		every_country_in_german_confederation = {
817: 			limit = {
818: 				NOT = {
819: 					c:RHN ?= THIS
820: 				}
821: 				is_subject_of = ROOT
822: 				NOT = {
823: 					has_diplomatic_pact = {
824: 						who = ROOT
825: 						type = personal_union
826: 						is_initiator = no
827: 					}
828: 				}
829: 			}
830: 			c:RHN ?= {
831: 				annex_with_incorporation = prev
832: 			}
833: 		}
834: 		every_scope_state = {
835: 			limit = {
836: 				state_region = {
837: 					OR = {
838: 						is_homeland = cu:south_german
839: 						is_homeland = cu:north_german
840: 					}
841: 				}
842: 				is_in_geographic_region = geographic_region_german_confederation
843: 				is_incorporated = no
844: 			}
845: 			set_state_owner = c:RHN
846: 			set_state_type = incorporated
847: 		}
848: 	}
849: }
```

### R4: [00_countries.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt`  
SHA-256: `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74`

Lines 4289–4298:

```text
4289: RHN = {
4290: 	color = { 77 165 128 }
4291: 
4292: 	country_type = recognized
4293: 
4294: 	tier = empire
4295: 
4296: 	cultures = { north_german south_german }
4297: 	capital = STATE_HESSE
4298: }
```

### R5: [01_geographic_regions_europe.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/01_geographic_regions_europe.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/01_geographic_regions_europe.txt`  
SHA-256: `3d1a2f254103520231d5baeb9befc9a426562c26a72e7d0e855395b6774e8251`

Lines 31–39:

```text
31: geographic_region_german_confederation = {
32: 	short_key = "german_confederation"
33: 
34: 	state_regions = {
35: 		# former sr:region_north_germany
36: 		STATE_HESSE
37: 		STATE_HANNOVER
38: 		STATE_BRUNSWICK
39: 		STATE_ELBE
```

### C1: [triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log`  
SHA-256: `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`

Lines 3888–3893:

```text
3888: ## any_scope_state
3889: Iterate through all states including provinces from a: country, state_region, theater, front, or strait  
3890: any_scope_state = { <count=num/all> / <percent=fixed_point> <triggers> }
3891: Reads nothing for all scopes.
3892: **Supported Scopes**: country, front, state_region, strait, strategic_region, theater  
3893: **Supported Targets**: state  
```

Lines 5368–5372:

```text
5368: ## any_state_region
5369: Iterate through all state regions  
5370: any_state_region = { <count=num/all> / <percent=fixed_point> <triggers> }
5371: **Supported Scopes**: none  
5372: **Supported Targets**: state_region  
```

Lines 11999–12003:

```text
11999: ## is_largest_state_in_region
12000: Check if state is the largest in the state region = bool
12001: Traits: yes/no 
12002: Reads gamestate for all scopes.
12003: **Supported Scopes**: state  
```

Lines 12447–12452:

```text
12447: ## is_subject_of
12448: Checks if country in scope is subject (or subject-of-subject) of event target  
12449: is_subject_of = country
12450: Traits: country scope
12451: Reads gamestate for all scopes.
12452: **Supported Scopes**: country  
```

Lines 13453–13457:

```text
13453: ## owns_entire_state_region
13454: Check if country owns entire region  
13455: owns_entire_state_region = key
13456: Reads gamestate for all scopes.
13457: **Supported Scopes**: country  
```

### C2: [effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log`  
SHA-256: `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`

Lines 878–890:

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

Lines 924–941:

```text
924: ## create_dynamic_country
925: Creates a new country with a dynamic tag  
926: create_dynamic_country = {  
927:  origin = country	# optional, newly created country may inherit certain values from the origin country  
928:  country_type = country type # optional if origin is set, may be repeated, will try to inherit country type from origin if not specified  
929:  tier = country tier # optional if origin is set, may be repeated, will try to inherit country tier from origin if not specified  
930:  culture = culture # optional if origin is set, may be repeated, will try to inherit cultures from origin if not specified  
931:  religion = religion # optional if origin is set, if no religion is specified, will try to inherit religion from origin if not specified  
932:  capital = state		# optional if states have been supplied, will try to set a capital from supplied states if not specified  
933:  social_hierarchy = social hierarchy key # optional; if not specified: same as origin's if origin is set, default hierarchy otherwise  
934:  cede_state_trigger = trigger # if this trigger is set, each state in the world for which it evaluates true will be ceded to the new country  
935:  color = rgb 		# optional, will try to inherit map color from origin if not specified  
936:  primary_unit_color = rgb 		# optional, will try to inherit unit color from origin if not specified  
937:  secondary_unit_color = rgb 		# optional, will try to inherit unit color from origin if not specified  
938:  tertiary_unit_color = rgb 		# optional, will try to inherit unit color from origin if not specified  
939:  on_created = effect	# optional effect that will be run with the newly created country in scope  
940: }
941: **Supported Scopes**: none  
```

Lines 37144–37149:

```text
37144: ## set_state_owner
37145: Set State Owner  
37146: set_state_owner = scope
37147: **Supported Scopes**: state  
37148: **Supported Targets**: country  
37149: 
```

### C3: [05_struggle_for_the_highveld.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_struggle_for_the_highveld.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_struggle_for_the_highveld.txt`  
SHA-256: `cd0d30f6efb844f72d3ad377fddb204db62830fecf72056e11f31520a0bcda9b`

Lines 59–98:

```text
59: 
60: 	complete = {
61: 		# Cape Colony must exert direct or indirect control over all of IRL South Africa and Swaziland and Lesotho
62: 		trigger_if = {
63: 			limit = {
64: 				c:SAF ?= this
65: 			}
66: 
67: 			# Every other country with a capital in South Africa must either be a subject of Cape or of Cape's top overlord
68: 			# But Cape /can/ be a subject and complete this
69: 			custom_tooltip = {
70: 				text = je_struggle_for_the_highveld_saf_success
71: 
72: 				NOT = {
73: 					any_state_region = {
74: 						is_in_geographic_region = geographic_region_south_africa
75: 
76: 						any_scope_state = {
77: 							owner = {
78: 								capital ?= {
79: 									is_in_geographic_region = geographic_region_south_africa
80: 								}
81: 								NOR = {
82: 									c:SAF ?= this
83: 									is_country_type = decentralized
84: 									is_subject_of = c:SAF
85: 									AND = {
86: 										c:SAF ?= { is_subject = yes }
87: 										is_subject_of = c:SAF.top_overlord
88: 									}
89: 								}
90: 							}
91: 						}
92: 					}
93: 				}
94: 			}
95: 		}
96: 		trigger_else = {
97: 			# Both Boer and Southern Bantu states must become recognized to complete the JE, be independent, and have access to the sea
98: 
```

### C4: [india_decisions.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/decisions/india_decisions.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/decisions/india_decisions.txt`  
SHA-256: `310cfdd220e1f3e8673801cff342bd5fd12334fe2d4dbbfe821ea943316eaf0e`

Lines 76–84:

```text
76: make_delhi_capital = {
77: 	is_shown = {
78: 		c:BIC ?= this
79: 		NOT = {
80: 			has_variable = made_delhi_capital_var
81: 		}
82: 		p:xE0EFA0.state.owner = root
83: 	}
84: 
```

### C5: [00_poland.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_poland.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_poland.txt`  
SHA-256: `9b01c5dbfa033492753278f044dc20bf3c1f1ac8701c95e6aea51c82b65b930f`

Lines 38–43:

```text
38:     complete = {
39:         any_state_in_poland_old = {
40:             owner = root
41:             count = all
42:         }
43:     }
```

### C6: [03_geographic_regions_africa.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/03_geographic_regions_africa.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/03_geographic_regions_africa.txt`  
SHA-256: `82005a2e57194899645578b4a5d059fc592972ac791dd4eb303c95bcf3f3eab6`

Lines 50–61:

```text
50: geographic_region_south_africa = {
51: 	short_key = "south_africa"
52: 
53: 	state_regions = {
54: 		STATE_NORTHERN_CAPE
55: 		STATE_CAPE_COLONY
56: 		STATE_EASTERN_CAPE
57: 		STATE_VRYSTAAT
58: 		STATE_TRANSVAAL
59: 		STATE_ZULULAND
60: 	}
61: }
```

### C7: [04_geographic_regions_asia.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/04_geographic_regions_asia.txt>)

Path: `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/geographic_regions/04_geographic_regions_asia.txt`  
SHA-256: `58d9fca599ddcf90ea5302b623d48fab1e9a8525177812f2ee8bb95200ecb871`

Lines 43–57:

```text
43: geographic_region_india = {
44: 	short_key = "india"
45: 
46: 	strategic_regions = {
47: 		sr:region_north_india
48: 		sr:region_south_india
49: 	}
50: 
51: 	state_regions = {
52: 		STATE_QUETTA
53: 		STATE_PASHTUNISTAN
54: 		STATE_KASHMIR
55: 		STATE_BALUCHISTAN
56: 	}
57: }
```

### M1: [nesnd_commissions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commissions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_commissions.txt`  
SHA-256: `92952c23e1980bf39540962265579e72d8fe0821a3269379ca1aa398b4e1a2d9`

Lines 1–25:

```text
1: nesnd_tianzhu_region = { OR = { state_region = s:STATE_CIRCARS state_region = s:STATE_KURNOOL state_region = s:STATE_MADRAS state_region = s:STATE_MYSORE state_region = s:STATE_TRAVANCORE state_region = s:STATE_GUJARAT state_region = s:STATE_CEYLON state_region = s:STATE_INDIAN_OCEAN_TERRITORY } }
2: nesnd_tianzhu_commission_available = { c:USM ?= this NOT = { has_variable = nesnd_tianzhu_commission_established } NOT = { exists = c:TZ1 } }
3: nesnd_tianzhu_commission_ready = {
4:     nesnd_tianzhu_commission_available = yes is_subject = no is_at_war = no is_active_in_diplomatic_play = no
5:     has_technology_researched = democracy
6:     NOT = { has_variable = nesnd_tianzhu_commission_cooldown }
7:     exists = s:STATE_MADRAS.region_state:USM
8:     s:STATE_MADRAS.region_state:USM ?= { state_population > 0 any_scope_building = { is_building_type = building_port level >= 1 } }
9:     any_scope_state = { count >= 2 nesnd_tianzhu_region = yes is_largest_state_in_region = yes state_population > 0 }
10:     any_scope_state = { nesnd_tianzhu_region = yes any_scope_building = { is_building_type = building_government_administration level >= 1 } }
11: }
12: nesnd_tianzhu_governance_live = { c:TZ1 ?= this is_country_alive = yes any_scope_state = { nesnd_tianzhu_region = yes } NOT = { has_variable = nesnd_commission_governance_done } }
13: 
14: nesnd_yuanshan_region = { OR = { state_region = s:STATE_CAPE_COLONY state_region = s:STATE_EASTERN_CAPE state_region = s:STATE_NORTHERN_CAPE state_region = s:STATE_ZULULAND state_region = s:STATE_VRYSTAAT state_region = s:STATE_TRANSVAAL } }
15: nesnd_yuanshan_commission_available = { c:USM ?= this NOT = { has_variable = nesnd_yuanshan_commission_established } NOT = { exists = c:YU1 } }
16: nesnd_yuanshan_commission_ready = {
17:     nesnd_yuanshan_commission_available = yes is_subject = no is_at_war = no is_active_in_diplomatic_play = no
18:     has_technology_researched = democracy
19:     NOT = { has_variable = nesnd_yuanshan_commission_cooldown }
20:     exists = s:STATE_ZULULAND.region_state:USM
21:     s:STATE_ZULULAND.region_state:USM ?= { state_population > 0 any_scope_building = { is_building_type = building_port level >= 1 } }
22:     any_scope_state = { count >= 2 nesnd_yuanshan_region = yes is_largest_state_in_region = yes state_population > 0 }
23:     any_scope_state = { nesnd_yuanshan_region = yes any_scope_building = { is_building_type = building_government_administration level >= 1 } }
24: }
25: nesnd_yuanshan_governance_live = { c:YU1 ?= this is_country_alive = yes any_scope_state = { nesnd_yuanshan_region = yes } NOT = { has_variable = nesnd_commission_governance_done } }
```

### M2: [nesnd_commissions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_commissions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_commissions.txt`  
SHA-256: `11f5dae6c49217e958c8cf36164502d0ad5304b27e2623946946d268e0371dae`

Lines 183–218:

```text
183: nesnd_establish_tianzhu_commission = {
184:     if = { limit = { nesnd_tianzhu_commission_ready = yes }
185:         set_variable = { name = nesnd_tianzhu_commission_cooldown months = 12 }
186:         create_country = { tag = TZ1 origin = c:USM state = s:STATE_MADRAS.region_state:USM on_created = {
187:                 set_country_type = colonial set_social_hierarchy = british_indian_caste_system activate_law = law_type:law_hindu_caste_not_enforced set_variable = nesnd_commission_created
188:                 nesnd_commission_inherit_technology = yes copy_laws = c:USM
189:                 activate_law = law_type:law_presidential_republic activate_law = law_type:law_autocracy set_social_hierarchy = british_indian_caste_system activate_law = law_type:law_hindu_caste_not_enforced
190:                 set_capital = STATE_MADRAS
191:             }
192:         }
193:         if = { limit = { exists = c:TZ1 }
194:             create_diplomatic_pact = { country = c:TZ1 type = puppet }
195:             if = { limit = { c:TZ1 = { is_subject_of = c:USM } }
196:                 if = { limit = { exists = s:STATE_CIRCARS.region_state:USM } s:STATE_CIRCARS.region_state:USM = { set_state_owner = c:TZ1 } }
197:                 if = { limit = { exists = s:STATE_KURNOOL.region_state:USM } s:STATE_KURNOOL.region_state:USM = { set_state_owner = c:TZ1 } }
198:                 if = { limit = { exists = s:STATE_MYSORE.region_state:USM } s:STATE_MYSORE.region_state:USM = { set_state_owner = c:TZ1 } }
199:                 if = { limit = { exists = s:STATE_TRAVANCORE.region_state:USM } s:STATE_TRAVANCORE.region_state:USM = { set_state_owner = c:TZ1 } }
200:                 if = { limit = { exists = s:STATE_GUJARAT.region_state:USM } s:STATE_GUJARAT.region_state:USM = { set_state_owner = c:TZ1 } }
201:                 if = { limit = { exists = s:STATE_CEYLON.region_state:USM } s:STATE_CEYLON.region_state:USM = { set_state_owner = c:TZ1 } }
202:                 if = { limit = { exists = s:STATE_INDIAN_OCEAN_TERRITORY.region_state:USM } s:STATE_INDIAN_OCEAN_TERRITORY.region_state:USM = { set_state_owner = c:TZ1 } }
203: 
204:                 s:STATE_CIRCARS = { nesnd_india_migrate_commission_case = yes }
205:                 s:STATE_KURNOOL = { nesnd_india_migrate_commission_case = yes }
206:                 s:STATE_MADRAS = { nesnd_india_migrate_commission_case = yes }
207:                 s:STATE_MYSORE = { nesnd_india_migrate_commission_case = yes }
208:                 s:STATE_TRAVANCORE = { nesnd_india_migrate_commission_case = yes }
209:                 s:STATE_GUJARAT = { nesnd_india_migrate_commission_case = yes }
210:                 set_variable = nesnd_tianzhu_commission_established
211:                 c:TZ1 = { if = { limit = { NOT = { has_journal_entry = nesnd_tianzhu_governance } } add_journal_entry = { type = nesnd_tianzhu_governance } } }
212:             }
213:             else = {
214:                 # Creation succeeded but the actual subject relationship failed. Only its seed may return.
215:                 if = { limit = { exists = s:STATE_MADRAS.region_state:TZ1 c:TZ1 = { num_states = 1 has_variable = nesnd_commission_created } }
216:                     s:STATE_MADRAS.region_state:TZ1 = { set_state_owner = c:USM }
217:                 }
218:             }
```

Lines 223–251:

```text
223: nesnd_establish_yuanshan_commission = {
224:     if = { limit = { nesnd_yuanshan_commission_ready = yes }
225:         set_variable = { name = nesnd_yuanshan_commission_cooldown months = 12 }
226:         create_country = { tag = YU1 origin = c:USM state = s:STATE_ZULULAND.region_state:USM on_created = {
227:                 set_country_type = colonial set_social_hierarchy = default_social_hierarchy set_variable = nesnd_commission_created
228:                 nesnd_commission_inherit_technology = yes copy_laws = c:USM
229:                 activate_law = law_type:law_presidential_republic activate_law = law_type:law_autocracy set_social_hierarchy = default_social_hierarchy
230:                 set_capital = STATE_ZULULAND
231:             }
232:         }
233:         if = { limit = { exists = c:YU1 }
234:             create_diplomatic_pact = { country = c:YU1 type = puppet }
235:             if = { limit = { c:YU1 = { is_subject_of = c:USM } }
236:                 if = { limit = { exists = s:STATE_CAPE_COLONY.region_state:USM } s:STATE_CAPE_COLONY.region_state:USM = { set_state_owner = c:YU1 } }
237:                 if = { limit = { exists = s:STATE_EASTERN_CAPE.region_state:USM } s:STATE_EASTERN_CAPE.region_state:USM = { set_state_owner = c:YU1 } }
238:                 if = { limit = { exists = s:STATE_NORTHERN_CAPE.region_state:USM } s:STATE_NORTHERN_CAPE.region_state:USM = { set_state_owner = c:YU1 } }
239:                 if = { limit = { exists = s:STATE_VRYSTAAT.region_state:USM } s:STATE_VRYSTAAT.region_state:USM = { set_state_owner = c:YU1 } }
240:                 if = { limit = { exists = s:STATE_TRANSVAAL.region_state:USM } s:STATE_TRANSVAAL.region_state:USM = { set_state_owner = c:YU1 } }
241: 
242:                 set_variable = nesnd_yuanshan_commission_established
243:                 c:YU1 = { if = { limit = { NOT = { has_journal_entry = nesnd_yuanshan_governance } } add_journal_entry = { type = nesnd_yuanshan_governance } } }
244:             }
245:             else = {
246:                 # Creation succeeded but the actual subject relationship failed. Only its seed may return.
247:                 if = { limit = { exists = s:STATE_ZULULAND.region_state:YU1 c:YU1 = { num_states = 1 has_variable = nesnd_commission_created } }
248:                     s:STATE_ZULULAND.region_state:YU1 = { set_state_owner = c:USM }
249:                 }
250:             }
251:         }
```

### M3: [west_south_asia_strategic_regions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/strategic_regions/west_south_asia_strategic_regions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/strategic_regions/west_south_asia_strategic_regions.txt`  
SHA-256: `da8efdef8673e2a0e06ebf7990f453c434256ecde34901c1a70b37d0debe4a04`

Lines 29–46:

```text
29: 	capital_province = x07104c
30: 	map_color = { 0.607 0.843 0.337 }
31: 	states = { STATE_CEYLON STATE_CIRCARS STATE_MYSORE STATE_TRAVANCORE STATE_MADRAS STATE_HYDERABAD STATE_KURNOOL STATE_BOMBAY }
32: }
33: 
34: region_himalayas = {
35: 	graphical_culture = "asian"
36: 	capital_province = x286514
37: 	map_color = { 177 207 205 }
38: 	states = { STATE_HIMALAYAS STATE_LHASA STATE_NGARI STATE_KASHMIR STATE_QINGHAI STATE_EASTERN_HIMALAYAS }
39: }
40: 
41: region_north_india = {
42: 	graphical_culture = "arabic"
43: 	capital_province = x13E50E
44: 	map_color = { 0.392 0.863 1 }
45: 	states = { STATE_GUJARAT STATE_SINDH STATE_CENTRAL_PROVINCES STATE_AWADH STATE_MALWA STATE_AGRA STATE_BUNDELKHAND STATE_BIHAR STATE_EAST_BENGAL STATE_WEST_BENGAL STATE_ASSAM STATE_ORISSA STATE_PUNJAB STATE_HILL_PUNJAB STATE_DELHI STATE_RAJPUTANA }
46: }
```

### M4: [00_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt`  
SHA-256: `a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`

Lines 4174–4201:

```text
4174: 	s:STATE_MYSORE = {
4175: 		create_state = {
4176: 			country = c:USM
4177: 			owned_provinces = { x189045 xD0F0A0 xE5A1AC x2A60B3 xB4ABD5 x903060 x8E3C9D x102D8B x25CBCC xBFDC26 xA26314 x16AA78 x9FE13F x1B7225 xEDFC06 x696049 }
4178: 		}
4179: 		# create_state = {
4180: 		# 	country = c:MUG
4181: 		# 	owned_provinces = { x189045 xD0F0A0 }
4182: 		# }
4183: 
4184: 		add_homeland = cu:kannada
4185: 	    add_homeland = cu:deccani
4186: 	}
4187: 	s:STATE_TRAVANCORE = {
4188: 		create_state = {
4189: 			country = c:TRA
4190: 			owned_provinces = { xEC8405 x2121D0 xFD0A78 xA11A79 x21A0D0 }
4191: 		}
4192: 		create_state = {
4193: 			country = c:USM
4194: 			owned_provinces = { xA0A050 xB0934C xCCDC34 }
4195: 		}
4196: 		create_state = {
4197: 			country = c:COC
4198: 			owned_provinces = { xE4EB67 }
4199: 		}
4200: 
4201: 		add_homeland = cu:malayalam
```

Lines 9329–9346:

```text
9329: 	}
9330: 
9331: 	s:STATE_KURNOOL = {
9332: 	    create_state = {
9333: 	    	country = c:USM
9334: 	    	owned_provinces = { x063403 x0F1912 x338BFB x34BB3B x35AB0E x461A00 x5170A0 x54D463 x59BBE1 x669373 xF2F82A xF46AEC  }
9335: 			state_type = unincorporated
9336: 		}
9337: 	    create_state = {
9338: 	    	country = c:KNO
9339: 	    	owned_provinces = { x84EE56 xF91482 }
9340: 		}
9341: 
9342: 	    add_homeland = cu:telegu
9343: 	    add_homeland = cu:kannada
9344: 	    add_homeland = cu:deccani
9345: 	}
9346: 
```

### M5: [ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt`  
SHA-256: `78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7`

Lines 134–149:

```text
134: 		}
135: 
136: 		# India Imperium
137: 		if = {
138: 			limit = { exists = c:MYS }
139: 			create_diplomatic_pact = {
140: 				country = c:MYS
141: 				type = puppet
142: 			}
143: 		}
144: 		create_diplomatic_pact = {
145: 			country = c:TRA
146: 			type = puppet
147: 		}
148: 	}
149: 	c:DEI ?= {
```

Lines 184–198:

```text
184: 
185: 	c:FRA ?= {
186: 		create_diplomatic_pact = {
187: 			country = c:FRM
188: 			type = protectorate
189: 		}
190: 		create_diplomatic_pact = {
191: 			country = c:LOM
192: 			type = protectorate
193: 		}
194: 		create_diplomatic_pact = {
195: 			country = c:MUG
196: 			type = tributary
197: 		}
198: 		create_diplomatic_pact = {
```

### M6: [USM - UnitedStatesOfMing.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/USM - UnitedStatesOfMing.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/USM - UnitedStatesOfMing.txt`  
SHA-256: `66ed33016dbc23ecafcb5e7ac91e21c0a3e5fbd547b61a126a1d6c64872b7bc4`

Lines 1–28:

```text
1: COUNTRIES = {
2: 	c:USM ?= {
3: 		set_market_capital = STATE_ZHEJIANG
4: 
5: 		add_era_researched = era_1
6: 		effect_starting_politics_conservative = yes
7: 		# Economic
8: 		add_technology_researched = railways
9: 		add_technology_researched = intensive_agriculture
10: 		add_technology_researched = mechanical_tools
11: 		add_technology_researched = atmospheric_engine
12: 
13: 		# Military	
14: 		add_technology_researched = screw_frigate
15: 		add_technology_researched = general_staff
16: 		add_technology_researched = percussion_cap
17: 		add_technology_researched = power_of_the_purse
18: 
19: 		# Cultural
20: 		add_technology_researched = dialectics
21: 		add_technology_researched = central_archives
22: 		add_technology_researched = central_banking
23: 		add_technology_researched = egalitarianism
24: 		add_technology_researched = corporate_charters
25: 
26: 		add_technology_researched = law_enforcement
27: 		add_technology_researched = sericulture
28: 		add_technology_researched = international_trade
```

### M7: [nesnd_india_core.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt`  
SHA-256: `6dd70c0df3720983dc3cd13d35b248df963ac9db1d82fb90bd729778f4f3aaec`

Lines 1–4:

```text
1: nesnd_india_state = { OR = { region = sr:region_north_india region = sr:region_south_india } }
2: nesnd_india_country = { is_country_alive = yes NOT = { is_country_type = decentralized } any_scope_state = { nesnd_india_state = yes state_population > 0 } }
3: nesnd_india_empire = { nesnd_india_country = yes OR = { c:MUG ?= this c:BHT ?= this c:DRA ?= this has_variable = nesnd_india_imperial_line } }
4: nesnd_india_prince = { nesnd_india_country = yes NOT = { nesnd_india_empire = yes } OR = { c:ALW ?= this c:ASM ?= this c:AWA ?= this c:BAG ?= this c:BAS ?= this c:BER ?= this c:BHO ?= this c:BHV ?= this c:BHW ?= this c:BIK ?= this c:BUN ?= this c:COC ?= this c:COO ?= this c:DHA ?= this c:GAR ?= this c:GWA ?= this c:HYD ?= this c:IDA ?= this c:IND ?= this c:JAI ?= this c:JAS ?= this c:JEY ?= this c:JHN ?= this c:JOD ?= this c:JUN ?= this c:KHP ?= this c:KNO ?= this c:KOT ?= this c:KUT ?= this c:MEW ?= this c:MNP ?= this c:MYB ?= this c:NAG ?= this c:NAR ?= this c:NAW ?= this c:PAN ?= this c:PLP ?= this c:PTA ?= this c:PTN ?= this c:SAT ?= this c:SIN ?= this c:SUR ?= this c:TRA ?= this has_variable = nesnd_india_local_state } }
```

### M8: [nesnd_commissions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/nesnd_commissions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/nesnd_commissions.txt`  
SHA-256: `90ae174bc3ae3e52c02f109d6a690dbefe42a24a2a10103f926f8255d49b5e62`

Lines 1–2:

```text
1: TZ1 = { color = { 118 93 154 } country_type = colonial tier = principality cultures = { ce_wuu min } religion = confucian capital = STATE_MADRAS social_hierarchy = british_indian_caste_system }
2: YU1 = { color = { 135 104 69 } country_type = colonial tier = principality cultures = { ce_wuu min } religion = confucian capital = STATE_ZULULAND  }
```

### M9: [nesnd_commissions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/decisions/nesnd_commissions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/decisions/nesnd_commissions.txt`  
SHA-256: `f8158c00425c4fdfbb56ef99d8a77b3be18b6cbc7bbb09233fda2a291f41eba3`

Lines 1–2:

```text
1: nesnd_establish_tianzhu = { is_shown = { nesnd_tianzhu_commission_available = yes } possible = { nesnd_tianzhu_commission_ready = yes } when_taken = { custom_tooltip = nesnd_establish_tianzhu_tt hidden_effect = { nesnd_establish_tianzhu_commission = yes } } ai_chance = { value = 5 } }
2: nesnd_establish_yuanshan = { is_shown = { nesnd_yuanshan_commission_available = yes } possible = { nesnd_yuanshan_commission_ready = yes } when_taken = { custom_tooltip = nesnd_establish_yuanshan_tt hidden_effect = { nesnd_establish_yuanshan_commission = yes } } ai_chance = { value = 5 } }
```

### M10: [nesnd_commissions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_commissions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_commissions.txt`  
SHA-256: `82ba94000fa6d6ccbd7ce7bfb01e13f81aebfb1b6c3d07a9861047075cc4c10c`

Lines 1–10:

```text
1: nesnd_establish_tianzhu_button = { name = nesnd_establish_tianzhu desc = nesnd_establish_tianzhu_desc
2:     visible = { nesnd_tianzhu_commission_available = yes } possible = { nesnd_tianzhu_commission_ready = yes }
3:     ai_chance = { value = 5 }
4:     effect = { custom_tooltip = nesnd_establish_tianzhu_tt hidden_effect = { nesnd_establish_tianzhu_commission = yes } }
5: }
6: nesnd_establish_yuanshan_button = { name = nesnd_establish_yuanshan desc = nesnd_establish_yuanshan_desc
7:     visible = { nesnd_yuanshan_commission_available = yes } possible = { nesnd_yuanshan_commission_ready = yes }
8:     ai_chance = { value = 5 }
9:     effect = { custom_tooltip = nesnd_establish_yuanshan_tt hidden_effect = { nesnd_establish_yuanshan_commission = yes } }
10: }
```

### M11: [nesnd_commissions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_commissions.txt>)

Path: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_commissions.txt`  
SHA-256: `957be9ccc4156c41c732fa8b7c0d4e089d2fd89ae82be5afa86135da068e5704`

Lines 1–8:

```text
1: nesnd_tianzhu_commission = { icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content
2:     is_shown_when_inactive = { nesnd_tianzhu_commission_available = yes any_scope_state = { nesnd_tianzhu_region = yes } }
3:     possible = { nesnd_tianzhu_commission_available = yes any_scope_state = { nesnd_tianzhu_region = yes } }
4:     scripted_button = nesnd_establish_tianzhu_button
5:     complete = { has_variable = nesnd_tianzhu_commission_established }
6:     invalid = { OR = { NOT = { c:USM ?= this } NOT = { any_scope_state = { nesnd_tianzhu_region = yes } } } }
7:     weight = 500
8: }
```

Lines 28–35:

```text
28: nesnd_yuanshan_commission = { icon = "gfx/interface/icons/event_icons/event_newspaper.dds" group = je_group_historical_content
29:     is_shown_when_inactive = { nesnd_yuanshan_commission_available = yes any_scope_state = { nesnd_yuanshan_region = yes } }
30:     possible = { nesnd_yuanshan_commission_available = yes any_scope_state = { nesnd_yuanshan_region = yes } }
31:     scripted_button = nesnd_establish_yuanshan_button
32:     complete = { has_variable = nesnd_yuanshan_commission_established }
33:     invalid = { OR = { NOT = { c:USM ?= this } NOT = { any_scope_state = { nesnd_yuanshan_region = yes } } } }
34:     weight = 500
35: }
```

