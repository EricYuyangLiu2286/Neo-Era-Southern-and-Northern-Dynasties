# 34 — 陈东阳警卫与一次重大刺杀案

2026-10-31。最终待合候选 `exports/chen-security-20261031-f`，直接父E、共同祖先 `exports/hus-pm-format-closure-20261031-a`。A–D为开发检查点，不合入；E是通过验证的行为基线，F仅共享案件准备effect供生产与QA共用。E与F均有独立SHA备份，F备份 `backups/candidate-chen-security-f-20261031T181840Z/mod`。主MOD、游戏本体、已冻结运行均未改。当前结论仅静态通过，真实引擎尚未验证。

## 现状问题与实施边界

旧 `flavorUSM.5` 在trigger中排除了protected，immediate内部的保护分支因而正常调用不可达；旧on_action对protected直接给保命事件，永久flag不随120月modifier到期。旧.5/.6无条件create郝廷疆，遇已有/离国/死亡对象可能重复创建。新方案同时修这三处，保留作者原“陈东阳遇刺”正文与死亡后政治效果，另写负伤/脱险分支。

不设不死、不改年龄、不阻断普通死亡。负伤使用原版 `wounded` trait，其本身的健康后果由引擎处理。新局/旧局不会生成另一位陈东阳。郝廷疆优先使用本国现存活角色；不存在且全局没有template且出生标记未出现才允许首次创建；已死或在外国的郝不会被复活/强拉回本国。自然死亡后的.6使用同一去重effect，只在世界中已无活陈时处理一次政治变化。

## 支出、期限与选择

|办法|首款|后续周支出|权威占用|期满/续办|案件死亡/负伤/脱险权重|
|---|---:|---:|---:|---|---|
|不设专卫|0|0|0|—|40/25/35|
|内阁警卫|£12,000|£500|40|6个月；第5月后可重新全额付费续6个月|15/25/60|
|留署理事|£24,000|£1,000|80|同上；撤去此前警卫修正，防重复叠加|10/20/70|
|有警卫并清查内应|另£18,000|沿用现有警卫周费|沿用|情报6个月，军队IG approval−2；警卫失效时情报防护一同停止|8/22/70|

费用初值仅待测：无风险事件时6个月约26周，常卫合计约£25,000，留署约£50,000；调查另£18,000。`country_expenses_add` 原版已有，真实预算与扣款须下次读档核对。不会为避免赤字偷偷免掉费用。购买用金储备与债务状态检查，不向无现金国家自动添加债务。

面板显示真实timed variable到期日：`TimeKeeper.GetCurrentDateWithDiff(GetVarTimeRemaining(ROOT.GetCountry.MakeScope,'nesnd_chen_guard_active'))`。本机data_types_script:80、原版interest_tier_types_l_simp_chinese:65提供同类调用。不是用月脉冲自行减一个假倒计时。事件选项在执行时再检查资金/人物/期限条件，避免开窗后人物死亡或钱已花掉仍扣费。

旧永久flag首次维护时删除。若案未发生且陈仍在本国，转换为6个月常卫；不收追溯首款，开始正常周费。若已经结案、离国、普通死亡或危机结束，移除警卫/情报及其费用。旧已排队的nesnd_crisis.11只做清理，不再赠送60个月保护。

## 案件机会与概率

保留主日志原月度随机事件比重：无事900、刺杀机会20，即每个**符合条件的月份**20/920≈2.174%。机会要求陈仍在本国、started标记有效、明吴日志在运作、未吴化/未结局、压力>24、该案从未发生。protected不再排除机会。

发生一次机会后先设置永久已结案标记，再按当时措施抽一次结果；所有结果总权重100。这里设计的是原剧情中的一次重大案件，不把它改成每月独立死亡判定。后续能自然死亡，但不会无限重开同案。

|持续符合机会条件的时长|遭遇本案概率|全程无专卫的案致死概率|全程常卫|全程留署|全程警卫+情报|
|---|---:|---:|---:|---:|---:|
|5年|73.25%|29.30%|10.99%|7.33%|5.86%|

这是对代码比重的解析核算，忽略自然死亡、和平结局、未续费与压力下降，不是实机多年存活率。完整1/3/5/10年在validation JSON。它使警卫有明显效果但不提供绝对免死；长年维持又需反复投入。

死亡：先保存真实陈对象，下一天原flavorUSM.5确认他仍活在本国后才执行kill、合法继任和原有+25压力。若这一日内自然死亡，flavorUSM.5不执行，.6处理正常死亡后政治变动，不重复加25。

负伤：真实对象加wounded，压力+10；脱险：压力+3。三种结果均结案，不刷多次忠诚/科研奖励；警卫开销清理。留署模式采用官署遇袭/投毒正文，普通模式采用航船正文，避免人已留署而叙述仍强称登船。旧作者死亡航船文本保留为未留署路线。

## 依赖与精确合并范围

新文件：`common/scripted_triggers/nesnd_chen_security.txt`、`common/scripted_effects/nesnd_chen_security.txt`、`common/static_modifiers/nesnd_chen_security.txt`、`common/on_actions/nesnd_chen_security.txt`、`events/nesnd_chen_security.txt`、CN/EN `zzzzzz_nesnd_chen_security_l_*.yml`。

