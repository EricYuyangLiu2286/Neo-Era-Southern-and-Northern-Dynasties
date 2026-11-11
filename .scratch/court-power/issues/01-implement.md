# 01 「宫廷力量」与「执政府与反对党」：实施

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-11）
Blocked by: none
Validation: STATIC_PASS
Evidence: `nesnd-workbench/reports/2026-11-11-court-power/`（audit.json、toolkit/、toolkit2/、生成脚本 gen_power.py 与 loc_power.py、art-prompt.md）；内容树索引 `V3-content-tree/output/index/`

## 1. 现象与期望

仿原版沙皇权威，做两个常驻菜单式日志，方案见 [spec.md](../spec.md)（第一步方案，下列答复覆盖其中的待定项）。作者 2026-11-11 答复：默认玩家有全部 DLC；法团国家等非共和政体凡能用宠臣都归「宫廷力量」；按钮仿诏令卡片，素材另出生图指令；共和国给“选票带来的合法性”；AI 不能轻易满权势，宫廷事件要频繁促使降权势，满权势带 +20% 税收浪费；空缺期权势流失，人物缺失时界面不能出错；做宠臣类型；西秦「伊犁的朝议」期间不显示本日志，并给朝议加类似按钮与宫廷事件条；明内战、法国（维持拿破仑王朝、宫廷与外省）期间排除，但在两国原有月度随机事件中加入新写的宫廷事件；极端事件死亡概率减半，结果可以是被推翻、被捕、流放。

## 2. 原因

新内容。前缀用 `nesnd_palace_`（宫廷力量）、`nesnd_cabinet_`（执政府与反对党）、`nesnd_power_`（共用），因为 `nesnd_court_` 已被法国「宫廷与外省」占用。数值以国家变量为唯一来源，进度条只做显示，月度增减与进度条明细由同一张表生成（skill journal-state §1）。

## 3. 改了什么

- 新增：`common/{journal_entries,scripted_buttons,scripted_triggers,scripted_effects,script_values,scripted_progress_bars,static_modifiers,customizable_localization}/nesnd_power*.txt`、`events/nesnd_palace.txt`、`events/nesnd_cabinet.txt`、`gui/journal_entry_widgets/nesnd_power.gui`、中英 `nesnd_power_l_*`、`nesnd_power_bars_l_*`。`journal_entries/nesnd_power.txt`、`script_values/nesnd_power_generated.txt`、`scripted_progress_bars/nesnd_power.txt`、`static_modifiers/nesnd_power.txt` 与两份 bars 本地化由 WORK 的 `gen_power.py` 生成，改数值改生成器。
- 西秦：新增 `*/nesnd_qe1_intrigue.txt`（朝争条、整肃朝堂、召开廷议、4 个事件）。改 `journal_entries/nesnd_qe1_court.txt`（挂条、按钮、月脉冲）、`script_values/nesnd_qe1_court.txt` 与 `scripted_progress_bars/nesnd_qe1_court.txt`（三方份额加“朝争中的一时偏向”一项）。
- 明：新增 `events/nesnd_usm_court.txt`、`scripted_effects/nesnd_power_story.txt`，`ce_usm_the_last_days_of_ming.txt` 的吴明论战月度随机事件加 3 件（各权重 5，调易代压力 ±2～4）。
- 法国：新增 `events/nesnd_fra_court.txt`，`ce_french_empire.txt` 的维持拿破仑王朝月度随机事件加 3 件（各权重 10，调王朝稳定度 −25～+50）。
- 中英 `nesnd_power_story_l_*`：西秦、明、法国新增部分的文字。

主要数值（源码估算，待实测）：权势 0–100，平常 +1.3/月，≥60 时 −0.6、≥80 时再 −1.0、≥95 时再 −2.0（平常约在 60–80 间平衡，条件最好时也停在 95 以下，满权势只能靠按钮或事件短暂达到）。宫廷事件平常 6–8/月，权势 ≥60 再 +3、≥80 再 +3。按钮费用常规 5/10、重大 10/20（无/有选举权），AI 留 20 点。换人：宠臣更替 ×0.5，共和同集团连任 ×0.7、换集团 ×0.5，政体互换 ×0.3。极端：遇害 20%（行刺执政者 15%），被逐或被捕流放 15%，脱身 65%，按钮清除成功 45%。

## 4. 怎么复测

不需新开局，读旧档即可（日志由 possible 自动激活）。控制台：

1. `tag AUS`（独裁君主制帝国）。人物界面任命一位宠臣，等一周，看两个头像、三条进度条、八张卡片。任命某集团领袖为宠臣时，若该集团最大，应出现“大权臣”字样（情形 B）。
2. 宫中无宠臣时宠臣头像框为空、显示“宫中尚无宠臣”，界面不报错。撤换宠臣再任命，看权势是否变为一半。
3. 极端：`effect set_variable = { name = nesnd_power_balance value = 5 }`、`effect set_variable = { name = nesnd_power_intrigue value = 99 }`，过一个月出极端事件。也可直接 `event nesnd_palace.21`（至 26）。
4. 保护排除：`effect random_scope_character = { limit = { has_role = character_role_favorite } set_character_immortal = yes }`，再做第 3 步。宠臣遇险不应出现，「剪除权臣」应不可用。
5. 共和：`tag HUS`，或在 AUS `effect activate_law = law_type:law_presidential_republic`，看「宫廷力量」消失、「执政府与反对党」出现，权势约为原来的三成。
6. 西秦 `tag QE1`（朝议已开启时）`event nesnd_qe1_intrigue.4`。明 `tag USM` `event nesnd_usm_court.1`。法国 `tag FRA` `event nesnd_fra_court.1`。

