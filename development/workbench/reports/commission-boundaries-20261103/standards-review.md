# Standards review

**Final: 0 open findings.** Snapshot review: `pre-change-commission-boundaries-20261103T074556Z/mod` → `commission-boundaries-20261103-a`; parent commit `a06244173fa8a36d97cde42d5bca4068004ece71`. Game 1.13.11/build 24799966; catalog CURRENT. No game launched.

Reviewed candidate manifest SHA-256: `715a18473ff7e65bab3a5fd3ef2d659fe8b21d2f2425ff87abb24e3ff19a8485` (787 files; UTF-8 compact sorted JSON of relative-path → file SHA mappings). All 15 changed files match `contract-validation.json`. Tool fingerprints and independent reruns are recorded in `standards-review-integrity.json`.

**Resolved P2:** the new realm/prince helpers initially compared against `root`, although GAME `common/on_actions/00_code_on_actions.txt:10–13` explicitly gives `on_game_started_after_lobby` no root. This breached NESND `syntax-and-routing.md` global-callback/reference-safety rules. Both helpers now guard `exists = c:USM`, compare with that fixed actor, and explicitly return false when absent. Durable tests cover no-root entry/readiness and absent USM; restoring the root dependency is detected by mutation testing.

The same-scope modifier guards comply with `log-first-delivery.md` rule 4. Geographic loss reaches adviser cleanup through maintenance selection and JE invalidation. Outer `any_state_region` counts each region once; current engine docs support region input to `any_scope_state`. Transfers target only USM fragments, and population/history files are unchanged.

Independently rerun: 45 predicate cases plus five mutations; seven cleanup sequences; six creation scenarios; 19 guarded removal sites; and 23 request cases plus stale-serial mutation, all PASS. The evaluator reads ordered ASTs, retains comparison operators, evaluates nested trigger branches eagerly, and rejects unsupported required references. Tests distinguish direct/indirect subjects, incomplete heartlands, occupation, exact thresholds, cooldown, stale replies, missing objects, creation failure and pact failure. Actual native-plus-MOD military declarations are separately checked as 3 + 37.

These remain bounded static evidence. Creation API results are injected; callback timing, largest-state engine criteria, UI previews and gameplay are not certified. Geographic cleanup tests dispatch eligibility and the cleanup effect separately; its refresh call chain was source-reviewed. The old 326 structural checks are not behavioral proof.

Text uses separate compound-count conditions and native requirements; redundant counting prose was removed. No smell finding is raised: ordered repetitions and generated region tables are justified by Jomini semantics.
