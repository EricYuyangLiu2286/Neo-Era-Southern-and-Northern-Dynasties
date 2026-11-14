# 2026-11-11 技能整理：各段去向

> 何时读：在旧任务记录、交接或提示词里看到已不存在的技能文件名，或要核对某段旧规则去了哪里。不必读：日常开发。

- 整理前备份：`WORK/backups/pre-change-skill-reorg-20261111T120525Z/`（两个技能目录、主 MOD 的 `AGENTS.md` 与 `docs/agents/`，67 个文件，SHA-256 清单在 `manifest.json`）。
- 防丢失检查：`python scripts/skill_loss_check.py --old <上面的备份>/skills`。结果见文末。
- 整理目标：`SKILL.md` 只做入口；`references/` 放做法，`lookup/` 放查表；每个参考文件开头一行写何时读；同一条规则只在一处写全。

## 1. 文件级去向

| 旧文件 | 新位置 |
|---|---|
| `SKILL.md` | 改写为入口（硬规则、通用做法、路由表、主题表）；“向谁学”移到 `lookup/paths.md` |
| `references/recipes.md` | 拆分：事件链登记与需求可行性 → `references/content-design.md`；进度条 → `references/journal-state.md`；历史归属与新地区 → `lookup/map-data.md`、`references/map-economy-design.md`；DNA、1.13.11 差异与 AI 权重 → `lookup/engine-facts.md`；嵌套悬停 → `lookup/journal-ui.md`；目录说明 → `lookup/engine-syntax.md` |
| `references/syntax-and-routing.md` | 拆分：语法骨架与文档配对 → `lookup/engine-syntax.md`；引用安全、覆盖原版、回调、人物、案件隔离、文化转换 → `references/script-safety.md`；接口事实 → `lookup/engine-facts.md`；全局日志 → `references/journal-state.md`；湖泊 → `references/map-economy-design.md` |
| `references/journal-text-contract.md` | 拆分：1.15 字段、条面、配图、概念与数据上下文 → `lookup/journal-ui.md`；状态、同步、阶段、父子日志 → `references/journal-state.md`；条件、提示、按钮预览、可见结局 → `references/journal-display.md`；随机姓名 → `lookup/engine-facts.md`；“开发说明不进正文” → `nesnd-player-writing/references/no-invention.md` §7 |
| `references/map-economy-design.md` | 拆分：尺度、经济、建筑与唯一建筑、就业 → 原文件；交通网、港口、门禁、海域迁移 → `references/map-transport.md`；数据入口、编号、编辑器操作 → `lookup/map-data.md` |
| `references/numeric-scale-contract.md` | 方法留原文件；已核实例、军需、有界算术 → `lookup/numeric-facts.md`；按钮/事件 AI 权重段 → `lookup/engine-facts.md` |
| `references/political-design-and-difficulty.md` | 原文件；党派原生字段段 → `lookup/engine-facts.md` §政治 |
| `references/faction-model.md` | 并入 `references/regional-history-and-survival.md` 末节 |
| `references/paths.md`、`vanilla-overrides.md`、`native-treaty-aid.md` | 移到 `lookup/`，内容不变 |
| `references/narrative-context.md`、`north-south-institutions.md`、`worldbook.json`、`character-book.json` | 移到 `lookup/canon/`；“事件文本预设”两段 → `nesnd-player-writing/references/fields.md`（通则）与 `voice.md` §2 |
| 其余 `references/*.md` | 原位，加“何时读”一行，个别链接与指引更新 |
| `scripts/__pycache__/` | 删除（缓存） |
| 新增 | `MIGRATION.md`、`references/tools.md`、`references/map-transport.md`、`references/journal-state.md`、`references/journal-display.md`、`references/script-safety.md`、`lookup/engine-syntax.md`、`lookup/engine-facts.md`、`lookup/numeric-facts.md`、`lookup/journal-ui.md`、`lookup/map-data.md`；脚本见 `references/tools.md` |
| `nesnd-player-writing/SKILL.md` | 改写为入口；§1 → `references/voice.md`；§2 → `references/fields.md`；§3 → `lookup/dynamic-loc.md` |
| `nesnd-player-writing/references/author-samples.md` | 移到 `lookup/author-samples.md` |

旧任务记录里出现的旧文件名（例如主 MOD `.scratch/denglai-route/handoff-prompt.md` 列出的 `syntax-and-routing.md`、`journal-text-contract.md`）按上表找新位置。主 MOD `docs/agents/prompt-kit.md` 引用的四个文件（debugging-and-updates、content-design、migration、verification）名称与位置不变。

## 2. 段落级去向

由拼装脚本按“旧文件第几节第几段”生成；段、项从 0 开始计。未写段号的表示整节搬入。

