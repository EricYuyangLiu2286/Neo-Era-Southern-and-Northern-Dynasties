# 海外通商：向三个方向的当地政府请求贸易特权或条约港

Execution: completed  
Validation: STATIC_PASS  
Blocked by: none  
Evidence: 工作台 `reports/2026-11-21-india-development/海外通商/交付记录.md`

印度线的最后一项。对象是印度国家：满足 `nesnd_india_empire`、不是未受认可国家、不是傀儡国（`nesnd_india_overseas_holder`）。依据工作台设计报告第五、八、九节和提示词 `prompts/06-海外通商.txt`。

## 文件

新文件：`common/scripted_triggers|scripted_effects|script_values|scripted_buttons|journal_entries/nesnd_india_overseas.txt`，`events/nesnd_india_overseas.txt`（命名空间 `nesnd_india_overseas`），`localization/*/replace/nesnd_india_overseas_l_*.yml`。日志和本地化由工作台 `海外通商/build_overseas.py` 生成。

改动：
- 记录、到期、续约那一套改成参数：期限读脚本值 `nesnd_india_frontier_<T>_days`、`_notice_days`；付款与记录 `nesnd_india_frontier_settle = { HOLDER PARTNER T AMOUNT }`；退约 `nesnd_india_frontier_withdraw_article = { PARTNER ARTICLE SOURCE TARGET BY }`；每月检查 `nesnd_india_frontier_tick` 加 `ASK = small|empire`；续约 `nesnd_india_frontier_renew` 发给条约另一方；事件 `nesnd_india_frontier.3`、`.4` 按种类分段，`.3.f` 不再写年数。
- 「印度事务」加事务种类 10 贸易特权、11 条约港、12 和 13 两者的续约（`nesnd_india_matters.txt` 四个文件和日志 `nesnd_india_foreign_affairs`）。11、13 算对方给出，凡附属国都要宗主国许可；10、12 只有傀儡国要。10、11 占六个月冷却。
- `nesnd_india_refresh` 调 `nesnd_india_overseas_upkeep`；on_action 的范围加 `has_variable = nesnd_india_frontier_overseas_trade_with`、`_port_with`（持有记录的当地政府每月检查到期）。

## 日志「海外通商」

- 正文：GDP 和人均 GDP 世界排名、通铁路的已整合州、钢厂级数与在岗比例（按一成近似）、港口总级数、海军力量投射世界排名。状态行：国库与债务违约、在办的请求、三个方向（印度尼西亚、波斯湾沿岸、东非）各三行。
- 门槛：贸易特权港口总级数 ≥3；条约港 ≥5 且海军力量投射世界前 20。只查本国。
- 当地政府：首都在该方向或持有该方向有人口的州，不含部落邦联。波斯湾沿岸是出海口为 STATE_PERSIAN_GULF 的七个州区域（`nesnd_india_overseas_state_2`）。
- 事件 `.1` 按关系列至多四个，不合条件的灰着写原因。条约港让出该方向、有港口、可作条约港、能签成的州里人口最多的一个。州有别国宣称或在波斯「重启远西战争」目标中时提示，不禁止。
- 签约：十年，印度国家付 £20,000 或 £60,000。记录在当地政府身上（共用记录 T = overseas_trade、overseas_port），到期前 180 日问印度国家续约；不续则到期退约，条约港由印度国家退约（条款的 can_withdraw 只限让出方）。
- 南洋小国系统成员被请求时占它的冷却 `nesnd_canon_request_cooldown` 六个月。
- 变量：印度国家上 `nesnd_india_overseas_dir`、`_show_<D>_<K>`、`_count_<D>_<K>`；当地政府上 `nesnd_india_overseas_<K>_dir` 和共用记录 `nesnd_india_frontier_overseas_<K>_*`。

## 没有做

领土、保护关系、驻军；外交博弈和战争目标；买船造船；改原版国际认可；已有玩家文字里的「德里」等代称（七个键，列在交付记录第八节）。

## 已按代码核验（原「代码无法证实」三项）

2026-11-22 收尾批读代码定下，依据见 工作台 reports/2026-11-21-india-development/收尾/审阅/待实机核验.md「四问」。

1. 条约港条约退约后港口是否交还：不交还。条约作废后港口成为接收方的普通州，让出方只得到该州区的宣称（原版 concept_treaty_port_desc、RENEGE_TREATY_PORTS_WITH 与条款 on_withdrawal）。effects.log 那句「returning the ports」是过时说明。现行文字与此一致，不改。
2. `withdraw` 是否检查条款的 can_withdraw：代码无法证实（原版没有一处脚本退带 can_withdraw 的条款）。本 MOD 由接收港口的印度国家退约，can_withdraw 只限让出方，两种情况下都能退成，不改。
3. 日志里由变量链取对方身上变量的到期日：能显示。数据类型文档里链上每一步都回到 Scope，状态行已用 exists 把关，不改。

另：附属国在宗主国市场之内，不能给出或收到贸易特权（原版 25_trade_privilege.txt 的 visible、can_ratify）。收尾给请求加了具名提示 nesnd_india_own_markets_tt。
