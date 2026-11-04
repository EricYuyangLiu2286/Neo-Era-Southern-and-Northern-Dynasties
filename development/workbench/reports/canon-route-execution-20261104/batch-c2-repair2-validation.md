# C2 repair2 independent validation — FAIL_STOPPED

Reviewer `/root/sol_c2_repair2_validation`, explicit task configuration `gpt-6.1-sol / medium`. Actual spawn assignment is the configuration evidence; no runtime metadata endpoint or substitute model is asserted. Source never edited; game never opened.

Fixed input `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-c2-repair2-20261104T181711Z\mod` is a copy of fixed repair1 full snapshot with only the29 repair2 owned files overlaid from its frozen manifest. No changing C/A2repair3 candidate was read. All1014files match start/end SHA;29owned match manifest SHA `9a8a39658795dd01575b2ea43b75a5f6c3d8a12bd685062a6099ec2d13a93efd`. Only fiveTXT changed versus repair1; six bilingual files byte-identical. A2repair2 pin remains separately excluded.

## Concentrated new finding

**C2-R2-F01 · P2 · Independent USM status description reads missing numeric variables.** `common/journal_entries/nesnd_civic_routes.txt:98–102` contains five `triggered_desc.trigger` blocks with sibling `has_variable` and direct comparison. They are `nesnd_c2_usm_west_open` / `west_success` / `west_fail` (western outcome1/2/3), `nesnd_c2_usm_truce` (USM outcome3) and `nesnd_c2_usm_wuu` (USM outcome2). Evaluating the actual trigger AST with the corresponding variable absent raises `unguarded_value`. Independent inactive/status evaluation cannot rely on prior startup writes under the project reference contract.

Complete same-family scan covered all26triggered_desc entries in civic-owned scripts across four contexts: bothoutcomes absent, western absent only, USM absent only and actual refresh initialized. **104checks:94safe,10red across exactly these5locations.** Actual startup/monthly refresh initializes the values and initialized clauses pass; this does **not** establish a natural-runtime reproduction. Evidence: `status-desc-family-audit.json`. Repair by real presence `trigger_if` body and explicit false else around each comparison, preserving thresholds, text, fallback ordering and existing refresh effects. No default initialization workaround.

Root instructed stop after this complete family list. No hotfix or further C2 behavior run followed the stop. Whole-batch PASS is withheld.

## Preserved successful checks

- Original repair1F01/F02/F03:684direct/helper/button contexts and631transitive/delayed contexts all pass. The latter increased by2new gate entries. Actual graph remains26directmonthlyhelpers /69reachable effects. Fresh missing choice,8missing target button paths and missing-all saved-participant event paths pass.
- All18people:72actual AST checks pass (dates/identity receipts/fourpools/female permissions and doubleintro→absent→monthly→organisation follow). Whole monthly entrypoint now passes9route×fresh/partial/lost cases. Permanent closure fragments90anddeathhooks36pass separately.
- All27project choices:81original source checks pass;10production options verify per-building profitable/employed levels and79%access rejection.27additional options pass interrupted sequence1,2,0,1,2,3, sourceJE inactive→active→complete predicates, frozenE0/quote despiteGDP change, and exactlyone12month expense. Actual automaticJE lifecycle/timing/accounting remains ENGINE_NOT_RUN.
- Preview/retarget108, bilateral16, routeoutcomes/closures147, scholarly/nativecompat14 and government54 pass unchanged matrices. This includes12monthno-refund expense, wrongserial/originalsender/partner preserving the other side’s newer transaction,16USMoutcomes, HUSnative-successor isolation, LOM→ITA callback, narrow nativeAST edits,1010delta combinations and progress clamps.
-34additional Duan qualification cases pass:4countries×choice absent/1/2/3×done/undone plusdead/wrongrole; only living local USMpolitician withcompletedchoice2/3qualifies once. IndependentSIH never qualifies.
- Real Tiger samefixedbottom:695→695, zeroadded/removed signatures. Remainingfield-missing is inherited nativeGaribaldi else_if. Actual MCP venv initialization+5exactqueries succeed. First systemPython invocation lackedMCPpackage; corrected tool invocation succeeded. Catalog1.13.11/build24799966CURRENTchanged0.
-684effectivepairedkeys perlocale (472C2+212C1), sixfilesbyte-identical, all29BOM, zeroeffectiveoverride loss or missingexplicitref. Exhaustive final implicit-key audit was not completed before stop; no blanket all-localizationPASS.

## Tool attempts and remaining coverage

`expanded-complete-lifecycle.json` preserves a134checkfirstattempt:64pass,70fixtureassertions requiring correction. These70are **not product defects or passes**:36personfollowtests omitted introducedreceipt;28missing-participant+3sameticktests deepcopy identity-bearing objects before equality, yielding false mismatches;3valid/poor-notice tests switched to actual countryidentity without supplying northernItalianprimaryculture. Root stop prevents a corrected behavioral rerun this phase. The64passes are27continuousproject/JE predicates,34Duan and3invalidnotice cases.

Do not equate the existing16bilateral passes with the pending full individual-participant/valid-alternative-budget matrix. Death/retirement organisation trajectories, automaticJE close/reentry, full natural multi-month whole-chain behavior, actual modifier expiry/accounting, native formation/transfer/character timing, UI rendering and exhaustive implicitlocalization remain explicitly incomplete/ENGINE_NOT_RUN. Report JSON lists each boundary.

All orderedASTtools preserve duplicatekeys and actual source control flow, with no sibling predicate short-circuit and explicit nativefacts. They are external source checks, not a replacement game engine. This report is an independent snapshot review with one new confirmed reference family; it is not an overall C2 acceptance.

Artifacts: `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\runs\batch-c2-repair2-20261104T181711Z`. Source SHA map is `final-snapshot-integrity.json`; original attempts and older freezes remain preserved. Next: separatelyassigned concentrated5branchrepair, newfreeze, then independent regression and corrected pendingfixture completion.
