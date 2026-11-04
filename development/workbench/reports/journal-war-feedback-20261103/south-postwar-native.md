# 南明战后分支：当前链条与原生接口核对

2026-11-03；GAME 1.13.11 / build 24799966。只读研究，未改玩法、未启动游戏，`SOURCE_RESEARCH / ENGINE_NOT_RUN`。这里“已核接口”指当前引擎文档与实际原版实例，**不等于本轮实机验证**。

## 先给实现结论

1. 现有 `.9`把“本轮停战”与“整个南朝剧情终结”混在同一个全局`nesnd_south_settled`；`.11`又只支持叛军总胜利、改tag成为USM后的世界。不能直接给`.11`加第三按钮便认为覆盖吴仍在的停战。
2. 首都投降`.5`现在先随机杀死/流放成年人物，再吞并；皇帝必须在这些随机处置**之前**迁走，并从后续处置中明确排除。当前迁徙effect只处理起始USM、固定优先HNA再SIH，不能承担“行在再次陷落→随机任一存活拥明国”的新要求。
3. 存活拥明国集合决定是否还能继续，不能以蜀国存在/灭亡代替。现有`nesnd_ming_court`在非USM国家且status quo时，已有后继JE；新分支应保留这条继续抵抗出口。
4. **本机未核到**`skipcountdown`、`skip_countdown`、`set_liberty_desire`、`make_subject`。当前实际接口是`create_diplomatic_play`、`set_war`、`create_diplomatic_pact`、`change_subject_type`、`add_liberty_desire`、`end_truce`。不要把口语接口写成代码。
5. CNE接受归附必须是独立的接收国答复；真正创建附属关系前重验双方存在/存活、和平、未承诺外交博弈、申请者仍独立及请求身份。拒绝/失效/超时都落入明确后继，不能将CNE提前塞进战争backers。

## 当前MOD链与锁

| 位置 | 实际行为 | 本轮设计影响 |
| --- | --- | --- |
| [usm_civilwar.9:1294–1332](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1294>) | trigger排除已总胜利/败退处理中/本国`nesnd_status_quo_seen`；immediate设本国seen、全局`usm_civilwar_status_quo`和`nesnd_south_settled`，移除CNE干预标记；option给衰败修正 | `.9`没有执行和约或停战，是**确认/标记结果**，不是创造和平的effect。不要在其他拥明国仍同USM交战时调用。不能把每国seen当成全局只有一次。 |
| [主JE:339–364](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:339>) | 完全没有存活独立反对国才算镇压完成；无带内战标记博弈且没有反对国与USM交战时fail→`.9`；10年timeout也→`.9` | 完成条件已按集合检查，蜀亡并不等于这一集合为空；timeout调用`.9`必须另核真实停战，不能仅因计时到而设全局settled。 |
| [拥明/革命JE:408–425、468–485](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:408>) | 同样无战/无博弈→`.9`；`nesnd_south_settled`使非胜者日志invalid；on_invalid尝试`.11` | 因`.11`当前资格过窄，原吴-USM停战后会“旧JE失效但新选择无资格”。 |
| [nesnd_postwar_allegiance_eligible](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_settlement.txt:44>) | 存活反对国、拥明/革命派、未answered、非USM；要求USM满足`nesnd_current_rebel_winner`；可独立或为USM属国；与USM无战 | `nesnd_current_rebel_winner`还要求`usm_rebel_winner_of_the_civil_war`和`nesnd_rebel_settlement_seen`。这服务的是`.10`胜利者吞并旧USM再change_tag的分支，不是原吴停战。 |
| [.11:1511–1636](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:1511>) | immediate设`nesnd_postwar_allegiance_pending`，存USM胜者与请求者scope；拒绝附属路线标answered并加首都宣称，延迟`.12`通知；接受路线USM创建dominion，确认成功才标answered，延迟`.13`；after清pending | 现有30/70 AI权重可作为旧分支基线。`.12`只显示效果/通知，不会真正发起新战争；`.13`也主要是确认已发生的附属关系。新“继续抵抗”需要独立明确后继。 |
| [nesnd_south_settlement_retry:26–47](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_settlement.txt:26>)＋[monthly:1–2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_south_settlement.txt:1>) | 重试未决胜利结算和符合资格且无pending的战后选边 | 请求途中不能提前清pending，否则每月重复初始选择；新请求结束/取消应消费本国一次性锁，不能仅依赖事件窗口。 |
| [nesnd_ming_after_truce:1–9](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_ming_after_truce.txt:1>) | 非USM独立行在＋status quo自动出现；日后满足胜利事实→`.10` | 已有继续抵抗/日后胜利的承载点，保留；不能因SIH死亡全局删除其他行在/拥明国路径。 |

