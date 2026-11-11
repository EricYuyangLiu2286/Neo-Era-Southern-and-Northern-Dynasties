# 日志界面与本地化上下文（1.15.0，附 1.13 记录）

> 何时读：要知道某段文字在 1.15 日志界面的哪个字段、哪个位置显示，某个本地化函数在什么数据上下文里可用，或排查条面、配图、钉选、概念链接。不必读：日志的状态与生命周期（读 references/journal-state.md）；措辞（读玩家写作技能）。

## 1. 1.15.0 Ivan-Chai 的日志退出、结案页与条（Steam 26453692）

本节是现行接口；下面 1.13.11 笔记中的顶层 `complete/on_complete/fail/on_fail/invalid/on_invalid/on_timeout` 仅作旧档及迁移对照。现行 GAME/common/journal_entries/journal_entries.md:135–194、00_opium_wars.txt:40–112 与 01_ryukyu_rivalry.txt 示范可重复的 `outcome`。同一结局的判定、后果及各参与国单独回调分别放入 `trigger`、`effect`、`effect_all_involved`。保留自定义表头与 `event_outcome_desc/event_outcome_effect_desc`。失效须 `flags = { hidden invalid_outcome }`；超时保留 JE 顶层 duration 字段 `timeout`，并用唯一的 `flags = { timeout }` 结局，后者不能写 trigger。所有结局都需可解析的 conclusion_desc，非隐藏结局还要 header、effect_header。原版 congo 与 prohibition 保留失败居首或失效居首的声明顺序，迁移不要给所有日志重新排序。每个结局没有必填的自定义 ID。

1.15 实体库 449 个 JE 都带 `activation_description`，369 个用 `always = yes`，包括 possible 有另外实际门槛的目标。两者分别维护。面板的 active JE、无实例后的 concluded 记录与 JournalEntryType 分属不同上下文（gui/journal_entry.gui:17、38–145、423–534）。标题依赖所属国或已保存对象时，给结案页静态 `<key>_concluded`。真实条仍由活动 JE + ScriptedProgressBar 取值。在用 `default/default_green/default_bad` 的类型之外，原双边条按 00_ip4_cuba_progress_bars.txt:29–35 用 progress_texture/background_texture/marker；左、右图标须与本地内容相符且确有资源。旧档保留活动实例、期限优先级与新结案页的历史，是独立的引擎验证项目。依据及可重复反例：WORK/reports/migration-115/journals/。

## 2. 条面、配图与字段分工

- **进度条表面只留短指标名和读数**，如“传教：42/100”。原版 1.15.0 的 `gui/journal_entry.gui:428–534` 把顶层 `desc` 画在条内，普通条 504×30，动态图形条 430×30。文本框自动加宽、单行无折行，条面没有独立的 `name`。有右标签的样式用 `second_desc`，左右标签共用这一行。条面读数用 `JournalEntry` 和 `ScriptedProgressBar`。
- “满 100 时当地人口改宗，随后清零”这类整句放在玩家查看后果的位置；作者指定时放到日志状态行。每周、每月、每年的增减来源写入周期块的具名 `desc`，由 `GetPeriodicProgressBreakdown` 悬停显示。长统计可放到状态行绑定的国家提示，使用 `ROOT.GetCountry.GetTooltipTag` 提供 `Country` 上下文。
- 排查按定义取直接子字段 `desc`、`second_desc`，遇到条件描述只展开该字段内的分支。核对中英文本，展开本地化别名，区分链接的可见标签和悬停目标。把读数代入后看条面是否仍为短单行；全文搜索同名 `desc` 会把周期来源误算为条面。
- 图标不等于事件大图。检查非隐藏弹窗是否有`event_image`，同时检查专用人物窗口、已禁用旧事件的例外；已有路径全部存在不代表缺少字段也正确。外交行动未写`texture`会按类型名推导资源，新增类型必须核这一隐式路径。

本轮来源：GAME的scripted_progress_bars.md:3–4、gui/journal_entry.gui及任务36。错误样本包括丹那沙林/吕宋second_desc、无图外交回信、DEI中等国已达12月但小国JE残留。外部修复不等于引擎显示通过。

依据 `GAME/common/journal_entries/journal_entries.md` 及实际 `GAME/gui/journal_entry.gui`：状态说明在按钮之前；scripted buttons 后是 scripted progress bars；正文 `JournalEntry.GetReason` 在其后；完成/失败/超时条件有独立位置。不要把一切塞进 `_reason`。

| 层 | 内容职责 | 当前脚本/GUI依据 |
|---|---|---|
| JE 标题与 `_reason` | 持续冲突、历史背景、各方的要求；可在正文末有简短目标，但不罗列隐藏变量 | `JournalEntry.GetReason`，gui 约 742 行 |
| `status_desc` / 默认 `_status` | 当前处境/阶段、目前阻碍，直接说明，无文学修辞；用 first_valid/triggered_desc 按状态切换 | journal_entries.md 约 175 行；gui 188 行 |
| scripted button | 行动名称；可用/不可用原因、成本、时长、冷却与后果放按钮 tooltip；选择不等于禁用，要用 possible | `common/scripted_buttons/scripted_buttons.md`；gui 215–235 行 |
| scripted progress bar | 顶层 desc 写短指标名与读数；支持右标签的样式用 second_desc；周期块内的 desc 写悬停来源 | `common/scripted_progress_bars/scripted_progress_bars.md`；实际印度兵变示例 |
| 完成/失败/超时 | 可观察的判定与结果；自定义 tooltip 隐藏实现细节时不能隐瞒真实代价 | JE complete/fail/timeout 及对应 on_* |
| 事件 desc | 发生了什么、谁请求什么、玩家面对什么决定 | 当前 events 示例与事件 GUI |
| 事件 flavor | 首先参照作者原有引文、诗句和人物话语；需要时再写场景，不能每条强造一段官署故事 | 原版 MOD 的 `.f` 键；见 `nesnd-player-writing` 技能 |
| option 名称与效果提示 | 名称是行动/表态，效果提示解释实际收益、代价和风险 | event option / custom_tooltip |

