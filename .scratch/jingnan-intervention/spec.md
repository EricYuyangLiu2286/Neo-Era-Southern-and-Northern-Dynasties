# 第二次靖难的域外介入：参战奖励与吴军「军心」条（第二稿：已按作者答复修订，待确认后实施）

只交方案，不写脚本。作者确认后另开 `issues/01-implement.md`。路径都相对源目录；游戏版本 1.15.1 / 26591675，部署版本 `55b80fd0`。

## 0. 现状（每条附出处）

### 0.1 开战、入场、结束

1. **易代与应答期。** 吴明易代事件 `flavorUSM.400` 给 USM 开「南明内战」日志 `ce_usm_civilwar_journal`，同时发出 `nesnd_notify_foreign_countries`（`events/flavorUSM_ce.txt:684-687`）。日志最长 180 天，等南方各国答复；有反吴国就弹 `usm_civilwar.2`，没有就弹 `.3`「悄无声息的易代」（`common/journal_entries/ce_usm_the_last_days_of_ming.txt:333-392`）。
2. **开战。** `usm_civilwar.2` 对 USM 调用 `nesnd_open_southern_war`（`events/usm_civilwar_events.txt:296-302`），USM 的选项开「平叛」日志 `ce_usm_suppress_rebellion`（同文件 `:327-337`）。开战效果按 明廷受禅者→SIH→HNA→GNG→PHI→DEI→YN1→JAP 的顺序选反吴盟主，建 `dp_usm_civil_war` 博弈后立即 `set_war`（`common/scripted_effects/nesnd_crisis_effects.txt:189-347`，`set_war` 在 `:554`）。战争目标是吞并盟主 `wg_nesnd_usm_annex`，`mirror_war_goal = yes`、不许谈判和平（`common/diplomatic_plays/ce_diplomatic_plays.txt:1-4`；`common/war_goal_types/nesnd_usm_annex.txt:1-8`）。
3. **各方入场。** 反吴国及其非吴宗主由 `nesnd_call_jingnan_participant`/`nesnd_fulfil_jingnan_call` 拉进防守方（`nesnd_crisis_effects.txt:319-326、402-489`）。日本另有 `usm_civilwar.23` 三选一：助吴、反吴、中立（`usm_civilwar_events.txt:1825-1870`）。
4. **结束。**
   - 反吴盟主首都失守或被占八成：`usm_civilwar.4`，被吴 `annex_as_civil_war`（`usm_civilwar_events.txt:537`；周检查 `.5` 在 `:804-810`）。
   - 吴全胜：「平叛」完成 → `usm_civilwar.8`，`nesnd_south_settled`（`ce_usm_the_last_days_of_ming.txt:424-436`；`usm_civilwar_events.txt:830-866`）。
   - 僵持：`usm_civilwar.9` 设 `usm_civilwar_status_quo`，「平叛」日志继续，其「续战」条满 5 个月再开一轮（`usm_civilwar_events.txt:869-912`；`ce_usm_the_last_days_of_ming.txt:449-460`；`common/scripted_progress_bars/nesnd_jingnan_continuation.txt:1-14`）。
   - 吴失大陆：「平叛」失败结局 → `nesnd_celestial_collapse.1`（`ce_usm_the_last_days_of_ming.txt:404-422`）。
   - 反吴方胜：`ce_usm_restoration_of_ming`/`ce_usm_acheive_revolution` 完成 → `usm_civilwar.10`，胜者经 `nesnd_commit_rebel_settlement` 吞并大吴并 `change_tag = USM`（`ce_usm_the_last_days_of_ming.txt:493-500`；`common/scripted_effects/nesnd_south_settlement.txt:1-31`）。其余反吴国走 `.11`。
   - 蜀国投降（任务 shu-jingnan 的 A1）：`nesnd_sih_surrendered` 关闭反吴日志（`ce_usm_the_last_days_of_ming.txt:507`）。

v3tree 邻居查询（用 `reports/2026-11-16-cne-journals/v3tree-config.json` 的索引）核对了 `wg_nesnd_usm_annex`、`nesnd_north_intervention`、`nesnd_joined_south_play`、`ce_usm_civilwar_journal` 四个节点，上面各条与索引的边一致。

### 0.2 现在哪些域外国家能参战

