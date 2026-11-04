# Batch B implementation plan: culture unity, common identity and Ottoman expansion

Status: PLAN_ONLY — awaiting organizer approval. No gameplay edits, new tests, or game launch have been performed for Batch B. Author: canon_current_spec / Batch B implementation agent. 2026-11-04.

## Scope and source objects

WORK=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`; C=`WORK/exports/canon-route-execution-20261104-a`; B=`WORK/backups/pre-change-canon-route-execution-20261104T080559Z/mod`; GAME=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`. Fixed parent remains b94582ecec7b0b6dd5620a184658190157fc1729. Only C gameplay files will be edited after approval. GAME, B, main MOD, workshop and author samples remain read-only. Installed source is 1.13.11/build24799966; catalog CURRENT, unchanged in this session.

This plan consumes `steer-implementation-ledger.md`, `unity-inventory-and-native-contract.md` (49 fingerprinted sources), NESND, engineering adaptation, player-writing, numeric-scale, journal-system-design, journal-text-contract and political-design-and-difficulty instructions. It does not supersede country work assigned to A/C or the organizer.

## Existing systems and exact integration points

| Country/system | Eligible owner and current behavior | B changes |
|---|---|---|
| QE1 / nesnd_qe1_unity_journal | Living QE1, not dissolved; starts 70, 0–100; sole writer nesnd_qe1_unity_monthly | Add two buttons, two independently named monthly policy terms; split law contribution into three law groups; preserve existing conversion, uprising and other arithmetic |
| JAP/JTK/JIM / nesnd_jp_cohesion | Exact living tags, including later unification survivors; starts 70; statistics-ready guard | Same policy pair and monthly terms; no existing direct law term, so do not invent one |
| MUG/BHT/DRA or retained imperial_line / nesnd_india_society | Populated India territory, centralized, imperial identity, reform_done, nationalism; actual common identity starts 25 | Pair affects common identity only; split citizenship from unrest, identify distribution-of-power row by actual law-group name; dynasty receives no policy growth |
| TUR / new nesnd_ottoman_unity | First unlock at 36 directly owned state objects; opening source count 27 | Persistent 0–100 unity, weighted culture shares, economics/laws/war/victory/expansion, shared pair and non-destructive low-unity pressure |

Source anchors in C: `common/journal_entries/nesnd_qe1_identity.txt:1–25`, `common/script_values/nesnd_qe1_identity.txt:8–42`, `common/scripted_effects/nesnd_qe1_identity.txt:5–34`; `common/journal_entries/nesnd_jp_cohesion.txt:1–21`, `common/script_values/nesnd_jp_development.txt:9–69`; `common/journal_entries/nesnd_india_core.txt:39–52`, `common/scripted_triggers/nesnd_india_core.txt:1–3,25`, `common/script_values/nesnd_india_core.txt:1–10`, `common/scripted_progress_bars/nesnd_india_core.txt:7–18`.

Inventory boundary: Japanese territorial reunification (`nesnd_japan_unity_score`) is not culture unity. French republican unity is a political modifier/objective, not an analogous cultural stock. Neither gets these buttons. Ordinary Indian princes and foreign owners of Indian land do not automatically acquire imperial common identity.

## Native complete chains and interface constraints

