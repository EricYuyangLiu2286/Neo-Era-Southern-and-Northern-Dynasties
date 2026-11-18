# 111 东征日本：吴方「重组日本诸藩」开战后作废，议和只剩日本的羞辱

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-18）
Blocked by: none
Validation: STATIC_PASS
Evidence: 报告 `nesnd-workbench/reports/2026-11-18-japan-wargoal/`（static_lints.json，toolkit/）；部署 `e23ee2c181e8db5b442dd5e0bd7e0c5a`

## 1. 现象与期望

1844 年存档：东征日本打了半年，议和界面吴方没有目标，只剩日本的“羞辱大吴”。1839.4.1 存档出现过同样的问题，当时只修了靖难入口。作者原话：“不要加太多有效条件！直接加上就能用就行了。”兑现时“按照对象拥有的地区逐个触发的 if……两个分封不要写在一起，不然很容易卡掉”。

## 2. 原因

`wg_nesnd_japan_reorganization` 的 `valid` 调用 `nesnd_eastern_reorganization_valid`。走原有东征入口时，这个 trigger 要求全套分封条件（`nesnd_japan_partition_possible`：三家君主、四州全有、群岛各州不得被吴以外的势力控制……）、dossier 未关、`nesnd_eastern_target_valid` 在整场战争中一直成立。战争中只要有一项不成立，引擎就会作废这个目标，而且作废后不会恢复。存档里这个目标是 `initial_war_goal=yes`、`status=discarded`。兑现时也是先整体判断分封条件，任一项不满足就整块不分。

## 3. 改了什么

- `common/war_goal_types/nesnd_japan.txt`：`valid` 只剩两条：持有方是吴，目标是仍然存活的日本，两个入口共用。`on_enforced` 改为按地区逐个判断：
  - 日本有京都的州且和国不存在，就建和国；
  - 日本有关东的州且扶国不存在，就建扶国；
  - 九州、四国日本拥有的州归吴；
  - 至少建成了一国，才把丰臣留在中国地方（要求日本有中国的州），再立保护国并收尾（全局分封标记、宣称、通知事件）。
  - 某一国没建成，不影响其他几项。现任君主只会送进这次新建的朝廷。
- `common/scripted_effects/nesnd_japan.txt`：`nesnd_partition_japan` 按领地拆成 9 段（准备、建扶国、建和国、给扶国、给和国、给吴、丰臣、保护国、收尾）。原效果仍按原顺序、原条件整体调用这几段；递表臣服、封授属国、吞并后恢复、待分封 on_action、事件 nesnd_japan.1 这五个入口的行为不变。保护国与收尾里的 `c:JTK`、`c:JIM` 改为 `?=`。
- `common/scripted_triggers/nesnd_japan.txt`：删除 `nesnd_eastern_reorganization_valid`。调用处只有这个战争目标的 valid 和 on_enforced，按钮、日志、on_actions 都不读它（v3tree 已确认）。
- `common/scripted_effects/nesnd_crisis_effects.txt`、`common/diplomatic_plays/nesnd_japan.txt`：变量 `nesnd_jingnan_japan_forced` 已没有读取方，写入和清除都去掉了。
- 中英 `nesnd_ui_conditions_l_*.yml`：删除无人引用的 `nesnd_ui_jingnan_japan_forced_tt`。
- 没有加第二个吴方目标，博弈类型其他设置、日本的羞辱目标都没改。

## 4. 怎么复测

作者这局已作废的目标不会恢复，必须重新开战才能测。新开局，或用还没开东征的存档：

1. 原有入口：走东征日本按钮或国书开战。打仗期间让盟友占领日本的州，或换掉日本君主，确认议和界面里吴方的「重组日本诸藩」一直在。
2. 靖难入口：在靖难中让日本被拉进战争（`nesnd_open_japan_jingnan_war`），同样确认目标一直在。
3. 吴胜后看结果：
   - 日本有京都就出现和国，有关东就出现扶国，两者互不影响；
   - 日本有中国地方就留丰臣，九州、四国归吴；
   - 若日本京都、关东都已丢掉，就不建国、不立保护国，只划九州、四国。

### 2026-11-18 作者复测：新开战仍无吴方目标

作者 11:31 启动游戏（部署 `bc10c7d8`，valid 已改宽，尚未拆分封），1839.7.10 开战，3 周后议和界面仍只有日本的羞辱。最新自动存档是 1839.7.1，早于开战，读不到这场战争。1844 存档里作废的目标记着 `other=18`：引擎把日本本身当成“要新建的国家”。推断：`settings` 里的 `country_creation` 让引擎在代码层面检查“新建国家”，而日本已经存在，所以检查不通过，不管脚本 valid 写什么，目标一开战就被作废（1839.4 存档也是“一开战就作废”）。本 MOD 只有这一个战争目标拿 `country_creation` 去对准一个已存在的国家；原版用这个设置的 liberate_country，目标是还不存在的国家。

改动：`settings` 只留 `require_target_be_part_of_war`，去掉 `country_creation`、`validate_conflicts_war_goals_all`、`conflicts_with_country_creation`、`conflicts_with_annex_country`。新国家由 on_enforced 建，不靠引擎。部署 `ab24288d`。推断，未实机验证。

## 5. 遗留问题

- 未实机验证：`create_country` 在 on_enforced 里刚建出国家后，同一效果能否立即用 `c:JIM`、`c:JTK`。原效果本来就是这样写的，推断可以。
- 只建成一国时，通知事件 nesnd_japan.3「东洋四府」的正文仍按三家分立来写；按要求没有为部分分封新写文字。
- 日本当时的君主属于没建成的那一家（例如德川君主而关东已失），这位君主就留在日本，丰臣仍会被设为残余政权标记。
- 2026-11-18 作者追加：`nesnd_japan_recovery.txt` 清除 `nesnd_ming_court_player_intent`、`nesnd_ming_court_waiting_flight` 两行已删去。这两个变量自 `67f1826` 起从未被设置，删除不改变行为。部署 `1b63cb63`。
