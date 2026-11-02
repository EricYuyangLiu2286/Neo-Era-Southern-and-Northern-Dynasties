# 日本开发：原版完整链条与接口证据

2026-11-02；研究基线 c4bbc19；只读研究，未改玩法、未开游戏。`catalog.py status`：Victoria 3 **1.13.11 / Steam build 24799966，CURRENT，0 changed**。引擎文档由本机游戏在 2026-10-31 导出；本次只读其接口，不把源码组合当成 ENGINE_PASS。实现依据为方案修订2/3。

路径：G＝`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`；M＝主 MOD；E＝`WORK/references/engine-docs-1.13.11-20261031`。文末列本次读取的文件 SHA-256。下列“候选组合”由已证实原生接口组成，并非已经实机运行的成品。

## 1. 日志入口、新国家与三 TAG 生命周期

### 已证明的原生链

- **JE激活**：G `common/journal_entries/journal_entries.md:15–51`：自动激活必须同时满足 `is_shown_when_inactive` 与 `possible`；`add_journal_entry` 跳过二者，但照样执行 `immediate`。因此不要仅写 `possible` 而遗漏可见入口，也不要让入口依赖该JE的 `immediate` 才会置起的变量。
- **真正的国家根**：同文件 `:1–5,73–104,156–167` 明确 owning-country context 下根是国家；`scope:journal_entry` 才是JE。country变量直接存国家，bar操作切到JE。`on_invalid` 用于清理和静默退出。
- **阶段式原生范本**：G `events/meiji_restoration.txt:26–46` 添加总JE；`:133–216` 对已完成工业/外交条件直接登记成果，未完成才加子JE。G `common/journal_entries/00_meiji_restoration.txt:640–880` 为总日志→工业/军队/外交→各自country完成变量；工业不破产、城市化与铁路，军队实际法律/科技/兵营PM/部队，外交实际独立与承认。应借结构，不能照搬原版 JAP/天皇/emperor_var/DLC依赖。
- **继承并非全自动**：G `journal_entries.md:402–407`：`transferable` 只控制玩家释放/革命换国时JE迁移，外部country变量不因此自动继承；胜利革命的 `can_revolution_inherit = yes` 则与父国变量继承有关。`transferable=yes` 会阻止革命继承。不能以 `transferable=yes` 代替三国统一成果交接。
- **按国家月度入口**：E `on_actions.log:1373–1375` 明确 `on_monthly_pulse_country` 的 root 是country；M `common/on_actions/ce_code_on_actions.txt:30–38` 和 `nesnd_japan_lin_regency.txt:1` 是现成接入模式。没有查到“任意独立发生时统一触发”的可靠专用hook；不能误用 `on_country_released_as_independent` 代表所有战争/外交独立。

### 建议入口（候选组合）

```text
is_shown_when_inactive = {
    OR = { c:JAP ?= this c:JTK ?= this c:JIM ?= this }
}
possible = {
    is_country_alive = yes
    is_subject = no
    NOT = { has_variable = nesnd_japan_development_completed }
    NOT = { has_variable = nesnd_japan_development_entered }
}
immediate = {
    set_variable = nesnd_japan_development_entered
    # 已达成子项先登记，再只开尚未完成子项；不统一清零旧成果。
}
```

以上可以覆盖旧档已独立和今后任意方式独立；若“立即”必须是同日而非JE检查周期，已知本项目自主答复/分国的落地effect末尾显式调用幂等同步effect，同时保留自动JE入口或月度旧档修复。先完成实际关系，再开发展；不要在临时 `make_independent` 与紧接着创建博弈之间发发展奖励。

三TAG共享一个幂等country维护effect即可，调用时先 `is_country_alive=yes`、TAG/继承身份成立。进度与已领奖标记以country保存，国际请求另外保存双方对象和有效期。共享全局变量只能表示世界事实（如历史分封发生），不能用来替三国各自完成。

|发生情境|应消费的事实与动作|
|---|---|
|JAP/JTK/JIM从属变独立|实际 `is_subject=no` 后激活一次；发展完成另受实际主权及行动条件约束|
|独立者又成属国|暂停发展推进/转自主阶段；保留工业、法律与已完成变量；不清 `completed/rewarded` 后重发奖励|
|改属CNE、其他宗主、间接属国|按实际 `overlord` 更新新案件，旧案件清理；不把USM标记当宗主关系|
|普通失州|目标重算；产业与建设不删除；暂失条件并不自动永久失败|
|合并/改号|在吞并前显式取各方已经完成成果的并集，胜者每种全国奖励至多一次；不同人的已领奖收益不叠三份|
|国家灭亡/对象不存在|清理仍存活的对方请求；所有目标解引用需先存在/存活/仍属相同案件|
|再次释放|清理父国错继承的身份/活跃案件，建立新国家阶段；继承何种成果须按明确来源账，不凭重置全部变量实现|

