# 陈案→压力→内战与日本原生回调：2026-11-01顺序审查

本次最新用户边界：玩家灭国/Game Over可接受，不以自动救回玩家作为交付门槛；旧叙事事件断开不自动等于本轮必须补齐。旧player-ack与Japan legacy候选保持UNSELECTED，源码/报告原样保留。本文不改写任何旧验证结果。

## 陈东阳实际链条

1. F2 `common/scripted_triggers/nesnd_chen_security.txt:10`：案件机会要求本人仍在USM活着、started标记、危机JE有效、未吴化/settled、压力>24、案未解决。
2. `common/journal_entries/ce_usm_the_last_days_of_ming.txt:27–34`：真实月脉冲先增长压力（通常+1，既有联邦协定+0.4），900无事/20案件权重调用`nesnd_chen.2`。
3. `events/nesnd_chen_security.txt:21`：正式随机事件调用prepare，按警卫/情报状态选择死亡、负伤或脱险。死亡路径只排`flavorUSM.5`（+1day，pending7days）。
4. `events/flavorUSM_ce.txt:749–772`：.5再次核实际陈仍在国，kill同一角色后调用`nesnd_chen_after_death`。该helper第74–78行仅在started标记仍存在时加25、clamp0–100、移除started，保证一次；原作者.5的预期增量也为25。
5. `.5`选项的`increase_usm_conflicts_25`只是既有说明，实际+25已在immediate发生。测试应比较事件投递之前与弹窗出现之后，不能只比较点击该选项的前后。
6. 自然死亡后的`.6`由国家月事件表调用同一去重helper；它要求世界中无活陈、started标记仍在、1862年前。活人转属/流亡不是死亡。
7. 当前压力bar通过`nesnd_refresh_south_display`每周刷新；same-tick画面可能落后于实际变量，应同时保存变量、面板和下一周结果。
8. 危机JE自然完成要求压力>=100、未settled、郑钦已去世或离开USM；计划26（第15/21/27行）和既有usm-live-engine-sequence（第9/38行）明确记录这条门槛。提前禅让按钮>=70、AI权重0，是另一路。此次不将这些已记录条件当成缺陷删除。
9. 完成后调用`flavorUSM.4`调度→`.400`实际继位，+7days邀请各地方/JAP。`ce_usm_civilwar_journal`等待3个月开始buffer及答复（最长180day），有反对者调用`usm_civilwar.2`→`nesnd_open_southern_war`。后者先确认实际创建了标记博弈，才写`usm_civilwar_occured`。无反对者转既有和平协商，不应强造战争。
10. 外交博弈创建失败已有`nesnd_south_retry_confrontation`按钮（succession_board JE:25挂载，AI权重5），不要仅因`.2`的have_seen标记就误认完全没有重试入口。

## 已修的具体源码顺序缺陷

`flavorUSM.1`的immediate先创建压力变量，按钮稍后才添加危机JE。如果intro窗口尚未确认期间真实自然死亡`.6`已增加25并移除started，随后点击intro会执行JE原有无条件set0，抹去已领取的一次性增量。

新独立候选`exports/f2-sequence-debug-20261101-a`只在JE初始化的set0外围增加`NOT has_variable`守卫。已有`nesnd_south_initialize`仍为正常新局创建0。反向去掉这个新守卫，整个JE文件有序AST完全等于F2；增量、月增、阈值、郑钦门槛及全部事件未动。

证据`chen-pressure-initialization-sequence-static.json`：实际父源码静态fixture FAIL（无条件写0一次）→新源码PASS（零次）；去掉守卫或反向守卫的负例均能检出。**尚未在引擎重现，不能称实机修复通过。**

## 最小真实场景

|场景|入口与观察|期望|
|---|---|---|
|延期intro顺序|新局让真实.1窗口暂不确认；在独立QA标明自然死亡夹具，使真实陈死亡；过原生月脉冲让.6处理并保存压力；再确认.1入JE，下一周核bar|已获得的25保留，started已移除，不会归零；正常无先前增量的新局仍为0|
|正式死亡结果组件|独立案前档、有活动JE和真实陈；QA准备压力75，再调用生产prepare+death，过1day实际.5|同角色死亡，压力到100一次；重复helper/后续.6不再加25。此夹具不证明随机概率|
|自然完成正例|上一分支另有郑钦已合法去世/离国、无settled；自然JE评估，实际继位/地方反对选项，过7days邀请和开始buffer|出现真实带this_is_nanming_civilwar_var的dp_usm_civil_war；不是直接强制.400/战争helper代替全链|
|自然完成负例|压力100但郑钦仍在国活着；或已settled；或全部邀请方不反对|按当前设计不自然开战；70按钮若使用须标明独立提前路线|
|同tick顺序|记录kill后立即、+1day、下次月的any_character活陈判定及压力|验证死亡对象移除/cache时序；不能仅凭Python推断同tick立即可见|

## 日本原生吞并时序能力

- GAME `common/war_goal_types/war_goal_types.md:47–49`与`00_annex_country.txt:193–194`只把on_enforced定义为原生kind行为之上的附加效果；`kind=annex_country`本身由引擎执行，priority80。
- GAME `common/on_actions/00_code_on_actions.txt:6230–6234`提供on_wargoal_enforced、目标对象和博弈scope；当前源码及导出的on_actions.log未列before_annex/on_country_annex前置钩子。
- diplomatic_plays.md:26–34只列周脉冲、战争开始/结束、on_demand_accepted等。其accepted备注明确是尚未创建外交博弈的直接接受入口，不能据此宣称可拦截所有退让或战争吞并。
- F2 `nesnd_japan_confirm_native_annex`明确先要求JAP已非活国，再设置pending；`nesnd_japan_recovery_request`再排+1day恢复。因此该已实现路径设计上就是吞并后恢复。当前两种on_enforced/on_wargoal_enforced相对先后次序没有独立逐钩证明。
- 文档确有custom kind（99–100行），能使效果全由脚本执行；改用它安排“释放→play_as→吞并”会改变原生战争目标行为，不是已证明可在当前annex kind前插队的接口。用户既接受Game Over，本轮不据这个猜想改造战争目标。

新review-register应将已观察的玩家Game Over按最新用户意图记为ACCEPTED_DESIGN，并把不要求的旧救援/叙事补链移出必要验收。旧FAIL报告保留历史意义；仍须验证实际国家恢复、领土与人物归属、陈案增量及战争目标达成，不把政策接受等同全部游戏通过。
