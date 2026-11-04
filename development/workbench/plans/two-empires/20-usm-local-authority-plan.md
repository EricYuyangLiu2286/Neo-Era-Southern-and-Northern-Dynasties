# 南朝旧勋贵：国家与地方修正分离

父 `exports/cne-local-modifier-20261031-b`；独立候选 `exports/usm-local-authority-20261031-a`。父/D/主MOD/活动run只读。

## 作者证据与错误

pre-update `.3`《摸着石头过河》讲政治家延缓帝国瓦解后遗留的地方政治抵抗；修正 `USM_conflict_invalid` 作者名为“前明勋贵势力”。作者一方面给整个国家15年递减修正（authority −20%、全国州税收浪费 +5%），另一方面从本国拥有的湖广地区选一州，再挂20年递减的同一修正。

国家调用是合法的，并且只执行一次；州调用里的 country_authority_mult 则不流向国家。不能简单删除整个修正，也不能把该州惩罚改成再给国家挂一次，尤其不能每州添加一份全国 authority 惩罚。

## 具体修复

1. 完整保留现有国家 modifier 定义与国家15年递减调用，保证原有全国取舍不变。
2. 仅地方调用改成独立 `nesnd_usm_old_guard_local`：`state_tax_waste_add=0.05` 原有当地税收流失保留；用 `state_turmoil_effects_mult=0.2` 表达地方统治受阻时既有动乱的额外损害，持续20年递减原样。
3. 地方效果加实际仍归 root 的检查，避免打开事件后转属时把该次中央妥协的地区修正落到新所有者。
4. 新标题引用 `$USM_conflict_invalid$`，保留作者名词；不重写事件正文、风味引文或选项标题。

这是修复地方治理代价的设计替代，不宣称 +20%动乱效果等于 −20%国家authority。没有动乱时该新增项不会凭空制造动乱或激进派；地方仍有 +5%税收浪费，国家原有全国 +5%也保留。不会把平静地区强行推入内战，不改全国官署或开局数值。

## 当前语法/尺度依据

- engine-docs modifiers.log `country_authority_mult` Mask country；`state_turmoil_effects_mult` 1951–1954 Mask state，改变既有动乱的地区惩罚。
- GAME `common/static_modifiers/00_ip2_02_modifiers.txt:249–251` mob_violence_modifier 用 +0.20；`agitators_4_modifiers.txt:348–350` modifier_legacy_of_democratic_rule_state 用 +0.2，`modifier_national_discontent` 亦同量级。当前原版提供实际量级，不从失效国家项的数字推导等价。
- 原有该湖广州调用仅一处；所有 `USM_conflict_invalid` 定义/使用已全项目检索。CNE 的查帮会州修复父B原样保留。

## 验证

静态逐节点验证：国家调用和原 modifier 字节不变，仅单个州调用名称与owner guard改变；两个新增语言key齐全，UTF-8 BOM，Tiger关于USM scope warning应消失。

引擎：从USM实际国家进入该结局前保存基线；触发真实`.3`后检查国家authority只新增一份原有15年递减，目标本国湖广州得到20年递减新修正，其他州没有附加当地修正；没有湖广或事件展开后州易主时不授予local项；推进时间与读回确认逐渐衰减。若目标州动乱为零，只核实modifier和税收浪费，不伪称测到动乱收益；持续影响需另行有实际动乱的可达场景对比。

## 交付状态

候选已冻结，390文件。修改前备份 `backups/pre-change-usm-local-authority-base-20261031T161357Z/mod`；候选备份 `backups/candidate-usm-local-authority-a-20261031T161514Z/mod`。相对直接父 CNE B 仅5文件变化（event、独立modifier、两语新增key、metadata），完整哈希在 `evidence/usm-local-authority-a-static.json`，可用 D→本候选累积合并以保留前置 UI A/CNE B。

Tiger 0 error，warning 634→633，USM modifier作用域警告消失；本候选剩余报告中没有 confidence=strong 的 scope/target/effect/trigger/modifier 作用域错误，也没有其他 modifiers-flow 项。未因此泛改原版或旧文本警告。此结论仅限 Tiger 当前静态模型，不能取代引擎运行与逐分支验证。