`usm_civilwar_occured`（历史上确实开过本轮战事）、`this_is_nanming_civilwar_var`（具体博弈实例）、`usm_opposition_country`（参加者）、`nesnd_restoration_side`（拥明者）、`nesnd_ming_court`（行在）、`usm_civilwar_status_quo`（停战结果）和`nesnd_south_settled`（当前广泛作终结标记）含义不同。新实现应把停战阶段与全部吞并/统一终局分开，不复用同一全局锁表示相反状态。

## 行在陷落与皇帝迁逃

[nesnd_south_capital_defeat:2–22](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_war_collapse.txt:2>)当前条件是存活反对国、非JAP/USM、非USM属国，并且已确认败退或与USM交战时满足：敌占>80%、首都由USM控制、首都由USM属国控制。若新用户只指定“USM占领行在首都”，应在行在特别分支严格核`capital.controller=c:USM`，不要无声扩大为任何敌人/友军/占领比例。

[usm_civilwar.5:927–1094](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/usm_civilwar_events.txt:927>)使用`nesnd_capital_surrender_pending`防重复，after重新验败退。但随后全体成年角色随机exile/kill，SIH概率权重1:5、HNA1:4等，最后USM `annex_as_civil_war=root`。本轮必须先保证皇帝身份及转移完成，不能把皇帝留给这段抽签。

目前避难实现的适用范围：[nesnd_ming_general_refuge:104–241](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_royal_refuge.txt:104>)只接受USM、`tag_WUU_var`、尚未settled、尚未resolved/player_transferred且USM为内战博弈发起者；先HNA再SIH。其候选[nesnd_ming_royal_refuge_host:1–8](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_court_followup.txt:1>)还硬限定这两个TAG。故它与“行在败退后随机任一拥明者”是不同生命周期，不应简单复用后期待自然生效。

建议事务顺序（为新实现合同，不是已有代码）：

1. 败退国保存为origin；识别实际`ruler`或`nesnd_ming_court_monarch`，先核存活、owner=origin及合法宗室身份。每次清旧临时host/monarch scope。
2. `any_country`和`random_country`使用**同一候选谓词**：存活、非origin/USM、确为拥明而非共和/吴派、至少一州、独立、首都仍自控。用户说任一拥明国，不能继续只允许HNA/SIH；是否允许玩家国家承接是产品约定，不要沿用旧`is_player=no`悄悄排除。
3. 有host：先`transfer_character`到host；确认新owner后保存新行在君主引用、设新`nesnd_ming_court`并按已定制度任君主；清origin行在引用。没有host：对皇帝`exile_character=yes`，保留人物，不kill。
4. 迁逃成功/流亡后才执行USM对origin吞并。其余角色处分必须排除保存的皇帝（及本轮明确要保全者），不要在所有其他国家里再次处理已转移角色。
5. 迁逃、吞并分别有一次锁，最后以真实国家消亡/人物owner或exile状态确认提交；不因scope失效无限循环。玩家失国允许GAME OVER，不需要另加play_as救援。

`exile_character`为character effect（引擎effects.log:9659–9662）；当前`.5`已有真实脚本用例，但本轮没有认证“仍任ruler时直接流亡”的引擎时序。以独立人物scope保留到吞并前后，若需要卸任，先查角色API再实施，不发明remove_ruler。现有`set_character_as_ruler`/`transfer_character`用法可见[nesnd_ming_enthrone_refuge:336–355](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_ming_royal_refuge.txt:336>)。

败退回调已有[nesnd_war_collapse on_actions:16–39](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_war_collapse.txt:16>)：胜方USM、`scope:target`为具体败方，设`nesnd_south_defeat_confirmed`，再排队次日检查；不能把某一支援国投降当所有拥明者战败。pending事务完成前，`nesnd_south_defeat_resolution_pending`会挡status quo，应保留此顺序保护。

