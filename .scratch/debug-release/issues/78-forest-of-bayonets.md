# 78 刺刀之林与人民之春

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [1.15.0 双语逐段比对、术语解析及文件指纹](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-forest-of-bayonets/static.json>)

## 现象与期望

《刺刀之林》正文及“1830年革命”术语沿用现实法国和波兰史。作者要求只改正文首段，保留“自由、平等、博爱”段落。波兰背景限于术语悬停。

## 原因

主 MOD 原来沿用本体 ip5_04 的日志正文和术语链接。后继日志在 content_105 中仍以“后拿破仑时代反动秩序”起笔。

## 改了什么

- 中英文 replace 目录的 nesnd_forest_of_bayonets 本地化文件分别覆盖两篇日志正文，并提供新术语的标题和释文。《刺刀之林》第二段及警告、《人民之春》的三色旗句及操作说明均逐字比对原版。
- common/glossary/nesnd_forest_of_bayonets.txt 注册“1829年的和议”链接的术语，标题复用现行外交条约名。

## 怎么复测

重启游戏后用法国或其他欧洲参与国打开《刺刀之林》，悬停“1829年的和议”。核对正文第二段和末行警告，再于革命之春爆发后查看《人民之春》的开头及街垒提示。英文界面可在同一位置复核。

## 遗留问题

术语弹窗及两个日志窗口尚待实机复核。另见既有英文波兰日志 je_ce_the_polish_problem_reason 的维也纳会议叙述，属波兰专线。
