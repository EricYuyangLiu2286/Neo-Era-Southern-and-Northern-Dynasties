Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Blocked by: none
Validation: STATIC_PASS
Evidence: 部署版本 `fc01f5734ffbfd3143ce72c7976702a7`（2026-11-18，含复核补改、头像标题与事件领袖守卫）。首版随 `8b9f06e3`（2026-11-17 23:54 force 部署）上线。

# 宠臣/执政者与最大集团领袖同属一个集团时，改与其集团以外的最大集团比较

## 1. 现象与期望

莫卧儿「宫廷力量」：宠臣桑托什·乔汉属于柴明达尔，最大集团也是柴明达尔，领袖是索汉·拉尔。日志写“权力平衡表示桑托什·乔汉一方与柴明达尔之间的消长……两派理念相近”，等于一个集团自己和自己较量。
期望：被选中的人与最大集团领袖同属一个集团、但不是同一人时，对手改为其所在集团以外的最大集团。被选中的人本人就是最大集团领袖（情形 2）保持不变。

## 2. 原因

`common/scripted_effects/nesnd_power.txt` 的 `nesnd_power_refresh` 总取全国最大集团作对手，只按“当权者是不是它的领袖”分情形。同集团、不同人落进情形 1，对手是自己的集团，关系一栏又因“同一集团视为相近”被记为相近。

## 3. 改了什么

- `common/scripted_effects/nesnd_power.txt`：当权者是最大集团领袖时对手仍为最大集团（情形 2）。否则对手取当权者所在集团以外影响力最高的集团（`ordered_interest_group` + `limit = { NOT = { prev.var:nesnd_power_holder_ig ?= this } }`）。没有可选集团时撤去 `nesnd_power_top_ig`。删去“同一集团视为相近”。对手集团或其领袖换了时平衡偏离减半，沿用原规则。
- `common/customizable_localization/nesnd_power.txt`：新增 `nesnd_power_leader_label`，头像标题显示对手集团名称（见下方 2026-11-18 条），变量缺失时按情形退回“最大利益集团的领袖”或“对手利益集团的领袖”。
- `common/script_values/nesnd_power.txt`、`events/nesnd_palace.txt`、`events/nesnd_cabinet.txt`：只改注释。
- 中英 `nesnd_power_l_*.yml`：两个日志的 `_reason` 和 `status_a`、关系文字、平衡条右端、≤20 条件、通称、两个头像标题键。cliche_check 0 条，loc_link_check 0 条。

- 复核补改（2026-11-18）：中英 `nesnd_power_bars_l_*.yml` 的进度条增减项（对手领袖人望、理念相近/相左、影响力比、理念吸纳）首版漏改，仍写“最大集团/最大派系”，改为“对手集团/对手派系”。增减项没有数据上下文，只能写通称。英文去掉玩家文字中的 “holder”，改为 “the side in power”（与中文“当权一方”一致）。

- 头像标题（2026-11-18）：改为显示对手集团名称（`nesnd_power_label_leader_named`，JournalEntry 上下文，变量缺失时退回通称）。标题框加宽到 220 并加 `fontsize_min = 14`、`elide = right`，防止长英文名溢出。
- 事件领袖守卫（2026-11-18）：`nesnd_power_case_a` 加对手领袖在世。新增 `nesnd_power_has_rival`（情形 A 或 B），用于两日志事件 .12、.14、.15、.17 的触发条件与抽取表，以及 `quarrel_ok`、`debate_ok`、`counsel_ok`、`budget_ok`、`retire_ok`、宫廷 `strike_ok`。宫廷 .14 在无宠臣时仍可抽到。对手领袖缺失或刚死的那一周，这些事件不再抽到。

统治者与内阁：首相在任时其集团必在政府中（`common/scripted_triggers/nesnd_premier.txt:49-56`），最大在野集团只从不在政府中的集团里取（`common/scripted_effects/nesnd_premier.txt:171-176`），同一次刷新先校验首相再取在野集团，不会是同一集团，未改。

## 4. 怎么复测

新开局莫卧儿（推断开局即有同集团宠臣，未核实，宠臣随机抽取），看宫廷力量面板：头像标题、状态行、平衡增减与关系都应指向柴明达尔以外的最大集团。旧存档在一周内刷新，平衡偏离减半一次。

## 5. 遗留问题


- 当权者不属任何集团时，理念差距取 0，关系显示为“相近”（原有行为）。
- 统治者与内阁首相空缺时 `nesnd_premier_pm_ig` 保留旧集团，可能与最大在野集团相同。此时没有首相，不构成对峙（推断，未核实）。
