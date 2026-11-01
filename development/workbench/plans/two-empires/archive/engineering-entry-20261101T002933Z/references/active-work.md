# 当前交接：2026-10-31 DEBUG ONLY## 2026-11-01 用户重启前断点（优先于以下全部历史）用户要求简短工作报告并准备重启程序；停止新增修改与新运行。最终统一候选 `WORK/exports/batch-debug-20261031-f1` 已生成，514文件，独立验证备份 `WORK/backups/candidate-batch-debug-f1-20261101T000328Z/mod`。精确合并：E1海域修复+C5→JapanA1（含Lin原线）+E1→功能本地化A+E1→字面scopeA；无新增福建州，无新经济调数。主MOD未覆盖，F1尚未进入游戏。统一检查已真实完成：`WORK/validation/runs/f1-global-20261101-final/report.md` / summary.json，17项中12 PASS、2 FAIL、3 NOT_RUN，候选与冻结工具前后SHA一致，真实stdio MCP PASS。人口固定±25%、历史顺序语义、生产/资源、全局海域及交通结构PASS。FAIL为内容闭包与Tiger待分类，不等于17项全通过：候选自身简中缺键0，内容唯一缺项是原版great_game_complete_tt的`$concept_geogregions$`拼写；实际原版已存在`concept_georegions`和`concept_georegion`，均译“地理区域”。尚未写MOD兼容alias，也未创建F2。Tiger新增原版annex克隆的枚举/target_region及3处纯缩进提示已有源码证据待汇总，26处character裸ig访问仍未实机证实，不批量改。已实测的PHI正常到期/提前撤约来自C5，陈案购买/撤卫/到期/指定负伤及部分日志/姓名来自此前精确版本；不能移用成F1全通过。E1/run230637实际新局USM Jan1已保存，seed2070510175/checksum6fc2，67港口连接已实例化；实际市场接入率/舰队到达未验证。CUA曾返回停止信号，root停止UI，不归因用户按ESC。重启后必须先枚举进程/窗口，不能沿用exec24443、window7934766或假定正常退出。SKILL已更新并quick_validate PASS；新增文件功效/替代入口、war_goal_types与on_wargoal_enforced用途、允许日本吞并后恢复、集中源码→批量代码→统一Python/MCP→集中引擎→差异回流流程。用户要求只DEBUG仍有效。当前执行计划40，原始范围12，详细状态总表`evidence/debug-status-and-release-blockers-20261031.md`。统一入口`WORK/tools/global_validation_runner.py`，用法`WORK/validation/README.md`。恢复先读F1最终报告与上述source-review，收口真实缺陷和工具分类，再集中验证F1日本吞并/重建/占领重试/玩家失国、Lin成功及失效、海运与既有未测关键分支；最后才备份合主MOD和建立成功版本。CNE完整改革、明吴其它结局/转国、海外市场退出与编辑器等原始验收欠账仍保留，不能称整个MOD已经完成。## 当前范围与运行状态（优先于下方历史）**用户已停止新增内容：只做DEBUG与收口，不扩剧情/路线、不再拆州、不调整经济数值。** 已有新内容候选冻结保留，未全验收、未发布、未合入主MOD。首读[DEBUG成果与发布阻断总表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/debug-status-and-release-blockers-20261031.md>)。最新工作流与本批距离见[40集中修复](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/40-batched-debug-and-delivery.md>)：集中源码分析→本批代码闭包→统一Python/MCP并修错→集中引擎验收→差异反馈。当前names代理做日本吞并后重建+Lin现有路线修复，map代理做复用现有工具的统一验证runner；root已更新SKILL/系统设计/增量编辑，格式验证通过，catalog CURRENT changed0。C5/run224458已正常退出，exec75069 exit0。PHI现金A正常到期和提前退出后自然运行已由root实际验证；付款与镜像清理原生证据已写总表。此通过仅限已测两条路径，改约/战争/亡国、B完整同tick仍不能一并认证。**当前实际运行**：`debug-naval-20261031-e1`，run`20261031T230637Z` / exec24443，profile同stamp；实际USM新局Jan1已保存，窗口7934766/gameplayO，checksum6fc2/seed2070510175。随后CUA返回停止信号，root停止窗口操作；不据此指认用户按ESC，不继续本轮UI。506文件、794地区，无新增福建州；不重复launch，不加载旧地图存档冒充新局地图验收。67受改港口节点/海港/直接连接已在native实例化，仍没有取得实际市场接入率或舰队到达证据。运行记录为`WORK/reports/runtime/20261031T230637Z/run.json`。**发布阻断与用户纠正**：日本被吞并本身允许，错误是后续三政权恢复入口依赖已死JAP导致断线。按最新用户指示保留可接受吞并，查`diplomatic_plays`/`war_goal_types(kind/on_enforced)`/`create_country`及存活胜者事件、日志、月脉冲，接通既有三方恢复；没有必要为了回避吞并重设计整场战争。其它海外结局、失败玩家续玩仍按原设计逐项判断，不将日本许可推广到所有国家。39号审计与总表须按此修订，不继续把“全吞本身”一概当P1。林汉涵原线最小修复`lin-defection-regression-20261031-a`已独立备份/静态检查，**未实测、待与本批整合**。安全边界：本体、工坊、旧项目和文案只读；EAC素材不得复制。工作工具/证据/备份在WORK；主MOD不自动合并，运行frozen不改，UI只由root操作。仅获授权的最小BUG修复进入独立候选；停止新增内容。静态检查、Python模型、同名事件有调用均不等于引擎已验。保留人物同ID、第三国领土/玩家控制权及固定地区人口基准；经济候选未生成，旧跑局海路故障不作调数依据。下方记录均为历史，不能覆盖本节。

