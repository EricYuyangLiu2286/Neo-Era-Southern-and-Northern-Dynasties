# 100 登莱两个资助按钮对中华帝国无限叠加激进

Record: implementation  
Category: bug  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（1.15.1 / 26591675）  
Evidence: [改动前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-sha-coastal-aid-20261114T192726Z>) · [Toolkit](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-radicals-flood/toolkit/>) · [日志副本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-radicals-flood/logs/>)（本问题是数值累积，日志无对应报错）

## 1. 现象与期望

玩家群反馈（创意工坊 2026-11-14 14:10 版，用 CNE）：“疑似有无限加激进的 bug”“燕逆爆了以后也不停刷激进”“而且范围不局限于东北”。期望：登莱的煽动有上限、有间隔，不在十几年里持续给北朝核心州灌激进。

## 2. 原因

全 MOD 中会按时间反复给 CNE 加激进的只有登莱的两个资助按钮。CNE 自身的来源都是一次性事件选项。

- **「接济北朝共和党人」**（`common/scripted_buttons/nesnd_sha_shandong.txt:24`）：复燕结束后，在「渡海」「齐鲁之约」中可用，日志期限 15 年（`common/journal_entries/nesnd_sha_shandong.txt:10,107`）。每按一次，山东、直隶、北京三州**全部人口**激进 5%（`common/scripted_effects/nesnd_sha_shandong.txt:14-20`），第 6、12 个月再各 5%（`events/nesnd_sha_delay.txt:109-114`）。资助修正 12 个月到期后按钮立刻可再按，没有冷却和次数上限，AI 权重 15。第 12 个月的那一次与下一次按下同日，实际每年 15–20%，最长 15 年。`nesnd_sha_delay.8` 只查登莱是否原生，不查阶段是否已结束。这就是“燕逆之后、不限东北”。
- **「资助燕人会党」**（`common/scripted_buttons/nesnd_sha_restore_yan.txt:1`）：复燕筹备期（最长 12 年）每按一次，东北七州辽东人、女真人激进 10%，同样到期即可再按。主 MOD 现行版已把 AI 权重改为燕旗未满时 100，每年必按。
- 设计表（`.scratch/denglai-route/numbers-v1.md`）写的是“山东、河间、燕京人口激进化 5%，每 6 个月再 5%”，本意是推北朝越过全国激进 15% 的信心线，没有规定重复次数。实现没有设上限。

## 3. 改了什么

作者 2026-11-14 定：接济北朝共和党人加冷却，登莱为北朝附庸或盟友时禁用，AI 用对北朝关系 −100 避免卡住。资助燕人会党不改。

- `common/scripted_buttons/nesnd_sha_shandong.txt`：每次拨款只在当时和第 6 个月各加 5% 激进，去掉第 12 个月那次。经费 12 个月期满后再隔 6 个月才能重新拨款（变量 `nesnd_sha_coastal_cooldown` 18 个月）。登莱是北朝附庸或与北朝结盟时不可用。经费原本就有：12 个月的支出修正「华北共和党人经费」，每周 GDP 的 0.05%，现提成脚本值并在条款里显示金额。
- `common/script_values/nesnd_sha_shandong.txt`（新）：`nesnd_sha_coastal_weekly_cost`，修正和条款共用。
- `common/scripted_triggers/nesnd_sha_shandong.txt`：`nesnd_sha_free_of_cne`，用原版 `is_subject_of` 与 `has_treaty_alliance_with`。
- `events/nesnd_sha_delay.8`：第 6 个月那次只在登莱仍处于「渡海」或「齐鲁之约」、且不是北朝附庸或盟友时生效。
- `common/journal_entries/nesnd_sha_shandong.txt`：「渡海」开启时及每年，AI 登莱对北朝关系 −100。只用于整军路线，因为「齐鲁之约」要靠与山东主人的好关系请开登州。
- 中英 `nesnd_sha_shandong_l_*.yml`：条款改写，新增冷却和附庸／结盟两条条件说明。

每次拨款的激进总量从 15% 降到 10%，间隔从 12 个月变为 18 个月，最长 15 年内约 10 次。

## 4. 怎么复测

可以读档。

1. `tag SHA`，在「渡海」或「齐鲁之约」中按「接济北朝共和党人」。悬停应显示每周支出金额、冷却与附庸／结盟条件。
2. 三州激进在拨款时和第 6 个月各加一次，第 12 个月不再加。经费到期后按钮灰 6 个月。
3. 与北朝结盟或成为其附庸后，按钮不可用，已排期的第 6 个月那次也不生效。
4. AI 登莱进入「渡海」后，对北朝关系降到 −100，此后每年再降。

## 5. 遗留问题

未启动游戏。关系 −100 能否完全阻止 AI 接受结盟或被附庸，取决于原版 AI，未实测。北朝通过战争把登莱变为附庸仍可能发生，此时「渡海」会卡住，按作者定接受。
