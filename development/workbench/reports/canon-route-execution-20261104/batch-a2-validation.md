# A2 独立外部审查与失败交接

2026-11-04。**FAIL_STOPPED_FOR_REPAIR / ENGINE_NOT_RUN**。实际显式配置 **gpt-6.1-sol / medium**，本代理 `/root/sol_b2_implementation` 按root NEW_TASK独立测试A2。未编辑A2候选/冻结/主MOD，未打开游戏；B2玩法保持冻结。发现源缺陷后停止受影响的正向验收，按root后续消息汇总红例后停止，不边测边修。

## 固定对象与工具

32份owned均匹配 `batch-a2-owned-files-sha256.json`，30份.txt保序解析成功。固定测试副本：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-a2-20261104T160647Z\mod`；基点副本：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-a2-baseline-20261104T160647Z\mod`。构成为C1 repair4固定完整依赖 + A1已验证 `canon-a-20261104T131339Z/mod` 的24份SHA匹配overlay + A2精确owned覆盖。基点的原owned也与A2 manifest baseline SHA一致。没有把变化中的整个C称冻结。

第一次试备仅以C1快照为底，缺A1新增定义，相关Tiger unknown-field不能算A2缺陷；旧试备目录 `batch-a2-validation-20261104T160308Z` 明确退役。下述证据只用补齐A1后的 `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\canon-route-execution-20261104\batch-a2-validation-20261104T160647Z`。

实际Tiger基点/current都运行：owned计数由missing-item10/unknown-field3/strict-scopes2/missing-localization58，变为missing-item20/unknown-field8/validation10/choice2/strict-scopes6/missing-localization6等。按路径+原文+诊断归一，**37新增、62移除**；逐条数据和分类见tiger-delta.json。没有将所有告警归入“继承”或全部当BUG。原生annex_country也使用control_half_target_country_states，故两条choice是工具枚举滞后；动态count、动态capital和AI字段形状未擅自认证。

实际stdio MCP完成initialize、list_tools、init_game与六次get_structure，isError均false，包含四州创建、军队、复国、迁徙、专用goal、容量helper。MCP仅结构查询，不是引擎执行。所有源/工具证据绑定SHA，详见evidence-source-sha.json及本轮JSON。

## 确认红例

### A2-F1 — has_role uses archetype strings agitator/general/ruler where current has_role expects a specific database role; native IDs are character_role_*.

**P1 / CONFIRMED_NATIVE_KEY_DEFECT**。位置：`common/scripted_effects/nesnd_american_restoration.txt:43,174,178`；`common/scripted_effects/nesnd_native_khanate.txt:131`。

Actual frozen commander-assignment AST yields zero assigned commanders for an existing same-country Tatanka carrying character_role_general. In-memory parameter-only native-ID control assigns one. GAME executable 00_victoria_ep2_scripted_effects.txt:25 uses has_role=character_role_general. Raw general only occurs in commander_orders/orders.md. add_character_role explicitly supports either archetype or database role; has_role_of_type is the separate archetype predicate.

建议：Use source-backed has_role_of_type=general/agitator/ruler or explicit character_role_* consistently. Recheck fallback general and global existing/exile/void cases; do not duplicate templates.

### A2-F2 — First exodus reads global_var:nesnd_hus_registration_exodus_epoch in the same boolean limit as has_global_variable, without a branch guard.

**P2 / CONFIRMED_REFERENCE_GUARD_DEFECT**。位置：`common/scripted_effects/nesnd_a2_manchu_exodus.txt:7-10`。

Actual frozen full helper with valid native registration/epoch and pending, but no previous exodus global receipt, raises unguarded_RHS in the reused strict non-short-circuit AST evaluator. No 70/30 positive pass claimed.

建议：Branch on receipt existence before comparing the numeric epoch; missing receipt must enter first-run movement. Keep each source-pop random_list lottery and immediate no-destination terminal.

### A2-F3 — No-HUS refuge branch references c:HUS in the same limit as exists=c:HUS.

**P2 / CONFIRMED_REFERENCE_GUARD_DEFECT**。位置：`common/scripted_effects/nesnd_american_restoration.txt:16-17`。

