# 74 打开「教士秀全的旅途」时崩溃

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [崩溃包与原版对照检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-xq-je-crash-192604/>)

## 现象与期望
作者打开日志即崩溃。打开、悬停及点击秀全画像都应可用，保留原版人物详情。

## 原因
19:17:18 原生 GUI 工厂在读取 nesnd_xiuquan.gui:23 时拒绝 GetGlobalVariable('nesnd_xq_char').AccessCharacter，诊断为 requires non const promote。19:24:52 打开日志时 Character.IsValid、边框和 GetAnimatedPortrait 都取不到人物；19:24:53 记录 C0000005、地址 0x0。无符号堆栈无法指出最后一条游戏指令。
上次仅核对了 Scope.AccessCharacter 的方法名。实际运行版本为 1.15.0，原版 ep2_japan_widgets.gui:506、520 把变量列表绑定到 fixedgridbox，列表项提供 Scope；同文件第 13–35 行才用 Scope.GetCharacter.IsValid 及 Scope.AccessCharacter 绑定大名头像。原版 00_sgui_effects.txt:99–101 将人物加入该列表。

## 改了什么
- gui/journal_entry_widgets/nesnd_xiuquan.gui:18–48 改用列表项的 Scope，空列表不会实例化人物画像，原有三种边框、悬停和点击控件保留。
- common/journal_entries/nesnd_xiuquan.txt:23 在日志激活时准备人物。全局日志没有固定所属国，因此把列表存在日志实例上。
- common/scripted_effects/nesnd_xiuquan.txt:27、40 在秀全存在且列表尚未设置时写入一个人物，沿用既有同步以补齐早已激活的实例。游戏外核对原报错链、列表写入和读取、原版控件层级，三个文件通过解析。未使用 Tiger，未启动游戏。

- 已把数据源到头像、悬停的可变性检查和崩溃包定位方法写入 [NESND 技能](../../../development/nesnd-skill/references/compatibility.md#日志人物像与悬停)，本地提交 60fd50f。

## 怎么复测
重新启动客户端加载修正后的 GUI。新局可暂停后直接打开；已有存档若日志早已开启，先过一次周同步再核头像。打开日志、悬停 5–10 秒、点击头像进入人物面板，关闭后再打开。检查本轮起始及操作时段的日志，关注 Invalid promote、缺失 Character、GetAnimatedPortrait 和先前的行军提示。

## 遗留问题
实机是否完全消除打开或悬停时的故障，待作者复测。
