# F2 初次原生可行性运行：20261101T003815Z

本轮是玩家续玩修复前的真实接口/回归样本，不是最终验收版本。

- 源候选：`WORK/exports/batch-debug-20261101-f2`，526文件，指纹 `416ac54f8fb9f4c4ab1c86266519b517724f9f78a9a396e4579342774fb9353f`。
- 冻结副本：`WORK/exports/runtime-20261101T003815Z/mod`；运行记录 `WORK/reports/runtime/20261101T003815Z/run.json`。
- 游戏1.13.11/build24799966；加载只读EAC、本轮冻结MOD和冻结QA。沿用前一隔离profile的shadercache；新局，不用旧地图存档代验。
- QA源：`WORK/qa-fixtures/f2-concentrated-20261101-a/manifest.json`；安装前整QA备份 `WORK/backups/pre-change-f2-qa-20261101T003717Z`，仅3文件差异。
- 独立profile：`WORK/runtime/profiles/20261101T003815Z`，monthly autosave请求待本局真实确认。
- 启动前进程枚举未发现victoria3.exe；runtime会话47407。窗口从本次枚举获得2691262，后续须实时重新观察，不能恢复后直接复用。

## 已观察的步骤

1. assistant启动运行器；看到真实游戏加载画面。
2. 真实主菜单出现，显示版本1.13.11、checksum7443（有修改）。立即归档22份冷启动日志到 `run/stages/cold-main-menu`，未清空日志。
3. assistant点击新游戏，再选无目标沙盒，进入地图新局初始化；此时尚未选国，也未证明任何游戏分支正确。

4. 实际选择USM并开始，Jan1暂停，UI为PLAYER YES/AI NO；checksum7443、seed35709482。用原生暂停菜单保存 `大明联邦_1836_01_01.v3`，SHA见run/evidence/Jan1-native-baseline；未动政策、产业或人口。
5. 从该局点击明确标记的JAP DP夹具；真实生产on_action登记。Jan2自然延迟probe输出REGISTRATION YES、JAP_NATIVE_DP YES；非直接调用恢复函数。首次控制台readonly日志日期getter伴随1条GameStateAccess断言，已单独归档；不归因生产恢复。B版无getter QA已独立准备，未改本运行。
6. 下方播放三角不等于上方暂停按钮。首段实际推进至Jan24，另存 `大吴_1836_01_24.v3`；正确上方暂停后Jan27再手动切JAP，保存 `丰臣幕府_1836_01_27.v3`。不把此段说成只推进一天。Jan27原档确认player country17、DP5和主/镜像wg_nesnd_usm_annex，USM预登记ctry17正确。
7. 在日本玩家的原生外交博弈页面点击“让步”，再点击原生确认“是”。立即出现“游戏结束／你已被吞并”，显示丰臣幕府于1836-01-27终结。没有手工执行annex或恢复helper。随后root明确点击内置“作为观察者继续”；这不是玩家自动续玩。
8. 观察者自然推进；Jan29的自然回调观测已有JAP/JTK/JIM存活、登记/排队/pending/blocked清除。实际暂停在Feb9，另存 `观察者_1836_02_09.v3`。原生Feb1 autosave也已出现。三国具体关系、地区与人物由独立存档审计核对；单靠地图旗帜不能认证全部分配。

## 后续覆盖

先建立USM Jan1自然基线和单独日本DP夹具分支，再验证生产on_action登记、原生退让/战目标执行、延迟恢复与玩家失国。Lin、海运、PHI分别从独立存档分支。夹具会明确标记，手动tag或直接helper不能充当自然回调/玩家自动续玩证据。
