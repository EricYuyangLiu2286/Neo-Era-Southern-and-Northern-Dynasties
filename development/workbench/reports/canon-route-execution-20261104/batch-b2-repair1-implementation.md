# B2 repair1 实施冻结交接

2026-11-04。**READY_FOR_TEST / ENGINE_NOT_RUN**。执行者 `/root/sol_b2_implementation`，实际父委派配置 **gpt-6.1-sol / medium**。依据root集中修复GO及其对literal AI有限边界方案的明确批准。已停止全部B2源码/本地化编辑；没有在编辑时运行行为矩阵、Tiger、MCP或游戏。

## 新冻结与差异

- owned freeze：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-b2-owned-repair1-freeze-20261104T164006Z\mod`。
- 固定测试副本：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-b2-repair1-20261104T164006Z\mod`，**931文件**。继承原完整A1依赖的931固定副本，再仅覆盖36份B2 owned；未复制变化中的A2/C2或整个C。
- 清单：`batch-b2-repair1-freeze.json`；源码与依据SHA：`batch-b2-repair1-sources.json`。
- 修复前独立备份：`batch-b2-repair1-pre-change.json`；原36份C先与最终B2验证SHA核同再备份。
- **36 owned / 32字节改变 / 4份既有共享或旧India文件逐字节不变。** 30份新脚本均仅额外加BOM，功能修改集中于其中7份；两份loc各只补同一通用desc键。完整可读差异：`batch-b2-repair1-owned.diff`（UTF-8-sig读取后的逻辑diff不把BOM计成文本改写）；BOM专表另存。
- 旧freeze、旧validation、原910/补A1的931快照和红例文件均保留，没有覆盖旧测试结果。

## 已实施

1. **F02**：首次事件资格要求原clock仍存在且尚未选择；duration=1月，与原一个月选择clock一致。承诺成功要求原24月clock仍在；有效在行12/24月项目仍由monthly独立维护，不因选择事件取消而误关。choice与事件issue数值通过明确has_variable分支读取，修同类迟答/取消预览缺值；缺issue的旧active按既有失效出口收束。
2. **F03**：market_verify先处理原deadline/合同失效，再接受own market结果；统一清7项本案核验标记与快照。没有改变真实market.owner、撤pact、拆产业或撤销实际已经发生的市场变更。
3. **F04**：B2自身直接排imperial_line及MUG/BHT/DRA，保留原保护TAG排除。未改变India empire helper或其它国全局身份语义。
4. **F05**：按本机真实事件调用使用literal base/literal add+trigger，保留原接受权重1–95 clamp和拒绝100。原score拆为raw+同名clamped值；事件逐项相同驱动，以11个可越界raw点的literal修正实现截断。完整raw集合公式、父批准与原生证据写入 `batch-b2-repair1-plan.md`；modifier.trigger内部dynamic比较阈值没有冒充权重add实例。
5. **编码/文字**：30份新脚本在原字节前加UTF-8 BOM，不重格式化原行；两条原生modifier缺desc诊断实际共用一个键，补中英一对。原186对文本未改，新合计187对；逐项新增文案对读在repair1 writing-comparison。

**F01已撤回**：四处building_barracks保持原样，GAME显式alias控制留给测试工具。没有改代码讨好错误的资源词典。

## 未运行的检查与下一步

本轮只有源码阅读、集中apply_patch、BOM定向字节前缀、独立备份、SHA冻结、差异及报告归档。**没有运行自己的修复行为测试，也没有STATIC_PASS/ENGINE_PASS。** source/接口差异只是可审查实施，不代表已通过后续测试。

root安排的新冻结后独立测试至少应：
- 重跑F02首次/已选、期限内/到期/到期后改法、运动消失和取消前旧desc/选项；
- 重跑F03原30日期限前后、同帧既有own market、失效pact/政府/宗主、旧serial，并断言市场事实不被回退；
- 对无印度土地的imperial_line与MUG/BHT/DRA、普通ACE及其lineage作F04正反；
- **穷举全部AI驱动组合**，对原冻结score AST与新raw/clamped/event权重实际AST比较，包含经济依赖三段、各kind、军队/GDP/关系阈值、缺对象、下限−12/−2和全部上限点。不得用两个抽样或手抄公式替代源码对照；
- 核30份新脚本BOM、187对双语与共享C1/旧India保留，保留真实native alias控制；
- 然后继续原B2完整生命周期未测项，按先外部后必要引擎的顺序。

主MOD、GAME、A1/A2/C2与人物/历史人口均未写入。技能仅复用现有“原生实例、字段区别、显式分支后读取”规则；未改永久技能。后续独立C2测试待root明确分派，不在本次修复阶段自动开始。
