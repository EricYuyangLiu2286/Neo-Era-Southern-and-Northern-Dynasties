# 印度实施合同：有效基线、原版链条与最小完整模块

2026-11-03。SOURCE_AUDIT / IMPLEMENTATION_CONTRACT / ENGINE_NOT_RUN。本轮只读主 MOD（M）与 GAME（G），仅在 WORK（W）写本报告及来源指纹；未改主 MOD、未改候选、未启动游戏。`catalog.py status`：1.13.11 / Steam build 24799966，CURRENT，changed_count=0。

本报告将已批准的印度方案修订2与 L01–L24 生命周期落到可实施边界，不删减原范围。远山与天竺宣慰司的定名、TAG、政体和所属地区以并行原稿研究为准，本报告只给它们必须接入的原生创建／继承／治理合同。正文中新 `nesnd_india_*` 名均为建议接口，并非当前已有代码。计划依据：[W/plans/two-empires/20261102-india-development-design.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:1>)、[W/plans/two-empires/20261102-japan-india-lifecycle.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-japan-india-lifecycle.md:1>)。

## 1. 立即可执行的范围与次序

一次实施可分六个独立核验闭包；每批都有实际可玩的结束，不以“添加一批空日志”代替内容。

1. **有效开局与兼容**：统一 MUG 国家／人物加载；处理不合用的英国公司；显式记录现有军队基线并按帝国范围配置合理编制；停用旧英属印度核心链。人口、原有产业、领土和外国投资不改。运行时迁移只补阶段记录，不重新生成历史人物或军队。
2. **行政改革与本邦议程**：MUG 主 JE＋学校官署／工场军队分阶段子 JE；43个有组织地方国家共用一个主权与发展 JE，独立／属国分路。USM 印度治理 JE 只作用于本国指定印度州。
3. **法国合作**：一套即时政体分类、一套有序号的双边请求，教育／产业／军官项目有不同法国偏好；复用并扩展旧援法身份与冷却。法国明确接受才付钱／建立合同，援助不等于参战。
4. **社会与共同体**：教育与国家能力之后开放王朝接受度、印度共同体；人权阶段开放种姓／公职改革。文化接纳、宗教待遇、识字和职业资格分别判定，不强制全民同化或改宗。
5. **土邦协商与地区起义**：一次一个可回绝的政治对象；按实际 USM owner-state 联络／暂停／发难；有限战争与战后地方自主独立结算。建国不能隐含赞助者吞并。
6. **统一与新政权后继**：承接 BHT/MUG/DRA 形成及远山／天竺宣慰司决议；迁移完成项、合同与冷却；统一后的财政、学校、军队、宗教／地区代表仍有治理目标。

建议文件分为 `nesnd_india_lifecycle`（唯一初始化／清理）、`nesnd_india_reform`、`nesnd_india_society`、`nesnd_indian_princes`、`nesnd_france_india_policy`、`nesnd_india_uprising`、`nesnd_usm_india`，各自配 JE／trigger／effect／button／value／bar／modifier／双语本地化。原版已有原生 JE、按钮、progress bar 和图标足够，不需要新 GUI。原生容器及 context 的定义在 [G/common/journal_entries/journal_entries.md:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:1>)。

## 2. 当前源码已经有什么，缺什么

