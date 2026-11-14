# 03 三角贸易成交与三个月的买卖约期

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（Victoria 3 1.15.1，待作者复测）
Evidence: [日志、存档比对、修改前后执行顺序与行号](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-13-triangle-settlement/trace.md>) · [变量读写、两语和脚本校验](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-13-triangle-settlement/settlement-checks.json>)

## 现象与期望

观察者看到三笔在途订单，同时显示「上一单失败：没有可用的成交单」。满条应结算原单，失败应说明理由；买卖选择锁定三个月，界面改称批次。

## 原因

1838 年 7 月明吴、蒙古卖往日本的两批，在 1839 年元旦仍是同一批人口，但买卖双方已被年度 AI 重置为暂停。南洋宣慰司卖往东洲的 1957 人也遇到卖方停卖。东洲仍在买，施行债务奴隶制。旧结算从州重新取所有国、重新计算人数及招募条件，许多分支共用一个失败码。轮转日志另记录了西洋目的州所有国失效及死亡人数算式取到空值。

## 改了什么

- `common/scripted_effects/nesnd_triangle_trade.txt` 保存每批原双方、人口、文化宗教、州和约定人数。只复核、执行该批。AI 保留现有选择，实际选边后加锁。
- `common/scripted_triggers/nesnd_triangle_trade.txt` 共用参与、目的州和按钮资格条件，锁定状态取自当前国家的限时修正。
- `common/scripted_buttons/nesnd_triangle_trade.txt` 两条航线的 12 个按钮共用资格与锁定判断。
- `common/static_modifiers/nesnd_triangle_trade.txt` 北洋和西洋各用独立的三个月计时修正。
- `common/on_actions/nesnd_triangle_trade.txt` 禁奴法生效立即撤销身份与锁定；其他资格失效由月度重算清理。
- `common/scripted_progress_bars/nesnd_triangle_trade.txt` 六条进度条以原定人数标记本批是否在途。
- `common/journal_entries/nesnd_triangle_trade.txt` 按真实结果显示原因，当周满条的批次全部结清后统一补单。
- `localization/{simp_chinese,english}/replace/nesnd_triangle_trade_l_*.yml` 两语的批次名、在途单、失败原因和三个月锁定提示。
- 本任务、同目录地图和项目 STATUS 记录交付与复测位置。

## 怎么复测

作者定稿的按钮提示为「我们每次选择后都必须等待三个月。」。北洋、西洋及英文均使用纯文字。批次名称仅在进度条显示。

推荐新开观察者局。可以重启后读 1839 年档观察后续新单。旧在途单缺签单身份，可能在第一次满条时报「无法确认下单时的卖方」，随后自动按新规则补单。原有模式从下次实际选边开始计时。

记下同一批的买卖双方、州、人数与文化，等条满后的周结。查迁移、目的州奴隶人数、双方成交通知、卖方货款、买方税收修正与途中损失。故意在约期满后暂停买入，剩余在途单满条应写明买方停止买入。选边后悬停改选和暂停按钮核对三个月提示，跨年观察 AI，废奴后查即时解锁和交易资格。两语显示甲／乙／丙批次及 Batch A／B／C。

## 遗留问题

最近结果每条航线只保留一笔，同周多批结算时以后处理的一笔为准。全库审计另报 Steam 文案解析 2 项、省份重复归属 132 项、建筑投资方重复 4 项，均在本次范围外。针对本次文件的 Toolkit 唯一提示是其 CK3 的 on_action 单数目录规则，Victoria 3 原版使用 on_actions。
