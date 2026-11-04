# SUPERSEDED：军营alias误分类已撤回

此为初始报告历史副本；不要依据F01修复MOD。以batch-b2-validation.md/json当前版为准。

# B2 独立外部验收：红例总单

**FAIL_STOPPED_NEEDS_B2_REPAIR / ENGINE_NOT_RUN**。2026-11-04，实际父委派配置gpt-6.1-sol / medium。本轮是独立B2审查；没有测试自己实现的C2，没有改玩法或打开游戏。root要求在固定版本集中完成结构/引用扫描、MCP/Tiger及既有C1保持后统一停测，现已停止整个B2测试。

## 对象与依赖

B2原owned冻结：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-b2-owned-freeze-20261104T155305Z\mod`，36文件；初始910文件快照逐SHA核对。root随后要求补全A1实际依赖，依据R/batch-a-validation.json的真实路径`validation/runs/canon-a-20261104T131339Z/mod`提取24份精确SHA，再覆盖B2 owned，生成固定931文件快照`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-b2-a1deps-20261104T161200Z\mod`。原910快照和初轮输出保留。没有读取变化中的全C作测试对象。

B2 36份owned在所有外部工具完成后仍与原freeze SHA一致。A1/A2/NKH上下文缺定义没有计为B2 BUG；Tiger基线同样叠加这24份A1再作差分。证据与全部931文件SHA在报告目录。

## 确定问题与最小修复建议

### B2-F01 [P1] 真实军营ID拼错，独立自卫支路无法达标

位置：`common/script_values/nesnd_small_states.txt:12`；`common/scripted_triggers/nesnd_small_states.txt:109`；`common/scripted_triggers/nesnd_small_states.txt:111`；`common/scripted_triggers/nesnd_small_states.txt:112`。

GAME common/buildings/05_military.txt:3定义building_barrack；GAME与固定MOD的有效buildings数据库均无building_barracks。B2四处过滤器无法命中真实军营。

nesnd_small_barracks恒0，self_defence和区域双区军营分支被堵；原有真实联盟/防御协定替代仍可能成立，不宣称整个终局绝对不可达。

建议：只在B2 owned四处用当前实际ID building_barrack，并对自卫/区域双区营最小正例复测；不为拼写添加假数据库别名。

### B2-F02 [P1] 政治争议迟答与承诺成功分支不检查原期限

位置：`common/scripted_triggers/nesnd_small_politics.txt:12`；`common/scripted_effects/nesnd_small_politics.txt:76`；`common/scripted_effects/nesnd_small_politics.txt:91`；`events/nesnd_small_states.txt:36`。

真实ACE南洋owner-state、现有liberal运动、合法议题/相同regime/serial和episode_active；episode_clock已过期不存在。实际orderedAST仍返回episode_valid=true，organise可点，cancellation=false。承诺choice=2、clock不存在、目标法现已生效时，monthly先选line76成功支路，首effect写nesnd_small_reform_done，期限检查line91来不及执行。

过期提议可重新写12/24月clock，过期后才改变法律也可取得按期履约事实。事件duration=100的单位是月，不是100日；本轮没有证明实际自然运行的具体迟答间隙长度。

建议：未选择回复资格须要求原clock仍存在；承诺结算在成功条件前核原clock或令成功同时要求clock。按当前阶段处理已经选择后的12/24月，不能把所有有效在行项目误关。校对事件窗口的月单位。

### B2-F03 [P1] 自有市场30日核验到期后仍能发成功通知

位置：`common/scripted_effects/nesnd_small_diplomacy.txt:66`；`common/scripted_effects/nesnd_small_diplomacy.txt:68`；`common/scripted_effects/nesnd_small_diplomacy.txt:72`。

固定源码fixture：market_verifying仍在，30日market_verification已不存在，原partner/regime/overlord/pact事实仍有效，此时market.owner=self。实际market_verify先选line68并发nesnd_canon_diplomacy.2；line72过期分支不执行。

没有证明在期限内兑现的结果也会被作为本次成功；日事件serial守卫不能弥补helper内部顺序，月维护同样调用该helper。

建议：先处理截止失效，或成功条件显式要求原deadline仍存在；保留现实市场归属，不为通知失败撤销已实际发生的市场变更。

### B2-F04 [P2] 帝国line身份在非印度国土时漏过B2排除

位置：`common/scripted_triggers/nesnd_small_states.txt:15`；`common/scripted_triggers/nesnd_india_core.txt:3`。

实际ACE身份与region_indonesia人口州，加nesnd_india_imperial_line永久标记。实际nesnd_india_empire=false（它先要求nesnd_india_country/印度根基）；实际nesnd_small_state_country=true。

违反B2计划及root合同对imperial_line明确排除，帝国身份失去印度州后可重新落入小国路线；不要修改印度帝国helper的全局语义。

建议：在B2自己的排除中显式检查nesnd_india_imperial_line及受保护TAG，不只借带地域前提的nesnd_india_empire；以南洋土地/旧lineage/保护帝国身份正反例复核。

### B2-F05 [P2] 事件AI base引用动态script_value被当前验证器拒绝

位置：`events/nesnd_small_states.txt:69`；`common/script_values/nesnd_small_diplomacy.txt:2`。

实际Tiger错误dynamic script values are not allowed here，info为only literal numbers or the name of a simple script value；当前GAME事件语料660个ai_chance.base均为数字。

这是新的外部验证error，必须修复或以真实原生/引擎证据解释后才能静态交付；本轮不开游戏，不把工具诊断独立冒称已观察到的引擎报错。

建议：用已证事件ai_chance形状实现获批倾向并保留数值合同；不要仅忽略validation类或换baseline掩盖。

## 已完成而不扩大结论的检查

- 34份B2脚本保序解析、36份owned身份通过；有效数据库扫描只有上述四处军营类型字面引用缺失。Tiger未检出这四处，独立数据库检查仍确认不存在，不能只看一个工具的错误数。
- 本案186对中英命名键的BOM/header、无重复、集合一致及全部显式游戏文本引用通过；另有两处原生modifier描述键警告，未归作已通过。29个按钮visible/possible/effect的有序源码树已单独分解，不宣称实机条件勾叉或悬停通过。
- C1 repair4完整50组源码矩阵重跑通过：Egypt17、原PRU/AUS/USA与历史17、请求13、补边界3；另有13组不执行预览写入的闭包及首次零点用例。kind5现使用真实ACE/B2资格完整走原canon send/accept，取得FRA投资人、小国资本帮助与成功通知，无假helper。其余B2 kind5全边界仍随本轮停测，不用一个正例认证全路线。
- 共享接口独立有序AST差分与实现交接相符：12个canon trigger、send/maintenance、7个旧India trigger和7个旧按钮不变；旧accept/refuse执行体及clear原字段保留，共享事件字节一致。kind1/2/3/4/11的实际C1行为矩阵也保持。
- 实际stdio MCP initialize/tools-list、931快照init_game与13次get_structure均isError=false，含B2身份/月维护/市场核验/争议/AI值；MCP能读取结构不等于该AI值的事件调用语法通过。
- 实际Tiger同依赖基线差分新增14项，均定位B2：validation 1、encoding 1（聚合30份缺BOM脚本）、missing-localization 2、logic 7、brace-placement 3。没有新strict-scopes被全局忽略；旧C1退役JE缺键和opium属于基线，未借另一个正在编辑候选的修复称本快照已清零。

## 停止范围与能力边界

未继续跑73国完整身份地域/人口、YN1/BUR/SIA/HYD尺度与零分母、2m/150万滞后、失州重订、12+12累计/永久奖励、kind6–9全动态后验、运动三行动/革命继承、终局切换与全部暂时效果，以及B2专属无写入预览矩阵。这些是发现实质红例后按root要求停止，仍标NOT_RUN；没有STATIC_PASS或ENGINE_PASS。

最小反例实际解释冻结有序AST/宏调用；国家、州、既有运动、pact、市场owner和计时变量状态为明确native fixture，不手抄B2状态模型。过期检查缺失及分支顺序是源码反例，不声称本轮观察到真实游戏具体先后帧。未知语法停止；适配器初期命名冲突或缺market支持已记录为工具问题，不算MOD BUG。

证据目录：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\canon-route-execution-20261104\batch-b2-validation-a1deps-20261104T161200Z`。核心：b2-minimal-source-red-cases.json、b2-structural-scan.json、b2-interface-independent.json、b2-ui-source-decomposition.json、c1-full-regression-summary.json、mcp-c-owned.json、tiger-b2-delta.json及两份原始Tiger。

本轮技能维护无新永久规则修改。主MOD与所有冻结游戏源码只读；后续由root组织B2编辑修复→新冻结→完整回归。
