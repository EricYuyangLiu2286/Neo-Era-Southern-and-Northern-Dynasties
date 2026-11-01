# 38 — 全局海域引用迁移与港口闭包

最新状态：用户要求**停止新增内容，仅debug与总结**。当前可测试交付为 `exports/debug-naval-20261031-e1`，仅把68个既有海域引用BUG修复叠到C5，506文件/794地区，**没有新增福建州**。D2/福建设计封存待另行安排；不得以本计划早期父版本描述将其混入debug交付。E1静态与独立复核通过，根负责新局实际验收；主MOD、源GAME、Workshop和冻结父版未改。

## 触发、范围与父版本

夏威夷港口经济追踪暴露继承的 `naval_exit_id=3001` 在当前1.13.11有效海域数据库已经不存在。扩大只读扫描后，共26个地区引用不存在的编号；还有旧编号仍有效但地理含义变化，不能以“存在”和全海网可达判正确。此问题涉及未完善国家，也须修其技术引用；不改变这些国家的国界、人口、产业、政治或剧情。

最初分析分支以 `exports/integrated-fujian-20261031-d2` 为精确父，保留福建北部795地区体系，仅用于追溯68引用差分。用户最新停止新增内容以后，已将D2→naval-A的这68处差分三方合到C5；没有拷入D2的其它内容或整文件覆盖C5。最终E1保留C5的PHI A7、原福建边界和794地区。不得为迁移海域复制原版新国界。

## 依赖图与分工

有效`default.map sea_starts` + 有效海域state_regions + `provinces.png` → 每个现有port省色实际相邻海域 → port视觉locator/陆地anchor → 独立harbor的位置 → 直接sea strip端点/海域anchor → naval_exit_id应指的当前海域 → 全部历史/人口/建筑/军队保持 → 新局实际市场和航行。

既有扫描由 `phi_native_contract_reader` 继续完成，不另写重复省色解析器：检查所有有效region ID重复、实际海域RGB邻接、port和harbor落点、直接海域端点；逐行给旧值/新值/证据，独立导出candidate。`map_workflow` 复核父差分、现有交通工具边界、地图与经济工作流，以及关键反例。根独占UI进行冻结后的实际测试。

## 已完成的导出门禁修正

`tools/map_transport_preflight.py` 以前只扫描 `--regions` 指定州；harbor至naval_exit仅检查海图连通，无法发现一个仍有效但遥远的海域编号。现在每次都会先对全部有效地图地区的 naval_exit 做：

1. 编号存在且唯一。
2. 目标province全部属于有效default.map的sea_starts，不能误指陆州/湖。
3. 记录所有引用、目标key、default.map SHA，再做旧有指定州交通测试。

编号类型门禁仍不做地理推断，未伪装成全局像素/直接海港验证。后者由独立扫描完成。旧脚本已保存在 `evidence/map_transport_preflight-before-global-sea-gate-20261031.py`。

真实负例：仅对D2指定`STATE_FUJIAN STATE_NORTHERN_FUJIAN`运行，仍检出全球26失效引用，详见 `evidence/d2-global-naval-ref-negative.json`。`tools/test_global_naval_reference_gate.py` 包含正确海域、缺失编号、陆地编号、重复编号、遥远但有效海域五类；最后一类明确不由此门禁识别，防止再作超范围保证。结果 `evidence/global-naval-reference-gate-regression.json`，未改候选。

## 候选修改与静态验收合同

- 每个修改必须有现有港口省色与正确近海的地理证据；原版现有同州定义只作交叉核对，不能凌驾实际MOD港口。
- 优先只改错误的 naval_exit_id。若网络原本指正确近海，保持splnet全部字节；若真实网络也错，独立列出必要的最小闭包，不随意移动港口/历史建筑。
- 跨文件所有 naval_exit 引用扫描，而非只改当前关注TAG。有效旧ID重用必须有地理检测，不能只修26个缺失ID。
- 候选与D2逆转明确标量补丁后AST应全等；人口群体、建筑/产权、耕地/资源、state/province边界、军事、首都、政治与PHI文件保持。metadata只改变候选身份。
- 全局编号类型门禁、逐港口像素/harbor/直接sea端点、15新州交通和负例通过后做独立备份。Tiger新增诊断单列，不用其代替几何或引擎。

### 复杂例复审（实现前依据）

全图377个port/exit条目无重号；本体自身有6条直接sea strip与声明不一致、3条port省色与声明海域不邻接，故不能把扫描器所有几何提醒升级为致命错误。最终拟68处窄改：63项港省色/当前原版/直接海路一致，4项当前同港官方声明+港海岸一致且保本体视觉例外，1项无port且当前本体也无port/exit的Kuopio孤立字段删除。

独立复核4例证据 `evidence/global-naval-four-exceptions-independent.json` 与坐标图 `global-naval-four-exceptions-coordinates.png`：French Low Countries 3028→3105；West Micronesia 3002→3157；Picardy保持3028；Kaunas保持3000。四州的province、port、locator、port anchor、harbor和直接条带均与本体逐项相同，修改只恢复已有港口声明的当前海域引用，不搬港。法国两州的harbor位置疑似跨州沿用、西密克罗尼西亚声明与视觉位于不同岛屿，均保留明确未证项，不推断成用户领土设计错误。

实现代理另核：Malaya 3052→3072、North Borneo 3055→3072，真实港海岸与harbor像素均在Malay Sea且当前同港本体声明一致；Formosa/Alaska不改，其全州与声明海域相邻且本体现行一致。Alaska作者port与visual落点差异另记，不用本轮窄修抹去。上述判断不表示这些地区实际航行已通过。

## 已生成候选与独立复核

