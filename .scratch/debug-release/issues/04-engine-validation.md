# 集中实机验收

Record: implementation
Category: bug
Status: ready-for-agent
Execution: open
Assignee: none
Blocked by: 03
Validation: NOT_RUN
Evidence: pending

## Scope

按 [日本最小实机分支表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/japan-annex-recovery-batch-review.md>)、[Lin 回归表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/lin-defection-regression-a-review.md>)和 [游戏验证](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/validation.md>)进入精确冻结候选。

## Acceptance

- 日本：原生退让/战争胜利/事件吞并真实入口，三国恢复、第三国/占领/部分创建重试、人物同ID与失国玩家续玩、自然时序及读档。
- Lin：实际选阵营与转属、一次通知、死人/外国owner/君主储君/失效与重入保护。
- 海运：新局真实市场接入和舰队到达；节点实例化与缓存计数不得替代结果。
- PHI及既有机制：依受影响闭包复用旧证据，补必要改约/退出/存读档等未测分支。
- 原生日志、存档、运行 manifest、候选及依赖 SHA 均有绑定；仅主控操作游戏 UI。
- 失败返回源码最小修复再冻结；部分完成明确 ENGINE_PARTIAL，不升级为全 MOD 验收。

## Result

尚无本轮 F2 引擎运行证据。

## Comments

旧 C5 现金A正常到期/提前撤约、旧版陈案和 E1 港口实例化证据保留，不自动认证 F2。
