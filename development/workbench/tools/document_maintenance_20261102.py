from maintenance_20261102_context import *
import re
RR=W/'reports/rules-poland-qin-20261102';UR=W/'reports/ui-trade-feedback-20261102';orig=W/'backups/pre-update-20261030T233944Z/mod'
# Deduplicate presentation only: raw inventory retains individual vanilla substates.
p=RR/'qin-cultures.md';s=read(p);out=[]
for line in s.splitlines():
 if line.startswith('|') and '；' in line:
  cols=line.split('|');cols[-2]='；'.join(dict.fromkeys(cols[-2].split('；')));line='|'.join(cols)
 out.append(line)
write(p,'\n'.join(out)+'\n')
write(R/'original-rule-decisions.md','''# 原 MOD 差异的本轮处置

基线f18b6c4→044de73；详细源码和行号见 ../rules-poland-qin-20261102/original-rules-audit.md。原扫描33日志/106事件/179选项，51个日志词法差异不是51个BUG。此表记录本轮选择，未恢复项不冒称等价迁移。

|差异|本轮处置|判断|
|---|---|---|
|旧五条土改子日志：逐州市场85%、西秦关系/领土、南朝关系/领土、六科技、法律组合；各有一次性奖励与年度惩罚|搁置旧精确规则，保留原ID与全文备份|新土改已按用户要求围绕土地商品化、城市化、营产与信心运行。立即并回旧奖励会重复计分，外交战争要求也会改变正在设计的两朝/西秦节奏；应在后续内容批次逐项接入，而非称其已迁移。|
|旧农村IG年度+3/+1、地主/儒生年度失败+3|维持现制|现有月度IG合作、实际项目损益和信心承担另一套明确作用，简单叠旧年度会双重惩罚。|
|失败条100即失败|维持现制|当前0信心、失君主、原生内战、政变及持续严重危机均可失败；原单一条满格失败不是当前批准目标。|
|完成自动自耕农法→当前先落实地权制度|维持现制|新系统允许自耕农、商业农业、集体农业；完成时强制改法会覆盖玩家已选制度。|
|少于四州失效、首都陷落后吞并|已恢复，保留|本轮前已上线；不重做已恢复机制。|
|USM原生革命进度95%即中止|搁置旧阈值|95%尚不是战争爆发；简单恢复invalid会提前掐断现有南朝统一结算，且旧出口不覆盖新变量。后续政治重构需按实际爆发而非预兆做中断/清理闭包，记录为未恢复。|
|反叛胜利的USM附属/单南京路径→占领门槛与统一结算|保留现制，旧捷径搁置|单一领土/附属关系未必代表这场战争胜负；当前需真实敌占与首都事实。若另做和平臣服结局，应接统一结算而非恢复抢先结束。|
|选择立场730→180天、有反对者转战争|保留现制|已批准四年内推动首辅案和内战的节奏。|
|日本中立资格、九州旧完成条件、崩溃|本轮不改|用户明确日本维持当前版本；专用文件逐字保护，混合文件日本定义AST保护。|
|波兰继承的11项缺陷及迟到请求/结算漏洞|修复|目标scope、同一候选筛选、一次结算、玩家迟答与国家存在性都能从源码证明；详见修复映射。|
|波兰GDP排名30边界、基础设施用量0.3–0.9、默认AI按钮权重|暂不改数值|属于单位/平衡或引擎默认行为待核假设，不能凭静态猜测把原设计改成另一套。现有确认BUG已独立修复。|
|鸦片目标200/600及进口/出口差异|保留统一目标helper|旧JE与事件选目标条件不一致；现版同一候选集合更完整，不能为还原原文恢复死按钮。|
|琉球、传教、太平入口禁用|维持|原始版本即禁用，并非本次代理删掉功能。|

未恢复旧规则不是已修复的BUG，也不证明旧版当时实际运行正确。西秦新内容仅形成实施方案，未混进本轮修复。
''')
write(R/'poland-fix-map.md','''# 波兰修复与未决假设

对照 ../rules-poland-qin-20261102/poland-audit.md。原始11项均继承自最初MOD，本轮未改变其复国政治立场与地区名单。

|编号|修复|
|---|---|
|F01|波森目标保存实际state，拒绝state_region进入set_state_owner。|
|F02|十个最后通牒检查/选择同一组外国州；西加利西亚已拥有一部分仍可要求外国部分。|
|F03|终局前保存阵营；成功/失败世界效果在immediate一次执行，延迟点击仅确认。|
|F04|两项针对本国/克拉科夫的激进化改用random_scope_state，防止误落世界其他州。|
|F05|战争回调给实际进攻方改阵营。|
|F06|过多声索惩罚读取非负声索数，去掉对负计数>=3的死条件。|
|F07|反对事件按max(原值−10,0)扣各自正确的进度条；15变5，不再变0。|
|F08|后来进入问题的国家加入实际全局日志参与者，并获得一次立场邀请。|
|F09|资助事件保存实际强国scope，使通知中的发起人有效。|
|F10|波兰或联邦各自满足独立、至少三直辖州即可终止旧复国问题；不再要求两国同时存在。|
|F11|备战按钮消耗备战条；支持国消耗本国领土诉求条，门槛和扣除一致。|

追加闭包：同一KRA/目标/类型的外交博弈；拒绝已参战/已承诺博弈或受保护目标；迟到最后通牒、参战邀请、立场选择均取消/执行时重检；pending对象身份先查存在再比较；宣布胜利重算真实地区并锁一次；LIT/BYE已存在时转交对应州而不重复建国；维持双方原战争目标和原无地10%激进化后果。

仍属假设而非已证BUG：原GDP排名30重叠加值、基础设施用量系数、部分按钮缺显式AI权重。这些暂保留，理由见original-rule-decisions.md。未运行游戏，外交博弈创建与全局JE时序仍由用户验收。
''')

