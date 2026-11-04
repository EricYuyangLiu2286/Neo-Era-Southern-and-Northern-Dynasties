# Spec review — four-feedback candidate

父提交 `c4626514277991a415283897af47769e12495138`；独立基线 `backups/pre-change-journal-war-feedback-20261103T222744Z/mod` 对候选 `exports/journal-war-feedback-20261103-a`。审查仅依据本轮 [spec](spec.md)；CURRENT 1.13.11/build 24799966。未开游戏、未改候选。

1. **[P1] 非行在接收国再败时，皇帝会重新进入随机杀人。**规格第4项要求“皇帝不进入旧随机杀人处置”。[迁逃效果:38](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-war-feedback-20261103-a/common/scripted_effects/nesnd_south_holdouts.txt:38>)仅给HNA/SIH设置行在标记，但随机host包括GNG等其它拥明国。GNG接收皇帝后再次败退，不满足第54行的行在保护入口，会进入[旧投降事件:1019](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-war-feedback-20261103-a/events/usm_civilwar_events.txt:1019>)，其中所有成年人物均参与2流亡/5死亡抽签。应独立识别所有合法明帝寄居者，并在任何旧处分/吞并前再次迁逃；不必改变接收国国名、国主或政体。

2. **[P2] HUS添加入口尚未受资格约束。**规格第3项要求“开局长期共和不应收到原生消灭君主制JE”“入口资格/无奖励invalid处理”。[候选JE:86](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-war-feedback-20261103-a/common/journal_entries/zzzz_nesnd_hus_native_monarchy.txt:86>)只提供事后invalid；未覆盖[原生transition_off_of_monarchy_effects:2664](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2664>)的计数初始化/add入口。HUS历史激活共和或以后脚本重激活时仍会加入错误JE，再等失效清退。应仅给该末尾add块加HUS资格守卫，保留原前半处理与其它国家逻辑；来源报告已说明此边界。

日本绝对进度/owner计分、印度显示与累计分离、CNE实际protectorate确认、每轮国家标记与拒绝/超时后继未发现其它确定规格偏差。真实吞并/角色转属、旧bar迁移与事件取消时机仍是ENGINE_NOT_RUN；源码审查不证明这些引擎行为。

## 修正复审

原两项发现关闭：`zzzz_nesnd_hus_monarchy_entry.txt`与当前原版effect保序token对比，仅增加添加资格；迁逃已覆盖任意寄居国，旧`.5`在随机处分前调用保护事务，保留接收国国主/政体，并确认转属或流亡后才允许吞并。日本新bar即时设绝对值、印度短缺country参数调用闭包、AI权重trigger包装均已复核。

本次新增2项待处理：

3. **[P2] 旧僵局出口仍可绕过新队列结算。**规格第5项要求“单轮战争结束不代表整个南朝争端结束”。[旧deadlock条件:12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-war-feedback-20261103-a/common/scripted_triggers/nesnd_court_followup.txt:12>)只检查和平、吴已立及压力，不排除未解决本土holdout；24个月后`.19`可调用[旧结算:44](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-war-feedback-20261103-a/common/scripted_effects/nesnd_south_reconciliation.txt:44>)直接置settled。因此外交条件长期阻塞再战时，该出口会清退继承面板，下周新wu_tick又撤销settled。须只在战后存在未解决队列时拦截此出口，保留战前路线。旧镇压JE完成与`.8`即时效果也应共享最终结算守卫，覆盖court身份没有opposition标记、旧排队胜利事件这两类边界。

4. **[P2] 迁逃失败的归降事务没有后继。**规格第6项要求归降执行吞并并先保护明帝。[归降效果:132](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-war-feedback-20261103-a/common/scripted_effects/nesnd_south_holdouts.txt:132>)先mark_answer；若随后设置`nesnd_ming_flight_blocked`，会跳过吞并，且不进入任何重试、抵抗或求助队列。answered等于enrolled又使offer_due永久为false。成功后才消费答复，或失败时恢复可达重试出口；不能靠安全阻止吞并把国家永久悬置。

上述为源码分支问题；没有声称已在引擎触发迁逃失败或旧事件抢跑。仍未启动游戏、未修改候选。

## 最终复审（2026-11-04）

**剩余发现：0；前两轮共4项发现全部关闭。**

- HUS入口保留原版完整处理，仅在添加JE前检查限定资格；原错误JE通过无奖励invalid退出。任意接收国寄居的明帝与预先保存的继承人均先迁逃，确认转属/流亡后才继续旧处分，接收国国主和政体保持。
- `nesnd_south_deadlock_context`现在排除“真实战争已发生且尚有未解决本土holdout”。旧镇压JE、胜利事件`.8`的入口/取消/即时/after统一使用`nesnd_south_wu_total_victory`，要求真实和平、无待处理holdout及无非吴附属的存活反对国；旧战前协商与实际反吴总胜利路径仍各自保留。
- 归降仅在吞并后实际`is_country_alive=no`时消费答复并标resolved。迁逃或吞并失败保留原轮次与可重试资格；从北朝拒绝分支进入时，其拒绝标记也保留后继。再战仅在创建实际博弈后递增轮次并消费等待标记；CNE回复仍核对申请国家、轮次与实际保护国关系。
- 日本绝对进度即时初始化及owner计分、印度显示/累计分离及三个短缺调用的国家参数未见新增规格偏差。

受审27个变化玩法文件的逐文件原始SHA-256与保序token SHA-256保存在[最终指纹](spec-review-final-hashes.json)。聚合保序token指纹：`247cc4410af63b3f718916535f7eb3a53400e0361f44235be4570bac1e50677d`；该值排除字符串之外的空白与注释，后续仅尾空白归一化不改变此指纹，原始文件哈希可能改变。

边界报告为PASS且明确`engine_verified=false`。本次结论为限定差异的源码审查，未开游戏；角色转属/流亡、吞并、旧JE恢复、外交博弈与取消时序仍不作引擎认证。

## 交付冻结等价核对（2026-11-04）

冻结清理后重新读取全部27个受审玩法文件，并逐项比对`spec-review-final-hashes.json`：**27/27保序token哈希一致，0个token变化**。仅`ce_diplomatic_plays.txt`、`ce_usm_the_last_days_of_ming.txt`、`zzzz_nesnd_hus_native_monarchy.txt`及`usm_civilwar_events.txt`共4个原始SHA改变，与交付说明的清理集合一致。聚合保序token SHA仍为`247cc4410af63b3f718916535f7eb3a53400e0361f44235be4570bac1e50677d`。

本次核对的准确正则、序列化说明、冻结后逐文件原始SHA及比对结果见[交付等价证据](spec-review-delivery-equivalence.json)。未修改候选、未运行游戏；Spec剩余发现仍为0。
