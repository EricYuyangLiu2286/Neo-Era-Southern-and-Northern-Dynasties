# 01 南朝易代重做 · 第一批：政治天平核心

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed（第一批，共五批）
Assignee: Claude（2026-11-16）
Blocked by: none
Validation: STATIC_PASS（Victoria 3 1.15.1，待作者新开局复测）
Evidence: [设计、模拟、Toolkit](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-16-south-succession-redesign>) · [改前备份](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-change-south-tilt-batch1-20261116>)

## 现象与期望

作者在观察者局看到 HNA、GNG 很少反吴。期望无人干预时三家同时反吴 95–99%。作者决定重做：每个属国一条政治天平，易代压力满 100 时定下立场，同日易代、开战。设计见工作台 `design-v2.md`。

## 改了什么（第一批）

- 开局外交历史：暹罗改为吴的自治领；删掉原版留下的占巴塞、清迈、琅勃拉邦附属暹罗、柬埔寨附属大南。
- 新文件 `nesnd_south_tilt.txt`（`journal_entries`、`script_values`、`scripted_buttons`、`scripted_effects`、`scripted_progress_bars`、`scripted_triggers`、`static_modifiers`、`events`）：属国日志 `nesnd_south_allegiance` 和进度条 `nesnd_south_tilt_bar`（八项月度来源），两枚表态按钮，朝廷的“忠于明室”“追随郑氏”，锁定 `nesnd_south_lock`，事件“图穷匕见” `nesnd_south_tilt.100`，结算 `nesnd_south_resolve`（明室不战而胜、大吴不战而成立、内战），易代 `nesnd_south_accession`，三省自理国政，战后的拥吴奖励。
- 「吴明论战」：易代压力改由 `nesnd_south_tilt_month` 每个事件 +4（本批没有事件正文，只推进数值）；改制承诺按拥护己方的国数比例增长（X=3）；完成后调用锁定；撤掉“提前推动易代”按钮。
- 开战：`nesnd_open_southern_war` 在创建博弈的块内加入反吴国和拥吴国；博弈建成后才调用易代。`nesnd_call_jingnan_participant` 不再把反吴国从支持者里移出。
- 旧件断开：立场与协定按钮从「南朝诸国」摘下；`nesnd_south_politics_monthly` 清空；`nesnd_board_fixed_ming_allegiance` 恒为否；`flavorUSM.4` 改为调用锁定；`usm_civilwar.1` 和「靖难应对」不再触发。定义留到第四批删除。
- 大表每国多一行天平数值。吴开局补科技“共同基金”。
- 本地化 `nesnd_south_tilt_l_*.yml` 各 78 键。作者原文已用；其余正文是“（文字待写）”，按钮和选项是工作用的标签，第五批统一写。

## 怎么复测

新开局。
1. 吴：日志页有「吴明论战」，易代压力大约每两个月 +4，1839 年 7 月到 100。「南朝诸国」表里每个属国有政治天平一行。
2. 任一属国（例如四川）：日志页有「[国名]藩的命运」，进度条悬停列出月度来源。
3. 观察者局跑到 1839 年 7 月：各属国收到“图穷匕见”，十天后开战。看蜀、楚、淮是否都在反吴一方的战争里，郑莒是否在开战当天才成为统治者。
4. 控制台：`tag USM` 后用 `conclude_journal_entry ce_usm_conflicts_within` 可以提前触发锁定。

## 遗留问题

- 全部没有实机验证。重点：进度条读数写回变量的脚本值；日志标题里的国名函数；创建博弈块内 `if` 加支持者；拥吴奖励里的两个修正是否作用在属国身上。
- 林则徐是吕宋的统治者，楚自理国政时“推举林则徐”的选项目前只在他不是统治者时出现，等于暂不可选。召回后吕宋由谁接任需要作者定。
- 事件链、安抚、遣使、法律提示、战时修正在后面几批。本批里蜀、楚、淮的 AI 会用表态按钮，海外属国的天平只受历史遗留问题和表态影响。
- 和平收场时独立势力的独立博弈要求它仍是吴的直属属国，所以先开博弈再独立。

## 第二至四批（2026-11-16，连续实施，部署 `ee972086`）

- 事件链：`nesnd_south_tilt.1`–`.7`、`.9` 八个特殊事件按月份触发（1836.1、1836.4、1836.7、1837.1、1837.4、1837.10、1838.1、1838.7），1838.4 由现有谋刺案占位；`.50`–`.57` 八个通用事件在进度落后时补发，落在一个随机属国身上。每个选项给点名各方一条限时的月度来源。
- 开局事件 `.1` 加修正 `nesnd_south_regency`（禁改组政府、实业家与地主势力和吸引力 +15%、属国自主欲望上升）和一年的合法性修正，推迟选举；易代或南府清洗时撤除。`.3` 加 `nesnd_south_redemption_levy`（税收浪费 +10%）并入库半年收入的估算值，被加派的一方得一年的税收减益。
- 谋刺案：改由事件链在 1838.4 启动；不再给易代压力加点；遇害时楚、蜀每月 −2、吕宋 −1；在警卫下生还时楚、蜀每月 +1。陈东阳死亡时记全局标记 `nesnd_chen_dead`，雕锦入蜀等后续改读这个标记。
- 按钮：吴的「安抚藩国」；蜀、楚、淮的「遣使南疆」移到属国日志，被遣使的国家天平向中间移动六个月。
- 吕宋开局日志：朝廷准其所请时吕宋每月 +1，八个月。
- 提示「政治天平的摆动」挂在「吴明论战」状态行，逐条显示选举制度、土地法和站队的影响。
- 战时修正 `nesnd_south_wartime`，由「吴明论战」每周续期。
- 楚自理国政可推举林则徐：他在任吕宋时，吕宋另生成一名统治者接任。
- 删除：`nesnd_south_political_ai.txt`、`nesnd_south_timing.txt`（效果）、`scripted_buttons/nesnd_south_accords.txt`、`scripted_buttons/nesnd_succession_board.txt`，以及 `nesnd_early_accession`、`nesnd_federal_compact_button`、`flavorUSM.400`、`usm_civilwar.1`、`nesnd_south_accession_window_open`。

