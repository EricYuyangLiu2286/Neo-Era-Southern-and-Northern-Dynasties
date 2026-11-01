# 36b — PHI 预览事务与提案期限修正

当前两项是实际游戏负例，不能以静态通过解释为玩家误操作。A3/A4均独立候选，不修改正在运行的run202721、主MOD或父候选。

## 最新优先：A3/A4预览修复已被实机否定，A5只修数值读取

run211226加载包含A4的综合C3，在旧Gbuy打开同一PHI QA菜单、未申请，就使error从143增至9871。报错转到A4 effects586/638，仍是save_scope_value_as读未持久化serial。原文已封存 `evidence/phi-preview-A4-negative-20261031T212029Z/`。**hidden_effect隐藏效果显示，不是可靠的求值隔离器。** 不能再把A3的有序AST等价或Tiger通过写成预览安全；此前推断已撤销。

A5 `exports/phi-imperial-service-20261031-a5` 精确父A4，只改四个scope capture的value为 `nesnd_phi_proposal_serial_for_event`：script_value先value0，只有has_variable为真时才add原var。真实执行仍先初始化0、递增，再读当前值；预览缺值返回0。原版 `ep2_japan_values.txt:183–198` 的tooltip专用数值、`ip4_cuba_values.txt:24–29`、`ai_script_values.txt:98/277–281` 使用同类守卫读取。当前候选只证明结构和类型静态一致，仍须同Gbuy反复悬停的实际新增错误计数。

A5共effects、script_values、metadata三文件，金额、事件期限、所有权限、ID/序号机制和B交割均未改。逆换四值引用后effects AST与A4全等；Tiger1035→1035新增0。独立备份 `candidate-phi-safe-serial-a5-20261031T212148Z`；证据 `evidence/phi-safe-serial-a5.json`、`.diff`、`-tiger-incremental.json`。

确认事件的quote/route/serial本应来自已实际提交的请求；commit的钱款数量是四个字面量，不依靠当场写后读。finish_creation中contract_serial、binding镜像及measure→display仍有有序依赖，但目前入口是实际原生on_action，尚无证据这次预览遍历到它。将来若暴露这类helper，必须逐值作numeric guard，并对typed treaty使用exists守卫，绝不能用数字0伪造实体。display的JE immediate也应持续以首次创建+立即hover实测，不能用已有变量的五月档覆盖所有生命周期。

## 真实断点和来源

1. run202721从旧Gbuy加载，USM打开PHI QA菜单，现金A/B选项显示，但未点击申请。20:55:53至20:56:45反复出现 `wrong type ... none`，分别指向A2效果577、626；两行各5,419次。关闭菜单后停止预览。原始debug/error/game及轮转11文件、SHA已封存在 `evidence/phi-preview-202721-20261031T205721Z/`。
2. 根再次从Gbuy自然推进May12→Dec13，没有PHI QA申请/批准。AI自然两次递送现金A议案。Dec1原生档保存：serial1创建1836.6.6，过期1838.12.6；serial2创建1836.10.4，过期1839.4.4。都是30个月，不是30天；相邻请求120天。证据 `evidence/phi-unanswered-proposals-native-202721-Dec1.json` 及原生events段 `.events.txt`。
3. 同一观察也给出有限正证：旧Gbuy缺少proposal_serial，实际AI入口却正确产生1、2并传到USM事件scope。请求初始化/递增/跨国提案上下文已实际执行。**没有任何一方批准，没有创建钱款或移交舰船。**

## 问题根因与工作流责任

预览系统不会先提交 `set_variable` 再让后面的getter按新值运行。四个请求的missing→0→+1→save-scope序列在真正执行时成立，在显示效果预览时会读到none。只加initialize或missing guard不能证明preview-safe。

事件顶层 `duration` 的单位是月；`trigger_event.days` 是投递延迟天数；`set_variable.days` 是变量存续天数。原版 `common/defines/00_defines.txt:1776–1779` 给出DEFAULT_MONTHS_VALID；`NUM_DAYS_TO_AUTO_OPEN_EVENT=30` 是过期前弹窗提示天数，不是默认事件寿命。GUI和默认选项来源见 `WORK/evidence/phi-event-duration-default-source-review-20261031.md`。

这两条规则此前已写入技能 `references/validation.md` 的“1.13.11原生存档缓存与作用域诊断”。本次失误是实现和审查时没有把既有规则应用到新的事务链，不能以“缺少文档”推脱。后续每个可见按钮/选项先登记预览路径，按“只读条件→可读结果提示→隐藏事务执行”逐项查；每个期限标明数值、单位和其它相关期限，再查原生排队事件的creation/expiry日期。一个helper能在控制台执行，不足以证明它可被放在可见option中预览。

