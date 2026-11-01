# 当前交接：综合候选实机验证与后续开发

更新：2026-11-01；本次状态快照截至已记录的Mar12原生结算与新局发型观察。先读 [任务索引](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/map.md>)，实际后续步骤以 [主控运行记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/resumed-runtime-20261101-root-observations.md>) 为准。本次整理前全文及SHA保存在 [独立文档归档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/resumed-hair-completion-20261101T022359Z/manifest.json>)，更早交接链接保留在档内。

## 授权与工作顺序

用户明确恢复并要求休息期间不要提问。先完成原版参考核心步骤、中国女性发型、六地区地图细化和DEBUG，再推进完整CNE改革、明吴多结局、编辑器；海外市场退出降低优先级。合理实现选择自主处理。最终主MOD玩法合并仍保留具体清单审批，当前不发起问题；独立候选、证据、备份和Git保存继续。

保留原设计、现有疆域/人口基准与已验机制。玩家失国/GAME OVER、合理稀缺与破产可接受；不默认救援或保证不败。当前三条机制重点是吞并后恢复三个日本政权、Lin统辖三个日本属国（可任一国摄政）、陈东阳刺杀后内战进度跃升再触发战争。写功能/修复前完成SKILL“实现前先查原版完整链条”。

## 当前源与保存

- 主MOD仍是独立加载目录，当前只更新工程文档；玩法没有用候选覆盖。原始版本、当前主MOD、F1、F2及未选用备选的Git历史均保留。
- 当前综合候选 `WORK/exports/resumed-integrated-20261101-a`：553文件，SHA `1f0c4f79024eb674d60b2d2cbc2b82e2e7fea56673a55caeb78eb2d421d4650d`。冻结运行副本 `WORK/exports/runtime-20261101T014437Z/mod` 不改。
- 综合A以sequence A为共同父，整合Lin resume、hair B、六地区map和工程文档；来源见 [合并清单](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/resumed-integrated-20261101-a-merge.json>)。
- [Git保存报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/git-resumed-candidates-20261101T014406Z/report.json>)已核6条新candidate分支及Git archive逐字一致；综合分支 `candidate/resumed-integrated-a` 提交 `5edbdf6d671f023c9a4d39026152de8e6402b6bb`。工作副本 `WORK/projects/nesnd-repository`，main只维护当前主MOD内容及文档/support。最新refs细表在 [任务02](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/02-github-history.md>)。
- `f2-player-continuation-20261101-a`（5b8e9824…）和 `f2-japan-legacy-20261101-a`（0332f0dc…）仍UNSELECTED，存档分支和独立备份均保留，不集成。它们的静态结果和备选局限不构成当前交付门槛。

## 当前验收范围

[综合全局报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/resumed-integrated-20261101-a-global/report.md>)：13 PASS、1 FAIL、3 NOT_RUN。唯一FAIL为Tiger分类债；Foochow同形原版奖励、旧Russia空if有独立源码依据，旧报告保留，未知告警不自动清绿。历史/人口/生产/几何/交通/MCP通过限静态或协议层。

| 任务 | 当前结果 |
| --- | --- |
| 06 原版参考与女性发型 | completed / ENGINE_PASS，限本票复现范围：A同档牧沐子/女群像修复实测，hair B随综合A新局牧沐子肖像复核通过；不是全MOD或全部肖像认证 |
| 07 六地图细化 | claimed / ENGINE_PARTIAL：新局12受改州及全球国家地块、人口/建筑股份/首都/交通对象初始化已核；真实接入率、航行、战争与重载覆盖尚欠 |
| 03 DEBUG顺序收口 | claimed / ENGINE_PARTIAL：日本真实退让后恢复、Lin摄政已有原生观察；Lin原生重载后摄政显示已保持，完整人物/关系审计及陈链仍在验证 |
| 04 集中实机 | claimed / ENGINE_PARTIAL：当前run014437，所需分支尚未全部覆盖 |
| 08 原始欠账 | 仍待本批闭包，按原计划推进，不把当前局部结果写成整个MOD完成 |

06详细源链和证据见 [发型任务](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/06-source-first-female-hair.md>)。A前后run012826/013305读取同一原生首日档，牧沐子ID3124、身份/脸/衣服不变；B只补UTF-8 BOM。B于run014437全新局中重新打开完整肖像通过，[新局截图与记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Jan1-new-baseline/mu-muzi-newgame.json>)明确绑定综合候选SHA，无新增BOM告警。

## 实际运行断点与边界

游戏1.13.11/build24799966，EACR→综合A→QA E，run `20261101T014437Z`。恢复后旧CUA停止已属历史；每次恢复仍须枚举进程/窗口，不复用旧句柄。主控独占UI，文档代理没有启动或操作游戏。

全新USM Jan1原生档SHA `9b4de7f764cb5e1e28e77c5aea76337651dd69e24ffbb6390941d2c1819f9982`、seed1873443562，见 [基线审计](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Jan1-new-baseline/baseline-review.md>)。地图必须用这个新局验收；旧档只支持同人对照，不能认证新州。QE1缺lathe导致4纺织等级手缝是旧原生fallback，不能当拆州损失或随意改经济。

Feb3原生JAP退让→实际GAME OVER→手动选择内置观察者继续→世界恢复三政权；这条路径未直接调用恢复helper。实际走至Mar12后，合法国家ROOT下probe观察REALM_READY、LIN_COMPLETED、LIN_ACTUAL_JAP_RULER、LIN_REGENCY_ACTIVE为YES，政治页显示摄政王林汉涵。Mar12原生档已保存并经实际Load Game重载（档SHA 517f15165a5ed10e91422c83e40600e9c878126e77378949607bda8082bcaf45），政治页摄政政府/摄政王林汉涵保持，见[重载记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T014437Z/evidence/Mar12-native-Lin-regency/reload-observation.json>)；完整关系和领土审计继续取证；不得把截图与单次probe扩成全部分支通过。短暂误点瑞典tag、无国家observer probe产生的QA错误及原版Peru/Bolivia重复均如实保留。

下一具体入口：完成Mar12人物/关系审计，再从Jan1新基线分支验证陈链与真实交通；按影响闭包补PHI及现有机制。原始设计/欠账继续引用 [范围12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/12-scope-ledger.md>)和 [批次40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)，历史进度以精确版本和当前任务结果校正。统一检查不能替代实际事件、航行、经济和存读档；成功后按已验范围备份，最终玩法合并清单另行保留待审。
