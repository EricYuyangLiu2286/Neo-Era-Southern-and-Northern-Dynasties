# 01 原创中期人物审核：段敬川与牧沐子

Record: implementation  
Category: bug  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付、人物清单、人物树与丰富建议](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-14-midgame-characters/交付.md>)

## 现象与期望

“不确定这些人物的事件链能否在新开局里走完，以及人物不在场时文字是否仍点名。”期望：出场、选择、退场按设计发生；本人不在场时由机构或地点出面。

## 原因

段敬川按第 14 组方案实施，人物不在场时也不会点名。但弹窗有效期是 3 个月，月检每月都会再发 .14／.200，玩家放着不答就会连弹，答过一张后，剩下的 .14 还能再答，再扣一次钱（`common/scripted_effects/nesnd_civic_characters.txt`）。待答保护写成了 3 天。
牧沐子是开局人物，她的剧情链从中期开始。`flavorCNE.14` 的 trigger 为空：她不在 CNE 时照样弹窗点名，没有加州持有国时移交也会失败。东渡保护和待答保护都在答复期结束前过期（`events/flavorCNE_ce.txt`）。

## 改了什么

- `common/scripted_effects/nesnd_civic_characters.txt`：段敬川带着待答标记时，不再发 .14／.200；标记改为 3 个月。
- `events/nesnd_civic_characters.txt`：已经介绍过他以后，取消剩下的 .14。
- `events/flavorCNE_ce.txt`：.14 要求她仍在本国且有别国持有加州，她离开就取消窗口，目的地排除本国。东渡保护延长到弹窗关闭。6 处待答保护由 3 天改为 3 个月。

第二轮按作者决定：
- 选项 2 留下她、目的地按加州持有国：都保持原样。
- 出书两边都有：新事件 `flavorCNE.16` 沿用 .15 的文字，只给 `bm_the_book`。她不在 CNE 时发给 CNE，在 CNE 时发给持有加州的别国（`events/flavorCNE_ce.txt`）。
- 1872 年前不死：年检设置、到期取消（`common/scripted_effects/nesnd_mu_muzi_book.txt`，挂在 `common/on_actions/ce_code_on_actions.txt`）。
- 1871.5.15 起任何国家都没有她时，月检从流放池把她移回应在的国家，找不到就新建替身（同上文件；判定在 `common/scripted_triggers/nesnd_mu_muzi_book.txt`）。

## 怎么复测

新开局，或读 1840 年前的存档。段敬川的 .14／.200 放置两个月，应当只有一张。CNE 的 .12 选 2，4 个月后看「沐子东渡」，再到加州持有国的面板里找她和费西翼。步骤见交付第 6 节。

第二轮须先关游戏、在源目录运行 `deploy.bat deploy`；步骤见交付第 6 节末的第二轮复测表。

## 遗留问题

未实机验证；第二轮尚未部署。第 3 节的 4 项作者问题已按作者决定处理。第 4 节列了 10 处同类的 3 天保护，本次未改。丰富建议见第 7 节。
