# 03 权力平衡的整数支持度、权威力与行政力

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [游戏外证据](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-court-approval>)

## 现象与期望

基础支持度 ±1 乘以 0.46，提示出现绿色 +0 或红色 −0。作者最终指定两端支持度分别为 ±3，国家权威力与行政力反向变化，最大各 10%。

## 原因

原版 1.15.1 的 common/modifier_type_definitions/00_modifier_types.txt:793、905 将支持度显示精度设为 0。旧宫廷和共和日志都直接把连续系数乘到支持度上。游戏脚本不能证明旧引擎结算是否保留不足一点的尾数。

## 改了什么

- common/script_values/nesnd_power.txt:51 计算有当权者与相应对手时的偏离值，第 60 行按离中点距离分三档。均势为零，其余为 1、2、3 点。
- common/journal_entries/nesnd_power.txt:39、122 两日志按集团分别挂整数修正。双方同集团时相抵，兼领时其余各集团站另一侧。
- common/static_modifiers/nesnd_power.txt:116 国家权威力与行政力反向增减，按整个百分点显示与结算。
- common/scripted_effects/nesnd_power.txt 与 common/scripted_effects/nesnd_cne_confidence.txt:122 移除旧小数缓存的计算和调用，北朝让步仍移动平衡点并同步进度条。
- 中英文 replace/nesnd_power_l_*.yml 新增两条国家修正名。工作台 gen_power.py 和 loc_power.py 同步。

## 怎么复测

重启并读原存档，走到下一周刷新。分别看偏向两侧和回到 50。日志的有利和不利提示与各集团支持度来源应同号、同值。顶部权威力、行政力来源中应各有一项，方向相反。无需重开；尚未实机复测。

## 遗留问题

两日志的原有权势、税收浪费按连续比例缩放，在非常靠近各自起算点时仍可能把小值显示成 0。没有调整。项目全量静态扫描的 75 条遍历比较提示未指向本次改动。Toolkit 检查 7 个文件零诊断，脚本数值检查覆盖 96 组。
