# Batch B repair plan — current1.13 military supply and claim scopes

Status: REPAIR_PLAN_ONLY. No gameplay edits or tests during this research phase. The organizer must approve the supply choice before implementation. GAME1.13.11/build24799966; C=WORK/exports/canon-route-execution-20261104-a. Main MOD/GAME/other mods remain read-only.

## Recommendation

Apply `unit_supply_consumption_mult` directly to the three existing **country** military-reform modifiers: ongoing−.20, Tanzimat success−.25, failure−.15. This matches the actual native Paraguay event and the current1.13 unit/ship separation. It changes maintenance-goods quantity, not monetary goods cost. It covers the native battalion system, **including marine battalions**, while fleet ships use a separate ship/materiel/upkeep system.

This is a current-source-supported interpretation, not a live-engine measurement. The old building-target version is unsupported and must be removed; the native tooltip cannot rescue it. The remaining engine observation would be actual army goods-order change and unchanged ship upkeep with a fixed country/army/fleet snapshot. No game launch is authorized in this task.

## Current military data and complete source chain

G=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`; D=`WORK/references/engine-docs-1.13.11-20261031`. Exact hashes: `batch-b-repair-source-hashes.json`. Read-only resolved inventory, including candidate overlays: `batch-b-military-source-inventory.json`.

| Evidence | Actual current source | Consequence |
|---|---|---|
| Native quantity reward executes on country | G/events/brazil/paraguay.txt:483–515: country_event paraguay.6, optiona calls add_modifier directly in country scope | Country scope has an actual executed native analogue |
| Reward definition | G/common/static_modifiers/brazil_2_modifiers.txt:314–317 sets unit_supply_consumption_mult=−.5 | Same quantity interface, without substituting monetary cost |
| Caller and misleading preview | G/common/scripted_buttons/03_paraguay_scripted_buttons.txt:234–250 triggers paraguay.6; only show_as_tooltip descends to a barracks | Building fragment is preview only; it is not execution evidence |
| General and army-order usage | G/common/character_traits/skill_traits.txt:4–15 is a general-only resupply trait; G/common/commander_orders/00_defend.txt:30–51 is military_type=army and uses unit_supply_consumption_mult | The modifier belongs to the battalion/army maintenance chain |
| Country-wide prosperity usage | G/common/company_types/99_basic_companies.txt:1278–1281; 00_companies_ip4.txt:826–830 | Current native country reward fields use the same supply modifier |
| Native unit meaning | G/localization/english/concepts_l_english.yml:920–925 defines military units as battalions operating under generals; :503–507 defines armies as land formations | “Unit” here is the battalion model, not a current fleet ship |
| All effective combat-unit types | G/common/combat_unit_types/00_land_combat_unit_types.txt:10ff; no C override in this database |19types:6 infantry,5 artillery,5 cavalry,3 marines; no ship type is in this database |
| Unit goods quantity | Same file:83–92 line infantry upkeep_modifier has small_arms1; :144–154 skirmish infantry has small_arms2/ammunition1; :953–1030 marines also have upkeep goods | These are per-unit material requirements; marines remain within the unit model |
| Recruitment buildings | G/common/buildings/05_military.txt:3–21 and28–45 set recruits_combat_units=yes for barracks/conscription, using training PMGs | Buildings recruit battalions; their PMs are not a substitute for the unit upkeep model |
| Recruitment PMs | G/common/production_methods/05_military.txt:1–233: professions and training-rate modifiers | A building goods-input replacement lacks demonstrated equivalence to current unit upkeep and is not the chosen repair |
| New navy system | G/common/ship_types/ship_types.md:4–11;00_ship_types.txt:2–52,94–144 |21effective ship types, separate ship groups and construction_goods/materiel_goods; ships are not combat_unit_types |
| Ship upkeep formula | G/common/defines/00_defines.txt:884–887 uses SHIP_MAINTENANCE_GOODS_TO_CONSTRUCTION_GOODS_FACTOR, SHIP_UPKEEP_GOODS_TO_CONSTRUCTION_GOODS_FACTOR and docked multiplier | Naval upkeep has its own construction-derived goods mechanism |
| Sailor recruitment | G/common/buildings/05_military.txt:99–119 uses recruits_sailors=yes; defines:877–878 defines sailors per naval assignment/building | Naval administration supplies sailors, rather than battalions using the old naval-base unit path |
| Separate modifier masks | D/modifiers.log:2107–2110 unit_supply_consumption_mult has unit mask; :1579–1594 ship_supply_capacity/efficiency have ship mask | No basis to make a building carry this unit modifier; separate ship mask reinforces the battalion-vs-ship boundary |
| Cost is different from quantity | G/localization/english/modifiers_l_english.yml:72–73 and2945–2946 explicitly describe military/navy goods-cost modifiers as monetary; :3256–3257 describes unit supply by goods quantity | Do not use country_military_goods_cost_mult or country_navy_goods_cost_mult as a replacement |
| Separate UI objects | G/gui/military_panel_formations.gui:281 uses MilitaryFormation.GetGoodsConsumptionCostRaw; G/gui/ship_panel.gui:1667–1673 uses Ship.GetUpkeepCost | Further evidence of distinct army formation and ship accounting, not runtime proof |

The inventory count is source extraction, not a behavior test. All19 combat-unit types and21 ship types resolve to current GAME definitions; C adds no combat-unit-type or ship-type override. Marine battalions are explicitly included in the proposed country modifier's scope. If the intended design excludes marines as well as ships, this exact native interface is broader than that narrower interpretation and must be reconsidered rather than silently relabeled.

## Why the alternatives are rejected

- Keep the building modifier: rejected by the frozen Tiger flow analysis and unsupported by the actual native event. Generic add_modifier accepting buildings is not proof that a unit-mask modifier flows through them.
- Put goods_input_*_mult on barracks: the actual current goods are declared in unit-type upkeep_modifier, while the barracks PMs mainly provide personnel/training. No demonstrated native chain establishes identical quantity behavior for all battalion types, mobilization options and recruitment forms. Do not substitute this without new evidence.
- Cut country_military_goods_cost_mult: explicitly monetary, so it violates the goods-quantity requirement.
- Change ship_supply_efficiency: separate naval supply behavior and outside the requested army reform.

## Bounded implementation after approval

1. **Claim predicate.** Replace state_region `NOT={has_claim_by=c:TUR}` with guarded TUR country `NOT={has_claim=prev}`. Keep the same state_region as prev and preserve `NOT={owns_entire_state_region=prev}` plus existing foreign-owner/independent-EGY conditions. Explicitly reject missing/dead TUR before entering country scope. Engine triggers.log:10141–10145 supports country has_claim targeting state/state_region/country; :10147–10155 proves has_claim_by is state-only. No geographical claim list, cost25 or postcondition changes.
2. **National supply reward.** Add unit_supply_consumption_mult=−.20/−.25/−.15 to `nesnd_ottoman_qin_reform`, `_success`, `_failed` respectively. Keep Armed Forces attraction/strength and army offense/defense amounts unchanged. The selected reform tier remains fixed for its12-month term.
3. **Retire broken building attachment.** Change the existing barracks refresh helper into cleanup-only behavior with has_modifier guards for each of the three legacy supply modifiers. Remove every branch that attaches those modifiers. Retain the three old modifier definitions as inert compatibility shells until their saved references are cleared. Stop new-building/state-created supply attachment hooks; country rewards naturally cover newly recruited units without those loops. Retain a narrow cleanup pass for legacy modifiers on transferred/loaded buildings and existing contract cleanup call sites. No currently existing map buildings are created, deleted or converted.
4. **Twelve-month lifecycle.** Keep national months12, pending marker, term marker, delayed hidden cleanup and weekly fallback guards. Since supply is now on the same national timed modifier, it expires with the offense/defense/reform benefits rather than lingering in a separate two-month building refresh. Old callbacks still require pending plus absent term, so a new term protects renewed rewards. Tag invalidation clears all national alternatives while retaining the original commitment marker to its own deadline.
5. **UI/text.** Country native modifier preview now displays the supply amount itself. Remove the three redundant custom supply-amount tooltip calls; do not promise a building modifier. If an explanatory scope line is retained, it says the reform covers battalions including marines; no development term such as “native” or propagation detail in player prose. Keep the actual quantity reward and12-month duration. Update zh/en comparison record and final effective keys.
6. **Encoding.** Add UTF-8 BOM to the21 txt files in the original aggregate warning, preserving exact text/newline content other than authorized repairs. Include the previously unchanged recovery trigger/value/modifier/bar dependencies in the new frozen manifest when BOM or logic changes their hashes. No blanket whole-MOD rewrite.

Owned repair files: `common/scripted_triggers/nesnd_ottoman_recovery.txt`; `common/static_modifiers/nesnd_ottoman_recovery.txt`; `common/scripted_effects/nesnd_ottoman_recovery.txt`; `common/on_actions/nesnd_ottoman_recovery.txt`; `common/scripted_buttons/nesnd_ottoman_recovery.txt`; dedicated B zh/en localization as necessary; and the explicit21 BOM targets. Claim-button file retains its72 target/effect definitions. Core unity equations/policy costs/primary-radical arithmetic are unchanged.

## Evidence preservation and later retest

The original failed150-warning evidence, first freeze, test snapshot manifest, AST/MCP results, source contract, implementation and writing records are preserved in `batch-b-first-freeze-evidence/`. The original independent test snapshot remains unchanged. No current result will be rewritten as if the first implementation passed.

After approved edits: finish code/text/source record, freeze all changed files plus dependencies, stop editing, then obtain test-phase authorization. Create a **new** independent snapshot path for the repair; do not edit the first snapshot. Retest the real AST for country-scope claim checks, missing/dead TUR, foreign/EGY/own/already-claimed regions,72-target/cost preservation, national supply coefficients/all3tiers, no remaining building attachments, inert-shell cleanup,12-month renewal/callback safety and legal/group arithmetic. Negative controls must catch the original invalid has_claim_by scope and original building-to-unit flow. Run MCP source queries and Tiger baseline/repair snapshot sequentially, preserving the first150 diagnostics for comparison. Complete deferred bar-sum/mutation coverage only after that freeze.

Acceptance target: source repairs remove146 claim-scope warnings,3 supply-flow warnings and the1 aggregate BOM warning without muting the checker or changing unrelated gameplay. Actual army goods-order changes, unchanged fleet-ship upkeep and timer/UI behavior still require an authorized engine observation; no STATIC_PASS result can certify those runtime outcomes.

Organizer decision: approve the country-level battalion supply reward (including marine battalions, excluding the separate ship system) and the bounded repairs above, or specify a narrower desired scope before edits begin.