| 国家 | 入口 | 能否真正参战 |
|---|---|---|
| 中华帝国 CNE | `nesnd_crisis.20`「伪朝禅代」，易代时弹出，一局一次（`events/nesnd_crisis_events.txt:14-90`）。c 项「准备南下」设 `nesnd_north_intervention`，加 60 个月 `nesnd_foreign_commitment`（军饷 +10%、权威 −5%，`common/static_modifiers/nesnd_crisis_modifiers.txt:128-132`），地权革命中失序 +15。须独立、未在战、有官僚、未破产；AI 权重 65/25/10。 | **能。** 开战时 `nesnd_open_southern_war` 让带旗的 CNE 加入（`nesnd_crisis_effects.txt:333-341`，条件在 `:337`），之后每月 `nesnd_crisis_monthly` 补入新一轮（`common/on_actions/nesnd_crisis_on_actions.txt:5`）。走 `join_war` 站反吴方（`nesnd_crisis_effects.txt:459`；记下所入之战在 `:472`）。 |
| 日本 JAP | `usm_civilwar.23` | 能，作反吴国（`usm_opposition_country`）或助吴。已有自己的分封与吞并链（`common/scripted_effects/nesnd_japan_recovery.txt:291-339`），本方案不动。 |
| 反吴国的外国宗主 | 开战时自动召入（`nesnd_crisis_effects.txt:322-324`） | 能，但只在蜀、楚等已附从外国时出现。 |
| 西秦 QE1、东洲 HUS、登莱 SHA、法、英、俄、缅、莫卧儿 | `nesnd_external.1` →「外交议程」日志 `nesnd_external_policy`（`events/nesnd_external_events.txt:3-15`；`common/journal_entries/nesnd_external_journal.txt:1-57`） | **不能。** 只能选对象、送钱或送械（按钮见 `common/scripted_buttons/nesnd_external_buttons.txt`）。西秦专有「联络川中」（`:43-60`）。 |
| 其他国家 | 博弈的 `additional_involvement_trigger` 允许任何可发起侵略博弈的非 CNE 国家（`ce_diplomatic_plays.txt:21-46`） | 实际上没有机会：博弈建好后同一效果里就 `set_war`，没有表态期。 |

### 0.3 CNE 参战后现在实际会发生什么

- 以普通参战国站在反吴方，**自己没有任何战争目标**。博弈只有吴对盟主的吞并目标和镜像目标，`join_war` 不加目标。
- 吴胜：盟主被吞并，战争结束，CNE 不割地不赔款，也无罚则。
- 反吴方胜：胜者吞并大吴，结算里对 CNE 只移除 `nesnd_north_intervention`（`nesnd_south_settlement.txt:25`）。僵持时同样只移除旗（`usm_civilwar_events.txt:893-895`）。
- 附带：登莱「登莱旧部」条在 CNE 带此旗时每月 +0.5（`common/scripted_progress_bars/nesnd_sha_shandong.txt:14`）。
- 结论：CNE 参战只付出 60 个月的军饷、权威和失序，得不到领土、附庸、条约或修正。

### 0.4 设定依据（只引原文）

- PPET 第 27 页第 19 段：1850 年末牧仲棠派费西翼、岳华兴南进，在**徐淮**被左宗棠截击败退；又派军**入汉中支援魏鉴的蜀国政权**，被曾国藩、吴直弼击败。
- PPET 第 27 页第 10 段：1839 年南明北华在江上签和平协议，邦交正常化、相互承认。
- PPET 第 17 页第 11 段：天演帝登基，“从极东洲到西极英蒽兰，列国纷纷遣使闻讯”。第 13 段：吴军（含井伊直弼的倭军）三年平乱，破成都、重庆后烧杀，西南人骂“倭吴”。
- PPET 第 13 页第 10–12 段：秦军残部退守伊犁称“西秦”；此后西秦“再不敢言东征”，转与俄、波斯、莫卧儿争西亚。第 12 页第 17 段：1820 年西秦曾“开始发力”（原文截断）。
- PPET 第 29 页：1896 年《牛镇条约》，中华帝国割汉中等地予吴，并“归还鄯州于西秦”。
- 世界书 `wu-succession` 条（出处 PPET 第 17 页）与上同。PPET 没有写东洲、登莱、英法俄在靖难中的动作；下文凡涉及它们的需求都标为“代理推断”。

## 1. 我对作者第 3、4 条的理解

