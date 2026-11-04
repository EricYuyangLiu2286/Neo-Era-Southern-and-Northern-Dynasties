# Batch A frozen validation

Status: **FAIL_STOPPED**. Engine verification: **NOT_RUN**. Gameplay files were not edited during tests. A-01's original failure remains in `batch-a-validation-red-a01/`; the repaired owner gate passes.

Snapshot: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/canon-a-20261104T124845Z/mod`. Scope is the 24 owned files and recorded dependencies; no whole-C fixed SHA is claimed. All test inputs come from this snapshot and the fingerprinted GAME inputs in [batch-a-test-snapshot.json](batch-a-test-snapshot.json).

| Case | Result | Evidence |
|---|---|---|
| native_law_owner_managed_HUS_is_selected | PASS | actual=True; expected=True |
| native_law_owner_unrelated_country_is_rejected | PASS | actual=False; expected=False |
| in_memory_optional_owner_control_rejects_empty_owner_cleanly | PASS | actual=False; expected=False |
| actual_callback_empty_owner_rejects_without_scope_fault | PASS | actual=False; expected=False |
| owned_ordered_AST_parses | PASS | 21 owned script files parsed with ordered duplicate-preserving AST |
| effective_cultures_disjoint_12_classes_native_profession_coverage | PASS | 4920 culture × native profession combinations, each exactly one class or default; original economic strata preserved |
| independent_group_three_laws_all_bounds_and_treatments | PASS | Three laws × 24 exact bounds; unchanged classes keep identical bounds; no duplicate citizenship treatment blocks |
| effective_68_ideology_mappings_preserve_all_original_AST_fields | PASS | All 68 effective attitude mappings and ordered-AST equality after removing only added group blocks |
| six_ordinary_laws_target_scope_root_target_four_way_matrix | PASS | 24 root/target combinations; lock applies only to target country and six ordinary citizenship laws |
| history_politics_is_guarded_before_hierarchy_initialization | PASS | All starting politics/activate_law commands lie inside mutation guard; initialization follows its removal |
| actual_first_choice_then_duplicate_click_preserves_epoch_and_deadline | PASS | Real helper AST allocates one epoch and a one-year global timer; second click cannot change either |
| fresh_button_preview_without_global_epoch_never_reads_uninitialized_values | FAIL | AssertionError(('unguarded_effect_argument', 'global_var:nesnd_hus_registration_serial', 'HUS', 'preview')) |

Coverage details: `{"classes": {"effective_cultures": 328, "native_professions": 15, "combinations": 4920, "applicable_cultures": 146, "class_witnesses": {"nesnd_hus_han_upper": 26, "nesnd_hus_han_middle": 91, "nesnd_hus_han_lower": 78, "nesnd_hus_manchu_upper": 8, "nesnd_hus_manchu_middle": 28, "nesnd_hus_manchu_lower": 24, "nesnd_hus_native_upper": 70, "nesnd_hus_native_middle": 245, "nesnd_hus_native_lower": 210, "nesnd_hus_white_upper": 188, "nesnd_hus_white_middle": 658, "nesnd_hus_white_lower": 564}}, "bounds": {"law_nesnd_hus_four_tier_system": {"han": [80, 100], "manchu": [60, 79], "native": [40, 59], "white": [20, 39]}, "law_nesnd_hus_manchu_registration": {"han": [80, 100], "manchu": [80, 100], "native": [40, 59], "white": [20, 39]}, "law_nesnd_hus_native_registration": {"han": [80, 100], "manchu": [60, 79], "native": [80, 100], "white": [20, 39]}}, "ideologies": 68, "ordinary_law_target_matrix": 24, "choice_trace": [["set_variable", "nesnd_hus_registration_choice", "1.0"], ["set_global_variable", "nesnd_hus_registration_serial", "0.0"], ["change_global_variable", "nesnd_hus_registration_serial", 1.0], ["read", "global_var:nesnd_hus_registration_serial", "1.0"], ["set_variable", "nesnd_hus_registration_epoch", "1.0"], ["read", "var:nesnd_hus_registration_epoch", "1.0"], ["set_global_variable", "nesnd_hus_registration_record_epoch", "1.0"], ["read", "this", "country:HUS"], ["set_global_variable", "nesnd_hus_registration_record_owner", "country:HUS"], ["set_global_variable", "nesnd_hus_registration_record_state", "1.0"], ["read", "var:nesnd_hus_registration_epoch", "1.0"], ["set_global_variable", "nesnd_hus_registration_wait", "1.0"], ["set_variable", "nesnd_hus_registration_wait", "True"], ["read", "var:nesnd_hus_registration_epoch", "1.0"]]}`.

## A-02: First-choice preview reads a global serial that only preceding effects initialize

The first HUS choice enters `nesnd_hus_choose_registration` and then `nesnd_hus_allocate_registration_epoch` (starts at L52). That helper writes a missing global serial and later reads `global_var:nesnd_hus_registration_serial` into the local epoch; further statements read the newly written local epoch. A first-open preview has neither value, and hidden_effect does not establish those variables for its later expressions. The normal execution positive control allocates epoch 1 with a one-year global wait and rejects a second click; the preview-only read fails. This is the same write-before-read preview pattern already prohibited by the project validation contract. A repair must make each preview-visible numeric expression independently readable via guarded values/fallbacks, while preserving real execution's serial allocation and immutable deadline. Moving the same expressions into another hidden block is insufficient.

Observed strict-AST error: `AssertionError(('unguarded_effect_argument', 'global_var:nesnd_hus_registration_serial', 'HUS', 'preview'))`. This follows actual ordered helper calls. Normal effect execution is tested separately; no engine preview was launched. The preview fixture resolves explicit arguments without pretending preceding set_variable/set_global_variable effects initialized the preview environment, as required by the project's recorded engine failures.

Testing stopped at this material finding. Remaining full lifecycle/old-window/source-loss/reentrancy, UI datatype assertions, MCP and Tiger checks are NOT_RUN. No repair was applied in the test phase.
