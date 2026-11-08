# NESND 当前状态

这是项目唯一的“当前”入口。只写现在的情况；历史放 `docs/agents/history/`。维护规则见文末。

更新：2026-11-08（内容树工具）

## 基线

- 游戏：Victoria 3 **1.15.0 Ivan-Chai / Steam build 26453692**。上一基线 1.13.11 / 24799966。
- 主干玩法基线：90fe4b4（任务46）。任务55分支 codex/event-recovery-and-text-archive-20261107 基于0b1fe37，保留任务47–51并应用本次事件修复，不合并main。主目录另保留任务50、52、54改动。指纹见 reports/2026-11-07-event-recovery/release.json；STATIC_PASS。
- metadata 版本 0.2.0，声明支持 1.15.0（仅为包声明）。
- 主 MOD 另应用任务50日志修复（42文件、83按钮、13日志），未同步Git分支；本任务指纹与交付见`reports/2026-11-06-journal-labels/`。STATIC_PASS，待新开局复测。

## 位置

| 名称 | 路径 | 说明 |
|---|---|---|
| 主 MOD | `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties` | 游戏加载目录，唯一可写的游戏目录 |
| Git 工作副本 | `…/Victoria 3/nesnd-workbench/projects/nesnd-repository` | 与主 MOD 是两个目录，合并时逐文件比较 |
| 远端 | `github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties` | 代理用分支，作者合并 |
| 工作台 | `…/Victoria 3/nesnd-workbench` | 工具、备份、报告、原版基线 |
| 技能 | `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3`、`nesnd-player-writing` | 仓库副本在 `development/` |
| 任务账 | `.scratch/debug-release/issues/NN-*.md`，索引 `map.md` | 每项任务的细节与证据 |
| 作者原作 | Git tag `original-20261030`（`f18b6c4`） | 风格与设计的样本 |

## 进行中

- 《西来的学说》已接入西秦经师讲学静态图，衣冠和拱手礼已修，待实机检查事件窗口。见[任务记录](../../.scratch/per-faith-illustration/issues/01-western-teaching.md)。

- Claude：任务65 唐衣大食第①批已实测并修正开局法律与立法支持；第②批（「三教消长」代表人物与改宗、「唐人同心」团结度）及天命说可替换佛门（开局事件二选一、传道、讲堂）STATIC_PASS；第③批（伊朗人起义、迎沙阿或分裂出伊朗、沙阿的新朝与道路）STATIC_PASS；第④批（经济线「大食的矿冶」三阶段、利权与油田特许权）STATIC_PASS；第④批经济线与第⑤批旧日志清理 STATIC_PASS；五批全部交付，待作者统一复测后集中修错。见[任务65](../../.scratch/debug-release/issues/65-per-ethnic-system.md)。
- 主菜单「南 · 北」已使用《接旗》1836四人版（陈东阳居中，牧仲棠、李霄业、拿破仑三世分列）。李霄业的模板注释记明留后与沙阿双重身份。场外解码及安全区检查通过，实际切换及重启记忆待作者复测。见[任务64](../../.scratch/debug-release/issues/64-dongting-main-menu.md)。
- 《接旗》已提前注册，原版旧默认入口也指向它；「原版自动（随 DLC）」可恢复原版选片。场外选取检查通过，列表首项及重启效果待作者复测。见[任务66](../../.scratch/debug-release/issues/66-main-menu-default.md)。
- [任务72](../../.scratch/debug-release/issues/72-observer-1826-errors.md) 已修秀全无效所属国、外交政策与波斯西线重复添加、复国征兵候选不足，STATIC_PASS，待作者观察者新局复测。19:24 崩溃包证实旧头像绑定被 GUI 拒绝；[任务74](../../.scratch/debug-release/issues/74-xiuquan-je-crash.md) 已改为原版大名列表项的作用域，待作者复测打开、悬停和点击；两处原版脚本及三个海军总部只记录。
- Claude：任务69「教士秀全的旅途」全局人物日志（高凉起步、逐州行走、驱逐按钮、传教条、追认圣徒）STATIC_PASS，仅主 MOD，待作者新开局复测；事件图占位，作图说明见任务账附件。见[任务69](../../.scratch/debug-release/issues/69-xiuquan-saint.md)。[任务73](../../.scratch/debug-release/issues/73-progress-bar-labels.md) 已分开传教读数与满条规则，完成全 MOD 条面排查并同步技能，待界面复测。[任务75](../../.scratch/debug-release/issues/75-xiuquan-neighbours.md) 驱逐已由作者实测成功；追加中国地理区目的州限制，待复测落点。[任务81](../../.scratch/debug-release/issues/81-xiuquan-disappearance.md) 据存档定位淮国灭亡时的人物清理，已补剧情保护与失联后追认圣徒；原版法西斯事件的候选提名照常，任命失败后仍可传教。待旧档和新局复测。

