# CNE 妥协修正只保留一个实例

父版：opium-target-scope-20261031-a（包含冻结 E 的三地图、事件反馈及 scope 修复）。独立候选 cne-compromise-refresh-20261031-a；不改冻结版/主 MOD/活动 QA。

## 实际问题与范围

原生 run153444 的 Nov15→Nov21 存档显示 nesnd_land_compromise 同时存在两条：.30b 委托议局的60月实例，及 .32a 冻结的120月实例。该顺序是正常可达路线，不能以累计 QA 为由排除。修正包含税收能力和权威各−5%，相同实例会造成额外叠加；根代理 UI 观察权威进一步下降也与之相符，但不拿整个国家预算变动作为纯因果。

设计为一次制度性妥协的延续：.30b 施加60月；冻结/瓦解时改为从当日持续120月，强度仍各−5%。清除旧同名实例后新增当前期限，保留作者叙事、现有变量变化、事件顺序及其他修正。

## 依赖图与实现

nesnd_crisis.30b → nesnd_land_choice_30_b → remove/add compromise60

nesnd_crisis.32a/31b/其他冻结入口 → nesnd_land_freeze → cleanup → remove/add compromise120

nesnd_land_fracture（实际瓦解分支）→ cleanup → remove/add compromise120

只修改 common/scripted_effects/nesnd_land_choices.txt 与 nesnd_crisis_effects.txt 的三个既有 add 调用，全部增加同名 remove。国家 scope 已由既有调用确定；不创建新国家/人口/法律/文案。当前原版 events/japan_events/ep2_tenpo_events.txt:627–633 有同名 remove_modifier 后 add_modifier 刷新实例。

## 验证与边界

修改前独立备份；AST 验证新候选移除三个新增 remove 节点后与父版逐值一致；其他文件哈希不变；Tiger 检查两文件，仍不得声称真实验收。

实际游戏：真实CNE活动改革→.30b→查看单60月修正→.32a→查看单120月修正；保存并核对 timed_modifiers 仅一个同名实例，旧60月已消失，其他修正不变。关闭JE后跨12月1日，月数/样本不再增加，再读档保持关闭。既有双实例旧档修复必须再次经过合法刷新入口；此候选不无条件遍历存档补偿历史。
