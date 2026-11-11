# 写脚本：引用安全、预览、回调与覆盖原版

> 何时读：写或修按钮、事件、延迟回复、on_action 回调、人物与外交对象的读取，或覆盖、停用原版内容。不必读：查语法骨架和作用域前缀（读 lookup/engine-syntax.md）；查某个接口在哪个版本怎么写（读 lookup/engine-facts.md）。

## 1. 引用安全：按钮、延迟回复与预览

适用当前 1.13.11 / build 24799966。供给按钮原生日志已经证明缺失 scope/变量会在预览中报错；外部援助与进度条的同形修复见 [按钮修复记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/button-guards-20261101/release-notes.md>)。本轮源码/Tiger/MCP检查不是新的引擎验收。

1. **对象先分支，再使用。** `exists`、`has_variable` 与读取并列，以及普通 AND/OR，不构成短路保证。对象变量用 `exists = var:...` 检查可解析对象；数值用 `has_variable` 检查已赋值。保护实际读取的完整链，例如 `s:STATE_TENASSERIM.region_state:DEI`，不是只检查 state_region。`has_war_with`、`has_truce_with`、`relations(...)`、条约国家参数的右侧对象也属于读取。
2. **谓词缺对象明确返回 false。** `trigger_if` 的 limit 只做安全存在性判断，进入分支后再访问对象；配 `trigger_else = { always = no }`。多层依赖按层嵌套。检查 overlord 时按 `is_subject` 分支；独立国走 this，不让另一并列 AND 求值空 overlord。`?=` 适合允许跳过的副作用，不能单靠它证明“有效目标”条件成立。
3. **预览与执行分开。** `visible`/`possible`/选项 `trigger` 不保护 effect 的预览；`hidden_effect` 也不建立安全边界。effect 内重新检查实际前置条件。预览不能假定前面的 `set_variable` 或 `save_scope_as` 已执行：进度条读取临时 scope 前加存在性分支；读取数值再核变量。缺值无明确默认语义时跳过刷新，不能给对象塞零。只有“未累计周数=0”等有定义的数值才用安全 script_value。
进度条的数值函数也须独立处理未初始化上下文，不能把JE的possible、is_shown_when_inactive或immediate当作读取保护。2026-11-03真实QE1日志和存档显示：其他国家持有未激活JE，数值函数仍触发缺变量报错。用script_value的has_variable分支返回无变化值；状态文字/完成条件用trigger_if并明确缺值false。不要为消除错误向所有国家写入西秦变量，也不要重置已有进度。回归证据：WORK/reports/qe1-variable-20261103/diagnosis.md。

4. **延迟回复核整个生命周期。** 沿按钮→请求标记/对象→延迟事件→选项/AI权重→取消/过期清理检查。接收国、发起国、pending、target、双方 sponsor 均可能失效。过期事件用安全的 cancellation_trigger 收尾；接受执行重新检查资格，拒绝清理只操作仍指向本事件接收国的请求。保留冷却与窗口设计，不能未经可达性核对就断言旧事件会覆盖新请求。
5. **可用条件和实际选择同一集合。** `any_*` 的候选条件应与 `random_*`/`ordered_*` 的 limit 一致，特别是 alive、owner、已有 modifier 等排除项。检查实际执行对象，不以按钮亮起替代结果验证。

条件骨架（country scope；对象有效时才比较）：

```text
trigger_if = {
    limit = { exists = var:partner }
    var:partner = { is_country_alive = yes }
    NOT = { has_war_with = var:partner }
}
trigger_else = { always = no }
```

查原版链条时可定位 GAME `events/commander_events.txt` 的 saved scope、cancellation_trigger 与 option；`common/scripted_triggers/00_scripted_triggers.txt` 的 trigger_if。原版也存在并列 exists 写法，不能据此覆盖本项目已有的真实失败证据。以修复后的外部援助条件和供给 display 为项目安全实例。

接口字段按各自文档核对，不能凭相似名字统一（例：条约预检用 `good`、创建用 `goods`，见[原生条约、供给和援助](../lookup/native-treaty-aid.md)）。

修改闭包后检查引用缺失、取消/过期、对象转属与预览四类边界；外部检查须绑定文件 SHA。现有回归工具为 `WORK/tools/check_button_guards_20261101.py`，覆盖真实源码结构及数据不变性，不模拟 Jomini。原生日志复发时扩展相应断言。读取 MCP 嵌套结构用精确 key_path（例如 `cancellation_trigger.NOT`），`[block]` 只表示未展开。

局部重写保留原 token 的引号、重复键和注释；尤其 `"relations(scope:...)"` 不能由宽松 parser 的 emitter 丢掉引号。格式化只限受改定义，以保序 AST 等价及独立 Tiger 复核。新脚本采用 UTF-8 BOM；原文件保留编码/换行。

## 2. 覆盖原版与编码

按目录分别验证同路径替换、数据库条目替换与追加。现代 `REPLACE:key` 可见于本 MOD 的文化和定义，但不能据此假设 history 文件有同等语义。重复国家/地区定义必须审查有效加载结果。不要用 `.bak` 作活动文件；备份在 WORK/backups 的独立目录。

文本保持原换行/BOM风格，局部修改保留注释；本地化键 ` key:0 "文本"` 不能把双引号/反斜杠错误转义。绝不全局格式化或以字典去重引擎脚本。

### 定点停用原版故障链

用户允许从本MOD侧停用已定位的原版故障内容，其他作者MOD只读。先从error.log定位ID和完整入口链，按数据库支持选择覆盖：本项目已证JE和scripted_button可用`REPLACE:ID`，关闭visible/possible等对应trigger；事件REPLACE支持未核实时沿用同路径覆盖，只把目标事件改为hidden惰性壳（trigger always=no、cancellation_trigger always=yes、空immediate），其余定义和namespace保序保留。只关闭UI入口不能替代清除旧队列和effect中的坏引用。

