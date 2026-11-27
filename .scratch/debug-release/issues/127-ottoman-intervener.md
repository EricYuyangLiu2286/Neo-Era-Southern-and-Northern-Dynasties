Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-26，奥斯曼 F3 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt` 与 `_agy_checks/tree_diff.md`

# 127 奥斯曼 F3：干涉者与欧洲协调从局面选

## 1. 现象与期望

F2 完成北方战争通用化后，奥斯曼线中仍残留三处写死国名的「奥斯曼面对的压力 / 欧洲协调」逻辑：
1. 鲁米利亚与东方诸省的镇压与东方宪章只认俄国（`c:RUS`），东方镇压另写死英国（`c:GBR`），事件 `.18` 的触发器也写死 `c:RUS ?= this`；
2. 鲁米利亚失地宣称效果 `nesnd_ottoman_rumelia_claim_lost_states` 仍使用一层 `is_subject_of = root`，未统一为 F1 的最上层宗主判定 `nesnd_ottoman_state_outside_ottoman_hands`；
3. 「伊斯兰领袖」结局事件 `.12` 选项 b（「以欧洲列强的身份立身」）写死英国（`c:GBR`）与法国（`c:FRA`）。

本批（F3）按规则 R2、R11 把上述写死国名改为按局面动态评分挑选，历史国家仅在脚本值分数中保留加权（R11 a 类），并同步去写死相关中英本地化文本；同时完成原版切尔克斯人驱逐链的只读调研（本批不接线）。

## 2. 改了什么

- **共用触发器、脚本值与挑选效果**（`common/scripted_triggers/nesnd_ottoman_common.txt`、新建 `common/script_values/nesnd_ottoman_common.txt`、`common/scripted_effects/nesnd_ottoman_common.txt`）：
  - 新增干涉者基础前提 `nesnd_ottoman_intervener_base`、巴尔干候选 `nesnd_ottoman_balkan_intervener_candidate`、东方候选 `nesnd_ottoman_east_intervener_candidate` 与欧洲协调候选 `nesnd_ottoman_concert_candidate`。
  - 新增评分脚本值 `nesnd_ottoman_intervener_score`（`c:RUS` +40、`c:AUS` +30，关系、宿敌与列强加分）与 `nesnd_ottoman_concert_score`（对奥关系值，`c:GBR`/`c:FRA` 各 +15）。
  - 新增挑选效果 `nesnd_ottoman_pick_balkan_intervener`、`nesnd_ottoman_pick_east_intervener`、`nesnd_ottoman_pick_east_intervener_second`（`position = 1` 取东方第二名）与 `nesnd_ottoman_pick_concert_partners`（`position = 0` / `position = 1` 取欧洲协调前两名）。
- **鲁米利亚与东方诸省**（`common/scripted_buttons/nesnd_ottoman_rumelia.txt`、`common/scripted_buttons/nesnd_ottoman_eastern_provinces.txt`、`common/journal_entries/nesnd_ottoman_rumelia.txt`、`common/scripted_triggers/nesnd_ottoman_rumelia.txt`、`common/scripted_effects/nesnd_ottoman_rumelia.txt`）：
  - 鲁米利亚与东方镇压按钮开头调用对应挑选效果，原生显示对 `scope:nesnd_intervener`（东方另含 `scope:nesnd_intervener_second`）的关系下降；第 2 次镇压后预告改为查此刻存在候选；第 3 次镇压仅在 `exists = scope:nesnd_intervener` 时设 `…_rus_warned` 并发事件 `.18`，无候选时留待下次镇压再检。
  - 东方宪章按钮（+15）与东方诸省宪章结局（+25）改调 `nesnd_ottoman_pick_east_intervener` 后对 `scope:nesnd_intervener` 改善关系。
  - `nesnd_ottoman_rumelia_claim_lost_states` 改用 F1 的 `nesnd_ottoman_state_outside_ottoman_hands = yes`，覆盖多层附属。
  - 保留 `_rus_` 标识符并在注释中写明现指被选中的干涉者。
- **事件 `.12` 选项 b 与 `.18`**（`events/nesnd_ottoman_recovery.txt`）：
  - `.12` 选项 b 改调 `nesnd_ottoman_pick_concert_partners`，对前两名各 +40 关系，并从第一名起为第一个满足 `nesnd_crimea_can_sign_defensive_pact_with` 者签防御条约。
  - `.18` 触发器去掉 `c:RUS ?= this`，改为 `is_subject = no`、`exists = c:TUR`、`c:TUR = { is_country_alive = yes }`，更新注释说明现行发送方式。
- **中英本地化**（`localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`）：
  - 更新两次镇压预告、`.18` 全套文案、博弈名「近东干涉」、修正名「近东抗议的声望」、`.12.d`（去伦敦与巴黎、改平叙）、以及鲁米利亚/东方诸省与伊斯兰领袖结局提示中残余的俄/英/法写死表述，中英键集合保持一致。

## 3. 怎么复测

1. 在巴尔干与近东/高加索不同列强格局下点击鲁米利亚与东方镇压按钮，核对按钮提示原生显示被选中的干涉国（东方镇压另显示第二名），第 2 次后无候选时不显示预告，第 3 次有候选时向该国延迟 3 天发事件 `.18`，无候选时不设已警告标记、待第 4 次出现候选后再发。
2. 扮演被选中的非俄、非基督教列强（如大明联邦或西秦）测试收到 `.18` 时的标题、正文、出处与两个选项，确认无俄国或宗教保护表述；测试 3 天延迟内沦为附属或奥斯曼被吞并时事件被拦截或安全降级。
3. 在「伊斯兰领袖」结局事件 `.12` 选 b，核对按对奥关系加英法 +15 选出前两名各 +40 并按序尝试签防御条约，且当前 `global_var:nesnd_north_foe` 被排除在候选之外。
4. 在鲁米利亚失控结局中验证奥斯曼附属的附属所持巴尔干州不会被误判为失地并加宣称。

## 4. 遗留问题

- 原版切尔克斯人驱逐链已完成调研（见 `_agy_checks/调研.md` 第 5 节），依规则第 16 条本批不接线。
- `common/static_modifiers/nesnd_ottoman_rumelia.txt` 不在本批允许修改的文件列表内，`nesnd_ottoman_rus_protest_prestige` 的注释补充于调用处 `events/nesnd_ottoman_recovery.txt`。
