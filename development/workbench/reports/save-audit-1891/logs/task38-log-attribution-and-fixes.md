# Task38 log attribution and scoped repairs

Executor: GPT-6.1 Sol / medium, delegated by parent `/root`. No game start/stop, console command or commit. Main writes began only after parent verified `backups/pre-change-save-audit-1891-20261105T080440Z`. Root/Astra own Japan balance, Persian changes and final player text; Astra confirmed no overlap with drift effect file.

## Actual input and counts

Captured immutable bytes from `live-observer-20261105/logs/error.log` and all retained `error.1.log` through `.5.log`. Latest file:472,112bytes,mtime07:48:51UTC,1,674 timestamped entries,9,631 physical lines,27 exact message/stack groups. Combined retained six files:11,039 entries,63,127 lines,61 groups. A timestamped multiline engine block is one entry, not one log line or unique root cause. Source code/error summaries retain Chinese bytes in raw captures; grouping decoded uncertain non-UTF8 country names with replacement, so no country attribution rests on garbled names.

`content_load.json` proves actual loaded MOD path was `backups/candidate-native-japan-localization-20261105T045024Z/mod`, between workshop3704408897(EAC debugger) and3085120028(debug UI). All seven initial functional source files match RUN git9cdfd02 and pre-edit main254ca1f byte-for-byte; commit/source proof is `source-version-proof.json`. `effective-source-attribution.json` checks GAME, loaded MOD and both actually enabled workshops for every filename in retained error stacks. Neither workshop overrides the logged gameplay files; unexplained engine-only entries are not blamed on workshop by inference.

## Retained-log attribution

| Source/root cause | Entries | Treatment |
| --- | ---: | --- |
| MOD Japan low-cohesion saved-culture comparisons, lines67/72 |10301|Fixed literal macro target adapter; no rate/target policy change|
| MOD canon regime sends variant law to parent-law API |59|Exact colonial variant uses `has_law`|
| MOD civic fresh quote reads and invalid provider-object comparison |3|29 same-source multipliers and27 analogous provider guards fixed|
| GAME-inherited character ideology government check, in MOD override |2|Logged anarchist and sole identical vanguardist character-context leaves scoped to actual IG|
| GAME ruler helper reached via MOD Norway/Sweden flag callers |4|Two guarded/inverted caller adapters; native helper untouched|
| GAME API naval battle getter copied into MOD Chinese localization |36|Exact existing keys/contract sent root/Astra; Sol did not author prose|
| GAME naval battle script-value type-none |224|Inherited value definition, already has formation existence guard; no proven MOD cause|
| GAME four treaty-article divisions |300|Inherited `inherent_accept_score` divisions by GDP, no MOD file/caller ownership proof; no broad native patch|
| Invalid country, stack `<unknown>:0` |78|Unattributed; no speculative scope/gameplay mutation|
| GAME government-change ruler selection failure |6|No MOD override; no proven MOD caller in returned stacks|
| GAME missing agitator scopes |15|Native event definitions and failed selectors confirmed; no MOD override|
| GAME lobby appeasement reason |1|Native catalyst/effect chain, no MOD override|
| Duplicate journal entry messages |8|Kept intentional behavior; not counted as loops or repaired by deleting journals|
| Engine employment assertion |1|No script attribution; not safely repairable from this evidence|
| Engine/debug NamedIndex `PdxDebugConstants` |1|No source filename; debug ownership not proved|

Total=11,039. Source-level repairs address signatures behind10,369 retained entries, not10,369 independent bugs or observed post-fix successes. Full61-group ledger remains in `attribution-summary.json`, including final fixed status of the four native-ruler helper calls through MOD flags. No retained evidence reports an infinite loop; high repetition is monthly iterator/candidate evaluation, not proof of a looping script.

## Precise mechanical changes

