# 西秦 QE1：设定与原生接口核查

日期：2026-11-02。范围：只读研究与方案证据；未改主 MOD、技能、Git，未启动游戏。本文件的接口结论是当前源码和已有 script_docs 支持，不是本轮实机验证。

后续用户明确修正：波斯应为西秦朝贡国，已授权修复。本文3.1关于独立PER的记载是修复前脚本审计，不再代表目标设计。类型限制、最小改动及旧档边界见 WORK/reports/ui-trade-feedback-20261102/persia-tributary-research.md；父任务负责实施。

## 1. 来源与指纹

- MAIN：D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties。
- GAME：D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game。
- WORK：D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench。
- 运行技能 catalog.py status：1.13.11 / Steam build 24799966，CURRENT，changed_count=0。
- 原设定：D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx。
- 本轮直接计算 PPT SHA-256：b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae；与 WORK/research/20261031/北明ppet.json 中 sha256 完全相同，故读取该缓存 records 原文，保留 slide/paragraph 定位。
- 引擎文档：WORK/references/engine-docs-1.13.11-20261031/；provenance.json 记录 Victoria 3 script_docs、1.13.11 / 24799966，生成时间 2026-10-31T01:04:00.740379+00:00。部分生成文档里的示例存在乱码/误拼，以下只取清楚的原生条目，并以当前 GAME 实例交叉确认。
- 已读 NESND 的 paths、narrative-context、system-design-and-plans、content-development、syntax-and-routing，以及项目 engineering-skills/domain、当前 map；本轮无需改变技能规则。

本文 GAME/MAIN/DOC 路径前缀分别指上述 GAME、MAIN、WORK/references/engine-docs-1.13.11-20261031。人口总量与逐州构成由主任务另行核算，本文3.1仅引用总量并链接该清点报告。

## 2. 原文确证与本轮分支

### 可作为前史的原文

|来源|确证内容|方案含义|
|---|---|---|
|PPT slide 3 p8–10|秦国从耕战诸侯转向殖民贸易国家；火器、民兵与大规模征兵使旧封建职业军人衰退；西北贸易地区宗族/地主权力受压，新兴资产阶级成长；秦帝国曾远征波斯、叙利亚、西伯利亚|西秦并非单纯游牧军国，地方商贸、书院与军府经济都能提供改革基础|
|slide 10 p5–9|1810年军饷贪墨、军资拖欠及军事地主集团行为，使青年军官请愿升级为革命；牧仲棠、吴省领头；1812共和国成立；1814陈东阳阐述万族主义；1815青年派执政，陈任周公、吴任召公；牧、吴、陈、邓明舆为“共和四子”|财政、军队、代表制与文化包容之间的矛盾有原文根据；不可把上述革命领袖无条件重新生成到1836西秦|
|slide 12 p20、22；slide 13 p4–12|1821年九月陈秦残部动员安西、安北、安南、波斯四军府，四十万号百万进关中；十月牧仲棠会张百里、费西翼于兰州破秦；苏宏西进斩秦愍宗；残部退守伊犁，号西秦；皇族仍“东顾玉门”，军士和武勋集团不敢再提东征，转与俄国、波斯、莫卧儿争西亚霸权|开局“恢复国力还是军事戒严”的主要张力已存在；东征必须重新取得军界支持，不能当1836全民现成共识|
|slide 21 p16–24|16世纪征阿富汗、入印度、与俄合作；前三次近西战争扩张；河中大疫；第四次近西战争1716–1730败北，西征衰落；冯小奎编史|中期的西向战争是重拾旧势力范围、处理旧军府与地方秩序，不是新发现的大陆|
|slide 22 p22|1673–1704波斯贤王阿兹丹（汉名陈玉梁）凭商贸、技术进步缓和民族矛盾，并取得秦体系内更大自治|“商业繁荣换归属/自治”是可用的前史先例，不等同文化被动消灭|
|slide 22 p24–30|1699东方条约试图保丝路贸易；秦俄关系有破裂和再次结盟；1729联军围伊斯坦布尔未克，1730巴格达条约终结两百年西进|俄国可敌可友，有非吞并的贸易/势力范围玩法依据|
|slide 28 p19；slide 29 p4、10|官方未来线1870华秦因共同受吴朝殖民贸易封锁而和解；1896条约要求华朝归还鄯州给西秦|复仇统一不能被写成唯一正史未来，应保留华秦和解与边疆恢复的可玩出口|

