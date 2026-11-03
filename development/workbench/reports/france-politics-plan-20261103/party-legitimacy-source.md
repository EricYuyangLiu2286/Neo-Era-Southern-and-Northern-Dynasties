# 法国政治方案：原版党派、选举与合法性来源核查

日期：2026-11-03。范围：只读研究，未改游戏脚本、未启动游戏。证据等级为 `SOURCE_RESEARCH / ENGINE_NOT_RUN`；这里的算式与闭包计划不代表真实游戏验收。按 NESND 技能、项目工程适配与 Matt research 的原始来源要求执行。本机 `catalog.py status` 返回 `1.13.11 / Steam build 24799966 / CURRENT / changed_count=0`。

路径：`GAME = D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`；`MOD = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`；`DOCS = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031`。以下行号均来自本次磁盘文件。引用表中的文件链接是来源；不把旧百科规则当本机版本事实。

## 作者最新约束（本报告建议的适用边界）

2026-11-03：常规政治目标采用相关IG执政＋合法性至少50；高于50只用于明确的困难目标。JE、决议、按钮不得检测指定党派组合、成员数或同党关系，也不能用隐藏条件或AI权重变相要求组合。以下党派成员/评分研究属于机制和党派定义的开发背景，不是任务达成条件；本轮方案优先沿用现有党派，未实施新党或强制分配。

## 核心结论

1. 原版党派数据库的实际接口为 `valid_for_country`、`available_for_interest_group`、`join_weight`，不是一个笼统的 `valid`。两个已读原版实例都在 `valid_for_country` 前注明 **只在游戏开始时运行一次**。法国不同路线能否参政应主要通过运行期 IG 可用性与评分表达，不能以 `update_party_support` 保证重新执行这项开局有效性。[S1][S2]
2. 有选举的国家中，党派由 IG 构成，正常组阁不能只把同党一个 IG 拉入政府而排除其他党内 IG。党派选票产生的政治力量按成员 IG 的势力比例分配；选票、IG 势力、人物人气、党派归属分数、竞选势头是不同量。[S3]
3. 每党最多三个 IG 是本项目的**设计目标与待验收不变量**，不是已证实的引擎硬上限。原版经常在第三个先加入的 IG 之后将评分乘零；但保守党在乘零后还有法国君主军方 `+10` 等加分，不能声称这段逻辑无条件封顶。[S1][S2]
4. 设计者理解“某 IG 入阁”的难度时，应考虑投票法、选举信任度、党鞭和整党组阁的原生后果；JE实际只检查所需IG执政与合法性50，不加入党派组成、政府实体数或同党成员门槛。不能把日志自定义“帝国稳定”视作原生合法性，也不能把人气 `+25` 写成势力 `+25%`。[S3][S6][S9][M1][M2]
5. 原生合法性阈值为 `0 / 25 / 50 / 75 / 90`。低于 25 的法律条件是“须有政治运动才能制定法律”，**不是绝对不能立法**。[S8]

## 量纲与相互作用

