# Final Spec review

**No remaining confirmed Spec findings in the reviewed diff.** Both earlier P2 findings are resolved. This is a read-only snapshot review, **ENGINE_NOT_RUN**, against `WORK/backups/pre-change-qin-planning-docs-20261102T004019Z/mod` (Git source `044de73`), candidate `WORK/exports/ui-poland-tributary-20261102-a`. WORK is `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`.

Changed-file set: 28 files, SHA-256 `92817e3dc27c2bfbb9e6a3a208ca046afcf757b5c84622d5cea7b312a956ffa7`; individual hashes are in `spec-review-final-fingerprint.json`. Game catalog remains CURRENT: **1.13.11 / 24799966**.

## Resolution and consequential checks

- **R02/R05:** Issue eligibility checks KRA's independence/commitment; the shared state predicate excludes targets at war. Selection precedes payment, and acceptance rechecks these constraints plus the pending state's identity. The previously identified immediate refusal-after-payment paths are closed.
- **F10:** POL and PLC now separately require independence and at least three incorporated states. Existing-POL collision protection remains separate at victory declaration/conversion.
- **Other Poland repairs:** Concrete state targeting, split West Galicia, victim-country radicalisation, correct attacking supporter, claim penalty, single progress subtraction, dynamic enrollment, aid-sender scopes, and preparation payment remain represented. Terminal settlement is immediate/once with stance preserved before cleanup. `.97` cancels after global termination and guards execution. Failure retains secessions, defeat/GAME OVER, and the original 10% radicalisation when neither region is held.
- **Trade:** All six invitations require 100 influence, apply −100 for six months, and retain pending identity for four months, beyond seven-day travel plus three-month reply duration. First accepted contact awards +25 relations once per sender; successful completion awards +100 influence for 24 months once. Effective invitation/acceptance text has no conflicting duplicate keys.
- **Persia:** New-game history makes PER a QE1 tributary; only their defensive-pact article is removed. Investment/trade articles remain. This does not migrate an already-running save.
- **CNE/UI:** Five qualifying cities and national industry totals remain separate; human start/funding omits AI caution gates. Expanded completion/failure rows preserve the original predicate terms. Confidence status is conditional without the initial revolt spoiler. The duplicate USM compact button is unmounted, with the envoy accord entry retained. Japan-specific files remain unchanged.

Actual UI expansion, event cancellation scheduling, existing-tag secession/war construction, and native treaty validity remain engine-verification boundaries; this review does not certify gameplay execution.
