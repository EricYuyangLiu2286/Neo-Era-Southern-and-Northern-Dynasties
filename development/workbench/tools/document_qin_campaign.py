from qin_persia_context import *
from datetime import datetime, timezone
import re

# Documentation edits retain independent pre-edit copies. Candidate only for game files.
archive = R/'documentation-before'
def preserve(p):
    dest=archive/(p.relative_to(S).as_posix() if p.is_relative_to(S) else p.name)
    if p.exists() and not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
def append(p,text):
    preserve(p);write(p,read(p).rstrip()+'\n\n'+text.strip()+'\n')

# One editorial correction: the actual law-speed cost affects landowners, not soldiers twice.
old='朝廷责成官员加紧议法，军府与军士的反对不得再使议程久拖不决。'
new='朝廷责成官员加紧议法，军府与地主的反对不得再使议程久拖不决。'
for lang in ['simp_chinese','english']:
    p=C/f'localization/{lang}/replace/zzzzzzz_nesnd_qin_persia_l_{lang}.yml'
    txt=read(p);assert old in txt or new in txt
    if old in txt:write(p,txt.replace(old,new))

author=W/'backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace'
selected={
 'ce_cne_events_l_simp_chinese.yml':['ce_cne_land_reform_reason','flavorCNE.3.d','flavorCNE.4.d','flavorCNE.4.1'],
 'ce_usm_events_l_simp_chinese.yml':['ce_usm_conflicts_within_reason'],
 'ce_french_empire_journals_l_simp_chinese.yml':['ce_french_support_dynasty_button_desc','ce_french_empire_oreleans_progress_bar_desc']}
samples=[]
for file,keys in selected.items():
    p=author/file
    for i,line in enumerate(read(p).splitlines(),1):
        if any(line.strip().startswith(k+':') for k in keys):
            samples.append({'file':str(p),'sha256':sha(p),'line':i,'text':line.strip()})
dump(R/'author-writing-samples.json',samples)
loc=C/'localization/simp_chinese/replace/zzzzzzz_nesnd_qin_persia_l_simp_chinese.yml'
entries=[]
for i,line in enumerate(read(loc).splitlines(),1):
    m=re.match(r'\s*([\w.]+):\d*\s+"(.*)"$',line)
    if not m:continue
    key,text=m.groups()
    category=('事件正文' if key.endswith('.d') else '日志正文' if key.endswith('_reason') else
              '按钮说明' if key.endswith('_button_desc') else '进度与效果' if '_bar_desc' in key or key.endswith('_tt') or '_delta' in key else
              '状态与名称')
    assert not any(bad in text for bad in ['子项目','参见三个子日志','按原规则','统计范围与','多组符合时仍只计算一次'])
    entries.append({'key':key,'line':i,'category':category,'text':text,'editorial_result':'通过',
                    'reason':{'事件正文':'行动者、动机与结果连贯；动态地区使用保存的地区scope。',
                              '日志正文':'说明历史处境及政治经济目标；不复述按钮门槛或预告未生效终局。',
                              '按钮说明':'说明行动；逐项条件与原生效果由脚本展示。',
                              '进度与效果':'短来源名或必要期限/比例；原生条承载持续增减。',
                              '状态与名称':'沿用已定专名、简短状态或角色表态；无开发过程文字。'}[category]})
