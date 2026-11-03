from commission_context import *
from datetime import datetime,timezone
# Evidence binding after the final source/text edits.
current=man(C);bm=man(B);changed={p:h for p,h in current.items() if bm.get(p)!=h}
proof=json.loads(read(R/'contract-validation.json'));assert proof['files']==changed
bound=json.loads(read(R/'boundary-cases.json'))
for name,h in bound['candidate_trigger_files'].items():assert sha(C/'common/scripted_triggers'/name)==h,(name,'stale boundary report')
assert json.loads(read(R/'final-validation.json'))['changed']==changed
write(R/'release-notes.md','''# 两司后置建立与边界验证

2026-11-03；父版本a062441。候选commission-boundaries-20261103-a。原版1.13.11/build24799966。STATIC_PASS / ENGINE_NOT_RUN。主目录、Git、远端和备份结果以main-merge.json/git-delivery.json为准。

## 新建立条件

|对象|条件|
|---|---|
|两司共用|USM独立、和平、未参与外交博弈；民主制和开化使命科技；首次筹建或一年间隔已过；TAG未存在、未标记已建立|
|天竺|直辖/直属国在至少12个印度大陆地区持有最大的state；至少3个有实际印度领土的历史土邦直属国，或完全控制至少3个土邦原辖地区；完全控制至少2个莫卧儿腹地|
|莫卧儿腹地|德里、阿格拉、比哈尔、西孟加拉、东孟加拉、孟买；必须整个地区所有owner-state均在直辖/直属国范围，不能只拿土邦边角或暂时占领|
|天竺首府与治理|USM直接拥有马德拉斯的有人人口州片段和至少1级港口；印度直辖地有至少1级政府行政建筑|
|远山|在开普、东开普、北开普、祖鲁兰、奥兰治自由邦、德兰士瓦六地区中控制至少4个地区的最大州；USM直接拥有祖鲁兰有人人口片段及港口，南非直辖地有行政建筑|

依据是原版非洲行政的开化使命后置、莱茵联邦的属地逻辑；12/3/2与4是本MOD本轮平衡选择，不冒称原版数字。现有地图23个印度大陆地区；USM和TRA联合开局只涉及6个（不是按分州重复计7），南非为0。MUG有12个原辖地区，其中极小飞地没有纳入六个腹地清单。

统计外层any_state_region去重；只认所有权与直属关系，间接属国和单纯占领不算。largest-state按原生谓词，不自定义人口/面积算法。三个土邦的征服替代避免先吞并土邦后永久不能建司。首府仍须USM直辖，不能把“满足数量”误作允许强拿属国首都。

筹建日志、决议和按钮共用后置入口；实际effect再核同一建立条件。成功flag与失效条件互斥。既存两司不回收、不重建、不重新领取成果。

天竺成立后划拨范围扩为23个印度大陆地区及锡兰/印度洋领地，只转USM自己持有的片段；原有土邦仍直属USM，第三国领土不动。当前两司是puppet，不擅自让它们收下次级属国。既有六地区筹备迁移保留。有限治理奖励JE撤去重复镇压按钮，常驻行政JE继续保留六按钮。

## 同轮修复的边界

- 19处印度顾问/起义修正移除增加同作用域has_modifier守卫；就绪、暂停、失效和二次清理均不无保护移除不存在修正。
- 援助对象失去最后一个印度州：外交JE失效立即撤顾问和临时加成；月度入口也能处理残留引用。原48个月援助锁保留，不能退出地域再回来刷援助。
- 全局开局回调没有root。新统计函数改为先确认c:USM存在，再比较固定USM与直属关系；国家入口、无root启动和缺USM均有反例。

## 检查分类及结果

- 45个真实trigger AST的资格场景；5个故意修改阈值、比较符、root、完整控制和土邦数量的负例均被检出。
- 23个真实请求/数值AST场景，覆盖缺scope、迟答serial、到期、改政体/宗主、战争、重定向、资金边界；去掉serial检查的负例被检出。
- 7组顾问清理各执行两次，旧源码失败、候选通过；移除一处守卫的负例被检出。另验证失去印度后的月度路由与JE退出两条清理入口。
- 两司共6个建国API结果注入场景：建国失败、宗属失败、成功；检查失败不移交其余州、宗属建立后再移交、第三国州不变、重复点击无变化。
- 326项结构回归、50项强化契约检查，含实际有效文件中原版MUG3营与新增37营，比较符/祖先守卫、地区范围和同一入口检查。
- 实际MCP5次查询、Tiger零新增、两轴复核零未关闭源码问题；最新文件SHA绑定。

旧484项中一些只是“存在该关键字”，不能证明比较方向、真实分支顺序或初始可达性。本轮保留它们作为结构检查，同时新增以上可失败的案例。没有通过简单增加PASS数宣称验证范围扩大。

## 尚未由外部工具证明

Python仅执行所需脚本AST子集和控制流；未知语法报错，缺对象报错，布尔兄弟项按非短路处理。世界数据与经济正值均为明确fixture；分裂州的largest标志由fixture提供，不冒称模拟了引擎判定。

建国API注入不模拟实际人口、军队继承、last-state消失、回调先后和战争；也未逐个注入宗属建立后的set_state_owner引擎失败。真实UI显示、自然外交退让/和平、长期AI经济仍未运行。不能给出“全部游戏边界已实测”或“0BUG”的保证。

未开游戏、未改用户存档。原人口、地图、建筑、人物历史以及用户日本改稿均保留。
''')
write(R/'test-coverage.md','''# 覆盖完整性审计

|层|本轮证据|性质|
|---|---|---|
|资格边界|boundary-cases.json，45场景＋5变异反例|执行真实AST子集，历史归属+显式fixture|
|请求身份与代价|request-boundaries.json，23场景＋serial变异|执行真实trigger/script_value；不运行事件计时器|
|清理幂等与失地退出|effect-boundaries.json，7重复清理及2退出路由|真实effect AST；旧源码反例和guard变异|
|建司阶段顺序|effect-boundaries.json，6创建/宗属结果场景|原生API结果注入，不模拟引擎内部|
|静态源契约|contract-validation.json 50、final-validation.json 326|操作符、祖先条件、有效原版文件、资源和双语|
|加载工具|mcp-final.json；tiger-added.json|真实源码查询与校验器，零新增诊断|
|引擎运行|没有新增|ENGINE_NOT_RUN，用户测试|

结论：已补齐本轮确认缺失的可外测边界，不能把静态/注入式测试称为引擎全覆盖。已识别且仍未覆盖的引擎行为列在release-notes.md。当前源码变化只绑定当前报告；旧484/326计数不独立代表测试质量。
''')
# Task and handoff.
write(C/'.scratch/debug-release/issues/26-commission-boundaries.md','''# 26 两司后置门槛与边界测试

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [交付与测试范围](<'''+(R/'release-notes.md').as_posix()+'''>)

## Result

参考原版非洲殖民行政/莱茵联邦，增加开化使命与直辖/直属地区规模、印度土邦和莫卧儿腹地门槛；所有入口一致，地区去重。修复修正清理/最后印度州退出/无root开局统计，保留实际历史与已建两司。45资格、23请求、7清理、6建国结果场景及7变异反例通过，另有50契约/326结构检查、MCP5与Tiger零新增。未开游戏；实际合并以报告JSON为准。
''')
p=C/'.scratch/debug-release/map.md';write(p,read(p)+'\n## 最新：两司后置与边界补测（2026-11-03）\n\n[26 建司门槛与测试](issues/26-commission-boundaries.md)收紧天竺/远山条件，修复清理和启动scope，并补可检出错误的AST边界与反例。任务25的484项不再被表述为全部行为通过；精确覆盖与引擎缺口看任务26报告。\n')
p=C/'.scratch/india-development/map.md';write(p,read(p)+'\n## 建司条件修订：2026-11-03\n\n[任务26](../debug-release/issues/26-commission-boundaries.md)取代初版两州门槛：天竺12大陆地区＋3土邦/征服替代＋2完整腹地；远山4南非地区，两者均开化使命后置。只有直辖地划拨，属国参与计数但不被吞并。\n')
for rel in ['references/validation.md','references/active-work.md']:
 q=R/'skill-before'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/rel,q)
