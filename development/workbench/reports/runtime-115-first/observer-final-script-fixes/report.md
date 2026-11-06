# 冻结观察者日志中的复国地块与西秦团结度

2026-11-05，Victoria 3 1.15.0，Steam build 26453692。分析使用 `observer-final/after-save` 的两份 error 轮换及 debug/game 镜像，未操作游戏或读取运行中的日志。以下均为主 MOD 离线修复。既有代理模型与推理强度未公开。

复国战争曾在州作用域调用 `every_province`。冻结 error.1.log:29 的引擎校验对此报 state vs province。当前导出的 effects.log:2664 正文仍描述从州取地块，列出的可用作用域却是 province，目标为 state。本轮绕开矛盾接口，调用引擎实际注册的洲级地块迭代器。仅在对方实际有领土的洲枚举，按当时真实所有者筛选，保存稳定的地块对象。亚、美、欧、非四组在 MOD 有效地理和战略区域中恰好一次覆盖全部694个1836有主地图地区，大洋洲已包含在亚洲组。初始/变更才需新建名单。若名单为空或与所存实际地块数不同，末次归属证据不足时不发奖励，对手尚在则可自动重建。分州合并或已死亡国家失去 State 对象不影响完整旧名单的逐块认定。

同样的失效 `every_province` 还出现在美国对东洲的边境要求。改从美洲实际地块中只取选定东洲 owner-state，核对已登记数等于该州地块总数后发起外交博弈。不同所属国在同一地图地区的部分保持独立。

冻结 error.1.log:66–70 另指向西秦 `primary_cultures_percent_country` 缺 `target_country`。现在分别读取当前国家各个主流文化在本国的人口比例，加总得到实际份额。采用本体已存在的数值形态 `culture_percent_country(prev)`，保留原公式 `(主流文化总份额 − 0.65) × 0.8`。单主流、多主流、无该文化人口及恰好65%都可计算。

主 MOD 受影响的四个文件与修改前后 SHA 见 verification.json。before 保存四份修改前字节副本；sources.md 给出当前游戏例子和引擎导出位置。复验从主 MOD 运行 `python ../../nesnd-workbench/reports/runtime-115-first/observer-final-script-fixes/verify.py`。49项通过，包含前轮17个战争/回调场景、手工吞并、第三国获得一部分、跨洲、残缺名单、USA实际州边界及西秦系数。三种内部故障注入证明漏掉所有者过滤、取消数量核对、更改西秦65%基线可被发现。`war_runtime_115.py` 在本轮目录内扩展原有 AST 子集测试器，保留上轮报告。地理迭代的实际引擎执行、存档变量读取及UI展示仍待有授权的后续局验证。

其余冻结脚本位置已逐堆栈对照。法国 scandalous、add_modifier 七处交法国分工。州事件 paralegal_discrimination.1 把州直接送入法国国家 AI 谓词；本 MOD 同路径 helper 的两段与本体一致。秘玻参与国重复、两个帝俄法令的失效国家、两次流亡煽动者无有效利益集团均落于未被主 MOD 覆盖的原版文件，相关堆栈没有直接 MOD 调用来源。未据此更改这些原版正常链或改动国际关系。未作 Git 操作。