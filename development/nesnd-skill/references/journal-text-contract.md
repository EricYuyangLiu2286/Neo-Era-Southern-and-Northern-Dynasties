# 日志、事件和说明的分工（1.15.0，附 1.13 记录）

## 1.15.0 Ivan-Chai 的日志退出、结案页与条（Steam 26453692）

本节是现行接口；下面 1.13.11 笔记中的顶层 `complete/on_complete/fail/on_fail/invalid/on_invalid/on_timeout` 仅作旧档及迁移对照。现行 GAME/common/journal_entries/journal_entries.md:135–194、00_opium_wars.txt:40–112 与 01_ryukyu_rivalry.txt 示范可重复的 `outcome`。同一结局的判定、后果及各参与国单独回调分别放入 `trigger`、`effect`、`effect_all_involved`。保留自定义表头与 `event_outcome_desc/event_outcome_effect_desc`。失效须 `flags = { hidden invalid_outcome }`；超时保留 JE 顶层 duration 字段 `timeout`，并用唯一的 `flags = { timeout }` 结局，后者不能写 trigger。所有结局都需可解析的 conclusion_desc，非隐藏结局还要 header、effect_header。原版 congo 与 prohibition 保留失败居首或失效居首的声明顺序，迁移不要给所有日志重新排序。每个结局没有必填的自定义 ID。

1.15 实体库 449 个 JE 都带 `activation_description`，369 个用 `always = yes`，包括 possible 有另外实际门槛的目标。两者分别维护。面板的 active JE、无实例后的 concluded 记录与 JournalEntryType 分属不同上下文（gui/journal_entry.gui:17、38–145、423–534）。标题依赖所属国或已保存对象时，给结案页静态 `<key>_concluded`。真实条仍由活动 JE + ScriptedProgressBar 取值。在用 `default/default_green/default_bad` 的类型之外，原双边条按 00_ip4_cuba_progress_bars.txt:29–35 用 progress_texture/background_texture/marker；左、右图标须与本地内容相符且确有资源。旧档保留活动实例、期限优先级与新结案页的历史，是独立的引擎验证项目。依据及可重复反例：WORK/reports/migration-115/journals/。


## 2026-11-05实测纠正：公开条件、条内文本与配图

- 从玩家入口`possible/complete/fail`递归展开scripted trigger后审查。身份枚举、初始化和防重复记录用`hidden_trigger`；影响玩家决定的前置、等待、正在进行的选择，各用一句具名条件；法律、建筑、合法性等仍用原生条件。不要把`visible`或状态分支内的变量误计为屏幕上的裸变量。`any_*`中的国家身份比较会产生scope-dependent描述警告，对实际候选集合做简短提示，不展示“他们是本国”的枚举。
- `second_desc`是进度条右侧标签，不是悬浮说明。只放短单行。长统计移至已绑定国家的tooltip；状态入口用`ROOT.GetCountry.GetTooltipTag`绑定后，目标tooltip才可用`Country.MakeScope`。条内读数使用`JournalEntry`/`ScriptedProgressBar`上下文。每条新增bar的desc须同时有指标名与实时值，不能只有数字或“已连续经营月数”静态文字。
- 图标不等于事件大图。检查非隐藏弹窗是否有`event_image`，同时检查专用人物窗口、已禁用旧事件的例外；已有路径全部存在不代表缺少字段也正确。外交行动未写`texture`会按类型名推导资源，新增类型必须核这一隐式路径。
- 常驻议程可无胜负，明确存续及关闭原因；真正成果用complete，身份/所有权失去用invalid。退出条件需要否定整个合取时，用明确OR的各项失效原因或NOT包AND，不能依赖多项NOT的含混阅读。已有国别counter完成而旧阶段JE仍在时先查真实存档，不再给一遍进度/奖励。

本轮来源：GAME的scripted_progress_bars.md:3–4、gui/journal_entry.gui及任务36。错误样本包括丹那沙林/吕宋second_desc、无图外交回信、DEI中等国已达12月但小国JE残留。外部修复不等于引擎显示通过。

