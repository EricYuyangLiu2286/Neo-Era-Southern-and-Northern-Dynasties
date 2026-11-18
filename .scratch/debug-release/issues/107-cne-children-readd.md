# 107 中华帝国子日志重复添加

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [v3tree 配置、观察者存档解码](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-16-cne-journals>) · [日志](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-15-yangtze-formal-observer/error-at-save.log:306>)

## 1. 现象与期望

观察者局 error.log 第 306–315 行：“中华帝国 already has a journal entry of type”，土地、信心各一次，国家城市化（urban）、营产（camps）各三次。期望：不再重复添加。

## 2. 原因

链条（v3tree `near` 核实）：`ce_cne_land_reform` 的月度脉冲（`common/journal_entries/ce_cne_land_draft.txt:15`）→ `nesnd_land_monthly` → `nesnd_land_init` → `nesnd_cne_programs_init` → `nesnd_cne_ensure_children`（`common/scripted_effects/nesnd_cne_confidence.txt:1`）。

每个国家开局就有这四个子日志的未激活实例；`is_shown_when_inactive` 与 `possible` 成立后由引擎自行激活（原版 `journal_entries.md` 第 48 行）。`has_journal_entry` 只看已激活的条目，所以地权革命开始（1836.1.16）到各子日志自行激活之间，每次脉冲都对已存在的未激活实例再 `add_journal_entry` 一次。观察者存档（1836.3.9）显示四个子日志已激活：土地 1.21、信心 1.22、营产 2.2、城市化 2.3，之后不再报错。加入从未成功，也不影响玩法，只是日志噪音。

## 3. 改了什么

- `common/scripted_effects/nesnd_cne_confidence.txt`：四个判断各加 `NOT = { has_inactive_journal_entry = … }`。只有子日志已经结束、实例不在时才重新添加，与 `nesnd_per_campaign.txt:33` 同一写法。

## 4. 怎么复测

已部署 `55b80fd0`。新开局让中华帝国开始地权革命，推进到 1836 年 2 月以后，error.log 中不应再有中华帝国四个子日志的 `already has a journal entry`。读旧档也可以看，但旧档里这四个条目已激活，本来就不会再报。

## 5. 遗留问题

- 这四个日志只对中华帝国有意义，却在 262 个国家各留一个未激活实例并持续求值。原版用 `disable_evaluation` 写永久身份条件（如 `NOT = { this = c:CNE }`）来省掉这类开销，但要先确认改名、继承后的中华帝国仍能匹配，本次未改。
