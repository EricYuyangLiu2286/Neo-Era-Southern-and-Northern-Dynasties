# 东洲与唐衣大食取消等级制度

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Validation: STATIC_PASS  
Blocked by: none  
Evidence: [回归结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-hus-per-abolition/checked.json>) · [工作台备份清单](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-hus-per-abolition-20261112T215103Z/manifest.json>)

## 现象与期望

两国在原法律组保留取消法。手动废法走立法流程，主体文化越过旧制界限时自动废除。已经取得的原住民汗国建国资格持续有效。

## 原因

东洲维护会按路线装回户籍法并冻结公民法，波斯每月会重设唐衣阶序。沙阿接管本已删除所有唐人主体文化、确保波斯文化为主体并恢复默认阶序。

## 改了什么

- 法律与组：`common/laws/` 和 `common/law_groups/` 各改 `nesnd_hus_social_hierarchy.txt`、`nesnd_per_tang_order.txt`。东洲在满蒙编户和人权之后、波斯在唐律宽和和政治煽动之后可以手动提案。
- 文化和维护：`common/scripted_triggers/nesnd_hus_registration.txt`，`common/scripted_effects/` 下的 `nesnd_hus_registration.txt`、`nesnd_per_tension.txt`、`nesnd_native_khanate.txt`。六个原版公民法仍用原有十二处锁判断；废除后停止冻结和回装。
- 立场：`common/ideologies/` 下 `00_ig_ideologies.txt`、`00_ig_ideologies_event.txt`、`00_ig_ideologies_flavored.txt`、`01_character_ideologies.txt`、`03_ig_ideologies_movement.txt`、`ce_legacy_social_democrat.txt`、`nesnd_keju_voting.txt`。
- 提示：新增 `events/nesnd_hierarchy_abolition.txt` 和中英 `localization/<语言>/replace/nesnd_hierarchy_abolition_l_<语言>.yml`。普通文化切换向玩家提示，迎立沙阿沿用现有剧情反馈。

## 怎么复测

1. 新局为验收基准。两国法律界面比较研究前后、前置法律生效前后和各集团态度。已运行的相应国家存档可以读档测试月度逻辑。
2. 分别在四等户籍、满蒙编户、原住民编户下增列欧洲主体文化，检查当月或次月取消、公民法解锁。满蒙编户增列满洲、原住民编户增列美洲原住民应保留。在未研究科技的档也测自动切换及文化恢复后不复辟。
3. 已取得汗国建国资格后先废法，再满足建国选州条件；与取得资格前废法对照。普通革命交接也应保留已获资格。
4. PER 保留任一唐人主体时可维持等级，移除最后一种则至迟次月废除。走迎立沙阿当天检查主体文化和默认阶序，下个国家月脉冲查取消法，随后再过一个月确认无重复提示。

## 遗留问题

游戏由作者复测。已按作者确认在 `common/journal_entries/nesnd_civic_routes.txt` 为「东洲编户」增加一个隐藏失效结局。读登记未满一年的存档增列欧洲主体文化，等取消法生效，检查日志静默关闭，再过原登记期限确认不会重新实行编户法。地图与建筑全局审计的 138 条既有报告与此前同路径审计逐项相同。

复核了 19 个游戏文本文件。新增提示事件补齐 UTF-8 BOM，逐字节比对确认玩法正文未变。Toolkit 对 19 个文件零诊断，已验证额外右括号反例。详见[编码清单](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-hus-per-abolition/debug-audit/bom.json>)和[Toolkit 报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-hus-per-abolition/debug-audit/toolkit-final/toolkit-checks.json>)。

## 后续修复（2026-11-12 23:25）

23:17 运行的 error.log 在读档时一次报 1,620 多条 `Invalid right side during comparison 'cu'`，位置 `common/scripted_triggers/nesnd_hus_registration.txt:106`（`nesnd_hus_manchu_culture` 的 `this = cu:manchu`），调用方是 `social_classes/nesnd_hus_social_classes.txt` 与 `social_hierarchies/nesnd_hus_social_hierarchy.txt` 的 `pop_criteria`。社会阶层人口条件里解析不了 `cu:` 链接。本 MOD 的满洲文化遗产是 `heritage_han`，比较失败时满洲人口会落入汉人阶层。已把 `nesnd_hus_manchu_pop` 改为人口作用域的 `has_pop_culture = manchu`（script_docs `triggers.log:8051`，原版社会阶层说明也用 `has_pop_religion = catholic` 这种写法），蒙古遗产分支不变。国家主体文化判断仍用 `nesnd_hus_manchu_culture`，那几处没有报错。备份 `backups/pre-change-hus-manchu-pop-key-20261112T232529Z`，Toolkit 零诊断。复测：读同一存档，error.log 不再有 `nesnd_hus_registration.txt:106`，东洲满洲人口应在满洲阶层。
