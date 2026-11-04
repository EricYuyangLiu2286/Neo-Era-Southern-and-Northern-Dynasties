# Batch A frozen validation

Status: **LIFECYCLE_PASS_UI_TOOLS_PENDING**. Engine verification: **NOT_RUN**. No gameplay files changed during tests. A-01 and A-02 original failures are preserved in their red archives. Both repaired gates and the guard-removal mutation control pass.

Snapshot: `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/canon-a-20261104T125828Z/mod`. This binds the 24 owned files and recorded candidate/native prerequisites, not the concurrently edited whole candidate. See [snapshot/dependency hashes](batch-a-test-snapshot.json).

The interpreter executes the actual ordered source AST. Unknown nodes fail loudly. Native API results, callback timing, object transitions and expiry are explicit injected boundaries, not recreated engine behavior. In particular, these results do not certify real law callback order, class modifier application, exact calendar expiry order, AI play or GUI layout.

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
| fresh_button_preview_without_global_epoch_never_reads_uninitialized_values | PASS | Fresh preview evaluates without relying on simulated earlier writes |
| existing_global_serial_missing_local_epoch_preview | PASS | Existing serial / missing local epoch also previews safely without mutation |
| A02_guard_removal_adversarial_mutation_is_detected | PASS | Removing the new explicit serial branch in memory reproduces the exact missing-global preview read |
| new_history_like_initialization_and_law_callback_reentrancy | PASS | Initialization and repeated reconciliation retain current governance and actual law CMF object under both injected callback timings |
| old_save_existing_ordinary_citizenship_is_not_rolled_back | PASS | Existing ordinary citizenship is saved once and preserved |
| legacy_completed_laws_preserve_choice_and_no_reissued_outcome | PASS | Both legacy registered laws migrate directly; completion does not reissue aftermath |
| legacy_pending_keeps_original_remaining_wait | PASS | Original 90-day remaining wait is retained; no extra year and no early settlement |
| new_global_year_before_at_after_deadline_and_duplicate_settle | PASS | Both routes settle only after fixed global expiry and remain idempotent |
| native_law_activation_failure_does_not_commit_done | PASS | Injected native activation failure leaves ready state and no committed outcome; retry succeeds |
| old_window_old_epoch_bounded_retry_and_repeat_event | PASS | Early same-date window waits, retry is bounded, stale epoch rejects, repeated event stays terminal |
| direct_activate_and_external_hierarchy_changes_preserve_frozen_choice | PASS | External ordinary/custom law or hierarchy changes cannot bypass pending route; monthly reconciliation covers injected pre-activation callback |
| ordinary_revolution_pending_formed_won_orders_and_source_gone | PASS | Both formed/won orders and lost-source variants retain choice/epoch and the original global deadline |
| revolution_after_done_or_original_completion_during_war | PASS | Both completed routes survive; original-government completion during war is refreshed from its source snapshot |
| legacy_source_object_loss_does_not_fake_elapsed_time | PASS | Unknown legacy remaining time enters explicit conflict and retains freeze |
| normal_retag_permanent_exit_and_late_return | PASS | Non-revolutionary retag permanently retires; bare later HUS tag does not revive the system |
| NKH_native_successor_priority_primary_fallback_and_native_HUS | PASS | Native successor wins over revolution receipt; all non-native primaries removed, fallback retained, default hierarchy and editable citizenship |
| clear_all_retains_foreign_CMF_and_has_no_reentrant_revival | PASS | Permanent clear removes all three legacy modifiers and own hierarchy while retaining foreign CMF law reference |

Core coverage: `{"classes": {"effective_cultures": 328, "native_professions": 15, "combinations": 4920, "applicable_cultures": 146, "class_witnesses": {"nesnd_hus_han_upper": 26, "nesnd_hus_han_middle": 91, "nesnd_hus_han_lower": 78, "nesnd_hus_manchu_upper": 8, "nesnd_hus_manchu_middle": 28, "nesnd_hus_manchu_lower": 24, "nesnd_hus_native_upper": 70, "nesnd_hus_native_middle": 245, "nesnd_hus_native_lower": 210, "nesnd_hus_white_upper": 188, "nesnd_hus_white_middle": 658, "nesnd_hus_white_lower": 564}}, "bounds": {"law_nesnd_hus_four_tier_system": {"han": [80, 100], "manchu": [60, 79], "native": [40, 59], "white": [20, 39]}, "law_nesnd_hus_manchu_registration": {"han": [80, 100], "manchu": [80, 100], "native": [40, 59], "white": [20, 39]}, "law_nesnd_hus_native_registration": {"han": [80, 100], "manchu": [60, 79], "native": [80, 100], "white": [20, 39]}}, "ideologies": 68, "ordinary_law_target_matrix": 24, "choice_trace": [["set_variable", "nesnd_hus_registration_choice", "1.0"], ["set_global_variable", "nesnd_hus_registration_serial", "0.0"], ["change_global_variable", "nesnd_hus_registration_serial", 1.0], ["read", "global_var:nesnd_hus_registration_serial", "1.0"], ["set_variable", "nesnd_hus_registration_epoch", "1.0"], ["read", "var:nesnd_hus_registration_epoch", "1.0"], ["set_global_variable", "nesnd_hus_registration_record_epoch", "1.0"], ["read", "this", "country:HUS"], ["set_global_variable", "nesnd_hus_registration_record_owner", "country:HUS"], ["set_global_variable", "nesnd_hus_registration_record_state", "1.0"], ["read", "var:nesnd_hus_registration_epoch", "1.0"], ["set_global_variable", "nesnd_hus_registration_wait", "1.0"], ["set_variable", "nesnd_hus_registration_wait", "True"], ["read", "var:nesnd_hus_registration_epoch", "1.0"]]}`.


UI datatype/narrow-diff assertions, actual MCP queries and A-scoped Tiger are still pending.

## UI and source closure

- PASS: native_GUI_narrow_AST_and_law_datatypes — Ordered GUI AST identical after removing one added native-style header; native data contexts and CMF law object agree
- FAIL: Chinese_English_effective_text_and_references — AssertionError(('unparsed localization row', 'simp_chinese'))
