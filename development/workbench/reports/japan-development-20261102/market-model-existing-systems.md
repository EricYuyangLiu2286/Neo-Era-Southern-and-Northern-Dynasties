# 现有南朝经济系统：共同市场模型审查

范围为当前主MOD（本轮文案提交38cf3ea后的加载目录）与日本候选 `japan-development-20261102-a` 的 Supply、External、PHI、Tenasserim四组脚本和双语本地化。只读审查，只输出报告与修正提案；未改游戏源码、主MOD、候选或技能，也未打开游戏。`catalog.py status`确认本机1.13.11／Steam build24799966、CURRENT、0变更。

## 结论

确认两处同根机制问题，均在现有Supply系统：

1. 共同市场已经发挥作用时，仍以“自行采购”或“收到商使答复”的旗标决定能否累计供需稳定期。市场价格、当地短缺和就业全都达标也会被第四格挡住。
2. 取消或失去外交联络直接清零稳定周数，即使国家仍处同一共同市场、实际商品供应和就业没有变化。

提案只改两个旧函数，并修正12个说明键。直接读取当前首都市场的参与国数量，至少两个成员时自动满足“商贸安排”；原有独立市场外交选择保留。取消联络不再直接归零；真实市场发生变化、战争、破产或任一实际门槛失效时，原有周度检查仍会归零。不会给共享市场成员自动补货、降军需成本或指定出口对象。

未发现需要删去的PHI“库存系统”：补贴是财政流量，贡赋是财政关系，交舰是既有舰船资产的所有权改变。Tenasserim的林场为正常政府建设，完工、招聘与生产进入真实市场。External的军械援助采用真实跨市场 goods_transfer 条约，而不是虚构政府仓库；这些机制全部保留。

## 原始来源与当前版本核对

官方DD37说明，共同市场成员的生产与消费共同形成买卖订单，基础设施和海上连接影响市场接入。它只用于解释共享供需，旧版贸易操作界面不作为1.13.11接口。[官方DD37](https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-37-market-expansion)

