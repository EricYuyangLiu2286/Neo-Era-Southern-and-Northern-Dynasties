# 印度诸邦与南印度起义：修订研究

2026-11-02。**SOURCE_AUDIT / DESIGN_PROPOSAL / ENGINE_NOT_RUN**。GAME 1.13.11 / Steam build 24799966；本轮 `catalog.py status` 返回 CURRENT、changed_count=0。只读主 MOD 与本体；只在 WORK 写研究，没有开游戏、没有改玩法。以下“当前”指有效开局脚本，不冒充运行存档的宗属、军力或外交能力。

本报告补充既有印度计划：保留“脱离殖民约束 **或** 已有足够能力”两种开放路径，增加逐州组织反吴起义；各印度地方国家拥有自己的主权与发展方向。MUG、USM、FRA可以影响它们，但不会因同为印度国家而自动归并到MUG。原计划与此前数据入口：[20261102-india-development-design.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/20261102-india-development-design.md:1>)、[current-mod-india.md:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/india-research-20261102/current-mod-india.md:1>)。

## 1. 实际国家：多数已经独立，不能统一做“摆脱莫卧儿”日志

本次重新解析有效 `.txt` 国家定义、州历史及全部有效外交历史，保留重复块，按 GAME→MOD 同相对路径覆盖。此前JSON只提供研究地区集合，不复用其宗属结论。该范围52个所有者中，扣除MUG、USM、FRA、POR、QE1后，有47个本地国家；其中43个为 `unrecognized` 的有组织国家，4个为 `decentralized`。完整TAG与实际持有地区见附表。

|对象|开局脚本事实|日志路由|
|---|---|---|
|TRA|USM的puppet；只持有特拉凡哥尔地区的一部分，另有USM与COC州|“争取自主／独立”的属国版本；不能把整个地区算TRA或算USM|
|MUG|FRA的tributary；在本MOD为大型直接领土帝国|独立与借法自强有冲突，但“强到足以行动”路径不能被写成先独立的硬锁|
|其余42个有组织地方国家|有效外交历史未发现给它们建立宗属的调用；HYD/AWA/NAG/PAN/SIN/JHN/KNO等已有实际领土|开局走“保全主权、建设本国、选择保护／联合”的独立版本|
|NGA、TIP、KKI、MGH|实际有领土但国家类型为decentralized|暂不套用普通玩家土邦／独立战争JE；地方运动需另行设计|
|MYS、BIC|本次完整有效州历史未见create_state|不能当现存外交收件人；USM→MYS调用受exists守卫；MYS可作起义建国候选，须现时重验|

TRA与MUG的关系来自 [ce_subject_relationships.txt:136](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:136>)、[ce_subject_relationships.txt:185](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/ce_subject_relationships.txt:185>)。原版BIC土邦关系在MOD同路径文件已注释，不能转译成MUG的属国列表：[00_subject_relationships.txt:279](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/diplomacy/00_subject_relationships.txt:279>)。四个分散国家的有效定义见 [00_countries.txt:4602](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4602>)。独立判断的范围是开局历史：后续启动事件、外交、革命或玩家行为改变主权后，JE按实时关系切换。

USM大陆直接领地是 `STATE_CIRCARS`、`STATE_GUJARAT`、`STATE_KURNOOL`、`STATE_MADRAS`、`STATE_MYSORE`、`STATE_TRAVANCORE` 的USM州；锡兰和印度洋领地另列。建议首批起义按钮列南方五区（CIRCARS/KURNOOL/MADRAS/MYSORE/TRAVANCORE），GUJARAT作为西岸扩展，锡兰和岛屿不自动纳入“南印度”。必须限定 `state_region` 与 `owner=USM` 的交集，不能取整个地区，也不能把原版BIC边界搬入。源：[00_states.txt:4124](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4124>)、[00_states.txt:4175](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4175>)、[00_states.txt:4214](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4214>)、[00_states.txt:4284](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4284>)、[00_states.txt:9332](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9332>)。

## 2. 波兰机制：可复用的请求闭环，不是现成的起义生成器