## 5. 遗留问题

- 2026-11-11 作者定：最大集团是“社会中最大的派系”，不以是否在政府区分（因此改组政府也无法换掉对手）。已改：每周按当权者所属集团与最大集团的理念差距（两集团 average_progressiveness 之差，≤25 相近，≥50 相左）设 `nesnd_power_relation`。相近：权势 +0.1、宫廷事件/政潮 −1、平衡每月向最大派系偏 0.5（逐渐被吸纳）、极端事件权重 −8。相左：权势 −0.1、宫廷事件/政潮 +1。替代原先按政体态度比较的两项，删去不再使用的 `nesnd_power_views_match`。共和文字去掉“反对党”预设，改称“[集团]的领袖”，平衡条改名「派系平衡」，状态行加关系说明。作者随后定名：共和日志改称「执政者与派系」（英文 Head of State and Factions），键名 nesnd_cabinet_* 不变。

- 2026-11-11 作者报：帝国以下的国家报 `Failed to fetch variable 'nesnd_power_balance'/'nesnd_power_power'`（scripted_progress_bars/nesnd_power.txt:166–168）。原因：进度条条件直接比较国家变量，从未开启本日志的国家没有这些变量，引擎仍会求值。已改：四个数值的比较一律经安全读数 `nesnd_power_p/_b/_i/_ten`（未设时取 0/50/0/0），人物与集团变量的作用域跳转一律改用 `?=`。覆盖进度条、月度数值、判定、按钮、效果、事件与自定义本地化。待复测。

- 2026-11-11 作者第二次实测反馈，已改（游戏外检查通过，待复测）：
  - 最大集团误认成工会：`ordered_interest_group` 未写 `position = 0`，遍历全部集团后 `save_scope_as` 留下了影响力最小的一个。已补，原版同类写法都带此项。人物面板头像下加了所属利益集团名，可直接核对。
  - 权势全部月度增减减半，另加人气：当权者人气 ≥50/≥20/≤−20/≤−50 为 +0.3/+0.15/−0.15/−0.3。情形 A 时最大集团领袖人气反向计入（−0.3/−0.15/+0.1/+0.2）。宫廷中统治者人气 ≥50 为 −0.2、≤−50 为 +0.2。
  - 统治者（共和为执政者）人气决定裁抑能力：拘押、查办的成功率 45%，人气 ≥50/≥20 加 15/5，≤−20/≤−50 减 10/20（`nesnd_power_arrest_chance`）。「裁抑宠臣」「约束党羽」把平衡拉回中点 15/10/5。
  - 失效可见：未激活时仍显示（帝国以上的非共和国或共和国），列出不满足的条件。状态行加“失效条件”悬停说明。
  - 文字函数：事件用保存对象的人名、统治者头衔（GetPrimaryRoleTitle）、国名。共和事件在执政者名前加其头衔。日志说明、状态行、按钮说明与效果提示用 `ROOT.GetCountry.GetRuler`、国名，人名与集团名经自定义本地化 `nesnd_power_holder_name` 等取得，人物或集团不存在时退回通称，避免取不到对象报错。进度条条面仍用通称（只有 JournalEntry 上下文）。
  - 宫廷事件改为各国通用的用语（督抚→地方长官，罢朝→抵制议事，寿宴→生日宴会，门生故吏/门下→亲信，税卡→税关，诏书→法令，御前→统治者面前，禁军→宫廷卫队，清君侧、逼宫等标题改写）。西秦、明、法国事件属本国剧情，保留原有用语，只补头衔与国名。
  - 极端事件改为可能发生：权重 15，与 11–12 件常规事件同抽，失衡时约三成。各加 5 件常规、2 件极端事件（宫廷 31–35、41–42，共和 31–35、41–42）。

- 2026-11-11 作者实测报 5691 个错误。error.log 全部来自日志状态行：`status_desc` 没有 JournalEntry 数据上下文，`nesnd_palace_status` 中的 `JournalEntry.GetCountry.GetCustom(...)` 每帧报错。已改为脚本内 `first_valid` 选键，删除该自定义本地化，待作者复测。其余用到 JournalEntry 的键只在进度条说明与日志控件中，与原版用法一致。

- 全部未实机验证：诏令卡片布局与人物面板位置、`can_deactivate` 的失效与重新激活、缩放修正在失效时撤销、`state_tax_waste_add` 作国家修正时是否传到各州、AI 实际花费节奏。
- 界面素材仍用原版占位图，生图指令见 WORK `art-prompt.md`。
- 「安抚诸派」等卡片名称不随情形 A/B 改名，情形差异写在卡片说明和效果里。
- 在世人物被刺死后，引擎何时选出新统治者（共和国 `kill_character` 统治者）未查证，执政者空缺期按 −1/月流失。
