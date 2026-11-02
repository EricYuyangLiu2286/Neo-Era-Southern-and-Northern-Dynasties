from qin_persia_context import W,M,S,read,write,sha,dump,man
from pathlib import Path
import shutil,json
R=W/'reports/india-research-20261102';J=W/'reports/japan-research-20261102/revision-2'
B=W/'backups/pre-change-japan-india-research-20261102T161938Z/mod'
assert man(M)==man(B)
def preserve(p):
 q=R/'documentation-before'/p.name
 if p.exists() and not q.exists():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
def append(p,s):preserve(p);write(p,read(p).rstrip()+'\n\n'+s.strip()+'\n')

write(R/'release-notes.md','''# 日本修订2与印度研究交付

2026-11-02；基线717c901。本轮是研究、方案与任务保存，没有修改游戏玩法脚本、国家主流文化、人物、人口、地图、建筑或军队，未启动游戏。日本上一轮研究已在仓库保存；本轮追加修订2和RAHF/资源证据，旧方案另有独立备份。

## 日本最新方案

- 作者明确天皇政权就是林摄政政权：计划对象改为JIM和国，JAP保留丰臣残余。当前游戏仍把林任命给JAP，列为首批必须同步纠正的实施项，不误报已改。JIM定义将增加ce_wuu（江南）主流，并联动出生/恢复/身份重置、任命、政府显示与旧档保存对象；不进行全局TAG替换。
- 扶国主矿业→金属工业→军工船业/对吴供给→城市；桑国主棉丝茶→成衣→消费品→SOL；林摄政和国主粮食→城市→罐头/加工，不获得第二条轻纺日志。目标按实际资源和国土规模，不能把全部关西给大阪或把缺显式矿山当缺矿藏。
- 任何日本三国成员或无九州统一国独立后，均可获得一次国家建设总日志，接军制、工业、外交；无需先拿回九州。原版有维新后建设框架；RAHF10.9确有帝国国会、大日本帝国、殖产兴业、民族融合法案，已读实际入口/条件/奖励。后期300营要求不会照搬给小国。
- 国家团结按经济/军事/社会状况变化；高团结每国每月抽一次30%，成功选一州，转换至多州总人口10%。JIM目标江南，其余日本文化，宗教不变；计算快照P/E避免把州人口10%误算成少数人口10%。仅做量纲示例，未写运行脚本。

详见WORK/plans/two-empires/20261102-japan-development-design.md修订2，以及WORK/reports/japan-research-20261102/revision-2/。此前三个研究报告保持原事实和时间指纹，最新作者设定单独追加。

## 印度研究

原版：native-india.md，23个JE对象（其中2项明确是DEI不套用）、125事件索引及核心条件链，81源码文件SHA。当前MOD：current-mod-india.md，人口/建筑/PM/军队/法律/宗教/外交及177来源；完整数据与紧凑摘要分开。设定：india-canon.md，重读北明PPT、海军人物全篇103非空段、其他原稿、旧HOI4和策划图，共29源复核。

方案：WORK/plans/two-empires/20261102-india-development-design.md。以少量主日志推进朝廷改革、法援、学校/产业、王朝与印度共同体、种姓/公职、地方统一与抗吴；阶段条件成立才开后继，不用大量随机剧情事件。

主要实际发现：MUG是法国朝贡国，93471151人口、印度教约69.01%；南部印度主要归USM直接统治，审计含岛屿22740898人。MUG有效主文化hindustani不等于王朝历史出身；新旧历史文件名不同会共存，原版BIC关联日志失去适用对象，EIC公司条件及仅3支显式原版编制须先审计。这些源码问题和风险未在本轮擅自改动。

印度教、种姓、学校和文化接受分层；法国可支持王朝或统一运动，援助与依赖并存。反吴殖民起义与反莫卧儿乡村/社会起义分开。海军文档的二十世纪人物不提前生成。原生民族主义的英国/BIC前提不直接移植。

## 核验与边界

原版和MOD研究者分别核对印度方案事实，唯一修正已落实：法援binding_period是一年约束期，不是自动到期；计划改为约束期与撤回/重谈。日本复用来源仅任务索引MD变化，相关游戏数据SHA一致。数值示例只是设计算术，不是游戏验证。当前所有新日本/印度机制仍为计划，游戏文件不变；主MOD只追加研究任务入口，私有仓库保存完整证据和计划。
''')

append(W/'reports/japan-research-20261102/japan-canon.md','''## 作者澄清（修订2）

2026-11-02最新用户明确：“ppet里提到的天皇政权就是林摄政政权”。这已是author_explicit，不再作为政权对应的未决问题。实施方案将JIM和国作为天皇—林摄政政权，JAP为丰臣残余；当前代码仍任命JAP的事实保留在源码报告中，属于待同步修正，不用旧实现覆盖作者新要求。江南目标文化为ce_wuu，产业与团结细则见revision-2及更新后的日本方案。
''')
append(W/'reports/japan-research-20261102/current-mod-japan.md','''## 后续作者修订与现有实现的区别

用户随后明确天皇JIM就是林摄政政权；本文记录的JAP任命是717c901之前的真实实现，并非新方案。最新计划已列JIM目标、主流ce_wuu及整条任命/恢复/保存对象迁移；本轮研究未改玩法，不能只看计划便认为游戏已切换受任国。见同目录revision-2/revision-record.json。
''')
append(W/'plans/two-empires/00-master-plan.md','''## 日本修订2与印度研究（2026-11-02）

日本方案明确JIM天皇—林摄政、三国产业、独立后发展与30%/州10%团结文化转换，仍待实现；当前JAP任命列首批修正。印度三份原始来源研究及少剧情制度方案完成，见20261102-india-development-design.md。证据与实际保存状态见WORK/reports/india-research-20261102/release-notes.md；本轮无玩法变更。
''')

