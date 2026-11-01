# 语法、作用域与目录

## Victoria 3 专属约束

```text
namespace = ce_example
ce_example.1 = {
    type = country_event
    title = ce_example.1.t
    desc = ce_example.1.d
    duration = 3
    trigger = { c:USM ?= this }
    option = { name = ce_example.1.a }
    option = { name = ce_example.1.b }
}
```

这是格式骨架，不是已验证的完整可发布事件。`#` 注释、`{}` 分块、`=` 赋值/匹配、`yes/no` 布尔；列表通常没有逗号。多次同名块是序列。带引号的值需处理转义，`rgb { ... }` / `hsv { ... }` 为带类型的数据。`@NAME` 是脚本常量，`$PARAM$` 是脚本替换参数，不是 Python/JS 字符串插值。`@[ ... ]` 等表达式不能用简单的空白切分重写。

`?=` 是可空作用域比较/跳转（读相同用法的原版代码以确定上下文），不是普通赋值。`c:USM` 是 country；`s:STATE_GUANGDONG` 是 state_region；`s:STATE_GUANGDONG.region_state:USM` 才是该地区中 USM 的 state；`cu:han` 是 culture；`rel:confucian` 是 religion；`law_type:law_monarchy` 是 law type。`root`、`this`、`prev` 与 `scope:saved_name` 不互换。

效果的 `if = { limit = { ... } ... } / else_if / else` 与条件里的 `trigger_if / trigger_else_if / trigger_else` 不同。script value 的 `value/add/multiply/min/max` 又是一种上下文。GUI 使用 Jomini widget/datacontext 及 `[Get...()]` 绑定，不能把效果写进 GUI 属性。

作用域是 API 的组成部分。写每个效果前记录“输入 scope→返回/跳转 scope→副作用”。事件可以是 country_event、character_event 等，不能从其他 Paradox 游戏推断 root。

## 必读文档与当前实现配对

以下均相对 GAME，读文档后必须再读右列真实实现；文档里的省略号不是可用语法。

| 任务 | 官方文档 | 当前代码交叉检查 |
|---|---|---|
| 地区 | `map_data/state_regions/state_regions.md` | `11_east_asia.txt` 与 `common/history/states/00_states.txt` |
| 社会阶层 | `common/social_classes/readme.md`、`common/social_hierarchies/readme.md` | `social_classes/00_default.txt`、`01_edo_system.txt`、`social_hierarchies/*.txt` |
| 法律 | `common/laws/readme.md` | `laws/00_distribution_of_power.txt` 等、`ideologies/*`、`ai_strategies/*` |
| IG 吸引 | 无独立完整规范则查代码 | `common/interest_groups/00_landowners.txt` 中实际吸引字段及相关 `pop_types`、`scripted_modifiers`；不要假设旧职业 strata 仍有效 |
| 日志 | `common/journal_entries/journal_entries.md` | `common/journal_entries/00_opium.txt`、带 `scripted_progress_bar` 的 JE |
| 进度条 | `common/scripted_progress_bars/scripted_progress_bars.md` | `00_je_progress_bars.txt`、使用该键的 JE/事件/按钮 |
| 按钮 | `common/scripted_buttons/scripted_buttons.md` | `common/scripted_buttons/*.txt` 和引用者 |
| 角色 | `common/dna_data/dna_data.md`、`common/genes/genes.md` | `character_templates/00_default_template.txt`、`country_afg.txt`、相应 `dna_data` 和 `history/characters` |
| 建筑/生产 | `common/buildings/buildings.md`、`production_methods/production_methods.md`、`production_method_groups/production_method_groups.md` | `common/history/buildings/11_east_asia.txt`、对应建筑和 PM 定义 |
| 军事编制 | `common/history/military_formations/military_formations.md` | 同目录实际编制；1.13 舰船系统不能继续照搬旧 naval base/flotilla 模型 |
| 事件调度 | `common/on_actions/_on_actions.md` | `common/on_actions/00_code_on_actions.txt`、原版事件 |
| UI | `common/scripted_guis/scripted_guis.md`、`gui/scripted_widgets/scripted_widgets.md` | GAME GUI + CMF + Expanded Building Grid |
| 真引擎测试 | `tools/scripted_tests/scripted_tests.md` | 引擎控制台 `help`、当前生成日志；测试文件不能代替在游戏实际运行 |

社会阶层注意：当前 `strata` 属于 social class，不是直接属于 pop type。一个 hierarchy 至少覆盖上下中三层；每种适用 pop 应明确唯一地匹配某个 class。readme 对 catch-all 顺序的描述与其“不依赖歧义顺序”的告诫并存，实施时用互斥条件，不能靠顺序碰运气。

法律注意：`ai_enact_weight_modifier` 只是 AI 立法选择权重，不保证有合法提案条件、政府/运动支持或可承受的革命风险。支持/反对从意识形态与现行法律比较等机制产生，不要拿 AI 权重冒充 IG 立场。

## 覆盖与编码

按目录分别验证同路径替换、数据库条目替换与追加。现代 `REPLACE:key` 可见于本 MOD 的文化和定义，但不能据此假设 history 文件有同等语义。重复国家/地区定义必须审查有效加载结果。不要用 `.bak` 作活动文件；备份在 WORK/backups 的独立目录。

文本保持原换行/BOM风格，局部修改保留注释；本地化键 ` key:0 "文本"` 不能把双引号/反斜杠错误转义。绝不全局格式化或以字典去重引擎脚本。
