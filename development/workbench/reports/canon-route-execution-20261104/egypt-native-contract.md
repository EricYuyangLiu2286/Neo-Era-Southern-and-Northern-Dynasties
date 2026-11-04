# 埃及独立、外资与六国条约：当前原版实现契约

2026-11-04；只读源码研究，供当前候选实施。GAME **1.13.11 / Steam build 24799966**；本轮 `catalog.py status` 返回 `CURRENT`、`changed_count=0`。未启动游戏、未改主 MOD 或本体。下列片段为 **SOURCE_VERIFIED / 静态语法样例**，不是游戏运行通过。**后续补查以第10节为准：SIH开局是USM的dominion，必须给保证独立条款做埃及定向例外；现有dominion允许主动博弈和拥有属国。不能把存活赞助国的资格问题改判为“无赞助失效”。**

路径：`G = D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`；`M = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`；`W = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`；`D = W/references/engine-docs-1.13.11-20261031`。文末记录源 SHA256。当前用户设计优先于旧计划：EGY开局独立；1825六国协议；30年独立考验；选择投资国并受外资侵蚀。

## 1. 结论与最小改动边界

1. 六份条约分别由 EGY 与 FRA、USM、SIH、GBR、QE1、TUR 签订。**投资权方向是 `source_country = c:EGY`、`target_country = 投资国`；独立保证方向相反。** 当前原版法埃条约正好提供投资权实例。
2. `entered_into_force_on = 1825.1.1` 与 `binding_period = { years = 20 }` 表达“自1825起，约束至1845”。**约束期不是自动终止日期**。若用户的“至1845”要求到期实际撤约，须用原生 `withdraw`；不能发明 `end_date` 或以约束期结束冒充解约。
3. 引擎已有 GDP 所有权比率：EGY scope 内 `gdp_ownership_ratio = { target = 外国 value > 0.1 }`。可用数值表达式 `"gdp_ownership_ratio(scope:owner_country)"`。不需退化成建筑等级比重；`country_ownership_fraction` 只是建筑政府所有权比例，不能当全部外国所有权。
4. 从预定宗主 scope 执行 `create_diplomatic_pact = { country = 埃及 type = protectorate }`。同类原版权力集团强制臣属入口与保护国数据库已查。设置终态前，必须确认 EGY 已实际成为该国保护国。
5. 主MOD现有 TUR→EGY 保护国、独立市场特许及EGY自由渴望初始化需删除；保留 EGY→HDJ 朝贡。现有法国援埃条约的独立支持和重复投资条款需调整，军事援助/商品转移可保留。
6. 原版坦志麦特和埃及危机没有“独立后无条件重新附庸EGY”的脚本。不要为此禁用整条奥斯曼改革。`je_veiled_protectorate` 是埃及被附庸后的另一奖励/换君链；如要避免它抢入新终局，最小停用对象仅该JE，保留其余坦志麦特与外交危机内容。

## 2. 1825—1845 条约完整链条

### 历史调用者与字段

- `G/common/history/treaties/00_historical_treaties.txt:1–17`：`TREATIES = { create_treaty = {...} }`，日期字段 `entered_into_force_on`，期限 `binding_period`。
- 同文件 `:217–231`：法国保证比利时独立；独立保证由FRA指向BEL。
- 同文件 `:242–289`：法埃军事任务；`:275–279` EGY向FRA授予投资权。
- `D/effects.log:1030–1083`：`create_treaty` 完整引擎形状；**无 `end_date`、无 `on_created` 字段**。`is_draft=no` 创建生效条约，日期不可在未来。
- `G/localization/english/concepts_l_english.yml:1343` 明确：约束期结束后退出不再受罚，条约没有在该日自行消失。

同形候选（其他五国替换所有FRA位置及双方字段）：

```text
TREATIES = {
    create_treaty = {
        name = nesnd_treaty_egypt_1825
        first_country = c:FRA
        second_country = c:EGY
        is_draft = no
        entered_into_force_on = 1825.1.1
        binding_period = { years = 20 }
        articles_to_create = {
            {
                article = foreign_investment_rights
                source_country = c:EGY
                target_country = c:FRA
            }
            {
                article = guarantee_independence
                source_country = c:FRA
                target_country = c:EGY
            }
        }
    }
}
```

### 数据库权限与维持条件

`G/common/treaty_articles/02_guarantee_independence.txt`：

- `:1–30` directed；`is_guarantee_independence`；source付50维护；一次每侧；与同盟、防御条约互斥；科技 `international_relations`。
- `:36–50` 新签可见/可能条件：source独立、source等级高于other、双方关系高于poor。
- `:52–72` 已有条约维持条件：source等级至少target等级，双方均非属国。
- `:74–139` 重叠利益等级与重复保证/同盟/防御约束。
- `:143–146` 退出保证产生12个月双向停战；`apply_break_penalties=no` 只免毁约惩罚，不能声称所有退出副作用都消失。

`G/common/treaty_articles/07_foreign_investment_rights.txt`：

- `:1–31` directed；`is_investment_rights`；target付25维护；科技 `stock_exchange`。
- `:33–39` 完整DLC环境有原生投资条款。
- `:79–108` 投资国对EGY首都战略区域的利益等级、重复投资条款限制。
- `:110–118` 双方须允许主动外交博弈才能维持。

这两种条款没有“仅欧洲国可以使用”的硬编码国家白名单。六国皆可按相同条款格式创建，但静态源码不能证明任意未来等级/宗属状态下保证永不冻结。国家等级不是由recognized单独保证：`G/common/country_ranks/00_country_ranks.txt:17–18,55–56,92–93,121–122,152–153,184–185` 分别为7/6/4/2/5/3。当前所有六国类型均允许原生保护国宗主，但等级必须按实际新局/届时状态核验。

### 与现有MOD重叠

`M/common/history/treaties/00_historical_treaties.txt:244–297` 现有FRA/EGY军事任务包含：军事援助、`:260` 独立支持、枪炮商品援助、`:283` 投资权、棉花转移。新增六国投资/保证约时：

