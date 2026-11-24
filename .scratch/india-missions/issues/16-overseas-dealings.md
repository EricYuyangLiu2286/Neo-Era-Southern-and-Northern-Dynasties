# 16 海外往来与流散（批次 17）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: agy  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/海外往来/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/海外往来/verify_overseas2.py)

## 现象与期望

旧「海外通商」此前已停用，需彻底删除其定义、「印度事务」种类 10–12 分支及孤立条约计时链；并按作者原意重做日志「海外往来」（`nesnd_india_overseas`），检测已获认可的独立印度帝国与周边五个战略区的外交、条约、关系与贸易往来，攒够数值与国库后直接签订 10 年投资权并在对方首都州留下主体文化社群（流散），攒满 100 可宣示利益，补全列强反应、一次性里程碑「印度洋商路」与失败结局「失去海外」。

## 改动

- 删旧：删除旧「海外通商」日志定义与中英本地化（含 `nesnd_india_core_l_*.yml` 中残留的 14 对旧键）、6 个旧按钮、事件 `nesnd_india_overseas.1`–`.3`、`nesnd_india_frontier.3`–`.4`、条约记录与清理链、`nesnd_india_matters` 种类 10–12 全部分支与 `nesnd_india_core.txt` 中的旧变量检查；保留仍在使用的 `nesnd_india_himalaya_country`。
- 新日志「海外往来」（`nesnd_india_overseas`，`foreign` 组）：由 `nesnd_india_overseas_upkeep` 按月发放给已获认可的独立印度帝国（`nesnd_india_overseas_holder` 去掉 `always = no`）；附喜马拉雅、印度尼西亚、东非、阿拉伯、大波斯五根 0–100 `default_green` 进度条（7 项月度读数，不设镜像变量，直接读条），以及 10 个按钮（五方向「签订投资权」与「宣示利益」）。
- 签订投资权与流散：往来 ≥ 50、国库 ≥ `nesnd_india_overseas_fir_cost`（`income × 13`，下限 £10,000）且有可签对象时弹出 `nesnd_india_overseas.1`（按关系由高到低列至多 3 国，灰显不可签项）；选定后往来 −50、付款、直接 `create_treaty` 签订 10 年 `foreign_investment_rights`（`source_country = 对方`，`target_country = 本国`），在对方首都州添加本国人口最多主体文化的文化社群（已有则跳过），发通知 `nesnd_india_overseas.2`。
- 宣示利益：往来满 100 时弹出 `nesnd_india_overseas.3`（按关系由低到高列至多 3 个持有未宣称州的国家），选定后清零往来、对对方在该区人口最多的未宣称州区域加宣称，发通知 `nesnd_india_overseas.4`。
- 列强反应与 AI：某方向往来首次到 50 时，向在该区（含附属国）持有州的他国大国/列强发 `nesnd_india_overseas.5`（5 年冷却），汇报至 `nesnd_india_overseas.6`；AI 按月检查，满足 2 倍签约价储备时签约，满 100 时每月 20% 宣示利益。
- 里程碑与结局：与 3 个不同方向国家持有生效投资权且三区利益等级 ≥ 2 时，触发一次性里程碑事件 `nesnd_india_overseas.7`「印度洋商路」（永久贸易修正 `nesnd_india_ocean_trade_modifier` + 各区 `add_involvement = 1000`）；沦为附属国或失去认可时触发失败结局「失去海外」（`nesnd_india_overseas_lost`，正统 −5 持续 5 年，已有条约与宣称留存）；不再是印度帝国时走隐藏 `invalid_outcome`。

## 待作者测试

数值均为默认值，实机测试后再调。交付记录「代码无法证实」一节列了 1.15 脚本与原版未见直接实例的写法（含 `add_cultural_community` 传动态作用域文化、`can_create_treaty` 是否内含 `can_ratify`、`has_strategic_region_interest_tier` 在进度条 `monthly_progress` 中求值等）。
