# 1.15.0 英俄大博弈关闭方案

本方案先于 MOD 写入。研究与实施由父任务委派给 gpt-6-astra / high，本机版本1.15.0、Steam build 26453692。游戏源码、其他MOD和存档均只读。

## 来源与耦合

`GAME/common/history/global/00_global.txt:6–15` 在拥有Sphere of Influence或State and Revolution时显式添加两个无国家上下文的JE，分别为高加索战争和 `je_great_game_control`。`MOD/common/history/global/ce_global.txt:565` 设置的是俄国成就初始资格。它没有启动大博弈。当前 `common/objectives` 只有教程以及经济霸权、霸主、平等社会三种正式目标，没有独立的大博弈开局目标。所谓大博弈“目标”实际是十个从属JE。`GAME/common/journal_entries/journal_entries.md:48–66,134–163` 明确区分显式添加、显示触发与 `hidden invalid_outcome`。只在 `possible` 写否不能可靠拦住显式添加。

主JE在 `00_player_objectives_great_game.txt:2`。它给英俄各设100初分，保存两国作用域，给参与国建计数器，配置地图和交互组件，按周刷新读数、按月计算被动分。真正的欧洲结算按分数、国力集团与列强等级发 `gg_core.1/.2/.3`。胜负会发威望修正、外交催化和 `achievement_great_game_no_re`。本土胜利分支发 `gg_core.4`、英俄失败通知和衰减修正。`complete_great_game_effect` 会随机写入高加索、哈萨克、阿富汗、波斯、朝鲜等地结局和铁路/边界旗标，只有原版debug事件调用，不能用作迁移清理。

`03_russia.txt` 中大博弈分数只是东部边境、高加索战争、安抚草原、最后的哈萨克汗、中亚征服等路线结算的附带效果。它们自有局势结果、事件与边界等变量，`je_great_reformer` 及三项大改革、`08_russia_provisional_government.txt` 没有以英俄总局胜败作为启动条件。`03_afghanistan.txt` 的独立政治过程另有地方胜负记录。西藏考察的加分支路已有参与资格。全GAME/common及events交叉搜索没有发现政治改革或临时政府读取 `modifier_great_game_defeated`、`modifier_great_game_victor` 或 `gg_core.2` 写出的俄方失败旗标。该失败事件实际只给修正、特定情形下清理读数并生成外交催化。因此不新增俄方败北或英国获胜记录。

十个从属目标分别为俄国在华让步/朝鲜保护国、英国干预俄属高加索/太平洋势力/巩固英属印度、帕米尔考察、阿富汗保护国、波斯影响力、波斯整合和地区主权。每个 `is_shown_when_inactive` 均以参与总JE为条件，每个都有失去参与资格后的原生隐藏失效和自己的清理效果。MOD对华让步地理修正仍保有这组门槛。英国/印度/波斯/阿富汗/区域小国的其他JE、AI、条约、成就和地区建设继续按各自来源处理。

## 最小实施边界

1. 新增一个JE覆盖文件，仅替换 `je_great_game_control`。保留有效ID、原组、图标、DLC和无上下文类型。明确拒绝所有参与者和旁观者显示，使用 `possible = { always = no }` 加一个恒真的原生 `hidden invalid_outcome`。显式历史创建至多产生短暂隐藏兼容实例。该实例不初始化分数、分配参与者、运行周期效果、触发结局、改变领土或外交关系。旧档已活动实例也在下一次引擎结局检查走同一失效路径。
2. 失效时仅以国家作用域清理两个大博弈专属计数器，以原版 `clear_great_game_variables` 清理六个临时全局计分值。原有地区胜负、边界、铁路、真实结局奖励及既已显示的历史事件继续保留。正在进行的原生从属JE沿现成失效路径退出；已满足其自身真实历史结局的目标由原版按正常顺序处理。没有世界历史整文件覆盖或每日/每月扫描器。
3. 原版七个 `great_game_{britain,russia}_progress_*` 接口都在可选JE跳转之外先发计分文字。只关闭总JE仍会让俄罗斯独立路线显示不存在比赛的加分。用第二个窄文件保留七个公共接口并将其改为无副作用的兼容效果。原版接口内只有大博弈提示、条进度和临时读数更新。独立路线其余结算、俄罗斯新内容及邻国的实际事件全部保留。
4. 游戏外从实际有序AST检查唯一启动入口、十个子目标、七种适配器的原始动作、失效/清理集合、俄罗斯新内容的独立作用、原MOD覆盖层和新/旧实例的状态。记录来源SHA与实际差异。不启动游戏，不提交Git。

## 实施与验证

已按上述计划新增两份脚本。历史总表、国家历史、真实战争、地区结局、既有NESND波斯内容与原版俄国新内容均保留原调用。当前1.15另有明确的沙皇政治资本联动。`08_tsarpoints.txt`未读取本轮撤下的总JE和计分接口。东境事件`russo_chinese.3`真实发放中量政治资本，哈萨克事件`kazakhstan_events.3`发放少量，`russian_central_asia.2`发放中量，分别由`has_journal_entry = je_tsarpoints_master`守卫。五个边境JE中的原生地区结果、事件和政治资本预览均在计分接口之外。部分成就 eligibility 或条约AI得分恰以“Great Game”命名，但依赖的是俄国实际拥有中亚州或阿富汗统一JE，故继续保留。`achievement_great_game_no_re`依赖真正参与/结算本竞赛，本补丁不补发。

`verify_great_game.py`完成91项离线检查，检索3538个本机原版common/events脚本。检查解析实际新旧有序AST，执行新开局显式添加后的失效处理、旧局比赛全量/部分暂存状态、已结案历史四类夹具，再调用七种兼容计分效果。地区与改革记录保留，模拟的计分残留清零。源文件SHA、全部交叉引用、十个子目标各自的失效清理和逐项结果见`great-game-validation.json`。冻结SHA与起始路径不存在的记录见`great-game-freeze.json`，两文件内容在`great-game-freeze/`。原版或MOD其他文件均未改动；未开游戏，未提交Git。

旧档的父JE在下一次引擎结局评估失效。已经排队的原生胜负弹窗、已授予的历史修正及此前真实发生的区域事件保留。若旧子目标同时满足其自身真实胜利和失效条件，选择顺序依原版引擎。本轮没有保存文件改写或强制回溯。
