# error.log 判读

实际反例run192545：打开陈案就由141变179，未选择任何政策；未加存在性guard的remove_modifier在事件效果预览持续报不存在，最终UI累计48,189。关闭案卷后稳定。轮转只保留8,342条对应错误，因此分别记录“UI累计”“现存文件记录数”“独特错误类型”，不据晚读文件推断用户还开着面板。首要处置是关该预览、保留整个error.N家族和最早快照，再修guard、同存档重测。该例不能归因为挂载或普通冷启动unused提示。

USERDATA/logs 的 error*.log 会轮转。先复制本次整组日志到 WORK/reports/runtime/<run-id>/logs，保留版本、启动时间、加载组合。不要清空日志后把空文件当通过。

已部署 paradox-script-mcp 只查询脚本，不判读引擎 error.log，不执行引擎断言。Tiger 是独立静态报告。本技能 `scripts/log_report.py <日志目录> --out <报告JSON> [--baseline <基线JSON>]` 归组比较；原文仍是证据。

先找最早语法/数据库/未知标识错误，沿路径、行号及调用链读取当前有效源码；后看 scope、人物、媒体和脉冲级联。数千条重复 scope 错误可能来自一个月度问题，不按条数修复。

归因区分本 MOD、被其覆盖的原版文件、依赖、原版也复现、旧存档/DLC、未知。同路径不等于同内容。依赖错误记录其实际影响，必要时在主 MOD 做最小兼容脚本，不编辑工坊素材。

去重只剔时间戳等噪声，保留类型、符号、路径和调用链；记录次数、首末出现、例子及基线新增/消失。不只看末尾几十行，不忽略轮转，不以全局忽略当修复。

开局查历史初始化：国界、人口、建筑所有权、PM/科技、法律/机构、角色、军事/条约。运行查脉冲和重复结算。媒体查 alias/texture/video→文件→portrait gene/accessory/model。文件存在不证明能渲染。

无新增日志仍要看真实结果：选项、人物、进度变化、战争结束和读档不重复。覆盖矩阵与这些观察共同决定 accepted。
# 2026-10-31 测试污染的实证

13674 计数截图对应的轮转剩余12729条、218个精确归组；11592条是同一批变量检查在编辑时重复输出。不能把计数当独立缺陷数，也不能因此忽略其中的真实脚本错误。旧 `-no_filewatcher` 参数错误；当前用 `-nofilewatcher` 和冻结副本，详见 validation.md。

原版对照曾因 QA 创建无数据上下文的 ConsoleWindow 而增加5098条错误。该测试按钮已移除。这些错误属于测试工具，不属于原版或用户 MOD；比较基线须排除并明示，不能用污染过的总数相减宣传修复。

文本生成曾输出物理换行，导致 localization_reader Missing colon/Invalid character。游戏每个本地化条目应占一个物理行，段落用字面 `\\n`。Tiger 0 error 未拦住此问题；必须检查 warning 内容和真实冷启动日志。失败 run024629 保留，修复后重新冻结启动，绝不修改正在加载的副本。

# 事件预览也会生成重复错误（2026-10-31 实测）

土地改革 QA 的 12 项数值断言全部通过，胜利弹窗的 `show_as_tooltip` 仍对已被收尾 effect 移除的 `CNE_land_draft_debuff` 执行移除预览。停留在弹窗界面后，`events/flavorCNE_ce.txt:170` 同一错误重复 2604 次。不能据 PASS 日志判定事件验收成功。清理 effect 和 tooltip 中的 remove_modifier 要按实际存在性保护；弹窗开启、悬停选项、关闭后分别读取日志增量。读取所有 error*.log，包含轮转文件；记录错误总数与去时间戳后的分组数，不直接输出万行。


# 2026-10-31 嵌套提示与日志轮转损失

run143454 的 CNE 土地改革状态链接传入 `[ROOT.GetCountry.GetTooltipTag]`，其 `nesnd_land_rules` 内层仍调用 `ROOT.GetCountry.MakeScope.Var`，导致四个变量每帧各输出 No context supplied + FetchData failed，再加总本地化失败，共九种重复。UI计数增长到四万余；磁盘最多保留 error.log 与 error.1—5.log，本次归档只剩20357行，冷启动114条原文已被挤出，幸存的冷启动JSON包含98组样例和行号。必须明确区分UI累计计数、当前轮转留存量与独立问题数。

每次冷启动完成、进国、触发事件、打开日志、悬停选项、关闭面板与读档后，以动作命名独立目录复制全部 error*.log 并保存哈希，记录该动作起止时间；冷启动原文在首次交互前立即归档，不只存聚类JSON。原文已轮转丢失时如实说明，不拼造“原日志”。发现连续刷屏先移开相关悬停或关闭面板，归档后再判断原因。

Country tooltip 对象不是事件 ROOT Container。当前原版 `localization/english/content_204_l_english.yml:787—788`：外层传 Country.GetTooltipTag，内层用 Country.MakeScope.Var。不要删除动态统计掩盖上下文问题，也不要用 GetPlayer 替代真正传入国家。修复后必须在真实JE中悬停、冻结提示、推进一次统计脉冲及读档，核对显示值和日志增量；Tiger对这类上下文问题不是验收。

run150709已立即归档cold原文，捕获四条Unexpected token: goods。错误都位于can_create_treaty；create_treaty的goods无同类错误。两接口字段不同（good / goods），静态检查器曾错误要求完全同形而通过，Tiger也未拦。此类新引擎证据必须反过来修校验器与函数实例，不能继续把旧“静态0错误”引用为可用证明。


## 轮转与缓冲的实际反例（run180905）

原生help全命令列表使debug.log轮转至debug.3/.2/.1.log；探针BEGIN和结果可能分处不同文件。运行中单看当前debug.log曾得到INCOMPLETE，正常退出flush后找回完整PASS，不能把缓冲当执行失败。读取同一run日志族，按编号降序至debug.log拼接，记录每文件SHA、读取期间稳定性以及原file+line。不要把不同profile或不同启动的log混起来。

qa_batch_probe.py的collector已实际覆盖轮转、缺BEGIN、截断、重复结果、跨周期不能拼成假PASS；无标记只能称“当前可用日志中未观察到”，不能证明整个run未执行。正常退出后运行器的snapshot-integrity与归档日志一起核；未退出时具体结果可报告但注明缓冲边界。
