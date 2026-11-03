# Southern restoration: actual-save findings and implementation blueprint

2026-11-03. Research only. Main MOD, candidate and save were not edited by this agent. Game was not launched. Native references are Victoria 3 **1.13.11 / Steam build 24799966**, catalog CURRENT. The latest user design overrides the old generic winner choices.

## Decisive actual-save evidence

Immutable input: [latest_test_save.v3](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/latest_test_save.v3>); SHA-256 `6d1563547bf2ec4368625e23e3aed25b06352fe90d03aa6cd43ee27ef97711ee`; game date **1844.7.13.18**. Read with the existing `save_market_network.sections`, `records` and ordered parser; no save mutation.

| Actual object | Evidence |
| --- | --- |
| USM/Wu | No `country_manager` record with `definition="USM"` remains. |
| SIH, country 315 | Still SIH, dynamic name `dyn_c_shuwang_name`, ruler Liu Zhongming / `USM_liu_zhongming`, character 3143. Owns **36 states**, including the sole current Nanjing state 826. |
| HNA, country 309 | Four states; ruler Zhu Jiangchen, character 3135. Holds refugee variables pointing to emperor **3146** and heir **3147**. |
| GNG, country 314 | Two states; own ruler **Zhu Jingyin**, character 3134 (`USM_zhu_jingyin`). This is its current living Zhu ruler, not an available foreign claimant to take for SIH. |
| Original Ming emperor | **Zhu Kuobing, character 3146**, `USM_zhu_kuobing`, alive in **HNA**, roles `character_role_magnate` + `character_role_nesnd_ming_refuge`, flags `nesnd_ming_claimant` and `nesnd_ming_dynastic_verified`. No dead/death-date field; present live character with guest role. |
| Original heir | **Zhu Zuoyu, character 3147**, `USM_zhu_zuoyu`, alive in HNA with guest role and `nesnd_ming_legal_heir`. |
| Stale terminal state | Globals contain **both** `usm_civilwar_status_quo` and `nesnd_south_settled`. SIH has opposition/leader flags, but no settlement waiting/pending/seen flag and no `nesnd_ming_court`. |
| Wartime faction flags | SIH, HNA and GNG all carry `ce_usm_republican_revolution_tag`; GNG is nevertheless still a Zhu monarchy. This flag is not a reliable final constitutional decision. |
| Pending event | No `usm_civilwar.10` occurrence in serialized events. The relevant restoration/revolution JE records are gone; the `nesnd_ming_after_truce` entries for all three are inactive. |

**The original emperor has already escaped successfully. Recall his existing HNA character object; do not create another Zhu Kuobing, and do not borrow GNG's Zhu Jingyin.** The current refuge system selects HNA before SIH, transfers the saved former USM ruler/heir, and stores those exact references in the host. That source behavior is reflected directly in this save. [migration selection and references](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_royal_refuge.txt:74>)

Compact verified evidence: [save summary](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/restoration-save-summary.json>); full selected [country records](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/restoration-country-records.json>), [character records](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/restoration-character-records.json>), [JE records](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/restoration-journal_entry_manager-records.json>).

## Why current settlement never reaches this winner

`nesnd_rebel_victory_fact` rejects a globally settled world except when the country already has `nesnd_ming_court` and the status-quo flag. Actual SIH lacks `nesnd_ming_court`, so it fails **despite USM being gone and SIH owning Nanjing**. The monthly retry additionally does nothing without `nesnd_rebel_settlement_waiting`, also absent here. If the old event could be forced, its restoration option excludes the republican wartime flag carried by SIH, and its generic claimant search is allowed to pick any flagged claimant rather than the exact displaced emperor. [victory and offer guards](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_settlement.txt:1>), [retry](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_settlement.txt:25>), [old event choices](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1336>), [old claimant search](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_court.txt:224>).

The source that can set the stale terminal flags is `.9 immediate`, which sets both globals for a status-quo outcome. Actual GNG has `nesnd_status_quo_seen`; this supports the status-quo path having executed, but the save does not establish the exact frame ordering. A new victory path must also prevent a different former participant's status-quo callback from winning a race after a complete territorial victory. [status-quo terminal write](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1294>)

## Result contract

Keep `change_tag = USM` in the common settlement helper. All existing postwar allegiance recognition is keyed to the victorious USM object; removing that tag change would require a much wider migration. Country **display name** is separate from the engine tag. Record original victor (`nesnd_postwar_origin_sih`, `_hna`, `_gng`) before common commit, then use outcome flags for display names and effects. [common commit and tag change](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_settlement.txt:1>), [USM winner recognition](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_settlement.txt:34>).