|对象|当前有效内容|实施动作／边界|
|---|---|---|
|MUG 国家身份|继承 G `MUG`：unrecognized、empire、hindustani、Sunni、`british_indian_caste_system`；旧四主文化定义只在 `.bak`|不把 `.bak` 当活动数据。若新增 `REPLACE:MUG`，显式保留宗教／文化／等级意图，不能用国家定义重写所有人口。[G/common/country_definitions/00_countries.txt:1278](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1278>)|
|MUG 国家历史|M `mug - mongul.txt` 与 G `mug - mughals.txt` **不同相对路径，均加载**。前者 tier3 与 academia 等科技、传统政治、印度教祭司思想及英国公司；后者 tier4、额外法律及 `je_mughal_hindustan`|准确同路径兼容覆盖 G 的国家历史，再让作者版本成为单一来源。明确保留哪些法律／技术；不可笼统认为字母顺序已解决冲突。[M/common/history/countries/mug - mongul.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/mug - mongul.txt:1>)、[G/common/history/countries/mug - mughals.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/countries/mug - mughals.txt:1>)|
|MUG 人物|M `mug - mongul.txt` 创建作者 Bahadur／Mirza、Zorawar／Gardner；G `mug - hindustan.txt` 另创 Akbar／Bahadur 和两个 IG 领袖|用准确原版相对路径处理冲突，保留作者君主／继承人。可保留不冲突的 IG 领袖，但不得再生成第二个王位／继承人。只证明源码重叠，未声称实测双君主。[M/common/history/characters/mug - mongul.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/characters/mug - mongul.txt:1>)、[G/common/history/characters/mug - hindustan.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/characters/mug - hindustan.txt:1>)|
|公司|M强制 `company_east_india_company`，G公司条件锁 GBR|删除不合用的初始化调用或完整定义法莫公司；不能只改公司名称便认作法国资本。公司实际选址、所有权、成立能力需要闭包。[M/common/history/countries/mug - mongul.txt:21](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/countries/mug - mongul.txt:21>)、[G/common/company_types/00_companies_asia.txt:2](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/company_types/00_companies_asia.txt:2>)|
|军队|M印度编制文件停用；G印度编制仍加载，MUG只2不正规步兵＋1骠骑；USM锡兰有南洋舰队15战列舰＋15护卫舰声明|不能把 MUG 军工8级误当军队8营。新增编制要对应驻地人口、科技和军费，原生历史生成军营不能另算一遍。不要重新复制整个印度军队文件覆盖所有土邦。[M/common/history/military_formations/CE_military_formations_india.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/military_formations/CE_military_formations_india.txt:1>)、[G/common/history/military_formations/05_military_formations_india.txt:1448](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/military_formations/05_military_formations_india.txt:1448>)、[M/common/history/military_formations/CE_military_formations_asia.txt:347](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/military_formations/CE_military_formations_asia.txt:347>)|
|法莫关系|FRA→MUG tributary；TRA→USM puppet；其余42个有组织土邦在有效开局外交历史未见宗属调用|用实时 `overlord`，不把法国／莫卧儿当全部印度国的默认宗主。[M/common/history/diplomacy/ce_subject_relationships.txt:136](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:136>)、[M/common/history/diplomacy/ce_subject_relationships.txt:185](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:185>)|
|既有援法|吴代明后外部通知→`nesnd_external_policy`；MUG可选FRA、申请资金／军械；真实接受／拒绝／条约；迈索尔按钮只加claim和关系−10|保留已签合同；新改革入口不能继续依赖南朝危机未结束。旧链的 `nesnd_south_settled`、`has_journal_entry=nesnd_external_policy`、dismissed／following 必须集中路由，不在新旧两套各领一次钱。[M/common/journal_entries/nesnd_external_journal.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_external_journal.txt:1>)、[M/common/scripted_triggers/nesnd_external_triggers.txt:43](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_external_triggers.txt:43>)、[M/common/scripted_buttons/nesnd_external_buttons.txt:241](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_external_buttons.txt:241>)、[M/common/scripted_buttons/nesnd_external_buttons.txt:459](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_external_buttons.txt:459>)|
|统一数据库|BHT：28地区、0.75、pan-nationalism；MUG：文化州100%；DRA：文化州75%、pan-nationalism，排除BHT/BIC|保留原形成机制，新增治理后继。不能把“28×75%=21”当引擎全部条件。[M/common/country_formation/00_formable_countries.txt:576](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_formation/00_formable_countries.txt:576>)、[M/common/country_formation/00_formable_countries.txt:959](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/country_formation/00_formable_countries.txt:959>)|
|新印度改革／土邦／共同体／起义|当前有效 `.txt` 中未发现该批准方案的独立 `nesnd_india_*` 或 `nesnd_mug_*` 玩法实现|研究／方案不能记作完成。旧外援、原版种姓和形成数据库是可复用基础，不等于完整印度主线。|

### 旧印度／鸦片处理的准确结论

用户要求参考既有禁用／替换办法，应采用**窄对象 REPLACE＋明确关闭旧入口**，不覆盖整个全球 history 或通用 on_action。当前 M `CE_00_opium_wars.txt` 是 `REPLACE:je_opium_obsession` 的改写，并非一个 `always=no` 禁用壳。M `CE_04_sepoy_mutiny.txt` 也是完整的 BIC绑定 `REPLACE:je_uneasy_raj`，**没有实际禁用**；G `history/global/00_global.txt:3` 仍无同路径MOD覆盖并显式加入该 contextless JE。不要把作者此前“改过印度文件”误读为全链已关。[M/common/journal_entries/CE_00_opium_wars.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/CE_00_opium_wars.txt:1>)、[M/common/journal_entries/CE_04_sepoy_mutiny.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/CE_04_sepoy_mutiny.txt:1>)、[G/common/history/global/00_global.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/global/00_global.txt:1>)。