| 量 | 所属 scope、含义 | 已证实接口/关系 | 不应推出的结论 |
| --- | --- | --- | --- |
| `popularity` 人气 | character；本机范围 −100 至 +100 | `character_popularity_add`；IG 领袖人气影响 Pop 对 IG 的吸引力；党魁人气影响竞选势头；统治者人气影响权威。`POPULARITY_MOMENTUM_FACTOR=0.005`，所以人气 +25 对应该原生系数下势头 +0.125。[S3][S4] | 不能直接等同 IG 势力 +25 点、票数 +25%、全国支持率 +25%。普通阵营人物并不自动成为党魁。 |
| Pop/IG `political_strength` 政治力量 | Pop 的财富等生成力量，分配给其支持的 IG；选票也给党内 IG 贡献力量 | 原生概念说明未整合州 Pop 少得力量、首都更多；IG 的份额构成 clout。`interest_group_pol_str_mult/factor` 是 IG scope；`interest_group_ig_landowners_pol_str_mult` 等是具名 IG 类型的生成修正。[S3][S10] | `+20% political_strength` 不等于 clout 直接加 20 个百分点，因为分母也变。`political_strength_share` trigger 的对象是职业/宗教/文化在国家/州中的份额，不是 `ig_clout` 的别名。[S11] |
| `ig_clout` 势力 | interest_group；该 IG 占全国总政治力量的比例 | trigger 例为 `ig_clout >= 0.2`。有影响/强势与边缘化有滞回门槛：强势 20%进入/18%退出；相关 IG 5%进入/4%退出；边缘 IG 入党还参考 3%人口支持、留党参考 2%。[S4][S11] | 人口支持率、得票率、政府中力量占比都不是同一分母。`ig_government_power_share` 另以政府总政治力量为分母。 |
| 选票、`voting_power` | 选民数量与选票所带政治力量分别可见 | 法律决定谁有票及票的政治力量；Pop 倾向所属 IG 的党，竞选势头可吸引其他票；选举日结算后党票数固定到下次选举。党内 IG 按 clout 比例受益。[S3][S5] | 不能以“一人一票”推定各选举法政治力量相同；不能声称每名 IG 获得该党全额票力或固定均分。改党/解党/中途入党的精确重分配时机仍须引擎观察。 |
| 党派 affiliation / `join_weight` | 正在考虑加入的 IG 为 root；`scope:number` 是比它先加入的 IG 数 | 资格先经 `available_for_interest_group`；评分可看 IG、领袖意识形态、国家法律、现有党内成员等。进入最低 affiliation 1，留党最低 0.5；UI 有分项 affiliation tooltip。[S1][S2][S4][S12] | 不存在本次已核的通用 `add_party_attraction` 或 `recalculate_party` effect。用这些虚构接口实现不得进入候选。Pop 对 IG 的 attraction 与 IG 对党的 affiliation 不同。 |
| `election_momentum` 竞选势头 | party，竞选期 | 开始随机势头 0.5–1.5；党魁人气系数 0.005；`add_momentum` 是 party scope 且文档限定竞选期；概念说明选举结束后势头归零。[S3][S4][S7] | 不永久保存为王朝支持，不直接加原生合法性。`add_momentum=0.1` 是势头量，不是保证得票 +10%。 |
| `government_legitimacy` 合法性 | country，显示范围0–100 | 原生 modifier 影响基础值、统治者 IG 入阁、政府总 clout、总票份额、政府人数和意识形态差异。`government_legitimacy` trigger 只读实际值。[S5][S8][S11] | 不存在已核 `set_legitimacy=...` 的直接 setter；不能拿剧情积分冒充原生值。 |

源码能证实这些连接与参数，**不能从公开脚本复现整个引擎**：Pop 选票转移的完整公式、党籍全体排序/并列处理、每一次自动刷新时点、票力中途重分配以及脚本强行改政府后的引擎纠正次序均未在本次读取的脚本中完整公开。

## 完整链条：从选举法到组阁

### 1. 法律、选举资格和初始化

`country_has_voting_franchise` 检查一组 `country_*_voting_power*` modifier 是否大于零，包含基本票权、识字率票权、财富门槛、各职业票权；并非硬编码只认四种法律名称。MOD 的同名 trigger 位于 `common/scripted_triggers/00_scripted_triggers.txt:16–40`，内容与原版所读这一段相同。[S6][M3]

四项常用选举法的参数如下；这是法律自身贡献，必须再加政体、修正案、税率、事件和其他修正。`govt_size_add` 是允许的额外政府实体数，基础值另有 `+1`。[S5][S9]

