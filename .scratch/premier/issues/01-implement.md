# 01 「统治者与内阁」：实施

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-15）
Blocked by: none
Validation: STATIC_PASS
Evidence: `nesnd-workbench/reports/2026-11-15-premier/`（gen_premier.py、xcheck.txt、static_lints.json、toolkit/、tiger/、before/ 为改前 MOD 文件夹副本 `9fe20a4e`）

## 1. 现象与期望

立宪君主国没有对应的常驻日志。新日志给不能任命宠臣的非共和帝国，框架同「宫廷力量」「执政者与派系」：三条进度条（首相人气、首相与各派、政潮），首相由角色互动任命，须是政府内某集团的领袖，按人气给立法速度与合法性。政府改组后首相集团不在政府中时，立即改由政府内最大集团的领袖出任。三个日志互斥。作者 2026-11-15 定：Q1 改 `nesnd_palace_shown` 一行；Q2 覆盖“非共和且不能任命宠臣”全部；Q3 自动补任；平衡为首相集团对最大在野集团，所有集团都在政府中时改为首相对其余各派；旧日志的对方模式不变。数值未改，按方案建议值实施。

## 2. 原因

新内容。互斥：`nesnd_premier_eligible`（`common/scripted_triggers/nesnd_premier.txt`）与 `nesnd_palace_eligible` 只差 `can_have_favorites`；显示条件 `nesnd_premier_shown` 与 `nesnd_palace_shown` 同样二分。按人气缩放用 `scaling_modifiers_while_active`，人气经人物链接 `popularity` 每月写入 `var:nesnd_premier_pop`。

## 3. 改了什么

- 改：`common/scripted_triggers/nesnd_power.txt` 的 `nesnd_palace_shown` 加 `can_have_favorites = yes`（只此一行）。
- 新增（WORK `gen_premier.py` 生成）：`journal_entries/nesnd_premier.txt`、`scripted_progress_bars/nesnd_premier.txt`、`script_values/nesnd_premier_generated.txt`、中英 `nesnd_premier_bars_l_*`。
- 新增（手写）：`scripted_triggers`、`scripted_effects`、`script_values`、`static_modifiers`、`scripted_buttons`、`character_interactions`、`on_actions`、`customizable_localization` 各一个 `nesnd_premier.txt`，`events/nesnd_premier.txt`（18 件），`gui/journal_entry_widgets/nesnd_premier.gui`，中英 `nesnd_premier_l_*`。
- 复用（只引用）：`nesnd_power_*` 的集团支持度、权威官僚、定时修正，`nesnd_power_character_removable`、`nesnd_power_story_excluded`、头像控件类型、诏令卡片插图。

## 4. 怎么复测

见交付说明（新开局或读档，`tag GBR`）。

## 5. 遗留问题

- 未实机：选举后组阁是否经过 `on_government_reformed`、`on_ig_resigned_government` 触发时集团是否已离开政府（每周刷新兜底）；人物修正改动后人气是否立即更新（条每月重写）；GUI 布局。
- 换首相后，按钮费用留在原首相身上，新首相不背负。
- 旧文件 `nesnd_power.txt:41` 的注释仍写“帝国以上等级的非共和国”，未改（只准改一行）。「宫廷力量」的失效说明 `nesnd_palace_end_rules` 未提到改由新日志接续，未改。

## Comments

- 2026-11-15 作者复测：按钮扣人气后人气条未刷新（人物面板 0，条仍为 10）。原因：`add_modifier` 后当场读 `popularity`，引擎下一结算日才重算。改为一天后由隐藏事件 `nesnd_premier.2` 重读并同步，每周刷新也重读。人气条按作者建议改为摇摆条（绿填红底、标记，同原版大博弈条）。已部署 `ad65c0dd`。
- 2026-11-15 作者第二次反馈：点击时按“现值 + 修正值”当场写入人气条（`nesnd_premier_predict_pop`），一天后的隐藏事件只作校正。联合组阁的平衡减项由三个集团改为四个集团起算。已部署 `b591b27f`。
- 2026-11-15 作者要求取消一天后的隐藏校正事件：已删除 `nesnd_premier.2` 及其调用，人气条只在点击当场按修正值写入，每周刷新与月脉冲读引擎实际人气。已部署 `7a6cbd09`。
- 2026-11-15 作者要求：卡片悬停的“费用”行改为一句描述（“此举会影响首相的人望。”），具体人气增减由效果列表显示。已部署 `ad3d7882`。
- 2026-11-15 作者要求改写修正名：「首相深孚众望」「首相不孚众望」，人气条右侧改为“不得人心 ← 0 → 深得人心”。已部署 `8eccdab9`。
- 2026-11-15 作者定：两个修正中文名统一为「首相的政治声望」，好坏由颜色区分。已部署 `f14191a8`。
- 2026-11-15 英文同步：两个修正改为 "Prime Minister's Political Standing"，人气条右侧改为 "Unpopular ← 0 → Highly popular"。已部署 `c3e2f208`。
