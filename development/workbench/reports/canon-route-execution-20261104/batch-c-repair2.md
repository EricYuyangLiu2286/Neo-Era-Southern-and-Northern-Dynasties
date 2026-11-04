# C批修复2

2026-11-04。root已批准原生字段/宏scope/BOM/五个action文本窄修。编辑阶段未运行测试。

- 删除不存在的building_military_shipyard_throughput_add；保留building_shipyard_throughput_add=0.15，没有改变已批准造船收益。
- AUS保证独立、支持独立的原生helper参数均使用稳定c:AUS；宏展开后不再依赖prev。其他参战资格不变。
- 31份owned脚本/本地化统一UTF-8 BOM；已带BOM文件不重复添加。
- 双语新增五个原生保护国action显示键，采用保护关系、建立/解除及终止通知的常规玩家术语。逐项补入writing-comparison。
- 原版opium严格scope告警尚未当作通过，留给重测后的原生AST/来源相等分类；kind5接口仍未实现，未填占位。

完成后重新冻结全部31份owned文件；旧红例、原始工具输出和前次冻结保留。