- 独立EGY不再符合 `support_independence` 意图；删该旧条款。
- 移走这份旧约的 EGY→FRA 投资条款，避免同时保留两份重复投资权。
- 保留军事援助、枪械10、火炮5、棉花120等既有内容；法国新保证与投资由1825新约承载。
- `:299–343` 无投资DLC分支也保留其他内容；当前任务默认完整DLC，不必扩大为一套缺DLC降级设计。

### 真正1845到期：标记对象后退出

`D/effects.log:4804–4808` 的 `every_scope_treaty` 只遍历当前国家实际生效的条约；`:37390–37398` 的 `withdraw` 在treaty scope执行。`G/events/italian_unification.txt:685–695,707–717` 是遍历条约退出的当前实例。

**不要到1845再凭“投资+保证”广泛匹配所有条约**，这样会误退玩家以后重签的条约。应在新局首轮初始化时准确抓取六份历史条约对象，给其设唯一标记；后续只撤标记对象。既有 `M/common/on_actions/nesnd_phi_finance.txt:12–14` 和 `M/common/scripted_effects/nesnd_phi_finance.txt:306–323` 已采用treaty-root回调保存真实条约scope。

原生回调为 `on_treaty_entered_into_force`，**root是treaty**，不是EGY；`G/common/on_actions/00_code_on_actions.txt:3407–3427` 明示。历史初始化是否调用该回调的精确时序尚未实测，因此最保守方案是在 after-lobby 的一次初始化中遍历已生效历史约，按双方及两条article方向标记，并设国家“已登记”锁，之后不重扫新约。`set_variable` 本机通用scope能力见 `D/effects.log:37194–37202`。

```text
# Country scope = EGY; run only once during new-game initialization.
every_scope_treaty = {
    limit = {
        binds = c:FRA
        any_scope_article = {
            has_type = foreign_investment_rights
            source_country = c:EGY
            target_country = c:FRA
        }
        any_scope_article = {
            has_type = guarantee_independence
            source_country = c:FRA
            target_country = c:EGY
        }
    }
    set_variable = nesnd_egypt_historical_1825_treaty
}

# Country scope = EGY; after game_date >= 1845.1.1, independent of JE lifetime.
every_scope_treaty = {
    limit = { has_variable = nesnd_egypt_historical_1825_treaty }
    withdraw = { country = c:EGY apply_break_penalties = no }
}
```

1845解除不应只挂在30年JE仍活跃的分支，避免EGY早期失败后旧约永久残留。若玩家已改约，旧标记对象被取代后无需再撤新约；要不要让改约继承1845截止是设计事项，不能自动删除合法新约。

## 3. 外资比重：使用真正GDP所有权

`D/triggers.log:9899–9904`：**scoped country中的GDP有多少属于target国家**；country scope，ratio单位。原生 `G/common/on_actions/00_code_on_actions.txt:1251–1256` 在ROOT中以 `"gdp_ownership_ratio(prev)" > 0.10` 判断一个外国持有超过10%；`G/events/law_events/corporate_state_events.txt:310` 使用1%阈值。这证实参数方向和0—1量纲。

`G/common/ai_strategies/00_default_strategy.txt:7920–7928` 使用相同函数作为value。该AI权重又除以GDP，与引擎文档/成就阈值的ratio定义不符，不应照搬额外除数；函数本身有原生数值读取证据。

安全计算全外资，而非仅当前投资国或六国（所有外资都会侵蚀用户所指比重）：

```text
# Script value; called from EGY.
nesnd_egypt_foreign_gdp_ratio = {
    value = 0
    every_country = {
        limit = {
            is_country_alive = yes
            NOT = { this = prev }
        }
        prev = { add = "gdp_ownership_ratio(prev)" }
    }
    min = 0
    max = 1
}
```

这里`every_country`进入外国后，`prev={...}`返回EGY，函数参数内的prev再指该外国，采用原版成就同样的scope方向。M现有 `common/script_values/nesnd_qe1_heritages.txt:3–11` 使用`every_scope_culture → prev → add = "culture_percent_country(prev)"`同形参数读取。调用方每月缓存一次，显示和扣值共用缓存，避免各条进度明细重复遍历世界。

不能用`1 - 本国GDP所有权`替代全外国累计，除非另证自营、未所有、特殊公司等残余都归本国；目前外资逐国求和更直接。不要把外资GDP占比称为“外国控制的建筑等级”，也不要将贸易依赖/economic_dependence代入。

`D/triggers.log:9444–9449` 的 `country_ownership_fraction` 仅为建筑级“政府持有的等级比例”；`:13911–13916` 的 `private_ownership_fraction` 是私人所有比例，均无指定外国国家参数。它们不是本任务需要的所有者国别统计。

数值契约：基础赞助月耗−1，外资附加月耗系数应由父实施明确（用户未给斜率）。外资ratio=0/0.5/1的附加值、无赞助时是否仍受外资侵蚀、100上限及0下限必须同源展示。这个系数是玩法决定，不能伪称原生固定成本。

## 4. 保护国方向、资格与回调

完整原生链条：

- `G/common/diplomatic_actions/31_power_bloc_force_become_subject.txt:22–27` 检查target独立、等级、非已承诺博弈参与者。
- 同文件 `:41–65` 从宗主country scope执行`create_diplomatic_pact`，unrecognized宗主用tributary、殖民地目标用dominion、通常用protectorate。这证明方向和类型分派；本任务不应悄悄把保护国变成朝贡国。
- `D/effects.log:899–907`：scope country是initiator，country字段为target；**没有on_created回调**。
- `G/common/diplomatic_actions/19_subject_protectorate.txt:7–9` potential=always no，因为外交要求创建；`:11–40` pact=subject_type_protectorate，first_country付维护。
- `G/common/subject_types/00_subject_types.txt:1–60`：保留自己的外交博弈、自己的属国；不自动参加宗主战争；宗主必须高一级；宗主类型recognized/colonial/company；宗主等级great/major/minor；目标等级minor/insignificant/unrecognized_regional/unrecognized。

