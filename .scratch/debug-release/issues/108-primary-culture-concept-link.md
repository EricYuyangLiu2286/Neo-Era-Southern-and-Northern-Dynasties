Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-16）
Blocked by: none
Validation: STATIC_PASS
Evidence: 扫描报告 `nesnd-workbench/reports/2026-11-16-concept-links/`；工具 `nesnd-workbench/tools/loc_link_check.py`；概念表 `nesnd-workbench/references/concepts-1.15.1.md`；备份 `nesnd-workbench/backups/20261116-concept-links/`

# 108 「承认和人为国人」说明：`[concept_primary_culture]` 报错

## 1. 现象与期望

决议说明末尾显示「便可承认日本文化为ERROR:[concept_primary_culture]」，error.log：`Could not find data system function 'concept_primary_culture'`、`Data error in loc string 'nesnd_usm_recognise_japanese_desc'`。应显示「主流文化」概念链接（原版中文译名是「主流文化」）。

## 2. 原因

原版 1.15.1 只定义了复数概念 `concept_primary_cultures`（`game/common/game_concepts/00_game_concepts.txt:1065`）。`concept_primary_culture` 只是显示用的本地化键（`concepts_l_simp_chinese.yml:1379`、`concepts_l_english.yml:1760`），不是概念，写成 `[concept_primary_culture]` 时引擎把它当数据函数解析。原版引用单数时写 `[Concept('concept_primary_cultures','$concept_primary_culture|q$')]`（如 `acceptance_statuses_l_english.yml:53`）。任务 96 的一次性脚本已修过同类写法，本键是之后新写的。

## 3. 改了什么

- `localization/simp_chinese/replace/nesnd_rising_warnings_l_simp_chinese.yml:65`、`localization/english/replace/nesnd_rising_warnings_l_english.yml:65`：`[concept_primary_culture]` → `[Concept('concept_primary_cultures','$concept_primary_culture$')]`，与本 MOD `ce_je_opium` 中已有写法一致。文字未改。
- 新工具 `loc_link_check.py` 扫描全部本地化：其他概念链接均有效。
- 扫描另查出 `nesnd_premier_l_*.yml` 14 个键（两种语言各 15 处）用 `SCOPE.sInterestGroup(...)`，1.15.1 没有这个函数；原版写 `SCOPE.gsInterestGroup(...)`（1032 处，dump 中 `TopScope.gsInterestGroup( Arg0 )` 返回 InterestGroup）。作者同意后全部改为 `gsInterestGroup`。改后扫描 0 条。部署 `729ea498` 之后。

## 4. 怎么复测

读档即可。决议「承认和人为国人」说明末尾显示「主流文化」链接，悬停为原版概念说明；重启后 error.log 不再有该键的报错。「统治者与内阁」的首相更替、对手、下台等事件中，利益集团名正常显示，不再出现 ERROR。

## 5. 遗留问题

无。
