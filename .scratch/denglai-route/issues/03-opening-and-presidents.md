# 03 登莱历史入口与两位开局周公

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（1.15.0 / 26453692，补丁待实机）  
Evidence: [验证与文件清单](<../../../../../nesnd-workbench/reports/denglai-route/presidents/verification.json>) · [内容树 near](<../../../../../nesnd-workbench/reports/denglai-route/presidents/near.json>) · [首轮实测日志](<../../../../../nesnd-workbench/reports/denglai-route/presidents/before-logs/error.1.log>)

## 1. 现象与期望

作者的开局截图确认寿汴辩已任周公，生效日志中未见「雪国共和」。要求改用法国式历史入口，并保护寿汴辩、郭庆达参加开局后的三次选举；允许提前落选。

## 2. 原因与来源

首轮 error.1.log:1172 报根日志缺 activation_description，3435 报重复添加；旧版显示和激活条件均恒假。原版说明显式添加会跳过这两个条件；仅凭报告无法断定哪一项令 UI 漏显。法国国家历史第 126 行显式添加，法国日志自己处理激活和开场事件。同次 1117、1122 还报迁都 level 与法律 type 的作用域错误。

寿汴辩沿用 SHA_bianbian（nesnd_asian_historical_leaders_overrides.txt:1296）：47 岁、华北、山东籍、文人领袖、共和主义者、谨慎。郭庆达沿用同文件第 1092 行的 HUS_Guo_qingda：60 岁、辽东、大原籍、实业家领袖、激进派、谨慎。两人原有 ruler=yes，均未指定固定党派。众人共和国采用总统选任（00_ce_government_types.txt:101）；原版 government_l_english.yml:933 说明选举结束时由影响力最大的利益集团领袖任元首。

## 3. 改了什么

- 国家历史 common/history/countries/SHA.txt 添加开局身份和根日志。根日志补齐激活、显示和大厅条件，在 immediate 安排次日选路。移除旧开局回调与月度重复添加。
- common/history/characters/SHA.txt、HUS.txt 在既有人物创建时调用同一效果。新增 common/scripted_effects/nesnd_sha_republic.txt，登记有保护的本人、初始化各国独立计数、设置不朽并给其集团加成，另含统一撤销效果。
- 第一批同名的 on_actions 管选举计数、换人和改制退出。static_modifiers 增加集团政治力量 +50%，两种语言 replace 文件各加「周公的选举声望」一键。数值依据写入 numbers-v1.md。
- scripted_triggers 加原生登莱未结案的日志资格；events 的开局事件读同一资格。迁都改读现成的行政等级 script value；改制回调直接读国家当前法律。更新路线 map.md 和项目 STATUS.md。
- 备份 pre-change-denglai-presidents-20261110T205214Z。pdx.py、全量 audit.py 前后比对和内容树 index / near 均已运行。全量原有 138 项提示逐项相同。Tiger 1.19.0 将 1.15 的 activation_description 和三个 outcome 报为未知字段，已对照当前法国日志与原版。

## 4. 怎么复测

1. 新开局选 SHA，先看生效日志和寿汴辩，再走一天看「雪中的抉择」。文人集团应显示 +50% 的「周公的选举声望」。HUS 新局对应郭庆达和实业家。
2. 在各次选举前后留档，记录元首与两大集团的影响力。前两次连任应保留修正及不朽。第三次结算次日两项均应撤销。提前换人时核对卸任总统本人；继任者不获保护。调试检查项为人物 is_immortal、国家 nesnd_sha_elections_completed（从 0 起，结束后移除）。
3. 另用分档在保护期内废除选举或强制改为非共和。走过次日后看原总统与原集团；恢复原法不应重开保护。迁都有条件时复测原行政等级是否转入新都。

## 5. 遗留问题

补丁未启动游戏。须实测日志显示、开场事件唯一性、三次选举实际结果、强制换届/改制时序、人物不朽与撤销、迁都行政等级。+50% 为源码估算。第 2 批尚未开始。
