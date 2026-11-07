# 69 教士秀全的旅途（全局人物日志）

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [报告目录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-xiuquan-saint/>)（tiger.json、files.json、保护条件改前备份）· [作图说明](69-xiuquan-art-brief.md)

## 现象与期望
作者：洪秀全是吴明战争期间的天主教传教士，救治伤者。全局日志记录他与追随者逐州行走：所在州荒废度恢复加快、人口增长；传教条满后0.1%人口改信随机一种基督教（体现误判，东方正统教会即景教）；所在国可驱逐；他去世后日志失效，玩家收到「追认圣徒」。开局即有，起点高凉，生于1814年，无意外活到80岁；可见范围为所在国、其邻国和玩家。

## 原因
新内容。依据：原版全局日志 `02_peru_bolivia.txt`、本项目 `nesnd_kr_restoration.txt`；人物像仿 `gui/journal_entry_widgets/tsarpoints_widgets.gui`；无原型角色仿 `common/character_roles/02_unique_roles.txt`；人物保护沿用靖难任务的 `nesnd_story_character_protected`（工作台 `reports/2026-11-07-jingnan-japan-155023/人物保护起止表.md` 已为他预留）。

## 改了什么
- 新增 `common/history/global/nesnd_xiuquan.txt`：开局在明（USM）生成人物，置于高凉，开日志。
- 新增 `common/journal_entries/nesnd_xiuquan.txt`：全局日志；每周对账（州失效补位、人物转籍、参与国）；每月满条皈依、25%换州、1894.1.1去世；唯一结局为去世后隐藏失效。
- 新增 `scripted_buttons/`、`scripted_progress_bars/`、`scripted_effects/`、`scripted_triggers/`、`static_modifiers/`、`on_actions/` 下各一个 `nesnd_xiuquan.txt`：驱逐按钮、传教条（每月+20，交战+10）、到达效果、所在国判定、「秀全的药箱」（荒废度恢复+200%、死亡率−2%≈年增长+0.1个百分点）、去世向玩家发事件。
- 新增 `common/character_roles/nesnd_xiuquan_roles.txt`（传教士，无任期、不当利益集团领袖）、`common/character_templates/nesnd_xiuquan.txt`、`common/dna_data/nesnd_hong_xiuquan.txt`（自定数值）。
- 新增 `events/nesnd_xiuquan.txt`（追认圣徒，占位视频）、`gui/journal_entry_widgets/nesnd_xiuquan.gui`（人物像）、中英本地化各一份（28键）。
- 修改 `common/scripted_triggers/nesnd_story_character_protection.txt`：加一条，日志有效期间保护洪秀全。
- 工作台新增 `tools/install_xiuquan_event_image.py`：事件图交稿后转DDS并接入。

## 怎么复测
1. 新开局（1836）。任何国家都能在日志「国际局势」里看到「教士秀全的旅途」；顶部是人物像，状态行写他在哪个州。
2. 选明（USM）：日志置顶，有「驱逐秀全」按钮。高凉州面板应有「秀全的药箱」。
3. 驱逐：点一次，成功则他到与明接壤的外国州（状态行写「刚被逐出」）；失败则高凉激进上升。按钮冷却1个月。
4. 传教条约5个月满（明交战时约4个月），状态行显示新信徒的教派。
5. 去世：控制台 `effect random_character = { limit = { has_template = nesnd_xiuquan_template } kill_character = yes }`，应弹「追认圣徒」，日志随后消失，所在州修正被移除。

## 遗留问题
- 未实机验证：GUI里 `GetGlobalVariable(...).GetCharacter` 人物像能否显示；`random_neighbouring_state` 是否含跨海相邻；无原型角色人物的转籍。
- tiger 1.19 对 `progress_condition`、`outcome`、`activation_description`、角色 `character_background`/`can_be_interest_group_leader` 报未知字段，均为1.15新字段（GAME文档有），判为规则滞后。
- 事件图为占位，作图规格与提示词见作图说明。