完整链条如下。

1. `je_ce_the_polish_problem`在无国家上下文的组中维护参与国；月度补纳实际目标地区的新所有者，邀请一次。国家子JE分别处理收复、战争准备、支持与反对。组声明、参与和收尾：[CE_journal_entries.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entry_groups/CE_journal_entries.txt:1>)、[ce_europe_poland_issude.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_europe_poland_issude.txt:1>)、[nesnd_poland_repairs.txt:19](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_poland_repairs.txt:19>)。
2. `je_ce_polish_reconquest`逐州按钮消耗动能并加claim；`je_ce_polish_war_preparation`逐州最后通牒按钮要求相应进度>=100，支付50进度，只选真实存在、非KRA所有且有KRA claim的州。它不是“按按钮便完成战争”。源：[ce_europe_poland_issude.txt:202](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_europe_poland_issude.txt:202>)、[ce_poland_scripted_buttons.txt:88](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/ce_poland_scripted_buttons.txt:88>)、[ce_poland_scripted_buttons.txt:165](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/ce_poland_scripted_buttons.txt:165>)、[nesnd_poland_repairs.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_poland_repairs.txt:1>)。
3. 发起者保存 `nesnd_polish_pending_state`（4个月），目标所有者收到 `.2`；`trigger`、`cancellation_trigger`、选项effect都重验发起者存在、pending同一目标、州仍归收件人、宗属/同盟/战争等条件。答复或after只清自己的匹配请求。源：[nesnd_poland_repairs.txt:6](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_poland_repairs.txt:6>)、[nesnd_poland_repairs.txt:37](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_poland_repairs.txt:37>)、[nesnd_poland_repairs.txt:79](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_poland_repairs.txt:79>)、[ce_poland_events.txt:58](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_poland_events.txt:58>)。
4. 让步仅把该实际state交给KRA；拒绝建立 `dp_return_state`，并给防守国对KRA的 `annex_country` 反向战争目标。支持国另收到 `.7`，选择后才 `add_initiator_backers`。源：[ce_poland_events.txt:75](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_poland_events.txt:75>)、[ce_poland_events.txt:115](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_poland_events.txt:115>)、[ce_poland_events.txt:339](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/ce_poland_events.txt:339>)。
5. 主问题胜利、失败、失效均通知并设终局；并非所有国家永久共用一条无关自身结果的进度。印度多起并行主权争端必须以本国/对象/本次行动为身份，不能复制波兰全局 `ce_poland_problem_end` 锁死整个印度。源：[ce_europe_poland_issude.txt:107](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_europe_poland_issude.txt:107>)。

**可借**：逐州按钮、原生进度、实际目标选择、支付一次、限时pending、迟答重验、独立的支援邀请、所有终局清理。**不能照抄**：KRA收复资格、claim必需、1850截止、五州胜利、拒绝即吞并KRA反目标、全局唯一终局。印度反殖民支持并不天然产生MUG的领土claim；这些内容必须按当地行动的授权与目标重新定义。

## 3. CNE营产：逐州状态、失地清理可复用

`nesnd_cne_camps_journal`引用22州的开始/停止按钮，JE失效调用统一停止；按钮只在 `region_state:CNE` 存在时显示。开始效果同时标记国家的该州项目与实际州，给予州修正、国家反对及军官反对；停止从该state_region下所有state清州收益，清国家和登记军官的对应成本。源：[nesnd_cne_programs.txt:37](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_cne_programs.txt:37>)、[nesnd_cne_programs.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_cne_programs.txt:1>)、[nesnd_cne_programs.txt:24](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_cne_programs.txt:24>)。

清理由原生 `on_state_owner_change` / `on_state_created` 接口触发，先移除已易主state的收益，再为CNE排队次日检查；两天queued标记防同一批分州重复排队，检查 `region_state:CNE` 已不存在时停止该州整套项目。源：[00_code_on_actions.txt:7131](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7131>)、[00_code_on_actions.txt:7174](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt:7174>)、[nesnd_cne_estate_ownership.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/on_actions/nesnd_cne_estate_ownership.txt:1>)、[nesnd_cne_estate_ownership.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_cne_estate_ownership.txt:1>)、[nesnd_cne_confidence.txt:38](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_cne_confidence.txt:38>)。

