# NESND 当前状态

这是项目唯一的“当前”入口。只写现在的情况；历史放 `docs/agents/history/`。维护规则见文末。

更新于 2026-11-19。当前跟进法国后继内容和登莱原生路线。此前收口的任务中，已交付的标 completed，未实施的任务 08 原始欠账、南朝立场 01–07 标 rejected。

## 基线

- 游戏：Victoria 3 **1.15.2 Ivan-Chai / Steam build 26763837**。上一基线 1.15.1 / 26591675。2026-11-19 [1.15.2 迁移](../../.scratch/migration-1152/issues/01-migrate.md)：机制改动三方合并，开局数据不跟原版（作者定），开局贸易全部注释，俄国「东部边界」日志停用，两个被移除的键与厄勒海峡像素已处理。STATIC_PASS，待作者新开局复测（报告在工作台 `reports/2026-11-19-game-1.15.2/迁移报告-1.15.2.md`）。
- Git：2026-11-14 起 Git 仓库就在源目录里（main `737a81b` 时迁入）。MOD 文件夹由部署脚本从源目录生成；工作台 `projects/nesnd-repository` 与同步工具 `sync_main_mod_to_repo.py` 停用。
- metadata 版本 0.2.0，声明支持 1.15.2。

## 位置

| 名称 | 路径 | 说明 |
|---|---|---|
| 源目录 | `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-source` | MOD 全部内容与 Git，唯一工作位置 |
| MOD 文件夹 | `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties` | 部署产物，游戏加载目录；不得直接修改 |
| 部署脚本 | 源目录 `deploy.bat`（实现与白名单在 `deploy/`） | 部署、预览、检查；记录在源目录 `update_record.json` |
| 远端 | `github.com/EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties` | 代理用分支，作者合并 |
| 工作台 | `…/Victoria 3/nesnd-workbench` | 工具、备份、报告、原版基线 |
| 技能 | `C:/Users/Eric Liu/.codex/skills/nesnd-victoria3`（其余技能在 `skills/` 下） | 独立的 Git 仓库，说明见其中的 `AGENTS.md`；2026-11-14 前的技能历史在本仓库 `development/` 的 Git 记录中 |
| 任务账 | `.scratch/debug-release/issues/NN-*.md`，索引 `map.md` | 每项任务的细节与证据 |
| 作者原作 | Git tag `original-20261030`（`f18b6c4`） | 风格与设计的样本 |

## 未完成

印度线 2026-11-22 [收尾](../../.scratch/india-missions/issues/09-closing.md)，已关闭。任务 [01](../../.scratch/india-missions/issues/01-aid-for-concessions.md)–[08](../../.scratch/india-missions/issues/08-overseas.md)：使团请求与外援、土邦开局、本地项目、不丹尼泊尔与莫卧儿的条约、土邦加入、中央与各邦、莫卧儿三件事、海外通商。运行文件按组合并，每个文件夹至多五个 `nesnd_india_<组>.txt`：core（身份、月度刷新、改革与社会日志）、matters（「印度事务」答复层）、princes（使团请求、本地项目、加入、南方起义）、empire（中央与各邦、莫卧儿的旧约、王公会议、饥荒）、foreign（不丹尼泊尔条约、海外通商）；事件 `events/nesnd_india_{princes,empire,foreign}.txt`，本地化 `nesnd_india_<组>_l_*.yml` 中英各五个。不合并：common/history、`00_indian_removal.txt`、`nesnd_india_native_overrides.txt`、起义国的国家与旗帜定义、gfx。03–08 的待实机项已全部按代码核验，结论写在各任务文件。2026-11-22 [修复08](../../.scratch/india-missions/issues/10-fix-review.md) 按整体复核与逐月模拟修了四组问题：开局给莫卧儿自有市场（不丹、尼泊尔的已在[修复10](../../.scratch/india-missions/issues/12-fix-10.md)按作者要求撤掉）；「与宗主国的旧约」按宗主国首都是否在印度判定，开局即有；条约港不设期限；新秩序比例只算首都在印度的国家所持的州；年金上限 6 份；续约付一半。同日[修复09](../../.scratch/india-missions/issues/11-fix-09.md)：新秩序比例再去掉宗主国首都不在印度的附属国所持的州；饥荒求援排队至多 90 日；莫卧儿开局的自有市场会被宗主国按原版规则收回，文字已写明。以后只加新内容；日志与本地化直接改文件，工作台旧的生成脚本不再运行。STATIC_PASS。

