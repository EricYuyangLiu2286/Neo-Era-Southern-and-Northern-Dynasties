# Batch B validation — FAIL_STOP_SOURCE_FINDINGS

Gameplay remains frozen; no gameplay edits during tests. Separate immutable snapshot: WORK/validation/runs/canon-b-unity-20261104/mod, constructed from parent B plus30 B-frozen files and4 explicit TUR recovery dependencies. Snapshot manifest is in batch-b-test-snapshot.json; it excludes concurrent A/C edits.

## Completed checks

- Real ordered-AST suite:10 groups passed, including616 effective law combinations,328 actual culture definitions/traits,9 zero/single/mixed population-share cases, eligible and unrelated/dead countries, TUR36-state entry/27-state resume, explicit national modifier values, primary-only0.001 movement with12-pulse cap, renewal, Tanzimat failure persistence and military contract callback guards. The suite traces source control flow with fixtures, not engine execution.
- MCP: all9 actual protocol queries passed after a tooling-only path correction. The original OR.num_states failure is preserved in batch-b-mcp-attempt1.json; repaired OR container output includes num_states, >= and36. Gameplay hashes stayed unchanged.
- Tiger: fixed baseline and fixed B snapshot ran with the same dependency/configuration. Snapshot yielded 710 diagnostics;150 B-scoped additions. These are149 scope/modifier warnings and one aggregate encoding warning:144 claim-caller warnings,2 scope cascades,3 supply-flow warnings,1 BOM warning. No zero-warning/zero-bug claim is made.

## Findings requiring repair

1. **P1 — Invalid claim-check scope.** `common/scripted_triggers/nesnd_ottoman_recovery.txt:19` calls `has_claim_by` in state_region scope. Engine triggers.log:10147–10155 supports only state. All72 buttons and their execution rechecks use this shared trigger. Engine :10141–10145 supports country `has_claim` targeting state/state_region/country; use the existing TUR country scope with `has_claim=prev` instead, preserving target geography.
2. **P1 — Military supply quantity does not have a supported building-to-unit path.** `common/static_modifiers/nesnd_ottoman_recovery.txt:8,21,22` supplies unit_supply_consumption_mult through building modifiers. Tiger reports it will not flow from building to non-combat unit. Paraguay’s building fragment is preview-only, while its real event applies the modifier to the country. The AST attachment/amount tests passing proves only which objects receive the modifier, not its engine propagation. A source-proven army-only quantity implementation is required; changing a goods-cost multiplier would not satisfy the specified quantity reward.
3. **P3 — Text encoding.** One aggregate BOM warning covers21 txt files; paired localization BOM/header checks passed. Normalize relevant owned/dependency files during repair, without changing unrelated source.

Testing stopped immediately after classifying these source findings. Remaining bar-sum/mutation coverage is NOT_RUN pending a dedicated repair phase and new freeze. No gameplay fixes have been applied. Source-proven claim correction and military supply research/repair were requested from the organizer.

Runtime scope: no game was launched. Native modifier propagation, timer expiry ordering/fallback timing, budget billing, actual natural-assimilation behavior and UI rendering remain ENGINE_NOT_RUN.
