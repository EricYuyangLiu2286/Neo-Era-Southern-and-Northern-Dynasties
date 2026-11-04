# 最终文案独立复审：需返工（2项P2）

对象：`final-button-preview-20261104T192525Z/mod`。本轮为旧Standards P2闭合及最新文字差异复审；原Spec零发现报告保持历史，不回写。

1. **WR-01，意大利共用叙述误把开支等同共和事业。** `localization/{simp_chinese,english}/replace/nesnd_civic_routes_l_*.yml:12`：“政府把钱投向何处，也就在选择今后的共和事业将依靠谁。”真实入口 `common/scripted_triggers/nesnd_civic_routes.txt:1–4,31` 不要求共和：SIC君主制、PAP神权制都可投资军需/学校，实际effect不使它们支持共和。两个characters文件`:21`的`.102.a`同样把唯一后续回应写成共和教育；Bellandi可在非共和国家出现。违反写作技能§4“内容与视角/脚本契约”。保留LOM法国支持的历史及人物个人共和观点，修正共用的当前国家立场。

2. **WR-02，HUS新稿把未保证的当前政体写成共和国。** 中文routes`:40,65,79`、英文`:79`及两种characters`:79`，例如“共和国须为所选的办法承担开支”。`nesnd_hus_civic_country`只查原HUS身份/非临时革命（trigger`:5`；registration trigger`:2–5`），不查政体。原HUS经普通立法改君主制、保留登记制度，有油井与科技仍符合oil入口`:96`。违反技能§3–4条件与事实须对应脚本。当前主体宜用政府/国家或已证动态名称，历史渊源不必删。

已对读全部最新342键改稿及显示修复142值，包括10日志、18人活跃/离场与选项、27按钮及必要TT；与真实trigger/effect/modifier核对。作者样本来自不可变pre-update备份的CNE地权改革、USM朝争及法国政治按钮；已读南北制度文档。其余未确认新缺陷：议题已具体化，英文自然；东青行未断言现存公司承担工程，USM六部/礼议院/布政司/学政分工与资格事件相符，新TT只说明已有数值。

实际配置`gpt-6.1-sol / medium`，root NEW_TASK为委派证据。仅写报告；未改源码、未运行测试或游戏，ENGINE_NOT_RUN。四文案/相关源码及样本SHA详JSON。
