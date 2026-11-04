# C1 接管／修复4计划：独立投资人和即时收属结算

2026-11-04；**PLAN_READY，等待GO**。仅源码研究及报告，没有改玩法或运行测试。主MOD仍为固定父 `b94582ecec7b0b6dd5620a184658190157fc1729`；唯一候选为 `WORK/exports/canon-route-execution-20261104-a`。GAME 1.13.11/build24799966；catalog CURRENT、changed_count=0。

本计划替代被用户否决的 repair3「90日保护交涉」。root已同意方向：不虚构on_cancel；用原生cancellation_trigger取消失去资格的事件，并由既有maintenance清理当前失效请求；埃及零独立性立即结算，不等期限。GO前不实施。

## 1. 接管时证据状态

旧 `batch-c-validation.md` 仍记录repair2的64次维护无限pending红例。随后repair3文件夹已存在16组埃及矩阵、17组其它路线矩阵的PASS_SOURCE_MATRIX、实际MCP响应和Tiger输出；它们证明的是**旧90日方案**及其冻结源码，不能当作本次新设计通过。

保留不改：`batch-c-repair3-plan.md`、`batch-c-repair3.md`、所有repair1/2/3报告目录、独立owned freezes和validation snapshots。实施前复制当前owned-SHA、验证索引、工具版本及文案比较到单独 `batch-c-before-repair4/`，新报告标记旧90日行为证据「设计已废止，历史证据保留」。不删除旧红例，不重写为从未失败。其它PRU/AUS/USA通过项只有源码与依赖完全未变时才能按范围复用。

## 2. 两种身份必须分开

**历史签约国**仍是FRA/USM/SIH/GBR/QE1/TUR。`history/treaties/nesnd_egypt_1825.txt`逐项创建1825投资权与保证独立两条有向条款；登记后1845只退出本案历史条约。`history/diplomacy/ce_subject_relationships.txt:2–5`明确USM→SIH dominion。因此不把“当前主要投资人必须独立”加到历史六约创建或存续例外里，不释放SIH，不把SIH权益转给USM，也不删历史SIH条款。

**当前主要投资人**必须实际存在、存活且`is_subject=no`。六个选择按钮继续同页显示；SIH仍为USM属国时不可选，若以后真正独立则可以选。UI用原生国家独立条件逐项显示，不能把有历史条约写成具备当前主要投资人资格。

查询的存在检查与country-link是同级条件，并保留effect内结构保护，避免依赖AND短路：

```text
# 条件：exists与国家链接同级；可选链接防止缺对象时报错。
exists = c:$TAG$
c:$TAG$ ?= { is_country_alive = yes is_subject = no }

# 实际effect：进入对象之前再次判exists，然后再判当前独立资格。
if = { limit = { exists = c:$TAG$ }
    if = { limit = { c:$TAG$ = { is_country_alive = yes is_subject = no } }
        ...
    }
}
```

保存的投资人变量同理：先exists，再进入变量country；非存活／已附属对象不得继续给主要投资收益、−1赞助扣分或被当作最终宗主。真实外国GDP所有权压力照旧统计所有外国实际权益，不因为某国不再是合格主要投资人而抹掉其财产。

## 3. 最简生命周期

保留原本100独立性、有效赞助−1/月、外资压力公式、30年成功和10年奖励。只修资格、取消与终局；不加新发展阶段、谈判期限或重复领取入口。

|实际状态|处理|
|---|---|
|主动选择none，独立性>0|保留mode=0，清主要投资收益；绝不自动重抽；实际外资压力仍存在。|
|mode=1，投资国亡国或附属化，独立性>0|清旧对象及其条件性收益；从六国中当前存在、存活、独立、与EGY无战争且有实际收属资格的对象重选。无合法候选则保持“失去投资人”的mode=1，等待现实条件改变或玩家另选；不恢复独立性、不重置30年。|
|mode=1，当前合法投资人仍在|不随机替换活且合格的投资人。临时战争／收属能力变化按同一资格判断更新，不在零点留下等待状态。|
|独立性0，当前对象失效但有合法替补|先完成一次替补资格检查，再执行零点结算；选人本身不发发展收益。|
|独立性0，有合格投资人|当次effect尝试合法保护国关系；当次读取实际直接宗属／保护国type确认成立，才写protected和finished。|
|独立性0，none／无合法投资人／全部合法创建路径未成立|当次走invalid／担保失败终局；一次−15合法性、60月，清投资收益并finished。通知区分“无人承担”与“安排未能成立”；不等待新事件／新国家／90日。|
|EGY已成为第三国属国|记external_subjugation并finish；不替其更换宗主、不冒记赞助者收属成功、不额外罚−15。|
|国家亡国或不再是EGY|不引用缺对象，不自动复国、不重置路线。|

