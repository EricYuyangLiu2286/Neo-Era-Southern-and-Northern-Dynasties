from cne_native_context import W,M,S,read,write,sha,man,dump
import shutil,difflib,re
R=W/'reports/italy-lombardy-correction-20261103'
plan=W/'reports/cne-time-native-ban-20261103/italy-research-plan.md'
baseline=__import__('json').loads(read(R/'baseline.json'))
old=read(__import__('pathlib').Path(baseline['backup'])/'italy-research-plan.md')
s=read(plan)
anchor='## 五、两个参考MOD具体取用与排除'
assert s.count(anchor)==1
gar='''### 加里波第及原生统一剧情：局部适配计划

用户本轮提出检查加里波第（Garibaldi）内容。先区分三层：人物模板与流亡/招募、`garibaldi_events.1—4`个人事件、`italian_unification`国家政治事件。后者使用`votp_garibaldi`视频并不意味着需要加里波第本人在场。完整入口、ID、行号与作用域证据见[加里波第流程核查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/italy-lombardy-correction-20261103/garibaldi-chain-audit.md>)。以下为实施计划，尚未改代码。

|环节|已查到的现状|计划与边界|
|---|---|---|
|开局入口|原版`common/history/global/00_global.txt`和本MOD的`ce_global.txt`都向PNI排同一`.1`事件，均为6天后；存在两个排程入口，但未证明双生人物|收敛成单一有效入口，先查既有角色及事件队列。PNI经历保留为待核的背景适配，不因亲法伦巴第起点就强制将人物开局搬到LOM|
|人物身份与存活|模板`garibaldi_character_template`，`garibaldi_var`、全局存活标记及死亡清理；人物可在国家或流亡池中|保留既有身份/肖像和合理流亡招募。实施时查全部国家、流亡池、死亡与退役状态，不能清全局变量后盲目重刷；不复活、不抹掉已有经历|
|到来与转赴战场|月事件`.1`按战争/政治条件来援，`.2`离开或转赴意大利战事；筛选并不只针对奥地利|对法合作、实际敌友与既有任职分别判定。允许援助法国支持的意大利战争，也保留因具体政治矛盾拒绝政府或离开的选择；民族主义本身不等于反法，亦不强制人物与佩佩意见一致。选择、展示与执行应使用同一战事目标|
|志愿军事件`.3`|外层只要求本国有带`garibaldi_var`的角色，保存人物时却另要求general；取消条件也未完整验证所存角色|修齐资格、取消和选项效果的同一对象检查，尤其仅以agitator招募时。这是源码前置不一致，能否实际触发缺scope还需定向验证；不能先报成已复现崩溃|
|激进派、改政与吞并|`italian_unification.4`在革命/激进派等条件下可流放统治者并改议会共和和选举制，不依赖加里波第在场；和平兼并与形成ITA另属国家链|按伦巴第已有共和国改写政治诉求，区分扩大选举权、军方权力及统一领导权；保留真实革命和失败可能，不能凭视频或民族主义直接赶走佩佩。兼并/形成仍依实际资格，不把领袖剧情当免费统一|
|圣马可分离及鼓动按钮|`on_secession_start`相关`.7/.8`并非只限奥地利；非意大利主文化的法国也可能进入。鼓动按钮资格与随机执行的关系筛选存在不一致，当前属国LOM通常看不到该按钮|改写奥地利专属叙事，核实际宗主与战争；和平合作阶段不默认削除法方关系。统一按钮选择与执行筛选闭合，防止独立后仍亲法的路线被随机误伤；不取消有真实冲突的分离诉求|
|视频与文案|`votp_garibaldi`是多个事件的媒体资源|按场景选择保留或更换视频、文字，不用删除人物解决国家事件问题，也不因为没有该人物就判定视频引用失效|

**最小实施顺序：**先查人物和排程唯一性、补志愿军角色前置；再把战争目标与亲法合作路线接上；最后适配国家改政、圣马可分离和原生统一立场。只替换受影响的ID或触发块；事件覆盖方式仍须遵守实际数据库支持。复用原生模板、月脉冲与流亡机制，暂不另造完整“加里波第系统”。

**人物定位提案：**佩佩代表现有亲法民族主义政府；加里波第可承担志愿军动员和更广泛公民参与的诉求，与政府在军队指挥、社会改革或行动时机上发生分歧。两人可以合作，分歧也可能发展成政治对立；不把加里波第预设为反法领袖、佩佩继承人或自动推翻政府的工具。马志尼和拟议虚构人物各保留自己的作用。

**专项验证清单（实施时）：**全新局两入口、已有角色在LOM/外国/流亡池、仅agitator无general、死后/退役/1862年后、两个同时存在的意大利战场、亲法且赞成统一、法国为敌、佩佩仍执政/已更替、LOM→ITA、目标吞并或战争提前结束、旧档已有事件队列；分别验证唯一人物、事件可取消、预览对象有效和一次性结算。全DLC环境不增加缺DLC分支。本次只做源码调查与方案，没有实施或引擎验收。

'''
s=s.replace(anchor,gar+anchor)
write(plan,s)
issue=M/'.scratch/debug-release/issues/28-cne-time-native-ban.md'
write(issue,read(issue)+'''
## 作者纠正：伦巴第与加里波第计划

2026-11-03：LOM开局为法国主导的伦巴第共和国，佩佩为历史人物挪用的亲法意大利民族主义者。现有意大利方案已局部修订：亲法整合为开局政府优先方向，自主/反法转向需要具体冲突；条件动态名不再列为开局错误。经济调查、参考MOD机制及统一后治理保持。另完成加里波第人物/事件/国家统一链核查，列排程唯一性、志愿军角色前置和改政/吞并适配计划。

本次为文档修订，NOT_APPLICABLE（游戏验收）；游戏脚本未改、未开游戏。证据：[修订核查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/italy-lombardy-correction-20261103/validation.json>)及[加里波第流程](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/italy-lombardy-correction-20261103/garibaldi-chain-audit.md>)。
''')
p=M/'.scratch/debug-release/map.md'
write(p,read(p)+'''
意大利方案最新纠正：LOM是法国主导的伦巴第共和国，佩佩为亲法民族主义历史人物挪用；以法国支持下的整合为优先方向。新增加里波第全链核查及局部替换计划，尚未实现；任务28追加记录，证据WORK/reports/italy-lombardy-correction-20261103/。游戏脚本未改。
''')
p=S/'references/active-work.md';t=read(p)
needle='意大利研究与方案已完成，尚未实现新路线；入口同报告italy-research-plan.md。'
assert t.count(needle)==1
t=t.replace(needle,needle+'作者随后纠正：LOM为法国主导的伦巴第共和国，佩佩是亲法意大利民族主义历史人物挪用；方案已据此局部修订，以亲法整合为开局政府优先方向。加里波第人物/事件/国家统一链已另核，最小适配计划见WORK/reports/italy-lombardy-correction-20261103/garibaldi-chain-audit.md，尚未改游戏脚本。')
write(p,t)
(R/'lombardy-plan.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='previous-plan',tofile='revised-plan')),'utf-8')
v=__import__('json').loads(read(R/'revision-scope.json'));v['plan_sha256']=sha(plan);v['garibaldi_audit']='source checked; adaptation planned, not implemented';dump(R/'revision-scope.json',v)
print('Plan, Garibaldi section and task handoff updated; pending document/link checks')