原文件窄改：

- `nesnd_crisis_buttons.txt` 仅`nesnd_protect_chen_button`。A模块改同文件compact节点，需AST三方合，不能整文件覆盖。
- `ce_usm_the_last_days_of_ming.txt` 仅`random_events`的`20=flavorUSM.5`改为`20=nesnd_chen.2`。
- `nesnd_crisis_on_actions.txt` 仅删除旧protected直接保命的第一个if；外国干预逻辑原样。
- `flavorUSM_ce.txt` 仅flavorUSM.5/.6：前者变为真实案致死通知，后者使用去重接任，移除不存在人物的show_as_tooltip分支；其他事件AST原样。
- `nesnd_crisis_events.txt` 仅旧.11兼容处理。

当前controller/四立场模块不包含在本候选中；对照计划30交由root合并。人口、地图、建筑、军队、王室与服装资源SHA全部沿父不动。

## 已做验证与待做验证

`tools/validate_chen_security.py` 从实际候选读取随机权重、timed variables、触发器与生命周期护栏，不另写一份假游戏逻辑宣称通过。23项静态检查含16组合的可达性说明、保护分支可进入、同案不能重复、已死/离国/结局清理、Hao出生去重、无陈/王室create、父未变、独立备份SHA。Tiger无新增，父1弱error/1032warning/1tip→候选1弱error/1031warning/1tip（比较剔除行号位移）。证据 `chen-security-e-validation.json`、`.diff`、完整Tiger报告。

实际引擎仍需：购买两档/扣首款/每周支出；第5月续费/第6月到期/撤回；情报叠加与到期；首次悬停expiry函数；旧永久flag迁移；人物离国和自然死亡费用停止；三种案件结果及未配置Hao/已活Hao/已死Hao/外国Hao；排队死亡遇自然死亡的竞态；旧.11存档迁移；读档后同案不再出现。

分支夹具只能在真实机会出现前档设置有无guard/intel和受控随机分支，调用同一正式效果；不得直接写最终assassination_resolved+伪造死亡结果。概率验证需要多seed或原生日志采样，不能用这23项静态检查称概率已实测平衡。


## F：共享准备动作与最短引擎测试

最终用于合并的护陈候选改为 **`exports/chen-security-20261031-f`**（父E；共同祖先仍hus-pm-format-closure-A）。仅把案卷开始时的“保存真陈对象→结案标记→留署叙事快照”提为共享 `nesnd_chen_prepare_case`；生产随机事件和QA指定结果共用。把共享动作展开后，生产AST与E完全相同。费用、概率、文案、时限均不变。F备份 `candidate-chen-security-f-20261031T181840Z`，Tiger对E新增0。`evidence/chen-security-f-refactor.json`。

独立QA目录 `WORK/runtime/chen-qa-20261031-f` 只有事件探针与夹具，没有改活动/冻结QA。下一次运行把其中 `events/nesnd_chen_qa.txt`合入QA源，或独立挂载它。正常生产MOD不包含这些夹具。真实控制台命令 `event namespace.number` 已在本机前次运行验证；本文件新事件尚未实际调用。

|命令|做什么|证据边界|
|---|---|---|
|`event nesnd_chen_qa.1`|只读当前case_possible、在国、guard/intel/renewal/resolved、Hao存在|不改世界|
|`event nesnd_chen_qa.10`|在真实USM玩家且正常警卫链有效时，将压力设25|仅加速前置，不是自然危机样本|
|`event nesnd_chen_qa.20`|正常case_possible成立后，共享prepare+正式死亡effect|指定结果覆盖；不是随机命中证据|
|`event nesnd_chen_qa.21`|同上，正式负伤effect|同上|
|`event nesnd_chen_qa.22`|同上，正式脱险effect|同上|
|`event nesnd_chen_qa.30`|注入旧永久flag/旧120月修正，调用正式迁移|旧档迁移夹具，不是收费购买|
|`event nesnd_chen_qa.40`|调用正式随机机会事件nesnd_chen.2|机会被强制，结果权重仍由引擎抽；不能计入月机会频率|
|`event nesnd_chen_qa.50`|控制性非本案死亡，走真实death on_action/.6|验证清理，不证明自然寿命分布|
|`event nesnd_chen_qa.51`|控制性转移真实陈到无人类玩家的HNA|验证离国清理，不证明正常外交可转移|

最短顺序（每个分支从同一无案件存档恢复，不能连点三个结果）：