本机原生说明明确：`add_journal_entry` 绕过 `is_shown_when_inactive` 和 `possible`，因此仅 `possible={always=no}` 不足。当前日本兼容文件有可参照的关闭壳：隐藏＋possible=no＋invalid=yes，不保留旧月度／成功／失败效果；contextless印度壳还要用原组和 `should_be_involved=no`／`should_show_when_not_involved=no`，避免无scope调用国家初始化。[G/common/journal_entries/journal_entries.md:12](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:12>)、[M/common/journal_entries/zz_nesnd_jp_native_journals.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/zz_nesnd_jp_native_journals.txt:1>)。

建议停用对象清单：`je_uneasy_raj`、`je_sepoy_mutiny`、`je_mughal_hindustan`、`je_consolidate_colonial_rule`、`je_imperialism_of_promise`、`je_british_dictate_plantations`、`je_british_dictate_military`、`je_british_dictate_law`、`je_british_dictate_universities`、`je_india_home_rule`、`je_india_nationalism_britain`、`je_india_nationalism`、`je_india_non_cooperation_movement`、`je_communal_divides`、`je_dravidian_movement`、`je_federation_of_india`、`je_victoria_terminus`。这些是 BIC／英国／旧王朝复兴链，不直接改TAG复用。`je_princely_states` 若启用新通用自主议程，也应窄禁用以免两个自主系统共存。新实现若代替全印度铁路路线，再单独停用 `je_india_railway`；否则保留其通用铁路活动。`je_indian_famines` 和 PAN的 `je_sikh_sovereignty` 不因“文件在04_印度目录”自动禁用。当前原生对象行号见同目录源表；完整原版研究见 [W/reports/india-research-20261102/native-india.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-research-20261102/native-india.md:1>)。

旧档已有JE应静默失效并清**旧链自己拥有的**临时状态；已签条约、实际领土、科技／建筑成果保留。需查旧 `mughal.*`／`sepoy_mutiny_events.*` 已排队事件的 trigger/cancellation，不能因为关JE就宣称所有旧弹窗都撤销。此旧档兼容仍须定向测试。

## 3. 地区与国家白名单：本轮重新解析

本轮用保序 `pdx.py` 重读有效 GAME→MOD 的所有国家定义、州历史及外交历史，并核全部当前州 TAG；源SHA和行号在 `native-implementation-sources.json`。下面是开局声明，不是实时存档认证。

**43个有组织地方国家**：`ALW ASM AWA BAG BAS BER BHO BHV BHW BIK BUN COC COO DHA GAR GWA HYD IDA IND JAI JAS JEY JHN JOD JUN KHP KNO KOT KUT MEW MNP MYB NAG NAR NAW PAN PLP PTA PTN SAT SIN SUR TRA`。TRA开局为USM puppet，其余42国有效历史未配置宗属。`KKI MGH NGA TIP` 是 decentralized，不套同一有组织国家外交JE。MUG另走帝国主线。`MYS CAR CEY BIC BHT DRA` 开局完整州历史没有领地，任何创建／回复前仍要实时核存在性。

通用资格宜为“白名单或本系统登记的合法地方继承者＋存活＋有实际印度州＋非decentralized”。单凭南亚主文化会遗漏某些本地政治对象，也可能误纳他处国家；单凭 `is_princely_state` 又会漏掉42个独立邦。原生该trigger主要识别特定政体／GBR、BIC、BHT属国。[G/common/scripted_triggers/00_scripted_triggers.txt:1842](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt:1842>)。BHT/DRA形成后可承接同国的任务记录，但不重复生成“首次独立”奖励。

|USM实际州|M州历史行|首批地区行动接收者／创建建议（设计选择）|
|---|---:|---|
|STATE_CIRCARS|4124|既有KNO或JEY的明确同意协作；不要覆盖它们现有本国；也可单独登记当地自治对象，不能擅自把整区归MUG|
|STATE_KURNOOL|9332|KNO已经存在，需先双边接受；不 `create_country KNO`|
|STATE_MADRAS|4214|CAR开局不存在，可按原版Carnatic本地身份作释放候选；须重验TAG未占用及人口>0|
|STATE_MYSORE|4175|MYS开局不存在，可作本地释放候选；已有MYS时转协作／外交接收分支，不覆写身份|
|STATE_TRAVANCORE|4192|TRA、COC均存在，本地区还有各自州；只处理USM部分，先确定哪一方接受／当地自主方案，不能夺另两国地区|
|STATE_GUJARAT|4284|西岸扩展。BER/DHA/IDA/NAW/PLP/JUN/BHV/KUT均已有相邻政治对象；必须选一个实际合格接收者并取得回复，不能凭文化随机吞并|
|STATE_CEYLON|1648|独立岛屿／USM殖民行政与天竺安排范围另核原稿；CEY可释放但不能自动当“南印度五区”|
|STATE_INDIAN_OCEAN_TERRITORY|3334|岛屿另列；不随南印度民族起义自动转地|

