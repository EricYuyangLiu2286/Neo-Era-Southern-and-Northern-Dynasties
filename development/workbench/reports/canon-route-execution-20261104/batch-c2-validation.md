# C2 independent validation — FAIL_STOPPED

Reviewer /root/sol_b2_implementation; explicitly assigned gpt-6.1-sol / medium. C2 was written by another agent. Frozen28 owned: D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c2-owned-freeze-20261104T155623Z\mod. No game launched, no C/main edits, no B2 self-test, no repairs.

## Red examples

### C2-F01 · P1 · 18 absent-person closure checks are outside the monthly helper

Location: common/scripted_effects/nesnd_civic_characters.txt:367. Parse ordered root definitions: monthly helper ends at line367; lines368-385 are18 top-level definitions named if. None belongs to nesnd_c2_character_monthly. A seen person absent from all pools therefore never receives this intended closed receipt through monthly processing.
Evidence: structure-contract.json top_level_builtin_errors; Tiger18 name-conflict.
Minimum repair: Move all18 checks into intended monthly helper without changing existing seen/dead/retired/void rules. No recreate allegation is made: seen still blocks can_create.
Stopped: full18-person lifecycle/dual-event closure matrix.

### C2-F02 · P1 · Italian lost-state/current-pair cancellation is an unreachable top-level if

Location: common/scripted_effects/nesnd_civic_routes.txt:1010. The if invoking compact_target_valid/mutual_current/partner target checks occurs as a standalone root definition after scholarly_maintenance. Existing callable italian_maintenance tests identity/regime/overlord/war and services, but lost target ownership only resets service months; it does not run abandon cancellation.
Evidence: structure-contract.json top_level_builtin_errors entry19 and actual italian_maintenance AST.
Minimum repair: Place the checks into callable maintenance, retain current reciprocal epoch safety and12-month expense/no-refund contract; test lost-state and stale old callback against a new accepted epoch.
Stopped: Italian accepted-obligation/lost-state/epoch-cancellation matrix.

### C2-F03 · P1 · One operating building validates levels from empty or loss-making buildings

Location: common/scripted_triggers/nesnd_civic_routes.txt:35. E0=0; one level tooling workshop occupancy.75 profit1 plus8-level arms industry occupancy0 profit-100. Required increment2. Actual frozen operating trigger returns true because levels sums9 raw levels while any_scope_building finds the one healthy level. Positive control:2 healthy tooling levels achieves3 months and one reward.
Evidence: source-effects-c2.json manufacturing_mixed_productive_and_empty_buildings_counterexample plus start/three-month positive control.
Minimum repair: Root clarified: preserve startup E0 actual built total and delta; completion sums only same target owner-state, selected production group, each building occupancy>=.75 and profit>0, with target access>=.80. Require E0+delta for3 continuous months. Public facilities retain responsibility/employment rules. Keep nonnegative progress clamp.
Stopped: manufacturing completion/reward matrices after minimal red/control.

### C2-F04 · P2 · 27 target previews reference an absent effect_localization definition

Location: common/scripted_buttons/nesnd_civic_routes.txt:5. Each custom_description uses text=nesnd_c2_project_target_tt and subject=selected state. Key exists only in YML. No effective common/effect_localization definition exists. Engine effects.log1093-1101 declares text as effect_localization_key; native common/effect_localization maps keys to loc fields. Tiger reports27 identical missing-item warnings.
Evidence: tiger-current-owned.json; engine effects.log; person-and-effective-text-audit.json proves YML alone exists.
Minimum repair: Add source-backed effect_localization definition or use supported custom_label/custom_tooltip interface preserving actual selected state. Test no prior writes and initialized valid target previews.
Stopped: valid selected-state preview rendering; no-target no-prior-write AST path is safe.

### C2-D01 · P3 · Owned script files lack UTF-8 BOM

Location: 22 owned .txt files:. All22 owned txt files lack BOM; six localized YML files have correct BOM/header. Tiger emits grouped encoding warning.
Evidence: person-and-effective-text-audit.json BOM list.
Minimum repair: Mechanical BOM addition only; preserve body bytes/ordered AST and refreeze.
Stopped: encoding-only refreeze required.

## Fixed dependency construction