| 原版法律 | 总票份额→合法性系数 | 政府总clout→合法性系数 | 选票力量参数 | 人数 allowance 增量 | 意识形态差异倍率增量 | 选举信任度影响倍率增量 |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `law_landed_voting` | 40 | 100 | 贵族100；军官/教士/资本家50 | +1 | +0.2 | −0.3 |
| `law_wealth_voting` | 65 | 75 | 基础50；财富门槛20 | +1 | +0.2 | −0.2 |
| `law_census_voting` | 85 | 55 | 财富门槛10；识字率票力50 | +1 | +0.1 | −0.1 |
| `law_universal_suffrage` | 110 | 25 | 基础50 | +1 | 无此项 | 无此项 |

例如政府 clout 0.5、选票份额0.4，仅 wealth voting 两项得到 `75×0.5 + 65×0.4 = 63.5`；这不是该政府最终合法性。无投票的 `law_autocracy` 自身为统治者IG入阁 +30、总clout系数120、差异倍率+0.5；`law_oligarchy` 自身为统治者IG入阁+10、clout120、允许政府数+2、差异−0.1。政体另叠加：君主制统治者IG+20、差异+0.1；议会共和票份额系数+20、允许政府数+1。[S5]

这些选举法的 `on_activate` 调用 `scripted_effect_parties_emergence`，并初始化选举信任度、继承有关修正案。原版 `00_scripted_effects.txt:274–283` 明确注释：此转换会立即触发选举，从而更新党派，故该 effect 不需再调用 `update_party_support`。非选举法调用对应 disappearance 提示并清理投票修正。**这段是原版法律转换证据，不是任意改变量都会自动重分党籍的证明。**[S6]

一党制是独立场景：`law_single_party_state` `on_activate` 调 `set_only_legal_party_from_ig = ruler.interest_group`；文档另有解除唯一合法党的 effect。它有基本票权且原生选举逻辑仍有相关入口，不能一概归类成“没有选举/没有党”。[S5][S7]

### 2. 至少两条原生党派定义

**自由党 `liberal_party`**：[S2]

- 图标 `gfx/interface/icons/political_parties/liberal.dds`，科技 `empiricism`；动态名称 `first_valid/triggered_desc` 与玩法资格分层。名称换了不等于创建新的党派类型。
- `valid_for_country = { always=yes }` 前标“只在游戏开始时运行一次”。运行期 `available_for_interest_group` 先要求投票权；已有党内成员或知识分子/小市民/实业家至少一个非边缘化；法西斯、整合主义、民族至上、共产、先锋、无政府主义领袖被排除。
- `join_weight` 初始 −5，按领袖/IG意识形态、当前国家法律及特例加减；如进步领袖+5。末尾强势知识分子×2，先加入者数≤1且本 IG 非强势/非边缘化时×2，已有2名时×0.5，已有≥3名时×0；人数项在本文件评分末尾。

**保守党 `conservative_party`**：[S1]

- `valid_for_country` 同样开局一次、始终可用。IG资格要求投票权，且已有成员或地主/教会/小市民至少一个非边缘化；工会明确不得加入。
- 初始−5；保守领袖+5，保守IG意识形态+5，地主clout≥0.15时+5，普选可使财阀/家长主义IG增加+5；各项反映共同法律利益而不是仅换名字。
- 强势地主×2；`scope:number=1`的适当非强势IG×2；先加入2名×0.5；先加入≥3名×0。但其后仍有法国王朝相互敌意−5、法国君主制下特定军方+10、其他国家特例加分。**乘零后再加分仍可回到可加入阈值**，因此本项目不能把复制这段等同“保证不超过3”。
- 法国原生权重识别原版 `ideology_bonapartist`、`ideology_legitimist`、`ideology_orleanist` 等符号；自定义人物/意识形态若未进入相同判定，不会因为叙事上是某派便自动命中。

适用差异：法国新路线可用自定义党派类型或有限覆盖，但必须考虑对原生常驻党的竞争。仅新增高分自定义党、不限制相冲突的现存党资格/评分，不能保证IG分配；直接强制改党也可能被下次原生刷新重新分配。

### 3. 原生脚本刷新与直接党籍接口

