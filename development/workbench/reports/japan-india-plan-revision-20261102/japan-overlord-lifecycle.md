# 日本宗主关系与生命周期闭包研究

2026-11-02，研究状态。仅写工作台报告，未改玩法、未开游戏。基线为 **Victoria 3 1.13.11 / build 24799966**；本轮catalog status返回CURRENT、changed_count=0。来源SHA见同目录japan-overlord-lifecycle.sources.json。日本修订2第九节为最新作者规格，以下“建议”是实施提案，不能写成已上线或引擎通过。

已读NESND技能、路径路由、工程适配、当前交接、引用安全规则；本子任务承担背景研究。保留首都崩溃、吞并后恢复三国、原分封边界及用户接受的失国/GAME OVER；不因团结低重做分裂，不撤回JIM江南文化方向。[S2:44](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/docs/agents/engineering-skills.md:44>)[P1:145](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:145>)

## 1. 现有身份/关系：哪些是TAG，哪些不是

|事实|来源与实施含义|
|---|---|
|“吴”主要是USM的政权阶段|USM动态名读tag_WUU_var；和平代明在原USM设置该变量。保明结果记nesnd_ming_preserved。不能臆造c:WUU作为当前吴。[M1:109](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/ce_dynamic_country_names.txt:109>)[M5:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_peace.txt:1>)[M5:413](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_peace.txt:413>)|
|同一USM TAG也可能换了国家对象|反方胜者结算吞并旧USM、change_tag=USM并移除tag_WUU_var；原有请求不得只比较c:USM。NOT tag_WUU_var也不足以证明合法明帝在位，还应区分复辟、共和与未决结果。[M6:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_settlement.txt:1>)|
|明行在不是固定新TAG|HNA/SIH动态名由nesnd_ming_court/interregnum决定。承认明廷、援助明廷和实际宗主分开；不能把“拥明”当is_subject_of。[M2:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/zz_nesnd_ming_court.txt:1>)[M2:31](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/zz_nesnd_ming_court.txt:31>)|
|CNE并非永远君主沐朝|NRP胜利后吞并CNE、改TAG为CNE、启用总统共和。旧皇室协议须由新政权确认，不能只因c:CNE仍存在继续兑现。[M7:107](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_cne_republic.txt:107>)[M1:54](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/ce_dynamic_country_names.txt:54>)|
|开局JAP朝贡USM；KOR朝贡CNE|MOD重写朝贡类型允许recognized宗主，不能用原版未受承认限定纠正本项目。[M3:16](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:16>)[M3:162](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:162>)[M4:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/subject_types/ce_subject_types.txt:1>)|
|分封后关系要读实际值|现分封只对当时独立的JAP/JTK/JIM建立USM保护国，原来已为属国者不统一改类型。三国完成标记不是永久宗属。[M8:401](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan.txt:401>)[M8:451](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan.txt:451>)|
|现统一条件仍绑独立和九州、四国|nesnd_japan_is_united要求九个整州和独立；JTK/JIM完成后变显示名，没有改TAG。新方案必须把国内统一、主权、外国占有领土分开。[M10:87](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_japan.txt:87>)[M11:50](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_japan.txt:50>)[M12:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/nesnd_japan.txt:1>)|
|JIM新设定尚未落实|当前定义只有japanese；恢复helper会移除所有非japanese主流。新增ce_wuu要贯穿定义、创建、恢复、迁移，保留japanese。[M13:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_definitions/nesnd_japan.txt:2>)[M9:52](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_recovery.txt:52>)|
|林现代码仍任JAP|精确保存人物、受任国、此前统治者，设林为实际ruler。失效清理只撤委任标记，不替换ruler/继位。迁移JIM须改完整链，不能仅改标题。[M14:13](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_japan_lin_regency.txt:13>)[M15:32](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_lin_regency.txt:32>)[M15:94](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_lin_regency.txt:94>)[M16:4](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/government_types/00_nesnd_japan_lin_regency.txt:4>)|

MOD保护国/朝贡类型均可自行开始博弈，不自动加入宗主战争。因此“所有属国都不能统一战争”或“都必须随吴出征”并非引擎事实；新内容的授权须说明是具体政治协议，而非不存在的通用禁令。[M4:124](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/subject_types/ce_subject_types.txt:124>)[G13:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/subject_types/00_subject_types.txt:1>)[G12:22](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_actions/19_subject_protectorate.txt:22>)

