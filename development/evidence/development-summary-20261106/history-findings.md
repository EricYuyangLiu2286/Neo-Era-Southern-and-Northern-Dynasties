# 开发历史与未完成项核查

2026-11-06。只读调查主MOD、任务31–44、既有报告及Git main；仅写本报告，未修改游戏文件，未启动游戏。执行代理 `/root/astra_history_synthesis`，父代理显式委派 `gpt-6-astra / high`。实际工具没有 `gpt-6.1-astra`，未冒称该版本。

MOD为 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`；WORK为 `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。Git命令在 `WORK/projects/nesnd-repository` 执行。此次 `catalog.py status` 返回1.15.0 / build26453692 / CURRENT / changed_count=0。Git main顶点为 `67c876e`，`git status --short`为空。此项只核Git工作副本，不声称全部主MOD文件与Git字节相同。

## 可用于项目总结的开发阶段

|阶段|实际交付|可追溯的main提交/任务|验证边界|
|---|---|---|---|
|原版保全与工程基线，10月30日快照至11月1日|保存作者原始版、分离主MOD与源码仓库；本地任务、候选/备份/原版链条和地图工具流程建立；部分女性发型、地图和日本恢复已有局部实测|`f18b6c4`原始快照、`45f475e`主MOD起点、`460f1e1`局部实测记录；任务01–10|不能将早期个别场景通过升级为全部包通过。编辑器舍入修复`49fed23`是工具成果，非完整编辑器交付。|
|基础故障收口及中国政治链，11月1–2日|按钮预览引用保护；南朝危机与战争结算；CNE地权改革子日志、信心与共和起义；波兰、西秦和波斯生命周期及完整性修复|`67f1826`、`629281f`、`8623191`、`47adfc0`、`bbe7ebe`、`044de73`、`7d39018`、`4014560`；任务09–18|多数交付为STATIC_PASS。用户后续反馈曾证明“子日志已写入”不等于实际入口可用。|
|日本、印度与跨国关系，11月2–3日|日本25个发展日志、原生共同市场；印度阶段发展、土邦/起义和两司；两司后置门槛与可失败回归；观察者错误归因、CNE拖延压力|`c1463da`、`a062441`、`adfc317`、`a70eb12`、`f6eb822`；任务21、25–28|两司的旧484项多为结构检查；任务26另补真实AST边界及变异反例，仍非引擎完整模拟。|
|区域路线和架空制度扩展，11月4日|波斯可消费施政/筹边资源、USM战后整合/西部置省；七国建设短链；HUS社会阶序、文化政策、原住民复国/汗国；意大利/HUS/USM十条建设分支、27选择、18名虚构人物；印度/南洋自主和市场路线|`b374be5`任务32、`b94582e`任务33、`f05f063`任务34，`0bd4bdb`交接|任务34明确187游戏文件＋2任务文件，无删除；当时1.13.11且ENGINE_NOT_RUN。不能再把意大利/HUS/USM和小国扩展概括为“仅计划”。|
|从长局证据修生命周期，11月4–5日|本地化清理、运行时scope及UI修复；原住民镇压/战争；1891终档审计后开放日本三家分封；战后人口流散、文化转换州预告|`90f15ac`、`9cdfd02`、`3ac2f76`、`a90ffac`；任务35–39|任务38依据改前1891档定位，改后离线；任务39有两次真实观察者开局和日本预告存档，但短期日志不能证明后期全部战争和迁徙。|
|1.15迁移及新版本首局收口，11月5–6日|204条JE定义、345结局、66进度条迁移；地图新地块/接口兼容；复国战争、援助合同；首局原生日志驱动职业/文化/战争压力修复；俄国边疆与架空西秦对齐；靖难余部、地区自治、东青行母子链、法国旧主线结局修复|`30eed2a`任务40、`278616a`任务41、`2fcfaf0`任务42|任务42记载278616a观察者存于1837-06-18；后续修复游戏外核验。1.13旧证据不能直接认证1.15。|
|玩家可操作性与发布内容，11月6日|四份中文稿逐条改写；224个实际挂载缺图标修正补图；独立JE可见结局；HUS道路、国内争议与编户操作；地区指标说明和真正分组变化门槛；埃及冷却状态|`02b66fe`任务43、`67c876e`任务44|两批均STATIC_PASS，尚无修后UI实际布局、原生结局刷新与连续时序引擎验收。|

任务详文入口：[执行索引](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/map.md>)。以上提交由本地main `git log --first-parent`核查。阶段按交付内容归并，非声称每次都完整结束后才有下一阶段。

## 旧“未实施”标记逐项裁定

