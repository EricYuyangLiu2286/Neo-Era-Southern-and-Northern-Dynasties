# HUS 玩家流程方案与编辑记录

配置：gpt-6-astra / high；由主代理 /root 显式委派，先方案后编辑。任务范围为 HUS 日志入口与中英文状态；不改建设条件、费用、奖励或 AI，不启动游戏。

## 主审裁定的实施方案

1. `nesnd_c2_hus_agenda` 保留“共和国的土地与人”名称，承接原 `nesnd_hus_registration` 的初始化、两项互斥选择、一年登记、月度结算、分支状态与真实施法成功出口。新日志不承载建设按钮。不新增计时变量；现有全局与国家登记时钟保持唯一来源。
2. 原登记日志停止新激活，已存在的条目隐藏失效；不清理国家登记时钟。保留同文件的原版 `je_indian_removal` 定点停用。
3. `nesnd_c2_hus_frontier`、`nesnd_c2_hus_citizenship`、`nesnd_c2_hus_oil` 直接以各自 `_open` 开启，移除“先选方案才可打开日志”的循环依赖。保留原按钮、条、完成条件与后台结算。新增简短状态：尚待选择、已选但未满足运营条件、连续运营中、目标失效等待重新选择。建筑/资金/政府勾叉仍留给原生条件。
4. 不把三项建设并入登记完成条件。族籍完成仍只是实际施行所选法律；建设各自达标、各自结束，油业仍按原科技和建筑门槛后置。
5. 编户按钮已有稳定效果提示和不可改选说明；点击后新日志立即改为具名进行状态。暂不新增弹窗，避免为同一选择重复确认。

## 已核源码事实

- `common/journal_entries/nesnd_civic_routes.txt:231`：原议程含8个建设按钮，无 `status_desc`，只有原政权不再适用时的出口。原登记独立存在。
- `common/scripted_triggers/nesnd_civic_routes.txt:110–147`：牧地/学校须先完成筑路，油业须抽油机科技及至少一座50%就业油井。启动方案另需预算、政治支持与目标州。运营累计连续3个月，中断清零；不能文案承诺暂停保留。
- `common/scripted_effects/nesnd_civic_routes.txt:215–330`：三项月度运营与一次结算分别独立，不依赖主议程存在。
- `common/scripted_effects/nesnd_hus_registration.txt:200–249`：选择后建立12个月既有时钟，期满实际激活法律成功后才记 done；原住民路线另安排满蒙迁出。
- `common/journal_entries/nesnd_hus_registration.txt:1–30`：原状态包含选择、满蒙/原住民进行、完成、冲突。关闭日志本身不得取消时钟。
- `common/scripted_buttons/nesnd_supply_buttons.txt`：HUS 两个收束按钮按 `market.owner = root` 互斥显示，不是点击后加入或退出共同市场的外交选择。4/4与12/12之后仍需点击，实际奖励经 `events/nesnd_supply_events.txt` 的 `.3` 事件唯一领取。

## 当前原版来源

catalog.py status：1.15.0 / Steam build 26453692，CURRENT，changed_count=0。

GAME `common/journal_entries/00_land_reclamation.txt:24–42,74–89` 使用具名 outcome 与 first_valid 条件状态；成功操作及预览分别展示。调用 `events/land_reclamation.txt:64–82` 更新同一进度变量并处理成果；修正定义 `common/static_modifiers/content_1_modifiers.txt:1108`，清理入口 `common/scripted_effects/00_victoria_cleanup_scripted_effects.txt:1465`。界面 `gui/journal_entry.gui:122,351–352` 原生展示结局/非空状态。这里只复用已有的日志字段，不照搬荷兰奖励或事件流程。

## 作者原文与本轮取舍

原稿均取只读源码仓库 f18b6c4，非当前 AI 修改后文本。

| 原稿 | 原文与本轮判断 |
|---|---|
| `ce_cne_events_l_simp_chinese.yml:15` / `ce_cne_land_reform_reason` | 用土地所有者、农民、生产与制度的因果解释改革。HUS 正文保留既有族籍身份冲突，不缩成“办理登记”的事务说明。 |
| 同文件:69 / `flavorCNE.3.d` | 改革结果写谁取得何种生活条件。本轮成功结局明确哪一族获得一等户籍及哪些等级仍保留，不泛称所有人获得平等。 |
| `ce_poland_l_simp_chinese.yml:27` / `ce_support_polish_problem_btn_desc` | “承诺支持波兰的复国运动。”短字段只讲当前行动。HUS 状态直接说明选择、等待或缺失条件。 |
| 同文件:12 / `ce_je_poland_1_invalid_tt_2` | “没有符合条件的参与国”。无可用对象应给具体原因，不写“暂时无任务”。 |

原稿 SHA256：CNE `3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a`；Poland `20731ac53ebbe66c85d65ac5a9eb1e52a00f69feb6bcf13b490f13f5bcc17f6d`。

## 编辑和验收边界

先编辑，后冻结；冻结前不运行测试。主审须亲读差异及原始脚本。此报告和编辑不构成引擎验证。仅修改主审分配的2个 JE 文件与4个中英文文本文件；供应/小国民生只另交文案建议。