印度可采用同样的“国家行动记录＋州状态＋所有权变更复核”。但CNE是自有州行政，印度是敌对州活动：不能只把CNE替换为MUG，也不能因原USM州转成起义国就把已建立的地方主权删掉。应分别清秘密组织成本/临时煽动修正、保留真实形成的国家与战争成果。现有CNE按钮的AI概率为0，这个数值不能继承给希望AI也参与的土邦系统；印度AI需用实力、局势和目标收益权衡。

## 4. 原版印度：两条相邻但不同的链

### 4.1 土邦自主JE

原版 `princely_state_decision`要求ip2、`is_princely_state`、未做过、和平、自由欲>=50、合法性>=80、浪漫主义；决定→`je_princely_states`→保存本国、直接宗主及最高宗主→通知宗主、事件1；实际独立且和平完成并发事件2；被吞并失败；每年随机事件反映宗主关系。源：[princely_state_decision.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/decisions/princely_state_decision.txt:1>)、[04_princely_states.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_princely_states.txt:1>)、[princely_states.txt:4](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/princely_states.txt:4>)。

`is_princely_state`依赖原版特殊政体或特定宗教的GBR/BIC/BHT属国，不是“有南亚文化即土邦”。因此不可直接作为本MOD42个独立地方国家的通用入口。原版JE immediate默认有宗主，本MOD独立国家不能直接运行该链。原版MUG JE也因BIC不存在而失效。源：[00_scripted_triggers.txt:1842](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt:1842>)、[04_mughals.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_mughals.txt:1>)。

独立战争的标准对象是自己的**直接宗主**：`dp_independence`指向 `independence`，后者valid写 `root.overlord = scope:target_country`。不是把MUG设成一切印度独立战争的对象，也不是给刚从USM直接州建立、并未形成属国关系的新国套同一战目标。外交博弈还要求原生关系阻挡检查；不会因按钮满足自定义实力条就自动合法。源：[00_diplomatic_plays.txt:202](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:202>)、[10_independence.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/war_goal_types/10_independence.txt:1>)。

### 4.2 兵变与多国起义

原版 `je_uneasy_raj`三大管区稳定与计时→失败/危机调用 `.3`→immediate创建/恢复反乱国并决定土邦态度→选项运行各管区强度效果→`dp_sepoy_mutiny`与具体战争目标→`je_sepoy_mutiny`按反乱国存亡、领地与战争结束判定。源：[04_sepoy_mutiny.txt:1](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sepoy_mutiny.txt:1>)、[04_sepoy_mutiny.txt:234](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sepoy_mutiny.txt:234>)、[sepoy_mutiny_events.txt:1798](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/sepoy_mutiny_events.txt:1798>)、[00_sepoy_mutiny_scripted_effects.txt:2794](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2794>)、[04_sepoy_mutiny.txt:422](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sepoy_mutiny.txt:422>)。

可借的是**当地独立主体＋独立加入的诸邦＋分区影响＋实际战争目标**：KNO起义有自己的KURNOOL/CIRCARS目标；土邦收到 `.4`后选择加入地方战场，`sepoy_mutiny_tag_specific_war_goals`按其文化/地区添加本国目标，并非把一切战果归MUG。源：[00_sepoy_mutiny_scripted_effects.txt:2258](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2258>)、[sepoy_mutiny_events.txt:1938](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/sepoy_mutiny_events.txt:1938>)、[00_sepoy_mutiny_scripted_effects.txt:2642](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2642>)。

不能复制的闭包：