- 第 3 条：给真正出兵的域外国家一条“战后讨账”路线。原版没有参战国自带战争目标的入口，所以奖励在战后由胜者兑现。
- 第 4 条：域外介入越多，吴军越能把内战说成抗外，军心越高；没人介入时是同室操戈，军心低且随战事拖延下滑。条值缩放吴军进攻、防御、士气（用士气损失表示）、军需品花费四项。

## 2. 内容树

```
[现有] flavorUSM.400 → ce_usm_civilwar_journal（≤180 天）→ usm_civilwar.2 开战
  ├─ [现有] CNE：nesnd_crisis.20.c → nesnd_north_intervention → 入战（不改）
  ├─ [新] 西秦、东洲：nesnd_external.1 为 QE1、HUS 各加一项「出兵」→ 设 nesnd_jingnan_intervener
  │        与 CNE 同样经 nesnd_join_opposition_play 入战；外交议程日志照旧可开
  └─ [新] 统一的入战标记：凡经上两条入战的国家，入战时记 nesnd_jingnan_intervener_play = 该战博弈
[改] ce_usm_suppress_rebellion（大吴「平叛」，作者原作）
  └─ [新] 第二条进度条 nesnd_wu_resolve_bar「军心」0–100，起点 30
        ├─ monthly_progress（唯一写入者，见第 4 节）
        ├─ on_monthly_pulse：按条值重挂一个缩放修正（高于 50 挂「同仇」，低于 50 挂「离心」）
        └─ 三个结局与 hidden invalid：移除两个修正
[新] 奖励结算：nesnd_jingnan_aid.1「酬谢外援」
  ├─ 触发：nesnd_commit_rebel_settlement 末尾，对每个战末仍在反吴方的介入国，由胜者（新 USM）收到
  ├─ a 依约酬谢（AI 70）：按国家给第 3 节的推荐奖励
  ├─ b 只给名分（AI 30）：只给声望与关系，介入国得到对胜者的「背约」关系惩罚
  └─ 介入国收到 nesnd_jingnan_aid.2 通知结果（一个选项）
[新] 僵持（usm_civilwar.9）：介入国什么都不得（作者 2026-11-16）
[新] 吴胜（usm_civilwar.8）：吴得到对介入国的宣称，介入国按国力付 5 年赔款（第 6 节）
```

规模：1 个现有日志加 1 条进度条和 2 个修正，2 个新事件，1 个新事件选项，约 4 个 scripted effect/trigger。属内容形状 B（计时压力）的一条条加一组结局事件。

## 3. 域外国家奖励推荐表

“原生机制”一栏都已在 1.15.1 的 `docs/effects.log` 或 GAME 文件里查到：`create_treaty`（:1076）、`set_owes_obligation_to`（:33667）、`set_state_owner`（:33754）、`create_bidirectional_truce`（:853）、`add_claim`（:78）；条约条款 `GAME/common/treaty_articles/` 的 `06_transfer_state`、`07_foreign_investment_rights`、`14_treaty_port`、`24_transit_rights`、`25_trade_privilege`。

