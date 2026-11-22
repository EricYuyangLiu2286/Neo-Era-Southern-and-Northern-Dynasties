# 114 「伊犁的朝议」三方份额的概念与修正

Record: implementation
Category: enhancement
Status: ready-for-human
Assignee: Claude

西秦「伊犁的朝议」的三条势力读数（皇权、地方士人、军队）玩家看不出有什么用。三个名字做成概念 `concept_nesnd_qe1_crown`、`_literati`、`_army`（`common/game_concepts/nesnd_qe1_court.txt`），进度条名字链接概念，悬停看一句话的结果说明。三方各加两个固定数值的静态修正（份额 ≥ 50 挂 `_high`，< 50 挂 `_low`），由新效果 `nesnd_qe1_refresh_court_modifiers` 在 `nesnd_qe1_compute_court` 重算与奖掖清理之后挂换；朝议不成立时周脉冲清除，结局与开局引导里的 `nesnd_qe1_archive_court` 也清除。结局「终止后」原先没有可见效果，补了一句具名提示。份额算法、朝争、奖掖、改制按钮未改。

工作台记录：`reports/2026-11-22-qe1-court-concepts/交付记录.md`。进度条名字的概念悬停、修正显示、`state_` 修正作用到各州、结局后修正已清，待实机。
