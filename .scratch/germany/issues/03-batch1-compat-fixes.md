# 03 · 第一批：莱茵按钮与克虏伯

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者实测，2026-11-12）

## 现象与期望

作者 2026-11-12：“没有问题。开始制作！”——待决 Q1–Q15 按默认。两批都做，第二批会替换“莱茵秩序的争夺”，所以第一批只做 1-B、1-D；1.15.1 无需合入。

## 原因

- D04：法国的两个莱茵邦联按钮写了 `hidden_trigger = { exists = c:PRU }`，普鲁士改为北德意志邦联或德意志、或被吞并后，按钮永远不可用，玩家看不到原因（`ce_replace_buttons.txt:15–18、:70–73`）。
- D09：普鲁士开局拥有克虏伯，总部设在威斯特法伦，而 MOD 中普鲁士在那里没有州。原版的安排是公司随鲁尔归属。

## 改了什么

- `common/scripted_buttons/ce_replace_buttons.txt:15–18、:70–73`：改为可见条件“普鲁士及由普鲁士组建的国家都不领导任何势力集团”，判定用 `nesnd_prussian_identity`。保留原作“普鲁士领导关税同盟时法国不能组建莱茵邦联”的意思。
- `common/history/countries/pru - prussia.txt`：删去克虏伯。
- `common/history/countries/frm - frankfurt am main.txt`：法兰克福开局拥有克虏伯，总部鲁尔，成立日期 1807.1.1 不变。
- 两语 `nesnd_europe_america_l_*.yml`：新键 `nesnd_rhine_no_prussian_bloc_tt`。

## 怎么复测

1. 新开局选法国，打开日志“莱茵邦联”，悬停“恢复邦联”：应显示“普鲁士及由普鲁士组建的国家都不领导任何势力集团”，开局为红（普鲁士领导关税同盟）。
2. 控制台切到普鲁士（`play PRU`），`change_tag NGF`，再切回法国：只要北德意志邦联仍领导关税同盟，此条仍为红。让它退出集团领袖后应变绿。
3. 选法兰克福（`play FRM`），公司页应有克虏伯，总部在鲁尔；普鲁士公司页没有克虏伯。
4. error.log 搜 `ce_replace_buttons`、`krupp`，应无报错。

备份：WORK `backups/pre-change-germany-batch1-20261112T225210Z`。检查：三份脚本解析通过、括号配平；两语键 86/86 一致，中文无分号；audit 与迁移后基线一致（2/132/4，均为旧问题）；v3tree 重建，`near` 显示两按钮的开启条件读 `nesnd_prussian_identity`（`:17`、`:72`）。

## 遗留问题

无。下一批是第二批（共同防卫修订、莱茵问题、莱茵联邦议会）。