| 旧文件 § 段落 | 新位置 |
|---|---|
| pw:SKILL.md § （文首） | 第0段 → pw:SKILL.md |
| pw:SKILL.md § 1. 先定叙述者与事实 | 第0段 → pw:references/voice.md；第1段 → pw:references/voice.md；第2段 → pw:references/voice.md；第3段 → pw:references/voice.md；第4段 → pw:references/voice.md；第5段 → pw:references/voice.md |
| pw:SKILL.md § 2. 按玩家看到文字的时点落笔 | → pw:references/fields.md §按玩家看到文字的时点落笔 |
| pw:SKILL.md § 3. 主动使用 Victoria 3 的动态本地化 | 第0段 → pw:lookup/dynamic-loc.md §主动使用 Victoria 3 的动态本地化；第1段 → pw:lookup/dynamic-loc.md §主动使用 Victoria 3 的动态本地化 |
| pw:references/author-samples.md § 作者样本 | → pw:lookup/author-samples.md |
| pw:references/author-samples.md § 日志正文中的历史来路与政治判断 | → pw:lookup/author-samples.md §日志正文中的历史来路与政治判断 |
| pw:references/author-samples.md § 事件正文：具体的人和利益 | → pw:lookup/author-samples.md §事件正文：具体的人和利益 |
| pw:references/author-samples.md § 标题、引文、选项 | → pw:lookup/author-samples.md §标题、引文、选项 |
| pw:references/author-samples.md § 按钮、进度条、修正 | → pw:lookup/author-samples.md §按钮、进度条、修正 |
| pw:references/author-samples.md § 英文（作者原作） | → pw:lookup/author-samples.md §英文（作者原作） |
| pw:references/author-samples.md § 对照用的旧代理稿 | → pw:lookup/author-samples.md §对照用的旧代理稿 |
| pw:references/no-invention.md § 不编造、不八股：作者已否决的写法 | → pw:references/no-invention.md |
| pw:references/no-invention.md § 1. 不替机制编理由 | → pw:references/no-invention.md §1. 不替机制编理由 |
| pw:references/no-invention.md § 2. 不预设剧情事实 | → pw:references/no-invention.md §2. 不预设剧情事实 |
| pw:references/no-invention.md § 3. 称谓 | → pw:references/no-invention.md §3. 称谓 |
| pw:references/no-invention.md § 4. 1836 年的人和政治 | → pw:references/no-invention.md §4. 1836 年的人和政治 |
| pw:references/no-invention.md § 5. 官样八股 | → pw:references/no-invention.md §5. 官样八股 |
| pw:references/no-invention.md § 6. 按钮 | → pw:references/no-invention.md §6. 按钮 |
| v3:SKILL.md § 5. 向谁学 | 第0段 → lookup/paths.md §向谁学 |
| v3:references/character-book.json § （整个文件） | → lookup/canon/character-book.json |
| v3:references/compatibility.md § 东亚服装与 UI 兼容 | → references/compatibility.md §东亚服装与 UI 兼容 |
| v3:references/compatibility.md § East Asian Clothes: Redux | → references/compatibility.md §East Asian Clothes: Redux |
| v3:references/compatibility.md § UI | → references/compatibility.md §UI |
| v3:references/compatibility.md § 日志人物像与悬停 | → references/compatibility.md §日志人物像与悬停 |
| v3:references/content-design.md § 内容设计：形状、尺寸与层级 | → references/content-design.md |
| v3:references/content-design.md § 1. 先选形状 | → references/content-design.md §1. 先选形状 |
| v3:references/content-design.md § A. 里程碑链 | → references/content-design.md §A. 里程碑链 |
| v3:references/content-design.md § B. 计时压力 | → references/content-design.md §B. 计时压力 |
| v3:references/content-design.md § C. 主日志 + 子目标 | → references/content-design.md §C. 主日志 + 子目标 |
| v3:references/content-design.md § D. 原版的对立势力条 | → references/content-design.md §D. 原版的对立势力条 |
| v3:references/content-design.md § E. 作者的深系统（法兰西帝国链） | → references/content-design.md §E. 作者的深系统（法兰西帝国链） |
| v3:references/content-design.md § 2. 尺寸 | → references/content-design.md §2. 尺寸 |
| v3:references/content-design.md § 3. 每个节点的最低要求 | → references/content-design.md §3. 每个节点的最低要求 |
| v3:references/content-design.md § 4. 兜底：用一行，不用一个系统 | → references/content-design.md §4. 兜底：用一行，不用一个系统 |
| v3:references/content-design.md § 5. 改造现有链 | → references/content-design.md §5. 改造现有链 |
| v3:references/content-design.md § 6. 文件功效与替代入口 | → references/content-design.md §6. 文件功效与替代入口 |
| v3:references/content-design.md § 7. 规划 | → references/content-design.md §7. 规划 |
| v3:references/content-tree.md § 什么时候用 | 第0段第0-1项 → references/content-tree.md |
| v3:references/content-tree.md § 规则 | → references/content-tree.md |
| v3:references/debugging-and-updates.md § 修复问题与游戏更新 | → references/debugging-and-updates.md §修复问题与游戏更新 |
| v3:references/debugging-and-updates.md § 1. 修一个问题 | → references/debugging-and-updates.md §1. 修一个问题 |
| v3:references/debugging-and-updates.md § 新开局是验收基准 | → references/debugging-and-updates.md §新开局是验收基准 |
| v3:references/debugging-and-updates.md § 2. 游戏更新了 | → references/debugging-and-updates.md §2. 游戏更新了 |
| v3:references/economic-agency-and-crises.md § 经济压力、玩家选择与可恢复性 | → references/economic-agency-and-crises.md §经济压力、玩家选择与可恢复性 |
| v3:references/economic-agency-and-crises.md § 共同市场与产业专长（作者2026-11-02纠正） | → references/economic-agency-and-crises.md §共同市场与产业专长（作者2026-11-02纠正） |
| v3:references/economic-agency-and-crises.md § 先判问题性质，再决定是否改数值 | → references/economic-agency-and-crises.md §先判问题性质，再决定是否改数值 |
| v3:references/economic-agency-and-crises.md § 两极正例与反例 | → references/economic-agency-and-crises.md §两极正例与反例 |
| v3:references/economic-agency-and-crises.md § 每个实质问题先写路线蓝图 | → references/economic-agency-and-crises.md §每个实质问题先写路线蓝图 |
| v3:references/economic-agency-and-crises.md § 实验与封版判断 | → references/economic-agency-and-crises.md §实验与封版判断 |
| v3:references/economic-agency-and-crises.md § 本轮人口调整的25%边界 | → references/economic-agency-and-crises.md §本轮人口调整的25%边界 |
| v3:references/faction-model.md § 国家势力与玩家体验：设计前填写 | → references/regional-history-and-survival.md |
| v3:references/journal-text-contract.md § 1.15.0 Ivan-Chai 的日志退出、结案页与条（Steam 26453692） | → lookup/journal-ui.md §1. 1.15.0 Ivan-Chai 的日志退出、结案页与条（Steam 26453692） |
| v3:references/journal-text-contract.md § 2026-11-05实测纠正：公开条件、条内文本与配图 | 第4段 → references/journal-state.md §1. 唯一的状态与写入者；第0段第5项 → references/journal-state.md §常驻议程；第5段 → references/journal-state.md §3. 全局日志、节奏与按钮组；第6段第1-3项 → references/journal-state.md §3. 全局日志、节奏与按钮组；第0段第0项 → references/journal-display.md §公开条件逐层展开；第0段第1-4项 → lookup/journal-ui.md §2. 条面、配图与字段分工；第1段 → lookup/journal-ui.md §2. 条面、配图与字段分工；第2段 → lookup/journal-ui.md §2. 条面、配图与字段分工；第3段 → lookup/journal-ui.md §2. 条面、配图与字段分工；第9段 → lookup/journal-ui.md §2. 条面、配图与字段分工；第6段第0项 → lookup/journal-ui.md §2. 条面、配图与字段分工；第7段 → pw:references/no-invention.md §7. 开发说明不进正文 |
| v3:references/journal-text-contract.md § 概念、实际状态与随机姓名 | 第4段 → lookup/engine-facts.md §人物、IG 与文化；第0段 → lookup/journal-ui.md §3. 概念与数据上下文；第1段 → lookup/journal-ui.md §3. 概念与数据上下文；第2段 → lookup/journal-ui.md §3. 概念与数据上下文；第3段 → lookup/journal-ui.md §3. 概念与数据上下文 |
| v3:references/journal-text-contract.md § 改革子日志与具名目标（2026-11-01） | → references/journal-state.md |
| v3:references/journal-text-contract.md § 国家日志状态、预报和条的反例（2026-11-05） | → lookup/journal-ui.md |
| v3:references/journal-text-contract.md § 原生进度条与初始化恢复 | → references/journal-state.md |
| v3:references/journal-text-contract.md § 1.15 可见结局与自动激活（2026-11-06） | 第4段 → references/journal-display.md §1. 原生条件优先与状态节制（2026-11-02）；第5段 → references/journal-display.md §1. 原生条件优先与状态节制（2026-11-02）；第0段 → references/journal-display.md §4. 1.15 可见结局与自动激活（2026-11-06）；第1段 → references/journal-display.md §4. 1.15 可见结局与自动激活（2026-11-06）；第2段 → references/journal-display.md §4. 1.15 可见结局与自动激活（2026-11-06）；第3段 → references/journal-display.md §4. 1.15 可见结局与自动激活（2026-11-06） |
| v3:references/journal-text-contract.md § 非开局入口、终局回调与镜像条 | → references/journal-state.md |
| v3:references/journal-text-contract.md § 阶段可进入与永久结束分开 | → references/journal-state.md |
| v3:references/journal-text-contract.md § 按钮预览与周期占比：2026-11-03实际反馈 | → references/journal-display.md §2. 按钮预览与周期占比：2026-11-03实际反馈 |
| v3:references/journal-text-contract.md § 阶段切换与数值同步：印度反例 | → references/journal-state.md |
| v3:references/journal-text-contract.md § 法律影响按法组呈现 | → references/journal-display.md §3. 法律影响按法组呈现 |
| v3:references/journal-text-contract.md § 绝对条件数与切换重点（1851测试档反例，2026-11-04） | → references/journal-state.md |
| v3:references/map-economy-design.md § 地区尺度、设定与经济共同设计 | → references/map-economy-design.md |
| v3:references/map-economy-design.md § 图像与数据入口 | → lookup/map-data.md |
| v3:references/map-economy-design.md § 避免错误归因 | → references/map-economy-design.md §避免错误归因 |
| v3:references/map-economy-design.md § 迁移合同 | → references/map-economy-design.md §迁移合同 |
| v3:references/map-economy-design.md § 建筑总等级与投资股份分两步取整 | → references/map-economy-design.md §建筑总等级与投资股份分两步取整 |
| v3:references/map-economy-design.md § 唯一建筑也属于迁移图 | → references/map-economy-design.md §唯一建筑也属于迁移图 |
| v3:references/map-economy-design.md § 2026-10-31 实测补充：locator 不是交通 hub | 第4段 → references/map-economy-design.md §候选与合入；第5段 → references/map-economy-design.md §候选与合入；第1段 → lookup/map-data.md §交通网与港口的编号〔1.13.11 实文件；换版本须重新核对〕；第3段 → lookup/map-data.md §原生编辑器与军队界面操作（1.13.11 实测）；第0段 → references/map-transport.md；第2段 → references/map-transport.md |
| v3:references/map-economy-design.md § 有格式证据的 splnet 备选工具 | 第2段 → lookup/map-data.md §原生编辑器与军队界面操作（1.13.11 实测）；第0段 → references/map-transport.md；第1段 → references/map-transport.md |
| v3:references/map-economy-design.md § 地方就业证据 | → references/map-economy-design.md §地方就业证据 |
| v3:references/map-economy-design.md § 2026-10-31 原生海港断链：陆地port与海面harbor不同 | 第1段 → lookup/map-data.md §交通网与港口的编号〔1.13.11 实文件；换版本须重新核对〕；第0段 → references/map-transport.md；第2段 → references/map-transport.md；第3段 → references/map-transport.md；第4段 → references/map-transport.md |
| v3:references/map-economy-design.md § 已知负例驱动的导出门禁 | → references/map-transport.md §已知负例驱动的导出门禁 |
| v3:references/map-economy-design.md § 海域版本迁移：编号有效不等于地理正确 | → references/map-transport.md §海域版本迁移：编号有效不等于地理正确 |
| v3:references/migration.md § 保留设计意图的版本迁移 | → references/migration.md §保留设计意图的版本迁移 |
| v3:references/migration.md § 三份数据，而不是新旧文件覆盖 | → references/migration.md §三份数据，而不是新旧文件覆盖 |
| v3:references/migration.md § 地图的持久身份是 province 集合 | → references/migration.md §地图的持久身份是 province 集合 |
| v3:references/migration.md § 机制变化 | → references/migration.md §机制变化 |
| v3:references/migration.md § 每次迁移产物 | → references/migration.md §每次迁移产物 |
| v3:references/migration.md § 1.15 保留旧文化的引用检查 | → references/migration.md §1.15 保留旧文化的引用检查 |
| v3:references/narrative-context.md § 设定、角色与文风入口 | → lookup/canon/narrative-context.md |
| v3:references/narrative-context.md § 读取顺序 | → lookup/canon/narrative-context.md §读取顺序 |
| v3:references/narrative-context.md § 时代与证据 | → lookup/canon/narrative-context.md §时代与证据 |
| v3:references/narrative-context.md § 事件文本预设 | 第1段 → pw:references/voice.md §2. 语体；第0段 → pw:references/fields.md §按玩家看到文字的时点落笔 |
| v3:references/narrative-context.md § 图片预设 | → lookup/canon/narrative-context.md §图片预设 |
| v3:references/narrative-context.md § 日本资料专题 | → lookup/canon/narrative-context.md §日本资料专题 |
| v3:references/narrative-context.md § 日本修订2与印度专题 | → lookup/canon/narrative-context.md §日本修订2与印度专题 |
| v3:references/native-treaty-aid.md § 1.13.11 原生条约、供给和援助 | → lookup/native-treaty-aid.md §原生条约、供给和援助（1.13.11 起） |
| v3:references/native-treaty-aid.md § 预检和创建的商品字段不同：run150709真引擎反例 | → lookup/native-treaty-aid.md §预检和创建的商品字段不同：run150709真引擎反例 |
| v3:references/north-south-institutions.md § 南北朝制度与叙事主体 | → lookup/canon/north-south-institutions.md |
| v3:references/north-south-institutions.md § 北朝牧氏政权 | → lookup/canon/north-south-institutions.md §北朝牧氏政权 |
| v3:references/north-south-institutions.md § 南朝明、吴 | → lookup/canon/north-south-institutions.md §南朝明、吴 |
| v3:references/north-south-institutions.md § 英文用名与权力边界 | → lookup/canon/north-south-institutions.md §英文用名与权力边界 |
| v3:references/north-south-institutions.md § 行动主体与事件范围 | → lookup/canon/north-south-institutions.md §行动主体与事件范围 |
| v3:references/numeric-scale-contract.md § 数值量纲与成本：改数值前必读 | 第0段 → references/numeric-scale-contract.md；第2段 → references/numeric-scale-contract.md；第1段 → lookup/engine-facts.md §按钮、事件与 AI 权重 |
| v3:references/numeric-scale-contract.md § 本机1.13.11已核实例 | → lookup/numeric-facts.md §本机1.13.11已核实例〔1.15.0 未复核〕 |
| v3:references/numeric-scale-contract.md § 本机陆军军需数量与舰船维持 | → lookup/numeric-facts.md §本机陆军军需数量与舰船维持〔1.13.11；1.15.0 已核编制仍用 `ship_type:`，其余未复核〕 |
| v3:references/numeric-scale-contract.md § 有界算术与单向生活变化（1.13.11，西秦实证） | → lookup/numeric-facts.md |
| v3:references/paths.md § 绝对路径和读写范围 | → lookup/paths.md |
| v3:references/paths.md § 会话需要连接哪些目录 | → lookup/paths.md §会话需要连接哪些目录 |
| v3:references/paths.md § 参考来源，不是可修改的第二工作区 | → lookup/paths.md §参考来源，不是可修改的第二工作区 |
| v3:references/paths.md § 当前 MOD 内该去哪里 | → lookup/paths.md §当前 MOD 内该去哪里 |
| v3:references/political-design-and-difficulty.md § 政治目标、党派与难度 | → references/political-design-and-difficulty.md |
| v3:references/political-design-and-difficulty.md § 玩家可控制的目标 | → references/political-design-and-difficulty.md §玩家可控制的目标 |
| v3:references/political-design-and-difficulty.md § 党派定义与任务条件分层 | 第0段 → references/political-design-and-difficulty.md；第2段 → references/political-design-and-difficulty.md；第1段 → lookup/engine-facts.md §政治 |
| v3:references/political-design-and-difficulty.md § 人物、运动与人口的传播链 | → references/political-design-and-difficulty.md §人物、运动与人口的传播链 |
| v3:references/recipes.md § 函数库与具体实现路线 | 第0段 → lookup/engine-syntax.md §语法、作用域与官方文档 |
| v3:references/recipes.md § 事件链与分支 | → references/content-design.md §事件链与分支的登记 |
| v3:references/recipes.md § 带进度条的日志 | → references/journal-state.md |
| v3:references/recipes.md § 历史归属、人口、建筑 | 第2段 → references/map-economy-design.md §改归属与新地区的同步清单；第0段 → lookup/map-data.md §历史归属、人口、建筑的形状；第1段 → lookup/map-data.md §历史归属、人口、建筑的形状 |
| v3:references/recipes.md § 新地区与地块迁移 | → references/map-economy-design.md §改归属与新地区的同步清单 |
| v3:references/recipes.md § 独特 DNA 人物 | → lookup/engine-facts.md §独特 DNA 人物〔1.13.11，1.15.0 未复核〕 |
| v3:references/recipes.md § 需求可行性 | 第1段 → references/content-design.md §事件链与分支的登记 |
| v3:references/recipes.md § 1.13.11 已核实的说明差异 | 第0段 → lookup/engine-facts.md §外交、战争与条约；第3段 → lookup/engine-facts.md §外交、战争与条约；第1段 → lookup/engine-facts.md §按钮、事件与 AI 权重；第2段 → lookup/engine-facts.md §军事单位；第4段 → lookup/engine-facts.md §改革指标的作用域〔1.13.11，1.15.0 未复核〕 |
| v3:references/recipes.md § Country 标签的嵌套动态悬停（run143454 实际失败） | → lookup/journal-ui.md |
| v3:references/recipes.md § 事件AI权重依据 | 第0段 → lookup/engine-facts.md §按钮、事件与 AI 权重 |
| v3:references/regional-history-and-survival.md § 人物、市场与地区路线 | → references/regional-history-and-survival.md §人物、市场、地区路线与国家势力 |
| v3:references/regional-history-and-survival.md § 事实分层决定入口 | → references/regional-history-and-survival.md §事实分层决定入口 |
| v3:references/regional-history-and-survival.md § 人物是社会过程的参与者 | → references/regional-history-and-survival.md §人物是社会过程的参与者 |
| v3:references/regional-history-and-survival.md § 市场与政治自主分开 | → references/regional-history-and-survival.md §市场与政治自主分开 |
| v3:references/regional-history-and-survival.md § 运动字段的实际方向 | → references/regional-history-and-survival.md §运动字段的实际方向 |
| v3:references/regional-history-and-survival.md § 文字也要过分支测试 | → references/regional-history-and-survival.md §文字也要过分支测试 |
| v3:references/skill-maintenance.md § 维护本技能 | → references/skill-maintenance.md §维护本技能 |
| v3:references/skill-maintenance.md § 什么可以写进技能 | → references/skill-maintenance.md §什么可以写进技能 |
| v3:references/skill-maintenance.md § 篇幅 | → references/skill-maintenance.md §篇幅 |
| v3:references/skill-maintenance.md § 同步 | → references/skill-maintenance.md §同步 |
| v3:references/subsistence-transition.md § 自给经济、资格与转型：本机1.13.11 | → references/subsistence-transition.md |
| v3:references/subsistence-transition.md § 文件链 | → references/subsistence-transition.md §文件链 |
| v3:references/subsistence-transition.md § 判断方法 | → references/subsistence-transition.md §判断方法 |
| v3:references/syntax-and-routing.md § Victoria 3 专属约束 | → lookup/engine-syntax.md |
| v3:references/syntax-and-routing.md § 引用安全：按钮、延迟回复与预览 | 第0段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第1段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第2段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第3段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第4段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第5段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第7段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览；第8段 → references/script-safety.md §1. 引用安全：按钮、延迟回复与预览 |
| v3:references/syntax-and-routing.md § 必读文档与当前实现配对 | → lookup/engine-syntax.md |
| v3:references/syntax-and-routing.md § 覆盖与编码 | → references/script-safety.md §2. 覆盖原版与编码 |
| v3:references/syntax-and-routing.md § 战争回调与一次全球日志（1.13.11） | 第0段第2项 → references/journal-state.md §3. 全局日志、节奏与按钮组；第0段第1项 → references/script-safety.md §3. 事件、回调与时序；第2段 → references/script-safety.md §3. 事件、回调与时序；第0段第3项 → references/map-economy-design.md §改归属与新地区的同步清单；第0段第0项 → lookup/engine-facts.md §外交、战争与条约；第1段 → lookup/engine-facts.md §外交、战争与条约 |
| v3:references/syntax-and-routing.md § 1.13.11 本机接口与创建回调 | 第0段 → lookup/engine-facts.md §人物、IG 与文化；第1段 → lookup/engine-facts.md §人物、IG 与文化 |
| v3:references/syntax-and-routing.md § 人物、日志局部scope及重复字段 | → lookup/engine-facts.md §按钮、事件与 AI 权重 |
| v3:references/syntax-and-routing.md § 宗室延续与无所属角色 | → references/script-safety.md |
| v3:references/syntax-and-routing.md § 印度实施的接口与案件隔离（1.13.11） | 第0段第1-2项 → references/script-safety.md §案件隔离与州转属（印度实施，1.13.11）；第1段 → references/script-safety.md §案件隔离与州转属（印度实施，1.13.11）；第0段第0项 → lookup/engine-facts.md §日志与国家对象〔1.13.11，1.15.0 未复核〕；第0段第3项 → lookup/engine-facts.md §日志与国家对象〔1.13.11，1.15.0 未复核〕 |
| v3:references/syntax-and-routing.md § 20261103 原生日志补证 | 第1段 → references/script-safety.md §宗室延续与无所属角色；第0段第1项 → lookup/engine-facts.md §人物、IG 与文化；第0段第2项 → lookup/engine-facts.md §日志与国家对象〔1.13.11，1.15.0 未复核〕 |
| v3:references/syntax-and-routing.md § 定点停用原版故障链 | → references/script-safety.md |
| v3:references/syntax-and-routing.md § 战后结算与寄居人物（2026-11-04） | → references/script-safety.md |
| v3:references/syntax-and-routing.md § 文化键与数量（2026-11-05） | 第2段 → references/script-safety.md §外交博弈与延迟答复的求值；第0段 → references/script-safety.md；第1段 → references/script-safety.md |
| v3:references/vanilla-overrides.md § 主 MOD 修改的原版文件 | → lookup/vanilla-overrides.md |
| v3:references/vanilla-overrides.md § 内容有改动（185 个） | → lookup/vanilla-overrides.md §内容有改动（185 个） |
| v3:references/vanilla-overrides.md § 仅编码标记或换行有差异（2 个） | → lookup/vanilla-overrides.md §仅编码标记或换行有差异（2 个） |
| v3:references/vanilla-overrides.md § 与原版逐字节相同的同路径副本（3 个） | → lookup/vanilla-overrides.md §与原版逐字节相同的同路径副本（3 个） |
| v3:references/verification.md § 检查、日志、备份与交付 | → references/verification.md §检查、日志、备份与交付 |
| v3:references/verification.md § 1. 检查顺序 | → references/verification.md §1. 检查顺序 |
| v3:references/verification.md § 2. 读日志 | → references/verification.md §2. 读日志 |
| v3:references/verification.md § 3. 交付时怎么写 | → references/verification.md §3. 交付时怎么写 |
| v3:references/verification.md § 4. 备份与版本 | → references/verification.md §4. 备份与版本 |
| v3:references/worldbook.json § （整个文件） | → lookup/canon/worldbook.json |
旧 `SKILL.md` 中手工改写的部分：§1 开工前 → 新 §1；§2 硬边界 → 新 §2（增加“新开局是验收基准”“产物写 D 盘”两条，静态≠实机说明改为指向 verification.md §3）；§3 默认工作方式 → 新 §3；§4 按任务找资料 → 新 §4 路由表与 §5 主题表；§6 交付 → `references/verification.md` §3 与新 §6；§7 维护 → 新 §6 与 `references/skill-maintenance.md`。