`can_create_diplomatic_pact` 文档在 `D/triggers.log:8924–8928`，但当前原版没找到用于protectorate的调用，且该action的potential永为no。**没有引擎证据时，不能以“can_create ... protectorate”为唯一终局门槛并声称它必定允许。** 后续找到更准确的`can_have_as_subject`，见第10节。类型/等级是诊断信息，不能据此提前把存活赞助者判成无赞助；从存活对象执行建立后确认真实关系。SIH本身不必独立。

当前六国类型：GBR/FRA/TUR在 `G/common/country_definitions/00_countries.txt:14–19,47–52,1106–1111` 为recognized；USM/QE1在 `M/common/country_definitions/ce_countries.txt:2–8,26–32` 为recognized；**SIH由同文件 `REPLACE:SIH:120–126` 改为recognized**。不要看原版SIH的unrecognized就误报当前MOD不兼容；`.bak`不参与加载。

```text
# Country scope = EGY. Identity/alive guards precede this fragment.
if = {
    limit = { exists = var:nesnd_egypt_investor }
    if = {
        limit = { var:nesnd_egypt_investor = { is_country_alive = yes } }
        save_scope_as = nesnd_egypt_subject
        var:nesnd_egypt_investor = {
            create_diplomatic_pact = {
                country = scope:nesnd_egypt_subject
                type = protectorate
            }
        }
        if = {
            limit = {
                is_subject_of = var:nesnd_egypt_investor
                is_subject_type = subject_type_protectorate
            }
            set_variable = nesnd_egypt_protectorate_settled
        }
    }
}
```

上例故意只在真实postcondition成立后写终态。JE `on_fail` 执行后JE已经结束，因此如果需要失败转换尚未完成时自动重试，应在国家on_action保留pending转换状态；不能先把变量、赞助国、JE全部清掉，再没有入口补救。没有存活赞助者时用户要求invalid＋合法性惩罚，这与“存活但当前关系资格可能受限的赞助者”不是同一情况；后者保持有赞助者分支并尝试建立，未兑现时保留pending，不凭空把资格失败当亡国。

真实回调：`G/common/on_actions/00_code_on_actions.txt:7573–7604` 的 `on_become_subject`，注释root=country，内容是州hub动态命名及菲律宾特殊IG修正，没有埃及重新独立/杀君逻辑。若新增此回调清理投资修正，应使用独立on_action追加并先判EGY/本路线，不覆盖整个原版effect；同步事件顺序仍是引擎待验。

## 5. 独立开局与原版埃及内容审计

`M/common/history/diplomacy/00_subject_relationships.txt`：

- `:243–247` EGY→HDJ tributary，保留。
- `:249–269` TUR的MOL/WAL/SER/TRI/TUN，保留。
- **`:270–277` 删TUR→EGY protectorate和grant_own_market两块。** 独立EGY自然拥有自身市场，不需对独立国建立该特许。
- **`:599–601` EGY add_liberty_desire=45删除**；已经没有宗属关系，不再需要该原版附庸初始化。
- EGY原版国家法/政治/科技初始化 `G/common/history/countries/egy - egypt.txt:1–24` 没有创建宗属关系，不必整份覆盖。

| 原版对象 | 真实触发/作用 | 最小处理 |
|---|---|---|
| `je_sick_man_syria`，G JE/00_sick_man.txt:95–178 | TUR取得黎凡特六州后增加改革分、给埃及核心宣称、加后续JE；没有强制转移/附庸 | 保留；TUR靠战争争夺是后续国家行为 |
| `je_sick_man_egypt`，同:180–220 | TUR持埃及四州或EGY已是TUR puppet才完成；仅增加改革分 | 保留；不是开局对EGY的强制恢复脚本 |
| `egyptian_crisis_events.1`，G events/egyptian_crisis_events.txt:3–120 | 由TUR对EGY博弈触发的国际反应；进入`:22`检查EGY存在 | 保留外交战争后果；不把它当独立开局错误 |
| 调用者，G on_actions/00_code_on_actions.txt:2539–2560 | initiator=TUR,target=EGY且博弈为征服/归还州/减自治/造属国等才触发危机 | 没有开局强制重建关系 |
| `je_veiled_protectorate`，G JE/00_veiled_protectorate.txt:1–75 | 他国已持埃及核心邻接领土、EGY独立未认可；对EGY索取/敌对；EGY成为ROOT属国才完成 | 可最小停用这一条，避免旧结算混入新投资终局 |
| `veiled_protectorate.1`，G events/veiled_protectorate_events.txt:24–65 | 保存EGY/TUR君主；选项给宗主修正或杀EGY现任君主，降低对TUR关系 | 该JE被停用后不新触发；如兼容旧队列才需额外取消/触发保护，不能只改JE就承诺旧队列消失 |
| `sick_man.3`，G events/sick_man_events.txt:203–232 | TUR改革失败释放一批自己的属国，然后自身降为unrecognized | 不会让独立EGY重新附庸；未来EGY若属TUR会受正常奥斯曼崩溃影响 |

`je_veiled_protectorate` 可以用本项目已证JE `REPLACE:`机制定点覆盖而非覆盖原版整个JE文件。要完整移除该旧埃及路线，可用禁用壳 `is_shown_when_inactive/possible=always no`，并在本路线EGY存在时invalid；若仅要求保护当前30年路线，按其active标记加条件。对新局没有必要同时删全部外交AI策略、坦志麦特、历史建筑或旧事件文本。

## 6. 赞助变量、消失与主动不选

本机 `D/triggers.log:9793–9796` 的exists只检查非null对象；`:11417–11422` 的 `is_country_alive=yes` 才证明国家在地图至少有一州、可交互。正确守卫为先exists，再在内部检查alive；不要并列假定短路。原生country变量可保存事件对象，`D/effects.log:37194–37202`。

必须另存一个选择模式/意图标记，例如 `nesnd_egypt_investor_mode=0/1`，不能仅以country变量是否存在区分“主动不选”和“被吞并丢失了country变量”。

