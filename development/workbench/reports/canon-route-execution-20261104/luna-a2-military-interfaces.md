# A2 两项原生接口核查（只读）

任务：查 formation 动态 count、capital target scope 与 general role trigger。配置：`gpt-6-luna / high`，由父任务显式委派并要求保持该配置。只读冻结候选、当前 GAME 与随本机 1.13.11 导出的 engine docs；不测试、不改脚本、不代替 root 裁定架构或军力数值。

## 结论速览

|问题|当前证据结论|可直接采用的边界|
|---|---|---|
|`create_military_formation.combat_unit.count` 能否用 `var:`/动态 script_value？|**未证实；文档和唯一找到的原生执行例均为字面整数 `5`。** 这不构成“引擎绝对拒绝动态值”的证明，但静态源码证据不足以把冻结版的 `count = var:...` 当成已支持接口。|若本轮不做针对性引擎验证，安全形状是按已计算军力分支，在 `create_military_formation` 内传固定数字字面值。保留参数动态用法则必须登记为待验证接口。|
|`set_capital` 的参数是州 scope 还是地区 scope？|**文档明确要求 state region。** 冻结版先在 `ordered_scope_state` 内转入 `state_region` scope 再保存，所以它的 saved scope 类型满足文档。|`state_region = { save_scope_as = target }` 后 `set_capital = scope:target` 是合乎文档类型的动态写法；直接保存 state scope 再传入则类型不符。文档支持目标类型，但没有找到本机原生脚本直接使用 `scope:...` 的 set_capital 实例，故该写法的引擎执行结果仍未实测。|
|`has_role = general` 是 `general` 类型的 alias 吗？|**没有这样的 alias 证据。** 文档将 `has_role` 定义为具体数据库 role，将 `has_role_of_type` 定义为 archetype；数据库 key 为 `character_role_general`，其 `type = general`。原生实例分别使用具体 key或 type trigger。|若目标是所有 general 类型，用 `has_role_of_type = general`；若目标仅是该数据库 role，用 `has_role = character_role_general`。冻结脚本的 `has_role = general` 没有对应 role DB key/原生查询实例，不应视作已证同义写法。`

## 1. Formation/count 完整证据链

- 冻结 A2 `common/scripted_effects/nesnd_native_khanate.txt:139–160`：army size 与 script values 计算 missing/quarter/artillery/infantry（140–145），按人口排序取州后构造 formation（146–157）；`combat_unit.count` 分别写 `var:nesnd_a2_cap_infantry`、`var:nesnd_a2_artillery`、`var:nesnd_a2_quarter`（152–156）。
- 冻结 A2 `common/scripted_effects/nesnd_american_restoration.txt:323–353`：先按 `nesnd_restoration_army_target` 算差额与兵种（324–334），然后两个分支 `create_military_formation`，`count` 使用 `var:nesnd_a2_infantry`、`var:nesnd_a2_artillery`、`var:nesnd_a2_secondary`（335–349）。这是当前具体待核写法。
- 当前引擎文档 `references/engine-docs-1.13.11-20261031/effects.log:959–981`：`create_military_formation` 的完整 grammar：country scope、`type=army/fleet`、`hq_region`、一个或多个 `combat_unit`、`type`、`service_type`、`state_region` 和 `count = 5`；文档没有说明 count 可用 `value = { ... }`、script value 或变量引用。
- 当前原生执行实例 G `events/soi_events/00_ep1_kazakh_events.txt:87–102`：Kenesary 事件在 `c:KAZ` context 新建 army；`hq_region = scope:kazakh_scope.capital.region`，两种 unit 的 state_region 从资本传入，count 两处均为固定 `5`。这证明具体原生建军链和静态 count 形状，**不证明动态 count 不可用**。
- A2 实施报告 `batch-a2-implementation.md:53–60` 也将“全部 ordered AST/宏展开/scope/value 动态闭包”“营数与实际 formation”列为待检查项；报告明确没有运行行为测试。这里沿用该未验证边界。
- 可审查替代写法：保留动态计算供分支判定，但在执行构建时使用若干可达 `if/else_if` 档位，每个分支的 `create_military_formation` 块写常量 `count = N`，其内部形状照搬上面 Kazakh 原生实例。不要把 effects 文档的示例外推为脚本 value 可接受。

## 2. set_capital 完整证据链

- 引擎文档 `effects.log:36800–36803`：`## set_capital`、说明“Set capital state in a country scope”、参数 `set_capital = X`，并明确“Where X is a state region”；支持 scope 为 country。
- 冻结 A2 `common/scripted_effects/nesnd_american_restoration.txt:222–224`：`ordered_scope_state` 选择人口最大的州；内部 `state_region = { save_scope_as = nesnd_restoration_capital }`，然后 country context 下 `set_capital = scope:nesnd_restoration_capital`。类型转换是明确的；前面的 existence guard 可挡无保存结果。
- 同文件 `296–303` 重定位原东道国首都：从 ordered state 中排除将割出的两块，在嵌套 `state_region` 里保存 `nesnd_restoration_host_capital`，country scope 设置 saved region。
- Native 常量实例可见 G `events/agitators_events/algeria_events.txt:939,974,1067`，以 `set_capital = STATE_ALGIERS` 指定命名州 region。此原生例证明常量 target，不直接验证动态 saved-scope 执行。
- 因此，`set_capital` 的 target 类型已由 engine docs 证明为 state region；冻结版把 `state_region` scope 保存后传值，接口方向正确。若代码将 `ordered_scope_state` 当前 `state` 直接 `save_scope_as` 后交给 `set_capital`，则不符合该参数类型。动态 saved scope 仍缺一次实际执行证据，文档/源码静态结论不得升级为 engine pass。

