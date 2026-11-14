# 文化团结度日志：结构、范例与避坑

> 何时读：新建或修改“团结条 + 按团结高低转化 Pop 文化”的日志。不必读：只有团结条、只加减修正、不转化文化的日志（如奥斯曼「国家团结度」），按 journal-state.md 写。

现有三例（1.15.1）：日本 `nesnd_jp_cohesion`、西秦 `nesnd_qe1_unity_journal`、唐衣大食 `nesnd_per_unity_journal`。

## 1. 结构

```
进度条（明细，引擎先算）──┐
                          ▼
月脉冲 <P>_monthly：更新团结值 → 执行上月预选 <P>_settle → 清空 → 为下月预选 <P>_prepare
                                      ▲                                   │
                                      │ 同一个条件                         ▼ 写
                               <P>_plan_valid ◄──────────── 国家变量 <P>_next_*（模式、州、Pop、源/目标文化）
                                      │                                   │ 读
                                      ▼                                   ▼
                     状态行 triggered_desc                   规模 script value <P>_next_size
                                      └──────── 本地化：Var(...).GetState / GetCulture、ScriptValue(...) ┘
```

- **权威值只有一个。** 用国家变量记团结值，月脉冲末 `set_bar_progress` 覆盖条；条的 `monthly_progress` 只用来显示明细。引擎先跑条的月更新，再跑日志月脉冲（GAME `common/scripted_progress_bars/scripted_progress_bars.md:17`），所以不会重复计分。也可以反过来以条为准、脉冲把条值读进变量（唐衣大食），但同一日志只能选一种。
- **转化目标在上个月末抽定。** 执行时只读变量，不再抽签。显示与执行调用同一个有效性 trigger，复核失败时两边同时变成“不转化”。
- **时间写“下次月结”。** 脚本存不了日期，周计数又耗性能（作者 2026-11-12 否决），所以状态行写“下次月结”和“届时团结度须仍低于／高于 X”。

- **统一结束。** 研究身份证件（`identification_documents`），或采用委员会共和国／法团国家时，三个日志各以一个蓝色结局结束，并写入永久标记 `nesnd_cohesion_fixed`。条件统一放在 `common/scripted_triggers/nesnd_unity_policies.txt`：`nesnd_cohesion_fixed_by_ideas`、`nesnd_cohesion_fixed_by_ideology`、`nesnd_cohesion_open`。新日志的 `possible`、`is_shown_when_inactive` 以及所有 `add_journal_entry` 入口都要带 `nesnd_cohesion_open = yes`。带团结补贴按钮的日志，每个结局都调用 `nesnd_unity_stop_subsidies`：补贴按周计入开支，撤掉修正就不再支出。选身份证件，是因为它有每州税收容量 +25，后面还接中央计划，玩家很难为保留同化而绕开它（作者 2026-11-13 定）。

## 2. 最小范例

参数：`<P>` 前缀，`<TARGET>` 文化键，`<LOW>`/`<HIGH>` 阈值，`<CHANCE>` 抽中几率（百分比），`<FRACTION>` 转化比例。下面是“一州一批”的写法。“一个 Pop”见日本 mode 1；“全国微量”不需要预选，直接按当月团结执行，显示用实时求和。

