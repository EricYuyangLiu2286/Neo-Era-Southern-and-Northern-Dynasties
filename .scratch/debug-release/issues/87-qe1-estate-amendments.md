# 87 西秦开局营产修正案

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [Tiger 原始输出](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-10-qe1-estate-amendments/tiger.json>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-qe1-estate-amendments-20261110>)

## 现象与期望

作者要求：1836 新开局时，西秦（QE1）的佃农制挂“营产完全所有律”，职业军队挂“设置特许军州”。修正案的可提出条件由作者改为：对应利益集团（地主/军队）在政府中或强大，或主要文化属儒家文化圈传统（tradition_sinosphere）。

## 原因

两条修正案原先的 `possible` 是 `c:CNE ?= this has_modifier = nesnd_cne_estate_settlement`（`common/amendments/nesnd_military_estates.txt`），只对中华帝国在“二十年之约”事件之后放行，QE1 开局不满足。

## 改了什么

- `common/amendments/nesnd_military_estates.txt`：两条 `possible` 改为作者给的条件。营产完全所有律看 `ig_landowners`，特许军州看 `ig_armed_forces`；两条都可由儒家文化圈主要文化放行。
- 追加要求：中华帝国（CNE）须先经事件解锁。两条 `possible` 加 `trigger_if = { limit = { c:CNE ?= this } … has_variable = nesnd_cne_estate_settled }`。
- `common/scripted_effects/nesnd_cne_military_estates.txt`：`nesnd_cne_settle_military_estates`（flavorCNE.2、.9、.10 调用）在挂案前设永久变量 `nesnd_cne_estate_settled`。不用 20 年修正判断，是为了约期满后中华帝国仍保有资格。
- 中英本地化新增 `nesnd_cne_estate_settled_tt`（条件提示）。
- `common/history/countries/QE1 - Western Qin.txt`：法律之后按原版奥地利、法国、西班牙历史文件的写法 `active_law:lawgroup_x ?= { add_amendment = { type sponsor = PREV.ig:… } }` 挂上两案，发起者分别为地主、军队。未写 `cooldown`（同奥地利）。

## 怎么复测

新开局 → 西秦 → 法律界面：佃农制、职业军队上各显示一条修正案；国家修正列表含两案的效果（地主/农民/军队政治力量、农业产出 +10% 等）；地主与军队集团带“维护营产”意识形态。

中华帝国：新开局时两条法律上没有这两案，修正案的可提出条件里显示“政府已与营伍订立营产与军州二十年之约”且未满足；触发 flavorCNE.2/.9/.10 之后两案挂上，条件满足。

## 遗留问题

- 儒家文化圈分支使两案对本 MOD 几乎所有华夏国家全程可提出，地主与军队会主动发起（`would_sponsor`）。中华帝国除外：须先经 flavorCNE.2/.9/.10 订约。
- `ai_will_revoke = { always = yes }`：AI 操控的西秦在合法性够时会尝试废止两案；西秦没有二十年锁。
- 中文 `amendment_nesnd_cne_estate_ownership_desc` 句子不通（“……土地。无论在城市或是乡村，并将其上获得的产出……”）。未改。
- 原有：QE1 与 CNE 历史文件里各有一行 `add_ideology` 跟在注释后面被一起注释掉（QE1 `ideology_patriotic`、CNE `ideology_oligarchic`）；QE1 `law_racial_segregation` 重复激活。未改。

## Comments

2026-11-10：作者测试完毕。正文中“未启动游戏”“待复测”等为交付时的状态。