依据 `GAME/common/journal_entries/journal_entries.md` 及实际 `GAME/gui/journal_entry.gui`：状态说明在按钮之前；scripted buttons 后是 scripted progress bars；正文 `JournalEntry.GetReason` 在其后；完成/失败/超时条件有独立位置。不要把一切塞进 `_reason`。

| 层 | 内容职责 | 当前脚本/GUI依据 |
|---|---|---|
| JE 标题与 `_reason` | 持续冲突、历史背景、各方的要求；可在正文末有简短目标，但不罗列隐藏变量 | `JournalEntry.GetReason`，gui 约 742 行 |
| `status_desc` / 默认 `_status` | 当前处境/阶段、目前阻碍，直接说明，无文学修辞；用 first_valid/triggered_desc 按状态切换 | journal_entries.md 约 175 行；gui 188 行 |
| scripted button | 行动名称；可用/不可用原因、成本、时长、冷却与后果放按钮 tooltip；选择不等于禁用，要用 possible | `common/scripted_buttons/scripted_buttons.md`；gui 215–235 行 |
| scripted progress bar | name 是指标；desc/second_desc 是当前读数；周期增减的 desc 解释来源；两个相反指标可放同一 JE | `common/scripted_progress_bars/scripted_progress_bars.md`；实际印度兵变示例 |
| 完成/失败/超时 | 可观察的判定与结果；自定义 tooltip 隐藏实现细节时不能隐瞒真实代价 | JE complete/fail/timeout 及对应 on_* |
| 事件 desc | 发生了什么、谁请求什么、玩家面对什么决定 | 当前 events 示例与事件 GUI |
| 事件 flavor | 首先参照作者原有引文、诗句和人物话语；需要时再写场景，不能每条强造一段官署故事 | 原版 MOD 的 `.f` 键；见 `nesnd-player-writing` 技能 |
| option 名称与效果提示 | 名称是行动/表态，效果提示解释实际收益、代价和风险 | event option / custom_tooltip |

旧候选把土地进度和风险拆成两个无故事日志，又把规则塞进正文，需要改造。若用 scripted progress bars，必须核对独立存储与变量的同步：不能让条本身 monthly_progress 与 JE on_monthly 同时重复计分。源注释说明前者先执行；旧国家变量、存档迁移、按钮与事件变更均应统一到一个权威状态，真实游戏测月界和保存重载。

2026-11-01南朝反馈补充：

- 全局JE分开设置参与国与其他国家的默认钉选：`should_be_pinned_by_default_involved`、`should_be_pinned_by_default_uninvolved_or_context`。只写后者不会给实际参与国设默认钉选。原版`00_peoples_springtime_je.txt:317–318`并用两项；既有存档的玩家钉选状态不冒充新激活的默认值验证。
- 事件调用scripted effect时，沿调用链找真实加分位置。陈死亡的＋25在`nesnd_chen_after_death`，不能因事件文件只有函数名便再加一次。变量改变后同步国家JE与全局JE的对应bar，保留preview scope guard和一次结算标记；同时审查intro/immediate的归零，刷新与旧档迁移不能覆盖已经积累的值。
- 节奏有明确期限时，同时核月增量、随机等待、人物存活门槛、各国答复期限及外交阶段。随机事件概率不等于最迟日期；用既有事件入口安排明确窗口，并让延迟死亡先结算再进入后续。具体南朝1837–1839安排属于本轮用户规格，见主项目任务11，不推广成其他剧情的固定年份。
- 同一按钮组按政治身份筛选：中央朝廷不提供“从自身争取自主”或“对自身争位中立”的入口。固定阵营须同时约束初始化、只读显示、AI复议、盟约和事件默认选项；只改初始数值不能保证下一月仍有效。

日志正文用作者同类原文的政治议题、行动者与具体利害；“每周更新、实际检查、达标检验、对应事件结算”等开发说明移出正文和叙事状态。按国家写当前阻碍，完整门槛保留在对应tooltip，避免一国日志列出四国的检查清单。本轮对照与外部检查见`WORK/reports/south-feedback-20261101/prose-review.json`、`source-checks.json`；未启动游戏。

