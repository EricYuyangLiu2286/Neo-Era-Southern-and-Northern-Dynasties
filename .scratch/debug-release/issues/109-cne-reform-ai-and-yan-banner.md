# 109 地权革命系列的 AI 提前结束；复燕燕旗新增两项来源

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-16）
Blocked by: none
Validation: STATIC_PASS
Evidence: [工作台报告目录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-16-cne-ai-yan>)（观察者存档解码、模拟脚本与结果、v3tree、xcheck、loc_link_check）· 部署 `80e7ddf9`

## 1. 地权革命系列怎样结束

1.15.1 没有“AI 放弃日志”的机制。日志只能经结局（outcome）、超时或失效结束（GAME `common/journal_entries/journal_entries.md`）。

| 存档 | 中华帝国已结束条目（日期、结局序号） | 结论 |
|---|---|---|
| 观察者局 `yangtze-ten-formal-play` autosave（1845-01-01，部署 `729ea498` 前后） | `je_ip4_coup` 1840-04-02 结局 0（政变成功）；营产 04-03、`ce_cne_land_reform` 04-04 **结局 1（失败）**、城市化 04-04、土地 04-05、信心 04-06（均为隐藏失效） | 原版政变成功，母日志失败条件 `nesnd_cne_coup_has_succeeded`（`common/journal_entries/ce_cne_land_draft.txt:49`）成立。四个子日志随 `nesnd_cne_programs_live` 失效。国家变量有 `nesnd_cne_coup_failure`、`nesnd_land_failed` |
| 观察者局 `观察者_1853_04_17.v3`（2026-11-12） | 四子日志 1841-03-23 至 25，母日志 1841-03-26 结局 2（隐藏失效） | 国家变量 `nesnd_land_frozen`、`ce_CNE_land_reform_done`：AI 按「议止地权革命」（`ai_chance = 1`），`nesnd_crisis.32` 选 a（权重 20）冻结 |

两局都不是超时或放弃。旧版本中提前结束主要来自「议止」冻结（2026-11-09 核算估为 AI 局的 30%）。本局来自政变。

政变由原版 `ip4_coup.1`（月度 on_action）发起：将领忠诚低于 25、政变实力足够（GAME `events/iberia_events/ip4_coup_events.txt`）。营产每开一州，全体将领忠诚 −1、军队支持 −1（`common/static_modifiers/nesnd_cne_programs.txt`），AI 在军队支持高于 −5 时最多开 3 州，支持 ≤ −8 才全停（`common/scripted_effects/nesnd_cne_programs.txt` AI 段）。忠诚随利益集团支持度变化（define `LOYALTY_FROM_IG_APPROVAL = 5`），所以 AI 自己开的营产就能把军队系将领推到 25 以下。2026-11-09 核算把政变当作每年 0.3% 的假设，没有落到脚本上。

存档只留下政变后的状态（1845 年 11 名将领忠诚多为 100，只有一人 43），1840 年政变将领与当时忠诚已无法复原。

## 2. 为什么现在才出现

对照 Git（`git log -- …cne…`）与 tag `original-20261030`：作者原作只有年度进度与随机事件，没有营产、政变失败条件和「议止」按钮，这些都是后来的代理稿。近期与本局相关的改动：

- 2026-11-15「统治者与内阁」：`nesnd_palace_shown` 加 `can_have_favorites = yes`。中华帝国不能任命宠臣，本局从 1836-01-01 起挂的是 `nesnd_premier_journal`（首相为军功爵，对手乡村民众）。该日志按平衡给各集团 ±1–3 支持度，并有专门针对军队集团的事件（`events/nesnd_premier.txt:683–695`）。这是本局唯一新出现、能直接改动军队支持度的系统，但没有 1840 年的存档，不能证明它就是政变的诱因。
- 同一改动的副作用：「做出让步」按钮要求 `has_journal_entry = nesnd_palace_journal`（`common/scripted_buttons/nesnd_cne_concession.txt:16`），中华帝国现在永远按不了。
- 2026-11-14 信心按月结算（任务 97）、让步（任务 99）、预警起义：与政变无直接连线。