## A3：有序执行保留，隐藏显示的尝试（实机未解决求值错误）

候选 `exports/phi-imperial-service-20261031-a3`，精确父A2。四个request保留外层只读资格；旧档序号初始化、递增、保存scope、设置报价和跨国投递放在一个 `hidden_effect` 中。可见提示明确“递交→中央审议→吕宋确认”，再引用原有对应条款的金额、期限、军队后果和财政条件，避免隐藏真实成本。

commit事务也放在隐藏执行段。8个协商事件的20个受序号guard保护的选项，把实际写入/递送/commit放在隐藏执行段，现有批准、拒绝、暂缓、取消与条款提示保留。原版 `common/scripted_buttons/06_canada_australia_buttons.txt` 用同类custom_tooltip+hidden trigger_event模式，`04_law_imposition_buttons.txt` 把内部变量/修正整理放在hidden_effect；引擎docs定义hidden_effect为不显示内含效果。

finish_creation的原生条约回调、expiry隐藏事件及月度监测没有当前可见预览入口，不扩改。其contract_serial递增→scope保存、binding→payer镜像、active_cash→分支、measure→display都是有序运行依赖；不得今后直接放入可见预览。完整审查见 `WORK/evidence/phi-a2-preview-chain-review-20261031.md`。

范围：effects/events/双语4个新请求提示/metadata共5文件。去掉展示wrapper与纯tooltip后，完整有序AST和A2全等。资格、金额、条约身份、proposal/contract序号、冷却、期限、舰船转归与退出语义均未改。Tiger相对A2新增0；旧 `total_crew_needed` 词库报告已有引擎docs和自然存档值反证。独立备份 `backups/candidate-phi-preview-a3-20261031T205927Z`；证据 `evidence/phi-preview-a3.json`、`.diff`、`-tiger-incremental.json`。

## A4：协商窗口与pending闭包

候选 `exports/phi-imperial-service-20261031-a4`，精确父A3。只有events的13个duration标量及metadata改变：

|窗口|事件|新期限|原默认行为|
|---|---|---|---|
|中央审议|.1/.2/.11/.13|2个月|defer，当前案清pending并冷却30天|
|吕宋最终确认|.3/.4/.12/.14|1个月|cancel，当前案清pending并冷却30天|
|签约/到期/中断/恢复/改约通知|.5/.6/.7/.8/.10|1个月|原既有确认项|

pending仍120天。从递交到最晚接受再到最终确认，最多约93个日历日，给内层资格复查留出余量。没有为追逐过期窗口续长pending，也没有改AI概率或资金义务。不能统一设两阶段各3个月却继续假定整条链受120天有效期覆盖。

全部20选项的proposal serial guard、现金/原生模式、默认选项和effect保持。序号不匹配的旧窗口只会关闭，不应清理更新的请求；当前案超时则正常走defer/cancel。这个语义目前通过源码保留检查，**新期限自动选择和旧窗口不干扰新案仍须实际走时验证**。

13标量逆改后事件AST与A3全等，其余文件字节全等。Tiger1035→1035新增0。独立备份 `backups/candidate-phi-expiry-a4-20261031T210424Z`；证据 `evidence/phi-expiry-a4.json`、`.diff`、`-tiger-incremental.json`。下一综合版若基于当前A2，取A2→A4累计差分；只取A3→A4会漏掉预览修复。

## 下一实机门禁

1. 加载新冻结候选和事件尚未生成的Gbuy。记录当前error各类基线；反复打开QA菜单、正式PHI日志按钮、hover两个现金提案，核新错误增量为0，既有serial仍缺失且无pending。关闭菜单后再次核验。A3代码静态通过不等于此项通过。
2. 正式申请A现金，保留新serial和真实USM事件上下文，核expiry_date为creation+2个月。核准后PHI事件应为creation+1个月；正确记录人类/AI分别作出的选择。不能手工force最终事件伪造丢失上下文。
3. 独立不批准分支：走过中央2个月，验证默认defer、pending消失、30天冷却；最终确认1个月同理。旧serial窗口和更新请求并存的负例必须证旧默认不会清新请求。
4. 若使用已有Dec存档，它保存的绝对expiry_date已在1838/1839；不声称改事件定义会自动重定时旧popup。应清楚区分旧保存窗口与新生成窗口。
5. 真正签约同tick检查typed treaty ID/单money条款/方向/精确quote8700/原binding/双方镜像/active_cash与无unbound；然后才跑周款项、12月到期、改约、战争/市场退出和恢复能力。

A3/A4均没有新增EP2门禁。原生ship_transfer article的feature条件与通用剧情转船effect可执行范围仍是不同问题；B须独立实测原舰ID/crew/formation，不能以flag等价交割成功。以上候选均未合入主MOD，未宣称真实合同或经济恢复通过。