### 不应强行裁定的异文

- 革命起点：slide 3 p11、slide 15 p8 写1805；slide 10 p5与现行MOD土改背景写1810。方案介绍可写“大革命以来”，不用未经作者裁定的单日做新触发器。
- 秦败亡：PPT slide13 的兰州会战及苏宏西进放在1821；MAIN/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:10 写1822敦煌会战、张百里。两者应并列记录，不把人物与年份强行拼成一场。
- 地名核对：首都 STATE_ILI 仍名“伊犁”，来自 MAIN/localization/simp_chinese/nesnd_editor_l_simp_chinese.yml:11；MAIN/common/country_definitions/ce_countries.txt:34仍以它为首都。最近改为“西益”的是非首都 STATE_JETISY，来自 MAIN/localization/simp_chinese/replace/map/ce_states_l_simp_chinese.yml:731。原版把 STATE_JETISY 也译成伊犁，不能因此把两个不同state_region混为一处。本报告初稿曾错误地把西益归给首都，现已纠正。

### 必须标为本轮 gameplay_proposal 的内容

用户此次提出的持续归化、受征兵/经济衰退驱动的西域汉羌身份复归、文化统一数值、皇权/地方士人/军队三权竞争、可通往军事独裁或复归中华的各阶段日志，属于用户指定方向和新玩法设计。PPT没有给出这些数值算法，也没有确证1836以后每一次政变、具名政变首领或必然大统一。

## 3. 当前 QE1 已有实体与命名

- MAIN/common/country_definitions/ce_countries.txt:26–35：recognized、empire，主文化是 ce_laoqin、ce_xiyu、ce_xibei，capital=STATE_ILI。
- MAIN/common/cultures/CE_cultures.txt:1146–1154：老秦，heritage_han、language_mandarin、开蒙儒教；1230–1233：西北为heritage_han；1314–1319：西域汉羌已有明确融合史注释、heritage_uighur、language_xiyu_mandarin、大乘佛教、tradition_sinosphere。
- “主文化人口比例”已经包含西域汉羌；不是只计算老秦，更不是将文化统一理解为单一血统。文化数与heritage trait/group数也不等价；老秦和西北共享heritage_han，而西域汉羌本来就属于另一heritage。
- MAIN/common/history/countries/QE1 - Western Qin.txt:33–60：ig_armed_forces显示“武勋门阀”、ig_landowners显示“军士”，二者开局在政府；ig_intelligentsia名为ig_literati。地方士人不是ig_landowners的直接替代：军士本身就是旧军事土地精英。
- MAIN/localization/simp_chinese/replace/ce_country_flavor_l_simp_chinese.yml:2–12：原文解释军士是旧军国中剩下的精英；武勋门阀是大土地所有者、有功军人、旧贵族的联盟。
- 同国家历史:64–90：君主、专制、委任官僚、职业军队、地方警察、宗教学校，学校1级、警察2级。文件重复激活公民权/妇女权法律；计划须以实际最后生效法律为准，不据前一行认定开局状态，也不在本报告顺手修历史。
- MAIN/common/character_templates/zz_historical_leaders_ce_asia.txt:1259–1292：陈戊兴40岁，君主，老秦、武装力量、秦保王主义、残暴；陈矗国15岁，继承人、同文化同IG同意识形态、享乐主义。由common/history/characters/QE1 - Western Qin Empire.txt:3–9生成。
- 上述两人是当前MOD确有角色；本轮PPT匹配段落未给他们详细生平，不可自称PPT确证的政变经历。
- MAIN/common/ideologies/ce_leader_ideologies.txt:1–23已有秦保王主义：强赞君主与专制，但总统共和态度neutral；可支撑军政妥协分支，不能把neutral写成既定共和主张。
- MAIN/common/dynamic_country_names/ce_dynamic_country_names.txt:234以后及localization/simp_chinese/replace/ce_countries_l_simp_chinese.yml:71–80已有大秦共和邦/西秦/大秦/河中苏维埃共和国等名称；新政体应首先复用并核条件。
- 现有外部参与：events/nesnd_external_events.txt:3–10与common/scripted_triggers/nesnd_external_triggers.txt:26–28，将QE1同SIH外交目标相连；nesnd_crisis_effects.txt:169–171会通知QE1。CNE旧“对西秦战争”JE在ce_cne_land_draft.txt:81已possible=no、invalid=yes，不能据存在标题宣称已上线可玩西秦战争链。新系统应接现存外部策略，避免双重奖励/命令。

