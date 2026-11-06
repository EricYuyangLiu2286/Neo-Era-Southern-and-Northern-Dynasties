Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: STATIC_PASS
Evidence: WORK/reports/2026-11-06-play-commitment-audit/

# GNG 与外交博弈参战判定全 MOD 审计（2026-11-06）

## 范围与结论

用户报告 GNG 重现上一轮 HNA 的独立／未参战现象，明确要求本次全面检查并修复同类问题。此授权扩展了任务48的 HNA 限定范围。沿用不启动游戏、独立分支推送、同步主 MOD、不合并 main 的约定。

已对主 MOD `common/`、`events/` 中涉及国遍历、涉及关系、双方 backer 添加／移除逐项做保序 AST 清点：18 文件、46 个有效代码位置（排除注释），逐项结论保存在 `audit-results.json`。另核查实际 join_war、is_active_in_diplomatic_play 的使用，以及直接加入命令的调用前提。

确认并修正 7 个既有文件中的 13 处同类错误或过宽判定，增加 1 个复用 trigger 文件。撤销 HNA 独占的代码例外，共同入场循环现在对所有已选择反吴的国家采用同一标准；包括 GNG、SIH、HNA、PHI、DEI、YN1、JAP。没有把“选择反吴”改成“所有国家无条件反吴”。

## 根因与 GNG 顺序

GNG 与 HNA 共享 `flavorUSM.400` 邀请 → `usm_civilwar.1` 回答 → `ce_usm_civilwar_journal` 等待回复 → USM 的 `.2 immediate` → `nesnd_open_southern_war`。GNG 选择反吴后带有 `usm_opposition_country`，开场先解除对 USM 的附庸关系，再加入反吴领袖所在的 target 方。

任务48仅为 HNA 绕过了 `NOT any_scope_play_involved` 守卫，GNG 仍走旧分支。因此 GNG 只要已经在涉及国列表，即使中立或尚未承诺，加入命令就被跳过。这里的独立是共同入场前的解除宗主步骤，不代表掷骰选中了中立。GNG 自己选择效忠吴方时不应该被强迫加入明方，其原概率和政体选项本次保留。

同一错误还影响后续干预、已加入标记、战争轮次标记、秦边疆共同参战和波兰邀请；仅替换 GNG 标签会继续把缺陷留给其他调用者。

## 证据与来源

- 父提交 `8516522`；GAME 1.15.0 Ivan-Chai，STATUS 基线 Steam build 26453692。
- 开工首先复制整组日志：`reports/2026-11-06-play-commitment-audit/logs/`，66 文件、9,554,029 字节，SHA 见 `log-manifest.json`。分析来自固定快照，未轮询运行中的日志。
- 相关 error 日志主要是 GNG／干预变量未使用及旧事件孤立警告，没有给出加入守卫失败的运行时调用栈。守卫返回 false 本身不会产生错误日志；不把这些警告当成运行时实证。
- 修改前独立备份 `WORK/backups/pre-change-play-commitment-audit-20261106-20261106T233028Z/mod`，1107 文件。逐项源清点和副本在 `audit-inventory-before.json`、`before/`。
- 当前原版 `00_sepoy_mutiny_scripted_effects.txt:909–923` 在选定博弈中直接添加 PAN 等 backer，不以“涉及”替代承诺。script_docs `is_diplomatic_play_participant_with` 明确指 committed participant；`is_diplomatic_play_enemy_of` 区分敌方；战时 `is_war_participant` 与 `is_on_defending_side` 直接检查该场战争。
- `original-20261030` 的吴明事件／波兰邀请原本直接执行加入。`2fcfaf0` 才给南朝共同加入增加“已涉及则跳过”的守卫；任务48留下的非 HNA 分支就是此次 GNG 复现路径。秦相关模块为后续实现，不能称为作者原作。

## 完整修复清单

| 文件 | 修复内容 |
| --- | --- |
| `common/scripted_triggers/nesnd_diplomatic_participation.txt`（新） | 两个带 COUNTRY 参数的共同判定。博弈阶段检查确切涉及列表、实际承诺和目标阵营；主发起国／目标国自身正确计入。战时改查该博弈自己的 war、实际参战者及进攻／防守方，缺失 war 不算成功。 |
| `common/scripted_effects/nesnd_crisis_effects.txt` | 反吴入场对全部国家一致；北方／其他干预的尝试与成功标记分开；开场轮次只在真实 target 方加入后记录；支持吴方的日本使用 initiator 方判定。 |
| `common/scripted_effects/nesnd_south_holdouts.txt` | 后续吴明战争登记成功和清除待参战标记前，核验真正加入 target 方。 |
| `common/scripted_effects/nesnd_qe1_fracture.txt` | 秦边疆联合进攻不再跳过中立涉及国；反向战争目标及“已开战”博弈分支以已承诺 initiator 方为准。战时目标检查也核真实进攻方。 |
| `common/scripted_triggers/nesnd_qe1_fracture.txt` | “已有边疆参战”不再因仅涉及该博弈就成立。 |
| `common/scripted_triggers/nesnd_poland_repairs.txt` | 删除阻止中立涉及国接受波兰邀请的条件；保留原有“未在任何博弈承诺参战”、未与 KRA 交战及确切目标博弈等约束。 |
| `common/scripted_triggers/nesnd_south_holdouts.txt` | 南朝战争涉及日本的间接分支须证实日本在该战争的 target 方，不能凭日本在旁观列表就归入日吴战争。直接以日吴为双方领袖的分支保留。 |
| `common/scripted_triggers/nesnd_civic_project_security.txt` | 地区项目的战争阻断检查真实 war 参与者，避免单纯出现在涉及列表就阻断项目。 |