2026-11-18 [东征日本吴方目标作废](../../.scratch/debug-release/issues/111-japan-reorganization-goal-kept.md)：「重组日本诸藩」有效条件只剩吴对存活的日本；去掉引擎的 country_creation 设置（推断它让目标一开战即作废）；兑现按京都、关东、中国、九州四国逐项分封。部署 `ab24288d`，STATIC_PASS，待新开局两入口复测。

2026-11-18 [日志专属图标](../../.scratch/journal-icons/issues/01-design.md)：156 个 MOD 日志的图标设计分 8 批，每批一份 Codex 画图提示词（工作台 `reports/2026-11-18-journal-icons/codex-journal-icons-batchN.txt`）。尚未画图，未接入。批次拆分、几处国家符号和地权革命原作子目标是否补回，待作者决定。

2026-11-18 [自建国家的本国公司](../../.scratch/national-companies/issues/01-design.md)：19 家公司、4 个特许事件、1 个日志、7 名经理、16 种名贵商品，部署 `a6699181`，STATIC_PASS，未实机验证。图标暂用原版，画图提示词在工作台 `reports/2026-11-18-national-companies/codex-icon-prompt.md`。

2026-11-17 波兰线三批已部署 5dc18f1c。根日志及朝圣者地图解析、九个默认选项与四个结局已修（[修复记录](../../.scratch/poland-redesign/issues/04-ending-repair.md)）。[第三批](../../.scratch/poland-redesign/issues/05-windows-congress.md)已接入五个危机窗口、法国与瓜分国选项、战后和会、两项议程表决、守约与否决、原创会议图。STATIC_PASS，未启动游戏，待新局验收。 [八枚日志图标](../../.scratch/poland-redesign/issues/06-journal-icons.md)已部署 7872679d，重启读档可看。 [波兰朝圣者逐批迁移](../../.scratch/poland-redesign/issues/07-single-journey.md)已部署 914bcc27，STATIC_PASS，待重启读档复测。 [大陆会议回执与公开条件](../../.scratch/poland-redesign/issues/08-public-tooltips.md)已部署 8b9f06e3，STATIC_PASS，待复测。

2026-11-17 [西岸的砝码十州目标](../../.scratch/acw-slavery/issues/01-west-ten-claims.md)：修复共同分州造宣称立即完成。十州经领土要求取得并持有后完成，两项自动化独立开关，内战及战后继续索地。文案按技能四轮复核，55对中修改36对，STATIC_PASS。最终文案已包含于部署752609ec65fbedbd0145378c185c459c，待作者新开局复测交地与分州合并回调。

2026-11-16 [靖难战争南线](../../.scratch/debug-release/issues/110-jingnan-southern-front.md)：吴借中南半岛 dominion 自动参战，从缅甸、老挝北上，蜀国「成都的去从」因云南先失而早于楚、淮亡国出现。新增战斗条件「瘴疠山路」（吴方在内战中进攻滇黔、川南、广西山地时进攻 −25%、士气损失 +25%、伤亡 +20%，内战外不出现）。游戏外检查通过，已部署 `b5273335`，未实机验证，待作者新开局观察者复测。附属国转为不参战（A）按作者选的日志按钮入口实施：「南朝诸国」加「遣使南疆」，答复、回报、吴胜后清算四个事件，其余数值用方案默认值（工作台 `reports/2026-11-16-xifu-southern-front/A-design.md`），同样未实机验证，部署 `bbab5753`。

2026-11-17 [西秦「边疆诸部」与波斯忠心](../../.scratch/qin-frontier/issues/01-frontier-risings.md)。同一观察者局的 1850 年 10 月档中，团结度 31.10，草原运动激进度 76.60%，已开始筹备分离。地区方案及西秦补贴已实施。旧解体条件、重复加入和分离认领、战果结算已修并部署 `fdaa7f43`，待新开局验证战果。[专项交付](../../../nesnd-workbench/reports/2026-11-17-qe1-stability-audit/diagnosis.md)

2026-11-16 [地权革命 AI 提前结束；复燕燕旗新增两项](../../.scratch/debug-release/issues/109-cne-reform-ai-and-yan-banner.md)：观察者局中华帝国 1840-04 政变成功，母日志按失败结局结束，子日志随之失效（旧局是「议止」冻结）。AI 改为只在改革濒临失败时议止，将领忠诚低于 25 或政变中关停营产，自耕农法权重不再限 96 个月。燕旗加「失去首都苦兀」−5、「底层困苦」每州 +0.5。游戏外检查通过，已部署 `80e7ddf9`，待作者新开局复测。−5 按作者决定保留（失去首都即停滞）。「做出让步」改为在「宫廷力量」「执政者与派系」「统治者与内阁」下都可用，部署 `73e6a716`，可读档复测。