## 2. 原版完整链条与适配边界

1. **宗属查询**：is_direct_subject_of明确排除属国的属国；is_subject_of包含。overlord为直接宗主，top_overlord为顶层宗主。林的吴方委任、直接采购许可用前者；阵营可用后者。必须先按is_subject分支，再访问overlord。[G1:11539](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/triggers.log:11539>)[G1:12447](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/triggers.log:12447>)[G3:1314](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/event_targets.log:1314>)[G3:1385](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/event_targets.log:1385>)
2. **关系失效**：原版琉球JE因RYU转入第三国、JAP/CHI变属国或国家不存在而invalid；结束事件make_independent并withdraw相关钱款条约。可借“关系变化使旧争端关闭”，不能连带删除日本内政。[G6:264](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/01_ryukyu_rivalry.txt:264>)[G7:636](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ryukyu_rivalry_events.txt:636>)[G7:647](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ryukyu_rivalry_events.txt:647>)
3. **真实供应**：create_treaty→goods_transfer定向条款→数量/商品输入→港口/邻接与贸易可达性→维护条件→物流/出口条件不足freeze。条约存在不等于履约；吞吐buff不等于交货。binding_period是约束期，不是自动到期。[G2:1030](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:1030>)[G4:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/13_goods_transfer.txt:1>)[G4:64](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/13_goods_transfer.txt:64>)[G8:3514](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:3514>)
4. **退出条约**：treaty scope支持withdraw，country参数须有效并受该条约约束；可选择apply_break_penalties。原版琉球遍历条约筛选后退出。新模块必须识别自己创建的确切合同，不能退出双方全部同类条约。create_treaty文档没有on_created参数；精确捕获拟用on_treaty_entered_into_force的窄事务登记，时序仍待验证。[G2:37390](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:37390>)[G1:3916](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/triggers.log:3916>)[G7:637](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/japan_events/ryukyu_rivalry_events.txt:637>)[G8:3408](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:3408>)
5. **JE出口**：complete、fail、invalid与各自effect分别定义。fail用于明确失败，invalid用于静默清理；“暂停”在本报告是保持JE、停止进度/行动的设计状态，不是宣称存在pause关键字。终局条件互斥，不赌同帧判断顺序。[G5:70](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:70>)[G5:128](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:128>)[G5:148](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:148>)
6. **生命周期hook**：变属国/独立为country root，换ruler为character root，转州由state处理；释放hook为释放国root、新国target。月度幂等刷新补旧档及未证覆盖入口，不假定hook捕获所有革命/吞并顺序。[G8:7574](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7574>)[G8:7607](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7607>)[G8:2889](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:2889>)[G8:7131](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7131>)[G8:3756](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:3756>)
7. **摄政**：原生天皇角色是非ruler角色；日本新君主hook限JAP owner，helper写emperor_var到JAP。通用designate_character_as_regent会加不死。建议林仍为唯一实际ruler，天皇以真实存活人物及专用角色承载；JIM须独立适配，不直接调用JAP硬绑helper。[G11:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_roles/02_unique_roles.txt:1>)[G10:3083](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:3083>)[G8:3117](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:3117>)[G9:298](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:298>)

**同市场采购须补证。** goods_transfer的visible和维护条件排除关税同盟次要成员，不能保证“属吴就能建对吴商品条约”。先核当前市场和条约合法性：跨市场使用有效条约；同市场另核真实支付/采购与供给记录。无可证接口时暂不开供应支线，工业主链仍可通过实际建设完成，不用关系+10或吞吐奖励假装履约。[G4:24](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/13_goods_transfer.txt:24>)[G4:48](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/13_goods_transfer.txt:48>)[P1:173](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:173>)

现外援链可借安全形状，但其request_valid要求南朝未结算、特定父JE仍在；不可整段复用到长期日本/印度发展。旧链30日pending、6月冷却、3月事件窗口为它自身设计；新链另定窗口/请求身份，不能凭同名pending断言等价。[M19:43](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_external_triggers.txt:43>)[M18:6](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_external_effects.txt:6>)[M20:184](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:184>)

## 3. 关系轴与内容矩阵

每次刷新重算当前事实，历史只记已发生结果：