- 选择六国：实际country保存到 `nesnd_egypt_investor`，mode=1；先清全部赞助修正再加唯一当前方案。
- 选择不投资：mode=0，移除country变量和所有赞助修正；以后每月保持none。
- 月度mode=1而country引用缺失/死亡：先清旧对象与全部修正，再在六个TAG的alive国家内 `random_country` 选一次。没有候选时保持country空，不访问空var；是否继续等待复国可由mode=1安全表达。不得另加“必须独立”而漏掉SIH。
- 切换或亡国不得重新把独立度设回100、重置30年钟、续领成功奖励。
- `random_country`是原生effect，`D/effects.log:26878–26882`；每次循环前清自己的临时scope，避免沿用前次候选。

两JE共享国家持久数据时，父JE单独拥有扣值、终局、一次性奖励/惩罚；子JE只承担投资选择展示与相应清理。父JE结束标记写在清理前；子JE invalid不再重复给合法性惩罚。0点失去赞助与30年成功互斥（成功必须独立度>0且未结算），不能依赖complete/fail/invalid引擎求值先后。

30年可用360累计月份/到期变量，避免将10950日直接声称精确30历年。原版主JE `00_sick_man.txt:23` 用10950作为30年近似，但这不迫使本玩法照抄。新局1836开始，30年目标为1866；条约1845到期是独立的一条时钟。

## 7. 修正键与量纲

| 用户效果 | 当前真实键与建议量纲 | 证据 |
|---|---|---|
| 建造效率15% | `state_construction_mult = 0.15`；可由country修正传播各州 | D/modifiers.log:1655–1658；G/static_modifiers/portuguese_colonialism_modifiers.txt:127–129；原版国家高政力效果00_code_static_modifiers.txt:563–566 |
| SIH纺织15% | `building_textile_mill_throughput_add = 0.15` | D/modifiers.log:3193 |
| QE1军工15% | `building_arms_industry_throughput_add = 0.15`；若“军工”明确涵盖火炮可另含`building_artillery_foundry_throughput_add`，不能自行把全制造算军工 | D:2141,2149 |
| USM造船15% | `building_shipyard_throughput_add = 0.15` | D:3129 |
| GBR食品/鸦片15% | `building_food_industry_throughput_add = 0.15`，`building_opium_plantation_throughput_add = 0.15` | D:2329,3089 |
| FRA钢铁15% | `building_steel_mill_throughput_add = 0.15`，注意是单数mill | D:3169 |
| TUR合理产业 | 可选纸业 `building_paper_mill_throughput_add = 0.15`，服务行政教育；这是玩法选择，非PPET已定产业史 | D:3093 |
| 科研≤10% | `country_tech_research_speed_mult = 0.05` 或0.10；不叠六国 | D:1103；G/static_modifiers/00_ip2_03_modifiers.txt:223–226 |
| 教育/识字 | 推荐 `state_education_access_add = 0.05` 或0.10，文本称受教育机会＋5/10百分点；不能称瞬间识字率＋10% | D:1695–1698；G/static_modifiers/00_ip2_03_modifiers.txt:4 |
| 识字增长直接键 | `state_literacy_growth_add`，**不可把0.10当温和10%增幅**；原版国家基值仅0.0005 | D:1771–1774；G/static_modifiers/00_code_static_modifiers.txt:45 |
| 成功合法性15 | `country_legitimacy_base_add = 15` 是15点，不是0.15/15% | D:739–742 |
| 成功制造20% | `building_group_bg_manufacturing_throughput_add = 0.20` | D:2665 |
| 成功威望 | `country_prestige_add`固定点或`country_prestige_mult`比例；用户未定具体值须实施写明 | D:915,927 |
| 成功十年期限 | `add_modifier = { name = ... months = 120 }` | 期限沿原生add_modifier形状；不可每月刷新成永久奖励 |

所有赞助方案公共建造、教育、科研不要拆成可重复相加的六项常驻修正。转换/主动none/JE终局均要立即移除公共与专属修正。成功十年奖励与赞助修正按需求独立结算，不让存档/重开JE反复领取。

## 8. PPET原文再读与设定层级

本轮直接只读ZIP/XML重读原件 `D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx`，SHA256 `b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`。不是只引用旧摘要。

- slide21 p12：1517–1518奥斯曼征服埃及，马穆留克灭亡。
- slide22 p24：1699《东方条约》旨在东地中海—黑海—里海稳定与丝路贸易；有效期预定30年。不是本轮1825六国投资约的既有原文。
- slide22 p28：第四次近西战争下，奥斯曼获伊斯兰世界共同推举为领袖。
- slide26 p13–18：1918奥斯曼解体、大吴调停；1919埃及阿里王朝北伐；1920–22列强干涉；1922英国支持哈希姆进入埃及，取代阿里王朝。

这些后世段落提供独立、投资、外国干涉与王朝存续的矛盾背景，不能硬写成1836已发生或所有存档必然未来。**1825独立与六国投资保证来自本轮作者明确新设计**，高于旧MOD的TUR保护国数据；无需伪造PPET有同年条文。保留1918–22作为后世可发展素材，本次30年链没有授权自动生成哈希姆推翻王朝。

## 9. 验证边界与实施检查

已完成：当前本机版本校验；历史→条约类型→引擎接口→既有MOD重叠链；GDP查询scope/ratio；原生保护国调用与数据库；埃及JE及战争入口；PPET原件再读。文中脚本仅验证保序解析结构和来源字段，不代表实际条约生效/条款不冻结、精确rank、GDP读数、转换回调时序或UI均已通过。

父实施应至少检查：六方向条款、FRA无重复投资、全部开局宗属块仅移除EGY目标；none重复选择不改进度/期限；赞助国引用不存在/死亡两种状态；六国全死；选择后被吞并；0点恰遇满30年；转换失败不假成功；父子同帧退出不双处罚；1845准确退出标记旧约但保留新签约；成功奖励120月且不刷新；每项动态国家名在缺对象时有静态替代。引擎证据仍由用户后续游戏测试提供。

## 源指纹

