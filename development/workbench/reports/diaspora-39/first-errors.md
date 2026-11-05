# 第39轮第一局退出日志：归因与源码修复

状态：STATIC_PASS；本分工未启动游戏、未提交 Git。检查对象为主 MOD 的下列定点修改。执行配置：父代理委派的 `first_log_fixes`；本上下文未公开实际模型/推理强度，不从任务名推断。

`catalog.py status` 核对当前本体 1.13.11 / Steam build 24799966，索引 CURRENT、changed_count=0。原始证据为同目录 `first-exit.log`；完整逐条调用栈和分组保存在 `first-log-attribution.json`。修改前五文件独立备份：`WORK/backups/pre-change-diaspora39-first-errors/`。备份不是本轮其他代理修改前的整个 MOD 基线。

## 归因

按时间戳分隔的完整 Script system error 块计数，52 条中有 39 条的首个脚本路径实际由主 MOD 提供，13 条为无 MOD 覆盖的本体或无来源错误。

| 首个脚本位置 | 数量 | 处理 |
| --- | ---: | --- |
| `nesnd_egypt_independence.txt:148` | 6 | Treaty(40–45) 不支持变量，撤销 treaty scope 的写入与后续读取 |
| `nesnd_american_restoration.txt:462` | 2 | 单州种子没有 second；可空比较右值仍报错，改为存在性分支内比较 |
| 同上 `:333/:342` undefined/unset host | 8 | 创建后的初始化从调用方上下文执行，派遣不再清理调用者持有的 host scope |
| 同上 `:19–22` remove_variable | 8 | 上述缺 host 的级联错误，清理回到真实 host country |
| 同上 `:335–336` set_variable | 10 | 上述缺 host 的级联错误 |
| 同上 `:348` has_variable | 2 | 上述缺 host 的级联错误 |
| `agitators_events/agitators_law_events.txt:990–991` | 3 | MOD 确有该覆盖；原生同形也漏 supporting_ig，补候选资格、取消条件和两个选项的可空副作用 |
| 本体 `brazil/peru_bolivia.txt` | 3 | 2次重复参与国、1次同国关系；主 MOD 无该文件 |
| 本体 `peoples_springtime.txt` | 3 | 叛乱 IG 移出执政；主 MOD 无该文件 |
| 本体 `agitators_events/exiles_events_02.txt` | 4 | 无有效 IG 的角色任命；主 MOD 无该文件 |
| 本体 `00_dynamic_state_names_europe.txt` | 1 | 波兰动态 hub 名缺本地化；主 MOD 无该脚本覆盖 |
| `<unknown>:0` | 2 | 失效 country，日志无可定位项目调用栈，不能无依据归为本 MOD 已修 |

另有 134 次重复 JE 提示；按既定要求保留自动入口，不为消警关闭日志。DLC 商店、第三方重复肖像资源、无 MOD 覆盖的 GUI、引擎断言和变量静态提示分开记录，不算进上述52条。无游戏内回归证据时不宣称它们已经消失。

## 改动与生命周期

埃及：删除在 treaty 上标记 `nesnd_egypt_1825_treaty` 的注册逻辑。`nesnd_egypt_expire_historical_treaties` 只在 EGY 存活且日期到1845年后，针对 FRA/USM/SIH/GBR/QE1/TUR 六组条约检查 `is_historical_treaty=yes`、对方绑定，以及 EGY→对方投资权、对方→EGY独立保证两条有向条款，随后无罚退出。开局/读档 after-lobby 与每周维护均可调用；旧档中的 `nesnd_egypt_treaties_registered` 不再控制迁移，不依赖此前失败的 treaty 标记。1836—1844不退出；游戏开始后新签的同形条约不退出；已退出或不再绑定 EGY 的条约自然不再入选。没有改1825历史条约、20年期限或其六方权利。