- Money: GAME `common/journal_entries/04_indian_famines.txt:1–8` binds `common/scripted_buttons/04_indian_famines_buttons.txt:20–28`, applying a 12-month country expense modifier; `common/static_modifiers/00_ip2_02_modifiers.txt:39–42` defines `country_expenses_add=1`; `common/modifier_type_definitions/00_modifier_types.txt:481–488` defines currency output; `common/script_values/event_values.txt:69–75` supplies GDP-scaled multiplier syntax. Its comment disagrees with its arithmetic: use the real formula, not its comment.
- Assimilation: GAME `common/journal_entries/06_philippines_je.txt:182` → `common/scripted_buttons/06_philippines_buttons.txt:4–48` → `events/iberia_events/philippines_events.txt:342,376–383` → `common/static_modifiers/00_ip4_03_modifiers.txt:18–22`: a country-applied `state_assimilation_mult=.1` is native +10% population assimilation. It is not state incorporation and does not multiply the Qin/Japan scripted pop-conversion amounts.
- Political cost: `country_legitimacy_base_add=-10`, GAME modifier definitions :979–985, is ten points. Primary-only radical-sensitivity modifier is not supported by inspected native definitions. GAME `events/balkans_events/subjecthood_events.txt:148–155` demonstrates `every_primary_culture` → country `add_radicals` filtered to that culture. Engine effects.log :367–380 defines fractional movement. We use explicit monthly 0.001 movement, not a falsely named sensitivity modifier.
- Culture shares: engine triggers.log :9546–9556 `culture_percent_country`, :10277–10287 culture traits; GAME `common/script_values/ip4_je_values.txt:516–519`, C `common/script_values/nesnd_qe1_heritages.txt:3–11`. Country→culture→prev-country formula, guarded total_population>0; no country use of state-only population_by_culture.
- Acquisition/victory: GAME `common/on_actions/00_code_on_actions.txt:6230–6234` on_wargoal_enforced ROOT is beneficiary country; :7131–7185 owner-change/state-created ROOT is state. on_war_end ROOT is diplomatic play and actor is not necessarily winner; we will not mistake it for a winner-country callback.
- Army quantities: GAME `common/scripted_buttons/03_paraguay_scripted_buttons.txt:239–250` applies `barracks_boost_paraguay_quantity_modifier` to a barracks; `common/static_modifiers/brazil_2_modifiers.txt:314–317` uses `unit_supply_consumption_mult=-.5`. Engine modifiers.log :2107–2110 defines maintenance goods quantity. The building-scoped fragment is inside show_as_tooltip, not actual execution. The actual paraguay.6 option applies the modifier to the country. Engine effects.log:312–314 allows add_modifier on a building, while modifiers.log:2107–2110 identifies the unit mask and maintenance-goods semantics. These facts permit the scripted target shape but do not prove runtime propagation from a building to its units. TUR building→unit behavior remains ENGINE_NOT_RUN; country_military_goods_cost_mult is a different cost mechanic.
- Timers: engine effects.log :37336–37340 explicitly allows trigger_event with days/weeks/months/years. A guarded hidden country cleanup event delayed months=12 can close the TUR military contract without a recurring two-month building modifier outlasting the national commitment.

## Shared 12-month policies

Names in player UI: “补贴落后人群” / “补贴政治存在”; English proposals “Subsidize Disadvantaged Communities” / “Support Political Representation”. Final prose will be compared with author samples before landing.

| Policy | Monthly unity/common-identity | National effect for 12 months | Cost |
|---|---:|---|---|
| Material subsidy | +0.50 | population assimilation +10% | Weekly expense frozen from GDP at activation; once each monthly country pulse move 0.1% of each current primary-culture pop toward radicalism, at most 12 pulses |
| Political-presence subsidy | +0.50 | population assimilation +10% | legitimacy −10 points |

Material weekly expense uses the native medium-cost arithmetic: `max(100, round(GDP / 100000 * .25) * 100)`. Before rounding/floor this is 0.025% of annual GDP per week, approximately 1.3% of GDP over 52 weeks. GDP 10m gives £2,500/week; GDP 100m gives £25,000/week. These are source-derived design estimates, not measured budgets. Money lives in a dedicated `country_expenses_add=1` modifier with the cost multiplier; assimilation must be in a separate modifier so the currency multiplier cannot multiply assimilation. Store the quoted expense at execution and use the same formula for preview.

