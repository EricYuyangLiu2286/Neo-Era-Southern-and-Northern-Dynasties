# Spec 复审

2026-11-04，快照审查。Git 父提交 `b374be519fe71a7c8bfca48b18d94645b0151766`；实际比较独立基线 `backups/pre-change-regional-expansion-20261104T032336Z/mod` 与候选 `exports/regional-expansion-20261104-a`，不是已提交分支。命令：`git -c core.autocrlf=false diff --no-index B C`。游戏目录指纹核查为 1.13.11 / build 24799966、CURRENT、0 changed。

**确认问题：0。** 九个新增玩法文件与最终 `spec.md` 一致；未发现缺失要求、未经请求扩展或可据源码确认的错误实现。

- 对照“2/3升级计划不直接实现整套”：意大利/HUS/USM保留旧路线，扩充18名虚构候选和6名历史候选，区分原稿、现实史与拟议生涯；年龄、分期、全球唯一、死亡/流亡与组织接续齐备。小国方案明确印度/南洋实际对象、市场依赖与自主两路、旧政权与底层变革、动态宗主及退出；没有把方案写成已上线。
- 对照“累计12个条件合格月”“原生scripted_progress_bar是唯一进度写入者”：七国共享原生月进度，战争/就业不足不减已得月份；条件用自有州或国家所属建筑，75%边界、学校/军制与各国前置符合最终规格。PRU-origin允许同国NGF/GER延续；AUS使用曾进入的变量且排除仍活跃的匈牙利JE；TUR读取原生成功/失败共同终标。已抽读原版AUS、USA链核其含义。
- 对照“奖励只在成功事件选项执行一次”：成功票据与领取标记分离，选项和effect再验身份/存活/州数；失败、超时及失效封入口。修订后的archive只在身份失配时取消票据，重复JE失效不会吞掉合法成功奖励。迟答不重验就业，符合已经赢得成果的保留要求；奖励为60月国家修正，未触碰外国州。
- 对照“不覆盖地图/人口/制度历史”：差分只有7个独立脚本及中英2个本地化文件；未修改既有历史、人物或原版大链。研究中的旧候选数值及重试建议已由最终spec明确取代，不作为实现缺陷。

边界：这是源码Spec审查，未开游戏、未改脚本；71项AST子集测试不能证明引擎调度、UI显示或实际经济难度。原生bar回调时序、自动选项与同日JE回调优先级仍属引擎验证边界。主MOD合并、备份及Git保存由主任务收口，不以本报告声明已经完成。

最终窄范围复核：七个JE的失败条件改为`nesnd_rg_collapsed`后，内部仍仅判断`num_states < 2`；新增中英提示与终态行为相符。政体、宗主和公民称谓修订去除了条件未保证的断言，奖励和入口未扩展。USM方案已按既有代码纠正成都、襄阳、桂北及`add_radicals value=0.25`量纲。补充写作对读和实现来源文档符合上述边界，新增问题0，结论不变。
## 最终受审文件 SHA-256

| Path | SHA256 |
| --- | --- |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\common\journal_entries\nesnd_regional_development.txt | 9cdc67645ba34bca630d8c0b30149b2f9a7ba3d9fb4747bcec9b437270403e4d |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\common\on_actions\nesnd_regional_development.txt | e04cef95d04e631c39401c5c553c3db915940e03b36a454ec41b52d533952ec2 |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\common\scripted_effects\nesnd_regional_development.txt | e8592dd345bb74f325eb70753987b075e732e908e52149842f5d955c3af0250e |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\common\scripted_progress_bars\nesnd_regional_development.txt | edd38e5bbc992b1c1bdd621a6cff2e7e85f0f607f0f711e68c1b57f22885062c |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\common\scripted_triggers\nesnd_regional_development.txt | d5ad989cea56569da5aab1cc25947b0d239667051a71692f3d5de9db5a8a48d6 |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\common\static_modifiers\nesnd_regional_development.txt | 85f26af9b9c38d6e046f2214ac53951f5e3b43e36b898f09b035c8610383f297 |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\events\nesnd_regional_development.txt | 5735c23cf82f5c8a7747ebab3e6f272c40f7ab40e7cdbf847dfba7627ac66026 |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\localization\english\replace\zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_english.yml | 7f2dc57e80b35812a06004224559c17053bb9b948bef3c2b6b197971e365ac67 |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\regional-expansion-20261104-a\localization\simp_chinese\replace\zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_simp_chinese.yml | 764fb8168d759ecc429c1de0bdcc5a5cb44e738a90b4e70fc1a26cb05487354a |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\regional-expansion-20261104\spec.md | 9db30cc0a81aabbd540ea26359c98f7e002af7c5e3eb8915d33418c4fcb7460d |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\regional-expansion-20261104\italy-hus-usm-plan.md | 487ecd2a79a965cf9b65d0d2282a5e01a28ec987f20decd1d57c0d49d73c9388 |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\regional-expansion-20261104\small-state-survival-plan.md | 4b9817df3e79fddd7f90081805baf9e71a721739debf8f4723dd0247648ca3fa |
| D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\regional-expansion-20261104\seven-countries-source-design.md | 991655899e69cdc9865b69053fba018d947cba0b7f755d64985fa352769b9a72 |
| D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/regional-expansion-20261104/writing-comparison.md | ca956d5f13c793970a17706bc5943fec9e7f66f4e2ecf83ecca3ffcda919096f |
| D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/regional-expansion-20261104/implementation-sources.md | 2a63524b6721335a6b44d04f8d24f88155630da8cf5d64955c6cddfb9395787c |