| 已核符号 | scope与效果 | 使用边界 |
| --- | --- | --- |
| `update_party_support = yes` | country；更新党派支持 | 文档仅写更新支持。原版 `events/brazil/caudillo.txt:403–425` 先给军方领袖设 `caudillo_conservative`，再刷新；保守党评分1184–1194读取该变量+20，形成调用→状态→评分→刷新闭包。 |
| `add_ig_to_party = ig:...` / `remove_ig_from_party = ig:...` | party，目标IG | 可调整成员，不能据此承诺永远覆盖权重、无入阁副作用或支持任意不存在的party对象。 |
| `disband_party = yes` | party；移除所有IG使其解散 | 不表示删除数据库中的潜在党。 |
| `set_ruling_party = yes` | party；将党内全部IG入阁、其余IG出阁 | 明确整体换政府；不适合作为仅“保证一个IG入阁”的无副作用操作。 |
| `add_ruling_interest_group = yes` / `remove_ruling_interest_group = yes` | interest_group | 文档允许操作个别IG；本次未证实对同党IG如何自动扩展/校正，不能以此绕过正常整党组阁规则来设计。 |
| `call_election = { months=N }` / `set_next_election_date` | country；改下一选举日期 | 前者不是“马上完成选举”，后者不是设置票数。 |
| `add_momentum = X` | party，竞选期 | 不等于改变 affiliation，不等于永久支持率。 |

效果来源为引擎文档 [S7]；刷新实际实例 [S13]。可用查询包括 country 的 `any_active_party`/`any_potential_party`，party 的 `any_member`/`has_party_member`，IG 的 `has_party`/`is_member_of_party` 与 `party` scope；`election_momentum` 是 party trigger。访问历史人物、IG、party 需先存在性/类型守卫；已解党、人物死亡、革命/失国后的延迟回复不能沿用悬空scope。[S7][S11]

### 4. 竞选、投票、组阁和界面

原版通常每4年选举，提前6个月竞选；初始势头随机0.5–1.5，党魁人气参与势头。党魁是党内clout最大的IG领袖；不是由剧情手工指定“阵营领袖”的名字自动对应。[S3][S4]

`on_monthly_pulse_country_elections` → 必要时 `initialize_electoral_confidence` → `elections_monthly_events` → `election_generic.1` 等竞选事件。该实际事件检查竞选中、至少两个活跃有成员党、非一党制与冷却；保存党scope，迟答时检查竞选是否仍在，option对存在的党 `add_momentum=momentum_large`。这提供时间、触发、选项、取消、scope保护的完整原生参考。[S14]

`on_election_campaign_start` 有自由选举传统的信任度恢复；`on_election_campaign_end` 有原生收尾但脚本中未写出完整票数分配算法；票数结算属于引擎。[S14] 原生概念说明选后提供一次不新增出阁激进派的政府改革；defines允许期限6个月，平常出阁激进化率参数0.25。不能简单说“每次大选自动让得票最多党执政”，也不能用剧情选项无代价反复重组政府。[S3][S4]

正常组阁会整党移动；党内任一IG参与持续革命或被镇压时有不能入阁提示。界面 `politics_panel_reform_government.gui` 直接读取 `GetPredictedLegitimacy` 与各级阈值，IG界面显示 `GetPartyAffiliationTooltip`。法国验收应比较原生预览与结算后的实际明细，不另造一个貌似准确的合法性计算器。[S12]

## 合法性组成、党鞭与数值边界

可证实的组成是：基础合法性；统治者IG在阁；政府总clout×法律系数；政府票份额×法律系数；超额政府实体惩罚；意识形态差异；其他国家修正。原版UI把超额 **party和独立IG** 分列，不能把三个同党IG机械数作三个政府实体。基础允许数+1，wealth voting再+1，因此不计其他修正的君主制财富投票允许两个实体；每个超额实体扣20。党内人数目标3与允许政府实体数不是同一约束。[S4][S5][S9][S12]