dump(R/'writing-items.json',{'editorial_review':True,'engine_render_verified':False,'source_sha256':sha(loc),'entries':entries})
write(R/'writing-comparison.md','''# 西秦与波斯玩家文本对读

作者样本取自修改前独立原始备份；文件、行号、SHA及完整条目见 author-writing-samples.json。本轮全部有效新键及逐项结论见 writing-items.json。中文版与英文槽同键，英文槽目前使用中文回退，不声称完成英译。源文、PPT事实与本轮创作分开；本轮新台词不冒称作者旧稿。

|类别|作者原文证据|本轮候选|判断与处理|
|---|---|---|---|
|日志|地权革命从1810西秦革命讲到解除宗族束缚；南朝日志以朱、郑之争落到乡校和议会|“秦军退守伊犁以后……”由败退、恢复生产写到安国派与军府的要求|保留具体历史、行动者与利益因果，不把政治改写成按钮说明。篇幅按本轮小日志缩短。通过。|
|事件|flavorCNE.4.d以法律机关、争夺与背叛表现改革阻力|“被排除在朝议之外的官员与军人已经集结成军……”|有明确主语和动作；不只说失序或阈值。通过。|
|选项|“胡言乱语，正不必忧心。”表达人物立场|“先养民力。”“整饬军政。”|是国家的选择，不重复即将发放的buff表。通过。|
|按钮|法国拥护王朝按钮直接表达阵营主张|“裁军兴业”说明将朝廷力量投入安国之策|政治行动与代价对应，条件单列原生勾叉。通过。|
|返工|地权革命原文明确被改变利益的阶层|责令议法初稿写“军府与军士”，代码实际降低军队和地主支持|初稿重复军队而漏地主；改为“军府与地主”，两语言槽同步，复核通过。|
|进度|法国原生条直接显示当前值/总值|平衡点−50..50、文化团结、暴动与三权各显示真实条值|月度原因由原生条逐项列出，正文不再抄算式。通过。|
|条件式状态|本轮用户明确要求按trigger出现，不提前公开共和起义|团结低于阈值才出现离心状态和暴动日志|玩家初始仅见当前处境；后续危机有自己的正文。通过。|

逐项审查覆盖用词、断句、主语动作、重复、视角与脚本对应。标题、短读数、资源壳名称无需强写历史叙事；文化转换内部临时文化只显示既有“西域汉羌”名，没有另造玩家身份。波斯五组宣称按钮各自可独立悬停，说明同类规则属于必要复用，不是在同一面板把数字说两遍。

新增规则仅收录“文本须点名实际承担代价的集团”；其余已由独立写作技能覆盖，不重复堆规则。以上为编辑与源码审查，未运行游戏核对排版或动态渲染。
''')

pools=json.loads(read(R/'future-identity-pools.json'))['states']
dump(R/'identity-implementation-mapping.json',{
 'status':'final implementation mapping','regions':len(pools),'paired_choices':sum(len(x['return_pairs']) for x in pools),
 'initial_regions':36,'initial_native_pairs':174,'reversion_field':'return_pairs',
 'reversion_filter':'All native region culture/religion pairs; no Sinosphere exclusion.',
 'assimilation_filter':'Only non-Sinosphere cultures; religion unchanged.',
 'weights':'Original native population reference, not exact ancestry of current MOD population.',
 'conversion':'Three fresh pop traversals; stage half, convert all staged religion, convert all staged culture.',
 'heritage_cache':'Bootstrap maintenance and monthly refresh; potentially twice per month, UI reads cache.',
 'engine_verified':False})

plan=W/'plans/two-empires/20261102-qin-persia-implementation.md'
append(plan,'''## 最终落地与来源边界

本节补充设计初稿；实际源码、最终检查和交付以 WORK/reports/qin-persia-20261102/release-notes.md 为准。12个新日志、51个玩法/本地化文件。原始国家地图、人口、建筑、人物与日本系统保留，两个国家history仅追加幂等入口。

- 经济建设为工具20、铁路10；军事建筑在开局大厅结束后读取实际营房数，以此加25为目标，并有次日/旧档月度恢复入口。历史82级营房与36个编制单位不能互换。军事预算六个月一次，支出一周收入、至少10000，军需品−10%、军队支持+1和平衡+10；AI另核可用资金。
- 端点计时29天，周度判定首次满足通常要到下一周；持续超过四周。十年country时钟保留，重新添加JE不延长期限。一次普通秦国内部战争不自动结束朝议，少于4州才按失效关闭。
- 文化复归覆盖原版677地区3001文化/宗教配对；原始36秦地区174配对全部保留。非中华文化圈限制仅用于归化，不过滤复归候选。新建分裂国接纳本地文化及西域汉羌；已存在国家的文化/宗教不重写。
- 文化团结按非主流传承汇总人口，某传承至少占1%才计入多样性压力，每组−0.05；缓存于初始化/维护和月度刷新，可能一月两次，不重复扣团结。UI不遍历人口。三权另保留显著文化数量这一不同指标。
- 解体保留伊犁、准噶尔、西益的现有秦土；36原始地区各只分配一次，新增征服地由西部诸省联邦接收。各国加入同一反秦战争，90天启动窗口，一次开战锁；不夺第三国土地，不替玩家保国。
- 各原生条显示公式，自定义变量是唯一结算来源。暴动由团结主JE结算，暴动JE同步镜像；两种月度回调顺序都需绝对同步，不叠加第二次。
- 波斯三类援助事件各自检查六个月修正存续；未来结算不依赖已从列表移除的本JE。后继显式添加兼有possible入口。完成时若已属第三国，不强抢其宗属关系。
- 单向生活水平奖励为州×职业的月度变化采样：基础系数与农民折减、较高生活水平折减参考原版define；净变化与月内涨跌不等价，属于近似。技术/法律组合采用本机实际法组和启用钩子，皇权路线为君主制＋技官制。

外部检查和双轴审查通过；用户要求不开游戏，运行时人口批次、战争联盟及时序仍需用户实机观察，不能宣称引擎零BUG。
''')
append(W/'plans/two-empires/20261102-western-qin-design.md','''## 2026-11-02 实施进展

用户新规格已经形成独立候选，具体数值和文件闭包以同目录 `20261102-qin-persia-implementation.md` 及 WORK/reports/qin-persia-20261102/release-notes.md 为准。旧方案保留作剧情与原始文化研究来源；不是逐条原样实现，也不覆盖最新明确规格。未运行游戏。
''')

