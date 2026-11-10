# 86 整理 nesnd_crisis 事件与修正

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [结构树对比结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-10-crisis-cleanup/verify.json>) · [对比脚本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-10-crisis-cleanup/verify.py>) · [Tiger 原始输出](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-10-crisis-cleanup/tiger.json>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/2026-11-10-crisis-cleanup>)

## 现象与期望

作者：nesnd_crisis_modifiers.txt 和 nesnd_crisis_events 写得太乱，自己看几乎看不懂。同意按方案整理，不改任何事件 ID、修正名和本地化键。

## 原因

两份文件是代理多轮批量生成、删改的产物。地权危机四个事件的选项只调用 `nesnd_land_choice_*`，效果另放在 `nesnd_land_choices.txt`，九段各只用一次。删改留下首尾相接的选项、成段空行、空块和五行重复注释。一个文件里混着地权革命、靖难对外反应和吴国善后三个系统，编号乱序。修正都写成一行，没有分组。另有两个孤立事件和四个无引用修正。

## 改了什么

- `events/nesnd_land_reform_events.txt`（新）：.30–.33 按编号排列，选项效果原样写入，每个事件和选项前加中文注释，写明触发时机与效果。
- `events/nesnd_crisis_events.txt`：只留 .20、.21、.40，分“靖难对外反应”“吴国新朝善后”两段，一项一行。删除孤立事件 .10、.11。
- `common/scripted_effects/nesnd_land_choices.txt`：已全部写入事件，删除。
- `common/static_modifiers/nesnd_crisis_modifiers.txt`：按系统分六段，注明施加来源与期限，一项一行。删除 `nesnd_army_audit`、`nesnd_refugee_reception`、`nesnd_maritime_security`、`nesnd_japan_reorganization`。`nesnd_land_compromise` 保留作者改定的权威 −5%。
- 两语 `nesnd_crisis_l_*.yml`、`nesnd_japan_l_*.yml`：移出 38 个已无引用的键，包括 .10、.11 的全部文字、.21 的旧可见文字和四个修正名。原文存入 `development/nesnd-player-writing/resources/unused_localisations/2026-11-10-crisis-cleanup/`，已同步技能副本。

## 怎么复测

1. 不需要实机。运行 `verify.py`：七个保留事件及其选项内的语句、顺序、数值与改前（含被调用效果展开后）一致，仅事件顶层字段次序和空块有变；修正除删去的四个外逐项一致。
2. 想在游戏里确认时，任选一次清丈风潮或议止，选项悬停应与改前相同。

## 遗留问题

- Tiger 报 `nesnd_crisis_buttons.txt:32` 括号位置可疑（议止按钮的写法），不在本次范围，未改。
- 第 33.b 选项对 NSX 的 `dp_annex_war` 只为 NSX 显式写目标、帝国的吞并目标依靠博弈类型，与任务 84 之前的共和起义同类。原版虾夷共和国事件也这样写，未改。
