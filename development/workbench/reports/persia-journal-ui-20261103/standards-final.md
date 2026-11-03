# Standards review

Snapshot review: baseline `pre-change-persia-journal-ui-20261103T005805Z/mod` (Git `f0463ffed11809bf3efbc570de17d333836a7521`) versus `exports/persia-journal-ui-20261103-a`, using per-file `git diff --no-index` and complete new files. Forty changed files; no synthetic merge-base. Manifest `review-snapshot.json` SHA-256: `bb44221e117e0d00905323db532b5e5cc22d042ff9f3a9f2d37807f5ea19510e`.

Two low-priority documented-standard findings; no confirmed gameplay blocker:

1. **[P3] Describe royal availability accurately.** Both `localization/{english,simp_chinese}/replace/zzzzzzzzzzzzz_nesnd_feedback_l_*.yml:127` say the heir succeeds only “if the emperor is dead” / “若天子已故”. However `common/scripted_effects/nesnd_south_restoration.txt:84` falls back whenever the emperor is *unavailable*, while `common/scripted_triggers/nesnd_south_restoration.txt:11` also excludes a living foreign ruler or designated heir. An available heir can therefore be selected while the emperor survives abroad. Update both tooltips to describe availability and the protection for foreign sovereigns/heirs. Basis: `nesnd-player-writing/SKILL.md` §4–5 requires effective text to match actual script conditions; `journal-text-contract.md` requires necessary conditions and consequences in tooltips.

2. **[P3] Do not imply a Great Power rank restriction.** The English feedback file at line 30 and the other 36 claim-effect keys says “A Great Power may block the demand.” `common/scripted_effects/nesnd_per_campaign.txt:48` admits Major Powers, Unrecognized Major Powers, and five named countries irrespective of rank. Use “A foreign power” or equivalent. Otherwise players are given an incorrect description of who may block a claim. Same text/script-contract standard; Chinese “强权” does not impose the same rank restriction.

Reviewed source SHA-256: English feedback `52ed4543b83335822aa24a6371d60711637a05d77f1d8e3af61bad0c4c984ee7`; Chinese feedback `b380c28b9efc2e8bdcf9469f9ed3208ef28c7d81a362d54268369afb1106eaa9`; restoration effects `b987d784ce96b50e0138d40fba4fd299afefac18d22251696a5f9cf55fc382d9`. All match the manifest.

Scope included delayed settlement locking, actual-war observation, respite guards, claim selection/preview, and QE1 single-owner weekly synchronization. Repeated Jomini blocks and scope traversals were assessed under repository overrides; no independent smell finding warrants refactoring. Tool-enforced checks remain the root agent’s responsibility. Catalog is CURRENT at 1.13.11/build24799966. No game was launched; this is source review only.
