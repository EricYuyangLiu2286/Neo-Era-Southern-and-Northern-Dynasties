# C批验证：修复2通过原红例，生命周期新失败

状态：**FAIL_STOPPED / NEEDS_LIFECYCLE_DESIGN_REPAIR**。2026-11-04。对象为`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c-owned-repair2-freeze-20261104T131234Z\mod`；隔离快照`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-c-repair2-20261104T131440Z\mod`。测试阶段未修改候选或冻结玩法，未启动游戏。

## 修复2后的已完成检查

- 31份owned文件SHA与冻结清单一致；29份.txt保序解析PASS。
- 原EGY缺临时scope的效果预览用例PASS。
- 本轮实际stdio MCP完成initialize/tools-list、固定快照init_game及5个get_structure查询；结果文件mcp-c-owned.json，所有call isError=false，未冒称引擎执行。
- C范围Tiger不再报告shipyard错误、AUS宏prev错误、BOM或五个action键缺失。
- 剩余6处`nesnd_small_state_country`为**EXPECTED_UNIMPLEMENTED**，属于尚未接入B2的真实外部接口，不填假定义、不称整包引用PASS。
- 剩余opium严格scope告警已按root要求完成严格归类：候选guarantee_independence的完整ai有序AST与GAME相等；有效00_ai_triggers中该helper的有序AST与GAME相等；相同article ID/field context；单独原版Tiger控制运行在Vic3来源的同一article/helper位置复现相同告警。因此只将此项标**INHERITED**。证据opium-native-classification.json、tiger-native-control.json，未全局忽略其他strict-scopes。

## C-LIFECYCLE-03：活赞助者永久失去持属国能力时无限pending

root特别要求补查此边界，因此在剩余大矩阵之前运行。工具为WORK/tools/test_batch_c_egypt_pending.py；复用已验证的保序AST控制流解释子集，所有实际路线代码来自冻结文件。国家原生事实由fixture明确注入，未知语法报NOT_RUN，不伪造pact创建成功。

fixture：EGY存活、独立、独立性0，mode=1且当前赞助FRA存活；FRA原先可选，现已失去can_have_subjects能力，没有战争，也不在EGY属国树；外部条件保持不变。

结果：

|实际源码行为|观察|
|---|---|
|首次nesnd_egypt_settle_dependence|写pending与pending_explained，发一次nesnd_egypt.5|
|随后64次nesnd_egypt_maintenance|仍pending，未写finished，未建立保护关系，未出现其它解决事件|
|pending写入|65次；每次均无days/months/years期限|
|主JE存续|原生fail已结束父JE；本fixture不伪造重加|
|nesnd_egypt_independence_open|false|
|none按钮实际possible|false|
|六国改选|全部共用已关闭的independence_open资格|

因此在外部条件不变时，源码中没有自动有界终态或本路线的玩家处置入口。普通外交可能在未来改变外部世界，不等于本任务提供了可靠退出。当前通知只要求等待，没有行动效果。

64次调用本身不是引擎时间模拟；它证明当前重试不改变相关持久状态，配合实际pending写入无期限、无计次终态及全部选择关闭，形成可持续的源码死锁反例。这个结论不是本次游戏内观察。

## 建议下一阶段

这是新生命周期设计问题，超出同类scope/BOM自动窄修授权，已停止并交root决策。建议明确：只初始化一次的协商期限；正常活且可以持属国的赞助者仍按原保护国结算；结构上不能建立关系时允许玩家作明确处置或到期承担不同于“赞助国死亡”的失败结果。保持独立性0及原三十年期限，不刷重置/成功奖。未经批准未实现任何新终局。

原始数据：`batch-c-validation-repair2-20261104T131440Z/egypt-pending-lifecycle.json`。其余nonce/创建失败/六约expiry/0+30年等矩阵、PRU/AUS/USA完整行为矩阵和209对有效文本检查仍**NOT_RUN**，在此新实质失败处停止。旧报告/红例/修复1与修复2冻结均保留。