- 原版BIC/GBR/管区/历史province/TAG硬编码；KNO、SAT、PAN、MUG在本MOD本来已有领土，不能反复create_country覆盖现存政权。CAR、MYS可用性也须逐次核TAG与本地地理，不凭原版截图决定。
- 原版土邦态度先遍历宗主属国、以自由欲判断、再删除对BIC的关系；本MOD42个独立地方国家不在该属国列表。原版还带英国受挫后的Raj收尾，不能让USM兵变改变成英国统治。源：[00_sepoy_mutiny_scripted_effects.txt:2521](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2521>)、[04_sepoy_mutiny.txt:471](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sepoy_mutiny.txt:471>)。
- `dp_sepoy_mutiny`默认 `annex_country`，不允许谈判和平；原版加入反叛的土邦会被追加BIC吞并目标。这是特定硬战设计，**不是通用反殖民战争的中性模板**。给独立KNO套此play意味着USM争取吞并整个KNO，不只是恢复起义州。源：[00_diplomatic_plays.txt:1368](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/diplomatic_plays/00_diplomatic_plays.txt:1368>)、[sepoy_mutiny_events.txt:2020](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/india_events/sepoy_mutiny_events.txt:2020>)。
- 原版局部存在必须重新核验的形状：Carnatic建国分支检查Bombay进度、南方防重复检查 `dp_secession` 而实际创建 `dp_sepoy_mutiny`。本报告只记录源码事实，不宣称是已复现引擎BUG，不照抄这些细节。源：[00_sepoy_mutiny_scripted_effects.txt:344](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:344>)、[00_sepoy_mutiny_scripted_effects.txt:2263](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:2263>)。

上述JE/按钮使用原生组、进度条、国家事件与原生图标路径；实现首批可沿用原生容器，无须另造复杂GUI。原版引用的ip2决策/事件并不等于新自定义JE必须强制整条ip2入口；凡直接复用DLC资源或模板另核授权/可用性，不能把不可用资源当存在。

## 5. 提案：本国主权JE共享规则，按当前身份分路

通用的是规则与动作，不是共同宗主或共同终局。建议一套country-context父JE，根据当前是否有宗主切换条件式状态/按钮；战争期间进入同一行动的战时阶段。保存 `actor / target_overlord / sponsor / operation / stage`，不用一个全印度global变量代表每一国。MUG仍有专门帝国改革主线；共享系统可供其地方关系调用。

|阶段/版本|玩家行为|真实结果与退出|
|---|---|---|
|独立国家：保全本邦|行政、军队/供给和财政建设；选择保持独立、寻求条约保护、区域合作、加入协商联盟|不显示“从MUG独立”或凭空自由欲；完结靠本国能力与兑现的外交安排，成为属国则切换下列版本|
|属国：争取自主|向**当前直接宗主**交涉；自强；向可用外部国家求支援；选择维持安排、提高自治或独立|TRA开局对USM；未来HYD若被MUG或FRA附庸，按真实对象。宗主改变使旧请求失效；实际独立且和平完成，非点请求按钮便完成|
|危机：谈判或战争|目标双方作决定；赞助者单独答复；自主/独立走合法外交机制，拒绝可能推进战争|盟约/援助不同于自动参战；发动者与受援者都可失败、失去主权甚至亡国。没有自动复活/强制转国保控|
|独立后的发展|学校、行政、军需与区域贸易；有限承担统一事业或继续本邦路线|可以保持独立、协商联邦/保护或自愿并入，结果各有成本。统一形成数据库另行核验；不以民族主义直接吞并全部印度国|

需避免“独立即完成永不再见”的共享JE：主权危机可完成并记录成功，但本国发展入口继续；后来再次附庸可开启新危机周期，不重领旧奖励。共和制/换王朝不是本系统自动失败；其与王朝专项任务的关系分别判断。分散国家不是有组织国家的自动失败版。

## 6. 提案：逐州支持南印度起义

### 6.1 入口与成本

MUG及后续具备条件的本地政治主体可拥有“南方的主权”JE。战略入口是 **（实际摆脱殖民/外国宗属约束）OR（军政财政能力与地区联系已足以行动）**，不是把两者改成AND，也不是仅把“解放法国”当唯一前置。国家能力分支需在后续实现前核真实军力/预算/技术/通路；本轮不填无来源的固定营数、GDP或进度。

