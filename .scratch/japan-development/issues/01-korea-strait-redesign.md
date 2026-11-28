Record: implementation
Category: enhancement
Status: ready-for-agent
Execution: completed
Assignee: Claude（脚本经 agy，文字 Claude）
Blocked by: none
Validation: STATIC_PASS
Evidence: <D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-27-jp-korea-redesign/交付记录.md>

# 01 重做日本日志「海峡彼岸」

## 1. 现象与期望（作者原话，2026-11-27）

「开局朝鲜领土除了没有整合外，没有明显的 DEBUFF……日志奖励没有写明到底解决了什么问题」；「按钮写的奖励完全是负面」；「0/12，但是具体什么是完成条件没写明」。要求：开局给朝鲜属地挂真正的负面修正，两条路线二选一、选定不改，进度条用「推进条件」显示每月增减，三种结局加两种失效，结束后不再开启。

## 2. 原因

旧日志只有月检变量 nesnd_jp_korea_months（满 12 再点按钮），玩家看不到条件，开局也没有要解决的问题（common/journal_entries/nesnd_jp_korea.txt 旧版第 13–20 行）。

## 3. 改了什么

- common/history/countries/jap - japan.txt：开局给庆尚道、全罗道挂「武士代官在朝鲜的统治」（不可整合）。
- common/journal_entries/nesnd_jp_korea.txt：重写。挂「朝鲜的丰臣派大名」，月度补挂武士代官修正，六个结局（归还失效、失地失效、失败、科举成功、关白成功、invalid），任何结局设 nesnd_jp_korea_closed。
- common/scripted_progress_bars/nesnd_jp_korea.txt：新建进度条（0–100，固定 −3，科举五行各 +1，关白四行各 +2、动乱 −10，第三至五个朝鲜州各 −0.5）。
- common/scripted_buttons/nesnd_jp_korea.txt：两按钮改为二选一、选定不改；删除呈交税册、议定学款。
- scripted_effects / scripted_triggers / script_values / static_modifiers / on_actions 的 nesnd_jp_korea.txt：按新设计改写，删除旧月检、冷却、州变量和重开日志的调用。
- events/nesnd_jp_coast.txt：.1、.2 改为两条成功结局的弹窗。events/nesnd_jp_court.txt：删除 .2。
- 国民团结：科举成功时有国民团结日志就设 nesnd_jp_cohesion_korea，进度条多一行 −0.15。
- 中英本地化：本日志全部玩家文字重写。

## 4. 怎么复测

1836 开局 JAP：查庆尚道、全罗道有「武士代官在朝鲜的统治」，日志进度 0。选「开放高丽科举」后看进度条推进条件五行，选后另一按钮不可点。交付记录第五节有 20 个情形的预期结果。

## 5. 遗留问题

- 未开游戏。进度条包在 owner 里的写法、if 能否藏住推进条件行都没实测（C5 用了把路线写进每行 limit 的写法）。
- 旧档：已经走过旧结局的存档没有 nesnd_jp_korea_closed，仍持有两州时日志会按新设计重新出现。
