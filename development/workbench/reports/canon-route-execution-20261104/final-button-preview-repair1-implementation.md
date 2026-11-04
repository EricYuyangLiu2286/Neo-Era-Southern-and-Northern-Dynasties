# 最终显示修复 repair1：READY_FOR_TEST

已集中修复 FBP-F01、WR-01、WR-02，停止编辑。配置沿root明确委派 **gpt-6.1-sol / medium**；本轮是编辑，不是独立复测。主MOD与游戏源码只读，未开游戏。

## 冻结对象

- pre-change：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\pre-change-final-button-preview-repair1-20261104T194132Z\mod`
- 新owned freeze：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\final-button-preview-repair1-owned-freeze-20261104T194559Z\mod`（8份既有文件，无新增文件）
- 新完整snapshot：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\final-button-preview-repair1-20261104T194559Z\mod`（1015份）
- manifest：`R/final-button-preview-repair1-freeze.json`；全部SHA齐备，旧192525冻结保留。

## FBP-F01：新承诺使用当前价，旧承诺显示锁定价

root裁定的共同合同是：`has_quote AND (active OR corresponding expense still applied)`。10项目和compact的11个display_quote只读函数在该条件为真时才读已存quote，否则返回原weekly_quote。读取旧变量仍处于真正has_variable分支内。27按钮显式传入实际category active变量；项目锁定提示if与对应SV if、compact双方提示if与compact SV if构造期保序AST逐一相同。没有以某州已有地方修正代替本国承诺状态。

未承诺分支仅保留原生费用preview，显示当前金额和12月，不同处再列相同金额TT。10种current_quote TT（20中英值）及27个相应无用参数删除。已承诺分支仅给简短锁定报价文字，注明原支付期12月；不重复add_modifier费用预览，不暗示重启付款。地方24月、IG12月的原生预览与必要既存修正fallback仍原样，fallback只陈述数值/原期限，不擅称不可再次开办。

双边 `.10.a/.11.a` 各国独立决定commitment，未承诺时native multiplier在其本国scope求值；已承诺时事件root用ROOT，伙伴用明确saved sender/partner。两个聚合报价TT改为各自伙伴的锁定价TT，另加一对root锁定价TT。真实双方/serial存在及原eligibility body保护保持，不让嵌套peer误用ROOT读取同一国家。

`final-button-preview-repair1-red-example-map.json` 逐条映射独立原27个retarget与2个二次compact红例：无active/expense但留quote100时，预期新显示采用真实新交易价（项目800；compact LOM800/SAR400），而非历史100。它是基于原独立记录的修复期待映射，**本轮未执行这29条测试，也未标PASS**。

## WR-01/02：仅精确位置的当前主体修正

共10个中英已有值窄改。Italy共用工程结句只说明政府优先照顾哪些需要，Bellandi唯一后续选项只承认女校需求；LOM法国扶持历史、Bellandi个人共和观点均保留。HUS指定的transport/citizenship/oil、Shen后续当前主体改本国/政府；英文已经中立的transport/citizenship正文原字节片段保留。正式国号、历史叙述没有全局替换。

四本地化共36键变动：14既有值改写（10WR+4compact伙伴价），20废弃current_quote值删除，2个root锁定价值新增。逐键前后文、问题ID及SHA见 `final-button-preview-repair1-locale-changes.json`；中英对读见 `final-button-preview-repair1-writing-comparison.md/json`。

上一轮342条文稿：278逐字保留，54仅维持此前已批准共同尾巴删减，10仅本轮WR精确修正；无其他回退。人物两文件各只改 `.102.a` 和 `.108.d`。

## 真实payload与数值保持

修改文件内53个原hidden_effect保序AST一致；51个原玩法script_value保序AST一致；预览helper的12个native effect payload AST也一致（只调整其显示分支）。207份既有真实effect/modifier/trigger文件逐字节SHA一致；owned以外1007文件逐字节SHA一致。真实start、retarget、pay、cleanup、DB、recipient、期限、奖励receipt和AI不变。证据 `final-button-preview-repair1-payload-equivalence.json`。

8owned全UTF8 BOM；新freeze与候选文件SHA相同。构造期只做源码parse、AST保留/guard形状对照、双语逐键阅读和SHA收集，不执行行为或工具测试。

后续独立Sol需重跑29原红例并完成先前未跑矩阵：无quote/旧quote、active或expense独立成立/均失效、GDP变化、目标缺失/失主、既存地方/政治modifier、双边不等报价与对象缺失、B2/A2/C1保持；两WR用SIC/PAP与合法君主制HUS反例复核。动态文字及真实悬浮渲染仍ENGINE_NOT_RUN。

Diff SHA：`70b6b3857526e316cac0c1c73b2e6578b368d6271281eb1ddc703fe0105ca066`。作者工具留WORK，不进入MOD。