| 国家 | 设定上的需求与动机 | 可行奖励（原生实现） | 推荐与理由 | 风险 |
|---|---|---|---|---|
| **中华帝国 CNE** | 南征统一、削吴（PPET 27:19 的两路出兵：东路徐淮，西路入汉中援魏鉴）；1839 年江上和约、相互承认（PPET 27:10）。 | ① **苏北**（`STATE_JIANGSU`，徐淮一线，开局属吴）：胜者 `set_state_owner` 给 CNE，或用 `transfer_state` 条款。② 胜者欠 CNE 一个人情：`set_owes_obligation_to`。③ 十年停战：`create_bidirectional_truce = { months = 120 }`。④ 投资权与贸易特权条约：`foreign_investment_rights`、`trade_privilege`，`create_treaty` 约束期 10 年。⑤ 地权革命完成度 `cne_landreform_completion_tracker` +10。⑥ 附庸：`make_subject`/条约，**不推荐**。 | **东路（默认）：** ③ + ⑤；战末 CNE 占着苏北时再加 ①，没占着时改给苏北宣称（`add_claim`）。**胜者为蜀或大汉时（西路）：** 改为 ② + ④ + ③ + ⑤，不割苏北。理由：东西两路各对应原文一次出兵，割地只发生在 CNE 自己打的那一路。附庸与大汉独立、「统一南方」要求 `is_subject = no`（`common/scripted_triggers/nesnd_unify_south.txt:50`）直接冲突。 | 苏北是「统一南方」26 州之一（`nesnd_unify_south.txt:30`）。割给 CNE 后胜者要再打北朝才能完成该日志，这本身是剧情张力，也可能让日志长期挂着（问 2）。AI CNE 选 c 只有 10%，滥用风险低；割地以战末占领为条件，玩家 CNE 不能只挂名参战就拿到苏北；其余奖励也只给战末仍在战的介入国。 |
| **西秦 QE1** | 原文：东征已绝，重心在西亚（PPET 13:12）；其失地鄯州在中华帝国手里（PPET 29）。与蜀的往来只见于代理写的外交议程文本（`nesnd_external_l_simp_chinese.yml:11`，非原文）。 | ① 胜者与西秦的贸易特权、过境权条约：`trade_privilege`、`transit_rights`。② 胜者欠人情：`set_owes_obligation_to`。③ 胜者每周向西秦送茶（`goods_transfer`，g:tea）。④ 领土：西秦的青海、拉萨与川西相邻，但 26 州里没有可割而不伤蜀的州，**不推荐**。⑤ 鄯州：与本战无关，**不做**。 | ① + ②。理由：原文不支持西秦求地；给商路和人情，代价小，不碰大汉路线。③ 有趣但需要市场接入与运力，冻结条件多（见技能 `lookup/native-treaty-aid.md`），留作可选。 | 西秦出兵与原文“不敢言东征”相左，所以入口只给玩家与低 AI 权重（建议 AI 5%）。西秦未必有通路进川，AI 入战后可能不出兵，却让吴军心上涨（这对吴有利，不算漏洞）。 |
| **日本 JAP** | 已有反吴、助吴两线及战后分封（`usm_civilwar_events.txt:1825-1870`；`nesnd_japan_recovery.txt:291-339`）。 | 现有。 | **不加。** 反吴的日本是 `usm_opposition_country`，按反吴国处理。 | 无。 |
| **反吴国的外国宗主** | 原文无。 | 宗属关系本已保留。 | **不加奖励**，但计入军心条的域外国家数。 | 无。 |
| **登莱 SHA、英法俄、缅、莫卧儿** | 原文只有“列国遣使”（PPET 17:11）。现只能援钱援械。 | — | **本轮不开参战入口，也不加奖励。** 外交议程日志行为不变。东洲已改为开放，见第 6 节。 | 开放给 AI 列强后，第一次靖难常被大国卷入，脱离设定。 |

## 4. 吴军「军心」条

### 4.1 挂在哪里

| 方案 | 优点 | 缺点 |
|---|---|---|
| **A 挂在「平叛」`ce_usm_suppress_rebellion`（推荐）** | 只属吴；开战即开，吴全胜、吴失大陆、`nesnd_south_settled` 时结束，与“第二次靖难期间”完全一致；僵持后续战的几轮里条值延续，正好体现“拖得越久越低”。已有「续战」条，原版也有一日志多条（法国君主派三条）。 | 是作者原作日志，要在其中加一条进度条、一段月脉冲和四处清理。 |
| B 新建小日志 `nesnd_wu_resolve` | 不碰原作文件。 | 要复写一遍开启与结束条件；吴同时挂两个战时日志。 |

推荐 A。反吴方胜时吴被吞并，修正随国家消失，不需另外清理。

### 4.2 条值

- 记号：`N` = 当前站在吴敌方的域外国家的权重和，上限 4。域外国家指：在本轮靖难战争（`nesnd_south_named_play`）里与吴敌对、且没有 `usm_opposition_country` 的国家。权重：中华帝国 2，其余 1（问 1）。
- 范围 0–100，起点 30（作者给定）。
- 只在吴处于靖难战争时变化；两轮之间冻结。

每月变化（`monthly_progress` 的具名条目，唯一写入者）：

| 条目 | 数值 | 说明 |
|---|---|---|
| 同室操戈 | −1；本轮战争满 24 个月后 −1.5 | 无人介入时的基础下滑 |
| 外敌在境 | +1 × N | 介入越多涨得越快 |
| 新近介入 | 每个新加入的域外国家，加入后头 2 个月每月 +7.5 × 权重 | 合计中华帝国 +30、其余 +15，相当于“起点更高” |

几种局面（月数为开战后）：

