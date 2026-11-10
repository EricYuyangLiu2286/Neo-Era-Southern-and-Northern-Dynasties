# 50 日志国名、条件与地区文字

Record: implementation
Category: bug
Status: ready-for-agent
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [交付报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-06-journal-labels/delivery.md>)

## 现象与期望
先修「独立的代价」「国计在民生」，再检索并修复同类日志：按钮取国家现用名；条件消除重复并汇总紧急状况与外交冷却；通用文字符合真实地区适用范围。本次不启动游戏。

## 原因
`$TAG$`取默认国名。`small_can_request`和嵌套`small_request_eligible`两次调用外交准备；canon与印度/外援两套等待检查使用相同提示。临时scope赋值与临时政权变量直接外露。印度六地案件被所有小国显示。

## 改了什么
9个日志文件绑定/刷新国家命名scope；8个按钮文件使用动态标签并隐藏内部scope准备；7个trigger文件去重、汇总与限制印度案件显示；18个中英本地化文件修改190键。合计42文件、83按钮、13日志。完整清单、条件表、逐键对照见交付报告。保留作者其余改稿。
使用`[SCOPE.sCountry('nesnd_label_usm').GetName]`等原版支持的saved-scope文本函数；不依赖执行后才有的请求scope。
保序解析、命名绑定、逐键代码/数字/颜色/BOM检查通过；修改前后发函与答复的布尔条件对照通过。Tiger本任务新增诊断为0；未开游戏。

## 怎么复测
以重启后的新开局验收。埃及六投资国；暹罗、远南的投资/自治/和平独立/市场/防御；印度有实际案件地区的国家；抽检PRU、AUS、USA、意大利、日本与共同市场使节。检查改名、紧急/冷却红色摘要、无重复/原始键、接收方仍能答复。旧档日志不重跑初始化，跨月绑定待实测，不保证读档即生效。

## 遗留问题
未实测UI红绿、月度命名scope刷新与旧档。并行任务49的8个源码文件与Tiger旧接口诊断未修改；本任务编号由49改为50以免冲突。详情见交付报告范围外清单。
