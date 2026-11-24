Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-24，「源目录写法整理」会话调度的奥斯曼 B3）
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-ottoman-b3-20261124T193950Z/`；记录 `nesnd-workbench/reports/2026-11-24-ottoman-qinist/交付记录-B3.md`，检查 `checks-b3/`，模拟 `sim/ottoman_charter_sim.py`

# 121 奥斯曼：宪章与军营

## 1. 现象与期望

坦志麦特成功后的第一份路线日志。提示词：工作台 `reports/2026-11-24-ottoman-qinist/B3-提示词-宪章与军营.txt`。

## 2. 改了什么

- 新日志 `nesnd_ottoman_charter`：宪政、秦制两套议程各 6 项法律，加 .5 的选择与事件给的 60 个月加分，任一方 5 项先满即胜，240 个月超时。结局变量 `nesnd_ottoman_charter_outcome` = `flag:charter`／`flag:qin`／`flag:stalemate`，关闭变量 `nesnd_ottoman_charter_closed`。
- 入口：事件 .5 两个选项 `add_journal_entry`；已过 .5 的存档由 on_action `nesnd_ottoman_charter_fallback` 补加。
- 事件 .9「青年奥斯曼人」、.10「秦人的营规」（连续三次驳回：空闲将领开原版政变，否则军队激进派加永久不满）、.11「颁布宪章」。按钮「宪政派集会」「整饬军纪」共用 24 个月冷却。
- B2 收尾：「诸民同心」加「坦志麦特已经结束」。

## 3. 怎么复测

控制台 `tag TUR`，坦志麦特成功后选 .5 任一项，日志出现；`event nesnd_ottoman_recovery.9`、`.10`、`.11` 看文字与选项；日志面板看两组条件逐项打勾。

## 4. 遗留问题

- `nesnd_ottoman_charter_outcome` 只写不读，留给 B5 与后续「议会」段。
- B3 修复：胜负条件增加法律项（c1–c6 / q1–q6）至少 4 项；.9/.10 军队限时代价改用新修正 `nesnd_ottoman_army_vexed`；秦制胜清除三种限时军改修正与 `nesnd_ottoman_reform_pending`/`nesnd_ottoman_reform_term` 并在军改按钮 `possible` 中排除 `nesnd_ottoman_qin_state`；.10 政变分支补 `je_ip4_coup` 与 `coup_event_active` 守卫；修订 .9/.10 首都、标题与措辞。
