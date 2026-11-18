# 01 「礼法之下的生活」按收场分版，大吴与大明的等级制度

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-17）
Blocked by: none
Validation: STATIC_PASS（Victoria 3 1.15.1，待作者复测）
Evidence: 改前备份 nesnd-workbench/backups/pre-change-south-order-20261117

## 改了什么

- 日志分三个版本，名称与说明相同：`nesnd_c2_usm_agenda`（内战收场，两个结局不变）、`nesnd_c2_usm_agenda_zheng`（郑氏和平，只有“郑家的要求”）、`nesnd_c2_usm_agenda_ming`（明室和平，只有“大明的要求”）。引用日志的六个文件改为认三个版本（`nesnd_usm_agenda_any`）。
- 出现条件：`nesnd_south_settled` 且不在 `usm_civilwar_status_quo`（僵持时不出现）。
- 和平奖励：`nesnd_south_zheng_settlement`、`nesnd_south_ming_settlement`（各 20 年）；明室另得华北十二个地区的宣称；通牒事件 `nesnd_south_order.1`、`.2`，拒绝者挂 `nesnd_south_defied_ultimatum` 十年并进入博弈 `dp_nesnd_order_unification`（不能议和）。
- 等级制度（`common/*/nesnd_south_order.txt`）：社会等级 `nesnd_wu_fence_hierarchy`（六个按文化的阶层）、`nesnd_ming_gate_hierarchy`（七个按职业的阶层）；法律组 `lawgroup_nesnd_wu_fence`、`lawgroup_nesnd_ming_gate` 各四部法律；26 个接纳度修正类型；利益集团立场 79 处照唐律分等对应复制。内战胜利后由日志的开局与月度脉冲调用 `nesnd_south_order_grant` 生效。
- 让权换取效忠改为每月 −1.5。

## 写法要点（东洲、波斯留下的教训）

- `pop_criteria` 里不能用 `cu:`，用 `has_pop_culture`。
- 每个文化条件包在 `custom_tooltip` 里，否则阶级面板没有人群作用域，说明文字残缺并刷错误日志。
- 同一等级的阶层互斥且覆盖全部人群，兜底阶层排最后；上中下三层各至少一个阶层。
- 法律组启用时引擎取文件里第一部法律，基础法排第一。
- 新法律组必须在利益集团意识形态里有立场，否则无人支持、立法成功率为 0。

## 怎么复测

1. 观察者局打完内战：胜方法律页多出一个法律组，社会页的阶级面板显示新阶层，条件文字是具名的六类或七类。
2. 控制台 `tag USM`，和平收场后看日志是否只有一个结局。
3. 完成和平版本后，蜀、楚、淮里仍是属国的收到通牒。

## 遗留问题

- 全部没有实机验证。重点：阶级面板显示；`set_social_hierarchy` 后人群是否都落进阶层；利益集团对新法律的态度；同名日志三个版本的切换；通牒拒绝后的开战。
- 引擎没有“禁止投降”的开关，只做到不能议和。
- 新文字（法律说明四条、阶层名十三个、事件两个）是代理草稿，待作者确认。

## Comments

- 2026-11-18 作者要求：内战版 `nesnd_c2_usm_agenda` 的集权、地方两个结局完成时也向仍是属国的蜀、楚、淮发合并通牒（`nesnd_south_order_ultimatums`），提示行 `nesnd_usm_agenda_ultimatum_tt`。通牒事件 `nesnd_south_order.1` 按发出方是否和平收场分两段正文（`.d`、`.d_war`）。STATIC_PASS，未部署时 MOD 文件夹版本号缺失，见交付说明。
