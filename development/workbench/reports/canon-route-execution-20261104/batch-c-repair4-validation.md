# C1 repair4 冻结外部验收

2026-11-04。实际显式配置 **gpt-6.1-sol / medium**；委派证据：`/root → /root/sol_c1_frozen_validation` NEW_TASK。结论：**STATIC_PASS_C1_WITH_EXPLICIT_DEPENDENCY_AND_WARNINGS / ENGINE_NOT_RUN**。没有发现应中止并要求玩法修复的源码行为反例；以下依赖与告警未隐去，不宣称整个候选无错误。

## 对象与身份

只测冻结 `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c-owned-repair4-freeze-20261104T145402Z\mod` 的31份owned及固定依赖快照，不测试持续变化的全C。准确冻结清单是R/batch-c-repair4-freeze.json；请求中的repair4-plan.md实际文件名为batch-c-repair4-plan.md。隔离快照 `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-c-repair4-20261104T150000Z\mod` 从repair3固定依赖快照继承，覆盖31份repair4 owned，并对历史SIH等只读依赖逐项核SHA。测试结束31份freeze/隔离快照与清单仍逐字一致。snapshot.json保存878份快照文件SHA和依赖来源。主MOD、候选、冻结玩法、GAME均未编辑；未打开游戏。

GAME catalog status：1.13.11/build24799966，CURRENT，changed_count=0。已读项目工程适配、恢复图、NESND目录/验证/日志优先规则、repair4计划、实现报告、source contract与只读Sol审查；本轮不写玩法，复用计划记录的完整原生保护国/subject type/事件取消链。

## 实际运行与结果

- 29份.txt保序解析、31份owned SHA核对通过。
- 埃及新即时结算矩阵 **17组**通过：六国缺失/死国/附属/独立；标准创建、标准失败转专用、只专用可用、两条创建均失败；none不重抽；亡国/附属化替补不重置进度；全部候选无资格立即一次终局；旧pending独立/实际保护国/第三国附属/已finished迁移；JE invalid先于weekly；0与30年两种回调顺序；原GDP压力和附属赞助停止−1；旧事件/JE退役。
- 原路线矩阵 **17组**重新通过：nonce/迟答、关系/政体/原生权限、条约创建失败后不发奖、PRU三个不同盟友与NGF/GER、AUS阶段/参战后验/精确战争回调/白和平、USA原province所有权与精确目标/ACW/原住民HUS退出/单次宣称/创建失败、六约方向和仅旧约1845退出。历史SIH宗属/条约数据SHA保留；不把历史签约资格等同当前赞助资格。
- 新共享请求矩阵 **13组**通过：实际send保存双方政体；当前有效请求保持；伙伴附属/死国/缺对象、发起国死国、双方政体变化、权限/关系失效、旧档缺快照；事件cancellation_trigger成立，现有maintenance在45日clock仍存在时清理；serial和冷却保留；旧nonce回复/取消不擦新事务；USA只选实际独立外资条约替代，既有条约不withdraw。
- 补边界 **3组**通过：共享kind5既有投资存量资格失效与收益清理（无B2假定义）；finish清投资人后final_patron仍支持通知，关系丢失仅取消通知；全owned无旧pending/deadline/grace/attempted新写入；.5/.90/.91全部惰性。
- 预览闭包 **13组**及独立首次零点反例通过：所有effect的save/set/remove/change跳过，hidden_effect仍遍历；有效/缺失/死国/附属/终局投资人、六选择helper、共享send缺scope条件均不越过缺对象。不是实机UI悬停证据。
- 双语210对有效C键：BOM/header、无重复、键集合一致、显式文本引用有效覆盖、无90日/两日旧期限内容；退役JE隐含键告警另列。作者文案逐项对读见implementation保留的writing-comparison，未用键检查替代文风审查。
- **实际stdio MCP** initialize/tools-list、snapshot init_game、8次get_structure均isError=false；查询包含即时settle、current_request_valid、protected_fact、请求事件、reply_valid、AUS、USA与投资JE。MCP仅查询结构。

## Tiger差分与未完成依赖

新旧均实际Tiger运行；对repair3同owned诊断按key/message/路径/原文归一（不以变动行号制造差分）。repair4 owned：6条unknown-field、1条strict-scopes、2条missing-localization；相对repair3新增2条warning，移除0条。

1. 六处`nesnd_small_state_country`为 **EXPECTED_UNIMPLEMENTED B2**。不插占位；kind5完整创建/接受正向入口资格仍 **NOT_RUN**。共享投资存量已实测；kind2/5分支的同级exists及独立条件已按实际源核查，但不冒称B2已完成。
2. opium严格scope为 **INHERITED**：当前article与有效helper保持旧SHA及AST；复用repair2原版Tiger控制/完整article-ai/helper同AST归类证据，仅此项，不全局忽略strict-scopes。
3. **两条新warning保留**：退役`nesnd_egypt_protection_negotiations`缺隐含标题与reason。该兼容壳possible/show=false、invalid=true且无effects/buttons；其旧玩家文案被删除。没有将此新告警标成继承、没有补虚构可玩日志、没有改冻结。若要求Tiger零新增，可在后续独立文案修复轮次保留两条退役兼容标题；此处仅报告，不自行改源。

## 证据和能力边界

证据目录：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\canon-route-execution-20261104\batch-c-validation-repair4-20261104T150000Z`；逐项索引和工具SHA见同名JSON。核心文件：egypt-repair4-matrix.json、routes-matrix.json、requests-repair4-matrix.json、extra-repair4-boundaries.json、preview-repair4-closure.json、localization-repair4.json、mcp-c-owned.json、tiger-repair4-delta.json、snapshot.json。

所有行为检查都读取冻结的保序AST与宏调用；没有手抄路线状态机冒充游戏。适配器新增只支持当前源码出现的原生谓词/作用域值形状；未知语法返回NOT_RUN。country事实、can_have_as_subject结果、create pact/treaty/backer成败显式注入；64次effect调用是重复写入/终局幂等检查，不是64周引擎运行。测试工具旧报告保留，新工具使用独立repair4配置，不覆盖全局current索引。

本报告不证明原生create当帧时序、自定义subject type后帧存续、事件实际取消帧、实机预览、AI随机选择、自然时间与存读档迁移。没有ENGINE_PASS。技能维护已复核，无新永久接口/版本事实，未改技能。