原始州行来源均为 [M/common/history/states/00_states.txt:1648](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:1648>)。所有按钮用 `s:STATE_X.region_state:USM` 或同一owner-state谓词，不能用 `s:STATE_X` 代表整区所有土地，也不能用 `is_incorporated=no` 代替殖民资格。未整合标记在USM印度并不统一。当前 MUG／USM人口、产业静态基线可复用，但只作输入：MUG约9347万人；USM大陆约2138万人、含锡兰岛屿约2274万人；不把这些数字当运行GDP／SOL／就业。[W/reports/india-research-20261102/current-mod-india.md:15](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-research-20261102/current-mod-india.md:15>)。

## 4. 分阶段 JE 的最小完成合同

|模块／拥有者|进入与实际目标|暂停／结束／后继|
|---|---|---|
|MUG朝廷与改革（开局）|MUG或合法继承者存活且有印度州；记录当前合法性、财政、机构、文化接纳，初始化一次；选择学校／产业优先方向|共和国不等于全部印度玩法失败：仅关闭王朝专项，保留国家建设与共同体。灭亡无继承者失效；换TAG刷新对象。开局只显示此主JE及可选法援。|
|学校与官署（早期）|改革选择＋academia等实际科技；本国大学／行政岗位、纸的可得性、学校法律和机构投入；跨实际持有地区安排，不能要求尚属USM的MADRAS才可做第一期|财政不足／纸贵是暂停或明定风险，不补国库；完成保存done、撤临时项目支出、开放下一期。识字目标采用运行 `literacy_rate` 或实际学校／职业条件，不 `set_pop_literacy` 一键全国加值。|
|工场与军队（早中期）|已有棉染丝纺织和军工作底盘；煤铁工具／军工／训练／交通实际建设，允许国内产业或共同市场供给；用 `country_has_building_type_levels`＋occupancy／profit／有效PM|不要求每种商品自给或每州零失业；使用原生市场订单与价格。临时短缺暂停，已建工厂永久保留；完成不免费生成满编军队、舰队或整时代科技。|
|法援项目（收到接受后）|教育、设备产业、军官训练三种议题；报价保存，双方真实财政和法律资格核完再付主要成本；法国可拒绝|拒绝有冷却，过期／换政体不记作恶意违约；顾问修正到期／条件失效撤除，建筑科技保留。真实原生条约继续按条约结算，项目结束不能伪装解约。|
|王朝与印度（民族阶段）|nationalism／pan-nationalism＋教育／城市政治阶段；两项有界状态：王朝接受与共同体。君主印度化／立宪分享／共和参与均可产生国家认同|废君主只终结王朝分支，不清共同体；接受多文化是一条合法完成路线。只有选择长期语言整合才使用局部文化转换，且不把日本10%／30%参数搬来。|
|身份与公职（晚期）|human_rights／相应改革政治阶段；原生caste法律和农村人口／政府支持；教育、公职／军官资格与种姓约束分别显示|只有适用社会等级时才开启种姓目标；改用default hierarchy应判制度转型／承接，不无条件失败。宗教自由与公共／宗教学校是不同法律取舍。|
|土邦自己的主线（开局共用）|独立国：守土／发展／商业保护／联合选择；属国：向当前直接宗主请求自治、独立或维持安排；双方都有实际选择|独立→属国／改宗主，旧pending失效并转议程；独立成功仅记一次阶段成果，后续本国发展继续。自主／保护／贸易／参战四种承诺不可混为一个“支持”。|
|印度诸邦（统一准备）|共同体与整合能力达标；每次选择一个现存邦，报价地方权利／年金／保护或真正联合；玩家明确接受才转宗属／吞并|拒绝不自动灭国；政治排他承诺最多一份，商业可多份；已存在附庸也须依当前主权条件。完成按实际关系与领土；形成BHT后接统一治理。|
|地区起义（后期）|**独立 OR 足够军政财政能力**，且真实印度基础、合格USM州与当地伙伴；选择、筹备、暂停、发难分步|成熟只表示可发难，不能JE自动完成清掉按钮；发难成功登记战争案件后才清筹备成本。全部USM目标消失时按实际世界结束或转外交，不永远空转。|
|USM印度治理／新行政体|USM现有印度owner-state常驻治理；远山／天竺宣慰司决议在原稿确定制度、地区后接入此合同|不改USM全国social_hierarchy来模拟印度地方种姓。新国家仅配置自己法律；转出州清USM局部修正，既有人口、建筑、投资随原生州转移保留。|
|统一后治理|实际形成／统一成果＋保留下来的阶段数据；财政负担、代表参与、学校、市场交通和军队整合|没有“一统一就所有社会问题完成”。成立国家只登记一次；允许现实经济压力与政治失败，不自动补钱或复活。|

