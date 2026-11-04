# B2 实施冻结与交接

2026-11-04。**READY_FOR_TEST / BEHAVIOR_NOT_RUN / ENGINE_NOT_RUN**。配置为父任务显式指定的 **gpt-6.1-sol / medium**；委派证据：`/root → /root/sol_b2_implementation` 的 NEW_TASK。最终架构、数值与合入权属于root，本代理只按GO实施。已停止玩法与本地化编辑，不自行审自己的B2，不启动游戏。

## 精确对象

- 编辑对象：`exports/canon-route-execution-20261104-a`（C）；主MOD只读。
- 冻结 owned：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-b2-owned-freeze-20261104T155305Z\mod`，**36文件**。SHA清单：`batch-b2-freeze.json`。
- 固定测试副本：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\batch-b2-20261104T155305Z\mod`，**910文件**；从C1 repair4已验证的固定依赖快照继承，再只覆盖36份B2 owned。它不夹带正在编辑的C2，也不代表整个当前C的验收。
- 编辑前备份：`backups/b2-preimplementation-20261104`。印度can_send原文基点取C1 repair4固定依赖中的原B1文件。没有回退共享repair4。
- GAME：1.13.11 / Steam build24799966；本轮catalog CURRENT，changed_count=0。引用源码SHA和真实行号在 `batch-b2-sources.json`。

## 已实施闭包

**身份与事实经营。** 印度复用真实43土邦触发器；南洋24邦+PHI/DEI/YN1/BUR/SIA/DAI共30入口。名单不能替代存活、集中政体及实际本区人口州。JOH注释旧土与旧POP没有被复活；无MYS补地。MUG/BHT/DRA/imperial_line、TZ1、YU1、IR1–6明确排除。印度后继须保留印度根基，南洋后继须保留本轮地区根基；远南专属Oceania分支不向其他大洋洲国家扩散。三国地理lineage随真实革命后继移交。

生产类型按GAME+C有效building_group父闭包读取得出，排除subsistence；只统计本国实际建筑、等级、75%就业、正利润、非补贴。自有市场意向及终局自有市场路径另核投入短缺。J是合格就业州人口覆盖，T是接入80%的州人口覆盖，未伪称全国失业率。没有商品库存、股票变量、赐送厂房、资产转移或history/pops改写。

**四层记录与地区目标。** 永久成果/领奖、当前规模身份、目标期次/具体owner-state、有效观察月分开。初次/旧档按完整当前资格进入；后续完整资格六个月升级；人口低于150万或少于两个人口州六个月转紧凑恢复。分类准入200万/至少2个人口州；地区及支点阈值由共用 `nesnd_small_region_numbers_valid` 核5%与10万人，不保留旧10%/两组合计50%门槛。

远南澳新、缅甸上下游、暹罗中部+人口较多的另一组采用实际拥有的指定本土地理组人口作分母；新增海外人口不稀释本土目标。暹罗分母包含中部、内陆和外围全部指定本土地理组，不只两组任务人口。其它国为最大人口州+其他直接州。支点及成员按实际state、country、期次登记，失地当月失效，不把外国owner-state计入。失去新西兰/Pegu等不默默改组；显式重订可改为当前国土通用两区，24个月间隔，新期次清当前地区观察与确认、永久奖励不重发。保留既有区域身份的150–200万人滞后区间可重订有效地区；规模准入仍须200万。缺原本地理联系的三国旧档也能显式选择通用地区，紧凑身份随后仍须完整资格六个月才升级，未绕过窗口。

专业路线严格要求每区一种type各至少2级，同类但两地type不同。稻2/麦2可；稻1茶1/稻2不可；单区4/另区0不可。另一条路线为全国两类合格产业各2级且每区至少1级。市场接入全国及两区75%覆盖、远南两区就业港口、两区真实行政与学校/大学均落到实际对象。经营12月后治理再12月，代码用互斥阶段分支，不能同月给两阶段各加1。唯一月写入者为本案on_action；JE无月度计数effect，旧新JE不能双脉冲。

**行动、政治与主权。** 公共投入按clamp(round(GDP×.0002),10,2000)冻结每周报价，连续12月，同项目不叠；费用与服务帮助分开修正并有原生预览。现有市场专业化12月资格+.10/权威−25，市场主人变化只撤该关系政策，不清事实经营月份。自有市场筹备不改变市场归属。基础完成奖励与36/60月期限、终局24/120月及60月奖励依批准值实施；永久rewarded防止成长、重订、革命后继重复领取。

地方困顿连续六个月且已有适格原生土地/劳动/自由或激进运动才开争议；按实际相关POP规模选议题，固定平局顺序保留。组织12月、具体法组承诺24月、镇压12月互斥；支持权重是原生movement modifier。按相关POP一次激进/效忠变化，无循环脉冲。人物仅选实际存活、在本国且支持该运动者，12月声望；关闭争议时按存活对象撤帮助，不生成虚构领袖。承诺通过原生立法兑现，不自动activate_law；土地、债役、劳动、种姓/代表分别存具体目标。完成法组的永久事实标记与当前承诺分开；制度改动撤旧承诺，不惩罚新政府。延迟事件核serial/政体/议题；原生革命决定起义、法律与主权，不把国内胜利当独立。

