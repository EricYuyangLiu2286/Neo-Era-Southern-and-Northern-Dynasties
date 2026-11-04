# C1 repair4 只读脚本审查

2026-11-04。任务：脚本实现审查与潜在BUG识别。实际显式配置：`gpt-6.1-sol / medium`；委派证据为本次 `/root → /root/sol_c1_review` NEW_TASK。没有推断其它代理配置。

审查对象：`C = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a` 当前repair3源码，以及 `R = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-route-execution-20261104` 下 `batch-c-repair4-plan.md`（PLAN_READY，尚未实施）。主MOD、GAME、候选游戏脚本均只读；只写本报告。未启动游戏、未运行行为测试、未把历史PASS认作repair4验证。

已读NESND技能、项目工程适配、恢复索引、目录路由和引用安全规则。catalog status：1.13.11 / build24799966，CURRENT，changed_count=0。原生复核：GAME `common/diplomatic_actions/31_power_bloc_force_become_subject.txt:41–65`、`events/iberia_events/independence.txt:22–28,110–114`；直接create保护国有原版实例，取消与普通after不是同一种回调。

## 结论

未发现repair4方向必须撤回的问题。计划已覆盖现存“附属SIH可被选为当前主要投资人”和旧90日pending设计；没有发现额外的、已能证明计划必然实现错误的BUG。下列两处是实施前应写清的契约缺口，属于潜在BUG，不能当作尚不存在的repair4代码已失败。另列实际闭包清单，防止仅改按钮的局部修补遗漏。

## 潜在问题

### P1：新建保护国资格不能复用于已成立关系的后置确认

位置：R `batch-c-repair4-plan.md:51,55,66–68,86`。关联当前源码：C `common/scripted_triggers/nesnd_egypt_independence.txt:63–68`；C `common/scripted_effects/nesnd_egypt_independence.txt:75–80,108–111,120–127`；C `events/nesnd_egypt_independence.txt:8–12`。

可复现输入：EGY独立性0，当前投资人FRA独立且合法；create成功，EGY立即成为FRA直接保护国。或者旧pending存档在载入时已经是该投资人的真实保护国。

风险：计划要求“同一明确资格契约”，但第66行把EGY仍独立列入选择/最终收属资格。若后置确认、迁移真实保护国分支或通知取消直接重用这一全量谓词，关系一成功便因EGY已是属国而变false，成功会被误判成外部收属或失败。另，当前finish会删除investor；finish之后通知如重用当前`protectorate_confirmed`，也必定因变量不存在而取消。

建议：明确三个层次：投资国自身存在/存活/独立；新建路径额外要求EGY独立、无战及type可收属；已成立事实仅用真实直接宗属和保护国type核对。终局通知在finish后需要的事实应取终局快照/专用终局对象或安全的当前overlord分支，不能依赖已经清掉的主要投资人变量。后置确认必须先于finish清理。

### P2：旧pending迁移需要先记录旧状态，再清变量和替补

位置：R `batch-c-repair4-plan.md:53–55`。关联当前源码：C `common/scripted_effects/nesnd_egypt_independence.txt:40–51,75–80,166–177`。

可复现输入：旧repair3存档带settlement_pending/started，EGY仍独立，独立性0；另一个输入为旧pending且EGY已是其原投资人的直接保护国。首次weekly maintenance处理。

风险：第55行“首先清旧待收属变量”没有明确先保存pending迁移判据。若先清pending再按`has_variable=pending`判断，迁移会失去入口；若保留现有maintenance先replace顺序，套用含EGY独立条件的资格后又可能先清/重抽原投资人，丢掉用于确认旧保护国事实的对象。结果分别可能是0点悬置或真实保护国被误记外部收属。

建议：进入maintenance时先以当前匹配对象、finished、旧pending和真实关系决定互斥迁移分支；可在同一作用域使用有exists保护的临时迁移标记/对象，再清所有旧字段。已finished只清残留。未finished先确认旧事实/外部属国，再对仍独立的EGY做替补和一次即时结算。不要新增延迟或期限。