## 3. AI 代码调整

| 位置 | 原值 → 新值 | 依据 |
|---|---|---|
| `common/scripted_buttons/nesnd_crisis_buttons.txt` `nesnd_land_suspend` 议止 | `1` → `0`；改革濒临失败（`nesnd_cne_ai_reform_doomed`：信心 ≤100，或失序 ≥80 且连续困苦 ≥6 个月）时 `10` | 核算 §7.7：权重 1 约让 30% 的 AI 局在 1837–1849 冻结。分档写法同原版 `00_balkan_wars_buttons.txt:181`、本 MOD 让步按钮 |
| `events/nesnd_land_reform_events.txt` `nesnd_crisis.32` a 结束改革 | `base = 20` → `base = 5`，濒临失败时 `add = 75`（与 b 的 80 相当） | 同上。冻结只在失败已近时才比失败划算。写法同原版 `ip4_coup_events.txt:884` |
| `common/scripted_effects/nesnd_cne_programs.txt` 营产 AI | 新增：营产在办且有将领忠诚 <25 或政变进行中，关停全部营产（土地商品化照常），6 个月内不再开（`nesnd_cne_ai_camp_wait`）；新开一州须全体将领忠诚 ≥40 | 本局政变；原版政变门槛 25（`ip4_coup.1`）；原版 `ip4_coup_events.txt:506`“If the AI can avert a coup, it will try to” |
| 同上 | 拆出 `nesnd_cne_stop_all_camps`，`nesnd_cne_stop_all_programs` 改为调用它；清理时移除新变量 | 只关营产、不停土地商品化 |
| `nesnd_land_review` 复核 | `20` → 失序 ≥25 时 `20`，否则 `0` | 核算 §7.6：失序 15–25 时复核压低无威胁的数值，还附行政力 −5%，可能破坏“行政力 ≥0”完成条件 |
| `common/scripted_triggers/nesnd_cne_ai_agenda.txt` `nesnd_cne_ai_reform_window` | 去掉 `var:nesnd_land_months <= 96` | 核算 §5.1、§7.1：佃农制下完成结局关闭，96 个月后 AI 再无推动。原版葡萄牙、西班牙日志在整个日志期间加权（`GAME/common/laws/01_land_reform.txt:495`）。此触发器同时控制 `ai_strategy_nesnd_cne_land_and_schools`，策略也随之延长 |
| `common/laws/nesnd_cne_ai_agenda_overrides.txt` 自耕农法 | `750` → `1000`（仍要求在朝集团或 10% 运动支持） | 与原版葡萄牙、西班牙同值。不是强制通过，原版立法判断不变 |

未改：全面暂缓（仅信心 ≤600 时 15）、`nesnd_crisis.31`（极端危机已是失败）、年度事件 `flavorCNE.4–8`（无 ai_chance，两项等概率）。

## 4. 改前改后粗算

`WORK/reports/2026-11-16-cne-ai-yan/sim/land_reform_sim_1116.py`，3000 次，种子 20261116。沿用 2026-11-09 核算的模型，改为月度信心（军功爵在朝 −20、盈余一半月份 +30、生活水平 ≥11 +30），政变按“每个营产每年 8%”估（**假设**，只由本局第 51 个月政变一例校准）。第 51 个月校准：进度 44.7（实测 49.25），信心 803（实测 824）。

| AI 中华帝国 | 改前 | 改后 |
|---|---|---|
| 母日志结束年中位（10%–90%） | 1839.5（1837.4–1845.8） | 1848.7（1839.5–1851.1） |
| 政变或原生革命失败 | 85.6%（中位 1839.5） | 41.2%（中位 1842.5） |
| 「议止」冻结 | 11.0%（中位 1838.6） | 21.1%（中位 1850.4，信心将尽时） |
| 信心耗尽失败 | 2.0% | 23.1% |
| 被共和国吞并 | 1.4% | 14.6% |
| 完成 | 0% | <0.1% |
| 进度到 100 | 0.7% | 5.5% |

