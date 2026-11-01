# 断点恢复后的主控实机记录

用户明确 resume；不要提问。版本1.13.11/build24799966，catalog CURRENT changed0。此前关闭进程的run003815冻结逐hash完整，正常游戏退出未证实，resume-integrity.json保留该边界。

## 原生女性发型对照（已观察）

- before：run20261101T012826Z，sequence A 532文件SHA3325ec418bf25fceef54cda480444e1ca739c0836c40c97af051c841bc7b1b5a，校验码8861。
- after：run20261101T013305Z，female-hair A 533文件SHA8794f72ab8dd92a34bbe39e48d39f6f6f2bbf5e1e95a9e1efed5c2ac4f05e156，校验码8861。
- 两次均 EACR→独立候选→QA A；读取run003815首日原生存档的逐字副本，SHAfba18150b6b8ba22e3e847cbde354b4cc6307a096f7ff52a4c8c709dc60c3ba5；游戏暂停，无日期推进。通过明确QA切国USM→CNE，政治→乡村民众→人物。
- 同一CNE_mu_muzi（旧档原生ID3124）修复前全秃，修复后完整女发/花饰出现；脸、衣服、年龄21、老秦/儒经及乡村民众领袖身份一致。乡村民众女群像也恢复。前后完整截图与JSON分别存两run/evidence/mu-muzi-before/after。
- before最终error165：较旧冷菜单156，多4条初版Lin无BOM、1条旧候选名载入警告、4条原版政治页FindChild动画null。after166：新增仅兼容hair文件缺BOM。均正常原生菜单退出，runtime程序退出0并存snapshot-integrity。
- B仅对兼容hair脚本加BOM，其他字节一致，AST相同，SHA2579d29090c8ee4356fc8172d3b977e2810e566087cbe2fd2714b0658efa1e77；B不冒用A整包实机通过。已独立checkpoint，等待综合新局复核。

## 综合运行（正在执行）

run20261101T014437Z，候选resumed-integrated-20261101-a，553文件SHA1f0c4f79024eb674d60b2d2cbc2b82e2e7fea56673a55caeb78eb2d421d4650d；冷菜单校验码995d。冻结副本exports/runtime-20261101T014437Z/mod；隔离profile同ID。EACR→候选→QA E（30文件），monthly autosave仅隔离设置。

共同父sequence A经逐文件SHA核实一致；整合Lin resume、hair B、六地区map、最新工程文档。各分支和综合branch已推Git并archive回算逐字匹配，见reports/git-resumed-candidates-20261101T014406Z/report.json；main工程资料提交670870a，综合candidate提交5edbdf6。主MOD玩法未覆盖。

统一global v2：13PASS/1FAIL/3NOT_RUN；唯一FAIL为Tiger分类债，新增Foochow同形原版奖励及旧Russia空if有独立源码证据，原报告保留。全部历史/人口/生产/几何/交通/MCP通过只是静态或协议证据。旧来源过期不批量清绿。

冷菜单181记录，较旧156多25，均待逐项记录QA分类；无BOM新告警。stages/cold-main-menu和cold-main-menu-audit保留原日志。原生点击新游戏→沙盒，当前等待国家选择。

新地图验收必须新局。预先复制两个旧档只为同人/部分转属回归，不能据此认证新州。新局先保存独立首日基线，再覆盖发型、12受改州、首都/港口/市场、航行与事件链；每个夹具分支从基线重载。QA E只改D的global战争旗观测，旧未选救援/legacy按钮隐藏，生产候选不含那些备选。

## 新局与日本原生结算（已观察，继续取证）

首日全新档为 `大明联邦_1836_01_01RESUME_A_NEW_1836_01_01.v3`，99,561,728bytes，SHA9b4de7f764cb5e1e28e77c5aea76337651dd69e24ffbb6390941d2c1819f9982，原生seed1873443562。存档输入框Ctrl+A未选中，因此新名追加到原默认名；保存前已见独立名称，旧seed档未覆盖。首日12州及全球国别地块清单全部匹配，人口/建筑股份/首都和实际交通对象通过初始化核验。QE1缺lathe导致4纺织等级仍用手缝，是旧原生版本已有fallback，不是拆州损失。市场百分比和舰队到达未据此判通过。

首日暂停切CNE、打开牧沐子完整肖像，BOM发型在综合新局通过；截图Jan1-new-baseline/mu-muzi-newgame.jpg。回USM，点击capture Lin与capture JAP people，再点击FIXTURE JAP DP。此夹具跳过继位/邀请，仅创建真实DP，恢复/分国/任命不由QA直接调用。

关闭一个短暂toast时，通知已经消失，点击误落到QA瑞典tag；立即收起瑞典事件，无选择选项，再明确tag JAP。该UI偏差在debug.log可核，不冒充纯默认玩家路径。JAP实际推进至1836.2.3暂停，诸府约章只收起未选任何条款。退让前原生档`丰臣幕府_1836_02_03.v3`111,746,776bytes，SHA10861e1b94b710518e25187ef4936f570ca095e63c530082b07a3683f8d5c69c；DP5/目标10为USM730吞并JAP17，尚无war record。林3153仍USM；原JAP储君3447已经退位，当前新储君6892在吞并前即存在，不能把它误报为此次摄政复制。

原生博弈让步→是，1836.2.3出现“游戏结束／你已被吞并”，截图Feb3-native-backdown/game-over.jpg。手动点击内置“作为观察者继续”，走时实际至1836.3.12后暂停（UI观察间引擎推进，未将其描述为只过两天）。世界恢复三政权。observer无国家下点QA sequence probe导致一条测试root无效错误；随后手动观察USM、toggle observe退出观察，真实ROOT有效后probe输出REALM_READY、LIN_COMPLETED、LIN_ACTUAL_JAP_RULER、LIN_REGENCY_ACTIVE YES。手动tag JAP检查政治，实际显示“摄政政府／摄政王 林汉涵”，截图Mar12-native-Lin-regency/lin-regency-government.jpg。

结果原生档 `桑国_1836_03_12.v3`116,594,357bytes，02:16:12UTC保存完成。当前游戏停在菜单、日期Mar12暂停，准备实际重载该档再验证人物/职务持久，之后回Jan1新档做陈链与交通。新档同ID/主从/领土具体审计由代理继续落盘。

运行新增需独立分类：02:01:27 GameStateAccess assertion发生于诸府约章弹窗期间；02:09:54两条当前GAME Peru-Bolivia add_involved_country重复；02:11:01无国家observer下QA sequence root无效。均保留原日志，不泛化无BUG或隐藏。原生恢复/旧人物predicate在debug缓冲内，提取时核完整落盘记录。