Input/run: D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\runs\batch-c2-20261104T164849Z. Baseline starts from immutable B2repair1 full snapshot, overlays original A2 32 and B1r3 exact34, then current snapshot overlays final C2 28. No changing C read. A1 and all C2 captured MOD dependencies match. B2 base was missing3 unity_policies dependencies; actual B1r3 all34 supplied. QA-only nesnd_batch_c_dependency_slice removed from both test inputs and recorded in config, since actual C2 trigger supersedes it. Full snapshot/source/tool SHA evidence retained.

## Coverage

- **fixed snapshot identity/interfaces — STATIC_PASS**: 28 owned SHA match; A1 non-A2/B1r3 all34/A2 original32 pinned; captured17 MOD deps match; C1/B2repair1 original shared files retained.
- **native compatibility boundary — STATIC_PASS**: Only Garibaldi .1/.2/.3 and Italian .4/.7/.8/.10 AST changed; all other native definitions preserved. ce_global removes only PNI6-day schedule. JE/buttons narrow overrides parsed; native formation/on_action whole files not overridden.
- **project values and budget — SOURCE_AST_PASS**: 1010 delta combinations,8 bounded quotes, player/AI income and2slot boundaries; interpreter round fixture does not certify engine half rounding.
- **project source behavior — SOURCE_AST_PARTIAL_FAIL**: E0/same target/start expense/3months/once; employment/profit/access/owner resets pass. Mixed-building counterexample FAIL; full10-family behavior stopped.
- **JE autoactivation/complete/invalid/reentry — STATIC_ONLY_ENGINE_NOT_RUN**: 10 project and3 persistent agenda source gates; automatic possible/complete timing not reproduced in engine.
- **Italy negotiations — STATIC_PARTIAL_FAIL_STOPPED**: 90day clock,12month cooldown, serial reply guards,2real partner list source present. F02 blocks accepted lost-state/current-epoch closure; full bilateral matrix not run.
- **HUS original/successor boundary — SOURCE_AST_PASS_LIMITED**: actual original/native_successor/retired/provisional/NKH gate controls; no C2 pop move/exodus or A1 law writes; real A2 territory changes not engine-tested.
- **USM Ming/Wu/truce/western outcomes — SOURCE_AST_PARTIAL**: four western outcomes, repeated refresh no punishment/pop/law mutation pass. Ming/Wu/truce and conflict source reviewed; full conflict/peace temporal engine sequence NOT_RUN.
- **18 characters — STATIC_PASS_BEHAVIOR_FAIL_STOPPED**: 18birth contracts,minimum opening age25,native roles,36event definitions; global receipt/pool searches source present; F01 stops lifecycle/dual-event natural ordering.
- **471 CN/EN — EFFECTIVE_TEXT_STATIC_PASS**: 201character+270route keys paired,nonempty,no override losses;683 including unchanged212 C1 keys. Institution subjects reviewed against north-south contract; no game rendering claim.
- **preview — SOURCE_AST_PARTIAL_FAIL**: no-target prior-write-free path safe;27 valid-target descriptions F04, rendering NOT_RUN.
- **MCP/Tiger — EXTERNAL_TOOLS_RUN**: MCP init+5 corrected exact symbol queries; initial3wrong query spellings preserved as test-tool evidence, not product bugs. Tiger641baseline/759current. No engine launch.

## Tool interpretation and limits

- Not a full behavioral pass. True defects stop affected matrices; full JE natural timing, duplicate event delivery, native formation/tag transition, role retirement/exile/death callbacks and localization rendering remain NOT_RUN.
- Inherited GAME Garibaldi .2 else_if without limit is not C2-introduced; retain separately, do not fix merely for Tiger.
- 57 singleton OR logic and14 brace-placement warnings are mechanical style observations; no automatic semantic rejection.
- building_barracks is a native building_barrack alias; do not resurrect withdrawn B2 false positive.
- C1 two changed shared trigger definitions are inherited authorized B2 additions; C2 does not edit shared file. C1 values/buttons exact AST unchanged.
- MCP structure output is navigation evidence; ordered parser is authoritative for repeated AST children.

Detailed evidence: D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\runs\batch-c2-20261104T164849Z/structure-contract.json; source-effects-c2.json; interface-inventory.json; person-and-effective-text-audit.json; tiger-current-owned.json; tiger-delta.json; mcp-c2.json; evidence-source-sha.json; snapshot-sha.json.

Root must assign separate implementation repair, then freeze before independent tests resume.
