# 16 远北：俄属边地任何民族的起事都推进剧情

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS（1.15.1，pdx.py 解析，Toolkit 7 个文件零诊断，1 条为 CK3 规则误报，见下）
Evidence: [1878 自动存档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-error-flood/save-button/>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-sha-borderland-risings-20261112T211740Z>)

## 现象与期望
作者问登莱援助后俄国境内的辽东人、蒙古人起事有没有爆发过。1878 年自动存档里，远北日志在 1848-02-10 期满结束，伊尔库茨克（1865）和上叶尼塞斯克（1872）后来都由西秦从俄国取得。起事是否发生过，存档已无记录可查。原脚本只认主体民族为辽东人的起事国，蒙古人、布里亚特人等起事不会推进剧情。作者要求：对应地区的任何起事都推进剧情。

## 改了什么
- common/scripted_triggers/nesnd_sha_far_north.txt：新增 `nesnd_sha_borderland_uprising`（起事国拥有伊尔库茨克或上叶尼塞斯克的州，或主体民族为辽东人）和 `nesnd_sha_borderland_movement`（俄国境内、在这两地有人口的非俄罗斯民族的少数民族运动）。
- common/on_actions/nesnd_sha_far_north.txt：分离开始、结束两个回调改用 `nesnd_sha_borderland_uprising`，运动解散回调改用 `nesnd_sha_borderland_movement`。
- common/script_values/nesnd_sha_far_north.txt：`nesnd_sha_liaodong_progress` 改为 `nesnd_sha_borderland_progress`，取两地各非俄罗斯民族在俄国的分离进度最高值。日志进度条（journal_entries:20）和“义勇军”按钮的 50% 门槛（scripted_buttons:44）随之改名。
- events/nesnd_sha_delay.txt：`nesnd_sha_delay.5` 只在俄国境内已没有其他边地民族运动时才撤回援助，避免一族运动解散就让还在发展的另一族前功尽弃。
- 本地化（中英，均为 Codex 稿，见文本对照第二节）：`nesnd_sha_far_north_bar_desc`、`nesnd_sha_relief_status`、`nesnd_sha_revolt_status`、`nesnd_sha_halfway_tt`、`nesnd_sha_north.1.d` 首句，把“辽东人”改为“俄属边地”或“边地起事者”。

## 检查
- pdx.py 解析 6 个脚本文件通过。
- Toolkit：7 个文件零诊断。on_actions 文件报 `wrong-on-action-folder`，这是 CK3 的规则（要求单数 `on_action/`），维多利亚 3 原版就在 `common/on_actions/`，属误报。

## 怎么复测
新开局玩登莱走远北路线，派出援助后观察进度条（现在跟踪边地各族中进度最高的一族）。任一民族在伊尔库茨克或上叶尼塞斯克起事，日志状态应变为“俄属边地已有人举兵起事”，起事国独立且占有伊尔库茨克时应出现谈归并的事件。

## 遗留问题
- 起事国在分离开始回调里是否已拥有边地州，未实机确认。拿不到州时只有辽东人起事仍能被识别（保底条件），其他民族的起事要到结束回调时才可能被记录。
- 同时有两场边地起事时，后开始的一场会覆盖先前记录的起事国。
- 进度条取的是民族在俄国全境的分离进度，例如蒙古人的运动若主要在别处，也会计入。
