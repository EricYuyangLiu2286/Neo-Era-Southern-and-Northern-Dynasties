# Spec review — commission boundary candidate

Compared baseline `pre-change-commission-boundaries-20261103T074556Z/mod` (source a062441) with `exports/commission-boundaries-20261103-a`, using `git -c core.autocrlf=false diff --no-index`. Specification: latest user request and root's selected thresholds, supported by `native-thresholds.md`, `boundary-audit.md` and `implemented.json`. Catalog: game 1.13.11/build 24799966, CURRENT, zero fingerprint changes.

**Confirmed findings: 0.**

The request that commissions must not be initial unlocks is implemented by the shared `civilizing_mission` entry prerequisite, consistently used by JE activation, decisions, scripted buttons and refresh. Final readiness is separately checked inside creation effects. Tianzhu requires 12 distinct mainland regions, either three direct princely subjects or three fully controlled original princely regions, and two fully controlled Mughal heartlands. Yuanshan requires four of its six regions. Full control rejects remaining foreign fragments and therefore cannot be satisfied merely by occupying Mughal territory or conquering a neighboring prince's enclave. Absent MUG does not prohibit formation.

Country-scoped state iterators preserve personal USM ownership requirements for the capital port and an administration. Actual land handover remains explicit `region_state:USM` cession: 25 bounded Indian regions/islands, six South African regions, no subject-country annexation or foreign-state transfer. Prince relationships remain unchanged. Established flags follow confirmation of the subject relationship; the inherited failed-pact rollback is restricted to the newly created one-state seed. Formation cooldowns and readiness rechecks limit duplicate attempts. Existing six uprising cases retain their transfer migration calls.

Geographic exit now reaches adviser cleanup through both maintenance eligibility and JE invalidation; expired aid clears stored adviser references. Modifier removals have same-scope existence guards. Final review confirms suppression buttons removed from finite governance while the permanent India journal retains all six. Explicit guarded USM references remove reliance on startup ROOT.

**Final binding:** all 15 changed-file hashes match `contract-validation.json` (SHA-256 `099a39b8428a957b60afe8821ba2751d574617b677f51c44f8f2564734377616`). Reviewed 45 predicate cases/five mutations, seven repeated-cleanup fixtures, six creation/pact scenarios, two geographic-exit paths, 23 request cases/serial mutation and 50 contract checks. The stale earlier test/manifest binding after tooltip/text edits was reported for refresh before release.

**Limits:** source evaluation only. Direct subjects and largest-state ownership are explicit design choices, matching displayed requirements. Six creation scenarios cover creation failure, pact failure and success per commission; independent post-pact transfer failure, native callbacks, country destruction and runtime timing are not certified. Structural regression counts are separate from behavioral cases. No game launched.