未做或保留：
- 协定事件 `events/nesnd_south_accords.txt`、`nesnd_south_accords` 效果、`nesnd_south_peace.txt`、`nesnd_south_reconciliation.txt` 仍在，已无入口；它们与战后一侧互相引用，没有逐个理清，未删。「靖难应对」日志定义也还在（另有两处条件读它）。相应本地化未清理。
- 吕宋的请求被驳回时没有接天平（四处驳回分支没有逐个核实）。
- “半年税款”用每周固定收支乘 26 估算，不是真实税额。
- 文字是第五批。

## 第五批：文字（2026-11-16）

- `nesnd_south_tilt_l_*.yml` 中英文各 188 键，已无占位。作者认可的十条代表键按定稿写入；易代通告的标题、引文、选项沿用作者原作 `flavorUSM.4`，正文用原作 `usm_civilwar.1.d` 的后半段；「图穷匕见」的三个选项沿用原作 `usm_civilwar.1.1`–`.3`。
- 每个事件都有引文：先秦至明以前的典籍原句、世界内的文书与谚语、素材人物的话。典籍引文按记忆写出，篇名已标，原文未逐字核对。
- 「图穷匕见」正文按天平分拥明、中立、拥吴三段。属国日志正文按三省、屯垦地、藩国分三段（自定义本地化 `nesnd_south_allegiance_reason_loc`）。杭州夜议里的吴王用作用域 `nesnd_wu_king` 取在世的郑家家主。
- 八股检查命中 11 条，改了 4 条，其余是作者认可稿里的句子或真实的转折。

## 收尾（2026-11-16，部署 `0b35b861`）

已做：
- 渡边华山：模板 `JAP_watanabe_kazan`（`character_role_notable`，知识分子集团），开局在日本生成；姓名键 `Watanabe`、`Kazan`。
- 吕宋请求被驳回（`nesnd_phi_finance.1`、`.2`、`.11`、`.13` 的“此项开支暂不核拨”）：吕宋天平每月 −1，八个月。“退回重议”“暂缓签署”不算驳回。
- 半年税款改用引擎的 `tax_income`（每周税收，不含关税、条约和转移）乘 26。
- 典籍引文 13 条已对照维基文库。改正一处：《史记·货殖列传》“天下壤壤”，原写作“攘攘”。
- 删除没有写入方的读取 `nesnd_tilt_ev_10`。其余变量、事件、按钮都有写有读。
- 模拟按已部署脚本重写：`sim/south_tilt_sim.py`、`sim/compact_race.py`；旧版改名 `*_v1_design.py`。结果 `final_as_deployed.txt`、`final_proposed.txt`、`compact_race_final.txt`。

- 作者确认后的数值改动：海外属国 AI 不再按“追随郑氏”表态（权重 20 改 0）；南洋宣慰司起点 24 改 27；远南在拥明区可投东洲（与吕宋同权重）。
- 「吴明论战」加外战状态行 `nesnd_south_status_foreign_war`（作者原文），吴与列强交战时排在最前。
- 「遣使南疆」对象扩到全部在册海外属国（含傀儡国），使者去拥吴区里天平最低、尚未答复的一国；1838 年 6 月的风闻仍只发原来六国；战后清算不变。
- 改制承诺先满时只看朝廷站队：忠于明室即明室不战而胜，追随郑氏即大吴不战而立，不看属国天平（`nesnd_south_resolve`）。
- 按清单删除：`events/nesnd_south_accords.txt`、`nesnd_south_literal_capitals.txt`、旧协定与旧和平效果九个、修正六个、触发器七个、数值七个、「靖难应对」定义及两处判断；中英文各删 46 条本地化。保留战后和解、开战动员快照、`nesnd_south_withdraw_accord`。
- 模拟（8000 局，全 AI，`sim/final_deployed_v2.txt`）：蜀楚淮同时反吴 96.1%；承诺先满 0.5%；吕宋拥吴 51%、中立 40%、自立 7%、投东洲 2.4%；远南拥吴 66%、中立 23%、自立 8%、投东洲 2.8%；南洋宣慰司拥吴 77%；其余多中立。

