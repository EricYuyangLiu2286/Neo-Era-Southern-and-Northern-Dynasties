from japan_dev_context import *

# Preserve the completed prose receipt, which was updated after the candidate fork.
shutil.copy2(M/'.scratch/debug-release/issues/22-canon-prose.md',C/'.scratch/debug-release/issues/22-canon-prose.md')
write(C/'.scratch/debug-release/issues/21-japan-implementation.md','''# 21 日本日志实施与共同市场修正

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: claimed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: WORK/reports/japan-development-20261102/review-aggregate.md

## Result

独立候选 WORK/exports/japan-development-20261102-a 已完成25个新日志、三国产业、独立发展、文化团结、政治、朝鲜、外交和Lin任职链。保留既有崩溃/恢复机制。作者最新共同市场指令覆盖旧采购提案：采购模块完全撤回，未进入主MOD。既有商路改为认可实际共同市场；终止外交联络不再抹去经济稳定期。市场、价格、投入品与消费仍由原生机制处理。

866项外部检查、10项实际MCP查询通过；Tiger相对当前主版本553条继承诊断，新增0；最新Spec/Standards审查剩余0。原始开发父提交c4bbc194，交付基线38cf3ea；作者657键文案批次和原稿注释已保留。

主MOD合入和Git保存的实际状态以同目录报告 main-merge.json / git-delivery.json 为准。最终外部检查不等于引擎验证。观察者启动尚待完成，具体覆盖写入 runtime-observation.md；复杂战争/分封/统一与晚期人物分支并未因此全部实测。

## Authorization

用户允许全部更新、外部测试和文风审查完成后启动一次游戏，切入任意国家再观察者、五速运行留待用户。若启动失败/崩溃，按当次日志定向修复重试。QA操作入口仅在独立运行覆盖层，正式包不包含。

## Remaining work

印度/土邦/法国玩法与南朝新概率/密使仍在各自任务图，未由本次日本交付替代。
''')
mapfile=C/'.scratch/debug-release/map.md'
write(mapfile,read(mapfile)+'''
## 最新：日本实施与共同市场纠正（2026-11-02）

[21 日本实施](issues/21-japan-implementation.md)已完成代码与最终外部检查：25个新日志，866检查、MCP10、Tiger零新增，两轴复核收口。作者明确撤回采购/库存/预付款/履约模块；实际共同市场自然汇合生产和消费。商路条件与联络清理同时修正。实际主MOD/Git与观察者运行状态见任务21报告，不能用STATIC_PASS代替游戏验证。
''')
write(S/'references/active-work.md','''# 当前交接：日本实施与共同市场修正

Updated: 2026-11-02。当前任务为主MOD .scratch/debug-release/issues/21-japan-implementation.md；证据 WORK/reports/japan-development-20261102/。作者657键中英文案与制度批次已交付main，见任务22。新日本候选已包含该批，保留作者原稿和注释。

当前候选 WORK/exports/japan-development-20261102-a：25个新日志、三国产业、团结、政治、外交、朝鲜、Lin迁JIM及人物闭包已完成源代码检查。866外部检查、MCP10、Tiger零新增，最新两轴审查各剩余0。原开发父c4bbc194，合入基线38cf3ea；主MOD/Git实际保存以 main-merge.json / git-delivery.json 为准。旧build脚本不能重跑覆盖当前修补。

作者最新共同市场纠正是当前权威：撤回采购、预付款、定额交货、仓储与履约日志，旧模块从未进入主MOD。日本产业按实际市场贡献买卖订单；现有供给日志已改为直接认可共同市场，取消外交联络不清零经济稳定期。设计规则见 economic-agency-and-crises.md；旧方案采购段已改，拒绝的草稿只存报告归档。

游戏尚未启动。用户已授权完成更新/测试后仅启动一次，选择任意国家后切观察者并五速运行留待用户；失败/崩溃按当次error.log定向修复。运行后读取 runtime-observation.md，不能把此处旧的“尚未启动”当作新开局授权。正式包排除QA，运行仅使用独立最小观察者按钮，不加载历史夹具。

印度/土邦/法国与南朝概率/密使待办保持各自map，仍为方案。不要声称本轮已完成这些玩法，也不要重开已验证的进港、死亡或分裂场景。
''')
write(R/'release-notes.md','''# 日本日志与共同市场修正交付

日本三政权按资源发展矿业军工、轻工与粮食加工；独立后进入国家发展，另有文化团结、政治路线、朝鲜和外交协商。Lin摄政使用JIM，原有崩溃恢复保留；历史人物、迟答、换宗主、改制及灭国出口已外部复核。

作者纠正已落实：采购功能全数撤回，未进入主MOD。共享市场自然汇合买卖订单；产业完成不依赖宗主订货或答复。日本粮食条件读取实际地方粮价，次要市场成员的开港描述不再承诺掌握关税。既有商路直接认可共同市场，取消外交联络不再清零稳定期。财政补助、真实舰船交接及合法跨市场条约保留各自真实作用。

866项外部检查、MCP10查询通过；Tiger553条继承诊断/新增0；两轴审查收口。正式包无QA工具。完整证据见 review-aggregate.md、market-web-sources.md 和 market-model-native-review.md。引擎实际覆盖另见 runtime-observation.md，不宣称全MOD零BUG。

作者657键文案修订和现存游戏数据已保留。印度/土邦/法国新玩法及南朝概率/密使仍为待实施计划。备份、差异、Git提交和打包指纹见本目录交付JSON。
''')
print('Task, plan, skill handoff, and release records prepared; no game started.')