按钮 `_desc` 可写行动的政治理由；实际消耗/冷却/可用条件由 effect、possible 与独立 custom_tooltip 展示。已触发不再可用的原因应直接说明。脚本 progress bar 使用自身 desc/second_desc；不可把普通 JE 的 `progress_desc` 误接到 scripted bars。文本验证同时检查动态值、概念链接、人物 scope、颜色闭合与实际布局。

- 全局JE分开设置参与国与其他国家的默认钉选：`should_be_pinned_by_default_involved`、`should_be_pinned_by_default_uninvolved_or_context`。只写后者不会给实际参与国设默认钉选。原版`00_peoples_springtime_je.txt:317–318`并用两项；既有存档的玩家钉选状态不冒充新激活的默认值验证。

## 3. 概念与数据上下文

概念链接同时查 `GAME/common/game_concepts/00_game_concepts.txt` 定义和对应本地化，不是看见 `concept_xxx` 翻译键就可直接链接。例如本机`concept_unemployment`只有名词本地化，定义是`concept_unemployed`；用`[Concept('concept_unemployed','$concept_unemployment$')]`，原版migration_pull说明有实例。

`[concept_default]`是债务违约；`[concept_bankruptcy]`是宣告破产。若判定`has_modifier = declared_bankruptcy`，准确写“[concept_bankruptcy]后的惩罚仍生效”；不能将赤字、违约和多年破产修正混成同一事实。CNE/供给帮助文字逐条核实际条件，不用全局词语替换。

动态读数和机制链接依照所处数据上下文：bar desc中的`JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)`，国家tooltip中的`Country.MakeScope.Var('...').GetValue`，事件中的`ROOT.GetCountry`并不互换。当前南朝文字维护在`nesnd_south_politics_l_<language>.yml`；具体链接仍需首次打开和悬停实测，不能因原生API存在就声称展示已通过。

2026-11-04实机反例：国家JE的status_desc使用JournalEntry.GetCountry会每帧反复报“没有JournalEntry上下文”；当前原版journal_entries.md说明root为owning country，经济复兴状态用ROOT.GetCountry读取国家变量。状态按ROOT写，bar/GUI按其实际数据对象写；禁止对所有本地化盲目替换。每种语言每key只有一个维护文件，直接修改主题条目，不再加z覆盖层。

### Country 标签的嵌套动态悬停（run143454 实际失败）

日志状态的外层可用 `#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],my_stats_link 统计#!#!`。`my_stats_link` 内层仅获得 Country 对象，动态国家变量应写 `[Country.MakeScope.Var('my_value').GetValue|%1]`，不得继续写 ROOT.GetCountry；不得为省事改为 GetPlayer。当前原版 `content_204_l_english.yml:787—788` 和 `agitators_4_l_english.yml:1473/1478` 有完整调用对，`companies_l_english.yml:25—26` 也展示 GetTooltipTag→Country 的绑定。只在这种对象绑定层切换根，事件和JE正文既有 ROOT 不能全局替换。日志轮转与读法见 verification.md。

### 国家日志状态、预报和条的反例（2026-11-05）

以调用位置确认数据对象。原版 1.13.11 的 `common/journal_entries/06_economic_regeneration.txt:24–37` → `localization/english/ip4_spain_l_english.yml:21` 用 `ROOT.GetCountry.MakeScope.Var` 读取国家状态。第39轮原始日志反复报告日本 `status_desc` 的 `Country.GetCustom` 缺少 Country。对有州／无州等预报，在 JE 的 `first_valid/triggered_desc` 中核所属国、有效对象和状态后选择文字，只在有对象的文本中从根读已保存的州／文化。Realism AI 10.9 的 `common/journal_entries/dsk_je_jap.txt:15–35` 有并列状态组。另有明确 Country datacontext 的 GUI 行可以调用 Country；不能用其例证明状态正文或嵌套文字有同样的数据对象。

原版 `gui/journal_entry.gui:246–288` 由类型选择器绘制进度条，并从当前 JE 取值；已挂条和翻译齐全仍可能因只写 `default_green = no` 而没有可绘制样式。逐项核一个启用样式、当前值／上限、明细和 0／中间／满值三态。限期读实际到期限变量；原版 `interest_tier_types_l_english.yml:71` 由 `GetVarTimeRemaining` 取得剩余天数。测试由状态入口跟到实际分支及中英文叶键，分别覆盖缺值/失效、所有者变更、期限内/期限后、有并行状态和无其他状态；将旧错接回同一检查须失败。未开游戏时，仅记录静态结论。
