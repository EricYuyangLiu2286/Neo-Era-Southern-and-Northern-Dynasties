# 印度子日志来源核查：本批只读诊断

2026-11-03；`SOURCE_DIAGNOSIS / ENGINE_NOT_RUN`。按 NESND 与 Matt research 核本机1.13.11/build24799966。只读主MOD与本体，不启动游戏、不解析完整存档、不改玩法脚本。研究对象是主MOD，不是 root 正在编写的 candidate。旧484项静态检查不作为本次界面成功证据。

## 结论与证据等级

**现有设计确实有两个子JE，按钮也确实显式调用添加工场子JE；不是只写了完成说明而没有实现子任务。** 正常 country 执行链在 `priority=2` 后即可添加 `nesnd_india_industry`，不要求先造完工厂、铁路或军队。没有发现“父JE immediate 在父注册前添加子JE”的旧式自锁：父JE根本没有 immediate；refresh先尝试补父，再判断子；子资格也未正向依赖自身 `has_journal_entry`。[M1–M4]

已能由源码确定的缺陷/不足：

1. 父JE `complete` 把 schools_done 和 industry_done 两个独立事实包进一个 `custom_tooltip`，因此玩家只得到“完成学校与官署、工场与军队”一个真假项。内部没有引用子JE的实际建设条件，父面板不会自行显示这些条件。[M1:27][M8:48]
2. 两个子JE不默认钉选，只有父JE默认钉选；原版明治的经济/军队子JE分别默认钉选。日志并不存在由“父子命名”自动产生的嵌套UI；这里三个JE是历史内容组内并列项。因此“父条旁没出现子项”可能是显示/钉选问题，**不能单凭该现象证明添加效果未执行**。[M1:1–32][G2:744–848]
3. `available` 同时承担首次加入、显示、完成资格和永久invalid；其中包含“当前优先项等于本项”。切换重点后旧项立即满足 `invalid`，静默消失，实际上是销毁并等将来重建，不是文案所说的“另一项暂停”。country月份虽保留，JE对象/可见建设清单不保留。[M1:3–20][M3:37–38][M8:38]
4. 主JE状态始终是“朝廷正在筹办学校与工场”，不显示当前priority、未选择、另一项暂停或某项已完成；按钮也只显示一条改革重点说明，玩家无法从主面板辨别是否成功选择。[M1:31][M8:5、38]
5. 工业ready在进度条上下文还有独立scope风险：四个市场替代分支使用 `country_has_local_shortage=root`；普通JE/country tick中的root是country，但progress-bar经 `owner={...}` 调用ready时root仍是JE。原版同类bar使用 `root.owner` 引用国家，而 shortage 参数要求country。它影响进度条预览/计分一致性，**不是首次添加缺失的已证原因**。[M3:16–19][M7:4–6][G7][G8]

“点击后在完整活动日志列表仍完全找不到工场JE”的唯一运行根因尚未由本次只读证据锁定。不能把第三项的切换生命周期缺陷直接冒充第一次点击未添加的原因。需要最小状态摘录：MUG的priority、done、months、以及工场JE active/inactive/finished状态；无需读全存档AST。下文给出能同时收口可见性、暂停与旧档恢复的最小方案。

## 当前完整调用链

