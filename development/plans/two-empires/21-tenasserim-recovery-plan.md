# 21 丹那沙林：地方生计与南洋制度转型

状态：候选a已冻结，尚未原生验收；独立候选父integrated-gameplay-20261031-d；主MOD/父D/原版只读，不操作游戏。先读evidence/tenasserim-recovery-blueprint.md与tenasserim-workforce-audit.json。证据：DEI地块6级自给+2级盈利染料满员，1837-07欠食284,365中83.1%为在岗自给农；新增染料会占耕地且净岗位减少。原作者法律人口不自动改。

## 目标和依赖图

DEI拥有的丹那沙林state→现有人口/岗位/食品/木材市场→地方日志→可支付且有容量的真实林场建设队列→实际招聘与持续民生改善；制度路线另外连接地主/改革派支持、原生租佃/废奴立法、现有je_reform_indies。文本拆为故事正文、动态状态/进度、按钮规则、结果事件；图标/事件视频引用当前本体现成资源。新脚本用nesnd_tenasserim前缀，不覆盖原全国改革JE。

前期提供至多两次1级林场委办；施工走真实政府队列和正常费用，先1级招聘75%后才能委办第2级，玩家可自行选择其他非占地产业。保留染料、人口、耕地及所有历史PM。局部教习有一次性财政成本、12月效果与12月冷却，不能消除资质生成的制度限制。正常法律菜单保留；新按钮在any_law can_be_enacted、真实在阁/运动支持、15%机会和25合法性门槛下调用start_enactment，只启动原生立法。AI使用同一门槛和按钮，不用activate_law或换政府。正在合法推进租佃/废奴时，可付费协商地主补偿，限时IG赞同，不篡改投票或立法结果。

中期按每月真实state pop workforce统计无业、欠食、在岗欠食、SoL及market_access；连续6个月低于压力线才完成，不要求全国全就业/废奴/完全工业化。全国改革原ID继续以GDP+制度目标运行，二者没有重复结算。当前试验线：至少3个月采样、地方无业<=12%、欠食劳力<=25%、劳力加权SoL>=6.5、接入>=85%、非战争/破产，连续6个月；在岗欠食单列读数和状态不藏在失业中。具体阈值是候选设计初值，必须原生跑后修订。

危机/退出：战争和暂时衰退重置连续达标但不自动惩罚；24个月后连续12个月严重压力（欠食>50%、无业>25%、或破产）发生一次停办/重审事件，给玩家延长或停办选择，不自动删建筑或生造叛乱。失去DEI丹那沙林所有权时invalid清理；重新取得可通过有限重开决议，不重复赠送建设额度/奖励。主动停办取消后续专项安排但已存在原生施工、法律与市场照常，明示不取消用户原生队列。

终局：局部恢复一次性限期小额资质奖励，保留殖民制度的长期国家任务；可选择维持吴市场、既有内战效忠/自治路线、新独立后的替代供货。新JE不赠贸易条约/市场、不改变日本政体、不再叠加“顺吴换供应”外交奖励。D的DEI已有usm_civilwar.1.3忠吴120月修正及关系；新路径只读取实际市场状态。DEI不属于nesnd_supply_country，故不会直接重复HNA/SIH/GNG/HUS准备条。

## 原生格式依据和验证

engine effects.log start_building_construction（state）、triggers.log can_construct_building（state）/law_enactment_stance（IG/运动）/can_be_enacted（law）/enactment_chance_for_law（country）；GAME land_ownership_law_events.12实际启动建设；east_indies.2限期资质奖励。进度条只由每月effect更新，scripted bar无第二个增长源。

需主控补真实场景：DEI玩家从选国页新局、丹那沙林资源份额/木价/工资/资格/实际贡赋；按钮一次进入1级队列且正常扣施工费、复按阻止；第1级完工且75%配员后第二次；月底缓存与原生存档核对；租佃支持/地主政治力量与正常立法时间；战争/失州/破产/重审/主动退出/成功后读档；自然AI半年/年和独立QA强制达标不得混淆。

## 文风

以pre-update replace ce_cne_land_reform_reason、flavorCNE.3.d的制度—土地—人口自由—生活链条为同类原文；不抄牧朝的民族国家立场到殖民公司，不虚构引用人物。新正文写南洋港务/种植园/田主债役和流民工资关系；规则放状态、bar desc、tooltip。交付保留逐类并排对读及动态语法检验。


候选完善：成功事件在选择时再次验证DEI仍持州及未领奖，防延迟/重复领效果；停办满一年后AI仅在和平、非破产且金储至少5000时可重开，保留委办额度/奖励标记，不会无限重送。

冻结：exports/tenasserim-recovery-20261031-a；backup candidate-tenasserim-recovery-20261031T162804Z。实现与实际测试表在evidence/tenasserim-recovery-implementation.md，逐类原文对照在tenasserim-style-comparison.md；可选QA源码在tools/tenasserim-qa-source，未进候选。
