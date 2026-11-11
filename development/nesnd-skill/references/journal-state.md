# 日志的状态、同步与生命周期

> 何时读：新建或改造日志、进度条、父子日志、阶段切换，或修“进度不对、重复计分、旧档日志残留、子日志没出现”。不必读：只改条面或提示文字（读 journal-display.md 与玩家写作技能）；查 1.15 字段名（读 lookup/journal-ui.md）。

## 1. 唯一的状态与写入者

旧候选把土地进度和风险拆成两个无故事日志，又把规则塞进正文，需要改造。若用 scripted progress bars，必须核对独立存储与变量的同步：不能让条本身 monthly_progress 与 JE on_monthly 同时重复计分。源注释说明前者先执行；旧国家变量、存档迁移、按钮与事件变更均应统一到一个权威状态，真实游戏测月界和保存重载。

### 带进度条的日志

定义 `common/scripted_progress_bars/ce_*.txt` → JE 用 `scripted_progress_bar = key` 引用 → `complete/fail/invalid` 收尾 → 按钮/事件只改变指定的 bar 或用于 bar 计算的变量 → 条面本地化写短指标名与读数，周期变化原因写在悬停明细。字段和排查示例见 [日志文字约定](../lookup/journal-ui.md)。

真实参考：MOD `ce_poland_progress_bars.txt` 的 `ce_polish_reconquest_energy_bar`、`journal_entries/ce_europe_poland_issude.txt`、`scripted_buttons/ce_poland_scripted_buttons.txt`。另读原版 `00_je_progress_bars.txt` 及引用者验证 scope。原版文档规定 weekly/monthly/yearly 的进度更新先于对应 JE pulse；不要双重累计。

进度条的 `start_value/min_value/max_value`、`monthly_progress = { add = { desc = key value = 1 } }` 是定义；不能伪造 `progress_bar = { current = ... }`。使用 `change_journal_entry_progress` 等名称前必须从本机导出或当前用例确认其确切名称和参数，而非凭记忆。

### 原生进度条与初始化恢复

GAME/common/scripted_progress_bars/scripted_progress_bars.md与本MOD ce_french_empire_progress_bars.txt支持monthly_progress/yearly_progress内具名add={desc=... value=...}，value可用脚本值或有守卫的变量。先用原生明细呈现来源，勿用长篇更新说明替代空白条。

已有国家变量供存档与事件使用时，允许同一条公式供原生明细与实际结算共同调用；原生条先于同周期JE脉冲运行，随后JE更新国家变量并绝对set_bar_progress。必须在同一JE完成周期计分与同步；不得再把已经自动增长的bar读回后加同一增量。跨父子JE年度顺序无此保证。新建/旧档、月年同日、按钮改变与临时scope预览都分别查；源码公式相同不等于引擎验收。

一次性schema/init标记与可恢复running标记分开。若开场事件在父JE加入前初始化，孤儿清理可删running；后续恢复不可因init已存在而永远跳过。实际父JE有效且无终局时，恢复running并用has_journal_entry保护显式补齐子JE；不重置进度/信心。on_fail/on_invalid与旧档迁移都应覆盖。

州按钮的开始与暂停都看所属州是否仍存在于本国。原生on_state_owner_change/on_state_created的root为state（GAME/00_code_on_actions，ip4_on_actions有移除州modifier实例）；检查父JE有效后清理失去的州，再用具名国家事件清理对应国家/人物惩罚，保留其他州。补周度检查覆盖旧档与部分割地。普通脚本战争与原生revolution/secession分别判定，不能用is_at_war代替内战。

## 2. 父子日志、阶段与终局

### 非开局入口、终局回调与镜像条

新增父子JE或后继JE时，画“初始化→添加父JE→添加子JE”有向图；初始化effect不反向添加自己的JE。possible不能正向依赖自己的has_journal_entry；完成effect判断持久资格、进度和done，不要求该JE仍在活动列表。显式添加与自动possible入口共用终局锁，维护回调补漏不重置既有进度。
有期限的JE保留country期限标记，意外移除再添加不得刷新十年；端点保持时间必须离开后清除重计。军事基线在大厅结束后读实际建筑数量，日志初始化过早时使用有界次日恢复及旧档月度入口，不能把未初始化的0当正常基线。
通常由本JE独占country结算及条同步；父/子需要镜像时仍只有一个country写入者，每个JE自身回调做绝对同步，并覆盖两种回调顺序。外部顺序模型只证明脚本约定，不能替代引擎时序验收。实例与12项生命周期矩阵见 WORK/reports/qin-persia-20261102/。

### 阶段可进入与永久结束分开

跨阶段JE分别定义available（现在允许开始）与eligible（国家/制度仍允许继续）。未达到后继阶段不能被通用bootstrap当作永久invalid而提前写archived。当前已活动的旧档JE可在维护effect登记opened标记；不要把自己的has_journal_entry写进possible形成首次进入自锁。后继已解锁不因暂时丢失触发地重置，完成/封存锁仍独立阻止重领。西秦五脚本修正及原版“维新完成标记→神佛分离决议→宗教JE”来源见WORK/reports/japan-research-20261102/qin-stage-design.md。

