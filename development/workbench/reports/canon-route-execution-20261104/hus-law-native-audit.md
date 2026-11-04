# HUS 新公民权法律：原版完整链条审计

日期：2026-11-04。游戏：Victoria 3 1.13.11，Steam build 24799966。技能 catalog status = CURRENT，changed_count = 0。本报告仅阅读实际 GAME、候选 C 与本机导出的引擎文档；未修改玩法，未启动游戏。结论是 SOURCE_AUDIT，不是 ENGINE_PASS。

## 结论与优先修正

候选确实创建了三项真实法律，归入原生公民权法律组，并由日志在等待后使用原生 `activate_law` 更换。满蒙文化的独立判定也避免了修改全球 `manchu` 的 `heritage_han`。这些基础方向成立。[C01:1-44][C03:21-33][C04:8-9][C12:292-299]

目前不能把它认证为完整、长期自洽的“汉一等、满蒙二等、原住民三等、白人四等”制度：它是有正确开局基线的文化接纳度方案，并没有创建社会阶序或固定阶级上下限；还存在施加法律作用域错误、改法后修正残留和旧档无入口等缺口。先修前三项确定脚本缺陷，再按下文明确等级制度的承诺范围。

| 优先级 | 问题 | 最小处理 |
|---|---|---|
| P1 | 六项普通公民法 `can_impose` 的锁检查施加国而非目标国 | 将锁放入 `scope:target_country`；保留原版其余 OR 条件 |
| P1（若承诺固定社会等级） | 只有接纳度加值，没有真正社会阶序/阶级接纳上下限 | 采用完整 social_hierarchy/social_classes 链条，或明确本轮只承诺基线法律待遇，不能把后者称为已完成固定社会阶序 |
| P2 | 三项新法无 `on_deactivate`，改成普通公民法后旧接纳修正保留到月脉冲 | 三法退出时立即 `nesnd_hus_clear_tiers = yes`；启用时明确安装本法修正 |
| P2 | 改法或外部激活后，锁完全由“目前仍有旧法”推导，缺少独立初始阶段状态 | 若要求任何入口均锁住初始阶段，保存初始化/待登记状态，并处理 `on_law_activated`；不要只用当前 law 推导整个生命周期 |
| P2（若承诺旧档适用） | 仅 history 激活新法；旧档不会执行这段历史 | 增加只执行一次的旧档迁移及 successor 排除，或交付明确限新局 |
| P2 | NKH/原住民 HUS 不显式设置 default hierarchy，主体文化清理遍历对象不精确 | 在准备/改 tag 后显式设 default hierarchy；清除旧主体文化用 `every_primary_culture` |
| 政策补全 | parent 不能作为完整法律效果继承的依据；当前很多原生待遇项缺省 | 逐项确定投票、同化、工资、政治力量、资质、官职、军职；不要盲目把普通文化排斥的全部数值复制进来 |

## 1. 原版完整链条及实际语义

### 1.1 法律组、变体与意识形态

`lawgroup_citizenship` 位于 power_structure，ideological_opinion_impact = 1.0，affected_by_regime_change = yes。它没有 linked_social_hierarchy。日本/印度的社会阶序法律组则另有 `linked_social_hierarchy`，它不是给公民法改一个名称就自动拥有的能力。[G01:32-50]

本版普通公民法共有六项：subjecthood、ethnostate、national_supremacy、racial_segregation、cultural_exclusion、multicultural。没有找到“日本专属公民法变体”或“奥地利专属公民法变体”；本版日本使用普通 subjecthood，并另用 Edo 社会阶序。因此不能虚构一个日本/奥地利 citizenship variant 来证明实现。[G02:5-720][G10:14-27]

实际可用的变体实例是：

