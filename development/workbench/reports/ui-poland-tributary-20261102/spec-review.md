# Spec review — in-progress snapshot

Baseline: `WORK/backups/pre-change-qin-planning-docs-20261102T004019Z/mod` (Git source `044de73`). Candidate: `WORK/exports/ui-poland-tributary-20261102-a`. WORK = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`.

Read-only snapshot review, not Git merge-base review. Source fingerprint: Victoria 3 **1.13.11 / 24799966**, catalog CURRENT, zero changed indexed files. **ENGINE_NOT_RUN**. The reviewed trigger file SHA-256 is `9e963ad98400be2dd1c994efbc1cc6aa780d162d29a7e4d6a8e64b2dc4b33a69`.

## Findings

- **P2 — Paid ultimatums can fail their event-entry trigger immediately.** `common/scripted_triggers/nesnd_poland_repairs.txt:6–16` allows peaceful KRA to click while it is committed to a prewar diplomatic play; `:19–34` also permits target owners already fighting another war. But `:35–43` requires KRA to be uncommitted and the event recipient to be at peace. All ten buttons charge 50 and create a four-month pending variable before triggering `.2` (example: `common/scripted_buttons/ce_poland_scripted_buttons.txt:183–190`); `.2:151` then refuses activation. The player loses preparation and receives no ultimatum. Spec R02 requires “执行与取消走同一资格判断”; R05 requires “先证明有目标再扣费”. Include the same sender and target diplomatic prerequisites in availability/selection before payment. Native `triggers.log:11481–11486` confirms commitment includes diplomatic plays, separately from war.

- **P2 — F10 changes the intended successor threshold.** `common/scripted_triggers/nesnd_poland_repairs.txt:55–60` treats any living POL as sufficient to invalidate the global JE, including a subject or a one-state remnant; PLC retains the intended restrictions. Spec F10 explicitly says “保留独立和三整合州的设计限制”. Keep `is_subject = no` and `num_incorporated_states >= 3` on both successor branches. Existing-tag protection belongs separately at victory/tag conversion (already guarded at `events/ce_poland_events.txt:483`).

## Covered / limits

F01/F02 use concrete foreign state targets; F04 selects within the victim country; F05 changes the initiator; F07 subtracts once; F09 saves the aid sender; F11 uses war preparation. F03 snapshots precede cleanup, and terminal effects execute once in event immediate. F08 follows native global-JE enrollment (`GAME/common/journal_entries/99_test_global_je.txt:78,129`). R01/R03 now filter the diplomatic play and lock victory at click time. Defeat, secessions and loss of country remain possible.

CNE separately checks five states with five urban centres and national industry totals; human gates exclude AI bureaucracy/bankruptcy/disorder restrictions. Confidence status is conditional and removes the initial revolt spoiler. Japan-specific files have no reviewed diff. Persia/trade work remains in progress and is not scored as missing. Existing-tag secession/war engine semantics remain unverified, not claimed as reproduced defects.