敏感性：政变率取每营产每年 2% 时，政变失败 45% → 14%；取 15% 时 93% → 59%；拦截效果只有一半时为 72%。生活水平均值 11.2 时改后完成 10%，再加自耕农法必过为 32%（改前 1.3%）。

完成率仍近于零，原因与核算相同：开局佃农制、改革区生活水平约 10.8 低于 11。这两项不是 AI 权重能解决的。改动的效果是 AI 不再在头几年因政变或议止退出，日志平均多运行约 9 年。

## 5. 复燕之路：燕旗新增两项

复燕相关州（`nesnd_sha_yan_region`，`common/scripted_triggers/nesnd_sha_restore_yan.txt:14`）：辽东 `STATE_SHENGJING`、吉林 `STATE_SOUTHERN_MANCHURIA`、松江 `STATE_SONGJIANG`、黑龙江 `STATE_NORTHERN_MANCHURIA`、五国 `STATE_AMUR`、海参崴 `STATE_OUTER_MANCHURIA`、勃利 `STATE_BOLI`，共 7 个州区域。

- **国家遭受重大挫折 −5/月**：`nesnd_sha_yan_capital_lost`（同文件末尾）——登莱不再拥有 `STATE_SAKHALIN`（开局首都，`common/country_definitions/ce_countries.txt:134`；地图名「苦兀」）的任何部分，且没有经青岛决议（`nesnd_sha_qingdao_capital`）或海参崴迁都事件（`nesnd_sha_republic.8` a，新设 `nesnd_sha_vladivostok_capital`）迁都。按作者默认，正常迁都后丢失不算。
- **底层困苦 +0.5/州/月**：`nesnd_sha_yan_hardship_states`（`common/script_values/nesnd_sha_restore_yan.txt`）逐州区域计算下层阶层（`strata = lower`）按人口加权的平均生活水平，低于 9 计一州，不论归属。写法同原版 `ip5_je_values.txt:515`。
- 两行挂在 `common/scripted_progress_bars/nesnd_sha_restore_yan.txt` 的 `c:SHA` 段，中英键 `nesnd_sha_yan_capital_lost_row`、`nesnd_sha_yan_hardship_row`。

原有限定：整条进度只在中华帝国存在且登莱处于筹备期时结算（进度条外层 `limit`）。原有的“起事地区平均动荡”一行只算中华帝国持有的州，新一行不受此限。

实测（观察者局 1845-01，七州都属中华帝国）：五国 8.01，其余 9.67–10.14，即通常 1 州 +0.5。同一局中苦兀已归中华帝国。

## 6. 燕旗时间估算

`WORK/reports/2026-11-16-cne-ai-yan/sim/yan_banner_sim.py`：经费连续 +4/月（AI 每年续拨晚一个月），联络每次 −50、成功率 80%，玩家 ≥50 即联络三处必需州，AI ≥65 才联络并会把辽东、吉林也联络上，≥95 议约，警示 90 日后 100 起事，期限 144 个月。不含“北朝交战或改革失败”的外部门槛。

| 情形 | 困苦州数 | 玩家：月数中位（期限内比例） | AI：月数中位 [10%–90%]（期限内比例） |
|---|---|---|---|
| 改前 | 0 | 65（100%） | 110 [97–124]（94.5%） |
| 常态 | 1 | 58（100%） | 97 [85–121]（99.2%） |
| | 2 | 52 | 87 |
| | 3 | 48 | 79 |
| 七州全困 | 7 | 36 | 58 |
| 失去首都 | 0–3 | 不可能（0%） | 不可能（0%） |
| 失去首都 | 7 | 101（94%） | 0% |

困苦一项不会造成超时，七州全困时玩家三年可备齐，属于极端局面。失去首都的 −5 大于经费的 +4，燕旗只降不升，是停滞而不是减速。

## 7. 待作者决定