- 奥地利 `law_crownland_diets`：parent = law_hereditary_bureaucrats，并明确注释“继承意识形态立场”；它自己再声明 group、is_visible、modifier、on_enact、disallowing_laws、ai_will_do 与 ai_enact_weight_modifier。[G03:54-105]
- 日本 `law_sakoku`：parent = law_isolationism，同样明确继承意识形态立场；独立声明条件与数值，并用 on_activate/on_deactivate 联动边境法律及地主意识形态。[G04:289-367]
- 原版文化排斥自身的完整条款包括 unlocking_laws、on_enact、can_impose、国家接纳组成和 acceptance_modifier；父法律名称没有替代这些条款的完整声明。[G02:486-609]

所以现有 `parent = law_cultural_exclusion` 是合法且有原版依据的政治立场入口，但不能据此认定工资、同化、资质、政力等未写字段全部继承。也不能把 `progressiveness` 当作 IG 支持度：IG/人物立场来自意识形态的 lawgroup_citizenship 映射。[G11:569-579][E02:12701-12704]

三个新法同一个 parent，因此默认继承同一文化排斥立场，满蒙/原住民分支不会自动产生彼此不同的政治支持。候选 HUS 地主添加 ideology_liberal；该意识形态赞成文化排斥。郭庆达是 industrialists 的 ruler + ig_leader，ideology_radical；radical 的明示政治条款并不等于额外支持这两个登记分支。当前日志结算直接激活法律，也没有请求政府支持/统治者批准；这是明确的脚本机制，而不是正常立法已经通过。[C07:47-55][C13:1092-1106][G11:569-579][G12:1176-1259]

引擎另提供 `has_law_or_variant`，会把三个新法视为文化排斥的变体。需要意识到其他使用该触发器的原版机制会接纳它们；它们虽然有不同接纳待遇，却不是与文化排斥完全无关的法律。[E02:10471-10476]

### 1.2 正常立法、施加、脚本激活是三个入口

`can_be_enacted` 与 `law_is_available` 是 law scope；后者忽略政府支持。`ai_enact_weight_modifier` 再高也不能越过支持不足、ai_will_do 等限制。候选的三项 `can_enact = { always = no }` 因此意味着玩家/AI不能经普通立法按钮通过它们；这不妨碍被历史或日志脚本激活。[G05:1-11][E02:8898-8904,12687-12692][C01:5,21,35]

`activate_law` 是 country scope → law_type 的原生 effect。原版 on_law_activated 文档明确说脚本直接激活绕过 enactment process，仍会触发 on_law_activated，而不会触发 on_law_enactment_ended。此 on_action 的 root = law，应进入 owner 后处理国家变量/修正。[E01:12-15][G06:5020-5033,5108-5119]

**施加法律作用域有一处原版文档自身矛盾。** laws/readme.md:31-34 的旧说明称目标国为当前 scope；实际 scripted_rules 和 scripted_triggers 的当版注释都写 root = imposing country、scope:target_country = imposed upon，且当前实际 `law_colonial_administration.can_impose` 使用 `scope:target_country ?= { ... is_subject_of = root }`。本次以实际调用链为准。[G05:28-34][G07:145-150][G08:1806-1822][G09:310-315]

候选六项普通法的 can_impose 顶层直接写 `nesnd_hus_citizenship_unlocked = yes`，因此判断了施加国：普通宗主向尚未登记 HUS 施法时，这个新增条件会通过；尚未登记 HUS 向外国属国施法时，却错误禁止。即便引擎另一层也用 can_enact 阻断前者，这一层守卫本身仍然方向错误，不能作为已覆盖强制改法的证据。[C02:23-35,142-154,269-281,398-410]

最小原生修正形状：

```text
can_impose = {
    scope:target_country = { nesnd_hus_citizenship_unlocked = yes }
    # 保留当前原版 OR = { 同集团施法 / can_impose_law_default } 原文
}
```

三个新法也建议显式 `can_impose = { always = no }` 与 `ai_will_do = { always = no }`，表达它们只能由本国日志/历史脚本获得。原版缺少 can_impose 时会使用默认 scripted rule，因此“不写”和“禁止”不等义。[G07:145-150][G09:302-315,325-327]

