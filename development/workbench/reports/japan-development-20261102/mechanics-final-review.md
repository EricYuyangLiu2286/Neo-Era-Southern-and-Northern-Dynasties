# 日本候选机制终审

对象：`WORK/exports/japan-development-20261102-a` 当前源码；2026-11-02。只读审查，不修改玩法、不启动游戏。前置接口依据见同目录 `native-mechanics.md`；本次重点为JE入口/退出、外交迟答、联合与领土、文化转换。人物迁移由另一审查负责；旧版可接受失国、玩法难度不作为缺陷。主代理正在修复的动态AI权重及统计初始化/政权epoch不重复报旧问题。

## 已修复并定向复核：朝鲜自我外交案件（原P2）

位置：候选 `common/scripted_triggers/nesnd_jp_korea.txt:10–21`、`common/scripted_buttons/nesnd_jp_korea.txt:30–35`、`common/scripted_effects/nesnd_jp_foreign.txt:7–29,92–95`。

可达状态：独立JAP/JTK/JIM仍有非朝鲜领土、尚未 `nesnd_jp_korea_settled`，KOR已经成为该国直接属国（原生战争或附庸关系可产生）。如日方仍有Busan/Yangho州，则朝鲜JE已可用；完整国内统一也可开启该JE。

1. `nesnd_jp_korean_envoy_available` 只验证KOR存在、没有战争、对KOR宗主没有战争，没有排除 `c:KOR.overlord = root`。
2. 按钮从KOR切到其 `overlord` 保存 `jp_partner`，因此保存的是日方请求国本身。
3. `nesnd_jp_send_request` 没有 `partner != this`，把45天请求、付款与答复事件都发给自己。
4. `nesnd_jp_reply_valid` 的kind5路径也允许该身份：sender独立、partner就是sender，KOR的overlord确实是partner，双方patron快照仍一致，故接受可执行。
5. 接受先将日方朝鲜州转给自属KOR；随后通用非联合分支执行 `change_relations = { country = scope:jp_partner value = 25 }`，变为对自己改关系。拒绝也会执行country=self的−10关系效果。

这不是玩家失国保护问题，而是缺少不同外交主体约束。最小修复：朝鲜使节入口/按钮effect排除KOR直接宗主就是请求方；通用send及reply再统一拒绝 `jp_sender = jp_partner`，覆盖旧档已有悬挂事件。若需要允许对自属KOR安排归还，则应另走明确的对KOR本人/内部治理路径，不将请求发给自己。

本条已由主代理修复，2026-11-02定向源码复核关闭：外部朝鲜JE入口、envoy predicate及按钮visible都排除KOR为当前日方直接属国，effect重复消费该predicate；generic send在扣款/排队前拒绝partner=this；reply在sender scope再拒绝partner=this，故旧档悬挂自答事件也不能接受或拒绝执行。日方仍实际拥有朝鲜州时，治理JE的owned_korea分支保留。7项定向源码断言通过，未重跑全审、未开游戏。此次修复后的四文件SHA另附末尾，不覆盖原审查快照。

## JE激活和关闭逐组核查

原生依据：G `common/journal_entries/journal_entries.md:15–51`：自动进入由 `is_shown_when_inactive + possible`，直接 `add_journal_entry` 跳过入口但执行immediate；本候选两种方式都有。`possible`变假不会自行退出已激活JE，退出由complete/fail/invalid控制。