作者 2026-11-16 追加的结算规则（已实施）：
- 改制承诺每月涨幅按实力加权：实力 = GDP（百万）+ 陆军营数 + 舰队数（`nesnd_tilt_strength`）。涨幅 = 10 × 10 ×（己方实力 − 对方实力）÷ 总实力，取整，可为负，承诺在 0–1000 之间。
- 吴本部恒算拥吴：朝廷追随郑氏时按全部实力，忠于明室时按一半（`nesnd_tilt_court_strength`）。
- 承诺先满：只看朝廷站队，忠于明室即明室不战而胜，追随郑氏即大吴不战而立。
- 易代压力满而承诺未满：一律内战。若无省份自行起兵，大陆三省里天平最低的一家起兵。原“压力满时无人反对即和平”的两个判断已删。
- 模拟（`sim/final_deployed_v3.txt`、`compact_race_final.txt`，实力取自存档“华夏东洲共和国_1839_06_08”，舰队数未取到）：全 AI 内战 98.7%，承诺先满 1.3%；玩家追随郑氏并改法安抚 77–100% 和平；玩家忠于明室 0%。
- 实力改为只算陆军营数（作者 2026-11-17 定）：观察局里吴的 `navy_size` 约 3392，GDP、营数、舰队数三种单位直接相加后吴一家压过全南方，承诺 1838.1 就满、无人起兵。原值 `gdp/1000000 + army_size + navy_size`、系数 10；新值 `army_size`、系数 11（`multiply = 110`）。舰队、GDP 是有意不计。南朝诸国面板去掉舰船一项，两条进度条说明与改制承诺说明改为“陆军”。模拟（`WORK/reports/2026-11-17-observer-1839b/sim/scheme_sweep2.txt`，1836.9 存档营数）：全 AI 内战 100%、三省同时反吴 96%；吴·改法顾蜀淮 吴和 40%，吴·改法顾海外 吴和 99%，吴·不改法 内战 100%；明·肯放属国 明和 100%，明·不放属国 内战 98%，明·退回财产投票 明和 100%。另比较过六种含舰队或 GDP 的加权，都会让明朝玩家在 AI 达标的系数下几乎打不成和平。
- 系数按朝廷立场分开（2026-11-17，作者要求“修改数值”）：只算陆军、系数 11 的观察局（存档 1843.10.22）朝廷追随郑氏，改制承诺第 27 个月满，大吴不战而立。改为追随郑氏 6（`multiply = 60`）、忠于明室 11（`multiply = -110`）。模拟（`WORK/reports/2026-11-17-observer-1839b/sim/court_split.txt`，1836.9 与本局两套营数）：全 AI 内战 100%；吴方四种玩家打法全部内战；明·肯放属国 明和 60–100%，明·不放属国 内战 99–100%，明·退回财产投票 明和 100%。差异已查明（本局开局存档 观察者_1836_03_04）：开局营数是吴 255、蜀 114、楚 98、淮 46，三省只占南方陆军 29%，开局在拥吴区的海外各国占 41%。此前用的 1836.9 旧存档里楚、淮各 131 营，不是开局常态。用开局营数模拟，系数 11 时全 AI 46% 不战而立、平均第 32 个月，与实机第 27 个月相符；系数 6 时全 AI 内战 100%（`sim/early_armies.txt`）。同一组营数下，忠于明室系数 11 时明朝玩家几乎打不成和平（肯放属国 0%，退回财产投票 18%）。
- 作者 2026-11-17 定：a）忠于明室系数改为 15（`multiply = -150`），追随郑氏仍为 6。开局营数模拟：全 AI 内战 100%、三省同时反吴 96.4%；明·肯放属国 明和 100%（第 37 月），明·不放属国 内战 100%，明·退回财产投票 明和 100%（第 34 月）。b）蜀、楚、淮的 AI 在易代未决且偏向明室时、或与吴交战时扩军：判断 `nesnd_south_muster_ai`（不在违约中）；行政策略 `ai_strategy_nesnd_south_muster`（兵营建筑权重 1.5，小武器、火炮求高供给，权重 1000）；同一策略里 `wanted_army_size = { value = wanted_army_size_script_value }`，与默认策略的军队规模相加，即 ×2（原先用 `REPLACE:` 覆盖原版脚本值，作者问能否只留这一个 if，已改为策略内相加，覆盖文件删除）。照原版普鲁士统一策略（兵营 1.5、军队规模 ×2）。扩军对改制承诺的作用未计入模拟：三省营数增加只会压低郑氏一方的承诺、抬高明方的。
- 首辅案加压生效（作者 2026-11-17）：原先压力每月按“事件数×4”重写，朝中事件的 ±2–4 下月即被冲掉，首辅案本身不加压（遇害事件只显示 +25）。现设 `var:nesnd_south_pressure_extra`，每月压力 = 事件数×4 + 该值（`nesnd_south_tilt_month`）。`nesnd_south_add_pressure`：遇害 +25（flavorUSM.5；陈东阳另因他故死亡的 flavorUSM.6 同样 +25，两者不会都触发），负伤 +10，脱险 +3；朝中事件 `nesnd_usm_court_pressure` 同时记入该值。「朝争进展」后半段按现行脚本重写（删去 70 提前易代、1839 年初升满、和解等已不存在的规则）。模拟（`sim/chen_pressure.txt`，开局营数，朝中事件未计）：压力提前满会提前锁定立场。明系数 15 时，全 AI 内战 100%（52% 提前锁定，平均第 35 月）；明·肯放属国 明和 84%，明·退回财产投票 明和 89%，明·不放属国 内战 100%。明系数 20 时三者为 100%、100%、内战 67%。系数未改，待作者定。
- 开局天平重设（作者 2026-11-17，“按你认为最好的做”，明系数不提高）：引擎日志显示开局郑氏一方占南方 `army_size` 的 85%，主因是中南七国（14）与南洋诸邦（16）开局即在拥吴区。改为中南七国、南洋诸邦、吕宋开局 8（中立），南洋宣慰司 27→14，三省仍 −30。实力仍用 `army_size`，系数吴 6、明 15 不变。模拟（`sim/start_values.txt`，权重取 1836.2.1 引擎日志，现行开局一行首月 +44 与实测一致）：开局郑氏一方约 30%，追随郑氏首月 +11；全 AI 内战 95%；吴·改法顾海外仍和平（第 35 月），其余吴方打法内战；明方三种打法均内战。作者指出实机比模拟更容易和平，故取最保守一档。南朝诸国面板删去「改制承诺」说明段与旧协定的两行死数据，两条改制承诺条加原生每月明细（`nesnd_south_compact_monthly_value`）。
- 作者 2026-11-17：陈东阳在首辅案之外去世（flavorUSM.6）不再加压，选项上的“+25”提示删去；只有 1838 年 4 月首辅案的遇害 +25、负伤 +10、脱险 +3 生效。原因：17:13 观察局陈东阳 1836 年春去世，+25 使靖难提前到 1838 年 12 月。AI 朝廷开局站队由郑氏 75 / 明室 25 改为 90 / 10（作者要大吴概率高；原比例下五局中两局抽到明室，属概率，非 bug）。
- 战后收尾从未运行（2026-11-17 查明）：`common/on_actions/nesnd_south_holdouts.txt` 挂在 `on_weekly_pulse_country` 上，引擎不触发它（docs/on_actions.log：From Code: No），所以 `nesnd_south_holdout_wu_tick` 从未执行，三省都归附后「未息的南朝战事」也不会结束，只剩两年期满的「议定现状」。已改挂 `on_monthly_pulse_country`。另有七个系统（美洲复国、埃及、欧美、汗国、奥斯曼两项、西部置省）挂在同一个钩子上，作者同日决定一并改挂月度脉冲，这些系统此前从未运行，行为待实机观察。
- 外交行动 `da_nesnd_south_concede_autonomy`「让权换取效忠」（作者 2026-11-17）：朝廷忠于明室时，对拥吴区的属国提一级自主程度，其天平每月 −3、12 个月；已无法再提高的属国改为独立。AI 只在对方还能提高时用，评估概率 0.005。模拟（`sim/final_deployed_v4.txt`）：全 AI 内战约 98%；玩家忠于明室并逐国让权，明室不战而胜 100%，平均第 26 个月。
- 「朝争进展」里的改制承诺说明已换成现行规则，第二段用作者原文。

