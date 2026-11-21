# 中央与各邦：税收、军务与外交、学务与公职

Execution: completed  
Validation: STATIC_PASS  
Blocked by: none  
Evidence: 工作台 `reports/2026-11-21-india-development/中央与各邦/交付记录.md`

本文的「莫卧儿」泛指满足 `nesnd_india_empire` 的国家。「印度附属国」指莫卧儿的直属附属国中满足 `nesnd_india_country` 的国家，任何附属国类型都算。依据工作台设计报告第六节（谁收税、谁任官、谁养军）和提示词 `prompts/04-中央与各邦.txt`。

## 日志

新日志 `nesnd_india_order`「中央与各邦」（`common/journal_entries/nesnd_india_order.txt`，正文由工作台 `中央与各邦/build_journal.py` 生成）。持有条件 `nesnd_india_order_live`：莫卧儿、改革完成、至少一个印度附属国。每月由 `nesnd_india_refresh` 调 `nesnd_india_order_upkeep` 补挂；条件不再成立时日志不显示地结束，`nesnd_india_order_end` 清掉一切。

三件事各一对按钮，选一端写变量（1 中央，2 地方），改选后 60 个月冷却（`nesnd_india_order_<事>_wait`），开局都未选。

| 事 | 变量 | 中央 | 地方 |
|---|---|---|---|
| 税收 | `nesnd_india_order_tax` | 与每个印度附属国订「提高附属国贡金」；本国征税能力 +5% | 订「降低附属国贡金」 |
| 军务与外交 | `nesnd_india_order_army` | 本国每个附属国权威力 +10；每个印度附属国每周独立倾向 +0.05 | 订「免除军事服务」 |
| 学务与公职 | `nesnd_india_order_school` | 订「分享知识」；本国人口资格 +5% | 每个印度附属国人口资格 +5%、每周独立倾向 −0.05 |

条约用 `can_create_diplomatic_pact` 先查，建成后在附属国身上记标记 `nesnd_india_order_tax_pact`（1 提高、2 降低）、`nesnd_india_order_army_pact`（2）、`nesnd_india_order_school_pact`（1），同时记 `nesnd_india_order_lord`。只撤有标记、由莫卧儿发起的条约。签不了的不记标记，每月再试。标记在而条约没了（玩家或 AI 撤了），不重建，到改选或附属国离开时清。附属国离开后，由它自己的月度刷新跑 `nesnd_india_order_leave`（on_action 的范围加了 `has_variable = nesnd_india_order_lord`）。

## 改国号后的奖励

`nesnd_india_initialize` 给 `c:MUG` 补记 `nesnd_india_mughal_court`，改国号后仍在。「学校与官署」「工场与军队」的莫卧儿专属奖励改按它发，别的土邦成立 BHT、DRA 拿通用奖励。

## 没有做

跨州铁路分摊、赈济调粮、歉收压力测试；改附属国类型或傀儡化；地方退出或重新谈判；莫卧儿与法兰西的旧约、王公会议、饥荒；BHT、DRA 的成立条件。

## 待实机

接着 05 的编号：

28. 脚本 `create_diplomatic_pact` 建这四种条约；`can_create_diplomatic_pact` 对自治领、朝贡国、受保护国、傀儡国的结果（例 3、6、13）。
29. `remove_diplomatic_pact` 撤有 12 个月强制期的条约（降低附属国贡金、免除军事服务、分享知识）能否撤掉，撤时是否触发对方独立倾向 +10。
30. 正文三行的计数和改选日期显示。
31. AI 莫卧儿会不会按原版的 will_break 自己撤掉本日志建的条约。
32. 成立 BHT 后日志、选择、条约、修正都在（例 10），以及莫卧儿专属奖励（例 11）。
33. 附属国独立后，标记、修正、条约在一个月内清干净（例 8）。
34. 分享知识在莫卧儿科技不多于对方时自动解除，正文计入「已撤」。
35. `country_authority_per_subject_add` 写在国家修正上生效（原版只用在国家集团原则上）。