| Victor | Allowed final outcomes | Character rule |
| --- | --- | --- |
| SIH | Restore Ming, or establish **Great Han** | Ming recalls the **actual displaced Ming emperor**, or an explicitly identified surviving legal heir if the emperor is dead/missing. Great Han retains SIH's current ruler. |
| HNA | Restore Ming, or republic | Ming uses its original-emperor/legitimate-heir object. Republic retains actual native constitutional behavior and receives one dedicated ten-year modifier, described below. |
| GNG | **Direct Ming restoration with its own current Zhu sovereign** | Keep local ruler, or an existing local designated Zhu heir if current ruler is unavailable. **Never run the foreign-emperor finder for GNG.** |
| Other existing rebel victors | Preserve their current generic alternatives | Do not silently expand this task into DEI/PHI/YN1/JAP redesign. |

Country-specific victory options must **not be blocked by `ce_usm_republican_revolution_tag`**; the latest instruction explicitly creates a new postwar choice. Remove incompatible flags only when the selected outcome successfully commits. Preserve pending-state/character rechecks inside option effects, not just their display triggers.

## Minimal closed recovery for this save and future native annexation

Add one independent fact trigger which does not consult stale terminal state. This is true for actual SIH and false for HNA/GNG in this save. The `NOT settlement_seen` guard and USM's absence prevent re-running a completed USM-tag winner. This does not grant a mere occupation the same status as annexation.

```text
nesnd_rebel_unclaimed_total_victory = {
    is_country_alive = yes
    is_subject = no
    has_global_variable = usm_civilwar_occured
    has_variable = usm_opposition_country
    NOT = { has_variable = nesnd_rebel_settlement_seen }
    NOT = { exists = c:USM }
    owns_entire_state_region = STATE_NANJING
}
```

Use that fact in **four places**, as one closure:

1. Add `nesnd_rebel_unclaimed_total_victory = yes` as an alternative to the current top terminal-state gate in `nesnd_rebel_victory_fact`. Keep all existing independence, opposition, and actual victory conditions. The current final absent-USM/Nanjing branch already supplies the territorial fact; do not broaden the live-USM occupation threshold.
2. At the **start** of `nesnd_south_settlement_retry`, branch on the new fact: set waiting if absent; if neither pending nor seen, trigger the normal `.10` event. Make the entire previous waiting-handling block an `else_if`, so its stale-settled cleanup cannot clear the fresh pending marker in the same tick.
3. Add `NOT = { any_country = { nesnd_rebel_unclaimed_total_victory = yes } }` to `.9`'s trigger **and recheck in its immediate before writing terminal globals**. Where JE `on_fail` calls `.9`, the event's own guard will reject a false status-quo conclusion.
4. Use a short expiring pending marker (`days = 7`) in `.10 immediate`, clear it in `after`, and repeat all victory/choice/character conditions at execution. A vanished/cancelled event cannot lock this winner forever; the existing monthly pulse retries only genuinely unresolved winners.

Exact replacement outline at the top of retry:

```text
if = {
    limit = { nesnd_rebel_unclaimed_total_victory = yes }
    set_variable = nesnd_rebel_settlement_waiting
    if = {
        limit = {
            NOT = { has_variable = nesnd_rebel_settlement_pending }
            NOT = { has_variable = nesnd_rebel_settlement_seen }
        }
        trigger_event = { id = usm_civilwar.10 popup = yes }
    }
}
else_if = {
    # Existing waiting-handling branch here, with its current checks/effects.
    limit = { has_variable = nesnd_rebel_settlement_waiting is_country_alive = yes }
    # ... existing body ...
}
# Existing postwar allegiance branch follows unchanged.
```

On successful commit, the existing helper clears `usm_civilwar_status_quo`, marks settlement seen and the winner, sets the world settled, and changes the winner tag to USM. Thus its own success makes recovery ineligible. Do **not** clear the world's settled/status-quo flags merely on discovery or event display, and do not touch other countries' territory, monarchs, or subjects to prepare the choice.

## Exact emperor identity, preservation and recall

### Capture and legacy import

At `nesnd_ming_prepare_accession`, when the actual old Ming ruler is already copied into `var:nesnd_ming_claimant_ref`, also mark that **same character** `nesnd_original_ming_emperor` and set a global boolean `nesnd_ming_original_identity_recorded`. Mark the actual saved heir `nesnd_original_ming_heir`. This captures a later successor as the real deposed emperor if the war occurs long after the initial ruler dies. Do not infer the displaced emperor from all `nesnd_ming_claimant` flags; local Zhu rulers and other heirs can have those flags. [existing exact accession capture](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_court.txt:2>)

