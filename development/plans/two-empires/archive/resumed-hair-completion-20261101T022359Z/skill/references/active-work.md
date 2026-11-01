# 当前交接：DEBUG 收口与 GitHub 保存

更新：2026-11-01。旧交接已原样归档到 [完整历史](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/engineering-entry-20261101T002933Z/references/active-work.md>)，[归档 manifest](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/engineering-entry-20261101T002933Z/manifest.json>)保存原始 SHA。旧运行 ID、窗口号及历史“当前”标题仅为证据，不作为现时进程状态。

## 当前授权与入口

用户已要求保存最初版本和最新成果到 [私有 GitHub 仓库](https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties)，并依次完成文档/技能整理、独立 F2 最小修复、集中实机验收、交付清单。**最终合入主 MOD 前仍须用户批准具体清单。**
最新任务已扩展：先完成原版参考核心步骤、女性发型、指定六地区地图细化及既有 DEBUG，再实施完整 CNE 改革、明吴多结局、编辑器；海外市场退出为低优先级，仅保障基本开局运行和合理难度。保留原设计、人口基准与已有数据。用户已休息且明确不提问，当前自主推进已授权工作，不发起批准问题。当前任务状态与结果统一到 [执行索引](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/map.md>)，工程方法适配见 [项目说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/docs/agents/engineering-skills.md>)。

**最新用户纠正优先：接受包括日本在内的玩家失国/GAME OVER，不再以保控续玩作为发布门槛。** 当前只用F2别名修复版继续查源码和机制顺序，不集成玩家确认或日本旧终局备选。调试重点是吞并→恢复三个日本政权；林汉涵后续统辖三个日本属国（可任其中一国摄政）；陈东阳刺杀→内战进度跃升→战争。依原定目标核顺序、可达性、难度与玩家行动空间，减少设计追问，不自动加救援或新剧情。修订前说明完整保存在[范围归档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/accepted-failure-20261101T010339Z/manifest.json>)。

详细设计与验收欠账继续读取 [原始范围12](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/12-scope-ledger.md>)、[批次计划40](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)、[发布阻断历史总表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/debug-status-and-release-blockers-20261031.md>)。这些旧表部分状态落后于 F1；优先核精确候选及新任务结果，保留原文作为历史。

## 已核快照与候选

- 主 MOD：318文件，SHA `bf6558a3d20d475988e5487f59aab6d08205c4a8f7091280ba7313ff44e787b6`，本轮编辑前备份 `WORK/backups/pre-change-github-f2-entry-20261101T002814Z/mod`。本轮文档编辑后指纹会变化，此值只是起点。
- 冻结 F1：`WORK/exports/batch-debug-20261031-f1`，514文件，SHA `3b379906c62a4611513bcf9110ecce429a84c22b48562b920b86f2307f3ebcdb`；独立备份 `candidate-batch-debug-f1-20261101T000328Z/mod`，不覆盖。
- F1 已合 E1 海域、Japan A1（含 Lin）、功能本地化和字面 scope 修复；[合并记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/batch-debug-20261031-f1-merge.json>)为来源。计划40中 Lin“待合本批”、日本“待完成闭包”是旧状态。
- 当前运行基底F2为 `WORK/exports/batch-debug-20261101-f2`，526文件，SHA `416ac54f8fb9f4c4ab1c86266519b517724f9f78a9a396e4579342774fb9353f`。后续编辑在独立 `WORK/exports/f2-sequence-debug-20261101-a`：保留已赚危机进度的JE初始化守卫、用户允许的Lin日本摄政链路；本体/F1/本运行冻结不改。实际生成、冻结与验证结果在 [F2任务](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/03-f2-minimal-debug.md>)更新。
- 未选用备选保持原样：`f2-player-continuation-20261101-a`，SHA `5b8e98246e52f4d8cb160257e18aa9a4f4e8896e8be7473d618ea0ee9632fd5e`，备份 `candidate-f2-player-continuation-a-final-20261101T004755Z/mod`；`f2-japan-legacy-20261101-a`，SHA `0332f0dcc72f290b7873f2ae61d222c8f215e5e4f428d56db6a97d7e69213018`，备份 `candidate-f2-japan-legacy-a-20261101T005454Z/mod`。这些是保留的静态候选，不是accepted或待自动合并。玩家主动离开后的selection锁中断边界仍是备选局限；日本备选没有完成第二次独立审查。
- GitHub 保存由 [版本任务](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/02-github-history.md>)记录远端与提交结果。官方设备授权及首次推送已成功；原始288文件、当前主MOD318文件和F1的独立提交/标签均已保存并核对远端refs。Git工作副本为 `WORK/projects/nesnd-repository`；文档更新与F2后续保存仍在进行。