append(S/'references/numeric-scale-contract.md','''## 有界算术与单向生活变化（1.13.11，西秦实证）

script_value 的 `min` 是下限、`max` 是上限；以当前原版实例核验，再执行真实AST的边界算术，不凭自然语言误读。两者颠倒会把人口比例、力量和收益推到极端。
SoL带来的“额外15%效忠”是对对应新增量乘0.15，不是每月把全国15%人口变成效忠派。当前原生仅有双向合并修正；需要单向时先记录近似边界，再按原版define的基础量、农民折减及高SoL折减采样。月度净变化无法还原月内所有涨跌。来源及720样本见 WORK/reports/qin-persia-20261102/native-political-contracts.md、sol-approximation.json、arithmetic-cases.json。
''')
append(S/'references/journal-text-contract.md','''## 非开局入口、终局回调与镜像条

新增父子JE或后继JE时，画“初始化→添加父JE→添加子JE”有向图；初始化effect不反向添加自己的JE。possible不能正向依赖自己的has_journal_entry；完成effect判断持久资格、进度和done，不要求该JE仍在活动列表。显式添加与自动possible入口共用终局锁，维护回调补漏不重置既有进度。
有期限的JE保留country期限标记，意外移除再添加不得刷新十年；端点保持时间必须离开后清除重计。军事基线在大厅结束后读实际建筑数量，日志初始化过早时使用有界次日恢复及旧档月度入口，不能把未初始化的0当正常基线。
通常由本JE独占country结算及条同步；父/子需要镜像时仍只有一个country写入者，每个JE自身回调做绝对同步，并覆盖两种回调顺序。外部顺序模型只证明脚本约定，不能替代引擎时序验收。实例与12项生命周期矩阵见 WORK/reports/qin-persia-20261102/。
''')
append(S/'references/syntax-and-routing.md','''## 1.13.11 本机接口与创建回调

IG判定用当前script_docs的 `ig_clout` / `ig_approval`；不能将scope列表中的简名误当trigger。文化数据使用 `heritage` / `language` / `traditions`，特质查询用 `has_discrimination_trait`。营房标准键是 `building_barrack`，历史复数别名需确认解析后再统计。
跨 `create_country.on_created` 回调不假定外层root或saved scope自动可用：对固定国家先exists再进入c:TAG；遍历内确需回到调用country时按实际scope栈用prev，不能把全局history或after-lobby的none root当country。原版链条、错误名纠正与最终检查见 WORK/reports/qin-persia-20261102/native-political-contracts.md、source-name-corrections.json。
''')
append(S/'references/content-development.md','''## 人口文化与宗教的成对转换

同时转换同一半数人口的文化与宗教时，分别在原pop调用两次0.5不保证作用于同一批。西秦方案先暂存半数为内部文化，再用两个全新人口遍历完成宗教和目标文化，并清理异常残留。原生接口有出处，但三遍组合仍须引擎观察。临时文化要有完整文化、六类静态修正、三类modifier定义及本地化资源链，开局不创建此文化人口。
地区复归取原版实际存在的文化＋宗教配对及参考权重；保留配对，不分别随机。归化与复归的过滤资格分别来自用户规格，不能把“仅同化非中华文化圈”误套到复归。原版分布是剧情参考，不是作者现有人口的精确祖源。新生国家身份仅在on_created设置；现存国家保持原有文化、宗教和第三方土地。实例及局限见 WORK/reports/qin-persia-20261102/native-identity-breakup.md、identity-implementation-mapping.json。
''')
writing=S.parent/'nesnd-player-writing/references/author-samples.md'
preserve(writing)
append(writing,'''## 代价承担者对读

2026-11-02西秦“责令议法”：初稿写“军府与军士”，实际effect降低军队与地主支持；改为“军府与地主”。作者地权革命正文逐一指出转出与取得利益的阶层。写按钮时据effect点名实际承担者，不能用相近政治名词替换。完整原文与逐条复核见 WORK/reports/qin-persia-20261102/writing-comparison.md。
''')

