# 未做五项的任务提示词（2026-11-07）

按 `nesnd-prompt-kit.md` 第 2 节模板写成。每份开头的“先确认现状”是给开发代理跑的命令：任务账可能比文件旧，先看实际情况再动手。

【】里是只有作者能回答的内容，发出前填好；标“先问我”的留给代理来问。

命令用 Git Bash 写法，在主 MOD 目录下运行。`W` 指工作台，`R` 指 Git 工作副本：

```
cd "D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties"
W="../../nesnd-workbench"; R="$W/projects/nesnd-repository"
```

---

## 1. 法国新后继路线

```
本次任务：按任务29的方案，实施法国新后继路线中的【先实施哪一条：波旁奥尔良“宫廷与外省” / 共和国繁荣分配与右转 / 巴黎与地方配置】。
类型：新内容
游戏：本次不启动游戏，由我复测。
范围：只做本任务。发现的其他问题列在交付说明里，不顺手改。

先确认现状（任务29只交了方案；之后可能有人动过法国文件）：
  grep -m4 -E '^(Status|Execution|Validation|Evidence):' .scratch/debug-release/issues/29-france-political-planning.md
  grep -n "法国" docs/agents/STATUS.md .scratch/debug-release/issues/42-campaign-followup.md
  ls -lt common/journal_entries/ce_french_*.txt common/scripted_buttons/ce_french_* | head
  grep -rln "宫廷与外省\|court_and_provinces" common localization | head
  git -C "$R" log --oneline -8 -- common/journal_entries/ce_french_empire.txt common/journal_entries/ce_french_coalition.txt
  git -C "$R" status --short -- common localization | grep -i french
方案原文：$W/reports/france-politics-plan-20261103/france-development-plan.md

内容：法国在既有帝国/王朝主线之后的后继政治路线。【这条路线里玩家面对什么处境，想玩到什么】
时间与终点：【开始条件（哪一派实际取得政权）、大致时长、怎样算成功/失败/超时】
规模：按 content-design.md 选形状；【大致几个日志、按钮、事件，或交给代理提议】
必须保留：既有法国帝国/王朝主线及已修复的行为；任务46的古吉拉特、包罗达、讷瓦讷格尔直辖与舰队；【其他设定、人物、名词】

方案里写明待证的量（纯迁出修正、都市比例区间、奖励平衡）先问我，不自行定数。
先按 content-design.md 画出内容树（日志、状态量、行动、事件、结局），交给我确认，再写脚本和文字。
```

## 2. 日本新政的差异化选择

```
本次任务：给日本新政（宫廷/军队/代议三条改革路线）加入利益和风险各不相同的实质选择，替换现在只能“加速”的按钮。
类型：新内容
游戏：本次不启动游戏，由我复测。
范围：只做本任务。发现的其他问题列在交付说明里，不顺手改。

先确认现状（任务31仍是 open，任务32只补了按钮反馈；之后可能改过日本文件）：
  grep -m4 -E '^(Status|Execution|Validation|Evidence):' .scratch/debug-release/issues/31-continuity-journal-rework.md
  sed -n '/### 8：日本新政/,/### 9：/p' "$W/plans/two-empires/61-continuity-and-journal-rework-20261104.md"
  grep -n "scripted_button" common/journal_entries/nesnd_jp_politics.txt
  grep -rn "nesnd_jp_inspect_court\|nesnd_jp_court_ready\|nesnd_jp_advance_reform\|nesnd_jp_abandon_reform" common | head -20
  ls -lt common/journal_entries/nesnd_jp_*.txt common/scripted_buttons/nesnd_jp_*.txt | head
  git -C "$R" log --oneline -8 -- common/journal_entries/nesnd_jp_politics.txt common/scripted_buttons/nesnd_jp_politics.txt

内容：日本选定改革方针后，政府如何推动它。计划61第8节的草案是三种干预：资助学务与新法支持者（钱与立法）、与旧臣议定过渡（IG态度与推进速度）、由君主推动改革（权力集中与激进化）。【是否采用这三种；军队、代议两条路线是否各有自己的一组】
时间与终点：沿用现有改革日志的完成条件；不点按钮也能靠正常法律与建设完成；取消路线要有真实退出。【有无时限】
规模：在现有日志里换按钮组，不新增日志链。【每条路线几个按钮】
必须保留：三家分封、产业、独立、文化团结等已有日本内容；现有按钮的费用、期限与反馈显示（任务32）。

数值（费用、修正幅度、冷却）先给候选表问我。
先按 content-design.md 画出这组按钮的树（状态量、行动、可见反馈、结局），交给我确认，再写脚本和文字。
```

## 3. 编辑器完整交付

