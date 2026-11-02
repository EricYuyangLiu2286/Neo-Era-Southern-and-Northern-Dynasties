# 共同市场：官方网络来源

2026-11-02读取。当前安装仍以GAME 1.13.11/build24799966为准，不因网络显示更新版本而更新用户游戏。

- https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-37-market-expansion ：2022-03-09；正文58–75明确成员生产消费归于同一国家市场，汇合买卖订单，接入受连接与基础设施影响。旧外交/贸易UI规则不当当前实现引用。
- https://steamcommunity.com/games/529340/announcements/detail/524212840420081890 ：2025-03的官方DD143；检索返回官方正文，直接open只提取到图片。世界市场为自主跨市场贸易层，国家市场仍处理人口和建筑的交易；1.9改为贸易中心驱动。
- https://vic3.paradoxwikis.com/Market ：401，未取得正文。猜测Paradox DD143路径无法访问，未当已读来源。

本轮实现遵照用户纠正撤销采购模块。判断实际价格、产量、市场归属、州接入和原生条约接口，还须对应本机源码；相关引用由market-model-native-review.md保存。
