# 54 「天竺的土地」改为成立天竺宣慰司

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [Tiger 前后对比与静态检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-tianzhu-commission/>)；改前备份 `nesnd-workbench/backups/pre-change-tianzhu-commission-20261107T014158Z`

## 1. 现象与期望

作者：「天竺的土地」只有一条终止条件，没有进度、按钮、目标和增益，测试局里从未起作用。原设计：USM 在印度占领比开局多一些的土地后，把这些土地组成殖民地附属国（天竺宣慰司），做法类似开局的南洋宣慰司。

## 2. 原因

- `nesnd_india_usm` 是任务25（`a062441`）的“常驻行政”日志，任务26（`adfc317`）后只挂六个镇压起义按钮；按钮要莫卧儿开始策动起义才显示。
- 建司在另一条日志 `nesnd_tianzhu_commission`，门槛为民主＋开化使命、12个印度大陆地区、3个土邦、2个莫卧儿腹地，且要开化使命才显示；建司用 `puppet`，与南洋的 `dominion` 不同。

## 3. 改了什么（作者确认：8个地区、自治领、海外宣慰司政体、含锡兰与印度洋领地、威望+20／权威+150 五年、镇压按钮移到天竺的庶务）

- `journal_entries/nesnd_india_core.txt`：「天竺的土地」改为小型里程碑：进度条、状态行、设立按钮；成立即完成，失地时静默关闭。保留六个镇压按钮。
- `journal_entries/nesnd_commissions.txt`：删除「筹建天竺宣慰司」；六个镇压按钮加到 TZ1 的「天竺的庶务」。
- `scripted_triggers/nesnd_india_core.txt`：日志只给不是附属国、天竺宣慰司尚不存在的 USM。
- `scripted_triggers/nesnd_commissions.txt`、`nesnd_commission_expansion.txt`：新门槛（直辖有人口的州分布在≥8个印度大陆地区，不在战争或外交博弈中，一年冷却）；删去只供旧门槛用的五个判断。
- `scripted_effects/nesnd_commissions.txt`：建司改为自治领，首府马德拉斯（不持有则取人口最多的州），加原版 `colonial_administration` 修正；新增共用的划拨效果。
- `scripted_effects/nesnd_india_core.txt`：去掉旧日志的入口。
- `scripted_buttons/nesnd_commissions.txt`：设立按钮用新门槛，AI 达标即建（100）。
- `decisions/nesnd_commissions.txt`：旧建司决议换成「将新得的天竺土地划归宣慰司」。
- `scripted_progress_bars/`、`script_values/nesnd_india_core.txt`：进度条「天竺直辖地区 X / 8」，每周按实数同步。
- `static_modifiers/nesnd_commissions.txt`、新文件 `events/nesnd_tianzhu.txt`：成立事件与「天竺开府」修正（只给一次）。
- 本地化中英：`nesnd_india_l_*.yml` 改写或新增 16 个键、删除 4 个；`nesnd_journal_closures_l_*.yml` 删除 2 个。作者改过的 `_reason` 未动。

## 4. 怎么复测

新开局为准（读档也能看到日志，进度条一周内同步）。玩 USM（大明联邦）：

1. 开局即在日志「天竺的土地」看到进度条 5 / 8、状态行和灰色的「设立天竺宣慰司」按钮（悬停看差几个地区）。
2. 控制台 `annex HYD`（海得拉巴、中央诸省 → 7）、`annex SAT`（孟买 → 8），按钮变亮；不在战争中点击。
3. 次日弹出「宣慰司开府」，选项给五年修正；地图上出现自治领「天竺宣慰司」，首府马德拉斯，日志完成。
4. 再 `annex MYB`（奥里萨），决议页出现「将新得的天竺土地划归宣慰司」，执行后新州归宣慰司。

## 5. 遗留问题

- 未实机验证：自治领能否建立、政体是否显示为海外宣慰司、宣慰司转大国后自治领关系是否保持、进度条显示。
- 宣慰司成立后，USM 新打下的印度州上若有起义筹备，USM 没有镇压按钮，要先划归宣慰司；「天竺的庶务」完成后宣慰司也不再有镇压按钮。
- 远山宣慰司（YU1）门槛同样过严，未改。
- `nesnd_commission_inherit_technology` 逐项复制约180项科技，未精简。
