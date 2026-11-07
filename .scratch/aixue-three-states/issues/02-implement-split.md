# 皑雪三州实施

Record: implementation

Category: enhancement

Status: ready-for-human

Execution: completed

Assignee: Codex

Blocked by: none

Validation: STATIC_PASS

Evidence: [交付与检查证据](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/aixue-split-20261107/皑雪三州交付.md>)

## 现象与期望

按作者确认的方案将皑雪分成玉京、朔海、林莽皑雪；新开局守恒重分人口、资源与建筑。

## 原因

旧 STATE_ALASKA 包含 1,028 个不同省份；枢纽与海陆交通需随新界一同迁移。

## 改了什么

36 个游戏文件，逐项处理见上方交付说明。三州全部归 HUS，合计人口 368,028、建筑 10 级。

## 怎么复测

1836 新开局查看三州，核对港口产权、枢纽、出海、陆路及市场，存读一次；有条件再测释放、拒绝和成交。

## 遗留问题

未启动游戏，待作者新局验收。既有差异与工具版本限制已列入交付说明。
