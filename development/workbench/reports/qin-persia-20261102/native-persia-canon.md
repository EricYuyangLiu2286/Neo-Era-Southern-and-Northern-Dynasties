# 唐衣大食／西秦：原版波斯链、战争设定与声索范围研究

日期：2026-11-02。范围：只读 GAME、主 MOD 与作者材料；只写本报告及 `claimsets.json`，没有修改 MOD、技能或启动游戏。采用 NESND、Matt Pocock research 和玩家文案技能；本任务本身已是被委派的研究代理，按本轮要求不另开代理。

已运行 NESND `catalog.py status`：**1.13.11 / build 24799966，CURRENT，changed_count = 0**。以下结论为当前源码研究和实现建议，不是游戏验收。

路径简写：

- `G` = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`。
- `M` = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`。
- `W` = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`。

## 1. 结论与直接影响实现的发现

1. 原版波斯只有一个适合借用结构的长期总日志：`je_eastern_frontier`。入口在 `G/common/history/countries/per - persia.txt:33–37`，经 `03_eastern_frontier.txt` 调五个按钮，再进 `persia_events` 与国家／地区修正。**当前 MOD 的同名波斯国家史没有加入该日志**，不能假定新国已继承原版内容。[原版入口](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/per - persia.txt:33>)；[当前国家史](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/per - persia.txt:1>)。
2. 当前 MOD **巴士拉、巴格达、摩苏尔已经归 PER**，分别在 `M/common/history/states/00_states.txt:143,6208,6217`。西向范围必须按本 MOD 的奥斯曼／埃及开局领土选择，不能照搬原版两河声索。[当前两河](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:6208>)。
3. PER 已在历史初始化成为 QE1 朝贡国：`M/common/history/diplomacy/ce_subject_relationships.txt:168–182`。援秦满条时应该幂等确认关系，已有正确关系直接保留。[关系入口](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:168>)。
4. 作者 PPT 已证实的是四次“近西战争”。在 20261031 抽取的 PPT 与其他 `.txt` 原资料中检索“远西战争”无命中。用户分别说“重启远西战争”与“同样的近西战争重启”，属于本轮命名不一致；可按分支采用“重启远西战争”（援秦西进）与“重启近西战争”（离秦东进），但必须标为本轮设计，不能声称原文已有此地理区分。见第 2 节。
5. 秘密路线完成时“推翻秦国统治”的具体独立方式尚非用户明确细化项。最小建议是：仅在 PER 仍为 QE1 属国时和平独立，再进入东向声索日志；不要无条件释放其他宗主的属国，不强制发动用户没指定的独立战争。当前原版有**日志满条→国家事件→`make_independent = yes`**的琉球实例，见第 5 节。

## 2. 作者战争设定与唐衣大食现有身份

原 PPT：`D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx`。本研究重新读取原文件并核 SHA-256：`b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`，与 `W/research/20261031/北明ppet.json` 记录相同。以下段号为 JSON 的 slide／paragraph；TXT 行号也逐项核对。

| 作者原始位置 | 作者明确记载 | 本轮可采用／不能推出的内容 |
|---|---|---|
| PPT 21 p19；TXT 274 | 1591–1600 第一次近西战争，陈秦与游牧仆从对抗呼罗珊、萨菲波斯和德里联军，战后帖木儿入主德里、波斯衰落 | “近西”从一开始已涉及中亚、伊朗与印度，不是仅指秦国以东或唐衣大食以东。 |
| PPT 21 p20；TXT 275 | 1608–1611 第二次近西战争；秦胜波斯、莫卧儿、乌兹别克同盟，在呼罗珊建立中国藩王统治的唐衣大食 | 唐衣大食起源与秦的军事体系有关，不套现实卡扎尔王朝。 |
| PPT 21 p22；TXT 277 | 1632–1637 第三次近西战争；秦胜波斯、莫卧儿、奥斯曼联军，征服设拉子，以唐衣大食控制伊朗高原 | 可写军政传统与伊朗地方治理的张力；不能把原版“恢复阿契美尼德／纳迪尔沙旧土”直接当本王朝宣言。 |
| PPT 21 p23–24；TXT 278–279 | 1716–1730 第四次近西战争，目标为两河；秦败；冯小奎著《肆伐大食史略》 | 当前 PER 已占两河；“重启战争”可承接历史雄心，不能据历史目标自动添加已拥有地区声索。 |
| PPT 22 p22；TXT 301 | 1673–1704 阿兹丹（汉名陈玉梁）统治波斯，以商贸、技术与近代化改革缓和民族矛盾，扩张秦体系下的自治 | 适合内政／经济 JE 的事实切口：商贸、技术、族群与自治。不能无依据决定其与游戏高昌李氏的确切谱系。 |
| PPT 22 p24；TXT 303 | 1699 《东方条约》试图维护东地中海、黑海、里海周边和平，保证海陆丝路畅通与贸易自由 | 可以设计本地商业和交通建设；不要求自动加入现实英国贸易体系。 |
| PPT 22 p28–30；TXT 307–309 | 第四次战争中伊斯兰诸派拥戴奥斯曼；1729 秦俄围伊斯坦布尔失败；1730 秦俄大食联军签《巴格达条约》 | 共同军事传统与穆斯林合法性可以并置，不替任何一方添加现代民族主义定论。 |
| PPT 13 p10、p12；TXT 128–129 | 秦军退守伊犁；皇族仍东顾玉门，军士、武勋不敢再言东征，与俄、波斯、莫卧儿争夺西亚霸权 | 波斯参与秦局势具有设定基础；秘密文化运动及每月扣团结是本轮用户新机制，不是作者已写事件。 |

[作者抽取原文](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031/北明ppet.txt:270>)。

当前原作者开场：`M/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:28` 的 `PER_FLAVOR_TEXT`，与原始 `f18b6c4`／修改前备份同键一致，叙述**高昌李氏、元代汉军世侯、浩罕与希瓦军阀生涯、伊尔汗与穆斯林贵族联姻、秦国安西军府庇护、王朝主宰伊朗**，结尾同时称其为西秦后裔和先知追随者。不能写成“异教征服者统治纯波斯臣民”的单线故事。[作者 PER 开场](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_country_flavor_text_l_simp_chinese.yml:28>)。

当前 PER 定义为 unrecognized / empire，文化 `ce_xiyu persian`；国家史执政集团含地主、什叶派学校、名为“武勋门阀”的军队；法律包括传统主义、重商主义、奴隶贸易、国家宗教。来源：`M/common/country_definitions/ce_countries.txt:153–164`；`M/common/history/countries/per - persia.txt:3–31`。

**动态国名注意**：`M/common/dynamic_country_names/ce_dynamic_country_names.txt:843–884` 中唐衣大食为 priority 50、汉文化条件；秦／华／明的属国名“波斯将军府”为 priority 75。因此新日志谈唐衣大食政治传统成立，但当前玩家看到的国名未必是唐衣大食。保持既有动态命名，不在本研究擅改。

## 3. 原版完整链条与可借用的部分

| 层 | 当前源码与行号 | 实际行为与适用差异 |
|---|---|---|
| 调用者 | `G/common/history/countries/per - persia.txt:33–37` | `has_dlc_feature = ep1_content` 后 `add_journal_entry = { type = je_eastern_frontier }`。MOD 覆盖该文件，不自动继承调用。 |
| 日志数据库 | `G/common/journal_entries/03_eastern_frontier.txt:1–100` | 13–17 行注册五按钮，19–52 行保存国家、文化与地区 scope；55–80 行征服三个地理组并复兴梅尔夫；83–87 行触发 `persia_events.1`；无固定到期时间。原版为扩张总日志，本轮应另做三个小内政日志。 |
| 声索按钮 | `G/common/scripted_buttons/04_persia_buttons.txt:1–227` | 拥有赫拉特后，事件 `persia_events.2` 添加大呼罗珊与河中声索；国家级一次变量防重复。按钮内 `show_as_tooltip` 仅预览，实际声索由事件兑现，不能照抄两边造成双执行。 |
| 外力响应 | 同文件 194–209 行；`G/events/soi_events/00_ep1_persia_events.txt:355–379,900–967,1020–1226` | GBR 在大波斯有利益、关系不高于中立、不是外交博弈盟友／宗主、无休战时触发反应。可移植“有利益＋关系／阵营＋真实目标”的判断，不照搬固定英国。 |
| 国内发展按钮 | `04_persia_buttons.txt:543–592` | 占有整个梅尔夫且当地城市中心 ≥2 后可复兴城市；只执行一次，进 `persia_events.7`。本 MOD 梅尔夫归 QE1 等，不能把 PER 的初始国内任务绑在尚未拥有的梅尔夫。 |
| 国内发展事件 | `00_ep1_persia_events.txt:967–1018` | 重新取得 PER 的梅尔夫 state scope，玩家二选一：当地农业吞吐或国家威望。国家、地区 scope 分开，提供本轮内政分工的实际模板。 |
| 修正数据库 | `G/common/static_modifiers/07_sphere_of_influence_2_modifiers.txt:23–30,65–74,109–112` | 梅尔夫国家威望 +10%；水坝本州农业吞吐 +10%；东方财富公司吞吐／公司建设效率；学院技术传播／大学吞吐。数值不是本轮“小 buff”的自动基线。 |
| 本地化 | `G/localization/simp_chinese/sphere_of_influence_persia_l_simp_chinese.yml:1–90` | 含纳迪尔沙、波斯奴隶、英国／俄国军事团等现实语境。只参考字段和因果，不把这些史实搬进高昌李氏剧情。 |
| UI | `G/gui/journal_entry.gui:188–189,215–216,246–267` | 状态、按钮、进度条分区；bar tooltip 调 `ScriptedProgressBar.GetPeriodicProgressBreakdown`。状态只写当前处境，独立条件逐项原生勾叉，按钮门槛不重抄进状态。 |
| 资源 | `03_eastern_frontier.txt:4` 与 `00_ep1_persia_events.txt:975–983` | 常规地图图标实际存在；原事件视频 `ep1_central_asian_city` 且标 dlc010。新自有日志可使用已核常规图标，不为借事件结构顺带引入 DLC 视频依赖。 |

[原版 JE](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/03_eastern_frontier.txt:1>)；[按钮](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/04_persia_buttons.txt:543>)；[事件](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/soi_events/00_ep1_persia_events.txt:967>)；[修正](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/07_sphere_of_influence_2_modifiers.txt:23>)。

三个小常驻内政 JE 的建议切口（是设计说明，不是最终玩家正文）：

- **水利与农业生产**：借梅尔夫“城市门槛＋当地农业修正”的结构，在 PER 实际拥有的伊朗州选目标；不要写成征服梅尔夫的前置。以单州工程为规模，不用全帝国永久无限叠加。
- **商贸与财源**：承接阿兹丹改革和《东方条约》的通商传统，用当前国内城市／交通／经济法条件展示政策阶段；独立条件各一勾叉，真实商业效果放按钮结果。
- **学院与技术**：借 `darulfunun_modifier` 的国家技术传播／大学吞吐分工，承接作者“商贸和技术进步”，不把真实世界阿米尔·卡比尔传记自动放进李氏历史。

“常驻”建议指日志可以持续管理、无自动短时超时，不代表奖励永久可刷。可用阶段变量显示已完成工程、每次行动独立冷却；若用一次性完成型则不符合常驻管理的本轮需求。具体新增标题、正文、事件、按钮仍须按玩家写作技能另做同类作者原文对照；本报告未把这些工作名当正式文案。

## 4. 路线进度、事件与量纲

用户明确要求：援秦／颠覆二选一；颠覆 AI 25%，援秦 75%；两条均 0–100、每月固定 +2；援秦随机触发三类小立法／建设／合法性事件；颠覆期间若 QE1 的团结机制仍存在，每月扣 1%，并由 QE1 原生 bar 显示“波斯文化秘密运动：−1%”。

- 用 100 点最大值时，+2 是每月 **2 个百分点**，无其他增减从 0 到 100 为 **50 个自然月脉冲**，不是“2% 当前值”；若 QE1 团结 bar 最大值为 100，扣 1 点才是 1 个百分点。若其最大值不同，应按满值的 1% 转换，不能盲写 -1 或乘 0.99。
- 原生 bar 支持 `start_value = 0 / min_value = 0 / max_value = 100 / monthly_progress = { add = { desc = … value = 2 } }`。来源 `G/common/scripted_progress_bars/scripted_progress_bars.md:8–10,20–36`。该文档第 20 行明确周期更新先于 JE 的同周期 pulse。
- **扣团结只放在 QE1 的权威计算链一次**。在 QE1 bar 中加入带条件的具名负项，条件检查 PER 仍处秘密路线、PER 对应 JE 仍有效、QE1 团结 JE 仍有效。不要一边 PER 月脉冲扣变量、一边 QE1 bar 又扣一遍。若现有系统用变量为权威，则 bar 明细与结算调用同一脚本值并做绝对同步。跨两个 JE 的月度顺序仍需小范围引擎验证。
- 第一月与第 50 月边界需要明确：扣减发生在有效秘密运动的月份；满条终局清掉 active 标记，后续月不扣。QE1 团结 JE 提前结束时，扣减停止，PER 自己的 +2 按用户要求继续。不是“秦团结不存在就让波斯永远卡住”。
- 三类随机事件不影响固定 +2。原生 `G/common/journal_entries/00_sick_man.txt:336–351` 示范 `on_monthly_pulse = { effect = … random_events = { 100 = 0 10 = event } }`。可使用相同入口配三事件并留空结果，避免每月必弹；具体事件频率与 buff 持续时间用户未定，需作为实现选择记账。
- 可供小 buff 使用的实际类型：`country_law_enactment_success_add`（0.05 为 5 个百分点，`00_modifier_types.txt:1134–1140`）、`country_construction_add`（固定建设点，314–319 行）、`country_legitimacy_base_add`（固定合法性点，979–984 行）。建议初稿分别 +0.05、+1、+5，短期 3–6 月；这些只是量级建议，没有实测平衡依据。相同修正用同 key 刷新／替换，不因随机重复无限叠高。
- AI 二选一若只这两项且同时可选，事件 `ai_chance = { base = 75 }` / `base = 25` 能给指定比例；不要加入未说明乘数改变 25%。脚本按钮 AI 则是 `value/if/add`，不得混用事件的 `base/modifier`。

[bar 文档](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/scripted_progress_bars.md:20>)。目前主 MOD 的公开 JE／bar 搜索未找到已存在的 QE1 团结条，因此具体新键由父任务实现统一，本研究不编造现有键。

## 5. 朝贡、变更类型及独立

原版 `G/common/subject_types/00_subject_types.txt:124–173` 的 tributary 允许自行发起外交博弈，且不自动参加宗主战争；原版只允许未获认可宗主。**本 MOD 已用 `M/common/subject_types/ce_subject_types.txt:1–55` 覆盖**，加入 recognized 宗主和 great/major/minor rank，因此不能拿原版限制否定 QE1→PER、FRA→MUG 的当前关系。

援秦完成建议的分支：

1. PER 已是 QE1 朝贡：保留关系并仅记录一次成功／开启西向 JE。
2. PER 已是 QE1 其他属国：在 PER scope 用 `change_subject_type = subject_type_tributary`；引擎 docs 说明它保留当前自由渴望值（`W/references/engine-docs-1.13.11-20261031/effects.log:677–680`）。不要先独立再重建造成无谓外交状态变化。
3. PER 独立且 QE1 存在、双方外交状态可兼容：在 **QE1 scope** 用 `create_diplomatic_pact = { country = c:PER type = tributary }`。本 MOD 历史正是此方向；原版 `G/common/diplomatic_actions/31_power_bloc_force_become_subject.txt:41–47` 是同类型真实调用。不可在 PER scope 将 QE1 变成 PER 属国。
4. PER 已成为其他国家属国、QE1 已灭亡／反向成为 PER 属国、双方正在互战：要有明确未决结果或延后重检，不能盲目强制造循环宗主关系。本项属于真实外交前提；AI 的“战争中不选”不应被混写成所有玩家都不能操作的永久禁令。

秘密路线完成建议：`PER = { if = { limit = { is_subject_of = c:QE1 } make_independent = yes } }`，然后记录完成并加东向 JE；若本已独立则不重复。来源链为 `G/events/japan_events/ryukyu_rivalry_events.txt:627–636`，注释明言 JE 满条触发并在国家 `immediate` 执行独立；引擎 `effects.log:9819–9822` 确认 country scope。该方案是用户“推翻秦国统治”在小型路线中的建议兑现方式，不是已确认作者正史。

独立战争另有 `dp_independence` 数据库（`G/common/diplomatic_plays/00_diplomatic_plays.txt:202–252`）和 `G/events/british_raj_events.txt:276–280` 实例。但该事件写 `target_country`，当前引擎 docs 的 `create_diplomatic_play` 却说明 scoped object 为目标、显式 `initiator`（`effects.log:909–922`）。此处有源码／文档接口差异，不能照抄这一段就声称已证实调用。用户也未指定战争终局，优先用上面的最小和平独立建议；若选择战争，须另查更新实例并实际验证。

无论哪条路线，所有成功、失效和意外移除都要清理路线 active 状态／随机事件入口，保留完成标记；只在首次初始化设 0，旧档恢复不得重置已积进度。避免把历史 `nesnd_qe1_per_relation_v1` 迁移标记做成永久强制复朝贡开关。

## 6. 实际开局声索集合

完整逐州 ID、所有开局分割所有国及 `00_states.txt` 行号已保存 [claimsets.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/qin-persia-20261102/claimsets.json>)。取的是当前 MOD 的定义，所有 `create_state` 所有者保留；没有把重复块折叠为单一国家。

用户只指定方向及“中东的一些州”，未列全州。下列为**首圈建议**，不是作者地理定论；JSON 另给全中亚／南北印度战略区候选，供父任务需要更广范围时选取。

| 路线／组 | 建议州 | 当前拥有者要点 |
|---|---|---|
| 援秦：黎凡特与南安纳托利亚（8） | ADANA、DIYARBAKIR、DEIR_EZ_ZOR、TRANSJORDAN、PALESTINE、LEBANON、SYRIA、ALEPPO | ADANA 为 EGY/TUR 分割；DIYARBAKIR、DEIR_EZ_ZOR 为 TUR；其余五州为 EGY。均符合本 MOD 开局奥斯曼／埃及范围。 |
| 援秦：埃及（4） | SINAI、LOWER_EGYPT、MIDDLE_EGYPT、UPPER_EGYPT | 均 EGY。埃及沙漠、马特鲁没有列入首圈；苏丹、厄立特里亚、克里特和巴尔干不自动纳入“中东”。 |
| 援秦：阿拉伯（6） | OMAN、ABU_DHABI、YEMEN、HEDJAZ、HAIL、NEJD | 来自本 MOD `region_arabia`，含分割地区；用户单独授权的阿拉伯范围，不要求当初归 EGY/TUR。 |
| 秘密：大呼罗珊／花拉子模／河中（12） | HERAT、KABUL、KANDAHAR、BALKH、CENTRAL_HIGHLANDS、MERZ、NORTHERN_BALUCHISTAN、TURKMENIA、KHIVA、FERGANA、TAJIKISTAN、UZBEKIA | 与原版 `je_eastern_frontier` 三组完成条件相同，当前多数涉及 QE1，也含其他小国的分割份额。 |
| 秘密：西北印度（7） | SINDH、PUNJAB、HILL_PUNJAB、DELHI、AGRA、RAJPUTANA、GUJARAT | 德里／阿格拉等涉及 MUG；古吉拉特包含 USM；能实际连接用户点名的法国（经莫卧儿）与明势力，而非只写抽象欧洲干涉。 |

以上省略统一 `STATE_` 前缀；机器文件保留完整 ID。西向首圈 18 州，东向首圈 19 州。扩展候选来自 `M/common/strategic_regions/west_south_asia_strategic_regions.txt`：中亚 17 州、北印度 16 州、南印度 8 州。南印度列表含锡兰，属于当前战略区定义，不代表用户已明确要将锡兰纳入印度大陆战争。

实施时按**冻结的开局 ID 集合**提供声索，不在 1840 年重新取 TUR/EGY 当前全部领土，否则会随未来征服扩张目标。每次领取再排除已有完整所有权／已有声索；声索使用 `s:STATE_X = { add_claim = scope:PER }`，不转移州，也不把 split state 的某国份额当整个地区。原版按钮一组授予多州，但用户还要求一个月缓冲；建议一个区域按钮一次成功授予一组、完成后锁定，或每次一个未声索州，两者都可。**用户未明确批量粒度**，需要父任务明确选一种并记录，不把原版一次性整组隐含为强制。

## 7. “有强权”与宣称成功的建议判定

不能简单写“FRA 存在则所有声索失败”，否则整个路线可能永久无效。原版 `greater_khorasan_button` 194–209 行的判断有三个实质条件：在相关地区有利益、关系不高于中立、没有盟友／宗主／休战排除关系。法国经 MUG 的当前关系在 `M/common/history/diplomacy/ce_subject_relationships.txt:185–197`：FRA 对 MUG 建立 tributary。

建议把用户点名 FRA、MUG、USM、RUS、QE1 作为需要检查的政治行动者，按下列条件判断本次目标是否受其阻挠：

1. 国家存在，并且**拥有目标地区的一部分、其属国拥有目标地区，或在目标对应战略区有利益**。法国需沿目标所有国的 `overlord/top_overlord` 解析到 FRA，不能只搜法国直属土地；本体 `G/common/scripted_triggers/00_clothes_triggers.txt:466` 已有 `top_overlord ?= { … }` 用法，`00_ai_triggers.txt:68` 有 `any_overlord_or_above` 实例。
2. 与 PER 的关系不高于中立；不是 PER 当前宗主／宗主链、不是共同外交博弈盟友。这样援秦路线的宗主 QE1 不会因为“存在”就反过来阻止全部西向行动；秘密独立之后 QE1 可作为竞争者。
3. 沿用原版有休战即不触发此特殊干涉的处理。其他条约是否排除，须逐项用当前 treaty 查询，不凭旧同盟 effect 猜测。
4. 如果还要扩展到用户没点名的国家，用引擎 rank 条件将列强／强国与未获认可大国并列；不要只 `country_rank >= great_power`，否则漏掉 MUG 或未获认可国家。固定用户点名者不应因原版属国 rank 上限被无意全部过滤。

**最小成功规则建议**：没有上述反对强权时成功授予声索；有反对强权则本次失败并给出该国与所涉区域，保留一个月后重试。它符合用户的“是否有强权判断是否成功”，不用凭空加第二个随机百分比。若希望友好强权保障成功，可以通过关系／宗主排除自然达成。这里的阻挠模型与失败表现是建议，用户没有给详细外交算法。

按钮本身应允许按设计支付尝试成本，是否成功在效果中重新检查；不能只在 `possible` 检查成功条件而让“失败尝试”永远发生不了。没有剩余可授予声索时禁用，避免空扣合法性；每个独立前提单列原生条件。若多个组按钮可并列，使用**共享一个月锁／费用修正**，否则单按钮各有冷却仍可同日点完数个区域，违背“点一次缓冲一个月”。

**成本量纲**：`country_legitimacy_base_add = -5` 是临时合法性修正，持续 `months = 1`；不是永久删除 5 点政治库存，也不是 -5%。冷却也用 `months = 1`，不用 30 天冒充日历月。可参考原生按钮的 `cooldown = { months = … }`（`G/common/scripted_buttons/00_wild_je_buttons.txt:40`）。国家 modifier 定义在 `00_modifier_types.txt:979–984`；原生 -5 示例在 `G/common/static_modifiers/00_ep2_02_modifiers.txt:37`。

原版波斯声索按钮的 `is_at_war`／`in_default` 仅在 `ai_chance` 降低 AI 使用概率（`04_persia_buttons.txt:214–225`），**不能搬入玩家 `possible` 后当成必要玩家资格**。开场状态不列未来叛乱或后续声索总规则，状态也不复述按钮全部门槛。

## 8. 待实施时必须关闭的边界

- 初始已有朝贡关系、独立状态、其他宗主、QE1 灭亡、反向宗属分别收尾；完成标记防重复给新 JE／奖励。
- 新档及有进度旧档均能恢复；取消／结束秘密路线后停止 QE1 月扣；50 月完成边界和跨 JE 更新顺序需实际验证。
- 声索目标所有国可能灭亡、州被吞并或早已获得声索；点击与事件选项执行都重验保存目标，不能在确认后换目标或空扣。
- 援秦随机小 buff 不能无限叠高；三类只在有效路线刷；同月成功事件结束后不继续随机弹出。
- 各小游戏 JE 保持常驻和小体量，不能被原版扩张总 JE 的“占全中亚”硬门槛绑住。
- 本研究只确认来源和建议算法。没有声称新文本已过作者逐项审查、没有声称脚本静态通过，更没有声称游戏内验证。


## 9. 读取指纹

以下为研究快照；后续实现若改动主 MOD，同名文件以新版本重新核对。

| 来源 | SHA-256 |
|---|---|
| `G/common/journal_entries/03_eastern_frontier.txt` | `fe924bbf590bbe4c20fd173b1321444cc2f9f0f5f9b731f0711341f793c16ee6` |
| `G/common/scripted_buttons/04_persia_buttons.txt` | `c7ca570c37e6afcd05e86698a696dcc00ad6eac3525694339cae5d469e2fc1db` |
| `G/events/soi_events/00_ep1_persia_events.txt` | `7f86799585cd6bc5936ac1b863548837eb7d937bf24ae05dc1527d78b3521128` |
| `G/common/static_modifiers/07_sphere_of_influence_2_modifiers.txt` | `7f040c2417204186f757506a0e3cedfdb21e545defd59fefff30c09a09185578` |
| `G/common/scripted_progress_bars/scripted_progress_bars.md` | `9f0fbb5b5c3dafd72c19dd967dad2801544c730b3cbe2950bd3214dd49933bff` |
| `M/common/history/states/00_states.txt` | `a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa` |
| `M/common/history/diplomacy/ce_subject_relationships.txt` | `78c0a457795ff30388fd8fa2a3ecff90fb75fc23af6af1e803e30f7b05075aa7` |
| `M/common/history/countries/per - persia.txt` | `5fa7ba7f9b2f5b3d2499df035a22f50bafb29d2200241e52252bd8a5e5f401f6` |
| `M/common/subject_types/ce_subject_types.txt` | `292328c999b666d639bd6ae9795046678d0943b1c996fb6f55c0dd8671390795` |
| `M/common/dynamic_country_names/ce_dynamic_country_names.txt` | `33bb1a5caccf0df985052b5c37c8d93bad9bb2c4eb19c95f93934bfe870a86fd` |
| `M/common/strategic_regions/west_south_asia_strategic_regions.txt` | `da8efdef8673e2a0e06ebf7990f453c434256ecde34901c1a70b37d0debe4a04` |
