# Spec review — journal bug sweep

对象：`backups/pre-change-journal-bug-sweep-20261104T005112Z/mod` → `exports/journal-bug-sweep-20261104-a`快照差异。1.13.11/build24799966，catalog CURRENT。依据本轮委派范围：修当前BUG及同类缺陷；危机描述、印度身份/等待反馈、西秦两端奖励/预览、日本拨款预览、故事JE钉选；地图、波斯重构和西方JE为后续增强，不在本批。

## 构建中首次审查

当前只形成4个修改文件，`spec.md`尚未生成；其它计划项仍在构建，不能以此快照认证全部需求完成。

1. **[P2] 日本拨款预览包装改变了两个按钮的AI字段层级。**本轮要求是“JP funding preview”，应保留既有扣款、冷却及AI行为。[nesnd_jp_politics.txt:50](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-bug-sweep-20261104-a/common/scripted_buttons/nesnd_jp_politics.txt:50>)的`nesnd_jp_inspect_military`和第76行的`nesnd_jp_inspect_representative`仅关闭if/hidden_effect后便写`ai_chance`，将它留在effect内部；同文件court按钮有正确的第三个闭括号。结果为非法effect字段，且原按钮根层的AI权重丢失。将effect在ai_chance前关闭，并移除按钮末尾对应多出的闭括号。

西秦结算修改目前将经济/军事胜利分别显式守卫，并保留十年奖励、后续解锁与一次结算标记；印度等待/援助条件的NOR等价于原各NOT条件，未见确定行为偏差。其余候选内容完成后需继续复核，当前不作零剩余问题或完整通过声明。

另已提醒实施端核对error-before.log的原版`agitators_law_events.txt:260`法律variant错误及`nesnd_war_collapse.txt:60`描述刷屏；二者仍是本轮已定位BUG清单项，构建中未据此额外列缺项。

未修改候选、未开游戏；本报告只代表源码差异审查。

## 完整规格复审

用户新增波斯/USM机制授权已写入[spec.md](spec.md)，取代首次构建时的增强范围排除。原JP按钮AI层级发现已关闭。已核对完整差异、原版法律同路径覆盖及对应调用链；当前2项待处理：

2. **[P1] 晚期已整合旧档的豁免依赖周脉冲先发生。**规格要求“旧档首次引入时若三州已整合且过1850，保留既有完成成果”。[JE:6](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-bug-sweep-20261104-a/common/journal_entries/nesnd_usm_western_provinces.txt:6>)仍允许该旧档自动加入，日期fail立即满足；豁免只在[周度迁移:28](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-bug-sweep-20261104-a/common/scripted_effects/nesnd_usm_western_provinces.txt:28>)设置。JE若先于下一次周脉冲执行，会误罚四文化25%，随后周迁移还可能同时留下failed/succeeded标记。应使入口、即刻初始化或失败效果自行识别首次引入豁免，避免依赖尚未验证的引擎调度次序。

3. **[P2] 自动整合发生在吞并成功确认之前。**规格要求“吴朝内战吞并后”整合大陆。新增[归降整合调用:137](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/journal-bug-sweep-20261104-a/common/scripted_effects/nesnd_south_holdouts.txt:137>)紧跟annex但先于下一行`is_country_alive=no`成功判断；行在崩溃和旧`.5`也有同样形状。若原生吞并未成功，仍会整合所有匹配大陆州并创建西部JE。应在确实消灭目标的分支中提交整合，保留失败重试；原生胜利回调的时序边界另列引擎限制。

其它已核范围：37个逐州按钮共用25点扣费与实际目标重验；波斯双路线互斥、两资源单一变量周期与绝对bar同步；旧民政/工商JE封入口并移除旧键，新grant独立；12个日本请求预览和3个新政预览与实际费用/期限一致；Qin无胜利不发默认军事奖励；法律同路径文件只有目标两处变化；四文化失败只在单一effect执行，通知无再次惩罚。SoL明确为15职业cohort月度近似、首次采样、40日过期及结束清理，未当作原生逐次变化精确效果。

尚不作引擎通过声明。复审发现针对确定代码分支/调度缺口，并非声称已经实机复现。

## 最终受影响闭包复审（2026-11-04）

**剩余Spec发现：0。首次构建的JP层级问题及完整审查的2项USM问题，合计3项均已关闭。**

- `nesnd_usm_western_eligible`现要求`nesnd_usm_western_migrated`。自动possible及显式ensure均依赖该谓词；周度迁移先记录首次引入状态并处理1850后已完整整合的豁免，再调用ensure。旧档不能先加入JE并受罚；1850后未完成实例仍按当前绝对期限处理。
- 行在崩溃、向吴归降及旧`.5`三条脚本路径都只在原目标实际`is_country_alive=no`后调用大陆整合。原生回调另外要求吴方争端尚未结算、败方持反对国标记且已经消亡；存活投降或赔款回调不再满足。`.8`在真实总胜利守卫内提供最终整合补偿入口。原生吞并/回调执行先后仍保留引擎验证限制。
- 波斯同步改用真实JE的owner读取存量，移除临时保存scope依赖；未改变月度资源值、消费或进度条算法。

本次只复核上述受影响闭包，没有重复扩大全局检查。45个变化玩法文件的原始SHA与保序token指纹存于[最终审查指纹](spec-review-final-hashes.json)，聚合保序token SHA-256为`2287574a681a0fd240dc74fbf41e208c12d4ab9023f5f29cea26e700240e77f5`。该记录绑定本次读取到的候选；主任务仍须完成正在进行的外部检查及交付校验。

未修改候选、未开游戏。0发现是本轮规格差异审查结论，不等于全MOD零BUG或引擎验收通过。

## 最终窄范围收口复核

**剩余Spec发现仍为0。**本节取代上一节45文件指纹作为最终受审版本，之前的指纹已保存在`spec-review-prior-45-hashes.json`。

- 三条脚本吞并入口先在原败方快照实际大陆/三例外州来源，每次先清旧标记，吞并确认成功且该次有大陆来源才整合；日本或纯海外吞并不会通过该入口触发大陆整合。原生回调另要求死去目标有真实`enrolled_round`与反对国标记，且争端尚未结算；原生回调时序继续保留引擎验证边界。
- 西部失败effect新增`opened`门槛，不能在日志从未启动时直接罚文化；身份失效设置`finished/archived`，清理采样后永久关闭入口。正常成功、失败及旧档已完成豁免仍不重复处罚。
- 波斯东/西JE各自在月度调用前检查本路线eligible；旧路线尚未失效时也无法凭另一条路线的资格重复写入资源。资源存量与先前月增公式不变。
- 外交剧情JE只将默认钉选从no改为yes，未改变周度逻辑或反复覆盖玩家选择；与最新委派确认的23个钉选范围一致。英文`STATE_SICHUAN`明确覆盖为Chengdu，契合本项目成都州语义，不改地图。来源标签已移除QE1/FRA兜底实现叙述；`writing-comparison.md`覆盖了本轮文本与脚本对应关系。
- 相对上次指纹，`nesnd_crisis_buttons.txt`原始SHA改变但保序token完全一致；其它语义变化均为上述收口范围。外部日志文件的尾空白与新增默认钉选差异分别核对，没有误把语义改动归为纯格式。

最终46个变化玩法文件指纹已更新至[spec-review-final-hashes.json](spec-review-final-hashes.json)，聚合保序token SHA-256：`cebcb1c9622e2909ff73150719b90da68e514ad465557ab247956f25ab45f103`。仅报告文件发生写入；未修改候选、未开游戏。主任务还将重跑最终SHA交付校验。