有些旧 readme 的按钮 AI 示例用 base/modifier，本机实际 scripted button 用 script value 的 value/if/add；事件 option 的 ai_chance 仍用 base/modifier。分别核对，不套成一个语法。

按钮 `_desc` 可写行动的政治理由；实际消耗/冷却/可用条件由 effect、possible 与独立 custom_tooltip 展示。已触发不再可用的原因应直接说明。脚本 progress bar 使用自身 desc/second_desc；不可把普通 JE 的 `progress_desc` 误接到 scripted bars。文本验证同时检查动态值、概念链接、人物 scope、颜色闭合与实际布局。

## 概念、实际状态与随机姓名

概念链接同时查 `GAME/common/game_concepts/00_game_concepts.txt` 定义和对应本地化，不是看见 `concept_xxx` 翻译键就可直接链接。例如本机`concept_unemployment`只有名词本地化，定义是`concept_unemployed`；用`[Concept('concept_unemployed','$concept_unemployment$')]`，原版migration_pull说明有实例。

`[concept_default]`是债务违约；`[concept_bankruptcy]`是宣告破产。若判定`has_modifier = declared_bankruptcy`，准确写“[concept_bankruptcy]后的惩罚仍生效”；不能将赤字、违约和多年破产修正混成同一事实。CNE/供给帮助文字逐条核实际条件，不用全局词语替换。

动态读数和机制链接依照所处数据上下文：bar desc中的`JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)`，国家tooltip中的`Country.MakeScope.Var('...').GetValue`，事件中的`ROOT.GetCountry`并不互换。当前南朝文字维护在`nesnd_south_politics_l_<language>.yml`；具体链接仍需首次打开和悬停实测，不能因原生API存在就声称展示已通过。

2026-11-04实机反例：国家JE的status_desc使用JournalEntry.GetCountry会每帧反复报“没有JournalEntry上下文”；当前原版journal_entries.md说明root为owning country，经济复兴状态用ROOT.GetCountry读取国家变量。状态按ROOT写，bar/GUI按其实际数据对象写；禁止对所有本地化盲目替换。每种语言每key只有一个维护文件，直接修改主题条目，不再加z覆盖层。

“马 马”已由原生角色字段证明是随机名池组合，不是作者模板。随机名字修订改`common/cultures/CE_cultures.txt`对应名池和独立`nesnd_given_*`键，不全局重译Ma；混合文化保留其其他片段，固定历史人物和旧存档已保存的名字不自动变化。单字名或名姓同字并非语言上必错，是否回避是本项目命名设计。完整溯源与候选见WORK/plans/two-empires/32-names-and-test-harness.md。


## 改革子日志与具名目标（2026-11-01）

长改革把各项目的建设/法律条件、启停和真实利益得失放入对应子日志；主日志保留总进度、失序与终局。删减主tooltip时把仍在使用的完成阈值迁到子日志，统一有效本地化键，检查旧replace层是否还保留过时的进度说明。主成功/失败/invalid/主动结束及意外移除都清理临时项目，子日志依赖实际父JE，不能仅靠永久flag。

涉及“最高失业州”等动态目标时，先通过具名州的placement/本地化确认事件展示目标与实际费用，再扣款；保存目标不在确认时悄悄换州。确认、取消和执行检查这个保存对象的资格，而不只检查全国还有任一合格对象。当前CNE例子见WORK/reports/cne-reform-subjournals-20261101，尚未引擎验收。

IG吸引力、IG支持与角色忠诚各用自己的实际修正。逐州军队支持是国家修正，军官忠诚是角色修正，不能把character_loyalty_add塞进国家修正并假设传给全体军官。按州唯一key对应开始/暂停/终局清理；显示可叠加的实际代价。角色维护按受影响对象列表处理，参照原版00_sgui_effects的daimyos_list与00_victoria_ep2_scripted_effects的variable列表迭代；新任、转属、退役和终局分别处理，避免月度全世界人物扫描。


## 国家日志状态、预报和条的反例（2026-11-05）