遗留：
- 让权行动的名称和说明是代理起的草稿，待作者确认。
- 全部没有实机验证。

## 让权换取效忠：自主级数（2026-11-17，作者定为保持现状）

- 本 MOD 属国只有两级自主程度。自治领、保护国、朝贡国已到顶；只有南洋 8 个傀儡小邦能再提一级。
- 因此对吕宋、远南、南洋宣慰司、中南七国、文莱、布隆岸、兰芳用这个行动就是直接独立。
- 模拟（`sim/concede_tiers.txt`，每月 −1.5）：玩家忠于明室并肯放属国独立，明室不战而胜 100%，平均第 32 个月，丢约 12 个属国；不肯放则内战 100%，期末承诺约 62。全 AI 内战 98.8%。
- 作者决定：保持现状。忠于明室的和平是放弃海外换来的，明室没有郑家的海上力量，留不住海外。
- 此前按“可无限提级”算出的 78.9%、100% 作废。

## 2026-11-17 定稿的海外设定（部署 `b33096ac`）

- 吕宋、南洋宣慰司改为傀儡国；让权对它们只能提一级，不得放归独立；蜀、楚、淮同样不得放。
- 让权每月 −1.5，十二个月；因让权独立的属国与吴双向停战 60 个月。
- 吕宋起点 13。吕宋、远南、南洋宣慰司的「历史遗留问题」每三个月 +1。
- 中南七国天平高过 16 后每月 −1，回到中立区为止。
- 模拟（`sim/final_deployed_v6.txt`、`keep_yn1.txt`）：全 AI 内战 99.7%，三省同时反吴 96.4%；吕宋拥吴 73%，远南拥吴 94%，南洋宣慰司拥吴 94%。玩家忠于明室并肯放远南，明室不战而胜 100%（第 39 个月，放走约 11 个属国）；不放远南则 59.8%。玩家追随郑氏并改法，大吴不战而立 87–100%。
- 作者认可以上结果。全部未实机验证。

## 观察者局 1836-04 的日志修复（2026-11-17）

日志副本：工作台 `reports/2026-11-17-observer-1836/logs/`（对应部署 `19c34683`）。改前备份 `backups/pre-change-observer-fixes-20261117`。

