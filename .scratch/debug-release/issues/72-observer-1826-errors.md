# 72 观察者局 error.log（18:26–18:35）

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [逐项核对及地图省份清单](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-observer-1826/核对说明.md>)

## 现象与期望
作者指定最新观察者局前 2,289 行的六组问题。修直接源于 MOD 的报错，保留玩法；地图只定位，复测由作者执行。

## 原因
- 秀全的州引用可以进入，但 owner 在四次周同步时无效；相邻检查直接传入这个国家，累计 155 次错误。
- 外交政策与波斯西线同时允许 JE 自动激活及脚本直接添加；波斯的显式添加原本已有实例守卫。
- 古纳雅拉由一个省建国，共用征兵效果却要求最多两个州。引擎已按候选数截取。
- 人物提示取编队时 constness 不符；原版州事件调用国家条件；原版北秘鲁事件遍历参与国时包含自己。其中后两处未见 MOD 引入差异。19:05 的头像悬停复测定位到 MOD 给原版人物提示传入只读 Character。

## 改了什么
- common/journal_entries/nesnd_xiuquan.txt:16、common/scripted_triggers/nesnd_xiuquan.txt:3 检查有效所属国；common/scripted_effects/nesnd_xiuquan.txt:16、41、54 从当前有效 owner 转籍和更新参与国。
- common/journal_entries/nesnd_external_journal.txt:8 和 common/journal_entries/nesnd_per_campaign.txt:55 关闭这两项的自动激活。events/nesnd_external_events.txt:12、common/decisions/nesnd_external_decisions.txt:7 在显式添加前检查；波斯沿用原有守卫。
- common/scripted_effects/nesnd_a2_common.txt:53 使用引擎的按实际候选长度截取选项。

- 19:05 复测补修 gui/journal_entry_widgets/nesnd_xiuquan.gui:23、30、37。此版后来在打开日志时崩溃，直接串接全局变量的绑定已由[任务74](74-xiuquan-je-crash.md)取代。原版日本日志的头像和人物提示使用同一接口。[日志快照及 Toolkit 诊断](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-xiuquan-hover-190625/>)。

## 怎么复测
1836 新开观察者五速约 10–15 分钟，至少到 1841 年初。检查周同步、换州与邻国可见性；五国表态和波斯援助路线后同类日志只出现一份；复国征兵按余量选州。对应 MOD 栈应消失，分支未触发时待验。另重载 MOD 后暂停，悬停秀全头像 5–10 秒，移开再悬停；增量日志中应无该本地化键及 GetMilitaryFormation.GetName 失败，再点头像验证人物页。本次 GUI 解析与 Toolkit 通过，未启动游戏。

## 遗留问题
地图只记录。玻利维亚正常港在安托法加斯塔，1838 年初被智利完全占领；卡派巴斯克港正常，总部在相邻两档间消失。古纳雅拉的唯一建国省 xBB820B 临海，巴拿马港 x8A8A20 在国界之外。其余原版两项、失效编队断言、18:39 后键读取失败及未报错的波斯东线双入口见证据。