1. 真新局USM、JE自然出现后保存S0。实际点击“首辅警卫案”买常卫，保存G0：核£12k一次扣款、每周£500、权威−40、六个月到期日。保持压力<25，未注入前置，便不会在期限测试中被本案打断。
2. G0自然走满五个月，读取`.1`与续费按钮；保存G5。不续费继续到六个月后：真实timed variable及费用消失。重载G5再实际续费：首款再扣，新的6个月窗口、同key周费只一份。不要用改日期命令代替这段自然时间。
3. S0重载，买留署/清查，核首款£24k+£18k、周费£1k、军队approval−2。案卷两种expiry日期应正确显示；悬停后error增量为0。
4. 为每个结果重载G0→`.10`→`.1`确认case_possible YES→`.20`或`.21`或`.22`。死亡分支走至少两天，保存核陈死亡、Hao最多一位、+25压力只一次、警卫费用归零、flavorUSM.5原文和留署变体正确；另外两分支核wounded/+10或存活/+3，并再次调用同一QA结果应SKIP。
5. S0/G0各自重载，用`.30`验证旧flag只变6个月且没有追溯首款；用`.50`验证非案死亡、`.51`验证离国后下个月停费。读档重进重复读取不得再给政治进度或创造人物。
6. 用独立seed/基线+`.40`补有/无警卫真实random_list覆盖；正式月机会频率另自然运行统计。用24次强制机会取到分支不能宣称2.174%的月概率已经实测。

这些步骤复用已验证原生存档，不需要为每个选项冷启动。地图/历史/随机初始化没有再变化时允许同候选内重载分支；全部记录fixture类型与自然运行区分。

## G1与活动QA菜单（19:05 UTC，覆盖上述F交付状态）

正式合并版本为`exports/chen-security-20261031-g1`，继承F共享effect与全部玩法，只改CN/EN文案；同类作者原文逐类并排及叙事差异见`evidence/chen-security-prose-comparison.md`，G1去掉会误读陈为西秦旧王朝遗臣的措辞。G/G1未改概率、费用、人物生命周期。F仍是行为与QA接口基线，不能误当当前最终文本。

活动`runtime/qa-overlay`已在独立备份后加入新菜单。HUD按钮`QA: Chen branches`（1180,405）调用`event nesnd_chen_qa.100`，进可见菜单：取消、正式警卫案、明确标夹具的压力25/真实随机/死亡/负伤/脱险/旧flag/非案死亡/离国。结果按生产case trigger显示；新局未出现真实JE时会说明不可用，不自动伪造人物或日志。每个结果从同一案前档重载。调用键盘console在本机不可靠，因此入口沿用已经实际证实的`ExecuteConsoleCommand` HUD按钮，而菜单事件本身仍待本轮引擎验证。

源备份`backups/qa-chen-menu-pre-change-20261031T185938Z`；`evidence/chen-qa-hud-menu-source.json`记全SHA、唯一HUD插入及保留全部旧按钮的逆向断言。只改活动QA源，已冻结版本未动。正式G1不包含这些QA夹具。

## run192545真实May12 G0（本轮基线不能当未保护新局）

根从CNE玩家自然推进到May12后切USM，保存`大明联邦_1836_05_12_G0.v3`，SHA `0a5722f60cbe160c9c43c5c989a0e65be88fedf4096b7b3673cc83a5a2e3b3f0`。此前USM AI已买常卫（inner_guard，3月11日→9月7日）及情报（4月17日→10月14日）。这不是留署档，也不是首次购买前档。May12 guard剩118ticks、续费锁88、情报155；压力4、stance2拥吴，陈3148仍活，无案件resolved。

`evidence/chen-native-192545-May12-G0.json`记录修正ID1常卫/ID2情报及预算原生money 2868469.43212、money_trend.current 2848666.12885。authority总值未在country记录序列化，必须UI读回；不能把modifier的−40说成全国权威。六个月在此真实例子为180天。可从这个档验证现有保护清理/案件以及自然到期；首次扣款对照应另取未购档，或正式撤回后建立明确标注的人为子分支。`tools/audit_chen_guard_save.py --before <G0.json>`可比较同tick款项、变量、修正和真实角色ID。

## G2：真实选项预览刷错的修正

run192545 May12打开正式案卷而未选择，清理选项的效果预览反复尝试移除不存在的court_protection/residence_guard。根在19:54左右关闭案卷；UI错误累计48189后稳定。晚些时候可用error轮转只保留其中8342条相关错误，是文件保留下界，不能据此推断案卷仍开启。已归档`evidence/chen-preview-errors-20261031T200415Z`六个error文件及SHA；初始cold和assert另有更早快照。

独立`exports/chen-security-20261031-g2`父G1，将clear/buy/maintenance/investigate中13处remove_modifier全部加同scope has_modifier守卫。旧G1扫描检出13遗漏；实际G0修正集合精确复现两个缺失目标；16种修正存在组合的合法清理结果保持，去guard后的AST与G1全等。Tiger新增0；最终备份`candidate-chen-preview-g2-final-20261031T195900Z`。另加准确的撤回/清查提前结束tooltip，不改费用、概率、时限、人物创建或自然死亡。还须新冻结版本中实际打开/悬停/选择并比较错误增量，静态通过不证明预览刷错已在引擎消失。

日期raw字符串仍保留为已知UI缺口：本机原生dump80640明确TimeKeeper.GetCurrentDateWithDiff返回CString，Date.GetString则需要Date；原版interest_tier_types也直接使用此CString。尚未找到并验证转换方法，不猜`.GetString`或数值格式符能修它。
