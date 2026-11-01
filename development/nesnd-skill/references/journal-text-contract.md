# 日志、事件和说明的分工（本机 1.13.11）

依据 `GAME/common/journal_entries/journal_entries.md` 及实际 `GAME/gui/journal_entry.gui`：状态说明在按钮之前；scripted buttons 后是 scripted progress bars；正文 `JournalEntry.GetReason` 在其后；完成/失败/超时条件有独立位置。不要把一切塞进 `_reason`。

| 层 | 内容职责 | 当前脚本/GUI依据 |
|---|---|---|
| JE 标题与 `_reason` | 持续冲突、历史背景、各方的要求；可在正文末有简短目标，但不罗列隐藏变量 | `JournalEntry.GetReason`，gui 约 742 行 |
| `status_desc` / 默认 `_status` | 当前处境/阶段、目前阻碍，直接说明，无文学修辞；用 first_valid/triggered_desc 按状态切换 | journal_entries.md 约 175 行；gui 188 行 |
| scripted button | 行动名称；可用/不可用原因、成本、时长、冷却与后果放按钮 tooltip；选择不等于禁用，要用 possible | `common/scripted_buttons/scripted_buttons.md`；gui 215–235 行 |
| scripted progress bar | name 是指标；desc/second_desc 是当前读数；周期增减的 desc 解释来源；两个相反指标可放同一 JE | `common/scripted_progress_bars/scripted_progress_bars.md`；实际印度兵变示例 |
| 完成/失败/超时 | 可观察的判定与结果；自定义 tooltip 隐藏实现细节时不能隐瞒真实代价 | JE complete/fail/timeout 及对应 on_* |
| 事件 desc | 发生了什么、谁请求什么、玩家面对什么决定 | 当前 events 示例与事件 GUI |
| 事件 flavor | 首先参照作者原有引文、诗句和人物话语；需要时再写场景，不能每条强造一段官署故事 | 原版 MOD 的 `.f` 键；见 author-prose-profile.md |
| option 名称与效果提示 | 名称是行动/表态，效果提示解释实际收益、代价和风险 | event option / custom_tooltip |

旧候选把土地进度和风险拆成两个无故事日志，又把规则塞进正文，需要改造。若用 scripted progress bars，必须核对独立存储与变量的同步：不能让条本身 monthly_progress 与 JE on_monthly 同时重复计分。源注释说明前者先执行；旧国家变量、存档迁移、按钮与事件变更均应统一到一个权威状态，真实游戏测月界和保存重载。

有些旧 readme 的按钮 AI 示例用 base/modifier，本机实际 scripted button 用 script value 的 value/if/add；事件 option 的 ai_chance 仍用 base/modifier。分别核对，不套成一个语法。

按钮 `_desc` 可写行动的政治理由；实际消耗/冷却/可用条件由 effect、possible 与独立 custom_tooltip 展示。已触发不再可用的原因应直接说明。脚本 progress bar 使用自身 desc/second_desc；不可把普通 JE 的 `progress_desc` 误接到 scripted bars。文本验证同时检查动态值、概念链接、人物 scope、颜色闭合与实际布局。

## 概念、实际状态与随机姓名

概念链接同时查 `GAME/common/game_concepts/00_game_concepts.txt` 定义和对应本地化，不是看见 `concept_xxx` 翻译键就可直接链接。例如本机`concept_unemployment`只有名词本地化，定义是`concept_unemployed`；用`[Concept('concept_unemployed','$concept_unemployment$')]`，原版migration_pull说明有实例。

`[concept_default]`是债务违约；`[concept_bankruptcy]`是宣告破产。若判定`has_modifier = declared_bankruptcy`，准确写“[concept_bankruptcy]后的惩罚仍生效”；不能将赤字、违约和多年破产修正混成同一事实。CNE/供给帮助文字逐条核实际条件，不用全局词语替换。

动态读数和机制链接依照所处数据上下文：bar desc中的`JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)`，国家tooltip中的`Country.MakeScope.Var('...').GetValue`，事件中的`ROOT.GetCountry`并不互换。已有候选可参考`zzzzz_nesnd_south_journal_ui_*`；具体链接仍需首次打开和悬停实测，不能因原生API存在就声称展示已通过。

“马 马”已由原生角色字段证明是随机名池组合，不是作者模板。随机名字修订改`common/cultures/CE_cultures.txt`对应名池和独立`nesnd_given_*`键，不全局重译Ma；混合文化保留其其他片段，固定历史人物和旧存档已保存的名字不自动变化。单字名或名姓同字并非语言上必错，是否回避是本项目命名设计。完整溯源与候选见WORK/plans/two-empires/32-names-and-test-harness.md。