### 1.3 四等基线实际算对了，但不是恒定阶序

候选每文化加值为汉85、满蒙55、原住民35、白人15；开局 total_separation 对全部宗教另加15。排除额外州/文化修正时，新局基线如下；主流汉文化另有 primary_culture = 100，受最大值100约束。[C08:2-149][C01:6][C07:71,79][G13:483-487][G14:1489-1507]

| 文化类别 | 初始文化项 | 宗教项 | 基线总接纳 | 原生等级 |
|---|---:|---:|---:|---|
| 汉文化 | 85；主体文化至少100 | +15 | 100 | full_acceptance（80起） |
| 满蒙 | 55 | +15 | 70 | second_rate_citizen（60起） |
| 美洲原住民 | 35 | +15 | 50 | open_prejudice（40起） |
| 白人 | 15 | +15 | 30 | cultural_erasure（20起） |
| 满蒙登记后的满蒙 | 80 | +15 | 95 | full_acceptance |
| 原住民登记后的原住民 | 80 | +15 | 95 | full_acceptance |

因此“55不是二等”并不是正确缺陷；它漏掉了宗教项。当前登记法确实提升选定群体的原生接纳等级，而不只是换名称。[C08:150-445][G15:12-46]

但这些是加值，**不是边界**。例如改成 state_religion 后，无共同宗教特质的满蒙可能是55-25=30，白人中信奉国教者可能是15+25=40，原本满蒙高于白人的关系能够翻转。primary文化高接纳也不等于所有汉文化都绝对固定：非主体汉文化85-25=60可跌到次等。州级 acceptance delta、文化加值和新文化社区的初始修正还能改变当地结果。当前没有锁 church_and_state，也没有社会阶层上下限。[G13:41-44][G14:1506-1507][E01:21-24][C01:1-44]

若用户的“一二三四等”仅指当前开局的法律待遇，这个方案有原生作用且可以保留；若指制度内无论宗教和州级波动都恒定的社会阶序，当前实现未达标。不能只在文案里声称“社会阶序”而省去下列机制。

### 1.4 真正 social_hierarchy 的完整原版链条

日本链：country_definitions 的 JAP.social_hierarchy = edo_system → history 激活 law_intermediate_edo_system → social_hierarchies 定义适用人群 → social_classes 定义每个 pop 的职业、文化与经济 strata → lawgroup_edo_social_system 关联 hierarchy → 法律对各 social class 设置接纳上下限和资质效果 → culture_panel 与 pop_details_panel 展示阶层/边界。终止时 `set_social_hierarchy = default_social_hierarchy`，不是只删除一项国家修正。[G10:14-27][G16:201-210][G17:17-24][G18:1-68][G01:45-50][G19:175-322][G20:57-70][G21:214-247,839-1040][G22:429]

原版严格 Edo 的例子是高武士 min80、低武士 min60/max70、庶民 min20/max59、贱民 max19；中等 Edo 则调整庶民的边界。印度法律也有同形字段，明确证明这是一套国家法律控制的实际接纳钳制机制。[G19:188-210,241-261,34-40]

创建 HUS 专属 hierarchy 的最小完整方案：