本任务造成、已修：
- `nesnd_crisis_effects.txt`：创建博弈的块内不能写 `if`（引擎报 Unexpected token，49 行）。改为博弈建成后立即在博弈作用域里逐国加入支持者，位置在易代之前。
- `script_values/nesnd_south_tilt.txt`：科举投票制是财产投票的变体，`has_law_or_variant = law_wealth_voting` 对它为真，开局选举法一项被算成 −1（蜀楚淮与吕宋）。改为先按本键判断科举投票制；宅地法是自耕农所有制的变体，改用 `has_law`（原报错 81 次）。提示用的自定义本地化同改。
- `nesnd_south_tilt.1` 等十六个事件加默认选项；「图穷匕见」四个选项加默认。
- 日志 `nesnd_south_allegiance` 补 `activation_description`。
- `00_subject_relationships.txt`：删掉柬埔寨的 `add_liberty_desire`（它原来的宗主关系已删）。
- 吕宋财政第一条路线原先要求旧的政治协定，协定删除后永远不成立。`nesnd_phi_political_accord_valid` 改为“吕宋的天平与朝廷站在同一侧”。

不属本任务、未动：
- `nesnd_jingnan_aid.txt:296` 的 `quantity = scope:nesnd_jingnan_reparation` 解析失败（域外介入）。
- 登莱共和国重复添加 `nesnd_sha_gold_alliance`；缺纹章贴图 `ce_Aoi_mon.dds`；`MISSING_DLC_ENTRY`、`1.15` 版本解析、`banks_enabled` 等游戏规则引用失败（各 243 次，同一来源）；蜀的华南司令部无港口。
- 旧协定变量仍有读取（`nesnd_south_accord_active` 等，在战后一侧的触发器里，恒为否）。

## 日志修复第二轮（2026-11-17，观察者局跑到 1844 年后的日志）

日志副本 `reports/2026-11-17-observer-1836/logs2/`。作者要求：能修的都修。

- `ce_canals.txt`：`REPLACE:` 覆盖原版四个运河日志，六处移除勘测修正前先判断修正是否存在（打开大吴日志页时每帧报错，11 秒 2128 条）。
- 南洋宣慰司是殖民地类型国家，傀儡国不接受这种类型，引擎报“无法维持”。改为 `colony`（一级自主，可升自治领）。战后奖励与遣使对象同步认 `subject_type_colony`。
- 吕宋改傀儡国后，原版规定傀儡国不能有属国，吕宋对马京达瑙、苏禄的关系被引擎断开。`REPLACE:subject_type_puppet`，只把 `can_have_subjects` 改为 yes。
- 本地化 105 处：方括号表达式里的 `'$key$'` 补成 `'$key|q$'`。
- 十四种日志被同一刻重复添加（西秦六个、登莱三个、外部方针、鸦片、印度两个、丰臣朝鲜）：15 处添加改为先查是否已有、并用一个三天的变量挡住同一刻的第二次调用。
- `nesnd_rep_warning`、`nesnd_yan_warning` 补 `activation_description`。
- `je_nesnd_opium_recovery_goal` 被引擎当作多余的目标文字：改名 `je_nesnd_opium_recovery_target_tt`，引用同改。
- `exiles_events_02.txt`：没有利益集团的人物不再被设为领袖。
- 补 `lens_toolbar_icons/nesnd_sha_mediate.dds`（用原版 offer_recognition 图标）。
- `ce_rivalries.txt`：去掉引擎每次开局都断开的美国对吴的宿敌关系。
- 赔款条约数额改为分档的固定数字（`nesnd_jingnan_aid.txt`）。

MOD 改不了或没有改的：
- 读旧存档产生的三组（规则引用、`MISSING_DLC_ENTRY`、版本号解析）。
- `ce_Aoi_mon.dds`：来自创意工坊 MOD 2893069455 的纹章文件。
- `gui/ingame_hud.gui` 的两条：来自 Console Access。
- 原版文件里的报错：`00_ai_triggers.txt:1304/1313`、`peru_bolivia.txt`、`ig_revolutions.txt:533`、`00_victoria_scripted_effects.txt:4887` 的循环上限、地图港口与后处理体积、列表面板缺失。
- “变量设了没用／用了没设”与孤立事件的提示（约 216 条），司令部无港口，重复贴图与模型（与 EACR 同名）。

## 僵局定局与“三省都不在”（2026-11-17）

- 核实：僵局定局在新流程下锁定前、战后都不会出现。作者确认一国可同时处在多个博弈中，内战博弈不会建不起来，所以“开战失败”这一角落也不存在。僵局定局的件（按钮 `nesnd_south_inconclusive_order`、事件 `nesnd_court_followup.19`、计时）保留但实际不会触发。
- 修复：锁定时蜀、楚、淮都已不在（无人起兵、也没有仍为属国的三省之一），按朝廷站队直接收场：忠于明室走 `nesnd_south_peace_ming`，追随郑氏走 `nesnd_south_peace_wu`（`nesnd_tilt_no_rebel_left`，`nesnd_south_resolve`）。开战脚本找不到起兵方时同样处理，不再调用旧事件 `usm_civilwar.3`（它会撤销易代，或让南朝永不定局）。`usm_civilwar.3`、`nesnd_ming_court.9`、`.10` 因此不再被触发。

