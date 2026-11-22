# 莫卧儿：与法兰西的旧约、王公会议、饥荒

Execution: completed  
Validation: STATIC_PASS  
Blocked by: none  
Evidence: 工作台 `reports/2026-11-21-india-development/莫卧儿/交付记录.md`

本文的「莫卧儿」只指带变量 `nesnd_india_mughal_court` 的国家（开局的 c:MUG，改国号后仍在）。别的土邦成立 BHT、DRA，不带这个变量，本任务的三件事都不给它。依据工作台设计报告第六节「莫卧儿：旧帝国能否重新取得支配权」和提示词 `prompts/05-莫卧儿：旧约、王公会议、饥荒.txt`。

## 文件

新文件：`common/scripted_triggers|scripted_effects|script_values|scripted_buttons|journal_entries|static_modifiers/nesnd_india_mughal.txt`，`events/nesnd_india_mughal.txt`（命名空间 `nesnd_mug`），`localization/*/replace/nesnd_india_mughal_l_*.yml`。

改动：「印度事务」一层（`nesnd_india_matters.txt` 四个文件和日志 `nesnd_india_foreign_affairs`）加事务种类 7、8、9；`nesnd_india_refresh` 调 `nesnd_mug_upkeep`；on_action 的范围加 `has_variable = nesnd_mug_loan_from`；土邦受邀加入时成为自治领的 AI 权重，带 `nesnd_mug_council_attended` 的加 10（`events/nesnd_india_diplomacy.txt`）。

## 与法兰西的旧约（日志 `nesnd_mug_france`）

持有条件 `nesnd_mug_france_live`：莫卧儿、是附属国、宗主国不是印度国家。不再成立时不显示地结束。

- 请求借款：事务种类 7 送宗主国。同意时宗主国付 £100,000，两国订 money_transfer 条约，莫卧儿每周付 £460，约束期五年（约 £120,000）。条约建不成时，莫卧儿改为每月由脚本直接付 £2,000，共 60 个月。
- 借款记录：`nesnd_mug_loan_from`（债权国）、`nesnd_mug_loan_term`（1825 日）、`nesnd_mug_loan_by_script`（按月付）。每月 `nesnd_mug_loan_tick`：陷入债务违约或宣布破产即违约，退出还款条约、清记录，莫卧儿给债权国贸易特权十年（签不成则关系 −50）；到期则退出条约、清记录、关系 +20；条约被别的方式终止则清记录并通知。附属关系变了或莫卧儿独立，借款照常。
- 赎回附属关系：事务种类 8 送宗主国，价钱 £250,000。同意时莫卧儿付款、宗主国收款、`make_independent`。建筑产权不动。
- 两个请求都占用 `nesnd_india_request_cooldown`（6 个月）。

## 王公会议（日志 `nesnd_mug_council`，事件 `nesnd_mug.11`–`.13`）

莫卧儿改革完成后可召集，冷却 `nesnd_mug_council_wait` 120 个月。议题铁路、赈济、共同防务三选一（`nesnd_mug_council_topic`）。按关系邀请至多 8 个土邦（`nesnd_mug_council_invite`），各自出席或婉拒（`nesnd_mug_council_answer`），30 日后结算：铁路、赈济给莫卧儿和出席者 120 个月修正，共同防务给每个出席者签五年共同防御条约。出席者记 `nesnd_mug_council_attended` 120 个月。

## 饥荒（事件 `nesnd_mug.21`–`.24`）

每月检查莫卧儿、土邦，以及不是莫卧儿的 BHT、DRA：有人口的印度州所在州区域有影响农田的收获状况（干旱、洪水、霜冻、野火、雹暴、蝗群、热浪、疫病爆发、强风、暴雨），且 24 个月内没收过（`nesnd_mug_famine_wait`）。受灾州记 `nesnd_mug_famine_state`（120 日）。自己赈济每州 £10,000，州得 12 个月修正。土邦还可请莫卧儿或宗主国援助（事务种类 9），同意后援助方付款、关系 +25，莫卧儿援助另记 `nesnd_mug_council_attended`。婉拒或不答复，土邦再选一次自己赈济或不赈济。

## 没有做

两次大起义和《孟买条约》（源目录没有现成剧情，要先从作者素材查人物和年代）；宗主国建筑产权的赎回或过户；法兰西主动续约或加价；触发收获状况；改开局附属关系和建筑数据；已有玩家文字里第二节列为不用的代称（7 个键，未改，见交付记录第八节）。

## 已按代码核验

2026-11-22 收尾批读代码定下，不进游戏。每项的依据（原版与源目录文件:行）见 工作台 reports/2026-11-21-india-development/收尾/审阅/待实机核验.md。

36. 莫卧儿开局没有科技 central_banking（money_transfer 条款的解锁科技），`can_create_treaty`、`create_treaty` 是否因此不成立，借款走条约还是走按月付（例 1）。
   结论：莫卧儿确实没有该科技；条款要求由哪一方具备，代码无法证实。 不改。
37. 朝贡国与宗主国之间能否签 money_transfer、trade_privilege 条约（例 1、2）。
   结论：money_transfer：条款不拦附属关系（只要付款方未违约、同约里没有反向的 take_on_debt），科技见 07-36。trade_privilege：莫卧儿仍是附属国时签不成。 收尾已改：nesnd_mug_guarantee_tt 中英改成有条件的说法（有自己的市场才给贸易特权，否则关系下降）。
38. 每周 £460 是否实际从莫卧儿付到宗主国；莫卧儿债务违约时引擎冻结付款（例 2）。
   结论：每周付款成立；引擎不会因违约冻结。 不改。
39. 脚本按条款和每周数额找到还款条约并退出（例 2、3）。
   结论：成立。 不改。
40. 借款期间赎回成功：还款条约仍在，宗主国在莫卧儿境内的建筑产权不变（例 4、5）。
   结论：条约部分成立；产权部分代码无法证实。 不改。
41. `nesnd_mug_overlord_levels`（`levels_owned_by_country` 以 `state.owner.overlord` 为目标逐级计数）在日志里显示的数目。
   结论：成立，有一个上限。 未改，可选：日志文字写「每座建筑至多计 10 级」，或把逐级判断加到 20 级（见核验报告）。
42. 王公会议：`ordered_country` 按 `relations:root` 取至多 8 个土邦，受邀土邦收事件，30 日后结算，计数显示（例 7–9）。
   结论：成立。 不改。
43. 莫卧儿（朝贡国）与土邦（朝贡国或傀儡国）之间建共同防御条约（例 8）。
   结论：朝贡国土邦可以（在条件内），傀儡国土邦不行。 不改。
44. 写在国家修正里的 `state_infrastructure_add`、`state_construction_mult`、`state_harvest_condition_*_impact_mult` 作用到本国各州。
   结论：成立。 不改。
45. 收获状况波及的州区域（不只中心）`has_harvest_condition` 为真，饥荒事件按月发出，24 个月内不重发（例 11–13）。
   结论：按月发、24 个月不重发成立；波及区域是否判真，代码无法证实。 不改。
46. 事件标题里的 `SCOPE.sCountry`、日志里的 `GetSubjectType.GetName`、`Var(...).GetValue` 显示正常。
   结论：成立。 不改。
47. 法兰西收到「印度事务」里借款、赎回、援助三种事务的正文和按钮（E2）。
   结论：成立。 不改。
48. 莫卧儿成立 BHT 后两条日志、在途借款、会议冷却都在（例 15）。
   结论：成立。 不改。

