# 日本外交、朝鲜与摄政：逐键编辑对照

2026-11-02。仅写本报告和文本JSON；未修改候选或主MOD，未启动游戏。本轮即使获准在完整检查后启动游戏，也没有由本编辑代理启动。

对象：`WORK/exports/japan-development-20261102-a`。全部结论为 **编辑通过，待装配**；后续仍须根任务复核最终覆盖层、动态scope与脚本SHA。不能据本报告宣称引擎显示、谈判或转地已经通过。

## 作者依据与实际内容边界

A1–A3原始路径、全文取样、SHA及与f18b6c4逐字一致的证明见[作者来源研究](writing-source-study.md)。当前摄政说明是后加文本，只作为本次修订对象，不充当作者文风依据。

|类别|原作者同类样本|本轮选择|
|---|---|---|
|日本外交日志|A1:150“丰臣幕府……依靠大明吴王的支持平定了战国之世……朝鲜的争夺”|从军援、朝贡与商业的历史关系解释当前自主与统一要求。|
|要求兑现承诺|A1:256“我们为南明赴汤蹈火……承诺……领土的归还。”|具体谈判围绕明确权利与交换，拒绝“开展一个合作项目”式空泛流程。|
|答复与立场|A1:261、266从答复方说“他们要求我们……代价”；270“岂有此理！你不过是尽了本分！”|七种请求用接收方视角，接受/拒绝各是实际政治决定，不替另一国家预先答应。|
|自主与制度|A1:332九州、海关、东洋领事府与独立；334“我们不必再遵守锁国令了！”|自治提升、独立、改革许可、统一许可各写清含义，不混成同一个“自主”奖励。|
|利益与政治过程|A2:79写阶层利益转移及强制执行|朝鲜总督/议事会分别涉及税务、行政、教育与地方合作，不凭空加入匿名反对者或道德总结。|
|修正/政治按钮|A2:74“投资狂热”；A3:237“革命君主制和拿破仑的宪政……”|状态名和政治理由保持简洁；费用与修正数字交原生展示，必要冷却另说明。|

## 从草稿到实际契约的返工

- 研究稿曾提供“朝鲜自治”方向；当前实际只是本国州的地方议事会政策，不能把它写成释放朝鲜或提升国家自治等级。本批用“设立地方议事会”。
- 外援是一次实际资金转账、12个月建造与资质支持。全稿删除军械交货、固定采购单、免费工厂、实际转移工匠人口等没有实现的效果。
- 第一版北朝按钮写“北朝有意扩展在东洋的联系”。当前只有日方发出请求，不能代替未回应的北朝作既成判断；改成日方以工商业合作寻资。
- 南朝名称覆盖USM明/吴阶段，北朝覆盖CNE君主/共和阶段；按钮使用“南朝/北朝”而非固定政体全称。东洲沿既定名称。合邦按钮按根任务明确允许使用`$JAP$/$JTK$/$JIM$`基础国家键。
- 合邦是答复国并入提议国，必须直述国家与单独政府被结束，不能仅写“加强合作”或松散联邦。邀请、宗主授权、对方接受是三个不同事实。
- 朝鲜和解只移交提议国持有的釜山/两湖state，并放弃两地区宣称。无领土时仍可交涉宣称，所以请求正文使用“仍持有/any territory it still holds”。没有许诺转移第三方土地或自动取得朝鲜宗主权。
- 旧摄政说明“奉宗主国之命……/commissioned by its overlord”返工：职位可在独立后继续，改为代天皇主持政务。保留现行“摄政政府/Regency Government”“摄政王/Prince-Regent”。

## 技术与显示契约

动态国家名只用于已有事件保存的`jp_sender`、`jp_partner`。前者由reply_valid保护；答复事件有exists/cancellation保护后者。没有在JE按钮中编造GetCountry动态函数。

`RULER_TITLE_EMPEROR`和`RULER_TITLE_EMPRESS`在当前本体两语言均存在：中文`government_l_simp_chinese.yml:925–926`，英文`government_l_english.yml:940–941`。当前政府定义已以这两个原生键作为男女继承人称谓。本批不重复定义、不创建无依据的皇帝键。

6个月是共享派使间隔，45天是请求存续守卫，事件窗口1个月；后两者由请求/事件系统控制，没有混写成六个月答复期限。一次援助后3年不能再获资助，在资金按钮说明中显示。自治提升与协商独立若接受，实际有60个月停战；对尚未发出请求的玩家说明为5年。朝鲜政策24个月不能改换，两按钮均明确这一必要决策信息。

