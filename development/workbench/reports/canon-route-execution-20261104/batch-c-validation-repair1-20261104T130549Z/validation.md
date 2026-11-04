# C批验证：修复1后再次停止

状态：**FAIL_STOPPED / READY_FOR_REPAIR_2**。当前冻结为`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c-owned-repair1-freeze-20261104T130453Z\mod`；隔离测试快照`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-c-repair1-20261104T130549Z\mod`。全部测试与编辑分阶段执行，本轮没有在测试中修改玩法。

## 已完成

- 31份owned文件字节与冻结清单一致，29份脚本保序解析通过。
- 首次EGY零独立性＋活赞助者预览红例已转PASS。它展开真实冻结AST，并在不执行save_scope_as/set_variable的预览fixture下读取country目标；不是游戏内附庸执行证据。
- 实际stdio MCP已initialize、tools/list，并完成init_game固定快照及5个get_structure符号查询；各调用isError=false。报告`batch-c-validation-repair1-20261104T130549Z/mcp-c-owned.json`。MCP只能证明这次源码查询，不执行国家、条约或战争。
- Tiger1.19.0在固定快照＋本体＋既有只读EAC依赖上运行；仅把含C-owned位置的17条诊断带入本批分类。原始全量留`tiger-raw.json`，C范围留`tiger-c-owned.json`；没有全局忽略来取得通过。

## 新实质失败：停止等待原生接口/作用域修复

1. **C-NATIVE-01 / P1**：`common/static_modifiers/nesnd_egypt_independence.txt:3`引用`building_military_shipyard_throughput_add`。当前GAME/common/buildings/01_industry.txt:318只有`building_shipyard`；当前引擎modifiers.log:3129有`building_shipyard_throughput_add`，不存在军事造船厂键。Tiger的missing building和missing modifier两条是同一根因。此字段来自本轮早期scaffold，仍属于C交付闭包。建议删无效额外项，保留已批准的造船吞吐15%。
2. **C-SCOPE-02 / P1**：`common/scripted_triggers/nesnd_europe_america.txt:56–57`将`TARGET=prev`传入原生保证独立/支持独立helper。原生00_diplomacy_triggers.txt:106–110、124–128在宏展开后又进入treaty/article，`prev`此时是条约，而不是奥地利。建议改稳定`c:AUS`或显式稳定ACTOR参数。这个问题属于宏作用域，不当作普通缺对象预览守卫悄悄修。

同次工具输出还记录：10份文件缺UTF-8 BOM；专用埃及保护国缺5个原生action显示键。这两类可在获准修复阶段做编码/本地化窄修。首次红例原报告仍保存在batch-c-validation-20261104T125656Z，未改写旧证据。

## 分开保留的依赖/工具边界

- `nesnd_small_state_country`六处unknown-field：**EXPECTED_UNIMPLEMENTED**，B2接口未实现；未填假定义，也不是C全面引用通过。
- 原样复制的保证独立article中`ai_opium_dealer_no_alliance_trigger`的other_country严格scope告警：**PENDING_NATIVE_COMPARISON**，尚未用原版同形差分完成归类，不先全局屏蔽。
- 其余nonce/旧回复/政体变化/创建失败，EGY0＋30年/none/亡国/grace，PRUdistinct/形成国，AUS阶段/同侧/领土goal，USA原province/实际goal/白和/ACW/nativeHUS和204对有效双语键矩阵：**NOT_RUN**，遵守下一实质失败即停。

具体诊断及来源在`batch-c-validation-repair1-20261104T130549Z/classified-stop.json`。root确认修复2后再编辑→冻结→重跑工具并续测；不启动游戏，不声称ENGINE_PASS。