旧政府自主入口只查相关IG实际执政、合法性50、实际财政/地方能力/原生外交条件，无党派组合。区域终局可选择高度自主实际level2宗属或实际独立；主权分支变化清该终局观察，经济成果保留。法律、市场、防御及地区伙伴均是当前事实。伙伴可为本国属国，但不计附属POP/产业，也不新建虚构地区联盟。自卫读取真实军队、军营、就业/投入，区域还须双区军营；没有声称营数等于战胜列强。

**外交。** kind5补真实B2资格并保留C1实际独立投资人/真实有向投资权/一次60月帮助合同。kind6实际直接宗主increase_autonomy；kind7make_independent；kind8实际market.owner创建grant_own_market；kind9双方独立的实际防御条约。原生自治LD/科技/催化剂、实际军队/GDP比或可靠有向支持条款、关系与权限均重验。没有强制战争按钮，原生独立/自治外交和失败吞并继续有效。

B2动态接收者保存双方、canon serial/kind/政体、当时宗主、市场主人、原自主级；复用45日请求时钟和6月冷却，取消、迟答、拒绝/执行均走现有nonce。自有市场pact存在但owner未重算时无成功登记，最多30日验证；本机无daily-country pulse，使用原生hidden country_event每日延迟自调度并核serial，加月维护兜底。双方政体、原宗主、真实pact、市场事实等变化取消验证。无on_cancel或未知pulse。邻邦预选与实际选择复用同一候选trigger，关系优先、GDP平局，并先具名确认。

## 四处既有文件与共享接口差分

详见 `batch-b2-interface-diff.json`，保序AST比较仅用于记录接口差异，未运行行为矩阵。

1. `common/scripted_triggers/nesnd_canon_diplomacy.txt`：12个原定义逐AST不变（包括reply/current_request/投资有效性）；只扩eligible/result。kind1/11、3、4的旧分支原AST保留；kind2/5共分支仅kind5子支补B2守卫，kind2子支、独立投资人守卫及共同can_create_treaty原操作保留。旧关系20仍适用于全部旧kind；仅新kind6/7/8用其批准的关系门槛。
2. `common/scripted_effects/nesnd_canon_diplomacy.txt`：send与maintenance逐AST不变；accept/refuse仅在原执行体之前委托新kind，原整个执行体逐AST保留；clear只追加B2快照字段清理，不清永久serial或冷却。B2委托成功/失败均清当前请求，原执行体不再次结算。共享事件文件逐字节不变，cancellation_trigger与既有取消合同未回退。
3. `common/scripted_triggers/nesnd_india_diplomacy.txt`：只在can_send中对真实B2国家增加canon等待/冷却及市场验后互锁，其余原字段与7个其它定义逐AST不变。此窄边界有root本轮明确确认。
4. `common/scripted_buttons/nesnd_india_diplomacy.txt`：只路由request4/7真实土邦到新kind6/7。原名称/desc/visible/AI保留；非B2的原possible及整个旧hidden_effect分支保序移入else。其它7按钮逐AST不变。已排队旧印度事件协议/effects未改。

A1/A2/B1其它文件、C2 civic/人物/意大利兼容均未编辑。states和五份本轮相关pops与固定基点SHA相同。主MOD未写入。

## 来源与数值口径

先读NESND/player-writing/工程适配、B2修订2、Astra结构审读、Luna源码人口表及root最终合同。复用计划§3已批准完整链，并补读当前GAME的盈利就业JE→building_groups与building types→真实pact/subject/treaty定义及调用事件、政治运动→原生modifier/人物接口→革命/胜利on_action。原生多州JE只证明对象与检查形状，不复制巴西/西班牙/俄国的固定建筑数。本案新hidden核验事件复用GAME/debug_events的country_event/hidden/immediate形状。原生TryGetOverlordTooltipEntry、Country.GetMarket与Var.GetState显示函数有本机loc实例，未编造UI函数。

GDP10万/100万/1000万对应£20/£200/£2000每周，约52周£1040/£10400/£104000，未封顶前约年度GDP的1.04%。这是源码量纲估算，不能当作73国实测平衡。J/T、利润、市场与支点全部在运行态读取；Luna开局数字仍仅为源码人口普查。

## 文案与后续测试

186对本案双语及其引用文本的作者原文取样、逐条编辑判断、原稿返工和脚本合同说明见 `batch-b2-writing-comparison.md`。保留现有国名与术语，不对原作者署名新引文。反复核对人口覆盖/失业率区别、真实投资许可/实际产出区别、实际主权与高度自主区别，玩家文本不出现profile/epoch或开发交接说明。

本轮只完成实现、冻结、源指纹及定向接口AST差分。**未运行B2 parser/Tiger/MCP全闭包、行为矩阵或游戏，不写STATIC_PASS/ENGINE_PASS。** 下一步由root安排独立Sol/medium测试冻结910文件副本，优先：缺对象/初始预览、73国资格及JOH/YN1后继、200万/150万滞后、两州HYD、三国本土分母/失地重订/海外新增、专业路线正反例、12+12唯一月写入、marketowner改变、政治serial/真实运动/改法超时/人物退出、革命/改TAG/吞并、独立↔高自主终局、kind5独立出资人、kind6–9nonce/拒绝/迟答/失败创建/30日市场后验，以及旧印度/旧C1分支定向保留。原生pact市场重算、事件取消帧、革命回调、AI与自然存读档仍为未实机语义。

技能维护：复核无新永久规则；本机缺daily-country pulse及本案安全守卫均为现有“先查实际接口/分支后读取”规则的应用。未改技能或用户资料。