完整原生样例链：功利主义JE（公共学校／小学／废奴／税制／官僚）→`utilitarian.1/.2/.3`；英国大学合同（三地建筑目标）→JE完成／超时关系；铁路JE→`india_railway.5`；反种姓JE→`caste_conflict.1/.2/.3`。这些证明条件／期限／结果形状，不能搬其英国叙事或DLC专属角色。[G/common/journal_entries/04_imperialism_of_promise.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_imperialism_of_promise.txt:1>)、[G/common/journal_entries/04_india_british_dictates.txt:345](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_british_dictates.txt:345>)、[G/common/journal_entries/04_india_railway.txt:2](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_railway.txt:2>)、[G/common/journal_entries/04_dravidian_movement.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_dravidian_movement.txt:1>)。

### 种姓、教育与共同体的精确原生接缝

`british_indian_caste_system.pop_criteria` 是 hindu＋南亚heritage；MUG Sunni国教不代表所有穆斯林都进入该等级。`lawgroup_caste_hegemony` 链接该 hierarchy；四法律ID为 `law_hindu_caste_enforced`、`law_hindu_caste_codified`、`law_hindu_caste_not_enforced`、`law_affirmative_action`。后一项的原生解锁是 `law_slavery_banned`；`human_rights` 是原版反种姓**JE**门槛，不能错写成该法律数据库强制技术。[G/common/social_hierarchies/00_social_hierarchies.txt:5](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/social_hierarchies/00_social_hierarchies.txt:5>)、[G/common/law_groups/00_laws.txt:38](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/law_groups/00_laws.txt:38>)、[G/common/laws/00_caste_hegemony.txt:7](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_caste_hegemony.txt:7>)、[G/common/laws/00_caste_hegemony.txt:129](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_caste_hegemony.txt:129>)。

Hindu宗教本身只有heritage／颜色／图标／禁忌，没有固有识字惩罚；识字初始化baseline会按职业、阶层、未整合状态调整，不能报全国5%。原生学校链为 `law_religious_schools`／`law_public_schools`→`institution_schools`→教育获取；小额 `state_pop_qualifications_mult`／`state_education_access_add` 必须查实际修正类型和成本，不能称最终识字直接增加同值。[G/common/religions/religion.txt:89](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/religions/religion.txt:89>)、[G/common/scripted_effects/00_starting_pop_literacy.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:1>)、[G/common/laws/01_education_system.txt:36](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_education_system.txt:36>)、[G/common/laws/01_education_system.txt:299](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/01_education_system.txt:299>)、[G/common/institutions/00_institutions.txt:26](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/institutions/00_institutions.txt:26>)。

`movement_india_pan_national.creation_trigger` 锁BIC、属国、非南亚主文化、泛民族主义，不能直接拿它作为MUG后期JE的必须运动。首批可由科技／实际法律／城市与学校判共同体；若需要专门运动，独立前缀定义再沿原生 movement→support factors→人物／POP支持链适配，不能全局重写BIC运动污染别国。印度教民族主义、穆斯林民族主义与王朝支持也不应合并成一项宗教数值。[G/common/political_movements/03_pan_national_movements.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/03_pan_national_movements.txt:1>)、[G/common/political_movements/04_national_movements.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/04_national_movements.txt:1>)、[G/common/political_movements/04_national_movements.txt:365](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/political_movements/04_national_movements.txt:365>)。

## 5. 法国与印度：一套分类，一套请求，一次兑现