2026-11-16 [「承认和人为国人」主流文化链接报错](../../.scratch/debug-release/issues/108-primary-culture-concept-link.md)：改用原版概念 `concept_primary_cultures`，两种语言。新扫描工具 `nesnd-workbench/tools/loc_link_check.py` 查出「统治者与内阁」事件 30 处 `SCOPE.sInterestGroup`，已按原版改为 `gsInterestGroup`。改后扫描 0 条。游戏外检查通过，待作者读档复测。

2026-11-15 [长江十州合入源目录](../../.scratch/yangtze-merge/issues/01-merge.md)：外审版 `yangtze-ten-nanjing` 按文件三方合并进源目录（29 个取外审版、4 个合并、15 个新增），主线另改的 144 个文件保持不动。江面三段、两关、三渡、原生 Repack 高度文件、十州人口建筑与城镇交通均已在源目录副本上复核。部署白名单加了 `map_data` 的图片与 `default.map`、`adjacencies.csv`。游戏外检查通过，已部署 `6e1eafbd`。观察者局报出的落水要塞定位点和邻接表末尾空行已修，部署 `c84bc423`，待作者用 `yangtze-ten-formal-play` 存档目录开新局复测。46 个占位名提案未动。

2026-11-15 [选国界面「特有日志条目」](../../.scratch/debug-release/issues/106-lobby-journal-entries.md)：补波兰问题的列表描述，地权革命、教派消长及 25 个主要国别日志加入列表，共 30 条中英描述，按作者样本重写，国名改用开局全局变量显示。全 MOD 日志正文中的代理腔也已清理（作者稿保留）。游戏外检查通过，各条已点出所属国，外国叙述已去掉汉地旧式名词，已部署 `90707c71`，待作者在选国界面和日志里复测，重点看国名是否正常显示。

2026-11-15 [新日志「统治者与内阁」](../../.scratch/premier/issues/01-implement.md)：给不能任命宠臣的非共和帝国（多为立宪君主国）。首相由角色互动任命，按人气缩放立法速度与合法性。平衡是首相集团对最大在野集团，所有集团都入阁时改为对其余各派。政府改组后首相集团出阁时，由政府内最大集团的领袖接任。与「宫廷力量」「执政者与派系」互斥，只改了 `nesnd_palace_shown` 一行。游戏外检查通过，已部署 `c3e2f208`（人气条为摇摆条，按钮扣人气当场刷新），待作者复测（英国）。

2026-11-14 [公民工程日志 `war` 无效对象报错](../../.scratch/debug-release/issues/102-civic-theatre-war-link.md)：战区和平检查先判断 `is_at_war`，`war` 链接先判断存在，判定结果不变。`TRIGGER_MARKET_ACCESS_GREATER_OR_EQUAL_THIRD` 是原版本地化缺陷，未改。游戏外检查通过，已部署 `0fc4bf0b`，待作者复测。

2026-11-14 [「资助燕人会党」改为随机一处 +3% 激进派](../../.scratch/debug-release/issues/103-yan-subsidy-effect.md)：查明时关系 −30，提示同步。游戏外检查通过，已部署 `0fc4bf0b`，可读档复测。部署脚本改为游戏运行时只提示不停止。

2026-11-14 [「资助燕人会党」通知中华帝国，东北七州迁入吸引力 +5%](../../.scratch/debug-release/issues/104-yan-unrest-event-dongbei-trait.md)：未被查明时中华帝国收到【不满在东北积蓄】，激进派改由该事件添加，被查明时只降关系。新州特性「东北垦荒」。游戏外检查通过，已部署 `9fe20a4e`，需新开局复测。

2026-11-14 [联合州事权目标 `has_law_or_variant` 报错](../../.scratch/debug-release/issues/105-keju-law-variant-check.md)：科举投票改用 `has_law` 检查。游戏外检查通过，已部署 `9fe20a4e`，可读档复测。

2026-11-14 [error.log 中本 MOD 的报错](../../.scratch/debug-release/issues/101-error-log-20261114.md)：登莱复燕与起事预警的状态行改用 ROOT，燕旗增减项改静态文字，修正 `concept_law` 链接，波斯远西日志改为自动激活。游戏外检查通过，已部署 `e3a55317`，待作者重启后看新日志并复测远西日志。

