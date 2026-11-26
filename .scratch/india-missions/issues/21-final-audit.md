# 21 印度线总核验与收尾（批次 18）

Record: implementation  
Category: audit-and-fix  
Status: ready-for-agent  
Execution: completed  
Assignee: agy  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/总核验/交付记录.md) · [开局审计](../../../../nesnd-workbench/reports/2026-11-21-india-development/总核验/开局审计.md) · [结局可达表](../../../../nesnd-workbench/reports/2026-11-21-india-development/总核验/结局可达表.md) · [文本核验](../../../../nesnd-workbench/reports/2026-11-21-india-development/总核验/文本核验.md) · [扩展模拟对比](../../../../nesnd-workbench/reports/2026-11-21-india-development/总核验/sim/对比报告.md)

## 现象与期望

批次 11–17 完成后，对印度线全线执行五项收尾工作（开局审计、结局可达表、扩展模拟、总代码核验、总文本核验），并将查出的脚本、数值与文案问题在本批直接修复，不改动 `nesnd_per_*`、`nesnd_ott_*` 与大陆会议文件。

## 改动

- **开局错开与压力门槛（A 节）**：
  - `common/scripted_triggers/nesnd_india_core.txt`、`common/on_actions/nesnd_india_core.txt`：新增 `nesnd_india_indep_ready_to_open`（要求独立倾向 ≥ 55、与宗主关系 ≤ `poor`、或有改革/工程/外援推进），使「谋求独立」与「属邦动向」不再于 1836.1.1 首月同开；删去 `on_actions/nesnd_india_core.txt:5-6` 中只读不写的历史残留变量 `nesnd_mug_loan_from`。
  - `common/scripted_triggers/nesnd_india_princes.txt`：`nesnd_india_mission_country` 将印度帝国开启「出使求援」错开至独立或学务/实业/改革完成后；`nesnd_india_union_live` 加入压力/推进门槛（自强之邦、帝国完成学务/改革、或与帝国关系 ≤ `poor`），消除「土邦联合」首月开启与 1836 年即成约问题。
  - `common/scripted_triggers/nesnd_india_empire.txt`、`events/nesnd_india_empire.txt`、`common/scripted_progress_bars/nesnd_india_core.txt`、`common/scripted_effects/nesnd_india_empire.txt`、`common/journal_entries/nesnd_india_empire.txt`：旧约争议触发与 AI 门槛由 `LD >= 50` 抬至 `>= 65`（AI 停缴 `>= 70`）；谈判条关系扣分由 `<= 0` 改为 `< 0`，被动步进由 `±1` 改为 `±0.5`（纯被动需 100 个月 ≥ 60 个月）；宗主「许以新款」补 `change_relations = +10`，宗主重申阈值改为 `<= poor`；废约结局对仍为附属国的莫卧儿改设 `secret_goal = dominate`（脱离后设 `conquer`），保留首都州宣称。
  - `common/scripted_triggers/nesnd_india_rivalry.txt`、`common/script_values/nesnd_india_rivalry.txt`、`common/journal_entries/nesnd_india_rivalry.txt`：法明对立关系门槛由 `<= 0` 改为 `<= relations_threshold:poor`；属邦项改为比较双方印度属邦所持印度州数（开局法 26 对明 15，与直辖州 1 对 6 平衡）；在月度脉冲补上 AI 每月 `1%` 提议划界（修复《孟买条约》AI 永远走不到的问题）。
- **结局可达与守卫补齐（B/D 节）**：
  - `common/scripted_effects/nesnd_india_core.txt`：`nesnd_india_refresh` 为非 `usm_live`/`tianzhu_governance_live` 的殖民州持有者初始化 `nesnd_india_case_watch_clock`（`RESET = no`），修复 0 起事时「南方安定」永不触发的缺口。
  - `events/nesnd_india_foreign.txt`、`common/journal_entries/nesnd_india_princes.txt`：对 `add_involvement` 补齐 `NOT = { any_scope_state = { region = ... } }` 运行时守卫（规则 27）。
- **总文本核验修订（E 节）**：
  - 通读 `git diff 8740e95^ HEAD` 全部 542 对中英键，直接修订 27 个唯一键名（代码改动对齐 5 键、事件正文去具体条款与 UI 词 3 键、去重复概念链接 2 键、去「触发/修正」术语 9 键、统一英式 `Despatch` 与引文破折号排版 8 键）。

## 代码无法证实

全部 7 批遗留「代码无法证实」项已汇总并二次检索原版脚本与 `script_docs`，详见交付记录对应表格（其中 `add_fervor_target_modifier`、`add_to_variable_list` 带 `days`、`has_strategic_region_interest_tier`、`GetCurrentInterestTierTypeIn`、`create_bidirectional_truce`、`has_social_class`、`add_cultural_community`/`add_homeland` 均已查到原版脚本或 `script_docs` 出处；仅少数参数化变量作用域写法仍无原版直接实例，已写明失效表现与兜底）。本批扩展模拟为设计估算，不算实机验证。
