Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: WORK/reports/2026-11-06-hna-civilwar/

# HNA 在吴明战争开场时未加入拥明方（2026-11-06）

## 用户要求与边界

用户在新开局中多次目击：战争开始时明方仅有蜀国，或蜀国、淮国与第三国，湖广独立而未参战。目标明确为 AI HNA 约 95% 拥明参战、约 5% 独立中立。没有提供独立局数，因此不估计实际故障发生率。
本次不启动、不操作游戏，由用户复测；仅修 HNA 开场选边。不改其他国家权重、不修其他国家的同类加入问题、不救已经开战的旧档。沿用本聊天新分支提交推送、同步主 MOD、不合并 main 的交付约定。

## 证据与版本

- GAME 1.15.0 Ivan-Chai；项目记录 build 26453692。Git 父提交 31c3cfe，包含上一任务 HUS 修复。
- 开工首先复制 USERDATA/logs 整组至 `WORK/reports/2026-11-06-hna-civilwar/logs/`，66 文件、10,765,800 字节；逐文件 SHA 在 `log-manifest.json`，没有清空或修改原日志。
- error.log 中找到 11 条相关名称，主要为 HNA 准备变量未设置、旧事件 orphan、nesnd_joined_south_play 设置后未使用；没有该次 HNA 加入的运行时错误栈。不能把这些启动检查警告当成本缺陷的直接原因。原文行号在 `log-analysis.json`。
- 只读复制现有 `塔万廷苏尤_1841_07_17.v3` 到报告 `save-evidence/observed-1841-07-17.v3` 后解码，原存档未改。Rakaly 0.8.22 不认识一个 1.15 token 0xd04，使用 stringify 保留未知键；未根据未知字段推断行为。相关国家变量均为已识别字段。
- 该副本中 HNA 为国家 310，存在 `nesnd_invited_south`、`nesnd_south_answered`、`usm_opposition_country`、`have_seen_dierci_jingnan`，并有 `ce_usm_republican_revolution_tag`、`nesnd_south_stance=4`；无 `nesnd_holdout_enrolled_round`。这证明该局收到并回答了两次事件，选择过共和路线；晚期存档不保留吴明开场博弈，不能还原加入失败的精确一刻，也不宣称该存档就是用户描述的每一局。
- 独立修改前备份：`WORK/backups/pre-change-hna-civilwar-20261106-20261106T225527Z/mod`，1106 文件核验通过。候选是 Git 工作副本，主 MOD 同步逐文件核 SHA。

## 完整顺序

本节行号取修改前 `before/` 与未改文件，便于对照故障。

| 顺序 | 入口与实际行为 |
| --- | --- |
| 1 | `common/journal_entries/ce_usm_the_last_days_of_ming.txt:44–63`：危机进度等条件满足，调用 `flavorUSM.4`。 |
| 2 | `events/flavorUSM_ce.txt:433–481`：`.4` 的 immediate 准备明室转移、检查篡位条件，调用 `.400`。`.400` 的 immediate 执行篡位并设置 `tag_WUU_var`、`ce_usm_civilwar_journal_trigger`。执行阶段不依赖 AI 对按钮的选择。 |
| 3 | 同文件 `612–623`：只有 HNA 当时是 root USM 的附庸，才设置 `nesnd_invited_south` 并安排 7 天后的 `usm_civilwar.1`。这里 country scope 已切至 HNA，root 仍是 USM，宗主检查正确。 |
| 4 | `events/usm_civilwar_events.txt:14–351`：`.1` 要求 USM 存在、该国未回答、内战未发生且未结算。旧 HNA 唯一有效选项是专用 `.1.1`：设置反吴标记和立场 1。其权重通常为 75+100=175，但因为没有竞争选项，实际是 100% 反吴，不是 95%。`after` 设置 `nesnd_south_answered`，防止重复选择。 |
| 5 | `ce_usm_civilwar_journal` 自然激活并设置 3 个月缓冲；每月重算未回复数和反吴国数。缓冲到期且回复完成并存在反吴国，outcome 在 USM 调用 `.2`；180 天 timeout 也按是否存在反吴国分流到 `.2` 或和平 `.3`。 |
| 6 | USM 的 `.2 immediate` 先设 `have_seen_dierci_jingnan`，再调用 `nesnd_open_southern_war`。该 effect 用全局 `usm_civilwar_occured` 防重入；优先玩家拥明接收国，否则按蜀、湖广、淮等顺序选反吴领袖。只有 `usm_opposition_country` 国家可进入此路径。 |
| 7 | `common/scripted_effects/nesnd_crisis_effects.txt:281–292`：所有仍属 root USM 的反吴国先 `make_independent=yes`，然后由 USM 创建以反吴领袖为 target 的 `dp_usm_civil_war`。所以“解除宗主”是参战准备，不等于选中了少数独立路线。 |
| 8 | 同文件 `293–340`：找到刚创建的、USM 发起的同类型博弈，保存确切 scope。遍历独立的非领袖反吴国，执行加入 target 方。旧守卫只查 `NOT any_scope_play_involved(candidate)`；只要 HNA 已在涉及国列表，就会跳过 `add_target_backers`，即使它尚未承诺站队。真正站在 USM 对面的国家才写入轮次标记。 |
| 9 | 同文件 `341–379`：给各国安排 1 天后的 `.2`，处理已有北方／日本干预，最后将博弈升级到 90。`.2` 在非 USM 国家不会再次创建战争。 |
| 10 | 旧 `.2` 的拥明、共和选项权重分别 65、35，无 HNA 特例。这是政体／战后目标分流，不是 95/5；两者都保持反吴标记，旧原作也都曾直接加入反吴方。共和选项设置立场 4 和共和变量，但没有从博弈撤出的命令。不能把 35% 共和路线直接等同于 35% 中立。 |
| 11 | `dp_usm_civil_war.on_war_begins` 只给实际参战的反吴国登记轮次，不替未加入者补加入。`enable_switch_sides=no` 从原作起一直存在。 |

