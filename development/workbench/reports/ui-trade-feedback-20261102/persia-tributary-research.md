# 波斯朝贡西秦：最小修复研究

2026-11-02；只读研究。用户最新明确“波斯应该是西秦朝贡国，修复”，该指令确定目标关系。先前qin-canon-api.md记载“当前脚本没有PER属国关系”是修复前事实，不是要维持独立的设计裁定。本报告未修改玩法文件、未开游戏。

## 结论

**西秦的recognized类型目前已能拥有朝贡国，本次无须修改subject_type全局规则。最小新局修复是补QE1→PER tributary历史关系，并从两国旧条约中删除不相容的defensive_pact条款。** 原有经济权利不应因为条约标题误导而整份删除。旧存档的历史文件不会重跑；如要求同时兼容旧档，新增一次性、有明确适用入口的迁移，不把“波斯当前独立”长期当作BUG自动纠正。

## 1. 当前完整链

路径前缀：
- MAIN = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties
- GAME = D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game
- DOC = D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031
- 当前版本1.13.11 / 24799966；已读取原版定义、原版history和事件调用、引擎script_docs、实际MOD覆盖定义。

### 原版与MOD类型限制

GAME/common/subject_types/00_subject_types.txt:124–181定义subject_type_tributary。原版只允许unrecognized宗主（:153–155），宗主等级只列unrecognized_major_power/unrecognized_regional_power（:163–166）。

**本项目已覆盖这些限制**：MAIN/common/subject_types/ce_subject_types.txt:1是REPLACE:subject_type_tributary：

|字段|现行MOD值|对QE1/PER的结论|
|---|---|---|
|valid_overlord_country_types (:30–33)|unrecognized、recognized|QE1 recognized已经允许|
|valid_overlord_ranks (:41–47)|unrecognized_major_power、unrecognized_regional_power、great_power、major_power、minor_power|recognized宗主相关等级已存在|
|valid_subject_country_types (:35–39)|unrecognized、recognized、colonial|PER unrecognized已允许|
|valid_subject_ranks (:49–54)|minor_power、insignificant_power、unrecognized_regional_power、unrecognized_power|不含unrecognized_major_power，须检查实际初始化后的国家rank|
|overlord_must_be_higher_rank (:10)|yes|仍有宗主较高等级要求|
|overlord_must_be_same_country_type (:11)|no|不要求QE1/PER同类型|
|can_start_own_diplomatic_plays (:6)|yes|朝贡保有自行博弈权限|
|join_overlord_wars (:8)|no|不会因此无条件替西秦参加每场战争|
|breaks_if_subject_not_protected (:7)|yes|原生保护义务仍保留|
|diplomatic_action (:16)|tributary|必须通过对应pact建立实际关系|

MAIN/common/country_definitions/ce_countries.txt:26–35的QE1为recognized；:153–162的REPLACE:PER为unrecognized、ce_xiyu+persian主文化。无需将QE1降为unrecognized，亦无需把PER改文化/人口或直辖领土。

现有全球recognized扩展是本项目前置行为；本次不再扩大，也不以“缩回原版”为名撤销。USM/CNE/FRA历史也使用tributary（ce_subject_relationships.txt:17、51、165、193、205），贸然缩回会改变已有设计。

### rank不是国家type

GAME/common/country_ranks/00_country_ranks.txt:1–7说明rank由威望条件及合法性分配；:152–169定义unrecognized_major_power，:184–204定义unrecognized_regional_power，两者均enforce_subject_rank_check=yes。本轮没有实时存档rank证据，因此不能以PER国土大或帝国tier断言它必为unrecognized_major_power，也不能承诺历史建关系后引擎一定如何降rank。

引擎有可查询入口 DOC/triggers.log:9003–9008：
```text
# 在QE1 country scope
can_have_as_subject = { who = c:PER type = subject_type_tributary }
```
此trigger有原生文档与trigger_localization/00_trigger_localization.txt:4254–4257；当前原版玩法文件未找到实际使用例。因此适宜作为定向运行诊断，不把它悄悄加为历史初始化条件导致“想修复但条件不满足就静默跳过”。

未查到subject_types中按TAG运行的valid_overlord_trigger/valid_subject_trigger等动态钩子。上述字段是静态列表，不能往列表塞“只允许QE1”的trigger块。既然现行type已经允许，最小方案就是不改。若实测确认rank阻断，先读取真实rank和can_have_as_subject结果；不要为尚未出现的故障先全局放开unrecognized_major_power或取消rank要求。独立自定义subject_type+配套diplomatic_action是更大方案，亦需额外验证，不适合作为当前默认修复。