以调用位置确认数据对象。原版 1.13.11 的 `common/journal_entries/06_economic_regeneration.txt:24–37` → `localization/english/ip4_spain_l_english.yml:21` 用 `ROOT.GetCountry.MakeScope.Var` 读取国家状态。第39轮原始日志反复报告日本 `status_desc` 的 `Country.GetCustom` 缺少 Country。对有州／无州等预报，在 JE 的 `first_valid/triggered_desc` 中核所属国、有效对象和状态后选择文字，只在有对象的文本中从根读已保存的州／文化。Realism AI 10.9 的 `common/journal_entries/dsk_je_jap.txt:15–35` 有并列状态组。另有明确 Country datacontext 的 GUI 行可以调用 Country；不能用其例证明状态正文或嵌套文字有同样的数据对象。

原版 `gui/journal_entry.gui:246–288` 由类型选择器绘制进度条，并从当前 JE 取值；已挂条和翻译齐全仍可能因只写 `default_green = no` 而没有可绘制样式。逐项核一个启用样式、当前值／上限、明细和 0／中间／满值三态。限期读实际到期限变量；原版 `interest_tier_types_l_english.yml:71` 由 `GetVarTimeRemaining` 取得剩余天数。测试由状态入口跟到实际分支及中英文叶键，分别覆盖缺值/失效、所有者变更、期限内/期限后、有并行状态和无其他状态；将旧错接回同一检查须失败。未开游戏时，仅记录静态结论。

## 原生进度条与初始化恢复

GAME/common/scripted_progress_bars/scripted_progress_bars.md与本MOD ce_french_empire_progress_bars.txt支持monthly_progress/yearly_progress内具名add={desc=... value=...}，value可用脚本值或有守卫的变量。先用原生明细呈现来源，勿用长篇更新说明替代空白条。

已有国家变量供存档与事件使用时，允许同一条公式供原生明细与实际结算共同调用；原生条先于同周期JE脉冲运行，随后JE更新国家变量并绝对set_bar_progress。必须在同一JE完成周期计分与同步；不得再把已经自动增长的bar读回后加同一增量。跨父子JE年度顺序无此保证。新建/旧档、月年同日、按钮改变与临时scope预览都分别查；源码公式相同不等于引擎验收。

一次性schema/init标记与可恢复running标记分开。若开场事件在父JE加入前初始化，孤儿清理可删running；后续恢复不可因init已存在而永远跳过。实际父JE有效且无终局时，恢复running并用has_journal_entry保护显式补齐子JE；不重置进度/信心。on_fail/on_invalid与旧档迁移都应覆盖。

州按钮的开始与暂停都看所属州是否仍存在于本国。原生on_state_owner_change/on_state_created的root为state（GAME/00_code_on_actions，ip4_on_actions有移除州modifier实例）；检查父JE有效后清理失去的州，再用具名国家事件清理对应国家/人物惩罚，保留其他州。补周度检查覆盖旧档与部分割地。普通脚本战争与原生revolution/secession分别判定，不能用is_at_war代替内战。


## 原生条件优先与状态节制（2026-11-02）

### 1.15 可见结局与自动激活（2026-11-06）

用户要求独立剧情日志有可见的关闭条件。按当前 `GAME/common/journal_entries/journal_entries.md:135–194`，`outcome` 的 `hidden invalid_outcome` 不显示在结局面板。结构合法不等于玩家能知道如何结束。查每个实际启用的日志：常驻政策可直接显示原有终止条件，不另造满条胜利、奖励或一套存在性分支；真正依附父日志的条目注明父日志，并核实际存续依赖。暂时无目标而允许恢复的隐藏失效，才与长期退出分开。

同文档25–49说明自动激活需要 `is_shown_when_inactive` 与 `possible`，显式 `add_journal_entry` 则绕过两者。互斥子日志优先用“父日志有效＋方案已选”控制两项自动条件，单一入口。不能一边永远隐藏潜在条目，一边用每周重复add当作激活已证明的证据。若日志报告already has而UI不见，先查实际激活条件及实例状态。