## 3. general 角色查询及数据库映射

- Engine `triggers.log:10746–10750`：`has_role` = “specific role”，grammar `has_role = role`，character scope；`10752–10756`：`has_role_of_type` = role archetype，grammar `has_role_of_type = archetype`，同为 character scope。
- DB G `common/character_roles/00_auto_assigned_roles.txt:37–47` 定义 `character_role_general`，其中 `type = general`；`50–60` 对 admiral 作同一模式。**DB role key 是 `character_role_general`，type 是 `general`；两字符串分别属于不同字段，不是数据库 alias。**
- 原生查询实际写法：G `common/scripted_effects/00_victoria_ep2_scripted_effects.txt:25–26` 用 `has_role = character_role_general` / `character_role_admiral` 查具体角色；多处事件如 G `events/agitators_events/algeria_events.txt:43,662,706,788,803` 用 `has_role_of_type = general` 查角色类型。
- `effects.log:64–68` 对 add_character_role 允许 `general/character_role_general`，但这仅是**赋角色**效果语法，不证明 `has_role = general` 是有效查询别名。冻结 A2 两个脚本 `nesnd_native_khanate.txt:134`（随机角色筛选）和 `nesnd_american_restoration.txt:43,174,178` 用 `has_role = general`；改读写时按目标意图改为上述两种查询之一，并避免把任何其他角色 key 扩成通用 general type。

## 来源 SHA-256

|对象|相对路径/路径|SHA-256|
|---|---|---|
|冻结 A2 建汗国|`backups/batch-a2-frozen-owned-20261104/common/scripted_effects/nesnd_native_khanate.txt`|`355A26BABE45D6DE581385BC3856F976644C549541AD55526E195606EC0BFFE0`|
|冻结 A2 美洲复国|`backups/batch-a2-frozen-owned-20261104/common/scripted_effects/nesnd_american_restoration.txt`|`C96F3E1C3D0D1F2A9CC9C8B3D949E6AF5842669B0C805F327CA6C6EDA557E22C`|
|A2 实施报告|`reports/canon-route-execution-20261104/batch-a2-implementation.md`|`4E937B67D52E49FD40D237ECF7F18777C44D7239FAD35FFF3F22C7F70A1D1214`|
|当前原生 Kazakh formation|`GAME/events/soi_events/00_ep1_kazakh_events.txt`|`588DEA97463EF633E6A29812507CED11501419A733C5CC256D357B9A7A2635C5`|
|当前原生 set capital 示例|`GAME/events/agitators_events/algeria_events.txt`|`A97DC3D27072FA07E099178997B7C2821ADDE09E46124C6EA7760E292C9D422B`|
|general/admiral 角色 DB|`GAME/common/character_roles/00_auto_assigned_roles.txt`|`7C53B49F0F79AC683811B3D5F5085197915F18DE00864DF8DC3873935CE49763`|
|角色写入原生实例|`GAME/common/scripted_effects/00_victoria_ep2_scripted_effects.txt`|`5EB6DCA67E7647B4D09DBEB1C22E0AB2B68CEE66C04A7476375C581F074191DC`|
|本机 effects docs 1.13.11|`references/engine-docs-1.13.11-20261031/effects.log`|`24E7AF8C1F338DEA727E256C862A915F92260E22FA740A98A896738D3B4668E1`|
|本机 triggers docs 1.13.11|`references/engine-docs-1.13.11-20261031/triggers.log`|`AD323401EAD8B74C6BCA34C147CE37FCEA0F5DFF98D4993F22D412D1AA31F94E`|

GAME=`D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`; WORK=`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`.
