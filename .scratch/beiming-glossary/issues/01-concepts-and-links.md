# 01 北明与大革命的悬停名词及全文链接

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [round1.md](../round1.md)、[round2.md](../round2.md)、[作者答复](../author-decisions-20261112.md)，`nesnd-workbench/reports/2026-11-12-beiming-glossary/`

## 1. 现象与期望

作者原话：新建“北明”“大革命”两组游戏概念（主概念加子概念的悬停提示），并在 MOD 全部文本中把相关名词换成概念链接。先交概念草稿和样本，确认后再批量插入。

## 2. 原因

MOD 中原本没有解释北明时代与大革命的悬停条目。原版 1.15.1 用词汇表（`GAME/common/glossary/00_glossary.txt`）承载历史名词，MOD 已有一条先例 `common/glossary/nesnd_forest_of_bayonets.txt:1`。作者于2026-11-12确认采用词汇表。

## 3. 改了什么

- `common/glossary/nesnd_beiming_glossary.txt`：新增 15 条词条。
- `localization/{simp_chinese,english}/replace/nesnd_beiming_glossary_l_*.yml`：新增中英文标题与说明各 15 条。
- 20 个已有本地化文件：插入 94 处 `[Glossary(...)]`，其中中文 49 处、英文 45 处，只替换名词本身。文件清单与跳过位置见 round2.md。
- 技能 `nesnd-victoria3/lookup/canon/narrative-context.md`：记下作者的年代裁定，并指向答复原文。

## 4. 怎么复测

见 round2.md 的“复测时看哪里”：百科词汇表页、地权革命日志、flavorCNE.1.d、flavorCNE.15.d、flavorUSM.1.d 与 flavorUSM.4.d、共和派日志，中英文各看一遍。

## 5. 遗留问题

- 作者已答复：苏阿宏即苏宏，北明亡于1707年，说明长度不再压缩。
- 第一轮第八节的其他文本问题未改。

## Result

2026-11-12 完成。静态检查全部通过，包括 BOM、语言头、重复键、中英键名、引用、字面不变、pdx 解析和 audit。未实机验证。
