# 蜀国第二次靖难：人物、执政选择、大汉与统一南方（第三稿：定稿待确认）

只交方案，不写脚本。作者确认本稿后另开实施任务 `issues/01-implement.md`。

## 0. 核对要点

- 蜀国真正的战败是 `usm_civilwar.4`（首都失守或敌占 >80%，蜀国人物 1:5 流放或处死，被大吴 `annex_as_civil_war`）。`.11 → .12/.13` 是“别国已胜，余下反吴国服从还是独立”。
- 作者原作 `usm_civilwar.2` 的“蜀王出逃”（`sih_shuwang_ran_off_tt`）被代理删去，键仍在。本方案用它作 B 线文案。
- 蜀国获胜后吞并大吴并 `change_tag = USM`。战后内容都挂在 USM 上。
- 现有蜀军修正 `nesnd_shu_army`：军事商品 −20%，攻防 +20%。新修正与它叠加。
- 大明联邦的成立写法见 `nesnd_celestial_collapse.3`（`events/nesnd_celestial_collapse.txt:75`）。其中“原统治者改任地主集团领袖并封贵族”在同文件 :142-158，拒绝加入的处理在 :199。
- 首都失守每周检查（`nesnd_check_war_collapses`，`ce_code_on_actions.txt:44` 也挂了 `usm_civilwar.5`）。
- 引擎缺口：1.15 的 `docs/effects.log` 和 GAME 脚本里，既没有让单个参战国退出战争的效果，也没有直接改州控制者的效果。见第 6 节。
- 现有的南方僵局日志有三个：大吴的「残局」`nesnd_south_holdout_campaign`，明廷停战后的 `nesnd_ming_after_truce`，开战前的 `nesnd_south_reconciliation`。

## 1. 作者答复

第一轮（2026-11-12）：萧兴华与魏鉴同批招募。魏鉴保留原作模板与登场时机，三人都做剧情保护。执政选择取代“蜀王出逃”。劣势触发。复明、革命两种日志都弹。蜀国已附从外国时直接走魏鉴线。投降时魏鉴、萧虎力各 65% 流亡、30% 被杀、5% 一同投降。士气按“少掉士气”，产品开销用所有建筑投入品，与蜀军修正叠加。AI 权重 15/45/40。大汉在胜利时二选一，走过政变仍可成立大明，原统治者改任集团领袖并封贵族。忠明国家 AI 85% 拒绝，拒绝后双方互得全境宣称，另做重建大明的决议。属国独立 35%，玩家自选。统一南方不设时限，奖励权威、威望、行政力、荒废恢复，持续 15 年，做成通用日志。不做蜀国失败事件，但要理顺触发顺序。开局至起义不加内容。

第二轮（2026-11-12）：

| # | 答复 |
|---|---|
| 1 | 萧兴华是萧虎力的侄子，其余由代理设计（见第 3 节）。 |
| 3 | B 线刘忠明出逃，沿用原作“乘船逃出成都”的文案。 |
| 6 | 投降：交出的 5 州直接成为大吴的已整合州，蜀国保留成都一州，成为大吴附庸。 |
| 7、8 | 朱慎徽不动。萧兴华在投降时同样按 65/30/5 处理。 |
| 9 | 大汉二选一：萧虎力推举一位刘氏亲族为汉帝，或魏鉴称帝。 |
| 10 | 重建大明决议的目的是促进南方统一。凡上面讨论过的情形陷入僵局都可用，MOD 已有内容覆盖的情形除外。 |
| 12 | 宣称、奖励数值、适用范围全部同意。 |
| 13 | 保护期改为 6 个月。选定时，成都或随机一个被占领的蜀国州翻回蜀国控制，并在该州刷 20 个步兵营。 |

## 2. 内容树（定稿）