## 观察者局 1836–1841 存档核查（2026-11-17）

存档：`观察者_1836_02_21`、autosave 1839.7.1 / 1840.1.1 / 1841.1.1、`大吴_1841_10_15`。这一局加载的是部署 `2767128b`。

- 南朝没有和平收场：1839.7 锁定，三省起兵（fate 1），吴已易代，内战博弈到 1841.10 仍在；楚、淮在 1841.1 前已不存在。AI 朝廷开局选了忠于明室。改制承诺只有 28/1000。
- 但 18 个海外属国在锁定时直接独立（fate 4），吕宋、远南、南洋宣慰司、琅勃拉邦中立（fate 5），没有一家拥吴。
- 原因：每个属国的天平进度条都从 0 开始。日志 `immediate` 里给进度条设起点的那一句没有生效，入册时的起点（三省 −30、海外 11–27）全部丢失。海外属国从 0 起步，在忠于明室的朝廷下被事件和安抚推到 −15～−26，进了拥明区，于是在「图穷匕见」里选了独立。
- 修复：入册时另存起点 `nesnd_tilt_start`；属国第一次月度同步时（吴的易代月数 ≤ 2）用 `je:nesnd_south_allegiance` 把起点写进进度条，并记 `nesnd_tilt_seeded`。已开局的存档不受影响。之前所有模拟都假设起点生效，模拟结论不变；实机此前从未按设计起步。

## 战后没有出现等级制度与「礼法之下的生活」；海外独立改为开战（2026-11-17）

存档核查（Rakaly 解码 `大吴_1841_10_15`，副本在工作台 `reports/2026-11-17-observer-1836/saves/`）：
- 内战博弈 1839.7.11 开战，吴的吞并目标在 1841.10.12 以蜀投降执行，蜀已无州。作者截图（1841.1、1841.2）时内战仍在进行，所以那时没有等级制度和日志是对的。存档里 1841.10.15 尚未定局（`nesnd_south_settled` 不存在）；战后的每周检查要下一次周脉冲才会定局，没有更晚的存档可以确认。
- 已结束的博弈会在存档里留一段时间（无战争、升级 100）。`nesnd_south_named_play` 改为只认进行中的博弈，以免它挡住战后定局。
- 博弈的发起方目标由博弈类型的 `war_goal` 自动加上（同一存档里内战的吴方吞并目标 `initial_war_goal=yes`，脚本里没有写 `add_war_goal`）。

海外独立改为开战（作者要求）：
- 新效果 `nesnd_south_secession_war`：属国先独立，朝廷随即开战。海外属国：朝廷要求重新附庸（原傀儡或殖民地还原为傀儡，其余为自治领；新战争目标 `wg_nesnd_usm_resubjugate`、`_puppet`，原版 make_dominion 去掉 requires_interest），独立方要求羞辱朝廷。三省在和平收场时自理国政：朝廷要求吞并（`dp_nesnd_order_unification`），三省要求羞辱朝廷。内战收场时三省自理国政仍直接独立。
- 新博弈类型 `dp_nesnd_south_resubjugation`、`_puppet`，取代 `dp_nesnd_southern_independence` 的用法。
- 通牒拒绝后的战争补上省一方的目标（羞辱）。
- 全 MOD 的单边博弈补防守方目标（羞辱）：`nesnd_acw_slavery_question`、`nesnd_jp_foreign`、`nesnd_europe_america`、`nesnd_per_rising` 两处、`usm_civilwar_events` 的东洋领事府。

## 第二次靖难：继位路径、三藩事件、日本单独开战（2026-11-17，部署 `3217c1ee`）

证据：工作台 `reports/2026-11-17-japan-war/`（1839.10–1840.10 六个存档的 Rakaly 明文、当局日志、`scan.py` 国家／协定／战争扫描、`toolkit*/` 检查结果）。第 1–6 项全部 STATIC_PASS，未实机验证。