| 来源 | SHA256 |
|---|---|
| [G/common/history/treaties/00_historical_treaties.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/treaties/00_historical_treaties.txt>) | `a1c7e519ef1b07e2491f473ce0f94e6abae718fe725d68bcd8644d2432602f4e` |
| [G/common/treaty_articles/02_guarantee_independence.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/02_guarantee_independence.txt>) | `00df82497474b941e75be7ce66c2306ff920d3e8393dca09b8421cab9cf9bb4f` |
| [G/common/treaty_articles/07_foreign_investment_rights.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/07_foreign_investment_rights.txt>) | `d1e4b58b2bdd5bf931e02b65ed89d4c8ef952611eef6558852af8360fdc20bf1` |
| [G/localization/english/concepts_l_english.yml](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/concepts_l_english.yml>) | `62864f4b3ec16e8e2792a6cf073f7313d645150dbf6074e8bdfb7c7f09199501` |
| [G/common/country_ranks/00_country_ranks.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_ranks/00_country_ranks.txt>) | `ac9ed2205753a32ddf052f72d47b17f0205dbd8dc275bacdc9bada60cae19dac` |
| [G/common/ai_strategies/00_default_strategy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ai_strategies/00_default_strategy.txt>) | `1121870047d92eec23feb15e9c257d56710e51aa9567a10feb513263bddab962` |
| [G/common/on_actions/00_code_on_actions.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>) | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |
| [G/events/law_events/corporate_state_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/law_events/corporate_state_events.txt>) | `b90f0d97fe9b5af6f3cdfd06cf263995d1a7134eabcb85a6b44bf66c1c8a73f1` |
| [G/events/italian_unification.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/italian_unification.txt>) | `3564046713083efe19a97fe04a3d83a6e875a627794652ce726c727c602b296e` |
| [G/common/diplomatic_actions/31_power_bloc_force_become_subject.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/31_power_bloc_force_become_subject.txt>) | `94389082fc0480145f226023a828250c912fdb1d8a9c2c37c3af6bc34e0f43ed` |
| [G/common/diplomatic_actions/19_subject_protectorate.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/19_subject_protectorate.txt>) | `f3dac10f47458557dacd850ee2f2fe10235c935cc4592d1f0b5cc47b3172cb0e` |
| [G/common/subject_types/00_subject_types.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/subject_types/00_subject_types.txt>) | `97a488157dfb2f340cca06aba30bfef42a36ea0a48dce6e591c8891628a6b91d` |
| [G/common/country_definitions/00_countries.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt>) | `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74` |
| [G/common/country_definitions/01_africa.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/01_africa.txt>) | `dd89615390fc8051e818c1eb8aa8b96964be2257019c740eaa00dd2339d152cd` |
| [G/common/journal_entries/00_sick_man.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_sick_man.txt>) | `e48405bfabb52f6ce757880e436c8d44c67111e246af3215fd3f96ec4f3477f9` |
| [G/common/journal_entries/00_veiled_protectorate.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_veiled_protectorate.txt>) | `b67fc2d52874e59373b36052c0c52af5e79ad4846519556aef67df8893d5fb17` |
| [G/common/journal_entries/journal_entries.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md>) | `1032c0dac08d502d49380e05929912fa94ba3a3a6f2a6279b480d58ea7272323` |
| [G/events/veiled_protectorate_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/veiled_protectorate_events.txt>) | `50b2110d93cb0694347a4a7f68de55e55437230844b6ea8ef99df116eb4b7383` |
| [G/events/egyptian_crisis_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/egyptian_crisis_events.txt>) | `fc3c83094b0ffbf873c9ded935f047acef4a19f5c8cd7c56c384a47e4c3a36f3` |
| [G/events/sick_man_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/sick_man_events.txt>) | `d110d1fd83cd98e131d4c2769b606cc908f17844eff88ef65f51febf313a0c2b` |
| [G/common/history/countries/egy - egypt.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/egy - egypt.txt>) | `e5a22623deea26108296bb06b08343805c76b75b166d2404bf9fc2225d1b42af` |
| [G/common/static_modifiers/00_code_static_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_code_static_modifiers.txt>) | `0f42a271058ca8932c8b87641328473f1bc6a7961b7f4bf40663d5aba43faf1d` |
| [G/common/static_modifiers/00_ip2_03_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ip2_03_modifiers.txt>) | `7ace51c19d4956f23a840b744e36ac053e4329dc888a9a692a13f63a70b801dc` |
| [G/common/static_modifiers/portuguese_colonialism_modifiers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/portuguese_colonialism_modifiers.txt>) | `b4e81f66bd674561ab5ddf71412b8ae7e39eb32e69314216c5466621fa839a0e` |
| [M/common/history/diplomacy/00_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/00_subject_relationships.txt>) | `618289bd6e7bd4e8fe5f3276249b6997f7a0c51cd2ab9f4f4f46289b9a02d59e` |
| [M/common/history/treaties/00_historical_treaties.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/treaties/00_historical_treaties.txt>) | `fbb2d10c7e3840b50c2dab4fc2510a68439bcc6fdfcec98e0c6e7ab4d0d1d352` |
| [M/common/country_definitions/ce_countries.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/ce_countries.txt>) | `7056d622fb21e0d3a72f0af4f73a9a5e23a87f769870b23c5df9043f8fbfb6f5` |
| [M/common/on_actions/nesnd_phi_finance.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_phi_finance.txt>) | `d47b15a1e5d9d35143f4dfba2e62ded99c310dbfd278e829d3b46fd40789a976` |
| [M/common/scripted_effects/nesnd_phi_finance.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_phi_finance.txt>) | `b930560066f6c62ce2cd5ba0e14ab194f5579c570e68180b152a7b628c383a80` |
| [M/common/script_values/nesnd_qe1_heritages.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_qe1_heritages.txt>) | `dea7f1a5c3d4229d5b6a353fc60eb522224a5c95637a88e2e119b44d97670cad` |
| [D/effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>) | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |
| [D/triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log>) | `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e` |
| [D/modifiers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/modifiers.log>) | `1d8ea1f6fb6bc0e2677d4591d45e21ef8f94ba4931074aa871583d61a63ceeff` |
| [D/on_actions.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/on_actions.log>) | `3740d7aaad67474b61d55798d6b6c177a1b6dee027948db097f47d1d7f2f0fb9` |

