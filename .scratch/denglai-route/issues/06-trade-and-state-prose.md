# 06 登莱的远北贸易、领土与人物口吻

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（游戏外文本检查）  
Evidence: [逐键改动与文件指纹](<../../../../../nesnd-workbench/reports/denglai-route/trade-and-state/verification.json>)

## 1. 现象与期望

「登莱与华夏」共和结局的语序错接。两批文字还把政府经营山东写成居民一概还乡，把长期贸易写成无偿接济。作者要求校正远北社会的种族等级、革命与反革命的经验，以及外交代表和驻军的口吻。

## 2. 原因

共和结局中的“山东的土”被后文隔断，动态国名落在了句末。贸易叙事混淆了奴隶买主、收款的船商和出资的投资人。旧引语也把领土谈判、中央官署迁移写成了逐户解释与催发军饷。

## 3. 改了什么

- 两种语言的 nesnd_sha_republic 和 nesnd_sha_far_north 本地化文件以作者现稿为底本。修订统一结局、国家路线和贸易背景，以及涉及谈判、驻防、请愿、报禁和俄属远北的文字。英文对应作者的鲸脂、苦兀交涉、流放等改笔。
- map.md 的 C1 改为作者本次确认的贸易关系，并区分国家目标与个人故乡。实际安装的写作技能和 development/nesnd-player-writing/SKILL.md 同步增订禁止为仿古漏字截词、核对交易流向和说话人权限的规则。技能保存在本地分支 codex/denglai-player-writing-20261110，提交 cc53e12ddefb。

## 4. 怎么复测

查看开局两线、女真和雅库特请愿、苦兀来使、迁都海参崴及共和统一结局。动态国名应落在完整句子里。青岛作为政府首都的决议与山东籍人物自己的还乡愿望各有相应语境。

## 5. 遗留问题

两批各语言共 237 个键及其动态引用已核对，技能两份入口均通过 quick_validate.py。新文案未进游戏查看排版。
