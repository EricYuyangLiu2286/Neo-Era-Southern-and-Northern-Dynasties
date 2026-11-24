Record: implementation
Category: cleanup
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-24）
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-concise-effects-scan-20261124T140242Z/`；交付记录与核对脚本 `nesnd-workbench/reports/2026-11-24-concise-effects-scan/`（交付记录.md、verify.py、checks/）

# 118 全源目录简洁写法整理

## 1. 要求

作者要求扫描四类「绕远路」写法并改成原版写法：进度条另存国家变量再盖回、提示＋隐藏效果、效果 if 的 limit 里套具名提示、重复守卫；日志结局按条件给出不同结果的 if 补 else。玩法、数值、句子不改。

## 2. 改了什么

- limit 里的具名提示：拆 759 处（630 处直接在 limit 下，129 处在嵌套 if 里），依据原版 `common/scripted_buttons/00_scripted_buttons.txt:55–57`（trigger_if 的 limit 写裸 has_variable，不显示）。作者原作 ce_french 的 5 处不动。
- 提示＋隐藏效果：505 处里展开 1 处（迈索尔宣称按钮），其余保留，理由见交付记录 Q3。
- 进度条：A 类改为条自己累加 7 条（西秦朝争、议程平衡、边疆两条，日本国民团结、新政推行，埃及独立）；B 类改为直接写条 8 条（西秦三方份额 3 条，菲律宾 2 条、丹那沙林 2 条、补给连续周数）；另去掉 2 处变量副本（吴国军心、南方改制承诺）。共删变量 20 个。其余按 C 保留，理由见交付记录。
- 重复守卫：拆 13 处（日本产业日志 8、印度统一、西秦恢复、普鲁士联盟、埃及能力、迈索尔按钮）。
- 日志结局补 else 3 处（明末日本干预、俄国平定草原超时、沙燕进入山东）。
- 删本地化键 233 个，中英同删。

## 3. 怎么复测

读档或新开局即可。重点看：西秦朝议三方份额条与朝争、议程平衡条、边疆两条的数值与明细；日本国民团结与新政推行条；埃及独立条；菲律宾、丹那沙林、补给的连续计数条。