### 实际建立关系的原生链

- GAME/common/diplomatic_actions/24_subject_tributary.txt:1–27：tributary.pact关联subject_type_tributary；income_transfer=0.2，按second_country收入，转给第一国；actor_can_break及target_can_break保留正常外交退出规则。potential always=no只禁止常规界面主动建关系，不禁止原版history或脚本effect调用。
- GAME/common/history/diplomacy/00_subject_relationships.txt:240、246、641、647有create_diplomatic_pact type=tributary历史实例。
- GAME/events/zanzibar_events.txt:961–965在ROOT宗主scope中创建c:UTR tributary，证明运行中也有同形调用。
- DOC/effects.log:899–907：create_diplomatic_pact由country scope发起，country目标、type外交行为名。
- DOC/effects.log:677–680：change_subject_type在属国scope调用，只改变既有subject类型并保留Liberty Desire。它不能把独立PER变成朝贡国，也不负责指定宗主。
- DOC/triggers.log:11539–11545 is_direct_subject_of，12455–12459 is_subject_type；12447–12453 is_subject_of包含间接属国，迁移守卫应优先检查direct关系。
- 原生战争链GAME/common/war_goal_types/17_make_tributary.txt:1–16有kind=make_tributary和validate_subject_relation；该战目标不是修补历史初始关系所必需。

## 2. 最小建议diff：新开局

### A. MAIN/common/history/diplomacy/ce_subject_relationships.txt

在现有c:QE1块（原:168–180）保留KAZ/KAL，加入：

```text
if = {
    limit = { exists = c:PER }
    create_diplomatic_pact = {
        country = c:PER
        type = tributary
    }
}
set_variable = nesnd_qe1_per_relation_v1
```

新局历史中PER已有state、没有其他宗主，故不需要先make_independent，也不应重建PER country。标记用于声明这个新局已使用新关系版本，防将来运行脚本把合法独立战争结果重置。若项目偏好独立前缀历史文件，同样可在COUNTRIES之外的正确DIPLOMACY容器中复用现文件形状；不要混用country history容器。

### B. MAIN/common/history/treaties/ce_historical_treaties.txt

仅在name=treaty_name_state_of_persia_protectorate、QE1/PER这一条约（原:64–102）删除其:74–76的：
```text
{ article = defensive_pact }
```

保留条约名、1811.6.22日期、30年binding_period、两向投资与贸易特权，先不改其他USM/QE1和第三国条约。此旧诏现在承载宗藩体系内既有经济权利，实际朝贡关系由pact负责。**不要添加第二个20%money_transfer条款重复征收朝贡。**

### C. 不必改的文件

- common/subject_types/ce_subject_types.txt：类型已允许。
- country_definitions：保留QE1 recognized、PER unrecognized和两国culture/tier。
- states/pops/buildings：PER仍是自己持有领土和人口的TAG；朝贡不等于吞并。
- 全球24_subject_tributary、17_make_tributary及原版treaty_articles：不需要全局覆盖。

## 3. 原条约保护：哪些冲突已证实

MAIN/common/history/treaties/ce_historical_treaties.txt:64–102现有防御、两向投资、两向贸易；名字里的protectorate不是实际属国规则。

**防御条款确实不兼容：**
- GAME/common/treaty_articles/01_defensive_pact.txt:49–55，requirement_to_maintain要求first_country NOT has_subject_relation_with second_country。
- GAME/common/treaty_articles/treaty_articles.md:106–112明确：维持条件失败，下一更新自动break该article；can_ratify也检查维持条件。
- 所以新局主动去掉该条款；旧档迁移建立朝贡后，可由原生在下一更新清掉该article，无需整份withdraw条约。

**投资和贸易不能一起武断删除：**
- 07_foreign_investment_rights.txt:41–44的possible排除“ROOT是对方subject”，是新谈判资格。其:110–118实际维持条件只要求双方aggressive_diplomatic_plays_permitted=yes，而tributary允许自行博弈。故不能仅凭possible宣称已有历史投资权会立即失效；要查迁移后实际条款与权限。
- 25_trade_privilege.txt:44–59的non_fulfillment会在source为junior_in_customs_union或孤立主义时freeze。朝贡是否同市场及是否出现此条件须读实际状态，不以“subject”单词代替关税同盟判断。此项不是已证明必须删除的条款。
- treaty_articles.md:389–406区分possible与can_ratify；不要混作持续维护条件。
- DOC/effects.log:37390–37398 withdraw作用在整份treaty；即使apply_break_penalties=no也不是仅移除防御article。原生意大利等事件也会withdraw整份；本修复不应借此抹掉用户后来追加的经济条款。
- 未找到可直接静默删指定article的原生effect。本轮不要发明remove_treaty_article。依赖原生维持检查清理已证不兼容条款即可。
- 不因该诏30年binding_period便写成1841自动消失：binding period不是本轮已证明的有效期终点。

