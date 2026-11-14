# 88 西秦“比例代表制”改为地产投票

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [改前备份（含完整 MOD 副本）](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-qe1-pr-to-landed-20261111>) · [Tiger 对比](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-qe1-pr-to-landed>) · [法律系统研究 1.2 节](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-law-system-research/法律系统研究.md>)

## 现象与期望

作者原话：“比例代表制应该是 MOD 所遗留的旧版本的 VIC3 代码，版本迁移时被搞不清楚状况的 GPT 当作了新内容……现在暂时给比例代表制的转为地产投票。”

## 原因

原版 1.15 没有比例代表制法律，只剩本地化键 `law_proportional_representation`（GAME laws_l_simp_chinese.yml:473）。`law_nesnd_qe1_proportional_representation`（资格选举的变体）由代理在 Git 提交 7d39018（2026-11-02）加入，不在 tag `original-20261030`。它只由“改立共和”按钮授予，作为变体还有几处兼容缺口：女性选举权解锁清单与两条继承修正案不含它；没写 `is_visible`，所有国家的法律列表都会显示。

## 改了什么

- `common/scripted_buttons/nesnd_qe1_court.txt`：“改立共和”按钮的可见条件、预览与实际效果三处，改为授予 `law_landed_voting`。
- `common/laws/nesnd_qe1_laws.txt`：删除（只有这一条法律）。
- `localization/{english,simp_chinese}/replace/nesnd_qin_persia_l_*.yml`：删去该法律名称与说明两键。
- `localization/{english,simp_chinese}/replace/nesnd_qin_politics_l_*.yml`：按钮说明改为“由民选总统与按地产投票选出的议会主持国政” / “a parliament elected under Landed Voting”。

## 怎么复测

新开局西秦，走宫廷日志至文人一方鼎盛并研究民主，点“改立共和”：应得到总统共和制＋地产投票；任一国家法律列表中不再出现“比例代表制”。

## 遗留问题

- 宫廷文人分数原先只给资格选举 +20、财产投票 +15，不计地产投票。作者定为地产投票 +5：已加在 `common/script_values/nesnd_qe1_court.txt:17` 与进度条 `common/scripted_progress_bars/nesnd_qe1_court.txt:25` 的“选举与共和制度”一项（改前备份在同一备份目录 `round2/`）。西秦开局为专制，开局分数不变。
- 旧存档中已实行比例代表制的西秦，载入后该法律不存在；按规则不写救档，以新开局为准。
- 西秦的新投票法律构想另记于 [89](89-qe1-xitang-xiyuan-law.md)。