Actual frozen nesnd_restoration_refugees with a live pending NAH source and no HUS object raises unguarded scope c:HUS before the intended terminal_no_destination branch. Live-HUS control moves 40% once and clears pending.

建议：Use a true exists branch before entering HUS scope, then alive/populated-state checks. Missing HUS must produce result3 without population movement or pending.

### A2-F4 — Khanate goal validity/on_enforced checks type and pair but not the stored dispatched DP identity or a transaction epoch.

**P1 / CONFIRMED_WRONG_TRANSACTION_RESULT**。位置：`common/scripted_triggers/nesnd_native_khanate.txt:29-43`；`common/war_goal_types/nesnd_native_americas.txt:31-45`。

Actual frozen humiliation on_enforced with USA's stored actual-dispatched DP, but callback different-same-pair DP of the same type, accepts the callback, sets USA outcome2 and grants NKH first victory reward. Native DP and participants are explicit fixture facts; no war outcome is simulated.

建议：Bind both sides/goal callback to the original country objects, current transaction epoch and exact stored DP, and require the matching dispatched/current case before writing outcome/reward. Preserve separate USA/HUS transactions. Restoration settlement already has an additional stored-play check; do not falsely classify both routes as identical.

### A2-F5 — Preview relies on earlier set/save effects to initialize capacity variables and temporary country/state scopes.

**P2 / CONFIRMED_PREVIEW_REFERENCE_DEFECT**。位置：`common/scripted_effects/nesnd_a2_common.txt:2-9`；`common/scripted_effects/nesnd_native_khanate.txt:138-147`。

Actual frozen nesnd_khanate_army on four populated NKH states, army_size0, preview with writes/saves skipped, reaches nesnd_a2_barrack_capacity while.limit and reads missing var:nesnd_a2_capacity_total. No engine UI result claimed.

建议：Close all construction/army preview reads with explicit has_variable/exists branches; use safe defined values for zero-default counters. Keep actual mutation in hidden execution and native/cost previews separate. Audit the whole helper closure, not this first field alone.

### A2-F6 — Dynasty spawn windows use date as a country trigger.

**P1 / CONFIRMED_UNKNOWN_NATIVE_TRIGGER**。位置：`common/scripted_effects/nesnd_american_restoration.txt:110,113`。

Current generated trigger registry contains game_date, not date; current executable bulgaria_events.txt:162/174/186 uses game_date. Tiger identifies four unknown date fields. History date syntax is a different context.

建议：Use verified game_date conditions while preserving approved character windows, global seen/dead receipts and no resurrection.

### A2-F7 — War dispatch treats alliance and defensive_pact treaty-article IDs as diplomatic-action pact types.

**P1 / CONFIRMED_WRONG_DATABASE_INTERFACE**。位置：`common/scripted_effects/nesnd_native_khanate.txt:189-190`。

Current GAME defines those IDs only in common/treaty_articles, not common/diplomatic_actions; no aliases were located. has/remove_diplomatic_pact expects diplomatic-action type. Tiger emits four missing-item diagnoses. Actual native italian_unification.txt:680-718 filters exact binds pair and alliance/defensive_pact articles then withdraws the matching treaty.

建议：Use the current native pair-scoped treaty route and preserve unrelated third-country relations. Do not globally remove alliances or invent a remove-article effect. Follow the actual native withdraw source and decide mixed-article treaty implications explicitly.

角色判定额外核过不同接口：has_role是specific role，has_role_of_type才是archetype；add_character_role文档明确两种皆可。原生可执行txt使用character_role_general；仅commander_orders/orders.md有旧general示例，不能用该示例抵消当前角色DB和实际执行实例。军队红例只执行冻结中赋军片段，已有真实角色/formation为显式原生事实；未把片段通过冒称整个军政准备已验证。

迁徙的缺global/缺HUS反例是当前项目已确立“不依靠布尔同级短路”的严格AST引用缺陷，不声称已实机看到何种报错或人口结果。原生效果是明确注入的操作边界，未模拟战争或整套经济。

## 未证明的接口与窗口