2026-11-14 [登莱「接济北朝共和党人」无限叠加激进](../../.scratch/debug-release/issues/100-sha-radicals-flood.md)：每次拨款改为两次各 5%，经费期满后冷却 6 个月，登莱为北朝附庸或盟友时禁用，AI 登莱在「渡海」中对北朝关系保持 −100。条款显示每周经费。游戏外检查通过，可读档复测。

2026-11-14 [原创中期人物审核](../../.scratch/midgame-characters/issues/01-duan-muzi-audit.md)：段敬川 .14／.200 不再因月检而连弹、重复扣款；牧沐子「沐子东渡」要求她仍在 CNE、且有别国持有加州。待答保护由 3 天改为 3 个月。第二轮按作者决定：出书时她所在国和另一方（CNE 或加州持有国）都得到奖励；1872 年前不死；1871 年后若已死亡或被流放，则重建或找回。游戏外检查通过，第二轮未部署，待作者复测。9 条中期丰富建议待作者决定。

2026-11-14 [AI 触发器改为按键 REPLACE](../../.scratch/ai-behavior/issues/01-ai-triggers-replace.md)：删去整文件覆盖的 `00_ai_triggers.txt`，新增 `ce_ai_triggers.txt`，只替换与原版不同的 4 个触发器。游戏外逐键比对与原覆盖一致，待新开局看 error.log。默认 AI 策略仍整文件覆盖。同日技能新增 AI 倾向参考 `references/ai-behavior.md`。

2026-11-14 [人物设计研究的复核与调整](../../.scratch/character-design/issues/01-research-review.md)：技能人物参考已拆为三份、只引原版和 NESND，已合入 Git main（`db9351d`）；内容树工具已合入其 main（`842ea65`）。修复分支 `fix/tooltip-concepts-observer-buttons` 已并入新 main（`bb62624`），技能三处冲突已解决，合入 main 时不再冲突。

2026-11-14 [共和军、复燕预警与南朝接纳和人决议](../../.scratch/rising-warnings/issues/01-cne-sha-usm.md)已完成游戏外检查。共和军和东燕各预警九十日。登莱逐州联络旧部，成功时给北朝送一件[任务 98 的呈报](../../.scratch/debug-release/issues/98-yan-rising-visibility.md)。八州词条已接入中英文本。待作者验收预警州份与开战、读档锁定、按钮成功和失败、原生内战的发起运动。

2026-11-14 [地权革命加入战争胜利、「再次击败共和主义者」与「做出让步」](../../.scratch/debug-release/issues/99-cne-concessions.md)已完成游戏外检查，待作者复测平叛事件、让步按钮与完成奖励的替换。

2026-11-14 [「帝国人民的信心」改为按月结算并加收支、民生两项，拨款按钮改按负债比例](../../.scratch/debug-release/issues/97-cne-confidence-monthly.md)已完成游戏外检查，已推送到分支 `fix/tooltip-concepts-observer-buttons`，待作者复测条面明细、名词解释与欠债拨款。

2026-11-14 [地权革命悬停丢失与全 MOD 无效概念链接](../../.scratch/debug-release/issues/96-invalid-concepts.md)已完成游戏外检查，待复测；同批给三角贸易按钮加了观察者模式下的空 root 守卫，待观察者模式实测。

[四类加载报错](../../.scratch/debug-release/issues/95-loading-errors.md)已完成游戏外检查。待新开局复测波斯规则、法国失效分支和两种中美洲文化修正。东亚服装重名来自原版与 EACR。

2026-11-12 [文化团结度日志的转化预告](../../.scratch/cohesion-display/issues/01-cohesion-display.md)：日本、西秦、唐衣大食三个日志的状态行显示下次月结的州、人数和文化方向。同时修了日本转化中可能静默失效的文化比较，西秦与唐衣大食的抽签提前一个月。2026-11-13 加统一结束：研究身份证件或采用委员会共和国、法团国家后三个日志永久结束，进行中的团结补贴随之停止。技能新增 `references/cohesion-journal.md`。游戏外检查通过，可读档复测。

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

