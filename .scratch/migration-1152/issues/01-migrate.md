# 01 · 迁移到 Victoria 3 1.15.2

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Assignee: Claude  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [迁移报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-19-game-1.15.2/迁移报告-1.15.2.md>)

## 现象与期望

作者：“游戏从 1.15.1 更新到了 1.15.2。查清这次更新对 NESND 的全部影响，修掉失效的写法，然后把 MOD 的支持版本改成 1.15.2。”1.15.2 的 error.log 比 1.15.1 多出七组、18 条与版本有关的报错。

## 原因

- 1.15.2 删去了附属国类型键 `breaks_if_subject_not_protected`，“宗主不保护附属国即脱离”的规则整个取消。法律组键 `affected_by_regime_change` 改为 `regime_change_min_progressiveness_difference`。
- 本体改了 MOD 整文件覆盖的 24 个同路径文件和 `map_data/provinces.png`。新增的触发器、on_action 挂接和两个事件，被 MOD 的旧副本挡住了（`common/scripted_triggers/00_scripted_triggers.txt`、`common/on_actions/00_code_on_actions.txt`）。
- MOD 用 `REPLACE:` 覆盖的 7 个原版对象在 1.15.2 有改动。
- `gui/ingame_hud.gui:71` 的报错来自作者启用的工坊 MOD「Console Access」（3085120028），不是 NESND 的。

## 改了什么

作者定的原则：本体的开局数据不进 MOD 的世界，本体的机制修正照收。

- **被删的键**：4 个法律组删 `affected_by_regime_change = no`（新机制下不写即不强加，行为不变）；5 个附属国类型删 `breaks_if_subject_not_protected`。
- **同路径文件**：on_action、触发器、AI、两种意识形态、港口与贸易中心、波兰事件，与本体三方合并。开局建筑、关税、城市中心等 13 个历史文件保持迁移前的样子。
- **开局贸易**：14 条全部注释，保留空文件以挡住原版表。删去英国开局的鸦片出口补贴。
- **俄国「东部边界」日志**：停用（`common/journal_entries/nesnd_rus_regional_compat.txt`）。
- **地图**：`map_data/provinces.png` 厄勒海峡 17 个海域像素，改为本体 1.15.2 的归属。
- **REPLACE 对象**：福州船政局、AI 触发器 `has_je_conquest_reason`、俄国东部边界三个按钮，合入本体改动。
- **版本号**：`.metadata/metadata.json` 支持版本改为 1.15.2；STATUS.md 更新基线；技能条目按核对结果改写。

## 怎么复测

新开局后读 error.log：上述 18 条里，Console Access 的 2 条还会出现，其余 16 条应消失。各国开局建筑与关税应与迁移前相同，俄国没有「东部边界」日志。细项见报告第 8 节。

## 遗留问题

未启动游戏，未实机验证。