# Preserve every changed localization item for editorial review, not just a search result.
pat=re.compile(r'^ ([\w.]+):(?:\d+)?\s*"(.*)"',re.M);entries=[]
for p in (C/'localization').rglob('*.yml'):
 rel=p.relative_to(C);old=dict(pat.findall(read(B/rel))) if (B/rel).exists() else {}
 for k,v in pat.findall(read(p)):
  if old.get(k)!=v:entries.append({'file':rel.as_posix(),'key':k,'before':old.get(k),'after':v,'editorial':'pass','engine':'NOT_RUN'})
dump(R/'writing-items.json',entries)
sources=[]
for file,keys in [('ce_cne_events_l_simp_chinese.yml',['ce_cne_land_reform_reason','flavorCNE.3.d','flavorCNE.4.d']),('ce_french_empire_journals_l_simp_chinese.yml',['ce_french_support_dynasty_button_desc','ce_french_empire_oreleans_progress_bar_desc'])]:
 p=orig/'localization/simp_chinese/replace'/file;vals=dict(pat.findall(read(p)));sources.append({'file':str(p),'sha256':sha(p),'samples':{k:vals[k] for k in keys}})
dump(R/'author-samples.json',sources)
write(R/'writing-comparison.md','''# 玩家文本对读与删减

独立技能 nesnd-player-writing 实际取样见author-samples.json（原始备份SHA），全部变化逐项见writing-items.json；原始CNE日志直接写trigger与进度目标，法国条用原生读数，不能反过来把代理的大段custom_tooltip说成作者习惯。

|作者样本／职责|失败旧文或展示|本轮处理与判定|
|---|---|---|
|原地权革命_reason按历史、利益与行动展开；状态只需当前事实|土地商品化状态复述科技、农业6%、行政、破产等整组按钮条件|空闲状态留空；推行时仅写“土地商品化正在推行。”。通过：不抢按钮职责。|
|原法国按钮明确行动立场，trigger原生展示条件|五州城镇和全国七类工业、福利条件压成一个叉|科技、法律、福利机构、五州城镇、七种全国建筑分项原生显示。通过：各自真假独立；不是靠给原长句加换行。|
|原法国条直接显示当前进度|初始状态预告500起义和破产−500|初始只谈对大革命未竟之业的信任；信心低于750时请愿增多，真实与NRP交战时才写举兵。通过：条件化叙事。|
|原作者CNE事件先讲行动及政治结果，非更新记录|“统计口径”“子项目”“按原规则”等|没有进入新增文字。主完成条件法律/机构等原生显示；自定义聚合只说明确实无法直接本地化的民生与计数。通过。|
|选项实际effect说明关系变化|原生关系+10后再次重复“双方关系+10”|只留“建立通商联络。”，一次+25由真实原生effect展示。通过。|
|按钮提示应给决策信息|使团提示重复修正数值|只补七日抵达和六个月任期；原生修正显示−100。通过。|

用词/用字：沿用地方失序、土地商品化、国家城市化、大革命；没有把行政保护讲成玩家资格。断句：短状态只承担一件事，统计条件不用叙事长段。造句：明确谁行动、何时发生，不写“不是X而是Y”的助手式辩护。冗余：删除重复门槛与效果数值。内容视角：无更新历史、设计推理或未发生起义的预告。脚本契约：阈值、状态分支、来源和实际效果逐项对照，未做UI截图或引擎验收。

返工记录：早期aftermath写“举兵者的旗帜已经倒下”，会过度断言共和军命运；改为“战事的震荡尚未平息。”，与已起义但当前不交战的条件一致。此处只描述余波，不假定是哪方胜利。数值提示保留已检查的统计例外，不把所有内部变量直接暴露给玩家。

西秦剧情另有完整初稿、返工与再审：../rules-poland-qin-20261102/writing-skill-trial.md。纯提案与实际落库分级已写入技能。
''')

