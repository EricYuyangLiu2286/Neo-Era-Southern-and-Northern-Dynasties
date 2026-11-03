from cne_native_context import W,M,S,read,write,sha,man,dump
from pathlib import Path
import re,json,shutil
R=W/'reports/france-politics-plan-20261103'
b=json.loads(read(R/'baseline.json'));backup=Path(b['backup'])

p=R/'party-legitimacy-source.md';s=read(p)
anchor='## 核心结论'
assert s.count(anchor)==1
s=s.replace(anchor,'''## 作者最新约束（本报告建议的适用边界）

2026-11-03：常规政治目标采用相关IG执政＋合法性至少50；高于50只用于明确的困难目标。JE、决议、按钮不得检测指定党派组合、成员数或同党关系，也不能用隐藏条件或AI权重变相要求组合。以下党派成员/评分研究属于机制和党派定义的开发背景，不是任务达成条件；本轮方案优先沿用现有党派，未实施新党或强制分配。

'''+anchor)
s=s.replace('法国“某 IG 入阁”条件必须连同整党组成、投票法及修正、选举信任度、党鞭、执政势力、政府实体数和当前法律立场一起审查。','设计者理解“某 IG 入阁”的难度时，应考虑投票法、选举信任度、党鞭和整党组阁的原生后果；JE实际只检查所需IG执政与合法性50，不加入党派组成、政府实体数或同党成员门槛。')
s=s.replace('以下是研究导出的建议约束，不是已经实现的功能。','以下是研究导出的建议约束，不是已经实现的功能。其中党派定义/刷新条目仅在以后确需修改党派时适用；本轮不增加党派设计任务。')
s=s.replace('3. 原生组阁条件写“目标IG及其整党能执政”；玩家条件检查可聚焦目标IG，但代价、提示与蓝图应承认同党成员同行。若故事只要求阵营支持而不要求政府席位，采用独立剧情支持条件，避免把任命人物误当组阁。','3. 常规政治目标只检查目标IG执政及合法性至少50。禁止检测党派组合、党内人数、同党关系和具体组阁排列；原生整党规则由引擎负责，不再叠加任务条件。若故事只要求支持而非政府席位，不强加执政门槛。')
s=s.replace('8. 合法性门槛围绕真实档位设置，常规执政设计以至少25避免运动立法强依赖，50减少低档压力，75以上改善效忠；这是设计候选目标，不是强制保玩家成功。故事允许少数政府/低合法性，但须有可读代价与可操作恢复路径。','8. 常规执政目标按作者要求采用50。75或90仅是原生较高档位，不能据此升级常规任务门槛；只有有意困难的目标才另设更高值，并说明可控手段、期限、其他前置和回报。低合法性通常暂停相应行动，不自动判整个后继路线失败。')
s=s.replace('先完成外部源码检查，冻结候选后只对未决引擎语义做集中测试；本轮未执行下列实机测试。','以下是未来实际修改对应层时才运行的开发验证，不是游戏任务条件；党派定义未改时不为法国JE另跑整套分党测试。本轮未执行实机测试。政治目标必须补查49/50/51以及相同执政/合法性而党籍不同的情况，确认没有隐藏组合门槛。')
write(p,s)

p=S/'SKILL.md';s=read(p)
needle='6. 新内容和改造已有系统先按 [系统设计与分支计划](references/system-design-and-plans.md) 建立依赖图与持久计划，统一评估开局、中期和终局。'
assert s.count(needle)==1
s=s.replace(needle,needle+'涉及政治日志、IG执政、党派或人物/运动传播时，先读[政治目标与难度](references/political-design-and-difficulty.md)。')
write(p,s)

