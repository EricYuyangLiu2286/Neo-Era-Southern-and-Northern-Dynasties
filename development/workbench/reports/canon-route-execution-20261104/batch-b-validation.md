# Batch B validation — STATIC_PASS, ENGINE_NOT_RUN

Revision `B-r3-state-count-display`, fixed parent `b94582ecec7b0b6dd5620a184658190157fc1729`. The34-file B closure and explicit recovery dependencies are frozen in batch-b-freeze.json; immutable snapshot `WORK/validation/runs/canon-b-unity-20261104-r3/mod` contains the r2 snapshot plus exactly three display files. No concurrent A/C or planned B2 content is included.

## New display repair and checks

Root identified a real coverage gap: the TUR unity JE exposed two bare num_states comparisons, whose native localization mapping is absent in this game build. Tiger did not detect that UI problem. Each original comparison now has a short named tooltip, with Chinese and English labels; the rest of the eligibility tree stays visible.

- **104 actual ordered-AST eligibility cases pass**:0–50states with/without opened flag, deadTUR and non-TUR. Removing only the two tooltip wrappers produces exactly the old ordered JE AST. The checker rejects the original r2 bare comparisons and confirms neither native num_states localization mapping exists.
- **Four effective localized strings pass**: exactly27/36, Chinese and English, UTF8BOM, final override resolves to the new text; every pre-existing key remains identical. Both tooltips contain only text plus one actual num_states predicate.
- **Two actual MCP protocol queries pass**: returned structures include the correct tooltip key, num_states, >= and27/36. The initial system-Python invocation lacked the MCP package; its failure is preserved. Tests stopped, the corrected virtual-environment invocation was recorded/refrozen, then MCP resumed successfully. No gameplay edit was needed.
- All34 candidate/snapshot file hashes, full snapshot manifest and test-tool hashes remained frozen through the checks.

## Reused r2 evidence

The accepted `B-r2-country-supply` evidence is preserved in batch-b-r2-before-display-repair. Its14 AST groups,13 MCP queries and Tiger560baseline→560snapshot/0added remain applicable to unchanged gameplay. The display-only AST equivalence above connects the changed JE to that result. **Tiger was not rerun for r3**; final combined validation remains root-owned.

That earlier coverage includes616 legal combinations,328 cultures, zero/mixed population, all72 claim buttons,12-pulse policy cap, renewal/timer guards,96bar/delta cases, all3country supply tiers and4negative controls. The original150-warning failure and first snapshot remain separately preserved in batch-b-first-freeze-evidence.

No game was launched. Native UI rendering, actual army goods orders versus separate ship upkeep, live budget billing, natural assimilation, callback ordering and save/reload behavior remain ENGINE_NOT_RUN. Static text/structure checks do not prove the new labels rendered in game.

B2 is PLAN_REVIEW only: batch-b2-small-states-plan.md and its55-source ledger are separate planning artifacts, with no gameplay implementation or tests.
