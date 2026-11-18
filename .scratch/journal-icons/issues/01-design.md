Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: NOT_APPLICABLE
Evidence: [清单、参照图、设计表与八批提示词](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-18-journal-icons/README.md>) · [地权革命内容树与退役日志](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-18-land-reform-tree/report.md>)

# 01 MOD 日志专属图标：设计与分批提示词

## 1. 现象与期望

MOD 自己的日志约 170 个借用原版通用图标，报纸、平等主义、工业、机械工具、革命一个图标被十几到三十几个日志共用，在“启用的日志条目”列表里分不清。每个日志都要有自己的图标，按国家分批画；本次只出设计和交给 Codex 的画图提示词，不画图、不接入。

## 2. 原因

- MOD 定义、不覆盖原版键的日志共 187 个（`common/journal_entries/`）。
- 已有自制图标的 12 个不动：波兰线 8 个、宫廷力量、执政者与派系、统治者与内阁、开蒙儒学。
- 已退役、玩家看不到的 19 个不画：
  - 12 个旧档兼容键。
  - 地权革命原作的 5 个子日志与“帝国的腐化”：git 建库前已改成空壳。
  - 代理稿“襄阳之后”。
- 要画的 156 个。原版日志图标实读规格：150×150，A8R8G8B8，8 级 mipmap，119808 字节。

## 3. 改了什么

- 源目录 MOD 运行文件未改，未部署。
- 工作台 `reports/2026-11-18-journal-icons/`：
  - 全部日志清单。
  - 样式参照图与 DDS 头实读。
  - 8 批共 156 行设计表。
  - 每批一份 Codex 提示词：`codex-journal-icons-batchN.txt` 是纯文本，`.md` 是整块可复制的版本。
- 156 个接入行号逐一回原文确认过。

## 4. 怎么复测

- 交给 Codex 前，先看 `style-reference.png` 与 `design-table.md`。
- 每批画完，Codex 交 `batchN/compare-batchN.png` 与 24 像素列表模拟图，并已部署；读档后看“启用的日志条目”列表。

## 5. 遗留问题

- 待作者决定：
  - 第 4 批（日本 29 张）、第 5 批（西秦、波斯与印度 30 张）是否拆分。
  - 第 7、8 批里法国自由帽、鸢尾花、普鲁士尖顶盔、菲斯帽和三角贸易的镣铐是否可用。
  - “礼法之下的生活”三个同名变体的题材分配。
- 地权革命原作的西秦、南朝、科技三个子目标在现行版本中没有对应，是否补回待作者决定。详见地权革命报告。
- 死代码与残留：7 个退役空壳的本地化、3 个无挂载的湖广准备按钮、地权革命里 2 个无调用条件和 2 个无调用数值。是否清理，待作者决定。
