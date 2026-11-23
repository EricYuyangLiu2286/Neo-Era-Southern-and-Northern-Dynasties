# 115 第二次靖难军心悬停崩溃

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: Victoria 3/crashes/victoria3_01261023_003501/{logs/error.log,exception.txt}

## 现象与原因

2026-11-23，1.15.2 观察者查看吴国「第二次靖难」时悬停军心，00:35:01 连报七组同样的错误。标签只传入 JournalEntry，规则键读取 `SCOPE.sCountry('nesnd_label_cne').GetName` 时收到 `_null_type_`，00:35:02 记录 EXCEPTION_ACCESS_VIOLATION。正式源开工部署号 `01b265dfb4428b157dad14cc19439a63`。运行文件中只有军心条面引用这个规则键。

## 改动（每行同时适用于中英）

| 键 | 原写法 | 新写法 |
|---|---|---|
| `nesnd_wu_resolve_bar_desc` | JournalEntry 标签打开军心规则 | 直接显示原名称及 `JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self) / 100`（整数） |
| `nesnd_wu_resolve_bar_rules_tt` | 内层用 SCOPE 读中华帝国国名 | 删除 |
| `nesnd_regional_native_release_state_tt` | `SCOPE.sCountry('nesnd_regional_release_host').GetCustom(…)` | 按钮所属国 `ROOT.GetCountry.GetCustom(…)` |
| `nesnd_regional_native_whole_state_name` | 在 GetCustom 选中的州名键里重读同一个 SCOPE | 沿用调用处的 `ROOT.GetCountry.MakeScope.Var('nesnd_regional_native_peace_seed').GetState.GetName` |
| `nesnd_jp_political_bar_desc` | JournalEntry 标签打开每月变化 | 直接显示原名称和读数 |
| `nesnd_jp_political_bar_monthly_tt` | 四项均用 `JournalEntry.GetCountry.MakeScope.ScriptValue` | 四项均用外层日志状态的 `ROOT.GetCountry.MakeScope.ScriptValue`，保留原文、变量和格式 |
| `nesnd_jp_unsettled_policy` | 仅原方针状态 | 末尾内联 `$nesnd_jp_political_bar_monthly_tt$` |
| `nesnd_jp_court_policy` | 仅原方针状态 | 末尾内联 `$nesnd_jp_political_bar_monthly_tt$` |
| `nesnd_jp_military_policy` | 仅原方针状态 | 末尾内联 `$nesnd_jp_political_bar_monthly_tt$` |
| `nesnd_jp_representative_policy` | 仅原方针状态 | 末尾内联 `$nesnd_jp_political_bar_monthly_tt$` |

军心规则留档：本轮战争未满 24 个月每月 −1，满 24 个月起每月 −1.5。敌方外国中，中华帝国计 2 点，其余每国 1 点，合计至多 4 点。反吴的南方各国和日本不计。每点每月 +1，外国参战头两个月每点每月另加 +7.5。原有月度分项与高、低军心修正继续由游戏显示。

## 全 MOD 排查

从中英运行本地化、GUI 和数据绑定追踪标签、Localize、SelectLocalization 和 GetCustom，展开内联键并核对本体目标。改前每种语言有 26 个不同的标签目标（改后 24 个）、251 个 GetCustom 目标、14 个 SelectLocalization 目标，无直接 Localize 调用。国家标签的内层没有 ROOT.GetCountry 或 MakeScope.ScriptValue。其余使用 ROOT.GetCountry 的自定义行均能追到 ROOT 调用处。日本四项原来由 JournalEntry 标签打开，按作者决定移到外层。

## 静态验证

技能提交 `7d9a4b8`。原 `tipctx,locsv` 都报 0。补强 `tipctx` 后在未改的正式源上命中军心规则和整州名称，中英各两项。修后全量 `tipctx`、`locsv` 均为 0，仅余原有 `anyeq` 65 项。关联脚本 `script_xcheck.py` 改前改后均只有两条 `progress_condition` 未识别提示，调用作用域无报错。逐键比较备份，中英各改 9 键、删同一规则键，原有语言间键差未变。

部署 `ae1f4d8787dcdd6b789e337b744f1f47`，1900 个运行文件 SHA-256 核对一致。工作台原始记录 `reports/deploy-logs/deploy-20261123-005319.txt`。

## 待实机（新开局）

1. 观察者与吴国玩家各悬停「第二次靖难」军心，确认不崩溃，能读到军心数值及当前月度分项。原来唯一显示中华帝国国名的计点规则已按作者决定删除，军心悬停没有国名显示项。
2. 「承认地方独立」选到整州时悬停条件，核对拟建国的州名。日本「新政推行」悬停条面，并在日志状态检查四项原文与读数，覆盖未选方针及三种已选方针。
