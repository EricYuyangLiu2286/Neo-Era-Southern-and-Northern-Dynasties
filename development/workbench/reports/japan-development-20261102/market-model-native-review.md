# 共同市场模型与日本产业日志审查

2026-11-02；G=本机GAME，C=`WORK/exports/japan-development-20261102-a`，E=`WORK/references/engine-docs-1.13.11-20261031`。本轮 `catalog.py status`：**1.13.11 / build24799966，CURRENT，0 changed**。只读代码/网页研究；未改玩法、未开游戏。

## 用户纠正与当前结论

采购模块已被用户明确否决。不要恢复预付款、双边采购成本buff、定向订单、交货或库存模拟。本候选应让日本各国产业通过实际生产、就业和现有市场自然发展；同市场所需的买卖交互由引擎承担。旧 `wu-procurement-native.md` 顶部已标 **撤回／禁止实施**，以下旧正文仅保留历史，不再作为设计依据。

本次扫描C的日本新脚本/事件/两语loc：未找到procurement文件、kind8、采购clock/quote或添加人工buy/sell orders的日本效果。剩余外资请求kind4是实际资金援助＋短期建设/资格修正，不应再解释为吴国已采购或收货。政治/海岛完成的军需成本奖励属于各自改革/地缘结果，也不得重命名为采购履约。

发现三项需要修正的语义问题：**JIM粮价门槛只看市场价、属国开港文字越过关税权限、消费品正文用仓库存货解释需求不足。** 尚未发现现候选把造船能力当可出口商品或承诺确定交付数量；没有“每国所有物资必须自给”的通用门槛。

## 官方网页：原则与版本边界

[Paradox官方DD37《Market Expansion》](https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-37-market-expansion)，发布2022-03-09，明确共同市场把参与方买卖订单汇集，专业化产业可获得更广销路，但并不保证每个产业都获利；市场连接仍有运输条件。这里只采用这一原则，不采用旧版主动建立trade route/convoy控制细节。

