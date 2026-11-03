# 工具和真实引擎验证

当前优先：[日志优先的增量交付](log-first-delivery.md)。2026-11-01用户已取消重复进港/读档/截图验收，要求修日志错误、外部检查优先、正式包排除QA，并授权修复后直接整合。以下历史流程仅按受改范围选用。

验收先对照当前用户认可的结果。2026-11-01已接受玩家失国/GAME OVER（含日本）；实际失败画面如实留证，不再单凭它判定BUG或要求救援。世界机制可在明确记录的观察者继续过程中核验，不能改写为玩家自动续玩。当前重点是既定事件链的顺序、可达条件、完成结果及难度/行动空间证据；具体范围见[当前任务索引](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/.scratch/debug-release/map.md>)。

## 可失败的边界检查（2026-11-03）

测试计数不代表覆盖率。判断条件测试要保留操作符、数值、作用域祖先与执行顺序；只查“army_size和1存在”会让<1被误改成>1仍通过。新增门槛至少有开局、差一档、刚好满足、对象转属/消失和已完成重入案例；对旧源码跑红，再对阈值、比较符、缺守卫作内存变异，确认检查真的失败。

需用外部AST子集执行时，记录支持的语义，未知节点必须报错；布尔兄弟项不能假设短路，trigger_if按分支处理。全局启动没有root，测试不能一律注入当前country来掩盖调用上下文。API结果注入只能证明脚本控制流，不能代替实际建国、转地、战争或人口引擎。

报告绑定最终文件SHA；测试后编辑了条件或本地化，按变化重跑或保存可核的AST等价链。地区门槛按state_region去重，直辖与直接/间接属国区别、共享分州、占领不等于所有权均列入案例。原生largest-state算法未证实就作为明确fixture输入，不能用province数量假装引擎语义。

实际反例与证据：WORK/reports/commission-boundaries-20261103/boundary-audit.md、boundary-cases.json、effect-boundaries.json、request-boundaries.json。测试仍为STATIC_PASS，未运行游戏。

## hidden_effect 的真实边界（1.13.11，run211226反证）

`hidden_effect` 的引擎文档仅承诺不显示内部效果；不能把它当作“预览不求值”或“先写后读必定完成”的保证。run211226/C3 的PHI菜单已包hidden，root仍实际观察到新serial未定义被save_scope_value_as读取，error由143增至9871后关闭。E1政治隐藏包装同样不能独立证明安全。错误根因与修复候选见 WORK/plans/two-empires/evidence/politics-preview-e2-review.md；此反证不等于所有hidden都会报错。

预览引用链中的数值必须独立可读：按真实has_variable/has_global_variable条件取现值，缺项用明确定义的只读fallback；除法另验证有效正分母。国、州、人物、条约等typed对象用exists或可选scope保护，不能用数字0、新建对象或伪造DLC补缺。实际执行已初始化的路径应保持原值、时序与作用域，列逆变换/数值等价证据；本地检查后仍重测未初始化菜单预览、持续悬停和真实点击。show_as_tooltip/hidden_effect/自定义说明只解决展示，不代替这些检查。


2026-10-31新增实证：run192545隔离profile的`game.autosave="monthly"`在原生设置显示“每月”，真实跨月产生Feb/Mar/Apr/May1四份存档，`WORK/tools/capture_autosaves.py`稳定双SHA归档成功。它是采集工具，不修改世界或代替游戏；保存成功和经济正确分别判定。相同run的两条只读monthly probe完整PASS，只覆盖初始化/压力范围，不认证整个事件网。

UI预览必须作为独立门禁：run192545冷加载正常，但正式陈案的未选选项在预览时对不存在的修正执行`remove_modifier`检查，累计48,189条错误。所有可能移除的修正先用同scope `if={limit={has_modifier=...} remove_modifier=...}`，包括旧档兼容与互斥档位。扫描旧代码能检出遗漏不等于新代码实机通过；须冷载修复并打开同G0案卷、悬停/停留，再实际执行清理。发现每帧重复报错先关闭对应案卷并归档轮转，勿让错误刷屏同时继续无关操作。

