from integrity_context import *
from datetime import datetime,timezone

def save_before(p):
 q=R/'skill-before'/p.name
 if not q.exists():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
def append(p,s):save_before(p);write(p,read(p).rstrip()+'\n\n'+s.strip()+'\n')

append(S/'references/validation.md','''## 编辑器报红与源码闭包（CWTools 0.10.31实证）

遇到“自定义trigger is unexpected / CW262”，先查有效数据库定义、完整括号和实际调用，再以安装的语言服务器冷启动复核。仅看定义存在不能证明工具索引正常；仅看红线也不能认定游戏脚本无效。本轮CNE两个福利trigger在同文件250/253有定义，冷加载无对应诊断；独立全MOD反例删除这两定义后准确产生两个CW262。源码保持，编辑器可重载规则/窗口以刷新索引，不能删除有效判定迁就缓存。
LSP初始空诊断不是最终通过：等待规则重建及后续文件诊断，URI比较先统一百分号编码。引用检查要有已运行的缺定义反例。证据与可复用探测工具在 WORK/reports/integrity-recheck-20261102/cwtools-*.json、WORK/tools/probe_cwtools_integrity.py；它只启动语言服务器，缓存与反例在WORK，不改用户IDE配置、不启动游戏。
''')
append(S/'references/syntax-and-routing.md','''## 人物、日志局部scope及重复字段

角色当前IG由 `owner.ig:...` 取得；`ig:`只支持country/political_movement，不能直接从character调用。人物转国后应指向转国后的owner。比较法律对象时两端均用law；只有明确比较law_type才取`.type`。JE在immediate保存的事件链scope不自动成为全局AI法案评估scope；固定法案目标可直接比较当前law的type。
同一事件的cancellation_trigger只定义一次，按完整OR语义合并所有取消理由；缺对象先分支判定，再检查人物存活。避免将原本可重复的option/modifier与本应单一的条件字段混为一类。全局on_action调用country效果时不要把全局root当当前country，需在country入口明确保存行动者。
以上修正以1.13.11 event_targets/effects及原版调用链查证，26处人物IG、Donghak三scope、法国取消条件的定位见 WORK/reports/integrity-recheck-20261102/tiger-source-review.json。
''')
append(S/'references/content-development.md','''## 新生国家的人口与战争闭包

每条create_country路径在创建分支内清旧seed，选择实际所有且state_population>0的州，再检查seed存在；无有效人口时跳过新TAG，不造人口。既有国家仍可接收空地区。军事准备放在全部领土转移后，按全国及驻地人口核最大兵员比例；继承军队非零时不额外赠兵，零赠兵也记一次准备完成。只明确补所选兵种必需科技，不能假定origin完整复制科技。
人口转换前先恢复异常临时文化批次，再划出本次半数；新遍历转换宗教和文化。与原作者华夏转换、原版部分文化/宗教转换使用相同原生接口；无删人口或补人口动作，实际split/merge可见性仍需引擎证据。
战争目标逐方、逐参战国审计。一个联盟共同羞辱同一目标时，原版humiliation使用validate_conflicts_war_goals_all，不堆重复羞辱。防守国可分别要求吞并每个不同对手；后加入者既要入战，也要补对应目标。join_war后以实际war参与者验证资格，外交阶段才使用DP参与者列表，配合一次锁与期限。来源、人口分档和边界案例见 WORK/reports/integrity-recheck-20261102/qin-latest-source-audit.md。
''')
writing=S.parent/'nesnd-player-writing/references/author-samples.md'
append(writing,'''## 英文玩家文本

英文槽中的中文回退不能记作完成英译。英文修订先核作者世界专名，再读当前原版同类JE/事件，以自然英文表达人物、制度、行动和代价；精确保留动态scope、概念、颜色和实际数值。把“elapsed-time guard”“preparation snapshot”“monthly calculations”改为玩家可理解的等待期、准备状况和改革效果。未发生剧情的日期与结局不写进无条件常驻说明；删除预测须人工记录，不能靠数值token相等判定文意完整。2026-11-02已对读20条原文、逐项审查720键，见 WORK/reports/integrity-recheck-20261102/english/editorial-comparison.md。
''')

