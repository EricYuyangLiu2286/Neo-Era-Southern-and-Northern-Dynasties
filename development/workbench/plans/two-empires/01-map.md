# 01 地图、资源与引用迁移

状态：已有独立候选；后七州交通与全部直接引用待引擎验收。目标是可经营的地区、可信的政治空间和可走的交通，不是靠切州刷免费税容。

## 设计与取舍

累计候选包括关中/陕北/汉中、成都/川南/川东/梓潼、晋中/晋北、燕京/承德、吉林/松江、荆州/襄阳、赣北/赣南、桂南/桂林。逐州边界和locator来源在 `WORK/research/20261031/national-design/national-map-candidate.json`；比例是候选设计而非史实人口普查。全国审议不能只看拆出的州：没有拆分的江南、山东、河南、广东、福建等仍需核对承载、市场和故事功能，日本州界严格保留。

晋北为1819大同共和起义提供独立政治空间，晋中保留煤钢起点；不能直接把1860年代成熟工业放进1836。东北的分州给不同开发次序、交通瓶颈和生态/资源容量，不把空旷州开局都建满。四川盆地的多中心让地方军政与内陆供应有实际路线。赣南、桂北等需能解释交通、资源或政治决定，否则撤销无功能的拆分。边界必须是连通province集合，不能仅以经纬切线替代河谷与枢纽审议。

## 文件关系与实施

`map_data/state_regions/*.txt` 的 ID/provinces/resources/arable_land/traits/hubs → `common/history/states/00_states.txt` → `history/pops`、`history/buildings` → `country_definitions/ce_countries.txt` 的首都、`history/countries`市场首都和军队；反向检索所有 `STATE_*` 引用，包括公司、统一、叛乱和战争目标。随后联动 `gfx/map/map_object_data/generated_map_object_locators_*`、`gfx/map/spline_network/spline_network.splnet`、strategic_regions，以及localization/replace/map和hub names。素材层沿用原有地形纹理，不修改位图环境。

特别处理：HNA原首都和军队重心究竟指荆州还是襄阳；NSX起义原来锁STATE_SHANXI，拆晋北后须按大同历史定位，不能沿用旧键让起义发生太原而不自知。粮食、煤铁和工业不应所有类型同一比例分家，保留工矿聚集与已有线路；民政、首都、军营、海军各自审阅。

## 全程与验证

1836验证每州国界、人口文化、所有权、军队驻地、资源上限、耕地及税容。中期验证地方独立后港口/陆路/市场接入与战线；终局验证统一、首都迁移、州被第三国部分占有时的选项与claims。守恒按国家×文化×宗教、建筑种类×所有者、全部province一对一归属分别核算；全球资源容量的有意变化另记，不能藏在拆分取整中。

执行：先自动反向引用索引→逐引用语义判断→非均匀产业/首都配置→冻结→新局→七州相邻真实军队到达及必要战争→保存读档。原来五次川陕和平到达仅覆盖早期三州；不扩充为全图通过。

已执行依赖反查：生成critical-impact.json，在独立`national-reference-fix-20261031T121919Z`纠正HNA首都至襄阳、NSX首都及释放位置至晋北，含CNE初始化目标修复及紫禁城1级恢复。121319版仍缺紫禁城，已被替代。未移动军队招聘地：对应原有营房，不能把它误当军队总部必须跟首都走。SHN通用山西国首都和刘秋甫home_region暂保留晋中，缺乏迁往大同的依据。候选源自纯地图+路线113226，不含71项经济试案。真实进CNE及首日存档已完成，新七州路线、战争及全部引用仍待验。

土地来源已逐文件核验，见[evidence/arable-provenance.md](evidence/arable-provenance.md)。当前容量原样拆分：山西262+73=335、河南500；赣北408+赣南192、桂南240+桂林160、荆州192+襄阳128、川东340+梓潼160。它们目前仅有守恒证据，还需地理与经济验收。不得以原版375推断作者335被损坏，也不得称河南500过大而无依据扣40。

接下来的地图依赖迁移在[evidence/southern-map-migration.md](evidence/southern-map-migration.md)逐处区分旧领土集合、特定城市和名称。先修flavorUSM中对新梓潼/襄阳/桂林等的漏覆盖，不把大范围事件改成重复对每州施加同一全国后果。

## 固定人口边界与长期恢复证据（2026-10-31续）

人口审计入口：[population_envelope_audit.py](../../tools/population_envelope_audit.py)。固定作者原地区基准和新拆州分配均有钉死SHA；按province归并子州，报告国别/文化/宗教和全球变化，不滚动重设25%基准。[真实文件树边界测试](evidence/population-envelope-real-input-verification.md)已验证恰好±25%通过、越1人拒绝、累计改名+56.25%仍拒绝、有理由全球增减允许。当前integrated/A均未重配人口，781原地区全在界内；见[实际审计](evidence/population-envelope-integrated.md)。

[年度及七月自然运行](evidence/integrated-economy-longitudinal-findings.md)已改变试案判断：贵州10级染料不缩减，七月当地饥饿231,835→72；SHA等自然改善，A仍实验、B未实施。逐项试验价值和正常/危机多路线均写入报告，不把失业人数直接转成人口迁移或补地目标。
