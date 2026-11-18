# 01 第二次靖难的域外介入：参战奖励、吴军军心条与统一南方八要点（实施）

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-16）
Blocked by: none
Validation: STATIC_PASS
Evidence: `nesnd-workbench/reports/2026-11-16-jingnan-intervention/`（toolkit/、tiger/）。改动前备份 `nesnd-workbench/backups/pre-change-jingnan-intervention-20261116T010905Z/`。部署版本 `dd61f45b`。

## 1. 现象与期望

按 [spec.md](../spec.md) 第二稿及第 6 节作者答复实施，作者 2026-11-16 批准：“宁国就是江西，照现在写，开始实施。另，条约港设定看原版学习一下。设计在浙江。”

- 中华帝国（`nesnd_crisis.20` c 项，原有）、西秦与华夏东洲（新）可以出兵反吴。
- 反吴方获胜时，胜者在「出兵各国的要求」中决定是否酬谢。吴胜时，介入国付五年赔款，吴得到中华帝国汉中、皖北的宣称。僵持时什么都不给。
- 吴「平叛」日志加「军心」条，按站在敌方的外国缩放吴军四项。
- 「统一南方」改为八处要地。

## 2. 原因

新内容。原来中华帝国参战时自己没有战争目标，战后只移除旗标（spec §0.3）。

## 3. 改了什么

新文件
- `common/scripted_triggers/nesnd_jingnan_aid.txt`：介入国、有资格得酬谢的国家、吴是否在靖难战争中、算入军心的外国。
- `common/script_values/nesnd_jingnan_aid.txt`：外国权重（中华帝国 2、其余 1，上限 4）、新近参战加成、两个修正的倍数。
- `common/scripted_progress_bars/nesnd_wu_resolve.txt`：军心 0–100，起点 30。每月 −1，本轮战争满 24 个月后 −1.5，每点外国 +1，参战头两个月每点另加 +7.5。只在吴处于靖难战争时变化。
- `common/static_modifiers/nesnd_jingnan_aid.txt`：「同仇敌忾」（满条：进攻 +15%、防御 +15%、士气损失 −20%、军用商品 −15%）与「军心涣散」（零条：−10%、−5%、+25%、+10%），每月按 |条值−50|/50 带 `multiplier` 重挂。
- `common/scripted_effects/nesnd_jingnan_aid.txt`：入战、清旗、军心刷新与清理、酬谢与拒绝、吴胜赔款。
- `events/nesnd_jingnan_aid.txt`：.1 出兵各国的要求（胜者，AI 70/30），.2 介入国得知答复，.3 吴廷索赔。
- 中英 `localization/*/replace/nesnd_jingnan_aid_l_*.yml`。

修改
- `events/nesnd_external_events.txt`：`nesnd_external.1` 为西秦、东洲加「出兵反吴」，条件与花费同中华帝国 c 项，AI 权重 5。
- `common/scripted_effects/nesnd_crisis_effects.txt`：开战时所有介入国入战（原只有中华帝国），入战记录对所有介入国生效。
- `common/on_actions/nesnd_crisis_on_actions.txt`：每月补入与战后清旗对两种旗标都生效。
- `common/scripted_effects/nesnd_south_settlement.txt`：结算前登记应得酬谢的介入国，结算后弹 .1，清旗改为全体介入国。
- `events/usm_civilwar_events.txt`：.8 吴胜时赔款与宣称，.9 僵持时清旗。
- `common/journal_entries/ce_usm_the_last_days_of_ming.txt`（作者原作「平叛」）：加军心条、月脉冲刷新、三个结局清理。
- 统一南方八要点：`nesnd_unify_south` 的触发器、脚本值、进度条（满值 8）、日志目标；`nesnd_restore_ming` 决议与触发器的门槛由“26 州中 8 州”改为“八要点中 7 处”（作者 2026-11-16 定）。中英 `nesnd_sih_jingnan_l_*.yml` 相应 8 键。