| 局面 | N | 第 2 个月 | 第 12 个月 | 第 24 个月 | 第 36 个月 |
|---|---|---|---|---|---|
| 无人介入 | 0 | 28 | 18 | 6 | 0 |
| 只有西秦 | 1 | 45 | 45 | 45 | 39 |
| 只有中华帝国 | 2 | 62 | 72 | 84 | 90 |
| 中华帝国 + 西秦 | 3 | 79 | 99 | 100 | 100 |

### 4.3 四项如何缩放

`f = (条值 − 50) / 50`，取值 −1 到 +1。月脉冲先移除两个修正，再按 |f| 用 `add_modifier = { name = … multiplier = … }` 挂其中一个（原版写法见 `GAME/common/journal_entries/00_communism.txt:1194`）。修正键都已在 `docs/modifiers.log` 查到。

| 修正键（modifiers.log 行号） | 「同仇」f = +1 | 「离心」f = −1 | 起点 30 时 |
|---|---|---|---|
| `unit_offense_mult` 进攻（:2375） | +15% | −10% | −4% |
| `unit_defense_mult` 防御（:2327） | +15% | −5% | −2% |
| `unit_morale_loss_mult` 士气损失（:2355） | −20% | +25% | +10% |
| `country_military_goods_cost_mult` 军用商品花费（:871） | −15% | +10% | +4% |

参照：蜀军常驻修正是攻防 +20%、军用商品 −20%（`common/static_modifiers/nesnd_shu_army.txt:1-6`）。军心满条的吴军仍略弱于蜀军加成，吴靠兵力取胜。

### 4.4 出现、结束、清理

- 出现：USM 开「平叛」日志时（`usm_civilwar_events.txt:336`），条起点 30。
- 结束：日志三个结局（吴失大陆、吴全胜、hidden invalid）各调用一个清理效果，移除两个修正。每轮战争之间月脉冲也移除修正（条值保留）。
- 入战标记 `nesnd_jingnan_intervener_play` 与 `nesnd_jingnan_intervener` 在 `nesnd_commit_rebel_settlement`、`usm_civilwar.9`、`.8` 中与现有 `nesnd_north_intervention` 一起移除。

### 4.5 要改的文件（实施时）

- `common/journal_entries/ce_usm_the_last_days_of_ming.txt`：「平叛」加条、月脉冲、结局清理。
- 新建 `common/scripted_progress_bars/nesnd_wu_resolve.txt`、`common/static_modifiers/nesnd_wu_resolve.txt`、`common/script_values/nesnd_wu_resolve.txt`。
- `common/scripted_effects/nesnd_crisis_effects.txt`：`nesnd_join_opposition_play` 接受新标记；入战时记 `nesnd_jingnan_intervener_play`。
- `common/diplomatic_plays/ce_diplomatic_plays.txt`：`additional_involvement_trigger` 加新标记一行。
- `events/nesnd_external_events.txt`：`nesnd_external.1` 为西秦加一项。
- 新建 `events/nesnd_jingnan_aid.txt`（.1、.2）。
- `common/scripted_effects/nesnd_south_settlement.txt`、`events/usm_civilwar_events.txt`（.8、.9）：奖励与清理。
- 中英本地化 `nesnd_jingnan_aid_l_*.yml`，按 nesnd-player-writing 写。

### 4.6 引擎不确定处

- `add_modifier` 不带 `months` 时是否在月脉冲内移除再加不闪烁，要实测（静态无法确认）。
- 战末判断“仍在战”的时点：`usm_civilwar.10` 弹出时战争可能已因吞并结束。实施时在 `.10` 的 immediate 先把在战介入国记下，再在结算后发奖。
- **苏北的占领判定（2026-11-16 订正）。** 第一稿说查不到控制者判定，有误：1.15.1 的 `docs/event_targets.log:1990` 有 `controller` 链接（输入省份或州，输出国家）。原版用作作用域块，例如 `controller ?= { … NOT = { this = prev.owner } }`（`GAME/common/journal_entries/08_russia_provisional_government.txt:420`）。拟写法：在 `usm_civilwar.10` 的 immediate、吞并大吴之前判断 `s:STATE_JIANGSU = { any_scope_state = { controller ?= { this = c:CNE } } }`，结果记为变量，结算后再割。两处要实测：州级 `controller` 在部分省份被占时返回谁（若返回业主，改为逐省判断，“CNE 控制过半省份”即算占领）；`.10` 弹出时占领是否还在。所以割地改为看占领，第 3 节表与问 2 已随之修改。

