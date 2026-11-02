# 扶国—吴国军需采购：当前原生接口与最小合同

> **已撤回／不得用于实施（用户纠正，2026-11-02）**：用户明确否决本采购模块。共同市场中的日本产业应通过正常生产和市场买卖订单自然向吴市场供给；不得在此额外叠加预付款、采购成本优惠、合同或虚构定向交货。本报告以下内容仅保留为被否决方案与接口研究历史，不是当前规格。相关候选7文件、kind8与本地化已由主代理移除，从未合入主MOD。后续请读同目录 `market-model-native-review.md`。原生接口存在不等于用户授权采用其设计。

2026-11-02；Victoria 3 1.13.11 / build 24799966，使用当前GAME与引擎docs；只读研究、未开游戏、未改候选。G=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`，E=`WORK/references/engine-docs-1.13.11-20261031`。

**建议最小实现：同市场走“实际预付款＋六个月制造/采购优惠”，仅对真实在岗的JTK军工与船厂、当前吴政权USM、和平同市场关系生效；不同市场才考虑原生goods_transfer。** 一般资助只有钱和关系，不能作为“支持吴国供给”已完成；这里必须把付款、买方军需成本、卖方生产效果和持续资格绑成同一案件。

## 1. 有真实财政作用的原生依据

最直接的原生完整链是 **military_assistance条约**：

- G `common/treaty_articles/12_military_assistance.txt:21–41`：general_staff科技，source军需商品成本 `+0.10`，target `-0.10`，并有训练/经验/传播等效果。
- 同文件 `:43–64,70–115`：没有customs-union junior市场排除，但source军力须高于other、source rank至少target、source非革命国家、目标援助数量及重复条款受限。
- G `events/soi_events/00_ep1_persia_events.txt:477–489` 先 `can_create_treaty`，`:511–525` 之后 `create_treaty`，同一military_assistance对象/方向/条款。原生并非只写一句“提供援助”，财政修正是实际机制。
- G `common/history/treaties/00_historical_treaties.txt:74–77,120–123` 是GBR→POR真实历史条款。
- **不能直接拿该article给JTK→USM**：JTK通常比USM弱、可能没有general_staff，另有rank门槛。它是经济效果范本，不是可绕资格的捷径。

`country_military_goods_cost_mult`：E `modifiers.log:851–854` country mask，说明为“对必要军用商品的货币支出的增益或惩罚”；G `common/modifier_type_definitions/00_modifier_types.txt:526–533` 定义百分比，负数减少花费；G `company_types/00_companies_europe.txt:1506–1509` 的军工公司原生给 **−5%**。G `static_modifiers/00_ip4_04_modifiers.txt:371–375` 的 `captured_royal_arsenals` 同样给−5%。

制造端也有现成接口：G `company_types/99_basic_companies.txt:508` 使用 `building_shipyard_throughput_add=0.05`；G `company_types/00_companies_cots.txt:299` 使用 `building_arms_industry_throughput_add=0.1`。吞吐提高投入和产出，并不等于凭空增加免费库存。

本机造船链：`building_shipyard → pmg_base_building_shipyard → pm_basic_shipbuilding`（G buildings/01_industry `:318–338`，PMG/01_industry `:231–241`，PM/01_industry `:1908–1935`）给 `country_ship_construction_add=5` 与 `goods_output_clippers_add=40`。不要称它在向吴“交付manowars”；本版造船能力本身不是商品条约goods。

## 2. 同市场六个月合同：建议写入的最小闭包

### 真实入口与期限

以现有“JTK完成矿业→军工船业”的结果开采购按钮/子项目，但**每次报价、答复和合同维护还要核当前开工**。仅有 `arsenals_done` 是历史成果，不能永久代替实际产能。

候选country-scope资格形状（root=JTK）:

```text
c:JTK ?= this
is_country_alive = yes
has_variable = nesnd_jp_arsenals_done
c:USM ?= { is_country_alive = yes has_variable = tag_WUU_var }
market = c:USM.market
NOT = { has_war_with = c:USM }
# 若合同限定吴属时期：is_direct_subject_of = c:USM
# 若独立后允许自愿续订，必须由本次明确接受建立独立合作资格。
any_scope_building = {
    is_building_type = building_arms_industry
    occupancy >= 0.6
    weekly_profit > 0
    state = { market_access >= 0.9 }
}
any_scope_building = {
    is_building_type = building_shipyard
    occupancy >= 0.6
    weekly_profit > 0
    state = { market_access >= 0.9 }
}
```

这些指标原生依据见G `journal_entries/00_player_objectives_economic_dominance.txt:8–16,72–78`；E triggers的 `any_scope_building` country/state、occupancy/weekly_profit building、market_access state均已证实。如parent选 `is_at_war=no` 为双方完全和平，这比仅无双方战争更严格，是本项目明确选择，不是API强制。

最小财政/生产效果，使用独立修正名，示例幅度只是研究候选：

```text
nesnd_jp_wu_supplier_contract = {
    building_arms_industry_throughput_add = 0.05
    building_shipyard_throughput_add = 0.05
}
nesnd_jp_wu_buyer_contract = {
    country_military_goods_cost_mult = -0.05
}
```

效果在**USM答复国根**完成，预先冻结报价Q（正数）存在JTK案件变量；执行再核当前吴身份、双方不同/存活、原案件编号/宗属或自愿合作、同市场、产能、USM金库≥Q、无既有活跃合同：

```text
# Root=实际答复USM；scope:jp_sender 已确认仍是JTK。
add_treasury = { value = scope:jp_sender.var:nesnd_jp_procurement_quote multiply = -1 }
scope:jp_sender = {
    add_treasury = var:nesnd_jp_procurement_quote
    add_modifier = { name = nesnd_jp_wu_supplier_contract months = 6 }
    set_variable = { name = nesnd_jp_procurement_clock months = 6 }
    set_variable = { name = nesnd_jp_procurement_partner value = root }
}
add_modifier = { name = nesnd_jp_wu_buyer_contract months = 6 }
```

E effects `:526–529` 证明add_treasury正负数；G `british_raj_events.txt:221–232` 有跨国金库数值转入的真实caller。这里明确等额扣USM、加JTK，不能只向JTK凭空发补贴。Q必须保存一次，扣款后不用另一套现值重算。

**维护和清理是合同的一部分：** 两国存活、USM仍吴、实际原对象/关系仍允许合作、同市场、和平、JTK工厂开工持续成立。失效应移除两边本合同修正并清clock/partner，保留建筑和产业done；不得月月 `add_modifier months=6` 续命，也不得因换宗主自动改付款方。合同仅一个JTK→USM，对USM侧另做维护入口，可在JTK灭亡后清买方优惠；只从JTK维护会让残余优惠保留到期。期限本身已由months=6硬限，再用月度/已有关联事件做提前终止；月度维护意味着最长一个月检测迟滞，不能宣称每日即时终止。

付的是既定六个月预付采购/产能合作费；若提前违约不退款，必须作为约定而非隐性误扣。若要按未履行月份退款，需要另记余额，不属于最小闭包。清理不发新的资金，不重置采购冷却/已付款编号。拒绝或旧回信失效不可生成任何成本优惠。

**可诚实说明的经济行为：** 吴国金库真实减少，扶国金库真实增加；合同期间吴军需采购的货币支出下降，扶国在岗工厂投入/产出提高，共同市场因此可获得额外生产。它没有逐件卸货记录、没有保证吴独享扶国产出，也不强制库存转移。玩家文字应写“预付军需订金、整顿采购／承办军需”，不能写“已交付X件轻武器”。这满足实际采购财政结果，且清楚保留模型边界。

Q不能直接用 `military_expenses * 0.05 * 26` 声称精确抵消优惠：E targets `:1105–1112` 的military_expenses含奴隶/工资/商品，并非纯军需商品支出；−5%也与现有修正合并。报价应是明确限额或基于可核的当前收入/财力，记录一次扣款、6个月和重复上限，勿把全年GDP当订金。

## 3. goods_transfer：跨市场时的准确语法与资格

原生来源链：G `common/history/treaties/00_historical_treaties.txt:94–101` POR→GBR wine条款 → G `common/treaty_articles/13_goods_transfer.txt` → goods数据库（`common/goods/00_goods.txt:18–26` small_arms、`:234–242` clippers）→对应图标，原生treaty界面展示。E effects `:1030–1083` 包含完整create_treaty并直接给goods_transfer例子。

**真实屏蔽同市场原因**：article `visible:25–31` 要求两国 `is_junior_in_customs_union=no`，`requirement_to_maintain:51–65` 对两侧重复要求。因此JTK处在USM共同市场的junior时条款不可持续；不能靠create_treaty强推。实施还应显式 `NOT={market=c:USM.market}` 分路，防同市场的特殊非junior情境。

其他必要条件：`international_trade`（`:21–23`）；双方市场可贸易到达、双方有港口或市场相邻（`:33–49`）；source供给网≥.75或两国相邻（`:101–108`）；goods可贸易且双方进/出口额度仍有余（`:152–161`）；Qgoods至少10且不超双方剩余额度（`:164–193`）；原生重复条款检查（`:111–144`）。每周不履约会freeze（`:67–97`）。不能以“own military industry”代替这些跨市场条件。

建议两个国家均独立或有已核外交权限，当前仍为吴、无双方战争，且双重检查 `can_create_treaty` 与显式market/technology/access。当前docs中can_create_treaty的示例仍有旧 `resource_transfer/good`，**采用真实当前article及effect的 `goods_transfer/goods`**，不要抄旧别名。

下面以10单位轻武器给出结构；10是原生最小量示例，实际值需按国产量/市场余量定。**这是进入原生商品流的真实条款，不是关系修正。**

```text
# Root=JTK；scope:jp_buyer 已固定并复核为当前吴USM。
# 双方批准及所有显式资格完成后，在effect内部再次检查同一完整条约：
if = {
    limit = {
        NOT = { market = scope:jp_buyer.market }
        is_junior_in_customs_union = no
        scope:jp_buyer = { is_junior_in_customs_union = no }
        can_create_treaty = {
            first_country = root
            second_country = scope:jp_buyer
            is_draft = no
            binding_period = { months = 6 }
            articles_to_create = {
                {
                    article = goods_transfer
                    source_country = root
                    target_country = scope:jp_buyer
                    inputs = { { goods = g:small_arms } { quantity = 10 } }
                }
            }
        }
    }
    create_treaty = {
        name = nesnd_jp_wu_goods_contract
        first_country = root
        second_country = scope:jp_buyer
        is_draft = no
        binding_period = { months = 6 }
        articles_to_create = {
            {
                article = goods_transfer
                source_country = root
                target_country = scope:jp_buyer
                inputs = { { goods = g:small_arms } { quantity = 10 } }
            }
        }
    }
}
```

`can_create_treaty`→`create_treaty`配对为上面的Persia当前原版caller所证实。普通历史create_treaty并不足以证明effect会自动执行所有交互visible/possible检查，故不要省显式guard。原生商品转移不自动向JTK付采购款，可与同笔已同意预付款配合；**若用此真实goods条款，USM不要再无条件叠同市场−5%优惠，避免把同一履约算两次。**

**binding_period不是到期销毁。** 它约束退出的绑定期（money article on_break直接按remaining_binding_period算代价），无文档说明结束后article自动消失。有限6月商品合同需保存确切创建的treaty对象，6月后对该对象执行E effects `:37390–37398`：

```text
scope:the_exact_procurement_treaty = {
    withdraw = { country = scope:jp_supplier apply_break_penalties = no }
}
```

country必须仍有效且受该treaty约束。当前create_treaty文档没有可用on_created返回scope；可在严格无已有同方向同goods条款的前置下，创建后遍历JTK `every_scope_treaty`、`binds=buyer`、对应article source/target/input_goods精确标记/保存；别宽泛撤销所有USM/JTK条约。若不愿新增该生命周期闭包，最小上线只做同市场有期限财政合同；跨市场保留玩家原生条约入口，不伪造六个月自动结束。

## 4. money_transfer的定位

G `common/treaty_articles/05_transfer_money.txt:1–72` 是真实持续货币支付，source付target；无customs-junior限制，required quantity；central_banking科技、source非default、quantity、互斥等仍成立。G `events/japan_events/ep2_meiji_restoration.txt:1537–1555` 给完整实际create_treaty。它可以作为同市场长期采购付款，但单独money_transfer仍不证明产能/商品履约；也同样需要确切treaty识别与到期withdraw，复杂度高于一次预付款。

因此当前最小方案优先预付款+6月两侧修正+清理。原生article可作为科技与外交权限充足后的扩展，不强制JTK/USM早期签不合法协议。

## 5. 追加数值核验：固定20,000的吴国预算基准

引擎 `event_targets.log`/`triggers.log` 与GAME `common/script_values` 未找到 `military_goods_expenses`、`weekly_military_goods_expenses` 或等价的仅军用商品预算script value；只有包含奴隶/工资/商品的 `military_expenses`。G `gui/budget_panel.gui:844–846` 确有 `GetPlayer.GetMilitaryGoodsExpenses`，这是GUI数据函数，不能据此写一个虚构的同名Jomini数值字段。当前最小可实现方案因此使用固定报价，而非假称动态读取纯军需预算。

已有真实吴政权证据：`WORK/reports/runtime/20261101T003815Z/evidence/Jan27-DP-before-backdown/native-pre-annex-records.json` 的 `countries["730"]`，dynamic_country_name明确 `USM_WUU_monarchy`。其country_building_budget.expenses.military_goods.values为：

|每周分项|数值|
|---|---:|
|building_naval_fortification|16,724.68571|
|building_naval_logistics_center|3,875.17138|
|building_army_logistics_center|15,814.40751|
|合计|36,414.26460|

以该旧实测规模粗估，12周×5%为 **21,848.56**；约26周×5%为 **47,338.54**。固定预付款 **20,000** 接近半期优惠，并占六个月粗估优惠42.25%。其他旧USM参考规模为34,398.96、34,934.38、42,579.45/周军需商品，12周×5%报价约20,639、20,961、25,548，也支持20,000作为有界初值，而不是泛用外资资助的25k–150k。

该估算仅证明报价量级有已有预算参考；真实−5%与现有成本修正叠加、军队/价格在六个月内变化、当前候选与旧存档不同，不能宣称玩家保证净赚或必然节省47,338。固定20,000不会自动适应极小化吴国；AI仍须金库够付与实际合同资格，玩家明确看见数额再同意。取值与来源SHA已独立存 `wu-procurement-budget-benchmark.json`。

同市场比较也已核原版真实字面实例：G `events/spanish_flu_events.txt:958,1021` 在country迭代里用 `market = root.market`；G `events/balkans_events/the_grand_collapse_events.txt:55,84,115` 用 `this.market = root.market`。所以JTK country scope下 **`market = c:USM.market`** 是相同原生scope比较；c:USM先有存在/存活guard即可。无需绕道market_capital。

## 边界与证据

已证明接口、作用域、数据库与原生实例；未启动游戏。跨市场can_create_treaty的当前goods输入形状由实际create_treaty/article加引擎接口组合推得，需候选静态工具核验和以后定向引擎观察；不能写为本次实机通过。真实经济验收应观察两国同额金库变化、USM军需费用修正、JTK吞吐及开工、停产/战争/改属/吴身份消失时两边清理、到期不续命及重复请求不叠加。

### 关键源SHA-256

- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\treaty_articles\12_military_assistance.txt` — `7d4fe31295bd5791b1f01873eea8255fd9dc4ec215ba7792ed2afa4c884b0514`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\treaty_articles\13_goods_transfer.txt` — `50d4e8ae301c522a278598c9f315430417fc34a3a8bbf536b0d3a5cf371b607d`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\treaty_articles\05_transfer_money.txt` — `6f59db04c429ab06eb6844cfadc87c3a54525e9e447586f19d0e40c780198112`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\events\soi_events\00_ep1_persia_events.txt` — `7f86799585cd6bc5936ac1b863548837eb7d937bf24ae05dc1527d78b3521128`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\history\treaties\00_historical_treaties.txt` — `a1c7e519ef1b07e2491f473ce0f94e6abae718fe725d68bcd8644d2432602f4e`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\modifier_type_definitions\00_modifier_types.txt` — `b07822b507cdf169cc7df5edd41214857a80d95ce6ba79de7d11e688a86a6dbe`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\company_types\00_companies_europe.txt` — `15c2eff77d6f9830ba0258aede08f8116b19287c737e4147db91560c276f8817`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\company_types\00_companies_cots.txt` — `1c391432856c9444fb2cde4e3f4bb83c7433d0bbe6859c3aad988ed4e7b43ece`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\company_types\99_basic_companies.txt` — `8da8c02afc1e1ede66937862865fc206c73f9697346082acc10ffe5dc90e6623`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\static_modifiers\00_ip4_04_modifiers.txt` — `a514e1fa61aa2178182506c90eb138f4bea53ad341fc20f9dbc1b6dbc5a7bf5c`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\goods\00_goods.txt` — `e5d8ed5e5deaf3d2c7193bc6b749555c63c78631aecaf87784a2e34051ddfa48`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\events\japan_events\ep2_meiji_restoration.txt` — `358d0b9d3b8b356f102e14caf469f873087f2ee657768a5ef6aa64f4101084bb`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\buildings\01_industry.txt` — `7e41e84ab11ab85715badbea648f1ce938f989b00761f47882c65de986fcf25c`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\production_method_groups\01_industry.txt` — `070243064f5a07d84e25ce773686b0e5a9e2e7d0b942798d74caf88ea8f5b681`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\production_methods\01_industry.txt` — `d0abb71f6ba922f46e1e512810053d1206a3cbfd8a2ff419d8a66c87b8a36886`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\journal_entries\00_player_objectives_economic_dominance.txt` — `7fb15aab732c9ce9f93c4f3a86265de98aaef64b1d9fdb4a4dd8174ec8e12599`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\events\british_raj_events.txt` — `9e3918a3a19bc34401d5af419b8a25fbf15ffa61c6169efddfd310a6fcb7db7c`
- `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\references\engine-docs-1.13.11-20261031\effects.log` — `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`
- `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\references\engine-docs-1.13.11-20261031\triggers.log` — `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`
- `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\references\engine-docs-1.13.11-20261031\event_targets.log` — `cc12b15da310d0d8ef10a9209107b4d2298a882fa6ee038c202650e3c9bd7c71`
- `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\references\engine-docs-1.13.11-20261031\modifiers.log` — `1d8ea1f6fb6bc0e2677d4591d45e21ef8f94ba4931074aa871583d61a63ceeff`

追加预算接口与同市场实例SHA：

- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\gui\budget_panel.gui` — `a21dbd8f14ffbfd6fdcf942d36771ee42fb7bd5c55dea21aca3dbb549b38af90`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\events\spanish_flu_events.txt` — `dae1e93887b03a12bc55007c0a6c9d42e5877cbcff9e7ee2123737223d91708f`
- `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\events\balkans_events\the_grand_collapse_events.txt` — `f03774a0931676331f55ac45a8316a9d8a4e00d53ec70596e6b7fcfc43316e78`
