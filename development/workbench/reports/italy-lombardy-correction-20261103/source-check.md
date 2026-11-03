# 伦巴第共和国：作者纠正与源码核对

日期：2026-11-03。范围：精简只读核查；仅新增本备忘，未改原方案、MOD、技能或游戏文件，未启动游戏、未做现实历史外网研究。按 NESND 工程适配使用 research；`catalog.py status` 返回 **1.13.11 / build 24799966，CURRENT，changed_count=0**。以下源码结论不等于本轮游戏内验证。

## 作者确认（author_explicit）

本轮用户确认：**当前 LOM 是法国主导的“伦巴第共和国”；统治者为历史人物挪用的亲法意大利民族主义者。** 该确认是本项目设定依据。不能把开局 LOM 改述为“北意大利共和国”，也不能由“民族主义者”直接推出反法、独立或摆脱法国才算完成国家建设。历史人物在此世界线的政治立场以作者确认优先，不能以现实同名者经历补写或推翻。

## 当前源码（current_script）

| 核对项 | 直接证据与边界 |
| --- | --- |
| 统治者身份 | [LOM 人物历史第3—8行][characters] 创建 `ITA_GUGLIELMO_PEPE`，另创建马志尼。 [佩佩模板第3—19行][template] 给出 Guglielmo Pepe、`ruler=yes`、53岁、北意大利文化、军队IG、将军及 `ideology_jingoist_leader`；不能将“自定义模板”改写为“虚构人物”。中文已有“古格里尔墨”“佩佩”译名。[names] |
| 意识形态与对法立场 | [模板第11行][template] 的 jingoist 标识是机械配置；[现行意识形态定义第2815—2833行][ideology]列军制、海军及殖民法律态度，不能由此推出对法敌意。**亲法意大利民族主义者**来自上述作者确认；本次不提出改意识形态或新增亲法标记。 |
| 共和国制度 | [国家历史第9—18、33—37行][country] 明确总统共和、财富投票、重商主义、干预主义、集会权、国民民兵，军队和知识分子入阁。共和国不是待经反法革命才建立的政体。 |
| 法国主导与两层宗属 | [宗属历史第185—193行][subjects]：FRA 对 LOM 建 `protectorate`；第212—224行：LOM 对 PAR/MOD/TUS 建 `puppet`。这些是具体关系，不等于法国已经承诺统一，也不等于 LOM 政权天然反对法国。 |
| 名称与动态条件 | 基础中文 `LOM` 为“伦巴第”[cn-base]，英文为“Lombardia”[en-base]；`ce_north_italy` 中文为“北意大利共和国”[cn-dynamic]、英文现为“Italy”[en-dynamic]。[动态名第831—847行][dynamic]仅在整有伦巴第、南蒂罗尔、威尼西亚时启用该键；[州历史第8534—8537行][states]将南蒂罗尔给 AUS。不能据这个未满足条件的名称替换作者确认的开局身份；也不能据作者纠正自动授权改名、改边界或修订动态名条件。 |
| tier 与政体分开 | 当前有效原版 [LOM 定义第665—675行][definition]仍是 `tier=principality`、北意大利文化、首都伦巴第；MOD 国家定义检索只在 `.bak` 见 LOM，备份不计活动定义。tier 字段不能推翻国家历史的总统共和，也不因作者确认就自动构成必须修的缺陷。 |

## 原方案应如何重读（建议，未改方案）

以下行号基于 [italy-research-plan.md][plan] 本次读取版本，SHA256 为 `ca449581ff531ba5fae3fb0cf9f780c1ceddec3ac055413ead0d61655aa1d4f0`。

