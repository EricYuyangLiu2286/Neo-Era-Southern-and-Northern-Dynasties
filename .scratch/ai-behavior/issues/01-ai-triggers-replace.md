# 01　AI 触发器由整文件覆盖改为按键 REPLACE

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude (Opus 5.5)
Blocked by: none
Validation: STATIC_PASS
Evidence: [研究报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/2026-11-14-ai-tendency/report.md>)；检查目录 `WORK/reports/2026-11-14-ai-triggers-replace/`（`extract_triggers.py`、`verify_triggers.py`、`tiger-after.json`）；备份 `WORK/backups/pre-change-ai-triggers-replace-20261114T183109Z`

## 1. 现象与期望

作者（2026-11-14）问 MOD 能不能不覆盖原版文件，改用 `ce_` 开头的文件写 `REPLACE:` 加 `always = no`，并同意先改 AI 触发器。

## 2. 原因

`common/scripted_triggers/00_ai_triggers.txt` 是整文件覆盖：75 个触发器中只有 4 个与 1.15.1 原版不同，原版更新时其余 71 个会被旧副本挡住。默认 AI 策略（`common/ai_strategies/00_default_strategy.txt`）只有一个对象，`REPLACE:` 也得整份复制，而且它由 define 指定、`always = no` 关不掉，所以这次不动。

## 3. 改了什么

- 新增 `common/scripted_triggers/ce_ai_triggers.txt`：用 `REPLACE:` 替换 `ai_has_reasons_to_not_oppose_law`、`ai_has_enact_weight_modifier_journal_entries`、`has_je_conquest_reason`、`has_je_subjugation_reason`，内容原样取自旧覆盖文件。
- 删除 `common/scripted_triggers/00_ai_triggers.txt`（已备份）。
- 技能：`lookup/vanilla-overrides.md` 新增单条覆盖表，同路径清单去掉这个文件；`references/ai-behavior.md` 改写覆盖说明。

## 4. 怎么复测

游戏外：`verify_triggers.py` 确认“原版 + 4 个 REPLACE”与旧覆盖逐键一致（75 键，EQUIVALENT）。vic3-tiger 把 `ce_ai_triggers.txt` 识别为有效定义，没有 replace 或重复报错；这个文件里的 10 条报告是 tiger 规则落后（`has_military_reach`、`carrying_capacity`），原版文件里也有。

游戏内（待作者）：新开局后 `error.log` 不应出现与 `ce_ai_triggers.txt` 或这 4 个触发器相关的报错。美国昭昭天命的 AI 仍会对南北大垣发起博弈。

## 5. 遗留问题

- 默认 AI 策略仍是整文件覆盖（24 行改动：昭昭天命、阿拉斯加、勃利、日本宿敌宣称）。
- ~~技能的 `scripts/vanilla_overrides.py` 会整体重写清单~~ 已修（2026-11-14，作者要求）：现在只生成“内容有改动”及之后的三节，前面的手写部分原样保留，并检查其中引用的路径是否存在。用当前清单重新生成，结果与现有清单内容一致；两种保护分支也各测过一次。工具备份在 `WORK/backups/pre-change-vanilla-overrides-tool-20261114T183408Z`，输出在 `WORK/reports/2026-11-14-vanilla-overrides/`。
