Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-cne-confidence-monthly-20261114T020856Z/`；报告 `nesnd-workbench/reports/2026-11-14-cne-confidence-monthly/`

# 97 中华帝国「帝国人民的信心」改为按月结算，转移支付按负债比例

## 1. 现象与期望

群内玩家反馈：“把转移支付的条件改成不负债过25%就行”，“这个欠钱就不能转移支付还是有点难蚌”，“但热情扣太快”。作者提出：经济为正、民生11以上可以提升信心。作者定稿：

- 原有各项年度值不变，改为每月结算十二分之一。满值是 1000。
- 收支为正、民生不低于 11 分成两项，各每年 +30。地主执政每年 -20。
- 加一个名词解释，说明哪些利益集团进入政府会增减信心。

## 2. 原因

- 「拨款官营工坊」「增拨转业救济」及其审批事件要求国库余额不少于拨款额（`nesnd_cne_reform.txt` 的 `nesnd_reform_can_invest`、`nesnd_reform_can_relieve`），所以只要欠债就无法拨款。
- 信心条原用 `yearly_progress`，各项都指向具名脚本值。按 GAME `scripted_progress_bars.md`，具名脚本值“计入但不列出”，悬停明细是空的。实际数值又由年脉冲写进变量，再 `set_bar_progress` 覆盖条，同一个值有两个写入者。

## 3. 改了什么

- `common/scripted_buttons/nesnd_crisis_buttons.txt`、`common/scripted_triggers/nesnd_cne_reform.txt`：余额条件改为 `scaled_debt <= 0.25`，按钮显示「债务不超过信贷上限的25%」。复核地权争讼仍要求余额（属于讼费，不是转移支付）。
- `common/scripted_progress_bars/nesnd_cne_confidence.txt`：改为 `monthly_progress`，每项写成带 `desc` 的 `progress_condition`，悬停逐项列出（未满足的显示空框）。新增收支为正 +2.5/月、改革地区劳动力生活水平不低于 11 +2.5/月、地主执政 -1.66667/月。右侧 `second_desc` 链接名词解释。
- `common/scripted_effects/nesnd_cne_confidence.txt`：条为唯一权威值。`nesnd_cne_confidence_pull` 把条值读回变量 `nesnd_cne_confidence`，原有阈值（900、750、600、500、0）照旧读变量。破产 -250、暂缓 +100 改由 `nesnd_cne_confidence_add` 经 `add_progress` 写到条上。年脉冲效果改为月脉冲 `nesnd_cne_confidence_monthly`。
- `common/journal_entries/nesnd_cne_confidence.txt`：`on_yearly_pulse` 改为 `on_monthly_pulse`。
- `common/script_values/nesnd_cne_confidence.txt`：删去不再使用的年度脚本值和 `nesnd_cne_confidence_annual_change`。
- `common/glossary/nesnd_cne_glossary.txt`（新）与中英 `nesnd_cne_land_reform_l_*.yml`：名词解释「帝国人民的信心」，另加 3 个条目名、债务提示和条右侧链接，共 7 键。

## 4. 怎么复测

以中华帝国读档或新开局，开始地权革命：

1. 悬停信心条：逐项列出每月增减，未满足的显示空框。每周收支转负、生活水平跌破 11 时，对应项的勾应消失。
2. 悬停条右侧「信心的来源」：显示名词解释。
3. 欠债但不超过上限 25% 时，两个拨款按钮可点，审批事件可选「照此拨付」。超过 25% 时按钮不可点。
4. 宣布破产后信心一次扣 250，「暂缓诸项改革」一次加 100，条和阈值事件（共和派起事等）一致。

## 5. 遗留问题

- 旧档：条值成为权威，原变量在下一次周检查时被条值覆盖。旧版年度结算可能已让条与变量有出入，以条上显示的数为准。
- 生活水平一项读月度统计 `nesnd_reform_sol`，与“民生与制度条件”同一统计范围（中华本土及东北诸州的劳动力）。
- 游戏外检查：Toolkit 9 个文件 0 诊断，本地化成对且无分号。vic3-tiger 在改动文件新增 16 条，均为其 1.19 规则不认识的 1.15 写法：`progress_condition` 14 条（任务 60 同样被报）、`Glossary` 数据函数 2 条。script_xcheck 同样只报 `progress_condition`。
