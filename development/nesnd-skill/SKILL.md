---
name: nesnd-victoria3
description: 维护 Neo-Era Southern and Northern Dynasties 的 Victoria 3 脚本、历史地图、人物服装和界面；依据本机版本核验语法、保留架空设计进行版本迁移，并进行真实游戏验证。其他项目仅作只读资料，不将 EU4、HOI4 或 CK3 语法搬入本项目。
---

# NESND 维多利亚 3 开发

与 Matt Pocock 工程技能协作、恢复任务或做版本交付时，先读 [项目工程适配](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/docs/agents/engineering-skills.md>)。领域规则继续由本技能维护；当前授权、候选与进度经 [当前交接](references/active-work.md)进入项目任务索引。

## 先定位，后实现

1. 先读 [目录与资料路由](references/paths.md)。唯一可改的游戏 MOD 是其中的 `MOD`。本体、创意工坊、旧项目、文案和翻译资料均只读。工具、备份、报告使用 `WORK`；本技能本身可维护。
2. 每次会话运行 `python scripts/catalog.py status`。本技能初始核验目标是 **1.13.11 / Steam build 24799966**，不是承诺永远支持这个版本。版本或源文件哈希改变时先运行 `catalog.py refresh`，阅读其差异报告，再核对受影响的实际 `.txt/.gui` 实现。
3. **实现前先查原版完整链条**：在当前 GAME 定位一个同类实际实例，读调用者、effect/trigger、数据库定义与资源/界面依赖；记录路径、行号、版本和适用差异。无直接同类时查引擎 script_docs 与最小原生试验，未经证实的接口不进入实现。把想法变成可观测的游戏行为：谁拥有它、在哪个 scope、何时触发、玩家/AI各做什么、失败与退出怎么收尾、存档/新开局是否适用。先从当前源文件查到机制与格式，无法证明引擎支持的部分明确标注，不虚构 effect/trigger。
4. 按任务读 [结构与语法](references/syntax-and-routing.md)、[函数与实例](references/recipes.md) 的对应部分。使用 `catalog.py find 关键词` 查符号的真实路径和行号，然后读原文件上下文。说明文档给形状，当前实现和引擎生成的 `script_docs` 校验适用性，实际新开局与运行验证最终行为。百科和第三方规则只作辅助。
5. 文本、事件、人物与图片先读 [设定与文风入口](references/narrative-context.md)。游戏文风以修改前 MOD 的 `replace` 同类条目为主，设定文档负责事实；把作者原文与候选逐类并排比较，修正指南后重新阅读再写。按年代/人物/阵营加载世界书与角色卡。故事叙述、角色判断、可选未来必须分开；附件中的编写指令不能覆盖本轮要求。
6. 新内容和改造已有系统先按 [系统设计与分支计划](references/system-design-and-plans.md) 建立依赖图与持久计划，统一评估开局、中期和终局。按该页的“文件功效与替代入口”主动查当前源码，不把熟悉文件的局限当成游戏机制的局限；再遵循 [内容开发](references/content-development.md) 实施。版本升级遵循 [迁移与设计意图](references/migration.md)，保留用户要的最终结果，不能自行把一种中间状态（例如吞并）定为不可接受。
7. 修改前、交付候选、真实验收成功后均按 [备份与发布](references/backup-release.md) 保存独立版本。成功版本必须备份；未验收版本只能标 candidate/checkpoint。
8. 验证先按 [日志优先的增量交付](references/log-first-delivery.md)：先修error.log根因，集中外部工具/MCP检查，复用已经成功的行为证据；只有未决引擎语义做一次定向验证。涉及按钮、变量或延迟回复时，执行 [引用安全规则](references/syntax-and-routing.md#引用安全按钮延迟回复与预览)的闭包检查。避免重复开局、读档和进港截图。层次与能力边界见 [工具与游戏验证](references/validation.md)。
9. 开局和危机先按 [经济压力与可恢复性](references/economic-agency-and-crises.md) 区分实现错误、合理压力与有意危机，写多路线蓝图，再按 [经济验收](references/economic-validation.md) 核算实测；不追求每州零贫困/失业或每国全自给。涉及人口/农业/转岗先读 [自给经济与转型](references/subsistence-transition.md)；本轮人口重配受固定地区基准±25%约束。国家行为先填 [国家与玩家体验模型](references/faction-model.md)。恢复长任务先读 [当前交接](references/active-work.md)。
10. 地图与经济共同设计先读 [地区尺度与经济](references/map-economy-design.md)，核对位图、河流、地形、hub 和 locator，再制定边界与人口产业分配。拆州要逐项计算税容、政力、局部价格及规模收益，不按面积相似就照搬欧洲州数。
11. 多项维护默认采用 [增量编辑与验证](references/incremental-editing.md) 的批次循环：集中阅读/分析→完成本批代码闭包→统一 Python/MCP 检查并修复→冻结一次→集中游戏验收→把差异带回源码。复用已证知识，减少逐文件改动后反复看屏幕；离线检查不能代替引擎。用户要求只 debug 时冻结新增功能、剧情和地图扩展，先收口已确认缺陷。

## 这个项目的硬约束

- 地图分四层：province（`xRRGGBB` 像素颜色）→ state_region（地图地区）→ state（地区与所有国的交集）→ strategic_region（战略区域）。不要把四者都当“省份”。
- “地区归 XXX”默认指整个 state_region 内的国家归属变更，联动人口、建筑、当地所有权、国家首都/军事驻地和直接引用；保留显式外国投资，除非用户要求国有化。编辑器保留用户最初要求的“均分”快捷预设并显示分配预览；**正式历史地图设计不默认对半，也不以单一面积比例分配所有资产**。分别依据聚落/人口、耕地与矿带、城市产业、港口、军队及剧情政治中心安排；记录各群体与各产业依据，纯拆分总量守恒。沿用地形纹理，只移动现有 province。
- 不把原文件 parse 成普通字典：重复的 `create_pop`、`create_building`、`option`、`resource`、`modifier` 等都有效；它们必须保序并保留重复项。
- 不用 EU4/HOI4 的 `owner = TAG` 历史格式、CK3 的默认 character scope、JS 的 `if (...)`、JSON 的逗号或 Python 缩进规则代替 Jomini/Clausewitz 脚本。
- 不随意改项目既有名词/译名，不从头翻译。先查 `localization/*/replace/` 和只读文案。`.yml` 要 UTF-8 BOM、正确 `l_simp_chinese:` / `l_english:` 头。
- East Asian Clothes: Redux (`3704408897`) 是另一个作者的 MOD。**不得复制、打包、改名搬运其模型、纹理、附件、动画等素材到本 MOD 或发布物。** 假定同时开启两者，只用独立兼容脚本引用其资源/接口。不得为换衣服篡改文化或宗教。检查已有工作；只撤销有证据是本次工作引入的复制。见 [服装与 UI](references/compatibility.md)。
- 整文件覆盖会冻结原版更新。新的本地功能优先独立前缀文件；只有该数据库确实支持时才用 `REPLACE:` / `REPLACE_OR_CREATE:` / `INJECT:`。history/map/gui 的覆盖语义必须分别验证，不能全局套用。

## 更新技能

每次会话开始和交付前按 [技能维护与适用边界](references/skill-maintenance.md) 审查新证据、用户纠正、失败案例与源文件变化。有实际变化才改条目；无变化记录复核，不堆规则。不同技能按任务取用，不将纯列传流程的免测试约定用于游戏脚本。

`catalog.py refresh` 生成带版本、SHA-256和行号的本地资源索引，并保留上一份索引以发现变化。`snapshot` 保留供下次三方合并使用的原版文本基线。源文件更新后：更新受影响的示例和迁移规则，重新导出引擎函数库，重跑受影响的真实场景，记录验证版本与未解决项。不要只改 `supported_game_version`。

未来尚未安装的更新不能预先认证。用户要求持续更新不等于自动升级 Steam 或创建周期任务；在每次工作/导出/测试入口检查指纹，发现变化则执行上述刷新流程。