- **A2-U1 UNPROVEN_BLOCKING：Dynamic formation combat_unit.count。** 10 new Tiger expected-integer diagnostics for var: counts. Engine documentation only shows literal count and no current native variable-count instance was located. Do not treat source arithmetic as proof that native formation accepts the arguments. Requires a source-proven shape or one later targeted engine check.
- **A2-U2 UNPROVEN_BLOCKING：Dynamic set_capital scope arguments。** Four new Tiger missing state-region-item diagnostics. Engine docs say state region, but no actual dynamic scope/var instance was found in GAME. Capital relocation and retained origin capital are not certified.
- **A2-U3 UNRESOLVED_TOOL_SOURCE_SHAPE：Button ai_chance value plus modifier。** Four unknown modifier diagnostics. Current scripted_buttons.md shows base+modifier with explicit trigger; submitted blocks mix value+modifier and no trigger wrapper. Need a source-backed homogeneous shape; documentation example alone does not prove submitted mix.
- **A2-U4 SOURCE_LIFECYCLE_REVIEW_NEEDED：Restoration invitation old window。** Event .10 has no cancellation_trigger; accept option trigger only checks receiving TWT independence/war, while full pending/nonce/applicant checks occur in effect. Current pending expiry does not by itself prove the old option disappears. Effect reentry/nonce must be independently tested after guarded-reference repairs; no actual UI timing claimed.

此外，已有Tatanka在别国/流亡/void或seen/dead时，本国是否仍有合格指挥官与统治者，需要角色修复后完整测试；本轮不为缺模板而提议复制活人。旧goal周度迁移不能证明“读档后首次周回调前的旧和平窗”已安全；该边界与实施报告一致。

## 实际已完成的局部覆盖

- 32 owned SHA、30份有序AST、131对本案双语BOM/header/重复键/有效键集合与显式引用；均在当前固定副本上。文风结论继续由原写作对读承担，未用键覆盖冒充文字质量。
- A1另外21个非重叠owned文件SHA保留；HUS effects只变nesnd_hus_manchu_exodus定义；原.10时钟事件和native primary helper逐AST保留。24个后继普通法均唯一，无混入HUS特别登记法。五份意识形态、法律锁等未扩大。
- Turtle Island三按钮原name/desc/visible/possible/effect主体逐AST保留；直接执行旧effect窗口，在NKH及native_successor两种标记下六例均无原生效果。Cherokee七stub文件逐字节不变。
- 实际script_value执行20个人口档边界；这只证明档位算术，不能证明动态count参数已创建实际formation。
- 实际核心州trigger执行四例：99,999人口拒绝；100,000完整州接受；同人口split-state拒绝；200,000完整州接受。完整1/2/4州事务、连通分量探索、割地提交与原国/新国迁首都仍NOT_RUN。
- 在“割地已经完成”的明确fixture上执行真实50% helper：USA剩余原住民200迁100，HUS400迁200，已在汗国的割出人口100不再计入；重入不再迁。未冒称实际四州create_country已执行。
- 真实40% helper的有HUS控制例：源500迁200，重入不再迁且pending清除；无HUS例触发上述引用红例。
- 汗国wrong-DP实际on_enforced AST产生了真实变量/修正写入；角色片段内存原生ID控制证明适配器并非总拒绝。两项表内“反例测试PASS”仅指成功复现缺陷，**A2玩法判定为FAIL**。

## 停止与交接

70/30两/一/零目的地正向执行、实际1/2/4州完整建国、继承设施/军队容量、正确DP两战结算、40%→流亡→annex完整顺序、NPU/SPU竞争与邀请期限、人物全生命周期、旧goal迁移与完整UI预览，均因相关红例或未知接口保留NOT_RUN，不用手抄状态机或regex presence补一个PASS。

测试适配器初次把culture对象当字典键导致half/refugee控制例KeyError，已修工具并保留初始adapter-observations文件；该错误没有归因玩法。另补了真实culture scalar比较与DP initiator/target链接支持，不接受未知节点为真。全部源控制流从冻结保序AST读取，原生人口/formation/DP事实边界明确。

主汇总：batch-a2-validation.json。原始动态trace：source-effects-matrix.json；结构/保护/双语：structure-contract.json；实际MCP/Tiger及差分同目录。后续由root交Y修A2，修复完整后再冻结，再由独立测试继续未决项。本代理不修A2，等待root的下一批授权。
