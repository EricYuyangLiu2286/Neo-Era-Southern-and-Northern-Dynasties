# 两宣慰司最小执行契约：当前原版链条

2026-11-03；Victoria 3 **1.13.11 / build 24799966**。只读研究，未改玩法、未开游戏。结论限当前源码／本机引擎文档；静态证据不等于引擎通过。原始摘录与SHA见 [commission-native-evidence.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-development-20261103/commission-native-evidence.json>)，下列N/D/M编号在该文件均有绝对路径、行号、原文。

## 建议采用的最小组合

**固定TAG：TZ1＝天竺、YU1＝远山；从USM实际拥有的owner-state创建；傀儡＋殖民国家类型＋总统共和＋专制，匹配现有宣慰司政府；天竺单独设印度种姓hierarchy。** 这是沿用本MOD现有官制的最小实现选择，不是声称作者已给两司全部法律定案。2026-11-03本轮查询时，GAME和主MOD的活动country_definitions、dynamic_country_names、flag_definitions均没有TZ1/YU1。旧HOI4中TZ1不构成V3冲突。父任务若已新建这些TAG，后续按自己的同一实现使用，不再次定义。

正确接口是：

- 初始宗属由**宗主scope** `create_diplomatic_pact = { country = c:TZ1 type = puppet }` 创建。
- 已有属国改等级在**属国scope**用 `change_subject_type = subject_type_dominion`。**没有查到当前 `set_subject_type` 接口。**
- `create_country.state` 是 **state / owner-state**，例如 `s:STATE_MADRAS.region_state:USM`；不是整个 `s:STATE_MADRAS` region。
- `set_state_owner` 在**state scope**转交当前片段；`set_capital`在**country scope**接受 **state_region**，例如 `s:STATE_MADRAS`。
- `set_social_hierarchy`和`activate_law`均是**country scope**；只在TZ1调用，不改USM全国制度。

来源：D01 effects.log L677–680、878–907、36799–36803、37134–37159；原版具体运行实例N03 `events/zanzibar_events.txt` L32–35、71–94，N04 `events/india_events/princely_state_creation.txt` L76–96。

## 完整原版参照链及差异

| 层 | 当前原版来源 | 本次适用差异 |
| --- | --- | --- |
| JE入口 | N01 `common/journal_entries/00_establish_colonial_administration.txt` L17–25、57–67：独立、非未承认国家、有撒哈拉以南领地、civilizing_mission；挂四地区创建／扩建按钮。 | 专用于非洲后期殖民；印度旧殖民地不应机械套civilizing_mission。两司采用本MOD专属JE/决议。 |
| 按钮门槛 | N02 `common/scripted_buttons/00_colonial_administration_buttons.txt` L259–296：南非地区至少两个本国为最大owner-state的地区，非战争、非已承诺参战博弈，90天按钮冷却。 | “两个最大份额州”和和平条件可直接用作设计基线；90天不是引擎要求。 |
| 创建与赋地 | N02 L302–382：保存宗主、文化、首府；标本国目标state；`create_dynamic_country`，`country_type=colonial`，`cede_state_trigger`转交标记州；之后创建colony pact。 | 原版动态TAG适合任意殖民者。此任务需要固定TZ1/YU1和固定地图锚点，推荐N03固定TAG＋明确owner-state路线，省去全世界标记扫描。 |
| 固定TAG片段 | N03 L32–35：ZAN从`STATE_ZANZIBAR.region_state:OMA`创建；L71–94把其余OMA片段逐个转给ZAN；不动第三国片段。 | 可一一替换为USM固定片段；效果执行时重新exists检查。 |
| 建国后政治 | N04 L76–96：新KAL的on_created内设country_type、君主/专制，然后BIC创建puppet。N20 `events/british_raj_events.txt` L59在运行时设colonial。 | 原版验证`set_country_type`虽文档短注“for history”，确实也用于事件；不需要虚构setter。 |
| 国家数据库 | N06 `common/country_definitions/00_countries.txt` L1977–1987 PHI是colonial；L2529–2539 BIC同时有british主文化和印度种姓hierarchy。 | 行政主文化可以不同于当地种姓适用群体，不能为了种姓改USM主文化。 |
| 宗属数据库 | N05 `common/diplomatic_actions/20_subject_puppet.txt` L11–25：pact携带`subject_type_puppet`，收30%收入和10影响力维护。 | 原版pact会带真实成本；不能在文案称无贡自治。另加财政补助属于新合同，不是设司自动需要的条约。 |
| 政府显示 | M01 `common/government_types/00_ce_government_types.txt` L70–98：总统共和、puppet或dominion、USM直接属国、colonial、汉主文化、无投票权。 | **原版colony＋law_colonial_administration组合不匹配这个现有宣慰司政府。** 要用原版组合须另建精确限TZ1/YU1的政府类型；不扩大旧PHI/DEI条件。 |
| 资源 | N14旗帜数据库说明及PHI实例；N15固色pattern实例。实际GAME `gfx/coat_of_arms/patterns/pattern_solid.tga`存在；MOD `gfx/coat_of_arms/colored_emblems/ce_ming.dds`存在。 | 无需拷贝外部MOD资产、无需新位图才能做到可加载。 |