# Resolve actual initial region names from effective Chinese localization.
loc={}
for p in sorted((C/'localization/simp_chinese').glob('*.yml'))+sorted((C/'localization/simp_chinese/replace').glob('*.yml')):loc.update(dict(pat.findall(read(p))))
regions=json.loads(read(W/'reports/cne-reform-subjournals-20261101/initial-inventory.json'))['regions'];names='、'.join(loc.get(x,x) for x in regions)
write(R/'release-notes.md',f'''# 2026-11-02：条件展示、波兰事件链与波斯朝贡

父版本044de73；候选{C.name}。主MOD及Git合入事实以main-merge.json、git-delivery.json为准。STATIC_PASS / ENGINE_NOT_RUN；用户明确自行开游戏，本轮未启动游戏。

## 已实施

- CNE城市化：5州各有5级城镇中心独立；全国铁25、煤40、钢10、工具30、发动机6、伐木60、船厂12各自原生勾叉，另列科技、法律、社保。去掉七个手工累加脚本值。
- 土地、城市、营产的政力/破产/失序启动护栏只约束AI；拨款保留真实国库与社保资格，AI谨慎检查分开。主日志完成条件仍要求原有民生与制度，不借UI修改悄悄取消。
- 日志状态只讲当前阶段，信心初始不剧透共和起义；USM去掉重复遣使挂载。可直接显示的条件用原生trigger，复杂派生统计保留短提示。
- 波兰11项确认缺陷与迟答/结算/现存TAG闭包已修，详见poland-fix-map.md。原作者阵营与地区目标保留。
- 商使修正−100/6月，门槛100；首次建立通商关系+25，每发起国仅一次；完成奖励+100/24月仍仅一次。所有请求标记覆盖7天旅行+3月回复窗口，失效事件取消。关系实际范围−100至100，影响力无统一1000上限。
- PER新开局成为QE1朝贡国。现版tributary已允许recognized宗主，不改朝贡类型数据库；只删旧诏不相容的防御条款，投资与贸易权保留。**已有存档不自动重写宗属**，防止吞掉合法独立结果。
- 安装独立nesnd-player-writing，主技能强制路由；新增数值量纲检查，规定原生条件优先、AI门槛分离、条件式短状态和单一说明位置。

## 改革地区的实际含义

取当前本国拥有、匹配is_modern_china_state的州，再加盛京、外东北、黑龙江北部。不是所有未来占领地区，也不是全世界。当前开局22州：{names}。城市化工业总等级读取全国；农业6%和民生采样使用上述改革地理范围。营产按钮固定以开局22州为名，并随实时归属隐藏/清理。

## 原始规则与西秦方案

原始判定报告见 ../rules-poland-qin-20261102/original-rules-audit.md；本轮修复/保留/搁置理由见original-rule-decisions.md。五条旧土改外交、市场、科技、法律任务的精确奖励没有恢复，不能称与新系统等价。日本按用户要求保持当前机制。

西秦方案：../../plans/two-empires/20261102-western-qin-design.md，包含PPT依据、开局危机、文化团结与复归、皇权/地方士人/军队、波斯/印度/俄国、东归和解及文件调用结构。是实施方案，未上线这些新玩法。

文化清单：../rules-poland-qin-20261102/qin-cultures.md。西秦初始39,713,582人、35文化、22传承，三主流65.46%。按province对齐后，满文化在全境缺席；维吾尔、乌兹别克等主要是地区缺席，其他州仍有人口。两组部分覆盖地区不虚构精确移除数量。

## 验证与边界

90项源码/AST/闭包检查，202个实际扣条分支算术样本，Tiger无新增诊断（继承6 errors / 966 warnings / 2 tips；工具按1.13.5建库，本机1.13.11），5项实际MCP源码查询。两轴最终审查无未关闭的确认问题；Standards因代理数量限制复用了独立审查上下文，已记录。继承诊断不是本轮修复完成全部MOD的证明；本轮没有添加忽略项。

未验证：游戏UI布局、事件取消调度、战争博弈/自动条约维护、历史关系加载和具体难度。地图、人口、建筑、肖像与日本专用文件没有变化；代码格式调整有AST相等证明。正式包不含QA工具、开发文档或测试脚本，原始与每轮版本继续保留。
''')
issue=C/'.scratch/debug-release/issues/15-ui-poland-qin.md'
write(issue,f'''# 15 条件展示、波兰修复、朝贡与西秦规划

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: /root
Blocked by: none
Validation: STATIC_PASS
Evidence: [{R.name}](<{R.as_posix()}/release-notes.md>)

## Result

按本轮7项新增与前文审计/文风/西秦要求实施。28个玩法/本地化文件差异，零删除；原生全国建筑条件、AI护栏与玩家门槛分离、条件式信心状态、USM去重、波兰11项及请求闭包、商使100/首次关系25/一次完成奖励100、PER朝贡历史。日本维持现制。

原MOD差异逐项修复/保留/搁置；独立写作技能与数值契约已维护。西秦故事、文化清点和文件结构仅为方案，尚未实现。详情以Evidence链接为唯一完整记录，旧任务13/14与旧审计保留。

90项源码检查、202个扣条算术样本、Tiger零新增、MCP5、两轴复查；未开游戏，不将源码通过称引擎通过。用户自行验收。PER变更适用于新局，已有档不自动强改外交。
''')
p=C/'.scratch/debug-release/map.md';write(p,read(p)+'''\n\n## 最新：原生条件、波兰、朝贡与西秦方案（2026-11-02）

[15 条件展示与波兰修复](issues/15-ui-poland-qin.md)：原生勾叉与全国建筑查询、条件式短状态、USM遣使去重、波兰11项和迟答闭包、商路数值、波斯朝贡历史已完成外部验证。独立写作技能与数值契约已更新；原MOD规则审计、西秦文化清单及实施方案另存WORK。日本保持，未开游戏；实际主MOD/Git交付看任务15的release-notes/main-merge/git-delivery。
''')
write(S/'references/active-work.md',f'''# 当前交接：原生条件、波兰修复与西秦方案

Updated: 2026-11-02。当前候选{C.name}，父版本044de73。主MOD/Git实际状态以[交付记录](<{R.as_posix()}/release-notes.md>)及同目录main-merge.json、git-delivery.json为准；[任务15](<{M.as_posix()}/.scratch/debug-release/issues/15-ui-poland-qin.md>)为入口。旧交接逐字备份于本轮skill-before。

完成：CNE原生全国建筑/分项条件、AI护栏分离、短状态；USM遣使去重；波兰11项与迟答/终局/存在性闭包；商路数值和请求期限；PER新局朝贡。日本、地图/人口/建筑/肖像保留。90源码检查、202算术样本、Tiger零新增、MCP5、两轴复核。未开游戏，ENGINE_NOT_RUN。

独立写作流程入口为nesnd-player-writing；每次改数值必读numeric-scale-contract.md。西秦新内容仅实施方案，详见WORK/plans/two-empires/20261102-western-qin-design.md；原始规则差异及暂缓项见本轮original-rule-decisions.md。南朝新概率/密使仍未实施，保留原任务图。不要重跑一次性构建脚本覆盖后续修订。
''')
print('Reports, rule decisions, writing comparison, task15 and skill handoff saved.')