| 受影响位置 | 应调整的推导 |
| --- | --- |
| 第9—15、23、99行：主体、名称与人物 | 主体明确写“法国主导的伦巴第共和国”；“北方共和国”只能作地理描述。第15行提出名称解耦是未获确认的设计建议，不应继续列为纠正开局身份的必要工作。第23行补明佩佩是历史人物挪用、亲法民族主义者，`自定义统治者`仅描述模板技术来源。 |
| 第11—13、61、68、107、141行：自主权的地位 | 自主权可作为谈判议题，但不能把摆脱法国作为共和国唯一尚未完成的使命。法国支持下的民族整合、经济发展和长期协作应是完整可行路线，不是走向反法的过渡站。第107行的体系内协商结构可保留；“争取更高自治”应为具体选择，不能强制所有合作项目先脱离现关系。 |
| 第72、108行：民族主义与反法 | 第72行属于原生按钮的潜在机制适配，不是佩佩或 LOM 的既定意图。第108行“民族主义者挑战法国宗主权”需改为明确的条件性未来分支；须由利益冲突、法国实际行动、执政联盟变化等另立理由，不能从民族主义直接起跳。 |
| 第130行：虚构工业家转向 | 因干预、征用而转向自主派仍可作为候选冲突，但不能用这个新角色的可能转向覆盖佩佩的亲法起点，也不宜使所有融资路线必然导向反法。其余虚构角色仍只是提案。 |
| 第140、159行：实施和验证清单 | LOM 名称/tier 应从“暗示缺陷”改为来源核对项；本次身份纠正本身不要求改游戏脚本或再开局。真正实施名称、动态名或宗属机制后，才按受影响行为安排验证。 |

**可保持的内容：**第35—49行的地区经济差异及第97—101行的建设、军需转产、融资、就业、税款与附属邦议价，不依赖反法前提；第114—122行统一后的财政军制、南北投资、公民资格、罗马和边界议题也不被本次纠正否定。第109—110行南方、教宗及长期多国路线，以及第148—157行国家继承、关系变化、人物退出和旧档处理仍可作为条件性设计。这里仅判断其与新设定兼容，**没有重新认证人口、资产数值、存档观察或未实施API**。

后续规划的合适起点是：**亲法的伦巴第共和国如何借法国支持发展、整合和争取意大利领导权；这种合作在何种具体利益冲突中可能调整。** 亲法不保证法国同意所有要求，民族认同也不自动产生反法立场。这两点应同时保留。

技能复核：本次新增的是明确作者纠正，已在本备忘分层记录；依只读核查范围未改技能。无新增实现或 ENGINE_PASS 声明。

## 定位链接与关键指纹

[characters]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/characters/LOM.txt:3>
[template]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_ce_italian.txt:3>
[names]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_names_l_simp_chinese.yml:63>
[ideology]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/ideologies/01_character_ideologies.txt:2810>
[country]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/LOM.txt:9>
[subjects]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:185>
[cn-base]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_00_countries_l_simp_chinese.yml:437>
[en-base]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/english/replace/ce_00_countries_l_english.yml:453>
[cn-dynamic]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_countries_l_simp_chinese.yml:8>
[en-dynamic]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/english/replace/ce_countries_l_english.yml:8>
[dynamic]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/dynamic_country_names/ce_dynamic_country_names.txt:831>
[states]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:8534>
[definition]: <D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:665>
[plan]: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/cne-time-native-ban-20261103/italy-research-plan.md:1>

| 源文件 | SHA256 |
| --- | --- |
| 人物历史 LOM.txt | `65bd1d1c53933ca2171f008f6fbaa333cf594770e8628503682e6495119ad75f` |
| 人物模板 zz_ce_italian.txt | `dd4f8f72c3c9e747c77c9c1090afa6c606ed740186d603ee39c0bc96f10ea2e7` |
| 国家历史 LOM.txt | `f4ede35d5c0804cd4351eff9e99022839faa2daebb5530947aeef6deccdf5ad2` |
| ce_dynamic_country_names.txt | `19fe37f408bd08f9ef24a850aed99270b3febf481de369120ca2c2872cc2518c` |
| ce_subject_relationships.txt | `78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7` |
