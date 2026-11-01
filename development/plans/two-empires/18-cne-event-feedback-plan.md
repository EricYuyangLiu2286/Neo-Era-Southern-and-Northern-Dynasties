# CNE 事件机制提示与地图位置修补

2026-10-31；父版本 `exports/integrated-gameplay-20261031-d`。候选 `exports/cne-event-feedback-20261031-a`。仅修机制 UI，作者叙事、人物、国家历史、地图经济不在此分支修改。

## 证据与问题

- 实机 run153444：flavorCNE.4/.5 的失序变量确实变化，但选项悬停没有显示；普通 `change_variable` 不产生面向玩家的指标说明。
- flavorCNE.6 正文引用随机州，事件 placement 却是 root（首都），导致河南副标题与吉林正文同时出现。
- `.6.1`“只是将涉事官吏调离岗位”在 `backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml` 是作者原文，保持不变。
- 当前 GAME `events/autocracy_events.txt` 的 autocracy.2 在 immediate 随机州保存 scope，然后 `placement = scope:secret_societies_state`。这是当前有效实例，不增加虚构 location 字段。
- 当前 GAME `events/assassination_events.txt` 141–146 用 custom_tooltip 配合 change_variable 明示进度。

## 依赖图与实施

`flavorCNE.4–8 immediate 随机州 → 保存州/IG scope → placement/正文 → 选项的原有 scope/owner/reform_active guards → progress/disorder → after refresh → 两条 JE bar`

`nesnd_crisis.30–33 选项 → nesnd_land_choice_* → 原有 active/local_crisis guards → 数值/冻结/解体效果 → 显示刷新`

`JE 按钮 → nesnd_cne_reform scripted effects → 风险变化/冷却 → JE 提示`

1. 修改前完整独立备份；复制 D 创建独立候选。
2. 逐项核对五个事件、petition/local crisis/终止路线和改革按钮；在实际执行条件之内显示有色 custom_tooltip，不因停办改革或失去州而虚报本地后果。
3. 五个地方事件 placement 使用各自 immediate 已保存的州。保留国家根作用域、IG 作用域与地方 owner guard。
4. 新机制文字使用独立本地化；数字、正负颜色和 clamp 的边界需与代码一致。原有 progress 名称错误已被 D override 修正，避免重复键覆写作者叙事。
5. 不把未发生的起义或未来人物保证写成既定后果。没有变量改变的按钮/维持路线也不能编造奖励。

## 验证与未完成项

- 静态：所有 changed Jomini 文件 parse；新 key 两语言对齐；机制 AST 删除新增 tooltip 后与父完全一致；仅五个 placement 允许变化；原作者叙事文件 SHA 不变。
- 实机必须由 root 新冻结版本测试：.4–8 每个选项悬停，至少 .6 比对事件副标题/正文随机州/地图卷轴位置；petition 三选项、local crisis 两选项、停办与继续路线；数值在 0/100 边界及 inactive 改革不得产生假效果；每次操作前后 error.log 增量归档。
- 候选只可标静态已检，不能标游戏内已验证。所有人名、角色生成/转移/存活逻辑保持父版本。

## 并行地图二进制合并

CA 3169、海南 3170、湄公 3171 的 primary hub IDs 可分别固定；从相同 D 派生的中间 anchor/strip 数字会碰撞。各分支必须交 typed delta（source SHA、完整 added/removed/changed before/after）后统一编号，或在合并地理上重新生成路径。禁止最后一个 splnet 文件覆盖其他分支。
