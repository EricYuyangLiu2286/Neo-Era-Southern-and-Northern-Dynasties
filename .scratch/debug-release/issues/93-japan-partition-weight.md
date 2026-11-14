# 93 提高日本三家分封各路线的机会

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（1.15.1，有序解析与改前逐项比对）
Evidence: [本轮三文件备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-japan-partition-routes-20261112T144652Z/manifest.json>) · [Toolkit 零诊断](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-japan-partition-routes/toolkit/toolkit-checks.json>)

## 现象与期望

作者要求增加所有既有分封路线的机会。第一轮仅调了日本直接接受国书。

## 原因

靖难中日本实际反吴并战败，可以进入吞并、重建、分封。拥吴参战遇战平，九州交涉又可引发吴重新收日本为保护国。东洋之议另有直接同意、拒议开战及提出反案后吴决定出兵三条路。议案开启期间日本重新臣服，或满足重建条件后，已有回调自动分封。

## 改了什么

- `events/usm_civilwar_events.txt`：靖难拥吴、反吴、中立从 45/30/25 调为 50/40/10。战平后，若吴仍有机会通过重新收日本为保护国实现分封，且两个选项均可选，吴要求建立保护国的概率从 70% 升到 80%。
- `common/scripted_buttons/nesnd_japan.txt`：发国书的 AI 值从 30 提至 60，对原反吴日本从 40 提至 70。协商期后，维持现状的三个非零 AI 值分别从 2/8/5 降至 1/4/3。
- `events/nesnd_japan_events.txt`：保留第一轮将直接分封基础权重从 30 调到 90 的改动。降低日方反案权重，提高吴收到反案后决定出兵的权重。下表从同一封国书算起，以第一轮开发版为对照，假定日本三项回复及吴方出兵均可选。

| 路径 | 第一轮开发版 → 本轮 |
|---|---|
| 日本直接接受（日军较弱／不弱于吴） | 61.11% → 63.22% ／ 50% → 51.72% |
| 日本拒议东征（日军较弱／不弱于吴） | 22.22% → 22.99% ／ 33.33% → 34.48% |
| 日本提反案且吴坚持东征（非赤字／赤字） | 8.33% → 11.82% ／ 4.63% → 10.61% |

已按解析后的两个版本分别计算军力和财政四种组合。军事路径的数值截至选择出兵，后续需成功创建博弈并兑现要求。战争胜利、归属、重建和原宗属条件沿用原脚本。

## 怎么复测

靖难选边需读日本答复前的存档；保护国分支需在战平的九州交涉前；国书分支需在东洋之议决策前。已作出的选择不会重抽。

## 遗留问题

没有启动游戏，整局出现三国结局的频率尚未实测。