1. `nesnd_hus_social_hierarchy` 的 pop_criteria 覆盖本制度定义的四类人群；未覆盖人群回到 default。不得改变 default hierarchy 的 is_default。[G29:11-80]
2. 使用互斥文化触发器：先区分 `this = cu:manchu` 与 heritage_mongolian；汉文化条件显式排除满洲；再原住民/白人。继续保持全球 manchu = heritage_han。
3. 保留经济 strata 的既有意义：建议每类文化按原版 upper/middle/lower 职业分组交叉成12个 social classes，而不是把所有汉人无论职业一律放入 upper。对每个适用 culture × profession，必须且只能命中一个 class。原版文档明确说明漏配/重叠属于不受支持状态，可能造成严重运行问题。[G23:18-54,134-161][G24:1-38]
4. 沿用原版 `country_<social_class>_acceptance_min_add/max_add` 命名模式与 modifier type metadata，并给每个文化层级的三个职业 class 同样的边界。初始为汉80–100、满蒙60–79、原住民40–59、白人20–39；登记后把选中群体提高至80–100。具体 numeric policy 可调整，但不需要改全球文化。[G19:200-209][G25:1-21,93-193]
5. HUS历史及旧档迁移显式 set hierarchy；三项公民法保留真实 lawgroup_citizenship 身份，以其 modifier 控制这些 class。**不建议为了展示把原生 citizenship group 全局 linked 到HUS hierarchy**，那会影响所有国家。若要求单列“阶序法组”，再建独立法组并明确其与公民法的同步关系，不能把两组状态放任漂移。
6. GUI并非全自动：culture_panel 的阶序标题/法条条目对 caste_hegemony 和 edo_social_system 写了两段显式分支；一般 class 列表使用 SocialHierarchy 数据。自定义 hierarchy 的标题与法律入口需定点适配现有框架，不能凭数据库定义就宣称玩家能完整看到它。[G21:182-247,725-879,1026-1040]
7. 普通公民法取代三项新法时恢复 default；NKH与原住民HUS继承者始终 default。原版移除阶序示例见 G20。

这是一项完整的新系统实现，不是给当前文件补一个 social_hierarchy 字段即可。当前报告不将该建议伪称为已写好或实测通过。

## 2. 法律效果矩阵：必须明确的缺省行为

原版 citizenship 的 acceptance_modifier 负责投票、政治力量、工资、资质、同化、军职和官职待遇；并非“接纳值越低便自动拥有原版所有惩罚”。[G02:557-598]

| 通道 | 当前初始法 | 两项登记法 | 审计判断 |
|---|---|---|---|
| 政治权威 | +100 | +50 | 明确生效的政策变化 |
| 投票 | violent/cultural_erasure禁投；open票力-50%；second票力-25% | 相同 | 选中群体升至full，投票权力随真实acceptance tier改善 |
| 政治力量 | open -20%；second -10% | 都未写 | 登记同时取消未选择群体既有政力惩罚；不能声称收益只发生在被选群体 |
| 工资 | cultural_erasure -20% | 未写 | 白人基线30从工资-20%变成无本法工资惩罚，无论选哪条分支 |
| 资质增长 | 未写 | 未写 | 不能假设父法的 -50/-30/-10%存在 |
| 同化许可/速率 | 全部未写 | 全部未写 | 不能假设父法的许可 yes 与加速继承；若设计允许同化必须声明 |
| 军职 | cultural_erasure禁职；violent未写 | 同左 | 更低接纳人群未被本法显式禁军职，政策可能出现倒挂 |
| 官职 | violent与cultural_erasure禁职 | 只写cultural_erasure禁职 | 登记后最受敌视人群未被本法显式禁官职，反而30分人群仍禁止 |
| 激进/忠诚、分离主义、文化热忱 | 未写 | 未写 | 不自动获得普通法条款；是否需要由设计决定 |

建议先写出最终待遇矩阵，再在三法中完整声明关键 bool 和选择的数值。不能把每个缺省都自动称为BUG，也不能假装父法已替它补齐。至少低于20分的人不应无意比20–39分的人享有更多军政职业资格；未选择群体的普遍改善也应是有意政策。[C01:6-14,22-28,36-42][G02:557-598]

`country_*_cultural_acceptance_add` 本身有原生 modifier type 与原版修正案实例（海地波兰归化 +60），并不是虚构API。将这些加值直接放进三项法的 modifier 可以自然随法律启停，避免额外国家修正生命周期；若继续用 static_modifier，则务必补启用/退出清理。[G26:1-7][G27:242-255]