## 5. 先问你（附推荐答案）——已答复，结论见第 6 节，以第 6 节为准

1. **权重与计数。** 中华帝国在军心条里算 2 个、其余 1 个，权重和上限 4；日本作反吴国时不算域外。推荐：照此。
2. **苏北。** 东路胜利时，中华帝国战末占着苏北才割给它，没占着只给宣称。割走后苏北就成了「统一南方」26 州里要从北朝收回的一州。推荐：按占领割（2026-11-16 修改：可以判断占领后，推荐从“东路胜利就割”改为“占着才割”，出兵徐淮的结果直接决定苏北归属）；若你不想让统一南方被卡住，改为一律只给宣称和十年停战。
3. **吴胜时的后果。** 现在介入国无罚则。推荐：吴得到中华帝国汉中、皖北的宣称（PPET 29 页吴后来取得汉中），西秦不受罚；不另加赔款。
4. **僵持（.9）时的奖励。** 推荐：只给非领土奖励的一半（人情、停战，不给苏北与条约）。
5. **西秦入口。** 只在 `nesnd_external.1` 给西秦加“出兵”一项，AI 权重 5%，花费与中华帝国 c 项相同（`nesnd_foreign_commitment` 60 个月）。东洲等国本轮不开入口。推荐：照此。


## 6. 作者答复（2026-11-16）

本节覆盖前文与之不符的地方。

| # | 答复 | 对方案的改动 |
|---|---|---|
| 1 | 中华帝国在军心条里算 2 个，其余 1 个，上限 4；日本反吴时不算域外。 | 第 4.2 节不变。 |
| 2 | 东路胜利（胜者不是蜀或大汉）时，中华帝国得**苏北、滁州、合肥**三州（`STATE_JIANGSU`、`STATE_CHUZHOU`、`STATE_SOUTHERN_ANHUI`），**不看占领**，三州全割。 | 第 3 节 CNE 东路改为：三州 + 十年停战 + 地权完成度 +10。第 4.6 节的占领判定不再需要。 |
| 2′ | 「统一南方」不再按 26 州计，只算八个要点：广州（`STATE_GUANGDONG`）、成都（`STATE_SICHUAN`）、重庆（`STATE_CHONGQING`）、长沙（`STATE_HUNAN`）、武汉（**只算** `STATE_EASTERN_HUBEI`）、南京（`STATE_NANJING`）、福建（`STATE_FUJIAN`）、宁国（赣北 `STATE_JIANGXI`，古称宁国府）。 | 割给中华帝国的三州都不在八要点内，统一南方不再被卡住。这是对 [shu-jingnan](../shu-jingnan/spec.md) 日志 `nesnd_unify_south` 的改动：`common/scripted_triggers/nesnd_unify_south.txt` 的州表、计数 `nesnd_unify_south_held < 26` 与条面 n/26 改为 n/8，开启时只对八州加宣称。实施时与本任务同批做。 |
| 3 | 吴胜时：吴得到中华帝国汉中、皖北的宣称；所有介入国（中华帝国、西秦、东洲）按国力付赔款，`money_transfer` 条约，每周付介入国周收入的 10%，约束期 5 年。 | 第 2 节树已改。赔款额在签约时按当时周收入算定，之后不变。 |
| 4 | 僵持（`.9`）时介入国什么都不得。 | 第 2 节树已改。 |
| 5 | 西秦、东洲都开出兵入口：`nesnd_external.1` 各加一项「出兵」，花费与中华帝国「准备南下」相同（`nesnd_foreign_commitment` 60 个月）。AI 权重沿用推荐的 5%（作者未另定）。 | 东洲奖励：反吴方胜时，胜者割一处**条约港**给东洲（`cede_treaty_port`，作用于州，割的是该州的一个港口省份，不是整州），另签 10 年贸易特权条约（`trade_privilege`）。条约港设在浙江（`STATE_ZHEJIANG`，作者 2026-11-16 定），不成时依次改福建、闽江、粤中（作者 2026-11-16 要求加退路）；写法照原版 `treaty_port` 条款，见 [01 实施](issues/01-implement.md)。东洲在军心条里算 1 个。 |

实施时待查：`cede_treaty_port` 对已有条约港或无港口的州的行为（`docs/effects.log:620`）；东洲是否已有通往福建的海路不影响割让，只影响它能否出兵。
