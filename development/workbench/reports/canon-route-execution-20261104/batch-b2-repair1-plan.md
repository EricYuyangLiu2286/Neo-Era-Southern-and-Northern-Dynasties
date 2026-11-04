# B2 repair1 — 集中修复与原生源合同

2026-11-04；**READY_FOR_TEST / EDIT_FROZEN**。父任务显式GO，配置gpt-6.1-sol / medium。仅编辑既有B2 owned中的源码/双语；A2测试已停止，旧B2测试亦停止。本轮不在编辑时运行行为矩阵、Tiger、MCP或游戏。最终架构/数值仍归root，root已另条消息批准下列literal AI等价方案并要求冻结后穷举驱动组合。

## 基点、范围与撤回项

基点是 `batch-b2-validation.md/json` 最终版和36份原owned SHA。修复前C逐SHA与该清单核同并独立备份，路径存 `batch-b2-repair1-pre-change.json`。旧原freeze、931依赖完整测试副本及所有红例证据不覆盖。

F01的building_barracks误报已撤回。本轮保留四处原生有效alias，不改代码迁就漏aliases词典；测试者应保留05_military.txt:3–4的alias控制。

## 原生AI链与等价合同（F05）

当前GAME：1.13.11 / build24799966；本轮catalog CURRENT，changed_count=0。

实际同类调用：`GAME/events/iberia_events/negotiation_events.txt` 的 `negotiation.1` 选项，约460–468行使用：
```text
ai_chance = {
    base = 0
    modifier = {
        trigger = { ... }
        add = 5
    }
}
```
这是事件选项→原生ai_chance→modifier.trigger→字面量add的实际执行链。本轮只读整个相关选项及脚本值依赖；没有拿说明文件代替实例。

对GAME事件AST的只读定位发现：660个ai_chance.base均为字面量；modifier直属add/factor也未找到动态值的实际实例。曾检索出的 `add = law_estimated_stall_chance/credit/root.income` 位于modifier.trigger里的比较阈值表达式，**不是AI权重add证据**。本案不使用未经证明的动态base或动态modifier.add。

实际改法：事件接受选项使用literal base=30，modifier的所有add也为literal。原kind6/7/8基准分别以−5/−22/+15调整为25/8/45，kind9仍30；所有原关系、接收国违约/战争、可靠支持、依赖、军队/GDP驱动保持同值同条件。拒绝base100不变。缺sender/partner/kind时扣30并令其它驱动false，保留原安全值0。

原动态值内容移入 `nesnd_small_reply_acceptance_raw`；原 `nesnd_small_reply_acceptance` 仍返回同样的1–95截断值，供数值对照与后续读取。事件以raw值触发有限字面量边界校正，未把raw值塞入权重字段。

### raw可达集合的来源

设r=关系≥50、w=接收者违约或外战、s=可靠支持、a=按kind的军队比、g=GDP比，各取0/1；d为经济依赖区间贡献，`d∈{-20,0,15}`，不是两个区间同时加。驱动来自原冻结 `common/script_values/nesnd_small_diplomacy.txt` 的实际分支。

- kind6：`25 +20r +15w +20s +20a +10g +d`；a门槛.4。
- kind7：`8 +20r +15w +20s +20a +10g +d`；a门槛.6。
- kind8：`45 +20r +15w +d`。
- kind9：`30 +20r +15w`。

上述集合仅在以下raw点越界：下限−12/−2；上限kind6的100/105/110/115/120/125与kind7的98/103/108。分别使用literal `1−raw` 或 `95−raw`，其余点不校正。该有限集合及对应实现已获root批准；本节是实现数学合同，**没有冒称已执行组合穷举**。新冻结后独立测试必须穷举全部驱动组合、依赖三区间、军队/GDP门槛、缺对象和旧新score，不能仅抽两例。

## 各修复闭包

### F02 — 首次答复与在行期限

`nesnd_small_episode_valid` 只作为首次选择/事件资格，现要求原episode_clock仍在且尚未选择。原serial、政体、活国/实际议题重验保留。选择后该事件可取消，但12/24月在行项目不使用这个首次选择predicate，不会因此被提前关停。

承诺成功分支显式要求原clock仍在；超时后才通过法律不再取得“按期兑现”的奖励。未选择时missing choice的读取改用有has_variable分支的helper；旧事件desc/选项的issue数值同样经有分支helper，避免取消前的缺值读取。缺议题记录的旧active项目按既有失效清理收束。

事件duration由100改1。此字段按月计，现与开始时一个月首次答复clock相符；不是100日。事件次日弹出也不能延长原clock，迟答仍由clock/serial守卫拒绝。组织12月、承诺24月、镇压12月及24月重开冷却均未改变。若有效期限内实际通过承诺法而原运动随后失去议题，原成功分支仍可兑现；没有要求必须仍保留反对该已通过法律的运动。

### F03 — 市场核验截止先行

`nesnd_small_market_verify` 先处理原30日deadline缺失/当前合同失效，再判断真实own market成功。因此迟于deadline的市场改变不再算本次按期成功。

成功/失败/总清理共用 `nesnd_small_clear_market_verification`，只清本批核验marker、deadline及partner/regime/overlord/serial快照。没有remove pact、撤市场、改owner、拆建筑或退款。已经实际取得的市场仍是现实事实。旧日事件因marker/serial不再有效而停止，不能清掉新事务。

### F04 — B2自己的无地域帝国排除

在B2自有身份NOR中直接排 `nesnd_india_imperial_line` 和MUG/BHT/DRA，保留既有TZ1/YU1/IR1–6及 `nesnd_india_empire` 条件。不改印度帝国helper的全局语义，也不依赖“仍有印度人口州”才排除旧帝国line。

### 编码与修正说明

原36 owned里4份既有共享/旧India脚本不碰编码；30份本轮新脚本仅在原字节前补UTF-8 BOM，保留原换行与其它字节，不批量重格式化。操作清单见 `batch-b2-repair1-bom-changes.json`。

两条missing-localization诊断实际都引用同一个通用键 `state_pop_support_movement_land_reform_mult_desc`（组织/镇压各一处）。新增该键的中英一对，描述真实支持倾向；原186对文本原样保留，合计187对。不虚构两个不同modifier键。

## 后续交接

编辑完整后生成新的时间戳owned freeze与固定依赖快照，清单另存 `batch-b2-repair1-freeze.json`；基于已补齐A1的原931固定副本，仅覆盖B2 owned，避开变化中的C2/A2。旧清单及旧红例均保留。新source契约与SHA在repair1 sources中；新增修正说明对读见repair1 writing-comparison。

**READY_FOR_TEST之后停止编辑。** 本轮不执行自己的行为测试；独立阶段需重跑F02/F03/F04负例及有期限正例、AI全组合等价、BOM/文本、共享C1/India保持和原native alias控制。没有STATIC_PASS或ENGINE_PASS。C2外部测试待root另行显式分派。
