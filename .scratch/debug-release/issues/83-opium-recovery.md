# 83 战胜鸦片瘾

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者内审通过，2026-11-10，游戏 1.15.0，Git main 0dfb25c；原始记录未附）
Evidence: [1.15.0 静态用例和文件指纹](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-09-opium-recovery/validation.json>)

另见[月度条件复核](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-09-opium-recovery/monthly-factors.json>)。

## 现象与期望

「鸦片失控」留下长期国家修正。作者要求用国内戒烟日志解除它，推行政策时体现小市民、地主、实业家的抵制。

## 原因与原版参照

原版 00_opium_wars.txt 在和平禁烟时按月累计，60 个月结案，3650 天超时。china_buttons.txt 由市场主实施商品禁令，opium_wars_events.txt 的成功选项解除主流文化嗜好。这里保留累计月份和戒除嗜好的处理，用国内执法和医疗能力提供不依赖市场所有权的路径。

## 改了什么

- ce_opium_je_progress_bars.txt 定义 0–100% 的鸦片瘾覆盖率，初始为 100%。每月社交传播 +0.5 个百分点，禁运 −2，章程配合二级医疗或警察 −3。章程下自有市场鸦片卖单低于 400 减 1；卖单达到 400、破产、全国动乱超过 50% 各加 1。
- CE_00_opium.txt 以「鸦片泛滥」修正为自动入口，覆盖率降至 40% 或以下后移除修正，并解除现有主流文化的鸦片嗜好。原来源国宣战资格继续由原链管理。
- scripted_buttons/nesnd_opium_recovery.txt 允许颁行五年章程，满三个月可撤销，到期或撤销后可再次颁行。按钮、进度条与状态行就地判断国内条件。
- ce_opium_modifiers.txt 通过单个国家修正同时影响三个集团的支持度，各 −3。ce_opium_events.txt 的失败选项提示新日志来源。双语 ce_je_opium 文案补齐按钮、状态、条件与结局。使用本体鸦片成瘾特质、药房和负面公文图标。

## 怎么复测

检查禁运与章程可以叠加。持有市场，卖单 399 和 400 时分别核对加减，动乱 50% 和略高于 50% 时核对严格门槛。覆盖率 40.5% 时继续，40% 或以下时解除国家修正。

## 遗留问题

验收到游戏外解析和条件用例。原版文化嗜好属于文化对象，结案会影响共享该主流文化的人口。章程和三项支持度同进退，结案一并解除。

[撤销与到期边界复核](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-09-opium-recovery/repeal.json>)

## Comments

2026-11-10：作者在 `ce_opium_je_progress_bars.txt` 修正生活水平条件：主流文化平均生活水平低于 8 时每月 +1.5（原写反为高于 8），新增高于 10 时每月 −1.5；中英文条件文字已补。

2026-11-10：作者内审通过。正文中“未启动游戏”“待复测”等为交付时的状态。
