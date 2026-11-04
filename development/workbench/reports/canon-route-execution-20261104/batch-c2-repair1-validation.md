# C2 repair1 independent validation — FAIL_STOPPED

Reviewer /root/sol_b2_implementation, explicit gpt-6.1-sol / medium. Fixed input: D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-c2-repair1-20261104T172948Z\mod. Original C2report/freeze remain preserved. Root170000+B2repair2+C2repair1 only; A2 remains repair2, no changingrepair3 read. No game, source edits or B2self-test.

## Concentrated scope/variable red examples

### C2-R1-F01 · P1 · Unconditional monthly Duan qualification reads a missing constitution choice

Location: common/scripted_effects/nesnd_civic_characters.txt:91. 
Minimal case: Fresh LOM/HUS/USM, no nesnd_c2_usm_constitution_choice. character_monthly unconditionally calls nesnd_c2_duan_qualification. Its if.limit contains country eligibility and done flag beside OR of direct var comparisons2/3. These sibling guards do not prevent reads. Actual strict source raises unguarded_value var:nesnd_c2_usm_constitution_choice.
Contexts: all3route countries x fresh/partial-active/lost-target; same failure after every one of18 double-intro cases reaches the monthly helper
Evidence: all18-character-source-lifecycle.json, isolated-monthly-and-player-preview.json, transitive-helpers-delayed-events-guards.json
Repair: Nest actual if/trigger_if body branches before choice reads; country/done/choice existence must be proven. Preserve qualification only for actual USM constitutional choices2/3 and a living local politician. Do not initialize invented default choice or qualify independent SIH.
Stopped: whole character monthly/organisation temporal lifecycle; main monthly chain not certified.

### C2-R1-F02 · P2 · Eight diplomacy buttons read missing target countries in possible

Location: common/scripted_buttons/nesnd_civic_routes.txt:120. 
Minimal case: For each7 Italian propose buttons and scholarly_exchange, possible has sibling exists=c:TAG and NOT={has_war_with=c:TAG}. Missing target TAG still reaches has_war_with. Optional country scope block and visible=false do not guard this independent possible evaluation.
Contexts: missing/annexed/uncreated target country in independent possible/preview path;23records across route fixtures because each root country itself still exists
Evidence: isolated-monthly-and-player-preview.json
Repair: Use structural trigger_if/else guard around all target-dependent possible predicates. Keep existing request mutex, identity, independence, war and actual character conditions. No change to offer/consent semantics.
Stopped: missing-target button/validity preview branch.

### C2-R1-F03 · P2 · Italian delayed options and alternative helper still directly read missing saved participants

Location: events/nesnd_civic_routes.txt:7. common/scripted_effects/nesnd_civic_routes.txt:nesnd_c2_italian_alternative
Minimal case: With no saved sender/partner, .10 accept/alternative option triggers first call reply_valid but then read scope:c2_compact_sender in the same trigger block. .10 alternative hidden effect reaches nesnd_c2_italian_alternative whose if.limit repeats that shape. .11 trigger has exists checks beside direct scope:c2_compact_partner. Four actual source traces raise unguarded saved scope.
Contexts: expired/lost-participant delayed event and independent option/effect preview; source reply_valid itself safely returns false but cannot guard a sibling read
Evidence: transitive-helpers-delayed-events-guards.json
Repair: Place direct sender/partner use under true structural existence/live-receipt branches, including helper and event trigger/option closure. Keep both-country original sender+serial receipts and one-alternative policy. Do not weaken stale-request rejection.
Stopped: lost-saved-participant delayed option/event matrix.

## Coverage and actual limits