N02动态国家原文有 `cede_state_trigger`，D01 L934明确它遍历**世界所有state**；若以后改用该接口，必须在该trigger里同时限定owner和任务范围，不能只依赖通用`state_to_cede`标记。固定TAG最小路径不需要这个全局扫描。

## 数据库、名字与旗帜最小形状

以下为有来源的本轮建议形状。颜色、主文化、宗教及阶位是本MOD设计选择；`ce_wuu/min`行政主文化不创建或转换当地人口。

```text
# common/country_definitions/nesnd_commissions.txt
TZ1 = {
    color = { 118 93 154 }
    country_type = colonial
    tier = principality
    cultures = { ce_wuu min }
    religion = confucian
    capital = STATE_MADRAS
    social_hierarchy = british_indian_caste_system
}
YU1 = {
    color = { 135 104 69 }
    country_type = colonial
    tier = principality
    cultures = { ce_wuu min }
    religion = confucian
    capital = STATE_ZULULAND
}
```

字段参考N06；`religion`字段亦见同源MUG L1287。无土地history块即不在1836开局凭空有地。创建时显式补country_type和hierarchy，避免把`origin`未说明的继承行为当保证。

普通localization至少有TZ1、TZ1_ADJ、YU1、YU1_ADJ；可用基础名“天竺／远山”，仅USM属国显示宣慰司。两种语言同键、UTF-8 BOM。动态名字**按原版actor上下文**，不是无根据地把database root当country：N13 `00_dynamic_country_names.txt` L1066–1080。

```text
TZ1 = {
    dynamic_country_name = {
        name = nesnd_tianzhu_commission_name
        adjective = nesnd_tianzhu_commission_adj
        is_main_tag_only = yes
        priority = 25
        trigger = {
            trigger_if = {
                limit = { exists = scope:actor exists = c:USM }
                scope:actor = { is_subject_of = c:USM }
            }
            trigger_else = { always = no }
        }
    }
}
```

YU1同形。英文Tianzhu Pacification Commission／Yuanshan Pacification Commission，宣慰使沿用Pacification Commissioner。独立后回基础名，不因旧变量永久显示USM官署。

旗帜最小可用形状（本轮设计配色；N14 L1–16、8254–8262；N15 L3–15）：

```text
# common/coat_of_arms/coat_of_arms/nesnd_commissions.txt
TZ1 = { pattern = "pattern_solid.tga" color1 = "purple" color2 = "yellow" }
YU1 = { pattern = "pattern_solid.tga" color1 = "orange" color2 = "yellow" }
# common/flag_definitions/nesnd_commissions.txt
TZ1 = { flag_definition = { coa = TZ1 subject_canton = TZ1 allow_overlord_canton = yes priority = 1 } }
YU1 = { flag_definition = { coa = YU1 subject_canton = YU1 allow_overlord_canton = yes priority = 1 } }
```

原版说明默认`coa_with_overlord_canton=coa`，可使用现有USM旗角。更有辨识度的作者图样可以另加，但不要用不存在的texture。所示`orange`／`purple`已核为GAME `common/named_colors/00_coa_colors.txt` L10、12的真实颜色键（N21）；`red`／`azure`亦在L9、20。

## 创建、转交与政治初始化顺序

执行阶段依次：同一资格集合重验→创建首府片段→确认新TAG实际存在→转交其余**USM实际片段**→设首府/政治→建立从属→设置完成标记。任何用户费用只在实际创建成功后结算。不可先记completed再创建；不可把消失／独立的新司重新当作空TAG免费再生。

下面仅演示一州创建与另一州条件转交；其余六州展开成同形分支，并在effect外及effect内复用相同资格。

