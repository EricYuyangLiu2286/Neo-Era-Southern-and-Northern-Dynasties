Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: WORK/reports/2026-11-06-hus-classes/

# HUS 社会阶序条件显示（2026-11-06）

## 范围与来源

修复“社会 → 阶级 → 东洲等级制度／四等户籍”将文化条件显示成反复“有满文化／没有满文化”的问题。用户禁止本次启动游戏，由作者复测；要求新分支提交推送、同步主 MOD、不合并 main。没有操作当时仍在运行的游戏。

游戏 1.15.0 Ivan-Chai，STATUS 基线 Steam build 26453692。Git 父提交 90fe4b4。分支 `codex/hus-classes-tooltip-20261106`，最终提交及同步文件 SHA 见 WORK 报告目录 `release.json`。

已读取主 MOD AGENTS、NESND 调试/验证流程、STATUS、工程适配及任务约定。用户点名的 setup-matt-pocock-skills 已检查：本地任务账、五种分诊标签、single-context 文档布局均已配置，沿用现状，不重新初始化。另使用 diagnosing-bugs 的项目双层反馈及 nesnd-player-writing。

## 原始证据

- 先保留已存在的同名旧快照为 `logs-preserved-before-current-copy/`，再将 USERDATA/logs 整组复制至 `WORK/reports/2026-11-06-hus-classes/logs/`：66 文件、12,003,068 字节。`log-manifest.json` 保存逐文件 SHA。由于作者的游戏仍在运行，这是复制时刻的快照，不代表运行终局。
- 当前 error.log 最早相关条目为 22:17:06，首条指向 `common/scripted_triggers/nesnd_hus_registration.txt:78`，调用链包含 `common/social_hierarchies/nesnd_hus_social_hierarchy.txt:2`。
- 当前 error.log 有 372 条本问题错误；error.1–5.log 有 6,546 条同源错误，总计 6,918 条。轮转日志只保留最近部分，不能据此推定首次发生时间。
- 错误成对出现：`Invalid scope for switch ... got 'none'` 和 `Event target link 'culture' returned an unset scope`，分别指向旧第 74、78、82、86 行的 culture 切换。完整分组及调用栈在 `log-analysis.json`。
- 截图已留存为 `reported-screenshot.png`。修改前独立完整备份：`WORK/backups/pre-change-hus-classes-20261106-20261106T223132Z/mod`，1104 文件核验通过。

## 原因与逐行映射

原版 GUI `game/gui/culture_panel.gui:756` 调用 `[SocialHierarchy.GetPopTriggerDesc]` 生成阶序的通用说明。该路径没有具体 pop，日志确认当前 scope 为 none。四类 trigger 却展开 `culture = { ... }`，无法取得文化对象；文化传承条件被丢掉后，只剩可直接描述的 `has_pop_culture = manchu` 及它的反向条件。

下表行号均对应备份中的旧 `common/scripted_triggers/nesnd_hus_registration.txt`，不是修改后行号。

| 截图行 | 脚本来源与残缺展开 |
| --- | --- |
| “给予任何人群一个特殊的社会阶级” | 原版 GUI 第 747 行 `SOCIAL_HIERARCHY_TRIGGER_HEADING`，是固定标题，不是脚本的恒真判断。 |
| 最外层“至少一项” | hierarchy 第 2 行 → `nesnd_hus_hierarchy_pop` 第 89–95 行，四类人群的 OR。 |
| 第一个“没有满文化” | 汉人分支第 78–79 行：汉传承条件无法展示；`NOT = { nesnd_hus_manchu_pop = yes }` 展开后留下对第 73 行的否定。 |
| 第一个“有满文化” | 满蒙分支第 71–75 行：蒙古传承的第 74 行失败，只剩第 73 行 `has_pop_culture = manchu`。 |
| 第一组“以下所有” | 原住民分支第 82–83 行：原住民传承消失，`NOR = { 满蒙 汉人 }` 变成“非满蒙且非汉人”。 |
| 其下“没有满文化／有满文化” | 前者是非满蒙；后者是非汉人的双重否定：`NOT (NOT manchu)`。真正的汉传承约束已在说明生成中丢失。 |
| 第二组“以下所有” | 白人分支第 86–87 行：欧洲传承消失，`NOR = { 满蒙 汉人 原住民 }` 展开三项排除。 |
| 其下“没有满文化／有满文化” | 对满蒙和汉人的排除，与上一组相同。 |
| 最内层“至少一项” | 白人分支排除原住民；原住民本身是 `NOR = { 满蒙 汉人 }`，再次否定后显示 OR。 |
| 最内层“有满文化／没有满文化” | 上述 OR 又展开为满蒙残留的 `manchu` 与汉人残留的 `NOT manchu`。 |
| “受影响人口 25.0M” | 原生阶序人口统计，脚本没有写死该数值；应由作者在相同开局状态复核，不把残缺条件文字当成统计口径。 |
| 汉人／满蒙上中下层卡片 | `common/social_classes/nesnd_hus_social_classes.txt` 的 12 个阶层：各族的 3 层复用相同文化 trigger，`allowed_professions` 决定职业层级。 |

因此“是满或不是满”是损坏的文字展开，不是完整脚本的布尔条件。真实筛选仍含汉／蒙古传承、美洲原住民／欧洲传承组和排除顺序。满文化在 MOD 的 `CE_cultures.txt` 用 `REPLACE:manchu` 保留汉传承，所以必须先按文化 key 单独划入满蒙，不能删掉这个排除。

