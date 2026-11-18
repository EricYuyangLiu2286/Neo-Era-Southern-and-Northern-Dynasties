# 100 吴吞并日本后的三家分封

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS（Victoria 3 1.15.1，待作者复测）
Evidence: [日志副本、内容树邻居、Toolkit、静态检查、数据图](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-16-japan-partition-trigger>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-japan-partition-trigger-20261116T165451Z/manifest.json>)

## 现象与期望

作者在观察者局看到 AI 的吴吞并日本后没有三分，没有存档。期望吴拿下日本后大概率按既定安排三分。

## 原因

- 分封效果 `nesnd_partition_japan` 有五个调用者：日本接受国书、战争目标兑现、日本重新臣属、待分封月检、吞并后重建。前四个要求日本存活。重建要求吴带 `nesnd_japan_recovery_pending`。
- 该标记只有三处写入，都绑定靖难：`usm_civilwar_events.txt:787`、`nesnd_war_collapse.txt:11`、`nesnd_japan_recovery.txt:335`（要求兑现的博弈就是登记的靖难博弈）。
- 日本开局是吴的朝贡国。AI 用原版手段吞并（降低自治后吞并属国、征服州、对弱国的吞并战）不经过上述任何一处。东洋之议在日本亡国时走隐藏的失效结局并关闭议案。
- 发国书要求吴处于和平。旧观察者档（任务 91 的六份存档，1851–1853）里吴始终有进行中的战争目标，十年没有发出国书，议案超时关闭。此后只剩原版手段。这一条是按旧档推断的，本次没有存档可证。
- 工坊版与开发版在这条链上的脚本相同，只有日志文件差一行，同样有此缺口。

## 改了什么

- 新增 `common/decisions/nesnd_usm_enfeoff_japan.txt`：吴（`tag_WUU_var`）在南方已定、日本、扶国、和国均不存在、尚未分封、未在重建中，且拥有关东、京都或中国地区的州时显示。吴在这三个地区各拥有并控制至少一州时可执行。执行后设 `nesnd_japan_recovery_pending` 并调用 `nesnd_japan_recovery_request`，其余走现有的重建和分封。AI 权重 100，玩家自愿。
- `common/scripted_buttons/nesnd_japan.txt`：发国书的 AI 权重由 60（原反吴日本 70）改为 100。
- `common/scripted_triggers/nesnd_japan.txt`：`nesnd_japan_diplomatic_window` 中吴的 `is_at_war = no` 改为 `OR = { is_at_war = no is_ai = yes }`。玩家的条件和提示不变。
- 中英文各四条：决议名称、说明、条件提示、效果提示。

## 怎么复测

新开局验收。读档也可以，条件是档里吴仍带吴路线标记、南方已定且尚未三分。

1. 补救入口：`tag USM`，`annex JAP`，打开决议页看「分封日本诸藩」，执行后隔两天看地图和宗属。九州、四国留吴，关东与北方归扶国，京都和大阪归和国，关西余部与中国地区归丰臣，三家都是吴的保护国。
2. AI：观察者局里用 `annex` 让 AI 的吴吞并日本，看它是否在几个月内自行执行。
3. 国书：观察者局看吴在别处有战争时是否仍发国书，日本拒议后博弈能否建立。

## 遗留问题

- 走决议的重建不带吞并前的州登记，原有朝鲜领地留在吴手里，不交给丰臣。靖难路线不受影响。
- 吴只征服了日本一部分、日本仍存活时没有入口。
- AI 的吴在战争中发国书，日本拒议时要另开一场博弈。交战中能否建立这场博弈没有实机验证。建不成时议案会停在「等待答复」直到十年超时。
- AI 评估决议和按钮的频率在脚本里查不到，权重 100 只保证每次评估时优先。
- 靖难中由原生战争目标吞并日本时，登记转为重建依赖兑现回调发生时日本已不存在，这一时序没有实机验证。即使失败，决议现在也能接住。

