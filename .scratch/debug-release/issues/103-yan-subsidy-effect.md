Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-14）
Blocked by: none
Validation: STATIC_PASS
Evidence: Toolkit 报告 `nesnd-workbench/reports/2026-11-14-yan-subsidy/toolkit/`

# 103 「资助燕人会党」：随机一处 +3% 激进派，查明时关系 −30

## 1. 现象与期望

现效果：起事地区中由汴梁方面管辖的辽东、女真人口全部 +10% 激进派，25% 机会被查明，关系 −10。作者要求：从属于中华帝国的起事地区（辽东、吉林、松江、黑龙江、五国、海参崴、勃利）随机选一处，当地辽东、女真人口 +3% 激进派。查明几率仍为 25%，关系改为 −30。经费修正、费用、时长、按钮条件不变，提示同步。

## 2. 原因

数值调整，不是故障。效果直接写在按钮里（`common/scripted_buttons/nesnd_sha_restore_yan.txt:17–24`），用 `every_scope_state` 遍历 `nesnd_sha_yan_region`，不与其他按钮共用。不在 `original-20261030` 中（代理稿，2026-11-11 d8fabf8 起）。

## 3. 改了什么

- `common/scripted_buttons/nesnd_sha_restore_yan.txt`：`every_scope_state` 改为 `random_scope_state`（范围不变），两种文化各 0.10 → 0.03，关系 −10 → −30。没有符合条件的州时，`random_scope_state` 什么也不做，不报错。
- `localization/simp_chinese/replace/nesnd_sha_restore_yan_l_simp_chinese.yml`、`localization/english/replace/nesnd_sha_restore_yan_l_english.yml`：`nesnd_sha_yan_subsidy_terms_tt` 改为新效果。

## 4. 怎么复测

读档即可（未改变量和状态）。登莱共和国，复燕日志「资助燕人会党」按钮：悬停看提示，点击后查看七个起事地区，只有一处的辽东、女真人口激进派增加。

## 5. 遗留问题

- 「联络五国旧部」「联络辽东旧部」等联络按钮走 `nesnd_yan_contact_attempt`，只扣燕旗、记联络、触发事件，不加激进派，没有类似的“全部地区 +10%”写法。
- 脚本中经费修正为 `months = 12`，作者在游戏里看到“11 个月”，未改，未查。
