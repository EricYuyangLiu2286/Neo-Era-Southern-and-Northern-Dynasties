# 最终按钮显示修复：READY_FOR_TEST

执行者 `/root/sol_c1_frozen_validation`，沿 root 明确配置 **gpt-6.1-sol / medium**。本轮为获批显示编辑，不能作为自己的独立审查者。编辑已停止；所有旧freeze保留。

本批只修改15份owned：14既有文件和1个独立预览helper。完整冻结1015文件。主MOD、历史人口、本体源码均未编辑；没有启动游戏、行为矩阵、Tiger或MCP。

## 固定对象

- pre-change：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\pre-change-final-button-preview-20261104T191826Z\mod`
- owned freeze：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\final-button-preview-owned-freeze-20261104T192525Z\mod`
- full snapshot：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\validation\snapshots\final-button-preview-20261104T192525Z\mod`
- manifest：`R/final-button-preview-freeze.json`，含15owned及1015完整SHA。
- 当前1.13.11/build24799966，计划源链catalog CURRENT、changed0。原版按钮→JE调用→数据库→引擎导出依据在 `final-button-preview-source-chain.json`，未捏造GUI API。

## 实际修改

C2 27项目按钮调用只读预览helper，传入全部完整字面参数，不用未证实的参数后缀拼接。实际存在option_target的if body后再分支验证owner与原candidate，才显示目标名、国家12月费用、实际目标州24月地方修正及本国12月IG修正。不依赖start写出的category_target/provider/choice/baseline。地方/政治已有同名modifier时，以按真实数据库值复用的5种地方、7种IG组合提示补足原生可能去重的反馈，负值也列出。

10类别+compact共11个只读display_quote：初值为现有weekly_quote，仅has_variable实际if body读取已存quote；费用函数、GDP系数、round/clamp25..2500和实际支付完全未改。27按钮区分当前起办报价与本期锁定报价。双边 `.10.a/.11.a` 各展示两国自己的12月开支；金额native multiplier在各country求值，动态TT仅在事件root显示一次，分别显式读取saved sender或saved partner，避免ROOT误读成同一个国家。两国及serial必须实际存在，再过原accept/confirm资格分支。

B2 specialise加既有12月修正原生预览。own_market只有真实拥有市场、外层互斥合格、无违约、收入足报价且无公共投入时显示真正可能启动的12月费用与服务；原空modifier与请求过程未改。运动已有明确成本TT仅补权重±15%、适格支持人物人气+10/12月，不新增人物。

A2 recognise仅即时自行复统分支预览120月修正；既有TWT合并申请分支不显示立即领奖。suppress原提示补准：迁徙后本国剩余原住民人口15%转为激进派；仅实际接纳迁民的目的地州迁徙吸引+25%/60月。没有把州效果写成整个接纳国效果，没有把人口份额误写成相对既有激进派增长。

C1 `.1.a` 只在双方/serial/kind/政制快照实际存在并通过原reply/eligibility的分支，显示kind2/3/5在实际承诺/协议生效后的sender支持；kind2/5沿原一次性receipt条件显示60月投资奖励，kind3按原72月政治信用，原首次成功关系+25也仅在原receipt未持有时预览。先写清条件结果，未把申请/投资权利说成现成工厂；真实accept、后验、recipient和receipt均原样。

## 文案与玩法保持对照

- 8本地化共142个编辑/新增值：60既有值（54条中英项目desc只去共同尾巴、6条中英精确效果TT）、82新增值（41双语对）。`final-button-preview-locale-changes.json` 逐键保存前后文及源SHA。
- 之前final_standards的342条改稿：288条逐字保留，54条只去重复财政/期限/三月尾巴，具体行动逐字保留；两人物本地化文件字节SHA保留。详见 `final-button-preview-writing-comparison.md/json`。
- 修改脚本中78个既有hidden_effect保序AST完全一致；51个既有script_value AST一致；207份既有effect/modifier/trigger文件逐字节SHA一致；owned以外1000文件逐字节SHA一致。新增helper中有实际数值效果的12个原生节点全部包在show_as_tooltip，B2 specialise新增节点亦直接包在show_as_tooltip。没有新增真实变量写入/奖励/收费/外交事件。证据 `final-button-preview-payload-equivalence.json`。
- 全15owned UTF8 BOM。新增helper仅MODscript；作者工具及报告留WORK，不入正式包。

## 后续独立验证边界

本轮仅做作者构造期parse、源码/双语阅读、上述AST保留对照与冻结SHA，不运行行为或工具验证。独立Sol应覆盖27目标缺失/失主/不合candidate/有效、无quote与已存quote/GDP变化、同名费用/州/政治修正已生效、双边不同GDP/缺参与者或serial/迟答，及所有获批B2/A2/C1条件与receipt保持。预览须无写；native文字/动态TT/已生效modifier实际悬浮渲染仍属ENGINE_NOT_RUN，不能因源码同形宣称游戏内已验。

diff：`R/final-button-preview.diff`；SHA `d0dcca149a2ed667e3ae880180734fd9134eb661e601d02009e7790b70df7536`。源码现在停在新freeze，等待独立测试。