| 步骤 | 当前源码与scope | 行为/边界 |
|---|---|---|
| 国家资格 | `nesnd_india_country`：alive、非decentralized、在印度南/北战略区至少一个有人州。`empire`：再满足MUG/BHT/DRA或imperial_line变量。 | 战争、破产、政党组合、政府IG不影响玩家改革资格。MUG具有印度州即可是empire。[M3:1–6] |
| 父JE | `nesnd_india_reform_live = empire && !reform_done`；inactive与possible相同。历史内容group的context=country。 | 自动入口与refresh显式入口并存；父JE默认钉选。[M1:23–34][G1][G9] |
| 按钮可见 | reform_live、industrial未done、当前priority不等于2。 | 重复选择同一项会隐藏按钮。[M2:7–8] |
| 按钮可用 | academia；无priority_cooldown。 | bureaucracy≥0/default/破产只出现在AI安全权重，不能给玩家补上。[M2:9–10] |
| 按钮执行 | country：hidden_effect内再次核reform_live、无冷却、industry未done；写priority_cooldown=12个月；写priority=2；调用 `nesnd_india_refresh`。 | 实际执行没有再次核academia，但不妨碍正常已可点击路径；无效果日志不等于失败。[M2:11] |
| refresh | country：initialize→补父JE→补schools→补industry→其他印度JE和外交维护。 | `industry_available && !has_journal_entry(industry)` 即 `add_journal_entry={type=nesnd_india_industry}`。[M4:19–44] |
| 子JE资格 | reform_live、industry未done、有priority且safe script_value=2。 | 与建设完成条件分开；不要求学校先完成。学校仅是AI优先顺序。[M3:37–38][M2:10] |
| 子JE immediate | country：months不存在才置0；sync保存当前country，再跳`je:nesnd_india_industry`设条。 | 已累计月份不重置。同步的hasJE若在immediate注册尚未完成时未命中，后续tick仍会再同步；这最多影响初始条，不能据此证明JE不出现。[M1:15][M4:52–56] |
| 月度计分 | country：available为真；ready时months+1；clamp0–12；绝对同步bar。 | 条自身先做monthly+1，JE随后写country值并set_bar_progress；不是再读增长后的bar叠加两次。原版说明条更新先于JE pulse。[M4:9–15][M7][G6] |
| 完成 | available、ready、累计months≥12；设置industry_done，给120月industrial_service。 | 是累计达标月份，条件暂时掉落时不清零；还需要完成当刻ready。[M1:17–18] |
| 切换 | priority改1后industry_available=false。 | 下个invalid检查静默移除industry；无on_invalid。months仍存在。[M1:19][M2:5] |

safe script values `nesnd_india_priority_value / *_months_value` 在变量未初始化时返回0，不能把“未选择”误判为industry。没有与这些JE同名的第二定义/REPLACE覆盖。[M6:12–14]

## 实际玩家建设条件应在哪显示

这些条件现存于 `nesnd_india_*_ready`，子JE complete直接引用它们，应保留原生逐项勾叉；不搬入一个新大tooltip，也不擅自更改阈值。[M3:7–24]

| 学校与官署 | 工场与军队 |
|---|---|
| 已研究academia | 煤矿全国≥15级，**或**市场煤价加成≤25%且本国无煤短缺 |
| 学校机构≥2 | 铁矿全国≥15级，或对应铁供应替代条件 |
| 大学全国≥5级 | 工具厂全国≥15级，或对应工具供应替代条件 |
| 造纸厂全国≥8级 | 钢厂全国≥5级，或对应钢供应替代条件 |
| 至少一所大学≥3级且occupancy≥75% | 武器厂全国≥10级、铁路全国≥10级 |
| literacy_rate≥20% | 至少一所武器厂occupancy≥75%且weekly_profit>0 |
| 当前重点=学务；达标月份累计≥12 | army_size≥40；当前重点=实业；达标月份累计≥12 |

父complete最小改为**两个单项短tooltip**，分别包装一条持久变量：学校与官署已完成；工场与军队已完成。不能裸露技术变量名，也不能把两个flag重新包成一个。建设/科技/机构等已经有原生表示能力，留给常驻可见子JE直接呈现。`has_variable`只是未本地化的内部成果，单项短tooltip符合项目规则。

“持续达标月份”与“已累计维持十二个月”现有措辞存在歧义：代码是累计，不是连续。这里建议维持累计机制，只把bar名称明确为“累计达标月份”；若要连续必须另获设计授权，不能在修BUG时添加回零逻辑。

## 与当前原版完整实例对照

### 明治改革父/子链

原版 `je_meiji_restoration.on_complete` 发 `meiji.1`；country event immediate添加 `je_meiji_main`；after先判断经济/军队是否已达成，未达成才显式添加 `je_meiji_economy / je_meiji_army`，已达成则登记对应成果。子JE本体有建设complete、on_complete改国家进度/完成flag、默认钉选；不在自身possible正向依赖自身hasJE。[G2:155–161、640–848][G3:26–45、75–218]

这证实实际接口是country语境的 `add_journal_entry`，没有额外的“刷新JE列表”工具/GUI调用步骤。本体JE文档明确显式add会忽略inactive/possible；`immediate`在激活时执行。`effects.log`虽然把Supported Scopes列none，但自然语言写“scoped country's journal”，实际country event用法提供了落地证据，不能只靠生成文档scope一行误判为需要全局调用。[G1:12–46][G4:250–253]

### 暂停与失效的区别

本体文档 `can_deactivate=yes` 明确：possible变false后可回到inactive；默认不允许。`05_prestige_goods.txt`中的衣服JE显示资格与繁荣possible分离，设can_deactivate，并非用“非繁荣”作为invalid；这是可用暂停实例。[G1:422–424][G5:6–28、79–113]

