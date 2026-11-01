# 1.13.11 原生条约、供给和援助

2026-10-31，build24799966。本页记录当前源码能力，**不是新候选游戏验收结论**。涉及援助、供货、财政或共同市场时，先读这些实际文件，再读engine docs并测试条约UI和两国账目。

|意图|实际接口与来源|不得混淆的边界|
|---|---|---|
|贸易权利|`GAME/common/treaty_articles/25_trade_privilege.txt`|影响贸易权利，不是固定商品数量承诺；共同市场junior受原生资格限制|
|指定商品转移|`13_goods_transfer.txt`；`history/treaties/00_historical_treaties.txt:258–272`法援埃及，小武器10、火炮5|真实goods_transfer条款支持quantity/goods。市场、出口cap、港口/相邻市场、运输网络、科技和双方非junior资格仍必须满足；多次违反履行条件会freeze。不能笼统写“引擎不能按商品供货”|
|实际资金转移|`05_transfer_money.txt`实际key为`money_transfer`；`events/soi_events/00_ep1_afghanistan_events.txt:492`|必须核付款方source、收款方target、inputs.quantity、科技和default资格；不能用给收款国战斗buff和给付款国工资modifier替代真实收支|
|约束和撤回|engine effects.log `create_treaty`、`withdraw`；对应article的on_break/on_withdrawal|`binding_period`是违约约束期，不是自动到期日。未明确撤回的条约可继续履行。脚本withdraw默认apply_break_penalties=no，若模拟正常提前违约必须显式遵守原生惩罚，不能偷偷免责|

有效形状（原版法国援助埃及的一个条款）：

```text
create_treaty = {
 first_country = c:FRA second_country = c:EGY is_draft = no
 binding_period = { years = 2 }
 articles_to_create = {
  { article = goods_transfer source_country = c:FRA target_country = c:EGY
    inputs = { { goods = g:small_arms } { quantity = 10 } }
  }
 }
}
```

新事件使用**语义一致、各自遵循接口语法的can_create_treaty**检查，不因为这段history有效就绕过外交权限。请求先保存真实发起国/对象、期限及宗属身份；接收国可接受/拒绝，接受前再查国家存在、当前关系、战争、宗属、资格及供给。求援的发起国并不一定是付款方：MUG向FRA求援的source是FRA、target是MUG。

数量按周：GAME `localization/english/diplomacy_l_english.yml:1964–1966`明确money_transfer每周支付，`:1978–1979`明确goods_transfer每周转移。实际订单/预算仍由测试确认，不能把条约显示量与未扣运输/冻结的净供给混作一列。

财政评估同时看`net_fixed_income`、`net_total_income`、储备及实际UI的建设和军费。候选门槛（如每周500）只服务一项自愿承诺，不能变成所有国家开局健康标准。自给农不是失业；短缺、贫困或转产阵痛不自动是BUG。保留留共同市场、渐进转产、节流、外交补给、退出后重组等可行路线。

实际测试至少包括：双方预算/市场订单、条约source/target/quantity、接受与拒绝、缺科技/被限制的junior、运力/出口不足冻结、失约/战争/灭亡/宗属变化、提前撤回的责任、约束期结束但尚未撤回、保存重载。一次静态通过不能证明资金或货物已在引擎中移动。

## 预检和创建的商品字段不同：run150709真引擎反例

当前1.13.11 `can_create_treaty.inputs` 使用单数 `good = g:small_arms`（本机triggers.log:8955、8977）；`create_treaty.inputs` 使用复数 `goods = g:small_arms`（effects.log:1056、1078，当前原版history/treaties/00_historical_treaties.txt:258—264）。article名仍是 `goods_transfer`。triggers.log示例旧称resource_transfer不能照抄；当前article定义明确是goods_transfer。

run150709四处预检误写goods，产生Unexpected token: goods；实际create的两处goods未报错。此前“can/create全部参数结构完全相同”断言是错误的，会把两处同时写错当通过。校验应保证语义（付款/出货方、收款/收货方、商品、数量、期限）一致，同时分别检查good/goods语法；不能机械全文替换，更不能移除can_create绕过原生资格。修复后仍需新冷启动、真实按钮、接受、条约UI和订单验收。
