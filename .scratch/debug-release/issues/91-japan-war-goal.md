# 91 重组日本诸藩的战争结算

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS（Victoria 3 1.15.1，待作者复测）
Evidence: [完整脚本链、原版依据、版本与复测步骤](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-japan-war-goal/report.md>) · [六份存档](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-japan-war-goal/save-evidence.json>)

## 现象与期望

工坊玩家报告吴打赢日本后白和。吴方兑现「重组日本诸藩」时应执行既定分封。另查本机最新观察者档，实际由东洋之议在 1852.11.15 十年超时结案，六档均未发国书。

## 原因

工坊和改前开发版的目标只声明争夺首都，没有启用 1.15 的占领计时执行。分封资格只认可本土日领由日本或吴直接控制，本场吴方盟军占领也会使目标无效。群友的实际和约条款未留存。

## 改了什么

- `common/war_goal_types/nesnd_japan.txt` 加占领计时配置，满条兑现重组。
- `common/scripted_triggers/nesnd_japan.txt` 按本场战争的参战国和吴方阵营判断盟军占领。领土与宗属沿用原效果。

## 怎么复测

以修正后新局验收，或重启读合资格的东征前旧档。吴发国书，日本拒议，检查两项主要要求，开战时分存。一路用 OccupationTool 占日本当前首都并守吴都，最好让同方属国占日本一州；另一路 tag JAP 直接投降。核领土、宗属和双方目标执行明细。

## 遗留问题

修正版尚待两路实机验收，再以两份玩法脚本热修工坊。旧任务 79 的文案断言发现失败提示中文比英文多一个州概念链接，保留作者现有文字。
