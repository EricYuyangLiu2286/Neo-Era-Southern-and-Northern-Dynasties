# Editor rounding 修复已整合

2026-11-01，用户明确授权恢复该子任务、外部测试并整合；未打开游戏或UI。

该任务修复离线地图编辑器Project.split的建筑等级分配。旧算法逐股份向下取整，使两笔1级股份的2级伐木场在50%拆分后成为旧2/新0；世界总量不变，旧守恒检查无法发现。修复仅修改model.py的import和分配调用，复用现有divide_building_ownership：先确定建筑迁出总等级，再按最大余数分配股份，50%明确得到旧1/新1。

现有主MOD无需重生成地图：独立核对12州148个国家/建筑组合，与原明确设计分配表完全一致（current-map-impact.json）。编辑器Python不被游戏加载，修复正式入口是WORK/editor，源码保存到Git main的development/workbench/editor；没有把工具、测试地图或数据夹具放进游戏目录。

验证：7项真实Project接口测试全部通过，0失败/0错误/0跳过。覆盖2→1/1、奇数和非50%比例、重复/外国/外州所有权、零级过滤、整个国别分州迁移、修正后的split保存/重开和不完整几何导出拒绝、当前主MOD无动作保存/重开/独立导出。测试源SHA保持不变；完整明细见D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/editor-rounding-20261101/current-main-regression-green.json。

已部署编辑器SHA：479f107cf7b5aa25bf25036d48b70db1db5ab959b46738b7add3561f645e1f11。
工具修改前完整备份：D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-editor-rounding-integration-20261101T095520Z/editor。
工具交付checkpoint：D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/checkpoint-editor-rounding-20261101T095520Z/editor。
主MOD修改前备份：WORK/backups/pre-change-editor-rounding-main-entry-20261101T094538Z/mod。

本次主MOD只更新任务记录；玩法文件与按钮修复版本629281f保持逐字节相同。沿用nesnd-20261101-button-guards.zip，游戏无需增加工具或QA加载项。游戏运行和编辑器UI验收没有在本轮执行；编辑器其它已列明的能力限制仍保留。

首次扩展回归的Dobruja/RUS夹具因原本没有建筑，在测试前置断言处失败；改用同州实际有4行/6级建筑的TUR分州后，完整7项重跑全绿。原失败日志保留，不把空夹具当生产缺陷或跳过测试。
