# 印度逐州起义：执行接口合同

2026-11-03；GAME 1.13.11 / build24799966。只读当前GAME、引擎文档与主MOD；未改玩法、未开游戏。以下原文片段为 SOURCE_PROVEN，适配片段为待外部／引擎核验的组合；不冒称组合实机通过。六地区为 CIRCARS、KURNOOL、MADRAS、MYSORE、TRAVANCORE、GUJARAT。结果属于当地政权，赞助者不自动吞并。

## 可立即使用的结论

- `create_diplomatic_play` 放在**发起国**scope，原版有同时提供 `target_country`、`target_state` 的实际例子。play定义的 `war_goal`＋`target_state` 产生发起方主诉求，不再手动重复加同一主目标。
- 新建国家的 `state` 接收实际owner-state：`s:STATE_X.region_state:USM`，不是裸state_region。
- **现存接收国与新生国家分路**：KNO/TRA/COC等已在同地区有州，先转地可能合并owner-state，回滚整个 `region_state:receiver` 会夺走其旧土地。现存国应先同意、创建有限州目标博弈，待和约执行转地；只有不存在TAG的新国使用先创建单州→立即建收复博弈→失败原州返还的路径。
- 军队没有找到“把既有兵营无副作用重绑成营队”的原生effect；`transfer_to_formation` **只支持character**。不应把 `create_military_formation` 宣称为重绑旧兵营。最低无重复实现是保留转入的实际营队，已有军队时绝不再生成；零军队且有兵营的异常状态不能靠盲目生成等量营队“修复”。
- 六个地区各用一个前缀play类型，可用类型＋双方＋案件序号准确匹配，不需要未经证实的DP `target_state`链或遍历war_goal接口。

## 1. 原版州目标创建：直接同形例子

原文：G `events/soi_events/00_ep1_kazakh_events.txt:268–279`。此处发起者KAZ、目标RUS、主目标阿克莫林斯克，另加乌拉尔斯克及俄方保护国反目标：

```text
c:KAZ ?= {
    create_diplomatic_play = {
        name = annex_war
        target_country = c:RUS
        type = dp_return_state
        target_state = s:STATE_AKMOLINSK.region_state:RUS

        add_war_goal = { holder = c:KAZ target_state = s:STATE_URALSK.region_state:RUS type = return_state }
        add_war_goal = { holder = c:RUS target_country = c:KAZ type = make_protectorate }
    }
}
```

[原文件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/soi_events/00_ep1_kazakh_events.txt:268>)。补充原文 `events/balkans_events/00_ip3_hungary_events.txt:1074–1087`：AUS scope创建play，`target_state=c:HUN.capital`，防守方 `holder=c:HUN type=independence target_country=c:AUS primary_demand=yes`；证明 `primary_demand` 的实际位置。[原文件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/balkans_events/00_ip3_hungary_events.txt:1074>)。

`escalation=80`有原版印度实例（`00_sepoy_mutiny_scripted_effects.txt:2275–2280`），引擎文档允许0–100；它只是开始时升级值，保留谈判可不写 `war=yes`。不照抄原版 `dp_sepoy_mutiny` 的吞并与禁和谈。[印度实例](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2275>)、[effect文档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:909>)。

有限play定义建议仅用当前文档支持字段：

```text
dp_nesnd_india_mysore = {
    war_goal = return_state
    requires_interest_marker = no
    allow_negotiated_peace = yes
    mirror_war_goal = no
    initiator_can_add_war_goals = no
    target_can_add_war_goals = no
    add_infamy_for_starting_initiator_wargoals = no
    texture = "gfx/interface/icons/war_goals/return_state.dds"
    selectable_in_lens = { always = no }
    possible = { }
    ai_acceptance_max = 75
    on_weekly_pulse = { }
    on_war_begins = { }
    on_war_end = { }
}
```

此为**适配模板**，有脚本入口自己的外交守卫；`possible={}`不是允许忽略停战／宗属／已有战争。字段出处：[diplomatic_plays.md:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/diplomatic_plays.md:1>)；原生 `dp_return_state`：[00_diplomatic_plays.txt:129](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:129>)。其余五区用对应独立类型，值与规则一致。

目标选择有明确互斥：`return_state.valid`要求实际 `target_state.owner=target_country` 且 `has_claim_by=root`；`conquer_state.valid`反而要求 `NOT has_claim_by=root`。使用return-state时先确保地区已有相应发起国claim；不得同时给同一holder/州重复两种目标。[return_state:31](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/21_return_state.txt:31>)、[conquer_state:31](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/03_conquer_state.txt:31>)。

新起义MYS的组合形状（不是原文逐字）：