分类即时读取现行法律，顺序：委员会共和→神权→总统／议会共和→君主／社会君主→其他。君主内再判断唯一可靠在位家族：`house_bonaparte`、`house_orleans`、`house_bourbon`／`legitimist_leader`／MOD `house_bourbon_leader`。家族和政治意识形态不同；摄政本人姓氏不能换朝。无可靠当前证据用other_monarchy／unresolved，普通商业教育仍可有默认答复，王朝承诺暂停。`country_has_monarchy_law` 已覆盖 `law_social_monarchy`。[G/common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt:13](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt:13>)、[M/common/character_templates/zz_ce_FRA.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/character_templates/zz_ce_FRA.txt:1>)、[M/events/ce_fra_unrest_events.txt:2136](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_fra_unrest_events.txt:2136>)、[M/events/ce_fra_unrest_events.txt:2360](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_fra_unrest_events.txt:2360>)。更详逐路径出处见 [W/reports/japan-india-plan-revision-20261102/france-regime-policy.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/france-regime-policy.md:1>)。

偏好是项目权重，不是必定接受：波拿巴偏军官军工；奥尔良偏投资铁路商业；波旁偏王朝／官署秩序；代表共和偏学校／参与；委员会政府偏合作工业与现存相近政府；神权有宗教协商和普通贸易。战争、破产、无法到达市场、对敌援助等先作硬条件。当前政府变化只改未来请求／可撤回的政治支持，不能自动删除已签合同或已建学校。

**最低请求字段**：sender、receiver、kind、serial、quoted_cost、sender_sponsor、receiver_sponsor、relevant_policy_version、deadline、subject/target-state。发送增加serial；事件保存数值快照；trigger、cancellation、option trigger、AI读取、effect、after清理均核同serial。旧答复只能清旧请求，不能把新请求锁删掉。当前日本外交通道已具备可借的serial／双方sponsor／regime快照，不建议继续照搬旧external只存pending的简版。[M/common/scripted_effects/nesnd_jp_foreign.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_jp_foreign.txt:1>)、[M/common/scripted_triggers/nesnd_jp_foreign.txt:33](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_jp_foreign.txt:33>)。

新入口与旧 `nesnd_external` 的互斥至少包含 pending、cooldown、aid_committed／实际条约身份。可在旧trigger中把 MUG 的资格改为“外部政策JE OR 印度合作JE”，并把南朝结算禁令只留给原危机参与国；不能为修MUG而取消所有国家的原有危机限制。旧JE清理只清旧JE字段，不清印度正在进行的请求。

**合同与资源**：原资金条约 quantity=500是每周流量；一年binding是最短约束期，不是自动到期。原生 `goods_transfer` 有可达市场、海港／接壤市场和非关税同盟junior等条件；required_inputs 为 `quantity`＋`goods`。本机effects.log只有create_treaty和遍历条约等接口，未发现已认证的定时解约effect。本轮新项目可以使用一次有报价的国库拨款与有期限顾问支出，并复用旧合法条约；不要承诺“到期自动停款”，更不要写虚构库存／仓储采购。[G/common/treaty_articles/05_transfer_money.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/05_transfer_money.txt:1>)、[G/common/treaty_articles/13_goods_transfer.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/13_goods_transfer.txt:1>)、[M/common/scripted_triggers/nesnd_external_triggers.txt:215](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_external_triggers.txt:215>)。

所有工业／军需条件使用原生市场订单、当地价格／短缺、实际建筑生产与就业；共同市场能正常供给即合法。不加库存条、不模拟消耗仓库、不强塞商品order掩盖经济问题。原版非合作JE区分同市场生产份额与不同市场进口依赖，是可用的制度层观察；不无测量照抄2.5／2.0阈值。[G/common/journal_entries/04_india_non_cooperation.txt:65](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_india_non_cooperation.txt:65>)。

## 6. 地区起义：必须先闭合一个州，再扩展按钮

### 唯一案件的状态与对象

建议地区案件身份登记在稳定 `state_region` 变量上（case_serial、sponsor、local_actor、original_owner、stage），并在实际owner-state记该案临时修正来源。这样赞助者灭亡后可由其他存活参与者／一个contextless维护入口收尾。国家JE负责本国费用／按钮，**不能各国JE各转一次地**。最小枚举为 contact→preparing↔paused→ready→transferred→play_created→war→settled／failed／invalid。成熟ready保留发难入口；只有成功移交战争案件才清接触子阶段。