静态样例检查：4个text代码块均由本项目保序 `pdx.parse` 完整解析；解析器 `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts/pdx.py`。这只验证结构，不执行Jomini，也不提升为ENGINE_PASS。

## 10. 补查：SIH属国、埃及专用保证与保护国类型（当前执行依据）

### 10.1 当前SIH的真正身份及投资资格

补查活动历史文件全目录，而非只查`00_subject_relationships.txt`：`M/common/history/diplomacy/ce_subject_relationships.txt:2–6` 明确 **USM→SIH `dominion`**。`M/common/subject_types/ce_subject_types.txt:64–122` 覆盖该类型：`:69 can_start_own_diplomatic_plays=yes`；`:72 can_have_subjects=yes`；`:97–101`允许recognized/unrecognized/colonial作为自治领。因此当前SIH是认可国家、明的自治领，可以有自己的属国，不应当成独立国家，也不应误称朝贡国。

`D/triggers.log:33–38` 定义 `aggressive_diplomatic_plays_permitted` 为“独立或允许自行发动外交博弈”。原生投资条款`07_foreign_investment_rights.txt:110–118`只要求双方这个trigger，不要求双方独立。所以**SIH当前dominion满足这一条自治来源**；没有查到其现行法律另加禁止主动外交的字段。现有投资条款还在`:45–62`阻止属国重复签订宗主已提供的同方向投资权：本轮USM获得的是 **EGY→USM**，SIH待签的是 **EGY→SIH**，该例不等于“USM给EGY投资USM的权利”，不可把方向倒过来误判重复。

新局实际利益范围、关系和条约创建时序仍未进游戏验证。可以保留原生`foreign_investment_rights`，不需要仅为“SIH是自治领”复制投资article或更改法律/宗属。

### 10.2 专用历史保证article可以定义，但有识别闭包

`G/common/treaty_articles/treaty_articles.md:213–242`：article flags决定引擎固有行为，并非仅凭数据库key；实际原生`02_guarantee_independence.txt:14`使用 **`is_guarantee_independence`**。文档`:223`的`is_gurantee_independence`是拼写错误，以实际源码为准。新`nesnd_egypt_historical_guarantee`可以复用正确flag并修改脚本维护条件；这是本机数据驱动能力，不是发明新外交effect。

但是不能只复制flag就声称它与原生保证所有外围系统完全相同：

- `G/common/scripted_triggers/00_diplomacy_triggers.txt:99–115` 的 `has_treaty_guarantee_independence_with`硬查 `has_type=guarantee_independence`。
- `G/common/scripted_triggers/00_ai_triggers.txt:580–600` 的 `has_powerful_protectors`也按该旧key判断保护者。
- 原生alliance/defensive_pact的`mutual_exclusions`列的是旧article key；专用article至少应反向列出`alliance defensive_pact guarantee_independence`，其重复条款判定同时识别标准/专用保证。
- 新article的本地化要提供自己的key与`_desc`，不能假定自动继承原生名称。原生loc在`G/localization/english/diplomacy_l_english.yml:2119–2120`。
- 攻击方若为SIH的宗主USM，通用战争层仍可能把SIH从敌对一侧撤下；`G/common/defines/00_defines.txt:1280`明确宗主加入博弈会让其处于对面的属国转为中立。保证条款脚本不能承诺绕过这条战争关系。保证本身也只是可被召援，不是原生强制自动参战；概念`:1245`说明defender可call guarantor。

**visible不能只写EGY。** 文档`:380–387`说明visible对双方检查且只有root；写`visible={c:EGY=this}`会令六个保证国在第一层失败。专用历史条款应：visible只预筛EGY+六国；possible按root/other_country限定这七者中必须有一侧EGY；can_ratify和requirement_to_maintain以source/target严格限定六国→EGY。source/target可用性由`:408–420`证明。

专用article的实际文件合同（独立新文件，不覆写全球条款）：

| 文件 | 来源与准确改动 |
|---|---|
| `common/treaty_articles/nesnd_egypt_historical_guarantee.txt` | 复制G/02_guarantee_independence对象，改key；保留正确flag、费用50、source付款、关系增长、退出/毁约效果。visible允许EGY与六国，possible只允许EGY成对；将source独立维护条件改为白名单且alive（允许SIH自治领）；rank维护按作者六国历史保证要求豁免该专用关系。target仍限定EGY、alive、独立。保留技术、重复/互斥、利益范围等实际需保留条件；若六国历史约要免利益范围限制，明确仅此专用article豁免，不修改全局等级效果。|
| `common/scripted_triggers/nesnd_egypt_treaties.txt` | 明确六国country白名单，区分country上下文与article上下文，避免visible读不存在的source/target。|
| `common/scripted_triggers/00_diplomacy_triggers.txt` 的该helper，或已证支持的单定义覆盖 | `has_type=guarantee_independence`改为OR包含专用保证；保留原source方向、其他helper不动。|
| `common/scripted_triggers/00_ai_triggers.txt` 的 `has_powerful_protectors` | 原article OR增加专用key，其余实力/宗属过滤不变。M已经覆盖本文件时编辑有效M副本，不能从G整份覆盖M。|
| 历史条约文件 | 仅六份新约使用专用article；投资条款仍原生。到期撤约沿第2节，勿把can_ratify时间限制当已生效条约自动失效。|

这里`requirement_to_maintain`失败不是普通灰掉按钮：官方文档`:106–112`写明下次更新自动break；can_ratify还自动包含全部维护要求。创建当日不报错不足以证明SIH保证一直保留。

### 10.3 更小的外围改动：对原生保证做埃及定向例外

如果希望保留所有原生helper/AI的识别而减少扩散，可以保留article key `guarantee_independence`，仅从MOD侧同路径覆盖 `common/treaty_articles/02_guarantee_independence.txt`，在其脚本条件加入精确EGY例外。**不是全局删除source `is_subject=no`。** 当前没有核实treaty_article数据库REPLACE支持，故同路径完整副本＋保序差异审计比猜REPLACE更确定。