Both policies can coexist: +1.00/month and +20% natural assimilation, with both costs. One policy contributes at most +6 unity over twelve consumed monthly pulses; two at most +12 before the stock's 100 cap and other terms. Material radical movement is bounded at 12×0.001 attempted fractional movements under fixed population, not a promise of +1.2 percentage points net radicals.

Player finance policy: native recurring expenses can use credit; do not add an unrequested gold-reserve or bankruptcy prohibition. At zero cash/negative balance the expense still exists and can deepen deficit—there is no free activation or refund. AI affordability is separate: favor material subsidy below unity 50 with positive net_fixed_income sufficient to cover the quoted expense; political policy below 50 with legitimacy at least 40, using native script-value ai_chance (`value/if/add`). These AI checks are not player gates.

Lifecycle:

1. `possible` and hidden execution both require the live owning system and absence of that policy's timed active marker and modifiers. Same type cannot stack, refresh, or restart early. There is no cancel action.
2. Country timed modifiers and active marker last 12 months. Losing a JE, temporary threshold loss, political change or eligible tag change does not refund/clear the contract. The surviving country object continues to pay; the marker and cost are not stored only in a JE.
3. A single dedicated `on_monthly_pulse_country` callback handles material radicals. It re-enumerates current primary cultures, saves the country explicitly, applies culture-filtered add_radicals=.001, increments a guarded 0–12 counter and uses a one-day pulse lock to prevent accidental duplicate same-day callbacks. Neither JE nor progress bar applies radicals.
4. Each existing JE retains its single actual stock writer and absolute bar sync; its delta consumes the shared policy values only while that system is live. Expired/invalid systems have zero growth. The shared callback does not also add unity.
5. Expiry permits a new activation and resets only that new contract's counter/quote. Stale JE reinitialization never resets an active policy. Dead countries have no living national budget; annexers do not inherit the commitment by script. Same-object tag changes retain it.
6. Preview shows real timed modifiers plus one concise custom tooltip for monthly unity and the targeted discrete political cost. Missing variables have safe zero/default values. No tooltip dereferences a temporary scope established only during execution.

## Law contributions: one row per actual law group

The new user requirement changes presentation granularity without changing existing law arithmetic.

| System | Separate native bar rows | Formula preserved / introduced |
|---|---|---|
| Qin | `$lawgroup_citizenship$`; `$lawgroup_church_and_state$`; `$lawgroup_army_model$` | Citizenship: multicultural +.15, national supremacy −.25, racial segregation −.10, else0. Religion: total separation +.10, conscience +.05, else0. Army: wartime mass conscription −.20, else0 |
| Japan | No law row currently exists | Retain current order/living/learning/conflict/victory terms; do not manufacture legal effects |
| India common identity | `$lawgroup_distribution_of_power$`; `$lawgroup_citizenship$`; separate “社会动荡” | Distribution: not autocracy/oligarchy +.5. Citizenship: ethnostate −.5. Turmoil>25% −.5 stays its own non-law row |
| India dynasty (adjacent UI audit) | Existing religion-only row named `$lawgroup_church_and_state$` | Keep its own ±.25 religious-law arithmetic; no policy delta on dynasty |
| TUR | `$lawgroup_citizenship$`; `$lawgroup_church_and_state$`; `$lawgroup_army_model$` | Use the specified Qin-shaped three contributions above, as explicit new TUR balance |

Use one script value per group; if/else_if may distinguish laws within that group. No generic “法律影响” row remains on these unity bars. Qin's aggregate helper can remain as an internal sum if referenced, but UI lists the three components and actual delta sums them exactly once. India's mixed unrest helper will become pure turmoil with citizenship separate. Institution investment is not an active-law-group check and keeps its institution/economic label. Reuse actual localized group names; GAME simp_chinese laws localization :374,396,467,482 confirms them.

## Ottoman expansion and reform completion