按钮六地区固定显示可行；每一“可见／可点／选择／真正执行”都复用同谓词：当前USM owner-state、人口>0、未被第三国取得、未有该地区案件、政治接收者合法／同意、双方无现存相同战争、能承担沉没联络费。玩家可暂停，停维护费且按明定组织衰减；重开不重发资源。原版按钮接法来自波兰claim→最后通牒→双边答复；临时州修正清理来自CNE owner-change。[M/common/scripted_buttons/ce_poland_scripted_buttons.txt:165](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/ce_poland_scripted_buttons.txt:165>)、[M/common/scripted_triggers/nesnd_poland_repairs.txt:6](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_poland_repairs.txt:6>)、[M/events/ce_poland_events.txt:58](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_poland_events.txt:58>)、[M/common/on_actions/nesnd_cne_estate_ownership.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_cne_estate_ownership.txt:1>)。

### 创建与战争的原生链

1. 当地TAG未存在时，从真实USM州选择人口>0 seed，`create_country={tag=... origin=... state=... on_created={...}}`。`origin`只说继承certain values，不证明科技／军队／人物全继承；新身份配置放在on_created，仅对新国执行。既有KNO/TRA/COC只走已同意接收分支。原生 docs有重复state／province和新国家on_created scope；Carnatic实例用未存在TAG＋本地province。[W/references/engine-docs-1.13.11-20261031/effects.log:878](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:878>)、[G/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:344](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:344>)。
2. 领土只能转本案登记的actual state；`set_state_owner`是state→country原生效果。不移动人口块、不复制建筑、不先删当地产业；外资处置另受原生规则，不默认国有化。原版Kurnool有相同USM替代前的BIC owner-state转移形状。[W/references/engine-docs-1.13.11-20261031/effects.log:37144](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37144>)、[G/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2258](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2258>)。
3. 新独立政权不能直接用 `independence`：该wargoal要求 `root.overlord=target_country`。TRA等真实属国争独立才用原生 `dp_independence`。[G/common/war_goal_types/10_independence.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/10_independence.txt:1>)、[G/common/diplomatic_plays/00_diplomatic_plays.txt:202](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:202>)。
4. **不要用 `dp_sepoy_mutiny`**：它是annex_country且禁止谈判，会把既存KNO全部领土押上。可建独立前缀有限play，允许谈判，USM要求本案州收复，地方政权保留防守与合法有限目标；不自动给所有土邦吞并目标。`return_state`还要求目标state有USM claim；其 `annexes_entire_state` 要与混合地区真实owner-state复核，不能假定只一province。必要时选择已核验的conquer-state有限目标，或前缀custom wargoal按确切登记州执行，后者需单独验证回调。[G/common/diplomatic_plays/00_diplomatic_plays.txt:1368](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:1368>)、[G/common/war_goal_types/21_return_state.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/21_return_state.txt:1>)、[G/common/war_goal_types/03_conquer_state.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/03_conquer_state.txt:1>)。
5. 创建DP后立刻寻找**本case＋双方＋类型＋目标州**的实际DP并登记其身份；只有存在才到play_created。战争观察用具体DP／war参与者、和约／退让和真实领土，不能用赞助者 `is_at_war=no` 判全部成功。赞助者、法国、土邦加入都需单独合法承诺；已援助不自动入战。原生 `create_diplomatic_play` 与 `add_war_goal` 接口及本项目波兰源分别在 [W/references/engine-docs-1.13.11-20261031/effects.log:909](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:909>)、[M/events/ce_poland_events.txt:115](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_poland_events.txt:115>)。
6. 部队只能在转地结束后按实际军营、人口、科技、当地支援一次初始化；继承单位非零不再免费加同批兵，零赠兵也要记prepared；不赠海军、不靠人口造空国家。胜后当地可以独立、保护、联合，必须另谈；赞助者不能在战争结束自动吞并。

### 非原子步骤与错误出口

创建、转地、建DP不是一个事务。每完成一步写stage及准确state集合；下一步失败不发奖励。限定重试次数／期限，仅补仍合法的缺失步骤。若没有DP且临时国仍只持本案土地，USM仍活且未有第三方变化，可用 `set_state_owner` 返还登记state并记录终止；若临时国家已合法取得别地、被第三国占有／兼并，不能 `annex` 整个国家回滚，转外交余局结案。空临时实体在最后州返还后的引擎灭亡／残留语义未被本报告实测；**该新建分支交付前必须有引擎证据或完成可靠源码闭包，不能宣称已解决L23**。

州易主即时移除旧USM／秘密组织buff并排队一次维护；移交战争时只清联络成本，不能把战争登记一并删掉。无主办国时由地方国或contextless案件继续收尾。无目标时结束／失效；不每月强造新州目标。原生 `on_state_owner_change`／`on_state_created` 的scope与CNE排队去重参考：[G/common/on_actions/00_code_on_actions.txt:7131](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7131>)、[G/common/on_actions/00_code_on_actions.txt:7174](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7174>)、[M/common/scripted_effects/nesnd_cne_estate_ownership.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_cne_estate_ownership.txt:1>)。