### 3.1 现行属国、波斯条约与直辖领土的区别

下列是当前有效历史脚本配置；本轮未读取新开局存档，不冒称实机外交状态。

|对象|当前配置与来源|方案影响|
|---|---|---|
|KAL 卡拉特|MAIN/common/history/diplomacy/ce_subject_relationships.txt:168–180在QE1 scope对KAL创建dominion；KAL在common/history/states/00_states.txt:105–108有俾路支斯坦领土|卡拉特是西秦明确配置的直接属国，不能把它人口当QE1直辖人口|
|MAK 莫克兰|MAIN/common/history/diplomacy/00_subject_relationships.txt:526–530在KAL scope对MAK创建vassal；MAK领土见states/00_states.txt:109–112、6257–6260|它是卡拉特的属国、属于西秦体系的下一级；宗主和顶级宗主判断须区分|
|KAZ 哈萨克|MAIN/common/history/diplomacy/ce_subject_relationships.txt:169–175仅在exists=c:KAZ时创建tributary；本轮搜索当前common/history/states全部有效.txt未找到给KAZ建立state的country=c:KAZ条目|这是带存在守卫的条件关系，不能无条件写成1836实际存活的第三个属国；未来释放/建国另行处理|
|PER 波斯|MAIN/common/country_definitions/ce_countries.txt:153–162的REPLACE:PER将其定义为unrecognized帝国，主文化ce_xiyu、persian，首都STATE_IRAKAJEMI；有独立国家历史、人物、州和军队|是另一个持有领土和人口的国家TAG；不是QE1的地理别称，也不是其直辖波斯地区|

波斯的关键陷阱是条约名称：MAIN/common/history/treaties/ce_historical_treaties.txt:64–102创建treaty_name_state_of_persia_protectorate，中文名在localization/simp_chinese/replace/ce_diplomatic_treaties_l_simp_chinese.yml:6为“大食封贡藩篱诏”。条约从1811.6.22生效，binding_period为30年。实际条款仅有防御条约（:74–76）、双向外国投资权（:78–88）、双向贸易特权（:90–100），并无让PER成为protectorate或其他subject的条款。GAME/common/treaty_articles/01_defensive_pact.txt:1–18、07_foreign_investment_rights.txt:1–20、25_trade_privilege.txt:1–20也分别定义对应防御/投资/贸易flags，不是属国关系。故“protectorate”键名、封贡叙事不能代替实际宗主检查。当前历史脚本表明PER是西秦具有防御与经济特权关系的独立国家，未配置为QE1属国。30年binding_period也不应未经验证便写成1841自动废约灭失。

