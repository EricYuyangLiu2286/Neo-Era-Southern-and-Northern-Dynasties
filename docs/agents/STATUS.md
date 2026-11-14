# NESND 当前状态

这是项目唯一的“当前”入口。只写现在的情况；历史放 `docs/agents/history/`。维护规则见文末。

更新于 2026-11-11。当前跟进法国后继内容和登莱原生路线。此前收口的任务中，已交付的标 completed，未实施的任务 08 原始欠账、南朝立场 01–07 标 rejected。

## 基线

- 游戏：Victoria 3 **1.15.1 Ivan-Chai / Steam build 26591675**。上一基线 1.15.0 / 26453692。[原版覆盖迁移](../../.scratch/migration-1151/issues/02-merge.md)已完成游戏外检查，待作者复测法律生效、分州铜矿及开局历史。
- Git main：2026-11-10 与主 MOD 逐文件同步，主 MOD 的新增、改动与删除均已提交。只在 Git 中的 `development/` 旧参考与 `README.md` 照旧保留。其余分支为历史记录，未合入的内容以主 MOD 为准。
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

2026-11-12 [文化团结度日志的转化预告](../../.scratch/cohesion-display/issues/01-cohesion-display.md)：日本、西秦、唐衣大食三个日志的状态行显示下次月结的州、人数和文化方向。同时修了日本转化中可能静默失效的文化比较，西秦与唐衣大食的抽签提前一个月。2026-11-13 加统一结束：研究身份证件或采用委员会共和国、法团国家后三个日志永久结束，进行中的团结补贴随之停止。技能新增 `references/cohesion-journal.md`。游戏外检查通过，可读档复测。

法国后继内容还剩两批，沿用[任务 29 的法国方案](../../.scratch/debug-release/issues/29-france-political-planning.md)。

- 第二批：地方建设与人物、政治运动的联动。
- 第三批：共和国的繁荣分配与条件性右转。

法国后继首批[「宫廷与外省」](../../.scratch/debug-release/issues/70-france-court-and-provinces.md)和[法国印度领地与本地舰队](../../.scratch/debug-release/issues/46-english-gujarat.md)均已完成。

此前收口的任务均已由作者测试完毕（2026-11-10），记录中旧的“待复测”字样已清理。2026-11-10 更新的 Steam 改动说明见 `.scratch/steam-desc/steam_changenote_20261110_*.txt`。

[北洋 / 西洋三角贸易](../../.scratch/triangle-trade/map.md)两个全局日志已完成游戏外检查，连带改了登莱、日本、俄国开局奴隶制法律和藏族、琉球的文化传统，等作者新开局复测。

登莱共和国按[六批定稿](../../.scratch/denglai-route/map.md)实施。作者截图已确认「雪国共和」在通商局显示，[两位周公的选举保护](../../.scratch/denglai-route/issues/03-opening-and-presidents.md)仍待实测。[第 2 批远北、黄金与北海公司](../../.scratch/denglai-route/issues/05-far-north-and-gold.md)及[两批文字的贸易、领土与人物口吻修订](../../.scratch/denglai-route/issues/06-trade-and-state-prose.md)已完成游戏外检查，等作者复测。[第 3 批「复燕」](../../.scratch/denglai-route/issues/07-restore-eastern-yan.md)已完成游戏外检查，等作者实测东燕起事、两种划界及北朝镇压后的整编。[勘金条件与复燕后续文案](../../.scratch/denglai-route/issues/08-survey-and-yan-prose.md)已修订，等作者复测。[第 4 批「渡海」「齐鲁之约」](../../.scratch/denglai-route/issues/09-shandong.md)已实施，待测山东省城与口岸分属不同国家时的外交，以及停战回退。[第 5 批非洲落脚点、垦殖船期与远洋公司](../../.scratch/denglai-route/issues/10-overseas.md)已实施，等作者实测。[第 6 批「君主主义阴谋」](../../.scratch/denglai-route/issues/11-monarchist-conspiracy.md)已实施，六批现均待按各自记录实测。2026-11-11 [外东北分为海参崴、勃利两州，延迟回调改为事件，渡海结盟分支重做](../../.scratch/denglai-route/issues/14-boli-split-delay-alliance.md)，游戏外检查通过，待实测。

2026-11-11 新增帝国级以上国家的常驻日志[「宫廷力量」与「执政者与派系」](../../.scratch/court-power/map.md)，连带给西秦「伊犁的朝议」加了朝争条与两个按钮，并在明吴明论战、法国维持拿破仑王朝的月度随机事件中各加 3 件宫廷事件。游戏外检查通过。[22 张界面素材](../../.scratch/court-power/issues/02-art.md)已接入脚本与界面，待作者实测。

2026-11-11 [西秦“比例代表制”改为地产投票](../../.scratch/debug-release/issues/88-qe1-pr-to-landed.md)，游戏外检查通过，待作者复测。

[四国开局科举投票制](../../.scratch/debug-release/issues/90-keju-voting.md)已完成游戏外检查，待作者新开局复测修正案、文人立场和法律显隐。科举已列入民族之春变量清理。

## 已知差异

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