酬谢内容（胜者选 a）
| 介入国 | 得到 |
|---|---|
| 中华帝国，胜者非蜀（东路） | 苏北、滁州、合肥三州中胜者现有的部分；十年停战；地权革命完成度 +10 |
| 中华帝国，胜者为蜀（西路） | 胜者欠人情；投资权、贸易特权条约（约束期 10 年）；十年停战；完成度 +10 |
| 西秦 | 胜者欠人情；贸易特权、过境权条约（10 年） |
| 华夏东洲 | 条约港（`treaty_port` 条款，约束期 99 年），浙江不成依次改福建、闽江、粤中；贸易特权（10 年） |

条约港照原版写法（`events/iberia_events/dominican_events.txt:608`、`events/japan_events/ep2_meiji_restoration.txt:1657`）：`create_treaty` 加 `treaty_port` 条款，条款生效时由原版 `on_entry_into_force` 调用 `cede_treaty_port`（`common/treaty_articles/14_treaty_port.txt`）。浙江是单一州 `STATE_ZHEJIANG`（港口省份 `x301080`），合并后的地图中没有别的浙江州。所有条约先用 `can_create_treaty` 检查，同参数再 `create_treaty`。赔款按原版 `00_sepoy_mutiny_scripted_effects.txt:539` 的写法取 `fixed_income`，乘 0.10，约束期 5 年。

## 4. 怎么复测

1. 新开局选西秦或东洲。吴明易代后外交议程事件应有「出兵反吴」。选后开战时应站在反吴方，大吴「平叛」日志出现「军心」条。
2. 选大吴，分别在无人介入、只有中华帝国、中华帝国加西秦时看军心：起点 30，悬停读数与 spec §4.2 表格相符，四项修正随条值变化。
3. 反吴方胜：胜者收到「出兵各国的要求」。选 a 后看苏北、滁州、合肥归属，条约界面中的贸易特权、投资权、过境权，**东洲在浙江的条约港是否设立**，以及人情。选 b 看关系 −30。
4. 吴胜：介入国收到「吴廷索赔」，条约界面有赔款条约，吴对汉中、皖北有宣称。
5. 僵持（.9）：介入国什么都没有，之后不再每月补入。
6. 统一南方：条面 n/8，八要点齐时完成。重建大明决议的“八要点中 7 处”。

## 5. 遗留问题

- **未实机验证：** 脚本创建的条约是否受科技限制（条约港需 `colonization`，贸易特权需 `international_relations`）；不满足时 `can_create_treaty` 为假，该条款不生效，.2 会写“浙江的条约港没有设成”。约束期满后付款国可以撤回赔款条约（`binding_period` 不是自动到期，见技能 `lookup/native-treaty-aid.md`），AI 多半会撤。
- **浙江条约港的退路：** 原版 `state_valid_trigger` 表明浙江已是条约港、不是潜在条约港或胜者不再拥有浙江时都会失败。作者 2026-11-16 要求加退路：依次改试福建、闽江、粤中（`nesnd_jingnan_aid_try_port`），四处都不成时东洲只得贸易特权，.2 写明设在哪一州。
- `common/diplomatic_plays/ce_diplomatic_plays.txt` 的 `additional_involvement_trigger` 原计划加一行新旗标，改动被权限分类器拦下，未改。西秦、东洲已满足其中“非中华帝国且可发起侵略博弈”一支，入战走 `join_war`，不经过此处。
- 军心修正每月先移除再重挂，界面是否闪动待看。新近参战加成每国一局只给一次。
- Toolkit 只报 `wrong-on-action-folder`（CK3 规则，误报）。vic3-tiger 1.19 与 script_xcheck 不认 `progress_condition`（原版 1.15 `00_greece_progress_bars.txt` 在用）。cliche_check 命中东洲提示中的“九十九年……十年”，这是条约期限，保留。
