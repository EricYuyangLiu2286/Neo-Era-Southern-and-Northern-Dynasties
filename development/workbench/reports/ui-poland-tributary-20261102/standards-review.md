# Standards review — 044de73 → ui-poland-tributary-20261102-a

Read-only source review of the Poland/CNE UI delta against `backups/pre-change-qin-planning-docs-20261102T004019Z/mod`; Victoria 3 1.13.11 / build 24799966, catalog CURRENT. No game launch. Persia/trade-scale additions were outside this review. Existing `has_claim_by` state/state_region correction is already assigned to the parent and not duplicated below.

## Documented-standard violations

1. **[P2] Missing NRP is not explicitly false in the first status branch.** [confidence JE:12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/ui-poland-tributary-20261102-a/common/journal_entries/nesnd_cne_confidence.txt:12>) uses `c:NRP ?= { has_war_with = root }` as the entire rebellion predicate. Optional scope access is not an existence predicate, so this does not establish that an actual republican belligerent exists before selecting the rebellion text. Line 14 also places `has_variable` beside the confidence read. [syntax-and-routing.md:30–32](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/syntax-and-routing.md:30>) requires “对象先分支，再使用” and “谓词缺对象明确返回 false”, and expressly disallows treating `?=` as proof of a valid target. Use nested `trigger_if` checks with false fallback for both branches.

2. **[P2] The changed Polish bar reads a different global variable from the one guarded.** [ce_poland_progress_bars.txt:297](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/ui-poland-tributary-20261102-a/common/scripted_progress_bars/ce_poland_progress_bars.txt:297>) checks `ce_polish_claim_state_count_inverse` twice, then reads `ce_polish_claim_state_count` in the same limit. Missing or not-yet-initialized count is unprotected. The same standard states “普通 AND/OR，不构成短路保证”. Guard `ce_polish_claim_state_count` itself, then compare it inside the branch.

3. **[P2] Reply validation does not require a live pending-request object.** [nesnd_poland_repairs.txt:40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/ui-poland-tributary-20261102-a/common/scripted_triggers/nesnd_poland_repairs.txt:40>) checks the requester country but relies solely on `var:nesnd_polish_pending_state ?= scope:target_diplo_play_state` for request identity. Missing pending data must explicitly invalidate the reply. The reference-safety rules require checking object variables with `exists = var:...` and checking “pending、target” across the full delayed lifecycle. Add that check before ordinary identity comparison; retain the four-month lock and three-month event window.

## Other scope checks

No additional finding in the reviewed tag-change, side-switch, state transfer, once-only result, military-formation preservation, CNE native building checks, or AI-only risk-gate changes. No heuristic-only refactor requests.

Reviewed SHA-256: confidence JE `0BCABA0D3B0FA8635E1E1EE12792B30D72254BC715BDB919A44D4202B38E8F77`; Poland bars `20E11A0D8748B4B4F254993274D4340928FC25531CD74E2FD65F873A988C5A02`; Poland triggers `9E963AD98400BE2DD1C994EFBC1CC6AA780D162D29A7E4D6A8E64B2DC4B33A69`.
