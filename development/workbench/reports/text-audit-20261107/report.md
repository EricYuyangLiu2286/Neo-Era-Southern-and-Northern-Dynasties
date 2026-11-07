# NESND 本地化审核 · 2026-11-07

**审核界限**　2026-11-07T17:19:15.0127723+00:00（伦敦，UTC+0；严格晚于）。任务 68 的两轮剧透审核均已记入 `.scratch/debug-release/issues/68-description-spoilers.md`。该报告未署时分秒，采用最终落盘时间。备份目录中的两轮文件早于该时间。

Git 工作副本基线 `7c52e222536ef92f5074471866338f1aafd26f9e`。检查所有本地可见分支的提交者时间。游戏加载目录与 Git 分开；无提交的新增文件以及内容异于 Git 的本地版本用文件修改时间。仅换行不同视为同一版本。

## 审核范围与计数

入选 9 组、18 份文件；4 组、8 份纳入本次交付，其余 5 对波斯专档交外审。共用结案文件中两个波斯条件键及两个波斯结案键的双语原文均保留。原作同字段样本取自 original-20261030 的 ce_french_empire_journals_l_simp_chinese.yml 和 ce_cne_events_l_simp_chinese.yml。

波斯另有 86 条工作底稿留作外审。下列表格只计算实际写入的修改。

| 完整文件 | 审前键数 | 判定依据 | 时间（UTC） | 修改条数 |
|---|---:|---|---|---:|
| `localization/english/replace/nesnd_france_court_l_english.yml` | 49 | Git 无此文件，取主 MOD 修改时间 | 2026-11-07T17:39:20.375261+00:00 | 3 |
| `localization/english/replace/nesnd_india_l_english.yml` | 234 | 主 MOD 版本未提交，取主 MOD 修改时间 | 2026-11-07T17:49:50.003395+00:00 | 6 |
| `localization/english/replace/nesnd_japan_l_english.yml` | 350 | 主 MOD 版本未提交，取主 MOD 修改时间 | 2026-11-07T18:18:21.2975952Z | 9 |
| `localization/english/replace/nesnd_journal_closures_l_english.yml` | 40 | 主 MOD 版本未提交，取主 MOD 修改时间 | 2026-11-07T18:11:37.477953+00:00 | 2 |
| `localization/simp_chinese/replace/nesnd_france_court_l_simp_chinese.yml` | 49 | Git 无此文件，取主 MOD 修改时间 | 2026-11-07T17:39:20.376767+00:00 | 7 |
| `localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml` | 234 | 主 MOD 版本未提交，取主 MOD 修改时间 | 2026-11-07T17:49:49.964533+00:00 | 31 |
| `localization/simp_chinese/replace/nesnd_japan_l_simp_chinese.yml` | 350 | 主 MOD 版本未提交，取主 MOD 修改时间 | 2026-11-07T17:38:57.295922+00:00 | 48 |
| `localization/simp_chinese/replace/nesnd_journal_closures_l_simp_chinese.yml` | 40 | 主 MOD 版本未提交，取主 MOD 修改时间 | 2026-11-07T18:11:37.476953+00:00 | 15 |

每个语言文件中的一个键按一处计，按首要问题归类。一个废键在中英各删一次，计两处。

**技术错误 40 处**、**AI 八股 53 处**、**剧透 10 处**、**机械性 18 处**。

## 技术错误（40）

