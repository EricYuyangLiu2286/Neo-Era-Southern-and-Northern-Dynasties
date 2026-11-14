# 63 主菜单主题规格与占位接入（第一步）

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [作图规格、定义位置与参考图](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-main-menu-theme/作图规格与接入清单.md>)

## 现象与期望
新增独立的 NESND 主菜单背景和简写角标。第一步只接占位图并交付绘图规格。

## 原因与接口
俄国主题在 `common/themes/00_themes.txt` 登记 IP5 Bink 视频。`frontend_main.gui` 的 `FrontEndMainView.GetMainMenuImage` 提供循环画面。俄国人物、城市和天气已合成在视频内。

## 改了什么
新增独立主题定义、Bink 占位视频、中英本地化两份。作者确定角标为「南 · 北」，采用玩家在 Theme 中选一次并保存的方案。Workbench 已存原视频副本、原尺寸合成帧、局部参考、七种 GUI 装饰及 4K 安全区模板。

## 怎么复测
主菜单 Theme → 主菜单背景 → 南 · 北（NESND）。查看角标、与俄国主题互切并重启检查记忆。游戏外已验证七个原版条目与新增条目并存，游戏同版解码器回读全部48帧。

## 遗留问题
正式成图待作者提供。主题列表与实际切换待作者实测；首次无存储偏好时的引擎排序无公开脚本保证。