p=S/'references/validation.md';s=read(p);marker='## hidden_effect 的真实边界';insert='''## 可失败的边界检查（2026-11-03）

测试计数不代表覆盖率。判断条件测试要保留操作符、数值、作用域祖先与执行顺序；只查“army_size和1存在”会让<1被误改成>1仍通过。新增门槛至少有开局、差一档、刚好满足、对象转属/消失和已完成重入案例；对旧源码跑红，再对阈值、比较符、缺守卫作内存变异，确认检查真的失败。

需用外部AST子集执行时，记录支持的语义，未知节点必须报错；布尔兄弟项不能假设短路，trigger_if按分支处理。全局启动没有root，测试不能一律注入当前country来掩盖调用上下文。API结果注入只能证明脚本控制流，不能代替实际建国、转地、战争或人口引擎。

报告绑定最终文件SHA；测试后编辑了条件或本地化，按变化重跑或保存可核的AST等价链。地区门槛按state_region去重，直辖与直接/间接属国区别、共享分州、占领不等于所有权均列入案例。原生largest-state算法未证实就作为明确fixture输入，不能用province数量假装引擎语义。

实际反例与证据：WORK/reports/commission-boundaries-20261103/boundary-audit.md、boundary-cases.json、effect-boundaries.json、request-boundaries.json。测试仍为STATIC_PASS，未运行游戏。

''';assert marker in s;write(p,s.replace(marker,insert+marker,1))
p=S/'references/active-work.md';s=read(p);write(p,'''# 当前交接：两司门槛与边界补测

Updated: 2026-11-03。当前任务26：主MOD .scratch/debug-release/issues/26-commission-boundaries.md；报告WORK/reports/commission-boundaries-20261103/。父提交a062441，两司改为扩张后建立，补资格/请求/清理/建国故障边界测试。STATIC_PASS，未开游戏；主MOD与远端最终结果以main-merge.json/git-delivery.json为准。任务25印度已实施，不再是纯方案。旧记录按时序保留如下，不能用其“计划中/当前任务23”覆盖本节。

'''+s)
print('Final evidence binding, task26 and skill test rules prepared')