两个分支都仍有行动条件：行动国存活、有实际合法外交能力、目标还是USM所持的选定印度state、当地合作对象/组织条件成立、没有冲突的同一行动、能支付本次成本。脱离控制只是战略资格，不能令微小独立国无限免费发动起义；“强 enough”也不会绕过原生停战和外交许可。MUG仍向FRA朝贡时可发展组织与谈判，能否直接加入战争要单独过原生合法性检查。

界面借CNE逐州开始/停止：每个目标按钮显示该州组织状态、实际支出、当地风险和支持者；只有条件齐备才出现“发动”按钮。不是先给MUG整片南印度claim再贴起义文案。联络/输送/起事/战争分阶段，成本对应真实资金流、限时修正或已证明支持的条约，不永久免费产军。详细量纲按技能数值契约及实际经济基线后定。

### 6.2 对象、所有权与地方选择

同一state只允许一个主组织行动；多国资助可登记为同一行动的不同参与者，防按国重复加同一种动员收益。身份同时记录初始USM state、state_region、地方主体及发起国；分州后重选/终止而非指向失效state。

地方主体按次序选择：已有适当地理/文化利益、且愿意参与的现存国家→本地新政权（仅TAG空缺、划定种子province确属USM时建立）→没有合适主体则暂只保留组织压力，不伪造新国。KNO/TRA/HYD不是可任意拿来更换政府的工具；现存国家可以拒绝，也可与MUG在其他方向对立。MYS/CAR是否作为建国候选需另核定义、首都和人口/军队初始化。不要从中国本土复制USM的文化、法律、军队给反殖民新国。

最小实现建议先选择一个明确的地区与当地主体闭环（例如现存KNO参与、争取USM的KURNOOL州），再扩至其他州。这条路线在已有国家提供领土主张时表现为地方支持下的解放战争；若要在USM州内真正形成独立起义军，须另走建国/分裂分支，不能把前者的外交战宣称为后者已实现。

### 6.3 发动与结算

|场景|建议行为|禁止的捷径|
|---|---|---|
|现存属国争取独立|对实际直接宗主走自治/独立谈判和合法play；他国自愿支援|对无宗属关系的USM或MUG添加无效independence目标|
|新生本地起义国|转出核定的USM种子领土，配置有限军政初始化；建立压制/主权战争，双方目标明确|create_country立即吞全部南印度；新国继承USM全部本土制度；无战争永久免费割地|
|既存独立地方国参与|本人同意后加入对应博弈；可争取本地USM州，承担自己实际承诺的风险|未经同意让所有土邦参战；把原版“可吞并整个参战土邦”的默认目标隐蔽继承|
|地方胜利|按战争目标保留地方主权/领土，再选择独立、条约保护或已同意的联盟|所有胜利州自动set_state_owner=MUG；把FRA资助自动变成FRA宗主权|
|USM胜利|按目标收回种子领土或维持既定宗属；组织失败进入冷却，地方主体可以灭亡|无条件失败后原地重建反复刷兵；未写入战争目标却吞并既存地方国全部领土|
|白和/退让/部分结果|以实际领土、关系、和平状态分类结算，保留部分解放|仅凭“没有正在打仗”当全面胜利；全局终局变量结束其他邦仍在进行的战争|

第一版不直接复用 `dp_sepoy_mutiny` 的吞并/禁止谈判预设；以本次冲突需要的有限目标设计专用play或适用原生play，再核双方获胜/退让的实际处理。战争目标的引擎效果不能靠静态脚本推断全部结果，列为后续定向实测项。

## 7. 大国影响与必须封闭的例外

|参与者|可选利益与行动|不得自动赋予的结果|
|---|---|---|
|MUG|资助反吴、邀入联合、承认地方君主/共和政府、要求共同防务；也可与诸邦竞争甚至征服|“反吴＝拥莫卧儿”；援助换来全部领土或文化统一|
|USM|改革/让步、停止吞并、维持附庸、镇压或分化起义、与某邦达成保护协议|所有南印度州都视为完整USM地区；中国本土社会等级因印度JE整体切换|
|FRA|支持现朝MUG、支持另一本地力量、援助或促和；利用条约维护商业/军事利益|既有对MUG宗主权扩展至全部印度；一项法援合同自动保证参战|
|地方国家|拒绝大国、换赞助者、保持独立、联合或对抗其他地方国家|被视为只有“加入MUG/消失”两种未来|

