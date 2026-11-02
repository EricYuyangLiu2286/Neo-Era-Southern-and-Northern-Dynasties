from qin_stage_context import *
def before(p):
 q=R/'documentation-before'/p.name
 if p.exists() and not q.exists():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
def append(p,s):before(p);write(p,read(p).rstrip()+'\n\n'+s.strip()+'\n')

other=json.loads(read(R/'other-japan-design-sources.json'))
append(R/'japan-canon.md','''## 根任务补充核验：日本专门设计文件

最新用户原话明确要求研究三个玩法分支：“统一的日本+九州，统一的日本（无九州），分裂三国”。因此三种玩法局面属于author_explicit的本轮目标；具体条件、法律和剧情仍是提案，不将PPT的一条未来线覆盖其余分支。人物冲突已获用户明确允许以当前游戏为准，本轮方案沿用林汉涵/JAP/JTK/JIM。

前述未读日本设计文件已由根任务补读，来源及完整段落/图节点存other-japan-design-sources.json：

- `计划文件（相关项目）/Japanese map brief.docx` 开头明确论述AD220–280的邪马台、弥生/古坟时代，并以EU4/CK2术语说明政治制度。它是古代题材设计，不作为1836文化、宗教或君主制度的依据，不将稿内历史论断当本轮已考证事实。
- `Japanese Mission Overhual.drawio` 有“国主攻略—上洛面圣—统一日本”、大和圣族、关东管领、北海/琉球/朝鲜/南洋等主题节点，后段延伸至印度、西域、波斯。图中没有Victoria3的触发器或当前丰臣三国条件。可作征服与海权主题备选，不直接成为本轮必走路线或开局claims。
- `朝鲜任务树.drawio` 包含南北统一、三韩水师、结好九州藩、事大/朝贡、书市/文字/学校及多方向外交发展。它提示朝鲜具有自己的统治和建设目标，不能在日本方案中仅作为一块待吞并土地。仅采用主题，未搬入别的游戏语法或未读的PDF。

上述补读不改变PPT和地图证据的年代边界。日本政治/经济方案详见WORK/plans/two-empires/20261102-japan-development-design.md，未接入游戏。
''')
# Correct only a reference range; the implementation and its audit are unchanged.
p=R/'qin-stage-design.md';s=read(p).replace('07_japanese_religion.txt:1–96','07_japanese_religion.txt:1–118');write(p,s)

write(R/'release-notes.md','''# 日本研究与西秦日志分阶段

日本研究基线：a7b445b；本机游戏1.13.11/build24799966。日本玩法未改；原版、PPT、旧地图和废弃工程只读。西秦阶段修正另有独立候选qin-journal-stages-20261102-a，实际备份/合入/远端保存见main-merge.json、git-delivery.json。

## 日本研究成果

- native-japan.md：15日本JE、124事件、112人物模板及经济/法律/继位调用链；125源码哈希复核，原版经济和人物逐项有来源。
- current-mod-japan.md：当前实现、72源码指纹、政治表态与军事承诺区分、旧孤立事件、三国恢复与林摄政、人口/建筑/PM/编制、朝鲜和对外关系。
- japan-canon.md：原始PPT、Word、1835/1936/1950地图、HOI4原文件；区分1836背景和未来线。另核日本/朝鲜设计drawio与古代地图brief，后者不用于1836设定。
- 实施提案：WORK/plans/two-empires/20261102-japan-development-design.md。三种疆域局面交叉幕府改革、军事集权、民主化；分阶段日志、朝鲜及吴/CNE/HUS关系、产业分工、人物继承、文件结构和实施顺序。尚未实施日本新内容。

关键事实：当前JAP35,594,072人口，朝鲜两州8,669,114；九州保留2/12省色，尚有贸易入口。完全无九州和只失大部九州不是同一经济状态。原版锁国与幕府法退出、人物JAP硬绑和大名/武士global标记均需专门适配。原作者flavorJAP事件逐字保留；旧.14/.17/.19缺普通入边不能当当前正常路线。

## 西秦实际修正

|阶段|日志|
|---|---|
|开局|西部帝国的自救、安国之策、军府之议、帝国的稳定|
|朝议结算后|伊犁的朝议（三权）、恢复故土；仍分别受原有资格和终局锁控制|
|提前重返西北|自己或附属完整控制河西/甘肃/西安/陕北任一地区，可提前开启恢复故土|
|危机出现后|文化团结首次低于25，开启羌种暴动；维持既有规则|

旧档已有三权或故土日志会登记opened标记并保留；不会回退既有进度或强制隐藏玩家已在玩的内容。未解锁仅表示尚不可进入，不会因此永久封存或领取结束奖励。新档和正常后继按新阶段运行。

共5个玩法脚本修改：阶段谓词、bootstrap解锁、朝议结算时登记、两个后继JE的可见/进入条件。原来的invalid/完成、奖励、人物、经济和文化/战争逻辑不改。24项有限AST条件/迁移测试通过（原版候选在开局等4场景失败），4项实际MCP源码查询通过，Tiger新增0；Standards/Spec两轴均无可行动问题。仅静态与源码验证，未启动游戏。

### 保存与范围

研究结论、计划和证据保存在WORK及私有源码仓库development；主MOD只带阶段修正和任务文档。正式游戏包不含QA、研究截图、检查器或原版/工坊素材。原有游戏数据与日本机制保持。新日本玩法的开发顺序已经记录，研究完成不等于日本新路线已经上线。
''')

