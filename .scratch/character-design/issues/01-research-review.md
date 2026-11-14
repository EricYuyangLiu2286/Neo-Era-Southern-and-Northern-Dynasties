# 01 人物设计研究的复核与调整

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: NOT_APPLICABLE（文档与工具，无游戏行为）
Evidence: [复核报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-character-design-review/复核报告.md>)、[研究目录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/2026-11-14-character-design/README.md>)

## 现象与期望

作者要求复核 GPT 的“人物设计研究”是否真实、完整、可用，修正技能参考的事实与语法错误，再按复核提出的六个待决问题的默认选项处理。

## 原因

- 原版事实与出处可靠（抽查 30 条，28 条精确吻合，2 条偏一两行）。
- 技能参考以工坊 MOD 设计为依据，与“不学习其他作者设计”的硬规则冲突。
- 六类缺“宠臣”和“复国”，原版正有对应案例（`common/character_roles/00_auto_assigned_roles.txt:307`、`events/french_pretenders.txt:4`、`events/heavenly_kingdom_events.txt:300`）。
- 内容树工具不跟踪放进变量列表的人物，洪秀全结案时经头像列表撤保护一步（`common/journal_entries/nesnd_xiuquan.txt:148`）不在图上。

## 改了什么

- 技能：人物参考拆为 `character-design.md`（共用骨架、反例、清单）、`character-court.md`（继位、宠臣、觊觎者与复国）、`character-office.md`（煽动者、席位、跨国人物、经理、日志负责人），只引原版和 NESND；路由移到 SKILL.md 第 5 节；`regional-history-and-survival.md` 重叠句改为指向；`tools.md` 写入 `person`；MIGRATION.md 登记改写。两个副本已同步。
- 仓库：2a86315 从修复分支移到 `skill/character-design-20261114`（ccc3fdf、db9351d），已推送。
- 工具：V3-content-tree 新分支 `character-nodes`（842ea65，已推送），补变量列表跟踪和一项测试，25 项测试通过。
- 研究目录：增补拉斯普京、宠臣议程、法国觊觎者、太平天国四张案例卡，分类改为八类，19 张树重新导出并通过 `verify.py`。

## 怎么复测

读 `character-design.md` 的分类表，按一类打开对应文件与研究目录的案例卡；在 V3-content-tree 的 `character-nodes` 分支运行 `python -B -m unittest discover -s tests`。

## 遗留问题

- 两个分支已按作者要求合入各自的 main 并推送：NESND `db9351d`，V3-content-tree `842ea65`。修复分支 `fix/tooltip-concepts-observer-buttons` 已并入新 main（`bb62624`，已推送），技能 SKILL.md、MIGRATION.md、tools.md 的冲突保留两边内容解决。
- 新代码骨架只核对了 script_docs 与原版写法，未实机验证。
