Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS（未启动游戏，待作者复测）
Evidence: [第一轮报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-ai-cliche-audit/report.md>) · [第二轮报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-ai-cliche-audit/report_round2.md>) · [逐键记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-ai-cliche-audit/changes_final.tsv>)

# AI 八股清理与 flavor 补写

## 现象与期望

作者要求在 nesnd_ 文件和 ce_ 中代理改过的键里，清理 GPT 留下的“AI 八股”，并为缺少 flavor 的可见事件补写中英 flavor。范围包括公文套话、应改用文本函数或概念的死文字、减字、生造译名、英文 AI 腔，以及注释里的过程记录。xiuquan、per_tension、acw_slavery_question、button_tooltips 四组本地化不动。第一轮确认后，作者授权直接实施，保留修改痕迹，拿不准的统一询问。

## 原因

代理稿的高频特征与作者原作、原版差距大。单字“须”每十万字 176 次（原作 0），“安排”104 次（原作 2.2），英文 arrangements 25.7 次（原作 0），英式拼写 329 处（原作与原版用美式）。

## 改了什么

- 本地化 128 个文件：改写 1,599 个键，新增 286 个 flavor 键。需处理的问题从 2,169 处降到 59 处，剩余均为有意保留。
- 事件脚本 37 个：各加 `flavor = <事件>.f`，共 143 个事件。
- 其他脚本 31 个：只删注释中的任务编号、批次、日期。
- 修改前备份：`WORK/backups/pre-change-ai-cliche-cleanup-20261112T030017Z`。

## 怎么复测

读档即可。重点看公共事业、南朝改制、小国防御按钮的动态国名、吕宋财政、地权革命条件提示、朝鲜重建运动、宫廷派系进度条。详见第二轮报告第 9 节。

## 遗留问题

第二轮的 13 项已由作者答复，第三轮已执行，见下节。

## 第三轮（2026-11-12）

[第三轮报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-ai-cliche-audit/report_round3.md>)。

- 改动 745 个键：
  - ce_ 代理改写过的 55 个键恢复原作。
  - 英文改为英式拼写，事件标题改为标题式大写，指本国的 the government 改为 we/our。
  - “通商章程”统一。
  - 六个自创人物改用备选二名字。
  - 53 条有套式的 flavor 重写为核实引语或体裁文字。
- 注释只把“作者定”改为“作者规定”，唐衣大食的注释恢复原样。
- flavor 套式和数字规则写进 nesnd-player-writing。
- 备份：`WORK/backups/pre-change-ai-cliche-round3-20261112T110750Z`。
- 待作者决定：
  - 其余 84 条匿名 flavor 和其他代理的 10 条怎么处理。
  - 三处过时的“待作者定名”注释。
  - 图片制作清单中未记录的场景。

追加（同日，作者第二次答复后）：
- 我写的另 84 条匿名 flavor 已按新规则重写成体裁文书。
- 其他代理写的 137 条 flavor 已全面审查：保留 54 条，建议改写 71 条，建议修正 1 条，作者原文 11 条。是否改写待作者定。
- 第二轮误改的 4 条登莱作者手改稿已恢复。
- 三处过时注释已加“（旧注释，实际情况需要核查）”。
- 新增技能文件 period-voices.md。
- 批量重绘事件图的清单和提示词在 `WORK/art/2026-11-12-event-redraw/`。
- 作者第三次答复后：其他代理写的 72 条（71 条改写、1 条修正）已按新规则重写。俄国边疆 8 条核实为 MOD 有意改写，没有恢复原版。作者决定事件图不重绘。
