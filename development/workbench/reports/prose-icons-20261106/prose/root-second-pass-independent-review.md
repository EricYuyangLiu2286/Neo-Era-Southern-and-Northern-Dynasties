# 主审二改独立终审

配置gpt-6-astra / high。读取reviewed实际文本，并与root/editorial-second-pass.json定位45个改键。仅生成报告，未改候选、主MOD或启动游戏。

结论：45键中41键通过、4键返工。root已指出的Native.1与small order在reviewed中已修正，本次判通过。另读最终44+28个中英文键，未发现新的工程口吻、术语或脚本范围问题。

## 需要返工的具体问题

### nesnd_civic_characters.6.d

“地方工业的收入逐年增加”断言已发生的年度经济增长。此人物可以在产业收入下降或硫矿亏损时出场。

依据：common/scripted_triggers/nesnd_civic_characters.txt:31，只检查socialism、西西里硫矿occupancy>=0.5及年份；无profit或收入增长条件。

建议范围：保留伤病家庭与矿业分配的冲突，只去除逐年增长的事实断言。

### nesnd_civic_characters.200.d

“取得礼议院的考试资格”通常指取得应试资格，不能直接推出下一句成为学政进入议席。

依据：nesnd-victoria3/references/north-south-institutions.md：进入政界要通过礼议院考试。common/scripted_effects/nesnd_civic_characters.txt:90–98设置nesnd_c2_delegate_qualified后触发200；events/nesnd_civic_characters.txt:363–368要求合格且为政治家。

建议范围：明确已经通过礼议院考试或已取得学政资格，保留后面由提出需求转为承担公共责任的叙事。

### nesnd_small_states.6.d

“曾经必须向外求助的事情，如今可以由政府自行安排”预设受援历史，又容易把达标写成摆脱外部依赖。原本独立的国家也能进入日志；成功可以依靠共同市场、防御条约，或维持高度自主的属国地位。

依据：common/scripted_triggers/nesnd_small_states.txt:nesnd_small_market_order、nesnd_small_defence_order、nesnd_small_order_ready；common/scripted_effects/nesnd_small_states.txt:nesnd_small_choose_order。

建议范围：保留具备维持自主所需基础的成果，不比较未经条件证明的过去受援与现在摆脱依赖。

### nesnd_american_restoration.3.d

仍将当前执行镇压的政府称为共和国，与root已修正的1.d是同一种政体范围错误。

依据：events/nesnd_american_restoration.txt:16–21仅要求nesnd_native_repression；common/scripted_triggers/nesnd_american_restoration.txt:nesnd_restoration_can_suppress与pressure_host无共和政体守卫。

建议范围：改称政府或现政权，保持原住民视角对土地侵夺者受到保护的判断。

## 其余判断

不把没有独立计数器的局部生活场景一概判错，也不以正文长度判冗余。18条organisation续篇通过：群体能在人物退出后承接议题，利益与行动具体，未统一套用人物消失的占位说明。civic.6.d被判返工的原因是“收入逐年增加”直接断言可与实际经济相反的持续走势，并非禁止写矿工家庭或地方争执。

原样保留作者有立场的句子是正面判断依据，尤其讽刺、反问应服务诉求而非每条都作道德结论。当前长段不需要整体删短。逐键判定、两语言新增字段与文件SHA见同名JSON。
