# Standards review — canon prose snapshot

Reviewed U `backups/pre-canon-prose-20261102T213403Z/mod` → E `exports/canon-prose-20261102-a` under WORK (`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`). Both trees matched `review-frozen-manifest.json` at review entry; 63 changed files. Diff evidence: `standards-review-diff.txt`. This is a snapshot review, with no Git commit range. GAME catalog: 1.13.11 / build 24799966, CURRENT. No game run or candidate edits by this reviewer.

## Hard violations

1. **[P2] Complete the active English timing tooltip.** E `localization/english/replace/zzzzzzzzzz_nesnd_court_followup_l_english.yml:27` still ends with “once Zheng Qin has departed,” and omits the 1839 deadline; the earlier copy at `localization/english/replace/zzzzz_nesnd_south_journal_ui_l_english.yml:10` repeats it. The actual `common/scripted_triggers/nesnd_south_timing.txt:21` opens accession on 1839-01-01 even with Zheng Qin alive, while `common/scripted_effects/nesnd_south_timing.txt:14`–21 forces pressure to 100 once the Chen case has concluded. The Chinese tooltip explains this deadline and the 1837/1838 Chen schedule. The English audit therefore leaves players without the deadline that limits their planning and suggests the old ruler condition still controls automatic progression. Translate the complete current timing explanation into both English copies, including the case-concluded qualification. This is an inherited omission left in a modified, explicitly audited key, not a newly introduced gameplay regression.

Rule: `C:/Users/Eric Liu/.codex/skills/nesnd-player-writing/SKILL.md:40` requires decision-relevant deadlines; lines 47 and 56 require checking every modified/referenced effective text and stale replacement layers; line 64 requires reworking text/effect mismatches.

## Judgement calls

No actionable smell findings. Jomini scope chains, repeated keys, and intentional mirrored localization are not OO refactoring defects under `docs/agents/engineering-skills.md`. The CNE saved-state/fallback, guarded PER source/receipt branches, and South button description selection have no additional Standards finding. Dynamic button descriptions match the current native Cuba example; the stance script value safely defaults before initialization.

Root subsequently reported indentation-only changes in the two button files. This report pins the original frozen review content; final hashes and AST-equivalence evidence belong in the delivery record. Neither this review nor external checks establish engine/UI acceptance. Japan development remains excluded.

Standards: 1 hard finding (P2), 0 judgement findings.

## Targeted resolution

**Finding 1 RESOLVED.** Rechecked all four CN/EN overrides against actual timing scripts: 1837/1838/1839 timing, the case-concluded qualification, and the living-Zheng-Qin override now agree. Fix source `root-review-proposals.json` SHA256: `e42a90a12f0f7652095fd02d52a9858111dc8aeaa52b182176982af135e87003`. Exact localization and script hashes are recorded in `standards-resolution-verification.json`. No full repeat review, candidate edits, or game run. Remaining Standards findings: **0**.