| 文件 | 键 | 原文 | 新文 | 理由 |
|---|---|---|---|---|
| `nesnd_france_court_l_english.yml` | `nesnd_court_royal_reason` | The Paris delegation has brought plans for a new quay. A provincial manufacturer waits three days in the corridor before a minister asks about freight. He lays two invoices on the desk. One gives the cost of landing a boatload of coal in Paris, the other the cost of getting it to his factory gate. The new king has yet to put his signature on a single drawing. Both men want the first. | The Paris delegation has brought plans for a new quay. A provincial manufacturer waits three days in the corridor before a minister asks about freight. He lays two invoices on the desk. One gives the cost of landing a boatload of coal in Paris, the other the cost of getting it to his factory gate. The court has yet to approve a single drawing. Both delegations want theirs signed first. | 【中】摄政时也可显示，不应断言新王亲批。 |
| `nesnd_france_court_l_english.yml` | `nesnd_court_activation` | The imperial succession has been settled and a Bourbon or Orléans monarch holds the French throne. | The imperial succession is settled. A Bourbon or Orléans holds the French throne, or is the heir during a regency. | 【中】政体触发在摄政时查储君。 |
| `nesnd_france_court_l_english.yml` | `nesnd_france_court.1.marked` | The auditor adds up both columns twice. The towns favored by the ministry have grown and now account for a larger share of the country’s urban centers. When the minister gives the table to the press, he asks the compositor to print the totals exactly as they stand.\n\nFrance gains #g 10#! Prestige for #v 24#! months. | The auditor adds up both columns twice. The towns favored by the ministry have grown and now account for a larger share of the urban centers in metropolitan states whose borders remained unchanged. When the minister gives the table to the press, he asks the compositor to print the totals exactly as they stand.\n\nFrance gains #g 10#! Prestige for #v 24#! months. | 【中】份额仅以可比本土州为分母。 |
| `nesnd_india_l_english.yml` | `nesnd_india_reform_status` | The government is establishing schools and workshops. | 〔删除此键〕 | 【低】日志显式使用三路状态文本，覆盖旧默认状态。 |
| `nesnd_india_l_english.yml` | `nesnd_india_reform_finished_tt` | Complete Schools and Administration and Workshops and Armies. | 〔删除此键〕 | 【低】两项改革的完成提示各有专键，旧合并提示无调用。 |
| `nesnd_india_l_english.yml` | `nesnd_india_uprising_reason` | The Southern Court relies on ports, garrisons and local allies to sustain its rule. Its opponents also need organisation, money and friends. Delhi can assist them without treating their lands as its reward. | The Southern Court relies on ports, garrisons and local allies to sustain its rule. Its opponents also need organisation, money and friends. Our government can assist them without treating their lands as its reward. | 【中】担任赞助方的印度政权不限于德里，主语改为当前政府。 |
| `nesnd_india_l_english.yml` | `nesnd_india_contact_desc` | Support local opponents of colonial rule as they prepare to rise. | Local organizers need messengers they can trust and backers willing to pay. | 【中】四种按钮共用描述，避免暂停时误显示为继续资助。 |
| `nesnd_india_l_english.yml` | `nesnd_india_preparation_tt` | Preparation in this region has reached 100. | 〔删除此键〕 | 【低】六地各用自己的举事条件，筹备值由脚本直接判断。 |
| `nesnd_india_l_english.yml` | `nesnd_india_usm_ready_status` | The Tianzhu Commission can now be established. | Enough mainland regions are under direct rule to meet the territorial requirement. | 【中】状态只核对直辖地区数，原文误报为全部条件满足。 |
| `nesnd_japan_l_english.yml` | `nesnd_japan_send_terms_requirements` | Wu and Japan are at peace, with no truce between them, and neither is committed to a diplomatic play. Japan is independent or a Wu subject, is ruled by a Toyotomi, Tokugawa or Yamato monarch, and fully owns Kyoto, Kanto, Kansai and Chugoku. Fu and Wa have yet to be established. | Wu and Japan are at peace, with no truce between them, and neither is committed to a diplomatic play. Japan is independent or a Wu subject, is ruled by a Toyotomi, Tokugawa or Yamato monarch, and fully owns Kyoto, Kanto, Kansai and Chugoku. Fu and Wa have yet to be established. Japanese holdings in Honshu, Hokkaido, Kyushu and Shikoku must be controlled by Japan or Wu. | 【中】唯一的遣使条件提示遗漏了日本诸岛日属地不能被第三国占领的判定。 |
| `nesnd_japan_l_english.yml` | `nesnd_japan.1.d` | The envoys from Nanjing propose to divide the realm. Kyoto and Osaka would recognize the Emperor, the Tokugawa would rule from Edo, and the Toyotomi would govern western Kansai and Chugoku. Wu would administer Kyushu and Shikoku directly. The levies and revenues of the eastern domains would henceforth answer to several governments. The retainers have laid their accounts of troops and provisions before &#91;ROOT.GetCountry.GetRuler.GetFullName&#93;, who must decide how to answer. | The envoys from Nanjing propose to divide the realm. Kyoto and Osaka would recognize the Emperor, the Tokugawa would rule from Edo, and the Toyotomi would govern western Kansai and Chugoku. Wu would administer Kyushu and Shikoku directly. The levies and revenues of the eastern domains would henceforth answer to several governments. The retainers have laid their accounts of troops and provisions before the assembled council and await an answer. | 【中】事件未保证当前统治者存在，避免称谓处显示空名。 |
| `nesnd_japan_l_english.yml` | `nesnd_japan.2.d` | Japan’s envoys have declined the proposed settlement. An expedition would require Nanjing to provide funds and ships to install the three houses in their domains. The court may also withdraw its demands and leave Japan under a single government. The decision rests with &#91;ROOT.GetCountry.GetRuler.GetFullName&#93;. | Japan’s envoys have declined the proposed settlement. An expedition would require Nanjing to provide funds and ships to install the three houses in their domains. The court may also withdraw its demands and leave Japan under a single government. The decision rests with the court in Nanjing. | 【中】事件未保证当前统治者存在，避免称谓处显示空名。 |
| `nesnd_japan_l_english.yml` | `nesnd_jp_mercantile_ports_desc` | Allow merchants to trade overseas, using tariffs to support state revenue and domestic commerce. | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_japan_l_english.yml` | `nesnd_jp_protected_ports_desc` | Open the sea routes to obtain the materials our factories need, while using tariffs to support domestic producers in the wider market. | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_japan_l_english.yml` | `nesnd_jp_political_opposition_desc` | War and Radicalism | 〔删除此键〕 | 【低】进度条改用战争、激进情绪两条独立明细，旧合并键无调用。 |
| `nesnd_japan_l_english.yml` | `nesnd_jp_development.2.t` | Reform Takes  | Reform Takes Root | 【中】在审核期间英文标题被截成半句；按本轮开工备份补回缺失的单词。 |
| `nesnd_japan_l_english.yml` | `nesnd_jp_mercantile_ports_junior_desc` | Replace seclusion with mercantilism and permit overseas commerce. The common market’s tariffs remain under the control of its leading country. | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_japan_l_english.yml` | `nesnd_jp_protected_ports_junior_desc` | Adopt protectionist trade laws and open our ports. The common market’s tariffs remain under the control of its leading country. | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_journal_closures_l_english.yml` | `nesnd_journal_closures_parent_cne` | This undertaking ends with “&#36;ce&#95;cne&#95;land&#95;reform&#36;”. | While &#36;ce&#95;cne&#95;land&#95;reform&#36; is in effect. | 【中】用于 activation_description，应显示适用期间。 |
| `nesnd_journal_closures_l_english.yml` | `nesnd_journal_closures_parent_qin` | This court agenda ends with “&#36;nesnd&#95;qe1&#95;agenda&#95;journal&#36;”. | While &#36;nesnd&#95;qe1&#95;agenda&#95;journal&#36; is in session. | 【中】用于 activation_description，应显示适用期间。 |
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_court_royal_reason` | 巴黎市政厅送来了新码头的图样。外省来的商会代表也带着图样，在走廊上等了三天，终于等到大臣问起运费。他把两张账单并排摆好：一船煤运到巴黎是多少钱，运到自家厂门口又是多少钱。新国王刚刚登基，两拨人都盼着他在自己的图纸上签第一个字。 | 巴黎市政厅送来了新码头的图样。外省来的商会代表也带着图样，在走廊上等了三天，终于等到大臣问起运费。他把两张账单并排摆好：一船煤运到巴黎是多少钱，运到自家厂门口又是多少钱。宫里还没批下头一项工程，两拨人都想把自己的图纸放在上面。 | 【中】摄政时日志也能开启。用宫廷签押替代必由新王亲自签字的断言。 |
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_court_activation` | 法国帝国主线已经结束，波旁或奥尔良君主已就位。 | 帝位继承已定，法国由波旁或奥尔良家族执政；摄政期间以储君的家族为准。 | 【中】摄政时脚本查储君家族，旧文漏此分支，并把帝国日志称为「主线」。 |
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_france_court.1.marked` | 审计员把两栏数字分别加了两遍。拨款所及的城镇确已扩张，它们在全国账上所占的份额也见了涨。公共工程部长把这张表交给报馆时，特地嘱咐排字工照原样印出末尾的合计。\n\n法国获得 #g 10#! 威望，持续 #v 24#! 个月。 | 部长把审计员的表送去排印，特地用铅笔圈出末栏。只算本期拨款后疆界未动的本土州，领过拨款的城镇所占的份额也涨了。他要报馆把这栏也印出来。\n\n评议结算　法国威望 #g 10#! 点，为期 #v 24#! 个月。 | 【中】实际分母限疆界可比的本土，原称全国。把已发奖励独立排为结算行，保留本键色值和期限。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_reform_status` | 政府正在筹办学校与工场。 | 〔删除此键〕 | 【低】日志显式使用三路状态文本，覆盖旧默认状态。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_reform_finished_tt` | 完成学校与官署、工场与军队。 | 〔删除此键〕 | 【低】两项改革的完成提示各有专键，旧合并提示无调用。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_uprising_reason` | 南朝的统治依靠港口、驻军和愿意合作的地方势力。反对者同样需要组织、经费与盟友。德里可以帮助他们行动，却不能因此把他们的土地视作自己的奖赏。 | 南朝的驻军把守海港，收税却少不了当地人帮忙。反对它的人也在各处找钱、找门路。他们托人捎来的话很明白：肯出钱的可以做朋友，别来做主人。 | 【中】赞助国脚本也允许巴拉特、达罗毗荼等；旧句固定写德里，并先行解释吞并规则。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_contact_desc` | 资助当地的反殖民组织，为公开举事作准备。 | 南方的密信要有人送，愿意出面举事的人也得知道，身后还有谁肯出钱。 | 【中】联络、暂停、恢复与举事共用此键；旧文在暂停时仍说要资助。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_preparation_tt` | 本地区的筹备已达100。 | 〔删除此键〕 | 【低】六地各用自己的举事条件，筹备值由脚本直接判断。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_usm_ready_status` | 已可设立天竺宣慰司。 | 直辖的天竺地区已够设司。 | 【中】状态只核对直辖地区数；战事、外交博弈和筹建间隔另由按钮判断。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_japan_send_terms_requirements` | 吴、日两国均处于和平，未投入外交博弈，且彼此没有停战协定。日本须由丰臣、德川或大和家君主统治，独立或隶属吴朝，完整拥有京都、关东、关西和中国地区。扶国与和国尚未建立。 | 吴、日两国均处于和平，未投入外交博弈，且彼此没有停战协定。日本须由丰臣、德川或大和家君主统治，独立或隶属吴朝，完整拥有京都、关东、关西和中国地区。扶国与和国尚未建立。本州、北海道、九州和四国的日本领地须由日本或吴朝控制。 | 【中】唯一的遣使条件提示遗漏了日本诸岛日属地不能被第三国占领的判定。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_japan_partition_tt` | #bold 日本的领土安排#!\n九州与四国的日本领地转交吴朝。德川据江户和北方诸领建立扶国，和国奉天皇统治京都与大阪。丰臣治关西余部、中国地区及原有朝鲜领地。扶、和成为吴朝保护国，丰臣原属国关系保留，原本独立时成为保护国。三家各自宣称由另两家完整控制的分封首府地区。#v EZO、琉球及其他外国领土不受转移。#! | #bold 日本的领土安排#!\n九州与四国的日本领地转交吴朝。德川据江户和北方诸领建立扶国，和国奉天皇统治京都与大阪。丰臣治关西余部、中国地区及原有朝鲜领地。扶、和成为吴朝保护国，丰臣原属国关系保留，原本独立时成为保护国。三家各自宣称由另两家完整控制的分封首府地区。#v &#36;EZO&#36;、琉球及其他外国领土不受转移。#! | 【中】EZO 是直接露出的国家标签，改为引用已有国名键。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_japan.1.d` | 南京使节带来了分封之议。京都与大阪奉天皇名位，德川以江户为府，丰臣领关西余部与中国地区，九州和四国则归吴朝直辖。海东诸藩的兵力与赋税将从此分属数家。家臣已呈上各地兵力与军粮，等候&#91;ROOT.GetCountry.GetRuler.GetFullName&#93;决定如何答复。 | 南京使节带来了分封之议。京都与大阪奉天皇名位，德川以江户为府，丰臣领关西余部与中国地区，九州和四国则归吴朝直辖。海东诸藩的兵力与赋税将从此分属数家。家臣已呈上各地兵力与军粮，等候裁决。 | 【中】事件显示时只保证收件国存在。移除无守卫的君主姓名回调。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_japan.2.d` | 日本使者未肯接受分封方案。南京若决意东征，就须筹措军饷、调集舰船，扶持三家接管海东诸藩。朝廷也可以撤回要求，让日本保有统一的政府。如何答复，已交由&#91;ROOT.GetCountry.GetRuler.GetFullName&#93;裁定。 | 日本使者未肯接受分封方案。南京若决意东征，就须筹措军饷、调集舰船，扶持三家接管海东诸藩。朝廷也可以撤回要求，让日本保有统一的政府。如何答复，已交由南京朝议裁定。 | 【中】事件显示时只保证收件国存在。移除无守卫的君主姓名回调。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_mercantile_ports_desc` | 准许商人经营海外买卖，以关税维护国家的收入和本国商业的地位。 | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_protected_ports_desc` | 开放海路，让工场取得所需的原料，再以关税扶持本国生产者在新市场中的地位。 | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_political_opposition_desc` | 战争与激进情绪 | 〔删除此键〕 | 【低】进度条改用战争、激进情绪两条独立明细，旧合并键无调用。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_mercantile_ports_junior_desc` | 以重商主义取代闭关，准许本国商人经营海外买卖。共同市场的关税仍由市场主导国制定。 | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_protected_ports_junior_desc` | 改定保护主义贸易法，放开本国口岸。共同市场的关税仍由市场主导国制定。 | 〔删除此键〕 | 【低】开港按钮显式改用 nesnd_sweep 系列说明；旧按钮描述及其共同市场变体均无调用。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_parent_cne` | 此项事务随“&#36;ce&#95;cne&#95;land&#95;reform&#36;”一同结束。 | 「&#36;ce&#95;cne&#95;land&#95;reform&#36;」施行期间。 | 【中】本键用于开启条件，旧文在开启前提示关闭。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_parent_qin` | 此项朝议随“&#36;nesnd&#95;qe1&#95;agenda&#95;journal&#36;”一同结束。 | 「&#36;nesnd&#95;qe1&#95;agenda&#95;journal&#36;」议政期间。 | 【中】本键用于开启条件，旧文在开启前提示关闭。 |