本案更适合**保持两个子JE可见，仅暂停非优先项计分**，玩家才能随时查建设清单；不必引入can_deactivate。若选择让另一项进入inactive，也必须将永久invalid与临时priority拆开，不能一边deactivate一边invalid。不要复制原版所有其他退出逻辑；它不承诺本MOD的阶段设计。

`has_journal_entry`只检查active，`has_inactive_journal_entry`单独检查inactive。[G4:triggers10415–10443] 因此自动possible与显式add双入口可能在状态更新边界撞车；本次旧日志确见duplicate-entry，但没有证明它会吞掉第一次工业添加。

## complete / fail / invalid 与旧档恢复

| 场景 | 当前源码行为 | 最小修复建议 |
|---|---|---|
| 未选择重点 | 父显示、两个子均不可见；priority缺失。 | 父激活后展示两个未完成子项目，状态说明未选重点。选择只改变计分对象。 |
| 首次选择industry | 应当立即写priority2并显式add；两个子没有默认钉选。 | 定向ensure子JE并默认钉选；父状态立刻显示当前重点。保留按钮真实执行守卫。 |
| 暂时不达建设条件 | 保留months，tick不增。 | 保留，明确“暂停累计”，不加处罚或新fail。 |
| 切换重点 | 旧子invalid静默删除；country months保留。 | 子JE保持可见；priority只控制advance/complete。 |
| 单项完成 | done先置，再奖120月modifier；无专用fail/invalid回调。 | done必须先于奖励，保持幂等；不用active hasJE作为on_complete guard。 |
| 两项完成 | 父complete置reform_done并移除priority；没有显式移除priority_cooldown。 | 清临时priority/cooldown；保留两个done与奖励；后继社会路线沿原nationalism条件开启。 |
| 父invalid | reform_live假（非存活/失印度有人州/分散国，或已经done）；只移除priority。 | 区分已有完成与不再合格；统一清临时选择/运行标记，不删除成果。子invalid仅绑定父制度永久资格/终局，而非优先项。 |
| 破产、战争、IG变动 | 现有父/子没有因此fail；AI选择可能停。 | 不添加新的玩家党派、战争、破产门槛。 |
| 主JE意外移除 | reform_live不检查父JE；月度refresh会重加，子仍可能单独跑。 | 恢复入口先确保父/长期状态，再ensure孩子；子运行绑定有效改革身份，避免孤儿计分。避免反向自调用初始化或把自身hasJE写入possible。 |
| 旧档缺子JE但有priority2/months | monthly refresh会尝试补industry，immediate只在months缺失时置0。 | 保留该恢复合同，不重置months/done。增加恢复时补齐可见的两项目；可通过现有按钮立即ensure，暂停旧档无需等月也能修。 |
| 已完工旧档 | *_done阻止对应子重建；reform_done阻止父重建。 | 不撤销done，不重复发10年奖。无需重开档。 |

本案父/子均**没有`fail`和`on_fail`、没有timeout**，这是当前长期建设设计；不存在一个隐藏“失败条件过严”导致该子JE消失。silent出口来自invalid。原版文档也明确未定义fail即不能fail，invalid是无失败通知的静默移除。[G1:130–158] 不应为了字段齐全凭空新增失败结局。

旧档自动补漏来自：

- `on_monthly_pulse_country`→`nesnd_india_maintenance`→refresh，root=country；
- `on_country_formed`同样刷新，root=新country；
- `on_game_started_after_lobby`→startup→every_country→refresh，原版注释该hook是每个campaign第一次进局，**不能宣称每次读档都运行**。因此现有旧档保障是月度回调与按钮，不是读档回调。[M5][G10:10–13、474–475、3886–3887]

印度合并继承效果只复制school/industry/reform等done，不复制priority/months。[M9:106–113] 这是与普通旧档补漏不同的跨国迁移；本次MUG原地修复不应擅自扩成统一继承设计重写。

## 推荐最小补丁合同