本项目的两个必要入口：M `common/scripted_effects/nesnd_japan.txt:80–100,150–170` 的JTK/JIM `create_country.on_created`；M `nesnd_japan_recovery.txt:52–84,180` 的JAP恢复初始化。现有恢复初始化会把所有非japanese主流文化删掉，**JIM加入ce_wuu必须发生在该清理之后/在JIM自身分支，且保留japanese**。本次不改这些文件。

## 2. 安全的经济、人口、就业和军队取值

|指标|安全作用域与形状|当前原生证据/限制|
|---|---|---|
|全国存在某类建筑|country `any_scope_building = { is_building_type = building_arms_industry ... }`|E triggers `:3761` 明确country/state；G经济目标JE `:72–78` 实用。无需误套只能州用的模板|
|实际经营|building `level >= N occupancy >= 0.75 weekly_profit > 0 is_subsidized=no`|G `00_player_objectives_economic_dominance.txt:8–16`；occupancy是0–1，weekly_profit是本周货币利润。不能把一个州的level门槛写成全国级数之和|
|全国建筑级数|country script_value `value=0 every_scope_building={limit={is_building_type=...} add=level}`|基于原生迭代/数值；若目标要求在岗产能，可加 `occupancy`/利润筛选。全国总和与单建筑门槛是两种设计|
|全国人口|country `total_population`|E triggers `:14631–14636`；G `building_values.txt:26–38` 原版直接除以此值并guard `>0`|
|本国州人口|state `state_population`|E triggers `:14458`。只代表state交集；不等于整个state_region人口|
|单pop全部人口|pop `total_size`|E triggers `:14659`；本项目 `nesnd_qe1_identity.txt` 数值文件已有加权求和；不要把workforce当总人口|
|劳动力/家属|pop `workforce`、`dependents`；`is_employed=yes/no`|E triggers `:14829,:9672,:11561`。就业率应以workforce求和为分母；每pop的count/percent不是按人口加权|
|GDP|country/state `gdp`|E targets `:341–344`：**年度预测GDP**。不是金库、每周收入或可以原额发放的资金|
|全国人均GDP|country `value=gdp if={limit={total_population>0} divide=total_population} else={value=0}`|G `ep2_japan_values.txt:311–320`为州人均GDP范式；country分母按building_values的正数guard|
|识字|country/state/pop `literacy_rate >= 0.5`|E triggers `:12776`；G `00_east_indies.txt:174` 和 `00_hawaii.txt:31`；比例0–1。引擎log示例有旧名 `literacy`，以实际原版 `literacy_rate` 为准|
|全国/州SOL|country/state `average_sol`|E targets `:1517–1520`；G `00_standard_of_living.txt:10,14,83`。`standard_of_living` 是pop接口，不能直接country用|
|军队规模|country `army_size` 与 `army_size_including_conscripts`|E targets `:888–907`；G `ai_script_values.txt:103–143` 基于人口、收入及兵制定规模。不能对京都/大阪JIM强塞300营|
|军用舰维护|country `military_ship_maintenance_fulfillment >= 0.9`|E triggers `:13109`；本项目既有海军准备条件已用。不等于某次军需合同已经交货|

GDP、SOL、就业类数值只作观察/门槛；不是凭空加库存的效果。SOL需维持一段时间时按月累积连续合格月数，不合格清零；该计数是持续性验证，不应永久直接加SOL冒充完成。

给实施者的可直接取用形状（country root）：

```text
nesnd_japan_population = { value = total_population }
nesnd_japan_sol = { value = average_sol }
nesnd_japan_literacy = { value = literacy_rate }
nesnd_japan_gdp_per_person = {
    value = 0
    if = { limit = { total_population > 0 } value = gdp divide = total_population }
}
# 初始化一次：set_variable = { name = nesnd_japan_gdp_baseline value = gdp }
# 之后的增长率为相对基准比例：0.10即增长10%，不是十个百分点GDP。
nesnd_japan_gdp_growth = {
    value = 0
    if = {
        limit = { has_variable = nesnd_japan_gdp_baseline var:nesnd_japan_gdp_baseline > 0 }
        value = gdp
        divide = var:nesnd_japan_gdp_baseline
        subtract = 1
    }
}
```

