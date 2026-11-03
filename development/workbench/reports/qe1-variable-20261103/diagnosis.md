# QE1 数值变量缺失报错

读取 20261102T234900Z 隔离运行的 error.log 与 error.1.log，保存原日志；主用户目录旧 error.log 时间较早，没有冒用为本次运行。两份保留日志共4827条脚本错误，其中4824条对应本次修复：unity三处读取各产生524组错误，war_months两处读取合计36组；其余3条是原版秘鲁/玻利维亚重复加入日志参与国，另列但不混入本次变量修复。

## 原因与证据

按顺序检查了：未激活日志的求值、初始化遗漏/旧档缺值、变量所属scope不符。

实际1836.3.1 autosave中，唯一存活QE1有campaign_v1，unity为70.50745，war_months/uprising为0；只有QE1团结日志active=yes。与此同时保存了526个团结/暴动JE实例，其余525个未激活，其中包括英、俄、法。结合重复报错和实际源码，问题是进度条script_value直接访问不具备西秦变量的上下文。JE的possible/is_shown_when_inactive不能充当数值读取保护；给所有国家初始化西秦变量会掩盖错误并污染状态。

未改初始化、数值、历史、人口、文化转换或进度推进顺序。四个script_value在独立has_variable分支内执行原计算，缺值时只返回0；不会set_variable为0。两条状态文字及暴动完成条件同样用trigger_if/trigger_else保护，缺值明确false。

## 原版链条

1.13.11 / build24799966：05_danubian_federation JE immediate设置count_integrated_cultures；00_victoria_ip3_scripted_effects变更计数；je_values的danubian_federation_remaining_cultures_to_integrate先查has_variable再读取；JE完成条件使用trigger_if。另对照ep2_japan_values的cached_daimyo_loyalty缺值分支。路径/行号/SHA见native-sources.json。进度条文档明确更新先于JE pulse。

## 验证

- check_qe1_variable_guards.py 修前FAIL：5处未保护；修后STATIC_PASS：8次变量读取均有分支保护。
- 46项结构/不变性检查通过：变量存在时原计算AST完全保留，只改变缺值路径；全common/events可解析，游戏内容只改2文件。
- 5项实际MCP结构查询通过。
- Tiger相对已交付版本553→553，新增0；不代表全MOD无遗留诊断。
- 没有启动或操作游戏、没有改存档或冻结运行副本。修后引擎结果待用户运行确认。

来源：runtime-save-evidence.json、error-inventory.json、guards-before/after.json、validation.json、mcp.json。保存的真实存档只读，报告仅存相关字段和SHA。
