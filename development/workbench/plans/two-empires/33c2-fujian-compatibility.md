# C2 的福建新局兼容增量

输入均为冻结版本：政治父 `court-reconciliation-20261031-c2`；地图补丁 `fujian-split-20261031-b`，它的真实父为 `hus-pm-format-closure-20261031-a`。输出独立 `court-fujian-compatibility-20261031-a`；不修改活动 runtime、不加载旧档、不改主 MOD。

合并按地图补丁的父差分执行，冲突必须停止。输入 manifest 核实后，地图/人口/建筑/交通/本地化/公司语义引用保留福建B结果；C2政治文件仅增加 `STATE_NORTHERN_FUJIAN` 到中国地理集合，并将字面迁都映射从794重生为795个有效地区。其余政治AST必须与C2相同。

依赖图：福建31province→北16/南15及各hub→定位与splnet陆海路→state/pops/buildings守恒→战略/地理/公司/完整控制触发→南朝政治地理白名单→迁都applied守卫。对白名单作“范围新增一州”，不扩展国家同意或政治票组。

本地验收：所有冻结输入指纹不变，地图资产与福建B逐文件相同，新增ID3172唯一、795映射精确覆盖，首都写入对该字面州可达且保留applied旗，其他C2政治AST不变；重复运行交通preflight和Tiger增量，并核参考账簿和省色/人口/资源守恒证据。原版公司旧modifier诊断单独分类。

引擎验收另开新局：两福建人口/产业/市场/军队，陆上移动、北港进出和保存读取；真正迁都测试命中3172并设置applied，再测混合领土和平移交。静态覆盖不代替这些实际结果。


## 已冻结结果

候选court-fujian-compatibility-20261031-a，父C2；484文件、27差异，独立备份candidate-court-fujian-compatibility-a-20261031T201357Z。static.json含完整三输入/输出指纹，diff是C2→地图增量。地图游戏文件与已审福建B完全相同；候选metadata和EDITOR-REVIEW更新身份与合并义务完成情况。独立人口9群体11,324,832守恒，15州交通图重新通过。

map_workflow只读复核PASS，证据court-fujian-map-workflow-review.json；names_and_testing语义与坐标复核无阻断。附属方同意、四立场、王室、战争/和平控制器AST保持C2，只有白名单增加北福建与795字面首都分支。当前运行组合中的L2四州arable标量等来自另一父链，根合并时必须保留，禁止整目录覆盖活动QA。

坐标表述：部分旧视觉locator保留，陆路anchor按locator重新对齐。旧wood49804 anchor存在小幅对齐，北mine/farm亦保旧locator而非旧anchor；原港49803和city49800完全保留。不得把“保旧视觉位置”误写成所有旧交通anchor不变。此说明不修改冻结游戏图。

实际新局/行军/航行/地图重新载入/3172真实迁都尚未验收。最小入口见evidence/court-fujian-newgame-checklist.md；不得加载当前无新地图G0旧档来认证拆州。
