# AI 倾向设计：策略、信心、按钮权重与集体敌意

> 何时读：要让某国 AI 在某段时期更进取、更克制、必然推进某步、或对某类国家集体敌视；写 `ai_chance`、`ai_strategy`、秘密目标、条约 AI 时。不必读：只写玩家按钮、AI 不会遇到的内容。

依据：1.15.1 原版。完整出处、六条玩家说法的核实结论见 `WORK/research/2026-11-14-ai-tendency/report.md`。下文 `DS` = `GAME/common/ai_strategies/00_default_strategy.txt`，`ASV` = `GAME/common/script_values/ai_script_values.txt`，`NAI` = `GAME/common/defines/00_ai.txt`。

## 1. 先懂四个量

| 量 | 含义 | 基础值 | 叠加规则 |
|---|---|---|---|
| `aggression` | 对 `scope:target_country` 主动开博弈的倾向 | 0.5 | 各策略相加（DS:4379） |
| `recklessness` | 乘在自估兵力上；2 = 自认两倍，半数兵力也敢打 | 1 | 相加（DS:3923） |
| `diplomatic_play_boldness` | 博弈中不肯退让；`scope:diplomatic_play` 可用 | 50 | 相加（DS:1256） |
| `diplomatic_play_support` | 中立国站哪边；`scope:country`/`scope:enemy_country`；**每个加项必须写 `desc`** | 0 | 相加（DS:208-215） |

- 国家有默认策略 + admin/diplomatic/political 各一条；`set_strategy` 可直接指定；否则按 `weight` 加随机因子在“变更点数”满 100 时重抽（NAI:38-47）。
- 已承认国家互攻默认 ×0.15（DS:5517），除非目标在 `has_je_conquest_reason`（`GAME/common/scripted_triggers/00_ai_triggers.txt:230`）或系统性理由（宣称、家园、宿敌，同文件 :834）里。**想让 AI 真的开战，必须把日志加进 `has_je_conquest_reason`**。
- 策略块里的 `multiply` 只乘本块已累计的值，不乘其他策略的加项（ASV:46 注释）。要“绝不”，用大负数 `add` 或同时在活跃策略里处理。
- 本 MOD 整文件覆盖了 `00_default_strategy.txt`。默认策略只有 `ai_strategy_default` 一个对象（约 11,300 行），用 `REPLACE:` 也得整份复制；它由 define `DEFAULT_STRATEGY_STRING` 指定，`possible = { always = no }` 关不掉它。所以改默认策略只改 MOD 副本，版本更新时重新合并。AI 触发器改用 `common/scripted_triggers/ce_ai_triggers.txt`，按键 `REPLACE:`，要加征服理由就改这里（[vanilla-overrides](../lookup/vanilla-overrides.md)）。

## 2. 模式

### 2.1 路线专属策略（普鲁士统一型）

何时：某国在某段路线里要持续进取或持续克制，且影响面超过一两个目标。原版 `ai_strategy_unify_germany`（`02_diplomatic_strategies.txt:1701`）：aggression 基础 −2.0，研究征兵办公室后对候选国 +10，军队规模 ×2（ASV:249-254），秘密目标 conquer/dominate 1000。

```
ai_strategy_nesnd_<路线> = {
	icon = "gfx/interface/icons/ai_strategy_icons/territorial_expansion.dds"
	type = diplomatic                         # 会顶掉该国原有的外交策略
	possible = { c:SHA ?= this has_journal_entry = <日志> }
	weight = { value = 250 }                  # 原版 prussia_of_the_balkans 量级
	aggression = {
		value = -2.0                          # 闸门未开：抵消默认 0.5，不主动开战
		if = { limit = { <闸门> = yes scope:target_country = { <目标> } } add = 5 }
	}
	diplomatic_play_boldness = { value = 25 }
	secret_goal_scores = {
		conquer = { trigger = { scope:target_country = { <目标> } } score = { value = 1000 } }
	}
}
```
未写的字段沿用默认策略。想扩军，只能改 `wanted_army_size_script_value`（ASV:146，同名覆盖）或给 `building_group_weights = { bg_army = 1.5 }`。风险：×2 扩军会吃空财政；抢走原外交策略后，其他外交行为也会变。检查：观察者局看策略名（外交面板）与兵营数。

### 2.2 日志期间的定向信心（昭昭天命型）

何时：日志存在期间，对特定地区的拥有者要敢打。原版美国：recklessness +1（DS:4041）、aggression +5（DS:4617）、`wargoal_maneuvers_fraction` +0.25（DS:1500），加入 `has_je_conquest_reason`。在 MOD 的默认策略副本中，各块末尾加：

```
if = { # NESND <日志>
	limit = { has_journal_entry = <日志> scope:target_country = { <拥有目标州> } }
	add = 1
}
```
量级：常规 recklessness +0.5～1、aggression +2～5；必须发生的历史战争 recklessness +5～10、aggression +50～100（奥斯曼、鸦片战争）。风险：AI 带一半兵力去打强国。开日志前先确认对手已被削弱（见 §4 正例）。

### 2.3 时间或科技闸门

何时：一定要等某个条件成熟才开打，例如等对方先乱。做法：基础给负 aggression，闸门满足后大加（2.1 的 −2.0 → +10）；或 `revolution_aversion` 加日期条件（DS:131-151）。风险：闸门条件 AI 永远达不到，路线就会卡死；要有日志超时或其他推进办法。

### 2.4 按钮：必然、高频与严格