- 宫殿及成都焚掠画面已加入随机加载池，DDS 回读通过，待实机观察。见[任务61](../../.scratch/debug-release/issues/61-throne-hall-loadingscreen.md)、[任务62](../../.scratch/debug-release/issues/62-chengdu-loadingscreen.md)。

- Codex：皑雪三州已按确认方案实施，STATIC_PASS，待作者新开局复测。见 [.scratch/aixue-three-states/issues/02-implement-split.md](../../.scratch/aixue-three-states/issues/02-implement-split.md)。

- Claude：任务58修复普鲁士、奥地利、美国、意大利与南方小邦的外交请求按钮恒为“永不”（隐藏的临时作用域在条件里失效），请求条件按类型拆分并改为逐条一句的提示；普鲁士22个德意志协定按钮的效果区写明协定内容、对方接受机会、成功收益与失败代价；“请求自有市场”效果拆成两句短提示；STATIC_PASS，主MOD未同步Git，待作者新开局复测。见 `.scratch/debug-release/issues/58-request-button-tooltips.md`。
- Claude：任务57用 custom_tooltip 消除普鲁士“德意志的共同防卫”条件的 country_c_equal 刷屏报错，判断逻辑不变；STATIC_PASS，主MOD未同步Git，待作者复测。见 `.scratch/debug-release/issues/57-prussian-coalition-tooltip.md`。
- Codex：任务56朝鲜重建运动已加入主MOD，半岛持地国共享压力、请愿与有限战争；STATIC_PASS，待作者复测。见 `.scratch/debug-release/issues/56-korean-restoration.md`。

- Claude：任务54「天竺的土地」改为成立天竺宣慰司（8个印度大陆地区、自治领、划归决议），STATIC_PASS，待作者新开局复测。见 `.scratch/debug-release/issues/54-tianzhu-commission.md`。
- Claude：任务71放宽远山宣慰司门槛（民主＋4个南非直辖地区，去掉开化使命与建筑要求，自治领、划归决议；日志加完成条件、状态行与 X / 4 进度条），STATIC_PASS，仅主 MOD，待作者新开局复测。见[任务71](../../.scratch/debug-release/issues/71-yuanshan-commission.md)。
- Codex：任务59修复任务52国政条面的多行挤压；「海峡彼岸」加入总督与议事会里程碑，KOR亡国后由任务56的全局运动承接。STATIC_PASS，待作者复测。见 `.scratch/debug-release/issues/59-japan-strait-and-progress.md`。

- Claude：任务60 用 `REPLACE:je_acw_countdown` 重写「奴隶制存废之争论」（分裂危机条、和解／内战／失效、分离危机），新增东洲「西岸的砝码」（逃亡、宣称、东进）。STATIC_PASS，仅主 MOD，待作者新开局复测。见 `.scratch/debug-release/issues/60-acw-slavery-question.md`。
- Codex：任务55已落实82条建议：19项适配、61个清单内事件删除、2个有效隐藏入口保留；另删除被取代的nesnd_crisis.41，共62个定义。842条文字入技能。详见 .scratch/debug-release/issues/55-event-recovery-and-text-archive.md。
- Codex：任务49已审计18文件46处参战／涉及判定，修复共同入场、干预、秦边疆、波兰及相关成功标记；STATIC_PASS，待作者复测。详见 `.scratch/debug-release/issues/49-play-commitment-audit.md`。
- Codex：任务50已修动态按钮名、小国条件重复与印度文字适用范围，待作者新开局检查标签、摘要红绿及外交答复。详见`.scratch/debug-release/issues/50-journal-labels-and-conditions.md`。
- 技能于 2026-11-06 重写（分支 `claude/skill-rewrite-20261106`）：去掉模型分工条款和事故记录，新增内容形状与两种声音的写作规则。

- [任务76](../../.scratch/debug-release/issues/76-supply-button-tooltips.md) 商路筹备按钮的中英文条件提示已修，STATIC_PASS，待界面复测。

- [任务77](../../.scratch/debug-release/issues/77-objective-countries.md) 经济第三位为莫卧儿，四栏共16国；已补齐推荐卡双语标题、正文组合键，待重启复测。
- Claude：[内容树工具](../../.scratch/content-tree/issues/01-content-tree-tool.md)已交付（工作台 `tools/content_tree`），USM 内战与南美土著叛乱两份交互图、覆盖率报告见 `nesnd-workbench/reports/content-tree/DELIVERY.md`；查图所见疑似问题只列未改。工作流已写进技能（`references/content-tree.md`），提交 `91ed9a1`，未推送。[独立成仓库](../../.scratch/content-tree/issues/02-standalone-package.md)已完成，仓库在 `OneDrive/Documents/Modings/V3-content-tree`（本地提交，未推送）。

