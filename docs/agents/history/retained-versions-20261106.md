# 保留版本清单（2026-11-06）

与[开发总结](development-summary-20261106.md)配套。逐项核查实际目录、manifest、Git引用及远端；不是依据旧交接推断文件还在。用途部分依据目录名和附近报告归类，未逐个运行旧版本。

`W = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。表中路径相对W。旧备份的manifest版本指制作时的游戏安装，未必是里面脚本已适配的版本；manifest verified也不是本轮重算，更不是引擎验收。完整SHA、数量、元数据和调查说明见`W/reports/development-summary-20261106/retained-versions-20261106.json`。

## 1. 正式工作对象

- **主MOD M**：`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`。盘点1093文件。当前应从这里继续，不能改旧备份后误以为已交付。
- **源码Git G**：`W/projects/nesnd-repository`。仅一个本地分支main、一个worktree；最新玩法提交`67c876e`。Git中额外有README和development证据。
- **作者待同步改稿**：M的`localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml`与G不同。本次只记录，未覆盖或上传。
- **其他MOD**：同级`Neo-Era Hanfu`是独立项目，不是NESND旧版，当前任务只读。

## 2. backups内每一份保留材料

共22个目录；其中有完整源码快照，也有局部文件和重建材料。没有把candidate、checkpoint或pre-change登记成accepted。

| 相对目录 | 状态／manifest项数 | 内容与用途 |
| --- | --- | --- |
| `backups/candidate-audited-japan-1891-20261105T094403Z` | candidate／1021 | 1891长局审计后的日本候选，1021文件。候选身份不是引擎验收。 |
| `backups/candidate-native-japan-localization-20261105T045024Z` | candidate／1020 | 任务37原住民、日本及文本整合候选，尚不以文件名证明完整实测。 |
| `backups/checkpoint-hus-player-flow-final-20261106T201131Z` | checkpoint／1093 | 任务44最终玩法检查点。发布前3个JE又做了纯缩进规范，AST相同；不能声称与67c876e逐字一致。 |
| `backups/checkpoint-prose-icons-final-20261106T041413Z` | checkpoint／1091 | 任务43文案、图标和可见结局检查点，对应02b66fe交付范围。 |
| `backups/checkpoint-task37-stageA-static-20261105T024437Z` | checkpoint／1009 | 任务37 Stage A静态候选检查点，不是A/B/C最终整合。 |
| `backups/pre-change-diaspora39-20261105T095657Z` | pre-change／1021 | 任务39流散修改前；manifest整体SHA与audited-japan-1891候选相同。 |
| `backups/pre-change-diaspora39-first-errors` | partial capture; no manifest／无完整manifest | 流散首次报错时的局部源码，不是完整MOD。 |
| `backups/pre-change-maintenance-pre-cleanup-20261104T213001Z` | pre-change／1015 | 任务35清理前基线，保留当时作者改动和旧文件布局。 |
| `backups/pre-change-migration115-20261105T135256Z` | pre-change／1031 | 1.15迁移前源码。manifest记录已安装1.15，不能据此称该备份已完成迁移。 |
| `backups/pre-change-prose-icons-outcomes-20261106T025436Z` | pre-change／1081 | 任务43大批修改前。包含最先完成的War提示修复，更早War原件另存该批报告。 |
| `backups/pre-change-runtime-followup-20261105-20261105T000605Z` | pre-change／1004 | 任务36运行反馈修复前完整副本。 |
| `backups/pre-change-save-audit-1891-20261105T080440Z` | pre-change／1020 | 1891长局审计前源码，供定位当时运行版本。 |
| `backups/pre-change-stageA-player-text-20261105T022134Z` | partial capture; no manifest／无完整manifest | Stage A玩家文本改前子集。 |
| `backups/pre-change-stageB-final-text-20261105T040305Z` | partial capture; no manifest／无完整manifest | Stage B最终文本改前子集。 |
| `backups/pre-change-stageB-player-text-20261105T034028Z` | partial capture; no manifest／无完整manifest | Stage B玩家文本改前子集。 |
| `backups/pre-change-startup-loc115-20261105T174041Z` | partial capture; no manifest／无完整manifest | 1.15启动/本地化修复前子集。 |
| `backups/pre-change-task37-punctuation-20261105T014544Z` | partial capture; no manifest／无完整manifest | 任务37标点改前文本和范围记录。 |
| `backups/pre-change-task37-stageB-scripts-20261105` | partial capture; no manifest／无完整manifest | 任务37 Stage B地区脚本改前子集。 |
| `backups/pre-change-task37-stageC-20261105T031031Z` | partial capture; no manifest／无完整manifest | 任务37 Stage C日本文化脚本改前子集。 |
| `backups/pre-change-task38-japan-20261105T082134Z` | partial capture; no manifest／无完整manifest | 任务38日本改前子集。 |
| `backups/pre-update-20261030T233944Z` | legacy status unspecified／288 | 作者原始快照，旧式manifest列288项；对应Git original-20261030，不代表1.15可直接运行。 |
| `backups/reconstructed-task37-stageA-parent-20261105` | partial capture; no manifest／无完整manifest | 重建的8文件Stage A父版本材料，不是原始完整包。 |

## 3. exports及嵌套源码副本

- `exports/maintenance-current`：1004文件的旧维护导出，metadata为0.1.0、支持版本为空。是旧源码材料，非当前主版。
- `exports/task37-punctuation-text-freeze-20261105T014544Z`：26文件（主要为25份文本及清单），状态TEXT_SUBSET_FROZEN_STATIC_PASS。不能作为完整MOD加载。

下面18份带MOD元数据的嵌套材料也仍在；它们不是正式分支。尤其故意损坏的反例和已经撤回的采购方案不能重新部署。

| 相对目录 | 文件数 | 性质与用途 |
| --- | --- | --- |
| `map-projects/spline-authoring-20261031T035657Z/mod` | 327 | 地图/spline编写工程的地理试验包。保留编辑用途，不是主MOD版本。 |
| `reports/canon-route-execution-20261104/batch-c-validation-repair2-20261104T131440Z/native-empty-mod` | 1 | 仅metadata的空MOD对照，不含玩法。 |
| `reports/integrity-recheck-20261102/cwtools-negative-full` | 664 | 故意构造缺定义错误的完整规模测试输入，不能发布。 |
| `reports/japan-development-20261102/withdrawn-procurement-20261102/candidate-before-withdrawal` | 738 | 已撤回的日本采购/库存/预付款方案候选。作者否决，禁止自行恢复。 |
| `reports/population-envelope-boundary-20261031/minus25` | 334 | 人口±25%边界测试输入。名称区分合法边界、超一人、缺理由或滚动改基准，不是游戏版本。 |
| `reports/population-envelope-boundary-20261031/minus25_one_person_over` | 334 | 人口±25%边界测试输入。名称区分合法边界、超一人、缺理由或滚动改基准，不是游戏版本。 |
| `reports/population-envelope-boundary-20261031/plus25` | 334 | 人口±25%边界测试输入。名称区分合法边界、超一人、缺理由或滚动改基准，不是游戏版本。 |
| `reports/population-envelope-boundary-20261031/plus25_one_person_over` | 334 | 人口±25%边界测试输入。名称区分合法边界、超一人、缺理由或滚动改基准，不是游戏版本。 |
| `reports/population-envelope-boundary-20261031/plus25_without_reason` | 334 | 人口±25%边界测试输入。名称区分合法边界、超一人、缺理由或滚动改基准，不是游戏版本。 |
| `reports/population-envelope-boundary-20261031/rolling_rebase_and_rename` | 334 | 人口±25%边界测试输入。名称区分合法边界、超一人、缺理由或滚动改基准，不是游戏版本。 |
| `reports/punctuation-native-art-20261105/independent-stageA/full-current-main` | 954 | 任务37独立验证的整套游戏输入。full-current-main仅是当时名称，不是当前主目录；A+B/A+C也不是最终全部整合。 |
| `reports/punctuation-native-art-20261105/independent-stageA/full-parent-task37` | 951 | 任务37独立验证的整套游戏输入。full-current-main仅是当时名称，不是当前主目录；A+B/A+C也不是最终全部整合。 |
| `reports/punctuation-native-art-20261105/independent-stageA/tiger-B-input` | 9 | Tiger或原版比较的少量文件输入，不是完整MOD。 |
| `reports/punctuation-native-art-20261105/independent-stageA/tiger-C-input` | 10 | Tiger或原版比较的少量文件输入，不是完整MOD。 |
| `reports/punctuation-native-art-20261105/independent-stageB/A-plus-B` | 964 | 任务37独立验证的整套游戏输入。full-current-main仅是当时名称，不是当前主目录；A+B/A+C也不是最终全部整合。 |
| `reports/punctuation-native-art-20261105/independent-stageC/A-plus-C` | 954 | 任务37独立验证的整套游戏输入。full-current-main仅是当时名称，不是当前主目录；A+B/A+C也不是最终全部整合。 |
| `reports/runtime-followup-20261104/sol-independent-validation/native-comparison-probe` | 3 | Tiger或原版比较的少量文件输入，不是完整MOD。 |
| `reports/save-audit-1891/logs/tiger-candidate` | 1020 | 1891候选的Tiger审计副本，不是额外通过验收的版本。 |

- `research/20261031/naval-reference-vanilla-empty-overlay/descriptor.mod`只是空覆盖层描述，不能当作完整版本。
- `reports/hus-player-flow-20261106/before`是任务44改前文本/脚本子集；`astra-frozen*`是各轮分配文件子集，带v2的最终冻结与中间稿有区别。发布以release.json绑定的主MOD/Git为准。
- `reports/prose-icons-20261106`内before、candidate、reviewed等也是审查材料，不因名称像版本就成为主目录。
- 本次扫描以MOD metadata/descriptor定位报告内源码包，不把每个单文件diff或文本截取另算完整版本。未带元数据的局部材料仍应按原报告清单使用。
- `runtime`、`live-observer-20261105`、`observer-diaspora39`等是日志/设置/存档证据，未发现MOD代码目录；不把运行profile列作新的主源码。
- **旧维护打包版** `releases/nesnd-maintenance-20261104.zip`：945文件条目，44,540,363字节，包metadata为0.1.0且支持版本为空。SHA256 `3334708b37e064cf46affd98e6c6b9c794c677f9676a669bfd8865b4a392aac2`。不是当前1.15修正版，也不认证引擎通过。
- **旧清理前包** `reports/logfix-release-20261101/pre-cleanup-package.zip`：534文件条目，44,192,941字节。SHA256 `eedcac183d6c4c08a477daa779b2f954103f98a3ac699705dfd1ff994ff4a32f`。保存早期logfix清理前内容，可能包含当时临时材料，不能直接作为现行发布包。
- 以上两份ZIP均实际读取了目录和metadata，没有解压覆盖主MOD。工具目录的Tiger、Rakaly ZIP是工具安装包，不是MOD版本。
- `baselines`和本体、工坊参考资料是只读语法依据，不是NESND发布版本。

## 4. Git保留的版本引用

下列远端分支在2026-11-06通过git ls-remote核对，缓存与实际远端一致。旧本地候选分支已经清掉，但远端仍保留。`origin/HEAD`只是main别名，不是另一个版本。

| 远端分支 | 提交 | 用途 |
| --- | --- | --- |
| `archive/original-20261030` | `f18b6c45525351f5bf1a86ab29cccff9fee49500` | Archive original MOD snapshot from 2026-10-30 before development |
| `archive/unselected-japan-legacy-a` | `6448bd8575dadbbc2d53cae5c3a0c06179001d7b` | Checkpoint f2-japan-legacy-20261101-a; UNSELECTED alternative after user design clarification |
| `archive/unselected-player-ack-a` | `5bbfadad35ebe07f5fc4f1e5888f48a6d07a99cf` | Checkpoint f2-player-continuation-20261101-a; UNSELECTED alternative after user design clarification |
| `candidate/f1` | `63bd857f709c63c9331ad8afbd86592c3807de1e` | Archive frozen F1 debug candidate; engine acceptance pending |
| `candidate/f2` | `6b9c90c38520dc9fe4695d4cc7c2b6a01e305c50` | Checkpoint batch-debug-20261101-f2; Selected debug baseline; runtime coverage partial |
| `candidate/female-hair-a` | `e3726f929186b9c24899bcc817c78a816257c7e8` | Preserve female-hair-20261101-a; independent candidate, acceptance limited to recorded evidence |
| `candidate/female-hair-b` | `954f661fb5937cd7a1850678e82753d0013986e8` | Preserve female-hair-20261101-b; independent candidate, acceptance limited to recorded evidence |
| `candidate/lin-resume-a` | `7623b72cf3063f28fdde31ab5045b166f2b80c93` | Preserve sequence-resume-20261101-a; independent candidate, acceptance limited to recorded evidence |
| `candidate/map-refinement-a` | `4bf0ce6d333d48c3b53a535a547db6c5910822e6` | Preserve map-refinement-20261101-a; independent candidate, acceptance limited to recorded evidence |
| `candidate/resumed-integrated-a` | `5edbdf6d671f023c9a4d39026152de8e6402b6bb` | Preserve resumed-integrated-20261101-a; independent candidate, acceptance limited to recorded evidence |
| `candidate/sequence-a` | `8931bd455a53ca949628a507db2058760505bb29` | Preserve f2-sequence-debug-20261101-a; independent candidate, acceptance limited to recorded evidence |
| `copilot/create-empty-repo` | `d05a263e1497318212aad1a45b9d145b66a749b5` | Remove starter README for empty repository |
| `feature/canon-routes-20261104T203047Z` | `f05f0639d3cba02206fb357043a90deb32ba8c47` | Implement canon-based country routes, HUS hierarchy and unity policies |
| `feature/regional-development-20261104` | `b94582ecec7b0b6dd5620a184658190157fc1729` | Add seven regional development chains and expand character and small-state plans |
| `fix/cne-time-native-ban-20261103` | `f6eb822e16cae6bd0a2b420a27a9116efdacdb9f` | Escalate prolonged CNE reform costs and disable isolated native error chains |
| `fix/journal-mechanics-20261104` | `b374be519fe71a7c8bfca48b18d94645b0151766` | Fix journal feedback and add Persian resources and Wu western incorporation |
| `fix/journal-war-feedback-20261104` | `ece3f9fcdf421a21f628873512159c2d277062bd` | Fix journal progress, Delhi visibility and Ming loyalist war settlement |
| `fix/observer-logfix-20261103` | `a70eb1257795372105751b1e257a0a21dc83638e` | Fix observer-run scope and parsing errors without changing journal refresh |
| `main` | `67c876ef315162cf66a4e4b26338bf43abf72d45` | Clarify regional goals and complete HUS journal interactions |
| `test/observer-5x-20261103` | `adfc31759b355d33e0f09269822911b367499b53` | Gate overseas commissions behind expansion and harden India boundary cleanup |

标签的目标是以下**提交**，不是annotated tag对象本身的SHA。

| 标签 | 目标提交 | 含义 |
| --- | --- | --- |
| `f1-frozen-20261101` | `63bd857f709c` | 冻结F1调试候选，未认证整包。 |
| `f2-pre-player-20261101` | `6b9c90c38520` | 当时选用的F2调试基线，实机覆盖局部。 |
| `main-snapshot-20261101` | `45f475e1228d` | 当时主MOD和工程配置起点，未整体实机认证。 |
| `original-20261030` | `f18b6c455253` | 作者原始快照。 |
| `unselected-japan-legacy-20261101` | `6448bd8575da` | 明确未选用的日本旧机制候选。 |
| `unselected-player-ack-20261101` | `5bbfadad35eb` | 明确未选用的玩家续玩确认候选。 |

main的历次提交同样保留完整历史，关键玩法阶段见开发总结。没有为每一个提交重新创建一份本地MOD。远端`copilot/create-empty-repo`仅是建仓记录，没有玩法；`test/observer-*`仅表明测试分支名称，不认证其全部功能。

## 5. 应保留什么、接手时避免什么

1. 工作以M和最新main为准，先保护M中尚未同步的作者编辑。原始版是文风和设计溯源基准。
2. 作者要求约三份关键源码：原始版、本轮改前、当前最终。当前22个backup目录、2个export及嵌套副本明显超出这个目标；本次文档任务没有执行删除，不能写成“清理完毕”。
3. Git保存历史。完整备份可按需要轮换；失败现场、测试输入和撤回候选不承担永久发布职责。清理时仍须验证绝对路径与用途，用户存档及独立Hanfu项目不在可随意清理范围。
4. 已经删除的2026-11-01旧本地F1/F2目录，不因旧交接链接存在就当成仍可读取；需要时查上面的Git标签/分支。
5. candidate/checkpoint、文案冻结、工具测试通过与ENGINE_PASS互不等价。此清单不新增任何游戏验收声明。