1. ~~失去首都 −5 等于让复燕停滞，期限内无法完成。要“大幅减速”可改 −3（与经费合计 +1/月）。~~ 作者 2026-11-16 定：保留 −5，失去首都时复燕停滞是预期结果。
2. 正常迁都后丢失苦兀不算挫折（按默认实现）。
3. ~~中华帝国现在挂「统治者与内阁」，「做出让步」按钮因要求「宫廷力量」而永远不可用。~~ 作者 2026-11-16：三个日志是同一系统的三种情形，按日志分支。已改，见第 11 节。

## 11. 「做出让步」适用三种情形（2026-11-16，部署 `73e6a716`）

- `common/scripted_triggers/nesnd_cne_confidence.txt`：`nesnd_cne_concession_court`（三个日志之一在进行）、`nesnd_cne_concession_has_holder`（首相读 `nesnd_premier_has_pm`，其余读 `nesnd_power_has_holder`）、`nesnd_cne_concession_holder_ig = { IG = … }`（`nesnd_premier_pm_ig` 或 `nesnd_power_holder_ig`）。
- `common/script_values/nesnd_cne_confidence.txt`：`nesnd_cne_concession_b`，AI 权重的平衡读数按日志取 `nesnd_premier_b` 或 `nesnd_power_b`。
- `common/scripted_effects/nesnd_cne_confidence.txt`：平衡偏移在「统治者与内阁」下调用 `nesnd_premier_add = { BAR = balance AMT = 25 }`，其余照旧。集团修正改读 `nesnd_cne_concession_holder_ig`。
- `common/scripted_buttons/nesnd_cne_concession.txt`：条件与 ai_chance 改用上述触发器和值，数值不变。
- 文字：条件写三个日志之名，称谓（宠臣、大权臣、执政者、首相）和平衡一行按日志切换（`common/customizable_localization/nesnd_cne_concession.txt` 新增 `nesnd_cne_concession_holder_word`、`nesnd_cne_concession_balance_line`，`_target`、`_current` 加首相分支）。说明里补“首相在任命时即被认定”。新增中英各 7 键（含 `nesnd_premier_balance_add_25_tt`）。
- 检查：pdx 解析、script_xcheck 0 条，新键中英各一，loc_link_check 0 条，cliche_check 唯一命中为原有“冷却”的“却”，BOM 0。复测可读档：中华帝国「帝国人民的信心」里按钮应可用（信心 <1000、首相属于军功爵、军队或实业家），点击后「首相与各派」+25、信心 +150、得对应集团的让步修正。

## 8. 发现的其他问题（未改）

- `nesnd_cne_ai_started_camp` 只被移除、从未设置（`script_xcheck`）。
- 年度事件 `flavorCNE.4–8` 无 ai_chance。
- 燕旗“北朝正在交战”等原有行用泛称“北朝”。

## 9. 检查

pdx.py 解析 9 个改动文件通过。audit.py 7 条解析问题均在 `development/`、`.scratch/` 非运行文件。script_xcheck：新变量有写有读，`base`/`modifier.trigger` 为该工具不认识事件选项格式（与原版相同写法）。v3tree 重建索引后 `near` 确认 `nesnd_cne_ai_camp_wait`、`nesnd_sha_vladivostok_capital` 及新触发器、脚本值都有写有读。两键中英各一，无中文分号，loc_link_check 全 MOD 0 条，cliche_check 0 命中，BOM 0。部署 `80e7ddf9`。

## 10. 复测

需新开局（营产 AI 和燕旗来源都从开局起作用；海参崴迁都标记只在新局写入）。

- 观察者局五速运行到 1850 前后：中华帝国「地权革命」等五个日志不应在 1840 年前后结束。日志里看营产州数，政变日志出现时营产应关停。
- 登莱「复燕之路」开启后，悬停燕旗：常态应见“底层困苦”一行（通常 +0.50）。控制台 `own STATE_SAKHALIN CNE` 把苦兀给中华帝国，下月看“−5.00 国家遭受重大挫折”。在下层生活水平低于 9 的州（通常是五国），每州 +0.5。