将当前`investor_alive`与新的“合格主要投资人”清晰分离，避免函数名暗示仅检查存活。月度扣分、收益、替补、JE fail/invalid和实际结算均用同一明确资格契约；纯历史条约继续用signatory契约。

**删除执行中的pending系统**：不再写`settlement_pending/started/deadline/grace/standard_attempted/pending_explained`；无90日隐藏事件、无2日稳定观察期、无待收属JE、无重试计数、无期限续签或变相倒计时。旧`.90/.91`只保留惰性兼容壳（type先定义、trigger=false、cancellation=true、无effects），让已排队旧事件不能改新状态。旧pending JE如需存档兼容，仅留possible/show=false、invalid=true、无按钮和无结算的退役壳；不是可见或可玩的新日志。

既有weekly Egyptian maintenance首先清旧待收属变量；未finished的旧pending：已实际处于合格投资人的直接保护国则确认旧事实，否则已是第三国属国则外部结案，仍独立则按当前资格即时结算。已finished旧档不重罚、不补奖、不重开30年。旧事件触发不会撤销之后的选择或触发第二次处罚。

## 4. 保护国原生接口：先验与后验

已读完整原生链：

* G `common/diplomatic_actions/31_power_bloc_force_become_subject.txt:41–65`实际由宗主country执行`create_diplomatic_pact country=target type=protectorate`。
* G `19_subject_protectorate.txt:8–17`为`potential={always=no}`、pact指定`subject_type_protectorate`；该potential隐藏常规外交入口，**不能据此断言原生直接create effect不可执行**，因为上条同版本原生确实直接调用。
* G `subject_types/00_subject_types.txt:1–61`定义标准保护国的等级、类型、持属国及其它规则。D `triggers.log:9003–9008`明确`can_have_as_subject={who=X type=Y}`是country原生触发器。
* C保留现有EGY专用subject type/action，作为明确的EGY范围rank/type替代路径，不改通用保护国规则，不给附属SIH开后门。

选择／最终收属资格：当前投资国独立、存活、集中政体、`can_have_subjects=yes`，EGY独立且双方不交战，并且`can_have_as_subject(EGY, standard)`或`can_have_as_subject(EGY, EGY专用)`至少一条通过。

执行时再次完整重验；标准type合法则最多尝试一次。实际未成为属国，且专用type合法时才尝试专用一次。两次都以真实直接保护国后置条件结算；不因effect被调用就设成功。`can_create_diplomatic_pact`与隐藏action potential的涵义不等同于`can_have_as_subject`；本处采用后者核subject类型规则，不用未经实测的“potential=false必然导致此effect失败”推论。

取消稳定观察timer意味着源码后置条件是当次实际关系，并非保证未来永不解除。独立性试炼已经结案；以后原生战争／外交解除保护关系不会重开奖励。engine是否在后续帧自动撤销自定义type仍是引擎未测边界，不能靠静态工具谎称已证明稳定。

## 5. 事件取消与请求清理：不虚构on_cancel

已核原生完整链：G `on_actions/00_code_on_actions.txt:5169–5180`向革命后继触发`independence.1`；G `events/iberia_events/independence.txt:22–28`在对象重新成为属国时用`cancellation_trigger={is_subject=yes}`取消；实际法律效果在option，`after:110–114`是普通选项之后设置country type，不据此声称after会在取消时执行。另有G `montenegro_events.txt:45–49`因TUR不存在取消事件的实际例子。

本机G全部events搜索未找到`on_cancel`、`cancel_effect`、`cancellation_effect`事件字段。缓存Vic3 `events.cwt:160–202`也只列trigger、cancellation_trigger、option、after；它是工具格式旁证，不是引擎支持证明。官方wiki页读取401，不引用其未读取内容。因此本计划**不写on_cancel字段，不把自定义cleanup helper称为原生取消callback**。root已明确接受这个替代。

共享请求事件`nesnd_canon_diplomacy.1`增加实时资格取消：nonce/对象/政体不再匹配，或当前request_eligible=false即取消。接受effect仍重验，不假设事件取消或AND条件天然保护缺scope。

当前C1 investment kinds2/5的投资接收国新增存在＋独立条件，落实到按钮查询、实际send、回复接受及维护的同源资格。对已有真实条约不强行withdraw；条件性投资帮助可失效，USA仍可从**实际现有、合格独立投资国**的条约中找到替代。历史六约不走此限制。其它条约、PRU/AUS/USA门槛与数值保持。

