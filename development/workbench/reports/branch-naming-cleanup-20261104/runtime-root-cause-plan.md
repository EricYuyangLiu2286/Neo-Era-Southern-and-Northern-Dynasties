# 真实运行错误根因与修复计划

PLAN_ONLY；gpt-6.1-sol / medium。只读源码和已捕获日志，仅写WORK报告；未改MOD、未跑候选、未开游戏。秦条件计划继续等待GO。

## 已证实的两条根因

六份error*.log共18,655条。埃及状态链7种关联报错合计17,524；这不是17,524个独立逻辑BUG。小国两种实际堆栈分别225和166条；空纹理268条另列未归因。日志文件SHA采用runtime-error-capture/summary.json，完整指纹见JSON。

### 埃及状态文字的数据上下文错误

`common/journal_entries/nesnd_egypt_independence.txt:15-19` 以status_desc的first_valid选择三个状态；`nesnd_egypt_with_investor_status`中文/英文目前都访问JournalEntry.GetCountry。真实日志明确“New data types does not contain a JournalEntry data context”和“wanted context of type JournalEntry”。投资对象与foreign_share两项读取同时失败；因此不是仅投资对象已死亡或份额变量缺失。

当前原版契约 `GAME/common/journal_entries/journal_entries.md:175-179` 明写status_desc root=owning country or no scope。`GAME/common/journal_entries/06_economic_regeneration.txt:22-38` 的status_desc选择`je_spa_economic_regeneration_master_status_loc`；`GAME/localization/english/ip4_spain_l_english.yml:21` 用ROOT.GetCountry.MakeScope.Var读取两个国家变量。`GAME/common/journal_entries/06_cuba.txt:338` 与 `ip4_cuba_l_english.yml:31` 是另一条ROOT.GetCountry状态实例。

候选只在实际国家status字符串把`JournalEntry.GetCountry`替为`ROOT.GetCountry`，保留中文/英文文字、百分比和同一个投资对象。cooperating分支已有对象存在性/资格守卫；without/lost分支不访问投资对象，份额script_value本身有缺值0守卫。无需为修展示改国策或设置投资标记。

同类状态键（中英各改；精确路径/行号、调用JE见JSON）：

- `nesnd_egypt_without_investor_status` — `common\journal_entries\nesnd_egypt_independence.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzz_nesnd_batch_c_l_english.yml:5`。
- `nesnd_egypt_lost_investor_status` — `common\journal_entries\nesnd_egypt_independence.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzz_nesnd_batch_c_l_english.yml:211`。
- `nesnd_egypt_with_investor_status` — `common\journal_entries\nesnd_egypt_independence.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzz_nesnd_batch_c_l_english.yml:4`。
- `nesnd_austrian_dispute_status` — `common\journal_entries\nesnd_europe_america.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzz_nesnd_batch_c_l_english.yml:94`。
- `nesnd_usa_border_selected_status` — `common\journal_entries\nesnd_europe_america.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzz_nesnd_batch_c_l_english.yml:110`。
- `nesnd_small_independent_status` — `common\journal_entries\nesnd_small_states.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzzz_nesnd_small_states_l_english.yml:44`。
- `nesnd_small_subject_status` — `common\journal_entries\nesnd_small_states.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzzz_nesnd_small_states_l_english.yml:43`。
- `nesnd_small_regional_status` — `common\journal_entries\nesnd_small_states.txt`；本地化示例 `localization\english\replace\zzzzzzzzzzzzz_nesnd_small_states_l_english.yml:5`。
- `nesnd_south_reconciliation_status` — `common\journal_entries\nesnd_south_reconciliation.txt`；本地化示例 `localization\english\replace\zzzzzzzzzz_nesnd_court_followup_l_english.yml:7`。

完整枚举仅读本项目`common/journal_entries/nesnd*.txt`内status_desc、默认_status、_reason及其$键引用；JSON记录所有有动态函数的条目，不只埃及错误键。缺少状态的默认key不意味着应新增文本。其它同类键仅为源码发现，不冒称本次日志已报。

区分位置，不能全局替换：

- 国家JE的status_desc与reason里访问本国：优先ROOT.GetCountry/SCOPE已保存对象。原版reason实例 `GAME/localization/english/content_2_l_english.yml:471`；JE文档47行亦允许SCOPE.sCountry。contextless JE须其自己的保存/参与国上下文，不能盲套本国。
- 进度条desc由ScriptedProgressBar/JournalEntry UI数据对象调用，原版 `agitators_1_l_english.yml:65-69` 用JournalEntry.GetCurrentBarValue；本MOD南朝bar desc的JournalEntry.GetCountry.GetTooltipTag与当前条数值不能被状态替换规则误伤。
- `gui/journal_entry_widgets/nesnd_succession_board.gui:12` 的JournalEntry.GetInvolvedCountries位于真实GUI数据模型；各行Country来自行模型，原样保留。
- 原版也存在某些reason/状态相关文字使用JournalEntry对象，不能仅凭字符串出现就判整个原版错；本次以真实埃及错误+字段root约定+同字段当前实例锁定替换范围。

### 小国首次累计、清零重入都会写入空变量

调用链 `common/on_actions/nesnd_small_states.txt:1-2` → `nesnd_small_monthly` → 各条件计数，末尾`:167`调用`nesnd_small_episode_monthly`。`nesnd_small_initialize:29-43`仅创建lineage/地理/目标，不创建这八种月份变量。其同名script_value返回0只保护读取，不创建持久value变量。引擎的`change_variable`操作仍面对empty scope。

