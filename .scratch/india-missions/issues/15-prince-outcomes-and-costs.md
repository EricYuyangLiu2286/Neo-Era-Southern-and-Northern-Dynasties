# 15 土邦与附属一侧日志结局、金额读收入（批次 12）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: Claude  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/结局-土邦/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/结局-土邦/verify_outcomes_princes.py)

## 现象与期望

作者 2026-11-24：日志只有完成、失败、取消条件和按钮，没有奖励、惩罚或导向。土邦、附属国、宗主国一侧的日志也要有真正的结局。印度各处写死的金额改读付款方或收款方的收入，莫卧儿产业买卖按建筑施工量定价。

## 改动

- 诸邦之间：「自强之邦」（独立、3 项本地工程，永久建设修正、地主满意 5 年，设 `nesnd_india_prince_strong`）；「并入帝国」（作为自治领加入时得永久「王公特权」）；原「无效果」结束改为隐藏 invalid。
- 出使求援：「外援成约」（累计 3 份外援，与出援国关系 +30，出援国在本国首都战略区参与度一时 +1000）。
- 举事的烽火：「南方已定」（六州都归首都在印度的国家，正统永久 +10）；「烽火熄灭」（3 败 0 胜，正统 −10 五年，各原主 antagonize，十年停歇）。
- 保卫地方自主：「守住」修正改永久，原主得宣称并对资助帝国 antagonize，事件 `nesnd_india_revolt.2` 二选一；「失败」时原主收回的州里起事国主体文化激进 +20%。
- 缉查地方组织：「南方安定」（满十年无起事，永久修正，十年冷却）。
- 谋求独立：「独立」发事件 `nesnd_india_indep.12` 三选一；「独立受挫」由月度检查发事件 `.13`，两条进度条减半，首都州激进 +10%。
- 属邦动向：「属邦安定」「属邦离散」。
- 金额：`nesnd_india_contact_price`、`_launch_price`、`_suppress_price`、`nesnd_india_indep_watch_price`、`_conciliate_price`。
- 莫卧儿产业：价格 = 施工量 × £40 / £64，报价时选定建筑（`nesnd_mug_deal_state`、`nesnd_mug_deal_kind`），`gen_deal.py` 生成施工量与类型编号。

## 待作者测试

数值都是默认，测后再调。交付记录「代码无法证实」一节列了未见原版实例的写法。