| 写法 | 效果 | 用于 |
|---|---|---|
| `autocomplete = yes` | 条件满足就自动执行，**玩家也一样**（`scripted_buttons.md:73`；`08_tsarpoints_buttons.txt:681`） | 不该让人选择的推进 |
| `ai_chance = { value = 100 }` | 每次评估权重高，不保证执行 | AI 应尽快做的事 |
| `value = 0` 起、`if/else_if` 分档 | 只在急迫时点 | 让步、花钱、改变身份 |

按钮的 `ai_chance` 是 script value 形状，事件选项是 `base/modifier` 形状，两者不能互相移植（[engine-facts](../lookup/engine-facts.md#按钮事件与-ai-权重)）。AI 评估按钮的频率在源码中找不到，概率表只能当量级参考。

### 2.5 绝不退让或绝不开战

原版：太平天国 boldness +1000（DS:1294），东印度公司对宗主 aggression ×0，尼古拉一世对中国 ×0，秘密目标同步排除（DS:5464、:9622）。注意 §1 的 multiply 限制。风险：盟友被拖进必败战争；生存内容卡住。

### 2.6 对某类国家的集体敌意（无产阶级国家型）

何时：某种政体或身份应当遭到全世界孤立，而且敌意要能随进度增减。原版部件：
1. 修正类型，挂在**目标国**上：`country_other_country_socialist_*_hostility_impact_{add,mult}`，`script_only = yes`（`modifier_type_definitions/14_ip5_script_modifiers.txt:29`）。
2. 来源：法律 `modifier` add 50；日志 `scaling_modifiers_while_active = { modifier = X value = <条进度> }` 让 mult 随进度增长（`journal_entries/00_communism.txt:396`）；和解结局给 mult −0.5。
3. 默认策略各处读 `scope:target_country.modifier:<类型>`：support −100（DS:1022）、aggression +5×(1+mult)（DS:5358）、befriend 乘至 0、antagonize ×2、政权更迭 +100；`static_treaty_acceptance` 扣分，到期后 AI 退约。

恶名（国际弃民，≥100）则主要靠 defines：同情 +100（NAI:366）、威胁 ×1000（NAI:1067），再加脚本里大国 aggression +100（DS:4429）、遏制博弈 `dp_contain_threat`。defines 只能全局调，不能分国家。风险：全局敌意会波及无关国家；必须给玩家留和解路线。

### 2.7 升级阶梯

原版海地债务：法国对海地的 aggression 随修正等级 1→4 依次为 5、10、50、1000（DS:4640）。玩家能从修正等级读出风险，还有回头的机会。适合“拖得越久越危险”的外交僵局。

### 2.8 历史关系预设，之后自然衰减

`history/treaties` 用 `binding_period` 写约束期（神圣同盟 35 年），`history/ai` 用 `set_secret_goal = { country = c:X secret_goal = befriend }` 设开局目标；到期后交给通用评估：约束期外接受分 ≤ −50 就退约（NAI:1207）。本 MOD 实例：`common/history/ai/nesnd_hus_initial_goal_overrides.txt`。不要按月强制覆写外交目标。

## 3. 可控与写死

- **脚本**：策略全部字段、`set_strategy`、`set_secret_goal`、按钮和决议的 `ai_chance` 与 `autocomplete`、法律 `ai_will_do`、条约条款 `ai` 块、`static_treaty_acceptance`、催化剂 `ai_country_goal_recalculation`、`script_only` 修正、AI script value。
- **defines**（全局）：恶名阈值 25/50/100（`00_defines.txt:989`）、同情、威胁、遏制、统一倍率 ×20（NAI:56）、退约阈值、策略重抽速率。
- **写死**：策略抽取算法、兵力与信心的公式、何时评估发起博弈和选边、秘密目标到态度的映射、遏制博弈的发起、按钮评估频率、前线 AI。只能通过上面两层的值间接影响。
- 引擎发起的统一、领导权、遏制博弈没有 `ai_chance`。原版的敌意都不区分玩家，只有游戏规则“严苛 AI”对玩家同情 −25。

## 4. 本 MOD 的正反例

- **正：先煽动，看到乱局再解锁。** 登莱开局很弱，凡是要动武的环节，先用按钮或进度条煽动目标国内部的原生运动，检测到对方真的陷入乱局（运动爆发、起义、内战）后才给 aggression 和 recklessness。**反**：日志一开就给登莱 +5 aggression 去打俄国，AI 会送死。
- **正：先比实力。** `script_values/nesnd_small_ai.txt` 先比兵力比、GDP 比或可靠外援，达标才给自治、独立的权重。
- **反：频繁重掷。** 三角贸易的 AI 每年重掷买卖身份，在途订单因此失效。现行做法是选边后锁定三个月，在途订单按原批次结算（`.scratch/triangle-trade/issues/03`）；“选边后永不重掷”作者不采纳（2026-11-14）。规则：AI 定期重掷时，已承诺的交易要按原双方结算，重掷后还要锁定一段时间。
- **正：让步按钮严格。** `common/scripted_buttons/nesnd_cne_concession.txt` 默认 0，按急迫程度分四档互斥；权力已偏向宠臣、改革临近完成时降权。规则：有代价的按钮，`ai_chance` 写成“只在需要时点”，并写清每一档的理由。

## 5. 检查

1. 每个加项的作用域写对：aggression/recklessness 用 `scope:target_country`，boldness 用 `scope:diplomatic_play`，support 用 `scope:country` 并写 `desc`。
2. 算一遍合计值：默认值 + 当前外交策略 + 新加项；正负号与目标量级要对得上 §2 的表。
3. 要开战的，确认日志已加进 `has_je_conquest_reason`。
4. 有闸门的，写出“闸门永远不开”时怎么推进。
5. 游戏内由作者在观察者局验证：策略名、秘密目标、博弈发起和选边。
