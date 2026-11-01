# 当前交接：DEBUG 收口与 GitHub 保存

更新：2026-11-01。旧交接已原样归档到 [完整历史](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/engineering-entry-20261101T002933Z/references/active-work.md>)，[归档 manifest](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/engineering-entry-20261101T002933Z/manifest.json>)保存原始 SHA。旧运行 ID、窗口号及历史“当前”标题仅为证据，不作为现时进程状态。

## 当前授权与入口

用户已要求保存最初版本和最新成果到 [私有 GitHub 仓库](https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties)，并依次完成文档/技能整理、独立 F2 最小修复、集中实机验收、交付清单。**最终合入主 MOD 前仍须用户批准具体清单。**
本轮仍为 DEBUG ONLY：保留原设计与数据；不扩剧情、不新增拆州、不调经济数值。当前任务状态与结果统一到 [执行索引](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/map.md>)，工程方法适配见 [项目说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/docs/agents/engineering-skills.md>)。

详细设计与验收欠账继续读取 [原始范围12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/12-scope-ledger.md>)、[批次计划40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)、[发布阻断历史总表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/debug-status-and-release-blockers-20261031.md>)。这些旧表部分状态落后于 F1；优先核精确候选及新任务结果，保留原文作为历史。

## 已核快照与候选

- 主 MOD：318文件，SHA `bf6558a3d20d475988e5487f59aab6d08205c4a8f7091280ba7313ff44e787b6`，本轮编辑前备份 `WORK/backups/pre-change-github-f2-entry-20261101T002814Z/mod`。本轮文档编辑后指纹会变化，此值只是起点。
- 冻结 F1：`WORK/exports/batch-debug-20261031-f1`，514文件，SHA `3b379906c62a4611513bcf9110ecce429a84c22b48562b920b86f2307f3ebcdb`；独立备份 `candidate-batch-debug-f1-20261101T000328Z/mod`，不覆盖。
- F1 已合 E1 海域、Japan A1（含 Lin）、功能本地化和字面 scope 修复；[合并记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/batch-debug-20261031-f1-merge.json>)为来源。计划40中 Lin“待合本批”、日本“待完成闭包”是旧状态。
- 本轮 F2 目标 `WORK/exports/batch-debug-20261101-f2`；实际生成、冻结与验证结果在 [F2任务](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/03-f2-minimal-debug.md>)更新。
- GitHub 保存由 [版本任务](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/02-github-history.md>)记录远端与提交结果。官方设备授权及首次推送已成功；原始288文件、当前主MOD318文件和F1的独立提交/标签均已保存并核对远端refs。Git工作副本为 `WORK/projects/nesnd-repository`；文档更新与F2后续保存仍在进行。

## 尚需收口

[F1统一报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/f1-global-20261101-final/report.md>)：12 PASS、2 FAIL、3 NOT_RUN，F1未绑定实际运行证据。源码版本1.13.11/build24799966、固定人口±25%、历史顺序、资源/生产、海域/交通结构、实际MCP通过均限各自检查范围。

1. 内容闭包唯一 hard error 是原版简中 `great_game_complete_tt` 的 `concept_geogregions` 拼写；现有本体概念为 `concept_georegion(s)`。F2用独立兼容入口处理，不改本体。
2. Tiger 的 annex 枚举/target_region、3处缩进提示需按现有源码证据完成分类。原版俄罗斯空if改值会影响全球AI；26处人物裸ig仍兼容性待证，不因清告警批量改。
3. `known_semantic_review` 的旧FAIL记录源见证已变，当前状态是NOT_RUN。逐项复核后记录具体新SHA与结论，不能继承旧FAIL或自动升级PASS。
4. 优先实测日本吞并/恢复/占领重试/玩家失国、Lin、海运，再按受影响闭包覆盖PHI与既有机制。失败玩家续玩、旧日本其它失败/退出选择仍有缺口；日本吞并本身允许。

PHI现金A正常到期/提前撤约只在C5已测；陈案购买/撤卫/到期/指定负伤及部分姓名/界面来自更早精确版本。E1 Jan1已证明67港口连接实例化，未证明实际接入率或舰队抵达。全部证据继续保留原版本身份。
完整CNE改革、明吴其它结局/转国、海外市场退出和编辑器等原始欠账仍在范围12；本轮收口不等于整个MOD交付完成。

## 恢复运行

2026-11-01本轮已实际启动run `20261101T003815Z`，冻结源为F2玩家续玩修复前526文件，指纹 `416ac54f8fb9f4c4ab1c86266519b517724f9f78a9a396e4579342774fb9353f`。运行器exec47407；实际是否仍运行须重新枚举。主菜单已真实观察、冷启动日志已归档，正在新局；[实时操作记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/runtime-003815-root-observations.md>)记录后续实际步骤。另有独立玩家确认修复候选由代理准备，未覆盖本运行冻结副本。

先枚举当前进程/窗口，核真实加载组合；不得沿用旧exec或窗口号。编辑候选、冻结运行副本和存档分别记录，主控独占UI。
统一入口与证据要求见 [validation README](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/README.md>)及 [游戏验证](validation.md)。F2实际通过后保存独立版本，汇总精确差异并请求最终合入批准。