issue='16-qin-persia-campaign.md'
write(C/'.scratch/debug-release/issues'/issue,f'''# 西秦与波斯日志群

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [{R.name}](<{R.as_posix()}/release-notes.md>)

## Scope

按用户最新西秦/波斯九项要求实施12个JE与配套按钮、事件、进度、法律、文化转换和战争闭包。原始地图/人口/建筑/人物、日本及其他国家既有日志保留。不开游戏。

## Result

独立候选 `{C.name}`，父版本c0e11fe。源码与外部检查通过；双轴审查无剩余问题。实际主MOD合入、备份、压缩包与Git保存以证据目录的main-merge.json、package.json、git-delivery.json为准，未运行引擎。

皇权路线采用原生君主制＋技官制；两种同法组法律不能同时生效。生活水平单向效忠/激进奖励使用定向采样，非原生精确modifier。完整规则、各JE入口/终局/一次性保护及限制见实施规格和release-notes。

南朝新概率/密使仍在原任务图，未混入本次西秦实施。构建脚本是历史一次性工具，后续维护直接改已审源码，不能批量重跑覆盖修订。
''')
append(C/'.scratch/debug-release/map.md',f'''## 最新：西秦与唐衣大食（2026-11-02）

[16 西秦与波斯日志群](issues/{issue})：朝议三日志、文化团结/暴动、恢复故土、三权，以及波斯常驻内政/经济、前途与东西战争路线共12个JE。已完成外部核查和双轴审查；主MOD/Git交付以任务16证据为准。ENGINE_NOT_RUN，用户自行测试。旧记录和南朝新政治待办保留。
''')
preserve(S/'references/active-work.md')
write(S/'references/active-work.md',f'''# 当前交接：西秦与唐衣大食

Updated: 2026-11-02。候选qin-persia-campaign-20261102-a，父版本c0e11fe。[任务16](<{M.as_posix()}/.scratch/debug-release/issues/{issue}>)和[交付记录](<{R.as_posix()}/release-notes.md>)为当前入口；实际主MOD/Git/压缩包看同目录main-merge.json、git-delivery.json、package.json。上一份交接保留于本目录对应报告的documentation-before。

12个新JE及完整配套：短期经济/军府争权、团结归化与复归、暴动解体、故土奖励、三权法律路线、波斯援秦或秘密运动和后继扩张。原始人口/地图/建筑/人物/日本保留；只追加QE1/PER历史入口。外部源码、边界算术、Tiger差分、实际MCP查询与两轴审查；未开游戏，ENGINE_NOT_RUN。

实施规格为 WORK/plans/two-empires/20261102-qin-persia-implementation.md。原生君主＋技官取代不可共存的专制＋技官；单向SoL奖励为月度采样近似。文化三遍转换、动态战争联盟及引擎回调仍未实机核验。原版677地区配对不代表真实祖源。

不要重跑一次性构建脚本覆盖后续修订。技能新增证据分别在numeric-scale-contract、journal-text-contract、syntax-and-routing及content-development末节。南朝概率/密使任务仍未实施，保留原任务图；以前的日志修复与实机记录只覆盖各自版本。
''')
print('Documented style review:',len(entries),'keys; metadata, skills, task and handoff updated.')