## AI 八股（53）

| 文件 | 键 | 原文 | 新文 | 理由 |
|---|---|---|---|---|
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_reform_reason` | 莫卧儿的旧帝国曾靠君主的声望维系各省，如今的统治者却必须面对新的问题。法国商人与教官带来了财富和新式兵器，也带来了新的债主。国家需要自己的学校和工场，让地方的赋税变成能够保卫它的力量。 | 莫卧儿君主从前凭一道谕令就能向各省征调兵马。如今军中添一批新枪，先得同法国商人议价，再由法国教官教人操练。各省送来的税银，有多少能留下来办自己的学堂和工场？ | 【低】把反复的「新问题、新债主」落到枪款和税银的去向。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_schools_reason` | 帝国需要能看懂账簿的官员，也需要能教会下一代读书的人。德里的一所学院无法代替各省的学校。纸张、教师与稳定的经费，必须一同送到地方。 | 德里的学院每年送得出多少识字的办事员？各省的税册堆在官署里，等着有人来核。地方要开学堂，先生的薪水和学生用的纸都得有着落。 | 【低】用各省缺人核税册说明办学的缘由，删去三项并列总结。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_princes_reason` | 德里、南京与巴黎都向印度诸邦递出了自己的条件。王公们所要保住的不只是祖传的宫殿，还有土地、税收和决定本国命运的权力。合作可以带来援助，却不一定带来自主。 | 德里、南京和巴黎的使节都肯帮王公守住宫门。至于门外的田租归谁，军队听谁号令，几封国书开出的价可大不相同。 | 【低】用王公要保住的收入、兵权替代援助与自主的套话。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_princes_status` | 本国的主权与地方利益仍待守护。 | 王公们还在同各方议价。 | 【低】「地方利益仍待守护」未说明眼前的交涉。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_unified_reason` | 统一使许多边界从地图上消失，却没有消除各省的差别。新的国家必须把税收、教育与公共事务维持下去，让共同的法律在宫廷以外也具有意义。 | 从前隔着邦界打官司，走到界碑就得另投一道状。如今两边奉同一部法令，收税的旧账还各有各的算法。各省百姓要看这新政府怎样断头一桩案。 | 【低】用跨邦诉讼说明统一后待办的事务，去掉抽象的法律意义。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_tianzhu_governance_reason` | 天竺的商人熟悉海路，乡村却有另一套秩序。宣慰使既要维持港口与驻军，也要让学校和税务进入内地。当地王公与村社不会仅因南京的任命就放弃自己的利益。 | 天竺港里的商人知道哪一季来船，也知道关税该交给谁。往内地走，收租有王公，断事有村社。宣慰使若要在那里办学收税，光给他们看南京发的印信可不够。 | 【低】把地方利益写成王公与村社各自掌握的事务。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_foreign_reason` | 法国希望以贸易、投资与军事援助维持在印度的影响，&#91;ROOT.GetCountry.GetName&#93;的政府则需要教师、工程师和军官。借助法国的知识与技术，可以培养本国人才，也会使国家继续依赖巴黎的支持。 | 法国愿意把教师、工程师和教官送到&#91;ROOT.GetCountry.GetName&#93;来。当地要有人懂得开矿练兵，巴黎也有自己的盘算。等学生们能接先生的班时，聘书上那些条件还作不作数？ | 【低】保留随本国变化的国名，以聘用和接班写出双方的利害。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_foreign_status` | 援助与自主之间，需要自己的打算。 | 使团可与法国商议延聘教师、工程师和教官。 | 【低】把空泛的「援助与自主」改为当前可议的三种聘请对象。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;的使团已经抵达，带来了有关两国关系的请求。使者正在等待答复。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;的使者递上国书，在客馆候信。 | 【低】删去「有关两国关系的请求」这一空泛转述。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.2.d` | &#91;SCOPE.sCountry('india&#95;partner').GetName&#93;接受了我们的请求。约定已交付执行，接下来仍要靠本国将它变为成果。 | 使者把&#91;SCOPE.sCountry('india&#95;partner').GetName&#93;签过的文书带回来了。两边议定的事，如今可以照办。 | 【低】把「将它变为成果」改为使者带回的凭据。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.3.d` | &#91;SCOPE.sCountry('india&#95;partner').GetName&#93;拒绝了使团提出的条件。我们仍须寻找自己的出路。 | &#91;SCOPE.sCountry('india&#95;partner').GetName&#93;退回了国书。使团照原路返程，没能带回一纸约定。 | 【低】用退回国书交代交涉的结果。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d1` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;请求法国派遣教师，并拨款支持初期办学。使者希望以此培养本国人才，法国也将借顾问团扩大在当地教育中的影响。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;的使者想从法国请几位教师，连办学的钱也想在巴黎筹。他说，学堂可以在本国开，头一批先生得劳法国人费心。 | 【低】用办学的具体请求打破七份使团来文的同一句式。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d2` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;请求法国派遣矿业与工业工程师，并拨款协助开办产业。使者希望取得新的生产技术，法国企业也将从这段合作中寻找商机。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;缺的是会勘矿、会办厂的人。使团来法国延请工程师，也来谈开办的本钱。做机器买卖的商人已经打听起这桩生意。 | 【低】将「寻找商机」写为机器商人的行动。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d3` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;请求法国派遣军事教官，并拨款协助整训军队。受援国希望改善训练与装备，法国则有机会影响这支军队今后的组织。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;想用法国的办法练兵，托使者来请教官。操典可以随身带去，枪械却要花钱，来文末尾便是请法国拨款的数目。 | 【低】用操典与军械交代教官、款项两项请求。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d4` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;的使者要求扩大自治权，让当地政府自行处理更多事务。我们必须决定是否放宽现有的宗主权。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;的使者来争一件事。凡地方自己办得了的事务，往后别再叫他们把文书送到宗主这里来回跑。 | 【低】删去读者已经面对的「我们必须决定」结句。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_revolt.1.d` | &#91;SCOPE.sState('india&#95;case&#95;state').GetName&#93;的反对者已经公开举事。他们占据地方官署，宣布不再服从旧统治者。现在，是否承认这场分离已成为两国之间的争端。 | &#91;SCOPE.sState('india&#95;case&#95;state').GetName&#93;的反对者占了官署，宣布独立。旧官吏要他们交还印信，门内传出一句话：这地方的公文，今后由我们来签。 | 【低】原句以「是否承认这场分离已成为」绕述争端，改写举事后的行动。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_revolt_ack` | 局势已变。 | 把举事的消息传开。 | 【低】选项原先只说局势有变，改为对举事消息的回应。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_mining_reason` | 征税和征兵曾是武士的本分，开矿、办厂却要仰仗商人。北方的矿藏给江户带来了新的财源，也带来了旧军府不熟悉的合作者。那些不佩刀的人正在积累财富，并开始要求政府保护他们的生意。 | 江户的武士下乡，从前为的是点丁收税。如今矿口塌了，要找商人垫木料钱。佩刀的人头一次得听听柜台后面那位开些什么条件。 | 【低】删去两次「带来了」及泛言的新合作者，留下开矿所需的资本。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_metal_cities_reason` | 城下町原本围着城郭与武士宅邸生长，如今来此谋生的人却越来越多。工人、学徒和小店主住进新街区，他们的孩子也要在这里读书。旧日替领主办事的城镇，正在长成有自己诉求的社会。 | 城下町的街巷原是顺着武士宅子的围墙修的。如今墙外又住满了工人和学徒，等他们的孩子也到了上学的年纪，哪一家肯腾出房子来做学堂？ | 【低】以住处和学堂交代城镇变化，替代「有自己诉求的社会」。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_cash_crops_reason` | 海港把远方的价钱带到了乡间。棉田、桑园和茶山有了新的买主，土地所有者与商人都想从中分得更多。农民日复一日的劳作，也开始受到这些遥远市场的支配。 | 收茶的人带着港口的价钱上山时，桑园的主人也会问一句，今年的生丝卖得怎样。农家到秋后才知道，一片叶子在海那边值多少钱，竟能抵掉自家几个月的辛苦。 | 【低】从收购现场写出农户受海外价格牵动，避免抽象归纳。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_textiles_reason` | 收购生丝与棉花的商人开始把织工集中起来。熟悉的手艺进入了更大的工场，雇工按时领钱，也须服从工头的规矩。对于离开田地的人，这是新的指望。对于商人，这则是把乡村生产握得更紧的办法。 | 商人把生丝和棉花运进工场，来领料的织工也在那里坐下了。从前赶织到半夜，天亮还能歇一晌。如今按日领工钱，连什么时候停梭子，都得听工头的。 | 【低】拆除连续「对于……」的均衡论述，用织工的作息落笔。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_consumer_goods_reason` | 食品、家具和日用器皿的生意，正在从少数富户扩展到更多家庭。经营这些工场的人开始关心普通人的收入：顾客若只能勉强糊口，工场便难以扩大销路，产品的价格与收益也会受到压制。 | 做桌椅的木匠过去只等得起大户的生意。如今街上租屋过日子的人多了，谁家不缺一张桌？可米铺若拿走了工钱的最后一文，再好的桌子也只能搁在店里。 | 【低】把销路与收入的关系写成买卖双方的处境。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_living_standards_reason` | 已经进入工场的人开始盘算房租、米价和孩子读书的钱。他们为城市带来了劳力与税收，也要求从繁荣中得到自己的份额。政府许诺的新生活，终究要落到这些日常开支上。 | 月钱发下来，先扣房租，再留出买米的钱。城里人想送孩子读书，摊开手心一数，剩下的钱可够付先生的束脩？ | 【低】删去重复概括繁荣成果的句子，以一家人的支出写生活水平。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_food_cities_reason` | 粮商带来了买卖，工匠和学徒也跟着留下。新街区需要学校，官府与书商需要纸张。许多过去由乡里宗族包办的事情，开始交到城镇的机构手中。 | 粮船靠岸的地方先有了脚店，又有工匠带着学徒来住。要是住下来的人想送孩子念书，从前村里凑钱延师的那套办法，在码头上该找谁出面？ | 【低】具体说明人口入城后的学务问题，替代笼统的机构移交。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_cohesion_reason` | 幕府治下的诸藩、乡间的宗族和城下町的商人，曾各自维持着一方秩序。学校与官府把远近的地方联结起来，繁荣的工商业又使更多人的生活休戚相关。百姓能否过得安定，国家能否在战争中保护他们，都在改变人们对共同前途的信心。 | 各藩的孩子渐渐读起同样的书，各地的官吏也认得同一道印信。可到了歉收要开仓、开战要出兵的时候，百姓究竟信本地的老爷，还是信那张盖印的告示？ | 【低】删去产业、安定与战争的连续归纳，用百姓向谁求助串起团结问题。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_new_army_reason` | 旧日军队依靠世袭武士与地方关系维持，征募和训练也随各家而异。国家需要有组织的兵员、受过训练的军官和能够听从统一调度的部队。无论以常备军还是国民军承担防务，都应使军事服务于共同的国事。 | 各家的武士认自家的旗号，连点名操练也各有规矩。倘若明日几支人马要合守一个港口，谁带来的枪药，谁听谁的号令？兵册上的这些空白，靠报一个祖传的姓氏填不上。 | 【低】将抽象的军队应服务国事落到合防与指挥。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_open_diplomacy_reason` | 过去的朝贡和海禁把外交、通商交织在宗主的安排之中。我们需要以本国的名义派遣商船、开放港口，同其他国家商谈彼此的利益。持续的自主将使这些往来有一个可以信赖的政府作为依托。 | 商船过去要借宗主的名义出海。到了异国港口，哪怕是本国货主同当地税吏争一笔税，也得托别人捎话。我们要派自己的使节，让他们认得船尾的旗。 | 【低】删去对持续自主的抽象总结。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_choose_court_desc` | 王朝的号召力可以把旧臣与改制者召到一处。保留君主，任用新官员，让议政与实业为国家带来新的力量。 | 请君主为新法用印。旧臣肯来听宣，商人也想知道往后该照哪条法令纳税。 | 【低】由新法下各方关切替代「为国家带来新的力量」。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_choose_military_desc` | 军队需要统一的指挥，国家也需要能够贯彻到底的政令。支持军官们整顿兵制与军需，把地方的人力和财力用于共同的防务。 | 各藩的兵册既要合在一起，军官就要问，临阵时究竟由谁发令？ | 【低】按军官立场写按钮理由，删去双重「需要」。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_choose_representative_desc` | 国事关乎所有纳税、服役和谋生的人。让更多代表参与议政，使官员必须面对公开的讨论，也使国民能够以选票影响政府。 | 税要百姓缴，兵要百姓出，议事时总该给出钱出力的人留个位子。 | 【低】用纳税服役的理由取代选举作用的教科书式说明。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_development.2.d` | 新的任官办法已经推行，国家的法令也改变了权力在各阶层间的分配。旧日凭借门第把持地方的人，如今必须面对由政府确定的职位和权限。参与改制的官员、军人和商人，则在新的秩序中寻找自己的位置。这场改革已经进入日常统治，成为处理国事的准则。 | 地方官署换了任命书。旧日凭家名就能坐上的位子，如今得拿出新法上的凭据。有人读罢文书接过印信，也有人读到末行，才明白自己该把印信交出去。 | 【低】通用结局以任免生效收束，删去「新秩序、自己的位置、处理国事的准则」等空句。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.1.d1` | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;希望扩大自行处理国事的权力，要求我们放宽现有宗属关系的约束。使者认为，更大的自主可以让地方政府及时应对国内事务，同时保留两国之间的联系。 | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;的使者带来一摞须请宗主批复的公文。地方的事等到文书往返才肯办，误了事又算谁的？使者请我们把其中一部分留给当地裁处。 | 【低】用文书为何耽搁说明自治请求，删去重复解释能及时处理事务。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.1.d2` | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;的使者要求结束藩属关系。他们希望从此自行决定外交、军队与通商事务，并以独立国家的身份同我们往来。这份答复将决定我们是否愿意交出原有的宗主权。 | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;的使者请求独立。他想要的，是下回再来递交国书时，可以用本国的名义同我们平起平坐。 | 【低】由使者的身份交代独立，删去「这份答复将决定」的总结。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.1.d4` | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;正为工场建设寻求一笔资金。使者希望我们拨款，帮助他们扩建生产、培养熟练工匠，以日益兴盛的工商业加深双方的往来。 | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;递来开办工场的用款单。机器、匠师和学徒的费用都列在纸上，使者唯独拿不出足够的本钱，想请我们拨款。 | 【低】将「加深双方往来」落实为来使为哪些开支请款。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.1.d7` | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;希望得到我们的许可，同其他日本属国商议归并。他们打算由本国政府主持统一，并承诺只有受邀国家同意才结束其单独统治。我们需要决定是否允许这项合邦计划在现有宗属体系内进行。 | &#91;SCOPE.sCountry('jp&#95;sender').GetNameNoFormatting&#93;的使者要一封准许合邦的文书。他明白宗主可以点头，却不能替另一位藩主落款。只要我们准他出使，他愿自己去讨那个签押。 | 【低】用两份不同的同意区分宗主许可和对方受邀，删去末句设问式概括。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.2.d` | 使者带回了&#91;SCOPE.sCountry('jp&#95;partner').GetNameNoFormatting&#93;的答复。对方已经接受我们的提议，双方将依照商定的安排处理此事。 | 使者回国时，行囊里多了一封&#91;SCOPE.sCountry('jp&#95;partner').GetNameNoFormatting&#93;的复书。末页已经用印，所请照准。 | 【低】通用同意答复原先把同一件事复述两次。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_development.2.d_representative` | 取得选举权的人开始用选票选择代表，报纸也能公开议论政府的行为。官员须面对新的任用办法，而议场内外的争论已经越出旧日少数家族的范围。\n\n新学堂还在把更多人带进这个世界。下一代读书人将怎样运用这些权利，要由他们自己决定。 | 头一批代表入席时，报馆也派了人来。昔日几家人关起门就能定下来的事，如今上午在议场里说了什么，下午选他们来的人就能读到。 | 【低】以选民得知议事经过收束，删去预言下一代的套句。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_establish_edo_reason` | 江户如今统辖着大片北方领地。驻军可以守住要道，却不能替地方筹办一切政务。军府需要任用办事人员，将税收与支出纳入共同的安排。各地城下町也须容纳商人、工匠与离乡谋生的人。只有这些地方能够支撑日常统治，江户才有余力谋求更大的权利。 | 江户派兵能守住北方的要道，可领粮的军士到了城下，常要跑好几个衙门才找得到经手的人。各地府库究竟收进多少，又从哪一本账里付饷，军府自己先得弄清楚。 | 【低】三个分封日志原本都以政府须办事收尾，江户改从北方驻军的饷账写起。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_establish_kyoto_reason` | 京都的公卿与大阪的商人各有自己的交游和利益。朝廷的名位不能直接变成军饷，商人的财富也不会自行成为公用。办理财赋的官员须将现有辖地的收入与政务组织起来，使城市能够供养这个新立的政府。 | 京都的公卿替新朝排好了朝班，大阪的商人却还等着有人来议军饷。朝廷向谁借，拿哪一处的税来还，光抬出天皇的名位还不足以叫人在欠据上署名。 | 【低】以公卿的名位与大阪的财赋写和国建制。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_establish_toyotomi_reason` | 分封使丰臣旧臣失去了支配整个日本的地位，留在西部的军队与家臣却仍须供养。各地收入从哪里征收，谁来办理地方政务，都不能只靠旧日的威望维持。政府须在现有辖地建立可靠的行政机关，使城下町成为办事、征税与雇工的中心。 | 丰臣的旧臣还拿着平定天下时的俸单，府库能支用的却只剩西部诸领的收入。城下町的商户若把同一笔税交给了两位家臣，明日还肯认谁的收据？ | 【低】用旧俸单与新辖地的矛盾取代行政建设清单。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_restoration_conclusion` | 本国原有的原住民复国交涉已经结束。 | 本国不再以原先的身份参与复国谈判。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_america_conclusion` | 围绕&#36;HUS&#36;的大陆扩张议程已经结束。 | 针对&#36;HUS&#36;的扩张计划就此撤下。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_india_society_conclusion` | 原有的印度共同认同议程已经结束。 | 各省共同议定印度政体的商谈就此中断。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_india_princes_conclusion` | 原有印度邦国的对外交涉安排已经结束。 | 王公们不能再循旧例遣使了。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_india_dynasty_conclusion` | 本国围绕王朝维系政治效忠的议程已经结束。 | 再也无人以这个王朝的名义召集各省。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_india_france_conclusion` | 原有的对法交涉及法国顾问安排已经结束。 | 同法国的交涉中止，顾问团撤离。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_india_uprising_conclusion` | 原有的起义联络议程已经结束。 | 通往南方举事者的联络断了。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_japan_cohesion_conclusion` | 原有日本政权主持的国民团结议程已经结束。 | 诸藩与百姓的向背，已由另一个政权面对。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_japan_foreign_conclusion` | 原有日本政权的使节交涉已经结束。 | 旧政府派出的使节收回了国书。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_ottoman_recovery_conclusion` | 奥斯曼复兴政策所维系的军政安排已经结束。 | 奥斯曼旧政府留下的整军办法到此为止。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_ottoman_unity_conclusion` | 奥斯曼国家原有的团结政策已经结束。 | 维系奥斯曼各地的旧政就此废止。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_qin_court_conclusion` | 皇族、士人与军队之间原有的朝议安排已经结束。 | 皇族、士人与军方不再共议国事。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |
| `nesnd_journal_closures_l_simp_chinese.yml` | `nesnd_journal_closures_qin_unity_conclusion` | 维系西秦诸地共同认同的旧有安排已经结束。 | 朝廷已无力再把西秦诸地统在一起。 | 【低】同文件结案文本反复套用「原有……议程／安排已经结束」，改写本案停止的事务。 |

