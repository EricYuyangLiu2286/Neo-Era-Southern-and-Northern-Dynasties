# 13 登莱日志逻辑与触发器复查

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-11）
Blocked by: none
Validation: STATIC_PASS
Evidence: 改动前备份 `nesnd-workbench/backups/pre-change-sha-logic-review-20261111T104847Z`；检查脚本 `nesnd-workbench/tools/sha_logic_check/sha_check.py`

## 1. 现象与期望

作者：GPT 写的登莱日志常有逻辑错误和触发器错用，用脚本和人工逻辑过一遍。

## 2. 怎么查的

- 脚本：读 1.15 的 `docs/triggers.log`、`effects.log`、`event_targets.log`、`modifiers.log`，对 65 个 `nesnd_sha_*` 文件逐键检查。项目：触发器与效果是否存在、是否用错上下文（`if` 写进条件、触发器写进效果）；按作用域链接推算所在作用域，核对支持的作用域；从内容推断脚本化触发器/效果的作用域，再核对调用处；变量是否有读有写；修正、事件、按钮、进度条、本地化键是否有定义；修正类型是否存在。先用故意写错的样例验证脚本能报出这些错。
- 结果：机械层面没有错用。剩下 8 条都是误报（`$参数$`、比较里内联数值块、事件选项的 `base`）。
- 对照 2026-11-11 01:49 那次实测的 error.log。
- 人工逐个读 7 个日志及其触发器、效果、按钮、事件、on_action、外交行动、战争目标：雪国共和、远北、黄金同盟、复燕之路、渡海、齐鲁之约、海外落脚点与垦殖、君主主义阴谋。核对 on_action 的根作用域（原版 `00_code_on_actions.txt` 注释）。

## 3. 改了什么

1. `journal_entries/nesnd_sha_far_north.txt`：「远北」「黄金同盟」的超时结局补 `header`、`effect_header`（引擎报错：非隐藏结局必须有标题）。
2. `journal_entries/nesnd_sha_restore_yan.txt`：「十二年未起事」结局补 `color`（引擎报错）。
3. `scripted_buttons/nesnd_sha_far_north.txt`「勘金」：`order_by = "state_region.remaining_undepleted(building_gold_field)"` 引擎读不了（报 CBuildingDatabase 找不到），排序失效。`remaining_undepleted` 只有触发器形式，改为新数值 `nesnd_sha_gold_left`（`script_values/nesnd_sha_far_north.txt`，按 1–8 分档计数，远北金矿储量最大为 8）。
4. `scripted_progress_bars/nesnd_sha_overseas.txt`「船期」：日志未开始或已结束时也会读 `nesnd_sha_misses`，变量不存在会刷错误。加存在检查。
5. `diplomatic_actions/nesnd_sha_overseas.txt`「租借口岸」：`ordered_scope_state` 用的是 `max = 1`，按文档是取序号区间，对方若有两个合格州会割出两处口岸、只付一次钱。改为原版通用的 `position = 0`。
6. `on_actions/nesnd_sha_far_north.txt`：辽东人分离战争若在登莱援助之前就已开始，起事国不会被记录；即使它赢得独立，脚本也会按“被镇压”处理并让登莱撤手。分离结束时补记起事国。

## 4. 没改、需实测或作者决定

- 01:49 日志里的 “already has a journal entry”：雪国共和由国家历史文件加入、远北/黄金同盟由事件加入，同时日志自身的 `possible` 也会自动激活，属重复添加的警告，不影响结果。
- `nesnd_sha_yan_two_states` 标志“设置但从未使用”：只比较另一种分地方案，这是默认分支，属无害警告。
- 延迟的 `trigger_event = { on_action = … days/months = N }`：原版只用不带延迟的写法。日志没有报错，但延迟是否生效需实测（远北援助分期、选举、海岸援助分期、复燕整编回调都用到）。
- 乙约下登莱在外东北只有通商口岸，「定都海参崴」仍会出现，迁都目标是口岸州。设计上“拥有海参崴所在州即可用”，引擎是否允许口岸作首都需实测。
- 「渡海」中若选择与共和派山东结盟，信号停发，日志只能等到十五年超时。设计稿写的是“结盟不进兵”，按设计保留。

## 5. 怎么复测

- 读档后看 error.log 不再出现上面 1–3 条的报错。
- 黄金同盟：按「勘金」，看是否选中余量最多的州。
- 垦殖：日志开始前和结束后，error.log 不刷 `nesnd_sha_misses`。
- 远北：先让伊尔库茨克辽东人起事，再按「接济」，起事成功后应得到 `nesnd_sha_north.1` 而不是撤手事件。
