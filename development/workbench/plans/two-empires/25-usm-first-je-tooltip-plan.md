# USM 首个JE尚未走时的契约悬停刷屏

实际run162626：自然flavorUSM.1于1836-03-11接受，保护按钮可用；首次悬停联邦契约，nesnd_crisis_buttons.txt:60读取未设置nesnd_compact_progress，重复产生三联错误。滚动原日志已完整归档runtime-162626-compact-flood-20261031T164947Z；当时各错误3358次。点击契约后真实进度20%，说明点击效果内初始化能执行，悬停效果预览却不会执行该写入后再求值。

父：已冻结harbor-closure-20261031-a（F+三港修复）；新独立usm-startup-tooltip-20261031-a。保持splnet SHA b1dd897a678f081c17eb5b79e5c8f3cd3d5a65e77872d67008c029f2051a5aef及全部地图/历史/资源字节。

## 根因与生命周期

旧compact初始化只在显示refresh里的has_journal_entry条件内，以及按钮click effect内。首JE的immediate调用显示器时尚未得到country JE可见性，是当前证据支持的初始化时序缺口；无论这个具体引擎时序如何，数值必须由独立生命周期初始化而不是依赖显示器存在来保证。

自然intro immediate → 独立幂等初始化两计数 → add JE → JE immediate再次保障 → 显示bar；显示刷新和契约按钮也调用幂等保障。只补缺失值0，不清已有进度，不替玩家成功。

所有两计数的数值读取改用有has_variable分支的只读script value，未初始化时返回0，悬停预览不产生写入依赖。涵盖契约完成判断、提前禅让、JE完成、保护陈事件压力门和两根bar。实际click仍真实+20/-8、18月冷却、10年modifier，达到100才按原effect保全；不隐藏整段tooltip，也不绕过政治条件。

当前原版实例：common/script_values/ep2_japan_values.txt中absolute_state_daimyo_loyalty/state_daimyo_loyalty在变量不存在时给默认值，否则读取var（明确服务tooltips）；common/scripted_effects/04_negotiation_scripted_effects.txt:128/137用scope:ig.script_value；common/scripted_buttons/06_iberia_buttons.txt:41展示条件求值与click操作区分。

## 扩展检查但不泛改

CNE land_init直接初始化completion/failure/months与实际measure再刷新；supply_initialize直接设置score/weeks/market/sponsor再refresh；DEI initialize直接设置good/bad/target并measure再display。它们不把核心计数初始化藏在has_journal_entry显示守卫内。本次仅修确证USM两计数；各新JE首次出现仍必须逐项实际悬停测试。

## 验证

修改前独立备份；AST解析、所有raw读取闭包、缺失/0/80/100边界模型、作者文字/地图/历史完整SHA，Tiger与父差分。模型只证明读值设计，不称引擎已测。

下一冷启动：自然intro前保存；接受后暂停且不走一天→悬停三按钮和两bar→日志不增长；契约首点20/压力clamp0、保护仍实际可点，政治不足时按钮正常禁用。原生保存读回并重复悬停。旧未初始化JE档先hover也应安全默认0，下一真实刷新补缺失值，不把已有20归0。还需真实第五次契约保全及70压力禅让门槛测试，不能声称修一次首hover就全链通过。