## 原版与作者原作

- GAME 1.15 `common/social_hierarchies/00_social_hierarchies.txt:6` 的印度种姓制度在 `pop_criteria` 中用 `custom_tooltip` 包住宗教与 culture 传承组判断；中文 `social_hierarchy_l_simp_chinese.yml:19` 提供具名条件。
- 同文件江户制度直接用 `has_pop_culture` 的 OR，无需在说明中切到 culture。`common/social_classes/readme.md` 要求每个适用人群由职业及人口条件唯一归入一个阶层。
- USERDATA/docs/triggers.log 的 `custom_tooltip` 文档明确：以自定义文字替换内部条件说明。保留内部判定，且文字无需具体人口对象。
- `original-20261030` 中没有 `common/social_hierarchies/`、`common/social_classes/` 定义，也没有“东洲等级制度／四等户籍／满蒙”这套定义。后续提交 f05f063 引入本系统；278616a 将文化条件改为当前 pop 入口，解决了另一接口问题，但仍把文化切换暴露给无 pop 的说明生成。不得把后续实现称为作者原作。
- 作者规则文字样本取自原作 `ce_french_empire_journals_l_simp_chinese.yml` 的短条件提示；本次仅新增规则文字，沿用现有文化及传承译名。

## 修复

只改 3 个游戏文件：

1. `common/scripted_triggers/nesnd_hus_registration.txt`：四个复用的人口分类 predicate 各加一层 `custom_tooltip`。顶层仍按 OR 列出四类；12 个阶层及满蒙迁徙共用的条件保持原判定。
2. `localization/simp_chinese/replace/nesnd_hus_social_hierarchy_l_simp_chinese.yml`：新增 4 条具名文化条件提示，保留旧文案。
3. `localization/english/replace/nesnd_hus_social_hierarchy_l_english.yml`：新增对应 4 条英文。

另更新本 issue、任务索引及 STATUS。Git 原先缺少 STATUS；从主 MOD 当前版本纳入，只更新受影响状态行。没有改阶序定义、12 个阶层定义、法律、法律组、文化数据库、接受度、职业或迁徙效果。

界面应展示汉传承（满蒙除外）、满文化或蒙古传承、美洲原住民传承组、欧洲传承组四项明确条件。具名提示在说明生成处终止递归展开，原有文化判断仍在有实际 pop 的运行时执行。

## 检查

- 保序 PDX 解析，并沿真实阶序／阶层引用图检查说明是否裸露 culture 切换。修改前实际运行 `check_hus_classes.py` 得 FAIL：13 个入口暴露；修复后 PASS：0 个入口暴露。证据 `before-checks.json`、`after-checks.json`。这是静态危险模式检查，不是引擎渲染器。
- 去除新增 tooltip 展示包装后，整个 trigger 文件 AST 与独立备份完全一致；阶序、阶层、法律、法律组、迁徙 effect 字节完全一致。
- 两种语言各新增 4 键，BOM／语言头、同键、旧文案保留、静态文字均通过；新增键全语言目录唯一，文化名和 concept_culture 引用存在（localization-reference-check.json）。
- 实际启动已安装 Paradox Modding Toolkit 0.5.0 的 LSP，检查 trigger、hierarchy、classes 和两份本地化，5 文件诊断为空。用未保存缓冲区额外添加 `}`，真实检测到 `stray-close`，恢复后诊断清空。证据 `toolkit-checks.json`、`toolkit-protocol.json`。其诊断仍使用 ck3-script 名称，这里仅认证结构解析，不认证 Vic3 运行时作用域；未运行 Tiger。
- `git -c core.whitespace=cr-at-eol diff --check`：通过，允许项目已有 CRLF。
- 未启动、重开、暂停或控制游戏，未声称运行时错误已消失。

## 作者复测

1. 自行退出当前运行后，从 Steam 重新启动修复版，使用新开局 HUS。
2. 打开“社会 → 阶级”，查看“东洲等级制度／四等户籍”下的适用人群：应为上述四类文化条件，不再出现残缺的“有满／没有满”反复。
3. 查看及悬停汉人、满蒙、美洲原住民、白人的上中下层卡片；满文化应仍属满蒙，各职业层级与原设定一致。四等户籍的接纳上下限仍为汉人 80–100、满蒙 60–79、原住民 40–59、白人 20–39。
4. 打开／关闭该面板后，检查新 error.log 是否还出现指向这四个 trigger 的 none/culture 错误。中英文换行、阶层悬停及实际人口数量均待此复测。

## 遗留问题

此快照另有 22 条无关条目：俄国／印度／CNE 重复 journal entry，巴西－秘鲁事件重复 add_involved_country，00_ai_triggers.txt 的 state/country scope 不匹配，HQ 港口 travel position 缺失与 invalid formation assertion。这里只记录线索；没有逐项归因、修复或认定全属本 MOD。

工程文档还引用了重写后已删除的 skill reference 文件（incremental-editing.md、backup-release.md）；本次读取 Git 中历史副本辨明增量边界，未修改技能或工程配置。

## Result

源代码修复及游戏外检查完成；分支交付和主 MOD 同步指纹见同目录 `release.json`。状态为 STATIC_PASS，等待作者实机复测，不合并 main。
