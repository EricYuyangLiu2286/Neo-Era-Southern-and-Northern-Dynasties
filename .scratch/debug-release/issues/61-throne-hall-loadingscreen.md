# 61 宫殿加载画面

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [纹理回读记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-throne-hall-loadingscreen/verification.json>)

## 现象与期望
将作者提供的宫殿图作为一张新的加载画面加入主 MOD。

## 原版依据
1.15.0 的 `gfx/loadingscreens/loadingscreen_settings.md` 说明该目录中的 DDS 自动加入候选池。前端 `frontend_loadingscreen.gui` 使用 `[GetCurrentLoadingScreen]` 和 `centercrop`。游戏内加载界面复用 `widget_loading_screen`，另加左下角提示。

## 改了什么
新增 `gfx/loadingscreens/nesnd_imperial_throne_hall.dds`，沿用默认抽取权重。纹理为 1672 × 941，像素格式与原版 `victoria3_load_1.dds` 一致。11 层 mipmap 完整，最高分辨率回读的 RGB 与原图逐像素相同。

## 怎么复测
启用 MOD 后重启游戏，在启动或读档的加载画面中观察随机轮播。可用已有存档。

## 遗留问题
游戏内抽取和显示效果待实测。
