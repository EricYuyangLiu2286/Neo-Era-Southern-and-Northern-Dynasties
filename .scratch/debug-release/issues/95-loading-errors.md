# 95 波斯规则、东亚服装、文化修正与法国日志的加载报错

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（1.15.1，build 26591675；本次由作者复测）
Evidence: [本次 error.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-13-loading-errors/logs/error.log>) · [日志归组与检查结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-13-loading-errors>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-loading-errors-20261113T001428Z>)

## 现象与期望

00:05–00:06 加载期间出现波斯规则解析失败、东亚 mesh/entity 重名、12 条文化修正类型缺失、3 条法国日志失效结局重复。整份 error.log 共 4,267 行。外部 MOD 冲突只报告。

## 原因

- A：旧中文传道规则使用 `[concept_pops]`。原版注册 `concept_pop`，复数只作本地化键。00:04 的文件备份可检出错误，00:10 的主 MOD 已改正。中英规则键及 GUI 引用齐全。
- B：按 content_load.json 核对全部五个启用 MOD。中国帝冠、日本平民头饰的 mesh 和 entity，以及日本御服的 mesh，均由原版和 East Asian Clothes: Redux 各定义一次。另有 11 条贴图重名，其中 4 条是日本头饰与原版重名，7 条来自 EACR 内部。主 MOD 无对应定义。
- C：布里布里、古纳文化及 12 项正负静态修正齐全。生活水平、文化接纳度、文化狂热目标的 6 个底层类型在数据库中缺少显式定义。
- D：三个日志均有政治和资格两条失效定义。原作标签 original-20261030 的政治事件为 .3、.22、.21。后来加入的无建制州流亡路径及子日志静默退出，见工作台 reports/runtime-115-first/french-seat-loss/independent.md。

## 改了什么

- `common/modifier_type_definitions/ce_culture_modifier_types.txt` 加 6 个类型，字段对照原版 central_american。
- `common/journal_entries/ce_french_empire.txt` 将每项两个失效 trigger 用 OR 合并。按作者选择，政治结局保留事件和清理，资格失效时仅父日志按原流亡守卫最多派发一次 .24，两项王朝日志静默退出。
- 波斯本地化沿用现文。服装资产只读核对。pdx.py 已逐树比对条件和效果。Toolkit 七文件零诊断，波斯双语各 150 键一致，6 个修正类型各定义一次，12 处引用全部解析。

## 怎么复测

重启后检查新的 error.log 第一次加载。建议新开局验收。读档可查尚活跃的日志和规则显示。打开唐衣大食「三教消长」天命说版。法国分别测政治失效和存续但失去全部建制州。哥斯达黎加有布里布里人口，巴拿马有古纳人口，查看对应修正生效时的数值明细。

## 遗留问题

使用同一 playset 时仍预期出现 B。另见 21 条重复添加日志（包括法国父日志）、HUD 路径及文字、TGGM 元数据、缺失调停图标、地图港口及 HQ、三角贸易脚本取值等独立报告，详见 log-groups.json。audit.py 的 2 条 Steam 文案解析、132 条省份归属及 4 条重复投资者与上轮逐项一致。static_lints.py 的 75 条 any 遍历提示未指向改动文件。
