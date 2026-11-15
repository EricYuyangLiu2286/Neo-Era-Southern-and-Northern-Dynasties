Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-14）
Blocked by: none
Validation: STATIC_PASS
Evidence: Toolkit 与 script_xcheck 报告 `nesnd-workbench/reports/2026-11-14-yan-unrest-event/`

# 104 「资助燕人会党」未被查明时通知中华帝国；东北七州迁入吸引力 +5%

## 1. 现象与期望

作者：点击成功且未被查明时，给中华帝国发事件【不满在东北积蓄】，写燕国宗室逃入深山、东北垦殖与驻军稀少、共和派活动，并显示激进派增加，不显示登莱方面的效果。另给东北各州加一个简单修正：本地迁入吸引力 +5%。作者选定：修正自开局起永久存在、不论归属，被查明时不加激进派。

## 2. 原因

原先激进派在按钮的 hidden_effect 里直接加给中华帝国，中华帝国玩家看不到。

## 3. 改了什么

- `common/scripted_buttons/nesnd_sha_restore_yan.txt`：`random_list`，25% 只降关系 −30，75% 向中华帝国发 `nesnd_cne_yan.6`。激进派不再在按钮里加。
- `events/nesnd_cne_yan_hints.txt`：新事件 `nesnd_cne_yan.6`，immediate 从七个起事州中随机选一处属于中华帝国的州，选项给辽东、女真人口各 +3% 激进派（选项提示里可见）。
- `common/state_traits/nesnd_dongbei_settlement.txt`：新州特性 `nesnd_state_trait_dongbei_settlement`，`state_migration_pull_mult = 0.05`。
- `map_data/state_regions/11_east_asia.txt`、`15_russia.txt`：辽东、吉林、松江、黑龙江、海参崴、勃利、五国七个州区加上该特性。
- 本地化（中英）：`nesnd_cne_yan_hints_l_*`（事件四键）、`nesnd_national_map_l_*`（特性名与说明）、`nesnd_sha_restore_yan_l_*`（按钮提示改写被查明的情形）。

## 4. 怎么复测

州特性在地图加载时生效，需要新开局。登莱点「资助燕人会党」，未被查明时中华帝国收到【不满在东北积蓄】，选项提示显示某州辽东、女真激进派 +3%。被查明时没有事件，只降关系。七个州的州面板应有「东北垦荒」特性。

## 5. 遗留问题

- 中华帝国为 AI 时也会收到该事件，自动选唯一选项。