1. **法国完整新增后继路线仍待实施，但法国既有帝国主线确已修复。** 任务29计划中的“宫廷与外省”、巴黎/外省资源配置、共和国繁荣与分配及条件性右转，拟使用 `nesnd_france_development` 文件组；当前 `common/events` 文件清单没有该组。当前任务42/提交`2fcfaf0`实际修改的是既有 `ce_french_empire.txt`及其按钮、效果、条和新增`nesnd_french_empire.txt` trigger，内容为登场、政体退出、王朝支持、国号和失去全部整合州的混乱。不要因这些修复声称新后继路线完成，也不要声称“法国尚未实施任何玩法”。[计划](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/france-politics-plan-20261103/france-development-plan.md>)，[任务42](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/42-campaign-followup.md>)。
2. **法国古吉拉特、包罗达、讷瓦讷格尔直辖及当地舰队仍待实施。** 当前主MOD `common/history/states/00_states.txt:4254`的古吉拉特依旧有USM、BER、NAW等国家state，未变为指定法国直辖安排。当前军事编队目录未检出GUJARAT驻地。它是新开局历史调整，不是引擎未测而已。[任务31](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/31-continuity-journal-rework.md>)，[总账61](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/61-continuity-and-journal-rework-20261104.md>)。
3. **日本新政的额外实质干预选择仍待实施；日本分封改造已实施。** 当前 `common/scripted_buttons/nesnd_jp_politics.txt:8/34/60`的三条新政资助仍共同使用相同费用、六个月`nesnd_jp_reform_effort`和冷却，未实现任务31提出的学务/旧臣协商/君主推动等不同代价与政治风险。任务38的三家政治提案、军事回应和首府宣称属于另一已交付闭包，不能拿它抵销新政选择欠账。[任务38](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/38-save-audit-1891.md>)。
4. **意大利、HUS、USM及小国路线不再是纯计划。** 任务34明确落库，之后任务36、42、44继续修实际UI、出资资格与生命周期。旧总账中“这些路线待实现”须限为被新交付覆盖前的历史。不可反向推断所有早期提案的每个细节都完成；具体遗漏仍需以需求逐项对照。
5. **编辑器仍有较大旧欠账，不能笼统写未做。** 已有真实建筑拆分舍入修复和当前地图分配检查；通用编辑、完整UI及更多资产拆分未整体认证。任务08/10与原规格是下一次细化的入口。本调查未运行或逐功能审查编辑器，不能给出全部未实现功能清单。

## 已实现但尚待当前版本引擎证据

- 任务43–44的道路子日志自动出现、国内争议正常退出、HUS编户通知和本地化布局、图标实际绘制、War提示不再刷日志、埃及期满重新出现。
- 任务42的首轮靖难与PHI结算、流散目的州失效后重选、东青行母子JE实际刷新；法国新失地出口也仅有外部反例。
- 1.15的复国战争结束回调、长期移民人口收支、各国自然AI路线/经济难度和存读档持续性不能由旧版短局或有限AST模型认证。
- 日本1891旧档的无分封原因已定位并修订，但新AI提案/实际开战频率未证。原住民汗国未出现也有旧档事实，不能据此保证新版必然出现；条件性历史事件不应强保触发。

这不是要求立即启动游戏。当前任务没有启动许可，后续须用户当次明确要求。也不要求重复已经匹配版本与源码闭包的通过场景。

## 有证据的主导工作弱点，供主代理自评

这些是交付与组织记录中的可观察问题，不是对主代理内部感受或固有能力的猜测。

- **通过数曾代替验收覆盖。** 任务25的484项中有大量关键字存在检查，不能证明比较方向、分支顺序或开局可达；任务26明确纠正，补原错误红绿、真实AST与变异反例。建议自评为“我曾过早把结构性检查当成玩法可靠性的依据”，不要把后来所有外部测试一概贬为无用。[任务26报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/commission-boundaries-20261103/release-notes.md>)。
- **对玩家界面和实际操作链的理解滞后于代码交付。** 任务36的Country上下文、second_desc重叠，任务43的道路JE缺失/重复add，任务44的代表州误指整组和五条JE成功/失效同时成立，都在“已有代码”后才通过用户反馈和独立反例收口。问题不止文案不好，而是缺少从玩家看见条件到点击、等待、成功退出的完整核对。[任务36](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/36-runtime-ui-followup.md>)，[HUS诊断](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/prose-icons-20261106/hus-diagnosis.md>)。
- **代理报告和最终发布对象曾失配。** 任务43最后四条文字纠正曾停在稿本，未进main；独立复查才补应用。任务44 Luna报告引用旧11按钮版本，须以before及当前源码纠正。应承认最终主审有责任核具体文件字节和引用版本，不能只接收子代理PASS。[任务43](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/43-prose-icons-outcomes.md>)，[任务44](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/issues/44-hus-player-flow.md>)。
- **检查器本身也曾接受错误假设。** 图标检查曾让坏MOD资源回退有效GAME资源、误判负IG图标方向，并要求修复后的主目录仍保留旧缺项。后来改为MOD优先、DDS实际头和不可变旧夹具。当前`astra-independent-final-review.md`明确未知谓词报错，不默认为零，2162项也不冒充2162种场景。这些是纠偏成果，不应删除失败教训。[图标实现说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/prose-icons-20261106/icons/implementation-notes.md>)，[任务44独立复核](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/hus-player-flow-20261106/astra-independent-final-review.md>)。
- **交接累积方式使状态过期。** active-work仍以任务40为顶部入口；map保存多段“当前/最新”。任务36仍有Result待填写和已过期的法国/Japan待办表述。合理修正是一个明确的当前摘要和历史链接，逐项核实际代码后更新，不机械删掉旧证据或复制旧pending。
- **文本质量需要主审返工而非只过格式。** 任务43首稿同构人物续篇、过量结局分支、无依据的增长/政体断言被退回，45键由主审重写。最终程序格式通过不能替代作者语体和剧情合理性对读；但本批只重写四份中文，旧英文正文并非同步完成。

## 仍待核定的问题

法国新后继路线的巴黎比例难度、人口基建上限、迁出接口和奖励周期仍是未校准设计量；不能写成既有机制。任务08编辑器与更早原始范围账的全量完结状态本调查未逐功能核完。部分旧报告已在授权清理中删除，缺路径不等于从未执行，须从Git或保留交接判定。无调用栈引擎断言、外部HUD/RAHF旧档资源和本体问题必须分开归因，不能为了“全MOD零BUG”扩大无证修复。