write(M/'.scratch/debug-release/issues/19-japan-india-research.md',f'''# 日本方案修订与印度研究

Record: decision
Type: research
Status: resolved
Assignee: root
Blocked by: none

## Question

按作者澄清修订日本三国产业、林摄政JIM、独立后发展及文化团结；保存日本研究，再按原版/当前MOD/设定三层研究莫卧儿和明属印度，形成少剧情制度方案。

## Answer

研究及方案已完成，详见[交付说明](<{R.as_posix()}/release-notes.md>)及两个开发map。当前游戏脚本未改；日本新机制、JIM任命/主流和印度基线修复均未实施。资料覆盖与事实复核有独立来源和SHA，未开游戏。
''')
append(M/'.scratch/debug-release/map.md','''## 最新：日本修订2与印度研究（2026-11-02）

[19 研究与方案](issues/19-japan-india-research.md)：作者明确JIM＝天皇／林摄政；三国产业、独立发展、文化团结计划已更新。印度原版、当前MOD、原稿与HOI4研究及制度方案完成。本轮只改研究入口与文档，玩法未改。后续见日本与印度开发map。
''')
append(M/'.scratch/japan-development/map.md','''## 修订2：作者新要求

天皇JIM即林摄政政权；当前JAP受任代码是待同步修正项，不能继续把其当计划。JIM需加入ce_wuu主流并保持日本兼容身份。扶国矿业军工船业、桑国轻纺消费品SOL、和国粮食城市食品链；JIM排除轻纺日志。独立后国家发展总JE及每国每月30%→一州总人口10%的文化转换列入方案。详见20261102-japan-development-design.md第九节。尚未写入玩法。
''')
write(M/'.scratch/india-development/map.md',f'''# 印度开发入口

Record: decision
Type: research
Status: resolved
Assignee: root
Blocked by: none

## Destination

以少剧情、多制度处理莫卧儿半殖民地/种姓国家、法国现代化援助、王朝与印度共同体、宗教/识字/文化整合、地方统一及抗吴。

## Decisions-so-far

[三层研究与证据](<{R.as_posix()}/release-notes.md>)及[实施方案](<{(W/'plans/two-empires/20261102-india-development-design.md').as_posix()}>)已完成。MUG/FRA朝贡、USM南印度直接领地、土邦、宗教文化与产业数据按有效源码；不照搬英国BIC叙事。民族主义与王朝不必零和，印度教与种姓/教育分层。

## Next work

先整理MUG活动定义与不同名历史叠加、王朝人物、编制/公司和BIC硬绑；再做小型改革主JE与法援合同，随后学校/产业、社会与民族动员、统一/抗吴及统一后治理。每阶段有实际入口和终局，后期不在开局全开。

## Not yet implemented

本轮没有实施印度新机制、改初始军队或文化，也没有改州归属。报告中的人口与产业是静态输入，非运行SOL/GDP；未开游戏。
''')
append(S/'references/narrative-context.md','''## 日本修订2与印度专题

涉及日本林摄政/文化同化/三国产业时，先读最新日本方案第九节和WORK/reports/japan-research-20261102/revision-2：作者已明确天皇政权JIM就是林摄政，旧JAP任命为待改实现，不能再当未决设定。数值和主流修改是否上线以任务19与交付记录为准。
涉及莫卧儿/明属印度/法国援助/种姓时，读WORK/reports/india-research-20261102的native-india.md、current-mod-india.md、india-canon.md。王朝历史出身、国家主文化、宗教和种姓适用群体分别核实；旧.bak不是活动定义，不同名history不会覆盖原版。海军原稿的人物年代与1836分开。实施方案在WORK/plans/two-empires/20261102-india-development-design.md；具体法援同时读native-treaty-aid.md。
''')
preserve(S/'references/active-work.md')
write(S/'references/active-work.md',f'''# 当前交接：日本修订2与印度研究

Updated: 2026-11-02；研究基线717c901。[任务19](<{M.as_posix()}/.scratch/debug-release/issues/19-japan-india-research.md>)、[报告](<{R.as_posix()}/release-notes.md>)为当前入口；仓库保存核对见同目录git-delivery.json。本轮无玩法变更，未开游戏。

日本：作者明确JIM天皇＝林摄政；当前代码JAP任命仍待按完整链改，JIM主流ce_wuu待添加。三国产业、独立后发展、每国每月30%抽一州总人口10%文化转换已入计划，绝不称已上线。最新日本方案第九节优先，旧方案独立保存在revision-2。

印度：原版23JE/125事件索引、当前MOD人口产业与初始化、PPT/海军全篇/HOI4/策划图研究完成。少剧情制度方案完成。下一批先审MUG不同名history叠加、活动国家定义、人物、编制/公司和BIC绑定，再做改革/法援/民族/种姓/统一。法援一年binding_period不是到期，已有规则须继续读取。

西秦上一轮阶段修正已交付：开局4JE、后继三权/故土、危机暴动，旧档已开启保留。本轮不修改该玩法。日本/印度开发map是计划入口；未实现部分不要因研究resolved误当游戏功能completed。
''')

current=man(M);baseline=man(B)
changed=[p for p,h in current.items() if baseline.get(p)!=h]
assert all(p.startswith('.scratch/') and p.endswith('.md') for p in changed)
assert not set(baseline)-set(current)
dump(R/'gameplay-unchanged.json',{'baseline':'717c901195aa683a68a88409e1b6acb464e64f06','backup':str(B),'files_before':len(baseline),'files_after':len(current),'only_main_changes':changed,'gameplay_changed':False,'game_launched':False})
print('Research docs saved; main only task Markdown changed:',changed)