## 3. 删除或改写的段落

检查脚本找不到原文的段落逐条列在这里（`u:` 后为该段规范化文本的 SHA-1 前 8 位）。

| ID | 旧位置 | 处理 | 理由 / 现在在哪里 |
|---|---|---|---|
| u:08a581b3 | content-tree.md 开头 | 改写 | 现行工具换成 V3-content-tree；“给定根……覆盖率报告”一句原样保留，旧工具位置改写为“前身”一句 |
| u:8f475947 | content-tree.md §什么时候用 第3项 | 改写 | 重建索引改为 v3tree 的 `run.py index`（新 content-tree.md 开头） |
| u:440bf5f9 | journal-text-contract.md 按钮 AI 示例段 | 删除 | 重复；同一事实在 `lookup/engine-facts.md` §按钮、事件与 AI 权重 |
| u:a5eacebf | recipes.md §需求可行性 第1段 | 改写 | 条约事实与 `lookup/native-treaty-aid.md` 表格重复；保留为 content-design.md §7 的一句指引 |
| u:3ebce673 | recipes.md §事件AI权重依据 第2段 | 删除 | 重复；`good`/`goods` 全文在 `lookup/native-treaty-aid.md` 末节 |
| u:0ce5a782 | recipes.md §事件AI权重依据 第3段 | 删除 | 重复；港口须补 harbor 与海路在 `references/map-transport.md` §海港断链 |
| u:f77528ce | skill-maintenance.md §篇幅 | 改写 | SKILL.md 上限由约 6 KB 放宽到约 8 KB，因为加入了路由表与主题表 |
| u:46bdb5fb | subsistence-transition.md 末段 | 改写 | 原文指向已不存在的 `system-design-and-plans`，改指 verification.md；其余原文不变 |
| u:f1d37523 | syntax-and-routing.md §引用安全 `good`/`goods` 段 | 改写 | 例子与 native-treaty-aid 重复；保留通则一句（script-safety.md §1） |
| u:fe9f90d0 | syntax-and-routing.md §20261103 第1项 | 删除 | 重复；关系比较写法在 `lookup/engine-facts.md` §外交（取自 recipes，1.15.0 已核） |
| u:48ff4b0a | SKILL.md 开头 | 改写 | 新入口说明，意思不变并加路由提示 |
| u:e3eac65e | SKILL.md §3 第4条 | 改写 | 同义，链接位置调整 |
| u:d59ddbb4 | SKILL.md §3 第5条 | 改写 | script_docs 的位置细节归 verification.md §1，这里只留做法 |
| u:407c4a5a、u:16d41236、u:c3c46ecd、u:26ddca27、u:b4a3259a、u:0fd918af、u:8b695762、u:6ac93660、u:eaa56809、u:2f9035ef、u:f4b5ae91、u:d8ffb7d7、u:8537268c、u:6f91a805 | SKILL.md §4 旧路由表各行 | 取代 | 由新 SKILL.md §4 路由表（按任务类型）与 §5 主题表取代，原有每个目标文件都仍在表中 |
| u:0de6ca1d | SKILL.md §4 末句（1.13.11 提示） | 改写 | 新 SKILL.md §5 末句；engine-facts、numeric-facts 逐条标版本状态 |
| u:7fd481aa | SKILL.md §5 退役文字素材 | 删除 | 重复；在 nesnd-player-writing SKILL.md 路由表与 `resources/unused_localisations/README.md` |
| u:91fa3075 | SKILL.md §6 交付 | 删除 | 重复；四件事在 verification.md §3，“然后更新 STATUS.md”在新 SKILL.md §6 |
| u:ac167ed1 | SKILL.md §7 维护 | 删除 | 重复；同步规则在 skill-maintenance.md §同步 |
| u:5eeca787 | nesnd-player-writing SKILL.md §3 末句 | 改写 | 并入新 SKILL.md 路由表“找旧素材”一行 |
| u:7935d76e | references/character-design.md §二“用于” | 改写（2026-11-14） | 删去工坊 MOD 列宁一例（作者决定技能只引原版和 NESND），补“煽动者后来当君主接第八节”；现在 character-office.md §二 |
| u:7b7b474f | references/character-design.md §五“用于” | 改写（2026-11-14） | 删去工坊 MOD 银行经理一例，改为周学熙一句；现在 character-office.md §五 |
| u:30567507 | references/character-design.md §六“用于” | 改写（2026-11-14） | 工坊 MOD 居里一例换成原版沙皇宠臣议程（08_tsarpoints.txt:2678）；现在 character-office.md §六 |
| u:25ec218f | references/character-design.md 检查清单末条 | 改写（2026-11-14） | 命令出处由研究目录改为 tools.md（person 命令已写入），补变量列表节点的核对提示 |
| u:1291c06a | references/regional-history-and-survival.md §人物 第一段 | 改写（2026-11-14） | “人物死亡后组织延续”一句与 character-design.md 重复，改为一句指向；“唯一身份跨国复用”同理删去，规则在 character-office.md §四 |

