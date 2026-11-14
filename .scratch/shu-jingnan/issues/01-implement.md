# 01 蜀国第二次靖难：执政选择、大汉与统一南方（实施）

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-12）
Blocked by: none
Validation: STATIC_PASS
Evidence: `nesnd-workbench/reports/2026-11-12-shu-jingnan/`（toolkit/、tiger/）。改动前备份 `nesnd-workbench/backups/pre-change-shu-jingnan-20261112T174739Z/`

## 1. 现象与期望

按 [spec.md](../spec.md) 第三稿实施，作者两轮答复见 spec 第 1 节。萧兴华（萧虎力之侄）与魏鉴同批登场，三人受剧情保护。战局转向不利时蜀国选择执政者：A 刘、萧续政后再选投降或续战，B 魏鉴自立。胜利后可成立大明，或成立大汉（萧虎力拥立刘氏，或魏鉴称帝）。大汉成立后，非中国属国可以独立，忠明国家多半拒绝附庸。另做通用日志「统一南方」与「重建大明」决议。

## 2. 原因

新内容。战时不新建日志，执政选择由「蜀军」日志周脉冲触发，比首都失守的检查早一步。引擎没有退出战争与改控制者的效果，两处按 spec 第 6 节的变通写法。

## 3. 改了什么

- 新增 `events/nesnd_sih_jingnan.txt`：.1 执政选择，.2 是否投降，.3 降后诸将，.4 借兵自立（蜀国已附从外国时直接走魏鉴线），.10 属国去留，.20 南方一统。
- 新增 `scripted_effects/`、`scripted_triggers/`、`static_modifiers/` 的 `nesnd_sih_jingnan.txt`：收复州县、刷 20 营步兵、6 个月保护期，投降结算（交出 5 州并整合、成为吴廷自治领、三将各按 65/30/5 处理），蜀国成立大明时原统治者改任本集团领袖并封贵族，两组战时修正，统一南方奖励。
- 新增 `nesnd_unify_south.txt`（journal_entries、scripted_triggers、script_values、scripted_progress_bars）：26 州判定、计数条、开启时宣称，适用范围与僵局判定。新增 `decisions/nesnd_restore_ming.txt`，复用 `nesnd_celestial_collapse.3`。
- `nesnd_war_collapse.txt`（日志）：蜀军日志加周脉冲，结局时移除两组修正。`nesnd_war_collapse.txt`（触发器）：首都失守判定在蜀国选择期间及选后 6 个月暂停。
- `ce_usm_the_last_days_of_ming.txt`：两个反吴日志的 invalid 结局加“已投降”一项，只此一处改动。
- `usm_civilwar_events.txt`：.4 在楚、淮覆亡时设全局标记。.9 让大吴获统一南方资格。.10 大汉拆为两项。.11 对大汉的拒绝权重 85/15，拒绝后双方互得全境宣称。
- `nesnd_south_restoration.txt`：改造 `nesnd_postwar_sih_great_han`，蜀国迎立原明时调用原统治者安置。`nesnd_south_settlement.txt`：所有胜者获统一南方资格。`nesnd_celestial_collapse.txt`：大明联邦获统一南方资格。
- 人物：`nesnd_asian_historical_leaders_overrides.txt` 加萧兴华模板，`nesnd_crisis_effects.txt` 同批招募，`nesnd_story_character_protection.txt` 三人保护至胜利后名分确定。
- 中英本地化 `nesnd_sih_jingnan_l_*.yml`（新），`nesnd_button_tooltips_l_*.yml` 改大汉选项两键。

## 4. 怎么复测

1. 新开局选蜀国，靖难开战后让吴军占一州。当周应弹「成都的去从」，首都失守事件不得先弹。
2. 选 B：刘忠明流亡，魏鉴即位，被占州收复（成都优先），该州出现 20 营线列步兵。6 个月内首都失守也不被吞并。
3. 读档选 A→投降：5 州归吴且为已整合州，蜀国成为吴廷自治领。**看蜀国是否退出战争**。反吴日志与蜀军日志应关闭。
4. 胜利后分别选两种大汉、成立大明，核对君主、刘忠明下落、原统治者的集团领袖与贵族身份。大汉成立后看非中国属国的事件与楚、淮的 .11 选择。
5. 统一南方：计数条读数、宣称、26 州齐后的 15 年修正。重建大明决议的显示与可用条件。

## 5. 遗留问题

- **未实机验证的两处变通**：投降后成为附庸是否让蜀国离开战争，以及州产权转出再转回是否让控制权回到蜀国（`nesnd_sih_rally`）。若后者不生效，只会刷兵，不会收复。
- vic3-tiger 1.19 对新日志报 `activation_description`/`outcome` 未知字段，全 MOD 日志同样报 692 处，属规则落后。script_xcheck 对 `ai_chance base` 与参数化变量的报错为误报。
- 刘氏宗亲从四川常用名中三选一（承恩、明远、文彬），年龄 32/38/45。