## 剧透（10）

| 文件 | 键 | 原文 | 新文 | 理由 |
|---|---|---|---|---|
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_autonomy_desc` | 请求宗主放宽对本国的约束，将现有宗属关系提升一个自治等级。\n\n若获同意，双方将有 #v 5#! 年停战期。 | 地方的公文来回渡海，急事也耽误成了旧事。请准我们在本地裁处，使者愿以 #v 5#! 年休兵作保。 | 【低】将同意后的停战改为使者当下愿议的条款。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_independence_desc` | 要求宗主解除藩属关系，让本国自行处理内外事务。\n\n若获同意，双方将有 #v 5#! 年停战期。 | 请宗主收回藩属名分。使者带去的国书里另有一条，两国愿约 #v 5#! 年休兵，各守疆界。 | 【低】呈请独立及拟议的停战年期，答复留在事件。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_overlord_capital_desc` | 请求宗主拨款兴办工场、培养熟练工匠，使本国的生产能够成长。\n\n获准后，#v 3#! 年内不能再次获得这项资助。 | 工场要置机器，熟手还得从学徒带起。请宗主拨一笔开办款，往后 #v 3#! 年，我们不为同一桩事再登门。 | 【低】把禁领期限写为请款时的承诺，未预告批准。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_capital_cne_desc` | 以工商业合作为纽带，向北朝争取建设资金，吸引其参与日本的发展。\n\n获准后，#v 3#! 年内不能再次获得这项资助。 | 这份工场用款的账请北朝过目。钱若拨得下来，#v 3#! 年之内，本国自理后续用度。 | 【低】保留期限，以对北朝的请求代替获准后锁定。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_capital_hus_desc` | 以通商和工业发展为由，向东洲争取一笔用于工场建设的资金。\n\n获准后，#v 3#! 年内不能再次获得这项资助。 | 东洲做海外买卖的人多，懂得工场开张时最费本钱。使者只为开办来筹一笔款，#v 3#! 年以内不来续请。 | 【低】以东洲通商和此次筹资解释期限，避免四次照抄冷却句。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_capital_usm_desc` | &#91;SCOPE.sCountry('nesnd&#95;label&#95;usm').GetName&#93;与日本的商业联系由来已久。我们可以循着这些关系寻求资助，为本国工场筹集资本、培养工匠。\n\n获准后，#v 3#! 年内不能再次获得这项资助。 | 同&#91;SCOPE.sCountry('nesnd&#95;label&#95;usm').GetName&#93;来往的海商熟悉日本工场的底细，请他们带使者去谈开办费。往后 #v 3#! 年，不能指望再开这个口。 | 【低】保留动态对象与期限，将给付结论收回到当前筹款。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_union_jap_desc` | 向&#91;SCOPE.sCountry('nesnd&#95;label&#95;jap').GetName&#93;提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。 | 请&#91;SCOPE.sCountry('nesnd&#95;label&#95;jap').GetName&#93;共议归统。天下的政令该从何处发出，使者得让对方听完这一席话。 | 【低】吞并结算留在答复，保留受邀国。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_union_jtk_desc` | 向&#91;SCOPE.sCountry('nesnd&#95;label&#95;jtk').GetName&#93;提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。 | 使者带着合邦的国书去见&#91;SCOPE.sCountry('nesnd&#95;label&#95;jtk').GetName&#93;。两家的兵册各管各的日子，还要过多久？ | 【低】用合邦当下的争议代替同意后的吞并。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_union_jim_desc` | 向&#91;SCOPE.sCountry('nesnd&#95;label&#95;jim').GetName&#93;提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。 | 请向&#91;SCOPE.sCountry('nesnd&#95;label&#95;jim').GetName&#93;陈明归统的条件。肯不肯共奉一道政令，还得听对方亲口答复。 | 【低】让对方的立场保持开放。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_korean_envoy_desc` | 向朝鲜提出归还属地。朝鲜有宗主时由宗主答复。议定后，本国将交还在庆尚道和全罗道所持的州块，并撤销对两地的宣称。 | 庆尚道、全罗道的属地，我们愿意交回朝鲜，两地的宣称也可以一并谈。朝鲜若有宗主，这封国书就得送到宗主手里。 | 【低】将转交及撤销宣称还原为谈判条件，保留谁有权答复。 |

