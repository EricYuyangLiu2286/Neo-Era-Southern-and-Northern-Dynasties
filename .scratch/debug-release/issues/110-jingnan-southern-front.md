# 110 靖难战争南线：吴军经缅甸、老挝北上，西府军事件不按东西顺序触发

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed（B、A 均已实施，A 的入口由作者选定，其余按方案默认值）
Assignee: Claude（2026-11-16）
Blocked by: none
Validation: STATIC_PASS
Evidence: [工作台报告目录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-16-xifu-southern-front>)（A 方案 `A-design.md`、Toolkit、tiger）· 内容树 `V3-content-tree/output/cases/xifu_resistance_fall/` · 部署 B `b5273335`，A `bbab5753`

## 1. 现象与期望

观察者局多次：吴朝不以东线为主攻方向，而借附属国参战，从缅甸、老挝方向北上，西府军抵抗与灭亡系列事件不按由东向西的设计触发。期望吴军以东线为主，云南亚热带山地雨林不成为几十万大军的主攻方向。

## 2. 原因

- 西府军事件只看各国自己的占领与首都，不看方向。蜀国「成都的去从」由 `nesnd_sih_regime_due`（`common/scripted_triggers/nesnd_sih_jingnan.txt:12`）触发：蜀国任一州被敌控制、被占 25%，或楚、淮首都已失（全局 `nesnd_jingnan_rebel_fell`，`events/usm_civilwar_events.txt:616`）。设计上第三条在前，南线进攻时第一条先成立。亡国判定 `nesnd_south_capital_defeat`（`common/scripted_triggers/nesnd_war_collapse.txt:2`）同样只看首都控制或占领 80%。
- 云南、贵州属蜀国（`common/history/states/00_states.txt`）。缅甸、琅勃拉邦、清迈、占巴塞、柬埔寨、大越开局是吴的 dominion（`common/history/diplomacy/ce_subject_relationships.txt:30-60`），本 MOD 的 dominion 写 `join_overlord_wars = yes`（`common/subject_types/ce_subject_types.txt:72`），自动随吴参战。暹罗是 tributary（`= no`）。东京（`STATE_TONKIN`）是吴的直辖州，按原版地图与云南、广西相邻（未在本 MOD 地图上逐省核对）。
- 南线战争目标是反吴盟主（蜀国优先，`common/scripted_effects/nesnd_crisis_effects.txt:189`），AI 可能因此直取成都。此点未实机验证。

## 3. 改了什么（B）

- 新增 `common/battle_conditions/nesnd_battle_conditions.txt`：战斗条件「瘴疠山路」。吴方在靖难战争中进攻云南、贵州、川南、广西四州的山地、险地、森林地块时出现，权重 20（原版进攻方条件约 0.5–3）。进攻 −25%，士气损失 +25%，伤亡 +20%，量级参照原版「迷路」。只在吴方参加 `dp_usm_civil_war` 时成立，内战结束即不再出现，不加州修正。桂林不列入（湖广入广西的东线）。
- `localization/simp_chinese/replace/nesnd_war_collapse_l_simp_chinese.yml`、`localization/english/replace/nesnd_war_collapse_l_english.yml`：条件名与说明各两键。

- A（作者 2026-11-16 选日志按钮入口，其余按 `A-design.md` 的默认值）：
  - 新增 `common/scripted_buttons/nesnd_indochina_envoys.txt`：「南朝诸国」日志按钮「遣使南疆」，拥明国家开战前可用，冷却 6 个月，加 12 个月修正「南疆使团」（官僚 −10，`common/static_modifiers/nesnd_indochina_envoys.txt`）。AI 只有蜀、楚、淮和明廷会按，1837 年起权重 50。
  - 新增 `common/scripted_triggers/`、`common/scripted_effects/nesnd_indochina_envoys.txt`：按缅甸、大越、琅勃拉邦、占巴塞、清迈、柬埔寨顺序遣使，每国最多两轮。1838-06-01 起未接洽的国家自行收到「风闻南朝将乱」（接受基础 40）。
  - 新增 `events/nesnd_indochina_envoys.txt`：.1 附属国答复（静观其变改为 tributary，与吴 −25、与遣使国 +25，拒绝则反之），.2 回报遣使国，.3 通知吴，.10 吴胜后逐国清算（恢复出兵 60、兴师问罪 25、既往不咎 15）。
  - 改 `common/journal_entries/nesnd_succession_board.txt`（加按钮、每周检查保底事件）、`events/usm_civilwar_events.txt`（「大吴帝国的黎明」后开始清算）。
  - 本地化 `nesnd_indochina_envoys_l_{simp_chinese,english}.yml` 各 31 键。

## 4. 怎么复测

新开局，观察者五速跑到靖难战争（1838–1839）。A：拥明国家「南朝诸国」日志里出现「遣使南疆」，各附属国答复与吴、遣使国的回报事件，开战时观望国不随吴参战，吴胜后的「南疆清算」。B：吴军主攻是否仍在南线；西府诸国被占和亡国顺序（襄阳、广西先于成都，「成都的去从」在楚或淮亡后出现）；滇黔、川南、广西山地战斗中吴方是否带「瘴疠山路」，平原与桂林、东线战斗不应出现；内战结束后同一地区的战斗不再出现。

## 5. 遗留问题

- A 的成本、关系数值、报复权重、保底事件等 8 项用的是方案默认值，作者可改。战争中途改附属类型的后果未核实，答复事件在开战时取消。
- A 与 B 同时生效可能让吴明显变弱，复测时一并观察。
- 战斗条件不改变 AI 的兵力部署，只让南线进攻更难推进。AI 选前线由引擎决定，无法用脚本控制。
- 开局 00 与 ce 两份外交历史给同一批国家定了不同宗主（暹罗附属清迈、占巴塞、琅勃拉邦，大越附属柬埔寨），实际归属须开局核实。未改。