## 7. 统一、远山／天竺宣慰司与继承接缝

三类操作不要混淆：`change_tag`是现存国家改号；`create_country`是创建并给州；`annex`是合并现存政治主体。远山／天竺的原稿若要求USM设立地方政府，需新国家创建＋精确USM地区＋实际宗属条约；若要求现存地方政府改制，保留其现有外交／人口／领土，只改已授权身份。任何TAG冲突先转“现存政府接收／拒绝／不可执行”，不能无条件覆写。引擎 `change_tag` 和 `create_country` 各自接口见 [W/references/engine-docs-1.13.11-20261031/effects.log:682](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:682>)、[W/references/engine-docs-1.13.11-20261031/effects.log:878](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:878>)。

统一协商可以借原 `je_federation_of_india`→invite button→`federation_of_india.*`→吞并＋`modifier_privy_purse_payments` 年金：其入门却要求BHT/BIC和原土邦集合，不能原样套MUG。也不能沿其“委员会共和国即失败”强迫本MOD所有联合走君主制。新合同保留具体承诺和财政代价，按双方的真实选择走保护／联邦／并入。[G/common/journal_entries/04_indian_federation.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_indian_federation.txt:1>)。

`on_country_formed` 原版root=新国家，可作为形成后的刷新入口；仅补缺失数据和重新路由，不将done清零。既有国家吞并前，先由存活接收者复制对应阶段成果、一次奖标记、地方承诺与冷却；已答应但未执行的旧请求应失效并由新主权重新确认。派生新国不得每国重新领取同一基础奖励。新共和国／换朝保留共同体，王朝专项暂停或关闭。[G/common/on_actions/00_code_on_actions.txt:3887](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:3887>)。本项目 `nesnd_jp_inherit_partner` 已有显式完成项迁移范例，但印度要覆盖自己全部记录，不复制日本列表。[M/common/scripted_effects/nesnd_jp_foreign.txt:111](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_jp_foreign.txt:111>)。

## 8. 本批必须提交的核验表

|覆盖|最低外部检查|未证引擎边界|
|---|---|---|
|有效加载|GAME→MOD有效路径，重复对象／history调用；MUG只一套王位；关闭旧JE的入口／complete／fail／pulse全部检查|history顺序、实际显示、军营生成、公司选址|
|阶段／一次结算|每JE available/running/paused/done/failed/invalid所有写入者；done锁先于奖励；父子双向清理；后期不在开局添加|自然pulse、同帧完成／失效竞态、读档持久|
|请求|对所有trigger/cancellation/option/AI/effect/after做对象＋serial＋policy闭包；拒绝、超时、旧回复、新请求全覆盖|事件取消、旧弹窗迟答、法国变政／摄政|
|地区与人口|每按钮同一候选谓词；实际USM state集合；无第三国转地；人口／建筑／外资没有手写搬迁；新TAG存在冲突|split/merge保留、最后一州返还、军队继承、占领／所有权差异|
|战争|实际DP类型／双方／target-state；双方战争目标；退让／白和平／部分结果；唯一执行者|DP失败／退让回调、第三国介入、停战、L23恢复|
|经济／社会|本地化展示真实原生条件；市场供给与短缺为原生值；无库存采购；种姓只适用Hindu＋南亚，USM全国制度不改|真实就业、财政、识字、资格与发展难度|
|继承／新政府|BHT/DRA/MUG、远山／天竺变化后的done／冷却／承诺；无重复人物、奖励、舰队|玩家国家形成、被吞并／分裂、多人双方选择|

上述映射覆盖L01–L24：L01–L05阶段与幂等；L06–L09、L17、L21、L24双边／法国；L10–L11、L18、L23具体战争；L12–L16、L20继承／地区；L19真实经济；L22AI退出。外部静态检查只能标STATIC_PASS；未开游戏不能写ENGINE_PASS。报告没有提供新的玩家文案，实际落地文案须另走 `nesnd-player-writing` 的原作者取样流程。

本次技能复核没有新增维护规则；已有规则已覆盖本次新证据。最重要的差异是：旧 `CE_04_sepoy_mutiny` 不是禁用壳、旧外援把MUG绑在南朝危机、现有日本serial回复闭环可复用、CAR/MYS/CEY开局未用而多数土邦已存在。对应文件均只读核验。