`INCOHERENCE_FACTOR=5`。当前概念说明差异来自政府IG意识形态与现行法律不相符，不能只检查“IG彼此理念相近”。原生明细按law/law group展示。党魁兼任党鞭，对其他同党IG用于差异计算的法律立场进行部分覆盖；基础 `country_party_whip_impact_add=0.5`，并非取消党内差异。具体立场聚合、最坏项选择与引擎取整未从脚本完整还原，最终以原生明细为准。[S3][S4][S9][S12]

税率还可贡献合法性：极低+10，低+5，中0，高−10，极高−20。这些值是来源明确的背景变量，不能忽略后把所有低合法性归咎于新党派。[S9]

**选举信任度是1.13.11必须纳入的层**：最高/默认定义1.0，实际初始化由 `eagle_burger_freedom_index` 设值。`low_electoral_confidence` 原生静态修正的最大基础量为合法性−50、选票力量−0.5、财富政治力量+0.5，注释明确按缺失信任度及 `country_electoral_confidence_impact_mult` 缩放。财富投票自身该倍率增量为−0.2；例如只有该法律影响且信任度为0，源码估算完整惩罚会按0.8缩放为−40合法性/−40%票力/+40%财富力量；实际受修正案等叠加，不能当法国实测读数。[S4][S5][S6][S9]

### 原生合法性档位与debuff

以下区间按整数UI读数表达；基础 `loyalties_gain` 不含额外国家 multiplier。源码注释称按月“multiply”，**不是每月凭空给全国总人口增加同百分比的激进派/效忠派**。[S8]

| 合法性L | 档位 | 静态效果 | 基础月度loyalties_gain |
| --- | --- | --- | --- |
| 0–24 | `illegitimate` | 政治运动产生激进派+50%；在野IG支持度−3；须有政治运动才可制定法律 | `(L−50)×0.0006`，0时−3.00%，24时−1.56%；趋近25时−1.50% |
| 25–49 | `unacceptable` | 政治运动产生激进派+25%；在野IG支持度−2；立法速度−25% | 同式，25时−1.50%，49时−0.06%；趋近50时0 |
| 50–74 | `contested` | 在野IG支持度−1 | 本档未定义loyalties_gain |
| 75–89 | `legitimate` | 政治运动产生效忠派+25% | `(L−74)×0.0005`，75时+0.05%，89时+0.75% |
| 90–100 | `righteous` | 政治运动产生效忠派+33%；立法速度+25% | 同式，90时+0.80%，100时+1.30% |

负档乘 `max(0,1+country_radicals_from_legitimacy_mult)`，正档乘 `max(0,1+country_loyalists_from_legitimacy_mult)`；脚本末尾 `max=1` 是上限1，与之前`min=0`的下限不能读反。政治运动产生激进派倍率与`loyalties_gain`是两条不同渠道，不应相加成一个“全国月增激进派百分比”。最低档没有再写−25%速度，而是运动立法门槛；不要从旧版本印象补上未见的修正。

## 当前MOD覆盖与法国开局

本次枚举：MOD没有 `common/parties`、`common/legitimacy_levels`；`common/defines`只有`ce_graphics.txt`，未发现本报告相关政治defines覆盖；没有覆盖`00_code_static_modifiers.txt`。MOD保留同名`00_scripted_triggers.txt`，投票权trigger段落与原版相同。因而本报告所列党派/档位/关键defines仍为原生基线；没有证明所有其他玩法脚本都永远不加政治修正。[M3]

当前法国历史开局设置君主制、财富投票，地主/军方/实业家在阁；地主改名拿破仑派别，并设置 `ce_france_support_napoleon`、`bonapartist_restoration_var` 等剧情变量。改IG名称与设置国家变量不等于改变党籍。[M1]

开局另带两个必须入账的修正案：[M1][S15]

