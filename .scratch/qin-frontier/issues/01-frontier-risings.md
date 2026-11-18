# 01 西秦「边疆诸部」与波斯「将军府的忠心」：第一版实施

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-16）
Blocked by: none
Validation: STATIC_PASS
Evidence: `nesnd-workbench/research/2026-11-16-qin-fracture/`（01–05 号文档、checks/、v3tree/ 内容树、tools/qe1_pops.py）

## 1. 现象与期望

作者 2026-11-16：西秦的内部问题日志没有压力，波斯将军府很少走独立路线。要求起义有威胁，与原版民族独立运动挂钩，学美国内战运动的写法。起事者是西秦军中的合法军官和部族民兵领袖，也包括汉羌人，他们否定“汉羌认同”。

作者定的范围：南线阿富汗（七州加俾路支三州）、北线草原六州（国号乌兹别克汗国，首都锡尔河）各有一条地区条。土库曼、希瓦、浩罕连锁响应。康国（乌兹别基亚）、塔吉克斯坦、吉尔吉斯、西域核心、吐蕃、蒙古不反。兵力按西秦兵力的比例。西秦有“敌国越多越能打”的战意。波斯用一条持续的态度条。人物用真实历史人物。

## 2. 原因

调查见工作台 `01-现状调查.md`：团结度开局每月净变化约 0，不产生任何修正。波斯 AI 一次掷骰 75/25。

## 3. 改了什么

新文件（都叫 `nesnd_qe1_frontier.txt`，另有 `events/nesnd_per_stance.txt`）：

- `common/political_movements/`：两个自定义分离运动 `movement_nesnd_qe1_afghan`、`movement_nesnd_qe1_uzbek`。仿原版 `movement_anti_slavery` 的 secession 段，`forced_tags` 指定 AFG、KAZ，`state_weight` 指定州。激进度读地区条（50 为 0，100 为 +100%）。本地区内的西域汉羌也可以支持。
- `common/journal_entries/`：`nesnd_qe1_frontier_journal`（三条进度条、六个按钮、三个月度随机事件）和 `nesnd_per_stance_journal`。
- `common/scripted_effects/`：月结、文化退转、认领引擎建出的新国家（国号、首都、人物、军队）、战果判定、连锁响应（土库曼与希瓦，十八个月后浩罕，借用现有 `dp_nesnd_qe1_frontier` 开战）、许以自治、波斯态度条。
- `common/scripted_triggers/`、`script_values/`、`scripted_progress_bars/`、`scripted_buttons/`、`static_modifiers/`、`on_actions/`（`on_secession_start`）。
- 事件 `nesnd_qe1_frontier.1–13`、`nesnd_per_stance.2–3`。中英文字 185 键。

改动的现有文件：

- `common/script_values/nesnd_qe1_identity.txt`：团结度加五项来源（边疆积怨、民族之说、合法性、宫廷、边疆诸部），波斯联络由 −1 改为 −0.5。
- `common/scripted_progress_bars/nesnd_qe1_identity.txt`：明细加五行。
- `common/journal_entries/nesnd_qe1_identity.txt`：加两个按团结度缩放的修正。
- `common/dynamic_country_names/00_dynamic_country_names.txt`：KAZ 加「乌兹别克汗国」一项。

## 4. 第二轮（同日，作者离线，按默认自行决定）

- 「羌种暴动」起义条涨满的结局由全盘解体改为 `nesnd_qe1_fr_final`：尚未起事的两处立刻由脚本建国并开战，连锁响应随即开始，弹 `nesnd_qe1_frontier.14`。`nesnd_qe1_breakup` 及各 `release_*` 效果保留未删，现在没有调用者。只改了 `common/journal_entries/nesnd_qe1_identity.txt` 一行。
- 波斯 AI 选路线不再掷 75/25（`common/scripted_effects/nesnd_per_campaign.txt`）：看「将军府的忠心」，60 以上联络，40 以下遣使，1845 年仍未定时按当时倾向定。没有态度条时（已不是西秦附属）才用旧掷骰。
- 波斯出兵助剿要求有叛军正在交战。
- 群山动乱加一项“什叶派教师”：波斯忠心 60 以上时每月 +0.05。
- 补人物：卡姆兰·杜兰尼、努尔别尔迪、莫拉涅佩斯、穆苏尔曼库尔、娜迪拉。
- 文字：【白毡上的苏丹】点出阿布海尔与昔班尼。

## 4a. 没有做的

- 俄罗斯：本 MOD 的 `nesnd_rus_regional_compat.txt` 在草原相关条件里读 `c:KAZ`（如 `:281`、`nesnd_rus_kazakh_seed`）。乌兹别克汗国用的就是 KAZ，俄罗斯的草原日志会把它当作哈萨克参与者。只查到这一层，没有改。
- 汗国建国后境内汉羌屯民的内容。克什米尔按不反处理。乔坎·瓦里汉诺夫（1835 年生）没有做。

## 4b. 第三轮（作者七条意见）

