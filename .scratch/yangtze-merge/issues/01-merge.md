# 01 长江十州合入源目录

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS
Evidence: [交付说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-15-yangtze-merge/交付.md>) · [定案表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/yangtze-sea-2026-11-13/decisions.md>)

## 1. 现象与期望

作者批准把长江十州外审版（工作台 `exports/yangtze-ten-nanjing`）中已定案的地图改动合入源目录，静态核对后部署，作者开新局复测。46 个矿区／农区／林区替换名仍是待批提案，本次不合入。

## 2. 原因

外审副本的底本是 2026-11-13 的主 MOD（`exports/yangtze-full-repack` 及 Git `d8fabf8`）。此后主线另改了 144 个文件，其中 4 个与长江改动重叠，所以按文件做三方合并，没有整包覆盖。

## 3. 改了什么

- 29 个文件主线未动，取外审版：东亚人口、建筑、州历史，五类定位点，splnet，战略区，统一计分，福海船厂，QE1，首都，可释放国，地理区，`flavorUSM_ce`，中英城镇名与地理名。
- 4 个文件三方合并：`11_east_asia.txt`（州定义 + 主线东北垦荒特性），`nesnd_cne_republic.txt`（共和军南方宣称 + 主线起事预警），中英 `ce_states`（新州名 + 主线五国）。
- 15 个新文件：省图、河图、原生 Repack 高度文件四份、`default.map`、`adjacencies.csv`、`province_terrains.txt`、三段江面州与战略区、两关海峡、海路网、江面与关口名称（外审版 `nesnd_yangtze_test_l_*` 改名为 `nesnd_yangtze_seas_l_*`，内容不变）。
- 没有带回 `00_ai_triggers.txt`：主线已在 2026-11-14 改为 `ce_ai_triggers.txt`。
- `deploy/deploy-whitelist.txt` 加四行，部署 `map_data` 下的 png、`default.map`、`adjacencies.csv`、`heightmap.heightmap`。

## 4. 怎么复测

已部署 `6e1eafbd`。用隔离存档目录 `nesnd-workbench/runtime/profiles/yangtze-ten-formal-play` 启动（只加载 EACR 和正式 MOD 文件夹），命令和新局检查清单见交付说明。

2026-11-16 观察者局（1836.3.9 存档）的 error.log 有两条长江相关报错，已修并部署 `c84bc423`：

- `fortification_locators.txt` 新增为原版覆盖文件，只把要塞图形定位点 285 从下段江面 (6860,1358) 移到同省 x301000 的陆地 (6864,1354)，离水 2.2 px。原版其余 585 个要塞点不变，现在没有一个落水。
- `adjacencies.csv` 去掉文件末尾换行，与原版一致。引擎原先把第 248 行空行当成一条记录读，报 `Failed to read province string`；五条长江记录不变。

## 5. 遗留问题

- 十州正式部署版尚未实机验证。舰队过两关、陆军过三渡此前只在外审副本测过。
- `heightmap.png` 52.5 MB，超过 GitHub 的 50 MB 警告线（硬上限 100 MB），提交推送时会有提示。
- 46 个占位名提案未处理。
