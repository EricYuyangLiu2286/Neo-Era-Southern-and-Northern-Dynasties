# 按钮引用修复：供用户测试的主 MOD 交付

2026-11-01。用户授权修复上一轮代码审计发现的问题，备份后合入主项目，由用户自行测试。本轮没有启动游戏或修改游戏加载配置。

## 修复范围

- 外部援助：目标选择、援款/军火的供给与请求、AI周检查的缺目标保护；pending/双方sponsor与发起国安全校验；接受执行重新检查资格，取消/超时撤销事件，拒绝仅清理匹配请求。保留30天pending、6个月冷却、7天投递及原金额/货量。
- 土改、南明/吴、丹那沙林进度刷新：临时scope和数值存在后再读取；同形PHI helper也保护。按钮预览不会假定前面保存作用域已经执行。
- 丹那沙林的建设、培训、健康条件与地主协商：对象失效时安全返回false。
- 日本发送条件及实际执行：JAP不存在时不读取停战关系、不设置“已送达”标记或发送空目标事件；原吞并/恢复/Lin链保持原样。
- 法国打击共和派团结按钮：实际随机目标采用与可用条件相同的排除规则。
- 新的AI闲置周数安全getter；既有接口字段good/goods写法按各自引擎文档保留，没有机械替换。

## 检查与边界

53项针对真实源代码的守卫/选择一致性检查，旧版53项失败→候选0项失败；条约实际payload、保存的金额/期限、地图/历史/人口/图像/本地化和发布metadata的SHA一致。全common/events文本通过有序解析。Tiger零新增诊断，最终6 error、975 warning、2 tips；6条旧error沿用上次已有原版/工具差异分类，并非本次新增。4次实际stdio MCP嵌套查询通过。

这些检查不执行引擎。本批为STATIC_PASS / ENGINE_NOT_RUN，用户测试结果尚未产生，不声称error.log已经在实机清零。

Skill的核心入口和syntax-and-routing引用安全章节已更新，log-first-delivery链接该单一规则来源。记录对象/数值、嵌套guard、预览、过期请求、随机候选一致性、接口字段差异及保留引号的局部编辑方法。

## 保存与测试入口

主MOD原路径不变，正常加载组合不变；无需QA覆盖层。可以直接使用主项目测试上述按钮。旧存档里已经出现的错误不会被本轮倒推消除；新交互受修复代码保护，不修改已有存档。

完整修改前备份：WORK/backups/pre-change-button-guard-fix-20261101T093152Z/mod。
候选：WORK/exports/button-guards-20261101-a；独立候选/合入后checkpoint备份由backup.py生成。
正式包：WORK/releases/nesnd-20261101-button-guards.zip，工具/报告/任务文档/QA均排除。
逐文件合并和SHA：本目录main-merge.json；Git与远端结果：git-delivery.json。

## 原版与工具依据

GAME为本机Victoria 3 1.13.11 / build24799966，catalog CURRENT、changed0。原版events/commander_events.txt:57–61提供saved scope失效时cancellation_trigger；common/scripted_triggers/00_scripted_triggers.txt:44起为条件分支实例。已有供给预览原生日志与已修的supply helper提供本项目错误模式；本轮只修同类闭包。

WORK/references/engine-docs-1.13.11-20261031/triggers.log:8955与effects.log:1056分别约定good/goods；GAME/common/treaty_articles/13_goods_transfer.txt及history/treaties实例用于实际条约payload交叉核查。

旧审计：WORK/reports/button-code-audit-20261101/report.md。检查脚本：WORK/tools/check_button_guards_20261101.py。MCP浅层返回[block]必须继续展开key_path；本轮修正的是查询路径，不是为迎合工具改变脚本。
