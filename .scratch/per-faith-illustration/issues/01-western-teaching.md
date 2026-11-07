# 《西来的学说》事件插画

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [成品回读](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-per-faith-event-picture/revision-2/verification.json>)

## 现象与期望
以原版秋日仪式画的站位与用色表现西秦经师讲学，衣冠、建筑与听众礼节依作者参考修正。

## 原因
原事件引用 `asia_confucianism_shinto.bk2` 的神道仪式。初稿仍有祓串，讲学稿又保留了举掌合十与折叠软帽。

## 改了什么
从原片第150帧取构图，将神社改为中国讲堂，经师持书戴中央起棱、两侧系带的黑色儒巾。长者躬身拱手，青衣听者收手入袖。新增独立 DDS 和命名 GUI 窗口，`nesnd_per_faith.2` 引用静态插画。

## 怎么复测
重启启用主 MOD 的游戏，在《西来的学说》事件窗口查看儒巾、拱手与插画裁切。

## 遗留问题
已核对事件、GUI 与纹理引用，DDS 逐层回读通过；游戏内显示待作者复测。
