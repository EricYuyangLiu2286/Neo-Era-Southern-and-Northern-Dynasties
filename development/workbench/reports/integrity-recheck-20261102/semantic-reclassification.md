# Stale semantic register: narrow reclassification

Read-only, 2026-11-02. These replace the interpretation of the five 2026-10-31 assertions in `global-before/known_semantic_review.json`; the old evidence file is preserved. Exact source witnesses/hashes and per-entry limits are in `semantic-reclassification.json`.

| Entry | Current classification | Current evidence and limit |
| --- | --- | --- |
| south_settlement_overseas_annexation | SUPERSEDED_SOURCE_FINDING | `events/usm_civilwar_events.txt:1255` now only records victory, gives its modifier and queues post-war notification. The alleged unconditional .8 annex loop is absent. Task 12 explicitly permits defeat-triggered annexation; current collapse callback runtime remains untested. |
| civilwar_native_wargoal_annexation | SOURCE_CLOSURE_PRESENT / ACCEPTED_DESIGN | `common/diplomatic_plays/ce_diplomatic_plays.txt:2` uses `wg_nesnd_usm_annex`; its `on_enforced` at `common/war_goal_types/nesnd_usm_annex.txt:154` connects registered Japan recovery. Native annex is intended. Earlier backdown/recovery evidence does not certify new task-12 callback dispatch. |
| lin_defection_regression | SOURCE_FIXED | `events/usm_civilwar_events.txt:430`–478 again transfers the living eligible original Lin to YN1, verifies ownership and sends .25; `.25` at line 2589 is enabled. This closes the removed-code allegation, not all YN1 runtime edges. Japanese regency observations are separate evidence. |
| loser_player_continuation | SUPERSEDED_REQUIREMENT / ACCEPTED_GAME_OVER | `docs/agents/engineering-skills.md` and the accepted-failure policy explicitly permit lost-country/GAME OVER. No automatic switch/rescue or restored .4/.7 player-continuation choice is required. |
| japan_result_routes | LEGACY_ROUTES_UNSELECTED / CURRENT_ENTRY_ENGINE_PENDING | Task 12 and `common/scripted_effects/nesnd_war_collapse.txt:2` connect confirmed defeat/two-centre collapse to established three-country recovery. Old .20/.22 restoration alternatives remain unselected. Retain only the specific untested callback, occupation-refresh and shared-JE timing limits. |

No Japanese source change or new game run is justified by these stale assertions alone. Existing successful recovery/regency observations remain valid only for their recorded scenarios/candidates.

# Qin repair acceptance and closure checks

The seven additional launch preparations belong inside their `create_country.on_created` callbacks. This fulfils “新兴国对QE1…” without automatically drafting pre-existing PER/TIB/etc. A source closure check must enumerate XIN, UZB, BUK, KHI, TRC, KYR, TJI, KAZ, AFG, KAL, PER, TIB, KAS, MGL, TUV and QFR; establish each new-country path reaches attacker marker + 90-day window + .91/common-war fallback; and preserve the once-only war lock, independence guards, third-country land protection and unchanged seven existing-tag branches. This is source reachability, not an engine simulation.