## 224458 C5已启动；全海域迁移是经济新局前置条件（历史）root确认C4/run214835已正常退出exec14417 exit0、frozen unchanged=true、gameplayM closed。当前C5=integrated-preview-20261031-c5已启动run20261031T224458Z / exec75069，506文件、同stamp profile；May1/Gbuy/Jan1启动前seed。root独占UI并等待实际加载。勿按下文旧run状态重复launch；C5是PHI A7到期修复测试，未改地图/经济，尚不能宣称新逻辑实机成功。37号经济候选暂停落地，离线PM与分州容量算表见WORK/plans/two-empires/evidence/usm-employment-options-offline.md/json。Hawaii原版naval_exit3147、旧作者及C4仍3001；全图旧海域ID缺失/重用由地图代理处理，需D3全新开局先重测供货。五阶段旧值未变≠当前GAME正确。旧战役价格/AI未修/饥饿的因果推断受海路故障干扰；容量与历史职业来源资料保留。Guji335→455因+35.82%全域土地外溢而暂拒，未生成经济A/B，人口/产业/法律/主MOD均未因此改动。## 214835 C4仍运行；C5到期回归候选已备份（历史）
root独占UI，当前run20261031T214835Z、candidate integrated-preview-20261031-c4、checksum052c、seed1519042830；最近实测1837May9 USM暂停。下文“当前无游戏”是较早历史。详见WORK/plans/two-empires/evidence/runtime-214835-root-observations.md，禁止重复launch或更改frozen。

C5=exports/integrated-preview-20261031-c5，精确C4 + PHI A5→A7，仅3生产脚本+身份；地图/历史/经济/E2全保留，Tiger新增0，独立备份。E/preview-c5-seed-saves.json以本run真实May1（到期前）、Gbuy、Jan1为基线，排除May7失败清理档。由root结束当前run后另行冻结/冷启；本条不表示C5已实际通过。

