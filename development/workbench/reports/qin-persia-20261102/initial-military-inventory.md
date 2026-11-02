# 秦国开局军事源码库存

2026-11-02；候选 `WORK/exports/qin-persia-campaign-20261102-a`，基线 `WORK/backups/pre-change-qin-persia-campaign-20261102T022528Z/mod`；本机1.13.11/build24799966。只读源码研究，未开游戏。逐项记录与SHA见同目录 `initial-military-inventory.json`。

**可核实的历史脚本是：QE1所在州显式兵营82级；两支陆军合计36个常备单位。两者不是同一个数字。实际完整开局的兵营总级数尚未读取。**

## 兵营等级

原生规范名为 `building_barrack`，`building_barracks`只是兼容别名（GAME `common/buildings/05_military.txt:3–7`；`common/defines/00_defines.txt:34`也指定单数名）。本次首次仅搜复数的临时“零声明”结论已撤回；以下同时覆盖单数和别名。

在候选全部13个建筑历史文件中，按 `s:STATE_* → region_state:QE1 → create_building` 保序提取，得到：

| 所在地区 | 显式级数 | 资产所有者字段 | `common/history/buildings/`来源 |
|---|---:|---|---|
| STATE_UZBEKIA | 20 | QE1 | `09_central_asia.txt:362–371` |
| STATE_TAJIKISTAN | 10 | QE1 | `09_central_asia.txt:552–561` |
| STATE_KIRGHIZIA | 10 | QE1 | `09_central_asia.txt:627–636` |
| STATE_TURKMENIA | 6 | QE1 | `09_central_asia.txt:801–810` |
| STATE_LHASA | 12 | QE1 | `09_central_asia.txt:1335–1344` |
| STATE_NGARI | 6 | QE1 | `09_central_asia.txt:1363–1372` |
| STATE_URALSK | 3 | **KZH** | `15_russia.txt:1803–1812` |
| STATE_KHIVA | 14 | QE1 | `15_russia.txt:1864–1873` |
| STATE_SEMIRECHE | 1 | **OZH** | `15_russia.txt:1886–1895` |
| 合计 | **82** | QE1字段78；其他4 | |

本统计按建筑所在的QE1州计数，符合当前 `every_scope_state → every_scope_building → add=level` 指标。Uralsk/Semireche的外国所有者字段是原有脚本，不能为完成本次目标而擅自国有化或清理。实际引擎对这两项的有效资产与兵营初始化仍待读取。

DOC `effects.log:817–843`说明create_building支持add_ownership.levels；它与直接level互斥。已存在同类型建筑时，使用已有等级与脚本等级的最大值，并非将重复create_building等级无条件相加。这里九项均为不同州，无重复州兵营声明。

## 编制数量

`common/history/military_formations/CE_military_formations_asia.txt:609–683`：

| 编制 | 单位数 | 招募地区 |
|---|---:|---|
| QE1_dongzheng_expedition (`:610`) | 18 | TIANSHAN：线列步兵12、龙骑兵2、枪骑兵2、骠骑兵1、机动炮兵1 |
| QE1_anxi_zhihuishisi_army (`:647`) | 18 | KHIVA：线列步兵12；UZBEKIA：龙骑兵2、枪骑兵2、骠骑兵1、机动炮兵1 |
| 合计 | **36** | 线列24、龙骑4、枪骑4、骠骑2、机动炮2；无QE1舰队定义 |

两编制都没有service_type字段；DOC `effects.log:970–975`定义默认regular。DOC `event_targets.log:888–893`的army_size为不计已征召兵的营数，并非兵营建筑级数，也不保证兵员招满、补给充足。

Tianshan在建筑历史没有独立兵营声明，却有18个编制单位；Khiva的14级兵营对应12个编制单位、Uzbekia的20级对应6个。因而不能直接将36或82声称为游戏实际兵营总数。若编制初始化对Tianshan补18级，则可能出现100级，但这是**需要引擎证据的推断**，不作为确定基线。

## 初始化顺序与建议

当前候选 `common/history/countries/QE1 - Western Qin.txt:93`调用bootstrap；`common/scripted_effects/nesnd_qe1_agendas.txt:3–6`用一次schema标记同时保存 `barracks_total + 25`。现有GAME历史readme和导出API未给出country-history、building-history、military-formations三者完整执行顺序。因此不能保证这一时刻已经看见全部兵营；一旦早采样为0或部分等级，schema会使错误目标永久保留。此风险不等于已经复现顺序错误。

优先方案：把**军事基线的一次初始化与通用campaign_v1分开**。新局用原生 `on_game_started_after_lobby` 进入QE1采集实际兵营等级并存目标+25；GAME `common/on_actions/00_code_on_actions.txt:10–13`明确它在本campaign第一次从大厅进入游戏后触发。也可在此安排次日country event，再以单独标记保证仅捕获一次。新基线未建立时army_ready明确返回false；不要在country-history提前设置这个专用标记。旧档首次启用可在现有monthly维护补采样，但应称“首次启用时基线”，不能伪称1836历史数。

若必须完全依源码固定目标，**82＋25＝107**是可复核的“显式历史建筑等级＋25”设计值，可直接登记为固定目标；但它不等同于“完整开局实际兵营＋25”。**36＋25＝61只能作为编制营数目标，不能拿来替兵营等级目标。**

## 俄国边境目标

候选 `common/history/states/00_states.txt`中三者均只有RUS的create_state，没有QE1州块：

| 地区 | 定义/归属来源 | 开局源码归属 |
|---|---|---|
| STATE_ASTRAKHAN | `map_data/state_regions/09_central_asia.txt:155`；states`:8261–8265` | RUS；另有QE1 claim不改变所有权 |
| STATE_UFA | `map_data/state_regions/15_russia.txt:1004`；states`:9246–9250` | RUS |
| STATE_TOBOLSK | `map_data/state_regions/14_siberia.txt:67`；states`:8120–8125` | RUS |

因此它们都是有效的外国俄国开局目标，较无数据库定义的旧ORENBURG引用正确。目标trigger使用“秦或其附属国拥有整个地区”是在之后检查征服/附属成果；不能把开局claim或历史上原属秦当作开局已满足。