```
# journal_entries
<P>_journal = {
    group = je_group_historical_content
    activation_description = { always = yes }
    can_revolution_inherit = no
    is_shown_when_inactive = { <P>_country = yes }
    possible = { <P>_country = yes }
    immediate = { if = { limit = { NOT = { has_variable = <P>_cohesion } } set_variable = { name = <P>_cohesion value = 70 } } <P>_sync = yes }
    scripted_progress_bar = <P>_bar
    on_monthly_pulse = { effect = { <P>_monthly = yes } }
    status_desc = {
        first_valid = { ... 处境三档 ... }
        first_valid = {
            triggered_desc = { trigger = { <P>_plan_valid = yes } desc = <P>_next_state }
            triggered_desc = { trigger = { has_variable = <P>_next_mode <P>_value < <LOW> } desc = <P>_next_missed }
            triggered_desc = { trigger = { has_variable = <P>_next_mode } desc = <P>_next_mid }
            desc = <P>_next_none
        }
    }
    outcome = {
        header = nesnd_journal_closures_header  effect_header = nesnd_journal_closures_effect_header
        color = "blue_negative"  conclusion_desc = <P>_closed
        trigger = { custom_tooltip = { text = <P>_closed_tt NOT = { <P>_country = yes } } }
        effect = { <P>_clear_plan = yes }
    }
}
# script_values
<P>_value = { value = 70 if = { limit = { has_variable = <P>_cohesion } value = var:<P>_cohesion } }
<P>_next_size = {
    value = 0
    if = { limit = { <P>_plan_valid = yes }
        var:<P>_next_state = { add = { value = 0 every_scope_pop = { limit = { NOT = { culture = cu:<TARGET> } } add = total_size } multiply = <FRACTION> } }
    }
}
# scripted_effects
<P>_monthly = {
    change_variable = { name = <P>_cohesion add = <P>_delta }
    clamp_variable = { name = <P>_cohesion min = 0 max = 100 }
    <P>_settle = yes
    <P>_prepare = yes
    <P>_sync = yes
}
<P>_settle = {
    if = { limit = { <P>_plan_valid = yes }
        var:<P>_next_state = { every_scope_pop = { limit = { NOT = { culture = cu:<TARGET> } } change_pop_culture = { target = cu:<TARGET> value = <FRACTION> } } }
    }
}
<P>_prepare = {
    <P>_clear_plan = yes
    if = { limit = { <P>_value < <LOW> }
        set_variable = { name = <P>_next_mode value = 0 }      # 0 也是抽签结果，读档不重抽
        save_scope_as = <P>_plan_owner
        random_list = { <100−CHANCE> = { } <CHANCE> = {
            random_scope_state = { limit = { any_scope_pop = { NOT = { culture = cu:<TARGET> } } }
                scope:<P>_plan_owner = { set_variable = { name = <P>_next_state value = prev } set_variable = { name = <P>_next_mode value = 1 } }
            }
        } }
        clear_saved_scope = <P>_plan_owner
    }
}
<P>_clear_plan = {
    if = { limit = { has_variable = <P>_next_mode } remove_variable = <P>_next_mode }
    if = { limit = { has_variable = <P>_next_state } remove_variable = <P>_next_state }
}
# scripted_triggers
<P>_plan_valid = {
    trigger_if = { limit = { has_variable = <P>_next_mode exists = var:<P>_next_state }
        has_journal_entry = <P>_journal
        <P>_value < <LOW>
        var:<P>_next_state = { owner = prev any_scope_pop = { NOT = { culture = cu:<TARGET> } } }
    }
    trigger_else = { always = no }
}
```

```
# 本地化（中英同键，状态行属机制文字：短、直白、数字与脚本一致）
 <P>_next_state:0 "\n下次月结：[ROOT.GetCountry.MakeScope.Var('<P>_next_state').GetState.GetName]约 #v [ROOT.GetCountry.MakeScope.ScriptValue('<P>_next_size')|D]#! 人转为[GetCulture('<TARGET>').GetName]文化。届时团结度须仍低于 #v <LOW>#!。"
 <P>_next_missed:0 "\n下次月结：不转化。本月没有抽中任何[concept_state]，团结度低于 #v <LOW>#! 时每月有 #v <CHANCE>%#! 的几率。"
 <P>_next_mid:0 "\n下次月结：不转化。团结度在 #v <LOW>#! 到 #v <HIGH>#! 之间。"
 <P>_next_none:0 "\n下次月结：不转化。"
```