新增country触发器和article方向触发器形状：

```text
nesnd_egypt_1825_guarantor = {
    game_date < 1845.1.1
    is_country_alive = yes
    OR = {
        c:FRA ?= this
        c:USM ?= this
        c:SIH ?= this
        c:GBR ?= this
        c:QE1 ?= this
        c:TUR ?= this
    }
}

# Only use where native guarantee already has these two country scopes.
nesnd_egypt_1825_guarantee_direction = {
    scope:source_country = { nesnd_egypt_1825_guarantor = yes }
    scope:target_country = {
        c:EGY ?= this
        is_country_alive = yes
        is_subject = no
    }
}
```

对应原生条款必须同时调整下列位置，缺一会留下失败路径：

1. `visible:36–38` 改为`OR={is_subject=no nesnd_egypt_1825_guarantor=yes}`。这只是把SIH放进候选；不能在此读other/source/target。
2. `possible:40–50` 原生分支显式补`is_subject=no`再保留其rank/relations限制；另加“本country是上述guarantor，other_country是独立EGY”的分支。**若只拓宽visible而不在原生possible分支补回is_subject=no，SIH会被意外允许对其他低rank国家保证。** 可以保留原生双方关系>poor在两分支外，或仅在历史特例中免除；这是明确玩法选择。
3. rank维护`:52–56`：原来的rank比较与`nesnd_egypt_1825_guarantee_direction=yes`取OR。
4. source独立维护`:58–64`：原来的source非属国与该direction取OR。target独立维护`:66–72`保持。
5. `can_ratify:74–139` 原生duplicate/同盟/防御约检查不变；如历史六国必须无视当前战略利益，则只给第一项重叠利益检查加上述direction OR，不能删整个can_ratify块。
6. 1845到期后country helper为false，不再给新约或他国放宽资格；已标记六份约由第2节准确撤销。五个仍独立的原生合法保证不能仅凭例外到期自动视为已撤销。

该方案改变一个标准article定义但**实际新增许可只对六国→EGY且1845以前**，不会使SIH可以普遍保证世界各国，也不会改其对USM宗属。仅改变SIH这一个例外也可，但rank与其他五国未来被附庸时的用户“六国历史保障”承诺应保持一致。

### 10.4 SIH成为埃及宗主：现有类型已允许多层宗属

准确资格接口：`D/triggers.log:9003–9008`：

```text
can_have_as_subject = {
    who = c:EGY
    type = subject_type_protectorate
}
```

在SIH country scope查询；不是在EGY调用。`can_have_subjects`（`:9010–9014`）只查询宗主是否能有任何属国。SIH现在的dominion有该权，故“SIH是USM属国”本身不要求创建第二种保护国。当前M对protectorate的有效覆盖在`ce_subject_types.txt:124–183`：`:133`仍要求宗主高rank；`:154–168`允许recognized/colonial宗主及great/major/minor；`:170–175`限定目标rank。这比G原版少company宗主，必须按M有效定义评估。

**source里没有已证的按目标EGY或变量动态控制这些字段的接口。** 所有当前subject_type实例的`overlord_must_be_higher_rank`是bool，`valid_overlord_ranks`/`valid_subject_ranks`是列表；不能把它们改成`trigger_if`或塞入`has_variable`。给外交action加一个EGY条件只限制action入口，不会改subject_type列表本身。

### 10.5 如确需放宽rank：专用埃及保护国类型与action合同

可以复制当前M protectorate的数据为 **`subject_type_nesnd_egypt_protectorate`**，另设只被埃及终局effect调用的 **`nesnd_egypt_protectorate`** action，保留标准对象不变。数据类型显式通过`diplomatic_action`关联，action pact通过`subject_type`反向关联，原版已提供同形。`overlord_must_be_higher_rank=no`有原生personal_union实例（G/00_subject_types.txt:371）；所有非decentralized宗主rank列表也有`:406–414`原生实例。

建议完整最小数据形状如下；它是源码候选，尚未引擎证明新类型行为与标准类型所有外围脚本一致：

```text
subject_type_nesnd_egypt_protectorate = {
    allow_change_country_flag = no
    use_overlord_map_color = yes
    use_overlord_ruler = no
    annex_on_country_formation = no
    can_start_own_diplomatic_plays = yes
    breaks_if_subject_not_protected = yes
    join_overlord_wars = no
    can_have_subjects = yes
    overlord_must_be_higher_rank = no
    overlord_must_be_same_country_type = no
    use_for_release_country = no
    gives_prestige_to_overlord = yes
    can_offer_to_become_in_sway_offers = no
    diplomatic_action = nesnd_egypt_protectorate
    autonomy_level = 2
    category = same_as_puppet
    lower_autonomy_subject_type_alternatives = {
        subject_type_puppet
        subject_type_colony
    }
    same_autonomy_subject_type_alternatives = {
        subject_type_tributary
        subject_type_dominion
    }
    valid_overlord_country_types = { recognized colonial unrecognized company }
    valid_subject_country_types = { recognized unrecognized colonial company }
    valid_overlord_ranks = {
        great_power major_power minor_power insignificant_power
        unrecognized_major_power unrecognized_regional_power unrecognized_power
    }
    valid_subject_ranks = {
        great_power major_power minor_power insignificant_power
        unrecognized_major_power unrecognized_regional_power unrecognized_power
    }
    ai_value = { value = 1 }
}

nesnd_egypt_protectorate = {
    groups = { general }
    show_in_lens = no
    potential = { always = no }
    pact = {
        cost = 10
        has_junior_participant = yes
        maintenance_paid_by = first_country
        relations_progress_per_day = 1
        relations_improvement_max = 50
        max_target_involvement = 5000
        target_involvement_applies_to = source_country
        subject_type = subject_type_nesnd_egypt_protectorate
        second_modifier = {}
        actor_can_break = { is_diplomatic_play_committed_participant = no }
        target_can_break = { always = no }
        manual_break_effect = {
            create_bidirectional_truce = { country = scope:target_country months = 60 }
        }
        auto_break_effect = {
            create_bidirectional_truce = { country = scope:target_country months = 60 }
        }
    }
    ai = { will_break = { always = no } }
}
```