write(R/'release-notes.md','''# 代码完整性复查与西秦修正

父版本870639a；独立候选integrity-recheck-20261102-a。用户授权外部复查、修复并合入；未开游戏。实际合入/备份/远端以main-merge.json、git-delivery.json为准。旧交付证据保留，本报告取代本轮修改处的旧行为说明。

## Standards

截图中的两个CNE福利trigger都存在且唯一，调用链正确。已实际运行CWTools：冷加载源码不出现这两条CW262，独立删除定义反例准确产生两条相同诊断。说明磁盘代码完整，编辑器当前红线更可能来自未刷新索引或未保存状态；未修改有效触发条件，也未改变用户IDE配置。

全分类源码解析覆盖75类、447个活动txt文件；字面引用、生产/资源、固定人口、地图/海域、MCP检查独立执行。修复26处人物IG目标scope、全局法案评估借用JE局部scope的三处引用及一处law/law_type错比；合并法国事件重复的取消条件。7条波兰英文缺键补齐。英文720键逐项审查，281条修改/补入，西秦波斯205键全部保持动态表达式与含义。

本轮未为凑零告警改动原版AI权重或国旗设计。Tiger剩余的3个缺CoA定义（5处引用，BUN_subject/JAP_theocracy/TSW）、其他历史缺本地化、原版Russia无效分支，以及工具版本/作用域规则差异均单列在tiger-source-review与global-final报告；这些未被伪装为已修复。全局历史/语义登记仍有旧来源指纹，不把旧的NOT_RUN自动转通过；重新审查结论见semantic-reclassification。

## Spec

- 解体战争采用共同羞辱诉求；西秦反向吞并各参战国，后加入联盟者补齐吞并目标。原版禁止同目标的重复羞辱，所以不叠加16次羞辱。秦国内部权争仍维持双方吞并。
- 7条漏接的新国家分支补齐参战入口；全部16条新生分支共用90天窗口及一次性准备。7条对应既有国家的领土接收分支AST保持，未强令既存波斯/西藏等宣战。
- 17条建国种子路径清除旧scope、选人口最多且人口>0的实际州，无合格州则跳过。空地区仍可转给既有国家；不创建空壳人口国家，不补造人口。
- 新生军队在领土转移后准备，明确给予线列步兵与火炮科技；已有军队不叠加。全国及首都人口同时达到5万/10万/20万/40万时，分别最多补1/2/4/8营；低于5万不赠营。最大编制兵员不超过两项人口基数的2%，实际招募仍由游戏决定。零营、继承军队两种结果也写一次锁，不能重试刷兵。
- 文化复归采用与原作者华夏转换相同的change_pop_culture原生接口；先清理异常残留，再标记半数汉羌、整批换信仰、整批换文化。没有删人口指令。原版36地区人口均为正，但部分复国地人口很少：Sistan仅16012、Tuva49000，因此原来统一八营确不合理。
- 西秦/波斯只有两条custom_tooltip用于原生无法单独显示的SoL单向额外奖励。条件继续由原生trigger展开，持续变化由原生进度条显示；文化/传承统计缓存不在UI反复遍历。长文化配对表是静态地理数据，只有复归事件才查询，不改为不受支持的动态接口。
- 奖励对比原版保加利亚、菲律宾与澳门等实例：军事攻防+20%十五年已足够，民政全国多项十五年奖励更广；本轮不普遍增益。逐项量纲与来源见qin-latest-source-audit。

## 验证边界

39项定向缺陷检查修复前35项失败、修复后全通过；独立规格复核58项通过。全局runner保留原始FAIL/NOT_RUN分类，不以“零新增”冒充全局零BUG。Tiger原始966 warning降至545，新增诊断0（最终计数以global-final为准）。用户要求不开游戏；人口分裂/合并时序、出生继承、战争目标实际结算、动态英文显示尚无新引擎证据。

英文审校范围是近期CNE/USM覆盖层及本轮秦波斯；更早供给/外援/菲律宾文件仍存在中文回退，已在english/coverage-inventory.json登记，不声称全部英语工程翻译完成。任务与技能已记录本次发现；正式游戏包不含工具、反例及QA。
''')

write(C/'.scratch/debug-release/issues/17-integrity-recheck.md',f'''# 代码完整性复查

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: [{R.name}](<{R.as_posix()}/release-notes.md>)

CW262实际冷加载与缺定义反例对照；修复scope、重复取消条件、西秦建国/军队/战争链，英文编辑审查。用户新增战争诉求、人口、科技、tooltip、奖励及英文要求纳入同轮。范围内源码与定向检查通过；全局继承/依赖/未运行诊断如实保留，ENGINE_NOT_RUN。

实际交付见报告的main-merge/package/git-delivery。主MOD已有配置、人口、地图和历史数据不改；日本仅修复4处人物转国后的IG目标scope，不改变其既定崩溃/恢复路线。后续用户实机反馈与未解决的遗留资源缺项分开跟踪。
''')
p=C/'.scratch/debug-release/map.md';write(p,read(p).rstrip()+'''\n\n## 最新：完整性复查（2026-11-02）

[17 完整性复查](issues/17-integrity-recheck.md)：CNE截图为冷加载未复现的编辑器诊断，缺定义反例已复现；修复真实scope/事件条件、秦解体非对称战争目标、新国人口/科技/军队与文化批次恢复，完成近期英文审校。定向STATIC_PASS，未开游戏；全局遗留缺项与工具规则差异另列，不宣称全MOD零BUG。
''')
save_before(S/'references/active-work.md')
write(S/'references/active-work.md',f'''# 当前交接：完整性复查与西秦修正

Updated: 2026-11-02。候选integrity-recheck-20261102-a，父版本870639a。[任务17](<{M.as_posix()}/.scratch/debug-release/issues/17-integrity-recheck.md>)与[交付说明](<{R.as_posix()}/release-notes.md>)为当前入口；实际main/Git/压缩包以同目录main-merge.json、git-delivery.json、package.json为准。旧交接保留在skill-before。

修正：26人物IG路径、Donghak局部scope与law对象比较、法国取消条件、西秦七新国参战遗漏、羞辱/反吞并、所有建国正人口seed、转地后一次分档新军与科技、文化复归前清残留。英语17文件720键已审。截图CNE两trigger未缺，CWTools冷加载与明确删除定义反例相对照。未开游戏。

主MOD只合审定差异，地图/人口/历史、文化原数据和日本设计保持。原版/依赖国旗缺失及旧缺本地化等遗留项和global runner的FAIL/NOT_RUN保留说明，不凭零新增清空。本轮源码定向通过不是ENGINE_PASS。

西秦原实施规格在WORK/plans/two-empires/20261102-qin-persia-implementation.md；本轮战争/新军规则以任务17及其报告取代旧规格对应段落。南朝概率/密使仍未实施。构建脚本为一次性历史工具，不重跑覆盖已修代码。
''')
print('Task, handoff, source-based skill lessons and candid review report written.')
