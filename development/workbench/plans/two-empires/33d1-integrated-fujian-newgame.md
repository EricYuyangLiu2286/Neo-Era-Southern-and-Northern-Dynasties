# D1 新局整合事务

当前操作只读基线 `exports/integrated-politics-phi-20261031-c2`，505文件，已冻结且被活动游戏加载，禁止写入。地图增量精确取 `court-reconciliation-20261031-c2` → `court-fujian-compatibility-20261031-a`，输出 `exports/integrated-fujian-20261031-d1`；合并配置保存在 `evidence/integrated-fujian-d1-merge-config.json`。

本次只合已评审福建地理与兼容闭包，不另改国家设计。必须保留基线C2政治、PHI A2实际协议、Chen G2预览守卫、姓名池；L2四州耕地须维持晋中297、燕京213、河间310、漠南122。地图其它差异来自福建B事务：新州3172、北16/南15province，795字面首都、51州中国白名单，原定位/重建对齐anchor的事实见33及33c2。

门禁：逐文件父差分/输入不变，指定模块字节不变，L2四arable及非福建地图AST不变；固定原始781地区人口75%–125%边界，分州合并回原父地区验算，不能给新州重置允许范围；15州交通preflight、项目region/history一致性、相对正在运行基线的最小Tiger增量。现有源支持角色与原版福州船政奖励诊断分类，不以静态通过冒充实机。

候选冻结前保存精确manifest与独立备份。仅新局测试；当前G0/Jan1旧图回归继续由根在无福建运行版进行。不得自动切换挂载或操作窗口。


## 20:51 UTC：D1 可复用的新局整合

已冻结 `exports/integrated-fujian-20261031-d1`。精确父为正在运行的 `integrated-politics-phi-20261031-c2`（505文件）；取 `court-reconciliation-20261031-c2` → `court-fujian-compatibility-20261031-a` 的27文件父差分三方合并，最终508文件。没有将旧地图候选整目录覆盖当前代码。

合并配置：`evidence/integrated-fujian-d1-merge-config.json`。最终父/候选/补丁输入manifest与检查：`evidence/integrated-fujian-d1-static.json`；精确代码差分：`evidence/integrated-fujian-d1.diff`。独立备份 `backups/candidate-integrated-fujian-d1-20261031T205122Z`。冻结后不要写入；后续补丁以此另建新候选。

本地通过：固定原始781地区均在75%–125%人口包络内（以原MOD+固定原版继承地域为基准，新州聚合回旧福建，不重置基准）；无未映射和缺理由。15州交通图零错误，国家province归属以及人口、PM、建筑级别、产权、资源总量守恒。非福建地区及其states/pops/buildings AST不变；PHI A2、护陈G2、姓名与军队保持当前父版字节。L2四州耕地准确保留：晋中297、燕京213、河间310、漠南122。

D1有效地区795、北福建3172、南朝中国地理白名单51；字面政治/市场首都及applied守卫完整。相对505文件父版，Tiger只新增已审的原版福州船政公司同内容ship_hull_damage_mult奖励诊断1条，未解释新增0；继承角色type=other等源支持诊断未隐去，不等于引擎零错误。

只用于新局，尚未实机。下一轮复用 `evidence/court-fujian-newgame-checklist.md`，先开未干预USM新局，再另存实际3172迁都/混合领土/行军航行夹具。当前无地图C2的G0、Jan1旧存档测试与D1隔离；不自动切挂载、不改活动QA、不合主MOD。后续PHI权限/船转若另有审定补丁，须按其真实父差分追加，不能假定D1已含尚未实现内容。