For pre-update saves, import identities **once** from existing explicit references in this order: living USM's `nesnd_ming_claimant_ref`/`nesnd_ming_heir_ref`, then HNA's `nesnd_ming_refuge_claimant`/`nesnd_ming_refuge_heir`, then SIH's corresponding references. For each reference require `exists`, `is_character_alive`, and `nesnd_ming_authorized_dynast`. Mark the character objects; set the recorded-global only after a real object is found. Current save therefore resolves exactly **3146/3147 in HNA**. If no authoritative reference survives, do not silently guess from `USM_zhu_jingyin` or create a template: leave recall unavailable and keep SIH/HNA's other legal choice.

The legacy-import effect should run before `.10` displays and may also be called once from monthly settlement maintenance. It is metadata-only and does not transfer or enthrone anyone. GNG never calls it to select its sovereign.

### Keep a royal safe before USM disappears

Normal HNA/SIH migration already protects actual royals, as this save proves. Preserve that path. Scripted `nesnd_commit_rebel_settlement` already transfers live USM characters before `annex_as_civil_war`; retain that order. For a **future** war with no refuge host, add a fallback immediately **after** `nesnd_ming_resolve_court_migration` completes: only if the specifically recorded former emperor/heir is still alive, still owned by USM, no longer ruler, and USM has changed to Wu, exile that existing character. Use the native `exile_character_with_role_cleanup` wrapper, which detaches commanders and replaces transient roles, rather than leaving an owned guest behind for native annexation. Preserve identity flags, template, traits, culture and religion; do not create replacements, immortalize anyone, or stop natural death. [current migration dispatch](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_royal_refuge.txt:182>), [native exile cleanup](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_scripted_effects.txt:720>).

Do not rely on `on_wargoal_enforced` as a pre-annex character hook: native war-goal documentation describes `on_enforced` as script **on top of** the predefined kind effect, not a guaranteed before-annex callback. [war-goal lifecycle contract](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/war_goal_types.md:1>)

### Candidate eligibility and actual transfer

For SIH/HNA, select by `nesnd_original_ming_emperor` first, `nesnd_original_ming_heir` only if no available original emperor. Use global `any_character`/`random_character`, not only `any_country/any_scope_character`: the former can locate the exact existing person in exile or the void. Require `is_character_alive = yes`. The native Espartero chain uses this global search and handles void, exile, foreign ownership and enthronement. [native global character finder](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/ip4_spanish_political_events.txt:768>)

**Do not seize an existing third country's reigning sovereign or current heir.** A guest, politician, exiled or alive-in-void original emperor is recallable; a foreign current ruler/heir is unavailable without a separate diplomatic succession design. The current HNA guest is available. If a specific third-country sovereign is ever intended to move, native personal-union logic is a wider dependency, not a safe drop-in transfer. [existing project non-seizure rule](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_settlement.txt:56>), [native sovereign-transfer/P.U. branch](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:2154>).

At event creation save only the chosen candidate scope for presentation. At click, reacquire/revalidate the same object; if it died, try the recorded existing heir, otherwise leave the choice uncommitted. No monetary or political rewards precede successful transfer and ownership/ruler verification.

Character-scope transfer block (winner scope saved from event ROOT):

```text
# Requires an already selected live original emperor/heir and a live winner.
if = {
    limit = { is_character_alive = yes is_in_void = yes }
    free_character_from_void = yes
}
if = {
    limit = { is_character_alive = yes NOT = { owner ?= scope:nesnd_postwar_winner } }
    owner ?= { save_scope_as = nesnd_original_emperor_previous_country }
    transfer_character = scope:nesnd_postwar_winner
}
if = {
    limit = {
        is_character_alive = yes
        owner = scope:nesnd_postwar_winner
        is_in_exile_pool = no
    }
    if = { limit = { has_modifier = in_exile_modifier } remove_modifier = in_exile_modifier }
    if = { limit = { has_role = character_role_nesnd_ming_refuge } remove_character_role = character_role_nesnd_ming_refuge }
    if = { limit = { is_heir_of_own_country = yes } remove_character_role = heir }
    set_character_as_ruler = yes
}
```

Activate monarchy on the winner **before final enthronement**, and reassert the selected ruler after the common annex/tag-change operation (existing common commit already does this). Only commit if `ruler` actually equals the chosen live character. The exact transferred character retains age, identity, traits, religion and culture. Do not call `free_from_exile_effect` blindly: it also runs ideology-switch helpers, which this task did not request. Its guarded removal of `in_exile_modifier` is enough for this specific original-emperor recall. Native `free_character_from_void = yes` returns an existing living object; it must never run for a dead character. [native exile/foreign transfer/enthronement sequence](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/ip4_spanish_political_events.txt:793>), [free-from-exile side effects](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_scripted_effects.txt:5050>), [engine effect docs](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:9683>).