|变量|实际写入源|首次/重入边界|
|---|---|---|
|`nesnd_small_upgrade_months`|`common\scripted_effects\nesnd_small_states.txt:116`|无regional且candidate_valid进入；else/remove及升级后remove，后续重入仍缺值。|
|`nesnd_small_decline_months`|`common\scripted_effects\nesnd_small_states.txt:125`|regional且人口/州数跌破下限进入；else/remove或降级时remove。|
|`nesnd_small_regional_economy_months`|`common\scripted_effects\nesnd_small_states.txt:131`|首次regional经济条件达成进入；retarget/restore地理时remove。|
|`nesnd_small_regional_governance_months`|`common\scripted_effects\nesnd_small_states.txt:135`|经济分支未运行且regional治理达标进入；retarget/restore时remove。|
|`nesnd_small_economy_months`|`common\scripted_effects\nesnd_small_states.txt:141`|compact分支经济达标首次；革命继承可按安全script_value复制现值，但普通首次无写入。|
|`nesnd_small_governance_months`|`common\scripted_effects\nesnd_small_states.txt:145`|compact治理达标首次；革命复制不保护普通新入国家。|
|`nesnd_small_order_months`|`common\scripted_effects\nesnd_small_states.txt:158`|choose_order刻意remove后设置active/deadline；首次ready便必遇缺值；身份失配/到期再清除。|
|`nesnd_small_pressure_months`|`common\scripted_effects\nesnd_small_politics.txt:99`|政治压力首次连续累计；close_episode与未达条件else/remove后重入。|

建议八处统一改为显式`set_variable={name=计数器 value={value=同名安全script_value add=1}}`。该写法先读取实际脚本值再创建或覆盖数字变量；已有计数n仍变n+1，缺值变1，保留remove作为清零机制。不要用全局一次init标记解决，因为order/pressure/upgrade/decline等被有意remove；不要仅修本次日志已触达的economy/pressure两处。

同项目`nesnd_small_register_targets`的epoch和`nesnd_small_begin_episode`的episode_serial已采用set_variable+safe script_value+1，来源分别`nesnd_small_states.txt:17`、`nesnd_small_politics.txt:27`；不是新增未经证明的接口。原版完整初始化/使用链为`00_meiji_restoration.txt:68`设0、`:83`检查、`:103`change、`:106`重置，证明change应有持久数字前置。若主代理选择缺值设0再change，也须贴近每个入口并覆盖remove重入。

未发现其它小国change_variable写入（全文命中八处）；其他新数值用途核对：issue_population先set0；epoch/episode_serial用安全set表达式；frozen_quote显式set后才var读取；革命on_actions:30-31通过安全script_value复制economy/governance，保留。flag、到期clock、国家/州/人物引用不应硬初始化为数值0。

### 必须保留的真实反例与验收入口（现在不执行）

1. 日志真实反例：`nesnd_small_politics.txt:99` 与 `nesnd_small_states.txt:141` 的change_variable报Variable not value Type empty，不能由mock把缺var当0后声称旧实现通过。
2. 源码直接可达反例：`nesnd_small_choose_order`先remove order_months再激活；后续ready第一次调用change必然无已创建数字。即使修一次初始化也会复发。
3. 源码重入反例：pressure不足→else remove→下次压力达标；upgrade/decline交替分支各自remove；retarget/restore删除regional月份后再次达标。保留原本累计/暂停语义，不追加未有reset。
4. 未来测试必须实际运行真实AST的set/change/remove与脚本值读取；测试环境区分missing、numeric、object类型，旧源码应在真实反例失败，候选才修复。边界包括缺值首月=1、已有n→n+1、阈值前后6/12/24、reset后重入=1、旧档lineage已存在但counter缺失、革命继承有/无counter。
5. 状态未来测试为实际Egypt三分支+small三分支+austria/USA/南朝和两语言，不以正则消失代替UI验收；bar/GUI应仍保留它们的JE对象。主代理先亲审源码和测试，再决定放行。

## 268条空纹理：尚未定位，不改资产

实际信息只有`virtualfilesystem.cpp:569 Could not find texture due to VFSOpen Error:  not found`，没有文件名、widget或调用栈。例error.log:7起连续同秒记录；与上方counter错误相邻不足以证明因果。

只读查MOD三份GUI、gfx与JE，未找到字面texture/icon/sprite/image=""。两个新JE widget未显式请求纹理，board内部small_flag是继承组件；culture_panel有AcceptanceStatus/Religion/PopType等动态纹理。这些事实不足以排除UI数据为空，也不足以归咎我们的GUI或资源。当前结论UNRESOLVED。须获得GUI inspector/引擎调试指向具体widget/请求路径，或最小实际界面复现关联，才批准相应修复。不能因为空路径就随意补图标或删widget。

## 计划文件边界

- `common/scripted_effects/nesnd_small_states.txt`七处counter写；`common/scripted_effects/nesnd_small_politics.txt`一处pressure写。script_values已有正确缺值读取，原则不改；on_actions保留单写入者与革命继承。
- 上列九个状态键的中英文有效定义（实际数量以JSON为准）；root的zz去重/topic迁移同时进行时，修在唯一topic所有文件，删除旧覆盖前逐键证明最终值。不创建另一层zz修补。
- 状态调用者、bar、GUI、资产均只读审计；若候选引入额外逻辑变动须另列具体证据。
- 本报告不将采集日志认定为当前源码所有同类都已发生；源指纹与未来实际运行候选必须重新绑定。