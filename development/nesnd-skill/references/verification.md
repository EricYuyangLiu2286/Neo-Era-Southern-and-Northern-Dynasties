# 检查、日志、备份与交付

> 何时读：每次交付前；写完脚本跑外部检查时；读 error.log 时；实质修改前做备份时。不必读：纯设计讨论。

## 1. 检查顺序

1. **写之前**：在 GAME 找到同类实例，读它的调用者、effect/trigger 和本地化。接口名以用户文档目录 `docs/effects.log`、`triggers.log`、`modifiers.log`、`on_actions.log`、`event_targets.log`、`custom_localization.log` 为准（当前版本的 script_docs 导出；游戏更新后请作者重新导出）。
2. **写之后，游戏外**：
   - Paradox Modding Toolkit（VS Code 扩展 `JDeffner.px-toolkit`，或命令行 `px-lsp`）：解析、作用域补全、括号/BOM/本地化头/缺失事件诊断，集成 vic3-tiger，有按触发顺序排列的事件图和本地化覆盖视图。它的规则可能落后于最新游戏版本，报错先对照 GAME 再判断。
   - 本技能 `scripts/pdx.py`（保序解析，保留重复键）、`scripts/audit.py`（GAME+MOD 数据图）、`scripts/catalog.py find <名称>`（定位符号的真实路径与行号）。
   - 交付前跑 `scripts/static_lints.py`，扫三类 Toolkit 查不出、只在加载或显示时报错的问题：缺 UTF-8 BOM、可见结局缺 `color`、会生成说明的条件里有随遍历对象变化的 `any_*` 比较（规则见 [journal-display.md](journal-display.md)）。2026-11-12 这三类在同一局里一共报了约 29 万条。
   - 查一个具体问题就写一个小检查，不建通用模拟器；检查条数不代表质量。
   - 声称某些对象相互连接时（结构梳理、调用链），做两项防幻觉检查：随机抽若干条边回原文件逐行核对；反向检查——每个对象的 id 在原文中的每处出现，都能由一条边或定义解释。内容树报告自带这两项，见 [content-tree.md](content-tree.md)。
3. **游戏内**：只在用户当次明确要求时启动（见 SKILL.md）。通常由作者自己测试，代理读作者留下的日志。

现成的检查脚本（Toolkit 语言服务器、Tiger 前后对比、按 script_docs 交叉检查）见 [tools.md](tools.md)。逐批检查的写法可参照登莱路线的 `WORK/reports/denglai-route/batch6/verify.py`：解析新文件、核本地化成对与 BOM、用内容树核邻居。

## 2. 读日志

- 位置：用户文档目录 `logs/`。`error.log`、`debug.log`、`game.log` 会轮转为 `.1` 到 `.5`；先按修改时间确认哪一份对应哪次运行，再复制整组到工作台 `reports/<日期>/logs/` 后分析，不在原处清空。
- 刷屏时，同一次运行内几秒钟就会把 error.log 轮转五次，早期内容丢失。作者报告后立即复制整组，并记下 `system.log` 的启动时间，区分本次与上次运行。game.log 覆盖整次运行，但不记条件说明类的错误。
- `scripts/log_report.py <日志目录> --out <报告.json>` 按内容归组，并保留原文位置。
- 实际时间换算游戏日期：`dedicated_server.log` 的 `[时:分:秒] … Processing Tick: 年.月.日` 行，暂停与恢复也有记录。用它判断报错发生在哪个游戏日期，和某个事件的先后关系。
- 打开存档或读档界面时，游戏会读存档文件夹里其他 MOD 和旧版本的存档，产生 `Failed to read key reference`、`Failed to find type '1' in '1.13'`、`MISSING_DLC_ENTRY`、旧国旗纹章等报错，与本 MOD 无关。
- 刷屏条数可用来反推来源。例如每秒一批、每批条数等于“国家数 × 某条件里的比较处数”，说明是界面在为一个 `any_country` 生成说明。
- 问“某件事发生过没有”时，存档比日志可靠。明文存档（或 Rakaly 解码）里各国已结束日志的记录有类型、日期和结局说明键。存档不保留已灭亡国家，结束的战争记录里也没有交战方。
- 先修本 MOD 脚本引起的错误和每帧刷屏的根因。总错误数包含原版和其他 MOD 的错误，不等于本 MOD 的错误数。
- 同一行为已经在游戏中验证过（例如进港、死亡、分裂），除非相关代码或存档格式变了，不重复验证。

## 3. 交付时怎么写

- `STATIC_PASS`：只有游戏外检查。`ENGINE_VERIFIED`：在指定版本的游戏中看到了该行为，写明场景。
- 写清楚：改了哪些文件；跑了哪些检查；哪些行为未经实机验证；遗留问题。
- 正式包只含玩法与必要资源。QA 浮层、测试事件、测试存档和验证脚本留在工作台。

## 4. 备份与版本

- 作者规则：本地只保留约三份完整源码，即原始版、本轮修改前、当前版；历史由 Git 保存。
- 实质修改前用 `scripts/backup.py --status pre-change` 备份到工作台 `backups/`；交付后清理多余的中间副本，清理前确认作者的改稿已进 Git。
- 主 MOD（游戏加载目录）和 Git 工作副本（工作台 `projects/nesnd-repository`）是两个目录。合并时按文件比较，保留作者在主 MOD 里直接做的修改。
- 远端：`EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties`。不直接推送 main；用分支，交由作者合并。

只备份将要改动的部分（例如技能目录、`AGENTS.md`、`docs/agents/`）时，用 `scripts/backup.py --paths <文件或目录>…`；路径须在主 MOD 或技能目录内，备份目录同样带 SHA-256 清单。