再加一条：日志关闭以外的退出路径（亡国、换 tag）由 `common/on_actions/nesnd_unity_policies.txt` 的 `nesnd_discard_retired_unity_forecast` 每月兜底清理，新日志在那里补一行。

## 3. 避坑

| 不要这样写 | 应该这样写 | 原因 |
|---|---|---|
| 别国也会求值的 value／条件里直接读 `var:<P>_cohesion` | `has_variable` 分支或带默认值的 `<P>_value` | 未设置变量刷 error.log（任务 23） |
| 按钮费用读一个只在点击后才写的变量 | 有守卫的 script value | 首次点击报错（任务 36） |
| 改文化、改宗分两次随机比例 | 先转入过渡文化，再整体改宗、改文化；每次先清残留的过渡文化 | 保证两者落在同一批人身上；中断会留下孤儿文化（西秦，Git 4014560） |
| `NOT = { culture = scope:目标 }`、`culture = prev.var:目标` | 目标作为参数直接写 `cu:键`；从变量取的文化用 `var:x = { this = cu:键 }` 分支 | 1891 档每次比较都报 “Invalid right side during comparison”，转化静默跳过，刷 1 万条（任务 38） |
| 被 `common/social_classes` 的 `pop_criteria` 调用的 trigger 里写 `cu:` | `has_pop_culture = 键` | 社会阶层条件解析不了 `cu:` 链接（2026-11-12 东洲满洲阶层）。改共用的 Pop trigger 前先查有没有被社会阶层引用 |
| 状态正文用 `Country.GetCustom` 取国家 | `first_valid` 先判有无对象，文字从 `ROOT.GetCountry.MakeScope.Var(...)` 读 | 缺 Country 上下文报错（任务 39） |
| 预告抽一次、执行时再抽一次 | 预选存变量，执行只读变量；“本月不抽”也存 0 | 显示与实际不符；读档或刷新会重抽（任务 39） |
| 只在关闭结局里清预告变量 | 结局 + 每月 on_action 兜底 | 亡国、换政权后变量残留（任务 39） |
| 规则说明写进进度条 desc | 条 desc 只放读数，规则放第二段状态行 | 条面单行，溢出（任务 65） |
| 可见结局不写 `color` | 写 `color = "blue_negative"` 等原版色 | 加载时报 “outcome has no color” |
| 结束条件里只写法律 | 结局里写永久标记，`possible` 和补加入口排除该标记 | 法律可以改回去，日志会重新激活 |
| 删人口、造人口来模拟同化 | `change_pop_culture` | 作者要求，人口与州归属不变 |
| 让 trigger_event 后面的预选覆盖事件要用的 saved scope | 交给事件的对象另起名字（如 `_settle_` 前缀），事件里再转存 | 同一效果里后续的 `save_scope_as` 可能改写已排队事件读到的对象（西秦，2026-11-12 起这样写） |

## 4. 新建清单

- [ ] 团结值只有一个写入者；条 desc 只放读数。
- [ ] 每个预选变量都有写、读（执行、显示或规模值）、清理；用 `v3tree near var:<名>` 核对。
- [ ] 显示和执行调用同一个 `<P>_plan_valid`；规模值用执行时的同一比例。
- [ ] 抽签只在预选时做；“不抽”也存；读档入口（bootstrap）不重抽。
- [ ] Pop 文化只和 `cu:键` 比较；共用 Pop trigger 不进 `pop_criteria` 才可用 `cu:`。
- [ ] 状态行覆盖：将转化（州、人数、方向）、未抽中（附几率）、无合格州、团结在中段、日志未就绪。
- [ ] 中英同键同函数，中文无“；”，英文英式拼写。
- [ ] 关闭结局和 on_action 都清预告。
- [ ] 加统一结束：两个结局（科技、制度），`possible` 与补加入口带 `nesnd_cohesion_open`；有补贴按钮的，所有结局都停补贴。
- [ ] 本地化里的阈值、几率与脚本一致。