2026-11-11 新增帝国级以上国家的常驻日志[「宫廷力量」与「执政者与派系」](../../.scratch/court-power/map.md)，连带给西秦「伊犁的朝议」加了朝争条与两个按钮，并在明吴明论战、法国维持拿破仑王朝的月度随机事件中各加 3 件宫廷事件。游戏外检查通过。[权力平衡支持度及国家能力](../../.scratch/court-power/issues/03-balance-approval.md)已完成游戏外检查。[22 张界面素材](../../.scratch/court-power/issues/02-art.md)已接入脚本与界面，待作者实测。2026-11-17 [同集团宠臣的对手改为其集团以外的最大集团](../../.scratch/court-power/issues/04-rival-outside-own-group.md)，部署 `fc01f573`，STATIC_PASS，待作者新开局复测（莫卧儿）。

2026-11-16 [第二次靖难的域外介入](../../.scratch/jingnan-intervention/issues/01-implement.md)：西秦、东洲可与中华帝国一样出兵反吴。反吴方胜时由胜者决定是否酬谢：中华帝国东路得苏北、滁州、合肥，西路得人情与投资、贸易条约，西秦得人情与贸易、过境条约，东洲得条约港（浙江，不成依次改福建、闽江、粤中）与贸易特权。吴胜时介入国付五年赔款，吴得汉中、皖北宣称，僵持时不给。大吴「平叛」日志加「军心」条，按敌方外国数缩放吴军四项。「统一南方」改为八处要地。游戏外检查通过，已部署 `dd61f45b`，待作者新开局实测条约是否成立、浙江条约港与军心读数。

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

2026-11-16 [南朝易代重做 · 第一批](../../.scratch/south-succession/issues/01-balance-core.md)：每个属国一条政治天平，易代压力满 100 时各国定下立场，同日易代、开战；另有两种不战而定的收场。旧的立场、协定和表态事件已断开。暹罗及其附属国改为吴的自治领。游戏外检查通过，待作者新开局复测。第二至四批（事件链、谋刺案重做、安抚与遣使、法律提示、战时修正、撤旧件）已连续实施并部署 `ee972086`。剩文字一批，正文键目前是占位。第五批文字已写入并部署 `8e5141a8`。收尾（渡边华山、吕宋驳回、真实税收、引文核对、遣使扩大、外战状态行、旧协定件清理、数值调整、承诺先满按站队结算）已部署 `a15e7a21`，模拟对上目标，仍未实机验证。2026-11-17 第二次靖难收尾已部署 `3217c1ee`，均未实机验证：继位路径补发「镇压叛乱」，三藩收事件的条件改回遍历战争，日本反吴单开「东征日本」并当场开战、不拖大陆结算，面板日本一行，日本新日志「外藩去从」。待作者新开局复测。同日观察者局（加载 `1533ad4c`）1842 年易代压力停在 91：事件数封顶 25 后，朝中事件记下的 −9 使压力永远到不了 100。已改为第 42 个月后事件数照原进度续涨，朝中减压只推迟锁定，悬停同步，部署 `43e6b322`，STATIC_PASS，可读该局 1842 年存档复测。复测局 1839.4.1 靖难开战后崩溃：「东征日本」在日本仍是朝贡国时开战，吴的目标当场失效（首要嫌疑，推断）。已改为先令日本独立，大和主体文化的日本一律开战，否则只给关东、京都、四国宣称，并删去重复目标，部署 `a1d6a6e0`，待新开局验证能否打过 1839 年 4 月。已确认：大吴拿到「镇压叛乱」，三藩收到 `usm_civilwar.2`。

[吴吞并日本后的三家分封](../../.scratch/debug-release/issues/100-japan-partition-after-annex.md)：吴在东洋之议以外取得日本会绕过分封。分封决议在日本被吞并或成为朝贡国以外的吴属国时可用（AI 权重 100，玩家自愿）。新增日志“东征”，吴占有九州以外的日本本土而日本尚存时，和平满 6 个月开吞并战，不许议和。发国书的 AI 权重提到 100，AI 的吴在战争中也可发国书。游戏外检查通过，待作者复测。

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
2026-11-17 [礼法之下的生活与等级制度](../../.scratch/south-order/issues/01-life-under-the-rites.md)：日志按内战、郑氏和平、明室和平分三个版本；和平版本完成后发通牒；内战胜方获得等级制度（大吴按文化，大明按职业），各四部法律。让权换取效忠改为每月 −1.5。游戏外检查通过，未实机验证。
2026-11-18 [吴明论战两条路线汇入同一内战入口与战后迎驾](../../.scratch/south-succession/issues/02-civil-war-routes.md)：明帝出逃不再按路线分叉，行在开战当天成立；大明联邦与行在并存时战后发一次「迎驾」。部署 `1587ec5b`，STATIC_PASS，待新开局复测。
