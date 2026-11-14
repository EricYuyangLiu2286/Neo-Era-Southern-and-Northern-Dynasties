# NESND 当前状态

这是项目唯一的“当前”入口。只写现在的情况；历史放 `docs/agents/history/`。维护规则见文末。

更新于 2026-11-12。当前跟进法国后继内容和登莱原生路线。此前收口的任务中，已交付的标 completed，未实施的任务 08 原始欠账、南朝立场 01–07 标 rejected。

## 基线

- 游戏：Victoria 3 **1.15.1 Ivan-Chai / Steam build 26591675**。上一基线 1.15.0 / 26453692。[原版覆盖迁移](../../.scratch/migration-1151/issues/02-merge.md)已完成游戏外检查，待作者复测法律生效、分州铜矿及开局历史。
- Git：分支 `fix/tooltip-concepts-observer-buttons`（2026-11-14）已与主 MOD 逐文件同步，待作者合并入 main；同步工具 `nesnd-workbench/tools/sync_main_mod_to_repo.py`。Git main：2026-11-10 与主 MOD 逐文件同步，主 MOD 的新增、改动与删除均已提交。只在 Git 中的 `development/` 旧参考与 `README.md` 照旧保留。其余分支为历史记录，未合入的内容以主 MOD 为准。
- metadata 版本 0.2.0，声明支持 1.15.1。

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

## 未完成

2026-11-14 [「帝国人民的信心」改为按月结算并加收支、民生两项，拨款按钮改按负债比例](../../.scratch/debug-release/issues/97-cne-confidence-monthly.md)已完成游戏外检查，未提交 Git，待作者复测条面明细、名词解释与欠债拨款。

2026-11-14 [地权革命悬停丢失与全 MOD 无效概念链接](../../.scratch/debug-release/issues/96-invalid-concepts.md)已完成游戏外检查，待复测；同批给三角贸易按钮加了观察者模式下的空 root 守卫，待观察者模式实测。

[四类加载报错](../../.scratch/debug-release/issues/95-loading-errors.md)已完成游戏外检查。待新开局复测波斯规则、法国失效分支和两种中美洲文化修正。东亚服装重名来自原版与 EACR。

2026-11-12 [文化团结度日志的转化预告](../../.scratch/cohesion-display/issues/01-cohesion-display.md)：日本、西秦、唐衣大食三个日志的状态行显示下次月结的州、人数和文化方向。同时修了日本转化中可能静默失效的文化比较，西秦与唐衣大食的抽签提前一个月。2026-11-13 加统一结束：研究身份证件或采用委员会共和国、法团国家后三个日志永久结束。技能新增 `references/cohesion-journal.md`。游戏外检查通过，可读档复测。

2026-11-12 [东洲与唐衣大食取消等级制度](../../.scratch/hierarchy-abolition/issues/01-hus-per.md)已完成游戏外核验。待作者复测法律立场、主体文化切换与汗国资格。东洲在登记期内废除等级制度时，编户日志通过单一失效条件退出，待随读档复测。

2026-11-12 [明吴「礼法之下的生活」的两方胜利、长期制度与重复拨款](../../.scratch/wu-mandate/issues/03-wu-victories.md)已实施。取士和税款分配长期改变事权，书院与实业可复办。总日志及四项子日志各有中央、地方胜利和资格失效。游戏外核验通过，待作者实测结局、两年期满后复办与同州奖励续期。

[公民路线人物事件清理](../../.scratch/civic-character-cleanup/issues/01-civic-characters.md)已完成游戏外检查。东洲特许承包与废奴、段敬川任用和西府书院交流待作者新开局复测。

[商路、靖难备战和南洋／印度经济奖励](../../.scratch/journal-rewards/issues/01-rewards.md)通过游戏外检查，待作者复测实际参战时的军需发放及各国、各州修正。