- `amendment_200_franc_suffrage`：资本家政治力量+15%，财富门槛+10，基本票力−5，权威+50。财富投票基线因而成为财富门槛20+10=30、基本票力50−5=45（仅计这两来源）；不能用财富门槛20推演本MOD法国开局选民。
- `amendment_tradition_of_free_elections`：禁止选举舞弊、基础合法性+10，另有专制等法案通过率惩罚；竞选开始存在信任度恢复。原版历史注释有七月王朝语境，但本MOD的架空帝国设计不能仅因沿用了这些机制而自动改回原版历史。

`ce_french_empire_journal_effects.txt`当前自定义稳定度计入人物popularity、IG clout（在阁×2）及法律等因素；`ce_event_modifiers.txt`中的`FRA_ORL_popularity`与`FRA_BOR_popularity`是人物人气+25。它们是剧情稳定计算与人物修正，不是原生党票、clout或合法性setter。未来重构须说明保留/替换的计分层，避免同一人气经“自定义稳定+党魁势头+IG吸引力”多次受益却未计入平衡。[M2]

## 法国实施前设计约束

以下是研究导出的建议约束，不是已经实现的功能。其中党派定义/刷新条目仅在以后确需修改党派时适用；本轮不增加党派设计任务。

1. 为每党建立“可入IG集合、核心IG、共同支持的当前/目标法律、领袖意识形态例外、退出条件”的矩阵。目标每党1–3IG，但只能把≤3写成预期与测试要求，不能称引擎自然保证。尤其核原生法国军方+10、王朝互斥−5及其他党竞争。
2. 法国专属资格最好由开局国家范围确定；运行期路线变化放`available_for_interest_group`与`join_weight`。旧档若需增加全新党，`valid_for_country`开局一次是明确风险，先做一次最小原生旧档探针，不承诺自动迁移。
3. 常规政治目标只检查目标IG执政及合法性至少50。禁止检测党派组合、党内人数、同党关系和具体组阁排列；原生整党规则由引擎负责，不再叠加任务条件。若故事只要求支持而非政府席位，不强加执政门槛。
4. 共同法律立场要核两层：IG固有意识形态与领袖意识形态；还要核法国现行法律。只因同属某王朝而把互不相容的IG塞进同党，党鞭并不会清除所有合法性成本。
5. 换人物/意识形态/路线变量后，可依caudillo实例调用一次`update_party_support`；先保存需要的国家/对象scope，再按最终党籍重新解析。不要在同一循环内假设刷新前的party成员表、party领袖或scope仍有效。日常自然刷新频率未证实，勿周期强制分配掩盖设计错误。
6. 评分人数限制放完整算式的最后，避免后续加分重新越过入党阈值；仍需检验强行`add_ig_to_party`、一党制、革命国家、旧档和人物更替路径。评分静态通过只证算式，不证全局分配结果。
7. 不以人物人气或自定义稳定度触发“选举胜利”；需要选举结果时读取/观察真实党票与政府状态。任何人为保证某党获胜的设计须显式说明其与选举信任度/自由选举修正案的关系，不能悄然按剧情分数覆盖。
8. 常规执政目标按作者要求采用50。75或90仅是原生较高档位，不能据此升级常规任务门槛；只有有意困难的目标才另设更高值，并说明可控手段、期限、其他前置和回报。低合法性通常暂停相应行动，不自动判整个后继路线失败。

## 闭包测试计划

以下是未来实际修改对应层时才运行的开发验证，不是游戏任务条件；党派定义未改时不为法国JE另跑整套分党测试。本轮未执行实机测试。政治目标必须补查49/50/51以及相同执政/合法性而党籍不同的情况，确认没有隐藏组合门槛。

