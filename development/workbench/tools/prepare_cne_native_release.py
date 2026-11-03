from cne_native_context import *
from collections import Counter

tests=json.loads(read(R/'regression-candidate.json'));mcp=json.loads(read(R/'mcp-final.json'))
assert tests['status']==mcp['status']=='PASS'
assert not json.loads(read(R/'tiger-added.json'))
patch=json.loads(read(R/'patch-files.json'));current=man(C)
for rel,h in patch.items():assert current[rel]==h==tests['source_files'][rel]
old=json.loads(read(W/'reports/observer-logfix-20261103/audit-candidate.json'))
new=json.loads(read(R/'graph-audit.json'))
assert {k:v for k,v in old['summary'].items() if k!='mod'}=={k:v for k,v in new['summary'].items() if k!='mod'}
def norm(x):
    if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
    if isinstance(x,list):return [norm(v) for v in x]
    if isinstance(x,str):return x.replace(old['summary']['mod'],'<MOD>').replace(new['summary']['mod'],'<MOD>')
    return x
assert Counter(json.dumps(norm(x),sort_keys=True) for x in old['issues'])==Counter(json.dumps(norm(x),sort_keys=True) for x in new['issues'])
dump(R/'graph-audit-comparison.json',{'status':'PASS','identical_effective_graph':True,'unchanged_warnings':new['summary']['issues'],'no_new_issues':True,'comparison':'Normalized issue multiset, preserving duplicate counts'})

