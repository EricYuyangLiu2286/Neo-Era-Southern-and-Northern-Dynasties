# Run 143454 实际引擎错误修复

状态：实现中；父候选 integrated-gameplay-20261031-a，只编辑独立候选。

## 原因与范围
CNE Jan27 土地改革日志状态中的民生统计悬停，每帧四项 ROOT.GetCountry.MakeScope 读取丢失 Container，另带总体本地化失败；日志轮转严重。依赖链为 ce_cne_land_reform → status_desc → nesnd_land_rules_link → GetTooltipTag 提供 Country 对象 → nesnd_land_rules → Country.MakeScope.Var → 每月统计 effect。只改悬停正文数据根，不去掉动态数据，不更改经济指标、叙事或玩家路线。

当前原版 localization/english/content_204_l_english.yml:787—788 和 agitators_4_l_english.yml:1473、1478 同模式证明自定义 Country 标签的内层使用 Country.MakeScope.Var，外层事件/日志 ROOT 上下文不能自动继承。

## 冷启动归因
先归档所有 error*.log。与 run134533、纯原版 run022323 比较同组，剔除 QA 空 ConsoleWindow 污染，不按总数相减。已交付 supply-scope-fix-b 的3处关系表达式不重复修改。遗留未设置变量、未触发事件、依赖资源重名、无效 rivalry 分别溯源；不能用伪 setter 或激活废弃事件消除警告。只有能证明语义与当前接口的问题进入补丁。

## 验证
独立完整备份父候选；仅允许经过确证的文件差异；本地化 BOM、键与动态函数校验、Tiger仅辅助。根代理冷启动新冻结版，CNE进入游戏自然或实际触发 flavorCNE.1，开JE后悬停民生统计至少5秒；四项值应显示且 error*.log 无9组重复。推进一月后四项显示与存档变量一致；退出重开/读档再次悬停；切换HUS等国不应污染CNE统计。新增冷错误和原有警告分列。

## 不确定性
本补丁未做真实引擎回归；原版样例是接口依据而非验收。人口、地图、资金、条约、原版/工坊资产和活动QA不改。

## 已确证的南服统治终止缺口

`ce_usm_ruling_of_nanfu.fail.custom_tooltip` 使用 ce_usm_conflict_fail，该变量没有任何写入。修改前作者 `ce_usm_events_l_simp_chinese.yml:111` 明定此失败为“吴明论战无效（不再是君主制）”，主JE现有 invalid 也已经直接检查君主制。独立B将南服JE失败条件直接改为 NOT has_law_or_variant=law_monarchy，保留原tooltip和 nanfu_ruling_je_ended 收尾，没有伪造变量、调整国体或改其他剧情。与现有君主仍在但属国流失的 looming invalid 路线区分。

真实验证：USM仍君主、两个JE活动时不应失败；同样存档实际变为共和国后两JE应正确收尾、全局nanfu_ruling_je_ended写入，临时while_active修正撤除，读档不重复；吴朝禅代原complete路线和原looming invalid路线仍需检查。纯静态AST证明仅这个fail条件变动，不证明事件执行顺序。

当前状态：A与B均已冻结、静态核验、完整candidate备份；报告evidence/runtime-143454-error-remediation.md。真实引擎回归由根代理下一run实施。