PER实际拥有呼罗珊（MAIN/common/history/states/00_states.txt:6278–6287）、法尔斯（:6299–6306）、伊斯法罕（:6308–6315）、伊拉克阿杰米（:6329–6335）、塞姆南（:6337–6345）等州；西秦在锡斯坦有独立直辖片区（:6263–6266），在俾路支斯坦也有自有片区（:113–116）。PER州有西域汉羌homeland或QE1 claim，均不等于QE1持有该州。中期“维持波斯”宜先实现维持/重谈现有条约、协防、投资与扶持亲秦集团；升级属国、索地或吞并应作为会改变现存关系的新分支，不预先写成收紧一个已经存在的protectorate。

人口清点关联文件：WORK/reports/rules-poland-qin-20261102/qin-culture-inventory.json。按该报告当前脚本清点，QE1直辖36个state_region中人口39,713,582，35种文化；三主文化合计25,996,645，占65.460337977%，ce_xiyu仍为heritage_uighur。此口径是1836脚本初始数量，不是运行存档，也不包含整个PER、KAL或MAK。文化统一计算只应在目标国家实际领有的state内取数；条约伙伴/属国另设外交整合指标，不能把他们的文化悄然纳入国内统一度分母。

## 4. 完整原版参照链与可支持接口

### A. 定向文化转换：可以；自动追溯祖源：尚无证据

完整实例链：

1. GAME/common/journal_entries/06_iberia.txt:156–219：JE完成后，在c:IBE中按bureaucrats/academics筛选every_scope_pop，再change_pop_culture target=cu:iberian value=0.25；:244–251另有所有pop 1%转换。
2. GAME/common/diplomatic_actions/53_subjects_change_culture.txt:125–148：外交行为选宗主主文化，按人口数量排序目标国官僚pop，将其中5%转换。证明可以传culture scope作为目标，也可以按职业限定。
3. DOC/effects.log:646–649：change_pop_culture = { target = cu:spanish value = 0.33 }，scope必须pop；:4762–4766 every_scope_pop可从country/state/IG/culture遍历。
4. GAME/common/effect_localization/00_pop_effects_loc.txt:34–36接CHANGE_POP_CULTURE；GAME/localization/english/effects_l_english.yml:378解释“该pop的百分比改变文化”，不是改变整个国家culture字段。
5. 替代身份结局链：GAME/common/journal_entries/06_philippines_je.txt:312、364、453，分别触发philippines.11/.12；GAME/events/iberia_events/philippines_events.txt:732–754、824–846把filipino_mestizo转为filipino或filipino_hispanophone。**这是同一来源的两个候选去向，不是恢复原文化的实例。**

适配西秦：

- 繁荣时可以只在QE1领有的中亚州，筛选允许的文化、人口生活水平等条件，以小比例定向变为ce_xiyu。原生effect无需新建人口或删除人口。
- 复归同样可将ce_xiyu的一部分改成一个明确指定的现存文化；但是DOC文化target只暴露pop当前culture（event_targets.log:1790–1793）。没有查到previous_culture/original_culture/culture_history或变更来源回调。不要宣称可以精确找回几十年前每个个体的祖源。
- 推荐第一阶段采用“地方身份重新凝聚”：每州事先核定候选文化及权重，在征兵压力和衰退持续时小比例转换，名称和叙事承认是当代身份选择。可只让本系统产生的累积“可复归份额”形成上限，但账本是宏观近似。
- 若要求严格只回转已归化人口，则需要来源账本设计，并验证人口迁移、增长、职业转移、pop合并/拆分、州拆并、换主后的守恒；当前接口证据不够支持逐个pop永续血缘标记。不要先承诺完整精确追溯。
- 不推荐逐月创建数十个“某族归化汉羌”新文化来保来源：会污染文化计数/接受度/人物/迁移，反过来破坏用户要的文化统一玩法。
- 本轮没有进行最小引擎实验，尚未验证小比例转换的取整、pop合并、迁移与账本稳定性。

### B. 自然同化与指定汉羌转换必须分开