## 外交接口：核到什么、没有核到什么

| 需求 | 当前实际接口与来源 | 边界 |
| --- | --- | --- |
| 开外交博弈 | country scope `create_diplomatic_play={target_country=... type=... escalation=... add_war_goal={holder=... type=... target_country=...}}` | 原生[虾夷事件:79–100](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ep2_ezo_republic.txt:79>)先独立、移出旧博弈backers，再另开`dp_annex_war`、escalation60，并给对手撤销宣称目标。文档的scope描述与实例形状有差异，使用当前实际实例的initiator country root＋target_country。 |
| 立即战争/跳阶段 | effects.log:909–922列`war=bool`；37204–37207列diplomatic_play scope `set_war=bool` | 未搜到`skipcountdown`或`skip_countdown`。本MOD西秦等用`war=yes`，但本轮无原生立即战争实例及新的实机结果，不能写“已验证必定绕过所有外交限制”。优先普通博弈；要立即战争另做定向验证。 |
| 创建附属 | 接收宗主country中`create_diplomatic_pact={country=申请国 type=protectorate/dominion/puppet}` | docs899–907；原生[巴尔干接受臣属:277–291](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/balkan_wars_events.txt:277>)从TUR scope创建保护国，`country=root`为申请者；[巴西:46–55](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/brazil/brazilian_minors.txt:46>)创建puppet。没有`make_subject` effect。 |
| 更改已有属国类型 | 属国scope `change_subject_type=subject_type_dominion` | effects677–680明确保留当前liberty desire；不是新建立宗属。 |
| 调整独立倾向 | 属国scope `add_liberty_desire=-5` | effects266–269，非条约属国无效；没有`set_liberty_desire`。若设计需要目标值，应先读`liberty_desire`、算差值并检查范围；最小实现可以不改独立倾向。 |
| 休战 | `has_truce_with=目标`；`create_bidirectional_truce={country=目标 months=N}`；`end_truce=目标` | effects809–815/1241–1246。原生[巴黎公社:616–624](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/paris_commune_events.txt:616>)有end_truce；[哈萨克:26–41](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/soi_events/00_ep1_kazakh_events.txt:26>)先独立再end_truce。说明可脚本解除，不等于应该给所有后续抵抗默认解除。 |
| 战争事实 | country `has_war_with=目标`与`is_at_war=yes/no` | triggers10988–10994、11260–11264。前者只看两国交战，后者看所有战争，含义不同。`is_country_alive`要求至少一州、可交互（11417–11422），比单纯exists更适合外交执行门槛。 |

引擎接口来源：[effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:899>)及[triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:10917>)。未发现可据此直接调用的`end_war`/`white_peace`接口；设置status_quo flag不会结束现有战争。

### 复战的可达性

- **国家存在且无双方战争**不等于可以立即复战：可能仍有休战、已承诺其他博弈、宗属关系、友好关系等阻碍。
- 原生`dp_annex_war`在[00_diplomatic_plays.txt:939–958](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:939>)还限制目标国等级≤insignificant、双方非相互宗属等；`diplomatic_play_has_no_relations_blockers`要求对目标/宗主关系低于cordial。[原生trigger:1753–1784](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt:1753>)。不能把UI普通吞并的限制忽略后保证脚本调用一定成功。
- 本MOD的[dp_usm_civil_war](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/diplomatic_plays/ce_diplomatic_plays.txt:1>)使用`wg_nesnd_usm_annex`、镜像目标，不是原版普通吞并。其[自定义目标:1–13](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/war_goal_types/nesnd_usm_annex.txt:1>)是`kind=annex_country`，settings包含目标参战、整国吞并与冲突验证；可借其已有语义做后继，但需新的本轮/再战锁，不能让旧全局settled封住。
- 推荐“继续抵抗”立即记录立场并显示后继，**等休战到期、双方存在独立且无冲突博弈后再开放/发起再战**。若作者明确要立即撕毁休战，则使用`end_truce`后重验并创建指定双方博弈，明确这是设计选择，不能用`war=yes`偷偷绕过去。
- 不添加`add_initiator_backers`/`add_target_backers`，就不会由该脚本强制点名拉第三国；但原生宗主、同盟和外交站队仍可能介入，不能承诺“永远没有第三国”。CNE接受附属后成为宗主，将来战争有自然关系后果，必须由它在和平时真实接受。
- 创建后用**当前发起者＋目标＋类型/本轮标记**确认新博弈存在再消费“已发起”锁；不要随便`random_diplomatic_play`选到另一个博弈加速。现有[内战开局effect:281–303](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_crisis_effects.txt:281>)就是先创建、再按initiator/target查到、再设置occurred的参考。

