# 12 复燕、海外、君主主义阴谋文本校订

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-11）
Blocked by: none
Validation: STATIC_PASS
Evidence: 改动前备份 `nesnd-workbench/backups/pre-change-denglai-prose-proofread-20261111T032015Z`

## 1. 现象与期望

作者：去除“结案”“交付”等八股用词、预设剧情、不合身份的口吻；用国名函数代替“北朝”；1836 年的人带着种族偏见、惯于政治暴力。参照作者对复燕文本的批注与 GPT 的《登莱共和国（SHA）文本对照》。

## 2. 原因

Codex 稿替机制编理由、替玩家预设事实（谁战死、只有一艘船）、把军政场面写成乡村或现代社区口吻。

## 3. 改了什么

- 范围：`nesnd_sha_restore_yan`、`nesnd_sha_overseas`、`nesnd_sha_conspiracy` 中英本地化里的 Codex 稿。对照表标为“作者手改”的中文条目（复燕之路正文至 `nesnd_sha_yan.2.*`）不动，只在合写的 `yan.1.d`、`ready_status` 里把“北朝”换成国名函数。
- 复燕 33 条、海外 22 条、阴谋 7 条，中英同步。新增 `nesnd_sha_yan_at_war_korea`（朝鲜密约 AI 评分专用，那里没有日志上下文）。
- 脚本：`journal_entries/nesnd_sha_restore_yan.txt` 在开启与每周存 `nesnd_sha_yan_north = c:CNE` 供文字取国名；`diplomatic_actions/nesnd_sha_restore_yan.txt` 改用新键；`events/nesnd_sha_restore_yan.txt` 的 `.4`、`.8` 补存北方政府作用域。
- 写作技能新增 `references/no-invention.md`，`SKILL.md` 加一行指引，仓库副本已同步。

## 4. 怎么复测

看「燕旗」悬停三行、复燕筹备状态行里的国名；触发 `nesnd_sha_yan.3`–`.8`、`nesnd_sha_overseas.1`–`.5`、`nesnd_sha_plot.1`–`.3` 看正文与国名。

## 5. 遗留问题

- 已按作者决定把国家 `YAN` 的国名与形容词改为“大燕”（英文 Great Yan），`nesnd_sha_annex_yan` 改为“吞并大燕”。改前备份 `backups/pre-change-yan-rename-20261111T102844Z`。作者正文里作史称的“东燕”保留。
- 作者改定的复燕正文仍用“北朝”“东燕”，未改。
- 作者 2026-11-11 指出起事只划四州有误：第二版方案为避开北朝共和军的东北起事地，把辽东、吉林排除在外，作者未曾同意。现改为东北六州：外东北、黑龙江北、松江、黑龙江四州仍是起事条件，辽东、吉林在北朝手中时起事一并划给燕国（`scripted_triggers`、`scripted_effects`、`script_values` 的复燕文件；平均动荡改按实际州数）。燕旗筹备状态行与招徕流民说明补上两州。改前备份 `backups/pre-change-yan-six-states-20261111T103223Z`。燕国占辽东、吉林后，北朝共和军的东北起事地在北朝境内已不存在，原脚本会改从西路或华北起事。