- GAME/common/defines/00_defines.txt:1419–1426：原版ALLOW_ASSIMILATION_IN_HOMELANDS=no，ASSIMILATION_RATE=0.002/月，最少1人；是自然同化资格与速度规则。
- GAME/common/laws/00_citizenship.txt:200–206、321–327等：接受等级控制自然同化资格/倍率；不能仅靠“文化被接受”做旧版本直觉判断。
- GAME/common/laws/01_education_system.txt:299–320：公立学校关联institution_schools，每级state_assimilation_mult=0.125等。
- GAME/common/modifier_type_definitions/02_modifier_types_rules.txt:89、97存在本土同化、无需存在目标文化的规则修正；有这些定义不等于本方案已经验证了所有目标选择规则。
- 提高自然同化速度，不能保证原生系统每次选择ce_xiyu；若用户要持续明确流向西域汉羌，应使用单独定向小比例脚本，并防止同时施加过大的自然倍率造成叠加。不得为此修改全球defines或删除地方homeland。

### C. 月度生活水平趋势和文化统一输入

- DOC/event_targets.log:1517–1520：average_sol接受country/state scope。
- 完整采样实例：GAME/common/journal_entries/00_negotiation_quests_je.txt:701–755，immediate把root.average_sol保存到IG变量starting_sol/current_sol，on_monthly_pulse重新采样current_sol，并以承诺值判断完成。
- 因此可保存QE1或各州的上月/过去季度SoL，先算差值，再更新基线。没有本轮查证的“过去三月SoL趋势”现成函数；滚动窗口、连续增长月数是自建变量。
- DOC/triggers.log:14307–14312 standard_of_living是pop scope；国家不能直接用它替代average_sol。
- DOC/triggers.log:9546–9568 culture_percent_country/state按给定文化取比例；:13887–13903 primary_cultures_percent_country/state读取所有主文化比例；:13567–13572 pop_has_primary_culture用于pop筛选。
- DOC/effects.log:4689–4693 every_scope_culture、triggers.log:3782–3787 any_scope_culture支持country/state；可统计本国实际有的文化，而非遍历所有世界文化。
- heritage与heritage group分别可由has_discrimination_trait、has_discrimination_trait_group判断（DOC/triggers.log:10277–10287）。没有已证实的一步“distinct heritage count”函数：固定枚举已核定trait/group存在性再累计，或另写明确去重逻辑。
- 推荐文化数只计达到最小人口份额的群体，避免几名移民就增加整档负担；主文化比例与可见文化统一数值分开。征服立即稀释主文化比例，可以给一次有限胜利信心，却不应永久抵消新人口治理成本。
- 全国SoL会因吞并贫困州、迁移而改变，不能把构成变化全部叙述为原居民骤然变穷。归化/复归主要用州级趋势，并对新取得州设置观测期；全国指标用来表达财政政治压力即可。

### D. 军队、征兵、制度与行政负担

|输入|本机接口与来源|限制|
|---|---|---|
|常备陆军规模|DOC/event_targets.log:888–893 army_size|营数，不是人员满编数，也不是军队实际忠诚|
|实际已征召规模|:902–907 army_size_including_raised_conscripts|与army_size的差可作当期已征召营的代理；应clamp>=0并测动员/复员时点|
|总潜在征召|:895–900 army_size_including_conscripts|文档描述与raised版本不够清楚；勿据此当作实际在役，优先explicit raised版本|
|动员|DOC/triggers.log:12104–12109 is_mobilized|military_formation scope；不能直接对country调用|
|行政盈余/开支/产出|DOC/triggers.log:8860–8870 bureaucracy、bureaucracy_usage；13924–13928 produced_bureaucracy|bureaucracy是可用余额，不能混作总行政实力|
|学校/警察等机构|DOC/triggers.log:11151–11156 institution_investment_level={institution=… value>=…}|国家scope，需要实际法律允许；没有机构不等于读取任意自造institution|
|法律|DOC/triggers.log:10451–10476 has_law/has_law_or_variant；effects.log:12–15 activate_law|强制切法与玩家正常立法是不同动作|

