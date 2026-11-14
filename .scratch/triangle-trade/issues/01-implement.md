# 01 北洋 / 西洋三角贸易：实施

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-11）
Blocked by: none
Validation: STATIC_PASS
Evidence: `nesnd-workbench/reports/2026-11-11-triangle-trade/audit.json`；内容树 `nesnd-workbench/reports/content-tree/cases/triangle-north.*`、`triangle-west.*`

## 1. 现象与期望

新增两个全局日志，在参与国之间以进度条节奏买卖贫困 pop，迁入后变为奴隶。方案见 [spec.md](../spec.md)。作者对方案的八条答复：判定州决定资格 a；登莱、日本开局改债务奴隶制，俄国改遗留奴隶制；失效对象是“除奴隶制外其他条件都符合的国家”，永久终止；琉球、藏族加入儒家文化圈，女真单列可卖；殖民地奴隶制仍算奴隶制；买方同受文化限制；默认关闭；失效弹窗叙事事件。

## 2. 原因

新内容。迁入后与目标州同文化同宗教同职业的 pop 合并（大流散 `scripted_effects/nesnd_diaspora.txt` 已注明），所以目标州须没有该文化宗教的非奴隶人口，改职业时才不会波及原住户。

## 3. 改了什么

- 新增 `common/{geographic_regions,scripted_triggers,scripted_effects,script_values,scripted_buttons,journal_entries,scripted_progress_bars,static_modifiers,history/global}/nesnd_triangle_trade.txt`、`events/nesnd_triangle_trade.txt`、中英 `nesnd_triangle_trade_l_*.yml`。
- `history/countries/SHA.txt`：禁止蓄奴 → 债务奴隶制。`jap - japan.txt`：加债务奴隶制。`rus - russia.txt`：加遗留奴隶制。
- `cultures/CE_cultures.txt`：藏族加 `tradition_sinosphere`（保留 `tradition_himalayan`），琉球加 `tradition_sinosphere`。

可调数值：买方修正天数 `script_values/nesnd_triangle_trade.txt` 的 `nesnd_triangle_credit_days`（913 天）；人口门槛 25 万、pop 财富 <10、识字 <30%、规模 ≥5,000 在 `nesnd_triangle_region_country`、`nesnd_triangle_poor_pop`；每单人数在 `nesnd_triangle_set_amount`。

## 4. 怎么复测

需新开局（开局法律与文化改动只在新开局生效）。

2026-11-11 作者反馈：进度条悬停显示“当前无进度”。原因是进度存在全局变量里、由脚本写到条上，条本身没有 `monthly_progress`，原版提示 `PROGRESS_BAR_BREAKDOWN` 无条目可列。按作者要求改为原生写法：进度条 `monthly_progress` 三行来源（基础 +1、奴隶贸易或殖民地奴隶制的参与国、商业海军），日志周脉冲读 `scripted_bar_progress` 满 100 结算，`set_bar_progress` 清零；删去 `_trade_progress`、`_trade_rate` 两个全局变量和正文增速行。控制台已无法直接加满进度，成交须等进度自然涨满（西洋开局约 8 个月一单，北洋较慢）。失败与失效仍可用控制台制造（清空买方模式、让目标州所有国禁奴、设 `nesnd_<KEY>_trade_ended`）。

2026-11-11 作者追加：成交时随机取 0 / 25% / 50% / 75% 死亡率（各 1/4）。迁移并改为奴隶后，在目标州该文化宗教的奴隶中用 `kill_population_in_state` 扣除，运抵与死亡人数按前后计数实测，写入 `_last_moved`、`_last_dead` 并显示在正文与两条成交事件里。卖方货款不受死亡影响。文本中把一单称作“一批货物”，不再写“一船”。

## 5. 遗留问题

- 死亡在目标州结算（原版没有从 pop 取职业的链接，无法只在迁出的那个 pop 上扣减）；目标州若原有同文化宗教的奴隶，扣除可能落到他们身上，人数总量不变。

- 未实机验证：`move_partial_pop` 后改职业、`state_population` 等点号取值、多段 `status_desc` 拼接、按钮 `selected` 显示、AI 年度重设频率、月结遍历人口的性能。
- `manchu` 在 MOD 中无本地化，游戏显示原版“满”，不是“女真”。
- 买卖两方同受文化限制后，登莱卖出的辽东人只有登莱能买，日本卖出的朝鲜人只有日本系国家能买，这两项例外实际上很难成交。
- 藏族、琉球加入儒家文化圈的连带影响：西秦同化（`nesnd_qe1_identity.txt:17、50`）不再转化藏族人口；以藏族或琉球为主体文化的国家满足军事庄园修正案的文化条件（`amendments/nesnd_military_estates.txt:18、56`）；与其他儒家文化圈文化的接受度随共有传统上升。
