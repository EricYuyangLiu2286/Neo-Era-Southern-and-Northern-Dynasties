# A2 repair3 — READY_FOR_TEST

已冻结于 `2026-11-04T17:31:59Z`：`WORK/backups/batch-a2-repair3-owned-freeze-20261104T173159Z/mod`。清单 `batch-a2-repair3-freeze.json` SHA256 `e09f1936b960aa042d4d5d3b919ad167c23dffd463c67655ba5dbe3124d5df95`；33个所有权文件，16个相对repair2变动（含机械BOM）。状态READY_FOR_TEST，已停止编辑源码。

执行者 `/root/sol_b2_implementation/a2_repair3_confirmed_batch`；父任务明确指定 `gpt-6.1-sol / medium`，角色为新修复编辑，非本次独立测试者。只编辑独立候选 `WORK/exports/canon-route-execution-20261104-a` 的原33个A2所有权路径；主MOD、GAME、历史人口及其它批次只读。repair1/2冻结与原始失败证据保留。

本轮读取 NESND技能、工程适配、恢复map、目录路由、引用安全、数值契约及玩家写作技能；catalog status 为 CURRENT，当前游戏1.13.11/build24799966，changed_count=0。没有运行行为解释器、Tiger、MCP、游戏或其它行为测试。

## F01：root最终架构与数值裁定

root明确允许NKH最多4支、复统国家本案实际1或2支新formation；禁止跨州笛卡尔枚举及40个单营模板。每州实际空额沿 `state → every_scope_building(limit is_building_type=building_barrack) → every_combat_unit` 统计，`max(军营等级−现存单位数,0)`。继承军队和建筑不拆、不搬、不重复发放。先用实际最大空额州，分州新增总量不超过其空额；全国新增只消耗人口档目标与现有army_size之间的正差额。

扩建全国总等级最多补至人口档目标；已有全国等级超过目标时新增0且保留全部已有等级。每州新增等级最多为原PER_STATE：NKH target/4（最高10），复统target/实际有人州数。扩建选当前军营等级最少的有人州，不要求继承后的最终等级均匀，也不为固定均分营数补造额外军营。

root明确纠正旧逐州舍入：NKH全国新增炮兵 `floor(deficit*0.20)`，复统 `floor(deficit*0.25)`，其余步兵。旧NKH `4*floor(deficit*0.05)` 在小差额丢失炮兵；本次不继续保留该旧实际舍入。先在最大空额州分配全国剩余炮兵；每次扣减全国待补总数和待补炮兵，其余分州保持守恒。既有人口档（NKH8/16/24/32/40；复统2/4/8/12/16/24）不变。脚本中遗留的未调用quarter数值定义未改；当前军队调用已全部改走共享raise helper。

实现落在 `common/scripted_effects/nesnd_a2_common.txt`、两个原army入口及现有NKH script_values文件。共享literal dispatcher只有单州D=1..40、A=0..min(D,10)的395个固定组合；每块最多两种正数单位行，0人数行省略。没有跨四州枚举。`create_military_formation` 内保存实际新formation scope，存在后才扣待补数与分配将领。

每支新formation先选同国现有未分配general，不足才创建一位普通将领并分配到该确切新formation。不会夺走继承部队的将领。Tatanka与Rumi的原一次性人物创建移到本案army准备前；模板/seen/dead机制不重写，普通将领不是同名人物复制。旧“随机一支军队、随机一名将领”的尾处理删除，避免它覆盖上述对应关系。永久prepared收据与原调用边界继续阻止月度补兵。

原生完整链：GAME `common/buildings/05_military.txt:3–8` 把barrack声明为招募战斗单位建筑；本机engine `effects.log:4671–4675`支持country/state建筑迭代，`:1306–1311`支持building战斗单位迭代；native `common/scripted_effects/00_victoria_scripted_effects.txt:3–16` 和 `events/soi_events/00_ep1_kazakh_events.txt:87–100` 为实际固定人数编制；`common/history/military_formations/03_military_formations_north_africa.txt:91–100` 实际在create_military_formation内save_scope_as并将角色transfer_to_formation。`effects.log:37330–37334`明确transfer输入character、目标formation；`triggers.log:10503–10508`提供has_military_formation，角色DB `common/character_roles/00_auto_assigned_roles.txt:37–47`把general archetype连到实际角色；`events/africa_colonial_events_02.txt:109–115`有普通is_general创建，create_character的on_created字段见effects.log845+。本轮不推断引擎会自动扩建或拒绝不合法营数；没有这样的行为验收。

