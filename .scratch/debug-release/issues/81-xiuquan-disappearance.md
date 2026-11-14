# 81 教士秀全失联与旅途结案

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [存档、选人排查与逐文件说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/test-evidence/xiuquan-20261108-194046-562/核查与复测.md>)

## 现象与期望

latest_test 中，日志显示秀全在陇右，传教 90/100，人物已无法找到。传教士应随州移动，失联与死亡都应触发原结局。

## 原因

- 1840.1.1 本人在淮国桂北。6.10 淮国及 HNA 灭亡；同日人物库将 3115 等 59 人列入清理队列。7.1 秀全仍有记录，所属国 USM，历史人物、已退休；1 月的淮国 28 人均已退休。10.23 人物库已无 3115，日志与头像仍指向 3115，死亡标志未设。
- 控制台历史有相邻的 ANNEX HNA、ANNEX GNG，与退场过程吻合，命令无逐条时间。靖难的 usm_civilwar.4 也可对淮国成人随机执行流放／处决，未见它命中秀全的记录。
- 旧日志只检查 nesnd_xq_dead，旧的周同步还会按州强制转籍。original-20261030 中只有人名，旅途是任务 69 新增。

## 改了什么

- common/history/global/nesnd_xiuquan.txt 创建时施加原版剧情忙碌与不死标记。模板已有 historical = yes，运行档也保留了它。
- common/scripted_triggers/nesnd_xiuquan.txt 校验原人物、职务、所属国名单和州，给原版常规事件筛选加上旅途人物排除。
- common/scripted_triggers/nesnd_story_character_protection.txt 复用同一人物身份条件。
- events/usm_civilwar_events.txt 的五个随机惩处分支排除本人；实际吞并所在国前让仍在职的本人随州交接。fascism_events.9 沿用原版候选池。按作者复核意见，撤回本任务在 events/fascism_events.txt 的两行过滤，整文件与任务 81 前的副本逐字节一致；此前 .1 的剧情人物保护仍在。
- common/scripted_effects/nesnd_xiuquan.txt 取消每周强制转籍，保存抵达国，共用一次性追认通知。common/on_actions/nesnd_xiuquan.txt 处理死亡与实际州易主。
- common/journal_entries/nesnd_xiuquan.txt 扩展唯一的 hidden invalid_outcome，停止失效脉冲、清除修正并解除保护；1894 年 1 月按期解除保护并死亡。common/scripted_buttons/nesnd_xiuquan.txt 在失联后关闭驱逐操作。

## 怎么复测

- 读 latest_test，放行至下次日志结算。应收到一次「追认圣徒」，旅途消失，陇右失去「秀全的药箱」。
- 新局高凉（USM）打开头像，确认身份为客家天主教传教士。跨境后同一人随州改变所属国。
- 另存后用 `effect global_var:nesnd_xq_char = { set_character_busy_and_immortal = no kill_character = yes }` 测死亡；或在另一份档用 `effect remove_global_variable = nesnd_xq_char` 单测失联。

## 遗留问题

传教士角色禁止任命为 IG 领袖。被 .9 点名后若任命失败且仍在当地任职，旅途继续；实际失联才进入原结局。换为乡村民众也可能被点名，保留知识分子。兼容清单见[技能参考](../../../development/nesnd-skill/references/vanilla-overrides.md)，两份技能已同步，技能提交 2e69acc。只做游戏外验证。控制台直接吞并时，引擎是否在州易主回调之前把他退休须实机复测；若先退休，走原结局。开局剧情保护也抑制提前自然死亡。Toolkit 的唯一提示误用 CK3 的目录规则。
