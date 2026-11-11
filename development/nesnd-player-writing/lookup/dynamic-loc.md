# 主动使用 Victoria 3 的动态本地化

> 何时读：写国名、实时读数、概念链接、加粗与颜色，或改稿需逐键保留动态代码时。不必读：纯措辞修改且不碰动态代码。

写中英文时，主动为当前对象、可悬停的概念和实时数值选用文本函数，以加粗与颜色标示决定性的条款。历史叙述保留史称，当前交涉对象优先用动态国名。

- **国旗与国名。** 埃及投资按钮 `nesnd_egypt_investor_fra`（1.15.0）。中文为 `接受[SCOPE.sCountry('nesnd_label_fra').GetName]投资`，英文为 `Choose [SCOPE.sCountry('nesnd_label_fra').GetName] as investment partner`。用 `GetName` 显示带旗国名。同名日志与按钮脚本 `nesnd_egypt_independence.txt` 中，日志开启及月度更新时以 `c:FRA ?= { save_scope_as = nesnd_label_fra }` 保存对象，按钮用 `exists = scope:nesnd_label_fra` 控制可见性。写别的按钮时换成该按钮实际持有的作用域；延迟答复须查显示时的对象。缺少必要作用域时，纯文字任务记录脚本缺口，先用在各分支都成立的称谓。
- **概念与共用键。** 如 `[concept_diplomatic_play]` 供玩家悬停查看概念，`$ce_cne_land_reform$` 复用日志的正式名称。分别查 GAME 的 `common/game_concepts/` 和对应语言的本地化定义。
- **实时读数。** 日本国民团结条用 `$nesnd_jp_cohesion_bar_name$：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|1] / 100#!`。此函数依赖进度条上下文。其他字段查同类调用。
- **加粗与颜色。** 用 `#bold 地权革命#!` 突出关键政策或条款，用 `#v 24#! 个月` 标出中性期限。收益如 `#g +50#!`，不利的激进派增长可标为 `#r 10%#!`。红绿依效果对玩家的利弊确定，每个标记均以 `#!` 闭合。
- **改稿校验。** 新写内容主动选用适配字段的动态表达。已有文本若只改语体，逐键保留函数、作用域、共用键、数字、格式参数和颜色。中英文可以调整语序，但要引用同一对象、显示相同数值并表达相同效果。技术错误单独修正。两种语言各自保持键唯一、UTF-8 BOM 和正确语言头。字段上下文详见 `nesnd-victoria3/lookup/journal-ui.md`。
