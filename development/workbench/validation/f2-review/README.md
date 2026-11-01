# F2 最小闭包修复与证据分类（玩家续玩修复前）

本轮只在独立 F2 加入简中/英文 concept_geogregions → $concept_georegions$ 兼容别名及 F2 身份。原版、F1、人口、地图、历史、玩法脚本未因此改动。主控同步的 AGENTS/docs/.scratch 文档已包含在本次全量指纹中。

## 已完成

- 完整字面闭包实际重跑：content-before.json 中 hard_errors=1，content-after.json 中 hard_errors=0；review_findings 仍为2406，未删除或忽略既有待审项。别名两语均有 BOM/正确语言头；原版两语 concept_georegions 都存在，未改作者文本。
- Tiger 分类按精确诊断签名、候选源文件SHA和来源证据SHA匹配。旧 E1 审查只复用源文件未变的项；17项源漂移不继承原分类。不同token、源漂移、证据漂移/缺失均不能被豁免。
- 原版 annex_country 的 on_enforced 为空；排除原/新两者的 on_enforced 后，F2战争目标的完整有序AST与当前原版相等。5条enum/target_region诊断因此记为当前源码规则差距；这不认证新callback的执行。
- 俄罗斯空if仍记 confirmed_inherited_defect，未移动500权重；26处人物ig访问不能统称已修或已验（22项继承精确旧审查，其余源漂移保留待审）。3条新波兰brace提示以完整可解析事件文件SHA单独归类。
- 证据匹配适配器10项回归通过，包含真实5条annex报告和1条俄罗斯诊断。实际输出保存在 tiger-review-regression.json。
- 原 review-register.json / toolchain-frozen-current.json 未覆盖；旧 runner 和登记副本保存在 tooling-before/。

## 集中检查结果

`../runs/f2-global-20261101-before-player-fix/report.md`：17项中13 PASS、2 FAIL、2 NOT_RUN。真实MCP、固定人口、历史顺序、生产资源、地图海域/交通、字面闭包及候选/工具完整性通过。

Tiger相对F1新增0；总数仍为5 errors / 967 warnings / 1 tip。17条warning未分类，563条已有具体审查但尚未解决，多数是重复调用链的共同问题，不能当563个独立BUG，也没有被豁免成PASS。

语义登记中的旧.4玩家失败选择缺口保持FAIL；日本原生恢复及Lin待实机；旧.20零字面调用只表明legacy源码入口不完整，不能据此证明不存在动态分派。其状态为NOT_RUN，已按主控要求在生成后收窄。玩家续玩修复将另建候选，不能改写本报告为已修。

## 下次使用

运行global_validation_runner.py时明确传入：

- --review-register WORK/validation/review-register-f2.json
- --toolchain-manifest WORK/validation/toolchain-frozen-f2-20261101.json
- --baseline 精确父候选
- --out WORK内尚不存在的报告目录

22项工具已冻结；源文件变化会使相关已审项重新NOT_RUN。若修改工具，先局部回归并建立新的显式冻结清单，保留本版证据。

此结果尚无F2引擎运行绑定，不能标accepted。接下来由主控运行真实callback/玩家失国、Lin、海运和受影响既有机制；文档/工具的通过不替代这些门禁。

本次精确候选指纹：`416ac54f8fb9f4c4ab1c86266519b517724f9f78a9a396e4579342774fb9353f`。
