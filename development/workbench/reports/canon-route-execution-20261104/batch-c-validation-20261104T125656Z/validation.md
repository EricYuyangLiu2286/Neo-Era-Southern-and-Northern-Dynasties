# C批冻结验证：首个实质失败后停止

状态：**FAIL_STOPPED / READY_FOR_REPAIR**。2026-11-04。root授权测试阶段；遵守“第一项实质失败后停止，先报告再修复”。候选与31份自有冻结文件均未被本测试修改；没有启动游戏。

## 测试对象与依赖

- C自有冻结：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c-owned-edit-freeze-20261104T124748Z\mod`。
- 隔离快照：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-c-20261104T125656Z\mod`。
- 快照构造：固定父备份完整复制，再叠31份C冻结文件。不是从正在被A/B编辑的整个候选做镜像。
- 显式依赖：根代理先前写入的EGY历史宗属、法埃历史条约、旧regional/veiled JE关闭文件；`nesnd_italy_country`从实际nesnd_civic_routes.txt提取完整原始AST文本，保留源SHA/行号/切片SHA。详见`batch-c-validation-20261104T125656Z/snapshot.json`。
- kind5的`nesnd_small_state_country`仍未实现，作为**EXPECTED_UNIMPLEMENTED**外部接口记录；没有添加占位定义，也没有把整包依赖记为通过。

## 已运行及首个失败

|检查|结果|范围|
|---|---|---|
|31份文件SHA对冻结清单|PASS|隔离快照的C-owned字节一致|
|29份.txt保序解析|PASS|只证明可解析，保留重复项；不是字段/引用/作用域完整验证|
|EGY零独立性＋活赞助者，未建立临时scope的效果预览|**FAIL**|实际source AST展开nesnd_egypt_settle_dependence，country目标在读取时为空|

失败位置：`common/scripted_effects/nesnd_egypt_independence.txt:88`。

实际执行的源码链：

1. 国家fixture为EGY：存活、独立，独立性0，当前投资者是存活且可持属国的FRA；未有finished、pending、grace或已尝试标记。
2. 从冻结AST进入`nesnd_egypt_settle_dependence`，按真实trigger_if/if/else_if和helper展开。布尔兄弟条件全部求值，不假定AND/OR短路。
3. 预览fixture不执行`set_variable`、`save_scope_as`等写入。这是项目已经明确必须支持的预览边界，不模拟真实建国/附庸结果。
4. 程序走到`var:nesnd_egypt_investor`的FRA scope，`create_diplomatic_pact.country = scope:nesnd_egypt_subject`读空；没有独立exists分支阻止它。

本机规则依据：NESND `references/syntax-and-routing.md`“引用安全”要求预览不能假定前面的save_scope_as已执行；`references/validation.md`“hidden_effect的真实边界”明确hidden包装不提供这种保证。这是**静态引用安全失败**，没有把外部fixture冒称本次游戏内error.log复现。

## 复现工具与语义边界

工具：`WORK/tools/test_batch_c_preview.py`。它从冻结source解析真实函数，fixture只提供country原生事实；未知节点抛Unsupported，绝不默认通过。不是按期望重写一份平行逻辑，也不模拟create_diplomatic_pact是否真的建立关系。

原始结果/源码调用链/预览操作轨迹：`batch-c-validation-20261104T125656Z/first-stage-results.json`。运行退出码1。结果包含FRA为实际actor、缺失目标scope名、source文件与行号。

## 未运行

根据首错即停，本轮没有继续执行：nonce/迟答/缺国/政体变化/条约创建失败矩阵；六历史条约与1845；0＋30年/none/亡国替换/保护grace其余矩阵；PRU distinct/NGF/GER；AUS stage/side/goals；USA省份归属/wargoal/白和/ACW/nativeHUS；204对双语有效键及native字段引用检查；Tiger；实际stdio MCP。

这些都标**NOT_RUN**，不继承任何旧候选PASS。31文件解析通过不改变此结论。

## 建议的下一修复任务

埃及目标固定且此effect限定EGY。把标准与专用保护国的country参数改为受现有国家身份/存活资格保护的`c:EGY`，删去仅为这两个调用服务的临时`nesnd_egypt_subject` scope；或为临时scope增加真正分支守卫，但固定目标更直接。当前尚未实施任何修复。

root发修复指令后只改该具体失败闭包，重新冻结SHA，再重跑同一红例及反例，继续剩余矩阵。测试与编辑不同时进行。C2后续路线仍未开始。
