# Spec axis — final recheck

**No remaining confirmed spec findings in the reviewed candidate.** This supersedes the five open findings in `spec-review.md`; it does not certify engine behavior.

Baseline remains the independent `pre-change-qin-persia-campaign-20261102T022528Z/mod` snapshot (`c0e11fe`). Candidate remains `exports/qin-persia-campaign-20261102-a`; MAIN was not edited. Latest ordered-AST coverage is **51 changed files, 49 scripts, 384 top-level definitions**. The initial final pass completed 20 targeted checks; this latest specification alignment completed **14 further checks**. Current fingerprints and the retained prior review are in [spec-review-final-evidence.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/qin-persia-20261102/spec-review-final-evidence.json>).

Closed findings:

- SoL divisor and all 30 directional fractions now use the intended lower/upper bounds; diversity no longer suppresses its own penalty.
- Recovery claims exactly match the current three strategic-region sets plus the author's China trigger, excluding Formosa/Hainan. Previously missing Korean/Japanese regions are present.
- Each aid event is excluded while its own six-month modifier remains active.
- Patronage clears below40 and immediately recalculates shares after removing its cost.
- The army child includes the six-month preparation action, actual treasury debit, temporary military benefit and balance change.

Additional closures checked: 29-day endpoint clocks; timeout/endpoint priority and under-four-state no-award handling; first activation starts the lifetime clock; barracks target captures actual runtime total plus25 once; PER completion uses persistent facts; PER+2 and Qin subversion have separate single owners; uprising has one authoritative writer and a display-only child; three fresh conversion passes remain intact; civil opposition follows the suppressed faction and is checked weekly; frontier joining uses an existing coalition and a bounded launch window. The two agenda children no longer declare an always-false completion condition.

Latest user5 alignment intentionally supersedes the earlier reversion-filter proposal: **only assimilation excludes Sinosphere cultures**. Reversion now uses all native pairs: **677 regions, 3,001 choices**, including all **174 pairs across the 36 detailed starting regions**. Script weights, data and whitelist match exactly. The 100 heritage aggregators combine population shares, exclude primary-culture heritages and count groups at ≥1%; unity reads the cached count at −0.05/group. Court administration retains its separate culture-count metric. All 15 native newborn-country initializers retain shared ce_xiyu, remove only ce_xibei/ce_laoqin and set native official religion inside `on_created`; existing tags' identities and pop religions are not rewritten. Evidence: [spec-alignment-delta-evidence.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/qin-persia-20261102/spec-alignment-delta-evidence.json>).

**Validation boundary:** `ENGINE_NOT_RUN`. Population splitting/rounding, country inheritance, military staffing, coalition joining and simultaneous lifecycle callbacks still require their targeted runtime observations. No source edits or game launch were performed by this review.