## 机械性（18）

| 文件 | 键 | 原文 | 新文 | 理由 |
|---|---|---|---|---|
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_france_court.1.growth` | 各地寄回的册页已经订成一卷。审计员在合计数下划了一道线：当年领了工程的地方，如今确实多出了都市街区。这句话足够让部长在议事厅把五年前的许诺再念一遍。\n\n法国获得 #g 5#! 威望，持续 #v 24#! 个月。 | 部长在议事厅念了五年前的许诺，随即翻到审计员作记号的那一页。领过拨款的地方，新添的街区已经逐处登了册。\n\n评议结算　法国威望 #g 5#! 点，为期 #v 24#! 个月。 | 【低】事件选项没有奖励效果栏；把故事写完再独列已发奖项，保留本键数值。 |
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_france_court.1.paris` | 核算地区：巴黎。&#36;nesnd&#95;court&#95;figures&#36; | 巴黎工务呈报。&#36;nesnd&#95;court&#95;figures&#36; | 【低】引文栏按巴黎呈报件的口吻引出原数字。 |
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_france_court.1.provinces` | 核算地区：外省。&#36;nesnd&#95;court&#95;figures&#36; | 外省工务合报。&#36;nesnd&#95;court&#95;figures&#36; | 【低】把系统式「核算地区」改为各省合报的抬头。 |
| `nesnd_france_court_l_simp_chinese.yml` | `nesnd_court_figures` | 都市等级从 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;before')&#124;0&#93;#! 至 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;after')&#124;0&#93;#!，在疆界可比的本土州中所占份额从 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;share&#95;before')&#124;2&#93;%#! 至 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;share&#95;after')&#124;2&#93;%#!。 | 本土各州，疆界有变者另册。所报城镇原计 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;before')&#124;0&#93;#! 级，今计 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;after')&#124;0&#93;#! 级。占同册各州都市总数，原为 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;share&#95;before')&#124;2&#93;%#!，今为 #v &#91;SCOPE.GetValue('nesnd&#95;court&#95;share&#95;after')&#124;2&#93;%#!。 | 【低】按期初和期末两栏写成工务账摘，保留全部四个报值。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_priority_desc` | 将政府的人力与经费集中到这项事业上。 | 国库里这笔钱，学堂要用，工场也要用。总得有一家先领。 | 【低】两个按钮共用此句，以经费争执代替操作说明。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_settlement_desc` | 将各省共同的政治要求确立为国家的制度。 | 各省肯同奉一部宪章，就得在议席上听得见自己的声音。 | 【低】王朝与共和两个按钮都涉及扩大选举，以各省的诉求解释议宪。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_establish_yuanshan_desc` | 将远山的领地交由中央委任的宣慰使治理。 | 远山的驻军等得到海船，等不得每件事都送南京批。 | 【低】把按钮名称的行政释义改为就地设司的理由。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomatic_desc` | 向对方正式提出请求，由其政府作答。 | 把条件写进国书，请使者带一句准话回来。 | 【低】多种请求共用此键，以使节口吻交代交涉。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d6` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;邀请本国并入统一的印度，并提出以年金保障原有王公。接受这一安排，就意味着结束本国的单独统治，将土地与人民交由对方政府管辖。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;送来了合邦的约书。王公名下的年金写得明白，往后本地的税簿要送到对方政府，约书上也写得明白。 | 【低】以约书条款呈现王公要作的选择，避免重复按钮效果。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_diplomacy.1.d7` | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;请求我们承认其独立，由当地政府自行决定内外事务。接受请求将结束现有的宗属关系。 | &#91;SCOPE.sCountry('india&#95;sender').GetName&#93;的来使请求独立。这回他求见宗主，为的是往后两国再通国书时，谁也不必向谁称臣。 | 【低】将生硬的解除关系说明写成来使所求。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_revolt_war_reason` | 旧统治者要求收回这片土地。独立的命运将由这场交涉与战争决定。外国资助不应成为另一个国家吞并我们的借口。 | 旧统治者已来索地，举事的人守着刚接过手的官署。我们向外人借钱时，可曾答应连官署的钥匙也一并交给债主？ | 【低】把资助不会自动吞并的规则转成起义一方的政治立场。 |
| `nesnd_india_l_simp_chinese.yml` | `nesnd_india_suppression_desc` | 以额外的警务开支打击地方秘密组织。 | 巡警要打听出谁在替举事的人递信，手里总得有几个钱。 | 【低】开支数额另有提示，按钮说明只写侦缉缘由。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_japan_reunification_reason` | 海峡两岸的盟约曾替丰臣打开平定诸侯的道路，也让唐土朝廷得以介入日本的继承、封地和征战。城下町的税赋汇往各家府库，军队与商人各认其主。&#91;ROOT.GetCountry.GetName&#93;要重建统一的政府，就须使本州归于一统，并取得自主决定内外政务的地位。 | 海峡两岸的旧盟替丰臣家开过路，也给了唐土朝廷插手封地的由头。如今本州的税各归各家，兵也各听各家号令。&#91;ROOT.GetCountry.GetName&#93;纵能号召诸侯，若连自家的国书都得请外人用印，天下又凭什么归心？ | 【低】本州和自主的硬条件已有目标栏，正文改写为税兵和国书由谁掌握。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_abandon_reform_desc` | 撤回当前改革方针，结束政府为新政进行的动员。改革进度归零，#v 24#! 个月内不能重新提出改革。已有法律和建设保留。 | 请把新政的议案收起来。各处已行的法照旧，已开的工照做。这一搁就是 #v 24#! 个月，再要重提，还得从头召集肯出力的人。 | 【低】将归零和冷却写成搁置政务的代价，保留原带色期限。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_seek_reform_permission_desc` | 请宗主认可本国的制度改革，让我们能够自行筹划官员任用、军政与议政的安排。 | 新法即使只在本国施行，宗主若不首肯，谁肯第一个在文书上署名？ | 【低】用改制者需要许可的理由代替制度分类。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_independence_play_desc` | 向宗主提出独立的最后通牒，发起独立&#91;concept&#95;diplomatic&#95;play&#93;，准备以战争迫使其接受。 | 使节带去的是最后一封国书。独立的要求若谈不拢，这场&#91;concept&#95;diplomatic&#95;play&#93;就得由军队接手。 | 【低】保留博弈链接，用最后通牒的口吻代替操作步骤。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.2.d1` | 宗主已同意放宽对本国的约束，原有的宗属关系升为更自主的等级。双方议定休兵五年，政府可以据此着手处理此前受制的事务。 | 宗主在来书上准我们多办几件原要请示的国事。使节还带回了一份休战文书，约定双方五年不动兵。 | 【低】用允办事务与休战文书呈现答复，去掉自治等级术语。 |
| `nesnd_japan_l_simp_chinese.yml` | `nesnd_jp_foreign.2.d4` | &#91;SCOPE.sCountry('jp&#95;partner').GetNameNoFormatting&#93;同意拨给建设资金。工场扩建与工匠训练有了新的助力。政府须善用这笔资助，三年内不能再获同类拨款。 | &#91;SCOPE.sCountry('jp&#95;partner').GetNameNoFormatting&#93;答应了这笔拨款。工场可以订机器，也可以招学徒了。使者临行时记得最牢的一句，是对方叮嘱三年之内别再来筹同一笔钱。 | 【低】保留援款和三年期限，以来使转述代替领取冷却。 |

