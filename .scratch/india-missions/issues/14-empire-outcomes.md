# 14 印度帝国一侧日志结局（批次 11）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: Claude  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/结局-帝国/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/结局-帝国/verify_outcomes_empire.py)

## 现象与期望

作者 2026-11-24：帝国一侧的日志只有完成、失败、取消条件和按钮，没有奖励、惩罚或导向。每个结局都要写清给什么、扣什么、往哪里去。「删除日志给的临时效果」和 120 个月修正不算结局。

## 改动

- 学校与行政、工场与军队：修正改为永久，数值减半。工场与军队另给贝塞麦转炉（已有则机械化作坊）科技进度 5000。
- 学务与实业：完成时触发事件 nesnd_india_core.1，选集权或分权，记入 `nesnd_india_reform_path`（1 集权，2 分权），「中央与各邦」开出时按它摆默认安排。新失败结局「改革中辍」：改革期间违约或破产，十年内不能重开（`nesnd_india_reform_lapse`）。
- 谁代表国家：「共同体成形」（事件 .2，王朝宪章或共和安排）与「共同体破裂」。原「无效果」结束改为隐藏 invalid。
- 种姓与公职：「平等任官」永久修正加下层忠诚派。新失败结局「守旧反扑」。
- 王朝的民望：「王朝稳固」与「王朝危机」（事件 .3，退位改制或镇压）。
- 中央与各邦：「集权定局」（事件 .4 逐个问并入或保留）、「联邦定局」、「联盟离散」。定局后日志不再开回，安排照旧维持。
- 统一与新秩序：修正永久，宣称、南北印度利益、热忱目标。「新秩序瓦解」由月度检查发事件 .6，撤回本日志给的宣称。
- 与宗主国的旧约：「旧约终结」。王公会议：「会议成制」与「会议失败」。
- 新事件文件 `events/nesnd_india_core.txt`（命名空间 nesnd_india_core）。

## 待作者测试

数值都是默认，测后再调。交付记录「代码无法证实」一节列了未见原版实例的写法。
