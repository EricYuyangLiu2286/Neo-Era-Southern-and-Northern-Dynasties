# 01 内容树工具与首批两个用例

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: NOT_APPLICABLE（工具，不涉游戏行为；未启动游戏）
Evidence: [交付说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/content-tree/DELIVERY.md>)

## 现象与期望

USM 内战 JE 链经多轮代理改写后，作者只有大概印象；tiger/toolkit 读不了 1.15，单靠 AI 搜索又分不清漏了还是编的。要求：脚本机械抓关系、每条边可追到出处，AI 只补软边并留证据；交付可重复使用的工具、USM 内战与"南美土著王朝叛乱"两份 HTML、覆盖率报告。

## 原因

无（新工具）。

## 改了什么

- 新增 `nesnd-workbench/tools/content_tree/`（ct_index.py 索引、content_tree.py 命令行、ct_pending.py、ct_render.py、ct_template.html、README.md）。复用技能 pdx.py 与 catalog.py。
- 输出 `nesnd-workbench/reports/content-tree/`：全局索引（27,712 节点 / 137,328 边 / 未解析 10），两个用例的 HTML、判定记录、子图 JSON、覆盖率报告，DELIVERY.md。
- MOD 脚本未改。作者确认后，工作流写进技能：新增 `references/content-tree.md`（何时用、五条规则，含编户 JE 的正反例），SKILL.md 第 4 节表格加一行，`references/verification.md` 加抽查与反向检查。已同步主 MOD 与 Git 工作副本的 `development/nesnd-skill/`，提交 `91ed9a1`（分支 `codex/event-recovery-and-text-archive-20261107`，未推送）。

## 怎么复测

双击 `reports/content-tree/cases/usm_civilwar.html` 与 `native_rebellion.html`；查判定是否划对，直接改同名 `.decisions.txt` 后执行 `python content_tree.py expand …` 与 `render …` 重出。

## 遗留问题

- 验收用例第一次判定把编户改革 JE（`nesnd_c2_hus_agenda`）误判为"公民路线"边界，已改正并在判定文件里留记录。
- 查图时发现的疑似问题（只写不读、只读不写、无调用、永不触发的结局、提示与实际年限不一致等）见交付说明第 7 节，未修改。
- SKILL.md 约 6.5 KB，略超技能自定的 6 KB 篇幅。
