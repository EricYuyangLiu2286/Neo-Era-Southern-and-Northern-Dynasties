# 19 殖民者一侧：旧约争议与法明对立（批次 15）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: agy  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/殖民者/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/殖民者/verify_colonial.py)

## 现象与期望

印度线此前仅有土邦与帝国一侧的改革、起事、独立与联合机制，缺少殖民宗主国（法兰西、大明联邦）一侧围绕莫卧儿旧约和印度势力范围的外交角逐与划界收场。本批补齐两套机制：莫卧儿与法兰西双边日志「旧约争议」，以及法兰西与大明联邦在印度的拉锯日志「法明对立」。

## 改动

- **旧约争议**（合入 `nesnd_india_empire` 同组文件与 `common/scripted_progress_bars/nesnd_india_core.txt`，不新建文件）：
  - 出现：`nesnd_mug_upkeep` 月度检查，莫卧儿仍为 FRA 附属国且满足改革既成（`nesnd_india_reform_done`）、独立倾向 ≥ 50 或王公会议成制（`nesnd_mug_council_settled`）之一、且不在冷却期时，向 FRA 发「旧约的继承」事件 `nesnd_mug.30`（不锁日期；AI 选质疑权重 70，独立倾向 ≥ 50 时改为 90；选不予追究则 10 年不再触发且关系 +10）。
  - 谈判进度与按钮：双方各开 `nesnd_india_treaty_dispute` / `nesnd_india_treaty_dispute_overlord`，共用 0–100 谈判条 `nesnd_india_treaty_dispute_bar`（起点 50，月度关系 ≥ 20 时 +1、≤ 0 时 −1）。莫卧儿有「遣使陈情」（周收入 ×4、£2,000–£20,000，条 +10，冷却 12 月）与「停缴岁贡」（条 −15，主体文化热忱目标 +5 持续 5 年，冷却 12 月）；FRA 有「重申旧约」（条 −10，关系 −10，冷却 12 月）与「许以新款」（同价算法，条 +10，冷却 12 月）。双方 AI 每月 5% 按规则点按钮。
  - 结局：条到 100 续约（关系 +30、莫卧儿永久 `nesnd_india_treaty_renewed`、FRA 永久 `nesnd_india_treaty_renewed_overlord` 及未持州印度区 `add_involvement +1000`、事件 `nesnd_mug.31`、20 年不再出继承事件）；条到 0 废约（FRA 得莫卧儿首都州宣称、`catalyst_event_negative`、AI 设 `conquer`；关系 −30；莫卧儿得 10 年 `nesnd_india_treaty_void`、主体文化热忱 +10 持续 10 年、若有「谋求独立」两进度条各 +10；双方各收 `nesnd_mug.32`）；争议期间莫卧儿不再是 FRA 附属国时以隐藏 `invalid_outcome` 静默结束，「与宗主国的旧约」照旧结算。
- **法明对立**（新建 `nesnd_india_rivalry` 一组文件，并在 `events/nesnd_india_empire.txt` 的 `nesnd_india_indep.12.c` 补 2 行移条接线）：
  - 出现：全局 `on_monthly_pulse`（`nesnd_india_rivalry_maintain`，不含 `root`）检查 FRA 与 USM 均存活且在印度各有州或印度附属国，满足关系 ≤ 0、旧约争议已有结局或任一方对对方印度州有宣称之一时，两国各开 `nesnd_india_rivalry`（不锁日期）。
  - 拉锯条与按钮：`nesnd_india_rivalry_bar`（−100 至 100，起点 0，正向 FRA、负向 USM；月度按印度附属国数与印度州数各比较 ±0.5）。双方均有「拉拢土邦」（周收入 ×4、£2,000–£20,000，与关系最高独立土邦关系 +15、移条 ±10，冷却 12 月；无独立土邦时灰显并提示一句；AI 每月 5% 使用）与「提议划界」（条在 −30 至 30 且未交战时可用，冷却 24 月）。独立事件 `nesnd_india_indep.12.c` 投向 FRA/USM 时同步移条 ±10。
  - 结局：任一方到 ±100 共用 `nesnd_india_rivalry_settle_upper`（胜方得对方在印度与己方或附属国相邻之州宣称至多 3 个、10 年 `nesnd_india_rivalry_upper` 威望 +10%、AI 设 `conquer`、收 `.2`；负方得 10 年 `nesnd_india_rivalry_lower` 正统 −5、AI 设 `antagonize`、收 `.3`；10 年后可再开）；提议划界发 `nesnd_india_rivalry.1`，对方同意则签 10 年期双向 `military_access` 条约（经 `can_create_treaty` 守卫）配 10 年双向停战 `create_bidirectional_truce`、关系 +30、双方各得 10 年 `nesnd_india_rivalry_border`（影响力 +5%）、两国日志结束并收《孟买条约》`.4`、20 年不再开；拒绝则提议方得 `catalyst_event_negative`、关系 −10、条向提议方移 10 并收 `.5`；任一方失去全部印度州与附属国时日志静默结束，留下一方得 `nesnd_india_rivalry_upper`。

## 代码无法证实

数值均为默认值，实机测试后再调。交付记录「代码无法证实」一节列了：双国日志同 tick 结算结局的防重时序、`create_treaty` 双向 `military_access` 配 `create_bidirectional_truce` 组合、`ordered_scope_state` 结合 `any_neighbouring_state` 与 `max = 3` 加宣称、进度条 `monthly_progress` 跨国脚本值悬停刷新，以及 1.15.2 双向条纹理/`marker` 的条面实机显示五项。
