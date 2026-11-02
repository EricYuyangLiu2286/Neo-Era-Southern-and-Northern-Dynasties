from pathlib import Path
import sys,json,hashlib,shutil,re
sys.path.insert(0,str(Path(__file__).parent))
from qin_persia_context import W,M,G,S,read,write,sha,dump,parse,man
R=W/'reports/japan-research-20261102/revision-2';R.mkdir(parents=True,exist_ok=True)
F=Path('D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/2893069455')
paths=['.metadata/metadata.json','common/journal_entries/dsk_je_jap.txt','common/scripted_buttons/dsk_jap_scripted_buttons.txt','common/static_modifiers/dsk_usa_modifiers.txt','events/sino_events.txt','localization/simp_chinese/DSK main events/DSK_CHI_and_JAP_l_simp_chinese.yml','localization/english/open_japan_l_english.yml']
dump(R/'rahf-sources.json',[{'file':str(F/p),'sha256':sha(F/p)} for p in paths])
write(R/'rahf-japan-reference.md','''# 独立后的日本建设：原版与RAHF参考

本机已安装Realism Ai Historical Flavor Mod，工坊ID2893069455，metadata版本10.9，支持1.13.*。只读脚本；不改工坊、不复制图片或整套代码到主MOD。文件SHA见rahf-sources.json。

原版确有维新后建设总日志 `je_meiji_main`，中文名由emperor_var生成“某某维新”，并非名为“发展帝国”的通用独立日志。其军制、经济、外交/使团子项在维新结算后添加，不天然适用于JTK/JIM/共和国；本MOD日本也已经受承认，不能照搬“取得承认”当全部外交目标。具体原生链见上一轮native-japan.md。

RAHF实际有：

|条目|入口/条件与结果|借鉴边界|
|---|---|---|
|je_jap_empire“帝国国会”|dsk_je_jap.txt:486，君主及JAP/特殊KOR身份可见；选举/法律条件进入，政治事件在议会环境中展开|不是独立即开的通用改革日志，也不是所有国家必须称帝|
|je_great_japan“大日本帝国”|同文件2141；dsk_jap_scripted_buttons.txt:1413的jap_be_empire_button消耗国会进度50后添加；要求300军队、职业/大众征兵、战争游戏与堑壕技术、军制/军需及国家等级；完成触发sino_event.29。AI有100军队的宽松invalid结算|可借鉴后期国家能力目标；不能直接把300营目标交给新独立的京都小国，也不复制AI/player不同结算来伪造一致难度|
|je_zhi_chan_xing_ye“殖产兴业”|同文件1646；sino_events.txt:2349添加；食品/纺织/玻璃各有一栋15级、occupancy>75%、盈利>0；完成激活自定义law_IJ_CI，制造/服务吞吐+20%十年（dsk_usa_modifiers.txt:2048）|建设链和有期限奖励可参考；15级三厂不是NESND三国统一尺度，自定义法律不可只抄调用|
|je_IJdcr“民族融合法案”|同文件932；按钮在dsk_jap_scripted_buttons.txt:1296加入，使用地区法令、失败计数、事件和短期修正|不是用户要求的月度30%/一州10%机制。只参考民族整合成为持续国政议题，不照搬其法令和事件|

结论：独立后的JAP/JTK/JIM，以及无九州统一日本，都应获得本项目自己的“重建国家”总日志。它借原版多部门发展结构，按实际国家规模与已完成建设设目标；不触发原版天皇复位、不强加帝制、不要求先收齐九州。RAHF的大日本帝国可作为更晚的实力目标参考。
''')

# Pure arithmetic examples for the requested magnitude; this is not an engine test.
cases=[]
for total,eligible in [(100000,100000),(100000,20000),(100000,5000),(100000,0),(1,1)]:
 q=min(1,0.1*total/eligible) if eligible else 0
 cases.append({'state_population':total,'population_not_target_culture':eligible,'conversion_fraction_of_eligible':q,'expected_people_before_engine_rounding':eligible*q,'target':min(eligible,0.1*total)})
 assert abs(eligible*q-min(eligible,0.1*total))<1e-8
dump(R/'cohesion-scale-examples.json',{'monthly_country_roll':0.3,'selected_state_share':0.1,'cases':cases,'expected_successes_per_year_if_always_eligible':3.6,'engine_verified':False,'implementation_written':False})

