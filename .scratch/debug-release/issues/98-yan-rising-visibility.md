# 98 燕逆（复燕）起义的触发链与中华帝国一侧的进度显示

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（Victoria 3 1.15.1 / 26591675）  
Evidence: [第一轮调查报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-yan-uprising/round1.md>) · [内容树](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-yan-uprising/content-tree/report.md>) · [改动前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-yan-hints-20261114T122928Z>) · [Toolkit](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-yan-uprising/toolkit/>) · [日志副本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-yan-uprising/logs/>)

## 1. 现象与期望

玩家群反馈（现行版，用 CNE）：“中帝看不到燕逆进度”，不知道燕方起义离爆发还有多远、受什么影响。期望：起义按设计爆发，CNE 玩家在界面上能看到进度和影响因素并据此应对。

## 2. 原因

- 燕逆起义是登莱路线第 3 批「复燕之路」（[任务 07](../../denglai-route/issues/07-restore-eastern-yan.md)），不是政治运动。驱动量是登莱日志里的进度条「燕旗」（`common/scripted_progress_bars/nesnd_sha_restore_yan.txt:1`），满 100 且北朝陷入战争、革命或地权革命失败时，由登莱一侧的周脉冲弹事件、脚本建 YAN 并开战（`common/journal_entries/nesnd_sha_restore_yan.txt:37`、`common/scripted_effects/nesnd_sha_restore_yan.txt:2`）。
- 与设计记录一致：作者 2026-11-10 确认的 [spec-v3](../../denglai-route/spec-v3.md) J2 与 [numbers-v1](../../denglai-route/numbers-v1.md) §4 就是“进度条 + 乱局门槛 + 脚本起事”；用原版运动的是俄国一环。作者原作 tag 无此内容；Git `d8fabf8` 至今脚本未改。内容树未见断链。
- 看不到的原因：进度只存在于登莱的日志，CNE 没有任何日志、运动或事件显示它；起事时只有登莱收到事件，CNE 只看到新国家和一场战争。

## 3. 改了什么

作者 2026-11-14 定：不设日志，用通知事件。五件呈报，口吻官方、不点破，读者自己去琢磨。其余按默认：会党联络建立后才开始，触发链不改，北朝不加对策。

- `common/journal_entries/nesnd_sha_restore_yan.txt`：新增月脉冲。会党已联络且燕旗 ≥50 时，每月 10% 概率（燕旗满 100 时 20%）给北朝发一件呈报，上一件之后须隔满 6 个月。门槛直接读燕旗本身。
- `common/scripted_effects/nesnd_sha_restore_yan.txt`：新增 `nesnd_sha_yan_send_hint`，从北朝还没收到的呈报里随机挑一件。燕旗 ≥50 可出 1、2，≥75 加 3、4，≥100 加 5。
- `events/nesnd_cne_yan_hints.txt`（新）：五件北朝事件，每局各一次，只有一个表态选项，无数值效果。1 辽东勋贵寿宴（向北敬酒），2 松江账目（鼠耗、无存根放木票、外洋银元），3 黑龙江军械缺数（刮去编号的火枪，商人往海边去），4 松江巡防营一夜点卯缺半，5 林中操练空地与绣白字的蓝布（燕子早归）。须北朝仍持有五个必要州，事件 1 另需辽东。
- 中英本地化 `nesnd_cne_yan_hints_l_*.yml`（新），各 20 键。
- 同日按写作规范复核：事件 1 删去未有设定的“勋贵聚会须报备”规定，改为主人家主动送呈宾客名单。事件 2 不再用代理稿里的“木场监”。事件 2、3、5 的 flavor 改为只复述正文已有的事实，事件 5 的署名改为“勘界委员报告所附见闻”。事件 1–4 配图改用作者 CNE 事件所用的本 MOD 图 `event_ce_mordern_chinese_7/8/5/6`，分别配夜间屋宇、市集货栈、持枪兵丁、黎明街道。事件 5 本 MOD 没有林区图，保留原版 `europenorthamerica_gold_prospectors`（荒野营地）。flavor 套式检查 0 命中。
- 作者改写事件 1、2、5 的中文后，英文按新稿重译。事件 5 英文作 “the swallows, the yanzi bird”。
- 新增词条「张百里北征」（`common/glossary/nesnd_beiming_glossary.txt`，中英 `nesnd_beiming_glossary_l_*.yml`），事件 1 的“百里东征”链到此条。依据：作者 BM_flavor.372（徐鼎元病逝、八子争权、六个月、残部去向）、`北明ppet.pptx` 第 27 页（1823—1824、北征至黑龙江源、张百里封北国公），以及事件 1 作者稿（降顺燕军将门仍在任职）。作者 2026-11-14 澄清：攻入奉天府覆灭燕廷之后北上扫清东北直至黑龙江源，“亡于奉天府”是简写。徐鼎元病亡为准，ppet 的公审处斩是早期设定。写作技能 `no-invention.md` §2 同步改正。改动前备份 `nesnd-workbench/backups/pre-change-yan-glossary-20261114T132042Z`。

## 4. 怎么复测

可以读档：只改了日志脉冲与新增事件，无需新开局。

1. 读一个登莱「复燕之路」进行中的存档（或新开局玩到该阶段）。`tag SHA`，按一次「资助燕人会党」，悬停看燕旗当前值。
2. `tag CNE` 后继续运行。燕旗 <50 时不应出现呈报。≥50 后约每 6–16 个月一件，满 100 后更频繁。同一件不重复，五件出完即止。
3. 读文字：`tag CNE` 后 `event nesnd_cne_yan.1` 至 `.5`（事件条件要求登莱仍在筹备、北朝持有五州，不满足时可能不弹）。
4. 起事条件、起事时机与本次修改无关，仍按第 2 节的链条：燕旗满 100 且北朝陷入战争、革命或地权革命失败。

## 5. 遗留问题

- 未启动游戏。`random_list` 的 `trigger` 由 script_xcheck 报为未知键，是工具误报：`docs/effects.log` 记载此写法，原版 `00_west_america.txt:105` 同样使用。
- 呈报不显示数值，北朝仍不能直接读到燕旗读数，这是作者选择的效果。
- 第一轮报告第 6 节列出的五项未改：察觉无提示、未资助时燕旗也会因北朝乱局上涨、`nesnd_land_failed` 不清除、起事时北朝无说明事件、燕旗只增不减。
