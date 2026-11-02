# 印度方案原版事实窄范围复核

2026-11-02。审查对象：`WORK/plans/two-empires/20261102-india-development-design.md`。依据本轮已读GAME 1.13.11/build24799966原始源码，限阶段门槛、种姓/宗教、BIC身份约束、教育初始化与莫卧儿身份。**未发现需纠正的原版事实陈述。** 未改方案或游戏源码，未开游戏。

| 草案位置 | 结果与直接依据 |
| --- | --- |
| 第20行：baseline识字不能报全国5% | 正确。基础0.05，另有职业/阶层加项，未整合州乘0.5。[00_starting_pop_literacy.txt:292–336](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:292>) |
| 第27、41、55行：王朝来源不能等同全部人口文化；民族主义不必推翻王朝 | 原版事实边界处理正确。原版MUG定义是hindustani主体文化、Sunni宗教及种姓等级；泛印度运动另有BIC、属国、无南亚主体文化、泛民族主义等前提，不能原封不动成为反MUG运动。后两行是已标明的提案，没有冒称原版强制结果。[00_countries.txt:1278–1289](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1278>)；[03_pan_national_movements.txt:13–27](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/03_pan_national_movements.txt:13>) |
| 第30行：原版Mughal日志在BIC不存在时失效 | 正确，`invalid`明确写`NOT exists c:BIC`。[04_mughals.txt:37–41](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_mughals.txt:37>) |
| 第46行：功利主义/铁路/民族主义/人权/联邦的阶段依据 | 正确，是机制对应的简写，并未声称这些条件是各JE的完整且充分条件。功利主义完成有学校、税制等要求；铁路需科技及南北印度据点；自治需泛民族主义、运动及非公司属国；反种姓需human_rights；联邦需独立或自治及所属土邦。详见[功利主义](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_imperialism_of_promise.txt:41>)、[铁路](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_railway.txt:14>)、[自治](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_home_rule.txt:12>)、[反种姓](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_dravidian_movement.txt:11>)、[联邦](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_indian_federation.txt:8>) |
| 第61行：种姓体系与宗教分开，适用印度教且南亚传承，无印度教固有识字惩罚 | 正确。等级pop criteria同时要求两条件，hindu宗教条目无教育/识字修正；法律确有四档。[社会等级](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_hierarchies/00_social_hierarchies.txt:5>)、[社会阶层](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_classes/01_british_indian_caste_system.txt:1>)、[四法律](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_caste_hegemony.txt:6>)、[hindu定义](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/religions/religion.txt:89>) |

第67行大学/教师/公职的描述位于拟议机制表，属于设计目标；本轮没有将其判为已经存在的原生专门军官学校链。第42行“社会运动或相应改革授权”、法国援助指标和新阶段条件同样是提案，不按原版默认门槛指错。

范围外：MOD人口/建筑/领土/人物有效加载、公司与军编制审计结论、BHT/MUG/DRA形成数据库数字、原始叙事资料。这些由另两份研究承担，本复核不据未读新来源扩大认证范围。无实施或引擎验收结论。
