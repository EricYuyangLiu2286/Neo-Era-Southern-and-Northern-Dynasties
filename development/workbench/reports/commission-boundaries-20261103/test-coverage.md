# 覆盖完整性审计

|层|本轮证据|性质|
|---|---|---|
|资格边界|boundary-cases.json，45场景＋5变异反例|执行真实AST子集，历史归属+显式fixture|
|请求身份与代价|request-boundaries.json，23场景＋serial变异|执行真实trigger/script_value；不运行事件计时器|
|清理幂等与失地退出|effect-boundaries.json，7重复清理及2退出路由|真实effect AST；旧源码反例和guard变异|
|建司阶段顺序|effect-boundaries.json，6创建/宗属结果场景|原生API结果注入，不模拟引擎内部|
|静态源契约|contract-validation.json 50、final-validation.json 326|操作符、祖先条件、有效原版文件、资源和双语|
|加载工具|mcp-final.json；tiger-added.json|真实源码查询与校验器，零新增诊断|
|引擎运行|没有新增|ENGINE_NOT_RUN，用户测试|

结论：已补齐本轮确认缺失的可外测边界，不能把静态/注入式测试称为引擎全覆盖。已识别且仍未覆盖的引擎行为列在release-notes.md。当前源码变化只绑定当前报告；旧484/326计数不独立代表测试质量。