```
[现有] usm_civilwar.2 → 2.2 复明 / 2.3 革命（作者原作日志，不改）
  └─ nesnd_raise_jingnan_officers（nesnd_crisis_effects.txt:353）
       招魏鉴（现有）＋[新] 招萧兴华（同条件：SIH、1860 年前、未出生过）
[改] 剧情保护 nesnd_story_character_protected：魏鉴、萧兴华、萧虎力
     保护期从“反吴日志在”延到“胜利后名分未定”（nesnd_rebel_settlement_waiting）
[现有] 蜀军日志 nesnd_shu_army_journal（nesnd_war_collapse.txt:57）
  ├─ [新] on_weekly_pulse：未定 regime 且满足任一 → nesnd_sih_jingnan.1
  │     a 大吴一方控制蜀国任一州  b 敌占 ≥25%  c 楚或淮已被吞并  d 首都失守条件已满足
  │     例外：已是大吴以外国家的附属国 → nesnd_sih_jingnan.4「借兵自立」，效果同 B
  └─ [改] 结局：移除两个战时修正
[新] nesnd_sih_jingnan.1「执政选择」（SIH，一次）
  ├─ A 刘忠明、萧虎力续政 → .2
  │    ├─ A1 刘忠明投降（AI 15）
  │    │     川东、川南、梓潼、贵州、云南 5 州交大吴，并直接成为已整合州
  │    │     蜀国保留成都，成为大吴附庸，退出战争（写法见第 6 节）
  │    │     魏鉴、萧虎力、萧兴华各自 65% 流亡 / 30% 被杀 / 5% 留下 → .3 通知结果
  │    │     移除反吴身份，反吴日志、蜀军日志随之关闭，不再进入 .4/.10/.11
  │    └─ A2 萧虎力续战（AI 45）：regime=1
  │          修正 nesnd_sih_xiao_holds：军事商品 −25%，士气损失 −10%，攻击 +15%
  └─ B 魏鉴自立（AI 40，需魏鉴在世且在蜀）：regime=3
        刘忠明出逃（流亡，沿用 sih_shuwang_ran_off_tt 的文案），魏鉴即位，朱慎徽不动
        修正 nesnd_sih_wei_rules：士气损失 −20%，攻击 +20%，建筑投入品 −10%
  A2、B、.4 共有：
        成都若被占，翻回蜀国控制，否则随机翻回一个被占的蜀国州（没有被占的州就跳过）
        在该州刷一支 20 营正规线列步兵的部队
        6 个月内蜀国不触发首都失守事件 .4/.5
胜利 → [现有] usm_civilwar.10
  ├─ [改] 成立大明（nesnd_postwar_restore_original_ming）
  │     蜀国原统治者（刘或魏）改任本集团领袖并封贵族（照搬 celestial_collapse.3）
  │     刘忠明是地主集团，魏鉴是农村民众集团
  ├─ [改] 成立大汉·萧虎力推举刘氏：刘忠明在世且在国内就由他做汉帝，否则新建一位刘氏亲族（四川文化，30–50 岁）
  └─ [改] 成立大汉·魏鉴称帝（需魏鉴在世且在国内）：刘忠明若在世，“事故”身亡
        └─ [改造] nesnd_postwar_sih_great_han（加一个君主参数）
             ├─ [现有] nesnd_commit_rebel_settlement：吞并大吴，change_tag USM
             ├─ [新] 每个非中国直属属国弹 nesnd_sih_jingnan.10（AI 35% 独立，玩家自选）
             └─ [新] 开启统一南方
[现有] 其余反吴国 → usm_civilwar.11
  └─ [改] 胜者为大汉、本国为 nesnd_ming_federation_loyalist 时：
        拒绝的 AI 权重 85%。拒绝后双方互得对方全境宣称（现为只宣称首都州）
[新] 决议 nesnd_restore_ming「重建大明」（适用条件见第 4 节）
     效果：照搬 celestial_collapse.3，成立大明联邦，迎立朱氏，其余拥明国家称臣或拒绝
[新] 通用日志 nesnd_unify_south「统一南方」（适用范围见第 4 节）
  ├─ 开启：对 26 州中未拥有的州加宣称
  ├─ 状态量：本国或附庸拥有的目标州数 n/26（脚本值，只显示）
  ├─ 成功：26 州齐 → nesnd_sih_jingnan.20
  │     修正 nesnd_south_unified，15 年：权威 +20%，威望 +20%，行政力 +15%，荒废衰减 +50%
  └─ hidden invalid：国亡
```