## 未确认的未使用键

- `wg_nesnd_japan_reorganization_action_name`　中英均保留。主 MOD 的 `common/war_goal_types/nesnd_japan.txt` 定义了对应战争目标；未找到精确调用，不能排除引擎按对象名取键。
- `war_goal_wg_nesnd_japan_reorganization`　中英均保留。主 MOD 的 `common/war_goal_types/nesnd_japan.txt` 定义了对应战争目标；未找到精确调用，不能排除引擎按对象名取键。
- `war_goal_wg_nesnd_japan_reorganization_desc`　中英均保留。主 MOD 的 `common/war_goal_types/nesnd_japan.txt` 定义了对应战争目标；未找到精确调用，不能排除引擎按对象名取键。

## 英文需同步

- `nesnd_france_court.1.growth`
- `nesnd_france_court.1.paris`
- `nesnd_france_court.1.provinces`
- `nesnd_court_figures`
- `nesnd_india_reform_reason`
- `nesnd_india_schools_reason`
- `nesnd_india_princes_reason`
- `nesnd_india_princes_status`
- `nesnd_india_unified_reason`
- `nesnd_india_priority_desc`
- `nesnd_india_settlement_desc`
- `nesnd_tianzhu_governance_reason`
- `nesnd_establish_yuanshan_desc`
- `nesnd_india_foreign_reason`
- `nesnd_india_foreign_status`
- `nesnd_india_diplomatic_desc`
- `nesnd_india_diplomacy.1.d`
- `nesnd_india_diplomacy.2.d`
- `nesnd_india_diplomacy.3.d`
- `nesnd_india_diplomacy.1.d1`
- `nesnd_india_diplomacy.1.d2`
- `nesnd_india_diplomacy.1.d3`
- `nesnd_india_diplomacy.1.d4`
- `nesnd_india_diplomacy.1.d6`
- `nesnd_india_diplomacy.1.d7`
- `nesnd_india_revolt_war_reason`
- `nesnd_india_suppression_desc`
- `nesnd_india_revolt.1.d`
- `nesnd_india_revolt_ack`
- `nesnd_japan_reunification_reason`
- `nesnd_jp_mining_reason`
- `nesnd_jp_metal_cities_reason`
- `nesnd_jp_cash_crops_reason`
- `nesnd_jp_textiles_reason`
- `nesnd_jp_consumer_goods_reason`
- `nesnd_jp_living_standards_reason`
- `nesnd_jp_food_cities_reason`
- `nesnd_jp_cohesion_reason`
- `nesnd_jp_new_army_reason`
- `nesnd_jp_open_diplomacy_reason`
- `nesnd_jp_choose_court_desc`
- `nesnd_jp_choose_military_desc`
- `nesnd_jp_choose_representative_desc`
- `nesnd_jp_abandon_reform_desc`
- `nesnd_jp_development.2.d`
- `nesnd_jp_seek_autonomy_desc`
- `nesnd_jp_seek_independence_desc`
- `nesnd_jp_seek_reform_permission_desc`
- `nesnd_jp_seek_overlord_capital_desc`
- `nesnd_jp_seek_capital_cne_desc`
- `nesnd_jp_seek_capital_hus_desc`
- `nesnd_jp_seek_capital_usm_desc`
- `nesnd_jp_independence_play_desc`
- `nesnd_jp_union_jap_desc`
- `nesnd_jp_union_jtk_desc`
- `nesnd_jp_union_jim_desc`
- `nesnd_jp_korean_envoy_desc`
- `nesnd_jp_foreign.1.d1`
- `nesnd_jp_foreign.1.d2`
- `nesnd_jp_foreign.1.d4`
- `nesnd_jp_foreign.1.d7`
- `nesnd_jp_foreign.2.d`
- `nesnd_jp_development.2.d_representative`
- `nesnd_jp_establish_edo_reason`
- `nesnd_jp_establish_kyoto_reason`
- `nesnd_jp_establish_toyotomi_reason`
- `nesnd_jp_foreign.2.d1`
- `nesnd_jp_foreign.2.d4`
- `nesnd_journal_closures_restoration_conclusion`
- `nesnd_journal_closures_america_conclusion`
- `nesnd_journal_closures_india_society_conclusion`
- `nesnd_journal_closures_india_princes_conclusion`
- `nesnd_journal_closures_india_dynasty_conclusion`
- `nesnd_journal_closures_india_france_conclusion`
- `nesnd_journal_closures_india_uprising_conclusion`
- `nesnd_journal_closures_japan_cohesion_conclusion`
- `nesnd_journal_closures_japan_foreign_conclusion`
- `nesnd_journal_closures_ottoman_recovery_conclusion`
- `nesnd_journal_closures_ottoman_unity_conclusion`
- `nesnd_journal_closures_qin_court_conclusion`
- `nesnd_journal_closures_qin_unity_conclusion`
- `nesnd_france_court.1.marked`
- `nesnd_india_uprising_reason`

