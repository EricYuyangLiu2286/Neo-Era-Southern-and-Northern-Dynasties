# 32 — 中文随机姓名、概念链接与分层测试

**当前状态18:37 UTC：姓名B已实际生成且仅马耀祖有UI实证；正常退出后，探针收得两个完整SKIP周期和一个完整PASS周期，本run加载指纹绑定成功。只认证USM日志初始化与压力范围两谓词。最新收集规则见末节；初始NOT_RUN描述为旧工具历史。**

2026-10-31。范围：只读溯源、独立姓名候选、只读引擎探针生成与日志收集器。没有修改主MOD、当前冻结运行或游戏本体；没有操作游戏窗口。引擎探针尚未实际挂载运行。

## A. “马 马”的来源

原生证据：`WORK/runtime/profiles/20261031T165620Z/save games/大明联邦_1836_02_03_startup_fixed.v3`。详情与SHA见 `evidence/chinese-given-names-b-static.json`。

|原生角色ID|国家/文化|实际字段|来源判断|
|---|---|---|---|
|3029|USM / ce_wuu|first_name="Ma"、last_name="Ma"、无template，政治家/利益集团领袖，籍贯南京|随机名池组合；不是作者指定角色模板|
|5489|SIH / ce_xibei|同上，无template，政治家，籍贯云南|同样随机组合|

主MOD `common/cultures/CE_cultures.txt` 把25词Han姓名片段用于14文化（部分混合文化仅用其中一段）。`Ma`、`Dong`、`Hu`同时在该片段和姓池出现；例如han段479/519行的Ma。原版 `GAME/common/cultures/00_cultures.txt:10096` han条目同样如此。原版中文 `localization/simp_chinese/names_l_simp_chinese.yml:2741` 将Ma译为“马”。14个现有片段与 `backups/pre-update-20261030T233944Z/mod` 完全相同，故不是本轮更新造成。

这不表示“马”或任何单字名在语言上非法。问题是这一小随机池几乎全为常见姓，反复与姓池组合，容易产生不合本MOD文风的双姓式姓名。修改是随机命名设计选择，不是修正引擎语法。截图中“马马已去世”又涉及any_scope_character展开方式；不能据那个提示推定马马是郑钦。现有USM提示候选已将整个条件包装为准确概述，姓名候选分别处理随机人口。

## B. 独立候选与新名表

采用 `exports/chinese-given-names-20261031-b`，父 `usm-journal-ui-20261031-a`。A版遗漏原文件BOM，已保留为失败检查点；B版已纠正，**不要合A**。B备份 `backups/candidate-chinese-given-names-20261031T175516Z`。

仅4文件：文化定义一个文件、两语随机名本地化、metadata。仅替换各池中完整继承的25词Han片段，池总数与混合文化其余词保留。普通姓、贵族姓、女性名、王室专用名、文化属性、全部历史角色模板不动。

|原池词|新显示名|原池词|新显示名|原池词|新显示名|
|---|---|---|---|---|---|
|Chen|承恩|Cheng|承志|Deng|怀瑾|
|Dong|敬修|Gao|明远|Hsia|世昌|
|Hu|廷瑞|Huang|文彬|Kong|文达|
|Kwong|文清|Li|维桢|Liang|锡龄|
|Liao|修齐|Liu|学礼|Luo|彦章|
|Ma|耀祖|Mao|允中|Pan|允升|
|Tan|志诚|Wang|志远|Xie|仲衡|
|Yang|子安|Yu|宗贤|Zhang|景和|
|Zhu|国钧|||||

映射只是保留池槽数/混合权重的实现手段，不是把每个已有“Ma”角色改为“耀祖”。使用独立`nesnd_given_*`键，不全局覆盖原版Ma，因此历史马姓和其他语言不会被改名。新表选常见的两字读书人/士绅取名结构，保留修身、家族、官学语汇，不声称来自统计语料。各地域专门姓名差异仍可后续扩充；不是把彝族或琉球整个名库改成汉名。

14池为ce_zhonghua、han、yi、yue、ce_liaodong、ce_laoqin、ce_xibei、ce_xiyu、ce_sichuan、ce_chu、ce_wuu、ce_xinan、ryukyuan、ce_yuannan。混合池剩余非Han段没有Ma；manchu原有单字Ma未改且其姓池没有Ma。其他文化的异常组合不在本次证据范围内。

