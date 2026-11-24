Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-24，「源目录写法整理」会话调度的奥斯曼 B2）
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-ottoman-b2-20261124T185237Z/`；记录 `nesnd-workbench/reports/2026-11-24-ottoman-qinist/交付记录-B2.md`，检查 `checks-b2/`

# 120 奥斯曼：两份日志的结局与路线里程碑

## 1. 现象与期望

「重整东方秩序」与「帝国诸民」唯一可见结局都是「不再是奥斯曼」，只清修正，不合结局要有后果的规定；坦志麦特结束后没有路线分岔。B2 提示词：工作台 `reports/2026-11-24-ottoman-qinist/B2-提示词-整理现有结局与里程碑.txt`。

## 2. 改了什么

- 「重整东方秩序」：新完成结局「东方秩序」（整片持有巴格达、摩苏尔、巴士拉、叙利亚、阿勒颇，永久修正，事件 .3 选继续东进或巩固）；新失败结局「旧秩序的终结」（不再整片持有东色雷斯，热情归零、72 个按钮州的宣称作废、永久合法性 −10，事件 .4 迁都安卡拉或求援）；「不再是奥斯曼」改隐藏 invalid。
- 坦志麦特结束后的月度脉冲发「宪政的帝国」(.5) 或「苏丹的帝国」(.6)，设 `nesnd_ottoman_route` = `flag:constitutional`／`flag:sultanic`，选项设 `nesnd_ottoman_route_lean`（`flag:charter`／`flag:barracks`／`flag:sultan`），供 B3 起的路线日志读。日志先结束时由 on_action `nesnd_ottoman_route_fallback` 补发。
- 「帝国诸民」：两条计数进度条（同心、离心的月数）；完成「诸民同心」（连续 36 个月不低于 75，永久同化修正，事件 .7 给土耳其人占多数的已整合州加本土）；失败「诸民离心」（连续 24 个月低于 25，永久修正，事件 .8 在非土耳其人占多数的州加激进派）；原有两个隐藏结局合并为一个 invalid（引擎只许一个）。

## 3. 怎么复测

控制台 `tag TUR`。坦志麦特结束后下个月应弹 .5 或 .6；用 `event nesnd_ottoman_recovery.3`～`.8` 逐个看文字与选项。东方秩序、旧秩序的终结各看一次日志面板的结局说明。

## 4. 遗留问题

- 宣称购买没有记录，失败时撤掉的是 72 个按钮州上的全部奥斯曼宣称，包括非购买来的。
- `nesnd_ottoman_route_lean` 目前只写不读，B3、B6、B8 读。

B2 修复（2026-11-24）：诸民同心改为对各州最大的非主要文化加永久接纳度；里程碑等原版收尾（nesnd_ottoman_tanzimat_settled：有 sick_man_complete、无 sick_man_var）；军改首次开始设 nesnd_ottoman_qin_reform_begun，路线两事件按它分两版正文；玩家文字修 8 处；on_action 合并。记录见交付记录-B2.md「B2 修复」。