计划37继续就业可恢复性候选（尚未合入）：九州/粤东/古吉拉特有初始容量缺口；作者原有债役法、Jan1无奴隶、历史pop_type没有误迁slaves。阿夷洲实机0%market access，缺失naval_exit显示，港口满员但clipper买6卖0/本地105市场57；这是先查海运链的证据，不应先造工业。人口、制度、军事与日本边界均不因试算而改动。主MOD未合。


## 211226 已退出；C4/D2与精确回归基线（最新）

当前无游戏运行。run211226/exec8615正常exit0，frozen unchanged=true；旧8324818/gameplayL不用。读 `WORK/plans/two-empires/evidence/runtime-211226-root-observations.md` 最新顶部。现金A真实签约/原生8700与双边条约ID已证；正常360日收尾未通过（finish_reason0/native_amendment异常），精确时序待dailyprobe，不许当已完成。

C4=`exports/integrated-preview-20261031-c4`保原地图，E2真实safe getters＋PHI A5；D2=`exports/integrated-fujian-20261031-d2`含福建，只能新局。两者均已备份/静态审查，尚未新冷启，A5/E2 preview未验。`E/preview-c4-seed-saves.json`含211226 profile的Jan1/Gbuy/Gwounded/真实A_signed四档SHA；没复制archives。新probe manifest在runtime/batch-probe-integrated-preview-c4，2TXT与原冻结完全相同。map活动QA dailyprobe未完成，**禁止据本条自动launch**，等其完成后由root安排。

211226正常退出后两谓词collector为18个完整PASS周期（usm_init/usm_pressure_range），仅此两项；E/batch-probe-runtime-211226-final.json。别扩判全链。hidden_effect只隐藏展示、仍可能求值的实机反证已写validation.md；E1包装并非安全证明，须E2＋实际回归。主MOD未合。


## 202721 已退出；政治预览E1候选就绪（最新）

run202721已正常退出exec2678 exit0，旧window3475144/gameplayK不可继续操作；collector58567也已600.0秒exit0，98扫描、Jun–Dec七档齐全。最新完整断点仍见 `WORK/plans/two-empires/evidence/runtime-202721-root-observations.md`。下方运行中说法是历史记录。

独立 `exports/politics-preview-20261031-e1` 精确父integrated-politics-phi-C2，六政治脚本只hidden执行事务，四loc补既有±15关系提示及重复键一致性，meta身份，共11files。去hidden后有序AST全等、独立505文件SHA/27保护文件复核、Tiger相对父新增0；PHI/人物/首都映射不动。已备份candidate-politics-preview-e1-20261031T210836Z。详见E/politics-preview-e1-review.md，可供根与PHI A4同批精确差分合并；尚未实机验政治preview/click，未声称修复Interface断言。主MOD仍未合。


## 202721 自然走时后续（优先当前状态）

root已重载Gbuy、USM玩家speed5自然May12→Dec13暂停，无护卫/国家/预算选择。Jun–Dec七月自动档均归档：续费锁150日先消退，Nov1警卫剩7天，Dec1警卫/费用缓存消退；陈3148活且未伤、无Hao/结案，原危机JE仍active。详见 `WORK/plans/two-empires/evidence/chen-natural-202721-audit/README.md` 和已更新 `runtime-202721-root-observations.md`。不将低于案件门槛的此次走时写成随机概率测试，不把总预算或authority变动单归因guard。

PHI菜单预览none洪流已关闭交map修A3；root未申请条约，随后自然AI两张岁费审核未点。自然新增一条Interface/HiddenAllowed断言仍待排因，E/runtime-202721-natural-assert已归档。勿按下文旧“准备申请”直接操作未修菜单。collector58567有界600秒仍在运行（此条写入时），先查结束状态勿重复启动。主MOD仍未合。


## 202721 实际护陈回归与当前断点（最新，覆盖下文旧状态）

短续接记录：`WORK/plans/two-empires/evidence/runtime-202721-root-observations.md`；先读此文件。run20261031T202721Z/exec2678/window3475144/gameplayK仍运行，checksum3f01，root独占UI；候选integrated-politics-phi-C2共505文件，保留CNE L2、不含福建。不要重复launch，主MOD尚未合。