After successful move, clear old host's refugee claimant/heir reference **only when it points to the moved character**; leave its own ruler/heir and unrelated guest characters alone. If no original guest remains there, clear its `nesnd_ming_refuge_received` marker. An informational notice may use the captured actual previous-country scope, but must not dereference a vanished owner. Existing `nesnd_notify_jingyin_origin` is specifically a Jingyin notice and must not be reused as if Zhu Kuobing were Jingyin.

### Missing and delayed-state outcomes

| State at execution | Safe result |
| --- | --- |
| Original emperor alive, already winner's ruler | Keep him; no transfer or duplicate. |
| Original alive as HNA/SIH/third-country guest | Transfer exact person, then enthrone, then commit. |
| Original alive in exile | Native `transfer_character` directly recruits that same exile. |
| Original alive in void | Native `free_character_from_void = yes`, then transfer/enthrone. |
| Original dead/deleted | Try only recorded living original heir; use successor-specific UI wording. Never resurrect. |
| Original/heir is another living country's ruler/heir | Do not take him; other legal choice remains. |
| SIH has no eligible original/emperor/heir | Great Han remains available; Ming recall is unavailable, with an honest reason. |
| HNA has no eligible original/emperor/heir | Republic remains available; Ming recall is unavailable. |
| GNG current Zhu ruler alive | Keep that local ruler; current save is Zhu Jingyin3134. |
| GNG local ruler absent but local designated authorized Zhu heir exists | Promote that existing local heir. |
| GNG has no living local authorized Zhu | Do not invent/import one. Bounded notification/cooldown and retain current GNG world state; this exceptional condition cannot honestly be reported as fulfilled Ming restoration. |
| Winner loses Nanjing/independence or dies before click | Recheck fails; no transfer/reward/tag change. Pending marker expires; recovery may reoffer only after actual eligibility returns. |
| Already committed legitimate winner | Seen/outcome flags block recurrence; no new reward or re-choice. |

## Event integration and names

In `.10 immediate`, capture pre-change origin flags, import identity if needed, select the existing recall candidate only for SIH/HNA, and set the 7-day pending marker. Add country-specific alternatives; exclude SIH/HNA/GNG from all three old generic alternatives so the old republican flag cannot veto the new choices.

- **SIH restore:** require current victory and eligible original/recorded heir. Save current Liu/local patron reference, restore existing person, set Ming outcome, clear republican/Great-Han/Wu flags, apply the existing ten-year restoration reward once, then common commit. Keep displaced Liu as the existing local patron via `nesnd_ming_preserve_local_patron`; do not delete him.
- **SIH Great Han:** require current victory, retain the current ruler, set `nesnd_postwar_great_han`, clear incompatible Ming-court/interregnum/restoration/republic/Wu flags, monarchy, common commit. The **same** country object becomes tag USM and displays Great Han.
- **HNA restore:** same precise-person route; no generic foreign-prince random selection.
- **HNA republic:** presidential republic, outcome marker, clear Ming/Great-Han/interregnum flags, new HNA-specific modifier once, then common commit. Do not attach the old generic republican modifier as well.
- **GNG:** one acknowledgement/default option, no dynastic choice. Save its own current eligible Zhu ruler (or local designated heir), monarchy, Ming outcome, common commit, verify saved local sovereign remains the ruler. No original-emperor finder or transfer call occurs.

The inherited `nesnd_commit_rebel_settlement` saves the selected ruler before annex/tag change and restores it afterward. Preserve its actual-character transfer-before-annex and winner flags. Add `nesnd_postwar_constitution_decided` **only on successful commit**, alongside the existing settlement-seen flag. The chosen outcome marker is permanent; temporary political modifiers cannot be refreshed by retry.

Add a high-priority dynamic name **inside the existing USM definition**, preserving all other entries (do not add another full `REPLACE:USM` that freezes the whole file):

```text
dynamic_country_name = {
    name = nesnd_great_han_name
    adjective = nesnd_great_han_adj
    priority = 1100
    is_main_tag_only = yes
    trigger = { scope:actor ?= { has_variable = nesnd_postwar_great_han } }
}
```