未找到可直接用于国家的原生 `gdp_growth` trigger；用上面的有界分母/冻结基准组合。G `common/script_values/ip4_cuba_values.txt:14–31` 原版在CUB仍存在时读当前GDP，否则读取保存的 `cubas_last_gdp`，证明当前值/持久快照的数值读取；G `ep2_japan_values.txt:174–178` 原版比较 `gdp >= var:tenpo_gdp_goal`。全国GDP包含扩张所得，若要“生产率改善”应另看人均GDP/本国产量，不暗称固定领土有机增长。

军制/教范不应杜撰一个 `military_doctrine` 总分：直接复用G Meiji军队JE `:798–823` 的 `has_technology_researched=napoleonic_warfare`、`NOT has_law_or_variant=law_type:law_peasant_levies`、`any_scope_barracks` 排除 `pm_no_organization/pm_samurai_training`、`any_military_formation { is_army=yes any_combat_unit { has_unit_type=unit_type:combat_unit_type_irregular_infantry } }`；再按人口规模要求 `army_size`。识字是0–1的 `literacy_rate`，可直接country条件与数值读取；学校投资使用 `institution_investment_level={institution=institution_schools value>=N}`，后者代表投入并不等于已经达到识字率。

### 原生产业闭包

G `common/buildings/01_industry.txt:411–432`：`building_arms_industry`，组 `bg_military_industry`，gunsmithing，`pmg_firearms_manufacturing` → G `common/production_method_groups/01_industry.txt:302–312` → G `common/production_methods/01_industry.txt:1910,2312–2334` 的 `pm_muskets`：workforce-scaled消耗铁10、硬木10，产轻武器30；level-scaled职业容量共5000。对应building/PM图标真实存在，沿用G `gui/journal_entry.gui` 与原生JE条件展示即可，无需新增UI脚本。

**版本差异：** G buildings `:318–338` 的 `building_shipyard`（旧复数名为alias）→ PMG `:231–241` → PM `:1908–1935`：`pm_basic_shipbuilding` 同时给 `country_ship_construction_add=5`（workforce_scaled）及 `goods_output_clippers_add=40`。不能照旧版臆造“military_shipyards生产manowars”的链。造船目标检查真实船厂、在岗/PM、科技、船舰结果；该country造船能力不是可用商品条约直接转出的商品。

## 3. 每国每月30%，一州、至多州总人口10%，宗教不变

### 接口与算法

- E effects `:646–649`：`change_pop_culture` **仅pop scope**，`value`是该pop被转换的比例；`convert_population` `:797–800` 是宗教转换，不能用来改文化。
- E effects `:30870–30874`：`random_scope_state` 从country选择一个本国state，不能用state_region扩大到外国交集；`:4762–4766` `every_scope_pop` 支持state。
- G `common/script_values/event_values.txt:294–299` 原生 `japanese_culture_fraction` 直接 `add = "culture_percent_state(cu:japanese)"`。可准确取当前州目标占比。
- G `events/brazil/culture_south_america.txt:381–391,888–895` 保存目标文化后，对匹配pop调用 `change_pop_culture`，不同时调用宗教效果。
- M `ce_scripted_effects.txt:2–33` 是华夏文化转换参考，M `nesnd_qe1_identity.txt:7–31` 是monthly/阈值参考；**西秦的每州每pop 0.005、低团结复归及转换临时cohort不可照搬**。其 `:36–43` 故意另改宗教，本日本规则不能调用该效果。

令选中州总人口N，合格非目标人口P，则转换人数 `C=min(0.10*N,P)`，对每个合格pop使用同一比例 `q=C/P`。当合格定义仅是“不是目标文化”，等价于 `q=min(0.10/(1-target_share),1)`。必须先冻结q，再迭代；在每pop中重算会随着前面已转换的人口改变分母，从而超过本月额度。

如果另有资格筛选，直接求和 `every_scope_pop={limit={...} add=total_size}` 得P；不要再以 `1-target_share` 代替。

### 候选组合（JAP/JTK；JIM替换目标为ce_wuu）

