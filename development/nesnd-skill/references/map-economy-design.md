# 地区尺度、设定与经济共同设计

开始地图经济工作时，重读当前 `ppet` 的相关页和原 MOD，而非沿用此前简化的阵营总结。2026-10-31 完整重读 29 页，原始提取、源 SHA、三张内嵌图片在 `WORK/research/20261031/map-design/ppet-reread.json`。PPT 内日期和姓名有版本冲突；1836 前事实、官方未来结局、可供玩家改变的分支须分别处理。具体事实和冲突见同目录设计报告。

## 图像与数据入口

- `GAME/map_data/provinces.png`：8192×3616，每个 RGB 对应 province。不改变像素、地形和河流，仅重分组时仍需确认省份连续。
- `heightmap.png`：16384×7232，使用同范围的 2 倍坐标裁切；`rivers.png` 同 province 图尺寸。高度只供判断地形，不把游戏投影像素当平方公里。
- `map_data/state_regions/*.txt`：ID、provinces、city/farm/mine/wood/port、资源、耕地、traits、impassable、prime_land、naval_exit_id。
- `gfx/map/map_object_data/generated_map_object_locators_{city,farm,mine,wood,port}.txt`：instance.id 对应地区数字 ID。本机已用 12 个川陕旧枢纽核对：图像 x≈position.x，图像 y≈3615−position.z。新地区必须有对应 locator；移走原枢纽时也要重定位原地区。不要把字典序首个地块当合格城市。
- `localization/simp_chinese/hub_names_l_simp_chinese.yml` 与 MOD replace：真实枢纽地名。新地名须有地理或设定依据。城市、矿、林、农四个枢纽都需对应地块，不把全部挤到同一点。
- `tools/map_design_audit.py` 生成当前州人口、产业、资源、真实像素面积、province 邻接和 locator 像素归属证据；`map_design_options.py` 生成地理提案图。它们只写 WORK，图像是分析结果，不是引擎验证。

## 避免错误归因

1. 当前 defines：每整合州基础政力费 10；每 10 万人口基础费 4；机构另计。base_values 每州税容 100、基础设施 3。税容每点对应 1 万人口。最终数值受法律、科技、州比例和修正影响。
2. 拆两次州原始增量为 +200 基础税容、+20 州底费；没有删除人口机构成本。原 CNE 约 −6000 政力不能主要归因于陕西太大。拆州可改善地方可玩性、税容分配和政治分支，但不能靠免费基础量任意切碎全国。
3. 拆州同时改变当地价格、规模收益、资格/工资、基础设施、建筑上限、征兵、战线和政治运动。必须比较纸—木—硫、煤—铁—工具、粮食—人口、军火—驻军与贸易枢纽，不能只做行政加减法。
4. 小地区不一定更合理；稀疏边疆和富裕港口不按统一人口/面积阈值处理。先列该地区承载的玩家决定，再判断边界。

## 迁移合同

### 唯一建筑也属于迁移图

2026-10-31全国候选漏掉紫禁城：旧工具只数所有权`levels`，没有数纪念建筑的顶层`level`，旧守恒检查同样漏检。修复后统计两种形式；拆分遇到顶层level建筑必须在修改前明确保留哪侧，不能按比例变零或复制两座。紫禁城原版`common/buildings/08_monuments.txt`还有`unique=yes`、`potential state_region=STATE_BEIJING`及`forbidden_city_locator`，需联查建筑定义和实际定位。当前全国方案它保留燕京，恢复原1级；若未来移动到新地区，还要迁移potential/locator等引用，不能仅改历史块。证据在WORK/plans/two-empires/evidence/monument-regression.json，静态回归不等于引擎验收。

### 2026-10-31 实测补充：locator 不是交通 hub

第一版川陕试案进入实际新局后，新州人口和建筑可用、关中市场接入 100%，但真实日志新增 13 次 `no connection node found in state` 和 5 对旧连线的 `non-adjacent` 报错（每对由两个调用点各报一次）。因此“locator 齐全且经济面板正常”不能视作地图正确。