write(C/'.scratch/debug-release/issues/18-qin-journal-stages.md',f'''# 日本研究与西秦日志阶段

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [{R.name}](<{R.as_posix()}/release-notes.md>)

用户要求研究原版、日本现有实现及旧设定，并检查西秦日志不应全开局出现。日本交付研究及实施方案，未修改玩法；西秦五脚本后置三权/恢复故土，保留已开启旧档。24有限条件检查、4MCP查询、Tiger零新增、双轴审查完成；ENGINE_NOT_RUN。

研究后续入口：`.scratch/japan-development/map.md`。实际主MOD/Git保存看报告目录main-merge.json、git-delivery.json，不将研究方案标作日本功能完成。
''')
p=C/'.scratch/debug-release/map.md';write(p,read(p).rstrip()+'''\n\n## 最新：日本研究与西秦阶段（2026-11-02）

[18 日本研究／西秦分阶段](issues/18-qin-journal-stages.md)：三份原始来源研究与日本三局面实施方案已保存；日本新玩法尚未实施。西秦开局保留朝议三日志与文化团结，三权/恢复故土后置，旧档已开启内容保留；24条件检查、MCP4与双轴复核通过，未开游戏。日本后续见[开发入口](../japan-development/map.md)。
''')
write(C/'.scratch/japan-development/map.md',f'''# 日本开发入口

Record: decision
Type: research
Status: resolved
Assignee: root
Blocked by: none

## Destination

支持统一含九州、统一无完整九州、三国并立三局面；军政、幕府改革、民主化分别有可玩过程，衔接朝鲜与吴/CNE/HUS，日志按阶段开启。

## Decisions-so-far

原版、当前MOD和旧设定已分别研究，见 [{R.name}](<{R.as_posix()}/release-notes.md>)。[日本实施方案](<{(W/'plans/two-empires/20261102-japan-development-design.md').as_posix()}>)为当前提案；原始数据和日方角色以当前游戏优先，旧图不直接改1836边界。

## Next work

先适配幕府法退出/继位/global变量，再拆分国内统一与九州归还，随后贸易及三国立足、政治议程、朝鲜/外交、产业后继。具体门槛与奖励在相关模块实施前对原版定量核验。

## Not yet implemented

日本新政治、独立/再统一、朝鲜及HUS/CNE响应尚为提案。本轮只有西秦阶段修正写入玩法。

## Out of scope

原版/工坊/旧HOI4工程只读；不开游戏；不重画日本地图、不重配人口、不取消既有崩溃/恢复/林摄政，不提供自动玩家救援。
''')