同G0实机正式陈案预览/悬停不再刷缺失modifier，error141稳定；实际Gclear撤卫钱差0；实际Gbuy居所警卫扣24k、180天/续费锁150天、全6744人物记录不变；明确压力25+指定负伤夹具的Gwounded中陈3148加wounded/压力35/警卫清除/结案flag/Hao无。详见上述记录与native JSON；不写成自然概率、自然到期或全部生命周期已通过。

根刚菜单reload Gbuy，准备USM玩家经PHI QA完整生产请求A现金8700→正式审核；尚未实际签约/付款/转船。subject_and_bloc_actions实际NO阻原生减贡；ep2_content NO仅证原生舰船条约门槛，不能推定通用set_ship_owner_multiple禁用，map代理正在边界审查。保留A2和真实guard，不伪造DLC，不force无proposal上下文的确认事件。额度重置已成功、不再使用。


## 20:27 UTC 最新运行（覆盖20:18条目）

run201812仅冷加载，主菜单提示未发现存档：root启动后复制的2存档未进入启动时扫描目录列表，**没有加载G0/没有验证G2预览**。已正常退出，exec2571 exit0，gameplayJ/21432508关闭。不要把冷启140条写成G2回归通过。

runtime.py已备份后加可选第五参数save_manifest，在Popen之前读取明确copies/source/sha256、验证WORK/profiles下.v3、exclusive创建并复核SHA。新run20261031T202721Z，exec2678，仍同候选integrated-politics-phi-C2(505files)、同QA，monthly，prelaunch_seed_saves记录在run.json；这次Jan1/G0启动前已复制，尚待UI验证载入列表。新窗口尚未枚举。首先load G0→正式陈案停留不刷error→真实分支。

明玩家实际转国操作已有精确清单E/ming-player-transfer-run201812-operations.md：USM真按钮选明/host，生产dispatcher flavorUSM.4，D0 tag目标→+7天真点.1拒绝→当日tag回USM→另存；可调用生产usm_civilwar.2只跳3月等待但仍实际make_independent/createDP/王室移属/play_as，另自然排程3月/180天对照。没有改活动QA增加此快捷项。

## 20:18 UTC 最新正在加载

run20261031T201812Z，exec2571；candidate integrated-politics-phi-20261031-c2，505files，精确base集成B1+政治C2+ChenG2+PHIA2，**地图与上run字节不变含L2，不含福建**。候选备份candidate-integrated-politics-phi-c2-20261031T201600Z。Tiger新增仅2个other-role旧schema误报，原版unique角色typeother支持，无未解释新增项；角色行为仍待引擎。

新profile runtime/profiles/20261031T201812Z/save games已复制上run Jan1和May12_G0，SHA完全相同；G0有AI常卫+情报。先实际菜单加载G0、打开同Chen.1停留/悬停验不刷error，再案卷真实撤卫/购办/过期及三结果各读档；随后Jan1用PHI诊断和生产协议。新窗口尚未枚举，禁止复用gameplayI/1377966。

QA已加入两详细只读按钮x855,445 rootUSM与x1060,445 rootPHI（event nesnd_phi_permission_context.2/.3），copy诊断B两events。原PHI QA菜单另加实际条件式现金A/B申请，不写资金/盟书/船数，只调用生产请求。native feature NO才能现金B3700，原贡赋不变；真实双方确认/唯一ID/同tick callback/20原船转属/unbound硬锁必须测。probe新manifest runtime/batch-probe-integrated-politics-phi-c2；2TXT与挂载active内容相同。

## 20:10 UTC 运行结束与下一候选（最新）

run192545已正常退出，exec89432 exit0、frozen unchanged=true；窗口1377966/gameplayI CLOSED。collector32250正常600s结束、四日期齐全；batch-probe-runtime-192545-final两个谓词真实PASS。不要再操作旧窗口或停止这些session。