| 层/场景 | 必须记录的输入与观察 | 通过条件与反例 |
| --- | --- | --- |
| 数据库/资源闭包 | 国家资格、科技、图标、本地化、party/IG/ideology/law符号；`valid_for_country`与运行期条件分离 | 零缺失引用；国外党派不受法国变量误影响。反例：给不存在党加成员应被外部检查拦截。 |
| 完整评分边界 | 每IG每党，`scope:number=0/1/2/3/4`，强势/非强势/边缘，各路线、君主/共和、人物意识形态 | 枚举完整有序算式；第四成员分数不得因后置加分恢复。零分与0.5/1阈值单独列出；不据此宣称引擎分配通过。 |
| 新开局资格 | 架空法国开局、既有投票权和两项修正案、8IG势力与领袖 | party可用性、实际成员、党魁、票力、clout、合法性分项保存。确认设计每党≤3。 |
| 旧档资格/迁移 | 原存档缺新party数据库资格、已有party/票数/政府 | 验证新增类型是否可用；若不行明确仅新局或制定已证迁移，不靠刷新口头保证。 |
| 领袖/路线变更 | 党魁死亡、IG领袖更换、意识形态变更、变量切换 | 刷新前/立即后/自然周期后党籍一致；无失效scope；不能让全部IG周期性反复跳党。 |
| 有票/无票切换 | 财富/资格/普选→专制/寡头→恢复选举；另测一党制 | 原生党派消失/重现、票数、修正案清理、信任度、政府成员均合预期；不重复领选举/剧情奖励。 |
| 组阁闭包 | 一个目标IG带1/2位同党成员；独立IG；2/3个政府实体；有人被镇压/支持革命 | UI整党入阁、预览与实际合法性一致；超过实体数按原生明细解释；禁止入阁分支不死锁剧情。 |
| 合法性分界 | 0、24、25、49、50、74、75、89、90、100及修正跨界 | 25以下运动立法门槛、在野支持度、速度/运动激进派修正按档切换；检查自定义提示不写错。 |
| 选举结算 | 两党以上、党魁人气低/高、竞选事件、信任度高/低 | 势头只在竞选有效；票力、票份额与IG clout分开存；选后票数保留和势头结束；不宣称必定按人气赢。 |
| 中途改党 | 选前、竞选中、选后分别入党/退党/解党/刷新 | 实测选票政治力量如何重分、政府整党状态如何校正，保存精确日时序；此项当前引擎未决。 |
| 出口/迟答 | 党已解散、IG边缘化、角色死亡、国家被吞并/革命分裂、法改变、读档 | 事件取消或安全重选目标；没有悬空party/character scope、双重结算或永久modifier。 |
| 法律一致性 | 每党现行法律与目标法律矩阵、党鞭前后分项 | 使用原生差异tooltip核实，不以党名相近视作一致；党魁换人后再观察。 |

## 来源索引