共同 helper 不负责改变国家选择或强制换边。加入请求与加入成功是两次不同的检查；请求若被引擎拒绝，中立／错误一方不会因此获得成功标记。
`events/usm_civilwar_events.txt`、`common/diplomatic_plays/ce_diplomatic_plays.txt` 与修改前字节完全相同：HNA 95/5、GNG 和其他国家的 AI 权重、独立选择、共和国路线、允许参战规则均保留。

## 其余审计位置

11 个清点文件经核查保持原样，逐行原因在 `audit-results.json`：

- 成就与原版 AI 策略：用涉及／敌对关系做成就或估值，不以它跳过强制加入或记录加入成功。
- 卡洛斯战争历史：从涉及列表中清除殖民地，涉及列表正是清理对象。
- 印度六地区起义、奥地利干预、意大利介入、原版波兰起义与哈萨克事件：在各自具名或保存的博弈内直接加入，未发现同类涉及国短路。奥地利调用前已明确检查未承诺参战。
- 加里波第事件：在战时再用 has_war_with 筛选实际敌国，未发现本次加入问题。
- `ce_poland_events` 的加入命令本身正确；修的是其外部共享邀请条件。
- `flavorCNE.999` 是无正常调用者的旧 DEBUG 事件，未将它当作生产干预入口；其战时使用 backer 命令属于另一个旧调试问题，本次未改。

## 检查与限制

- 实际对旧源运行 `check_play_commitment.py`：GNG、SIH、PHI、DEI、YN1、JAP 的“已涉及但中立”加入检查失败，HNA 因任务48特例通过，直接呈现旧修复未覆盖共享循环的问题。
- 候选同一检查通过：25 条源代码断言与 24 个明确的双方成员边界案例。覆盖未涉及、中立、倾向、承诺正确／错误方、只在另一场博弈承诺、主领袖、战时参与／非参与／错误方、缺失 war。它们只执行实际 AST 的小段布尔逻辑，不模拟引擎随机数、外交规则、AI 或调度。
- 全面扫描确认受修自定义入口不再裸用 `any_scope_play_involved` 作为加入或成功条件；新的两个 helper 内保留该遍历，并附带承诺与阵营条件。原有合法使用逐项登记，不做字符串盲替换。
- 未选择的顶层定义 AST 全部相同；11 个审计后未改文件与备份字节相同；两轮选边及外交博弈规则文件字节相同。
- 实际运行 Paradox Modding Toolkit 0.5.0 LSP，8 个改动／新增文件诊断为空；未保存缓冲区的多余右括号被检测为 stray-close，恢复后为空。Toolkit 的结构诊断标为 ck3-script，此处仅认证解析；未运行 Tiger。
- `git -c core.whitespace=cr-at-eol diff --check` 通过。未启动或操作游戏，仍为 STATIC_PASS。

## 复测入口

主验收用修复版新开局：吴明博弈刚创建和正式开战时，检查 GNG 及其他已选反吴国家是否出现在明方参战名单。仅看地图上独立与否不足以判断；拥明国家也会解除对吴附庸关系。HNA 5% 独立与其他国家原有非反吴选择仍允许发生。

扩展复测可在自然出现时检查：CNE 已接受干预是否真正入明方；日本选择吴方是否入 initiator 方；后续残余战争是否正确登记参战；QE1 多个边疆叛离国是否共同参战；波兰邀请能否让尚未承诺的涉及国正常加入。项目只在本国实际参加当地战争时受战争阻断。

已经漏掉加入或写入错误成功标记的旧存档不会自动补入、重新掷骰或重写结局。本次不添加旧档救援。所有引擎内显示、实际加入与战争结果仍待用户验证。

## Result

新分支 `codex/play-commitment-audit-20261106`，基于 `8516522`；完成后推送并逐文件同步主 MOD，不合并 main。最终提交、同步 SHA 与备份见报告目录 `release.json`。任务48记录保留为历史，其“其他国家同类问题未修”已由本任务覆盖，当前入口以 STATUS 为准。