既有`nesnd_canon_diplomatic_maintenance`在每次现有回调中，发现当前请求资格已失效就清理该请求，不等原有45日clock耗尽；原来45日正常请求生命周期和6月发函冷却不扩张、不重置。为重现事件发出时的政体快照，send将两个已保存的regime值同时存为sender的请求变量；maintenance以当前serial/kind/partner及这些快照重验。旧pending缺新快照时安全取消，不补造一个无法知道的旧政体。

清理不使用失效事件的旧nonce去清新请求。统一helper只作用于当前匹配serial；旧迟答／旧取消事件不能擦掉新事务；原有cooldown保留。双方亡国和缺partner使用显式存在分支。**这发生在下一次既有maintenance调用，最多等待其原有月度节奏；不是引擎取消当帧callback，也不是新增业务期限。** 埃及本身没有需要等待这个回调才能完成的零点结算。

埃及结果通知在已经提交真实终局之后发出，只承担通知作用。加适当cancellation_trigger保护已不存在对象／已失去所叙事实的事件；取消通知不撤销已发生的合法结算，不重新发奖、不生成待处理事务。

## 6. 文件和文本闭包

修改C1自有：

1. 埃及scripted_triggers、scripted_effects、script_values、scripted_buttons、journal_entries、events（同名`nesnd_egypt_independence.txt`）；必要时沿现有on_actions维护入口加入旧状态清理，不新增定时入口。
2. 共用`nesnd_canon_diplomacy` triggers/effects/events，及必要的请求按钮资格入口；只把当前独立投资资格和失效取消接入，不改kind1/3/4/11原效果、保留B2 kind5真实依赖与kind6/7/8/9预留。
3. 专用CN/EN `zzzzzzzzzzzz_nesnd_batch_c_l_*`：删除90日、deadline、待收属改选等现行文字；主要投资说明写“存在且独立的签约国”；none仍是主动退出投资。失败通知明确当前没有合法投资人／保护关系未能成立；历史SIH权益照事实说明，不把历史签约夸成当前可收属。
4. owned SHA、source contract、writing comparison、implementation及新验证报告。

不改历史六约文件、SIH历史宗属、标准保护国定义、当前专用type/action规则、GDP算术、能力目标、30年／10年、PRU/AUS/USA战争路线、B1团结度、A1/A2法律／原住民或B2玩法。

文案按NESND player-writing已确认作者样本的“实际利益／政治后果→简短行动”方法逐条对读；新增取消文案不写nonce／维护轮询。删除“须在期限前另择保护国”，改为终局事实：“原有投资安排已经失去承担保护责任的政府。埃及仍须自行承受独立政策失败的政治后果。”具体原因按实际分支分开，不能说所有投资国均死亡。

## 7. GO后顺序与必要验收（现在不运行）

先归档旧证据→完整编辑代码和双语→冻结全部C1 owned＋依赖SHA→停止编辑→获准才测试。完整回归复用现有实际AST工具，不用手抄模型冒充执行。

必查：六按钮存在/不存在/死国/独立/附属SIH；SIH历史六约仍在且1845只退历史约；主动none不重抽；亡国／附属化重抽且不重置；0点无合法候选立即一次debuff；合法标准/专用type实际创建成功／失败；EGY第三国附属；0与30年同日只一终局；所有旧90/2日事件惰性；旧pending迁移一次；无新增deadline/started/pending执行写入。

请求检查：事件发出后对象附属化／亡国／政体变化／条约权限失效→cancellation_trigger成立；维护不等45日期满就清当前请求；新nonce不被旧回复／清理覆盖；source snapshot无对象／缺新字段安全。kind2/5的创建与接受、既有条约替代、所有旧PRU/AUS/USA保持性用原矩阵回归。

随后实际MCP、Tiger差分、双语有效覆盖／预览／引用；保持B2未实现接口为明确外部依赖，不塞占位。新freeze不复用旧90日PASS。无游戏启动，结论最多STATIC_PASS／ENGINE_NOT_RUN。

## 8. 当前决策

root已批准最简方向与非on_cancel回调的事实表述。本文件给出具体可审实现范围；等待明确GO后才编辑。附下列精确源指纹；取证只读，不是候选验证。

源码只读清点：GAME/events下328份txt，2255个具type事件，其中1074个定义cancellation_trigger，on_cancel定义为0。这证明当前原版没有可复用的on_cancel实例，不据此反推未知引擎内部绝对不支持。