p=W/'reports/observer-finish-20261103/canon-and-routes.md';s=read(p)
a=s.index('### FRA：兑现波拿巴繁荣，再决定帝国的政治形状');z=s.index('### HUS：',a)
s=s[:a]+'''### FRA：繁荣、宫廷与外省、共和分配

2026-11-03修订：[当前法国详细方案](../france-politics-plan-20261103/france-development-plan.md)已结合RAHF人物/地方运动传播、原生党派与合法性补全。原有波拿巴及王党取得政权的日志继续负责前期，不再新造平行争位系统。

- 波拿巴延续工业、就业、社会改善与帝国承诺，将地方运动、职业激进派和人物选择接到现有稳定因素。
- 波旁/奥尔良中期采用“宫廷与外省”：巴黎都市等级占FRA实有本土都市总等级的份额，配互斥的巴黎人口基建与地方建设/迁移政策。铁路回到具体物流需求。
- 共和国偏向政治经济自由化与维持繁荣；社会后果可能推动公共服务和劳动保障，也可能促成军队与寡头合作、镇压及右转，均由实际条件和选择推进。

常规政治目标只要求相关IG执政及合法性至少50；不检测党派组合，党派规则仅用于理解政治取舍。新路线目前均为计划，未改游戏脚本。[依据：P24；A-FRA；本轮作者纠正]

'''+s[z:]
write(p,s)
p=W/'reports/observer-finish-20261103/reference-mods.md';s=read(p)
anchor='## 5. FRA专案：在已有政治树上增加经济与外交后继'
assert s.count(anchor)==1
s=s.replace(anchor,anchor+'\n\n2026-11-03更新：具体实施方向以[法国政治与地区方案](../france-politics-plan-20261103/france-development-plan.md)为准。常规政治任务是相关IG执政＋合法性50，不设党派组合门槛。原参考公司与人物资料保留。')
old='|实业家君主／受管理的资本|可在既有奥尔良或波拿巴政府下扶持铁路、工程与银行；经过实际繁荣后开启公司集中议题，选反垄断/有条件合并/继续特许。|技术、贸易与私人资本扩张；金融集中、财政担保和工人议价矛盾。经济下滑触发的是可处理危机，不设1862必然崩盘。|'
new='|奥尔良后继：宫廷与外省|取得政权后选择巴黎集中发展或外省城市成长，用巴黎都市份额显示倾向；金融、服务、工业与地方学校围绕选择展开。|巴黎人口基建或外省迁移吸引/施工效率；保留财政、就业、公司集中和劳动争议。铁路不再是统一的路线终点。|'
assert old in s;s=s.replace(old,new)
old='|保守王朝／社会保守整合|接现有波旁后继，走地方公共工程、农业改良、教会教育和有选择的产业补助；也可以接受技术与铁路。|乡村/教会支持与较渐进转型；纳税、学校控制、地方特权和城市代表权仍有冲突。不把“保守”写成禁止工业。|'
new='|波旁后继：宫廷与外省|复用同一空间选择，按农村、教会、军人购田者及在位人物的利益发展不同政治反馈；既可经营外省也可强化巴黎。|公共工程、农业加工与教育；纳税、学校控制、地方特权和城市代表权仍有冲突。不把王朝名称固定为某个按钮。|'
assert old in s;s=s.replace(old,new)
old='|共和终局与社会共和国分化|若现有政治树产生共和国，原建设进度继续；围绕市民共和、劳动权和公共服务分配争论，不清空公司。|共和国仍可能殖民、资本集中或保守；对外政策按现政府和实际利益选择，不自动扶持所有共和/独立运动。|'
new='|共和繁荣与分配|现实共和制度成立后，延续资产并推动政治经济自由化；比较企业繁荣与民众生活，回应真实政治运动。|可走社会改革，也可形成军队与寡头的合作、压制社会主义运动乃至右转；不是预定结局，不复制俄罗斯人物和时间线。|'
assert old in s;s=s.replace(old,new)
write(p,s)

issue=M/'.scratch/debug-release/issues/29-france-political-planning.md'
assert not issue.exists()
write(issue,'''# 29 法国政治传播与后继建设方案

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: NOT_APPLICABLE
Evidence: [法国完整方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/france-politics-plan-20261103/france-development-plan.md>)

## Result

完成RAHF征韩论及前后长期动员链、原版党派/选举/合法性、当前法国王朝接口及巴黎地区修正的源码研究。常规政治目标按相关IG执政＋合法性50；JE/决议/按钮禁止党派组合检测，较高难度先论证。规则已写入NESND技能political-design-and-difficulty.md并由主技能条件路由。

波拿巴保留原方向并接真实人口/运动/人物；波旁奥尔良在实际取得政权后以“宫廷与外省”替代泛铁路中心；共和国以自由化、繁荣分配及条件性的军队寡头合作/压制/右转展开。纯迁出修正、都市比例区间与奖励平衡仍为明确待证量。仅研究/方案/技能交付，未实施法国玩法、未开游戏，未改历史数据；验证文件与远端结果见同报告目录validation.json/git-delivery.json。
''')
p=M/'.scratch/debug-release/map.md'
write(p,read(p)+'''
## 当前研究交付：法国政治与地区建设（2026-11-03）

[29 法国方案](issues/29-france-political-planning.md)：RAHF动员与原生党派机制已核；常规目标IG执政＋合法性50，不检测党派组合。补“宫廷与外省”及共和国分配/右转的条件性路线，保留波拿巴原方向；新增政治难度技能规则。本批仅文档，未实施玩法、未开游戏。后续以WORK/reports/france-politics-plan-20261103/france-development-plan.md为准，不沿用被纠正的组合门槛。
''')
p=S/'references/active-work.md'
write(p,'''# 当前交接：法国政治与地区建设方案（2026-11-03）

任务29为研究/方案/技能交付，未修改游戏玩法。报告WORK/reports/france-politics-plan-20261103/：france-development-plan.md为当前法国拓展方案，另两份来源报告记录RAHF完整动员链和党派/合法性。较旧四国方案的法国部分已指向本稿，意大利计划保持。

作者最新约束：常规政治目标只查相关IG执政＋合法性至少50；JE、决议、按钮不得检测党派成员组合、同党关系、人数或组阁排列，隐藏判断/AI权重亦不能变相要求。更高合法性只用于有意困难的目标，需反思可控性、期限、叠加前置及回报。党派定义若以后修改才考虑1—3IG与共同法律立场；本批不新增党派。规则入口references/political-design-and-difficulty.md。

波拿巴续接既有经济与政治反馈；波旁/奥尔良实际得政权后用巴黎/本土都市份额及互斥政策发展“宫廷与外省”；共和国自由化与繁荣可走社会改革，也可在具体利益冲突下走向军队寡头合作与镇压。尚未实施，纯迁出接口/城市比例奖励区间需校准。不打开游戏。本批保存状态见同报告git-delivery.json。以下旧交付记录保留。

'''+read(p))
print('Research advice corrected; French plan, skill route and task handoff recorded')
