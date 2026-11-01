# 保存原始版本与当前源码

Record: implementation
Category: enhancement
Status: ready-for-agent
Execution: claimed
Assignee: root
Blocked by: none
Validation: NOT_APPLICABLE
Evidence: [首次保存](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/git-bootstrap-20261101.json>)；[六个新候选远端与archive核对](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/git-resumed-candidates-20261101T014406Z/report.json>)

## Scope

按用户要求保存最初版本、当前主 MOD 和最新候选到 [私有仓库](https://github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties)。保留可追溯历史与验收状态。源码上传不等于主 MOD 合入或游戏验收。

## Acceptance

- 先核远端已有内容与权限，保留已有历史。
- 最初可证版本从 `WORK/backups/pre-update-20261030T233944Z` 及 manifest 建立来源；上传前复核其内容。
- 当前主 MOD、F1/F2 等独立保存，提交或标签绑定来源与实际验证等级。
- 推送后核远端 ref；登录未成功时保留本地工作并记录具体阻塞。
- 最终合并清单同时保护新文档，避免旧候选整包覆盖。

## Result

已确认私有仓库与当前账号推送权限，保留原远端初始提交和既有 copilot 分支。首次推送与远端 refs 核对已完成：

- 原始288文件：`archive/original-20261030`，提交 `f18b6c45525351f5bf1a86ab29cccff9fee49500`，标签 `original-20261030`。
- 本轮起点318文件：提交 `45f475e1228dee046607f4a1bdd784f661830341`，标签 `main-snapshot-20261101`；main额外保留远端README历史与验收状态说明。
- 冻结F1共514文件：`candidate/f1`，提交 `63bd857f709c63c9331ad8afbd86592c3807de1e`，标签 `f1-frozen-20261101`。
- 工作副本：`WORK/projects/nesnd-repository`，Git元数据留在WORK，不进入主MOD加载或快照指纹。

本轮更新文档、F2与最终验证证据的后续提交仍在进行；本任务保持claimed直至交付版本保存并复核。

F2已另存 `candidate/f2`，提交 `6b9c90c38520dc9fe4695d4cc7c2b6a01e305c50`；玩家确认和旧日本终局备选已保存到两个 `archive/unselected-*` 分支，未合入选定候选。三条远端分支均已核对。后续顺序修复使用独立 `f2-sequence-debug-20261101-a`，未验收前仅保存checkpoint。

## Comments

2026-11-01：用户指定远端作为后续最终保存位置；本机首次 git ls-remote 因没有可用登录凭据失败，主控正在处理。此记录不宣称仓库已上传。

2026-11-01：Git Credential Manager官方设备授权完成，HTTPS访问及推送成功。上述首次失败保留为历史，不再是当前阻塞。

## Latest remote checkpoint

2026-11-01本轮重新读取远端refs，原始版、F1/F2、未选用备选及下列6条新候选均仍存在。报告remote_verified=true、git_archive_exact=true；Git保存不代表玩法合入或全体验收。

| 分支 | 提交 | 文件数 |
| --- | --- | ---: |
| candidate/sequence-a | 8931bd455a53ca949628a507db2058760505bb29 | 532 |
| candidate/lin-resume-a | 7623b72cf3063f28fdde31ab5045b166f2b80c93 | 532 |
| candidate/female-hair-a | e3726f929186b9c24899bcc817c78a816257c7e8 | 533 |
| candidate/female-hair-b | 954f661fb5937cd7a1850678e82753d0013986e8 | 533 |
| candidate/map-refinement-a | 4bf0ce6d333d48c3b53a535a547db6c5910822e6 | 549 |
| candidate/resumed-integrated-a | 5edbdf6d671f023c9a4d39026152de8e6402b6bb | 553 |

本次文档整理前main为670870a0dc3e4f2bae2d37a81f60bda1e1fc2e04且工作树干净；后续仅提交本票/任务索引、当前交接及development支持快照。原始玩法文件保持main基线，综合候选及运行冻结均不改。本任务随持续交付保持claimed。
