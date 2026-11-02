# 设定、角色与文风入口

这里是按需加载的世界书/角色书/写作预设，服务于本 MOD；不把整套小说无条件塞进上下文，也不把一次拟稿永久当成正史。

玩家文本的完整写作与审查流程由独立技能 [nesnd-player-writing](../../nesnd-player-writing/SKILL.md)维护；本页只负责设定与资料路由。涉及条件展示同时读 [日志契约](journal-text-contract.md)。

## 读取顺序

1. 用户最新明确设定与本次适用年代。
   涉及南北朝制度、称谓、议会权限或改革终局，先读[南北朝制度与叙事主体](north-south-institutions.md)，其中记录作者2026-11-02的明确纠正；旧资料不能覆盖这些纠正。
2. `worldbook.json` 中匹配关键词、年代与阵营的条目。沿 sources 回读来源段落/幻灯片；条目不是原文替代品。
3. `character-book.json` 中人物的目标、筹码、限制、关系及生死/身份条件。别名和模板需核查，不靠现实同名人物补齐生平。
4. **游戏文案首先读作者原有 `localization/simp_chinese/replace/`，按事件正文、引文、选项、标题、日志正文、按钮、进度条、modifier 分别对读。** 用户明确：设定资料多为简化文案。用修改前备份 `WORK/backups/pre-update-20261030T233944Z/mod` 区分作者原文与代理新增，后者不能冒充风格依据。
5. 读对应 events/JE/buttons/progress bars，确认触发条件、说话者及有效 scope。阅读 `WORK/research/20261031/replace-style-review/逐类对照.md` 与 [作者语体实测](author-prose-profile.md)，更新指南后重读指南再改写。
6. 用 [文本呈现层](journal-text-contract.md) 决定 UI 字段。任务是人物列传或需要补充场景时再使用 `beiming-biography` 的文体；世界书、人物卡负责事实和立场，不自动规定事件句法。

原资料只读目录：`D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世`。重点：`北明ppet.pptx`、`朱班博传（上）.docx`、`朱班博传（中）.docx`、`北明人物列传.docx`；补充《骆军始末》《海军人物》及时间线。缓存 `WORK/research/20261031` 的 JSON 保留原文定位与 SHA；使用前核验 SHA，变更后重新提取。提取脚本：`beiming-biography/scripts/extract_ooxml.py`。

## 时代与证据

- 1819—1821 南征地图是背景，不是覆盖 1836 国界的指令。图中文字中的经略军、共和派与文献异名/日期需要并列核对。
- PPT 内有 1805/1810 革命起点等异文，人物传还有不同称帝日期。不能仅按文件时间或形式裁决。后续危机尽量用条件与相对时间，不以有争议的日月强制触发。
- 《海军人物》多数角色生于 19 世纪末；1836 不生成他们，不倒置航母/潜艇/一战经历。官制沿革也要核对适用年代。
- 《骆军始末》是早期土地、族群与组织成长的因果参考；1836 不无条件复活 15 世纪人物/组织。
- 证据类型：author_explicit、text_attested、inference、gameplay_proposal、unresolved_variant。批准实施分支不等于它是小说唯一未来；只有作者明确确认才升级正史。

## 事件文本预设

标题点明具体冲突或意象。描述写谁提出什么、凭什么能做到、谁承担代价。风味段可用有对象的短对白；人物判断与旁白分开。选项写实际行动，效果提示告知成本、时长、条件与风险，不在风味段堆变量。

自然现代中文为主，保留编年、制度、利益与因果；避免过密文言、空洞宣言和人人金句。原文讽刺、角色辱称不能自动升格为全知旁白。吴朝的建制能力与战争暴行可以同时呈现。

## 图片预设

生成前记录年代、地点、阵营、人物当时年龄/身份、服装、建筑/舰船/武器技术、画面动作与构图及来源条目。未确认细节标为美术演绎；不搬运 EACR 素材。新图遵循 imagegen 技能，再查资源引用与实际显示。生成肖像不等于游戏 DNA，DNA 与 portrait modifier 单独实现测试。

## 日本资料专题

研究日本丰臣/德川/天皇、三国、九州或朝鲜时，先读WORK/reports/japan-research-20261102/{native-japan,current-mod-japan,japan-canon}.md。PPT27是1847–1852未来线（三日本政权＋吴直辖），1936/1950地图更晚；最新用户三局面目标不等于唯一正史。当前游戏林汉涵等名优先，异文保留研究说明。原版锁国九州入口、幕府法退出、JAP/DLC硬绑和大名/武士global标记需逐项适配，不能整套移给三个新国家。开发提案在WORK/plans/two-empires/20261102-japan-development-design.md，未实施部分明确分列。

## 日本修订2与印度专题

涉及日本林摄政/文化同化/三国产业时，先读最新日本方案第九节和WORK/reports/japan-research-20261102/revision-2：作者已明确天皇政权JIM就是林摄政，旧JAP任命为待改实现，不能再当未决设定。数值和主流修改是否上线以任务19与交付记录为准。
涉及莫卧儿/明属印度/法国援助/种姓时，读WORK/reports/india-research-20261102的native-india.md、current-mod-india.md、india-canon.md。王朝历史出身、国家主文化、宗教和种姓适用群体分别核实；旧.bak不是活动定义，不同名history不会覆盖原版。海军原稿的人物年代与1836分开。实施方案在WORK/plans/two-empires/20261102-india-development-design.md；具体法援同时读native-treaty-aid.md。

日本／印度宗属、土邦起义或法国政体分支实施前，读取WORK/plans/two-empires/20261102-japan-development-design.md第十节、20261102-india-development-design.md第十至十三节及20261102-japan-india-lifecycle.md。修订报告在WORK/reports/japan-india-plan-revision-20261102/。它们是设计与源码证据，尚非新玩法；现行政体、当朝身份、现实宗属与承诺分开，不能按显示国名套关系。