2026-11-12 [普鲁士与德意志](../../.scratch/germany/map.md)两批均已实施：第一批作者实测通过；[第二批](../../.scratch/germany/issues/04-batch2-rhine.md)（共同防卫修订、普鲁士“莱茵问题”、法兰克福“议会”倾向条与 4 个设定事件）游戏外检查通过，待作者实测。

法国后继内容还剩两批，沿用[任务 29 的法国方案](../../.scratch/debug-release/issues/29-france-political-planning.md)。

- 第二批：地方建设与人物、政治运动的联动。
- 第三批：共和国的繁荣分配与条件性右转。

法国后继首批[「宫廷与外省」](../../.scratch/debug-release/issues/70-france-court-and-provinces.md)和[法国印度领地与本地舰队](../../.scratch/debug-release/issues/46-english-gujarat.md)均已完成。

此前收口的任务均已由作者测试完毕（2026-11-10），记录中旧的“待复测”字样已清理。2026-11-10 更新的 Steam 改动说明见 `.scratch/steam-desc/steam_changenote_20261110_*.txt`。

[北洋 / 西洋三角贸易](../../.scratch/triangle-trade/map.md)已修复跨年停买停卖导致的订单失效，两条航线按原批次结算，买卖身份锁定三个月。[成交、锁定与复测](../../.scratch/triangle-trade/issues/03-settlement-and-mode-lock.md)已完成游戏外检查。旧档可观察新排批次，完整验收用新开局。

登莱共和国按[六批定稿](../../.scratch/denglai-route/map.md)实施。作者截图已确认「雪国共和」在通商局显示，[两位周公的选举保护](../../.scratch/denglai-route/issues/03-opening-and-presidents.md)仍待实测。[第 2 批远北、黄金与北海公司](../../.scratch/denglai-route/issues/05-far-north-and-gold.md)及[两批文字的贸易、领土与人物口吻修订](../../.scratch/denglai-route/issues/06-trade-and-state-prose.md)已完成游戏外检查，等作者复测。[第 3 批「复燕」](../../.scratch/denglai-route/issues/07-restore-eastern-yan.md)已完成游戏外检查，等作者实测东燕起事、两种划界及北朝镇压后的整编。[勘金条件与复燕后续文案](../../.scratch/denglai-route/issues/08-survey-and-yan-prose.md)已修订，等作者复测。[第 4 批「渡海」「齐鲁之约」](../../.scratch/denglai-route/issues/09-shandong.md)已实施，待测山东省城与口岸分属不同国家时的外交，以及停战回退。[第 5 批非洲落脚点、垦殖船期与远洋公司](../../.scratch/denglai-route/issues/10-overseas.md)已实施，等作者实测。[第 6 批「君主主义阴谋」](../../.scratch/denglai-route/issues/11-monarchist-conspiracy.md)已实施，六批现均待按各自记录实测。2026-11-11 [外东北分为海参崴、勃利两州，延迟回调改为事件，渡海结盟分支重做](../../.scratch/denglai-route/issues/14-boli-split-delay-alliance.md)，已按 1.15.1 完成[全链可达性与条件概率复核](../../.scratch/denglai-route/issues/15-reachability.md)，待实测。2026-11-12 [俄属远北 9 州人口按东西渐变重算](../../.scratch/denglai-route/issues/17-far-north-pops-gradient.md)，游戏外检查通过，待新开局复测。

2026-11-11 新增帝国级以上国家的常驻日志[「宫廷力量」与「执政者与派系」](../../.scratch/court-power/map.md)，连带给西秦「伊犁的朝议」加了朝争条与两个按钮，并在明吴明论战、法国维持拿破仑王朝的月度随机事件中各加 3 件宫廷事件。游戏外检查通过。[22 张界面素材](../../.scratch/court-power/issues/02-art.md)已接入脚本与界面，待作者实测。