### 阶段切换与数值同步：印度反例

保存变量并不会自动初始化新加JE的条。JE immediate、保留进度后重新进入、按钮改变与外国镇压改变都调用同一个只同步效果；计分仍只有该JE的周期回调。同步时保存当前country并保护存在性，不用可能是全球调用者的root读取国家变量。跨国/全局案件只负责生命周期，避免与国家JE重复推进。

暂时条件（战争、破产、军力或合法性）失去时按设计暂停、停维护费并保留案件；不要共用“新建资格”作为存续资格，导致自动清案与长冷却。建设奖JE完成之后仍需要的治理/防御按钮应挂在常驻入口。人口与领土成果不是按钮退出时的临时修正。

实际前后：WORK/reports/india-development-20261103/india-spec-review.md、india-spec-review-final.md及final-validation.json。未开游戏。

### 绝对条件数与切换重点（1851测试档反例，2026-11-04）

现值条不是“从进入日志起再增加多少”。goal_add_value会保留进入时baseline；东洋JE存档baseline=2、goal=5，现值1显示−1/3。当前条件数/占领数改用有界scripted_progress_bar，immediate同步现值，周期明细算目标减当前条。旧活动JE必须迁移而不能只改定义留着旧baseline；迁移不得重置外交结果或重发奖励。

互斥建设重点若仅暂停推进，显示/存续条件与计分条件分开。取消重点不等于invalid；父日志结束/不再符合国家身份才清退。复核调用者根scope：country JE/tick与JE-root bar不是同一root，跨层shortage等国家参数显式传入，并核全部调用点。别用未经验证的prev.prev链掩盖根对象不明。

来源、39组文案对读、实际AST边界与局限：WORK/reports/journal-war-feedback-20261103/。静态检查不认证旧档JE重建的引擎显示时序。

### 常驻议程

- 常驻议程可无胜负，明确存续及关闭原因；真正成果用complete，身份/所有权失去用invalid。退出条件需要否定整个合取时，用明确OR的各项失效原因或NOT包AND，不能依赖多项NOT的含混阅读。已有国别counter完成而旧阶段JE仍在时先查真实存档，不再给一遍进度/奖励。

### 改革子日志与具名目标（2026-11-01）

长改革把各项目的建设/法律条件、启停和真实利益得失放入对应子日志；主日志保留总进度、失序与终局。删减主tooltip时把仍在使用的完成阈值迁到子日志，统一有效本地化键，检查旧replace层是否还保留过时的进度说明。主成功/失败/invalid/主动结束及意外移除都清理临时项目，子日志依赖实际父JE，不能仅靠永久flag。

涉及“最高失业州”等动态目标时，先通过具名州的placement/本地化确认事件展示目标与实际费用，再扣款；保存目标不在确认时悄悄换州。确认、取消和执行检查这个保存对象的资格，而不只检查全国还有任一合格对象。当前CNE例子见WORK/reports/cne-reform-subjournals-20261101，尚未引擎验收。

IG吸引力、IG支持与角色忠诚各用自己的实际修正。逐州军队支持是国家修正，军官忠诚是角色修正，不能把character_loyalty_add塞进国家修正并假设传给全体军官。按州唯一key对应开始/暂停/终局清理；显示可叠加的实际代价。角色维护按受影响对象列表处理，参照原版00_sgui_effects的daimyos_list与00_victoria_ep2_scripted_effects的variable列表迭代；新任、转属、退役和终局分别处理，避免月度全世界人物扫描。

## 3. 全局日志、节奏与按钮组

- 同一日志供各国查看时，使用`context=none`的journal_entry_group、should_be_involved/should_show_when_not_involved，并按原版01_ryukyu_rivalry方式动态add/remove_involved_country。全局副作用放单次全局回调，个人通知才用all_involved。`scope:journal_entry`只在已附着的JE上下文访问；一次激活与一次提交分开记录，既有状态不随读档清零。

2026-11-01南朝反馈补充：

- 事件调用scripted effect时，沿调用链找真实加分位置。陈死亡的＋25在`nesnd_chen_after_death`，不能因事件文件只有函数名便再加一次。变量改变后同步国家JE与全局JE的对应bar，保留preview scope guard和一次结算标记；同时审查intro/immediate的归零，刷新与旧档迁移不能覆盖已经积累的值。
- 节奏有明确期限时，同时核月增量、随机等待、人物存活门槛、各国答复期限及外交阶段。随机事件概率不等于最迟日期；用既有事件入口安排明确窗口，并让延迟死亡先结算再进入后续。具体南朝1837–1839安排属于本轮用户规格，见主项目任务11，不推广成其他剧情的固定年份。
- 同一按钮组按政治身份筛选：中央朝廷不提供“从自身争取自主”或“对自身争位中立”的入口。固定阵营须同时约束初始化、只读显示、AI复议、盟约和事件默认选项；只改初始数值不能保证下一月仍有效。