26 州沿用第一稿：蜀 6、楚 4、淮 2、大明联邦 14。东京、松江、皖北、汉中和海外诸州都不列入。

## 3. 萧兴华人物模板（代理设计）

除“萧虎力的侄子”外，以下都是代理拟定，作者可改。

| 项 | 值 | 理由 |
|---|---|---|
| 模板 | `USM_xiao_xinghua` | 与 `USM_xiao_huli` 并列 |
| 生年 | 1818.1.1 | 比叔父小 26 岁，与魏鉴（1814）同辈 |
| 文化 / 宗教 | `cu:ce_sichuan` / `rel:kaimeng_confucianism` | 与魏鉴相同 |
| 职务 | 将领，`commander_rank_2`，`hq = region_south_china`，`home_region = STATE_SICHUAN` | 起义中带兵，低魏鉴一级 |
| 利益集团 | `ig_armed_forces`，不当领袖 | 随叔父的军中一系，叔父是现任军队领袖 |
| 意识形态 | `ideology_royalist` | 复明一派，与魏鉴的波拿巴主义对照 |
| 特质 | `honorable`、`persistent`、`mountain_commander`、`experienced_defensive_strategist` | `persistent` 与叔父相同，山地与守御对应蜀中关隘 |
| 其他 | `historical = yes`，`on_created` 设全局变量 `nesnd_born_usm_xiao_xinghua` | 照魏鉴写法，防止重复生成 |

侄子关系只写在本地化里。引擎没有亲属系统。

## 4. 适用范围

**统一南方。** 有以下标记的国家开启：

- 大汉
- 蜀、楚迎立原明
- 楚国共和
- 淮国复明
- 其他反吴国通过 `.10` 获胜
- 大明联邦（`celestial_collapse.3`）
- 以决议重建的大明
- 维持现状的大吴（`.9`）

另有一条通用规则：只在 `nesnd_south_settled` 或 `usm_civilwar_status_quo` 之后开启，并且本国当时没有「残局」「停战后的明廷」「和解」三个现有日志。全胜的大吴、北朝和外国不开。

**重建大明决议。** 满足以下全部条件时可用：

- 本国为 `nesnd_ming_federation_loyalist`。
- 本国不是附属国。
- 当前没有活着的大明朝廷（无人有 `nesnd_ming_court`）。
- 南方处于僵局，即靖难已结束（`nesnd_south_settled` 或 `usm_civilwar_status_quo`），且 26 州不在同一国及其附庸手中。
- 本国拥有南京，或拥有 26 州中的至少 8 个。

若大吴还在且有 `tag_WUU_var`，决议不可用，因为这种情形现有的「残局」和停战日志已经覆盖。

## 5. 触发顺序

1. 执政选择每周检查，比首都失守事件更早进入（触发条件 d 保证首都已失时也先弹选择）。
2. `.1` 弹出后到选定前，蜀国设 `nesnd_sih_regime_pending`，`.4/.5` 对蜀国暂停。
3. 选 A2、B 或进入 `.4` 借兵线后，设 `nesnd_sih_grace`（6 个月）。期间 `.4/.5` 对蜀国暂停，州控制翻转和 20 营步兵立即生效。
4. 选 A1 后，蜀国移除 `usm_opposition_country`，`.4/.11` 都不再针对蜀国。
5. 6 个月后若首都仍失、敌占仍 >80%，照常进入 `.4` 并被吞并。