2026-11-13 [蜀国第二次靖难](../../.scratch/shu-jingnan/map.md)的[大汉国旗与属旗](../../.scratch/shu-jingnan/issues/03-great-han-flag.md)已通过游戏外检查。[v3tree 核查](../../.scratch/shu-jingnan/issues/02-trigger-audit.md)记录的朝廷身份、战败顺序、割地与战后日志缺口待处理。投降退战与州控制权待实测。

2026-11-11 [西秦“比例代表制”改为地产投票](../../.scratch/debug-release/issues/88-qe1-pr-to-landed.md)，游戏外检查通过，待作者复测。

2026-11-12 [北明与大革命悬停名词](../../.scratch/beiming-glossary/map.md)已实施：新增 15 条词汇表词条（中英），在 20 个本地化文件插入 94 处链接。游戏外检查通过，待作者复测悬停与嵌套链接。

2026-11-12 [AI 八股清理与 flavor 补写](../../.scratch/ai-cliche-cleanup/map.md)已实施：改写 1,599 个本地化键，143 个事件补了中英 flavor，并清理了注释中的任务编号。游戏外检查通过，可读档复测。另有 13 项待作者判断，见第二轮报告第 6 节。
2026-11-12 第三轮已按作者答复执行：恢复 55 个 ce_ 原作键，英文改为英式拼写，重写 53 条套式 flavor，并列出了需要制作的图片。游戏外检查通过，可读档复测。同日追加：84 条匿名 flavor 已重写，其他代理的 flavor 已全面审查并重写了 72 条，4 条误改的作者手改稿已恢复，作者决定事件图不重绘。待作者决定的事项见[第三轮报告](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-12-ai-cliche-audit/report_round3.md>)第 11 节。

[四国开局科举投票制](../../.scratch/debug-release/issues/90-keju-voting.md)已完成游戏外检查，待作者新开局复测修正案、文人立场和法律显隐。科举已列入民族之春变量清理。

[「伪朝禅代」南下选项](../../.scratch/debug-release/issues/92-cne-intervention-option.md)已对属国北朝禁选，补全两语悬停提示，待作者复测。

2026-11-12 [大吴测试局报错刷屏](../../.scratch/debug-release/issues/94-holdouts-tooltip-flood.md)已修：南方残余势力条件包上 custom_tooltip，内战事件日期改用当前日期。游戏外检查通过，待作者新开局复测。外国干预日志从未激活的问题已改为按跟进旗标自动激活，可读 1838 档复测。

## 已知差异

[重组日本诸藩的战争结算](../../.scratch/debug-release/issues/91-japan-war-goal.md)已在开发版修复占领计时和吴方盟军占领的判定，待作者实测后热修工坊。

[日本三家分封各路线](../../.scratch/debug-release/issues/93-japan-partition-weight.md)已在开发版调整靖难选边、保护国交涉、国书与东征的 AI 权重，游戏外检查通过，待实测整局分封频率。

- 主 MOD 比 Git main 多远北人口与祖地、登莱第 1–2 批及开局补丁，以及三角贸易（文件见其[任务记录](../../.scratch/triangle-trade/issues/01-implement.md)）。文件范围见[登莱路线任务记录](../../.scratch/denglai-route/map.md)，尚未同步。

## 历史

- `history/development-summary-20261106.md`：开发过程、作者约束、代理自评。
- `history/retained-versions-20261106.md`：工作台中保留的备份与 Git 引用。
- `history/active-work-to-20261106.md`：2026-11-06 前的逐轮交接。
- `handoff-20261105.md`：任务 36–37 的交接。

## 维护规则

- 本文件只写现在。改动时覆盖旧内容，不在顶部追加新的“当前”段。全文控制在两屏以内。
- 作者确认完成后，从当前待办中移除该项。任务细节和当时的验证记录保存在各自的 issue 文件。
- 被替换的旧状态如仍有价值，另存为 `history/<主题>-<日期>.md`。
- 技能里不写项目状态。
