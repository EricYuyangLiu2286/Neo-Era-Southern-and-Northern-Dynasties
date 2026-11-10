# 58 外交请求按钮的“永不”与条件提示

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [改前备份与 Tiger 结果](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-request-button-tooltips/>)

## 现象与期望
普鲁士“德意志的共同防卫”和南洋、东南亚、印度“国计与民生”的请求按钮，条件里显示“X永不”，进游戏后一直无法点击。期望：条件按原设计生效，提示铺开但简洁。

## 原因
按钮在 `hidden_trigger` 里存临时作用域（发起国、对象国），再用 `save_temporary_scope_value_as` 存请求类型，随后 `nesnd_canon_request_conditions` 先查这三个作用域是否存在，不存在就走 `trigger_else = { always = no }`。引擎生成提示时跳过 `hidden_trigger`；原版也从不在条件里用 `save_temporary_scope_value_as`（只在效果里用）。结果条件只剩“永不”。同一写法还在 `nesnd_canon_current_request_valid`（月度维护用它判断待答复请求是否有效）和 `nesnd_small_market_verification_valid` 里。

## 改了什么
- scripted_triggers/nesnd_canon_diplomacy.txt：请求条件按类型拆成独立 trigger（德意志同盟/防御协约、美国投资、意大利信用、奥地利防御、小邦投资），`nesnd_canon_request_rules = { KIND = … }` 按类型分派；`request_conditions`、`request_eligible`、`current_request_valid` 改用它，后者直接读变量，不再存临时值。判断内容逐条不变。
- scripted_triggers/nesnd_small_diplomacy.txt：`nesnd_small_diplomacy_ready`、`nesnd_small_request_eligible` 改为 `nesnd_small_request_common` 和 `nesnd_small_request_rules_6/7/8/9`；原第9类的“不在战争中”移入规则9。`nesnd_small_reliable_support` 的临时作用域移出 `hidden_trigger`。
- scripted_triggers/nesnd_small_actions.txt：`nesnd_small_can_request` 存作用域后直接调用 `nesnd_small_request_rules_$KIND$`。
- scripted_triggers/nesnd_small_neighbours.txt：作用域移出 `hidden_trigger`；“相邻小邦”整段用一句提示包住（any 内含依赖作用域的文字）。
- scripted_triggers/nesnd_small_verification.txt：伙伴政权比较改读 `scope:…var:`，不再存临时值。
- scripted_buttons/nesnd_canon_requests.txt：39个按钮改为直接存作用域并调用对应类型的规则。
- 本地化：nesnd_diplomatic_negotiations 新增12键，nesnd_small_states 新增16键，中英各一份。
提示设计：玩家能自己达成的门槛逐条显示（关系、独立倾向、实力比例、可否缔约、合法性等），每条一句并标出双方国名；按钮能出现就必然成立的身份检查隐藏；只在特定政体或属国类型下才有的条件，只对相关国家显示。

## 怎么复测
新开局：普鲁士打开“德意志的共同防卫”，悬停“与符腾堡商议防御协约”；南洋/东南亚小邦打开“国计与民生”，悬停“请求自有市场”和各“请求防御条约”。应看到逐条红绿条件，不再有“永不”；条件全绿时按钮可点，发出请求后对方能收到答复事件，45日内请求不应被提前判为失效。error.log 搜 `nesnd_canon` 与 `nesnd_small`，不应出现新的作用域或本地化报错。

## 遗留问题
- 印度直属请求（`nesnd_india_request_1/2/3/6` 与印度邦国防御）不走这条链，本次未改。
- Tiger 1.19.0 落后于 1.15，不认 JE 的 `outcome` 与 `activation_description`；改动文件中无 Tiger 报告。

## 第二轮（作者追加）
- 空项目符号：“请求自有市场”的效果是一个 custom_tooltip，一句约40字的长句；截图里圆点独占一行、正文无圆点，说明是同一条目在圆点旁放不下、整句被挤到下一行，不是多出一条空效果。改为两句短提示：nesnd_small_request_market_tt（缩短）和新增 nesnd_small_request_market_deadline_tt；scripted_buttons/nesnd_small_states.txt:63。确切排版原因需游戏内确认。
- 德意志邦国协定：22个普鲁士按钮（巴伐利亚、汉诺威、萨克森、符腾堡、巴登、黑森、黑森-卡塞尔、拿骚、瓦尔德克、利珀、奥地利，各一个同盟、一个防御协约）的效果改为 scripted_effects/nesnd_canon_diplomacy.txt 新增的 `nesnd_canon_german_request_preview = { TAG KIND }`，只显示提示：提议内容（5年同盟/防御协约）；对方接受机会（按 nesnd_canon_diplomacy.1 的AI权重：基础50%，关系≥50时67%，敌对时不接受，玩家国自行决定，按当前状况只显示一行）；成功后计入“德意志的共同防卫”的3国；首次协定关系+25（尚未得到时显示）；被拒或45日未答复作废、发出后6个月不能再提交涉。新增9个本地化键，中英各一。
- 检查：解析、括号、编码与换行不变，本地化无重复；Tiger 在改动文件中只有既有的 nesnd_small_states.txt:145 括号提示（邻邦按钮，未改）和非中英语言缺键。
- 复测：普鲁士悬停任一“与X商议同盟/防御协约”，看效果区五行左右的说明，接受机会随关系与态度变化；小邦悬停“请求自有市场”，效果应为两行、圆点与文字同行。
- 第三轮（作者要求）：关系≥90时接受机会为78%。events/nesnd_canon_diplomacy.txt 的接受权重新增一项：仅德意志同盟/防御协约（类型1、11），关系≥90再加60，即140对40≈78%；奥地利、美国、意大利、小邦投资的回复规则不变。按钮预览加一档，新增 nesnd_canon_reply_chance_top_tt，改写 base/high 两句，中英各一。