复国：原调用栈已经证实 `on_created` 读取 caller saved host 时为空；日志不能单独证明是回调复制边界还是调用后清理时序。修复不依赖这两者：固定 TAG 在 `create_country` 后从调用方显式跳转再初始化，完成后才清理种子。区域复国同一机制一并改写。派遣使用自己的 `nesnd_restoration_dispatch_host`，不删除外围选择器拥有的 `nesnd_restoration_host`。`nesnd_restoration_state_selected` 在每个 seed/second 存在性分支内比较，州选择仍排除同一组已选州。未改人口流散、settlement、war_watch 函数。

煽动者：第9事件的 supporting IG 筛选可能为空；事件 trigger 现在要求与实际 random selector 同形的在野程度/执政/法律立场候选，当前立法对象先分支确认。支持 IG 消失时取消，选项对 supporting IG / opposing movement 的副作用使用原生 `?=` 跳转。两种修正、期限及玩家文本不变。

## 实现前本体完整链条

- 国家创建：`GAME/events/central_america_events.txt:49–95`，`central_america.2` 在 `create_country` 后使用 `c:GUA ?= { save_scope_as = scope_GAU }`，从原调用方继续访问新国家。`effects.log:878–888` 定义 tag/origin/state/on_created，说明 on_created 的当前对象是新国家，不承诺继承 saved scope 的生命周期。本项目差异：固定 NAH/TWT 与四类地区 TAG 随后运行原有复国初始化。
- 条约历史数据：`GAME/common/history/treaties/00_historical_treaties.txt:1–18` 使用历史生效日和 binding_period；本 MOD `common/history/treaties/nesnd_egypt_1825.txt:1–56` 定义六份1825/20年条约。`GAME/common/treaty_articles/02_guarantee_independence.txt:1–22`、`07_foreign_investment_rights.txt:1–22` 定义两种 directed article。项目 `nesnd_canon_diplomacy.txt:116–120` 在 source/target 存在性分支内核对条款方向。
- 条约查找与退出：`GAME/common/scripted_effects/00_chris_scripted_effects.txt:118–145` 的 `russia_breaks_independence_pact` 由 country 遍历 every_scope_treaty，按 binds 和 article 过滤后在 treaty scope withdraw。`GAME/common/script_values/static_treaty_acceptance.txt:416` 使用 is_historical_treaty；生成文档 `triggers.log` 的同名条目明确支持 treaty。`effects.log:37390–37398` 定义 withdraw 国家及罚则参数。
- 外交博弈：`effects.log:909–922` 的生成说明与当前实际脚本对字段的描述存在差异；`GAME/events/british_raj_events.txt:276–280`、`japan_events/ep2_ezo_republic.txt:89–101` 实际使用 `target_country`，因此保留 MOD 已有的 target_country 写法，没有根据泛化文档擅改。
- 煽动者事件：`GAME/events/agitators_events/agitators_law_events.txt:922–1018` 的第9事件、`GAME/common/scripted_effects/00_scripted_effects.txt:319` 的 save_agitator_law_scopes、`GAME/common/scripted_triggers/00_scripted_triggers.txt:1300–1361` 的 enactment predicates 组成原生链。原生事件在缺 supporting IG 时同样缺保护，已有 MOD 覆盖中的对应位置偏移+2行；本次只修该事件，不拷贝整个本体新文件。

## 外部验证及限制

`python WORK/reports/diaspora-39/check_first_errors.py first-errors-red.json` 在原始源码上记录6项失败；定点修改后同一命令的 green 记录为 STATIC_PASS。扩展后共10项源码合同通过，包括实际 trigger AST 的12个 seed/second 有无/州匹配分支，以及实际 treaty filter/date AST 的192组历史/后来条约、双向条款、日期和六方组合。未支持的 AST 节点会报错；空比较右值抛错，不把缺失对象当0。

该程序验证实际源码片段的已知错误结构和分支，不执行游戏引擎，不证明引擎回调时序、真实建国/战争、条约到期或事件自然抽取。最终主审应亲读原日志和差异，并在本轮冻结后统一跑 Tiger/集成检查。尚未运行新的游戏场景，不能将本报告升级为 ENGINE_PASS。
