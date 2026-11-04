# 南朝事件可达性与冷日志复核

## 当前批次交付（优先）

最终分支为`exports/japan-annex-recovery-20261031-a1`，精确链C5→Japan A（含Lin A）→A1；source已冻结、map独立最终复核无新增静态阻断，交root合E1/功能文本成单一F1。完整依赖、source证据、guard、真实验证清单和遗留在`evidence/japan-annex-recovery-batch-review.md`；manifest/窄差异在`evidence/japan-annex-recovery-a1.json/.diff`。A1逆父AST核验、12分配反例、Tiger1029→1029新增0；游戏尚未加载本分支。主MOD未合，原始全部任务未完成。

A1保证自有非锚州仍受第三方控制时不提前partitioned；补关东/京都部分成功后的续转；pending重试不重复建国/造人/改首都法律。玩家JAP被原生吞并后的gameover及1日重建能否继续操控仍是实机边界，未偷偷夺USM控制。其它旧失败/退出选项留在遗留清单，本批按40计划四项DEBUG收口，不扩剧情或经济。

## 最新纠正：吞并后接续既有三日本，而非禁止吞并

用户最新边界（root转达）：战目标文件可以修改并参考GAME/MOD；允许吞并JAP，只要随后由事件/JE重建已经设计的三个日本政权。当前P1是**吞并后未重建三政权的断线**。下方“限制吞并/分流战后目标”的早期方案不再作为当前要求。继续DEBUG，保既有剧情/三方领土设计及本地化，不扩写新路线。

当前工作候选`japan-annex-recovery-20261031-a`精确C5父并合Lin A：自有`wg_nesnd_usm_annex`保留原版`kind=annex_country`、所有设置和成本，本内战DP改用它；同原生`on_enforced`后由存活USM登记后续。旧存档既有目标由已登记对象严格限定的`on_wargoal_enforced`兼容监听接续，未覆写全局annex_country。事件annex前登记实际JAP/领土，执行后确认JAP不再存活，随后1日隐藏事件与月度重试共用恢复函数。月脉冲不凭吴国/土地持有自行改造世界，只续办已确认pending。

三锚州为USM实际持有并控制的关东、京都、中国；外部JTK/JIM、第三国领土/占领或无USM时保blocked/pending，绝不夺地或抢现存TAG。先重建JAP再复用现有`nesnd_partition_japan`创建JTK/JIM；角色沿用USM手中现存活人，历史人物已死不复活，普通新监国仅在新国确需时一次生成。尚未封板，正在全局Python/MCP、Tiger与本地负例检查，未声称引擎验收。

起点：run224458实际C5冷日志153条记录；条数不等于独立故障数量。主MOD、当前C5及frozen只读。复用既有原版/EAC归因与southern-scope审查，但重新按C5现代码确认路线，不沿用旧候选已过期的风险结论。

依赖图：引擎on_action／历史初始化 → 活动JE／按钮／外交目标 → scripted_effect → trigger_event → 可见选项／延迟通知 → 人物、国家、战争、市场与本地化。每条边保留文件、行号、触发与可选条件。事件有入边不代表自然可达；自循环、always=no、未挂JE、QA控制台入口须单列。

任务：

1. 归档真实冷日志，分类平台/本体、依赖资源、本MOD冗余、未用/未设变量、事件孤立。不得以冷日志无unknown声称全链有效。
2. 比较作者原始备份与C5中usm_civilwar.4/.14/.17/.19/.20/.22/.25，解释原功能、旧入边、当前替代路径与遗失体验。
3. 扩展检查相关死子链、自循环、正常主线与Japan/海外/外部TAG入口；列实际已验证和仅源码可达。
4. 明确BUG才做独立候选；未完成的设计不以强制挂入旧吞并事件伪装修复。经济与海路改动不混入。

实机验收仍由root执行：正常引导进入、各真实选项、延迟时国家/人物失效、战争及和平结算、恢复/失败和第三方保护。此计划当前是只读审计，不把静态图当引擎执行。

## 用户收口要求与审计结果

停止新增内容，集中DEBUG。用户可读总表与发布阻断在`evidence/debug-status-and-release-blockers-20261031.md`；153条冷日志归档`evidence/runtime-224458-cold-event-audit/`；有序调用图`evidence/south-event-graph-c5.json`。作者版本的7个重点孤立事件均曾有入边，不能再一概称“作者没完成”。

林汉涵最小原线恢复单独在`exports/lin-defection-regression-20261031-a`：精确父C5，只改原`.2.2`拥明选项及`.25`通知，原本地化字节保持；不新增故事、角色、经济、军队或奖励。仅真实活林仍在USM、非君主/储君/流亡、独立YN1选择拥明时同ID迁移，并在转属事实有效时通知。其它国家已持有林时不抢回，死者不重生；反复选择不重复。候选静态/原生验证状态见其JSON，不能因inverse AST通过声称引擎通过。

## 历史方案：限制吞并／分流（已被最新用户边界替代）

源证据：`events/usm_civilwar_events.txt` `.8`现即刻按80%占领全吞；`common/diplomatic_plays/ce_diplomatic_plays.txt:1`的主目标为`annex_country`且mirror=yes。仅从循环排除JAP仍会被原生战目标吞并，故不做假修。

可复用的真实API：

- 现有`common/war_goal_types/nesnd_japan.txt`已采用`kind=custom`、`target_type=country`、`on_enforced`；它可作为真实原生强制执行入口的语法参考，但**尚未证明新南朝自定义目标的完整scope/时序**。
- 原版及原作者用`set_state_owner`转实际state、`create_diplomatic_pact={country=... type=dominion}`重建主从；后者原日本`.22`来自已和平的JE失败路径，不能假定在占领80%但仍交战时可安全强行建约。
- 当前`nesnd_south_chinese_state`为明确地理白名单；混合国保留非目标state/首都的实现已在`nesnd_south_integrate_consented_country`和`nesnd_south_apply_selected_capitals`中。其和平同意guard不能直接作为战败guard复用；只复用已证state/首都API与原地理范围。未来含福建父需新增子州映射，不能拿C5的50州覆盖新图51州。
- 现有`play_as`必须同时验证败者原为玩家、USM没有另一人类玩家、真实结算仍成立、确实面临失去整个TAG，并放在原失败选项的实际点击后；不在预览/立即效果中抢玩家控制权。

执行闭包应为：实际主战目标选择/镜像目标 → 退让或原生胜利on_enforced记录真实获胜方/目标 → 等双方真实停战后处理旧失败通知及选择 → 依据纯大陆/混合/日本/受保护海外分类分配实际state或主从 → 一次结算标记/失效清理。不得用单独80%占领变量等同最终和平，也不得让旧事件弹窗在国家转属/第三方占领后继续吞并。

大陆全白名单且不受海外保护者可整合；混合国仅让出自己的白名单state，先迁政治/市场首都并保有非目标领土，第三国交集和非本人所有权不得误吞。日本仅在保留至少一州且可合法迁首都时适配原割首都+dominion结果；无保留州时不强行灭国冒充此路线。海外保留TAG并恢复主从是本轮root明确的边界，须诚实区别于作者旧`.4`实际同样全吞海外的实现。

这一闭包还需原生博弈退让、双方战争胜负、外国占领、只剩日本/海外反吴leader、玩家失败与读档验收。未完成前列为发布阻断；本次总结不等待大框架重构，也不把局部白名单候选当完整修复。