```
本次任务：对照原规格，盘点地图编辑器现在能做什么、缺什么，交一份差距清单，确认后再补。
类型：工具
游戏：本次不启动游戏，由我复测。
范围：只做本任务。只改 $W/editor 与工具、报告；不改主 MOD、本体或候选。发现的其他问题列在交付说明里，不顺手改。

先确认现状（任务08仍是 open，但不能由此推断没做过；舍入缺陷已由任务10修好）：
  grep -m4 -E '^(Status|Execution|Validation|Evidence):' .scratch/debug-release/issues/08-original-backlog.md .scratch/debug-release/issues/10-editor-rounding.md
  ls -lt "$W/editor" | head -20
  git -C "$W/editor" log --oneline -10 2>/dev/null || echo "editor 不是 Git 目录"
  sed -n 1,40p "$W/plans/two-empires/11-editor.md"
  cat "$W/plans/two-empires/evidence/editor-closure-findings.md"
  grep -n "编辑器" "$W/plans/two-empires/12-scope-ledger.md"

我要的编辑器：改人口数量与文化、地区 TAG、建筑、province 归属、region modifier 及新地区；不改地形环境。先形成差异与守恒表，导出独立候选，不能一键写主 MOD。【还要哪些能力；哪些可以不做】
怎样算交付：【例如：能在 UI 里完成一次拆州并导出候选，我用新开局检查】

先交差距清单：每项写现状（已接通/仅后端/未做）、证据（文件:行或测试）、补齐所需工作量。我确认范围后再动手。
交付：改了哪些文件；跑了哪些工具测试；我在 UI 里怎么验收。
```

## 4. 新美术

```
本次任务：盘点新美术（人物、场景图、主菜单、事件图）已交付和未交付的部分，列出缺口与每张图的规格，确认后再做。
类型：新内容
游戏：本次不启动游戏，由我复测。
范围：只做本任务。发现的其他问题列在交付说明里，不顺手改。

先确认现状（主菜单已由任务64、66接入，两张载入图已由任务61、62接入，开发总结仍记“未全部交付”）：
  for n in 61 62 64 66 69; do grep -m4 -H -E '^(Status|Execution|Validation):' .scratch/debug-release/issues/$n-*.md; done
  sed -n '/新美术/,+2p' docs/agents/history/development-summary-20261106.md
  ls -lt "$W/art"
  ls -lt gfx/loadingscreens gfx/event_pictures 2>/dev/null | head -30
  grep -rn "event_image\|texture" events/nesnd_*.txt | grep -ci "placeholder\|占位"

要的美术：【五张指定场景是哪五张；要新画像的人物是谁；事件图要重绘哪些】
来源与作画：【由谁出图（我自己 / 外部 / 代理生成），尺寸与风格参照】

先交清单：每项写已接入/有样图未接入/未开始，以及接入位置（载入池、事件、人物）与所需尺寸。我确认后再接入。
交付：接入了哪些图、改了哪些文件；DDS 回读结果；我在游戏里看哪里。
```

## 5. 远山宣慰司门槛过严

```
本次任务：修复远山宣慰司（YU1）成立门槛过严的问题，参照任务54对天竺宣慰司的改法。
类型：修复
游戏：本次不启动游戏，由我复测。
范围：只做本任务。发现的其他问题列在交付说明里，不顺手改。

先确认现状（任务54只改了天竺，记明远山“未改”）：
  grep -m4 -E '^(Status|Execution|Validation|Evidence):' .scratch/debug-release/issues/54-tianzhu-commission.md
  grep -n "远山" .scratch/debug-release/issues/54-tianzhu-commission.md docs/agents/STATUS.md
  grep -n "nesnd_yuanshan_commission_ready = {" -A14 common/scripted_triggers/nesnd_commissions.txt
  grep -n "nesnd_tianzhu_commission_ready = {" -A10 common/scripted_triggers/nesnd_commissions.txt
  grep -n "yuanshan" common/scripted_triggers/nesnd_commission_expansion.txt
  git -C "$R" log --oneline -5 -- common/scripted_triggers/nesnd_commissions.txt

我看到的：远山宣慰司要求研究“民主”“开化使命”两项科技、控制南非六个地区中至少4个、祖鲁兰有港口、远山地区有政府行政建筑，同改前的天竺一样过严。
怎么看到的：代理在任务54审查时标出，未实机观察。【若你在对局中见过，补写】
应该是：【放宽到什么程度：几个地区、是否去掉两项科技要求、成立后是否同天竺一样为自治领并可划归新地】
怀疑：门槛沿用旧天竺写法，任务54没有一起改。

按 debugging-and-updates.md：找到决定远山能否成立的全部条件，对照任务54天竺的新写法和 tag original-20261030 的原作。
门槛数值先问我；原因清楚时直接修。
交付：改了哪些文件；原门槛为什么过严；我复测时用哪些控制台命令让条件成立、看哪里。
```