## 3. 生命周期、初始化与异常路径

### 3.1 新局、旧档与12个月结算

新局入口：HUS history 激活初始法；日志 possible 与 inactive 展示都要求 original HUS + 当前初始法 + 未done；按钮只允许一次 choice；choice 创建12个月限时变量；月脉冲发现 wait不存在后激活对应登记法并设done。AI按钮权重满蒙100、原住民0，所以它有选满蒙的脚本偏好；这不是本轮已经观测AI点击的证据。[C07:79][C05:1-15][C06:1-14][C03:21-33][C09:1-5]

因为完成检测在月脉冲，实际改法发生在12个月等待到期后的下一次检查；不是已证明在精确到期日即时执行。若文案仅说“耗时一年”可以理解为约一年，若验收要求精确12个月，应改成有明确原生时序依据的定时结算，并保留幂等检查。

旧档若仍使用原有公民法，不会重放 country history；当前月维护只刷新已有三法/已有选择，没有激活初始法的迁移逻辑，日志也永远不可达。因此当前只支持新局，或已由其他手段激活该法的档。修旧档需独立 `nesnd_hus_registration_initialized` 版本标记、排除原住民 successor，并明确应否覆盖玩家已经改变的旧公民法；不能静默每月覆盖玩家改革。[C03:55-63][C04:6-7][C09:1-5]

### 3.2 on_activate 不能假设已看见新法

候选三项 on_activate 都调用 `nesnd_hus_refresh_tiers`，后者用 `has_law` 判断究竟安装哪项修正。原版国教法的 on_activate 会检查当前是否仍有 law_state_atheism，再恢复国教，说明不能未经验证假设这个回调里的 has_law一定已是新法。[C01:15,29,43][C03:6-19][G13:467-480]

日志结算在 activate_law后又显式refresh，因此它有第二次同步；但单独history/其他脚本激活并不能靠这个回调独立证明即时一致。最小办法是每项 on_activate 直接 clear后添加自己的修正，而不是再按当前法猜；on_deactivate直接clear。更稳妥的是把文化值放进该法modifier，取消额外同步层。[C03:27-33][G04:339-367]

### 3.3 确定存在的退出清理缺口

普通法开放后，玩家把登记法改成任一普通公民法，三个 custom laws 都没有 on_deactivate。`nesnd_hus_refresh_tiers` 确实会清，但它只由特定law on_activate、JE和月维护调用；普通法激活没有调用这套refresh。所以旧国家修正最多持续到下一月，与普通公民法的接纳值叠加。另一个可能状况是已有正确修正又带额外错误修正，refresh只看正确修正是否缺失，不清除多余项。[C01:1-44][C03:6-19][C09:1-5]

最小可审改法：三项 on_deactivate = { nesnd_hus_clear_tiers = yes }；每项 on_activate按自身法律安装确定的修正；保留月维护作旧档修复，但应保证恰好一项匹配修正，或零项普通法。on_deactivate是已查到的原版API，不需自造事件。[G04:352-367][G28:120-122]

### 3.4 锁、外部激活与登记中断

当前锁仅是 `NOT = { has_law = initial }`。任何直接脚本activate、政体更迭或其他入口一旦换掉初始法，锁立刻消失；日志 invalid会删除wait但保留choice。若随后又激活初始法，choice还在且wait已不存在，下一次settle可立即完成，不再等一年。这个状态机边界在当前文件中能静态复现。[C04:1-7][C05:9-10][C03:21-33]

应选择并实现一个明确策略：初始阶段被外力改法时保持/恢复初始锁；或者承认改革被终止并清choice、wait，允许重新选择。不要保留“已选但无等待且未完成”的半状态。若用户说锁只针对普通立法，正常 `can_enact` 守卫足够表达该范围，但应明确没有禁止直接脚本改法；若说初始制度必须锁死，需独立初始化状态配合 `on_law_activated`，在owner scope幂等恢复，避免递归触发。[G06:5020-5033]