## 4. 旧存档迁移与玩家改变后的世界

### 能保证的行为

历史文件改变只保证新开局使用新配置。on_game_started在书签初始化后触发，on_game_started_after_lobby只在每个campaign首次入局触发，见GAME/common/on_actions/00_code_on_actions.txt:3–13；没有把这两者当每次load自动补丁的依据。

若添加旧档修复effect，必须具备：

1. 显式入口与一次性标记nesnd_qe1_per_relation_v1；一旦处理过就不再自动重绑。
2. 两TAG存在，QE1独立，PER当前独立；双方没有活跃战争/外交博弈/革命等会冲突的场景。
3. 如PER已直接朝贡QE1，仅登记已满足；若PER是第三国属国、间接属国，或已是QE1其他自治等级，不应make_independent/强制降自治。
4. 只创建QE1→PER这一个pact；不释放土地、不移动人口、不卡拉特/莫克兰关系、不重建所有条约。
5. 建立后以PER.is_direct_subject_of=QE1和is_subject_type=subject_type_tributary检查实际结果；失败应留可诊断状态，不能把未建立写成完成。
6. 后续独立、吞并、换宗主、升降自治都尊重原生玩法，不让每月脉冲“修回”。

### 不能凭空保证的事

**旧档首次安装时PER独立、仍保留1811历史条约，并不能证明玩家此前没有合法改变其宗属关系。** 该旧版本从未写入归属修复标记，也没有已证实的“玩家曾争取独立”完整历史查询API。仅以日期较早、条约尚在、ruler未变、国界未变作守卫，都只是启发式，无法严格区分“旧版漏建关系”与“玩家刚恢复独立”。

因此推荐：
- 新局只依history修正。
- 已有目标存档若用户明确要求本次修回，可用受上述约束的一次性定向effect；入口可以是仅供该迁移使用的决定/事件，或已授权的精确存档迁移。不要部署永久自动从属修复。
- 无明确旧档修回要求时，旧档首次加载只能标记迁移可用，不能静默把所有后期PER重新附属。如此无需每次追问用户，也不会把正常外交结果当BUG。

可选自动兼容仅限已确认未推进的1836.1.1初始旧档；仍应在实现说明标明该适用范围，而非声称适用于任何年份。若父任务决定对用户当前明确指定的进行中存档迁移，则把该存档作为独立验收对象，不把授权推广至所有未来存档。

### 指纹筛选可用API，非祖先历史证明

DOC/triggers.log:3916–3921 any_scope_treaty、8833–8844 binds、11725–11732 is_historical_treaty，以及3747–3752 any_scope_article、10925–10931 has_type，可核对两国仍拥有历史条约和期望条款集合。它们支持窄筛选，但未查到按条约本地化name直接判身份的trigger；不要编造has_treaty_name。仅同一条约的历史flag及双方bind也不能证明玩家未重新协商其他内容，迁移时应保留它们。

## 5. 必要检查与边界

- 静态：关系方向QE1→PER；新增type=tributary；MOD最终subject_type覆盖仍允许recognized；防御条款只删除QE1/PER这一处；其他经济条款和第三国关系保持；新局标记与旧档effect幂等。
- 定向引擎/存档：新局两国rank、can_have_as_subject诊断、实际PER.overlord=QE1/subject_type、20%朝贡与影响力维护；次更新防御条款清理且其余条约条款不被整份撤销；两国市场/投资权是否仍满足原设计。
- 旧档：不处理第三国属国、不处理在战/博弈中、不处理已登记后合法独立；同一存档再load不重复；新局也不可被fallback二次创建pact。
- 前述人口报告仍为QE1直辖36州、39,713,582人口、35文化、65.46%主文化。PER改为朝贡仍不进入国内同化pop遍历与统一度分母，需通过subject体系单独观察。
- 状态：源码研究完成；最小diff尚由父任务实施；本报告未获得本轮ENGINE_PASS。
