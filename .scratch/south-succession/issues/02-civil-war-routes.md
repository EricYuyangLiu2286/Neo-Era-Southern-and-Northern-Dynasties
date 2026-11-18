# 02 吴明论战两条路线汇入同一个内战入口；战后迎驾事件

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-18）
Blocked by: none
Validation: STATIC_PASS（Victoria 3 1.15.1，部署 1587ec5b，待作者新开局复测）
Evidence: 改前备份 nesnd-workbench/backups/pre-change-ming-court-unify-20261118T013547Z；检查 nesnd-workbench/reports/2026-11-18-ming-court-unify/

## 现象与期望

作者：追随郑氏、追随明皇两条路线和平解决失败后，局面应完全相同：吴王篡位，明帝出逃到一个支持者国家，西方拥明军阀对南方大吴，胜方得到同样的等级制度、「礼法之下的生活」内战版本和后续日志。
作者（截图，2026-11-18）：大明联邦与大明行在同时存在。应有一个战后月度检测事件，只触发一次：把行在的天子迁入大明联邦，或拒绝迁移、把天子降为留在行在的贵族藩王。AI 不选拒绝，拒绝方合法性 −25，持续 10 年。

## 原因

- 开战（`nesnd_south_resolve` → `nesnd_open_southern_war`）、篡位（`nesnd_south_accession`）、胜负（`ce_usm_suppress_rebellion`、`usm_civilwar.8`、`.10`）和等级制度（`nesnd_south_order_grant`）都不读路线，两条路线一致。
- 分叉只在明帝出逃（`nesnd_ming_court.2` → `nesnd_ming_resolve_court_migration`）。玩家追随明皇时走 `nesnd_ming_commit_player_transfer`：按 `nesnd_ming_host_rebel` 选湖广或四川，当场即位，行在当场成立并拿到「光复大明」。其余情况走 `nesnd_ming_general_refuge`：按另一个条件 `nesnd_ming_royal_refuge_host` 选国，只把天子送过去，要等该国在 `usm_civilwar.2` 选“拥明”才即位。四川选共和（AI 35%）时天子永远不即位，没有行在。起兵领头国也不同：追随明皇时是行在，否则四川优先。
- 战后两个大明并存：明方胜利后由占南京的一国改为 USM（`nesnd_commit_rebel_settlement`）。胜方不是行在时，天子仍是行在的君主，`nesnd_ming_restore_existing_claimant` 也不会去拿别国在位君主，没有任何脚本收拾这个局面。两条路线都会出现。
- 原作 tag 没有这套逻辑（只有 `usm_civilwar.1` 三选一），分叉是后来代理稿加出来的。

## 改了什么

- `common/scripted_effects/nesnd_ming_court.txt`：`nesnd_ming_find_rebel_host` 对所有路线生效（玩家仍忠于明室时先看玩家所选，再湖广、四川）。新效果 `nesnd_ming_seat_court` 取代原玩家专用的迁移块：天子与储君迁往行在，当场即位，行在得「光复大明」。
- `common/scripted_effects/nesnd_ming_royal_refuge.txt`：`nesnd_ming_resolve_court_migration` 改为单一入口，玩家追随明皇时只多一步 `play_as`。删去 `nesnd_ming_general_refuge`、`nesnd_ming_enthrone_refuge`。出逃后吴的站队一律记为郑氏。新效果 `nesnd_ming_court_dissolve`。
- `events/usm_civilwar_events.txt`：`usm_civilwar.2` 拥明选项不再调用已删的即位效果。
- 迎驾事件 `nesnd_court_followup.20`（`events/nesnd_court_followup.txt`）：大明联邦（USM 且非大吴）在南方定局后、与行在不交战时，每月检测一次（`common/on_actions/nesnd_court_followup.txt`、`common/scripted_triggers/nesnd_court_followup.txt`），全局只触发一次。由大明联邦决定。迎驾：天子与行在储君迁入，联邦行君主制则天子即位，否则为明室宗亲。拒绝：联邦得「拒迎天子」（合法性 −25，10 年），天子降为“明藩王”贵族留在原国。两种结果下原国都不再是行在，原地方领袖复任君主。
- 新修正 `nesnd_ming_court_refused`、新角色 `character_role_nesnd_ming_fanwang`，中英本地化在 `nesnd_court_followup_l_*.yml`。

## 怎么复测

新开局，玩 USM。控制台走法见交付说明。看点：开战当天湖广（或四川）改名大明行在、君主是明帝；明方胜利后若胜方不是行在，下个月大明联邦收到「迎驾」。

## 遗留问题

- 全部未实机验证。`create_character` 兜底立新君、`set_is_noble` 后角色显示未验证。
- 行在拒绝归附时，若日后与联邦开战，迎驾要等停战后才检测。
- 角色 `type = other` 被 tiger 报错，与已有两个明室角色写法相同，未改。
- Toolkit 检查器的反例对照失败（工具本身），本次只跑了 script_xcheck、static_lints、tiger 前后对比、cliche_check、loc_link_check。

## Comments

- 2026-11-18 作者要求用 v3tree 与触发扫查确认不会凭空弹事件。v3tree 以源目录建索引（配置 `nesnd-workbench/reports/2026-11-18-ming-court-unify/v3tree/source.json`），逐一列出改动事件与效果的全部调用方，再核对调用时的状态。查出并修正：
  1. 无人接驾时先发「明室岁费」（`nesnd_court_followup.15`，称宗室留在本国），同一效果随即把宗室送入流亡（原有问题，现在走共用入口）。改为无人接驾时不发通告，通告效果在出逃未定时不发，事件本身再查一次宗室仍在。
  2. 追随明皇的玩家无人接驾时，「去路未定」说朝廷还在南京，天子却已被流放，再遣迎驾使只能立监国。改为等待期间天子留在南京。放弃迎驾（`.12` 选项二）记为出逃已定。
  3. 玩家扮演行在时，迎驾结果没有任何提示。新增通知 `nesnd_court_followup.21`（行在收到，分迎回、拒绝两段正文）。
  4. 「交印归并」延迟 7 天送达，送达时已不是属国的省也会收到，接受即被吞并。事件条件加上仍是发出方属国。
  5. 迎驾只在内战且明方胜利（`usm_civilwar_occured`、`usm_rebel_winner_of_the_civil_war`）时检测，正文“南府已经覆灭……入主南京”始终成立。
- 「行在未归」只在僵局（吴仍在位）出现，与迎驾互斥。「重建大明」要占南京或八处要地中的七处，联邦胜后不会触发。换君主的 on_action（沐朝、日本、山海共和）都不涉及吴明。