## 跳过的文件

- `localization/english/replace/nesnd_per_faith_l_english.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/english/replace/nesnd_per_mines_l_english.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/english/replace/nesnd_per_rising_l_english.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/english/replace/nesnd_per_tension_l_english.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/english/replace/nesnd_persia_l_english.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/simp_chinese/replace/nesnd_per_faith_l_simp_chinese.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/simp_chinese/replace/nesnd_per_mines_l_simp_chinese.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/simp_chinese/replace/nesnd_per_rising_l_simp_chinese.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/simp_chinese/replace/nesnd_per_tension_l_simp_chinese.yml`　波斯专档，按作者最后指示留给外部代理复核。
- `localization/simp_chinese/replace/nesnd_persia_l_simp_chinese.yml`　波斯专档，按作者最后指示留给外部代理复核。

## 发现的脚本问题

- `common/scripted_buttons/nesnd_jp_politics.txt:7`（另见 109、209 行）同时把 `nesnd_jp_policy_wait` 用于「没有冷却变量」的条件和「有冷却变量」的效果。前者仍可能读取不存在的计时器。需要拆开条件与剩余时间两个显示入口；后者的动态倒计时保留。
- `common/scripted_buttons/nesnd_jp_foreign.txt:68` 等资助按钮在可见条件已排除援助冷却后，又在对玩家公开的 `possible` 中直接检查 `NOT = { has_variable = nesnd_jp_capital_aid_lock }`。界面有显示原生变量条件的风险；应由按钮脚本隐藏重复检查或提供专用条件提示。
- `common/journal_entries/nesnd_india_core.txt:158` 的天竺状态只看地区数，按钮还看战争、外交博弈和筹建间隔。状态行已改述地区条件；如需像远山一样单列完全就绪状态，须再接按钮的完整触发器。