1. 在trigger层拆开“改革/项目仍有效”“该项目当前获得优先资源”“建设达标”。项目可见/保留不含priority；tick与完成仍需当前priority。只改印度两项，不触日印其他路线。
2. `refresh`在父有效时ensure两个未完成子JE，按钮执行后直接调用同一ensure；子JE默认钉选。不要让initialize反向递归add自己的父JE，也不要把进度清零作为刷新手段。根据active/inactive实际状态避免不必要重复add；不为清日志删除用户授权保留的其他入口。
3. 父complete拆两个成果勾叉，子complete保留native ready条件及单一月份tooltip。priority不要hidden到玩家无法知道暂停原因；用一条短状态或单项条件表示。
4. 父/子终局只清临时选择/运行标记，保留成果、累计与已发奖励。统一complete/invalid的幂等提交。清理不能以“自己仍hasJE”为必要条件，因为结算回调可能已从active列表移除。
5. 四个市场短缺检查显式取得调用country；country-ready与bar-ready分别传入正确国家引用，不能全局把root换成root.owner。普通complete/tick里root.owner并不保证存在。这个修复不变动矿/厂/市场替代阈值。
6. 增量恢复对已有MUG读档有效：缺月份默认0、已有值保留、done不重领；priority无值时不猜先学校/工业。可把未选择状态保留为玩家选择，而非给新政治门槛。

## 验证建议：验证行为，不以存在字符串代替

外部检查应从本次实际源分支提取判断，覆盖：priority缺失/1/2；学校或工业done；父done；months缺失/0/11/12；建设达标/失达标；active/inactive/缺失子JE；MUG暂失印度州再恢复。每个反例需能检出旧代码：例如priority从2→1时旧industry invalid=true而修复后应仍可见且tick=0。只验证文本包含`add_journal_entry`不能证明首次点击成功。

需要用户后续定向引擎验证的最小矩阵（本次未运行）：

| 场景 | 要观测的事实 |
|---|---|
| 旧MUG档点先兴实业，暂停状态 | priority=2；工场子JE确在完整活动列表；默认钉选；建设逐项显示；不靠推进时间才出现。 |
| 同档切重点 | 旧项目仍可见、标暂停、country months不变；新项目计分；十二月冷却仍生效。 |
| 11个月→次月且ready | 只增加1个月，只发一次奖励；不因bar先更新和JE同步产生双计分。 |
| ready暂时false后恢复 | 累计保留、暂停期不增；重新达标继续。 |
| 两项结算同周期/旧档两项done | 父完结只一次；无父重建、无子重奖；后继按现有nationalism条件出现。 |
| 存读档 | priority、months、done保持；缺JE补漏；显示条件与完成勾叉准确。 |

本次可读日志仅作线索：第一次读取 `error.log` 时文件430818字节、LastWriteTime 17:13:54，行232/233报告MUG重复reform/foreign，行281报告MUG重复schools（16:50:50），未找到industry/priority脚本错误。研究期间该文件被外部进程更新到510847字节、17:27:41，重搜已不含这些行；**不能把两次日志当同一冻结运行，更不能用无报错推导industry已成功出现**。未改游戏或日志。报告若需要冻结证据，应另由root绑定当时运行/候选及最小状态摘录。

## 原始来源

M均位于唯一主MOD；G均为只读当前本体。行号为研究时版本。

- **M1**：[印度核心JE](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_india_core.txt:1>)。
- **M2**：[改革按钮](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_india_reform.txt:1>)。
- **M3**：[资格与ready触发器](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_india_core.txt:1>)。
- **M4**：[初始化、refresh、tick、sync](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_core.txt:1>)。
- **M5**：[新局/月度/建国回调](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_india_core.txt:1>)。
- **M6**：[安全变量读取](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_india_core.txt:12>)。
- **M7**：[原生进度明细](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_progress_bars/nesnd_india_core.txt:1>)。
- **M8**：[玩家文本](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/zzzzzzzzzzzzzz_nesnd_india_l_simp_chinese.yml:3>)。
- **M9**：[跨国成果继承](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_india_diplomacy.txt:106>)。
- **G1**：[原生JE定义文档](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:12>)，包含country root、显式add、complete/fail/invalid、can_deactivate。
- **G2**：[原版明治父子JE](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_meiji_restoration.txt:640>)。
- **G3**：[明治事件显式子JE创建](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/meiji_restoration.txt:43>)。
- **G4**：[effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:250>)、[triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:10415>)。
- **G5**：[原版可暂停JE](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_prestige_goods.txt:1>)。
- **G6**：[进度条先于JE pulse](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/scripted_progress_bars.md:20>)。
- **G7**：[原版bar的owner与root.owner](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/00_ip4_morocco_progress_bars.txt:168>)；[另一实际owner实例](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/00_ip4_victoria_progress_bars.txt:65>)。
- **G8**：[短缺trigger输入要求](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:9407>)，本体实际 `common/alert_types/00_alert_types.txt:410`传`scope:actor`。
- **G9**：[历史内容组country context](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entry_groups/00_journal_entries.txt:99>)。
- **G10**：[回调root与启动频率](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:10>)。