下一无地图候选应以integrated-politics-phi-B1为base，合 south-politics-B1→court-reconciliation-C2（已冻结23文件）、ChenG1→G2（已冻结13处remove_modifier存在性守卫；raw日期仍已知格式缺口）、PHI A1→A2（正在proposal序号最后审查，暂不可用工作版）。还要copy详细PHI权限diagnostic B到新QA、加可见入口；旧QA保留。不含福建的新合并可复制Jan1和May12_G0到新profile，先加载G0验陈案预览，再新Jan1测PHI许可/合同；不可用G0当首次无保护基线。

福建另有court-fujian-compatibility-A工作候选：C2+fujianB差分，795首都映射/51州白名单已补、其它政治AST不变，待独立复核冻结，必须新局。后续主合并可取C2→该候选的地图delta；别丢CNE L2四arable调整。

## 19:54 UTC 首要恢复入口（优先于下文旧记录）

新完整根记录 `WORK/plans/two-empires/evidence/runtime-192545-root-observations.md`。run192545仍运行、May12暂停USM，exec89432/window1377966/gameplayI，勿重复启动。Jan1与May12_G0原生手动存档已保留，Feb/Mar/Apr/May1自动存档已稳定归档，monthly自动保存真实通过。CNE L2四月实测审计已完成见cne-l2-native-assessment.md；全局A2纵排/双widget显示、Apr1B公式精确核算通过。PHI钱款/船转仍没有执行，payments_possible NO待原生许可诊断。CNE旁观者误有4站队按钮交C2修。

**新的真实严重问题**：May12打开正式nesnd_chen.1就开始预览remove_modifier absent刷error（141→179→44263），legacy court_protection与residence_guard不存在却直接移除；root已选择“仍照旧章办理”关面板停止预览，未撤卫未购买。names代理独立ChenG2修guard及raw日期显示；当前G0其实已有AI常卫+情报，非空白。其期限/国库/人物ID已在chen-native-192545-May12-G0.json固定，下一冷启可直接加载G0做UI负例回归；新地图历史仍须新局。

用户明确授权一张额度重置已兑换成功：outcome reset，周剩余100%，卡剩0；幂等key6f4072d4-ae60-4c23-8b3d-dbe597036f11不可再次调用。继续原任务，不需询问重置。

map代理完成福建candidate fujian-split-20261031-b/31省色9群体15产业及14陆路，新state3172；15州transport静态通过与负例证据，未实机。其正定位PHI权限；succession代理独立court-reconciliation-C2 working未冻结（AI王室、降压/僵局出口、观察国UI）；三者都不得改当前冻结run。

## 19:26 UTC 最新运行覆盖下文旧状态

run20261031T192545Z已启动，exec89432，窗口1377966/gameplayI；candidate integrated-politics-phi-20261031-b1（494文件），冻结exports/runtime-20261031T192545Z/mod，profile runtime/profiles/20261031T192545Z。截至加载画面，还未进入新局。合并链：integrated-court-security-A + C1→south-politics-B + B→B1 + hus-pm-format→PHI A1。B1额外和平pressure<60、破产恢复期排除、明和平实际纸/工具/轻武器供应；PHI A1未绑定条约异常硬锁。B1的政变后高压无反对无DP死路和AI王室迁徙仍在独立C2处理，不包含本run。

Tiger相对court-A新增两项有源证据：total_crew_needed（本机event_targets.log1390明确支持）与multiple widget（原版00_meiji_restoration10/16）。其余新增0，不把这等同实机通过。完整候选备份candidate-integrated-politics-phi-b1-20261031T192700Z与frozen SHA相等。QA非空事件顶层namespace/id检查通过（nesnd_qa_land.txt只有废弃注释允许空）；PHI QA原匿名花括号错误已在freeze前修好。活动QA新增PHI菜单x650,445，Chen x1180,405；旧入口保留。原probe两TXT内容未变，与本run专属manifest runtime/batch-probe-integrated-politics-phi-b1一致。