1. 继位路径缺「镇压叛乱」。作者要求：大吴开战后必须拿到 `ce_usm_suppress_rebellion`，否则战后的吴胜判定和等级制度都不会发。原因：改制压力满额后 `nesnd_south_tilt` 直接调 `nesnd_open_southern_war`，绕过了发 JE 的 `usm_civilwar.2`。改法：开战成功后，吴尚无该 JE 时补发 `usm_civilwar.2`（`common/scripted_effects/nesnd_south_tilt.txt`）。
2. 三藩收不到 `usm_civilwar.2`。同日把 `nesnd_jingnan_may_receive_rebel_journal` 改成 `var:nesnd_jingnan_locked_play = { is_war = yes }` 加 `has_war_with`，游戏里三藩都没收到事件。改回遍历战争：本国在防守方，且战争属于 `nesnd_south_named_play`（`common/scripted_triggers/nesnd_south_holdouts.txt`，与 `nesnd_south_capital_defeat` 同写法）。旧写法实机有效，改回后只做过静态检查。
3. 日本反吴单开「东征日本」。作者要求：日本反吴时不进大陆总博弈，单独与吴打，当场转为战争；结果照原有钩子写进「东洋之议」。改法：
   - `nesnd_call_jingnan_participant` 对反吴的 JAP 分流到新效果 `nesnd_open_japan_jingnan_war`，原逻辑移到 `nesnd_call_jingnan_participant_inner`（`common/scripted_effects/nesnd_crisis_effects.txt`）。
   - 新效果调用现有的 `nesnd_japan_create_eastern_intervention` 建 `dp_nesnd_eastern_intervention`，加变量 `nesnd_jingnan_japan_play`，`set_war = yes`。带该变量的博弈算作 `nesnd_south_named_play`。
   - `dp_nesnd_eastern_intervention` 的 `on_war_begins` 加 `nesnd_muster_jingnan_war`（`common/diplomatic_plays/nesnd_japan.txt`）。
   - `dp_usm_civil_war` 的 `additional_involvement_trigger` 禁止反吴的 JAP 加入（`common/diplomatic_plays/ce_diplomatic_plays.txt`）；开战时 JAP 不作为总博弈支持国（`nesnd_crisis_effects.txt` 开战块）。
   - 战争结果走原有钩子 `nesnd_eastern_hostilities_ended`、`nesnd_eastern_military_loss`、`nesnd_japan_war_started`。
   - 上一会话只用 grep 时另造了一个对日博弈，已删。
4. 大陆打完就结算，日本另算。作者要求：日本那场战争不拖住大陆的定局。改法：`nesnd_south_campaign_holdout` 删 JAP 分支；`nesnd_south_campaign_peace` 忽略带 `nesnd_jingnan_japan_play` 的战争与博弈；`nesnd_south_defeat_resolution_pending` 去掉日本复国分支（`common/scripted_triggers/nesnd_war_collapse.txt`）；「镇压叛乱」完成条件（`common/journal_entries/ce_usm_the_last_days_of_ming.txt`）、`nesnd_south_wu_total_victory`、`nesnd_south_holdout_wu_tick` 判吴胜时排除 JAP。
5. 南朝诸国面板中日本一行。锁定前显示「开战前表态」，选过或答复后显示「助吴 / 反吴 / 中立」（`common/customizable_localization/nesnd_succession_board.txt`，`nesnd_south_politics` 本地化）。
6. 新日本日志「外藩去从」`nesnd_jp_jingnan_stance`。作者要求：玩家日本在锁定前可预先表态，锁定时的 `usm_civilwar.23` 只给所选一项；战后分不分裂仍由大吴在「东洋之议」里定。改法：三个按钮（谋求独立 = 反吴，表态臣服 = 助吴，不卷入 = 中立），选择存 `var:nesnd_jp_jingnan_choice`（1 反吴、2 助吴、3 中立），每次选择后冷却 12 个月，AI 权重 0。文件：`common/journal_entries/nesnd_jp_jingnan_stance.txt`、`common/scripted_buttons/nesnd_jp_jingnan_stance.txt`、`events/usm_civilwar_events.txt`；中英文本地化在 `localization/*/replace/nesnd_japan_l_*.yml` 末尾。

已知风险：
- `nesnd_japan_create_eastern_intervention` 要求日本统治者出自三家、日本完整拥有关东、京都、关西、中国四地。不满足时博弈开不起来，日本就不会与吴开战。
- 日本战胜吴时日本保持独立，大陆照常结算。
- `nesnd_south_campaign_peace` 第 84 行 `NOT = { is_diplomatic_play_type = … has_variable = … }` 内有两个条件。引擎文档只写“negates content”，未写多条件时是“非且”还是“都不”。按“都不”理解时，它还会忽略吴发起的、未带标记的其他东征博弈。推断，未核实；未改。

## 观察者局易代压力停在 91（2026-11-17）

作者截图：1842.5.23，朝廷忠于明室，易代压力 91/100，月进度为零；改制承诺 84.5。这局 18:49 启动，加载的是部署 `1533ad4c`（早于第 1–6 项的 `3217c1ee`），`nesnd_south_tilt_month` 两版相同。

存档（工作台 `reports/2026-11-17-pressure-stall/saves/autosave_1842_melted.v3`，1842.4.1）中吴的变量：`nesnd_tilt_month` 75，`nesnd_tilt_events_done` 25，`nesnd_south_pressure_extra` −9，`usm_conflicts_within_tracker` 91，`nesnd_pledge_milli` 840；首辅案已结（`nesnd_assassination_resolved`）。

原因：压力每月重算为“事件数 × 4 + 额外值”。事件数在第 42 个月封顶 25（即 100），此后不再增加。朝中事件 `nesnd_usm_court.1`–`.3` 的减压选项记进额外值（同日为让首辅案加压生效而加的写法），额外值为负时压力永远到不了 100。此前朝中事件的增减下月即被冲掉，所以不会卡住。这一局实际会以改制承诺满额收场（明室不战而胜），不会内战。