- **fixed input and external tools — STATIC_PASS_TOOLS_RUN**: 29C2owned and36B2repair2 SHA match; root170000 complete base pins A2repair2,33A2 SHA unchanged. Full snapshot 1014 source SHA match start/end. Actual Tiger738baseline->695current, C2owned no name-conflict/missing-item/encoding; remaining field-missing is inherited native Garibaldi else_if. Actual MCPinit+5exactsymbol queries, no not-found. No changing C or A2repair3 read.
- **original F01 closure repair — ISOLATED_SOURCE_PASS_FULL_CHAIN_BLOCKED**: No top-level builtin definitions remain. All18 exact repaired close clauses were executed in isolation across absent/local/exile/void/dead (90source cases), plus36death-hook owner/noowner cases; permanent guards hold. Full monthly remains stopped at new F01.
- **18 people and identity permissions — SOURCE_AST_PARTIAL**: 72planned checks:54dates/seen-dead-retired-closed/fourpool/nonforcedforeign/female-law-slot-movement checks pass;18double-intro/absent/follow trajectories reach new F01 after their pre-monthly creation checks. Exact native roles/date contracts retained. Player event trigger/cancellation/option missing-pending entries independently checked; natural event ordering, age UI, exile/void/retirement engine behavior NOT_RUN.
- **original F02 bilateral repair — SOURCE_AST_PASS_LIMITED**: 16Italian bilateral cases: actual send/accept/real service3months/partner lists; own/partner lost state, war, regime, overlord and identity cancel current pair; wrong serial/sender/partner clears only stale local record and preserves new other-side record; timeout/nonce/regime/overlord/war late accept no-op; one alternative.12month expenses persist after cancel/complete. New F03 blocks missing saved participant event paths.
- **original F03 operating levels — SOURCE_AST_PASS**: All27actual project options checked across start/E0/frozenquote/12month expense/3months/one completion/local side effects;81source checks pass. All10production choices reject mixed good/empty or underemployed stock, count each building profit/employment and reject79%access.17public choices have no profit requirement. Production negative test initially removed unrelated required rail facts; adapter corrected, first attempt preserved, not a product bug.
- **project lifecycle/budget/government — SOURCE_AST_PASS_LIMITED**: 27lost target/explicit retarget cases;81valid/missing/stale target previews; all108pass. Prior12month expense prevents early retarget; explicit native expense-expiry fact permits later reset, no engine expiry claim.54source government threshold checks (49/50) preserve political vs economic distinction.1010delta combos and0..3negative/high clamps pass. Full JE automatic attach/close/reentry natural timing and actual recurring budget accounting NOT_RUN.
- **original F04 preview map/BOM/text — STATIC_AND_SOURCE_PASS_RENDER_NOT_RUN**: Actual effect_localization map resolves custom_description key in bothlocales;27valid preview subjects are actual selected states and missing/foreign targets omit safely without prior writes.472C2paired keys (201characters+271routes), plus212unchangedC1keys=684perlocale; no effective override loss/missing explicitref; all29owned BOM. Production tooltip attached to exactly10production options and matches source thresholds. [STATE.GetName] has actual native localization instances; UI rendering NOT_RUN.
- **HUS/USM/source boundaries — SOURCE_AST_PASS_LIMITED**: Actual HUS original/native successor/retired/provisional gates pass.16USM Ming/Wu/truce/conflict×western4 outcome cases pass repeated refresh without old penalty/pop/law mutation; conflict closes politics. Independent SIH7scholarly cases preserve teacher ownership and do not confer delegate qualification. No A1law lock/A2population writes. Full real war/truce/territory callbacks NOT_RUN.
- **Italian native compatibility — STATIC_AND_SOURCE_PARTIAL**: Only allowed Garibaldi1/2/3 and Italian4/7/8/10 native AST definitions differ; all others unchanged. LOM->ITA same-country fixture runs C2 formed callback retaining lifetime results;5Garibaldi saved-character role/alive/ownership guards pass. Native state formation/secession/war/transfer timing remains engineNOT_RUN.
- **expanded reference closure — FAIL_STOPPED_CONCENTRATED**: Actual graph has26directmonthlyhelpers and69reachable effects.684direct-helper/player-button contexts:652safe,9same Duan red,23missing country reads. Isolate remaining67reachable callees in3countries×3fresh/partial/lost contexts plus delayed entries:629checks,616safe,9Duanred+4savedparticipant red. Real static state-region DB loaded; initial missing-static-DB errors excluded as tool fixture issues. No whole-chain PASS and no source hotfix.

## Call graph and tool discipline

Call graph and all traces: D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\runs\batch-c2-repair1-20261104T172948Z. All helper matrices execute actual frozen ordered AST with explicit native-world facts and fail on missing required references. They are not an independent hand-written gameplay state machine. Nested source control flow is kept, sibling AND/OR/limit children are not short-circuited. Conditional subhelpers were isolated because the whole character chain is stopped; these partial passes never certify the full chain.

A slow first guard scan repeatedly reloaded the same native static-region database; it was interrupted and replaced with an immutable per-run cache. Initial static DB omissions and missing landowner fixture were corrected as test-tool inputs, not reported as gameplay bugs. The production fixture's public-vs-private choice classification was also corrected using actual source branch membership.

All old/native alias classifications remain: building_barracks is a valid native alias. Current Garibaldi else_if without limit is inherited GAME source and not charged to C2. C1 shared trigger changes are inherited B2 additions; no C2 shared diplomatic edit. Timed modifiers, automatic JE lifecycle, dynamic localization rendering and native character/formation/transfer callbacks remain ENGINE_NOT_RUN.

Editing must stay stopped until root assigns the complete three-family guard repair; then freeze again before testing. No gameplay source was changed by this reviewer.
