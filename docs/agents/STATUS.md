# NESND 当前状态

这是项目唯一的“当前”入口。只写现在的情况；历史放 `docs/agents/history/`。维护规则见文末。

更新：2026-11-07（任务55：事件恢复、退役清理与文本归档）

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

- Claude：任务54「天竺的土地」改为成立天竺宣慰司（8个印度大陆地区、自治领、划归决议），STATIC_PASS，待作者新开局复测。见 `.scratch/debug-release/issues/54-tianzhu-commission.md`。
- Codex：任务52日本国政进度明细、方针提示与条件已修复，STATIC_PASS，待作者复测；朝鲜子方案已按任务53修订为亡国后的global重建运动，研究完成待确认，未改朝鲜玩法。见 `.scratch/debug-release/issues/52-jp-politics-ui.md`。

- Codex：任务55已落实82条建议：19项适配、61个清单内事件删除、2个有效隐藏入口保留；另删除被取代的nesnd_crisis.41，共62个定义。842条文字入技能。详见 .scratch/debug-release/issues/55-event-recovery-and-text-archive.md。
- Codex：任务49已审计18文件46处参战／涉及判定，修复共同入场、干预、秦边疆、波兰及相关成功标记；STATIC_PASS，待作者复测。详见 `.scratch/debug-release/issues/49-play-commitment-audit.md`。
- Codex：任务50已修动态按钮名、小国条件重复与印度文字适用范围，待作者新开局检查标签、摘要红绿及外交答复。详见`.scratch/debug-release/issues/50-journal-labels-and-conditions.md`。
- 技能于 2026-11-06 重写（分支 `claude/skill-rewrite-20261106`）：去掉模型分工条款和事故记录，新增内容形状与两种声音的写作规则。

## 已知差异

- 主 MOD 的 `localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml` 是作者改稿，与 Git 不同。先查看差异，不覆盖。

## 未完成

- [本地化审核](../../.scratch/text-audit-20261107/issues/01-localization.md)的 121 条已完成[语体返工](../../.scratch/text-audit-20261107/issues/02-prose-rework.md)，修改 90 条、保留 31 条。STATIC_PASS，待作者复测。波斯另行外审。

1. 法国新后继路线（“宫廷与外省”、巴黎与地方配置、共和国分配与右转）。任务 29、42。
2. 法国古吉拉特、包罗达、讷瓦讷格尔直辖与本地舰队：任务 46 已写入，未实机验证。
3. 日本新政的差异化政治选择。任务 31。
4. 编辑器完整交付（舍入缺陷已修）。任务 08。
5. 新美术：人物、五张场景图、主菜单、事件图。
6. 四份中文改稿对应的旧英文正文：任务 46 已全量审阅重写（只认证这四份）。
7. HUS 社会阶序的文化提示、阶层悬停及相关 culture/none 错误是否消失：任务 47 待作者复测。
8. GNG／其他反吴国、北方干预、日本、秦边疆与波兰的真实参战：任务49已共同修复，待作者复测；HNA 95/5及其他国家原有选择不变。
9. 任务50命名scope月度刷新、旧档及条件摘要的实际UI表现尚未验证。
10. 任务51月度触发及任务55恢复链待作者新开局复测；已删除事件的旧存档排队不作迁移。
11. 远山宣慰司门槛同天竺旧门槛一样过严（民主＋开化使命＋4个南非地区），任务54未改。

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