验证：350个词替换后逆映射AST与父完全一致，模板SHA原样；新loc均BOM，Tiger新增0（继承1弱error/1042warning/1tip）。已有存档的名字已序列化，加载B不会自动重命名。实机待：新局随机角色、姓名显示/排列、旧作者模板不变。无需为纯随机名称宣称已做战争或人口模拟。

## C. 概念链接必须跟真实判定一致

`GAME/common/game_concepts/00_game_concepts.txt:409,417`，`GAME/localization/simp_chinese/concepts_l_simp_chinese.yml:813–820`。

|玩家意义|脚本/数据意义|文本写法|
|---|---|---|
|债务违约|`in_default = yes`|`[concept_default]`|
|宣告破产|破产动作|`[concept_bankruptcy]`或带自定义显示的`[Concept('concept_bankruptcy','宣告破产')]`|
|破产后的惩罚仍生效|`has_modifier = declared_bankruptcy`|“仍处于[concept_bankruptcy]后的恢复期”|
|国家财政每周亏损|income/expense或income trigger|赤字/周结余，不能当作已经债务违约或破产|

现有CNE改革、湖广军需、丹那沙林多数检查的是declared_bankruptcy修正；`nesnd_external_can_offer_money/arms`同时检查in_default和破产修正。不能只把所有“破产”替换成一个漂亮链接而保留模糊条件。原版 `alerts_l_simp_chinese.yml:6–8`、`interfaces_l_simp_chinese.yml:5598–5606`提供成熟范例。

## D. 可减少屏幕操作，但不能让Python冒充引擎