## 4. NKH 与原住民 HUS 继承者

候选NKH定义以 siouan/cherokee 为主体文化；prepare直接激活racial_segregation及total_separation，继承者转换后也激活racial_segregation并清HUS tiers，因此已有的正面逻辑应保留。[C10:1-4][C11:53-61,129-143]

仍需补齐：

- 两个阶段显式 `set_social_hierarchy = default_social_hierarchy`。当前两处都没有；代码依赖建国/改tag时的隐含行为。若HUS本次升级为真实hierarchy，这项退出更成为硬要求。原版有确切effect与解除Edo示例。[E01:37134-37137][G20:65-70]
- 清旧主体文化用 `every_primary_culture`，不要用 `every_scope_culture` + is_primary_culture_of模拟。引擎把前者定义为主体文化枚举，后者仅是当前scope的文化枚举；当前第二轮可能漏掉不在境内的旧主体文化。显式补删五个汉/满蒙键也没有穷尽所有外国主体文化，正确枚举可彻底消除这个假设。[C11:93-108][E01:3194-3198,4689-4693]
- 顺序必须先添加至少一项合法原住民主体文化，再遍历当前主体文化删除所有非原住民。若目标国无原住民人口，须有确定fallback（NKH定义自带siouan/cherokee），不能删除到零项。
- successor 标记在change_tag前设置是正确顺序，现有 original_country 排除该标记；保留这一守卫，禁止后续旧档初始化把原住民共和国再次变成汉人初始法。[C11:129-143][C04:6]

## 5. 外部验证与引擎验证边界

可直接完成的外部检查：

1. 解析合并后的六普通法，逐项确认can_enact锁和can_impose.target锁仍存在，原版其他字段未意外丢失；三个定制法禁普通立法/施加。
2. 对国家生命周期做静态状态矩阵：新局、无标记旧档、等待中、两条完成、改普通法、外部改法后回初始、successor、附属国与非HUS；每态验证choice/wait/done、law、tiers/hierarchy无不一致。
3. 用实际GAME+候选解析文化定义，Manchu判定优先；SHA证明全球文化文件未改。计算基线100/70/50/30，同时建立反例宗教与州级delta，确保报告没有把baseline当invariant。
4. 若建真实hierarchy，穷举每个覆盖culture × religion × profession；每组合恰好命中一个class，每经济strata都有定义；所有modifier type/本地化/icon/GUI引用闭合。
5. 验证两分支效果矩阵：选中群体提高，未选群体的工资、政力、官军职变化是否与批准设计一致；不能只断言文件包含新law key。

本次未做、不能用静态检查代替的引擎语义：law.on_activate与新法状态的精确时序；新法是否在UI显示预期的继承支持；真实can_impose菜单/施加结算；脚本激活对IG重算与on_law_activated的回调；AI按钮自然选择；12个月自然到期与存读档；自定义hierarchy的UI和每pop分类。用户当前要求不启动游戏，应把这些明确留在交付限制，不重复已有无关开局。

## 来源索引

下列编号、路径和SHA由读取实际文件生成。正文 `[编号:行号]` 指当前文件的一基行号；行号区间只用于审计定位，不表示所有片段都已游戏内执行。E为2026-10-31导出的1.13.11引擎文档，与catalog确认的当前build一致。GAME是实际安装目录，不是复制基线。