赞助请求借波兰pending闭环：一个请求一身份，回复重验国/州/关系/期限/战争状态；拒绝/过期/发起者亡国清本次锁，不清掉后来新发的请求。更换赞助者要结清旧合同与承诺；成本、冷却属于行动国/本次行动，不能给其他国家继承刷取。

以下均须纳入实现验收：目标易主或被分州；USM亡国/变TAG/失去印度；土邦灭亡又重建；王朝倒台或革命国家继承；赞助者变敌对或为宗主；在外交博弈中迟答；已参另一战争；停战；已签军事支援但未参战；本国被MUG/FRA/USM之一附庸；同一地区多国同时赞助；双方同时满足终止条件。玩法暂停/失效仅清临时支持、待答和修正，不能撤销已合法获得的领土、工厂、人物或国家存在。

原版资源链的证据只证明存在相关接口和实例。定向游戏验证至少要覆盖：按钮预览零缺scope、请求迟答、州易主、已有TAG与空TAG、双方战争胜败/退让、赞助者拒绝与加入、存读档不重置、独立↔属国版本迁移；本轮均未运行。

## 8. 与现有计划的衔接与范围

把原计划“印度诸邦”从MUG单向统合任务改为：MUG的诸邦外交＋各地方国家共享主权JE＋南印度逐州组织行动。阶段仍为基本行政/财政/军队→自强和援助→有条件的对外行动，但反吴开放条件明确保留独立OR能力。大国互动使用真实收件国和合约；起义胜利后的联合单独协商，不能混入战果处理。

实现顺序建议：有效开局关系与MUG初始化兼容→一个独立邦/TRA属国的共享JE→一个USM州与当地主体的单次行动闭环→双方战争结算→扩展逐州按钮与AI→印度联合后继。此顺序是本次研究建议，不是授权写入游戏的声明。维护规则没有新增需要改技能的证据；本轮未改技能、任务跟踪或MOD。

## 附表：实际地方TAG与领土

下列“独立”严格表示有效开局外交历史未配置宗属；所有地区名均为 `state_region`，表格指该TAG持有的state，**不表示拥有整个地区**。国家类型、主文化由当前有效定义重读；人口与主文化不能代替本国政体/主权判断。

