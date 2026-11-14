# 57 普鲁士共同防卫条件的 country_c_equal 报错

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [日志副本与改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-country-c-equal-tooltip/>)

## 现象与期望
error.log 反复出现 `country_c_equal: Scope dependent values in localization inside an any trigger; consider using a custom_tooltip; at common/scripted_triggers/nesnd_europe_america.txt:12`。期望：报错消失，判断结果不变，提示不变或更清楚。

## 原因
`nesnd_prussian_coalition_ready`（scripted_triggers/nesnd_europe_america.txt:7）里的 `any_country` 含两处随被遍历国家而变的国家比较：`NOT = { this = scope:nesnd_prussian_actor }` 和 `nesnd_canon_german_partner` 里的 `NOT = { c:FRM ?= this }`。引擎为 any 内部生成逐项说明时无法把 `this` 写成文字，每生成一次就报一次。
会生成说明的调用处：日志“德意志的共同防卫”的完成条件（journal_entries/nesnd_europe_america.txt:36），以及两个日志完成效果里 `if limit` 的说明（scripted_effects/nesnd_europe_america.txt:2、18）。status_desc 的 triggered_desc（同日志文件:91）和月度 on_action 只做判断，不生成说明。日志在界面上显示时说明按帧重建，所以同一运行里报了上万次：最新 error.log 936 条，error.1–5 各 2416 条，01:37:38–42 五秒内把 error.log 轮转了五次。

## 改了什么
- common/scripted_triggers/nesnd_europe_america.txt:12–18：用 `custom_tooltip = { text = nesnd_prussian_coalition_partners_tt … }` 包住整个 `any_country`，内部条件一字未改。
- localization/simp_chinese/replace/nesnd_europe_america_l_simp_chinese.yml:5、localization/english/replace/nesnd_europe_america_l_english.yml:5：新键 `nesnd_prussian_coalition_partners_tt`。
  - 中：至少三个独立的德意志邦国与本国结盟或订有防御协约（莱茵邦联和法国的盟国不计）
  - 英：At least three independent German states have an alliance or defensive pact with us (excluding the Rhenish Confederation and allies of France)
最新 error.log 里没有其他“Scope dependent values in localization inside an any trigger”报错。

## 怎么复测
新开局玩普鲁士（PRU），打开日志“德意志的共同防卫”，看完成条件：原来的逐项嵌套列表变成上面一句，满足时变绿。运行一段时间后在 error.log 搜 `nesnd_europe_america.txt:12`，应为 0 条。完成后进入“莱茵秩序的争夺”，悬停完成效果也可能看到这句。

## 遗留问题
- 文中“莱茵邦联”沿用同文件 `nesnd_prussian_rhine_resolved_tt` 的称呼；FRM 不在法国宗主下时游戏内国名是“法兰克福”，两处称呼可能不一致，未改。
- 最新 error.log 其余报错（存档中其他 MOD 的游戏规则键 `Failed to read key reference`、`MISSING_DLC_ENTRY`）不指向本 MOD 文件，未处理。
- 这次刷屏把同一运行较早的 error.log 轮转覆盖掉了，本次之前的报错无法从这组日志找回。