```text
# Only after the new MYS owns this case's former USM state.
s:STATE_MYSORE = { add_claim = c:USM }
c:USM = {
    create_diplomatic_play = {
        name = nesnd_india_mysore_uprising
        type = dp_nesnd_india_mysore
        target_country = c:MYS
        target_state = s:STATE_MYSORE.region_state:MYS
        escalation = 80
        add_war_goal = {
            holder = c:MYS
            type = humiliation
            target_country = c:USM
            primary_demand = yes
        }
    }
}
```

USM主目标仅收复本案州；防守方humiliation是一个可用的有限反目标，其数据库没有国家类型／宗属前提，不能称为“独立”war_goal或自动国际承认。若采用它，要接受其原生战争支持／占领条件和外交效果，属于设计选择。原生`independence`只用于确有直接宗主的TRA等属国；刚创建独立MYS不适用。[humiliation定义](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/08_humiliation.txt:1>)、[independence.valid](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/10_independence.txt:27>)。

对已存在KNO的路线相反：KNO明确接受后，由KNO创建 `dp_nesnd_india_kurnool`，目标 `s:STATE_KURNOOL.region_state:USM`，主目标return_state，USM有限反目标；此前**不转地**。这样已有KNO州、人物、外交和主权均保留，失败也无已转地回滚问题。赞助者如要加入，另按真实同意加入backers，不因为资助自动参战。

## 2. 精确登记play，不靠“任意战争结束”

原版提供：`any_diplomatic_play`／`random_diplomatic_play`，`is_diplomatic_play_type`，`initiator`，`target`。印度原文有类型＋target过滤；NESND应再加initiator、每地区唯一案件锁。原生未找到通用DP→目标state可链访问器；`region`返回的是strategic_region，**不是state_region**。[trigger文档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:1873>)、[target/region文档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:1771>)。

```text
clear_saved_scope = nesnd_india_created_play
random_diplomatic_play = {
    limit = {
        is_diplomatic_play_type = dp_nesnd_india_mysore
        initiator = c:USM
        target = c:MYS
    }
    save_scope_as = nesnd_india_created_play
}
if = {
    limit = { exists = scope:nesnd_india_created_play }
    scope:nesnd_india_created_play = {
        set_variable = { name = nesnd_india_case_serial value = scope:nesnd_india_case_serial }
    }
    s:STATE_MYSORE = {
        set_variable = { name = nesnd_india_case_play value = scope:nesnd_india_created_play }
    }
}
```

该**组合**要求创建前已经证明没有同类型同双方旧play，而且scope数值`nesnd_india_case_serial`已保存；否则此查找不能证明是刚创建。`set_variable`允许任意event target作值，DP保存引用合法；保存后依旧每次先exists再解引用。原文保存DP的例子在 `italian_unification.txt:644–651`，变量接口在effects.log37194。[保存DP原文](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt:644>)、[变量接口](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37194>)。

更窄的入口是 `on_diplomatic_play_started`：root就是刚创建的DP，提供scope:initiator和scope:target，可在地区launching锁和序号匹配时直接登记该root，避免随机选择。原文注释：[00_code_on_actions.txt:2477](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:2477>)。

战争阶段由已登记DP的 `war`取得实际war；反向war有`diplomatic_play`。结束回调 `on_war_end` root仍是DP（scope:actor=initiator、scope:target=target），退让有 `on_diplo_play_back_down` rootDP、scope:actor参与者。对已登记ID与序号响应一次，再核实际州归属／存活国判胜败／余局；不可使用双方是否还参与其他战争判断。[DP→war](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:109>)、[war_end](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:6988>)、[back_down](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:4264>)。

## 3. 新国创建只给实际owner-state

原文 `central_america_events.txt:83–90`：

```text
create_country = {
    tag = GUA
    origin = this
    state = s:STATE_GUATEMALA.region_state:UCA
    on_created = {
        set_variable = ca_secession_country
    }
}
```

[源文件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/central_america_events.txt:83>)。其前置核owner-state存在及不是首都；相邻ALT分支还明确 `NOT exists c:ALT`。印度要另外核人口>0、全案政治接收资格、无现存TAG、USM仍拥有、无相同案件；先标来源state及case，再从存活USM执行创建。`on_created`是新国scope，设置当地文化／宗教／制度应只在此分支；不能把USM的中华身份当当地政权身份。`origin`文档仅承诺继承certain values，不保证继承全部科技、军队或人物。[create_country接口](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:878>)。

不存在TAG的新国只接受一个本案州时，没有其原有同region土地需要保留；先创建MYS／CAR或已确定新本地TAG，再由新国保存引用并确认实际拥有州，最后建DP。不能将sponsor设为收地者，也不能用 `annex` 结算地方独立。