## 6. 引擎缺口与拟定写法（实施后需你实测）

- **A1 退出战争。** 拟定：先把 5 州 `set_state_owner = c:USM` 并整合，再由大吴对蜀国建附庸条约。附庸条约能否让蜀国当即离开战争，静态检查无法确认。若不能，退路是在同一效果里结束蜀国作为反吴方的身份，使其不再是战争目标，由现有结算收尾。
- **州控制翻回蜀国。** 拟定：对目标州先 `set_state_owner` 给占领方，再 `set_state_owner` 回蜀国，借产权变更重置控制者。这会不会丢失整合状态、建筑归属，要实测。若不可行，退路是只刷 20 营步兵、不翻转，由部队自行收复。
- 20 营步兵用 `create_military_formation`（GAME 与 effects.log 均有实例）。

## 7. 文件

新建
- `events/nesnd_sih_jingnan.txt`：.1 执政选择，.2 是否投降，.3 投降后人物下落，.4 借兵自立，.10 属国去留，.20 统一南方完成。
- `common/static_modifiers/nesnd_sih_jingnan.txt`：两个战时修正，以及 `nesnd_south_unified`。
- `common/scripted_effects/nesnd_sih_jingnan.txt`：选定后的共有效果（翻转、刷兵、保护期），投降结算，人物下落。
- `common/journal_entries/nesnd_unify_south.txt`。
- `common/scripted_triggers/nesnd_unify_south.txt`：26 州判定、适用范围、僵局判定。
- `common/script_values/nesnd_unify_south.txt`、`common/scripted_progress_bars/nesnd_unify_south.txt`。
- `common/decisions/nesnd_restore_ming.txt`。
- 中英本地化 `nesnd_sih_jingnan_l_*.yml`（之后按 nesnd-player-writing 写）。

修改
- `common/journal_entries/nesnd_war_collapse.txt`：蜀军日志的周脉冲与结局清理。
- `common/scripted_effects/nesnd_south_restoration.txt`：改造 `nesnd_postwar_sih_great_han`，蜀国成立大明时的原统治者处理，各胜者开启统一南方。
- `events/usm_civilwar_events.txt`：.10 大汉选项拆为两项，.11 的权重与互相宣称，.4/.5 的蜀国暂停条件，.9 开启统一南方。
- `common/scripted_effects/nesnd_war_collapse.txt`：`nesnd_check_war_collapses` 对蜀国的暂停条件（或改在 .5 的 trigger 中）。
- `events/nesnd_celestial_collapse.txt`：.3 开启统一南方。决议复用 .3。
- `common/scripted_effects/nesnd_crisis_effects.txt`：招萧兴华。
- `common/character_templates/nesnd_asian_historical_leaders_overrides.txt`：萧兴华模板。
- `common/scripted_triggers/nesnd_story_character_protection.txt`：三人的保护与保护期。

## 8. 改造 `nesnd_postwar_sih_great_han` 的理由

保留它的名字和三处接口：国名读 `nesnd_postwar_great_han`（`ce_dynamic_country_names.txt:126`），宪制清理移除该变量（`nesnd_south_restoration.txt:129`），.10 调用它（`usm_civilwar_events.txt:1052`）。只加一个君主参数，并在吞并之后接属国去留和开启日志。

## 9. 顺带发现，本次不改

- `usm_civilwar.2.d*` 写“蜀藩魏鉴、萧虎力”，PPET 是“魏鉴、萧兴华”。
- PPET 淮藩人名前后不一（朱靖堙 / 朱仲进）。
- `flavorUSM.8`「川东整肃」的条件是成都、川南，不含川东。
- 蜀王是谁几处说法不一（刘忠明、朱慎徽、“朱深橞”）。本方案以刘忠明为蜀王。
- `nesnd_postwar_sih_great_han` 对同一统治者重复 `set_character_as_ruler`。
- `usm_civilwar.10` 有四个选项同时写 `default_option = yes`。