## 第二轮（作者 2026-11-16 定的两条设计）

作者的设计：日本被占一部分而尚存时，仿南朝续战开日志“东征”，读条 6 个月后开战，吴要吞并，日本要收复，不许停战。分封决议在日本被吞并或成为附庸、南朝内战结束时可用。

- 新日志 `nesnd_wu_eastern_expedition`（`common/journal_entries/nesnd_japan.txt`）。启用条件 `nesnd_eastern_expedition_ready`：吴路线，日本存活且独立或仍是吴的朝贡国，吴在九州以外拥有本州、北海道或四国的州，南朝战事结束，吴是列强而日本不是，两国都没有战争和博弈，彼此没有停战。进度条 `nesnd_eastern_expedition_bar` 每个满足条件的月份加 1，不清零。满 6 后在下一个满足条件的月份调用 `nesnd_eastern_expedition_open`。
- `nesnd_eastern_expedition_open`（`common/scripted_effects/nesnd_japan.txt`）：日本若是朝贡国先独立。给日本加上吴在四岛所占各州的宣称，建立博弈 `dp_nesnd_eastern_expedition`（吴的目标是 `wg_nesnd_usm_annex`，日本对吴在四岛的每个州各有一个 `return_state`，九州在内），关闭东洋之议，登记日本现有各州，随即开战。博弈不许议和，双方不能再加目标，吴不因开战目标得恶名。博弈没建成时恢复朝贡关系。
- 日本灭亡时日志完成，提示可用分封决议，并去掉日本对九州、四国的宣称。吴失去九州以外的土地、日本成为别国属国或朝贡以外的吴属国时，日志隐藏作废。
- 九州不算“被占”：开局时吴已拥有九州一部分，算进去会使东征在南朝战事一结束就必然发生。
- 决议 `nesnd_usm_enfeoff_japan` 改为两种情形。日本已被吞并：同第一轮。日本是朝贡国以外的吴属国（`nesnd_japan_held_as_subject`）：要求关东、京都、关西、中国地区都在日本或吴手中，执行时 `nesnd_japan_enfeoff_subject` 把吴在本州和北海道的州还给日本，记为臣属并关闭东洋之议，再调用 `nesnd_partition_japan`。席位被占领时由原有的月检补做。
- 南朝战事结束的判定 `nesnd_japan_south_war_over`：没有进行中的靖难博弈，吴不是叛军获胜的一方，并且全局已定、维持现状或吴带政府军获胜标记三者有其一。这一条从“显示条件”移到“可执行条件”，玩家能看到缺什么。
- 开局的朝贡关系不算附庸：东洋之议正是与朝贡的日本交涉，算进去会使决议在南朝战事结束后立刻可点。

### 第二轮的复测

1. 东征：`tag USM`，让吴取得本州一州（例如对日本打一场征服战，或在调试模式下改州归属），确认日本尚存、两国和平、没有停战。日志页出现“东征”，进度条每月加 1。满 6 个月后两国直接开战，战争界面没有议和选项，吴的目标是吞并，日本的目标是收回各州。
2. 东征获胜：`annex JAP` 或打完战争。日志完成，决议页出现“分封日本诸藩”。
3. 附庸：让日本成为吴的附庸或保护国后看决议页。执行后当天完成分封，原有朝鲜领地留给丰臣。
4. 朝贡国的日本不应出现决议。

### 第二轮的遗留问题

- 日志要在两国同时和平的某一天才会启用。启用后进度不清零，但 AI 的吴长期有战事时仍可能很久才开战。
- 日本是第三国属国时没有入口。
- `add_war_goal` 对已建成的博弈追加目标、`return_state` 靠临时宣称生效，都只过了脚本文档的交叉检查，没有实机验证。只有第一个收复目标写在建立博弈的块里。
- 东征不给吴恶名，是仿靖难博弈定的，可按需要改。
