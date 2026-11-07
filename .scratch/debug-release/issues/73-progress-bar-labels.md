# 73 进度条条面文字溢出

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [原版与 MOD 逐条读数表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-progress-labels/labels.txt>) · [Toolkit](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-progress-labels/toolkit-checks.json>)

## 现象与期望
秀全的传教条显示满条改宗说明，单行超出条框。作者要求条面只留“传教：读数/100”，规则移到状态行，并把字段规范写进技能。

## 原因
1.15.0 原版 gui/journal_entry.gui:428–534 的默认条宽高为 504×30，自定义图形条为 430×30。顶层 desc 直接交给 autoresize 的单行文本框；部分样式另画右侧 second_desc，没有独立的 name 文本框。悬停明细由 GetPeriodicProgressBreakdown 单独读取。
任务 36 发现右侧标签溢出；任务 59 把日本国政明细移回悬停；任务 65 修过波斯改宗说明，随后把该路线的通知放到事件。已有参考文件提示过右侧标签，玩家写作技能仍合写“进度条与提示”且要求“规则进提示和进度条”，未约束主标签上的整句说明。
原版共 61 条：60 条顶层 desc 直接引用键；古巴一条按条件选择“加入美国／加入美利坚联盟国”。14 条另有右标签。去格式、把每个动态表达式记作一个占位符后，原版简中左标签为 1–17 个字符。例如读数 12 时为“剩余月数：12”，读数 2 时为“已完成的议程：2/3”。数字位数与动态国名影响实机宽度。
主 MOD 的 86 条均核对简中与英文；未定义右标签，未覆盖原版条面文案键。朝鲜的上月变化、西秦的两端刻度属于数值标签，日本条上的链接目标在悬停层。其余条面没有同类整句机制说明。

## 改了什么
- 接手时秀全的中英文条面已缩短、改宗比例已移至共用位置状态。补回原说明的“进度归零”，核对驱逐、改宗记录与默认位置七个状态分支均可显示一次完整规则。改动限两种语言的 nesnd_xiuquan 本地化。
- 技术技能明确顶层与周期 desc 分属条面和悬停；写作技能分开条面、条件和效果提示。安装版与 development/ 下四个对应文件逐字节一致。技能本地 Git 提交 542ea8e。

## 怎么复测
重新加载 MOD，暂停打开「教士秀全的旅途」。条内应只显示“传教：0/100”（已有进度时数字相应变化）；所在州的状态行应说明满 100 后当地 0.1% 人口改宗、进度归零。悬停条面仍显示周期来源。

## 遗留问题
八十六条中英字段通过静态审阅；原截图来自修改前，当前客户端实际显示由作者复测。无玩法脚本或 GUI 改动。