[官方Steam DD143《Trade Rework: The World Market》](https://steamcommunity.com/games/529340/announcements/detail/524212840420081890)，发布2025-03-27，描述1.9重做：世界市场没有取代国家市场，建筑和人口仍在地方进行交易；贸易中心用Trade Capacity和地方价进行自动逐利贸易，港口提供Merchant Marine。此文是开发期说明，细节以本机1.13.11脚本为准。网页直接open只返回图片，已通过该官方URL的search全文核对，不采纳论坛玩家回答或2026更新摘要来覆盖本机版本。

## 本机完整链条

### 1. 属国关系与真实市场身份

- G `common/diplomatic_actions/20_subject_puppet.txt:11–26` 的pact连接 `subject_type=subject_type_puppet`；G `common/subject_types/00_subject_types.txt` 定义其军事/外交等权限。这里没有可随意移植的 `join_market=yes` 脚本字段。
- 当前G `localization/english/concepts_l_english.yml:1222` 明确subject diplomatic pacts也形成customs union，`:1652` 明确同市场各州互相交易（隔离州除外）。这是本版本游戏内概念，而非把2022规则不加区分地搬入。
- **属国不永远等于同市场**：G `36_subjects_grant_own_market.txt:12–40` 先比较同市场，再以pact `market_owner=second_country` 给对方自己市场；G `42_subjects_request_market_control.txt:13–31,91–103` 允许请求并以 `market_owner=first_country` 实现。不能仅凭 `is_subject_of=c:USM` 宣称当前已向吴市场供货。
- 原生比较形状是country `market = scope:other.market`，例见G grant-own-market `:14` 的 `market=prev.market`、`events/spanish_flu_events.txt:958,1021` 的 `market=root.market`。日本判断用存活guard后 `market=c:USM.market`，买方/卖方无需额外手工合同。
- 关税/禁运控制属于市场senior，见当前concepts `:1051,1225,1230`；它与法律、正式主权和实际市场身份是不同维度。

### 2. 生产、消费、订单、地方价

当前G concepts `:2365,2371`：生产形成sell orders、消费形成buy orders，市场可达性影响州贡献的订单数量。`:682` 市场价取决于买卖订单；`:687` 所有交易使用地方价，地方生产/消费与市场价共同决定价格，市场影响权重受market_access×MAPI影响。`:1119` 建筑按地方价获得收入；这不是国家金库之间自动等额打款。

E `triggers.log:12859–12890,12938–12953` 给market_goods buy/sell orders、production、consumption及delta；delta是流量 `(production + imports) - (consumption + exports)`。`:14366–14403` 的state_goods production/consumption/delta及地方溢价分别限定state_goods scope。**delta不是仓库存量，市场总产量也不是JTK国产量**。E targets `:325–328,435–439,1491–1495` 对应country→market→mg和state→sg。

因此：JTK在USM共同市场开工的轻武器厂增加该市场轻武器供给与投入需求；USM军事建筑/人口的消费正常形成相应需求。产出并不锁定某一个国买家，不需要额外“USM购买按钮”。JAP纺织/消费品、JIM食品同理。若独立仍同市场，它们继续参与；若真的离开该市场，价格/销路风险由新市场与原生世界市场渠道产生，不能再保留“必定供吴”的叙述。

### 3. 可达性、基础设施与地方供给

- G concepts `:1658`：基础设施使用超过容量会降低market_access；market_access同时影响订单与地方价中的市场权重。`:1640` 隔离州不会向中央市场贡献买卖订单，市场价也不影响其地方价。
- G `common/static_modifiers/00_code_static_modifiers.txt:49` 基础MAPI=.75；G `technology/technologies/30_society.txt:296–304` stock_exchange增加.1。即便100%可达，各州地方价格也不必完全一样；不要把共享market ID等同于全国同一价格。
- G concepts `:2255` 港口连接需要两端港口，航运负担跟相关州基础设施使用有关；G defines `:631–638` 当前使用merchant_marine及供给网络短缺，不靠旧2022贸易路线模型解释。
- 原生资源链：G buildings `11_private_infrastructure.txt:3–28` 港口；PMG的港口组实际位于 `07_government.txt:1`；PM `11_private_infrastructure.txt:15–35` basic_port耗clippers6、产merchant_marine9，并按workforce提供基础设施3。港口级数存在不等于满员或海路已畅通。
- G defines `00_defines.txt:419–425` 有投入品不足产生output penalty的阈值、逐日速度和上限；不能保证工厂造出来就达到名义产量/利润。无需反过来要求每种投入必须自产，真实市场获取也可供其运作。

### 4. 当前世界市场与贸易中心

G buildings `11_private_infrastructure.txt:236–263` 的building_trade_center可由政府或私人建造，调用PMG `11_private_infrastructure.txt:27–36`；PM同文件 `:333–360` 通过workforce给state_weekly_trades、state_trade_capacity，`:394–400` 等贸易量PM消耗merchant_marine。与DD143方向相符，**贸易中心是跨国家市场/世界市场渠道，不是同一USM市场中JTK向USM卖枪的必备“订单中心”**。

若日志只要求加入或利用共同市场，不必额外强制每国都建一套贸易中心。若目标明确是跨市场出口、商贸专长或市场独立，则可选择真实港口/贸易容量/实际贸易数据，不能只因拥有港口级数就声称自动出口或永久无短缺。

### 5. 产业PM与日本专长

|产业|原生投入/产出或能力|对日本目标的含义|
|---|---|---|
|轻武器|G PM `01_industry.txt:2313–2334` muskets：铁10＋硬木10→small_arms30，workforce_scaled|JTK产能可服务共同市场；无需USM额外付脚本订金|
|船厂|G PM `:1908–1935` basic_shipbuilding：木40＋fabric20→clippers40，另country_ship_construction_add5|clippers是可交易商品；country造船能力是该国能力，不能写成同市场自动共享给USM的商品|
|纺织|G PM `:274–313` handsewn fabric40→clothes45；dye_workshops另加dye5→clothes60|JAP可买市场原料；发展经济作物是其专长选择，不代表工厂所有原料必须国内自产|
|食品|G PM `:1–18` bakery grain40→groceries45；`:78–123` cannery/cannery_fish更改肉/鱼/铁等投入并增加groceries|JIM可在共同市场获取原料。当前没有要求JIM自产罐藏所需铁，是正确的分工边界|

吞吐由当前concepts `:1475` 明确定义为同时增加投入/产出及相应效果。候选产业奖励5/10年10–15%吞吐不会保证有销路、盈利或家庭富裕；需保留在岗/利润和实际SOL条件，不应增加人工sell_orders代替产业成长。

## 需要修改的具体项

### M1：市场粮价替代地方生活条件（机制问题，P2）

位置：C `common/scripted_triggers/nesnd_jp_industry.txt:1–4,59–65`；同条件嵌在C JE `nesnd_jp_industry.txt:155–165`；文字两语loc `:17`。

`nesnd_jp_affordable_grain` 只查 `market_capital.market.mg:grain.market_goods_pricier<=.1`。只要共同市场粮价便宜，即使JIM城市被隔离、基础设施不足导致本地粮价昂贵，且饥荒尚未出现，粮食阶段仍可以完成。`NOT has_famine`不是市场可达性或本地负担条件，也不是充分的当期购粮保障。

提议：评价真正相关的本国城市/有人口州的 `sg:grain.state_goods_pricier`（必要时结合粮食安全/SOL或实际市场连接）；可以接受本地生产便宜，也可以接受共同市场或贸易带来的便宜供给。不要将修复改成“全部粮食都要本国产”。原来的“国内稻田级数”路线也只证明能力，若目标是居民买得起饭，应同时需要实际开工/价格或生活结果，而不是空田级数绕过。

定义相关城市范围后，两处ready/JE条件同时使用同一predicate，避免一处地方价另一处仍全市场价。E `state_goods_has_local_goods_shortage`只检查“地方缺但全市场不缺”，不能单独替代所有供给/可负担性判断。

### M2：关税权限与junior开港文字不一致（玩家描述问题，P2）

位置：C `common/scripted_triggers/nesnd_jp_development.txt:21–31` 允许一些subject进入；C buttons `nesnd_jp_nation.txt:1–23` 只改本国贸易法；两语loc `:62,78` 描述本国政府选择关税保护谁、以关税扶持本国生产者。

当前原生senior控制共同市场关税；`activate_law=law_protectionism`没有改变market_owner或授予自主关税权。因此处在USM市场的JIM/JTK/JAP执行同按钮时，文字会把贸易法变化描述成已经获得市场关税控制。提议按 `market.owner=this` 区分说明，junior只说调整本国制度/开放条件；不要为了配合文字强制退出USM市场，也不要无必要禁止其发展。

### M3：仓库存货比喻不适合当前纠正（文字问题，P3）

位置：两语loc `zzzzzz_nesnd_jp_development_*:13` 的consumer_goods_reason：“货物……堆在仓库里”／“goods waiting in their warehouses”。候选没有库存机制，当前市场模型是流量和价格/利润。按用户明确拒绝库存虚构，建议改为购买力不足压低销路、价格或工场收入，不增库存变量或模拟售罄。

两语loc `:5` 的“承包商盼望长久订单”只是叙事期望，没有保证订单数量/实际脚本合同，可保留为社会矛盾；若改文案，应解释为政府需求和市场销路，而非恢复被否决采购模块。

## 其余日本模块的市场模型核查

|范围|结论与处理建议|
|---|---|
|JTK矿业→军工船厂→工业城市|铁/煤/木及钢铁/工具门槛是本国产业建设目标，没有指定必须国内自给率100%；原料仍正常从市场获得。无需再加USM付款、单独供给合同或每月交货计数。若强调对共同市场有贡献，可用实际在岗产能＋state market_access作状态解释，不保证专供USM。|
|JAP经济作物→纺织→消费品→SOL|阶段特色明确，不要求全部棉/染料/丝/家具投入都自产；三种作物只要其中两项。真实SOL保持12个月才完成，未用永久SOL buff替代。修M3即可；无需把本国纺织建设目标放宽成“市场里任何国家有纺织厂”而丢国家产业特色。|
|JIM粮食→城市→食品|已有“稻田或市场粮价”的非自给思路；修M1以获得实际本地负担。食品要求canneries和在岗食品厂，但没有要求国内拥有全部肉/鱼/铁投入；合乎分工。城市阶段强制纸厂1级是可讨论的产业目标，不能当作学校必须自产纸的引擎条件；若这不是作者期望专长，可替换为纸张可获得性。|
|产业奖励|C static_modifiers/nesnd_jp_industry 仅本国目标产业吞吐、行政/教育/声望；无USM无偿对应补贴、无人工订单、无固定保证收益。吞吐同时提高原料需求，市场不利时仍可亏损，这是合理经营风险。|
|独立后国家发展|只需要完成本国一条工业主链、军制、外交；不要求同时完成三国全部工业。成为独立国家不等于脱离所有贸易渠道，不能在文字里宣称已自给。|
|军事政治、开港、朝鲜、海岛|未见通过共享市场自动转交军舰或库存。政治军事奖励与海岛军事成本减免均没有采购结算变量，应按其政治/地缘语境解释。开港文字按M2修；朝鲜转地可能改变市场供给，是实际后果，不自动补齐丢失煤矿。|
|一般外资kind4|C foreign effects实际扣资助方/加日方，修正是建设＋资格；并非商品交易或供给证明。用户此次取消采购不能被曲解为连普通已授权外交援助都必须删除；同样也不能用该援助冒充产业对吴供给。|
|既有崩溃/恢复|保持既有真实领土/属国结算。市场归属按实际关系与market scope读取；不得为了保护旧供应人为撤销败战、恢复边界或再造保证合同。|

## 建议的可复用判读

先区分“本国建立某产业能力”与“居民/工厂能取得某商品”。前者可以要求本国建筑并核就业/盈利；后者应允许共同市场/贸易，观察相关州地方价、短缺和生活结果。第三种“本国专供特定外国买家”不是共同市场自动成立的事实，本次用户明确不要另造这一系统。

静态查证完成不等于本候选经济已实测。后续由正常玩家局面观察市场身份、关键州access/local price、工厂就业/利润、需求和SOL即可；此次研究不授权重新开游戏、反复读档或修改主MOD。

## 来源指纹

完整来源SHA存同目录 `market-model-native-review-sources.json`，包含以下当前C与G/E文件；报告结论按该时点快照，不把后续修改自动算为复核通过。

- G `common/diplomatic_actions/20_subject_puppet.txt` — `0a653598deac05bf3c7bfb31ac7bb307c366cf33beee0b4fc94f139a201742e7`
- G `common/subject_types/00_subject_types.txt` — `97a488157dfb2f340cca06aba30bfef42a36ea0a48dce6e591c8891628a6b91d`
- G `common/diplomatic_actions/36_subjects_grant_own_market.txt` — `ad712dcfe896c0255eedf87ab979859c3e0702c56b8fc57370b7d61c71a076b3`
- G `common/diplomatic_actions/42_subjects_request_market_control.txt` — `88c081fb87846a98b78345fbda4e62e878184a08f161512a5c09baaab45699d1`
- G `localization/english/concepts_l_english.yml` — `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`
- G `common/static_modifiers/00_code_static_modifiers.txt` — `0f42a271058ca8932c8b87641328473f1bc6a7961b7f4bf40663d5aba43faf1d`
- G `common/technology/technologies/30_society.txt` — `410b033c6ed95b5b417370a8778e5e056bc49d2cb95098854b0eb88d69f58cbb`
- G `common/defines/00_defines.txt` — `e47db10931a2149c80aadab0b8de8f3fa000fdbb82a2f878fee893aa4434dd39`
- G `common/buildings/11_private_infrastructure.txt` — `6e3a9f21fec99e13158a4ee10d6a92ce9cdc78e35e1ee0bc9bce6c6632165ae0`
- G `common/production_method_groups/07_government.txt` — `fa5db0c793e60880b525ee1e30e77724239c108b2497c3180273402d5c41354c`
- G `common/production_method_groups/11_private_infrastructure.txt` — `cf04fc870d1b1bb48bdbde342612b8c6b5df62723150656b9a35d86e4ad8ca17`
- G `common/production_methods/11_private_infrastructure.txt` — `cd32009af5d592d99cf1a9822a57542b9e0b9ad82c7193f24ec32cf3799a017e`
- G `common/production_methods/01_industry.txt` — `d0abb71f6ba922f46e1e512810053d1206a3cbfd8a2ff419d8a66c87b8a36886`
- G `events/spanish_flu_events.txt` — `dae1e93887b03a12bc55007c0a6c9d42e5877cbcff9e7ee2123737223d91708f`
- C `common/scripted_triggers/nesnd_jp_industry.txt` — `91bbfdeb8dc261b7261fb5f3346ecb90460d12d93bd6cc7d0732d15ce2eeb873`
- C `common/journal_entries/nesnd_jp_industry.txt` — `1f098ba6df02c44c0e5584870f0993e550139f83a5e7ae407c37f07bc8ee4397`
- C `common/static_modifiers/nesnd_jp_industry.txt` — `4011d679679eaff718da8ce9a06b7a34f1a1c37547f01f1ff06bd36196a8684c`
- C `common/script_values/nesnd_jp_industry.txt` — `e1fea205c982fc65ce84ebd9d81b6dcec8c413168d71bfbaf1482fbc0a383270`
- C `common/scripted_triggers/nesnd_jp_development.txt` — `7c73e027b05b81bf7fc042a24ff69fd3449c493a27a3d1267ce2abfa3aad020b`
- C `common/scripted_triggers/nesnd_jp_nation.txt` — `58f260e7f8febad48a02f9737e73532f7e5a2fa5243d58725eededf753599cc7`
- C `common/scripted_buttons/nesnd_jp_nation.txt` — `a15e1bb1a5a6e6f83a1a7b6619401a08d4bad0a69d40f5e3fdd8952f92baaef8`
- C `common/scripted_effects/nesnd_jp_foreign.txt` — `72d3a433e59a25fe8cf6f9021811d4b7ae26ee4f6b055235d9eb66b03a97c870`
- C `common/static_modifiers/nesnd_jp_foreign.txt` — `f68a73975f921809a7d8b373d5eb1908986cd57739cffe42c69e70045a55c73e`
- C `common/static_modifiers/nesnd_jp_politics.txt` — `59f3ddfb9bcb3bf227ce99d4a2f4452a94cdb7e0eca7a47032862713cb765681`
- C `common/static_modifiers/nesnd_jp_nation.txt` — `ecf1d6710c28337519153b0c9f33bd056af520fbce06c499bcccb2b1bd54338e`
- C `localization/simp_chinese/replace/zzzzzz_nesnd_jp_development_l_simp_chinese.yml` — `bba2b6a29c953138abdd43990808f354692c6a20a0b4f6ce4e1ce93a13296adf`
- C `localization/english/replace/zzzzzz_nesnd_jp_development_l_english.yml` — `c9e85a69f61b7f9662d8f09e38d46af48822ca54cd67746b35253cfb37b30b50`
- E `triggers.log` — `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`
- E `event_targets.log` — `cc12b15da310d0d8ef10a9209107b4d2298a882fa6ee038c202650e3c9bd7c71`