同路径覆盖须记录当前GAME版本/源SHA，并用保序AST比较所有非目标对象；升级时重新对照，避免冻结整文件后漏掉更新。局部坏权重只停该limit，勿关闭仍被本MOD引用的整个意识形态。scripted_button的ai_chance采用当前实例的`value=0`（00_colonial_administration_buttons.txt:40），旧Markdown的`base`不能直接当作有效语法。2026-11-03具体证据：WORK/reports/cne-time-native-ban-20261103/native-ban-contract.md。

## 3. 事件、回调与时序

- 战斗结束的on_action先排队次日检查，待占领刷新；用日志周度检查补漏。实际执行重新核战争与controller，友军控制不算敌占。所有回调共用一次标记与同一个提交效果，不能按每个观察国各吞并一次。

事件duration按本机NEvents.DEFAULT_MONTHS_VALID及原版实例理解为月，不能与变量days等同。异步请求的锁覆盖事件窗口；实际答复提前清理，父任务结束使请求失效。若不能证明锁与事件不会重叠，增加请求身份检查；不要仅凭同名pending变量认定旧回复属于新请求。

### 外交博弈与延迟答复的求值

外交博弈 `possible` 和延迟事件答复均可能在常规发起者以外求值。对手、申请对象等可空变量须在同一个 `trigger_if.limit` 里先检查存在，主体内才比较；不能依赖并列的另一条 trigger 返回 false 来保护随后读取。按钮预览与事件选项都需分开审：用原生说明显示修正、关系，内部请求编号和收据不应展开。

### 战后结算与寄居人物（2026-11-04）

一轮war结束不等于整个剧情争端结束。改停战/战败链时搜索所有settled写入者，包括旧JE complete、延迟事件immediate、僵局按钮；不能让新周度队列与旧终局互相改写。按实际参战轮次登记一次答复，延迟外国回复重验对象、轮次、期限和当前关系，实际建立附属关系后才提交结果。

先保存皇帝与原继承者，再转移皇帝；移动君主可能立刻触发继承。实际owner确认失败则走原生exile_character_with_role_cleanup；两者失败时阻止吞并且保留重试，不能先记录已答复把国家锁死。寄居别国的受保护人物也要避开旧随机处置链，不仅检查“行在”国名标记。不得据此自动改接收国君主、政体或玩家tag。

来源：GAME/common/scripted_effects/00_scripted_effects.txt的流亡清角色；WORK/reports/journal-war-feedback-20261103/ming-war-source.md及boundary-tests.json。故障注入检验脚本分支，不是引擎迁逃验收。

## 4. 人物、地区与人口

### 宗室延续与无所属角色

需要恢复人物时先查已保存身份，再查本国、every/any_character、流亡池及void，确认存活与owner；exile/void不得先无保护比较owner。移出外国在位ruler/heir须有明确剧情授权，不能将同姓当作身份。只有确定缺少可用活人且作者授权时，create_character创建新角色，不能重用旧历史template当复活。行辈/支系单独记录，淮系不能混宁系；已有姓名不回写，新出生只查自己的父系，不能为每个国家的出生扫描全球。on_created保存新角色后验证其owner，再立为君主；一次结算/创建锁避免重复刷人。当前原版法国、日本及巴西来源见WORK/reports/persia-journal-ui-20261103/ming-successor-generation.md。

角色存在、存活和owner有效性分别判断；适用于前述宗室/流亡池读取规则的实际失败证据为WORK/reports/observer-logfix-20261103。图形tag中的market链接同样在不存在时显式false；同路径兼容覆盖需随原版更新重查。修复源码与静态检查不升级为实机通过。

### 案件隔离与州转属（印度实施，1.13.11）

- 地区案件循环与重试每次先clear自己的临时backer/target scope。上次循环saved scope不会因下一次if不命中而自动消失。本轮已复现源码反例：第二案不合格赞助者会沿用第一案backer。
- set_state_owner转入现存国可能合并同地区州。返还整个region_state不是返还原来的province子集；回滚须保守证明未取得第三国地块。当前新建单州案同时保存原省份数并监听后续territory变化；不能以num_states=1单独证明安全。未知回调顺序保留引擎待验，不为清理而吞并整个现存国。

来源与实际复查：WORK/reports/india-development-20261103/commission-execution-contract.md、uprising-execution-contract.md、india-standards-review.md。

### 文化键与数量（2026-11-05）

人口转文化先由游戏中显示的名称反查当前有效本地化，再查文化数据库和 MOD 覆盖。这里“华北”是 `han`，“江南”是 `ce_wuu`；`ce_zhonghua` 是“华夏”。以 Pop、全州或全国为分母是三种不同的效果。指定“随机一州的一群人”时要分别抽州、抽 Pop，在 Pop 作用域使用 `change_pop_culture`，不迁移、不删除人口。测试还要覆盖选无合格人群及恰好等于门槛的月份。

1891年终档所对应的1.13.11日志中，日本逐 Pop 过滤时比较暂存的目标文化反复产生 `Invalid right side during comparison 'scope'`。已知有限的目标文化可在调用处传入实际 `cu:` 文化键，再在同一参数化 effect 中用于候选过滤与转换。离线模型中能比较对象，只能证明抽样意图，不能为引擎的文化类型接口背书。收到长局日志时一并读取保留下来的轮替文件，按时间戳分隔的整条调用栈计数，再与实际加载的源码版本比对。