- **国家连续性**：country对象、TAG、显示名、谱系JAP/JTK/JIM及真实创建的实例登记分开。origin只保证继承某些值，须显式成果白名单；新建/恢复不可继承旧pending。同对象change_tag不重置成果。[G2:878](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:878>)[G2:682](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs/effects.log:682>)
- **宗属**：独立/直接USM/直接CNE/其他直接宗主，另列top_overlord。USM若被CNE控制，日本可直接属USM而顶层属CNE，不能算两个直接宗主。
- **宗主身份和国内政体**：USM奉明/吴/复辟/共和/未决；CNE君主/共和/危机；日本幕府/天皇林制度/其他政体。相互独立。
- **外交与地理**：战争、博弈、停战、合作授权；国内核心、九州全有/留港/全失、四国、朝鲜；实际owner-state、贸易法和市场。
- **协议与成果**：请求对象、双方宗主快照、请求序号、父阶段、条约/项目对象及期限；产业已成、已领奖、统一历史、团结和文化政策另存。

|当前关系|统一日本|三国|变化时处理|
|---|---|---|---|
|直接USM、奉明/保明|朝贡、关税、海防协商；幕府内政不等九州|若实际出现三国，按当地制度发展，不假装吴已分封|入吴阶段重议政治许可，已建工厂学校不清零|
|直接USM、吴|维持统一、割让/归还、建设授权、自主谈判|分国立足、吴采购、三种自主诉求；JIM按直接宗属及分封结果受委任|独立后终止强制义务/吴委任，可另签商业合同|
|USM仅顶层宗主|先向直接宗主协商，涉及吴承诺再处理吴|不当成吴直接任命三国|直接宗主变化取消旧请求，顶层变化重核安全许可|
|直接CNE|发展持续，吴旧约重议，朝鲜按KOR/CNE/实际土地谈判|CNE可支持自治/统一者/分治，但有成本且需真实答复|吴方委任和供应失效，JIM文化政策不回滚|
|其他宗主|一般自治/发展，约束按真实关系|各自产业不永远等USM答复|旧宗主请求过期，新宗主不继承空授权|
|独立、与吴合作|立即发展总JE，可签供给/领土/海防协议|各自发展，不等统一；统一逐一同意|合作结束只停合同，不挡工业化|
|独立、与吴敌对|自主军工/商业，战果确认后才结算领土外交|外援、共同独立、统一战争可成可败|停对敌供给；不能每场短战反复刷团结和改革奖|

CNE还保护KOR，有朝鲜诉求、预算和内乱压力，不能无条件资助一切反吴者；承认明廷、外援者、宗主可以不是同一方。仅与第三国战争时，相关合同可受物流/财政影响，但不自动失败全国农业和内政JE。[P1:85](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:85>)

## 4. 共用闭包

每个模块填：owner、进入、持续资格、暂时暂停、complete、fail、invalid、清理、后继、重入/继承。概念状态为未解锁→可进入→活动/暂停→成功/明确失败/失效；暂停不跑终局。

possible只管进入，不能要求尚未设置的running。已满足目标的旧档登记成果，不塞瞬间完成JE。终局共用幂等effect：检查对象和唯一结算→关未完子项/请求→清本模块临时状态/局部修正→记结果→一次奖励→合条件后继。complete/fail/invalid互斥；短缺、负预算、低团结多为暂停/倒退，不能全算永久失败。

父JE结束须令旧事件cancellation_trigger成立；visible/possible不保护effect预览，option/AI权重/执行均逐层存在性守卫。拒绝只清本请求序号，不能清新请求锁。持久建设与临时项目分开；吞并前由存活方登记要移交的资料，事后不能凭复用TAG猜历史。现日本恢复已有USM主导的存活方入口。[S1:26](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/syntax-and-routing.md:26>)[M9:290](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_recovery.txt:290>)[M21:13](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_japan_recovery.txt:13>)

## 5. 五个系统的状态与出口

### 5.1 产业链与供应合同分开

产业：未解锁→核既有建设→合格本国州建设/就业/生产→持续达标→记账/后继。失州或资源暂失重选真实目标/暂停，不能给不存在矿产的国家永久死按钮。成果与当前产量分开；建筑、法律不回滚。JIM永不开放轻纺—SOL日志，不因林死或独立补发。[P1:159](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:159>)

