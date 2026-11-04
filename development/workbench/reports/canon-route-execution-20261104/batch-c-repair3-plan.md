# C批修复3计划：有界的埃及保护交涉

2026-11-04。依据root已批准的C-LIFECYCLE-03修复设计，先写计划，再编辑；同一授权下无需额外审批跳转。当前停止全部测试，原64次维护仍无限pending的红例原样保留。

## 保留的正常路径

主独立性JE的六投资国按钮、none与独立性bar同页不变。独立性0且当前投资国存活、有现实保护能力时，仍优先建立同一个赞助国的标准/埃及专用保护国，并走既有2日grace确认。不会自动改选存活赞助者，也不恢复独立性或重置30年时钟。

## 唯一90日期限

新增持久`nesnd_egypt_settlement_started`与90日`nesnd_egypt_settlement_deadline`。第一次进入pending才同时设置并排队一次90日隐藏事件；旧档已有pending但尚无started时只补一次。started不在deadline过期或finish时删除，因此维护不能重新续上90日。

每次维护先核真实保护关系、已有grace及实际创建结果，再处理期限。90日隐藏事件先移除deadline（覆盖事件/变量到期同日求值次序），再调用同一settle；若当天赞助者已能建立关系，则先建立并进入grace，不按独立的失败处理。仍独立且未形成保护关系才终结。

## 玩家处置，仅限失败的独立pending

新增罕见pending JE，possible/显示仅在存活EGY、独立、pending、deadline仍在、无grace、无finished时成立。它复用现有六国选择和none按钮；不复制主独立性bar，不提供普通路径撤销失败的入口。

- 六国改选：另一个仍存活、非EGY自身/属国树、未与EGY交战、可持属国的六国对象；不得自动替换活赞助者。选定后清单次尝试标记，立即用同一settle尝试真实保护；不发普通发展利益、不重置独立性、30年钟或90日期限。
- none：明确承认本次保护交涉失败，执行一次−15合法性/60月及finished。pending之外的none仍只撤销普通投资承诺，保留既有作用。
- 埃及已经成为属国或处于grace时，所有pending改选/退出资格均false，不能先建立附属后点击逃脱。
- 期限过后仍独立：同一失败helper终结。事件区分“活赞助者无法落实保护”与“没有当前赞助者”，不谎称对方死亡。终态先写标记、再清临时状态/JE、再罚一次。

## 修改文件（C owned）

仅common/scripted_triggers/nesnd_egypt_independence.txt、common/scripted_effects/nesnd_egypt_independence.txt、common/scripted_buttons/nesnd_egypt_independence.txt、common/journal_entries/nesnd_egypt_independence.txt、events/nesnd_egypt_independence.txt及专用中英replace；更新writing-comparison与owned SHA。原标准/专用subject类型、历史六约、其他国家路线不变。

## 预览、文本与原生来源

固定EGY对象沿修复1引用；新增期限使用已核set_variable days与trigger_event days，不引入新引擎接口。pending处置按钮的收益预览区分普通合作与接受保护，不在pending显示实际上不会发放的产业利益；none有稳定说明与真实处罚show_as_tooltip。新事件保持type在cancellation之前。

原生来源沿batch-c-native-sources.json：effects.log:37194–37200变量期限、37336–37341延迟事件；31_power_bloc_force_become_subject.txt:41–65建立方向；19_subject_protectorate与有效subject定义；已有按钮/JE原生生命周期规则。未运行游戏。

## 冻结后的测试

先重跑原preview红例和原64次pending红例的有界版本，然后逐项：0正常、90日期满、90日同日赞助恢复能力、改选另一国、none、循环宗属、已属国/grace不可退、旧pending无started补一次、started已有但deadline缺失不得续期、两次终结只罚一次、改选不重置任何时钟。所有行为从最终冻结AST取源；原生pact结果作为明确fixture注入，不冒称游戏执行。随后继续尚未运行的共用请求、条约、PRU/AUS/USA矩阵与双语引用；发现新语义失败照约停止。

## root补充批准：第三国附属的外部终结

若pending期间EGY实际成为另一国家的直接属国，写独立的nesnd_egypt_external_subjugation，调用finish清pending/deadline/投资利益；不写赞助保护成功、不发奖励、不额外罚−15合法性，也不改实际宗主及关系。当前赞助国的真实直接protectorate仍优先走原确认/grace。用is_direct_subject_of核实直接宗主，不能将“第三国是赞助者的属国”误当EGY直接归赞助者。之后再次独立也由finished阻止重开30年或自动领奖；旧90日事件因finished/pending守卫惰性退出。新增外部失去独立的通知只叙事实，不冒称其来自本保护协议。
