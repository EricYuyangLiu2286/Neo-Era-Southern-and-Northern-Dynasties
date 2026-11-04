# Batch A2 安全交接

状态：**STOPPED**。2026-11-04。执行者：`/root/unity_native_inventory`。

暂停依据：root收到用户新的模型分工硬性要求，要求在安全编辑边界停止A2、保存交接，不启动测试，由root按显式模型配置重新分派。当前agent继承父级配置；当前工具没有公开可核实的实际模型名／reasoning effort，不能将预期配置冒报为已使用配置。

## 实际完成与文件状态

**A2 gameplay/localization edits：0。** root发GO之后只补读原版接口、当前候选和作者文案样本，尚未创建实现生成器，尚未改任何C文件。没有A2行为测试、Tiger、MCP或游戏运行。主MOD与游戏源码只读。没有重跑人口重配工具。A1先前STATIC_PASS及冻结接口仍保持；不要将A2获GO理解为A2已经落库。

本agent已写的A2文件均在WORK：

- `reports/canon-route-execution-20261104/batch-a2-native-americas-plan.md`：已获root原则GO的完整计划，75条文件来源索引。注意正文仍有GO前的精确人口70:30与静态国家名表达，实施前按下一节修订；没有通过修改游戏玩法来落实这些旧表述。
- `reports/canon-route-execution-20261104/batch-a2-source-manifest.json`：75项只读来源SHA。不是整个C的冻结证明，其他agent还可能编辑C其它范围。
- `reports/canon-route-execution-20261104/batch-a2-ppet-primary.json`：原PPTX slides18/19/22 XML文本提取；原件SHA `b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`。
- `reports/canon-route-execution-20261104/batch-a2-current-population-source-census.json`：只读当前人口源加总；没有写history/pops。
- `tools/capture_batch_a2_sources.py`：仅更新上述来源manifest和计划文末表格的只读源采集脚本；不是玩法实现工具或测试。
- 本交接 `batch-a2-handoff.md`。

没有A2 implementation/validation报告，没有READY_FOR_TEST。不要误用A1旧生成器重生成本轮候选。

## 已批准设计与两项最终修订

root批准计划§17全部具体政策：大国两州／小安第斯一州；NAH议会君主、TWT寡头宫廷；old_confucianism仅TWT国教，不转民众；40%失败迁徙无HUS时立即原地保留并结束；建战有限重试；全美洲补格陵兰；原住民HUS24普通法；custom on_enforced先迁徙再真实吞并。

**root明确覆盖旧计划两处：**

1. 满蒙外迁保留用户“70%-30%随机”原意：每个原HUS满蒙pop执行 `random_list`，70权重实际 `move_pop`到CNE、30到USA西部。不是每pop拆70%/30%，也不保证国家人口总数的70:30份额。仅一个有效目的地时全送该处；两个都缺席时明确终态、留原地，均已批准。报告和tooltip必须称统计概率，不称精确份额。
2. 国家名称优先实际 `Country.GetName`／flag，不能把CNE固定写“大汉共和邦”或“中华帝国”造成政体／时态错误。当前历史旁白可按明确年代称吴国、北明；当代实际国家使用有效scope。

继续约束：完成代码+中英文 → 停编辑并冻结所有权SHA／A1局部diff／原版窄diff／写作对照 → READY_FOR_TEST → root另派测试。编辑中不测同一系统；no_game；主MOD只读。无需虚构固定文件总数。

## 路径与所有权

- W=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`
- C=`W/exports/canon-route-execution-20261104-a`
- R=`W/reports/canon-route-execution-20261104`
- G=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`
- 引擎文档=`W/references/engine-docs-1.13.11-20261031`

完整所有权见计划§15。A1允许局部边界：`common/scripted_effects/nesnd_hus_registration.txt` **只改 `nesnd_hus_manchu_exodus` 内body**；`events/nesnd_hus_registration.txt`只迁徙／汗国通知接线；NKH文件里的A1 legal helper/classifier/default/native_successor/mutating顺序保留。不得改A1阶序法组、三法、十二类、接纳边界、68意识形态、公民法锁、global12月时钟与革命继承。B、C及其后续批次文件不碰。

## GO后新补读到的精确原版事实

以下是源码阅读，没有执行任何验证：