Expansion JE stays open for any living TUR, independent of Tanzimat success. Native `common/journal_entries/00_sick_man.txt:23,44–56,79–85` gives timeout10950days, four goals, timed failed_tanzimat and permanent failed_sick_man_main with full DLC. Both success and failure events set sick_man_complete (`events/sick_man_events.txt`, success immediate; failure:195–201). Therefore success requires complete+goals>=4+no permanent failure; failure includes permanent failure or completed without success; otherwise ongoing. Expired failed_tanzimat must not turn failure into success.

Keep the current three chosen reward scales:

| Result | Base enthusiasm/month | 12-month military goods quantity | Armed Forces attraction/strength | Army offense/defense |
|---|---:|---:|---:|---:|
| Successful | +2 | −25% | +20%/+20% | +15%/+15% |
| Ongoing | +1 | −20% | +15%/+15% | +10%/+10% |
| Failed | +.75 | −15% | +10%/+10% | +5%/+5% |

Other enthusiasm terms remain army>=100 +.5; Armed Forces in government and legitimacy>=50 +.5; active military reform −.5. Existing 25 enthusiasm/state-claim purchase remains. UI gives the reform-outcome base a clear name/status and keeps army/government/reform distinct.

Fix all three national-modifier cleanup branches, supply cleanup for lost/new states/buildings, and native scripted-button AI syntax. A military contract gets a persistent pending marker and one delayed hidden cleanup event at 12 months. Pending blocks renewal until cleanup, so an old callback cannot clear a newly renewed contract on the same date. Cleanup removes all three national alternatives before refreshing buildings; expiry or tag invalidation clears all relevant supply variants. New buildings acquire only the currently chosen national tier. The selected tier stays fixed for its 12-month commitment even if Tanzimat resolves meanwhile; next contract uses the new result. This preserves a reviewable fixed-duration contract.

## Ottoman unity lifecycle and arithmetic

First entry: living TUR directly owns at least36 states (`num_states`, no subjects). Persist `nesnd_ottoman_unity_opened`; initialize unity70, war_months0 and prior-SoL snapshot only if missing. Old saves already beyond36 initialize once. Existing stock survives missing JE/reload. Initialization does not add its own JE recursively.

After first entry: remain active at27 or more direct states. Below27, pause/archive the JE while preserving opened marker, unity, current policy commitments and eligible future re-entry. Regaining27 reopens with previous unity, not70. At27–35 before first unlock there is no JE. Identity loss/cessation invalidates; strip only TUR-owned dynamic high/low unity modifiers, never shared fixed commitments. Returning TUR may resume its same-object record. This 36-entry/27-resume hysteresis prevents conquest/release loops from resetting unity.

Culture-share groups are disjoint. Check exact Turkish first (zero); then Arab/Berber/Afro-Arab; Han; African group excluding higher groups; East/South/West Slavic; all remaining cultures. No invented geographic trait. Every share is population-weighted via actual culture_percent_country, guarded live country and total_population>0 and clamped0..1. For a zero-population country all buckets, including fallback, return0.

Monthly cultural burden in unity points:

`B = −1.20*A −0.90*H −0.60*F −0.35*S −0.15*O`, where shares refer to total population and Turkish has coefficient0. Arab includes `heritage_arab`, `heritage_berber`, and explicit `heritage_afro_arab`; Han includes MOD Han heritage cultures. African-medium excludes Arab/Afro-Arab; Slavic uses heritage_east_slavic/south_slavic/west_slavic. Display each weighted bucket in a named bar row, not one unexplained diversity number.

Proposed remaining monthly terms (points, source-estimated balance):