```text
# state-scope scripted value；调用者已保证存在非目标人口。
nesnd_japan_conversion_fraction = {
    value = 0.1
    divide = {
        value = 1
        subtract = "culture_percent_state(cu:japanese)"
        min = 0.00001
    }
    min = 0
    max = 1
}

# country-scope effect，仅从唯一 monthly owner 调用一次。
if = {
    limit = {
        has_variable = nesnd_japan_unity
        var:nesnd_japan_unity > 75
        any_scope_state = {
            state_population > 0
            any_scope_pop = { NOT = { culture = cu:japanese } }
        }
    }
    random_list = {
        70 = { }
        30 = {
            random_scope_state = {
                limit = {
                    state_population > 0
                    any_scope_pop = { NOT = { culture = cu:japanese } }
                }
                set_variable = {
                    name = nesnd_japan_conversion_fraction_frozen
                    value = nesnd_japan_conversion_fraction
                }
                every_scope_pop = {
                    limit = { NOT = { culture = cu:japanese } }
                    change_pop_culture = {
                        target = cu:japanese
                        value = state.var:nesnd_japan_conversion_fraction_frozen
                    }
                }
                remove_variable = nesnd_japan_conversion_fraction_frozen
            }
        }
    }
}
```

`state`从pop的链接由E targets `:330–333` 支持。min是下限、max是上限（G building_values `:15–16,38–39`），顺序无歧义；目标文化应分别写固定版本或以显式目标culture保存scope，不从主流文化列表随机取。JIM保留japanese+ce_wuu主流，转换目标始终ce_wuu，宗主变化、林死亡都不回滚人口。

同样可按父scope写成 `change_pop_culture = { target = cu:japanese value = prev.var:nesnd_japan_conversion_fraction_frozen }`，前提是紧接state→`every_scope_pop`，pop effect中间没有再切其他对象；上例用显式 `state.var` 减少重构时prev层次漂移。原生州文化数值的**字面语法**就是 `value = "culture_percent_state(cu:japanese)"`（原版同义写 `value=0 add="culture_percent_state(cu:japanese)"`）；江南版写 `value = "culture_percent_state(cu:ce_wuu)"`。

月度单次保证只能有一个owner：国家on_action **或** unity JE `on_monthly_pulse.effect`，不要两处都调用。三国各自一次意味着最多三次独立国家抽签，不是共享一次全局骰，也不是州/每pop各抽30%。成功后选一合格state，不把相同地区外国owner-state转换。

边界算例：N=1000、P=1000→q=.1，C=100；P=500→q=.2，C=100；P=60→q=1，C=60；P=0→不进入。比例与整数人口的实际舍入、同循环split/merge处理仍属于引擎边界，本次未开游戏，需单次定向观察后才能承诺到人头精度。若要求硬性逐人不超过额度，可在外部检查中用真实AST评估极值，并在实测中检查前后文化人口总量与宗教总量；不能用四个算式宣布实机通过。

## 4. 实际宗主、自主答复与原生独立博弈

### 对象/关系

E targets `:1314–1317`：`overlord` 是**直接宗主**；`:1385` 是最高宗主。E triggers `:11539` 的 `is_direct_subject_of` 排除间接属国；`:12447` 的 `is_subject_of` 包含间接关系。应在发信时保存请求方及当时直接宗主，在选项显示及执行时重新验证 `requester.overlord = responder` 或 `is_direct_subject_of=responder`。改属不能让新宗主自动收到旧国同意，USM内部改明吴也不能沿用过期身份承诺。

### 原版完整链

G `common/diplomatic_actions/38_subjects_increase_autonomy.txt:107–188`：subject组、`requires_approval=yes`，native possible核 `liberty_desire>=75`、`can_increase_autonomy=yes`、科技例外、催化剂冷却、不得正在敌对博弈；accept在**属国country scope**执行 `increase_autonomy=yes`、自由欲−30、双向停战60月，并记录外交催化剂。同文件 `:1–62` 则是宗主主动授予型。

E effects `:9707–9710` 证明 `increase_autonomy`；`:677–680` `change_subject_type` 也合法，但直接指定dominion不能代替所有文化/认可/殖民类型的原生晋级。G `common/subject_types/00_subject_types.txt:1–81` 等定义自治梯度及可否自主开博弈，宜用原生晋级并先核 `can_increase_autonomy`。

同意完全独立时 `make_independent=yes` 是country合法效果（E `:9819–9822`），只在双方明确同意并执行时调用；这并不代表国家发展阶段全部完成。