合同：无→可提→待答复→有效→履约/暂停→完成、拒绝、超时、违约或失效。

|转移|必要条件与副作用|
|---|---|
|发起|双方存活、阶段有效、实例与许可明确、非对敌供给、市场财政可行；登记请求身份与覆盖答复期的锁/冷却，不预发奖励|
|接受|再次核双方实例、宗主/政治许可、父JE、数量/商品与can_create_treaty；真实协议成立且捕获对象后才active|
|暂停|条约freeze、封锁、暂时产量/港口/预算问题；停履约计时和对应临时收益，不每月补发|
|完成|实际履约量/期间成立；有限期产业奖一次；按合同期限退出或重新协商续订，binding_period结束不等于完成|
|拒绝/过期/失效|父任务结束、换宗主/政权/实例、对象灭亡；只清本请求，保留冷却，已实际发生成本不假装撤回|
|战争/违约/转宗主|结束该专用条约/支付，确认退出再清active；是否break penalties按已选规则，不顺便撤联盟或别人的贸易|

独立后对吴继续合作须重签或确认，不能把政治义务自动改为商业合同。本模块不向统一者、CNE或新USM静默复制旧合同；原生已继承的商业条约按实际状态与合法条款处理，政治承诺另行追认，已交付不补发。此生命周期同样适用印度法援、土邦年金；同市场采购接缝见第二节。

### 5.2 团结与文化政策

团结是持久country状态，不因换君主、独立、换宗主、改显示名重置；低团结只暂停融合并产生既定压力，不新增秦式解体。JIM ce_wuu目标来自天皇—林政权制度身份，吴委任失效或林死不撤销；后续制度变更只能明确选择今后的政策，不追溯改回已转换人口。[P1:185](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:185>)

融合资格：政策仍有效、团结>75、本月未抽样；全国一次30%，成功只选一个合格本国州；快照P=州总人口、E=非目标人口，转换min(0.1P,E)，比例min(1,0.1P/E)。E=0排除，只change_pop_culture，宗教不变。候选与实际选取条件相同；转地后重新核owner与对象，失效则本次跳过，不再抽第二州提高概率。

吞并国停止脉冲；胜者不能补跑被吞并者本月抽样。真实释放/恢复要新实例登记，按谱系恢复/初始化，不因反复释放刷70或奖励。统一团结不相加；建议保留胜者数值，以一次可见整合压力反映新增地区，幅度待核。若改选人口加权继承须事前快照，不能两种办法叠用。

### 5.3 独立发展

任一实际独立JAP/JTK/JIM立即得一次发展总JE，含统一无九州和旧档；on_become_independent即时刷新、月度巡检补漏。不能加先统一/全九州/明吴结算/天皇复位前置。工业承接成果，军制按规模，外交按真实能力。[P1:177](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:177>)[G8:7607](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7607>)

特殊场景：东征前现事件先make_independent再建博弈。总JE仍立即可见，但临时脱藩不能直接兑“主权完成”奖励，也不挡东征/首都崩溃。再附庸暂停独立行动；以后独立恢复原成果，不再发入口奖。[M17:62](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_japan_events.txt:62>)[M22:30](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_war_collapse.txt:30>)

成功关闭未完子项、开后继；重新附庸暂停独立专属子项，当地民生产业可继续；被统一承接迁移成果并关闭旧父子JE；被吞并停止实例；改共和进入相容制度路线，不清教育与工业。

### 5.4 统一

国内统一、主权、九州/四国归还分列。不能仅另两TAG不存在就统一，因为核心领土可能被外国占有；也不自动把现代北海道/朝鲜边界作为必收条件。行动资格依真实独立、原生外交能力或宗主明确认可的协议；不同宗主的日本国家不能被“同文化多数”绕过。

协商：请求→每个当事方答复→重新核实例、领土、主权→登记胜者、人物/军队/财政移交→执行并核实际结果→唯一结算。另一玩家国家不可被多数投票删除。战争按真实战果；既定崩溃/吞并后恢复照常，团结和统一JE不重跑它。

胜者保留制度、人物和法律；只合并成果集合，不叠领三个全国奖。JTK/JIM显示为日本不等于变JAP。JIM统一保持其ce_wuu政策，JAP/JTK通常japanese；只有以后明确选择改政策才变未来目标。目标灭亡/换TAG/转宗主使旧谈判invalid；拒绝/败战按具体计划fail并有冷却。失核心地重新评估现状，不擦“曾统一”历史、不重发首奖。

