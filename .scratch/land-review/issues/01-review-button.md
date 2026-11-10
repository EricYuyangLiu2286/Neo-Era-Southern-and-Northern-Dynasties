# 复核地权争讼

Record: implementation  
Category: bug  
Status: ready-for-agent  
Execution: completed  
Assignee: Codex  
Blocked by: none  
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）  
Evidence: [按钮条件、变量和旧档复测](<../../../../../nesnd-workbench/reports/2026-11-09-land-review/button-audit.md>)、[地权革命功能说明](<../../../../../nesnd-workbench/reports/2026-11-09-land-review/guide.md>)、[离线内容树](<../../../../../nesnd-workbench/reports/2026-11-09-land-review/map.html>)

## 现象与期望

按钮悬停反复列出国家与变量，作者观察到复核局显示 11 个月。须按实际条件说明能否办理，复核与冷却均应为 12 个月。

## 原因

原按钮展开整套项目运行与改革失败判定，效果区还预览记账。现行主 MOD 的按钮效果在修改前已经为两项各写 12 个月。另有一条 24 个月的地方请愿事件路径。

## 改了什么

按钮专用触发器逐项给出条件提示。按钮效果隐藏记账预览。中英文同步显示费用、门槛和期限。与备份比较，14 项独立输入的 16,384 种组合结果一致。内容树以 ce_cne_land_reform 为根。

## 怎么复测

重启后可读进行中的存档。比较可办与不可办的勾叉。选尚无复核局的档暂停办理，核对修正到期日、即时扣款和失序。满 12 个月检查冷却解除、资金和失序均足时再次办理。

## 遗留问题

界面“11 个月”与实际结束日待作者实测，既有计时不迁移。树中发现的未调用、未读变量及期限单位等见功能说明末节。

## Comments

2026-11-10：作者测试完毕。正文中“未启动游戏”“待复测”等为交付时的状态。