1. `effects.log:817 create_building`：如果州已有同类建筑，结果等级是 **max(scripted level, existing level)**，不是增加scripted level。现金储备亦取max。用该接口补目标等级时无需误写“已有等级+目标等级”；全国总上限仍须在脚本里计算／分配，不可每州都建全国目标。
2. `effects.log:959 create_military_formation`：country scope；字段 `type=army/fleet`、`hq_region`、重复 `combat_unit={type=unit_type:… service_type=regular state_region=s:… count=…}`。不能自行假设有 `create_combat_unit` effect。`effects.log:37330 transfer_to_formation`：character→military_formation；`unassign_from_formation`同为character effect。
3. `event_targets.log:888 army_size`：country实际正规营数，排除当前征召军；不要为了军力预算另造num_battalions国家接口（该名字在文档中是commander麾下营数）。`triggers.log:11253 is_army`可筛formation。
4. `script_values.md:38–40`：`round=yes`取最近整数，`floor=yes`向下；不是`round=down`。脚本值支持list迭代和正常scope切换。
5. 军事科技真实前置：standing_army无前置；mandatory_service→standing_army；gunsmithing→standing_army；military_drill→standing_army；artillery→gunsmithing；line_infantry→mandatory_service+military_drill。全部era1。`combat_unit_type_line_infantry`解锁line_infantry，cannon_artillery解锁artillery。基础工厂的生产科技仍需按实际DB补读后决定，不可泛给era2。
6. `create_character`文档字段是`ruler=yes`，原版template也用`ruler=yes`；当前草稿有`is_ruler=yes`，应按原生修正。`is_general=yes`有原版Huachaca template实际用法。模板来源 `common/character_templates/country_peu.txt:43`：Huachaca是Quechua、58岁、ruler+general、IQU人，不能偷为TWT新君主。
7. `triggers.log:2023 any_neighbouring_state`支持country/state/state_region/strategic_region，返回state；文档描述“states neighbouring a state region”。实现可按计划用state→neighbor原生接口，但后续split-state测试要明确它是否仅按region邻接，不能仅凭文本声称province接触已实机证实。不存在已发现的`any_neighbouring_province`接口。此项如导致实际新接口问题，应报root，不能自造trigger。
8. `common/character_interactions/00_character_interactions.txt:997 invite_exile`真实完整门槛：`empty_agitator_slots>=1`，devout/state_religion的宗教条件，character_acceptance≥acceptance_status_3，非closed_borders，`can_agitate=actor`；effect transfer_character + free_from_exile_effect。计划已经由旧event样例的status4改成此真实interaction的status3。

## 当前候选需要替换的具体入口

- `common/scripted_effects/nesnd_american_restoration.txt`仍是root草稿：mark_resolved过早、HUS缺席pending、NAH/TWT都总统共和、固定24营、先一州create、enemy_occupation>=0.8吞并、敌人不见算胜。没有任何A2修复已写入。
- `common/scripted_triggers/nesnd_american_restoration.txt`仍NPU遮SPU；`pair_at_war`泛匹配任何DP；corestate只人口100k且anynative。
- `common/scripted_progress_bars/nesnd_american_restoration.txt`已有月度progress项；草稿effect又自己加pressure并set_bar。实施前应选择明确权威值，避免原生bar月增和人工月增重复；计划允许变量/原生bar正常同步，不能在未证实的调用顺序上双算。一个可行方向是bar原生月增、monthly只读取bar作起兵判断，谈判在实际JE存在时改bar；这是尚未写入代码的实现选择。
- `common/scripted_effects/nesnd_native_khanate.txt`仍先一州create后转另外三州、固定40营和大量工厂、单个random目的州、战争泛flag。A1 `nesnd_native_primary_cultures_only`位于该文件98行，内容已冻结，完整保留。
- `common/scripted_triggers/nesnd_native_khanate.txt`当前has_play是war OR DP，不是精确案件；Americas不含Greenland。`common/journal_entries/nesnd_native_khanate.txt`仍只按没有战争判survival。
- `common/scripted_effects/nesnd_hus_registration.txt:355`当前外迁已经是random_list70/30 move_pop，**概率形式应保留**；修目的地缺失、收据／结果与通知即可。
- `events/nesnd_hus_registration.txt` .1汗国通知、.2迁徙通知；.10是A1时钟回调，**不改**。
- `events/native_resettlement.txt` .1–.7已经trigger=no、cancellation=yes、无effect选项。只冻结／后续验证；无证据不改。
- `common/scripted_buttons/turtle_island_buttons.txt`在G；C无对应三按钮覆盖。计划新增窄REPLACE，保留原body，仅NKH/native_successor在visible/possible/effect守卫。C已有JE窄覆盖。

## 写作来源与记录

已重新读 `nesnd-player-writing/SKILL.md`、`north-south-institutions.md`。作者样本只读备份：

- `W/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml`：flavorCNE.1.d、ce_cne_land_reform_reason、ce_cne_land_draft_failing_reason。政治集团的起源、利益和阻力承担因果，不能只剩“核册/批复”。
- 同备份 `ce_french_empire_journals_l_simp_chinese.yml`：je_ce_republican_movement_reason、原生进度条名和简短行动按钮。日志正文有历史与社会原因；按钮是具体行动，数值放效果提示。
- 当前完整A2计划含作者PPET定位与虚构人物边界；新王族名字、出生年必须注明本批补充，不能伪称作者原文。

尚未写任何A2中英文，也未形成writing-comparison。接续者需要把本轮所有有效文本逐条对照并记录；本交接不冒称文案已通过。

## 下一步

等待root显式重新分派。新实现者先读当前计划、此交接和项目技能，然后按上述两项GO修订更新计划；在WORK独立备份本批原文件并保存A1冻结源片段，完成全部代码/人物/双语/窄替换/旧档闭包。不要运行测试直到完整编辑停止和SHA冻结。对未知原生接口或批准范围外语义变更及时报root。

本agent停止后不继续A2编辑或测试。
