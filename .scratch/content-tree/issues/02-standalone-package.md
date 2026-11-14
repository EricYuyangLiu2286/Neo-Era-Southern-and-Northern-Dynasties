# 02 内容树独立成仓库

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: 01
Validation: NOT_APPLICABLE（工具；未启动游戏）
Evidence: [第一步评估报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/content-tree/packaging/01-assessment.md>)；[第二步设计](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/content-tree/packaging/02-design.md>)；[第三步实现与验收](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/content-tree/packaging/03-implementation.md>)

## 现象与期望

把内容树封装为独立 git 仓库，不依赖 NESND，其他制作者及其大模型能从零用起来；人不用大模型时，可在本地网页里输入根、设步数、逐步"接受 / 继续"直到验收，再保存并展示。分三步（评估 → 设计 → 实现），每步经作者确认。

## 原因

无（新工作）。

## 改了什么

- 第一步：只写评估报告，未改代码。结论：推荐"步数搜索 + 停止规则 + 本地网页界面"与现行大模型判定两条路径，共用判定文件。双击打开的 HTML 不能运行 Python、不能读写本地路径，界面需要本地小服务器。

- 第二步：设计文档。作者已定：工作台外单独文件夹（路径待给）、MIT 以后公开、中英双语、只附原版示例。配置用 JSON；多 MOD 顺序先读启动器 content_load.json 再请用户确认；本地网页界面靠本机后台（127.0.0.1 + 随机口令），节点操作写成与大模型路径相同的判定文件。

- 第三步：新仓库 `D:/Users/Eric Liu/OneDrive/Documents/Modings/V3-content-tree`（MIT，EricYuyangLiu2286；提交 f0c11bd、2d31abd，未推送）。原版、两层、三层、网页、两次冷启动均已验收；NESND 两个用例与工作台结果完全一致。工作台 tools/content_tree、主 MOD 脚本、技能均未改。

## 怎么复测

双击新仓库的 start.bat，在“设置”里填路径、建索引、搜索一个 JE；或按 README 用命令行。

## 遗留问题

- 多 MOD 加载顺序（`content_load.json` 列表顺序是否即加载顺序）与 REPLACE/INJECT 语义未实证。
- 推送与公开由作者决定。
- 加载顺序、REPLACE/INJECT 语义、无前缀重复定义“先读到的为准”仍未经游戏内实证。
- 工作台旧版 tools/content_tree 仍有参数化边来源层、漏抓文件夹、含空格 id 三个问题，未改。
- 现有缺陷：`ct_index.py:801/807/819` 参数化边的来源写死为 MOD，仅影响代码片段显示。