## 尚需收口

[F1统一报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/runs/f1-global-20261101-final/report.md>)：12 PASS、2 FAIL、3 NOT_RUN，F1未绑定实际运行证据。源码版本1.13.11/build24799966、固定人口±25%、历史顺序、资源/生产、海域/交通结构、实际MCP通过均限各自检查范围。

1. 内容闭包唯一 hard error 是原版简中 `great_game_complete_tt` 的 `concept_geogregions` 拼写；现有本体概念为 `concept_georegion(s)`。F2用独立兼容入口处理，不改本体。
2. Tiger 的 annex 枚举/target_region、3处缩进提示需按现有源码证据完成分类。原版俄罗斯空if改值会影响全球AI；26处人物裸ig仍兼容性待证，不因清告警批量改。
3. F2最初统一报告为13 PASS、2 FAIL、2 NOT_RUN。`known_semantic_review`中的玩家续玩FAIL依据已被用户最新范围撤回，应保留旧报告并更新当前分类，不伪造当时PASS；其余项仍逐一核来源SHA与实际机制证据。
4. 优先核日本吞并后恢复、Lin后续统辖、陈案触发内战三条链，再覆盖海运、PHI与实际受影响机制。日本吞并和玩家GAME OVER本身允许；不因旧事件无调用就擅自接回叙事。

PHI现金A正常到期/提前撤约只在C5已测；陈案购买/撤卫/到期/指定负伤及部分姓名/界面来自更早精确版本。E1 Jan1已证明67港口连接实例化，未证明实际接入率或舰队抵达。全部证据继续保留原版本身份。
完整CNE改革、明吴其它结局/转国、海外市场退出和编辑器等原始欠账仍在范围12；本轮收口不等于整个MOD交付完成。

## 恢复运行

2026-11-01本轮实际运行run `20261101T003815Z`，冻结源为上述F2别名版526文件。原生Jan27 JAP玩家让步后实际GAME OVER，主控点击内置“作为观察者继续”；Jan29自然回调与Feb9原生档证明JAP/JTK/JIM存活及真实保护关系，96省色分配、第三国未变，见[Feb9审计](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T003815Z/evidence/Feb9-native-backdown-result/review.md>)与[原始人物时间线](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T003815Z/evidence/Feb9-native-backdown-result/original-character-timeline.json>)。旧JAP人物retired/仍记owner17不等于已死，实际is_character_alive探针尚欠。GAME OVER是已接受结果，不改写成自动续玩。

随后准备Lin夹具时CUA返回“physical Escape”停止信号；本轮已停止所有ComputerUse，不归因用户实际按键。Lin结果为NOT_OBSERVED，最后已知状态为Jan1暂停YN1；没有因此启动第二局或改变生产候选。[实时操作记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/runtime-003815-root-observations.md>)和[GAME OVER界面证据](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261101T003815Z/stages/native-backdown-gameover/capture.json>)保留原始步骤。后续源码分析可继续，UI恢复须按工具边界与最新用户授权处理，不能沿用旧exec或窗口ID。

先枚举当前进程/窗口，核真实加载组合；不得沿用旧exec或窗口号。编辑候选、冻结运行副本和存档分别记录，主控独占UI。
统一入口与证据要求见 [validation README](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/README.md>)及 [游戏验证](validation.md)。F2实际通过后保存独立版本并汇总精确合并清单；用户休息期间不提出问题，继续独立候选和欠账工作。

## 2026-11-01断点恢复

用户明确 resume；旧“本轮停止 ComputerUse”描述属于上一回合，不再作为本次操作禁令。新运行先枚举真实进程/窗口，不能沿用旧ID。共同父候选 sequence A 为532文件，SHA `3325ec418bf25fceef54cda480444e1ca739c0836c40c97af051c841bc7b1b5a`；Lin补齐、发型、地图分别独立派生，再三方合并。本次范围变更前全文与SHA见 [resumed-expanded-scope-20261101T012820Z](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/archive/resumed-expanded-scope-20261101T012820Z/manifest.json>)。
