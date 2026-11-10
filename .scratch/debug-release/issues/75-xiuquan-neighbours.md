# 75 秀全日志参与国与驱逐

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [日志、开局陆界与回归检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-xiuquan-neighbours/>)

## 现象与期望
高凉开局只列大明联邦，驱逐按钮呈灰色。作者要求所在地所属国的邻国加入日志并修正驱逐。沿用仅所在国可驱逐、成功前往与该国陆地接壤的外国州。

## 原因
1. 原先 should_be_involved 只认所在国，周同步还会移除其他国家；邻国只在 should_show_when_not_involved 中可见。
2. 19:37:09，按钮第 6 行在无效国家上下文调用所在国判定。驱逐还通过按钮 root 排除本国州，未显式要求外国州有主，也未用陆界触发器核对目的州。成功标志在随机目的州迭代器外，空选也能写入。该日志没有逐次随机结果。

## 改了什么
- common/journal_entries/nesnd_xiuquan.txt 与 common/scripted_triggers/nesnd_xiuquan.txt：激活时纳入所在国及所有邻国，非参与玩家仍可查看。所在地国由全局州的当前所有者确定。
- common/scripted_effects/nesnd_xiuquan.txt：周同步、月度移动后按同一条件增删参与国；驱逐成功后立即刷新。
- common/scripted_buttons/nesnd_xiuquan.txt：先验证按钮查询国，再检查驱逐权限。可用条件和成功效果共用「有外国所有者、与所在国陆地接壤」的州筛选，抵达后才标记成功。保留 50/50、一个月冷却及失败时的当地激进效果。

- 作者复测确认驱逐已生效，但 USM 在印度的领土也提供边界。现给共用目的州条件增加 is_in_geographic_region = geographic_region_china，并同步中英文按钮提示。原版 00_reunify_china.txt 与 MOD 00_default_strategy.txt 使用该地域判定；MOD 定义取南中国、北中国。按开局历史与省份图的陆界，USM 的 35 个外国边境州中有 8 个位于该区域。[候选清单](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-xiuquan-expel-china/candidates.json>)。

## 怎么复测
新局选 USM，在高凉打开日志；名单应同时有 USM 与接壤国（如 CNE）。非所在国能参与但不能驱逐。已有日志过一次周同步再验名单。在有陆界、按钮冷却已完时点击，成功应显示中国地理区内新的外国州，所在国及邻国名单随之刷新；失败应留在原州。没有合格外国州时按钮应不可用。

## 遗留问题
四文件通过保序解析、范围检查及 Toolkit。使用开局领土历史与省份图交叉核实 USM 与 CNE 的陆界；该证据不含海峡专用连接或运行中领土变动。按钮实际点击、随机结果及名单 UI 待作者复测。