## F02：完整callback引用分支

`nesnd_restoration_goal_pair`最外trigger_if只检查callback target/DP、当前epoch及对手对象存在；在真分支才读取DP、当前对手和epoch。目标国家又有独立trigger_if，在其epoch及对手存在后才比较双方epoch和反向对手。每个缺失分支明确false。`nesnd_restoration_settlement`外层if先核callback对象和stored-DP变量存在，内层才调用pair及直接比较stored-DP。原exact-pair/epoch/DP、reentrancy、settlement_done、迁徙→流亡→吞并→结果的顺序及所有结局不变。

调用者为本批custom wargoal的valid/on_enforced；原生 `common/war_goal_types/war_goal_types.md:26–55`声明ROOT=holder、target_country和diplomatic_play等scope，原生annex_country定义提供相同目标范围。存在性与读取必须分支的本项目规则见NESND syntax-and-routing引用安全章节；当前GAME `common/scripted_triggers/00_scripted_triggers.txt:44+`提供trigger_if语法实例。没有把并列exists/has_variable当作短路。

## F03：按钮AI接口

三按钮现用当前实际GAME `common/scripted_buttons/00_scripted_buttons.txt:490+、636+` 的script-value形状 `value`、`if={limit={} add=N}`；不再采用stale markdown示例的base/modifier。保留recognize30＋native_share30＋radicals30，negotiate50，suppress15＋army20＋laws20。不是事件ai_chance格式迁移。

## F04：六个隐式双语键

补齐NKH、NKH_ADJ、两种DP的desc/tooltip，两语言各6键；原134对正文保留。采用既有“大平原汗国”与真实吞并/羞辱诉求；tooltip仅引用标题和说明。逐键原文、候选、效果与结论见 `batch-a2-repair3-writing-comparison.md`。实际调用闭包由两种DP→本批war_goal_types→对应settlement/on_enforced构成，不新增故事或效果。

## 编码、来源与冻结边界

repair2清单baseline_sha256=null的10个全新A2 .txt均机械增加UTF-8 BOM；其余原有文件保留编码。除本轮实际功能修改的common helper与NKH values外，BOM-only文件剥除BOM后与repair2字节一致，见bom.json。两份本地化继续BOM和正确language header。BOM不是行为修复。

纠正历史说明：literal-capital输入是800个有效state_region定义，包含sea定义，并非800个陆地。现有owner-state守卫让sea分支无合法owned-state候选；本轮保留原代码和800有效定义，不将历史措辞错误称为已观察到的玩法BUG，也不扩大设计删除sea。原repair1报告保留历史，不回写其旧结论。

## 交给独立测试的矩阵

- 复用repair2原有通过证据时绑定新源SHA和受影响闭包；不得把修复报告当作行为pass。
- NKH每个0..40差额、复统0..24差额、每个当前人口档；0差额无新增；原实际10/10/0/0继承单位对10/10/10/10军营反例；任意更大继承空额；已有容量大于目标；现有等级不足；某州新增已达PER_STATE；非有人州；无有效空额。核全国人数/炮兵、每州空额、全国和逐州新增等级预算，继承对象与将领分配不变。
- 单州395个literal组合正数/求和/类型/目标state；实际按最大空额分派不超过4/2支；新增formation各有同国将领；优先未分配者、无可用者普通生成、Tatanka/Rumi不重复；prepared后月度/重入不补兵。核原生save_scope_as返回、实际单位和将领持久性，仍为ENGINE_NOT_RUN。
- F02缺callback DP、缺target、缺任一方epoch/对手、旧/错DP、错epoch、反向对手、重复终局、正常双向结算；所有缺引用应false/no-op，正常结果及一次迁徙和吞并顺序保持。
- F03所有share/radical和army/law驱动组合，对照原意权重表达式；按钮解析和实际选择另验。
- F04有效GAME+候选双语隐式键覆盖、BOM、标题引用、实际UI显示；机械BOM-only文件体与旧冻结一致。

只执行authoring delimiter/encoding/diff与SHA冻结，不运行上述矩阵。本次交付为READY_FOR_TEST，不是STATIC_PASS、SOURCE_AST_PASS或ENGINE_PASS；冻结后停止编辑，等待另一个独立测试阶段。