|JE/组|入口、前置和退出结论|
|---|---|
|`nesnd_jp_cohesion`|三TAG存活即进入；startup/bootstrap显式添加，immediate幂等初始化；无完成出口，为常驻日志；失去日本国家身份invalid清divided_councils。未发现自锁。|
|`nesnd_jp_mining → arsenals → metal_cities`|JTK、统计ready、产业资格；每阶段需前一done，当前done为false；opened只参与“未开且已达标则登记”的分支，不在possible中反向要求；完成设done并ensure下一项；invalid清opened。未发现自锁。|
|`nesnd_jp_cash_crops → textiles → consumer_goods → living_standards`|JAP同上；生活水平另有连续12个月计数，不达标清零；没有把生活水平已有单月合格直接跳过。JIM不进入该组。|
|`nesnd_jp_food_supply → food_cities → food_processing`|JIM同上；粮食允许本国稻田或实际市场粮价且无饥荒；没有所有三国共用done。|
|`nesnd_jp_nation`|实际独立或已经opened且未done可进入；opened维持被重新附庸时日志存在，complete仍要独立/无战争/三成果/12月；每月附庸时清sovereign计数。done使自身和子JE退出。|
|`nesnd_jp_new_army / open_diplomacy`|依nation_live但不反向要求自身已经存在，主ensure先add总JE再add子JE。各自完成标记独立；父完成或国家不适用使子JEinvalid。没有入口环。|
|`nesnd_jp_open_ports`|隔离法＋可用国家条件，含无九州港口替代；按钮科技/真实港口/金库同时复核；非隔离即完成，登记ports_opened并开产业。|
|`nesnd_jp_islands`|国内七核心整州、独立、未closed且岛屿未全收复；初次只加九州/四国claims；拥有两岛完成，和平承认现状按钮置closed后invalid；不再次发国内统一奖励。|
|`nesnd_jp_politics`|政治资格独立于日志存在；设started后不会因opened自锁；国家/完成/setback使invalid，君主路线失君主制fail；两出口均清临时修正。放弃清route/started并24月setback，结束后可再开。|
|`nesnd_jp_court_reform / military_reform / representative_reform`|依父live+正确route；未达ready才开；达到条件complete，切路线/父不live invalid；没有要求自己running的possible。已ready者不会新开无意义子JE，父仍要求持续12月与进度。|
|`nesnd_jp_foreign`|1840或分封/独立时进入；常驻国家外交入口；country不再适用invalid清请求。request_clock到期由monthly ensure清partner/kind/quote。|
|`nesnd_jp_korea`|拥有Busan/Yangho即进入，或国内统一独立且未settled、KOR存活；失去资格且未settled静默清治理修正；settled且无朝鲜州完成清治理。唯一已确认问题为上面的自我partner。|
|`nesnd_japan_reunification`|三个TAG、partitioned且未unified；immediate的unity_entered不再挡入口；core触发与goal=7一致；独立才完成，保留事件5和原奖励。|
|`nesnd_wu_eastern_question`|既有吴方案件入口；不是日方发展阶段；旧entered仅防重复，dossier_closed完成、失吴身份invalid；未改旧战败/恢复链。|
|7个 `REPLACE:je_meiji_* / je_sakoku`|明确关闭被本MOD替代的原生日志：possible=no、inactive=no、invalid=yes；这些不是新内容无法进入的意外自锁。军队/外交旧完成变量由ensure_nation迁移消费。|

注意验证边界：自动日志具体日刷新、create_country人口统计何时就绪属于引擎时序。本候选使用country启动/月度bootstrap及2天后stats event，且产业门槛要求statistics_ready；源码存在恢复路径。本次不把该时序宣称实机已验证。

## 外交迟答与联合：已闭合部分

