# 70 法国后继首批 · 宫廷与外省

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [工作台核验结果与文件指纹](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/france-court-20261107/validation.json>)

## 现象与期望

任务29只交了[法国方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/france-politics-plan-20261103/france-development-plan.md>)。作者确认波旁／奥尔良共用政策、考虑共和国接续，接受两地政策力度和以吸引力差引导迁移，并委托设定评议数值。第一批采用 B 型五年评议，1 日志、1 显示条、2 按钮、1 期末事件。

## 现状与接续

- 既有帝国日志已结束，波旁或奥尔良实际在位才开。摄政查继承人。既有登位弹窗 `fra_unrest.19/.23` 的 immediate／after 增设和释放短期标记，待原有选择落定再开；选择神权不会入线。
- 议会共和／总统共和沿用同一份法国日志，换标题和正文，继承工程方向、年度冷却、选策时的账目与原截止日。直接从帝国进入共和不启动王党工程。其他政体或王朝关闭政策。日志开启原生胜利革命继承；任期只结一次。

## 改了什么

- 新的 `common/journal_entries/nesnd_france_court.txt` 统管 1825 日任期、月度同步、期末和失效。同名 triggers、values、buttons、progress_bars、effects、static_modifiers、on_actions 及 customizable_localization 分别处理范围、读数、行动、结算和政体显示。原事件文件只增加四行衔接标记。新增同名评议事件与中英 replace 各49键。
- 巴黎的人口基建 +20%。外省方向使巴黎移民吸引力 −15%，法属本土其余州吸引力 +15%、施工效率 +10%。选策后一年可换向，重记期初，期限照旧。法国地理集合20地区另加科西嘉。失巴黎暂停，复得恢复；州转手时移除政策，疆界变化的地区退出本次比较。
- 受益地都市净增至少1级，威望 +5，持续24个月。其在同批本土州中的都市份额同时上升至少1个百分点时，改为 +10 威望、24个月。设普通档让全国普遍增长也能兑现承诺；高档要求建设重心确有转移。未达标或无法核算，均无奖励。

## 怎么复测

1. 新局分别拥戴波旁、奥尔良；检查弹窗落定才开日志、神权选项不触发。选策后在法兰西岛、外省和法国印度领地核对不同州面板。
2. 王党任内选择外省，记下截止日、当前份额和冷却；年内改为议会／总统共和，核对共和国标题、原政策、同一到期日及冷却；冷却期满换向只重记比较起点。另验摄政、胜利革命继承，以及改委员会共和／神权的退出清理。
3. 观察分裂州、失去／收复巴黎、迁都、零都市；在第1825日核对可比地区的前后等级、份额、单档威望及24个月后到期。复核巴黎人口基建上限、施工与实际迁移。
4. 已对实际评奖算式运行632组边界输入，检查中英键与数值、日志退出、州归属回调、单次奖励、既有两份法国日志及按钮、124份历史文件。对任务46发布版本核对古吉拉特归属、人口、建筑与分舰队。详见[验证脚本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/france-court-20261107/verify.py>)。

## 遗留问题

- 本次未启动游戏。政权更替、尤其胜利革命后的日志继承、分裂州回调时序、数值难度和动态界面待实机复测。
- Tiger 1.19.0 的 schema 针对游戏1.13.5，把现行1.15的 activation_description 和两个 outcome 报为未知字段；已对照1.15原版。旧法国事件第483行另有既存缩进提示，备份行与当前一致。
- 后续源码核对：旧换君效果的五处调用均在外层写入胜方复辟标记之后，两处移除分支对现行夺权流程的该标记没有作用。旧日志按君主思想结算、新日志按在位家族开启，是另一项独立差异。见[系统关联图与逐项源码依据](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/france-court-20261107/restoration-dependencies.md>)。第二批地方社会事件、共和国繁荣分配与条件性右转仍待后续。
