# 印度修订2复核

2026-11-02；范围：印度方案第十—十四节与共享生命周期。**DESIGN_REVIEW / ENGINE_NOT_RUN**；只读审查，未改方案或玩法。以下是设计闭包问题，不是已复现游戏BUG。L23“建国/转地部分成功但博弈失败”和直接宗主约束由主任务补充，本报告不重复列为待修项。

## 结论

用户新增要求均已进入设计：逐州策动南印度起义；独立 **OR** 足够能力（含仍朝贡法国的MUG秘密组织）；土邦自己的独立/属国分路；MUG、USM、FRA分别参与；地方胜利不自动归MUG；法国现行政体/王朝影响政策。没有发现必须推翻方案的来源事实错误。下列两处需要在实施前明确，才能避免日志提前清理或永久悬挂。

## 需要明确的两项退出

1. **[P2] “筹备成熟”不能直接等同地区联络JE的终局成功。** 逐项结算表把地区联络成功写成“筹备成熟进入发难窗口”，而按钮方案仍让玩家在其后选择最终发难；共享流程又要求父JE终局立即关闭子项、维护费与临时效果。如果成熟使当前JE完成并清理，发难按钮及已准备的组织状态可能先消失。建议把成熟标为进行中的“待发难阶段”，继续适用维护/衰减/放弃规则；只有发动被确认且必要状态完整移交战争案件后，联络阶段才完成。若另建待发难JE，须明确同一次身份、进度和地方对象先移交再清旧项。依据：[印度逐项结算](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:188>)、[发难按钮](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:127>)、[共享收尾规则](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-india-lifecycle.md:40>)。

2. **[P2] “没有合格目标→暂停”需要区分临时无目标与对USM行动已终结。** 方案末尾规定无合格州显示无目标并暂停；但若USM已永久失去全部候选领土、当地均已解放，或地区全部转归第三国，这条持续JE会没有可再进入的目标。共享生命周期已有永久失去适用对象应失效的原则，需落实到此JE：停战/当前实力不足/准备条件暂失→暂停；全部预定目标已实现当地自主→完成并进入后继；全部第三国接收或USM灭亡且未实现本案目标→按真实结果失效/转段，清待答与未来维护费，既有战争独立结算。不得自动把对USM的授权改成对FRA等新所有者发动。依据：[无目标规则](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:192>)、[USM目标资格](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:143>)、[永久失效规则](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-india-lifecycle.md:35>)。

## 来源核对与实施注意

- 47个本地所有者中4个decentralized、43个有组织国家；TRA是USM puppet，其余42个有效开局历史未配置宗属；MUG是FRA tributary。第十一节准确限定为开局脚本事实，未冒充实机关系。逐TAG表和完整SHA见 [诸邦来源报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/india-princes-uprising.md:1>)。
- 波兰提供逐州请求/迟答/外交博弈闭环；CNE提供州所有权改变后的清理。方案正确将这些与建国起义区分，并排除了BIC→USM直接替换、重复创建现存TAG、默认反叛者归赞助国以及原版Sepoy的无条件吞并预设。
- **非阻断澄清：** 第十节的“殖民关系”不应以 `is_incorporated = no` 或USM属国关系代替。CIRCARS、MYSORE、MADRAS及TRAVANCORE的USM部分没有显式 `unincorporated`，却正是要求支持的直接领土。推荐以已核定地区集合＋当前owner-state＋本案政治条件判定；整合状态可影响难度，不能悄然剔除目标。源：[CIRCARS](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4123>)、[MYSORE](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4174>)、[MADRAS](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4203>)、[TRAVANCORE](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4187>)。
- “共用一套土邦主JE”建议在实现规格写明**同一country-context定义、各国独立实例**；只有具体起义案件的国际结果采用唯一执行者。不可把波兰全印度唯一global终局套在各土邦自身议程上。当前文本没有要求共享同一个实例，因此本项不是来源错误。
- 法国分类先现行法律、后实际在位王朝；历史标记不抢占当前政体，援助权重明确是提案，条约 `binding_period` 未被误写为自动到期。与 [法国研究](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/france-regime-policy.md:1>)的事实/提案边界一致。没有新增固定军力、GDP、免费人口或免费海军参数。

## 本次读取指纹

|文件|SHA-256|
|---|---|
|印度方案|`adc4aea2e5b7d5ce94da210ccd1d458af6f3f647bb930b7b6ca3eb17877e96b2`|
|共享生命周期|`c4d5786f40c33df7b557bbcb841e1893982a8aab6b4a55829978f97c363a9cc1`|
|主MOD州历史|`a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`|

以上指纹对应本次读取；主任务正在并行补充L23等，后续文本变化应以重新核对为准。本轮没有引擎证据，也不宣称已完成玩法验收。