实际部署要分放 `common/subject_types/nesnd_egypt_subject_types.txt` 与 `common/diplomatic_actions/nesnd_egypt_protectorate.txt`；不能放同一数据库目录。`potential=always no`沿原生protectorate，由脚本终局建立，避免外交界面给其他国家新入口。新类型不加入任何旧类型的alternatives、war-goal define或release映射。调用effect和postcondition都用新key，玩家本地化可仍称“保护国”。自定义key的`_no_icon`、action名/desc/pact_desc需显式提供；原生键族在diplomacy_l_english.yml:167及1331–1332。

**这不是标准`is_subject_type=subject_type_protectorate`的别名。** M `common/diplomatic_actions/43_subjects_handle_states.txt:97,175` 与 `common/flag_definitions/00_flag_definitions.txt:1156` 等字面检测不会自动匹配；G `37_subjects_decrease_autonomy.txt:134`也有标准类型专门分支。需按EGY用途局部OR自定义类型，不能声称复制数据即与原生所有规则同一身份。其余类型通过autonomy/category与alternatives工作的行为可继承，但仍待真实游戏验证。

### 10.6 “赞助国存活必定保护国”的固有边界及正确结算

没有公开C++源码，本次只读资料**不能证明** `create_diplomatic_pact` 会强制执行 `can_have_as_subject` 的每项资格，也不能证明它一定绕过。原生`potential=always no`却由effect创建，至少说明外交UI入口限制不是effect的可靠等价门槛。因此：

- 不把 `can_have_as_subject=no` 或 `is_subject=yes` 用作“无赞助invalid”条件。
- 0点分支只先按exists＋alive决定是否属于“有赞助者”终局；有赞助者始终尝试建立原生/选定专用保护国，随后核真实postcondition。保留赞助对象直至确认，不先清空。
- 若关系未实际建立，保留独立的pending结果和可重试入口，不能播放成功提示，也不能给用户无赞助失效结局；这个状态代表未兑现指定结果，不能冒称任务完成。
- 专用EGY类型能明确放宽**EGY这条关系**的rank/type；若赞助国以后成为`can_have_subjects=no`的puppet/vassal，其对上级的类型限制是否仍阻止创建，无法仅靠改变EGY类型证明已解除。
- 赞助者若已经处于EGY自己的属国树，直接反向附庸会构成循环；必须先改变至少一条既有关系才能满足图结构。不应假称新类型允许循环，也不应悄悄换一个投资国。该极端结果不是“赞助国已死”。
- 让所有任意未来live sponsor都成为宗主，可能需要解除/改造赞助者原有关系。该动作超出本次“给EGY一条特殊保护国”的最小数据改动，未在这里擅自执行，也不建议以全局放宽puppet/vassal规则解决。

当前SIH这个已确定开局案例没有上述can_have_subjects障碍，标准或专用类型均无需先让SIH脱离USM。正常多层目标应是 **USM→SIH→EGY**，不是EGY直接归USM，更不是把SIH强制独立。

### 补查文件指纹

| 来源 | SHA256 |
|---|---|
| [M/common/history/diplomacy/ce_subject_relationships.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt>) | `78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7` |
| [M/common/subject_types/ce_subject_types.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/subject_types/ce_subject_types.txt>) | `292328c999b666d639bd6ae9795046678d0943b1c996fb6f55c0dd8671390795` |
| [M/common/history/countries/SIH.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/SIH.txt>) | `ed11682a68d67539e91c90a554888bc2a15f43e33e3be48ffdb7af488711a9e8` |
| [M/common/diplomatic_actions/43_subjects_handle_states.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/diplomatic_actions/43_subjects_handle_states.txt>) | `6ead3a6c420f1cc77a7c6fdcc01682ae155eeb65c4b989da636ef9dc1aedcea5` |
| [M/common/flag_definitions/00_flag_definitions.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/flag_definitions/00_flag_definitions.txt>) | `a4be62af5ef7616345625cabd67d65d28351eb6926712fec681eca770a14c950` |
| [G/common/treaty_articles/treaty_articles.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/treaty_articles.md>) | `d374a5030cb977974f65dbd99132c3fe82af3aad6830dfd9d567f78060a2530b` |
| [G/common/diplomatic_actions/diplomatic_action.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/diplomatic_action.md>) | `9f146dd9e108d9753747efb1bf0671a18e19e728f6916a1fcd58c4d0b76fb69c` |
| [G/common/scripted_triggers/00_diplomacy_triggers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_diplomacy_triggers.txt>) | `a3a6cfb1a86709bb35487f6b6c6f2fa3e02496e62896746a4d10aa868ff0bf2f` |
| [G/common/scripted_triggers/00_ai_triggers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_ai_triggers.txt>) | `2bd740780dfa17060f84f28feec041734fd84cce4fda2f764098dcdd69dcd44f` |
| [G/common/diplomatic_actions/37_subjects_decrease_autonomy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/37_subjects_decrease_autonomy.txt>) | `3e154626c260d1424afda4ccfa8df408440f992f1e9a605e0d49d5a5401e99f7` |
| [G/common/defines/00_defines.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt>) | `e47db10931a2149c80aadab0b8de8f3fa000fdbb82a2f878fee893aa4434dd39` |
| [G/localization/english/diplomacy_l_english.yml](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/diplomacy_l_english.yml>) | `d476345a324ed97be4aa2816f82614e2e66c45fbd2ca722638049c18e1604fb7` |

补查验证：报告现有7个text代码块全部保序解析通过；11项源码/引用断言通过（SIH实际dominion、recognized、自治/有附庸权、有效标准保护国限制、专用type/action相互引用、隐藏入口）。未执行引擎；can_have_as_subject结果、effect强制建立与下一tick维护仍非实机结论。