静态审查需覆盖真正的引用链。2026-10-31 `audit.py`补充建筑→PM组→PM、人口history文件名与内部国家scope的待审差异；用已知错误候选回测找到6个不存在PM与2个错误组别。文件名差异只列待审，不能自动改国家。地图守恒同时统计普通建筑所有权`levels`与纪念建筑`level`；不能用与转换代码相同的遗漏定义自证守恒。

## 已查到的项目（2026-10-30）

- [paradox-script-mcp](https://github.com/106-/paradox-script-mcp)：支持 `game_type = vic3` 的只读脚本探索；可按符号/路径查块与引用。作者明确自定义 parser 不覆盖全部 Paradox 语法。不能声称其能启动引擎或证明 scope 正确。
- [Tiger](https://github.com/amtep/tiger)：`vic3-tiger` 可结合本体与 MOD 检查引用、scope、本地化等；当前下载发行版 1.19.0，规则可能落后于 1.13.11，需要原版对照和真实日志去分辨误报。
- [CWTools Victoria 3 rules](https://github.com/cwtools/cwtools-vic3-config)：IDE补全/静态规则补充，不是引擎真值。
- [Paradox Toolkit CLI](https://github.com/JDeffner/paradox-toolkit-cli)：另一个带本地 MCP/语言服务/Tiger 的工具；本任务优先使用已实际运行验证的工具，不因 README 声称支持就标为已部署。
- [官方维基 Modding](https://vic3.paradoxwikis.com/Modding)：本次网页访问 401，不能声称已读；遇到可访问页面仍核对版本。

插件目录搜索 Victoria 3/Paradox 未返回可安装集成；这不表示 GitHub 无 MCP。工具源码与虚拟环境放 WORK/tools，不能放游戏或工坊目录。安装与实际 MCP 调用记录放 WORK/reports，最终以记录为准。

## MCP 使用

服务器：`WORK/tools/mcp-venv/Scripts/paradox-script-mcp.exe`（stdio）。从协议 `tools/list` 获取当前参数 schema，勿把别的客户端 `.mcp.json` 直接抄入 Codex 配置。

本地源码基于 commit `e6aff2c35d29d89ec1810ff8f6490d84a2c66ced`。已发现并修补公开 `init_game` 未传递 `game_type`、默认走 HOI4 的问题：本地入口 `init_game(game_directory, game_type="vic3")` 传给 `GameContext.initialize`。另将 MCP SDK 固定为 `mcp>=1,<2`，因为上游旧 FastMCP API 在 2.x 已移除。不能裸装最新版依赖后声称可运行。

实际协议验证已通过，证据 `WORK/reports/mcp-smoke.json`：initialize→tools/list→从本机读 `upper_class`、`STATE_GUANGDONG`→切换MOD读 `flavorUSM.1` 与 `ce_polish_reconquest_energy_bar`。重跑命令：`WORK/tools/mcp-venv/Scripts/python.exe -X utf8 <技能目录>/scripts/mcp_smoke.py`。

先 `init_game` 选 GAME 与 `vic3`，再 `list_symbols`、`get_structure`、`search_references`；参数以运行时 schema 为准。服务器每个会话的根目录与缓存可能不同，切换到 MOD 后不能当成已自动叠加本体。返回结构可能聚合重复项，绝不能用返回的普通对象反写原文件。复杂/不可解析块退回 `rg` 与直接读源文件。

## 分层验收，全部对应实际文件/真实场景

多文件debug先采用 [批次循环](incremental-editing.md)：代码闭包完成并整合后统一离线检查，最后集中引擎验证。统一入口为 `WORK/tools/global_validation_runner.py --candidate <实际MOD根> --baseline <明确父候选>`，具体选项见 [WORK/validation/README.md](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/validation/README.md>)。默认只读，不启动游戏、不改候选、不重建人口基准；输出唯一目录中的 fingerprint/progress/summary 与逐项证据。

入口复用有序parser、生产/历史/资源、固定人口、影响图、字面内容/本地化、全局海域/交通、Tiger和实际stdio MCP查询。`PASS`限该项覆盖范围；流程完成但存在缺陷是`FAIL`，缺工具/未执行原生场景是`NOT_RUN`。传入 `--runtime-run` 与 `--engine-collector` 时核实际候选/挂载probe/日志身份，旧版本PASS不能移用。界面、动态scope、市场就业、AI、战争和航行依然由引擎验证；原生存档中的计数器也不能冒充运行时百分比。

不要用清空告警、更新baseline到失败候选或泛化忽略类取得全绿。先查诊断的文件职责及当前本体同形实现：有的内部modifier模板没有公开标题，有的动态本地化/GUI读取不计入脚本变量使用，不能因此批量补无依据文案或删状态。相反，原作者也有的地块重叠或断链同样须核验；“继承旧值”不证明兼容新版本。

1. 语法/资源：解析活动文件，保留重复键；本地化 BOM/header；地图集合与引用；Tiger 对当前本体+依赖+MOD运行。保存原始报告，不能把全局忽略当修复。
2. 加载：先归档旧日志，使用 `WORK/editor/runtime.py` 冻结 MOD/QA 副本并创建独立 `-userdir`；本机实测关闭监视的参数是 **`-nofilewatcher`**，旧参数 `-no_filewatcher` 无效。严禁挂载正在编辑的工作树后，把重载中的半成品报错当成固定版本结论。记录 run.json 的加载组合、启动参数和 SHA，退出后验证冻结副本未变。原版、依赖、完整 MOD 分别对照。
3. 新开局：USM/CNE及受改国家，检查领土、人口文化/宗教/数量、建筑等级/PM/所有权、首都、角色服装/外貌。地图编辑器的候选导出同样必须新开局验证。
4. 行为：真实游戏控制台查看 `help`，用当前可用命令导出 `script_docs`、触发指定事件，逐分支检查变量/JE/进度条；自然跑日/月脉冲确认不重复、不丢触发；另存测试存档再读档。
5. 日志：比较本次启动以来 error.log 的新增项，分为本 MOD、依赖、原版基线；时间戳/版本/加载组合/游戏日期与截图或存档形成证据链。空旧日志不是通过。

GAME `tools/scripted_tests/scripted_tests.md` 说明了真实引擎 `scripted_tests`，测试会逐日执行 success/fail，并可输出结果；它还说明 XML 可能写入 binaries。用户禁止修改本体，因此未经核实重定向输出前，不启用会往本体写文件的测试模式。改用控制台 effect/assert式日志（以当前命令帮助为准）、实际运行与 USERDATA 中的存档/日志证据。禁止自行在 binaries 写测试资产。

若没有 UI/游戏启动能力、授权或引擎崩溃，应保留具体失败日志和复现步骤；不能用 Python 单元测试代替“游戏里正确”，也不能把未完成标为完成。

## 更新时

本机 launcher版本+Steam build+受影响文件 hash 是目标；同版本改文件也刷新索引。运行 `catalog.py refresh` 后，对变化目录重读文档与实现，重新导出函数库。之前的运行结论只适用于记录中的版本和文件哈希。
# 2026-10-31 真实开局控制的纠正

`WORK/editor/runtime.py` 是启动/加载配置恢复/日志归档器，不是完整自动测试驱动。启动进程不算开局；必须观察主菜单→新游戏→沙盒→选国→国家卡→开始→国家 HUD 与日期→暂停，才能执行国家作用域事件。每步记录 assistant、user 或混合操作者。2026-10-31 第二次运行已由 assistant 完成上述开局到 CNE 1836.1.1；随后用户明确选择自己操作，后续由用户控制、assistant 读图和分析。上一次运行选国/推进有用户帮助，不得改写记录。

`paradox-script-mcp` 已完成真实 stdio 查询试验，但它是语法/资料查询服务，没有驱动 Victoria 3 进程的能力。Windows computer-use 的 sky MCP 能观察/操作游戏；游戏控制台和 `ExecuteConsoleCommand` 才调用引擎命令。分别报告能力。此前 QA Script docs 按钮已导出文件；QA Save 按钮点击后未出现预期存档，保存命令未核验，不能把按钮名称当证据。grave 快捷键也未打开控制台；遇到用户输入后先重读状态，不盲目连按。

真实测试状态机：未运行→加载→主菜单→模式选择→国家选择→国家局面→暂停且 tag/date 正确→独立基线存档→触发指定场景→推进指定周期→断言与面板/存档核验→另存结果→日志归档。每个状态必须有可观察的入口条件；失败停在实际位置，不执行依赖后继状态的命令。用户操作时不抢窗口；给出下一项具体动作，再读取结果。

文本调试存档可读取：`WORK/tools/save_economy.py <save.v3>` 保留原始副本/SHA、日期、多国预算数组和 balance_trend；`save_structure.py` 按国家汇总职业人口、物理位置上的建筑等级/实际 staffing/商品成本/政府分红及 PM。staffing 是已配员等级等价值，不是员工人数；建筑所在地不等于所有者。只支持核验过的 SAV 文本格式。

2026-10-31 实测：1 月 1 日序列化预算缓存未包含全部即时重算，不能用数组总和替代 UI；1 月 15 日周缓存和当日预算也有差异。须对照实际预算面板、税制、固定/临时收支、投资池划转与周结算，保留差值，不能强制改公式使其“对上”。

失败记录：`gui.CreateDockable gui/console.gui console_window` 创建的窗口没有 ConsoleWindow 数据上下文，会大量报 FetchData 错误，已从 QA 移除，禁止复用。`save qa_snapshot` 未保存成功，也已移除。原生暂停菜单保存到独立用户目录已成功。键盘 grave 在此环境没有生效；不要反复试相同按键或调用系统屏幕键盘。鼠标坐标上的 `sky.scroll` 取 0/0 已实测可触发悬停；右上角运行/暂停可点击，并以实际日期变化复核。

## 玩家辅助 AI 与观察者的实测区别（1.13.11，2026-10-31）

`enable_ai self` 和 `observe` 不能互相替代。run `20261031T131239Z` 的 CNE 在玩家模式启用前者后，从1836-02-20推进到03-03，主控观察到军队210→283、政府建设35/57→57/57及公司等自动行动，但QA界面仍是 `Country.IsAI=NO / IsPlayer=YES`。随后执行 `observe`，QA显示 `NO COUNTRY / OBSERVER`；河南国家debug tooltip显示CNE `IsPlayer=否 / IsLocalPlayer=否 / IsAI=是`。需要测试AI身份限定分支时，先进入观察者并核对目标国身份，不能仅用自动建设证明 `is_ai=yes`。

以上是主控真实UI与行动证据；尚未运行同国 `if={limit={is_ai=yes} debug_log=...}` 的脚本探针，不把GUI同名接口伪装成trigger求值记录。完整证据/存档/待测项见 `WORK/plans/two-empires/evidence/ai-control-commands.md` 第6节。按需保存玩家、辅助AI、观察者三种独立样本；按实际状态和命令回显判成功。此run退出flush后已确认两次 enable_ai self 均执行，observe进入与第二次observe退出、disable_ai self均有成功响应。观察期间tag HNA/QE1/HUS虽回显Now Playing，UI仍是观察者；不能以tag回显判定离开观察模式。observe是切换，应先看当前状态再操作。debug.log有缓冲，运行中缺命令行不等于未执行。

## 隔离运行的缓存与采样

`runtime.py <candidate> mod <previous-isolated-profile>` 可选第四个命令行参数用于复用同版本先前隔离profile的引擎shadercache。只复制着色器缓存，不复制存档、日志、settings或地图缓存；来源必须在WORK/runtime/profiles内，并在run.json记录。run060444实际使用并仍完成新局初始化。这只节省图形编译时间，不复用脚本验收结论；更换游戏/显卡/依赖版本时不假定缓存仍适用。

本机速度V在文档处理的一分钟内可能推进数月。需要固定周/月采样时使用较低速度并频繁观察日期；不得将错过的采样日补写成已测。高速自然事件可能超时自动选默认项，必须列出已观察选择和未知区间。滚轮有时穿透面板缩放地图，改拖可见scrollbar并观察实际列表；不要重复无效滚动。

若工具返回“physical Escape”而用户明确表示没有按键，将其记录为工具中断/误报；不据此指认用户操作，也不改写游戏证据。遵守当次工具停止要求，用户重新明确恢复后重新枚举和观察窗口。本次2026-10-31恢复可正常列窗并回到USM1836-01-01，前次中断原因未查明。


### 补充：真实脚本is_ai探针已完成（2026-10-31 15:34 UTC）

run150709 debug.log1156–1185补足上一节待测项：CNE玩家NO，enable_ai self后仍NO，observe后tag CNE再触发为YES，退出observe/disable_ai self恢复NO；HNA/HUS均YES。无国家观察者直接event产生无ROOT错误，因此先tag目标国再触发国家事件。原始日志及snapshot-integrity已归档，暂停中的身份测试不作为经济AI行为证据。此补充取代上一段“尚未运行脚本探针”的状态。

### 1.13.11 原生存档缓存与作用域诊断（2026-10-31）
暂停同一tick连续触发事件时，国家population_radicals/population_loyalists缓存可尚未刷新；按pop.loyalists_and_radicals实际字段汇总、同时留国家缓存与原始日期。不能据缓存没变断言effect无效，也不能把累计互斥选项测试当自然路线经济结果。实例WORK/plans/two-empires/evidence/cne-qa10-native-save-comparison.md。

Tiger警告的locations可包含“定义→调用→scope推断”整条链。修正前核准具体modifier名和实际落地scope；不要把邻近定义名误认成报错对象。实例CNE_crack_local_gangs附state却含country项，与CNE_local_industrial_broom不同。

原生存档database保留已销毁对象，JE记录中的active=yes不独立证明仍活跃。先排除dead.dead_objects及其death_date，再结合UI与活动国家列表；实例CNE暂停后原生JE39327仍有旧active字段，但1836.11.18已登记死亡，UI关闭。

事件顶层duration单位为月；trigger_event的days是投递延迟天数。实际duration=3显示约92天，duration=30显示约914天。不能按“三日过期”安排测试。保护/援助pending变量的days与事件窗口分别核验，过期选项必须说明失效原因。

JE immediate时country的has_journal_entry查询可能尚不包含新加入JE；数值初始化不能只藏在这一守卫内。按钮effect预览不执行前面的set_variable后再评估var比较。给生命周期入口明确初始化、比较缺值保护；以首次进入JE后立即悬停/点击回归，不能只测过月后的已初始化档。实例run162626首次契约预览117→10191错误，具体修复及复验状态见active-work。

### 批量原生探针，减少重复看屏幕

`WORK/tools/qa_batch_probe.py build --candidate <候选> --out <新probe目录>`生成独立QA事件/on_action和SHA清单；`collect --log <profile/logs/debug.log> --manifest <PROBE-MANIFEST.json> --run <run.json> --out <报告>`读取引擎输出并绑定加载指纹。脚本不会启动新局或模拟Clausewitz。实际进入国家后日/月脉冲可自动检查生产变量并记录PASS/FAIL/SKIP；无标记是NOT_RUN，缺失或截断不能算通过。当前仅两条USM变量初始化/范围谓词，扩充按实际新功能逐项加，不能称完整事件链已自动验收。

2026-10-31 run180905已实际加载并自然走时：日志激活前两周期SKIP，激活后的usm_init/usm_pressure_range完整PASS；正常退出flush后，run/candidate/挂载probe/轮转日志指纹绑定通过。证据WORK/plans/two-empires/evidence/batch-probe-runtime-180905-final.json，仅证明这两条真实谓词，不是整个事件链或经济验收。正式effect提取后由QA调用同一effect可覆盖结果分支；自然触发、AI概率、按钮可点性及UI仍单独验证。现有查询MCP/Tiger/CWTools不执行游戏，VSCode任务可组织流程但不提供已经证实的Vic3无界面解释器。

## 编辑器报红与源码闭包（CWTools 0.10.31实证）

遇到“自定义trigger is unexpected / CW262”，先查有效数据库定义、完整括号和实际调用，再以安装的语言服务器冷启动复核。仅看定义存在不能证明工具索引正常；仅看红线也不能认定游戏脚本无效。本轮CNE两个福利trigger在同文件250/253有定义，冷加载无对应诊断；独立全MOD反例删除这两定义后准确产生两个CW262。源码保持，编辑器可重载规则/窗口以刷新索引，不能删除有效判定迁就缓存。
LSP初始空诊断不是最终通过：等待规则重建及后续文件诊断，URI比较先统一百分号编码。引用检查要有已运行的缺定义反例。证据与可复用探测工具在 WORK/reports/integrity-recheck-20261102/cwtools-*.json、WORK/tools/probe_cwtools_integrity.py；它只启动语言服务器，缓存与反例在WORK，不改用户IDE配置、不启动游戏。
