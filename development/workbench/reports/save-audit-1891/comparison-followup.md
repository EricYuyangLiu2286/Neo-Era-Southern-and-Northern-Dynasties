# Two-save outcome comparison and gate audit

**Read-only evidence.** Compared the observer save from **1836-08-11** with the final save from **1891-11-04**. No game launch or MOD edits. The exact save paths, byte sizes and SHA-256 values are in [comparison-followup.json](comparison-followup.json).

## Persia

PER's saved claims grew from 4 to 7, with no claim removed. The only additions are **Herat, Sindh, Turkmenia**; all three remain foreign-owned at the final snapshot (Herat/Turkmenia by QE1; Sindh by SIN). All three are named in the east frontier JE buttons. PER owns the same 16 state regions in both snapshots, so these were claim additions without territorial acquisition. At start, future/progress JE is active at 14 and governance at 7. By final, `nesnd_per_future_done=yes`, progress 100, route covert, and east frontier JE is active with claim bar 15.5. The claim action costs 25 points per use; no exact click/date receipt is serialized.

## Ottoman

TUR's saved claims grew from 7 to 44, with no claim removed. **31 of 37 new claims match a region target in the custom Ottoman claim-button file.** The six unmatched there are Albania, Bulgaria, Dobrudja, Eastern Thrace, Montenegro, and Northern Thrace. Five of those (all except Montenegro) are regions TUR owned in the August save and no longer owns in the final save; Montenegro is split between TUR and MON in the final state. TUR gained the Ionian Islands and lost Albania, Bulgaria, Dobrudja, Eastern Thrace, and Northern Thrace. This pattern makes the six unmatched claims consistent with lost Balkan holdings, but the save cannot establish the source or exact date for any claim.

The Ottoman recovery JE is active in both saves: enthusiasm **7.0** (1836) and **18.25** (1891), below the scripted 25-point claim cost at both snapshots. That shows the currently saved bar and current purchase gate; it does not show whether enthusiasm crossed 25 between snapshots. The 1891 active play is Egypt-led `dp_humiliation` against TUR, targeting Eastern Thrace (then USA-owned), separate from the Ottoman recovery JE.

## HUS / USA and the Native Khanate gate

Both snapshots have no global `american_civil_war` and no `nesnd_khanate_created`. HUS has no `nesnd_khanate_campaign_started`, no `nesnd_hus_native_successor` or retired marker, and no NKH country instance. HUS remains the original HUS tag in both saves.

- **1836:** HUS selected choice 1 (Manchu), registration epoch 1, but still has `nesnd_hus_registration_wait`; registration is not done, and active law is `law_nesnd_hus_four_tier_system`. `law_nesnd_hus_manchu_registration` is not active yet. The global registration record is state 1 / epoch 1.
- **1891:** same Manchu choice and epoch, `nesnd_hus_registration_done=yes`, correct Manchu-registration law active since 1837-02-01 replacing the four-tier law, global record state 3 / epoch 1. The next gate still fails because `american_civil_war` is absent.
- The separate USA terrain condition was **not** a blocker: USA owns 7 populated state records in the saved Great Plains strategic region in August 1836 and 10 in November 1891. Four eligible neighboring states are therefore not missing in either snapshot. The missing American-civil-war global marker blocks the trigger before NKH selection/creation.

This distinguishes the HUS registration receipt from the later civil-war prerequisite; registration did complete, but the save has no evidence the USA civil-war marker was ever set.

## QE1 population and dissolution markers

QE1's total population in its owned states (sum of pop workforce + dependents) rose from **39,929,639** to **71,443,178**. The serialized primary-culture population rose from **26,158,024** to **66,066,375** (65.50% to 92.47%). Its saved primary-culture IDs are `319, 320, 321` in both snapshots, matching the MOD's `ce_laoqin`, `ce_xibei`, `ce_xiyu` definitions.

The custom culture described in source as **西域汉羌** is `ce_xiyu`, but its actual culture definition sets `heritage_uighur`. Its population in QE1-owned states rose from **12,896,835 (32.30%)** to **43,901,607 (61.45%)**. Separately, all cultures with `heritage_han` sum to **13,331,779 (33.39%)** and **24,602,632 (34.44%)**. So `ce_xiyu` must not be counted as Han heritage when explaining the saved Han-share or foreign-heritage measures.

QE1 unity rose **64.17733 →100** and `nesnd_qe1_heritage_count` **5 →1**. `nesnd_qe1_dissolved` is absent in both snapshots; the final save has active unity, court, and recovery JEs. The recovery JE is not complete: its trigger requires full country-or-subject ownership of Hexi, Gansu, Xian, and Shaanbei. The heritage count is a foreign-heritage measure based on share and primary culture, not a direct count of `ce_xiyu` people.

## Poland receipts and terminal state

In August 1836, the global `je_ce_the_polish_problem` is active from 1836-01-01. Country evidence includes KRA (4 Polish regions, `ce_participated_in_polish_problem`, council marker and state-count marker), FRA (participation plus pro-Polish and result-pro receipts), RUS (participation plus anti-Polish and result-anti receipts), and PRU registrations. Active subsidiary entries are KRA's reconquest/preparation JEs, FRA's territory-claim JE, PRU's territory-claim JE, and RUS's block-advance JE.

By November 1891, `ce_poland_problem_end=yes`; the root JE and all listed subsidiary JEs are absent or inactive. FRA's `nesnd_polish_result_pro` and RUS's `nesnd_polish_result_anti` remain as receipts; transient stance/participation markers have been cleaned. `ce_polish_victory_declared` is absent. KRA's tag record has no owned state; POL exists with one state (West Galicia), no claims, and no active Polish JE. The end marker is persistent, but its source can be JE completion/failure or the on-action's missing-KRA branch; this save has no terminal timestamp, so the exact branch/date is unresolved.

## Italy stage receipts

There is no `ITA` tag in either save. At 1836, PAP/LOM/LUC/TUS/SIC have their Italian agendas active; LOM has the only foundation action receipt already started (commercial-credit choice 2, target state 24, active marker, zero bar). At 1891, PAP has a completed/rewarded foundation action (choice 3, target state 197) and a chosen plural-compact direction. LOM and LUC retain active choice-2 projects with zero bars; SIC has an active foundations JE but no saved project `active`/choice/done receipt, so its active JE alone does not prove a project was started. PAP, LOM, LUC, and SIC have active Risorgimento entries; TUS has none. Factional state ownership remains split.

The project operating trigger requires peace, target validity, no default, market access ≥0.8, and target building/institution conditions. Thus a zero bar is evidence of a stalled/not-operating stage, not alone proof of a script defect. The save does show no unified Italian result.

## Interpretation limits

These are two point-in-time snapshots, not a replay history. Claims are serialized without actor/timestamp receipts. The save's journal manager contains no closed-entry history rows, so inactive JEs do not retain close dates/reasons. The “unmatched 6 Ottoman claims” and Italy's long zero-bar projects are evidence cues for targeted follow-up, not source attribution or confirmed runtime defects.

Exact paths/line ranges and machine-readable value tables are in [comparison-followup.json](comparison-followup.json).
