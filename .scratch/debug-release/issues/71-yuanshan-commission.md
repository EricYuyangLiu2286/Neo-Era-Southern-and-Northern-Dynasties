# 71 放宽远山宣慰司成立门槛

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [Tiger 前后对比与静态检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-yuanshan-commission/>)；改前备份 `nesnd-workbench/backups/pre-change-yuanshan-commission-20261107T173510Z`

## 1. 现象与期望

作者：远山宣慰司（YU1）门槛同改前的天竺一样过严，参照任务54放宽。代理在任务54审查时标出，未实机观察。
作者确认：4个南非地区（只算直辖）、只保留“民主”、去掉港口与政府行政建筑、首府可替换、自治领＋划归决议。

## 2. 原因

远山不在作者原作（tag `original-20261030`）中，由任务25（`a062441`）新建、任务26（`adfc317`）收紧。改前须同时满足：

- `scripted_triggers/nesnd_commission_expansion.txt:24`：日志要“开化使命”（第3时代）才显示，即使已在南非有地。
- `scripted_triggers/nesnd_commissions.txt:15`：“民主”＋“开化使命”；4个南非地区里最大的州归本国或附属国，打下小州不算；祖鲁兰有港口；某南非州有政府行政建筑。
- `scripted_effects/nesnd_commissions.txt:230`：种子州写死为祖鲁兰，不持有祖鲁兰无法建司。
- 开局 USM 在南非一个州也没有，六个地区分属 SAF、NAM、XHO、TSW、ZUL、BST、ORA、PHL、MTB、PDI、TRN。

## 3. 改了什么

- `scripted_triggers/nesnd_commissions.txt`：新门槛为“民主”、直辖有人口的州分布在≥4个南非地区、非附属国、不在战争或外交博弈中、一年冷却。
- `scripted_triggers/nesnd_commission_expansion.txt`：日志改为在南非直辖一个有人口的州即显示；删去只供旧门槛用的三个判断。
- `scripted_effects/nesnd_commissions.txt`：建司改为自治领，首府祖鲁兰（不持有则取人口最多的南非州），加原版 `colonial_administration` 修正；新增划拨效果 `nesnd_yuanshan_transfer_states`。
- `decisions/nesnd_commissions.txt`：旧的重复建司决议换成「将新得的远山土地划归宣慰司」。
- `scripted_buttons/nesnd_commissions.txt`：设立按钮用新门槛；AI 权重 5→100，同天竺，达标即建。
- 本地化中英 `nesnd_india_l_*.yml`：改写地区提示与设立提示（傀儡→自治领，列出六个地区），新增划归决议3键。作者改稿的其他键未动。
- 作者追加（日志可读性，同天竺写法）：`journal_entries/nesnd_commissions.txt` 完成条件改为“远山宣慰司已经设立。”（原来显示原版通用的“拥有该变量”）；加状态行（地区不足／地区已足但缺其他条件／已可设立）和进度条「远山直辖地区 X / 4」。新文件 `script_values/nesnd_commissions.txt`、`scripted_progress_bars/nesnd_commissions.txt`，每周按实数同步。中英各加7键。未加成立事件与修正。

## 4. 怎么复测

新开局，玩 USM。南非各国：SAF 持开普殖民地、东开普、北开普；ZUL 持祖鲁兰；ORA 持自由邦。

1. 控制台 `annex SAF`。下一个月初日志出现「筹建远山宣慰司」：进度条 3 / 4（一周内同步），状态行“尚不足以单设宣慰司”，按钮灰色；悬停看“民主”和地区两条未满足。日志的完成条件应写“远山宣慰司已经设立。”
2. `annex ZUL`：进度条 4 / 4，状态行变为“已足，还缺其他条件”。再 `research democracy`（若无此命令，打开 debug 模式后用 `effect add_technology_researched = democracy`）：状态行“已可设立”，按钮变亮，不在战争中点击。
3. 地图上出现自治领「远山宣慰司」，首府祖鲁兰，原 SAF 三州一并划入；USM 日志完成，YU1 获得「远山的庶务」。外交面板关系应为自治领。
4. `annex ORA`，决议页出现「将新得的远山土地划归宣慰司」，执行后自由邦归宣慰司。
5. 可另开一局只 `annex SAF` 再 `annex BST`（祖鲁兰的另一个州），首府应落在人口最多的州（开普殖民地）。

## 5. 遗留问题

- 未实机验证：自治领能否建立、首府不在祖鲁兰时的表现、进度条与状态行显示、控制台科技命令名。
- 远山没有天竺那样的成立事件和「开府」修正（只是奖励，不影响玩家理解日志）；本次未加。
- 工作台任务26的测试脚本（`tools/test_commission_boundaries.py` 等）是针对旧门槛的一次性模拟，无流程调用；作者同意不更新。
- 检查期间另一代理正在改主 MOD 的法国宫廷文件；Tiger 对比中 `events/nesnd_france_court.txt` 新增8个缺失本地化报告，来自那边的未完成工作，与本任务无关。
