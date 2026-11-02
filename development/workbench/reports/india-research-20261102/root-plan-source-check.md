# 印度实施方案：当前 MOD 来源复核

2026-11-02；只读复核，未改 MOD 或方案、未启动游戏。对象：`WORK/plans/two-empires/20261102-india-development-design.md`，读取时 SHA-256 `686f368f2a56c0b76a14277f2e8d77fb0df2036f044cec62516833f275047aab`。仅核当前 MOD 事实；新指标、路线、奖励和未来文件安排均视为提案。

## 发现 1 处需要改准的表述

方案第74行把现有法援条约列为可复用的“实际扣款、答复、拒绝、**到期**和权限”。当前源码只有一年 `binding_period`，不是一年后自动终止；应改为“实际扣款、答复、拒绝、约束期、撤回/重谈和权限”，避免后续实现错误地删掉持续条约。证据：[当前文案第44行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/nesnd_external_l_simp_chinese.yml:44>)明确约束期不是自动到期日；[事件创建条约第139行](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:139>)使用 `binding_period = { years = 1 }`。

## 两项特别复核

- **军营别名没有漏算。** 当前原版定义是 `building_barrack`，并有 `aliases = { building_barracks }`，见[05_military.txt:3](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/buildings/05_military.txt:3>)。本次重新遍历全部有效 GAME+MOD `common/history/buildings`，MUG 的单数、复数键均无 `create_building`（显式等级各为0）。这只证明无显式历史建筑声明，不证明 setup 后军营数量为零。原版 MUG 唯一编制声明仍为2不正规步兵+1骠骑兵，见[05_military_formations_india.txt:1448](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/military_formations/05_military_formations_india.txt:1448>)。方案已保留此界限。
- **MUG 93,471,151 是全国全部静态人口，不只预选地区。** 本次重新遍历全部有效 GAME+MOD `common/history/pops`；所有 MUG 人口都来自 MOD `10_india.txt` 的12地区，合计仍为93,471,151，无其他文件/海外人口遗漏。范围为比哈尔、西孟加拉、东孟加拉、阿萨姆、德里、阿瓦德、中央邦、拉杰普塔纳、奥里萨、孟买、阿格拉、山地旁遮普。USM的22,740,898则有明确印度研究范围，方案没有误写成USM全国人口。

其余已列当前 MOD 数字、主文化/宗教、人口占比、USM大陆/含岛屿总量、主要地方国家人口、建筑等级、锡兰舰船声明、法国朝贡、两组MUG历史文件共存、`.bak`非活动、德里/阿格拉未整合、BIC依赖和既有形成条目，未发现与本轮原始数据不一致之处。

机器记录：[root-plan-source-check-data.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-research-20261102/root-plan-source-check-data.json>)；重跑脚本：[check_root_plan_sources.py](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-research-20261102/check_root_plan_sources.py>)。人口源 SHA `2d4674d742540bc1168daf3fe2397185a670dd7bae50e2dcf013605f6a3ad1d3`；建筑源 SHA `9d98062c3bf4df26efff13b0518df092c8f9b3d30b62cd264d5d35695ed2dfbd`。
