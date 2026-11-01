# 中国女性发型：A原生对照与B编码收口

A 的同人物原生对照已通过。主控在 GAME 1.13.11/build24799966、EACR1.0.4先加载的条件下，以同一原生存档、同一人物3124牧沐子、1836-01-01暂停状态比较：sequence A 无头发；female-hair A 恢复完整头发与花饰，脸、服装、年龄21、老秦文化、儒经宗教和身份保持一致。乡村民众群像女发也恢复。独立读取两张原始截图确认这一差异。

证据：`WORK/reports/runtime/20261101T012826Z/evidence/mu-muzi-before.jpg/json` 与 `WORK/reports/runtime/20261101T013305Z/evidence/mu-muzi-after.jpg/json`。两个 run.json 的源manifest与各自冻结运行副本逐文件一致；两份加载存档 SHA 都是 `fba18150b6b8ba22e3e847cbde354b4cc6307a096f7ff52a4c8c709dc60c3ba5`。绑定报告为 `female-hair-20261101-a-native.json`。

去掉时间戳后逐行对比原生 error.log，A 相对基线只新增一条本次新增 modifier 缺 UTF-8 BOM 提示，未删减基线任何错误。已把这两份原日志快照保存在本证据目录。该结果确认修正前后当前肖像行为，不代表全部帽饰、儿童、男性、新局、走时或存读档场景全部通过。

主控要求保留 A 原样，新增 B 仅修编码：

- A：`WORK/exports/female-hair-20261101-a`，SHA `8794f72ab8dd92a34bbe39e48d39f6f6f2bbf5e1e95a9e1efed5c2ac4f05e156`。
- B：`WORK/exports/female-hair-20261101-b`，SHA `2579d29090c8ee4356fc8172d3b977e2810e566087cbe2fd2714b0658efa1e77`。
- 两者均533文件。唯一差异为 `gfx/portraits/portrait_modifiers/EACR_hairstyles.txt` 前置 `EF BB BF`，增加3字节；其余文件含metadata完全相同，完整保序AST相等。A未修改，依赖和运行冻结副本未修改。B目录是新的冻结对象，launcher显示名仍继承A，由绝对路径/manifest区分。
- 生成/复核工具：`WORK/tools/build_female_hair_bom_20261101.py`。B完整manifest和断言：`female-hair-20261101-b-build.json`。
- A原生部分成功备份：`WORK/backups/checkpoint-female-hair-native-partial-a-20261101T013935Z/mod`。
- B编码checkpoint：`WORK/backups/checkpoint-female-hair-bom-b-20261101T013941Z/mod`。

当前任务等级为 **ENGINE_PARTIAL**：A的同档女性肖像场景PASS；B只证明编码修正/AST等价，尚待集成版本冷启动、新局/走时和重载复核。仍要求EACR→候选的联合加载，不冒称已有单MOD回退，也不改人物身份或搬运工坊素材。