创建博弈的原生 on_diplomatic_play_started 挂有波兰换边、日本登记、美洲登记回调：分别要求波兰关系、目标 JAP、USA→HUS，未发现针对 HNA 的独立或撤出动作。引擎内部回调相对同日事件队列的细粒度时序未实测，但这些回调不承担 HNA 加入。月度 `.5` 处理首都失败且没有独立命令，`.6` 已为 always=no；其余 make_independent 位于后续结算／投靠事件，非新局开场前置路径。

## 根因与原版、历史对照

1. **后加的加入守卫混淆“涉及国”与“实际站队”。** `any_scope_play_involved` 遍历涉及国；GAME 文档另有 `is_diplomatic_play_involved_with` 和 `is_diplomatic_play_participant_with`，后者才说明 committed participant；`is_diplomatic_play_enemy_of` 检查与指定国家处于敌方。原版 GUI 也区分 IsInvolved、IsUndecidedParticipant、IsBacker。仅仅出现在涉及国列表不足以跳过加入。
2. **95/5 没有在当前 HNA 开场链中实现。** 没有 95 的 random_list；第一轮是 HNA 唯一合法选项，第二轮是通用 65/35 ai_chance。旧日志没有证明 AI 修改器把某个 95 覆盖，因为代码里原本就没有这个 95。
3. **原生 AI 可能接手未承诺的国家。** 旧守卫漏掉强制加入后，留下的国家仍受普通外交 AI 处理；不能把这种结果说成“已成功强制加入后又被 AI 覆盖”。没有找到 HNA 被脚本撤出或转至吴方的开场命令。修复同时明确排除选择 5% 独立的 AI HNA 对此类博弈的普通参与资格。

原始 `original-20261030`：第一轮普通 HNA 为反吴 175、效忠 USM 15，约 92.1% 反吴（不计特定人物减权），独立选项只给云南／日本；第二轮为拥明 75、共和 23，两者都调用 `add_target_backers`。原作也不是用户本次明确的 95/5 独立分布。
后续 `8623191` 将 HNA 第一轮改为专用唯一反吴选项；当前第二轮 65/35 可见于 `c1463da`。`2fcfaf0` 才在共同加入循环中增加“不在 any_scope_play_involved 才加入”的守卫，是此次可定位的加入路径回归。此前源码与完整 diff 已保存到 `history/`。

原版同类：`GAME/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:909–923` 找到指定起义博弈后直接 `add_target_backers={c:PAN}`；没有用“是否涉及”阻止实际加入。当前 script_docs 的 add_target_backers 支持 diplomatic_play 作用域及国家列表。新代码仍在已保存的本次博弈 scope 内执行，不采用全局任意战争或定时补救。

## 修复的 3 个游戏文件