## 校验与抽查

- 日本丰臣段、印度「种姓与公职」和「天朝的荣光和税金」等作者改稿均保留。英文标题在审核期间从 Reform Takes Root 变为截断的 Reform Takes，按轮初备份修复。此前已完成的波斯候选及脚本线索另存工作台同目录 persia-review.json，全部待外审。这两处中文（法国评议高档、印度南方举事缘由）同时修了技术问题，英文只校正事实，两键仍列入英文需同步。
- 确认删除 8 个双语废键。日本两项 `_progress`、日志默认 `_reason`、法国 `_concluded`、国家形容词及有博弈对象的后缀均保留。矿冶 `$MOD$_half` 三个具体键可从效果参数还原，属于已确认使用。
- 游戏外核对 UTF-8 BOM、语言头、引号、同语键唯一、括号与颜色标记、中英键集合、嵌套引用和改动逐键指纹。审前原件保存在 `backup/localization/`。英文仅作技术修订；脚本逻辑及游戏内表现未经本轮实机验证。
- 日本「东洋交涉」先悬停求援和合邦，再看使者答复。应能分清当下呈请、拟议期限与获准后的结果。
- 法国「宫廷与外省」看王党或摄政时的开启说明，再看五年评议的本土比较范围和威望结算。
- 南朝「天竺的土地」在直辖地区满额、仍在战争或外交博弈时核对状态行与设司按钮。
- 日本「国政之争」核对三条路线说明、改换方针的冷却，以及「搁置新政」的 24 个月。
- 印度「南方的烽火」分别悬停联络、暂停、恢复、举事。同一行说明应适用于四种操作，具体开支在各自提示里。

在本目录运行 `python audit.py report` 即可由 `records.json` 重建本报告。使用 `python audit.py verify --mod "主 MOD 路径"` 核对各文件的交付指纹。