| Term | Value |
|---|---|
| Administrative continuity | +.15 |
| Government legitimacy | >=50:+.15; <25:−.30; otherwise0 |
| Bureaucracy | >=0:+.10; <0:−.40 |
| Schools | >=1:+.05; >=2:+.05; >=3:+.05; >=4:+.05, cumulative |
| Living-standard change | monthly>=+.05:+.40; <=−.05:−.60; otherwise0 |
| Declared-bankruptcy modifier | −1.00 while present |
| Citizenship, church/state, army laws | Three explicit group rows, as above |
| Sustained war | −.20 during war; additional−.30 from12 continuous months; additional−.30 from24; reset counter at peace |
| Recent enforced military goal | +.15/month for24months, country cooldown12months prevents multiple wargoals stacking; source text describes victory, not every on_war_end |
| Recent territorial acquisition | +.10/month for12months, shared12month acquisition cooldown; owner-change and state-created consume the same guard |
| Each active shared subsidy | +.50 |

`U_next=clamp(U+sum(all displayed terms),0,100)`. One JE monthly callback samples current shares/SoL, advances the sustained-war counter, updates U and absolutely synchronizes its native bar. New statistics initialize to zero change, not an artificial economic jump. Acquisitions use actual new owner scope and live-game guard; callbacks also check entry threshold before marking. Peaceful acquisition counts as expansion; duplicate callbacks do not stack. Subject acquisitions do not count. Broad war-end events do not generate victory rewards.

Consequence proposal: below25 apply a reversible low-unity national modifier (legitimacy−5, turmoil-effects+10%, matching Japanese low-cohesion severity); at75 or more apply natural assimilation+5%. The two are mutually exclusive, refreshed only while TUR unity is active, removed promptly on band exit/pause/tag loss. At0 the low-unity consequence continues; no scripted Qin breakup, coerced culture/religion conversion, new forced secession, or resurrection. At100 no one-time reward that can be farmed. Endogenous unrest remains the gameplay pressure. This provides consequences and recovery without copying Qin's authored catastrophe.

Scale examples: at100% of a single non-Turkish category, culture burden is respectively−1.20/−.90/−.60/−.35/−.15; at100% Turkish it is0. Mixed shares T=.5,A=.2,H=.1,F=.1,S=.05,O=.05 give B=−.415. Under ordinary +.15 continuity,+.15 legitimacy,+.10 bureaucracy,+.10 schooling and neutral other terms, net is+.085/month; both policies make it+1.085 before their political consequences. A24-month war subtracts.80; bankruptcy another1.00; meaningful economic/legal intervention remains necessary.

## Owned files and collaboration boundary

New C files:

- `common/{scripted_buttons,scripted_effects,scripted_triggers,script_values,on_actions,static_modifiers}/nesnd_unity_policies.txt`.
- `common/{journal_entries,scripted_effects,scripted_triggers,script_values,scripted_progress_bars,on_actions,static_modifiers}/nesnd_ottoman_unity.txt`.
- `events/nesnd_ottoman_recovery.txt` for hidden timed cleanup only.
- `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml` and matching English file; this dedicated pair contains all B-owned new/overridden labels, TUR text and law-row names.

Existing targeted edits:

- `common/journal_entries/nesnd_qe1_identity.txt`, `nesnd_jp_cohesion.txt`, `nesnd_india_core.txt` (only society binding and related unity/dynasty blocks).
- `common/script_values/nesnd_qe1_identity.txt`, `nesnd_jp_development.txt`, `nesnd_india_core.txt` (unity/community/law terms only).
- `common/scripted_progress_bars/nesnd_qe1_identity.txt`, `nesnd_jp_development.txt`, `nesnd_india_core.txt` (unity/community and religion row only).
- Existing `nesnd_ottoman_recovery.txt` in journal_entries/scripted_effects/scripted_triggers/script_values/scripted_progress_bars/scripted_buttons/on_actions/static_modifiers; preserve the 72 claim-button definitions and claim boundaries unless source review proves a blocking bug.

No HUS citizenship laws, social classes, map/pops/history, figures, diplomacy requests, or regional/Italian/USM routes. If C agent needs another block in the India files, coordinate block ownership and reread current bytes before surgical edits. No whole-file regeneration from an old snapshot. Tools and evidence stay in WORK. Test tools will be B-specific and will not enter a release package.

