# 20 北方波斯东征应对与种姓读原版阶层（批次 16）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: agy  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/北方/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/北方/verify_north.py)

## 现象与期望

1. **北方（波斯东征与印度互见）**：此前波斯「近西战争重启」（`nesnd_per_east_journal`）可在印度七个州地区买下宣称，但印度一方缺少可见的应对日志与外交出口。本批新增日志 `nesnd_india_north`，受波及且首都在印度的国家（土邦或印度帝国）各有一份，支持边备整顿、向大秦共和邦或宗主交涉、波斯 50 进度的双向反馈，并以「东征被挡」或「东征得手」收场。`nesnd_per_*` 各文件只读不改。
2. **种姓（P6）**：此前「种姓与公职」（`nesnd_india_caste`）只查法律与全国识字率，未区分本国是否使用原版种姓阶层（`british_indian_caste_system`）。本批改读原版种姓阶层，增加最低阶层生活水平门槛、种姓法回退触发守旧反扑，以及对「谁代表国家」共同体条的导向。

## 改动

- **北方应对**（合入 `nesnd_india_princes` 组及 `common/scripted_progress_bars/nesnd_india_core.txt`，不新建文件组，`nesnd_per_*` 未改动）：
  - 出现：全局 `on_monthly_pulse` 挂载 `nesnd_india_north_global_pulse` → `nesnd_india_north_maintain`（不含 `root`）。波斯存活并持有 `nesnd_per_east_journal`，且对首都在印度（`nesnd_india_capital_in_india`）的国家所持印度州有宣称且不在 10 年冷却期内时，开出 `nesnd_india_north`（无 `possible`/`is_shown_when_inactive`，支持 10 年后重开），并将被宣称州地区记入 `nesnd_india_north_regions`（每月补记新宣称）。法兰西与大明联邦所持印度州不开此日志，交给原版外交。
  - 进度与按钮：单向条 `nesnd_india_north_bar`（0–100，起点 0；未与波斯交战且列表内州地区均由本国持有时每月 +0.5，纯靠月度 200 个月满）。三枚按钮：「整饬边备」（周收入 ×4、£2,000–£20,000，条 +10，人口最多的被宣称州获 5 年 `nesnd_india_north_garrison`，冷却 12 月）、「遣使大秦共和邦」（同价，大秦共和邦存活且未交战时可用，关系 +15，条 +10，冷却 12 月）、「请宗主国出面」（仅附属国可见，免费，宗主对波斯关系 −10 并生 `catalyst_event_negative`，条 +10，冷却 24 月）。AI 每月 5% 按上述先后执行。
  - 波斯可见：条首次达到 50 时触发波斯事件 `nesnd_india_north.1`（每份日志仅一次，root 为波斯），可选加紧图谋（`catalyst_event_negative`、关系 −10、AI 设 `conquer`，AI 权重 60，战时或正统 < 25 降为 20）或暂缓东进（关系 +10、对方条 +10）。
  - 结局与优先级：结局 1「东征得手」排在最前（同月优先于东征被挡）：列表内任一州地区落入波斯、其宗主或其附属国之手，失守州获波斯主体文化 `add_homeland`、本国得失守州 `add_claim`、10 年 `nesnd_india_north_lost`（正统 −5）、首都州激进 +10%、AI 对夺州方设 `conquer`、不动谋求独立或土邦联合日志，双方收 `nesnd_india_north.4`/`.5`，10 年后可再开；结局 2「东征被挡」：条满 100 且无州失守，得永久 `nesnd_india_north_held`（部队防御 +5%、威望 +5%）、各被宣称州 10 年 `nesnd_india_north_garrison` 与 5% 主体文化忠诚派、关系 −10、AI 波斯设 `antagonize`，双方收 `.2`/`.3`，10 年后波斯新买宣称可再开；结局 3 隐藏 `invalid_outcome`（波斯亡、既无剩余宣称也无失州、或首都离开印度）。
- **种姓与公职**（只改 `nesnd_india_core` 组）：
  - 新增触发器 `nesnd_india_caste_hierarchy_in_use`（`has_social_hierarchy = british_indian_caste_system`），与脚本值 `nesnd_india_caste_lower_pop` / `nesnd_india_caste_lower_sol`（读取 `shudras` 与 `dalit` 人口加权平均生活水平）。
  - `nesnd_india_caste_ready` 改为 `trigger_if` 两支：未用种姓阶层时保持原样；在用种姓阶层时在既有法律与教育门槛之外增加 `$shudras$` 与 `$dalit$` 人口平均生活水平 ≥ 10 的条件（带单句 `custom_tooltip`）。
  - 「守旧反扑」保留原信仰法被废触发（`nesnd_india_caste_law_held`），另立独立变量 `nesnd_india_caste_equality_law_held`，在曾用种姓阶层并持有不强制种姓或平权法后退回强制种姓法且宗教集团执政时亦触发。
  - 两个结局仍按 `strata = lower`（原版 `add_loyalists`/`add_radicals` 无 `social_class` 参数，且 `strata = lower` 即对应 `shudras` + `dalit`）增减 10% 忠诚/激进派，并各补「谁代表国家」共同体条（`nesnd_india_community_bar`）+10 / −10 导向（日志不在则跳过）。
  - `nesnd_india_caste` 新增 `status_desc`，仅在使用种姓阶层时显示 `$shudras$` 与 `$dalit$` 平均生活水平现值。

## 代码无法证实

数值均为默认值，实机测试后再调。交付记录「代码无法证实」一节列了：`has_social_class` 在 `every_scope_pop` 脚本值中无原版脚本调用实例（仅 `triggers.log` 与 `00_trigger_localization.txt` 有定义）、`add_homeland` 传动态文化作用域 `scope:india_north_per_culture`（原版均传字面量 `cu:...`）、`nesnd_india_north_defended_regions` 嵌套 `is_target_in_variable_list` 与重开判断、以及 1.15.2 结局字段在 Tiger 1.19.0 中的 4 条滞后提示。
