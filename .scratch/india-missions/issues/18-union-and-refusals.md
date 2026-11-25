# 18 先礼后兵与土邦联合（批次 14）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: agy  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/土邦联合/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/土邦联合/verify_union.py)

## 现象与期望

此前王公并入被拒只有 6 个月冷却，本地项目与莫卧儿产业买卖被拒毫无外交后果，不符合「先礼后兵、谈不拢就动武」（R4）；独立土邦之间亦无抱团抗拒并入的集体机制。本批为三类被拒补齐外交与宣称出口，不设新禁令，并在 `princes` 组新增独立土邦日志「土邦联合」（`nesnd_india_union`）。

## 改动

- 王公并入被拒（`nesnd_india_union_decline`、`nesnd_india_diplomacy.1`、`nesnd_india_union.2`）：保留 6 个月冷却；帝国首次被拒得拒绝方首都州宣称（`state_region = { add_claim = scope:india_sender }`）并在拒绝方记 `nesnd_india_union_refused_empire`（`days = 3650`）；10 年内再被同一土邦拒绝时，再得其印度其余各州宣称；帝国为 AI 时对拒绝方设 `set_secret_goal = conquer`；拒绝方若属 `nesnd_india_union_members`，联合其余活着的独立成员对帝国关系 −10；双边提示均写明宣称与联合反响。
- 本地项目与产业买卖被拒（`nesnd_india_matter_fail`、`nesnd_mug_matter_fail`、`nesnd_india_matters` 按钮、`nesnd_india_project.5`、`nesnd_mug.2`）：种类 1（本地项目）与种类 7、8（产业出售与买回）因拒绝或宗主禁许（结果 1、2）落空时，请求方对拒绝方生成原版外交诱因 `catalyst_event_negative` 并令双方关系 −15，不加禁令，各处提示写明。
- 新日志「土邦联合」（`nesnd_india_union`，写入 `princes` 组各文件与 `nesnd_india_refresh`）：
  - 面向独立土邦（`nesnd_india_prince = yes`、`is_subject = no`，不另挂「自强之邦」门槛），印度境内另有至少一个独立土邦时出现。
  - 按钮「邀约互保」（`nesnd_india_union_invite_button`）：花费周收入 ×4（`nesnd_india_union_invite_price`，下限 £2,000、上限 £20,000），冷却 12 个月，选与本国关系最高且尚未与本国缔结防御条约的土邦（优先独立土邦，无则回退至附属土邦以免灰显），发独立邀约事件 `nesnd_india_union.5`（回执 `nesnd_india_union.6`）。对方同意则关系 +20、依次尝试 `defensive_pact` / `alliance` / `guarantee_independence` 签 5 年期防御条约并将独立双方加入全局变量列表 `nesnd_india_union_members`；对方拒绝则关系 −10。AI 接受权重：基础 50、关系每 +10 加 10、被印度帝国持有宣称加 30、为印度帝国附属国时乘以 0。AI 独立土邦每月 5% 机会自动发起。
  - 结局「联合成约」（`nesnd_india_union_members` 有 3 个及以上活着的独立成员）：各成员永久得 `nesnd_india_union_pact`（`unit_defense_mult = 0.1`），成员间互设 `set_secret_goal = protect`，日后面对帝国并入邀请时 AI 接受权重 ×0.25，触发成约事件 `nesnd_india_union.7`（中英 flavor）。
  - 结局「联合破裂」（列表曾达 2 个以上而后活着的独立成员少于 2 个）：剩下成员对离开者（若存活）关系 −30，得 10 年修正 `nesnd_india_union_broken`（`country_legitimacy_base_add = -5`），触发破裂事件 `nesnd_india_union.8`（中英 flavor），10 年后（`nesnd_india_union_reopen_wait`）若仍独立可再开日志。
  - 成员成为附属国或被并入时（`nesnd_india_settle_union` 与月度 `nesnd_india_union_maintain`），从 `nesnd_india_union_members` 移除，条约存废交由原版处理。

## 代码无法证实

数值均为默认值，实机测试后再调。交付记录「代码无法证实」一节列了 `remove_list_global_variable`、未获认可土邦间 `create_treaty` 与条约维持条件、本地化经脚本值读 `every_in_global_list`、以及成约后再次跌破 2 成员时月度维护的触发时序四项。