- `nesnd_jp_send_request` 每次递增country request_number，保存partner、45天clock、双方直接patron、partner regime和realm revision；一次请求有6月冷却。
- 回信trigger和cancellation_trigger共同消费 `nesnd_jp_reply_valid`；选项effect再次通过同一谓词，处理“窗口打开后状态改变”。国家存活、仍是日本sender、原foreign JE仍存在、编号/partner一致、clock未过、无双方战争均复核。
- kind1/2/3/7要仍是该partner的直接属国，并复核其regime；kind1再核 `can_increase_autonomy`，kind3再核改革未完成。
- kind4核报价正数；accept额外核付款方金库；付款和收款使用冻结quote，没有扣款后重算金额。未来资助有3年锁。
- kind5要求请求方实际独立无战争、自己持有的朝鲜州均未被占领、仍保有朝鲜之外领土，KOR仍活且仍由原partner直接统属或自身独立。转地effect只枚举请求方当前所拥有的Busan/Yangho交集，不转外国州，也不整state_region吞外国份额。
- kind6在sender scope执行union_pair：双方不同、三TAG存活、均无战争/活跃博弈；独立双方或同宗主且sender获得该实际宗主授权。accept调用继承成果后才annex partner；已done是并集，没有再次加三份已完成奖励。
- `nesnd_jp_new_realm` 清请求并递增request_number/realm revision；JAP分封开头、JTK/JIM on_created及JAP恢复身份均已调用。旧响应不能直接沿用本次分封前的案件编号。
- 独立战按钮保持属国关系后调用原生 `dp_independence`，使用现overlord，没有预先 `make_independent`。入口检查停战、双方博弈、关系和原生拒绝自治条件；和平同意独立在kind2实际落地，并重置独立月数。

没有把“当前仍有效的援助承诺”“同TAG已经完成政治改革”或合法失败结果当成推测bug。尚未用游戏验证合并时人物/军队原生继承；人物部分以对应独立审查为准。

## 团结与文化：调用根和数量

候选 `common/journal_entries/nesnd_jp_cohesion.txt:11` 是唯一 `nesnd_jp_cohesion_monthly` 调用者；country monthly bootstrap只补入口，不再次调用转换。效果先核cohesion JE和statistics_ready，再更新country团结并clamp 0–100，高于75才调用文化效果。

文化效果在country根，JIM明确ce_wuu，其余japanese；两个分支各为70空/30选择**一个**random_scope_state，且只从本国有非目标人口的state选。先在state存固定 `nesnd_jp_conversion_fraction`，pop迭代通过 `state.var`读取，结束删除state临时变量。未出现country/root漂移或每pop重新取骰/重新算分母。两公式均为 `min(0.1/(1-target_share),1)`，作用于所有非目标pop，数学上为 `min(州总人口×0.1,非目标人口)`；未调用任何宗教效果。引擎整数舍入与split/merge仍未实测。

进度同步先save `jp_bar_owner` 再切JE，value显式从保存country读，避免在JE根直接读country变量。母JE退出清临时修正的范围仅限本模块。

## 指纹与覆盖

审查覆盖源文件 41 项；SHA逐项写入同目录 `mechanics-final-review-sources.json`。以下是已确认问题的关键源：

- `common/scripted_triggers/nesnd_jp_foreign.txt` — `40e0e1d523c6e1b1a910d966d061467cd953920f84903988908fba1f0f878370`
- `common/scripted_triggers/nesnd_jp_korea.txt` — `d426f533a3d6aaf7df140550052dad7030d9beecf00ebdcbbcdffe1d6f0e3826`
- `common/scripted_effects/nesnd_jp_foreign.txt` — `73e8918a222ccaf7ccc2c1741f009df65447afd944a37069e5d821b00cabc279`
- `common/scripted_buttons/nesnd_jp_korea.txt` — `b6aa7749a0861b4105c303a54d01157677c33163545a2884c175256ea52be3f6`


## 自我外交修复后的定向指纹

- `common/scripted_triggers/nesnd_jp_korea.txt` — `514ac9d263b9b425638b0d7605d20576b01193254bc0919d239511ff23713fe9`
- `common/scripted_buttons/nesnd_jp_korea.txt` — `d5318204cc471ce88376ca4c0bc9e5bddeadcbfd9e732ea7d49fd60cc4cbf479`
- `common/scripted_effects/nesnd_jp_foreign.txt` — `345b0f4f33d693836e4a9a09600ee825ef8eb7e302805bdf928fbac6b115e331`
- `common/scripted_triggers/nesnd_jp_foreign.txt` — `f9b3d9b6dedb7e50d1eb86fe94ec082332ee8b5b0d6462715fb4aef44a335dcf`