plan=W/'plans/two-empires/07-japan.md';before(plan)
s=read(plan).replace('状态：现有日本政权人物和事件待接入完整危机；日本州界保持不改。','状态更新：2026-11-02已核当前日本的参战、分封、恢复与林摄政实现；本页其余旧提纲保留。最新研究与后续提案见20261102-japan-development-design.md，日本州界保持不改。',1);write(plan,s)
append(W/'plans/two-empires/20261102-qin-persia-implementation.md','''## 日志阶段修订（2026-11-02）

用户明确不是所有日志开局出现。新档开局只有朝议主从三JE与团结；三权、恢复故土在朝议结算后解锁，提前完整收回西北四目标之一可先开故土。已有旧档后继JE保留，不回退进度。available和永久eligible分开，未解锁不封存；见WORK/reports/japan-research-20261102/qin-stage-design.md及任务18。
''')
append(W/'plans/two-empires/00-master-plan.md','''## 日本三局面研究与西秦阶段（2026-11-02）

研究与下一步方案见20261102-japan-development-design.md；源码/原稿证据在WORK/reports/japan-research-20261102。日本新内容未实施。西秦后继日志已按任务18制作阶段修正并外部核验，实际交付状态见同目录release-notes/main-merge/git-delivery。
''')
append(S/'references/journal-text-contract.md','''## 阶段可进入与永久结束分开

跨阶段JE分别定义available（现在允许开始）与eligible（国家/制度仍允许继续）。未达到后继阶段不能被通用bootstrap当作永久invalid而提前写archived。当前已活动的旧档JE可在维护effect登记opened标记；不要把自己的has_journal_entry写进possible形成首次进入自锁。后继已解锁不因暂时丢失触发地重置，完成/封存锁仍独立阻止重领。西秦五脚本修正及原版“维新完成标记→神佛分离决议→宗教JE”来源见WORK/reports/japan-research-20261102/qin-stage-design.md。
''')
append(S/'references/narrative-context.md','''## 日本资料专题

研究日本丰臣/德川/天皇、三国、九州或朝鲜时，先读WORK/reports/japan-research-20261102/{native-japan,current-mod-japan,japan-canon}.md。PPT27是1847–1852未来线（三日本政权＋吴直辖），1936/1950地图更晚；最新用户三局面目标不等于唯一正史。当前游戏林汉涵等名优先，异文保留研究说明。原版锁国九州入口、幕府法退出、JAP/DLC硬绑和大名/武士global标记需逐项适配，不能整套移给三个新国家。开发提案在WORK/plans/two-empires/20261102-japan-development-design.md，未实施部分明确分列。
''')
before(S/'references/active-work.md')
write(S/'references/active-work.md',f'''# 当前交接：日本研究与西秦日志阶段

Updated: 2026-11-02。父版本a7b445b，候选qin-journal-stages-20261102-a。[任务18](<{M.as_posix()}/.scratch/debug-release/issues/18-qin-journal-stages.md>)与[交付说明](<{R.as_posix()}/release-notes.md>)为入口；实际主MOD/Git保存看同目录main-merge.json、git-delivery.json。旧交接在documentation-before。

日本：原版15JE/124事件/112角色、当前MOD人口产业/人物/分封/旧失联事件、PPT/旧地图/HOI4专题研究与三局面方案完成。新日本政治/统一/朝鲜玩法仍是提案，入口为.scratch/japan-development/map.md。

西秦：新档朝议3JE＋团结开局；三权/故土后继，提前收回西北可先开故土，旧档已开启JE保留。五玩法脚本、24有限条件检查、MCP4、Tiger零新增、两轴复核；未开游戏。其余原有数据/日本机制不改。

全局历史资源缺项和旧验证登记仍看任务17报告；本轮不将它们清绿。不要重跑一次性构建脚本覆盖后续修订。源资料有年代/名字冲突时按当前用户要求与实际游戏对象处理，不把旧世界图强套开局。
''')
print('Research supplement, proposal links, task indexes and stage handoff recorded.')
