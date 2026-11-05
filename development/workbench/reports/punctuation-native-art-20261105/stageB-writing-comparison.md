# StageB 玩家文本对读与冻结交付

作者配置：父任务明确委派 `gpt-6-astra / high`。按 NESND 与玩家写作技能读取全部冻结文本契约、区域触发器/数值/效果/JE/按钮/事件/消息/进度条，以及共享准备、建国、开战、结算和避难调用。先保存初稿，再逐项返工和写入。没有修改脚本。

## 范围和来源

清单111项中，12项是变量/枚举/对象名称，并非玩家文本：created_polity、creation_mode、kind、partner、peace_region、peace_seed、profile、request_cooldown、request_epoch、request_pending、request_result、request_target。主代理批准排除，不为其建立本地化。

实际新增99对：区域主题96对，原战争JE语义叶3对。主代理又明确授权改写10对共享战争/目标展示键，避免原住民地区误用王朝名称。总计109对、218条语言/键，写入四个本地化文件。两份新主题文件为 `nesnd_regional_native_restoration_l_*.yml`。两份既有 `nesnd_native_americas_l_*.yml` 各只增3键、改10键。

原始作者样本沿用已逐字核实的 f18b6c4 `localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml`，SHA256 `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`。原文与行号保存在 `stageA-author-samples.json`。第118行通过政治参与和实际社会群体组织叙事，第179行区分结盟者的不同诉求，第194行区分阶段结束与政治矛盾仍存，第136行直接写必要条件与数值。本轮借鉴这些游戏句法，不移植南明的人名、宫廷制度或王朝立场。

当前原住民主题文字仅作术语和UI连贯性参照，不冒称作者原始文案。真实身份由脚本的 Aimara/AYM、Amazonian/AMZ、Muisca/MUI、Mayan/MAY 及现有 MKT 对应决定。共享文本没有虚构原住民王朝、君主或适用于所有地区的印卡传统。

## 初稿返工与逐条结论

初稿保存在 `stageB-player-text-draft-v1.json`，最终对读稿为 `stageB-player-text-draft.json`。后者为每个有效键记录类别、逐条结论和依据，并保留七项返工的原文与改稿。

|类别|初稿或原稿问题|最终决定|
|---|---|---|
|区域JE正文|“共和国的疆界”假设所有可用宿主都是共和国，实际trigger没有政体限制|改写为原住民社群与中央政府对土地和地方政治的争执。没有额外指定政体|
|压力状态英文|让 territory 本身“开始筹备”，主语不当|改为地方组织在具备可用地区时筹备。100/12个月来自实际effect|
|独立条件叶|“建国民族”表达生硬，且必须清楚分母|改为选定州、主体原住民文化35%、州人口100k、半数上限和保留150k/另一人口州。动态state有exists保护|
|开战事件及通知|首稿只写主权对峙，未突出实际war=yes开战阶段|逐行核对共同dispatch的create_diplomatic_play war=yes与匹配play/目标后通知，最终明确开战。筹备和建国通知保持各自阶段，不提前写成战争|
|地方谈判、协议、镇压|三种行为不能互相冒充|协议只有对方接受才给下方修正/关系25/压力−25/取消筹备。国内谈判−15。镇压−20及5%激进化，期限与IG修正留原生预览|
|终止事件与通知|同一终止事件覆盖未发起、失去对手和无吞并结束|只写未完成吞并的结果。分别用简短通知呈现各原因，不把它们统写成军事败北|
|独立结果事件|created_polity对象没有事件trigger存在守卫|不引用该变量，只写确实独立的选定地区。无土地/国号替换误述|
|共享战争/目标|旧“王朝复兴之战”“复统王朝与共和国”不适用于区域3|按主代理授权改成“原住民复国战争”/“War of Indigenous Restoration”和“统一国家”/“Unify the Country”。目标描述保留吞并及有条件的外逃/流亡，取消“先处理”等实现口吻|
|通知tooltip|不应每条重复另写长段落|十条tooltip全部引用自身name/desc；消息正文各只一段简短事实|

所有109对文本自身编辑审查通过，最终仍待主代理逐条审定。没有新增永久技能规则：本轮返工均已由现有“政体需来源、阶段需实际effect、动态对象需守卫”规则覆盖。

## 动态引用与实际调用

- 通知只用 `SCOPE.sCountry('nesnd_restoration_notice_actor').GetName`。共享publish先保存actor，再向外交相关国家post_notification。建国notice的actor是原宿主，因此文字为“原属该国的原住民地区另立政府”，没有把接收通知的国家当成起兵国。
- 接受协议事件7只读受 `nesnd_regional_native_reply_live` 保护的 `regional_native_sender`。结果事件9采用静态文本，不依赖周更超时路径没有保存的recipient。
- 事件3和6属于country_event，使用 ROOT.GetCountry.GetName。事件3发生在吞并实际完成之后，事件6由真实失败后的迁徙路径通知HUS。
- 独立条件叶使用 `ROOT.GetCountry.MakeScope.Var('nesnd_regional_native_peace_seed').GetState.GetName`。实际can_release的trigger_if先检查该变量存在。绑定参照当前争议州状态原用法，以及本机runtime data types中的Country.MakeScope和State.GetName。
- 进度条desc严格沿用已用模式 `JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)`，没有Country.MakeScope的条上下文混用，也没有second_desc长段落。
- 战争目标草稿名保留 `[WAR_GOAL_DRAFT.GetTarget.GetName]`。既有DP tooltip无需改键，其name/desc别名自动解析到新文字。

## 读回与冻结

独立修改前备份：`WORK/backups/pre-change-stageB-player-text-20261105T034028Z/mod`。新文件写前不存在，记录在manifest。四文件冻结：`WORK/reports/punctuation-native-art-20261105/stageB-player-text-freeze`。这只是文本子集，不能当完整MOD。

实际逐键前后、SHA、范围在 `stageB-player-text-applied.json`，原始差异在 `stageB-player-text-actual.diff`。`stageB-writing-final-readback.json` 确认218条内容精确对应审核稿，语言/键组合唯一，所有别名有目标，四文件UTF-8 BOM且当前SHA匹配冻结，未出现双重转义换行。十二个内部键两语均未补入。

两份既有文件中，除13个目标键外的所有行保持一致，因此墨西哥/安第斯原JE、事件及大平原文字未被替换。写入期间16个StageB源码文件SHA均未变。对release按钮request_open原始旗标的包裹建议已交主代理和脚本实现者，不由本次文本写入越界处理。

这是写作和源码绑定检查，不是游戏验证。脚本独立审查、Tiger与整合后的运行证据由根代理负责。

## 最后两条提示

地区镇压条件使用反抗压力至少50的专用提示。接受协议的提示引用已受保护的提议国，说明反抗压力降低25并停止起兵筹备。最终增加101对键，改写10对既有键，共222条。两个地区文件分别追加两行，完整清单和最终差异继续使用本报告所列路径。