候选 `exports/naval-exit-closure-20261031-a`，精确父D2；独立备份 `backups/candidate-naval-exit-closure-a-20261031T224853Z`。构建工具 `tools/build_naval_exit_closure_a.py`，父子完整清单/68项依据 `evidence/global-naval-exits-migration-a.json` 与 `.diff`。只有9份state_regions文件和metadata改变：67个exit标量改值，Kuopio删除1个孤立exit。

独立工具 `tools/review_naval_exit_candidate_a.py` 不信任构建器自己的守恒结果，重新逐文件读取父子SHA和有序AST。去掉naval_exit字段以后所有改过文件AST完全相同；全部非map文件除metadata逐字节相同。因此地图边界、population/building/军队、L2四耕地、福建、字面首都映射、政治、PHI和整个splnet均保留。报告 `evidence/global-naval-exit-candidate-a-independent-review.json`。

新候选376个有效exit，missing/type/duplicate均0，无剩余明确迁移建议；几何提醒的**具体州与类别**与本体现行逐项一致，不只比较总数。原版固有6 direct-strip、3声明港邻接、1整州邻接提醒保留为已解释例外。全港通用交通检查273条提醒、原版275条，新增0；差的2条是原本广东mine/wood缺节点的提醒在此工程已不出现。不能因此写“全图0错误”。15个新州专项transport报告仍为0错误。

证据入口：`global-naval-exits-a-after.json`、`global-naval-exits-vanilla.json`、`global-transport-naval-a.json`、`global-transport-vanilla.json`、`naval-a-15-state-transport.json`，均位于本计划evidence目录。naval-A是封存分析分支，实际debug交付以以下E1为准。

## 当前debug交付E1：没有新福建内容

`tools/build_debug_naval_e1.py` 使用现有 `combine_candidate_patches.py`，配置 `evidence/debug-naval-e1-merge-config.json`：base C5、patch parent D2、patch candidate naval-A。三方无冲突；输出 `exports/debug-naval-20261031-e1`，只有9map+metadata改变。精确68字段old/new列表与独立审过的naval-A相同；剔除这些字段以后C5地图有序AST全等，所有非map文件除metadata字节相同。不存在STATE_NORTHERN_FUJIAN；原福建province、资源、人口、建筑、军事和所有脚本均保持C5。A7五个PHI脚本另经独立SHA核对。

E1新扫描375个有效出口，missing/type/duplicate=0，迁移建议0；剩余具体地理提醒与本体现行集合完全相同。原13新州加旧福建共14州专项transport=0错误。Tiger以C5为基线1034→1034，新增0。工具 `finalize_debug_naval_e1.py`，证据 `debug-naval-e1-static.json`、`debug-naval-e1-independent-review.json`、`debug-naval-e1-global-geography.json`、`debug-naval-e1-14-state-transport.json`、`debug-naval-e1-tiger-delta.json`。

独立备份 `backups/candidate-debug-naval-e1-20261031T225349Z`，修改前C5备份 `pre-change-debug-naval-e1-20261031T225349Z`。E1尚未据本地检查标engine_verified；根将用它做海域新局验收，不复用旧存档的历史地图当新图证明。

## E1真实新局载入（run230637，Jan1）

根实际进入USM新局并保存 `runtime/profiles/20261031T230637Z/save games/大明联邦_1836_01_01.v3`，seed2070510175/checksum6fc2。严格分段的冷日志为153条，与C5的153条逐项归一化完全相同；新局初始化另添一条USA–USM历史rivalry无法维持提示，合计154。没有旧档missing-mod提示、没有新增海港或none脚本报错。旧C5“cold快照”文件实际还混有两条后续记录，总155，已经按22:46:09截断后比较，不能错写分母155。证据 `runtime-230637-bounded-cold-comparison.json`。

复用原生section/database读取器检查全部68受改region，对应100个国家所属state。**这些state与region记录没有直接序列化naval_exit、connected或市场接入百分比**。Hawaii state118属于USM，基础设施8.30127/use6.6；`counters.market_access=54`只是缓存更新计数，绝不表示54%或连通。67个有港的受改region全部实际实例化port、harbor及其源直接type3连接；第68项Kuopio只是删孤立出口。Hawaii有真实节点port1367/harbor3225与`strip_8419508_8703308_3`，对应当前静态3147海域。

这一步证明新图节点已进入引擎，不证明67处市场都100%、舰队已实际航行或全部战争路径正确。根仍在做Hawaii UI读取与约两周自然运行；报告不代填尚未观察的结果。数据 `runtime-230637-naval-native-Jan1.json`，工具 `audit_naval_exit_runtime_e1.py`；从源字段缺失出发明确可证边界，没有把静态声明或计数器当原生百分比。

## 新局实际门禁及经济结论边界

首次引擎验收必须用新图新局，读取实际港口接入、海军出入/贸易路径、错误增量与存读档。优先夏威夷及本轮错误分布覆盖的代表港口；其余未实际运行的港口保留未证标记，不把一艘船成功写成全图战争路径认证。

旧C4自然局的夏威夷持续短缺不能独立归因为产业缺货：无效海域引用是一项需排除的运输混杂因素。修图前后先复测真实市场接入/当地价格/短缺，再决定37经济候选。既有CNE容量测试、PHI合同测试可保留各自范围证据，但不能因此宣称所有沿海TAG经济通过。

## 工作流增量

已在技能 `references/map-economy-design.md` 和 `references/incremental-editing.md` 修订局部绿灯的适用边界，增加全局cheap引用扫描、源海域变动时全港口地理闭包、有效ID重用反例。修改前副本在本计划evidence中。只录会改变下次操作的规则；具体数量、候选状态和省色对应留本计划/证据，不固化为永久地图事实。