GAME/common/script_values/negotiation_values.txt:592–596已以bureaucracy_usage、produced_bureaucracy作算术；ip4_je_values.txt:537–553以实际军队存在与将领军衔份额计算政变实力。可沿用分母保护、min/max，不发明“军队掌控度”引擎值。

建议将领土、制度、文化多样性作为行政需求，把行政产出和盈余作为承载能力；制度升高既能加强整合，也要消耗真实官僚，不设无限免费制度红利。原生已经存在人口/机构行政负担，新增多样性扣分须明确为政治协调成本，避免对同一项扩张无解释地重复惩罚。

### E. 胜利、新疆土和军事失败

- GAME/common/on_actions/00_code_on_actions.txt:2099–2115 on_battle_won：root为胜方国家，enemy_country、battle、attacker/defender commander、state均有注释；还实际调用carlist_war_battle_score。:2125–2134给出败仗及空战斗不同回调。
- :6230–6264 on_wargoal_enforced：root=Country，target=被执行国，diplomatic_play、wargoal_impact可用；原版此处设置recently_won_war。但外交退让也可能执行战目标，故这个回调不天然等价“真正打赢战场战争”。
- :6988–7015 on_war_end：root=外交博弈，actor/target为发起/目标国；这里只表示战争结束，不能无条件给胜利。
- :7125–7134 on_state_incorporation/on_state_owner_change从state进入，新领土可在此登记，并逐月对照本国持有州重新计算。
- 战胜奖励应有指定战争/对手/战目标范围、冷却和总上限。同场多战目标不应重复按完整胜利加值；同一州在战线反复占领不应反复算“新领土”。战斗奖励宜小且短期，稳定收益来自占有、治理和生活恢复。
- 复归中华终局应看实际持有关键西北州/独立地位/政治制度与一次性结算标记，不能只看击败CNE一次。可先做“重返河西/关中”，后续统一与现有中国战争系统对接。

### F. 三权竞争与政变

完整原版竞争链：

1. GAME/common/journal_entries/01_french_monarchism.txt:15–28初始化三派变量、登记三个bar；:113–128每周重算输入。
2. GAME/common/scripted_effects/00_victoria_scripted_effects.txt:2116–2141初始化；:2144–2219从人物人气、IG clout、是否执政、实际已雇佣军事建筑和政府合法性计算进度。
3. GAME/common/scripted_progress_bars/00_victoria_progress_bars.txt:3–45按月累计、逐条desc显示贡献，含明确min/max。这比在事件描述手写每月百分比更适合本项目原生明细要求。

区别与映射：

- DOC/triggers.log:11039–11058，ig_approval是态度、ig_clout是政治影响力、ig_government_power_share是政府内相对实力；三者不能互换。
- DOC/triggers.log:12824–12829 loyalty只属character，不能用“军队loyalty”虚构国家/IG属性。本次未找到可以直接设置任意“全军忠诚”的原生effect。
- 皇权没有独立标准IG；建议独立“皇权”值，由君主制度、君主合法性、任官法、王朝事件、受支持IG计算。保王军人与皇室并非永远同阵营。
- “军队”权力来自武勋门阀clout、将领及军队规模、动员/胜败；“地方士人”来自知识分子、地方行政/学校制度和相关职业/实际支持。旧军士地主另作为联盟势力参与，避免硬把他们全部等同地方文人。
- 建议三权是实时相对权重（归一化前每项有上下限），不让三个无限增长bar都到100；另有一个累积“政变危机”bar。势力优势不等于忠诚，不满也不等于必然政变。

完整政变链：