monthly autosave隔离设置本轮实验，仍需UI+实际跨月文件确认。root仅UI；names代理只读cold日志/原生存档，map代理独立福建候选，succession代理独立C2。勿改冻结副本、勿重复launch。

## 原任务与最新范围

完整scope仍有效，主MOD未合入。WORK/plans/two-empires/00-master-plan.md、12-scope-ledger.md保原始范围，28-current-redesign-contract.md是最新九项要求。29北朝简单政治经济、30明吴四立场/加权图/和平与转国、31全域地图复审、32名字与测试、33福建具体提案、34护陈、35北朝容量L2；36-phi-imperial-service-and-autonomy.md已交付候选，正在独立审查。福建提案开始独立导出实现，未改主MOD。

C盘清理已完成：7,597,320,019 bytes约7.60GB/7.08GiB，剩余约39.74GB/37.01GiB。浏览器/凭据/聊天DB/作者资料不动。报告WORK/reports/disk-cleanup/result.md。技能已独立备份并更正均分适用范围、增量编辑、概念/测试/地图方法。catalog 1.13.11/build24799966 CURRENT changed0。

## 最新真实运行：已正常退出

run20261031T180905Z，integrated-succession-20261031-a，450files，checksum5066 seed2699654634；EACR→frozen MOD→frozen QA（含batch probe）。exec66802已正常结束，snapshot-integrity unchanged=true。原窗口657016/gameplayH已退出，不再调用旧窗口。新启动应枚举新窗口。

assistant真实新局USM：Jan1暂停基线→自然Feb5→四国立场same-tick QA→USM自然Mar11保存并正常退出。profile save games中：大明联邦_1836_01_01.v3(99059454)、大明联邦_1836_02_05_four_stances.v3(110588532)、大明联邦_1836_03_11.v3(114984084)。不要把四立场样本当未经政治选择的完整默认路线。

### 实际通过的范围

- globalJE正常自然激活，原生JE79、Jan13加入、45唯一国家、无dead。USM/HNA/SIH/PHI分别实际选拥明/拥吴/中立/自主；各自cooldown180ticks，global明1吴1/45，bar2.22222%，不是每国独立假globalJE。各国切换时同一表可见。
- A1真实显示发现国家卡横向溢出、按钮safe-value raw缺loc；A2修补已静态通过，尚未实机。
- 随机名B真实新局213角色/25个新键全部出现，Ma Ma=0，21个作者模板名保持；UI只核小市民领袖3029显示“领袖 马 耀祖”，魏景和仅native未UI。
- CNE新bar链接“内阁与失序”可实际点击，条件/±0.25/概念正确显示；破产链接真实展开原版帮助。政治月度四种条件尚未全部实测。concept-clarity显示把破产惩罚期与债务违约分开。
- 真实原生batch probe：两完整SKIP周期，随后18:27:29完整PASS usm_init/usm_pressure_range。正常退出flush后collector结合debug.3/.2/.1/log、指纹与run绑定 engine_verified=true，**仅两谓词**。不能称事件链/AI/经济全通过。
- 原生help已取conquerall/add_war_support/scripted_tests/event/testevent/escalate等，未执行占领/改战争支持。scripted_tests没有已证安全输出重定向。
- error119启动/进入→121自然推进，新增2条原版Peru/Bolivia重复参与；hover/四立场无unset洪流，旧海港加载错误无。Cold仍有本体/依赖与loc-only unused等分类，不称全日志0。

证据：evidence/runtime-180905-root-observations.md、succession-controller-runtime-180905.md/json、chinese-given-names-native-180905.json、batch-probe-runtime-180905-final.json、native-help-runtime-180905.json。完整logs在reports/runtime/20261031T180905Z。

## 当前候选与下一合并