```text
if = {
    limit = {
        NOT = { exists = c:TZ1 }
        exists = s:STATE_MADRAS.region_state:USM
    }
    create_country = {
        tag = TZ1
        origin = c:USM
        state = s:STATE_MADRAS.region_state:USM
        on_created = {
            set_country_type = colonial
            set_social_hierarchy = british_indian_caste_system
        }
    }
    if = {
        limit = { exists = c:TZ1 }
        if = {
            limit = { exists = s:STATE_MYSORE.region_state:USM }
            s:STATE_MYSORE.region_state:USM = { set_state_owner = c:TZ1 }
        }
        c:TZ1 = {
            copy_laws = c:USM
            activate_law = law_type:law_presidential_republic
            activate_law = law_type:law_autocracy
            set_social_hierarchy = british_indian_caste_system
            activate_law = law_type:law_hindu_caste_not_enforced
            set_capital = STATE_MADRAS
        }
        c:USM = {
            create_diplomatic_pact = { country = c:TZ1 type = puppet }
        }
    }
}
```

**依据和设计取舍：**

- `copy_laws`确实存在，D01 L802–807；会终止目标国家正在进行的立法。这里只用于刚建立的新司；绝不每月重跑或覆盖已有属国改革。
- 总统共和要求democracy科技（N11 L334–343）。若选择匹配旧宣慰司政府，建立条件应要求USM拥有democracy，科技保证按下节处理；法激活不会替按钮自动完成“所有普通立法条件都已满足”的论证。
- autocracy可与总统共和配套，N12 L12–14只禁止议会共和；其on_activate清政党/投票强度。新司专制属于中央委派体制选择，不改变USM自己财富投票。
- 上例`not_enforced`是最小、不额外追溯强化种姓的建议；若本轮明确要殖民法典化，用`law_hindu_caste_codified`（N10 L53）替代，说明这是新制度选择。不要默认先用enforced然后声称原稿已指定。
- 需要保留既有“直属省”全部法律时，也可不copy_laws而显式设每组，但不要误以为origin的笼统描述证明所有法律一定复制。
- 对YU1同形：首府STATE_ZULULAND；**不设印度种姓**，显式`set_social_hierarchy=default_social_hierarchy`可防从origin意外继承其他体系。
- 若想用更贴近原版的`type=colony`＋`law_colonial_administration`，这是可行第二方案，须另建两TAG专用政府类型。不要同时保留总统共和和殖民行政法，它们同属治理原则组，后者会覆盖前者。N11 L290–291、334–335。

宗属不是必须用`create_treaty`建立。原版N02/N04在当前版本明确使用pact初建；新税负、补贴、军事义务或条约条款另核原生 treaty_articles。不要把“binding_period一年”误当条约自动消失期，也不要把最小建司写成隐含资金援助。

## 种姓只作用天竺的边界

N07 `set_hierarchy_events.txt` L28–29提供：

```text
set_social_hierarchy = british_indian_caste_system
activate_law = law_type:law_hindu_caste_not_enforced
```

N08层级的`pop_criteria`限定 **Hindu＋南亚heritage group**；不影响全部穆斯林、移民吴人或非南亚族群。N09 `lawgroup_caste_hegemony` L38–43通过`linked_social_hierarchy`连接法律。把上述效果放`c:TZ1`便为属国自己的国家制度；不需要修改`USM`、所有印度国家或全局hierarchy数据库。不要照抄N07自动事件的英国、50%宗教及owner遍历条件，那是另一条自动设置路径，非setter必须条件。

## 科技、军队及舰船：明确证据边界

D01 `create_country.origin` L882只说继承“certain values”；**没有逐项保证科技、法律、部队与舰船继承**。N02原版殖民创建没有额外造军队，N03桑给巴尔也不靠免费军队宏完成。最小实现应保留`origin=c:USM`，禁止全科技tier、整套兵营、完整免费舰队补偿。

如果必须在不依赖未明继承语义的情况下确保某项已掌握科技，原版N17 `00_chris_scripted_effects.txt` L353–373使用“宗主有TECH、接收者没有→`add_technology_researched`”。例如新司匹配总统共和所需：

```text
# newly created TZ1 country scope, after USM existence is established
if = {
    limit = {
        c:USM = { has_technology_researched = democracy }
        NOT = { has_technology_researched = democracy }
    }
    add_technology_researched = democracy
}
```

仅对已证实需要的法律/生产方式/军种前置作同形确保；或若本轮明确决定完整复制宗主技术，用当前有效技术数据库生成逐项conditional脚本，**只给USM已经有且新司没有的科技**。不发明`copy_technology`／`inherit_technology`，不把全tier当“继承”。对既有TZ1/YU1不得再次免费补新技术，除非另有已授权的长期援助契约。