- GAME/common/journal_entries/01_coup.txt:8–43先寻找有golpista标记的IG/将领并保存上下文；:71–85进度完成后只触发ip4_coup.2，show_as_tooltip中的victory effect只是展示。
- GAME/events/iberia_events/ip4_coup_events.txt:167、250、456、499有真正ip4_coup_victory_effect调用；不能把JE完成当作政变已经成功。
- GAME/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:378–385统一结算；:433–435可能更换统治者，:437–442给IG成功修正，:451–473设置执政党/IG，:488–491给国家modifier_government_recently_couped；后续law/special/technical分支各司其职。
- 原版helper依赖一整组标记与作用域，不能在QE1事件直接裸调ip4_coup_victory_effect。可研究完整接入或写独立前缀状态机，确保与已有原生政变不会双结算。
- 新危机需有预警、妥协/镇压/退让决策、将领死亡/流亡兜底、冷却、清理；角色身份来自当下存在对象，不能每次政变都复活陈戊兴或固定历史将领。

## 5. 建议的阶段与文件职责（尚未实施）

以下是可供主计划采用的设计建议，具体系数应等人口/经济清点后确定。

1. 开局：失去关中后的军府帝国。皇室要求保留东征大义；军士守住土地与地方权力；武勋反对再赌国运。玩家可用粮价/商路、复员减负、任官/税制、学校和文官行政恢复生活，也可扩大军警、以秩序维系中央。军管提供短期稳定和行动能力，但长期征召与财政压迫引发地方身份复归。
2. 中期：先维持/重谈与独立PER波斯的现有防御、投资及贸易条约，并经营卡拉特—莫克兰的真实属国链，再向波斯、印度、俄边疆恢复更大影响。胜利带来短期声望与军界议价力；直接吞并增加需治理人口、文化协调与军费。把波斯纳为属国或索取其领土是新关系分支，必须与维护旧条约分开。贸易条约、属国/军府自治与整合可以作为不同成本的路线，不把所有地区都锁为必须吞并。繁荣归化与文化权利保护均可提高忠诚，但只有定向文化转换改变人口文化构成。
3. 长期：恢复经济、军制和制度承载后，才能使新一轮东征成为可承担的国家战略。分“河西归来—关中旧都—中华竞争”逐层目标；皇权复兴、军政国家、地方士人宪制各有统一后的制度后果。继续保留与CNE和解、经营中亚的终局，不强迫玩家为了清日志征服全中国。

建议新文件（仅建议，无创建）：

|文件|职责|
|---|---|
|common/journal_entries/nesnd_qe1.txt|主日志、开局复振、西向经营、重返关中、政变危机入口与生命周期|
|common/script_values/nesnd_qe1.txt|统一度输入、行政承载、三权相对权重、趋势和转换比例；明确分母/上下限|
|common/scripted_triggers/nesnd_qe1.txt|国家/州资格、趋势持续条件、战争识别、政体/角色有效性|
|common/scripted_effects/nesnd_qe1.txt|幂等初始化、月度快照、转换/复归、胜败登记、终局和清理|
|common/scripted_progress_bars/nesnd_qe1.txt|统一度与政变风险的原生明细；实时权力份额不与累计危机混用|
|common/scripted_buttons/nesnd_qe1.txt|行政/复员/学校/军管等行动，真实预算与时限；所有预览scope安全|
|common/on_actions/nesnd_qe1.txt|只接必要胜败/领土变化回调，限制QE1与已登记战争|
|events/nesnd_qe1.txt|财政会商、地方身份、将领要求、政变结算、阶段叙事；所有future剧情标为游戏分支|
|common/static_modifiers/nesnd_qe1.txt|少量分档且有清理路径的暂时修正；避免永久重复叠加|
|localization/simp_chinese/replace/nesnd_qe1_l_simp_chinese.yml及英文对应|沿用既有军士/武勋/西域汉羌名词，风味与机制提示分开，UTF-8 BOM|

必要验收：同化/复归人口守恒和目标正确；主文化总占比算法；新增州观测期；季度SoL读档持久；无战争/复员时减负；一战多目标只结算一次；非军事外交退让区别；三权分母为零与极值；君主/政变人物死亡流亡；原生政变并行不双结算；QE1亡国/重建清理；现有对SIH外部参与不会被抢写；本土与自然同化叠加；所有按钮预览及本地化scope。完成这些之前不得写“游戏内已验证”。
