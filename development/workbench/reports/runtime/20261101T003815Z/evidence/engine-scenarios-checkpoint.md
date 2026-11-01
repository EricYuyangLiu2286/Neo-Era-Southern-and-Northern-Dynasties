# 引擎场景审计断点

ROOT 已报告 CUA 在尝试 Lin 夹具点击时返回停止信号；用户是否按键未确认。本子任务从未操作UI，也没有关闭或终止游戏。

最后经 ROOT 直接确认的状态：已重新加载自然Jan1档、切换YN1（远南）成功、玩家YN1、暂停。后续 Lin 夹具点击结果为 **NOT_OBSERVED**。不称 Lin 选项或人物迁移已经执行/成功，也不凭工具中断证明它绝对未执行。

已完成证据：

- `Jan1-native-baseline/`：F2新局初始化、玩家/Lin/日本原始对象、67港口层实例化。
- `Jan27-DP-before-backdown/`：实际JAP玩家、真实DP5及主/镜像目标10/11、typed登记ctry17、吞并前人物与领土。
- `Feb9-native-backdown-result/`：真实原生退让后、ROOT手动继续观察者所得的三国保护关系与96省色分配；原JAP退休人物及dead旧owner的Jan27/Feb1/Feb9时序。玩家即时Game Over独立记为实际观察；自动续玩未通过。
- `stages/qa-readonly-getter-audit/`：一次manual readonly日期getter附近的GameStateAccess断言及原始日志；归因高度支持但仍待无getterA/B。

未安装的下一冷启 QA：`WORK/qa-fixtures/f2-concentrated-20261101-c/qa-overlay`，同目录上一层有 `manifest.json` 和 `README.md`。C包含所有旧按钮，继承B两处新F2日期getter删除，增加typed日本人物捕获/存活与owner谓词、player-ack真实战争JE夹具和legacy原选项→JE测试入口。没有安装到mutable QA或运行冻结，也未实机执行。

恢复时 ROOT 必须先枚举进程/窗口并确认真实日期、国家、暂停状态。现有run可能仍活，不能重复launch；不要沿用旧window/exec句柄。该停止信号不改变源代码或验证结论。
