Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-14）
Blocked by: none
Validation: STATIC_PASS
Evidence: 日志副本与 Toolkit 报告 `nesnd-workbench/reports/2026-11-14-civic-routes-war-error/`（logs/ 对应部署 `39ab2dda`，toolkit/）

# 102 公民工程日志：`war` 无效对象与市场接入提示报错

## 1. 现象与期望

新开局运行中，error.log 在 21:36 起反复出现两类报错：`Event target link 'war' returned an invalid object`（`nesnd_civic_project_security.txt:5`，经 `journal_entries/nesnd_civic_routes.txt:119` → `scripted_triggers/nesnd_civic_routes.txt:153`），以及 `TRIGGER_MARKET_ACCESS_GREATER_OR_EQUAL_THIRD` 拿不到 State 上下文。画面无异常。期望：日志条件正常检查不报错；国家不在战争中时按“无战争”处理。

## 2. 原因

- `common/scripted_triggers/nesnd_civic_project_security.txt:5`（2026-11-06 d478e8f 加入，不在 `original-20261030`）：`any_diplomatic_play = { is_war = yes … exists = war war = { is_war_participant = … } }`。实际判定时前面的条件不成立就不往下算；但生成说明时引擎逐行求值，对没有战争的外交博弈（或没有博弈时）也打开 `war = { }`，于是报错。报错时机是 `nesnd_c2_hus_citizenship` 完成结局（119 行）的说明生成，与第二类报错同一轮。
- 第二类是原版本地化缺陷：`triggers_l_*.yml` 中 `TRIGGER_MARKET_ACCESS_*_THIRD` 写 `[State.GetName]`，引擎不提供该数据对象；其他同类键（`TRIGGER_STATE_POPULATION_THIRD` 等）写 `[STATE.GetName]`，正常。原版脚本只在遍历或州自身作用域里用 `market_access`，走不到 `_THIRD`；本 MOD 用 `var:… = { market_access >= 0.8 }` 从国家切到州，才暴露它。

## 3. 改了什么

- `common/scripted_triggers/nesnd_civic_project_security.txt`：整段战区检查放进 `trigger_if = { limit = { is_at_war = yes } … }`；`war = { }` 放进 `trigger_if = { limit = { exists = war } … } trigger_else = { always = no }`。不在战争中的国家不可能是战争参与方，判定结果不变；平时说明里不再显示“战区无战争”这一行。
- 第二类未改（原版问题，按要求只说明）。

## 4. 怎么复测

读档或新开局均可（只改条件，不改状态）。打开胡斯公民权日志（或任一公民工程日志），在已选目标、计划进行中时悬停完成条件，看 error.log 不再出现 `'war' returned an invalid object`。`TRIGGER_MARKET_ACCESS_GREATER_OR_EQUAL_THIRD` 仍会出现。

## 5. 遗留问题

- 同一触发器的其他调用（意大利两项、胡斯边疆/石油、联合州四项、胡斯道路）走的是同一段，一并修好；道路日志外层已有 custom_tooltip，原本就不报。
- 市场接入提示报错：如要消掉，可在 MOD 里把 `var:… = { market_access >= 0.8 }` 包进 custom_tooltip（`nesnd_civic_routes.txt` 43/56/124/156/185/215/226/257/295/303/406 行、`nesnd_hus_road_projects.txt:2`），需作者决定。
