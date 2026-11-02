# Final Spec review — integrity-recheck-20261102-a

Candidate: `WORK/exports/integrity-recheck-20261102-a`; main MOD untouched by this reviewer. Source checks: **58 PASS / 0 FAIL**, bound to `spec-final-closure-checks.json`. No remaining actionable Spec finding in the reviewed repair closure.

- All **16 frontier newborns** register attacker/newborn markers, a 90-day launch window and delayed event. All **17 creation paths including QRC** clear old seed scopes, choose an actual positive-population owned state, and check that selection exists before creating the country. Empty existing regions remain transferable; no population is fabricated.
- Frontier force preparation occurs after transfers, only for newborns and only once, including zero-force/inherited-army outcomes. Existing nonzero armies are preserved; line infantry/artillery prerequisites are explicit. The 0/1/2/4/8 tiers require both country and capital population thresholds, bounding created maximum manpower to 2% of each denominator. This does not certify staffing or inherited buildings in-engine.
- Seven existing AFG/KAL/PER/TIB/KAS/MGL/TUV transfer branches remain AST-identical to main. QRC keeps mirrored annexation. Frontier war uses one shared humiliation demand against Qin and individual Qin annex countergoals. The common-war effect is independent of outer root; later annex checks actual war participation when at war, otherwise DP participation, closing the reviewed synchronization concern.
- **Do not duplicate humiliation for each backer:** native `08_humiliation.txt:6`–11 uses `validate_conflicts_war_goals_all`; `war_goal_types.md:166`–167 applies conflicts across all participants. A shared coalition demand is the source-supported implementation of this objective.
- Identity conversion clears orphan temporary pops before the 0.5/1/1 three-pass transaction. French `fra_unrest.10` has one guarded cancellation predicate preserving JE removal, missing character/IG and character death handling.

Final `common/scripted_effects/nesnd_qe1_fracture.txt` SHA-256: `c97a64068a89dbc0f2981f3a366f979ce862468f954b7f862b6f65f989388d87`. All six reviewed hashes match the 55-check read: the guard repair was already on disk when that read ran. Their full hashes are recorded in the JSON.

**ENGINE_NOT_RUN.** Source closure and bounded arithmetic do not prove population split/merge timing, military staffing, runtime war-goal dispatch or UI rendering. No new broad review, Japan edits or engine run performed.