## 已核闭包与必须落地的现存缺陷

下列是当前repair3源码的真实行为，repair4计划已有对应修复，不作为“计划遗漏”重复报错。

|范围|当前实际位置|输入与现状|计划落实要求|
|---|---|---|---|
|EGY选择|C `common/scripted_triggers/nesnd_egypt_independence.txt:33–50`；六按钮调用在buttons文件3/18/33/48/63/78行|SIH是USM dominion，仍能通过alive及“不是EGY属国”条件|六按钮同级exists及可选country-link内is_subject=no；执行层再次结构化检查|
|EGY替补及月扣|C triggers同文件10–20,56–61；effects40–51；script_values8|投资国附属第三国仍被alive认可；替补也允许第三国属国；月扣仍−1|替补可用集合与random集合一致；收益、月扣、JE终局、执行都接新的资格定义|
|EGY即时终局|C effects81–140；JE33–45；events27–45|当前仍写90日pending、2日grace；旧事件能结算|按计划退役执行链；.90/.91惰性，不从旧事件清当前事务；JE所有0点路径最终一次finish|
|EGY外部属国|C JE35–45；effects101–105|当前非pending的外部收属经on_invalid直接finish，不写external标记/通知|接计划独立的external分支，先于收属创建，不替换第三国宗主|
|共用投资请求|C `common/scripted_triggers/nesnd_canon_diplomacy.txt:45–55,85–93,115–120`|kind2/5、已存investor、USA条约替代均缺投资国独立检查|四处同源资格全部修，不只send/accept或按钮；真实既有条约不withdraw|
|共用取消|C events `nesnd_canon_diplomacy.txt:13–19`；effects67–71|实时request_eligible失效只隐藏接受，取消仅检查reply_valid；维护只在clock消失后清请求|按计划取消+现有maintenance；两个regime快照存sender变量；缺快照安全取消；helper保留serial和cooldown|

## 无额外发现的项目与边界

- 死scope：当前pair_valid、reply_valid、request_eligible、investment_valid及directed_article均有对象存在分支。未发现这些函数中新增的确定空scope读取。新维护重建scope时仍须分别保护对象和数值；不能只用has_variable证明国家变量还可解析。
- hidden_effect预览：六个EGY按钮和共享请求按钮均能进入完整helper闭包；hidden_effect不构成保护。现有selection/refresh通过helper中exists分支保护investor读取；send通过request_eligible的scope存在检查保护后续对象链。没有发现可据现有源码证明的额外预览报错。新增加的快照读、迁移对象、后置关系读应同样逐层检查，不能假定前序set/save在预览中执行。
- 重复请求/终态：当前reply_valid校验sender当前serial/kind/partner/clock及政体；拒绝迟答不能跨nonce清理。计划保留serial和冷却、失效只清当前事务，方向正确。新clear helper应同时清新快照字段；不删除递增serial。埃及finished守卫与互斥终局可阻止重复处罚，必须保留在实际effect入口。
- 历史SIH：C `common/history/diplomacy/ce_subject_relationships.txt:2–5`确为USM→SIH dominion。历史条约SIH块在`common/history/treaties/nesnd_egypt_1825.txt:22–31`；保证条款例外在`common/treaty_articles/zzzz_nesnd_egypt_guarantee.txt:36–75`。历史例外不是当前投资人资格；保留这些只读历史权益与禁止当前附属SIH被选择并不矛盾。1845维护仅withdraw登记的条约，未发现其直接吞掉所有未来外交条约的循环。
- 未新跑Tiger、MCP或矩阵。本报告是只读源码/计划审查，状态为REVIEW_ONLY / ENGINE_NOT_RUN；不是STATIC_PASS或ENGINE_PASS。当前修复尚未实施，必须在冻结实际repair4代码后才能确认两项潜在风险已消除。
