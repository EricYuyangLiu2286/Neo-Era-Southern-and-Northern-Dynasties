# C批修复1：预览中的保存对象

2026-11-04；root已批准窄修复。编辑期间未运行测试。

- 原红例：EGY结算预览在save_scope_as不执行时读取scope:nesnd_egypt_subject。
- EGY标准/专用protectorate调用均改为c:EGY，外层仍限定存活EGY；删除这一个无必要保存对象。保护国确认、grace、pending与失败分支未变。
- 同类玩家入口审计发现三处相同形状并纳入窄闭包：PRU完成奖励中的保存宣称者加exists分支；AUS干预固定actor改c:AUS；USA原省份清单固定接收国改c:USA。后两者删除各自无必要保存对象。所有输入身份由既有外层资格约束，不改政策、数值、目标选择或结果。
- 其余effect内保存对象已有后续exists分支，或仅用于受取消条件保护的事件。触发器中的save_temporary_scope_as沿原生查询实例，不把不同机制猜成同一故障后重写。

原红例与初次冻结保留不动。重新冻结31份owned文件后才能进入测试；修复实现本身不是通过结论。