触发器能判真，不代表其原生自动描述有正确数据上下文。本轮 `is_on_defending_side` 可执行，但经国家条件展开时原版 `TRIGGER_IS_ON_DEFENDING_SIDE` 读取 `War.GetName` 而没有War上下文。保留原布尔子树，以一句具名custom_tooltip包装这一判定；不改战争创建、阵营或和平规则，也不伪造全局原版翻译。

工具与证据：WORK/reports/prose-icons-20261106/root/verify_delivery.py、outcomes/audit_native_outcomes.py、原始error-before.log。检查真实原缺陷和原版字段，主MOD后的检查不得要求旧缺陷仍存在。STATIC_PASS不代表游戏内显示已验证。

- 先读作者原始日志/按钮的 trigger，再查当前 GAME 同类条目。能直接呈现的法律、科技、机构、建筑、国库等条件直接写在 possible/complete，独立条件各占原生勾叉。不要把多项真实门槛塞入一个 custom_tooltip；换行不能替代独立真假状态。
- 全国等级用 country_has_building_type_levels = { target = bt:building_iron_mine value >= 25 }（GAME/common/scripted_buttons/07_japan_buttons.txt）；州分布另用 any_scope_state 的 count 与 state_has_building_type_levels。五州各有五级城镇中心不等于每州须同时达到全国工业总量。
- custom_tooltip 只用于原生显示无法说明的自定义统计/对象选择，以及未自动呈现的必要效果；写最短的可判断条件。原生 effect 已显示关系变化，就不再加一行相同数字。内部存在性、schema、重复执行保护用 hidden_trigger，但不能隐藏真实玩家资格或费用。GAME/common/scripted_buttons/00_balkan_wars_buttons.txt 有原生隐藏示例。
- AI 谨慎阈值与玩家资格分别维护。用户指定仅供 AI 的政力、破产、失序限制，放 is_ai 分支/AI选择权重，不能悄悄变成玩家硬门槛。玩家仍须支付实际费用；该规则不自动删除完成条件或进度公式里的同名指标。
- status_desc 用 first_valid/triggered_desc 呈现当前阶段；没有新增信息时留空。未发生的起义不在开场预告。状态不复述按钮已列的门槛；按钮 desc 不复述原生效果。统计面板只保留读数。
- 检查同国同时激活的全部 JE 挂载。两个名称不同、调用同一操作的按钮依然可能重复；删除冗余挂载不删除其他日志或 AI 使用的 effect。

本轮来源与前后对照：WORK/reports/ui-trade-feedback-20261102/research.md、WORK/reports/ui-poland-tributary-20261102。源码检查不能证明实际UI布局。

## 非开局入口、终局回调与镜像条

新增父子JE或后继JE时，画“初始化→添加父JE→添加子JE”有向图；初始化effect不反向添加自己的JE。possible不能正向依赖自己的has_journal_entry；完成effect判断持久资格、进度和done，不要求该JE仍在活动列表。显式添加与自动possible入口共用终局锁，维护回调补漏不重置既有进度。
有期限的JE保留country期限标记，意外移除再添加不得刷新十年；端点保持时间必须离开后清除重计。军事基线在大厅结束后读实际建筑数量，日志初始化过早时使用有界次日恢复及旧档月度入口，不能把未初始化的0当正常基线。
通常由本JE独占country结算及条同步；父/子需要镜像时仍只有一个country写入者，每个JE自身回调做绝对同步，并覆盖两种回调顺序。外部顺序模型只证明脚本约定，不能替代引擎时序验收。实例与12项生命周期矩阵见 WORK/reports/qin-persia-20261102/。

## 阶段可进入与永久结束分开

跨阶段JE分别定义available（现在允许开始）与eligible（国家/制度仍允许继续）。未达到后继阶段不能被通用bootstrap当作永久invalid而提前写archived。当前已活动的旧档JE可在维护effect登记opened标记；不要把自己的has_journal_entry写进possible形成首次进入自锁。后继已解锁不因暂时丢失触发地重置，完成/封存锁仍独立阻止重领。西秦五脚本修正及原版“维新完成标记→神佛分离决议→宗教JE”来源见WORK/reports/japan-research-20261102/qin-stage-design.md。

