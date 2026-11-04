# A2 repair2 — READY_FOR_TEST

Frozen owned: `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-a2-repair2-owned-freeze-20261104T165712Z\mod`

Manifest: `batch-a2-repair2-freeze.json`. 33 owned, 8 changed from repair1. This replaces repair1 for testing; `20261104T164801Z` is retained unchanged. Agent `/root/sol_c1_frozen_validation`, explicit `gpt-6.1-sol / medium`, A2 repair editing role.

## Narrow repair and source

The repair1 call graph used `nesnd_andean_restoration_host` (triggers:2–11) for JE visible/possible/invalid, recognize and invitation-live checks. That host rejected `nesnd_andean_restoration_resolved`, while successful recognition and war settlement set it (effects:4,141,272). Thus the successful court blocked its own later joining route. `batch-a2-repair2-narrow.diff` contains only this closure.

New-case qualification now requires unresolved, no started case and no existing TWT. It alone drives another uprising and local negotiation/suppression. The separate invitation route requires a real surviving PEU/NPU/SPU with the original native/peru/local-open conditions and the actual registered court. The registry stores TWT's country object and epoch once. Registration occurs only on actual approved creation/recognition or explicit rebel+adopted old-court upgrade, never on bare TAG existence and never over an old registry. Current native country-object registry source is `GAME/events/warlord_china_events.txt:460–461` with comparison in `common/journal_entries/00_reunify_china.txt:37–42`; the same owner+epoch shape is already present in read-only A1 effects:60–61.

JE and recognition visibility now include this invitation route. No new-case pressure advances in invitation-only mode; active-case values retain the same numbers. Native progress documentation `scripted_progress_bars.md:27–37` provides the conditional increment shape. Existing court status was revised as one bilingual pair, stating bilateral agreement, independent peaceful parties and no further court/uprising. Existing recognition prose remains the author sample; the rewrite speaks to political choices, with no nonce or engineering vocabulary in player text.

The request saves the real receiver object and its epoch in addition to the applicant nonce. Display, execution and cancellation all call the existing shared live trigger, which now requires that exact receiver and case registry, current full eligibility and matching pending nonce. Acceptance stays bilateral; no automatic annexation, new modifier or repeated reward was introduced. A completed global case remains completed for creating another state.

## Boundary and test handoff

Only authoring delimiter parsing, call-graph/diff review, paired prose reading and freeze SHA collection were performed. **No behavior tests, Tiger, MCP or game launch.** Main MOD/GAME/A1/history/population unchanged. Repair2 does not claim engine behavior verified.

Independent tests must cover all three real applicants after recognition/win with resolved=true; fake/recreated/missing/wrong-epoch court; saved receiver replacement; pending/nonce/refusal/expiry/cooldown; both independence/war/IG/legitimacy changes; new-case lock and invitation-only zero pressure; explicit acceptance/no duplicate reward; legacy once-only receipt adoption without replay. Re-run repair1's complete matrix against this freeze.

Editing stopped at READY_FOR_TEST. B2 repair1 independent retest is the next separately assigned stage; C2 work is not mixed into this freeze.