读入源码的朝鲜交涉守卫检查与朝鲜/其直接宗主不存在交战，但未要求全球`is_at_war=no`；已向根任务报告与其最新peace契约的差别，文本没有凭空说已满足全球和平。根任务如补该守卫，原生条件显示即可，不必污染reason。

## 源码指纹

C-JE-F/K、C-EFF-F/K、C-MOD-F/K分别指外交/朝鲜JE、effect与modifier。行号及实际内容以以下SHA为本次编辑对象。

|文件|SHA-256|
|---|---|
|[common/journal_entries/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_jp_foreign.txt>)|`32aa642c7b05dbf26f539f382796963665476e4a42cfe762c8fb4343ced2de8a`|
|[common/journal_entries/nesnd_jp_korea.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/journal_entries/nesnd_jp_korea.txt>)|`603e0835dd165e880cae7e204b5340469683df273453c9b24957334fe9b3bd58`|
|[common/scripted_buttons/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_buttons/nesnd_jp_foreign.txt>)|`751882815ed5281109eb644cace5a09f68eeb1413ba2576eaed154f45094c5a1`|
|[common/scripted_buttons/nesnd_jp_korea.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_buttons/nesnd_jp_korea.txt>)|`2641311927fd8d16ace85c7841a23ff3b9f3d3d4f48056d160cc2f62f35ab478`|
|[common/scripted_effects/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_effects/nesnd_jp_foreign.txt>)|`e4b98a6bde3d200d7bda476918b5a3806badf9b51078151a131973d65e909151`|
|[common/scripted_effects/nesnd_jp_korea.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_effects/nesnd_jp_korea.txt>)|`ca107cd009f3c4c323fdde48ed942ad36d02c68fad4ef5069dcebefe5dbe0734`|
|[common/scripted_triggers/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_foreign.txt>)|`3a3ee2907e40bbd4d6e3ebe31fb433eb503f2f778d22cec84ea0ea12a78bbb08`|
|[common/scripted_triggers/nesnd_jp_korea.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/scripted_triggers/nesnd_jp_korea.txt>)|`c7a3980957a468a0c5361b5c545119c32c90afdc53f174fac2f9d31d7f4a7d9e`|
|[common/static_modifiers/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/static_modifiers/nesnd_jp_foreign.txt>)|`f68a73975f921809a7d8b373d5eb1908986cd57739cffe42c69e70045a55c73e`|
|[common/static_modifiers/nesnd_jp_korea.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/static_modifiers/nesnd_jp_korea.txt>)|`3cd576e095a61e7f1bcaccfd04ae3b92b3249e0951fee9f944d7f09c9ac1f453`|
|[events/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/events/nesnd_jp_foreign.txt>)|`ff16721d51e116c8e5f291b966d2aa7d5b7d1b21559aa6bd1dcd7e2809361c7b`|
|[common/script_values/nesnd_jp_foreign.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/script_values/nesnd_jp_foreign.txt>)|`abeab862e35d96b1c51653e4ed37d52957e7f2f02fd2ebcf637a6435d9f6bce1`|
|[common/government_types/00_nesnd_japan_lin_regency.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/common/government_types/00_nesnd_japan_lin_regency.txt>)|`8817015afc86346baca866098f74cfc50a6bba5793cc3bcea6b6cc9ec6b965e3`|
|[localization/simp_chinese/replace/nesnd_japan_lin_regency_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/localization/simp_chinese/replace/nesnd_japan_lin_regency_l_simp_chinese.yml>)|`8659b5c0727b77eac6c10bebc6b64dfb308bc70c8c49bd4f2efc15768e003acb`|
|[localization/english/replace/nesnd_japan_lin_regency_l_english.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/japan-development-20261102-a/localization/english/replace/nesnd_japan_lin_regency_l_english.yml>)|`cd9852632357a4850dbdeb84aa667deac6c74049b3f000775c43cb4470c99f60`|

## 全键中英候选与决定

逐键检查用词、断句、造句、冗余、视角、触发与效果。必要游戏规则属于操作信息；未把开发步骤或恢复清理流程写入故事。

