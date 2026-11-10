# 77 新游戏目标推荐国家

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [名单及引用检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-objective-countries/static.json>)

## 现象与期望

四个目标一直读取原版推荐 tag。作者实测新组合显示 objective_* 键名；经济第三位最终确认莫卧儿 MUG。作者确认四栏名单，霸主第三位改为奥斯曼，另写普鲁士介绍。

## 原因

选国界面读目标定义的 recommended_tags。课程由目标 on_start 启动，日志由各 objective_subgoal 的 on_start 发放。

## 改动与核对

- common/objectives/00_objective_tutorial.txt 与 01_player_objectives.txt 基于 1.15.0 同路径文件，仅四处名单不同。
- 中英文 ce_country_flavor_text 各新增 SWE、PRU、TUR 三键，后依作者意见追加 RUS、USA 两键并替换入门第三、四位。所有入选国双语非空。原版四个首课、子目标、最终子目标及关联日志的引用均已核对。
- 入门首课 lesson_basics 同时启动随机科研。建设子目标要求有可扩建的闲置农场。SWE 斯韦阿兰、YN1 新南威尔士、RUS 考纳斯、USA 纽约均有对应农场。检查的四国开局科技历史是已研科技。和谈教学要求已派将上前线且正在战争，之后解锁提升排名；远南自治领外交受限。
- 经济首课 economic_dominance。sg_expand_goods_production 选择可扩建铁矿或煤矿。HUS 科罗拉多煤、PER 呼罗珊铁、MUG 西孟加拉铁煤、阿格拉铁矿、GBR 兰开夏煤铁均有建筑记录。最终要求扩展市场、降低成本，并通过提高出口额或利用优势之一，最终日志要求本国 GDP 超过世界的四分之一。
- 霸主首课 hegemon，殖民法子目标无开局门槛，依国家排名设变量并发日志。结盟及取得属国以后续前置解锁，最终由排名支线之一进入，要求含属国占世界人口至少四成。奥斯曼另有整军与东进国别日志。
- 平等社会首课 egalitarian_society。鼓励自由思想及解放奴隶均可进入初始判定，已有禁奴法或变体能完成废奴日志。妇女儿童与废奴两项目完成后，还须具备公共教育、多元文化、言论保护等具体法律才会发最终日志；结案要求农民占比低于一成、平均生活水平至少20、识字率至少九成。

- 中英文 nesnd_objective_countries 各补 28 个原版未提供的组合键，标题引用开局国名，正文引用已有国情。原检查只验证国情键，遗漏了卡片的两层组合键。16 个不同 tag，每种语言 32 个卡片键及其引用均已核对。[复查记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-objective-card-keys/static.json>)。

## 复测

重启后浏览四栏，逐栏直接开一国核对首课和首条对应日志。霸主组选奥斯曼，再从霸主的「选择任意国家」及沙盒分别选奥斯曼，对照目标课与国别日志。普鲁士另在选国地图核对介绍。

## 遗留

待作者实测界面、首日实际扩建资格与日志触发时点。静态检查未发现需要覆盖目标日志的国别冲突。
