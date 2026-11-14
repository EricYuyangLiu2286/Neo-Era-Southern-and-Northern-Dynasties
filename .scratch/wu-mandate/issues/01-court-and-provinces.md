# 01 · 朝廷与外省的事权

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [清单、改前与改后内容树、游戏外检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-never-wu-agenda/report.md>)

## 现象与期望

作者要求「礼法之下的生活」具备中央和地方的平衡玩法。玩家可以切换支持方向，两端都有收益与代价，现有工程的选择也要影响进度条。

## 原因

改前总页负责发起四阶段工程与书院交流。各阶段有自己的进度与成功结局，总页没有事权指标。

## 改了什么

五份 `common/*/nesnd_civic_routes.txt` 加入 0–100 的原生双向条和两个互斥开关，十种工程在开工后推动同一条。按分数切换四档互斥国家修正，离开日志时撤除。中英本地化补齐了立场、条面、工程提示、修正及总页说明。

按作者要求，四档收益与代价在初版基础上提高 66%，再将幅度向上取到 5 的倍数。普通档为 10%，强档为 20%。朝廷的税收浪费分别为 5 和 10 个百分点。已核对 32 个修正数值及两语提示，见[原版同项数值对照](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-never-wu-agenda/vanilla-balance.md>)。

## 怎么复测

在符合资格的战后吴国或明廷打开总页。从 50 选择六部统筹，两个月到 60 时查行政力、建设和税收浪费。直接切换外省，再点一次停止，核对分数保留。检查 40、25 两档，分别从总页与子页采纳不同方向的工程，在有旧活动总页的存档复查初始条面和立场按钮。

## 遗留问题

尚待游戏内确认条面、月度结算和经济读数。工作台已另列地区治理与全 MOD 的“永不”展示问题。