## CNE请降与每国一次选择的闭包建议

状态建议只描述需要，不发明原生API：`未选 → 继续抵抗/请求CNE中/降吴中 → 已解决`。新请求变量使用MOD前缀；现有`nesnd_postwar_allegiance_pending/answered`可沿用或显式迁移，但不要让旧“叛军USM获胜”语义误锁新分支。

1. **真实停战**才派发初始选择：USM与该国仍存活，没有相关战事/待结算吞并、没有有关活动博弈；是否要求所有国家停战由用户“真实停战”所指本轮战事判定，不以“该国眼下无战”代表整个南朝战争结束。
2. 初始每国仅派发一次；即时设pending，延迟回复始终带请求者与目标CNE身份。选择“请求CNE”后pending继续有效，不重新弹初始三选一；answered只在最终结果确认时设置。
3. CNE接收事件的trigger/option显示/实际effect各自重验：CNE与申请国都alive；CNE独立；申请国独立或已是CNE属国（后者幂等成功）；双方`is_at_war=no`且`is_diplomatic_play_committed_participant=no`；请求仍指向本CNE；双方关系仍达设计阈值。**阈值是平衡选择，接口并无强制“必须多少关系才能归附”的固定数值。**
4. 接受effect在CNE scope创建保护国/自治领，随后在申请国确认`is_subject_of=CNE`才成功收尾。发现已经投吴、改宗主、国家灭亡、开战或请求过期则走失效出口，不能强制拆别人属国或把CNE接进旧战争。
5. 拒绝有具名后继：申请国接收拒绝通知后选择继续抵抗或降吴，或按预设默认继续抵抗。该后继与初始三选一分开，仍保证初始只触发一次。超时/取消必须有同一保底结果和清锁；不让“pending永久悬挂”封死国家，也不因月度重试无限向CNE发请求。
6. 降吴同样不是只改flag：在和平、独立且USM仍为吴政权时创建实际臣属关系，确认成功再answered；若USM已变明/共和或消亡，原选项过期、通知并退至抵抗/自主结果。

AI可用原生条件：`is_at_war`、`is_subject`/`is_subject_of`、`is_diplomatic_play_committed_participant`、`has_truce_with`、`country_rank`、`liberty_desire`、关系和本MOD已有立场值；以`ai_chance={base=N modifier={add=... trigger={...}}}`表达。关系采用本机已证 `"relations(scope:requester)"`并先分支确认对象存在，原生[01_event_catalysts:24、30](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_catalysts/01_event_catalysts.txt:24>)与本MOD[外援答复:77–109](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:77>)提供实际形状。不把权重当资格；即使AI偏向接受，真正effect也必须再验和平/对象/关系。

## 最小验收清单

- SIH灭亡、HNA或其他拥明国仍存：不得全局宣告明方故事结束；其停战选择/后继仍可达。
- 行在首都被USM控：皇帝先迁随机合法host；无host时流亡；随后该国确实吞并；皇帝不被旧随机kill分支再次处理。
- 两个受降/战斗回调同日：一次迁逃、一次吞并；迁逃后新的host不能继承旧pending导致立刻再败。
- 停战但仍有其他参与者交战、或待结算吞并：不派发错误“战事已终”选择；`.9`timeout也不能跳过事实守卫。
- 每国三选一只出现一次；请求CNE期间读档、过期、对象消亡、CNE开战或申请国改属：确定清锁与后继，无附属关系则不标成功。
- CNE拒绝、接受成功、接受时条件失效三条都能收尾；接受前不会给CNE加backer/war goal。
- 有休战的继续抵抗：任务有效但不虚称已经再战；休战结束可复战；显式撕约若实现，只作用指定双方。
- 外部AST/引用检查后，实机仅验证尚未证实的迁皇帝—吞并顺序、旧档锁和外交创建结果；本报告不宣称这些已通过。

引用自检：28条本地文件链接存在、引用起始行均有效；只认证来源可定位。