## 4. 营队：已证接口与不能承诺的部分

原生`create_military_formation`是**新建**：

```text
create_military_formation = {
    type = army
    hq_region = sr:region_south_india
    combat_unit = {
        type = unit_type:combat_unit_type_irregular_infantry
        state_region = s:STATE_MYSORE
        count = 1
    }
}
```

上例1营是接口示意，不是建议免费赠兵数。文档支持country scope、可重复combat_unit；原版太平天国与Ezo实际用它创建固定军队，但这不证明能消费／复用既有兵营等级。[effects.log:959](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:959>)、[太平军原文](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_scripted_effects.txt:1>)、[Ezo原文](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:2726>)。

当前源码与引擎docs检索结果：

- 有 `army_size`＝本国营队数；可在完成转地后检测当前实际军队。不是人口／军工等级。[army_size文档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/event_targets.log:888>)
- 真正建筑ID为 `building_barrack`（单数），不是`building_barracks`；某些script_docs示例用后者，必须以数据库为准。可核 `has_building=building_barrack`、`b:building_barrack.level`、building scope的`any_combat_unit`，但观察值不等于创建／重绑接口。[building_barrack定义](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/buildings/05_military.txt:3>)、[原版读取等级](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:10>)
- `transfer_to_formation` supported scope=character；`every_combat_unit` supported target=new_combat_unit，但该scope本轮找到的专属effect只有`add_morale`。没有发现transfer-battalion、set-unit-formation、attach-existing-barracks之类接口，不能发明。[transfer_to_formation文档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37330>)、[every_combat_unit文档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:1306>)

**最小安全实施**：全案转地结束后只记一次 `military_inspected`，保留现有营队；实际army_size>0时不创建。既存KNO/TRA直接使用它们本国原军队。新国若零营队，不自动复制USM整编，不额外创建舰队，也不将“存在兵营”认作已有部队；可继续使用已明确同意支援的盟军或按设计暂停／取消本案。若产品必须保证新国自身至少一营，应把它写成有来源、有费用、有当地人口上限、一次性**新募兵**，并核生成后兵营是否增级；这不是“从既有兵营无重复复用”的已证能力。本报告不提供虚假的保证。

若为了消除可能的延迟初始化而次日再观察，读取必须按同case且仍持有州；不能隔日无条件刷新奖励，军队观察完成与成功发难要分开。该延迟是否必要属引擎待证。

## 5. 失败回滚：只限新建单州分支

`set_state_owner`的文档scope=state、target=country；原版Kurnool将实际BIC owner-state转给KNO：

```text
if = {
    limit = { exists = s:STATE_KURNOOL.region_state:BIC }
    s:STATE_KURNOOL.region_state:BIC = { set_state_owner = c:KNO }
}
```

[原版实例](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2258>)、[接口](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37144>)。

原始state对象在转地／同region合并后能否保持scope身份不由此接口保证；因此建议新建分支当次执行内失败立即核：USM仍活、此TAG确由本case创建、接收国仍只有本case州、没有额外土地、state的case标记和序号匹配、未检测到本案DP／war、当地owner仍是接收国。都满足才返还实际本案州：

```text
# Conditions above must have passed in separate guarded branches.
s:STATE_MYSORE.region_state:MYS = {
    set_state_owner = c:USM
}
```

之后清该case临时modifier／pending／launch锁并记失败和冷却；沉没联络费不全退。不 `annex=c:MYS`，不清其在别处的州，不使用整个state_region所有state循环。若有第三方取得／合法新领土／其他战争介入，转一次性外交余局；不倒转第三方战果。

新国失去最后一州后的自动灭亡／历史对象保留属于引擎语义，本轮未实测；不存在可认证的delete_country接口。`remove_owned_country`是company scope移除公司对目标国家的所有权，**不是杀国家**（[原生定义](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:36604>)）。所以返还后只依据实际`is_country_alive`及州数清案，不调用虚构销毁effect。新生无领土对象可保留历史定义，不复活、不发兵、不重发奖励。

**不能把这一返还片段套给既存接收国**：KNO原有KURNOOL、TRA/COC原有TRAVANCORE、古吉拉特各邦原有GUJARAT。除非拥有经验证的原province集合记录与精确反向省份转移，禁止预转合并再返还owner-state；本合同的既存国先DP后和约方案消除这一风险，不需要编写复杂回滚系统。

本轮结论：州目标创建、双向诉求、owner-state建国、实际州返还和精确DP事件入口均有当前原始来源；“既有兵营无重复转成新营队”以及末州返还的引擎生命周期没有被本轮验证，必须保留这个准确边界。