G `common/diplomatic_plays/00_diplomatic_plays.txt:202–229` `dp_independence`：原生目标 `independence`，要求不能再提高自治，或近期被拒绝提高自治，并检查关系阻挡。`:254–280` `dp_increase_autonomy` 使用近期被拒绝催化剂。

G `common/war_goal_types/10_independence.txt:1–52`：`kind=independence`、`validate_independence`、目标国在战中，且 `valid={root.overlord=scope:target_country}`。结算由引擎原生kind做；不要另手搓胜负/先吞并再释放。

**最直接实际caller**：G `events/british_raj_events.txt:276–280`，属国根里直接：

```text
create_diplomatic_play = {
    target_country = scope:overlord_scope
    type = dp_independence
    add_war_goal = {
        holder = scope:overlord_scope
        target_country = ROOT
        type = annex_country
    }
}
```

这个原版例子没有先 `make_independent`，也没有 `war=yes` 跳过正常升级。日本按钮可照scope形状，但不应无条件照搬宗主反要求 `annex_country`；由当前设计选择合法反要求。入口与effect内均核国家存在/存活、仍是该直接宗主、无重复博弈/战争、停战、原生关系/自主资格。`is_active_in_diplomatic_play` 的原版组合见G scripted_triggers `:1737–1743`。

E `create_diplomatic_play` docs `:909–923` 的文字仍以旧“scope target”方式说明，遗漏current `target_country`；**当前原版实际caller**证明本版本 `root initiator + target_country` 的形状。不能凭文档旧措辞反转双方。

不在延迟回信路径里直接无guard调用G `diplomatic_play_has_no_relations_blockers`：它依赖预设 `scope:target_country`，包括直接/最高宗主读取（G scripted_triggers `:1753–1785`）。先保存/guard此scope，或用项目自己的明确对象关系trigger。

## 5. 同市场供给：合法、可核验的替代链

G `common/treaty_articles/13_goods_transfer.txt:25–31,51–65` 明确双方都不能是关税同盟junior；possible另核市场可达、双方港口或市场接壤（`:33–49`）；can_ratify核供给网/邻接及重复条款（`:101–144`）。不能通过 `create_treaty` 绕开这些条件伪造一个运行中非法条约。

### 可实施的同市场合同定义

把同市场部分明确命名和描述为**建设资助／军需产能合作**：宗主实际支付一笔钱，受资助方在共同市场中建立和维持本国轻武器/火炮/船厂产能。该方案有真实财政与生产后果，但不是定向交付X件武器，不能在文案宣称有实物交付账。

原生现金接口：E effects `:526–529` `add_treasury` 可加减；G `british_raj_events.txt:221–232` 实际将原国家金库数值给宗主。现金双边转移应在同一已复核effect里冻结金额，再付款方负数、收款方正数；两边使用同一冻结金额，不能扣款后重新读gold计算入账。

```text
# 在付款方country，双方已明确接受、saved recipient有效、金额已冻结。
if = {
    limit = {
        exists = scope:recipient
        scope:recipient = { is_country_alive = yes }
        gold_reserves >= var:nesnd_japan_grant_amount
        var:nesnd_japan_grant_amount > 0
        market = scope:recipient.market
        NOT = { has_war_with = scope:recipient }
    }
    add_treasury = {
        value = var:nesnd_japan_grant_amount
        multiply = -1
    }
    scope:recipient = {
        add_treasury = root.var:nesnd_japan_grant_amount
    }
    # 仅在同一成功分支登记本案件paid/received，不在显示或发信时登记。
}
```

片段根必须确实是付款方；从别的嵌套root调用需改成保存的payer scope。数额需另核收入、金库、期限与重复领取，不在研究里暗定平衡值。一次款不可作为永久无成本无限合同开关；同一partner/case一次支付，过期/拒绝/对象改变统一清理。

生产证据：E targets `:1491–1495` `sg:small_arms` 从state到StateGoods；E triggers `:14397–14403` `state_goods_production` 是本state实际总产量。G history贸易 `00_historical_trade.txt:129` 有 `sg:artillery` 实例。候选全国产量：

```text
nesnd_japan_small_arms_production = {
    value = 0
    every_scope_state = {
        # 若合同要求可送共同市场，先筛 market_access >= 0.9
        sg:small_arms = { add = state_goods_production }
    }
}
```