## Writing and UI contract

Author samples were read from immutable `pre-update-20261030T233944Z/mod`, not current AI prose:

- `localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml:236–237`: “保卫王朝” and political reasoning in its desc; :247–248 show a short indicator name and native current/max readout. SHA352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844.
- `ce_cne_events_l_simp_chinese.yml:15` explains reform through historical actors/interests; :69 narrates social consequences rather than code processes. SHA3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a.

Local rule: name the communities that gain funding/voice and the primary-culture groups that bear the political cost. JE reason explains Ottoman expansion beyond the established polity and the interests of different populations. Status describes present cohesion/pause; it does not dump formulas or implementation history. Buttons give the action and political reason; native modifier preview gives money/assimilation/legitimacy, while short custom text gives monthly stock change, targeted radicals, fixed12months and uncancellable term. Named progress rows use actual law groups and concrete economic/war/cultural causes. Same fact is not repeated across reason/status/tooltip. No unsourced historical quote or fabricated future certainty.

Before landing localization, write `batch-b-writing-comparison.md` with each new/changed category's author sample, candidate, issue, rewrite and pass/rework conclusion. Verify all live keys, correct zh/en headers and UTF-8 BOM, dynamic scopes, native concept definitions, and final override precedence. Exact sensitivity approximation is reported in design/delivery; player tooltip truthfully states the discrete monthly effect.

## Tests to run only after approved implementation

1. Ordered AST/source closure: unique effective keys, repeated-item preservation, source-hash changes limited to owned blocks; no main/GAME changes.
2. Laws: enumerate relevant active-law combinations, check old Qin total equals sum of the three new components and old India total equals new law+unrest components; group-row labels resolve to real lawgroup names. Japan remains unchanged except two policy terms.
3. Policies: all eligible regimes and imperial-line successor; unrelated countries/ordinary princes rejected; inactiveJE and duplicateJE; first/repeat/both/expiry/reload/tag-change; zero cash/negative budget still charges positive expense; 12-pulse cap and primary-only targeting; national costs survive JE loss; no cancellation/refund. Counter test uses actual AST effects, not an unconnected replacement model.
4. TUR entry27/35/36/37, subject-only territory, opened36→26→27 without reset; zero population, each single culture category, Afro-Arab exclusion, Turkish exemption, mixed overlaps and clamping. Newly activated monthly sample does not create fictitious SoL change.
5. TUR war0/11/12/23/24months and peace reset; multiple enforced goals and both state callbacks do not stack; same-country threshold callback and monthly initialization orders; no forced conversion/breakup hidden in the effects.
6. Tanzimat ongoing/success/failure/expired temporaryfailure, missing variables, permanent failure evenwith4goals; three reform tiers, repeated click, exactlyone delayedcleanup, building creation/transfer, same-day expiry/renew guard and all three cleanup paths.
7. Native bar decomposition equals actual stockdelta, country/JE scope and missingvariable preview paths, source-index/MCP and Tiger relative delta, final two-axis review. No engine launch. Native timer removal/order, live budget, actual assimilation and UI rendering remain explicitly ENGINE_NOT_RUN unless fingerprint-compatible prior evidence covers them.

Organizer decision requested: approve this concrete plan or send a bounded correction before B edits gameplay. Then B implements its files, writes comparison evidence, and performs its own scoped checks; the organizer integrates and assigns final cross-review.

## Approved implementation handoff

Organizer approved equations and ownership, then issued GO after all three plans closed. Batch B was edited and localized without behavior/Tiger/MCP testing. The source correction above is mandatory. Fixed policy text describes discrete monthly primary-culture radical movement, never sensitivity. The original +6/+12 totals are estimates for twelve monthly accruals; exact end-date tick ordering remains an engine boundary. Implementation is frozen by batch-b-freeze.json; next stage must explicitly authorize tests.