|TAG|国家类型／主文化|历史主权|实际持有地区（源行）|
|---|---|---|---|
|ALW|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4590>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4104>)|
|ASM|[unrecognized / assamese](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2915>)|独立（历史无宗属配置）|[ASSAM](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4367>)|
|AWA|[unrecognized / avadhi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1418>)|独立（历史无宗属配置）|[AWADH](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4398>)|
|BAG|[unrecognized / bageli](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4787>)|独立（历史无宗属配置）|[BUNDELKHAND](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9348>)|
|BAS|[unrecognized / gondi telegu](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1432>)|独立（历史无宗属配置）|[CENTRAL_PROVINCES](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4157>)|
|BER|[unrecognized / gujarati marathi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1444>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4255>)|
|BHO|[unrecognized / marathi pathan](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1456>)|独立（历史无宗属配置）|[MALWA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4310>)|
|BHV|[unrecognized / gujarati](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4742>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4293>)|
|BHW|[unrecognized / panjabi sindi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4467>)|独立（历史无宗属配置）|[PUNJAB](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4140>)|
|BIK|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1468>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4079>)|
|BUN|[unrecognized / bundeli](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1479>)|独立（历史无宗属配置）|[BUNDELKHAND](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9352>)|
|COC|[unrecognized / malayalam](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4966>)|独立（历史无宗属配置）|[TRAVANCORE](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4196>)|
|COO|[unrecognized / bengali](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4642>)|独立（历史无宗属配置）|[WEST_BENGAL](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4354>)|
|DHA|[unrecognized / gujarati](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4720>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4268>)|
|GAR|[unrecognized / pahari](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4566>)|独立（历史无宗属配置）|[AGRA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9376>)；[HILL_PUNJAB](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9405>)|
|GWA|[unrecognized / marathi bundeli](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1491>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4112>)；[MALWA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4306>)|
|HYD|[unrecognized / deccani](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1503>)|独立（历史无宗属配置）|[CENTRAL_PROVINCES](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4148>)；[HYDERABAD](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4245>)|
|IDA|[unrecognized / gujarati](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4698>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4272>)|
|IND|[unrecognized / marathi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1527>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4116>)；[MALWA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4302>)|
|JAI|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1539>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4095>)|
|JAS|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1551>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4083>)|
|JEY|[unrecognized / oriya](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4822>)|独立（历史无宗属配置）|[CIRCARS](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4128>)|
|JHN|[unrecognized / bundeli](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4665>)|独立（历史无宗属配置）|[BUNDELKHAND](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9360>)|
|JOD|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1563>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4091>)|
|JUN|[unrecognized / gujarati pathan](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4730>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4289>)|
|KHP|[unrecognized / marathi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4776>)|独立（历史无宗属配置）|[BOMBAY](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4332>)|
|KKI|[decentralized / lushai](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4622>)|分散国家|[ASSAM](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4383>)|
|KNO|[unrecognized / pathan deccani telegu](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4809>)|独立（历史无宗属配置）|[KURNOOL](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9337>)|
|KOT|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4687>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4108>)|
|KUT|[unrecognized / gujarati](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1597>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4259>)|
|MEW|[unrecognized / rajput](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1631>)|独立（历史无宗属配置）|[RAJPUTANA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4087>)|
|MGH|[decentralized / naga](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4632>)|分散国家|[ASSAM](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4387>)|
|MNP|[unrecognized / manipuri](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:2930>)|独立（历史无宗属配置）|[ASSAM](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4375>)|
|MYB|[unrecognized / oriya](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4833>)|独立（历史无宗属配置）|[ORISSA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4055>)|
|NAG|[unrecognized / marathi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1656>)|独立（历史无宗属配置）|[CENTRAL_PROVINCES](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4153>)|
|NAR|[unrecognized / oriya](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4855>)|独立（历史无宗属配置）|[ORISSA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4063>)|
|NAW|[unrecognized / gujarati](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4709>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4276>)|
|NGA|[decentralized / naga](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4602>)|分散国家|[ASSAM](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4371>)|
|PAN|[unrecognized / panjabi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1692>)|独立（历史无宗属配置）|[PUNJAB](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4136>)；[HILL_PUNJAB](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9409>)|
|PLP|[unrecognized / gujarati pathan](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4753>)|独立（历史无宗属配置）|[GUJARAT](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4280>)|
|PTA|[unrecognized / panjabi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4578>)|独立（历史无宗属配置）|[DELHI](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4417>)；[HILL_PUNJAB](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9413>)|
|PTN|[unrecognized / oriya](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4844>)|独立（历史无宗属配置）|[ORISSA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4059>)|
|SAT|[unrecognized / marathi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4765>)|独立（历史无宗属配置）|[BOMBAY](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4328>)|
|SIN|[unrecognized / sindi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1715>)|独立（历史无宗属配置）|[SINDH](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4071>)|
|SUR|[unrecognized / chhattisgarhi](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4798>)|独立（历史无宗属配置）|[BUNDELKHAND](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9356>)|
|TIP|[decentralized / lushai](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:4612>)|分散国家|[ASSAM](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4379>)|
|TRA|[unrecognized / malayalam](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/country_definitions/00_countries.txt:1727>)|USM puppet|[TRAVANCORE](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:4188>)|

证据清单：[完整SHA-256与扫描范围](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-india-plan-revision-20261102/india-princes-uprising-sources.json>)。报告构建脚本同时重新解析历史，列出该范围全部关系调用及四类分散国家；源码清单中的完整外交历史扫描用于支持“无宗属配置”的有限否定结论。引用行号和SHA绑定本轮文件，不认证任何未运行的引擎行为。