此数值应与“受资助方与付款方同市场”、本国产能真实开工相交。共享市场 `market_goods_production` 包含外国生产，不能用它证明日本属国产了武器。`sg`链与state production均由引擎docs证明，但组合本次未运行；若需要最大稳妥的初版，可用已大量出现的全国 `any_scope_building` + type/occupancy/weekly_profit门槛，再在实测中加严实际产量。

可选择的持续现金条约：G `common/treaty_articles/05_transfer_money.txt:1–72` 的 `money_transfer` 没有junior市场排除，但解锁科技central_banking、付款方default、quantity与条约互斥仍须遵守；G `events/japan_events/ep2_meiji_restoration.txt:1537–1555` 给出完整 `create_treaty { first_country second_country is_draft=no binding_period ... articles_to_create={ { article=money_transfer source_country target_country inputs={{quantity=5500}} } } }`。1836早期无法证明合规时优先上面的一次付款，不强制创建未解锁条约。

离开市场/改属/战争/独立时终止未来支付和旧供给义务，保留已建建筑/法律；独立且友好要继续合作必须另有有效协定。产业JE本身不能因为宗主拒付就永久锁死，应转本国军备目标。

## 6. 国内统一与九州归还：最小闭包，不动崩溃

当前M `common/scripted_triggers/nesnd_japan.txt:87–98` 的 `nesnd_japan_is_united` 要求Kanto、Kyoto、Kansai、Chugoku、**Kyushu**、Shikoku、Tokai、Tohoku、Hokushinetsu九整州及独立。M values `nesnd_japan_unity_score:7–18` 同样计九州；M JE `nesnd_japan.txt:49–73` goal=9，完成置 `nesnd_japan_unified`、120个月 `nesnd_japan_integrated` 并发事件5。

建议保留旧 `nesnd_japan_is_united` 为“完整九州版”兼容谓词，新增明确的core触发与core计分供现有reunification使用：排除Kyushu，八州，独立。完整版可写成 `core=yes owns_entire_state_region=STATE_KYUSHU`。新增九州后继JE只对core已成立且不拥有完整Kyushu者开启；complete核九州实际归属，绝不再次发统一整合奖励。

这只是“九州不挡国内统一”的最小规格。**仍保留Shikoku要求**：目前方案明确点名九州，不能擅自将吴占四国也一并从核心目标删除。若作者之后明确四国同样只属外部收复目标，再单独修改；本次保留已有领土意图。

需联动查的本项目闭包：

- `common/journal_entries/nesnd_japan.txt:49`：core complete与goal；已有JE存档不能只加 `NOT entered` 的新入口而丢旧条目。
- `common/scripted_triggers/nesnd_japan.txt:87`、`common/script_values/nesnd_japan.txt:7`：区分core/all，不要一处改八州另一处仍goal9。
- `events/nesnd_japan_events.txt:99–106` 与两语事件5：统一通知不得仍声称收复全部九州。
- `common/dynamic_country_names/nesnd_japan.txt:1–2`、`ce_dynamic_country_names.txt:525–526` 消费 `nesnd_japan_unified`。把该标记定义为国内统一即可让JTK/JIM无九州时得到统一名称；不要改TAG删掉独立国家。
- `common/scripted_effects/nesnd_japan.txt:95–96,166–167`、`nesnd_japan_recovery.txt:61–62` 已对新分国清旧unity标记。新增core/kyushu阶段变量同样需要新国初始化策略，但不能因此重置已完成国家发展奖励。
- `common/static_modifiers/nesnd_japan.txt:1` 仍是5%行政、−10%动乱影响；八州统一若沿用奖励，只结算一次，不另发三份全国修正。

保护边界：`nesnd_war_collapse`、两中心敌占、原生战争退让/吞并注册、`nesnd_japan_recovery`和原分封领土转移均不属于core/Kyushu拆分的必要改动。当前崩溃trigger只依其自身partitioned/collapse/败战事实，不消费 `nesnd_japan_is_united`。M `nesnd_war_collapse.txt` 两份效果/条件及 `nesnd_japan_recovery.txt` on_actions保持原序；不把新独立战争送入旧日本首次崩溃案件。

## 7. 外部核验与尚需定向引擎观察

可以直接纳入外部检查：原版接口/数据库存在；三TAG所有入口；country/state/pop scope闭包；country值分母正数；请求对象存活/仍属同一直接宗主；按钮visible/possible/effect各自guard；30/70只有唯一monthly调用；固定文化目标；不含宗教转换；八州/九州计分一致；不碰旧崩溃；每种奖励一次；source SHA。