- **S1** [GAME保守党](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/parties/conservative_party.txt:479>)：479–503资格；505–511 root/number/基础；549–613保守加分；668–682普选；1001–1039人数倍率；1040–1117王朝竞争；1118–1138法国军方加分；1184–1194caudillo变量。
- **S2** [GAME自由党](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/parties/liberal_party.txt:388>)：388–426资源/科技/开局有效性/IG资格；428–435root/number/基础；505–521进步领袖；1220–1258人数倍率。
- **S3** [原版机制概念](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:2432>)：48党鞭；851票；854clout；1004合法性；1021意识形态差异；1445政治力量；1874选举；2277人气；2287势头；2432党、票力分配和整党入阁；2436党魁；2734选举信任度。
- **S4** [原版defines](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt:297>)：189–198强势/边缘/入党人口；297–309竞选/人气/阈值/改革；320–323差异与规模；1813–1819人气范围。
- **S5** [权力分配法律](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_distribution_of_power.txt:606>)：30–32专制；261–264寡头；606–667地主选举；745–804财富；886–945资格；1017–1072普选；1301–1311一党。另见[政体法律](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt:74>)74–78君主制、516–519议会共和。
- **S6** [投票权trigger](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt:16>)16–40；[党派出现/消失effect](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_scripted_effects.txt:274>)274–292；[信任度初始化](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:2528>)2528–2555、2558起清理投票修正；指数见[ideology_values](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/script_values/ideology_values.txt:1402>)。
- **S7** [本机引擎effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:213>)：213–219加IG；316–318势头；411–414入阁；574–579选举；1195–1198解党；36539–36545退党；36630–36633出阁；37049–37058选举日期/唯一党；37109–37112执政党；37363–37371解除唯一党/刷新。
- **S8** [合法性五档](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/legitimacy_levels/00_legitimacy_levels.txt:1>)1–96完整文件：1/24/47/55/76各档；各档`modifier`及`loyalties_gain`为实际数值来源。
- **S9** [基础、税率和低信任度](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_code_static_modifiers.txt:14>)14政府数；73党鞭；313–348税率；976–982低信任度。modifier元数据见[00_modifier_types](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/00_modifier_types.txt:979>)979–1064。
- **S10** [引擎modifier说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/modifiers.log:1199>)1199–1208 IG政治力量/吸引力；307人气；739–767合法性；903党鞭；1135–1147票权。具名IG说明见[modifiers本地化](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/modifiers_l_english.yml:389>)389–404。
- **S11** [本机引擎triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:9968>)：93活跃党；2009成员；2072潜在党；9706势头；9968合法性；10602–10614党籍；11046–11055clout与政府份额；11089竞选；12096党籍；12178类型；13519–13527职业/宗教/文化政治力量份额。
- **S12** [原生界面说明](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/interfaces_l_english.yml:913>)913–946合法性各分项；7917–7918禁止入阁；10125–10133票力/党籍分数。UI见[组阁页面](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/politics_panel_reform_government.gui:389>)389–494预测合法性、743/875整党按钮，以及[IG页面](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/interest_group_panel.gui:316>)316–318党籍tooltip。
- **S13** [caudillo实际刷新调用](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/brazil/caudillo.txt:403>)403–425设变量再刷新；原版保守党读取变量见S1。
- **S14** [原生选举on_actions](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:1921>)1921–1935月度；7321–7369竞选开始/结束/改组；[选举随机事件入口](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_on_actions_election.txt:1>)1–14；[实际竞选事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/election_events/election_generic_events.txt:23>)23–115。
- **S15** [两项法国选举修正案](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/amendments/00_amendments_historical_04.txt:108>)108–132二百法郎；429–449自由选举传统。
- **M1** [MOD法国历史](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/FRA - France.txt:13>)13–39法律与二百法郎；57–73入阁/IG名；83–89自由选举；99–112剧情变量。
- **M2** [MOD法国稳定度effects](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/ce_french_empire_journal_effects.txt:80>)80–126人物人气、144–204clout和在阁加权；[人物人气修正](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/ce_event_modifiers.txt:380>)380–387。
- **M3** [MOD投票权trigger](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/00_scripted_triggers.txt:16>)16–40；目录枚举结果见本报告“当前MOD覆盖”。

引用核验：29条本地来源链接均存在，所引用起始行均在文件范围内；只证明可定位，不是游戏运行验证。原版三个关键来源SHA-256：`conservative_party.txt = 6aa468990bacd9423d34bc0d54b6ee1b6cdf415aacb8bb9316d0725c9a4a84fb`；`liberal_party.txt = 24517a25ac1be81a4ef532b1a535f16bcf2d815f8d8079b2e9ee36a8930fea20`；`00_legitimacy_levels.txt = 7aa7ecc0df54f798dd26847cb02d57b61bbc92b762eadfadfe672f8dbd7cd4e7`。GAME与MOD投票权trigger第16–40行规范化换行后SHA均为`dac3ab7ebfe1b98d88d96e57cd9d39ba44ec9347564e1dcf838146b1a742cd87`。

技能维护复核：本轮新证据为本机党派开局有效性、人数评分位置与1.13选举信任度/党鞭，应先随本报告供父任务方案使用；本子任务未修改技能或项目规则，未把研究发现冒充新实现或引擎验收。