## 4. 顺带修正的问题

- `journal-text-contract.md` 的标题错层：“原生条件优先与状态节制（2026-11-02）”标题下紧跟“1.15 可见结局”小节，原属前者的六条反而落在后者之下。现在分别是 journal-display.md §1 与 §4。
- 重复规则合并：按钮与事件 `ai_chance` 的两种形状原在 4 处（recipes、numeric、journal-text-contract、syntax）；`relations(scope:…)` 原在 2 处；`good`/`goods` 原在 3 处。现在各只在一处写全。
- `subsistence-transition.md` 的失效引用（`system-design-and-plans`）已改。
- 1.13.11 条目在 1.15.0 的复核（2026-11-11，只读 GAME 与 script_docs 导出）：

| 条目 | 结果 |
|---|---|
| 按钮 `ai_chance` 用 script value | 成立；`07_meiji_buttons.txt:87/211/295` 未变，殖民管理按钮的值现为 100 |
| `"relations(scope:target_country)"` | 成立，`01_event_catalysts.txt:24、30` |
| `annex_as_civil_war = yes` | 成立；1.15 另有同名效果条目，`create_diplomatic_play` 说明仍写旧名 |
| 条约预检 `good`、创建 `goods` | 成立 |
| `ig_clout`/`ig_approval`、`building_barrack`、`has_role`/`has_role_of_type`、`ideology_jingoist_leader` | 成立 |
| 海军编制用 `ship_type:` | 成立 |
| `on_enemy_capitulated_notification` | 存在，行号由 4217 变为 2297 |
| `concept_unemployed`（非 `concept_unemployment`）、`building_textile_mill` | 成立 |
| `should_be_pinned_by_default_*` 两项并用 | 成立，行号变为 695–696 |
| `MIN_RAISE_TO_HIRE = 0.10`、自给建筑每级 5000 农民 | 成立 |
| 事件 `DEFAULT_MONTHS_VALID` | 仍按月计；1.15 默认值为 −1（不过期） |
| 无 `customs_union` 条约条款；`economic_dependence`、`can_leave_power_bloc` 仍在 | 成立 |
| 事件 option `ai_chance` 的 `modifier` 全用 `add` | 未能复核（需重新计数），engine-facts 中保留“未复核” |

其余标 1.13.11 的条目在 engine-facts / numeric-facts 中标为“1.15.0 未复核”。

## 5. 防丢失检查结果


```
{"kept": 661, "edited": 7, "documented": 32, "missing": 0}
```

2026-11-11 运行。kept 为原样保留，edited 为小改后保留，documented 为第 3 节所列。

2026-11-14 拆分人物设计参考（备份 `WORK/backups/pre-change-character-design-split-20261114T182616Z/`）。

```
{"kept": 1016, "edited": 3, "documented": 5, "missing": 0}
```
