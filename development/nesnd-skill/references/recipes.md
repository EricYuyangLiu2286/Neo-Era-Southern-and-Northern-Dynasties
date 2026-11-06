# 函数库与具体实现路线

这里提供可定位、可复核的配方。完整引擎 effect/trigger/scope/modifier 清单必须由当前游戏 `script_docs` 导出，不能把本页当穷举 API。WORK/reports/source-catalog.json 是当前源码符号索引，`catalog.py find 名称` 返回文件、行号、类型及源哈希。

## 事件链与分支

先查 GAME `events` 中 `type = country_event` 和需要的 effect；本项目入口 `events/flavorUSM_ce.txt` 的 `flavorUSM.1`，由 `common/on_actions/ce_code_on_actions.txt` 的月脉冲调用。链上每个节点需登记：事件 ID、调用者、guard 变量、玩家选项、AI权重、下一事件/JE、退出清理。

真实项目形状：
```text
trigger_event = { id = flavorUSM.1 popup = yes }
set_global_variable = flavor_USM_crisis_ongoing_global
add_journal_entry = { type = ce_usm_conflicts_within }
```

不要给所有分支共享一个模糊布尔标志。国家变量记录各国进度，全局变量仅记录真正世界共享状态；`save_scope_as` 目标在延时期间可能死亡/被吞并，后续用可空 scope/exists 保护。月脉冲不能每月重复开同一事件。测试每个选项及灭国/换统治者/JE失效的边界。

## 带进度条的日志

定义 `common/scripted_progress_bars/ce_*.txt` → JE 用 `scripted_progress_bar = key` 引用 → `complete/fail/invalid` 收尾 → 按钮/事件只改变指定的 bar 或用于 bar 计算的变量 → 本地化所有名称、说明、变化原因。

真实参考：MOD `ce_poland_progress_bars.txt` 的 `ce_polish_reconquest_energy_bar`、`journal_entries/ce_europe_poland_issude.txt`、`scripted_buttons/ce_poland_scripted_buttons.txt`。另读原版 `00_je_progress_bars.txt` 及引用者验证 scope。原版文档规定 weekly/monthly/yearly 的进度更新先于对应 JE pulse；不要双重累计。

进度条的 `start_value/min_value/max_value`、`monthly_progress = { add = { desc = key value = 1 } }` 是定义；不能伪造 `progress_bar = { current = ... }`。使用 `change_journal_entry_progress` 等名称前必须从本机导出或当前用例确认其确切名称和参数，而非凭记忆。

## 历史归属、人口、建筑

```text
STATES = {
    s:STATE_GUANGDONG = {
        create_state = { country = c:USM owned_provinces = { xRRGGBB } }
        add_homeland = cu:han
    }
}
POPS = {
    s:STATE_GUANGDONG = {
        region_state:USM = {
            create_pop = { culture = han religion = confucian size = 10000 }
        }
    }
}
BUILDINGS = {
    s:STATE_GUANGDONG = {
        region_state:USM = {
            create_building = {
                building = "building_government_administration"
                add_ownership = { country = { country = "c:USM" levels = 1 } }
                reserves = 1
                activate_production_methods = { "pm_professional_bureaucrats" "pm_religious_bureaucrats" "pm_horizontal_drawer_cabinets" }
            }
        }
    }
}
```

以上演示当前形状，`xRRGGBB` 是必须换成真实 province 的占位符，不得直接输出。依据 GAME `history/buildings/11_east_asia.txt`，建筑 levels 常在 `add_ownership` 的 owner 内，不能只查 `create_building.level`。金融区/庄园 owner 可能在另一 state，要保留外国投资和跨地区引用的语义。

修改归属同时更新：state创建块、POPS/BUILDINGS 的 `region_state:TAG`、需转移的本地所有权 `country/region`、首都、编制HQ、国家历史及显式 `s:STATE.region_state:TAG` 引用。`history/population` 是财富/识字率，不是人口数量。国家财富设置影响目标国新增 state，需检查最终新开局表现。

## 新地区与地块迁移

不改 `provinces.png`、heightmap、terrain、rivers。挑选已存在 province；从旧 state_region 移除并加入新/目标地区，唯一数字 id，城市/农场/矿山/林业/港口 hub 必须在所属地区。沿海地区需要适当 naval_exit_id；内陆不能凭空新增港口。更新 strategic_region 的 `states`、history states、人口建筑、homeland、资源、traits、本地化与所有直接引用。新地区必须有有效城市等 hub，无法推断合理港口时阻止导出并明确指出。

默认二等分按每一人口行与每类建筑所有权逐项整数拆分，旧地区保留奇数余量，总量不增不减。人口的文化/宗教/类型与 PM 保持；对稀缺资源总潜力、耕地做守恒分配，不能复制一份使资源翻倍。traits 根据地理属性决定复制或独占，支持用户选择；全国唯一建筑、海军建筑、首都、跨区股权需显式检查。对 state_region 的事件条件可能应同时覆盖两个新地区，不能只机械替换字符串。

## 独特 DNA 人物

链条：`common/dna_data/ce_*.txt` 中唯一 DNA key → `common/character_templates/ce_*.txt` 中 `dna = ce_person_dna` → `common/history/characters/...` 的 `create_character = { template = ce_person }`，或已证实的事件生成调用。