1. `common/scripted_effects/nesnd_jp_development.txt`: `nesnd_jp_low_cohesion_drift` dispatches to one parameterized converter with literal Japanese/Han/Jiangnan culture target. Same policy test,50/50 alternate target choice, one random eligible owned state and one actual primary-culture Pop, same0.25fraction. Both bad RHS saved-target comparisons removed; actual native culture identities checked. Monthly cohesion and high-cohesion conversion ASTs identical. This is separate from Japan balance work.
2. `common/script_values/nesnd_canon_diplomacy.txt:12`: replace only `has_law_or_variant=law_colonial_administration` with exact `has_law`. GAME `00_governance_principles.txt:290` declares parent=law_monarchy; engine requires parent for `has_law_or_variant`. Regime numbers/order preserved, including existing monarchy-parent first branch; no regime policy redesign.
3. `common/scripted_effects/nesnd_civic_routes.txt`:29 expense applications immediately following quote assignment use the same `nesnd_c2_weekly_quote` numeric SV directly. All29 quote receipts preserved.27 object-provider guards in10 cleanup workers now require object existence before equality; existing stale marker is not treated as zero or a valid country. Marker/modifier removal effects and project semantics unchanged. Native SV modifier example `00_chris_scripted_effects.txt:164` verified.
4. `common/ideologies/01_character_ideologies.txt`: only character-context anarchist and vanguardist `is_in_government` leaves now use `interest_group ?= { ... }`; all weights and IG-leader-context blocks unchanged. Existing native-style optional IG scope is already used elsewhere in MOD. The original GAME has the same inherited defect; MOD overrides this file, allowing a narrow repair without editing GAME.
5. `common/flag_definitions/00_flag_definitions.txt`: guard exactly two Norway/Sweden `coa_SWE_use_union_mark_canton_trigger` callers. Native helper source says `SWE exists AND NOT(ruler is monarch AND French)`. Existing ruler: delegate unchanged. Absent SWE: positive false/negative true. Existing SWE without ruler: positive true/negative false, representing absence of the French-monarch predicate, not an invented monarch. This fallback is justified by source boolean decomposition, not claimed gameplay evidence. Entire flag AST after removing only these two adapters equals original; default flags, priorities, all other conditions untouched. No native ruler dereference occurs on absent country/ruler.
6. `events/nesnd_regional_development.txt`, `events/veiled_protectorate_events.txt`: remove9 empty options from permanently disabled hidden no-op legacy events. Always-no triggers, cancellation, immediate effects unchanged; no active narrative/effects removed.
7. `events/nesnd_small_states.txt`: mark existing first/general organise option in event10 as default; eligibility/effects/AI unchanged. This records existing first-option fallback explicitly, rather than inventing a new choice.

Initial generated ideology patch matched a different identical line. Actual-source regression caught it; it was reverted and correctly anchored to character context before final freeze. Failed/interim source preserved; draft generator retired. No such incorrect change remains in final diff.

## Earlier startup signatures that rotated out

The retained six files begin after startup; do not present them as evidence that startup errors vanished. Prior05:00 tool read recorded two unexpected `handle_annexation_as_civil_war` tokens,16 distinct missing-BOM files (one repeated warning), two missing Egyptian diplomatic-action notification keys, nine disabled hidden-events-with-options warnings and no-default warning on small_states10. Complete original startup file has rotated out; two exact token failure lines are retained under R37/live-DP-schema-repair-20261105/engine-failure-excerpt.json. Other startup signatures are bounded prior-session observations, independently confirmed by original loaded source properties; no fabricated raw log excerpt.

Main254ca1f already removed both unsupported false fields; Task38 leaves DP schema/goals/geopolitics unchanged. All16 flagged script files still lacked BOM in both RUN and pre-edit main. Task38 adds exactly UTF8 BOM prefix bytes to those16 files; every other content byte identical. Full list and fingerprints: `encoding-freeze.json`; earlier state: `earlier-startup-carryovers.json`. No additional encoding sweep.

Egypt exact missing keys sent for root/Astra: `nesnd_egypt_protectorate_action_notification_name`, `nesnd_egypt_protectorate_action_notification_desc`. Contract: establishment of custom protectorate, distinct from existing termination notification; no unimplemented reward/territory/law claim. Existing naval keys for root/Astra: `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER_START_OF_BATTLE`, `...DEFENDER...`; remove unsupported non-const NAVAL_BATTLE getters, retain verified battle-header reference and truthful attacker/defender statement. No new script text keys.

## Validation and review artifacts

- Final scope:24 MOD paths=8 functional plus16 BOM-only; `all-sol-changes.json` enumerates exact before/after hashes. Three source freezes are disjoint. No history/map/data change, no commit.
-15 original-source red/candidate-green AST/schema cases in `static-regression.json`, including actual parent-law metadata, direct quote values, preserved receipts, provider guards, Japanese selection AST equivalence, both character ideology contexts and hidden/default events. `flag-caller-regression.json` verifies two inverted guards and exact unmodified rest of flag AST. `encoding-freeze.json` verifies16 exact-prefix-only deltas. All24 changed scripts parse.
- Actual Tiger1.19.0 CLI on whole parent backup versus isolated parent+24 frozen changes:658→655 diagnostics,0new errors; exit0. Existing legacy diagnostics remain. `tiger-final-summary.json` records command, input manifest hash and raw outputs. Candidate isolates concurrent parent/Astra changes and uses read-only parent hardlinks; modified files are separate copies.
- Root can run `validate_task38.py`, then `verify_encoding.py`, then `verify_flag_callers.py`, then `run_final_tiger.py`. These write WORK evidence, not MOD. The initial seven-file Tiger report is superseded by final24-file result.
- **STATIC_PASS only.** No engine reload, runtime continuation or post-fix save/behavior verification. Original runtime failures are real; source fixes and static checks do not establish engine success.
