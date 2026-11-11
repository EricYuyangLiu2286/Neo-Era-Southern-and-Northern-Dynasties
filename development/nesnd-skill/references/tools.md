# 工具索引

> 何时读：要跑检查、查接口、建索引、备份、生成清单或批量改历史文件前，先在这里找现成工具。不必读：纯设计和写作。

命令都在技能目录 `C:\Users\Eric Liu\.codex\skills\nesnd-victoria3` 下运行（`python scripts/<脚本>`）。脚本只读 GAME 和工坊；写入的位置都在工作台，`pop_rewrite.py --write` 例外，它按计划改主 MOD。

## 1. 本技能 scripts/（通用，随技能维护）

| 脚本 | 用途 | 什么时候用 | 运行 |
|---|---|---|---|
| `catalog.py` | 版本化的源码符号索引（GAME、MOD、三个工坊兼容源） | 找定义的真实路径和行号；游戏更新后先 `status` | `python scripts/catalog.py find <名称>`；`status`；`refresh` |
| `pdx.py` | 保序解析器，保留重复键 | 其他检查脚本 `from pdx import read` | — |
| `audit.py` | GAME+MOD 数据图与失效引用 | 版本迁移、大范围改名后 | `python scripts/audit.py --out <WORK/reports/…/audit.json>` |
| `je_stats.py` | 日志的行数、按钮、进度条、timeout 统计 | 对比原版、作者原作与代理稿的尺寸 | `python scripts/je_stats.py "<原版 glob>" "<ce_ glob>" "<nesnd_ glob>"` |
| `log_report.py` | 按内容归组 error.log，保留原文位置 | 读作者留下的日志 | `python scripts/log_report.py <日志目录> --out <报告.json>` |
| `docs_lookup.py` | 查 script_docs 导出（trigger、effect、event target、on_action、modifier、custom loc、data type） | 不确定接口名、作用域或参数时 | `python scripts/docs_lookup.py <名称> --kind trigger` |
| `toolkit_check.py` | 用 Paradox Modding Toolkit 的语言服务器检查指定文件，带“多一个右括号”的反例对照 | 改完脚本或本地化后 | `python scripts/toolkit_check.py --out <报告目录> <MOD 相对路径>…` |
| `tiger_delta.py` | 对改动前备份和当前 MOD 各跑一次 vic3-tiger，只列改动文件新增的报错 | 交付前 | `python scripts/tiger_delta.py --before <备份>/mod --out <报告目录>` |
| `script_xcheck.py` | 按 1.15 script_docs 交叉检查一组文件：未知 trigger/effect、条件与效果混用、作用域不符、变量只写不读、引用未定义 | 一个新系统写完时 | `python scripts/script_xcheck.py "common/**/nesnd_sha_*.txt" "events/nesnd_sha_*.txt"` |
| `vanilla_overrides.py` | 比对主 MOD 与原版同路径文件，重写 [vanilla-overrides.md](../lookup/vanilla-overrides.md) 与基线 JSON | 版本更新；新增或撤回同路径覆盖 | `python scripts/vanilla_overrides.py --out <WORK/reports/…>` |
| `pop_rewrite.py` | 按 JSON 计划改 `history/pops`：替换某文化人数、追加人口，逐州断言总量 | 人口重配、拆州后补人口 | `python scripts/pop_rewrite.py <plan.json>`（只预览）；确认后加 `--write` |
| `backup.py` | 带 SHA-256 清单的校验备份 | 实质修改前 | `python scripts/backup.py --status pre-change --label <主题>`；只备份部分：`--paths <路径>…` |
| `skill_loss_check.py` | 技能整理后，逐段核对旧内容的去向 | 整理或大改本技能后 | `python scripts/skill_loss_check.py --old <备份>/skills` |

## 2. 工作台与外部工具（只登记，不移动）

| 工具 | 位置 | 用途 |
|---|---|---|
| V3-content-tree（v3tree） | `D:\Users\Eric Liu\OneDrive\Documents\Modings\V3-content-tree` | 内容树：`index`、`near`、`new/expand/render`，见 [content-tree.md](content-tree.md) |
| Paradox Modding Toolkit | VS Code 扩展 `jdeffner.px-toolkit`（语言服务器 `dist/server.js`） | 解析、作用域、本地化诊断；`toolkit_check.py` 自动找最新版本 |
| vic3-tiger 1.19.0 | `WORK/tools/tiger-1.19.0/vic3-tiger.exe` | 静态检查；规则可能落后于新版本 |
| Rakaly 0.8.22 | `WORK/tools/rakaly-0.8.22/` | 解码存档副本（先复制到工作台） |
| 存档结构导出 | `WORK/tools/save_structure.py` | 逐州职业、配员、基础设施、建筑账项 |
| 地图审计与提案 | `WORK/tools/map_design_audit.py`、`map_design_options.py` | 州人口、产业、面积、邻接、locator 证据 |
| 交通与港口门禁 | `WORK/tools/map_transport_preflight.py`、`inspect_splnet.py`、`spline_candidate.py` | 见 [map-transport.md](map-transport.md) |
| 地图编辑器工程 | `WORK/editor/`（`province_move.py`、`harbor_routes.py`、`map_editor_runtime.py`） | 拆州的守恒计算、显式新港口、隔离启动编辑器 |
| 按钮守卫回归 | `WORK/tools/check_button_guards_20261101.py` | 引用安全的回归断言，见 [script-safety.md](script-safety.md) |
| 旧内容树 | `WORK/tools/content_tree/` | v3tree 的前身，旧用例仍可读 |
| OOXML 提取 | `beiming-biography/scripts/extract_ooxml.py` | 从设定 docx/pptx 提取带定位的文本 |

工作台 `tools/` 和各报告目录里其余脚本多为一次性（带日期或任务名），不再登记；需要时按报告目录查。

## 3. 好的实例（只读，作参照）

| 实例 | 位置 | 看什么 |
|---|---|---|
| 任务记录 | 主 MOD `.scratch/denglai-route/issues/14-boli-split-delay-alliance.md` | 作者要求、改法、对照表、验证状态与证据路径写在一页 |
| 逐批检查脚本 | `WORK/reports/denglai-route/batch6/verify.py` | 解析、本地化成对与 BOM、邻居核对 |
| 内容树报告 | `WORK/reports/2026-11-09-land-review/` | 判定理由、核对清单、按钮核对 |
| 链条概率模拟 | `WORK/reports/2026-11-09-land-review/sim/land_reform_sim.py`、`odds.md` | 规则带出处，外部条件写成假设 |
| 任务提示词 | 主 MOD `docs/agents/prompt-kit.md` §3 | 修复类提示词的复述、提问与成稿 |