仍未被本报告证明为实机行为：文化split/merge的整数舍入与前后宗教总量；本JE自动进入具体刷新时刻；原生战争/同意独立后当天状态变化；同市场资助实际财政入账和按国产量门槛；革命/再次释放/再统一的具体存档继承；create_treaty是否自动重验所有article资格（因此实现须自行guard，不依赖猜测）。不应凭静态通过或本报告宣称游戏内验收。

## 源文件指纹

|来源|相对路径|SHA-256|
|---|---|---|
|G|`common/journal_entries/journal_entries.md`|`1032c0dac08d502d49380e05929912fa94ba3a3a6f2a6279b480d58ea7272323`|
|G|`common/journal_entries/00_meiji_restoration.txt`|`aaaf94eb3c4acd16e2985381ef68f6cd1cf1ca8fa012002ad2305c24faa135d0`|
|G|`events/meiji_restoration.txt`|`5e010ebc08631a2c18921792a768d9510cb3b117be961fb0f762597c537144b0`|
|G|`common/journal_entries/00_player_objectives_economic_dominance.txt`|`7fb15aab732c9ce9f93c4f3a86265de98aaef64b1d9fdb4a4dd8174ec8e12599`|
|G|`common/script_values/building_values.txt`|`43d63633c893313e574afb93c399d95d2c1bd0b88cebc765f6ef4b165787296f`|
|G|`common/script_values/event_values.txt`|`2bde5cecb435cf0e41ed83987e7acd72adb41578ebc39df5970f176a39469581`|
|G|`common/script_values/ep2_japan_values.txt`|`fbe8069966e67a2b73a9bb7672a219092b19cea0aba3c857813deade510cca9e`|
|G|`common/script_values/ip4_cuba_values.txt`|`b562c8d98cb139c22a026f3e378e711057792fe11e9ffec89588f89067380e86`|
|G|`common/script_values/ai_script_values.txt`|`ee7f0fb9826ad5c32d91bfcca85b121b30a70acc1d1d9fc4760cccfb58d9aa99`|
|G|`common/journal_entries/00_standard_of_living.txt`|`76f931b1df74300c9cc9703eae609caaf4f90ac30bcc81ab0d997578536c530b`|
|G|`common/journal_entries/00_east_indies.txt`|`2398d417afc4de586401479b7bbd95c4129e9a1ef66e0d290561b5595362ccd2`|
|G|`common/journal_entries/00_hawaii.txt`|`43eb4de1c8d507f679d35f6228fa09cbae258e926414f6deb91c71092e82ddbd`|
|G|`common/buildings/01_industry.txt`|`7e41e84ab11ab85715badbea648f1ce938f989b00761f47882c65de986fcf25c`|
|G|`common/production_method_groups/01_industry.txt`|`070243064f5a07d84e25ce773686b0e5a9e2e7d0b942798d74caf88ea8f5b681`|
|G|`common/production_methods/01_industry.txt`|`d0abb71f6ba922f46e1e512810053d1206a3cbfd8a2ff419d8a66c87b8a36886`|
|G|`events/brazil/culture_south_america.txt`|`b4a1cb8f0ba08b507d3320f2575fa2b639ec63e1505755edd46d5bafdcf9a68b`|
|G|`common/diplomatic_actions/38_subjects_increase_autonomy.txt`|`c7e43033ad2684f579ea72f80f180bd08553d4064942fe892e11ec2842172d56`|
|G|`common/subject_types/00_subject_types.txt`|`97a488157dfb2f340cca06aba30bfef42a36ea0a48dce6e591c8891628a6b91d`|
|G|`common/diplomatic_plays/00_diplomatic_plays.txt`|`4f4c61ad1198cc1b862e6399fb08cff7813be815d8c3644b08e3d43a708c00a9`|
|G|`common/war_goal_types/10_independence.txt`|`4ef3498504a15eae8264f2839ef980202104c633e6c30a3e6e7d92d7c4d15eae`|
|G|`common/war_goal_types/09_increase_autonomy.txt`|`2d378c613cedf1da9a84d4299209e129b1e754328f701842f4730e46dbaf75f1`|
|G|`events/british_raj_events.txt`|`9e3918a3a19bc34401d5af419b8a25fbf15ffa61c6169efddfd310a6fcb7db7c`|
|G|`common/scripted_triggers/00_scripted_triggers.txt`|`66432c31661d560146707744da29475cae92bbb6cbe432a1f0409133c92a3178`|
|G|`common/treaty_articles/13_goods_transfer.txt`|`50d4e8ae301c522a278598c9f315430417fc34a3a8bbf536b0d3a5cf371b607d`|
|G|`common/treaty_articles/05_transfer_money.txt`|`6f59db04c429ab06eb6844cfadc87c3a54525e9e447586f19d0e40c780198112`|
|G|`events/japan_events/ep2_meiji_restoration.txt`|`358d0b9d3b8b356f102e14caf469f873087f2ee657768a5ef6aa64f4101084bb`|
|G|`common/history/trade/00_historical_trade.txt`|`224e158cc34043a7ab342677013ab49a48c7062f5e73627c59f400c84efc2a8c`|
|M|`common/on_actions/ce_code_on_actions.txt`|`df60c03cc9eece388a7eb8e030eca2b14f8890e8a522f18aa28c57086b2b709b`|
|M|`common/on_actions/nesnd_japan_lin_regency.txt`|`2f86d12c2fb20f169e929d5374b23ed9c915121bb7c52559cc0747b86b3186b0`|
|M|`common/scripted_effects/nesnd_japan.txt`|`a37223a6f87ab9bf5eac53b525a1a4e9f0227e53517cdb0831702fefaa0f4f1e`|
|M|`common/scripted_effects/nesnd_japan_recovery.txt`|`b1ff7114bd4866a0fd031568fe2148b9b9a1275539969e2888b43678ee1889f4`|
|M|`common/scripted_effects/ce_scripted_effects.txt`|`7d83ee6d0da5016c70b2a14d56480ce33f660b2f6aa910f175318ae6585c3dbc`|
|M|`common/scripted_effects/nesnd_qe1_identity.txt`|`33bd8f871ce7163aa3d1539a8a56a125cee153ab0408d0c6e81748aef2894e49`|
|M|`common/script_values/nesnd_qe1_identity.txt`|`b50916f67ba3102baa2079329ac39c3e111d756db516ccc4296673c806c4f779`|
|M|`common/scripted_triggers/nesnd_japan.txt`|`be2b59c7b6ac07ba26208277f73597f205096d0dd0ed07458c9d8e40d9372c38`|
|M|`common/script_values/nesnd_japan.txt`|`c2bf36d4d754fb259a8911d692461215f3b2d40c2c743268a162ca573c4f7f36`|
|M|`common/journal_entries/nesnd_japan.txt`|`424dece3a340197f5899728dd4f9513a6c54e62fdd5e403d70efe2f4c4066725`|
|M|`events/nesnd_japan_events.txt`|`913ee9ed28d80e8c2c125bb757ebca02d4def35ff040ac4e52ad4150802e0a16`|
|M|`common/dynamic_country_names/nesnd_japan.txt`|`0ebb42d5ce0083d209edbca17548da82b874e187f4232f9814171fd0d342f362`|
|M|`common/dynamic_country_names/ce_dynamic_country_names.txt`|`33bb1a5caccf0df985052b5c37c8d93bad9bb2c4eb19c95f93934bfe870a86fd`|
|M|`common/static_modifiers/nesnd_japan.txt`|`759bdced1718b5ef457ebc6b591deb727fb850d50041fa60d00b3af2ee94a177`|
|M|`common/scripted_triggers/nesnd_war_collapse.txt`|`6ae291edab567b237df552bad91d541e88463850e0f0190585ed65f04878a014`|
|M|`common/scripted_effects/nesnd_war_collapse.txt`|`677f731881187b195f1c22a302059ff0fe4a91aa6c874a45af981b7f4bb1d1da`|
|M|`common/on_actions/nesnd_japan_recovery.txt`|`583397fed8ef78711c67cc0f082054095fbe1583f82383a4d4db9c90092cbc13`|
|M|`common/country_definitions/nesnd_japan.txt`|`6d80091d1ee6fd742713041771c964f7bbf3f9ba0b0a3006dbe53bf4561592d9`|
|E|`effects.log`|`24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`|
|E|`triggers.log`|`ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`|
|E|`event_targets.log`|`cc12b15da310d0d8ef10a9209107b4d2298a882fa6ee038c202650e3c9bd7c71`|
|E|`on_actions.log`|`3740d7aaad67474b61d55798d6b6c177a1b6dee027948db097f47d1d7f2f0fb9`|
|E|`provenance.json`|`ac4f01577b82c5f7eb7e91f0b301c9f551ea3382252bf3f1cafe81cf208ffab3`|
