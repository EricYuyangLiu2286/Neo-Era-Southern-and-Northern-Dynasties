# Final button preview independent validation — FAIL_STOPPED

Reviewer `/root/sol_c2_repair2_validation`, explicitly retained `gpt-6.1-sol / medium`; independent of editor. Fixed snapshot `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\final-button-preview-20261104T192525Z\mod`. All1015sourcefiles retain start/end SHA and all15owned match freeze SHA `3041bcc50b6a911dc1537cb9cc2496f9ac40fbfa9f7f28294d5f26f226cf35dc`. No source edited and no game opened.

## FBP-F01 · P1 · Historical quote is displayed as the price of a new transaction

The new11 display quote wrappers use any existing stored quote. The project helper’s locked/current wording gate also tests only quote existence. The actual gameplay starts and bilateral acceptance correctly recompute a **new** price, so display and payment diverge.

**Project counterexample, actual source:** start at GDP1million → saved weeklyquote100; explicitly supply native12month expense expiry fact → GDP8million; run actual category `retarget` → active/choice/target/baseline cleared but quote100 remains. Evaluate actual button/helper → locked wording and native expense preview100. Run actual `_start` → new quote/expense800. **All27buttons in10categories reproduce.** Evidence `retarget-display-start-price-counterexamples.json` includes actual displayed native modifier and TT key for every option.

**Compact counterexample, actual source:** accept100/100 → actual bilateral abandon → explicitly expire12month expense/cooldown facts → GDPsender8million /receiver4million → actualnewsend. Both `.10.a` and alternative `.11.a` display100/100 while their actual acceptance records and charges800/400. Evidence `compact-second-contract-display-price-counterexamples.json`. Each country scope is correct; both values are historical. This is the same complete stale-quote family across **29financialentrypoints**, not a ROOT cross-country pricing mixup.

Anchors: `common/script_values/nesnd_civic_routes.txt` final11 definitions; `common/scripted_effects/nesnd_final_button_previews.txt:7–10`. Fix display policy rather than changing payment/retarget semantics: distinguish an actual current commitment from a historical quote with structural guards; inactive/new project uses the current start price, and acceptance previews reflect each participant’s price recomputed by actual accept. Root decides exact state policy. Do not clear old gameplay receipts/quotes merely to make a tooltip look correct.

Affected financial-display tests stopped after the complete same-family red list. No hotfix was made. These are ordered-source-AST counterexamples using explicit native expiry facts; actual engine/UI reproduction is NOT_RUN.

## Independent preservation and external evidence

- Independently rebuilt the author’s preservation result: **78oldhiddenblocks ASTidentical;51oldscriptvalues ASTidentical;207implementation/effect/trigger/modifierfiles byteidentical;1000files outsideowned byteidentical.** All12newhelpernative effects remain enclosed in `show_as_tooltip`, with zero helper gameplay writes outside it. No actual start/payment/award/DB change is present.
- All27 display argument triples match the actual start modifier keys and current DB. Expense/state/politics durations are12/24/12months. All27 actual preview counterexamples left country variables unchanged.
- Literal plus expanded helper localization:439 reference occurrences /305 unique keys, zero missing.143 nested `$KEY$` inclusions resolve. The8ownedlocales have851effective English keys. Dynamic compact text explicitly reads currentROOTand saved peer country; rendering is untested, while the stale numeric result is confirmed.
- All10 native/source-chain SHA match. Actual stdio MCP initialization +5exact structure queries succeeded. Actual Tiger samefixeddependency bottom: **682→680, added1/removed3diagnostic signatures**. The added aggregate is the same encoding warning group shrinking17→16 locations; atomic diagnostic location additions=0, removals=1. No new owned warning was introduced. Raw output and both delta forms retained.

The pre-change author backup contains only14files and no metadata. Initial Tiger therefore could not run against that partial directory; the valid1014-file baseline was reconstructed from the fixedfullsnapshot excluding the newly added helper and overlaying the14oldfiles. This is a tool-input correction, not a candidate change. Initial macro-key substitution and localization parameter-classification tool issues were corrected in WORK only.

## Coverage still pending

No whole-batch STATIC_PASS is claimed. The full project target/state/GDP/existing-modifier/fallback matrix, all exact fallback numeric and negative values, B2ownmarket/public/specialise/movement behavior branches, A2recognize/application/suppress branches, C1kind2/3/5actual-success/firstreceipt/no-award branches, and complete missing-participant financial-previews remain pending the next frozen repair. Source equivalence is preservation evidence, not proof that each new branch displays correctly. All dynamic rendering and actual engine behavior remain ENGINE_NOT_RUN.

Artifacts `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\runs\final-button-preview-20261104T193031Z`. JSON records fixed source SHA, full finding and explicit pending items. Root should assign one concentrated display-price repair, freeze, then rerun these29red entrypoints and complete the remaining approved matrix.
