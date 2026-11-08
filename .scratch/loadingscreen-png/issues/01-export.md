# 01 两张加载图导出

Record: implementation
Category: enhancement
Status: ready-for-agent
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [导出目录](../../../gfx/loadingscreens/)

## 现象与期望

把 Loadingscreens 的两张图另存为 PNG，每张小于 2 MB。

## 原因

两张 DDS 直接导出全彩 PNG 时均超过 2,000,000 字节。

## 改了什么

从 DDS 最高分辨率层导出同名 256 色 PNG。宫殿保留 1672 × 941，成都从 3840 × 2160 等比缩至 2304 × 1296。

## 怎么复测

使用 Pillow 校验 PNG 并重新打开完整解码。宫殿为 1,062,260 字节，成都为 1,954,019 字节。

## 遗留问题

无。