|来源文件|SHA-256|
|---|---|
|[independence.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/iberia_events/independence.txt>)|`a1c098c8f1a00f6b112f6fcb2079b87bd209c6a771032218487f63b13ce2960a`|
|[montenegro_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/montenegro_events.txt>)|`d1631199ad20be91c4a8e7659f377d393d7c748db88ede1d9799e19fca935c2d`|
|[00_code_on_actions.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>)|`ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb`|
|[31_power_bloc_force_become_subject.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/31_power_bloc_force_become_subject.txt>)|`94389082fc0480145f226023a828250c912fdb1d8a9c2c37c3af6bc34e0f43ed`|
|[19_subject_protectorate.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/19_subject_protectorate.txt>)|`f3dac10f47458557dacd850ee2f2fe10235c935cc4592d1f0b5cc47b3172cb0e`|
|[00_subject_types.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/subject_types/00_subject_types.txt>)|`97a488157dfb2f340cca06aba30bfef42a36ea0a48dce6e591c8891628a6b91d`|
|[02_guarantee_independence.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/02_guarantee_independence.txt>)|`00df82497474b941e75be7ce66c2306ff920d3e8393dca09b8421cab9cf9bb4f`|
|[07_foreign_investment_rights.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/07_foreign_investment_rights.txt>)|`d1e4b58b2bdd5bf931e02b65ed89d4c8ef952611eef6558852af8360fdc20bf1`|
|[00_defines.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt>)|`e47db10931a2149c80aadab0b8de8f3fa000fdbb82a2f878fee893aa4434dd39`|
|[triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log>)|`ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`|
|[effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>)|`24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`|
|[events.cwt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/cwtools-recheck-cache/vic3/config/events/events.cwt>)|`af0ecf30e8bded4c56d59be8b8fd1379825913b0f4ab5b0f6f1d6a217ca1aab1`|
|[nesnd_egypt_independence.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_egypt_independence.txt>)|`db4e395333f7a362782172a2e441be8ad089cd2cb675a6bc83e0474b95ef4166`|
|[nesnd_egypt_independence.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_egypt_independence.txt>)|`a8443ee7217f0d336acf3a1afe68b09152801e89e489ced2f6baa492892f9a30`|
|[nesnd_egypt_independence.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/script_values/nesnd_egypt_independence.txt>)|`d0d7e162905b9c9a377ebe65e86e7b0704c7bcd3758c2a5cc3707243a02cfc96`|
|[nesnd_egypt_independence.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_egypt_independence.txt>)|`0e8d3957d34a3e6ec3015a75055147bd9e92203968dac246819bbda361e279ad`|
|[nesnd_egypt_independence.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_egypt_independence.txt>)|`0feb3ed48b2dbde1639629db842118ab7febba984d99bc6ebc8acb275f208cfc`|
|[nesnd_egypt_independence.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/events/nesnd_egypt_independence.txt>)|`204bd3f6113faccb46d4ab2c40e36e47e4bab0d249c1d101e85c64f353640c30`|
|[nesnd_canon_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_canon_diplomacy.txt>)|`03e0bc00c96836c96d2410d2739427ea1ed63e917b69fbb796e84526aac444e6`|
|[nesnd_canon_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_canon_diplomacy.txt>)|`91e79671b76e2f0467c60606590e529fc3435fed7eb9385d2fa8417f7cdced32`|
|[nesnd_canon_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/events/nesnd_canon_diplomacy.txt>)|`119f4782a3669097c522a2cafcdbaefce6dad45aee60361e7cff73937a7615cb`|
|[nesnd_canon_diplomacy.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/on_actions/nesnd_canon_diplomacy.txt>)|`6c138384ad5c47ab8cfc093af4121adf75937d8d490451f17b5e412eb35f467d`|
|[nesnd_egypt_1825.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/treaties/nesnd_egypt_1825.txt>)|`14c49fb1e6c90eb911eb0aae930139209948d2efb50827f5b72f94c7dd51423b`|
|[ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/diplomacy/ce_subject_relationships.txt>)|`78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7`|
|[zzzz_nesnd_egypt_guarantee.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/treaty_articles/zzzz_nesnd_egypt_guarantee.txt>)|`ea1fa146acd23cf9deb85bdf45a8fa70605097f4e18a0af5772b297ada9c0536`|
|[nesnd_egypt_protectorate.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/diplomatic_actions/nesnd_egypt_protectorate.txt>)|`2e08cea60f5f27d371cdd189253ce2a7ce7c1304eb14a884be8de2335dc3c387`|
|[nesnd_egypt_subject_types.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/subject_types/nesnd_egypt_subject_types.txt>)|`67dc4a0a68c0ac7bfae11291d521f72fe22d160274c0a9345d0b55450d58e8d3`|
