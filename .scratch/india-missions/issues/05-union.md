# 土邦加入：并入或自治领

Execution: completed  
Validation: STATIC_PASS  
Blocked by: none  
Evidence: 工作台 `reports/2026-11-21-india-development/土邦加入/交付记录.md`

本文的「莫卧儿」泛指满足 `nesnd_india_empire` 的国家（1836 年只有莫卧儿）。依据工作台设计报告第六、九、十节和提示词 `prompts/03-土邦加入：并入或自治领.txt`。

## 一次结算

`nesnd_india_settle_union = { MODE = merge|dominion }`（`common/scripted_effects/nesnd_india_diplomacy.txt`）是唯一的结算。调用前存好 `scope:india_union_prince`（土邦）、`scope:india_union_requester`（发出邀请或请求的国家）和值 `scope:india_union_price`（报价），在莫卧儿的作用域里调用。步骤：土邦若是别国的附属国，先 `make_independent`，莫卧儿付报价，记一份王公年金，清发出方的请求，按方式分开（merge：清土邦的请求和顾问再 annex；dominion：报价付给土邦，订为自治领），有原宗主国时再付它一笔等于报价的补偿，刷新。从答复事件进来走 `nesnd_india_union_accept = { MODE = … }`（`nesnd_india_union.txt`）。

## 两条入口

| 入口 | 请求种类 | 谁答复 | 选项 |
|---|---|---|---|
| 莫卧儿邀请（按钮「邀请土邦加入」，选对象事件 `.5`） | 6 | 土邦 | 并入、成为自治领、婉拒。已是莫卧儿附属国的只有并入、婉拒 |
| 土邦请求加入（「诸邦之间」按钮「请求加入」，选方式事件 `nesnd_india_union.4`） | 8 | 莫卧儿 | 同意、婉拒。已是莫卧儿附属国的只能请求并入 |

对象可以是任何国家的附属国。是别国的附属国时，先在「印度事务」里问原宗主国（事务种类 6，许可规则仍是 `nesnd_india_consent_needed`，按 GRANTS = yes 传入），30 日不答复算不许可。许可以后事务结束，邀请或请求照常进请求通道，许可不留到下一次。婉拒双方各收通知，什么都不改，冷却照现有。

莫卧儿有几个时，土邦一侧取 GDP 最高的一个（变量 `nesnd_india_union_host`，每月由 `nesnd_india_refresh` 设定），「与莫卧儿商议互保」也跟随它，改国号后仍在。

「印度的新秩序」完成条件加一条：本国和本国附属国持有的有人口的印度州（`nesnd_india_state`）占全部的 75% 以上（`nesnd_india_held_share`），状态行显示当前比例。

## 顺带

- 不丹、尼泊尔条约的文字：「续订」改「续约」，泛指的「印度政府」改成动态国名或「印度国家」，日志名改为「喜马拉雅山区的条约」。
- 作者转来的 T9 实机刷错：使团工坊条件在未建成的工坊上读所有权（`country_ownership_fraction`），加了原版的 `level > 0`（`common/scripted_triggers/nesnd_india_diplomacy.txt` 两处）。

## 没有做

帝国制度的两端、武力统一的专门玩法、BHT 与 DRA 成立条件、贷款和担保、`transfer_subject`、开局附属关系、天竺与远山宣慰司。已有文字里用城市名指莫卧儿政府的代称没改。日志 `nesnd_india_schools`、`nesnd_india_industry` 的完成奖励按 `c:MUG` 发放莫卧儿专属修正（`common/journal_entries/nesnd_india_core.txt`），改国号后发通用修正，留给作者定。

## 待实机

接着 04 的编号：

17. 附属国的州算不算进 BHT、DRA 的成立比例（查原版文字只说 control，推断不算）。
18. 例 5：同一个效果里 `make_independent` 再订自治领；自治领要求宗主国国家等级更高，等级不够时订不成。
19. 例 13：成立 BHT 后国家变量、王公年金、自治领、出资约定都在。
20. 土邦成为自治领后，与莫卧儿的共同防御条约由引擎撤掉，与第三国的保留。
21. 被并入的土邦里外国政府的建筑产权去向。
22. 答复事件：邀请显示三个或两个选项，请求显示同意、婉拒，其余请求种类不变。
23. 例 17：旧档里未答复的邀请。
24. 「印度的新秩序」比例显示，以及遍历全部国家的州是否卡顿。
25. 原宗主国在「印度事务」里看到的许可说明（两层变量取国名）。
26. T9 的工坊所有权刷错不再出现。
27. 土邦按钮的国名在改国号后更新。
