# Boundary audit — deployed India / commissions

Reviewed `a1f2be2..a062441`, game 1.13.11/build 24799966 (`catalog.py status`: CURRENT), without launching the game or changing gameplay. Paths below are MOD-relative unless prefixed WORK or GAME. Findings describe source behavior; no engine verification is claimed.

## Standards findings

**P2 — cleanup is not safely repeatable.** `common/scripted_effects/nesnd_india_diplomacy.txt:87` removes four adviser modifiers unconditionally. Acceptance at lines 59, 63–65 installs the common adviser modifier and only one specialization, so normal cleanup necessarily removes two absent modifiers; inheritance at line 110 can remove all four absent modifiers. `common/scripted_effects/nesnd_india_uprising.txt:859` removes contact cost every monthly pulse at stage 3/progress 100; launch at line 91 and close at line 7 remove it again. Equivalent launch sites cover all six regions. Project `log-first-delivery.md`, rule 4 requires same-scope `has_modifier`; lifecycle specification line 36 requires repeatable cleanup. Add guarded removals and test actual AST guard ancestry plus repeated cleanup. These are demonstrated missing guards, not a newly observed error.log claim.

**P2 — geographic exit strands aid maintenance.** A recipient that loses its final Indian state while retaining territory elsewhere fails `nesnd_india_country` (`common/scripted_triggers/nesnd_india_core.txt:2`). Its monthly maintenance then stops (`common/on_actions/nesnd_india_core.txt:4`). The foreign JE invalidates but clears only requests (`common/journal_entries/nesnd_india_diplomacy.txt:4–5`), leaving adviser references and temporary costs/bonuses. Subsequent war, patron change, or France disappearance cannot reach adviser cleanup at `common/scripted_effects/nesnd_india_diplomacy.txt:90–102`; modifiers persist until their fixed expiry. Lifecycle specification line 40/L04 requires parent exit cleanup. Regression seam: eligible recipient → accept aid → retain non-Indian territory only → invalidate → verify no adviser modifiers/references; repeat safely.

## What the 484 checks actually miss

`WORK/tools/validate_india_final.py:7` discards comparison operators and nesting. In-memory negative controls executed during this audit both still returned **true** after changing actual source `army_size < 1` to `> 1` (line 80 assertion), and `state_population > 0` to `< 0` (line 100 assertion). These were parser/validator experiments, not engine simulation.

Other labels overstate their assertions: line 64 checks merely that `possible`/`invalid` exist; line 99 checks pact/subject tokens anywhere, not transfer ordering or guard dominance; line 71 checks snapshot names exist, not stale-serial rejection; line 61 sums only the added 37 battalions. Native three do currently exist in GAME `common/history/military_formations/05_military_formations_india.txt:1448–1465`, but that dependency is not tested. Arithmetic/rollback cases at lines 104–107 are detached expressions.

## Bounded next tests

Use source-bound predicate cases for entry, terminal overlap, cooldown/duplicate clicks, old replies, last-target loss, exact recruitment thresholds, and distinct owner-plus-subject region counting. Preserve operators, duplicate keys, quoted tokens and scope ancestry; seed world data from effective history.

Commission failure branches at `common/scripted_effects/nesnd_commissions.txt:183–253` need failure-injection cases at create/pact/transfer boundaries: no success flag before confirmed relation, only USM fragments transferred, seed-only rollback, later retry after cooldown. Existing lifecycle matrix L23 describes uprising retries; it does not exercise commission failures. No additional commission failure is asserted as reproduced.

Native provenance: GAME `common/scripted_buttons/00_colonial_administration_buttons.txt:278–286` uses `count >= 2` and `is_diplomatic_play_committed_participant = no`; this supports syntax, not the new design threshold. The source-bound tests remain STATIC evidence; native object creation and callback order remain ENGINE_NOT_RUN.