Use Chinese display name **大汉**, English **Great Han**; the adjective key must be provided in both localization languages. This is a display-name change, not a new country tag or country creation. Existing USM Wu names already use the same flag-driven mechanism. [USM current dynamic naming](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/ce_dynamic_country_names.txt:109>), [native name/priority/actor schema](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/dynamic_country_names/00_dynamic_country_names.txt:8>).

Ming restoration clears `nesnd_postwar_great_han` and `tag_WUU_var` and uses existing USM Ming naming. HNA republic uses existing USM republican naming. Ensure both `nesnd_ming_court` and `nesnd_ming_interregnum` cannot continue to impose a royal display name after the republic/Han choice; the current HNA/SIH high-priority court override is tag-specific, but cleaning outcome flags prevents future ambiguity. [current court name overrides](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/zz_nesnd_ming_court.txt:1>).

## HNA republic modifier: exact keys and dimensional contract

Proposed dedicated modifier, awarded **once for 120 months**, non-decaying. Ten years follows the existing postwar republican duration; the user specified lasting opposition but no exact duration, so this duration and -5 approval are implementation choices, not claimed author canon. It keeps the existing -20% authority and -10 legitimacy costs while replacing the contradictory generic +15 all-opposition approval with targeted gentry opposition.

```text
nesnd_hna_republic_gentry_opposition = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_negative.dds
    country_authority_mult = -0.20
    country_legitimacy_base_add = -10
    interest_group_ig_landowners_approval_add = -5
    interest_group_ig_intelligentsia_pop_attraction_mult = 0.25
    interest_group_ig_intelligentsia_pol_str_mult = 0.25
    interest_group_ig_petty_bourgeoisie_pop_attraction_mult = 0.25
    interest_group_ig_petty_bourgeoisie_pol_str_mult = 0.25
}
```

The four `0.25` values are **+25% multipliers**, not +25 clout percentage points and not +25 approval. The -5 is approval points. Native examples use the exact intelligentsia/petty political-strength keys together at +0.25; native attraction definitions and generated docs confirm the attraction keys. [native paired political-strength example](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip4_04_modifiers.txt:172>), [native intelligentsia attraction](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip4_02_modifiers.txt:278>), [engine modifier definitions](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/modifiers.log:7365>), [old generic republican package](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/ce_event_modifiers.txt:203>).

The proposed native `modifier_flag_negative.dds` asset was checked on disk and exists. Restore-Ming/Great-Han/GNG choices must not receive this HNA-only package. Natural expiry does not reopen the constitutional choice. If a later lawful restoration changes the government, retain the already awarded historical modifier for its original remaining duration unless the author later requests an explicit cleanup rule; do not silently restart ten years.

## Proposed files and bounded checks

| File | Change |
| --- | --- |
| `common/scripted_triggers/nesnd_south_settlement.txt` | Add unclaimed territorial fact; permit that exact completed-victory recovery despite stale terminal flags; candidate eligibility for original person. |
| `common/scripted_effects/nesnd_south_settlement.txt` | Reorder retry; origin/outcome commit markers; retain existing annex/tag/selected-ruler protection. |
| `common/scripted_effects/nesnd_ming_court.txt` | Mark exact displaced emperor/heir at existing capture; avoid generic claimant finder for these three final branches. |
| New narrowly prefixed restoration effects file | Legacy pointer import, exact candidate selection, safe recall, local GNG sovereign selection, one-time outcome effects. |
| `common/scripted_effects/nesnd_ming_royal_refuge.txt` | Optional bounded exile fallback after existing migration, only for actual recorded royals still left in Wu. |
| `events/usm_civilwar_events.txt` | Country-specific choices; preview/execute rechecks; 7-day pending marker; false-status-quo guard. |
| `common/dynamic_country_names/ce_dynamic_country_names.txt` | One Great-Han entry inside existing USM block. |
| New static modifier + bilingual localization | Dedicated HNA political aftermath and accurate emperor/heir/missing-state prose. Apply player-writing skill before final player-facing wording. |

External acceptance should assert: actual save SIH alone is recovery-eligible; current live original 3146 is chosen before heir3147; GNG 3134 is never transferred to SIH; existing refugee guest remains same ID after scripted recall; republic package has exactly four +0.25 fields and awards once; USM dependency closure remains intact; preview/death/foreign-ruler/void/exile/absent-USM cases have explicit guards. Source/AST/MCP checks cannot establish engine success. Root owns implementation and optional user-run engine confirmation.

**Do not edit the user's save to fabricate settlement flags or a replacement emperor. The source fix can discover this already victorious SIH on the next existing monthly settlement pulse and offer the new choice.** No state rollback, war restart, or broad restoration of dead countries is needed.