| ID | Actual source file | SHA-256 |
|---|---|---|
| G01 | [00_laws.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/law_groups/00_laws.txt>) | `dc2cc8675a97353c297f0ec5d96e75bc2ab67df90079841088310da8c56140b4` |
| G02 | [00_citizenship.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_citizenship.txt>) | `c006054323511c81b40502810c4ed8f6a806ebde02bf0a3023538e756ec9bb10` |
| G03 | [00_bureaucracy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_bureaucracy.txt>) | `3d4b720fa18a75f361075504dfc1cf9e0ba1a90200a5b2e6bff9c3a1bad8f98f` |
| G04 | [01_trade_policy.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_trade_policy.txt>) | `f6e0ca1e180c57f994aae1a04ea3e407bfadd4ede85f75f67c303ed16d734e6d` |
| G05 | [readme.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/readme.md>) | `2e172974c75e5a544777f0a21099019043ca0164d499927786e10572b8956a0c` |
| G06 | [00_code_on_actions.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>) | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |
| G07 | [00_scripted_rules.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_rules/00_scripted_rules.txt>) | `520c6da79f4832838bb59371ee2c5c4efc97b9b9fa736e6e78916db760aae92d` |
| G08 | [00_scripted_triggers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt>) | `66432c31661d560146707744da29475cae92bbb6cbe432a1f0409133c92a3178` |
| G09 | [00_governance_principles.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt>) | `e676448ea64c17079677ddbf2cbfdbec0ffdefa465286f16c1e6107a14e7f4cf` |
| G10 | [jap - japan.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/jap - japan.txt>) | `b9e7df278cb01ab2e5059a142d28a8102f88efcc0bae517c646787cc554113c5` |
| G11 | [00_ig_ideologies.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/00_ig_ideologies.txt>) | `4c8bc020d2d1060795e5a615b850736b731a31193862399363ec2e1829639b05` |
| G12 | [01_character_ideologies.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/ideologies/01_character_ideologies.txt>) | `b54d0c294632be73ebc77edcb65d7f841803c6a19bacbb03e6331b0cd2ce39d3` |
| G13 | [00_church_and_state.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_church_and_state.txt>) | `ad4e366533b268a86f29813c13aeae6f7472d94de84c35bfe51ce960fd8bb015` |
| G14 | [00_defines.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt>) | `e47db10931a2149c80aadab0b8de8f3fa000fdbb82a2f878fee893aa4434dd39` |
| G15 | [00_acceptance_statuses.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/acceptance_statuses/00_acceptance_statuses.txt>) | `a4edb8eb0b7d78d34d0fbd320312856cd0e41b60e9c1d3713fe767fed7425409` |
| G16 | [00_countries.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt>) | `d13a2a5ddfe9391287be287041c28611599fed537d1d41c3fb5691de08872a74` |
| G17 | [00_social_hierarchies.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_hierarchies/00_social_hierarchies.txt>) | `792c51c15d7239a39879d285fff07ddb7df9d1b0ceb06f05e503b47551780808` |
| G18 | [01_edo_system.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_classes/01_edo_system.txt>) | `eb102ffd1367c91fd06125470bc48fc3deea26b168507187f1f70881cd9cc09c` |
| G19 | [00_caste_hegemony.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_caste_hegemony.txt>) | `0c31a075766c3fc3db997e23b9aa61d737fe0c4c1086a5c8f501a2d03eecbae8` |
| G20 | [set_hierarchy_events.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/set_hierarchy_events.txt>) | `90a810b2dcae5c04e99ecab5798b978dbb2e68a19b98163ede600f21228f0729` |
| G21 | [culture_panel.gui](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/culture_panel.gui>) | `17f02494fe2e797d75750493d368441a446128f891bb149947c759fd1959f295` |
| G22 | [pop_details_panel.gui](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/pop_details_panel.gui>) | `5a2e03b8ce0ec3b08e28b3d1a7fd75bd1ea339cd565e8fa0efc929cb69fdd5f8` |
| G23 | [readme.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_classes/readme.md>) | `f861a9f7953b59e6daafad72da526ace79243e47a47785c8d179ff4c56456458` |
| G24 | [00_default.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_classes/00_default.txt>) | `cef1b21c99752d04523139dba1a3519804fff690b204c42c98e5be85e347e8d8` |
| G25 | [09_social_class_modifier_types.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/09_social_class_modifier_types.txt>) | `1f79d5a49a233263fdc2314033eb3e4ba8b15fcceb023ff9250b4e04e6be4cd3` |
| G26 | [10_country_cultural_acceptance_culture_modifier_types.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions/10_country_cultural_acceptance_culture_modifier_types.txt>) | `e93dc0657d388ee6931770864838cd66afc63c069e6727a9c7e0e64bfdab11ae` |
| G27 | [00_amendments_historical_04.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/amendments/00_amendments_historical_04.txt>) | `4350452fbb9db5b7263bdc348f2383f9d1b83be377ab6cd9891c59a7ff842bbe` |
| G28 | [02_migration.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/02_migration.txt>) | `53229809fe63dd8d4c7748fa2205183c737f8afbfb60ab2e9510bc4d65fff5e3` |
| G29 | [readme.md](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_hierarchies/readme.md>) | `537eb57ac08f78168d5ca5ee3ea5aff4ebfdc94b02d4f5982d6d11bde4eacef0` |
| C01 | [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/laws/nesnd_hus_registration.txt>) | `d1cea0a8f06d6815ecf3d0e42ceec53add6ee5347215b11c5a45e6510e235343` |
| C02 | [zzzz_nesnd_hus_citizenship_lock.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/laws/zzzz_nesnd_hus_citizenship_lock.txt>) | `f27fa12c8ee7ebe3a2a4e48b30e971278d8c31677172cfb5db3c27ba330d3f40` |
| C03 | [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_hus_registration.txt>) | `a744fe86df9ffa26f167c579c81b8741f7415c4f1783f330986ea55b2f6bb047` |
| C04 | [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_triggers/nesnd_hus_registration.txt>) | `ccef3df31459352f302188e4795c4cdfd5a3e2cca25dcecf4853512122f2663f` |
| C05 | [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/journal_entries/nesnd_hus_registration.txt>) | `84096af19c44c4cfcbcda6661d1c2f809bdf740a8752f3a929c5e6bf2a7dbe3a` |
| C06 | [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_buttons/nesnd_hus_registration.txt>) | `2ef65c78cac49dd6e1895fad6afc2cc25f887dece14a15afc90d004572a3b1a1` |
| C07 | [HUS.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/history/countries/HUS.txt>) | `3c37f1c75bdf0b18f4adc877ad2b94103840302d227ef89cdbc47c181187c639` |
| C08 | [nesnd_hus_culture_tiers.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/static_modifiers/nesnd_hus_culture_tiers.txt>) | `09b62190a871499d7590c66195588432ce49bceb4fa14fde0eb6135ac2132a53` |
| C09 | [nesnd_hus_registration.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/on_actions/nesnd_hus_registration.txt>) | `8bdb1e7a048680e108c3e2bc7dc3778b0ff0817dce07fbba0eff4eb98f2c2494` |
| C10 | [nesnd_native_khanate.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/country_definitions/nesnd_native_khanate.txt>) | `67318bccd394b9d4ea4c735eb7e6ac7756fc5784ca26a226406dc0a60fd9b4d4` |
| C11 | [nesnd_native_khanate.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/scripted_effects/nesnd_native_khanate.txt>) | `2e3f9f2a93fa27a2f721428a9827f2105ec8cab971c90ffac49dc40af8442f22` |
| C12 | [CE_cultures.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/cultures/CE_cultures.txt>) | `deab0fd04a418e17f063665669610d3930d1af007a513d38da6b86247fe400b0` |
| C13 | [zz_historical_leaders_ce_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/canon-route-execution-20261104-a/common/character_templates/zz_historical_leaders_ce_asia.txt>) | `d740dc245ef314bfa2889687fc23db366b7945c0427f376573d547daf2d595ad` |
| E01 | [effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>) | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |
| E02 | [triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log>) | `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e` |
