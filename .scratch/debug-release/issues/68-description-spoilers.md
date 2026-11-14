Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: WORK/backups/spoiler-fix-20261107/（改前四个文件）

# 68 日志与按钮描述的结局剧透

## 现象与期望

“GPT 写的本地化里，有日志描述提前透露结局。”日志描述（_reason 等）、按钮描述（_desc）只写当下的处境、各方的立场和玩家面对的选择；结局只在结局事件、结局文字或按下按钮之后的事件里出现。「幕府危局」已在任务67改过，本任务跳过。

## 原因

扫描 nesnd_ 中文本地化中 661 条日志 `_reason`／`_status`／status_desc 与按钮 `_desc`，对照脚本确认三条明确剧透：

- `nesnd_cne_republic_journal_reason`、`nesnd_cne_republic_status`：写出胜利后吞并帝国、重建大汉共和邦、取得湖广四川声索，失败后领土归入帝国（common/scripted_effects/nesnd_cne_republic.txt:131–140）。
- `nesnd_usm_western_provinces_reason`：末句预告失败效果，即荆楚、西南、客家、粤人口激进化（common/scripted_effects/nesnd_usm_western_provinces.txt:24–27）。

## 改了什么

- `localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`：共和日志正文第二段改写为当下处境；状态行只留胜负条件。
- `localization/english/replace/nesnd_cne_land_reform_l_english.yml`：同上对应英文。
- `localization/simp_chinese/replace/nesnd_per_usm_mechanics_l_simp_chinese.yml`：西部置省正文删去失败后果一句，保留1850年期限。
- `localization/english/replace/nesnd_per_usm_mechanics_l_english.yml`：同上对应英文。

第二轮（作者确认拿不准的四条也改）：

- `nesnd_japan_l_*`：`nesnd_wu_eastern_question_reason` 末句改为“远洋驻军与海上商路，都押在这次东征上”，不再写成分封已成。
- `nesnd_hus_social_hierarchy_l_*`：`nesnd_hus_register_native_desc` 删去满蒙外迁一句（按钮提示 `_tt` 未动，仍写外迁）。
- `nesnd_acw_slavery_question_l_*`：`nesnd_hus_west_lever_reason` 两处改为假设语气（“联邦一旦分裂”“若是华盛顿自顾不暇”）。
- `nesnd_chen_security_l_*`：`nesnd_protect_chen_button_desc` 删去刺杀死亡／负伤／脱险概率一句。

动态代码、数字、颜色与改前一致；各文件保持 UTF-8 BOM、CRLF 与语言头。第二轮备份在 WORK/backups/spoiler-fix-20261107/round2/。

## 怎么复测

共和军起兵后看「共和军」日志正文与状态行；悬停完成／失败结局，确认吞并、改称与声索仍在结局提示中显示。吴朝取得西部后看西部置省日志正文；悬停失败结局确认激进化提示仍在。

## 遗留问题

- 未启动游戏。状态行删去结局效果后，玩家要靠原生结局提示看到这些效果，是否显示未经实机验证。
- 陈东阳刺杀的 40／25／35 概率现在不再出现在任何中英文本地化里；脚本数值未改。若要让玩家看到，需另放在结局后可见的位置。
- 另见交付说明：故事字段中的规则（流散、意大利、港路、丹那沙林、日本求援按钮）、9条“旧议程已经结束”开发者口吻、`nesnd_cne_land_journal_reason` 平衡腔。
