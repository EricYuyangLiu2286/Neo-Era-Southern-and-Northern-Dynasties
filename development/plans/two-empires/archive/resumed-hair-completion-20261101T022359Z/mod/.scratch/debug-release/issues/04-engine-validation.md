# 集中实机验收

Record: implementation
Category: bug
Status: ready-for-agent
Execution: claimed
Assignee: root
Blocked by: 03
Validation: ENGINE_PARTIAL
Evidence: [F2运行观察](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/runtime-003815-root-observations.md>)
Resume: 用户明确恢复；旧停止保留为历史证据，本轮重新启动隔离运行。新增女性发型同人前后对照、六地区地图和实际交通覆盖。

## Scope

按 [日本最小实机分支表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/japan-annex-recovery-batch-review.md>)、[Lin 回归表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/lin-defection-regression-a-review.md>)和 [游戏验证](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/validation.md>)进入精确冻结候选。

## Acceptance

- 日本：原生退让/战争胜利/事件吞并真实入口后恢复三国，第三国/占领/部分创建重试、人物同ID、自然时序及读档。玩家失国/GAME OVER已接受，不要求自动转国或保控；观察者继续采证须如实标明。
- Lin：实际选阵营与同ID转属、一次通知、失效及重入保护，继续核后续统辖三个日本属国（可任其中一国摄政）的原定链路与结果。
- 陈案：刺杀结果→内战进度跃升→战争的先后、触发条件及一次性；合理难度与失败结果不自动视作BUG。
- 海运：新局真实市场接入和舰队到达；节点实例化与缓存计数不得替代结果。
- PHI及既有机制：依受影响闭包复用旧证据，补必要改约/退出/存读档等未测分支。
- 原生日志、存档、运行 manifest、候选及依赖 SHA 均有绑定；仅主控操作游戏 UI。
- 失败返回源码最小修复再冻结；部分完成明确 ENGINE_PARTIAL，不升级为全 MOD 验收。

## Result

run20261101T003815Z已在F2别名版真实新开USM，原生JAP让步确认后出现GAME OVER；手动作为观察者继续，自然回调观察到三国恢复。原档与关系/领土审计见Evidence及主控后续记录。Lin操作被CUA中断，不能标通过；海运、PHI等剩余覆盖仍欠。该结果不是两个未选用备选的验收。

## Comments

旧 C5 现金A正常到期/提前撤约、旧版陈案和 E1 港口实例化证据保留，不自动认证 F2。