技能复核：本次依据再次印证现有“available与永久结束分开”“原生逐项条件”“源码检查不等于引擎验收”约定，未新增或修改技能。


## 来源指纹

| 文件 | SHA-256 |
|---|---|
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\journal_entries\nesnd_india_core.txt` | `624b1e26679136bf170515efd343a5eaf7a59e5b1e04b9a188aba03d74d4a1ca` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\scripted_buttons\nesnd_india_reform.txt` | `91cb05f6cfa7cae8191ad6404a1c80a5143f5a5346581f2157aec36a77fcf804` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\scripted_triggers\nesnd_india_core.txt` | `fdb69f29b8a5cf109dc367d5a5c5368e0bb240eca4f84f65b0257969f35062f2` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\scripted_effects\nesnd_india_core.txt` | `37ec7cd1f2755c59366291666038a6fa6efbe8e3fa76f3860eed6a9b9cac78e3` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\on_actions\nesnd_india_core.txt` | `d3c97d53b64227798e789c770ef65f219e28d120c17da0f6ef5c9a21ea02fa49` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\script_values\nesnd_india_core.txt` | `558382f1b1f8992d672a728e7bbd2d034dd2a562daaa387f93c9b27872603be3` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\scripted_progress_bars\nesnd_india_core.txt` | `aef962512d48cc365064617041db337cecb5323d44fd861b3b3edf5cd498a120` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zzzzzzzzzzzzzz_nesnd_india_l_simp_chinese.yml` | `013b020c0702f42f13f11ad52a77a67307968eb1c1ffa37ce1ba3087e1602bd5` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\common\scripted_effects\nesnd_india_diplomacy.txt` | `8021ffc24d62850d79cdcbf0f155bf81ef88c3a7c651de610635a756c10326e9` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\journal_entries\journal_entries.md` | `1032c0dac08d502d49380e05929912fa94ba3a3a6f2a6279b480d58ea7272323` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\journal_entries\00_meiji_restoration.txt` | `aaaf94eb3c4acd16e2985381ef68f6cd1cf1ca8fa012002ad2305c24faa135d0` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\events\meiji_restoration.txt` | `5e010ebc08631a2c18921792a768d9510cb3b117be961fb0f762597c537144b0` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\references\engine-docs-1.13.11-20261031\effects.log` | `24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1` |
| `D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\references\engine-docs-1.13.11-20261031\triggers.log` | `ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\journal_entries\05_prestige_goods.txt` | `28d78a15b585a27b3978570b22b978ede32ecf31d5b9112f7dae194a320649fd` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\scripted_progress_bars\scripted_progress_bars.md` | `9f0fbb5b5c3dafd72c19dd967dad2801544c730b3cbe2950bd3214dd49933bff` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\scripted_progress_bars\00_ip4_morocco_progress_bars.txt` | `735b39a625b7844baed38a95baec11dcc6d6c8d52e83427fcf73ce32b6e9e6c4` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\scripted_progress_bars\00_ip4_victoria_progress_bars.txt` | `da2c2aca01848a91b000739cd7a9e07b751e1ef8a5b31913c4abebf979f29dd1` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\journal_entry_groups\00_journal_entries.txt` | `ccee248be47bc1606e715f16503cca90aa2baa15a89ef978a5665c1eb8dee439` |
| `D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\on_actions\00_code_on_actions.txt` | `ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb` |


## 本批复核：是否已在任务25/26修好

本批重新读取主MOD五个核心文件，并对前报告20个原始来源逐文件比较SHA-256，全部相同，前述行号与结论仍适用。以下直接比较两个已交付候选与当前主MOD，不把交付叙述当运行证据。

| 文件/闭包 | 任务25→任务26→当前主MOD | 对本问题的结论 |
|---|---|---|
| `common/journal_entries/nesnd_india_core.txt` | 三者完全同SHA `624b1e26679136bf170515efd343a5eaf7a59e5b1e04b9a188aba03d74d4a1ca` | 合并完成tooltip、无子JE钉选、priority绑定invalid均未改。 |
| `common/scripted_buttons/nesnd_india_reform.txt` | 三者完全同SHA `91cb05f6cfa7cae8191ad6404a1c80a5143f5a5346581f2157aec36a77fcf804` | 按钮原来就set priority后调用refresh，不存在后来漏合“add子JE”的修复。 |
| `common/scripted_effects/nesnd_india_core.txt` | 任务26只改36/38行的两司entry，当前等于26 | schools/industry显式add和月份累计未改变。 |
| `common/scripted_triggers/nesnd_india_core.txt` | 任务26只改USM地区集合，当前等于26 | 两项priority资格与工业root短缺检查未改变。 |
| `common/on_actions/nesnd_india_core.txt` | 任务26给维护/开局筛选补外交残留对象，当前等于26 | MUG月度修复入口本来存在；本轮失去末州后的补漏是顾问清理，不是德里子JE显示修复。 |

对比来源：[任务25独立候选](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/india-development-20261103-a/common/journal_entries/nesnd_india_core.txt:1>)、[任务26独立候选](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/commission-boundaries-20261103-a/common/journal_entries/nesnd_india_core.txt:1>)、[任务26交付说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/commission-boundaries-20261103/release-notes.md:1>)。

任务25 `final-validation.json:1493–1501` 的三项是 `schools same possible and explicit-add qualifier`、`industry same possible and explicit-add qualifier`、`School and industry progress preserved across priority switch`。它们检查的是同一谓词和country月份不被清零；**即使旧JE切换时invalid消失，这三项仍可通过**。所以本次是原覆盖漏掉了显示与JE生命周期，不能称“这个问题当时已实测修好”。任务26交付也明确旧484中有关键字存在性检查，UI首次出现仍未运行。

## 当前设计回答与严格最小范围

按现有源码，玩家选工业后**学校不出现是当前只开放优先项的设计**；但工业应出现。两者都未选择前都隐藏。用户反映工业也没出现，则不符合这条脚本意图。没有证据支持把“学校须先完成”加给玩家：这条限制只在工业按钮AI权重里。

为了保持原先“先选一项”的设计，严格最小方案可比前文的“双子项目始终显示”更窄：

1. 选中项目显式ensure并默认钉选；父状态显示当前重点；未选中且从未开启的项目仍不提前创建。
2. 将“已经开启过”与“当前优先”分开。已开项目切换后保留可见、停止tick，`invalid`仅处理改革资格真正丢失/完成，不用priority。已有active JE或已有priority可登记opened；旧months/done保留。
3. 父完成仍只要求原两项done，拆成两个单项可见条件；子JE科技/建筑/机构/就业/军力条件不改，累计12个月不改。
4. 按钮和月度backfill共用同一个幂等ensure；父完成/失效清临时选择/冷却。不要重刷初始军队、法国请求或其他日印JE。

上文“双子JE同时可见”只是改善查条件的可选呈现，不是解决BUG必须扩展的范围。本批建议root优先采用以上保留原分阶段开启的方案。

## 可证旧代码失败模式，供实现回归

这些是可从真实源码导出的反例，不是宣称执行了Jomini引擎：

| 编号 | 输入/旧代码分支 | 旧代码确定结果 | 修复后应验证 |
|---|---|---|---|
| I01 | 活跃industry、未done，priority由2改1 | `industry_available=false`→industry `invalid=true` | 仍有已开子JE，paused；months不变。 |
| I02 | parent reform完整complete | 两done在同一个custom_tooltip | 拆两条真假项；任一done时可区分已完成项。 |
| I03 | priority2且industry未done；观测钉选列表 | 子JE没有默认钉选字段，parent有 | 新开子JE默认钉选；完整列表与钉选分开断言。 |
| I04 | priority2旧档，industry JE缺失，months=7 | 月度refresh资格为真，add分支可达；immediate不应清已有months | 恢复实际JE且条=7，奖未发；不能只断言源码含add。 |
| I05 | industry_done=true但JE意外重触发 | on_complete guard含available，done使其false | 不重奖；父完成不清完成标记。 |
| I06 | industry_ready由bar的owner country调用 | market_good shortage参数仍root（JE） | country调用与JE-bar调用均传实际MUG；不统一替换root.owner。 |
| I07 | 新国回调或月度country入口 | root country，已有imperial_line/months不重置 | initialize→父ensure→子ensure，无反向递归。 |
| I08 | 父本身在complete回调被移出active列表 | 现有结算不依赖hasJE，仍能置done | 保持这一点，别为“父子关联”给on_complete加入active自锁。 |

第一次按钮后industry的实际运行状态仍需要最小country/JE摘录才能定位。当前源码的已有显式add链、无解析报错或旧STATIC_PASS都不足以替代这条证据。本报告没有读取完整存档、没有启动游戏、没有改candidate。