本机实际安装的 `WORK/tools/paradox-script-mcp/src/paradox_script_mcp/server.py` 只有初始化、文件/符号/引用/结构查询；它没有游戏进程控制或事件执行接口。已经使用的Tiger是静态检查器。VSCode集成可启动游戏、显示error.log，但不是Clausewitz解释器，也不能像Python一样在事件脚本打断点。[Tiger作者文档](https://github.com/amtep/tiger)明确说明存在误报及新版本适配延迟；[Paradox Modding Toolkit作者说明](https://github.com/JDeffner/paradox-modding-toolkit/wiki/Running-the-Game)明确区分启动与调试，并未为Vic3提供已证自动benchmark能力。本机官方[Modding开发日志](https://www.paradoxinteractive.com/games/victoria-3/news/victoria-3-dev-diary-60-modding)也要求实际运行并读error.log。

原生 `GAME/tools/scripted_tests/scripted_tests.md` 支持每天success/fail以及截止日skipped。但官方文档写XML进入binaries；现在仍没有已验证安全输出重定向，因此本次没有启用它。具体前次查证在 `evidence/native-engine-test-automation.md`。不照搬CK3的`-play`、`-skip`、`-benchmark`、`-nographics`到Vic3。

本次做成了更小且安全的替代：`WORK/tools/qa_batch_probe.py` 生成QA-only事件与on_action，在实际进入游戏后第1天、以后每月按真实国家scope检查已加载世界，写原生debug.log。两项首批断言：USM当前日志存在时其两变量是否已初始化、易代压力是否处于0–100。未有日志则SKIP；未载/未走时则NOT_RUN。所有脚本只读，不设置政策、法律、角色、财政或胜负变量，不瞬移日期。

- 源参考：`GAME/common/on_actions/00_code_on_actions.txt:13`真实after-lobby接口（无root，必须显式c:USM）；475行monthly country有country root。现MOD `common/on_actions/ce_code_on_actions.txt:30`同样追加独立子on_action。
- 最终overlay：`WORK/runtime/batch-probe-20261031-b`，两脚本文件+metadata+指纹manifest。不要合A（A缺BOM）。B静态Tiger新增0。
- 挂载：合入活动QA的`events/nesnd_batch_probe.txt`与`common/on_actions/nesnd_batch_probe.txt`两文件，保留原QA metadata/gui；或作为额外独立MOD挂到候选之后。不可编辑已经冻结的run。
- 每次候选合并后重新build一份overlay/manifest，candidate指纹必须对应真正启动内容；不是复用旧manifest证明新代码。
- 第一次仍需真正新游戏→选国→开始→解除暂停。此后月度断言与日志收集无需不断读屏。UI/选项布局、工具提示与地图可达性保留有针对性的人工/电脑操作验收。

```powershell
& 'D:/ProgramData/anaconda3/python.exe' 'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/qa_batch_probe.py' build --candidate '<已冻结候选绝对路径>' --out '<WORK下新的probe目录>'
& 'D:/ProgramData/anaconda3/python.exe' 'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/qa_batch_probe.py' collect --log '<本次profile/logs/debug.log>' --manifest '<本次probe/PROBE-MANIFEST.json>' --run '<本次reports/runtime/时间/run.json>' --out '<WORK下报告.json>'
```

占位符必须替换。collector核对run中的candidate SHA集合、挂载MOD里探针文件SHA和日志路径。只有完整PASS、指纹绑定全部成立才`engine_verified=true`。该字段也只证明列出的两谓词，**不证明整个事件链、经济或UI**。缺失日志标记、SKIP、半截块、失败块各自有状态；不会把未执行误判成功。

实际已完成：在当前真实run日志采集，因从未加载探针而正确返回NOT_RUN；5种合成collector测试覆盖无输出/SKIP/PASS/截断/FAIL，全部通过，但都强制保留engine_verified=false；证据`batch-probe-existing-run-no-markers.json`和`batch-probe-collector-selftest.json`。这些只证明Python收集器行为，探针本身仍待下一次实际加载。

## E. 事件链如何进一步批量化

先重构共享effects，再对**同一条正式effect**做独立场景调用，而不是复制选项逻辑到测试脚本；测试准备条件与生产结果分开。每分支建立基线存档/条件清单，安排原生延迟事件与月脉冲，记录期望前置、执行、真实后置和清理。可在QA-only脚本下推进受控分支，真实AI自然选择另跑固定seed样本。

当前两个只读断言是首个可运行模板，尚不是用户要求的完整战争自动化。下一步把新设计的明吴四立场、切国、人物存亡、地区归属/海军、正常/中断结算分别列为场景，再生成每项断言。玩家选项UI仍至少覆盖一次；直接调用shared effect不证明按钮可点。用console触发事件不证明自然trigger/AI权重；受控占领不证明战线会自然打赢；快进不等于修改日期。

每次闭环报告固定保存：静态预计、实际原生结果、差异、remain bugs、修复后回归，以及基线/候选/游戏版本/load/seed/SHA。有同版本复用存档可省冷启动；地图/history或随机初始化变化必须新局。仅改文字的候选不重新跑一年经济；引擎scope/地图/经济变更不能靠文字测试通过。


## 后续实际姓名生成验收（18:12 UTC）

root在run180905真实USM新局保存Jan1原生档。全世界213个随机角色使用nesnd_given_*，25个新键全部出现，Ma+Ma组合0。USM小市民领袖3029为Ma/nesnd_given_yaozu（应显示马耀祖），工会领袖3031为Wei/nesnd_given_jinghe（应显示魏景和）。21名USM作者模板的姓名与原pre-update逐条相同，冻结亚洲模板与USM人物history文件SHA与名字改动前父完全相同。证据`evidence/chinese-given-names-native-180905.json`。这里只认证真实生成、对象与保存，不替root声称已确认画面排列。

更新18:20 UTC：当前run180905探针已在真实first-day执行，debug.log仅BEGIN及第一条SKIP落盘，collector为INCOMPLETE。原“尚未挂载”描述只适用于生成时与旧run165620，不能作为当前状态。等待正常退出flush再收完整结果。全局JE及四立场实际证据见evidence/succession-controller-runtime-180905.md/json。

## 日志轮转反例与收集器修订（18:30 UTC）

run180905执行完整`help`后，debug.log按约512KiB轮转。先前只读debug.log出现“BEGIN/SKIP半截”，不能据此判断整个探针没运行。已先归档debug.3/.2/.1/debug.log+error.log至 `evidence/runtime-180905-preexit-logs-20261031T182904Z`，各文件SHA、大小和读取稳定性均保存；这是退出前快照，尚不替代正常退出归档。

`qa_batch_probe.py collect --log <日志目录或任一debug*.log>`现在按数字N降序读取debug.N.log，再读debug.log。BEGIN与END可跨文件，每个结果保存file+line。完整周期必须包含每个预期case恰一次；缺BEGIN、缺END、重复case或两个不完整周期凑齐结果都不算通过。只有同一个完整周期全部PASS才能OBSERVED_PASS；任意FAIL优先；无marker返回NOT_OBSERVED_IN_AVAILABLE_LOGS，**不推定整个run从未执行**。run/candidate/probe/路径SHA绑定仍保留。

8个Python合成测试覆盖跨三文件、证据全在旧轮转、缺marker、截断、BEGIN丢失、FAIL优先、跨周期假PASS、重复case；均按预期状态返回。仅测试解析器，不是游戏测试。当前真实轮转日志已经找回两个完整SKIP周期、指纹绑定成立，报告 `batch-probe-runtime-180905-rotations.json` 为SKIPPED_OR_PARTIAL；仍无PASS，不夸大为变量/范围已认证。根正常退出后需再收完整落盘数据。

给技能的精确增补建议：

1. 启动/退出和执行大批量help/script_docs前后，归档全部debug/error轮转家族，不只live文件。每个文件独立SHA与行号，不把不同run同名日志混合。
2. 看不到marker意味着“当前可用文件未观察到”，先查轮转与缓冲；只有真实完整BEGIN→全部case→END、且绑定本run加载指纹，才登记相应PASS。
3. 自动化报告必须区分NOT_OBSERVED、SKIP、INCOMPLETE、FAIL和PASS；“无错误/无结果”不能当通过。
4. 本机真实`help scripted_tests`现已回显`before/none/after`只控制失败存档。没有由此获得报告目录重定向；继续不执行会写binaries的官方测试。完整help已证`testevent [event name] [<country_tag/province_id>]`、`escalate [<amount>]`、`conquerall [country tag]`及`add_war_support [country_TAG] [amount]`的名字/签名；名字被列出不等于已经实际执行或证明其所有语义。


正常退出最终复核：`evidence/batch-probe-runtime-180905-final.json`为OBSERVED_PASS，engine_verified=true，限定usm_init、usm_pressure_range两项；debug.log335–338完整周期，归档SHA/加载fingerprint匹配。由此已实际证明“入局一次后，原生月脉冲自动检查、Python无需读屏收集结果”的可用流程。它仍不等于无人值守启动选国、全部自动事件链或经济模拟器。

## 稳定自动存档采集器（19:05 UTC）

`tools/capture_autosaves.py`只读指定隔离profile的`save games/autosave*.v3`。两次SHA及四次stat在稳定间隔一致后，核SAV0100、原生game_date、必需顶层数据库、完整括号/字符串与末数据库，复制到独立证据目录。按profile+内容SHA去重；目标文件exclusive-create，不覆盖旧证据。一次扫描或最多3600秒有界watch，不启动/暂停游戏、不修改存档或用户配置。原生每月自动存档设置由root隔离profile另做实际验证。

`tools/test_capture_autosaves.py`使用真实旧1836.7.1原生存档的**副本**测试初次采集、再次去重、截断拒收、写入中跳过、字符串截断、原件SHA保持等11项。`evidence/autosave-capture-local-tests.json`记录这只是采集器本地测试，所有记录`engine_verified=false`。结构完整并不意味着引擎能读档、事件正确或经济平衡。真正游戏运行得到的新文件也只标runtime_capture，由对应场景断言另外判定结果。

用法：`python tools/capture_autosaves.py --profile "<WORK/runtime/profiles/本轮>" --out "<WORK/plans/two-empires/evidence/本轮-autosaves>" --watch-seconds 300`。源限定为WORK隔离profile；输出限定WORK证据/reports/qa-fixtures具名子目录；失效或轮转读锁记skip，不强制解锁。未证明原生安全暂停接口前，固定日期仍用已验证的游戏暂停UI。

后续真实验证：run192545隔离设置页已显示每月，CNE玩家自然Jan1→May12期间，collector实际保存Feb1/Mar1/Apr1/May1四份SAV及内部日期/SHA，见`evidence/autosaves-192545-cne-player/index.json`。因此“原生定期保存→稳定文件采集→离线读真实gamestate”已在这轮工作，不需要每个检查点手动另存。原生存档审计与日志仍发现未解决断言和PHI减贡资格阻断，不能从采集成功推成游戏验证完成。