- `events/usm_civilwar_events.txt`：HNA 专用反吴权重改为固定 95，去掉仅用于其他国家／旧人物的无效修正；允许 HNA 选择原有“本国自理国政”选项，并将其 HNA 权重设为 10−5=5。其余国家仍为原权重。HNA 已选反吴后，第二轮共和选项 AI 权重 35−35=0，忠明选项归一化为 100%，避免二次改变已确定路线；玩家仍可主动选择原有选项。
- `common/scripted_effects/nesnd_crisis_effects.txt`：开场共同加入循环中仅为 HNA 增加实际阵营判定：HNA 尚未同时满足“与 USM 为敌”和“与 USM 同处一场博弈的已承诺参与国”时，在保存的本次博弈中加入 target 方。仅倾向明方但未承诺者也会正式加入；已承诺站在明方的不重复加；若 HNA 是领袖，则原生 target 身份已满足参战，原循环会排除它。其他国家继续原判断，未扩修。
- `common/diplomatic_plays/ce_diplomatic_plays.txt`：已回答开场事件但没有反吴标记的 AI HNA，不再由普通 AI 加入该类博弈，保持 5% 独立结果。玩家及其他国家不受此新增过滤影响。

无新增事件、变量、计时器、旧档修复、重投掷骰或本地化；既有选项效果与文字保持。概率在首次宣召选边时确定，实际入场在开战 effect 中完成。

## 外部验证

- 保序解析 3 文件。`check_hna.py` 在原始 before 上实际 FAIL：无95/5、有第二次65/35、已涉及但中立的 HNA 会被跳过、独立 HNA 未限制普通参战；修复后 PASS（20 条定向断言）。
- 输入“已涉及但尚未站到 USM 对面”时：旧 guard=false，新 HNA guard=true；输入“已承诺在明方”时不重复加入；仅倾向明方尚未承诺者继续执行加入。检查的是实际 AST 的小段布尔逻辑，不冒充游戏执行。
- HNA 首轮权重 95/5、次轮 65/0；SIH/GNG/PHI/YN1/JAP/DEI/USM 两轮权重与原版候选相同。其他国家的原加入守卫未变。
- 核对 make_independent → create_diplomatic_play → add_target_backers → add_escalation 顺序。两次事件之外的事件 AST、开战 effect 之外的 effect AST、两次选项的实际效果与玩家文字均相同。
- 实际运行已安装 Toolkit 0.5.0 LSP：3 文件无诊断；在未保存缓冲区加多余右括号，检测到 stray-close，恢复后清空。其结构诊断标为 ck3-script，仅认证真实解析，不认证 Vic3 运行时。未运行 Tiger，未启动游戏。
- `git -c core.whitespace=cr-at-eol diff --check` 通过。报告 `regression-before-checks.json`、`after-checks.json`、`toolkit-checks.json`、`toolkit-protocol.json`。

## 用户复测

正式验收用修复版新开局，保持 HNA 为 AI。篡位宣召后观察其是否宣布独立；战争博弈创建后以及真正开战时，分别检查 HNA 是否在以蜀国／明方领袖为首的 target 方参战名单中。不能仅凭地图颜色或宗主关系判断：拥明的 HNA 也会先解除对 USM 的附庸关系，但必须出现在明方参战名单。
95% 路径应显示拥明、与吴交战，并有 `usm_opposition_country`、`nesnd_restoration_side`；加入后轮次登记可辅助确认。5% 路径应独立且不参加这场战争，没有 `usm_opposition_country`。不要以少数几局必须出现固定次数来验概率；没有统计实测结果之前，只认证脚本权重。

篡位宣召前的旧档可辅助检查此流程，但新开局是验收基准。已经回答 `.1` 的旧档不会重投95/5；已开战／已失败加入的旧档不会补入或改阵营。反复读取同一份已选边存档不能测试概率分布。

## 遗留问题与证据限制

- 通用 `nesnd_join_opposition_play`、日本入场及后续残余战役仍有同类 any_scope_play_involved 判断；依本次仅 HNA 开场范围，记录而不修改。它们可能影响其他国家或后续战争，未宣称全局解决。
- 本快照还有旧 HUS culture scope 轮转、变量／孤立事件、原住民文化修正缺失、variable_list_size 读 target 失败、日志 outcome、地图港口等告警，未扩修。
- 本任务消除已确定的错误权重和会跳过中立 HNA 的逻辑路径；未在引擎中证明最终实际参战率为95%，亦无统计依据给出用户此前遭遇的精确失败频率。

## Result

源码修复与外部检查完成，STATIC_PASS，待用户实机复测。新分支 `codex/hna-civilwar-alignment-20261106` 基于 31c3cfe；具体提交、远端及主 MOD 同步 SHA 见 `WORK/reports/2026-11-06-hna-civilwar/release.json`。未合并 main。
