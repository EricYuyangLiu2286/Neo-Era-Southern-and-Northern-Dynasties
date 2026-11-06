# 四项纠正与新增短句最终复核

状态：FINAL_EDITORIAL_PASS。配置gpt-6-astra / high。

4项主审修订的文字均通过。已逐字核对reviewed与main完全一致。

|键|文字判断|main一致|reviewed一致|
|---|---|---|---|
|nesnd_civic_characters.6.d|已去掉收入逐年增长，保留矿业财富分配冲突。|True|True|
|nesnd_civic_characters.200.d|明确通过礼议院考试并取得学政资格，未混同应试资格。|True|True|
|nesnd_small_states.6.d|改为已有财源、人才及外交交涉资本，不预设受援史或摆脱共同市场/防约。|True|True|
|nesnd_american_restoration.3.d|当前镇压者改称这个政府，不预设共和国。|True|True|

新增nesnd_small_review_available_tt与nesnd_small_dispute_law_promised_tt的中英文短句通过。源码已见在新争议begin中移除旧nesnd_small_promise，旧承诺不会被该显示读取为新争议的承诺。此为源码检查，不是游戏实测。

初轮4项返工及原文保留在root-second-pass-independent-review.json。主审修订文案、当前main值、SHA与比对结果见同名JSON。未改主MOD或候选。