先读 GAME `character_templates/00_default_template.txt`、`country_afg.txt`，配对 `dna_data/dna_data.md` 和实际 DNA 定义。独特外貌应从当前肖像编辑器导出的 `dna` 字符串或 `portrait_info.genes` 保存，逐项核查当前 `common/genes`，不能编造 DNA 字符串。脸部 DNA 与服装规则分离；创建后在游戏人物页检查姓名、年龄、角色、外貌、服装和读档后保持一致。

## 需求可行性

外交援助、供货和预算相关任务还须读[原生条约、供给和援助](native-treaty-aid.md)。1.13.11有实际`goods_transfer`和`money_transfer`；`trade_privilege`无固定数量保证，不等于引擎不支持商品转移。`binding_period`不是自动到期日。

每个 idea 输出短实现说明：可用的机制、证据路径、实际可交互结果、引擎不支持之处及最接近方案。优先组合已有 JE/变量/事件/按钮/UI，而不是承诺新增引擎层。新版本未知字段必须等安装后查证。不要将“AI想支持某法”实现成直接 `activate_law`，也不要将“完整广东”实现成跟随原版国界的机械迁移。


## 1.13.11 已核实的说明差异

关系数值的保存scope参数用`"relations(scope:target_country)" >= relations_threshold:cordial`，精确实例在GAME `events/diplomatic_events.txt:49`、`common/diplomatic_catalysts/01_event_catalysts.txt:24`。简单`relations:root`不能机械拼成`relations:scope:xxx`；后者在2026-10-31 run143454真实引擎报Unknown trigger type三次，而Tiger未报。须用当前实际参数语法并再冷启动。

`common/scripted_buttons/scripted_buttons.md` 仍示范 `ai_chance = { base = ... }`，但当前 `07_meiji_buttons.txt:87`、`:211`、`:295` 使用 script-value 形状 `ai_chance = { value = 10 if = { limit = { ... } add = 5 } }`。新按钮依据后者；事件 option 的 `ai_chance` 仍是 base/modifier 形状，不能混用。2026-10-31 Tiger 检出前者 unknown token，当前源码复核后改正；真实按钮执行另行验收。

海军历史编制在 `create_military_formation` 内使用 `ship`（`ship_type:`），陆军使用 `combat_unit`。统计兵力不能只遍历 combat_unit 而把海军漏报为零；预设单位数不等于实际招募完成数、舰艇维护能力或可投送兵力。

2026-10-31 CNE改革复核：本机导出的 `effects.log` 在 `create_diplomatic_play` 说明中写 `handle_annexation_as_civil_war`，实际 `GAME/common/history/diplomatic_plays/00_carlist_war.txt:9`、`common/on_actions/00_code_on_actions.txt:5220` 使用 `annex_as_civil_war = yes`；Tiger也将前者指出为文档错名。新脚本以实际源码后者为候选，并单独真实触发博弈验证，不能把文档列出视为引擎已经接受。

改革指标的scope须明确：`standard_of_living`、`workforce`、`is_in_mild_starvation`、`is_in_severe_starvation`在pop；`state_unemployment_rate`、`state_population`在state；机构、金库、全国收入在country。月度script_value可用`every_scope_state`→`every_scope_pop`聚合，但劳动力加权家庭SoL、州人口加权失业率都是有说明的指标，不能冒充全国UI统计。实现例子与未测边界见 `WORK/plans/two-empires/evidence/cne-reform-engine-matrix.md`；当前只静态核验，需由真实缓存/存档和UI对照补上engine状态。

## Country 标签的嵌套动态悬停（run143454 实际失败）

日志状态的外层可用 `#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],my_stats_link 统计#!#!`。`my_stats_link` 内层仅获得 Country 对象，动态国家变量应写 `[Country.MakeScope.Var('my_value').GetValue|%1]`，不得继续写 ROOT.GetCountry；不得为省事改为 GetPlayer。当前原版 `content_204_l_english.yml:787—788` 和 `agitators_4_l_english.yml:1473/1478` 有完整调用对，`companies_l_english.yml:25—26` 也展示 GetTooltipTag→Country 的绑定。只在这种对象绑定层切换根，事件和JE正文既有 ROOT 不能全局替换。日志轮转与读法见 verification.md。

## 事件AI权重依据

本机1.13.11原版events根目录实际149个ai_chance.modifier全部使用add，其中146个显式trigger块（如events/1848.txt:45起）。本项目新事件用 `ai_chance = { base = 50 modifier = { add = 50 trigger = { 条件 } } }`；把权重按实际国家条件逐支计算，不把按钮script_value的`if/limit/value`语法与事件modifier混为一类。不要依据别的P社游戏假定factor行为；当前未单独证明factor不支持，选择已证实原版用法并实测。亲善/敌对条件互斥时，50的×2/×0意图可分别写+50/−50。

条约预检`can_create_treaty`的商品字段是`good`，创建`create_treaty`是`goods`。见native-treaty-aid.md中run150709实证；比较语义而非要求两棵AST逐字段同名。

新增沿海地区还必须补独立harbor锚点和到海域的type3海路；只有port locator/naval_exit不足。2026-10-31三新港真实cpp128错误与当前编码/导出实现见[地区尺度与经济：原生海港断链](map-economy-design.md)。不得把静态港口定位通过当作海运可用。
