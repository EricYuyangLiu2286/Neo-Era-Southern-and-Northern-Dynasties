from pathlib import Path
import json,hashlib,collections
O=Path(__file__).parent
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
W=M.parent.parent/'nesnd-workbench'
d=json.loads((O/'current-mod-india-data.json').read_text(encoding='utf-8'))
def ref(rel,line=1,root=M):
    p=root/rel
    d['source_sha256'][p.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    return f'[{rel}:{line}](<{p.as_posix()}:{line}>)'
def fmt(x): return f'{x:,}'
tot={x['tag']:x['size'] for x in d['population_by_owner']}
def pct(x,t):return f'{x/t*100:.2f}%'
relig={t:{x['religion']:x['size'] for x in d['population_by_religion'] if x['tag']==t} for t in ['MUG','USM']}
btypes={t:{x['type'].removeprefix('building_'):x['levels'] for x in d['buildings_by_type'] if x['tag']==t} for t in ['MUG','USM']}
summary={'status':'SOURCE_AUDIT / ENGINE_NOT_RUN','version':'1.13.11','build':'24799966','baseline_git':'717c901','audit_geography':'All regions declared in effective MOD history/pops/10_india.txt, plus every MUG owned region; includes Kashmir, Ceylon and Indian Ocean Territory; excludes Nepal/Bhutan/Afghanistan except where same file explicitly includes them.','population_total_audit':sum(tot.values()),'population_by_owner':tot,'USM_mainland_population':tot['USM']-1258836-103400,'MUG_primary_culture':'hindustani','MUG_primary_population':24467839,'USM_primary_cultures':['ce_wuu','min'],'USM_primary_population_in_audit':0,'religion':relig,'buildings':btypes,'military':{'MUG_scripted_combat_units':{'irregular_infantry':2,'hussars':1},'USM_indian_mainland_scripted_combat_units':0,'USM_ceylon_ship_assignments':{'ship_of_the_line':15,'frigate':15},'TRA_scripted_combat_units':{'line_infantry':7,'lancers':1,'cannon_artillery':1},'TRA_ship_assignments':{'frigate':1}},'critical_overlay':['GAME mug - mughals.txt and MOD mug - mongul.txt coexist','GAME characters mug - hindustan.txt and MOD mug - mongul.txt coexist','MUG country definition only inherited GAME 00_countries.txt; MOD 00_countries.txt.bak ignored','CE_military_formations_india.txt comment-only; GAME 05_military_formations_india.txt survives'],'implemented_mod_hook':'nesnd_external_policy, France aid requests and Mysore claim only','source_sha256':d['source_sha256']}
text=f'''# 当前主 MOD：莫卧儿与明朝治下印度源码研究

2026-11-02；**SOURCE_AUDIT / ENGINE_NOT_RUN**。本轮只读 MOD/GAME，未开游戏、未改玩法、未改技能。catalog：1.13.11 / Steam 24799966 / CURRENT / changed_count=0。根任务给定 Git 对照基点 `717c901`；主 MOD 是独立加载目录，其本轮身份以 JSON 内逐文件完整 SHA-256 为准。

数据： [完整保序数据](<{(O/'current-mod-india-data.json').as_posix()}>)；[紧凑摘要](<{(O/'current-mod-india-summary.json').as_posix()}>)；[可复跑审计脚本](<{(O/'audit_current_mod_india.py').as_posix()}>)。解析保留重复 `create_pop`、`create_building`、`resource`，按 GAME→MOD 同相对路径覆盖；`.bak` 不参与。人口块未显式写宗教时按有效文化默认宗教计算。没有缺所有者的人口块。建筑等级按显式 `level`，否则合计 `add_ownership`，不把自动生成自给建筑和军营混为这一静态账。

## 1. 最先要纠正的地图和覆盖认识

这里不是英属印度。当前州历史没有 BIC 或 MYS 的 `create_state`；莫卧儿 MUG 直接持有北印度—孟加拉与孟买大片领土，南印度主要直接所有者是 USM。TRA 是 USM 傀儡；MYS 的傀儡调用受到 `exists` 保护，不能把它当成现存迈索尔土邦。其余印度诸邦没有因为 BIC 原来是其宗主就自动改属莫卧儿。原版 BIC 属国关系在本 MOD 同路径文件中被注释；没有查到把 HYD、AWA、NAG 等转给 MUG 的有效开局关系。{ref('common/history/diplomacy/ce_subject_relationships.txt',136)}；{ref('common/history/diplomacy/00_subject_relationships.txt',279)}。

MUG 有两组会共存的历史文件：原版 `mug - mughals.txt` 与 MOD `mug - mongul.txt`；人物也是原版 `mug - hindustan.txt` 与 MOD `mug - mongul.txt`。新增不同文件名不覆盖原版。原版科技与法律、DLC Mughal JE 初始化，以及四名原版人物仍在加载集合中。具体同一席位最终是谁、运行时日志是否立刻失效，须引擎核实，不能由文件排序假定。{ref('common/history/countries/mug - mughals.txt',1,G)}；{ref('common/history/countries/mug - mongul.txt',1)}；{ref('common/history/characters/mug - hindustan.txt',1,G)}；{ref('common/history/characters/mug - mongul.txt',1)}。

有效 MUG 定义来自 GAME：未受承认、帝国级、首都德里、主文化仅 `hindustani`、国教 Sunni，社会等级是 `british_indian_caste_system`。当前 MOD 没有活动 MUG 定义。忽略文件 `00_countries.txt.bak` 内却保留 `avadhi sindi kannada bengali` 四主文化，属于旧设计线索，不能当作已实施。{ref('common/country_definitions/00_countries.txt',1278,G)}；{ref('common/country_definitions/00_countries.txt.bak',1249)}。

## 2. 人口、归属和社会基础

审计范围是 MOD `history/pops/10_india.txt` 的全部地区（含锡兰、印度洋领地、克什米尔），并追加所有 MUG 实际所有地区；不是凭现代国界估算全南亚人口。范围内共有 **{fmt(sum(tot.values()))} 人**；MUG **{fmt(tot['MUG'])}**；USM **{fmt(tot['USM'])}**，其中印度大陆 **{fmt(summary['USM_mainland_population'])}**，锡兰 1,258,836，印度洋领地 103,400。各州所有者、来源行、每个人口块见 JSON。主要人口底账：{ref('common/history/pops/10_india.txt',1)}；州归属：{ref('common/history/states/00_states.txt',4051)}。

| 所有者 | 地区 | 静态人口 | 历史整合状态 |
|---|---|---:|---|
'''
for x in d['population_by_state']:
    if x['tag'] not in {'MUG','USM'}: continue
    s=next(s for s in d['states'] if s['tag']==x['tag'] and s['region']==x['region'])
    status='未整合（显式）' if s['type']=='unincorporated' else '未显式标未整合'
    text+=f"| {x['tag']} | {x['region']} | {fmt(x['size'])} | {status} |\n"
text+='''
德里与阿格拉虽然是王朝核心地理，却显式 `unincorporated`；明朝的迈索尔、马德拉斯、锡尔卡尔斯和特拉凡哥尔部分没有写 `unincorporated`。这是当前历史字段的不对称，不能在设计时默认“莫卧儿核心一概整合、明殖民地一概未整合”。本报告没有把省格数按面积换算人口或资源。

| 所有者 | 印度教 | 逊尼派 | 什叶派 | 穆斯林合计占比 |
|---|---:|---:|---:|---:|
'''
for t in ['MUG','USM']:
    rr=relig[t]
    text+=f"| {t} | {fmt(rr['hindu'])}（{pct(rr['hindu'],tot[t])}） | {fmt(rr['sunni'])} | {fmt(rr.get('shiite',0))} | {pct(rr['sunni']+rr.get('shiite',0),tot[t])} |\n"
text+=f'''
上述宗教比例是**当前静态人口配方比例**，不是动态存档调查。其余宗教包含佛教、锡克教、基督教、犹太教、泛灵信仰；不可用“非印度教全部等于穆斯林”。文化与宗教为两维：孟加拉、印度斯坦等文化内同时有不同宗教人口。

MUG 的最大文化依次为孟加拉 38,867,650，印度斯坦 24,467,839，比哈尔 14,041,474，马拉地 8,675,089，卡纳达 2,084,070。有效主文化 hindustani 占 **{pct(24467839,tot['MUG'])}**。USM 地区为泰米尔 9,097,732、卡纳达 4,342,796、泰卢固（脚本拼作 `telegu`）3,516,818、古吉拉特 2,626,260、马拉雅拉姆 1,224,909、僧伽罗 980,828；**本批人口中 ce_wuu/min 均为 0**。USM 主文化仍为 ce_wuu/min，所以民族至上和本地族群接受度是一项实际结构问题，不能用几句归化文案解决。{ref('common/country_definitions/ce_countries.txt',2)}。

静态明列奴隶人口 MUG 2,477,600，USM 本范围 274,024；其余未写 pop_type 的块会进入引擎初始化与职业分配，不能称作全是农民或失业者。奴隶、农奴、佃农与种姓是不同层：奴隶职业、土地法、社会等级、宗教文化接受度分别核对。

主要仍存活本地政权：HYD 10,855,454；PAN 6,904,483；AWA 4,824,221；NAG 3,148,803；SIN 1,960,004；JAI 1,821,010；GWA 1,450,619；ASM 1,212,183；TRA 1,055,033。它们不是背景空白地。HYD/AWA/NAG 继承各自主文化、王朝、法律和种姓配置；PAN 是锡克政权的独立利益中心；TRA 的已有吴属身份与其余土邦不同。全部 52 个实际所有者的本范围人口见摘要 JSON。

## 3. 法律、宗教、种姓、机构与识字

MUG 自定义历史调用 `effect_starting_politics_traditional`。有效原版宏对伊斯兰国设 `law_people_of_the_book`，并设君主、专制、世袭官僚、臣民制、传统主义、农奴制、土地税、重商主义、农民征召、集会权、闭关、行会、无劳工权；自定义历史另设债务奴隶制、地主执政，反而把虔诚派改名为 `ig_hindu_priesthood` 并加 `ideology_hindu_moralist`。这是逊尼国教、印度教多数、印度教祭司 IG 的现有组合，不宜未经设计确认就“修正”为纯穆斯林国家。{ref('common/scripted_effects/00_political_setup.txt',74,G)}；{ref('common/history/countries/mug - mongul.txt',8)}。

`people_of_the_book` 不表示所有宗教平等：当前法定义具有国教/共宗教特征接受度加成、无共同宗教特征的 −25、非信徒税等。具体本地人口接受等级仍取决于文化与社会阶层，不能只凭 Sunni 国教推导全部 Hindu 的同一等级。{ref('common/laws/00_church_and_state.txt',243,G)}。

MUG 的种姓体系是真实有效国家定义，不是因正文写“英国”便自动停用。其人口适用条件是 Hindu 且南亚 heritage group；因此不覆盖全部穆斯林。原版有强制、成文、不强制、平等主义等法，联动资格与接受度、地主政治力量、行政人口成本。MUG 两份历史均未显式设种姓法，实际初始取值尚需引擎/初始化完整审计；**不能把传统政治宏误说成显式设了强制种姓**。TRA 的 princely_state 宏则显式设 `law_hindu_caste_not_enforced`。USM 定义无印度种姓 hierarchy，当前也未查到给它切换该 hierarchy 的本地脚本，不能默认其印度教臣民自动接受和 MUG 完全相同的种姓法律效果。{ref('common/social_hierarchies/00_social_hierarchies.txt',5,G)}；{ref('common/law_groups/00_laws.txt',38,G)}；{ref('common/laws/00_caste_hegemony.txt',7,G)}；{ref('common/scripted_effects/00_political_setup.txt',117,G)}。

MUG 无显式机构投资；人口历史设 low wealth / baseline literacy。baseline 在职业加成前为 0.05，未整合州乘半；文件首行明确**真正识字率在 setup 中重新计算，1836-01-01 不等于脚本值**，所以不能报“莫卧儿全国识字 5%”。USM 则 medium wealth / middling literacy，基值 0.35，职业、上层、自给就业和未整合州继续修正；该全国宏也覆盖它的印度领地，不能未经核实假定殖民地恒为另一识字档。{ref('common/history/population/mug - mongul.txt',1)}；{ref('common/history/population/USM - UnitedStatesOfMing.txt',1)}；{ref('common/scripted_effects/00_starting_pop_literacy.txt',1,G)}；{ref('common/scripted_effects/00_starting_pop_literacy.txt',292,G)}；{ref('common/scripted_effects/00_starting_pop_literacy.txt',121,G)}。

USM 的当前法律有财富投票、民族至上、信仰自由、干预主义、重商主义、农民自有地、债务奴隶制、职业军队、私立学校；学校机构 1、殖民机构 2，未整合州是否实际受益还须按机构规则判断。这是南印度受同一国家法律管辖的结构，而非独立的“明属印度国家”。{ref('common/history/countries/USM - UnitedStatesOfMing.txt',76)}。

## 4. 工业、资源和现代化的已有底盘

| 静态建筑等级 | MUG 全国 | USM 本研究印度地区 |
|---|---:|---:|
'''
for kind in ['construction_sector','government_administration','textile_mill','arms_industry','artillery_foundry','paper_mill','furniture_manufactory','glassworks','shipyard','coal_mine','iron_mine','gold_mine','logging_camp','port','naval_administration','trade_center','opium_plantation','cotton_plantation','dye_plantation','silk_plantation','sugar_plantation','tea_plantation','tobacco_plantation']:
    text+=f"| {kind} | {btypes['MUG'].get(kind,0)} | {btypes['USM'].get(kind,0)} |\n"
text+=f'''
来源为 {ref('common/history/buildings/10_india.txt',1)} 及完整 JSON 内每个重复建筑块。MUG 没有静态工具厂、钢厂、铁路、大学；煤 2、铁 3、建筑部门 2 与 9,347 万人口和广域行政形成的差距，应作为产业/技术/税制建设线的输入。MUG 并非完全没有制造业，纺织 22、军工 8、造船 5，不能重新设为纯自给国家。USM 本批也没有铁路、工具厂或大学；其核心区市场的进口供给不可从地方静态表直接读出。

资源潜力不是已开采产能：比哈尔地区耕地 375、煤上限 81、铁 30；东孟加拉耕地 601、煤 4；阿格拉耕地 483、煤 4、铁 3；孟买耕地 400、煤 12、铁 23；迈索尔耕地 210、铁 24、金 6；马德拉斯耕地 375、铁 26。分享地区的上限不能直接全数归给任一州所有者；必须依据实际 province/resource 分配与引擎州值。迈索尔和马德拉斯还分别有未发现橡胶 6/7，不能当作1836既有产出。{ref('map_data/state_regions/10_india.txt',1,G)}；{ref('map_data/state_regions/10_india.txt',123,G)}；{ref('map_data/state_regions/10_india.txt',408,G)}；{ref('map_data/state_regions/10_india.txt',459,G)}；{ref('map_data/state_regions/10_india.txt',518,G)}。

MUG 历史强行添加 `company_east_india_company` 并记成立日 1600-12-31，但原版公司当前 `potential/possible` 锁 GBR，是贵族所有的茶/烟草/鸦片公司。静态存在 `add_company` 只证明调用意图，未证明此公司在 MUG 正常生成、选址、所有权、繁荣加成正确；这应列兼容审计，不借公司名推断英国控制莫卧儿。{ref('common/history/countries/mug - mongul.txt',21)}；{ref('common/company_types/00_companies_asia.txt',2,G)}。

旧存档经济报告可提供曾出现的风险：2026-10-31 national-reference 候选在 AI 控制 MUG 下观察到未分配劳动力和饥饿，USM 古吉拉特有承载压力、锡兰部分已就业劳工仍贫困。但它绑定旧候选/旧场景，不能作为今日主 MOD 的最新 SOL、GDP、赤字或“改革预算”。本轮未复用其数值作当前经济验收。{ref('plans/two-empires/evidence/national-reference-economy-findings.md',1,W)}。

## 5. 实际编制与人物

自定义 `CE_military_formations_india.txt` 只有两行停用注释，不能据此说印度无军队，因为原版不同名 `05_military_formations_india.txt` 仍加载。原版 MUG 只有德里 2 不正规步兵 + 1 骠骑兵，总计 3 支 combat_unit；没有 MUG 舰队声明。当前静态建筑表无 MUG `building_barracks` 声明，不等于初始化后没有军营，也不能把军工厂等级当营数。**这个原版残留小国编制与本 MOD 大帝国体量不匹配，属于需要先核实/修复的基础项。** {ref('common/history/military_formations/CE_military_formations_india.txt',1)}；{ref('common/history/military_formations/05_military_formations_india.txt',1448,G)}。

USM 当前编制没有把陆军 combat_unit 指向本研究印度大陆地区；锡兰在南洋舰队中有 15 战列舰 + 15 护卫舰的 ship 声明。这不是证明世界里绝不会有调来的驻军，也不是30个旧式海军基地。TRA 继承7线列步兵、1枪骑兵、1火炮、1护卫舰。{ref('common/history/military_formations/CE_military_formations_asia.txt',347)}；{ref('common/history/military_formations/05_military_formations_india.txt',981,G)}。

MOD 为 MUG 创建 BahadurShahII（1775-10-24生、sindi、君主兼将领、地主传统主义、romantic/alcoholic）、MirzaDahlaBakht（20岁、sindi、继承人、军队、jingoist、reckless/expensive_tastes）、Zorawar Singh、Alexander Gardner。后两人沿用原版模板，分别来自克什米尔和旁遮普；本轮不将现实人生自动补进架空身份。{ref('common/history/characters/mug - mongul.txt',1)}；{ref('common/character_templates/zz_historical_leaders_ce_asia.txt',1129)}；{ref('common/character_templates/country_pan.txt',410,G)}。

同时原版还会创建 Akbar II 君主、Bahadur II 继承人、Sohan Lal 地主领袖、Hamid Ali Khan 小市民领袖。于是出现原版 Akbar/Bahadur 与自定义 Bahadur/Mirza 的席位及年代重叠风险。应先定现存王朝人物的唯一初始化，之后再设计继承/改革派；本轮不宣称已经测得双君主 UI。{ref('common/history/characters/mug - hindustan.txt',1,G)}；{ref('common/character_templates/country_mug.txt',5,G)}。

## 6. 法国、吴朝与现有日志闭环

开局 FRA→MUG 为 `tributary`；这是有效历史关系，不是仅风味上的法国顾问。当前没有发现 MUG→FRA/USM 的显式开局关系数值或 MUG/USM 直接战争/盟约；不得编造“关系−50”或既存同盟。MUG 出现在势力集团文件里的 member 行是注释，不能当有效成员。旧运行曾记录 FRA 市场含 MUG，但当前市场成员、权限和法债务应以当前运行数据核对。{ref('common/history/diplomacy/ce_subject_relationships.txt',185)}；{ref('common/history/power_blocs/ce_power_blocs.txt',64)}。

已接入的是有限对外政策：吴代明通知→`nesnd_crisis.21` 隐藏分发→`nesnd_external.1` 国别消息→玩家选择跟踪后 `nesnd_external_policy`。MUG 可以选择 FRA，申请真实资金/军械条约，收件人重验并可拒绝；还可在 USM 实际持有迈索尔时加 claim、关系−10。该按钮不割地、不宣战、不改变宗主；已签条约按原生规则持续，危机 JE 结束不等于自动到期。{ref('common/scripted_effects/nesnd_crisis_effects.txt',174)}；{ref('events/nesnd_crisis_events.txt',190)}；{ref('events/nesnd_external_events.txt',1)}；{ref('common/journal_entries/nesnd_external_journal.txt',1)}；{ref('common/scripted_buttons/nesnd_external_buttons.txt',241)}；{ref('common/scripted_buttons/nesnd_external_buttons.txt',459)}。

这部分已存在源码实现；其早期计划不能仍当作全未实现，也不能扩大成“莫卧儿内政/印度统一路线已完成”。计划明确保留南印度真正归还谈判、殖民地独立等为未完成范围。{ref('plans/two-empires/08-external-actions-plan.md',7,W)}；{ref('plans/two-empires/evidence/external-actions-implementation.md',29,W)}。

原版 Mughal JE 初始化受 ip2 DLC 控制，但其 `invalid = NOT exists BIC`；本 MOD 没有 BIC 开局州，所以不能把它当成可用的完整 MUG 解放流程。MOD 的 `REPLACE:je_uneasy_raj` 仍把参与者/完成/失败/政区稳定绑定 BIC；`00_east_indies.txt` 殖民巩固仍要求英国宗主。它们**没有适配成 USM 印度殖民管理或 MUG 民族主义机制**。{ref('common/journal_entries/04_mughals.txt',1,G)}；{ref('common/journal_entries/CE_04_sepoy_mutiny.txt',1)}；{ref('common/journal_entries/00_east_indies.txt',1)}。

现有统一数据库并非没有印度：MOD `BHT` 有28地区清单、75%比例与泛民族主义门槛；`MUG` 是100%文化州式形成；`DRA` 是75%文化州、泛民族主义。它们是形成机制条目，不是全套民族整合、宪政、经济改革日志；可否由具体国家形成还要核国家定义、文化和引擎规则，不把 BHT 的75%写成“21州按一次按钮必定成功”。{ref('common/country_formation/00_formable_countries.txt',576)}；{ref('common/country_formation/00_formable_countries.txt',959)}。

## 7. 作者原意、旧未来线与提案边界

作者原始 MUG 国家背景（与 pre-update 备份同条目一致）明确把它写为参加对西秦战争的旧帝国，列腐败、酒精、鸦片、外国干涉、南方明殖民地为衰落压力，提供倚法、反向靠东方、自力更生的开放分歧。它称统治集团为突厥—蒙古，而有效主文化仅 hindustani、自定义皇室 sindi；应把这个差异列为待确定设定/实现关系，不能偷偷把文化和人口改到某一种解释。{ref('localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml',30)}；{ref('backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml',30,W)}。

原始 PPT《北明ppet》SHA-256 `b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae` 本轮核对一致。第23页第6–8段记1730年代吴吞并孟加拉、法国渗入莫卧儿，1750年代饥荒，以及1770年代法英南明瓜分殖民地；**当前州历史的孟加拉属 MUG**，因此旧年代线不能直接覆盖现行1836所有权。第24页第19段给出1853–1860章西女王反抗吴吞地的第一次印度大起义；第25页第4段给出1876–1889地方村社领袖阿里借宗教动员、反抗莫卧儿饥荒统治的第二次大起义，最后由吴、法、英援助莫卧儿镇压。它支持“本地反殖民”和“反莫卧儿统治/乡村危机”可以分立，列强也可支持旧王朝；**这些后世线不是当前已经接入的定时事件，更不是必须强迫玩家走到的唯一结局**。原始资料： [北明ppet.pptx](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx>)；带slide/paragraph定位的已核SHA提取：{ref('research/20261031/北明ppet.json',2236,W)}。

对后续系统设计的直接约束：把王朝保全、印度本地民族主义、地主/种姓特权、地方诸邦主权、法国利益、吴殖民利益分别建模；“反吴”不自动等于“拥莫卧儿”，扩大国教特权也不等于全国整合。先核人口/身份/军队/公司和原版残留初始化，再谈财政行政、土地税/商业税、教育与专业资格、纺织—工具—煤铁—运输、军队供给和诸邦联邦/征服。以上是由源码提出的设计约束，**尚未实现新路线**；不得写固定改革预算、以按钮凭空产军或许诺必然工业化。

## 8. 本轮交付与证据边界

本轮产物仅在 WORK。没有修改 MOD，没有运行游戏，没有新游戏内验证声明。数字是静态历史人物数和建筑等级；不能换算为精确 SOL、GDP、预算余额、市场短缺或实际动员数。完整数据保留每块来源路径与起止行，`source_sha256` 保留完整 SHA-256；下表列关键证据指纹前16位用于阅读核对，完整值见 JSON。

| 文件 | SHA-256 前16位 |
|---|---|
'''
for p in sorted(d['source_sha256']):
    if any(s in p for s in ['mug -','10_india.txt','CE_military_formations_india.txt','ce_subject_relationships.txt','CE_04_sepoy_mutiny.txt','04_mughals.txt','ce_country_flavor','00_countries.txt','nesnd_external_journal']):
        text+=f"| `{p}` | `{d['source_sha256'][p][:16]}` |\n"
(O/'current-mod-india.md').write_text(text,encoding='utf-8')
(O/'current-mod-india-data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'current-mod-india-summary.json').write_text(json.dumps(summary,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({'report':str(O/'current-mod-india.md'),'total_population':sum(tot.values()),'MUG_hindu':pct(relig['MUG']['hindu'],tot['MUG']),'MUG_muslim':pct(relig['MUG']['sunni']+relig['MUG']['shiite'],tot['MUG']),'USM_hindu':pct(relig['USM']['hindu'],tot['USM']),'USM_muslim':pct(relig['USM']['sunni'],tot['USM']),'source_files':len(d['source_sha256'])},ensure_ascii=False))
