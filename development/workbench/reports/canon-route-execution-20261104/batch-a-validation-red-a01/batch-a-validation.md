# Batch A validation — stopped at first failing gate

Status: **FAIL_STOPPED**. No gameplay files were changed. No game was launched.

Frozen A scope: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/canon-a-20261104T124235Z/mod`. The 24 owned files were matched to the edit-phase manifest before copying. Additional candidate and native dependency fingerprints are in [batch-a-test-snapshot.json](batch-a-test-snapshot.json); this does not claim the concurrently edited whole candidate has one fixed SHA.

## Executed gate

The existing strict subset interpreter executes the **actual ordered trigger AST**, preserving operators and eager boolean sibling evaluation. It does not run the game. Unknown nodes or required empty scope links raise errors instead of returning a permissive result. The module's documented rule is that an `exists` sibling does not protect another sibling's scope dereference.

| Case | Result | Evidence |
|---|---|---|
| native_law_owner_managed_HUS_is_selected | PASS | actual=True; expected=True |
| native_law_owner_unrelated_country_is_rejected | PASS | actual=False; expected=False |
| in_memory_optional_owner_control_rejects_empty_owner_cleanly | PASS | actual=False; expected=False |
| actual_callback_empty_owner_rejects_without_scope_fault | FAIL | AssertionError(('unguarded scope', 'owner', 'law_example')) |

## Finding A-01

`common/on_actions/nesnd_hus_registration.txt:11` defines the custom law callback with sibling `exists = owner` and mandatory `owner = { ... }` blocks. With a law fixture having no owner, the first sibling evaluates false but the second still resolves the missing scope and raises `unguarded scope`. The normal native callback supplies an owner, so this is an adversarial graceful-failure defect, **not a claim that an ownerless callback was observed in-game**.

The test's positive HUS case and ordinary-country case use the same source AST. Its in-memory optional-owner control returns false cleanly; that control was evaluated before the failing actual AST case and did not modify candidate files. A real repair should put the owner body behind a `trigger_if` existence branch (or equivalent verified optional scope handling), preserving the normal owner semantics.

## Stopped work

Per the coordinator's instruction, testing stopped immediately at A-01. The 12-class/15-profession effective-culture matrix, full law-treatment and ideology preservation assertions, six-law root/target matrix, lifecycle interpreter scenarios, UI datatype/narrow-diff assertions, A-scoped Tiger and MCP queries remain **NOT_RUN in this test phase**. Previous edit/source records are not relabeled as tests.

Repair phase is required before continuing. The next run must bind a new owned-file manifest and rerun this gate before the remaining validation matrix.
