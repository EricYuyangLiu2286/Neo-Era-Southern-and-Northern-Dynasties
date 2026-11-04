# C1 repair4 原生来源与实现契约

GAME 1.13.11 / build24799966；catalog CURRENT，changed_count=0。复用已读完整来源链，未发明新API。

- GAME common/diplomatic_actions/31_power_bloc_force_become_subject.txt:41–65：宗主country执行create_diplomatic_pact，protectorate在60–65行。
- GAME common/diplomatic_actions/19_subject_protectorate.txt:8–17；common/subject_types/00_subject_types.txt:1–61：标准action/type；potential隐藏入口不当作直接effect禁令。
- WORK references/engine-docs-1.13.11-20261031/triggers.log:9003–9008：can_have_as_subject={who=country type=subject_type}。本轮实现传subject_type_protectorate及subject_type_nesnd_egypt_protectorate。
- GAME events/iberia_events/independence.txt:22–28,110–114及common/on_actions/00_code_on_actions.txt:5169–5180：原生事件取消与普通after分开。未使用on_cancel/cancel_effect/cancellation_effect。
- C common/history/diplomacy/ce_subject_relationships.txt:2–5：USM→SIH dominion；common/history/treaties/nesnd_egypt_1825.txt保留六约；保证条款历史例外不接当前patron独立门槛。

原版具体SHA沿用batch-c-repair4-plan.md:117起及batch-c-repair4-plan-sources.json；本次候选全部owned和只读依赖SHA绑定batch-c-repair4-freeze.json。未改history六约、SIH宗属、subject type/action、真实GDP所有权算术。

生命周期：none保持mode0；mode1资格失效仅从相同合法集合重抽；无候选保留mode1但无对象/收益。零点当次替补、至多各尝试一次标准/专用保护国，真实关系后验后才能protected/finished；无合法对象或创建未成立当次一次60月既有失败modifier。第三国属国external结案无额外处罚。finished挡住任何重复结算。

资格分层：patron_country只核投资国本身；patron_can_take_egypt额外核EGY独立/无战争/type合法；protectorate_confirmed只核已存在对象、投资国本身及真实直接保护国关系。confirm_protection先保存final_patron再finish；protected_fact仅核终局对象实际关系，不要求EGY独立。

迁移：maintenance先进入旧pending且未finished分支，尚未替补或删除investor，然后清旧标记并调用立即结算。settle首先确认真实旧保护国，再判断外部属国，最后才在仍独立分支替补。JE invalid若先于weekly触发，对旧pending同样调用settle，避免抢先记成external。已finished仅清旧字段，不罚不奖。旧.5/.90/.91惰性、旧交涉JE不可见/不可激活/invalid且无效果。

请求：kind2/5的partner独立限制、已存investor帮助和USA条约替代条件一致；现有真实条约不退出。send将双方政体快照写sender；maintenance从当前partner/kind/serial及快照检查，缺快照安全失效。clear_request保留serial/cooldown并删两个新快照；事件接受/拒绝原有reply_valid匹配当前serial/partner后才调用clear，maintenance直接清当前事务，不采纳任何旧事件nonce。

边界：cancellation_trigger可立即取消事件；请求清理由既有月度maintenance完成，不声称取消当帧回调。关系当次后验不证明以后引擎不会自动解除，亦不重开终局。没有新的业务等待期限。
