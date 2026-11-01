# 南朝战争与日本崩溃修复

2026-11-01。父版本8623191；候选south-war-collapse-20261101-a。验证STATIC_PASS / ENGINE_NOT_RUN，用户自行实机测试。

## 已改行为

- 恢复usm_civilwar.5：普通反吴藩国的首都由USM或USM附属控制，或敌占超过80%，会触发投降吞并。按最新要求覆盖盟主；JAP排除在单首都规则外。战斗结束后次日检查、原有每月入口与吴方日志每周补检查共用谓词；投降事件沿原duration=3和人物结局执行。执行时再核实际资格，按钮不再强制玩家转到USM。
- 实际吴方战争要求执行及“敌国投降”原生回调，记录具体败方，解决没有对其索取战争要求的支援国战败后留独立问题。没有战争/败退证据的国家不会被吞并。
- 日本与吴朝交战，京都STATE_KYOTO与关东STATE_KANTO同时被敌方控制即崩溃；实际败给吴朝的另一入口也进入结算。吞并前登记日本土地、转存人物，吞并后沿已验证的恢复三国、Lin摄政链。允许玩家GAME OVER，不加入自动续玩救援。
- 新全球日志“幕府危局”只创建一次，日本及当前敌国共享同一实例；动态更新可见国、周度控制结算。日志持续跟踪至三分完成，单纯停战不会抹掉一次性状态。原属第三国的土地不转移；第三国仍占领的必要锚点按现有恢复安全条件等待，不能假称当日立即完成全部三国。
- 延迟投降/恢复未完时，三条战争日志和全局现状事件均禁止抢先判现状；避免“战争结束→现状→随后吞并”的错误次序。
- 襄樊初始正规营队21→25，增加4营襄阳散兵步兵。使用原生combat_unit历史入口，不重复另建兵营。日志“襄阳大营”在HNA拥有襄阳时给军用品费用−20%、防御+20%，无额外攻击加成；失去襄阳则失效。新增营队仅新局历史生效，旧档不强行补兵。
- 旧STATE_JETISY的中文伊犁→西益，英文Ili→Xiyi；QE1首都STATE_ILI保留伊犁。甘肃xBD5671确实继承原版lakes分类，按用户新要求不修改。较早独立map-only候选标为superseded，未进主MOD。

## 历史原因与边界

原始f18b6c4有首都OR80%事件与日本败后分支；45f475e已将usm_civilwar.5/.6置always=no，关闭日本旧JE的fail/invalid；后续主版本沿用了它们。不是玩家读档/操作导致。源码可以证明禁用，不能单凭diff证明当时是否出于避免GAME OVER的动机。本轮已恢复相关玩法并记入技能。

战时make_independent在原始内战链就存在，是反吴阵营脱离宗主、进入战争的引擎表示；它不等于赢得永久独立。旧日本.22本身是割首都+降为dominion，并非现有三分效果；本轮把明确败局接到后来已实测的三分链。旧反吴胜利.6仍由现有明廷胜利/宪制选择流程接替，不盲目同时启用两套结算。

本轮不实施新概率、北方密使、约章重抽、六档倾向或B政治评分。详细[计划](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261101-southern-allegiances-envoys-plan.md>)已记录所有新旧要求、公式、可行性、未定参数、七项依赖和数值枚举。主MOD的HNA战前立场仍是上一轮固定拥明，下一阶段统一替换。

## 外部证据

- 32项真实源码结构检查：父版30项失败，候选32项通过；不将它们称为引擎行为测试。
- Tiger：6 error /973 warning /2 tips，较已交付父版零新增；继承问题仍按原分类保留，未宣称全MOD无错误。
- 实际stdio MCP四次嵌套源码查询通过。两轴审查：Standards初查2处引用保护问题，Spec初查2处败局遗漏/结算竞态，均已修并复查关闭。
- 所有地图几何、州归属、人口、产业、国家定义、人物历史与主metadata保持原字节；军事历史仅HNA4营变化。新文本中英文BOM与引用经过检查。
- 未启动游戏，未新读写存档。原生日志也不是本轮新跑产生的。通知回调对无要求支援国及AI的完整运行时分发、两州占领刷新时点、全球日志实际显示仍由用户实测确认。

## 原始来源

本机GAME1.13.11/build24799966：00_code_on_actions.txt的on_battle_ended/on_empty_battle_won、on_wargoal_enforced（root胜者、scope:target败者）、on_enemy_capitulated_notification（root国家）；messages/00_messages.txt:70与interfaces_l_english.yml:9318–9319确认enemy_capitulated对应scope:target。这些是原版实际链条，非推测隐藏的war对象。

全球JE：00_peoples_springtime_je.txt、journal_entries.md、journal_entry_groups/00_journal_entries.txt；动态成员参照原版01_ryukyu_rivalry和项目已用的board。HNA军事历史参照原版07_military_formations_subsaharan_africa.txt及99_military_formations_example.txt；战斗修正见105_modifiers.txt的shi_gakko，军费乘数见00_modifier_types.txt:526。

修改前独立备份：WORK/backups/pre-change-south-plan-map-20261101T213214Z/mod。交付候选/checkpoint、主MOD合并和Git结果分别见同目录backup-delivery.json、main-merge.json、git-delivery.json。正式包排除QA、工具和开发文档。