## 按钮预览与周期占比：2026-11-03实际反馈

禁止滥用custom_tooltip不等于删除变量效果提示。按钮可见/可用条件不保证effect预览受同样条件约束；执行内的if在预览时可能展开内部缺值，或已设置标记使效果消失。把真实守卫留在hidden_effect，外层用简短custom_tooltip说明不可原生呈现的变量、路线与一次性期限，配show_as_tooltip显示真实modifier/law/treasury；不得重复同一收益。验证实际执行AST及提示两面。

国家变量完成条件没有本地化时，只包装对应单项条件，勿用全局伪造country_var_*翻译或把无关门槛合成一个勾叉。建筑用bt引用时核对实际定义键，别名不保证可作scope：本轮error.log证明building_textile_mills失败，而building_textile_mill正确。先查同类JE/events/decisions完整链条，再决定用全国累计还是单座建筑；两者不能为显示漂亮而互换。

占比条每周重算不是每月固定增量。原生weekly_progress应解释新目标减旧值，并纳入同周期扶持撤销，再由既有单一写入者绝对同步；只读预览不得改变持久变量。依据：原生00_ip4_victoria_progress_bars与本轮QE1三权来源/80组边界报告。

证据：WORK/reports/persia-journal-ui-20261103/release-notes.md、sources.json、button-feedback-other-review.md、qe1-court-progress-research.md。未做引擎验收。

## 阶段切换与数值同步：印度反例

保存变量并不会自动初始化新加JE的条。JE immediate、保留进度后重新进入、按钮改变与外国镇压改变都调用同一个只同步效果；计分仍只有该JE的周期回调。同步时保存当前country并保护存在性，不用可能是全球调用者的root读取国家变量。跨国/全局案件只负责生命周期，避免与国家JE重复推进。

暂时条件（战争、破产、军力或合法性）失去时按设计暂停、停维护费并保留案件；不要共用“新建资格”作为存续资格，导致自动清案与长冷却。建设奖JE完成之后仍需要的治理/防御按钮应挂在常驻入口。人口与领土成果不是按钮退出时的临时修正。

实际前后：WORK/reports/india-development-20261103/india-spec-review.md、india-spec-review-final.md及final-validation.json。未开游戏。

## 法律影响按法组呈现

进度条增减包含法律时，先按实际 `lawgroup` 拆分贡献值，并用该法组的既有本地化名作行名。一行内部用 `if/else_if/else` 表达不同现行法律即可；不同法组分别显示，便于玩家从负数找到可调整的法律。社会动荡、机构等级、经济和战争另列，避免混进“法律”行。内部总和函数可以保留，但实际结算和UI不得把分项与总和重复计入。

依据：2026-11-04作者纠正；西秦旧 `nesnd_qe1_unity_laws` 混合公民权、宗教与军队法组，印度共同认同又把社会动荡与公民权混在一起。当前来源与实施要求见 WORK/reports/canon-route-execution-20261104/unity-inventory-and-native-contract.md、batch-b-unity-plan.md；最终是否通过以该批验证报告为准。

## 绝对条件数与切换重点（1851测试档反例，2026-11-04）

现值条不是“从进入日志起再增加多少”。goal_add_value会保留进入时baseline；东洋JE存档baseline=2、goal=5，现值1显示−1/3。当前条件数/占领数改用有界scripted_progress_bar，immediate同步现值，周期明细算目标减当前条。旧活动JE必须迁移而不能只改定义留着旧baseline；迁移不得重置外交结果或重发奖励。

互斥建设重点若仅暂停推进，显示/存续条件与计分条件分开。取消重点不等于invalid；父日志结束/不再符合国家身份才清退。复核调用者根scope：country JE/tick与JE-root bar不是同一root，跨层shortage等国家参数显式传入，并核全部调用点。别用未经验证的prev.prev链掩盖根对象不明。

来源、39组文案对读、实际AST边界与局限：WORK/reports/journal-war-feedback-20261103/。静态检查不认证旧档JE重建的引擎显示时序。
