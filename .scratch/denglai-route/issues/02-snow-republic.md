# 02 雪国共和与迁都

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（Victoria 3 1.15.0 / 26453692）  
Evidence: [检查结果与候选文件 SHA](<../../../../../nesnd-workbench/reports/denglai-route/batch1/verification.json>) · [49 个节点的 near 输出](<../../../../../nesnd-workbench/reports/denglai-route/batch1/near-all.json>) · [改动前备份](<../../../../../nesnd-workbench/backups/pre-change-denglai-snow-republic-20261110T201325Z/manifest.json>)

## 1. 现象与期望

作者要求先交付「雪国共和」和两个迁都决议。路线开局选定，回山东前保护共和政体，最后由原生统一机制决定谁能组建华夏。

## 2. 原因

`common/history/countries/SHA.txt:24` 已有十年开局修正；`common/country_formation/CE_major_formables.txt:2` 已有 CHI 范围和门槛。两者沿用。海参崴、青岛是港口城镇，原生迁都效果接受州区域。

## 3. 改了什么

主 MOD 新增九份脚本，其中八份同名 `nesnd_sha_republic.txt`。

- `common/journal_entries/` 管身份替换、年度六事件、统一状态和结局。
- `events/` 管开局选择、六个年度事件、议都与统一后的两种叙事。
- `common/decisions/` 管海参崴与青岛的两个一次性决议。
- `common/scripted_buttons/` 管誓师及颁布共和宪草。
- `common/static_modifiers/` 定义身份、改制、迁都、誓师和集团认可修正。
- `common/scripted_triggers/` 共用登莱身份、共和政体、山东解锁及华北华南领土判定。
- `common/script_values/` 计算迁都费用，以及首都迁前、迁后的华北和西北人口。
- `common/on_actions/` 接新开局、山东易手、改制、革命继承和北朝镇压战果。
- `common/laws/nesnd_sha_governance_lock.txt` 给六项非共和政体的提案增加登莱条件。逐项对照原版，其他字段一致。
- `localization/{simp_chinese,english}/replace/nesnd_sha_republic_l_<语言>.yml` 各 68 个键。已更新路线 `map.md` 与 `docs/agents/STATUS.md`。
- 九份脚本经技能 `pdx.py` 解析。对改动前备份与当前目录分别运行 `audit.py`，原有两处说明文字解析提示、132 条地块归属和四条建筑投资者提示逐项相同。内容树已重建索引并运行 `near`；十个登莱持久变量均有写入、读取。Tiger 1.19.0 对三个 1.15 日志 `outcome` 报未知字段，已同本版原生文档及实例核对。

## 4. 怎么复测

1. 新开局用登莱，分别试整军和通商。两局都应有「雪国共和」、唯一真正的共和国及原有十年开局修正；读档不重选。山东未得时君主制提案受限。北朝成为共和国或共和军立国后，下一个周脉冲应换成「共和不孤」。
2. 在回山东前经外力改成非共和政体，应有十年权威、威望各 −10%，日志与路线继续。年度抽取有空签；北朝镇压获胜后才可能有流亡者，每次合计 5,000–10,000 名华北人、西北人，间隔至少五年。可对照来源与首都人口。
3. 取得外东北州份后，分别试留都和迁都。留都免费；迁都扣 GDP 的 5%（至少 7,500），新都十年移民吸引 +20%。勘察加行政等级移到新都；登莱持有的勘察加、鄂霍次克改为未整编，两地华北人南迁。取得山东即解锁政体；还都青岛只可执行一次，给二十年基础合法性 +10、10% 效忠派，关闭海参崴选项。
4. 取得华北或华南任一州份，核对日志中的泛民族主义、候选和 75% 提示，以及各自的路线按钮。整军可誓师，持续 24 个月，期满再冷却 60 个月。通商可颁宪一次，共和/其余区域国家关系分别 +30/+15。自行组建 CHI 后先结算原有统一文化事件，再看当前政体的结局；若别国先建则登莱日志失败。

## 5. 遗留问题

未启动游戏。需实机确认 CHI 候选资格、条约口岸作为首都、跨国迁徙、革命换届后回调及政体锁的界面表现。数值均为源码估算；开局 GDP、实际扣款与随机节奏待测。第 2–6 批等作者反馈。
