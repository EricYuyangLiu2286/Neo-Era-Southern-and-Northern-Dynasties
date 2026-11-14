# 03 大汉国旗

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [Toolkit 检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-13-great-han-flag/toolkit/toolkit-checks.json>)、[旗面预览](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-13-great-han-flag/flag-preview.png>)

## 现象与期望

蜀国称汉后国号已变，旗上仍写「明」。刘氏和魏鉴称帝共用一面黄底黑「漢」字旗。

## 原因

USM 的动态国名读取 `nesnd_postwar_great_han`，原有旗规只读吴廷身份和政体。七种专用属旗另在纹章内部固定绘制宗主的「明」字。

## 改了什么

新增「漢」字 DDS 及纹章。在 USM 旗规接入两条称帝路线共有的标记，同时设置宗主旗角。七种原有专用属旗各沿用自己的属地徽记及适用条件，在汉为宗主时改用「漢」字。

## 怎么复测

刘氏、魏鉴分别称帝，检查国家旗与属旗。另选复明核对明旗。可从已称汉且保留大汉标记的存档检查。脚本解析、国号标记、两条称帝调用、八组旗规、纹理资源路径及 DDS 十级 mipmap 已核对；Toolkit 两文件零诊断。

## 遗留问题

实际引擎中的旗面和属旗显示待实测；[事件链审计](02-trigger-audit.md)的其他缺口另行跟进。
