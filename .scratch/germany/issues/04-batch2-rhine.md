# 04 · 第二批：共同防卫修订、莱茵问题、法兰克福的议会

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: 03
Validation: STATIC_PASS

## 现象与期望

作者 2026-11-12：“实测通过，做第二批。”按[报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-germany-review/report.md>)第 6 节与待决默认值实施。设定出处：《北明ppet》s23 p14、p24，s24 p7、p10、p25、p28，s25 p8、p18。

## 原因

旧“莱茵秩序的争夺”在普鲁士收法兰克福为附庸时永不完成，别国替普鲁士赶走法国也算普鲁士成功，没有失败出口，22 个按钮与结局无关（D01–D03、D08）。共同防卫奖励指向阿尔萨斯-洛林、奥地利算伙伴（D06、D07）。法兰克福没有自己的内容。

## 改了什么

- 共同防卫：伙伴不含奥地利（`scripted_triggers/nesnd_canon_diplomacy.txt` 的 `nesnd_canon_german_partner`）；按钮删奥地利两个、补梅克伦堡、奥尔登堡、不伦瑞克、安哈尔特，28 个按钮只对独立的邦显示（`scripted_buttons/nesnd_canon_requests.txt`）；奖励改为宣称莱茵兰、北莱茵、鲁尔、威斯特法伦（`scripted_effects/nesnd_europe_america.txt:7–10`）。
- “莱茵问题”替换旧日志（同键 `nesnd_prussian_rhine`，移到 `journal_entries/nesnd_rhine.txt`）：两个按钮“庇护莱茵流亡者”（3 年一次）、“莱茵动员”（法国无暇或议会倒向民族派时，5 年一次）；每月约 8% 抽 3 个随机事件；成功＝四地区中至少 3 个全归本国或附庸，或组成德意志；失败＝1880 年；失效＝不再是普鲁士一系。
- “法兰克福的议会”（`nesnd_frm_parliament`，法兰克福）：民族派倾向条 0–100、起点 30，四项具名月度来源；按钮“请求巴黎增派驻军”；1843《德法年鉴》、1848 驱逐令、1890 后动荡时的法兰克福公社；倾向达 90 时民族派掌握议会（事件）；1900 年结束。
- 删除旧事件 `nesnd_europe_america.2`、旧条件 `nesnd_prussian_rhine_resolved`、月度维护里的莱茵奖励。
- `german_unification.3` 的中英文覆盖：俾斯麦“出身萨克森”，引文换成 1867 年“政治是可能性的艺术”。
- 新文件：`journal_entries/`、`scripted_buttons/`、`scripted_progress_bars/`、`scripted_triggers/`、`static_modifiers/`、`events/` 下的 `nesnd_rhine.txt`，两语 `nesnd_rhine_l_*.yml`。

## 怎么复测

控制台没有 `effect` 命令，以下只用 1.15.1 实有的命令（`tag`、`activate_journal_entry`、`conclude_journal_entry`、`event`、`annex`）。

1. 普鲁士新开局：共同防卫只显示巴伐利亚与北德小邦的按钮，不再有奥地利。`activate_journal_entry nesnd_prussian_rhine` 直接激活“莱茵问题”（作者已实测可用），悬停两个按钮看条件。
2. `tag FRM`：日志“法兰克福的议会”，悬停倾向条看四项来源。`event nesnd_rhine.21` 看《德法年鉴》，`event nesnd_rhine.22` 看驱逐令（自然触发分别在 1843、1848 年）。
3. `tag PRU`，点“庇护莱茵流亡者”选第一项，再 `tag FRM` 确认倾向 +10。
4. 莱茵成功：在普鲁士 `annex FRM`，下个月应弹“莱茵河畔的边界”。失败：`conclude_journal_entry nesnd_prussian_rhine 1`（第二个结局。若弹出的是成功事件，说明索引从 1 起，改用 2）。
5. 俾斯麦：`event german_unification.3` 预览新正文与引文。
6. error.log 搜 `nesnd_rhine`、`nesnd_frm`，应无报错。

备份：WORK `backups/pre-change-germany-batch2-20261112T225805Z`。检查：12 份脚本解析与括号通过；三组本地化两语键一致（88/77/108），中文无分号；脚本引用的本地化键齐全，事件定义与引用一一对应；audit 与基线一致（2/132/4）；v3tree 重建后新变量与进度条均有写有读。

## Comments

2026-11-12 作者实测：共同防卫的激活与失效条件被逐层展开、难以读懂。已把普鲁士身份、法兰克福身份收成一句提示，变量条件改为具名提示或隐藏（`scripted_triggers/nesnd_europe_america.txt:1`、`journal_entries/nesnd_europe_america.txt:48`、`journal_entries/nesnd_rhine.txt` 两个日志的 possible 与失效结局），备份 `backups/pre-change-germany-batch2-tooltips-20261112T233341Z`。

2026-11-12 作者要求“莱茵问题”开局就显示：`journal_entries/nesnd_rhine.txt` 的 is_shown_when_inactive 去掉“已完成共同防卫”，改为普鲁士一系且早于 1880 年。激活条件不变，悬停可见“已完成「德意志的共同防卫」”。备份 `backups/pre-change-germany-rhine-shown-20261112T234043Z`。

## 遗留问题

无。