- [任务78](../../.scratch/debug-release/issues/78-forest-of-bayonets.md) 《刺刀之林》首段、和议术语和《人民之春》开头已按 MOD 欧洲史改写。中英文静态检查通过，待实机查看悬停与后继日志。

- Claude：[任务80](../../.scratch/debug-release/issues/80-jingnan-continuation.md) 第二次靖难加蜀军子日志、吴方“继续战争”进度条、吴失大陆后的“天朝帝国解体”与大明联邦链，STATIC_PASS，仅主 MOD，待作者复测。

- [任务79 东洋之议](../../.scratch/debug-release/issues/79-eastern-question.md) 已修吴日倒计时、分封与失败后果及目标选择器。日本重新臣属按日方落败执行解体及后续。作者已实测倒计时、日方羞辱及吴属国自动支持。创建效果已补吴方重组主要要求，待复测吴方要求、两国结案与四岛迁移。

## 已知差异

- 主 MOD 的 `localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml` 是作者改稿，与 Git 不同。先查看差异，不覆盖。

## 未完成

- [本地化审核](../../.scratch/text-audit-20261107/issues/01-localization.md)的 121 条已完成[语体返工](../../.scratch/text-audit-20261107/issues/02-prose-rework.md)，修改 90 条、保留 31 条。STATIC_PASS，待作者复测。波斯另行外审。

### 未做

代理尚未实施。各项的任务提示词（含核对现状的命令）见 [prompts-unfinished-20261107.md](../../.scratch/debug-release/prompts-unfinished-20261107.md)。

1. 法国后继第二、三批：地方建设与人物／政治运动联动、共和国繁荣分配与条件性右转。见任务29方案；第一批已见任务70。
2. 编辑器完整交付（舍入缺陷已修）。任务 08。
3. 新美术：人物、五张场景图、事件图。主菜单已由任务 64、66 接入，两张载入图已由任务 61、62 接入。

### 已做、待作者复测

代码或文字已交付，只做了游戏外检查（STATIC_PASS）。

1. 法国古吉拉特、包罗达、讷瓦讷格尔直辖与本地舰队：任务 46 已写入，未实机验证。
2. HUS 社会阶序的文化提示、阶层悬停及相关 culture/none 错误是否消失：任务 47 待作者复测。
3. [任务67](../../.scratch/debug-release/issues/67-jingnan-participation-and-characters.md)已修正靖难实际参战、日本选边与幕府危局、六人征召；作者确认的剧情人物保护已接入通用刺杀及下野。STATIC_PASS，待新局核参战与投降按钮、危局开启关闭及人物面板。任务49其余战场仍待复测。
4. 任务50命名scope月度刷新、旧档及条件摘要的实际UI表现尚未验证。
5. 任务51月度触发及任务55恢复链待作者新开局复测；已删除事件的旧存档排队不作迁移。
6. 任务60：南北战争满条后几个月内爆发、条明细与1850/1855/1860读数待作者复测。
7. [任务68](../../.scratch/debug-release/issues/68-description-spoilers.md)：七条描述剧透已改（中英），STATIC_PASS；结局提示是否显示被移出的效果待实机看。
8. [任务70「宫廷与外省」](../../.scratch/debug-release/issues/70-france-court-and-provinces.md)：王党接位、巴黎／外省政策、共和国承接与五年评议已写入主 MOD。STATIC_PASS，待作者新局复测。
8. [任务31日本新政](../../.scratch/debug-release/issues/31-continuity-journal-rework.md)三条路线各有三项干预，共用六个月冷却。STATIC_PASS，待作者新局复测扣款、政治效果及搁置。

待作者在游戏中回答的问题（任务 43–44 的界面、靖难战争、原住民复国、流散人口、团结度节奏、地区门槛）见 `history/development-summary-20261106.md` 第 4 节。

## 历史

- `history/development-summary-20261106.md`：开发过程、作者约束、代理自评。
- `history/retained-versions-20261106.md`：工作台中保留的备份与 Git 引用。
- `history/active-work-to-20261106.md`：2026-11-06 前的逐轮交接。
- `handoff-20261105.md`：任务 36–37 的交接。

## 维护规则

- 本文件只写现在。改动时覆盖旧内容，不在顶部追加新的“当前”段。全文控制在两屏以内。
- 一项任务完成：细节写进它的 issue 文件；这里只更新“基线”“进行中”“未完成”中受影响的行。
- 被替换的旧状态如仍有价值，另存为 `history/<主题>-<日期>.md`。
- 技能里不写项目状态。