修法（作者 2026-11-17 选“事件时钟继续走”，部署 `43e6b322`）：
- `nesnd_south_tilt_month`：第 42 个月以后，事件数改为按原进度计算，即“月数 × 24 ÷ 42，取整后 +1，至少 25”，不再停在 25。之后约每 1.75 个月加 4 点压力，不发事件。朝中事件减掉的压力只推迟锁定。
- 「朝争进展」悬停 `nesnd_south_pressure_detail_tt` 中英各加一句：朝中事件增减的压力一直计入，到期未满时照同样的进度继续上涨，直到满 100。
- 检查：`script_xcheck.py`、`static_lints.py`（bom、locsv、tipctx 均 0）、`toolkit_check.py`（3 个文件，0 条诊断）、`cliche_check.py`（0 条）。报告在工作台 `reports/2026-11-17-pressure-stall/`。STATIC_PASS。
- 读这局 1842 年的存档：下一次月结时事件数算作 43，压力满 100，随即锁定立场。新开局下，朝中事件为负时锁定会晚几个月。

## 复测局崩溃：1839.4.1 靖难开战后（2026-11-17）

证据：工作台 `reports/2026-11-17-jingnan-crash/`（`logs/` 整组、`crash/` 的 exception.txt 与 minidump、`saves/` 五个自动存档，其中 1839.1.1 与 1839.4.1 已解码，`scan_out.txt`）。游戏 19:28 启动，加载部署 `43e6b322`。崩溃在 1839.4.1.6，访问冲突，堆栈无符号。

已查明的缺陷（崩溃原因的首要嫌疑，推断，未核实）：
- 1839.3.13 日本反吴，`nesnd_open_japan_jingnan_war` 开出「东征日本」并当场开战（war 17：吴、文莱、马辰、占碑对日本）。日本此时仍是吴的朝贡国。`is_subject = no` 对朝贡国为真，这道保护没有拦住。原有入口 `nesnd_japan_launch_intervention` 会先让日本独立，新入口跳过了这一步。
- 目标有效性 `nesnd_eastern_target_valid` 把“已开战而日本仍是吴的属国”当作日本已臣服。吴的两个「重组日本诸藩」目标在 1839.4.1 存档里都是 `status=discarded`，这场战争里吴没有任何有效目标，只剩日本的羞辱目标。
- 同一博弈上有两个「重组日本诸藩」：博弈类型自带一个（`initial_war_goal=yes`），`nesnd_japan_create_eastern_intervention` 又加一个。原入口同样如此。
- 上一局日本作为朝贡国加入大陆总博弈打到 1840.10，没有崩溃，所以“属国与宗主交战”本身不是原因。新出现的是吴方目标全部失效的东征战争。

同局其他日志问题（未改）：
- `nesnd_crisis_effects.txt:167` `this ?= scope:….var:nesnd_joined_south_play` 报 Invalid right side（北朝介入加入博弈，1839.3.13）。
- `nesnd_wu_resolve_bar_rules_tt` 里的 `SCOPE.sCountry('nesnd_label_cne')` 在悬停中拿不到作用域，崩溃同一秒连报。
- 大吴重复添加「未息的南朝战事」、日本重复添加五个日志：`has_journal_entry` 对未激活的日志为否，只是报错，无害。

复测项（1839.4.1 存档）：
- 大吴有「镇压叛乱」；蜀、楚、淮和日本都有 `have_seen_dierci_jingnan`（`usm_civilwar.2` 设置），三藩收到了事件。ENGINE_VERIFIED。
- 日本另开「东征日本」并当场开战：开了，但吴的目标当场失效（见上）。大陆停战后是否继续、等级制度、「幕府危局」存续：崩溃前未到。「幕府危局」`nesnd_japan_war_collapse` 已建立。
- 「外藩去从」按钮与冷却：观察者局 AI 不按，未测。面板日本一行：存档里看不到，未测。

修复（作者 2026-11-17：“就算不符合，也强制日本独立并开战，只要对方是日本／日本主流文化就行。否则切断这条线，只让他独立并获得江户、京都、四国的宣称。”部署 `a1d6a6e0`，改前备份 `backups/pre-change-update-20261117T194932Z`）：
- `nesnd_open_japan_jingnan_war`（`nesnd_crisis_effects.txt`）：日本是任何国家的属国或吴的直属属国（含朝贡国）时先 `make_independent`。日本主体文化含大和（`cu:japanese`）时，吴记 `nesnd_jingnan_japan_forced`，开「东征日本」并当场开战，不看分封条件。否则不开战，日本得关东、京都、四国三州宣称。
- `nesnd_eastern_reorganization_valid`（`scripted_triggers/nesnd_japan.txt`）：吴有 `nesnd_jingnan_japan_forced` 时，只要日本存在且不是吴的属国，吴的目标就有效。兑现时 `nesnd_partition_japan` 仍自查分封条件，不满足则不分封。
- `dp_nesnd_eastern_intervention` 战争结束时移除该变量。
- `nesnd_japan_create_eastern_intervention` 删去吴方的第二个「重组日本诸藩」（博弈类型自带一个）。原有东征入口同样只剩一个。
- 检查：`script_xcheck.py`（3 条未知键均为原有参数写法）、`static_lints.py`（bom、anyeq、deadhook）、`toolkit_check.py`（4 个文件 0 条诊断）。v3tree 已按部署重建索引，查过 `nesnd_open_japan_jingnan_war`、`wg_nesnd_japan_reorganization`、`nesnd_eastern_reorganization_valid`、`nesnd_partition_japan` 的上下游。STATIC_PASS。崩溃是否由此引起仍待新开局验证。