2025年3月27日DD143介绍1.9贸易重做：人口和建筑仍在国家市场买卖，世界市场提供自主跨市场贸易，贸易中心按盈利调整贸易量；国家间定向协议仍另有机制。当前源码进一步确认了这些类别。[官方DD143](https://steamcommunity.com/games/529340/announcements/detail/524212840420081890)

- [localization/english/concepts_l_english.yml:1652](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:1652>)：concept_market：同一市场州之间交易；市场接入决定连接程度。 SHA256 `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`。
- [localization/english/concepts_l_english.yml:1658](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:1658>)：concept_market_access：影响州产出和消费形成的订单及地方价。 SHA256 `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`。
- [localization/english/concepts_l_english.yml:2365](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:2365>)：concept_sell_orders与2371 buy_orders：按市场内各州生产/消费形成。 SHA256 `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`。
- [localization/english/concepts_l_english.yml:170](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:170>)：concept_trade：自主世界市场贸易与国家定向条约并存。 SHA256 `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`。
- [localization/english/concepts_l_english.yml:178](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:178>)：trade_privilege给另一市场参与国贸易优势，并不分配一个库存。 SHA256 `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`。
- [localization/english/concepts_l_english.yml:1178](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml:1178>)：foreign investment：产权收益和当地劳动力/税收/市场分开，货物仍属当地市场。 SHA256 `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501`。
- [common/journal_entries/00_player_objectives_economic_dominance.txt:121](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_player_objectives_economic_dominance.txt:121>)：当前country JE实例：market={owner=ROOT participants>=8}。由此验证participants为实际市场成员读数。 SHA256 `7fb15aab732c9ce9f93c4f3a86265de98aaef64b1d9fdb4a4dd8174ec8e12599`。
- [common/journal_entries/04_india_non_cooperation.txt:56](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_non_cooperation.txt:56>)：当前JE直接比较 root.market 与 top_overlord.market，之后读取市场卖单；不是宗属旗标替代市场。 SHA256 `8f700a392a548f3ddbd5013ee237226dfeb3db85a836b894a34d3f4960d4c1fd`。
- [common/journal_entries/00_trade_route_event_missions.txt:50](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_trade_route_event_missions.txt:50>)：原版以首都商品补贴政策及capital.market粮价检查经济结果，不建立库存。 SHA256 `73cf21807a31233312d38932aab6ebe36344f883e81f70487f1a13723d0b4ac1`。
- [common/history/treaties/00_historical_treaties.txt:233](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/treaties/00_historical_treaties.txt:233>)：法国援埃及：create_treaty→goods_transfer small_arms quantity10，证明跨市场定向援助确有同类。 SHA256 `a1c7e519ef1b07e2491f473ce0f94e6abae718fe725d68bcd8644d2432602f4e`。
- [common/treaty_articles/13_goods_transfer.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/13_goods_transfer.txt:1>)：required inputs、市场可达、非关税同盟从属成员、运输/出口上限与冻结条件。 SHA256 `50d4e8ae301c522a278598c9f315430417fc34a3a8bbf536b0d3a5cf371b607d`。
- [common/treaty_articles/25_trade_privilege.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/25_trade_privilege.txt:1>)：两市场所有者的贸易优势条款，内有junior限制和履行条件。 SHA256 `175370234bc4b186929b9ad24acfc7b0632dd954c026366fb5e9eda1b9068389`。
- [common/treaty_articles/05_transfer_money.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/05_transfer_money.txt:1>)：quantity为财政转移，付款国default导致冻结；没有商品库存输入。 SHA256 `6f59db04c429ab06eb6844cfadc87c3a54525e9e447586f19d0e40c780198112`。
- [events/agitators_events/land_ownership_law_events.txt:1576](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/agitators_events/land_ownership_law_events.txt:1576>)：原版state scope start_building_construction调用，正常排队建设。 SHA256 `32ffdd874d2536863a8378a62ead186121cdde997d69a885df000024ee02b635`。
- [common/buildings/09_misc_resource.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/buildings/09_misc_resource.txt:1>)：logging camp→required_construction、PM groups、图标/资源。 SHA256 `35cd32a26048973da45b79c00c30fb473dcbf4e57591a436dc769ec6d8f2f6b7`。
- [common/production_method_groups/09_misc_resource.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/production_method_groups/09_misc_resource.txt:1>)：林场基础PM组→simple_forestry/saw_mills。 SHA256 `5b4ed0b128d021cd448cafbc4031ff1ee7df29861831248efeec4e1507f27a07`。
- [common/production_methods/09_misc_resource.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/production_methods/09_misc_resource.txt:1>)：林场PM workforce_scaled wood30；saw_mills投入tools5、产出wood60，实际雇员决定生产，而非点按钮发木材。 SHA256 `e2aadd13e1b7042fc0ce85fb66ba016db0b3a06248e7a9d1eb5efa228d2bde0d`。

引擎文档：[effects.log:37128](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37128>)的set_ship_owner_multiple说明真实舰船批量转移，并须clear_ownership_transfer_fleet；[triggers.log:8930](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:8930>)与[effects.log:1030](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:1030>)分别记录条约检查与创建格式。

## 逐系统结果

### Supply：需要修正

`nesnd_supply_inputs_ready`从当前 `capital.market`读取paper/tools/small_arms价格，并按root国家检查本地短缺。`jobs_ready`分别要求湖广大学与军营、四川工具厂及铁矿/林场、广西纸厂及林场、东洲港口与官署。这些是产业与行政专业能力门槛，**没有要求每国自建所有投入品**，应保留。`livelihood_ready`看就业、饥荒及共同市场粮价，也接受共同市场供应。

错误集中在商贸旗标门槛与联络清理。真实调用链如下：

- [common/journal_entries/nesnd_supply_journals.txt:25](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_supply_journals.txt:25>)。
- [common/scripted_triggers/nesnd_supply_triggers.txt:83](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_supply_triggers.txt:83>)。
- [common/scripted_triggers/nesnd_supply_triggers.txt:86](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_supply_triggers.txt:86>)。
- [common/scripted_effects/nesnd_supply_effects.txt:32](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_supply_effects.txt:32>)。
- [common/scripted_effects/nesnd_supply_effects.txt:50](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_supply_effects.txt:50>)。
- [common/scripted_effects/nesnd_supply_effects.txt:103](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_supply_effects.txt:103>)。
- [common/scripted_buttons/nesnd_supply_buttons.txt:489](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_supply_buttons.txt:489>)。
- [events/nesnd_supply_events.txt:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_supply_events.txt:2>)。
- [events/nesnd_supply_events.txt:253](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_supply_events.txt:253>)。
- [common/static_modifiers/nesnd_supply_modifiers.txt:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/nesnd_supply_modifiers.txt:2>)。

`self`实际只清除partner/pending、设置self_reliance并刷新；没有建厂、改PM、改就业、增产或转移货物。因而不能将其改名“整顿本国生产”来掩盖没有生产效果。提案将其准确表述为交由商人继续往来。商使首次接受的实际政治收益是关系+25，六个月−100影响力；完成奖励是24个月+100影响力，不是商品或收入收益。已经存在的外交联系与双向trade_privilege可作为可选外交行动留下，不把它们当作共同市场供需的前提。

### External：机制保留；排除一项初步误报

钱款条约为每周500；军械条约是quantity10的small_arms goods_transfer。创建之前重复检查can_create_treaty以及供应者市场价格/本地短缺，原生条约定义另负责市场可达、成员身份、运输与进出口上限。它不设置“军械库存”、预付款库存或自定义交货量，也没有用buff冒充商品。待答请求失效时清理的是外交提议，不删除产业；已签条约由原生机制继续履行。

审查中初看见can_create_treaty写 `good`、create_treaty写 `goods`，曾向主代理提示可疑。继续读取当前引擎完整文档后立即撤回：triggers.log明确使用单数good，effects.log明确使用复数goods。**不得对这六处检查盲改为goods**。当前本体历史条约只有create侧的goods实例，不能据此反推can_create侧语法。无本轮引擎运行，不给这项接口另立成功或失败结论。

- [common/journal_entries/nesnd_external_journal.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_external_journal.txt:1>)。
- [common/scripted_triggers/nesnd_external_triggers.txt:134](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_external_triggers.txt:134>)。
- [events/nesnd_external_events.txt:184](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:184>)。
- [events/nesnd_external_events.txt:555](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:555>)。
- [common/scripted_effects/nesnd_external_effects.txt:55](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_external_effects.txt:55>)。

### PHI：不删财政和舰船机制

PHI的relation_valid明确要求当前 `market = c:USM.market`、直属宗属及和平；这是军费协定适用关系，不是市场供需开关。四种补贴数额8000/3000/8700/3700经真实money_transfer支付，减贡和免役经独立外交协定处理。首次B路线将现有20艘战列舰转归USM，`b_transferred`防止续签重复交舰。`needed_crew`是舰员需求，绝非商品库存。

市场或宗属改变时，PHI军费协议停止或重新评估可以保留：它反映补贴的政治条款，不代表两市场之间商品从此完全断绝。当前文案写重新商议军费，与效果相符。既有舰船不回收、不重新创建、不删除；没有理由因本轮经济模型纠正重做已验证海军。

- [common/scripted_triggers/nesnd_phi_finance.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_phi_finance.txt:1>)。
- [common/scripted_effects/nesnd_phi_finance.txt:175](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_phi_finance.txt:175>)。
- [common/scripted_effects/nesnd_phi_finance.txt:307](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_phi_finance.txt:307>)。
- [common/scripted_effects/nesnd_phi_finance.txt:431](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_phi_finance.txt:431>)。
- [common/scripted_effects/nesnd_phi_finance.txt:452](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_phi_finance.txt:452>)。

### Tenasserim：正常地方发展，保留

林场按钮按本国实际state排入一级政府建设，仍需建设力、财政、完工和招聘。`nesnd_ten_orders`仅累计该按钮委办过几次，最多2次；不是“商品订单库存”。林场PM产出进入该州实际市场，若DEI仍在USM共同市场，就自然参与USM共享卖单，不需要再发一份运木材给吴国的合同。

完成检查使用就业、家庭饥饿/生活水平、人口加权市场接入，以及至少一处适当非农建筑75%配员/无投入短缺。教习增加资质获取，补偿扣财政并给地主好感，法律按钮走真实enactment。停止专项只清理专项教习和连续月数；已排建设、既有产业、当前法案和已付补偿保留。没有本轮市场模型问题。

“南洋海船将染料运往江南”是作者世界中的地理与经济叙事，没有承诺某次按钮把一批存货交给USM，不应机械删除。产业专业化与不同地方市场价格仍然可以产生实际地理贸易关系。

- [common/journal_entries/nesnd_tenasserim.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_tenasserim.txt:1>)。
- [common/scripted_effects/nesnd_tenasserim.txt:79](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_tenasserim.txt:79>)。
- [common/scripted_triggers/nesnd_tenasserim.txt:39](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_tenasserim.txt:39>)。
- [common/script_values/nesnd_tenasserim.txt:7](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_tenasserim.txt:7>)。
- [common/scripted_effects/nesnd_tenasserim.txt:104](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_tenasserim.txt:104>)。

## 修复闭包与极值场景

|场景|修复后预期|保留的限制|
|---|---|---|
|HNA/SIH/GNG与USM同一实际市场|第四格自动满足；可凭真实货源、专业建筑与民生累计12周|仍会因价格、当地短缺、招工、失业、粮价、战争/破产不合格而停|
|仍是USM附属但获独立市场|不按宗属假定共享；依当前参与国数与原有独立市场选择判断|消费可来自本市场及自主世界市场贸易，不要求全套自给工厂|
|HUS仍在北朝共同市场|直接读取其实际市场，完全不硬编码USM|HUS本有港口/官署、硬木条件保留|
|取消商使，市场和经济条件没变|不直接归零；共同市场第四格仍成立|尚未付款的商业请求可清理，真实已签条约不受影响|
|退出共同市场，首都市场确实改变|原有market比较将连续周数重算；旧联络按现有政治关系校验|已建建筑、在建工程、人口、PM、舰船不删除|
|独立市场失去唯一已选伙伴且未选自行往来|现有all_ready不满足，依原规则重算|这是保留的外交安排选择，不写成物资库存归零|
|JE已完成后市场改变|不重新激活已经完成的JE，不撤销产业|本有一次奖励与期限保持；没有新的快照/采购系统|
|外援签署前加入别人市场|保留真实can_create_treaty再次校验|不绕过原生同盟从属成员和市场可达条件|

## 文案对读

前一轮已读取并保存的成熟作者样本为备份ce_usm_events的flavorUSM.4.d（海贸、兵财与政治地位的因果）、ce_usm_conflicts_within_reason（读书议政的社会过程）。本轮只调整操作事实和必要条件，不再次重写这些叙事。下面逐项列出旧句、提案与原因；仅编辑提案通过，尚未接入游戏。

|键|当前中文|提案中文|原因|
|---|---|---|---|
|`nesnd_supply_status_diplomacy`|各方商路尚待议定。可以遣使联络邻邦，也可以交由本国商帮筹措。\n$nesnd_supply_rules_link$|商贸联络的安排尚未议定。可以派使接洽，也可以交由商人自行往来。\n$nesnd_supply_rules_link$|Shared-market members now bypass this status automatically; independent-market political choice remains, without suggesting goods begin flowing only after acceptance.|
|`nesnd_supply_self`|依靠本国商帮|由商人自行往来|Actual effect only selects a policy flag and clears contacts. It does not improve production or jobs, so do not call it industrial reorganisation.|
|`nesnd_supply_self_desc`|请本国商人自行安排采购，召回此前遣出的使者。|撤回专项使团与待答请求，由商人继续经营现有买卖。市场归属和已经签署的条约照旧。|Describe the actual clear_partner/self flag; no production, procurement, stock or access effect exists.|
|`nesnd_supply_invite_desc`|遣使与对方商议商人往来和采购联络，听取他们的条件。|派使与对方商议商业往来，争取更好的两国关系。现有市场中的买卖照常进行。|The first accepted contact changes relations by +25. It neither creates goods nor establishes a market connection.|
|`nesnd_supply_invitation_tt`|商使将在七日后抵达；本次使团任期六个月。|商使将在#v 7日#!后抵达。使团任期#v 6个月#!，期间[concept_influence]#n −100#!。|State existing diplomatic influence cost; no fictitious purchase fee or commodity payment.|
|`nesnd_supply_accept_tt`|建立通商联络。|建立商业联络；首次接受时，两国关系#p +25#!。|Exact event1 first_contact_rewarded effect; do not claim guaranteed supply.|
|`nesnd_supply_end_contact_desc`|召回驻外使者，另寻能够长久往来的商路。|召回专项使团，结束此次商业联络。现有市场中的买卖与已签条约继续有效。|Contact is diplomatic, not a pipe that switches ordinary common-market production on or off.|
|`nesnd_supply_end_contact_tt`|结束此次联络，连续安定周数归零；已经签署的正式条约仍依约履行。|结束此次联络。若商贸安排因此中断，连续稳定周数重新累计；已经签署的正式条约仍依约履行。|No unconditional zero when shared-market arrangements remain valid; independent-market selection still follows live qualification.|
|`nesnd_supply_finish_desc`|货源、工场、民生与通商安排连续安定#v 12周#!后，首次获得持续#v 2年#!的通商收益。|货源、工场、民生与商贸安排连续安定#v 12周#!后，首次获得持续#v 2年#!的[concept_influence]#p +100#!。|The reward is influence capacity, not extra goods or income; preserve exact +100/24-month modifier.|
|`nesnd_supply_finish_shared_desc`|继续在共同市场中经营，保留既有盟约。货源与生计连续安定#v 12周#!，首次获得#v 2年#!通商收益。|继续在现有共同市场中经营。各项条件连续维持#v 12周#!后，首次获得持续#v 2年#!的[concept_influence]#p +100#!。|The button only records completion. It does not create or preserve a new market treaty.|
|`nesnd_supply_finish_autonomous_desc`|由本国掌管市场，安排对外通商。各项条件连续维持#v 12周#!，首次获得#v 2年#!通商收益。|在本国掌管的市场中继续经营。各项条件连续维持#v 12周#!后，首次获得持续#v 2年#!的[concept_influence]#p +100#!。|Requires market.owner=root before click; no market secession happens here. Avoid saying the button takes control of the market.|
|`nesnd_supply_rules`|#bold 货源#!\n纸张、工具、小武器无本国短缺，价格涨幅不超过#v 50%#!；东洲另需硬木。\n\n#bold 工场与人手#!\n所需建筑各有至少一座雇员达到#v 75%#!，且不缺生产投入。湖广为大学与军营；四川为工具厂，以及铁矿或伐木场；广西为纸厂与伐木场；东洲为港口与官署。招工困难时可查看[concept_pop_qualifications]、[concept_building_wage]与原料供应。\n\n#bold 生计#!\n全国无业劳动力不超过#v 12%#!；劳动力至少#v 5万#!的州不超过#v 20%#!。自给农民属于有业人口。全国无饥荒，粮食无本国短缺且涨价不超过#v 25%#!。\n现有无业劳动力：#v [Country.MakeScope.Var('nesnd_supply_unemployed').GetValue／0] / [Country.MakeScope.Var('nesnd_supply_workforce').GetValue／0]#!（#v [Country.MakeScope.Var('nesnd_supply_unemployment').GetValue／%1]#!）；超过地方失业界线的州：#v [Country.MakeScope.Var('nesnd_supply_critical_states').GetValue／0]#!。\n\n#bold 商路安定#!\n确定联络伙伴或依靠本国商帮，四项条件连续维持#v 12周#!。战争、破产、市场改变或任一条件不满足，连续周数重新计算。|#bold 货源#!\n纸张、工具、小武器无本国短缺，价格涨幅不超过#v 50%#!；东洲另需硬木。\n\n#bold 工场与人手#!\n所需建筑各有至少一座雇员达到#v 75%#!，且不缺生产投入。湖广为大学与军营；四川为工具厂，以及铁矿或伐木场；广西为纸厂与伐木场；东洲为港口与官署。招工困难时可查看[concept_pop_qualifications]、[concept_building_wage]与原料供应。\n\n#bold 生计#!\n全国无业劳动力不超过#v 12%#!；劳动力至少#v 5万#!的州不超过#v 20%#!。自给农民属于有业人口。全国无饥荒，粮食无本国短缺且涨价不超过#v 25%#!。\n现有无业劳动力：#v [Country.MakeScope.Var('nesnd_supply_unemployed').GetValue／0] / [Country.MakeScope.Var('nesnd_supply_workforce').GetValue／0]#!（#v [Country.MakeScope.Var('nesnd_supply_unemployment').GetValue／%1]#!）；超过地方失业界线的州：#v [Country.MakeScope.Var('nesnd_supply_critical_states').GetValue／0]#!。\n\n#bold 商路安定#!\n处于共同市场时，商贸安排自动满足；本国单独掌管市场时，可确定联络伙伴或由商人自行往来。四项条件连续维持#v 12周#!。战争、破产、市场改变或任一条件不满足，连续周数重新计算。|Explain the actual market read and retained independent-market policy choice. Prices, local shortages and domestic specialisations remain unchanged; no autarky requirement is added.|

## 精确代码修改

文件 `common/scripted_triggers/nesnd_supply_triggers.txt`，M/C匹配数量 `{'main': 1, 'candidate': 1}`。以以下块替换当前同名块：

```text
nesnd_supply_diplomacy_ready = {
    OR = {
        capital.market = { participants >= 2 }
        has_variable = nesnd_supply_self_reliance
        nesnd_supply_partner_valid = yes
    }
}
```

文件 `common/scripted_effects/nesnd_supply_effects.txt`，M/C匹配数量 `{'main': 1, 'candidate': 1}`。以以下块替换当前同名块：

```text
nesnd_supply_clear_partner = {
    remove_variable = nesnd_supply_partner
    remove_variable = nesnd_supply_partner_sponsor
    remove_variable = nesnd_supply_pending
    remove_variable = nesnd_supply_pending_sponsor
    remove_variable = nesnd_supply_trade_pending
}
```

该两处与双语文案详见同目录JSON。未对External、PHI、Tenasserim提出删除或机制改写。

## M/C逐文件指纹

|文件|一致|主MOD SHA256|
|---|---|---|
|`common/decisions/nesnd_external_decisions.txt`|True|`7b2df60305a037345b944c25cd2b42420917596fbd2dc0d86a288a7aaccb3b21`|
|`common/decisions/nesnd_supply_decisions.txt`|True|`4bc7d9b4a1e8b5e06b94631fb43b67e99dc7640627fd09b1b368508a3384ca0e`|
|`common/decisions/nesnd_tenasserim.txt`|True|`99efd560e5429988bfaf67461065909b802e573760ef2572cf5f87fcd3e8ad34`|
|`common/journal_entries/nesnd_external_journal.txt`|True|`7adda3f57c93331b8c85865f05874c9ce2b47fb44956365d44a3cf8a193d144e`|
|`common/journal_entries/nesnd_phi_finance.txt`|True|`53cb0d7e79dcfd1812f1d9d780408500f319c48504cf41dbe4de1f9aeba62ead`|
|`common/journal_entries/nesnd_supply_journals.txt`|True|`060d6d03ecffafd1696e90348d3593a36b2a8f9ef36eced1ce31fad8945e450a`|
|`common/journal_entries/nesnd_tenasserim.txt`|True|`c315413710c9e7a3c40150a16b0e49b3995c5a3124bc1b07accfbf918c78b807`|
|`common/on_actions/nesnd_phi_finance.txt`|True|`d47b15a1e5d9d35143f4dfba2e62ded99c310dbfd278e829d3b46fd40789a976`|
|`common/script_values/nesnd_external_preview_values.txt`|True|`ebe7a922e14c66797848d067e3742fedc36a68bb22c68ec515d36a1a8f52a3a3`|
|`common/script_values/nesnd_phi_finance.txt`|True|`89fbcce3c47ff0766424e1d801c54d6d2c41537cad14672cd8b135b28f40d26a`|
|`common/script_values/nesnd_supply_preview_values.txt`|True|`3e3bece79fd7b50943e8dbe4aa694ce87a300e91835b7bdf082027725c36f7bc`|
|`common/script_values/nesnd_supply_workforce.txt`|True|`df24560553736c6283be61d105b95009a526efb51bf4bc01d37d4caf753a3c71`|
|`common/script_values/nesnd_tenasserim.txt`|True|`6cd3668e92518fc3032567c15e8c0fd86547bd8c8617dfb24b4dc8579f5a0825`|
|`common/scripted_buttons/nesnd_external_buttons.txt`|True|`6c362de3f1bb51ec56f10478895e2fafa1666c19088ed586415227ff430083d6`|
|`common/scripted_buttons/nesnd_phi_finance.txt`|True|`d4e00cab515b3820884ba132e0e34b793f37e1a27f5111628f373da76a50d44a`|
|`common/scripted_buttons/nesnd_supply_buttons.txt`|True|`26a490567875574232c07a0af12e0e7ff71124773231fa406008319e6e7eb4b4`|
|`common/scripted_buttons/nesnd_tenasserim.txt`|True|`2f6fc209379deddaefbbb58581cdfb7aea9485c4e2383248bdc5541ee2d6393b`|
|`common/scripted_effects/nesnd_external_effects.txt`|True|`245da31f194fdf7281b14a63b438a23cf1d444f7c116e2c0b2fb74aa5054a873`|
|`common/scripted_effects/nesnd_phi_finance.txt`|True|`b930560066f6c62ce2cd5ba0e14ab194f5579c570e68180b152a7b628c383a80`|
|`common/scripted_effects/nesnd_supply_effects.txt`|True|`97602af82481cd82c2f47e73cad3ad1e28c1966d5cc8ebaa4d08e2116857b874`|
|`common/scripted_effects/nesnd_tenasserim.txt`|True|`44f0542ed2b3649d463f94fb4894a4cfc7aae6e74dddd3eaedcc9fdd1c3176b3`|
|`common/scripted_progress_bars/nesnd_phi_finance.txt`|True|`763b373c287650f65fbb2b7d59cbc185965d527f9ea976adea9dc0def17ead4d`|
|`common/scripted_progress_bars/nesnd_supply_bars.txt`|True|`7128f38ea7ffc8fce4109f2320f1097a6189febe8c9e5b0ab3716a6d18bfd46a`|
|`common/scripted_progress_bars/nesnd_tenasserim.txt`|True|`b7eada43d8d17c96ddf78f501373c689dda44774bec40adfc8f92613a844cc71`|
|`common/scripted_triggers/nesnd_external_triggers.txt`|True|`01861eb1cdc486108ddad1f77d83080a227fe18107614120162825dbd4b03227`|
|`common/scripted_triggers/nesnd_phi_finance.txt`|True|`394954cd72315c3a5142325506479cf8ba68d50578ebbb60966e95a40c91eb61`|
|`common/scripted_triggers/nesnd_supply_triggers.txt`|True|`620f10fbc185b30e94c5bd8425412ee1fda8e8ef0a40a75c8a00df311a07efd8`|
|`common/scripted_triggers/nesnd_tenasserim.txt`|True|`49c80c7cf8faa9354008eeacf0403585fdb9e63b0e71e68df4279ee9e2137180`|
|`common/static_modifiers/nesnd_supply_modifiers.txt`|True|`2f06d33a6c3108f0b1b29ef4757141f0929b47db2527ca9384d86d5de8ff732b`|
|`common/static_modifiers/nesnd_tenasserim.txt`|True|`6ad595c2c4730c37bf5dc8712460f4df7e182a70bbb7309d4d96dd3d2cceb0fd`|
|`events/nesnd_external_events.txt`|True|`66a88ac04086284176a99ae1f81c06037b45cb985f98ea87f637ce07e74648dc`|
|`events/nesnd_phi_finance.txt`|True|`81e95fc45107fb27ba5d6d597abf11012dbbd6d9da597b51c0b3ae678d6ed128`|
|`events/nesnd_supply_events.txt`|True|`2e27f4b54b2eb9be60bbfdd88d1b93617159bd428697d1f77ea715585800042b`|
|`events/nesnd_tenasserim.txt`|True|`9dfb578d5b90e9ad28557337128aa83327b1eb1f59e9563cec59a61fdd883520`|
|`localization/english/nesnd_external_l_english.yml`|True|`dd47977401e3e5595a51ddceaf2a1b2ef66f07dff93c61f4e1967c4476a1b4ee`|
|`localization/english/nesnd_phi_finance_l_english.yml`|True|`3b6d48081846a1b81f007b95b45c8f779b87f207653c44e91647215e30f4d574`|
|`localization/english/nesnd_supply_l_english.yml`|True|`01666a74b1ed64ab837c611056a35cb4bcc0de21accf92ba79b6811e253de665`|
|`localization/english/nesnd_tenasserim_l_english.yml`|True|`de21bb6b528a8840b113ba2df952095c21c043c2078b07af3921d7703e01e7fa`|
|`localization/simp_chinese/nesnd_external_l_simp_chinese.yml`|True|`bf5b2dbc3f3fa221b26d1f0509a194f68a21ffe826d22ef68c3a40575f1afa64`|
|`localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml`|True|`b230b2f2b40dfc8e6dbba37ad726164c67d50d84d8eee5fcf8c70c2e0c79b7e1`|
|`localization/simp_chinese/nesnd_supply_l_simp_chinese.yml`|True|`a919f92203aa9c072596e0c7b88b76972bb109553850ba84f11fd9a8cd221a52`|
|`localization/simp_chinese/nesnd_tenasserim_l_simp_chinese.yml`|True|`7f7c15e8a6fb9e3193fb357cc081347ea930c8733e7526bd332b81d352d5f575`|

检查结果：`{"no_code_or_main_edits": true, "engine_run": false, "scopes_equal": true, "exact_matches": true, "scope_files": 42, "different_files": []}`。精确文本匹配和双语引用对等是外部检查，不是游戏内验收。