### 5.5 林、天皇及继位

分开四项：JIM制度来源、吴对特定人物/国家的委任、林当前职务、天皇/继承资格。当前active委任标记不能兼作文化政策。

|阶段|守卫、结果与出口|
|---|---|
|可委任|真实分封成功、JIM天皇制度、直接USM吴、林仍可合法转移；死/流亡/已在YN1或别国ruler/heir不造替身、不抢、不复活。无林也可发展|
|待转移|捕获精确人物、JIM实例、天皇承载；重试只允许人仍在原方或已转受任方；不拿新JIM替旧对象|
|在任|林唯一实际ruler；天皇真实人物+角色/国家引用；制度政策独立保存。不是两个ruler|
|吴委任失效|独立、转宗主、对吴战争、吴政权更替、吞并：清吴委任/临时效果，不强遣返或杀林，不回滚文化；林仍合法在位可转本国职务|
|个人离任/死亡|按现法律和玩家制度选择，找本国仍存活合法天皇/继承人；无合法对象走实际继承/新政体，不拿旧previous_ruler跨国抓人。团结/制度连续|

迁移旧JAP任林档只处理精确旧实例和人物、且双方合法的状态；不满足则登记未迁移原因，不全局搜索模板强抢。JIM主流ce_wuu+japanese为已批准规格，林不在或死亡也不擅自撤销。原生日本继位helper的JAP硬绑需专门适配，不能全局JAP→JIM。[M14:32](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_japan_lin_regency.txt:32>)[M15:105](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_japan_lin_regency.txt:105>)[G10:3083](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ep2_scripted_effects.txt:3083>)[P1:157](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-development-design.md:157>)

## 6. 必要异常矩阵与实施顺序

|场景|通过条件|
|---|---|
|统一有九州、留港、全失九州|均可独立发展；贸易和领土目标不互相永久锁死|
|USM保明→吴→复辟/共和；CNE被NRP替代|识别实例/政权和许可，不把显示名当TAG或旧承诺自动继承|
|日本直接USM、顶层CNE；后直接CNE|直接/间接不混；吴委任及供应收尾，JIM政策持续|
|东征脱藩→吞并→原三国恢复|发展入口幂等，无瞬间主权终奖，不抢战争结算或救援玩家|
|州归第三国/分州重建|停旧owner-state写入，重算目标，清本模块局部临时buff，不改第三国建设|
|旧回复时换宗主/实例/请求号/父JE|预览无空scope，无效不付款，不清新锁|
|约束期结束/条约freeze/手工撤约|约束期不当到期，freeze不当交付，active跟真实条约|
|林死/出走/天皇先死/制度改共和|无复制、复活、强抢；个人委任、制度、文化与继位分别正确|
|统一多个已领奖国/反复释放同TAG|成果可继承，奖励去重，新实例不接旧pending，当月融合最多一次|
|无合格文化州/人口变化/转州|无零除；全国一次30%；仅一州≤快照10%；宗教不变|
|同帧complete与fail接近|单一幂等结算、条件互斥，无双奖励或先清再误加|

顺序：关系/实例/成果登记→JIM人物文化全链→产业与供应分离→独立发展与统一去重→团结持续→继位/迟答/旧档。先查写入者、读取者、清理者和预览，再集中验证未决引擎语义；本报告未给任何新行为ENGINE_PASS。

两个计划均应给每个JE/请求填owner、入口、持续资格、暂停、complete/fail/invalid、清理、后继、重入/继承。印度法援、王朝/共同体、学校官署、土邦统一及南方主权同样需要；形成新TAG继承发展成果并重议外援/年金，但不移植日本30%/10%文化率，也不把印度改共和默认算国家发展失败。[P2:106](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:106>)[P2:59](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:59>)

待证接缝：同市场真实采购；精确新条约捕获和退出时序；吞并/重新释放后的实例引用；JIM天皇角色与继位界面；统一成果白名单的存取。已找到原生机制入口，仍须实施时核验，不能编造API填空。

技能复核：版本未变，现引用安全/身份/条约约束期规则继续适用。本子任务限报告目录，因此未改技能或MOD。来源SHA只用于复核，不是静态或引擎测试证书。
