# 02 · 季度事权、两省拨款与西部置省

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [本次实施与核验](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-wu-mandate-revision/report.md>)

## 现象与期望

初版可以停在端点长期领取修正，工程开工时已经移交事权。作者要求加入制度本身的影响，并使拨款、任免和置省产生相应后果。

## 原因

原有两项立场只控制月增减，跨省公共投入只指定一个州。

## 改了什么

按科举投票制、任命官僚制、乡村民众是否强势入阁以及玩家立场计算目标。自然季初最多靠近 5 点。验收后才按考试、任免与拨款权移动事权。两省拨款各给一个州同一地方修正，西部三地置省成功只给一次 +10。四项施政完成后，总页列出所选方案。

## 怎么复测

启用立场，跨过季初后撤回，再观察下一季度。选择跨省公共投入，核对两个州的税收能力和国家预算；让一地的政府行政机构用工不足，核对连续月份归零。成功置省后跨月读档，核对事权未再增加 10 点。

## 遗留问题

新局与旧档的画面、实际月度时序及修正仍待实机确认。旧档已经开工的单州拨款可按原范围完成，再次立项适用双州规则。