土地、人口和建筑随真实owner-state转交；不使用`create_pop`、补贴人口或重造同等级建筑。至于原驻军是否随州转交，保留为实际引擎待验事实，不能仅凭州所有权变化宣称全部部队已归新司。最小建司不调用`create_military_formation`/`create_ship`；让真实宗属提供宗主保护，后续招募按当地劳动力与财政进行。

**`transfer_to_formation`只转移角色，不是转移combat_unit**（D01 L37330–37334）。舰船转交确有`set_ship_owner`／`set_ship_owner_multiple`（D01 L37122–37132），多舰转移后需要`clear_ownership_transfer_fleet`；若要划拨锡兰驻舰，必须先明确并核查真实选定船只／港口，不能按旧历史“30舰”在当前存档凭空新建。没有舰船划拨授权时保留宗主舰队。成立后可外部检查新司军力与军需；没有实测不声称继承已验收。

## 最小领土、建设及和平条件建议

以下门槛是`gameplay_proposal`，不是引擎硬编码。

- **两司共用和平保护**：USM `is_at_war=no`、`is_diplomatic_play_committed_participant=no`，执行时重验。原版N02 L284–286明确说此限制防止分国使战争目标失效。建国期间不转战争州。
- **天竺**：必须有马德拉斯USM片段作为明确首府；八个已确认印度候选中至少两州满足`is_largest_state_in_region=yes`。有实际港口和政府行政建筑后允许建司。若要允许失去马德拉斯后仍建司，另定义有序首府备选，不在运行时随机挑不存在的州。
- **远山**：必须有`STATE_ZULULAND.region_state:USM`，建议该片段为当地最大份额；南非允许划拨清单中至少两州为本国最大份额（与原生南非按钮相同数量基线）。首府片段须沿海、有港口和行政建筑。可选择只转祖鲁兰＋USM已有相邻州；不得把1936KL1十三州当自动领地。
- **建设最小检查**：在首府**owner-state scope**用`is_coastal=yes`、`has_building=building_port`、`has_building=building_government_administration`。D02 L10122–10126、11376–11381；真实建筑键N18 L2、N19 L3。`has_building`只是有该建筑，不证明满员、高效或有盈余；这是轻量的建设门槛，不是经济验收。无需凭空加统一50万/100万人阈值。
- 如果认为两州门槛过严，至少保留“明确首府＋最大份额＋港口＋行政建筑”，把一州可成立列为本轮改动；不能把“原版两州”写成硬接口限制。

精确远山锚点：N16 `map_data/state_regions/04_subsaharan_africa.txt` L1183–1200，STATE_ZULULAND id257，city=`x41C070`，port=`x279045`，naval_exit_id3106。当前MOD州历史L5957–5973的所有者是ZUL/BST，无USM。`region_state:USM`必须先exists检查；港口省不在USM片段时，不能因为整个region有港口就宣称USM有出海口。用state的沿海／建筑条件解决，不直接从region读取资源。

## 上线前最小闭包

1. 两TAG定义／动态国名／中英文／旗帜键全部有效，未重复定义。两个JE/决议在明吴两阶段显示与执行一致。
2. effects存在性重验；首府和候选是同一集合；只转USM片段；MUG、TRA和其他土邦、南非第三国不被误转。
3. 成立后各自真实宗属、country_type、法律、hierarchy、capital与政府显示匹配；USM原法律／hierarchy不变。
4. 原八印度州的当地起义／资助案件与owner predicates必须接纳新TZ1或按真实转属收尾，不因行政重组自动抹去MUG议程；远山不混印度集合。
5. 新司已存在、独立、被灭、失去首府或USM灭亡分别收尾；一次奖励／初始化标记防重复。技术、军队实测边界单列。

本报告完成了当前原版链条与数据库/资源取证；尚无新司的引擎运行证据。父任务可据此实施及执行必要外部检查，无需为已授权的常规实现选择追加审批。

## 实施核对纠正

原版events/meiji_restoration.txt:82与agitators_events/algeria_events.txt:939使用裸state-region数据库键：set_capital = STATE_KANTO / STATE_ALGIERS。本报告早期适配片段误加s:，已改；state创建仍是owner-state scope。奥兰治自由邦当前数据库键为STATE_VRYSTAAT，不是STATE_ORANJE。候选已修并通过Tiger检查。
