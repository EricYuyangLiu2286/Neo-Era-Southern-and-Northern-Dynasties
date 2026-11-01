# 集中实机验收

Record: implementation
Category: bug
Status: ready-for-agent
Execution: completed
Assignee: root
Blocked by: 03
Validation: ENGINE_PARTIAL
Evidence: [恢复后综合实机记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/resumed-runtime-20261101-root-observations.md>)；[新局基线](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Jan1-new-baseline/baseline-review.md>)
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

当前run20261101T014437Z使用冻结综合A（553文件，SHA 1f0c4f79024eb674d60b2d2cbc2b82e2e7fea56673a55caeb78eb2d421d4650d），真实新局首日基线与hair B肖像复核已完成。Feb3原生退让→GAME OVER→手动观察者继续→三日本政权恢复，Mar12合法ROOT下Lin完成/实际JAP君主/摄政探针为YES，政治页实显摄政王林汉涵。Mar12已另存并通过原生Load Game重载，政治页摄政政府/摄政王林汉涵保持，见[重载记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Mar12-native-Lin-regency/reload-observation.json>)；完整人物/关系审计、陈链与交通等仍待，保持ENGINE_PARTIAL。实际误点tag及无ROOT probe的QA错误详见Evidence，不能改写为纯默认玩家路线或全部通过。

以下为旧run来源记录：

run20261101T003815Z已在F2别名版真实新开USM，原生JAP让步确认后出现GAME OVER；手动作为观察者继续，自然回调观察到三国恢复。原档与关系/领土审计见Evidence及主控后续记录。Lin操作被CUA中断，不能标通过；海运、PHI等剩余覆盖仍欠。该结果不是两个未选用备选的验收。

## Comments

旧 C5 现金A正常到期/提前撤约、旧版陈案和 E1 港口实例化证据保留，不自动认证 F2。

## 2026-11-01 收口

依用户最新指令复用已有机制、地图/进港证据，停止重复开局/读档。日志优先修复及主MOD整合已完成；具体范围与未新跑引擎边界见WORK/reports/logfix-release-20261101/release-notes.md。旧未测组合不扩写为全部通过。

完成范围按2026-11-01用户修订的日志优先验收执行；ENGINE_PARTIAL保留实际历史覆盖边界，新按钮修复为STATIC_PASS。