`gfx/map/spline_network/spline_network.splnet` 另存交通 anchors/strips；本机文件是二进制，不能当 PDX 文本解析或随意字节替换。土地 hub ID 为 state ID×100 + 类型（city00/farm01/mine02/port03/wood04）；与视觉 locator 的 ID 不是同一编码。新州需要四类交通 anchors、州内连通和可通行相邻州连接；移走旧 hub 的位置后还要处理旧连接。来源为地图作者本人的 [实作指南](https://steamcommunity.com/sharedfiles/filedetails/?id=3165669021)，并由本次真实日志证明必须补做；指南版本较旧，操作以本机编辑器为准。

`WORK/editor/map_editor_runtime.py <export>` 生成独立可写 authoring 副本、隔离用户目录，并以 `-map_editor` 启动。该工具启动本身不是修复或验证。编辑器只用 **Save As**，逐文件确认 `spline_network.splnet` 保存目标是 WORK/map-projects/.../mod；不使用 Save All，不保存到 GAME 或 Workshop。完成后比较差异，导出新的冻结测试候选，再做相邻州调动／动员、市场路径和存读档验证。简易编辑器现已能补显式新港口的harbor/海路（见下文），通用陆路与既有港口移动仍须独立处理；导出保留transport_review_required，不能静默认为全链路完成。

原生编辑器实测（1.13.11）：Spline Strip Tool 在左栏线网图标；右侧地区筛选支持 `|`，清空按钮比全选替换可靠。选择地区后工具提示为 `Automatically place all hub anchors for currently selected territories` 的按钮会按现有 locators 生成节点。右侧 AnchorID 搜索可定位节点，双击输入框原有数字可替换搜索；点结果会把相机聚焦节点。视口右键取得焦点后分次滚轮缩放。**不要修改已有连线的 anchor index**：本轮把 49401 改为 315900 时原生编辑器崩溃（04:10:01，E06D7363）；先另存检查点，解除旧连线／删除重建后再连接，编号应在首次连接前确定。崩溃证据在 WORK/map-projects/spline-authoring-20261031T035657Z；`map_editor_runtime.py <map-project> --resume` 复用隔离工程并先归档旧日志/崩溃，不覆盖证据。

每个候选明确 province 集合、连通分量、保留国界、枢纽位置和命名、人口按文化宗教逐组分配、各类建筑及所有权、军队、耕地/可发现资源/固定资源、州特征、整合/祖地、战略区、首都/公司/事件引用。纯拆分事务须守恒；有依据的经济再设计可改变容量，并单列增减及理由。用户2026-10-31明确允许增加新州的`arable_land`，不必从其他州扣回以凑全局总量。以地形、聚落、当地自给配员、商业农业占用和未来开发任务决定增量；有空余自给岗位却未招聘时，先查工资、盈利、资格、歧视和招聘冷却。不同产业可用不同分配比例并给出理由。用户的简易编辑器默认人口与建筑各半，但定制地图设计的比例可以根据明确方案调整；不得把面积比例误称真实人口分布。

正式合入前在冻结导出上新开局，检查所有新增地区的地图/建筑/就业/价格/税容与存读档；比较无政策操作的月、季、年财政。历史改动不承诺兼容旧存档。保留未拆州候选供 A/B 对照，并分别记录工业调整和地图调整的影响。

### 有格式证据的 splnet 备选工具

原生编辑器无法稳定完成连线时，可先用 `WORK/tools/inspect_splnet.py` 只读检查实际二进制，再在独立候选上使用 `spline_candidate.py`。后者目前专用于 20261031 川陕工程，不是任意地图的一键发布工具。当前构建的 primitive token 编码来自 Jomini 开源解析器，字段结构从本机原生保存的文件核对。编码前必须满足原文件逐字节 roundtrip；不改的 anchors/strips/connections 须保留原始有序记录。

候选的27条新路线沿 province 可通行像素寻路，并用 heightmap 坡度和高度作代价；它不是史料道路或原生 NavMesh 的等价实现。禁止把这套启发式改名为官方自动寻路。20261031T043941Z 冷启动已消除第一版新增的23条节点/不相邻连线错误；实际军队完成河南→汉中→陕北、贵州→川南→成都→重庆五条和平调动，且原生读档恢复成功。详见 WORK/research/20261031/map-design/道路与运行验收记录.md。其余线路、全网视觉及跨国战争仍待验；零静态错误和无启动报错都不替代实际到达检查。

当前原生军队界面：地图旗帜按钮是“战略目标”，房屋旗帜按钮是“驻扎地区”。只有后者显示实际行程天数并发起移动。选中汉中作为战略目标不等于已测试军队移动。暂停/运行可用右上角按钮；键盘快捷键无效时改用可见按钮并核对日期，不能把调用成功当游戏接收到按键。

### 地方就业证据

`save_structure.py` 现导出逐 state 的职业劳动人口、配员等级、基础设施与建筑账项，且已对21国验证州总数等于国家总数。使用同一候选的英国/法国/日本数据时必须注明它们属于 MOD 世界；独立原版对照是另一运行档案。新的地方分析见 `WORK/research/20261031/map-design/地区就业与财政补充.md`，不要只比较全国农民比例或建筑数量。

拆州前还要检查劳动人口／总人口比与可耕地承载：CNE在保留女性财产权后约30%劳动人口，原版大清同州约25%；不能按相似总人口照搬原版岗位。山西335耕地和现有产业已留下约66万失业劳动力，纯拆州只重新分配这些岗位，不会消除缺口。新增纸煤硫还使基础设施116.1/108.03，需实物铁路及其引擎煤供应才能恢复100%接入。地图、制度、工业、交通与家庭收入必须联验；证据见北朝供应链运行记录。


### 2026-10-31 原生海港断链：陆地port与海面harbor不同

run162626冷日志真实新增三条 `travel_connection_definition.cpp:128 Port node ... has no harbor node to connect to`。新增南大原316903、海南317003、南中部317103都有port locator、naval_exit和陆地交通节点，仍不能成立海港。当前375个带port地区中只有这三新州缺harbor；其余372个本体/继承港口有海路层。

当前1.13.11实文件的节点约定：陆地port锚点`state_id*100+3`；独立harbor锚点`(1<<23)+state_id*100`；海域锚点同为`(1<<23)+sea_region_id*100`。原广东harbor8438308用type3条带1121027连南海8694208；原CA harbor8421208用type3条带1577219连太平洋8703908。节点编码来自当前原生文件实证，换版本须重新核对，不把经验公式当永久API。海面connection键与端点/条带类型保持原生同形；港口陆地→harbor连接由引擎按对应ID识别，不能用陆地铁路替代。

沿海新州必须一起生成port定位、陆地port锚点、独立harbor、到naval_exit实际海域的type3条带及connection；所有海路采样点在实际海面，不能穿陆或给岛屿制造陆路。port所在province必须邻接所选海域；现有原生标记可能有1像素视觉偏移，需保留证据并实际看港口。移动已有港口时还要同步旧陆路、harbor位置/海路，不可仅补一个新点。

`WORK/editor/harbor_routes.py` 已将**显式新港口操作**缺失的harbor/海路补入独立导出暂存，配合set_hubs选真实沿海像素；无geometry动作工程不暗改源网络。未知海域、非沿海port、需重新处理的既有陆地锚点拒绝猜测。通用陆路/既有港口移动仍有范围边界，报告transport_review_required不能因此清除。

窄修补`exports/harbor-closure-20261031-a`父F，仅改splnet；旧记录全保留，三个新harbor及三条海路。证据`WORK/plans/two-empires/evidence/harbor-closure-a.json`、`harbor-closure-plan.md`。静态海面路径和二进制往返只是入口，必须冷启动消除对应真实错误，并实测新港的舰队出海、贸易/海路、存读档，才标海港验收通过。13个新州逐像素海岸审计`thirteen-new-states-harbor-audit.json`证明早先10州（含松江）均内陆，新增3州有海岸，不因无error就省略位置核验。

### 已知负例驱动的导出门禁

`WORK/tools/map_transport_preflight.py --candidate <MOD根> --regions <受改STATE...> --out <报告.json>`先对全部有效地区做naval_exit编号存在性、唯一性和海域类型检查，再检查指定州的splnet逐字节往返、重号、悬空strip/connection、hub的locator/anchor、陆路图连通和harbor至naval_exit。早先旧F三处missing harbor能检出、13新州通过，仅是当时的局部结果；新门禁已用D2只指定福建两州仍检出全球26个旧海域失效编号。它不验证整条路径地形或引擎NavMesh；像素/海面采样和真实交通仍另验。

### 海域版本迁移：编号有效不等于地理正确

1.13.11本轮反例：夏威夷继承的naval_exit_id=3001已不存在；另有旧编号被其它海域沿用。不能只检查编号存在，或因harbor在全球连通海网中能到达该编号就放行。旧检查只跑新州，漏掉未改历史文件继承的过期引用；这种依赖错误应修复全部实际受影响地区，即使对应TAG剧情尚未完善，也不改变其领土/人口/产业设计。

迁移按有效加载后的`default.map`之sea_starts、`state_regions`海域province、实际`provinces.png`邻接，核港口province邻接的海域；再核视觉port、陆地port anchor、独立harbor位置和直接海路端点。海图全局可达仅是连通性条件。源`99_seas.txt`、default.map、province图或基础splnet变更时，对全球既有港口重新做此闭包；之后局部地图修改可复用其指纹一致的全球几何证据，但每次仍做便宜的全局编号/类型扫描。按实际地理重新对应海域，不能把原版国界或同名州整体覆盖进架空地图。

把“需解释的不一致”与“已证错误”分开：当前本体也有港口声明province、视觉locator、harbor和直接条带不全重合的实例。源海域迁移可由当前同港声明+实际海岸证据确认，同时把未改的本体视觉异常记录为继承例外；不要为了让自制几何规则全绿而交换港口/海港编号或改变岛屿用途。是否需要修这些本体例外须另有引擎行为或更强设计证据；它们不能掩盖MOD自身过期编号。

负例入口：`WORK/plans/two-empires/evidence/d2-global-naval-ref-negative.json`，工具回归`global-naval-reference-gate-regression.json`；后者明确保留“指向遥远但有效海域”不会被编号门禁发现的测试，防止再次误称全图正确。海域窄修的全局像素/harbor审计与实际新局门禁见`WORK/plans/two-empires/38-global-naval-exit-migration.md`。这些检查通过仍不能证明市场接入、航行、战争路径或经济正常；需新局看实际港口/航线和存档，旧海运有混杂因素的经济局不得被当作纯产业对照。

1.13.11原生存档中的`counters.market_access`是缓存更新计数，不是接入百分比。当前实测state/region记录未直接保存naval_exit或市场接入率时，不能用该计数、基础设施够用或已实例化的port/harbor/strip替代UI/原生getter；缺字段就是不可由该档直接证明。地图定义id与原生manager对象ID也不保证相同，用template/region名称解析身份。批量读67个港口的节点闭包可减少屏幕操作，但仍与实际市场接入、舰队到达分开记录。

地图修改作为一次事务：独立省色/人口/行业/资源/军队分配表→hub/locator→陆路与海港图→历史/产权/首都→语义引用（经营范围OR、完整拥有AND、唯一地点只保一处）→新局实际交通/战线/存读档。详细工作方法与162地区复审在WORK/plans/two-empires/31-regional-scale-review.md。全国早先七州曾共用ratio初分多类资产，这只能算待审初稿，不因非50%便称合理。新剧情需要可重新审议旧封板。
