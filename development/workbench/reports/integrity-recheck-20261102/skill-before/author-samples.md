# 作者样本与反例入口

原始目录：`D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/`。也可从仓库 `f18b6c4` 读同路径；使用前核验来源，不以当前同名键自动认定作者原文。

|类别|原始文件与键|对读重点|
|---|---|---|
|改革完成正文|`ce_cne_events_l_simp_chinese.yml` / `flavorCNE.3.d`|法案、人口摆脱宗族、进入城市与皇帝理想之间的因果；不缩成发契登记。|
|改革阻力正文|同文件 / `flavorCNE.4.d`|冷酷政治过程与阶层关系，法律、欺骗、争夺、暴力并列为具体手段。|
|选项|同文件 / `flavorCNE.4.1`|“胡言乱语，正不必忧心。”有说话人的立场；不改成助手式后果预告。|
|日志正文|同文件 / `ce_cne_land_reform_reason`|从西秦革命、土地所有权到牧仲棠恢复运动的历史过程。|
|历史叙事|`ce_usm_events_l_simp_chinese.yml` / `flavorUSM.4.d`|郑昭觐见、军队与属地细节、流民和集权变法；长段不等于冗余。|
|朝争日志|同文件 / `ce_usm_conflicts_within_reason`|由“明朝朱姓，还是吴国郑氏？”进入社会中的争论，有具体场所和传播形式。|
|政治按钮|`ce_french_empire_journals_l_simp_chinese.yml` / `ce_french_support_dynasty_button_desc`|明确阵营立场，按钮正文不是中性的规格表。|
|进度条|同文件 / `ce_french_empire_oreleans_progress_bar_desc`|原生百分比、当前值与总值；来源明细在进度条代码中。|

历史对读记录：`WORK/research/20261031/replace-style-review/逐类对照.md`。该文件保存了当时的失败候选，不是可直接照抄的合格文案；其中“本轮候选”可能早已被改正。作者风格研究保留在 `nesnd-victoria3/references/author-prose-profile.md`，本技能负责实际写作流程。

## 已确认的返工模式

- 原文谈土地商品化与劳动力自由，候选却只谈清丈、盖印、核册：主题被缩小，须按原文重建因果，不补几个宏大词了事。
- 原文引文为有归属的誓言，候选改成没有事件功能的廊下领契场景：改变了字段用途，不应把场景描写当默认风味段。
- “统计范围与地方困顿判断保持一致。推进中的子项目才增加改革进度；暂停不清空已有进度”：面向开发者。统计只保留读数，进度来源用原生条，机制名称用“地方失序”。
- “多组符合时仍只计算一次。两项可以同时生效”：若前文已说“任一”且规则可并存，这些句子重复。保留真实而不可推知的互斥限制即可。
- “继续决定改革成果”“按原规则增加压力”：叙述版本变化，玩家无需知道旧实现。删掉更新视角，直接写本次可见的事实或效果。

本表不限制作者在人物台词中使用“不是”“继续”等普通词。判断句子承担什么工作，不能靠关键词替代编辑。

## 代价承担者对读

2026-11-02西秦“责令议法”：初稿写“军府与军士”，实际effect降低军队与地主支持；改为“军府与地主”。作者地权革命正文逐一指出转出与取得利益的阶层。写按钮时据effect点名实际承担者，不能用相近政治名词替换。完整原文与逐条复核见 WORK/reports/qin-persia-20261102/writing-comparison.md。