write(R/'review.md','''# 两轴审查

基点：a70eb1257795372105751b1e257a0a21dc83638e / pre-change-cne-time-native-ban-20261103T124341Z。范围：本轮12个玩法/文本文件；spec.md；原版来源、文本证据。

## Standards

独立代理 cne_native_standards_review。最初发现逐键文本对读证据不足（P2）；现已补齐八键原文/候选/结论、作者样本键/行/SHA及原始来源哈希，复核后剩余0。三个海况均有实际日志定位，cyclone是00_naval_battle_conditions.txt:119。未更改原版或其他MOD。

## Spec

独立代理 cne_native_spec_review。剩余0。核对保序AST：仅五个事件、两个赔款权重和三个海况受停用；既有其余事件、namespace及对象不变。CNE复用既有年龄变量及退出守卫，保持旧存档终态、不重置数值；意大利仅方案。

## 最终格式与用户补充

审查后仅清理新复制原版文件的行尾空白（前后AST完全一致），23检查、Tiger零新增和MCP5均已重新绑定最终源码SHA。追加完整DLC环境约定并撤除意大利无DLC替代路线，属于计划/技能变化，未新增玩法代码。没有启动游戏；本轮结论为STATIC_PASS。
''')
write(R/'release-notes.md','''# CNE拖延压力、原版故障停用与意大利方案

父提交a70eb125。12个玩法/文本文件，2个修改、10个新增，无文件删除。验证状态STATIC_PASS；本轮没有开游戏或改动1866终档。实际合入/远端指纹见main-merge.json及git-delivery.json。

## CNE

没有固定年限到期失败；既有失君主制、信心0、政变、原生革命/分离战争、极端危机可失败，领土少于4州失效。失序满值并非单独失败条件。1866终档已冻结/结算，进度28.2、失序12.5、信心1000、月份11，主从日志均不活跃；最符合现存标记的解释是AI永久议止发生于首次年扣之前，具体点击日期未记录。未重新打开旧日志。

新增年耗25*floor(max(0,months)/60)：基础年耗在0/5/10/15年阶段分别25/50/75/100，此后每五年继续加25。进度条明细显示“改革久拖未成”。原有战争、改革、营产消耗与执政恢复、破产、一次暂缓保持。算术场景见confidence-cost-model.json，非引擎仿真或固定失败年份。

## 原版故障

关闭原生波兰请求按钮/.1/.2、阿曼分裂JE/zanzibar.1、movement_events.6及coup_aftermath_events.1；保留本MOD波兰、其它同文件事件、既有国家/领土。整合主义仅关闭两个错scope赔款权重。海况cyclone/rough_waters/tropical_storm禁用并去掉随机求值，三类海况不再产生其原有效果；其它海况及核心海战逻辑保持。海战本地化仅修不存在/不可求值的方法调用。重复add JE不处理。

JE和按钮使用已证REPLACE。事件等采用同路径覆盖并保留非目标定义；没有假定所有数据库均支持REPLACE。整文件覆盖绑定当前1.13.11/build24799966，升级必须对照来源SHA。无定位的command_values未知国家、引擎断言和外部资源冲突仍未解决，不能宣称整MOD零错误。

## 检查与设计

23定向检查、MCP5查询通过；相对同原版覆盖范围的Tiger对照零新增；数据图及原有132省份重复归属/4建筑投资警告不变；两轴审查剩余0。候选独立备份，正式包排除QA/开发工具。

意大利调查综合PPET、当前MOD、原版统一/公司链、RAHF、More Unique Companies和1866终档；方案以既存北方共和国及法国宗主体系、两西西里竞争、教宗地位与统一后整合为中心。未实施意大利路线或改地图。详见italy-research-plan.md。

按用户新增约定，默认完整DLC环境，不设计缺DLC替代路线、不列入验收阻断；真实引用、生命周期和人物边界照常核查。规则已进入NESND技能system-design-and-plans.md。
''')
issue='''.scratch/debug-release/issues/28-cne-time-native-ban.md'''
write(C/issue,'''# 28 CNE拖延压力、原版故障停用与意大利研究

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [交付与限制](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/cne-time-native-ban-20261103/release-notes.md>)

## Result

CNE新增每满五年年耗信心增加25，既有失败/退出和其它消耗/恢复不变，不重开已结束的1866改革。原版仅停已定位故障入口与目标定义，CE波兰、历史数据及其他MOD保留。23定向检查/MCP5/Tiger零新增/数据图不变/两轴审查0剩余；未开游戏。候选备份、主MOD与Git结果看报告candidate-backup.json/main-merge.json/git-delivery.json。

[意大利研究及分阶段方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/cne-time-native-ban-20261103/italy-research-plan.md>)已完成，玩法尚未实施。按用户新增约定，默认完整DLC环境，不为缺DLC增加替代分支；规则写入技能system-design-and-plans.md。无位置引擎报错与外部资源冲突仍未解决；duplicate add JE按用户要求不处理。
''')
p=C/'.scratch/debug-release/map.md';s=read(p)
s+='''
## 当前交付：CNE拖延压力、原版故障停用与意大利研究（2026-11-03）

[28 CNE与原版故障](issues/28-cne-time-native-ban.md)：信心按完成的五年阶段增加年耗；原版故障入口定点关闭，保留本MOD波兰及历史数据。23外部检查/MCP5/Tiger零新增/数据图不变/两轴审查0剩余，STATIC_PASS，未开游戏。意大利方案已完成、未实施；按完整DLC环境规划。

此前观察者运行已于1866.1.15暂停，完成两机位截图、存档字节核验并正常关闭。终档与完整日志在WORK/reports/observer-finish-20261103/；下次恢复不得沿用上方历史“游戏仍运行”的描述。实际部署和Git指纹见WORK/reports/cne-time-native-ban-20261103/git-delivery.json。
'''
write(p,s)
p=S/'references/active-work.md';s=read(p)
header='''# 当前交接：CNE拖延压力、原版停用与意大利方案（2026-11-03）

当前任务28，主MOD .scratch/debug-release/issues/28-cne-time-native-ban.md；报告WORK/reports/cne-time-native-ban-20261103/。CNE每满五年增加年耗25，既有成功/失败及恢复不变，已结算旧日志不重开。原版五事件、两个入口、两个无效权重和三海况定点停用；海战本地化方法修正。23定向检查、MCP5、Tiger零新增、数据图不变，两轴审查各0剩余，STATIC_PASS。主MOD/main/远端指纹以main-merge.json和git-delivery.json为准。

意大利研究与方案已完成，尚未实现新路线；入口同报告italy-research-plan.md。新用户约定：一般不考虑DLC缺失，按完整DLC环境设计，见system-design-and-plans.md。

观察者旧局adfc317已于1866.1.15完成两机位截图、存档核验和正常退出；没有活跃的游戏测试授权待执行。本轮未开游戏、未改终档。CNE该局主日志11个月后已冻结结束，信心1000是保留值，不代表1866仍在持续改革。以下是历史断点，仅供追溯。

'''
write(p,header+s)
dump(R/'final-validation.json',{'status':'STATIC_PASS','targeted_checks':23,'mcp_queries':5,'tiger_added':0,'graph_identical':True,'standards_findings':0,'spec_findings':0,'gameplay_files':patch,'engine_verified':False,'DLC_assumption':'Full installed DLC environment; no missing-DLC alternate routes'})
print('Graph unchanged; review, release, task and skill handoff written')