当前实测integrated-succession-A父succession-controller-A1，合姓名B（父usm-journal-ui-A）、CNE政治合作B和concept-clarity-A（父hus-pm-format-A）。hus-pm-format-A包括前次地图/海港/引用闭包、4 HUS宗教PM声明修正与format-only。

下一需合（都未游戏验收）：
- succession-controller-20261031-a2，精确父A1，5文件UI/tooltip窄改，无玩法变动。
- ming-court-transfer-20261031-c1，父C，C父A1：.4隐藏调度→原文.400，真实王室/继承人保存、DP成立后合格独立HNA/SIH移跸+只原USM玩家play_as、无host安全出口、停战后复国；封旧无人反对即settled；C1补可点无效guard。
- chen-security-20261031-g1（G1父F，F父hus-pm-format-A）：6月两档警卫/真实费用/情报/案件随机三结果、shared prepare与生命周期。G1只改F的文案，游戏脚本SHA相同；最终合G1。活动QA已加入可见护陈菜单，现已退出run未挂载。不得把过时F当最终文字。
- cne-capacity-l2-20261031-a，父hus-pm-format-A：只四arable scalar+meta，晋中262→297、燕京197→213、河间300→310、漠南102→122。人口建筑军队SHA不变。根选择不提前迁东北人口，残留29.28万无岗仅容量减法，燕京基建与漠南接受度另需测。新局验收，不能用旧存档。
- B加权政治/真实双方盟书/12月严格和平/吴地域白名单整合仍由succession_design实现中；父C1，不可将A当前表态百分比称最终准备加权系统。

合并工具WORK/tools/combine_candidate_patches.py支持explicit metadata_identity{name,id,short_description}，只消候选名称冲突，其他metadata改动拒绝；保具体父版三方差分，禁止覆盖现冻结。候选根直接含common/.metadata，通常没有/mod子目录。

## 当前经济与地图后续

31复审162州：闽浙优先地理设计，粤东/昆士兰有条件，不一律拆半。33福建提案南15格留旧key/海军军需、北16格木纸/新港，精确省色/hub/9群体/行业表与河流heightmap图均有；未导出地图。旧七新州曾同ratio初分多资产，仍需逐行业核。吉林内陆8渔业cap原版也继承，不能为了清零任意迁资源；热河naval admin真实有效，非非法建筑。

map_transport_preflight.py已实际检出旧F三缺harbor负例，当前13州通过；不等于NavMesh/战争/实航。前run165620最后Jun4只视觉驻华南，抵海南native存档从未保存，不许补证。

SIH/PHI实测在evidence/sih-phi-fiscal-recovery-audit.md及5原生JSON：SIH32官署满员/纸价正常/机构未升，−316政力但固定财政正，旧AI32→39官署有实际恢复行动。PHI Feb5军费10.30k>全部收入7.52k、向USM贡赋1.64k，AI42→12常备/15k→1k水手并借债才恢复。40舰不等于满配海军。原版7营+作者35营叠加待设定取舍，不能随意删军。代理正在做真实中央军费分摊/自治减义务路线36。

## 继续顺序

已经合并A2/C1/G1/L2为integrated-court-security-20261031-a（465文件、31差异），尚未启动；Tiger新增0、781人口基准约束通过。B准备完成后按父C1差分合，PHI须独立复核后再决定。每轮冷启测试一组，复用same-version shadercache，仅日志/名字小改不重测整年。首先新globalUI纵列与提示、有限护陈、玩家转国/人物安全，再CNE L2周/月/季与AI对照；王室/战争/白和/复国/两条和平/日本/海外履约/编辑器导出和最终主MOD备份仍欠。不要把候选和部分实机改写为全任务已完成。

runtime.py新增可选第4参数monthly，只写隔离profile的game.autosave；未证引擎采用，需实际设置UI+跨月新autosave。tools/capture_autosaves.py只读稳定存档双SHA后归档，11项fixture通过，未冒充原生自动存档验证。没有已证save控制台命令，不再试虚构save。
