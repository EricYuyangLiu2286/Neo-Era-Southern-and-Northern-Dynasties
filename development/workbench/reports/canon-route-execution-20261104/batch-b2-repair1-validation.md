# B2 repair1 independent validation — FAIL_STOPPED_NEEDS_B2_REPAIR2

Agent `/root/sol_c1_frozen_validation`, explicit `gpt-6.1-sol / medium`. B2 test role; A2 repair editing had already ended. No game launched, no gameplay source changed, no ENGINE PASS.

Final object is root's full fixed integration `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\canon-integration-20261104T170000Z\mod`, manifest `integration-snapshot-current.json`; all1013 SHA match at start/end and B2 owned36 match repair1 manifest. The earlier931-dependency run is preserved separately and is not silently treated as full integration acceptance. Evidence: `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\canon-route-execution-20261104\batch-b2-repair1-integration-validation-20261104T170000Z`.

## New blocking source red example B2-R1-F06 [P2]

`common/scripted_effects/nesnd_small_display.txt:2–7` saves `small_display_country`, then five journal `set_bar_progress` reads use that scope with no existence branch. Actual economy JE `immediate` at `common/journal_entries/nesnd_small_states.txt:43` calls initialize then sync_bars. In an already-initialized ACE with its actual economy JE, the established preview contract skips effect saves/writes; the first bar read reaches missing `scope:small_display_country.nesnd_small_economy_months`. This is a strict source preview reference defect, not an observed game UI error.

The minimal actual orderedAST trace and explicit native JE fact are in `b2r1-display-preview-red.json`. Repair suggestion: guard the entire five-bar read closure after the save, or use a separately proven native JE owner path. Keep the monthly writer and progress values. Stopped remaining B2 behavior tests after confirming this example; did not edit the script.

## Repaired original red examples

F02's expired option now rejects/cancels and the expired promise selects the non-success branch. Three valid political choices are mutually exclusive and revolution closes their temporary state. F03's original expired30-day case now sends failure. F04's outside-India imperial-line ACE now rejects B2. F01 remains withdrawn: native building_barracks is a valid alias.

F05 old score AST, repair raw/clamped AST and literal event modifier AST are exactly equal across2560 complete driver combinations, plus all7 missing sender/partner/kind masks. The actual reliable-support helper reads actual treaty facts and actual ratio script values run; no copied score formula. Includes the−12/−2 lower raw points and all reachable upper points. Correction rows103/120 are unreachable under the actual driver product and harmless. Refuse weight remains literal100. Native AI decision outcomes are untested.

## Completed on full1013 snapshot

-34 TXT parse,36 owned integrity, effective resource/alias missing0;187 paired keys, BOM/header/duplicates/missing checks;29 buttons decomposed by visible/possible/effect AST.
-2m upgrade/1.5m decline six-month hysteresis, ownership-loss target invalidation, own-state retarget with epoch+1 and cooldown.
-Compact6good+1bad+6good cumulative economy, next12 governance, all reward modifiers once;24month independent order; switched subject status and expired terminal close; policy/episode cleanup preserves native market/building facts.
-Actual liberal movement organise/promise/suppress exclusivity, repeated choice no mutation, revolution cleanup.
-C1 original50 source groups and13 skipped-write preview cases pass. Real kind5 full send/reply/accept obtains FRA investor, capital modifier and success notification; no B2/Italy placeholder.
-Actual stdio MCP initialization/list/init_game plus13 structure queries succeed. Full integration Tiger exact36 B2 owned gives errors0, logic7 and brace-placement3. A2/C2 diagnoses are separately visible in raw output, not labelled B2 or globally cleared.

## Preserved older evidence and NOT_RUN

73-country identity/actual territory controls (43 India+30 south), YN1/BUR/SIA/HYD scale/registered groups and nine zero-denominator checks passed in the prior fixed931 run with the same B2 owned SHA. The independent identity script was not rerun on1013 before the new red example; this distinction corrects the earlier progress wording. Do not call this group a final integration rerun.

Remaining kind6–9 full native pre/post transactions, full market verification/pact/regime/overlord boundaries, all remaining preview paths, regional full12+12 and high-autonomy positive terminal, all law/movement/character/revolution-inheritance cases, and a newly rebuilt identical-integration no-B2 Tiger differential are NOT_RUN after stop. No engine economy, autonomy, market, treaty, AI or UI timing result is claimed.

Adapter corrections (ordered metadata, native numeric/IG/chained properties, scoped market.owner, missing explicit fixture values) and the system-Python MCP import failure were tool issues. Only WORK tools changed. The official integration correctly has no QA Italy slice; loaders now read actual frozen source definitions.

State: stopped, needs root-assigned B2 repair2 then a new freeze before full continuation. Main MOD/GAME and every frozen game file remain unchanged.
