# A2 repair2 independent validation — FAIL_STOPPED

Explicit gpt-6.1-sol / medium; reviewer /root/sol_b2_implementation. Tested root fixed snapshot D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\canon-integration-20261104T170000Z\mod; all33 owned SHA match. Original failed report remains unchanged. No game run or source edit.

## Confirmed red examples

### A2-R2-F01 · P1 · New units are spread without subtracting each state's inherited regular units

Location: common/scripted_effects/nesnd_native_khanate.txt:142; common/scripted_effects/nesnd_a2_common.txt:2.
Minimal source case: Actual source NKH target40; four states each10 barracks; inherited20 units are10/10/0/0. Source new20 distribution5/5/5/5 produces combined15/15/5/5 against10/10/10/10. National target and summed barracks alone do not prove per-state capacity.
Evidence: source-literal-matrix.json inherited_troops_per_state_capacity_counterexample; root explicit adjudication.
Repair boundary: Count actual per-state existing regular units via state->every_scope_building(limit building_barrack)->every_combat_unit. Available=max(barrack levels-existing units,0). Add only national deficit; prefer states with real spare capacity; each literal allocation <=spare. Preserve inherited units and population targets. Original per-state <=10 constrains new barracks added, not use of larger existing spare barracks. Do not create excess free barracks merely to keep an even distribution. Preserve total allocation and new-build budgets.
Stopped: inherited deployment/formation completion and full military acceptance.
Limit: No claim of observed engine troop loss. Automatic barrack expansion/rejection by create_military_formation is unproven ENGINE_NOT_RUN.

### A2-R2-F02 · P1 · Restoration goal/settlement still reads absent callback references in sibling guards

Location: common/scripted_triggers/nesnd_american_restoration.txt:55; common/scripted_effects/nesnd_american_restoration.txt:268.
Minimal source case: Execute unchanged settlement AST on a NAH fixture with no saved diplomatic_play: goal_pair has sibling exists checks followed by scope:diplomatic_play block, yielding unguarded scope. Settlement also has same-level has_variable=nesnd_restoration_play followed by var comparison, which is not a structural guard. Incomplete old callbacks must fail without required reads.
Evidence: source-literal-matrix.json restoration_settlement_missing_callback_scope_guard.
Repair boundary: Use nested trigger_if/if branches before every callback scope, opponent/epoch and stored-DP variable read; preserve exact-pair and exact-DP terminal receipts. Audit same helper's full missing/old reference closure. No changed outcomes or new mechanics.
Stopped: incomplete/legacy restoration callback and full settlement matrix.
Limit: Actual source safety red; engine reachability/timing of an incomplete legacy callback not observed.

### A2-R2-F03 · P2 · Scripted-button AI still uses obsolete base/modifier shape

Location: common/scripted_buttons/nesnd_american_restoration.txt:6; common/scripted_buttons/nesnd_american_restoration.txt:17; common/scripted_buttons/nesnd_american_restoration.txt:25.
Minimal source case: Repair1 followed scripted_buttons.md example. Current actual GAME has195 scripted-button AI blocks and zero direct base fields; actual 00_scripted_buttons.txt:490+ and636+ use value plus if={limit... add=N}. Tiger rejects all7 submitted base/modifier fields. Event ai_chance uses a different interface and cannot justify button shape.
Evidence: structure-and-interfaces.json native_button_AI and tiger-current-owned.json unknown-field.
Repair boundary: Use current native button script-value shape value/if/limit/add. Preserve recognize base30 with+30 native share/+30 radicals; negotiate50; suppress15 with+20 army/+20 laws. Test all driver combinations against old intended numeric expressions.
Stopped: button AI numerical behavior until source shape corrected.
Limit: No game/rendering behavior certified.

### A2-R2-F04 · P2 · Six implicit UI keys missing in both effective locales

Location: localization/english/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml; localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml.
Minimal source case: NKH, NKH_ADJ, dp_nesnd_native_restoration_desc, dp_nesnd_native_restoration_tooltip, dp_nesnd_khanate_suppression_desc, dp_nesnd_khanate_suppression_tooltip are absent in effective GAME+snapshot CN/EN. Explicit134 paired keys do not cover these implicit database UI keys.
Evidence: structure-and-interfaces.json localization.implicit_missing; Tiger6 missing-localization.
Repair boundary: Add bilingual keys using existing Great Plains Khanate and war terminology and actual outcomes. No new design or fictional effect.
Stopped: complete UI localization acceptance.
Limit: No game/rendering behavior certified.

## Coverage

