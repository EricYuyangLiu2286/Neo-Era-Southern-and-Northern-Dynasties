# 日本修订3与共用生命周期：来源及闭包审查

2026-11-02；仅计划审查，未修改玩法、未开游戏。本文件记录读取修订3第十节及共用生命周期后的发现；父任务可据此局部修订。完整来源链见[japan-overlord-lifecycle.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/japan-overlord-lifecycle.md>)及其SHA清单。

结论：主体身份、直接/间接宗属、独立发展、同市场商品条约限制、条约约束期、JIM制度与个人委任分离均与本机来源相符。未发现需要推翻修订2文化方向或重做已定崩溃的证据。以下三处应收窄文字，一处补迁移事务；它们是实现前规格闭包问题，不是已运行缺陷。

## 需要收窄的表述

1. **共用L12“原宗主不能继续收费”须限定收费来源。** 旧宗属贡赋和本项目尚未兑现义务应随关系失效收尾，但仍有效商业money_transfer不能被这一句无条件删除。建议改为“停止已失效的宗属收费/本项目义务；仍有效商业条约依实际存续与合法终止处理”。原生条约withdraw是显式效果，且可区分约束期内违约处罚；同一对国家可能另有有效条约。[L:64](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-india-lifecycle.md:64>) [E:37390](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:37390>)

2. **日本“ 一般商业条约依法延续”不能成为同TAG继承的引擎保证。** 建议“检查一般商业条约的实际存续及合法继承，不因改制自动解除；政治/个人承诺明确追认”。同对象改制与吞并旧国家后新对象change_tag不同。南朝和NRP都有后者，不能只因USM/CNE仍存在就推出旧条约对象/请求仍有效。[J:214](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:214>) [S:8](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_settlement.txt:8>) [N:115](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_cne_republic.txt:115>)

3. **朝鲜治理与对外交涉分开。** 修订3收尾表“实际持有朝鲜州才开放/无朝鲜州失效”适合本国地方治理，但旧主方案明确允许“或提出具体交涉/干预”。建议无州只关闭本国治理子项，对外朝鲜协商由真实KOR/CNE/实际持有者与具体提案决定。否则JTK/JIM未持朝鲜时不能讨论KOR保护与统一后的承诺，属于非必要缩小原设计。[J:53](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:53>) [J:251](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:251>)

## 迁移与边界补项

- **旧档JAP实际ruler林→JIM不是普通USM军官任命。** 现pending/candidate链主要允许USM非统治者或已到JAP的精确人物。迁移需一次事务保存旧JAP的合法接任、JIM天皇承载、林精确对象、双方现有国家实例；确认接任及角色安排可用后移交。部分成功时只重试该事务，不生成第二个林，不拿新复活JIM代替旧对象，不全局夺取模板人物。不能把“完整链迁移”缩成替换pending_country。[P:8](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_lin_regency.txt:8>)
- **原崩溃保持。** 源码当前是京都与关东两处都由对JAP敌国控制，或既有已确认败战事实；不是任一首都失守，也不是友军占领。修订3开头概述可接受，但实施安排“先修JIM身份与已有完整战争链”宜改“对齐JIM身份并复核既有战争链接口”，避免重新授权不必要的崩溃改动。[C:25](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_war_collapse.txt:25>) [C:30](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_war_collapse.txt:30>)
- **L23部分执行案例应保留。** 父任务已计划加入create_country成功但博弈创建失败：必须有已创建/已扣费/已建立博弈三个不同事实；有效国家保留、重试不再造国，失败清未兑现资助/请求，不免费重复部队、不强行吞回玩家。新增L23后同步日本“L01–L22全覆盖”引用；此处是预期验收场景，非已证引擎结果。
- **即时独立入口不等于即时主权终奖。** 原on_become_independent可作入口，但现东征有make_independent准备动作；新计划正确要求真实外交结果，不需要再加先统一/九州/南朝结算的入口门槛。[O:7607](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7607>)

## 来源核对通过项

is_subject_of包括间接属国、is_direct_subject_of才是直接；USM显示名/阶段不等于新TAG；CNE共和可复用TAG；JIM文化持续不依附于吴委任；goods_transfer同市场资格与精确条约捕获仍列待证；父JE不能自动结束已爆发战争；多人协商保留对方选择；成功/fail/invalid互斥及幂等清理；世界效果唯一执行者。以上都可继续用于实现规格。

本轮审查没有宣称STATIC_PASS或ENGINE_PASS。建议修订后的父计划再次查找上述短语；详细接口待证事项仍见研究报告，不能以本审查替代引擎观察。

## 读取指纹

|来源|SHA-256|
|---|---|
|J 20261102-japan-development-design.md|b90be65e5aaaadd2cf5edd2e1349dea8028c505b84aee79e9e4f5f42a6491d3e|
|L 20261102-japan-india-lifecycle.md|c4d5786f40c33df7b557bbcb841e1893982a8aab6b4a55829978f97c363a9cc1|
|E effects.log|24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1|
|T triggers.log|ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e|
|O 00_code_on_actions.txt|ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb|
|C nesnd_war_collapse.txt|6ae291edab567b237df552bad91d541e88463850e0f0190585ed65f04878a014|
|S nesnd_south_settlement.txt|c17d6705136d29bd2a33a258dbdd1b4d8d06d1d9853dbd1789d68e423ebf71e2|
|N nesnd_cne_republic.txt|113c78b0c36183f033ac7daf259414775d3be4c50114138d00eece5feea2bbfb|
|P nesnd_japan_lin_regency.txt|137ddf6eb366bf07e2814eb3c3b7cc4bf53dd2f7adc78d79c23fda681f4f6570|
