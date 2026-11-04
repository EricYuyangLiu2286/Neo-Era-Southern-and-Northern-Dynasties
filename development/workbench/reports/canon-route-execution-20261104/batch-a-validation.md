# Batch A HUS 法律验证

状态：**STATIC_PASS**；**ENGINE_NOT_RUN**。本轮没有启动游戏，没有合入主MOD，也没有开始A2。

测试绑定本批24个文件及已记录依赖，不把其他代理仍在编辑的整份C称为固定版本。最终24文件与当前候选及测试快照逐字SHA一致。主清单：[batch-a-owned-files-sha256.json](batch-a-owned-files-sha256.json)，清单SHA：`f4d08eea054d5d80528673860b9a7f5deb29c0900f0f9c6b599994afaf48318f`。测试快照：`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/canon-a-20261104T131339Z/mod`。依赖包含NKH定义/触发器、有效文化/trait/职业/意识形态及当前GAME原始文件，见[快照与依赖指纹](batch-a-test-snapshot.json)；Tiger额外使用两种语言的既有国家名称本地化，前后基线相同并单独记录SHA。

## 已通过的范围

- **37组外部断言**：实际保序AST、缺值/对象保护、原版字段保留及生命周期。不是把每个单词或字段计成行为通过。
- **328种有效文化 × 15种原生职业 = 4920组合**：适用者恰好一个class，其他文化回default；12类互斥、职业经济阶层保留，满洲仍为全球Han heritage但优先归MM。
- 三项真正阶序法、独立法组、每法24项上下限；未选择群体边界不变，不重复叠加公民法待遇。六普通公民法的原版保序AST除两个冻结守卫外一致；24个root/target组合确认施加锁检查目标国。
- 68项意识形态在GAME＋候选同路径覆盖＋CE文件的有效来源中保留；删去本次新增组块后，其他源AST完全一致。
- 新局/旧档、两个完成分支、旧pending剩余90天、新全局一年、重复点击/结算、旧epoch、次日重试上限、注入改法失败、外部改法/阶序重置、变更其他法律组、普通革命形成/胜出两顺序、战争中原国完成、来源对象消失、一般改tag、损坏legacy记录、释放/分离目标清理、NKH法律前缀和原住民HUS均有实际源AST执行断言。
- 原生GUI仅新增一个同形header，其余保序AST不变；CMF值为law对象。**112对中英文键**通过BOM、单行转义、语言头、引用闭合与无中文英文回退检查。NKH非法律函数及其他国家定义字段保持源AST一致。
- **8项真实MCP stdio查询通过**，查询快照源码前后SHA未变；见[batch-a-mcp.json](batch-a-mcp.json)。其功能是源码查询，不是游戏执行。
- Tiger当前与同依赖的pre-A基线均返回0。**无新增语义诊断**，有**5条新增brace-placement布局warning**：紧凑的双闭括号行，保序解析与相关实际分支已通过。未添加忽略规则；每条原始诊断和判定见[Tiger差异](batch-a-tiger-delta.json)。不将其表述为“零新增warning”。

## 修复与反例

A-01（owner并列守卫）、A-02（预览先写后读编号）、A-03（本地化段落未转义）均按“失败→停测→窄修→重冻→复验”执行，原红报告/快照保留在相应`batch-a-validation-red-a01/a02/a03/`。A-02去掉新保护的内存变异会重现相同缺值读，证明检查能拦截回归。A-03只改两份文本的转义，其他脚本SHA未变，故按精确指纹复用已通过的玩法AST测试。

两项工具适配单列：文本采集器最初把save_scope_value_as内部name误当本地化键，已限于显示字段；MCP将yes/no规范化为True/False，查询期望已对应其数据表示。首次Tiger快照缺既有国家名且baseline无locale，已在双方补齐同一依赖后重新比较；旧结果保存在`batch-a-tiger-incomplete-input-context/`。这些没有引发额外玩法改动。

## 证明边界

AST执行器严格处理源节点和非短路布尔兄弟项，未知节点报错。原生法律落地/回调时序、历法到期、革命对象转换等作为明确输入或故障注入；因此它证明脚本控制流与不变量，不证明引擎已经这样运行。仍需真实引擎观察：自定义class修正识别及最终接纳、真实强制改法菜单/回调、自然到期与存读档、革命对象寿命、AI自然选择、无CMF/有CMF的实际布局。损坏旧档已丢失原等待期限时保留冻结并标记冲突，不伪造剩余时间。

本批没有验证A2的疆土选择、实际人口迁移、军队与战争结算；仅核法律接入口与原有未编辑函数。主MOD、Git合并和跨批全局回归由root协调。

## 逐组结果

| 检查 | 结果 | 具体边界 |
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
| native_GUI_narrow_AST_and_law_datatypes | PASS | Ordered GUI AST identical after removing one added native-style header; native data contexts and CMF law object agree |
| Chinese_English_effective_text_and_references | PASS | 112 paired keys, BOM/header/quote parsing, no English Chinese fallback, required legal/UI text and aliases closed |
| six_ordinary_citizenship_native_AST_preservation | PASS | All six native citizenship law ordered ASTs are preserved except the two explicit freeze guards |
| shared_Khanate_functions_and_country_definition_boundaries | PASS | NKH non-legal functions and all original country-definition fields remain ordered-AST identical |
| NKH_prepare_actual_legal_prefix_default_hierarchy | PASS | Executed actual gated legal prefix through native research boundary and law package; later construction/military code intentionally outside A test |
| released_target_cannot_cancel_original_HUS_clock | PASS | Released/secession target loses inherited credentials and hierarchy without changing original HUS global timer |
| global_completed_epoch_survives_reclaimed_original_source | PASS | Global done/emigration epoch restores completed Indigenous route after source payload disappears |
| damaged_legacy_done_without_choice_cannot_reselect | PASS | Completed legacy with no route evidence remains frozen/conflicted and cannot reselect |
| HUS_freeze_does_not_lock_other_law_groups | PASS | A direct governance-principles change remains; reconciliation only restores citizenship and hierarchy |

完整输入、工具SHA、案例及数据在[JSON报告](batch-a-validation.json)。编辑与文本依据见[实施记录](batch-a-implementation.md)、[文案对读](batch-a-writing-comparison.md)、[有效意识形态来源](batch-a-native-ideology-narrowdiff.md)。