- **freeze/dependencies — STATIC_PASS**: 33repair2 owned exact SHA in root170000 unified snapshot;31scripts parse; baseline is same full dependency snapshot with original A2 owned restored. C2 known errors not attributed to A2.
- **original seven red cases — SOURCE_AST_PARTIAL**: F1 role assignment fixed; F2first exodus all4destination combinations/70-30 actual moves and receipts fixed; F3missingHUS40% terminal fixed; F4USA/HUS exact storedDP/case/epoch/copy/terminal controls fixed; F5five helpers prior-write-free preview fixed; F6game_date source fixed but natural character ages/pools engineNOT_RUN; F7mixed same-pair treaty withdrawal with break penalties and third-party preservation source-pass.
- **literal army counts — SOURCE_AST_PASS_COUNTS_ONLY**: All0..40 NKH and0..24 two-state restoration source branches execute, one complete positive literal-count formation or no formation for0. All66 allocations equal execution of original dynamic-count source exactly. F01 blocks inherited per-state capacity acceptance; single-state fallback source present but not fully exhaustively run.
- **capital dispatch — SOURCE_AST_PASS**: All800 actual literal target branches and missing/unknown/foreign-owned no-op controls executed. Count includes sea-region definitions from99_seas, so implementation prose800land is inaccurate; owner-state guard prevents a sea capital. Do not label it observed gameplay bug.
- **territory1/2/4 — SOURCE_AST_PASS_LIMITED**: Actual selection/create-country source1small/2large/4NKH, remaining state/population and original/new capital ownership pass; one-state/insufficient remainder/all split cores/disconnected cases reject. Native create_country operation is a fixture; military setup/war dispatch excluded on confirmed downstream defect and50%movement tested separately.
- **migration — SOURCE_AST_PASS_LIMITED**: Actual70/30whole-pop moves two source groups; one/no destination terminals and once-only receipt; actual two original-source50%moves preserve ceded populations;40%HUSdestination and no-HUS terminal. Full40%before-annex engine sequence remains stopped/NOT_RUN, though source ordering is refugees/exile before annex.
- **creation authorization and treaties — SOURCE_AST_PASS_NATIVE_FIXTURE**: BothUSA/HUS, zero/one/two matching newDP candidates: phase-valid guarded creation, temporary flags removed, only unique actual result binds; mixed original-pair treaty ends with penalties, third-party and unrelated article-only pair preserved. Native timing fixture is explicitly not engine execution.
- **exact DP goals/two wars — SOURCE_AST_PASS_PARTIAL**: 14USA/HUS bound controls include actual humiliation on_enforced; exactDP/epoch/case/terminal/storedcopy/missing reject. Full annex settlement and terminal war end natural callbacks NOT_RUN; restoration invalid reference F02 stops affected branch.
- **NPU/SPU/PEU same TWT invitation — SOURCE_AST_PASS**: Actual recognize source and acceptance executed for all3after resolved=true and case_started=true, no duplicate acceptance.11stale/ineligible controls reject:nonce,expiry,legitimacy,IG,subject,war,court_epoch,recreated_receiver,registry,missingreceiver,missingpending.
- **A1/24laws/TIS/Cherokee — STATIC_SOURCE_PASS**: A1 non-A2 file identities preserved; HUS effects only exodus wrapper changed; native-primary helper exact;24ordinary successor laws identical to original A2 frozen helper and do not add HUS-special laws.6old Turtle Island guards executed; Cherokee stubs byte-unchanged. Full old-save adopt/war conversion natural ordering NOT_RUN.
- **characters/AI/localization — PARTIAL_FAIL**: Role archetype repair verified; birth/date and seen/dead guards source-reviewed but fullperson creation/exile/void/retirement native timing NOT_RUN.134explicit paired values/BOM/effective overrides pass, six implicit keys missing. Button AI F03 unresolved.
- **external tools — RUN**: Actual MCPinit+6symbols; actual Tiger759baseline→738current; filter33owned. Current7unknownAI,6strict-scopes,6missingloc etc classified, not blanket ignored. KnownC2diagnostics remain outside A2 finding ownership.

## Native source delegation

Luna actual canonical /root/sol_b2_implementation/a2_capacity_native_interface; explicit gpt-6-luna / high, fork none, root authorized. GAME common/buildings/05_military.txt3–8; engine effects.log4671–4675 and1306–1311; triggers.log3761–3766 and146–152; createformation effects.log959–979; native00_victoria_scripted_effects.txt3–16 and00_ep1_kazakh_events.txt87–100. Proven per-state barrack building combat_unit iterator. No proof of automatic barrack expansion/rejection. Root capacity contract recorded verbatim in F01.

## Evidence and next stage

Evidence root: D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\runs\batch-a2-repair2-20261104T170323Z. Files: original-red-regression.json; source-literal-matrix.json; original-vs-literal-allocation.json; invitation-and-exact-DP.json; creation-phase-and-treaties.json; territory-source-matrix.json; structure-and-interfaces.json; tiger-current-owned.json; mcp-a2-repair2.json. Source/tool/artifact SHA attached separately.

This is a stopped partial external/source validation with real red examples, not an overall behavioral pass. A separate repair editor must finish this confirmed batch, freeze a new manifest, then independent tests resume. Current C2 errors do not block isolated A2 source tests and were not charged to A2.