|键/类别|作者或原生依据|本轮中文候选|本轮英文候选|决定|
|---|---|---|---|---|
|`nesnd_jp_foreign`<br>日志标题|A1:255、272|东洋交涉|Diplomacy in East Asia|编辑通过。适用于独立与附属，避免“旧约”暗示每个请求都是正式条约。|
|`nesnd_jp_foreign_reason`<br>日志正文|A1:150、302、332；D十|日本与大陆的关系，长久由援兵、朝贡和海上买卖维系。丰臣借这些关系平定诸侯，列岛上的政权也因此受到外朝的干预。如今各国都在寻找新的财源与盟友，自主、改革和统一的要求将随着使者渡海而去；对方是否愿意让步，仍取决于它自己的利益。|Military assistance, tribute and maritime trade have long bound Japan to the mainland. These ties helped the Toyotomi overcome their rivals and gave foreign governments a hand in Japanese affairs. Governments now seek new sources of wealth and new partners. Envoys will carry requests for autonomy, reform and union, which their counterparts will judge according to their own interests.|编辑通过。以真实前史与政治利益开篇，不把USM固定为吴或CNE固定为君主；没有交付武器/自动援助承诺。|
|`nesnd_jp_korea`<br>日志标题|A1:150；D五|海峡彼岸|Across the Strait|编辑通过。既适用于持有朝鲜州者，也适用于已统一且无朝鲜地的交涉者。|
|`nesnd_jp_korea_reason`<br>日志正文|A1:150；A2:79；D五|丰臣与吴国的联军征服朝鲜南部之后，煤矿、港口与驻军把两岸的利益紧紧联在一起。朝鲜地方居民希望掌握自己的民政和税赋，列岛的统治者则长期倚赖半岛的资源与航路。地方治理与领土归属，将决定这些旧有关系怎样延续。|After Toyotomi and Wu forces conquered southern Korea, mines, ports and garrisons bound interests on both sides of the strait. Local Koreans seek control over civil affairs and taxation, while Japanese governments have long relied on the peninsula’s resources and shipping routes. Questions of local government and sovereignty will shape the future of these ties.|编辑通过。历史与当下议题分开，不声称玩家现在占有整个半岛或两个完整州；当地政治诉求为本轮明确方案。|
|`nesnd_jp_envoy_away`<br>条件式状态|A1:332；C-JE-F/C-JE-K|使者正在等待对方的答复。|Our envoy is awaiting a reply.|编辑通过。request_clock存在时，未声称已经获准或资助入账。|
|`nesnd_jp_envoy_rest`<br>条件式状态|A1:332；C-JE-F/C-JE-K|使团尚未整顿完毕；两次遣使须相隔 #v 6#! 个月。|The delegation is not yet ready to depart again. Envoys may be sent once every #v 6#! months.|编辑通过。共享派使冷却状态，不把45天请求锁说成六个月答复时限。|
|`nesnd_jp_subject_treaties`<br>条件式状态|A1:332；C-JE-F/C-JE-K|本国仍受宗主约束，可以就自主权与建设寻求交涉。两次遣使须相隔 #v 6#! 个月。|The country remains subject to an overlord and may negotiate over autonomy and development. Envoys may be sent once every #v 6#! months.|编辑通过。无pending/冷却且附属才显示。必要共享冷却只在当前互斥状态出现。|
|`nesnd_jp_independent_treaties`<br>条件式状态|A1:332；C-JE-F/C-JE-K|本国可以自行寻求外援与合邦。两次遣使须相隔 #v 6#! 个月。|The country may seek foreign assistance and union on its own behalf. Envoys may be sent once every #v 6#! months.|编辑通过。非附属且无pending/冷却；合邦仍取决于实际双方权限和同意，不称已达成。|
|`nesnd_jp_korea_across_the_strait`<br>条件式状态|A1:332；C-JE-F/C-JE-K|朝鲜的领土争议仍待交涉。|Territorial questions in Korea remain open to negotiation.|编辑通过。无本国朝鲜州仍可谈宣称；不显示不存在的总督治理。|
|`nesnd_jp_korea_governors_status`<br>条件式状态|A1:332；C-JE-F/C-JE-K|朝鲜属地的税务与民政由总督集中处理。|Governors direct taxation and civil administration in our Korean territories.|编辑通过。policy=1；不把税容加成说成税收额保证。|
|`nesnd_jp_korea_councils_status`<br>条件式状态|A1:332；C-JE-F/C-JE-K|当地议事会参与民政与教育。|Local councils take part in civil administration and education.|编辑通过。policy=2；不写朝鲜国家已经获独立。|
|`nesnd_jp_korea_undecided`<br>条件式状态|A1:332；C-JE-F/C-JE-K|政府尚未确定朝鲜属地的治理办法。|The government has yet to settle how its Korean territories will be administered.|编辑通过。有地且尚无方针时的准确短状态。|
|`nesnd_jp_seek_autonomy`<br>按钮标题|A1:332；D十|争取更多自主|Seek Greater Autonomy|编辑通过。原生increase_autonomy一步，未写成直接独立；五年停战是尚未答复时玩家需要知道的实质结果。|
|`nesnd_jp_seek_autonomy_desc`<br>按钮说明|A1:332；D十|请求宗主放宽对本国的约束，将现有宗属关系提升一个自治等级。<br><br>若获同意，双方将有 #v 5#! 年停战期。|Ask the overlord to relax its control and raise our subject relationship by one autonomy level.<br><br>Acceptance will establish a #v 5#!-year truce between the two countries.|编辑通过。原生increase_autonomy一步，未写成直接独立；五年停战是尚未答复时玩家需要知道的实质结果。|
|`nesnd_jp_seek_independence`<br>按钮标题|A1:332–334|商议独立|Negotiate Independence|编辑通过。只能最高可自治等级后提议；接受才make_independent，未将派使写成已经独立。|
|`nesnd_jp_seek_independence_desc`<br>按钮说明|A1:332–334|要求宗主解除藩属关系，让本国自行处理内外事务。<br><br>若获同意，双方将有 #v 5#! 年停战期。|Ask the overlord to end the subject relationship and recognize our right to govern our own affairs.<br><br>Acceptance will establish a #v 5#!-year truce between the two countries.|编辑通过。只能最高可自治等级后提议；接受才make_independent，未将派使写成已经独立。|
|`nesnd_jp_seek_reform_permission`<br>按钮标题|A1:337–340；A3:237|请求改制许可|Request Leave to Reform|编辑通过。只授political_permission；不附赠独立或合邦许可，不声称直接改法。|
|`nesnd_jp_seek_reform_permission_desc`<br>按钮说明|A1:337–340；A3:237|请宗主认可本国的制度改革，让我们能够自行筹划官员任用、军政与议政的安排。|Seek the overlord’s assent to domestic reform, allowing us to reconsider appointments, military administration and political representation.|编辑通过。只授political_permission；不附赠独立或合邦许可，不声称直接改法。|
|`nesnd_jp_seek_union_permission`<br>按钮标题|A1:302；D十|请求合邦许可|Request Leave to Unite|编辑通过。只授权发起合邦；同一宗主与双方明确同意仍分别核验，未自动吞并。|
|`nesnd_jp_seek_union_permission_desc`<br>按钮说明|A1:302；D十|请宗主允许我们同其他日本属国商议归并，由愿意合邦的双方共同结束分立。|Ask the overlord to permit negotiations with other Japanese subjects over a voluntary union.|编辑通过。只授权发起合邦；同一宗主与双方明确同意仍分别核验，未自动吞并。|
|`nesnd_jp_seek_overlord_capital`<br>按钮标题|A2:69；D十.3|向宗主请求建设资金|Seek Development Funds from the Overlord|编辑通过。一次真实资金与建设/资质修正，不假称收到军械订单或必须交货。|
|`nesnd_jp_seek_overlord_capital_desc`<br>按钮说明|A2:69；D十.3|请求宗主拨款兴办工场、培养熟练工匠，使本国的生产能够成长。<br><br>获准后，#v 3#! 年内不能再次获得这项资助。|Ask the overlord to fund workshops and the training of skilled workers, giving domestic production room to grow.<br><br>After receiving assistance, further funding is unavailable for #v 3#! years.|编辑通过。一次真实资金与建设/资质修正，不假称收到军械订单或必须交货。|
|`nesnd_jp_seek_capital_cne`<br>按钮标题|A1:302；D五、十|向北朝寻求资金|Seek Capital from the North|编辑通过。目标为实际CNE；不用其共和基名冒称当前政体。以日方寻援理由表达合作，删除尚无事件支持的“北朝有意”既成判断。|
|`nesnd_jp_seek_capital_cne_desc`<br>按钮说明|A1:302；D五、十|以工商业合作为纽带，向北朝争取建设资金，吸引其参与日本的发展。<br><br>获准后，#v 3#! 年内不能再次获得这项资助。|Seek development funds from the northern government, offering closer commercial ties as a reason to support our growing industries.<br><br>After receiving assistance, further funding is unavailable for #v 3#! years.|编辑通过。目标为实际CNE；不用其共和基名冒称当前政体。以日方寻援理由表达合作，删除尚无事件支持的“北朝有意”既成判断。|
|`nesnd_jp_seek_capital_hus`<br>按钮标题|A2:69；D五|向东洲寻求资金|Seek Capital from Dongzhou|编辑通过。目标HUS；中文英文沿东洲专名，不冒称已有贸易条约或军事盟约。|
|`nesnd_jp_seek_capital_hus_desc`<br>按钮说明|A2:69；D五|以通商和工业发展为由，向东洲争取一笔用于工场建设的资金。<br><br>获准后，#v 3#! 年内不能再次获得这项资助。|Approach Dongzhou for funds to build workshops, making the case for closer trade and industrial development.<br><br>After receiving assistance, further funding is unavailable for #v 3#! years.|编辑通过。目标HUS；中文英文沿东洲专名，不冒称已有贸易条约或军事盟约。|
|`nesnd_jp_seek_capital_usm`<br>按钮标题|A1:150、332；D十|向南朝寻求资金|Seek Capital from the South|编辑通过。目标USM，避开明吴阶段误名；给予的是钱与资质，不声称脚本转移实体工匠人口。|
|`nesnd_jp_seek_capital_usm_desc`<br>按钮说明|A1:150、332；D十|南朝与日本的商业联系由来已久。我们可以循着这些关系寻求资助，为本国工场筹集资本、培养工匠。<br><br>获准后，#v 3#! 年内不能再次获得这项资助。|The southern government has long-standing commercial ties with Japan. Draw on these connections to seek funds for workshops and the training of skilled labour.<br><br>After receiving assistance, further funding is unavailable for #v 3#! years.|编辑通过。目标USM，避开明吴阶段误名；给予的是钱与资质，不声称脚本转移实体工匠人口。|
|`nesnd_jp_independence_play`<br>按钮标题|A1:272–274|独立最后通牒|An Ultimatum for Independence|编辑通过。发起原生dp_independence；不写点击后立即脱离宗主或已开战。|
|`nesnd_jp_independence_play_desc`<br>按钮说明|A1:272–274|向宗主提出独立的最后通牒，发起独立[concept_diplomatic_play]，准备以战争迫使其接受。|Issue an ultimatum for independence, opening an independence [concept_diplomatic_play] and preparing to enforce the demand through war.|编辑通过。发起原生dp_independence；不写点击后立即脱离宗主或已开战。|
|`nesnd_jp_union_jap`<br>合邦按钮标题|A1:302；D十|请$JAP$归统|Invite $JAP$ to Join Us|编辑通过。按根任务允许使用现有国家本地化键；不创造GetCountry界面函数。|
|`nesnd_jp_union_jap_desc`<br>合邦按钮说明|A1:302；C-EFF-F kind6|向$JAP$提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。|Propose a union to $JAP$. If accepted, their country will be annexed into ours and governed by our state.|编辑通过。明确接受国被并入，不把annex包装成松散联盟或无主权后果的友好协议；双方权限仍由实际trigger核验。|
|`nesnd_jp_union_jtk`<br>合邦按钮标题|A1:302；D十|请$JTK$归统|Invite $JTK$ to Join Us|编辑通过。按根任务允许使用现有国家本地化键；不创造GetCountry界面函数。|
|`nesnd_jp_union_jtk_desc`<br>合邦按钮说明|A1:302；C-EFF-F kind6|向$JTK$提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。|Propose a union to $JTK$. If accepted, their country will be annexed into ours and governed by our state.|编辑通过。明确接受国被并入，不把annex包装成松散联盟或无主权后果的友好协议；双方权限仍由实际trigger核验。|
|`nesnd_jp_union_jim`<br>合邦按钮标题|A1:302；D十|请$JIM$归统|Invite $JIM$ to Join Us|编辑通过。按根任务允许使用现有国家本地化键；不创造GetCountry界面函数。|
|`nesnd_jp_union_jim_desc`<br>合邦按钮说明|A1:302；C-EFF-F kind6|向$JIM$提出合邦。对方若同意，其国家将并入本国，由我们的政府统辖。|Propose a union to $JIM$. If accepted, their country will be annexed into ours and governed by our state.|编辑通过。明确接受国被并入，不把annex包装成松散联盟或无主权后果的友好协议；双方权限仍由实际trigger核验。|
|`nesnd_jp_korean_governor`<br>朝鲜按钮标题|A2:79；D五|委派总督|Appoint Governors|编辑通过。以税容与集中治理解释政策，动乱影响增加交原生效果显示，不许诺治安改善。|
|`nesnd_jp_korean_governor_desc`<br>朝鲜按钮说明|A2:79；C-EFF-K|任用总督，将朝鲜属地的税务与民政集中起来，使政府能够更直接地掌握当地的收入与事务。<br><br>此后 #v 24#! 个月内不能改换朝鲜治理方针。|Appoint governors to centralize taxation and civil administration in our Korean territories, giving the government closer control over local revenue and affairs.<br><br>Korean policy cannot be changed again for #v 24#! months.|编辑通过。以税容与集中治理解释政策，动乱影响增加交原生效果显示，不许诺治安改善。|
|`nesnd_jp_korean_councils`<br>朝鲜按钮标题|A2:79；D五|设立地方议事会|Establish Local Councils|编辑通过。明确是州治理合作，并非释放KOR或国家自治等级提升；税容代价、教育和动乱数值由原生效果显示。|
|`nesnd_jp_korean_councils_desc`<br>朝鲜按钮说明|A2:79；C-EFF-K|让当地议事会参与民政、兴办学校，以地方人士的合作缓和居民对统治的抵触。<br><br>此后 #v 24#! 个月内不能改换朝鲜治理方针。|Bring local councils into civil administration and education, seeking local cooperation to ease resistance to our rule.<br><br>Korean policy cannot be changed again for #v 24#! months.|编辑通过。明确是州治理合作，并非释放KOR或国家自治等级提升；税容代价、教育和动乱数值由原生效果显示。|
|`nesnd_jp_korean_envoy`<br>朝鲜按钮标题|A2:79；D五|交涉朝鲜归属|Negotiate a Korean Settlement|编辑通过。对方实际答复后才转本国state，不转第三方土地；可无地撤宣称，尚有其他非朝鲜领土条件由入口核验，不复制细节。|
|`nesnd_jp_korean_envoy_desc`<br>朝鲜按钮说明|A2:79；C-EFF-K|向朝鲜或其宗主提出和解。对方若同意，我们将把本国在釜山与两湖的领土移交朝鲜，并放弃对这两个地区的宣称。<br><br>两次遣使须相隔 #v 6#! 个月。|Offer a settlement to Korea or its overlord. If accepted, our holdings in Busan and Yangho will pass to Korea, and we will relinquish our claims to both regions.<br><br>Envoys may be sent once every #v 6#! months.|编辑通过。对方实际答复后才转本国state，不转第三方土地；可无地撤宣称，尚有其他非朝鲜领土条件由入口核验，不复制细节。|
|`nesnd_jp_foreign_workshops`<br>修正名称|A2:73–74；C-MOD-F/K|海外建设资助|Foreign Development Assistance|编辑通过。12个月建造+10%、资质+15%，非运送武器或自动产生建筑。|
|`nesnd_jp_korea_governor`<br>修正名称|A2:73–74；C-MOD-F/K|总督辖治|Government by Governors|编辑通过。本国持有朝鲜州的税容+15%、动乱影响+10%；不误称征税额/激进人口。|
|`nesnd_jp_korea_councils`<br>修正名称|A2:73–74；C-MOD-F/K|地方议事会|Local Councils|编辑通过。州税容-10%、教育可及性+10个百分点、动乱影响-10%；不声称已成立主权国家。|
|`nesnd_jp_korea_administration`<br>修正名称|A2:73–74；C-MOD-F/K|朝鲜行政开支|Korean Administration|编辑通过。国家政府工资+5%，仍有任何本国朝鲜地时的共同成本。|
|`nesnd_jp_foreign.1.t`<br>请求事件标题|A1:260、265、276|来自[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者|An Envoy from [SCOPE.sCountry('jp_sender').GetNameNoFormatting]|编辑通过。保存的sender有reply_valid全链存在守卫，动态显示真正国名。|
|`nesnd_jp_foreign.1.d1`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]希望扩大自行处理国事的权力，要求我们放宽现有宗属关系的约束。使者认为，更大的自主可以让地方政府及时应对国内事务，同时保留两国之间的联系。|[SCOPE.sCountry('jp_sender').GetNameNoFormatting] seeks greater authority over its own affairs and asks us to relax the present subject relationship. The envoy argues that greater autonomy would let the local government respond to domestic needs while preserving ties between our countries.|编辑通过。原生自治升一级，不假称放独立；诉求属于来使立场。|
|`nesnd_jp_foreign.1.d2`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者要求结束藩属关系。他们希望从此自行决定外交、军队与通商事务，并以独立国家的身份同我们往来。这份答复将决定我们是否愿意交出原有的宗主权。|An envoy from [SCOPE.sCountry('jp_sender').GetNameNoFormatting] asks us to end the subject relationship. Their government seeks control over diplomacy, the military and trade, and wishes to deal with us as an independent country. We must decide whether to relinquish our authority as overlord.|编辑通过。真实make_independent由接受触发；接收方知道放弃宗主权。|
|`nesnd_jp_foreign.1.d3`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]希望改造国内的官员任用、军政与议政制度。使者前来寻求我们的认可，以便政府能够召集支持者、推行新政。原有的宗属关系仍将保留。|[SCOPE.sCountry('jp_sender').GetNameNoFormatting] wishes to reform appointments, military administration and political representation. Its envoy seeks our assent so that the government can rally supporters and pursue its programme. The existing subject relationship would remain in place.|编辑通过。国内改革许可与主权分开；不提前决定具体路线/替其改法。|
|`nesnd_jp_foreign.1.d4`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]正为工场建设寻求一笔资金。使者希望我们拨款，帮助他们扩建生产、培养熟练工匠，以日益兴盛的工商业加深双方的往来。|[SCOPE.sCountry('jp_sender').GetNameNoFormatting] is seeking funds for workshop construction. Its envoy asks us for a grant to expand production and train skilled workers, arguing that growing industry would deepen ties between our countries.|编辑通过。接收方支付一次现金，申请方入账并获有限期支持；不描述军械定单或商品义务。|
|`nesnd_jp_foreign.1.d5`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]提出就朝鲜南部的领土问题达成和解。他们愿意放弃对釜山与两湖的宣称，并将本国仍持有的当地领土移交朝鲜。使者要求我们接受这一安排，结束这项长期争端。|[SCOPE.sCountry('jp_sender').GetNameNoFormatting] proposes a settlement over southern Korea. Its government offers to relinquish claims to Busan and Yangho and transfer any territory it still holds there to Korea. The envoy asks us to accept these terms and settle the dispute.|编辑通过。KOR或其实际直接宗主答复均适用；any holdings可为零，转地受本国所有权限制。|
|`nesnd_jp_foreign.1.d6`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]邀请我们结束两国分立，由他们的政府统辖双方的疆土、军队与国事。这意味着我们的国家将并入[SCOPE.sCountry('jp_sender').GetNameNoFormatting]，不再保有单独的政府。决定权仍在我们手中。|[SCOPE.sCountry('jp_sender').GetNameNoFormatting] invites us to end the division between our countries and place both territories and their affairs under its government. Acceptance would annex our country into [SCOPE.sCountry('jp_sender').GetNameNoFormatting] and end our separate government. The decision is ours to make.|编辑通过。明示annex与失去独立政府，避免把玩家失国包装成普通联盟；仅当实际主权/共同宗主授权仍有效时可接受。|
|`nesnd_jp_foreign.1.d7`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]希望得到我们的许可，同其他日本属国商议归并。他们打算由本国政府主持统一，并承诺只有受邀国家同意才结束其单独统治。我们需要决定是否允许这项合邦计划在现有宗属体系内进行。|[SCOPE.sCountry('jp_sender').GetNameNoFormatting] seeks our permission to negotiate union with other Japanese subjects. Its government would lead the union, with each invited country surrendering its separate government only by consent. We must decide whether to allow such negotiations within the existing subject order.|编辑通过。授予同宗主合邦权限，既不即时吞并也不更改所有属国主权；invitedcountry仍有独立接受选项。|
|`nesnd_jp_foreign.1.d`<br>请求事件正文|A1:256、261、266、272；C-EFF-F|[SCOPE.sCountry('jp_sender').GetNameNoFormatting]的使者已经抵达，带来了有关两国关系的提议。他们正在等待我们的答复。|An envoy from [SCOPE.sCountry('jp_sender').GetNameNoFormatting] has arrived with a proposal concerning relations between our countries and awaits our reply.|编辑通过。fallback只用保证存在sender，不虚构未匹配种类的具体条件。|
|`nesnd_jp_foreign.1.a`<br>事件选项|A1:258、274|同意所议。|Accept the proposal.|编辑通过。七类共用真实接受项，结果由原生effect显示；合邦主权后果在对应正文已明确。|
|`nesnd_jp_foreign.1.b`<br>事件选项|A1:270；A2:81|我们不接受这些条件。|We cannot accept these terms.|编辑通过。默认拒绝，不伪造尚未发生的报复战争。|
|`nesnd_jp_foreign.2.t`<br>答复事件标题|A1:260、265、276|[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的答复|The Reply from [SCOPE.sCountry('jp_partner').GetNameNoFormatting]|编辑通过。事件trigger/cancellation保护保存的jp_partner，不另查可能已亡的标签。|
|`nesnd_jp_foreign.3.t`<br>答复事件标题|A1:260、265、276|[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的答复|The Reply from [SCOPE.sCountry('jp_partner').GetNameNoFormatting]|编辑通过。事件trigger/cancellation保护保存的jp_partner，不另查可能已亡的标签。|
|`nesnd_jp_foreign.2.d`<br>接受结果正文|A1:256、261；C-EFF-F|使者带回了[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的答复。对方已经接受我们的提议，双方将依照商定的安排处理此事。|Our envoy has returned with the reply from [SCOPE.sCountry('jp_partner').GetNameNoFormatting]. They have accepted our proposal, and the agreed arrangements will govern the matter.|编辑通过。kind6吞并不调用此事件；适用资助/自治/独立/改革许可/朝鲜/统一许可，不声称六种结果同时发生。|
|`nesnd_jp_foreign.2.a`<br>接受结果选项|A1:258|就按商定的办法办理。|Proceed as agreed.|编辑通过。已结算结果的确认，不再支付或承诺新的效果。|
|`nesnd_jp_foreign.3.d`<br>拒绝结果正文|A1:266、270、297|[SCOPE.sCountry('jp_partner').GetNameNoFormatting]拒绝了使者带去的条件。我们未能说服对方让步，这次交涉也使两国的关系更为紧张。|[SCOPE.sCountry('jp_partner').GetNameNoFormatting] has rejected the terms carried by our envoy. We failed to persuade them to concede, and the exchange has strained relations between our countries.|编辑通过。真实关系-10适用于所有拒绝；不把仅自治/独立才加的自由倾向和羞辱写到其他请求。|
|`nesnd_jp_foreign.3.a`<br>拒绝结果选项|A1:298、305；A2:82|只得另作打算。|We must consider another course.|编辑通过。简短态度，无必然战争/保证重试成功的剧情。|
|`gov_nesnd_japan_lin_regency`<br>既有政体名称|现行摄政replace:2|摄政政府|Regency Government|编辑通过。保留既有专名；其有效性由实际摄政谓词决定。|
|`gov_nesnd_japan_lin_regency_desc`<br>既有政体说明修订|原生gov_regency_empire_desc；现行摄政replace:3|保留天皇名位，由摄政王代行统治、主持政务的君主制政权。|A monarchy in which a Prince-Regent conducts the government on behalf of the imperial sovereign.|编辑通过。删除“奉宗主国之命/commissioned by its overlord”，独立后仍适用；不假称摄政永久在世或复活。|
|`RULER_TITLE_NESND_JAPAN_REGENT`<br>既有统治者称谓|现行摄政replace:4|摄政王|Prince-Regent|编辑通过。保留现行译名；皇帝/女皇继承人复用已存在原生键，不另造称谓。|

## 本批完成边界

共 **66键**：2个JE的标题/正文，8个条件状态，12个外交按钮及3个朝鲜按钮的名称/说明，4个修正名称，3个事件的17个实际引用键，以及3个现有摄政键。7种请求正文另有安全fallback，三事件无新增风味引文。

上述所有候选完成编辑对照。自动检查只核键覆盖、动态表达/数字对称与可疑开发措辞，不以词频替代文风判断。最终装配后应再逐键回读有效覆盖层；未运行引擎，未验证玩家国家吞并、朝鲜转地或存档继承。