详见工作台 `06-第三轮：七条意见的处理.md`。

- 删除「羌种暴动」：日志、起义条、月结中的唤醒与推进、全盘解体脚本（`nesnd_qe1_breakup` 与十六个 `release_*`）、事件 `nesnd_qe1_fracture.2`、上一轮的 `nesnd_qe1_fr_final` 与事件 14。文字键中英各 33 个退役，存工作台。
- 波斯：删除「近西帝国的未来」日志、进度条、两个按钮、事件 `nesnd_per.9`（三个 `nesnd_per_campaign.txt` 文件整个删除）。方略改由「将军府的忠心」决定：≤20 定策助秦（弹 `nesnd_per.4`），到 100 自立（弹 `nesnd_per.5`）。`nesnd_per_route_aid / _covert / nesnd_per_future_done` 三个变量照旧写入，教派、矿冶、波斯之忧的读取不变。`nesnd_qe1_persian_subversion` 改为读忠心 ≥60。
- 俄罗斯：`nesnd_rus_regional_compat` 会自己建立 KAZ 并把它当俄国属国。汗国改用 UZB，动态国名另起文件 `common/dynamic_country_names/nesnd_qe1_frontier.txt`，撤回对 `00_dynamic_country_names.txt` 的改动。
- 数值（按模拟）：边疆积怨随已了结地区减半、归零；地区条到 60 的惩罚 −0.10；一处独立或自治后 +0.10；波斯一项 −0.25；两个运动的分离条件加“对方起事后五年内不得分离”。
- 人物收敛为君主、将领、鼓动者。鼓动者在运动出现时登场于西秦境内。
- 文字：事件正文与引文按 no-invention 重写，正文用作用域取国名。

修过一处自己造成的错误：改写 `nesnd_qe1_unity_frontier` 时多留了一个右括号，`script_xcheck` 报 PARSE 后修正，并对全部相关文件做了括号配平扫描。

## 4c. 第四轮（补贴方案、文字语体、复核）

- 文字：按作者意见去口语化和金句，中英各改 40 键。日志正文不再写“军饷官缺先紧着老秦人”（无依据），改用作者立意：信仰文化受压制、族人贫困、地位在老秦人之下。波斯日志正文改写为脚本实有的两种方略。已部署 `e33718741b57c8fc654bf9d2c042cd58`。
- 两项团结补贴的数值方案只是提案，未实施。共用脚本，影响日本、西秦、印度、唐衣大食。方案与模拟见工作台 `research/2026-11-16-qin-fracture/07-第四轮：补贴数值方案与文字语体.md`、`tools/subsidy_sim.py`。
- 复核：提示数字与脚本逐项一致。cliche_check 只剩冷却提示一条，loc_link_check 0，185 键成对。脚本本轮未改。

## 4d. 第五轮（补贴的激进与忠诚效果）

- 两枚团结补贴按钮开启时各结算一次：平均融合度四级、五级的文化 15% 人口趋于激进，一至三级的文化 15% 人口趋于忠诚。原每月 0.1% 主流文化激进效果删除。按文化的平均融合度分类，因为引擎效果不能按单个人口筛选。四国共用。未实机验证。

## 4e. 第六轮（西秦补贴方案实施）

- 团结补贴在西秦改读专用公式：0.35 × 国情 × 区间 × 续期（`nesnd_qe1_subsidy_*`）。其余三国不变。
- 团结度新增五项来源：国库收支、激进派、生活水平、污染、饥荒（`has_famine` 的州每个 −0.05，至多 −0.30）。
- 已部署 `6dfb59239d6e2f4d6164ac60fb3fe7ab`，未实机验证。日本的新方案只是提案。详见工作台 `research/2026-11-16-qin-fracture/08-第六轮：西秦补贴方案实施与日本新方案.md`。

## 5. 验证

游戏外：`script_xcheck`（9 条，均为检查器不认识的写法：`relations:root`、`$REGION$` 参数、事件 `ai_chance = { base }`，以及原有的 `nesnd_power_type`）；Toolkit 语法检查 16 个文件，只有 on_actions 目录的已知误报；`loc_link_check` 0 条；`cliche_check` 新键命中 1 条（冷却提示，机制文字，保留）；vic3-tiger 对新的效果、数值、按钮、事件文件没有报告。

未实机验证，尤其是：自定义运动能否被引擎创建并按 `forced_tags` 分离；`on_secession_start` 时新国家是否已持有州；`create_military_formation` 的骑兵；国家修正里的州级修正是否传到各州；`scaling_modifiers_while_active` 的显示。

## 6. 复测

新开局用西秦。控制台 `tag QE1`。1840 年后应出现「边疆诸部」。把团结度压低（或等几年）后群山动乱上涨，到 40 弹【喀布尔的队正】并出现运动。运动激进度到 75% 后在政治界面可见分离进度。开战后应弹【兴都库什的烽火】，阿富汗由多斯特·穆罕默德统治并有一支军队，日志第三条「老秦战意」为 20。
