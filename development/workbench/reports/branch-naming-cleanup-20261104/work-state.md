# 当前任务35：清理、命名、条件文案与真实刷错修复

父main `0bd4bdbd43adf0076165a8e338a92e70daefeb40`。唯一主MOD=M，repo=W/projects/nesnd-repository；本轮临时编辑候选C=W/exports/maintenance-current。用户最新授权清旧候选/失败现场/snapshots/runtime，只留少数关键版；不改普通USERDATA存档。最后要合入M/main并重新上传。不开游戏；用户已自行运行测试并报告错误暴增。

## 已实施/尚待

- 已研究Git19分支/目录；已执行cleanup_obsolete_workspace.ps1，删除791项、562547文件、122909477122逻辑字节。结果cleanup-result.json。保留backups/pre-update-20261030T233944Z原版、pre-change-maintenance-pre-cleanup-20261104T213001Z本轮前、当前C；最终完成再补第三备份。保留evidence/key-engine-terminal/观察者_1866_01_15.v3一份。旧exports/backups/runtime/snapshots/runs/临时editor工程和旧v3已清，普通游戏存档未动。PS5因GetRelativePath不支持先失败，PS7.6.5最终成功。Git18旧本地branch尚待删除（须核实时远端SHA），main保留、original标签保留；远端不删。
- 121个z文件（94loc+27script）均非凭名称可删的临时内容。用户明确不用优先级补丁：全部改informative主题名，重复key合并成唯一所有者，直接编辑原有条目。Luna全152replace文件审计：239 key×language重复、80多值冲突；完整来源在localization-duplicate-consolidation-plan.json。root尚须逐项选值并执行；不能无脑按文件名后者胜。27script计划含三组本MOD定义/REPLACE链：HNA/SIH、印度JE、7regionalJE，合并/直接改定义需保持数据库语义。
- Sol已完成C中9脚本的实施，已冻结未测试，见implementation-script-owned-sha.json/.patch。八个small计数在每次change前增加缺值set0（不是一次init）；QE1七JE/十四button条件单项TT与hidden内部守卫；EGY隐藏六tag枚举/finished。数值、29天、+25基准、持久opened等不改。32required-loc keys只列契约，文案由Astra提供proposed-condition-text.json，root待逐条亲审与应用。
- 真实刷错：捕获USERDATA/logs/error.log及error.1–5.log于runtime-error-capture，18655保留记录23签名（日志轮换不能恢复全部394329计数）。17524上下文错误来自埃及status_desc误用JournalEntry；9状态key×中英需只在状态中替成ROOT.GetCountry。八个small缺值change错误225+166条，已在C按最小方案修复。root已亲读当前原版journal_entries.md177–179及实际写入链。runtime-root-cause-plan.md/json。268空纹理无具体widget/path，UNRESOLVED，不猜修。其他旧DLC/mod gamerules无归属本MOD证据。
- Astra/high审读2618条非中国scope，提交124keys/246语言修改proposed-loc-edits.json，root尚待逐条审；明确去埃及朝廷/印度实现解释、PRU重复转折、其他非中国机械语句。不能把子代理通过当验收。
- 两SKILL已增加玩家文本最低GPT6 Astra/Medium（本轮Astra/high）与root逐条重写复审、主审High+要求和不得直接采信subagent claims；未知root运行时meta不能伪报，需显式Astra/high独立补核+root实证。backup-release更新只保留少量关键版。尚待语法skill补status ROOT及missing var严守、本地化单owner规则。

## 实际代理

- luna_file_order_inventory：显式gpt-6-luna/high，只读文件/重复key/源码定位。
- astra_cleanup_structure：显式gpt-6-astra/high，先清理结构方案，后非中国及条件文本候选；不改源码。
- sol_qin_condition_audit：显式gpt-6.1-sol/medium，先只读QE1/真实错误诊断，再按rootGO改C的9脚本；不写最终文案、不测试自身候选。

## 剩余执行

1. root逐条审核本地化冲突和Astra246+64文案，亲自重写不通过项；执行唯一key/描述性文件整理、9status ROOT修复；保持不可变原稿与key契约。脚本改名只改安全独立文件，对本MOD原定义直接修正不叠加z。
2. 冻结，主代理亲审差异+原生源例并运行能让原八个counter失败的严格missing/type AST回归、显示上下文/键唯一/BOM/动态引用/逻辑等价；另显式Sol独立审查脚本、Astra/high独立文案/证据复核。查其余同类初始化问题，不用mock缺省0掩盖真实引擎问题。
3. Git本地refs只留main，标签/远端历史保留。清理余下大型旧decoded存档如果确为旧测试产物（勿删基线/工具或原稿）。编辑器旧projectJSON保留设计但声明source已退役，从M开始新工程，不伪造manifest。
4. 完成三份备份、三方合入M（注意用户可能并行改文案，必须diff基线）、Git上传、正式包，删除本轮临时C。简要新交接指出已主动退役的旧路径。未执行新游戏运行不得声称错误计数已实际归零；空纹理未归因需如实保留。