plan=W/'plans/two-empires/20261102-japan-development-design.md'
before=R/'previous-japan-plan.md';assert not before.exists();shutil.copy2(plan,before)
s=read(plan)
s=s.replace('2026-11-02。日本部分为研究及玩法提案，尚未改日本玩法；','2026-11-02，修订2。日本部分为研究及玩法提案，尚未改日本玩法；',1)
s=s.replace('三国时期扶国的军府、桑国的摄政军政网络都可成为入口','三国时期扶国的军府、和国的林摄政军政网络都可成为入口')
s=s.replace('- 林汉涵沿用当前游戏名与USM_lin_hanhan；其三国统辖在实现上固定由JAP摄政承载，不把同一角色复制成三国君主。','- 最新作者明确：天皇政权就是林摄政政权。因此方案以JIM和国承载林摄政，保留天皇政权身份；沿用USM_lin_hanhan，不复制人物。当前已交付代码仍把林任命到JAP，这是与新设定不符的实施待办，须连同任命/恢复/保存对象/政府显示一起改为JIM，不能只替换一句名称。')
s=s.replace('- 和国以京都政治合法性和大阪实际商港为基础；税容、民政、商业联系优先。','- 和国作为天皇—林摄政政权，以京都政治合法性和大阪实际商港为基础；粮食、城市化、食品加工为主，不给棉丝茶—成衣—消费品—SOL日志链。')
s=s.replace('- 桑国处理丰臣旧臣、林军政与朝鲜治理，','- 桑国处理丰臣旧臣与朝鲜治理，')
s=s.replace('以当前游戏为实施依据，保留资料异文，不擅自改林汉涵为李汉涵。','以当前游戏为人物命名依据，保留资料异文，不擅自改林汉涵为李汉涵；政权对应以本轮作者明确的“天皇政权即林摄政政权”为准。',1)
write(plan,s.rstrip()+'''

## 九、作者新增要求：三国产业、独立后发展与团结（修订2）

本节为最新实施规格，优先于前文尚未定稿部分；仍是计划，不声称相关日志或江南主流文化已经写入游戏。对应资源证据见WORK/reports/japan-research-20261102/revision-2/three-state-economic-inputs.json，RAHF参考见同目录rahf-japan-reference.md。

### 1. 政权、领土和主流文化必须一起对齐

|TAG|现有分封领土（不改边界）|新方案政权|文化目标|
|---|---|---|---|
|JAP／桑国|中国地区、关西扣除大阪，原有釜山/两湖等朝鲜领地|丰臣残余|japanese|
|JTK／扶国|关东、东北、东海、北陆信越、日本原持有北海道部分|德川军府|japanese|
|JIM／和国|京都＋大阪province xB03EF0|天皇政权＝林摄政政权|ce_wuu（本MOD显示名“江南”）|

实施必须同时处理：country_definitions/nesnd_japan.txt 中JIM的cultures加入ce_wuu（保留japanese）；新国on_created、身份重置和恢复链不能又删掉ce_wuu；林任命、pending精确人物/受任国、政府类型、维护/撤任、旧档迁移都从当前错误JAP目标改成JIM。不能全局把c:JAP替换成c:JIM，也不能把老档已转给其他国家的人物强抢回来。天皇与摄政的角色关系需参考当前V3原生角色接口，保留一个实际ruler，明确天皇身份承载，不能复制同一角色或用无效regent指令。

### 2. 产业日志默认分配与顺序

每国先开放一条主链的第一步，完成后才出现下一步。资源足够时允许其他合理补充链；林摄政JIM始终排除第二条轻纺—SOL链。这个排除只针对日志，不禁止玩家经营现有茶、丝、纺织建筑。

|主链|默认主要承接者|按次序开启|奖励与现实依据|
|---|---|---|---|
|矿业—军工船业—城市|JTK扶国；JAP取得合适矿区后可补充|扩建适用矿业→建军工和船业并参与对吴供给→城市化|扶国现有铁15、木10、军营35；其四个完整州铁潜力合计69、煤6。矿业完成奖钢铁/工具等金属工业吞吐，军工船业再给有限期军需/造船收益。不得把矿山吞吐误称金属制造产能|
|棉丝茶—成衣—消费品—SOL|JAP桑国；JTK可在自身资源满足时开放|种植/原料→成衣制造→食品/家具/玻璃等消费品→持续生活改善|桑国整州上限已有丝4、茶6、纺织8、食品8、造船4；中国地区和关西可种棉丝茶。大阪分割后的实际数量要重新读取。JIM不获得此链|
|粮食—城市—食品加工|JIM和国为主；其他两国可补充|粮食/渔业供给与就业→适度城市化→罐头/食品加工与后续产业|京都固定耕地44、铁潜力8、鱼20，加实际大阪份额；已有稻1、牧2、食品1。粮食来自生产和贸易都可形成经济基础，不能逼所有国家全国自给|

现有产业与潜力分开：JAP暂缺显式铁矿，但中国地区铁潜力22、关西整州12，不能写成“桑国没有铁资源”；JIM京都铁潜力8，不能套原版京都3。关西/北海道分州的资源与建筑不得按省色数量等比例编造，实际读取owner-state。

城市目标采用分国档位，作为实施初值：扶国先2个三级城市，再3个五级城市；桑国先2个三级城市，再1个五级城市并达到就业/消费品条件；和国先1个三级城市，后续1个五级城市。最终阈值需用实际分封后的城市中心、人口与工业基线核算，已满足者直接记成果，不能靠重新分国重复领奖。原料目标只选本国真正可生产的品类，缺矿不产生永远无法完成的按钮。

“支持吴国”在仍属吴或有效合作协议时表现为实际采购/供给安排，不用空关系+10替代。独立且仍友好可以协商继续；若已经与吴敌对，原供给安排清理，产业成果保留，由独立后军工议程接续。没有满足实际外交条件的对吴义务，不阻止已独立国家继续工业化。

奖励参考原版钢铁/工具/军工公司常见5%–10%吞吐与RAHF殖产兴业制造/服务20%十年；暂拟阶段金属工业10%五年、主链完成对应产业15%十年，不叠加成永久万能20%。这是设计初值，不是已经上线数值。SOL终点采用实际生活水平达到门槛并维持一段时间，不直接发永久SOL把未解决问题遮住。

### 3. 独立之后，立即获得国家发展总日志

JAP/JTK/JIM任何一国从属国变为独立，或旧档加载时已经独立而尚未登记本阶段，都获得一次独立后的发展总日志；统一但无九州同样适用。不以三国先统一或收齐九州为入口。完整有九州日本也可承接同一发展框架，但不能与既有同功能改革日志重复领奖。

借原版je_meiji_main“军制、工业、外交”结构，改成不依赖emperor_var、天皇复位、德川家或未受承认身份的本项目日志。工业承接各国已有主链；军制要求适合人口规模的训练、军需和兵制；外交要求真实独立与对外行动能力。JIM只有京都/大阪时不要求300营；只有后期国力及科技足够，才可参考RAHF大日本帝国的强国目标。

进度和奖励按country保存。分国、独立、改号和统一各有来源/继承登记，统一者继承已完成的相关成果而不叠领三个相同全国奖励。主日志退出需关闭其未完成子项并清理临时修正；已完成建设和实际法律保留。

### 4. 日本团结系统

这是日本的新规格，不照搬西秦的低团结复归/帝国解体。每国独立计算0–100团结，经济繁荣、生活改善、有效教育/行政、军事胜利提高，长期战争、败战、破产、严重激进化降低。增减在原生进度条显示；胜利修正有期限/不重复堆叠。开局值暂定70，高于75时启动文化融合，阈值属于可调设计初值。

作者已指定的两项数值固定记录：**每国每月判定一次，30%概率；成功后只选一个合格本国州，将至多该州总人口10%转为目标文化。** 同月不是对所有州各抽30%，也不是每个pop各抽30%。目标：JAP/JTK及其通常统一国为japanese；天皇—林摄政JIM为ce_wuu。JIM保留日本主流资格用于既有角色/制度兼容，但同化目标明确选江南，不随机从主流列表抽取。

数量实现：先快照州总人口P、非目标文化人口E；需转换min(0.1P,E)，对所有非目标文化pop使用同一快照比例min(1,0.1P/E)。E=0的州不入候选。例：十万人州只有两万人尚未属于目标文化，应转换一万人，即这两万人的50%；直接value=0.1只会转换两千，不符合本轮要求。只调用change_pop_culture，宗教保持；不需要西秦宗教复归的临时文化批次。量纲算例见cohesion-scale-examples.json，尚未做游戏执行。

团结属于国家状态，不因换君主重置。江南文化路线按林摄政政权的制度身份持续，不因林个人去世自动撤销；若玩家后来改变该制度，明确选择此后文化政策，既有人口不追溯改回。低团结暂只造成政治/社会压力和暂停同化，不无条件重复三分日本。以上接口需在实施时按原版文化转换及既有huaxia效果完整核验。

### 5. 当前状态

日本原始研究和本轮RAHF/资源补充均已保存。此修订是未来实现的权威计划：本轮未迁移林、未修改JIM主流、未新增产业/团结日志；当前代码与新设定的差距已明确列入首批实施任务，不能误报已上线。印度研究另存20261102-india-development-design.md。
''')
dump(R/'revision-record.json',{'base_git':'717c901195aa683a68a88409e1b6acb464e64f06','plan':str(plan),'before_sha256':sha(before),'after_sha256':sha(plan),'latest_author_mapping':{'JAP':'Toyotomi','JTK':'Tokugawa','JIM':'Emperor and Lin regency'},'gameplay_changed':False,'primary_culture_change_status':'planned: JIM adds ce_wuu, pending implementation with appointment/recovery chain','conversion_status':'planned, not implemented'})
print('Japan revision2 and primary-source supplement saved; gameplay untouched.')
