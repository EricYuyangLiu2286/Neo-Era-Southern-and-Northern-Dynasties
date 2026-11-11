# 交通网、港口与海域

> 何时读：新建或移动城市/港口枢纽，修交通网报错（`no connection node`、`non-adjacent`、`has no harbor node`），或做海域与港口的版本迁移。不必读：只调人口和产业（读 map-economy-design.md）。编号规则与编辑器操作见 [map-data.md](../lookup/map-data.md)。

## 2026-10-31 实测补充：locator 不是交通 hub

第一版川陕试案进入实际新局后，新州人口和建筑可用、关中市场接入 100%，但真实日志新增 13 次 `no connection node found in state` 和 5 对旧连线的 `non-adjacent` 报错（每对由两个调用点各报一次）。因此“locator 齐全且经济面板正常”不能视作地图正确。

`WORK/editor/map_editor_runtime.py <export>` 生成独立可写 authoring 副本、隔离用户目录，并以 `-map_editor` 启动。该工具启动本身不是修复或验证。编辑器只用 **Save As**，逐文件确认 `spline_network.splnet` 保存目标是 WORK/map-projects/.../mod；不使用 Save All，不保存到 GAME 或 Workshop。完成后比较差异，导出新的冻结测试候选，再做相邻州调动／动员、市场路径和存读档验证。简易编辑器现已能补显式新港口的harbor/海路（见下文），通用陆路与既有港口移动仍须独立处理；导出保留transport_review_required，不能静默认为全链路完成。

## 有格式证据的 splnet 备选工具

原生编辑器无法稳定完成连线时，可先用 `WORK/tools/inspect_splnet.py` 只读检查实际二进制，再在独立候选上使用 `spline_candidate.py`。后者目前专用于 20261031 川陕工程，不是任意地图的一键发布工具。当前构建的 primitive token 编码来自 Jomini 开源解析器，字段结构从本机原生保存的文件核对。编码前必须满足原文件逐字节 roundtrip；不改的 anchors/strips/connections 须保留原始有序记录。

候选的27条新路线沿 province 可通行像素寻路，并用 heightmap 坡度和高度作代价；它不是史料道路或原生 NavMesh 的等价实现。禁止把这套启发式改名为官方自动寻路。20261031T043941Z 冷启动已消除第一版新增的23条节点/不相邻连线错误；实际军队完成河南→汉中→陕北、贵州→川南→成都→重庆五条和平调动，且原生读档恢复成功。详见 WORK/research/20261031/map-design/道路与运行验收记录.md。其余线路、全网视觉及跨国战争仍待验；零静态错误和无启动报错都不替代实际到达检查。

## 2026-10-31 原生海港断链：陆地port与海面harbor不同

run162626冷日志真实新增三条 `travel_connection_definition.cpp:128 Port node ... has no harbor node to connect to`。新增南大原316903、海南317003、南中部317103都有port locator、naval_exit和陆地交通节点，仍不能成立海港。当前375个带port地区中只有这三新州缺harbor；其余372个本体/继承港口有海路层。

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
